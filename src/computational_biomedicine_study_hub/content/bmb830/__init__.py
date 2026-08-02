"""Trilingual authored content and runtime bundles for BMB830."""

from __future__ import annotations

from ...i18n import AppLocale
from ..bundles import LocalizedModuleBundle, validate_bundle_catalog
from .book_grounded_audit import (
    BMB830_BOOK_SOURCES,
    AcademicReference,
    ModuleSourceAudit,
    apply_foundation_review,
)
from .book_grounded_audit import (
    BMB830_MODULE_SOURCE_AUDIT as _BASE_BMB830_MODULE_SOURCE_AUDIT,
)
from .book_grounded_inference import apply_inference_review, update_inference_audit
from .book_grounded_regression import apply_regression_review, update_regression_audit
from .module_01_r_foundations import (
    LOCALIZED_MODULE_01_R_FOUNDATIONS as _BASE_LOCALIZED_MODULE_01_R_FOUNDATIONS,
)
from .module_01_r_foundations import (
    LOCALIZED_OBJECTIVE_QUESTION_BANK_01,
    materialize_module_01_question_bank,
)
from .module_02_data_summary import (
    LOCALIZED_MODULE_02_DATA_SUMMARY as _BASE_LOCALIZED_MODULE_02_DATA_SUMMARY,
)
from .module_02_data_summary import (
    LOCALIZED_OBJECTIVE_QUESTION_BANK_02,
    materialize_module_02_question_bank,
)
from .module_03_probability import (
    LOCALIZED_MODULE_03_PROBABILITY as _BASE_LOCALIZED_MODULE_03_PROBABILITY,
)
from .module_03_probability import (
    LOCALIZED_OBJECTIVE_QUESTION_BANK_03,
    materialize_module_03_question_bank,
)
from .module_04_estimation import (
    LOCALIZED_MODULE_04_ESTIMATION as _BASE_LOCALIZED_MODULE_04_ESTIMATION,
)
from .module_04_estimation import (
    LOCALIZED_OBJECTIVE_QUESTION_BANK_04,
    materialize_module_04_question_bank,
)
from .module_05_hypothesis_testing import (
    LOCALIZED_MODULE_05_HYPOTHESIS_TESTING as _BASE_LOCALIZED_MODULE_05_HYPOTHESIS_TESTING,
)
from .module_05_hypothesis_testing import (
    LOCALIZED_OBJECTIVE_QUESTION_BANK_05,
    materialize_module_05_question_bank,
)
from .module_06_group_comparison import (
    LOCALIZED_MODULE_06_GROUP_COMPARISON as _BASE_LOCALIZED_MODULE_06_GROUP_COMPARISON,
)
from .module_06_group_comparison import (
    LOCALIZED_OBJECTIVE_QUESTION_BANK_06,
    materialize_module_06_question_bank,
)
from .module_07_correlation_regression import (
    LOCALIZED_MODULE_07_CORRELATION_REGRESSION as _BASE_LOCALIZED_MODULE_07_CORRELATION_REGRESSION,
)
from .module_07_correlation_regression import (
    LOCALIZED_OBJECTIVE_QUESTION_BANK_07,
    materialize_module_07_question_bank,
)
from .module_08_multiple_regression import (
    LOCALIZED_MODULE_08_MULTIPLE_REGRESSION as _BASE_LOCALIZED_MODULE_08_MULTIPLE_REGRESSION,
)
from .module_08_multiple_regression import (
    LOCALIZED_OBJECTIVE_QUESTION_BANK_08,
    materialize_module_08_question_bank,
)
from .module_09_interactions_nonlinearity import (
    LOCALIZED_MODULE_09_INTERACTIONS_NONLINEARITY,
    LOCALIZED_OBJECTIVE_QUESTION_BANK_09,
    materialize_module_09_question_bank,
)
from .module_10_diagnostics_validation import (
    LOCALIZED_MODULE_10_DIAGNOSTICS_VALIDATION,
    LOCALIZED_OBJECTIVE_QUESTION_BANK_10,
    materialize_module_10_question_bank,
)
from .module_11_intro_multivariate import (
    LOCALIZED_MODULE_11_INTRO_MULTIVARIATE,
    LOCALIZED_OBJECTIVE_QUESTION_BANK_11,
    materialize_module_11_question_bank,
)
from .module_12_high_dimensional_case import (
    LOCALIZED_MODULE_12_HIGH_DIMENSIONAL_CASE,
    LOCALIZED_OBJECTIVE_QUESTION_BANK_12,
    materialize_module_12_question_bank,
)

_INFERENCE_BMB830_MODULE_SOURCE_AUDIT = update_inference_audit(
    _BASE_BMB830_MODULE_SOURCE_AUDIT
)
BMB830_MODULE_SOURCE_AUDIT = update_regression_audit(
    _INFERENCE_BMB830_MODULE_SOURCE_AUDIT
)

LOCALIZED_MODULE_01_R_FOUNDATIONS = apply_foundation_review(_BASE_LOCALIZED_MODULE_01_R_FOUNDATIONS)
LOCALIZED_MODULE_02_DATA_SUMMARY = apply_foundation_review(_BASE_LOCALIZED_MODULE_02_DATA_SUMMARY)
LOCALIZED_MODULE_03_PROBABILITY = apply_foundation_review(_BASE_LOCALIZED_MODULE_03_PROBABILITY)
LOCALIZED_MODULE_04_ESTIMATION = apply_foundation_review(_BASE_LOCALIZED_MODULE_04_ESTIMATION)
LOCALIZED_MODULE_05_HYPOTHESIS_TESTING = apply_inference_review(
    _BASE_LOCALIZED_MODULE_05_HYPOTHESIS_TESTING
)
LOCALIZED_MODULE_06_GROUP_COMPARISON = apply_inference_review(
    _BASE_LOCALIZED_MODULE_06_GROUP_COMPARISON
)
LOCALIZED_MODULE_07_CORRELATION_REGRESSION = apply_regression_review(
    _BASE_LOCALIZED_MODULE_07_CORRELATION_REGRESSION
)
LOCALIZED_MODULE_08_MULTIPLE_REGRESSION = apply_regression_review(
    _BASE_LOCALIZED_MODULE_08_MULTIPLE_REGRESSION
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
        "1.1.0",
    ),
    LocalizedModuleBundle(
        LOCALIZED_MODULE_04_ESTIMATION,
        LOCALIZED_OBJECTIVE_QUESTION_BANK_04,
        "1.1.0",
    ),
    LocalizedModuleBundle(
        LOCALIZED_MODULE_05_HYPOTHESIS_TESTING,
        LOCALIZED_OBJECTIVE_QUESTION_BANK_05,
        "1.1.0",
    ),
    LocalizedModuleBundle(
        LOCALIZED_MODULE_06_GROUP_COMPARISON,
        LOCALIZED_OBJECTIVE_QUESTION_BANK_06,
        "1.1.0",
    ),
    LocalizedModuleBundle(
        LOCALIZED_MODULE_07_CORRELATION_REGRESSION,
        LOCALIZED_OBJECTIVE_QUESTION_BANK_07,
        "1.1.0",
    ),
    LocalizedModuleBundle(
        LOCALIZED_MODULE_08_MULTIPLE_REGRESSION,
        LOCALIZED_OBJECTIVE_QUESTION_BANK_08,
        "1.1.0",
    ),
    LocalizedModuleBundle(
        LOCALIZED_MODULE_09_INTERACTIONS_NONLINEARITY,
        LOCALIZED_OBJECTIVE_QUESTION_BANK_09,
        "1.0.0",
    ),
    LocalizedModuleBundle(
        LOCALIZED_MODULE_10_DIAGNOSTICS_VALIDATION,
        LOCALIZED_OBJECTIVE_QUESTION_BANK_10,
        "1.0.0",
    ),
    LocalizedModuleBundle(
        LOCALIZED_MODULE_11_INTRO_MULTIVARIATE,
        LOCALIZED_OBJECTIVE_QUESTION_BANK_11,
        "1.0.0",
    ),
    LocalizedModuleBundle(
        LOCALIZED_MODULE_12_HIGH_DIMENSIONAL_CASE,
        LOCALIZED_OBJECTIVE_QUESTION_BANK_12,
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
MODULE_09_INTERACTIONS_NONLINEARITY = BUNDLES[8].module
MODULE_10_DIAGNOSTICS_VALIDATION = BUNDLES[9].module
MODULE_11_INTRO_MULTIVARIATE = BUNDLES[10].module
MODULE_12_HIGH_DIMENSIONAL_CASE = BUNDLES[11].module

OBJECTIVE_QUESTION_BANK_01 = BUNDLES[0].objective_question_bank
OBJECTIVE_QUESTION_BANK_02 = BUNDLES[1].objective_question_bank
OBJECTIVE_QUESTION_BANK_03 = BUNDLES[2].objective_question_bank
OBJECTIVE_QUESTION_BANK_04 = BUNDLES[3].objective_question_bank
OBJECTIVE_QUESTION_BANK_05 = BUNDLES[4].objective_question_bank
OBJECTIVE_QUESTION_BANK_06 = BUNDLES[5].objective_question_bank
OBJECTIVE_QUESTION_BANK_07 = BUNDLES[6].objective_question_bank
OBJECTIVE_QUESTION_BANK_08 = BUNDLES[7].objective_question_bank
OBJECTIVE_QUESTION_BANK_09 = BUNDLES[8].objective_question_bank
OBJECTIVE_QUESTION_BANK_10 = BUNDLES[9].objective_question_bank
OBJECTIVE_QUESTION_BANK_11 = BUNDLES[10].objective_question_bank
OBJECTIVE_QUESTION_BANK_12 = BUNDLES[11].objective_question_bank

__all__ = [
    "AcademicReference",
    "BMB830_BOOK_SOURCES",
    "BMB830_MODULE_SOURCE_AUDIT",
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
    "LOCALIZED_MODULE_09_INTERACTIONS_NONLINEARITY",
    "LOCALIZED_MODULE_10_DIAGNOSTICS_VALIDATION",
    "LOCALIZED_MODULE_11_INTRO_MULTIVARIATE",
    "LOCALIZED_MODULE_12_HIGH_DIMENSIONAL_CASE",
    "LOCALIZED_OBJECTIVE_QUESTION_BANK_01",
    "LOCALIZED_OBJECTIVE_QUESTION_BANK_02",
    "LOCALIZED_OBJECTIVE_QUESTION_BANK_03",
    "LOCALIZED_OBJECTIVE_QUESTION_BANK_04",
    "LOCALIZED_OBJECTIVE_QUESTION_BANK_05",
    "LOCALIZED_OBJECTIVE_QUESTION_BANK_06",
    "LOCALIZED_OBJECTIVE_QUESTION_BANK_07",
    "LOCALIZED_OBJECTIVE_QUESTION_BANK_08",
    "LOCALIZED_OBJECTIVE_QUESTION_BANK_09",
    "LOCALIZED_OBJECTIVE_QUESTION_BANK_10",
    "LOCALIZED_OBJECTIVE_QUESTION_BANK_11",
    "LOCALIZED_OBJECTIVE_QUESTION_BANK_12",
    "MODULES",
    "MODULE_01_R_FOUNDATIONS",
    "MODULE_02_DATA_SUMMARY",
    "MODULE_03_PROBABILITY",
    "MODULE_04_ESTIMATION",
    "MODULE_05_HYPOTHESIS_TESTING",
    "MODULE_06_GROUP_COMPARISON",
    "MODULE_07_CORRELATION_REGRESSION",
    "MODULE_08_MULTIPLE_REGRESSION",
    "MODULE_09_INTERACTIONS_NONLINEARITY",
    "MODULE_10_DIAGNOSTICS_VALIDATION",
    "MODULE_11_INTRO_MULTIVARIATE",
    "MODULE_12_HIGH_DIMENSIONAL_CASE",
    "ModuleSourceAudit",
    "OBJECTIVE_QUESTION_BANKS",
    "OBJECTIVE_QUESTION_BANK_01",
    "OBJECTIVE_QUESTION_BANK_02",
    "OBJECTIVE_QUESTION_BANK_03",
    "OBJECTIVE_QUESTION_BANK_04",
    "OBJECTIVE_QUESTION_BANK_05",
    "OBJECTIVE_QUESTION_BANK_06",
    "OBJECTIVE_QUESTION_BANK_07",
    "OBJECTIVE_QUESTION_BANK_08",
    "OBJECTIVE_QUESTION_BANK_09",
    "OBJECTIVE_QUESTION_BANK_10",
    "OBJECTIVE_QUESTION_BANK_11",
    "OBJECTIVE_QUESTION_BANK_12",
    "materialize_module_01_question_bank",
    "materialize_module_02_question_bank",
    "materialize_module_03_question_bank",
    "materialize_module_04_question_bank",
    "materialize_module_05_question_bank",
    "materialize_module_06_question_bank",
    "materialize_module_07_question_bank",
    "materialize_module_08_question_bank",
    "materialize_module_09_question_bank",
    "materialize_module_10_question_bank",
    "materialize_module_11_question_bank",
    "materialize_module_12_question_bank",
]
