"""Academic, localization, and integrity tests for the complete DM847 catalog."""

from __future__ import annotations

import pytest

from computational_biomedicine_study_hub.content.dm847 import (
    BUNDLES,
    LOCALIZED_BUNDLES,
    MODULES,
    OBJECTIVE_QUESTION_BANKS,
)
from computational_biomedicine_study_hub.i18n import AppLocale
from computational_biomedicine_study_hub.learning.activity_types import ActivityType

EXPECTED_IDS = tuple(f"dm847.m{number:02d}" for number in range(1, 11))


def test_dm847_catalog_has_ten_complete_modules() -> None:
    assert tuple(module.module_id for module in MODULES) == EXPECTED_IDS
    assert len(BUNDLES) == len(LOCALIZED_BUNDLES) == 10
    assert tuple(OBJECTIVE_QUESTION_BANKS) == EXPECTED_IDS

    for bundle in BUNDLES:
        module = bundle.module
        assert module.course_code == "DM847"
        assert len(module.objectives) >= 6
        assert len(module.concepts) >= 6
        assert len(module.worked_examples) >= 3
        assert len(module.practice_exercises) >= 8
        assert len(module.assessment_items) == 10
        assert len(bundle.objective_question_bank) == 20
        assert bundle.content_version == "1.0.0"


@pytest.mark.parametrize("locale", tuple(AppLocale))
def test_dm847_modules_materialize_in_every_locale(locale: AppLocale) -> None:
    for localized_bundle in LOCALIZED_BUNDLES:
        bundle = localized_bundle.materialize(locale)
        module = bundle.module
        bank = bundle.objective_question_bank

        assert module.title.strip()
        assert module.summary.strip()
        assert all(objective.statement.strip() for objective in module.objectives)
        assert all(concept.body.strip() for concept in module.concepts)
        assert all(example.problem.strip() for example in module.worked_examples)
        assert all(exercise.solution.strip() for exercise in module.practice_exercises)
        assert all(
            item.prompt.strip() and item.explanation.strip() for item in module.assessment_items
        )
        assert all(item.prompt.strip() and item.explanation.strip() for item in bank)
        assert all(document.text.strip() for document in module.tutor_documents())


@pytest.mark.parametrize("bundle_index", range(10))
def test_dm847_question_identity_is_stable_across_languages(bundle_index: int) -> None:
    localized_bundle = LOCALIZED_BUNDLES[bundle_index]
    reference = localized_bundle.materialize(AppLocale.SPANISH_SPAIN).objective_question_bank
    reference_ids = tuple(item.item_id for item in reference)
    reference_option_ids = tuple(item.option_ids for item in reference)
    reference_correct_ids = tuple(item.correct_option_ids for item in reference)

    for locale in AppLocale:
        bank = localized_bundle.materialize(locale).objective_question_bank
        assert tuple(item.item_id for item in bank) == reference_ids
        assert tuple(item.option_ids for item in bank) == reference_option_ids
        assert tuple(item.correct_option_ids for item in bank) == reference_correct_ids
        assert len({item.item_id for item in bank}) == 20
        assert all(item.item_id.startswith(f"{EXPECTED_IDS[bundle_index]}.bank.") for item in bank)
        assert all(len(item.correct_option_ids) == 1 for item in bank)
        assert all(set(item.correct_option_ids).issubset(set(item.option_ids)) for item in bank)


def test_dm847_examples_and_starter_code_compile() -> None:
    for module in MODULES:
        for example in module.worked_examples:
            compile(example.code, f"<{example.example_id}>", "exec")
        for exercise in module.practice_exercises:
            if exercise.starter_code:
                compile(exercise.starter_code, f"<{exercise.exercise_id}>", "exec")


@pytest.mark.parametrize("locale", tuple(AppLocale))
def test_dm847_tutor_support_is_retrieval_ready(locale: AppLocale) -> None:
    for localized_bundle in LOCALIZED_BUNDLES:
        module = localized_bundle.materialize(locale).module
        support = module.tutor_support
        documents = module.tutor_documents()

        assert len(support.canonical_explanation) >= 650
        assert len(support.knowledge_fragments) >= 6
        assert len(support.common_misconceptions) >= 6
        assert len(support.socratic_questions) >= 6
        assert len(support.grading_criteria) >= 6
        assert len(support.response_constraints) >= 5
        assert len(support.source_basis) >= 6
        assert len({document.document_id for document in documents}) == len(documents)
        assert all(module.course_code in document.tags for document in documents)
        assert all(module.module_id in document.tags for document in documents)


def test_dm847_practice_covers_the_supported_learning_cycle() -> None:
    practice_types = {
        exercise.activity_type for module in MODULES for exercise in module.practice_exercises
    }
    assessment_types = {
        item.activity_type for module in MODULES for item in module.assessment_items
    }

    assert {
        ActivityType.CODE_TRACING,
        ActivityType.DEBUGGING,
        ActivityType.FILL_IN_THE_BLANK,
        ActivityType.SHORT_ANSWER,
        ActivityType.ORAL_EXPLANATION,
        ActivityType.DATA_INTERPRETATION,
        ActivityType.PIPELINE_DESIGN,
        ActivityType.MATCHING,
        ActivityType.ORDERING,
    }.issubset(practice_types)
    assert {ActivityType.MULTIPLE_CHOICE, ActivityType.TRUE_FALSE}.issubset(assessment_types)


@pytest.mark.parametrize(
    ("locale", "constraint_marker"),
    (
        (AppLocale.SPANISH_SPAIN, "no "),
        (AppLocale.ENGLISH, "do not"),
        (AppLocale.DANISH_DENMARK, "ikke"),
    ),
)
def test_dm847_modules_include_explicit_response_constraints(
    locale: AppLocale, constraint_marker: str
) -> None:
    for localized_bundle in LOCALIZED_BUNDLES:
        module = localized_bundle.materialize(locale).module
        constraints = "\n".join(module.tutor_support.response_constraints).casefold()
        assert constraint_marker in constraints


def test_dm847_catalog_covers_the_active_course_domains() -> None:
    titles = "\n".join(module.title for module in MODULES).casefold()
    required_fragments = (
        "molecular",
        "ontolog",
        "secuenc",
        "alineamiento",
        "markov",
        "bwt",
        "operon",
        "motivo",
        "redes",
        "omics",
    )
    assert all(fragment in titles for fragment in required_fragments)
