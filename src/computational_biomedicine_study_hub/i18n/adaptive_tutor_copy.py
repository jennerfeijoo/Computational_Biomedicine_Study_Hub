"""Strict localized copy for adaptive tutor sessions."""

from __future__ import annotations

from enum import StrEnum
from string import Formatter

from .locales import AppLocale


class AdaptiveTutorCopyKey(StrEnum):
    """Stable text keys for adaptive help levels, history and feedback."""

    LEVEL_LABEL = "adaptive_tutor.level_label"
    LEVEL_SOCRATIC = "adaptive_tutor.level.socratic"
    LEVEL_CONCEPTUAL = "adaptive_tutor.level.conceptual"
    LEVEL_STRUCTURAL = "adaptive_tutor.level.structural"
    LEVEL_EXPLANATION = "adaptive_tutor.level.explanation"
    REQUEST_LEVEL = "adaptive_tutor.request_level"
    HISTORY_TITLE = "adaptive_tutor.history_title"
    TURN_TITLE = "adaptive_tutor.turn_title"
    TURN_QUESTION = "adaptive_tutor.turn_question"
    TURN_MODEL = "adaptive_tutor.turn_model"
    TURN_SOURCES = "adaptive_tutor.turn_sources"
    HELPFUL_PROMPT = "adaptive_tutor.helpful_prompt"
    HELPFUL = "adaptive_tutor.helpful"
    NOT_HELPFUL = "adaptive_tutor.not_helpful"
    RATED_HELPFUL = "adaptive_tutor.rated_helpful"
    RATED_NOT_HELPFUL = "adaptive_tutor.rated_not_helpful"
    ESCALATED = "adaptive_tutor.escalated"
    RATING_HELPFUL = "adaptive_tutor.rating.helpful"
    RATING_NOT_HELPFUL = "adaptive_tutor.rating.not_helpful"
    SESSION_NOTICE = "adaptive_tutor.session_notice"
    HINT_QUESTION_SOCRATIC = "adaptive_tutor.hint_question.socratic"
    HINT_QUESTION_CONCEPTUAL = "adaptive_tutor.hint_question.conceptual"
    HINT_QUESTION_STRUCTURAL = "adaptive_tutor.hint_question.structural"
    HINT_QUESTION_EXPLANATION = "adaptive_tutor.hint_question.explanation"


_CATALOGS: dict[AppLocale, dict[AdaptiveTutorCopyKey, str]] = {
    AppLocale.SPANISH_SPAIN: {
        AdaptiveTutorCopyKey.LEVEL_LABEL: "Nivel de ayuda",
        AdaptiveTutorCopyKey.LEVEL_SOCRATIC: "Pregunta socrática",
        AdaptiveTutorCopyKey.LEVEL_CONCEPTUAL: "Pista conceptual",
        AdaptiveTutorCopyKey.LEVEL_STRUCTURAL: "Pista estructural",
        AdaptiveTutorCopyKey.LEVEL_EXPLANATION: "Explicación completa",
        AdaptiveTutorCopyKey.REQUEST_LEVEL: "Solicitar este nivel",
        AdaptiveTutorCopyKey.HISTORY_TITLE: "Historial de esta sesión",
        AdaptiveTutorCopyKey.TURN_TITLE: "Turno {number} · {level}",
        AdaptiveTutorCopyKey.TURN_QUESTION: "Pregunta: {question}",
        AdaptiveTutorCopyKey.TURN_MODEL: "Modelo: {model}",
        AdaptiveTutorCopyKey.TURN_SOURCES: "Fuentes: {sources}",
        AdaptiveTutorCopyKey.HELPFUL_PROMPT: "¿Esta respuesta te ayudó?",
        AdaptiveTutorCopyKey.HELPFUL: "Sí, fue útil",
        AdaptiveTutorCopyKey.NOT_HELPFUL: "No fue suficiente",
        AdaptiveTutorCopyKey.RATED_HELPFUL: "Respuesta marcada como útil.",
        AdaptiveTutorCopyKey.RATED_NOT_HELPFUL: "Respuesta marcada como insuficiente.",
        AdaptiveTutorCopyKey.ESCALATED: "Se propone el siguiente nivel: {level}.",
        AdaptiveTutorCopyKey.RATING_HELPFUL: "Útil",
        AdaptiveTutorCopyKey.RATING_NOT_HELPFUL: "Insuficiente",
        AdaptiveTutorCopyKey.SESSION_NOTICE: (
            "La ayuda utilizada se registra únicamente como evidencia de apoyo para el siguiente intento."
        ),
        AdaptiveTutorCopyKey.HINT_QUESTION_SOCRATIC: (
            "Formula una pregunta socrática y una observación mínima basadas en el diagnóstico."
        ),
        AdaptiveTutorCopyKey.HINT_QUESTION_CONCEPTUAL: (
            "Dame una pista conceptual sobre la causa del fallo sin escribir la solución."
        ),
        AdaptiveTutorCopyKey.HINT_QUESTION_STRUCTURAL: (
            "Describe la estructura o los pasos que debería seguir mi código sin completarlo."
        ),
        AdaptiveTutorCopyKey.HINT_QUESTION_EXPLANATION: (
            "Explícame completamente la corrección sin revelar las pruebas ocultas."
        ),
    },
    AppLocale.ENGLISH: {
        AdaptiveTutorCopyKey.LEVEL_LABEL: "Assistance level",
        AdaptiveTutorCopyKey.LEVEL_SOCRATIC: "Socratic question",
        AdaptiveTutorCopyKey.LEVEL_CONCEPTUAL: "Conceptual hint",
        AdaptiveTutorCopyKey.LEVEL_STRUCTURAL: "Structural hint",
        AdaptiveTutorCopyKey.LEVEL_EXPLANATION: "Full explanation",
        AdaptiveTutorCopyKey.REQUEST_LEVEL: "Request this level",
        AdaptiveTutorCopyKey.HISTORY_TITLE: "History for this session",
        AdaptiveTutorCopyKey.TURN_TITLE: "Turn {number} · {level}",
        AdaptiveTutorCopyKey.TURN_QUESTION: "Question: {question}",
        AdaptiveTutorCopyKey.TURN_MODEL: "Model: {model}",
        AdaptiveTutorCopyKey.TURN_SOURCES: "Sources: {sources}",
        AdaptiveTutorCopyKey.HELPFUL_PROMPT: "Did this response help?",
        AdaptiveTutorCopyKey.HELPFUL: "Yes, it helped",
        AdaptiveTutorCopyKey.NOT_HELPFUL: "It was not enough",
        AdaptiveTutorCopyKey.RATED_HELPFUL: "The response was marked as helpful.",
        AdaptiveTutorCopyKey.RATED_NOT_HELPFUL: "The response was marked as insufficient.",
        AdaptiveTutorCopyKey.ESCALATED: "The next suggested level is {level}.",
        AdaptiveTutorCopyKey.RATING_HELPFUL: "Helpful",
        AdaptiveTutorCopyKey.RATING_NOT_HELPFUL: "Insufficient",
        AdaptiveTutorCopyKey.SESSION_NOTICE: (
            "Assistance used is recorded only as support evidence for the next attempt."
        ),
        AdaptiveTutorCopyKey.HINT_QUESTION_SOCRATIC: (
            "Provide one Socratic question and one minimal observation based on the diagnostic."
        ),
        AdaptiveTutorCopyKey.HINT_QUESTION_CONCEPTUAL: (
            "Give me a conceptual hint about the failure without writing the solution."
        ),
        AdaptiveTutorCopyKey.HINT_QUESTION_STRUCTURAL: (
            "Describe the structure or steps my code should follow without completing it."
        ),
        AdaptiveTutorCopyKey.HINT_QUESTION_EXPLANATION: (
            "Explain the correction fully without revealing hidden tests."
        ),
    },
    AppLocale.DANISH_DENMARK: {
        AdaptiveTutorCopyKey.LEVEL_LABEL: "Hjælpeniveau",
        AdaptiveTutorCopyKey.LEVEL_SOCRATIC: "Sokratisk spørgsmål",
        AdaptiveTutorCopyKey.LEVEL_CONCEPTUAL: "Begrebsmæssigt hint",
        AdaptiveTutorCopyKey.LEVEL_STRUCTURAL: "Strukturelt hint",
        AdaptiveTutorCopyKey.LEVEL_EXPLANATION: "Fuld forklaring",
        AdaptiveTutorCopyKey.REQUEST_LEVEL: "Anmod om dette niveau",
        AdaptiveTutorCopyKey.HISTORY_TITLE: "Historik for denne session",
        AdaptiveTutorCopyKey.TURN_TITLE: "Runde {number} · {level}",
        AdaptiveTutorCopyKey.TURN_QUESTION: "Spørgsmål: {question}",
        AdaptiveTutorCopyKey.TURN_MODEL: "Model: {model}",
        AdaptiveTutorCopyKey.TURN_SOURCES: "Kilder: {sources}",
        AdaptiveTutorCopyKey.HELPFUL_PROMPT: "Hjalp dette svar?",
        AdaptiveTutorCopyKey.HELPFUL: "Ja, det hjalp",
        AdaptiveTutorCopyKey.NOT_HELPFUL: "Det var ikke nok",
        AdaptiveTutorCopyKey.RATED_HELPFUL: "Svaret blev markeret som nyttigt.",
        AdaptiveTutorCopyKey.RATED_NOT_HELPFUL: "Svaret blev markeret som utilstrækkeligt.",
        AdaptiveTutorCopyKey.ESCALATED: "Det næste foreslåede niveau er {level}.",
        AdaptiveTutorCopyKey.RATING_HELPFUL: "Nyttigt",
        AdaptiveTutorCopyKey.RATING_NOT_HELPFUL: "Utilstrækkeligt",
        AdaptiveTutorCopyKey.SESSION_NOTICE: (
            "Den anvendte hjælp registreres kun som støttebevis for det næste forsøg."
        ),
        AdaptiveTutorCopyKey.HINT_QUESTION_SOCRATIC: (
            "Giv ét sokratisk spørgsmål og én minimal observation baseret på diagnosen."
        ),
        AdaptiveTutorCopyKey.HINT_QUESTION_CONCEPTUAL: (
            "Giv mig et begrebsmæssigt hint om fejlen uden at skrive løsningen."
        ),
        AdaptiveTutorCopyKey.HINT_QUESTION_STRUCTURAL: (
            "Beskriv strukturen eller trinene i min kode uden at færdiggøre den."
        ),
        AdaptiveTutorCopyKey.HINT_QUESTION_EXPLANATION: (
            "Forklar rettelsen fuldt ud uden at afsløre skjulte test."
        ),
    },
}


def adaptive_tutor_text(
    locale: AppLocale | str,
    key: AdaptiveTutorCopyKey,
    **values: object,
) -> str:
    """Return one localized adaptive-tutor string with strict placeholders."""

    resolved = locale if isinstance(locale, AppLocale) else AppLocale.resolve(locale)
    template = _CATALOGS[resolved][key]
    required = {
        field_name for _, field_name, _, _ in Formatter().parse(template) if field_name is not None
    }
    if required != set(values):
        raise ValueError(
            f"Adaptive tutor copy {key.value!r} requires {sorted(required)}; "
            f"received {sorted(values)}."
        )
    return template.format(**values)


def validate_adaptive_tutor_copy() -> None:
    """Reject missing keys or placeholder drift across supported languages."""

    expected_keys = set(AdaptiveTutorCopyKey)
    expected_placeholders: dict[AdaptiveTutorCopyKey, set[str]] | None = None
    for locale, catalog in _CATALOGS.items():
        if set(catalog) != expected_keys:
            raise ValueError(f"Incomplete adaptive tutor copy for {locale.value}.")
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
            raise ValueError(f"Adaptive tutor placeholders differ for locale {locale.value}.")


validate_adaptive_tutor_copy()

__all__ = [
    "AdaptiveTutorCopyKey",
    "adaptive_tutor_text",
    "validate_adaptive_tutor_copy",
]
