"""Tests for Ollama thinking and schema-constrained chat payloads."""

from __future__ import annotations

from dataclasses import dataclass, field

import pytest

from computational_biomedicine_study_hub.integrations import (
    ChatMessage,
    ChatRole,
    JsonObject,
    OllamaChatClient,
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


def _response() -> JsonObject:
    return {
        "model": "qwen3.5:9b-q8_0",
        "message": {"role": "assistant", "content": '{"reply":"Question"}'},
        "done": True,
    }


def test_chat_sends_structured_schema_thinking_and_resource_options() -> None:
    transport = FakeTransport(_response())
    client = OllamaChatClient(transport=transport)
    schema: JsonObject = {
        "type": "object",
        "properties": {"reply": {"type": "string"}},
        "required": ["reply"],
    }

    client.chat(
        [ChatMessage(ChatRole.USER, "Use the schema")],
        think=True,
        format_schema=schema,
        num_ctx=16_384,
        num_predict=1_400,
        keep_alive="30m",
    )

    _, payload, _ = transport.post_calls[0]
    assert payload["think"] is True
    assert payload["format"] == schema
    assert payload["keep_alive"] == "30m"
    assert payload["options"] == {
        "temperature": 0.2,
        "num_ctx": 16_384,
        "num_predict": 1_400,
    }


def test_chat_accepts_named_thinking_effort() -> None:
    transport = FakeTransport(_response())
    client = OllamaChatClient(transport=transport)

    client.chat(
        [ChatMessage(ChatRole.USER, "Evaluate this")],
        think="high",
    )

    assert transport.post_calls[0][1]["think"] == "high"


@pytest.mark.parametrize("thinking", ["maximum", "", "HIGHER"])
def test_chat_rejects_unknown_thinking_values(thinking: str) -> None:
    client = OllamaChatClient(transport=FakeTransport(_response()))

    with pytest.raises(ValueError, match="Thinking"):
        client.chat(
            [ChatMessage(ChatRole.USER, "Question")],
            think=thinking,
        )


@pytest.mark.parametrize(
    ("argument", "value"),
    [("num_ctx", 0), ("num_ctx", -1), ("num_predict", 0), ("num_predict", -2)],
)
def test_chat_rejects_non_positive_generation_limits(argument: str, value: int) -> None:
    client = OllamaChatClient(transport=FakeTransport(_response()))
    kwargs = {argument: value}

    with pytest.raises(ValueError, match=argument):
        client.chat(
            [ChatMessage(ChatRole.USER, "Question")],
            **kwargs,  # type: ignore[arg-type]
        )
