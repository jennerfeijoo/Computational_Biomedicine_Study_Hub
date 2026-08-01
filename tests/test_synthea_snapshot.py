"""Tests for deterministic local Synthea CSV snapshot inspection."""

from __future__ import annotations

import csv
import json
from pathlib import Path

from computational_biomedicine_study_hub.datasets.synthea_cli import main
from computational_biomedicine_study_hub.datasets.synthea_snapshot import (
    IssueSeverity,
    inspect_synthea_csv_directory,
)


def _write_csv(path: Path, columns: tuple[str, ...], rows: tuple[tuple[str, ...], ...]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.writer(handle, lineterminator="\n")
        writer.writerow(columns)
        writer.writerows(rows)


def _valid_snapshot(root: Path) -> None:
    _write_csv(
        root / "patients.csv",
        ("Id", "BIRTHDATE", "GENDER", "CITY"),
        (
            ("P01", "1980-01-01", "F", "Boston"),
            ("P02", "1970-06-12", "M", "Cambridge"),
        ),
    )
    _write_csv(
        root / "encounters.csv",
        (
            "Id",
            "START",
            "STOP",
            "PATIENT",
            "ENCOUNTERCLASS",
            "CODE",
            "DESCRIPTION",
        ),
        (
            ("E01", "2025-01-01", "2025-01-01", "P01", "ambulatory", "185349003", "Encounter"),
            ("E02", "2025-02-01", "2025-02-01", "P02", "wellness", "162673000", "Checkup"),
        ),
    )
    _write_csv(
        root / "conditions.csv",
        ("START", "PATIENT", "ENCOUNTER", "CODE", "DESCRIPTION"),
        (("2025-01-01", "P01", "E01", "44054006", "Diabetes mellitus type 2"),),
    )
    _write_csv(
        root / "observations.csv",
        ("DATE", "PATIENT", "ENCOUNTER", "CODE", "DESCRIPTION", "VALUE", "UNITS", "TYPE"),
        (
            ("2025-01-01", "P01", "E01", "39156-5", "Body Mass Index", "24.1", "kg/m2", "numeric"),
            ("2025-02-01", "P02", "E02", "8480-6", "Systolic Blood Pressure", "125", "mm[Hg]", "numeric"),
        ),
    )


def test_valid_snapshot_builds_deterministic_manifest(tmp_path: Path) -> None:
    first = tmp_path / "first"
    second = tmp_path / "second"
    _valid_snapshot(first)
    _valid_snapshot(second)

    first_report = inspect_synthea_csv_directory(first, source_label="teaching-copy-a")
    second_report = inspect_synthea_csv_directory(second, source_label="teaching-copy-b")

    assert first_report.valid
    assert not first_report.issues
    assert len(first_report.tables) == 4
    assert tuple(table.row_count for table in first_report.tables) == (2, 2, 1, 2)
    assert first_report.fingerprint == second_report.fingerprint
    assert first_report.manifest_payload()["synthetic_data"] is True
    assert "not real-patient or omics evidence" in first_report.to_json()


def test_duplicate_primary_key_and_orphan_patient_are_errors(tmp_path: Path) -> None:
    _valid_snapshot(tmp_path)
    _write_csv(
        tmp_path / "patients.csv",
        ("Id", "BIRTHDATE", "GENDER"),
        (
            ("P01", "1980-01-01", "F"),
            ("P01", "1990-01-01", "M"),
        ),
    )
    _write_csv(
        tmp_path / "encounters.csv",
        (
            "Id",
            "START",
            "STOP",
            "PATIENT",
            "ENCOUNTERCLASS",
            "CODE",
            "DESCRIPTION",
        ),
        (("E01", "2025-01-01", "2025-01-01", "P99", "ambulatory", "1", "Encounter"),),
    )

    report = inspect_synthea_csv_directory(tmp_path)
    error_codes = {
        issue.code for issue in report.issues if issue.severity is IssueSeverity.ERROR
    }

    assert not report.valid
    assert "duplicate-primary-key" in error_codes
    assert "orphan-patient-reference" in error_codes


def test_missing_file_and_required_columns_are_reported(tmp_path: Path) -> None:
    _valid_snapshot(tmp_path)
    (tmp_path / "observations.csv").unlink()
    _write_csv(
        tmp_path / "conditions.csv",
        ("START", "PATIENT", "CODE"),
        (("2025-01-01", "P01", "44054006"),),
    )

    report = inspect_synthea_csv_directory(tmp_path)
    issues = {(issue.code, issue.filename): issue for issue in report.issues}

    assert not report.valid
    assert ("missing-file", "observations.csv") in issues
    assert ("missing-columns", "conditions.csv") in issues
    assert issues[("missing-columns", "conditions.csv")].count == 2


def test_blank_encounter_reference_is_warning_not_error(tmp_path: Path) -> None:
    _valid_snapshot(tmp_path)
    _write_csv(
        tmp_path / "observations.csv",
        ("DATE", "PATIENT", "ENCOUNTER", "CODE", "DESCRIPTION", "VALUE", "UNITS", "TYPE"),
        (("2025-01-01", "P01", "", "39156-5", "Body Mass Index", "24.1", "kg/m2", "numeric"),),
    )

    report = inspect_synthea_csv_directory(tmp_path)

    assert report.valid
    assert len(report.issues) == 1
    assert report.issues[0].code == "blank-encounter-reference"
    assert report.issues[0].severity is IssueSeverity.WARNING


def test_cli_writes_manifest_and_returns_validation_status(
    tmp_path: Path,
    capsys: object,
) -> None:
    del capsys
    snapshot = tmp_path / "snapshot"
    manifest = tmp_path / "artifacts" / "synthea-manifest.json"
    _valid_snapshot(snapshot)

    assert main([str(snapshot), "--manifest", str(manifest), "--source-label", "unit-test"]) == 0
    payload = json.loads(manifest.read_text(encoding="utf-8"))
    assert payload["valid"] is True
    assert payload["source_label"] == "unit-test"
    assert len(payload["fingerprint"]) == 64

    (snapshot / "patients.csv").unlink()
    assert main([str(snapshot)]) == 2


def test_non_directory_is_invalid_and_still_has_fingerprint(tmp_path: Path) -> None:
    report = inspect_synthea_csv_directory(tmp_path / "missing")

    assert not report.valid
    assert report.issues[0].code == "root-not-directory"
    assert len(report.fingerprint) == 64
