"""Persistent DM847 writing studio with asynchronous grounded Ollama feedback."""

from __future__ import annotations

from collections.abc import Callable
from typing import Protocol

from PySide6.QtCore import QObject, QRunnable, QSettings, QThreadPool, QTimer, Signal, Slot
from PySide6.QtWidgets import (
    QComboBox,
    QGroupBox,
    QHBoxLayout,
    QLabel,
    QPlainTextEdit,
    QPushButton,
    QScrollArea,
    QTextBrowser,
    QVBoxLayout,
    QWidget,
)

from ...content.bundles import ModuleBundle
from ...content.dm847 import BUNDLES, LOCALIZED_BUNDLES
from ...content.models import LearningModule
from ...i18n.locales import DEFAULT_LOCALE, AppLocale
from ...i18n.written_assessment_copy import (
    WrittenAssessmentCopyKey,
    written_assessment_text,
    written_prompt_copy,
)
from ...integrations import (
    DEFAULT_CHAT_MODEL,
    OllamaChatClient,
    OllamaConfig,
    OllamaConnectionError,
    OllamaProtocolError,
)
from ...learning.dm847_written_assessment import (
    DM847_WRITTEN_PROMPTS,
    WrittenAssessmentSnapshot,
    WrittenFeedbackMode,
    WrittenTaskKind,
)
from ...storage.dm847_written_assessment_store import DM847WrittenAssessmentStore
from ...storage.sqlite_progress_store import SQLiteProgressStore
from ...tutoring.written_feedback import (
    WrittenFeedbackRequest,
    WrittenFeedbackResponse,
    WrittenFeedbackService,
)


class WrittenFeedbackRunner(Protocol):
    """Minimal feedback service contract consumed by the writing page."""

    @property
    def model(self) -> str:
        """Return the configured local model name."""

    def generate(
        self,
        module: LearningModule,
        request: WrittenFeedbackRequest,
    ) -> WrittenFeedbackResponse:
        """Return source-bounded feedback for one learner draft."""


FeedbackTask = Callable[[], WrittenFeedbackResponse]
FeedbackSuccessCallback = Callable[[int, WrittenFeedbackResponse], None]
FeedbackFailureCallback = Callable[[int, Exception], None]


class WrittenFeedbackExecutor(Protocol):
    """Execution boundary keeping blocking Ollama calls outside the UI thread."""

    def submit(
        self,
        request_id: int,
        task: FeedbackTask,
        on_success: FeedbackSuccessCallback,
        on_failure: FeedbackFailureCallback,
    ) -> None:
        """Schedule one request and report its eventual outcome."""

    def cancel(self, request_id: int) -> None:
        """Cancel or detach one request without blocking the UI."""


class _FeedbackSignals(QObject):
    succeeded = Signal(int, object)
    failed = Signal(int, object)


class _FeedbackRunnable(QRunnable):
    def __init__(self, request_id: int, task: FeedbackTask) -> None:
        super().__init__()
        self._request_id = request_id
        self._task = task
        self.signals = _FeedbackSignals()
        self.setAutoDelete(True)

    @Slot()
    def run(self) -> None:
        try:
            response = self._task()
        except Exception as exc:  # pragma: no cover - exercised through executor tests
            self.signals.failed.emit(self._request_id, exc)
        else:
            self.signals.succeeded.emit(self._request_id, response)


class QtWrittenFeedbackExecutor:
    """Run blocking local generation in Qt's shared worker pool."""

    def __init__(self, thread_pool: QThreadPool | None = None) -> None:
        self._thread_pool = thread_pool or QThreadPool.globalInstance()

    def submit(
        self,
        request_id: int,
        task: FeedbackTask,
        on_success: FeedbackSuccessCallback,
        on_failure: FeedbackFailureCallback,
    ) -> None:
        runnable = _FeedbackRunnable(request_id, task)
        runnable.signals.succeeded.connect(on_success)
        runnable.signals.failed.connect(on_failure)
        self._thread_pool.start(runnable)

    def cancel(self, request_id: int) -> None:
        """Detach from a running request; stale results are rejected by ID."""

        del request_id


class DM847WrittenAssessmentPage(QWidget):
    """Author, persist and revise DM847 written responses with local-model support."""

    BASE_URL_KEY = "ollama/base_url"
    MODEL_KEY = "ollama/model"
    MINIMUM_FEEDBACK_WORDS = 40

    feedback_ready = Signal(object)

    def __init__(
        self,
        progress_store: SQLiteProgressStore | None,
        locale: AppLocale = DEFAULT_LOCALE,
        *,
        settings: QSettings | None = None,
        written_store: DM847WrittenAssessmentStore | None = None,
        feedback_runner: WrittenFeedbackRunner | None = None,
        executor: WrittenFeedbackExecutor | None = None,
        parent: QWidget | None = None,
    ) -> None:
        super().__init__(parent)
        self.setObjectName("dm847WrittenAssessmentPage")
        self._locale = locale
        self._settings = settings if settings is not None else QSettings()
        self._bundles: tuple[ModuleBundle, ...] = (
            BUNDLES
            if locale == DEFAULT_LOCALE
            else tuple(bundle.materialize(locale) for bundle in LOCALIZED_BUNDLES)
        )
        self._module_by_id = {bundle.module.module_id: bundle.module for bundle in self._bundles}
        self._prompt_by_id = {item.prompt_id: item for item in DM847_WRITTEN_PROMPTS}
        self._store = written_store
        if self._store is None and progress_store is not None:
            self._store = DM847WrittenAssessmentStore.for_progress_store(progress_store)
        loaded = self._store.load() if self._store is not None else None
        self._snapshot = loaded or WrittenAssessmentSnapshot.empty()
        self._runner = feedback_runner or self._default_runner()
        self._executor = executor or QtWrittenFeedbackExecutor()
        self._loading = False
        self._loaded_prompt_id = self._snapshot.active_prompt_id
        self._request_serial = 0
        self._active_request_id: int | None = None
        self._pending_prompt_id = ""

        self._save_timer = QTimer(self)
        self._save_timer.setSingleShot(True)
        self._save_timer.setInterval(350)
        self._save_timer.timeout.connect(self.persist)

        root = QVBoxLayout(self)
        root.setContentsMargins(0, 0, 0, 0)

        scroll = QScrollArea()
        scroll.setObjectName("writtenAssessmentScroll")
        scroll.setWidgetResizable(True)
        body = QWidget()
        body.setObjectName("writtenAssessmentBody")
        layout = QVBoxLayout(body)
        layout.setContentsMargins(4, 4, 12, 24)
        layout.setSpacing(14)

        title = QLabel(written_assessment_text(locale, WrittenAssessmentCopyKey.TITLE))
        title.setObjectName("writtenAssessmentTitle")
        intro = QLabel(written_assessment_text(locale, WrittenAssessmentCopyKey.INTRO))
        intro.setObjectName("writtenAssessmentIntro")
        intro.setWordWrap(True)
        layout.addWidget(title)
        layout.addWidget(intro)

        selector_group = QGroupBox(written_assessment_text(locale, WrittenAssessmentCopyKey.TASK))
        selector_group.setObjectName("writtenTaskSelectorGroup")
        selector_layout = QVBoxLayout(selector_group)
        self._prompt_selector = QComboBox()
        self._prompt_selector.setObjectName("writtenPromptSelector")
        for spec in DM847_WRITTEN_PROMPTS:
            prompt_title, _, _ = written_prompt_copy(locale, spec.prompt_id)
            module = self._module_by_id[spec.module_id]
            self._prompt_selector.addItem(
                f"{module.title} — {prompt_title}",
                spec.prompt_id,
            )
        saved_index = self._prompt_selector.findData(self._snapshot.active_prompt_id)
        self._prompt_selector.setCurrentIndex(max(0, saved_index))
        self._prompt_selector.currentIndexChanged.connect(self._on_prompt_changed)
        selector_layout.addWidget(self._prompt_selector)

        self._module_label = QLabel()
        self._module_label.setObjectName("writtenModuleLabel")
        self._module_label.setWordWrap(True)
        self._kind_label = QLabel()
        self._kind_label.setObjectName("writtenTaskKind")
        self._objectives_label = QLabel()
        self._objectives_label.setObjectName("writtenObjectives")
        self._objectives_label.setWordWrap(True)
        selector_layout.addWidget(self._module_label)
        selector_layout.addWidget(self._kind_label)
        selector_layout.addWidget(self._objectives_label)
        layout.addWidget(selector_group)

        task_group = QGroupBox(written_assessment_text(locale, WrittenAssessmentCopyKey.TASK))
        task_group.setObjectName("writtenTaskGroup")
        task_layout = QVBoxLayout(task_group)
        self._task_text = QLabel()
        self._task_text.setObjectName("writtenTaskText")
        self._task_text.setWordWrap(True)
        self._focus_heading = QLabel(
            written_assessment_text(locale, WrittenAssessmentCopyKey.FOCUS)
        )
        self._focus_heading.setObjectName("contentSubheading")
        self._focus_text = QLabel()
        self._focus_text.setObjectName("writtenFocusPoints")
        self._focus_text.setWordWrap(True)
        task_layout.addWidget(self._task_text)
        task_layout.addWidget(self._focus_heading)
        task_layout.addWidget(self._focus_text)
        layout.addWidget(task_group)

        draft_group = QGroupBox(written_assessment_text(locale, WrittenAssessmentCopyKey.DRAFT))
        draft_group.setObjectName("writtenDraftGroup")
        draft_layout = QVBoxLayout(draft_group)
        self._draft = QPlainTextEdit()
        self._draft.setObjectName("writtenDraftEditor")
        self._draft.setPlaceholderText(
            written_assessment_text(locale, WrittenAssessmentCopyKey.DRAFT_PLACEHOLDER)
        )
        self._draft.setMinimumHeight(260)
        self._draft.textChanged.connect(self._on_draft_changed)
        self._word_count = QLabel()
        self._word_count.setObjectName("writtenWordCount")
        draft_actions = QHBoxLayout()
        self._save_button = QPushButton(
            written_assessment_text(locale, WrittenAssessmentCopyKey.SAVE)
        )
        self._save_button.setObjectName("writtenSaveButton")
        self._save_button.clicked.connect(lambda _checked=False: self.persist())
        self._save_status = QLabel()
        self._save_status.setObjectName("writtenSaveStatus")
        draft_actions.addWidget(self._save_button)
        draft_actions.addWidget(self._word_count)
        draft_actions.addWidget(self._save_status, 1)
        draft_layout.addWidget(self._draft)
        draft_layout.addLayout(draft_actions)
        layout.addWidget(draft_group)

        feedback_group = QGroupBox(
            written_assessment_text(locale, WrittenAssessmentCopyKey.FEEDBACK_TITLE)
        )
        feedback_group.setObjectName("writtenFeedbackGroup")
        feedback_layout = QVBoxLayout(feedback_group)
        notice = QLabel(
            written_assessment_text(locale, WrittenAssessmentCopyKey.FEEDBACK_NOTICE)
        )
        notice.setObjectName("writtenFeedbackNotice")
        notice.setWordWrap(True)
        feedback_layout.addWidget(notice)

        buttons = QHBoxLayout()
        self._review_button = QPushButton(
            written_assessment_text(locale, WrittenAssessmentCopyKey.CONTENT_REVIEW)
        )
        self._review_button.setObjectName("writtenContentReviewButton")
        self._review_button.clicked.connect(
            lambda _checked=False: self.request_feedback(WrittenFeedbackMode.CONTENT_REVIEW)
        )
        self._revision_button = QPushButton(
            written_assessment_text(locale, WrittenAssessmentCopyKey.WRITING_REVISION)
        )
        self._revision_button.setObjectName("writtenRevisionButton")
        self._revision_button.clicked.connect(
            lambda _checked=False: self.request_feedback(WrittenFeedbackMode.WRITING_REVISION)
        )
        self._essay_button = QPushButton(
            written_assessment_text(locale, WrittenAssessmentCopyKey.ESSAY_COACH)
        )
        self._essay_button.setObjectName("writtenEssayButton")
        self._essay_button.clicked.connect(
            lambda _checked=False: self.request_feedback(WrittenFeedbackMode.ESSAY_COACH)
        )
        self._cancel_button = QPushButton(
            written_assessment_text(locale, WrittenAssessmentCopyKey.CANCEL)
        )
        self._cancel_button.setObjectName("writtenCancelButton")
        self._cancel_button.clicked.connect(self.cancel_request)
        self._cancel_button.hide()
        buttons.addWidget(self._review_button)
        buttons.addWidget(self._revision_button)
        buttons.addWidget(self._essay_button)
        buttons.addWidget(self._cancel_button)
        buttons.addStretch(1)
        feedback_layout.addLayout(buttons)

        self._feedback_status = QLabel()
        self._feedback_status.setObjectName("writtenFeedbackStatus")
        self._feedback_status.setWordWrap(True)
        feedback_layout.addWidget(self._feedback_status)

        self._feedback = QTextBrowser()
        self._feedback.setObjectName("writtenFeedbackBrowser")
        self._feedback.setOpenExternalLinks(False)
        self._feedback.setMinimumHeight(240)
        feedback_layout.addWidget(self._feedback)

        sources_heading = QLabel(
            written_assessment_text(locale, WrittenAssessmentCopyKey.SOURCES)
        )
        sources_heading.setObjectName("contentSubheading")
        self._sources = QLabel()
        self._sources.setObjectName("writtenFeedbackSources")
        self._sources.setWordWrap(True)
        self._model_label = QLabel(
            written_assessment_text(
                locale,
                WrittenAssessmentCopyKey.MODEL,
                model=self._runner.model,
            )
        )
        self._model_label.setObjectName("writtenFeedbackModel")
        feedback_layout.addWidget(sources_heading)
        feedback_layout.addWidget(self._sources)
        feedback_layout.addWidget(self._model_label)
        layout.addWidget(feedback_group)
        layout.addStretch(1)

        scroll.setWidget(body)
        root.addWidget(scroll)
        self._load_prompt(self._snapshot.active_prompt_id)

    @property
    def snapshot(self) -> WrittenAssessmentSnapshot:
        """Return the latest captured state, including the visible draft."""

        return self._capture_prompt_draft(self._loaded_prompt_id, clear_feedback=False)

    @property
    def current_prompt_id(self) -> str:
        """Return the stable identity selected in the task control."""

        value = self._prompt_selector.currentData()
        return str(value or DM847_WRITTEN_PROMPTS[0].prompt_id)

    @property
    def draft_editor(self) -> QPlainTextEdit:
        """Expose the learner editor for tests and higher-level integrations."""

        return self._draft

    @property
    def feedback_text(self) -> str:
        """Return the currently rendered model feedback."""

        return self._feedback.toPlainText()

    def select_prompt(self, prompt_id: str) -> bool:
        """Select one written task by stable ID."""

        index = self._prompt_selector.findData(prompt_id)
        if index < 0:
            return False
        if index == self._prompt_selector.currentIndex():
            self._load_prompt(prompt_id)
        else:
            self._prompt_selector.setCurrentIndex(index)
        return True

    def persist(self) -> None:
        """Capture and atomically save learner drafts without grading them."""

        self._save_timer.stop()
        self._snapshot = self._capture_prompt_draft(
            self._loaded_prompt_id,
            clear_feedback=False,
        )
        if self._store is not None:
            self._store.save(self._snapshot)
        self._save_status.setText(
            written_assessment_text(self._locale, WrittenAssessmentCopyKey.SAVED)
        )

    def request_feedback(self, mode: WrittenFeedbackMode) -> None:
        """Request one bounded asynchronous Ollama operation for the current draft."""

        if self._active_request_id is not None:
            return
        draft = self._draft.toPlainText().strip()
        if not draft:
            self._feedback_status.setText(
                written_assessment_text(self._locale, WrittenAssessmentCopyKey.EMPTY_DRAFT)
            )
            return
        if _word_count(draft) < self.MINIMUM_FEEDBACK_WORDS:
            self._feedback_status.setText(
                written_assessment_text(self._locale, WrittenAssessmentCopyKey.TOO_SHORT)
            )
            return

        self.persist()
        prompt_id = self._loaded_prompt_id
        spec = self._prompt_by_id[prompt_id]
        _, task_prompt, focus_points = written_prompt_copy(self._locale, prompt_id)
        module = self._module_by_id[spec.module_id]
        request = WrittenFeedbackRequest(
            prompt_id=prompt_id,
            task_prompt=task_prompt,
            focus_points=focus_points,
            draft=draft,
            mode=mode,
            locale=self._locale,
        )
        self._request_serial += 1
        request_id = self._request_serial
        self._active_request_id = request_id
        self._pending_prompt_id = prompt_id
        self._set_generating(True)
        self._executor.submit(
            request_id,
            lambda: self._runner.generate(module, request),
            self._apply_feedback_success,
            self._apply_feedback_failure,
        )

    @Slot()
    def cancel_request(self) -> None:
        """Detach the current request and ignore any stale eventual result."""

        request_id = self._active_request_id
        if request_id is None:
            return
        self._executor.cancel(request_id)
        self._active_request_id = None
        self._pending_prompt_id = ""
        self._request_serial += 1
        self._set_generating(False)
        self._feedback_status.clear()

    def _default_runner(self) -> WrittenFeedbackService:
        base_url = str(
            self._settings.value(
                self.BASE_URL_KEY,
                OllamaConfig().normalized_base_url(),
            )
        )
        model = str(self._settings.value(self.MODEL_KEY, DEFAULT_CHAT_MODEL)).strip()
        if not model:
            model = DEFAULT_CHAT_MODEL
        client = OllamaChatClient(OllamaConfig(base_url=base_url))
        return WrittenFeedbackService(client, model=model)

    def _on_prompt_changed(self, _index: int) -> None:
        if self._loading:
            return
        if self._active_request_id is not None:
            self.cancel_request()
        self._snapshot = self._capture_prompt_draft(
            self._loaded_prompt_id,
            clear_feedback=False,
        )
        target_prompt_id = self.current_prompt_id
        self._snapshot = self._snapshot.with_active_prompt(target_prompt_id)
        self._load_prompt(target_prompt_id)
        self._schedule_save()

    def _load_prompt(self, prompt_id: str) -> None:
        self._loading = True
        try:
            self._snapshot = self._snapshot.with_active_prompt(prompt_id)
            spec = self._prompt_by_id[prompt_id]
            module = self._module_by_id[spec.module_id]
            _, task, focus_points = written_prompt_copy(self._locale, prompt_id)
            kind_key = (
                WrittenAssessmentCopyKey.ESSAY
                if spec.kind is WrittenTaskKind.ESSAY
                else WrittenAssessmentCopyKey.OPEN_RESPONSE
            )
            self._module_label.setText(
                f"{written_assessment_text(self._locale, WrittenAssessmentCopyKey.MODULE)}: "
                f"{module.title}"
            )
            self._kind_label.setText(
                f"{written_assessment_text(self._locale, WrittenAssessmentCopyKey.TASK_KIND)}: "
                f"{written_assessment_text(self._locale, kind_key)}"
            )
            objective_text = ", ".join(
                objective.statement
                for objective in module.objectives
                if objective.objective_id in spec.objective_ids
            )
            self._objectives_label.setText(
                written_assessment_text(
                    self._locale,
                    WrittenAssessmentCopyKey.OBJECTIVES,
                    objectives=objective_text,
                )
            )
            self._task_text.setText(task)
            self._focus_text.setText("\n".join(f"• {item}" for item in focus_points))
            draft = self._snapshot.draft(prompt_id)
            self._draft.setPlainText(draft.response_text)
            self._render_feedback(draft.feedback_text, draft.source_ids)
            self._feedback_status.setText(
                ""
                if draft.feedback_text
                else written_assessment_text(
                    self._locale,
                    WrittenAssessmentCopyKey.NO_FEEDBACK,
                )
            )
            self._loaded_prompt_id = prompt_id
            self._update_word_count()
        finally:
            self._loading = False

    def _on_draft_changed(self) -> None:
        if self._loading:
            return
        had_feedback = bool(self._snapshot.draft(self._loaded_prompt_id).feedback_text)
        self._snapshot = self._capture_prompt_draft(
            self._loaded_prompt_id,
            clear_feedback=True,
        )
        self._render_feedback("", ())
        self._feedback_status.setText(
            written_assessment_text(
                self._locale,
                (
                    WrittenAssessmentCopyKey.FEEDBACK_STALE
                    if had_feedback
                    else WrittenAssessmentCopyKey.NO_FEEDBACK
                ),
            )
        )
        self._save_status.clear()
        self._update_word_count()
        self._schedule_save()

    def _capture_prompt_draft(
        self,
        prompt_id: str,
        *,
        clear_feedback: bool,
    ) -> WrittenAssessmentSnapshot:
        return self._snapshot.with_response(
            prompt_id,
            self._draft.toPlainText(),
            clear_feedback=clear_feedback,
        ).with_active_prompt(self.current_prompt_id)

    def _schedule_save(self) -> None:
        self._save_timer.start()

    def _update_word_count(self) -> None:
        self._word_count.setText(
            written_assessment_text(
                self._locale,
                WrittenAssessmentCopyKey.WORD_COUNT,
                words=_word_count(self._draft.toPlainText()),
            )
        )

    def _set_generating(self, generating: bool) -> None:
        for button in (self._review_button, self._revision_button, self._essay_button):
            button.setEnabled(not generating)
        self._cancel_button.setVisible(generating)
        if generating:
            self._feedback_status.setText(
                written_assessment_text(
                    self._locale,
                    WrittenAssessmentCopyKey.GENERATING,
                )
            )

    @Slot(int, object)
    def _apply_feedback_success(self, request_id: int, response_object: object) -> None:
        if request_id != self._active_request_id:
            return
        if not isinstance(response_object, WrittenFeedbackResponse):
            self._apply_feedback_failure(
                request_id,
                TypeError("Ollama returned an unexpected written-feedback object."),
            )
            return

        self._active_request_id = None
        self._set_generating(False)
        prompt_id = self._pending_prompt_id
        self._pending_prompt_id = ""
        self._snapshot = self._snapshot.with_feedback(
            prompt_id,
            feedback_text=response_object.content,
            feedback_mode=response_object.mode,
            source_ids=response_object.source_ids,
        )
        if prompt_id == self._loaded_prompt_id:
            self._render_feedback(response_object.content, response_object.source_ids)
            self._feedback_status.clear()
            self._model_label.setText(
                written_assessment_text(
                    self._locale,
                    WrittenAssessmentCopyKey.MODEL,
                    model=response_object.model,
                )
            )
        if self._store is not None:
            self._store.save(self._snapshot)
        self.feedback_ready.emit(response_object)

    @Slot(int, object)
    def _apply_feedback_failure(self, request_id: int, error_object: object) -> None:
        if request_id != self._active_request_id:
            return
        self._active_request_id = None
        self._pending_prompt_id = ""
        self._set_generating(False)
        error = (
            error_object
            if isinstance(error_object, Exception)
            else RuntimeError(str(error_object))
        )
        message = str(error) or error.__class__.__name__
        if not isinstance(error, (OllamaConnectionError, OllamaProtocolError, ValueError)):
            message = str(error) or error.__class__.__name__
        self._feedback_status.setText(
            written_assessment_text(
                self._locale,
                WrittenAssessmentCopyKey.REQUEST_FAILED,
                message=message,
            )
        )

    def _render_feedback(self, feedback: str, source_ids: tuple[str, ...]) -> None:
        self._feedback.setPlainText(feedback)
        self._sources.setText(" · ".join(f"[{item}]" for item in source_ids) or "—")


def _word_count(text: str) -> int:
    return len(text.split())


__all__ = [
    "DM847WrittenAssessmentPage",
    "QtWrittenFeedbackExecutor",
    "WrittenFeedbackExecutor",
    "WrittenFeedbackRunner",
]
