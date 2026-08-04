"""Typed atomic sidecar persistence for durable DM857 capstone state."""

from __future__ import annotations

from pathlib import Path

from ..learning.dm857_capstone import CapstoneSnapshotError, DM857CapstoneProgress
from .atomic_json_store import AtomicJsonSidecarStore
from .sqlite_progress_store import SQLiteProgressStore


def _serialize(progress: DM857CapstoneProgress) -> str:
    return progress.to_json()


class DM857CapstoneStore(AtomicJsonSidecarStore[DM857CapstoneProgress]):
    """Persist one private capstone scaffold beside the learning database."""

    def __init__(
        self,
        database: str | Path,
        *,
        memory_owner: SQLiteProgressStore | None = None,
    ) -> None:
        super().__init__(
            database,
            suffix=".dm857-capstone.json",
            serializer=_serialize,
            deserializer=DM857CapstoneProgress.from_json,
            invalid_exceptions=(CapstoneSnapshotError,),
            memory_owner=memory_owner,
        )

    @classmethod
    def for_progress_store(cls, progress_store: SQLiteProgressStore) -> DM857CapstoneStore:
        """Create a capstone store sharing the progress store's local lifetime."""

        return cls(
            progress_store.database,
            memory_owner=progress_store if progress_store.database == ":memory:" else None,
        )


__all__ = ["DM857CapstoneStore"]
