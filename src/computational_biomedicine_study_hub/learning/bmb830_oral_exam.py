"""Grounded BMB830 oral-exam practice and provisional model evaluation.

The simulator uses authored BMB830 Socratic questions and grading criteria. Ollama
feedback remains formative: it is persisted as mentor evidence, but it never changes
objective mastery or represents an official SDU grade.
"""

from __future__ import annotations

import json
from dataclasses import dataclass, replace
from datetime import UTC, datetime
from enum import StrEnum
from statistics import mean
from typing import cast

from ..content.bmb830 import LOCALIZED_BUNDLES
from ..i18n.locales import AppLocale
from ..integrations.ollama import JsonObject
from ..learning.mentor import MentorObservation

BMB830_ORAL_SCHEMA_VERSION = 1
BMB830_ORAL_MAX_ATTEMPTS = 180


class BMB830OralSnapshotError(ValueError):
    """Raised when an oral-practice snapshot or evaluation is malformed."""


class OralCriterion(StrEnum):
    """Stable dimensions used for formative oral-answer analysis."""

    ACCURACY = "accuracy"
    STATISTICAL_REASONING = "statistical_reasoning"
    INTERPRETATION = "interpretation"
    LIMITATIONS = "limitations"
    COMMUNICATION = "communication"


@dataclass(frozen=True, slots=True)
class BMB830OralPrompt:
    """One grounded oral prompt derived from authored BMB830 tutor support."""

    prompt_id: str
    module_id: str
    module_title: str
    question: str
    objective_ids: tuple[str, ...]
    grading_criteria: tuple[str, ...]
    source_basis: tuple[str, ...]

    def __post_init__(self) -> None:
        required = (self.prompt_id, self.module_id, self.module_title, self.question)
        if any(not value.strip() for value in required):
            raise ValueError("BMB830 oral prompts require stable identities and visible text.")
        if not self.objective_ids:
            raise ValueError("BMB830 oral prompts require linked learning objectives.")
        if len(self.objective_ids) != len(set(self.objective_ids)):
            raise ValueError("BMB830 oral prompt objective IDs cannot be duplicated.")
        if not self.grading_criteria:
            raise ValueError("BMB830 oral prompts require authored grading criteria.")


@dataclass(frozen=True, slots=True)
class OralCriterionScore:
    """A formative zero-to-four score with transcript-grounded evidence."""

    criterion: OralCriterion
    score: int
    evidence: str

    def __post_init__(self) -> None:
        if not 0 <= self.score <= 4:
            raise ValueError("Oral criterion scores must be between zero and four.")
        if not self.evidence.strip():
            raise ValueError("Oral criterion scores require evidence from the response.")

    def to_dict(self) -> JsonObject:
        return {
            "criterion": self.criterion.value,
            "score": self.score,
            "evidence": self.evidence,
        }

    @classmethod
    def from_dict(cls, payload: JsonObject) -> OralCriterionScore:
        try:
            criterion = OralCriterion(str(payload.get("criterion") or ""))
        except ValueError as exc:
            raise BMB830OralSnapshotError("Unknown oral evaluation criterion.") from exc
        score = payload.get("score")
        if isinstance(score, bool) or not isinstance(score, int):
            raise BMB830OralSnapshotError("Oral criterion scores must be integers.")
        evidence = str(payload.get("evidence") or "").strip()
        try:
            return cls(criterion, score, evidence)
        except ValueError as exc:
            raise BMB830OralSnapshotError(str(exc)) from exc


@dataclass(frozen=True, slots=True)
class BMB830OralEvaluation:
    """Structured provisional feedback for one oral response transcript."""

    feedback: str
    strengths: tuple[str, ...]
    gaps: tuple[str, ...]
    misconceptions: tuple[str, ...]
    scores: tuple[OralCriterionScore, ...]
    follow_up_question: str
    recommended_next_action: str
    confidence: float
    needs_source_check: bool = False

    def __post_init__(self) -> None:
        if not self.feedback.strip() or not self.follow_up_question.strip():
            raise ValueError("Oral evaluations require feedback and one follow-up question.")
        if not self.recommended_next_action.strip():
            raise ValueError("Oral evaluations require a recommended next action.")
        if not 0.0 <= self.confidence <= 1.0:
            raise ValueError("Oral evaluation confidence must be between zero and one.")
        criteria = tuple(item.criterion for item in self.scores)
        if criteria != tuple(OralCriterion):
            raise ValueError(
                "Oral evaluations require every criterion exactly once in stable order."
            )
        for collection in (self.strengths, self.gaps, self.misconceptions):
            if len(collection) != len(set(collection)):
                raise ValueError("Oral evaluation observation lists cannot contain duplicates.")

    @property
    def average_score(self) -> float:
        """Return a formative zero-to-four mean across the five dimensions."""

        return mean(item.score for item in self.scores)

    def score_for(self, criterion: OralCriterion) -> OralCriterionScore:
        """Return one criterion result by stable identity."""

        return next(item for item in self.scores if item.criterion is criterion)

    def to_mentor_observation(self) -> MentorObservation:
        """Convert formative feedback into longitudinal, explicitly provisional memory."""

        return MentorObservation(
            demonstrated=self.strengths,
            gaps=self.gaps,
            misconceptions=self.misconceptions,
            recommended_next_action=self.recommended_next_action,
            next_question=self.follow_up_question,
            confidence=self.confidence,
            needs_source_check=self.needs_source_check,
        )

    def to_dict(self) -> JsonObject:
        return {
            "feedback": self.feedback,
            "strengths": list(self.strengths),
            "gaps": list(self.gaps),
            "misconceptions": list(self.misconceptions),
            "scores": [score.to_dict() for score in self.scores],
            "follow_up_question": self.follow_up_question,
            "recommended_next_action": self.recommended_next_action,
            "confidence": self.confidence,
            "needs_source_check": self.needs_source_check,
        }

    @classmethod
    def from_dict(cls, payload: JsonObject) -> BMB830OralEvaluation:
        raw_scores = payload.get("scores")
        if not isinstance(raw_scores, list) or not all(
            isinstance(item, dict) for item in raw_scores
        ):
            raise BMB830OralSnapshotError("Oral evaluation scores must be a list of objects.")
        try:
            return cls(
                feedback=_required_text(payload.get("feedback"), "feedback"),
                strengths=_string_tuple(payload.get("strengths")),
                gaps=_string_tuple(payload.get("gaps")),
                misconceptions=_string_tuple(payload.get("misconceptions")),
                scores=tuple(
                    OralCriterionScore.from_dict(cast(JsonObject, item)) for item in raw_scores
                ),
                follow_up_question=_required_text(
                    payload.get("follow_up_question"),
                    "follow-up question",
                ),
                recommended_next_action=_required_text(
                    payload.get("recommended_next_action"),
                    "recommended next action",
                ),
                confidence=_confidence(payload.get("confidence")),
                needs_source_check=payload.get("needs_source_check") is True,
            )
        except ValueError as exc:
            if isinstance(exc, BMB830OralSnapshotError):
                raise
            raise BMB830OralSnapshotError(str(exc)) from exc


@dataclass(frozen=True, slots=True)
class BMB830OralAttempt:
    """One learner transcript and its provisional model evaluation."""

    attempt_id: str
    prompt_id: str
    module_id: str
    transcript: str
    evaluation: BMB830OralEvaluation
    created_at: datetime
    model: str = ""
    prompt_eval_count: int = 0
    eval_count: int = 0
    total_duration_ns: int = 0

    def __post_init__(self) -> None:
        if not self.attempt_id.strip() or not self.prompt_id.strip() or not self.module_id.strip():
            raise ValueError("Oral attempts require stable identities.")
        if not self.transcript.strip():
            raise ValueError("Oral attempts require a learner transcript.")
        if self.created_at.tzinfo is None or self.created_at.utcoffset() is None:
            raise ValueError("Oral attempt timestamps must be timezone-aware.")
        if any(
            value < 0 for value in (self.prompt_eval_count, self.eval_count, self.total_duration_ns)
        ):
            raise ValueError("Oral evaluation telemetry cannot be negative.")

    def to_dict(self) -> JsonObject:
        return {
            "attempt_id": self.attempt_id,
            "prompt_id": self.prompt_id,
            "module_id": self.module_id,
            "transcript": self.transcript,
            "evaluation": self.evaluation.to_dict(),
            "created_at": self.created_at.isoformat(),
            "model": self.model,
            "prompt_eval_count": self.prompt_eval_count,
            "eval_count": self.eval_count,
            "total_duration_ns": self.total_duration_ns,
        }

    @classmethod
    def from_dict(cls, payload: JsonObject) -> BMB830OralAttempt:
        raw_evaluation = payload.get("evaluation")
        if not isinstance(raw_evaluation, dict):
            raise BMB830OralSnapshotError("Oral attempts require a structured evaluation.")
        try:
            return cls(
                attempt_id=_required_text(payload.get("attempt_id"), "attempt ID"),
                prompt_id=_required_text(payload.get("prompt_id"), "prompt ID"),
                module_id=_required_text(payload.get("module_id"), "module ID"),
                transcript=_required_text(payload.get("transcript"), "transcript"),
                evaluation=BMB830OralEvaluation.from_dict(cast(JsonObject, raw_evaluation)),
                created_at=datetime.fromisoformat(str(payload.get("created_at") or "")),
                model=str(payload.get("model") or "").strip(),
                prompt_eval_count=_non_negative_int(payload.get("prompt_eval_count")),
                eval_count=_non_negative_int(payload.get("eval_count")),
                total_duration_ns=_non_negative_int(payload.get("total_duration_ns")),
            )
        except (TypeError, ValueError) as exc:
            if isinstance(exc, BMB830OralSnapshotError):
                raise
            raise BMB830OralSnapshotError("Oral attempt metadata is malformed.") from exc


@dataclass(frozen=True, slots=True)
class BMB830OralSnapshot:
    """Versioned local history for oral-exam preparation."""

    schema_version: int
    active_prompt_id: str
    attempts: tuple[BMB830OralAttempt, ...]
    updated_at: datetime

    def __post_init__(self) -> None:
        if self.schema_version != BMB830_ORAL_SCHEMA_VERSION:
            raise ValueError("Unsupported BMB830 oral snapshot schema version.")
        if not self.active_prompt_id.strip():
            raise ValueError("BMB830 oral snapshots require an active prompt.")
        if len(self.attempts) > BMB830_ORAL_MAX_ATTEMPTS:
            raise ValueError("BMB830 oral snapshot exceeds the local retention limit.")
        if self.updated_at.tzinfo is None or self.updated_at.utcoffset() is None:
            raise ValueError("BMB830 oral snapshot timestamps must be timezone-aware.")
        attempt_ids = tuple(item.attempt_id for item in self.attempts)
        if len(attempt_ids) != len(set(attempt_ids)):
            raise ValueError("BMB830 oral attempt IDs must be unique.")

    @classmethod
    def empty(
        cls,
        active_prompt_id: str,
        *,
        now: datetime | None = None,
    ) -> BMB830OralSnapshot:
        return cls(
            schema_version=BMB830_ORAL_SCHEMA_VERSION,
            active_prompt_id=active_prompt_id,
            attempts=(),
            updated_at=now or datetime.now(UTC),
        )

    def with_active_prompt(
        self,
        prompt_id: str,
        *,
        now: datetime | None = None,
    ) -> BMB830OralSnapshot:
        if not prompt_id.strip():
            raise ValueError("Active oral prompt IDs cannot be blank.")
        return replace(self, active_prompt_id=prompt_id, updated_at=now or datetime.now(UTC))

    def append(
        self,
        attempt: BMB830OralAttempt,
        *,
        now: datetime | None = None,
    ) -> BMB830OralSnapshot:
        attempts = (*self.attempts, attempt)[-BMB830_ORAL_MAX_ATTEMPTS:]
        return replace(self, attempts=attempts, updated_at=now or datetime.now(UTC))

    def attempts_for(self, prompt_id: str) -> tuple[BMB830OralAttempt, ...]:
        return tuple(item for item in self.attempts if item.prompt_id == prompt_id)

    def attempts_for_module(self, module_id: str) -> tuple[BMB830OralAttempt, ...]:
        return tuple(item for item in self.attempts if item.module_id == module_id)

    def latest_for(self, prompt_id: str) -> BMB830OralAttempt | None:
        attempts = self.attempts_for(prompt_id)
        return attempts[-1] if attempts else None

    @property
    def average_score(self) -> float | None:
        if not self.attempts:
            return None
        return mean(attempt.evaluation.average_score for attempt in self.attempts)

    def criterion_average(self, criterion: OralCriterion) -> float | None:
        if not self.attempts:
            return None
        return mean(attempt.evaluation.score_for(criterion).score for attempt in self.attempts)

    def recommended_prompt(self, prompts: tuple[BMB830OralPrompt, ...]) -> BMB830OralPrompt:
        if not prompts:
            raise ValueError("Oral practice requires at least one prompt.")
        indexed = {prompt.prompt_id: index for index, prompt in enumerate(prompts)}
        return min(
            prompts,
            key=lambda prompt: (
                len(self.attempts_for(prompt.prompt_id)),
                indexed[prompt.prompt_id],
            ),
        )

    def to_json(self) -> str:
        payload: JsonObject = {
            "schema_version": self.schema_version,
            "active_prompt_id": self.active_prompt_id,
            "attempts": [attempt.to_dict() for attempt in self.attempts],
            "updated_at": self.updated_at.isoformat(),
        }
        return json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True)

    @classmethod
    def from_json(cls, raw: str) -> BMB830OralSnapshot:
        try:
            payload = json.loads(raw)
        except json.JSONDecodeError as exc:
            raise BMB830OralSnapshotError("BMB830 oral snapshot is not valid JSON.") from exc
        if not isinstance(payload, dict):
            raise BMB830OralSnapshotError("BMB830 oral snapshot must be a JSON object.")
        raw_attempts = payload.get("attempts")
        if not isinstance(raw_attempts, list) or not all(
            isinstance(item, dict) for item in raw_attempts
        ):
            raise BMB830OralSnapshotError("BMB830 oral attempts must be a list of objects.")
        try:
            return cls(
                schema_version=_non_negative_int(payload.get("schema_version")),
                active_prompt_id=_required_text(
                    payload.get("active_prompt_id"),
                    "active prompt ID",
                ),
                attempts=tuple(
                    BMB830OralAttempt.from_dict(cast(JsonObject, item)) for item in raw_attempts
                ),
                updated_at=datetime.fromisoformat(str(payload.get("updated_at") or "")),
            )
        except (TypeError, ValueError) as exc:
            if isinstance(exc, BMB830OralSnapshotError):
                raise
            raise BMB830OralSnapshotError("BMB830 oral snapshot metadata is malformed.") from exc


def bmb830_oral_prompt_bank(locale: AppLocale) -> tuple[BMB830OralPrompt, ...]:
    """Materialize stable prompts from localized authored Socratic questions."""

    prompts: list[BMB830OralPrompt] = []
    for localized_bundle in LOCALIZED_BUNDLES:
        module = localized_bundle.materialize(locale).module
        questions = module.tutor_support.socratic_questions[:2]
        if not questions:
            questions = (module.summary,)
        for index, question in enumerate(questions, start=1):
            prompts.append(
                BMB830OralPrompt(
                    prompt_id=f"bmb830.oral.{module.module_id}.q{index}",
                    module_id=module.module_id,
                    module_title=module.title,
                    question=question,
                    objective_ids=tuple(objective.objective_id for objective in module.objectives),
                    grading_criteria=module.tutor_support.grading_criteria,
                    source_basis=module.tutor_support.source_basis,
                )
            )
    identities = tuple(prompt.prompt_id for prompt in prompts)
    if len(identities) != len(set(identities)):
        raise ValueError("BMB830 oral prompt identities must be unique.")
    return tuple(prompts)


ORAL_EVALUATION_SCHEMA: JsonObject = {
    "type": "object",
    "properties": {
        "feedback": {"type": "string", "minLength": 1},
        "strengths": {"type": "array", "items": {"type": "string"}},
        "gaps": {"type": "array", "items": {"type": "string"}},
        "misconceptions": {"type": "array", "items": {"type": "string"}},
        "scores": {
            "type": "array",
            "minItems": 5,
            "maxItems": 5,
            "items": {
                "type": "object",
                "properties": {
                    "criterion": {
                        "type": "string",
                        "enum": [criterion.value for criterion in OralCriterion],
                    },
                    "score": {"type": "integer", "minimum": 0, "maximum": 4},
                    "evidence": {"type": "string", "minLength": 1},
                },
                "required": ["criterion", "score", "evidence"],
                "additionalProperties": False,
            },
        },
        "follow_up_question": {"type": "string", "minLength": 1},
        "recommended_next_action": {"type": "string", "minLength": 1},
        "confidence": {"type": "number", "minimum": 0.0, "maximum": 1.0},
        "needs_source_check": {"type": "boolean"},
    },
    "required": [
        "feedback",
        "strengths",
        "gaps",
        "misconceptions",
        "scores",
        "follow_up_question",
        "recommended_next_action",
        "confidence",
        "needs_source_check",
    ],
    "additionalProperties": False,
}


def parse_oral_evaluation(raw: str) -> BMB830OralEvaluation:
    """Decode a schema-constrained Ollama evaluation."""

    try:
        payload = json.loads(raw)
    except json.JSONDecodeError as exc:
        raise BMB830OralSnapshotError("Ollama oral evaluation was not valid JSON.") from exc
    if not isinstance(payload, dict):
        raise BMB830OralSnapshotError("Ollama oral evaluation must be a JSON object.")
    return BMB830OralEvaluation.from_dict(cast(JsonObject, payload))


def _string_tuple(value: object) -> tuple[str, ...]:
    if not isinstance(value, list):
        return ()
    normalized: list[str] = []
    for item in value[:12]:
        text = str(item or "").strip()[:600]
        if text and text not in normalized:
            normalized.append(text)
    return tuple(normalized)


def _required_text(value: object, label: str) -> str:
    text = str(value or "").strip()
    if not text:
        raise BMB830OralSnapshotError(f"BMB830 oral {label} cannot be blank.")
    return text


def _confidence(value: object) -> float:
    if isinstance(value, bool) or not isinstance(value, int | float):
        return 0.0
    return min(1.0, max(0.0, float(value)))


def _non_negative_int(value: object) -> int:
    if isinstance(value, bool) or not isinstance(value, int):
        return 0
    return max(0, value)


__all__ = [
    "BMB830_ORAL_MAX_ATTEMPTS",
    "BMB830_ORAL_SCHEMA_VERSION",
    "ORAL_EVALUATION_SCHEMA",
    "BMB830OralAttempt",
    "BMB830OralEvaluation",
    "BMB830OralPrompt",
    "BMB830OralSnapshot",
    "BMB830OralSnapshotError",
    "OralCriterion",
    "OralCriterionScore",
    "bmb830_oral_prompt_bank",
    "parse_oral_evaluation",
]
