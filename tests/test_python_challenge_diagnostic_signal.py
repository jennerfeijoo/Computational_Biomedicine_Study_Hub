from __future__ import annotations

from PySide6.QtWidgets import QApplication

from computational_biomedicine_study_hub.content.python_challenges import (
    PythonChallenge,
    python_challenge_for,
)
from computational_biomedicine_study_hub.i18n import AppLocale
from computational_biomedicine_study_hub.learning.progress import ConfidenceLevel
from computational_biomedicine_study_hub.learning.python_challenge import (
    ChallengeCaseStatus,
    PythonChallengeCaseResult,
    PythonChallengeResult,
)
from computational_biomedicine_study_hub.tutoring import ChallengeDiagnostic
from computational_biomedicine_study_hub.ui.widgets import PythonChallengeWidget


class _FakeEvaluator:
    def evaluate(self, source: str, challenge: PythonChallenge) -> PythonChallengeResult:
        del source
        return PythonChallengeResult(
            exercise_id=challenge.exercise_id,
            visible_results=(
                PythonChallengeCaseResult(
                    case_id="duplicates",
                    description="Counts repeated integers correctly.",
                    status=ChallengeCaseStatus.FAILED,
                ),
                PythonChallengeCaseResult(
                    case_id="empty",
                    description="An empty collection contains zero unique elements.",
                    status=ChallengeCaseStatus.PASSED,
                ),
            ),
            hidden_passed=1,
            hidden_total=2,
            duration_ms=19,
        )


def _challenge() -> PythonChallenge:
    challenge = python_challenge_for(
        "m07.p04",
        "def unique_count(values):\n    pass",
        AppLocale.ENGLISH,
    )
    assert challenge is not None
    return challenge


def test_widget_emits_and_retains_verified_diagnostic(qapp: QApplication) -> None:
    widget = PythonChallengeWidget(
        "def unique_count(values):\n    pass",
        _challenge(),
        locale=AppLocale.ENGLISH,
        evaluator=_FakeEvaluator(),
        prompt="Write unique_count(values).",
        reference_solution="def unique_count(values):\n    return len(set(values))",
        explanation="A set removes duplicates before len counts the remaining values.",
    )
    emitted: list[ChallengeDiagnostic] = []
    widget.diagnostic_ready.connect(emitted.append)
    widget.set_source("def unique_count(values):\n    return len(values)")
    widget.choose_confidence(ConfidenceLevel.HIGH)

    widget.run_tests()

    assert len(emitted) == 1
    assert widget.last_diagnostic is emitted[0]
    assert emitted[0].course_code == "DM857"
    assert emitted[0].module_id == "dm857.m07"
    assert emitted[0].exercise_id == "m07.p04"
    assert emitted[0].confidence is ConfidenceLevel.HIGH
    assert not emitted[0].deterministic_grade
    assert emitted[0].hidden_passed == 1
    assert emitted[0].hidden_total == 2

    widget.reset_code()

    assert widget.last_diagnostic is None
