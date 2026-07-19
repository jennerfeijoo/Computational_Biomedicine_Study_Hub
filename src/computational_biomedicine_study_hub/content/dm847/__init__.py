"""Complete trilingual authored content and validated runtime bundles for DM847."""

from __future__ import annotations

from ...i18n import AppLocale
from ..bundles import LocalizedModuleBundle, validate_bundle_catalog
from .module_01_molecular_information import (
    LOCALIZED_MODULE_01_MOLECULAR_INFORMATION,
    LOCALIZED_OBJECTIVE_QUESTION_BANK_01,
    materialize_module_01_question_bank,
)

LOCALIZED_BUNDLES = (
    LocalizedModuleBundle(
        localized_module=LOCALIZED_MODULE_01_MOLECULAR_INFORMATION,
        localized_objective_question_bank=LOCALIZED_OBJECTIVE_QUESTION_BANK_01,
        content_version="1.0.0",
    ),
)
validate_bundle_catalog(LOCALIZED_BUNDLES)

BUNDLES = tuple(bundle.materialize(AppLocale.SPANISH_SPAIN) for bundle in LOCALIZED_BUNDLES)

MODULE_01_MOLECULAR_INFORMATION = BUNDLES[0].module
OBJECTIVE_QUESTION_BANK_01 = BUNDLES[0].objective_question_bank

MODULES = tuple(bundle.module for bundle in BUNDLES)
LOCALIZED_MODULES = tuple(bundle.localized_module for bundle in LOCALIZED_BUNDLES)
OBJECTIVE_QUESTION_BANKS = {
    bundle.module.module_id: bundle.objective_question_bank for bundle in BUNDLES
}

__all__ = [
    "BUNDLES",
    "LOCALIZED_BUNDLES",
    "LOCALIZED_MODULES",
    "LOCALIZED_MODULE_01_MOLECULAR_INFORMATION",
    "LOCALIZED_OBJECTIVE_QUESTION_BANK_01",
    "MODULES",
    "MODULE_01_MOLECULAR_INFORMATION",
    "OBJECTIVE_QUESTION_BANKS",
    "OBJECTIVE_QUESTION_BANK_01",
    "materialize_module_01_question_bank",
]
