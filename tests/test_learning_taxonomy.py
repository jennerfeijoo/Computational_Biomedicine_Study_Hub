from __future__ import annotations

from computational_biomedicine_study_hub.learning import ActivityType, StudyCycleStage


def test_requested_assessment_types_are_supported() -> None:
    assert ActivityType.MULTIPLE_CHOICE.value == "multiple_choice"
    assert ActivityType.FLASHCARD.value == "flashcard"
    assert ActivityType.FILL_IN_THE_BLANK.value == "fill_in_the_blank"
    assert ActivityType.MATCHING.value == "matching"


def test_learning_cycle_includes_retrieval_and_spaced_review() -> None:
    assert StudyCycleStage.RETRIEVAL.value == "retrieval"
    assert StudyCycleStage.SPACED_REVIEW.value == "spaced_review"
