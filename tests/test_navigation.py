from __future__ import annotations

from PySide6.QtWidgets import QApplication

from computational_biomedicine_study_hub.ui.main_window import MainWindow
from computational_biomedicine_study_hub.ui.routes import RouteId


def test_main_window_can_navigate_between_registered_routes(qapp: QApplication) -> None:
    window = MainWindow()

    window.navigate(RouteId.ASSESSMENTS)
    assert window.current_route is RouteId.ASSESSMENTS

    window.navigate(RouteId.FLASHCARDS)
    assert window.current_route is RouteId.FLASHCARDS
