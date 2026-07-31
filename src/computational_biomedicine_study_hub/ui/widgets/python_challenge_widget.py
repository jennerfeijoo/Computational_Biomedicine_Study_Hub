"""Editable PySide6 surface for starter-code challenges with hidden tests."""

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

from ...content.python_challenges import PythonChallenge
from ...i18n.challenge_copy import ChallengeCopyKey, challenge_text
from ...i18n.locales import DEFAULT_LOCALE, AppLocale
from ...learning.python_challenge import (
    ChallengeCaseStatus,
    PythonChallengeCaseResult,
    PythonChallengeEvaluator,
    PythonChallengeResult,
    PythonChallengeRunner,
)
from .python_challenge_styles import PYTHON_CHALLENGE_STYLESHEET

_CASE_COPY = {
    ChallengeCaseStatus.PASSED: ChallengeCopyKey.CASE_PASSED,
    ChallengeCaseStatus.FAILED: ChallengeCopyKey.CASE_FAILED,
    ChallengeCaseStatus.ERROR: ChallengeCopyKey.CASE_ERROR,
    ChallengeCaseStatus.TIMED_OUT: ChallengeCopyKey.CASE_TIMED_OUT,
    ChallengeCaseStatus.REJECTED: ChallengeCopyKey.CASE_REJECTED,
    ChallengeCaseStatus.OUTPUT_LIMIT: ChallengeCopyKey.CASE_OUTPUT_LIMIT,
}


class PythonChallengeWidget(QFrame):
    """Let learners complete starter code and run visible plus hidden tests."""

    tests_finished = Signal(str, bool)

    def __init__(
        self,
        starter_code: str,
        challenge: PythonChallenge,
        *,
        locale: AppLocale = DEFAULT_LOCALE,
        evaluator: PythonChallengeRunner | None = None,
        parent: QWidget | None = None,
    ) -> None:
        super().__init__(parent)
        if not starter_code.strip():
            raise ValueError("Python challenges require non-empty starter code.")
        if starter_code != challenge.starter_code:
            raise ValueError("Starter code must match the authored Python challenge.")

        self.setObjectName("pythonChallengeWidget")
        self.setStyleSheet(PYTHON_CHALLENGE_STYLESHEET)
        self._challenge = challenge
        self._locale = locale
        self._original_source = starter_code
        self._evaluator = evaluator or PythonChallengeEvaluator()
        self._last_result: PythonChallengeResult | None = None
        self._result_labels: list[QLabel] = []

        layout = QVBoxLayout(self)
        layout.setContentsMargins(16, 14, 16, 14)
        layout.setSpacing(10)

        title = QLabel(challenge_text(locale, ChallengeCopyKey.TITLE))
        title.setObjectName("pythonChallengeTitle")
        layout.addWidget(title)

        intro = QLabel(challenge_text(locale, ChallengeCopyKey.INTRO))
        intro.setObjectName("pythonChallengeIntro")
        intro.setWordWrap(True)
        layout.addWidget(intro)

        self._editor = QPlainTextEdit(starter_code)
        self._editor.setObjectName("pythonChallengeEditor")
        self._editor.setLineWrapMode(QPlainTextEdit.LineWrapMode.NoWrap)
        self._editor.setTabChangesFocus(False)
        self._editor.setMinimumHeight(145)
        layout.addWidget(self._editor)

        actions = QHBoxLayout()
        actions.setContentsMargins(0, 0, 0, 0)
        actions.setSpacing(8)
        actions.addStretch(1)

        self._reset_button = QPushButton(challenge_text(locale, ChallengeCopyKey.RESET))
        self._reset_button.setObjectName("pythonChallengeResetButton")
        self._reset_button.clicked.connect(self.reset_code)
        actions.addWidget(self._reset_button)

        self._run_button = QPushButton(challenge_text(locale, ChallengeCopyKey.RUN))
        self._run_button.setObjectName("pythonChallengeRunButton")
        self._run_button.clicked.connect(self.run_tests)
        actions.addWidget(self._run_button)
        layout.addLayout(actions)

        self._status = QLabel()
        self._status.setObjectName("pythonChallengeStatus")
        self._status.setWordWrap(True)
        self._status.hide()
        layout.addWidget(self._status)

        self._visible_heading = QLabel(challenge_text(locale, ChallengeCopyKey.VISIBLE_TESTS))
        self._visible_heading.setObjectName("pythonChallengeHeading")
        self._visible_heading.hide()
        layout.addWidget(self._visible_heading)

        self._results_container = QWidget()
        self._results_layout = QVBoxLayout(self._results_container)
        self._results_layout.setContentsMargins(0, 0, 0, 0)
        self._results_layout.setSpacing(7)
        self._results_container.hide()
        layout.addWidget(self._results_container)

        self._hidden_summary = QLabel()
        self._hidden_summary.setObjectName("pythonChallengeHiddenSummary")
        self._hidden_summary.setWordWrap(True)
        self._hidden_summary.hide()
        layout.addWidget(self._hidden_summary)

    @property
    def source(self) -> str:
        """Return the learner's current source code."""

        return self._editor.toPlainText()

    @property
    def last_result(self) -> PythonChallengeResult | None:
        """Return the latest aggregate test result."""

        return self._last_result

    @property
    def status_text(self) -> str:
        """Return the visible localized aggregate status."""

        return self._status.text()

    @property
    def hidden_summary_text(self) -> str:
        """Return the non-disclosing hidden-test summary."""

        return self._hidden_summary.text()

    @property
    def visible_result_texts(self) -> tuple[str, ...]:
        """Return rendered visible-case messages in authored order."""

        return tuple(label.text() for label in self._result_labels)

    def set_source(self, source: str) -> None:
        """Replace editable source without changing the authored reset point."""

        self._editor.setPlainText(source)

    @Slot()
    def run_tests(self) -> None:
        """Evaluate the current source and render visible plus hidden summaries."""

        self._set_busy(True)
        self._status.setProperty("resultState", "running")
        self._status.setText(challenge_text(self._locale, ChallengeCopyKey.RUNNING))
        self._status.show()
        self._refresh_style(self._status)
        QApplication.processEvents()

        try:
            result = self._evaluator.evaluate(self.source, self._challenge)
        except Exception as exc:  # pragma: no cover - defensive adapter boundary
            result = PythonChallengeResult(
                exercise_id=self._challenge.exercise_id,
                visible_results=tuple(
                    PythonChallengeCaseResult(
                        case_id=case.case_id,
                        description=case.description,
                        status=ChallengeCaseStatus.ERROR,
                        detail=str(exc),
                    )
                    for case in self._challenge.visible_cases
                ),
                hidden_passed=0,
                hidden_total=len(self._challenge.hidden_cases),
                duration_ms=0,
            )
        finally:
            self._set_busy(False)

        self._last_result = result
        self._render_result(result)
        self.tests_finished.emit(result.exercise_id, result.all_passed)

    @Slot()
    def reset_code(self) -> None:
        """Restore starter code and clear all prior test feedback."""

        self._editor.setPlainText(self._original_source)
        self._last_result = None
        self._status.clear()
        self._status.hide()
        self._visible_heading.hide()
        self._hidden_summary.clear()
        self._hidden_summary.hide()
        self._clear_result_labels()
        self._results_container.hide()

    def _render_result(self, result: PythonChallengeResult) -> None:
        aggregate_key = (
            ChallengeCopyKey.STATUS_ALL_PASSED
            if result.all_passed
            else ChallengeCopyKey.STATUS_INCOMPLETE
        )
        aggregate_state = "passed" if result.all_passed else "incomplete"
        aggregate = challenge_text(self._locale, aggregate_key)
        self._status.setText(
            challenge_text(
                self._locale,
                ChallengeCopyKey.STATUS_WITH_DURATION,
                status=aggregate,
                duration=result.duration_ms,
            )
        )
        self._status.setProperty("resultState", aggregate_state)
        self._refresh_style(self._status)
        self._status.show()

        self._clear_result_labels()
        for case_result in result.visible_results:
            status = challenge_text(self._locale, _CASE_COPY[case_result.status])
            text = f"{status}: {case_result.description}"
            if case_result.detail:
                text = f"{text} — {case_result.detail}"
            label = QLabel(text)
            label.setObjectName("pythonChallengeCaseResult")
            label.setProperty("resultState", case_result.status.value)
            label.setWordWrap(True)
            self._result_labels.append(label)
            self._results_layout.addWidget(label)

        self._visible_heading.show()
        self._results_container.show()
        self._hidden_summary.setText(
            challenge_text(
                self._locale,
                ChallengeCopyKey.HIDDEN_SUMMARY,
                passed=result.hidden_passed,
                total=result.hidden_total,
            )
        )
        self._hidden_summary.show()

    def _clear_result_labels(self) -> None:
        self._result_labels.clear()
        while self._results_layout.count():
            item = self._results_layout.takeAt(0)
            if item is None:
                break
            widget = item.widget()
            if widget is not None:
                widget.setParent(None)
                widget.deleteLater()

    def _set_busy(self, busy: bool) -> None:
        self._run_button.setEnabled(not busy)
        self._reset_button.setEnabled(not busy)
        self._editor.setReadOnly(busy)

    @staticmethod
    def _refresh_style(widget: QWidget) -> None:
        widget.style().unpolish(widget)
        widget.style().polish(widget)


__all__ = ["PythonChallengeWidget"]
