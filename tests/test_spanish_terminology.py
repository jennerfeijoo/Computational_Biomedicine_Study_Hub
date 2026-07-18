from __future__ import annotations

from computational_biomedicine_study_hub.content.dm857 import MODULE_01_FOUNDATIONS


def test_exported_dm857_content_uses_spain_compatible_sequencing_terms() -> None:
    example = MODULE_01_FOUNDATIONS.worked_examples[0]
    searchable_text = "\n".join(
        (
            example.title,
            example.problem,
            *(document.text for document in MODULE_01_FOUNDATIONS.tutor_documents()),
        )
    ).casefold()

    assert "corrida" not in searchable_text
    assert "proceso de secuenciación" in searchable_text
