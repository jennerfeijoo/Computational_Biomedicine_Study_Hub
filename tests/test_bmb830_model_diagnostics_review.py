"""Regression tests for the BMB830 M09-M10 source-grounded review."""

from __future__ import annotations

import math

from computational_biomedicine_study_hub.content import bmb830
from computational_biomedicine_study_hub.i18n import AppLocale
from computational_biomedicine_study_hub.learning.r_execution import can_execute_r


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


def _simple_fit(
    x: tuple[float, ...],
    y: tuple[float, ...],
) -> tuple[float, float, tuple[float, ...]]:
    x_mean = sum(x) / len(x)
    y_mean = sum(y) / len(y)
    sxx = sum((value - x_mean) ** 2 for value in x)
    sxy = sum(
        (x_value - x_mean) * (y_value - y_mean)
        for x_value, y_value in zip(x, y, strict=True)
    )
    slope = sxy / sxx
    intercept = y_mean - slope * x_mean
    residuals = tuple(
        observed - (intercept + slope * predictor)
        for predictor, observed in zip(x, y, strict=True)
    )
    return intercept, slope, residuals


def test_m09_m10_review_states_and_source_registry() -> None:
    state_by_module = {item.module_id: item.state for item in bmb830.BMB830_MODULE_SOURCE_AUDIT}
    reviewed = {
        module_id
        for module_id, state in state_by_module.items()
        if state in {"consistent", "correct"}
    }

    assert reviewed == {f"bmb830.m{index:02d}" for index in range(1, 11)}
    assert state_by_module["bmb830.m09"] == "correct"
    assert state_by_module["bmb830.m10"] == "consistent"
    assert state_by_module["bmb830.m11"] == "pending"
    assert state_by_module["bmb830.m12"] == "pending"
    assert "islr-2021-ch07" in {source.source_id for source in bmb830.BMB830_BOOK_SOURCES}


def test_m09_m10_review_identity_is_locale_stable() -> None:
    for module_id in ("bmb830.m09", "bmb830.m10"):
        reference = _identities(module_id, AppLocale.SPANISH_SPAIN)
        for locale in AppLocale:
            assert _identities(module_id, locale) == reference


def test_piecewise_linear_extension_recovers_local_slopes_and_corrects_quadratic_output() -> None:
    module = _module("bmb830.m09")
    basis = next(
        item
        for item in module.concepts
        if item.concept_id == "piecewise-linear-basis-and-local-slopes"
    )
    exported = "\n".join((basis.body, *basis.key_points)).casefold()

    assert "hinge" in exported
    assert "knot" in exported
    assert "beta1+beta2" in exported
    assert "continuous" in exported
    assert "global polynomial" in exported
    assert "validation" in exported
    assert "extrapolation" in exported

    example = next(item for item in module.worked_examples if item.example_id == "m09.bg.e01")
    assert can_execute_r(example.code)
    assert example.expected_output == (
        "slope_before=0.50\nslope_after=2.00\npredictions=2.00, 6.50"
    )

    x = tuple(float(value) for value in range(7))
    knot = 3.0
    hinge = tuple(max(0.0, value - knot) for value in x)
    response = tuple(1.0 + 0.5 * value + 1.5 * local for value, local in zip(x, hinge, strict=True))
    assert response[2] == 2.0
    assert response[5] == 6.5
    assert response[3] - response[2] == 0.5
    assert response[5] - response[4] == 2.0

    corrected = next(item for item in module.worked_examples if item.example_id == "m09.e02")
    assert corrected.expected_output == (
        "quadratic=0.344\ncomparison_p=0.0000\n2.34, 1.04, 2.49"
    )


def test_press_extension_links_leverage_and_leave_one_out_error() -> None:
    module = _module("bmb830.m10")
    press = next(
        item for item in module.concepts if item.concept_id == "press-residuals-and-loocv"
    )
    exported = "\n".join((press.body, *press.key_points)).casefold()

    assert "e_i/(1-h_ii)" in exported
    assert "press" in exported
    assert "leave-one-out" in exported
    assert "leverage" in exported
    assert "fixed design" in exported
    assert "pipeline" in exported
    assert "external validation" in exported

    example = next(item for item in module.worked_examples if item.example_id == "m10.bg.e01")
    assert can_execute_r(example.code)
    assert example.expected_output == (
        "train_rmse=0.563\nloocv_rmse=1.018\npress=6.219\nlargest_loo_residual=2.000"
    )

    x = (1.0, 2.0, 3.0, 4.0, 5.0, 6.0)
    y = (1.0, 2.0, 3.0, 4.0, 5.0, 8.0)
    _, _, residuals = _simple_fit(x, y)
    x_mean = sum(x) / len(x)
    sxx = sum((value - x_mean) ** 2 for value in x)
    leverage = tuple(1 / len(x) + (value - x_mean) ** 2 / sxx for value in x)
    loo_residuals = tuple(
        residual / (1 - h) for residual, h in zip(residuals, leverage, strict=True)
    )
    press_value = sum(value**2 for value in loo_residuals)
    train_rmse = math.sqrt(sum(value**2 for value in residuals) / len(residuals))
    loocv_rmse = math.sqrt(press_value / len(loo_residuals))

    assert round(train_rmse, 3) == 0.563
    assert round(loocv_rmse, 3) == 1.018
    assert round(press_value, 3) == 6.219
    assert round(max(abs(value) for value in loo_residuals), 3) == 2.0


def test_m09_m10_review_versions_counts_and_source_basis() -> None:
    bundles = {bundle.module.module_id: bundle for bundle in bmb830.LOCALIZED_BUNDLES}
    interaction = _module("bmb830.m09")
    diagnostics = _module("bmb830.m10")

    assert bundles["bmb830.m09"].content_version == "1.1.0"
    assert bundles["bmb830.m10"].content_version == "1.1.0"
    assert len(interaction.assessment_items) == 9
    assert len(diagnostics.assessment_items) == 9
    assert "islr-2021-ch07" in interaction.tutor_support.source_basis
    assert "yachay-biostatistics-linear-models" in diagnostics.tutor_support.source_basis
