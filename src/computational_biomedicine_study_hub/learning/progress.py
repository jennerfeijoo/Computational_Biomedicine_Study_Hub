"""Language-independent learning progress domain models.

The models in this module deliberately know nothing about SQLite or PySide6. Stable
academic identifiers are the persistence keys; localized text is only optional attempt
metadata and is never used to decide correctness.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import UTC, datetime
from enum import StrEnum

from .activity_types import ActivityType


def utc_now() -> datetime:
    """Return an aware UTC timestamp suitable for persisted learning records."""
    return datetime.now(UTC)


def require_aware(value: datetime, field_name: str) -> None:
    """Reject ambiguous local timestamps at the domain boundary."""
    if value.tzinfo is None or value.utcoffset() is None:
        raise ValueError(f"{field_name} must include timezone information.")


def require_identifier(value: str, field_name: str, *, allow_empty: bool = False) -> None:
    """Validate one stable identifier without imposing a course-specific syntax."""
    if allow_empty and not value:
        return
    if not value.strip():
        raise ValueError(f"{field_name} cannot be empty.")
    if value != value.strip():
        raise ValueError(f"{field_name} cannot contain surrounding whitespace.")


class MasteryState(StrEnum):
    """Coarse, explainable mastery state derived from persisted evidence."""

    NEW = "new"
    LEARNING = "learning"
    REVIEWING = "reviewing"
    MASTERED = "mastered"


class AttemptOutcome(StrEnum):
    """Learner-facing outcome, including honest open-response self-assessment."""

    SOLVED = "solved"
    PARTIAL = "partial"
    REVIEW = "review"


class LearningItemKind(StrEnum):
    """Kind of stable content identifier referenced by an attempt or review."""

    PRACTICE = "practice"
    ASSESSMENT = "assessment"
    FLASHCARD = "flashcard"
    CONCEPT = "concept"


class AssessmentScope(StrEnum):
    """Supported assessment session scopes."""

    QUICK_MODULE = "quick_module"
    COMPLETE_MODULE = "complete_module"
    COURSE = "course"
    MIXED = "mixed"
    OBJECTIVE_MODULE = "objective_module"
    PRACTICE_MODULE = "practice_module"


@dataclass(frozen=True, slots=True)
class AttemptRecord:
    """One immutable answer or self-assessment event."""

    attempt_id: str
    course_code: str
    module_id: str
    item_id: str
    item_kind: LearningItemKind
    activity_type: ActivityType
    outcome: AttemptOutcome
    locale: str
    content_version: str
    created_at: datetime = field(default_factory=utc_now)
    response_text: str = ""
    selected_option_ids: tuple[str, ...] = ()
    is_correct: bool | None = None
    score: float | None = None
    session_id: str = ""

    def __post_init__(self) -> None:
        for field_name in ("attempt_id", "course_code", "module_id", "item_id"):
            require_identifier(str(getattr(self, field_name)), field_name)
        require_identifier(self.session_id, "session_id", allow_empty=True)
        require_aware(self.created_at, "created_at")
        if self.score is not None and not 0.0 <= self.score <= 1.0:
            raise ValueError("score must be between 0 and 1.")
        for option_id in self.selected_option_ids:
            require_identifier(option_id, "selected option ID")


@dataclass(frozen=True, slots=True)
class PracticeProgress:
    """Latest persisted state for one authored practice exercise."""

    course_code: str
    module_id: str
    exercise_id: str
    mastery_state: MasteryState
    attempt_count: int
    last_outcome: AttemptOutcome
    updated_at: datetime
    response_text: str = ""
    selected_option_ids: tuple[str, ...] = ()

    def __post_init__(self) -> None:
        for field_name in ("course_code", "module_id", "exercise_id"):
            require_identifier(str(getattr(self, field_name)), field_name)
        if self.attempt_count < 1:
            raise ValueError("attempt_count must be positive.")
        require_aware(self.updated_at, "updated_at")


@dataclass(frozen=True, slots=True)
class AssessmentSession:
    """Persisted assessment composition and completion state."""

    session_id: str
    scope: AssessmentScope
    course_code: str
    module_id: str
    item_ids: tuple[str, ...]
    seed: int
    locale: str
    started_at: datetime
    answered_item_ids: tuple[str, ...] = ()
    correct_count: int = 0
    completed_at: datetime | None = None

    def __post_init__(self) -> None:
        for field_name in ("session_id", "course_code"):
            require_identifier(str(getattr(self, field_name)), field_name)
        require_identifier(self.module_id, "module_id", allow_empty=True)
        if not self.item_ids:
            raise ValueError("Assessment sessions require at least one item.")
        if len(self.item_ids) != len(set(self.item_ids)):
            raise ValueError("Assessment session item IDs must be unique.")
        if len(self.answered_item_ids) != len(set(self.answered_item_ids)):
            raise ValueError("Answered item IDs must be unique.")
        if not set(self.answered_item_ids).issubset(self.item_ids):
            raise ValueError("Answered item IDs must belong to the session.")
        if not 0 <= self.correct_count <= len(self.answered_item_ids):
            raise ValueError("correct_count is inconsistent with answered items.")
        require_aware(self.started_at, "started_at")
        if self.completed_at is not None:
            require_aware(self.completed_at, "completed_at")
            if self.completed_at < self.started_at:
                raise ValueError("completed_at cannot precede started_at.")

    @property
    def is_complete(self) -> bool:
        """Return whether the session has an explicit completion timestamp."""
        return self.completed_at is not None


@dataclass(frozen=True, slots=True)
class ModuleProgress:
    """Read model summarizing persisted activity for one module."""

    course_code: str
    module_id: str
    mastery_state: MasteryState
    attempt_count: int
    correct_count: int
    pending_review_count: int
    last_activity_at: datetime | None

    def __post_init__(self) -> None:
        require_identifier(self.course_code, "course_code")
        require_identifier(self.module_id, "module_id")
        if min(self.attempt_count, self.correct_count, self.pending_review_count) < 0:
            raise ValueError("Module progress counts cannot be negative.")
        if self.correct_count > self.attempt_count:
            raise ValueError("correct_count cannot exceed attempt_count.")
        if self.last_activity_at is not None:
            require_aware(self.last_activity_at, "last_activity_at")

    @property
    def success_ratio(self) -> float:
        """Return an evidence ratio without inventing success for an empty module."""
        if not self.attempt_count:
            return 0.0
        return self.correct_count / self.attempt_count


@dataclass(frozen=True, slots=True)
class OpenResponseDraft:
    """Latest local draft for one language-independent open-response item."""

    course_code: str
    module_id: str
    item_id: str
    locale: str
    response_text: str
    updated_at: datetime

    def __post_init__(self) -> None:
        for field_name in ("course_code", "module_id", "item_id", "locale"):
            require_identifier(str(getattr(self, field_name)), field_name)
        require_aware(self.updated_at, "updated_at")


@dataclass(frozen=True, slots=True)
class OpenResponseAttempt:
    """Versioned learner response and optional local formative feedback."""

    attempt_id: str
    item_id: str
    course_code: str
    module_id: str
    locale: str
    confidence: str
    response_text: str
    created_at: datetime
    feedback_json: str | None = None
    version: int = 1
    helpful: bool | None = None

    def __post_init__(self) -> None:
        for field_name in (
            "attempt_id",
            "item_id",
            "course_code",
            "module_id",
            "locale",
        ):
            require_identifier(str(getattr(self, field_name)), field_name)
        if self.confidence not in {"low", "medium", "high"}:
            raise ValueError("confidence must be low, medium, or high.")
        if self.version < 1:
            raise ValueError("version must be positive.")
        require_aware(self.created_at, "created_at")


@dataclass(frozen=True, slots=True)
class FlashcardProgress:
    """Scheduling state for one generated or authored flashcard."""

    course_code: str
    module_id: str
    card_id: str
    mastery_state: MasteryState
    repetitions: int
    interval_days: int
    easiness: float
    due_at: datetime
    last_reviewed_at: datetime | None = None
    first_seen_at: datetime | None = None
    lapse_count: int = 0
    last_rating: str = ""
    total_reviews: int = 0
    bookmarked: bool = False

    def __post_init__(self) -> None:
        for field_name in ("course_code", "module_id", "card_id"):
            require_identifier(str(getattr(self, field_name)), field_name)
        if (
            self.repetitions < 0
            or self.interval_days < 0
            or self.lapse_count < 0
            or self.total_reviews < 0
        ):
            raise ValueError("Flashcard repetitions and interval cannot be negative.")
        if not 1.3 <= self.easiness <= 3.0:
            raise ValueError("Flashcard easiness must be between 1.3 and 3.0.")
        require_aware(self.due_at, "due_at")
        if self.last_reviewed_at is not None:
            require_aware(self.last_reviewed_at, "last_reviewed_at")
        if self.first_seen_at is not None:
            require_aware(self.first_seen_at, "first_seen_at")


@dataclass(frozen=True, slots=True)
class ReviewSchedule:
    """Independent spaced-review schedule for any stable learning item."""

    course_code: str
    module_id: str
    item_id: str
    item_kind: LearningItemKind
    mastery_state: MasteryState
    repetitions: int
    interval_days: int
    easiness: float
    due_at: datetime
    last_reviewed_at: datetime | None = None

    def __post_init__(self) -> None:
        for field_name in ("course_code", "module_id", "item_id"):
            require_identifier(str(getattr(self, field_name)), field_name)
        if self.repetitions < 0 or self.interval_days < 0:
            raise ValueError("Review repetitions and interval cannot be negative.")
        if not 1.3 <= self.easiness <= 3.0:
            raise ValueError("Review easiness must be between 1.3 and 3.0.")
        require_aware(self.due_at, "due_at")
        if self.last_reviewed_at is not None:
            require_aware(self.last_reviewed_at, "last_reviewed_at")


__all__ = [
    "AssessmentScope",
    "AssessmentSession",
    "AttemptOutcome",
    "AttemptRecord",
    "FlashcardProgress",
    "LearningItemKind",
    "MasteryState",
    "ModuleProgress",
    "OpenResponseAttempt",
    "OpenResponseDraft",
    "PracticeProgress",
    "ReviewSchedule",
    "require_aware",
    "utc_now",
]
