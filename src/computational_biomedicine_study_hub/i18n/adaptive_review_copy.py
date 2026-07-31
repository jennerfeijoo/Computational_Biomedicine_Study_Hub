"""Strict localized copy for adaptive review sessions."""

from __future__ import annotations

from enum import StrEnum
from string import Formatter

from .locales import AppLocale


class AdaptiveReviewCopyKey(StrEnum):
    """Stable labels for the adaptive review launcher and active session."""

    TAB = "adaptive_review.tab"
    TITLE = "adaptive_review.title"
    INTRO = "adaptive_review.intro"
    START = "adaptive_review.start"
    RESTART = "adaptive_review.restart"
    DUE_SUMMARY = "adaptive_review.due_summary"
    NO_DUE = "adaptive_review.no_due"
    NO_ELIGIBLE = "adaptive_review.no_eligible"
    PROGRESS = "adaptive_review.progress"
    PRIMARY_OBJECTIVE = "adaptive_review.primary_objective"
    NEXT = "adaptive_review.next"
    FINISH = "adaptive_review.finish"
    SUMMARY_TITLE = "adaptive_review.summary_title"
    SUMMARY = "adaptive_review.summary"
    EXHAUSTED = "adaptive_review.exhausted"
    COMPLETE = "adaptive_review.complete"
    RETURN_TO_QUEUE = "adaptive_review.return_to_queue"


_CATALOGS: dict[AppLocale, dict[AdaptiveReviewCopyKey, str]] = {
    AppLocale.SPANISH_SPAIN: {
        AdaptiveReviewCopyKey.TAB: "Sesión adaptativa",
        AdaptiveReviewCopyKey.TITLE: "Repaso adaptativo",
        AdaptiveReviewCopyKey.INTRO: (
            "La sesión selecciona preguntas autorizadas según debilidad, lapsos y resultados de "
            "esta sesión. Evita repetir inmediatamente el mismo objetivo."
        ),
        AdaptiveReviewCopyKey.START: "Iniciar sesión",
        AdaptiveReviewCopyKey.RESTART: "Crear otra sesión",
        AdaptiveReviewCopyKey.DUE_SUMMARY: (
            "Objetivos vencidos: {due}. Elegibles para preguntas deterministas: {eligible}. "
            "Sin banco objetivo: {unsupported}."
        ),
        AdaptiveReviewCopyKey.NO_DUE: "No hay objetivos vencidos para repasar.",
        AdaptiveReviewCopyKey.NO_ELIGIBLE: (
            "Los objetivos vencidos actuales todavía no tienen un banco de preguntas con enlaces "
            "explícitos. Permanecen disponibles en la cola de módulos."
        ),
        AdaptiveReviewCopyKey.PROGRESS: "Pregunta {current} de hasta {target} · {correct} correctas",
        AdaptiveReviewCopyKey.PRIMARY_OBJECTIVE: "Objetivo prioritario: {objective}",
        AdaptiveReviewCopyKey.NEXT: "Siguiente pregunta",
        AdaptiveReviewCopyKey.FINISH: "Ver resumen",
        AdaptiveReviewCopyKey.SUMMARY_TITLE: "Resumen de la sesión",
        AdaptiveReviewCopyKey.SUMMARY: (
            "Respuestas: {answered}. Correctas: {correct}. Precisión: {accuracy} %. "
            "Objetivos trabajados: {objectives}."
        ),
        AdaptiveReviewCopyKey.EXHAUSTED: (
            "La sesión terminó antes del objetivo previsto porque no quedaban preguntas autorizadas "
            "sin repetir."
        ),
        AdaptiveReviewCopyKey.COMPLETE: "Se alcanzó el objetivo de la sesión.",
        AdaptiveReviewCopyKey.RETURN_TO_QUEUE: "Actualizar cola de repaso",
    },
    AppLocale.ENGLISH: {
        AdaptiveReviewCopyKey.TAB: "Adaptive session",
        AdaptiveReviewCopyKey.TITLE: "Adaptive review",
        AdaptiveReviewCopyKey.INTRO: (
            "The session selects authorized questions from weakness, lapses, and results within this "
            "session. It avoids immediately repeating the same objective."
        ),
        AdaptiveReviewCopyKey.START: "Start session",
        AdaptiveReviewCopyKey.RESTART: "Create another session",
        AdaptiveReviewCopyKey.DUE_SUMMARY: (
            "Due objectives: {due}. Eligible for deterministic questions: {eligible}. "
            "Without an objective bank: {unsupported}."
        ),
        AdaptiveReviewCopyKey.NO_DUE: "No objectives are currently due for review.",
        AdaptiveReviewCopyKey.NO_ELIGIBLE: (
            "The current due objectives do not yet have a question bank with explicit links. They "
            "remain available in the module queue."
        ),
        AdaptiveReviewCopyKey.PROGRESS: "Question {current} of up to {target} · {correct} correct",
        AdaptiveReviewCopyKey.PRIMARY_OBJECTIVE: "Priority objective: {objective}",
        AdaptiveReviewCopyKey.NEXT: "Next question",
        AdaptiveReviewCopyKey.FINISH: "View summary",
        AdaptiveReviewCopyKey.SUMMARY_TITLE: "Session summary",
        AdaptiveReviewCopyKey.SUMMARY: (
            "Answers: {answered}. Correct: {correct}. Accuracy: {accuracy}%. Objectives reviewed: "
            "{objectives}."
        ),
        AdaptiveReviewCopyKey.EXHAUSTED: (
            "The session ended before its target because no unrepeated authorized questions "
            "remained."
        ),
        AdaptiveReviewCopyKey.COMPLETE: "The session target was reached.",
        AdaptiveReviewCopyKey.RETURN_TO_QUEUE: "Refresh review queue",
    },
    AppLocale.DANISH_DENMARK: {
        AdaptiveReviewCopyKey.TAB: "Adaptiv session",
        AdaptiveReviewCopyKey.TITLE: "Adaptiv repetition",
        AdaptiveReviewCopyKey.INTRO: (
            "Sessionen vælger autoriserede spørgsmål ud fra svaghed, tilbagefald og resultater i "
            "denne session. Det samme læringsmål gentages ikke umiddelbart."
        ),
        AdaptiveReviewCopyKey.START: "Start session",
        AdaptiveReviewCopyKey.RESTART: "Opret en ny session",
        AdaptiveReviewCopyKey.DUE_SUMMARY: (
            "Forfaldne læringsmål: {due}. Egnede til deterministiske spørgsmål: {eligible}. "
            "Uden objektivbank: {unsupported}."
        ),
        AdaptiveReviewCopyKey.NO_DUE: "Der er ingen læringsmål, som skal repeteres nu.",
        AdaptiveReviewCopyKey.NO_ELIGIBLE: (
            "De aktuelle forfaldne læringsmål har endnu ikke en spørgsmålsbank med eksplicitte "
            "koblinger. De er fortsat tilgængelige i modulkøen."
        ),
        AdaptiveReviewCopyKey.PROGRESS: (
            "Spørgsmål {current} af op til {target} · {correct} korrekte"
        ),
        AdaptiveReviewCopyKey.PRIMARY_OBJECTIVE: "Prioriteret læringsmål: {objective}",
        AdaptiveReviewCopyKey.NEXT: "Næste spørgsmål",
        AdaptiveReviewCopyKey.FINISH: "Se oversigt",
        AdaptiveReviewCopyKey.SUMMARY_TITLE: "Sessionsoversigt",
        AdaptiveReviewCopyKey.SUMMARY: (
            "Svar: {answered}. Korrekte: {correct}. Nøjagtighed: {accuracy} %. Bearbejdede "
            "læringsmål: {objectives}."
        ),
        AdaptiveReviewCopyKey.EXHAUSTED: (
            "Sessionen sluttede før målet, fordi der ikke var flere autoriserede spørgsmål uden "
            "gentagelse."
        ),
        AdaptiveReviewCopyKey.COMPLETE: "Sessionens mål blev nået.",
        AdaptiveReviewCopyKey.RETURN_TO_QUEUE: "Opdater repetitionskø",
    },
}


def adaptive_review_text(
    locale: AppLocale | str,
    key: AdaptiveReviewCopyKey,
    **values: object,
) -> str:
    """Return localized adaptive-review text with strict placeholder validation."""

    resolved = locale if isinstance(locale, AppLocale) else AppLocale.resolve(locale)
    template = _CATALOGS[resolved][key]
    required = {
        field_name for _, field_name, _, _ in Formatter().parse(template) if field_name is not None
    }
    if required != set(values):
        raise ValueError(
            f"Adaptive review copy {key.value!r} requires {sorted(required)}; "
            f"received {sorted(values)}."
        )
    return template.format(**values)


def validate_adaptive_review_copy() -> None:
    """Reject missing keys or placeholder drift across supported locales."""

    expected_keys = set(AdaptiveReviewCopyKey)
    expected_placeholders: dict[AdaptiveReviewCopyKey, set[str]] | None = None
    for locale, catalog in _CATALOGS.items():
        if set(catalog) != expected_keys:
            raise ValueError(f"Incomplete adaptive review copy for {locale.value}.")
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
            raise ValueError(f"Adaptive review placeholders differ for locale {locale.value}.")


validate_adaptive_review_copy()

__all__ = [
    "AdaptiveReviewCopyKey",
    "adaptive_review_text",
    "validate_adaptive_review_copy",
]
