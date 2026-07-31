"""Versioned domain model for the DM857 project-and-report preparation workflow."""

from __future__ import annotations

import json
from dataclasses import dataclass, replace
from datetime import UTC, datetime
from enum import StrEnum
from typing import Any

CAPSTONE_SCHEMA_VERSION = 1


class CapstoneSnapshotError(ValueError):
    """Raised when persisted capstone state cannot be validated safely."""


class CapstoneMilestoneStatus(StrEnum):
    """Derived readiness state for one capstone milestone."""

    NOT_STARTED = "not_started"
    IN_PROGRESS = "in_progress"
    READY = "ready"


@dataclass(frozen=True, slots=True)
class CapstoneMilestoneSpec:
    """Stable contract for one evidence-bearing project milestone."""

    milestone_id: str
    checklist_item_ids: tuple[str, ...]
    official_requirement_ids: tuple[str, ...]

    def __post_init__(self) -> None:
        if not self.milestone_id.strip():
            raise ValueError("Capstone milestone IDs cannot be empty.")
        if not self.checklist_item_ids:
            raise ValueError(f"Milestone {self.milestone_id!r} requires checklist items.")
        if len(self.checklist_item_ids) != len(set(self.checklist_item_ids)):
            raise ValueError(f"Milestone {self.milestone_id!r} has duplicate checklist IDs.")
        if not self.official_requirement_ids:
            raise ValueError(f"Milestone {self.milestone_id!r} requires official alignment.")


@dataclass(frozen=True, slots=True)
class CapstoneRubricCriterion:
    """One internal readiness criterion; this is not an official SDU rubric."""

    criterion_id: str
    weight_percent: int
    official_requirement_ids: tuple[str, ...]

    def __post_init__(self) -> None:
        if not self.criterion_id.strip():
            raise ValueError("Capstone rubric criterion IDs cannot be empty.")
        if not 1 <= self.weight_percent <= 100:
            raise ValueError("Capstone rubric weights must be between 1 and 100.")
        if not self.official_requirement_ids:
            raise ValueError(f"Criterion {self.criterion_id!r} requires official alignment.")


DM857_CAPSTONE_MILESTONES: tuple[CapstoneMilestoneSpec, ...] = (
    CapstoneMilestoneSpec(
        "dm857.capstone.m01",
        (
            "dm857.capstone.m01.problem",
            "dm857.capstone.m01.model",
            "dm857.capstone.m01.success",
        ),
        ("dm857.sdu.lo01", "dm857.sdu.lo02"),
    ),
    CapstoneMilestoneSpec(
        "dm857.capstone.m02",
        (
            "dm857.capstone.m02.structure",
            "dm857.capstone.m02.data",
            "dm857.capstone.m02.interfaces",
        ),
        (
            "dm857.sdu.lo02",
            "dm857.sdu.lo07",
            "dm857.sdu.ct03",
            "dm857.sdu.ct05",
        ),
    ),
    CapstoneMilestoneSpec(
        "dm857.capstone.m03",
        (
            "dm857.capstone.m03.implementation",
            "dm857.capstone.m03.library",
            "dm857.capstone.m03.versioned",
        ),
        ("dm857.sdu.lo03", "dm857.sdu.lo04"),
    ),
    CapstoneMilestoneSpec(
        "dm857.capstone.m04",
        (
            "dm857.capstone.m04.plan",
            "dm857.capstone.m04.execute",
            "dm857.capstone.m04.analyse",
        ),
        ("dm857.sdu.lo05", "dm857.sdu.ct03"),
    ),
    CapstoneMilestoneSpec(
        "dm857.capstone.m05",
        (
            "dm857.capstone.m05.traceability",
            "dm857.capstone.m05.limitations",
            "dm857.capstone.m05.page_limit",
        ),
        ("dm857.sdu.exam01",),
    ),
)

DM857_CAPSTONE_RUBRIC: tuple[CapstoneRubricCriterion, ...] = (
    CapstoneRubricCriterion("dm857.capstone.r01", 15, ("dm857.sdu.lo01",)),
    CapstoneRubricCriterion(
        "dm857.capstone.r02",
        15,
        ("dm857.sdu.lo02", "dm857.sdu.lo07"),
    ),
    CapstoneRubricCriterion(
        "dm857.capstone.r03",
        20,
        ("dm857.sdu.lo03", "dm857.sdu.lo04"),
    ),
    CapstoneRubricCriterion("dm857.capstone.r04", 20, ("dm857.sdu.lo05",)),
    CapstoneRubricCriterion("dm857.capstone.r05", 10, ("dm857.sdu.ct03",)),
    CapstoneRubricCriterion("dm857.capstone.r06", 15, ("dm857.sdu.exam01",)),
    CapstoneRubricCriterion("dm857.capstone.r07", 5, ("dm857.sdu.exam01",)),
)

if sum(item.weight_percent for item in DM857_CAPSTONE_RUBRIC) != 100:
    raise ValueError("The DM857 capstone readiness rubric must total 100 percent.")

_MILESTONE_BY_ID = {item.milestone_id: item for item in DM857_CAPSTONE_MILESTONES}
_RUBRIC_BY_ID = {item.criterion_id: item for item in DM857_CAPSTONE_RUBRIC}


@dataclass(frozen=True, slots=True)
class CapstoneMilestoneProgress:
    """Learner evidence attached to one stable capstone milestone."""

    milestone_id: str
    completed_item_ids: tuple[str, ...] = ()
    evidence_note: str = ""
    commit_reference: str = ""

    def __post_init__(self) -> None:
        spec = _MILESTONE_BY_ID.get(self.milestone_id)
        if spec is None:
            raise ValueError(f"Unknown capstone milestone {self.milestone_id!r}.")
        if len(self.completed_item_ids) != len(set(self.completed_item_ids)):
            raise ValueError(f"Milestone {self.milestone_id!r} has duplicate completed items.")
        unknown = set(self.completed_item_ids) - set(spec.checklist_item_ids)
        if unknown:
            raise ValueError(
                f"Milestone {self.milestone_id!r} references unknown checklist items: "
                + ", ".join(sorted(unknown))
            )

    @property
    def status(self) -> CapstoneMilestoneStatus:
        """Derive readiness from checklist completion and repository evidence."""

        spec = _MILESTONE_BY_ID[self.milestone_id]
        has_any = bool(
            self.completed_item_ids or self.evidence_note.strip() or self.commit_reference.strip()
        )
        if not has_any:
            return CapstoneMilestoneStatus.NOT_STARTED
        if (
            set(self.completed_item_ids) == set(spec.checklist_item_ids)
            and self.evidence_note.strip()
            and self.commit_reference.strip()
        ):
            return CapstoneMilestoneStatus.READY
        return CapstoneMilestoneStatus.IN_PROGRESS


@dataclass(frozen=True, slots=True)
class DM857CapstoneProgress:
    """Complete local state for one DM857 group-project preparation workflow."""

    schema_version: int
    project_title: str
    group_members: tuple[str, ...]
    repository_url: str
    report_path: str
    milestones: tuple[CapstoneMilestoneProgress, ...]
    rubric_scores: tuple[tuple[str, int], ...]
    updated_at: datetime

    def __post_init__(self) -> None:
        if self.schema_version != CAPSTONE_SCHEMA_VERSION:
            raise ValueError(
                f"Unsupported capstone schema {self.schema_version}; "
                f"expected {CAPSTONE_SCHEMA_VERSION}."
            )
        _require_aware(self.updated_at, "updated_at")
        expected_milestones = tuple(item.milestone_id for item in DM857_CAPSTONE_MILESTONES)
        if tuple(item.milestone_id for item in self.milestones) != expected_milestones:
            raise ValueError(
                "Capstone milestone progress must preserve the authored milestone order."
            )

        member_keys = tuple(item.strip().casefold() for item in self.group_members)
        if any(not item for item in member_keys):
            raise ValueError("Capstone group members cannot be empty.")
        if len(member_keys) != len(set(member_keys)):
            raise ValueError("Capstone group members cannot be duplicated.")

        criterion_ids = tuple(item[0] for item in self.rubric_scores)
        if len(criterion_ids) != len(set(criterion_ids)):
            raise ValueError("Capstone rubric scores cannot contain duplicate criteria.")
        unknown = set(criterion_ids) - set(_RUBRIC_BY_ID)
        if unknown:
            raise ValueError(
                "Capstone rubric scores reference unknown criteria: " + ", ".join(sorted(unknown))
            )
        for criterion_id, score in self.rubric_scores:
            if not 0 <= score <= 4:
                raise ValueError(f"Criterion {criterion_id!r} requires a score from 0 to 4.")

    @classmethod
    def empty(cls, *, now: datetime | None = None) -> DM857CapstoneProgress:
        """Create a validated empty project state."""

        return cls(
            schema_version=CAPSTONE_SCHEMA_VERSION,
            project_title="",
            group_members=(),
            repository_url="",
            report_path="",
            milestones=tuple(
                CapstoneMilestoneProgress(item.milestone_id) for item in DM857_CAPSTONE_MILESTONES
            ),
            rubric_scores=(),
            updated_at=now or datetime.now(UTC),
        )

    def with_metadata(
        self,
        *,
        project_title: str,
        group_members: tuple[str, ...],
        repository_url: str,
        report_path: str,
        now: datetime | None = None,
    ) -> DM857CapstoneProgress:
        """Replace project metadata while preserving evidence and scores."""

        members = tuple(item.strip() for item in group_members if item.strip())
        return replace(
            self,
            project_title=project_title.strip(),
            group_members=members,
            repository_url=repository_url.strip(),
            report_path=report_path.strip(),
            updated_at=now or datetime.now(UTC),
        )

    def with_milestone(
        self,
        milestone: CapstoneMilestoneProgress,
        *,
        now: datetime | None = None,
    ) -> DM857CapstoneProgress:
        """Replace one milestone by stable ID."""

        if milestone.milestone_id not in _MILESTONE_BY_ID:
            raise ValueError(f"Unknown capstone milestone {milestone.milestone_id!r}.")
        updated = tuple(
            milestone if item.milestone_id == milestone.milestone_id else item
            for item in self.milestones
        )
        return replace(
            self,
            milestones=updated,
            updated_at=now or datetime.now(UTC),
        )

    def with_rubric_score(
        self,
        criterion_id: str,
        score: int | None,
        *,
        now: datetime | None = None,
    ) -> DM857CapstoneProgress:
        """Set or clear one internal readiness score."""

        if criterion_id not in _RUBRIC_BY_ID:
            raise ValueError(f"Unknown capstone rubric criterion {criterion_id!r}.")
        scores = dict(self.rubric_scores)
        if score is None:
            scores.pop(criterion_id, None)
        else:
            if not 0 <= score <= 4:
                raise ValueError("Capstone rubric scores must be between 0 and 4.")
            scores[criterion_id] = score
        ordered = tuple(
            (item.criterion_id, scores[item.criterion_id])
            for item in DM857_CAPSTONE_RUBRIC
            if item.criterion_id in scores
        )
        return replace(
            self,
            rubric_scores=ordered,
            updated_at=now or datetime.now(UTC),
        )

    def milestone(self, milestone_id: str) -> CapstoneMilestoneProgress:
        """Return one milestone progress record by stable ID."""

        return next(item for item in self.milestones if item.milestone_id == milestone_id)

    def rubric_score(self, criterion_id: str) -> int | None:
        """Return one internal readiness score when self-assessed."""

        return dict(self.rubric_scores).get(criterion_id)

    @property
    def ready_milestone_count(self) -> int:
        return sum(item.status is CapstoneMilestoneStatus.READY for item in self.milestones)

    @property
    def milestone_completion_percent(self) -> int:
        return round(100 * self.ready_milestone_count / len(self.milestones))

    @property
    def weighted_rubric_percent(self) -> int | None:
        """Return weighted self-assessment after every criterion is scored."""

        scores = dict(self.rubric_scores)
        if set(scores) != set(_RUBRIC_BY_ID):
            return None
        weighted = sum(
            scores[item.criterion_id] / 4 * item.weight_percent for item in DM857_CAPSTONE_RUBRIC
        )
        return round(weighted)

    @property
    def preparation_ready(self) -> bool:
        """Return whether the internal scaffold has complete preparation evidence."""

        return bool(
            self.project_title.strip()
            and self.group_members
            and self.repository_url.strip()
            and self.report_path.strip()
            and self.ready_milestone_count == len(self.milestones)
            and self.weighted_rubric_percent is not None
        )

    def to_json(self) -> str:
        """Serialize validated state to canonical JSON."""

        payload: dict[str, Any] = {
            "schema_version": self.schema_version,
            "project_title": self.project_title,
            "group_members": list(self.group_members),
            "repository_url": self.repository_url,
            "report_path": self.report_path,
            "milestones": [
                {
                    "milestone_id": item.milestone_id,
                    "completed_item_ids": list(item.completed_item_ids),
                    "evidence_note": item.evidence_note,
                    "commit_reference": item.commit_reference,
                }
                for item in self.milestones
            ],
            "rubric_scores": [
                {"criterion_id": criterion_id, "score": score}
                for criterion_id, score in self.rubric_scores
            ],
            "updated_at": self.updated_at.isoformat(),
        }
        return json.dumps(
            payload,
            ensure_ascii=False,
            sort_keys=True,
            separators=(",", ":"),
        )

    @classmethod
    def from_json(cls, document: str) -> DM857CapstoneProgress:
        """Parse and validate one persisted document defensively."""

        try:
            payload = json.loads(document)
            if not isinstance(payload, dict):
                raise TypeError("Capstone document root must be an object.")
            raw_milestones = payload["milestones"]
            raw_scores = payload["rubric_scores"]
            if not isinstance(raw_milestones, list) or not isinstance(raw_scores, list):
                raise TypeError("Capstone milestones and rubric scores must be arrays.")
            milestones = tuple(
                CapstoneMilestoneProgress(
                    milestone_id=_required_string(item, "milestone_id"),
                    completed_item_ids=tuple(_required_string_list(item, "completed_item_ids")),
                    evidence_note=_required_string(
                        item,
                        "evidence_note",
                        allow_empty=True,
                    ),
                    commit_reference=_required_string(
                        item,
                        "commit_reference",
                        allow_empty=True,
                    ),
                )
                for item in raw_milestones
            )
            rubric_scores = tuple(
                (
                    _required_string(item, "criterion_id"),
                    _required_int(item, "score"),
                )
                for item in raw_scores
            )
            return cls(
                schema_version=_required_int(payload, "schema_version"),
                project_title=_required_string(
                    payload,
                    "project_title",
                    allow_empty=True,
                ),
                group_members=tuple(_required_string_list(payload, "group_members")),
                repository_url=_required_string(
                    payload,
                    "repository_url",
                    allow_empty=True,
                ),
                report_path=_required_string(payload, "report_path", allow_empty=True),
                milestones=milestones,
                rubric_scores=rubric_scores,
                updated_at=datetime.fromisoformat(_required_string(payload, "updated_at")),
            )
        except (KeyError, TypeError, ValueError) as exc:
            raise CapstoneSnapshotError("Invalid DM857 capstone document.") from exc


def _required_string(
    payload: object,
    key: str,
    *,
    allow_empty: bool = False,
) -> str:
    if not isinstance(payload, dict):
        raise TypeError("Expected an object.")
    value = payload[key]
    if not isinstance(value, str):
        raise TypeError(f"{key!r} must be a string.")
    if not allow_empty and not value.strip():
        raise ValueError(f"{key!r} cannot be empty.")
    return value


def _required_int(payload: object, key: str) -> int:
    if not isinstance(payload, dict):
        raise TypeError("Expected an object.")
    value = payload[key]
    if isinstance(value, bool) or not isinstance(value, int):
        raise TypeError(f"{key!r} must be an integer.")
    return value


def _required_string_list(payload: object, key: str) -> list[str]:
    if not isinstance(payload, dict):
        raise TypeError("Expected an object.")
    value = payload[key]
    if not isinstance(value, list) or not all(isinstance(item, str) for item in value):
        raise TypeError(f"{key!r} must be an array of strings.")
    return value


def _require_aware(value: datetime, name: str) -> None:
    if value.tzinfo is None or value.utcoffset() is None:
        raise ValueError(f"{name} must be timezone-aware.")


__all__ = [
    "CAPSTONE_SCHEMA_VERSION",
    "DM857_CAPSTONE_MILESTONES",
    "DM857_CAPSTONE_RUBRIC",
    "CapstoneMilestoneProgress",
    "CapstoneMilestoneSpec",
    "CapstoneMilestoneStatus",
    "CapstoneRubricCriterion",
    "CapstoneSnapshotError",
    "DM857CapstoneProgress",
]
