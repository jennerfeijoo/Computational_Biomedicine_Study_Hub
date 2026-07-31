"""Academic integrity tests for the initial BMB830 module block."""

from __future__ import annotations

from computational_biomedicine_study_hub.content.bmb830 import (
    BUNDLES,
    LOCALIZED_BUNDLES,
    MODULES,
    OBJECTIVE_QUESTION_BANKS,
)
from computational_biomedicine_study_hub.i18n import AppLocale
from computational_biomedicine_study_hub.learning.r_execution import can_execute_r


def test_bmb830_registers_three_complete_modules_in_order() -> None:
    assert tuple(module.module_id for module in MODULES) == (
        "bmb830.m01",
        "bmb830.m02",
        "bmb830.m03",
    )
    assert len(BUNDLES) == len(LOCALIZED_BUNDLES) == 3
    assert set(OBJECTIVE_QUESTION_BANKS) == {
        "bmb830.m01",
        "bmb830.m02",
        "bmb830.m03",
    }

    for bundle in BUNDLES:
        module = bundle.module
        assert module.course_code == "BMB830"
        assert len(module.objectives) >= 4
        assert len(module.concepts) >= 4
        assert len(module.worked_examples) >= 2
        assert len(module.practice_exercises) >= 6
        assert len(module.assessment_items) == 8
        assert len(bundle.objective_question_bank) == 16
        assert bundle.content_version == "1.0.0"
        assert all(can_execute_r(example.code) for example in module.worked_examples)


def test_bmb830_locales_preserve_assessment_identity() -> None:
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


def test_bmb830_activity_ids_are_unique_within_each_module() -> None:
    for bundle in BUNDLES:
        module = bundle.module
        identifiers = (
            *(item.exercise_id for item in module.practice_exercises),
            *(item.item_id for item in module.assessment_items),
            *(item.item_id for item in bundle.objective_question_bank),
        )
        assert len(identifiers) == len(set(identifiers))
        assert all(
            identifier.startswith((f"{module.module_id}.", f"m{module.module_id[-2:]}"))
            for identifier in identifiers
        )
