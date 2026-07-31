"""Application service connecting graded activities to persistent learning evidence."""

from __future__ import annotations

from collections.abc import Callable
from dataclasses import dataclass
from datetime import datetime
from typing import Protocol
from uuid import uuid4

from ..storage.sqlite_progress_store import SQLiteProgressStore
from .progress import AttemptRecord, ConfidenceLevel, ErrorRecord, MasteryState


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
    hints_used: int = 0
    solution_revealed: bool = False
    prompt: str = ""
    selected_answer: str = ""
    correct_answer: str = ""
    explanation: str = ""

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
        if self.hints_used < 0:
            raise ValueError("hints_used cannot be negative.")
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

        context = {
            "prompt": self.prompt,
            "selected_answer": self.selected_answer,
            "correct_answer": self.correct_answer,
            "explanation": self.explanation,
        }
        supplied = tuple(bool(value) for value in context.values())
        if any(supplied) and not all(supplied):
            raise ValueError("Authored error context must be supplied completely or omitted.")
        for field_name, value in context.items():
            if value and value != value.strip():
                raise ValueError(
                    f"Submission field {field_name!r} cannot contain surrounding whitespace."
                )

    @property
    def has_error_context(self) -> bool:
        """Return whether authored prompt, answers and explanation are available."""

        return bool(self.prompt)


class ObjectiveAttemptRecorder(Protocol):
    """Minimal interface required by objective-assessment widgets."""

    def record_objective_answer(
        self,
        submission: ObjectiveAnswerSubmission,
    ) -> tuple[MasteryState, ...]:
        """Persist one answer as evidence for all explicitly linked objectives."""


class LearningProgressService:
    """Expand one activity interaction into atomic objective-level evidence."""

    def __init__(
        self,
        store: SQLiteProgressStore,
        *,
        attempt_id_factory: Callable[[], str] | None = None,
        error_id_factory: Callable[[], str] | None = None,
    ) -> None:
        self._store = store
        self._attempt_id_factory = attempt_id_factory or (lambda: uuid4().hex)
        self._error_id_factory = error_id_factory or (lambda: uuid4().hex)

    @property
    def store(self) -> SQLiteProgressStore:
        """Return the local store used by this service."""

        return self._store

    def record_objective_answer(
        self,
        submission: ObjectiveAnswerSubmission,
    ) -> tuple[MasteryState, ...]:
        """Persist objective evidence and maintain the authored error notebook."""

        attempts = tuple(
            AttemptRecord(
                attempt_id=self._new_identifier(self._attempt_id_factory, "Attempt"),
                course_code=submission.course_code,
                module_id=submission.module_id,
                objective_id=objective_id,
                item_id=submission.item_id,
                activity_type=submission.activity_type,
                answer=submission.answer,
                is_correct=submission.is_correct,
                confidence=submission.confidence,
                hints_used=submission.hints_used,
                response_time_ms=submission.response_time_ms,
                solution_revealed=submission.solution_revealed,
                attempted_at=submission.attempted_at,
            )
            for objective_id in submission.objective_ids
        )

        error: ErrorRecord | None = None
        if not submission.is_correct and submission.has_error_context:
            error = ErrorRecord(
                error_id=self._new_identifier(self._error_id_factory, "Error"),
                course_code=submission.course_code,
                module_id=submission.module_id,
                item_id=submission.item_id,
                prompt=submission.prompt,
                selected_answer=submission.selected_answer,
                correct_answer=submission.correct_answer,
                explanation=submission.explanation,
                confidence=submission.confidence,
                objective_ids=submission.objective_ids,
                occurred_at=submission.attempted_at,
            )

        return self._store.record_learning_interaction(
            attempts,
            error=error,
            resolve_item_errors=submission.is_correct,
        )

    @staticmethod
    def _new_identifier(factory: Callable[[], str], label: str) -> str:
        identifier = factory()
        if not identifier.strip():
            raise ValueError(f"{label} ID factories must return a non-empty identifier.")
        if identifier != identifier.strip():
            raise ValueError(
                f"Generated {label.casefold()} IDs cannot contain surrounding whitespace."
            )
        return identifier


__all__ = [
    "LearningProgressService",
    "ObjectiveAnswerSubmission",
    "ObjectiveAttemptRecorder",
]
