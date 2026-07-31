from __future__ import annotations

from PySide6.QtWidgets import QApplication

from computational_biomedicine_study_hub.content.dm857 import MODULE_07_MAPPINGS_SETS
from computational_biomedicine_study_hub.ui.widgets import GuidedPracticeCard, PythonChallengeWidget


def _exercise(exercise_id: str):
    return next(
        exercise
        for exercise in MODULE_07_MAPPINGS_SETS.practice_exercises
        if exercise.exercise_id == exercise_id
    )


def test_authored_starter_code_uses_executable_challenge_surface(
    qapp: QApplication,
) -> None:
    exercise = _exercise("m07.p04")

    card = GuidedPracticeCard(1, exercise)

    assert card.has_python_challenge
    assert isinstance(card.challenge_widget, PythonChallengeWidget)
    assert card.answer_text == exercise.starter_code


def test_unmapped_practice_keeps_the_general_answer_workspace(
    qapp: QApplication,
) -> None:
    card = GuidedPracticeCard(1, _exercise("m07.p01"))

    assert not card.has_python_challenge
    assert card.challenge_widget is None
    assert card.answer_text == ""
