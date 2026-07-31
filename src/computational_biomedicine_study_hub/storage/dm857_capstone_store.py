"""Atomic sidecar persistence for durable DM857 capstone preparation state."""

from __future__ import annotations

from pathlib import Path
from weakref import WeakKeyDictionary

from ..learning.dm857_capstone import CapstoneSnapshotError, DM857CapstoneProgress
from .sqlite_progress_store import SQLiteProgressStore

_MEMORY_DOCUMENTS: WeakKeyDictionary[SQLiteProgressStore, str] = WeakKeyDictionary()


class DM857CapstoneStore:
    """Persist one private capstone scaffold beside the learning database."""

    def __init__(
        self,
        database: str | Path,
        *,
        memory_owner: SQLiteProgressStore | None = None,
    ) -> None:
        self._database = str(database)
        self._memory_owner = memory_owner
        self._path = (
            None if self._database == ":memory:" else Path(f"{self._database}.dm857-capstone.json")
        )
        if self._path is not None:
            self._path.parent.mkdir(parents=True, exist_ok=True)

    @classmethod
    def for_progress_store(cls, progress_store: SQLiteProgressStore) -> DM857CapstoneStore:
        """Create a capstone store sharing the progress store's local lifetime."""

        return cls(
            progress_store.database,
            memory_owner=progress_store if progress_store.database == ":memory:" else None,
        )

    @property
    def path(self) -> Path | None:
        """Return the sidecar path, or ``None`` for an in-memory test store."""

        return self._path

    def save(self, progress: DM857CapstoneProgress) -> None:
        """Atomically replace the current capstone document."""

        document = progress.to_json()
        if self._path is None:
            owner = self._require_memory_owner()
            _MEMORY_DOCUMENTS[owner] = document
            return

        temporary = self._path.with_name(f"{self._path.name}.tmp")
        temporary.write_text(document, encoding="utf-8")
        temporary.replace(self._path)

    def load(self) -> DM857CapstoneProgress | None:
        """Return saved progress, deleting malformed documents defensively."""

        try:
            document: str | None
            if self._path is None:
                owner = self._require_memory_owner()
                document = _MEMORY_DOCUMENTS.get(owner)
            elif self._path.exists():
                document = self._path.read_text(encoding="utf-8")
            else:
                document = None

            if document is None:
                return None
            return DM857CapstoneProgress.from_json(document)
        except (CapstoneSnapshotError, OSError, UnicodeError):
            self.discard()
            return None

    def discard(self) -> None:
        """Remove capstone preparation state without touching learning evidence."""

        if self._path is None:
            owner = self._require_memory_owner()
            _MEMORY_DOCUMENTS.pop(owner, None)
            return

        for path in (self._path, self._path.with_name(f"{self._path.name}.tmp")):
            try:
                path.unlink()
            except FileNotFoundError:
                pass

    def _require_memory_owner(self) -> SQLiteProgressStore:
        owner = self._memory_owner
        if owner is None:
            raise RuntimeError("In-memory capstone storage requires a progress-store owner.")
        return owner


__all__ = ["DM857CapstoneStore"]
