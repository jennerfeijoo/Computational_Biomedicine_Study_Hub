"""Conservative BMB830 audit against the active public SDU specification.

Official requirements are transcribed from the active ODIN course description. Master-level
criteria are an explicit expert judgement layer and are never presented as unpublished SDU
requirements. The public specification contains an individual oral examination and tutorial
exercises; it does not publish a group project or group-presentation requirement.
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import StrEnum

from . import BUNDLES

BMB830_ODIN_SOURCE_URL = (
    "https://odin.sdu.dk/sitecore/index.php?a=searchfagbesk&internkode=bmb830&lang=en"
)
BMB830_ODIN_APPROVAL_DATE = "2025-03-06"
BMB830_ODIN_VERSION = "Approved - active"
BMB830_ODIN_AUDIT_DATE = "2026-08-01"
BMB830_PUBLIC_GROUP_PROJECT_REQUIRED = False
BMB830_APPLICATION_TEAMWORK_POLICY = (
    "No group project, role allocation, collaborative submission, or group-presentation workflow. "
    "All authored study activities are individually completable."
)


class CoverageStatus(StrEnum):
    """Conservative implementation state."""

    COVERED = "covered"
    PARTIAL = "partial"
    GAP = "gap"
    NOT_REQUIRED = "not_required"


class OfficialRequirementKind(StrEnum):
    """Section of the public SDU course specification."""

    LEARNING_OUTCOME = "learning_outcome"
    CONTENT_TOPIC = "content_topic"
    EXAM_COMPONENT = "exam_component"


class MasterCriterionKind(StrEnum):
    """Expert judgement axis used to assess master's-level readiness."""

    CONCEPTUAL_RIGOUR = "conceptual_rigour"
    COMPUTATIONAL_WORKFLOW = "computational_workflow"
    BIOLOGICAL_REALISM = "biological_realism"
    SCALE = "scale"
    MULTIVARIATE_ANALYSIS = "multivariate_analysis"
    CRITICAL_APPRAISAL = "critical_appraisal"
    ORAL_REASONING = "oral_reasoning"
    TEAMWORK = "teamwork"


@dataclass(frozen=True, slots=True)
class OfficialRequirement:
    """One stable public-course requirement and its current evidence mapping."""

    requirement_id: str
    kind: OfficialRequirementKind
    official_text: str
    module_ids: tuple[str, ...]
    status: CoverageStatus
    rationale: str
    next_action: str = ""

    def __post_init__(self) -> None:
        if not self.requirement_id.strip() or not self.official_text.strip():
            raise ValueError("Official requirements require stable IDs and text.")
        if not self.rationale.strip():
            raise ValueError("Official requirements require a rationale.")
        if self.status in {CoverageStatus.PARTIAL, CoverageStatus.GAP} and not self.next_action:
            raise ValueError("Partial and gap requirements require a next action.")


@dataclass(frozen=True, slots=True)
class MasterLevelCriterion:
    """One explicit expert judgement, separate from official SDU wording."""

    criterion_id: str
    kind: MasterCriterionKind
    expectation: str
    module_ids: tuple[str, ...]
    status: CoverageStatus
    rationale: str
    next_action: str = ""

    def __post_init__(self) -> None:
        if not self.criterion_id.strip() or not self.expectation.strip():
            raise ValueError("Master-level criteria require stable IDs and expectations.")
        if not self.rationale.strip():
            raise ValueError("Master-level criteria require a rationale.")
        if self.status in {CoverageStatus.PARTIAL, CoverageStatus.GAP} and not self.next_action:
            raise ValueError("Partial and gap criteria require a next action.")


@dataclass(frozen=True, slots=True)
class CoverageEvidence:
    """Counts of authored evidence exposed by mapped modules."""

    module_count: int
    objective_count: int
    practice_count: int
    assessment_count: int
    objective_bank_count: int
    executable_example_count: int


@dataclass(frozen=True, slots=True)
class OfficialCoverageRow:
    requirement: OfficialRequirement
    evidence: CoverageEvidence


@dataclass(frozen=True, slots=True)
class MasterCoverageRow:
    criterion: MasterLevelCriterion
    evidence: CoverageEvidence


@dataclass(frozen=True, slots=True)
class CoverageSummary:
    total: int
    covered: int
    partial: int
    gap: int
    not_required: int

    @property
    def fully_covered(self) -> bool:
        return self.partial == 0 and self.gap == 0


_ALL_MODULE_IDS = tuple(bundle.module.module_id for bundle in BUNDLES)

OFFICIAL_BMB830_REQUIREMENTS: tuple[OfficialRequirement, ...] = (
    OfficialRequirement(
        "bmb830.sdu.lo01",
        OfficialRequirementKind.LEARNING_OUTCOME,
        "Independently analyse biological data sets.",
        _ALL_MODULE_IDS,
        CoverageStatus.PARTIAL,
        "The course now provides a coherent individual workflow from R foundations through model "
        "validation, but most worked data are intentionally small and synthetic rather than one "
        "integrated biological data set.",
        "Add an individually completed biological-data analysis case with provenance, data quality, "
        "visualisation, modelling, diagnostics, interpretation, and reproducible reporting.",
    ),
    OfficialRequirement(
        "bmb830.sdu.lo02",
        OfficialRequirementKind.LEARNING_OUTCOME,
        "Work with large data amounts and carry out standard statistical analysis to identify relevant features.",
        ("bmb830.m01", "bmb830.m02", "bmb830.m06", "bmb830.m08", "bmb830.m10"),
        CoverageStatus.PARTIAL,
        "Standard analysis and reproducible R reasoning are covered, but the current laboratories do "
        "not yet exercise memory-aware processing or feature screening on a realistically large matrix.",
        "Add an individual high-dimensional biological matrix laboratory with explicit dimensions, "
        "missingness, filtering, feature summaries, and leakage-safe validation.",
    ),
    OfficialRequirement(
        "bmb830.sdu.lo03",
        OfficialRequirementKind.LEARNING_OUTCOME,
        "Use standard algorithms for multi-variate analysis.",
        (),
        CoverageStatus.GAP,
        "No completed BMB830 module yet teaches a standard multivariate algorithm.",
        "Add an introductory multivariate module covering scaling, distance, PCA, clustering, and "
        "biological interpretation with deterministic R examples.",
    ),
    OfficialRequirement(
        "bmb830.sdu.lo04",
        OfficialRequirementKind.LEARNING_OUTCOME,
        "Design scripts for detailed visualisation of results.",
        ("bmb830.m01", "bmb830.m02", "bmb830.m07", "bmb830.m09", "bmb830.m10"),
        CoverageStatus.COVERED,
        "The authored modules connect reproducible scripts to distribution, association, interaction, "
        "prediction, and diagnostic visualisation decisions, with practice and assessment evidence.",
    ),
    OfficialRequirement(
        "bmb830.sdu.lo05",
        OfficialRequirementKind.LEARNING_OUTCOME,
        "Apply tools for data interpretation.",
        (
            "bmb830.m02",
            "bmb830.m04",
            "bmb830.m05",
            "bmb830.m06",
            "bmb830.m07",
            "bmb830.m08",
            "bmb830.m09",
            "bmb830.m10",
        ),
        CoverageStatus.COVERED,
        "Effect sizes, intervals, tests, regression, interactions, diagnostics, and validation are "
        "interpreted in biomedical rather than purely computational terms.",
    ),
    OfficialRequirement(
        "bmb830.sdu.lo06",
        OfficialRequirementKind.LEARNING_OUTCOME,
        "Objectively discuss applied data-analysis methods presented, for example, in publications.",
        ("bmb830.m05", "bmb830.m06", "bmb830.m07", "bmb830.m08", "bmb830.m09", "bmb830.m10"),
        CoverageStatus.PARTIAL,
        "The course teaches the concepts needed for critique and includes oral explanations, but it "
        "does not yet provide a structured publication-methods appraisal workflow using a real paper.",
        "Add an individual critical-appraisal studio that separates design, estimand, assumptions, "
        "analysis, diagnostics, uncertainty, multiplicity, validation, and justified conclusions.",
    ),
    OfficialRequirement(
        "bmb830.sdu.ct01",
        OfficialRequirementKind.CONTENT_TOPIC,
        "Basic probability.",
        ("bmb830.m03", "bmb830.m04", "bmb830.m05"),
        CoverageStatus.COVERED,
        "Probability, sampling distributions, estimation, and hypothesis testing are explicitly taught.",
    ),
    OfficialRequirement(
        "bmb830.sdu.ct02",
        OfficialRequirementKind.CONTENT_TOPIC,
        "Different types of data modelling.",
        ("bmb830.m06", "bmb830.m07", "bmb830.m08", "bmb830.m09", "bmb830.m10"),
        CoverageStatus.COVERED,
        "Independent, paired, multi-group, linear, adjusted, interaction, nonlinear, and validation "
        "settings are represented with explicit design assumptions.",
    ),
    OfficialRequirement(
        "bmb830.sdu.ct03",
        OfficialRequirementKind.CONTENT_TOPIC,
        "Basic statistical models.",
        (
            "bmb830.m04",
            "bmb830.m05",
            "bmb830.m06",
            "bmb830.m07",
            "bmb830.m08",
            "bmb830.m09",
            "bmb830.m10",
        ),
        CoverageStatus.COVERED,
        "The course provides estimation, tests, ANOVA-style comparisons, regression, interactions, "
        "nonlinearity, diagnostics, and validation.",
    ),
    OfficialRequirement(
        "bmb830.sdu.ct04",
        OfficialRequirementKind.CONTENT_TOPIC,
        "Data visualisation.",
        ("bmb830.m02", "bmb830.m07", "bmb830.m09", "bmb830.m10"),
        CoverageStatus.COVERED,
        "Visualisation is treated as an analytical tool for distributions, relationships, fitted "
        "effects, and diagnostic patterns rather than decoration.",
    ),
    OfficialRequirement(
        "bmb830.sdu.ct05",
        OfficialRequirementKind.CONTENT_TOPIC,
        "Data interpretation.",
        (
            "bmb830.m02",
            "bmb830.m04",
            "bmb830.m05",
            "bmb830.m06",
            "bmb830.m07",
            "bmb830.m08",
            "bmb830.m09",
            "bmb830.m10",
        ),
        CoverageStatus.COVERED,
        "Every statistical block includes interpretation, uncertainty, assumptions, and limits of conclusions.",
    ),
    OfficialRequirement(
        "bmb830.sdu.ct06",
        OfficialRequirementKind.CONTENT_TOPIC,
        "Basic multi-variate analysis.",
        (),
        CoverageStatus.GAP,
        "The current catalog stops at regression diagnostics and validation.",
        "Implement scaling, PCA, clustering, distance choices, validation, and biological interpretation.",
    ),
    OfficialRequirement(
        "bmb830.sdu.exam01",
        OfficialRequirementKind.EXAM_COMPONENT,
        "Complete the tutorial and exercise prerequisite.",
        _ALL_MODULE_IDS,
        CoverageStatus.PARTIAL,
        "Every module includes individually completable practice, but the official itslearning "
        "exercise set and completion criteria are not public and cannot be reproduced or certified.",
        "Import the official exercise specification when available and map it without inventing "
        "group roles, group submissions, or unpublished grading rules.",
    ),
    OfficialRequirement(
        "bmb830.sdu.exam02",
        OfficialRequirementKind.EXAM_COMPONENT,
        "Complete the individual oral examination.",
        (
            "bmb830.m04",
            "bmb830.m05",
            "bmb830.m06",
            "bmb830.m07",
            "bmb830.m08",
            "bmb830.m09",
            "bmb830.m10",
        ),
        CoverageStatus.PARTIAL,
        "Oral-explanation activities exist throughout the course, but there is no dedicated timed "
        "individual oral-exam simulator spanning the complete syllabus.",
        "Add an individual oral-exam workflow with randomised syllabus coverage, statistical figures, "
        "R-output interpretation, follow-up questions, and an internal non-official rubric.",
    ),
)

MASTER_LEVEL_CRITERIA: tuple[MasterLevelCriterion, ...] = (
    MasterLevelCriterion(
        "bmb830.master.01",
        MasterCriterionKind.CONCEPTUAL_RIGOUR,
        "Explain assumptions, estimands, uncertainty, effect size, and limitations rather than applying tests by recipe.",
        (
            "bmb830.m03",
            "bmb830.m04",
            "bmb830.m05",
            "bmb830.m06",
            "bmb830.m07",
            "bmb830.m08",
            "bmb830.m09",
            "bmb830.m10",
        ),
        CoverageStatus.COVERED,
        "The course consistently prioritises reasoning, interpretation, and failure modes over menu-driven test selection.",
    ),
    MasterLevelCriterion(
        "bmb830.master.02",
        MasterCriterionKind.COMPUTATIONAL_WORKFLOW,
        "Build reproducible individual R workflows from data checking through modelling and validation.",
        _ALL_MODULE_IDS,
        CoverageStatus.COVERED,
        "The sequence is cumulative, script-based, and backed by conservative executable R laboratories.",
    ),
    MasterLevelCriterion(
        "bmb830.master.03",
        MasterCriterionKind.BIOLOGICAL_REALISM,
        "Analyse biological measurements with realistic metadata, dependence, missingness, and scientific interpretation.",
        ("bmb830.m02", "bmb830.m06", "bmb830.m08", "bmb830.m10"),
        CoverageStatus.PARTIAL,
        "Biological framing is strong, but most examples remain compact teaching data rather than a "
        "realistic end-to-end molecular or clinical data set.",
        "Add a provenance-preserving individual biological case study without fabricating an official SDU assignment.",
    ),
    MasterLevelCriterion(
        "bmb830.master.04",
        MasterCriterionKind.SCALE,
        "Handle high-dimensional or large biological data without confusing rows, features, and independent units.",
        ("bmb830.m01", "bmb830.m02", "bmb830.m08", "bmb830.m10"),
        CoverageStatus.PARTIAL,
        "The conceptual safeguards exist, but computational scale and high-dimensional feature workflows are not yet exercised.",
        "Add a bounded large-matrix laboratory and explicit patient-versus-feature dimension checks.",
    ),
    MasterLevelCriterion(
        "bmb830.master.05",
        MasterCriterionKind.MULTIVARIATE_ANALYSIS,
        "Use and interpret introductory multivariate methods such as PCA and clustering.",
        (),
        CoverageStatus.GAP,
        "This is the clearest remaining academic gap relative to both ODIN and normal master's-level biostatistics expectations.",
        "Implement the next module on scaling, PCA, distances, clustering, and validation.",
    ),
    MasterLevelCriterion(
        "bmb830.master.06",
        MasterCriterionKind.CRITICAL_APPRAISAL,
        "Critically appraise statistical methods and conclusions in biomedical publications.",
        ("bmb830.m05", "bmb830.m06", "bmb830.m07", "bmb830.m08", "bmb830.m09", "bmb830.m10"),
        CoverageStatus.PARTIAL,
        "The necessary reasoning is present, but no real-paper appraisal workflow has been implemented.",
        "Add an individual methods-critique exercise with source-bounded Ollama writing feedback and no model grading authority.",
    ),
    MasterLevelCriterion(
        "bmb830.master.07",
        MasterCriterionKind.ORAL_REASONING,
        "Defend model choice, assumptions, diagnostics, and interpretation orally under follow-up questioning.",
        (
            "bmb830.m04",
            "bmb830.m05",
            "bmb830.m06",
            "bmb830.m07",
            "bmb830.m08",
            "bmb830.m09",
            "bmb830.m10",
        ),
        CoverageStatus.PARTIAL,
        "Oral prompts exist, but they are not yet assembled into a timed individual examination experience.",
        "Add individual oral-exam rehearsal after multivariate coverage is complete.",
    ),
    MasterLevelCriterion(
        "bmb830.master.08",
        MasterCriterionKind.TEAMWORK,
        "Require a collaborative project or group presentation.",
        (),
        CoverageStatus.NOT_REQUIRED,
        "The active public BMB830 specification describes an individual oral exam and recommends "
        "group discussion during exercises, but it does not publish a group project or group presentation. "
        "The application deliberately keeps all activities individually completable.",
    ),
)


def _evidence_for(module_ids: tuple[str, ...]) -> CoverageEvidence:
    selected = tuple(bundle for bundle in BUNDLES if bundle.module.module_id in module_ids)
    return CoverageEvidence(
        module_count=len(selected),
        objective_count=sum(len(bundle.module.objectives) for bundle in selected),
        practice_count=sum(len(bundle.module.practice_exercises) for bundle in selected),
        assessment_count=sum(len(bundle.module.assessment_items) for bundle in selected),
        objective_bank_count=sum(len(bundle.objective_question_bank) for bundle in selected),
        executable_example_count=sum(len(bundle.module.worked_examples) for bundle in selected),
    )


def bmb830_official_coverage_matrix() -> tuple[OfficialCoverageRow, ...]:
    return tuple(
        OfficialCoverageRow(requirement=item, evidence=_evidence_for(item.module_ids))
        for item in OFFICIAL_BMB830_REQUIREMENTS
    )


def bmb830_master_level_matrix() -> tuple[MasterCoverageRow, ...]:
    return tuple(
        MasterCoverageRow(criterion=item, evidence=_evidence_for(item.module_ids))
        for item in MASTER_LEVEL_CRITERIA
    )


def _summary(statuses: tuple[CoverageStatus, ...]) -> CoverageSummary:
    return CoverageSummary(
        total=len(statuses),
        covered=statuses.count(CoverageStatus.COVERED),
        partial=statuses.count(CoverageStatus.PARTIAL),
        gap=statuses.count(CoverageStatus.GAP),
        not_required=statuses.count(CoverageStatus.NOT_REQUIRED),
    )


def bmb830_official_coverage_summary() -> CoverageSummary:
    return _summary(tuple(row.requirement.status for row in bmb830_official_coverage_matrix()))


def bmb830_master_level_summary() -> CoverageSummary:
    return _summary(tuple(row.criterion.status for row in bmb830_master_level_matrix()))


def validate_bmb830_coverage() -> None:
    official_rows = bmb830_official_coverage_matrix()
    master_rows = bmb830_master_level_matrix()
    ids = tuple(row.requirement.requirement_id for row in official_rows) + tuple(
        row.criterion.criterion_id for row in master_rows
    )
    if len(ids) != len(set(ids)):
        raise ValueError("The BMB830 audit contains duplicate stable IDs.")

    known = set(_ALL_MODULE_IDS)
    referenced = {
        module_id
        for row in (*official_rows, *master_rows)
        for module_id in (
            row.requirement.module_ids
            if isinstance(row, OfficialCoverageRow)
            else row.criterion.module_ids
        )
    }
    unknown = referenced - known
    if unknown:
        raise ValueError(
            "The BMB830 audit references unknown modules: " + ", ".join(sorted(unknown))
        )

    expected_official_counts = {
        OfficialRequirementKind.LEARNING_OUTCOME: 6,
        OfficialRequirementKind.CONTENT_TOPIC: 6,
        OfficialRequirementKind.EXAM_COMPONENT: 2,
    }
    for kind, expected in expected_official_counts.items():
        actual = sum(row.requirement.kind is kind for row in official_rows)
        if actual != expected:
            raise ValueError(f"BMB830 requires {expected} {kind.value} rows, found {actual}.")

    for row in official_rows:
        if row.requirement.module_ids and row.evidence.module_count != len(
            row.requirement.module_ids
        ):
            raise ValueError(f"Incomplete evidence for {row.requirement.requirement_id}.")
        if row.requirement.status is CoverageStatus.COVERED:
            if row.evidence.practice_count == 0 or (
                row.evidence.assessment_count + row.evidence.objective_bank_count == 0
            ):
                raise ValueError(
                    f"Covered requirement {row.requirement.requirement_id} lacks evidence."
                )

    teamwork = next(
        row for row in master_rows if row.criterion.kind is MasterCriterionKind.TEAMWORK
    )
    if teamwork.criterion.status is not CoverageStatus.NOT_REQUIRED:
        raise ValueError("BMB830 teamwork must remain explicitly not required.")
    if teamwork.evidence.module_count != 0 or BMB830_PUBLIC_GROUP_PROJECT_REQUIRED:
        raise ValueError("BMB830 must not fabricate a group-project requirement.")


validate_bmb830_coverage()

__all__ = [
    "BMB830_APPLICATION_TEAMWORK_POLICY",
    "BMB830_ODIN_APPROVAL_DATE",
    "BMB830_ODIN_AUDIT_DATE",
    "BMB830_ODIN_SOURCE_URL",
    "BMB830_ODIN_VERSION",
    "BMB830_PUBLIC_GROUP_PROJECT_REQUIRED",
    "CoverageEvidence",
    "CoverageStatus",
    "CoverageSummary",
    "MASTER_LEVEL_CRITERIA",
    "MasterCriterionKind",
    "MasterCoverageRow",
    "MasterLevelCriterion",
    "OFFICIAL_BMB830_REQUIREMENTS",
    "OfficialCoverageRow",
    "OfficialRequirement",
    "OfficialRequirementKind",
    "bmb830_master_level_matrix",
    "bmb830_master_level_summary",
    "bmb830_official_coverage_matrix",
    "bmb830_official_coverage_summary",
    "validate_bmb830_coverage",
]
