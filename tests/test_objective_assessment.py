from __future__ import annotations

import random

import pytest
from PySide6.QtWidgets import QApplication

from computational_biomedicine_study_hub.content.dm857 import OBJECTIVE_QUESTION_BANK
from computational_biomedicine_study_hub.content.models import AssessmentItem
from computational_biomedicine_study_hub.courses.dm857 import DM857Page
from computational_biomedicine_study_hub.learning import ActivityType
from computational_biomedicine_study_hub.learning.objective_assessment import (
    ObjectiveSessionGenerator,
    grade_objective_answer,
)
from computational_biomedicine_study_hub.ui.widgets import (
    ObjectiveAssessmentWidget,
    ObjectiveQuestionCard,
)


def test_dm857_objective_bank_is_large_unique_and_deterministic() -> None:
    assert len(OBJECTIVE_QUESTION_BANK) == 20
    assert len({item.item_id for item in OBJECTIVE_QUESTION_BANK}) == 20
    assert all(
        item.activity_type in {ActivityType.MULTIPLE_CHOICE, ActivityType.TRUE_FALSE}
        for item in OBJECTIVE_QUESTION_BANK
    )
    assert all(len(item.correct_answers) == 1 for item in OBJECTIVE_QUESTION_BANK)
    assert all(item.correct_answers[0] in item.options for item in OBJECTIVE_QUESTION_BANK)


def test_generator_builds_balanced_varied_sessions_and_shuffles_options() -> None:
    generator = ObjectiveSessionGenerator(
        OBJECTIVE_QUESTION_BANK,
        question_count=6,
        rng=random.Random(17),
    )

    first = generator.new_session()
    second = generator.new_session()

    assert len(first.questions) == 6
    assert len(set(first.item_ids)) == 6
    assert set(first.item_ids) != set(second.item_ids)
    assert {question.item.activity_type for question in first.questions} == {
        ActivityType.MULTIPLE_CHOICE,
        ActivityType.TRUE_FALSE,
    }
    assert all(
        set(question.display_options) == set(question.item.options)
        for question in first.questions
    )


def test_objective_grading_returns_authored_feedback() -> None:
    generator = ObjectiveSessionGenerator(
        OBJECTIVE_QUESTION_BANK,
        question_count=1,
        rng=random.Random(3),
    )
    question = generator.new_session().questions[0]
    correct_answer = question.item.correct_answers[0]
    wrong_answer = next(option for option in question.item.options if option != correct_answer)

    correct = grade_objective_answer(question, correct_answer)
    incorrect = grade_objective_answer(question, wrong_answer)

    assert correct.is_correct
    assert not incorrect.is_correct
    assert incorrect.correct_answer == correct_answer
    assert incorrect.explanation == question.item.explanation


def test_generator_rejects_unsupported_activity_types() -> None:
    unsupported = AssessmentItem(
        item_id="unsupported",
        activity_type=ActivityType.SHORT_ANSWER,
        prompt="Explica el concepto.",
        options=(),
        correct_answers=("Respuesta",),
        explanation="Explicación",
    )

    with pytest.raises(ValueError, match="supports only"):
        ObjectiveSessionGenerator((unsupported,), question_count=1)


def test_dm857_page_renders_six_interactive_questions(qapp: QApplication) -> None:
    page = DM857Page()
    widget = page.findChild(ObjectiveAssessmentWidget, "objectiveAssessmentWidget")

    assert widget is not None
    assert len(widget.question_cards) == 6
    assert len(widget.current_item_ids) == 6
    assert widget.score_text == "0 aciertos · 0/6"


def test_question_card_autocorrects_and_updates_score(qapp: QApplication) -> None:
    widget = ObjectiveAssessmentWidget(
        OBJECTIVE_QUESTION_BANK,
        generator=ObjectiveSessionGenerator(
            OBJECTIVE_QUESTION_BANK,
            question_count=6,
            rng=random.Random(21),
        ),
    )
    bank_by_id = {item.item_id: item for item in OBJECTIVE_QUESTION_BANK}
    card = widget.question_cards[0]
    item = bank_by_id[card.item_id]

    assert card.choose_answer(item.correct_answers[0])
    card.check_answer()

    assert card.is_answered
    assert card.feedback_text.startswith("Correcto.")
    assert widget.score_text == "1 aciertos · 1/6"


def test_question_card_exposes_correct_answer_after_an_error(qapp: QApplication) -> None:
    widget = ObjectiveAssessmentWidget(
        OBJECTIVE_QUESTION_BANK,
        generator=ObjectiveSessionGenerator(
            OBJECTIVE_QUESTION_BANK,
            question_count=6,
            rng=random.Random(25),
        ),
    )
    bank_by_id = {item.item_id: item for item in OBJECTIVE_QUESTION_BANK}
    card: ObjectiveQuestionCard = widget.question_cards[0]
    item = bank_by_id[card.item_id]
    wrong_answer = next(option for option in item.options if option != item.correct_answers[0])

    assert card.choose_answer(wrong_answer)
    card.check_answer()

    assert card.is_answered
    assert card.feedback_text.startswith("Incorrecto.")
    assert item.correct_answers[0] in card.feedback_text
    assert widget.score_text == "0 aciertos · 1/6"


def test_new_practice_replaces_the_question_set(qapp: QApplication) -> None:
    widget = ObjectiveAssessmentWidget(
        OBJECTIVE_QUESTION_BANK,
        generator=ObjectiveSessionGenerator(
            OBJECTIVE_QUESTION_BANK,
            question_count=6,
            rng=random.Random(31),
        ),
    )
    first_ids = set(widget.current_item_ids)

    widget.new_session()

    assert set(widget.current_item_ids) != first_ids
    assert len(widget.question_cards) == 6
    assert widget.score_text == "0 aciertos · 0/6"
