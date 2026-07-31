"""Conservative local execution for short educational R examples."""

from __future__ import annotations

import os
import re
import shutil
import subprocess
import tempfile
from dataclasses import dataclass
from pathlib import Path
from time import monotonic
from typing import Final, Protocol

from .python_execution import ExecutionStatus, normalize_output

_DEFAULT_TIMEOUT_SECONDS: Final = 3.0
_DEFAULT_OUTPUT_LIMIT: Final = 16_000
_MAX_SOURCE_LENGTH: Final = 20_000

_FORBIDDEN_CALLS: Final = (
    "system",
    "system2",
    "shell",
    "pipe",
    "fifo",
    "socketConnection",
    "url",
    "download.file",
    "file",
    "gzfile",
    "bzfile",
    "xzfile",
    "unz",
    "readLines",
    "writeLines",
    "source",
    "setwd",
    "getwd",
    "dir",
    "list.files",
    "unlink",
    "file.remove",
    "file.rename",
    "file.copy",
    "dir.create",
    "install.packages",
    "library",
    "require",
    "dyn.load",
    "dyn.unload",
    "Sys.getenv",
    "Sys.setenv",
    "Sys.info",
    "Sys.sleep",
    "eval",
    "parse",
    "get",
    "assign",
    "do.call",
    "load",
    "save",
    "saveRDS",
    "readRDS",
    "serialize",
    "unserialize",
    "quit",
    "q",
    "options",
    "trace",
    "debug",
    "browser",
    "globalenv",
    "parent.frame",
    "environment",
    "as.environment",
    "unlockBinding",
    "makeActiveBinding",
)
_FORBIDDEN_PATTERN: Final = re.compile(
    r"(?i)\b(?:" + "|".join(re.escape(name) for name in _FORBIDDEN_CALLS) + r")\s*\("
)
_NATIVE_PATTERN: Final = re.compile(r"(?i)\.(?:Internal|Call|C|External)\s*\(")


class RPolicyError(ValueError):
    """Raised when R source requests capabilities outside the learning-lab policy."""


@dataclass(frozen=True, slots=True)
class RExecutionRequest:
    """One short R submission and its authored expected output."""

    source: str
    expected_output: str | None = None
    timeout_seconds: float = _DEFAULT_TIMEOUT_SECONDS
    output_limit: int = _DEFAULT_OUTPUT_LIMIT

    def __post_init__(self) -> None:
        if not self.source.strip():
            raise ValueError("R source cannot be empty.")
        if len(self.source) > _MAX_SOURCE_LENGTH:
            raise ValueError(f"R source cannot exceed {_MAX_SOURCE_LENGTH} characters.")
        if not 0.1 <= self.timeout_seconds <= 15.0:
            raise ValueError("timeout_seconds must be between 0.1 and 15.0.")
        if not 256 <= self.output_limit <= 65_536:
            raise ValueError("output_limit must be between 256 and 65536 characters.")


@dataclass(frozen=True, slots=True)
class RExecutionResult:
    """Normalized result returned by the local R subprocess."""

    status: ExecutionStatus
    stdout: str
    stderr: str
    duration_ms: int
    expected_output: str | None

    @property
    def output_matches(self) -> bool | None:
        """Return output agreement when an expected result was supplied."""

        if self.expected_output is None:
            return None
        return normalize_output(self.stdout) == normalize_output(self.expected_output)


class RCodeRunner(Protocol):
    """Interface consumed by the R lab widget."""

    def run(self, request: RExecutionRequest) -> RExecutionResult:
        """Execute one request and return a normalized result."""


def _policy_view(source: str) -> str:
    """Remove comments and string contents before conservative token checks."""

    result: list[str] = []
    quote: str | None = None
    escaped = False
    in_comment = False

    for character in source:
        if in_comment:
            if character == "\n":
                in_comment = False
                result.append(character)
            else:
                result.append(" ")
            continue

        if quote is not None:
            if escaped:
                escaped = False
            elif character == "\\":
                escaped = True
            elif character == quote:
                quote = None
            result.append(" ")
            continue

        if character in {'"', "'"}:
            quote = character
            result.append(" ")
        elif character == "#":
            in_comment = True
            result.append(" ")
        else:
            result.append(character)

    return "".join(result)


def validate_r_source(source: str) -> None:
    """Reject file, network, package-installation and process capabilities."""

    if not source.strip():
        raise RPolicyError("R source cannot be empty.")
    if len(source) > _MAX_SOURCE_LENGTH:
        raise RPolicyError(f"R source cannot exceed {_MAX_SOURCE_LENGTH} characters.")

    view = _policy_view(source)
    if "`" in view:
        raise RPolicyError("Backtick-based function lookup is not allowed in learning labs.")
    if "::" in view or ":::" in view:
        raise RPolicyError("Namespace access is not allowed in learning labs.")
    if _FORBIDDEN_PATTERN.search(view):
        raise RPolicyError(
            "The R source requests a blocked file, network, package or process capability."
        )
    if _NATIVE_PATTERN.search(view):
        raise RPolicyError("Native-code entry points are not allowed in learning labs.")


def can_execute_r(source: str) -> bool:
    """Return whether source satisfies the conservative local R policy."""

    try:
        validate_r_source(source)
    except RPolicyError:
        return False
    return True


def find_rscript() -> str | None:
    """Return the available Rscript executable, if one is on PATH."""

    return shutil.which("Rscript") or shutil.which("Rscript.exe")


class RSubprocessRunner:
    """Run validated R code with --vanilla in a temporary working directory."""

    def __init__(self, executable: str | Path | None = None) -> None:
        self._executable = str(executable) if executable is not None else find_rscript()

    @property
    def available(self) -> bool:
        """Return whether an Rscript executable was resolved."""

        return self._executable is not None

    def run(self, request: RExecutionRequest) -> RExecutionResult:
        started = monotonic()
        try:
            validate_r_source(request.source)
        except RPolicyError as exc:
            return self._result(
                ExecutionStatus.REJECTED,
                stdout="",
                stderr=str(exc),
                started=started,
                expected_output=request.expected_output,
            )

        if self._executable is None:
            return self._result(
                ExecutionStatus.RUNTIME_ERROR,
                stdout="",
                stderr=(
                    "Rscript was not found. Install R and ensure Rscript is available on PATH."
                ),
                started=started,
                expected_output=request.expected_output,
            )

        with tempfile.TemporaryDirectory(prefix="cb-study-r-lab-") as directory:
            source_path = Path(directory) / "source.R"
            source_path.write_text(request.source, encoding="utf-8")
            creation_flags = (
                int(getattr(subprocess, "CREATE_NO_WINDOW", 0)) if os.name == "nt" else 0
            )
            try:
                completed = subprocess.run(
                    [self._executable, "--vanilla", str(source_path)],
                    cwd=directory,
                    stdin=subprocess.DEVNULL,
                    capture_output=True,
                    text=True,
                    encoding="utf-8",
                    errors="replace",
                    timeout=request.timeout_seconds,
                    check=False,
                    env=self._subprocess_environment(directory),
                    creationflags=creation_flags,
                )
            except subprocess.TimeoutExpired:
                return self._result(
                    ExecutionStatus.TIMED_OUT,
                    stdout="",
                    stderr="Execution exceeded the configured time limit.",
                    started=started,
                    expected_output=request.expected_output,
                )
            except OSError as exc:
                return self._result(
                    ExecutionStatus.RUNTIME_ERROR,
                    stdout="",
                    stderr=f"Unable to start Rscript: {exc}",
                    started=started,
                    expected_output=request.expected_output,
                )

        stdout = completed.stdout
        stderr = completed.stderr
        if len(stdout) + len(stderr) > request.output_limit:
            remaining = request.output_limit
            stdout = stdout[:remaining]
            remaining -= len(stdout)
            stderr = stderr[: max(0, remaining)]
            status = ExecutionStatus.OUTPUT_LIMIT
        elif completed.returncode != 0:
            status = ExecutionStatus.RUNTIME_ERROR
        elif request.expected_output is None:
            status = ExecutionStatus.PASSED
        elif normalize_output(stdout) == normalize_output(request.expected_output):
            status = ExecutionStatus.PASSED
        else:
            status = ExecutionStatus.OUTPUT_MISMATCH

        return self._result(
            status,
            stdout=stdout,
            stderr=stderr,
            started=started,
            expected_output=request.expected_output,
        )

    @staticmethod
    def _subprocess_environment(directory: str) -> dict[str, str]:
        null_device = "NUL" if os.name == "nt" else "/dev/null"
        environment = {
            key: value
            for key in ("SYSTEMROOT", "WINDIR", "PATH")
            if (value := os.environ.get(key)) is not None
        }
        environment.update(
            {
                "HOME": directory,
                "R_USER": directory,
                "R_ENVIRON_USER": null_device,
                "R_PROFILE_USER": null_device,
                "TEMP": directory,
                "TMP": directory,
            }
        )
        return environment

    @staticmethod
    def _result(
        status: ExecutionStatus,
        *,
        stdout: str,
        stderr: str,
        started: float,
        expected_output: str | None,
    ) -> RExecutionResult:
        return RExecutionResult(
            status=status,
            stdout=stdout,
            stderr=stderr,
            duration_ms=max(0, round((monotonic() - started) * 1000)),
            expected_output=expected_output,
        )


__all__ = [
    "RCodeRunner",
    "RExecutionRequest",
    "RExecutionResult",
    "RPolicyError",
    "RSubprocessRunner",
    "can_execute_r",
    "find_rscript",
    "validate_r_source",
]
