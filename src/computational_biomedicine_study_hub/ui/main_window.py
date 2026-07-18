"""Main application window."""

from __future__ import annotations

from PySide6.QtCore import Qt
from PySide6.QtWidgets import QLabel, QMainWindow, QWidget


class MainWindow(QMainWindow):
    """Minimal shell used as the stable base for later navigation work."""

    def __init__(self, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self.setWindowTitle("Computational Biomedicine Study Hub")
        self.resize(1200, 760)
        self.setMinimumSize(960, 640)

        placeholder = QLabel(
            "Computational Biomedicine Study Hub\n\n"
            "Project foundation initialized."
        )
        placeholder.setAlignment(Qt.AlignmentFlag.AlignCenter)
        placeholder.setObjectName("applicationPlaceholder")
        self.setCentralWidget(placeholder)
