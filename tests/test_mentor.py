"""Regression tests for structured Socratic mentor behaviour and journal state."""

from __future__ import annotations

import json
from datetime import UTC, datetime, timedelta

import pytest

from computational_biomedicine_study_hub.integrations import (
    ChatMessage,
    ChatResponse,
    ChatRole,
)
from computational_biomedicine_study_hub.learning.mentor import (
    MentorJournalSnapshot,
    MentorMode,
    MentorObservation,
    MentorSnapshotError,
    MentorTurnRecord,
    mentor_system_prompt,
    parse_mentor_turn,
)

NOW = datetime(2026, 8, 4, 12, 0, tzinfo=UTC)


def _structured_response() -> ChatResponse:
    payload = {
        "reply": "¿Qué evidencia del gráfico apoya esa interpretación?",
        "observation": {
            "demonstrated": ["Distingue asociación de causalidad"],
            "gaps": ["No justificó el tamaño del efecto"],
            "misconceptions": [],
            "recommended_next_action": "Revisar el estimando y volver a interpretar el intervalo",
            "next_question": "¿Qué representa exactamente el intervalo de confianza?",
            "confidence": 0.82,
            "needs_source_check": False,
        },
    }
    return ChatResponse(
        model="qwen3.5:9b-q8_0",
        message=ChatMessage(ChatRole.ASSISTANT, json.dumps(payload, ensure_ascii=False)),
        prompt_eval_count=100,
        eval_count=40,
    )


def _turn(
    *,
    session_id: str = "session-a",
    created_at: datetime = NOW,
    context: str = "BMB830 | Module 2 | Assessment",
) -> MentorTurnRecord:
    return MentorTurnRecord(
        session_id=session_id,
        created_at=created_at,
        context=context,
        mode=MentorMode.SOCRATIC,
        user_message="La correlación demuestra causalidad.",
        assistant_message="¿Qué alternativa podría explicar la asociación?",
        observation=MentorObservation(
            gaps=("Confunde asociación y causalidad",),
            misconceptions=("Interpreta correlación como causalidad",),
            recommended_next_action="Comparar confusión, mediación y causalidad",
            next_question="¿Qué variable de confusión plausible propondrías?",
            confidence=0.9,
        ),
        model="test-model",
    )


def test_parse_mentor_turn_separates_visible_reply_from_private_observation() -> None:
    result = parse_mentor_turn(_structured_response())

    assert result.content == "¿Qué evidencia del gráfico apoya esa interpretación?"
    assert result.response.message.role is ChatRole.ASSISTANT
    assert result.observation.demonstrated == ("Distingue asociación de causalidad",)
    assert result.observation.gaps == ("No justificó el tamaño del efecto",)
    assert result.observation.confidence == pytest.approx(0.82)
    assert result.response.prompt_eval_count == 100


def test_parse_mentor_turn_rejects_unstructured_model_output() -> None:
    response = ChatResponse(
        model="test-model",
        message=ChatMessage(ChatRole.ASSISTANT, "Una respuesta normal"),
    )

    with pytest.raises(MentorSnapshotError, match="not valid JSON"):
        parse_mentor_turn(response)


def test_socratic_prompt_requires_one_question_and_protects_mastery() -> None:
    prompt = mentor_system_prompt(
        context="DM847 | Hidden Markov models",
        memory="No previous mentor observations are available.",
        locale_name="English",
        mode=MentorMode.SOCRATIC,
    )

    assert "Ask exactly one central question at a time" in prompt
    assert "Do not immediately reveal the complete answer" in prompt
    assert "Never invent" in prompt
    assert "objective mastery" in prompt
    assert "<response_schema>" in prompt
    assert "<current_context>" in prompt
    assert "<provisional_mentor_memory>" in prompt


def test_journal_round_trip_restores_latest_session_and_chat_history() -> None:
    first = _turn(created_at=NOW - timedelta(hours=2))
    second = _turn(
        session_id="session-b",
        created_at=NOW,
        context="DM857 | Recursion | Practice",
    )
    snapshot = MentorJournalSnapshot.empty(now=NOW - timedelta(days=1)).append(first).append(second)

    restored = MentorJournalSnapshot.from_json(snapshot.to_json())

    assert restored == snapshot
    assert restored.latest_session_id == "session-b"
    assert restored.latest_session_turns() == (second,)
    assert tuple(message.role for message in restored.chat_history()) == (
        ChatRole.USER,
        ChatRole.ASSISTANT,
    )


def test_journal_memory_is_explicitly_provisional_and_contextual() -> None:
    snapshot = MentorJournalSnapshot.empty(now=NOW).append(_turn())

    memory = snapshot.memory_for("BMB830 | Module 2 | Assessment")

    assert "provisional model-generated mentor observations" in memory
    assert "misconceptions=Interpreta correlación como causalidad" in memory
    assert "next=Comparar confusión, mediación y causalidad" in memory


def test_journal_rejects_naive_timestamps() -> None:
    with pytest.raises(ValueError, match="timezone-aware"):
        MentorTurnRecord(
            session_id="session",
            created_at=datetime(2026, 8, 4, 12, 0),
            context="context",
            mode=MentorMode.REFLECT,
            user_message="What changed?",
            assistant_message="What evidence supports that change?",
            observation=MentorObservation.empty(),
        )
