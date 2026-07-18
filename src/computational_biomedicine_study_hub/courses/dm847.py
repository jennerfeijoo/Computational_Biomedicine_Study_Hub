"""DM847 course registration and initial page."""

from __future__ import annotations

from PySide6.QtWidgets import QWidget

from ..i18n import AppLocale, DEFAULT_LOCALE
from ..ui.pages.course_overview_page import CourseOverviewPage
from .models import CourseRegistration


_OVERVIEW = {
    AppLocale.SPANISH_SPAIN: (
        "Modelos y algoritmos para secuencias, motivos, HMM, índices, NGS, redes y datos ómicos.",
        (
            "Contexto biológico de cada problema",
            "Modelo formal y supuestos",
            "Algoritmo, pseudocódigo y complejidad",
            "Implementación sobre ejemplos pequeños",
            "Interpretación biomédica y limitaciones",
        ),
    ),
    AppLocale.ENGLISH: (
        "Models and algorithms for sequences, motifs, HMMs, indexes, NGS, networks and omics data.",
        (
            "Biological context for each problem",
            "Formal model and assumptions",
            "Algorithm, pseudocode and complexity",
            "Implementation on small examples",
            "Biomedical interpretation and limitations",
        ),
    ),
    AppLocale.DANISH_DENMARK: (
        "Modeller og algoritmer til sekvenser, motiver, HMM'er, indekser, NGS, netværk og omikdata.",
        (
            "Biologisk kontekst for hvert problem",
            "Formel model og antagelser",
            "Algoritme, pseudokode og kompleksitet",
            "Implementering på små eksempler",
            "Biomedicinsk fortolkning og begrænsninger",
        ),
    ),
}


class DM847Page(CourseOverviewPage):
    """Initial bioinformatics page with a course-specific future structure."""

    def __init__(self, locale: AppLocale = DEFAULT_LOCALE) -> None:
        summary, sections = _OVERVIEW[locale]
        super().__init__(
            code="DM847",
            ects=10,
            summary=summary,
            planned_sections=sections,
            locale=locale,
        )


def create_page(locale: AppLocale = DEFAULT_LOCALE) -> QWidget:
    """Create the DM847 page without constructing widgets during import."""
    return DM847Page(locale)


COURSE = CourseRegistration(
    code="DM847",
    title="Introducción a la bioinformática",
    ects=10,
    semester=1,
    summary="Algoritmos, secuencias, modelos probabilísticos, redes y ómicas.",
    page_factory=create_page,
    localized_titles={
        AppLocale.SPANISH_SPAIN: "Introducción a la bioinformática",
        AppLocale.ENGLISH: "Introduction to Bioinformatics",
        AppLocale.DANISH_DENMARK: "Introduktion til bioinformatik",
    },
    localized_summaries={
        AppLocale.SPANISH_SPAIN: (
            "Algoritmos, secuencias, modelos probabilísticos, redes y datos ómicos."
        ),
        AppLocale.ENGLISH: (
            "Algorithms, sequences, probabilistic models, networks and omics data."
        ),
        AppLocale.DANISH_DENMARK: (
            "Algoritmer, sekvenser, probabilistiske modeller, netværk og omikdata."
        ),
    },
)
