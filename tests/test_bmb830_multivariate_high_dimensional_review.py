"""Regression tests for the BMB830 M11-M12 source-grounded review."""

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


def _matrix_rank(matrix: tuple[tuple[float, ...], ...], tolerance: float = 1e-10) -> int:
    work = [list(row) for row in matrix]
    rows = len(work)
    columns = len(work[0])
    rank = 0
    pivot_column = 0

    while rank < rows and pivot_column < columns:
        pivot = max(range(rank, rows), key=lambda row: abs(work[row][pivot_column]))
        if abs(work[pivot][pivot_column]) <= tolerance:
            pivot_column += 1
            continue
        work[rank], work[pivot] = work[pivot], work[rank]
        pivot_value = work[rank][pivot_column]
        work[rank] = [value / pivot_value for value in work[rank]]
        for row in range(rows):
            if row == rank:
                continue
            factor = work[row][pivot_column]
            work[row] = [
                value - factor * pivot_value
                for value, pivot_value in zip(work[row], work[rank], strict=True)
            ]
        rank += 1
        pivot_column += 1
    return rank


def test_m11_m12_review_states_and_source_registry() -> None:
    state_by_module = {item.module_id: item.state for item in bmb830.BMB830_MODULE_SOURCE_AUDIT}
    reviewed = {
        module_id
        for module_id, state in state_by_module.items()
        if state in {"consistent", "correct"}
    }
    source_ids = {source.source_id for source in bmb830.BMB830_BOOK_SOURCES}

    assert reviewed == {f"bmb830.m{index:02d}" for index in range(1, 13)}
    assert state_by_module["bmb830.m11"] == "consistent"
    assert state_by_module["bmb830.m12"] == "consistent"
    assert "murphy-2023-ch20" in source_ids
    assert "islr-2021-ch06" in source_ids
    assert "yachay-biostatistics-multivariate" in source_ids


def test_m11_m12_review_identity_is_locale_stable() -> None:
    for module_id in ("bmb830.m11", "bmb830.m12"):
        reference = _identities(module_id, AppLocale.SPANISH_SPAIN)
        for locale in AppLocale:
            assert _identities(module_id, locale) == reference


def test_covariance_and_correlation_pca_extension_exposes_scale_contract() -> None:
    module = _module("bmb830.m11")
    pca = next(
        item for item in module.concepts if item.concept_id == "covariance-vs-correlation-pca"
    )
    exported = "\n".join((pca.body, *pca.key_points)).casefold()

    assert "covariance matrix" in exported
    assert "correlation matrix" in exported
    assert "original scales" in exported
    assert "variance one" in exported
    assert "zero-variance" in exported
    assert "geometry" in exported
    assert "loadings" in exported

    example = next(item for item in module.worked_examples if item.example_id == "m11.bg.e01")
    assert can_execute_r(example.code)
    assert example.expected_output == (
        "covariance_abs_loadings=0.010,1.000\ncorrelation_abs_loadings=0.707,0.707"
    )

    covariance_small = 1 / math.sqrt(1 + 100**2)
    covariance_large = 100 / math.sqrt(1 + 100**2)
    correlation_loading = 1 / math.sqrt(2)
    assert (round(covariance_small, 3), round(covariance_large, 3)) == (0.01, 1.0)
    assert round(correlation_loading, 3) == 0.707


def test_high_dimensional_extension_enforces_rank_ceiling() -> None:
    module = _module("bmb830.m12")
    rank_concept = next(
        item for item in module.concepts if item.concept_id == "rank-ceiling-and-p-greater-than-n"
    )
    exported = "\n".join((rank_concept.body, *rank_concept.key_points)).casefold()

    assert "min(n-1,p)" in exported
    assert "non-zero" in exported
    assert "singular" in exported
    assert "non-unique" in exported
    assert "perfect training fit" in exported
    assert "regularisation" in exported
    assert "nested validation" in exported

    example = next(item for item in module.worked_examples if item.example_id == "m12.bg.e01")
    assert can_execute_r(example.code)
    assert example.expected_output == ("samples=4\nfeatures=6\nrank_ceiling=3\nnonzero_pcs=3")

    matrix = (
        (1.0, 0.0, 0.0, 1.0, 1.0, 0.0),
        (0.0, 1.0, 0.0, 1.0, 0.0, 1.0),
        (0.0, 0.0, 1.0, 0.0, 1.0, 1.0),
        (1.0, 1.0, 1.0, 2.0, 2.0, 2.0),
    )
    column_means = tuple(sum(row[column] for row in matrix) / len(matrix) for column in range(6))
    centred = tuple(
        tuple(value - column_means[column] for column, value in enumerate(row)) for row in matrix
    )
    assert _matrix_rank(centred) == 3
    assert min(len(matrix) - 1, len(matrix[0])) == 3


def test_m11_m12_versions_counts_and_source_basis() -> None:
    bundles = {bundle.localized_module.module_id: bundle for bundle in bmb830.LOCALIZED_BUNDLES}
    multivariate = _module("bmb830.m11")
    high_dimensional = _module("bmb830.m12")

    assert bundles["bmb830.m11"].content_version == "1.1.0"
    assert bundles["bmb830.m12"].content_version == "1.1.0"
    assert len(multivariate.assessment_items) == 9
    assert len(high_dimensional.assessment_items) == 9
    assert "murphy-2023-ch20" in multivariate.tutor_support.source_basis
    assert "yachay-biostatistics-multivariate" in multivariate.tutor_support.source_basis
    assert "islr-2021-ch06" in high_dimensional.tutor_support.source_basis
    assert "murphy-2023-ch20" in high_dimensional.tutor_support.source_basis
