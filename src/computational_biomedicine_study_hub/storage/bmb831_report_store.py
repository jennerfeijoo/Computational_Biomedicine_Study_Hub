"""Typed atomic sidecar persistence for the BMB831 individual report."""

from __future__ import annotations

from pathlib import Path

from ..learning.bmb831_report import BMB831ReportSnapshot, BMB831ReportSnapshotError
from .atomic_json_store import AtomicJsonSidecarStore
from .sqlite_progress_store import SQLiteProgressStore


def _serialize(snapshot: BMB831ReportSnapshot) -> str:
    return snapshot.to_json()


class BMB831ReportStore(AtomicJsonSidecarStore[BMB831ReportSnapshot]):
    """Persist one private BMB831 report beside learning progress."""

    def __init__(
        self,
        database: str | Path,
        *,
        memory_owner: SQLiteProgressStore | None = None,
    ) -> None:
        super().__init__(
            database,
            suffix=".bmb831-report.json",
            serializer=_serialize,
            deserializer=BMB831ReportSnapshot.from_json,
            invalid_exceptions=(BMB831ReportSnapshotError,),
            memory_owner=memory_owner,
        )

    @classmethod
    def for_progress_store(cls, progress_store: SQLiteProgressStore) -> BMB831ReportStore:
        """Create storage sharing the progress store's local lifetime."""

        return cls(
            progress_store.database,
            memory_owner=progress_store if progress_store.database == ":memory:" else None,
        )


__all__ = ["BMB831ReportStore"]
