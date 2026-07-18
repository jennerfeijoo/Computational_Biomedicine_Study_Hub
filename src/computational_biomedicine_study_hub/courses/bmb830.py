"""BMB830 course registration and initial page."""

from __future__ import annotations

from PySide6.QtWidgets import QWidget

from ..ui.pages.course_overview_page import CourseOverviewPage
from .models import CourseRegistration


class BMB830Page(CourseOverviewPage):
    """Initial Biostatistics in R I page with a workflow-oriented structure."""

    def __init__(self) -> None:
        super().__init__(
            code="BMB830",
            ects=5,
            summary=(
                "Fundamentos de R, estadística descriptiva, probabilidad, "
                "inferencia, regresión y análisis multivariante inicial."
            ),
            planned_sections=(
                "Pregunta estadística y diseño",
                "Estructura y calidad de los datos",
                "Método, supuestos e incertidumbre",
                "Implementación reproducible en R",
                "Interpretación científica de resultados",
            ),
        )


def create_page() -> QWidget:
    """Create the BMB830 page without constructing widgets during import."""
    return BMB830Page()


COURSE = CourseRegistration(
    code="BMB830",
    title="Biostatistics in R I",
    ects=5,
    semester=1,
    summary="Fundamentos de R, inferencia, visualización y análisis biológico.",
    page_factory=create_page,
)
