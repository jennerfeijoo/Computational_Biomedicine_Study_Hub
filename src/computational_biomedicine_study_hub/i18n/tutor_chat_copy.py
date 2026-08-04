"""Strict localized copy for the application-wide contextual mentor chat."""

from __future__ import annotations

from enum import StrEnum
from string import Formatter

from .locales import AppLocale


class TutorChatCopyKey(StrEnum):
    """Stable text keys used by the floating mentor chat."""

    OPEN = "tutor_chat.open"
    TITLE = "tutor_chat.title"
    CONTEXT = "tutor_chat.context"
    MODE = "tutor_chat.mode"
    MODE_SOCRATIC = "tutor_chat.mode_socratic"
    MODE_EXPLAIN = "tutor_chat.mode_explain"
    MODE_PRACTICE = "tutor_chat.mode_practice"
    MODE_EVALUATE = "tutor_chat.mode_evaluate"
    MODE_PLAN = "tutor_chat.mode_plan"
    MODE_REFLECT = "tutor_chat.mode_reflect"
    PLACEHOLDER = "tutor_chat.placeholder"
    SEND = "tutor_chat.send"
    RESET = "tutor_chat.reset"
    MINIMIZE = "tutor_chat.minimize"
    RESTORE = "tutor_chat.restore"
    CLOSE = "tutor_chat.close"
    THINKING = "tutor_chat.thinking"
    EMPTY = "tutor_chat.empty"
    ERROR = "tutor_chat.error"
    EXPLAIN_SELECTION = "tutor_chat.explain_selection"
    SELECTION_PROMPT = "tutor_chat.selection_prompt"
    NOTE_TITLE = "tutor_chat.note_title"
    NOTE_DEMONSTRATED = "tutor_chat.note_demonstrated"
    NOTE_GAPS = "tutor_chat.note_gaps"
    NOTE_MISCONCEPTIONS = "tutor_chat.note_misconceptions"
    NOTE_NEXT = "tutor_chat.note_next"
    NOTE_CONFIDENCE = "tutor_chat.note_confidence"
    NOTE_DISCLAIMER = "tutor_chat.note_disclaimer"


_CATALOGS: dict[AppLocale, dict[TutorChatCopyKey, str]] = {
    AppLocale.SPANISH_SPAIN: {
        TutorChatCopyKey.OPEN: "Mentor",
        TutorChatCopyKey.TITLE: "Mentor de estudio",
        TutorChatCopyKey.CONTEXT: "Contexto actual: {context}",
        TutorChatCopyKey.MODE: "Método",
        TutorChatCopyKey.MODE_SOCRATIC: "Socrático",
        TutorChatCopyKey.MODE_EXPLAIN: "Explicar",
        TutorChatCopyKey.MODE_PRACTICE: "Practicar",
        TutorChatCopyKey.MODE_EVALUATE: "Evaluar respuesta",
        TutorChatCopyKey.MODE_PLAN: "Planificar",
        TutorChatCopyKey.MODE_REFLECT: "Reflexionar",
        TutorChatCopyKey.PLACEHOLDER: "Responde, pregunta o comparte tu razonamiento…",
        TutorChatCopyKey.SEND: "Enviar",
        TutorChatCopyKey.RESET: "Iniciar una conversación nueva",
        TutorChatCopyKey.MINIMIZE: "Minimizar",
        TutorChatCopyKey.RESTORE: "Restaurar",
        TutorChatCopyKey.CLOSE: "Cerrar",
        TutorChatCopyKey.THINKING: "Ollama está razonando y preparando la siguiente intervención…",
        TutorChatCopyKey.EMPTY: "Escribe una pregunta o respuesta antes de enviarla.",
        TutorChatCopyKey.ERROR: "No se pudo obtener una respuesta: {detail}",
        TutorChatCopyKey.EXPLAIN_SELECTION: "Trabajar este texto con el mentor",
        TutorChatCopyKey.SELECTION_PROMPT: (
            "Ayúdame a comprender el siguiente texto seleccionado y relaciónalo con el contexto "
            "actual. Comienza comprobando qué entiendo antes de dar una explicación completa:\n\n"
            "{selection}"
        ),
        TutorChatCopyKey.NOTE_TITLE: "Observación provisional del mentor",
        TutorChatCopyKey.NOTE_DEMONSTRATED: "Evidencia observada: {items}",
        TutorChatCopyKey.NOTE_GAPS: "Aspectos por aclarar: {items}",
        TutorChatCopyKey.NOTE_MISCONCEPTIONS: "Posibles errores conceptuales: {items}",
        TutorChatCopyKey.NOTE_NEXT: "Siguiente acción sugerida: {items}",
        TutorChatCopyKey.NOTE_CONFIDENCE: "Confianza de la observación: {percent}%",
        TutorChatCopyKey.NOTE_DISCLAIMER: (
            "Esta nota es una inferencia del modelo para orientar el aprendizaje; no es una nota "
            "oficial ni modifica tu dominio objetivo."
        ),
    },
    AppLocale.ENGLISH: {
        TutorChatCopyKey.OPEN: "Mentor",
        TutorChatCopyKey.TITLE: "Study mentor",
        TutorChatCopyKey.CONTEXT: "Current context: {context}",
        TutorChatCopyKey.MODE: "Method",
        TutorChatCopyKey.MODE_SOCRATIC: "Socratic",
        TutorChatCopyKey.MODE_EXPLAIN: "Explain",
        TutorChatCopyKey.MODE_PRACTICE: "Practise",
        TutorChatCopyKey.MODE_EVALUATE: "Evaluate answer",
        TutorChatCopyKey.MODE_PLAN: "Plan",
        TutorChatCopyKey.MODE_REFLECT: "Reflect",
        TutorChatCopyKey.PLACEHOLDER: "Answer, ask, or share your reasoning…",
        TutorChatCopyKey.SEND: "Send",
        TutorChatCopyKey.RESET: "Start a new conversation",
        TutorChatCopyKey.MINIMIZE: "Minimise",
        TutorChatCopyKey.RESTORE: "Restore",
        TutorChatCopyKey.CLOSE: "Close",
        TutorChatCopyKey.THINKING: "Ollama is reasoning and preparing the next intervention…",
        TutorChatCopyKey.EMPTY: "Write a question or answer before sending it.",
        TutorChatCopyKey.ERROR: "A response could not be obtained: {detail}",
        TutorChatCopyKey.EXPLAIN_SELECTION: "Work through this text with the mentor",
        TutorChatCopyKey.SELECTION_PROMPT: (
            "Help me understand the following selected text and connect it to the current context. "
            "Begin by checking what I already understand before giving a complete explanation:\n\n"
            "{selection}"
        ),
        TutorChatCopyKey.NOTE_TITLE: "Provisional mentor observation",
        TutorChatCopyKey.NOTE_DEMONSTRATED: "Observed evidence: {items}",
        TutorChatCopyKey.NOTE_GAPS: "Points to clarify: {items}",
        TutorChatCopyKey.NOTE_MISCONCEPTIONS: "Possible misconceptions: {items}",
        TutorChatCopyKey.NOTE_NEXT: "Suggested next action: {items}",
        TutorChatCopyKey.NOTE_CONFIDENCE: "Observation confidence: {percent}%",
        TutorChatCopyKey.NOTE_DISCLAIMER: (
            "This note is a model inference used to guide learning; it is not an official grade "
            "and does not change objective mastery."
        ),
    },
    AppLocale.DANISH_DENMARK: {
        TutorChatCopyKey.OPEN: "Mentor",
        TutorChatCopyKey.TITLE: "Studiementor",
        TutorChatCopyKey.CONTEXT: "Aktuel kontekst: {context}",
        TutorChatCopyKey.MODE: "Metode",
        TutorChatCopyKey.MODE_SOCRATIC: "Sokratisk",
        TutorChatCopyKey.MODE_EXPLAIN: "Forklar",
        TutorChatCopyKey.MODE_PRACTICE: "Øv",
        TutorChatCopyKey.MODE_EVALUATE: "Vurdér svar",
        TutorChatCopyKey.MODE_PLAN: "Planlæg",
        TutorChatCopyKey.MODE_REFLECT: "Reflektér",
        TutorChatCopyKey.PLACEHOLDER: "Svar, spørg eller del din ræsonnering…",
        TutorChatCopyKey.SEND: "Send",
        TutorChatCopyKey.RESET: "Start en ny samtale",
        TutorChatCopyKey.MINIMIZE: "Minimér",
        TutorChatCopyKey.RESTORE: "Gendan",
        TutorChatCopyKey.CLOSE: "Luk",
        TutorChatCopyKey.THINKING: "Ollama ræsonnerer og forbereder næste intervention…",
        TutorChatCopyKey.EMPTY: "Skriv et spørgsmål eller svar, før du sender det.",
        TutorChatCopyKey.ERROR: "Der kunne ikke hentes et svar: {detail}",
        TutorChatCopyKey.EXPLAIN_SELECTION: "Arbejd med teksten sammen med mentoren",
        TutorChatCopyKey.SELECTION_PROMPT: (
            "Hjælp mig med at forstå den følgende markerede tekst og forbind den med den aktuelle "
            "kontekst. Begynd med at undersøge, hvad jeg allerede forstår, før du giver en fuld "
            "forklaring:\n\n{selection}"
        ),
        TutorChatCopyKey.NOTE_TITLE: "Foreløbig mentorobservation",
        TutorChatCopyKey.NOTE_DEMONSTRATED: "Observeret evidens: {items}",
        TutorChatCopyKey.NOTE_GAPS: "Punkter der skal afklares: {items}",
        TutorChatCopyKey.NOTE_MISCONCEPTIONS: "Mulige misforståelser: {items}",
        TutorChatCopyKey.NOTE_NEXT: "Foreslået næste handling: {items}",
        TutorChatCopyKey.NOTE_CONFIDENCE: "Observationens sikkerhed: {percent}%",
        TutorChatCopyKey.NOTE_DISCLAIMER: (
            "Denne note er en modelbaseret inferens til læringsvejledning; den er ikke en officiel "
            "karakter og ændrer ikke objektiv mestring."
        ),
    },
}


def tutor_chat_text(
    locale: AppLocale | str,
    key: TutorChatCopyKey,
    **values: object,
) -> str:
    """Return one localized mentor-chat string with strict placeholders."""

    resolved = locale if isinstance(locale, AppLocale) else AppLocale.resolve(locale)
    template = _CATALOGS[resolved][key]
    required = {
        field_name for _, field_name, _, _ in Formatter().parse(template) if field_name is not None
    }
    provided = set(values)
    if required != provided:
        raise ValueError(
            f"Tutor chat copy {key.value!r} requires placeholders {sorted(required)}; "
            f"received {sorted(provided)}."
        )
    return template.format(**values)


def validate_tutor_chat_copy() -> None:
    """Reject missing keys or placeholder drift across supported languages."""

    expected_keys = set(TutorChatCopyKey)
    expected_placeholders: dict[TutorChatCopyKey, set[str]] | None = None
    for locale, catalog in _CATALOGS.items():
        if set(catalog) != expected_keys:
            raise ValueError(f"Incomplete tutor chat copy for {locale.value}.")
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
            raise ValueError(f"Tutor chat placeholders differ for locale {locale.value}.")


validate_tutor_chat_copy()

__all__ = ["TutorChatCopyKey", "tutor_chat_text", "validate_tutor_chat_copy"]
