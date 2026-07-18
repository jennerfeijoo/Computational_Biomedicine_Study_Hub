from __future__ import annotations

from computational_biomedicine_study_hub.content.dm857 import (
    LOCALIZED_MODULE_02_CONDITIONALS,
    LOCALIZED_OBJECTIVE_QUESTION_BANK_02,
    MODULE_02_CONDITIONALS,
    OBJECTIVE_QUESTION_BANK_02,
    materialize_module_02_question_bank,
)
from computational_biomedicine_study_hub.i18n import AppLocale
from computational_biomedicine_study_hub.learning.activity_types import ActivityType


def test_module_two_has_complete_learning_components() -> None:
    module = MODULE_02_CONDITIONALS

    assert module.course_code == "DM857"
    assert module.module_id == "dm857.m02"
    assert len(module.objectives) == 7
    assert len(module.concepts) == 7
    assert len(module.worked_examples) == 4
    assert len(module.practice_exercises) == 10
    assert len(module.assessment_items) == 12


def test_module_two_covers_conditionals_and_varied_activity_types() -> None:
    module = MODULE_02_CONDITIONALS
    concept_ids = {concept.concept_id for concept in module.concepts}
    practice_types = {exercise.activity_type for exercise in module.practice_exercises}
    assessment_types = {item.activity_type for item in module.assessment_items}

    assert {
        "boolean-values-and-predicates",
        "comparison-operators",
        "logical-operators-and-precedence",
        "short-circuit-evaluation",
        "if-elif-else-control-flow",
        "compound-versus-nested-conditionals",
        "validation-boundaries-and-branch-testing",
    } == concept_ids
    assert {
        ActivityType.CODE_TRACING,
        ActivityType.MATCHING,
        ActivityType.CODE_COMPLETION,
        ActivityType.DEBUGGING,
        ActivityType.FILL_IN_THE_BLANK,
        ActivityType.SHORT_ANSWER,
        ActivityType.ORAL_EXPLANATION,
    }.issubset(practice_types)
    assert {
        ActivityType.MULTIPLE_CHOICE,
        ActivityType.TRUE_FALSE,
        ActivityType.MULTIPLE_SELECT,
        ActivityType.CODE_TRACING,
        ActivityType.FILL_IN_THE_BLANK,
        ActivityType.DEBUGGING,
        ActivityType.ORDERING,
        ActivityType.MATCHING,
        ActivityType.SHORT_ANSWER,
        ActivityType.CODE_COMPLETION,
        ActivityType.DATA_INTERPRETATION,
    }.issubset(assessment_types)


def test_module_two_materializes_complete_spanish_english_and_danish_versions() -> None:
    modules = {locale: LOCALIZED_MODULE_02_CONDITIONALS.materialize(locale) for locale in AppLocale}

    for module in modules.values():
        assert module.module_id == "dm857.m02"
        assert len(module.objectives) == 7
        assert len(module.concepts) == 7
        assert len(module.worked_examples) == 4
        assert len(module.practice_exercises) == 10
        assert len(module.assessment_items) == 12
        assert all(document.text.strip() for document in module.tutor_documents())

    assert modules[AppLocale.SPANISH_SPAIN].title.startswith("Lógica booleana")
    assert modules[AppLocale.ENGLISH].title.startswith("Boolean logic")
    assert modules[AppLocale.DANISH_DENMARK].title.startswith("Boolesk logik")


def test_module_two_tutor_support_is_substantive_and_retrieval_ready() -> None:
    module = MODULE_02_CONDITIONALS
    support = module.tutor_support
    documents = module.tutor_documents()

    assert len(support.canonical_explanation) >= 900
    assert len(support.knowledge_fragments) == 12
    assert len(support.common_misconceptions) == 10
    assert len(support.socratic_questions) == 10
    assert len(support.grading_criteria) == 9
    assert len(support.response_constraints) == 8
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


def test_module_two_randomized_bank_is_large_unique_and_trilingual() -> None:
    assert len(LOCALIZED_OBJECTIVE_QUESTION_BANK_02) == 24
    assert len(OBJECTIVE_QUESTION_BANK_02) == 24
    assert len({item.item_id for item in OBJECTIVE_QUESTION_BANK_02}) == 24
    assert all(
        item.activity_type in {ActivityType.MULTIPLE_CHOICE, ActivityType.TRUE_FALSE}
        for item in OBJECTIVE_QUESTION_BANK_02
    )

    for locale in AppLocale:
        bank = materialize_module_02_question_bank(locale)
        assert len(bank) == 24
        assert [item.item_id for item in bank] == [
            item.item_id for item in OBJECTIVE_QUESTION_BANK_02
        ]
        assert all(item.prompt.strip() for item in bank)
        assert all(item.explanation.strip() for item in bank)
        assert all(len(item.correct_answers) == 1 for item in bank)
        assert all(set(item.correct_answers).issubset(set(item.options)) for item in bank)


def test_module_two_uses_safe_terminology_and_non_clinical_boundaries() -> None:
    required_constraint = {
        AppLocale.SPANISH_SPAIN: (
            "no presentar umbrales didácticos como recomendaciones clínicas o de laboratorio"
        ),
        AppLocale.ENGLISH: (
            "do not present teaching thresholds as clinical or laboratory recommendations"
        ),
        AppLocale.DANISH_DENMARK: (
            "præsentér ikke undervisningsgrænser som kliniske eller laboratoriemæssige anbefalinger"
        ),
    }

    for locale in AppLocale:
        module = LOCALIZED_MODULE_02_CONDITIONALS.materialize(locale)
        exported = "\n".join(document.text for document in module.tutor_documents()).casefold()

        assert "corrida" not in exported
        assert required_constraint[locale] in exported
