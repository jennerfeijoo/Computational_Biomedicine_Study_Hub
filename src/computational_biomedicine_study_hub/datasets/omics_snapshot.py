"""Validate a declared local snapshot for one registered public omics source.

The validator is deliberately offline-first. It does not download remote content,
interpret an accession as an analysis, or infer missing metadata. A learner first
creates a small JSON plan that maps the source registry's required evidence roles
to concrete local files. The inspector then checks identity, path safety, file
presence, and content hashes before producing a deterministic manifest.
"""

from __future__ import annotations

import hashlib
import json
from dataclasses import dataclass
from datetime import date
from enum import StrEnum
from pathlib import Path, PurePosixPath
from typing import Final, cast

from .omics_registry import PublicOmicsSource, public_omics_source

DEFAULT_OMICS_PLAN_FILENAME: Final = "snapshot_plan.json"
GENERATED_OMICS_MANIFEST_ROLE: Final = "sha256_manifest.json"


class OmicsSnapshotSeverity(StrEnum):
    """Severity assigned to one public-omics snapshot finding."""

    ERROR = "error"
    WARNING = "warning"


@dataclass(frozen=True, slots=True)
class OmicsSnapshotIssue:
    """One deterministic validation finding."""

    code: str
    severity: OmicsSnapshotSeverity
    message: str
    role: str | None = None
    relative_path: str | None = None
    count: int = 1

    def __post_init__(self) -> None:
        if not self.code.strip() or not self.message.strip():
            raise ValueError("Omics snapshot issues require a code and message.")
        if self.count < 1:
            raise ValueError("Omics snapshot issue counts must be positive.")

    def as_dict(self) -> dict[str, object]:
        """Return a JSON-compatible representation."""

        return {
            "code": self.code,
            "severity": self.severity.value,
            "message": self.message,
            "role": self.role,
            "relative_path": self.relative_path,
            "count": self.count,
        }


@dataclass(frozen=True, slots=True)
class OmicsArtifactProfile:
    """Stable identity for one declared local artifact."""

    role: str
    relative_path: str
    byte_size: int
    sha256: str

    def __post_init__(self) -> None:
        if not self.role.strip() or not self.relative_path.strip():
            raise ValueError("Omics artifact profiles require role and relative path.")
        if self.byte_size < 0:
            raise ValueError("Omics artifact byte size cannot be negative.")
        if len(self.sha256) != 64:
            raise ValueError("Omics artifact profiles require a SHA-256 hex digest.")

    def as_dict(self) -> dict[str, object]:
        """Return a JSON-compatible representation."""

        return {
            "role": self.role,
            "relative_path": self.relative_path,
            "byte_size": self.byte_size,
            "sha256": self.sha256,
        }


@dataclass(frozen=True, slots=True)
class OmicsSnapshotReport:
    """Complete report for one declared local public-omics snapshot."""

    source: PublicOmicsSource
    root_name: str
    plan_filename: str
    plan_sha256: str | None
    retrieved_at: str | None
    artifacts: tuple[OmicsArtifactProfile, ...]
    issues: tuple[OmicsSnapshotIssue, ...]

    @property
    def valid(self) -> bool:
        """Return whether no error-severity findings were detected."""

        return not any(issue.severity is OmicsSnapshotSeverity.ERROR for issue in self.issues)

    @property
    def required_plan_roles(self) -> tuple[str, ...]:
        """Return registry roles that must be mapped before manifest generation."""

        return tuple(
            role
            for role in self.source.required_local_artifacts
            if role != GENERATED_OMICS_MANIFEST_ROLE
        )

    def _identity_payload(self) -> dict[str, object]:
        return {
            "schema_version": 1,
            "source_id": self.source.source_id,
            "access_identifier": self.source.access_identifier,
            "modality": self.source.modality.value,
            "plan_filename": self.plan_filename,
            "plan_sha256": self.plan_sha256,
            "retrieved_at": self.retrieved_at,
            "required_plan_roles": list(self.required_plan_roles),
            "artifacts": [artifact.as_dict() for artifact in self.artifacts],
            "issues": [issue.as_dict() for issue in self.issues],
        }

    @property
    def fingerprint(self) -> str:
        """Return a path-independent fingerprint of evidence and findings."""

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
                "title": self.source.title,
                "provider": self.source.provider,
                "landing_page": self.source.landing_page,
                "expected_sample_unit": self.source.expected_sample_unit,
                "generated_manifest_role": GENERATED_OMICS_MANIFEST_ROLE,
                "valid": self.valid,
                "fingerprint": self.fingerprint,
                "scientific_boundary": self.source.scientific_boundary,
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


def _load_plan(path: Path) -> dict[str, object]:
    text = path.read_text(encoding="utf-8-sig")
    raw = cast(
        object,
        json.loads(text, object_pairs_hook=_unique_json_object),
    )
    if not isinstance(raw, dict) or not all(isinstance(key, str) for key in raw):
        raise ValueError("Snapshot plan root must be a JSON object.")
    return cast(dict[str, object], raw)


def _normalise_relative_path(value: str) -> str:
    if not value or value.strip() != value:
        raise ValueError("Artifact paths cannot be empty or padded with whitespace.")
    if "\\" in value:
        raise ValueError("Artifact paths must use POSIX '/' separators.")
    path = PurePosixPath(value)
    if path.is_absolute() or ".." in path.parts:
        raise ValueError("Artifact paths must remain inside the snapshot directory.")
    normalised = path.as_posix()
    if normalised in {"", "."} or normalised != value:
        raise ValueError("Artifact paths must be normalised relative POSIX paths.")
    return normalised


def _string_field(plan: dict[str, object], field: str) -> str | None:
    value = plan.get(field)
    if isinstance(value, str) and value.strip():
        return value.strip()
    return None


def _base_report(
    source: PublicOmicsSource,
    root: Path,
    plan_filename: str,
    issue: OmicsSnapshotIssue,
) -> OmicsSnapshotReport:
    return OmicsSnapshotReport(
        source=source,
        root_name=root.name or str(root),
        plan_filename=plan_filename,
        plan_sha256=None,
        retrieved_at=None,
        artifacts=(),
        issues=(issue,),
    )


def inspect_public_omics_snapshot(
    root: Path | str,
    *,
    source_id: str,
    plan_filename: str = DEFAULT_OMICS_PLAN_FILENAME,
) -> OmicsSnapshotReport:
    """Validate one declared local snapshot against its registered source contract."""

    source = public_omics_source(source_id)
    resolved_root = Path(root)
    try:
        normalised_plan_filename = _normalise_relative_path(plan_filename)
    except ValueError as error:
        return _base_report(
            source,
            resolved_root,
            plan_filename,
            OmicsSnapshotIssue(
                code="invalid-plan-path",
                severity=OmicsSnapshotSeverity.ERROR,
                message=str(error),
                relative_path=plan_filename,
            ),
        )

    if not resolved_root.is_dir():
        return _base_report(
            source,
            resolved_root,
            normalised_plan_filename,
            OmicsSnapshotIssue(
                code="root-not-directory",
                severity=OmicsSnapshotSeverity.ERROR,
                message=f"Snapshot directory does not exist: {resolved_root}",
            ),
        )

    root_resolved = resolved_root.resolve()
    plan_path = resolved_root.joinpath(*PurePosixPath(normalised_plan_filename).parts)
    if plan_path.is_symlink():
        return _base_report(
            source,
            resolved_root,
            normalised_plan_filename,
            OmicsSnapshotIssue(
                code="plan-is-symlink",
                severity=OmicsSnapshotSeverity.ERROR,
                message="Snapshot plan must be a regular local file, not a symbolic link.",
                relative_path=normalised_plan_filename,
            ),
        )
    if not plan_path.is_file():
        return _base_report(
            source,
            resolved_root,
            normalised_plan_filename,
            OmicsSnapshotIssue(
                code="missing-plan",
                severity=OmicsSnapshotSeverity.ERROR,
                message=f"Snapshot plan is missing: {normalised_plan_filename}",
                relative_path=normalised_plan_filename,
            ),
        )

    try:
        plan = _load_plan(plan_path)
    except (OSError, UnicodeError, json.JSONDecodeError, ValueError) as error:
        return _base_report(
            source,
            resolved_root,
            normalised_plan_filename,
            OmicsSnapshotIssue(
                code="invalid-plan-json",
                severity=OmicsSnapshotSeverity.ERROR,
                message=f"Could not read snapshot plan: {error}",
                relative_path=normalised_plan_filename,
            ),
        )

    issues: list[OmicsSnapshotIssue] = []
    artifacts: list[OmicsArtifactProfile] = []
    plan_sha256 = _sha256_file(plan_path)

    declared_source_id = _string_field(plan, "source_id")
    if declared_source_id != source.source_id:
        issues.append(
            OmicsSnapshotIssue(
                code="source-id-mismatch",
                severity=OmicsSnapshotSeverity.ERROR,
                message=(
                    f"Plan source_id must be {source.source_id!r}; "
                    f"received {declared_source_id!r}."
                ),
            )
        )

    declared_access_identifier = _string_field(plan, "access_identifier")
    if declared_access_identifier != source.access_identifier:
        issues.append(
            OmicsSnapshotIssue(
                code="access-identifier-mismatch",
                severity=OmicsSnapshotSeverity.ERROR,
                message=(
                    f"Plan access_identifier must be {source.access_identifier!r}; "
                    f"received {declared_access_identifier!r}."
                ),
            )
        )

    retrieved_at = _string_field(plan, "retrieved_at")
    if retrieved_at is None:
        issues.append(
            OmicsSnapshotIssue(
                code="missing-retrieved-at",
                severity=OmicsSnapshotSeverity.ERROR,
                message="Plan requires retrieved_at in ISO YYYY-MM-DD format.",
            )
        )
    else:
        try:
            date.fromisoformat(retrieved_at)
        except ValueError:
            issues.append(
                OmicsSnapshotIssue(
                    code="invalid-retrieved-at",
                    severity=OmicsSnapshotSeverity.ERROR,
                    message="retrieved_at must use a valid ISO YYYY-MM-DD date.",
                )
            )

    known_fields = {"source_id", "access_identifier", "retrieved_at", "artifact_paths"}
    unknown_fields = tuple(sorted(set(plan) - known_fields))
    if unknown_fields:
        issues.append(
            OmicsSnapshotIssue(
                code="unknown-plan-fields",
                severity=OmicsSnapshotSeverity.WARNING,
                count=len(unknown_fields),
                message="Unrecognised plan fields: " + ", ".join(unknown_fields),
            )
        )

    raw_artifact_paths = plan.get("artifact_paths")
    if not isinstance(raw_artifact_paths, dict) or not all(
        isinstance(role, str) for role in raw_artifact_paths
    ):
        issues.append(
            OmicsSnapshotIssue(
                code="invalid-artifact-map",
                severity=OmicsSnapshotSeverity.ERROR,
                message="artifact_paths must be a JSON object mapping roles to path lists.",
            )
        )
        raw_artifact_paths = {}

    artifact_paths = cast(dict[str, object], raw_artifact_paths)
    required_roles = tuple(
        role
        for role in source.required_local_artifacts
        if role != GENERATED_OMICS_MANIFEST_ROLE
    )
    missing_roles = tuple(role for role in required_roles if role not in artifact_paths)
    if missing_roles:
        issues.append(
            OmicsSnapshotIssue(
                code="missing-artifact-roles",
                severity=OmicsSnapshotSeverity.ERROR,
                count=len(missing_roles),
                message="Missing required artifact roles: " + ", ".join(missing_roles),
            )
        )

    if GENERATED_OMICS_MANIFEST_ROLE in artifact_paths:
        issues.append(
            OmicsSnapshotIssue(
                code="generated-manifest-listed",
                severity=OmicsSnapshotSeverity.ERROR,
                role=GENERATED_OMICS_MANIFEST_ROLE,
                message=(
                    "The generated SHA-256 manifest must not be listed as input evidence; "
                    "it is produced after validation."
                ),
            )
        )

    extra_roles = tuple(
        sorted(
            role
            for role in artifact_paths
            if role not in source.required_local_artifacts
        )
    )
    if extra_roles:
        issues.append(
            OmicsSnapshotIssue(
                code="extra-artifact-roles",
                severity=OmicsSnapshotSeverity.WARNING,
                count=len(extra_roles),
                message="Additional declared artifact roles: " + ", ".join(extra_roles),
            )
        )

    declared_paths: dict[str, str] = {}
    for role in sorted(artifact_paths):
        if role == GENERATED_OMICS_MANIFEST_ROLE:
            continue
        raw_paths = artifact_paths[role]
        if not isinstance(raw_paths, list) or not raw_paths:
            issues.append(
                OmicsSnapshotIssue(
                    code="invalid-role-path-list",
                    severity=OmicsSnapshotSeverity.ERROR,
                    role=role,
                    message="Each artifact role must map to a non-empty JSON path list.",
                )
            )
            continue

        for raw_path in raw_paths:
            if not isinstance(raw_path, str):
                issues.append(
                    OmicsSnapshotIssue(
                        code="invalid-artifact-path-type",
                        severity=OmicsSnapshotSeverity.ERROR,
                        role=role,
                        message="Artifact paths must be strings.",
                    )
                )
                continue
            try:
                relative_path = _normalise_relative_path(raw_path)
            except ValueError as error:
                issues.append(
                    OmicsSnapshotIssue(
                        code="invalid-artifact-path",
                        severity=OmicsSnapshotSeverity.ERROR,
                        role=role,
                        relative_path=raw_path,
                        message=str(error),
                    )
                )
                continue

            if relative_path in {
                normalised_plan_filename,
                GENERATED_OMICS_MANIFEST_ROLE,
            }:
                issues.append(
                    OmicsSnapshotIssue(
                        code="reserved-artifact-path",
                        severity=OmicsSnapshotSeverity.ERROR,
                        role=role,
                        relative_path=relative_path,
                        message="Plan and generated-manifest files cannot be input artifacts.",
                    )
                )
                continue

            previous_role = declared_paths.get(relative_path)
            if previous_role is not None:
                issues.append(
                    OmicsSnapshotIssue(
                        code="artifact-path-reused",
                        severity=OmicsSnapshotSeverity.ERROR,
                        role=role,
                        relative_path=relative_path,
                        message=(
                            f"Artifact path is already assigned to role {previous_role!r}; "
                            "one file cannot silently represent multiple evidence roles."
                        ),
                    )
                )
                continue
            declared_paths[relative_path] = role

            artifact_path = resolved_root.joinpath(*PurePosixPath(relative_path).parts)
            try:
                artifact_path.resolve(strict=False).relative_to(root_resolved)
            except ValueError:
                issues.append(
                    OmicsSnapshotIssue(
                        code="artifact-path-escapes-root",
                        severity=OmicsSnapshotSeverity.ERROR,
                        role=role,
                        relative_path=relative_path,
                        message="Artifact path resolves outside the snapshot directory.",
                    )
                )
                continue

            if artifact_path.is_symlink():
                issues.append(
                    OmicsSnapshotIssue(
                        code="artifact-is-symlink",
                        severity=OmicsSnapshotSeverity.ERROR,
                        role=role,
                        relative_path=relative_path,
                        message="Declared artifacts must be regular local files, not symbolic links.",
                    )
                )
                continue
            if not artifact_path.is_file():
                issues.append(
                    OmicsSnapshotIssue(
                        code="missing-artifact-file",
                        severity=OmicsSnapshotSeverity.ERROR,
                        role=role,
                        relative_path=relative_path,
                        message="Declared artifact file does not exist.",
                    )
                )
                continue

            byte_size = artifact_path.stat().st_size
            if byte_size == 0:
                issues.append(
                    OmicsSnapshotIssue(
                        code="empty-artifact-file",
                        severity=OmicsSnapshotSeverity.ERROR,
                        role=role,
                        relative_path=relative_path,
                        message="Declared artifact file is empty.",
                    )
                )
            artifacts.append(
                OmicsArtifactProfile(
                    role=role,
                    relative_path=relative_path,
                    byte_size=byte_size,
                    sha256=_sha256_file(artifact_path),
                )
            )

    tracked_paths = set(declared_paths)
    untracked_paths: list[str] = []
    for path in resolved_root.rglob("*"):
        if not path.is_file() and not path.is_symlink():
            continue
        relative_path = path.relative_to(resolved_root).as_posix()
        if relative_path in {
            normalised_plan_filename,
            GENERATED_OMICS_MANIFEST_ROLE,
        }:
            continue
        if relative_path not in tracked_paths:
            untracked_paths.append(relative_path)
    if untracked_paths:
        issues.append(
            OmicsSnapshotIssue(
                code="untracked-local-files",
                severity=OmicsSnapshotSeverity.WARNING,
                count=len(untracked_paths),
                message="Local files not covered by artifact_paths: "
                + ", ".join(sorted(untracked_paths)),
            )
        )

    return OmicsSnapshotReport(
        source=source,
        root_name=resolved_root.name,
        plan_filename=normalised_plan_filename,
        plan_sha256=plan_sha256,
        retrieved_at=retrieved_at,
        artifacts=tuple(sorted(artifacts, key=lambda item: (item.role, item.relative_path))),
        issues=tuple(issues),
    )


__all__ = [
    "DEFAULT_OMICS_PLAN_FILENAME",
    "GENERATED_OMICS_MANIFEST_ROLE",
    "OmicsArtifactProfile",
    "OmicsSnapshotIssue",
    "OmicsSnapshotReport",
    "OmicsSnapshotSeverity",
    "inspect_public_omics_snapshot",
]
