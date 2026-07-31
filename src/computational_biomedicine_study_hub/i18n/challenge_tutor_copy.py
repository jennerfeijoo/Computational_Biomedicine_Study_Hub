"""Strict localized copy for the contextual programming tutor."""

from __future__ import annotations

from enum import StrEnum
from string import Formatter

from .locales import AppLocale


class ChallengeTutorCopyKey(StrEnum):
    """Stable text keys used by the contextual challenge tutor."""

    TITLE = "challenge_tutor.title"
    INTRO = "challenge_tutor.intro"
    WAITING = "challenge_tutor.waiting"
    READY = "challenge_tutor.ready"
    QUESTION_PLACEHOLDER = "challenge_tutor.question_placeholder"
    ASK = "challenge_tutor.ask"
    HINT = "challenge_tutor.hint"
    CANCEL = "challenge_tutor.cancel"
    RUNNING = "challenge_tutor.running"
    QUESTION_REQUIRED = "challenge_tutor.question_required"
    CANCELLED = "challenge_tutor.cancelled"
    RESPONSE_TITLE = "challenge_tutor.response_title"
    SOURCES = "challenge_tutor.sources"
    MODEL = "challenge_tutor.model"
    NON_GRADING_NOTICE = "challenge_tutor.non_grading_notice"
    ERROR_CONNECTION = "challenge_tutor.error.connection"
    ERROR_MODEL_MISSING = "challenge_tutor.error.model_missing"
    ERROR_PROTOCOL = "challenge_tutor.error.protocol"
    ERROR_GENERIC = "challenge_tutor.error.generic"
    DEFAULT_HINT_QUESTION = "challenge_tutor.default_hint_question"


_CATALOGS: dict[AppLocale, dict[ChallengeTutorCopyKey, str]] = {
    AppLocale.SPANISH_SPAIN: {
        ChallengeTutorCopyKey.TITLE: "Tutor contextual",
        ChallengeTutorCopyKey.INTRO: (
            "Pregunta sobre el último resultado verificado. El tutor puede explicar y proponer "
            "pistas, pero no puede modificar la calificación."
        ),
        ChallengeTutorCopyKey.WAITING: (
            "Ejecuta las pruebas para generar un diagnóstico verificable."
        ),
        ChallengeTutorCopyKey.READY: "Diagnóstico preparado para una consulta.",
        ChallengeTutorCopyKey.QUESTION_PLACEHOLDER: (
            "Escribe una pregunta sobre tu código, los fallos visibles o los objetivos evaluados."
        ),
        ChallengeTutorCopyKey.ASK: "Preguntar al tutor",
        ChallengeTutorCopyKey.HINT: "Pedir una pista",
        ChallengeTutorCopyKey.CANCEL: "Cancelar",
        ChallengeTutorCopyKey.RUNNING: "Ollama está generando una respuesta…",
        ChallengeTutorCopyKey.QUESTION_REQUIRED: "Escribe una pregunta antes de enviarla.",
        ChallengeTutorCopyKey.CANCELLED: "Consulta cancelada. El diagnóstico sigue disponible.",
        ChallengeTutorCopyKey.RESPONSE_TITLE: "Respuesta del tutor",
        ChallengeTutorCopyKey.SOURCES: "Fuentes académicas utilizadas",
        ChallengeTutorCopyKey.MODEL: "Modelo local: {model}",
        ChallengeTutorCopyKey.NON_GRADING_NOTICE: (
            "Esta explicación no forma parte de la evaluación. La calificación procede únicamente "
            "de las pruebas deterministas."
        ),
        ChallengeTutorCopyKey.ERROR_CONNECTION: (
            "No se pudo conectar con Ollama. Inicia el servicio local y comprueba su configuración."
        ),
        ChallengeTutorCopyKey.ERROR_MODEL_MISSING: (
            "Ollama está disponible, pero el modelo {model} no está instalado. Instálalo antes de "
            "solicitar tutoría."
        ),
        ChallengeTutorCopyKey.ERROR_PROTOCOL: (
            "Ollama respondió con datos incompletos o no válidos. Reintenta la consulta."
        ),
        ChallengeTutorCopyKey.ERROR_GENERIC: "No se pudo generar la respuesta: {detail}",
        ChallengeTutorCopyKey.DEFAULT_HINT_QUESTION: (
            "Dame una pista concreta y una pregunta socrática basadas en el diagnóstico, sin cambiar "
            "la calificación ni revelar las pruebas ocultas."
        ),
    },
    AppLocale.ENGLISH: {
        ChallengeTutorCopyKey.TITLE: "Contextual tutor",
        ChallengeTutorCopyKey.INTRO: (
            "Ask about the latest verified result. The tutor may explain and suggest hints, but it "
            "cannot change the grade."
        ),
        ChallengeTutorCopyKey.WAITING: "Run the tests to generate a verifiable diagnostic.",
        ChallengeTutorCopyKey.READY: "The diagnostic is ready for a question.",
        ChallengeTutorCopyKey.QUESTION_PLACEHOLDER: (
            "Ask about your code, visible failures, or the assessed learning objectives."
        ),
        ChallengeTutorCopyKey.ASK: "Ask the tutor",
        ChallengeTutorCopyKey.HINT: "Request a hint",
        ChallengeTutorCopyKey.CANCEL: "Cancel",
        ChallengeTutorCopyKey.RUNNING: "Ollama is generating a response…",
        ChallengeTutorCopyKey.QUESTION_REQUIRED: "Write a question before sending it.",
        ChallengeTutorCopyKey.CANCELLED: (
            "The request was cancelled. The diagnostic remains available."
        ),
        ChallengeTutorCopyKey.RESPONSE_TITLE: "Tutor response",
        ChallengeTutorCopyKey.SOURCES: "Academic sources used",
        ChallengeTutorCopyKey.MODEL: "Local model: {model}",
        ChallengeTutorCopyKey.NON_GRADING_NOTICE: (
            "This explanation is not part of the assessment. The grade comes only from the "
            "deterministic tests."
        ),
        ChallengeTutorCopyKey.ERROR_CONNECTION: (
            "Could not connect to Ollama. Start the local service and check its configuration."
        ),
        ChallengeTutorCopyKey.ERROR_MODEL_MISSING: (
            "Ollama is available, but model {model} is not installed. Install it before requesting "
            "tutoring."
        ),
        ChallengeTutorCopyKey.ERROR_PROTOCOL: (
            "Ollama returned incomplete or invalid data. Try the request again."
        ),
        ChallengeTutorCopyKey.ERROR_GENERIC: "The response could not be generated: {detail}",
        ChallengeTutorCopyKey.DEFAULT_HINT_QUESTION: (
            "Give me one concrete hint and one Socratic question based on the diagnostic, without "
            "changing the grade or revealing hidden tests."
        ),
    },
    AppLocale.DANISH_DENMARK: {
        ChallengeTutorCopyKey.TITLE: "Kontekstuel tutor",
        ChallengeTutorCopyKey.INTRO: (
            "Spørg om det seneste verificerede resultat. Tutoren kan forklare og foreslå hints, men "
            "kan ikke ændre bedømmelsen."
        ),
        ChallengeTutorCopyKey.WAITING: ("Kør testene for at oprette en verificerbar diagnose."),
        ChallengeTutorCopyKey.READY: "Diagnosen er klar til et spørgsmål.",
        ChallengeTutorCopyKey.QUESTION_PLACEHOLDER: (
            "Spørg om din kode, synlige fejl eller de vurderede læringsmål."
        ),
        ChallengeTutorCopyKey.ASK: "Spørg tutoren",
        ChallengeTutorCopyKey.HINT: "Bed om et hint",
        ChallengeTutorCopyKey.CANCEL: "Annuller",
        ChallengeTutorCopyKey.RUNNING: "Ollama genererer et svar…",
        ChallengeTutorCopyKey.QUESTION_REQUIRED: "Skriv et spørgsmål, før du sender det.",
        ChallengeTutorCopyKey.CANCELLED: (
            "Forespørgslen blev annulleret. Diagnosen er stadig tilgængelig."
        ),
        ChallengeTutorCopyKey.RESPONSE_TITLE: "Tutorens svar",
        ChallengeTutorCopyKey.SOURCES: "Anvendte akademiske kilder",
        ChallengeTutorCopyKey.MODEL: "Lokal model: {model}",
        ChallengeTutorCopyKey.NON_GRADING_NOTICE: (
            "Denne forklaring indgår ikke i vurderingen. Bedømmelsen kommer kun fra de "
            "deterministiske test."
        ),
        ChallengeTutorCopyKey.ERROR_CONNECTION: (
            "Der kunne ikke oprettes forbindelse til Ollama. Start den lokale tjeneste, og kontrollér "
            "konfigurationen."
        ),
        ChallengeTutorCopyKey.ERROR_MODEL_MISSING: (
            "Ollama er tilgængelig, men modellen {model} er ikke installeret. Installér den, før du "
            "beder om vejledning."
        ),
        ChallengeTutorCopyKey.ERROR_PROTOCOL: (
            "Ollama returnerede ufuldstændige eller ugyldige data. Prøv forespørgslen igen."
        ),
        ChallengeTutorCopyKey.ERROR_GENERIC: "Svaret kunne ikke genereres: {detail}",
        ChallengeTutorCopyKey.DEFAULT_HINT_QUESTION: (
            "Giv mig ét konkret hint og ét sokratisk spørgsmål baseret på diagnosen uden at ændre "
            "bedømmelsen eller afsløre skjulte test."
        ),
    },
}


def challenge_tutor_text(
    locale: AppLocale | str,
    key: ChallengeTutorCopyKey,
    **values: object,
) -> str:
    """Return one localized tutor string with strict placeholder validation."""

    resolved = locale if isinstance(locale, AppLocale) else AppLocale.resolve(locale)
    template = _CATALOGS[resolved][key]
    required = {
        field_name for _, field_name, _, _ in Formatter().parse(template) if field_name is not None
    }
    provided = set(values)
    if required != provided:
        raise ValueError(
            f"Challenge tutor copy {key.value!r} requires placeholders {sorted(required)}; "
            f"received {sorted(provided)}."
        )
    return template.format(**values)


def validate_challenge_tutor_copy() -> None:
    """Reject missing keys or placeholder drift across supported languages."""

    expected_keys = set(ChallengeTutorCopyKey)
    expected_placeholders: dict[ChallengeTutorCopyKey, set[str]] | None = None
    for locale, catalog in _CATALOGS.items():
        if set(catalog) != expected_keys:
            missing = expected_keys - set(catalog)
            extra = set(catalog) - expected_keys
            raise ValueError(
                f"Incomplete challenge tutor copy for {locale.value}: "
                f"missing={sorted(missing)}, extra={sorted(extra)}"
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
            raise ValueError(f"Challenge tutor placeholders differ for locale {locale.value}.")


validate_challenge_tutor_copy()

__all__ = [
    "ChallengeTutorCopyKey",
    "challenge_tutor_text",
    "validate_challenge_tutor_copy",
]
