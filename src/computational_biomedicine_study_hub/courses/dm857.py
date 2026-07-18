"""DM857 course registration and initial page."""

from __future__ import annotations

from PySide6.QtWidgets import QWidget

from ..ui.pages.course_overview_page import CourseOverviewPage
from .models import CourseRegistration


class DM857Page(CourseOverviewPage):
    """Initial programming course page; modules will be implemented independently."""

    def __init__(self) -> None:
        super().__init__(
            code="DM857",
            ects=10,
            summary=(
                "Programación estructurada en Python, resolución de problemas, "
                "estructuras de datos, recursión y testing."
            ),
            planned_sections=(
                "Conceptos y pensamiento computacional",
                "Ejemplos de código ejecutables",
                "Resolución guiada de problemas",
                "Testing, depuración y errores frecuentes",
                "Preguntas de explicación oral",
            ),
        )


def create_page() -> QWidget:
    """Create the DM857 page without constructing widgets during import."""
    return DM857Page()


COURSE = CourseRegistration(
    code="DM857",
    title="Introduction to Programming",
    ects=10,
    semester=1,
    summary="Python, pensamiento algorítmico, estructuras de datos y testing.",
    page_factory=create_page,
)
