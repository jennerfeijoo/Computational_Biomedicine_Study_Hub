"""Trace the active SDU DM857 specification to authored study-hub evidence.

The matrix is intentionally conservative. A requirement is marked covered only when
current authored modules provide teaching, practice, and assessment evidence. Exam
components remain partial or gaps until the application implements the required
experience and can be checked against the available official assessment materials.
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import StrEnum

from . import BUNDLES

DM857_ODIN_SOURCE_URL = (
    "https://odin.sdu.dk/sitecore/index.php?a=searchfagbesk&internkode=DM857&lang=en"
)
DM857_ODIN_APPROVAL_DATE = "2025-04-11"
DM857_ODIN_VERSION = "Approved - active"
DM857_ODIN_AUDIT_DATE = "2026-07-31"


class OfficialRequirementKind(StrEnum):
    """Section of the active SDU course specification."""

    LEARNING_OUTCOME = "learning_outcome"
    CONTENT_TOPIC = "content_topic"
    EXAM_COMPONENT = "exam_component"


class CoverageStatus(StrEnum):
    """Conservative implementation state for one official requirement."""

    COVERED = "covered"
    PARTIAL = "partial"
    GAP = "gap"


@dataclass(frozen=True, slots=True)
class OfficialRequirement:
    """One stable requirement transcribed from the active SDU specification."""

    requirement_id: str
    kind: OfficialRequirementKind
    official_text: str
    module_ids: tuple[str, ...]
    status: CoverageStatus
    rationale: str
    next_action: str = ""

    def __post_init__(self) -> None:
        if not self.requirement_id.strip():
            raise ValueError("Official requirements require a stable ID.")
        if not self.official_text.strip():
            raise ValueError(f"Requirement {self.requirement_id!r} requires official text.")
        if not self.rationale.strip():
            raise ValueError(f"Requirement {self.requirement_id!r} requires a rationale.")
        if self.status is CoverageStatus.COVERED and not self.module_ids:
            raise ValueError("Covered requirements require authored module evidence.")
        if self.status is not CoverageStatus.COVERED and not self.next_action.strip():
            raise ValueError("Partial and gap requirements require a concrete next action.")


@dataclass(frozen=True, slots=True)
class CoverageEvidence:
    """Counts of authored evidence exposed by mapped module bundles."""

    module_count: int
    learning_objective_count: int
    practice_exercise_count: int
    authored_assessment_count: int
    objective_bank_item_count: int


@dataclass(frozen=True, slots=True)
class OfficialCoverageRow:
    """One official requirement joined to validated authored evidence."""

    requirement: OfficialRequirement
    evidence: CoverageEvidence


@dataclass(frozen=True, slots=True)
class OfficialCoverageSummary:
    """Aggregate state of the official coverage audit."""

    requirement_count: int
    covered_count: int
    partial_count: int
    gap_count: int

    @property
    def fully_covered(self) -> bool:
        return self.partial_count == 0 and self.gap_count == 0


_ALL_MODULE_IDS = tuple(bundle.module.module_id for bundle in BUNDLES)

OFFICIAL_DM857_REQUIREMENTS: tuple[OfficialRequirement, ...] = (
    OfficialRequirement(
        "dm857.sdu.lo01",
        OfficialRequirementKind.LEARNING_OUTCOME,
        "Design models for concrete problems.",
        ("dm857.m01", "dm857.m04", "dm857.m11", "dm857.m12"),
        CoverageStatus.COVERED,
        "Foundations, functions, abstract data types, and object-oriented modelling provide "
        "explicit model-to-program practice and assessment.",
    ),
    OfficialRequirement(
        "dm857.sdu.lo02",
        OfficialRequirementKind.LEARNING_OUTCOME,
        "Devise a program structure based on the model.",
        ("dm857.m04", "dm857.m06", "dm857.m07", "dm857.m11", "dm857.m12"),
        CoverageStatus.COVERED,
        "Functions, sequences, mappings, ADTs, and classes require decomposition into coherent "
        "program structures.",
    ),
    OfficialRequirement(
        "dm857.sdu.lo03",
        OfficialRequirementKind.LEARNING_OUTCOME,
        "Implement the planned program in the concrete programming language used.",
        _ALL_MODULE_IDS,
        CoverageStatus.COVERED,
        "Every module uses Python implementations, worked examples, practice exercises, and "
        "authored assessments.",
    ),
    OfficialRequirement(
        "dm857.sdu.lo04",
        OfficialRequirementKind.LEARNING_OUTCOME,
        "Find and use adequate elements in the program library belonging to the language.",
        ("dm857.m05", "dm857.m06", "dm857.m07", "dm857.m08", "dm857.m13"),
        CoverageStatus.COVERED,
        "Core container and text APIs culminate in a dedicated scientific-libraries module.",
    ),
    OfficialRequirement(
        "dm857.sdu.lo05",
        OfficialRequirementKind.LEARNING_OUTCOME,
        "Plan and execute a testing of the program.",
        ("dm857.m10", "dm857.m14"),
        CoverageStatus.COVERED,
        "Tree invariants and the dedicated testing, debugging, and quality module provide explicit "
        "test-design and execution evidence.",
    ),
    OfficialRequirement(
        "dm857.sdu.lo06",
        OfficialRequirementKind.LEARNING_OUTCOME,
        "Design and implement recursive solutions of problems.",
        ("dm857.m09", "dm857.m10"),
        CoverageStatus.COVERED,
        "The recursion module teaches recursive reasoning directly and the tree module applies it "
        "to recursive data structures and traversals.",
    ),
    OfficialRequirement(
        "dm857.sdu.lo07",
        OfficialRequirementKind.LEARNING_OUTCOME,
        "Design and implement abstract data types.",
        ("dm857.m11", "dm857.m12"),
        CoverageStatus.COVERED,
        "The ADT module covers contracts and representations; the OOP module implements those "
        "abstractions with classes and encapsulation.",
    ),
    OfficialRequirement(
        "dm857.sdu.lo08",
        OfficialRequirementKind.LEARNING_OUTCOME,
        "Use basic tree structures and algorithms for these.",
        ("dm857.m10",),
        CoverageStatus.COVERED,
        "A dedicated tree module covers representations, traversals, search, metrics, complexity, "
        "invariants, and testing.",
    ),
    OfficialRequirement(
        "dm857.sdu.ct01",
        OfficialRequirementKind.CONTENT_TOPIC,
        "Sequence, repetition, conditional instruction, and subprogram.",
        ("dm857.m01", "dm857.m02", "dm857.m03", "dm857.m04"),
        CoverageStatus.COVERED,
        "The first four modules map one-to-one to the official basic structuring tools.",
    ),
    OfficialRequirement(
        "dm857.sdu.ct02",
        OfficialRequirementKind.CONTENT_TOPIC,
        "Fundamental data structures such as lists, maps, and trees.",
        ("dm857.m06", "dm857.m07", "dm857.m10"),
        CoverageStatus.COVERED,
        "Sequences, mappings and sets, and trees provide dedicated conceptual and practical coverage.",
    ),
    OfficialRequirement(
        "dm857.sdu.ct03",
        OfficialRequirementKind.CONTENT_TOPIC,
        "Structured programming techniques, including examples and applications.",
        ("dm857.m01", "dm857.m04", "dm857.m08", "dm857.m14"),
        CoverageStatus.COVERED,
        "The course repeatedly applies decomposition, explicit control flow, error handling, and "
        "testable program organization.",
    ),
    OfficialRequirement(
        "dm857.sdu.ct04",
        OfficialRequirementKind.CONTENT_TOPIC,
        "Recursion and recursive data structures.",
        ("dm857.m09", "dm857.m10"),
        CoverageStatus.COVERED,
        "Recursion is taught directly and then applied to trees as recursive structures.",
    ),
    OfficialRequirement(
        "dm857.sdu.ct05",
        OfficialRequirementKind.CONTENT_TOPIC,
        "Examples of abstract data types and their realization.",
        ("dm857.m11", "dm857.m12"),
        CoverageStatus.COVERED,
        "ADTs are specified through contracts and realized through concrete representations and classes.",
    ),
    OfficialRequirement(
        "dm857.sdu.exam01",
        OfficialRequirementKind.EXAM_COMPONENT,
        "Complete a group project and a written report of no more than 10 pages.",
        ("dm857.m04", "dm857.m08", "dm857.m11", "dm857.m12", "dm857.m14"),
        CoverageStatus.PARTIAL,
        "The application now provides a persistent five-milestone capstone with group metadata, "
        "repository and commit evidence, a ten-page report scaffold, and an explicitly internal "
        "weighted readiness rubric. It cannot yet validate work against the unavailable official "
        "itslearning project brief and assessment rubric.",
        "Import the official project brief and rubric when available, then add criterion-level "
        "artifact review, submission checks, and verified alignment without treating internal "
        "preparation aids as official assessment materials.",
    ),
    OfficialRequirement(
        "dm857.sdu.exam02",
        OfficialRequirementKind.EXAM_COMPONENT,
        "Give a group presentation of the project.",
        (),
        CoverageStatus.GAP,
        "The current application does not rehearse, time, record, or assess a collaborative project "
        "presentation.",
        "Add a presentation rehearsal workflow with role allocation, timing, slide checklist, and "
        "evidence-based group rubric.",
    ),
    OfficialRequirement(
        "dm857.sdu.exam03",
        OfficialRequirementKind.EXAM_COMPONENT,
        "Complete a short individual oral exam after the group presentation.",
        ("dm857.m10", "dm857.m11", "dm857.m12", "dm857.m14"),
        CoverageStatus.PARTIAL,
        "Authored oral-explanation activities exist, but there is no timed individual defense that "
        "samples the student's own project decisions and code.",
        "Add a timed oral-defense simulator that generates questions from the learner's capstone "
        "artifacts and scores reasoning with an explicit rubric.",
    ),
)


def _evidence_for(module_ids: tuple[str, ...]) -> CoverageEvidence:
    selected = tuple(bundle for bundle in BUNDLES if bundle.module.module_id in module_ids)
    return CoverageEvidence(
        module_count=len(selected),
        learning_objective_count=sum(len(bundle.module.objectives) for bundle in selected),
        practice_exercise_count=sum(len(bundle.module.practice_exercises) for bundle in selected),
        authored_assessment_count=sum(len(bundle.module.assessment_items) for bundle in selected),
        objective_bank_item_count=sum(len(bundle.objective_question_bank) for bundle in selected),
    )


def dm857_official_coverage_matrix() -> tuple[OfficialCoverageRow, ...]:
    """Return the official requirements joined to current authored evidence."""

    return tuple(
        OfficialCoverageRow(requirement=requirement, evidence=_evidence_for(requirement.module_ids))
        for requirement in OFFICIAL_DM857_REQUIREMENTS
    )


def dm857_official_coverage_summary() -> OfficialCoverageSummary:
    """Return aggregate coverage without disguising partial or missing exam components."""

    statuses = tuple(row.requirement.status for row in dm857_official_coverage_matrix())
    return OfficialCoverageSummary(
        requirement_count=len(statuses),
        covered_count=statuses.count(CoverageStatus.COVERED),
        partial_count=statuses.count(CoverageStatus.PARTIAL),
        gap_count=statuses.count(CoverageStatus.GAP),
    )


def validate_dm857_official_coverage() -> None:
    """Fail when the matrix drifts away from the authored catalog or official structure."""

    rows = dm857_official_coverage_matrix()
    requirement_ids = tuple(row.requirement.requirement_id for row in rows)
    if len(requirement_ids) != len(set(requirement_ids)):
        raise ValueError("The DM857 official matrix contains duplicate requirement IDs.")

    expected_module_ids = set(_ALL_MODULE_IDS)
    referenced_module_ids = {module_id for row in rows for module_id in row.requirement.module_ids}
    unknown_module_ids = referenced_module_ids - expected_module_ids
    if unknown_module_ids:
        raise ValueError(
            "The DM857 official matrix references unknown modules: "
            + ", ".join(sorted(unknown_module_ids))
        )

    expected_counts = {
        OfficialRequirementKind.LEARNING_OUTCOME: 8,
        OfficialRequirementKind.CONTENT_TOPIC: 5,
        OfficialRequirementKind.EXAM_COMPONENT: 3,
    }
    for kind, expected_count in expected_counts.items():
        actual_count = sum(row.requirement.kind is kind for row in rows)
        if actual_count != expected_count:
            raise ValueError(
                f"DM857 requires {expected_count} {kind.value} rows, found {actual_count}."
            )

    for row in rows:
        if row.requirement.module_ids and row.evidence.module_count != len(
            row.requirement.module_ids
        ):
            raise ValueError(
                f"Requirement {row.requirement.requirement_id!r} has incomplete module evidence."
            )
        if row.requirement.status is CoverageStatus.COVERED:
            if row.evidence.practice_exercise_count == 0:
                raise ValueError(
                    f"Covered requirement {row.requirement.requirement_id!r} lacks practice evidence."
                )
            if row.evidence.authored_assessment_count + row.evidence.objective_bank_item_count == 0:
                raise ValueError(
                    f"Covered requirement {row.requirement.requirement_id!r} lacks assessment evidence."
                )


validate_dm857_official_coverage()

__all__ = [
    "CoverageEvidence",
    "CoverageStatus",
    "DM857_ODIN_APPROVAL_DATE",
    "DM857_ODIN_AUDIT_DATE",
    "DM857_ODIN_SOURCE_URL",
    "DM857_ODIN_VERSION",
    "OFFICIAL_DM857_REQUIREMENTS",
    "OfficialCoverageRow",
    "OfficialCoverageSummary",
    "OfficialRequirement",
    "OfficialRequirementKind",
    "dm857_official_coverage_matrix",
    "dm857_official_coverage_summary",
    "validate_dm857_official_coverage",
]
