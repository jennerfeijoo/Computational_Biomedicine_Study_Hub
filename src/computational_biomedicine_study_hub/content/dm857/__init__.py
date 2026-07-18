"""Spanish runtime and complete trilingual authored content for DM857."""

from __future__ import annotations

from .module_01_es import MODULE as MODULE_01_FOUNDATIONS
from .module_01_localized import LOCALIZED_MODULE as LOCALIZED_MODULE_01_FOUNDATIONS
from .module_01_objective_bank import OBJECTIVE_QUESTION_BANK
from .module_01_objective_bank_localized import (
    LOCALIZED_OBJECTIVE_QUESTION_BANK,
    materialize_objective_question_bank,
)

MODULES = (MODULE_01_FOUNDATIONS,)

__all__ = [
    "LOCALIZED_MODULE_01_FOUNDATIONS",
    "LOCALIZED_OBJECTIVE_QUESTION_BANK",
    "MODULES",
    "MODULE_01_FOUNDATIONS",
    "OBJECTIVE_QUESTION_BANK",
    "materialize_objective_question_bank",
]
