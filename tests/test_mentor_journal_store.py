"""Persistence tests for private longitudinal mentor observations."""

from __future__ import annotations

from datetime import UTC, datetime

from computational_biomedicine_study_hub.learning.mentor import (
    MentorJournalSnapshot,
    MentorMode,
    MentorObservation,
    MentorTurnRecord,
)
from computational_biomedicine_study_hub.storage import (
    MentorJournalStore,
    SQLiteProgressStore,
)


NOW = datetime(2026, 8, 4, 12, 0, tzinfo=UTC)


def _snapshot() -> MentorJournalSnapshot:
    return MentorJournalSnapshot.empty(now=NOW).append(
        MentorTurnRecord(
            session_id="session-a",
            created_at=NOW,
            context="DM847 | Sequence alignment",
            mode=MentorMode.EVALUATE,
            user_message="My answer",
            assistant_message="Targeted feedback",
            observation=MentorObservation(
                demonstrated=("Identified the alignment objective",),
                gaps=("Did not justify the scoring matrix",),
                recommended_next_action="Compare two scoring matrices",
                confidence=0.75,
            ),
            model="test-model",
        ),
        now=NOW,
    )


def test_file_backed_mentor_journal_round_trip(tmp_path) -> None:  # type: ignore[no-untyped-def]
    database = tmp_path / "progress.sqlite3"
    store = MentorJournalStore(database)
    snapshot = _snapshot()

    store.save(snapshot)

    assert store.load() == snapshot
    assert store.path == tmp_path / "progress.sqlite3.mentor-journal.json"


def test_in_memory_mentor_journal_shares_progress_lifetime() -> None:
    progress = SQLiteProgressStore(":memory:")
    try:
        store = MentorJournalStore.for_progress_store(progress)
        snapshot = _snapshot()
        store.save(snapshot)

        restored = MentorJournalStore.for_progress_store(progress).load_or_empty()

        assert restored == snapshot
    finally:
        progress.close()


def test_malformed_mentor_journal_is_discarded(tmp_path) -> None:  # type: ignore[no-untyped-def]
    database = tmp_path / "progress.sqlite3"
    store = MentorJournalStore(database)
    assert store.path is not None
    store.path.write_text("{malformed", encoding="utf-8")

    assert store.load() is None
    assert not store.path.exists()
