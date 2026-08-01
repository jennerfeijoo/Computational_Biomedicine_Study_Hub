"""Complete trilingual authored content and validated runtime bundles for DM857."""

from __future__ import annotations

from ...i18n import AppLocale
from ..bundles import LocalizedModuleBundle, validate_bundle_catalog
from .book_grounded_adts import (
    apply_adts_book_extension,
    update_adts_audit,
)
from .book_grounded_extensions import (
    DM857_BOOK_SOURCES,
    apply_book_grounded_extensions,
)
from .book_grounded_extensions import (
    DM857_MODULE_SOURCE_AUDIT as _BASE_DM857_MODULE_SOURCE_AUDIT,
)
from .book_grounded_foundations import (
    apply_foundations_book_extensions,
    update_foundations_audit,
)
from .book_grounded_oop import (
    apply_oop_book_extension,
    update_oop_audit,
)
from .book_grounded_scientific_libraries import (
    apply_scientific_libraries_book_extension,
    update_scientific_libraries_audit,
)
from .book_grounded_strings_mappings import (
    apply_strings_mappings_book_extensions,
    update_strings_mappings_audit,
)
from .book_grounded_trees import (
    apply_trees_book_extension,
    update_trees_audit,
)
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
from .module_10_trees import (
    LOCALIZED_MODULE_10_TREES,
    LOCALIZED_OBJECTIVE_QUESTION_BANK_10,
    materialize_module_10_question_bank,
)
from .module_11_adts import (
    LOCALIZED_MODULE_11_ADTS,
    LOCALIZED_OBJECTIVE_QUESTION_BANK_11,
    materialize_module_11_question_bank,
)
from .module_12_oop import (
    LOCALIZED_MODULE_12_OOP,
    LOCALIZED_OBJECTIVE_QUESTION_BANK_12,
    materialize_module_12_question_bank,
)
from .module_13_scientific_libraries import (
    LOCALIZED_MODULE_13_SCIENTIFIC_LIBRARIES,
    LOCALIZED_OBJECTIVE_QUESTION_BANK_13,
    materialize_module_13_question_bank,
)
from .module_14_testing_debugging_quality import (
    LOCALIZED_MODULE_14_TESTING_DEBUGGING_QUALITY,
    LOCALIZED_OBJECTIVE_QUESTION_BANK_14,
    materialize_module_14_question_bank,
)

DM857_MODULE_SOURCE_AUDIT = update_scientific_libraries_audit(
    update_oop_audit(
        update_adts_audit(
            update_trees_audit(
                update_strings_mappings_audit(
                    update_foundations_audit(_BASE_DM857_MODULE_SOURCE_AUDIT)
                )
            )
        )
    )
)

(
    LOCALIZED_MODULE_01_FOUNDATIONS,
    LOCALIZED_MODULE_02_CONDITIONALS,
    LOCALIZED_MODULE_03_ITERATION,
    LOCALIZED_MODULE_04_FUNCTIONS,
    LOCALIZED_MODULE_05_STRINGS,
    LOCALIZED_MODULE_06_SEQUENCES,
    LOCALIZED_MODULE_07_MAPPINGS_SETS,
    LOCALIZED_MODULE_08_FILES_EXCEPTIONS,
    LOCALIZED_MODULE_09_RECURSION,
    LOCALIZED_MODULE_10_TREES,
    LOCALIZED_MODULE_11_ADTS,
    LOCALIZED_MODULE_12_OOP,
    LOCALIZED_MODULE_13_SCIENTIFIC_LIBRARIES,
    LOCALIZED_MODULE_14_TESTING_DEBUGGING_QUALITY,
) = apply_scientific_libraries_book_extension(
    apply_oop_book_extension(
        apply_adts_book_extension(
            apply_trees_book_extension(
                apply_strings_mappings_book_extensions(
                    apply_foundations_book_extensions(
                        apply_book_grounded_extensions(
                            (
                                LOCALIZED_MODULE_01_FOUNDATIONS,
                                LOCALIZED_MODULE_02_CONDITIONALS,
                                LOCALIZED_MODULE_03_ITERATION,
                                LOCALIZED_MODULE_04_FUNCTIONS,
                                LOCALIZED_MODULE_05_STRINGS,
                                LOCALIZED_MODULE_06_SEQUENCES,
                                LOCALIZED_MODULE_07_MAPPINGS_SETS,
                                LOCALIZED_MODULE_08_FILES_EXCEPTIONS,
                                LOCALIZED_MODULE_09_RECURSION,
                                LOCALIZED_MODULE_10_TREES,
                                LOCALIZED_MODULE_11_ADTS,
                                LOCALIZED_MODULE_12_OOP,
                                LOCALIZED_MODULE_13_SCIENTIFIC_LIBRARIES,
                                LOCALIZED_MODULE_14_TESTING_DEBUGGING_QUALITY,
                            )
                        )
                    )
                )
            )
        )
    )
)

_LOCALIZED_MODULES = (
    LOCALIZED_MODULE_01_FOUNDATIONS,
    LOCALIZED_MODULE_02_CONDITIONALS,
    LOCALIZED_MODULE_03_ITERATION,
    LOCALIZED_MODULE_04_FUNCTIONS,
    LOCALIZED_MODULE_05_STRINGS,
    LOCALIZED_MODULE_06_SEQUENCES,
    LOCALIZED_MODULE_07_MAPPINGS_SETS,
    LOCALIZED_MODULE_08_FILES_EXCEPTIONS,
    LOCALIZED_MODULE_09_RECURSION,
    LOCALIZED_MODULE_10_TREES,
    LOCALIZED_MODULE_11_ADTS,
    LOCALIZED_MODULE_12_OOP,
    LOCALIZED_MODULE_13_SCIENTIFIC_LIBRARIES,
    LOCALIZED_MODULE_14_TESTING_DEBUGGING_QUALITY,
)

_LOCALIZED_OBJECTIVE_BANKS = (
    LOCALIZED_OBJECTIVE_QUESTION_BANK,
    LOCALIZED_OBJECTIVE_QUESTION_BANK_02,
    LOCALIZED_OBJECTIVE_QUESTION_BANK_03,
    LOCALIZED_OBJECTIVE_QUESTION_BANK_04,
    LOCALIZED_OBJECTIVE_QUESTION_BANK_05,
    LOCALIZED_OBJECTIVE_QUESTION_BANK_06,
    LOCALIZED_OBJECTIVE_QUESTION_BANK_07,
    LOCALIZED_OBJECTIVE_QUESTION_BANK_08,
    LOCALIZED_OBJECTIVE_QUESTION_BANK_09,
    LOCALIZED_OBJECTIVE_QUESTION_BANK_10,
    LOCALIZED_OBJECTIVE_QUESTION_BANK_11,
    LOCALIZED_OBJECTIVE_QUESTION_BANK_12,
    LOCALIZED_OBJECTIVE_QUESTION_BANK_13,
    LOCALIZED_OBJECTIVE_QUESTION_BANK_14,
)

_CONTENT_VERSIONS = (
    "1.1.0",
    "1.1.0",
    "1.1.0",
    "1.1.0",
    "1.1.0",
    "1.0.0",
    "1.1.0",
    "1.1.0",
    "1.0.0",
    "1.1.0",
    "1.1.0",
    "1.1.0",
    "1.1.0",
    "1.0.0",
)

LOCALIZED_BUNDLES = tuple(
    LocalizedModuleBundle(
        localized_module=module,
        localized_objective_question_bank=bank,
        content_version=version,
    )
    for module, bank, version in zip(
        _LOCALIZED_MODULES,
        _LOCALIZED_OBJECTIVE_BANKS,
        _CONTENT_VERSIONS,
        strict=True,
    )
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
MODULE_10_TREES = BUNDLES[9].module
MODULE_11_ADTS = BUNDLES[10].module
MODULE_12_OOP = BUNDLES[11].module
MODULE_13_SCIENTIFIC_LIBRARIES = BUNDLES[12].module
MODULE_14_TESTING_DEBUGGING_QUALITY = BUNDLES[13].module

OBJECTIVE_QUESTION_BANK = BUNDLES[0].objective_question_bank
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
OBJECTIVE_QUESTION_BANK_13 = BUNDLES[12].objective_question_bank
OBJECTIVE_QUESTION_BANK_14 = BUNDLES[13].objective_question_bank

MODULES = tuple(bundle.module for bundle in BUNDLES)
LOCALIZED_MODULES = tuple(bundle.localized_module for bundle in LOCALIZED_BUNDLES)
OBJECTIVE_QUESTION_BANKS = {
    bundle.module.module_id: bundle.objective_question_bank for bundle in BUNDLES
}

__all__ = [
    "BUNDLES",
    "DM857_BOOK_SOURCES",
    "DM857_MODULE_SOURCE_AUDIT",
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
    "LOCALIZED_MODULE_10_TREES",
    "LOCALIZED_MODULE_11_ADTS",
    "LOCALIZED_MODULE_12_OOP",
    "LOCALIZED_MODULE_13_SCIENTIFIC_LIBRARIES",
    "LOCALIZED_MODULE_14_TESTING_DEBUGGING_QUALITY",
    "LOCALIZED_OBJECTIVE_QUESTION_BANK",
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
    "LOCALIZED_OBJECTIVE_QUESTION_BANK_13",
    "LOCALIZED_OBJECTIVE_QUESTION_BANK_14",
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
    "MODULE_10_TREES",
    "MODULE_11_ADTS",
    "MODULE_12_OOP",
    "MODULE_13_SCIENTIFIC_LIBRARIES",
    "MODULE_14_TESTING_DEBUGGING_QUALITY",
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
    "OBJECTIVE_QUESTION_BANK_10",
    "OBJECTIVE_QUESTION_BANK_11",
    "OBJECTIVE_QUESTION_BANK_12",
    "OBJECTIVE_QUESTION_BANK_13",
    "OBJECTIVE_QUESTION_BANK_14",
    "apply_book_grounded_extensions",
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
    "materialize_module_13_question_bank",
    "materialize_module_14_question_bank",
    "materialize_objective_question_bank",
]
