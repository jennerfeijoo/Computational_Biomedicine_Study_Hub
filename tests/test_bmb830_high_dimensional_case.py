"""Focused academic tests for the individual BMB830 high-dimensional case."""

from __future__ import annotations

from computational_biomedicine_study_hub.content.bmb830.module_12_high_dimensional_case import (
    LOCALIZED_MODULE_12_HIGH_DIMENSIONAL_CASE,
    LOCALIZED_OBJECTIVE_QUESTION_BANK_12,
    MODULE_12_HIGH_DIMENSIONAL_CASE,
)
from computational_biomedicine_study_hub.i18n import AppLocale
from computational_biomedicine_study_hub.learning.r_execution import can_execute_r


def _academic_text() -> str:
    module = MODULE_12_HIGH_DIMENSIONAL_CASE
    return " ".join(
        (
            module.title,
            module.summary,
            *(objective.statement for objective in module.objectives),
            *(concept.title for concept in module.concepts),
            *(concept.body for concept in module.concepts),
            *(point for concept in module.concepts for point in concept.key_points),
            *(exercise.prompt for exercise in module.practice_exercises),
            *(exercise.solution for exercise in module.practice_exercises),
            *(exercise.explanation for exercise in module.practice_exercises),
        )
    ).casefold()


def test_high_dimensional_case_has_complete_individual_contract() -> None:
    module = MODULE_12_HIGH_DIMENSIONAL_CASE

    assert module.module_id == "bmb830.m12"
    assert module.course_code == "BMB830"
    assert len(module.objectives) == 4
    assert len(module.concepts) == 4
    assert len(module.worked_examples) == 2
    assert len(module.practice_exercises) == 6
    assert len(module.assessment_items) == 8
    assert len(LOCALIZED_OBJECTIVE_QUESTION_BANK_12) == 16
    assert all(can_execute_r(example.code) for example in module.worked_examples)

    activity_text = " ".join(
        (
            *(exercise.prompt for exercise in module.practice_exercises),
            *(exercise.solution for exercise in module.practice_exercises),
        )
    ).casefold()
    assert "proyecto grupal" not in activity_text
    assert "group project" not in activity_text
    assert "gruppeprojekt" not in activity_text


def test_high_dimensional_case_covers_provenance_qc_leakage_and_reporting() -> None:
    text = _academic_text()

    assert "procedencia" in text
    assert "diccionario de datos" in text
    assert "sintétic" in text
    assert "p mayor que n" in text
    assert "ausencia por muestra" in text
    assert "varianza cero" in text
    assert "filtrado" in text
    assert "imputación" in text
    assert "log2" in text
    assert "escalado" in text
    assert "pca" in text
    assert "lote" in text
    assert "cribado" in text
    assert "fuga" in text
    assert "multiplicidad" in text
    assert "validación" in text
    assert "evidencia clínica" in text
    assert "ollama" in text


def test_high_dimensional_examples_use_deterministic_base_r_workflows() -> None:
    audit, screening = MODULE_12_HIGH_DIMENSIONAL_CASE.worked_examples

    assert "outer(" in audit.code
    assert "colMeans(is.na(x))" in audit.code
    assert "apply(x, 2, sd" in audit.code
    assert "median(" in audit.code
    assert "log2(" in audit.code
    assert "prcomp(" in audit.code
    assert "features_retained=235" in audit.expected_output
    assert "p_gt_n=TRUE" in audit.expected_output
    assert "missing_after=0" in audit.expected_output

    assert "abs(cor(pc1" in screening.code
    assert "validation <- seq(1, n, by = 5)" in screening.code
    assert "training <- setdiff" in screening.code
    assert "standardised_difference" in screening.code
    assert "pc1_metadata=batch" in screening.expected_output
    assert "top10_true_signal=10" in screening.expected_output
    assert "ranking_uses_validation=FALSE" in screening.expected_output


def test_high_dimensional_locales_preserve_assessment_identity() -> None:
    materialized = {
        locale: (
            LOCALIZED_MODULE_12_HIGH_DIMENSIONAL_CASE.materialize(locale),
            tuple(item.materialize(locale) for item in LOCALIZED_OBJECTIVE_QUESTION_BANK_12),
        )
        for locale in AppLocale
    }
    reference_module, reference_bank = materialized[AppLocale.SPANISH_SPAIN]
    reference_ids = tuple(item.item_id for item in reference_bank)
    reference_answers = tuple(item.correct_option_ids for item in reference_bank)

    for locale, (module, bank) in materialized.items():
        assert module.module_id == reference_module.module_id
        assert module.title.strip()
        assert tuple(item.item_id for item in bank) == reference_ids
        assert tuple(item.correct_option_ids for item in bank) == reference_answers, locale
