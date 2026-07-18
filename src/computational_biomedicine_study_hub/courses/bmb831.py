"""BMB831 course registration and initial page."""

from __future__ import annotations

from PySide6.QtWidgets import QWidget

from ..ui.pages.course_overview_page import CourseOverviewPage
from .models import CourseRegistration


class BMB831Page(CourseOverviewPage):
    """Initial Biostatistics in R II page with a pipeline-oriented structure."""

    def __init__(self) -> None:
        super().__init__(
            code="BMB831",
            ects=5,
            summary=(
                "Modelos avanzados, pruebas múltiples, reducción dimensional, "
                "clasificación y pipelines para datos ómicos."
            ),
            planned_sections=(
                "Método estadístico y supuestos",
                "Implementación en R y Bioconductor",
                "Etapas del pipeline analítico",
                "Control de calidad y reproducibilidad",
                "Interpretación biológica y evaluación crítica",
            ),
        )


def create_page() -> QWidget:
    """Create the BMB831 page without constructing widgets during import."""
    return BMB831Page()


COURSE = CourseRegistration(
    code="BMB831",
    title="Biostatistics in R II",
    ects=5,
    semester=1,
    summary="Estadística avanzada, Bioconductor y pipelines para datos ómicos.",
    page_factory=create_page,
)
