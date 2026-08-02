"""Regression tests for the cumulative BMB831 source-grounded review."""

from __future__ import annotations

import math
from statistics import median, stdev

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


def _matrix_rank(rows: tuple[tuple[float, ...], ...], tolerance: float = 1e-10) -> int:
    matrix = [list(row) for row in rows]
    row_count = len(matrix)
    column_count = len(matrix[0])
    pivot_row = 0
    pivot_column = 0

    while pivot_row < row_count and pivot_column < column_count:
        candidate = max(
            range(pivot_row, row_count),
            key=lambda row: abs(matrix[row][pivot_column]),
        )
        if abs(matrix[candidate][pivot_column]) <= tolerance:
            pivot_column += 1
            continue

        matrix[pivot_row], matrix[candidate] = matrix[candidate], matrix[pivot_row]
        pivot = matrix[pivot_row][pivot_column]
        matrix[pivot_row] = [value / pivot for value in matrix[pivot_row]]

        for row in range(row_count):
            if row == pivot_row:
                continue
            factor = matrix[row][pivot_column]
            matrix[row] = [
                value - factor * reference
                for value, reference in zip(matrix[row], matrix[pivot_row], strict=True)
            ]

        pivot_row += 1
        pivot_column += 1

    return pivot_row


def test_bmb831_source_registry_maps_and_reviews_all_modules() -> None:
    source_ids = {source.source_id for source in bmb831.BMB831_BOOK_SOURCES}
    audits = {item.module_id: item for item in bmb831.BMB831_MODULE_SOURCE_AUDIT}
    reviewed = {
        module_id for module_id, audit in audits.items() if audit.state in {"consistent", "correct"}
    }

    expected_ids = {f"bmb831.m{index:02d}" for index in range(1, 10)}
    assert set(audits) == expected_ids
    assert reviewed == expected_ids
    assert {audits[module_id].state for module_id in reviewed} == {"consistent"}
    assert not {module_id for module_id, audit in audits.items() if audit.state == "pending"}
    assert all(set(audit.source_ids) <= source_ids for audit in audits.values())
    assert "sdu-bmb831-active-2025" in source_ids
    assert "bioconductor-summarizedexperiment" in source_ids
    assert "bioconductor-edger-normalization" in source_ids
    assert "bioconductor-deseq2" in source_ids
    assert "limma-empirical-bayes" in source_ids
    assert "islr-2021-unsupervised-multiple-testing" in source_ids
    assert "ims-2024-visualisation-reporting" in source_ids
    assert "bioconductor-public-omics-workflows" in source_ids
    assert "protein-public-resources" in source_ids
    assert "functional-interpretation-resources" in source_ids


def test_reviewed_module_identity_is_locale_stable() -> None:
    for module_id in (f"bmb831.m{index:02d}" for index in range(1, 10)):
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


def test_m04_finite_sample_rank_extension_has_deterministic_contract() -> None:
    module = _module("bmb831.m04")
    rank_concept = next(
        item
        for item in module.concepts
        if item.concept_id == "finite-sample-rank-and-subspace-stability"
    )
    exported = "\n".join(
        (rank_concept.title, rank_concept.body, *rank_concept.key_points)
    ).casefold()

    assert "min(p, n - 1)" in exported
    assert "independent samples" in exported
    assert "subspace" in exported
    assert "eigenvalues" in exported
    assert "resampling" in exported

    worked = next(item for item in module.worked_examples if item.example_id == "m04.bg.e01")
    assert can_execute_r(worked.code)
    assert worked.expected_output == (
        "samples=4\nfeatures=6\nrank_ceiling=3\nobserved_rank=3\nnonzero_pcs=3"
    )

    matrix = (
        (1.0, 2.0, 3.0, 4.0, 5.0, 6.0),
        (2.0, 1.0, 4.0, 3.0, 6.0, 5.0),
        (3.0, 5.0, 1.0, 6.0, 2.0, 4.0),
        (5.0, 3.0, 6.0, 1.0, 4.0, 2.0),
    )
    column_means = tuple(sum(row[column] for row in matrix) / len(matrix) for column in range(6))
    centered = tuple(
        tuple(value - column_means[column] for column, value in enumerate(row)) for row in matrix
    )

    assert min(len(matrix) - 1, len(matrix[0])) == 3
    assert _matrix_rank(centered) == 3
    assert "islr-2021-unsupervised-multiple-testing" in module.tutor_support.source_basis


def test_m05_uncertainty_extension_distinguishes_error_bar_targets() -> None:
    module = _module("bmb831.m05")
    uncertainty = next(
        item for item in module.concepts if item.concept_id == "spread-versus-estimator-uncertainty"
    )
    exported = "\n".join((uncertainty.title, uncertainty.body, *uncertainty.key_points)).casefold()

    assert "standard deviation" in exported
    assert "standard error" in exported
    assert "confidence interval" in exported
    assert "prediction interval" in exported
    assert "analytical unit" in exported

    worked = next(item for item in module.worked_examples if item.example_id == "m05.bg.e01")
    assert can_execute_r(worked.code)
    assert worked.expected_output == (
        "group_A=mean:10.000,sd:1.633,se:0.816,ci_half:2.598\n"
        "group_B=mean:10.000,sd:4.899,se:2.449,ci_half:7.795"
    )

    groups = {
        "A": (8.0, 10.0, 10.0, 12.0),
        "B": (4.0, 10.0, 10.0, 16.0),
    }
    t_critical_df3 = 3.182446305284263
    summaries = {}
    for label, values in groups.items():
        sample_sd = stdev(values)
        standard_error = sample_sd / math.sqrt(len(values))
        summaries[label] = (
            sum(values) / len(values),
            sample_sd,
            standard_error,
            t_critical_df3 * standard_error,
        )

    assert tuple(round(value, 3) for value in summaries["A"]) == (
        10.0,
        1.633,
        0.816,
        2.598,
    )
    assert tuple(round(value, 3) for value in summaries["B"]) == (
        10.0,
        4.899,
        2.449,
        7.795,
    )
    assert "ims-2024-visualisation-reporting" in module.tutor_support.source_basis


def test_m06_protein_inference_extension_preserves_identifiable_level() -> None:
    module = _module("bmb831.m06")
    inference = next(
        item
        for item in module.concepts
        if item.concept_id == "shared-peptides-and-protein-inference"
    )
    exported = "\n".join((inference.title, inference.body, *inference.key_points)).casefold()

    assert "shared peptide" in exported
    assert "proteotypic" in exported
    assert "protein group" in exported
    assert "grouping rules" in exported
    assert "individual protein" in exported

    worked = next(item for item in module.worked_examples if item.example_id == "m06.bg.e01")
    assert can_execute_r(worked.code)
    assert worked.expected_output == (
        "peptides=4\n"
        "unique_peptides=2\n"
        "shared_peptides=2\n"
        "proteins_with_unique=2\n"
        "proteins_shared_only=2"
    )

    mapping = (
        ("pep1", "P1"),
        ("pep2", "P1"),
        ("pep2", "P2"),
        ("pep3", "P2"),
        ("pep4", "P3"),
        ("pep4", "P4"),
    )
    multiplicity: dict[str, int] = {}
    for peptide, _protein in mapping:
        multiplicity[peptide] = multiplicity.get(peptide, 0) + 1
    unique_peptides = {peptide for peptide, count in multiplicity.items() if count == 1}
    shared_peptides = {peptide for peptide, count in multiplicity.items() if count > 1}
    proteins_with_unique = {protein for peptide, protein in mapping if peptide in unique_peptides}
    all_proteins = {protein for _peptide, protein in mapping}

    assert len(multiplicity) == 4
    assert len(unique_peptides) == 2
    assert len(shared_peptides) == 2
    assert len(proteins_with_unique) == 2
    assert len(all_proteins - proteins_with_unique) == 2
    assert "bioconductor-public-omics-workflows" in module.tutor_support.source_basis


def test_m07_alphafold_extension_separates_local_and_relative_confidence() -> None:
    module = _module("bmb831.m07")
    confidence = next(
        item
        for item in module.concepts
        if item.concept_id == "local-confidence-versus-domain-placement"
    )
    exported = "\n".join((confidence.title, confidence.body, *confidence.key_points)).casefold()

    assert "plddt" in exported
    assert "per-residue" in exported
    assert "pae" in exported
    assert "relative positions" in exported
    assert "domain packing" in exported
    assert "mechanism" in exported

    worked = next(item for item in module.worked_examples if item.example_id == "m07.bg.e01")
    assert can_execute_r(worked.code)
    assert worked.expected_output == (
        "domain_A_plddt=90.0\n"
        "domain_B_plddt=89.0\n"
        "within_A_pae=2.0\n"
        "within_B_pae=2.0\n"
        "between_pae=18.0"
    )

    plddt = (92.0, 90.0, 88.0, 91.0, 89.0, 87.0)
    pae = (
        (0.0, 2.0, 2.0, 18.0, 18.0, 18.0),
        (2.0, 0.0, 2.0, 18.0, 18.0, 18.0),
        (2.0, 2.0, 0.0, 18.0, 18.0, 18.0),
        (18.0, 18.0, 18.0, 0.0, 2.0, 2.0),
        (18.0, 18.0, 18.0, 2.0, 0.0, 2.0),
        (18.0, 18.0, 18.0, 2.0, 2.0, 0.0),
    )
    domain_a = (0, 1, 2)
    domain_b = (3, 4, 5)
    within_a = tuple(pae[row][column] for row in domain_a for column in domain_a if row < column)
    within_b = tuple(pae[row][column] for row in domain_b for column in domain_b if row < column)
    between = tuple(pae[row][column] for row in domain_a for column in domain_b)

    assert round(sum(plddt[index] for index in domain_a) / len(domain_a), 1) == 90.0
    assert round(sum(plddt[index] for index in domain_b) / len(domain_b), 1) == 89.0
    assert round(sum(within_a) / len(within_a), 1) == 2.0
    assert round(sum(within_b) / len(within_b), 1) == 2.0
    assert round(sum(between) / len(between), 1) == 18.0
    assert "protein-public-resources" in module.tutor_support.source_basis


def test_m08_ontology_extension_exposes_propagated_dependence() -> None:
    module = _module("bmb831.m08")
    propagation = next(
        item
        for item in module.concepts
        if item.concept_id == "ontology-propagation-and-term-dependence"
    )
    exported = "\n".join((propagation.title, propagation.body, *propagation.key_points)).casefold()

    assert "ancestor" in exported
    assert "parent" in exported
    assert "child" in exported
    assert "not independent" in exported
    assert "semantic redundancy" in exported
    assert "evidence codes" in exported

    worked = next(item for item in module.worked_examples if item.example_id == "m08.bg.e01")
    assert can_execute_r(worked.code)
    assert worked.expected_output == (
        "direct_annotations=3\npropagated_annotations=6\nparent_genes=3\nchild_terms=2"
    )

    direct = (("G1", "child_A"), ("G2", "child_A"), ("G3", "child_B"))
    parent_map = {"child_A": "parent", "child_B": "parent"}
    propagated = (*direct, *((gene, parent_map[term]) for gene, term in direct))
    parent_genes = {gene for gene, term in propagated if term == "parent"}

    assert len(direct) == 3
    assert len(propagated) == 6
    assert len(parent_genes) == 3
    assert len({term for _gene, term in direct}) == 2
    assert "functional-interpretation-resources" in module.tutor_support.source_basis


def test_m09_specification_extension_detects_directional_instability() -> None:
    module = _module("bmb831.m09")
    sensitivity = next(
        item
        for item in module.concepts
        if item.concept_id == "specification-sensitivity-and-selective-reporting"
    )
    exported = "\n".join((sensitivity.title, sensitivity.body, *sensitivity.key_points)).casefold()

    assert "favourable specification" in exported
    assert "sensitivity analyses" in exported
    assert "selective reporting" in exported
    assert "sign" in exported
    assert "unreported" in exported

    worked = next(item for item in module.worked_examples if item.example_id == "m09.bg.e01")
    assert can_execute_r(worked.code)
    assert worked.expected_output == (
        "specifications=4\npositive=3\nnegative=1\nrange=-0.20,0.80\nsign_stable=FALSE"
    )

    estimates = (0.8, 0.6, 0.1, -0.2)
    positive = sum(value > 0 for value in estimates)
    negative = sum(value < 0 for value in estimates)
    sign_stable = positive == len(estimates) or negative == len(estimates)

    assert len(estimates) == 4
    assert positive == 3
    assert negative == 1
    assert (min(estimates), max(estimates)) == (-0.2, 0.8)
    assert sign_stable is False
    assert "ims-2024-visualisation-reporting" in module.tutor_support.source_basis


def test_m01_m09_versions_counts_and_source_basis() -> None:
    bundles = {bundle.localized_module.module_id: bundle for bundle in bmb831.LOCALIZED_BUNDLES}
    expected_versions = {"bmb831.m01": "1.0.0"} | {
        f"bmb831.m{index:02d}": "1.1.0" for index in range(2, 10)
    }

    for module_id, version in expected_versions.items():
        assert bundles[module_id].content_version == version

    assert len(_module("bmb831.m01").assessment_items) == 8
    for module_id in (f"bmb831.m{index:02d}" for index in range(2, 10)):
        assert len(_module(module_id).assessment_items) == 9
    assert "bioconductor-summarizedexperiment" in _module("bmb831.m02").tutor_support.source_basis
    assert "bioconductor-deseq2" in _module("bmb831.m03").tutor_support.source_basis
    assert "limma-empirical-bayes" in _module("bmb831.m03").tutor_support.source_basis
    assert (
        "islr-2021-unsupervised-multiple-testing"
        in _module("bmb831.m04").tutor_support.source_basis
    )
    assert "ims-2024-visualisation-reporting" in _module("bmb831.m05").tutor_support.source_basis
    assert "bioconductor-public-omics-workflows" in _module("bmb831.m06").tutor_support.source_basis
    assert "protein-public-resources" in _module("bmb831.m07").tutor_support.source_basis
    assert "functional-interpretation-resources" in _module("bmb831.m08").tutor_support.source_basis
    assert "ims-2024-visualisation-reporting" in _module("bmb831.m09").tutor_support.source_basis
