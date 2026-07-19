from __future__ import annotations

from pathlib import Path

import pytest
import yaml

from computational_biomedicine_study_hub.academic import (
    AcademicCatalog,
    SemesterContentLoader,
    default_content_root,
)
from computational_biomedicine_study_hub.academic.retrieval import (
    AcademicFragment,
    FragmentVisibility,
    LexicalRetriever,
    RetrievalQuery,
    build_fragments,
)
from computational_biomedicine_study_hub.academic.validation import validate_catalog


@pytest.fixture(scope="module")
def catalog() -> AcademicCatalog:
    return SemesterContentLoader().load()


def test_every_yaml_file_is_nonempty_and_safe_loadable() -> None:
    paths = sorted(default_content_root().rglob("*.yaml"))

    assert len(paths) == 119
    for path in paths:
        text = path.read_text(encoding="utf-8")
        assert text.strip(), path
        assert isinstance(yaml.safe_load(text), dict), path


def test_catalog_loads_four_courses_and_54_real_modules(catalog: AcademicCatalog) -> None:
    assert tuple(sorted(catalog.courses_by_id)) == ("bmb830", "bmb831", "dm847", "dm857")
    assert catalog.module_count == 54
    assert {course.id: len(course.modules) for course in catalog.courses} == {
        "bmb830": 10,
        "bmb831": 12,
        "dm847": 15,
        "dm857": 17,
    }


def test_audit_exposes_real_card_shortfall_without_fabricating_content(
    catalog: AcademicCatalog,
) -> None:
    assert catalog.flashcard_count == 1338
    assert {
        course.id: sum(len(module.flashcards) for module in course.modules)
        for course in catalog.courses
    } == {
        "bmb830": 246,
        "bmb831": 300,
        "dm847": 372,
        "dm857": 420,
    }
    report = validate_catalog(catalog, default_content_root())
    blocker_codes = {issue.code for issue in report.blockers}
    assert "semester.flashcard_count" in blocker_codes
    assert "course.flashcard_count" in blocker_codes
    assert "course.cumulative_missing" in blocker_codes


def test_flashcard_ids_and_runtime_entity_ids_are_unique(
    catalog: AcademicCatalog,
) -> None:
    cards = [
        card
        for course in catalog.courses
        for module in course.modules
        for card in module.flashcards
    ]
    assert len({card.id for card in cards}) == len(cards)
    assert all(card.front.complete and card.back.complete for card in cards)

    entities = [
        item.qualified_id
        for course in catalog.courses
        for module in course.modules
        for collection in (
            module.objectives,
            module.concepts,
            module.worked_examples,
            module.practice,
            module.objective_questions,
            module.open_assessments,
            module.glossary,
        )
        for item in collection
    ]
    assert len(set(entities)) == len(entities)
    assert all(
        question.prompt.complete
        for course in catalog.courses
        for module in course.modules
        for question in module.objective_questions
    )


def test_hidden_tutor_fragments_are_separate_from_visible_content(
    catalog: AcademicCatalog,
) -> None:
    fragments = build_fragments(catalog, "en")

    hidden = tuple(
        fragment for fragment in fragments if fragment.visibility is FragmentVisibility.HIDDEN_TUTOR
    )
    assert len(hidden) >= 54
    assert {fragment.module_id for fragment in hidden} == {
        module.id for course in catalog.courses for module in course.modules
    }
    assert all(module.hidden_support.raw for course in catalog.courses for module in course.modules)


def test_retrieval_requires_explicit_hidden_authorization() -> None:
    fragments = (
        AcademicFragment(
            "visible",
            "dm857.m01.c01",
            "dm857",
            "dm857.m01",
            "Concept",
            "en",
            "public tracing explanation",
            FragmentVisibility.VISIBLE,
        ),
        AcademicFragment(
            "hidden",
            "dm857.m01.hidden",
            "dm857",
            "dm857.m01",
            "Tutor support",
            "en",
            "private misconception rubric",
            FragmentVisibility.HIDDEN_TUTOR,
        ),
    )
    retriever = LexicalRetriever(fragments)

    assert retriever.search(RetrievalQuery("private misconception", "en")) == ()
    authorized = retriever.search(RetrievalQuery("private misconception", "en", allow_hidden=True))
    assert authorized
    assert authorized[0].fragment.visibility is FragmentVisibility.HIDDEN_TUTOR


def test_default_root_points_to_the_canonical_corpus() -> None:
    root = default_content_root()
    assert root == Path("academic_content/semester_1").resolve()
