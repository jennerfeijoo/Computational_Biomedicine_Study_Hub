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
from ..i18n import MessageKey, Translator
from .routes import RouteId, RouteLike, route_value


@dataclass(frozen=True, slots=True)
class NavigationEntry:
    """One visible item in the sidebar."""

    route: str
    label: str
    section: str


def build_navigation(
    courses: Iterable[CourseRegistration],
    translator: Translator | None = None,
) -> tuple[NavigationEntry, ...]:
    """Build localized navigation without hard-coding future semesters."""
    active_translator = translator or Translator()
    entries: list[NavigationEntry] = [
        NavigationEntry(
            RouteId.HOME.value,
            active_translator.text(MessageKey.NAV_HOME),
            active_translator.text(MessageKey.NAV_GENERAL),
        )
    ]

    semester_ordered_courses = sorted(courses, key=lambda course: course.semester)
    for course in semester_ordered_courses:
        entries.append(
            NavigationEntry(
                course.route,
                course.navigation_label_for(active_translator.locale),
                active_translator.text(MessageKey.NAV_SEMESTER, semester=course.semester),
            )
        )

    learning = active_translator.text(MessageKey.NAV_LEARNING)
    entries.extend(
        [
            NavigationEntry(
                RouteId.REVIEW.value,
                active_translator.text(MessageKey.NAV_REVIEW),
                learning,
            ),
            NavigationEntry(
                RouteId.ASSESSMENTS.value,
                active_translator.text(MessageKey.NAV_ASSESSMENTS),
                learning,
            ),
            NavigationEntry(
                RouteId.FLASHCARDS.value,
                active_translator.text(MessageKey.NAV_FLASHCARDS),
                learning,
            ),
            NavigationEntry(
                RouteId.GLOSSARY.value,
                active_translator.text(MessageKey.NAV_GLOSSARY),
                active_translator.text(MessageKey.NAV_RESOURCES),
            ),
            NavigationEntry(
                RouteId.SETTINGS.value,
                active_translator.text(MessageKey.NAV_SETTINGS),
                active_translator.text(MessageKey.NAV_SYSTEM),
            ),
        ]
    )
    return tuple(entries)


class NavigationSidebar(QWidget):
    """Render grouped navigation entries and support immediate retranslation."""

    route_selected = Signal(str)

    def __init__(
        self,
        courses: Iterable[CourseRegistration],
        translator: Translator | None = None,
        parent: QWidget | None = None,
    ) -> None:
        super().__init__(parent)
        self.setObjectName("navigationSidebar")
        self.setFixedWidth(320)
        self._courses = tuple(courses)
        self._buttons: dict[str, QPushButton] = {}
        self._button_group = QButtonGroup(self)
        self._button_group.setExclusive(True)

        root_layout = QVBoxLayout(self)
        root_layout.setContentsMargins(16, 20, 16, 20)
        root_layout.setSpacing(6)

        self._product_name = QLabel()
        self._product_name.setObjectName("productName")
        root_layout.addWidget(self._product_name)

        scroll = QScrollArea()
        scroll.setObjectName("navigationScroll")
        scroll.setWidgetResizable(True)
        scroll.setFrameShape(QFrame.Shape.NoFrame)

        self._container = QWidget()
        self._container.setObjectName("navigationContainer")
        self._layout = QVBoxLayout(self._container)
        self._layout.setContentsMargins(0, 0, 0, 0)
        self._layout.setSpacing(6)
        scroll.setWidget(self._container)
        root_layout.addWidget(scroll, 1)

        self.retranslate(translator or Translator())

    def retranslate(self, translator: Translator) -> None:
        """Rebuild visible labels while preserving stable routes."""
        active_route = next(
            (route for route, button in self._buttons.items() if button.isChecked()),
            RouteId.HOME.value,
        )
        self._clear_entries()
        self._product_name.setText(translator.text(MessageKey.PRODUCT_NAME))
        self._button_group = QButtonGroup(self)
        self._button_group.setExclusive(True)

        current_section = ""
        for entry in build_navigation(self._courses, translator):
            if entry.section != current_section:
                current_section = entry.section
                section_label = QLabel(current_section)
                section_label.setObjectName("navigationSection")
                self._layout.addWidget(section_label)

            button = QPushButton(entry.label)
            button.setObjectName("navigationButton")
            button.setCheckable(True)
            button.setToolTip(entry.label)
            button.clicked.connect(
                lambda checked=False, route=entry.route: self.route_selected.emit(route)
            )
            self._button_group.addButton(button)
            self._buttons[entry.route] = button
            self._layout.addWidget(button)

        self._layout.addStretch(1)
        self.set_active_route(active_route)

    def set_active_route(self, route: RouteLike) -> None:
        """Reflect the current route in the sidebar selection."""
        button = self._buttons.get(route_value(route))
        if button is not None:
            button.setChecked(True)

    def _clear_entries(self) -> None:
        self._buttons.clear()
        while self._layout.count():
            item = self._layout.takeAt(0)
            if item is None:
                break
            widget = item.widget()
            if widget is not None:
                widget.setParent(None)
                widget.deleteLater()
        self._button_group.deleteLater()
