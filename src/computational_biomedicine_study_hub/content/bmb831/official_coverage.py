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
    "longitudinal practice. It is not treated as real-patient evidence and does not define "
    "the course scope. Separate modules cover omics matrices, differential and multivariate "
    "analysis, advanced visualisation, public transcriptomics and proteomics workflow "
    "contracts, protein characterisation, biological interpretation, publication appraisal, "
    "and the individual English report."
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


_M01_09 = tuple(f"bmb831.m{number:02d}" for number in range(1, 10))
_M02_06 = tuple(f"bmb831.m{number:02d}" for number in range(2, 7))
_M03_06 = tuple(f"bmb831.m{number:02d}" for number in range(3, 7))
_M03_09 = tuple(f"bmb831.m{number:02d}" for number in range(3, 10))

OFFICIAL_BMB831_REQUIREMENTS: tuple[Requirement, ...] = (
    Requirement(
        "bmb831.sdu.lo01",
        RequirementKind.LEARNING_OUTCOME,
        "Independently analyse even conceptually demanding data sets.",
        _M01_09,
        CoverageStatus.COVERED,
        "The nine-module sequence requires independent work from relational and omics data "
        "contracts through modelling, visualisation, biological interpretation, publication "
        "appraisal, and a persistent individual report.",
    ),
    Requirement(
        "bmb831.sdu.lo02",
        RequirementKind.LEARNING_OUTCOME,
        "Work with large data amounts and carry out standard statistical analysis to identify relevant features.",
        ("bmb831.m01", "bmb831.m02", "bmb831.m03", "bmb831.m04", "bmb831.m06"),
        CoverageStatus.COVERED,
        "The authored workflow covers scalable table and matrix contracts, filtering, feature "
        "identification, multiplicity, dimensionality reduction, and versioned public-source "
        "snapshot requirements without bundling mutable remote data.",
    ),
    Requirement(
        "bmb831.sdu.lo03",
        RequirementKind.LEARNING_OUTCOME,
        "Use standard algorithms for multi-variate analysis.",
        ("bmb831.m04",),
        CoverageStatus.COVERED,
        "Module 4 covers PCA, scores, loadings, explained variance, distance choice, clustering, "
        "stability, batch interpretation, and leakage-safe supervised reduction.",
    ),
    Requirement(
        "bmb831.sdu.lo04",
        RequirementKind.LEARNING_OUTCOME,
        "Design scripts for detailed visualisation of results.",
        ("bmb831.m05",),
        CoverageStatus.COVERED,
        "Module 5 covers figure contracts, MA and volcano reasoning, heatmaps, uncertainty, "
        "annotation alignment, accessibility, and reproducible export.",
    ),
    Requirement(
        "bmb831.sdu.lo05",
        RequirementKind.LEARNING_OUTCOME,
        "Know and apply tools for data interpretation.",
        ("bmb831.m03", "bmb831.m04", "bmb831.m05", "bmb831.m07", "bmb831.m08"),
        CoverageStatus.COVERED,
        "The course applies effect-size and uncertainty reasoning, multivariate stability, "
        "protein evidence, identifier mapping, enrichment, pathways, networks, redundancy, "
        "and explicit claim boundaries.",
    ),
    Requirement(
        "bmb831.sdu.lo06",
        RequirementKind.LEARNING_OUTCOME,
        "Know and apply standard pipelines for the processing of omics data.",
        _M02_06,
        CoverageStatus.COVERED,
        "Modules 2–6 form a complete workflow from matrix and metadata validation through QC, "
        "normalisation, differential modelling, multivariate analysis, visualisation, and "
        "versioned public transcriptomics and proteomics source contracts.",
    ),
    Requirement(
        "bmb831.sdu.lo07",
        RequirementKind.LEARNING_OUTCOME,
        "Objectively discuss applied data-analysis methods presented, for example, in publications.",
        ("bmb831.m03", "bmb831.m04", "bmb831.m05", "bmb831.m08", "bmb831.m09"),
        CoverageStatus.COVERED,
        "Module 9 provides publication appraisal and claim-to-evidence tracing, supported by the "
        "methodological assumptions, sensitivity checks, and inferential limits trained earlier.",
    ),
    Requirement(
        "bmb831.sdu.ct01",
        RequirementKind.CONTENT_TOPIC,
        "Statistics for large data sets.",
        ("bmb831.m01", "bmb831.m02", "bmb831.m03", "bmb831.m04", "bmb831.m06"),
        CoverageStatus.COVERED,
        "The sequence covers scalable data contracts, high-dimensional screening, multiplicity, "
        "dimension reduction, and public-source snapshot and transition auditing.",
    ),
    Requirement(
        "bmb831.sdu.ct02",
        RequirementKind.CONTENT_TOPIC,
        "Different types of data modelling.",
        _M03_06,
        CoverageStatus.COVERED,
        "The course distinguishes count and Gaussian reasoning, adjusted contrasts, unsupervised "
        "projection, clustering, supervised selection boundaries, and modality-specific workflows.",
    ),
    Requirement(
        "bmb831.sdu.ct03",
        RequirementKind.CONTENT_TOPIC,
        "Advanced data visualisation.",
        ("bmb831.m05",),
        CoverageStatus.COVERED,
        "Module 5 provides an advanced visualisation block covering figure design, diagnostic and "
        "differential plots, heatmaps, uncertainty, accessibility, and reproducible export.",
    ),
    Requirement(
        "bmb831.sdu.ct04",
        RequirementKind.CONTENT_TOPIC,
        "Advanced data interpretation.",
        _M03_09,
        CoverageStatus.COVERED,
        "Interpretation spans estimands, effect sizes, multiplicity, geometry, stability, visual "
        "evidence, protein annotation, enrichment, pathways, networks, and publication appraisal.",
    ),
    Requirement(
        "bmb831.sdu.ct05",
        RequirementKind.CONTENT_TOPIC,
        "Computational tools for protein characterisation.",
        ("bmb831.m07",),
        CoverageStatus.COVERED,
        "Module 7 covers exact sequence identity, physicochemical descriptors, InterPro-style "
        "domains, UniProt evidence provenance, PDB coverage, and AlphaFold confidence boundaries.",
    ),
    Requirement(
        "bmb831.sdu.ct06",
        RequirementKind.CONTENT_TOPIC,
        "Standard workflows for data from omics experiments.",
        _M02_06,
        CoverageStatus.COVERED,
        "Modules 2–6 provide transcriptomics and proteomics workflow contracts from input "
        "validation through statistical and visual outputs, with immutable local artifact and "
        "checksum requirements for public sources.",
    ),
    Requirement(
        "bmb831.sdu.exam01",
        RequirementKind.EXAM_COMPONENT,
        "Complete the tutorial and exercise prerequisite, including at least 80 percent participation.",
        _M01_09,
        CoverageStatus.PARTIAL,
        "The application provides individually completable exercises across all nine modules, but "
        "it cannot certify institutional attendance or equivalence with the official Itslearning set.",
        "Use the official attendance record and exercise set when SDU makes them available to the learner.",
    ),
    Requirement(
        "bmb831.sdu.exam02",
        RequirementKind.EXAM_COMPONENT,
        "Complete the individual report in English.",
        ("bmb831.m09",),
        CoverageStatus.COVERED,
        "Module 9 and the persistent ten-section report studio cover question, data, methods, QC, "
        "results, figures, biological interpretation, limitations, reproducibility, and abstract. "
        "The tool supports preparation without claiming an official grade or private-rubric equivalence.",
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
