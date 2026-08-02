"""Regression tests for the cumulative BMB830 source-grounded audit."""

from __future__ import annotations

import itertools
import math

from computational_biomedicine_study_hub.content import bmb830
from computational_biomedicine_study_hub.i18n import AppLocale
from computational_biomedicine_study_hub.learning.r_execution import can_execute_r

_EXPECTED_MODULE_IDS = {f"bmb830.m{index:02d}" for index in range(1, 13)}
_REVIEWED_MODULE_IDS = {"bmb830.m01", "bmb830.m02", "bmb830.m03", "bmb830.m04"}


def _module(module_id: str, locale: AppLocale | str = AppLocale.ENGLISH):
    localized = next(item for item in bmb830.LOCALIZED_MODULES if item.module_id == module_id)
    return localized.materialize(locale)


def test_bmb830_source_audit_maps_every_module_once() -> None:
    audited_ids = tuple(item.module_id for item in bmb830.BMB830_MODULE_SOURCE_AUDIT)

    assert len(audited_ids) == 12
    assert len(set(audited_ids)) == 12
    assert set(audited_ids) == _EXPECTED_MODULE_IDS


def test_bmb830_source_catalog_has_unique_stable_ids() -> None:
    source_ids = tuple(source.source_id for source in bmb830.BMB830_BOOK_SOURCES)

    assert len(source_ids) == len(set(source_ids))
    assert "sdu-bmb830-active-2025" in source_ids
    assert "ims-2024-data-eda" in source_ids
    assert "ims-2024-probability-inference" in source_ids
    assert "ims-2024-regression-models" in source_ids
    assert "islr-2021-ch02-05" in source_ids
    assert "yachay-probability-statistics" in source_ids
    assert "yachay-biostatistics-linear-models" in source_ids


def test_only_completed_foundation_reviews_are_marked_consistent() -> None:
    state_by_module = {item.module_id: item.state for item in bmb830.BMB830_MODULE_SOURCE_AUDIT}

    assert {
        module_id for module_id, state in state_by_module.items() if state == "consistent"
    } == _REVIEWED_MODULE_IDS
    assert {
        module_id for module_id, state in state_by_module.items() if state == "pending"
    } == _EXPECTED_MODULE_IDS - _REVIEWED_MODULE_IDS


def test_foundation_review_identity_is_locale_stable() -> None:
    reference: tuple[tuple[str, ...], ...] | None = None

    for locale in AppLocale:
        probability = _module("bmb830.m03", locale)
        estimation = _module("bmb830.m04", locale)
        identities = (
            tuple(item.objective_id for item in probability.objectives),
            tuple(item.concept_id for item in probability.concepts),
            tuple(item.example_id for item in probability.worked_examples),
            tuple(item.exercise_id for item in probability.practice_exercises),
            tuple(item.item_id for item in probability.assessment_items),
            tuple(item.objective_id for item in estimation.objectives),
            tuple(item.concept_id for item in estimation.concepts),
            tuple(item.example_id for item in estimation.worked_examples),
            tuple(item.exercise_id for item in estimation.practice_exercises),
            tuple(item.item_id for item in estimation.assessment_items),
        )
        if reference is None:
            reference = identities
        else:
            assert identities == reference


def test_probability_extension_covers_bayes_and_base_rates() -> None:
    module = _module("bmb830.m03")
    bayes = next(
        item for item in module.concepts if item.concept_id == "bayes-updating-and-base-rates"
    )
    exported = "\n".join((bayes.body, *bayes.key_points)).casefold()

    assert "sensitivity" in exported
    assert "specificity" in exported
    assert "prevalence" in exported
    assert "p(d|+)" in exported
    assert "false positives" in exported
    assert "denominator" in exported

    example = next(item for item in module.worked_examples if item.example_id == "m03.bg.e01")
    assert can_execute_r(example.code)
    assert example.expected_output == "P(D|+)=0.269"

    prevalence = 0.02
    sensitivity = 0.90
    specificity = 0.95
    posterior = (
        sensitivity * prevalence / (sensitivity * prevalence + (1 - specificity) * (1 - prevalence))
    )
    assert round(posterior, 3) == 0.269


def test_estimation_extension_preserves_bootstrap_design_units() -> None:
    module = _module("bmb830.m04")
    bootstrap = next(
        item
        for item in module.concepts
        if item.concept_id == "bootstrap-resampling-and-design-units"
    )
    exported = "\n".join((bootstrap.body, *bootstrap.key_points)).casefold()

    assert "with replacement" in exported
    assert "sample size" in exported
    assert "independent unit" in exported
    assert "complete patients" in exported
    assert "clusters" in exported
    assert "bias" in exported
    assert "seed" in exported

    example = next(item for item in module.worked_examples if item.example_id == "m04.bg.e01")
    assert can_execute_r(example.code)
    assert example.expected_output == "observed=5.00\nresamples=256\nci=[2.75, 7.75]"

    values = (2.0, 4.0, 5.0, 9.0)
    means = sorted(
        sum(values[index] for index in sample) / len(values)
        for sample in itertools.product(range(len(values)), repeat=len(values))
    )
    lower = means[math.ceil(0.025 * len(means)) - 1]
    upper = means[math.ceil(0.975 * len(means)) - 1]
    assert (len(means), lower, upper) == (256, 2.75, 7.75)


def test_reviewed_modules_expose_named_source_basis() -> None:
    foundations = _module("bmb830.m01")
    summary = _module("bmb830.m02")
    probability = _module("bmb830.m03")
    estimation = _module("bmb830.m04")

    assert "sdu-bmb830-active-2025" in foundations.tutor_support.source_basis
    assert "ims-2024-data-eda" in foundations.tutor_support.source_basis
    assert "yachay-probability-statistics" in summary.tutor_support.source_basis
    assert "ims-2024-probability-inference" in probability.tutor_support.source_basis
    assert "yachay-biostatistics-linear-models" in estimation.tutor_support.source_basis
    assert "islr-2021-ch02-05" in estimation.tutor_support.source_basis
