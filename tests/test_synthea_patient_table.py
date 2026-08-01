"""Tests for leakage-aware Synthea patient analytical table derivation."""

from __future__ import annotations

import csv
import json
from pathlib import Path

import pytest

from computational_biomedicine_study_hub.datasets.synthea_patient_cli import main
from computational_biomedicine_study_hub.datasets.synthea_patient_table import (
    PATIENT_TABLE_COLUMNS,
    PatientTableBuildError,
    PatientTableConfig,
    build_synthea_patient_table,
)


def _write_csv(path: Path, columns: tuple[str, ...], rows: tuple[tuple[str, ...], ...]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.writer(handle, lineterminator="\n")
        writer.writerow(columns)
        writer.writerows(rows)


def _snapshot(root: Path) -> None:
    _write_csv(
        root / "patients.csv",
        ("Id", "BIRTHDATE", "GENDER", "CITY"),
        (
            ("P01", "1980-01-01", "F", "Boston"),
            ("P02", "1990-01-01", "M", "Cambridge"),
            ("P03", "1975-01-01", "F", "Boston"),
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
            ("E01", "2023-01-01", "2023-01-01", "P01", "ambulatory", "1", "Old"),
            ("E02", "2025-06-01", "2025-06-01", "P01", "ambulatory", "2", "Pre"),
            ("E03", "2025-07-01", "2025-07-01", "P01", "inpatient", "3", "Index"),
            ("E04", "2025-04-15", "2025-04-15", "P02", "wellness", "4", "Pre"),
            ("E05", "2025-05-01", "2025-05-01", "P02", "ambulatory", "5", "Index"),
        ),
    )
    _write_csv(
        root / "conditions.csv",
        ("START", "PATIENT", "ENCOUNTER", "CODE", "DESCRIPTION"),
        (
            ("2025-06-15", "P01", "E02", "C1", "Pre-index condition"),
            ("2025-07-01", "P01", "E03", "C2", "Index-day condition"),
            ("2024-01-01", "P02", "E04", "C0", "Outside window"),
            ("2025-04-20", "P02", "E04", "C3", "Pre-index condition"),
        ),
    )
    _write_csv(
        root / "observations.csv",
        ("DATE", "PATIENT", "ENCOUNTER", "CODE", "DESCRIPTION", "VALUE", "UNITS", "TYPE"),
        (
            ("2025-06-01", "P01", "E02", "39156-5", "Body Mass Index", "24.0", "kg/m2", "numeric"),
            ("2025-06-20", "P01", "E02", "39156-5", "Body Mass Index", "25.50", "kg/m2", "numeric"),
            (
                "2025-06-25",
                "P01",
                "E02",
                "8480-6",
                "Systolic Blood Pressure",
                "120",
                "mm[Hg]",
                "numeric",
            ),
            (
                "2025-07-01",
                "P01",
                "E03",
                "8462-4",
                "Diastolic Blood Pressure",
                "80",
                "mm[Hg]",
                "numeric",
            ),
            ("2025-06-25", "P01", "E02", "X", "Qualitative finding", "positive", "", "text"),
            (
                "2025-04-20",
                "P02",
                "E04",
                "8462-4",
                "Diastolic Blood Pressure",
                "70",
                "mm[Hg]",
                "numeric",
            ),
            ("2025-05-01", "P02", "E05", "39156-5", "Body Mass Index", "30", "kg/m2", "numeric"),
        ),
    )


def _read_rows(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def test_patient_table_uses_strict_pre_index_window_and_one_row_per_patient(
    tmp_path: Path,
) -> None:
    snapshot = tmp_path / "snapshot"
    output = tmp_path / "artifacts" / "patients.csv"
    _snapshot(snapshot)

    report = build_synthea_patient_table(snapshot, output)
    rows = _read_rows(output)
    by_patient = {row["patient_id"]: row for row in rows}

    assert report.row_count == 2
    assert report.excluded_without_index == 1
    assert tuple(rows[0]) == PATIENT_TABLE_COLUMNS
    assert set(by_patient) == {"P01", "P02"}

    p01 = by_patient["P01"]
    assert p01["index_date"] == "2025-07-01"
    assert p01["feature_window_start"] == "2024-07-01"
    assert p01["feature_window_end_exclusive"] == "2025-07-01"
    assert p01["age_at_index_years"] == "45"
    assert p01["encounter_count_pre_index"] == "1"
    assert p01["condition_event_count_pre_index"] == "1"
    assert p01["observation_count_pre_index"] == "4"
    assert p01["numeric_observation_count_pre_index"] == "3"
    assert p01["latest_bmi_date"] == "2025-06-20"
    assert p01["latest_bmi_value"] == "25.5"
    assert p01["latest_systolic_bp_value"] == "120"
    assert p01["latest_diastolic_bp_value"] == ""
    assert p01["split"] in {"train", "validation", "test"}

    p02 = by_patient["P02"]
    assert p02["encounter_count_pre_index"] == "1"
    assert p02["condition_event_count_pre_index"] == "1"
    assert p02["latest_diastolic_bp_value"] == "70"
    assert p02["latest_bmi_value"] == ""

    metadata = json.loads(output.with_suffix(".metadata.json").read_text(encoding="utf-8"))
    assert metadata["source_snapshot_fingerprint"] == report.source_snapshot_fingerprint
    assert metadata["output_sha256"] == report.output_sha256
    assert metadata["artifact_fingerprint"] == report.artifact_fingerprint
    assert metadata["synthetic_data"] is True
    assert "strictly before" in metadata["leakage_control"]


def test_patient_table_identity_is_path_independent(tmp_path: Path) -> None:
    first_snapshot = tmp_path / "first" / "snapshot"
    second_snapshot = tmp_path / "second" / "snapshot"
    first_output = tmp_path / "first" / "derived.csv"
    second_output = tmp_path / "second" / "derived.csv"
    _snapshot(first_snapshot)
    _snapshot(second_snapshot)

    first = build_synthea_patient_table(first_snapshot, first_output)
    second = build_synthea_patient_table(second_snapshot, second_output)

    assert first.source_snapshot_fingerprint == second.source_snapshot_fingerprint
    assert first.output_sha256 == second.output_sha256
    assert first.artifact_fingerprint == second.artifact_fingerprint
    assert first_output.read_bytes() == second_output.read_bytes()


def test_invalid_snapshot_is_rejected_before_output_is_written(tmp_path: Path) -> None:
    snapshot = tmp_path / "snapshot"
    output = tmp_path / "derived.csv"
    _snapshot(snapshot)
    _write_csv(
        snapshot / "patients.csv",
        ("Id", "BIRTHDATE", "GENDER"),
        (
            ("P01", "1980-01-01", "F"),
            ("P01", "1990-01-01", "M"),
        ),
    )

    with pytest.raises(PatientTableBuildError, match="duplicate-primary-key"):
        build_synthea_patient_table(snapshot, output)

    assert not output.exists()
    assert not output.with_suffix(".metadata.json").exists()


def test_invalid_clinical_date_is_reported_during_derivation(tmp_path: Path) -> None:
    snapshot = tmp_path / "snapshot"
    _snapshot(snapshot)
    _write_csv(
        snapshot / "encounters.csv",
        (
            "Id",
            "START",
            "STOP",
            "PATIENT",
            "ENCOUNTERCLASS",
            "CODE",
            "DESCRIPTION",
        ),
        (("E01", "not-a-date", "2025-01-01", "P01", "ambulatory", "1", "Encounter"),),
    )

    with pytest.raises(PatientTableBuildError, match="invalid START date"):
        build_synthea_patient_table(snapshot, tmp_path / "derived.csv")


def test_patient_table_configuration_rejects_invalid_boundaries() -> None:
    with pytest.raises(ValueError, match="at least one"):
        PatientTableConfig(window_days=0)
    with pytest.raises(ValueError, match="sum to 100"):
        PatientTableConfig(split_percentages=(80, 10, 5))
    with pytest.raises(ValueError, match="cannot be empty"):
        PatientTableConfig(split_salt=" ")


def test_patient_table_cli_writes_requested_artifacts(
    tmp_path: Path,
    capsys: pytest.CaptureFixture[str],
) -> None:
    snapshot = tmp_path / "snapshot"
    output = tmp_path / "derived" / "patient_table.csv"
    metadata = tmp_path / "derived" / "patient_table.json"
    _snapshot(snapshot)

    status = main(
        [
            str(snapshot),
            "--output",
            str(output),
            "--metadata",
            str(metadata),
            "--window-days",
            "180",
            "--train-percent",
            "60",
            "--validation-percent",
            "20",
            "--test-percent",
            "20",
            "--split-salt",
            "unit-test-salt",
        ]
    )

    captured = capsys.readouterr()
    assert status == 0
    assert "BUILT" in captured.out
    assert output.is_file()
    assert metadata.is_file()
    payload = json.loads(metadata.read_text(encoding="utf-8"))
    assert payload["config"]["window_days"] == 180
    assert payload["config"]["split_percentages"] == {
        "test": 20,
        "train": 60,
        "validation": 20,
    }

    invalid_status = main(
        [
            str(snapshot),
            "--output",
            str(tmp_path / "invalid.csv"),
            "--train-percent",
            "90",
            "--validation-percent",
            "20",
            "--test-percent",
            "0",
        ]
    )
    assert invalid_status == 2
