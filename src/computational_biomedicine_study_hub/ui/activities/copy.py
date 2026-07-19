"""Small trilingual copy catalog for reusable activity controls."""

from __future__ import annotations

from enum import StrEnum

from ...i18n import AppLocale


class ActivityCopyKey(StrEnum):
    SUBMIT = "submit"
    CHOOSE = "choose"
    CORRECT = "correct"
    INCORRECT = "incorrect"
    YOUR_ANSWER = "your_answer"
    REVEAL_REFERENCE = "reveal_reference"
    REFERENCE = "reference"
    RUBRIC = "rubric"
    SELF_ASSESS = "self_assess"
    SOLVED = "solved"
    PARTIAL = "partial"
    REVIEW = "review"
    GAP = "gap"
    MOVE_UP = "move_up"
    MOVE_DOWN = "move_down"
    MATCH_WITH = "match_with"
    CONFIDENCE = "confidence"
    CONFIDENCE_LOW = "confidence_low"
    CONFIDENCE_MEDIUM = "confidence_medium"
    CONFIDENCE_HIGH = "confidence_high"
    LOCAL_FEEDBACK = "local_feedback"


_COPY: dict[AppLocale, dict[ActivityCopyKey, str]] = {
    AppLocale.SPANISH_SPAIN: {
        ActivityCopyKey.SUBMIT: "Comprobar",
        ActivityCopyKey.CHOOSE: "Selecciona una respuesta",
        ActivityCopyKey.CORRECT: "Respuesta correcta.",
        ActivityCopyKey.INCORRECT: "Revisa la respuesta y la explicación.",
        ActivityCopyKey.YOUR_ANSWER: "Tu respuesta",
        ActivityCopyKey.REVEAL_REFERENCE: "Mostrar referencia y rúbrica",
        ActivityCopyKey.REFERENCE: "Respuesta de referencia",
        ActivityCopyKey.RUBRIC: "Rúbrica",
        ActivityCopyKey.SELF_ASSESS: "Autoevaluación",
        ActivityCopyKey.SOLVED: "Resuelto",
        ActivityCopyKey.PARTIAL: "Parcial",
        ActivityCopyKey.REVIEW: "Revisar",
        ActivityCopyKey.GAP: "Hueco",
        ActivityCopyKey.MOVE_UP: "Subir",
        ActivityCopyKey.MOVE_DOWN: "Bajar",
        ActivityCopyKey.MATCH_WITH: "Relacionar con…",
        ActivityCopyKey.CONFIDENCE: "Confianza",
        ActivityCopyKey.CONFIDENCE_LOW: "Baja",
        ActivityCopyKey.CONFIDENCE_MEDIUM: "Media",
        ActivityCopyKey.CONFIDENCE_HIGH: "Alta",
        ActivityCopyKey.LOCAL_FEEDBACK: "Pedir retroalimentación local",
    },
    AppLocale.ENGLISH: {
        ActivityCopyKey.SUBMIT: "Check",
        ActivityCopyKey.CHOOSE: "Select an answer",
        ActivityCopyKey.CORRECT: "Correct answer.",
        ActivityCopyKey.INCORRECT: "Review the answer and explanation.",
        ActivityCopyKey.YOUR_ANSWER: "Your answer",
        ActivityCopyKey.REVEAL_REFERENCE: "Show reference and rubric",
        ActivityCopyKey.REFERENCE: "Reference answer",
        ActivityCopyKey.RUBRIC: "Rubric",
        ActivityCopyKey.SELF_ASSESS: "Self-assessment",
        ActivityCopyKey.SOLVED: "Solved",
        ActivityCopyKey.PARTIAL: "Partial",
        ActivityCopyKey.REVIEW: "Review",
        ActivityCopyKey.GAP: "Gap",
        ActivityCopyKey.MOVE_UP: "Move up",
        ActivityCopyKey.MOVE_DOWN: "Move down",
        ActivityCopyKey.MATCH_WITH: "Match with…",
        ActivityCopyKey.CONFIDENCE: "Confidence",
        ActivityCopyKey.CONFIDENCE_LOW: "Low",
        ActivityCopyKey.CONFIDENCE_MEDIUM: "Medium",
        ActivityCopyKey.CONFIDENCE_HIGH: "High",
        ActivityCopyKey.LOCAL_FEEDBACK: "Request local feedback",
    },
    AppLocale.DANISH_DENMARK: {
        ActivityCopyKey.SUBMIT: "Kontrollér",
        ActivityCopyKey.CHOOSE: "Vælg et svar",
        ActivityCopyKey.CORRECT: "Korrekt svar.",
        ActivityCopyKey.INCORRECT: "Gennemgå svaret og forklaringen.",
        ActivityCopyKey.YOUR_ANSWER: "Dit svar",
        ActivityCopyKey.REVEAL_REFERENCE: "Vis referencesvar og rubric",
        ActivityCopyKey.REFERENCE: "Referencesvar",
        ActivityCopyKey.RUBRIC: "Rubric",
        ActivityCopyKey.SELF_ASSESS: "Selvevaluering",
        ActivityCopyKey.SOLVED: "Løst",
        ActivityCopyKey.PARTIAL: "Delvist",
        ActivityCopyKey.REVIEW: "Gennemgå",
        ActivityCopyKey.GAP: "Hul",
        ActivityCopyKey.MOVE_UP: "Flyt op",
        ActivityCopyKey.MOVE_DOWN: "Flyt ned",
        ActivityCopyKey.MATCH_WITH: "Match med…",
        ActivityCopyKey.CONFIDENCE: "Sikkerhed",
        ActivityCopyKey.CONFIDENCE_LOW: "Lav",
        ActivityCopyKey.CONFIDENCE_MEDIUM: "Mellem",
        ActivityCopyKey.CONFIDENCE_HIGH: "Høj",
        ActivityCopyKey.LOCAL_FEEDBACK: "Bed om lokal feedback",
    },
}


def activity_text(locale: AppLocale, key: ActivityCopyKey) -> str:
    """Return strict copy for one supported locale."""
    return _COPY[locale][key]


__all__ = ["ActivityCopyKey", "activity_text"]
