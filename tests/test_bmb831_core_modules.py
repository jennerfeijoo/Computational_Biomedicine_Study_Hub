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


def test_bmb831_registers_first_complete_module() -> None:
    assert tuple(module.module_id for module in MODULES) == ("bmb831.m01",)
    assert len(BUNDLES) == len(LOCALIZED_BUNDLES) == 1
    assert set(OBJECTIVE_QUESTION_BANKS) == {"bmb831.m01"}
    assert sum(len(bundle.objective_question_bank) for bundle in BUNDLES) == 16

    bundle = BUNDLES[0]
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


def test_bmb831_synthea_module_preserves_scientific_boundaries() -> None:
    module = MODULES[0]
    text = " ".join(
        (
            module.summary,
            *(objective.statement for objective in module.objectives),
            *(concept.body for concept in module.concepts),
            *(practice.explanation for practice in module.practice_exercises),
        )
    ).casefold()

    assert "synthea" in text
    assert "sintétic" in text
    assert "paciente" in text
    assert "cardinalidad" in text
    assert "fuga temporal" in text
    assert "ómic" in text
    assert "no sustit" in text


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


def test_bmb831_activity_ids_are_unique() -> None:
    bundle = BUNDLES[0]
    module = bundle.module
    identifiers = (
        *(item.exercise_id for item in module.practice_exercises),
        *(item.item_id for item in module.assessment_items),
        *(item.item_id for item in bundle.objective_question_bank),
    )
    assert len(identifiers) == len(set(identifiers))
    assert all(identifier.startswith(("bmb831.m01.", "m01.")) for identifier in identifiers)
