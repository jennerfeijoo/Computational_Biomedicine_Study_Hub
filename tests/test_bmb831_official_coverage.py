"""Regression tests for the public BMB831 coverage matrix."""

from __future__ import annotations

from computational_biomedicine_study_hub.content.bmb831 import MODULES
from computational_biomedicine_study_hub.content.bmb831.official_coverage import (
    BMB831_PUBLIC_EXAM,
    BMB831_SYNTHEA_BOUNDARY,
    OFFICIAL_BMB831_REQUIREMENTS,
    CoverageStatus,
    RequirementKind,
    coverage_rows,
    coverage_summary,
)


def test_bmb831_coverage_matrix_has_public_row_counts_and_unique_ids() -> None:
    assert len(OFFICIAL_BMB831_REQUIREMENTS) == 15
    assert (
        sum(
            requirement.kind is RequirementKind.LEARNING_OUTCOME
            for requirement in OFFICIAL_BMB831_REQUIREMENTS
        )
        == 7
    )
    assert (
        sum(
            requirement.kind is RequirementKind.CONTENT_TOPIC
            for requirement in OFFICIAL_BMB831_REQUIREMENTS
        )
        == 6
    )
    assert (
        sum(
            requirement.kind is RequirementKind.EXAM_COMPONENT
            for requirement in OFFICIAL_BMB831_REQUIREMENTS
        )
        == 2
    )

    requirement_ids = tuple(
        requirement.requirement_id for requirement in OFFICIAL_BMB831_REQUIREMENTS
    )
    assert len(requirement_ids) == len(set(requirement_ids))


def test_bmb831_coverage_references_existing_modules_and_evidence() -> None:
    module_ids = {module.module_id for module in MODULES}
    for row in coverage_rows():
        assert set(row.requirement.module_ids) <= module_ids
        assert row.evidence.module_count == len(row.requirement.module_ids)
        if row.requirement.module_ids:
            assert row.evidence.objective_count > 0
            assert row.evidence.practice_count > 0
            assert row.evidence.assessment_count > 0
            assert row.evidence.objective_bank_count > 0
            assert row.evidence.executable_example_count > 0


def test_bmb831_omics_core_reduces_but_does_not_close_public_gaps() -> None:
    summary = coverage_summary()
    assert summary.total == 15
    assert summary.covered == 0
    assert summary.partial == 12
    assert summary.gap == 3
    assert not summary.fully_covered

    assert BMB831_PUBLIC_EXAM == "Individual report"
    assert "not treated as real-patient evidence" in BMB831_SYNTHEA_BOUNDARY
    assert "no longer defines the course scope" in BMB831_SYNTHEA_BOUNDARY
    assert "real omics data remain required" in BMB831_SYNTHEA_BOUNDARY

    omics_rows = tuple(
        requirement
        for requirement in OFFICIAL_BMB831_REQUIREMENTS
        if "omics" in requirement.official_text.casefold()
    )
    assert omics_rows
    assert all(requirement.status is CoverageStatus.PARTIAL for requirement in omics_rows)
    assert all(
        requirement.module_ids == ("bmb831.m02", "bmb831.m03")
        for requirement in omics_rows
    )

    remaining_gaps = {
        requirement.requirement_id
        for requirement in OFFICIAL_BMB831_REQUIREMENTS
        if requirement.status is CoverageStatus.GAP
    }
    assert remaining_gaps == {
        "bmb831.sdu.lo03",
        "bmb831.sdu.ct05",
        "bmb831.sdu.exam02",
    }

    report = next(
        requirement
        for requirement in OFFICIAL_BMB831_REQUIREMENTS
        if requirement.requirement_id == "bmb831.sdu.exam02"
    )
    assert report.status is CoverageStatus.GAP
    assert not report.module_ids
