from __future__ import annotations

from PySide6.QtWidgets import QApplication, QPushButton

from computational_biomedicine_study_hub.content.python_challenges import (
    PythonChallenge,
    python_challenge_for,
)
from computational_biomedicine_study_hub.i18n import AppLocale
from computational_biomedicine_study_hub.learning.python_challenge import (
    ChallengeCaseStatus,
    PythonChallengeCaseResult,
    PythonChallengeResult,
)
from computational_biomedicine_study_hub.ui.widgets import PythonChallengeWidget


class _FakeEvaluator:
    def __init__(self, result: PythonChallengeResult) -> None:
        self.result = result
        self.calls: list[tuple[str, PythonChallenge]] = []

    def evaluate(self, source: str, challenge: PythonChallenge) -> PythonChallengeResult:
        self.calls.append((source, challenge))
        return self.result


def _challenge(locale: AppLocale = AppLocale.ENGLISH) -> PythonChallenge:
    challenge = python_challenge_for(
        "m07.p04",
        "def unique_count(values):\n    pass",
        locale,
    )
    assert challenge is not None
    return challenge


def _result(*, all_passed: bool) -> PythonChallengeResult:
    status = ChallengeCaseStatus.PASSED if all_passed else ChallengeCaseStatus.FAILED
    return PythonChallengeResult(
        exercise_id="m07.p04",
        visible_results=(
            PythonChallengeCaseResult(
                case_id="duplicates",
                description="Counts repeated integers correctly.",
                status=status,
            ),
            PythonChallengeCaseResult(
                case_id="empty",
                description="An empty collection contains zero unique elements.",
                status=ChallengeCaseStatus.PASSED,
            ),
        ),
        hidden_passed=2 if all_passed else 1,
        hidden_total=2,
        duration_ms=17,
    )


def test_widget_evaluates_edited_source_and_hides_test_inputs(qapp: QApplication) -> None:
    evaluator = _FakeEvaluator(_result(all_passed=False))
    widget = PythonChallengeWidget(
        "def unique_count(values):\n    pass",
        _challenge(),
        locale=AppLocale.ENGLISH,
        evaluator=evaluator,
    )
    source = "def unique_count(values):\n    return len(set(values))"
    widget.set_source(source)

    widget.run_tests()

    assert evaluator.calls[0][0] == source
    assert widget.last_result is evaluator.result
    assert "does not yet satisfy" in widget.status_text
    assert "17 ms" in widget.status_text
    assert widget.hidden_summary_text == "Hidden tests passed: 1/2"
    assert all("['A'" not in text for text in widget.visible_result_texts)


def test_widget_reset_restores_starter_code_and_clears_feedback(qapp: QApplication) -> None:
    evaluator = _FakeEvaluator(_result(all_passed=True))
    starter = "def unique_count(values):\n    pass"
    widget = PythonChallengeWidget(starter, _challenge(), evaluator=evaluator)
    widget.set_source("def unique_count(values):\n    return 99")
    widget.run_tests()

    widget.reset_code()

    assert widget.source == starter
    assert widget.last_result is None
    assert widget.status_text == ""
    assert widget.hidden_summary_text == ""
    assert widget.visible_result_texts == ()


def test_widget_buttons_are_localized_in_danish(qapp: QApplication) -> None:
    widget = PythonChallengeWidget(
        "def unique_count(values):\n    pass",
        _challenge(AppLocale.DANISH_DENMARK),
        locale=AppLocale.DANISH_DENMARK,
        evaluator=_FakeEvaluator(_result(all_passed=True)),
    )

    run_button = widget.findChild(QPushButton, "pythonChallengeRunButton")
    reset_button = widget.findChild(QPushButton, "pythonChallengeResetButton")

    assert run_button is not None
    assert reset_button is not None
    assert run_button.text() == "Kør test"
    assert reset_button.text() == "Nulstil kode"
