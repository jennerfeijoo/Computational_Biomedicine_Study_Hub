"""Stable public-source contracts for the BMB831 real-omics workflow.

The registry identifies public sources and the local artifacts a learner must retain.
It deliberately does not auto-download mutable remote content or claim a checksum
before a concrete local snapshot has been inspected.
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import StrEnum


class OmicsModality(StrEnum):
    """Supported real-data modalities in the BMB831 cumulative workflow."""

    BULK_RNA_SEQ = "bulk_rna_seq"
    LFQ_PROTEOMICS = "lfq_proteomics"


@dataclass(frozen=True, slots=True)
class PublicOmicsSource:
    """One stable source identity and its required local evidence contract."""

    source_id: str
    title: str
    modality: OmicsModality
    provider: str
    access_identifier: str
    landing_page: str
    expected_sample_unit: str
    required_local_artifacts: tuple[str, ...]
    scientific_boundary: str

    def __post_init__(self) -> None:
        required = (
            self.source_id,
            self.title,
            self.provider,
            self.access_identifier,
            self.landing_page,
            self.expected_sample_unit,
            self.scientific_boundary,
        )
        if any(not value.strip() for value in required):
            raise ValueError("Public omics source fields cannot be empty.")
        if not self.required_local_artifacts:
            raise ValueError("Public omics sources require local artifact expectations.")
        if len(self.required_local_artifacts) != len(set(self.required_local_artifacts)):
            raise ValueError("Public omics artifact expectations cannot contain duplicates.")


PUBLIC_OMICS_SOURCES: tuple[PublicOmicsSource, ...] = (
    PublicOmicsSource(
        source_id="bioconductor.airway",
        title="Airway smooth-muscle RNA-seq experiment",
        modality=OmicsModality.BULK_RNA_SEQ,
        provider="Bioconductor experiment data",
        access_identifier="airway",
        landing_page="https://bioconductor.org/packages/release/data/experiment/html/airway.html",
        expected_sample_unit="one RNA-seq library from one cell-line and treatment condition",
        required_local_artifacts=(
            "package_or_export_version.txt",
            "counts_or_assay_snapshot",
            "sample_metadata_snapshot",
            "feature_annotation_snapshot",
            "sha256_manifest.json",
            "dataset_card.md",
        ),
        scientific_boundary=(
            "The public package is a teaching dataset. A local analysis must record the exact "
            "package or export version, sample metadata, feature identifiers, and checksums. "
            "Results cannot be generalized beyond the represented experiment without external evidence."
        ),
    ),
    PublicOmicsSource(
        source_id="proteomexchange.pxd000001",
        title="ProteomeXchange reference project used by the rpx documentation",
        modality=OmicsModality.LFQ_PROTEOMICS,
        provider="ProteomeXchange through a repository-specific client such as rpx",
        access_identifier="PXD000001",
        landing_page="https://proteomecentral.proteomexchange.org/cgi/GetDataset?ID=PXD000001",
        expected_sample_unit="one mass-spectrometry run or biological sample declared by the project metadata",
        required_local_artifacts=(
            "project_metadata_snapshot",
            "selected_quantification_files",
            "sample_annotation_snapshot",
            "protein_or_precursor_mapping",
            "sha256_manifest.json",
            "dataset_card.md",
        ),
        scientific_boundary=(
            "ProteomeXchange projects may contain raw, identification, and processed files with "
            "different analytical units. The learner must select and document a coherent quantification "
            "level, verify sample identities, and retain exact local files; the accession alone is not an analysis."
        ),
    ),
)

_SOURCE_BY_ID = {source.source_id: source for source in PUBLIC_OMICS_SOURCES}
if len(_SOURCE_BY_ID) != len(PUBLIC_OMICS_SOURCES):
    raise ValueError("Public omics source IDs must be unique.")


def public_omics_source(source_id: str) -> PublicOmicsSource:
    """Return one registered public source by stable ID."""

    try:
        return _SOURCE_BY_ID[source_id]
    except KeyError as exc:
        raise ValueError(f"Unknown public omics source {source_id!r}.") from exc


__all__ = [
    "OmicsModality",
    "PUBLIC_OMICS_SOURCES",
    "PublicOmicsSource",
    "public_omics_source",
]
