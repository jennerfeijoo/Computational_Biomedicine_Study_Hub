from __future__ import annotations

import pytest

from computational_biomedicine_study_hub.content.dm857 import (
    EXTRA_CLOSED_ASSESSMENT_ITEMS,
    MODULE_01_FOUNDATIONS,
)
from computational_biomedicine_study_hub.learning.assessment_session import (
    SUPPORTED_ACTIVITY_TYPES,
    AssessmentSession,
)


def _question_bank():
    authored = tuple(
        item
        for item in MODULE_01_FOUNDATIONS.assessment_items
        if item.activity_type in SUPPORTED_ACTIVITY_TYPES
    )
    return authored + EXTRA_CLOSED_ASSESSMENT_ITEMS


def test_module_01_closed_bank_is_large_unique_and_supported() -> None:
    bank = _question_bank()

    assert len(bank) == 18
    assert len({item.item_id for item in bank}) == len(bank)
    assert all(item.activity_type in SUPPORTED_ACTIVITY_TYPES for item in bank)


def test_session_selects_questions_without_repetition() -> None:
    session = AssessmentSession(_question_bank(), question_count=6, seed=41)

    assert len(session.questions) == 6
    assert len(set(session.item_ids)) == 6
    assert session.answered_count == 0
    assert session.score == 0


def test_same_seed_reproduces_question_and_option_order() -> None:
    first = AssessmentSession(_question_bank(), question_count=6, seed=7)
    second = AssessmentSession(_question_bank(), question_count=6, seed=7)

    assert first.item_ids == second.item_ids
    assert [question.options for question in first.questions] == [
        question.options for question in second.questions
    ]


def test_next_session_replaces_at_least_one_question_when_sample_repeats() -> None:
    first = AssessmentSession(_question_bank(), question_count=6, seed=13)
    second = AssessmentSession(
        _question_bank(),
        question_count=6,
        seed=13,
        previous_item_ids=first.item_ids,
    )

    assert set(second.item_ids) != set(first.item_ids)


def test_session_grades_answers_deterministically_and_tracks_score() -> None:
    session = AssessmentSession(_question_bank(), question_count=2, seed=3)
    correct_answer = session.current_question.item.correct_answers[0]

    result = session.submit(correct_answer)

    assert result.is_correct
    assert session.score == 1
    assert session.answered_count == 1
    assert session.advance()

    wrong_answer = next(
        option
        for option in session.current_question.options
        if option != session.current_question.item.correct_answers[0]
    )
    result = session.submit(wrong_answer)

    assert not result.is_correct
    assert session.score == 1
    assert session.answered_count == 2
    assert session.is_complete
    assert not session.advance()


def test_session_rejects_duplicate_submission() -> None:
    session = AssessmentSession(_question_bank(), question_count=1, seed=2)
    session.submit(session.current_question.item.correct_answers[0])

    with pytest.raises(RuntimeError, match="already been answered"):
        session.submit(session.current_question.item.correct_answers[0])
