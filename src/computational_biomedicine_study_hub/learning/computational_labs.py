"""Domain model for persistent computational-biomedicine laboratory work."""

from __future__ import annotations

import json
from dataclasses import dataclass, replace
from datetime import UTC, datetime
from enum import StrEnum
from typing import cast

from ..i18n.locales import AppLocale, SUPPORTED_LOCALES

LAB_NOTEBOOK_SCHEMA_VERSION = 1
MAX_LAB_RESPONSE_LENGTH = 60_000


class LabSnapshotError(ValueError):
    """Raised when a persisted laboratory notebook is malformed."""


class LabStage(StrEnum):
    """Stable stages in the computational laboratory learning cycle."""

    PREPARE = "prepare"
    INVESTIGATE = "investigate"
    IMPLEMENT = "implement"
    CHECK = "check"
    INTERPRET = "interpret"
    DEFEND = "defend"
    CONSOLIDATE = "consolidate"


class LabTaskKind(StrEnum):
    """Interaction required by one laboratory task."""

    SHORT_ANSWER = "short_answer"
    PYTHON = "python"


@dataclass(frozen=True, slots=True)
class LocalizedText:
    """Strict text bundle requiring every supported application locale."""

    values: dict[AppLocale, str]

    def __post_init__(self) -> None:
        copied = {locale: value.strip() for locale, value in self.values.items()}
        if set(copied) != set(SUPPORTED_LOCALES):
            raise ValueError("Localized laboratory text requires Spanish, English, and Danish.")
        if any(not value for value in copied.values()):
            raise ValueError("Localized laboratory text cannot be blank.")
        object.__setattr__(self, "values", copied)

    def text(self, locale: AppLocale) -> str:
        """Return text in one explicitly supported locale."""

        return self.values[locale]


@dataclass(frozen=True, slots=True)
class LabTask:
    """One evidence-producing task within a laboratory stage."""

    task_id: str
    stage: LabStage
    kind: LabTaskKind
    title: LocalizedText
    instructions: LocalizedText
    mentor_notes: LocalizedText
    objective_ids: tuple[str, ...]
    estimated_minutes: int
    starter_response: str = ""
    verification_source: str = ""
    expected_output: str | None = None
    seed_from_task_id: str | None = None

    def __post_init__(self) -> None:
        if not self.task_id.strip():
            raise ValueError("Laboratory tasks require stable identities.")
        if not self.objective_ids:
            raise ValueError("Laboratory tasks require linked learning objectives.")
        if len(self.objective_ids) != len(set(self.objective_ids)):
            raise ValueError("Laboratory task objective IDs cannot be duplicated.")
        if not 1 <= self.estimated_minutes <= 180:
            raise ValueError("Laboratory task duration must be between 1 and 180 minutes.")
        if self.kind is LabTaskKind.PYTHON:
            if not self.verification_source.strip() or self.expected_output is None:
                raise ValueError("Python laboratory tasks require hidden verification and output.")
        elif self.verification_source or self.expected_output is not None:
            raise ValueError("Short-answer tasks cannot contain Python verification code.")
        if self.seed_from_task_id == self.task_id:
            raise ValueError("A laboratory task cannot seed itself.")


@dataclass(frozen=True, slots=True)
class ComputationalLab:
    """A complete internal preparation laboratory with an authentic research cycle."""

    lab_id: str
    course_code: str
    version: str
    title: LocalizedText
    research_question: LocalizedText
    disclaimer: LocalizedText
    data_provenance: LocalizedText
    objectives: tuple[tuple[str, LocalizedText], ...]
    prerequisites: tuple[LocalizedText, ...]
    tasks: tuple[LabTask, ...]
    estimated_minutes: int

    def __post_init__(self) -> None:
        if not self.lab_id.strip() or not self.course_code.strip() or not self.version.strip():
            raise ValueError("Laboratories require stable course, laboratory, and version identities.")
        if not 30 <= self.estimated_minutes <= 480:
            raise ValueError("Laboratory duration must be between 30 and 480 minutes.")
        if not self.objectives or not self.prerequisites or not self.tasks:
            raise ValueError("Laboratories require objectives, prerequisites, and tasks.")
        objective_ids = tuple(objective_id for objective_id, _ in self.objectives)
        if any(not objective_id.strip() for objective_id in objective_ids):
            raise ValueError("Laboratory objective IDs cannot be blank.")
        if len(objective_ids) != len(set(objective_ids)):
            raise ValueError("Laboratory objective IDs cannot be duplicated.")
        task_ids = tuple(task.task_id for task in self.tasks)
        if len(task_ids) != len(set(task_ids)):
            raise ValueError("Laboratory task IDs cannot be duplicated.")
        expected_stages = tuple(LabStage)
        present_stages = tuple(dict.fromkeys(task.stage for task in self.tasks))
        if present_stages != expected_stages:
            raise ValueError("Laboratory tasks must cover all stages in stable pedagogical order.")
        known_objectives = set(objective_ids)
        for task in self.tasks:
            if not set(task.objective_ids) <= known_objectives:
                raise ValueError(f"Task {task.task_id!r} references an unknown objective.")
            if task.seed_from_task_id is not None and task.seed_from_task_id not in task_ids:
                raise ValueError(f"Task {task.task_id!r} has an unknown response seed.")
        if sum(task.estimated_minutes for task in self.tasks) > self.estimated_minutes + 30:
            raise ValueError("Task estimates exceed the laboratory estimate by more than 30 minutes.")

    def task(self, task_id: str) -> LabTask:
        """Return one authored task by stable identity."""

        try:
            return next(task for task in self.tasks if task.task_id == task_id)
        except StopIteration as exc:
            raise ValueError(f"Unknown laboratory task {task_id!r}.") from exc

    def objective_text(self, objective_id: str, locale: AppLocale) -> str:
        """Return one localized objective description."""

        try:
            return next(text.text(locale) for key, text in self.objectives if key == objective_id)
        except StopIteration as exc:
            raise ValueError(f"Unknown laboratory objective {objective_id!r}.") from exc


@dataclass(frozen=True, slots=True)
class LabAttempt:
    """Learner-owned responses, checkpoints, hints, and execution evidence for one lab."""

    lab_id: str
    current_task_id: str
    responses: dict[str, str]
    completed_tasks: frozenset[str]
    passed_checkpoints: frozenset[str]
    hint_levels: dict[str, int]
    execution_outputs: dict[str, str]
    started_at: datetime
    updated_at: datetime

    def __post_init__(self) -> None:
        if not self.lab_id.strip() or not self.current_task_id.strip():
            raise ValueError("Laboratory attempts require lab and task identities.")
        for timestamp in (self.started_at, self.updated_at):
            if timestamp.tzinfo is None or timestamp.utcoffset() is None:
                raise ValueError("Laboratory attempt timestamps must be timezone-aware.")
        if self.updated_at < self.started_at:
            raise ValueError("Laboratory attempts cannot be updated before they start.")
        if any(len(value) > MAX_LAB_RESPONSE_LENGTH for value in self.responses.values()):
            raise ValueError("Laboratory responses exceed the local storage limit.")
        if any(level < 0 or level > 6 for level in self.hint_levels.values()):
            raise ValueError("Laboratory hint levels must be between zero and six.")
        object.__setattr__(self, "responses", dict(self.responses))
        object.__setattr__(self, "hint_levels", dict(self.hint_levels))
        object.__setattr__(self, "execution_outputs", dict(self.execution_outputs))

    @classmethod
    def new(cls, lab: ComputationalLab, *, now: datetime | None = None) -> LabAttempt:
        """Create a blank attempt positioned at the first authored task."""

        timestamp = now or datetime.now(UTC)
        return cls(
            lab_id=lab.lab_id,
            current_task_id=lab.tasks[0].task_id,
            responses={},
            completed_tasks=frozenset(),
            passed_checkpoints=frozenset(),
            hint_levels={},
            execution_outputs={},
            started_at=timestamp,
            updated_at=timestamp,
        )

    def response_for(self, task_id: str) -> str:
        """Return a saved learner response without inventing a value."""

        return self.responses.get(task_id, "")

    def hint_level_for(self, task_id: str) -> int:
        """Return the progressive support level already requested for a task."""

        return self.hint_levels.get(task_id, 0)

    def with_current_task(self, task_id: str, *, now: datetime | None = None) -> LabAttempt:
        """Move the visible task while retaining all learner evidence."""

        return replace(self, current_task_id=task_id, updated_at=now or datetime.now(UTC))

    def with_response(
        self,
        task_id: str,
        response: str,
        *,
        now: datetime | None = None,
    ) -> LabAttempt:
        """Replace one learner-owned response and clear stale completion evidence."""

        if len(response) > MAX_LAB_RESPONSE_LENGTH:
            raise ValueError("Laboratory responses exceed the local storage limit.")
        responses = dict(self.responses)
        responses[task_id] = response
        completed = set(self.completed_tasks)
        checkpoints = set(self.passed_checkpoints)
        completed.discard(task_id)
        checkpoints.discard(task_id)
        return replace(
            self,
            responses=responses,
            completed_tasks=frozenset(completed),
            passed_checkpoints=frozenset(checkpoints),
            updated_at=now or datetime.now(UTC),
        )

    def mark_complete(
        self,
        task_id: str,
        *,
        checkpoint_passed: bool = False,
        output: str = "",
        now: datetime | None = None,
    ) -> LabAttempt:
        """Record deterministic completion and optional checkpoint evidence."""

        completed = set(self.completed_tasks)
        completed.add(task_id)
        checkpoints = set(self.passed_checkpoints)
        if checkpoint_passed:
            checkpoints.add(task_id)
        outputs = dict(self.execution_outputs)
        if output:
            outputs[task_id] = output
        return replace(
            self,
            completed_tasks=frozenset(completed),
            passed_checkpoints=frozenset(checkpoints),
            execution_outputs=outputs,
            updated_at=now or datetime.now(UTC),
        )

    def with_requested_hint(
        self,
        task_id: str,
        *,
        now: datetime | None = None,
    ) -> LabAttempt:
        """Increase one task's support level without changing mastery or completion."""

        levels = dict(self.hint_levels)
        levels[task_id] = min(6, levels.get(task_id, 0) + 1)
        return replace(self, hint_levels=levels, updated_at=now or datetime.now(UTC))

    def completion_ratio(self, lab: ComputationalLab) -> float:
        """Return the fraction of authored tasks with deterministic completion evidence."""

        if self.lab_id != lab.lab_id:
            raise ValueError("Attempt and laboratory identities must match.")
        return len(set(task.task_id for task in lab.tasks) & set(self.completed_tasks)) / len(
            lab.tasks
        )

    def to_dict(self) -> dict[str, object]:
        return {
            "lab_id": self.lab_id,
            "current_task_id": self.current_task_id,
            "responses": dict(self.responses),
            "completed_tasks": sorted(self.completed_tasks),
            "passed_checkpoints": sorted(self.passed_checkpoints),
            "hint_levels": dict(self.hint_levels),
            "execution_outputs": dict(self.execution_outputs),
            "started_at": self.started_at.isoformat(),
            "updated_at": self.updated_at.isoformat(),
        }

    @classmethod
    def from_dict(cls, payload: dict[str, object]) -> LabAttempt:
        try:
            responses = _string_mapping(payload.get("responses"), "responses")
            hints = _int_mapping(payload.get("hint_levels"), "hint levels")
            outputs = _string_mapping(payload.get("execution_outputs"), "execution outputs")
            return cls(
                lab_id=_required_text(payload.get("lab_id"), "lab ID"),
                current_task_id=_required_text(payload.get("current_task_id"), "task ID"),
                responses=responses,
                completed_tasks=frozenset(
                    _string_sequence(payload.get("completed_tasks"), "completed tasks")
                ),
                passed_checkpoints=frozenset(
                    _string_sequence(payload.get("passed_checkpoints"), "checkpoints")
                ),
                hint_levels=hints,
                execution_outputs=outputs,
                started_at=datetime.fromisoformat(
                    _required_text(payload.get("started_at"), "start timestamp")
                ),
                updated_at=datetime.fromisoformat(
                    _required_text(payload.get("updated_at"), "update timestamp")
                ),
            )
        except (TypeError, ValueError) as exc:
            if isinstance(exc, LabSnapshotError):
                raise
            raise LabSnapshotError(str(exc)) from exc


@dataclass(frozen=True, slots=True)
class LabNotebookSnapshot:
    """Versioned collection of persistent laboratory attempts."""

    attempts: tuple[LabAttempt, ...] = ()
    schema_version: int = LAB_NOTEBOOK_SCHEMA_VERSION

    def __post_init__(self) -> None:
        if self.schema_version != LAB_NOTEBOOK_SCHEMA_VERSION:
            raise ValueError("Unsupported laboratory notebook schema version.")
        identities = tuple(attempt.lab_id for attempt in self.attempts)
        if len(identities) != len(set(identities)):
            raise ValueError("Laboratory notebooks require one attempt per lab.")

    def attempt_for(self, lab: ComputationalLab) -> LabAttempt:
        """Return saved work or create a new attempt for an authored lab."""

        return next(
            (attempt for attempt in self.attempts if attempt.lab_id == lab.lab_id),
            LabAttempt.new(lab),
        )

    def with_attempt(self, attempt: LabAttempt) -> LabNotebookSnapshot:
        """Replace one attempt while preserving other laboratory work."""

        remaining = tuple(item for item in self.attempts if item.lab_id != attempt.lab_id)
        return LabNotebookSnapshot((*remaining, attempt), self.schema_version)

    def to_json(self) -> str:
        return json.dumps(
            {
                "schema_version": self.schema_version,
                "attempts": [attempt.to_dict() for attempt in self.attempts],
            },
            ensure_ascii=False,
            indent=2,
            sort_keys=True,
        )

    @classmethod
    def from_json(cls, serialized: str) -> LabNotebookSnapshot:
        try:
            raw = json.loads(serialized)
        except json.JSONDecodeError as exc:
            raise LabSnapshotError("Laboratory notebook is not valid JSON.") from exc
        if not isinstance(raw, dict):
            raise LabSnapshotError("Laboratory notebook root must be an object.")
        version = raw.get("schema_version")
        if isinstance(version, bool) or not isinstance(version, int):
            raise LabSnapshotError("Laboratory notebook schema version must be an integer.")
        raw_attempts = raw.get("attempts")
        if not isinstance(raw_attempts, list) or not all(
            isinstance(item, dict) for item in raw_attempts
        ):
            raise LabSnapshotError("Laboratory notebook attempts must be objects.")
        try:
            return cls(
                attempts=tuple(
                    LabAttempt.from_dict(cast(dict[str, object], item)) for item in raw_attempts
                ),
                schema_version=version,
            )
        except ValueError as exc:
            if isinstance(exc, LabSnapshotError):
                raise
            raise LabSnapshotError(str(exc)) from exc


def render_lab_record(
    lab: ComputationalLab,
    attempt: LabAttempt,
    locale: AppLocale,
) -> str:
    """Render a portable Markdown record without exposing authored verification code."""

    lines = [
        f"# {lab.course_code} · {lab.title.text(locale)}",
        "",
        f"**Lab ID:** `{lab.lab_id}`  ",
        f"**Version:** `{lab.version}`  ",
        f"**Started:** {attempt.started_at.isoformat()}  ",
        f"**Updated:** {attempt.updated_at.isoformat()}  ",
        f"**Completion:** {attempt.completion_ratio(lab):.0%}",
        "",
        f"> {lab.disclaimer.text(locale)}",
        "",
        f"## {lab.research_question.text(locale)}",
        "",
    ]
    for task in lab.tasks:
        response = attempt.response_for(task.task_id).strip() or "_No response recorded._"
        lines.extend(
            (
                f"## {task.stage.value.title()} · {task.title.text(locale)}",
                "",
                task.instructions.text(locale),
                "",
                "### Learner evidence",
                "",
                "```python" if task.kind is LabTaskKind.PYTHON else "",
                response,
                "```" if task.kind is LabTaskKind.PYTHON else "",
                "",
                f"Checkpoint passed: {'yes' if task.task_id in attempt.passed_checkpoints else 'no'}",
                f"Hint level used: {attempt.hint_level_for(task.task_id)}",
                "",
            )
        )
    return "\n".join(lines).rstrip() + "\n"


def _required_text(value: object, label: str) -> str:
    text = str(value or "").strip()
    if not text:
        raise LabSnapshotError(f"Laboratory {label} cannot be blank.")
    return text


def _string_sequence(value: object, label: str) -> tuple[str, ...]:
    if not isinstance(value, list) or not all(isinstance(item, str) for item in value):
        raise LabSnapshotError(f"Laboratory {label} must be a list of strings.")
    return tuple(item for item in value if item)


def _string_mapping(value: object, label: str) -> dict[str, str]:
    if not isinstance(value, dict) or not all(
        isinstance(key, str) and isinstance(item, str) for key, item in value.items()
    ):
        raise LabSnapshotError(f"Laboratory {label} must be a string mapping.")
    return cast(dict[str, str], value)


def _int_mapping(value: object, label: str) -> dict[str, int]:
    if not isinstance(value, dict) or not all(
        isinstance(key, str)
        and isinstance(item, int)
        and not isinstance(item, bool)
        for key, item in value.items()
    ):
        raise LabSnapshotError(f"Laboratory {label} must be an integer mapping.")
    return cast(dict[str, int], value)


__all__ = [
    "ComputationalLab",
    "LAB_NOTEBOOK_SCHEMA_VERSION",
    "LabAttempt",
    "LabNotebookSnapshot",
    "LabSnapshotError",
    "LabStage",
    "LabTask",
    "LabTaskKind",
    "LocalizedText",
    "render_lab_record",
]
