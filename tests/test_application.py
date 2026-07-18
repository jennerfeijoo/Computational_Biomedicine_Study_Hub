from __future__ import annotations

from PySide6.QtWidgets import QApplication

from computational_biomedicine_study_hub import __version__
from computational_biomedicine_study_hub.application import create_application
from computational_biomedicine_study_hub.ui.main_window import MainWindow


def test_package_version_is_defined() -> None:
    assert __version__ == "0.1.0"


def test_application_metadata(qapp: QApplication) -> None:
    app = create_application([])

    assert app is qapp
    assert app.applicationName() == "Computational Biomedicine Study Hub"
    assert app.organizationName() == "Jenner Feijoo"


def test_main_window_has_stable_initial_geometry(qapp: QApplication) -> None:
    window = MainWindow()

    assert window.windowTitle() == "Computational Biomedicine Study Hub"
    assert window.minimumWidth() == 960
    assert window.minimumHeight() == 640
    assert window.centralWidget() is not None
