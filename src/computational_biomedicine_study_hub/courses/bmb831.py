"""BMB831 course registration and initial page."""

from __future__ import annotations

from PySide6.QtWidgets import QWidget

from ..i18n import DEFAULT_LOCALE, AppLocale
from ..ui.pages.course_overview_page import CourseOverviewPage
from .models import CourseRegistration

_OVERVIEW = {
    AppLocale.SPANISH_SPAIN: (
        "Modelos avanzados, pruebas múltiples, reducción dimensional, clasificación y pipelines para datos ómicos.",
        (
            "Método estadístico y supuestos",
            "Implementación en R y Bioconductor",
            "Etapas del pipeline analítico",
            "Control de calidad y reproducibilidad",
            "Interpretación biológica y evaluación crítica",
        ),
    ),
    AppLocale.ENGLISH: (
        "Advanced models, multiple testing, dimensionality reduction, classification and pipelines for omics data.",
        (
            "Statistical method and assumptions",
            "Implementation in R and Bioconductor",
            "Analytical pipeline stages",
            "Quality control and reproducibility",
            "Biological interpretation and critical appraisal",
        ),
    ),
    AppLocale.DANISH_DENMARK: (
        "Avancerede modeller, multiple test, dimensionsreduktion, klassifikation og pipelines til omikdata.",
        (
            "Statistisk metode og antagelser",
            "Implementering i R og Bioconductor",
            "Trin i den analytiske pipeline",
            "Kvalitetskontrol og reproducerbarhed",
            "Biologisk fortolkning og kritisk vurdering",
        ),
    ),
}


class BMB831Page(CourseOverviewPage):
    """Initial Biostatistics in R II page with a pipeline-oriented structure."""

    def __init__(self, locale: AppLocale = DEFAULT_LOCALE) -> None:
        summary, sections = _OVERVIEW[locale]
        super().__init__(
            code="BMB831",
            ects=5,
            summary=summary,
            planned_sections=sections,
            locale=locale,
        )


def create_page(locale: AppLocale = DEFAULT_LOCALE) -> QWidget:
    """Create the BMB831 page without constructing widgets during import."""
    return BMB831Page(locale)


COURSE = CourseRegistration(
    code="BMB831",
    title="Bioestadística en R II",
    ects=5,
    semester=1,
    summary="Estadística avanzada, Bioconductor y pipelines para datos ómicos.",
    page_factory=create_page,
    localized_titles={
        AppLocale.SPANISH_SPAIN: "Bioestadística en R II",
        AppLocale.ENGLISH: "Biostatistics in R II",
        AppLocale.DANISH_DENMARK: "Biostatistik i R II",
    },
    localized_summaries={
        AppLocale.SPANISH_SPAIN: (
            "Estadística avanzada, Bioconductor y pipelines para datos ómicos."
        ),
        AppLocale.ENGLISH: ("Advanced statistics, Bioconductor and pipelines for omics data."),
        AppLocale.DANISH_DENMARK: ("Avanceret statistik, Bioconductor og pipelines til omikdata."),
    },
)
