"""Reusable placeholder page for features implemented in later increments."""

from __future__ import annotations

from PySide6.QtCore import Qt
from PySide6.QtWidgets import QLabel, QVBoxLayout, QWidget


class PlaceholderPage(QWidget):
    """Reserve a stable route while keeping the implementation incremental."""

    def __init__(self, message: str, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        label = QLabel(message)
        label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        label.setWordWrap(True)
        label.setObjectName("placeholderMessage")

        layout = QVBoxLayout(self)
        layout.addStretch(1)
        layout.addWidget(label)
        layout.addStretch(1)
