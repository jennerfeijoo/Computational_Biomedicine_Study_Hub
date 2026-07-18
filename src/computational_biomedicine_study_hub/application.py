"""Application bootstrap and command-line entry point."""

from __future__ import annotations

import sys
from collections.abc import Sequence

from PySide6.QtWidgets import QApplication

from .ui.main_window import MainWindow


def create_application(argv: Sequence[str] | None = None) -> QApplication:
    """Create and configure the Qt application instance."""
    existing = QApplication.instance()
    if isinstance(existing, QApplication):
        return existing

    arguments = list(argv) if argv is not None else sys.argv
    app = QApplication(arguments)
    app.setApplicationName("Computational Biomedicine Study Hub")
    app.setOrganizationName("Jenner Feijoo")
    app.setOrganizationDomain("github.com/jennerfeijoo")
    return app


def main(argv: Sequence[str] | None = None) -> int:
    """Run the desktop application."""
    app = create_application(argv)
    window = MainWindow()
    window.show()
    return app.exec()
