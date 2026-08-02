"""Focused regression tests for the DM847 HMM and BWT source reviews."""

from __future__ import annotations

from computational_biomedicine_study_hub.content import dm847
from computational_biomedicine_study_hub.i18n import AppLocale

_REVIEWED_MODULE_IDS = {
    "dm847.m01",
    "dm847.m03",
    "dm847.m04",
    "dm847.m05",
    "dm847.m06",
    "dm847.m08",
    "dm847.m09",
    "dm847.m10",
}


def _module(module_id: str, locale: AppLocale | str = AppLocale.ENGLISH):
    localized = next(item for item in dm847.LOCALIZED_MODULES if item.module_id == module_id)
    return localized.materialize(locale)


def _run_example(module_id: str, example_id: str) -> None:
    module = _module(module_id)
    worked_example = next(item for item in module.worked_examples if item.example_id == example_id)
    exec(compile(worked_example.code, example_id, "exec"), {})


def test_hmm_and_bwt_reviews_update_only_completed_audit_states() -> None:
    state_by_module = {item.module_id: item.state for item in dm847.DM847_MODULE_SOURCE_AUDIT}

    assert {
        module_id for module_id, state in state_by_module.items() if state == "consistent"
    } == _REVIEWED_MODULE_IDS
    assert {module_id for module_id, state in state_by_module.items() if state == "pending"} == {
        f"dm847.m{index:02d}" for index in range(1, 11)
    } - _REVIEWED_MODULE_IDS

    for item in dm847.DM847_MODULE_SOURCE_AUDIT:
        if item.module_id in {"dm847.m05", "dm847.m06"}:
            assert item.implemented_change
            assert "original" in item.implemented_change.casefold()


def test_hmm_and_bwt_extensions_are_complete_and_locale_stable() -> None:
    reference_identity: tuple[tuple[str, ...], ...] | None = None

    for locale in AppLocale:
        hmm = _module("dm847.m05", locale)
        bwt = _module("dm847.m06", locale)

        assert "m05.bg.o1" in {item.objective_id for item in hmm.objectives}
        assert "soft-decoding-forward-backward" in {item.concept_id for item in hmm.concepts}
        assert "m05.bg.e01" in {item.example_id for item in hmm.worked_examples}
        assert "m05.bg.p01" in {item.exercise_id for item in hmm.practice_exercises}
        assert "dm847.m05.book.001" in {item.item_id for item in hmm.assessment_items}

        assert "m06.bg.o1" in {item.objective_id for item in bwt.objectives}
        assert "pigeonhole-seeding-and-verification" in {item.concept_id for item in bwt.concepts}
        assert "m06.bg.e01" in {item.example_id for item in bwt.worked_examples}
        assert "m06.bg.p01" in {item.exercise_id for item in bwt.practice_exercises}
        assert "dm847.m06.book.001" in {item.item_id for item in bwt.assessment_items}

        identity = (
            tuple(item.objective_id for item in hmm.objectives),
            tuple(item.concept_id for item in hmm.concepts),
            tuple(item.example_id for item in hmm.worked_examples),
            tuple(item.exercise_id for item in hmm.practice_exercises),
            tuple(item.item_id for item in hmm.assessment_items),
            tuple(item.objective_id for item in bwt.objectives),
            tuple(item.concept_id for item in bwt.concepts),
            tuple(item.example_id for item in bwt.worked_examples),
            tuple(item.exercise_id for item in bwt.practice_exercises),
            tuple(item.item_id for item in bwt.assessment_items),
        )
        if reference_identity is None:
            reference_identity = identity
        else:
            assert identity == reference_identity


def test_hmm_soft_decoding_preserves_probability_boundaries() -> None:
    hmm = _module("dm847.m05")
    concept = next(
        item for item in hmm.concepts if item.concept_id == "soft-decoding-forward-backward"
    )
    exported = "\n".join((concept.body, *concept.key_points)).casefold()

    assert "forward" in exported
    assert "backward" in exported
    assert "posterior" in exported
    assert "sum to one" in exported
    assert "viterbi" in exported
    assert "global path" in exported
    assert "future evidence" in exported
    assert "impossible transitions" in exported


def test_bwt_pigeonhole_seeding_preserves_algorithmic_boundaries() -> None:
    bwt = _module("dm847.m06")
    concept = next(
        item for item in bwt.concepts if item.concept_id == "pigeonhole-seeding-and-verification"
    )
    exported = "\n".join((concept.body, *concept.key_points)).casefold()

    assert "d+1" in exported
    assert "nonempty" in exported
    assert "exact" in exported
    assert "offset" in exported
    assert "duplicates" in exported
    assert "verification" in exported
    assert "hamming" in exported
    assert "indels" in exported


def test_reviewed_modules_expose_their_named_book_sources() -> None:
    hmm = _module("dm847.m05")
    bwt = _module("dm847.m06")

    assert "sdu-dm847-active-2025" in hmm.tutor_support.source_basis
    assert "compeau-pevzner-v2-ch10" in hmm.tutor_support.source_basis
    assert "sdu-dm847-active-2025" in bwt.tutor_support.source_basis
    assert "compeau-pevzner-v2-ch09" in bwt.tutor_support.source_basis


def test_hmm_and_bwt_examples_execute_deterministically(capsys) -> None:
    _run_example("dm847.m05", "m05.bg.e01")
    assert capsys.readouterr().out.rstrip("\n") == (
        "[{'H': 0.651, 'L': 0.349}, {'H': 0.316, 'L': 0.684}]"
    )

    _run_example("dm847.m06", "m06.bg.e01")
    assert capsys.readouterr().out.rstrip("\n") == "([0, 5, 10], [0, 5])"


def test_new_objective_items_protect_the_core_distinctions() -> None:
    hmm = _module("dm847.m05")
    bwt = _module("dm847.m06")

    hmm_item = next(item for item in hmm.assessment_items if item.item_id == "dm847.m05.book.001")
    bwt_item = next(item for item in bwt.assessment_items if item.item_id == "dm847.m06.book.001")

    assert hmm_item.correct_option_ids == ("forward_backward",)
    assert bwt_item.correct_option_ids == ("pigeonhole",)
