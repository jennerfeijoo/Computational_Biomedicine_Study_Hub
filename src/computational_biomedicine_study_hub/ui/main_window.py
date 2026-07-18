"""Main application window and navigation shell."""

from __future__ import annotations

from PySide6.QtCore import QByteArray, QSettings
from PySide6.QtGui import QCloseEvent
from PySide6.QtWidgets import QHBoxLayout, QMainWindow, QStackedWidget, QVBoxLayout, QWidget

from .header import PageHeader
from .navigation import NavigationSidebar
from .pages.home_page import HomePage
from .pages.placeholder_page import PlaceholderPage
from .routes import PAGE_DESCRIPTORS, RouteId
from .styles import APPLICATION_STYLESHEET


class MainWindow(QMainWindow):
    """Provide stable navigation, page hosting and lightweight persistence."""

    def __init__(self, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self.setWindowTitle("Computational Biomedicine Study Hub")
        self.resize(1200, 760)
        self.setMinimumSize(960, 640)
        self.setStyleSheet(APPLICATION_STYLESHEET)

        self._settings = QSettings()
        self._pages: dict[RouteId, QWidget] = {}

        self._navigation = NavigationSidebar()
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
    def current_route(self) -> RouteId:
        """Return the route associated with the current page."""
        current = self._stack.currentWidget()
        for route, page in self._pages.items():
            if page is current:
                return route
        return RouteId.HOME

    def navigate(self, route: RouteId) -> None:
        """Switch to a registered route and persist the selection."""
        page = self._pages.get(route)
        if page is None:
            route = RouteId.HOME
            page = self._pages[route]

        descriptor = PAGE_DESCRIPTORS[route]
        self._stack.setCurrentWidget(page)
        self._header.set_text(descriptor.title, descriptor.subtitle)
        self._navigation.set_active_route(route)
        self._settings.setValue("navigation/last_route", route.value)

    def closeEvent(self, event: QCloseEvent) -> None:  # noqa: N802
        """Persist geometry before the window closes."""
        self._settings.setValue("window/geometry", self.saveGeometry())
        super().closeEvent(event)

    def _register_pages(self) -> None:
        pages: dict[RouteId, QWidget] = {
            RouteId.HOME: HomePage(),
            RouteId.REVIEW: PlaceholderPage(
                "El motor de repaso incorporará recuperación activa, intercalado y repetición espaciada."
            ),
            RouteId.ASSESSMENTS: PlaceholderPage(
                "Las evaluaciones incluirán opción múltiple, selección múltiple, rellenar espacios, "
                "relacionar elementos, ordenar pasos, código y explicación oral."
            ),
            RouteId.FLASHCARDS: PlaceholderPage(
                "Las tarjetas cubrirán conceptos, fórmulas, código, errores frecuentes y conexiones entre asignaturas."
            ),
            RouteId.GLOSSARY: PlaceholderPage(
                "El glosario se poblará junto con cada módulo académico."
            ),
            RouteId.SETTINGS: PlaceholderPage(
                "Aquí se configurarán preferencias e integraciones locales como Ollama."
            ),
        }

        for route, page in pages.items():
            self._pages[route] = page
            self._stack.addWidget(page)

    def _on_route_selected(self, route_value: str) -> None:
        try:
            route = RouteId(route_value)
        except ValueError:
            route = RouteId.HOME
        self.navigate(route)

    def _stored_route(self) -> RouteId:
        value = self._settings.value("navigation/last_route", RouteId.HOME.value)
        try:
            return RouteId(str(value))
        except ValueError:
            return RouteId.HOME

    def _restore_window_state(self) -> None:
        geometry = self._settings.value("window/geometry")
        if isinstance(geometry, QByteArray):
            self.restoreGeometry(geometry)
