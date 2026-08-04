"""Persistence tests for BMB830 oral-exam preparation."""

from __future__ import annotations

from datetime import UTC, datetime

from computational_biomedicine_study_hub.learning.bmb830_oral_exam import (
    BMB830OralAttempt,
    BMB830OralEvaluation,
    BMB830OralSnapshot,
    OralCriterion,
    OralCriterionScore,
)
from computational_biomedicine_study_hub.storage import (
    BMB830OralExamStore,
    SQLiteProgressStore,
)

NOW = datetime(2026, 8, 4, 12, 0, tzinfo=UTC)


def _snapshot() -> BMB830OralSnapshot:
    evaluation = BMB830OralEvaluation(
        feedback="Feedback",
        strengths=("Strength",),
        gaps=("Gap",),
        misconceptions=(),
        scores=tuple(OralCriterionScore(criterion, 3, "Evidence") for criterion in OralCriterion),
        follow_up_question="Why?",
        recommended_next_action="Revise",
        confidence=0.7,
    )
    attempt = BMB830OralAttempt(
        attempt_id="attempt-1",
        prompt_id="prompt-1",
        module_id="module-1",
        transcript="Transcript",
        evaluation=evaluation,
        created_at=NOW,
    )
    return BMB830OralSnapshot.empty("prompt-1", now=NOW).append(attempt, now=NOW)


def test_file_backed_oral_snapshot_round_trip(tmp_path) -> None:  # type: ignore[no-untyped-def]
    store = BMB830OralExamStore(tmp_path / "progress.sqlite3")
    snapshot = _snapshot()

    store.save(snapshot)

    assert store.load() == snapshot
    assert store.path == tmp_path / "progress.sqlite3.bmb830-oral-exam.json"


def test_in_memory_oral_snapshot_shares_progress_lifetime() -> None:
    progress = SQLiteProgressStore(":memory:")
    try:
        store = BMB830OralExamStore.for_progress_store(progress)
        store.save(_snapshot())

        assert BMB830OralExamStore.for_progress_store(progress).load() == _snapshot()
    finally:
        progress.close()


def test_malformed_oral_snapshot_is_discarded(tmp_path) -> None:  # type: ignore[no-untyped-def]
    store = BMB830OralExamStore(tmp_path / "progress.sqlite3")
    assert store.path is not None
    store.path.write_text("{broken", encoding="utf-8")

    assert store.load() is None
    assert not store.path.exists()
