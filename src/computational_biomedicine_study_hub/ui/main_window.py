"""Main application window, navigation shell and immediate language switching."""

from __future__ import annotations

from pathlib import Path

from PySide6.QtCore import QByteArray, QSettings, Slot
from PySide6.QtGui import QCloseEvent
from PySide6.QtWidgets import (
    QHBoxLayout,
    QMainWindow,
    QStackedWidget,
    QVBoxLayout,
    QWidget,
)

from ..courses import COURSES, CourseRegistration
from ..courses.dm857 import DM857Page
from ..i18n import (
    AppLocale,
    LanguageController,
    MessageKey,
)
from ..learning.academic_catalog import AcademicCatalog
from ..learning.progress_repository import ProgressRepository
from ..persistence import SQLiteProgressRepository, default_progress_database_path
from .header import PageHeader
from .language_styles import LANGUAGE_STYLESHEET
from .navigation import NavigationSidebar
from .pages.assessments_page import AssessmentsPage
from .pages.flashcards_page import FlashcardsPage
from .pages.glossary_page import GlossaryPage
from .pages.home_page import HomePage
from .pages.ollama_settings_page import OllamaSettingsPage
from .pages.review_page import ReviewPage
from .routes import (
    PageDescriptor,
    RouteId,
    RouteLike,
    localized_page_descriptors,
    route_value,
)
from .styles import APPLICATION_STYLESHEET


class MainWindow(QMainWindow):
    """Provide localized navigation, course hosting and lightweight persistence."""

    def __init__(
        self,
        parent: QWidget | None = None,
        *,
        settings: QSettings | None = None,
        progress_repository: ProgressRepository | None = None,
    ) -> None:
        super().__init__(parent)
        self.resize(1200, 760)
        self.setMinimumSize(960, 640)
        self.setStyleSheet(APPLICATION_STYLESHEET + LANGUAGE_STYLESHEET)

        self._settings = settings if settings is not None else QSettings()
        if progress_repository is not None:
            self._progress = progress_repository
        else:
            database_path = (
                Path(self._settings.fileName()).parent / "progress.sqlite3"
                if settings is not None
                else default_progress_database_path()
            )
            self._progress = SQLiteProgressRepository(database_path)
        self._language = LanguageController(self._settings, self)
        self._translator = self._language.translator
        self._courses: tuple[CourseRegistration, ...] = COURSES
        self._pages: dict[str, QWidget] = {}
        self._descriptors: dict[str, PageDescriptor] = localized_page_descriptors(self._translator)

        self._navigation = NavigationSidebar(self._courses, self._translator)
        self._navigation.route_selected.connect(self._on_route_selected)
        self._header = PageHeader(self._language.locale)
        self._header.language_selected.connect(self._language.set_locale)
        self._language.locale_changed.connect(self._apply_locale)
        self._stack = QStackedWidget()
        self._stack.setObjectName("mainPageStack")

        content = QWidget()
        content_layout = QVBoxLayout(content)
        content_layout.setContentsMargins(28, 24, 28, 24)
        content_layout.setSpacing(20)
        content_layout.addWidget(self._header)
        content_layout.addWidget(self._stack, 1)

        shell = QWidget()
        shell_layout = QHBoxLayout(shell)
        shell_layout.setContentsMargins(0, 0, 0, 0)
        shell_layout.setSpacing(0)
        shell_layout.addWidget(self._navigation)
        shell_layout.addWidget(content, 1)
        self.setCentralWidget(shell)

        self._set_window_title()
        self._register_pages()
        self._restore_window_state()
        self.navigate(self._stored_route())

    @property
    def current_route(self) -> RouteId | str:
        """Return the route associated with the current page."""
        current = self._stack.currentWidget()
        for route, page in self._pages.items():
            if page is current:
                try:
                    return RouteId(route)
                except ValueError:
                    return route
        return RouteId.HOME

    @property
    def current_locale(self) -> AppLocale:
        """Return the active persisted application locale."""
        return self._language.locale

    @property
    def progress_repository(self) -> ProgressRepository:
        """Return the long-lived repository shared across page rebuilds."""
        return self._progress

    def navigate(self, route: RouteLike) -> None:
        """Switch to a registered route and persist the selection."""
        key = route_value(route)
        page = self._pages.get(key)
        if page is None:
            key = RouteId.HOME.value
            page = self._pages[key]

        descriptor = self._descriptors[key]
        self._stack.setCurrentWidget(page)
        self._header.set_text(descriptor.title, descriptor.subtitle)
        self._navigation.set_active_route(key)
        self._settings.setValue("navigation/last_route", key)

    def closeEvent(self, event: QCloseEvent) -> None:  # noqa: N802
        """Persist geometry before the window closes."""
        self._settings.setValue("window/geometry", self.saveGeometry())
        super().closeEvent(event)

    def _register_pages(self) -> None:
        locale = self._language.locale
        catalog = AcademicCatalog(locale=locale)
        home_page = HomePage(self._courses, self._translator)
        home_page.course_selected.connect(self.navigate)
        glossary_page = GlossaryPage(catalog, locale=locale)
        glossary_page.module_requested.connect(self._open_catalog_module)

        pages: dict[str, QWidget] = {
            RouteId.HOME.value: home_page,
            RouteId.REVIEW.value: ReviewPage(
                catalog,
                self._progress,
                locale=locale,
            ),
            RouteId.ASSESSMENTS.value: AssessmentsPage(
                catalog,
                self._progress,
                locale=locale,
            ),
            RouteId.FLASHCARDS.value: FlashcardsPage(
                catalog,
                self._progress,
                locale=locale,
            ),
            RouteId.GLOSSARY.value: glossary_page,
            RouteId.SETTINGS.value: OllamaSettingsPage(
                settings=self._settings,
                locale=locale,
            ),
        }

        for course in self._courses:
            pages[course.route] = (
                DM857Page(locale, progress_repository=self._progress)
                if course.code == "DM857"
                else course.page_factory(locale)
            )
            self._descriptors[course.route] = PageDescriptor(
                route=course.route,
                title=f"{course.code} — {course.title_for(locale)}",
                subtitle=course.summary_for(locale),
            )

        for route, page in pages.items():
            self._pages[route] = page
            self._stack.addWidget(page)

    @Slot(str)
    def _apply_locale(self, locale_code: str) -> None:
        """Rebuild visible pages immediately while preserving study location."""
        route = route_value(self.current_route)
        dm857_state = self._capture_dm857_state(route)

        self._header.set_locale(locale_code)
        self._navigation.retranslate(self._translator)
        self._descriptors = localized_page_descriptors(self._translator)
        self._clear_pages()
        self._register_pages()
        self._set_window_title()
        self.navigate(route)
        self._restore_dm857_state(route, dm857_state)

    def _capture_dm857_state(self, route: str) -> tuple[int, int] | None:
        dm857_route = next(
            (course.route for course in self._courses if course.code == "DM857"),
            "",
        )
        if route != dm857_route:
            return None
        page = self._pages.get(route)
        if not isinstance(page, DM857Page):
            return None
        return page.current_module_index, page.reader.current_section_index

    def _restore_dm857_state(
        self,
        route: str,
        state: tuple[int, int] | None,
    ) -> None:
        if state is None:
            return
        page = self._pages.get(route)
        if not isinstance(page, DM857Page):
            return
        module_index, section_index = state
        page.select_module(module_index)
        page.reader.select_section_index(section_index)

    def _clear_pages(self) -> None:
        self._pages.clear()
        while self._stack.count():
            page = self._stack.widget(0)
            if page is None:
                break
            self._stack.removeWidget(page)
            page.deleteLater()

    def _set_window_title(self) -> None:
        self.setWindowTitle(self._translator.text(MessageKey.APP_NAME))

    def _on_route_selected(self, selected_route: str) -> None:
        self.navigate(selected_route)

    @Slot(str, str)
    def _open_catalog_module(self, course_code: str, module_id: str) -> None:
        course = next(
            (item for item in self._courses if item.code == course_code),
            None,
        )
        if course is None:
            return
        self.navigate(course.route)
        page = self._pages.get(course.route)
        if isinstance(page, DM857Page):
            page.select_module_id(module_id)

    def _stored_route(self) -> str:
        value = str(
            self._settings.value(
                "navigation/last_route",
                RouteId.HOME.value,
            )
        )
        if value in self._pages:
            return value
        return RouteId.HOME.value

    def _restore_window_state(self) -> None:
        geometry = self._settings.value("window/geometry")
        if isinstance(geometry, QByteArray):
            self.restoreGeometry(geometry)
