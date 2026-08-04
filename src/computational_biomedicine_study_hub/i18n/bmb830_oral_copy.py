"""Strict trilingual copy for the BMB830 Socratic oral-practice simulator."""

from __future__ import annotations

from enum import StrEnum
from string import Formatter

from ..learning.bmb830_oral_exam import OralCriterion
from .locales import AppLocale


class BMB830OralCopyKey(StrEnum):
    TAB = "bmb830_oral.tab"
    TITLE = "bmb830_oral.title"
    INTRO = "bmb830_oral.intro"
    BOUNDARY = "bmb830_oral.boundary"
    PROMPT = "bmb830_oral.prompt"
    TRANSCRIPT = "bmb830_oral.transcript"
    TRANSCRIPT_PLACEHOLDER = "bmb830_oral.transcript_placeholder"
    EVALUATE = "bmb830_oral.evaluate"
    THINKING = "bmb830_oral.thinking"
    NEXT_RECOMMENDED = "bmb830_oral.next_recommended"
    FEEDBACK = "bmb830_oral.feedback"
    FOLLOW_UP = "bmb830_oral.follow_up"
    SCORES = "bmb830_oral.scores"
    STRENGTHS = "bmb830_oral.strengths"
    GAPS = "bmb830_oral.gaps"
    MISCONCEPTIONS = "bmb830_oral.misconceptions"
    NEXT_ACTION = "bmb830_oral.next_action"
    CONFIDENCE = "bmb830_oral.confidence"
    HISTORY = "bmb830_oral.history"
    NO_HISTORY = "bmb830_oral.no_history"
    SUMMARY = "bmb830_oral.summary"
    ATTEMPTS = "bmb830_oral.attempts"
    AVERAGE = "bmb830_oral.average"
    SAVED = "bmb830_oral.saved"
    EMPTY = "bmb830_oral.empty"
    ERROR = "bmb830_oral.error"
    NO_OFFICIAL_GRADE = "bmb830_oral.no_official_grade"


_COPY: dict[BMB830OralCopyKey, dict[AppLocale, str]] = {
    BMB830OralCopyKey.TAB: {
        AppLocale.SPANISH_SPAIN: "BMB830 · Examen oral",
        AppLocale.ENGLISH: "BMB830 · Oral exam",
        AppLocale.DANISH_DENMARK: "BMB830 · Mundtlig eksamen",
    },
    BMB830OralCopyKey.TITLE: {
        AppLocale.SPANISH_SPAIN: "Simulador socrático de examen oral BMB830",
        AppLocale.ENGLISH: "BMB830 Socratic oral-exam simulator",
        AppLocale.DANISH_DENMARK: "BMB830 sokratisk simulator til mundtlig eksamen",
    },
    BMB830OralCopyKey.INTRO: {
        AppLocale.SPANISH_SPAIN: "Responde como si estuvieras explicando ante un examinador. Ollama analiza la transcripción con el contenido autorado del módulo, identifica evidencia y formula una sola repregunta socrática.",
        AppLocale.ENGLISH: "Answer as though explaining to an examiner. Ollama analyses the transcript against the authored module content, identifies evidence, and asks one Socratic follow-up question.",
        AppLocale.DANISH_DENMARK: "Svar som ved en mundtlig forklaring til en eksaminator. Ollama analyserer transskriptionen ud fra modulets forfattede indhold, identificerer evidens og stiller ét sokratisk opfølgende spørgsmål.",
    },
    BMB830OralCopyKey.BOUNDARY: {
        AppLocale.SPANISH_SPAIN: "La evaluación del modelo es formativa y provisional. No es una calificación oficial y no modifica el dominio objetivo calculado por la aplicación.",
        AppLocale.ENGLISH: "The model evaluation is formative and provisional. It is not an official grade and does not change objective mastery calculated by the application.",
        AppLocale.DANISH_DENMARK: "Modelvurderingen er formativ og foreløbig. Den er ikke en officiel karakter og ændrer ikke den objektive mestring, som applikationen beregner.",
    },
    BMB830OralCopyKey.PROMPT: {
        AppLocale.SPANISH_SPAIN: "Pregunta oral",
        AppLocale.ENGLISH: "Oral question",
        AppLocale.DANISH_DENMARK: "Mundtligt spørgsmål",
    },
    BMB830OralCopyKey.TRANSCRIPT: {
        AppLocale.SPANISH_SPAIN: "Respuesta o transcripción",
        AppLocale.ENGLISH: "Answer or transcript",
        AppLocale.DANISH_DENMARK: "Svar eller transskription",
    },
    BMB830OralCopyKey.TRANSCRIPT_PLACEHOLDER: {
        AppLocale.SPANISH_SPAIN: "Expón tu razonamiento completo: método, supuestos, interpretación, incertidumbre y limitaciones…",
        AppLocale.ENGLISH: "State your complete reasoning: method, assumptions, interpretation, uncertainty, and limitations…",
        AppLocale.DANISH_DENMARK: "Forklar hele din ræsonnering: metode, antagelser, fortolkning, usikkerhed og begrænsninger…",
    },
    BMB830OralCopyKey.EVALUATE: {
        AppLocale.SPANISH_SPAIN: "Evaluar y generar repregunta",
        AppLocale.ENGLISH: "Evaluate and generate follow-up",
        AppLocale.DANISH_DENMARK: "Vurdér og generér opfølgende spørgsmål",
    },
    BMB830OralCopyKey.THINKING: {
        AppLocale.SPANISH_SPAIN: "Ollama está razonando sobre la respuesta y contrastándola con el material del módulo…",
        AppLocale.ENGLISH: "Ollama is reasoning about the answer and checking it against the module material…",
        AppLocale.DANISH_DENMARK: "Ollama ræsonnerer over svaret og sammenholder det med modulmaterialet…",
    },
    BMB830OralCopyKey.NEXT_RECOMMENDED: {
        AppLocale.SPANISH_SPAIN: "Abrir siguiente pregunta recomendada",
        AppLocale.ENGLISH: "Open next recommended question",
        AppLocale.DANISH_DENMARK: "Åbn næste anbefalede spørgsmål",
    },
    BMB830OralCopyKey.FEEDBACK: {
        AppLocale.SPANISH_SPAIN: "Retroalimentación formativa",
        AppLocale.ENGLISH: "Formative feedback",
        AppLocale.DANISH_DENMARK: "Formativ feedback",
    },
    BMB830OralCopyKey.FOLLOW_UP: {
        AppLocale.SPANISH_SPAIN: "Repregunta socrática",
        AppLocale.ENGLISH: "Socratic follow-up",
        AppLocale.DANISH_DENMARK: "Sokratisk opfølgning",
    },
    BMB830OralCopyKey.SCORES: {
        AppLocale.SPANISH_SPAIN: "Dimensiones formativas (0–4)",
        AppLocale.ENGLISH: "Formative dimensions (0–4)",
        AppLocale.DANISH_DENMARK: "Formative dimensioner (0–4)",
    },
    BMB830OralCopyKey.STRENGTHS: {
        AppLocale.SPANISH_SPAIN: "Fortalezas observadas",
        AppLocale.ENGLISH: "Observed strengths",
        AppLocale.DANISH_DENMARK: "Observerede styrker",
    },
    BMB830OralCopyKey.GAPS: {
        AppLocale.SPANISH_SPAIN: "Vacíos u omisiones",
        AppLocale.ENGLISH: "Gaps or omissions",
        AppLocale.DANISH_DENMARK: "Mangler eller udeladelser",
    },
    BMB830OralCopyKey.MISCONCEPTIONS: {
        AppLocale.SPANISH_SPAIN: "Posibles errores conceptuales",
        AppLocale.ENGLISH: "Possible misconceptions",
        AppLocale.DANISH_DENMARK: "Mulige misforståelser",
    },
    BMB830OralCopyKey.NEXT_ACTION: {
        AppLocale.SPANISH_SPAIN: "Siguiente acción recomendada",
        AppLocale.ENGLISH: "Recommended next action",
        AppLocale.DANISH_DENMARK: "Anbefalet næste handling",
    },
    BMB830OralCopyKey.CONFIDENCE: {
        AppLocale.SPANISH_SPAIN: "Confianza de la evaluación: {percent}%",
        AppLocale.ENGLISH: "Evaluation confidence: {percent}%",
        AppLocale.DANISH_DENMARK: "Vurderingens sikkerhed: {percent}%",
    },
    BMB830OralCopyKey.HISTORY: {
        AppLocale.SPANISH_SPAIN: "Intentos de esta pregunta",
        AppLocale.ENGLISH: "Attempts for this question",
        AppLocale.DANISH_DENMARK: "Forsøg til dette spørgsmål",
    },
    BMB830OralCopyKey.NO_HISTORY: {
        AppLocale.SPANISH_SPAIN: "Aún no hay intentos evaluados para esta pregunta.",
        AppLocale.ENGLISH: "No evaluated attempts exist for this question yet.",
        AppLocale.DANISH_DENMARK: "Der findes endnu ingen vurderede forsøg til dette spørgsmål.",
    },
    BMB830OralCopyKey.SUMMARY: {
        AppLocale.SPANISH_SPAIN: "Seguimiento acumulado",
        AppLocale.ENGLISH: "Accumulated tracking",
        AppLocale.DANISH_DENMARK: "Samlet opfølgning",
    },
    BMB830OralCopyKey.ATTEMPTS: {
        AppLocale.SPANISH_SPAIN: "Intentos evaluados: {count}",
        AppLocale.ENGLISH: "Evaluated attempts: {count}",
        AppLocale.DANISH_DENMARK: "Vurderede forsøg: {count}",
    },
    BMB830OralCopyKey.AVERAGE: {
        AppLocale.SPANISH_SPAIN: "Promedio formativo acumulado: {score}/4",
        AppLocale.ENGLISH: "Accumulated formative average: {score}/4",
        AppLocale.DANISH_DENMARK: "Samlet formativt gennemsnit: {score}/4",
    },
    BMB830OralCopyKey.SAVED: {
        AppLocale.SPANISH_SPAIN: "Intento guardado localmente.",
        AppLocale.ENGLISH: "Attempt saved locally.",
        AppLocale.DANISH_DENMARK: "Forsøget er gemt lokalt.",
    },
    BMB830OralCopyKey.EMPTY: {
        AppLocale.SPANISH_SPAIN: "Escribe o pega una transcripción antes de evaluarla.",
        AppLocale.ENGLISH: "Write or paste a transcript before evaluating it.",
        AppLocale.DANISH_DENMARK: "Skriv eller indsæt en transskription før vurdering.",
    },
    BMB830OralCopyKey.ERROR: {
        AppLocale.SPANISH_SPAIN: "No se pudo evaluar la respuesta: {detail}",
        AppLocale.ENGLISH: "The answer could not be evaluated: {detail}",
        AppLocale.DANISH_DENMARK: "Svaret kunne ikke vurderes: {detail}",
    },
    BMB830OralCopyKey.NO_OFFICIAL_GRADE: {
        AppLocale.SPANISH_SPAIN: "Los valores 0–4 son indicadores internos para comparar intentos y localizar debilidades. No corresponden a la escala oficial danesa ni predicen una nota de examen.",
        AppLocale.ENGLISH: "The 0–4 values are internal indicators for comparing attempts and locating weaknesses. They do not correspond to the official Danish grading scale or predict an exam grade.",
        AppLocale.DANISH_DENMARK: "Værdierne 0–4 er interne indikatorer til at sammenligne forsøg og finde svagheder. De svarer ikke til den officielle danske karakterskala og forudsiger ikke en eksamenskarakter.",
    },
}


_CRITERIA: dict[OralCriterion, dict[AppLocale, str]] = {
    OralCriterion.ACCURACY: {
        AppLocale.SPANISH_SPAIN: "Exactitud conceptual",
        AppLocale.ENGLISH: "Conceptual accuracy",
        AppLocale.DANISH_DENMARK: "Begrebsmæssig korrekthed",
    },
    OralCriterion.STATISTICAL_REASONING: {
        AppLocale.SPANISH_SPAIN: "Razonamiento estadístico",
        AppLocale.ENGLISH: "Statistical reasoning",
        AppLocale.DANISH_DENMARK: "Statistisk ræsonnering",
    },
    OralCriterion.INTERPRETATION: {
        AppLocale.SPANISH_SPAIN: "Interpretación biológica",
        AppLocale.ENGLISH: "Biological interpretation",
        AppLocale.DANISH_DENMARK: "Biologisk fortolkning",
    },
    OralCriterion.LIMITATIONS: {
        AppLocale.SPANISH_SPAIN: "Supuestos y limitaciones",
        AppLocale.ENGLISH: "Assumptions and limitations",
        AppLocale.DANISH_DENMARK: "Antagelser og begrænsninger",
    },
    OralCriterion.COMMUNICATION: {
        AppLocale.SPANISH_SPAIN: "Comunicación científica",
        AppLocale.ENGLISH: "Scientific communication",
        AppLocale.DANISH_DENMARK: "Videnskabelig kommunikation",
    },
}


def bmb830_oral_text(
    locale: AppLocale,
    key: BMB830OralCopyKey,
    **values: object,
) -> str:
    template = _COPY[key][locale]
    required = {
        field_name for _, field_name, _, _ in Formatter().parse(template) if field_name is not None
    }
    if required != set(values):
        raise ValueError(
            f"BMB830 oral copy {key.value!r} requires {sorted(required)}; "
            f"received {sorted(values)}."
        )
    return template.format(**values)


def bmb830_oral_criterion_text(locale: AppLocale, criterion: OralCriterion) -> str:
    return _CRITERIA[criterion][locale]


def validate_bmb830_oral_copy() -> None:
    expected = set(BMB830OralCopyKey)
    for locale in AppLocale:
        available = {key for key, translations in _COPY.items() if locale in translations}
        if available != expected:
            raise ValueError(f"Incomplete BMB830 oral copy for {locale.value}.")
        if {
            criterion for criterion, translations in _CRITERIA.items() if locale in translations
        } != set(OralCriterion):
            raise ValueError(f"Incomplete BMB830 oral criterion copy for {locale.value}.")


validate_bmb830_oral_copy()

__all__ = [
    "BMB830OralCopyKey",
    "bmb830_oral_criterion_text",
    "bmb830_oral_text",
    "validate_bmb830_oral_copy",
]
