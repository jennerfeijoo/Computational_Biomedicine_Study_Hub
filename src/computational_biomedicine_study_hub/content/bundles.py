"""Validated module-and-bank bundles for scalable course registration."""

from __future__ import annotations

from dataclasses import dataclass

from ..i18n import AppLocale
from ..learning.activity_types import ActivityType
from .localized_models import LocalizedAssessmentItem, LocalizedLearningModule
from .models import AssessmentItem, LearningModule

_OBJECTIVE_TYPES = {
    ActivityType.MULTIPLE_CHOICE,
    ActivityType.TRUE_FALSE,
}


@dataclass(frozen=True, slots=True)
class ModuleBundle:
    """One runtime module, its objective bank, and a stable content version."""

    module: LearningModule
    objective_question_bank: tuple[AssessmentItem, ...]
    content_version: str

    def __post_init__(self) -> None:
        if not self.content_version.strip():
            raise ValueError("Module bundles require a content version.")
        if not self.objective_question_bank:
            raise ValueError(f"Module {self.module.module_id!r} requires an objective bank.")

        item_ids = tuple(item.item_id for item in self.objective_question_bank)
        normalized_ids = tuple(item_id.strip().casefold() for item_id in item_ids)
        if any(not item_id for item_id in normalized_ids):
            raise ValueError("Objective bank item IDs cannot be empty.")
        if len(normalized_ids) != len(set(normalized_ids)):
            raise ValueError(
                f"Module {self.module.module_id!r} has duplicate objective-bank item IDs."
            )

        wrong_scope = tuple(
            item_id for item_id in item_ids if not item_id.startswith(f"{self.module.module_id}.")
        )
        if wrong_scope:
            raise ValueError(
                f"Module {self.module.module_id!r} has out-of-scope objective items: "
                + ", ".join(wrong_scope)
            )

        unsupported = tuple(
            item.item_id
            for item in self.objective_question_bank
            if item.activity_type not in _OBJECTIVE_TYPES
        )
        if unsupported:
            raise ValueError(
                f"Module {self.module.module_id!r} has non-objective bank items: "
                + ", ".join(unsupported)
            )


@dataclass(frozen=True, slots=True)
class LocalizedModuleBundle:
    """One complete trilingual module paired with its trilingual objective bank."""

    localized_module: LocalizedLearningModule
    localized_objective_question_bank: tuple[LocalizedAssessmentItem, ...]
    content_version: str

    def __post_init__(self) -> None:
        if not self.content_version.strip():
            raise ValueError("Localized module bundles require a content version.")
        if not self.localized_objective_question_bank:
            raise ValueError(
                f"Localized module {self.localized_module.module_id!r} requires an objective bank."
            )

        item_ids = tuple(item.item_id for item in self.localized_objective_question_bank)
        normalized_ids = tuple(item_id.strip().casefold() for item_id in item_ids)
        if any(not item_id for item_id in normalized_ids):
            raise ValueError("Localized objective bank item IDs cannot be empty.")
        if len(normalized_ids) != len(set(normalized_ids)):
            raise ValueError(
                f"Localized module {self.localized_module.module_id!r} has duplicate bank IDs."
            )

        wrong_scope = tuple(
            item_id
            for item_id in item_ids
            if not item_id.startswith(f"{self.localized_module.module_id}.")
        )
        if wrong_scope:
            raise ValueError(
                f"Localized module {self.localized_module.module_id!r} has out-of-scope items: "
                + ", ".join(wrong_scope)
            )

    def materialize(self, locale: AppLocale | str) -> ModuleBundle:
        """Materialize the module and bank together in one selected locale."""
        resolved = locale if isinstance(locale, AppLocale) else AppLocale.resolve(locale)
        return ModuleBundle(
            module=self.localized_module.materialize(resolved),
            objective_question_bank=tuple(
                item.materialize(resolved) for item in self.localized_objective_question_bank
            ),
            content_version=self.content_version,
        )


def validate_bundle_catalog(bundles: tuple[LocalizedModuleBundle, ...]) -> None:
    """Validate global uniqueness and ordering invariants for a course catalog."""
    if not bundles:
        raise ValueError("A bundle catalog cannot be empty.")

    module_ids = tuple(bundle.localized_module.module_id for bundle in bundles)
    normalized_ids = tuple(module_id.strip().casefold() for module_id in module_ids)
    if len(normalized_ids) != len(set(normalized_ids)):
        raise ValueError("A bundle catalog cannot contain duplicate module IDs.")

    course_codes = {bundle.localized_module.course_code for bundle in bundles}
    if len(course_codes) != 1:
        raise ValueError("All bundles in one catalog must belong to the same course.")


__all__ = ["LocalizedModuleBundle", "ModuleBundle", "validate_bundle_catalog"]
