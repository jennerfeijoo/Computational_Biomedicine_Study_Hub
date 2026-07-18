from __future__ import annotations

import random

import pytest
from PySide6.QtWidgets import QApplication

from computational_biomedicine_study_hub.content.dm857 import MODULE_01_FOUNDATIONS
from computational_biomedicine_study_hub.learning.guided_practice import (
    GuidedPracticeSessionGenerator,
)
from computational_biomedicine_study_hub.ui.widgets import (
    GuidedPracticeCard,
    GuidedPracticeWidget,
)


def test_guided_practice_generator_creates_non_repeating_sessions() -> None:
    generator = GuidedPracticeSessionGenerator(
        MODULE_01_FOUNDATIONS.practice_exercises,
        exercise_count=4,
        rng=random.Random(11),
    )

    first = generator.new_session()
    second = generator.new_session()

    assert len(first.exercises) == 4
    assert len(set(first.exercise_ids)) == 4
    assert set(first.exercise_ids) != set(second.exercise_ids)


def test_guided_practice_generator_rejects_duplicate_ids() -> None:
    exercise = MODULE_01_FOUNDATIONS.practice_exercises[0]

    with pytest.raises(ValueError, match="must be unique"):
        GuidedPracticeSessionGenerator((exercise, exercise), exercise_count=1)


def test_guided_practice_widget_renders_a_random_subset(qapp: QApplication) -> None:
    generator = GuidedPracticeSessionGenerator(
        MODULE_01_FOUNDATIONS.practice_exercises,
        exercise_count=4,
        rng=random.Random(21),
    )
    widget = GuidedPracticeWidget(
        MODULE_01_FOUNDATIONS.practice_exercises,
        generator=generator,
    )

    first_ids = widget.current_exercise_ids
    assert len(widget.exercise_cards) == 4
    assert widget.progress_text == "0 resueltos · 0 para repasar · 0/4 valorados"

    widget.new_session()

    assert len(widget.exercise_cards) == 4
    assert set(first_ids) != set(widget.current_exercise_ids)


def test_guided_practice_card_reveals_hints_solution_and_self_assessment(
    qapp: QApplication,
) -> None:
    exercise = MODULE_01_FOUNDATIONS.practice_exercises[0]
    card = GuidedPracticeCard(1, exercise)

    assert card.visible_hint_count == 0
    assert not card.solution_revealed
    assert card.assessment_state == ""

    card.show_next_hint()
    assert card.visible_hint_count == 1
    assert exercise.hints[0] in card.hint_text

    card.reveal_solution()
    assert card.solution_revealed
    assert card.solution_text == exercise.solution

    card.mark_review()
    assert card.assessment_state == "review"

    card.mark_solved()
    assert card.assessment_state == "solved"


def test_guided_practice_widget_updates_self_assessment_summary(qapp: QApplication) -> None:
    widget = GuidedPracticeWidget(
        MODULE_01_FOUNDATIONS.practice_exercises,
        exercise_count=4,
    )
    first_card = widget.exercise_cards[0]
    second_card = widget.exercise_cards[1]

    first_card.reveal_solution()
    first_card.mark_solved()
    second_card.reveal_solution()
    second_card.mark_review()

    assert widget.progress_text == "1 resueltos · 1 para repasar · 2/4 valorados"
