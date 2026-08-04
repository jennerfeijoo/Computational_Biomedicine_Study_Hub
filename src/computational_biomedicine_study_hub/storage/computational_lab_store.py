"""Atomic persistence for learner-owned computational laboratory notebooks."""

from __future__ import annotations

from pathlib import Path

from ..learning.computational_labs import LabNotebookSnapshot, LabSnapshotError
from .atomic_json_store import AtomicJsonSidecarStore
from .sqlite_progress_store import SQLiteProgressStore


def _serialize(snapshot: LabNotebookSnapshot) -> str:
    return snapshot.to_json()


class ComputationalLabStore(AtomicJsonSidecarStore[LabNotebookSnapshot]):
    """Persist all laboratory attempts beside the local learning database."""

    def __init__(
        self,
        database: str | Path,
        *,
        memory_owner: SQLiteProgressStore | None = None,
    ) -> None:
        super().__init__(
            database,
            suffix=".computational-labs.json",
            serializer=_serialize,
            deserializer=LabNotebookSnapshot.from_json,
            invalid_exceptions=(LabSnapshotError,),
            memory_owner=memory_owner,
        )

    @classmethod
    def for_progress_store(
        cls,
        progress_store: SQLiteProgressStore,
    ) -> ComputationalLabStore:
        return cls(
            progress_store.database,
            memory_owner=progress_store if progress_store.database == ":memory:" else None,
        )


__all__ = ["ComputationalLabStore"]
