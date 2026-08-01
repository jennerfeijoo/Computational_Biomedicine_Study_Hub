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
    assert module_ids == {f"bmb831.m{number:02d}" for number in range(1, 10)}

    for row in coverage_rows():
        assert set(row.requirement.module_ids) <= module_ids
        assert row.evidence.module_count == len(row.requirement.module_ids)
        if row.requirement.module_ids:
            assert row.evidence.objective_count > 0
            assert row.evidence.practice_count > 0
            assert row.evidence.assessment_count > 0
            assert row.evidence.objective_bank_count > 0
            assert row.evidence.executable_example_count > 0


def test_complete_authored_course_leaves_only_attendance_partial() -> None:
    summary = coverage_summary()
    assert summary.total == 15
    assert summary.covered == 14
    assert summary.partial == 1
    assert summary.gap == 0
    assert not summary.fully_covered

    assert BMB831_PUBLIC_EXAM == "Individual report"
    assert "not treated as real-patient evidence" in BMB831_SYNTHEA_BOUNDARY
    assert "does not define the course scope" in BMB831_SYNTHEA_BOUNDARY
    assert "public transcriptomics and proteomics" in BMB831_SYNTHEA_BOUNDARY

    partial = {
        requirement.requirement_id: requirement
        for requirement in OFFICIAL_BMB831_REQUIREMENTS
        if requirement.status is CoverageStatus.PARTIAL
    }
    assert set(partial) == {"bmb831.sdu.exam01"}
    assert partial["bmb831.sdu.exam01"].module_ids == tuple(
        f"bmb831.m{number:02d}" for number in range(1, 10)
    )
    assert "attendance" in partial["bmb831.sdu.exam01"].rationale.casefold()

    assert not any(
        requirement.status is CoverageStatus.GAP for requirement in OFFICIAL_BMB831_REQUIREMENTS
    )

    by_id = {
        requirement.requirement_id: requirement for requirement in OFFICIAL_BMB831_REQUIREMENTS
    }
    assert by_id["bmb831.sdu.ct05"].module_ids == ("bmb831.m07",)
    assert by_id["bmb831.sdu.exam02"].module_ids == ("bmb831.m09",)
    assert by_id["bmb831.sdu.ct05"].status is CoverageStatus.COVERED
    assert by_id["bmb831.sdu.exam02"].status is CoverageStatus.COVERED

    omics_rows = tuple(
        requirement
        for requirement in OFFICIAL_BMB831_REQUIREMENTS
        if "omics" in requirement.official_text.casefold()
    )
    assert omics_rows
    assert all(requirement.status is CoverageStatus.COVERED for requirement in omics_rows)
    assert all("bmb831.m06" in requirement.module_ids for requirement in omics_rows)
