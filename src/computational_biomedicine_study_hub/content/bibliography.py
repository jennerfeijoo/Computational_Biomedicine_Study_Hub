"""Structured bibliographic evidence for authored academic content.

The registry records which source and locator were used to verify a concept. It does
not embed copyrighted textbook text. Visible learning content remains independently
authored and can be reviewed without requiring the source files at runtime.
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import StrEnum


class EvidenceStatus(StrEnum):
    """Review state for one source-to-content relation."""

    VERIFIED = "verified"
    PARTIAL = "partial"
    PENDING = "pending"


@dataclass(frozen=True, slots=True)
class BibliographicSource:
    """One stable bibliographic source known to the Study Hub."""

    source_id: str
    authors: tuple[str, ...]
    title: str
    edition: str
    year: int
    publisher: str
    source_kind: str = "textbook"

    def __post_init__(self) -> None:
        required = {
            "source_id": self.source_id,
            "title": self.title,
            "edition": self.edition,
            "publisher": self.publisher,
            "source_kind": self.source_kind,
        }
        for field_name, value in required.items():
            if not value.strip():
                raise ValueError(f"Bibliographic source field {field_name!r} cannot be empty.")
        if self.source_id != self.source_id.strip():
            raise ValueError("Bibliographic source IDs cannot contain surrounding whitespace.")
        if not self.authors or any(not author.strip() for author in self.authors):
            raise ValueError(f"Bibliographic source {self.source_id!r} requires authors.")
        if self.year < 1900:
            raise ValueError(f"Bibliographic source {self.source_id!r} has an invalid year.")


@dataclass(frozen=True, slots=True)
class ContentEvidence:
    """One auditable link from authored content to a source location."""

    evidence_id: str
    course_code: str
    module_id: str
    content_ids: tuple[str, ...]
    source_id: str
    locator: str
    supported_scope: str
    status: EvidenceStatus
    review_note: str = ""

    def __post_init__(self) -> None:
        required = {
            "evidence_id": self.evidence_id,
            "course_code": self.course_code,
            "module_id": self.module_id,
            "source_id": self.source_id,
            "locator": self.locator,
            "supported_scope": self.supported_scope,
        }
        for field_name, value in required.items():
            if not value.strip():
                raise ValueError(f"Content evidence field {field_name!r} cannot be empty.")
        if self.evidence_id != self.evidence_id.strip():
            raise ValueError("Evidence IDs cannot contain surrounding whitespace.")
        if not self.content_ids or any(not content_id.strip() for content_id in self.content_ids):
            raise ValueError(f"Evidence {self.evidence_id!r} requires content IDs.")
        if len(self.content_ids) != len(set(self.content_ids)):
            raise ValueError(f"Evidence {self.evidence_id!r} contains duplicate content IDs.")


TEXTBOOK_CATALOG: tuple[BibliographicSource, ...] = (
    BibliographicSource(
        source_id="guttag-python-3e-2021",
        authors=("John V. Guttag",),
        title="Introduction to Computation and Programming Using Python",
        edition="3rd edition",
        year=2021,
        publisher="The MIT Press",
    ),
    BibliographicSource(
        source_id="downey-think-python-3e-2024",
        authors=("Allen B. Downey",),
        title="Think Python: How to Think Like a Computer Scientist",
        edition="3rd edition",
        year=2024,
        publisher="O'Reilly Media",
    ),
    BibliographicSource(
        source_id="compeau-pevzner-v1-2e-2015",
        authors=("Phillip Compeau", "Pavel Pevzner"),
        title="Bioinformatics Algorithms: An Active Learning Approach, Volume 1",
        edition="2nd edition",
        year=2015,
        publisher="Active Learning Publishers",
    ),
    BibliographicSource(
        source_id="compeau-pevzner-v2-2e-2015",
        authors=("Phillip Compeau", "Pavel Pevzner"),
        title="Bioinformatics Algorithms: An Active Learning Approach, Volume 2",
        edition="2nd edition",
        year=2015,
        publisher="Active Learning Publishers",
    ),
    BibliographicSource(
        source_id="ims-2e-2024",
        authors=("Mine Çetinkaya-Rundel", "Johanna Hardin"),
        title="Introduction to Modern Statistics",
        edition="2nd edition",
        year=2024,
        publisher="OpenIntro",
    ),
    BibliographicSource(
        source_id="islr-2e-2021",
        authors=(
            "Gareth James",
            "Daniela Witten",
            "Trevor Hastie",
            "Robert Tibshirani",
        ),
        title="An Introduction to Statistical Learning with Applications in R",
        edition="2nd edition",
        year=2021,
        publisher="Springer",
    ),
    BibliographicSource(
        source_id="murphy-pml-2022",
        authors=("Kevin P. Murphy",),
        title="Probabilistic Machine Learning: An Introduction",
        edition="1st edition",
        year=2022,
        publisher="The MIT Press",
    ),
)

_SOURCE_BY_ID = {source.source_id: source for source in TEXTBOOK_CATALOG}
if len(_SOURCE_BY_ID) != len(TEXTBOOK_CATALOG):
    raise ValueError("Bibliographic source IDs must be unique.")


def source_by_id(source_id: str) -> BibliographicSource:
    """Return one registered source by stable ID."""

    try:
        return _SOURCE_BY_ID[source_id]
    except KeyError as error:
        raise KeyError(f"Unknown bibliographic source: {source_id!r}") from error


def validate_evidence_catalog(evidence: tuple[ContentEvidence, ...]) -> None:
    """Validate unique evidence IDs and registered source references."""

    evidence_ids = tuple(item.evidence_id for item in evidence)
    if len(evidence_ids) != len(set(evidence_ids)):
        raise ValueError("Content evidence IDs must be unique.")
    unknown_sources = sorted({item.source_id for item in evidence} - set(_SOURCE_BY_ID))
    if unknown_sources:
        raise ValueError(f"Content evidence references unknown sources: {unknown_sources}")


def evidence_for_module(
    evidence: tuple[ContentEvidence, ...],
    module_id: str,
) -> tuple[ContentEvidence, ...]:
    """Return all evidence records for one stable module ID."""

    return tuple(item for item in evidence if item.module_id == module_id)


__all__ = [
    "BibliographicSource",
    "ContentEvidence",
    "EvidenceStatus",
    "TEXTBOOK_CATALOG",
    "evidence_for_module",
    "source_by_id",
    "validate_evidence_catalog",
]
