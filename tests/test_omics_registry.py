"""Tests for the stable public omics source registry."""

from __future__ import annotations

import pytest

from computational_biomedicine_study_hub.datasets import (
    OmicsModality,
    PUBLIC_OMICS_SOURCES,
    public_omics_source,
)


def test_public_omics_registry_has_transcriptomics_and_proteomics_sources() -> None:
    assert tuple(source.source_id for source in PUBLIC_OMICS_SOURCES) == (
        "bioconductor.airway",
        "proteomexchange.pxd000001",
    )
    assert {source.modality for source in PUBLIC_OMICS_SOURCES} == {
        OmicsModality.BULK_RNA_SEQ,
        OmicsModality.LFQ_PROTEOMICS,
    }
    assert len({source.source_id for source in PUBLIC_OMICS_SOURCES}) == len(PUBLIC_OMICS_SOURCES)


def test_public_omics_sources_require_snapshot_evidence() -> None:
    for source in PUBLIC_OMICS_SOURCES:
        artifacts = set(source.required_local_artifacts)
        assert "sha256_manifest.json" in artifacts
        assert "dataset_card.md" in artifacts
        assert source.access_identifier.strip()
        assert source.landing_page.startswith("https://")
        assert "local" in source.scientific_boundary.casefold()


def test_public_omics_source_lookup_is_strict() -> None:
    assert public_omics_source("bioconductor.airway").access_identifier == "airway"
    assert public_omics_source("proteomexchange.pxd000001").access_identifier == "PXD000001"
    with pytest.raises(ValueError, match="Unknown public omics source"):
        public_omics_source("unknown")
