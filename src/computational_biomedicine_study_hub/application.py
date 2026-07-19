"""Application bootstrap and command-line entry point."""

from __future__ import annotations

import sys
from collections.abc import Sequence

from PySide6.QtCore import Qt
from PySide6.QtWidgets import QApplication, QLabel, QMainWindow, QVBoxLayout, QWidget

from .academic import AcademicContentError
from .ui.main_window import MainWindow

APPLICATION_NAME = "Computational Biomedicine Study Hub"
ORGANIZATION_NAME = "Jenner Feijoo"
ORGANIZATION_DOMAIN = "github.com/jennerfeijoo"


def _configure_application(app: QApplication) -> None:
    """Apply stable metadata to newly created and reused Qt applications."""
    app.setApplicationName(APPLICATION_NAME)
    app.setOrganizationName(ORGANIZATION_NAME)
    app.setOrganizationDomain(ORGANIZATION_DOMAIN)


def create_application(argv: Sequence[str] | None = None) -> QApplication:
    """Create or reuse the Qt application and apply project metadata."""
    existing = QApplication.instance()
    if isinstance(existing, QApplication):
        _configure_application(existing)
        return existing

    arguments = list(argv) if argv is not None else sys.argv
    app = QApplication(arguments)
    _configure_application(app)
    return app


class ContentErrorWindow(QMainWindow):
    """Keep a packaged application usable enough to explain a corpus failure."""

    def __init__(self, error: Exception) -> None:
        super().__init__()
        self.setWindowTitle(f"{APPLICATION_NAME} — content error")
        self.setMinimumSize(720, 360)
        body = QWidget()
        layout = QVBoxLayout(body)
        title = QLabel("Academic content could not be loaded")
        title.setObjectName("contentErrorTitle")
        detail = QLabel(
            "ES: El contenido académico no pudo cargarse. No se inició una sesión de "
            "estudio.\n\n"
            "EN: Academic content could not be loaded. No study session was started.\n\n"
            "DA: Det faglige indhold kunne ikke indlæses. Ingen studiesession blev "
            "startet.\n\n"
            f"Technical detail:\n{error}"
        )
        detail.setObjectName("contentErrorDetail")
        detail.setWordWrap(True)
        detail.setTextInteractionFlags(Qt.TextInteractionFlag.TextSelectableByMouse)
        layout.addWidget(title)
        layout.addWidget(detail, 1)
        self.setCentralWidget(body)


def main(argv: Sequence[str] | None = None) -> int:
    """Run the desktop application."""
    app = create_application(argv)
    try:
        window: QMainWindow = MainWindow()
    except (AcademicContentError, FileNotFoundError) as error:
        window = ContentErrorWindow(error)
    window.show()
    return app.exec()
