"""Persistent PySide6 workflow for the DM857 group project and report scaffold."""

from __future__ import annotations

from datetime import UTC, datetime

from PySide6.QtCore import QTimer, Signal
from PySide6.QtWidgets import (
    QCheckBox,
    QComboBox,
    QFormLayout,
    QGroupBox,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QPlainTextEdit,
    QProgressBar,
    QPushButton,
    QScrollArea,
    QVBoxLayout,
    QWidget,
)

from ...content.technical_stations import DM857_PROJECT_ID
from ...i18n import DEFAULT_LOCALE, AppLocale
from ...i18n.capstone_copy import (
    CapstoneCopyKey,
    capstone_milestone_copy,
    capstone_rubric_text,
    capstone_text,
)
from ...learning.dm857_capstone import (
    DM857_CAPSTONE_MILESTONES,
    DM857_CAPSTONE_RUBRIC,
    CapstoneMilestoneProgress,
    CapstoneMilestoneSpec,
    CapstoneMilestoneStatus,
    DM857CapstoneProgress,
)
from ...storage import DM857CapstoneStore, SQLiteProgressStore
from ..widgets.technical_station_panel import TechnicalStationPanel


class CapstoneMilestoneEditor(QGroupBox):
    """Edit checklist and repository evidence for one stable milestone."""

    changed = Signal()

    def __init__(
        self,
        spec: CapstoneMilestoneSpec,
        progress: CapstoneMilestoneProgress,
        locale: AppLocale,
        parent: QWidget | None = None,
    ) -> None:
        title, description, checklist_labels = capstone_milestone_copy(
            locale,
            spec.milestone_id,
        )
        super().__init__(title, parent)
        self.setObjectName("capstoneMilestone")
        self.setProperty("milestoneId", spec.milestone_id)
        self._spec = spec
        self._locale = locale
        self._checkboxes: dict[str, QCheckBox] = {}

        description_label = QLabel(description)
        description_label.setObjectName("capstoneMilestoneDescription")
        description_label.setWordWrap(True)

        self._status = QLabel()
        self._status.setObjectName("capstoneMilestoneStatus")

        layout = QVBoxLayout(self)
        layout.addWidget(description_label)
        layout.addWidget(self._status)

        completed = set(progress.completed_item_ids)
        for item_id, label in zip(
            spec.checklist_item_ids,
            checklist_labels,
            strict=True,
        ):
            checkbox = QCheckBox(label)
            checkbox.setObjectName("capstoneChecklistItem")
            checkbox.setProperty("checklistItemId", item_id)
            checkbox.setChecked(item_id in completed)
            checkbox.toggled.connect(lambda _checked: self.changed.emit())
            self._checkboxes[item_id] = checkbox
            layout.addWidget(checkbox)

        evidence_label = QLabel(capstone_text(locale, CapstoneCopyKey.EVIDENCE_NOTE))
        self._evidence = QPlainTextEdit(progress.evidence_note)
        self._evidence.setObjectName("capstoneEvidenceNote")
        self._evidence.setPlaceholderText(
            capstone_text(locale, CapstoneCopyKey.EVIDENCE_PLACEHOLDER)
        )
        self._evidence.setMaximumHeight(100)
        self._evidence.textChanged.connect(self.changed.emit)

        commit_label = QLabel(capstone_text(locale, CapstoneCopyKey.COMMIT_REFERENCE))
        self._commit = QLineEdit(progress.commit_reference)
        self._commit.setObjectName("capstoneCommitReference")
        self._commit.setPlaceholderText(capstone_text(locale, CapstoneCopyKey.COMMIT_PLACEHOLDER))
        self._commit.textChanged.connect(lambda _text: self.changed.emit())

        layout.addWidget(evidence_label)
        layout.addWidget(self._evidence)
        layout.addWidget(commit_label)
        layout.addWidget(self._commit)
        self.refresh_status(progress.status)

    @property
    def milestone_id(self) -> str:
        return self._spec.milestone_id

    def progress(self) -> CapstoneMilestoneProgress:
        """Materialize the current editor state with stable checklist identities."""

        completed = tuple(
            item_id
            for item_id in self._spec.checklist_item_ids
            if self._checkboxes[item_id].isChecked()
        )
        return CapstoneMilestoneProgress(
            milestone_id=self._spec.milestone_id,
            completed_item_ids=completed,
            evidence_note=self._evidence.toPlainText().strip(),
            commit_reference=self._commit.text().strip(),
        )

    def refresh_status(self, status: CapstoneMilestoneStatus) -> None:
        """Render the localized derived readiness state."""

        key = {
            CapstoneMilestoneStatus.NOT_STARTED: CapstoneCopyKey.STATUS_NOT_STARTED,
            CapstoneMilestoneStatus.IN_PROGRESS: CapstoneCopyKey.STATUS_IN_PROGRESS,
            CapstoneMilestoneStatus.READY: CapstoneCopyKey.STATUS_READY,
        }[status]
        self._status.setText(capstone_text(self._locale, key))
        self._status.setProperty("milestoneStatus", status.value)


class DM857CapstonePage(QWidget):
    """Guide and persist one evidence-backed DM857 capstone preparation project."""

    mentor_requested = Signal()

    def __init__(
        self,
        progress_store: SQLiteProgressStore | None,
        locale: AppLocale = DEFAULT_LOCALE,
        *,
        capstone_store: DM857CapstoneStore | None = None,
        parent: QWidget | None = None,
    ) -> None:
        super().__init__(parent)
        self.setObjectName("dm857CapstonePage")
        self._locale = locale
        self._store = capstone_store
        if self._store is None and progress_store is not None:
            self._store = DM857CapstoneStore.for_progress_store(progress_store)
        loaded = self._store.load() if self._store is not None else None
        self._progress = loaded or DM857CapstoneProgress.empty()
        self._milestone_editors: dict[str, CapstoneMilestoneEditor] = {}
        self._rubric_scores: dict[str, QComboBox] = {}

        self._save_timer = QTimer(self)
        self._save_timer.setSingleShot(True)
        self._save_timer.setInterval(300)
        self._save_timer.timeout.connect(self.persist)

        root = QVBoxLayout(self)
        root.setContentsMargins(0, 0, 0, 0)

        scroll = QScrollArea()
        scroll.setObjectName("capstoneScroll")
        scroll.setWidgetResizable(True)
        body = QWidget()
        body.setObjectName("capstoneBody")
        layout = QVBoxLayout(body)
        layout.setContentsMargins(4, 4, 12, 20)
        layout.setSpacing(14)

        title = QLabel(capstone_text(locale, CapstoneCopyKey.TITLE))
        title.setObjectName("capstoneTitle")
        boundary = QLabel(capstone_text(locale, CapstoneCopyKey.SOURCE_BOUNDARY))
        boundary.setObjectName("capstoneSourceBoundary")
        boundary.setWordWrap(True)
        layout.addWidget(title)
        layout.addWidget(boundary)

        metadata = QGroupBox(capstone_text(locale, CapstoneCopyKey.METADATA))
        metadata.setObjectName("capstoneMetadata")
        form = QFormLayout(metadata)
        self._project_title = QLineEdit(self._progress.project_title)
        self._project_title.setObjectName("capstoneProjectTitle")
        self._group_members = QLineEdit(", ".join(self._progress.group_members))
        self._group_members.setObjectName("capstoneGroupMembers")
        self._group_members.setPlaceholderText(
            capstone_text(locale, CapstoneCopyKey.GROUP_PLACEHOLDER)
        )
        self._repository_url = QLineEdit(self._progress.repository_url)
        self._repository_url.setObjectName("capstoneRepositoryUrl")
        self._report_path = QLineEdit(self._progress.report_path)
        self._report_path.setObjectName("capstoneReportPath")
        form.addRow(
            capstone_text(locale, CapstoneCopyKey.PROJECT_TITLE),
            self._project_title,
        )
        form.addRow(
            capstone_text(locale, CapstoneCopyKey.GROUP_MEMBERS),
            self._group_members,
        )
        form.addRow(
            capstone_text(locale, CapstoneCopyKey.REPOSITORY_URL),
            self._repository_url,
        )
        form.addRow(
            capstone_text(locale, CapstoneCopyKey.REPORT_PATH),
            self._report_path,
        )
        for field in (
            self._project_title,
            self._group_members,
            self._repository_url,
            self._report_path,
        ):
            field.textChanged.connect(self._schedule_save)
        layout.addWidget(metadata)

        self._progress_bar = QProgressBar()
        self._progress_bar.setObjectName("capstoneProgressBar")
        self._progress_bar.setRange(0, 100)
        self._progress_label = QLabel()
        self._progress_label.setObjectName("capstoneProgressLabel")
        self._readiness = QLabel()
        self._readiness.setObjectName("capstoneReadiness")
        self._readiness.setWordWrap(True)
        layout.addWidget(self._progress_bar)
        layout.addWidget(self._progress_label)
        layout.addWidget(self._readiness)

        for spec in DM857_CAPSTONE_MILESTONES:
            editor = CapstoneMilestoneEditor(
                spec,
                self._progress.milestone(spec.milestone_id),
                locale,
            )
            editor.changed.connect(self._schedule_save)
            self._milestone_editors[spec.milestone_id] = editor
            layout.addWidget(editor)

        rubric_group = QGroupBox(capstone_text(locale, CapstoneCopyKey.RUBRIC_TITLE))
        rubric_group.setObjectName("capstoneRubric")
        rubric_layout = QVBoxLayout(rubric_group)
        rubric_notice = QLabel(capstone_text(locale, CapstoneCopyKey.RUBRIC_NOTICE))
        rubric_notice.setWordWrap(True)
        rubric_layout.addWidget(rubric_notice)

        for criterion in DM857_CAPSTONE_RUBRIC:
            row = QWidget()
            row_layout = QHBoxLayout(row)
            row_layout.setContentsMargins(0, 0, 0, 0)
            label = QLabel(capstone_rubric_text(locale, criterion.criterion_id))
            label.setWordWrap(True)
            score_label = QLabel(
                capstone_text(
                    locale,
                    CapstoneCopyKey.RUBRIC_SCORE,
                    weight=criterion.weight_percent,
                )
            )
            combo = QComboBox()
            combo.setObjectName("capstoneRubricScore")
            combo.setProperty("criterionId", criterion.criterion_id)
            combo.addItem(capstone_text(locale, CapstoneCopyKey.NOT_SCORED), None)
            for score in range(5):
                combo.addItem(str(score), score)
            saved_score = self._progress.rubric_score(criterion.criterion_id)
            combo.setCurrentIndex(0 if saved_score is None else combo.findData(saved_score))
            combo.currentIndexChanged.connect(self._schedule_save)
            self._rubric_scores[criterion.criterion_id] = combo
            row_layout.addWidget(label, 1)
            row_layout.addWidget(score_label)
            row_layout.addWidget(combo)
            rubric_layout.addWidget(row)
        layout.addWidget(rubric_group)

        report_group = QGroupBox(capstone_text(locale, CapstoneCopyKey.REPORT_TITLE))
        report_group.setObjectName("capstoneReportTemplate")
        report_layout = QVBoxLayout(report_group)
        report_notice = QLabel(capstone_text(locale, CapstoneCopyKey.REPORT_NOTICE))
        report_notice.setWordWrap(True)
        report_template = QPlainTextEdit(capstone_text(locale, CapstoneCopyKey.REPORT_TEMPLATE))
        report_template.setObjectName("capstoneReportOutline")
        report_template.setReadOnly(True)
        report_template.setMinimumHeight(220)
        report_layout.addWidget(report_notice)
        report_layout.addWidget(report_template)
        layout.addWidget(report_group)

        self._technical_stations = TechnicalStationPanel(
            progress_store,
            locale,
            parent=self,
        )
        self._technical_stations.set_lab(DM857_PROJECT_ID)
        self._technical_stations.mentor_requested.connect(self.mentor_requested.emit)
        layout.addWidget(self._technical_stations)

        actions = QHBoxLayout()
        self._save_button = QPushButton(capstone_text(locale, CapstoneCopyKey.SAVE))
        self._save_button.setObjectName("capstoneSaveButton")
        self._save_button.clicked.connect(lambda _checked=False: self.persist())
        self._save_status = QLabel()
        self._save_status.setObjectName("capstoneSaveStatus")
        actions.addWidget(self._save_button)
        actions.addWidget(self._save_status, 1)
        layout.addLayout(actions)
        layout.addStretch(1)

        scroll.setWidget(body)
        root.addWidget(scroll)
        self._refresh_summary(self._progress)

    @property
    def progress(self) -> DM857CapstoneProgress:
        """Return the latest persisted or captured capstone state."""

        return self._capture_progress()

    @property
    def technical_station_panel(self) -> TechnicalStationPanel:
        """Return the project-grounded technical reasoning panel."""

        return self._technical_stations

    def milestone_editor(self, milestone_id: str) -> CapstoneMilestoneEditor:
        """Return one editor for deterministic UI tests and integrations."""

        return self._milestone_editors[milestone_id]

    def rubric_combo(self, criterion_id: str) -> QComboBox:
        """Return one internal rubric score selector."""

        return self._rubric_scores[criterion_id]

    def persist(self) -> None:
        """Capture and atomically save all project metadata and evidence."""

        self._save_timer.stop()
        self._progress = self._capture_progress()
        self._technical_stations.persist()
        if self._store is not None:
            self._store.save(self._progress)
        self._save_status.setText(capstone_text(self._locale, CapstoneCopyKey.SAVED))
        self._refresh_summary(self._progress)

    def mentor_context(self) -> str:
        """Ground the Socratic mentor in current project evidence and learner reasoning."""

        progress = self._capture_progress()
        station_context = self._technical_stations.mentor_context()
        return "\n".join(
            (
                "Assessment preparation: DM857 group project and report.",
                f"Project title: {progress.project_title or '[not set]'}",
                f"Group members recorded: {len(progress.group_members)}",
                f"Repository reference: {progress.repository_url or '[not set]'}",
                f"Report reference: {progress.report_path or '[not set]'}",
                f"Ready milestones: {progress.ready_milestone_count}/{len(progress.milestones)}",
                "The detailed project brief and official grading rubric are not available in this "
                "application. Treat all station feedback as formative preparation.",
                station_context,
            )
        )

    def _capture_progress(self) -> DM857CapstoneProgress:
        timestamp = datetime.now(UTC)
        members = tuple(
            part.strip() for part in self._group_members.text().split(",") if part.strip()
        )
        progress = self._progress.with_metadata(
            project_title=self._project_title.text(),
            group_members=members,
            repository_url=self._repository_url.text(),
            report_path=self._report_path.text(),
            now=timestamp,
        )
        for spec in DM857_CAPSTONE_MILESTONES:
            progress = progress.with_milestone(
                self._milestone_editors[spec.milestone_id].progress(),
                now=timestamp,
            )
        for criterion in DM857_CAPSTONE_RUBRIC:
            value = self._rubric_scores[criterion.criterion_id].currentData()
            score = value if isinstance(value, int) else None
            progress = progress.with_rubric_score(
                criterion.criterion_id,
                score,
                now=timestamp,
            )
        return progress

    def _schedule_save(self, *_: object) -> None:
        self._save_status.clear()
        self._save_timer.start()
        self._refresh_summary(self._capture_progress())

    def _refresh_summary(self, progress: DM857CapstoneProgress) -> None:
        for milestone in progress.milestones:
            self._milestone_editors[milestone.milestone_id].refresh_status(milestone.status)
        self._progress_bar.setValue(progress.milestone_completion_percent)
        self._progress_label.setText(
            capstone_text(
                self._locale,
                CapstoneCopyKey.PROGRESS,
                ready=progress.ready_milestone_count,
                total=len(progress.milestones),
                percent=progress.milestone_completion_percent,
            )
        )
        readiness_key = (
            CapstoneCopyKey.READY_SUMMARY
            if progress.preparation_ready
            else CapstoneCopyKey.INCOMPLETE_SUMMARY
        )
        self._readiness.setText(capstone_text(self._locale, readiness_key))
        self._readiness.setProperty(
            "preparationReady",
            progress.preparation_ready,
        )


__all__ = ["CapstoneMilestoneEditor", "DM857CapstonePage"]
