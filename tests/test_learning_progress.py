from __future__ import annotations

import sqlite3
from datetime import UTC, datetime, timedelta
from pathlib import Path

import pytest

from computational_biomedicine_study_hub.learning.progress import (
    AttemptRecord,
    ConfidenceLevel,
)
from computational_biomedicine_study_hub.learning.review_scheduler import (
    evidence_score,
    update_mastery,
)
from computational_biomedicine_study_hub.storage import SQLiteProgressStore

_NOW = datetime(2026, 7, 30, 12, 0, tzinfo=UTC)


def _attempt(
    attempt_id: str,
    *,
    objective_id: str = "dm847.m01.objective.01",
    is_correct: bool = True,
    confidence: ConfidenceLevel = ConfidenceLevel.HIGH,
    hints_used: int = 0,
    solution_revealed: bool = False,
    attempted_at: datetime = _NOW,
) -> AttemptRecord:
    return AttemptRecord(
        attempt_id=attempt_id,
        course_code="DM847",
        module_id="dm847.m01",
        objective_id=objective_id,
        item_id="dm847.m01.question.01",
        activity_type="multiple_choice",
        answer="option_b",
        is_correct=is_correct,
        confidence=confidence,
        hints_used=hints_used,
        response_time_ms=18_500,
        solution_revealed=solution_revealed,
        attempted_at=attempted_at,
    )


def test_attempt_requires_timezone_aware_timestamp() -> None:
    with pytest.raises(ValueError, match="timezone-aware"):
        _attempt("attempt-naive", attempted_at=datetime(2026, 7, 30, 12, 0))


def test_mastery_rewards_independent_high_confidence_recall() -> None:
    attempt = _attempt("attempt-1")

    state = update_mastery(None, attempt)

    assert evidence_score(attempt) == 1.0
    assert state.mastery_score == 0.6425
    assert state.attempts == 1
    assert state.consecutive_correct == 1
    assert state.lapse_count == 0
    assert state.next_review_at == _NOW + timedelta(days=7)


def test_hints_and_solution_reduce_evidence_and_review_interval() -> None:
    hinted = _attempt(
        "attempt-hinted",
        confidence=ConfidenceLevel.MEDIUM,
        hints_used=2,
    )
    revealed = _attempt(
        "attempt-revealed",
        hints_used=1,
        solution_revealed=True,
    )

    hinted_state = update_mastery(None, hinted)
    revealed_state = update_mastery(None, revealed)

    assert evidence_score(hinted) == pytest.approx(0.77)
    assert hinted_state.next_review_at == _NOW + timedelta(days=2)
    assert evidence_score(revealed) == 0.35
    assert revealed_state.next_review_at == _NOW + timedelta(days=1)


def test_incorrect_high_confidence_attempt_resets_streak_and_records_lapse() -> None:
    first = update_mastery(None, _attempt("attempt-correct"))
    second_attempt = _attempt(
        "attempt-wrong",
        is_correct=False,
        attempted_at=_NOW + timedelta(days=1),
    )

    second = update_mastery(first, second_attempt)

    assert second.mastery_score < first.mastery_score
    assert second.attempts == 2
    assert second.consecutive_correct == 0
    assert second.lapse_count == 1
    assert second.next_review_at == second_attempt.attempted_at + timedelta(days=1)


def test_sqlite_store_round_trips_attempt_and_mastery(tmp_path: Path) -> None:
    database = tmp_path / "progress.sqlite3"
    attempt = _attempt("attempt-persisted")

    with SQLiteProgressStore(database) as store:
        saved_state = store.record_and_update(attempt)

    with SQLiteProgressStore(database) as reopened:
        assert reopened.get_attempt(attempt.attempt_id) == attempt
        assert reopened.get_mastery(attempt.objective_id) == saved_state
        assert reopened.list_attempts(objective_id=attempt.objective_id) == (attempt,)


def test_attempt_and_mastery_update_are_atomic() -> None:
    attempt = _attempt("attempt-unique")

    with SQLiteProgressStore(":memory:") as store:
        first_state = store.record_and_update(attempt)
        with pytest.raises(sqlite3.IntegrityError):
            store.record_and_update(attempt)

        assert store.list_attempts() == (attempt,)
        assert store.get_mastery(attempt.objective_id) == first_state


def test_due_mastery_is_ordered_by_due_time_then_weakness() -> None:
    early_objective = "dm847.m01.objective.early"
    weak_objective = "dm847.m01.objective.weak"
    strong_objective = "dm847.m01.objective.strong"

    with SQLiteProgressStore(":memory:") as store:
        store.record_and_update(
            _attempt(
                "attempt-early",
                objective_id=early_objective,
                is_correct=False,
                attempted_at=_NOW - timedelta(days=3),
            )
        )
        store.record_and_update(
            _attempt(
                "attempt-weak",
                objective_id=weak_objective,
                is_correct=False,
                attempted_at=_NOW - timedelta(days=1),
            )
        )
        store.record_and_update(
            _attempt(
                "attempt-strong",
                objective_id=strong_objective,
                confidence=ConfidenceLevel.LOW,
                attempted_at=_NOW - timedelta(days=2),
            )
        )

        due = store.due_mastery(_NOW, limit=3)

    assert tuple(state.objective_id for state in due) == (
        early_objective,
        weak_objective,
        strong_objective,
    )
