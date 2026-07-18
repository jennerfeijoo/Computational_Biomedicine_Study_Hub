from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

import pytest

from computational_biomedicine_study_hub.integrations import (
    DEFAULT_CHAT_MODEL,
    ChatMessage,
    ChatRole,
    JsonObject,
    OllamaChatClient,
    OllamaConfig,
    OllamaProtocolError,
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


def completed_response(**overrides: Any) -> JsonObject:
    response: JsonObject = {
        "model": DEFAULT_CHAT_MODEL,
        "message": {
            "role": "assistant",
            "content": "Una función transforma entradas en una salida definida.",
        },
        "done": True,
        "done_reason": "stop",
        "prompt_eval_count": 21,
        "eval_count": 12,
        "total_duration": 3_000_000,
    }
    response.update(overrides)
    return response


def test_chat_uses_preferred_model_and_non_streaming_payload() -> None:
    transport = FakeTransport(completed_response())
    config = OllamaConfig(generation_timeout_seconds=240.0)
    client = OllamaChatClient(config=config, transport=transport)

    response = client.chat(
        [
            ChatMessage(ChatRole.SYSTEM, "Responde de forma precisa."),
            ChatMessage(ChatRole.USER, "¿Qué es una función?"),
        ]
    )

    assert response.model == DEFAULT_CHAT_MODEL
    assert response.content.startswith("Una función")
    assert response.done_reason == "stop"
    assert response.prompt_eval_count == 21
    assert response.eval_count == 12
    assert response.total_duration_ns == 3_000_000

    assert len(transport.post_calls) == 1
    url, payload, timeout = transport.post_calls[0]
    assert url == "http://localhost:11434/api/chat"
    assert timeout == 240.0
    assert payload == {
        "model": "qwen3.6:27b",
        "messages": [
            {"role": "system", "content": "Responde de forma precisa."},
            {"role": "user", "content": "¿Qué es una función?"},
        ],
        "stream": False,
        "think": False,
        "keep_alive": "10m",
        "options": {"temperature": 0.2},
    }


def test_chat_accepts_an_explicit_model_and_generation_options() -> None:
    transport = FakeTransport(completed_response(model="ornith:9b"))
    client = OllamaChatClient(transport=transport)

    response = client.chat(
        [ChatMessage(ChatRole.USER, "Resume el concepto.")],
        model="ornith:9b",
        temperature=0.0,
        keep_alive="2m",
    )

    assert response.model == "ornith:9b"
    _, payload, _ = transport.post_calls[0]
    assert payload["model"] == "ornith:9b"
    assert payload["options"] == {"temperature": 0.0}
    assert payload["keep_alive"] == "2m"


def test_chat_message_rejects_blank_content() -> None:
    with pytest.raises(ValueError, match="cannot be empty"):
        ChatMessage(ChatRole.USER, "   ")


@pytest.mark.parametrize("temperature", [-0.1, 2.1, float("inf"), float("nan")])
def test_chat_rejects_invalid_temperatures(temperature: float) -> None:
    client = OllamaChatClient(transport=FakeTransport(completed_response()))

    with pytest.raises(ValueError, match="Temperature"):
        client.chat(
            [ChatMessage(ChatRole.USER, "Pregunta")],
            temperature=temperature,
        )


def test_chat_requires_at_least_one_message() -> None:
    client = OllamaChatClient(transport=FakeTransport(completed_response()))

    with pytest.raises(ValueError, match="At least one"):
        client.chat([])


@pytest.mark.parametrize(
    "response",
    [
        {},
        {"done": False, "message": {"role": "assistant", "content": "x"}},
        {"done": True, "message": "not-an-object"},
        {"done": True, "message": {"role": "user", "content": "x"}},
        {"done": True, "message": {"role": "assistant", "content": ""}},
    ],
)
def test_chat_rejects_malformed_responses(response: JsonObject) -> None:
    client = OllamaChatClient(transport=FakeTransport(response))

    with pytest.raises(OllamaProtocolError):
        client.chat([ChatMessage(ChatRole.USER, "Pregunta")])
