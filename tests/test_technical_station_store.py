"""Persistence tests for artifact-based technical reasoning evidence."""

from __future__ import annotations

from computational_biomedicine_study_hub.content.technical_stations import (
    DM847_TECHNICAL_STATIONS,
)
from computational_biomedicine_study_hub.learning.technical_stations import (
    TechnicalStationAttempt,
    TechnicalStationSnapshot,
)
from computational_biomedicine_study_hub.storage.sqlite_progress_store import (
    SQLiteProgressStore,
)
from computational_biomedicine_study_hub.storage.technical_station_store import (
    TechnicalStationStore,
)


def test_store_round_trip_for_file_backed_progress(tmp_path) -> None:  # type: ignore[no-untyped-def]
    database = tmp_path / "progress.sqlite3"
    station = DM847_TECHNICAL_STATIONS[0]
    attempt = TechnicalStationAttempt.new(station).with_response(
        "A detailed response that defines the code contract and its boundary behaviour."
    )
    snapshot = TechnicalStationSnapshot().with_attempt(attempt)
    store = TechnicalStationStore(database)

    store.save(snapshot)

    assert store.load() == snapshot
    assert (tmp_path / "progress.sqlite3.technical-stations.json").is_file()


def test_store_uses_memory_owner_for_in_memory_progress() -> None:
    progress = SQLiteProgressStore(":memory:")
    try:
        station = DM847_TECHNICAL_STATIONS[0]
        snapshot = TechnicalStationSnapshot().with_attempt(
            TechnicalStationAttempt.new(station).with_response(
                "A persistent in-memory technical response with enough detail for later review."
            )
        )
        first = TechnicalStationStore.for_progress_store(progress)
        first.save(snapshot)

        second = TechnicalStationStore.for_progress_store(progress)

        assert second.load() == snapshot
    finally:
        progress.close()
