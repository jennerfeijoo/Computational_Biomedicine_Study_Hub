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
    RESUME = "adaptive_review.resume"
    DISCARD = "adaptive_review.discard"
    RESUME_AVAILABLE = "adaptive_review.resume_available"
    INVALIDATED = "adaptive_review.invalidated"
    DUE_SUMMARY = "adaptive_review.due_summary"
    NO_DUE = "adaptive_review.no_due"
    NO_ELIGIBLE = "adaptive_review.no_eligible"
    PROGRESS = "adaptive_review.progress"
    PRIMARY_OBJECTIVE = "adaptive_review.primary_objective"
    ACTIVITY_TYPE = "adaptive_review.activity_type"
    QUESTION_ACTIVITY = "adaptive_review.activity.question"
    PROGRAMMING_ACTIVITY = "adaptive_review.activity.programming"
    PROGRAMMING_RETRY_NOTICE = "adaptive_review.programming_retry_notice"
    RESTORED_RESULT = "adaptive_review.restored_result"
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
            "La sesión combina preguntas y retos de programación autorizados según debilidad, "
            "lapsos y resultados de esta sesión. Evita repetir inmediatamente el mismo objetivo."
        ),
        AdaptiveReviewCopyKey.START: "Iniciar sesión",
        AdaptiveReviewCopyKey.RESTART: "Crear otra sesión",
        AdaptiveReviewCopyKey.RESUME: "Reanudar sesión",
        AdaptiveReviewCopyKey.DISCARD: "Descartar sesión guardada",
        AdaptiveReviewCopyKey.RESUME_AVAILABLE: (
            "Hay una sesión guardada: {answered} de {target} actividades aceptadas. "
            "Puedes continuar exactamente desde la actividad pendiente."
        ),
        AdaptiveReviewCopyKey.INVALIDATED: (
            "La sesión guardada se descartó porque cambió el catálogo académico o el archivo era "
            "incompatible. Tus intentos y tu dominio permanecen intactos."
        ),
        AdaptiveReviewCopyKey.DUE_SUMMARY: (
            "Objetivos vencidos: {due}. Elegibles para actividades deterministas: {eligible}. "
            "Sin banco objetivo: {unsupported}."
        ),
        AdaptiveReviewCopyKey.NO_DUE: "No hay objetivos vencidos para repasar.",
        AdaptiveReviewCopyKey.NO_ELIGIBLE: (
            "Los objetivos vencidos actuales todavía no tienen actividades con enlaces explícitos. "
            "Permanecen disponibles en la cola de módulos."
        ),
        AdaptiveReviewCopyKey.PROGRESS: (
            "Actividad {current} de hasta {target} · {correct} correctas"
        ),
        AdaptiveReviewCopyKey.PRIMARY_OBJECTIVE: "Objetivo prioritario: {objective}",
        AdaptiveReviewCopyKey.ACTIVITY_TYPE: "Tipo de actividad: {activity}",
        AdaptiveReviewCopyKey.QUESTION_ACTIVITY: "Pregunta objetiva",
        AdaptiveReviewCopyKey.PROGRAMMING_ACTIVITY: "Reto de programación",
        AdaptiveReviewCopyKey.PROGRAMMING_RETRY_NOTICE: (
            "Puedes revisar el diagnóstico, pedir ayuda al tutor y volver a ejecutar el código. "
            "Al continuar, contará el resultado determinista más reciente. El borrador se guarda "
            "automáticamente."
        ),
        AdaptiveReviewCopyKey.RESTORED_RESULT: (
            "Se restauró un resultado determinista pendiente. Puedes continuar con ese resultado o "
            "volver a ejecutar el código."
        ),
        AdaptiveReviewCopyKey.NEXT: "Continuar",
        AdaptiveReviewCopyKey.FINISH: "Ver resumen",
        AdaptiveReviewCopyKey.SUMMARY_TITLE: "Resumen de la sesión",
        AdaptiveReviewCopyKey.SUMMARY: (
            "Respuestas: {answered}. Correctas: {correct}. Precisión: {accuracy} %. "
            "Actividades: {questions} preguntas y {programming} retos de programación. "
            "Objetivos trabajados: {objectives}."
        ),
        AdaptiveReviewCopyKey.EXHAUSTED: (
            "La sesión terminó antes del objetivo previsto porque no quedaban actividades "
            "autorizadas sin repetir."
        ),
        AdaptiveReviewCopyKey.COMPLETE: "Se alcanzó el objetivo de la sesión.",
        AdaptiveReviewCopyKey.RETURN_TO_QUEUE: "Actualizar cola de repaso",
    },
    AppLocale.ENGLISH: {
        AdaptiveReviewCopyKey.TAB: "Adaptive session",
        AdaptiveReviewCopyKey.TITLE: "Adaptive review",
        AdaptiveReviewCopyKey.INTRO: (
            "The session combines authorized questions and programming challenges from weakness, "
            "lapses, and results within this session. It avoids immediately repeating the same "
            "objective."
        ),
        AdaptiveReviewCopyKey.START: "Start session",
        AdaptiveReviewCopyKey.RESTART: "Create another session",
        AdaptiveReviewCopyKey.RESUME: "Resume session",
        AdaptiveReviewCopyKey.DISCARD: "Discard saved session",
        AdaptiveReviewCopyKey.RESUME_AVAILABLE: (
            "A saved session is available: {answered} of {target} activities accepted. You can "
            "continue from the exact pending activity."
        ),
        AdaptiveReviewCopyKey.INVALIDATED: (
            "The saved session was discarded because the academic catalog changed or the document "
            "was incompatible. Your attempts and mastery remain intact."
        ),
        AdaptiveReviewCopyKey.DUE_SUMMARY: (
            "Due objectives: {due}. Eligible for deterministic activities: {eligible}. "
            "Without an objective bank: {unsupported}."
        ),
        AdaptiveReviewCopyKey.NO_DUE: "No objectives are currently due for review.",
        AdaptiveReviewCopyKey.NO_ELIGIBLE: (
            "The current due objectives do not yet have activities with explicit links. They "
            "remain available in the module queue."
        ),
        AdaptiveReviewCopyKey.PROGRESS: (
            "Activity {current} of up to {target} · {correct} correct"
        ),
        AdaptiveReviewCopyKey.PRIMARY_OBJECTIVE: "Priority objective: {objective}",
        AdaptiveReviewCopyKey.ACTIVITY_TYPE: "Activity type: {activity}",
        AdaptiveReviewCopyKey.QUESTION_ACTIVITY: "Objective question",
        AdaptiveReviewCopyKey.PROGRAMMING_ACTIVITY: "Programming challenge",
        AdaptiveReviewCopyKey.PROGRAMMING_RETRY_NOTICE: (
            "You may inspect the diagnostic, ask the tutor for help, and run the code again. The "
            "latest deterministic result counts when you continue. The draft is saved "
            "automatically."
        ),
        AdaptiveReviewCopyKey.RESTORED_RESULT: (
            "A pending deterministic result was restored. You may continue with it or run the code "
            "again."
        ),
        AdaptiveReviewCopyKey.NEXT: "Continue",
        AdaptiveReviewCopyKey.FINISH: "View summary",
        AdaptiveReviewCopyKey.SUMMARY_TITLE: "Session summary",
        AdaptiveReviewCopyKey.SUMMARY: (
            "Answers: {answered}. Correct: {correct}. Accuracy: {accuracy}%. Activities: "
            "{questions} questions and {programming} programming challenges. Objectives reviewed: "
            "{objectives}."
        ),
        AdaptiveReviewCopyKey.EXHAUSTED: (
            "The session ended before its target because no unrepeated authorized activities "
            "remained."
        ),
        AdaptiveReviewCopyKey.COMPLETE: "The session target was reached.",
        AdaptiveReviewCopyKey.RETURN_TO_QUEUE: "Refresh review queue",
    },
    AppLocale.DANISH_DENMARK: {
        AdaptiveReviewCopyKey.TAB: "Adaptiv session",
        AdaptiveReviewCopyKey.TITLE: "Adaptiv repetition",
        AdaptiveReviewCopyKey.INTRO: (
            "Sessionen kombinerer autoriserede spørgsmål og programmeringsopgaver ud fra svaghed, "
            "tilbagefald og resultater i denne session. Det samme læringsmål gentages ikke "
            "umiddelbart."
        ),
        AdaptiveReviewCopyKey.START: "Start session",
        AdaptiveReviewCopyKey.RESTART: "Opret en ny session",
        AdaptiveReviewCopyKey.RESUME: "Genoptag session",
        AdaptiveReviewCopyKey.DISCARD: "Kassér gemt session",
        AdaptiveReviewCopyKey.RESUME_AVAILABLE: (
            "Der findes en gemt session: {answered} af {target} aktiviteter er accepteret. Du kan "
            "fortsætte fra den præcise ventende aktivitet."
        ),
        AdaptiveReviewCopyKey.INVALIDATED: (
            "Den gemte session blev kasseret, fordi det faglige katalog blev ændret, eller dokumentet "
            "var inkompatibelt. Dine forsøg og din mestring er bevaret."
        ),
        AdaptiveReviewCopyKey.DUE_SUMMARY: (
            "Forfaldne læringsmål: {due}. Egnede til deterministiske aktiviteter: {eligible}. "
            "Uden objektivbank: {unsupported}."
        ),
        AdaptiveReviewCopyKey.NO_DUE: "Der er ingen læringsmål, som skal repeteres nu.",
        AdaptiveReviewCopyKey.NO_ELIGIBLE: (
            "De aktuelle forfaldne læringsmål har endnu ikke aktiviteter med eksplicitte "
            "koblinger. De er fortsat tilgængelige i modulkøen."
        ),
        AdaptiveReviewCopyKey.PROGRESS: (
            "Aktivitet {current} af op til {target} · {correct} korrekte"
        ),
        AdaptiveReviewCopyKey.PRIMARY_OBJECTIVE: "Prioriteret læringsmål: {objective}",
        AdaptiveReviewCopyKey.ACTIVITY_TYPE: "Aktivitetstype: {activity}",
        AdaptiveReviewCopyKey.QUESTION_ACTIVITY: "Objektivt spørgsmål",
        AdaptiveReviewCopyKey.PROGRAMMING_ACTIVITY: "Programmeringsopgave",
        AdaptiveReviewCopyKey.PROGRAMMING_RETRY_NOTICE: (
            "Du kan gennemgå diagnosen, bede tutoren om hjælp og køre koden igen. Det seneste "
            "deterministiske resultat tæller, når du fortsætter. Kladdekoden gemmes automatisk."
        ),
        AdaptiveReviewCopyKey.RESTORED_RESULT: (
            "Et ventende deterministisk resultat blev gendannet. Du kan fortsætte med det eller køre "
            "koden igen."
        ),
        AdaptiveReviewCopyKey.NEXT: "Fortsæt",
        AdaptiveReviewCopyKey.FINISH: "Se oversigt",
        AdaptiveReviewCopyKey.SUMMARY_TITLE: "Sessionsoversigt",
        AdaptiveReviewCopyKey.SUMMARY: (
            "Svar: {answered}. Korrekte: {correct}. Nøjagtighed: {accuracy} %. Aktiviteter: "
            "{questions} spørgsmål og {programming} programmeringsopgaver. Bearbejdede læringsmål: "
            "{objectives}."
        ),
        AdaptiveReviewCopyKey.EXHAUSTED: (
            "Sessionen sluttede før målet, fordi der ikke var flere autoriserede aktiviteter uden "
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
