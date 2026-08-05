"""Persistent weekly plan-execute-review panel for the DM857 group project."""

from __future__ import annotations

from datetime import date

from PySide6.QtCore import QSignalBlocker, QTimer, Signal
from PySide6.QtWidgets import (
    QCheckBox,
    QComboBox,
    QFormLayout,
    QFrame,
    QGroupBox,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QPlainTextEdit,
    QProgressBar,
    QPushButton,
    QVBoxLayout,
    QWidget,
)

from ...i18n.dm857_weekly_supervision_copy import (
    WeeklySupervisionCopyKey,
    weekly_cycle_status_text,
    weekly_supervision_text,
)
from ...i18n.locales import DEFAULT_LOCALE, AppLocale
from ...learning.dm857_weekly_supervision import (
    DM857WeeklyCycle,
    DM857WeeklySupervisionSnapshot,
)
from ...storage.dm857_weekly_supervision_store import DM857WeeklySupervisionStore
from ...storage.sqlite_progress_store import SQLiteProgressStore

_REQUIRED_EVIDENCE_TOTAL = 9


class DM857WeeklySupervisionPanel(QFrame):
    """Track longitudinal project evidence without claiming academic mastery."""

    mentor_requested = Signal()

    def __init__(
        self,
        progress_store: SQLiteProgressStore | None,
        locale: AppLocale = DEFAULT_LOCALE,
        *,
        supervision_store: DM857WeeklySupervisionStore | None = None,
        today: date | None = None,
        parent: QWidget | None = None,
    ) -> None:
        super().__init__(parent)
        self.setObjectName("weeklySupervisionPanel")
        self.setProperty("cardRole", "surface")
        self._locale = locale
        self._today = today or date.today()
        self._store = supervision_store
        if self._store is None and progress_store is not None:
            self._store = DM857WeeklySupervisionStore.for_progress_store(progress_store)
        loaded = self._store.load() if self._store is not None else None
        self._snapshot = loaded or DM857WeeklySupervisionSnapshot.empty()
        if not self._snapshot.cycles:
            first_cycle = DM857WeeklyCycle.empty(self._snapshot.next_week_start(self._today))
            self._snapshot = self._snapshot.with_cycle(first_cycle)
        self._current_cycle_id = self._snapshot.selected_cycle_id or self._snapshot.cycles[-1].cycle_id
        self._loading = False

        self._autosave = QTimer(self)
        self._autosave.setSingleShot(True)
        self._autosave.setInterval(600)
        self._autosave.timeout.connect(self.persist)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(16, 16, 16, 16)
        layout.setSpacing(10)

        title = QLabel(self._text(WeeklySupervisionCopyKey.TITLE))
        title.setObjectName("sectionHeading")
        layout.addWidget(title)

        description = QLabel(self._text(WeeklySupervisionCopyKey.DESCRIPTION))
        description.setWordWrap(True)
        description.setProperty("semanticTone", "muted")
        layout.addWidget(description)

        boundary = QLabel(self._text(WeeklySupervisionCopyKey.BOUNDARY))
        boundary.setObjectName("statusBanner")
        boundary.setWordWrap(True)
        layout.addWidget(boundary)

        selector_row = QHBoxLayout()
        selector_row.addWidget(QLabel(self._text(WeeklySupervisionCopyKey.WEEK)))
        self._selector = QComboBox()
        self._selector.setObjectName("weeklyCycleSelector")
        self._selector.currentIndexChanged.connect(self._select_cycle)
        self._new_week = QPushButton(self._text(WeeklySupervisionCopyKey.NEW_WEEK))
        self._new_week.setObjectName("weeklyNewCycleButton")
        self._new_week.clicked.connect(self._create_next_week)
        selector_row.addWidget(self._selector, 1)
        selector_row.addWidget(self._new_week)
        layout.addLayout(selector_row)

        progress_row = QHBoxLayout()
        self._progress_label = QLabel()
        self._progress_label.setObjectName("weeklyProgressLabel")
        self._progress = QProgressBar()
        self._progress.setObjectName("weeklyProgressBar")
        self._progress.setRange(0, 100)
        self._progress.setTextVisible(False)
        progress_row.addWidget(self._progress_label)
        progress_row.addWidget(self._progress, 1)
        layout.addLayout(progress_row)

        planning = QGroupBox(self._text(WeeklySupervisionCopyKey.PLANNING))
        planning_form = QFormLayout(planning)
        self._objective = self._multiline_editor("weeklyObjective", maximum_height=90)
        self._objective.setPlaceholderText(
            self._text(WeeklySupervisionCopyKey.OBJECTIVE_PLACEHOLDER)
        )
        self._success_criteria = self._multiline_editor(
            "weeklySuccessCriteria",
            maximum_height=100,
        )
        self._success_criteria.setPlaceholderText(
            self._text(WeeklySupervisionCopyKey.SUCCESS_PLACEHOLDER)
        )
        planning_form.addRow(
            self._text(WeeklySupervisionCopyKey.OBJECTIVE),
            self._objective,
        )
        planning_form.addRow(
            self._text(WeeklySupervisionCopyKey.SUCCESS_CRITERIA),
            self._success_criteria,
        )
        layout.addWidget(planning)

        repository = QGroupBox(self._text(WeeklySupervisionCopyKey.REPOSITORY_EVIDENCE))
        repository_form = QFormLayout(repository)
        self._start_reference = QLineEdit()
        self._start_reference.setObjectName("weeklyStartReference")
        self._start_reference.setPlaceholderText(
            self._text(WeeklySupervisionCopyKey.REFERENCE_PLACEHOLDER)
        )
        self._start_reference.textChanged.connect(self._schedule_save)
        self._end_reference = QLineEdit()
        self._end_reference.setObjectName("weeklyEndReference")
        self._end_reference.setPlaceholderText(
            self._text(WeeklySupervisionCopyKey.REFERENCE_PLACEHOLDER)
        )
        self._end_reference.textChanged.connect(self._schedule_save)
        self._changed_files = self._multiline_editor("weeklyChangedFiles", maximum_height=90)
        self._test_evidence = self._multiline_editor("weeklyTestEvidence", maximum_height=120)
        repository_form.addRow(
            self._text(WeeklySupervisionCopyKey.START_REFERENCE),
            self._start_reference,
        )
        repository_form.addRow(
            self._text(WeeklySupervisionCopyKey.END_REFERENCE),
            self._end_reference,
        )
        repository_form.addRow(
            self._text(WeeklySupervisionCopyKey.CHANGED_FILES),
            self._changed_files,
        )
        repository_form.addRow(
            self._text(WeeklySupervisionCopyKey.TEST_EVIDENCE),
            self._test_evidence,
        )
        layout.addWidget(repository)

        reasoning = QGroupBox(self._text(WeeklySupervisionCopyKey.REASONING))
        reasoning_form = QFormLayout(reasoning)
        self._decision_rationale = self._multiline_editor(
            "weeklyDecisionRationale",
            maximum_height=120,
        )
        self._individual_contribution = self._multiline_editor(
            "weeklyIndividualContribution",
            maximum_height=110,
        )
        self._biomedical_interpretation = self._multiline_editor(
            "weeklyBiomedicalInterpretation",
            maximum_height=110,
        )
        self._blocked = QCheckBox(self._text(WeeklySupervisionCopyKey.BLOCKED))
        self._blocked.setObjectName("weeklyBlocked")
        self._blocked.toggled.connect(self._schedule_save)
        self._blockers = self._multiline_editor("weeklyBlockers", maximum_height=100)
        reasoning_form.addRow(
            self._text(WeeklySupervisionCopyKey.DECISION_RATIONALE),
            self._decision_rationale,
        )
        reasoning_form.addRow(
            self._text(WeeklySupervisionCopyKey.INDIVIDUAL_CONTRIBUTION),
            self._individual_contribution,
        )
        reasoning_form.addRow(
            self._text(WeeklySupervisionCopyKey.BIOMEDICAL_INTERPRETATION),
            self._biomedical_interpretation,
        )
        reasoning_form.addRow("", self._blocked)
        reasoning_form.addRow(
            self._text(WeeklySupervisionCopyKey.BLOCKERS),
            self._blockers,
        )
        layout.addWidget(reasoning)

        review = QGroupBox(self._text(WeeklySupervisionCopyKey.REVIEW))
        review_form = QFormLayout(review)
        self._reflection = self._multiline_editor("weeklyReflection", maximum_height=120)
        self._next_commitment = self._multiline_editor(
            "weeklyNextCommitment",
            maximum_height=100,
        )
        review_form.addRow(
            self._text(WeeklySupervisionCopyKey.REFLECTION),
            self._reflection,
        )
        review_form.addRow(
            self._text(WeeklySupervisionCopyKey.NEXT_COMMITMENT),
            self._next_commitment,
        )
        layout.addWidget(review)

        actions = QHBoxLayout()
        self._save = QPushButton(self._text(WeeklySupervisionCopyKey.SAVE))
        self._save.setObjectName("weeklySaveButton")
        self._save.setProperty("buttonRole", "primary")
        self._save.clicked.connect(lambda _checked=False: self.persist())
        self._mentor = QPushButton(self._text(WeeklySupervisionCopyKey.MENTOR))
        self._mentor.setObjectName("weeklyMentorButton")
        self._mentor.clicked.connect(lambda _checked=False: self._request_mentor())
        self._save_status = QLabel()
        self._save_status.setObjectName("weeklySaveStatus")
        actions.addWidget(self._save)
        actions.addWidget(self._mentor)
        actions.addWidget(self._save_status, 1)
        layout.addLayout(actions)

        self._reload_selector()
        self._load_current_cycle()

    @property
    def snapshot(self) -> DM857WeeklySupervisionSnapshot:
        """Return the latest captured longitudinal history."""

        return self._capture_snapshot()

    @property
    def current_cycle(self) -> DM857WeeklyCycle:
        """Return the selected cycle including unsaved editor values."""

        return self._capture_cycle()

    def persist(self) -> None:
        """Capture and atomically persist the current weekly cycle."""

        self._autosave.stop()
        self._snapshot = self._capture_snapshot()
        if self._store is not None:
            self._store.save(self._snapshot)
        self._save_status.setText(self._text(WeeklySupervisionCopyKey.SAVED))
        self._refresh_summary(self._snapshot.cycle(self._current_cycle_id))
        self._refresh_selector_labels()

    def mentor_context(self) -> str:
        """Return bounded weekly evidence for Socratic project supervision."""

        cycle = self._capture_cycle()
        return "\n".join(
            (
                "Mentor focus: longitudinal DM857 project supervision.",
                f"Week starting: {cycle.week_start.isoformat()}",
                f"Derived status: {cycle.status.value}",
                f"Evidence completeness: {cycle.completion_percent}%",
                f"Weekly objective: {cycle.objective or '[blank]'}",
                f"Success criteria: {cycle.success_criteria or '[blank]'}",
                f"Start repository reference: {cycle.start_reference or '[blank]'}",
                f"End repository reference: {cycle.end_reference or '[blank]'}",
                f"Changed files or components: {cycle.changed_files or '[blank]'}",
                f"Test evidence: {cycle.test_evidence or '[blank]'}",
                f"Technical decision and rationale: {cycle.decision_rationale or '[blank]'}",
                f"Individual contribution: {cycle.individual_contribution or '[blank]'}",
                "Biomedical interpretation or relevance: "
                f"{cycle.biomedical_interpretation or '[blank]'}",
                f"Blocked: {'yes' if cycle.blocked else 'no'}",
                f"Blockers and dependencies: {cycle.blockers or '[blank]'}",
                f"Reflection: {cycle.reflection or '[blank]'}",
                f"Next commitment: {cycle.next_commitment or '[blank]'}",
                "Policy: ask one central diagnostic question before giving advice; distinguish "
                "repository evidence from learner interpretation; identify missing verification; "
                "do not assign an official grade or claim mastery; do not invent repository facts; "
                "end with one concrete, testable next commitment.",
            )
        )

    def _multiline_editor(self, object_name: str, *, maximum_height: int) -> QPlainTextEdit:
        editor = QPlainTextEdit()
        editor.setObjectName(object_name)
        editor.setMaximumHeight(maximum_height)
        editor.textChanged.connect(self._schedule_save)
        return editor

    def _capture_cycle(self) -> DM857WeeklyCycle:
        cycle = self._snapshot.cycle(self._current_cycle_id)
        return cycle.with_fields(
            objective=self._objective.toPlainText(),
            success_criteria=self._success_criteria.toPlainText(),
            start_reference=self._start_reference.text(),
            end_reference=self._end_reference.text(),
            changed_files=self._changed_files.toPlainText(),
            test_evidence=self._test_evidence.toPlainText(),
            decision_rationale=self._decision_rationale.toPlainText(),
            individual_contribution=self._individual_contribution.toPlainText(),
            biomedical_interpretation=self._biomedical_interpretation.toPlainText(),
            blockers=self._blockers.toPlainText(),
            reflection=self._reflection.toPlainText(),
            next_commitment=self._next_commitment.toPlainText(),
            blocked=self._blocked.isChecked(),
        )

    def _capture_snapshot(self) -> DM857WeeklySupervisionSnapshot:
        return self._snapshot.with_cycle(self._capture_cycle(), select=True)

    def _load_current_cycle(self) -> None:
        cycle = self._snapshot.cycle(self._current_cycle_id)
        self._loading = True
        self._objective.setPlainText(cycle.objective)
        self._success_criteria.setPlainText(cycle.success_criteria)
        self._start_reference.setText(cycle.start_reference)
        self._end_reference.setText(cycle.end_reference)
        self._changed_files.setPlainText(cycle.changed_files)
        self._test_evidence.setPlainText(cycle.test_evidence)
        self._decision_rationale.setPlainText(cycle.decision_rationale)
        self._individual_contribution.setPlainText(cycle.individual_contribution)
        self._biomedical_interpretation.setPlainText(cycle.biomedical_interpretation)
        self._blocked.setChecked(cycle.blocked)
        self._blockers.setPlainText(cycle.blockers)
        self._reflection.setPlainText(cycle.reflection)
        self._next_commitment.setPlainText(cycle.next_commitment)
        self._loading = False
        self._save_status.setText(
            self._text(WeeklySupervisionCopyKey.EMPTY_HINT)
            if cycle.status.value == "empty"
            else ""
        )
        self._refresh_summary(cycle)

    def _reload_selector(self) -> None:
        blocker = QSignalBlocker(self._selector)
        self._selector.clear()
        for cycle in self._snapshot.cycles:
            self._selector.addItem(self._selector_text(cycle), userData=cycle.cycle_id)
        index = self._selector.findData(self._current_cycle_id)
        self._selector.setCurrentIndex(index)
        del blocker

    def _refresh_selector_labels(self) -> None:
        blocker = QSignalBlocker(self._selector)
        for index, cycle in enumerate(self._snapshot.cycles):
            self._selector.setItemText(index, self._selector_text(cycle))
        del blocker

    def _selector_text(self, cycle: DM857WeeklyCycle) -> str:
        status = weekly_cycle_status_text(self._locale, cycle.status)
        return f"{cycle.week_start.isoformat()} · {status}"

    def _refresh_summary(self, cycle: DM857WeeklyCycle) -> None:
        status = weekly_cycle_status_text(self._locale, cycle.status)
        self._progress.setValue(cycle.completion_percent)
        self._progress_label.setText(
            self._text(
                WeeklySupervisionCopyKey.PROGRESS,
                status=status,
                completed=cycle.required_evidence_count,
                total=_REQUIRED_EVIDENCE_TOTAL,
                percent=cycle.completion_percent,
            )
        )
        self._progress_label.setProperty("weeklyCycleStatus", cycle.status.value)

    def _schedule_save(self, *_: object) -> None:
        if self._loading:
            return
        self._save_status.clear()
        self._autosave.start()
        self._refresh_summary(self._capture_cycle())

    def _select_cycle(self, index: int) -> None:
        if self._loading or index < 0:
            return
        cycle_id = self._selector.itemData(index)
        if not isinstance(cycle_id, str) or cycle_id == self._current_cycle_id:
            return
        self.persist()
        self._current_cycle_id = cycle_id
        self._snapshot = self._snapshot.select(cycle_id)
        self._load_current_cycle()

    def _create_next_week(self, _checked: bool = False) -> None:
        del _checked
        self.persist()
        cycle = DM857WeeklyCycle.empty(self._snapshot.next_week_start(self._today))
        self._snapshot = self._snapshot.with_cycle(cycle)
        self._current_cycle_id = cycle.cycle_id
        if self._store is not None:
            self._store.save(self._snapshot)
        self._reload_selector()
        self._load_current_cycle()

    def _request_mentor(self) -> None:
        self.persist()
        self.mentor_requested.emit()

    def _text(self, key: WeeklySupervisionCopyKey, **values: object) -> str:
        return weekly_supervision_text(self._locale, key, **values)


__all__ = ["DM857WeeklySupervisionPanel"]
