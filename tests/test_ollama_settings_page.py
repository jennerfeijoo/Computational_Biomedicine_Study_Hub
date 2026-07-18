from __future__ import annotations

from pathlib import Path

from PySide6.QtCore import QSettings
from PySide6.QtWidgets import QApplication, QComboBox

from computational_biomedicine_study_hub.integrations import OllamaModel
from computational_biomedicine_study_hub.ui.main_window import MainWindow
from computational_biomedicine_study_hub.ui.pages.ollama_settings_page import (
    OllamaSettingsPage,
)
from computational_biomedicine_study_hub.ui.routes import RouteId


def make_settings(path: Path) -> QSettings:
    return QSettings(str(path), QSettings.Format.IniFormat)


def test_settings_page_displays_and_persists_a_successful_probe(
    qapp: QApplication,
    tmp_path: Path,
) -> None:
    settings = make_settings(tmp_path / "settings.ini")
    page = OllamaSettingsPage(settings=settings)
    models = (
        OllamaModel(name="ornith:9b"),
        OllamaModel(name="qwen3-embedding:0.6b"),
        OllamaModel(name="qwen3.6:27b"),
    )

    page.apply_probe_success("0.32.1", models)

    selector = page.findChild(QComboBox, "ollamaModelSelector")
    assert selector is not None
    assert selector.isEnabled()
    assert selector.count() == 3
    assert "0.32.1" not in page.status_text
    assert "3 modelos" in page.status_text

    selector.setCurrentText("qwen3.6:27b")
    page.save_preferences()

    assert settings.value(OllamaSettingsPage.MODEL_KEY) == "qwen3.6:27b"
    assert settings.value(OllamaSettingsPage.BASE_URL_KEY) == (
        "http://localhost:11434/api"
    )


def test_settings_page_surfaces_connection_failures(
    qapp: QApplication,
    tmp_path: Path,
) -> None:
    page = OllamaSettingsPage(
        settings=make_settings(tmp_path / "settings.ini")
    )

    page.apply_probe_failure("No se pudo conectar con Ollama.")

    assert page.status_text == "No se pudo conectar con Ollama."
    assert page.selected_model == ""


def test_main_window_registers_the_real_ollama_settings_page(
    qapp: QApplication,
) -> None:
    window = MainWindow()

    window.navigate(RouteId.SETTINGS)

    assert window.current_route is RouteId.SETTINGS
    assert window.findChild(OllamaSettingsPage, "ollamaSettingsPage") is not None
