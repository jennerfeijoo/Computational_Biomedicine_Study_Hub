"""Domain and persistence tests for longitudinal DM857 project supervision."""

from __future__ import annotations

from datetime import UTC, date, datetime

import pytest

from computational_biomedicine_study_hub.learning.dm857_weekly_supervision import (
    DM857WeeklyCycle,
    DM857WeeklySupervisionSnapshot,
    WeeklyCycleStatus,
    WeeklySupervisionSnapshotError,
    render_weekly_cycle_record,
)
from computational_biomedicine_study_hub.storage import (
    DM857WeeklySupervisionStore,
    SQLiteProgressStore,
)

WEEK = date(2026, 8, 3)
NOW = datetime(2026, 8, 5, 8, 0, tzinfo=UTC)


def _cycle(**overrides: object) -> DM857WeeklyCycle:
    values: dict[str, object] = {
        "objective": "Add deterministic sample validation",
        "success_criteria": "Invalid sample IDs are rejected by tests",
        "start_reference": "commit-start",
        "end_reference": "commit-end",
        "changed_files": "src/validation.py\ntests/test_validation.py",
        "test_evidence": "pytest tests/test_validation.py: 8 passed",
        "decision_rationale": "Use one pure validation function with explicit errors",
        "individual_contribution": "Implemented the validator and boundary tests",
        "biomedical_interpretation": "Prevents malformed sample identifiers entering analysis",
        "blockers": "",
        "reflection": "I now distinguish input validation from downstream analysis",
        "next_commitment": "Add property-based tests for identifier length",
        "blocked": False,
    }
    values.update(overrides)
    empty = DM857WeeklyCycle.empty(WEEK, now=NOW)
    return empty.with_fields(now=NOW, **values)  # type: ignore[arg-type]


def test_weekly_cycle_status_tracks_plan_execution_blockage_and_completion() -> None:
    empty = DM857WeeklyCycle.empty(WEEK, now=NOW)
    planned = _cycle(
        start_reference="",
        end_reference="",
        changed_files="",
        test_evidence="",
        decision_rationale="",
        individual_contribution="",
        biomedical_interpretation="",
        reflection="",
        next_commitment="",
    )
    active = _cycle(end_reference="", reflection="", next_commitment="")
    blocked = _cycle(blocked=True, blockers="Waiting for a group data contract")
    complete = _cycle()

    assert empty.status is WeeklyCycleStatus.EMPTY
    assert planned.status is WeeklyCycleStatus.PLANNED
    assert active.status is WeeklyCycleStatus.ACTIVE
    assert blocked.status is WeeklyCycleStatus.BLOCKED
    assert complete.status is WeeklyCycleStatus.COMPLETE
    assert complete.required_evidence_count == 9
    assert complete.completion_percent == 100


def test_weekly_snapshot_round_trip_preserves_order_selection_and_evidence() -> None:
    first = _cycle()
    second = DM857WeeklyCycle.empty(date(2026, 8, 10), now=NOW)
    snapshot = (
        DM857WeeklySupervisionSnapshot.empty(now=NOW)
        .with_cycle(second, now=NOW)
        .with_cycle(first, now=NOW)
    )

    restored = DM857WeeklySupervisionSnapshot.from_json(snapshot.to_json())

    assert restored == snapshot
    assert tuple(cycle.week_start for cycle in restored.cycles) == (
        date(2026, 8, 3),
        date(2026, 8, 10),
    )
    assert restored.selected_cycle_id == first.cycle_id
    assert restored.next_week_start(date(2026, 8, 5)) == date(2026, 8, 17)


def test_weekly_cycle_requires_monday_identity_and_aware_timestamps() -> None:
    with pytest.raises(ValueError, match="Monday"):
        DM857WeeklyCycle(
            cycle_id="dm857.week.2026-08-04",
            week_start=date(2026, 8, 4),
            updated_at=NOW,
        )

    with pytest.raises(ValueError, match="timezone-aware"):
        DM857WeeklyCycle.empty(WEEK, now=datetime(2026, 8, 5, 8, 0))


def test_weekly_snapshot_rejects_malformed_documents() -> None:
    with pytest.raises(WeeklySupervisionSnapshotError):
        DM857WeeklySupervisionSnapshot.from_json("{not-json")


def test_weekly_record_renders_verifiable_evidence_without_claiming_grade() -> None:
    rendered = render_weekly_cycle_record(_cycle())

    assert "commit-start" in rendered
    assert "8 passed" in rendered
    assert "Individual contribution" in rendered
    assert "grade" not in rendered.casefold()


def test_weekly_store_persists_file_backed_history(tmp_path) -> None:
    database = tmp_path / "learning.sqlite3"
    store = DM857WeeklySupervisionStore(database)
    snapshot = DM857WeeklySupervisionSnapshot.empty(now=NOW).with_cycle(_cycle(), now=NOW)

    store.save(snapshot)
    reopened = DM857WeeklySupervisionStore(database)

    assert reopened.load() == snapshot
    assert reopened.path is not None
    assert reopened.path.exists()


def test_weekly_store_shares_in_memory_progress_store_lifetime() -> None:
    progress_store = SQLiteProgressStore(":memory:")
    first = DM857WeeklySupervisionStore.for_progress_store(progress_store)
    snapshot = DM857WeeklySupervisionSnapshot.empty(now=NOW).with_cycle(_cycle(), now=NOW)
    first.save(snapshot)

    second = DM857WeeklySupervisionStore.for_progress_store(progress_store)

    assert second.load() == snapshot
    progress_store.close()
