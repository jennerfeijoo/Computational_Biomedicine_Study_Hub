from __future__ import annotations

from PySide6.QtWidgets import QApplication

from computational_biomedicine_study_hub.content.dm857 import MODULE_07_MAPPINGS_SETS
from computational_biomedicine_study_hub.content.python_challenges import PythonChallenge
from computational_biomedicine_study_hub.learning.progress import ConfidenceLevel, MasteryState
from computational_biomedicine_study_hub.learning.progress_service import ObjectiveAnswerSubmission
from computational_biomedicine_study_hub.learning.python_challenge import (
    ChallengeCaseStatus,
    PythonChallengeCaseResult,
    PythonChallengeResult,
)
from computational_biomedicine_study_hub.ui.widgets import GuidedPracticeCard, PythonChallengeWidget


def _exercise(exercise_id: str):
    return next(
        exercise
        for exercise in MODULE_07_MAPPINGS_SETS.practice_exercises
        if exercise.exercise_id == exercise_id
    )


class _PassingEvaluator:
    def evaluate(self, source: str, challenge: PythonChallenge) -> PythonChallengeResult:
        del source
        return PythonChallengeResult(
            exercise_id=challenge.exercise_id,
            visible_results=tuple(
                PythonChallengeCaseResult(
                    case_id=case.case_id,
                    description=case.description,
                    status=ChallengeCaseStatus.PASSED,
                )
                for case in challenge.visible_cases
            ),
            hidden_passed=len(challenge.hidden_cases),
            hidden_total=len(challenge.hidden_cases),
            duration_ms=8,
        )


class _Recorder:
    def __init__(self) -> None:
        self.submissions: list[ObjectiveAnswerSubmission] = []

    def record_objective_answer(
        self,
        submission: ObjectiveAnswerSubmission,
    ) -> tuple[MasteryState, ...]:
        self.submissions.append(submission)
        return ()


def test_authored_starter_code_uses_executable_challenge_surface(
    qapp: QApplication,
) -> None:
    exercise = _exercise("m07.p04")

    card = GuidedPracticeCard(1, exercise)

    assert card.has_python_challenge
    assert isinstance(card.challenge_widget, PythonChallengeWidget)
    assert card.answer_text == exercise.starter_code


def test_guided_card_supplies_authored_context_to_persistence(
    qapp: QApplication,
) -> None:
    exercise = _exercise("m07.p04")
    recorder = _Recorder()
    card = GuidedPracticeCard(
        1,
        exercise,
        challenge_runner=_PassingEvaluator(),
        progress_recorder=recorder,
    )
    challenge_widget = card.challenge_widget
    assert challenge_widget is not None
    challenge_widget.set_source(exercise.solution)
    challenge_widget.choose_confidence(ConfidenceLevel.HIGH)

    challenge_widget.run_tests()

    assert len(recorder.submissions) == 1
    submission = recorder.submissions[0]
    assert submission.course_code == "DM857"
    assert submission.module_id == "dm857.m07"
    assert submission.item_id == exercise.exercise_id
    assert submission.activity_type == exercise.activity_type.value
    assert submission.objective_ids == ("m07.o6", "m07.o8")
    assert submission.prompt == exercise.prompt
    assert submission.selected_answer == exercise.solution
    assert submission.correct_answer == exercise.solution
    assert submission.explanation == exercise.explanation
    assert submission.is_correct


def test_unmapped_practice_keeps_the_general_answer_workspace(
    qapp: QApplication,
) -> None:
    card = GuidedPracticeCard(1, _exercise("m07.p01"))

    assert not card.has_python_challenge
    assert card.challenge_widget is None
    assert card.answer_text == ""
