"""DM847 course registration and initial page."""

from __future__ import annotations

from PySide6.QtWidgets import QWidget

from ..ui.pages.course_overview_page import CourseOverviewPage
from .models import CourseRegistration


class DM847Page(CourseOverviewPage):
    """Initial bioinformatics page with a course-specific future structure."""

    def __init__(self) -> None:
        super().__init__(
            code="DM847",
            ects=10,
            summary=(
                "Modelos y algoritmos para secuencias, motivos, HMM, índices, "
                "NGS, redes y datos ómicos."
            ),
            planned_sections=(
                "Contexto biológico de cada problema",
                "Modelo formal y supuestos",
                "Algoritmo, pseudocódigo y complejidad",
                "Implementación sobre ejemplos pequeños",
                "Interpretación biomédica y limitaciones",
            ),
        )


def create_page() -> QWidget:
    """Create the DM847 page without constructing widgets during import."""
    return DM847Page()


COURSE = CourseRegistration(
    code="DM847",
    title="Introduction to Bioinformatics",
    ects=10,
    semester=1,
    summary="Algoritmos, secuencias, modelos probabilísticos, redes y ómicas.",
    page_factory=create_page,
)
