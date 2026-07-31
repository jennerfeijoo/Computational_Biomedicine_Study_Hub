"""Localized lookup of authored objectives for review and analytics surfaces."""

from __future__ import annotations

from dataclasses import dataclass
from functools import lru_cache

from ..content.dm847 import LOCALIZED_BUNDLES as DM847_LOCALIZED_BUNDLES
from ..content.dm857 import LOCALIZED_BUNDLES as DM857_LOCALIZED_BUNDLES
from ..i18n.locales import AppLocale

ObjectiveCatalogKey = tuple[str, str, str]


@dataclass(frozen=True, slots=True)
class ObjectiveDescriptor:
    """Localized metadata for one stable course-module-objective identity."""

    course_code: str
    module_id: str
    module_title: str
    objective_id: str
    statement: str

    @property
    def key(self) -> ObjectiveCatalogKey:
        """Return the stable composite identity used by persistence."""

        return self.course_code, self.module_id, self.objective_id


@lru_cache(maxsize=len(AppLocale))
def authored_objective_catalog(
    locale: AppLocale,
) -> dict[ObjectiveCatalogKey, ObjectiveDescriptor]:
    """Build a localized catalog without inferring or rewriting authored objectives."""

    catalog: dict[ObjectiveCatalogKey, ObjectiveDescriptor] = {}
    for localized_bundle in (*DM847_LOCALIZED_BUNDLES, *DM857_LOCALIZED_BUNDLES):
        module = localized_bundle.materialize(locale).module
        for objective in module.objectives:
            descriptor = ObjectiveDescriptor(
                course_code=module.course_code,
                module_id=module.module_id,
                module_title=module.title,
                objective_id=objective.objective_id,
                statement=objective.statement,
            )
            if descriptor.key in catalog:
                raise ValueError(f"Duplicate authored objective identity: {descriptor.key!r}")
            catalog[descriptor.key] = descriptor
    return catalog


def objective_descriptor(
    course_code: str,
    module_id: str,
    objective_id: str,
    locale: AppLocale | str,
) -> ObjectiveDescriptor | None:
    """Resolve localized metadata for one persisted objective, when authored."""

    resolved = locale if isinstance(locale, AppLocale) else AppLocale.resolve(locale)
    return authored_objective_catalog(resolved).get((course_code, module_id, objective_id))


__all__ = [
    "ObjectiveCatalogKey",
    "ObjectiveDescriptor",
    "authored_objective_catalog",
    "objective_descriptor",
]
