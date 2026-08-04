"""Persistent vertical laboratory workflow with deterministic Python checkpoints."""

from __future__ import annotations

from pathlib import Path

from PySide6.QtCore import QSignalBlocker, QTimer, Signal, Slot
from PySide6.QtWidgets import (
    QComboBox,
    QFileDialog,
    QFrame,
    QGridLayout,
    QHBoxLayout,
    QLabel,
    QPlainTextEdit,
    QProgressBar,
    QPushButton,
    QScrollArea,
    QVBoxLayout,
    QWidget,
)

from ...content.labs import LABS
from ...i18n.computational_lab_copy import (
    ComputationalLabCopyKey,
    computational_lab_text,
    lab_stage_text,
)
from ...i18n.locales import DEFAULT_LOCALE, AppLocale
from ...learning.computational_labs import (
    ComputationalLab,
    LabAttempt,
    LabNotebookSnapshot,
    LabTask,
    LabTaskKind,
    render_lab_record,
)
from ...learning.python_execution import (
    ExecutionStatus,
    PythonCodeRunner,
    PythonExecutionRequest,
    PythonSubprocessRunner,
)
from ...storage.computational_lab_store import ComputationalLabStore
from ...storage.sqlite_progress_store import SQLiteProgressStore


class ComputationalLabsPage(QWidget):
    """Guide one complete computational investigation and persist learner evidence."""

    mentor_requested = Signal()

    def __init__(
        self,
        progress_store: SQLiteProgressStore | None,
        locale: AppLocale = DEFAULT_LOCALE,
        *,
        labs: tuple[ComputationalLab, ...] = LABS,
        runner: PythonCodeRunner | None = None,
        parent: QWidget | None = None,
    ) -> None:
        super().__init__(parent)
        if not labs:
            raise ValueError("The laboratory page requires at least one authored lab.")

        self.setObjectName("computationalLabsPage")
        self._locale = locale
        self._labs = labs
        self._runner: PythonCodeRunner = runner or PythonSubprocessRunner()
        self._store = (
            ComputationalLabStore.for_progress_store(progress_store)
            if progress_store is not None
            else None
        )
        loaded_snapshot = self._store.load() if self._store is not None else None
        self._snapshot: LabNotebookSnapshot = (
            loaded_snapshot if loaded_snapshot is not None else LabNotebookSnapshot()
        )
        self._lab = self._labs[0]
        self._attempt = self._validated_attempt(self._snapshot.attempt_for(self._lab))
        self._task_index = self._task_index_for(self._attempt.current_task_id)
        self._loading_task = False

        self._autosave = QTimer(self)
        self._autosave.setSingleShot(True)
        self._autosave.setInterval(600)
        self._autosave.timeout.connect(self.persist)

        root = QVBoxLayout(self)
        root.setContentsMargins(0, 0, 0, 0)
        scroll = QScrollArea()
        scroll.setObjectName("computationalLabsScroll")
        scroll.setWidgetResizable(True)
        body = QWidget()
        self._body_layout = QVBoxLayout(body)
        self._body_layout.setContentsMargins(4, 4, 16, 24)
        self._body_layout.setSpacing(14)

        self._build_lab_selector()
        self._build_overview()
        self._build_progress()
        self._build_task_card()
        self._body_layout.addStretch(1)

        scroll.setWidget(body)
        root.addWidget(scroll)
        self._render_lab()

    @property
    def current_lab(self) -> ComputationalLab:
        """Return the selected authored laboratory."""

        return self._lab

    @property
    def current_task(self) -> LabTask:
        """Return the visible authored task."""

        return self._lab.tasks[self._task_index]

    @property
    def attempt(self) -> LabAttempt:
        """Return the current learner-owned attempt."""

        return self._attempt

    def persist(self) -> None:
        """Persist visible work and deterministic evidence atomically."""

        self._capture_response()
        self._snapshot = self._snapshot.with_attempt(self._attempt)
        if self._store is not None:
            self._store.save(self._snapshot)

    def mentor_context(self) -> str:
        """Return bounded Socratic context for the current laboratory task."""

        self._capture_response()
        task = self.current_task
        response = self._attempt.response_for(task.task_id).strip()
        output = self._attempt.execution_outputs.get(task.task_id, "").strip()
        objectives = "\n".join(
            f"- {self._lab.objective_text(objective_id, self._locale)}"
            for objective_id in task.objective_ids
        )
        return "\n".join(
            (
                f"Course: {self._lab.course_code}",
                f"Internal preparation laboratory: {self._lab.title.text(self._locale)}",
                f"Research question: {self._lab.research_question.text(self._locale)}",
                f"Stage: {lab_stage_text(self._locale, task.stage)}",
                f"Task: {task.title.text(self._locale)}",
                f"Task instructions: {task.instructions.text(self._locale)}",
                "Linked objectives:",
                objectives,
                f"Learner response or code:\n{response or '[blank]'}",
                f"Latest checkpoint output:\n{output or '[none]'}",
                f"Checkpoint passed: {task.task_id in self._attempt.passed_checkpoints}",
                f"Requested hint level: {self._attempt.hint_level_for(task.task_id)}/6",
                f"Authored mentor notes: {task.mentor_notes.text(self._locale)}",
                "Mentor policy: use the Socratic method, ask for reasoning first, provide one "
                "progressive hint at a time, never reveal hidden verification code, and do not "
                "treat model feedback as mastery.",
            )
        )

    def _build_lab_selector(self) -> None:
        row = QHBoxLayout()
        label = QLabel(self._text(ComputationalLabCopyKey.LAB))
        label.setObjectName("fieldLabel")
        self._lab_selector = QComboBox()
        self._lab_selector.setObjectName("computationalLabSelector")
        for lab in self._labs:
            self._lab_selector.addItem(
                f"{lab.course_code} · {lab.title.text(self._locale)}",
                userData=lab.lab_id,
            )
        self._lab_selector.currentIndexChanged.connect(self._select_lab)
        row.addWidget(label)
        row.addWidget(self._lab_selector, 1)
        self._body_layout.addLayout(row)

    def _build_overview(self) -> None:
        self._disclaimer = QLabel()
        self._disclaimer.setObjectName("statusBanner")
        self._disclaimer.setWordWrap(True)
        self._body_layout.addWidget(self._disclaimer)

        card = QFrame()
        card.setProperty("cardRole", "surface")
        layout = QGridLayout(card)
        layout.setContentsMargins(16, 16, 16, 16)
        layout.setHorizontalSpacing(18)
        layout.setVerticalSpacing(8)

        self._question_heading, self._question = self._overview_pair()
        self._provenance_heading, self._provenance = self._overview_pair()
        self._objectives_heading, self._objectives = self._overview_pair()
        self._prerequisites_heading, self._prerequisites = self._overview_pair()
        layout.addWidget(self._question_heading, 0, 0)
        layout.addWidget(self._question, 1, 0)
        layout.addWidget(self._provenance_heading, 0, 1)
        layout.addWidget(self._provenance, 1, 1)
        layout.addWidget(self._objectives_heading, 2, 0)
        layout.addWidget(self._objectives, 3, 0)
        layout.addWidget(self._prerequisites_heading, 2, 1)
        layout.addWidget(self._prerequisites, 3, 1)
        self._body_layout.addWidget(card)

    @staticmethod
    def _overview_pair() -> tuple[QLabel, QLabel]:
        heading = QLabel()
        heading.setObjectName("sectionHeading")
        value = QLabel()
        value.setWordWrap(True)
        return heading, value

    def _build_progress(self) -> None:
        row = QHBoxLayout()
        self._progress_label = QLabel()
        self._progress = QProgressBar()
        self._progress.setRange(0, 100)
        self._progress.setTextVisible(False)
        row.addWidget(self._progress_label)
        row.addWidget(self._progress, 1)
        self._body_layout.addLayout(row)

    def _build_task_card(self) -> None:
        card = QFrame()
        card.setProperty("cardRole", "surface")
        layout = QVBoxLayout(card)
        layout.setContentsMargins(16, 16, 16, 16)
        layout.setSpacing(10)

        selector_row = QHBoxLayout()
        self._task_position = QLabel()
        self._task_selector = QComboBox()
        self._task_selector.setObjectName("computationalLabTaskSelector")
        self._task_selector.currentIndexChanged.connect(self._select_task)
        selector_row.addWidget(self._task_position)
        selector_row.addWidget(self._task_selector, 1)
        layout.addLayout(selector_row)

        self._stage = QLabel()
        self._stage.setObjectName("courseCardCode")
        self._task_title = QLabel()
        self._task_title.setObjectName("sectionHeading")
        self._instructions = QLabel()
        self._instructions.setWordWrap(True)
        self._hint_level = QLabel()
        self._hint_level.setProperty("semanticTone", "subtle")
        for widget in (
            self._stage,
            self._task_title,
            self._instructions,
            self._hint_level,
        ):
            layout.addWidget(widget)

        self._response = QPlainTextEdit()
        self._response.setObjectName("computationalLabResponse")
        self._response.setMinimumHeight(220)
        self._response.textChanged.connect(self._response_changed)
        layout.addWidget(self._response)

        self._output_heading = QLabel()
        self._output_heading.setObjectName("fieldLabel")
        self._output = QPlainTextEdit()
        self._output.setObjectName("computationalLabOutput")
        self._output.setReadOnly(True)
        self._output.setMaximumHeight(150)
        layout.addWidget(self._output_heading)
        layout.addWidget(self._output)

        actions = QHBoxLayout()
        self._previous = self._action_button(self._previous_task)
        self._next = self._action_button(self._next_task)
        self._verify = self._action_button(self._verify_or_complete)
        self._mentor = self._action_button(self._request_mentor)
        self._save = self._action_button(self._save_clicked)
        self._export = self._action_button(self._export_record)
        self._verify.setProperty("buttonRole", "primary")
        for button in (
            self._previous,
            self._next,
            self._verify,
            self._mentor,
            self._save,
            self._export,
        ):
            actions.addWidget(button)
        layout.addLayout(actions)

        self._status = QLabel()
        self._status.setWordWrap(True)
        self._status.setProperty("semanticTone", "muted")
        layout.addWidget(self._status)
        self._body_layout.addWidget(card)

    @staticmethod
    def _action_button(callback: object) -> QPushButton:
        button = QPushButton()
        button.clicked.connect(callback)
        return button

    def _render_lab(self) -> None:
        blocker = QSignalBlocker(self._task_selector)
        self._task_selector.clear()
        for task in self._lab.tasks:
            self._task_selector.addItem(
                f"{lab_stage_text(self._locale, task.stage)} · {task.title.text(self._locale)}",
                userData=task.task_id,
            )
        self._task_selector.setCurrentIndex(self._task_index)
        del blocker

        self._disclaimer.setText(self._lab.disclaimer.text(self._locale))
        self._question_heading.setText(self._text(ComputationalLabCopyKey.RESEARCH_QUESTION))
        self._question.setText(self._lab.research_question.text(self._locale))
        self._provenance_heading.setText(self._text(ComputationalLabCopyKey.DATA_PROVENANCE))
        self._provenance.setText(self._lab.data_provenance.text(self._locale))
        self._objectives_heading.setText(self._text(ComputationalLabCopyKey.OBJECTIVES))
        self._objectives.setText(
            "\n".join(f"• {text.text(self._locale)}" for _, text in self._lab.objectives)
        )
        self._prerequisites_heading.setText(self._text(ComputationalLabCopyKey.PREREQUISITES))
        self._prerequisites.setText(
            "\n".join(f"• {item.text(self._locale)}" for item in self._lab.prerequisites)
        )
        self._previous.setText(self._text(ComputationalLabCopyKey.PREVIOUS))
        self._next.setText(self._text(ComputationalLabCopyKey.NEXT))
        self._mentor.setText(self._text(ComputationalLabCopyKey.MENTOR))
        self._save.setText(self._text(ComputationalLabCopyKey.SAVE))
        self._export.setText(self._text(ComputationalLabCopyKey.EXPORT))
        self._output_heading.setText(self._text(ComputationalLabCopyKey.OUTPUT))
        self._load_task()

    def _load_task(self) -> None:
        self._loading_task = True
        task = self.current_task
        self._attempt = self._attempt.with_current_task(task.task_id)
        response = self._attempt.response_for(task.task_id)
        if not response and task.seed_from_task_id is not None:
            response = self._attempt.response_for(task.seed_from_task_id)
        if not response:
            response = task.starter_response

        blocker = QSignalBlocker(self._response)
        self._response.setPlainText(response)
        del blocker
        self._stage.setText(lab_stage_text(self._locale, task.stage))
        self._task_title.setText(task.title.text(self._locale))
        self._instructions.setText(task.instructions.text(self._locale))
        self._hint_level.setText(
            self._text(
                ComputationalLabCopyKey.HINT_LEVEL,
                level=self._attempt.hint_level_for(task.task_id),
            )
        )
        self._task_position.setText(
            self._text(
                ComputationalLabCopyKey.TASK,
                current=self._task_index + 1,
                total=len(self._lab.tasks),
            )
        )
        verify_key = (
            ComputationalLabCopyKey.VERIFY
            if task.kind is LabTaskKind.PYTHON
            else ComputationalLabCopyKey.COMPLETE
        )
        self._verify.setText(self._text(verify_key))
        self._output.setPlainText(self._attempt.execution_outputs.get(task.task_id, ""))
        self._previous.setEnabled(self._task_index > 0)
        self._next.setEnabled(self._task_index < len(self._lab.tasks) - 1)
        self._update_progress()
        self._status.clear()
        self._loading_task = False

    def _capture_response(self) -> None:
        if self._loading_task:
            return
        task = self.current_task
        response = self._response.toPlainText()
        if response != self._attempt.response_for(task.task_id):
            self._attempt = self._attempt.with_response(task.task_id, response)

    @Slot()
    def _response_changed(self) -> None:
        self._capture_response()
        self._autosave.start()
        self._update_progress()

    @Slot(int)
    def _select_lab(self, index: int) -> None:
        if index < 0 or index >= len(self._labs):
            return
        self.persist()
        self._lab = self._labs[index]
        self._attempt = self._validated_attempt(self._snapshot.attempt_for(self._lab))
        self._task_index = self._task_index_for(self._attempt.current_task_id)
        self._render_lab()

    @Slot(int)
    def _select_task(self, index: int) -> None:
        if self._loading_task or index < 0 or index >= len(self._lab.tasks):
            return
        self._capture_response()
        self._task_index = index
        self._load_task()
        self._autosave.start()

    @Slot()
    def _previous_task(self) -> None:
        self._task_selector.setCurrentIndex(max(0, self._task_index - 1))

    @Slot()
    def _next_task(self) -> None:
        self._task_selector.setCurrentIndex(min(len(self._lab.tasks) - 1, self._task_index + 1))

    @Slot()
    def _verify_or_complete(self) -> None:
        self._capture_response()
        task = self.current_task
        response = self._attempt.response_for(task.task_id)
        if task.kind is LabTaskKind.SHORT_ANSWER:
            self._complete_short_answer(task, response)
            return
        self._run_python_checkpoint(task, response)

    def _complete_short_answer(self, task: LabTask, response: str) -> None:
        if len(response.strip()) < 40:
            self._status.setText(self._text(ComputationalLabCopyKey.ANSWER_REQUIRED))
            return
        self._attempt = self._attempt.mark_complete(task.task_id)
        self._status.setText(self._text(ComputationalLabCopyKey.CHECKPOINT_PASSED))
        self.persist()
        self._update_progress()

    def _run_python_checkpoint(self, task: LabTask, response: str) -> None:
        source = f"{response.rstrip()}\n\n{task.verification_source.strip()}\n"
        result = self._runner.run(
            PythonExecutionRequest(
                source=source,
                expected_output=task.expected_output,
                timeout_seconds=4.0,
            )
        )
        output_parts = [
            f"status: {result.status.value}",
            f"duration_ms: {result.duration_ms}",
        ]
        if result.stdout:
            output_parts.extend(("stdout:", result.stdout.rstrip()))
        if result.stderr:
            output_parts.extend(("stderr:", result.stderr.rstrip()))
        rendered = "\n".join(output_parts)
        self._output.setPlainText(rendered)

        if result.status is ExecutionStatus.PASSED:
            self._attempt = self._attempt.mark_complete(
                task.task_id,
                checkpoint_passed=True,
                output=rendered,
            )
            message_key = ComputationalLabCopyKey.CHECKPOINT_PASSED
        else:
            failed_attempt = self._attempt.mark_complete(
                task.task_id,
                checkpoint_passed=False,
                output=rendered,
            )
            self._attempt = failed_attempt.with_response(task.task_id, response)
            message_key = ComputationalLabCopyKey.CHECKPOINT_FAILED
        self._status.setText(self._text(message_key))
        self.persist()
        self._update_progress()

    @Slot()
    def _request_mentor(self) -> None:
        self._capture_response()
        task_id = self.current_task.task_id
        self._attempt = self._attempt.with_requested_hint(task_id)
        self.persist()
        self._hint_level.setText(
            self._text(
                ComputationalLabCopyKey.HINT_LEVEL,
                level=self._attempt.hint_level_for(task_id),
            )
        )
        self.mentor_requested.emit()

    @Slot()
    def _save_clicked(self) -> None:
        self.persist()
        self._status.setText(self._text(ComputationalLabCopyKey.SAVED))

    @Slot()
    def _export_record(self) -> None:
        self.persist()
        suggested = f"{self._lab.lab_id.replace('.', '_')}.md"
        path_text, _ = QFileDialog.getSaveFileName(
            self,
            self._text(ComputationalLabCopyKey.EXPORT_DIALOG),
            suggested,
            self._text(ComputationalLabCopyKey.MARKDOWN_FILTER),
        )
        if not path_text:
            return
        path = Path(path_text)
        if path.suffix.casefold() != ".md":
            path = path.with_suffix(".md")
        path.write_text(
            render_lab_record(self._lab, self._attempt, self._locale),
            encoding="utf-8",
        )
        self._status.setText(self._text(ComputationalLabCopyKey.EXPORTED, path=str(path)))

    def _validated_attempt(self, attempt: LabAttempt) -> LabAttempt:
        known_tasks = {task.task_id for task in self._lab.tasks}
        return attempt if attempt.current_task_id in known_tasks else LabAttempt.new(self._lab)

    def _update_progress(self) -> None:
        percent = round(100 * self._attempt.completion_ratio(self._lab))
        self._progress.setValue(percent)
        self._progress_label.setText(self._text(ComputationalLabCopyKey.PROGRESS, percent=percent))

    def _task_index_for(self, task_id: str) -> int:
        return next(
            (index for index, task in enumerate(self._lab.tasks) if task.task_id == task_id),
            0,
        )

    def _text(self, key: ComputationalLabCopyKey, **values: object) -> str:
        return computational_lab_text(self._locale, key, **values)


__all__ = ["ComputationalLabsPage"]
