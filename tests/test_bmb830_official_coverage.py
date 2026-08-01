"""Regression tests for the BMB830 official and master-level audit."""

from computational_biomedicine_study_hub.content.bmb830.official_coverage import (
    BMB830_APPLICATION_TEAMWORK_POLICY,
    BMB830_ODIN_APPROVAL_DATE,
    BMB830_ODIN_VERSION,
    BMB830_PUBLIC_GROUP_PROJECT_REQUIRED,
    CoverageStatus,
    MasterCriterionKind,
    OfficialRequirementKind,
    bmb830_master_level_matrix,
    bmb830_master_level_summary,
    bmb830_official_coverage_matrix,
    bmb830_official_coverage_summary,
    validate_bmb830_coverage,
)


def test_bmb830_audit_matches_active_public_sdu_structure() -> None:
    validate_bmb830_coverage()
    rows = bmb830_official_coverage_matrix()

    assert BMB830_ODIN_APPROVAL_DATE == "2025-03-06"
    assert BMB830_ODIN_VERSION == "Approved - active"
    assert len(rows) == 14
    assert (
        sum(row.requirement.kind is OfficialRequirementKind.LEARNING_OUTCOME for row in rows) == 6
    )
    assert sum(row.requirement.kind is OfficialRequirementKind.CONTENT_TOPIC for row in rows) == 6
    assert sum(row.requirement.kind is OfficialRequirementKind.EXAM_COMPONENT for row in rows) == 2


def test_bmb830_official_audit_closes_multivariate_gap_but_keeps_partial_work_visible() -> None:
    rows = {row.requirement.requirement_id: row for row in bmb830_official_coverage_matrix()}

    assert rows["bmb830.sdu.lo03"].requirement.status is CoverageStatus.COVERED
    assert rows["bmb830.sdu.ct06"].requirement.status is CoverageStatus.COVERED
    assert rows["bmb830.sdu.lo01"].requirement.status is CoverageStatus.PARTIAL
    assert rows["bmb830.sdu.lo02"].requirement.status is CoverageStatus.PARTIAL
    assert rows["bmb830.sdu.lo06"].requirement.status is CoverageStatus.PARTIAL
    assert rows["bmb830.sdu.exam02"].requirement.status is CoverageStatus.PARTIAL

    summary = bmb830_official_coverage_summary()
    assert summary.total == 14
    assert summary.covered == 8
    assert summary.partial == 6
    assert summary.gap == 0
    assert not summary.fully_covered


def test_bmb830_master_level_evaluation_is_separate_and_conservative() -> None:
    rows = {row.criterion.kind: row for row in bmb830_master_level_matrix()}

    assert rows[MasterCriterionKind.CONCEPTUAL_RIGOUR].criterion.status is CoverageStatus.COVERED
    assert (
        rows[MasterCriterionKind.COMPUTATIONAL_WORKFLOW].criterion.status is CoverageStatus.COVERED
    )
    assert rows[MasterCriterionKind.BIOLOGICAL_REALISM].criterion.status is CoverageStatus.PARTIAL
    assert rows[MasterCriterionKind.SCALE].criterion.status is CoverageStatus.COVERED
    assert (
        rows[MasterCriterionKind.MULTIVARIATE_ANALYSIS].criterion.status is CoverageStatus.COVERED
    )
    assert rows[MasterCriterionKind.CRITICAL_APPRAISAL].criterion.status is CoverageStatus.PARTIAL
    assert rows[MasterCriterionKind.ORAL_REASONING].criterion.status is CoverageStatus.PARTIAL

    summary = bmb830_master_level_summary()
    assert summary.total == 8
    assert summary.covered == 4
    assert summary.partial == 3
    assert summary.gap == 0
    assert summary.not_required == 1
    assert not summary.fully_covered


def test_bmb830_does_not_fabricate_teamwork_assessment() -> None:
    teamwork = next(
        row
        for row in bmb830_master_level_matrix()
        if row.criterion.kind is MasterCriterionKind.TEAMWORK
    )

    assert not BMB830_PUBLIC_GROUP_PROJECT_REQUIRED
    assert teamwork.criterion.status is CoverageStatus.NOT_REQUIRED
    assert teamwork.evidence.module_count == 0
    policy = BMB830_APPLICATION_TEAMWORK_POLICY.casefold()
    assert "no group project" in policy
    assert "all authored study activities are individually completable" in policy
