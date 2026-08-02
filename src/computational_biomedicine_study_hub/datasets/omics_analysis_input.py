"""Validate lineage, assay orientation, and sample metadata before omics analysis.

This module begins where a valid public-omics snapshot manifest ends. It checks a
learner-authored analysis plan, links it to one immutable parent snapshot, profiles
a rectangular feature-by-sample assay, and verifies exact sample alignment with a
metadata table. It does not normalise, impute, model, or infer experimental design.
"""

from __future__ import annotations

import csv
import hashlib
import json
import math
from dataclasses import dataclass
from enum import StrEnum
from pathlib import Path, PurePosixPath
from typing import Final, cast

from .omics_registry import PublicOmicsSource, public_omics_source

DEFAULT_OMICS_ANALYSIS_PLAN_FILENAME: Final = "analysis_plan.json"
DEFAULT_OMICS_ANALYSIS_MANIFEST_FILENAME: Final = "analysis_manifest.json"


class OmicsAnalysisSeverity(StrEnum):
    """Severity assigned to one analytical-input finding."""

    ERROR = "error"
    WARNING = "warning"


class OmicsDelimiter(StrEnum):
    """Supported explicit delimiters for deterministic local tables."""

    COMMA = "comma"
    TAB = "tab"


class AssayValueScale(StrEnum):
    """Declared numerical scale used for structural value validation."""

    RAW_COUNTS = "raw_counts"
    NONNEGATIVE_CONTINUOUS = "nonnegative_continuous"
    REAL_CONTINUOUS = "real_continuous"


@dataclass(frozen=True, slots=True)
class OmicsAnalysisIssue:
    """One deterministic analytical-input finding."""

    code: str
    severity: OmicsAnalysisSeverity
    message: str
    relative_path: str | None = None
    column: str | None = None
    count: int = 1

    def __post_init__(self) -> None:
        if not self.code.strip() or not self.message.strip():
            raise ValueError("Omics analysis issues require a code and message.")
        if self.count < 1:
            raise ValueError("Omics analysis issue counts must be positive.")

    def as_dict(self) -> dict[str, object]:
        """Return a JSON-compatible representation."""

        return {
            "code": self.code,
            "severity": self.severity.value,
            "message": self.message,
            "relative_path": self.relative_path,
            "column": self.column,
            "count": self.count,
        }


@dataclass(frozen=True, slots=True)
class AssayMatrixProfile:
    """Structural and numerical profile of one feature-by-sample table."""

    relative_path: str
    sha256: str
    delimiter: OmicsDelimiter
    feature_id_column: str
    value_scale: AssayValueScale
    allow_missing_values: bool
    sample_ids: tuple[str, ...]
    feature_count: int
    value_count: int
    observed_value_count: int
    missing_value_count: int
    zero_value_count: int
    duplicate_feature_ids: int
    blank_feature_ids: int
    malformed_rows: int
    non_numeric_values: int
    non_finite_values: int
    negative_values: int
    non_integer_values: int

    def __post_init__(self) -> None:
        if not self.relative_path.strip() or len(self.sha256) != 64:
            raise ValueError("Assay profiles require a path and SHA-256 digest.")
        counts = (
            self.feature_count,
            self.value_count,
            self.observed_value_count,
            self.missing_value_count,
            self.zero_value_count,
            self.duplicate_feature_ids,
            self.blank_feature_ids,
            self.malformed_rows,
            self.non_numeric_values,
            self.non_finite_values,
            self.negative_values,
            self.non_integer_values,
        )
        if any(value < 0 for value in counts):
            raise ValueError("Assay profile counts cannot be negative.")

    @property
    def sample_count(self) -> int:
        """Return the number of sample columns in the assay."""

        return len(self.sample_ids)

    @property
    def missing_fraction(self) -> float:
        """Return the declared-cell fraction represented by empty values."""

        return 0.0 if self.value_count == 0 else self.missing_value_count / self.value_count

    @property
    def zero_fraction_observed(self) -> float:
        """Return the observed-value fraction equal to zero."""

        if self.observed_value_count == 0:
            return 0.0
        return self.zero_value_count / self.observed_value_count

    def as_dict(self) -> dict[str, object]:
        """Return a JSON-compatible representation."""

        return {
            "relative_path": self.relative_path,
            "sha256": self.sha256,
            "delimiter": self.delimiter.value,
            "feature_id_column": self.feature_id_column,
            "value_scale": self.value_scale.value,
            "allow_missing_values": self.allow_missing_values,
            "sample_ids": list(self.sample_ids),
            "sample_count": self.sample_count,
            "feature_count": self.feature_count,
            "value_count": self.value_count,
            "observed_value_count": self.observed_value_count,
            "missing_value_count": self.missing_value_count,
            "missing_fraction": self.missing_fraction,
            "zero_value_count": self.zero_value_count,
            "zero_fraction_observed": self.zero_fraction_observed,
            "duplicate_feature_ids": self.duplicate_feature_ids,
            "blank_feature_ids": self.blank_feature_ids,
            "malformed_rows": self.malformed_rows,
            "non_numeric_values": self.non_numeric_values,
            "non_finite_values": self.non_finite_values,
            "negative_values": self.negative_values,
            "non_integer_values": self.non_integer_values,
        }


@dataclass(frozen=True, slots=True)
class SampleMetadataProfile:
    """Structural profile of one row-per-sample metadata table."""

    relative_path: str
    sha256: str
    delimiter: OmicsDelimiter
    sample_id_column: str
    columns: tuple[str, ...]
    sample_ids: tuple[str, ...]
    row_count: int
    duplicate_sample_ids: int
    blank_sample_ids: int
    malformed_rows: int
    blank_required_cells: int

    def __post_init__(self) -> None:
        if not self.relative_path.strip() or len(self.sha256) != 64:
            raise ValueError("Metadata profiles require a path and SHA-256 digest.")
        counts = (
            self.row_count,
            self.duplicate_sample_ids,
            self.blank_sample_ids,
            self.malformed_rows,
            self.blank_required_cells,
        )
        if any(value < 0 for value in counts):
            raise ValueError("Metadata profile counts cannot be negative.")

    def as_dict(self) -> dict[str, object]:
        """Return a JSON-compatible representation."""

        return {
            "relative_path": self.relative_path,
            "sha256": self.sha256,
            "delimiter": self.delimiter.value,
            "sample_id_column": self.sample_id_column,
            "columns": list(self.columns),
            "sample_ids": list(self.sample_ids),
            "row_count": self.row_count,
            "duplicate_sample_ids": self.duplicate_sample_ids,
            "blank_sample_ids": self.blank_sample_ids,
            "malformed_rows": self.malformed_rows,
            "blank_required_cells": self.blank_required_cells,
        }


@dataclass(frozen=True, slots=True)
class OmicsAnalysisInputReport:
    """Complete lineage and structural report for one analytical input."""

    source: PublicOmicsSource
    root_name: str
    plan_filename: str
    plan_sha256: str | None
    parent_snapshot_manifest: str | None
    parent_manifest_sha256: str | None
    parent_snapshot_fingerprint: str | None
    required_metadata_columns: tuple[str, ...]
    assay: AssayMatrixProfile | None
    metadata: SampleMetadataProfile | None
    issues: tuple[OmicsAnalysisIssue, ...]

    @property
    def valid(self) -> bool:
        """Return whether no error-severity findings were detected."""

        return not any(issue.severity is OmicsAnalysisSeverity.ERROR for issue in self.issues)

    @property
    def sample_sets_match(self) -> bool:
        """Return whether assay and metadata contain exactly the same sample IDs."""

        if self.assay is None or self.metadata is None:
            return False
        return set(self.assay.sample_ids) == set(self.metadata.sample_ids)

    @property
    def sample_order_matches(self) -> bool:
        """Return whether assay and metadata sample IDs also share the same order."""

        if self.assay is None or self.metadata is None:
            return False
        return self.assay.sample_ids == self.metadata.sample_ids

    def _identity_payload(self) -> dict[str, object]:
        return {
            "schema_version": 1,
            "source_id": self.source.source_id,
            "access_identifier": self.source.access_identifier,
            "modality": self.source.modality.value,
            "plan_filename": self.plan_filename,
            "plan_sha256": self.plan_sha256,
            "parent_snapshot_manifest": self.parent_snapshot_manifest,
            "parent_manifest_sha256": self.parent_manifest_sha256,
            "parent_snapshot_fingerprint": self.parent_snapshot_fingerprint,
            "required_metadata_columns": list(self.required_metadata_columns),
            "assay": None if self.assay is None else self.assay.as_dict(),
            "metadata": None if self.metadata is None else self.metadata.as_dict(),
            "sample_sets_match": self.sample_sets_match,
            "sample_order_matches": self.sample_order_matches,
            "issues": [issue.as_dict() for issue in self.issues],
        }

    @property
    def fingerprint(self) -> str:
        """Return a root-independent identity for lineage, inputs, and findings."""

        canonical = json.dumps(
            self._identity_payload(),
            ensure_ascii=False,
            sort_keys=True,
            separators=(",", ":"),
        ).encode("utf-8")
        return hashlib.sha256(canonical).hexdigest()

    def manifest_payload(self) -> dict[str, object]:
        """Return the complete transition manifest."""

        payload = self._identity_payload()
        payload.update(
            {
                "root_name": self.root_name,
                "title": self.source.title,
                "provider": self.source.provider,
                "valid": self.valid,
                "fingerprint": self.fingerprint,
                "scientific_boundary": (
                    "This report validates declared lineage, table shape, identifiers, numeric "
                    "representation, and sample alignment. It does not establish biological "
                    "independence, experimental-design validity, normalization suitability, "
                    "missingness mechanism, model correctness, or external validity."
                ),
            }
        )
        return payload

    def to_json(self, *, indent: int = 2) -> str:
        """Serialize the transition manifest using stable key ordering."""

        return json.dumps(
            self.manifest_payload(),
            ensure_ascii=False,
            sort_keys=True,
            indent=indent,
        )


@dataclass(frozen=True, slots=True)
class _AssayConfig:
    relative_path: str
    delimiter: OmicsDelimiter
    feature_id_column: str
    value_scale: AssayValueScale
    allow_missing_values: bool


@dataclass(frozen=True, slots=True)
class _MetadataConfig:
    relative_path: str
    delimiter: OmicsDelimiter
    sample_id_column: str


def _sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        while chunk := handle.read(1024 * 1024):
            digest.update(chunk)
    return digest.hexdigest()


def _unique_json_object(pairs: list[tuple[str, object]]) -> dict[str, object]:
    result: dict[str, object] = {}
    for key, value in pairs:
        if key in result:
            raise ValueError(f"Duplicate JSON object key {key!r}.")
        result[key] = value
    return result


def _load_json_object(path: Path) -> dict[str, object]:
    text = path.read_text(encoding="utf-8-sig")
    raw = cast(object, json.loads(text, object_pairs_hook=_unique_json_object))
    if not isinstance(raw, dict) or not all(isinstance(key, str) for key in raw):
        raise ValueError("JSON root must be an object.")
    return cast(dict[str, object], raw)


def _normalise_relative_path(value: str) -> str:
    if not value or value.strip() != value:
        raise ValueError("Paths cannot be empty or padded with whitespace.")
    if "\\" in value:
        raise ValueError("Paths must use POSIX '/' separators.")
    path = PurePosixPath(value)
    if path.is_absolute() or ".." in path.parts:
        raise ValueError("Paths must remain inside the analysis directory.")
    normalised = path.as_posix()
    if normalised in {"", "."} or normalised != value:
        raise ValueError("Paths must be normalized relative POSIX paths.")
    return normalised


def _delimiter_character(delimiter: OmicsDelimiter) -> str:
    return "," if delimiter is OmicsDelimiter.COMMA else "\t"


def _string_value(mapping: dict[str, object], key: str) -> str | None:
    value = mapping.get(key)
    if isinstance(value, str) and value.strip():
        return value.strip()
    return None


def _enum_value[T: StrEnum](
    mapping: dict[str, object],
    key: str,
    enum_type: type[T],
) -> T | None:
    value = mapping.get(key)
    if not isinstance(value, str):
        return None
    try:
        return enum_type(value)
    except ValueError:
        return None


def _base_report(
    source: PublicOmicsSource,
    root: Path,
    plan_filename: str,
    issue: OmicsAnalysisIssue,
) -> OmicsAnalysisInputReport:
    return OmicsAnalysisInputReport(
        source=source,
        root_name=root.name or str(root),
        plan_filename=plan_filename,
        plan_sha256=None,
        parent_snapshot_manifest=None,
        parent_manifest_sha256=None,
        parent_snapshot_fingerprint=None,
        required_metadata_columns=(),
        assay=None,
        metadata=None,
        issues=(issue,),
    )


def _safe_file(
    root: Path,
    root_resolved: Path,
    relative_path: str,
    *,
    issues: list[OmicsAnalysisIssue],
    role: str,
) -> Path | None:
    path = root.joinpath(*PurePosixPath(relative_path).parts)
    try:
        path.resolve(strict=False).relative_to(root_resolved)
    except ValueError:
        issues.append(
            OmicsAnalysisIssue(
                code=f"{role}-path-escapes-root",
                severity=OmicsAnalysisSeverity.ERROR,
                message="Declared path resolves outside the analysis directory.",
                relative_path=relative_path,
            )
        )
        return None
    if path.is_symlink():
        issues.append(
            OmicsAnalysisIssue(
                code=f"{role}-is-symlink",
                severity=OmicsAnalysisSeverity.ERROR,
                message="Declared inputs must be regular local files, not symbolic links.",
                relative_path=relative_path,
            )
        )
        return None
    if not path.is_file():
        issues.append(
            OmicsAnalysisIssue(
                code=f"missing-{role}",
                severity=OmicsAnalysisSeverity.ERROR,
                message="Declared input file does not exist.",
                relative_path=relative_path,
            )
        )
        return None
    if path.stat().st_size == 0:
        issues.append(
            OmicsAnalysisIssue(
                code=f"empty-{role}",
                severity=OmicsAnalysisSeverity.ERROR,
                message="Declared input file is empty.",
                relative_path=relative_path,
            )
        )
        return None
    return path


def _parse_assay_config(
    plan: dict[str, object],
    issues: list[OmicsAnalysisIssue],
) -> _AssayConfig | None:
    raw = plan.get("assay")
    if not isinstance(raw, dict) or not all(isinstance(key, str) for key in raw):
        issues.append(
            OmicsAnalysisIssue(
                code="invalid-assay-config",
                severity=OmicsAnalysisSeverity.ERROR,
                message="assay must be a JSON object.",
            )
        )
        return None
    mapping = cast(dict[str, object], raw)
    path_value = _string_value(mapping, "path")
    feature_id_column = _string_value(mapping, "feature_id_column")
    delimiter = _enum_value(mapping, "delimiter", OmicsDelimiter)
    value_scale = _enum_value(mapping, "value_scale", AssayValueScale)
    allow_missing_values = mapping.get("allow_missing_values")
    unknown = tuple(
        sorted(
            set(mapping)
            - {
                "path",
                "delimiter",
                "feature_id_column",
                "value_scale",
                "allow_missing_values",
            }
        )
    )
    if unknown:
        issues.append(
            OmicsAnalysisIssue(
                code="unknown-assay-config-fields",
                severity=OmicsAnalysisSeverity.WARNING,
                count=len(unknown),
                message="Unrecognized assay config fields: " + ", ".join(unknown),
            )
        )
    if path_value is None or feature_id_column is None or delimiter is None or value_scale is None:
        issues.append(
            OmicsAnalysisIssue(
                code="incomplete-assay-config",
                severity=OmicsAnalysisSeverity.ERROR,
                message=(
                    "assay requires path, delimiter, feature_id_column, and value_scale using "
                    "supported string values."
                ),
            )
        )
        return None
    if not isinstance(allow_missing_values, bool):
        issues.append(
            OmicsAnalysisIssue(
                code="invalid-allow-missing-values",
                severity=OmicsAnalysisSeverity.ERROR,
                message="assay.allow_missing_values must be true or false.",
            )
        )
        return None
    try:
        relative_path = _normalise_relative_path(path_value)
    except ValueError as error:
        issues.append(
            OmicsAnalysisIssue(
                code="invalid-assay-path",
                severity=OmicsAnalysisSeverity.ERROR,
                message=str(error),
                relative_path=path_value,
            )
        )
        return None
    return _AssayConfig(
        relative_path=relative_path,
        delimiter=delimiter,
        feature_id_column=feature_id_column,
        value_scale=value_scale,
        allow_missing_values=allow_missing_values,
    )


def _parse_metadata_config(
    plan: dict[str, object],
    issues: list[OmicsAnalysisIssue],
) -> _MetadataConfig | None:
    raw = plan.get("sample_metadata")
    if not isinstance(raw, dict) or not all(isinstance(key, str) for key in raw):
        issues.append(
            OmicsAnalysisIssue(
                code="invalid-metadata-config",
                severity=OmicsAnalysisSeverity.ERROR,
                message="sample_metadata must be a JSON object.",
            )
        )
        return None
    mapping = cast(dict[str, object], raw)
    path_value = _string_value(mapping, "path")
    sample_id_column = _string_value(mapping, "sample_id_column")
    delimiter = _enum_value(mapping, "delimiter", OmicsDelimiter)
    unknown = tuple(sorted(set(mapping) - {"path", "delimiter", "sample_id_column"}))
    if unknown:
        issues.append(
            OmicsAnalysisIssue(
                code="unknown-metadata-config-fields",
                severity=OmicsAnalysisSeverity.WARNING,
                count=len(unknown),
                message="Unrecognized metadata config fields: " + ", ".join(unknown),
            )
        )
    if path_value is None or sample_id_column is None or delimiter is None:
        issues.append(
            OmicsAnalysisIssue(
                code="incomplete-metadata-config",
                severity=OmicsAnalysisSeverity.ERROR,
                message="sample_metadata requires path, delimiter, and sample_id_column.",
            )
        )
        return None
    try:
        relative_path = _normalise_relative_path(path_value)
    except ValueError as error:
        issues.append(
            OmicsAnalysisIssue(
                code="invalid-metadata-path",
                severity=OmicsAnalysisSeverity.ERROR,
                message=str(error),
                relative_path=path_value,
            )
        )
        return None
    return _MetadataConfig(
        relative_path=relative_path,
        delimiter=delimiter,
        sample_id_column=sample_id_column,
    )


def _parse_required_metadata_columns(
    plan: dict[str, object],
    issues: list[OmicsAnalysisIssue],
) -> tuple[str, ...]:
    raw = plan.get("required_metadata_columns")
    if not isinstance(raw, list) or not raw or not all(
        isinstance(value, str) and value.strip() == value and value for value in raw
    ):
        issues.append(
            OmicsAnalysisIssue(
                code="invalid-required-metadata-columns",
                severity=OmicsAnalysisSeverity.ERROR,
                message=(
                    "required_metadata_columns must be a non-empty list of unpadded column names."
                ),
            )
        )
        return ()
    columns = tuple(cast(list[str], raw))
    if len(columns) != len(set(columns)):
        issues.append(
            OmicsAnalysisIssue(
                code="duplicate-required-metadata-columns",
                severity=OmicsAnalysisSeverity.ERROR,
                message="required_metadata_columns cannot contain duplicates.",
            )
        )
    return columns


def _scan_assay(
    path: Path,
    config: _AssayConfig,
    issues: list[OmicsAnalysisIssue],
) -> AssayMatrixProfile | None:
    feature_ids: set[str] = set()
    sample_ids: tuple[str, ...] = ()
    feature_count = 0
    value_count = 0
    observed_value_count = 0
    missing_value_count = 0
    zero_value_count = 0
    duplicate_feature_ids = 0
    blank_feature_ids = 0
    malformed_rows = 0
    non_numeric_values = 0
    non_finite_values = 0
    negative_values = 0
    non_integer_values = 0

    try:
        with path.open("r", encoding="utf-8-sig", newline="") as handle:
            reader = csv.reader(handle, delimiter=_delimiter_character(config.delimiter))
            try:
                header = tuple(next(reader))
            except StopIteration:
                issues.append(
                    OmicsAnalysisIssue(
                        code="empty-assay-table",
                        severity=OmicsAnalysisSeverity.ERROR,
                        message="Assay table has no header.",
                        relative_path=config.relative_path,
                    )
                )
                return None

            if any(not column or column.strip() != column for column in header):
                issues.append(
                    OmicsAnalysisIssue(
                        code="invalid-assay-header",
                        severity=OmicsAnalysisSeverity.ERROR,
                        message="Assay header columns must be non-empty and unpadded.",
                        relative_path=config.relative_path,
                    )
                )
            if len(header) != len(set(header)):
                issues.append(
                    OmicsAnalysisIssue(
                        code="duplicate-assay-columns",
                        severity=OmicsAnalysisSeverity.ERROR,
                        message="Assay header contains duplicate columns.",
                        relative_path=config.relative_path,
                    )
                )
            if config.feature_id_column not in header:
                issues.append(
                    OmicsAnalysisIssue(
                        code="missing-feature-id-column",
                        severity=OmicsAnalysisSeverity.ERROR,
                        message="Declared feature_id_column is absent from the assay header.",
                        relative_path=config.relative_path,
                        column=config.feature_id_column,
                    )
                )
                return None

            feature_index = header.index(config.feature_id_column)
            sample_ids = tuple(
                column for index, column in enumerate(header) if index != feature_index
            )
            if not sample_ids:
                issues.append(
                    OmicsAnalysisIssue(
                        code="assay-has-no-samples",
                        severity=OmicsAnalysisSeverity.ERROR,
                        message="Assay table requires at least one sample column.",
                        relative_path=config.relative_path,
                    )
                )

            for row in reader:
                feature_count += 1
                if len(row) != len(header):
                    malformed_rows += 1
                    continue
                feature_id = row[feature_index]
                if not feature_id or feature_id.strip() != feature_id:
                    blank_feature_ids += 1
                elif feature_id in feature_ids:
                    duplicate_feature_ids += 1
                else:
                    feature_ids.add(feature_id)

                for index, raw_value in enumerate(row):
                    if index == feature_index:
                        continue
                    value_count += 1
                    value_text = raw_value.strip()
                    if not value_text:
                        missing_value_count += 1
                        continue
                    observed_value_count += 1
                    try:
                        value = float(value_text)
                    except ValueError:
                        non_numeric_values += 1
                        continue
                    if not math.isfinite(value):
                        non_finite_values += 1
                        continue
                    if value == 0:
                        zero_value_count += 1
                    if value < 0:
                        negative_values += 1
                    if config.value_scale is AssayValueScale.RAW_COUNTS and not value.is_integer():
                        non_integer_values += 1
    except (OSError, csv.Error, UnicodeError) as error:
        issues.append(
            OmicsAnalysisIssue(
                code="assay-read-error",
                severity=OmicsAnalysisSeverity.ERROR,
                message=f"Could not read assay table: {error}",
                relative_path=config.relative_path,
            )
        )
        return None

    if feature_count == 0:
        issues.append(
            OmicsAnalysisIssue(
                code="assay-has-no-features",
                severity=OmicsAnalysisSeverity.ERROR,
                message="Assay table contains no feature rows.",
                relative_path=config.relative_path,
            )
        )
    if malformed_rows:
        issues.append(
            OmicsAnalysisIssue(
                code="malformed-assay-rows",
                severity=OmicsAnalysisSeverity.ERROR,
                count=malformed_rows,
                message="Assay rows do not match the header width.",
                relative_path=config.relative_path,
            )
        )
    if blank_feature_ids:
        issues.append(
            OmicsAnalysisIssue(
                code="blank-or-padded-feature-ids",
                severity=OmicsAnalysisSeverity.ERROR,
                count=blank_feature_ids,
                message="Feature IDs must be non-empty and unpadded.",
                relative_path=config.relative_path,
                column=config.feature_id_column,
            )
        )
    if duplicate_feature_ids:
        issues.append(
            OmicsAnalysisIssue(
                code="duplicate-feature-ids",
                severity=OmicsAnalysisSeverity.ERROR,
                count=duplicate_feature_ids,
                message="Feature IDs must be unique at the declared analytical level.",
                relative_path=config.relative_path,
                column=config.feature_id_column,
            )
        )
    if missing_value_count and not config.allow_missing_values:
        issues.append(
            OmicsAnalysisIssue(
                code="unexpected-missing-assay-values",
                severity=OmicsAnalysisSeverity.ERROR,
                count=missing_value_count,
                message="Missing assay cells are present although allow_missing_values is false.",
                relative_path=config.relative_path,
            )
        )
    if missing_value_count and config.allow_missing_values:
        issues.append(
            OmicsAnalysisIssue(
                code="declared-missing-assay-values",
                severity=OmicsAnalysisSeverity.WARNING,
                count=missing_value_count,
                message=(
                    "Missing assay cells were retained by explicit plan declaration; their mechanism "
                    "and handling remain analytical decisions."
                ),
                relative_path=config.relative_path,
            )
        )
    for code, count, message in (
        ("non-numeric-assay-values", non_numeric_values, "Assay cells must be numeric or empty."),
        ("non-finite-assay-values", non_finite_values, "Assay cells cannot contain NaN or infinity."),
    ):
        if count:
            issues.append(
                OmicsAnalysisIssue(
                    code=code,
                    severity=OmicsAnalysisSeverity.ERROR,
                    count=count,
                    message=message,
                    relative_path=config.relative_path,
                )
            )
    if negative_values and config.value_scale is not AssayValueScale.REAL_CONTINUOUS:
        issues.append(
            OmicsAnalysisIssue(
                code="negative-values-in-nonnegative-scale",
                severity=OmicsAnalysisSeverity.ERROR,
                count=negative_values,
                message="Declared raw-count and nonnegative-continuous scales cannot be negative.",
                relative_path=config.relative_path,
            )
        )
    if non_integer_values:
        issues.append(
            OmicsAnalysisIssue(
                code="non-integer-raw-counts",
                severity=OmicsAnalysisSeverity.ERROR,
                count=non_integer_values,
                message="raw_counts requires integer-valued observed cells.",
                relative_path=config.relative_path,
            )
        )

    return AssayMatrixProfile(
        relative_path=config.relative_path,
        sha256=_sha256_file(path),
        delimiter=config.delimiter,
        feature_id_column=config.feature_id_column,
        value_scale=config.value_scale,
        allow_missing_values=config.allow_missing_values,
        sample_ids=sample_ids,
        feature_count=feature_count,
        value_count=value_count,
        observed_value_count=observed_value_count,
        missing_value_count=missing_value_count,
        zero_value_count=zero_value_count,
        duplicate_feature_ids=duplicate_feature_ids,
        blank_feature_ids=blank_feature_ids,
        malformed_rows=malformed_rows,
        non_numeric_values=non_numeric_values,
        non_finite_values=non_finite_values,
        negative_values=negative_values,
        non_integer_values=non_integer_values,
    )


def _scan_metadata(
    path: Path,
    config: _MetadataConfig,
    required_columns: tuple[str, ...],
    issues: list[OmicsAnalysisIssue],
) -> SampleMetadataProfile | None:
    sample_ids: list[str] = []
    seen_sample_ids: set[str] = set()
    row_count = 0
    duplicate_sample_ids = 0
    blank_sample_ids = 0
    malformed_rows = 0
    blank_required_cells = 0

    try:
        with path.open("r", encoding="utf-8-sig", newline="") as handle:
            reader = csv.reader(handle, delimiter=_delimiter_character(config.delimiter))
            try:
                header = tuple(next(reader))
            except StopIteration:
                issues.append(
                    OmicsAnalysisIssue(
                        code="empty-metadata-table",
                        severity=OmicsAnalysisSeverity.ERROR,
                        message="Metadata table has no header.",
                        relative_path=config.relative_path,
                    )
                )
                return None

            if any(not column or column.strip() != column for column in header):
                issues.append(
                    OmicsAnalysisIssue(
                        code="invalid-metadata-header",
                        severity=OmicsAnalysisSeverity.ERROR,
                        message="Metadata columns must be non-empty and unpadded.",
                        relative_path=config.relative_path,
                    )
                )
            if len(header) != len(set(header)):
                issues.append(
                    OmicsAnalysisIssue(
                        code="duplicate-metadata-columns",
                        severity=OmicsAnalysisSeverity.ERROR,
                        message="Metadata header contains duplicate columns.",
                        relative_path=config.relative_path,
                    )
                )
            if config.sample_id_column not in header:
                issues.append(
                    OmicsAnalysisIssue(
                        code="missing-sample-id-column",
                        severity=OmicsAnalysisSeverity.ERROR,
                        message="Declared sample_id_column is absent from metadata.",
                        relative_path=config.relative_path,
                        column=config.sample_id_column,
                    )
                )
                return None

            missing_required = tuple(column for column in required_columns if column not in header)
            if missing_required:
                issues.append(
                    OmicsAnalysisIssue(
                        code="missing-required-metadata-columns",
                        severity=OmicsAnalysisSeverity.ERROR,
                        count=len(missing_required),
                        message="Missing required metadata columns: " + ", ".join(missing_required),
                        relative_path=config.relative_path,
                    )
                )

            sample_index = header.index(config.sample_id_column)
            required_indices = tuple(header.index(column) for column in required_columns if column in header)
            for row in reader:
                row_count += 1
                if len(row) != len(header):
                    malformed_rows += 1
                    continue
                sample_id = row[sample_index]
                if not sample_id or sample_id.strip() != sample_id:
                    blank_sample_ids += 1
                else:
                    sample_ids.append(sample_id)
                    if sample_id in seen_sample_ids:
                        duplicate_sample_ids += 1
                    else:
                        seen_sample_ids.add(sample_id)
                blank_required_cells += sum(not row[index].strip() for index in required_indices)
    except (OSError, csv.Error, UnicodeError) as error:
        issues.append(
            OmicsAnalysisIssue(
                code="metadata-read-error",
                severity=OmicsAnalysisSeverity.ERROR,
                message=f"Could not read metadata table: {error}",
                relative_path=config.relative_path,
            )
        )
        return None

    if row_count == 0:
        issues.append(
            OmicsAnalysisIssue(
                code="metadata-has-no-samples",
                severity=OmicsAnalysisSeverity.ERROR,
                message="Metadata table contains no sample rows.",
                relative_path=config.relative_path,
            )
        )
    for code, count, message, column in (
        (
            "malformed-metadata-rows",
            malformed_rows,
            "Metadata rows do not match the header width.",
            None,
        ),
        (
            "blank-or-padded-sample-ids",
            blank_sample_ids,
            "Sample IDs must be non-empty and unpadded.",
            config.sample_id_column,
        ),
        (
            "duplicate-sample-ids",
            duplicate_sample_ids,
            "Metadata must contain exactly one row per sample ID.",
            config.sample_id_column,
        ),
        (
            "blank-required-metadata-cells",
            blank_required_cells,
            "Required metadata columns cannot contain blank cells.",
            None,
        ),
    ):
        if count:
            issues.append(
                OmicsAnalysisIssue(
                    code=code,
                    severity=OmicsAnalysisSeverity.ERROR,
                    count=count,
                    message=message,
                    relative_path=config.relative_path,
                    column=column,
                )
            )

    return SampleMetadataProfile(
        relative_path=config.relative_path,
        sha256=_sha256_file(path),
        delimiter=config.delimiter,
        sample_id_column=config.sample_id_column,
        columns=header,
        sample_ids=tuple(sample_ids),
        row_count=row_count,
        duplicate_sample_ids=duplicate_sample_ids,
        blank_sample_ids=blank_sample_ids,
        malformed_rows=malformed_rows,
        blank_required_cells=blank_required_cells,
    )


def inspect_omics_analysis_input(
    root: Path | str,
    *,
    source_id: str,
    plan_filename: str = DEFAULT_OMICS_ANALYSIS_PLAN_FILENAME,
) -> OmicsAnalysisInputReport:
    """Validate one assay/metadata transition linked to a valid snapshot manifest."""

    source = public_omics_source(source_id)
    resolved_root = Path(root)
    try:
        normalized_plan_filename = _normalise_relative_path(plan_filename)
    except ValueError as error:
        return _base_report(
            source,
            resolved_root,
            plan_filename,
            OmicsAnalysisIssue(
                code="invalid-analysis-plan-path",
                severity=OmicsAnalysisSeverity.ERROR,
                message=str(error),
                relative_path=plan_filename,
            ),
        )
    if not resolved_root.is_dir():
        return _base_report(
            source,
            resolved_root,
            normalized_plan_filename,
            OmicsAnalysisIssue(
                code="root-not-directory",
                severity=OmicsAnalysisSeverity.ERROR,
                message=f"Analysis directory does not exist: {resolved_root}",
            ),
        )

    root_resolved = resolved_root.resolve()
    plan_path = resolved_root.joinpath(*PurePosixPath(normalized_plan_filename).parts)
    if plan_path.is_symlink() or not plan_path.is_file():
        return _base_report(
            source,
            resolved_root,
            normalized_plan_filename,
            OmicsAnalysisIssue(
                code="missing-or-symlinked-analysis-plan",
                severity=OmicsAnalysisSeverity.ERROR,
                message="Analysis plan must be a regular local file.",
                relative_path=normalized_plan_filename,
            ),
        )

    try:
        plan = _load_json_object(plan_path)
    except (OSError, UnicodeError, json.JSONDecodeError, ValueError) as error:
        return _base_report(
            source,
            resolved_root,
            normalized_plan_filename,
            OmicsAnalysisIssue(
                code="invalid-analysis-plan-json",
                severity=OmicsAnalysisSeverity.ERROR,
                message=f"Could not read analysis plan: {error}",
                relative_path=normalized_plan_filename,
            ),
        )

    issues: list[OmicsAnalysisIssue] = []
    plan_sha256 = _sha256_file(plan_path)
    known_fields = {
        "schema_version",
        "source_id",
        "parent_snapshot_manifest",
        "assay",
        "sample_metadata",
        "required_metadata_columns",
    }
    unknown_fields = tuple(sorted(set(plan) - known_fields))
    if unknown_fields:
        issues.append(
            OmicsAnalysisIssue(
                code="unknown-analysis-plan-fields",
                severity=OmicsAnalysisSeverity.WARNING,
                count=len(unknown_fields),
                message="Unrecognized analysis plan fields: " + ", ".join(unknown_fields),
            )
        )
    if plan.get("schema_version") != 1:
        issues.append(
            OmicsAnalysisIssue(
                code="unsupported-analysis-schema-version",
                severity=OmicsAnalysisSeverity.ERROR,
                message="analysis_plan.json requires schema_version 1.",
            )
        )
    declared_source_id = _string_value(plan, "source_id")
    if declared_source_id != source.source_id:
        issues.append(
            OmicsAnalysisIssue(
                code="analysis-source-id-mismatch",
                severity=OmicsAnalysisSeverity.ERROR,
                message=(
                    f"Analysis source_id must be {source.source_id!r}; received {declared_source_id!r}."
                ),
            )
        )

    required_columns = _parse_required_metadata_columns(plan, issues)
    assay_config = _parse_assay_config(plan, issues)
    metadata_config = _parse_metadata_config(plan, issues)

    parent_snapshot_manifest: str | None = None
    parent_manifest_sha256: str | None = None
    parent_snapshot_fingerprint: str | None = None
    parent_value = _string_value(plan, "parent_snapshot_manifest")
    if parent_value is None:
        issues.append(
            OmicsAnalysisIssue(
                code="missing-parent-snapshot-manifest",
                severity=OmicsAnalysisSeverity.ERROR,
                message="Analysis plan requires parent_snapshot_manifest.",
            )
        )
    else:
        try:
            parent_snapshot_manifest = _normalise_relative_path(parent_value)
        except ValueError as error:
            issues.append(
                OmicsAnalysisIssue(
                    code="invalid-parent-manifest-path",
                    severity=OmicsAnalysisSeverity.ERROR,
                    message=str(error),
                    relative_path=parent_value,
                )
            )
        if parent_snapshot_manifest is not None:
            if parent_snapshot_manifest == normalized_plan_filename:
                issues.append(
                    OmicsAnalysisIssue(
                        code="parent-manifest-reuses-plan",
                        severity=OmicsAnalysisSeverity.ERROR,
                        message="Analysis plan cannot also serve as its parent snapshot manifest.",
                        relative_path=parent_snapshot_manifest,
                    )
                )
            parent_path = _safe_file(
                resolved_root,
                root_resolved,
                parent_snapshot_manifest,
                issues=issues,
                role="parent-snapshot-manifest",
            )
            if parent_path is not None:
                parent_manifest_sha256 = _sha256_file(parent_path)
                try:
                    parent = _load_json_object(parent_path)
                except (OSError, UnicodeError, json.JSONDecodeError, ValueError) as error:
                    issues.append(
                        OmicsAnalysisIssue(
                            code="invalid-parent-snapshot-json",
                            severity=OmicsAnalysisSeverity.ERROR,
                            message=f"Could not read parent snapshot manifest: {error}",
                            relative_path=parent_snapshot_manifest,
                        )
                    )
                else:
                    parent_snapshot_fingerprint = _string_value(parent, "fingerprint")
                    if parent.get("valid") is not True:
                        issues.append(
                            OmicsAnalysisIssue(
                                code="parent-snapshot-not-valid",
                                severity=OmicsAnalysisSeverity.ERROR,
                                message="Parent snapshot manifest must record valid=true.",
                                relative_path=parent_snapshot_manifest,
                            )
                        )
                    if _string_value(parent, "source_id") != source.source_id:
                        issues.append(
                            OmicsAnalysisIssue(
                                code="parent-source-id-mismatch",
                                severity=OmicsAnalysisSeverity.ERROR,
                                message="Parent snapshot source_id does not match the analysis source.",
                                relative_path=parent_snapshot_manifest,
                            )
                        )
                    if _string_value(parent, "access_identifier") != source.access_identifier:
                        issues.append(
                            OmicsAnalysisIssue(
                                code="parent-access-identifier-mismatch",
                                severity=OmicsAnalysisSeverity.ERROR,
                                message=(
                                    "Parent snapshot accession does not match the registered source."
                                ),
                                relative_path=parent_snapshot_manifest,
                            )
                        )
                    if (
                        parent_snapshot_fingerprint is None
                        or len(parent_snapshot_fingerprint) != 64
                        or any(
                            character not in "0123456789abcdefABCDEF"
                            for character in parent_snapshot_fingerprint
                        )
                    ):
                        issues.append(
                            OmicsAnalysisIssue(
                                code="invalid-parent-snapshot-fingerprint",
                                severity=OmicsAnalysisSeverity.ERROR,
                                message="Parent snapshot fingerprint must be a 64-character hex digest.",
                                relative_path=parent_snapshot_manifest,
                            )
                        )

    assay: AssayMatrixProfile | None = None
    metadata: SampleMetadataProfile | None = None
    if assay_config is not None and metadata_config is not None:
        reserved_paths = {
            normalized_plan_filename,
            DEFAULT_OMICS_ANALYSIS_MANIFEST_FILENAME,
        }
        if parent_snapshot_manifest is not None:
            reserved_paths.add(parent_snapshot_manifest)
        if assay_config.relative_path in reserved_paths:
            issues.append(
                OmicsAnalysisIssue(
                    code="reserved-assay-path",
                    severity=OmicsAnalysisSeverity.ERROR,
                    message="Assay path cannot reuse a plan or manifest path.",
                    relative_path=assay_config.relative_path,
                )
            )
        if metadata_config.relative_path in reserved_paths:
            issues.append(
                OmicsAnalysisIssue(
                    code="reserved-metadata-path",
                    severity=OmicsAnalysisSeverity.ERROR,
                    message="Metadata path cannot reuse a plan or manifest path.",
                    relative_path=metadata_config.relative_path,
                )
            )
        if assay_config.relative_path == metadata_config.relative_path:
            issues.append(
                OmicsAnalysisIssue(
                    code="assay-metadata-path-reused",
                    severity=OmicsAnalysisSeverity.ERROR,
                    message="Assay and metadata must be separate declared files.",
                    relative_path=assay_config.relative_path,
                )
            )
        assay_path = _safe_file(
            resolved_root,
            root_resolved,
            assay_config.relative_path,
            issues=issues,
            role="assay-file",
        )
        metadata_path = _safe_file(
            resolved_root,
            root_resolved,
            metadata_config.relative_path,
            issues=issues,
            role="metadata-file",
        )
        if assay_path is not None:
            assay = _scan_assay(assay_path, assay_config, issues)
        if metadata_path is not None:
            metadata = _scan_metadata(metadata_path, metadata_config, required_columns, issues)

    if assay is not None and metadata is not None:
        assay_ids = set(assay.sample_ids)
        metadata_ids = set(metadata.sample_ids)
        missing_from_metadata = tuple(sorted(assay_ids - metadata_ids))
        missing_from_assay = tuple(sorted(metadata_ids - assay_ids))
        if missing_from_metadata:
            issues.append(
                OmicsAnalysisIssue(
                    code="assay-samples-missing-from-metadata",
                    severity=OmicsAnalysisSeverity.ERROR,
                    count=len(missing_from_metadata),
                    message="Assay sample IDs absent from metadata: " + ", ".join(missing_from_metadata),
                )
            )
        if missing_from_assay:
            issues.append(
                OmicsAnalysisIssue(
                    code="metadata-samples-missing-from-assay",
                    severity=OmicsAnalysisSeverity.ERROR,
                    count=len(missing_from_assay),
                    message="Metadata sample IDs absent from assay: " + ", ".join(missing_from_assay),
                )
            )
        if not missing_from_metadata and not missing_from_assay and assay.sample_ids != metadata.sample_ids:
            issues.append(
                OmicsAnalysisIssue(
                    code="sample-order-differs",
                    severity=OmicsAnalysisSeverity.WARNING,
                    message=(
                        "Assay and metadata contain the same sample IDs in different order; downstream "
                        "construction must join by ID rather than row position."
                    ),
                )
            )
        if assay.sample_count < 2:
            issues.append(
                OmicsAnalysisIssue(
                    code="single-sample-assay",
                    severity=OmicsAnalysisSeverity.WARNING,
                    message="Only one sample is present; most comparative analyses are not identifiable.",
                )
            )
        if assay.feature_count < 2:
            issues.append(
                OmicsAnalysisIssue(
                    code="single-feature-assay",
                    severity=OmicsAnalysisSeverity.WARNING,
                    message="Only one feature is present; this is not a high-dimensional omics matrix.",
                )
            )

    return OmicsAnalysisInputReport(
        source=source,
        root_name=resolved_root.name,
        plan_filename=normalized_plan_filename,
        plan_sha256=plan_sha256,
        parent_snapshot_manifest=parent_snapshot_manifest,
        parent_manifest_sha256=parent_manifest_sha256,
        parent_snapshot_fingerprint=parent_snapshot_fingerprint,
        required_metadata_columns=required_columns,
        assay=assay,
        metadata=metadata,
        issues=tuple(issues),
    )


__all__ = [
    "DEFAULT_OMICS_ANALYSIS_MANIFEST_FILENAME",
    "DEFAULT_OMICS_ANALYSIS_PLAN_FILENAME",
    "AssayMatrixProfile",
    "AssayValueScale",
    "OmicsAnalysisInputReport",
    "OmicsAnalysisIssue",
    "OmicsAnalysisSeverity",
    "OmicsDelimiter",
    "SampleMetadataProfile",
    "inspect_omics_analysis_input",
]
