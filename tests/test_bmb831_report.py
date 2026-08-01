"""Domain and persistence tests for the BMB831 individual report."""

from __future__ import annotations

from datetime import UTC, datetime
from pathlib import Path

import pytest

from computational_biomedicine_study_hub.learning.bmb831_report import (
    BMB831_REPORT_SECTIONS,
    BMB831ReportSnapshot,
    BMB831ReportSnapshotError,
)
from computational_biomedicine_study_hub.storage.bmb831_report_store import BMB831ReportStore
from computational_biomedicine_study_hub.storage.sqlite_progress_store import SQLiteProgressStore


def test_empty_report_has_authored_order_and_deterministic_counts() -> None:
    now = datetime(2026, 8, 1, 8, 0, tzinfo=UTC)
    snapshot = BMB831ReportSnapshot.empty(now=now)

    assert snapshot.schema_version == 1
    assert snapshot.active_section_id == BMB831_REPORT_SECTIONS[0].section_id
    assert tuple(draft.section_id for draft in snapshot.drafts) == tuple(
        section.section_id for section in BMB831_REPORT_SECTIONS
    )
    assert snapshot.completed_section_count == 0
    assert snapshot.total_word_count == 0
    assert snapshot.updated_at == now


def test_report_updates_one_section_and_round_trips_json() -> None:
    snapshot = BMB831ReportSnapshot.empty().with_text(
        "bmb831.report.question",
        "We estimate the treatment effect among eligible samples.",
    )
    snapshot = snapshot.with_active_section("bmb831.report.methods")
    restored = BMB831ReportSnapshot.from_json(snapshot.to_json())

    assert restored == snapshot
    assert restored.completed_section_count == 1
    assert restored.total_word_count == 8
    assert restored.draft("bmb831.report.question").text.startswith("We estimate")


def test_report_parser_rejects_malformed_or_reordered_state() -> None:
    with pytest.raises(BMB831ReportSnapshotError):
        BMB831ReportSnapshot.from_json("not-json")

    snapshot = BMB831ReportSnapshot.empty()
    document = snapshot.to_json().replace(
        '"section_id":"bmb831.report.question"',
        '"section_id":"bmb831.report.unknown"',
        1,
    )
    with pytest.raises(BMB831ReportSnapshotError):
        BMB831ReportSnapshot.from_json(document)


def test_report_store_persists_atomically_next_to_database(tmp_path: Path) -> None:
    database = tmp_path / "progress.sqlite3"
    progress = SQLiteProgressStore(database)
    store = BMB831ReportStore.for_progress_store(progress)
    snapshot = BMB831ReportSnapshot.empty().with_text(
        "bmb831.report.results",
        "The adjusted log2 fold change was 1.20.",
    )

    store.save(snapshot)
    assert store.path == Path(f"{database}.bmb831-report.json")
    assert store.path is not None and store.path.is_file()
    assert store.load() == snapshot
    assert not store.path.with_name(f"{store.path.name}.tmp").exists()

    store.discard()
    assert store.load() is None


def test_memory_report_store_shares_progress_store_lifetime() -> None:
    progress = SQLiteProgressStore(":memory:")
    first = BMB831ReportStore.for_progress_store(progress)
    second = BMB831ReportStore.for_progress_store(progress)
    snapshot = BMB831ReportSnapshot.empty().with_text(
        "bmb831.report.abstract",
        "This report evaluates a versioned omics workflow.",
    )

    first.save(snapshot)
    assert second.load() == snapshot
