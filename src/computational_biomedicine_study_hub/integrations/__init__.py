"""Optional integrations with local services."""

from __future__ import annotations

from .ollama import (
    JsonObject,
    JsonTransport,
    OllamaClient,
    OllamaConfig,
    OllamaConnectionError,
    OllamaError,
    OllamaModel,
    OllamaProtocolError,
    UrllibJsonTransport,
)
from .ollama_chat import (
    DEFAULT_CHAT_MODEL,
    ChatMessage,
    ChatResponse,
    ChatRole,
    OllamaChatClient,
)

__all__ = [
    "DEFAULT_CHAT_MODEL",
    "ChatMessage",
    "ChatResponse",
    "ChatRole",
    "JsonObject",
    "JsonTransport",
    "OllamaChatClient",
    "OllamaClient",
    "OllamaConfig",
    "OllamaConnectionError",
    "OllamaError",
    "OllamaModel",
    "OllamaProtocolError",
    "UrllibJsonTransport",
]
