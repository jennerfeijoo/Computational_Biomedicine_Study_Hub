"""Application bootstrap and command-line entry point."""

from __future__ import annotations

import sys
from collections.abc import Sequence
from pathlib import Path

from PySide6.QtCore import QStandardPaths
from PySide6.QtWidgets import QApplication

from .courses.dm847 import configure_progress_recorder
from .learning.progress_service import LearningProgressService
from .storage import SQLiteProgressStore
from .ui.main_window import MainWindow

APPLICATION_NAME = "Computational Biomedicine Study Hub"
ORGANIZATION_NAME = "Jenner Feijoo"
ORGANIZATION_DOMAIN = "github.com/jennerfeijoo"
_PROGRESS_DATABASE_NAME = "learning_progress.sqlite3"


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


def progress_database_path() -> Path:
    """Return the writable per-user path for private learning progress."""

    location = QStandardPaths.writableLocation(QStandardPaths.StandardLocation.AppDataLocation)
    directory = Path(location) if location else Path.home() / ".cb-study-hub"
    directory.mkdir(parents=True, exist_ok=True)
    return directory / _PROGRESS_DATABASE_NAME


def main(argv: Sequence[str] | None = None) -> int:
    """Run the desktop application with local learning-state persistence."""

    app = create_application(argv)
    progress_store = SQLiteProgressStore(progress_database_path())
    configure_progress_recorder(LearningProgressService(progress_store))
    app.aboutToQuit.connect(progress_store.close)

    window = MainWindow(progress_store=progress_store)
    window.show()
    return app.exec()
