"""Tests for source-bounded Ollama support of DM847 written responses."""

from __future__ import annotations

from dataclasses import dataclass, field

import pytest

from computational_biomedicine_study_hub.content.dm847 import BUNDLES
from computational_biomedicine_study_hub.i18n import AppLocale
from computational_biomedicine_study_hub.integrations import (
    JsonObject,
    OllamaChatClient,
    OllamaConfig,
)
from computational_biomedicine_study_hub.learning.dm847_written_assessment import (
    WrittenFeedbackMode,
)
from computational_biomedicine_study_hub.tutoring import (
    WrittenFeedbackPromptBuilder,
    WrittenFeedbackRequest,
    WrittenFeedbackService,
)


@dataclass
class FakeTransport:
    response: JsonObject
    post_calls: list[tuple[str, JsonObject, float]] = field(default_factory=list)

    def get(self, url: str, *, timeout: float) -> JsonObject:
        raise AssertionError(f"Unexpected GET request: {url} ({timeout})")

    def post(
        self,
        url: str,
        payload: JsonObject,
        *,
        timeout: float,
    ) -> JsonObject:
        self.post_calls.append((url, payload, timeout))
        return self.response


def _request(mode: WrittenFeedbackMode) -> WrittenFeedbackRequest:
    return WrittenFeedbackRequest(
        prompt_id="dm847.w10",
        task_prompt="Design a leakage-free predictive omics study.",
        focus_points=(
            "experimental unit",
            "preprocessing within training folds",
            "grouped nested validation",
        ),
        draft=(
            "The patient is the independent unit. I would split patients before fitting any "
            "normalisation, imputation, feature selection, or hyperparameter. Inner folds select "
            "the model and outer folds estimate performance. A final test set is used once after "
            "the pipeline is frozen, with calibration and error analysis reported."
        ),
        mode=mode,
        locale=AppLocale.ENGLISH,
    )


@pytest.mark.parametrize("mode", list(WrittenFeedbackMode))
def test_written_feedback_prompt_is_grounded_and_non_grading(
    mode: WrittenFeedbackMode,
) -> None:
    module = BUNDLES[-1].module
    prompt = WrittenFeedbackPromptBuilder(module).build(_request(mode))

    assert len(prompt.messages) == 2
    assert prompt.source_ids
    assert prompt.source_ids[0] == "dm847.m10.overview"
    system = prompt.messages[0].content
    user = prompt.messages[1].content
    assert "Do not assign an official grade" in system
    assert "authorised module material" in system
    assert "<authorised_module_material>" in user
    assert "<learner_draft>" in user
    assert all(source_id in user for source_id in prompt.source_ids)


def test_written_feedback_service_uses_configured_model_and_low_temperature() -> None:
    transport = FakeTransport(
        {
            "model": "qwen3.5:9b-q8_0",
            "message": {
                "role": "assistant",
                "content": "Strengths: the split unit is correct [dm847.m10.overview].",
            },
            "done": True,
            "done_reason": "stop",
        }
    )
    client = OllamaChatClient(
        OllamaConfig(generation_timeout_seconds=220.0),
        transport=transport,
    )
    service = WrittenFeedbackService(client, model="qwen3.5:9b-q8_0")

    response = service.generate(BUNDLES[-1].module, _request(WrittenFeedbackMode.CONTENT_REVIEW))

    assert response.mode is WrittenFeedbackMode.CONTENT_REVIEW
    assert response.model == "qwen3.5:9b-q8_0"
    assert response.source_ids
    assert "Strengths" in response.content
    assert len(transport.post_calls) == 1
    url, payload, timeout = transport.post_calls[0]
    assert url == "http://localhost:11434/api/chat"
    assert timeout == 220.0
    assert payload["model"] == "qwen3.5:9b-q8_0"
    assert payload["options"] == {"temperature": 0.1}
    assert payload["stream"] is False
    assert payload["think"] is False
