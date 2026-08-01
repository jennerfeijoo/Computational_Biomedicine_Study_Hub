"""Focused academic tests for BMB830 introductory multivariate analysis."""

from __future__ import annotations

from computational_biomedicine_study_hub.content.bmb830.module_11_intro_multivariate import (
    LOCALIZED_MODULE_11_INTRO_MULTIVARIATE,
    LOCALIZED_OBJECTIVE_QUESTION_BANK_11,
    MODULE_11_INTRO_MULTIVARIATE,
)
from computational_biomedicine_study_hub.i18n import AppLocale
from computational_biomedicine_study_hub.learning.r_execution import can_execute_r


def _academic_text() -> str:
    module = MODULE_11_INTRO_MULTIVARIATE
    return " ".join(
        (
            module.summary,
            *(objective.statement for objective in module.objectives),
            *(concept.body for concept in module.concepts),
            *(point for concept in module.concepts for point in concept.key_points),
        )
    ).casefold()


def test_multivariate_module_has_complete_individual_contract() -> None:
    module = MODULE_11_INTRO_MULTIVARIATE

    assert module.module_id == "bmb830.m11"
    assert module.course_code == "BMB830"
    assert len(module.objectives) == 4
    assert len(module.concepts) == 4
    assert len(module.worked_examples) == 2
    assert len(module.practice_exercises) == 6
    assert len(module.assessment_items) == 8
    assert len(LOCALIZED_OBJECTIVE_QUESTION_BANK_11) == 16
    assert all(can_execute_r(example.code) for example in module.worked_examples)

    activity_text = " ".join(exercise.prompt for exercise in module.practice_exercises).casefold()
    assert "proyecto grupal" not in activity_text
    assert "group project" not in activity_text
    assert "gruppeprojekt" not in activity_text


def test_multivariate_content_covers_matrix_pca_clustering_and_validation() -> None:
    text = _academic_text()

    assert "muestras" in text
    assert "variables" in text
    assert "unidades independientes" in text
    assert "valores ausentes" in text
    assert "varianza cero" in text
    assert "centrar" in text
    assert "escalar" in text
    assert "distancia euclídea" in text
    assert "correlación" in text
    assert "componentes principales" in text
    assert "scores" in text
    assert "loadings" in text
    assert "varianza explicada" in text
    assert "signo" in text
    assert "clustering jerárquico" in text
    assert "linkage" in text
    assert "estabilidad" in text
    assert "lote" in text
    assert "fuga de información" in text


def test_multivariate_examples_use_deterministic_base_r_algorithms() -> None:
    pca, clustering = MODULE_11_INTRO_MULTIVARIATE.worked_examples

    assert "prcomp(" in pca.code
    assert "scale. = TRUE" in pca.code
    assert "abs(fit$rotation" in pca.code
    assert "abs(fit$x" in pca.code
    assert "pc1_variance=100.0" in pca.expected_output

    assert "scale(x)" in clustering.code
    assert "dist(" in clustering.code
    assert "hclust(" in clustering.code
    assert "cutree(" in clustering.code
    assert "same_partition=TRUE" in clustering.expected_output


def test_multivariate_locales_preserve_assessment_identity() -> None:
    materialized = {
        locale: (
            LOCALIZED_MODULE_11_INTRO_MULTIVARIATE.materialize(locale),
            tuple(item.materialize(locale) for item in LOCALIZED_OBJECTIVE_QUESTION_BANK_11),
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
