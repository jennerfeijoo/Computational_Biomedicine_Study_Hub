"""Spanish runtime and complete trilingual authored content for DM857."""

from __future__ import annotations

from .module_01_es import MODULE as MODULE_01_FOUNDATIONS
from .module_01_localized import LOCALIZED_MODULE as LOCALIZED_MODULE_01_FOUNDATIONS
from .module_01_objective_bank import OBJECTIVE_QUESTION_BANK
from .module_01_objective_bank_localized import (
    LOCALIZED_OBJECTIVE_QUESTION_BANK,
    materialize_objective_question_bank,
)
from .module_02_conditionals import (
    LOCALIZED_MODULE_02_CONDITIONALS,
    MODULE_02_CONDITIONALS,
)
from .module_02_objective_bank import (
    LOCALIZED_OBJECTIVE_QUESTION_BANK_02,
    OBJECTIVE_QUESTION_BANK_02,
    materialize_module_02_question_bank,
)
from .module_03_iteration import (
    LOCALIZED_MODULE_03_ITERATION,
    MODULE_03_ITERATION,
)
from .module_03_objective_bank import (
    LOCALIZED_OBJECTIVE_QUESTION_BANK_03,
    OBJECTIVE_QUESTION_BANK_03,
    materialize_module_03_question_bank,
)

MODULES = (
    MODULE_01_FOUNDATIONS,
    MODULE_02_CONDITIONALS,
    MODULE_03_ITERATION,
)
LOCALIZED_MODULES = (
    LOCALIZED_MODULE_01_FOUNDATIONS,
    LOCALIZED_MODULE_02_CONDITIONALS,
    LOCALIZED_MODULE_03_ITERATION,
)
OBJECTIVE_QUESTION_BANKS = {
    MODULE_01_FOUNDATIONS.module_id: OBJECTIVE_QUESTION_BANK,
    MODULE_02_CONDITIONALS.module_id: OBJECTIVE_QUESTION_BANK_02,
    MODULE_03_ITERATION.module_id: OBJECTIVE_QUESTION_BANK_03,
}

__all__ = [
    "LOCALIZED_MODULES",
    "LOCALIZED_MODULE_01_FOUNDATIONS",
    "LOCALIZED_MODULE_02_CONDITIONALS",
    "LOCALIZED_MODULE_03_ITERATION",
    "LOCALIZED_OBJECTIVE_QUESTION_BANK",
    "LOCALIZED_OBJECTIVE_QUESTION_BANK_02",
    "LOCALIZED_OBJECTIVE_QUESTION_BANK_03",
    "MODULES",
    "MODULE_01_FOUNDATIONS",
    "MODULE_02_CONDITIONALS",
    "MODULE_03_ITERATION",
    "OBJECTIVE_QUESTION_BANK",
    "OBJECTIVE_QUESTION_BANKS",
    "OBJECTIVE_QUESTION_BANK_02",
    "OBJECTIVE_QUESTION_BANK_03",
    "materialize_module_02_question_bank",
    "materialize_module_03_question_bank",
    "materialize_objective_question_bank",
]
