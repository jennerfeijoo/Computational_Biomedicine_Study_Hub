"""Academic integrity tests for the completed BMB830 module blocks."""

from __future__ import annotations

from computational_biomedicine_study_hub.content.bmb830 import (
    BUNDLES,
    LOCALIZED_BUNDLES,
    MODULES,
    OBJECTIVE_QUESTION_BANKS,
)
from computational_biomedicine_study_hub.i18n import AppLocale
from computational_biomedicine_study_hub.learning.r_execution import can_execute_r


def test_bmb830_registers_twelve_complete_modules_in_order() -> None:
    expected_ids = tuple(f"bmb830.m{index:02d}" for index in range(1, 13))
    expected_versions = {
        "bmb830.m01": "1.0.0",
        "bmb830.m02": "1.0.0",
        **{f"bmb830.m{index:02d}": "1.1.0" for index in range(3, 11)},
        **{f"bmb830.m{index:02d}": "1.0.0" for index in range(11, 13)},
    }
    expected_assessment_counts = {
        **{f"bmb830.m{index:02d}": 9 for index in range(3, 11)},
    }

    assert tuple(module.module_id for module in MODULES) == expected_ids
    assert len(BUNDLES) == len(LOCALIZED_BUNDLES) == 12
    assert set(OBJECTIVE_QUESTION_BANKS) == set(expected_ids)
    assert sum(len(bundle.objective_question_bank) for bundle in BUNDLES) == 192

    for bundle in BUNDLES:
        module = bundle.module
        assert module.course_code == "BMB830"
        assert len(module.objectives) >= 4
        assert len(module.concepts) >= 4
        assert len(module.worked_examples) >= 2
        assert len(module.practice_exercises) >= 6
        assert len(module.assessment_items) == expected_assessment_counts.get(module.module_id, 8)
        assert len(bundle.objective_question_bank) == 16
        assert bundle.content_version == expected_versions[module.module_id]
        assert all(can_execute_r(example.code) for example in module.worked_examples)


def test_bmb830_inference_block_covers_required_concepts() -> None:
    estimation, testing, comparison = MODULES[3:6]

    estimation_text = " ".join(
        (estimation.summary, *(concept.body for concept in estimation.concepts))
    ).casefold()
    testing_text = " ".join(
        (testing.summary, *(concept.body for concept in testing.concepts))
    ).casefold()
    comparison_text = " ".join(
        (comparison.summary, *(concept.body for concept in comparison.concepts))
    ).casefold()

    assert "error estándar" in estimation_text
    assert "intervalos de confianza" in estimation_text
    assert "error tipo i" in testing_text
    assert "potencia" in testing_text
    assert "aleatorización" in testing_text
    assert "intercambiables" in testing_text
    assert "welch" in comparison_text
    assert "anova" in comparison_text
    assert "paread" in comparison_text
    assert "contraste" in comparison_text


def test_bmb830_regression_block_covers_required_concepts() -> None:
    simple, multiple, interaction, diagnostics = MODULES[6:10]
    simple_text = " ".join(
        (simple.summary, *(concept.body for concept in simple.concepts))
    ).casefold()
    multiple_text = " ".join(
        (multiple.summary, *(concept.body for concept in multiple.concepts))
    ).casefold()
    interaction_text = " ".join(
        (interaction.summary, *(concept.body for concept in interaction.concepts))
    ).casefold()
    diagnostics_text = " ".join(
        (diagnostics.summary, *(concept.body for concept in diagnostics.concepts))
    ).casefold()

    assert "causalidad" in simple_text
    assert "pearson" in simple_text
    assert "spearman" in simple_text
    assert "pendiente" in simple_text
    assert "r²" in simple_text
    assert "intervalo de predicción" in simple_text
    assert "adimensional" in simple_text
    assert "sy/sx" in simple_text

    assert "media esperada" in multiple_text
    assert "matriz de diseño" in multiple_text
    assert "referencia" in multiple_text
    assert "confus" in multiple_text
    assert "colinealidad" in multiple_text
    assert "residualiz" in multiple_text
    assert "coeficiente ajustado" in multiple_text

    assert "modificación de efecto" in interaction_text
    assert "diferencia de pendientes" in interaction_text
    assert "centrar" in interaction_text
    assert "cuadrático" in interaction_text
    assert "extrapol" in interaction_text

    assert "residuo" in diagnostics_text
    assert "heterocedasticidad" in diagnostics_text
    assert "distancia de cook" in diagnostics_text
    assert "fuga de información" in diagnostics_text
    assert "fuera de muestra" in diagnostics_text


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
