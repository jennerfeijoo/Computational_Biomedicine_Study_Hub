"""Semantic visual tokens and persistent application-wide appearance control."""

from __future__ import annotations

from collections.abc import Callable
from dataclasses import dataclass
from enum import StrEnum

from PySide6.QtCore import QObject, QSettings, Qt, Signal, Slot
from PySide6.QtGui import QGuiApplication, QStyleHints


class AppearanceMode(StrEnum):
    """Persisted user preference for selecting the active visual theme."""

    SYSTEM = "system"
    LIGHT = "light"
    DARK = "dark"

    @classmethod
    def resolve(cls, value: object) -> AppearanceMode:
        """Resolve stored or external values without trusting malformed settings."""

        try:
            return cls(str(value))
        except ValueError:
            return cls.SYSTEM


class VisualTheme(StrEnum):
    """Concrete theme used to render the current application stylesheet."""

    LIGHT = "light"
    DARK = "dark"


@dataclass(frozen=True, slots=True)
class ThemePalette:
    """Semantic colors consumed by the application stylesheet."""

    window: str
    surface: str
    surface_alt: str
    surface_hover: str
    surface_selected: str
    sidebar: str
    sidebar_hover: str
    sidebar_text: str
    sidebar_muted: str
    text: str
    text_muted: str
    text_subtle: str
    border: str
    border_strong: str
    accent: str
    accent_hover: str
    accent_soft: str
    accent_soft_border: str
    accent_text: str
    focus: str
    success: str
    warning: str
    error: str
    code_background: str
    code_text: str
    code_border: str
    disabled_background: str
    disabled_text: str
    selection: str


LIGHT_PALETTE = ThemePalette(
    window="#f4f6f8",
    surface="#ffffff",
    surface_alt="#edf2f7",
    surface_hover="#edf4fb",
    surface_selected="#eaf2fd",
    sidebar="#17212b",
    sidebar_hover="#243443",
    sidebar_text="#dbe4ec",
    sidebar_muted="#8fa1b3",
    text="#1f2933",
    text_muted="#66727f",
    text_subtle="#52606d",
    border="#d8e0e8",
    border_strong="#9eb6cf",
    accent="#2f80ed",
    accent_hover="#2469c7",
    accent_soft="#eaf2fd",
    accent_soft_border="#9fc1e8",
    accent_text="#ffffff",
    focus="#145fc0",
    success="#16734a",
    warning="#8a5a00",
    error="#b42318",
    code_background="#101820",
    code_text="#e6edf3",
    code_border="#263746",
    disabled_background="#edf1f5",
    disabled_text="#7b8794",
    selection="#2f80ed",
)

DARK_PALETTE = ThemePalette(
    window="#0b1118",
    surface="#121b24",
    surface_alt="#17222e",
    surface_hover="#1d2a37",
    surface_selected="#173a63",
    sidebar="#080e14",
    sidebar_hover="#172431",
    sidebar_text="#dce7f2",
    sidebar_muted="#8fa3b8",
    text="#e7edf4",
    text_muted="#aeb9c6",
    text_subtle="#93a2b3",
    border="#2c3a48",
    border_strong="#496176",
    accent="#62a8ff",
    accent_hover="#82b9ff",
    accent_soft="#173a63",
    accent_soft_border="#376a9f",
    accent_text="#08111c",
    focus="#8fc2ff",
    success="#4fd39a",
    warning="#f4c15d",
    error="#ff7b72",
    code_background="#070c12",
    code_text="#e6edf3",
    code_border="#33475a",
    disabled_background="#1a242f",
    disabled_text="#738294",
    selection="#316da8",
)

SystemThemeResolver = Callable[[], VisualTheme]


def palette_for(theme: VisualTheme) -> ThemePalette:
    """Return the complete semantic palette for one concrete theme."""

    return DARK_PALETTE if theme is VisualTheme.DARK else LIGHT_PALETTE


def system_visual_theme() -> VisualTheme:
    """Resolve the operating-system color scheme with a safe light fallback."""

    app = QGuiApplication.instance()
    if not isinstance(app, QGuiApplication):
        return VisualTheme.LIGHT
    scheme = app.styleHints().colorScheme()
    return VisualTheme.DARK if scheme == Qt.ColorScheme.Dark else VisualTheme.LIGHT


class ThemeController(QObject):
    """Own, persist and announce the application appearance preference."""

    appearance_changed = Signal(str)
    theme_changed = Signal(str)
    SETTINGS_KEY = "ui/appearance"

    def __init__(
        self,
        settings: QSettings | None = None,
        parent: QObject | None = None,
        *,
        system_resolver: SystemThemeResolver | None = None,
    ) -> None:
        super().__init__(parent)
        self._settings = settings if settings is not None else QSettings()
        self._system_resolver = system_resolver or system_visual_theme
        self._tracks_system_signal = system_resolver is None
        self._style_hints: QStyleHints | None = None
        self._mode = AppearanceMode.resolve(
            self._settings.value(self.SETTINGS_KEY, AppearanceMode.SYSTEM.value)
        )
        self._theme = self._resolve_theme()
        self._connect_system_theme_signal()

    @property
    def mode(self) -> AppearanceMode:
        """Return the persisted appearance preference."""

        return self._mode

    @property
    def theme(self) -> VisualTheme:
        """Return the currently resolved concrete theme."""

        return self._theme

    @property
    def palette(self) -> ThemePalette:
        """Return semantic tokens for the resolved theme."""

        return palette_for(self._theme)

    def set_mode(self, mode: AppearanceMode | str) -> bool:
        """Persist a new preference and emit only meaningful visual changes."""

        resolved = mode if isinstance(mode, AppearanceMode) else AppearanceMode.resolve(mode)
        previous_mode = self._mode
        previous_theme = self._theme
        self._mode = resolved
        self._theme = self._resolve_theme()
        if resolved == previous_mode and self._theme == previous_theme:
            return False

        self._settings.setValue(self.SETTINGS_KEY, resolved.value)
        self._settings.sync()
        if resolved != previous_mode:
            self.appearance_changed.emit(resolved.value)
        if self._theme != previous_theme:
            self.theme_changed.emit(self._theme.value)
        return True

    def refresh_system_theme(self) -> bool:
        """Re-resolve system mode after an operating-system appearance change."""

        if self._mode is not AppearanceMode.SYSTEM:
            return False
        resolved = self._system_resolver()
        if resolved == self._theme:
            return False
        self._theme = resolved
        self.theme_changed.emit(resolved.value)
        return True

    def _resolve_theme(self) -> VisualTheme:
        if self._mode is AppearanceMode.LIGHT:
            return VisualTheme.LIGHT
        if self._mode is AppearanceMode.DARK:
            return VisualTheme.DARK
        return self._system_resolver()

    def _connect_system_theme_signal(self) -> None:
        if not self._tracks_system_signal:
            return
        app = QGuiApplication.instance()
        if not isinstance(app, QGuiApplication):
            return
        self._style_hints = app.styleHints()
        self._style_hints.colorSchemeChanged.connect(self._on_system_color_scheme_changed)

    @Slot(object)
    def _on_system_color_scheme_changed(self, color_scheme: object) -> None:
        del color_scheme
        self.refresh_system_theme()


__all__ = [
    "AppearanceMode",
    "DARK_PALETTE",
    "LIGHT_PALETTE",
    "SystemThemeResolver",
    "ThemeController",
    "ThemePalette",
    "VisualTheme",
    "palette_for",
    "system_visual_theme",
]
