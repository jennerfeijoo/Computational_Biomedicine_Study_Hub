from computational_biomedicine_study_hub.datasets.omics_registry import (
    PUBLIC_OMICS_SOURCES,
    OmicsModality,
    public_omics_source,
)


def test_public_omics_registry_contains_real_rna_seq_paths() -> None:
    source_ids = {source.source_id for source in PUBLIC_OMICS_SOURCES}
    assert "bioconductor.airway" in source_ids
    assert "ncbi.geo.gse305298" in source_ids
    assert "ucsc.xena.tcga-target-gtex" in source_ids


def test_real_rna_seq_sources_have_reproducibility_contracts() -> None:
    for source in PUBLIC_OMICS_SOURCES:
        if source.modality is OmicsModality.BULK_RNA_SEQ:
            assert source.access_identifier
            assert source.landing_page.startswith("https://")
            assert "sha256_manifest.json" in source.required_local_artifacts
            assert "dataset_card.md" in source.required_local_artifacts
            assert source.scientific_boundary


def test_public_omics_lookup_is_stable() -> None:
    source = public_omics_source("ncbi.geo.gse305298")
    assert source.access_identifier == "GSE305298"
