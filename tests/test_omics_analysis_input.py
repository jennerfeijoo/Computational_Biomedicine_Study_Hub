"""Tests for lineage-aware omics assay and metadata validation."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from computational_biomedicine_study_hub.datasets import (
    OmicsAnalysisSeverity,
    inspect_omics_analysis_input,
    public_omics_source,
)
from computational_biomedicine_study_hub.datasets.omics_analysis_cli import main


def _write_parent_manifest(
    root: Path,
    source_id: str,
    *,
    valid: bool = True,
    fingerprint: str = "a" * 64,
) -> None:
    source = public_omics_source(source_id)
    payload = {
        "schema_version": 1,
        "source_id": source.source_id,
        "access_identifier": source.access_identifier,
        "modality": source.modality.value,
        "valid": valid,
        "fingerprint": fingerprint,
    }
    (root / "sha256_manifest.json").write_text(
        json.dumps(payload, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )


def _write_analysis(
    root: Path,
    *,
    source_id: str = "bioconductor.airway",
    assay_text: str | None = None,
    metadata_text: str | None = None,
    allow_missing_values: bool = False,
    value_scale: str = "raw_counts",
    parent_valid: bool = True,
) -> None:
    root.mkdir(parents=True, exist_ok=True)
    _write_parent_manifest(root, source_id, valid=parent_valid)
    (root / "derived").mkdir(exist_ok=True)
    (root / "derived" / "assay.csv").write_text(
        assay_text
        or ("feature_id,S1,S2,S3\nENSG000001,10,11,12\nENSG000002,0,4,8\nENSG000003,5,5,5\n"),
        encoding="utf-8",
    )
    (root / "derived" / "samples.csv").write_text(
        metadata_text or ("sample_id,condition,batch\nS1,control,A\nS2,treated,A\nS3,treated,B\n"),
        encoding="utf-8",
    )
    plan = {
        "schema_version": 1,
        "source_id": source_id,
        "parent_snapshot_manifest": "sha256_manifest.json",
        "assay": {
            "path": "derived/assay.csv",
            "delimiter": "comma",
            "feature_id_column": "feature_id",
            "value_scale": value_scale,
            "allow_missing_values": allow_missing_values,
        },
        "sample_metadata": {
            "path": "derived/samples.csv",
            "delimiter": "comma",
            "sample_id_column": "sample_id",
        },
        "required_metadata_columns": ["condition", "batch"],
    }
    (root / "analysis_plan.json").write_text(
        json.dumps(plan, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )


def _codes(report: Any) -> set[str]:
    return {issue.code for issue in report.issues}


def test_valid_raw_count_input_profiles_lineage_matrix_and_metadata(tmp_path: Path) -> None:
    _write_analysis(tmp_path)

    report = inspect_omics_analysis_input(
        tmp_path,
        source_id="bioconductor.airway",
    )

    assert report.valid
    assert report.issues == ()
    assert report.parent_snapshot_fingerprint == "a" * 64
    assert report.sample_sets_match
    assert report.sample_order_matches
    assert report.assay is not None
    assert report.metadata is not None
    assert report.assay.sample_ids == ("S1", "S2", "S3")
    assert report.assay.feature_count == 3
    assert report.assay.value_count == 9
    assert report.assay.observed_value_count == 9
    assert report.assay.zero_value_count == 1
    assert report.assay.missing_fraction == 0.0
    assert report.metadata.row_count == 3
    assert report.metadata.columns == ("sample_id", "condition", "batch")
    assert len(report.fingerprint) == 64

    payload = report.manifest_payload()
    assert payload["schema_version"] == 1
    assert payload["source_id"] == "bioconductor.airway"
    assert payload["valid"] is True
    assert payload["sample_sets_match"] is True
    assert "normalization suitability" in str(payload["scientific_boundary"])


def test_analysis_fingerprint_is_independent_of_root_name(tmp_path: Path) -> None:
    first = tmp_path / "first"
    second = tmp_path / "second"
    _write_analysis(first)
    _write_analysis(second)

    first_report = inspect_omics_analysis_input(first, source_id="bioconductor.airway")
    second_report = inspect_omics_analysis_input(second, source_id="bioconductor.airway")

    assert first_report.valid and second_report.valid
    assert first_report.root_name != second_report.root_name
    assert first_report.fingerprint == second_report.fingerprint
    assert first_report.to_json() != second_report.to_json()


def test_sample_order_difference_warns_but_requires_id_join(tmp_path: Path) -> None:
    _write_analysis(
        tmp_path,
        metadata_text=("sample_id,condition,batch\nS3,treated,B\nS1,control,A\nS2,treated,A\n"),
    )

    report = inspect_omics_analysis_input(tmp_path, source_id="bioconductor.airway")

    assert report.valid
    assert report.sample_sets_match
    assert not report.sample_order_matches
    warning = next(issue for issue in report.issues if issue.code == "sample-order-differs")
    assert warning.severity is OmicsAnalysisSeverity.WARNING


def test_sample_set_mismatch_is_an_error(tmp_path: Path) -> None:
    _write_analysis(
        tmp_path,
        metadata_text=("sample_id,condition,batch\nS1,control,A\nS2,treated,A\nS4,treated,B\n"),
    )

    report = inspect_omics_analysis_input(tmp_path, source_id="bioconductor.airway")

    assert not report.valid
    assert not report.sample_sets_match
    assert _codes(report) >= {
        "assay-samples-missing-from-metadata",
        "metadata-samples-missing-from-assay",
    }


def test_missing_values_require_explicit_declaration(tmp_path: Path) -> None:
    assay = "feature_id,S1,S2,S3\nP001,10,,12\nP002,3,4,5\n"
    _write_analysis(tmp_path, assay_text=assay, allow_missing_values=False)

    rejected = inspect_omics_analysis_input(tmp_path, source_id="bioconductor.airway")
    assert not rejected.valid
    assert "unexpected-missing-assay-values" in _codes(rejected)

    _write_analysis(tmp_path, assay_text=assay, allow_missing_values=True)
    accepted = inspect_omics_analysis_input(tmp_path, source_id="bioconductor.airway")
    assert accepted.valid
    assert accepted.assay is not None
    assert accepted.assay.missing_value_count == 1
    assert "declared-missing-assay-values" in _codes(accepted)


def test_raw_count_scale_rejects_negative_and_fractional_values(tmp_path: Path) -> None:
    _write_analysis(
        tmp_path,
        assay_text=("feature_id,S1,S2,S3\nENSG1,10,-1,12\nENSG2,3.5,4,5\n"),
    )

    report = inspect_omics_analysis_input(tmp_path, source_id="bioconductor.airway")

    assert not report.valid
    assert _codes(report) >= {
        "negative-values-in-nonnegative-scale",
        "non-integer-raw-counts",
    }


def test_invalid_parent_snapshot_blocks_transition(tmp_path: Path) -> None:
    _write_analysis(tmp_path, parent_valid=False)

    report = inspect_omics_analysis_input(tmp_path, source_id="bioconductor.airway")

    assert not report.valid
    assert "parent-snapshot-not-valid" in _codes(report)


def test_cli_writes_transition_manifest(tmp_path: Path, capsys: Any) -> None:
    _write_analysis(tmp_path)
    manifest = tmp_path / "analysis_manifest.json"

    exit_code = main(
        (
            "bioconductor.airway",
            str(tmp_path),
            "--manifest",
            str(manifest),
        )
    )
    output = capsys.readouterr().out

    assert exit_code == 0
    assert "Omics analytical input: VALID" in output
    assert "Features: 3" in output
    assert "Samples: 3" in output
    assert "Sample sets match: TRUE" in output
    assert manifest.is_file()
    payload = json.loads(manifest.read_text(encoding="utf-8"))
    assert payload["valid"] is True
    assert payload["assay"]["feature_count"] == 3
