"""Build a leakage-aware one-row-per-patient table from validated Synthea CSV files."""

from __future__ import annotations

import csv
import hashlib
import json
import tempfile
from dataclasses import dataclass, field
from datetime import date, timedelta
from decimal import Decimal, InvalidOperation
from pathlib import Path
from typing import Final

from .synthea_snapshot import inspect_synthea_csv_directory


PATIENT_TABLE_COLUMNS: Final[tuple[str, ...]] = (
    "patient_id",
    "birthdate",
    "gender",
    "index_date",
    "age_at_index_years",
    "feature_window_start",
    "feature_window_end_exclusive",
    "split",
    "encounter_count_pre_index",
    "unique_encounter_classes_pre_index",
    "condition_event_count_pre_index",
    "unique_condition_codes_pre_index",
    "observation_count_pre_index",
    "numeric_observation_count_pre_index",
    "latest_bmi_date",
    "latest_bmi_value",
    "latest_bmi_unit",
    "latest_systolic_bp_date",
    "latest_systolic_bp_value",
    "latest_systolic_bp_unit",
    "latest_diastolic_bp_date",
    "latest_diastolic_bp_value",
    "latest_diastolic_bp_unit",
)

_TARGET_OBSERVATION_CODES: Final[dict[str, str]] = {
    "39156-5": "bmi",
    "8480-6": "systolic_bp",
    "8462-4": "diastolic_bp",
}


class PatientTableBuildError(RuntimeError):
    """Raised when a reproducible patient table cannot be constructed."""


@dataclass(frozen=True, slots=True)
class PatientTableConfig:
    """Deterministic feature-window and patient-split configuration."""

    window_days: int = 365
    split_percentages: tuple[int, int, int] = (70, 15, 15)
    split_salt: str = "synthea-patient-table-v1"

    def __post_init__(self) -> None:
        if self.window_days < 1:
            raise ValueError("window_days must be at least one day.")
        if len(self.split_percentages) != 3:
            raise ValueError("split_percentages must contain train, validation, and test values.")
        if any(value < 0 for value in self.split_percentages):
            raise ValueError("split percentages cannot be negative.")
        if sum(self.split_percentages) != 100:
            raise ValueError("split percentages must sum to 100.")
        if not self.split_salt.strip():
            raise ValueError("split_salt cannot be empty.")

    @property
    def train_percent(self) -> int:
        return self.split_percentages[0]

    @property
    def validation_percent(self) -> int:
        return self.split_percentages[1]

    @property
    def test_percent(self) -> int:
        return self.split_percentages[2]

    def as_dict(self) -> dict[str, object]:
        """Return a JSON-compatible configuration payload."""

        return {
            "window_days": self.window_days,
            "split_percentages": {
                "train": self.train_percent,
                "validation": self.validation_percent,
                "test": self.test_percent,
            },
            "split_salt": self.split_salt,
            "index_definition": "latest encounter START per patient",
            "feature_window_definition": "[index_date - window_days, index_date)",
        }


@dataclass(frozen=True, slots=True)
class PatientTableReport:
    """Path-independent identity and local output details for one derived table."""

    source_snapshot_fingerprint: str
    output_filename: str
    output_sha256: str
    metadata_filename: str
    row_count: int
    columns: tuple[str, ...]
    excluded_without_index: int
    config: PatientTableConfig
    synthetic_data: bool = True

    def __post_init__(self) -> None:
        if len(self.source_snapshot_fingerprint) != 64 or len(self.output_sha256) != 64:
            raise ValueError("Patient-table reports require SHA-256 hex digests.")
        if self.row_count < 0 or self.excluded_without_index < 0:
            raise ValueError("Patient-table counts cannot be negative.")
        if not self.columns:
            raise ValueError("Patient-table reports require a non-empty column contract.")

    @property
    def artifact_fingerprint(self) -> str:
        """Return a path-independent identity for source, configuration, and output."""

        payload = {
            "source_snapshot_fingerprint": self.source_snapshot_fingerprint,
            "output_sha256": self.output_sha256,
            "row_count": self.row_count,
            "columns": list(self.columns),
            "excluded_without_index": self.excluded_without_index,
            "config": self.config.as_dict(),
            "synthetic_data": self.synthetic_data,
        }
        canonical = json.dumps(
            payload,
            ensure_ascii=False,
            sort_keys=True,
            separators=(",", ":"),
        ).encode("utf-8")
        return hashlib.sha256(canonical).hexdigest()

    def metadata_payload(self) -> dict[str, object]:
        """Return complete derived-artifact metadata."""

        return {
            "artifact_type": "synthea-patient-analytical-table",
            "artifact_version": 1,
            "synthetic_data": self.synthetic_data,
            "scientific_boundary": (
                "This table is derived from synthetic Synthea records for technical and "
                "methodological practice. It is not real-patient, epidemiological, clinical-utility, "
                "or omics evidence."
            ),
            "source_snapshot_fingerprint": self.source_snapshot_fingerprint,
            "output_filename": self.output_filename,
            "output_sha256": self.output_sha256,
            "metadata_filename": self.metadata_filename,
            "artifact_fingerprint": self.artifact_fingerprint,
            "row_count": self.row_count,
            "columns": list(self.columns),
            "excluded_without_index": self.excluded_without_index,
            "config": self.config.as_dict(),
            "leakage_control": (
                "All event-derived features use dates strictly before the patient-specific index "
                "date. Patient assignment to train, validation, or test is deterministic by patient ID."
            ),
        }

    def to_json(self, *, indent: int = 2) -> str:
        """Serialize metadata with stable key ordering."""

        return json.dumps(
            self.metadata_payload(),
            ensure_ascii=False,
            sort_keys=True,
            indent=indent,
        )


@dataclass(frozen=True, slots=True)
class _PatientDemographic:
    birthdate: date
    gender: str


@dataclass(slots=True)
class _LatestMetric:
    event_date: date | None = None
    row_number: int = 0
    value: str = ""
    unit: str = ""

    def consider(self, *, event_date: date, row_number: int, value: str, unit: str) -> None:
        current_key = (self.event_date or date.min, self.row_number)
        candidate_key = (event_date, row_number)
        if candidate_key > current_key:
            self.event_date = event_date
            self.row_number = row_number
            self.value = value
            self.unit = unit


@dataclass(slots=True)
class _PatientAggregate:
    demographic: _PatientDemographic
    index_date: date
    encounter_count: int = 0
    encounter_classes: set[str] = field(default_factory=set)
    condition_event_count: int = 0
    condition_codes: set[str] = field(default_factory=set)
    observation_count: int = 0
    numeric_observation_count: int = 0
    bmi: _LatestMetric = field(default_factory=_LatestMetric)
    systolic_bp: _LatestMetric = field(default_factory=_LatestMetric)
    diastolic_bp: _LatestMetric = field(default_factory=_LatestMetric)


@dataclass(frozen=True, slots=True)
class _BuildResult:
    rows: tuple[dict[str, str], ...]
    excluded_without_index: int


def _cell(row: dict[str, str | None], column: str) -> str:
    value = row.get(column)
    return "" if value is None else value.strip()


def _required_cell(
    row: dict[str, str | None],
    column: str,
    *,
    filename: str,
    row_number: int,
) -> str:
    value = _cell(row, column)
    if not value:
        raise PatientTableBuildError(
            f"{filename} row {row_number} has a blank required value in {column}."
        )
    return value


def _parse_date(
    raw_value: str,
    *,
    filename: str,
    row_number: int,
    column: str,
) -> date:
    value = raw_value.strip()
    try:
        return date.fromisoformat(value[:10])
    except ValueError as error:
        raise PatientTableBuildError(
            f"{filename} row {row_number} has an invalid {column} date: {raw_value!r}."
        ) from error


def _normalise_decimal(raw_value: str) -> str | None:
    try:
        numeric = Decimal(raw_value.strip())
    except InvalidOperation:
        return None
    if not numeric.is_finite():
        return None
    text = format(numeric, "f")
    if "." in text:
        text = text.rstrip("0").rstrip(".")
    return text or "0"


def _age_at_index(birthdate: date, index_date: date, *, patient_id: str) -> int:
    if birthdate > index_date:
        raise PatientTableBuildError(
            f"Patient {patient_id} has a birthdate after the derived index date."
        )
    return index_date.year - birthdate.year - (
        (index_date.month, index_date.day) < (birthdate.month, birthdate.day)
    )


def _split_for_patient(patient_id: str, config: PatientTableConfig) -> str:
    digest = hashlib.sha256(f"{config.split_salt}\0{patient_id}".encode()).digest()
    bucket = int.from_bytes(digest[:8], byteorder="big") % 100
    if bucket < config.train_percent:
        return "train"
    if bucket < config.train_percent + config.validation_percent:
        return "validation"
    return "test"


def _within_window(event_date: date, index_date: date, window_days: int) -> bool:
    return index_date - timedelta(days=window_days) <= event_date < index_date


def _load_patients(root: Path) -> dict[str, _PatientDemographic]:
    path = root / "patients.csv"
    patients: dict[str, _PatientDemographic] = {}
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        reader = csv.DictReader(handle)
        for row_number, row in enumerate(reader, start=2):
            patient_id = _required_cell(
                row,
                "Id",
                filename="patients.csv",
                row_number=row_number,
            )
            birthdate_raw = _required_cell(
                row,
                "BIRTHDATE",
                filename="patients.csv",
                row_number=row_number,
            )
            gender = _required_cell(
                row,
                "GENDER",
                filename="patients.csv",
                row_number=row_number,
            )
            patients[patient_id] = _PatientDemographic(
                birthdate=_parse_date(
                    birthdate_raw,
                    filename="patients.csv",
                    row_number=row_number,
                    column="BIRTHDATE",
                ),
                gender=gender,
            )
    return patients


def _derive_index_dates(root: Path) -> dict[str, date]:
    path = root / "encounters.csv"
    index_dates: dict[str, date] = {}
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        reader = csv.DictReader(handle)
        for row_number, row in enumerate(reader, start=2):
            patient_id = _required_cell(
                row,
                "PATIENT",
                filename="encounters.csv",
                row_number=row_number,
            )
            start_raw = _required_cell(
                row,
                "START",
                filename="encounters.csv",
                row_number=row_number,
            )
            encounter_date = _parse_date(
                start_raw,
                filename="encounters.csv",
                row_number=row_number,
                column="START",
            )
            previous = index_dates.get(patient_id)
            if previous is None or encounter_date > previous:
                index_dates[patient_id] = encounter_date
    return index_dates


def _initialise_aggregates(
    patients: dict[str, _PatientDemographic],
    index_dates: dict[str, date],
) -> dict[str, _PatientAggregate]:
    return {
        patient_id: _PatientAggregate(demographic=patients[patient_id], index_date=index_date)
        for patient_id, index_date in index_dates.items()
        if patient_id in patients
    }


def _aggregate_encounters(
    root: Path,
    aggregates: dict[str, _PatientAggregate],
    config: PatientTableConfig,
) -> None:
    path = root / "encounters.csv"
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        reader = csv.DictReader(handle)
        for row_number, row in enumerate(reader, start=2):
            patient_id = _required_cell(
                row,
                "PATIENT",
                filename="encounters.csv",
                row_number=row_number,
            )
            aggregate = aggregates.get(patient_id)
            if aggregate is None:
                continue
            event_date = _parse_date(
                _required_cell(
                    row,
                    "START",
                    filename="encounters.csv",
                    row_number=row_number,
                ),
                filename="encounters.csv",
                row_number=row_number,
                column="START",
            )
            if not _within_window(event_date, aggregate.index_date, config.window_days):
                continue
            aggregate.encounter_count += 1
            encounter_class = _cell(row, "ENCOUNTERCLASS")
            if encounter_class:
                aggregate.encounter_classes.add(encounter_class)


def _aggregate_conditions(
    root: Path,
    aggregates: dict[str, _PatientAggregate],
    config: PatientTableConfig,
) -> None:
    path = root / "conditions.csv"
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        reader = csv.DictReader(handle)
        for row_number, row in enumerate(reader, start=2):
            patient_id = _required_cell(
                row,
                "PATIENT",
                filename="conditions.csv",
                row_number=row_number,
            )
            aggregate = aggregates.get(patient_id)
            if aggregate is None:
                continue
            event_date = _parse_date(
                _required_cell(
                    row,
                    "START",
                    filename="conditions.csv",
                    row_number=row_number,
                ),
                filename="conditions.csv",
                row_number=row_number,
                column="START",
            )
            if not _within_window(event_date, aggregate.index_date, config.window_days):
                continue
            aggregate.condition_event_count += 1
            code = _cell(row, "CODE")
            if code:
                aggregate.condition_codes.add(code)


def _metric_for_name(aggregate: _PatientAggregate, name: str) -> _LatestMetric:
    if name == "bmi":
        return aggregate.bmi
    if name == "systolic_bp":
        return aggregate.systolic_bp
    if name == "diastolic_bp":
        return aggregate.diastolic_bp
    raise ValueError(f"Unknown target observation name: {name}")


def _aggregate_observations(
    root: Path,
    aggregates: dict[str, _PatientAggregate],
    config: PatientTableConfig,
) -> None:
    path = root / "observations.csv"
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        reader = csv.DictReader(handle)
        for row_number, row in enumerate(reader, start=2):
            patient_id = _required_cell(
                row,
                "PATIENT",
                filename="observations.csv",
                row_number=row_number,
            )
            aggregate = aggregates.get(patient_id)
            if aggregate is None:
                continue
            event_date = _parse_date(
                _required_cell(
                    row,
                    "DATE",
                    filename="observations.csv",
                    row_number=row_number,
                ),
                filename="observations.csv",
                row_number=row_number,
                column="DATE",
            )
            if not _within_window(event_date, aggregate.index_date, config.window_days):
                continue
            aggregate.observation_count += 1
            normalised_value = _normalise_decimal(_cell(row, "VALUE"))
            if normalised_value is None:
                continue
            aggregate.numeric_observation_count += 1
            target_name = _TARGET_OBSERVATION_CODES.get(_cell(row, "CODE"))
            if target_name is None:
                continue
            _metric_for_name(aggregate, target_name).consider(
                event_date=event_date,
                row_number=row_number,
                value=normalised_value,
                unit=_cell(row, "UNITS"),
            )


def _metric_columns(prefix: str, metric: _LatestMetric) -> dict[str, str]:
    return {
        f"latest_{prefix}_date": metric.event_date.isoformat() if metric.event_date else "",
        f"latest_{prefix}_value": metric.value,
        f"latest_{prefix}_unit": metric.unit,
    }


def _materialise_rows(
    aggregates: dict[str, _PatientAggregate],
    config: PatientTableConfig,
) -> tuple[dict[str, str], ...]:
    rows: list[dict[str, str]] = []
    for patient_id in sorted(aggregates):
        aggregate = aggregates[patient_id]
        age = _age_at_index(
            aggregate.demographic.birthdate,
            aggregate.index_date,
            patient_id=patient_id,
        )
        row = {
            "patient_id": patient_id,
            "birthdate": aggregate.demographic.birthdate.isoformat(),
            "gender": aggregate.demographic.gender,
            "index_date": aggregate.index_date.isoformat(),
            "age_at_index_years": str(age),
            "feature_window_start": (
                aggregate.index_date - timedelta(days=config.window_days)
            ).isoformat(),
            "feature_window_end_exclusive": aggregate.index_date.isoformat(),
            "split": _split_for_patient(patient_id, config),
            "encounter_count_pre_index": str(aggregate.encounter_count),
            "unique_encounter_classes_pre_index": str(len(aggregate.encounter_classes)),
            "condition_event_count_pre_index": str(aggregate.condition_event_count),
            "unique_condition_codes_pre_index": str(len(aggregate.condition_codes)),
            "observation_count_pre_index": str(aggregate.observation_count),
            "numeric_observation_count_pre_index": str(
                aggregate.numeric_observation_count
            ),
        }
        row.update(_metric_columns("bmi", aggregate.bmi))
        row.update(_metric_columns("systolic_bp", aggregate.systolic_bp))
        row.update(_metric_columns("diastolic_bp", aggregate.diastolic_bp))
        rows.append(row)
    return tuple(rows)


def _build_rows(root: Path, config: PatientTableConfig) -> _BuildResult:
    patients = _load_patients(root)
    index_dates = _derive_index_dates(root)
    aggregates = _initialise_aggregates(patients, index_dates)
    _aggregate_encounters(root, aggregates, config)
    _aggregate_conditions(root, aggregates, config)
    _aggregate_observations(root, aggregates, config)
    return _BuildResult(
        rows=_materialise_rows(aggregates, config),
        excluded_without_index=len(patients) - len(aggregates),
    )


def _write_csv_atomic(path: Path, rows: tuple[dict[str, str], ...]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary_path: Path | None = None
    try:
        with tempfile.NamedTemporaryFile(
            mode="w",
            encoding="utf-8",
            newline="",
            delete=False,
            dir=path.parent,
            prefix=f".{path.name}.",
            suffix=".tmp",
        ) as handle:
            temporary_path = Path(handle.name)
            writer = csv.DictWriter(
                handle,
                fieldnames=PATIENT_TABLE_COLUMNS,
                lineterminator="\n",
                extrasaction="raise",
            )
            writer.writeheader()
            writer.writerows(rows)
        temporary_path.replace(path)
    except OSError as error:
        if temporary_path is not None:
            temporary_path.unlink(missing_ok=True)
        raise PatientTableBuildError(f"Could not write analytical table: {error}") from error


def _write_text_atomic(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary_path: Path | None = None
    try:
        with tempfile.NamedTemporaryFile(
            mode="w",
            encoding="utf-8",
            newline="\n",
            delete=False,
            dir=path.parent,
            prefix=f".{path.name}.",
            suffix=".tmp",
        ) as handle:
            temporary_path = Path(handle.name)
            handle.write(content)
        temporary_path.replace(path)
    except OSError as error:
        if temporary_path is not None:
            temporary_path.unlink(missing_ok=True)
        raise PatientTableBuildError(f"Could not write metadata: {error}") from error


def _sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        while chunk := handle.read(1024 * 1024):
            digest.update(chunk)
    return digest.hexdigest()


def build_synthea_patient_table(
    root: Path | str,
    output_csv: Path | str,
    *,
    metadata_path: Path | str | None = None,
    config: PatientTableConfig | None = None,
    source_label: str = "local-synthea-csv-snapshot",
) -> PatientTableReport:
    """Validate a snapshot, derive pre-index patient features, and write audited artifacts."""

    resolved_root = Path(root)
    resolved_output = Path(output_csv)
    resolved_metadata = (
        Path(metadata_path)
        if metadata_path is not None
        else resolved_output.with_suffix(".metadata.json")
    )
    effective_config = config or PatientTableConfig()
    if resolved_output == resolved_metadata:
        raise ValueError("The CSV output and metadata paths must be different.")

    snapshot = inspect_synthea_csv_directory(resolved_root, source_label=source_label)
    if not snapshot.valid:
        error_codes = sorted(
            {issue.code for issue in snapshot.issues if issue.severity.value == "error"}
        )
        raise PatientTableBuildError(
            "Synthea snapshot validation failed before derivation: " + ", ".join(error_codes)
        )

    result = _build_rows(resolved_root, effective_config)
    _write_csv_atomic(resolved_output, result.rows)
    output_sha256 = _sha256_file(resolved_output)
    report = PatientTableReport(
        source_snapshot_fingerprint=snapshot.fingerprint,
        output_filename=resolved_output.name,
        output_sha256=output_sha256,
        metadata_filename=resolved_metadata.name,
        row_count=len(result.rows),
        columns=PATIENT_TABLE_COLUMNS,
        excluded_without_index=result.excluded_without_index,
        config=effective_config,
    )
    _write_text_atomic(resolved_metadata, report.to_json() + "\n")
    return report


__all__ = [
    "PATIENT_TABLE_COLUMNS",
    "PatientTableBuildError",
    "PatientTableConfig",
    "PatientTableReport",
    "build_synthea_patient_table",
]
