"""Main application window and navigation shell."""

from __future__ import annotations

from PySide6.QtCore import QByteArray, QSettings
from PySide6.QtGui import QCloseEvent
from PySide6.QtWidgets import (
    QHBoxLayout,
    QMainWindow,
    QStackedWidget,
    QVBoxLayout,
    QWidget,
)

from ..courses import COURSES, CourseRegistration
from .header import PageHeader
from .navigation import NavigationSidebar
from .pages.home_page import HomePage
from .pages.ollama_settings_page import OllamaSettingsPage
from .pages.placeholder_page import PlaceholderPage
from .routes import (
    PAGE_DESCRIPTORS,
    PageDescriptor,
    RouteId,
    RouteLike,
    route_value,
)
from .styles import APPLICATION_STYLESHEET


class MainWindow(QMainWindow):
    """Provide stable navigation, course hosting and lightweight persistence."""

    def __init__(self, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self.setWindowTitle("Computational Biomedicine Study Hub")
        self.resize(1200, 760)
        self.setMinimumSize(960, 640)
        self.setStyleSheet(APPLICATION_STYLESHEET)

        self._settings = QSettings()
        self._courses: tuple[CourseRegistration, ...] = COURSES
        self._pages: dict[str, QWidget] = {}
        self._descriptors: dict[str, PageDescriptor] = dict(PAGE_DESCRIPTORS)

        self._navigation = NavigationSidebar(self._courses)
        self._navigation.route_selected.connect(self._on_route_selected)
        self._header = PageHeader()
        self._stack = QStackedWidget()

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
        home_page = HomePage(self._courses)
        home_page.course_selected.connect(self.navigate)

        pages: dict[str, QWidget] = {
            RouteId.HOME.value: home_page,
            RouteId.REVIEW.value: PlaceholderPage(
                "El motor de repaso incorporará recuperación activa, "
                "intercalado y repetición espaciada."
            ),
            RouteId.ASSESSMENTS.value: PlaceholderPage(
                "Las evaluaciones incluirán opción múltiple, selección múltiple, "
                "rellenar espacios, relacionar elementos, ordenar pasos, código "
                "y explicación oral."
            ),
            RouteId.FLASHCARDS.value: PlaceholderPage(
                "Las tarjetas cubrirán conceptos, fórmulas, código, errores "
                "frecuentes y conexiones entre asignaturas."
            ),
            RouteId.GLOSSARY.value: PlaceholderPage(
                "El glosario se poblará junto con cada módulo académico."
            ),
            RouteId.SETTINGS.value: OllamaSettingsPage(settings=self._settings),
        }

        for course in self._courses:
            pages[course.route] = course.page_factory()
            self._descriptors[course.route] = PageDescriptor(
                route=course.route,
                title=f"{course.code} — {course.title}",
                subtitle=course.summary,
            )

        for route, page in pages.items():
            self._pages[route] = page
            self._stack.addWidget(page)

    def _on_route_selected(self, selected_route: str) -> None:
        self.navigate(selected_route)

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
