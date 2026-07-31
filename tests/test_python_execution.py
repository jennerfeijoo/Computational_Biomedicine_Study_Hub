from __future__ import annotations

import sys

import pytest

from computational_biomedicine_study_hub.learning.python_execution import (
    ExecutionStatus,
    PythonExecutionRequest,
    PythonPolicyError,
    PythonSubprocessRunner,
    can_execute_python,
    normalize_output,
    validate_python_source,
)


def test_runner_matches_authored_output() -> None:
    runner = PythonSubprocessRunner()

    result = runner.run(
        PythonExecutionRequest(
            source="sample_count = 18\nprint(sample_count + 2)",
            expected_output="20",
        )
    )

    assert result.status is ExecutionStatus.PASSED
    assert result.output_matches is True
    assert result.stdout == "20\n"
    assert result.stderr == ""
    assert result.duration_ms >= 0


def test_runner_reports_output_mismatch_without_treating_it_as_a_crash() -> None:
    result = PythonSubprocessRunner().run(
        PythonExecutionRequest(source="print(4)", expected_output="5")
    )

    assert result.status is ExecutionStatus.OUTPUT_MISMATCH
    assert result.output_matches is False
    assert result.stdout == "4\n"
    assert result.stderr == ""


def test_runner_allows_selected_standard_library_imports() -> None:
    result = PythonSubprocessRunner().run(
        PythonExecutionRequest(
            source="import math\nprint(math.sqrt(81))",
            expected_output="9.0",
        )
    )

    assert result.status is ExecutionStatus.PASSED


def test_runner_supports_functions_and_classes() -> None:
    source = (
        "class Sample:\n"
        "    def __init__(self, value):\n"
        "        self.value = value\n\n"
        "def double(sample):\n"
        "    return sample.value * 2\n\n"
        "print(double(Sample(7)))"
    )

    result = PythonSubprocessRunner().run(
        PythonExecutionRequest(source=source, expected_output="14")
    )

    assert result.status is ExecutionStatus.PASSED


def test_policy_rejects_file_process_network_and_dunder_access() -> None:
    rejected_sources = (
        "import os\nprint(os.getcwd())",
        "open('data.txt', 'w')",
        "print((1).__class__)",
        "input('value: ')",
    )

    for source in rejected_sources:
        assert not can_execute_python(source)
        result = PythonSubprocessRunner().run(PythonExecutionRequest(source=source))
        assert result.status is ExecutionStatus.REJECTED
        assert result.stderr


def test_policy_exposes_clear_syntax_errors() -> None:
    with pytest.raises(PythonPolicyError, match="Syntax error"):
        validate_python_source("for value in")


def test_runner_stops_infinite_execution() -> None:
    result = PythonSubprocessRunner().run(
        PythonExecutionRequest(
            source="while True:\n    pass",
            timeout_seconds=0.2,
        )
    )

    assert result.status is ExecutionStatus.TIMED_OUT
    assert "time limit" in result.stderr


def test_runner_caps_large_output_before_returning_to_the_ui() -> None:
    result = PythonSubprocessRunner().run(
        PythonExecutionRequest(
            source="print('x' * 5000)",
            output_limit=256,
        )
    )

    assert result.status is ExecutionStatus.OUTPUT_LIMIT
    assert len(result.stdout) == 256


def test_runtime_errors_return_traceback_without_escaping_the_runner() -> None:
    result = PythonSubprocessRunner().run(
        PythonExecutionRequest(source="1 / 0", output_limit=1024)
    )

    assert result.status is ExecutionStatus.RUNTIME_ERROR
    assert "ZeroDivisionError" in result.stderr


def test_missing_interpreter_is_reported_as_runtime_error() -> None:
    runner = PythonSubprocessRunner(executable="missing-python-interpreter-for-study-hub")

    result = runner.run(PythonExecutionRequest(source="print(1)"))

    assert result.status is ExecutionStatus.RUNTIME_ERROR
    assert "Unable to start" in result.stderr


def test_output_normalization_preserves_internal_content() -> None:
    assert normalize_output(" value  \nnext\n") == " value\nnext"


def test_request_validation_is_bounded() -> None:
    with pytest.raises(ValueError, match="cannot be empty"):
        PythonExecutionRequest(source="  ")
    with pytest.raises(ValueError, match="between 0.1 and 10.0"):
        PythonExecutionRequest(source="print(1)", timeout_seconds=0.01)
    with pytest.raises(ValueError, match="between 256 and 65536"):
        PythonExecutionRequest(source="print(1)", output_limit=100)


def test_runner_uses_the_active_python_interpreter_by_default() -> None:
    runner = PythonSubprocessRunner()
    result = runner.run(
        PythonExecutionRequest(
            source="print('ok')",
            expected_output="ok",
        )
    )

    assert sys.executable
    assert result.status is ExecutionStatus.PASSED
