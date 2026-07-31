"""Strict localized copy for the spaced-review dashboard."""

from __future__ import annotations

from enum import StrEnum
from string import Formatter

from .locales import AppLocale


class ReviewCopyKey(StrEnum):
    """Stable text keys used by the review queue."""

    TITLE = "review.title"
    INTRO = "review.intro"
    DUE_COUNT = "review.due_count"
    EMPTY_TITLE = "review.empty_title"
    EMPTY_BODY = "review.empty_body"
    REFRESH = "review.refresh"
    OPEN_MODULE = "review.open_module"
    MODULE_LINE = "review.module_line"
    MASTERY = "review.mastery"
    ATTEMPTS = "review.attempts"
    LAPSES = "review.lapses"
    DUE = "review.due"
    PRIORITY_HIGH = "review.priority_high"
    PRIORITY_MEDIUM = "review.priority_medium"
    PRIORITY_LOW = "review.priority_low"


_CATALOGS: dict[AppLocale, dict[ReviewCopyKey, str]] = {
    AppLocale.SPANISH_SPAIN: {
        ReviewCopyKey.TITLE: "Repaso programado",
        ReviewCopyKey.INTRO: (
            "La cola prioriza objetivos vencidos, dominio débil y lapsos recientes. "
            "Cada respuesta actualiza automáticamente la siguiente fecha de recuperación."
        ),
        ReviewCopyKey.DUE_COUNT: "{count} objetivos pendientes",
        ReviewCopyKey.EMPTY_TITLE: "No hay repasos pendientes",
        ReviewCopyKey.EMPTY_BODY: (
            "Completa evaluaciones con seguimiento para generar una cola de repetición espaciada."
        ),
        ReviewCopyKey.REFRESH: "Actualizar",
        ReviewCopyKey.OPEN_MODULE: "Repasar ahora",
        ReviewCopyKey.MODULE_LINE: "{course_code} · {module_title}",
        ReviewCopyKey.MASTERY: "Dominio estimado: {percent}%",
        ReviewCopyKey.ATTEMPTS: "{count} intentos",
        ReviewCopyKey.LAPSES: "{count} lapsos",
        ReviewCopyKey.DUE: "Programado: {date}",
        ReviewCopyKey.PRIORITY_HIGH: "Prioridad alta",
        ReviewCopyKey.PRIORITY_MEDIUM: "Prioridad media",
        ReviewCopyKey.PRIORITY_LOW: "Prioridad baja",
    },
    AppLocale.ENGLISH: {
        ReviewCopyKey.TITLE: "Scheduled review",
        ReviewCopyKey.INTRO: (
            "The queue prioritizes overdue objectives, weak mastery and recent lapses. "
            "Every answer automatically updates the next retrieval date."
        ),
        ReviewCopyKey.DUE_COUNT: "{count} objectives due",
        ReviewCopyKey.EMPTY_TITLE: "No reviews are due",
        ReviewCopyKey.EMPTY_BODY: (
            "Complete tracked assessments to generate a spaced-repetition queue."
        ),
        ReviewCopyKey.REFRESH: "Refresh",
        ReviewCopyKey.OPEN_MODULE: "Review now",
        ReviewCopyKey.MODULE_LINE: "{course_code} · {module_title}",
        ReviewCopyKey.MASTERY: "Estimated mastery: {percent}%",
        ReviewCopyKey.ATTEMPTS: "{count} attempts",
        ReviewCopyKey.LAPSES: "{count} lapses",
        ReviewCopyKey.DUE: "Scheduled: {date}",
        ReviewCopyKey.PRIORITY_HIGH: "High priority",
        ReviewCopyKey.PRIORITY_MEDIUM: "Medium priority",
        ReviewCopyKey.PRIORITY_LOW: "Low priority",
    },
    AppLocale.DANISH_DENMARK: {
        ReviewCopyKey.TITLE: "Planlagt repetition",
        ReviewCopyKey.INTRO: (
            "Køen prioriterer forfaldne læringsmål, svag mestring og nylige fejl. "
            "Hvert svar opdaterer automatisk næste genkaldelsestidspunkt."
        ),
        ReviewCopyKey.DUE_COUNT: "{count} læringsmål skal repeteres",
        ReviewCopyKey.EMPTY_TITLE: "Ingen repetition er forfalden",
        ReviewCopyKey.EMPTY_BODY: (
            "Gennemfør evalueringer med registrering for at opbygge en tidsfordelt repetitionskø."
        ),
        ReviewCopyKey.REFRESH: "Opdater",
        ReviewCopyKey.OPEN_MODULE: "Repeter nu",
        ReviewCopyKey.MODULE_LINE: "{course_code} · {module_title}",
        ReviewCopyKey.MASTERY: "Estimeret mestring: {percent}%",
        ReviewCopyKey.ATTEMPTS: "{count} forsøg",
        ReviewCopyKey.LAPSES: "{count} fejlperioder",
        ReviewCopyKey.DUE: "Planlagt: {date}",
        ReviewCopyKey.PRIORITY_HIGH: "Høj prioritet",
        ReviewCopyKey.PRIORITY_MEDIUM: "Mellem prioritet",
        ReviewCopyKey.PRIORITY_LOW: "Lav prioritet",
    },
}


def review_text(
    locale: AppLocale | str,
    key: ReviewCopyKey,
    **values: object,
) -> str:
    """Return one localized dashboard string with strict placeholders."""

    resolved = locale if isinstance(locale, AppLocale) else AppLocale.resolve(locale)
    template = _CATALOGS[resolved][key]
    required = {
        field_name
        for _, field_name, _, _ in Formatter().parse(template)
        if field_name is not None
    }
    provided = set(values)
    if required != provided:
        raise ValueError(
            f"Review copy {key.value!r} requires placeholders {sorted(required)}; "
            f"received {sorted(provided)}."
        )
    return template.format(**values)


def validate_review_copy() -> None:
    """Reject missing keys or placeholder drift across languages."""

    expected_keys = set(ReviewCopyKey)
    expected_placeholders: dict[ReviewCopyKey, set[str]] | None = None
    for locale, catalog in _CATALOGS.items():
        if set(catalog) != expected_keys:
            missing = expected_keys - set(catalog)
            extra = set(catalog) - expected_keys
            raise ValueError(
                f"Incomplete review copy for {locale.value}: missing={sorted(missing)}, "
                f"extra={sorted(extra)}"
            )
        placeholders = {
            key: {
                field_name
                for _, field_name, _, _ in Formatter().parse(template)
                if field_name is not None
            }
            for key, template in catalog.items()
        }
        if expected_placeholders is None:
            expected_placeholders = placeholders
        elif placeholders != expected_placeholders:
            raise ValueError(f"Review placeholders differ for locale {locale.value}.")


validate_review_copy()

__all__ = ["ReviewCopyKey", "review_text", "validate_review_copy"]
