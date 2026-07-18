"""Optional integrations with local services."""

from __future__ import annotations

from .ollama import (
    OllamaClient,
    OllamaConfig,
    OllamaConnectionError,
    OllamaModel,
    OllamaProtocolError,
)
from .ollama_chat import (
    ChatMessage,
    ChatResponse,
    ChatRole,
    DEFAULT_CHAT_MODEL,
    OllamaChatClient,
)

__all__ = [
    "ChatMessage",
    "ChatResponse",
    "ChatRole",
    "DEFAULT_CHAT_MODEL",
    "OllamaChatClient",
    "OllamaClient",
    "OllamaConfig",
    "OllamaConnectionError",
    "OllamaModel",
    "OllamaProtocolError",
]
