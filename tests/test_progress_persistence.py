from __future__ import annotations

import sqlite3
from dataclasses import replace
from datetime import UTC, datetime, timedelta
from pathlib import Path

import pytest

from computational_biomedicine_study_hub.learning.activity_types import ActivityType
from computational_biomedicine_study_hub.learning.progress import (
    AssessmentScope,
    AssessmentSession,
    AttemptOutcome,
    AttemptRecord,
    FlashcardProgress,
    LearningItemKind,
    MasteryState,
    PracticeProgress,
    ReviewSchedule,
)
from computational_biomedicine_study_hub.persistence import (
    SCHEMA_VERSION,
    SQLiteProgressRepository,
)

NOW = datetime(2026, 7, 19, 10, 30, tzinfo=UTC)


def _attempt(*, attempt_id: str = "attempt-1", locale: str = "es-ES") -> AttemptRecord:
    return AttemptRecord(
        attempt_id=attempt_id,
        course_code="DM857",
        module_id="dm857.m01",
        item_id="dm857.m01.objective.001",
        item_kind=LearningItemKind.ASSESSMENT,
        activity_type=ActivityType.MULTIPLE_CHOICE,
        outcome=AttemptOutcome.SOLVED,
        locale=locale,
        content_version="2026.1",
        created_at=NOW,
        response_text="texto visible que puede cambiar",
        selected_option_ids=("correct-option",),
        is_correct=True,
        score=1.0,
        session_id="session-1",
    )


def test_schema_initialization_is_idempotent_and_versioned(tmp_path: Path) -> None:
    repository = SQLiteProgressRepository(tmp_path / "progress.sqlite3")

    repository.initialize()
    repository.initialize()

    assert repository.schema_version() == SCHEMA_VERSION
    with sqlite3.connect(repository.database_path) as connection:
        tables = {
            str(row[0])
            for row in connection.execute(
                "SELECT name FROM sqlite_master WHERE type = 'table'"
            ).fetchall()
        }
    assert {
        "attempts",
        "practice_progress",
        "assessment_sessions",
        "flashcard_progress",
        "review_schedule",
    }.issubset(tables)


def test_newer_database_schema_is_rejected(tmp_path: Path) -> None:
    database_path = tmp_path / "future.sqlite3"
    with sqlite3.connect(database_path) as connection:
        connection.execute("PRAGMA user_version = 999")

    with pytest.raises(RuntimeError, match="newer than supported"):
        SQLiteProgressRepository(database_path).initialize()


def test_attempts_survive_repository_restart_and_keep_option_ids(tmp_path: Path) -> None:
    database_path = tmp_path / "progress.sqlite3"
    first_process = SQLiteProgressRepository(database_path)
    first_process.record_attempt(_attempt())

    second_process = SQLiteProgressRepository(database_path)
    attempts = second_process.list_attempts(
        course_code="DM857",
        module_id="dm857.m01",
    )

    assert attempts == (_attempt(),)
    assert attempts[0].selected_option_ids == ("correct-option",)
    assert attempts[0].response_text == "texto visible que puede cambiar"


def test_attempt_identity_is_preserved_when_locale_changes(tmp_path: Path) -> None:
    repository = SQLiteProgressRepository(tmp_path / "progress.sqlite3")
    repository.record_attempt(_attempt(attempt_id="attempt-es", locale="es-ES"))
    repository.record_attempt(_attempt(attempt_id="attempt-en", locale="en"))

    attempts = repository.list_attempts(item_id="dm857.m01.objective.001")

    assert {attempt.locale for attempt in attempts} == {"es-ES", "en"}
    assert {attempt.item_id for attempt in attempts} == {"dm857.m01.objective.001"}
    assert {attempt.selected_option_ids for attempt in attempts} == {("correct-option",)}


def test_practice_progress_is_upserted_without_changing_stable_key(tmp_path: Path) -> None:
    repository = SQLiteProgressRepository(tmp_path / "progress.sqlite3")
    initial = PracticeProgress(
        course_code="DM857",
        module_id="dm857.m01",
        exercise_id="m01.p01",
        mastery_state=MasteryState.LEARNING,
        attempt_count=1,
        last_outcome=AttemptOutcome.PARTIAL,
        updated_at=NOW,
        response_text="first",
    )
    repository.save_practice_progress(initial)
    repository.save_practice_progress(
        replace(
            initial,
            mastery_state=MasteryState.REVIEWING,
            attempt_count=2,
            last_outcome=AttemptOutcome.SOLVED,
            updated_at=NOW + timedelta(minutes=5),
            response_text="second",
        )
    )

    restored = repository.get_practice_progress("DM857", "dm857.m01", "m01.p01")

    assert restored is not None
    assert restored.attempt_count == 2
    assert restored.response_text == "second"
    assert restored.mastery_state is MasteryState.REVIEWING


def test_assessment_session_survives_restart_and_restores_composition(tmp_path: Path) -> None:
    database_path = tmp_path / "progress.sqlite3"
    session = AssessmentSession(
        session_id="session-1",
        scope=AssessmentScope.QUICK_MODULE,
        course_code="DM857",
        module_id="dm857.m01",
        item_ids=("q1", "q2", "q3"),
        seed=857,
        locale="da-DK",
        started_at=NOW,
        answered_item_ids=("q1",),
        correct_count=1,
    )
    SQLiteProgressRepository(database_path).save_assessment_session(session)

    restored = SQLiteProgressRepository(database_path).latest_open_assessment_session(
        course_code="DM857",
        module_id="dm857.m01",
    )

    assert restored == session
    assert restored is not None
    assert restored.item_ids == ("q1", "q2", "q3")
    assert restored.seed == 857


def test_due_reviews_are_filtered_and_ordered(tmp_path: Path) -> None:
    repository = SQLiteProgressRepository(tmp_path / "progress.sqlite3")
    base = ReviewSchedule(
        course_code="DM857",
        module_id="dm857.m01",
        item_id="item-later",
        item_kind=LearningItemKind.PRACTICE,
        mastery_state=MasteryState.LEARNING,
        repetitions=0,
        interval_days=0,
        easiness=2.5,
        due_at=NOW + timedelta(hours=1),
    )
    repository.save_review_schedule(base)
    repository.save_review_schedule(
        replace(base, item_id="item-first", due_at=NOW - timedelta(days=1))
    )
    repository.save_review_schedule(
        replace(
            base,
            course_code="OTHER",
            module_id="other.m01",
            item_id="other-item",
            due_at=NOW - timedelta(days=2),
        )
    )

    due = repository.list_due_reviews(due_at=NOW, course_code="DM857")

    assert tuple(item.item_id for item in due) == ("item-first",)


def test_flashcard_progress_and_module_summary_are_persistent(tmp_path: Path) -> None:
    repository = SQLiteProgressRepository(tmp_path / "progress.sqlite3")
    card = FlashcardProgress(
        course_code="DM857",
        module_id="dm857.m01",
        card_id="dm857.m01.concept.state",
        mastery_state=MasteryState.REVIEWING,
        repetitions=2,
        interval_days=6,
        easiness=2.5,
        due_at=NOW + timedelta(days=6),
        last_reviewed_at=NOW,
    )
    repository.save_flashcard_progress(card)
    repository.record_attempt(_attempt())
    repository.save_review_schedule(
        ReviewSchedule(
            course_code="DM857",
            module_id="dm857.m01",
            item_id="m01.p01",
            item_kind=LearningItemKind.PRACTICE,
            mastery_state=MasteryState.LEARNING,
            repetitions=0,
            interval_days=0,
            easiness=2.5,
            due_at=NOW - timedelta(days=1),
        )
    )

    assert (
        repository.get_flashcard_progress("DM857", "dm857.m01", "dm857.m01.concept.state") == card
    )
    summary = repository.module_progress("DM857", "dm857.m01")
    assert summary.attempt_count == 1
    assert summary.correct_count == 1
    assert summary.pending_review_count == 1
    assert summary.last_activity_at == NOW
