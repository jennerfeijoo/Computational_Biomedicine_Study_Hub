from __future__ import annotations

from computational_biomedicine_study_hub.content.dm857 import (
    MODULE_01_FOUNDATIONS,
)
from computational_biomedicine_study_hub.learning.activity_types import ActivityType


def test_module_one_has_complete_learning_components() -> None:
    module = MODULE_01_FOUNDATIONS

    assert module.course_code == "DM857"
    assert module.module_id == "dm857.m01"
    assert len(module.objectives) >= 6
    assert len(module.concepts) >= 6
    assert len(module.worked_examples) >= 3
    assert len(module.practice_exercises) >= 8
    assert len(module.assessment_items) >= 10


def test_module_one_covers_varied_retrieval_and_assessment_modes() -> None:
    practice_types = {
        exercise.activity_type for exercise in MODULE_01_FOUNDATIONS.practice_exercises
    }
    assessment_types = {item.activity_type for item in MODULE_01_FOUNDATIONS.assessment_items}

    assert {
        ActivityType.CODE_TRACING,
        ActivityType.DEBUGGING,
        ActivityType.FILL_IN_THE_BLANK,
        ActivityType.ORAL_EXPLANATION,
    }.issubset(practice_types)
    assert {
        ActivityType.MULTIPLE_CHOICE,
        ActivityType.MULTIPLE_SELECT,
        ActivityType.TRUE_FALSE,
        ActivityType.MATCHING,
        ActivityType.ORDERING,
        ActivityType.CODE_COMPLETION,
    }.issubset(assessment_types)


def test_objective_and_content_identifiers_are_unique() -> None:
    module = MODULE_01_FOUNDATIONS

    identifier_groups = (
        [objective.objective_id for objective in module.objectives],
        [concept.concept_id for concept in module.concepts],
        [example.example_id for example in module.worked_examples],
        [exercise.exercise_id for exercise in module.practice_exercises],
        [item.item_id for item in module.assessment_items],
    )

    for identifiers in identifier_groups:
        assert len(identifiers) == len(set(identifiers))


def test_tutor_documents_are_complete_and_deterministic() -> None:
    module = MODULE_01_FOUNDATIONS

    first_build = module.tutor_documents()
    second_build = module.tutor_documents()

    assert first_build == second_build
    assert len(first_build) == (
        2
        + len(module.concepts)
        + len(module.worked_examples)
        + len(module.practice_exercises)
        + len(module.assessment_items)
    )
    assert len({document.document_id for document in first_build}) == len(first_build)
    assert all(document.text.strip() for document in first_build)
    assert all(module.course_code in document.tags for document in first_build)
    assert all(module.module_id in document.tags for document in first_build)


def test_tutor_support_is_substantive_and_bounded_to_the_module() -> None:
    support = MODULE_01_FOUNDATIONS.tutor_support

    assert len(support.canonical_explanation) >= 600
    assert len(support.knowledge_fragments) >= 8
    assert len(support.common_misconceptions) >= 6
    assert len(support.socratic_questions) >= 6
    assert len(support.grading_criteria) >= 6
    assert len(support.response_constraints) >= 6
    assert any("No introducir condicionales" in rule for rule in support.response_constraints)


def test_option_based_assessments_only_reference_declared_options() -> None:
    for item in MODULE_01_FOUNDATIONS.assessment_items:
        if item.options:
            assert set(item.correct_answers).issubset(set(item.options))
