from __future__ import annotations

from dataclasses import dataclass, field

import pytest

from computational_biomedicine_study_hub.content.dm857 import BUNDLES
from computational_biomedicine_study_hub.content.python_challenges import (
    PythonChallenge,
    python_challenge_for,
)
from computational_biomedicine_study_hub.integrations import (
    ChatMessage,
    ChatResponse,
    ChatRole,
)
from computational_biomedicine_study_hub.learning.progress import ConfidenceLevel
from computational_biomedicine_study_hub.learning.python_challenge import (
    ChallengeCaseStatus,
    PythonChallengeCaseResult,
    PythonChallengeResult,
)
from computational_biomedicine_study_hub.tutoring import (
    ChallengeDiagnostic,
    ChallengeTutorPromptBuilder,
    ChallengeTutorService,
)


def _module(module_id: str = "dm857.m07"):
    return next(bundle.module for bundle in BUNDLES if bundle.module.module_id == module_id)


def _challenge() -> PythonChallenge:
    challenge = python_challenge_for(
        "m07.p04",
        "def unique_count(values):\n    pass",
        _module().locale,
    )
    assert challenge is not None
    return challenge


def _result() -> PythonChallengeResult:
    return PythonChallengeResult(
        exercise_id="m07.p04",
        visible_results=(
            PythonChallengeCaseResult(
                case_id="duplicates",
                description="Cuenta correctamente enteros repetidos.",
                status=ChallengeCaseStatus.FAILED,
            ),
            PythonChallengeCaseResult(
                case_id="empty",
                description="La colección vacía contiene cero elementos únicos.",
                status=ChallengeCaseStatus.PASSED,
            ),
        ),
        hidden_passed=1,
        hidden_total=2,
        duration_ms=31,
    )


def _diagnostic() -> ChallengeDiagnostic:
    return ChallengeDiagnostic.from_attempt(
        challenge=_challenge(),
        result=_result(),
        confidence=ConfidenceLevel.HIGH,
        submitted_source="def unique_count(values):\n    return len(values)",
        prompt="Escribe unique_count(values).",
        reference_solution="def unique_count(values):\n    return len(set(values))",
        explanation="El conjunto elimina duplicados antes de contar.",
    )


def test_verified_payload_contains_objectives_without_hidden_contracts() -> None:
    challenge = _challenge()
    payload = _diagnostic().verified_payload(_module())

    assert '"deterministic_grade": false' in payload
    assert '"confidence": "high"' in payload
    assert '"passed": 1' in payload
    assert '"total": 2' in payload
    assert '"definitions_withheld": true' in payload
    assert "m07.o6" in payload
    assert "m07.o8" in payload
    assert all(case.case_id not in payload for case in challenge.hidden_cases)
    assert all(case.assertion not in payload for case in challenge.hidden_cases)


def test_prompt_combines_authored_sources_and_verified_diagnostic() -> None:
    question = "¿Por qué mi función cuenta repetidos como elementos distintos?"
    prompt = ChallengeTutorPromptBuilder(_module()).build(_diagnostic(), question)

    assert prompt.messages[0].role is ChatRole.SYSTEM
    assert prompt.messages[1].role is ChatRole.USER
    assert "calificación determinista es inmutable" in prompt.messages[0].content
    assert "No inventes ni reveles" in prompt.messages[0].content
    assert "<material_autorizado>" in prompt.messages[1].content
    assert "<contexto_verificado>" in prompt.messages[1].content
    assert prompt.messages[1].content.endswith(question)
    assert '"deterministic_grade": false' in prompt.messages[1].content
    assert prompt.source_ids[:2] == (
        "dm857.m07.overview",
        "dm857.m07.tutor-guidance",
    )
    assert all(
        case.assertion not in prompt.messages[1].content for case in _challenge().hidden_cases
    )


def test_prompt_rejects_a_diagnostic_from_another_module() -> None:
    with pytest.raises(ValueError, match="does not belong"):
        ChallengeTutorPromptBuilder(_module("dm857.m01")).build(
            _diagnostic(),
            "Ayúdame a interpretar el fallo.",
        )


@dataclass
class _FakeChatClient:
    calls: list[tuple[tuple[ChatMessage, ...], float]] = field(default_factory=list)

    def chat(
        self,
        messages: tuple[ChatMessage, ...],
        *,
        temperature: float = 0.2,
    ) -> ChatResponse:
        self.calls.append((messages, temperature))
        return ChatResponse(
            model="qwen3.5:9b-q8_0",
            message=ChatMessage(
                ChatRole.ASSISTANT,
                "Tu función está contando posiciones, no valores únicos.",
            ),
            done_reason="stop",
        )


def test_service_uses_low_temperature_and_returns_source_traceability() -> None:
    client = _FakeChatClient()
    service = ChallengeTutorService(_module(), client=client)

    response = service.ask(_diagnostic(), "Dame una pista, no la solución completa.")

    assert len(client.calls) == 1
    assert client.calls[0][1] == 0.1
    assert response.model == "qwen3.5:9b-q8_0"
    assert response.content.startswith("Tu función")
    assert response.source_ids[:2] == (
        "dm857.m07.overview",
        "dm857.m07.tutor-guidance",
    )
