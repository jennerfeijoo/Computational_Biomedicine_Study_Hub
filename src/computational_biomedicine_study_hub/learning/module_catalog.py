"""Runtime catalog used by AI study features.

The catalog deliberately consumes the same authored ``LearningModule`` objects used by
course pages. AI features therefore receive authored material rather than a second,
unsynchronised curriculum copy.
"""

from __future__ import annotations

from functools import lru_cache

from ..content.models import LearningModule
from ..i18n import AppLocale
from ..content import bmb830, bmb831, dm847, dm857

_COURSE_MODULES = {
    "DM857": dm857.LOCALIZED_BUNDLES,
    "DM847": dm847.LOCALIZED_BUNDLES,
    "BMB830": bmb830.LOCALIZED_BUNDLES,
    "BMB831": bmb831.LOCALIZED_BUNDLES,
}


@lru_cache(maxsize=3)
def modules_for_locale(locale: AppLocale) -> tuple[LearningModule, ...]:
    """Materialize every first-semester module for one UI locale."""

    modules: list[LearningModule] = []
    for course_code in ("DM857", "DM847", "BMB830", "BMB831"):
        modules.extend(bundle.materialize(locale).module for bundle in _COURSE_MODULES[course_code])
    return tuple(modules)


def module_by_id(course_code: str, module_id: str, locale: AppLocale) -> LearningModule:
    """Resolve one authored module or raise a clear lookup error."""

    normalized_course = course_code.strip().upper()
    for module in modules_for_locale(locale):
        if module.course_code == normalized_course and module.module_id == module_id:
            return module
    raise KeyError(f"Unknown authored module: {normalized_course}/{module_id}")


def modules_for_course(course_code: str, locale: AppLocale) -> tuple[LearningModule, ...]:
    """Return all authored modules for one first-semester course."""

    normalized = course_code.strip().upper()
    return tuple(module for module in modules_for_locale(locale) if module.course_code == normalized)


__all__ = ["module_by_id", "modules_for_course", "modules_for_locale"]
