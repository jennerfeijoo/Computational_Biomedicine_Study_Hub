"""Reusable atomic JSON sidecar persistence for private assessment state."""

from __future__ import annotations

from collections.abc import Callable
from pathlib import Path
from typing import Generic, TypeVar
from weakref import WeakKeyDictionary

from .sqlite_progress_store import SQLiteProgressStore

DocumentT = TypeVar("DocumentT")

_MEMORY_DOCUMENTS: WeakKeyDictionary[SQLiteProgressStore, dict[str, str]] = WeakKeyDictionary()


class AtomicJsonSidecarStore(Generic[DocumentT]):
    """Persist one typed JSON document beside the local learning database.

    File-backed stores use write-then-replace semantics. In-memory progress stores
    receive isolated namespaced documents so independent assessment workflows cannot
    overwrite one another during tests.
    """

    def __init__(
        self,
        database: str | Path,
        *,
        suffix: str,
        serializer: Callable[[DocumentT], str],
        deserializer: Callable[[str], DocumentT],
        invalid_exceptions: tuple[type[Exception], ...],
        memory_owner: SQLiteProgressStore | None = None,
    ) -> None:
        if not suffix.startswith(".") or not suffix.endswith(".json"):
            raise ValueError("JSON sidecar suffixes must start with '.' and end with '.json'.")
        if not invalid_exceptions:
            raise ValueError("JSON sidecar stores require explicit invalid-document exceptions.")

        self._database = str(database)
        self._suffix = suffix
        self._serializer = serializer
        self._deserializer = deserializer
        self._invalid_exceptions = invalid_exceptions
        self._memory_owner = memory_owner
        self._path = (
            None if self._database == ":memory:" else Path(f"{self._database}{self._suffix}")
        )
        if self._path is not None:
            self._path.parent.mkdir(parents=True, exist_ok=True)

    @property
    def path(self) -> Path | None:
        """Return the sidecar path, or ``None`` for an in-memory store."""

        return self._path

    def save(self, document: DocumentT) -> None:
        """Atomically replace the current serialized document."""

        serialized = self._serializer(document)
        if self._path is None:
            owner = self._require_memory_owner()
            documents = _MEMORY_DOCUMENTS.setdefault(owner, {})
            documents[self._suffix] = serialized
            return

        temporary = self._temporary_path()
        temporary.write_text(serialized, encoding="utf-8")
        temporary.replace(self._path)

    def load(self) -> DocumentT | None:
        """Return a validated document and discard malformed local state."""

        try:
            serialized = self._read_serialized()
            if serialized is None:
                return None
            return self._deserializer(serialized)
        except (OSError, UnicodeError):
            self.discard()
            return None
        except self._invalid_exceptions:
            self.discard()
            return None

    def discard(self) -> None:
        """Remove the namespaced document without touching other learning evidence."""

        if self._path is None:
            owner = self._require_memory_owner()
            documents = _MEMORY_DOCUMENTS.get(owner)
            if documents is None:
                return
            documents.pop(self._suffix, None)
            if not documents:
                _MEMORY_DOCUMENTS.pop(owner, None)
            return

        for path in (self._path, self._temporary_path()):
            try:
                path.unlink()
            except FileNotFoundError:
                pass

    def _read_serialized(self) -> str | None:
        if self._path is None:
            documents = _MEMORY_DOCUMENTS.get(self._require_memory_owner())
            return None if documents is None else documents.get(self._suffix)
        if not self._path.exists():
            return None
        return self._path.read_text(encoding="utf-8")

    def _temporary_path(self) -> Path:
        if self._path is None:
            raise RuntimeError("In-memory JSON sidecars do not have temporary paths.")
        return self._path.with_name(f"{self._path.name}.tmp")

    def _require_memory_owner(self) -> SQLiteProgressStore:
        owner = self._memory_owner
        if owner is None:
            raise RuntimeError("In-memory JSON sidecars require a progress-store owner.")
        return owner


__all__ = ["AtomicJsonSidecarStore"]
