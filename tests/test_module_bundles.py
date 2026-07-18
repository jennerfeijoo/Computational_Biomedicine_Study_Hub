from __future__ import annotations

import pytest

from computational_biomedicine_study_hub.content import (
    LocalizedModuleBundle,
    validate_bundle_catalog,
)
from computational_biomedicine_study_hub.content.dm857 import (
    BUNDLES,
    LOCALIZED_BUNDLES,
    LOCALIZED_MODULE_01_FOUNDATIONS,
    LOCALIZED_OBJECTIVE_QUESTION_BANK,
)
from computational_biomedicine_study_hub.i18n import AppLocale


def test_dm857_bundle_catalog_covers_every_completed_module_once() -> None:
    validate_bundle_catalog(LOCALIZED_BUNDLES)

    assert len(LOCALIZED_BUNDLES) == 3
    assert len(BUNDLES) == 3
    assert [bundle.module.module_id for bundle in BUNDLES] == [
        "dm857.m01",
        "dm857.m02",
        "dm857.m03",
    ]
    assert all(bundle.content_version == "1.0.0" for bundle in BUNDLES)
    assert all(bundle.objective_question_bank for bundle in BUNDLES)


def test_localized_bundle_materializes_module_and_bank_in_the_same_locale() -> None:
    bundle = LOCALIZED_BUNDLES[1].materialize(AppLocale.DANISH_DENMARK)

    assert bundle.module.module_id == "dm857.m02"
    assert bundle.module.title.startswith("Boolesk")
    assert all(item.prompt.strip() for item in bundle.objective_question_bank)
    assert all(item.option_ids for item in bundle.objective_question_bank)
    assert all(item.correct_option_ids for item in bundle.objective_question_bank)


def test_bundle_rejects_an_objective_bank_from_another_module() -> None:
    with pytest.raises(ValueError, match="out-of-scope"):
        LocalizedModuleBundle(
            localized_module=LOCALIZED_MODULE_01_FOUNDATIONS,
            localized_objective_question_bank=(LOCALIZED_OBJECTIVE_QUESTION_BANK[0],),
            content_version="1.0.0",
        )


def test_catalog_rejects_duplicate_modules() -> None:
    duplicate = LOCALIZED_BUNDLES[0]

    with pytest.raises(ValueError, match="duplicate module IDs"):
        validate_bundle_catalog((duplicate, duplicate))
