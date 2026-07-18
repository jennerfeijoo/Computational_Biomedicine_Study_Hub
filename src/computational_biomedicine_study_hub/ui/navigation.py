"""Sidebar navigation for the application shell."""

from __future__ import annotations

from dataclasses import dataclass

from PySide6.QtCore import Signal
from PySide6.QtWidgets import QButtonGroup, QLabel, QPushButton, QVBoxLayout, QWidget

from .routes import RouteId


@dataclass(frozen=True, slots=True)
class NavigationEntry:
    """One visible item in the sidebar."""

    route: RouteId
    label: str
    section: str


DEFAULT_NAVIGATION: tuple[NavigationEntry, ...] = (
    NavigationEntry(RouteId.HOME, "Inicio", "GENERAL"),
    NavigationEntry(RouteId.REVIEW, "Repaso", "APRENDIZAJE"),
    NavigationEntry(RouteId.ASSESSMENTS, "Evaluaciones", "APRENDIZAJE"),
    NavigationEntry(RouteId.FLASHCARDS, "Tarjetas de memoria", "APRENDIZAJE"),
    NavigationEntry(RouteId.GLOSSARY, "Glosario", "RECURSOS"),
    NavigationEntry(RouteId.SETTINGS, "Configuración", "SISTEMA"),
)


class NavigationSidebar(QWidget):
    """Render grouped navigation entries and emit stable route identifiers."""

    route_selected = Signal(str)

    def __init__(self, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self.setObjectName("navigationSidebar")
        self.setFixedWidth(260)

        self._buttons: dict[RouteId, QPushButton] = {}
        self._button_group = QButtonGroup(self)
        self._button_group.setExclusive(True)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(16, 20, 16, 20)
        layout.setSpacing(6)

        product_name = QLabel("Computational\nBiomedicine Hub")
        product_name.setObjectName("productName")
        layout.addWidget(product_name)

        current_section = ""
        for entry in DEFAULT_NAVIGATION:
            if entry.section != current_section:
                current_section = entry.section
                section_label = QLabel(current_section)
                section_label.setObjectName("navigationSection")
                layout.addWidget(section_label)

            button = QPushButton(entry.label)
            button.setObjectName("navigationButton")
            button.setCheckable(True)
            button.clicked.connect(
                lambda checked=False, route=entry.route: self.route_selected.emit(route.value)
            )
            self._button_group.addButton(button)
            self._buttons[entry.route] = button
            layout.addWidget(button)

        layout.addStretch(1)

    def set_active_route(self, route: RouteId) -> None:
        """Reflect the current route in the sidebar selection."""
        button = self._buttons.get(route)
        if button is not None:
            button.setChecked(True)
