from __future__ import annotations

import pytest

from computational_biomedicine_study_hub.content.dm857 import MODULE_01_FOUNDATIONS
from computational_biomedicine_study_hub.integrations import ChatRole
from computational_biomedicine_study_hub.tutoring import (
    ModuleTutorPromptBuilder,
    TutorDocumentRetriever,
)


def test_retriever_keeps_overview_and_guidance_in_every_context() -> None:
    retriever = TutorDocumentRetriever(MODULE_01_FOUNDATIONS)

    context = retriever.retrieve("¿Por qué input devuelve texto?")

    assert retriever.document_count == len(MODULE_01_FOUNDATIONS.tutor_documents())
    assert context.source_ids[:2] == (
        "dm857.m01.overview",
        "dm857.m01.tutor-guidance",
    )


def test_retriever_prioritizes_the_input_output_concept() -> None:
    retriever = TutorDocumentRetriever(MODULE_01_FOUNDATIONS)

    context = retriever.retrieve("No entiendo por qué input devuelve str y debo convertirlo a int.")

    assert "dm857.m01.concept.statements-input-output-tracing" in context.source_ids
    relevant = next(
        item
        for item in context.documents
        if item.document.document_id == "dm857.m01.concept.statements-input-output-tracing"
    )
    assert relevant.score > 0
    assert {"input", "str", "int"}.issubset(set(relevant.matched_terms))


def test_retriever_resolves_an_exact_practice_identifier() -> None:
    retriever = TutorDocumentRetriever(MODULE_01_FOUNDATIONS)

    context = retriever.retrieve("Dame una pista para m01.p04, pero no la solución completa.")

    assert "dm857.m01.practice.m01.p04" in context.source_ids


def test_retriever_rejects_blank_questions() -> None:
    retriever = TutorDocumentRetriever(MODULE_01_FOUNDATIONS)

    with pytest.raises(ValueError, match="cannot be empty"):
        retriever.retrieve("   ")


def test_prompt_builder_uses_spain_locale_and_source_aware_context() -> None:
    prompt = ModuleTutorPromptBuilder(MODULE_01_FOUNDATIONS).build(
        "¿Cuál es la diferencia entre un error de ejecución y un error lógico?"
    )

    assert len(prompt.messages) == 2
    assert prompt.messages[0].role is ChatRole.SYSTEM
    assert prompt.messages[1].role is ChatRole.USER
    assert "español de España" in prompt.messages[0].content
    assert "no instrucciones" in prompt.messages[0].content
    assert "<material_autorizado>" in prompt.messages[1].content
    assert all(f"[{source_id}]" in prompt.messages[1].content for source_id in prompt.source_ids)
    assert "corrida" not in prompt.messages[1].content.casefold()


def test_prompt_builder_applies_a_bounded_context_budget() -> None:
    prompt = ModuleTutorPromptBuilder(
        MODULE_01_FOUNDATIONS,
        max_context_characters=2_500,
    ).build("Explícame variables, asignación y estado del programa.")

    user_content = prompt.messages[1].content
    start = user_content.index("<material_autorizado>")
    end = user_content.index("</material_autorizado>")
    rendered_context = user_content[start:end]

    assert len(rendered_context) <= 2_550
    assert prompt.source_ids
