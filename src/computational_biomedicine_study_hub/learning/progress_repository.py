"""Persistence boundary for learning progress."""

from __future__ import annotations

from datetime import datetime
from typing import Protocol

from .progress import (
    AssessmentSession,
    AttemptRecord,
    FlashcardProgress,
    ModuleProgress,
    OpenResponseAttempt,
    OpenResponseDraft,
    PracticeProgress,
    ReviewSchedule,
)


class ProgressRepository(Protocol):
    """Storage contract consumed by learning services and UI coordinators."""

    def initialize(self) -> None:
        """Create or migrate persistent storage safely."""

    def record_attempt(self, attempt: AttemptRecord) -> None:
        """Append one immutable attempt."""

    def list_attempts(
        self,
        *,
        course_code: str | None = None,
        module_id: str | None = None,
        item_id: str | None = None,
        session_id: str | None = None,
        limit: int | None = None,
    ) -> tuple[AttemptRecord, ...]:
        """Return newest attempts matching language-independent identifiers."""

    def save_practice_progress(self, progress: PracticeProgress) -> None:
        """Insert or replace the latest exercise state."""

    def get_practice_progress(
        self,
        course_code: str,
        module_id: str,
        exercise_id: str,
    ) -> PracticeProgress | None:
        """Return the latest exercise state, if any."""

    def save_assessment_session(self, session: AssessmentSession) -> None:
        """Insert or update one stable assessment session."""

    def get_assessment_session(self, session_id: str) -> AssessmentSession | None:
        """Return one session by its stable ID."""

    def latest_open_assessment_session(
        self,
        *,
        course_code: str,
        module_id: str,
        scope: str | None = None,
    ) -> AssessmentSession | None:
        """Return the latest unfinished session for a module."""

    def save_open_response_draft(self, draft: OpenResponseDraft) -> None:
        """Persist the latest draft without treating it as a submitted attempt."""

    def get_open_response_draft(
        self,
        course_code: str,
        module_id: str,
        item_id: str,
        locale: str,
    ) -> OpenResponseDraft | None:
        """Return the latest local draft for an authored open-response item."""

    def record_open_response_attempt(self, attempt: OpenResponseAttempt) -> None:
        """Append one versioned open response and its optional local feedback."""

    def list_open_response_attempts(
        self,
        *,
        course_code: str | None = None,
        module_id: str | None = None,
        item_id: str | None = None,
    ) -> tuple[OpenResponseAttempt, ...]:
        """Return open responses in version order for comparison."""

    def save_flashcard_progress(self, progress: FlashcardProgress) -> None:
        """Insert or update scheduling state for one card."""

    def get_flashcard_progress(
        self,
        course_code: str,
        module_id: str,
        card_id: str,
    ) -> FlashcardProgress | None:
        """Return one card's scheduling state."""

    def list_flashcard_progress(
        self,
        *,
        course_code: str | None = None,
        module_id: str | None = None,
    ) -> tuple[FlashcardProgress, ...]:
        """Return persisted card schedules in stable identifier order."""

    def save_review_schedule(self, schedule: ReviewSchedule) -> None:
        """Insert or update one review schedule."""

    def get_review_schedule(
        self,
        course_code: str,
        module_id: str,
        item_id: str,
        item_kind: str,
    ) -> ReviewSchedule | None:
        """Return one schedule by its stable composite identity."""

    def list_due_reviews(
        self,
        *,
        due_at: datetime,
        course_code: str | None = None,
        module_id: str | None = None,
        limit: int | None = None,
    ) -> tuple[ReviewSchedule, ...]:
        """Return due items in deterministic due-date order."""

    def module_progress(self, course_code: str, module_id: str) -> ModuleProgress:
        """Aggregate attempts and pending reviews for one module."""

    def set_bookmark(
        self,
        *,
        item_id: str,
        item_kind: str,
        course_code: str,
        module_id: str,
        bookmarked: bool,
    ) -> None:
        """Create or remove a bookmark keyed only by stable identities."""

    def is_bookmarked(self, *, item_id: str, item_kind: str) -> bool:
        """Return whether one stable item identity is bookmarked."""


__all__ = ["ProgressRepository"]
