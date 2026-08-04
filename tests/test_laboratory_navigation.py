"""Navigation regression tests for the laboratory workspace."""

from __future__ import annotations

from PySide6.QtWidgets import QApplication

from computational_biomedicine_study_hub.i18n import Translator
from computational_biomedicine_study_hub.ui.main_window import MainWindow
from computational_biomedicine_study_hub.ui.navigation import build_navigation
from computational_biomedicine_study_hub.ui.routes import RouteId


def test_laboratory_route_is_localized_and_navigable(qapp: QApplication) -> None:
    entries = build_navigation((), Translator())
    laboratory = next(entry for entry in entries if entry.route == RouteId.LABS.value)
    assert laboratory.label

    window = MainWindow()
    window.navigate(RouteId.LABS)
    assert window.current_route is RouteId.LABS
