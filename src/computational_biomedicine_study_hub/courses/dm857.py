"""DM857 course registration and authored-module reader."""

from __future__ import annotations

from PySide6.QtWidgets import QFrame, QLabel, QPushButton, QVBoxLayout, QWidget

from ..content.dm857 import MODULE_01_FOUNDATIONS
from ..ui.pages.module_reader_page import ModuleReaderPage
from .models import CourseRegistration


class DM857Page(QWidget):
    """Host the independently authored modules for Introduction to Programming."""

    def __init__(self) -> None:
        super().__init__()
        self.setObjectName("dm857CoursePage")

        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(16)

        layout.addWidget(self._build_course_card())

        module_heading = QLabel("Módulos disponibles")
        module_heading.setObjectName("sectionHeading")
        layout.addWidget(module_heading)

        self._module_button = QPushButton(f"Módulo 1 · {MODULE_01_FOUNDATIONS.title}")
        self._module_button.setObjectName("moduleSelectorButton")
        self._module_button.setCheckable(True)
        self._module_button.setChecked(True)
        self._module_button.setEnabled(False)
        layout.addWidget(self._module_button)

        self._reader = ModuleReaderPage(MODULE_01_FOUNDATIONS)
        layout.addWidget(self._reader, 1)

    @property
    def reader(self) -> ModuleReaderPage:
        """Return the active module reader."""
        return self._reader

    @staticmethod
    def _build_course_card() -> QFrame:
        card = QFrame()
        card.setObjectName("courseIdentityCard")
        card_layout = QVBoxLayout(card)
        card_layout.setContentsMargins(20, 18, 20, 18)
        card_layout.setSpacing(7)

        code = QLabel("DM857 · 10 ECTS")
        code.setObjectName("courseCode")
        card_layout.addWidget(code)

        summary = QLabel(
            "Programación estructurada en Python, resolución de problemas, estructuras "
            "de datos, recursión, abstracción, testing y depuración."
        )
        summary.setObjectName("courseSummary")
        summary.setWordWrap(True)
        card_layout.addWidget(summary)
        return card


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
