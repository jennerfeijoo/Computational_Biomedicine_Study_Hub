"""Main application window, navigation shell and immediate preferences."""

from __future__ import annotations

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
from ..courses.dm847 import DM847Page
from ..courses.dm857 import DM857Page
from ..i18n import (
    AppLocale,
    LanguageController,
    MessageKey,
    UiCopyKey,
    ui_text,
)
from ..storage import SQLiteProgressStore
from .header import PageHeader
from .navigation import NavigationSidebar
from .pages.assessments_page import AssessmentsPage
from .pages.home_page import HomePage
from .pages.ollama_settings_page import OllamaSettingsPage
from .pages.placeholder_page import PlaceholderPage
from .pages.resumable_review_page import ReviewPage
from .routes import (
    PageDescriptor,
    RouteId,
    RouteLike,
    localized_page_descriptors,
    route_value,
)
from .styles import build_application_stylesheet
from .theme import AppearanceMode, ThemeController, VisualTheme

ModularCoursePage = DM847Page | DM857Page
StudyLocation = tuple[int, int]


class MainWindow(QMainWindow):
    """Provide localized navigation, themed course hosting and learning-state access."""

    def __init__(
        self,
        parent: QWidget | None = None,
        *,
        settings: QSettings | None = None,
        progress_store: SQLiteProgressStore | None = None,
    ) -> None:
        super().__init__(parent)
        self.resize(1200, 760)
        self.setMinimumSize(960, 640)

        self._settings = settings if settings is not None else QSettings()
        self._progress_store = progress_store
        self._theme = ThemeController(self._settings, self)
        self._theme.theme_changed.connect(self._apply_theme)
        self._apply_theme(self._theme.theme.value)
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
        content.setObjectName("mainContentArea")
        content_layout = QVBoxLayout(content)
        content_layout.setContentsMargins(28, 24, 28, 24)
        content_layout.setSpacing(20)
        content_layout.addWidget(self._header)
        content_layout.addWidget(self._stack, 1)

        shell = QWidget()
        shell.setObjectName("applicationShell")
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
    def current_appearance(self) -> AppearanceMode:
        """Return the persisted appearance preference."""

        return self._theme.mode

    @property
    def current_theme(self) -> VisualTheme:
        """Return the concrete theme currently rendered by the shell."""

        return self._theme.theme

    @property
    def theme_controller(self) -> ThemeController:
        """Return the shared application-wide appearance controller."""

        return self._theme

    def set_appearance(self, mode: AppearanceMode | str) -> bool:
        """Apply and persist a new appearance preference immediately."""

        return self._theme.set_mode(mode)

    def navigate(self, route: RouteLike) -> None:
        """Switch to a registered route and persist the selection."""

        key = route_value(route)
        page = self._pages.get(key)
        if page is None:
            key = RouteId.HOME.value
            page = self._pages[key]

        if isinstance(page, ReviewPage):
            page.refresh()

        descriptor = self._descriptors[key]
        self._stack.setCurrentWidget(page)
        self._header.set_text(descriptor.title, descriptor.subtitle)
        self._navigation.set_active_route(key)
        self._settings.setValue("navigation/last_route", key)

    def closeEvent(self, event: QCloseEvent) -> None:  # noqa: N802
        """Persist geometry and active learner work before the window closes."""

        self._persist_review_session()
        self._persist_assessments()
        self._settings.setValue("window/geometry", self.saveGeometry())
        super().closeEvent(event)

    def _register_pages(self) -> None:
        locale = self._language.locale
        home_page = HomePage(self._courses, self._translator)
        home_page.course_selected.connect(self.navigate)

        review_page = ReviewPage(self._progress_store, locale)
        review_page.review_requested.connect(self._open_review_item)

        pages: dict[str, QWidget] = {
            RouteId.HOME.value: home_page,
            RouteId.REVIEW.value: review_page,
            RouteId.ASSESSMENTS.value: AssessmentsPage(
                self._progress_store,
                locale,
                settings=self._settings,
            ),
            RouteId.FLASHCARDS.value: PlaceholderPage(
                ui_text(locale, UiCopyKey.FLASHCARDS_PLACEHOLDER)
            ),
            RouteId.GLOSSARY.value: PlaceholderPage(
                ui_text(locale, UiCopyKey.GLOSSARY_PLACEHOLDER)
            ),
            RouteId.SETTINGS.value: OllamaSettingsPage(
                settings=self._settings,
                locale=locale,
                theme_controller=self._theme,
            ),
        }

        for course in self._courses:
            pages[course.route] = course.page_factory(locale)
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
        """Rebuild visible pages immediately while preserving study and learner state."""

        route = route_value(self.current_route)
        study_location = self._capture_study_location(route)
        self._persist_review_session()
        self._persist_assessments()

        self._header.set_locale(locale_code)
        self._navigation.retranslate(self._translator)
        self._descriptors = localized_page_descriptors(self._translator)
        self._clear_pages()
        self._register_pages()
        self._set_window_title()
        self.navigate(route)
        self._restore_study_location(route, study_location)

    @Slot(str)
    def _apply_theme(self, theme_value: str) -> None:
        """Render the selected semantic palette without rebuilding page state."""

        theme = VisualTheme(theme_value)
        self.setProperty("visualTheme", theme.value)
        self.setStyleSheet(build_application_stylesheet(theme))

    def _capture_study_location(self, route: str) -> StudyLocation | None:
        page = self._modular_course_page(route)
        if page is None:
            return None
        return page.current_module_index, page.reader.current_section_index

    def _restore_study_location(
        self,
        route: str,
        state: StudyLocation | None,
    ) -> None:
        if state is None:
            return
        page = self._modular_course_page(route)
        if page is None:
            return
        module_index, section_index = state
        page.select_module(module_index)
        page.reader.select_section_index(section_index)

    def _modular_course_page(self, route: str) -> ModularCoursePage | None:
        page = self._pages.get(route)
        if isinstance(page, (DM847Page, DM857Page)):
            return page
        return None

    def _persist_review_session(self) -> None:
        page = self._pages.get(RouteId.REVIEW.value)
        if isinstance(page, ReviewPage):
            page.persist_active_session()

    def _persist_assessments(self) -> None:
        page = self._pages.get(RouteId.ASSESSMENTS.value)
        if isinstance(page, AssessmentsPage):
            page.persist()

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

    @Slot(str, str, str)
    def _open_review_item(
        self,
        course_code: str,
        module_id: str,
        objective_id: str,
    ) -> None:
        """Open the authored module and its assessment section for retrieval practice."""

        del objective_id
        route = f"course/{course_code.casefold()}"
        self.navigate(route)
        page = self._modular_course_page(route)
        if page is None or not page.select_module_by_id(module_id):
            return
        page.reader.select_section_index(4)

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
