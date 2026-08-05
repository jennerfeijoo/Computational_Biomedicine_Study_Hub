"""Versioned longitudinal supervision model for the DM857 group project."""

from __future__ import annotations

import json
from dataclasses import dataclass, replace
from datetime import UTC, date, datetime, timedelta
from enum import StrEnum
from typing import Any

WEEKLY_SUPERVISION_SCHEMA_VERSION = 1


class WeeklySupervisionSnapshotError(ValueError):
    """Raised when persisted weekly-supervision state is malformed."""


class WeeklyCycleStatus(StrEnum):
    """Derived state of one evidence-bearing weekly project cycle."""

    EMPTY = "empty"
    PLANNED = "planned"
    ACTIVE = "active"
    BLOCKED = "blocked"
    COMPLETE = "complete"


_REQUIRED_FIELD_NAMES: tuple[str, ...] = (
    "objective",
    "success_criteria",
    "start_reference",
    "end_reference",
    "test_evidence",
    "decision_rationale",
    "individual_contribution",
    "reflection",
    "next_commitment",
)

_EXECUTION_FIELD_NAMES: tuple[str, ...] = (
    "start_reference",
    "end_reference",
    "changed_files",
    "test_evidence",
    "decision_rationale",
    "individual_contribution",
    "biomedical_interpretation",
    "blockers",
    "reflection",
    "next_commitment",
)


@dataclass(frozen=True, slots=True)
class DM857WeeklyCycle:
    """One weekly plan-execute-review loop grounded in repository evidence."""

    cycle_id: str
    week_start: date
    objective: str = ""
    success_criteria: str = ""
    start_reference: str = ""
    end_reference: str = ""
    changed_files: str = ""
    test_evidence: str = ""
    decision_rationale: str = ""
    individual_contribution: str = ""
    biomedical_interpretation: str = ""
    blockers: str = ""
    reflection: str = ""
    next_commitment: str = ""
    blocked: bool = False
    updated_at: datetime = datetime.min.replace(tzinfo=UTC)

    def __post_init__(self) -> None:
        expected_id = cycle_id_for(self.week_start)
        if self.cycle_id != expected_id:
            raise ValueError(
                f"Weekly cycle ID {self.cycle_id!r} does not match {expected_id!r}."
            )
        if self.week_start.weekday() != 0:
            raise ValueError("DM857 weekly cycles must start on a Monday.")
        _require_aware(self.updated_at, "updated_at")

    @classmethod
    def empty(
        cls,
        week_start: date,
        *,
        now: datetime | None = None,
    ) -> DM857WeeklyCycle:
        """Create one empty cycle for a validated Monday."""

        monday = monday_for(week_start)
        return cls(
            cycle_id=cycle_id_for(monday),
            week_start=monday,
            updated_at=now or datetime.now(UTC),
        )

    def with_fields(
        self,
        *,
        objective: str,
        success_criteria: str,
        start_reference: str,
        end_reference: str,
        changed_files: str,
        test_evidence: str,
        decision_rationale: str,
        individual_contribution: str,
        biomedical_interpretation: str,
        blockers: str,
        reflection: str,
        next_commitment: str,
        blocked: bool,
        now: datetime | None = None,
    ) -> DM857WeeklyCycle:
        """Replace learner-owned evidence while preserving stable cycle identity."""

        return replace(
            self,
            objective=objective.strip(),
            success_criteria=success_criteria.strip(),
            start_reference=start_reference.strip(),
            end_reference=end_reference.strip(),
            changed_files=changed_files.strip(),
            test_evidence=test_evidence.strip(),
            decision_rationale=decision_rationale.strip(),
            individual_contribution=individual_contribution.strip(),
            biomedical_interpretation=biomedical_interpretation.strip(),
            blockers=blockers.strip(),
            reflection=reflection.strip(),
            next_commitment=next_commitment.strip(),
            blocked=blocked,
            updated_at=now or datetime.now(UTC),
        )

    @property
    def required_evidence_count(self) -> int:
        """Return how many completion-bearing fields contain evidence."""

        return sum(bool(getattr(self, field_name).strip()) for field_name in _REQUIRED_FIELD_NAMES)

    @property
    def completion_percent(self) -> int:
        """Return transparent evidence completeness, not academic mastery."""

        return round(100 * self.required_evidence_count / len(_REQUIRED_FIELD_NAMES))

    @property
    def status(self) -> WeeklyCycleStatus:
        """Derive cycle state without assigning an academic grade."""

        has_any_text = any(
            bool(getattr(self, field_name).strip())
            for field_name in (*_REQUIRED_FIELD_NAMES, "changed_files", "biomedical_interpretation", "blockers")
        )
        if not has_any_text and not self.blocked:
            return WeeklyCycleStatus.EMPTY
        if self.blocked:
            return WeeklyCycleStatus.BLOCKED
        if self.required_evidence_count == len(_REQUIRED_FIELD_NAMES):
            return WeeklyCycleStatus.COMPLETE
        has_execution_evidence = any(
            bool(getattr(self, field_name).strip()) for field_name in _EXECUTION_FIELD_NAMES
        )
        if has_execution_evidence:
            return WeeklyCycleStatus.ACTIVE
        return WeeklyCycleStatus.PLANNED


@dataclass(frozen=True, slots=True)
class DM857WeeklySupervisionSnapshot:
    """Ordered local history of weekly DM857 supervision cycles."""

    schema_version: int
    cycles: tuple[DM857WeeklyCycle, ...]
    selected_cycle_id: str | None
    updated_at: datetime

    def __post_init__(self) -> None:
        if self.schema_version != WEEKLY_SUPERVISION_SCHEMA_VERSION:
            raise ValueError(
                f"Unsupported weekly supervision schema {self.schema_version}; "
                f"expected {WEEKLY_SUPERVISION_SCHEMA_VERSION}."
            )
        _require_aware(self.updated_at, "updated_at")
        cycle_ids = tuple(cycle.cycle_id for cycle in self.cycles)
        if len(cycle_ids) != len(set(cycle_ids)):
            raise ValueError("Weekly supervision cycles cannot contain duplicate IDs.")
        if tuple(sorted(cycle.week_start for cycle in self.cycles)) != tuple(
            cycle.week_start for cycle in self.cycles
        ):
            raise ValueError("Weekly supervision cycles must be ordered chronologically.")
        if self.selected_cycle_id is not None and self.selected_cycle_id not in set(cycle_ids):
            raise ValueError("Selected weekly cycle must exist in the snapshot.")

    @classmethod
    def empty(
        cls,
        *,
        now: datetime | None = None,
    ) -> DM857WeeklySupervisionSnapshot:
        """Create an empty validated history."""

        timestamp = now or datetime.now(UTC)
        return cls(
            schema_version=WEEKLY_SUPERVISION_SCHEMA_VERSION,
            cycles=(),
            selected_cycle_id=None,
            updated_at=timestamp,
        )

    def cycle(self, cycle_id: str) -> DM857WeeklyCycle:
        """Return a cycle by stable ID."""

        return next(cycle for cycle in self.cycles if cycle.cycle_id == cycle_id)

    @property
    def selected_cycle(self) -> DM857WeeklyCycle | None:
        """Return the selected cycle when one exists."""

        if self.selected_cycle_id is None:
            return None
        return self.cycle(self.selected_cycle_id)

    def with_cycle(
        self,
        cycle: DM857WeeklyCycle,
        *,
        select: bool = True,
        now: datetime | None = None,
    ) -> DM857WeeklySupervisionSnapshot:
        """Insert or replace one cycle and preserve chronological order."""

        cycles_by_id = {item.cycle_id: item for item in self.cycles}
        cycles_by_id[cycle.cycle_id] = cycle
        ordered = tuple(sorted(cycles_by_id.values(), key=lambda item: item.week_start))
        selected = cycle.cycle_id if select else self.selected_cycle_id
        return replace(
            self,
            cycles=ordered,
            selected_cycle_id=selected,
            updated_at=now or datetime.now(UTC),
        )

    def select(
        self,
        cycle_id: str,
        *,
        now: datetime | None = None,
    ) -> DM857WeeklySupervisionSnapshot:
        """Select an existing cycle for editing and mentor context."""

        self.cycle(cycle_id)
        return replace(
            self,
            selected_cycle_id=cycle_id,
            updated_at=now or datetime.now(UTC),
        )

    def next_week_start(self, today: date) -> date:
        """Choose the current or next unused Monday."""

        current_monday = monday_for(today)
        if not self.cycles:
            return current_monday
        latest = self.cycles[-1].week_start
        return current_monday if current_monday > latest else latest + timedelta(days=7)

    def to_json(self) -> str:
        """Serialize the complete validated history to canonical JSON."""

        payload: dict[str, Any] = {
            "schema_version": self.schema_version,
            "cycles": [_cycle_payload(cycle) for cycle in self.cycles],
            "selected_cycle_id": self.selected_cycle_id,
            "updated_at": self.updated_at.isoformat(),
        }
        return json.dumps(
            payload,
            ensure_ascii=False,
            sort_keys=True,
            separators=(",", ":"),
        )

    @classmethod
    def from_json(cls, document: str) -> DM857WeeklySupervisionSnapshot:
        """Parse persisted state defensively and reject partial corruption."""

        try:
            payload = json.loads(document)
            if not isinstance(payload, dict):
                raise TypeError("Weekly supervision document root must be an object.")
            raw_cycles = payload["cycles"]
            if not isinstance(raw_cycles, list):
                raise TypeError("Weekly supervision cycles must be an array.")
            selected = payload["selected_cycle_id"]
            if selected is not None and not isinstance(selected, str):
                raise TypeError("Selected weekly cycle ID must be a string or null.")
            return cls(
                schema_version=_required_int(payload, "schema_version"),
                cycles=tuple(_cycle_from_payload(item) for item in raw_cycles),
                selected_cycle_id=selected,
                updated_at=_required_datetime(payload, "updated_at"),
            )
        except (
            json.JSONDecodeError,
            KeyError,
            TypeError,
            ValueError,
        ) as error:
            raise WeeklySupervisionSnapshotError(
                f"Invalid DM857 weekly supervision snapshot: {error}"
            ) from error


def monday_for(day: date) -> date:
    """Return the Monday containing ``day``."""

    return day - timedelta(days=day.weekday())


def cycle_id_for(week_start: date) -> str:
    """Return the stable identity for a Monday-based weekly cycle."""

    return f"dm857.week.{week_start.isoformat()}"


def render_weekly_cycle_record(cycle: DM857WeeklyCycle) -> str:
    """Render a portable Markdown record owned by the learner."""

    fields = (
        ("Objective", cycle.objective),
        ("Success criteria", cycle.success_criteria),
        ("Start reference", cycle.start_reference),
        ("End reference", cycle.end_reference),
        ("Changed files or components", cycle.changed_files),
        ("Test evidence", cycle.test_evidence),
        ("Decision rationale", cycle.decision_rationale),
        ("Individual contribution", cycle.individual_contribution),
        ("Biomedical interpretation", cycle.biomedical_interpretation),
        ("Blockers", cycle.blockers),
        ("Reflection", cycle.reflection),
        ("Next commitment", cycle.next_commitment),
    )
    sections = [
        f"# DM857 weekly supervision — {cycle.week_start.isoformat()}",
        "",
        f"Status: {cycle.status.value}",
        f"Evidence completeness: {cycle.completion_percent}%",
        f"Blocked: {'yes' if cycle.blocked else 'no'}",
    ]
    for heading, value in fields:
        sections.extend(("", f"## {heading}", value.strip() or "[not recorded]"))
    return "\n".join(sections).strip() + "\n"


def _cycle_payload(cycle: DM857WeeklyCycle) -> dict[str, Any]:
    return {
        "cycle_id": cycle.cycle_id,
        "week_start": cycle.week_start.isoformat(),
        "objective": cycle.objective,
        "success_criteria": cycle.success_criteria,
        "start_reference": cycle.start_reference,
        "end_reference": cycle.end_reference,
        "changed_files": cycle.changed_files,
        "test_evidence": cycle.test_evidence,
        "decision_rationale": cycle.decision_rationale,
        "individual_contribution": cycle.individual_contribution,
        "biomedical_interpretation": cycle.biomedical_interpretation,
        "blockers": cycle.blockers,
        "reflection": cycle.reflection,
        "next_commitment": cycle.next_commitment,
        "blocked": cycle.blocked,
        "updated_at": cycle.updated_at.isoformat(),
    }


def _cycle_from_payload(value: object) -> DM857WeeklyCycle:
    if not isinstance(value, dict):
        raise TypeError("Each weekly cycle must be an object.")
    return DM857WeeklyCycle(
        cycle_id=_required_string(value, "cycle_id"),
        week_start=_required_date(value, "week_start"),
        objective=_required_string(value, "objective", allow_empty=True),
        success_criteria=_required_string(value, "success_criteria", allow_empty=True),
        start_reference=_required_string(value, "start_reference", allow_empty=True),
        end_reference=_required_string(value, "end_reference", allow_empty=True),
        changed_files=_required_string(value, "changed_files", allow_empty=True),
        test_evidence=_required_string(value, "test_evidence", allow_empty=True),
        decision_rationale=_required_string(value, "decision_rationale", allow_empty=True),
        individual_contribution=_required_string(
            value,
            "individual_contribution",
            allow_empty=True,
        ),
        biomedical_interpretation=_required_string(
            value,
            "biomedical_interpretation",
            allow_empty=True,
        ),
        blockers=_required_string(value, "blockers", allow_empty=True),
        reflection=_required_string(value, "reflection", allow_empty=True),
        next_commitment=_required_string(value, "next_commitment", allow_empty=True),
        blocked=_required_bool(value, "blocked"),
        updated_at=_required_datetime(value, "updated_at"),
    )


def _required_string(
    payload: dict[str, Any],
    key: str,
    *,
    allow_empty: bool = False,
) -> str:
    value = payload[key]
    if not isinstance(value, str):
        raise TypeError(f"{key} must be a string.")
    if not allow_empty and not value.strip():
        raise ValueError(f"{key} cannot be empty.")
    return value


def _required_int(payload: dict[str, Any], key: str) -> int:
    value = payload[key]
    if isinstance(value, bool) or not isinstance(value, int):
        raise TypeError(f"{key} must be an integer.")
    return value


def _required_bool(payload: dict[str, Any], key: str) -> bool:
    value = payload[key]
    if not isinstance(value, bool):
        raise TypeError(f"{key} must be a boolean.")
    return value


def _required_date(payload: dict[str, Any], key: str) -> date:
    value = _required_string(payload, key)
    return date.fromisoformat(value)


def _required_datetime(payload: dict[str, Any], key: str) -> datetime:
    value = datetime.fromisoformat(_required_string(payload, key))
    _require_aware(value, key)
    return value


def _require_aware(value: datetime, field_name: str) -> None:
    if value.tzinfo is None or value.utcoffset() is None:
        raise ValueError(f"{field_name} must be timezone-aware.")


__all__ = [
    "DM857WeeklyCycle",
    "DM857WeeklySupervisionSnapshot",
    "WeeklyCycleStatus",
    "WeeklySupervisionSnapshotError",
    "cycle_id_for",
    "monday_for",
    "render_weekly_cycle_record",
]
