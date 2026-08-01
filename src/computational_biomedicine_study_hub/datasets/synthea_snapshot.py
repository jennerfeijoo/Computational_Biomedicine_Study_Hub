"""Inspect a local Synthea CSV snapshot without treating it as real-patient evidence."""

from __future__ import annotations

import csv
import hashlib
import json
from dataclasses import dataclass
from enum import StrEnum
from pathlib import Path
from typing import Final


@dataclass(frozen=True, slots=True)
class TableContract:
    """Minimum version-tolerant contract for one Synthea CSV table."""

    filename: str
    required_columns: tuple[str, ...]
    primary_key: str | None = None
    patient_foreign_key: str | None = None
    encounter_foreign_key: str | None = None

    def __post_init__(self) -> None:
        if not self.filename.endswith(".csv"):
            raise ValueError("Synthea table contracts require a .csv filename.")
        if not self.required_columns:
            raise ValueError("Synthea table contracts require at least one column.")
        if len(self.required_columns) != len(set(self.required_columns)):
            raise ValueError("Synthea table contracts cannot repeat required columns.")
        declared_columns = set(self.required_columns)
        for column in (
            self.primary_key,
            self.patient_foreign_key,
            self.encounter_foreign_key,
        ):
            if column is not None and column not in declared_columns:
                raise ValueError(f"Contract column {column!r} must appear in required_columns.")


SYNTHEA_CSV_CONTRACTS: Final[tuple[TableContract, ...]] = (
    TableContract(
        filename="patients.csv",
        required_columns=("Id", "BIRTHDATE", "GENDER"),
        primary_key="Id",
    ),
    TableContract(
        filename="encounters.csv",
        required_columns=(
            "Id",
            "START",
            "STOP",
            "PATIENT",
            "ENCOUNTERCLASS",
            "CODE",
            "DESCRIPTION",
        ),
        primary_key="Id",
        patient_foreign_key="PATIENT",
    ),
    TableContract(
        filename="conditions.csv",
        required_columns=("START", "PATIENT", "ENCOUNTER", "CODE", "DESCRIPTION"),
        patient_foreign_key="PATIENT",
        encounter_foreign_key="ENCOUNTER",
    ),
    TableContract(
        filename="observations.csv",
        required_columns=(
            "DATE",
            "PATIENT",
            "ENCOUNTER",
            "CODE",
            "DESCRIPTION",
            "VALUE",
            "UNITS",
            "TYPE",
        ),
        patient_foreign_key="PATIENT",
        encounter_foreign_key="ENCOUNTER",
    ),
)


class IssueSeverity(StrEnum):
    """Severity assigned to one snapshot-contract finding."""

    ERROR = "error"
    WARNING = "warning"


@dataclass(frozen=True, slots=True)
class SnapshotIssue:
    """One deterministic validation finding."""

    code: str
    severity: IssueSeverity
    message: str
    filename: str | None = None
    count: int = 1

    def __post_init__(self) -> None:
        if not self.code.strip() or not self.message.strip():
            raise ValueError("Snapshot issues require a code and message.")
        if self.count < 1:
            raise ValueError("Snapshot issue counts must be positive.")

    def as_dict(self) -> dict[str, object]:
        """Return a JSON-compatible representation."""

        return {
            "code": self.code,
            "severity": self.severity.value,
            "message": self.message,
            "filename": self.filename,
            "count": self.count,
        }


@dataclass(frozen=True, slots=True)
class TableProfile:
    """Reproducible structural profile for one CSV table."""

    filename: str
    byte_size: int
    sha256: str
    columns: tuple[str, ...]
    row_count: int
    duplicate_primary_keys: int = 0
    blank_primary_keys: int = 0
    blank_patient_references: int = 0
    orphan_patient_references: int = 0
    blank_encounter_references: int = 0
    orphan_encounter_references: int = 0

    def __post_init__(self) -> None:
        if self.byte_size < 0 or self.row_count < 0:
            raise ValueError("Table sizes and row counts cannot be negative.")
        if len(self.sha256) != 64:
            raise ValueError("Table profiles require a SHA-256 hex digest.")
        counts = (
            self.duplicate_primary_keys,
            self.blank_primary_keys,
            self.blank_patient_references,
            self.orphan_patient_references,
            self.blank_encounter_references,
            self.orphan_encounter_references,
        )
        if any(count < 0 for count in counts):
            raise ValueError("Table validation counts cannot be negative.")

    def as_dict(self) -> dict[str, object]:
        """Return a JSON-compatible representation."""

        return {
            "filename": self.filename,
            "byte_size": self.byte_size,
            "sha256": self.sha256,
            "columns": list(self.columns),
            "row_count": self.row_count,
            "duplicate_primary_keys": self.duplicate_primary_keys,
            "blank_primary_keys": self.blank_primary_keys,
            "blank_patient_references": self.blank_patient_references,
            "orphan_patient_references": self.orphan_patient_references,
            "blank_encounter_references": self.blank_encounter_references,
            "orphan_encounter_references": self.orphan_encounter_references,
        }


@dataclass(frozen=True, slots=True)
class SnapshotReport:
    """Complete local snapshot report with deterministic identity."""

    root_name: str
    source_label: str
    tables: tuple[TableProfile, ...]
    issues: tuple[SnapshotIssue, ...]
    source_format: str = "synthea-csv"
    synthetic_data: bool = True

    @property
    def valid(self) -> bool:
        """Return whether no error-severity findings were detected."""

        return not any(issue.severity is IssueSeverity.ERROR for issue in self.issues)

    def _identity_payload(self) -> dict[str, object]:
        return {
            "source_format": self.source_format,
            "synthetic_data": self.synthetic_data,
            "tables": [table.as_dict() for table in self.tables],
            "issues": [issue.as_dict() for issue in self.issues],
        }

    @property
    def fingerprint(self) -> str:
        """Return a path-independent fingerprint of content and validation findings."""

        canonical = json.dumps(
            self._identity_payload(),
            ensure_ascii=False,
            sort_keys=True,
            separators=(",", ":"),
        ).encode("utf-8")
        return hashlib.sha256(canonical).hexdigest()

    def manifest_payload(self) -> dict[str, object]:
        """Return the complete reproducibility manifest."""

        payload = self._identity_payload()
        payload.update(
            {
                "root_name": self.root_name,
                "source_label": self.source_label,
                "valid": self.valid,
                "fingerprint": self.fingerprint,
                "scientific_boundary": (
                    "Synthetic Synthea records support technical and methodological practice; "
                    "they are not real-patient or omics evidence."
                ),
            }
        )
        return payload

    def to_json(self, *, indent: int = 2) -> str:
        """Serialize the manifest using stable key ordering."""

        return json.dumps(
            self.manifest_payload(),
            ensure_ascii=False,
            sort_keys=True,
            indent=indent,
        )


@dataclass(frozen=True, slots=True)
class _TableScan:
    profile: TableProfile
    issues: tuple[SnapshotIssue, ...]
    primary_keys: frozenset[str]


def _sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        while chunk := handle.read(1024 * 1024):
            digest.update(chunk)
    return digest.hexdigest()


def _cell(row: dict[str, str | None], column: str) -> str:
    value = row.get(column)
    return "" if value is None else value.strip()


def _scan_table(
    path: Path,
    contract: TableContract,
    *,
    patient_ids: frozenset[str],
    encounter_ids: frozenset[str],
) -> _TableScan:
    issues: list[SnapshotIssue] = []
    primary_keys: set[str] = set()
    duplicate_primary_keys = 0
    blank_primary_keys = 0
    blank_patient_references = 0
    orphan_patient_references = 0
    blank_encounter_references = 0
    orphan_encounter_references = 0
    row_count = 0

    try:
        with path.open("r", encoding="utf-8-sig", newline="") as handle:
            reader = csv.DictReader(handle)
            columns = tuple(reader.fieldnames or ())
            missing_columns = tuple(
                column for column in contract.required_columns if column not in columns
            )
            if missing_columns:
                issues.append(
                    SnapshotIssue(
                        code="missing-columns",
                        severity=IssueSeverity.ERROR,
                        filename=contract.filename,
                        count=len(missing_columns),
                        message="Missing required columns: " + ", ".join(missing_columns),
                    )
                )
            if len(columns) != len(set(columns)):
                issues.append(
                    SnapshotIssue(
                        code="duplicate-header-columns",
                        severity=IssueSeverity.ERROR,
                        filename=contract.filename,
                        message="The CSV header contains duplicate column names.",
                    )
                )

            for row in reader:
                row_count += 1
                if contract.primary_key is not None and contract.primary_key in columns:
                    key = _cell(row, contract.primary_key)
                    if not key:
                        blank_primary_keys += 1
                    elif key in primary_keys:
                        duplicate_primary_keys += 1
                    else:
                        primary_keys.add(key)

                if (
                    contract.patient_foreign_key is not None
                    and contract.patient_foreign_key in columns
                ):
                    patient_reference = _cell(row, contract.patient_foreign_key)
                    if not patient_reference:
                        blank_patient_references += 1
                    elif patient_reference not in patient_ids:
                        orphan_patient_references += 1

                if (
                    contract.encounter_foreign_key is not None
                    and contract.encounter_foreign_key in columns
                ):
                    encounter_reference = _cell(row, contract.encounter_foreign_key)
                    if not encounter_reference:
                        blank_encounter_references += 1
                    elif encounter_reference not in encounter_ids:
                        orphan_encounter_references += 1
    except (OSError, csv.Error, UnicodeError) as error:
        columns = ()
        issues.append(
            SnapshotIssue(
                code="csv-read-error",
                severity=IssueSeverity.ERROR,
                filename=contract.filename,
                message=f"Could not read CSV content: {error}",
            )
        )

    if duplicate_primary_keys:
        issues.append(
            SnapshotIssue(
                code="duplicate-primary-key",
                severity=IssueSeverity.ERROR,
                filename=contract.filename,
                count=duplicate_primary_keys,
                message="Duplicate non-empty primary-key values were detected.",
            )
        )
    if blank_primary_keys:
        issues.append(
            SnapshotIssue(
                code="blank-primary-key",
                severity=IssueSeverity.ERROR,
                filename=contract.filename,
                count=blank_primary_keys,
                message="Rows with blank primary-key values were detected.",
            )
        )
    if blank_patient_references:
        issues.append(
            SnapshotIssue(
                code="blank-patient-reference",
                severity=IssueSeverity.ERROR,
                filename=contract.filename,
                count=blank_patient_references,
                message="Rows with blank patient foreign keys were detected.",
            )
        )
    if orphan_patient_references:
        issues.append(
            SnapshotIssue(
                code="orphan-patient-reference",
                severity=IssueSeverity.ERROR,
                filename=contract.filename,
                count=orphan_patient_references,
                message="Patient foreign keys absent from patients.csv were detected.",
            )
        )
    if blank_encounter_references:
        issues.append(
            SnapshotIssue(
                code="blank-encounter-reference",
                severity=IssueSeverity.WARNING,
                filename=contract.filename,
                count=blank_encounter_references,
                message=(
                    "Blank encounter references were detected. They may be valid for some event "
                    "types but must remain explicit in downstream analysis."
                ),
            )
        )
    if orphan_encounter_references:
        issues.append(
            SnapshotIssue(
                code="orphan-encounter-reference",
                severity=IssueSeverity.ERROR,
                filename=contract.filename,
                count=orphan_encounter_references,
                message="Encounter foreign keys absent from encounters.csv were detected.",
            )
        )

    profile = TableProfile(
        filename=contract.filename,
        byte_size=path.stat().st_size,
        sha256=_sha256_file(path),
        columns=columns,
        row_count=row_count,
        duplicate_primary_keys=duplicate_primary_keys,
        blank_primary_keys=blank_primary_keys,
        blank_patient_references=blank_patient_references,
        orphan_patient_references=orphan_patient_references,
        blank_encounter_references=blank_encounter_references,
        orphan_encounter_references=orphan_encounter_references,
    )
    return _TableScan(profile, tuple(issues), frozenset(primary_keys))


def inspect_synthea_csv_directory(
    root: Path | str,
    *,
    source_label: str = "local-synthea-csv-snapshot",
) -> SnapshotReport:
    """Inspect the four core Synthea CSV tables and build a deterministic manifest."""

    resolved_root = Path(root)
    if not source_label.strip():
        raise ValueError("source_label cannot be empty.")
    if not resolved_root.is_dir():
        return SnapshotReport(
            root_name=resolved_root.name or str(resolved_root),
            source_label=source_label,
            tables=(),
            issues=(
                SnapshotIssue(
                    code="root-not-directory",
                    severity=IssueSeverity.ERROR,
                    message=f"Snapshot directory does not exist: {resolved_root}",
                ),
            ),
        )

    profiles: list[TableProfile] = []
    issues: list[SnapshotIssue] = []
    patient_ids: frozenset[str] = frozenset()
    encounter_ids: frozenset[str] = frozenset()

    for contract in SYNTHEA_CSV_CONTRACTS:
        path = resolved_root / contract.filename
        if not path.is_file():
            issues.append(
                SnapshotIssue(
                    code="missing-file",
                    severity=IssueSeverity.ERROR,
                    filename=contract.filename,
                    message=f"Required Synthea table is missing: {contract.filename}",
                )
            )
            continue

        scan = _scan_table(
            path,
            contract,
            patient_ids=patient_ids,
            encounter_ids=encounter_ids,
        )
        profiles.append(scan.profile)
        issues.extend(scan.issues)
        if contract.filename == "patients.csv":
            patient_ids = scan.primary_keys
        elif contract.filename == "encounters.csv":
            encounter_ids = scan.primary_keys

    return SnapshotReport(
        root_name=resolved_root.name,
        source_label=source_label,
        tables=tuple(profiles),
        issues=tuple(issues),
    )


__all__ = [
    "SYNTHEA_CSV_CONTRACTS",
    "IssueSeverity",
    "SnapshotIssue",
    "SnapshotReport",
    "TableContract",
    "TableProfile",
    "inspect_synthea_csv_directory",
]
