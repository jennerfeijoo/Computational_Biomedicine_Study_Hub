from __future__ import annotations

from computational_biomedicine_study_hub.content.dm857 import (
    LOCALIZED_MODULE_03_ITERATION,
    LOCALIZED_OBJECTIVE_QUESTION_BANK_03,
    MODULE_03_ITERATION,
    OBJECTIVE_QUESTION_BANK_03,
    materialize_module_03_question_bank,
)
from computational_biomedicine_study_hub.i18n import AppLocale
from computational_biomedicine_study_hub.learning.activity_types import ActivityType


def test_module_three_has_complete_learning_components() -> None:
    module = MODULE_03_ITERATION

    assert module.course_code == "DM857"
    assert module.module_id == "dm857.m03"
    assert len(module.objectives) == 8
    assert len(module.concepts) == 8
    assert len(module.worked_examples) == 5
    assert len(module.practice_exercises) == 12
    assert len(module.assessment_items) == 14


def test_module_three_covers_iteration_and_varied_activity_types() -> None:
    module = MODULE_03_ITERATION
    concept_ids = {concept.concept_id for concept in module.concepts}
    practice_types = {exercise.activity_type for exercise in module.practice_exercises}
    assessment_types = {item.activity_type for item in module.assessment_items}

    assert {
        "iteration-as-state-transition",
        "while-loop-anatomy",
        "termination-progress-and-invariants",
        "for-loop-and-range",
        "counters-accumulators-and-best-values",
        "sentinels-break-and-continue",
        "nested-loops-and-operation-count",
        "loop-tracing-and-testing",
    } == concept_ids
    assert {
        ActivityType.CODE_TRACING,
        ActivityType.DEBUGGING,
        ActivityType.FILL_IN_THE_BLANK,
        ActivityType.CODE_COMPLETION,
        ActivityType.SHORT_ANSWER,
        ActivityType.ORDERING,
        ActivityType.ORAL_EXPLANATION,
    }.issubset(practice_types)
    assert {
        ActivityType.MULTIPLE_CHOICE,
        ActivityType.TRUE_FALSE,
        ActivityType.CODE_TRACING,
        ActivityType.FILL_IN_THE_BLANK,
        ActivityType.DEBUGGING,
        ActivityType.MULTIPLE_SELECT,
        ActivityType.MATCHING,
        ActivityType.ORDERING,
        ActivityType.SHORT_ANSWER,
        ActivityType.CODE_COMPLETION,
        ActivityType.DATA_INTERPRETATION,
        ActivityType.ORAL_EXPLANATION,
    }.issubset(assessment_types)


def test_module_three_materializes_complete_spanish_english_and_danish_versions() -> None:
    modules = {locale: LOCALIZED_MODULE_03_ITERATION.materialize(locale) for locale in AppLocale}

    for module in modules.values():
        assert module.module_id == "dm857.m03"
        assert len(module.objectives) == 8
        assert len(module.concepts) == 8
        assert len(module.worked_examples) == 5
        assert len(module.practice_exercises) == 12
        assert len(module.assessment_items) == 14
        assert all(document.text.strip() for document in module.tutor_documents())

    assert modules[AppLocale.SPANISH_SPAIN].title.startswith("Iteración controlada")
    assert modules[AppLocale.ENGLISH].title.startswith("Controlled iteration")
    assert modules[AppLocale.DANISH_DENMARK].title.startswith("Kontrolleret iteration")


def test_module_three_tutor_support_is_substantive_and_retrieval_ready() -> None:
    module = MODULE_03_ITERATION
    support = module.tutor_support
    documents = module.tutor_documents()

    assert len(support.canonical_explanation) >= 1800
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


def test_module_three_randomized_bank_is_large_unique_and_trilingual() -> None:
    assert len(LOCALIZED_OBJECTIVE_QUESTION_BANK_03) == 30
    assert len(OBJECTIVE_QUESTION_BANK_03) == 30
    assert len({item.item_id for item in OBJECTIVE_QUESTION_BANK_03}) == 30
    assert all(
        item.activity_type in {ActivityType.MULTIPLE_CHOICE, ActivityType.TRUE_FALSE}
        for item in OBJECTIVE_QUESTION_BANK_03
    )

    for locale in AppLocale:
        bank = materialize_module_03_question_bank(locale)
        assert len(bank) == 30
        assert [item.item_id for item in bank] == [
            item.item_id for item in OBJECTIVE_QUESTION_BANK_03
        ]
        assert len({item.prompt for item in bank}) == len(bank)
        assert all(item.prompt.strip() for item in bank)
        assert all(item.explanation.strip() for item in bank)
        assert all(len(item.correct_answers) == 1 for item in bank)
        assert all(set(item.correct_answers).issubset(set(item.options)) for item in bank)


def test_module_three_uses_safe_terminology_and_teaching_disclaimers() -> None:
    required_phrases = {
        AppLocale.SPANISH_SPAIN: (
            "escenarios de programación didácticos",
            "no representan protocolos",
        ),
        AppLocale.ENGLISH: ("programming exercises", "not protocols"),
        AppLocale.DANISH_DENMARK: ("programmeringsøvelser", "ikke protokoller"),
    }

    for locale in AppLocale:
        module = LOCALIZED_MODULE_03_ITERATION.materialize(locale)
        exported = "\n".join(document.text for document in module.tutor_documents()).casefold()

        assert "corrida" not in exported
        assert all(phrase in exported for phrase in required_phrases[locale])
