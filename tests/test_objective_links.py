from __future__ import annotations

import pytest

from computational_biomedicine_study_hub.content.dm847 import LOCALIZED_BUNDLES
from computational_biomedicine_study_hub.content.objective_links import (
    DM847_M01_OBJECTIVE_LINKS,
    ObjectiveLink,
    ObjectiveLinkCatalog,
    objective_links_for_module,
)
from computational_biomedicine_study_hub.i18n import AppLocale


def test_module_01_mapping_exactly_covers_every_assessable_activity() -> None:
    bundle = LOCALIZED_BUNDLES[0].materialize(AppLocale.SPANISH_SPAIN)
    catalog = bundle.objective_links

    assert catalog is DM847_M01_OBJECTIVE_LINKS
    expected_ids = {
        *(exercise.exercise_id for exercise in bundle.module.practice_exercises),
        *(item.item_id for item in bundle.module.assessment_items),
        *(item.item_id for item in bundle.objective_question_bank),
    }
    assert set(catalog.activity_ids) == expected_ids
    assert len(catalog.activity_ids) == 38


def test_module_01_mapping_is_identical_in_every_locale() -> None:
    catalogs = tuple(
        LOCALIZED_BUNDLES[0].materialize(locale).objective_links for locale in AppLocale
    )

    assert all(catalog is DM847_M01_OBJECTIVE_LINKS for catalog in catalogs)
    assert catalogs[0] is catalogs[1] is catalogs[2]


def test_every_module_01_objective_receives_practice_and_assessment_evidence() -> None:
    objective_ids = {f"m01.o{index}" for index in range(1, 7)}
    practice_targets = {
        objective_id
        for link in DM847_M01_OBJECTIVE_LINKS.links
        if ".p" in link.activity_id
        for objective_id in link.objective_ids
    }
    assessment_targets = {
        objective_id
        for link in DM847_M01_OBJECTIVE_LINKS.links
        if ".assessment." in link.activity_id or ".bank." in link.activity_id
        for objective_id in link.objective_ids
    }

    assert practice_targets == objective_ids
    assert assessment_targets == objective_ids


def test_specific_multidimensional_activities_keep_all_objective_links() -> None:
    assert DM847_M01_OBJECTIVE_LINKS.objectives_for("m01.p04") == (
        "m01.o4",
        "m01.o6",
    )
    assert DM847_M01_OBJECTIVE_LINKS.objectives_for("dm847.m01.bank.006") == (
        "m01.o5",
        "m01.o6",
    )
    assert DM847_M01_OBJECTIVE_LINKS.objectives_for("unknown") == ()


def test_unmapped_modules_do_not_receive_inferred_objectives() -> None:
    assert objective_links_for_module("dm847.m02") is None
    assert LOCALIZED_BUNDLES[1].objective_links is None


def test_catalog_rejects_duplicate_activity_ids() -> None:
    duplicate = ObjectiveLink("m01.p01", ("m01.o1",))

    with pytest.raises(ValueError, match="duplicate linked activity IDs"):
        ObjectiveLinkCatalog("dm847.m01", (duplicate, duplicate))


def test_catalog_validation_rejects_unknown_objectives() -> None:
    bundle = LOCALIZED_BUNDLES[0].materialize(AppLocale.ENGLISH)
    links = tuple(
        ObjectiveLink(link.activity_id, ("m01.missing",))
        if link.activity_id == "m01.p01"
        else link
        for link in DM847_M01_OBJECTIVE_LINKS.links
    )
    invalid = ObjectiveLinkCatalog("dm847.m01", links)

    with pytest.raises(ValueError, match="unknown objectives"):
        invalid.validate_against(bundle.module, bundle.objective_question_bank)
