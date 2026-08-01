"""Versioned learner-owned state for the BMB831 individual English report."""

from __future__ import annotations

import json
from dataclasses import dataclass, replace
from datetime import UTC, datetime
from typing import cast

BMB831_REPORT_SCHEMA_VERSION = 1


class BMB831ReportSnapshotError(ValueError):
    """Raised when persisted BMB831 report state is malformed."""


@dataclass(frozen=True, slots=True)
class ReportSectionSpec:
    """Stable report section and its internal preparation checklist."""

    section_id: str
    english_title: str
    checklist: tuple[str, ...]

    def __post_init__(self) -> None:
        if not self.section_id.startswith("bmb831.report."):
            raise ValueError("BMB831 report section IDs require the stable course prefix.")
        if not self.english_title.strip() or not self.checklist:
            raise ValueError("BMB831 report sections require title and checklist items.")
        if len(self.checklist) != len(set(self.checklist)):
            raise ValueError("BMB831 report checklist items cannot be duplicated.")


BMB831_REPORT_SECTIONS: tuple[ReportSectionSpec, ...] = (
    ReportSectionSpec(
        "bmb831.report.question",
        "Research question and estimand",
        (
            "State the biological question and analytical population.",
            "Define the estimand, comparison, time point, and unit of analysis.",
            "Separate exploratory and confirmatory aims.",
        ),
    ),
    ReportSectionSpec(
        "bmb831.report.data",
        "Data, provenance, and design",
        (
            "Identify the public source and exact local snapshot.",
            "Describe samples, features, metadata, exclusions, and technical factors.",
            "Reference checksums, versions, and the dataset card.",
        ),
    ),
    ReportSectionSpec(
        "bmb831.report.methods",
        "Methods and statistical design",
        (
            "Explain preprocessing, model, contrast, and multiplicity control.",
            "State assumptions and why the input scale matches the method.",
            "Describe validation or sensitivity analyses.",
        ),
    ),
    ReportSectionSpec(
        "bmb831.report.qc",
        "Quality control and preprocessing",
        (
            "Report sample and feature quality checks.",
            "Justify filtering, normalization, transformation, and missing-data decisions.",
            "Document exclusions and analyses with and without influential observations.",
        ),
    ),
    ReportSectionSpec(
        "bmb831.report.results",
        "Statistical results",
        (
            "Report effect size, uncertainty, adjusted evidence, and sample counts.",
            "Keep results aligned with the declared contrast and scale.",
            "Distinguish statistical evidence from practical relevance.",
        ),
    ),
    ReportSectionSpec(
        "bmb831.report.figures",
        "Figures and tables",
        (
            "Link every figure to a question and plotting-data artifact.",
            "Declare transformations, selection rules, units, and uncertainty.",
            "Use accessible encodings and informative captions.",
        ),
    ),
    ReportSectionSpec(
        "bmb831.report.interpretation",
        "Biological interpretation",
        (
            "Describe identifier mapping, background universe, and enrichment method.",
            "Differentiate pathway association from mechanism or causality.",
            "Integrate protein or pathway evidence without circular reasoning.",
        ),
    ),
    ReportSectionSpec(
        "bmb831.report.limitations",
        "Limitations and generalisation",
        (
            "Discuss design, measurement, missingness, confounding, and multiplicity.",
            "State what population and conditions the results represent.",
            "Identify evidence required for replication or external validation.",
        ),
    ),
    ReportSectionSpec(
        "bmb831.report.reproducibility",
        "Reproducibility and data availability",
        (
            "List scripts, manifests, versions, session information, and derived artifacts.",
            "Explain how another analyst can regenerate tables and figures.",
            "Respect source licences and do not redistribute restricted files.",
        ),
    ),
    ReportSectionSpec(
        "bmb831.report.abstract",
        "Abstract",
        (
            "Summarise background, question, methods, main quantitative result, and limitation.",
            "Use values consistent with the results section.",
            "Avoid claims beyond the design or represented experiment.",
        ),
    ),
)

_SECTION_BY_ID = {section.section_id: section for section in BMB831_REPORT_SECTIONS}
if len(_SECTION_BY_ID) != len(BMB831_REPORT_SECTIONS):
    raise ValueError("BMB831 report section IDs must be unique.")


@dataclass(frozen=True, slots=True)
class ReportSectionDraft:
    """Learner-owned English prose for one stable report section."""

    section_id: str
    text: str = ""

    def __post_init__(self) -> None:
        if self.section_id not in _SECTION_BY_ID:
            raise ValueError(f"Unknown BMB831 report section {self.section_id!r}.")


@dataclass(frozen=True, slots=True)
class BMB831ReportSnapshot:
    """All report sections with stable order and one active section."""

    schema_version: int
    active_section_id: str
    drafts: tuple[ReportSectionDraft, ...]
    updated_at: datetime

    def __post_init__(self) -> None:
        if self.schema_version != BMB831_REPORT_SCHEMA_VERSION:
            raise ValueError("Unsupported BMB831 report schema version.")
        if self.active_section_id not in _SECTION_BY_ID:
            raise ValueError("Unknown active BMB831 report section.")
        if self.updated_at.tzinfo is None or self.updated_at.utcoffset() is None:
            raise ValueError("BMB831 report timestamps must be timezone-aware.")
        section_ids = tuple(draft.section_id for draft in self.drafts)
        expected = tuple(section.section_id for section in BMB831_REPORT_SECTIONS)
        if section_ids != expected:
            raise ValueError("BMB831 report drafts must preserve authored section order.")

    @classmethod
    def empty(cls, *, now: datetime | None = None) -> BMB831ReportSnapshot:
        """Create a validated empty report."""

        return cls(
            schema_version=BMB831_REPORT_SCHEMA_VERSION,
            active_section_id=BMB831_REPORT_SECTIONS[0].section_id,
            drafts=tuple(
                ReportSectionDraft(section.section_id) for section in BMB831_REPORT_SECTIONS
            ),
            updated_at=now or datetime.now(UTC),
        )

    def draft(self, section_id: str) -> ReportSectionDraft:
        """Return one report draft by stable section ID."""

        return next(draft for draft in self.drafts if draft.section_id == section_id)

    def with_active_section(
        self,
        section_id: str,
        *,
        now: datetime | None = None,
    ) -> BMB831ReportSnapshot:
        """Select one section without changing its prose."""

        if section_id not in _SECTION_BY_ID:
            raise ValueError(f"Unknown BMB831 report section {section_id!r}.")
        return replace(
            self,
            active_section_id=section_id,
            updated_at=now or datetime.now(UTC),
        )

    def with_text(
        self,
        section_id: str,
        text: str,
        *,
        now: datetime | None = None,
    ) -> BMB831ReportSnapshot:
        """Replace learner prose for one section."""

        if section_id not in _SECTION_BY_ID:
            raise ValueError(f"Unknown BMB831 report section {section_id!r}.")
        replacement = ReportSectionDraft(section_id=section_id, text=text)
        drafts = tuple(
            replacement if draft.section_id == section_id else draft for draft in self.drafts
        )
        return replace(self, drafts=drafts, updated_at=now or datetime.now(UTC))

    @property
    def total_word_count(self) -> int:
        """Return the deterministic whitespace-delimited report word count."""

        return sum(len(draft.text.split()) for draft in self.drafts)

    @property
    def completed_section_count(self) -> int:
        """Return sections containing learner prose."""

        return sum(bool(draft.text.strip()) for draft in self.drafts)

    def to_json(self) -> str:
        """Serialize report state to deterministic JSON."""

        payload: dict[str, object] = {
            "schema_version": self.schema_version,
            "active_section_id": self.active_section_id,
            "drafts": [
                {"section_id": draft.section_id, "text": draft.text} for draft in self.drafts
            ],
            "updated_at": self.updated_at.isoformat(),
        }
        return json.dumps(payload, ensure_ascii=False, sort_keys=True, separators=(",", ":"))

    @classmethod
    def from_json(cls, document: str) -> BMB831ReportSnapshot:
        """Parse and validate one persisted report document defensively."""

        try:
            decoded: object = json.loads(document)
            if not isinstance(decoded, dict):
                raise TypeError("BMB831 report root must be an object.")
            payload = cast(dict[str, object], decoded)
            raw_drafts = payload["drafts"]
            if not isinstance(raw_drafts, list):
                raise TypeError("BMB831 report drafts must be an array.")
            drafts: list[ReportSectionDraft] = []
            for raw in raw_drafts:
                if not isinstance(raw, dict):
                    raise TypeError("BMB831 report draft entries must be objects.")
                item = cast(dict[str, object], raw)
                drafts.append(
                    ReportSectionDraft(
                        section_id=_required_string(item, "section_id"),
                        text=_required_string(item, "text", allow_empty=True),
                    )
                )
            return cls(
                schema_version=_required_int(payload, "schema_version"),
                active_section_id=_required_string(payload, "active_section_id"),
                drafts=tuple(drafts),
                updated_at=datetime.fromisoformat(_required_string(payload, "updated_at")),
            )
        except (KeyError, TypeError, ValueError, json.JSONDecodeError) as exc:
            raise BMB831ReportSnapshotError("The persisted BMB831 report is invalid.") from exc


def report_section(section_id: str) -> ReportSectionSpec:
    """Return one authored report section."""

    try:
        return _SECTION_BY_ID[section_id]
    except KeyError as exc:
        raise ValueError(f"Unknown BMB831 report section {section_id!r}.") from exc


def _required_string(payload: dict[str, object], key: str, *, allow_empty: bool = False) -> str:
    value = payload[key]
    if not isinstance(value, str):
        raise TypeError(f"{key} must be a string.")
    if not allow_empty and not value.strip():
        raise ValueError(f"{key} cannot be empty.")
    return value


def _required_int(payload: dict[str, object], key: str) -> int:
    value = payload[key]
    if isinstance(value, bool) or not isinstance(value, int):
        raise TypeError(f"{key} must be an integer.")
    return value


__all__ = [
    "BMB831_REPORT_SCHEMA_VERSION",
    "BMB831_REPORT_SECTIONS",
    "BMB831ReportSnapshot",
    "BMB831ReportSnapshotError",
    "ReportSectionDraft",
    "ReportSectionSpec",
    "report_section",
]
