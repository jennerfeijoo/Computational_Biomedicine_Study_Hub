"""Typed atomic sidecar persistence for DM857 weekly supervision history."""

from __future__ import annotations

from pathlib import Path

from ..learning.dm857_weekly_supervision import (
    DM857WeeklySupervisionSnapshot,
    WeeklySupervisionSnapshotError,
)
from .atomic_json_store import AtomicJsonSidecarStore
from .sqlite_progress_store import SQLiteProgressStore


def _serialize(snapshot: DM857WeeklySupervisionSnapshot) -> str:
    return snapshot.to_json()


class DM857WeeklySupervisionStore(AtomicJsonSidecarStore[DM857WeeklySupervisionSnapshot]):
    """Persist longitudinal project evidence beside the learning database."""

    def __init__(
        self,
        database: str | Path,
        *,
        memory_owner: SQLiteProgressStore | None = None,
    ) -> None:
        super().__init__(
            database,
            suffix=".dm857-weekly-supervision.json",
            serializer=_serialize,
            deserializer=DM857WeeklySupervisionSnapshot.from_json,
            invalid_exceptions=(WeeklySupervisionSnapshotError,),
            memory_owner=memory_owner,
        )

    @classmethod
    def for_progress_store(
        cls,
        progress_store: SQLiteProgressStore,
    ) -> DM857WeeklySupervisionStore:
        """Create a store sharing the progress store's local lifetime."""

        return cls(
            progress_store.database,
            memory_owner=progress_store if progress_store.database == ":memory:" else None,
        )


__all__ = ["DM857WeeklySupervisionStore"]
