"""Atomic sidecar persistence for one resumable adaptive review session."""

from __future__ import annotations

from pathlib import Path
from weakref import WeakKeyDictionary

from ..learning.adaptive_review import (
    AdaptiveReviewSessionSnapshot,
    AdaptiveReviewSnapshotError,
)
from .sqlite_progress_store import SQLiteProgressStore

_MEMORY_DOCUMENTS: WeakKeyDictionary[SQLiteProgressStore, str] = WeakKeyDictionary()


class AdaptiveReviewSessionStore:
    """Persist transient session state separately from immutable learning evidence."""

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
            else Path(f"{self._database}.active-review.json")
        )
        if self._path is not None:
            self._path.parent.mkdir(parents=True, exist_ok=True)

    @classmethod
    def for_progress_store(
        cls,
        progress_store: SQLiteProgressStore,
    ) -> AdaptiveReviewSessionStore:
        """Create a session store sharing the progress store's local lifetime."""

        return cls(
            progress_store.database,
            memory_owner=progress_store if progress_store.database == ":memory:" else None,
        )

    @property
    def path(self) -> Path | None:
        """Return the sidecar path, or ``None`` for an in-memory test store."""

        return self._path

    def save(self, snapshot: AdaptiveReviewSessionSnapshot) -> None:
        """Atomically replace the currently resumable session."""

        document = snapshot.to_json()
        if self._path is None:
            owner = self._require_memory_owner()
            _MEMORY_DOCUMENTS[owner] = document
            return

        temporary = self._path.with_name(f"{self._path.name}.tmp")
        temporary.write_text(document, encoding="utf-8")
        temporary.replace(self._path)

    def load(self) -> AdaptiveReviewSessionSnapshot | None:
        """Return the saved session, deleting malformed documents defensively."""

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
        try:
            return AdaptiveReviewSessionSnapshot.from_json(document)
        except (AdaptiveReviewSnapshotError, OSError, UnicodeError):
            self.discard()
            return None

    def discard(self) -> None:
        """Remove the current resumable session without touching learning evidence."""

        if self._path is None:
            owner = self._require_memory_owner()
            _MEMORY_DOCUMENTS.pop(owner, None)
            return
        try:
            self._path.unlink()
        except FileNotFoundError:
            pass
        temporary = self._path.with_name(f"{self._path.name}.tmp")
        try:
            temporary.unlink()
        except FileNotFoundError:
            pass

    def _require_memory_owner(self) -> SQLiteProgressStore:
        owner = self._memory_owner
        if owner is None:
            raise RuntimeError("In-memory adaptive review storage requires an owner.")
        return owner


__all__ = ["AdaptiveReviewSessionStore"]
