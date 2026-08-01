"""BMB830 module 12: individual high-dimensional biological case."""

from __future__ import annotations

from ...i18n import AppLocale
from ..models import AssessmentItem, LearningModule
from .module_12_high_dimensional_assessment import MCQS, TRUE_FALSE, TUTOR
from .module_12_high_dimensional_r import EXAMPLES
from .module_12_high_dimensional_text import CONCEPTS, OBJECTIVES, PRACTICES, SUMMARY, TITLE
from .standard import StandardModuleSpec, build_module, build_question_bank, materialize_bank

_SPEC = StandardModuleSpec(
    module_id="bmb830.m12",
    title=TITLE,
    summary=SUMMARY,
    objectives=OBJECTIVES,
    concepts=CONCEPTS,
    examples=EXAMPLES,
    practices=PRACTICES,
    mcqs=MCQS,
    true_false=TRUE_FALSE,
    tutor=TUTOR,
)

LOCALIZED_MODULE_12_HIGH_DIMENSIONAL_CASE = build_module(_SPEC)
LOCALIZED_OBJECTIVE_QUESTION_BANK_12 = build_question_bank(_SPEC)


def materialize_module_12_question_bank(
    locale: AppLocale | str = AppLocale.SPANISH_SPAIN,
) -> tuple[AssessmentItem, ...]:
    """Materialize the stable objective bank for module 12."""

    return materialize_bank(LOCALIZED_OBJECTIVE_QUESTION_BANK_12, locale)


MODULE_12_HIGH_DIMENSIONAL_CASE: LearningModule = (
    LOCALIZED_MODULE_12_HIGH_DIMENSIONAL_CASE.materialize(AppLocale.SPANISH_SPAIN)
)
OBJECTIVE_QUESTION_BANK_12 = materialize_module_12_question_bank()

__all__ = [
    "LOCALIZED_MODULE_12_HIGH_DIMENSIONAL_CASE",
    "LOCALIZED_OBJECTIVE_QUESTION_BANK_12",
    "MODULE_12_HIGH_DIMENSIONAL_CASE",
    "OBJECTIVE_QUESTION_BANK_12",
    "materialize_module_12_question_bank",
]
