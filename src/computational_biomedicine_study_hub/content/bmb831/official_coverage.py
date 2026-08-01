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
    "Synthea is used as a temporary synthetic clinical-data source for relational, "
    "longitudinal, large-table, modelling, visualisation, and critical-reasoning practice. "
    "It is not treated as real-patient evidence and cannot satisfy omics-pipeline or protein-"
    "characterisation requirements by itself."
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

OFFICIAL_BMB831_REQUIREMENTS: tuple[Requirement, ...] = (
    Requirement(
        "bmb831.sdu.lo01",
        RequirementKind.LEARNING_OUTCOME,
        "Independently analyse even conceptually demanding data sets.",
        _M01,
        CoverageStatus.PARTIAL,
        "The first module requires independent reasoning about relational grain, patient-level "
        "aggregation, time, provenance, and validation, but one bounded module is not a complete "
        "advanced analysis sequence.",
        "Add cumulative modelling, visualisation, interpretation, and report modules using the "
        "same explicit data contracts.",
    ),
    Requirement(
        "bmb831.sdu.lo02",
        RequirementKind.LEARNING_OUTCOME,
        "Work with large data amounts and carry out standard statistical analysis to identify relevant features.",
        _M01,
        CoverageStatus.PARTIAL,
        "The module teaches scalable table reduction, early filtering, dimension audits, and "
        "patient-level feature construction, but it currently uses deterministic teaching fixtures "
        "rather than a complete downloaded Synthea snapshot.",
        "Add a versioned Synthea CSV snapshot and memory-aware end-to-end feature pipeline.",
    ),
    Requirement(
        "bmb831.sdu.lo03",
        RequirementKind.LEARNING_OUTCOME,
        "Use standard algorithms for multi-variate analysis.",
        (),
        CoverageStatus.GAP,
        "No BMB831 multivariate module has yet been implemented.",
        "Add PCA, clustering, supervised dimensionality reduction, stability, and validation at "
        "advanced-course depth.",
    ),
    Requirement(
        "bmb831.sdu.lo04",
        RequirementKind.LEARNING_OUTCOME,
        "Design scripts for detailed visualisation of results.",
        (),
        CoverageStatus.GAP,
        "The first module audits tables but does not yet provide a complete advanced figure-building laboratory.",
        "Add layered statistical graphics, uncertainty, annotation, longitudinal displays, and "
        "reproducible export.",
    ),
    Requirement(
        "bmb831.sdu.lo05",
        RequirementKind.LEARNING_OUTCOME,
        "Know and apply tools for data interpretation.",
        _M01,
        CoverageStatus.PARTIAL,
        "The module applies provenance, cardinality, temporal-leakage, and external-validity "
        "reasoning, but does not yet include enrichment, pathway, or protein interpretation tools.",
        "Add biological interpretation modules and source-bounded appraisal tasks.",
    ),
    Requirement(
        "bmb831.sdu.lo06",
        RequirementKind.LEARNING_OUTCOME,
        "Know and apply standard pipelines for the processing of omics data.",
        (),
        CoverageStatus.GAP,
        "Synthea produces synthetic health records rather than omics abundance matrices and cannot "
        "stand in for transcriptomics or proteomics processing.",
        "Add separate synthetic or public omics matrices with explicit pipeline provenance.",
    ),
    Requirement(
        "bmb831.sdu.lo07",
        RequirementKind.LEARNING_OUTCOME,
        "Objectively discuss applied data-analysis methods presented, for example, in publications.",
        _M01,
        CoverageStatus.PARTIAL,
        "The first module trains claim boundaries and written reasoning but does not yet provide a "
        "structured appraisal of a complete publication.",
        "Add an individual publication-appraisal studio linked to the final report workflow.",
    ),
    Requirement(
        "bmb831.sdu.ct01",
        RequirementKind.CONTENT_TOPIC,
        "Statistics for large data sets.",
        _M01,
        CoverageStatus.PARTIAL,
        "Scalable relational preparation is introduced, while large-data estimation and modelling remain absent.",
        "Add chunked ingestion, efficient summaries, modelling, and performance measurement on a "
        "larger Synthea snapshot.",
    ),
    Requirement(
        "bmb831.sdu.ct02",
        RequirementKind.CONTENT_TOPIC,
        "Different types of data modelling.",
        (),
        CoverageStatus.GAP,
        "No complete BMB831 modelling block exists yet.",
        "Add regression, classification, count, survival or longitudinal models with explicit estimands and validation.",
    ),
    Requirement(
        "bmb831.sdu.ct03",
        RequirementKind.CONTENT_TOPIC,
        "Advanced data visualisation.",
        (),
        CoverageStatus.GAP,
        "No advanced visualisation module exists yet.",
        "Add a complete individually executable visualisation laboratory.",
    ),
    Requirement(
        "bmb831.sdu.ct04",
        RequirementKind.CONTENT_TOPIC,
        "Advanced data interpretation.",
        _M01,
        CoverageStatus.PARTIAL,
        "The first module introduces interpretation of provenance, dependency, leakage, and "
        "generalisation boundaries but not the full advanced biological interpretation scope.",
        "Extend interpretation to models, multiplicity, multivariate structure, and biological tools.",
    ),
    Requirement(
        "bmb831.sdu.ct05",
        RequirementKind.CONTENT_TOPIC,
        "Computational tools for protein characterisation.",
        (),
        CoverageStatus.GAP,
        "No protein-characterisation workflow is implemented.",
        "Add a dedicated protein-characterisation module using appropriate sequence, structure, "
        "annotation, and provenance resources.",
    ),
    Requirement(
        "bmb831.sdu.ct06",
        RequirementKind.CONTENT_TOPIC,
        "Standard workflows for data from omics experiments.",
        (),
        CoverageStatus.GAP,
        "No omics processing workflow is implemented and Synthea is explicitly excluded as a substitute.",
        "Add transcriptomics and proteomics teaching pipelines with synthetic or public matrices.",
    ),
    Requirement(
        "bmb831.sdu.exam01",
        RequirementKind.EXAM_COMPONENT,
        "Complete the tutorial and exercise prerequisite, including at least 80 percent participation.",
        _M01,
        CoverageStatus.PARTIAL,
        "The authored module provides individual exercises, but the application cannot certify "
        "attendance or equivalence with the official itslearning exercise set.",
        "Import the official exercise specification when available and keep attendance outside the "
        "application evidence model.",
    ),
    Requirement(
        "bmb831.sdu.exam02",
        RequirementKind.EXAM_COMPONENT,
        "Complete the individual report in English.",
        (),
        CoverageStatus.GAP,
        "No persistent BMB831 report workflow or internal preparation rubric exists yet.",
        "Add an individual English report studio with question, data manifest, methods, diagnostics, "
        "figures, results, limitations, reproducibility, and source-grounded revision.",
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
