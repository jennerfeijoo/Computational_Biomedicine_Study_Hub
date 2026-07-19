"""Low-level client and transport primitives for a local Ollama server."""

from __future__ import annotations

import json
from dataclasses import dataclass
from logging import getLogger
from typing import Any, Protocol
from urllib.error import HTTPError, URLError
from urllib.parse import urlsplit, urlunsplit
from urllib.request import Request, urlopen

JsonObject = dict[str, Any]
LOGGER = getLogger(__name__)


class OllamaError(RuntimeError):
    """Base exception for Ollama integration failures."""


class OllamaConnectionError(OllamaError):
    """Raised when the local Ollama API cannot be reached."""


class OllamaConfigurationError(OllamaError):
    """Raised when the configured Ollama URL cannot identify an HTTP service."""


class OllamaTimeoutError(OllamaConnectionError):
    """Raised when an Ollama request exceeds its configured timeout."""


class OllamaProtocolError(OllamaError):
    """Raised when Ollama returns malformed or unexpected data."""


@dataclass(frozen=True, slots=True)
class OllamaConfig:
    """Connection settings for the local Ollama API."""

    base_url: str = "http://localhost:11434/api"
    timeout_seconds: float = 5.0
    generation_timeout_seconds: float = 180.0

    def normalized_base_url(self) -> str:
        """Return one validated canonical API root ending in exactly one ``/api``."""
        value = self.base_url.strip()
        if not value:
            raise OllamaConfigurationError("The Ollama URL is empty.")

        parsed = urlsplit(value)
        if (
            parsed.scheme.casefold() not in {"http", "https"}
            or not parsed.netloc
            or parsed.query
            or parsed.fragment
            or parsed.username
            or parsed.password
        ):
            raise OllamaConfigurationError(
                "The Ollama URL must be a plain http(s) server URL without "
                "credentials, query parameters, or fragments."
            )

        segments = [segment for segment in parsed.path.split("/") if segment]
        while segments and segments[-1].casefold() in {"chat", "tags", "version"}:
            segments.pop()
        while (
            len(segments) >= 2
            and segments[-1].casefold() == "api"
            and segments[-2].casefold() == "api"
        ):
            segments.pop()
        if not segments or segments[-1].casefold() != "api":
            segments.append("api")

        return urlunsplit(
            (
                parsed.scheme.casefold(),
                parsed.netloc,
                "/" + "/".join(segments),
                "",
                "",
            )
        )


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
    """Small transport contract that keeps Ollama clients unit-testable."""

    def get(self, url: str, *, timeout: float) -> JsonObject:
        """Return a decoded JSON object from a GET request."""
        ...

    def post(
        self,
        url: str,
        payload: JsonObject,
        *,
        timeout: float,
    ) -> JsonObject:
        """Return a decoded JSON object from a JSON POST request."""
        ...


class UrllibJsonTransport:
    """Dependency-free HTTP transport for local Ollama JSON endpoints."""

    USER_AGENT = "Computational-Biomedicine-Study-Hub/0.1"

    def get(self, url: str, *, timeout: float) -> JsonObject:
        """Perform a GET request and decode one JSON object."""
        return self._request("GET", url, timeout=timeout)

    def post(
        self,
        url: str,
        payload: JsonObject,
        *,
        timeout: float,
    ) -> JsonObject:
        """Perform a JSON POST request and decode one JSON object."""
        body = json.dumps(payload, ensure_ascii=False).encode("utf-8")
        return self._request("POST", url, timeout=timeout, body=body)

    def _request(
        self,
        method: str,
        url: str,
        *,
        timeout: float,
        body: bytes | None = None,
    ) -> JsonObject:
        headers = {
            "Accept": "application/json",
            "User-Agent": self.USER_AGENT,
        }
        if body is not None:
            headers["Content-Type"] = "application/json; charset=utf-8"

        request = Request(url, data=body, headers=headers, method=method)

        try:
            with urlopen(request, timeout=timeout) as response:  # noqa: S310
                raw_content = response.read().decode("utf-8")
        except HTTPError as exc:
            detail = _read_http_error(exc)
            raise OllamaConnectionError(f"Ollama returned HTTP {exc.code}: {detail}") from exc
        except TimeoutError as exc:
            raise OllamaTimeoutError(
                f"The Ollama request exceeded its {timeout:g} second timeout."
            ) from exc
        except URLError as exc:
            if isinstance(exc.reason, TimeoutError):
                raise OllamaTimeoutError(
                    f"The Ollama request exceeded its {timeout:g} second timeout."
                ) from exc
            raise OllamaConnectionError(
                "No se pudo conectar con Ollama. Comprueba que el servicio "
                "esté activo y que la URL configurada sea correcta."
            ) from exc
        except OSError as exc:
            raise OllamaConnectionError(
                "No se pudo conectar con Ollama. Comprueba que el servicio "
                "esté activo y que la URL configurada sea correcta."
            ) from exc

        return _decode_json_object(raw_content)


def _read_http_error(error: HTTPError) -> str:
    """Extract Ollama's JSON error message when one is available."""
    raw_detail = error.read().decode("utf-8", errors="replace").strip()
    if raw_detail:
        try:
            payload = json.loads(raw_detail)
        except json.JSONDecodeError:
            return raw_detail
        if isinstance(payload, dict):
            message = str(payload.get("error") or "").strip()
            if message:
                return message
    return str(error.reason) or f"HTTP {error.code}"


def _decode_json_object(raw_content: str) -> JsonObject:
    """Decode and validate a JSON object response."""
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
        endpoint = f"{self.config.normalized_base_url()}/{path.lstrip('/')}"
        LOGGER.debug("Ollama GET endpoint=%s timeout=%s", endpoint, self.config.timeout_seconds)
        return endpoint
