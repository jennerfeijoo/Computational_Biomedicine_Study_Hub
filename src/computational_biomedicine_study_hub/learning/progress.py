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


__all__ = ["AttemptRecord", "ConfidenceLevel", "MasteryState"]
