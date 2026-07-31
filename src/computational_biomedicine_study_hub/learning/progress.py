"""Domain models for persistent, objective-level learning progress.

These models deliberately avoid PySide6 and database concerns. They can be used by
widgets, review scheduling, analytics and future tutor context without coupling the
learning model to a particular interface.
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from enum import StrEnum


class ConfidenceLevel(StrEnum):
    """Student-reported certainty before feedback is revealed."""

    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"


class ErrorKind(StrEnum):
    """Pedagogical interpretation of an incorrect answer and its confidence."""

    KNOWLEDGE_GAP = "knowledge_gap"
    FRAGILE_UNDERSTANDING = "fragile_understanding"
    MISCONCEPTION = "misconception"


@dataclass(frozen=True, slots=True)
class AttemptRecord:
    """One immutable interaction with an assessable learning activity."""

    attempt_id: str
    course_code: str
    module_id: str
    objective_id: str
    item_id: str
    activity_type: str
    answer: str
    is_correct: bool
    confidence: ConfidenceLevel
    hints_used: int
    response_time_ms: int
    solution_revealed: bool
    attempted_at: datetime

    def __post_init__(self) -> None:
        required_identifiers = {
            "attempt_id": self.attempt_id,
            "course_code": self.course_code,
            "module_id": self.module_id,
            "objective_id": self.objective_id,
            "item_id": self.item_id,
            "activity_type": self.activity_type,
        }
        for field_name, value in required_identifiers.items():
            if not value.strip():
                raise ValueError(f"Attempt field {field_name!r} cannot be empty.")
            if value != value.strip():
                raise ValueError(
                    f"Attempt field {field_name!r} cannot contain surrounding whitespace."
                )

        if self.hints_used < 0:
            raise ValueError("hints_used cannot be negative.")
        if self.response_time_ms < 0:
            raise ValueError("response_time_ms cannot be negative.")
        if self.attempted_at.tzinfo is None or self.attempted_at.utcoffset() is None:
            raise ValueError("attempted_at must be timezone-aware.")


@dataclass(frozen=True, slots=True)
class MasteryState:
    """Current objective-level estimate and next scheduled review."""

    objective_id: str
    mastery_score: float
    attempts: int
    consecutive_correct: int
    lapse_count: int
    last_attempt_at: datetime
    next_review_at: datetime

    def __post_init__(self) -> None:
        if not self.objective_id.strip():
            raise ValueError("objective_id cannot be empty.")
        if self.objective_id != self.objective_id.strip():
            raise ValueError("objective_id cannot contain surrounding whitespace.")
        if not 0.0 <= self.mastery_score <= 1.0:
            raise ValueError("mastery_score must be between 0 and 1.")
        if self.attempts < 1:
            raise ValueError("attempts must be at least 1.")
        if self.consecutive_correct < 0:
            raise ValueError("consecutive_correct cannot be negative.")
        if self.consecutive_correct > self.attempts:
            raise ValueError("consecutive_correct cannot exceed attempts.")
        if self.lapse_count < 0:
            raise ValueError("lapse_count cannot be negative.")
        for field_name, value in {
            "last_attempt_at": self.last_attempt_at,
            "next_review_at": self.next_review_at,
        }.items():
            if value.tzinfo is None or value.utcoffset() is None:
                raise ValueError(f"{field_name} must be timezone-aware.")
        if self.next_review_at < self.last_attempt_at:
            raise ValueError("next_review_at cannot precede last_attempt_at.")


@dataclass(frozen=True, slots=True)
class ReviewItem:
    """One course-scoped mastery state ready for review presentation."""

    course_code: str
    module_id: str
    state: MasteryState

    def __post_init__(self) -> None:
        for field_name, value in {
            "course_code": self.course_code,
            "module_id": self.module_id,
        }.items():
            if not value.strip():
                raise ValueError(f"Review field {field_name!r} cannot be empty.")
            if value != value.strip():
                raise ValueError(
                    f"Review field {field_name!r} cannot contain surrounding whitespace."
                )

    @property
    def objective_id(self) -> str:
        """Return the objective identity held by the mastery state."""

        return self.state.objective_id

    @property
    def key(self) -> tuple[str, str, str]:
        """Return the collision-safe persisted identity."""

        return self.course_code, self.module_id, self.objective_id


@dataclass(frozen=True, slots=True)
class ErrorRecord:
    """One authored incorrect answer retained for deliberate error review."""

    error_id: str
    course_code: str
    module_id: str
    item_id: str
    prompt: str
    selected_answer: str
    correct_answer: str
    explanation: str
    confidence: ConfidenceLevel
    objective_ids: tuple[str, ...]
    occurred_at: datetime
    resolved_at: datetime | None = None

    def __post_init__(self) -> None:
        required = {
            "error_id": self.error_id,
            "course_code": self.course_code,
            "module_id": self.module_id,
            "item_id": self.item_id,
            "prompt": self.prompt,
            "selected_answer": self.selected_answer,
            "correct_answer": self.correct_answer,
            "explanation": self.explanation,
        }
        for field_name, value in required.items():
            if not value.strip():
                raise ValueError(f"Error field {field_name!r} cannot be empty.")
            if value != value.strip():
                raise ValueError(
                    f"Error field {field_name!r} cannot contain surrounding whitespace."
                )

        if not self.objective_ids:
            raise ValueError("Error records require at least one objective ID.")
        normalized = tuple(objective_id.strip().casefold() for objective_id in self.objective_ids)
        if any(not objective_id for objective_id in normalized):
            raise ValueError("Error records cannot contain empty objective IDs.")
        if any(objective_id != objective_id.strip() for objective_id in self.objective_ids):
            raise ValueError("Error objective IDs cannot contain surrounding whitespace.")
        if len(normalized) != len(set(normalized)):
            raise ValueError("Error records cannot contain duplicate objective IDs.")

        if self.occurred_at.tzinfo is None or self.occurred_at.utcoffset() is None:
            raise ValueError("occurred_at must be timezone-aware.")
        if self.resolved_at is not None:
            if self.resolved_at.tzinfo is None or self.resolved_at.utcoffset() is None:
                raise ValueError("resolved_at must be timezone-aware.")
            if self.resolved_at < self.occurred_at:
                raise ValueError("resolved_at cannot precede occurred_at.")

    @property
    def kind(self) -> ErrorKind:
        """Classify the error from the learner's pre-feedback confidence."""

        if self.confidence is ConfidenceLevel.HIGH:
            return ErrorKind.MISCONCEPTION
        if self.confidence is ConfidenceLevel.MEDIUM:
            return ErrorKind.FRAGILE_UNDERSTANDING
        return ErrorKind.KNOWLEDGE_GAP

    @property
    def is_resolved(self) -> bool:
        """Return whether a later correct answer resolved this item."""

        return self.resolved_at is not None


__all__ = [
    "AttemptRecord",
    "ConfidenceLevel",
    "ErrorKind",
    "ErrorRecord",
    "MasteryState",
    "ReviewItem",
]
