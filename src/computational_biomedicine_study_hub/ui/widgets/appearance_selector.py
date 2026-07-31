"""Persistent, accessible segmented control for application appearance."""

from __future__ import annotations

from PySide6.QtCore import Slot
from PySide6.QtWidgets import (
    QButtonGroup,
    QGroupBox,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QVBoxLayout,
    QWidget,
)

from ...i18n import AppLocale, AppearanceCopyKey, appearance_text
from ..theme import AppearanceMode, ThemeController, VisualTheme


class AppearanceSelector(QGroupBox):
    """Select system, light or dark appearance with immediate persistence."""

    def __init__(
        self,
        controller: ThemeController,
        locale: AppLocale,
        parent: QWidget | None = None,
    ) -> None:
        super().__init__(appearance_text(locale, AppearanceCopyKey.GROUP), parent)
        self.setObjectName("settingsGroup")
        self.setProperty("settingsKind", "appearance")
        self._controller = controller
        self._locale = locale
        self._buttons: dict[AppearanceMode, QPushButton] = {}

        explanation = QLabel(appearance_text(locale, AppearanceCopyKey.EXPLANATION))
        explanation.setObjectName("settingsExplanation")
        explanation.setWordWrap(True)

        selector_layout = QHBoxLayout()
        selector_layout.setContentsMargins(0, 0, 0, 0)
        selector_layout.setSpacing(8)
        group = QButtonGroup(self)
        group.setExclusive(True)

        for mode, key in (
            (AppearanceMode.SYSTEM, AppearanceCopyKey.SYSTEM),
            (AppearanceMode.LIGHT, AppearanceCopyKey.LIGHT),
            (AppearanceMode.DARK, AppearanceCopyKey.DARK),
        ):
            label = appearance_text(locale, key)
            button = QPushButton(label)
            button.setObjectName("appearanceModeButton")
            button.setProperty("appearanceMode", mode.value)
            button.setCheckable(True)
            button.setMinimumHeight(38)
            button.setToolTip(label)
            button.setAccessibleName(label)
            button.clicked.connect(
                lambda checked=False, selected=mode: self._select_from_ui(selected, checked)
            )
            group.addButton(button)
            self._buttons[mode] = button
            selector_layout.addWidget(button, 1)

        self._active_theme = QLabel()
        self._active_theme.setObjectName("appearanceResolvedTheme")
        self._active_theme.setProperty("semanticTone", "muted")

        layout = QVBoxLayout(self)
        layout.setSpacing(12)
        layout.addWidget(explanation)
        layout.addLayout(selector_layout)
        layout.addWidget(self._active_theme)

        self._controller.appearance_changed.connect(self._on_appearance_changed)
        self._controller.theme_changed.connect(self._on_theme_changed)
        self._reflect_mode(self._controller.mode)
        self._reflect_theme(self._controller.theme)

    @property
    def selected_mode(self) -> AppearanceMode:
        """Return the appearance preference represented by the checked button."""

        for mode, button in self._buttons.items():
            if button.isChecked():
                return mode
        return self._controller.mode

    @property
    def active_theme(self) -> VisualTheme:
        """Return the controller's currently resolved concrete theme."""

        return self._controller.theme

    def select_mode(self, mode: AppearanceMode | str) -> bool:
        """Apply a mode through the shared controller."""

        return self._controller.set_mode(mode)

    def _select_from_ui(self, mode: AppearanceMode, checked: bool) -> None:
        if checked:
            self._controller.set_mode(mode)

    @Slot(str)
    def _on_appearance_changed(self, mode_value: str) -> None:
        self._reflect_mode(AppearanceMode.resolve(mode_value))

    @Slot(str)
    def _on_theme_changed(self, theme_value: str) -> None:
        self._reflect_theme(VisualTheme(theme_value))

    def _reflect_mode(self, mode: AppearanceMode) -> None:
        self._buttons[mode].setChecked(True)

    def _reflect_theme(self, theme: VisualTheme) -> None:
        key = (
            AppearanceCopyKey.THEME_DARK
            if theme is VisualTheme.DARK
            else AppearanceCopyKey.THEME_LIGHT
        )
        self._active_theme.setText(
            appearance_text(
                self._locale,
                AppearanceCopyKey.ACTIVE_THEME,
                theme=appearance_text(self._locale, key),
            )
        )


__all__ = ["AppearanceSelector"]
