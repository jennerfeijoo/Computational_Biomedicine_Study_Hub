"""Academic integrity tests for the BMB831 authored modules."""

from __future__ import annotations

from computational_biomedicine_study_hub.content.bmb831 import (
    BUNDLES,
    LOCALIZED_BUNDLES,
    MODULES,
    OBJECTIVE_QUESTION_BANKS,
)
from computational_biomedicine_study_hub.i18n import AppLocale
from computational_biomedicine_study_hub.learning.r_execution import can_execute_r


def test_bmb831_registers_three_complete_modules() -> None:
    expected_ids = ("bmb831.m01", "bmb831.m02", "bmb831.m03")
    assert tuple(module.module_id for module in MODULES) == expected_ids
    assert len(BUNDLES) == len(LOCALIZED_BUNDLES) == 3
    assert set(OBJECTIVE_QUESTION_BANKS) == set(expected_ids)
    assert sum(len(bundle.objective_question_bank) for bundle in BUNDLES) == 48

    for bundle in BUNDLES:
        module = bundle.module
        assert module.course_code == "BMB831"
        assert len(module.objectives) >= 4
        assert len(module.concepts) >= 4
        assert len(module.worked_examples) >= 2
        assert len(module.practice_exercises) >= 6
        assert len(module.assessment_items) == 8
        assert len(bundle.objective_question_bank) == 16
        assert bundle.content_version == "1.0.0"
        assert all(can_execute_r(example.code) for example in module.worked_examples)


def _module_text(index: int) -> str:
    module = MODULES[index]
    return " ".join(
        (
            module.summary,
            *(objective.statement for objective in module.objectives),
            *(concept.body for concept in module.concepts),
            *(practice.explanation for practice in module.practice_exercises),
        )
    ).casefold()


def test_bmb831_synthea_module_preserves_scientific_boundaries() -> None:
    text = _module_text(0)
    assert "synthea" in text
    assert "sintétic" in text
    assert "paciente" in text
    assert "cardinalidad" in text
    assert "fuga temporal" in text
    assert "ómic" in text
    assert "no sustit" in text


def test_bmb831_omics_modules_cover_matrix_and_inference_contracts() -> None:
    matrix_text = _module_text(1)
    differential_text = _module_text(2)

    assert "matriz" in matrix_text
    assert "metadata" in matrix_text
    assert "normalización" in matrix_text
    assert "muestra" in matrix_text
    assert "lote" in matrix_text

    assert "contraste" in differential_text
    assert "diseño" in differential_text
    assert "dispersión" in differential_text
    assert "tamaño del efecto" in differential_text
    assert "multiplicidad" in differential_text
    assert "benjamini-hochberg" in differential_text


def test_bmb831_locales_preserve_assessment_identity() -> None:
    for localized_bundle in LOCALIZED_BUNDLES:
        materialized = {locale: localized_bundle.materialize(locale) for locale in AppLocale}
        reference = materialized[AppLocale.SPANISH_SPAIN]
        reference_ids = tuple(item.item_id for item in reference.objective_question_bank)
        reference_option_ids = tuple(item.option_ids for item in reference.objective_question_bank)
        reference_correct_ids = tuple(
            item.correct_option_ids for item in reference.objective_question_bank
        )

        for locale, bundle in materialized.items():
            assert bundle.module.module_id == reference.module.module_id
            assert bundle.module.title.strip()
            assert tuple(item.item_id for item in bundle.objective_question_bank) == reference_ids
            assert (
                tuple(item.option_ids for item in bundle.objective_question_bank)
                == reference_option_ids
            )
            assert (
                tuple(item.correct_option_ids for item in bundle.objective_question_bank)
                == reference_correct_ids
            ), locale


def test_bmb831_activity_ids_are_unique_within_and_across_modules() -> None:
    all_identifiers: list[str] = []
    for bundle in BUNDLES:
        module = bundle.module
        local_identifiers = (
            *(item.exercise_id for item in module.practice_exercises),
            *(item.item_id for item in module.assessment_items),
            *(item.item_id for item in bundle.objective_question_bank),
        )
        local_number = module.module_id.rsplit("m", maxsplit=1)[-1]
        assert all(
            identifier.startswith((f"bmb831.m{local_number}.", f"m{local_number}."))
            for identifier in local_identifiers
        )
        assert len(local_identifiers) == len(set(local_identifiers))
        all_identifiers.extend(local_identifiers)

    assert len(all_identifiers) == len(set(all_identifiers))
