"""Compact typed helpers for complete trilingual modules with stable activity IDs."""

from __future__ import annotations

from collections.abc import Sequence

from ...learning.activity_types import ActivityType
from ..localized_models import (
    LocalizedAssessmentItem,
    LocalizedAssessmentOption,
    LocalizedConceptBlock,
    LocalizedLearningObjective,
    LocalizedPracticeExercise,
    LocalizedText,
    LocalizedTutorSupportPacket,
    LocalizedWorkedExample,
)

Triple = tuple[str, str, str]
OptionSpec = tuple[str, Triple]


def t(spanish: str, english: str, danish: str) -> LocalizedText:
    """Create one required text in Spanish, English and Danish."""
    return LocalizedText(spanish=spanish, english=english, danish=danish)


def same(text: str) -> LocalizedText:
    """Create a language-neutral technical string."""
    return t(text, text, text)


def objective(objective_id: str, text: Triple) -> LocalizedLearningObjective:
    return LocalizedLearningObjective(objective_id=objective_id, statement=t(*text))


def concept(
    concept_id: str,
    title: Triple,
    body: Triple,
    key_points: Sequence[Triple],
) -> LocalizedConceptBlock:
    return LocalizedConceptBlock(
        concept_id=concept_id,
        title=t(*title),
        body=t(*body),
        key_points=tuple(t(*point) for point in key_points),
    )


def example(
    example_id: str,
    title: Triple,
    problem: Triple,
    reasoning: Sequence[Triple],
    code: str,
    expected_output: str,
    explanation: Triple,
) -> LocalizedWorkedExample:
    return LocalizedWorkedExample(
        example_id=example_id,
        title=t(*title),
        problem=t(*problem),
        reasoning=tuple(t(*step) for step in reasoning),
        code=same(code),
        expected_output=same(expected_output),
        explanation=t(*explanation),
    )


def practice(
    exercise_id: str,
    activity_type: ActivityType,
    prompt: Triple,
    hints: Sequence[Triple],
    solution: Triple,
    explanation: Triple,
    starter_code: str = "",
) -> LocalizedPracticeExercise:
    return LocalizedPracticeExercise(
        exercise_id=exercise_id,
        activity_type=activity_type,
        prompt=t(*prompt),
        hints=tuple(t(*hint) for hint in hints),
        solution=t(*solution),
        explanation=t(*explanation),
        starter_code=same(starter_code) if starter_code else None,
    )


def option(option_id: str, text: Triple) -> LocalizedAssessmentOption:
    return LocalizedAssessmentOption(option_id=option_id, text=t(*text))


def objective_mcq(
    item_id: str,
    prompt: Triple,
    options: Sequence[OptionSpec],
    correct_option_id: str,
    explanation: Triple,
) -> LocalizedAssessmentItem:
    return LocalizedAssessmentItem(
        item_id=item_id,
        activity_type=ActivityType.MULTIPLE_CHOICE,
        prompt=t(*prompt),
        options=tuple(option(option_id, text) for option_id, text in options),
        correct_option_ids=(correct_option_id,),
        accepted_answers=(),
        explanation=t(*explanation),
    )


def objective_tf(
    item_id: str,
    prompt: Triple,
    *,
    correct: bool,
    explanation: Triple,
) -> LocalizedAssessmentItem:
    return LocalizedAssessmentItem(
        item_id=item_id,
        activity_type=ActivityType.TRUE_FALSE,
        prompt=t(*prompt),
        options=(
            option("true", ("Verdadero", "True", "Sandt")),
            option("false", ("Falso", "False", "Falsk")),
        ),
        correct_option_ids=("true" if correct else "false",),
        accepted_answers=(),
        explanation=t(*explanation),
    )


def authored_item(
    item_id: str,
    activity_type: ActivityType,
    prompt: Triple,
    accepted_answers: Sequence[Triple],
    explanation: Triple,
    *,
    options: Sequence[OptionSpec] = (),
    correct_option_ids: Sequence[str] = (),
    rubric: Sequence[Triple] = (),
) -> LocalizedAssessmentItem:
    return LocalizedAssessmentItem(
        item_id=item_id,
        activity_type=activity_type,
        prompt=t(*prompt),
        options=tuple(option(option_id, text) for option_id, text in options),
        correct_option_ids=tuple(correct_option_ids),
        accepted_answers=tuple(t(*answer) for answer in accepted_answers),
        explanation=t(*explanation),
        rubric=tuple(t(*criterion) for criterion in rubric),
    )


def tutor_support(
    canonical_explanation: Triple,
    knowledge_fragments: Sequence[Triple],
    common_misconceptions: Sequence[Triple],
    socratic_questions: Sequence[Triple],
    grading_criteria: Sequence[Triple],
    response_constraints: Sequence[Triple],
    source_basis: Sequence[str],
) -> LocalizedTutorSupportPacket:
    return LocalizedTutorSupportPacket(
        canonical_explanation=t(*canonical_explanation),
        knowledge_fragments=tuple(t(*value) for value in knowledge_fragments),
        common_misconceptions=tuple(t(*value) for value in common_misconceptions),
        socratic_questions=tuple(t(*value) for value in socratic_questions),
        grading_criteria=tuple(t(*value) for value in grading_criteria),
        response_constraints=tuple(t(*value) for value in response_constraints),
        source_basis=tuple(source_basis),
    )


__all__ = [
    "Triple",
    "authored_item",
    "concept",
    "example",
    "objective",
    "objective_mcq",
    "objective_tf",
    "option",
    "practice",
    "same",
    "t",
    "tutor_support",
]
