from __future__ import annotations

from collections.abc import Callable

import pytest

from computational_biomedicine_study_hub.content.dm857 import (
    LOCALIZED_MODULE_07_MAPPINGS_SETS,
    LOCALIZED_MODULE_08_FILES_EXCEPTIONS,
    LOCALIZED_MODULE_09_RECURSION,
    LOCALIZED_OBJECTIVE_QUESTION_BANK_07,
    LOCALIZED_OBJECTIVE_QUESTION_BANK_08,
    LOCALIZED_OBJECTIVE_QUESTION_BANK_09,
    MODULE_07_MAPPINGS_SETS,
    MODULE_08_FILES_EXCEPTIONS,
    MODULE_09_RECURSION,
    OBJECTIVE_QUESTION_BANK_07,
    OBJECTIVE_QUESTION_BANK_08,
    OBJECTIVE_QUESTION_BANK_09,
    materialize_module_07_question_bank,
    materialize_module_08_question_bank,
    materialize_module_09_question_bank,
)
from computational_biomedicine_study_hub.content.localized_models import (
    LocalizedAssessmentItem,
    LocalizedLearningModule,
)
from computational_biomedicine_study_hub.content.models import AssessmentItem, LearningModule
from computational_biomedicine_study_hub.i18n import AppLocale
from computational_biomedicine_study_hub.learning.activity_types import ActivityType

BankMaterializer = Callable[[AppLocale | str], tuple[AssessmentItem, ...]]
ModuleCase = tuple[
    str,
    LocalizedLearningModule,
    LearningModule,
    tuple[LocalizedAssessmentItem, ...],
    tuple[AssessmentItem, ...],
    BankMaterializer,
    dict[AppLocale, str],
]

MODULE_CASES: tuple[ModuleCase, ...] = (
    (
        "dm857.m07",
        LOCALIZED_MODULE_07_MAPPINGS_SETS,
        MODULE_07_MAPPINGS_SETS,
        LOCALIZED_OBJECTIVE_QUESTION_BANK_07,
        OBJECTIVE_QUESTION_BANK_07,
        materialize_module_07_question_bank,
        {
            AppLocale.SPANISH_SPAIN: "Diccionarios",
            AppLocale.ENGLISH: "Dictionaries",
            AppLocale.DANISH_DENMARK: "Ordbøger",
        },
    ),
    (
        "dm857.m08",
        LOCALIZED_MODULE_08_FILES_EXCEPTIONS,
        MODULE_08_FILES_EXCEPTIONS,
        LOCALIZED_OBJECTIVE_QUESTION_BANK_08,
        OBJECTIVE_QUESTION_BANK_08,
        materialize_module_08_question_bank,
        {
            AppLocale.SPANISH_SPAIN: "Archivos",
            AppLocale.ENGLISH: "Files",
            AppLocale.DANISH_DENMARK: "Filer",
        },
    ),
    (
        "dm857.m09",
        LOCALIZED_MODULE_09_RECURSION,
        MODULE_09_RECURSION,
        LOCALIZED_OBJECTIVE_QUESTION_BANK_09,
        OBJECTIVE_QUESTION_BANK_09,
        materialize_module_09_question_bank,
        {
            AppLocale.SPANISH_SPAIN: "Recursión",
            AppLocale.ENGLISH: "Recursion",
            AppLocale.DANISH_DENMARK: "Rekursion",
        },
    ),
)


@pytest.mark.parametrize(
    (
        "module_id",
        "localized_module",
        "runtime_module",
        "localized_bank",
        "runtime_bank",
        "materialize_bank",
        "title_prefixes",
    ),
    MODULE_CASES,
)
def test_modules_have_complete_learning_components(
    module_id: str,
    localized_module: LocalizedLearningModule,
    runtime_module: LearningModule,
    localized_bank: tuple[LocalizedAssessmentItem, ...],
    runtime_bank: tuple[AssessmentItem, ...],
    materialize_bank: BankMaterializer,
    title_prefixes: dict[AppLocale, str],
) -> None:
    del localized_module, localized_bank, materialize_bank, title_prefixes

    assert runtime_module.course_code == "DM857"
    assert runtime_module.module_id == module_id
    assert len(runtime_module.objectives) == 8
    assert len(runtime_module.concepts) == 8
    assert len(runtime_module.worked_examples) == 5
    assert len(runtime_module.practice_exercises) == 12
    assert len(runtime_module.assessment_items) == 14
    assert len(runtime_bank) == 30
    assert all(runtime_module.tutor_support.source_basis)


@pytest.mark.parametrize(
    (
        "module_id",
        "localized_module",
        "runtime_module",
        "localized_bank",
        "runtime_bank",
        "materialize_bank",
        "title_prefixes",
    ),
    MODULE_CASES,
)
def test_modules_materialize_completely_in_all_locales(
    module_id: str,
    localized_module: LocalizedLearningModule,
    runtime_module: LearningModule,
    localized_bank: tuple[LocalizedAssessmentItem, ...],
    runtime_bank: tuple[AssessmentItem, ...],
    materialize_bank: BankMaterializer,
    title_prefixes: dict[AppLocale, str],
) -> None:
    del runtime_module, localized_bank, runtime_bank

    for locale in AppLocale:
        module = localized_module.materialize(locale)
        bank = materialize_bank(locale)

        assert module.module_id == module_id
        assert module.title.startswith(title_prefixes[locale])
        assert len(module.objectives) == 8
        assert len(module.concepts) == 8
        assert len(module.worked_examples) == 5
        assert len(module.practice_exercises) == 12
        assert len(module.assessment_items) == 14
        assert len(bank) == 30
        assert all(document.text.strip() for document in module.tutor_documents())
        assert all(item.prompt.strip() for item in bank)
        assert all(item.explanation.strip() for item in bank)


@pytest.mark.parametrize(
    (
        "module_id",
        "localized_module",
        "runtime_module",
        "localized_bank",
        "runtime_bank",
        "materialize_bank",
        "title_prefixes",
    ),
    MODULE_CASES,
)
def test_objective_banks_are_unique_and_locale_independent(
    module_id: str,
    localized_module: LocalizedLearningModule,
    runtime_module: LearningModule,
    localized_bank: tuple[LocalizedAssessmentItem, ...],
    runtime_bank: tuple[AssessmentItem, ...],
    materialize_bank: BankMaterializer,
    title_prefixes: dict[AppLocale, str],
) -> None:
    del localized_module, runtime_module, title_prefixes

    assert len(localized_bank) == 30
    assert len(runtime_bank) == 30
    assert len({item.item_id for item in localized_bank}) == 30
    assert all(item.item_id.startswith(f"{module_id}.bank.") for item in localized_bank)
    assert all(
        item.activity_type in {ActivityType.MULTIPLE_CHOICE, ActivityType.TRUE_FALSE}
        for item in localized_bank
    )

    banks = {locale: materialize_bank(locale) for locale in AppLocale}
    reference_ids = tuple(item.item_id for item in runtime_bank)
    reference_option_ids = tuple(item.option_ids for item in runtime_bank)
    reference_correct_ids = tuple(item.correct_option_ids for item in runtime_bank)

    for locale, bank in banks.items():
        assert tuple(item.item_id for item in bank) == reference_ids
        assert tuple(item.option_ids for item in bank) == reference_option_ids
        assert tuple(item.correct_option_ids for item in bank) == reference_correct_ids
        assert len({item.prompt for item in bank}) == len(bank), locale
        assert all(len(item.correct_option_ids) == 1 for item in bank)
        assert all(set(item.correct_option_ids).issubset(set(item.option_ids)) for item in bank)


@pytest.mark.parametrize(
    (
        "module_id",
        "localized_module",
        "runtime_module",
        "localized_bank",
        "runtime_bank",
        "materialize_bank",
        "title_prefixes",
    ),
    MODULE_CASES,
)
def test_modules_have_retrieval_ready_tutor_support_and_valid_example_code(
    module_id: str,
    localized_module: LocalizedLearningModule,
    runtime_module: LearningModule,
    localized_bank: tuple[LocalizedAssessmentItem, ...],
    runtime_bank: tuple[AssessmentItem, ...],
    materialize_bank: BankMaterializer,
    title_prefixes: dict[AppLocale, str],
) -> None:
    del localized_module, localized_bank, runtime_bank, materialize_bank, title_prefixes
    support = runtime_module.tutor_support
    documents = runtime_module.tutor_documents()

    assert runtime_module.module_id == module_id
    assert len(support.canonical_explanation) >= 1200
    assert len(support.knowledge_fragments) == 14
    assert len(support.common_misconceptions) == 12
    assert len(support.socratic_questions) == 12
    assert len(support.grading_criteria) == 10
    assert len(support.response_constraints) == 9
    assert len(documents) == (
        2
        + len(runtime_module.concepts)
        + len(runtime_module.worked_examples)
        + len(runtime_module.practice_exercises)
        + len(runtime_module.assessment_items)
    )
    assert len({document.document_id for document in documents}) == len(documents)
    assert all(runtime_module.course_code in document.tags for document in documents)
    assert all(runtime_module.module_id in document.tags for document in documents)

    for example_item in runtime_module.worked_examples:
        compile(example_item.code, f"<{example_item.example_id}>", "exec")


@pytest.mark.parametrize(
    (
        "module_id",
        "localized_module",
        "runtime_module",
        "localized_bank",
        "runtime_bank",
        "materialize_bank",
        "title_prefixes",
    ),
    MODULE_CASES,
)
def test_modules_cover_varied_assessment_and_safe_teaching_contexts(
    module_id: str,
    localized_module: LocalizedLearningModule,
    runtime_module: LearningModule,
    localized_bank: tuple[LocalizedAssessmentItem, ...],
    runtime_bank: tuple[AssessmentItem, ...],
    materialize_bank: BankMaterializer,
    title_prefixes: dict[AppLocale, str],
) -> None:
    del module_id, localized_bank, runtime_bank, materialize_bank, title_prefixes
    assessment_types = {item.activity_type for item in runtime_module.assessment_items}
    practice_types = {item.activity_type for item in runtime_module.practice_exercises}

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

    required_phrases = {
        AppLocale.SPANISH_SPAIN: ("didácticos", "no representan protocolos"),
        AppLocale.ENGLISH: ("programming exercises", "not protocols"),
        AppLocale.DANISH_DENMARK: ("programmeringsøvelser", "ikke protokoller"),
    }
    for locale in AppLocale:
        module = localized_module.materialize(locale)
        exported = "\n".join(document.text for document in module.tutor_documents()).casefold()
        assert "corrida" not in exported
        assert all(phrase in exported for phrase in required_phrases[locale])
