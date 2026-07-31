"""Restricted local execution for short educational Python examples."""

from __future__ import annotations

import ast
import json
import os
import subprocess
import sys
import tempfile
from dataclasses import dataclass
from enum import StrEnum
from pathlib import Path
from time import monotonic
from typing import Final, Protocol

_DEFAULT_TIMEOUT_SECONDS: Final = 2.0
_DEFAULT_OUTPUT_LIMIT: Final = 16_000
_MAX_SOURCE_LENGTH: Final = 20_000
_ALLOWED_IMPORT_ROOTS: Final = frozenset(
    {
        "bisect",
        "collections",
        "dataclasses",
        "decimal",
        "enum",
        "fractions",
        "functools",
        "heapq",
        "itertools",
        "math",
        "random",
        "re",
        "statistics",
        "string",
        "typing",
    }
)
_BLOCKED_CALLS: Final = frozenset(
    {
        "breakpoint",
        "compile",
        "delattr",
        "dir",
        "eval",
        "exec",
        "exit",
        "getattr",
        "globals",
        "help",
        "input",
        "locals",
        "open",
        "quit",
        "setattr",
        "vars",
        "__import__",
    }
)

_HARNESS = r'''
import builtins
import contextlib
import io
import json
import sys
import traceback

source_path = sys.argv[1]
limit = int(sys.argv[2])
allowed_imports = frozenset(sys.argv[3].split(","))

class OutputLimitExceeded(RuntimeError):
    pass

class LimitedBuffer(io.StringIO):
    def __init__(self, maximum):
        super().__init__()
        self.maximum = maximum

    def write(self, value):
        text = str(value)
        remaining = self.maximum - len(self.getvalue())
        if remaining <= 0:
            raise OutputLimitExceeded()
        if len(text) > remaining:
            super().write(text[:remaining])
            raise OutputLimitExceeded()
        return super().write(text)

real_import = builtins.__import__

def safe_import(name, globals=None, locals=None, fromlist=(), level=0):
    root = name.split(".", 1)[0]
    if level != 0 or root not in allowed_imports:
        raise ImportError(f"Import {name!r} is not allowed in this learning lab.")
    return real_import(name, globals, locals, fromlist, level)

safe_names = (
    "ArithmeticError", "AssertionError", "AttributeError", "BaseException",
    "Exception", "IndexError", "KeyError", "LookupError", "NameError",
    "NotImplementedError", "OverflowError", "RuntimeError", "StopIteration",
    "SyntaxError", "TypeError", "ValueError", "ZeroDivisionError",
    "abs", "all", "any", "bin", "bool", "bytearray", "bytes", "callable",
    "chr", "classmethod", "complex", "dict", "divmod", "enumerate", "filter",
    "float", "format", "frozenset", "hash", "hex", "int", "isinstance",
    "issubclass", "iter", "len", "list", "map", "max", "min", "next",
    "object", "oct", "ord", "pow", "print", "property", "range", "repr",
    "reversed", "round", "set", "slice", "sorted", "staticmethod", "str",
    "sum", "super", "tuple", "type", "zip", "__build_class__"
)
safe_builtins = {name: getattr(builtins, name) for name in safe_names}
safe_builtins["__import__"] = safe_import
namespace = {
    "__builtins__": safe_builtins,
    "__name__": "__main__",
}
stdout = LimitedBuffer(limit)
stderr = LimitedBuffer(limit)
status = "ok"

try:
    with open(source_path, "r", encoding="utf-8") as handle:
        source = handle.read()
    with contextlib.redirect_stdout(stdout), contextlib.redirect_stderr(stderr):
        exec(compile(source, "<learning-lab>", "exec"), namespace, namespace)
except OutputLimitExceeded:
    status = "output_limit"
except BaseException:
    status = "runtime_error"
    try:
        traceback.print_exc(file=stderr)
    except OutputLimitExceeded:
        pass

payload = {
    "status": status,
    "stdout": stdout.getvalue(),
    "stderr": stderr.getvalue(),
}
sys.__stdout__.write(json.dumps(payload, ensure_ascii=False))
'''


class ExecutionStatus(StrEnum):
    """Final state of one local Python execution."""

    PASSED = "passed"
    OUTPUT_MISMATCH = "output_mismatch"
    RUNTIME_ERROR = "runtime_error"
    TIMED_OUT = "timed_out"
    REJECTED = "rejected"
    OUTPUT_LIMIT = "output_limit"


@dataclass(frozen=True, slots=True)
class PythonExecutionRequest:
    """One short source submission and its authored expected output."""

    source: str
    expected_output: str | None = None
    timeout_seconds: float = _DEFAULT_TIMEOUT_SECONDS
    output_limit: int = _DEFAULT_OUTPUT_LIMIT

    def __post_init__(self) -> None:
        if not self.source.strip():
            raise ValueError("Python source cannot be empty.")
        if len(self.source) > _MAX_SOURCE_LENGTH:
            raise ValueError(f"Python source cannot exceed {_MAX_SOURCE_LENGTH} characters.")
        if not 0.1 <= self.timeout_seconds <= 10.0:
            raise ValueError("timeout_seconds must be between 0.1 and 10.0.")
        if not 256 <= self.output_limit <= 65_536:
            raise ValueError("output_limit must be between 256 and 65536 characters.")


@dataclass(frozen=True, slots=True)
class PythonExecutionResult:
    """Normalized result returned by the restricted subprocess."""

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


class PythonCodeRunner(Protocol):
    """Interface consumed by the Python lab widget."""

    def run(self, request: PythonExecutionRequest) -> PythonExecutionResult:
        """Execute one request and return a normalized result."""


class PythonPolicyError(ValueError):
    """Raised when code requests capabilities outside the learning-lab policy."""


class _PolicyVisitor(ast.NodeVisitor):
    def visit_Import(self, node: ast.Import) -> None:  # noqa: N802
        for alias in node.names:
            self._require_allowed_import(alias.name)
        self.generic_visit(node)

    def visit_ImportFrom(self, node: ast.ImportFrom) -> None:  # noqa: N802
        if node.level != 0 or node.module is None:
            raise PythonPolicyError("Relative imports are not allowed in learning labs.")
        self._require_allowed_import(node.module)
        self.generic_visit(node)

    def visit_Call(self, node: ast.Call) -> None:  # noqa: N802
        if isinstance(node.func, ast.Name) and node.func.id in _BLOCKED_CALLS:
            raise PythonPolicyError(
                f"Calling {node.func.id!r} is not allowed in learning labs."
            )
        self.generic_visit(node)

    def visit_Attribute(self, node: ast.Attribute) -> None:  # noqa: N802
        if node.attr.startswith("_"):
            raise PythonPolicyError("Private and dunder attribute access is not allowed.")
        self.generic_visit(node)

    @staticmethod
    def _require_allowed_import(name: str) -> None:
        root = name.split(".", 1)[0]
        if root not in _ALLOWED_IMPORT_ROOTS:
            raise PythonPolicyError(
                f"Import {name!r} is not available in the restricted learning lab."
            )


def validate_python_source(source: str) -> None:
    """Validate syntax and reject file, network and process capabilities."""

    if not source.strip():
        raise PythonPolicyError("Python source cannot be empty.")
    if len(source) > _MAX_SOURCE_LENGTH:
        raise PythonPolicyError(f"Python source cannot exceed {_MAX_SOURCE_LENGTH} characters.")
    try:
        tree = ast.parse(source, mode="exec")
    except SyntaxError as exc:
        detail = exc.msg or "invalid syntax"
        raise PythonPolicyError(f"Syntax error: {detail}.") from exc
    _PolicyVisitor().visit(tree)


def can_execute_python(source: str) -> bool:
    """Return whether source satisfies the first local execution policy."""

    try:
        validate_python_source(source)
    except PythonPolicyError:
        return False
    return True


def normalize_output(value: str) -> str:
    """Normalize terminal whitespace without altering content inside each line."""

    return "\n".join(line.rstrip() for line in value.strip().splitlines())


class PythonSubprocessRunner:
    """Run validated code in an isolated interpreter and temporary directory."""

    def __init__(self, executable: str | Path | None = None) -> None:
        self._executable = str(executable or sys.executable)

    def run(self, request: PythonExecutionRequest) -> PythonExecutionResult:
        started = monotonic()
        try:
            validate_python_source(request.source)
        except PythonPolicyError as exc:
            return self._result(
                ExecutionStatus.REJECTED,
                stdout="",
                stderr=str(exc),
                started=started,
                expected_output=request.expected_output,
            )

        with tempfile.TemporaryDirectory(prefix="cb-study-lab-") as directory:
            source_path = Path(directory) / "source.py"
            source_path.write_text(request.source, encoding="utf-8")
            command = [
                self._executable,
                "-I",
                "-S",
                "-c",
                _HARNESS,
                str(source_path),
                str(request.output_limit),
                ",".join(sorted(_ALLOWED_IMPORT_ROOTS)),
            ]
            creation_flags = (
                int(getattr(subprocess, "CREATE_NO_WINDOW", 0)) if os.name == "nt" else 0
            )
            try:
                completed = subprocess.run(
                    command,
                    cwd=directory,
                    stdin=subprocess.DEVNULL,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                    text=True,
                    encoding="utf-8",
                    errors="replace",
                    timeout=request.timeout_seconds,
                    check=False,
                    env=self._subprocess_environment(),
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
                    stderr=f"Unable to start the Python interpreter: {exc}",
                    started=started,
                    expected_output=request.expected_output,
                )

        try:
            payload = json.loads(completed.stdout)
        except json.JSONDecodeError:
            detail = completed.stderr or completed.stdout or "The execution harness returned no data."
            return self._result(
                ExecutionStatus.RUNTIME_ERROR,
                stdout="",
                stderr=detail,
                started=started,
                expected_output=request.expected_output,
            )

        stdout = str(payload.get("stdout", ""))
        stderr = str(payload.get("stderr", ""))
        harness_status = str(payload.get("status", "runtime_error"))
        if harness_status == "output_limit":
            status = ExecutionStatus.OUTPUT_LIMIT
        elif harness_status != "ok" or completed.returncode != 0:
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
    def _subprocess_environment() -> dict[str, str]:
        environment = {
            key: value
            for key in ("SYSTEMROOT", "WINDIR", "TEMP", "TMP")
            if (value := os.environ.get(key)) is not None
        }
        environment.update({"PYTHONIOENCODING": "utf-8", "PYTHONUTF8": "1"})
        return environment

    @staticmethod
    def _result(
        status: ExecutionStatus,
        *,
        stdout: str,
        stderr: str,
        started: float,
        expected_output: str | None,
    ) -> PythonExecutionResult:
        return PythonExecutionResult(
            status=status,
            stdout=stdout,
            stderr=stderr,
            duration_ms=max(0, round((monotonic() - started) * 1000)),
            expected_output=expected_output,
        )


__all__ = [
    "ExecutionStatus",
    "PythonCodeRunner",
    "PythonExecutionRequest",
    "PythonExecutionResult",
    "PythonPolicyError",
    "PythonSubprocessRunner",
    "can_execute_python",
    "normalize_output",
    "validate_python_source",
]
