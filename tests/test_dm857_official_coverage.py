"""Regression tests for the active SDU DM857 coverage audit."""

from computational_biomedicine_study_hub.content.dm857.official_coverage import (
    CoverageStatus,
    DM857_ODIN_APPROVAL_DATE,
    DM857_ODIN_VERSION,
    OfficialRequirementKind,
    dm857_official_coverage_matrix,
    dm857_official_coverage_summary,
    validate_dm857_official_coverage,
)


def test_official_dm857_matrix_matches_active_sdu_structure() -> None:
    validate_dm857_official_coverage()
    rows = dm857_official_coverage_matrix()

    assert DM857_ODIN_APPROVAL_DATE == "2025-04-11"
    assert DM857_ODIN_VERSION == "Approved - active"
    assert len(rows) == 16
    assert sum(
        row.requirement.kind is OfficialRequirementKind.LEARNING_OUTCOME for row in rows
    ) == 8
    assert sum(
        row.requirement.kind is OfficialRequirementKind.CONTENT_TOPIC for row in rows
    ) == 5
    assert sum(
        row.requirement.kind is OfficialRequirementKind.EXAM_COMPONENT for row in rows
    ) == 3


def test_official_dm857_learning_and_content_requirements_have_practice_and_assessment() -> None:
    rows = dm857_official_coverage_matrix()
    academic_rows = tuple(
        row
        for row in rows
        if row.requirement.kind
        in {
            OfficialRequirementKind.LEARNING_OUTCOME,
            OfficialRequirementKind.CONTENT_TOPIC,
        }
    )

    assert len(academic_rows) == 13
    assert all(row.requirement.status is CoverageStatus.COVERED for row in academic_rows)
    assert all(row.evidence.module_count > 0 for row in academic_rows)
    assert all(row.evidence.learning_objective_count > 0 for row in academic_rows)
    assert all(row.evidence.practice_exercise_count > 0 for row in academic_rows)
    assert all(
        row.evidence.authored_assessment_count + row.evidence.objective_bank_item_count > 0
        for row in academic_rows
    )


def test_official_dm857_matrix_exposes_exam_readiness_gaps() -> None:
    rows = dm857_official_coverage_matrix()
    exam_rows = {
        row.requirement.requirement_id: row
        for row in rows
        if row.requirement.kind is OfficialRequirementKind.EXAM_COMPONENT
    }

    assert exam_rows["dm857.sdu.exam01"].requirement.status is CoverageStatus.PARTIAL
    assert exam_rows["dm857.sdu.exam02"].requirement.status is CoverageStatus.GAP
    assert exam_rows["dm857.sdu.exam02"].evidence.module_count == 0
    assert exam_rows["dm857.sdu.exam03"].requirement.status is CoverageStatus.PARTIAL
    assert all(row.requirement.next_action for row in exam_rows.values())


def test_official_dm857_summary_does_not_claim_full_completion() -> None:
    summary = dm857_official_coverage_summary()

    assert summary.requirement_count == 16
    assert summary.covered_count == 13
    assert summary.partial_count == 2
    assert summary.gap_count == 1
    assert not summary.fully_covered
