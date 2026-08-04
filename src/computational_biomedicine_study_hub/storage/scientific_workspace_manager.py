"""Filesystem service for bounded, persistent scientific laboratory workspaces."""

from __future__ import annotations

import hashlib
import json
import tempfile
from pathlib import Path

from ..learning.scientific_workspace import (
    ScientificWorkspaceTemplate,
    WorkspaceDefinitionError,
    WorkspaceFileTemplate,
    normalize_workspace_path,
)
from .sqlite_progress_store import SQLiteProgressStore

_MANIFEST_NAME = ".workspace-manifest.json"


class ScientificWorkspaceManager:
    """Materialize authored files and protect all access inside one workspace root."""

    def __init__(self, root: str | Path) -> None:
        self._root = Path(root).expanduser().resolve()
        self._root.mkdir(parents=True, exist_ok=True)

    @classmethod
    def for_progress_store(
        cls,
        progress_store: SQLiteProgressStore,
    ) -> ScientificWorkspaceManager:
        """Place durable workspaces beside file-backed progress or in a temp root for tests."""

        if progress_store.database == ":memory:":
            root = Path(tempfile.mkdtemp(prefix="cb-study-workspaces-"))
        else:
            root = Path(f"{progress_store.database}.workspaces")
        return cls(root)

    @property
    def root(self) -> Path:
        """Return the application-owned workspace root."""

        return self._root

    def materialize(self, template: ScientificWorkspaceTemplate) -> Path:
        """Create missing files, refresh immutable authored files, and preserve learner edits."""

        workspace = self.workspace_path(template)
        workspace.mkdir(parents=True, exist_ok=True)
        for file_template in template.files:
            path = self._resolved_file(template, file_template.relative_path)
            path.parent.mkdir(parents=True, exist_ok=True)
            if file_template.editable and path.exists():
                continue
            self._atomic_write(path, file_template.content)
        output = workspace / "output"
        output.mkdir(parents=True, exist_ok=True)
        self._atomic_write(
            workspace / _MANIFEST_NAME,
            json.dumps(
                {
                    "workspace_id": template.workspace_id,
                    "lab_id": template.lab_id,
                    "version": template.version,
                    "files": {
                        item.relative_path: {
                            "role": item.role.value,
                            "editable": item.editable,
                            "authored_sha256": _sha256(item.content),
                        }
                        for item in template.files
                    },
                },
                ensure_ascii=False,
                indent=2,
                sort_keys=True,
            ),
        )
        return workspace

    def workspace_path(self, template: ScientificWorkspaceTemplate) -> Path:
        """Return one deterministic application-owned workspace directory."""

        safe_name = template.workspace_id.replace(".", "_").replace("/", "_")
        if not safe_name or safe_name in {".", ".."}:
            raise WorkspaceDefinitionError("Workspace identity cannot produce an empty directory.")
        resolved = (self._root / safe_name).resolve()
        self._require_within_root(resolved)
        return resolved

    def read_text(self, template: ScientificWorkspaceTemplate, relative_path: str) -> str:
        """Read one authored text file after materializing the workspace."""

        self.materialize(template)
        path = self._resolved_file(template, relative_path)
        try:
            return path.read_text(encoding="utf-8")
        except OSError as exc:
            raise WorkspaceDefinitionError(
                f"Unable to read workspace file {relative_path!r}."
            ) from exc

    def write_text(
        self,
        template: ScientificWorkspaceTemplate,
        relative_path: str,
        content: str,
    ) -> Path:
        """Atomically replace one learner-editable authored file."""

        file_template = template.file(relative_path)
        if not file_template.editable:
            raise WorkspaceDefinitionError(
                f"Workspace file {file_template.relative_path!r} is authored and read-only."
            )
        if len(content.encode("utf-8")) > 1_000_000:
            raise WorkspaceDefinitionError("Workspace file content exceeds the local size limit.")
        self.materialize(template)
        path = self._resolved_file(template, file_template.relative_path)
        self._atomic_write(path, content)
        return path

    def write_execution_record(
        self,
        template: ScientificWorkspaceTemplate,
        name: str,
        content: str,
    ) -> Path:
        """Write a generated execution record inside the reserved output directory."""

        normalized = normalize_workspace_path(f"output/{name}")
        if not normalized.startswith("output/"):
            raise WorkspaceDefinitionError("Execution records must remain in output/.")
        self.materialize(template)
        path = (self.workspace_path(template) / normalized).resolve()
        self._require_workspace_path(template, path)
        path.parent.mkdir(parents=True, exist_ok=True)
        self._atomic_write(path, content)
        return path

    def authored_paths(self, template: ScientificWorkspaceTemplate) -> tuple[str, ...]:
        """Return authored files in display order."""

        return tuple(item.relative_path for item in template.files)

    def editable_paths(self, template: ScientificWorkspaceTemplate) -> tuple[str, ...]:
        """Return learner-editable authored files in display order."""

        return tuple(item.relative_path for item in template.editable_files)

    def file_template(
        self,
        template: ScientificWorkspaceTemplate,
        relative_path: str,
    ) -> WorkspaceFileTemplate:
        """Return metadata for one authored file."""

        return template.file(relative_path)

    def _resolved_file(
        self,
        template: ScientificWorkspaceTemplate,
        relative_path: str,
    ) -> Path:
        normalized = template.file(relative_path).relative_path
        path = (self.workspace_path(template) / normalized).resolve()
        self._require_workspace_path(template, path)
        return path

    def _require_workspace_path(
        self,
        template: ScientificWorkspaceTemplate,
        path: Path,
    ) -> None:
        workspace = self.workspace_path(template)
        try:
            path.relative_to(workspace)
        except ValueError as exc:
            raise WorkspaceDefinitionError("Workspace path escaped its laboratory root.") from exc

    def _require_within_root(self, path: Path) -> None:
        try:
            path.relative_to(self._root)
        except ValueError as exc:
            raise WorkspaceDefinitionError("Workspace path escaped the application root.") from exc

    @staticmethod
    def _atomic_write(path: Path, content: str) -> None:
        temporary = path.with_name(f"{path.name}.tmp")
        temporary.write_text(content, encoding="utf-8")
        temporary.replace(path)


def _sha256(content: str) -> str:
    return hashlib.sha256(content.encode("utf-8")).hexdigest()


__all__ = ["ScientificWorkspaceManager"]
