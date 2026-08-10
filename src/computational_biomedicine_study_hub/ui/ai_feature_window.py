"""Application shell extension that wires the AI study features into existing routes."""

from __future__ import annotations

from pathlib import Path

from PySide6.QtCore import QSettings
from PySide6.QtWidgets import QWidget

from ..storage import AILearningStore, SQLiteProgressStore
from .main_window import MainWindow as BaseMainWindow
from .pages.ai_study_pages import FlashcardsPage
from .pages.smart_assessments_page import SmartAssessmentsPage
from .routes import RouteId


class MainWindow(BaseMainWindow):
    """Existing shell with flashcards and module-aware intelligent assessments."""

    def __init__(
        self,
        parent: QWidget | None = None,
        *,
        settings: QSettings | None = None,
        progress_store: SQLiteProgressStore | None = None,
    ) -> None:
        self._ai_settings = settings if settings is not None else QSettings()
        self._ai_learning_store: AILearningStore | None = None
        if progress_store is not None and progress_store.database != ":memory:":
            database = Path(progress_store.database).with_name("ai_learning.sqlite3")
            self._ai_learning_store = AILearningStore(database)
        super().__init__(parent, settings=settings, progress_store=progress_store)

    def _register_pages(self) -> None:
        """Reuse the base shell and replace the affected routes with real AI pages."""

        super()._register_pages()
        if self._ai_learning_store is None:
            return
        locale = self.current_locale
        self._replace_page(
            RouteId.FLASHCARDS.value,
            FlashcardsPage(self._ai_learning_store, locale),
        )
        self._replace_page(
            RouteId.ASSESSMENTS.value,
            SmartAssessmentsPage(self._ai_learning_store, locale, self._ai_settings),
        )

    def _replace_page(self, route: str, page: QWidget) -> None:
        existing = self._pages.get(route)
        if existing is None:
            self._pages[route] = page
            self._stack.addWidget(page)
            return
        index = self._stack.indexOf(existing)
        if index < 0:
            self._pages[route] = page
            self._stack.addWidget(page)
            return
        self._stack.removeWidget(existing)
        existing.deleteLater()
        self._pages[route] = page
        self._stack.insertWidget(index, page)

    def closeEvent(self, event) -> None:  # noqa: N802
        if self._ai_learning_store is not None:
            self._ai_learning_store.close()
            self._ai_learning_store = None
        super().closeEvent(event)


__all__ = ["MainWindow"]
