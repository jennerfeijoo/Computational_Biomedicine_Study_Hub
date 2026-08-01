"""Trilingual authored content and runtime bundles for BMB831."""

from __future__ import annotations

from ...i18n import AppLocale
from ..bundles import LocalizedModuleBundle, validate_bundle_catalog
from .module_01_synthea_workflows import (
    LOCALIZED_MODULE_01_SYNTHEA_WORKFLOWS,
    LOCALIZED_OBJECTIVE_QUESTION_BANK_01,
    materialize_module_01_question_bank,
)
from .module_02_omics_matrices_qc import (
    LOCALIZED_MODULE_02_OMICS_MATRICES_QC,
    LOCALIZED_OBJECTIVE_QUESTION_BANK_02,
    materialize_module_02_question_bank,
)
from .module_03_differential_modeling import (
    LOCALIZED_MODULE_03_DIFFERENTIAL_MODELING,
    LOCALIZED_OBJECTIVE_QUESTION_BANK_03,
    materialize_module_03_question_bank,
)

LOCALIZED_BUNDLES = (
    LocalizedModuleBundle(
        LOCALIZED_MODULE_01_SYNTHEA_WORKFLOWS,
        LOCALIZED_OBJECTIVE_QUESTION_BANK_01,
        "1.0.0",
    ),
    LocalizedModuleBundle(
        LOCALIZED_MODULE_02_OMICS_MATRICES_QC,
        LOCALIZED_OBJECTIVE_QUESTION_BANK_02,
        "1.0.0",
    ),
    LocalizedModuleBundle(
        LOCALIZED_MODULE_03_DIFFERENTIAL_MODELING,
        LOCALIZED_OBJECTIVE_QUESTION_BANK_03,
        "1.0.0",
    ),
)
validate_bundle_catalog(LOCALIZED_BUNDLES)

BUNDLES = tuple(bundle.materialize(AppLocale.SPANISH_SPAIN) for bundle in LOCALIZED_BUNDLES)
LOCALIZED_MODULES = tuple(bundle.localized_module for bundle in LOCALIZED_BUNDLES)
MODULES = tuple(bundle.module for bundle in BUNDLES)
OBJECTIVE_QUESTION_BANKS = {
    bundle.module.module_id: bundle.objective_question_bank for bundle in BUNDLES
}

MODULE_01_SYNTHEA_WORKFLOWS = BUNDLES[0].module
MODULE_02_OMICS_MATRICES_QC = BUNDLES[1].module
MODULE_03_DIFFERENTIAL_MODELING = BUNDLES[2].module
OBJECTIVE_QUESTION_BANK_01 = BUNDLES[0].objective_question_bank
OBJECTIVE_QUESTION_BANK_02 = BUNDLES[1].objective_question_bank
OBJECTIVE_QUESTION_BANK_03 = BUNDLES[2].objective_question_bank

__all__ = [
    "BUNDLES",
    "LOCALIZED_BUNDLES",
    "LOCALIZED_MODULES",
    "LOCALIZED_MODULE_01_SYNTHEA_WORKFLOWS",
    "LOCALIZED_MODULE_02_OMICS_MATRICES_QC",
    "LOCALIZED_MODULE_03_DIFFERENTIAL_MODELING",
    "LOCALIZED_OBJECTIVE_QUESTION_BANK_01",
    "LOCALIZED_OBJECTIVE_QUESTION_BANK_02",
    "LOCALIZED_OBJECTIVE_QUESTION_BANK_03",
    "MODULES",
    "MODULE_01_SYNTHEA_WORKFLOWS",
    "MODULE_02_OMICS_MATRICES_QC",
    "MODULE_03_DIFFERENTIAL_MODELING",
    "OBJECTIVE_QUESTION_BANKS",
    "OBJECTIVE_QUESTION_BANK_01",
    "OBJECTIVE_QUESTION_BANK_02",
    "OBJECTIVE_QUESTION_BANK_03",
    "materialize_module_01_question_bank",
    "materialize_module_02_question_bank",
    "materialize_module_03_question_bank",
]
