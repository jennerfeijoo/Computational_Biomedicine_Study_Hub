"""Serialization and deterministic grading for option-based cloze activities."""

from __future__ import annotations

from collections.abc import Mapping
from typing import TypedDict, cast

from ..content.models import AssessmentItem, AssessmentOption, ClozeGap
from .activity_types import ActivityType


class SerializedClozeOption(TypedDict):
    option_id: str
    text: str


class SerializedClozeGap(TypedDict):
    gap_id: str
    options: list[SerializedClozeOption]
    correct_option_id: str


class SerializedClozeItem(TypedDict):
    item_id: str
    activity_type: str
    prompt: str
    explanation: str
    rubric: list[str]
    gaps: list[SerializedClozeGap]


def cloze_item_to_dict(item: AssessmentItem) -> SerializedClozeItem:
    """Serialize one materialized cloze item without deriving keys from text."""
    if item.activity_type is not ActivityType.CLOZE_CHOICE:
        raise ValueError("Only cloze-choice items can use this serializer.")
    return {
        "item_id": item.item_id,
        "activity_type": item.activity_type.value,
        "prompt": item.prompt,
        "explanation": item.explanation,
        "rubric": list(item.rubric),
        "gaps": [
            {
                "gap_id": gap.gap_id,
                "options": [
                    {"option_id": option.option_id, "text": option.text} for option in gap.options
                ],
                "correct_option_id": gap.correct_option_id,
            }
            for gap in item.cloze_gaps
        ],
    }


def cloze_item_from_dict(payload: Mapping[str, object]) -> AssessmentItem:
    """Deserialize one cloze item through the same validated domain constructors."""
    raw_gaps = payload.get("gaps")
    if not isinstance(raw_gaps, list):
        raise ValueError("Serialized cloze item requires a gaps list.")
    gaps: list[ClozeGap] = []
    for raw_gap in raw_gaps:
        if not isinstance(raw_gap, dict):
            raise ValueError("Serialized cloze gaps must be objects.")
        raw_options = raw_gap.get("options")
        if not isinstance(raw_options, list):
            raise ValueError("Serialized cloze gap requires an options list.")
        options: list[AssessmentOption] = []
        for raw_option in raw_options:
            if not isinstance(raw_option, dict):
                raise ValueError("Serialized cloze options must be objects.")
            options.append(
                AssessmentOption(
                    option_id=_required_string(raw_option, "option_id"),
                    text=_required_string(raw_option, "text"),
                )
            )
        gaps.append(
            ClozeGap(
                gap_id=_required_string(raw_gap, "gap_id"),
                options=tuple(options),
                correct_option_id=_required_string(raw_gap, "correct_option_id"),
            )
        )

    raw_rubric = payload.get("rubric", [])
    if not isinstance(raw_rubric, list) or not all(
        isinstance(criterion, str) for criterion in raw_rubric
    ):
        raise ValueError("Serialized cloze rubric must be a string list.")
    activity_type = _required_string(payload, "activity_type")
    if activity_type != ActivityType.CLOZE_CHOICE.value:
        raise ValueError("Serialized activity_type must be cloze_choice.")
    return AssessmentItem(
        item_id=_required_string(payload, "item_id"),
        activity_type=ActivityType.CLOZE_CHOICE,
        prompt=_required_string(payload, "prompt"),
        options=(),
        correct_answers=(),
        explanation=_required_string(payload, "explanation"),
        rubric=tuple(cast(list[str], raw_rubric)),
        cloze_gaps=tuple(gaps),
    )


def evaluate_cloze(item: AssessmentItem, answers: Mapping[str, str]) -> bool:
    """Grade all cloze gaps by stable gap and option IDs."""
    if item.activity_type is not ActivityType.CLOZE_CHOICE:
        raise ValueError("Only cloze-choice items can be evaluated as cloze.")
    expected = {gap.gap_id: gap.correct_option_id for gap in item.cloze_gaps}
    return dict(answers) == expected


def _required_string(payload: Mapping[str, object], key: str) -> str:
    value = payload.get(key)
    if not isinstance(value, str) or not value.strip():
        raise ValueError(f"Serialized cloze field {key!r} must be a non-empty string.")
    return value


__all__ = [
    "SerializedClozeItem",
    "cloze_item_from_dict",
    "cloze_item_to_dict",
    "evaluate_cloze",
]
