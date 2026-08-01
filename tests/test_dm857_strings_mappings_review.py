from __future__ import annotations

from computational_biomedicine_study_hub.content import dm857
from computational_biomedicine_study_hub.content.models import LearningModule
from computational_biomedicine_study_hub.i18n import AppLocale

EXPECTED_IDS = {
    "dm857.m05": (
        "regex-validation-boundaries",
        "m05.bg.e01",
        "m05.bg.p01",
        "dm857.m05.book.001",
    ),
    "dm857.m07": (
        "hash-tables-collisions-and-cost",
        "m07.bg.e01",
        "m07.bg.p01",
        "dm857.m07.book.001",
    ),
}


def _modules(locale: AppLocale) -> dict[str, LearningModule]:
    return {
        module.module_id: module.materialize(locale)
        for module in dm857.LOCALIZED_MODULES
        if module.module_id in EXPECTED_IDS
    }


def _signature(module: LearningModule) -> tuple[tuple[str, ...], ...]:
    return (
        tuple(item.objective_id for item in module.objectives),
        tuple(item.concept_id for item in module.concepts),
        tuple(item.example_id for item in module.worked_examples),
        tuple(item.exercise_id for item in module.practice_exercises),
        tuple(item.item_id for item in module.assessment_items),
    )


def test_reviewed_modules_have_complete_stable_extensions_in_every_locale() -> None:
    for locale in AppLocale:
        modules = _modules(locale)
        for module_id, expected in EXPECTED_IDS.items():
            module = modules[module_id]
            concept_id, example_id, exercise_id, item_id = expected

            assert concept_id in {item.concept_id for item in module.concepts}
            assert example_id in {item.example_id for item in module.worked_examples}
            assert exercise_id in {item.exercise_id for item in module.practice_exercises}
            assert item_id in {item.item_id for item in module.assessment_items}
            assert all(document.text.strip() for document in module.tutor_documents())


def test_reviewed_module_identifiers_are_locale_independent() -> None:
    reference = {
        module_id: _signature(module) for module_id, module in _modules(AppLocale.ENGLISH).items()
    }

    for locale in AppLocale:
        assert {
            module_id: _signature(module) for module_id, module in _modules(locale).items()
        } == reference


def test_reviewed_module_audit_records_sources_findings_and_changes() -> None:
    audit = {item.module_id: item for item in dm857.DM857_MODULE_SOURCE_AUDIT}

    assert audit["dm857.m05"].state == "consistent"
    assert audit["dm857.m07"].state == "consistent"
    assert set(audit["dm857.m05"].source_ids) == {
        "guttag-2021-ch05",
        "downey-2024-strings-collections",
    }
    assert set(audit["dm857.m07"].source_ids) == {
        "guttag-2021-ch05",
        "guttag-2021-ch10-12",
        "downey-2024-strings-collections",
    }
    assert audit["dm857.m05"].finding
    assert audit["dm857.m05"].implemented_change
    assert audit["dm857.m07"].finding
    assert audit["dm857.m07"].implemented_change


def test_new_concepts_preserve_their_scope_boundaries() -> None:
    modules = _modules(AppLocale.ENGLISH)
    regex = next(
        item
        for item in modules["dm857.m05"].concepts
        if item.concept_id == "regex-validation-boundaries"
    )
    hashing = next(
        item
        for item in modules["dm857.m07"].concepts
        if item.concept_id == "hash-tables-collisions-and-cost"
    )

    assert "fullmatch" in regex.body
    assert "search" in regex.body
    assert "biological meaning" in regex.body
    assert any("semantic validity" in point for point in regex.key_points)
    assert "collision" in hashing.body
    assert "equality" in hashing.body
    assert "average" in hashing.body
    assert "worst" in hashing.body
