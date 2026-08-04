"""Atomic persistence for artifact-based technical reasoning attempts."""

from __future__ import annotations

from pathlib import Path

from ..learning.technical_stations import (
    TechnicalStationSnapshot,
    TechnicalStationSnapshotError,
)
from .atomic_json_store import AtomicJsonSidecarStore
from .sqlite_progress_store import SQLiteProgressStore


def _serialize(snapshot: TechnicalStationSnapshot) -> str:
    return snapshot.to_json()


class TechnicalStationStore(AtomicJsonSidecarStore[TechnicalStationSnapshot]):
    """Persist technical-station attempts beside the local progress database."""

    def __init__(
        self,
        database: str | Path,
        *,
        memory_owner: SQLiteProgressStore | None = None,
    ) -> None:
        super().__init__(
            database,
            suffix=".technical-stations.json",
            serializer=_serialize,
            deserializer=TechnicalStationSnapshot.from_json,
            invalid_exceptions=(TechnicalStationSnapshotError,),
            memory_owner=memory_owner,
        )

    @classmethod
    def for_progress_store(
        cls,
        progress_store: SQLiteProgressStore,
    ) -> TechnicalStationStore:
        return cls(
            progress_store.database,
            memory_owner=progress_store if progress_store.database == ":memory:" else None,
        )


__all__ = ["TechnicalStationStore"]
