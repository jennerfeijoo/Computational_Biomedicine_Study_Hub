"""Qt worker boundary for blocking local written-feedback generation."""

from __future__ import annotations

from collections.abc import Callable
from typing import Protocol

from PySide6.QtCore import QObject, QRunnable, QThreadPool, Signal, Slot

from ..tutoring.written_feedback import WrittenFeedbackResponse

FeedbackTask = Callable[[], WrittenFeedbackResponse]
FeedbackSuccessCallback = Callable[[int, WrittenFeedbackResponse], None]
FeedbackFailureCallback = Callable[[int, Exception], None]


class WrittenFeedbackExecutor(Protocol):
    """Keep blocking Ollama calls outside the Qt UI thread."""

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
        except Exception as exc:  # pragma: no cover - worker-thread boundary
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


__all__ = ["QtWrittenFeedbackExecutor", "WrittenFeedbackExecutor"]
