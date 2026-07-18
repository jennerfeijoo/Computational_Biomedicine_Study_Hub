from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

import pytest

from computational_biomedicine_study_hub.integrations.ollama import (
    JsonObject,
    OllamaClient,
    OllamaConfig,
    OllamaProtocolError,
)


@dataclass
class FakeTransport:
    responses: dict[str, JsonObject]
    calls: list[tuple[str, float]] = field(default_factory=list)

    def get(self, url: str, *, timeout: float) -> JsonObject:
        self.calls.append((url, timeout))
        return self.responses[url]


def test_config_normalizes_local_server_urls() -> None:
    assert (
        OllamaConfig("http://localhost:11434").normalized_base_url()
        == "http://localhost:11434/api"
    )
    assert (
        OllamaConfig("http://localhost:11434/api/").normalized_base_url()
        == "http://localhost:11434/api"
    )


def test_client_reads_version_from_expected_endpoint() -> None:
    transport = FakeTransport(
        responses={"http://localhost:11434/api/version": {"version": "1.2.3"}}
    )
    client = OllamaClient(transport=transport)

    assert client.get_version() == "1.2.3"
    assert transport.calls == [("http://localhost:11434/api/version", 5.0)]


def test_client_lists_and_sorts_available_models() -> None:
    transport = FakeTransport(
        responses={
            "http://localhost:11434/api/tags": {
                "models": [
                    {
                        "name": "qwen3:27b",
                        "size": 17_000_000_000,
                        "details": {
                            "parameter_size": "27B",
                            "quantization_level": "Q4_K_M",
                            "family": "qwen3",
                        },
                    },
                    {"name": "embeddinggemma:latest", "details": {}},
                ]
            }
        }
    )
    client = OllamaClient(transport=transport)

    models = client.list_models()

    assert [model.name for model in models] == [
        "embeddinggemma:latest",
        "qwen3:27b",
    ]
    assert models[1].parameter_size == "27B"
    assert models[1].quantization_level == "Q4_K_M"
    assert models[1].family == "qwen3"


@pytest.mark.parametrize(
    "response",
    [
        {},
        {"models": "not-a-list"},
        {"models": None},
    ],
)
def test_client_rejects_invalid_model_lists(response: dict[str, Any]) -> None:
    transport = FakeTransport(
        responses={"http://localhost:11434/api/tags": response}
    )
    client = OllamaClient(transport=transport)

    with pytest.raises(OllamaProtocolError):
        client.list_models()
