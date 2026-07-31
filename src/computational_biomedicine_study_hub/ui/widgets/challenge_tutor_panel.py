"""Asynchronous, non-grading Ollama tutor for verified programming diagnostics."""

from __future__ import annotations

from collections.abc import Callable
from typing import Protocol

from PySide6.QtCore import QObject, QRunnable, QThreadPool, Signal, Slot
from PySide6.QtWidgets import (
    QFrame,
    QHBoxLayout,
    QLabel,
    QPlainTextEdit,
    QPushButton,
    QTextBrowser,
    QVBoxLayout,
    QWidget,
)

from ...i18n.challenge_tutor_copy import ChallengeTutorCopyKey, challenge_tutor_text
from ...i18n.locales import DEFAULT_LOCALE, AppLocale
from ...integrations import (
    DEFAULT_CHAT_MODEL,
    OllamaConnectionError,
    OllamaProtocolError,
)
from ...tutoring import ChallengeDiagnostic, ChallengeTutorResponse
from .challenge_tutor_styles import CHALLENGE_TUTOR_STYLESHEET


class ChallengeTutorRunner(Protocol):
    """Minimal service contract consumed by the tutor panel."""

    def ask(self, diagnostic: ChallengeDiagnostic, question: str) -> ChallengeTutorResponse:
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


class ChallengeTutorPanel(QFrame):
    """Ask a local tutor about the latest immutable deterministic diagnostic."""

    response_ready = Signal(object)

    def __init__(
        self,
        tutor: ChallengeTutorRunner,
        *,
        locale: AppLocale = DEFAULT_LOCALE,
        executor: ChallengeTutorExecutor | None = None,
        parent: QWidget | None = None,
    ) -> None:
        super().__init__(parent)
        self.setObjectName("challengeTutorPanel")
        self.setStyleSheet(CHALLENGE_TUTOR_STYLESHEET)
        self._tutor = tutor
        self._locale = locale
        self._executor = executor or QtChallengeTutorExecutor()
        self._diagnostic: ChallengeDiagnostic | None = None
        self._last_response: ChallengeTutorResponse | None = None
        self._request_serial = 0
        self._active_request_id: int | None = None

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
            challenge_tutor_text(locale, ChallengeTutorCopyKey.HINT)
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

        self._sources_heading = QLabel(
            challenge_tutor_text(locale, ChallengeTutorCopyKey.SOURCES)
        )
        self._sources_heading.setObjectName("contentSubheading")
        self._sources_heading.hide()
        layout.addWidget(self._sources_heading)

        self._sources = QLabel()
        self._sources.setObjectName("challengeTutorSources")
        self._sources.setWordWrap(True)
        self._sources.setTextInteractionFlags(self._sources.textInteractionFlags())
        self._sources.hide()
        layout.addWidget(self._sources)

        self._model = QLabel()
        self._model.setObjectName("challengeTutorModel")
        self._model.hide()
        layout.addWidget(self._model)

        notice = QLabel(
            challenge_tutor_text(locale, ChallengeTutorCopyKey.NON_GRADING_NOTICE)
        )
        notice.setObjectName("challengeTutorNotice")
        notice.setWordWrap(True)
        layout.addWidget(notice)

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

    def set_diagnostic(self, diagnostic: ChallengeDiagnostic) -> None:
        """Install a new verified result and invalidate any older explanation."""

        self._cancel_active(silent=True)
        self._diagnostic = diagnostic
        self._clear_response()
        self._set_status(
            challenge_tutor_text(self._locale, ChallengeTutorCopyKey.READY),
            state="ready",
        )
        self._update_actions()

    def begin_evaluation(self) -> None:
        """Invalidate prior tutor output when a new deterministic run begins."""

        self._cancel_active(silent=True)
        self._diagnostic = None
        self._clear_response()
        self._set_status(
            challenge_tutor_text(self._locale, ChallengeTutorCopyKey.WAITING),
            state="waiting",
        )
        self._update_actions()

    def clear_diagnostic(self) -> None:
        """Remove all tutor state, for example when resetting the challenge."""

        self.begin_evaluation()
        self._question.clear()

    @Slot()
    def request_hint(self) -> None:
        """Submit a localized hint request without exposing hidden tests."""

        question = challenge_tutor_text(
            self._locale,
            ChallengeTutorCopyKey.DEFAULT_HINT_QUESTION,
        )
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

    def _start_request(self, question: str) -> None:
        diagnostic = self._diagnostic
        if diagnostic is None or self.is_busy:
            return

        self._request_serial += 1
        request_id = self._request_serial
        self._active_request_id = request_id
        self._clear_response()
        self._set_status(
            challenge_tutor_text(self._locale, ChallengeTutorCopyKey.RUNNING),
            state="running",
        )
        self._set_busy(True)

        try:
            self._executor.submit(
                request_id,
                lambda: self._tutor.ask(diagnostic, question),
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

        self._active_request_id = None
        self._set_busy(False)
        self._last_response = payload
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
        self._set_busy(False)
        self._last_response = None
        self._set_status(self._localized_error(error), state="error")

    def _localized_error(self, error: Exception) -> str:
        detail = " ".join(str(error).split())
        normalized = detail.casefold()
        if isinstance(error, OllamaConnectionError):
            model_missing = "model" in normalized and any(
                token in normalized
                for token in ("not found", "not installed", "pull", "missing")
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

    def _clear_response(self) -> None:
        self._last_response = None
        self._response.clear()
        self._response.hide()
        self._response_heading.hide()
        self._sources.clear()
        self._sources.hide()
        self._sources_heading.hide()
        self._model.clear()
        self._model.hide()

    def _set_busy(self, busy: bool) -> None:
        self._question.setReadOnly(busy)
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
