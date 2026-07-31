"""Asynchronous adaptive Ollama tutor for verified programming diagnostics."""

from __future__ import annotations

from collections.abc import Callable
from typing import Protocol

from PySide6.QtCore import QObject, QRunnable, QThreadPool, Signal, Slot
from PySide6.QtWidgets import (
    QComboBox,
    QFrame,
    QHBoxLayout,
    QLabel,
    QPlainTextEdit,
    QPushButton,
    QTextBrowser,
    QVBoxLayout,
    QWidget,
)

from ...i18n.adaptive_tutor_copy import AdaptiveTutorCopyKey, adaptive_tutor_text
from ...i18n.challenge_tutor_copy import ChallengeTutorCopyKey, challenge_tutor_text
from ...i18n.locales import DEFAULT_LOCALE, AppLocale
from ...integrations import DEFAULT_CHAT_MODEL, OllamaConnectionError, OllamaProtocolError
from ...tutoring import (
    ChallengeDiagnostic,
    ChallengeTutorResponse,
    TutorAssistanceLevel,
    TutorSessionSnapshot,
    TutorSessionTurn,
)
from .challenge_tutor_styles import CHALLENGE_TUTOR_STYLESHEET


class ChallengeTutorRunner(Protocol):
    """Minimal adaptive service contract consumed by the tutor panel."""

    def ask(
        self,
        diagnostic: ChallengeDiagnostic,
        question: str,
        *,
        assistance_level: TutorAssistanceLevel = TutorAssistanceLevel.SOCRATIC,
        history: tuple[TutorSessionTurn, ...] = (),
    ) -> ChallengeTutorResponse:
        """Return one grounded explanation for a verified diagnostic."""


TutorTask = Callable[[], ChallengeTutorResponse]
TutorSuccessCallback = Callable[[int, ChallengeTutorResponse], None]
TutorFailureCallback = Callable[[int, Exception], None]


class ChallengeTutorExecutor(Protocol):
    """Execution boundary that keeps Ollama requests outside the Qt UI thread."""

    def submit(
        self,
        request_id: int,
        task: TutorTask,
        on_success: TutorSuccessCallback,
        on_failure: TutorFailureCallback,
    ) -> None:
        """Schedule one tutor request and report its eventual outcome."""

    def cancel(self, request_id: int) -> None:
        """Cancel or detach one request without blocking the user interface."""


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
        except Exception as exc:  # pragma: no cover - exercised through the panel boundary
            self.signals.failed.emit(self._request_id, exc)
        else:
            self.signals.succeeded.emit(self._request_id, response)


class QtChallengeTutorExecutor:
    """Run blocking Ollama generation in Qt's shared worker pool."""

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
        """Detach from a running HTTP call; stale results are rejected by request ID."""

        del request_id


_LEVEL_COPY = {
    TutorAssistanceLevel.SOCRATIC: AdaptiveTutorCopyKey.LEVEL_SOCRATIC,
    TutorAssistanceLevel.CONCEPTUAL: AdaptiveTutorCopyKey.LEVEL_CONCEPTUAL,
    TutorAssistanceLevel.STRUCTURAL: AdaptiveTutorCopyKey.LEVEL_STRUCTURAL,
    TutorAssistanceLevel.EXPLANATION: AdaptiveTutorCopyKey.LEVEL_EXPLANATION,
}

_HINT_COPY = {
    TutorAssistanceLevel.SOCRATIC: AdaptiveTutorCopyKey.HINT_QUESTION_SOCRATIC,
    TutorAssistanceLevel.CONCEPTUAL: AdaptiveTutorCopyKey.HINT_QUESTION_CONCEPTUAL,
    TutorAssistanceLevel.STRUCTURAL: AdaptiveTutorCopyKey.HINT_QUESTION_STRUCTURAL,
    TutorAssistanceLevel.EXPLANATION: AdaptiveTutorCopyKey.HINT_QUESTION_EXPLANATION,
}


class ChallengeTutorPanel(QFrame):
    """Maintain one bounded adaptive dialogue for the latest verified diagnostic."""

    response_ready = Signal(object)
    response_rated = Signal(bool)

    def __init__(
        self,
        tutor: ChallengeTutorRunner,
        *,
        locale: AppLocale = DEFAULT_LOCALE,
        executor: ChallengeTutorExecutor | None = None,
        max_session_turns: int = 6,
        parent: QWidget | None = None,
    ) -> None:
        super().__init__(parent)
        if max_session_turns < 1:
            raise ValueError("max_session_turns must be at least 1.")
        self.setObjectName("challengeTutorPanel")
        self.setStyleSheet(CHALLENGE_TUTOR_STYLESHEET)
        self._tutor = tutor
        self._locale = locale
        self._executor = executor or QtChallengeTutorExecutor()
        self._max_session_turns = max_session_turns
        self._diagnostic: ChallengeDiagnostic | None = None
        self._session = TutorSessionSnapshot()
        self._last_response: ChallengeTutorResponse | None = None
        self._request_serial = 0
        self._active_request_id: int | None = None
        self._pending_question = ""
        self._pending_level = TutorAssistanceLevel.SOCRATIC

        layout = QVBoxLayout(self)
        layout.setContentsMargins(16, 14, 16, 14)
        layout.setSpacing(9)

        title = QLabel(challenge_tutor_text(locale, ChallengeTutorCopyKey.TITLE))
        title.setObjectName("challengeTutorTitle")
        layout.addWidget(title)

        intro = QLabel(challenge_tutor_text(locale, ChallengeTutorCopyKey.INTRO))
        intro.setObjectName("challengeTutorIntro")
        intro.setWordWrap(True)
        layout.addWidget(intro)

        self._status = QLabel(challenge_tutor_text(locale, ChallengeTutorCopyKey.WAITING))
        self._status.setObjectName("challengeTutorStatus")
        self._status.setWordWrap(True)
        layout.addWidget(self._status)

        level_row = QHBoxLayout()
        level_row.setContentsMargins(0, 0, 0, 0)
        level_row.setSpacing(8)
        level_label = QLabel(adaptive_tutor_text(locale, AdaptiveTutorCopyKey.LEVEL_LABEL))
        level_label.setObjectName("challengeTutorLevelLabel")
        self._level_selector = QComboBox()
        self._level_selector.setObjectName("challengeTutorLevelSelector")
        for level in TutorAssistanceLevel:
            self._level_selector.addItem(
                adaptive_tutor_text(locale, _LEVEL_COPY[level]),
                level.value,
            )
        level_row.addWidget(level_label)
        level_row.addWidget(self._level_selector, 1)
        layout.addLayout(level_row)

        self._question = QPlainTextEdit()
        self._question.setObjectName("challengeTutorQuestion")
        self._question.setPlaceholderText(
            challenge_tutor_text(locale, ChallengeTutorCopyKey.QUESTION_PLACEHOLDER)
        )
        self._question.setMinimumHeight(82)
        self._question.setMaximumHeight(132)
        self._question.textChanged.connect(self._update_actions)
        layout.addWidget(self._question)

        actions = QHBoxLayout()
        actions.setContentsMargins(0, 0, 0, 0)
        actions.setSpacing(8)

        self._hint_button = QPushButton(
            adaptive_tutor_text(locale, AdaptiveTutorCopyKey.REQUEST_LEVEL)
        )
        self._hint_button.setObjectName("challengeTutorSecondaryButton")
        self._hint_button.clicked.connect(self.request_hint)
        actions.addWidget(self._hint_button)

        self._ask_button = QPushButton(challenge_tutor_text(locale, ChallengeTutorCopyKey.ASK))
        self._ask_button.setObjectName("challengeTutorPrimaryButton")
        self._ask_button.clicked.connect(self.ask_question)
        actions.addWidget(self._ask_button)

        self._cancel_button = QPushButton(
            challenge_tutor_text(locale, ChallengeTutorCopyKey.CANCEL)
        )
        self._cancel_button.setObjectName("challengeTutorCancelButton")
        self._cancel_button.clicked.connect(self.cancel_request)
        self._cancel_button.hide()
        actions.addWidget(self._cancel_button)
        actions.addStretch(1)
        layout.addLayout(actions)

        self._response_heading = QLabel(
            challenge_tutor_text(locale, ChallengeTutorCopyKey.RESPONSE_TITLE)
        )
        self._response_heading.setObjectName("contentSubheading")
        self._response_heading.hide()
        layout.addWidget(self._response_heading)

        self._response = QTextBrowser()
        self._response.setObjectName("challengeTutorResponse")
        self._response.setOpenExternalLinks(False)
        self._response.setMinimumHeight(130)
        self._response.hide()
        layout.addWidget(self._response)

        self._sources_heading = QLabel(challenge_tutor_text(locale, ChallengeTutorCopyKey.SOURCES))
        self._sources_heading.setObjectName("contentSubheading")
        self._sources_heading.hide()
        layout.addWidget(self._sources_heading)

        self._sources = QLabel()
        self._sources.setObjectName("challengeTutorSources")
        self._sources.setWordWrap(True)
        self._sources.hide()
        layout.addWidget(self._sources)

        self._model = QLabel()
        self._model.setObjectName("challengeTutorModel")
        self._model.hide()
        layout.addWidget(self._model)

        self._rating_widget = QWidget()
        rating_layout = QHBoxLayout(self._rating_widget)
        rating_layout.setContentsMargins(0, 0, 0, 0)
        rating_layout.setSpacing(8)
        rating_label = QLabel(adaptive_tutor_text(locale, AdaptiveTutorCopyKey.HELPFUL_PROMPT))
        rating_label.setObjectName("challengeTutorRatingLabel")
        self._helpful_button = QPushButton(
            adaptive_tutor_text(locale, AdaptiveTutorCopyKey.HELPFUL)
        )
        self._helpful_button.setObjectName("challengeTutorHelpfulButton")
        self._helpful_button.clicked.connect(self.mark_helpful)
        self._not_helpful_button = QPushButton(
            adaptive_tutor_text(locale, AdaptiveTutorCopyKey.NOT_HELPFUL)
        )
        self._not_helpful_button.setObjectName("challengeTutorNotHelpfulButton")
        self._not_helpful_button.clicked.connect(self.mark_not_helpful)
        rating_layout.addWidget(rating_label)
        rating_layout.addWidget(self._helpful_button)
        rating_layout.addWidget(self._not_helpful_button)
        rating_layout.addStretch(1)
        self._rating_widget.hide()
        layout.addWidget(self._rating_widget)

        self._history_heading = QLabel(
            adaptive_tutor_text(locale, AdaptiveTutorCopyKey.HISTORY_TITLE)
        )
        self._history_heading.setObjectName("contentSubheading")
        self._history_heading.hide()
        layout.addWidget(self._history_heading)

        self._history = QTextBrowser()
        self._history.setObjectName("challengeTutorHistory")
        self._history.setOpenExternalLinks(False)
        self._history.setMinimumHeight(150)
        self._history.hide()
        layout.addWidget(self._history)

        notice = QLabel(challenge_tutor_text(locale, ChallengeTutorCopyKey.NON_GRADING_NOTICE))
        notice.setObjectName("challengeTutorNotice")
        notice.setWordWrap(True)
        layout.addWidget(notice)

        session_notice = QLabel(adaptive_tutor_text(locale, AdaptiveTutorCopyKey.SESSION_NOTICE))
        session_notice.setObjectName("challengeTutorNotice")
        session_notice.setWordWrap(True)
        layout.addWidget(session_notice)

        self._update_actions()

    @property
    def diagnostic(self) -> ChallengeDiagnostic | None:
        """Return the immutable diagnostic currently available to the tutor."""

        return self._diagnostic

    @property
    def last_response(self) -> ChallengeTutorResponse | None:
        """Return the latest accepted tutor response."""

        return self._last_response

    @property
    def session_turns(self) -> tuple[TutorSessionTurn, ...]:
        """Return the bounded source-traceable conversation history."""

        return self._session.turns

    @property
    def assistance_count(self) -> int:
        """Return how many tutor responses supported the current diagnostic."""

        return self._session.assistance_count

    @property
    def solution_revealed(self) -> bool:
        """Return whether full explanation was used before the next attempt."""

        return self._session.solution_revealed

    @property
    def selected_level(self) -> TutorAssistanceLevel:
        """Return the currently selected assistance level."""

        data = self._level_selector.currentData()
        return TutorAssistanceLevel(str(data))

    @property
    def is_busy(self) -> bool:
        """Return whether this panel is waiting for an Ollama response."""

        return self._active_request_id is not None

    @property
    def status_text(self) -> str:
        return self._status.text()

    @property
    def response_text(self) -> str:
        return self._response.toPlainText()

    @property
    def history_text(self) -> str:
        return self._history.toPlainText()

    @property
    def sources_text(self) -> str:
        return self._sources.text()

    @property
    def model_text(self) -> str:
        return self._model.text()

    @property
    def question_text(self) -> str:
        return self._question.toPlainText()

    def set_question(self, question: str) -> None:
        """Replace the editable learner question."""

        self._question.setPlainText(question)

    def set_assistance_level(self, level: TutorAssistanceLevel) -> None:
        """Select one stable pedagogical support level."""

        index = self._level_selector.findData(level.value)
        if index < 0:
            raise ValueError(f"Unknown tutor assistance level: {level.value}")
        self._level_selector.setCurrentIndex(index)

    def set_diagnostic(self, diagnostic: ChallengeDiagnostic) -> None:
        """Install a new verified result and start a clean tutor session."""

        self._cancel_active(silent=True)
        self._diagnostic = diagnostic
        self._reset_session()
        self._set_status(
            challenge_tutor_text(self._locale, ChallengeTutorCopyKey.READY),
            state="ready",
        )
        self._update_actions()

    def begin_evaluation(self) -> None:
        """Invalidate dialogue state when a new deterministic run begins."""

        self._cancel_active(silent=True)
        self._diagnostic = None
        self._reset_session()
        self._set_status(
            challenge_tutor_text(self._locale, ChallengeTutorCopyKey.WAITING),
            state="waiting",
        )
        self._update_actions()

    def clear_diagnostic(self) -> None:
        """Remove all tutor state, for example when resetting the challenge."""

        self.begin_evaluation()

    @Slot()
    def request_hint(self) -> None:
        """Submit a localized request for the selected assistance level."""

        question = adaptive_tutor_text(self._locale, _HINT_COPY[self.selected_level])
        self._question.setPlainText(question)
        self._start_request(question)

    @Slot()
    def ask_question(self) -> None:
        """Submit the learner's question for asynchronous local generation."""

        question = self.question_text.strip()
        if not question:
            self._set_status(
                challenge_tutor_text(self._locale, ChallengeTutorCopyKey.QUESTION_REQUIRED),
                state="error",
            )
            self._update_actions()
            return
        self._start_request(question)

    @Slot()
    def cancel_request(self) -> None:
        """Detach the UI from the active request and ignore any late response."""

        self._cancel_active(silent=False)

    @Slot()
    def mark_helpful(self) -> None:
        """Record positive usefulness feedback for the latest response."""

        self._rate_latest(True)

    @Slot()
    def mark_not_helpful(self) -> None:
        """Record insufficient help and suggest the next stronger level."""

        self._rate_latest(False)

    def _start_request(self, question: str) -> None:
        diagnostic = self._diagnostic
        if diagnostic is None or self.is_busy:
            return

        self._request_serial += 1
        request_id = self._request_serial
        level = self.selected_level
        history = self._session.turns
        self._active_request_id = request_id
        self._pending_question = question
        self._pending_level = level
        self._clear_latest_response()
        self._set_status(
            challenge_tutor_text(self._locale, ChallengeTutorCopyKey.RUNNING),
            state="running",
        )
        self._set_busy(True)

        try:
            self._executor.submit(
                request_id,
                lambda: self._tutor.ask(
                    diagnostic,
                    question,
                    assistance_level=level,
                    history=history,
                ),
                self._handle_success,
                self._handle_failure,
            )
        except Exception as exc:  # pragma: no cover - defensive executor boundary
            self._handle_failure(request_id, exc)

    def _cancel_active(self, *, silent: bool) -> None:
        request_id = self._active_request_id
        if request_id is None:
            return
        self._executor.cancel(request_id)
        self._active_request_id = None
        self._pending_question = ""
        self._set_busy(False)
        if not silent:
            self._set_status(
                challenge_tutor_text(self._locale, ChallengeTutorCopyKey.CANCELLED),
                state="ready",
            )

    @Slot(int, object)
    def _handle_success(self, request_id: int, payload: object) -> None:
        if request_id != self._active_request_id:
            return
        if not isinstance(payload, ChallengeTutorResponse):
            self._handle_failure(
                request_id,
                TypeError("The tutor executor returned an unexpected response type."),
            )
            return

        question = self._pending_question
        level = self._pending_level
        self._active_request_id = None
        self._pending_question = ""
        self._set_busy(False)
        self._last_response = payload
        self._session = self._session.append(
            TutorSessionTurn(
                question=question,
                response=payload.content,
                assistance_level=level,
                model=payload.model,
                source_ids=payload.source_ids,
            ),
            max_turns=self._max_session_turns,
        )
        self._response.setMarkdown(payload.content)
        self._response_heading.show()
        self._response.show()
        self._sources.setText("\n".join(f"• {source_id}" for source_id in payload.source_ids))
        self._sources_heading.show()
        self._sources.show()
        self._model.setText(
            challenge_tutor_text(
                self._locale,
                ChallengeTutorCopyKey.MODEL,
                model=payload.model,
            )
        )
        self._model.show()
        self._rating_widget.show()
        self._render_history()
        self._set_status(
            challenge_tutor_text(self._locale, ChallengeTutorCopyKey.READY),
            state="ready",
        )
        self.response_ready.emit(payload)

    @Slot(int, object)
    def _handle_failure(self, request_id: int, payload: object) -> None:
        if request_id != self._active_request_id:
            return
        error = payload if isinstance(payload, Exception) else RuntimeError(str(payload))
        self._active_request_id = None
        self._pending_question = ""
        self._set_busy(False)
        self._last_response = None
        self._set_status(self._localized_error(error), state="error")

    def _rate_latest(self, helpful: bool) -> None:
        if not self._session.turns or self._session.turns[-1].helpful is not None:
            return
        previous_level = self._session.turns[-1].assistance_level
        self._session = self._session.rate_latest(helpful)
        self._rating_widget.hide()
        self._render_history()
        if helpful:
            status = adaptive_tutor_text(
                self._locale,
                AdaptiveTutorCopyKey.RATED_HELPFUL,
            )
        else:
            next_level = previous_level.next_level
            if next_level is previous_level:
                status = adaptive_tutor_text(
                    self._locale,
                    AdaptiveTutorCopyKey.RATED_NOT_HELPFUL,
                )
            else:
                self.set_assistance_level(next_level)
                level_text = adaptive_tutor_text(self._locale, _LEVEL_COPY[next_level])
                status = " ".join(
                    (
                        adaptive_tutor_text(
                            self._locale,
                            AdaptiveTutorCopyKey.RATED_NOT_HELPFUL,
                        ),
                        adaptive_tutor_text(
                            self._locale,
                            AdaptiveTutorCopyKey.ESCALATED,
                            level=level_text,
                        ),
                    )
                )
        self._set_status(status, state="ready")
        self.response_rated.emit(helpful)

    def _render_history(self) -> None:
        sections: list[str] = []
        for number, turn in enumerate(self._session.turns, start=1):
            level = adaptive_tutor_text(self._locale, _LEVEL_COPY[turn.assistance_level])
            title = adaptive_tutor_text(
                self._locale,
                AdaptiveTutorCopyKey.TURN_TITLE,
                number=number,
                level=level,
            )
            question = adaptive_tutor_text(
                self._locale,
                AdaptiveTutorCopyKey.TURN_QUESTION,
                question=turn.question,
            )
            sources = adaptive_tutor_text(
                self._locale,
                AdaptiveTutorCopyKey.TURN_SOURCES,
                sources=", ".join(turn.source_ids),
            )
            model = adaptive_tutor_text(
                self._locale,
                AdaptiveTutorCopyKey.TURN_MODEL,
                model=turn.model,
            )
            rating = ""
            if turn.helpful is not None:
                rating_key = (
                    AdaptiveTutorCopyKey.RATING_HELPFUL
                    if turn.helpful
                    else AdaptiveTutorCopyKey.RATING_NOT_HELPFUL
                )
                rating = f"\n\n**{adaptive_tutor_text(self._locale, rating_key)}**"
            sections.append(
                f"### {title}\n\n**{question}**\n\n{turn.response}\n\n{sources}\n\n{model}{rating}"
            )
        if sections:
            self._history.setMarkdown("\n\n---\n\n".join(sections))
            self._history_heading.show()
            self._history.show()
        else:
            self._history.clear()
            self._history.hide()
            self._history_heading.hide()

    def _localized_error(self, error: Exception) -> str:
        detail = " ".join(str(error).split())
        normalized = detail.casefold()
        if isinstance(error, OllamaConnectionError):
            model_missing = "model" in normalized and any(
                token in normalized for token in ("not found", "not installed", "pull", "missing")
            )
            if model_missing:
                return challenge_tutor_text(
                    self._locale,
                    ChallengeTutorCopyKey.ERROR_MODEL_MISSING,
                    model=DEFAULT_CHAT_MODEL,
                )
            return challenge_tutor_text(
                self._locale,
                ChallengeTutorCopyKey.ERROR_CONNECTION,
            )
        if isinstance(error, OllamaProtocolError):
            return challenge_tutor_text(
                self._locale,
                ChallengeTutorCopyKey.ERROR_PROTOCOL,
            )
        safe_detail = detail[:240] or error.__class__.__name__
        return challenge_tutor_text(
            self._locale,
            ChallengeTutorCopyKey.ERROR_GENERIC,
            detail=safe_detail,
        )

    def _clear_latest_response(self) -> None:
        self._last_response = None
        self._response.clear()
        self._response.hide()
        self._response_heading.hide()
        self._sources.clear()
        self._sources.hide()
        self._sources_heading.hide()
        self._model.clear()
        self._model.hide()
        self._rating_widget.hide()

    def _reset_session(self) -> None:
        self._session = TutorSessionSnapshot()
        self._pending_question = ""
        self._pending_level = TutorAssistanceLevel.SOCRATIC
        self.set_assistance_level(TutorAssistanceLevel.SOCRATIC)
        self._question.clear()
        self._clear_latest_response()
        self._render_history()

    def _set_busy(self, busy: bool) -> None:
        self._question.setReadOnly(busy)
        self._level_selector.setEnabled(not busy)
        self._cancel_button.setVisible(busy)
        self._update_actions()

    @Slot()
    def _update_actions(self) -> None:
        available = self._diagnostic is not None and not self.is_busy
        self._hint_button.setEnabled(available)
        self._ask_button.setEnabled(available and bool(self.question_text.strip()))

    def _set_status(self, text: str, *, state: str) -> None:
        self._status.setText(text)
        self._status.setProperty("state", state)
        self._status.style().unpolish(self._status)
        self._status.style().polish(self._status)


__all__ = [
    "ChallengeTutorExecutor",
    "ChallengeTutorPanel",
    "ChallengeTutorRunner",
    "QtChallengeTutorExecutor",
]
