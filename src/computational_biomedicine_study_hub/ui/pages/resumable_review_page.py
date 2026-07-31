"""Review page extension that resumes catalog-bound adaptive sessions."""

from __future__ import annotations

from PySide6.QtCore import Slot
from PySide6.QtWidgets import QLabel, QPushButton, QWidget

from ...i18n import AdaptiveReviewCopyKey, AppLocale, adaptive_review_text
from ...learning.adaptive_review import (
    AdaptiveReviewSession,
    AdaptiveReviewSessionSnapshot,
    AdaptiveReviewSnapshotError,
)
from ...learning.progress_service import LearningProgressService
from ...storage import AdaptiveReviewSessionStore, SQLiteProgressStore
from ..widgets.adaptive_review_session_widget import AdaptiveReviewSessionWidget
from .review_page import Clock
from .review_page import ReviewPage as BaseReviewPage


class ResumableReviewPage(BaseReviewPage):
    """Add explicit resume/discard controls and safe catalog invalidation."""

    def __init__(
        self,
        progress_store: SQLiteProgressStore | None,
        locale: AppLocale,
        *,
        clock: Clock | None = None,
        parent: QWidget | None = None,
    ) -> None:
        self._session_state_store = (
            AdaptiveReviewSessionStore.for_progress_store(progress_store)
            if progress_store is not None
            else None
        )
        self._resume_snapshot: AdaptiveReviewSessionSnapshot | None = None
        self._discard_button: QPushButton | None = None
        super().__init__(progress_store, locale, clock=clock, parent=parent)

    @property
    def resumable_snapshot(self) -> AdaptiveReviewSessionSnapshot | None:
        """Return the validated snapshot prepared for the resume action."""

        return self._resume_snapshot

    @property
    def discard_session_button(self) -> QPushButton | None:
        """Expose the optional discard action for deterministic UI tests."""

        return self._discard_button

    @Slot()
    def refresh(self) -> None:
        """Flush active work before rebuilding the review launcher and queues."""

        self.persist_active_session()
        super().refresh()

    def _render_session_launcher(self) -> None:
        self._clear_layout(self._session_layout)
        self._session_widget = None
        self._resume_snapshot = None
        self._discard_button = None
        invalidated = False

        snapshot = self._session_state_store.load() if self._session_state_store is not None else None
        if snapshot is not None:
            try:
                restored = AdaptiveReviewSession.from_snapshot(
                    snapshot,
                    locale=self._locale,
                )
            except AdaptiveReviewSnapshotError:
                invalidated = True
                assert self._session_state_store is not None
                self._session_state_store.discard()
            else:
                if restored.can_start:
                    self._pending_session = restored
                    self._resume_snapshot = snapshot
                    self._session_start_button.setEnabled(True)
                    self._session_start_button.setText(
                        adaptive_review_text(self._locale, AdaptiveReviewCopyKey.RESUME)
                    )
                    self._session_status.setText(
                        adaptive_review_text(
                            self._locale,
                            AdaptiveReviewCopyKey.RESUME_AVAILABLE,
                            answered=restored.answered_count,
                            target=restored.target_questions,
                        )
                    )
                    discard = QPushButton(
                        adaptive_review_text(self._locale, AdaptiveReviewCopyKey.DISCARD)
                    )
                    discard.setObjectName("adaptiveReviewDiscardButton")
                    discard.clicked.connect(self.discard_saved_session)
                    self._discard_button = discard
                    self._session_layout.addWidget(discard)
                    return
                assert self._session_state_store is not None
                self._session_state_store.discard()

        self._pending_session = AdaptiveReviewSession(
            self._items,
            locale=self._locale,
            target_questions=6,
        )
        session = self._pending_session
        self._session_start_button.setEnabled(session.can_start)
        self._session_start_button.setText(
            adaptive_review_text(self._locale, AdaptiveReviewCopyKey.START)
        )

        status_parts: list[str] = []
        if invalidated:
            status_parts.append(
                adaptive_review_text(self._locale, AdaptiveReviewCopyKey.INVALIDATED)
            )
        if not self._items:
            status_parts.append(
                adaptive_review_text(self._locale, AdaptiveReviewCopyKey.NO_DUE)
            )
            self._session_status.setText("\n\n".join(status_parts))
            return

        status_parts.append(
            adaptive_review_text(
                self._locale,
                AdaptiveReviewCopyKey.DUE_SUMMARY,
                due=len(self._items),
                eligible=session.eligible_objective_count,
                unsupported=len(session.unsupported_keys),
            )
        )
        self._session_status.setText("\n\n".join(status_parts))
        if not session.can_start:
            unavailable = QLabel(
                adaptive_review_text(self._locale, AdaptiveReviewCopyKey.NO_ELIGIBLE)
            )
            unavailable.setObjectName("adaptiveReviewUnavailable")
            unavailable.setWordWrap(True)
            self._session_layout.addWidget(unavailable)

    @Slot()
    def start_adaptive_session(self) -> None:
        """Start a new session or resume the validated saved activity."""

        session = self._pending_session
        if session is None or not session.can_start:
            return
        self._clear_layout(self._session_layout)
        recorder = LearningProgressService(self._store) if self._store is not None else None
        self._session_widget = AdaptiveReviewSessionWidget(
            session,
            locale=self._locale,
            progress_recorder=recorder,
            restored_snapshot=self._resume_snapshot,
            snapshot_saver=(
                self._session_state_store.save
                if self._session_state_store is not None
                else None
            ),
            snapshot_discarder=(
                self._session_state_store.discard
                if self._session_state_store is not None
                else None
            ),
        )
        self._session_widget.queue_refresh_requested.connect(self.refresh)
        self._session_layout.addWidget(self._session_widget)
        self._session_start_button.setEnabled(False)
        self._session_start_button.setText(
            adaptive_review_text(self._locale, AdaptiveReviewCopyKey.RESTART)
        )
        self._discard_button = None

    @Slot()
    def discard_saved_session(self) -> None:
        """Discard only transient session state, then prepare a fresh session."""

        if self._session_state_store is not None:
            self._session_state_store.discard()
        self._resume_snapshot = None
        self._session_widget = None
        super().refresh()

    @Slot()
    def persist_active_session(self) -> None:
        """Synchronously flush the current code draft before page destruction."""

        widget = self._session_widget
        if widget is not None:
            widget.persist_active_session()


ReviewPage = ResumableReviewPage

__all__ = ["ResumableReviewPage", "ReviewPage"]
