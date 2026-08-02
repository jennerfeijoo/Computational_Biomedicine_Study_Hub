"""Focused regressions for the DM847 motif and network source reviews."""

from __future__ import annotations

from computational_biomedicine_study_hub.content import dm847
from computational_biomedicine_study_hub.i18n import AppLocale

_REVIEWED_MODULE_IDS = {
    "dm847.m03",
    "dm847.m04",
    "dm847.m05",
    "dm847.m06",
    "dm847.m08",
    "dm847.m09",
}


def _module(module_id: str, locale: AppLocale | str = AppLocale.ENGLISH):
    localized = next(item for item in dm847.LOCALIZED_MODULES if item.module_id == module_id)
    return localized.materialize(locale)


def _run_example(module_id: str, example_id: str) -> None:
    module = _module(module_id)
    worked_example = next(item for item in module.worked_examples if item.example_id == example_id)
    exec(compile(worked_example.code, example_id, "exec"), {})


def test_motif_and_network_reviews_update_the_cumulative_audit() -> None:
    state_by_module = {item.module_id: item.state for item in dm847.DM847_MODULE_SOURCE_AUDIT}

    assert {
        module_id for module_id, state in state_by_module.items() if state == "consistent"
    } == _REVIEWED_MODULE_IDS
    assert {module_id for module_id, state in state_by_module.items() if state == "pending"} == {
        "dm847.m01",
        "dm847.m02",
        "dm847.m07",
        "dm847.m10",
    }


def test_network_source_catalog_corrects_chapter_11_and_adds_primary_sources() -> None:
    catalog = {source.source_id: source for source in dm847.DM847_BOOK_SOURCES}
    network_audit = next(
        item for item in dm847.DM847_MODULE_SOURCE_AUDIT if item.module_id == "dm847.m09"
    )

    assert "peptide sequencing" in catalog["compeau-pevzner-v2-ch11"].relevant_scope
    assert "not biological network enrichment" in catalog["compeau-pevzner-v2-ch11"].relevant_scope
    assert "ideker-2002-active-modules" in catalog
    assert "alcaraz-2012-keypathwayminer" in catalog
    assert "compeau-pevzner-v2-ch11" not in network_audit.source_ids
    assert "ideker-2002-active-modules" in network_audit.source_ids
    assert "alcaraz-2012-keypathwayminer" in network_audit.source_ids


def test_motif_and_network_extensions_are_complete_and_locale_stable() -> None:
    reference_identity: tuple[tuple[str, ...], ...] | None = None

    for locale in AppLocale:
        motif = _module("dm847.m08", locale)
        network = _module("dm847.m09", locale)

        assert "m08.bg.o1" in {item.objective_id for item in motif.objectives}
        assert "fractional-counts-and-em-convergence" in {
            item.concept_id for item in motif.concepts
        }
        assert "m08.bg.e01" in {item.example_id for item in motif.worked_examples}
        assert "m08.bg.p01" in {item.exercise_id for item in motif.practice_exercises}
        assert "dm847.m08.book.001" in {item.item_id for item in motif.assessment_items}

        assert "m09.bg.o1" in {item.objective_id for item in network.objectives}
        assert "predefined-enrichment-vs-active-subnetworks" in {
            item.concept_id for item in network.concepts
        }
        assert "m09.bg.e01" in {item.example_id for item in network.worked_examples}
        assert "m09.bg.p01" in {item.exercise_id for item in network.practice_exercises}
        assert "dm847.m09.book.001" in {item.item_id for item in network.assessment_items}

        identity = (
            tuple(item.objective_id for item in motif.objectives),
            tuple(item.concept_id for item in motif.concepts),
            tuple(item.example_id for item in motif.worked_examples),
            tuple(item.exercise_id for item in motif.practice_exercises),
            tuple(item.item_id for item in motif.assessment_items),
            tuple(item.objective_id for item in network.objectives),
            tuple(item.concept_id for item in network.concepts),
            tuple(item.example_id for item in network.worked_examples),
            tuple(item.exercise_id for item in network.practice_exercises),
            tuple(item.item_id for item in network.assessment_items),
        )
        if reference_identity is None:
            reference_identity = identity
        else:
            assert identity == reference_identity


def test_motif_extension_preserves_soft_em_boundaries() -> None:
    motif = _module("dm847.m08")
    concept = next(
        item for item in motif.concepts if item.concept_id == "fractional-counts-and-em-convergence"
    )
    exported = "\n".join((concept.body, *concept.key_points)).casefold()

    assert "sum to one" in exported
    assert "fractional" in exported
    assert "pseudocount" in exported
    assert "likelihood should not decrease" in exported
    assert "tolerance" in exported
    assert "maximum iteration" in exported
    assert "hard-assignment" in exported
    assert "local optima" in exported


def test_network_extension_separates_ora_from_selected_subnetworks() -> None:
    network = _module("dm847.m09")
    concept = next(
        item
        for item in network.concepts
        if item.concept_id == "predefined-enrichment-vs-active-subnetworks"
    )
    exported = "\n".join((concept.body, *concept.key_points)).casefold()

    assert "predefined" in exported
    assert "connected" in exported
    assert "jactivemodules" in exported
    assert "keypathwayminer" in exported
    assert "heuristic" in exported
    assert "not necessarily a calibrated p-value" in exported
    assert "selection process" in exported
    assert "null model" in exported


def test_new_modules_expose_their_named_sources() -> None:
    motif = _module("dm847.m08")
    network = _module("dm847.m09")

    assert "sdu-dm847-active-2025" in motif.tutor_support.source_basis
    assert "compeau-pevzner-v1-ch02" in motif.tutor_support.source_basis
    assert "compeau-pevzner-v2-ch08" in motif.tutor_support.source_basis
    assert "sdu-dm847-active-2025" in network.tutor_support.source_basis
    assert "ideker-2002-active-modules" in network.tutor_support.source_basis
    assert "alcaraz-2012-keypathwayminer" in network.tutor_support.source_basis
    assert "compeau-pevzner-v2-ch11" not in network.tutor_support.source_basis


def test_motif_and_network_examples_execute_deterministically(capsys) -> None:
    _run_example("dm847.m08", "m08.bg.e01")
    assert capsys.readouterr().out.rstrip("\n") == (
        "[{'A': 0.4, 'C': 0.167, 'G': 0.267, 'T': 0.167}, "
        "{'A': 0.167, 'C': 0.367, 'G': 0.167, 'T': 0.3}]"
    )

    _run_example("dm847.m09", "m09.bg.e01")
    assert capsys.readouterr().out.rstrip("\n") == "{'AB': 3.536, 'ABC': 2.309}"


def test_new_objective_items_protect_core_distinctions() -> None:
    motif = _module("dm847.m08")
    network = _module("dm847.m09")

    motif_item = next(
        item for item in motif.assessment_items if item.item_id == "dm847.m08.book.001"
    )
    network_item = next(
        item for item in network.assessment_items if item.item_id == "dm847.m09.book.001"
    )

    assert motif_item.correct_option_ids == ("fractional_counts",)
    assert network_item.correct_option_ids == ("connected_selection",)
