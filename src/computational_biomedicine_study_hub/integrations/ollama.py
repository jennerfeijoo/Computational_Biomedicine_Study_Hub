"""Connection and model-discovery client for a local Ollama server.

This increment deliberately supports only connection checks and model listing.
Chat, tutoring, retrieval and assessment are separate later increments.
"""

from __future__ import annotations

import json
from dataclasses import dataclass
from typing import Any, Protocol
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen

JsonObject = dict[str, Any]


class OllamaError(RuntimeError):
    """Base exception for Ollama integration failures."""


class OllamaConnectionError(OllamaError):
    """Raised when the local Ollama API cannot be reached."""


class OllamaProtocolError(OllamaError):
    """Raised when Ollama returns malformed or unexpected data."""


@dataclass(frozen=True, slots=True)
class OllamaConfig:
    """Connection settings for the local Ollama API."""

    base_url: str = "http://localhost:11434/api"
    timeout_seconds: float = 5.0

    def normalized_base_url(self) -> str:
        """Return a normalized URL ending in ``/api``."""
        value = self.base_url.strip().rstrip("/")
        if not value:
            value = "http://localhost:11434/api"
        if not value.endswith("/api"):
            value = f"{value}/api"
        return value


@dataclass(frozen=True, slots=True)
class OllamaModel:
    """Metadata for one locally available Ollama model."""

    name: str
    parameter_size: str = ""
    quantization_level: str = ""
    family: str = ""
    size_bytes: int = 0

    @classmethod
    def from_api(cls, payload: JsonObject) -> OllamaModel:
        """Construct a model from the ``GET /api/tags`` response."""
        raw_details = payload.get("details")
        details = raw_details if isinstance(raw_details, dict) else {}

        raw_size = payload.get("size", 0)
        size_bytes = raw_size if isinstance(raw_size, int) else 0

        return cls(
            name=str(payload.get("name") or payload.get("model") or "").strip(),
            parameter_size=str(details.get("parameter_size") or "").strip(),
            quantization_level=str(details.get("quantization_level") or "").strip(),
            family=str(details.get("family") or "").strip(),
            size_bytes=size_bytes,
        )


class JsonTransport(Protocol):
    """Small transport contract that keeps the client unit-testable."""

    def get(self, url: str, *, timeout: float) -> JsonObject:
        """Return a decoded JSON object from a GET request."""
        ...


class UrllibJsonTransport:
    """Standard-library transport for local JSON endpoints."""

    def get(self, url: str, *, timeout: float) -> JsonObject:
        request = Request(
            url,
            headers={
                "Accept": "application/json",
                "User-Agent": "Computational-Biomedicine-Study-Hub/0.1",
            },
            method="GET",
        )

        try:
            with urlopen(request, timeout=timeout) as response:  # noqa: S310
                raw_content = response.read().decode("utf-8")
        except HTTPError as exc:
            detail = exc.read().decode("utf-8", errors="replace").strip()
            message = detail or str(exc.reason) or f"HTTP {exc.code}"
            raise OllamaConnectionError(f"Ollama returned HTTP {exc.code}: {message}") from exc
        except (URLError, TimeoutError, OSError) as exc:
            raise OllamaConnectionError(
                "No se pudo conectar con Ollama. Comprueba que el servicio "
                "esté activo y que la URL configurada sea correcta."
            ) from exc

        try:
            payload = json.loads(raw_content)
        except json.JSONDecodeError as exc:
            raise OllamaProtocolError("Ollama returned invalid JSON.") from exc

        if not isinstance(payload, dict):
            raise OllamaProtocolError("Ollama returned a JSON value that was not an object.")
        return payload


class OllamaClient:
    """Check connectivity and discover locally installed models."""

    def __init__(
        self,
        config: OllamaConfig | None = None,
        transport: JsonTransport | None = None,
    ) -> None:
        self.config = config or OllamaConfig()
        self._transport = transport or UrllibJsonTransport()

    def get_version(self) -> str:
        """Return the version reported by ``GET /api/version``."""
        payload = self._transport.get(
            self._endpoint("version"),
            timeout=self.config.timeout_seconds,
        )
        version = str(payload.get("version") or "").strip()
        if not version:
            raise OllamaProtocolError("Ollama did not report a version.")
        return version

    def list_models(self) -> tuple[OllamaModel, ...]:
        """Return models reported by ``GET /api/tags``."""
        payload = self._transport.get(
            self._endpoint("tags"),
            timeout=self.config.timeout_seconds,
        )
        raw_models = payload.get("models")
        if not isinstance(raw_models, list):
            raise OllamaProtocolError("Ollama did not return a valid model list.")

        models: list[OllamaModel] = []
        for raw_model in raw_models:
            if not isinstance(raw_model, dict):
                continue
            model = OllamaModel.from_api(raw_model)
            if model.name:
                models.append(model)

        return tuple(sorted(models, key=lambda item: item.name.casefold()))

    def _endpoint(self, path: str) -> str:
        return f"{self.config.normalized_base_url()}/{path.lstrip('/')}"
