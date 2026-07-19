"""Academic-content tests for DM857 module 14."""

from __future__ import annotations

import pytest

from computational_biomedicine_study_hub.content.dm857 import (
    LOCALIZED_MODULE_14_TESTING_DEBUGGING_QUALITY,
    LOCALIZED_OBJECTIVE_QUESTION_BANK_14,
    MODULE_14_TESTING_DEBUGGING_QUALITY,
    OBJECTIVE_QUESTION_BANK_14,
    materialize_module_14_question_bank,
)
from computational_biomedicine_study_hub.i18n import AppLocale
from computational_biomedicine_study_hub.learning.activity_types import ActivityType

TITLE_PREFIXES = {
    AppLocale.SPANISH_SPAIN: "Testing",
    AppLocale.ENGLISH: "Testing",
    AppLocale.DANISH_DENMARK: "Testning",
}


def test_module_14_has_complete_learning_components() -> None:
    module = MODULE_14_TESTING_DEBUGGING_QUALITY

    assert module.course_code == "DM857"
    assert module.module_id == "dm857.m14"
    assert len(module.objectives) == 8
    assert len(module.concepts) == 8
    assert len(module.worked_examples) == 5
    assert len(module.practice_exercises) == 12
    assert len(module.assessment_items) == 14
    assert len(OBJECTIVE_QUESTION_BANK_14) == 30
    assert all(module.tutor_support.source_basis)


@pytest.mark.parametrize("locale", tuple(AppLocale))
def test_module_14_materializes_completely_in_every_locale(locale: AppLocale) -> None:
    module = LOCALIZED_MODULE_14_TESTING_DEBUGGING_QUALITY.materialize(locale)
    bank = materialize_module_14_question_bank(locale)

    assert module.module_id == "dm857.m14"
    assert module.title.startswith(TITLE_PREFIXES[locale])
    assert len(module.objectives) == 8
    assert len(module.concepts) == 8
    assert len(module.worked_examples) == 5
    assert len(module.practice_exercises) == 12
    assert len(module.assessment_items) == 14
    assert len(bank) == 30
    assert all(document.text.strip() for document in module.tutor_documents())
    assert all(item.prompt.strip() for item in bank)
    assert all(item.explanation.strip() for item in bank)


def test_module_14_objective_bank_has_stable_locale_independent_identity() -> None:
    assert len(LOCALIZED_OBJECTIVE_QUESTION_BANK_14) == 30
    assert len({item.item_id for item in LOCALIZED_OBJECTIVE_QUESTION_BANK_14}) == 30
    assert all(
        item.item_id.startswith("dm857.m14.bank.") for item in LOCALIZED_OBJECTIVE_QUESTION_BANK_14
    )
    assert all(
        item.activity_type in {ActivityType.MULTIPLE_CHOICE, ActivityType.TRUE_FALSE}
        for item in LOCALIZED_OBJECTIVE_QUESTION_BANK_14
    )

    reference = materialize_module_14_question_bank(AppLocale.SPANISH_SPAIN)
    reference_ids = tuple(item.item_id for item in reference)
    reference_option_ids = tuple(item.option_ids for item in reference)
    reference_correct_ids = tuple(item.correct_option_ids for item in reference)

    for locale in AppLocale:
        bank = materialize_module_14_question_bank(locale)
        assert tuple(item.item_id for item in bank) == reference_ids
        assert tuple(item.option_ids for item in bank) == reference_option_ids
        assert tuple(item.correct_option_ids for item in bank) == reference_correct_ids
        assert len({item.prompt for item in bank}) == len(bank)
        assert all(len(item.correct_option_ids) == 1 for item in bank)
        assert all(set(item.correct_option_ids).issubset(set(item.option_ids)) for item in bank)


@pytest.mark.parametrize("locale", tuple(AppLocale))
def test_module_14_has_retrieval_ready_tutor_support(locale: AppLocale) -> None:
    module = LOCALIZED_MODULE_14_TESTING_DEBUGGING_QUALITY.materialize(locale)
    support = module.tutor_support
    documents = module.tutor_documents()

    assert len(support.canonical_explanation) >= 1200
    assert len(support.knowledge_fragments) == 14
    assert len(support.common_misconceptions) == 12
    assert len(support.socratic_questions) == 12
    assert len(support.grading_criteria) == 10
    assert len(support.response_constraints) == 9
    assert len(documents) == (
        2
        + len(module.concepts)
        + len(module.worked_examples)
        + len(module.practice_exercises)
        + len(module.assessment_items)
    )
    assert len({document.document_id for document in documents}) == len(documents)
    assert all(module.course_code in document.tags for document in documents)
    assert all(module.module_id in document.tags for document in documents)


def test_module_14_examples_and_starter_code_compile() -> None:
    module = MODULE_14_TESTING_DEBUGGING_QUALITY

    for example_item in module.worked_examples:
        compile(example_item.code, f"<{example_item.example_id}>", "exec")
    for exercise in module.practice_exercises:
        if exercise.starter_code:
            compile(exercise.starter_code, f"<{exercise.exercise_id}>", "exec")


def test_module_14_covers_varied_assessment_types() -> None:
    module = MODULE_14_TESTING_DEBUGGING_QUALITY
    assessment_types = {item.activity_type for item in module.assessment_items}
    practice_types = {item.activity_type for item in module.practice_exercises}

    assert {
        ActivityType.CODE_TRACING,
        ActivityType.DEBUGGING,
        ActivityType.FILL_IN_THE_BLANK,
        ActivityType.CODE_COMPLETION,
        ActivityType.SHORT_ANSWER,
        ActivityType.ORDERING,
        ActivityType.ORAL_EXPLANATION,
        ActivityType.DATA_INTERPRETATION,
        ActivityType.PIPELINE_DESIGN,
    }.issubset(assessment_types | practice_types)
    assert {
        ActivityType.MULTIPLE_SELECT,
        ActivityType.MATCHING,
        ActivityType.ORDERING,
    }.issubset(assessment_types)


@pytest.mark.parametrize(
    ("locale", "required_phrases"),
    (
        (AppLocale.SPANISH_SPAIN, ("ejercicios didácticos", "no representan protocolos")),
        (AppLocale.ENGLISH, ("teaching exercises", "not laboratory protocols")),
        (AppLocale.DANISH_DENMARK, ("undervisningsøvelser", "ikke laboratorieprotokoller")),
    ),
)
def test_module_14_uses_safe_teaching_context(
    locale: AppLocale,
    required_phrases: tuple[str, ...],
) -> None:
    module = LOCALIZED_MODULE_14_TESTING_DEBUGGING_QUALITY.materialize(locale)
    exported = "\n".join(document.text for document in module.tutor_documents()).casefold()

    assert all(phrase in exported for phrase in required_phrases)
