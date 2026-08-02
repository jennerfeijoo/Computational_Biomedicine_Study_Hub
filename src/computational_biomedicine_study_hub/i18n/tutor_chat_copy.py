"""Strict localized copy for the application-wide contextual tutor chat."""

from __future__ import annotations

from enum import StrEnum
from string import Formatter

from .locales import AppLocale


class TutorChatCopyKey(StrEnum):
    """Stable text keys used by the floating tutor chat."""

    OPEN = "tutor_chat.open"
    TITLE = "tutor_chat.title"
    CONTEXT = "tutor_chat.context"
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


_CATALOGS: dict[AppLocale, dict[TutorChatCopyKey, str]] = {
    AppLocale.SPANISH_SPAIN: {
        TutorChatCopyKey.OPEN: "Tutor",
        TutorChatCopyKey.TITLE: "Tutor de estudio",
        TutorChatCopyKey.CONTEXT: "Contexto actual: {context}",
        TutorChatCopyKey.PLACEHOLDER: "Pregunta cualquier duda sobre el tema actual…",
        TutorChatCopyKey.SEND: "Enviar",
        TutorChatCopyKey.RESET: "Reiniciar conversación",
        TutorChatCopyKey.MINIMIZE: "Minimizar",
        TutorChatCopyKey.RESTORE: "Restaurar",
        TutorChatCopyKey.CLOSE: "Cerrar",
        TutorChatCopyKey.THINKING: "Ollama está preparando una respuesta…",
        TutorChatCopyKey.EMPTY: "Escribe una pregunta antes de enviarla.",
        TutorChatCopyKey.ERROR: "No se pudo obtener una respuesta: {detail}",
        TutorChatCopyKey.EXPLAIN_SELECTION: "Pedir explicación al tutor",
        TutorChatCopyKey.SELECTION_PROMPT: (
            "Explica con claridad el siguiente texto seleccionado y relaciónalo con el contexto "
            "actual. Señala cualquier supuesto o limitación importante:\n\n{selection}"
        ),
    },
    AppLocale.ENGLISH: {
        TutorChatCopyKey.OPEN: "Tutor",
        TutorChatCopyKey.TITLE: "Study tutor",
        TutorChatCopyKey.CONTEXT: "Current context: {context}",
        TutorChatCopyKey.PLACEHOLDER: "Ask any question about the current topic…",
        TutorChatCopyKey.SEND: "Send",
        TutorChatCopyKey.RESET: "Reset conversation",
        TutorChatCopyKey.MINIMIZE: "Minimize",
        TutorChatCopyKey.RESTORE: "Restore",
        TutorChatCopyKey.CLOSE: "Close",
        TutorChatCopyKey.THINKING: "Ollama is preparing a response…",
        TutorChatCopyKey.EMPTY: "Write a question before sending it.",
        TutorChatCopyKey.ERROR: "A response could not be obtained: {detail}",
        TutorChatCopyKey.EXPLAIN_SELECTION: "Ask the tutor to explain",
        TutorChatCopyKey.SELECTION_PROMPT: (
            "Explain the following selected text clearly and connect it to the current context. "
            "State any important assumptions or limitations:\n\n{selection}"
        ),
    },
    AppLocale.DANISH_DENMARK: {
        TutorChatCopyKey.OPEN: "Tutor",
        TutorChatCopyKey.TITLE: "Studietutor",
        TutorChatCopyKey.CONTEXT: "Aktuel kontekst: {context}",
        TutorChatCopyKey.PLACEHOLDER: "Stil et spørgsmål om det aktuelle emne…",
        TutorChatCopyKey.SEND: "Send",
        TutorChatCopyKey.RESET: "Nulstil samtalen",
        TutorChatCopyKey.MINIMIZE: "Minimér",
        TutorChatCopyKey.RESTORE: "Gendan",
        TutorChatCopyKey.CLOSE: "Luk",
        TutorChatCopyKey.THINKING: "Ollama forbereder et svar…",
        TutorChatCopyKey.EMPTY: "Skriv et spørgsmål, før du sender det.",
        TutorChatCopyKey.ERROR: "Der kunne ikke hentes et svar: {detail}",
        TutorChatCopyKey.EXPLAIN_SELECTION: "Bed tutoren om en forklaring",
        TutorChatCopyKey.SELECTION_PROMPT: (
            "Forklar den følgende markerede tekst tydeligt, og forbind den med den aktuelle "
            "kontekst. Angiv vigtige antagelser eller begrænsninger:\n\n{selection}"
        ),
    },
}


def tutor_chat_text(
    locale: AppLocale | str,
    key: TutorChatCopyKey,
    **values: object,
) -> str:
    """Return one localized tutor-chat string with strict placeholders."""

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
