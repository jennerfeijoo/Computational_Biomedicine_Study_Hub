"""Regression tests for the cumulative BMB830 source-grounded audit."""

from __future__ import annotations

import itertools
import math

from computational_biomedicine_study_hub.content import bmb830
from computational_biomedicine_study_hub.i18n import AppLocale
from computational_biomedicine_study_hub.learning.r_execution import can_execute_r

_EXPECTED_MODULE_IDS = {f"bmb830.m{index:02d}" for index in range(1, 13)}
_REVIEWED_MODULE_IDS = {f"bmb830.m{index:02d}" for index in range(1, 9)}


def _module(module_id: str, locale: AppLocale | str = AppLocale.ENGLISH):
    localized = next(item for item in bmb830.LOCALIZED_MODULES if item.module_id == module_id)
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


def _sample_mean(values: tuple[float, ...]) -> float:
    return sum(values) / len(values)


def _sample_variance(values: tuple[float, ...]) -> float:
    mean = _sample_mean(values)
    return sum((value - mean) ** 2 for value in values) / (len(values) - 1)


def _sample_covariance(left: tuple[float, ...], right: tuple[float, ...]) -> float:
    left_mean = _sample_mean(left)
    right_mean = _sample_mean(right)
    return sum(
        (left_value - left_mean) * (right_value - right_mean)
        for left_value, right_value in zip(left, right, strict=True)
    ) / (len(left) - 1)


def _simple_residuals(
    response: tuple[float, ...], predictor: tuple[float, ...]
) -> tuple[float, ...]:
    slope = _sample_covariance(predictor, response) / _sample_variance(predictor)
    intercept = _sample_mean(response) - slope * _sample_mean(predictor)
    return tuple(
        observed - (intercept + slope * value)
        for observed, value in zip(response, predictor, strict=True)
    )


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


def test_only_completed_reviews_are_marked_reviewed() -> None:
    state_by_module = {item.module_id: item.state for item in bmb830.BMB830_MODULE_SOURCE_AUDIT}
    reviewed_states = {"consistent", "correct"}

    assert {
        module_id for module_id, state in state_by_module.items() if state in reviewed_states
    } == _REVIEWED_MODULE_IDS
    assert {
        module_id for module_id, state in state_by_module.items() if state == "pending"
    } == _EXPECTED_MODULE_IDS - _REVIEWED_MODULE_IDS
    assert state_by_module["bmb830.m07"] == "correct"
    assert state_by_module["bmb830.m08"] == "correct"


def test_review_identity_is_locale_stable() -> None:
    for module_id in (
        "bmb830.m03",
        "bmb830.m04",
        "bmb830.m05",
        "bmb830.m06",
        "bmb830.m07",
        "bmb830.m08",
    ):
        reference = _identities(module_id, AppLocale.SPANISH_SPAIN)
        for locale in AppLocale:
            assert _identities(module_id, locale) == reference


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


def test_hypothesis_extension_preserves_randomization_design() -> None:
    module = _module("bmb830.m05")
    randomization = next(
        item
        for item in module.concepts
        if item.concept_id == "randomization-tests-and-exchangeability"
    )
    exported = "\n".join((randomization.body, *randomization.key_points)).casefold()

    assert "exchangeable" in exported
    assert "group sizes" in exported
    assert "paired" in exported
    assert "clusters" in exported
    assert "absolute value" in exported
    assert "(extreme+1)/(b+1)" in exported

    example = next(item for item in module.worked_examples if item.example_id == "m05.bg.e01")
    assert can_execute_r(example.code)
    assert example.expected_output == "observed=4.33\nassignments=20\np=0.100"

    values = (2, 3, 4, 6, 7, 9)
    observed = sum(values[3:]) / 3 - sum(values[:3]) / 3
    statistics = []
    for group_a in itertools.combinations(range(len(values)), 3):
        group_a_set = set(group_a)
        mean_a = sum(values[index] for index in group_a) / 3
        mean_b = sum(values[index] for index in range(len(values)) if index not in group_a_set) / 3
        statistics.append(mean_b - mean_a)
    p_value = sum(abs(value) >= abs(observed) for value in statistics) / len(statistics)
    assert (round(observed, 2), len(statistics), round(p_value, 3)) == (4.33, 20, 0.1)


def test_group_comparison_extension_separates_global_test_and_contrasts() -> None:
    module = _module("bmb830.m06")
    anova = next(
        item
        for item in module.concepts
        if item.concept_id == "anova-global-test-and-planned-contrasts"
    )
    exported = "\n".join((anova.body, *anova.key_points)).casefold()

    assert "between-group" in exported
    assert "within groups" in exported
    assert "f-statistic" in exported
    assert "at least one differs" in exported
    assert "planned contrast" in exported
    assert "multiplicity" in exported
    assert "welch's anova" in exported

    example = next(item for item in module.worked_examples if item.example_id == "m06.bg.e01")
    assert can_execute_r(example.code)
    assert "pf(" in example.code
    assert example.expected_output == "F=13.00\np=0.0066\nC_minus_A=4.00"


def test_simple_regression_extension_links_scale_slope_and_r_squared() -> None:
    module = _module("bmb830.m07")
    identity = next(
        item
        for item in module.concepts
        if item.concept_id == "correlation-slope-and-standardisation"
    )
    exported = "\n".join((identity.body, *identity.key_points)).casefold()

    assert "dimensionless" in exported
    assert "symmetric" in exported
    assert "sy divided by sx" in exported
    assert "r-squared equals r squared" in exported
    assert "standardised regression slope equals r" in exported
    assert "multiple regression" in exported

    example = next(item for item in module.worked_examples if item.example_id == "m07.bg.e01")
    assert can_execute_r(example.code)
    assert example.expected_output == (
        "r=0.998\nslope=1.342\nr_sy_sx=1.342\nstandardised_slope=0.998\nr2=0.997\nr_squared=0.997"
    )

    x = (1.0, 2.0, 4.0, 5.0, 7.0)
    y = (2.0, 3.0, 6.0, 7.0, 10.0)
    correlation = _sample_covariance(x, y) / math.sqrt(_sample_variance(x) * _sample_variance(y))
    slope = _sample_covariance(x, y) / _sample_variance(x)
    scale_identity = correlation * math.sqrt(_sample_variance(y) / _sample_variance(x))
    assert (round(correlation, 3), round(slope, 3), round(scale_identity, 3)) == (
        0.998,
        1.342,
        1.342,
    )
    assert round(correlation**2, 3) == 0.997

    corrected = next(item for item in module.worked_examples if item.example_id == "m07.e02")
    assert corrected.expected_output == ("mean=5.55\nmean_ci=[5.31, 5.79]\nprediction=[4.99, 6.12]")


def test_multiple_regression_extension_recovers_partial_slope_and_corrects_outputs() -> None:
    module = _module("bmb830.m08")
    partial = next(
        item
        for item in module.concepts
        if item.concept_id == "partial-regression-and-adjusted-coefficients"
    )
    exported = "\n".join((partial.body, *partial.key_points)).casefold()

    assert "residualise x and y" in exported
    assert "same covariates" in exported
    assert "adjusted coefficient" in exported
    assert "collinearity" in exported
    assert "causal" in exported

    example = next(item for item in module.worked_examples if item.example_id == "m08.bg.e01")
    assert can_execute_r(example.code)
    assert example.expected_output == (
        "adjusted=0.382\npartial=0.382\nmax_abs_exposure_residual=0.457"
    )

    exposure = (1.0, 2.0, 2.0, 3.0, 4.0, 4.0, 5.0, 6.0)
    age = (30.0, 34.0, 39.0, 42.0, 48.0, 53.0, 57.0, 62.0)
    response = (5.2, 6.1, 6.8, 7.4, 8.8, 9.2, 10.1, 11.0)
    exposure_residual = _simple_residuals(exposure, age)
    response_residual = _simple_residuals(response, age)
    partial_slope = _sample_covariance(exposure_residual, response_residual) / _sample_variance(
        exposure_residual
    )
    assert round(partial_slope, 3) == 0.382
    assert round(max(abs(value) for value in exposure_residual), 3) == 0.457

    crude = next(item for item in module.worked_examples if item.example_id == "m08.e01")
    factors = next(item for item in module.worked_examples if item.example_id == "m08.e02")
    assert crude.expected_output == (
        "crude_exposure=1.191\nadjusted_exposure=0.382\nadjusted_age=0.123"
    )
    assert factors.expected_output == ("(Intercept),groupA,groupB,age\ngroupA=0.95\ngroupB=1.89")


def test_reviewed_modules_expose_named_source_basis() -> None:
    foundations = _module("bmb830.m01")
    summary = _module("bmb830.m02")
    probability = _module("bmb830.m03")
    estimation = _module("bmb830.m04")
    testing = _module("bmb830.m05")
    comparison = _module("bmb830.m06")
    simple = _module("bmb830.m07")
    multiple = _module("bmb830.m08")

    assert "sdu-bmb830-active-2025" in foundations.tutor_support.source_basis
    assert "ims-2024-data-eda" in foundations.tutor_support.source_basis
    assert "yachay-probability-statistics" in summary.tutor_support.source_basis
    assert "ims-2024-probability-inference" in probability.tutor_support.source_basis
    assert "yachay-biostatistics-linear-models" in estimation.tutor_support.source_basis
    assert "islr-2021-ch02-05" in estimation.tutor_support.source_basis
    assert "ims-2024-probability-inference" in testing.tutor_support.source_basis
    assert "yachay-biostatistics-linear-models" in testing.tutor_support.source_basis
    assert "ims-2024-probability-inference" in comparison.tutor_support.source_basis
    assert "yachay-biostatistics-linear-models" in comparison.tutor_support.source_basis
    assert "ims-2024-regression-models" in simple.tutor_support.source_basis
    assert "islr-2021-ch02-05" in simple.tutor_support.source_basis
    assert "ims-2024-regression-models" in multiple.tutor_support.source_basis
    assert "yachay-biostatistics-linear-models" in multiple.tutor_support.source_basis
