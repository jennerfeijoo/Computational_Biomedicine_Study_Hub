"""BMB830 course registration and initial page."""

from __future__ import annotations

from PySide6.QtWidgets import QWidget

from ..i18n import DEFAULT_LOCALE, AppLocale
from ..ui.pages.course_overview_page import CourseOverviewPage
from .models import CourseRegistration

_OVERVIEW = {
    AppLocale.SPANISH_SPAIN: (
        "Fundamentos de R, estadística descriptiva, probabilidad, inferencia, regresión y análisis multivariante inicial.",
        (
            "Pregunta estadística y diseño",
            "Estructura y calidad de los datos",
            "Método, supuestos e incertidumbre",
            "Implementación reproducible en R",
            "Interpretación científica de resultados",
        ),
    ),
    AppLocale.ENGLISH: (
        "R foundations, descriptive statistics, probability, inference, regression and introductory multivariate analysis.",
        (
            "Statistical question and design",
            "Data structure and quality",
            "Method, assumptions and uncertainty",
            "Reproducible implementation in R",
            "Scientific interpretation of results",
        ),
    ),
    AppLocale.DANISH_DENMARK: (
        "Grundlæggende R, deskriptiv statistik, sandsynlighed, inferens, regression og introduktion til multivariat analyse.",
        (
            "Statistisk spørgsmål og design",
            "Datastruktur og datakvalitet",
            "Metode, antagelser og usikkerhed",
            "Reproducerbar implementering i R",
            "Videnskabelig fortolkning af resultater",
        ),
    ),
}


class BMB830Page(CourseOverviewPage):
    """Initial Biostatistics in R I page with a workflow-oriented structure."""

    def __init__(self, locale: AppLocale = DEFAULT_LOCALE) -> None:
        summary, sections = _OVERVIEW[locale]
        super().__init__(
            code="BMB830",
            ects=5,
            summary=summary,
            planned_sections=sections,
            locale=locale,
        )


def create_page(locale: AppLocale = DEFAULT_LOCALE) -> QWidget:
    """Create the BMB830 page without constructing widgets during import."""
    return BMB830Page(locale)


COURSE = CourseRegistration(
    code="BMB830",
    title="Bioestadística en R I",
    ects=5,
    semester=1,
    summary="Fundamentos de R, inferencia, visualización y análisis biológico.",
    page_factory=create_page,
    localized_titles={
        AppLocale.SPANISH_SPAIN: "Bioestadística en R I",
        AppLocale.ENGLISH: "Biostatistics in R I",
        AppLocale.DANISH_DENMARK: "Biostatistik i R I",
    },
    localized_summaries={
        AppLocale.SPANISH_SPAIN: (
            "Fundamentos de R, inferencia, visualización y análisis de datos biológicos."
        ),
        AppLocale.ENGLISH: (
            "R foundations, inference, visualization and biological data analysis."
        ),
        AppLocale.DANISH_DENMARK: (
            "Grundlæggende R, inferens, visualisering og analyse af biologiske data."
        ),
    },
)
