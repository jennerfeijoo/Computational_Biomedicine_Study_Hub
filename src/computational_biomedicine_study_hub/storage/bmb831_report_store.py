"""Atomic sidecar persistence for the BMB831 individual report."""

from __future__ import annotations

from pathlib import Path
from weakref import WeakKeyDictionary

from ..learning.bmb831_report import BMB831ReportSnapshot, BMB831ReportSnapshotError
from .sqlite_progress_store import SQLiteProgressStore

_MEMORY_DOCUMENTS: WeakKeyDictionary[SQLiteProgressStore, str] = WeakKeyDictionary()


class BMB831ReportStore:
    """Persist one private BMB831 report beside learning progress."""

    def __init__(
        self,
        database: str | Path,
        *,
        memory_owner: SQLiteProgressStore | None = None,
    ) -> None:
        self._database = str(database)
        self._memory_owner = memory_owner
        self._path = (
            None if self._database == ":memory:" else Path(f"{self._database}.bmb831-report.json")
        )
        if self._path is not None:
            self._path.parent.mkdir(parents=True, exist_ok=True)

    @classmethod
    def for_progress_store(cls, progress_store: SQLiteProgressStore) -> BMB831ReportStore:
        """Create storage sharing the progress store's local lifetime."""

        return cls(
            progress_store.database,
            memory_owner=progress_store if progress_store.database == ":memory:" else None,
        )

    @property
    def path(self) -> Path | None:
        """Return the sidecar path, or ``None`` for an in-memory test store."""

        return self._path

    def save(self, snapshot: BMB831ReportSnapshot) -> None:
        """Atomically replace the current report document."""

        document = snapshot.to_json()
        if self._path is None:
            _MEMORY_DOCUMENTS[self._require_memory_owner()] = document
            return
        temporary = self._path.with_name(f"{self._path.name}.tmp")
        temporary.write_text(document, encoding="utf-8")
        temporary.replace(self._path)

    def load(self) -> BMB831ReportSnapshot | None:
        """Return saved report state, deleting malformed documents defensively."""

        try:
            document: str | None
            if self._path is None:
                document = _MEMORY_DOCUMENTS.get(self._require_memory_owner())
            elif self._path.exists():
                document = self._path.read_text(encoding="utf-8")
            else:
                document = None
            if document is None:
                return None
            return BMB831ReportSnapshot.from_json(document)
        except (BMB831ReportSnapshotError, OSError, UnicodeError):
            self.discard()
            return None

    def discard(self) -> None:
        """Remove report drafts without touching learning evidence."""

        if self._path is None:
            _MEMORY_DOCUMENTS.pop(self._require_memory_owner(), None)
            return
        for path in (self._path, self._path.with_name(f"{self._path.name}.tmp")):
            try:
                path.unlink()
            except FileNotFoundError:
                pass

    def _require_memory_owner(self) -> SQLiteProgressStore:
        owner = self._memory_owner
        if owner is None:
            raise RuntimeError("In-memory BMB831 report storage requires a progress-store owner.")
        return owner


__all__ = ["BMB831ReportStore"]
