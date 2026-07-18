"""Sidebar navigation for the application shell."""

from __future__ import annotations

from collections.abc import Iterable
from dataclasses import dataclass

from PySide6.QtCore import Signal
from PySide6.QtWidgets import (
    QButtonGroup,
    QFrame,
    QLabel,
    QPushButton,
    QScrollArea,
    QVBoxLayout,
    QWidget,
)

from ..courses.models import CourseRegistration
from .routes import RouteId, RouteLike, route_value


@dataclass(frozen=True, slots=True)
class NavigationEntry:
    """One visible item in the sidebar."""

    route: str
    label: str
    section: str


def build_navigation(
    courses: Iterable[CourseRegistration],
) -> tuple[NavigationEntry, ...]:
    """Build navigation without hard-coding future semesters into the widget."""
    entries: list[NavigationEntry] = [NavigationEntry(RouteId.HOME.value, "Inicio", "GENERAL")]

    semester_ordered_courses = sorted(
        courses,
        key=lambda course: course.semester,
    )
    for course in semester_ordered_courses:
        entries.append(
            NavigationEntry(
                course.route,
                course.navigation_label,
                f"SEMESTRE {course.semester}",
            )
        )

    entries.extend(
        [
            NavigationEntry(RouteId.REVIEW.value, "Repaso", "APRENDIZAJE"),
            NavigationEntry(
                RouteId.ASSESSMENTS.value,
                "Evaluaciones",
                "APRENDIZAJE",
            ),
            NavigationEntry(
                RouteId.FLASHCARDS.value,
                "Tarjetas de memoria",
                "APRENDIZAJE",
            ),
            NavigationEntry(RouteId.GLOSSARY.value, "Glosario", "RECURSOS"),
            NavigationEntry(
                RouteId.SETTINGS.value,
                "Configuración",
                "SISTEMA",
            ),
        ]
    )
    return tuple(entries)


class NavigationSidebar(QWidget):
    """Render grouped navigation entries and emit stable route identifiers."""

    route_selected = Signal(str)

    def __init__(
        self,
        courses: Iterable[CourseRegistration],
        parent: QWidget | None = None,
    ) -> None:
        super().__init__(parent)
        self.setObjectName("navigationSidebar")
        self.setFixedWidth(320)

        self._buttons: dict[str, QPushButton] = {}
        self._button_group = QButtonGroup(self)
        self._button_group.setExclusive(True)

        root_layout = QVBoxLayout(self)
        root_layout.setContentsMargins(16, 20, 16, 20)
        root_layout.setSpacing(6)

        product_name = QLabel("Computational\nBiomedicine Hub")
        product_name.setObjectName("productName")
        root_layout.addWidget(product_name)

        scroll = QScrollArea()
        scroll.setObjectName("navigationScroll")
        scroll.setWidgetResizable(True)
        scroll.setFrameShape(QFrame.Shape.NoFrame)

        container = QWidget()
        container.setObjectName("navigationContainer")
        layout = QVBoxLayout(container)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(6)

        current_section = ""
        for entry in build_navigation(courses):
            if entry.section != current_section:
                current_section = entry.section
                section_label = QLabel(current_section)
                section_label.setObjectName("navigationSection")
                layout.addWidget(section_label)

            button = QPushButton(entry.label)
            button.setObjectName("navigationButton")
            button.setCheckable(True)
            button.setToolTip(entry.label)
            button.clicked.connect(
                lambda checked=False, route=entry.route: self.route_selected.emit(route)
            )
            self._button_group.addButton(button)
            self._buttons[entry.route] = button
            layout.addWidget(button)

        layout.addStretch(1)
        scroll.setWidget(container)
        root_layout.addWidget(scroll, 1)

    def set_active_route(self, route: RouteLike) -> None:
        """Reflect the current route in the sidebar selection."""
        button = self._buttons.get(route_value(route))
        if button is not None:
            button.setChecked(True)
