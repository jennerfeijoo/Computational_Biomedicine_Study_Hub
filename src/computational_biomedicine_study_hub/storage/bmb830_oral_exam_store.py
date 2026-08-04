"""Typed atomic sidecar persistence for BMB830 oral-practice history."""

from __future__ import annotations

from pathlib import Path

from ..learning.bmb830_oral_exam import (
    BMB830OralSnapshot,
    BMB830OralSnapshotError,
)
from .atomic_json_store import AtomicJsonSidecarStore
from .sqlite_progress_store import SQLiteProgressStore


def _serialize(snapshot: BMB830OralSnapshot) -> str:
    return snapshot.to_json()


class BMB830OralExamStore(AtomicJsonSidecarStore[BMB830OralSnapshot]):
    """Persist private formative oral-exam attempts beside learning progress."""

    def __init__(
        self,
        database: str | Path,
        *,
        memory_owner: SQLiteProgressStore | None = None,
    ) -> None:
        super().__init__(
            database,
            suffix=".bmb830-oral-exam.json",
            serializer=_serialize,
            deserializer=BMB830OralSnapshot.from_json,
            invalid_exceptions=(BMB830OralSnapshotError, ValueError),
            memory_owner=memory_owner,
        )

    @classmethod
    def for_progress_store(
        cls,
        progress_store: SQLiteProgressStore,
    ) -> BMB830OralExamStore:
        return cls(
            progress_store.database,
            memory_owner=progress_store if progress_store.database == ":memory:" else None,
        )


__all__ = ["BMB830OralExamStore"]
