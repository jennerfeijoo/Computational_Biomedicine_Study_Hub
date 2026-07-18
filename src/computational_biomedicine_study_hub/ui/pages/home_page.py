"""Initial dashboard page."""

from __future__ import annotations

from PySide6.QtCore import Qt
from PySide6.QtWidgets import QLabel, QVBoxLayout, QWidget


class HomePage(QWidget):
    """Introduce the semester scope without embedding course content."""

    def __init__(self, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        message = QLabel(
            "La estructura académica se añadirá por asignatura en entregas independientes.\n\n"
            "El sistema combinará teoría condensada, ejemplos resueltos, práctica guiada, "
            "recuperación activa, evaluaciones y revisión espaciada."
        )
        message.setAlignment(Qt.AlignmentFlag.AlignCenter)
        message.setWordWrap(True)
        message.setObjectName("homeMessage")

        layout = QVBoxLayout(self)
        layout.addStretch(1)
        layout.addWidget(message)
        layout.addStretch(1)
