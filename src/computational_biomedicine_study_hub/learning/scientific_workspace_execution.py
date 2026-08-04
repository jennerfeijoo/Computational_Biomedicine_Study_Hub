"""Controlled local execution for authored multi-file scientific workspaces."""

from __future__ import annotations

import ast
import os
import subprocess
import sys
from pathlib import Path
from time import monotonic
from typing import Final, Protocol

from .scientific_workspace import (
    ScientificWorkspaceTemplate,
    WorkspaceDefinitionError,
    WorkspaceExecutionMode,
    WorkspaceExecutionResult,
    WorkspaceExecutionStatus,
)

_BLOCKED_IMPORT_ROOTS: Final = frozenset(
    {
        "asyncio",
        "ctypes",
        "ftplib",
        "http",
        "importlib",
        "multiprocessing",
        "os",
        "requests",
        "shutil",
        "socket",
        "subprocess",
        "telnetlib",
        "urllib",
        "webbrowser",
    }
)
_BLOCKED_CALLS: Final = frozenset(
    {
        "breakpoint",
        "compile",
        "eval",
        "exec",
        "exit",
        "help",
        "input",
        "quit",
        "__import__",
    }
)
_HARNESS: Final = r"""
import builtins
import io
import pathlib
import runpy
import socket
import sys
import traceback

workspace = pathlib.Path(sys.argv[1]).resolve()
target = pathlib.Path(sys.argv[2]).resolve()

class WorkspaceAccessError(PermissionError):
    pass

def _path_from(value):
    if isinstance(value, int):
        return None
    return pathlib.Path(value).expanduser().resolve()

def _write_mode(mode):
    return any(flag in mode for flag in ("w", "a", "x", "+"))

def _guarded_open(file, mode="r", *args, **kwargs):
    path = _path_from(file)
    if path is not None and _write_mode(str(mode)):
        try:
            path.relative_to(workspace)
        except ValueError as exc:
            raise WorkspaceAccessError("Writing outside the laboratory workspace is blocked.") from exc
    return _real_open(file, mode, *args, **kwargs)

def _blocked_socket(*args, **kwargs):
    raise WorkspaceAccessError("Network access is blocked in laboratory workspaces.")

_real_open = builtins.open
builtins.open = _guarded_open
io.open = _guarded_open
socket.socket = _blocked_socket
socket.create_connection = _blocked_socket

try:
    target.relative_to(workspace)
    runpy.run_path(str(target), run_name="__main__")
except BaseException:
    traceback.print_exc(file=sys.stderr)
    raise SystemExit(1)
"""


class ScientificWorkspaceRunnerProtocol(Protocol):
    """Execution contract consumed by the workspace panel."""

    def run(
        self,
        template: ScientificWorkspaceTemplate,
        workspace_root: Path,
        mode: WorkspaceExecutionMode,
    ) -> WorkspaceExecutionResult:
        """Run the authored script or authored test entrypoint."""


class WorkspacePolicyError(ValueError):
    """Raised when learner source requests a blocked capability."""


class _WorkspacePolicyVisitor(ast.NodeVisitor):
    def __init__(self, allowed_import_roots: frozenset[str]) -> None:
        self._allowed_import_roots = allowed_import_roots

    def visit_Import(self, node: ast.Import) -> None:  # noqa: N802
        for alias in node.names:
            self._require_allowed(alias.name)
        self.generic_visit(node)

    def visit_ImportFrom(self, node: ast.ImportFrom) -> None:  # noqa: N802
        if node.level != 0 or node.module is None:
            raise WorkspacePolicyError(
                "Relative imports are not allowed in learner workspace files."
            )
        self._require_allowed(node.module)
        self.generic_visit(node)

    def visit_Call(self, node: ast.Call) -> None:  # noqa: N802
        if isinstance(node.func, ast.Name) and node.func.id in _BLOCKED_CALLS:
            raise WorkspacePolicyError(
                f"Calling {node.func.id!r} is blocked in scientific workspaces."
            )
        self.generic_visit(node)

    def _require_allowed(self, name: str) -> None:
        root = name.split(".", 1)[0]
        if root == "__future__":
            return
        if root in _BLOCKED_IMPORT_ROOTS or root not in self._allowed_import_roots:
            raise WorkspacePolicyError(
                f"Import {name!r} is not authorized for this laboratory workspace."
            )


def validate_workspace_source(
    source: str,
    *,
    allowed_import_roots: frozenset[str],
    filename: str,
) -> None:
    """Validate learner Python without claiming operating-system sandbox isolation."""

    try:
        tree = ast.parse(source, filename=filename, mode="exec")
    except SyntaxError as exc:
        raise WorkspacePolicyError(f"Syntax error in {filename}: {exc.msg}.") from exc
    _WorkspacePolicyVisitor(allowed_import_roots).visit(tree)


class ScientificWorkspaceRunner:
    """Run exact authored entrypoints without a shell, network, or installation commands."""

    def __init__(self, executable: str | Path | None = None) -> None:
        self._executable = str(executable or sys.executable)

    def run(
        self,
        template: ScientificWorkspaceTemplate,
        workspace_root: Path,
        mode: WorkspaceExecutionMode,
    ) -> WorkspaceExecutionResult:
        started = monotonic()
        workspace = workspace_root.expanduser().resolve()
        target_relative = (
            template.entrypoint if mode is WorkspaceExecutionMode.RUN else template.test_entrypoint
        )
        target = (workspace / target_relative).resolve()
        try:
            target.relative_to(workspace)
        except ValueError:
            return self._result(
                mode,
                WorkspaceExecutionStatus.REJECTED,
                "",
                "Authored execution target escaped the workspace root.",
                started,
                None,
            )
        if not target.is_file():
            return self._result(
                mode,
                WorkspaceExecutionStatus.REJECTED,
                "",
                f"Execution target {target_relative!r} does not exist.",
                started,
                None,
            )

        try:
            self._validate_learner_files(template, workspace)
        except (OSError, UnicodeError, WorkspacePolicyError, WorkspaceDefinitionError) as exc:
            return self._result(
                mode,
                WorkspaceExecutionStatus.REJECTED,
                "",
                str(exc),
                started,
                None,
            )

        command = [
            self._executable,
            "-I",
            "-c",
            _HARNESS,
            str(workspace),
            str(target),
        ]
        creation_flags = int(getattr(subprocess, "CREATE_NO_WINDOW", 0)) if os.name == "nt" else 0
        try:
            completed = subprocess.run(
                command,
                cwd=workspace,
                stdin=subprocess.DEVNULL,
                capture_output=True,
                text=True,
                encoding="utf-8",
                errors="replace",
                timeout=template.timeout_seconds,
                check=False,
                env=self._environment(),
                creationflags=creation_flags,
            )
        except subprocess.TimeoutExpired as exc:
            stdout = _bounded_text(exc.stdout, template.output_limit)
            stderr = _bounded_text(exc.stderr, template.output_limit)
            return self._result(
                mode,
                WorkspaceExecutionStatus.TIMED_OUT,
                stdout,
                stderr or "Execution exceeded the laboratory time limit.",
                started,
                None,
            )
        except OSError as exc:
            return self._result(
                mode,
                WorkspaceExecutionStatus.RUNTIME_ERROR,
                "",
                f"Unable to start the Python interpreter: {exc}",
                started,
                None,
            )

        stdout = _bounded_text(completed.stdout, template.output_limit)
        stderr = _bounded_text(completed.stderr, template.output_limit)
        if (
            len(completed.stdout) > template.output_limit
            or len(completed.stderr) > template.output_limit
        ):
            status = WorkspaceExecutionStatus.OUTPUT_LIMIT
        elif completed.returncode == 0:
            status = WorkspaceExecutionStatus.PASSED
        elif "ModuleNotFoundError" in stderr or "No module named" in stderr:
            status = WorkspaceExecutionStatus.MISSING_DEPENDENCY
        else:
            status = WorkspaceExecutionStatus.FAILED
        return self._result(mode, status, stdout, stderr, started, completed.returncode)

    @staticmethod
    def _validate_learner_files(
        template: ScientificWorkspaceTemplate,
        workspace: Path,
    ) -> None:
        for file_template in template.editable_files:
            if not file_template.relative_path.endswith(".py"):
                continue
            path = (workspace / file_template.relative_path).resolve()
            try:
                path.relative_to(workspace)
            except ValueError as exc:
                raise WorkspacePolicyError("Learner file escaped the workspace root.") from exc
            validate_workspace_source(
                path.read_text(encoding="utf-8"),
                allowed_import_roots=template.allowed_import_roots,
                filename=file_template.relative_path,
            )

    @staticmethod
    def _environment() -> dict[str, str]:
        environment = {
            key: value
            for key in ("SYSTEMROOT", "WINDIR", "TEMP", "TMP", "PATH")
            if (value := os.environ.get(key)) is not None
        }
        environment.update(
            {
                "PYTHONIOENCODING": "utf-8",
                "PYTHONUTF8": "1",
                "PYTHONDONTWRITEBYTECODE": "1",
                "HTTP_PROXY": "",
                "HTTPS_PROXY": "",
                "ALL_PROXY": "",
                "NO_PROXY": "*",
            }
        )
        return environment

    @staticmethod
    def _result(
        mode: WorkspaceExecutionMode,
        status: WorkspaceExecutionStatus,
        stdout: str,
        stderr: str,
        started: float,
        return_code: int | None,
    ) -> WorkspaceExecutionResult:
        return WorkspaceExecutionResult(
            mode=mode,
            status=status,
            stdout=stdout,
            stderr=stderr,
            duration_ms=max(0, round((monotonic() - started) * 1000)),
            return_code=return_code,
        )


def _bounded_text(value: str | bytes | None, limit: int) -> str:
    if value is None:
        return ""
    if isinstance(value, bytes):
        text = value.decode("utf-8", errors="replace")
    else:
        text = value
    return text[:limit]


__all__ = [
    "ScientificWorkspaceRunner",
    "ScientificWorkspaceRunnerProtocol",
    "WorkspacePolicyError",
    "validate_workspace_source",
]
