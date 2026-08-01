"""Regression tests for structured textbook evidence and DM847 enrichment."""

from __future__ import annotations

from contextlib import redirect_stdout
from io import StringIO

import pytest

from computational_biomedicine_study_hub.content.bibliography import (
    ContentEvidence,
    EvidenceStatus,
    TEXTBOOK_CATALOG,
    evidence_for_module,
    source_by_id,
    validate_evidence_catalog,
)
from computational_biomedicine_study_hub.content.dm847 import (
    DM847_TEXTBOOK_EVIDENCE,
    LOCALIZED_BUNDLES,
    LOCALIZED_MODULE_06_SUFFIX_ARRAYS_BWT_MAPPING,
)
from computational_biomedicine_study_hub.i18n import AppLocale


def test_textbook_catalog_has_stable_unique_sources() -> None:
    source_ids = tuple(source.source_id for source in TEXTBOOK_CATALOG)

    assert len(source_ids) == len(set(source_ids))
    assert source_by_id("compeau-pevzner-v2-2e-2015").year == 2015
    assert source_by_id("ims-2e-2024").publisher == "OpenIntro"


def test_unknown_bibliographic_source_is_rejected() -> None:
    invalid = (
        ContentEvidence(
            evidence_id="invalid.source",
            course_code="DM847",
            module_id="dm847.m06",
            content_ids=("suffix-tree",),
            source_id="missing-source",
            locator="Chapter 1",
            supported_scope="Invalid fixture",
            status=EvidenceStatus.PENDING,
        ),
    )

    with pytest.raises(ValueError, match="unknown sources"):
        validate_evidence_catalog(invalid)


def test_dm847_module_06_has_verified_textbook_evidence() -> None:
    evidence = evidence_for_module(DM847_TEXTBOOK_EVIDENCE, "dm847.m06")

    assert len(evidence) == 1
    assert evidence[0].status is EvidenceStatus.VERIFIED
    assert "suffix-tree" in evidence[0].content_ids
    assert "implementation challenges 9I–9R" in evidence[0].locator


def test_dm847_module_06_enrichment_is_trilingual_and_stable() -> None:
    localized = LOCALIZED_MODULE_06_SUFFIX_ARRAYS_BWT_MAPPING
    concept_ids = tuple(concept.concept_id for concept in localized.concepts)
    example_ids = tuple(example.example_id for example in localized.worked_examples)
    practice_ids = tuple(exercise.exercise_id for exercise in localized.practice_exercises)

    assert concept_ids[-2:] == ("suffix-tree", "index-equivalence")
    assert example_ids[-1] == "m06.e04"
    assert practice_ids[-2:] == ("m06.p09", "m06.p10")

    for locale in AppLocale:
        module = localized.materialize(locale)
        assert module.concepts[-2].body.strip()
        assert module.concepts[-1].body.strip()
        assert module.practice_exercises[-1].solution.strip()


def test_longest_repeat_example_executes_with_expected_output() -> None:
    module = LOCALIZED_MODULE_06_SUFFIX_ARRAYS_BWT_MAPPING.materialize(AppLocale.ENGLISH)
    worked_example = next(
        example for example in module.worked_examples if example.example_id == "m06.e04"
    )
    output = StringIO()

    with redirect_stdout(output):
        exec(worked_example.code, {})

    assert output.getvalue().strip() == worked_example.expected_output
    assert worked_example.expected_output == "ana"


def test_dm847_module_06_bundle_version_was_incremented() -> None:
    module_06_bundle = next(
        bundle
        for bundle in LOCALIZED_BUNDLES
        if bundle.localized_module.module_id == "dm847.m06"
    )

    assert module_06_bundle.content_version == "1.1.0"
