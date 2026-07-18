"""Taxonomy of supported learning activities and study-cycle stages."""

from __future__ import annotations

from enum import StrEnum


class ActivityType(StrEnum):
    """Learning interactions that the application can render and assess."""

    WORKED_EXAMPLE = "worked_example"
    FLASHCARD = "flashcard"
    MULTIPLE_CHOICE = "multiple_choice"
    MULTIPLE_SELECT = "multiple_select"
    TRUE_FALSE = "true_false"
    FILL_IN_THE_BLANK = "fill_in_the_blank"
    MATCHING = "matching"
    ORDERING = "ordering"
    CODE_COMPLETION = "code_completion"
    CODE_TRACING = "code_tracing"
    DEBUGGING = "debugging"
    SHORT_ANSWER = "short_answer"
    ORAL_EXPLANATION = "oral_explanation"
    DATA_INTERPRETATION = "data_interpretation"
    PIPELINE_DESIGN = "pipeline_design"


class StudyCycleStage(StrEnum):
    """Stages used to sequence content according to effective learning practice."""

    CONCEPT = "concept"
    WORKED_EXAMPLE = "worked_example"
    GUIDED_PRACTICE = "guided_practice"
    RETRIEVAL = "retrieval"
    FEEDBACK = "feedback"
    TRANSFER = "transfer"
    SPACED_REVIEW = "spaced_review"
