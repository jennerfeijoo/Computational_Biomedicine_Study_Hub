from __future__ import annotations

import pytest

from computational_biomedicine_study_hub.content.models import AssessmentItem
from computational_biomedicine_study_hub.learning import ActivityType


def test_assessment_rejects_duplicate_visible_options() -> None:
    with pytest.raises(ValueError, match="duplicate visible options"):
        AssessmentItem(
            item_id="dm857.test.duplicate",
            activity_type=ActivityType.MULTIPLE_CHOICE,
            prompt="Choose one.",
            options=("Same", " same "),
            correct_answers=("Same",),
            explanation="The options must remain distinguishable.",
            option_ids=("first", "second"),
            correct_option_ids=("first",),
        )


def test_assessment_rejects_option_ids_with_surrounding_whitespace() -> None:
    with pytest.raises(ValueError, match="surrounding whitespace"):
        AssessmentItem(
            item_id="dm857.test.whitespace",
            activity_type=ActivityType.TRUE_FALSE,
            prompt="A statement.",
            options=("True", "False"),
            correct_answers=("True",),
            explanation="The answer identity must be canonical.",
            option_ids=(" true", "false"),
            correct_option_ids=(" true",),
        )


def test_assessment_rejects_misaligned_answer_text_and_option_id() -> None:
    with pytest.raises(ValueError, match="wrong visible answer"):
        AssessmentItem(
            item_id="dm857.test.misaligned",
            activity_type=ActivityType.MULTIPLE_CHOICE,
            prompt="Choose one.",
            options=("Alpha", "Beta"),
            correct_answers=("Alpha",),
            explanation="The ID and visible answer must identify the same option.",
            option_ids=("alpha", "beta"),
            correct_option_ids=("beta",),
        )
