from __future__ import annotations

from pathlib import Path

from PySide6.QtWidgets import QApplication, QLabel

from computational_biomedicine_study_hub import __version__
from computational_biomedicine_study_hub.academic import AcademicContentError
from computational_biomedicine_study_hub.application import (
    ContentErrorWindow,
    create_application,
)
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


def test_packaged_content_error_is_understandable_and_traceable(qapp: QApplication) -> None:
    error = AcademicContentError(Path("broken.yaml"), "line 3: invalid mapping")
    window = ContentErrorWindow(error)

    detail = window.findChild(QLabel, "contentErrorDetail")
    assert detail is not None
    assert "could not be loaded" in detail.text()
    assert "broken.yaml" in detail.text()
    assert "line 3" in detail.text()
