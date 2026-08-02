"""Regression tests for the BMB831 M01-M03 source-grounded review."""

from __future__ import annotations

import math
from statistics import median

from computational_biomedicine_study_hub.content import bmb831
from computational_biomedicine_study_hub.i18n import AppLocale
from computational_biomedicine_study_hub.learning.r_execution import can_execute_r


def _module(module_id: str, locale: AppLocale | str = AppLocale.ENGLISH):
    localized = next(item for item in bmb831.LOCALIZED_MODULES if item.module_id == module_id)
    return localized.materialize(locale)


def _identities(module_id: str, locale: AppLocale) -> tuple[tuple[str, ...], ...]:
    module = _module(module_id, locale)
    return (
        tuple(item.objective_id for item in module.objectives),
        tuple(item.concept_id for item in module.concepts),
        tuple(item.example_id for item in module.worked_examples),
        tuple(item.exercise_id for item in module.practice_exercises),
        tuple(item.item_id for item in module.assessment_items),
    )


def test_bmb831_source_registry_maps_all_modules_and_reviews_first_three() -> None:
    source_ids = {source.source_id for source in bmb831.BMB831_BOOK_SOURCES}
    audits = {item.module_id: item for item in bmb831.BMB831_MODULE_SOURCE_AUDIT}
    reviewed = {
        module_id for module_id, audit in audits.items() if audit.state in {"consistent", "correct"}
    }

    assert set(audits) == {f"bmb831.m{index:02d}" for index in range(1, 10)}
    assert reviewed == {"bmb831.m01", "bmb831.m02", "bmb831.m03"}
    assert {audits[module_id].state for module_id in reviewed} == {"consistent"}
    assert {module_id for module_id, audit in audits.items() if audit.state == "pending"} == {
        f"bmb831.m{index:02d}" for index in range(4, 10)
    }
    assert all(set(audit.source_ids) <= source_ids for audit in audits.values())
    assert "sdu-bmb831-active-2025" in source_ids
    assert "bioconductor-summarizedexperiment" in source_ids
    assert "bioconductor-edger-normalization" in source_ids
    assert "bioconductor-deseq2" in source_ids
    assert "limma-empirical-bayes" in source_ids


def test_reviewed_module_identity_is_locale_stable() -> None:
    for module_id in ("bmb831.m01", "bmb831.m02", "bmb831.m03"):
        reference = _identities(module_id, AppLocale.SPANISH_SPAIN)
        for locale in AppLocale:
            assert _identities(module_id, locale) == reference


def test_m01_remains_a_bounded_synthetic_workflow_example() -> None:
    module = _module("bmb831.m01")
    exported = "\n".join(
        (
            module.summary,
            *(concept.body for concept in module.concepts),
            *module.tutor_support.source_basis,
        )
    ).casefold()

    assert "synthetic" in exported
    assert "not real clinical" in exported
    assert "do not replace omics" in exported
    assert "synthea-official-csv-export" in module.tutor_support.source_basis
    assert "sdu-bmb831-active-2025" in module.tutor_support.source_basis


def test_m02_composition_bias_extension_has_deterministic_contract() -> None:
    module = _module("bmb831.m02")
    composition = next(
        item for item in module.concepts if item.concept_id == "composition-bias-and-size-factors"
    )
    exported = "\n".join((composition.title, composition.body, *composition.key_points)).casefold()

    assert "composition bias" in exported
    assert "library size" in exported
    assert "normalisation factor" in exported
    assert "dominant feature" in exported
    assert "spike-ins" in exported
    assert "global shifts" in exported

    worked = next(item for item in module.worked_examples if item.example_id == "m02.bg.e01")
    assert can_execute_r(worked.code)
    assert worked.expected_output == (
        "library_factors=0.456,0.548,1.826,2.191\n"
        "median_factors=0.913,1.095,0.913,1.095\n"
        "G1_total=219.089,219.089,54.772,54.772\n"
        "G1_median=109.545,109.545,109.545,109.545"
    )

    counts = (
        (100.0, 120.0, 100.0, 120.0),
        (100.0, 120.0, 100.0, 120.0),
        (100.0, 120.0, 1000.0, 1200.0),
    )
    library_sizes = tuple(sum(row[column] for row in counts) for column in range(4))
    library_reference = math.prod(library_sizes) ** (1 / len(library_sizes))
    library_factors = tuple(value / library_reference for value in library_sizes)
    geometric_means = tuple(math.prod(row) ** (1 / len(row)) for row in counts)
    ratios = tuple(
        tuple(counts[row][column] / geometric_means[row] for row in range(3)) for column in range(4)
    )
    raw_median_factors = tuple(median(column) for column in ratios)
    factor_reference = math.prod(raw_median_factors) ** (1 / len(raw_median_factors))
    median_factors = tuple(value / factor_reference for value in raw_median_factors)
    total_normalized = tuple(
        counts[0][index] / value for index, value in enumerate(library_factors)
    )
    median_normalized = tuple(
        counts[0][index] / value for index, value in enumerate(median_factors)
    )

    assert tuple(round(value, 3) for value in library_factors) == (0.456, 0.548, 1.826, 2.191)
    assert tuple(round(value, 3) for value in median_factors) == (0.913, 1.095, 0.913, 1.095)
    assert tuple(round(value, 3) for value in total_normalized) == (
        219.089,
        219.089,
        54.772,
        54.772,
    )
    assert tuple(round(value, 3) for value in median_normalized) == (
        109.545,
        109.545,
        109.545,
        109.545,
    )


def test_m03_information_sharing_extension_separates_three_procedures() -> None:
    module = _module("bmb831.m03")
    moderation = next(
        item for item in module.concepts if item.concept_id == "information-sharing-across-features"
    )
    exported = "\n".join((moderation.body, *moderation.key_points)).casefold()

    assert "empirical-bayes" in exported
    assert "variance or dispersion" in exported
    assert "log-fold-change shrinkage" in exported
    assert "multiplicity adjustment" in exported
    assert "confounding" in exported
    assert "pseudoreplication" in exported

    worked = next(item for item in module.worked_examples if item.example_id == "m03.bg.e01")
    assert can_execute_r(worked.code)
    assert worked.expected_output == (
        "raw_variance=0.25,1.00,4.00\n"
        "moderated_variance=0.70,1.00,2.20\n"
        "raw_t=2.83,1.41,0.71\n"
        "moderated_t=1.69,1.41,0.95"
    )

    effects = (1.0, 1.0, 1.0)
    raw_variance = (0.25, 1.0, 4.0)
    residual_df = 4.0
    prior_variance = 1.0
    prior_df = 6.0
    contrast_variance = 0.5
    moderated_variance = tuple(
        (prior_df * prior_variance + residual_df * value) / (prior_df + residual_df)
        for value in raw_variance
    )
    raw_t = tuple(
        effect / math.sqrt(variance * contrast_variance)
        for effect, variance in zip(effects, raw_variance, strict=True)
    )
    moderated_t = tuple(
        effect / math.sqrt(variance * contrast_variance)
        for effect, variance in zip(effects, moderated_variance, strict=True)
    )

    assert tuple(round(value, 2) for value in moderated_variance) == (0.7, 1.0, 2.2)
    assert tuple(round(value, 2) for value in raw_t) == (2.83, 1.41, 0.71)
    assert tuple(round(value, 2) for value in moderated_t) == (1.69, 1.41, 0.95)


def test_m01_m03_versions_counts_and_source_basis() -> None:
    bundles = {bundle.localized_module.module_id: bundle for bundle in bmb831.LOCALIZED_BUNDLES}
    expected_versions = {
        "bmb831.m01": "1.0.0",
        "bmb831.m02": "1.1.0",
        "bmb831.m03": "1.1.0",
    }

    for module_id, version in expected_versions.items():
        assert bundles[module_id].content_version == version

    assert len(_module("bmb831.m01").assessment_items) == 8
    assert len(_module("bmb831.m02").assessment_items) == 9
    assert len(_module("bmb831.m03").assessment_items) == 9
    assert "bioconductor-summarizedexperiment" in _module("bmb831.m02").tutor_support.source_basis
    assert "bioconductor-deseq2" in _module("bmb831.m03").tutor_support.source_basis
    assert "limma-empirical-bayes" in _module("bmb831.m03").tutor_support.source_basis
