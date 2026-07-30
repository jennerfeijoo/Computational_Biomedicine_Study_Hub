"""Application service connecting graded activities to persistent learning evidence."""

from __future__ import annotations

from collections.abc import Callable
from dataclasses import dataclass
from datetime import datetime
from typing import Protocol
from uuid import uuid4

from ..storage.sqlite_progress_store import SQLiteProgressStore
from .progress import AttemptRecord, ConfidenceLevel, MasteryState


@dataclass(frozen=True, slots=True)
class ObjectiveAnswerSubmission:
    """One graded objective-answer interaction before expansion by objective."""

    course_code: str
    module_id: str
    item_id: str
    activity_type: str
    answer: str
    is_correct: bool
    confidence: ConfidenceLevel
    response_time_ms: int
    objective_ids: tuple[str, ...]
    attempted_at: datetime

    def __post_init__(self) -> None:
        required = {
            "course_code": self.course_code,
            "module_id": self.module_id,
            "item_id": self.item_id,
            "activity_type": self.activity_type,
            "answer": self.answer,
        }
        for field_name, value in required.items():
            if not value.strip():
                raise ValueError(f"Submission field {field_name!r} cannot be empty.")
            if value != value.strip():
                raise ValueError(
                    f"Submission field {field_name!r} cannot contain surrounding whitespace."
                )

        if self.response_time_ms < 0:
            raise ValueError("response_time_ms cannot be negative.")
        if self.attempted_at.tzinfo is None or self.attempted_at.utcoffset() is None:
            raise ValueError("attempted_at must be timezone-aware.")
        if not self.objective_ids:
            raise ValueError("Objective submissions require at least one objective ID.")

        normalized = tuple(objective_id.strip().casefold() for objective_id in self.objective_ids)
        if any(not objective_id for objective_id in normalized):
            raise ValueError("Objective submissions cannot contain empty objective IDs.")
        if any(objective_id != objective_id.strip() for objective_id in self.objective_ids):
            raise ValueError("Objective IDs cannot contain surrounding whitespace.")
        if len(normalized) != len(set(normalized)):
            raise ValueError("Objective submissions cannot contain duplicate objective IDs.")


class ObjectiveAttemptRecorder(Protocol):
    """Minimal interface required by objective-assessment widgets."""

    def record_objective_answer(
        self,
        submission: ObjectiveAnswerSubmission,
    ) -> tuple[MasteryState, ...]:
        """Persist one answer as evidence for all explicitly linked objectives."""


class LearningProgressService:
    """Expand one activity interaction into atomic objective-level attempts."""

    def __init__(
        self,
        store: SQLiteProgressStore,
        *,
        attempt_id_factory: Callable[[], str] | None = None,
    ) -> None:
        self._store = store
        self._attempt_id_factory = attempt_id_factory or (lambda: uuid4().hex)

    @property
    def store(self) -> SQLiteProgressStore:
        """Return the local store used by this service."""

        return self._store

    def record_objective_answer(
        self,
        submission: ObjectiveAnswerSubmission,
    ) -> tuple[MasteryState, ...]:
        """Persist one objective answer without inferring any objective relation."""

        attempts = tuple(
            AttemptRecord(
                attempt_id=self._new_attempt_id(),
                course_code=submission.course_code,
                module_id=submission.module_id,
                objective_id=objective_id,
                item_id=submission.item_id,
                activity_type=submission.activity_type,
                answer=submission.answer,
                is_correct=submission.is_correct,
                confidence=submission.confidence,
                hints_used=0,
                response_time_ms=submission.response_time_ms,
                solution_revealed=False,
                attempted_at=submission.attempted_at,
            )
            for objective_id in submission.objective_ids
        )
        return self._store.record_batch_and_update(attempts)

    def _new_attempt_id(self) -> str:
        attempt_id = self._attempt_id_factory()
        if not attempt_id.strip():
            raise ValueError("Attempt ID factories must return a non-empty identifier.")
        if attempt_id != attempt_id.strip():
            raise ValueError("Generated attempt IDs cannot contain surrounding whitespace.")
        return attempt_id


__all__ = [
    "LearningProgressService",
    "ObjectiveAnswerSubmission",
    "ObjectiveAttemptRecorder",
]
