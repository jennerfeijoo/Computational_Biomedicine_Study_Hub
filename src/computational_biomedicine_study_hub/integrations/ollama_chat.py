"""Typed non-streaming chat generation for the local Ollama API.

This module deliberately provides only transport-level message generation. Tutor
prompts, knowledge retrieval, evaluation policy and user-interface concerns belong
to later layers.
"""

from __future__ import annotations

from collections.abc import Iterable
from dataclasses import dataclass
from enum import StrEnum
from math import isfinite
from typing import Any

from .ollama import (
    JsonObject,
    JsonTransport,
    OllamaConfig,
    OllamaProtocolError,
    UrllibJsonTransport,
)

DEFAULT_CHAT_MODEL = "qwen3.6:27b"


class ChatRole(StrEnum):
    """Roles accepted by Ollama's chat message schema."""

    SYSTEM = "system"
    USER = "user"
    ASSISTANT = "assistant"


@dataclass(frozen=True, slots=True)
class ChatMessage:
    """One validated message in a chat history."""

    role: ChatRole
    content: str

    def __post_init__(self) -> None:
        if not self.content.strip():
            raise ValueError("Chat message content cannot be empty.")

    def to_api(self) -> JsonObject:
        """Serialize the message for Ollama's REST API."""
        return {"role": self.role.value, "content": self.content.strip()}


@dataclass(frozen=True, slots=True)
class ChatResponse:
    """Validated result from one non-streaming chat request."""

    model: str
    message: ChatMessage
    done_reason: str = ""
    prompt_eval_count: int = 0
    eval_count: int = 0
    total_duration_ns: int = 0

    @property
    def content(self) -> str:
        """Return the assistant's final textual response."""
        return self.message.content


class OllamaChatClient:
    """Generate complete assistant messages through ``POST /api/chat``."""

    def __init__(
        self,
        config: OllamaConfig | None = None,
        transport: JsonTransport | None = None,
    ) -> None:
        self.config = config or OllamaConfig()
        self._transport = transport or UrllibJsonTransport()

    def chat(
        self,
        messages: Iterable[ChatMessage],
        *,
        model: str = DEFAULT_CHAT_MODEL,
        temperature: float = 0.2,
        keep_alive: str = "10m",
    ) -> ChatResponse:
        """Generate one complete assistant response.

        Streaming and separate reasoning output are disabled intentionally. This
        makes the result deterministic to parse and prevents internal reasoning
        traces from becoming part of the study interface.
        """
        normalized_model = model.strip()
        if not normalized_model:
            raise ValueError("An Ollama model name is required.")
        if not isfinite(temperature) or not 0.0 <= temperature <= 2.0:
            raise ValueError("Temperature must be a finite value from 0.0 to 2.0.")

        message_list = tuple(messages)
        if not message_list:
            raise ValueError("At least one chat message is required.")

        payload: JsonObject = {
            "model": normalized_model,
            "messages": [message.to_api() for message in message_list],
            "stream": False,
            "think": False,
            "keep_alive": keep_alive,
            "options": {"temperature": temperature},
        }
        response = self._transport.post(
            self._endpoint("chat"),
            payload,
            timeout=self.config.generation_timeout_seconds,
        )
        return self._parse_response(response, requested_model=normalized_model)

    def _parse_response(
        self,
        payload: JsonObject,
        *,
        requested_model: str,
    ) -> ChatResponse:
        done = payload.get("done")
        if done is not True:
            raise OllamaProtocolError(
                "Ollama did not return a completed non-streaming chat response."
            )

        raw_message = payload.get("message")
        if not isinstance(raw_message, dict):
            raise OllamaProtocolError("Ollama did not return a valid chat message.")

        role_value = str(raw_message.get("role") or "").strip()
        if role_value != ChatRole.ASSISTANT.value:
            raise OllamaProtocolError(
                "Ollama returned a chat message with an unexpected role."
            )

        content = str(raw_message.get("content") or "").strip()
        if not content:
            raise OllamaProtocolError("Ollama returned an empty assistant message.")

        model = str(payload.get("model") or requested_model).strip()
        return ChatResponse(
            model=model,
            message=ChatMessage(ChatRole.ASSISTANT, content),
            done_reason=str(payload.get("done_reason") or "").strip(),
            prompt_eval_count=_non_negative_int(payload.get("prompt_eval_count")),
            eval_count=_non_negative_int(payload.get("eval_count")),
            total_duration_ns=_non_negative_int(payload.get("total_duration")),
        )

    def _endpoint(self, path: str) -> str:
        return f"{self.config.normalized_base_url()}/{path.lstrip('/')}"


def _non_negative_int(value: Any) -> int:
    """Normalize optional Ollama counters without accepting booleans."""
    if isinstance(value, bool) or not isinstance(value, int):
        return 0
    return max(0, value)


__all__ = [
    "ChatMessage",
    "ChatResponse",
    "ChatRole",
    "DEFAULT_CHAT_MODEL",
    "OllamaChatClient",
]
