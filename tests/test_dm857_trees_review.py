from __future__ import annotations

from computational_biomedicine_study_hub.content import dm857
from computational_biomedicine_study_hub.content.models import LearningModule
from computational_biomedicine_study_hub.i18n import AppLocale

EXPECTED_IDS = (
    "path-reconstruction-and-search-contracts",
    "m10.bg.e01",
    "m10.bg.p01",
    "dm857.m10.book.001",
)


def _module(locale: AppLocale | str) -> LearningModule:
    localized = next(
        module for module in dm857.LOCALIZED_MODULES if module.module_id == "dm857.m10"
    )
    return localized.materialize(locale)


def _signature(module: LearningModule) -> tuple[tuple[str, ...], ...]:
    return (
        tuple(item.objective_id for item in module.objectives),
        tuple(item.concept_id for item in module.concepts),
        tuple(item.example_id for item in module.worked_examples),
        tuple(item.exercise_id for item in module.practice_exercises),
        tuple(item.item_id for item in module.assessment_items),
    )


def test_tree_extension_is_complete_and_locale_independent() -> None:
    reference = _signature(_module(AppLocale.ENGLISH))
    concept_id, example_id, exercise_id, item_id = EXPECTED_IDS

    for locale in AppLocale:
        module = _module(locale)
        assert _signature(module) == reference
        assert concept_id in {item.concept_id for item in module.concepts}
        assert example_id in {item.example_id for item in module.worked_examples}
        assert exercise_id in {item.exercise_id for item in module.practice_exercises}
        assert item_id in {item.item_id for item in module.assessment_items}
        assert all(document.text.strip() for document in module.tutor_documents())


def test_tree_audit_records_review_and_named_sources() -> None:
    audit = {item.module_id: item for item in dm857.DM857_MODULE_SOURCE_AUDIT}
    item = audit["dm857.m10"]

    assert item.state == "consistent"
    assert set(item.source_ids) == {
        "guttag-2021-ch10-12",
        "guttag-2021-ch13-15-23",
    }
    assert item.finding
    assert item.implemented_change

    source_basis = _module(AppLocale.ENGLISH).tutor_support.source_basis
    assert "guttag-2021-ch10-12" in source_basis
    assert "guttag-2021-ch13-15-23" in source_basis


def test_tree_path_concept_preserves_search_scope_boundaries() -> None:
    module = _module(AppLocale.ENGLISH)
    concept = next(
        item
        for item in module.concepts
        if item.concept_id == "path-reconstruction-and-search-contracts"
    )
    text = " ".join((concept.body, *concept.key_points)).casefold()

    assert "predecessor" in text
    assert "unique simple path" in text
    assert "minimum edge" in text or "edge count" in text
    assert "total weight" in text
    assert "dfs" in text


def test_tree_path_example_executes_deterministically(capsys) -> None:
    module = _module(AppLocale.ENGLISH)
    worked_example = next(
        item for item in module.worked_examples if item.example_id == "m10.bg.e01"
    )

    exec(compile(worked_example.code, worked_example.example_id, "exec"), {})

    assert capsys.readouterr().out.rstrip("\n") == "['root', 'systems', 'immune']"
