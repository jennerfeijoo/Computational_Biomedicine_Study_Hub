from __future__ import annotations

import pytest

from computational_biomedicine_study_hub.content.dm857 import (
    LOCALIZED_MODULE_04_FUNCTIONS,
    LOCALIZED_MODULE_05_STRINGS,
    LOCALIZED_MODULE_06_SEQUENCES,
    LOCALIZED_OBJECTIVE_QUESTION_BANK_04,
    LOCALIZED_OBJECTIVE_QUESTION_BANK_05,
    LOCALIZED_OBJECTIVE_QUESTION_BANK_06,
    MODULE_04_FUNCTIONS,
    MODULE_05_STRINGS,
    MODULE_06_SEQUENCES,
    OBJECTIVE_QUESTION_BANK_04,
    OBJECTIVE_QUESTION_BANK_05,
    OBJECTIVE_QUESTION_BANK_06,
    materialize_module_04_question_bank,
    materialize_module_05_question_bank,
    materialize_module_06_question_bank,
)
from computational_biomedicine_study_hub.content.localized_models import (
    LocalizedAssessmentItem,
    LocalizedLearningModule,
)
from computational_biomedicine_study_hub.content.models import AssessmentItem, LearningModule
from computational_biomedicine_study_hub.i18n import AppLocale
from computational_biomedicine_study_hub.learning.activity_types import ActivityType

MODULE_CASES = (
    (
        "dm857.m04",
        LOCALIZED_MODULE_04_FUNCTIONS,
        MODULE_04_FUNCTIONS,
        LOCALIZED_OBJECTIVE_QUESTION_BANK_04,
        OBJECTIVE_QUESTION_BANK_04,
        materialize_module_04_question_bank,
        {
            AppLocale.SPANISH_SPAIN: "Funciones",
            AppLocale.ENGLISH: "Functions",
            AppLocale.DANISH_DENMARK: "Funktioner",
        },
    ),
    (
        "dm857.m05",
        LOCALIZED_MODULE_05_STRINGS,
        MODULE_05_STRINGS,
        LOCALIZED_OBJECTIVE_QUESTION_BANK_05,
        OBJECTIVE_QUESTION_BANK_05,
        materialize_module_05_question_bank,
        {
            AppLocale.SPANISH_SPAIN: "Cadenas",
            AppLocale.ENGLISH: "Strings",
            AppLocale.DANISH_DENMARK: "Strenge",
        },
    ),
    (
        "dm857.m06",
        LOCALIZED_MODULE_06_SEQUENCES,
        MODULE_06_SEQUENCES,
        LOCALIZED_OBJECTIVE_QUESTION_BANK_06,
        OBJECTIVE_QUESTION_BANK_06,
        materialize_module_06_question_bank,
        {
            AppLocale.SPANISH_SPAIN: "Listas",
            AppLocale.ENGLISH: "Lists",
            AppLocale.DANISH_DENMARK: "Lister",
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
def test_new_modules_have_complete_learning_components(
    module_id: str,
    localized_module: LocalizedLearningModule,
    runtime_module: LearningModule,
    localized_bank: tuple[LocalizedAssessmentItem, ...],
    runtime_bank: tuple[AssessmentItem, ...],
    materialize_bank: object,
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
def test_new_modules_materialize_completely_in_all_locales(
    module_id: str,
    localized_module: LocalizedLearningModule,
    runtime_module: LearningModule,
    localized_bank: tuple[LocalizedAssessmentItem, ...],
    runtime_bank: tuple[AssessmentItem, ...],
    materialize_bank: object,
    title_prefixes: dict[AppLocale, str],
) -> None:
    del runtime_module, localized_bank, runtime_bank
    assert callable(materialize_bank)

    for locale in AppLocale:
        module = localized_module.materialize(locale)
        bank = materialize_bank(locale)  # type: ignore[operator]

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
def test_new_module_banks_are_unique_objective_and_locale_independent(
    module_id: str,
    localized_module: LocalizedLearningModule,
    runtime_module: LearningModule,
    localized_bank: tuple[LocalizedAssessmentItem, ...],
    runtime_bank: tuple[AssessmentItem, ...],
    materialize_bank: object,
    title_prefixes: dict[AppLocale, str],
) -> None:
    del localized_module, runtime_module, title_prefixes
    assert callable(materialize_bank)

    assert len(localized_bank) == 30
    assert len(runtime_bank) == 30
    assert len({item.item_id for item in localized_bank}) == 30
    assert all(item.item_id.startswith(f"{module_id}.bank.") for item in localized_bank)
    assert all(
        item.activity_type in {ActivityType.MULTIPLE_CHOICE, ActivityType.TRUE_FALSE}
        for item in localized_bank
    )

    banks = {locale: materialize_bank(locale) for locale in AppLocale}  # type: ignore[operator]
    reference_ids = tuple(item.item_id for item in runtime_bank)
    reference_option_ids = tuple(item.option_ids for item in runtime_bank)
    reference_correct_ids = tuple(item.correct_option_ids for item in runtime_bank)

    for locale, bank in banks.items():
        assert tuple(item.item_id for item in bank) == reference_ids
        assert tuple(item.option_ids for item in bank) == reference_option_ids
        assert tuple(item.correct_option_ids for item in bank) == reference_correct_ids
        assert len({item.prompt for item in bank}) == len(bank), locale
        assert all(len(item.correct_option_ids) == 1 for item in bank)
        assert all(
            set(item.correct_option_ids).issubset(set(item.option_ids)) for item in bank
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
def test_new_modules_have_retrieval_ready_tutor_support(
    module_id: str,
    localized_module: LocalizedLearningModule,
    runtime_module: LearningModule,
    localized_bank: tuple[LocalizedAssessmentItem, ...],
    runtime_bank: tuple[AssessmentItem, ...],
    materialize_bank: object,
    title_prefixes: dict[AppLocale, str],
) -> None:
    del localized_module, localized_bank, runtime_bank, materialize_bank, title_prefixes
    support = runtime_module.tutor_support
    documents = runtime_module.tutor_documents()

    assert runtime_module.module_id == module_id
    assert len(support.canonical_explanation) >= 900
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
def test_new_modules_cover_varied_assessment_and_safe_teaching_contexts(
    module_id: str,
    localized_module: LocalizedLearningModule,
    runtime_module: LearningModule,
    localized_bank: tuple[LocalizedAssessmentItem, ...],
    runtime_bank: tuple[AssessmentItem, ...],
    materialize_bank: object,
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
