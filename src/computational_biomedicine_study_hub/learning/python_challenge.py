"""Deterministic evaluation of starter-code exercises against authored tests."""

from __future__ import annotations

from dataclasses import dataclass
from enum import StrEnum
from typing import Protocol

from ..content.python_challenges import PythonChallenge, PythonChallengeCase
from .python_execution import (
    ExecutionStatus,
    PythonCodeRunner,
    PythonExecutionRequest,
    PythonExecutionResult,
    PythonPolicyError,
    PythonSubprocessRunner,
    validate_python_source,
)


class ChallengeCaseStatus(StrEnum):
    """Learner-facing outcome for one visible challenge case."""

    PASSED = "passed"
    FAILED = "failed"
    ERROR = "error"
    TIMED_OUT = "timed_out"
    REJECTED = "rejected"
    OUTPUT_LIMIT = "output_limit"


@dataclass(frozen=True, slots=True)
class PythonChallengeCaseResult:
    """Result for one visible behavioral test."""

    case_id: str
    description: str
    status: ChallengeCaseStatus
    detail: str = ""

    @property
    def passed(self) -> bool:
        return self.status is ChallengeCaseStatus.PASSED


@dataclass(frozen=True, slots=True)
class PythonChallengeResult:
    """Aggregated visible and hidden test outcome without exposing hidden inputs."""

    exercise_id: str
    visible_results: tuple[PythonChallengeCaseResult, ...]
    hidden_passed: int
    hidden_total: int
    duration_ms: int

    def __post_init__(self) -> None:
        if not self.exercise_id.strip():
            raise ValueError("Python challenge results require an exercise ID.")
        if not self.visible_results:
            raise ValueError("Python challenge results require visible case results.")
        if not 0 <= self.hidden_passed <= self.hidden_total:
            raise ValueError("Hidden challenge counts are inconsistent.")
        if self.duration_ms < 0:
            raise ValueError("Challenge duration cannot be negative.")

    @property
    def all_passed(self) -> bool:
        return all(result.passed for result in self.visible_results) and (
            self.hidden_passed == self.hidden_total
        )


class PythonChallengeRunner(Protocol):
    """Interface consumed by the starter-code challenge widget."""

    def evaluate(self, source: str, challenge: PythonChallenge) -> PythonChallengeResult:
        """Evaluate learner source against visible and hidden authored cases."""


class PythonChallengeEvaluator:
    """Run each challenge case in an independent restricted Python process."""

    def __init__(self, runner: PythonCodeRunner | None = None) -> None:
        self._runner = runner or PythonSubprocessRunner()

    def evaluate(self, source: str, challenge: PythonChallenge) -> PythonChallengeResult:
        """Return deterministic case results while withholding hidden test details."""

        try:
            validate_python_source(source)
        except PythonPolicyError as exc:
            rejected_results = tuple(
                PythonChallengeCaseResult(
                    case_id=case.case_id,
                    description=case.description,
                    status=ChallengeCaseStatus.REJECTED,
                    detail=str(exc),
                )
                for case in challenge.visible_cases
            )
            return PythonChallengeResult(
                exercise_id=challenge.exercise_id,
                visible_results=rejected_results,
                hidden_passed=0,
                hidden_total=len(challenge.hidden_cases),
                duration_ms=0,
            )

        visible_results: list[PythonChallengeCaseResult] = []
        hidden_passed = 0
        duration_ms = 0

        for case in challenge.visible_cases:
            execution = self._run_case(source, case, challenge.timeout_seconds)
            duration_ms += execution.duration_ms
            visible_results.append(self._visible_result(case, execution))

        for case in challenge.hidden_cases:
            execution = self._run_case(source, case, challenge.timeout_seconds)
            duration_ms += execution.duration_ms
            if execution.status is ExecutionStatus.PASSED:
                hidden_passed += 1

        return PythonChallengeResult(
            exercise_id=challenge.exercise_id,
            visible_results=tuple(visible_results),
            hidden_passed=hidden_passed,
            hidden_total=len(challenge.hidden_cases),
            duration_ms=duration_ms,
        )

    def _run_case(
        self,
        source: str,
        case: PythonChallengeCase,
        timeout_seconds: float,
    ) -> PythonExecutionResult:
        combined_source = f"{source.rstrip()}\n\n{case.assertion.rstrip()}\n"
        return self._runner.run(
            PythonExecutionRequest(
                source=combined_source,
                timeout_seconds=timeout_seconds,
                output_limit=4096,
            )
        )

    @staticmethod
    def _visible_result(
        case: PythonChallengeCase,
        execution: PythonExecutionResult,
    ) -> PythonChallengeCaseResult:
        if execution.status is ExecutionStatus.PASSED:
            status = ChallengeCaseStatus.PASSED
            detail = ""
        elif execution.status is ExecutionStatus.RUNTIME_ERROR:
            if "AssertionError" in execution.stderr:
                status = ChallengeCaseStatus.FAILED
                detail = ""
            else:
                status = ChallengeCaseStatus.ERROR
                detail = PythonChallengeEvaluator._last_error_line(execution.stderr)
        elif execution.status is ExecutionStatus.TIMED_OUT:
            status = ChallengeCaseStatus.TIMED_OUT
            detail = ""
        elif execution.status is ExecutionStatus.REJECTED:
            status = ChallengeCaseStatus.REJECTED
            detail = execution.stderr
        elif execution.status is ExecutionStatus.OUTPUT_LIMIT:
            status = ChallengeCaseStatus.OUTPUT_LIMIT
            detail = ""
        else:
            status = ChallengeCaseStatus.ERROR
            detail = "Unexpected output-comparison state."

        return PythonChallengeCaseResult(
            case_id=case.case_id,
            description=case.description,
            status=status,
            detail=detail,
        )

    @staticmethod
    def _last_error_line(stderr: str) -> str:
        lines = tuple(line.strip() for line in stderr.splitlines() if line.strip())
        return lines[-1] if lines else "Runtime error"


__all__ = [
    "ChallengeCaseStatus",
    "PythonChallengeCaseResult",
    "PythonChallengeEvaluator",
    "PythonChallengeResult",
    "PythonChallengeRunner",
]
