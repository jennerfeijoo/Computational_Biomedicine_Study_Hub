"""Regression tests for namespaced atomic JSON sidecar persistence."""

from __future__ import annotations

from dataclasses import dataclass

from computational_biomedicine_study_hub.storage.atomic_json_store import AtomicJsonSidecarStore
from computational_biomedicine_study_hub.storage.sqlite_progress_store import SQLiteProgressStore


class InvalidDocumentError(ValueError):
    pass


@dataclass(frozen=True)
class Document:
    value: str


def _serialize(document: Document) -> str:
    return document.value


def _deserialize(document: str) -> Document:
    if document == "invalid":
        raise InvalidDocumentError("invalid fixture")
    return Document(document)


def _store(
    progress: SQLiteProgressStore,
    suffix: str,
) -> AtomicJsonSidecarStore[Document]:
    return AtomicJsonSidecarStore(
        progress.database,
        suffix=suffix,
        serializer=_serialize,
        deserializer=_deserialize,
        invalid_exceptions=(InvalidDocumentError,),
        memory_owner=progress,
    )


def test_in_memory_sidecars_are_isolated_by_suffix() -> None:
    progress = SQLiteProgressStore(":memory:")
    try:
        first = _store(progress, ".first.json")
        second = _store(progress, ".second.json")

        first.save(Document("alpha"))
        second.save(Document("beta"))

        assert first.load() == Document("alpha")
        assert second.load() == Document("beta")
        first.discard()
        assert first.load() is None
        assert second.load() == Document("beta")
    finally:
        progress.close()


def test_invalid_in_memory_document_is_discarded_defensively() -> None:
    progress = SQLiteProgressStore(":memory:")
    try:
        store = _store(progress, ".invalid.json")
        store.save(Document("invalid"))

        assert store.load() is None
        assert store.load() is None
    finally:
        progress.close()


def test_file_sidecar_uses_atomic_replacement_and_cleanup(tmp_path) -> None:  # type: ignore[no-untyped-def]
    database = tmp_path / "progress.sqlite3"
    store = AtomicJsonSidecarStore(
        database,
        suffix=".assessment.json",
        serializer=_serialize,
        deserializer=_deserialize,
        invalid_exceptions=(InvalidDocumentError,),
    )

    store.save(Document("first"))
    store.save(Document("second"))

    assert store.load() == Document("second")
    assert store.path is not None
    assert not store.path.with_name(f"{store.path.name}.tmp").exists()
    store.discard()
    assert not store.path.exists()
