"""Conservative BMB831 audit against the active public SDU specification."""

from __future__ import annotations

from dataclasses import dataclass
from enum import StrEnum

from . import BUNDLES

BMB831_ODIN_SOURCE_URL = (
    "https://odin.sdu.dk/sitecore/index.php?a=searchfagbesk&internkode=BMB831&lang=en"
)
BMB831_ODIN_APPROVAL_DATE = "2025-03-06"
BMB831_ODIN_VERSION = "Approved - active"
BMB831_ODIN_AUDIT_DATE = "2026-08-01"
BMB831_PUBLIC_EXAM = "Individual report"
BMB831_SYNTHEA_BOUNDARY = (
    "Synthea is retained only as one synthetic clinical-data case for relational and "
    "longitudinal practice. It is not treated as real-patient evidence and no longer defines "
    "the course scope. Separate omics modules cover assay matrices, quality control, "
    "normalization, differential modeling, and multiplicity, while public or learner-owned real "
    "omics data remain required for the final project."
)


class CoverageStatus(StrEnum):
    """Conservative implementation state for one public requirement."""

    COVERED = "covered"
    PARTIAL = "partial"
    GAP = "gap"


class RequirementKind(StrEnum):
    """Section of the public course specification."""

    LEARNING_OUTCOME = "learning_outcome"
    CONTENT_TOPIC = "content_topic"
    EXAM_COMPONENT = "exam_component"


@dataclass(frozen=True, slots=True)
class Requirement:
    """One stable public requirement and its current evidence mapping."""

    requirement_id: str
    kind: RequirementKind
    official_text: str
    module_ids: tuple[str, ...]
    status: CoverageStatus
    rationale: str
    next_action: str = ""

    def __post_init__(self) -> None:
        if not self.requirement_id.strip() or not self.official_text.strip():
            raise ValueError("BMB831 requirements require stable IDs and text.")
        if not self.rationale.strip():
            raise ValueError("BMB831 requirements require a rationale.")
        if self.status is not CoverageStatus.COVERED and not self.next_action.strip():
            raise ValueError("Partial and gap requirements require a next action.")


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
class CoverageRow:
    requirement: Requirement
    evidence: CoverageEvidence


@dataclass(frozen=True, slots=True)
class CoverageSummary:
    total: int
    covered: int
    partial: int
    gap: int

    @property
    def fully_covered(self) -> bool:
        return self.partial == 0 and self.gap == 0


_M01 = ("bmb831.m01",)
_M02 = ("bmb831.m02",)
_M03 = ("bmb831.m03",)
_M01_03 = ("bmb831.m01", "bmb831.m02", "bmb831.m03")
_M02_03 = ("bmb831.m02", "bmb831.m03")

OFFICIAL_BMB831_REQUIREMENTS: tuple[Requirement, ...] = (
    Requirement(
        "bmb831.sdu.lo01",
        RequirementKind.LEARNING_OUTCOME,
        "Independently analyse even conceptually demanding data sets.",
        _M01_03,
        CoverageStatus.PARTIAL,
        "Three modules now require independent reasoning about relational clinical data, omics "
        "matrix contracts, quality control, design matrices, differential effects, and multiplicity. "
        "The sequence still lacks multivariate, protein-characterisation, interpretation, and final "
        "report integration.",
        "Complete the remaining advanced modules and one cumulative real-data project.",
    ),
    Requirement(
        "bmb831.sdu.lo02",
        RequirementKind.LEARNING_OUTCOME,
        "Work with large data amounts and carry out standard statistical analysis to identify relevant features.",
        _M01_03,
        CoverageStatus.PARTIAL,
        "The course now covers scalable contracts, early filtering, assay quality control, feature "
        "screening, differential modeling, and false-discovery control with bounded executable "
        "examples. A substantially larger versioned dataset is still absent.",
        "Add a public transcriptomics or proteomics snapshot with measured memory and runtime.",
    ),
    Requirement(
        "bmb831.sdu.lo03",
        RequirementKind.LEARNING_OUTCOME,
        "Use standard algorithms for multi-variate analysis.",
        (),
        CoverageStatus.GAP,
        "No dedicated BMB831 multivariate module has yet been implemented.",
        "Add PCA, clustering, distance choice, stability, and leakage-safe supervised reduction.",
    ),
    Requirement(
        "bmb831.sdu.lo04",
        RequirementKind.LEARNING_OUTCOME,
        "Design scripts for detailed visualisation of results.",
        _M02,
        CoverageStatus.PARTIAL,
        "Module 2 teaches diagnostic distributions, profile deviation, and PCA-quality reasoning, "
        "but it does not yet provide a complete advanced figure-building laboratory.",
        "Add layered QC, differential, multivariate, and annotation figures with reproducible export.",
    ),
    Requirement(
        "bmb831.sdu.lo05",
        RequirementKind.LEARNING_OUTCOME,
        "Know and apply tools for data interpretation.",
        _M01_03,
        CoverageStatus.PARTIAL,
        "The modules apply provenance, design, effect-size, multiplicity, batch, leakage, and claim-"
        "boundary reasoning. Enrichment, pathway, network, and protein tools remain absent.",
        "Add biological interpretation and protein-characterisation workflows.",
    ),
    Requirement(
        "bmb831.sdu.lo06",
        RequirementKind.LEARNING_OUTCOME,
        "Know and apply standard pipelines for the processing of omics data.",
        _M02_03,
        CoverageStatus.PARTIAL,
        "The omics core now covers assay contracts, sample alignment, filtering, normalization, "
        "transformation, count-model reasoning, differential contrasts, and FDR. It remains based on "
        "bounded teaching matrices rather than a complete public real-data pipeline.",
        "Add end-to-end transcriptomics and proteomics cases with package-level provenance.",
    ),
    Requirement(
        "bmb831.sdu.lo07",
        RequirementKind.LEARNING_OUTCOME,
        "Objectively discuss applied data-analysis methods presented, for example, in publications.",
        _M01_03,
        CoverageStatus.PARTIAL,
        "Every module trains explicit claim boundaries, method assumptions, alternative explanations, "
        "and limitations, but no complete publication appraisal has yet been authored.",
        "Add a source-grounded publication-appraisal studio linked to the report workflow.",
    ),
    Requirement(
        "bmb831.sdu.ct01",
        RequirementKind.CONTENT_TOPIC,
        "Statistics for large data sets.",
        _M01_03,
        CoverageStatus.PARTIAL,
        "Scalable relational and matrix workflows, early reduction, model design, and multiple testing "
        "are present. Large external data and performance profiling remain incomplete.",
        "Run the workflows on a versioned larger dataset and record resource use.",
    ),
    Requirement(
        "bmb831.sdu.ct02",
        RequirementKind.CONTENT_TOPIC,
        "Different types of data modelling.",
        _M03,
        CoverageStatus.PARTIAL,
        "Module 3 distinguishes Gaussian and overdispersed count models and introduces covariate-"
        "adjusted contrasts. Classification, regularization, survival, and longitudinal models remain.",
        "Add advanced predictive and longitudinal modeling with leakage-safe validation.",
    ),
    Requirement(
        "bmb831.sdu.ct03",
        RequirementKind.CONTENT_TOPIC,
        "Advanced data visualisation.",
        _M02,
        CoverageStatus.PARTIAL,
        "Quality-control visual reasoning is introduced, but the detailed visualization requirement "
        "is not yet covered by a dedicated scripting module.",
        "Add a full visualization module with uncertainty, labels, panels, and export contracts.",
    ),
    Requirement(
        "bmb831.sdu.ct04",
        RequirementKind.CONTENT_TOPIC,
        "Advanced data interpretation.",
        _M01_03,
        CoverageStatus.PARTIAL,
        "Interpretation now includes provenance, dependence, batch, estimands, effect size, "
        "uncertainty, multiplicity, and inferential limits. Biological pathway and network "
        "interpretation remain absent.",
        "Extend interpretation to enrichment, pathways, networks, and publication appraisal.",
    ),
    Requirement(
        "bmb831.sdu.ct05",
        RequirementKind.CONTENT_TOPIC,
        "Computational tools for protein characterisation.",
        (),
        CoverageStatus.GAP,
        "No protein-characterisation workflow is implemented.",
        "Add sequence, domain, physicochemical, structure, annotation, and provenance practice.",
    ),
    Requirement(
        "bmb831.sdu.ct06",
        RequirementKind.CONTENT_TOPIC,
        "Standard workflows for data from omics experiments.",
        _M02_03,
        CoverageStatus.PARTIAL,
        "A standard omics core is now authored from matrix validation through differential results, "
        "but complete transcriptomics and proteomics pipelines on versioned real data remain absent.",
        "Add public real-data workflows and a cumulative analysis artifact.",
    ),
    Requirement(
        "bmb831.sdu.exam01",
        RequirementKind.EXAM_COMPONENT,
        "Complete the tutorial and exercise prerequisite, including at least 80 percent participation.",
        _M01_03,
        CoverageStatus.PARTIAL,
        "The application provides individual exercises for all completed modules, but it cannot "
        "certify attendance or equivalence with the official itslearning exercise set.",
        "Import official exercises when available and keep attendance outside the evidence model.",
    ),
    Requirement(
        "bmb831.sdu.exam02",
        RequirementKind.EXAM_COMPONENT,
        "Complete the individual report in English.",
        (),
        CoverageStatus.GAP,
        "No persistent BMB831 report workflow or internal preparation rubric exists yet.",
        "Add an English report studio covering question, data, methods, diagnostics, figures, results, "
        "limitations, reproducibility, and source-grounded revision.",
    ),
)


def _evidence(module_ids: tuple[str, ...]) -> CoverageEvidence:
    bundles = tuple(bundle for bundle in BUNDLES if bundle.module.module_id in module_ids)
    return CoverageEvidence(
        module_count=len(bundles),
        objective_count=sum(len(bundle.module.objectives) for bundle in bundles),
        practice_count=sum(len(bundle.module.practice_exercises) for bundle in bundles),
        assessment_count=sum(len(bundle.module.assessment_items) for bundle in bundles),
        objective_bank_count=sum(len(bundle.objective_question_bank) for bundle in bundles),
        executable_example_count=sum(len(bundle.module.worked_examples) for bundle in bundles),
    )


def coverage_rows() -> tuple[CoverageRow, ...]:
    """Return every official requirement with current authored evidence counts."""

    return tuple(
        CoverageRow(requirement=requirement, evidence=_evidence(requirement.module_ids))
        for requirement in OFFICIAL_BMB831_REQUIREMENTS
    )


def coverage_summary() -> CoverageSummary:
    """Summarise the current public-specification implementation state."""

    statuses = tuple(requirement.status for requirement in OFFICIAL_BMB831_REQUIREMENTS)
    return CoverageSummary(
        total=len(statuses),
        covered=statuses.count(CoverageStatus.COVERED),
        partial=statuses.count(CoverageStatus.PARTIAL),
        gap=statuses.count(CoverageStatus.GAP),
    )


__all__ = [
    "BMB831_ODIN_APPROVAL_DATE",
    "BMB831_ODIN_AUDIT_DATE",
    "BMB831_ODIN_SOURCE_URL",
    "BMB831_ODIN_VERSION",
    "BMB831_PUBLIC_EXAM",
    "BMB831_SYNTHEA_BOUNDARY",
    "CoverageEvidence",
    "CoverageRow",
    "CoverageStatus",
    "CoverageSummary",
    "OFFICIAL_BMB831_REQUIREMENTS",
    "Requirement",
    "RequirementKind",
    "coverage_rows",
    "coverage_summary",
]
