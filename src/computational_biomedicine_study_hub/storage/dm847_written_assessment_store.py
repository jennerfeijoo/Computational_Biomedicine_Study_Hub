"""Typed atomic sidecar persistence for DM847 written-assessment drafts."""

from __future__ import annotations

from pathlib import Path

from ..learning.dm847_written_assessment import (
    WrittenAssessmentSnapshot,
    WrittenAssessmentSnapshotError,
)
from .atomic_json_store import AtomicJsonSidecarStore
from .sqlite_progress_store import SQLiteProgressStore


def _serialize(snapshot: WrittenAssessmentSnapshot) -> str:
    return snapshot.to_json()


class DM847WrittenAssessmentStore(AtomicJsonSidecarStore[WrittenAssessmentSnapshot]):
    """Persist one private collection of DM847 drafts beside learning progress."""

    def __init__(
        self,
        database: str | Path,
        *,
        memory_owner: SQLiteProgressStore | None = None,
    ) -> None:
        super().__init__(
            database,
            suffix=".dm847-writing.json",
            serializer=_serialize,
            deserializer=WrittenAssessmentSnapshot.from_json,
            invalid_exceptions=(WrittenAssessmentSnapshotError,),
            memory_owner=memory_owner,
        )

    @classmethod
    def for_progress_store(
        cls,
        progress_store: SQLiteProgressStore,
    ) -> DM847WrittenAssessmentStore:
        """Create a store sharing the progress store's local lifetime."""

        return cls(
            progress_store.database,
            memory_owner=progress_store if progress_store.database == ":memory:" else None,
        )


__all__ = ["DM847WrittenAssessmentStore"]
