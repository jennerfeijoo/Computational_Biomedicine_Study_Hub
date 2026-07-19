"""Typed formative feedback returned by the local tutor."""

from __future__ import annotations

from collections.abc import Mapping
from dataclasses import dataclass
from typing import Any


@dataclass(frozen=True, slots=True)
class RubricDimension:
    name: str
    score: int
    evidence: str

    def __post_init__(self) -> None:
        if not 0 <= self.score <= 4:
            raise ValueError("Formative rubric scores must be between 0 and 4.")


@dataclass(frozen=True, slots=True)
class OpenResponseFeedback:
    summary: str
    strengths: tuple[str, ...]
    missing_concepts: tuple[str, ...]
    misconceptions: tuple[str, ...]
    unsupported_claims: tuple[str, ...]
    rubric_dimensions: tuple[RubricDimension, ...]
    suggested_revision: str
    follow_up_question: str
    source_ids: tuple[str, ...]
    evaluator_confidence: str

    @classmethod
    def from_mapping(cls, value: Mapping[str, Any]) -> OpenResponseFeedback:
        dimensions = tuple(
            RubricDimension(
                name=str(item.get("name", "")),
                score=int(item.get("score", 0)),
                evidence=str(item.get("evidence", "")),
            )
            for item in value.get("rubric_dimensions", ())
            if isinstance(item, Mapping)
        )

        def strings(key: str) -> tuple[str, ...]:
            raw = value.get(key, ())
            return tuple(str(item) for item in raw) if isinstance(raw, list) else ()

        return cls(
            summary=str(value.get("summary", "")),
            strengths=strings("strengths"),
            missing_concepts=strings("missing_concepts"),
            misconceptions=strings("misconceptions"),
            unsupported_claims=strings("unsupported_claims"),
            rubric_dimensions=dimensions,
            suggested_revision=str(value.get("suggested_revision", "")),
            follow_up_question=str(value.get("follow_up_question", "")),
            source_ids=strings("source_ids"),
            evaluator_confidence=str(value.get("evaluator_confidence", "low")),
        )


__all__ = ["OpenResponseFeedback", "RubricDimension"]
