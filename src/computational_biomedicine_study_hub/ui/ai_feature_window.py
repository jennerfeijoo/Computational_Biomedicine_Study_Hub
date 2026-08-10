"""Application shell extension that wires the new AI study features into existing routes."""

from __future__ import annotations

from pathlib import Path

from PySide6.QtCore import QSettings
from PySide6.QtWidgets import QWidget

from ..i18n import AppLocale
from ..storage import AILearningStore, SQLiteProgressStore
from .main_window import MainWindow as BaseMainWindow
from .pages.ai_study_pages import FlashcardsPage, SmartAssessmentsPage
from .routes import RouteId


class MainWindow(BaseMainWindow):
    """Existing shell with real flashcards and intelligent assessment pages."""

    def __init__(
        self,
        parent: QWidget | None = None,
        *,
        settings: QSettings | None = None,
        progress_store: SQLiteProgressStore | None = None,
    ) -> None:
        self._ai_learning_store: AILearningStore | None = None
        if progress_store is not None and progress_store.database != ":memory:":
            database = Path(progress_store.database).with_name("ai_learning.sqlite3")
            self._ai_learning_store = AILearningStore(database)
        super().__init__(parent, settings=settings, progress_store=progress_store)

    def _register_pages(self) -> None:
        """Reuse the base page registration and replace placeholder/legacy assessment routes."""

        super()._register_pages()
        if self._ai_learning_store is None:
            return
        locale = self.current_locale
        flashcards = FlashcardsPage(self._ai_learning_store, locale)
        assessments = SmartAssessmentsPage(self._ai_learning_store, locale)
        self._replace_page(RouteId.FLASHCARDS.value, flashcards)
        self._replace_page(RouteId.ASSESSMENTS.value, assessments)

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
