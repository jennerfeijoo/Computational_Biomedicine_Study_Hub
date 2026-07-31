"""Versioned domain model for DM847 open responses and essay drafts."""

from __future__ import annotations

import json
from dataclasses import dataclass, replace
from datetime import UTC, datetime
from enum import StrEnum
from typing import cast

WRITTEN_ASSESSMENT_SCHEMA_VERSION = 1


class WrittenAssessmentSnapshotError(ValueError):
    """Raised when persisted written-assessment state cannot be validated safely."""


class WrittenTaskKind(StrEnum):
    """Authored task formats available in the DM847 writing studio."""

    OPEN_RESPONSE = "open_response"
    ESSAY = "essay"


class WrittenFeedbackMode(StrEnum):
    """Bounded ways in which Ollama may support one learner draft."""

    CONTENT_REVIEW = "content_review"
    WRITING_REVISION = "writing_revision"
    ESSAY_COACH = "essay_coach"


@dataclass(frozen=True, slots=True)
class WrittenAssessmentPrompt:
    """Stable task identity linked to one authored DM847 module and objectives."""

    prompt_id: str
    module_id: str
    objective_ids: tuple[str, ...]
    kind: WrittenTaskKind

    def __post_init__(self) -> None:
        if not self.prompt_id.strip():
            raise ValueError("Written-assessment prompt IDs cannot be empty.")
        if not self.module_id.startswith("dm847.m"):
            raise ValueError("DM847 written prompts must reference a DM847 module.")
        if not self.objective_ids:
            raise ValueError(f"Prompt {self.prompt_id!r} requires objective links.")
        if len(self.objective_ids) != len(set(self.objective_ids)):
            raise ValueError(f"Prompt {self.prompt_id!r} has duplicate objective links.")


DM847_WRITTEN_PROMPTS: tuple[WrittenAssessmentPrompt, ...] = (
    WrittenAssessmentPrompt(
        "dm847.w01",
        "dm847.m01",
        ("m01.o2", "m01.o3", "m01.o6"),
        WrittenTaskKind.OPEN_RESPONSE,
    ),
    WrittenAssessmentPrompt(
        "dm847.w02",
        "dm847.m02",
        ("m02.o2", "m02.o4", "m02.o6"),
        WrittenTaskKind.OPEN_RESPONSE,
    ),
    WrittenAssessmentPrompt(
        "dm847.w03",
        "dm847.m03",
        ("m03.o2", "m03.o4", "m03.o6"),
        WrittenTaskKind.OPEN_RESPONSE,
    ),
    WrittenAssessmentPrompt(
        "dm847.w04",
        "dm847.m04",
        ("m04.o2", "m04.o4", "m04.o6"),
        WrittenTaskKind.OPEN_RESPONSE,
    ),
    WrittenAssessmentPrompt(
        "dm847.w05",
        "dm847.m05",
        ("m05.o1", "m05.o3", "m05.o6"),
        WrittenTaskKind.ESSAY,
    ),
    WrittenAssessmentPrompt(
        "dm847.w06",
        "dm847.m06",
        ("m06.o2", "m06.o4", "m06.o6"),
        WrittenTaskKind.OPEN_RESPONSE,
    ),
    WrittenAssessmentPrompt(
        "dm847.w07",
        "dm847.m07",
        ("m07.o2", "m07.o4", "m07.o6"),
        WrittenTaskKind.OPEN_RESPONSE,
    ),
    WrittenAssessmentPrompt(
        "dm847.w08",
        "dm847.m08",
        ("m08.o2", "m08.o4", "m08.o6"),
        WrittenTaskKind.ESSAY,
    ),
    WrittenAssessmentPrompt(
        "dm847.w09",
        "dm847.m09",
        ("m09.o2", "m09.o4", "m09.o6"),
        WrittenTaskKind.OPEN_RESPONSE,
    ),
    WrittenAssessmentPrompt(
        "dm847.w10",
        "dm847.m10",
        ("m10.o2", "m10.o4", "m10.o6"),
        WrittenTaskKind.ESSAY,
    ),
)

_PROMPT_BY_ID = {item.prompt_id: item for item in DM847_WRITTEN_PROMPTS}
if len(_PROMPT_BY_ID) != len(DM847_WRITTEN_PROMPTS):
    raise ValueError("DM847 written-assessment prompt IDs must be unique.")


@dataclass(frozen=True, slots=True)
class WrittenDraft:
    """One learner-owned draft and the latest optional model feedback."""

    prompt_id: str
    response_text: str = ""
    feedback_text: str = ""
    feedback_mode: WrittenFeedbackMode | None = None
    source_ids: tuple[str, ...] = ()

    def __post_init__(self) -> None:
        if self.prompt_id not in _PROMPT_BY_ID:
            raise ValueError(f"Unknown DM847 written prompt {self.prompt_id!r}.")
        if self.feedback_text.strip() and self.feedback_mode is None:
            raise ValueError("Persisted feedback requires a feedback mode.")
        if self.source_ids and not self.feedback_text.strip():
            raise ValueError("Persisted source IDs require feedback text.")
        if len(self.source_ids) != len(set(self.source_ids)):
            raise ValueError("Persisted written-feedback source IDs cannot be duplicated.")


@dataclass(frozen=True, slots=True)
class WrittenAssessmentSnapshot:
    """All local DM847 writing drafts with one active task identity."""

    schema_version: int
    active_prompt_id: str
    drafts: tuple[WrittenDraft, ...]
    updated_at: datetime

    def __post_init__(self) -> None:
        if self.schema_version != WRITTEN_ASSESSMENT_SCHEMA_VERSION:
            raise ValueError(
                f"Unsupported written-assessment schema {self.schema_version}; "
                f"expected {WRITTEN_ASSESSMENT_SCHEMA_VERSION}."
            )
        if self.active_prompt_id not in _PROMPT_BY_ID:
            raise ValueError(f"Unknown active written prompt {self.active_prompt_id!r}.")
        if self.updated_at.tzinfo is None or self.updated_at.utcoffset() is None:
            raise ValueError("Written-assessment timestamps must be timezone-aware.")
        prompt_ids = tuple(item.prompt_id for item in self.drafts)
        if len(prompt_ids) != len(set(prompt_ids)):
            raise ValueError("Written-assessment drafts cannot duplicate prompt IDs.")
        expected_order = tuple(item.prompt_id for item in DM847_WRITTEN_PROMPTS)
        if prompt_ids != expected_order:
            raise ValueError("Written-assessment drafts must preserve authored prompt order.")

    @classmethod
    def empty(cls, *, now: datetime | None = None) -> WrittenAssessmentSnapshot:
        """Create a validated empty draft collection."""

        return cls(
            schema_version=WRITTEN_ASSESSMENT_SCHEMA_VERSION,
            active_prompt_id=DM847_WRITTEN_PROMPTS[0].prompt_id,
            drafts=tuple(WrittenDraft(item.prompt_id) for item in DM847_WRITTEN_PROMPTS),
            updated_at=now or datetime.now(UTC),
        )

    def prompt(self, prompt_id: str) -> WrittenAssessmentPrompt:
        """Return one authored prompt specification by stable ID."""

        try:
            return _PROMPT_BY_ID[prompt_id]
        except KeyError as exc:
            raise ValueError(f"Unknown DM847 written prompt {prompt_id!r}.") from exc

    def draft(self, prompt_id: str) -> WrittenDraft:
        """Return one persisted learner draft by stable prompt ID."""

        return next(item for item in self.drafts if item.prompt_id == prompt_id)

    def with_active_prompt(
        self,
        prompt_id: str,
        *,
        now: datetime | None = None,
    ) -> WrittenAssessmentSnapshot:
        """Select one task without changing any draft content."""

        if prompt_id not in _PROMPT_BY_ID:
            raise ValueError(f"Unknown DM847 written prompt {prompt_id!r}.")
        return replace(
            self,
            active_prompt_id=prompt_id,
            updated_at=now or datetime.now(UTC),
        )

    def with_response(
        self,
        prompt_id: str,
        response_text: str,
        *,
        clear_feedback: bool = True,
        now: datetime | None = None,
    ) -> WrittenAssessmentSnapshot:
        """Replace learner text and optionally invalidate feedback for the older draft."""

        current = self.draft(prompt_id)
        replacement = replace(
            current,
            response_text=response_text,
            feedback_text="" if clear_feedback else current.feedback_text,
            feedback_mode=None if clear_feedback else current.feedback_mode,
            source_ids=() if clear_feedback else current.source_ids,
        )
        return self._replace_draft(replacement, now=now)

    def with_feedback(
        self,
        prompt_id: str,
        *,
        feedback_text: str,
        feedback_mode: WrittenFeedbackMode,
        source_ids: tuple[str, ...],
        now: datetime | None = None,
    ) -> WrittenAssessmentSnapshot:
        """Attach source-traceable model feedback to the current learner draft."""

        if not feedback_text.strip():
            raise ValueError("Written feedback cannot be empty.")
        replacement = replace(
            self.draft(prompt_id),
            feedback_text=feedback_text.strip(),
            feedback_mode=feedback_mode,
            source_ids=source_ids,
        )
        return self._replace_draft(replacement, now=now)

    def _replace_draft(
        self,
        replacement: WrittenDraft,
        *,
        now: datetime | None,
    ) -> WrittenAssessmentSnapshot:
        drafts = tuple(
            replacement if item.prompt_id == replacement.prompt_id else item
            for item in self.drafts
        )
        return replace(self, drafts=drafts, updated_at=now or datetime.now(UTC))

    def to_json(self) -> str:
        """Serialize learner-owned state to deterministic JSON."""

        payload: dict[str, object] = {
            "schema_version": self.schema_version,
            "active_prompt_id": self.active_prompt_id,
            "drafts": [
                {
                    "prompt_id": item.prompt_id,
                    "response_text": item.response_text,
                    "feedback_text": item.feedback_text,
                    "feedback_mode": (
                        item.feedback_mode.value if item.feedback_mode is not None else None
                    ),
                    "source_ids": list(item.source_ids),
                }
                for item in self.drafts
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
    def from_json(cls, document: str) -> WrittenAssessmentSnapshot:
        """Parse and validate one persisted document defensively."""

        try:
            decoded: object = json.loads(document)
            if not isinstance(decoded, dict):
                raise TypeError("Written-assessment document root must be an object.")
            payload = cast(dict[str, object], decoded)
            raw_drafts = payload["drafts"]
            if not isinstance(raw_drafts, list):
                raise TypeError("Written-assessment drafts must be an array.")

            drafts: list[WrittenDraft] = []
            for raw_item in raw_drafts:
                if not isinstance(raw_item, dict):
                    raise TypeError("Written-assessment draft entries must be objects.")
                item = cast(dict[str, object], raw_item)
                raw_mode = item.get("feedback_mode")
                feedback_mode = (
                    None
                    if raw_mode is None
                    else WrittenFeedbackMode(_required_string(item, "feedback_mode"))
                )
                drafts.append(
                    WrittenDraft(
                        prompt_id=_required_string(item, "prompt_id"),
                        response_text=_required_string(item, "response_text", allow_empty=True),
                        feedback_text=_required_string(item, "feedback_text", allow_empty=True),
                        feedback_mode=feedback_mode,
                        source_ids=tuple(_required_string_list(item, "source_ids")),
                    )
                )

            return cls(
                schema_version=_required_int(payload, "schema_version"),
                active_prompt_id=_required_string(payload, "active_prompt_id"),
                drafts=tuple(drafts),
                updated_at=datetime.fromisoformat(_required_string(payload, "updated_at")),
            )
        except (
            KeyError,
            TypeError,
            ValueError,
            json.JSONDecodeError,
        ) as exc:
            raise WrittenAssessmentSnapshotError(
                "The persisted DM847 written-assessment document is invalid."
            ) from exc


def _required_string(
    payload: dict[str, object],
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


def _required_string_list(payload: dict[str, object], key: str) -> list[str]:
    value = payload[key]
    if not isinstance(value, list) or any(not isinstance(item, str) for item in value):
        raise TypeError(f"{key} must be an array of strings.")
    return cast(list[str], value)


def _required_int(payload: dict[str, object], key: str) -> int:
    value = payload[key]
    if isinstance(value, bool) or not isinstance(value, int):
        raise TypeError(f"{key} must be an integer.")
    return value


__all__ = [
    "DM847_WRITTEN_PROMPTS",
    "WRITTEN_ASSESSMENT_SCHEMA_VERSION",
    "WrittenAssessmentPrompt",
    "WrittenAssessmentSnapshot",
    "WrittenAssessmentSnapshotError",
    "WrittenDraft",
    "WrittenFeedbackMode",
    "WrittenTaskKind",
]
