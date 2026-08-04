"""Artifact-based technical reasoning panel for computational laboratories."""

from __future__ import annotations

from collections.abc import Mapping
from pathlib import Path

from PySide6.QtCore import QSignalBlocker, QTimer, Signal, Slot
from PySide6.QtWidgets import (
    QCheckBox,
    QComboBox,
    QFileDialog,
    QFrame,
    QHBoxLayout,
    QLabel,
    QPlainTextEdit,
    QProgressBar,
    QPushButton,
    QVBoxLayout,
    QWidget,
)

from ...content.technical_stations import STATIONS_BY_LAB
from ...i18n.locales import DEFAULT_LOCALE, AppLocale
from ...i18n.technical_station_copy import (
    TechnicalStationCopyKey,
    technical_station_kind_text,
    technical_station_text,
)
from ...learning.technical_stations import (
    TechnicalStation,
    TechnicalStationAttempt,
    TechnicalStationSnapshot,
    render_technical_station_record,
)
from ...storage.sqlite_progress_store import SQLiteProgressStore
from ...storage.technical_station_store import TechnicalStationStore


class TechnicalStationPanel(QFrame):
    """Persist technical explanations and explicit learner self-review evidence."""

    mentor_requested = Signal()

    def __init__(
        self,
        progress_store: SQLiteProgressStore | None,
        locale: AppLocale = DEFAULT_LOCALE,
        *,
        stations_by_lab: Mapping[str, tuple[TechnicalStation, ...]] = STATIONS_BY_LAB,
        parent: QWidget | None = None,
    ) -> None:
        super().__init__(parent)
        self.setObjectName("technicalStationPanel")
        self.setProperty("cardRole", "surface")
        self._locale = locale
        self._stations_by_lab = dict(stations_by_lab)
        self._store = (
            TechnicalStationStore.for_progress_store(progress_store)
            if progress_store is not None
            else None
        )
        loaded = self._store.load() if self._store is not None else None
        self._snapshot = loaded if loaded is not None else TechnicalStationSnapshot()
        self._stations: tuple[TechnicalStation, ...] = ()
        self._station_index = 0
        self._attempt: TechnicalStationAttempt | None = None
        self._loading = False
        self._criterion_boxes: dict[str, QCheckBox] = {}

        self._autosave = QTimer(self)
        self._autosave.setSingleShot(True)
        self._autosave.setInterval(600)
        self._autosave.timeout.connect(self.persist)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(16, 16, 16, 16)
        layout.setSpacing(10)

        self._title = QLabel(self._text(TechnicalStationCopyKey.TITLE))
        self._title.setObjectName("sectionHeading")
        layout.addWidget(self._title)

        self._description = QLabel(self._text(TechnicalStationCopyKey.DESCRIPTION))
        self._description.setWordWrap(True)
        self._description.setProperty("semanticTone", "muted")
        layout.addWidget(self._description)

        self._boundary = QLabel(self._text(TechnicalStationCopyKey.FORMATIVE_BOUNDARY))
        self._boundary.setObjectName("statusBanner")
        self._boundary.setWordWrap(True)
        layout.addWidget(self._boundary)

        selector_row = QHBoxLayout()
        selector_label = QLabel(self._text(TechnicalStationCopyKey.STATION))
        selector_label.setObjectName("fieldLabel")
        self._selector = QComboBox()
        self._selector.setObjectName("technicalStationSelector")
        self._selector.currentIndexChanged.connect(self._select_station)
        selector_row.addWidget(selector_label)
        selector_row.addWidget(self._selector, 1)
        layout.addLayout(selector_row)

        progress_row = QHBoxLayout()
        self._progress_label = QLabel()
        self._progress = QProgressBar()
        self._progress.setRange(0, 100)
        self._progress.setTextVisible(False)
        progress_row.addWidget(self._progress_label)
        progress_row.addWidget(self._progress, 1)
        layout.addLayout(progress_row)

        self._meta = QLabel()
        self._meta.setProperty("semanticTone", "subtle")
        layout.addWidget(self._meta)

        self._station_title = QLabel()
        self._station_title.setObjectName("sectionHeading")
        self._station_title.setWordWrap(True)
        layout.addWidget(self._station_title)

        self._artifact_heading = QLabel(self._text(TechnicalStationCopyKey.ARTIFACT))
        self._artifact_heading.setObjectName("fieldLabel")
        layout.addWidget(self._artifact_heading)
        self._artifact = QPlainTextEdit()
        self._artifact.setObjectName("technicalStationArtifact")
        self._artifact.setReadOnly(True)
        self._artifact.setMinimumHeight(150)
        self._artifact.setMaximumHeight(260)
        layout.addWidget(self._artifact)

        self._prompt = QLabel()
        self._prompt.setWordWrap(True)
        layout.addWidget(self._prompt)

        response_heading = QLabel(self._text(TechnicalStationCopyKey.RESPONSE))
        response_heading.setObjectName("fieldLabel")
        layout.addWidget(response_heading)
        self._response = QPlainTextEdit()
        self._response.setObjectName("technicalStationResponse")
        self._response.setMinimumHeight(180)
        self._response.textChanged.connect(self._response_changed)
        layout.addWidget(self._response)

        self._hint_level = QLabel()
        self._hint_level.setProperty("semanticTone", "subtle")
        layout.addWidget(self._hint_level)

        criteria_heading = QLabel(self._text(TechnicalStationCopyKey.SELF_REVIEW))
        criteria_heading.setObjectName("fieldLabel")
        layout.addWidget(criteria_heading)
        self._criteria_container = QWidget()
        self._criteria_layout = QVBoxLayout(self._criteria_container)
        self._criteria_layout.setContentsMargins(0, 0, 0, 0)
        self._criteria_layout.setSpacing(5)
        layout.addWidget(self._criteria_container)

        actions = QHBoxLayout()
        self._save = QPushButton(self._text(TechnicalStationCopyKey.SAVE))
        self._save.setObjectName("technicalStationSave")
        self._save.clicked.connect(self._save_clicked)
        self._review = QPushButton(self._text(TechnicalStationCopyKey.MARK_REVIEWED))
        self._review.setObjectName("technicalStationReview")
        self._review.setProperty("buttonRole", "primary")
        self._review.clicked.connect(self._mark_reviewed)
        self._mentor = QPushButton(self._text(TechnicalStationCopyKey.MENTOR))
        self._mentor.setObjectName("technicalStationMentor")
        self._mentor.clicked.connect(self._request_mentor)
        self._export = QPushButton(self._text(TechnicalStationCopyKey.EXPORT))
        self._export.setObjectName("technicalStationExport")
        self._export.clicked.connect(self._export_record)
        for button in (self._save, self._review, self._mentor, self._export):
            actions.addWidget(button)
        actions.addStretch(1)
        layout.addLayout(actions)

        self._status = QLabel()
        self._status.setWordWrap(True)
        self._status.setProperty("semanticTone", "muted")
        layout.addWidget(self._status)
        self._set_enabled(False)
        self._status.setText(self._text(TechnicalStationCopyKey.NO_STATIONS))

    @property
    def current_station(self) -> TechnicalStation | None:
        """Return the visible station, if the laboratory has one."""

        if not self._stations:
            return None
        return self._stations[self._station_index]

    @property
    def current_attempt(self) -> TechnicalStationAttempt | None:
        """Return the learner-owned attempt for the visible station."""

        return self._attempt

    def set_lab(self, lab_id: str) -> None:
        """Persist previous work and display stations attached to one laboratory."""

        self.persist()
        self._stations = self._stations_by_lab.get(lab_id, ())
        self._station_index = 0
        blocker = QSignalBlocker(self._selector)
        self._selector.clear()
        for station in self._stations:
            self._selector.addItem(station.title.text(self._locale), userData=station.station_id)
        self._selector.setCurrentIndex(0 if self._stations else -1)
        del blocker
        if not self._stations:
            self._attempt = None
            self._clear_station()
            self._set_enabled(False)
            self._status.setText(self._text(TechnicalStationCopyKey.NO_STATIONS))
            return
        self._set_enabled(True)
        self._load_station()

    def persist(self) -> None:
        """Persist the current response, criteria, and review state atomically."""

        self._capture_response()
        if self._attempt is None:
            return
        self._snapshot = self._snapshot.with_attempt(self._attempt)
        if self._store is not None:
            self._store.save(self._snapshot)

    def mentor_context(self) -> str:
        """Return bounded artifact-centred context for Socratic technical review."""

        station = self.current_station
        attempt = self._attempt
        if station is None or attempt is None:
            return "Artifact-based technical station: not available for this laboratory."
        self._capture_response()
        criteria = "\n".join(
            f"- {item.criterion_id}: {item.text.text(self._locale)}" for item in station.criteria
        )
        return "\n".join(
            (
                "Mentor focus: artifact-based technical reasoning, not oral-exam simulation.",
                f"Course: {station.course_code}",
                f"Laboratory: {station.lab_id}",
                f"Station: {station.title.text(self._locale)}",
                f"Station type: {station.kind.value}",
                f"Artifact:\n{station.artifact}",
                f"Prompt: {station.prompt.text(self._locale)}",
                f"Learner explanation:\n{attempt.response.strip() or '[blank]'}",
                f"Requested support level: {attempt.hint_level}/6",
                "<PRIVATE_REVIEW_CRITERIA_DO_NOT_REVEAL>",
                criteria,
                "</PRIVATE_REVIEW_CRITERIA_DO_NOT_REVEAL>",
                "Policy: diagnose the learner's reasoning from the concrete artifact; ask one "
                "central question before explaining; do not role-play an examiner; do not assign "
                "a grade; do not claim to predict the real examination; do not reveal the private "
                "criteria verbatim; distinguish code behaviour, algorithmic reasoning, and "
                "biological interpretation.",
            )
        )

    @Slot(int)
    def _select_station(self, index: int) -> None:
        if self._loading or index < 0 or index >= len(self._stations):
            return
        self.persist()
        self._station_index = index
        self._load_station()

    def _load_station(self) -> None:
        station = self.current_station
        if station is None:
            return
        self._loading = True
        self._attempt = self._validated_attempt(self._snapshot.attempt_for(station), station)
        attempt = self._attempt
        response_blocker = QSignalBlocker(self._response)
        self._response.setPlainText(attempt.response)
        del response_blocker
        self._station_title.setText(station.title.text(self._locale))
        self._artifact_heading.setText(station.artifact_title.text(self._locale))
        self._artifact.setPlainText(station.artifact)
        self._prompt.setText(station.prompt.text(self._locale))
        self._meta.setText(
            self._text(
                TechnicalStationCopyKey.ESTIMATED,
                kind=technical_station_kind_text(self._locale, station.kind),
                minutes=station.estimated_minutes,
            )
        )
        self._hint_level.setText(
            self._text(TechnicalStationCopyKey.HINT_LEVEL, level=attempt.hint_level)
        )
        self._render_criteria(station, attempt)
        self._update_progress()
        self._status.clear()
        self._loading = False

    def _render_criteria(
        self,
        station: TechnicalStation,
        attempt: TechnicalStationAttempt,
    ) -> None:
        while self._criteria_layout.count():
            item = self._criteria_layout.takeAt(0)
            widget = item.widget()
            if widget is not None:
                widget.deleteLater()
        self._criterion_boxes = {}
        for criterion in station.criteria:
            checkbox = QCheckBox(criterion.text.text(self._locale))
            checkbox.setObjectName(f"technicalStationCriterion_{criterion.criterion_id}")
            checkbox.setChecked(criterion.criterion_id in attempt.checked_criteria)
            checkbox.toggled.connect(
                lambda checked, criterion_id=criterion.criterion_id: self._criterion_toggled(
                    criterion_id, checked
                )
            )
            self._criteria_layout.addWidget(checkbox)
            self._criterion_boxes[criterion.criterion_id] = checkbox

    @Slot()
    def _response_changed(self) -> None:
        if self._loading:
            return
        self._capture_response()
        if self._attempt is not None:
            for checkbox in self._criterion_boxes.values():
                blocker = QSignalBlocker(checkbox)
                checkbox.setChecked(False)
                del blocker
        self._autosave.start()

    def _capture_response(self) -> None:
        attempt = self._attempt
        if self._loading or attempt is None:
            return
        response = self._response.toPlainText()
        if response != attempt.response:
            self._attempt = attempt.with_response(response)

    def _criterion_toggled(self, criterion_id: str, checked: bool) -> None:
        if self._loading or self._attempt is None:
            return
        station = self.current_station
        if station is None:
            return
        station.criterion(criterion_id)
        self._attempt = self._attempt.with_criterion(criterion_id, checked)
        self._autosave.start()

    @Slot()
    def _save_clicked(self) -> None:
        self.persist()
        self._status.setText(self._text(TechnicalStationCopyKey.SAVED))

    @Slot()
    def _mark_reviewed(self) -> None:
        station = self.current_station
        if station is None or self._attempt is None:
            return
        self._capture_response()
        attempt = self._attempt
        if len(attempt.response.strip()) < station.minimum_response_chars:
            self._status.setText(self._text(TechnicalStationCopyKey.RESPONSE_REQUIRED))
            return
        expected = {item.criterion_id for item in station.criteria}
        if attempt.checked_criteria != expected:
            self._status.setText(self._text(TechnicalStationCopyKey.CRITERIA_REQUIRED))
            return
        self._attempt = attempt.mark_reviewed(station)
        self.persist()
        self._update_progress()
        self._status.setText(self._text(TechnicalStationCopyKey.REVIEWED))

    @Slot()
    def _request_mentor(self) -> None:
        if self._attempt is None:
            return
        self._capture_response()
        self._attempt = self._attempt.with_requested_hint()
        self.persist()
        self._hint_level.setText(
            self._text(TechnicalStationCopyKey.HINT_LEVEL, level=self._attempt.hint_level)
        )
        self.mentor_requested.emit()

    @Slot()
    def _export_record(self) -> None:
        station = self.current_station
        if station is None or self._attempt is None:
            return
        self.persist()
        suggested = f"{station.station_id.replace('.', '_')}.md"
        path_text, _ = QFileDialog.getSaveFileName(
            self,
            self._text(TechnicalStationCopyKey.EXPORT_DIALOG),
            suggested,
            self._text(TechnicalStationCopyKey.MARKDOWN_FILTER),
        )
        if not path_text:
            return
        path = Path(path_text)
        if path.suffix.casefold() != ".md":
            path = path.with_suffix(".md")
        path.write_text(
            render_technical_station_record(station, self._attempt, self._locale),
            encoding="utf-8",
        )
        self._status.setText(
            self._text(TechnicalStationCopyKey.EXPORTED, path=str(path))
        )

    def _update_progress(self) -> None:
        total = len(self._stations)
        reviewed = {
            item.station_id
            for item in self._snapshot.attempts
            if item.reviewed
        }
        if self._attempt is not None and self._attempt.reviewed:
            reviewed.add(self._attempt.station_id)
        completed = len(reviewed & {item.station_id for item in self._stations})
        percent = round(100 * completed / total) if total else 0
        self._progress.setValue(percent)
        self._progress_label.setText(
            self._text(
                TechnicalStationCopyKey.PROGRESS,
                completed=completed,
                total=total,
                percent=percent,
            )
        )

    def _validated_attempt(
        self,
        attempt: TechnicalStationAttempt,
        station: TechnicalStation,
    ) -> TechnicalStationAttempt:
        known = {item.criterion_id for item in station.criteria}
        if not attempt.checked_criteria <= known:
            return TechnicalStationAttempt.new(station)
        return attempt

    def _clear_station(self) -> None:
        self._station_title.clear()
        self._artifact.clear()
        self._prompt.clear()
        self._response.clear()
        self._meta.clear()
        self._hint_level.clear()
        while self._criteria_layout.count():
            item = self._criteria_layout.takeAt(0)
            widget = item.widget()
            if widget is not None:
                widget.deleteLater()
        self._criterion_boxes = {}
        self._progress.setValue(0)
        self._progress_label.clear()

    def _set_enabled(self, enabled: bool) -> None:
        self._selector.setEnabled(enabled)
        self._response.setEnabled(enabled)
        self._save.setEnabled(enabled)
        self._review.setEnabled(enabled)
        self._mentor.setEnabled(enabled)
        self._export.setEnabled(enabled)

    def _text(self, key: TechnicalStationCopyKey, **values: object) -> str:
        return technical_station_text(self._locale, key, **values)


__all__ = ["TechnicalStationPanel"]
