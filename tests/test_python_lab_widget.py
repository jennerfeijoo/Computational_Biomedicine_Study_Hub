from __future__ import annotations

from PySide6.QtWidgets import QApplication, QPushButton

from computational_biomedicine_study_hub.content.dm857 import MODULE_01_FOUNDATIONS
from computational_biomedicine_study_hub.i18n import AppLocale
from computational_biomedicine_study_hub.learning.python_execution import (
    ExecutionStatus,
    PythonExecutionRequest,
    PythonExecutionResult,
    can_execute_python,
)
from computational_biomedicine_study_hub.ui.pages.module_reader_page import ModuleReaderPage
from computational_biomedicine_study_hub.ui.widgets import PythonLabWidget


class _FakeRunner:
    def __init__(self, result: PythonExecutionResult) -> None:
        self.result = result
        self.requests: list[PythonExecutionRequest] = []

    def run(self, request: PythonExecutionRequest) -> PythonExecutionResult:
        self.requests.append(request)
        return self.result


def test_lab_runs_edited_source_without_grading_against_example(qapp: QApplication) -> None:
    runner = _FakeRunner(
        PythonExecutionResult(
            status=ExecutionStatus.PASSED,
            stdout="12\n",
            stderr="",
            duration_ms=24,
            expected_output=None,
        )
    )
    widget = PythonLabWidget(
        "print(6)",
        "6",
        locale=AppLocale.ENGLISH,
        runner=runner,
    )
    widget.set_source("print(6 * 2)")

    widget.run_code()

    assert len(runner.requests) == 1
    assert runner.requests[0].source == "print(6 * 2)"
    assert runner.requests[0].expected_output is None
    assert widget.last_result is runner.result
    assert widget.stdout_text == "12\n"
    assert widget.stderr_text == ""
    assert "Execution completed" in widget.status_text
    assert "24 ms" in widget.status_text
    assert not widget.reference_visible


def test_lab_can_opt_into_reference_comparison(qapp: QApplication) -> None:
    runner = _FakeRunner(
        PythonExecutionResult(
            status=ExecutionStatus.OUTPUT_MISMATCH,
            stdout="4\n",
            stderr="",
            duration_ms=8,
            expected_output="5",
        )
    )
    widget = PythonLabWidget(
        "print(5)",
        "5",
        runner=runner,
        compare_output=True,
        show_reference=True,
    )

    widget.set_source("print(4)")
    widget.run_code()

    assert runner.requests[0].expected_output == "5"
    assert widget.reference_visible
    assert "Ejecución completada" in widget.status_text


def test_lab_reset_restores_initial_workspace_and_clears_feedback(
    qapp: QApplication,
) -> None:
    runner = _FakeRunner(
        PythonExecutionResult(
            status=ExecutionStatus.PASSED,
            stdout="4\n",
            stderr="",
            duration_ms=8,
            expected_output=None,
        )
    )
    widget = PythonLabWidget("print(5)", "5", runner=runner)
    widget.set_source("print(4)")
    widget.run_code()

    widget.reset_code()

    assert widget.source == "print(5)"
    assert widget.last_result is None
    assert widget.status_text == ""
    assert widget.stdout_text == ""
    assert widget.stderr_text == ""


def test_blank_lab_requires_code_before_execution(qapp: QApplication) -> None:
    runner = _FakeRunner(
        PythonExecutionResult(
            status=ExecutionStatus.PASSED,
            stdout="",
            stderr="",
            duration_ms=1,
            expected_output=None,
        )
    )
    widget = PythonLabWidget("", runner=runner)

    widget.run_code()

    assert not runner.requests
    assert "Escribe código" in widget.status_text


def test_lab_renders_runtime_errors(qapp: QApplication) -> None:
    runner = _FakeRunner(
        PythonExecutionResult(
            status=ExecutionStatus.RUNTIME_ERROR,
            stdout="",
            stderr="ZeroDivisionError: division by zero",
            duration_ms=4,
            expected_output=None,
        )
    )
    widget = PythonLabWidget("1 / 0", runner=runner)

    widget.run_code()

    assert "Error durante la ejecución" in widget.status_text
    assert "ZeroDivisionError" in widget.stderr_text


def test_lab_buttons_are_localized_in_danish(qapp: QApplication) -> None:
    widget = PythonLabWidget(
        "print(1)",
        locale=AppLocale.DANISH_DENMARK,
        runner=_FakeRunner(
            PythonExecutionResult(
                status=ExecutionStatus.PASSED,
                stdout="1\n",
                stderr="",
                duration_ms=1,
                expected_output=None,
            )
        ),
    )

    run_button = widget.findChild(QPushButton, "pythonLabRunButton")
    reset_button = widget.findChild(QPushButton, "pythonLabResetButton")

    assert run_button is not None
    assert reset_button is not None
    assert run_button.text() == "Kør"
    assert reset_button.text() == "Nulstil"


def test_module_reader_embeds_exploratory_labs_for_policy_compatible_examples(
    qapp: QApplication,
) -> None:
    page = ModuleReaderPage(MODULE_01_FOUNDATIONS)

    assert page.select_section_index(2)
    labs = page.findChildren(PythonLabWidget)
    expected = sum(
        can_execute_python(example.code) for example in MODULE_01_FOUNDATIONS.worked_examples
    )

    assert expected > 0
    assert len(labs) == expected
    assert all(not lab.reference_visible for lab in labs)
