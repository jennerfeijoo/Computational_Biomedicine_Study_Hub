from __future__ import annotations

import sqlite3
from datetime import UTC, datetime

import pytest

from computational_biomedicine_study_hub.learning.progress import ConfidenceLevel
from computational_biomedicine_study_hub.learning.progress_service import (
    LearningProgressService,
    ObjectiveAnswerSubmission,
)
from computational_biomedicine_study_hub.storage import SQLiteProgressStore


def _submission(*, objective_ids: tuple[str, ...] = ("m01.o4", "m01.o6")) -> ObjectiveAnswerSubmission:
    return ObjectiveAnswerSubmission(
        course_code="DM847",
        module_id="dm847.m01",
        item_id="dm847.m01.bank.015",
        activity_type="true_false",
        answer="false",
        is_correct=True,
        confidence=ConfidenceLevel.HIGH,
        response_time_ms=3200,
        objective_ids=objective_ids,
        attempted_at=datetime(2026, 7, 30, 18, 0, tzinfo=UTC),
    )


def test_service_expands_one_answer_into_explicit_objective_attempts() -> None:
    generated_ids = iter(("attempt-a", "attempt-b"))
    with SQLiteProgressStore(":memory:") as store:
        service = LearningProgressService(store, attempt_id_factory=lambda: next(generated_ids))

        states = service.record_objective_answer(_submission())
        attempts = store.list_attempts()

    assert tuple(state.objective_id for state in states) == ("m01.o4", "m01.o6")
    assert tuple(attempt.attempt_id for attempt in attempts) == ("attempt-a", "attempt-b")
    assert {attempt.objective_id for attempt in attempts} == {"m01.o4", "m01.o6"}
    assert all(attempt.item_id == "dm847.m01.bank.015" for attempt in attempts)
    assert all(attempt.confidence is ConfidenceLevel.HIGH for attempt in attempts)
    assert all(attempt.hints_used == 0 for attempt in attempts)
    assert all(not attempt.solution_revealed for attempt in attempts)


def test_multi_objective_submission_rolls_back_as_one_transaction() -> None:
    generated_ids = iter(("duplicate", "duplicate"))
    with SQLiteProgressStore(":memory:") as store:
        service = LearningProgressService(store, attempt_id_factory=lambda: next(generated_ids))

        with pytest.raises(ValueError, match="duplicate attempt IDs"):
            service.record_objective_answer(_submission())

        assert store.list_attempts() == ()
        assert store.get_mastery("m01.o4") is None
        assert store.get_mastery("m01.o6") is None


def test_database_error_during_batch_rolls_back_previous_objective() -> None:
    with SQLiteProgressStore(":memory:") as store:
        service = LearningProgressService(store, attempt_id_factory=lambda: "same-id")
        first = _submission(objective_ids=("m01.o4",))
        service.record_objective_answer(first)

        second = ObjectiveAnswerSubmission(
            course_code=first.course_code,
            module_id=first.module_id,
            item_id="dm847.m01.bank.020",
            activity_type=first.activity_type,
            answer=first.answer,
            is_correct=False,
            confidence=ConfidenceLevel.LOW,
            response_time_ms=first.response_time_ms,
            objective_ids=("m01.o6",),
            attempted_at=first.attempted_at,
        )
        with pytest.raises(sqlite3.IntegrityError):
            service.record_objective_answer(second)

        assert len(store.list_attempts()) == 1
        assert store.get_mastery("m01.o6") is None


def test_submission_rejects_missing_or_duplicate_objectives() -> None:
    with pytest.raises(ValueError, match="at least one objective"):
        _submission(objective_ids=())

    with pytest.raises(ValueError, match="duplicate objective IDs"):
        _submission(objective_ids=("m01.o4", "m01.o4"))
