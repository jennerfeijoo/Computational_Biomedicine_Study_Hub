"""Typed atomic sidecar persistence for longitudinal mentor observations."""

from __future__ import annotations

from pathlib import Path

from ..learning.mentor import MentorJournalSnapshot, MentorSnapshotError
from .atomic_json_store import AtomicJsonSidecarStore
from .sqlite_progress_store import SQLiteProgressStore


def _serialize(snapshot: MentorJournalSnapshot) -> str:
    return snapshot.to_json()


class MentorJournalStore(AtomicJsonSidecarStore[MentorJournalSnapshot]):
    """Persist private mentor continuity without altering objective mastery."""

    def __init__(
        self,
        database: str | Path,
        *,
        memory_owner: SQLiteProgressStore | None = None,
    ) -> None:
        super().__init__(
            database,
            suffix=".mentor-journal.json",
            serializer=_serialize,
            deserializer=MentorJournalSnapshot.from_json,
            invalid_exceptions=(MentorSnapshotError, ValueError),
            memory_owner=memory_owner,
        )

    @classmethod
    def for_progress_store(cls, progress_store: SQLiteProgressStore) -> MentorJournalStore:
        """Create storage sharing the local progress database lifetime."""

        return cls(
            progress_store.database,
            memory_owner=progress_store if progress_store.database == ":memory:" else None,
        )

    def load_or_empty(self) -> MentorJournalSnapshot:
        """Return validated mentor history or an empty journal."""

        return self.load() or MentorJournalSnapshot.empty()


__all__ = ["MentorJournalStore"]
