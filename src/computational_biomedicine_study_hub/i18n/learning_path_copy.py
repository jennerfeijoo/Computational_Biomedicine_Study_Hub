"""Strict trilingual copy for the evidence-driven learning-path page."""

from __future__ import annotations

from enum import StrEnum

from ..learning.activity_types import StudyCycleStage
from .locales import AppLocale


class LearningPathCopyKey(StrEnum):
    NAVIGATION = "navigation"
    PAGE_TITLE = "page_title"
    PAGE_SUBTITLE = "page_subtitle"
    INTRO = "intro"
    DUE_TITLE = "due_title"
    NO_DUE = "no_due"
    COURSE_TITLE = "course_title"
    MASTERY = "mastery"
    OBJECTIVES = "objectives"
    OPEN = "open"


_COPY: dict[LearningPathCopyKey, dict[AppLocale, str]] = {
    LearningPathCopyKey.NAVIGATION: {
        AppLocale.SPANISH_SPAIN: "Ruta de aprendizaje",
        AppLocale.ENGLISH: "Learning path",
        AppLocale.DANISH_DENMARK: "Læringssti",
    },
    LearningPathCopyKey.PAGE_TITLE: {
        AppLocale.SPANISH_SPAIN: "Ruta de aprendizaje basada en evidencia",
        AppLocale.ENGLISH: "Evidence-driven learning path",
        AppLocale.DANISH_DENMARK: "Evidensbaseret læringssti",
    },
    LearningPathCopyKey.PAGE_SUBTITLE: {
        AppLocale.SPANISH_SPAIN: "Siguiente acción recomendada por asignatura a partir del progreso local.",
        AppLocale.ENGLISH: "Next recommended action for each course based on local progress.",
        AppLocale.DANISH_DENMARK: "Næste anbefalede handling for hvert kursus baseret på lokale fremskridt.",
    },
    LearningPathCopyKey.INTRO: {
        AppLocale.SPANISH_SPAIN: "La aplicación prioriza contenido, práctica, recuperación, transferencia y evaluación según evidencia objetiva. Las visitas a páginas y la retroalimentación de IA no se consideran dominio.",
        AppLocale.ENGLISH: "The application prioritises content, practice, retrieval, transfer, and assessment from objective evidence. Page visits and AI feedback do not count as mastery.",
        AppLocale.DANISH_DENMARK: "Applikationen prioriterer indhold, øvelse, genkaldelse, transfer og evaluering ud fra objektiv evidens. Sidebesøg og AI-feedback tæller ikke som mestring.",
    },
    LearningPathCopyKey.DUE_TITLE: {
        AppLocale.SPANISH_SPAIN: "Revisión pendiente",
        AppLocale.ENGLISH: "Due review",
        AppLocale.DANISH_DENMARK: "Forfalden repetition",
    },
    LearningPathCopyKey.NO_DUE: {
        AppLocale.SPANISH_SPAIN: "No hay objetivos vencidos para revisión espaciada.",
        AppLocale.ENGLISH: "No objectives are currently due for spaced review.",
        AppLocale.DANISH_DENMARK: "Ingen læringsmål er aktuelt forfaldne til intervalrepetition.",
    },
    LearningPathCopyKey.COURSE_TITLE: {
        AppLocale.SPANISH_SPAIN: "Siguiente paso por asignatura",
        AppLocale.ENGLISH: "Next step by course",
        AppLocale.DANISH_DENMARK: "Næste trin pr. kursus",
    },
    LearningPathCopyKey.MASTERY: {
        AppLocale.SPANISH_SPAIN: "Dominio objetivo estimado: {percent}%",
        AppLocale.ENGLISH: "Estimated objective mastery: {percent}%",
        AppLocale.DANISH_DENMARK: "Estimeret mestring af læringsmål: {percent}%",
    },
    LearningPathCopyKey.OBJECTIVES: {
        AppLocale.SPANISH_SPAIN: "Objetivos prioritarios: {count}",
        AppLocale.ENGLISH: "Priority objectives: {count}",
        AppLocale.DANISH_DENMARK: "Prioriterede læringsmål: {count}",
    },
    LearningPathCopyKey.OPEN: {
        AppLocale.SPANISH_SPAIN: "Abrir actividad recomendada",
        AppLocale.ENGLISH: "Open recommended activity",
        AppLocale.DANISH_DENMARK: "Åbn anbefalet aktivitet",
    },
}


_STAGE_COPY: dict[StudyCycleStage, dict[AppLocale, str]] = {
    StudyCycleStage.CONCEPT: {
        AppLocale.SPANISH_SPAIN: "Conceptos y orientación",
        AppLocale.ENGLISH: "Concepts and orientation",
        AppLocale.DANISH_DENMARK: "Begreber og orientering",
    },
    StudyCycleStage.WORKED_EXAMPLE: {
        AppLocale.SPANISH_SPAIN: "Ejemplos resueltos",
        AppLocale.ENGLISH: "Worked examples",
        AppLocale.DANISH_DENMARK: "Gennemarbejdede eksempler",
    },
    StudyCycleStage.GUIDED_PRACTICE: {
        AppLocale.SPANISH_SPAIN: "Práctica guiada",
        AppLocale.ENGLISH: "Guided practice",
        AppLocale.DANISH_DENMARK: "Vejledt øvelse",
    },
    StudyCycleStage.RETRIEVAL: {
        AppLocale.SPANISH_SPAIN: "Recuperación activa",
        AppLocale.ENGLISH: "Active retrieval",
        AppLocale.DANISH_DENMARK: "Aktiv genkaldelse",
    },
    StudyCycleStage.FEEDBACK: {
        AppLocale.SPANISH_SPAIN: "Retroalimentación",
        AppLocale.ENGLISH: "Feedback",
        AppLocale.DANISH_DENMARK: "Feedback",
    },
    StudyCycleStage.TRANSFER: {
        AppLocale.SPANISH_SPAIN: "Transferencia a un caso nuevo",
        AppLocale.ENGLISH: "Transfer to a novel case",
        AppLocale.DANISH_DENMARK: "Transfer til en ny case",
    },
    StudyCycleStage.ASSESSMENT: {
        AppLocale.SPANISH_SPAIN: "Preparación de evaluación",
        AppLocale.ENGLISH: "Assessment preparation",
        AppLocale.DANISH_DENMARK: "Eksamensforberedelse",
    },
    StudyCycleStage.SPACED_REVIEW: {
        AppLocale.SPANISH_SPAIN: "Revisión espaciada",
        AppLocale.ENGLISH: "Spaced review",
        AppLocale.DANISH_DENMARK: "Intervalrepetition",
    },
}


_REASON_COPY: dict[str, dict[AppLocale, str]] = {
    "no_evidence": {
        AppLocale.SPANISH_SPAIN: "Todavía no existe evidencia objetiva para este módulo.",
        AppLocale.ENGLISH: "No objective evidence exists for this module yet.",
        AppLocale.DANISH_DENMARK: "Der findes endnu ingen objektiv evidens for dette modul.",
    },
    "partial_evidence": {
        AppLocale.SPANISH_SPAIN: "Algunos objetivos aún no tienen evidencia y requieren ejemplos adicionales.",
        AppLocale.ENGLISH: "Some objectives still lack evidence and need additional examples.",
        AppLocale.DANISH_DENMARK: "Nogle læringsmål mangler stadig evidens og kræver flere eksempler.",
    },
    "weak_mastery": {
        AppLocale.SPANISH_SPAIN: "El dominio actual es débil; conviene practicar antes de volver a evaluarse.",
        AppLocale.ENGLISH: "Current mastery is weak; practise before reassessment.",
        AppLocale.DANISH_DENMARK: "Den aktuelle mestring er svag; øv før ny evaluering.",
    },
    "retrieval_needed": {
        AppLocale.SPANISH_SPAIN: "El contenido necesita recuperación adicional para demostrar estabilidad.",
        AppLocale.ENGLISH: "The content needs further retrieval to demonstrate stability.",
        AppLocale.DANISH_DENMARK: "Indholdet kræver yderligere genkaldelse for at vise stabilitet.",
    },
    "course_ready_for_assessment": {
        AppLocale.SPANISH_SPAIN: "Los objetivos del curso superan el umbral interno y corresponde practicar su formato de evaluación.",
        AppLocale.ENGLISH: "Course objectives exceed the internal threshold; practise the course assessment format.",
        AppLocale.DANISH_DENMARK: "Kursets læringsmål overstiger den interne tærskel; øv kursets eksamensformat.",
    },
    "transfer_needed": {
        AppLocale.SPANISH_SPAIN: "El contenido está recuperado, pero falta demostrar transferencia en un caso nuevo.",
        AppLocale.ENGLISH: "Content has been retrieved, but transfer to a novel case is still needed.",
        AppLocale.DANISH_DENMARK: "Indholdet er genkaldt, men transfer til en ny case mangler stadig.",
    },
    "review_due": {
        AppLocale.SPANISH_SPAIN: "Un objetivo alcanzó su fecha de revisión espaciada.",
        AppLocale.ENGLISH: "An objective has reached its spaced-review date.",
        AppLocale.DANISH_DENMARK: "Et læringsmål har nået sin dato for intervalrepetition.",
    },
}


def learning_path_text(
    locale: AppLocale,
    key: LearningPathCopyKey,
    **values: object,
) -> str:
    """Return strict localized page copy."""

    return _COPY[key][locale].format(**values)


def learning_stage_text(locale: AppLocale, stage: StudyCycleStage) -> str:
    """Return one localized study-cycle stage label."""

    return _STAGE_COPY[stage][locale]


def learning_reason_text(locale: AppLocale, reason: str) -> str:
    """Return one localized recommendation rationale by stable reason value."""

    try:
        return _REASON_COPY[reason][locale]
    except KeyError as exc:
        raise ValueError(f"Unknown learning-path reason {reason!r}.") from exc


__all__ = [
    "LearningPathCopyKey",
    "learning_path_text",
    "learning_reason_text",
    "learning_stage_text",
]
