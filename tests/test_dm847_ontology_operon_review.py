"""Focused regressions for the final DM847 ontology and operon reviews."""

from __future__ import annotations

from computational_biomedicine_study_hub.content import dm847
from computational_biomedicine_study_hub.i18n import AppLocale


def _module(module_id: str, locale: AppLocale | str = AppLocale.ENGLISH):
    localized = next(item for item in dm847.LOCALIZED_MODULES if item.module_id == module_id)
    return localized.materialize(locale)


def _run_example(module_id: str, example_id: str) -> None:
    module = _module(module_id)
    worked_example = next(item for item in module.worked_examples if item.example_id == example_id)
    exec(compile(worked_example.code, example_id, "exec"), {})


def test_final_reviews_complete_the_dm847_audit() -> None:
    state_by_module = {item.module_id: item.state for item in dm847.DM847_MODULE_SOURCE_AUDIT}

    assert set(state_by_module) == {f"dm847.m{index:02d}" for index in range(1, 11)}
    assert set(state_by_module.values()) == {"consistent"}

    for module_id in ("dm847.m02", "dm847.m07"):
        item = next(item for item in dm847.DM847_MODULE_SOURCE_AUDIT if item.module_id == module_id)
        assert item.implemented_change
        assert "original" in item.implemented_change.casefold()


def test_specialized_source_catalog_is_registered() -> None:
    source_ids = {source.source_id for source in dm847.DM847_BOOK_SOURCES}

    assert "coveney-2014-ch03-ch08" in source_ids
    assert "yachay-molecular-biology-ch19-ch26" in source_ids


def test_extensions_are_complete_and_locale_stable() -> None:
    reference_identity: tuple[tuple[str, ...], ...] | None = None

    for locale in AppLocale:
        ontology = _module("dm847.m02", locale)
        operons = _module("dm847.m07", locale)

        assert len(ontology.objectives) == 7
        assert len(ontology.concepts) == 7
        assert len(ontology.worked_examples) == 4
        assert len(ontology.practice_exercises) == 9
        assert len(ontology.assessment_items) == 11

        assert len(operons.objectives) == 7
        assert len(operons.concepts) == 7
        assert len(operons.worked_examples) == 4
        assert len(operons.practice_exercises) == 9
        assert len(operons.assessment_items) == 11

        identity = (
            tuple(item.objective_id for item in ontology.objectives),
            tuple(item.concept_id for item in ontology.concepts),
            tuple(item.example_id for item in ontology.worked_examples),
            tuple(item.exercise_id for item in ontology.practice_exercises),
            tuple(item.item_id for item in ontology.assessment_items),
            tuple(item.objective_id for item in operons.objectives),
            tuple(item.concept_id for item in operons.concepts),
            tuple(item.example_id for item in operons.worked_examples),
            tuple(item.exercise_id for item in operons.practice_exercises),
            tuple(item.item_id for item in operons.assessment_items),
        )
        if reference_identity is None:
            reference_identity = identity
        else:
            assert identity == reference_identity

    assert reference_identity is not None
    assert "m02.bg.o1" in reference_identity[0]
    assert "semantic-closure-and-assertion-provenance" in reference_identity[1]
    assert "m02.bg.e01" in reference_identity[2]
    assert "m02.bg.p01" in reference_identity[3]
    assert "dm847.m02.book.001" in reference_identity[4]
    assert "m07.bg.o1" in reference_identity[5]
    assert "genomic-order-vs-transcriptional-order" in reference_identity[6]
    assert "m07.bg.e01" in reference_identity[7]
    assert "m07.bg.p01" in reference_identity[8]
    assert "dm847.m07.book.001" in reference_identity[9]


def test_ontology_extension_preserves_inference_boundaries() -> None:
    module = _module("dm847.m02")
    concept = next(
        item
        for item in module.concepts
        if item.concept_id == "semantic-closure-and-assertion-provenance"
    )
    exported = "\n".join((concept.body, *concept.key_points)).casefold()

    assert "asserted" in exported
    assert "inferred" in exported
    assert "closure" in exported
    assert "relation type" in exported
    assert "direction" in exported
    assert "path" in exported
    assert "ontology release" in exported
    assert "exact" in exported
    assert "expanded" in exported
    assert "regulates" in exported


def test_operon_extension_preserves_strand_aware_ordering_boundaries() -> None:
    module = _module("dm847.m07")
    concept = next(
        item
        for item in module.concepts
        if item.concept_id == "genomic-order-vs-transcriptional-order"
    )
    exported = "\n".join((concept.body, *concept.key_points)).casefold()

    assert "genomic order" in exported
    assert "transcriptional order" in exported
    assert "negative strand" in exported
    assert "before filtering by strand" in exported
    assert "upstream" in exported
    assert "downstream" in exported
    assert "reverse-complemented" in exported
    assert "does not prove co-transcription" in exported


def test_reviewed_modules_expose_specialized_source_basis() -> None:
    ontology = _module("dm847.m02")
    operons = _module("dm847.m07")

    assert "sdu-dm847-active-2025" in ontology.tutor_support.source_basis
    assert "coveney-2014-ch03-ch08" in ontology.tutor_support.source_basis
    assert "sdu-dm847-active-2025" in operons.tutor_support.source_basis
    assert "yachay-molecular-biology-ch19-ch26" in operons.tutor_support.source_basis


def test_new_examples_execute_deterministically(capsys) -> None:
    _run_example("dm847.m02", "m02.bg.e01")
    assert capsys.readouterr().out.rstrip("\n") == (
        "[('T-cell', ('T-cell',), 'asserted'), ('lymphocyte', "
        "('T-cell', 'lymphocyte'), 'inferred'), ('cell', "
        "('T-cell', 'lymphocyte', 'cell'), 'inferred')]"
    )

    _run_example("dm847.m07", "m07.bg.e01")
    assert capsys.readouterr().out.rstrip("\n") == (
        "[('g1', 'g2', 20), ('g4', 'g3', 20)]"
    )
