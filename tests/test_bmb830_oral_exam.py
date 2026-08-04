"""Domain tests for grounded BMB830 oral-exam practice."""

from __future__ import annotations

import json
from datetime import UTC, datetime, timedelta

import pytest

from computational_biomedicine_study_hub.i18n import AppLocale
from computational_biomedicine_study_hub.learning.bmb830_oral_exam import (
    BMB830OralAttempt,
    BMB830OralEvaluation,
    BMB830OralSnapshot,
    BMB830OralSnapshotError,
    OralCriterion,
    OralCriterionScore,
    bmb830_oral_prompt_bank,
    parse_oral_evaluation,
)

NOW = datetime(2026, 8, 4, 12, 0, tzinfo=UTC)


def _scores(value: int = 3) -> tuple[OralCriterionScore, ...]:
    return tuple(
        OralCriterionScore(criterion, value, f"Evidence for {criterion.value}")
        for criterion in OralCriterion
    )


def _evaluation(value: int = 3) -> BMB830OralEvaluation:
    return BMB830OralEvaluation(
        feedback="The response is mostly sound but needs a clearer limitation.",
        strengths=("Selected an appropriate statistical approach",),
        gaps=("Did not discuss sampling assumptions",),
        misconceptions=(),
        scores=_scores(value),
        follow_up_question="Which assumption is most consequential here, and why?",
        recommended_next_action="Revise the answer around assumptions and uncertainty",
        confidence=0.8,
    )


def _attempt(prompt_id: str, module_id: str, *, value: int = 3) -> BMB830OralAttempt:
    return BMB830OralAttempt(
        attempt_id=f"attempt-{prompt_id}-{value}",
        prompt_id=prompt_id,
        module_id=module_id,
        transcript="I would begin by defining the estimand and checking the assumptions.",
        evaluation=_evaluation(value),
        created_at=NOW + timedelta(minutes=value),
        model="test-model",
    )


def test_prompt_bank_is_grounded_localized_and_identity_stable() -> None:
    spanish = bmb830_oral_prompt_bank(AppLocale.SPANISH_SPAIN)
    english = bmb830_oral_prompt_bank(AppLocale.ENGLISH)
    danish = bmb830_oral_prompt_bank(AppLocale.DANISH_DENMARK)

    assert len(spanish) >= 12
    assert tuple(prompt.prompt_id for prompt in spanish) == tuple(
        prompt.prompt_id for prompt in english
    )
    assert tuple(prompt.prompt_id for prompt in english) == tuple(
        prompt.prompt_id for prompt in danish
    )
    assert all(prompt.grading_criteria for prompt in english)
    assert all(prompt.source_basis for prompt in english)
    assert spanish[0].question != english[0].question


def test_evaluation_requires_all_formative_criteria_in_stable_order() -> None:
    with pytest.raises(ValueError, match="every criterion"):
        BMB830OralEvaluation(
            feedback="Feedback",
            strengths=(),
            gaps=(),
            misconceptions=(),
            scores=_scores()[:-1],
            follow_up_question="Question?",
            recommended_next_action="Next",
            confidence=0.5,
        )


def test_evaluation_converts_to_provisional_mentor_observation() -> None:
    evaluation = _evaluation()

    observation = evaluation.to_mentor_observation()

    assert observation.demonstrated == evaluation.strengths
    assert observation.gaps == evaluation.gaps
    assert observation.next_question == evaluation.follow_up_question
    assert observation.confidence == evaluation.confidence


def test_snapshot_round_trip_and_recommended_prompt_balance_coverage() -> None:
    prompts = bmb830_oral_prompt_bank(AppLocale.ENGLISH)[:3]
    snapshot = BMB830OralSnapshot.empty(prompts[0].prompt_id, now=NOW)
    snapshot = snapshot.append(
        _attempt(prompts[0].prompt_id, prompts[0].module_id),
        now=NOW,
    )

    restored = BMB830OralSnapshot.from_json(snapshot.to_json())

    assert restored == snapshot
    assert restored.recommended_prompt(prompts).prompt_id == prompts[1].prompt_id
    assert restored.average_score == pytest.approx(3.0)
    assert restored.criterion_average(OralCriterion.ACCURACY) == pytest.approx(3.0)


def test_parse_oral_evaluation_accepts_schema_constrained_output() -> None:
    payload = _evaluation().to_dict()

    parsed = parse_oral_evaluation(json.dumps(payload))

    assert parsed == _evaluation()


def test_parse_oral_evaluation_rejects_unstructured_output() -> None:
    with pytest.raises(BMB830OralSnapshotError, match="not valid JSON"):
        parse_oral_evaluation("normal prose")


def test_oral_attempt_rejects_naive_timestamp() -> None:
    with pytest.raises(ValueError, match="timezone-aware"):
        BMB830OralAttempt(
            attempt_id="attempt",
            prompt_id="prompt",
            module_id="module",
            transcript="Answer",
            evaluation=_evaluation(),
            created_at=datetime(2026, 8, 4, 12, 0),
        )
