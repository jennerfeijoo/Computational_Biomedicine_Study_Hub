"""Application-wide persistent Socratic Ollama mentor."""

from __future__ import annotations

from collections.abc import Callable
from datetime import UTC, datetime
from typing import Protocol
from uuid import uuid4

from PySide6.QtCore import (
    QEvent,
    QObject,
    QPoint,
    QRunnable,
    QSettings,
    Qt,
    QThreadPool,
    Signal,
    Slot,
)
from PySide6.QtGui import QContextMenuEvent, QMouseEvent, QTextOption
from PySide6.QtWidgets import (
    QComboBox,
    QFrame,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QMenu,
    QPlainTextEdit,
    QPushButton,
    QTextBrowser,
    QTextEdit,
    QVBoxLayout,
    QWidget,
)

from ...i18n.locales import DEFAULT_LOCALE, AppLocale
from ...i18n.tutor_chat_copy import TutorChatCopyKey, tutor_chat_text
from ...integrations import (
    DEFAULT_CHAT_MODEL,
    ChatMessage,
    ChatRole,
    OllamaChatClient,
    OllamaConfig,
)
from ...learning.mentor import (
    MENTOR_RESPONSE_SCHEMA,
    MentorJournalSnapshot,
    MentorMode,
    MentorObservation,
    MentorTurnRecord,
    MentorTurnResult,
    mentor_system_prompt,
    parse_mentor_turn,
)
from ...storage.mentor_journal_store import MentorJournalStore

ContextProvider = Callable[[], str]
TutorSuccessCallback = Callable[[int, MentorTurnResult], None]
TutorFailureCallback = Callable[[int, Exception], None]
TutorTask = Callable[[], MentorTurnResult]

_MODE_COPY: dict[MentorMode, TutorChatCopyKey] = {
    MentorMode.SOCRATIC: TutorChatCopyKey.MODE_SOCRATIC,
    MentorMode.EXPLAIN: TutorChatCopyKey.MODE_EXPLAIN,
    MentorMode.PRACTICE: TutorChatCopyKey.MODE_PRACTICE,
    MentorMode.EVALUATE: TutorChatCopyKey.MODE_EVALUATE,
    MentorMode.PLAN: TutorChatCopyKey.MODE_PLAN,
    MentorMode.REFLECT: TutorChatCopyKey.MODE_REFLECT,
}


class TutorChatRunner(Protocol):
    """Generate one context-aware structured mentor response."""

    def ask(
        self,
        context: str,
        history: tuple[ChatMessage, ...],
        question: str,
        *,
        locale: AppLocale,
        mode: MentorMode,
        memory: str,
    ) -> MentorTurnResult:
        """Return one visible mentor reply plus provisional longitudinal metadata."""


class TutorChatExecutor(Protocol):
    """Run blocking local generation away from the GUI thread."""

    def submit(
        self,
        request_id: int,
        task: TutorTask,
        on_success: TutorSuccessCallback,
        on_failure: TutorFailureCallback,
    ) -> None:
        """Schedule one request."""

    def cancel(self, request_id: int) -> None:
        """Detach one request without blocking the interface."""


class OllamaTutorChatRunner:
    """Use the configured local model as a structured longitudinal mentor."""

    BASE_URL_KEY = "ollama/base_url"
    MODEL_KEY = "ollama/model"
    NUM_CTX_KEY = "ollama/mentor_num_ctx"
    NUM_PREDICT_KEY = "ollama/mentor_num_predict"
    DEFAULT_NUM_CTX = 16_384
    DEFAULT_NUM_PREDICT = 1_400

    def __init__(self, settings: QSettings) -> None:
        self._settings = settings

    def ask(
        self,
        context: str,
        history: tuple[ChatMessage, ...],
        question: str,
        *,
        locale: AppLocale,
        mode: MentorMode,
        memory: str,
    ) -> MentorTurnResult:
        base_url = str(
            self._settings.value(
                self.BASE_URL_KEY,
                OllamaConfig().normalized_base_url(),
            )
        ).strip()
        model = str(self._settings.value(self.MODEL_KEY, DEFAULT_CHAT_MODEL)).strip()
        client = OllamaChatClient(config=OllamaConfig(base_url=base_url))
        language = {
            AppLocale.SPANISH_SPAIN: "Spanish",
            AppLocale.ENGLISH: "English",
            AppLocale.DANISH_DENMARK: "Danish",
        }[locale]
        messages = (
            ChatMessage(
                ChatRole.SYSTEM,
                mentor_system_prompt(
                    context=context,
                    memory=memory,
                    locale_name=language,
                    mode=mode,
                ),
            ),
            *history,
            ChatMessage(ChatRole.USER, question),
        )
        response = client.chat(
            messages,
            model=model or DEFAULT_CHAT_MODEL,
            temperature=self._temperature(mode),
            think=True,
            format_schema=MENTOR_RESPONSE_SCHEMA,
            num_ctx=self._positive_setting(self.NUM_CTX_KEY, self.DEFAULT_NUM_CTX),
            num_predict=self._positive_setting(
                self.NUM_PREDICT_KEY,
                self.DEFAULT_NUM_PREDICT,
            ),
            keep_alive="30m",
        )
        return parse_mentor_turn(response)

    def _positive_setting(self, key: str, default: int) -> int:
        raw = self._settings.value(key, default)
        try:
            value = int(raw)
        except (TypeError, ValueError):
            return default
        return value if value > 0 else default

    @staticmethod
    def _temperature(mode: MentorMode) -> float:
        return {
            MentorMode.SOCRATIC: 0.25,
            MentorMode.EXPLAIN: 0.2,
            MentorMode.PRACTICE: 0.3,
            MentorMode.EVALUATE: 0.1,
            MentorMode.PLAN: 0.2,
            MentorMode.REFLECT: 0.25,
        }[mode]


class _TutorTaskSignals(QObject):
    succeeded = Signal(int, object)
    failed = Signal(int, object)


class _TutorTaskRunnable(QRunnable):
    def __init__(self, request_id: int, task: TutorTask) -> None:
        super().__init__()
        self._request_id = request_id
        self._task = task
        self.signals = _TutorTaskSignals()
        self.setAutoDelete(True)

    @Slot()
    def run(self) -> None:
        try:
            response = self._task()
        except Exception as exc:  # pragma: no cover - worker boundary
            self.signals.failed.emit(self._request_id, exc)
        else:
            self.signals.succeeded.emit(self._request_id, response)


class QtTutorChatExecutor:
    """Use Qt's shared thread pool for local Ollama generation."""

    def __init__(self, thread_pool: QThreadPool | None = None) -> None:
        self._thread_pool = thread_pool or QThreadPool.globalInstance()

    def submit(
        self,
        request_id: int,
        task: TutorTask,
        on_success: TutorSuccessCallback,
        on_failure: TutorFailureCallback,
    ) -> None:
        runnable = _TutorTaskRunnable(request_id, task)
        runnable.signals.succeeded.connect(on_success)
        runnable.signals.failed.connect(on_failure)
        self._thread_pool.start(runnable)

    def cancel(self, request_id: int) -> None:
        del request_id


class FloatingTutorChat(QFrame):
    """Maintain one movable persistent mentor conversation across application pages."""

    MODE_KEY = "mentor/mode"
    visibility_changed = Signal(bool)

    def __init__(
        self,
        *,
        settings: QSettings,
        context_provider: ContextProvider,
        locale: AppLocale = DEFAULT_LOCALE,
        runner: TutorChatRunner | None = None,
        executor: TutorChatExecutor | None = None,
        journal_store: MentorJournalStore | None = None,
        parent: QWidget | None = None,
    ) -> None:
        super().__init__(parent)
        self.setObjectName("floatingTutorChat")
        self.setProperty("cardRole", "surface")
        self.setFrameShape(QFrame.Shape.StyledPanel)
        self.setFixedWidth(460)
        self.setMinimumHeight(190)
        self.setMaximumHeight(680)

        self._settings = settings
        self._locale = locale
        self._context_provider = context_provider
        self._runner = runner or OllamaTutorChatRunner(settings)
        self._executor = executor or QtTutorChatExecutor()
        self._journal_store = journal_store
        self._journal = (
            journal_store.load_or_empty() if journal_store is not None else MentorJournalSnapshot.empty()
        )
        self._session_id = self._journal.latest_session_id or uuid4().hex
        self._history: list[ChatMessage] = list(self._journal.chat_history(limit=6))
        self._last_observation = (
            self._journal.turns[-1].observation if self._journal.turns else MentorObservation.empty()
        )
        self._request_serial = 0
        self._active_request_id: int | None = None
        self._pending_user_message: ChatMessage | None = None
        self._pending_context = ""
        self._pending_mode = MentorMode.SOCRATIC
        self._minimized = False
        self._drag_offset: QPoint | None = None
        self._custom_position = False

        root = QVBoxLayout(self)
        root.setContentsMargins(14, 12, 14, 12)
        root.setSpacing(8)

        self._header = QFrame()
        self._header.setObjectName("floatingTutorDragHandle")
        self._header.setCursor(Qt.CursorShape.OpenHandCursor)
        self._header.installEventFilter(self)
        header = QHBoxLayout(self._header)
        header.setContentsMargins(0, 0, 0, 0)
        header.setSpacing(8)

        self._title = QLabel()
        self._title.setObjectName("floatingTutorTitle")
        self._title.setAttribute(Qt.WidgetAttribute.WA_TransparentForMouseEvents, True)
        header.addWidget(self._title, 1)

        self._minimize_button = self._header_button()
        self._minimize_button.clicked.connect(self.toggle_minimized)
        header.addWidget(self._minimize_button)

        self._reset_button = self._header_button()
        self._reset_button.clicked.connect(self.reset_conversation)
        header.addWidget(self._reset_button)

        self._close_button = self._header_button()
        self._close_button.clicked.connect(self.close_panel)
        header.addWidget(self._close_button)
        root.addWidget(self._header)

        self._body = QWidget()
        body_layout = QVBoxLayout(self._body)
        body_layout.setContentsMargins(0, 0, 0, 0)
        body_layout.setSpacing(8)

        self._context = QLabel()
        self._context.setObjectName("floatingTutorContext")
        self._context.setProperty("semanticTone", "muted")
        self._context.setWordWrap(True)
        body_layout.addWidget(self._context)

        mode_row = QHBoxLayout()
        self._mode_label = QLabel()
        self._mode_label.setProperty("semanticTone", "subtle")
        mode_row.addWidget(self._mode_label)
        self._mode_selector = QComboBox()
        self._mode_selector.setObjectName("mentorModeSelector")
        self._mode_selector.currentIndexChanged.connect(self._persist_mode)
        mode_row.addWidget(self._mode_selector, 1)
        body_layout.addLayout(mode_row)

        self._transcript = QTextBrowser()
        self._transcript.setObjectName("floatingTutorTranscript")
        self._transcript.setOpenExternalLinks(False)
        self._transcript.setMinimumHeight(210)
        self._transcript.setLineWrapMode(QTextEdit.LineWrapMode.WidgetWidth)
        self._transcript.setWordWrapMode(QTextOption.WrapMode.WrapAtWordBoundaryOrAnywhere)
        self._transcript.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOn)
        self._transcript.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        self._transcript.document().setDocumentMargin(8)
        self._transcript.document().setDefaultStyleSheet(
            "pre, code { font-family: monospace; white-space: pre-wrap; } "
            "table { border-collapse: collapse; } "
            "th, td { padding: 3px 6px; }"
        )
        body_layout.addWidget(self._transcript, 1)

        self._note_frame = QFrame()
        self._note_frame.setObjectName("mentorObservationFrame")
        self._note_frame.setProperty("cardRole", "surface")
        note_layout = QVBoxLayout(self._note_frame)
        note_layout.setContentsMargins(10, 8, 10, 8)
        note_layout.setSpacing(4)
        self._note_title = QLabel()
        self._note_title.setObjectName("mentorObservationTitle")
        note_layout.addWidget(self._note_title)
        self._note_body = QLabel()
        self._note_body.setObjectName("mentorObservationBody")
        self._note_body.setProperty("semanticTone", "muted")
        self._note_body.setWordWrap(True)
        self._note_body.setTextInteractionFlags(Qt.TextInteractionFlag.TextSelectableByMouse)
        note_layout.addWidget(self._note_body)
        self._note_disclaimer = QLabel()
        self._note_disclaimer.setProperty("semanticTone", "subtle")
        self._note_disclaimer.setWordWrap(True)
        note_layout.addWidget(self._note_disclaimer)
        self._note_frame.hide()
        body_layout.addWidget(self._note_frame)

        self._status = QLabel()
        self._status.setObjectName("floatingTutorStatus")
        self._status.setWordWrap(True)
        self._status.hide()
        body_layout.addWidget(self._status)

        self._question = QPlainTextEdit()
        self._question.setObjectName("floatingTutorQuestion")
        self._question.setMinimumHeight(72)
        self._question.setMaximumHeight(110)
        body_layout.addWidget(self._question)

        actions = QHBoxLayout()
        actions.addStretch(1)
        self._send_button = QPushButton()
        self._send_button.setObjectName("floatingTutorSendButton")
        self._send_button.setProperty("buttonRole", "primary")
        self._send_button.clicked.connect(self.send_question)
        actions.addWidget(self._send_button)
        body_layout.addLayout(actions)

        root.addWidget(self._body, 1)
        self.set_locale(locale)
        self.hide()

    @staticmethod
    def _header_button() -> QPushButton:
        button = QPushButton()
        button.setObjectName("floatingTutorHeaderButton")
        button.setProperty("buttonRole", "secondary")
        button.setFixedWidth(34)
        return button

    @property
    def conversation(self) -> tuple[ChatMessage, ...]:
        return tuple(self._history)

    @property
    def transcript_text(self) -> str:
        return self._transcript.toPlainText()

    @property
    def current_mode(self) -> MentorMode:
        value = self._mode_selector.currentData()
        try:
            return MentorMode(str(value))
        except ValueError:
            return MentorMode.SOCRATIC

    @property
    def journal(self) -> MentorJournalSnapshot:
        """Return the private mentor journal currently loaded by the panel."""

        return self._journal

    @property
    def is_minimized(self) -> bool:
        return self._minimized

    @property
    def has_custom_position(self) -> bool:
        """Return whether the learner has dragged the panel away from its default anchor."""

        return self._custom_position

    @property
    def active_context(self) -> str:
        return self._context_provider().strip()

    def eventFilter(self, watched: QObject, event: QEvent) -> bool:  # noqa: N802
        """Drag the panel from its header while leaving header buttons interactive."""

        if watched is not self._header or not isinstance(event, QMouseEvent):
            return super().eventFilter(watched, event)

        if (
            event.type() == QEvent.Type.MouseButtonPress
            and event.button() == Qt.MouseButton.LeftButton
        ):
            self._drag_offset = self.mapFromGlobal(event.globalPosition().toPoint())
            self._header.setCursor(Qt.CursorShape.ClosedHandCursor)
            self._header.grabMouse()
            self.raise_()
            event.accept()
            return True

        if event.type() == QEvent.Type.MouseMove and self._drag_offset is not None:
            host = self.parentWidget()
            if host is not None:
                pointer = host.mapFromGlobal(event.globalPosition().toPoint())
                self.move(self._bounded_position(pointer - self._drag_offset, host))
                self._custom_position = True
            event.accept()
            return True

        if (
            event.type() == QEvent.Type.MouseButtonRelease
            and event.button() == Qt.MouseButton.LeftButton
            and self._drag_offset is not None
        ):
            self._drag_offset = None
            self._header.releaseMouse()
            self._header.setCursor(Qt.CursorShape.OpenHandCursor)
            event.accept()
            return True

        return super().eventFilter(watched, event)

    def set_locale(self, locale: AppLocale | str) -> None:
        """Retranslate controls without discarding the conversation or mentor memory."""

        self._locale = locale if isinstance(locale, AppLocale) else AppLocale.resolve(locale)
        self._title.setText(tutor_chat_text(self._locale, TutorChatCopyKey.TITLE))
        self._mode_label.setText(tutor_chat_text(self._locale, TutorChatCopyKey.MODE))
        self._populate_mode_selector()
        self._send_button.setText(tutor_chat_text(self._locale, TutorChatCopyKey.SEND))
        self._reset_button.setText("↺")
        self._reset_button.setToolTip(tutor_chat_text(self._locale, TutorChatCopyKey.RESET))
        self._close_button.setText("×")
        self._close_button.setToolTip(tutor_chat_text(self._locale, TutorChatCopyKey.CLOSE))
        self._question.setPlaceholderText(
            tutor_chat_text(self._locale, TutorChatCopyKey.PLACEHOLDER)
        )
        self._update_minimize_copy()
        self.refresh_context()
        self._render_transcript()
        self._render_observation(self._last_observation)

    def refresh_context(self) -> None:
        context = self.active_context or "—"
        self._context.setText(
            tutor_chat_text(self._locale, TutorChatCopyKey.CONTEXT, context=context)
        )

    def show_panel(self) -> None:
        self.refresh_context()
        self.show()
        self.raise_()
        self.visibility_changed.emit(True)

    @Slot()
    def close_panel(self) -> None:
        self.cancel_request()
        self.hide()
        self.visibility_changed.emit(False)

    @Slot()
    def toggle_minimized(self) -> None:
        self._minimized = not self._minimized
        self._body.setVisible(not self._minimized)
        self.setFixedHeight(54 if self._minimized else 660)
        self.clamp_to_host()
        self._update_minimize_copy()
        self.raise_()

    @Slot()
    def reset_conversation(self) -> None:
        """Start a fresh visible dialogue while retaining longitudinal mentor memory."""

        self.cancel_request()
        self._session_id = uuid4().hex
        self._history.clear()
        self._last_observation = MentorObservation.empty()
        self._transcript.clear()
        self._question.clear()
        self._status.clear()
        self._status.hide()
        self._note_frame.hide()

    def clamp_to_host(self) -> None:
        """Keep the complete panel reachable after dragging or host resizing."""

        host = self.parentWidget()
        if host is not None:
            self.move(self._bounded_position(self.pos(), host))

    def explain_selection(self, selection: str) -> None:
        normalized = " ".join(selection.split())
        if not normalized:
            return
        self.show_panel()
        if self._minimized:
            self.toggle_minimized()
        self._question.setPlainText(
            tutor_chat_text(
                self._locale,
                TutorChatCopyKey.SELECTION_PROMPT,
                selection=normalized,
            )
        )
        self.send_question()

    @Slot()
    def send_question(self) -> None:
        if self._active_request_id is not None:
            return
        question = self._question.toPlainText().strip()
        if not question:
            self._show_status(tutor_chat_text(self._locale, TutorChatCopyKey.EMPTY), "warning")
            return

        self.refresh_context()
        context = self.active_context
        history = self._bounded_history()
        locale = self._locale
        mode = self.current_mode
        memory = self._journal.memory_for(context)
        self._request_serial += 1
        request_id = self._request_serial
        self._active_request_id = request_id
        self._pending_user_message = ChatMessage(ChatRole.USER, question)
        self._pending_context = context
        self._pending_mode = mode
        self._question.clear()
        self._set_busy(True)
        self._show_status(tutor_chat_text(locale, TutorChatCopyKey.THINKING), "pending")

        self._executor.submit(
            request_id,
            lambda: self._runner.ask(
                context,
                history,
                question,
                locale=locale,
                mode=mode,
                memory=memory,
            ),
            self._accept_response,
            self._accept_failure,
        )

    def cancel_request(self) -> None:
        if self._active_request_id is None:
            return
        request_id = self._active_request_id
        self._executor.cancel(request_id)
        self._active_request_id = None
        self._pending_user_message = None
        self._pending_context = ""
        self._request_serial += 1
        self._set_busy(False)
        self._status.hide()

    def _accept_response(self, request_id: int, result: MentorTurnResult) -> None:
        pending = self._pending_user_message
        if request_id != self._active_request_id or pending is None:
            return
        self._history.extend((pending, result.response.message))
        turn = MentorTurnRecord(
            session_id=self._session_id,
            created_at=datetime.now(UTC),
            context=self._pending_context,
            mode=self._pending_mode,
            user_message=pending.content,
            assistant_message=result.content,
            observation=result.observation,
            model=result.response.model,
            prompt_eval_count=result.response.prompt_eval_count,
            eval_count=result.response.eval_count,
            total_duration_ns=result.response.total_duration_ns,
        )
        self._journal = self._journal.append(turn)
        self._last_observation = result.observation
        storage_error = self._save_journal()
        self._active_request_id = None
        self._pending_user_message = None
        self._pending_context = ""
        self._set_busy(False)
        self._status.hide()
        self._render_transcript()
        self._render_observation(result.observation)
        if storage_error is not None:
            self._show_status(
                tutor_chat_text(
                    self._locale,
                    TutorChatCopyKey.ERROR,
                    detail=storage_error,
                ),
                "warning",
            )

    def _accept_failure(self, request_id: int, error: Exception) -> None:
        if request_id != self._active_request_id:
            return
        self._active_request_id = None
        self._pending_user_message = None
        self._pending_context = ""
        self._set_busy(False)
        detail = str(error).strip() or error.__class__.__name__
        self._show_status(
            tutor_chat_text(self._locale, TutorChatCopyKey.ERROR, detail=detail),
            "error",
        )

    def _save_journal(self) -> str | None:
        if self._journal_store is None:
            return None
        try:
            self._journal_store.save(self._journal)
        except OSError as exc:
            return str(exc).strip() or exc.__class__.__name__
        return None

    def _populate_mode_selector(self) -> None:
        selected = self.current_mode if self._mode_selector.count() else self._stored_mode()
        self._mode_selector.blockSignals(True)
        self._mode_selector.clear()
        for mode in MentorMode:
            self._mode_selector.addItem(
                tutor_chat_text(self._locale, _MODE_COPY[mode]),
                mode.value,
            )
        index = self._mode_selector.findData(selected.value)
        self._mode_selector.setCurrentIndex(max(0, index))
        self._mode_selector.blockSignals(False)

    def _stored_mode(self) -> MentorMode:
        raw = str(self._settings.value(self.MODE_KEY, MentorMode.SOCRATIC.value))
        try:
            return MentorMode(raw)
        except ValueError:
            return MentorMode.SOCRATIC

    @Slot()
    def _persist_mode(self) -> None:
        self._settings.setValue(self.MODE_KEY, self.current_mode.value)

    def _bounded_history(self) -> tuple[ChatMessage, ...]:
        history = self._history[-16:]
        while len(history) > 2 and sum(len(message.content) for message in history) > 24_000:
            history = history[2:]
        return tuple(history)

    def _render_transcript(self) -> None:
        user_label, tutor_label = {
            AppLocale.SPANISH_SPAIN: ("Tú", "Mentor"),
            AppLocale.ENGLISH: ("You", "Mentor"),
            AppLocale.DANISH_DENMARK: ("Dig", "Mentor"),
        }[self._locale]
        blocks: list[str] = []
        for message in self._history:
            label = user_label if message.role is ChatRole.USER else tutor_label
            blocks.append(f"**{label}**\n\n{message.content.strip()}")
        self._transcript.setMarkdown("\n\n---\n\n".join(blocks))
        scrollbar = self._transcript.verticalScrollBar()
        scrollbar.setValue(scrollbar.maximum())

    def _render_observation(self, observation: MentorObservation) -> None:
        lines: list[str] = []
        if observation.demonstrated:
            lines.append(
                tutor_chat_text(
                    self._locale,
                    TutorChatCopyKey.NOTE_DEMONSTRATED,
                    items="; ".join(observation.demonstrated),
                )
            )
        if observation.gaps:
            lines.append(
                tutor_chat_text(
                    self._locale,
                    TutorChatCopyKey.NOTE_GAPS,
                    items="; ".join(observation.gaps),
                )
            )
        if observation.misconceptions:
            lines.append(
                tutor_chat_text(
                    self._locale,
                    TutorChatCopyKey.NOTE_MISCONCEPTIONS,
                    items="; ".join(observation.misconceptions),
                )
            )
        if observation.recommended_next_action:
            lines.append(
                tutor_chat_text(
                    self._locale,
                    TutorChatCopyKey.NOTE_NEXT,
                    items=observation.recommended_next_action,
                )
            )
        if lines:
            lines.append(
                tutor_chat_text(
                    self._locale,
                    TutorChatCopyKey.NOTE_CONFIDENCE,
                    percent=round(observation.confidence * 100),
                )
            )
            self._note_title.setText(
                tutor_chat_text(self._locale, TutorChatCopyKey.NOTE_TITLE)
            )
            self._note_body.setText("\n".join(lines))
            self._note_disclaimer.setText(
                tutor_chat_text(self._locale, TutorChatCopyKey.NOTE_DISCLAIMER)
            )
            self._note_frame.show()
        else:
            self._note_frame.hide()

    def _set_busy(self, busy: bool) -> None:
        self._send_button.setEnabled(not busy)
        self._reset_button.setEnabled(not busy)
        self._mode_selector.setEnabled(not busy)
        self._question.setReadOnly(busy)

    def _show_status(self, text: str, state: str) -> None:
        self._status.setText(text)
        self._status.setProperty("chatState", state)
        self._status.show()
        self._refresh_style(self._status)

    def _update_minimize_copy(self) -> None:
        key = TutorChatCopyKey.RESTORE if self._minimized else TutorChatCopyKey.MINIMIZE
        self._minimize_button.setText("□" if self._minimized else "—")
        self._minimize_button.setToolTip(tutor_chat_text(self._locale, key))

    def _bounded_position(self, position: QPoint, host: QWidget) -> QPoint:
        max_x = max(0, host.width() - self.width())
        max_y = max(0, host.height() - self.height())
        return QPoint(
            min(max(0, position.x()), max_x),
            min(max(0, position.y()), max_y),
        )

    @staticmethod
    def _refresh_style(widget: QWidget) -> None:
        widget.style().unpolish(widget)
        widget.style().polish(widget)


class TutorSelectionEventFilter(QObject):
    """Add a mentor action to context menus when visible text is selected."""

    def __init__(
        self,
        panel: FloatingTutorChat,
        *,
        locale: AppLocale = DEFAULT_LOCALE,
        parent: QObject | None = None,
    ) -> None:
        super().__init__(parent)
        self._panel = panel
        self._locale = locale

    def set_locale(self, locale: AppLocale | str) -> None:
        self._locale = locale if isinstance(locale, AppLocale) else AppLocale.resolve(locale)

    def eventFilter(self, watched: QObject, event: QEvent) -> bool:  # noqa: N802
        if event.type() != QEvent.Type.ContextMenu or not isinstance(watched, QWidget):
            return False
        if watched is self._panel or self._panel.isAncestorOf(watched):
            return False
        if not isinstance(event, QContextMenuEvent):
            return False

        selection = self._selected_text(watched)
        if not selection:
            return False
        menu = self._standard_menu(watched)
        if menu.actions():
            menu.addSeparator()
        action = menu.addAction(tutor_chat_text(self._locale, TutorChatCopyKey.EXPLAIN_SELECTION))
        action.triggered.connect(
            lambda checked=False, text=selection: self._panel.explain_selection(text)
        )
        menu.exec(event.globalPos())
        menu.deleteLater()
        return True

    @staticmethod
    def _selected_text(widget: QWidget) -> str:
        if isinstance(widget, QLabel):
            return widget.selectedText().strip()
        if isinstance(widget, QLineEdit):
            return widget.selectedText().strip()
        if isinstance(widget, (QPlainTextEdit, QTextEdit)):
            return widget.textCursor().selectedText().replace("\u2029", "\n").strip()
        return ""

    @staticmethod
    def _standard_menu(widget: QWidget) -> QMenu:
        if isinstance(widget, QLineEdit):
            return widget.createStandardContextMenu()
        if isinstance(widget, (QPlainTextEdit, QTextEdit)):
            return widget.createStandardContextMenu()
        return QMenu(widget)


def position_floating_tutor(
    panel: FloatingTutorChat,
    launcher: QPushButton,
    host: QWidget,
) -> None:
    """Anchor a new panel, then preserve and constrain any learner-selected position."""

    margin = 18
    launcher.adjustSize()
    launcher.move(
        max(margin, host.width() - launcher.width() - margin),
        max(margin, host.height() - launcher.height() - margin),
    )
    panel_height = 54 if panel.is_minimized else min(660, host.height() - 90)
    panel.setFixedHeight(max(54, panel_height))
    if panel.has_custom_position:
        panel.clamp_to_host()
    else:
        panel.move(
            max(margin, host.width() - panel.width() - margin),
            max(margin, host.height() - panel.height() - launcher.height() - margin * 2),
        )
    launcher.raise_()
    if panel.isVisible():
        panel.raise_()


__all__ = [
    "FloatingTutorChat",
    "OllamaTutorChatRunner",
    "QtTutorChatExecutor",
    "TutorChatExecutor",
    "TutorChatRunner",
    "TutorSelectionEventFilter",
    "position_floating_tutor",
]
