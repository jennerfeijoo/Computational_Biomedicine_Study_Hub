"""Editable PySide6 surface for exploratory local Python execution."""

from __future__ import annotations

from PySide6.QtCore import Signal, Slot
from PySide6.QtWidgets import (
    QApplication,
    QFrame,
    QHBoxLayout,
    QLabel,
    QPlainTextEdit,
    QPushButton,
    QVBoxLayout,
    QWidget,
)

from ...i18n.lab_copy import LabCopyKey, lab_text
from ...i18n.locales import DEFAULT_LOCALE, AppLocale
from ...learning.python_execution import (
    ExecutionStatus,
    PythonCodeRunner,
    PythonExecutionRequest,
    PythonExecutionResult,
    PythonSubprocessRunner,
)
from .python_lab_styles import PYTHON_LAB_STYLESHEET

_STATUS_COPY = {
    ExecutionStatus.PASSED: LabCopyKey.STATUS_PASSED,
    ExecutionStatus.OUTPUT_MISMATCH: LabCopyKey.STATUS_MISMATCH,
    ExecutionStatus.RUNTIME_ERROR: LabCopyKey.STATUS_RUNTIME_ERROR,
    ExecutionStatus.TIMED_OUT: LabCopyKey.STATUS_TIMED_OUT,
    ExecutionStatus.REJECTED: LabCopyKey.STATUS_REJECTED,
    ExecutionStatus.OUTPUT_LIMIT: LabCopyKey.STATUS_OUTPUT_LIMIT,
}


class PythonLabWidget(QFrame):
    """Let learners change variables and inspect the resulting local output."""

    execution_finished = Signal(str)

    def __init__(
        self,
        source: str = "",
        expected_output: str | None = None,
        *,
        locale: AppLocale = DEFAULT_LOCALE,
        runner: PythonCodeRunner | None = None,
        timeout_seconds: float = 2.0,
        compare_output: bool = False,
        show_reference: bool = False,
        parent: QWidget | None = None,
    ) -> None:
        super().__init__(parent)
        if not 0.1 <= timeout_seconds <= 10.0:
            raise ValueError("timeout_seconds must be between 0.1 and 10.0.")

        self.setObjectName("pythonLabWidget")
        self.setStyleSheet(PYTHON_LAB_STYLESHEET)
        self._locale = locale
        self._original_source = source
        self._expected_output = expected_output
        self._compare_output = compare_output
        self._runner = runner or PythonSubprocessRunner()
        self._timeout_seconds = timeout_seconds
        self._last_result: PythonExecutionResult | None = None

        layout = QVBoxLayout(self)
        layout.setContentsMargins(18, 16, 18, 16)
        layout.setSpacing(10)

        title = QLabel(lab_text(locale, LabCopyKey.TITLE))
        title.setObjectName("pythonLabTitle")
        layout.addWidget(title)

        self._editor = self._code_editor(source, "pythonLabEditor", read_only=False)
        self._editor.setMinimumHeight(150)
        layout.addWidget(self._editor)

        action_row = QHBoxLayout()
        action_row.setContentsMargins(0, 0, 0, 0)
        action_row.setSpacing(10)
        action_row.addStretch(1)

        self._reset_button = QPushButton(lab_text(locale, LabCopyKey.RESET))
        self._reset_button.setObjectName("pythonLabResetButton")
        self._reset_button.clicked.connect(self.reset_code)
        action_row.addWidget(self._reset_button)

        self._run_button = QPushButton(lab_text(locale, LabCopyKey.RUN))
        self._run_button.setObjectName("pythonLabRunButton")
        self._run_button.clicked.connect(self.run_code)
        action_row.addWidget(self._run_button)
        layout.addLayout(action_row)

        self._status = QLabel()
        self._status.setObjectName("pythonLabStatus")
        self._status.setWordWrap(True)
        self._status.hide()
        layout.addWidget(self._status)

        self._expected_heading = self._output_heading(lab_text(locale, LabCopyKey.EXPECTED))
        self._expected = self._code_editor(
            expected_output or lab_text(locale, LabCopyKey.NO_OUTPUT),
            "pythonLabExpected",
            read_only=True,
        )
        self._expected_heading.setVisible(show_reference)
        self._expected.setVisible(show_reference)
        layout.addWidget(self._expected_heading)
        layout.addWidget(self._expected)

        self._stdout_heading = self._output_heading(lab_text(locale, LabCopyKey.STDOUT))
        self._stdout = self._code_editor("", "pythonLabStdout", read_only=True)
        self._stdout_heading.hide()
        self._stdout.hide()
        layout.addWidget(self._stdout_heading)
        layout.addWidget(self._stdout)

        self._stderr_heading = self._output_heading(lab_text(locale, LabCopyKey.STDERR))
        self._stderr = self._code_editor("", "pythonLabStderr", read_only=True)
        self._stderr_heading.hide()
        self._stderr.hide()
        layout.addWidget(self._stderr_heading)
        layout.addWidget(self._stderr)

    @property
    def source(self) -> str:
        """Return the current editable source."""

        return self._editor.toPlainText()

    @property
    def last_result(self) -> PythonExecutionResult | None:
        """Return the latest execution result."""

        return self._last_result

    @property
    def status_text(self) -> str:
        """Return the visible localized execution status."""

        return self._status.text()

    @property
    def stdout_text(self) -> str:
        """Return the currently rendered standard output."""

        return self._stdout.toPlainText()

    @property
    def stderr_text(self) -> str:
        """Return the currently rendered error output."""

        return self._stderr.toPlainText()

    @property
    def reference_visible(self) -> bool:
        """Return whether the optional authored reference output is displayed."""

        return self._expected.isVisible()

    def set_source(self, source: str) -> None:
        """Replace editable source without changing the reset point."""

        self._editor.setPlainText(source)

    @Slot()
    def run_code(self) -> None:
        """Execute the current source and display what actually happened."""

        if not self.source.strip():
            self._status.setProperty("executionStatus", "warning")
            self._status.setText(lab_text(self._locale, LabCopyKey.SOURCE_REQUIRED))
            self._status.show()
            self._refresh_style(self._status)
            return

        self._set_busy(True)
        self._status.setProperty("executionStatus", "running")
        self._status.setText(lab_text(self._locale, LabCopyKey.RUNNING))
        self._status.show()
        self._refresh_style(self._status)
        QApplication.processEvents()

        expected = self._expected_output if self._compare_output else None
        try:
            result = self._runner.run(
                PythonExecutionRequest(
                    source=self.source,
                    expected_output=expected,
                    timeout_seconds=self._timeout_seconds,
                )
            )
        except Exception as exc:  # pragma: no cover - defensive adapter boundary
            result = PythonExecutionResult(
                status=ExecutionStatus.RUNTIME_ERROR,
                stdout="",
                stderr=str(exc),
                duration_ms=0,
                expected_output=expected,
            )
        finally:
            self._set_busy(False)

        self._last_result = result
        self._render_result(result)
        self.execution_finished.emit(result.status.value)

    @Slot()
    def reset_code(self) -> None:
        """Restore the initial workspace and clear execution feedback."""

        self._editor.setPlainText(self._original_source)
        self._last_result = None
        self._status.clear()
        self._status.hide()
        self._stdout.clear()
        self._stdout.hide()
        self._stdout_heading.hide()
        self._stderr.clear()
        self._stderr.hide()
        self._stderr_heading.hide()

    def _render_result(self, result: PythonExecutionResult) -> None:
        status = lab_text(self._locale, _STATUS_COPY[result.status])
        self._status.setText(
            lab_text(
                self._locale,
                LabCopyKey.STATUS_WITH_DURATION,
                status=status,
                duration=result.duration_ms,
            )
        )
        self._status.setProperty("executionStatus", result.status.value)
        self._refresh_style(self._status)
        self._status.show()

        stdout = result.stdout or lab_text(self._locale, LabCopyKey.NO_OUTPUT)
        self._stdout.setPlainText(stdout)
        self._fit_output(self._stdout, stdout)
        self._stdout_heading.show()
        self._stdout.show()

        if result.stderr:
            self._stderr.setPlainText(result.stderr)
            self._fit_output(self._stderr, result.stderr)
            self._stderr_heading.show()
            self._stderr.show()
        else:
            self._stderr.clear()
            self._stderr_heading.hide()
            self._stderr.hide()

    def _set_busy(self, busy: bool) -> None:
        self._run_button.setEnabled(not busy)
        self._reset_button.setEnabled(not busy)
        self._editor.setReadOnly(busy)

    @staticmethod
    def _output_heading(text: str) -> QLabel:
        heading = QLabel(text)
        heading.setObjectName("pythonLabOutputHeading")
        return heading

    @staticmethod
    def _code_editor(text: str, object_name: str, *, read_only: bool) -> QPlainTextEdit:
        editor = QPlainTextEdit(text)
        editor.setObjectName(object_name)
        editor.setReadOnly(read_only)
        editor.setLineWrapMode(QPlainTextEdit.LineWrapMode.NoWrap)
        editor.setTabChangesFocus(False)
        PythonLabWidget._fit_output(editor, text)
        return editor

    @staticmethod
    def _fit_output(editor: QPlainTextEdit, text: str) -> None:
        line_count = max(1, text.count("\n") + 1)
        editor.setFixedHeight(min(220, 34 + line_count * 20))

    @staticmethod
    def _refresh_style(widget: QWidget) -> None:
        widget.style().unpolish(widget)
        widget.style().polish(widget)


__all__ = ["PythonLabWidget"]
