"""Focused regression tests for DM847 molecular foundations and OMICS learning."""

from __future__ import annotations

from computational_biomedicine_study_hub.content import dm847
from computational_biomedicine_study_hub.i18n import AppLocale

_REVIEWED_MODULE_IDS = {f"dm847.m{index:02d}" for index in range(1, 11)}


def _module(module_id: str, locale: AppLocale | str = AppLocale.ENGLISH):
    localized = next(item for item in dm847.LOCALIZED_MODULES if item.module_id == module_id)
    return localized.materialize(locale)


def _run_example(module_id: str, example_id: str) -> None:
    module = _module(module_id)
    worked_example = next(item for item in module.worked_examples if item.example_id == example_id)
    exec(compile(worked_example.code, example_id, "exec"), {})


def test_omics_and_foundations_reviews_update_only_completed_audit_states() -> None:
    state_by_module = {item.module_id: item.state for item in dm847.DM847_MODULE_SOURCE_AUDIT}

    assert {
        module_id for module_id, state in state_by_module.items() if state == "consistent"
    } == _REVIEWED_MODULE_IDS
    assert {module_id for module_id, state in state_by_module.items() if state == "pending"} == set()

    for item in dm847.DM847_MODULE_SOURCE_AUDIT:
        if item.module_id in {"dm847.m01", "dm847.m10"}:
            assert item.implemented_change
            assert "original" in item.implemented_change.casefold()


def test_omics_and_foundations_extensions_are_complete_and_locale_stable() -> None:
    reference_identity: tuple[tuple[str, ...], ...] | None = None

    for locale in AppLocale:
        foundations = _module("dm847.m01", locale)
        omics = _module("dm847.m10", locale)

        assert "m01.bg.o1" in {item.objective_id for item in foundations.objectives}
        assert "computational-problem-contracts" in {
            item.concept_id for item in foundations.concepts
        }
        assert "m01.bg.e01" in {item.example_id for item in foundations.worked_examples}
        assert "m01.bg.p01" in {item.exercise_id for item in foundations.practice_exercises}
        assert "dm847.m01.book.001" in {item.item_id for item in foundations.assessment_items}

        assert "m10.bg.o1" in {item.objective_id for item in omics.objectives}
        assert "clustering-objectives-initialization-and-stability" in {
            item.concept_id for item in omics.concepts
        }
        assert "m10.bg.e01" in {item.example_id for item in omics.worked_examples}
        assert "m10.bg.p01" in {item.exercise_id for item in omics.practice_exercises}
        assert "dm847.m10.book.001" in {item.item_id for item in omics.assessment_items}

        identity = (
            tuple(item.objective_id for item in foundations.objectives),
            tuple(item.concept_id for item in foundations.concepts),
            tuple(item.example_id for item in foundations.worked_examples),
            tuple(item.exercise_id for item in foundations.practice_exercises),
            tuple(item.item_id for item in foundations.assessment_items),
            tuple(item.objective_id for item in omics.objectives),
            tuple(item.concept_id for item in omics.concepts),
            tuple(item.example_id for item in omics.worked_examples),
            tuple(item.exercise_id for item in omics.practice_exercises),
            tuple(item.item_id for item in omics.assessment_items),
        )
        if reference_identity is None:
            reference_identity = identity
        else:
            assert identity == reference_identity


def test_foundations_extension_exposes_problem_contract_boundaries() -> None:
    module = _module("dm847.m01")
    concept = next(
        item for item in module.concepts if item.concept_id == "computational-problem-contracts"
    )
    exported = "\n".join((concept.body, *concept.key_points)).casefold()

    assert "input" in exported
    assert "output" in exported
    assert "reverse complement" in exported
    assert "coordinates" in exported
    assert "overlap" in exported
    assert "edge cases" in exported
    assert "biological relevance" in exported


def test_omics_extension_exposes_objective_and_stability_boundaries() -> None:
    module = _module("dm847.m10")
    concept = next(
        item
        for item in module.concepts
        if item.concept_id == "clustering-objectives-initialization-and-stability"
    )
    exported = "\n".join((concept.body, *concept.key_points)).casefold()

    assert "distortion" in exported
    assert "lloyd" in exported
    assert "local optima" in exported
    assert "restarts" in exported
    assert "responsibilities" in exported
    assert "sum to one" in exported
    assert "hierarchical" in exported
    assert "resampling" in exported
    assert "batch" in exported


def test_reviewed_modules_expose_named_source_basis() -> None:
    foundations = _module("dm847.m01")
    omics = _module("dm847.m10")

    assert "sdu-dm847-active-2025" in foundations.tutor_support.source_basis
    assert "compeau-pevzner-v1-ch01" in foundations.tutor_support.source_basis
    assert "sdu-dm847-active-2025" in omics.tutor_support.source_basis
    assert "compeau-pevzner-v2-ch08" in omics.tutor_support.source_basis


def test_foundations_example_contract_is_explicit() -> None:
    module = _module("dm847.m01")
    example = next(item for item in module.worked_examples if item.example_id == "m01.bg.e01")
    exported = "\n".join((example.problem, *example.reasoning, example.explanation)).casefold()

    assert "zero-based" in exported
    assert "overlap" in exported
    assert "canonical dna" in exported
    assert "reverse complement" in exported


def test_omics_example_compares_restarts_without_overclaiming() -> None:
    module = _module("dm847.m10")
    example = next(item for item in module.worked_examples if item.example_id == "m10.bg.e01")
    exported = "\n".join((example.problem, *example.reasoning, example.explanation)).casefold()

    assert "initial" in exported
    assert "distortion" in exported
    assert "stability" in exported
    assert "biological" in exported


def test_new_examples_execute_deterministically(capsys) -> None:
    _run_example("dm847.m01", "m01.bg.e01")
    assert capsys.readouterr().out.rstrip("\n") == "[0, 2]"

    _run_example("dm847.m10", "m10.bg.e01")
    assert capsys.readouterr().out.rstrip("\n") == (
        "{'left_start': ((1.0, 12.5), 11.286), 'right_start': ((5.5, 20.0), 17.929)}"
    )
