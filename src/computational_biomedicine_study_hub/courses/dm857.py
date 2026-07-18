"""DM857 course registration and authored-module reader."""

from __future__ import annotations

from PySide6.QtWidgets import QVBoxLayout, QWidget

from ..content.dm857 import EXTRA_CLOSED_ASSESSMENT_ITEMS, MODULE_01_FOUNDATIONS
from ..learning.assessment_session import SUPPORTED_ACTIVITY_TYPES
from ..ui.pages.module_reader_page import ModuleReaderPage
from .models import CourseRegistration


class DM857Page(QWidget):
    """Host the independently authored modules for Introduction to Programming."""

    def __init__(self) -> None:
        super().__init__()
        self.setObjectName("dm857CoursePage")

        authored_closed_items = tuple(
            item
            for item in MODULE_01_FOUNDATIONS.assessment_items
            if item.activity_type in SUPPORTED_ACTIVITY_TYPES
        )
        assessment_bank = authored_closed_items + EXTRA_CLOSED_ASSESSMENT_ITEMS

        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        self._reader = ModuleReaderPage(
            MODULE_01_FOUNDATIONS,
            assessment_bank=assessment_bank,
        )
        layout.addWidget(self._reader, 1)

    @property
    def reader(self) -> ModuleReaderPage:
        """Return the active module reader."""
        return self._reader


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
