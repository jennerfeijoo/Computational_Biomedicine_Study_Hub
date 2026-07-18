"""Optional integrations with local services."""

from __future__ import annotations

from .ollama import (
    OllamaClient,
    OllamaConfig,
    OllamaConnectionError,
    OllamaModel,
    OllamaProtocolError,
)

__all__ = [
    "OllamaClient",
    "OllamaConfig",
    "OllamaConnectionError",
    "OllamaModel",
    "OllamaProtocolError",
]
