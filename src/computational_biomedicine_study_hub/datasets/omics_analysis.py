"""Validate lineage, assay orientation, and sample metadata before omics analysis."""

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
    """Supported explicit delimiters."""

    COMMA = "comma"
    TAB = "tab"


class AssayValueScale(StrEnum):
    """Declared numerical representation of assay cells."""

    RAW_COUNTS = "raw_counts"
    NONNEGATIVE_CONTINUOUS = "nonnegative_continuous"
    REAL_CONTINUOUS = "real_continuous"


@dataclass(frozen=True, slots=True)
class OmicsAnalysisIssue:
    """One deterministic validation finding."""

    code: str
    severity: OmicsAnalysisSeverity
    message: str
    relative_path: str | None = None
    column: str | None = None
    count: int = 1

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
    """Structural and numerical profile of one feature-by-sample assay."""

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

    @property
    def sample_count(self) -> int:
        """Return the number of sample columns."""

        return len(self.sample_ids)

    @property
    def missing_fraction(self) -> float:
        """Return the fraction of assay cells that are empty."""

        if self.value_count == 0:
            return 0.0
        return self.missing_value_count / self.value_count

    @property
    def zero_fraction_observed(self) -> float:
        """Return the observed-cell fraction equal to zero."""

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
    """Complete lineage and analytical-input report."""

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
        """Return whether assay and metadata contain identical sample-ID sets."""

        if self.assay is None or self.metadata is None:
            return False
        return set(self.assay.sample_ids) == set(self.metadata.sample_ids)

    @property
    def sample_order_matches(self) -> bool:
        """Return whether assay and metadata also share sample order."""

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
        """Return a root-independent transition fingerprint."""

        encoded = json.dumps(
            self._identity_payload(),
            ensure_ascii=False,
            sort_keys=True,
            separators=(",", ":"),
        ).encode("utf-8")
        return hashlib.sha256(encoded).hexdigest()

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
        """Serialize the transition manifest with stable key ordering."""

        return json.dumps(
            self.manifest_payload(),
            ensure_ascii=False,
            sort_keys=True,
            indent=indent,
        )


@dataclass(frozen=True, slots=True)
class _AssayConfig:
    path: str
    delimiter: OmicsDelimiter
    feature_id_column: str
    value_scale: AssayValueScale
    allow_missing_values: bool


@dataclass(frozen=True, slots=True)
class _MetadataConfig:
    path: str
    delimiter: OmicsDelimiter
    sample_id_column: str


def _sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        while chunk := handle.read(1024 * 1024):
            digest.update(chunk)
    return digest.hexdigest()


def _unique_object(pairs: list[tuple[str, object]]) -> dict[str, object]:
    result: dict[str, object] = {}
    for key, value in pairs:
        if key in result:
            raise ValueError(f"Duplicate JSON object key {key!r}.")
        result[key] = value
    return result


def _load_object(path: Path) -> dict[str, object]:
    raw = cast(
        object,
        json.loads(
            path.read_text(encoding="utf-8-sig"),
            object_pairs_hook=_unique_object,
        ),
    )
    if not isinstance(raw, dict) or not all(isinstance(key, str) for key in raw):
        raise ValueError("JSON root must be an object.")
    return cast(dict[str, object], raw)


def _relative_path(value: object) -> str:
    if not isinstance(value, str) or not value or value.strip() != value:
        raise ValueError("Path must be a non-empty, unpadded string.")
    if "\\" in value:
        raise ValueError("Path must use POSIX '/' separators.")
    path = PurePosixPath(value)
    if path.is_absolute() or ".." in path.parts or path.as_posix() != value or value == ".":
        raise ValueError("Path must be normalized and remain inside the analysis directory.")
    return value


def _string(mapping: dict[str, object], key: str) -> str | None:
    value = mapping.get(key)
    if isinstance(value, str) and value and value.strip() == value:
        return value
    return None


def _delimiter_value(value: object) -> OmicsDelimiter | None:
    if not isinstance(value, str):
        return None
    try:
        return OmicsDelimiter(value)
    except ValueError:
        return None


def _scale_value(value: object) -> AssayValueScale | None:
    if not isinstance(value, str):
        return None
    try:
        return AssayValueScale(value)
    except ValueError:
        return None


def _issue(
    issues: list[OmicsAnalysisIssue],
    code: str,
    severity: OmicsAnalysisSeverity,
    message: str,
    *,
    relative_path: str | None = None,
    column: str | None = None,
    count: int = 1,
) -> None:
    issues.append(
        OmicsAnalysisIssue(
            code=code,
            severity=severity,
            message=message,
            relative_path=relative_path,
            column=column,
            count=count,
        )
    )


def _regular_file(
    root: Path,
    root_resolved: Path,
    relative_path: str,
    role: str,
    issues: list[OmicsAnalysisIssue],
) -> Path | None:
    path = root.joinpath(*PurePosixPath(relative_path).parts)
    try:
        path.resolve(strict=False).relative_to(root_resolved)
    except ValueError:
        _issue(
            issues,
            f"{role}-path-escapes-root",
            OmicsAnalysisSeverity.ERROR,
            "Declared path resolves outside the analysis directory.",
            relative_path=relative_path,
        )
        return None
    if path.is_symlink() or not path.is_file() or path.stat().st_size == 0:
        _issue(
            issues,
            f"missing-empty-or-symlinked-{role}",
            OmicsAnalysisSeverity.ERROR,
            "Declared input must be a non-empty regular local file.",
            relative_path=relative_path,
        )
        return None
    return path


def _parse_assay(
    plan: dict[str, object],
    issues: list[OmicsAnalysisIssue],
) -> _AssayConfig | None:
    raw = plan.get("assay")
    if not isinstance(raw, dict):
        _issue(
            issues,
            "invalid-assay-config",
            OmicsAnalysisSeverity.ERROR,
            "assay must be a JSON object.",
        )
        return None
    mapping = cast(dict[str, object], raw)
    feature_column = _string(mapping, "feature_id_column")
    delimiter = _delimiter_value(mapping.get("delimiter"))
    value_scale = _scale_value(mapping.get("value_scale"))
    allow_missing = mapping.get("allow_missing_values")
    try:
        path = _relative_path(mapping.get("path"))
    except ValueError as error:
        _issue(
            issues,
            "invalid-assay-path",
            OmicsAnalysisSeverity.ERROR,
            str(error),
        )
        return None
    if (
        feature_column is None
        or delimiter is None
        or value_scale is None
        or not isinstance(allow_missing, bool)
    ):
        _issue(
            issues,
            "incomplete-assay-config",
            OmicsAnalysisSeverity.ERROR,
            "assay requires supported delimiter, value scale, feature ID, and missingness fields.",
        )
        return None
    return _AssayConfig(
        path=path,
        delimiter=delimiter,
        feature_id_column=feature_column,
        value_scale=value_scale,
        allow_missing_values=allow_missing,
    )


def _parse_metadata(
    plan: dict[str, object],
    issues: list[OmicsAnalysisIssue],
) -> _MetadataConfig | None:
    raw = plan.get("sample_metadata")
    if not isinstance(raw, dict):
        _issue(
            issues,
            "invalid-metadata-config",
            OmicsAnalysisSeverity.ERROR,
            "sample_metadata must be a JSON object.",
        )
        return None
    mapping = cast(dict[str, object], raw)
    sample_column = _string(mapping, "sample_id_column")
    delimiter = _delimiter_value(mapping.get("delimiter"))
    try:
        path = _relative_path(mapping.get("path"))
    except ValueError as error:
        _issue(
            issues,
            "invalid-metadata-path",
            OmicsAnalysisSeverity.ERROR,
            str(error),
        )
        return None
    if sample_column is None or delimiter is None:
        _issue(
            issues,
            "incomplete-metadata-config",
            OmicsAnalysisSeverity.ERROR,
            "sample_metadata requires a supported delimiter and sample_id_column.",
        )
        return None
    return _MetadataConfig(
        path=path,
        delimiter=delimiter,
        sample_id_column=sample_column,
    )


def _required_columns(
    plan: dict[str, object],
    issues: list[OmicsAnalysisIssue],
) -> tuple[str, ...]:
    raw = plan.get("required_metadata_columns")
    if not isinstance(raw, list) or not raw:
        _issue(
            issues,
            "invalid-required-metadata-columns",
            OmicsAnalysisSeverity.ERROR,
            "required_metadata_columns must be a non-empty list.",
        )
        return ()
    values = tuple(value for value in raw if isinstance(value, str))
    invalid = len(values) != len(raw) or any(
        not value or value.strip() != value for value in values
    )
    if invalid:
        _issue(
            issues,
            "invalid-required-metadata-columns",
            OmicsAnalysisSeverity.ERROR,
            "Required metadata column names must be non-empty and unpadded.",
        )
        return ()
    if len(values) != len(set(values)):
        _issue(
            issues,
            "duplicate-required-metadata-columns",
            OmicsAnalysisSeverity.ERROR,
            "required_metadata_columns cannot contain duplicates.",
        )
    return values


def _delimiter_character(value: OmicsDelimiter) -> str:
    if value is OmicsDelimiter.COMMA:
        return ","
    return "\t"


def _scan_assay(
    path: Path,
    config: _AssayConfig,
    issues: list[OmicsAnalysisIssue],
) -> AssayMatrixProfile | None:
    feature_ids: set[str] = set()
    sample_ids: tuple[str, ...] = ()
    feature_count = 0
    value_count = 0
    observed_count = 0
    missing_count = 0
    zero_count = 0
    duplicate_features = 0
    blank_features = 0
    malformed_rows = 0
    non_numeric = 0
    non_finite = 0
    negative = 0
    non_integer = 0

    try:
        with path.open("r", encoding="utf-8-sig", newline="") as handle:
            reader = csv.reader(
                handle,
                delimiter=_delimiter_character(config.delimiter),
            )
            header_list = next(reader, None)
            if header_list is None:
                _issue(
                    issues,
                    "empty-assay-table",
                    OmicsAnalysisSeverity.ERROR,
                    "Assay table has no header.",
                    relative_path=config.path,
                )
                return None
            header = tuple(header_list)
            if any(not item or item.strip() != item for item in header):
                _issue(
                    issues,
                    "invalid-assay-header",
                    OmicsAnalysisSeverity.ERROR,
                    "Assay columns must be non-empty and unpadded.",
                    relative_path=config.path,
                )
            if len(header) != len(set(header)):
                _issue(
                    issues,
                    "duplicate-assay-columns",
                    OmicsAnalysisSeverity.ERROR,
                    "Assay header contains duplicate columns.",
                    relative_path=config.path,
                )
            if config.feature_id_column not in header:
                _issue(
                    issues,
                    "missing-feature-id-column",
                    OmicsAnalysisSeverity.ERROR,
                    "Declared feature_id_column is absent from the assay.",
                    relative_path=config.path,
                    column=config.feature_id_column,
                )
                return None
            feature_index = header.index(config.feature_id_column)
            sample_ids = tuple(item for index, item in enumerate(header) if index != feature_index)
            if not sample_ids:
                _issue(
                    issues,
                    "assay-has-no-samples",
                    OmicsAnalysisSeverity.ERROR,
                    "Assay requires at least one sample column.",
                    relative_path=config.path,
                )

            for row in reader:
                feature_count += 1
                if len(row) != len(header):
                    malformed_rows += 1
                    continue
                feature_id = row[feature_index]
                if not feature_id or feature_id.strip() != feature_id:
                    blank_features += 1
                elif feature_id in feature_ids:
                    duplicate_features += 1
                else:
                    feature_ids.add(feature_id)

                for index, raw_value in enumerate(row):
                    if index == feature_index:
                        continue
                    value_count += 1
                    text = raw_value.strip()
                    if not text:
                        missing_count += 1
                        continue
                    observed_count += 1
                    try:
                        number = float(text)
                    except ValueError:
                        non_numeric += 1
                        continue
                    if not math.isfinite(number):
                        non_finite += 1
                        continue
                    zero_count += int(number == 0)
                    negative += int(number < 0)
                    if config.value_scale is AssayValueScale.RAW_COUNTS:
                        non_integer += int(not number.is_integer())
    except (OSError, csv.Error, UnicodeError) as error:
        _issue(
            issues,
            "assay-read-error",
            OmicsAnalysisSeverity.ERROR,
            f"Could not read assay table: {error}",
            relative_path=config.path,
        )
        return None

    assay_errors = (
        ("assay-has-no-features", int(feature_count == 0), "Assay contains no features."),
        ("malformed-assay-rows", malformed_rows, "Assay rows do not match header width."),
        (
            "blank-or-padded-feature-ids",
            blank_features,
            "Feature IDs must be non-empty and unpadded.",
        ),
        (
            "duplicate-feature-ids",
            duplicate_features,
            "Feature IDs must be unique at the declared analytical level.",
        ),
        (
            "non-numeric-assay-values",
            non_numeric,
            "Assay cells must be numeric or empty.",
        ),
        (
            "non-finite-assay-values",
            non_finite,
            "Assay cells cannot contain NaN or infinity.",
        ),
    )
    for code, count, message in assay_errors:
        if count:
            _issue(
                issues,
                code,
                OmicsAnalysisSeverity.ERROR,
                message,
                relative_path=config.path,
                count=count,
            )
    if missing_count:
        _issue(
            issues,
            "declared-missing-assay-values"
            if config.allow_missing_values
            else "unexpected-missing-assay-values",
            OmicsAnalysisSeverity.WARNING
            if config.allow_missing_values
            else OmicsAnalysisSeverity.ERROR,
            "Missing assay cells require an explicit downstream missingness strategy.",
            relative_path=config.path,
            count=missing_count,
        )
    if negative and config.value_scale is not AssayValueScale.REAL_CONTINUOUS:
        _issue(
            issues,
            "negative-values-in-nonnegative-scale",
            OmicsAnalysisSeverity.ERROR,
            "Declared raw-count and nonnegative-continuous scales cannot be negative.",
            relative_path=config.path,
            count=negative,
        )
    if non_integer:
        _issue(
            issues,
            "non-integer-raw-counts",
            OmicsAnalysisSeverity.ERROR,
            "raw_counts requires integer-valued observed cells.",
            relative_path=config.path,
            count=non_integer,
        )

    return AssayMatrixProfile(
        relative_path=config.path,
        sha256=_sha256(path),
        delimiter=config.delimiter,
        feature_id_column=config.feature_id_column,
        value_scale=config.value_scale,
        allow_missing_values=config.allow_missing_values,
        sample_ids=sample_ids,
        feature_count=feature_count,
        value_count=value_count,
        observed_value_count=observed_count,
        missing_value_count=missing_count,
        zero_value_count=zero_count,
        duplicate_feature_ids=duplicate_features,
        blank_feature_ids=blank_features,
        malformed_rows=malformed_rows,
        non_numeric_values=non_numeric,
        non_finite_values=non_finite,
        negative_values=negative,
        non_integer_values=non_integer,
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
    duplicate_ids = 0
    blank_ids = 0
    malformed_rows = 0
    blank_required = 0

    try:
        with path.open("r", encoding="utf-8-sig", newline="") as handle:
            reader = csv.reader(
                handle,
                delimiter=_delimiter_character(config.delimiter),
            )
            header_list = next(reader, None)
            if header_list is None:
                _issue(
                    issues,
                    "empty-metadata-table",
                    OmicsAnalysisSeverity.ERROR,
                    "Metadata table has no header.",
                    relative_path=config.path,
                )
                return None
            header = tuple(header_list)
            if any(not item or item.strip() != item for item in header):
                _issue(
                    issues,
                    "invalid-metadata-header",
                    OmicsAnalysisSeverity.ERROR,
                    "Metadata columns must be non-empty and unpadded.",
                    relative_path=config.path,
                )
            if len(header) != len(set(header)):
                _issue(
                    issues,
                    "duplicate-metadata-columns",
                    OmicsAnalysisSeverity.ERROR,
                    "Metadata header contains duplicate columns.",
                    relative_path=config.path,
                )
            if config.sample_id_column not in header:
                _issue(
                    issues,
                    "missing-sample-id-column",
                    OmicsAnalysisSeverity.ERROR,
                    "Declared sample_id_column is absent from metadata.",
                    relative_path=config.path,
                    column=config.sample_id_column,
                )
                return None
            missing_columns = tuple(item for item in required_columns if item not in header)
            if missing_columns:
                _issue(
                    issues,
                    "missing-required-metadata-columns",
                    OmicsAnalysisSeverity.ERROR,
                    "Missing required metadata columns: " + ", ".join(missing_columns),
                    relative_path=config.path,
                    count=len(missing_columns),
                )
            sample_index = header.index(config.sample_id_column)
            required_indices = tuple(
                header.index(item) for item in required_columns if item in header
            )

            for row in reader:
                row_count += 1
                if len(row) != len(header):
                    malformed_rows += 1
                    continue
                sample_id = row[sample_index]
                if not sample_id or sample_id.strip() != sample_id:
                    blank_ids += 1
                else:
                    sample_ids.append(sample_id)
                    duplicate_ids += int(sample_id in seen_sample_ids)
                    seen_sample_ids.add(sample_id)
                blank_required += sum(not row[index].strip() for index in required_indices)
    except (OSError, csv.Error, UnicodeError) as error:
        _issue(
            issues,
            "metadata-read-error",
            OmicsAnalysisSeverity.ERROR,
            f"Could not read metadata table: {error}",
            relative_path=config.path,
        )
        return None

    metadata_errors = (
        ("metadata-has-no-samples", int(row_count == 0), "Metadata contains no samples."),
        (
            "malformed-metadata-rows",
            malformed_rows,
            "Metadata rows do not match header width.",
        ),
        (
            "blank-or-padded-sample-ids",
            blank_ids,
            "Sample IDs must be non-empty and unpadded.",
        ),
        (
            "duplicate-sample-ids",
            duplicate_ids,
            "Metadata must contain one row per sample ID.",
        ),
        (
            "blank-required-metadata-cells",
            blank_required,
            "Required metadata columns cannot contain blank cells.",
        ),
    )
    for code, count, message in metadata_errors:
        if count:
            _issue(
                issues,
                code,
                OmicsAnalysisSeverity.ERROR,
                message,
                relative_path=config.path,
                count=count,
            )

    return SampleMetadataProfile(
        relative_path=config.path,
        sha256=_sha256(path),
        delimiter=config.delimiter,
        sample_id_column=config.sample_id_column,
        columns=header,
        sample_ids=tuple(sample_ids),
        row_count=row_count,
        duplicate_sample_ids=duplicate_ids,
        blank_sample_ids=blank_ids,
        malformed_rows=malformed_rows,
        blank_required_cells=blank_required,
    )


def _empty_report(
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


def _validate_parent_manifest(
    root: Path,
    root_resolved: Path,
    source: PublicOmicsSource,
    relative_path: str,
    issues: list[OmicsAnalysisIssue],
) -> tuple[str | None, str | None]:
    path = _regular_file(
        root,
        root_resolved,
        relative_path,
        "parent-snapshot-manifest",
        issues,
    )
    if path is None:
        return None, None
    manifest_sha256 = _sha256(path)
    try:
        parent = _load_object(path)
    except (OSError, UnicodeError, json.JSONDecodeError, ValueError) as error:
        _issue(
            issues,
            "invalid-parent-snapshot-json",
            OmicsAnalysisSeverity.ERROR,
            f"Could not read parent snapshot manifest: {error}",
            relative_path=relative_path,
        )
        return manifest_sha256, None

    fingerprint = _string(parent, "fingerprint")
    if parent.get("valid") is not True:
        _issue(
            issues,
            "parent-snapshot-not-valid",
            OmicsAnalysisSeverity.ERROR,
            "Parent snapshot manifest must record valid=true.",
            relative_path=relative_path,
        )
    if _string(parent, "source_id") != source.source_id:
        _issue(
            issues,
            "parent-source-id-mismatch",
            OmicsAnalysisSeverity.ERROR,
            "Parent snapshot source_id does not match this analysis.",
            relative_path=relative_path,
        )
    if _string(parent, "access_identifier") != source.access_identifier:
        _issue(
            issues,
            "parent-access-identifier-mismatch",
            OmicsAnalysisSeverity.ERROR,
            "Parent snapshot accession does not match the registry.",
            relative_path=relative_path,
        )
    invalid_fingerprint = (
        fingerprint is None
        or len(fingerprint) != 64
        or any(character not in "0123456789abcdefABCDEF" for character in fingerprint)
    )
    if invalid_fingerprint:
        _issue(
            issues,
            "invalid-parent-snapshot-fingerprint",
            OmicsAnalysisSeverity.ERROR,
            "Parent snapshot fingerprint must be a 64-character hex digest.",
            relative_path=relative_path,
        )
    return manifest_sha256, fingerprint


def inspect_omics_analysis_input(
    root: Path | str,
    *,
    source_id: str,
    plan_filename: str = DEFAULT_OMICS_ANALYSIS_PLAN_FILENAME,
) -> OmicsAnalysisInputReport:
    """Validate one assay/metadata transition linked to a snapshot manifest."""

    source = public_omics_source(source_id)
    root_path = Path(root)
    try:
        normalized_plan = _relative_path(plan_filename)
    except ValueError as error:
        return _empty_report(
            source,
            root_path,
            plan_filename,
            OmicsAnalysisIssue(
                code="invalid-analysis-plan-path",
                severity=OmicsAnalysisSeverity.ERROR,
                message=str(error),
                relative_path=plan_filename,
            ),
        )
    if not root_path.is_dir():
        return _empty_report(
            source,
            root_path,
            normalized_plan,
            OmicsAnalysisIssue(
                code="root-not-directory",
                severity=OmicsAnalysisSeverity.ERROR,
                message=f"Analysis directory does not exist: {root_path}",
            ),
        )
    plan_path = root_path.joinpath(*PurePosixPath(normalized_plan).parts)
    if plan_path.is_symlink() or not plan_path.is_file():
        return _empty_report(
            source,
            root_path,
            normalized_plan,
            OmicsAnalysisIssue(
                code="missing-or-symlinked-analysis-plan",
                severity=OmicsAnalysisSeverity.ERROR,
                message="Analysis plan must be a regular local file.",
                relative_path=normalized_plan,
            ),
        )
    try:
        plan = _load_object(plan_path)
    except (OSError, UnicodeError, json.JSONDecodeError, ValueError) as error:
        return _empty_report(
            source,
            root_path,
            normalized_plan,
            OmicsAnalysisIssue(
                code="invalid-analysis-plan-json",
                severity=OmicsAnalysisSeverity.ERROR,
                message=f"Could not read analysis plan: {error}",
                relative_path=normalized_plan,
            ),
        )

    issues: list[OmicsAnalysisIssue] = []
    if plan.get("schema_version") != 1:
        _issue(
            issues,
            "unsupported-analysis-schema-version",
            OmicsAnalysisSeverity.ERROR,
            "analysis_plan.json requires schema_version 1.",
        )
    if _string(plan, "source_id") != source.source_id:
        _issue(
            issues,
            "analysis-source-id-mismatch",
            OmicsAnalysisSeverity.ERROR,
            "Analysis source_id does not match the requested registry source.",
        )

    required_columns = _required_columns(plan, issues)
    assay_config = _parse_assay(plan, issues)
    metadata_config = _parse_metadata(plan, issues)
    root_resolved = root_path.resolve()

    parent_relative: str | None = None
    parent_sha256: str | None = None
    parent_fingerprint: str | None = None
    try:
        parent_relative = _relative_path(plan.get("parent_snapshot_manifest"))
    except ValueError as error:
        _issue(
            issues,
            "invalid-parent-manifest-path",
            OmicsAnalysisSeverity.ERROR,
            str(error),
        )
    if parent_relative is not None:
        parent_sha256, parent_fingerprint = _validate_parent_manifest(
            root_path,
            root_resolved,
            source,
            parent_relative,
            issues,
        )

    assay: AssayMatrixProfile | None = None
    metadata: SampleMetadataProfile | None = None
    if assay_config is not None and metadata_config is not None:
        reserved_paths = {
            normalized_plan,
            DEFAULT_OMICS_ANALYSIS_MANIFEST_FILENAME,
        }
        if parent_relative is not None:
            reserved_paths.add(parent_relative)
        if assay_config.path in reserved_paths or metadata_config.path in reserved_paths:
            _issue(
                issues,
                "reserved-analysis-input-path",
                OmicsAnalysisSeverity.ERROR,
                "Assay and metadata paths cannot reuse plan or manifest paths.",
            )
        if assay_config.path == metadata_config.path:
            _issue(
                issues,
                "assay-metadata-path-reused",
                OmicsAnalysisSeverity.ERROR,
                "Assay and metadata must be separate files.",
                relative_path=assay_config.path,
            )

        assay_path = _regular_file(
            root_path,
            root_resolved,
            assay_config.path,
            "assay-file",
            issues,
        )
        metadata_path = _regular_file(
            root_path,
            root_resolved,
            metadata_config.path,
            "metadata-file",
            issues,
        )
        if assay_path is not None:
            assay = _scan_assay(assay_path, assay_config, issues)
        if metadata_path is not None:
            metadata = _scan_metadata(
                metadata_path,
                metadata_config,
                required_columns,
                issues,
            )

    if assay is not None and metadata is not None:
        assay_ids = set(assay.sample_ids)
        metadata_ids = set(metadata.sample_ids)
        assay_only = tuple(sorted(assay_ids - metadata_ids))
        metadata_only = tuple(sorted(metadata_ids - assay_ids))
        if assay_only:
            _issue(
                issues,
                "assay-samples-missing-from-metadata",
                OmicsAnalysisSeverity.ERROR,
                "Assay sample IDs absent from metadata: " + ", ".join(assay_only),
                count=len(assay_only),
            )
        if metadata_only:
            _issue(
                issues,
                "metadata-samples-missing-from-assay",
                OmicsAnalysisSeverity.ERROR,
                "Metadata sample IDs absent from assay: " + ", ".join(metadata_only),
                count=len(metadata_only),
            )
        if not assay_only and not metadata_only and assay.sample_ids != metadata.sample_ids:
            _issue(
                issues,
                "sample-order-differs",
                OmicsAnalysisSeverity.WARNING,
                "Join assay and metadata by sample ID rather than row position.",
            )
        if assay.sample_count < 2:
            _issue(
                issues,
                "single-sample-assay",
                OmicsAnalysisSeverity.WARNING,
                "Most comparative analyses are not identifiable with one sample.",
            )
        if assay.feature_count < 2:
            _issue(
                issues,
                "single-feature-assay",
                OmicsAnalysisSeverity.WARNING,
                "One feature is not a high-dimensional omics matrix.",
            )

    return OmicsAnalysisInputReport(
        source=source,
        root_name=root_path.name,
        plan_filename=normalized_plan,
        plan_sha256=_sha256(plan_path),
        parent_snapshot_manifest=parent_relative,
        parent_manifest_sha256=parent_sha256,
        parent_snapshot_fingerprint=parent_fingerprint,
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
