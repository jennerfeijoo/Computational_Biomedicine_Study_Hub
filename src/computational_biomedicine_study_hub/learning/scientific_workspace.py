"""Typed definitions for persistent multi-file scientific laboratory workspaces."""

from __future__ import annotations

from dataclasses import dataclass
from enum import StrEnum
from pathlib import PurePosixPath

MAX_WORKSPACE_FILE_BYTES = 1_000_000
MAX_WORKSPACE_OUTPUT_CHARS = 65_536


class WorkspaceDefinitionError(ValueError):
    """Raised when an authored workspace template is unsafe or inconsistent."""


class WorkspaceFileRole(StrEnum):
    """Pedagogical role of one authored workspace file."""

    README = "readme"
    DATA = "data"
    METADATA = "metadata"
    SOURCE = "source"
    TEST = "test"
    REPORT = "report"
    OUTPUT = "output"


class WorkspaceExecutionMode(StrEnum):
    """Supported deterministic workspace execution operations."""

    RUN = "run"
    TEST = "test"


class WorkspaceExecutionStatus(StrEnum):
    """Normalized result of one controlled workspace process."""

    PASSED = "passed"
    FAILED = "failed"
    REJECTED = "rejected"
    TIMED_OUT = "timed_out"
    OUTPUT_LIMIT = "output_limit"
    MISSING_DEPENDENCY = "missing_dependency"
    RUNTIME_ERROR = "runtime_error"


@dataclass(frozen=True, slots=True)
class WorkspaceFileTemplate:
    """One file materialized inside an authored laboratory workspace."""

    relative_path: str
    content: str
    role: WorkspaceFileRole
    editable: bool = False

    def __post_init__(self) -> None:
        normalized = normalize_workspace_path(self.relative_path)
        if len(self.content.encode("utf-8")) > MAX_WORKSPACE_FILE_BYTES:
            raise WorkspaceDefinitionError(
                f"Workspace file {normalized!r} exceeds the authored size limit."
            )
        if (
            self.role
            in {
                WorkspaceFileRole.DATA,
                WorkspaceFileRole.METADATA,
                WorkspaceFileRole.TEST,
                WorkspaceFileRole.README,
            }
            and self.editable
        ):
            raise WorkspaceDefinitionError(
                f"Workspace file {normalized!r} has an immutable role and cannot be editable."
            )
        object.__setattr__(self, "relative_path", normalized)


@dataclass(frozen=True, slots=True)
class ScientificWorkspaceTemplate:
    """A reproducible, bounded multi-file workspace attached to one laboratory."""

    workspace_id: str
    lab_id: str
    version: str
    files: tuple[WorkspaceFileTemplate, ...]
    entrypoint: str
    test_entrypoint: str
    allowed_import_roots: frozenset[str]
    timeout_seconds: float = 12.0
    output_limit: int = 32_000

    def __post_init__(self) -> None:
        for field_name, value in (
            ("workspace_id", self.workspace_id),
            ("lab_id", self.lab_id),
            ("version", self.version),
        ):
            if not value.strip():
                raise WorkspaceDefinitionError(
                    f"Scientific workspace {field_name} cannot be blank."
                )
        if not self.files:
            raise WorkspaceDefinitionError("Scientific workspaces require authored files.")
        paths = tuple(item.relative_path for item in self.files)
        if len(paths) != len(set(paths)):
            raise WorkspaceDefinitionError("Scientific workspace file paths must be unique.")
        entrypoint = normalize_workspace_path(self.entrypoint)
        test_entrypoint = normalize_workspace_path(self.test_entrypoint)
        by_path = {item.relative_path: item for item in self.files}
        if entrypoint not in by_path or by_path[entrypoint].role is not WorkspaceFileRole.SOURCE:
            raise WorkspaceDefinitionError(
                "Workspace entrypoint must reference an authored source file."
            )
        if not by_path[entrypoint].editable:
            raise WorkspaceDefinitionError("Workspace entrypoint must be learner editable.")
        if (
            test_entrypoint not in by_path
            or by_path[test_entrypoint].role is not WorkspaceFileRole.TEST
        ):
            raise WorkspaceDefinitionError(
                "Workspace test entrypoint must reference an authored test file."
            )
        if any(
            not root.strip() or "." in root or "/" in root for root in self.allowed_import_roots
        ):
            raise WorkspaceDefinitionError(
                "Allowed import roots must be plain top-level module names."
            )
        if not 0.5 <= self.timeout_seconds <= 60.0:
            raise WorkspaceDefinitionError("Workspace timeout must be between 0.5 and 60 seconds.")
        if not 1_024 <= self.output_limit <= MAX_WORKSPACE_OUTPUT_CHARS:
            raise WorkspaceDefinitionError(
                f"Workspace output limit must be between 1024 and {MAX_WORKSPACE_OUTPUT_CHARS}."
            )
        object.__setattr__(self, "entrypoint", entrypoint)
        object.__setattr__(self, "test_entrypoint", test_entrypoint)
        object.__setattr__(self, "allowed_import_roots", frozenset(self.allowed_import_roots))

    def file(self, relative_path: str) -> WorkspaceFileTemplate:
        """Return one authored file by normalized relative path."""

        normalized = normalize_workspace_path(relative_path)
        try:
            return next(item for item in self.files if item.relative_path == normalized)
        except StopIteration as exc:
            raise WorkspaceDefinitionError(f"Unknown workspace file {normalized!r}.") from exc

    @property
    def editable_files(self) -> tuple[WorkspaceFileTemplate, ...]:
        """Return learner-owned files in authored display order."""

        return tuple(item for item in self.files if item.editable)


@dataclass(frozen=True, slots=True)
class WorkspaceExecutionResult:
    """Normalized evidence from one controlled workspace execution."""

    mode: WorkspaceExecutionMode
    status: WorkspaceExecutionStatus
    stdout: str
    stderr: str
    duration_ms: int
    return_code: int | None

    def __post_init__(self) -> None:
        if self.duration_ms < 0:
            raise ValueError("Workspace execution duration cannot be negative.")
        if len(self.stdout) > MAX_WORKSPACE_OUTPUT_CHARS:
            raise ValueError("Workspace stdout exceeds the normalized storage limit.")
        if len(self.stderr) > MAX_WORKSPACE_OUTPUT_CHARS:
            raise ValueError("Workspace stderr exceeds the normalized storage limit.")

    def render(self) -> str:
        """Return a stable plain-text execution record for display and mentoring."""

        lines = [
            f"mode: {self.mode.value}",
            f"status: {self.status.value}",
            f"duration_ms: {self.duration_ms}",
        ]
        if self.return_code is not None:
            lines.append(f"return_code: {self.return_code}")
        if self.stdout:
            lines.extend(("stdout:", self.stdout.rstrip()))
        if self.stderr:
            lines.extend(("stderr:", self.stderr.rstrip()))
        return "\n".join(lines)


def normalize_workspace_path(value: str) -> str:
    """Normalize and validate one portable path confined to a workspace root."""

    stripped = value.strip().replace("\\", "/")
    if not stripped:
        raise WorkspaceDefinitionError("Workspace paths cannot be blank.")
    path = PurePosixPath(stripped)
    if path.is_absolute() or path.anchor or ".." in path.parts:
        raise WorkspaceDefinitionError("Workspace paths must remain inside the workspace root.")
    if any(part in {"", "."} for part in path.parts):
        raise WorkspaceDefinitionError(
            "Workspace paths must not contain empty or current segments."
        )
    normalized = path.as_posix()
    if len(normalized) > 240:
        raise WorkspaceDefinitionError("Workspace paths cannot exceed 240 characters.")
    return normalized


__all__ = [
    "MAX_WORKSPACE_FILE_BYTES",
    "MAX_WORKSPACE_OUTPUT_CHARS",
    "ScientificWorkspaceTemplate",
    "WorkspaceDefinitionError",
    "WorkspaceExecutionMode",
    "WorkspaceExecutionResult",
    "WorkspaceExecutionStatus",
    "WorkspaceFileRole",
    "WorkspaceFileTemplate",
    "normalize_workspace_path",
]
