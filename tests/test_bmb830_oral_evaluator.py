"""Tests for the grounded Ollama BMB830 oral evaluator."""

from __future__ import annotations

import json
from dataclasses import dataclass, field
from typing import Any, cast

import pytest

from computational_biomedicine_study_hub.i18n import AppLocale
from computational_biomedicine_study_hub.integrations import (
    ChatMessage,
    ChatResponse,
    ChatRole,
    OllamaChatClient,
)
from computational_biomedicine_study_hub.integrations.bmb830_oral import (
    BMB830OralEvaluator,
)
from computational_biomedicine_study_hub.learning.bmb830_oral_exam import (
    BMB830OralPrompt,
    OralCriterion,
)


def _payload() -> str:
    return json.dumps(
        {
            "feedback": "The answer identifies the estimand but needs a clearer assumption.",
            "strengths": ["Defined the estimand"],
            "gaps": ["Did not justify independence"],
            "misconceptions": [],
            "scores": [
                {
                    "criterion": criterion.value,
                    "score": 3,
                    "evidence": f"Evidence for {criterion.value}",
                }
                for criterion in OralCriterion
            ],
            "follow_up_question": "How would dependence change your analysis?",
            "recommended_next_action": "Review independence and clustered data",
            "confidence": 0.86,
            "needs_source_check": False,
        }
    )


@dataclass
class FakeChatClient:
    calls: list[tuple[tuple[ChatMessage, ...], dict[str, Any]]] = field(default_factory=list)

    def chat(self, messages, **kwargs):  # type: ignore[no-untyped-def]
        normalized = tuple(messages)
        self.calls.append((normalized, kwargs))
        return ChatResponse(
            model="test-model",
            message=ChatMessage(ChatRole.ASSISTANT, _payload()),
            prompt_eval_count=120,
            eval_count=70,
        )


def _prompt() -> BMB830OralPrompt:
    return BMB830OralPrompt(
        prompt_id="bmb830.oral.m01.q1",
        module_id="bmb830.m01",
        module_title="R foundations",
        question="How would you define the estimand?",
        objective_ids=("o1",),
        grading_criteria=("Justify the statistical target",),
        source_basis=("Authoritative source",),
    )


def test_evaluator_uses_thinking_schema_and_grounded_context() -> None:
    fake = FakeChatClient()
    evaluator = BMB830OralEvaluator(
        client=cast(OllamaChatClient, fake),
        model="test-model",
    )

    result = evaluator.evaluate(
        prompt=_prompt(),
        transcript="I define the estimand before selecting a model.",
        authoritative_context="<authoritative_course_context>Grounded material</authoritative_course_context>",
        locale=AppLocale.ENGLISH,
    )

    assert result.evaluation.follow_up_question == "How would dependence change your analysis?"
    assert result.evaluation.average_score == pytest.approx(3.0)
    messages, kwargs = fake.calls[0]
    assert messages[0].role is ChatRole.SYSTEM
    assert "exactly one central Socratic follow-up question" in messages[0].content
    assert "Grounded material" in messages[1].content
    assert "I define the estimand" in messages[1].content
    assert kwargs["think"] is True
    assert kwargs["num_ctx"] == 16_384
    assert kwargs["num_predict"] == 1_800
    assert kwargs["keep_alive"] == "30m"
    assert kwargs["format_schema"]["type"] == "object"


def test_evaluator_rejects_blank_transcript() -> None:
    evaluator = BMB830OralEvaluator(
        client=cast(OllamaChatClient, FakeChatClient()),
    )

    with pytest.raises(ValueError, match="transcript"):
        evaluator.evaluate(
            prompt=_prompt(),
            transcript="   ",
            authoritative_context="Context",
            locale=AppLocale.ENGLISH,
        )


def test_evaluator_includes_previous_follow_up_as_context() -> None:
    fake = FakeChatClient()
    evaluator = BMB830OralEvaluator(client=cast(OllamaChatClient, fake))

    evaluator.evaluate(
        prompt=_prompt(),
        transcript="Updated answer",
        authoritative_context="Context",
        locale=AppLocale.ENGLISH,
        previous_follow_up="Why is independence important?",
    )

    assert "Why is independence important?" in fake.calls[0][0][1].content
