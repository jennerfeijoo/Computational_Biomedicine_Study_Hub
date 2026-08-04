"""Artifact-based technical reasoning stations and learner-owned evidence."""

from __future__ import annotations

import json
from dataclasses import dataclass, replace
from datetime import UTC, datetime
from enum import StrEnum
from typing import cast

from ..i18n.locales import AppLocale
from .computational_labs import LocalizedText

TECHNICAL_STATION_SCHEMA_VERSION = 1
MAX_STATION_RESPONSE_LENGTH = 40_000


class TechnicalStationSnapshotError(ValueError):
    """Raised when persisted technical-station evidence is malformed."""


class TechnicalStationKind(StrEnum):
    """Stable forms of artifact-based technical reasoning practice."""

    CODE_READING = "code_reading"
    EXECUTION_TRACE = "execution_trace"
    DEBUGGING = "debugging"
    OUTPUT_INTERPRETATION = "output_interpretation"
    METHOD_SELECTION = "method_selection"
    COMPLEXITY_ANALYSIS = "complexity_analysis"
    SCIENTIFIC_INTERPRETATION = "scientific_interpretation"
    PROJECT_REASONING = "project_reasoning"


@dataclass(frozen=True, slots=True)
class TechnicalStationCriterion:
    """One explicit element used for learner self-review, not automatic grading."""

    criterion_id: str
    text: LocalizedText

    def __post_init__(self) -> None:
        if not self.criterion_id.strip():
            raise ValueError("Technical-station criteria require stable identities.")


@dataclass(frozen=True, slots=True)
class TechnicalStation:
    """One bounded task centred on code, output, trace, or scientific evidence."""

    station_id: str
    course_code: str
    lab_id: str
    kind: TechnicalStationKind
    title: LocalizedText
    artifact_title: LocalizedText
    artifact: str
    prompt: LocalizedText
    criteria: tuple[TechnicalStationCriterion, ...]
    estimated_minutes: int
    source_basis: tuple[str, ...]
    minimum_response_chars: int = 80

    def __post_init__(self) -> None:
        if not self.station_id.strip() or not self.course_code.strip() or not self.lab_id.strip():
            raise ValueError("Technical stations require station, course, and laboratory identities.")
        if not self.artifact.strip():
            raise ValueError("Technical stations require a concrete artifact.")
        if not 2 <= len(self.criteria) <= 8:
            raise ValueError("Technical stations require between two and eight review criteria.")
        criterion_ids = tuple(item.criterion_id for item in self.criteria)
        if len(criterion_ids) != len(set(criterion_ids)):
            raise ValueError("Technical-station criterion identities cannot be duplicated.")
        if not 3 <= self.estimated_minutes <= 60:
            raise ValueError("Technical-station duration must be between 3 and 60 minutes.")
        if not self.source_basis or any(not item.strip() for item in self.source_basis):
            raise ValueError("Technical stations require an explicit authored source basis.")
        if not 40 <= self.minimum_response_chars <= 2_000:
            raise ValueError("Technical-station minimum response must be between 40 and 2000 chars.")

    def criterion(self, criterion_id: str) -> TechnicalStationCriterion:
        """Return one review criterion by stable identity."""

        try:
            return next(item for item in self.criteria if item.criterion_id == criterion_id)
        except StopIteration as exc:
            raise ValueError(f"Unknown technical-station criterion {criterion_id!r}.") from exc


@dataclass(frozen=True, slots=True)
class TechnicalStationAttempt:
    """Learner response and explicit self-review evidence for one station."""

    station_id: str
    response: str
    checked_criteria: frozenset[str]
    hint_level: int
    reviewed: bool
    started_at: datetime
    updated_at: datetime
    reviewed_at: datetime | None = None

    def __post_init__(self) -> None:
        if not self.station_id.strip():
            raise ValueError("Technical-station attempts require a station identity.")
        if len(self.response) > MAX_STATION_RESPONSE_LENGTH:
            raise ValueError("Technical-station response exceeds the local storage limit.")
        if not 0 <= self.hint_level <= 6:
            raise ValueError("Technical-station hint level must be between zero and six.")
        for timestamp in (self.started_at, self.updated_at):
            if timestamp.tzinfo is None or timestamp.utcoffset() is None:
                raise ValueError("Technical-station timestamps must be timezone-aware.")
        if self.reviewed_at is not None and (
            self.reviewed_at.tzinfo is None or self.reviewed_at.utcoffset() is None
        ):
            raise ValueError("Technical-station review timestamp must be timezone-aware.")
        if self.updated_at < self.started_at:
            raise ValueError("Technical-station attempt cannot update before it starts.")
        if self.reviewed and self.reviewed_at is None:
            raise ValueError("Reviewed technical-station attempts require a review timestamp.")
        if not self.reviewed and self.reviewed_at is not None:
            raise ValueError("Unreviewed technical-station attempts cannot have a review timestamp.")

    @classmethod
    def new(
        cls,
        station: TechnicalStation,
        *,
        now: datetime | None = None,
    ) -> TechnicalStationAttempt:
        timestamp = now or datetime.now(UTC)
        return cls(
            station_id=station.station_id,
            response="",
            checked_criteria=frozenset(),
            hint_level=0,
            reviewed=False,
            started_at=timestamp,
            updated_at=timestamp,
        )

    def with_response(
        self,
        response: str,
        *,
        now: datetime | None = None,
    ) -> TechnicalStationAttempt:
        """Replace the answer and invalidate stale self-review evidence."""

        if len(response) > MAX_STATION_RESPONSE_LENGTH:
            raise ValueError("Technical-station response exceeds the local storage limit.")
        return replace(
            self,
            response=response,
            checked_criteria=frozenset(),
            reviewed=False,
            reviewed_at=None,
            updated_at=now or datetime.now(UTC),
        )

    def with_criterion(
        self,
        criterion_id: str,
        checked: bool,
        *,
        now: datetime | None = None,
    ) -> TechnicalStationAttempt:
        checks = set(self.checked_criteria)
        if checked:
            checks.add(criterion_id)
        else:
            checks.discard(criterion_id)
        return replace(
            self,
            checked_criteria=frozenset(checks),
            reviewed=False,
            reviewed_at=None,
            updated_at=now or datetime.now(UTC),
        )

    def with_requested_hint(
        self,
        *,
        now: datetime | None = None,
    ) -> TechnicalStationAttempt:
        return replace(
            self,
            hint_level=min(6, self.hint_level + 1),
            updated_at=now or datetime.now(UTC),
        )

    def mark_reviewed(
        self,
        station: TechnicalStation,
        *,
        now: datetime | None = None,
    ) -> TechnicalStationAttempt:
        """Record completion only after a substantive answer and explicit self-check."""

        if self.station_id != station.station_id:
            raise ValueError("Technical station and attempt identities must match.")
        if len(self.response.strip()) < station.minimum_response_chars:
            raise ValueError("Technical-station response is not yet substantive enough.")
        expected = {item.criterion_id for item in station.criteria}
        if self.checked_criteria != expected:
            raise ValueError("Every technical-station review criterion must be checked.")
        timestamp = now or datetime.now(UTC)
        return replace(self, reviewed=True, reviewed_at=timestamp, updated_at=timestamp)

    def to_dict(self) -> dict[str, object]:
        return {
            "station_id": self.station_id,
            "response": self.response,
            "checked_criteria": sorted(self.checked_criteria),
            "hint_level": self.hint_level,
            "reviewed": self.reviewed,
            "started_at": self.started_at.isoformat(),
            "updated_at": self.updated_at.isoformat(),
            "reviewed_at": self.reviewed_at.isoformat() if self.reviewed_at else None,
        }

    @classmethod
    def from_dict(cls, payload: dict[str, object]) -> TechnicalStationAttempt:
        try:
            station_id = _required_text(payload.get("station_id"), "station ID")
            response = payload.get("response", "")
            raw_checks = payload.get("checked_criteria", [])
            hint_level = payload.get("hint_level", 0)
            reviewed = payload.get("reviewed", False)
            reviewed_at_raw = payload.get("reviewed_at")
            if not isinstance(response, str):
                raise TechnicalStationSnapshotError("Technical-station response must be text.")
            if not isinstance(raw_checks, list) or not all(
                isinstance(item, str) and item.strip() for item in raw_checks
            ):
                raise TechnicalStationSnapshotError(
                    "Technical-station checked criteria must be text identities."
                )
            if isinstance(hint_level, bool) or not isinstance(hint_level, int):
                raise TechnicalStationSnapshotError("Technical-station hint level must be integer.")
            if not isinstance(reviewed, bool):
                raise TechnicalStationSnapshotError("Technical-station reviewed flag must be boolean.")
            if reviewed_at_raw is not None and not isinstance(reviewed_at_raw, str):
                raise TechnicalStationSnapshotError(
                    "Technical-station review timestamp must be text or null."
                )
            return cls(
                station_id=station_id,
                response=response,
                checked_criteria=frozenset(raw_checks),
                hint_level=hint_level,
                reviewed=reviewed,
                started_at=datetime.fromisoformat(
                    _required_text(payload.get("started_at"), "start timestamp")
                ),
                updated_at=datetime.fromisoformat(
                    _required_text(payload.get("updated_at"), "update timestamp")
                ),
                reviewed_at=(
                    datetime.fromisoformat(reviewed_at_raw)
                    if isinstance(reviewed_at_raw, str)
                    else None
                ),
            )
        except (TypeError, ValueError) as exc:
            if isinstance(exc, TechnicalStationSnapshotError):
                raise
            raise TechnicalStationSnapshotError(str(exc)) from exc


@dataclass(frozen=True, slots=True)
class TechnicalStationSnapshot:
    """Versioned collection of artifact-based reasoning attempts."""

    attempts: tuple[TechnicalStationAttempt, ...] = ()
    schema_version: int = TECHNICAL_STATION_SCHEMA_VERSION

    def __post_init__(self) -> None:
        if self.schema_version != TECHNICAL_STATION_SCHEMA_VERSION:
            raise ValueError("Unsupported technical-station schema version.")
        station_ids = tuple(item.station_id for item in self.attempts)
        if len(station_ids) != len(set(station_ids)):
            raise ValueError("Technical-station snapshot requires one attempt per station.")

    def attempt_for(self, station: TechnicalStation) -> TechnicalStationAttempt:
        existing = next(
            (item for item in self.attempts if item.station_id == station.station_id),
            None,
        )
        return existing if existing is not None else TechnicalStationAttempt.new(station)

    def with_attempt(self, attempt: TechnicalStationAttempt) -> TechnicalStationSnapshot:
        remaining = tuple(item for item in self.attempts if item.station_id != attempt.station_id)
        return TechnicalStationSnapshot((*remaining, attempt), self.schema_version)

    def completion_ratio(self, stations: tuple[TechnicalStation, ...]) -> float:
        if not stations:
            return 0.0
        reviewed = {item.station_id for item in self.attempts if item.reviewed}
        return len(reviewed & {item.station_id for item in stations}) / len(stations)

    def to_json(self) -> str:
        return json.dumps(
            {
                "schema_version": self.schema_version,
                "attempts": [item.to_dict() for item in self.attempts],
            },
            ensure_ascii=False,
            indent=2,
            sort_keys=True,
        )

    @classmethod
    def from_json(cls, serialized: str) -> TechnicalStationSnapshot:
        try:
            raw = json.loads(serialized)
        except json.JSONDecodeError as exc:
            raise TechnicalStationSnapshotError(
                "Technical-station snapshot is not valid JSON."
            ) from exc
        if not isinstance(raw, dict):
            raise TechnicalStationSnapshotError("Technical-station snapshot root must be object.")
        version = raw.get("schema_version")
        attempts = raw.get("attempts")
        if isinstance(version, bool) or not isinstance(version, int):
            raise TechnicalStationSnapshotError(
                "Technical-station schema version must be integer."
            )
        if not isinstance(attempts, list) or not all(isinstance(item, dict) for item in attempts):
            raise TechnicalStationSnapshotError(
                "Technical-station attempts must be objects."
            )
        try:
            return cls(
                attempts=tuple(
                    TechnicalStationAttempt.from_dict(cast(dict[str, object], item))
                    for item in attempts
                ),
                schema_version=version,
            )
        except ValueError as exc:
            if isinstance(exc, TechnicalStationSnapshotError):
                raise
            raise TechnicalStationSnapshotError(str(exc)) from exc


def _required_text(value: object, label: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise TechnicalStationSnapshotError(f"Technical-station {label} must be non-empty text.")
    return value


def render_technical_station_record(
    station: TechnicalStation,
    attempt: TechnicalStationAttempt,
    locale: AppLocale,
) -> str:
    """Render learner-owned evidence without presenting it as an examination result."""

    criteria = "\n".join(
        f"- [{'x' if item.criterion_id in attempt.checked_criteria else ' '}] "
        f"{item.text.text(locale)}"
        for item in station.criteria
    )
    return "\n".join(
        (
            f"# {station.course_code} — {station.title.text(locale)}",
            "",
            f"Station ID: `{station.station_id}`",
            f"Type: `{station.kind.value}`",
            f"Laboratory: `{station.lab_id}`",
            f"Estimated minutes: {station.estimated_minutes}",
            f"Self-reviewed: {'yes' if attempt.reviewed else 'no'}",
            f"Hint level used: {attempt.hint_level}/6",
            "",
            f"## {station.artifact_title.text(locale)}",
            "",
            "```text",
            station.artifact.rstrip(),
            "```",
            "",
            "## Prompt",
            "",
            station.prompt.text(locale),
            "",
            "## Learner response",
            "",
            attempt.response.rstrip() or "[blank]",
            "",
            "## Explicit self-review",
            "",
            criteria,
            "",
            "This record is formative technical-reasoning evidence. It is not an official "
            "exam simulation, grade prediction, or mastery certificate.",
        )
    )


__all__ = [
    "MAX_STATION_RESPONSE_LENGTH",
    "TECHNICAL_STATION_SCHEMA_VERSION",
    "TechnicalStation",
    "TechnicalStationAttempt",
    "TechnicalStationCriterion",
    "TechnicalStationKind",
    "TechnicalStationSnapshot",
    "TechnicalStationSnapshotError",
    "render_technical_station_record",
]
