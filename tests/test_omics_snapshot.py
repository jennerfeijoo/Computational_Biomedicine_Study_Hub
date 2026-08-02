"""Tests for local public-omics snapshot validation and manifest generation."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from computational_biomedicine_study_hub.datasets import (
    GENERATED_OMICS_MANIFEST_ROLE,
    OmicsSnapshotSeverity,
    inspect_public_omics_snapshot,
    public_omics_source,
)
from computational_biomedicine_study_hub.datasets.omics_snapshot_cli import main


def _artifact_paths(source_id: str) -> dict[str, list[str]]:
    source = public_omics_source(source_id)
    return {
        role: [f"evidence/{index:02d}-{role.replace('/', '-')}.txt"]
        for index, role in enumerate(source.required_local_artifacts, start=1)
        if role != GENERATED_OMICS_MANIFEST_ROLE
    }


def _write_snapshot(
    root: Path,
    source_id: str,
    *,
    artifact_paths: dict[str, list[str]] | None = None,
    access_identifier: str | None = None,
    retrieved_at: str = "2026-08-02",
) -> dict[str, list[str]]:
    source = public_omics_source(source_id)
    declared = artifact_paths or _artifact_paths(source_id)
    root.mkdir(parents=True, exist_ok=True)
    for role, paths in declared.items():
        for relative_path in paths:
            if relative_path.startswith("../"):
                continue
            path = root / relative_path
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(f"role={role}\nsource={source_id}\n", encoding="utf-8")

    plan = {
        "source_id": source_id,
        "access_identifier": access_identifier or source.access_identifier,
        "retrieved_at": retrieved_at,
        "artifact_paths": declared,
    }
    (root / "snapshot_plan.json").write_text(
        json.dumps(plan, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    return declared


def _issue_codes(report: Any) -> set[str]:
    return {issue.code for issue in report.issues}


def test_valid_airway_snapshot_produces_stable_manifest() -> None:
    from tempfile import TemporaryDirectory

    with TemporaryDirectory() as directory:
        root = Path(directory) / "airway-snapshot"
        declared = _write_snapshot(root, "bioconductor.airway")

        report = inspect_public_omics_snapshot(
            root,
            source_id="bioconductor.airway",
        )

        assert report.valid
        assert report.issues == ()
        assert len(report.artifacts) == len(declared) == 5
        assert len(report.plan_sha256 or "") == 64
        assert len(report.fingerprint) == 64
        assert tuple((item.role, item.relative_path) for item in report.artifacts) == tuple(
            sorted((role, paths[0]) for role, paths in declared.items())
        )

        payload = report.manifest_payload()
        assert payload["schema_version"] == 1
        assert payload["source_id"] == "bioconductor.airway"
        assert payload["access_identifier"] == "airway"
        assert payload["modality"] == "bulk_rna_seq"
        assert payload["generated_manifest_role"] == "sha256_manifest.json"
        assert payload["valid"] is True
        assert "local analysis" in str(payload["scientific_boundary"])


def test_snapshot_fingerprint_is_independent_of_root_directory() -> None:
    from tempfile import TemporaryDirectory

    with TemporaryDirectory() as directory:
        root = Path(directory)
        first = root / "first"
        second = root / "second"
        _write_snapshot(first, "proteomexchange.pxd000001")
        _write_snapshot(second, "proteomexchange.pxd000001")

        first_report = inspect_public_omics_snapshot(
            first,
            source_id="proteomexchange.pxd000001",
        )
        second_report = inspect_public_omics_snapshot(
            second,
            source_id="proteomexchange.pxd000001",
        )

        assert first_report.valid and second_report.valid
        assert first_report.root_name != second_report.root_name
        assert first_report.fingerprint == second_report.fingerprint
        assert first_report.to_json() != second_report.to_json()


def test_missing_role_and_identity_mismatch_are_errors(tmp_path: Path) -> None:
    artifact_paths = _artifact_paths("bioconductor.airway")
    artifact_paths.pop("sample_metadata_snapshot")
    _write_snapshot(
        tmp_path,
        "bioconductor.airway",
        artifact_paths=artifact_paths,
        access_identifier="wrong-accession",
    )

    report = inspect_public_omics_snapshot(
        tmp_path,
        source_id="bioconductor.airway",
    )

    assert not report.valid
    assert _issue_codes(report) >= {
        "access-identifier-mismatch",
        "missing-artifact-roles",
    }
    assert all(
        issue.severity is OmicsSnapshotSeverity.ERROR
        for issue in report.issues
        if issue.code in {"access-identifier-mismatch", "missing-artifact-roles"}
    )


def test_unsafe_and_reused_artifact_paths_are_rejected(tmp_path: Path) -> None:
    artifact_paths = _artifact_paths("bioconductor.airway")
    shared_path = artifact_paths["counts_or_assay_snapshot"][0]
    artifact_paths["sample_metadata_snapshot"] = [shared_path]
    artifact_paths["feature_annotation_snapshot"] = ["../outside.txt"]
    _write_snapshot(
        tmp_path,
        "bioconductor.airway",
        artifact_paths=artifact_paths,
    )

    report = inspect_public_omics_snapshot(
        tmp_path,
        source_id="bioconductor.airway",
    )

    assert not report.valid
    assert _issue_codes(report) >= {
        "artifact-path-reused",
        "invalid-artifact-path",
    }


def test_untracked_local_file_is_warning_without_invalidating_snapshot(tmp_path: Path) -> None:
    _write_snapshot(tmp_path, "bioconductor.airway")
    (tmp_path / "notes.tmp").write_text("not part of the declared evidence\n", encoding="utf-8")

    report = inspect_public_omics_snapshot(
        tmp_path,
        source_id="bioconductor.airway",
    )

    assert report.valid
    warning = next(issue for issue in report.issues if issue.code == "untracked-local-files")
    assert warning.severity is OmicsSnapshotSeverity.WARNING
    assert warning.count == 1
    assert "notes.tmp" in warning.message


def test_cli_writes_manifest_and_returns_nonzero_for_unknown_source(
    tmp_path: Path,
    capsys: Any,
) -> None:
    _write_snapshot(tmp_path, "bioconductor.airway")
    manifest = tmp_path / "sha256_manifest.json"

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
    assert "Public omics snapshot: VALID" in output
    assert "Artifacts profiled: 5" in output
    assert manifest.is_file()
    payload = json.loads(manifest.read_text(encoding="utf-8"))
    assert payload["valid"] is True
    assert payload["fingerprint"]

    unknown_exit_code = main(("unknown.source", str(tmp_path)))
    unknown_output = capsys.readouterr().out
    assert unknown_exit_code == 2
    assert "Unknown public omics source" in unknown_output
