from __future__ import annotations

from pathlib import Path

from PySide6.QtCore import QSettings
from PySide6.QtWidgets import QApplication, QPushButton

from computational_biomedicine_study_hub.i18n import (
    AppearanceCopyKey,
    AppLocale,
    appearance_text,
    validate_appearance_copy,
)
from computational_biomedicine_study_hub.ui.main_window import MainWindow
from computational_biomedicine_study_hub.ui.pages.ollama_settings_page import (
    OllamaSettingsPage,
)
from computational_biomedicine_study_hub.ui.routes import RouteId
from computational_biomedicine_study_hub.ui.styles import build_application_stylesheet
from computational_biomedicine_study_hub.ui.theme import (
    DARK_PALETTE,
    LIGHT_PALETTE,
    AppearanceMode,
    ThemeController,
    VisualTheme,
)
from computational_biomedicine_study_hub.ui.widgets import AppearanceSelector


def _settings(path: Path) -> QSettings:
    return QSettings(str(path), QSettings.Format.IniFormat)


def test_appearance_copy_is_complete_and_strict() -> None:
    validate_appearance_copy()

    assert appearance_text(AppLocale.SPANISH_SPAIN, AppearanceCopyKey.DARK) == "Oscuro"
    assert appearance_text(AppLocale.ENGLISH, AppearanceCopyKey.SYSTEM) == "Follow system"
    assert appearance_text(AppLocale.DANISH_DENMARK, AppearanceCopyKey.LIGHT) == "Lyst"


def test_stylesheets_resolve_every_semantic_token_for_both_themes() -> None:
    light = build_application_stylesheet(VisualTheme.LIGHT)
    dark = build_application_stylesheet(VisualTheme.DARK)

    assert "@" not in light
    assert "@" not in dark
    assert LIGHT_PALETTE.window in light
    assert LIGHT_PALETTE.surface in light
    assert DARK_PALETTE.window in dark
    assert DARK_PALETTE.surface in dark
    assert light != dark
    assert 'QPushButton[buttonRole="primary"]' in light
    assert 'QFrame[cardRole="surface"]' in dark


def test_theme_controller_persists_explicit_mode_and_restores_it(tmp_path: Path) -> None:
    settings = _settings(tmp_path / "appearance.ini")
    controller = ThemeController(
        settings,
        system_resolver=lambda: VisualTheme.LIGHT,
    )
    appearance_events: list[str] = []
    theme_events: list[str] = []
    controller.appearance_changed.connect(appearance_events.append)
    controller.theme_changed.connect(theme_events.append)

    assert controller.mode is AppearanceMode.SYSTEM
    assert controller.theme is VisualTheme.LIGHT

    assert controller.set_mode(AppearanceMode.DARK)

    assert settings.value(ThemeController.SETTINGS_KEY) == AppearanceMode.DARK.value
    assert appearance_events == [AppearanceMode.DARK.value]
    assert theme_events == [VisualTheme.DARK.value]

    restored = ThemeController(
        settings,
        system_resolver=lambda: VisualTheme.LIGHT,
    )
    assert restored.mode is AppearanceMode.DARK
    assert restored.theme is VisualTheme.DARK


def test_system_mode_refreshes_only_when_resolved_theme_changes(tmp_path: Path) -> None:
    settings = _settings(tmp_path / "system-theme.ini")
    current = [VisualTheme.LIGHT]
    controller = ThemeController(settings, system_resolver=lambda: current[0])
    events: list[str] = []
    controller.theme_changed.connect(events.append)

    assert not controller.refresh_system_theme()
    current[0] = VisualTheme.DARK
    assert controller.refresh_system_theme()
    assert controller.theme is VisualTheme.DARK
    assert events == [VisualTheme.DARK.value]

    controller.set_mode(AppearanceMode.LIGHT)
    current[0] = VisualTheme.LIGHT
    assert not controller.refresh_system_theme()


def test_main_window_applies_and_persists_theme_without_rebuilding_pages(
    qapp: QApplication,
    tmp_path: Path,
) -> None:
    settings = _settings(tmp_path / "window-theme.ini")
    settings.setValue(ThemeController.SETTINGS_KEY, AppearanceMode.DARK.value)
    window = MainWindow(settings=settings)

    assert window.current_appearance is AppearanceMode.DARK
    assert window.current_theme is VisualTheme.DARK
    assert window.property("visualTheme") == VisualTheme.DARK.value
    assert DARK_PALETTE.window in window.styleSheet()

    window.navigate(RouteId.SETTINGS)
    page = window.findChild(OllamaSettingsPage, "ollamaSettingsPage")
    selector = window.findChild(AppearanceSelector)
    assert page is not None
    assert selector is page.appearance_selector
    assert selector.selected_mode is AppearanceMode.DARK

    selector.select_mode(AppearanceMode.LIGHT)

    assert window.current_theme is VisualTheme.LIGHT
    assert window.current_route is RouteId.SETTINGS
    assert window.findChild(OllamaSettingsPage, "ollamaSettingsPage") is page
    assert LIGHT_PALETTE.window in window.styleSheet()
    assert settings.value(ThemeController.SETTINGS_KEY) == AppearanceMode.LIGHT.value


def test_appearance_selector_exposes_three_accessible_modes(
    qapp: QApplication,
    tmp_path: Path,
) -> None:
    controller = ThemeController(
        _settings(tmp_path / "selector.ini"),
        system_resolver=lambda: VisualTheme.LIGHT,
    )
    selector = AppearanceSelector(controller, AppLocale.ENGLISH)
    buttons = selector.findChildren(QPushButton, "appearanceModeButton")

    assert len(buttons) == 3
    assert {button.property("appearanceMode") for button in buttons} == {
        AppearanceMode.SYSTEM.value,
        AppearanceMode.LIGHT.value,
        AppearanceMode.DARK.value,
    }
    assert all(button.accessibleName() for button in buttons)
    assert selector.selected_mode is AppearanceMode.SYSTEM
    assert selector.active_theme is VisualTheme.LIGHT
