"""PySide6 tests for editable R learning labs."""

from __future__ import annotations

from dataclasses import dataclass, field

from PySide6.QtWidgets import QApplication

from computational_biomedicine_study_hub.i18n import AppLocale
from computational_biomedicine_study_hub.learning.python_execution import ExecutionStatus
from computational_biomedicine_study_hub.learning.r_execution import (
    RExecutionRequest,
    RExecutionResult,
)
from computational_biomedicine_study_hub.ui.widgets import RLabWidget


@dataclass
class FakeRRunner:
    requests: list[RExecutionRequest] = field(default_factory=list)

    def run(self, request: RExecutionRequest) -> RExecutionResult:
        self.requests.append(request)
        return RExecutionResult(
            status=ExecutionStatus.PASSED,
            stdout=request.expected_output or "",
            stderr="",
            duration_ms=7,
            expected_output=request.expected_output,
        )


def test_r_lab_runs_editable_source_and_renders_result(qapp: QApplication) -> None:
    del qapp
    runner = FakeRRunner()
    widget = RLabWidget(
        "cat('original')",
        "changed",
        locale=AppLocale.ENGLISH,
        runner=runner,
    )
    widget.set_source("cat('changed')")

    widget.run_code()

    assert runner.requests == [
        RExecutionRequest(
            source="cat('changed')",
            expected_output="changed",
            timeout_seconds=3.0,
        )
    ]
    assert widget.last_result is not None
    assert widget.last_result.status is ExecutionStatus.PASSED
    assert widget.stdout_text == "changed"
    assert "correct" in widget.status_text.casefold()


def test_r_lab_reset_restores_authored_source(qapp: QApplication) -> None:
    del qapp
    widget = RLabWidget(
        "cat('original')",
        "original",
        locale=AppLocale.DANISH_DENMARK,
        runner=FakeRRunner(),
    )
    widget.set_source("cat('changed')")
    widget.run_code()

    widget.reset_code()

    assert widget.source == "cat('original')"
    assert widget.last_result is None
    assert widget.stdout_text == ""
    assert widget.status_text == ""
