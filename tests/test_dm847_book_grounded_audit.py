"""Regression tests for the DM847 book-grounded audit and first extensions."""

from __future__ import annotations

from computational_biomedicine_study_hub.content import dm847
from computational_biomedicine_study_hub.i18n import AppLocale

_EXPECTED_MODULE_IDS = {f"dm847.m{index:02d}" for index in range(1, 11)}
_REVIEWED_MODULE_IDS = {
    "dm847.m03",
    "dm847.m04",
    "dm847.m05",
    "dm847.m06",
}


def _module(module_id: str, locale: AppLocale | str = AppLocale.ENGLISH):
    localized = next(item for item in dm847.LOCALIZED_MODULES if item.module_id == module_id)
    return localized.materialize(locale)


def _run_example(module_id: str, example_id: str) -> None:
    module = _module(module_id)
    worked_example = next(item for item in module.worked_examples if item.example_id == example_id)
    exec(compile(worked_example.code, example_id, "exec"), {})


def test_dm847_source_audit_maps_every_module_once() -> None:
    audited_ids = tuple(item.module_id for item in dm847.DM847_MODULE_SOURCE_AUDIT)

    assert len(audited_ids) == 10
    assert len(set(audited_ids)) == 10
    assert set(audited_ids) == _EXPECTED_MODULE_IDS


def test_dm847_source_catalog_has_unique_stable_ids() -> None:
    source_ids = tuple(source.source_id for source in dm847.DM847_BOOK_SOURCES)

    assert len(source_ids) == len(set(source_ids))
    assert "sdu-dm847-active-2025" in source_ids
    assert "compeau-pevzner-v1-ch01" in source_ids
    assert "compeau-pevzner-v1-ch05" in source_ids
    assert "compeau-pevzner-v2-ch09" in source_ids


def test_only_completed_focused_reviews_are_marked_consistent() -> None:
    state_by_module = {item.module_id: item.state for item in dm847.DM847_MODULE_SOURCE_AUDIT}

    assert {
        module_id for module_id, state in state_by_module.items() if state == "consistent"
    } == _REVIEWED_MODULE_IDS
    assert {
        module_id for module_id, state in state_by_module.items() if state == "pending"
    } == _EXPECTED_MODULE_IDS - _REVIEWED_MODULE_IDS


def test_first_extensions_are_complete_and_locale_stable() -> None:
    reference_ids: dict[str, tuple[tuple[str, ...], ...]] = {}

    for locale in AppLocale:
        matching = _module("dm847.m03", locale)
        alignment = _module("dm847.m04", locale)

        assert "approximate-pattern-matching-and-neighborhoods" in {
            item.concept_id for item in matching.concepts
        }
        assert "m03.bg.e01" in {item.example_id for item in matching.worked_examples}
        assert "m03.bg.p01" in {item.exercise_id for item in matching.practice_exercises}
        assert "dm847.m03.book.001" in {item.item_id for item in matching.assessment_items}

        assert "linear-space-scoring-and-traceback-boundary" in {
            item.concept_id for item in alignment.concepts
        }
        assert "m04.bg.e01" in {item.example_id for item in alignment.worked_examples}
        assert "m04.bg.p01" in {item.exercise_id for item in alignment.practice_exercises}
        assert "dm847.m04.book.001" in {item.item_id for item in alignment.assessment_items}

        identities = (
            tuple(item.objective_id for item in matching.objectives),
            tuple(item.concept_id for item in matching.concepts),
            tuple(item.example_id for item in matching.worked_examples),
            tuple(item.exercise_id for item in matching.practice_exercises),
            tuple(item.item_id for item in matching.assessment_items),
            tuple(item.objective_id for item in alignment.objectives),
            tuple(item.concept_id for item in alignment.concepts),
            tuple(item.example_id for item in alignment.worked_examples),
            tuple(item.exercise_id for item in alignment.practice_exercises),
            tuple(item.item_id for item in alignment.assessment_items),
        )
        if not reference_ids:
            reference_ids["ids"] = identities
        else:
            assert identities == reference_ids["ids"]


def test_reviewed_modules_expose_named_source_basis() -> None:
    matching = _module("dm847.m03")
    alignment = _module("dm847.m04")

    assert "compeau-pevzner-v1-ch01" in matching.tutor_support.source_basis
    assert "compeau-pevzner-v1-ch05" in matching.tutor_support.source_basis
    assert "compeau-pevzner-v1-ch05" in alignment.tutor_support.source_basis
    assert "sdu-dm847-active-2025" in matching.tutor_support.source_basis
    assert "sdu-dm847-active-2025" in alignment.tutor_support.source_basis


def test_matching_extension_preserves_algorithmic_boundaries() -> None:
    matching = _module("dm847.m03")
    concept = next(
        item
        for item in matching.concepts
        if item.concept_id == "approximate-pattern-matching-and-neighborhoods"
    )
    exported = "\n".join((concept.body, *concept.key_points)).casefold()

    assert "equal-length" in exported
    assert "d=0" in exported
    assert "insertions" in exported
    assert "deletions" in exported
    assert "reverse complement" in exported
    assert "significance" not in concept.title.casefold()


def test_alignment_extension_separates_score_memory_from_traceback() -> None:
    alignment = _module("dm847.m04")
    concept = next(
        item
        for item in alignment.concepts
        if item.concept_id == "linear-space-scoring-and-traceback-boundary"
    )
    exported = "\n".join((concept.body, *concept.key_points)).casefold()

    assert "o(min(n,m))" in exported
    assert "o(nm)" in exported
    assert "final row" in exported
    assert "traceback" in exported
    assert "divide-and-conquer" in exported


def test_new_examples_execute_deterministically(capsys) -> None:
    _run_example("dm847.m03", "m03.bg.e01")
    assert capsys.readouterr().out.rstrip("\n") == "[0, 5]"

    _run_example("dm847.m04", "m04.bg.e01")
    assert capsys.readouterr().out.rstrip("\n") == "(1, 3)"
