"""Policy and adapter tests for optional local R execution."""

from __future__ import annotations

import pytest

from computational_biomedicine_study_hub.learning.python_execution import ExecutionStatus
from computational_biomedicine_study_hub.learning.r_execution import (
    RExecutionRequest,
    RPolicyError,
    RSubprocessRunner,
    can_execute_r,
    validate_r_source,
)


def test_r_policy_accepts_short_base_r_analysis() -> None:
    source = "x <- c(1, 2, 3)\ncat(sprintf('mean=%.1f\\n', mean(x)))\n"

    validate_r_source(source)

    assert can_execute_r(source)


@pytest.mark.parametrize(
    "source",
    (
        "system('whoami')",
        "readLines('/tmp/data.txt')",
        "library(stats)",
        "stats::median(c(1, 2, 3))",
        "eval(parse(text = '1 + 1'))",
        ".Call('native_symbol')",
        "`system`('whoami')",
    ),
)
def test_r_policy_rejects_external_or_dynamic_capabilities(source: str) -> None:
    with pytest.raises(RPolicyError):
        validate_r_source(source)

    assert not can_execute_r(source)


def test_r_policy_ignores_blocked_words_inside_comments_and_strings() -> None:
    source = "# system('ignored')\nlabel <- \"readLines('/tmp/file')\"\ncat(label)\n"

    validate_r_source(source)


def test_missing_rscript_returns_a_normalized_runtime_error() -> None:
    runner = RSubprocessRunner(executable="/definitely/missing/Rscript")

    result = runner.run(RExecutionRequest("cat('ok')", expected_output="ok"))

    assert result.status is ExecutionStatus.RUNTIME_ERROR
    assert result.stdout == ""
    assert "Unable to start Rscript" in result.stderr
    assert result.output_matches is False


def test_r_request_rejects_invalid_execution_limits() -> None:
    with pytest.raises(ValueError):
        RExecutionRequest("cat('x')", timeout_seconds=0.01)
    with pytest.raises(ValueError):
        RExecutionRequest("cat('x')", output_limit=100)
