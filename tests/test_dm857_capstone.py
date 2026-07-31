"""Domain and storage tests for the DM857 capstone preparation workflow."""

from __future__ import annotations

from datetime import datetime, timezone

import pytest

from computational_biomedicine_study_hub.i18n import AppLocale
from computational_biomedicine_study_hub.i18n.capstone_copy import validate_capstone_copy
from computational_biomedicine_study_hub.learning.dm857_capstone import (
    DM857_CAPSTONE_MILESTONES,
    DM857_CAPSTONE_RUBRIC,
    CapstoneMilestoneProgress,
    CapstoneMilestoneStatus,
    DM857CapstoneProgress,
)
from computational_biomedicine_study_hub.storage import (
    DM857CapstoneStore,
    SQLiteProgressStore,
)

NOW = datetime(2026, 7, 31, 14, 0, tzinfo=timezone.utc)


def _ready_milestone(index: int) -> CapstoneMilestoneProgress:
    spec = DM857_CAPSTONE_MILESTONES[index]
    return CapstoneMilestoneProgress(
        milestone_id=spec.milestone_id,
        completed_item_ids=spec.checklist_item_ids,
        evidence_note=f"Evidence for milestone {index + 1}",
        commit_reference=f"commit-{index + 1}",
    )


def test_capstone_contract_has_five_milestones_and_weighted_internal_rubric() -> None:
    assert len(DM857_CAPSTONE_MILESTONES) == 5
    assert len(DM857_CAPSTONE_RUBRIC) == 7
    assert sum(criterion.weight_percent for criterion in DM857_CAPSTONE_RUBRIC) == 100
    assert all(spec.official_requirement_ids for spec in DM857_CAPSTONE_MILESTONES)
    assert all(criterion.official_requirement_ids for criterion in DM857_CAPSTONE_RUBRIC)


def test_capstone_copy_is_complete_in_all_supported_locales() -> None:
    validate_capstone_copy()
    assert tuple(AppLocale)


def test_milestone_status_requires_checklist_note_and_repository_reference() -> None:
    spec = DM857_CAPSTONE_MILESTONES[0]
    empty = CapstoneMilestoneProgress(spec.milestone_id)
    partial = CapstoneMilestoneProgress(
        spec.milestone_id,
        completed_item_ids=spec.checklist_item_ids,
        evidence_note="Model documented",
    )
    ready = _ready_milestone(0)

    assert empty.status is CapstoneMilestoneStatus.NOT_STARTED
    assert partial.status is CapstoneMilestoneStatus.IN_PROGRESS
    assert ready.status is CapstoneMilestoneStatus.READY


def test_capstone_progress_round_trip_preserves_stable_evidence_identity() -> None:
    progress = DM857CapstoneProgress.empty(now=NOW).with_metadata(
        project_title="Variant quality checker",
        group_members=("Ada", "Linus"),
        repository_url="https://example.invalid/group/project",
        report_path="reports/dm857.pdf",
        now=NOW,
    )
    for index in range(len(DM857_CAPSTONE_MILESTONES)):
        progress = progress.with_milestone(_ready_milestone(index), now=NOW)
    for criterion in DM857_CAPSTONE_RUBRIC:
        progress = progress.with_rubric_score(criterion.criterion_id, 3, now=NOW)

    restored = DM857CapstoneProgress.from_json(progress.to_json())

    assert restored == progress
    assert restored.ready_milestone_count == 5
    assert restored.milestone_completion_percent == 100
    assert restored.weighted_rubric_percent == 75
    assert restored.preparation_ready


def test_capstone_rejects_unknown_checklist_evidence() -> None:
    with pytest.raises(ValueError, match="unknown checklist"):
        CapstoneMilestoneProgress(
            DM857_CAPSTONE_MILESTONES[0].milestone_id,
            completed_item_ids=("dm857.capstone.unknown",),
        )


def test_capstone_store_persists_across_reopen(tmp_path) -> None:
    database = tmp_path / "learning.sqlite3"
    store = DM857CapstoneStore(database)
    progress = DM857CapstoneProgress.empty(now=NOW).with_metadata(
        project_title="Tree analysis",
        group_members=("A", "B"),
        repository_url="https://example.invalid/tree",
        report_path="report.md",
        now=NOW,
    )

    store.save(progress)
    reopened = DM857CapstoneStore(database)

    assert reopened.load() == progress
    assert reopened.path is not None
    assert reopened.path.exists()


def test_capstone_store_discards_malformed_documents(tmp_path) -> None:
    store = DM857CapstoneStore(tmp_path / "learning.sqlite3")
    assert store.path is not None
    store.path.write_text("{not-json", encoding="utf-8")

    assert store.load() is None
    assert not store.path.exists()


def test_in_memory_capstone_store_shares_progress_store_lifetime() -> None:
    progress_store = SQLiteProgressStore(":memory:")
    first = DM857CapstoneStore.for_progress_store(progress_store)
    progress = DM857CapstoneProgress.empty(now=NOW).with_metadata(
        project_title="In-memory capstone",
        group_members=("Student",),
        repository_url="https://example.invalid/repo",
        report_path="report.md",
        now=NOW,
    )
    first.save(progress)

    second = DM857CapstoneStore.for_progress_store(progress_store)

    assert second.load() == progress
    progress_store.close()
