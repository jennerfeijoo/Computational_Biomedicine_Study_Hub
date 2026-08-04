"""Qt integration tests for the vertical computational laboratory workflow."""

from __future__ import annotations

from PySide6.QtWidgets import QComboBox, QPlainTextEdit

from computational_biomedicine_study_hub.content.labs import DM857_LAB_01
from computational_biomedicine_study_hub.i18n.locales import AppLocale
from computational_biomedicine_study_hub.learning.python_execution import (
    ExecutionStatus,
    PythonExecutionRequest,
    PythonExecutionResult,
)
from computational_biomedicine_study_hub.storage.sqlite_progress_store import (
    SQLiteProgressStore,
)
from computational_biomedicine_study_hub.ui.pages.computational_labs_page import (
    ComputationalLabsPage,
)


class PassingRunner:
    def run(self, request: PythonExecutionRequest) -> PythonExecutionResult:
        return PythonExecutionResult(
            status=ExecutionStatus.PASSED,
            stdout=request.expected_output or "",
            stderr="",
            duration_ms=2,
            expected_output=request.expected_output,
        )


class FailingRunner:
    def run(self, request: PythonExecutionRequest) -> PythonExecutionResult:
        return PythonExecutionResult(
            status=ExecutionStatus.OUTPUT_MISMATCH,
            stdout="incorrect",
            stderr="",
            duration_ms=2,
            expected_output=request.expected_output,
        )


def test_page_records_checkpoint_and_persists_code(qtbot) -> None:  # type: ignore[no-untyped-def]
    progress = SQLiteProgressStore(":memory:")
    page = ComputationalLabsPage(
        progress,
        AppLocale.ENGLISH,
        runner=PassingRunner(),
    )
    qtbot.addWidget(page)
    try:
        selector = page.findChild(QComboBox, "computationalLabTaskSelector")
        editor = page.findChild(QPlainTextEdit, "computationalLabResponse")
        assert selector is not None
        assert editor is not None

        selector.setCurrentIndex(2)
        editor.setPlainText(
            "def summarize_measurements(values, lower, upper):\n    return (3, 2, 70.67)\n"
        )
        page._verify_or_complete()
        page.persist()

        task_id = DM857_LAB_01.tasks[2].task_id
        assert task_id in page.attempt.passed_checkpoints

        restored = ComputationalLabsPage(
            progress,
            AppLocale.ENGLISH,
            runner=PassingRunner(),
        )
        qtbot.addWidget(restored)
        assert restored.attempt.response_for(task_id).startswith("def summarize_measurements")
        assert task_id in restored.attempt.passed_checkpoints
    finally:
        progress.close()


def test_failed_checkpoint_preserves_output_without_increasing_progress(qtbot) -> None:  # type: ignore[no-untyped-def]
    page = ComputationalLabsPage(None, AppLocale.ENGLISH, runner=FailingRunner())
    qtbot.addWidget(page)
    selector = page.findChild(QComboBox, "computationalLabTaskSelector")
    editor = page.findChild(QPlainTextEdit, "computationalLabResponse")
    assert selector is not None
    assert editor is not None

    selector.setCurrentIndex(2)
    task_id = DM857_LAB_01.tasks[2].task_id
    editor.setPlainText(
        "def summarize_measurements(values, lower, upper):\n    return (0, 0, None)\n"
    )
    page._verify_or_complete()

    assert task_id not in page.attempt.completed_tasks
    assert task_id not in page.attempt.passed_checkpoints
    assert "output_mismatch" in page.attempt.execution_outputs[task_id]
    assert page.attempt.completion_ratio(DM857_LAB_01) == 0.0


def test_requesting_mentor_increases_support_without_completing_task(qtbot) -> None:  # type: ignore[no-untyped-def]
    page = ComputationalLabsPage(None, AppLocale.ENGLISH, runner=PassingRunner())
    qtbot.addWidget(page)
    task_id = page.current_task.task_id
    with qtbot.waitSignal(page.mentor_requested):
        page._request_mentor()

    assert page.attempt.hint_level_for(task_id) == 1
    assert task_id not in page.attempt.completed_tasks
    assert "Socratic method" in page.mentor_context()
