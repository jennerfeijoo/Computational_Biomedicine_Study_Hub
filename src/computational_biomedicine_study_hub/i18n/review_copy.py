"""Strict localized copy for spaced review and the error notebook."""

from __future__ import annotations

from enum import StrEnum
from string import Formatter

from .locales import AppLocale


class ReviewCopyKey(StrEnum):
    """Stable text keys used by the review system."""

    TITLE = "review.title"
    INTRO = "review.intro"
    QUEUE_TAB = "review.queue_tab"
    ERROR_TAB = "review.error_tab"
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

    ERROR_COUNT = "error.count"
    ERROR_EMPTY_TITLE = "error.empty_title"
    ERROR_EMPTY_BODY = "error.empty_body"
    ERROR_STATUS_OPEN = "error.status_open"
    ERROR_STATUS_RESOLVED = "error.status_resolved"
    ERROR_KIND_KNOWLEDGE_GAP = "error.kind_knowledge_gap"
    ERROR_KIND_FRAGILE = "error.kind_fragile"
    ERROR_KIND_MISCONCEPTION = "error.kind_misconception"
    ERROR_PROMPT = "error.prompt"
    ERROR_SELECTED = "error.selected"
    ERROR_CORRECT = "error.correct"
    ERROR_EXPLANATION = "error.explanation"
    ERROR_CONFIDENCE = "error.confidence"
    ERROR_OCCURRED = "error.occurred"
    ERROR_RESOLVED = "error.resolved"
    ERROR_OBJECTIVES = "error.objectives"
    CONFIDENCE_LOW = "confidence.low"
    CONFIDENCE_MEDIUM = "confidence.medium"
    CONFIDENCE_HIGH = "confidence.high"


_CATALOGS: dict[AppLocale, dict[ReviewCopyKey, str]] = {
    AppLocale.SPANISH_SPAIN: {
        ReviewCopyKey.TITLE: "Sistema de repaso",
        ReviewCopyKey.INTRO: (
            "La cola programa recuperación activa; el cuaderno conserva errores auténticos, "
            "su explicación y el estado de corrección posterior."
        ),
        ReviewCopyKey.QUEUE_TAB: "Repaso programado",
        ReviewCopyKey.ERROR_TAB: "Cuaderno de errores",
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
        ReviewCopyKey.ERROR_COUNT: "{open_count} abiertos · {total_count} registrados",
        ReviewCopyKey.ERROR_EMPTY_TITLE: "Todavía no hay errores registrados",
        ReviewCopyKey.ERROR_EMPTY_BODY: (
            "Las respuestas incorrectas con contexto académico aparecerán aquí automáticamente."
        ),
        ReviewCopyKey.ERROR_STATUS_OPEN: "Pendiente de corregir",
        ReviewCopyKey.ERROR_STATUS_RESOLVED: "Corregido posteriormente",
        ReviewCopyKey.ERROR_KIND_KNOWLEDGE_GAP: "Vacío de conocimiento o incertidumbre",
        ReviewCopyKey.ERROR_KIND_FRAGILE: "Comprensión frágil",
        ReviewCopyKey.ERROR_KIND_MISCONCEPTION: "Posible concepción errónea",
        ReviewCopyKey.ERROR_PROMPT: "Pregunta: {text}",
        ReviewCopyKey.ERROR_SELECTED: "Tu respuesta: {text}",
        ReviewCopyKey.ERROR_CORRECT: "Respuesta correcta: {text}",
        ReviewCopyKey.ERROR_EXPLANATION: "Explicación: {text}",
        ReviewCopyKey.ERROR_CONFIDENCE: "Confianza previa: {level}",
        ReviewCopyKey.ERROR_OCCURRED: "Registrado: {date}",
        ReviewCopyKey.ERROR_RESOLVED: "Corregido: {date}",
        ReviewCopyKey.ERROR_OBJECTIVES: "Objetivos: {objectives}",
        ReviewCopyKey.CONFIDENCE_LOW: "baja",
        ReviewCopyKey.CONFIDENCE_MEDIUM: "media",
        ReviewCopyKey.CONFIDENCE_HIGH: "alta",
    },
    AppLocale.ENGLISH: {
        ReviewCopyKey.TITLE: "Review system",
        ReviewCopyKey.INTRO: (
            "The queue schedules active retrieval; the notebook retains authentic errors, "
            "their explanation and whether later performance corrected them."
        ),
        ReviewCopyKey.QUEUE_TAB: "Scheduled review",
        ReviewCopyKey.ERROR_TAB: "Error notebook",
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
        ReviewCopyKey.ERROR_COUNT: "{open_count} open · {total_count} recorded",
        ReviewCopyKey.ERROR_EMPTY_TITLE: "No errors have been recorded yet",
        ReviewCopyKey.ERROR_EMPTY_BODY: (
            "Incorrect answers with authored academic context will appear here automatically."
        ),
        ReviewCopyKey.ERROR_STATUS_OPEN: "Needs correction",
        ReviewCopyKey.ERROR_STATUS_RESOLVED: "Corrected later",
        ReviewCopyKey.ERROR_KIND_KNOWLEDGE_GAP: "Knowledge gap or uncertainty",
        ReviewCopyKey.ERROR_KIND_FRAGILE: "Fragile understanding",
        ReviewCopyKey.ERROR_KIND_MISCONCEPTION: "Possible misconception",
        ReviewCopyKey.ERROR_PROMPT: "Question: {text}",
        ReviewCopyKey.ERROR_SELECTED: "Your answer: {text}",
        ReviewCopyKey.ERROR_CORRECT: "Correct answer: {text}",
        ReviewCopyKey.ERROR_EXPLANATION: "Explanation: {text}",
        ReviewCopyKey.ERROR_CONFIDENCE: "Prior confidence: {level}",
        ReviewCopyKey.ERROR_OCCURRED: "Recorded: {date}",
        ReviewCopyKey.ERROR_RESOLVED: "Corrected: {date}",
        ReviewCopyKey.ERROR_OBJECTIVES: "Objectives: {objectives}",
        ReviewCopyKey.CONFIDENCE_LOW: "low",
        ReviewCopyKey.CONFIDENCE_MEDIUM: "medium",
        ReviewCopyKey.CONFIDENCE_HIGH: "high",
    },
    AppLocale.DANISH_DENMARK: {
        ReviewCopyKey.TITLE: "Repetitionssystem",
        ReviewCopyKey.INTRO: (
            "Køen planlægger aktiv genkaldelse; fejlloggen bevarer autentiske fejl, "
            "forklaringen og om senere præstation rettede dem."
        ),
        ReviewCopyKey.QUEUE_TAB: "Planlagt repetition",
        ReviewCopyKey.ERROR_TAB: "Fejllog",
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
        ReviewCopyKey.ERROR_COUNT: "{open_count} åbne · {total_count} registrerede",
        ReviewCopyKey.ERROR_EMPTY_TITLE: "Der er endnu ingen registrerede fejl",
        ReviewCopyKey.ERROR_EMPTY_BODY: (
            "Forkerte svar med faglig kontekst vises automatisk her."
        ),
        ReviewCopyKey.ERROR_STATUS_OPEN: "Skal rettes",
        ReviewCopyKey.ERROR_STATUS_RESOLVED: "Rettet senere",
        ReviewCopyKey.ERROR_KIND_KNOWLEDGE_GAP: "Videnshul eller usikkerhed",
        ReviewCopyKey.ERROR_KIND_FRAGILE: "Skrøbelig forståelse",
        ReviewCopyKey.ERROR_KIND_MISCONCEPTION: "Mulig misforståelse",
        ReviewCopyKey.ERROR_PROMPT: "Spørgsmål: {text}",
        ReviewCopyKey.ERROR_SELECTED: "Dit svar: {text}",
        ReviewCopyKey.ERROR_CORRECT: "Korrekt svar: {text}",
        ReviewCopyKey.ERROR_EXPLANATION: "Forklaring: {text}",
        ReviewCopyKey.ERROR_CONFIDENCE: "Forudgående sikkerhed: {level}",
        ReviewCopyKey.ERROR_OCCURRED: "Registreret: {date}",
        ReviewCopyKey.ERROR_RESOLVED: "Rettet: {date}",
        ReviewCopyKey.ERROR_OBJECTIVES: "Læringsmål: {objectives}",
        ReviewCopyKey.CONFIDENCE_LOW: "lav",
        ReviewCopyKey.CONFIDENCE_MEDIUM: "middel",
        ReviewCopyKey.CONFIDENCE_HIGH: "høj",
    },
}


def review_text(
    locale: AppLocale | str,
    key: ReviewCopyKey,
    **values: object,
) -> str:
    """Return one localized review-system string with strict placeholders."""

    resolved = locale if isinstance(locale, AppLocale) else AppLocale.resolve(locale)
    template = _CATALOGS[resolved][key]
    required = {
        field_name for _, field_name, _, _ in Formatter().parse(template) if field_name is not None
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
