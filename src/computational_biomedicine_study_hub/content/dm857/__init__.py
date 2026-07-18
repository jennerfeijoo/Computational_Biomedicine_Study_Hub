"""Complete trilingual authored content and validated runtime bundles for DM857."""

from __future__ import annotations

from ...i18n import AppLocale
from ..bundles import LocalizedModuleBundle, validate_bundle_catalog
from .module_01_localized import LOCALIZED_MODULE as LOCALIZED_MODULE_01_FOUNDATIONS
from .module_01_objective_bank_localized import (
    LOCALIZED_OBJECTIVE_QUESTION_BANK,
    materialize_objective_question_bank,
)
from .module_02_conditionals import LOCALIZED_MODULE_02_CONDITIONALS
from .module_02_objective_bank import (
    LOCALIZED_OBJECTIVE_QUESTION_BANK_02,
    materialize_module_02_question_bank,
)
from .module_03_iteration import LOCALIZED_MODULE_03_ITERATION
from .module_03_objective_bank import (
    LOCALIZED_OBJECTIVE_QUESTION_BANK_03,
    materialize_module_03_question_bank,
)
from .module_04_functions import (
    LOCALIZED_MODULE_04_FUNCTIONS,
    LOCALIZED_OBJECTIVE_QUESTION_BANK_04,
    materialize_module_04_question_bank,
)
from .module_05_strings import (
    LOCALIZED_MODULE_05_STRINGS,
    LOCALIZED_OBJECTIVE_QUESTION_BANK_05,
    materialize_module_05_question_bank,
)
from .module_06_sequences import (
    LOCALIZED_MODULE_06_SEQUENCES,
    LOCALIZED_OBJECTIVE_QUESTION_BANK_06,
    materialize_module_06_question_bank,
)
from .module_07_mappings_sets import (
    LOCALIZED_MODULE_07_MAPPINGS_SETS,
    LOCALIZED_OBJECTIVE_QUESTION_BANK_07,
    materialize_module_07_question_bank,
)
from .module_08_files_exceptions import (
    LOCALIZED_MODULE_08_FILES_EXCEPTIONS,
    LOCALIZED_OBJECTIVE_QUESTION_BANK_08,
    materialize_module_08_question_bank,
)
from .module_09_recursion import (
    LOCALIZED_MODULE_09_RECURSION,
    LOCALIZED_OBJECTIVE_QUESTION_BANK_09,
    materialize_module_09_question_bank,
)

LOCALIZED_BUNDLES = (
    LocalizedModuleBundle(
        localized_module=LOCALIZED_MODULE_01_FOUNDATIONS,
        localized_objective_question_bank=LOCALIZED_OBJECTIVE_QUESTION_BANK,
        content_version="1.0.0",
    ),
    LocalizedModuleBundle(
        localized_module=LOCALIZED_MODULE_02_CONDITIONALS,
        localized_objective_question_bank=LOCALIZED_OBJECTIVE_QUESTION_BANK_02,
        content_version="1.0.0",
    ),
    LocalizedModuleBundle(
        localized_module=LOCALIZED_MODULE_03_ITERATION,
        localized_objective_question_bank=LOCALIZED_OBJECTIVE_QUESTION_BANK_03,
        content_version="1.0.0",
    ),
    LocalizedModuleBundle(
        localized_module=LOCALIZED_MODULE_04_FUNCTIONS,
        localized_objective_question_bank=LOCALIZED_OBJECTIVE_QUESTION_BANK_04,
        content_version="1.0.0",
    ),
    LocalizedModuleBundle(
        localized_module=LOCALIZED_MODULE_05_STRINGS,
        localized_objective_question_bank=LOCALIZED_OBJECTIVE_QUESTION_BANK_05,
        content_version="1.0.0",
    ),
    LocalizedModuleBundle(
        localized_module=LOCALIZED_MODULE_06_SEQUENCES,
        localized_objective_question_bank=LOCALIZED_OBJECTIVE_QUESTION_BANK_06,
        content_version="1.0.0",
    ),
    LocalizedModuleBundle(
        localized_module=LOCALIZED_MODULE_07_MAPPINGS_SETS,
        localized_objective_question_bank=LOCALIZED_OBJECTIVE_QUESTION_BANK_07,
        content_version="1.0.0",
    ),
    LocalizedModuleBundle(
        localized_module=LOCALIZED_MODULE_08_FILES_EXCEPTIONS,
        localized_objective_question_bank=LOCALIZED_OBJECTIVE_QUESTION_BANK_08,
        content_version="1.0.0",
    ),
    LocalizedModuleBundle(
        localized_module=LOCALIZED_MODULE_09_RECURSION,
        localized_objective_question_bank=LOCALIZED_OBJECTIVE_QUESTION_BANK_09,
        content_version="1.0.0",
    ),
)
validate_bundle_catalog(LOCALIZED_BUNDLES)

BUNDLES = tuple(bundle.materialize(AppLocale.SPANISH_SPAIN) for bundle in LOCALIZED_BUNDLES)

MODULE_01_FOUNDATIONS = BUNDLES[0].module
MODULE_02_CONDITIONALS = BUNDLES[1].module
MODULE_03_ITERATION = BUNDLES[2].module
MODULE_04_FUNCTIONS = BUNDLES[3].module
MODULE_05_STRINGS = BUNDLES[4].module
MODULE_06_SEQUENCES = BUNDLES[5].module
MODULE_07_MAPPINGS_SETS = BUNDLES[6].module
MODULE_08_FILES_EXCEPTIONS = BUNDLES[7].module
MODULE_09_RECURSION = BUNDLES[8].module

OBJECTIVE_QUESTION_BANK = BUNDLES[0].objective_question_bank
OBJECTIVE_QUESTION_BANK_02 = BUNDLES[1].objective_question_bank
OBJECTIVE_QUESTION_BANK_03 = BUNDLES[2].objective_question_bank
OBJECTIVE_QUESTION_BANK_04 = BUNDLES[3].objective_question_bank
OBJECTIVE_QUESTION_BANK_05 = BUNDLES[4].objective_question_bank
OBJECTIVE_QUESTION_BANK_06 = BUNDLES[5].objective_question_bank
OBJECTIVE_QUESTION_BANK_07 = BUNDLES[6].objective_question_bank
OBJECTIVE_QUESTION_BANK_08 = BUNDLES[7].objective_question_bank
OBJECTIVE_QUESTION_BANK_09 = BUNDLES[8].objective_question_bank

MODULES = tuple(bundle.module for bundle in BUNDLES)
LOCALIZED_MODULES = tuple(bundle.localized_module for bundle in LOCALIZED_BUNDLES)
OBJECTIVE_QUESTION_BANKS = {
    bundle.module.module_id: bundle.objective_question_bank for bundle in BUNDLES
}

__all__ = [
    "BUNDLES",
    "LOCALIZED_BUNDLES",
    "LOCALIZED_MODULES",
    "LOCALIZED_MODULE_01_FOUNDATIONS",
    "LOCALIZED_MODULE_02_CONDITIONALS",
    "LOCALIZED_MODULE_03_ITERATION",
    "LOCALIZED_MODULE_04_FUNCTIONS",
    "LOCALIZED_MODULE_05_STRINGS",
    "LOCALIZED_MODULE_06_SEQUENCES",
    "LOCALIZED_MODULE_07_MAPPINGS_SETS",
    "LOCALIZED_MODULE_08_FILES_EXCEPTIONS",
    "LOCALIZED_MODULE_09_RECURSION",
    "LOCALIZED_OBJECTIVE_QUESTION_BANK",
    "LOCALIZED_OBJECTIVE_QUESTION_BANK_02",
    "LOCALIZED_OBJECTIVE_QUESTION_BANK_03",
    "LOCALIZED_OBJECTIVE_QUESTION_BANK_04",
    "LOCALIZED_OBJECTIVE_QUESTION_BANK_05",
    "LOCALIZED_OBJECTIVE_QUESTION_BANK_06",
    "LOCALIZED_OBJECTIVE_QUESTION_BANK_07",
    "LOCALIZED_OBJECTIVE_QUESTION_BANK_08",
    "LOCALIZED_OBJECTIVE_QUESTION_BANK_09",
    "MODULES",
    "MODULE_01_FOUNDATIONS",
    "MODULE_02_CONDITIONALS",
    "MODULE_03_ITERATION",
    "MODULE_04_FUNCTIONS",
    "MODULE_05_STRINGS",
    "MODULE_06_SEQUENCES",
    "MODULE_07_MAPPINGS_SETS",
    "MODULE_08_FILES_EXCEPTIONS",
    "MODULE_09_RECURSION",
    "OBJECTIVE_QUESTION_BANK",
    "OBJECTIVE_QUESTION_BANKS",
    "OBJECTIVE_QUESTION_BANK_02",
    "OBJECTIVE_QUESTION_BANK_03",
    "OBJECTIVE_QUESTION_BANK_04",
    "OBJECTIVE_QUESTION_BANK_05",
    "OBJECTIVE_QUESTION_BANK_06",
    "OBJECTIVE_QUESTION_BANK_07",
    "OBJECTIVE_QUESTION_BANK_08",
    "OBJECTIVE_QUESTION_BANK_09",
    "materialize_module_02_question_bank",
    "materialize_module_03_question_bank",
    "materialize_module_04_question_bank",
    "materialize_module_05_question_bank",
    "materialize_module_06_question_bank",
    "materialize_module_07_question_bank",
    "materialize_module_08_question_bank",
    "materialize_module_09_question_bank",
    "materialize_objective_question_bank",
]
