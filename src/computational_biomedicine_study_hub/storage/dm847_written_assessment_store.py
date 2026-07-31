"""Atomic sidecar persistence for DM847 written-assessment drafts."""

from __future__ import annotations

from pathlib import Path
from weakref import WeakKeyDictionary

from ..learning.dm847_written_assessment import (
    WrittenAssessmentSnapshot,
    WrittenAssessmentSnapshotError,
)
from .sqlite_progress_store import SQLiteProgressStore

_MEMORY_DOCUMENTS: WeakKeyDictionary[SQLiteProgressStore, str] = WeakKeyDictionary()


class DM847WrittenAssessmentStore:
    """Persist one private collection of DM847 drafts beside learning progress."""

    def __init__(
        self,
        database: str | Path,
        *,
        memory_owner: SQLiteProgressStore | None = None,
    ) -> None:
        self._database = str(database)
        self._memory_owner = memory_owner
        self._path = (
            None
            if self._database == ":memory:"
            else Path(f"{self._database}.dm847-writing.json")
        )
        if self._path is not None:
            self._path.parent.mkdir(parents=True, exist_ok=True)

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

    @property
    def path(self) -> Path | None:
        """Return the sidecar path, or ``None`` for an in-memory test store."""

        return self._path

    def save(self, snapshot: WrittenAssessmentSnapshot) -> None:
        """Atomically replace the current written-assessment document."""

        document = snapshot.to_json()
        if self._path is None:
            _MEMORY_DOCUMENTS[self._require_memory_owner()] = document
            return

        temporary = self._path.with_name(f"{self._path.name}.tmp")
        temporary.write_text(document, encoding="utf-8")
        temporary.replace(self._path)

    def load(self) -> WrittenAssessmentSnapshot | None:
        """Return saved drafts, deleting malformed documents defensively."""

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
            return WrittenAssessmentSnapshot.from_json(document)
        except (WrittenAssessmentSnapshotError, OSError, UnicodeError):
            self.discard()
            return None

    def discard(self) -> None:
        """Remove drafts without touching objective-learning evidence."""

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
            raise RuntimeError("In-memory DM847 writing storage requires a progress-store owner.")
        return owner


__all__ = ["DM847WrittenAssessmentStore"]
