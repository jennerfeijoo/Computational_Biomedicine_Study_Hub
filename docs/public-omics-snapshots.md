# Public omics snapshot workflow

## Purpose

The repository registers two public teaching sources:

- `bioconductor.airway` for a bulk RNA-seq workflow;
- `proteomexchange.pxd000001` for a proteomics workflow.

A registry entry identifies a source and its scientific boundary. It is not a local dataset, does not prove that files were retrieved correctly, and does not determine the analytical unit automatically. The snapshot workflow converts a learner-selected local export into inspectable evidence before analysis.

The implementation is offline-first and deliberately does not:

- download remote files;
- install R or Bioconductor packages;
- infer sample identities from filenames;
- accept an accession alone as a reproducible analysis;
- treat a generated checksum as biological validation.

## Snapshot directory contract

Each local snapshot contains:

1. `snapshot_plan.json`;
2. the concrete files declared in that plan;
3. a generated `sha256_manifest.json` after successful inspection.

All declared paths use normalized POSIX-style relative paths. Absolute paths, `..`, backslashes, symbolic links, duplicate path assignments, missing files, and empty files are rejected.

Untracked local files produce a warning because they are not part of the reproducibility evidence. Warnings do not invalidate an otherwise complete snapshot.

## Plan schema

The plan is a UTF-8 JSON object with four required fields:

```json
{
  "source_id": "bioconductor.airway",
  "access_identifier": "airway",
  "retrieved_at": "2026-08-02",
  "artifact_paths": {
    "package_or_export_version.txt": [
      "metadata/package_or_export_version.txt"
    ],
    "counts_or_assay_snapshot": [
      "assay/counts.csv"
    ],
    "sample_metadata_snapshot": [
      "metadata/samples.csv"
    ],
    "feature_annotation_snapshot": [
      "metadata/features.csv"
    ],
    "dataset_card.md": [
      "dataset_card.md"
    ]
  }
}
```

`artifact_paths` maps a registry role to one or more concrete files. The generated role `sha256_manifest.json` must not be listed as input evidence.

The plan records retrieval identity, not data interpretation. The dataset card must still describe the analytical unit, experimental design, represented conditions, feature identifiers, preprocessing state, known limitations, and intended teaching use.

## Airway snapshot example

A minimal directory may be organized as:

```text
data/omics/airway/
├── snapshot_plan.json
├── dataset_card.md
├── assay/
│   └── counts.csv
└── metadata/
    ├── package_or_export_version.txt
    ├── samples.csv
    └── features.csv
```

Inspect and generate the manifest:

```bash
cb-omics-inspect bioconductor.airway data/omics/airway \
  --manifest data/omics/airway/sha256_manifest.json
```

The command validates source identity, required evidence roles, relative paths, file presence, non-empty content, and SHA-256 identities. It returns exit code `0` for a valid snapshot and `2` for an invalid snapshot.

## PXD000001 snapshot example

The proteomics contract preserves the distinction among project metadata, sample annotation, selected quantitative files, and precursor, peptide, protein, or protein-group mappings.

```json
{
  "source_id": "proteomexchange.pxd000001",
  "access_identifier": "PXD000001",
  "retrieved_at": "2026-08-02",
  "artifact_paths": {
    "project_metadata_snapshot": [
      "metadata/project.json"
    ],
    "selected_quantification_files": [
      "quantification/run_01.tsv",
      "quantification/run_02.tsv"
    ],
    "sample_annotation_snapshot": [
      "metadata/samples.tsv"
    ],
    "protein_or_precursor_mapping": [
      "metadata/peptide_protein_mapping.tsv"
    ],
    "dataset_card.md": [
      "dataset_card.md"
    ]
  }
}
```

Inspect and generate the manifest:

```bash
cb-omics-inspect proteomexchange.pxd000001 data/omics/pxd000001 \
  --manifest data/omics/pxd000001/sha256_manifest.json
```

The validator does not decide whether a run, sample, peptide, protein, or protein group is the correct inferential unit. That decision remains explicit in the dataset card and subsequent workflow.

## Generated manifest

The output contains:

- schema version;
- stable source ID and accession;
- modality and source metadata from the registry;
- plan filename and SHA-256;
- retrieval date;
- required roles;
- sorted artifact roles, relative paths, byte sizes, and SHA-256 values;
- warnings and errors;
- a path-independent fingerprint;
- the registered scientific boundary.

The fingerprint excludes the directory name, so identical snapshots copied to different local roots retain the same evidence identity. The complete JSON manifest includes `root_name` for local traceability.

## Recommended workflow boundary

Use the validator before writing an analytical script or notebook:

1. select and retrieve files manually or through a separately reviewed acquisition process;
2. create the dataset card and explicit plan;
3. inspect the snapshot and resolve all errors;
4. preserve the generated manifest with the analysis;
5. build an assay-specific analytical object without changing the source files;
6. report every derived artifact separately.

This stage establishes reproducible local identity. It does not yet perform RNA-seq normalization, differential modelling, proteomics missingness handling, protein inference, enrichment, or biological interpretation.
