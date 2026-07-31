"""Trilingual authored content and runtime bundles for BMB830."""

from __future__ import annotations

from ...i18n import AppLocale
from ..bundles import LocalizedModuleBundle, validate_bundle_catalog
from .module_01_r_foundations import (
    LOCALIZED_MODULE_01_R_FOUNDATIONS,
    LOCALIZED_OBJECTIVE_QUESTION_BANK_01,
    materialize_module_01_question_bank,
)
from .module_02_data_summary import (
    LOCALIZED_MODULE_02_DATA_SUMMARY,
    LOCALIZED_OBJECTIVE_QUESTION_BANK_02,
    materialize_module_02_question_bank,
)
from .module_03_probability import (
    LOCALIZED_MODULE_03_PROBABILITY,
    LOCALIZED_OBJECTIVE_QUESTION_BANK_03,
    materialize_module_03_question_bank,
)
from .module_04_estimation import (
    LOCALIZED_MODULE_04_ESTIMATION,
    LOCALIZED_OBJECTIVE_QUESTION_BANK_04,
    materialize_module_04_question_bank,
)
from .module_05_hypothesis_testing import (
    LOCALIZED_MODULE_05_HYPOTHESIS_TESTING,
    LOCALIZED_OBJECTIVE_QUESTION_BANK_05,
    materialize_module_05_question_bank,
)
from .module_06_group_comparison import (
    LOCALIZED_MODULE_06_GROUP_COMPARISON,
    LOCALIZED_OBJECTIVE_QUESTION_BANK_06,
    materialize_module_06_question_bank,
)
from .module_07_correlation_regression import (
    LOCALIZED_MODULE_07_CORRELATION_REGRESSION,
    LOCALIZED_OBJECTIVE_QUESTION_BANK_07,
    materialize_module_07_question_bank,
)
from .module_08_multiple_regression import (
    LOCALIZED_MODULE_08_MULTIPLE_REGRESSION,
    LOCALIZED_OBJECTIVE_QUESTION_BANK_08,
    materialize_module_08_question_bank,
)

LOCALIZED_BUNDLES = (
    LocalizedModuleBundle(
        LOCALIZED_MODULE_01_R_FOUNDATIONS,
        LOCALIZED_OBJECTIVE_QUESTION_BANK_01,
        "1.0.0",
    ),
    LocalizedModuleBundle(
        LOCALIZED_MODULE_02_DATA_SUMMARY,
        LOCALIZED_OBJECTIVE_QUESTION_BANK_02,
        "1.0.0",
    ),
    LocalizedModuleBundle(
        LOCALIZED_MODULE_03_PROBABILITY,
        LOCALIZED_OBJECTIVE_QUESTION_BANK_03,
        "1.0.0",
    ),
    LocalizedModuleBundle(
        LOCALIZED_MODULE_04_ESTIMATION,
        LOCALIZED_OBJECTIVE_QUESTION_BANK_04,
        "1.0.0",
    ),
    LocalizedModuleBundle(
        LOCALIZED_MODULE_05_HYPOTHESIS_TESTING,
        LOCALIZED_OBJECTIVE_QUESTION_BANK_05,
        "1.0.0",
    ),
    LocalizedModuleBundle(
        LOCALIZED_MODULE_06_GROUP_COMPARISON,
        LOCALIZED_OBJECTIVE_QUESTION_BANK_06,
        "1.0.0",
    ),
    LocalizedModuleBundle(
        LOCALIZED_MODULE_07_CORRELATION_REGRESSION,
        LOCALIZED_OBJECTIVE_QUESTION_BANK_07,
        "1.0.0",
    ),
    LocalizedModuleBundle(
        LOCALIZED_MODULE_08_MULTIPLE_REGRESSION,
        LOCALIZED_OBJECTIVE_QUESTION_BANK_08,
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

MODULE_01_R_FOUNDATIONS = BUNDLES[0].module
MODULE_02_DATA_SUMMARY = BUNDLES[1].module
MODULE_03_PROBABILITY = BUNDLES[2].module
MODULE_04_ESTIMATION = BUNDLES[3].module
MODULE_05_HYPOTHESIS_TESTING = BUNDLES[4].module
MODULE_06_GROUP_COMPARISON = BUNDLES[5].module
MODULE_07_CORRELATION_REGRESSION = BUNDLES[6].module
MODULE_08_MULTIPLE_REGRESSION = BUNDLES[7].module

OBJECTIVE_QUESTION_BANK_01 = BUNDLES[0].objective_question_bank
OBJECTIVE_QUESTION_BANK_02 = BUNDLES[1].objective_question_bank
OBJECTIVE_QUESTION_BANK_03 = BUNDLES[2].objective_question_bank
OBJECTIVE_QUESTION_BANK_04 = BUNDLES[3].objective_question_bank
OBJECTIVE_QUESTION_BANK_05 = BUNDLES[4].objective_question_bank
OBJECTIVE_QUESTION_BANK_06 = BUNDLES[5].objective_question_bank
OBJECTIVE_QUESTION_BANK_07 = BUNDLES[6].objective_question_bank
OBJECTIVE_QUESTION_BANK_08 = BUNDLES[7].objective_question_bank

__all__ = [
    "BUNDLES",
    "LOCALIZED_BUNDLES",
    "LOCALIZED_MODULES",
    "LOCALIZED_MODULE_01_R_FOUNDATIONS",
    "LOCALIZED_MODULE_02_DATA_SUMMARY",
    "LOCALIZED_MODULE_03_PROBABILITY",
    "LOCALIZED_MODULE_04_ESTIMATION",
    "LOCALIZED_MODULE_05_HYPOTHESIS_TESTING",
    "LOCALIZED_MODULE_06_GROUP_COMPARISON",
    "LOCALIZED_MODULE_07_CORRELATION_REGRESSION",
    "LOCALIZED_MODULE_08_MULTIPLE_REGRESSION",
    "LOCALIZED_OBJECTIVE_QUESTION_BANK_01",
    "LOCALIZED_OBJECTIVE_QUESTION_BANK_02",
    "LOCALIZED_OBJECTIVE_QUESTION_BANK_03",
    "LOCALIZED_OBJECTIVE_QUESTION_BANK_04",
    "LOCALIZED_OBJECTIVE_QUESTION_BANK_05",
    "LOCALIZED_OBJECTIVE_QUESTION_BANK_06",
    "LOCALIZED_OBJECTIVE_QUESTION_BANK_07",
    "LOCALIZED_OBJECTIVE_QUESTION_BANK_08",
    "MODULES",
    "MODULE_01_R_FOUNDATIONS",
    "MODULE_02_DATA_SUMMARY",
    "MODULE_03_PROBABILITY",
    "MODULE_04_ESTIMATION",
    "MODULE_05_HYPOTHESIS_TESTING",
    "MODULE_06_GROUP_COMPARISON",
    "MODULE_07_CORRELATION_REGRESSION",
    "MODULE_08_MULTIPLE_REGRESSION",
    "OBJECTIVE_QUESTION_BANKS",
    "OBJECTIVE_QUESTION_BANK_01",
    "OBJECTIVE_QUESTION_BANK_02",
    "OBJECTIVE_QUESTION_BANK_03",
    "OBJECTIVE_QUESTION_BANK_04",
    "OBJECTIVE_QUESTION_BANK_05",
    "OBJECTIVE_QUESTION_BANK_06",
    "OBJECTIVE_QUESTION_BANK_07",
    "OBJECTIVE_QUESTION_BANK_08",
    "materialize_module_01_question_bank",
    "materialize_module_02_question_bank",
    "materialize_module_03_question_bank",
    "materialize_module_04_question_bank",
    "materialize_module_05_question_bank",
    "materialize_module_06_question_bank",
    "materialize_module_07_question_bank",
    "materialize_module_08_question_bank",
]
