"""Application bootstrap and command-line entry point."""

from __future__ import annotations

import sys
from collections.abc import Sequence

from PySide6.QtWidgets import QApplication

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


def main(argv: Sequence[str] | None = None) -> int:
    """Run the desktop application."""
    app = create_application(argv)
    window = MainWindow()
    window.show()
    return app.exec()
