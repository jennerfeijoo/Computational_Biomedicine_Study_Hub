"""Page header and immediate application-language controls."""

from __future__ import annotations

from PySide6.QtCore import Signal
from PySide6.QtWidgets import (
    QButtonGroup,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QVBoxLayout,
    QWidget,
)

from ..i18n import AppLocale, DEFAULT_LOCALE


class PageHeader(QWidget):
    """Display page context and three persistent language buttons."""

    language_selected = Signal(str)

    def __init__(
        self,
        locale: AppLocale = DEFAULT_LOCALE,
        parent: QWidget | None = None,
    ) -> None:
        super().__init__(parent)
        self._title = QLabel()
        self._title.setObjectName("pageTitle")
        self._subtitle = QLabel()
        self._subtitle.setObjectName("pageSubtitle")
        self._subtitle.setWordWrap(True)

        text_container = QWidget()
        text_layout = QVBoxLayout(text_container)
        text_layout.setContentsMargins(0, 0, 0, 0)
        text_layout.setSpacing(4)
        text_layout.addWidget(self._title)
        text_layout.addWidget(self._subtitle)

        switcher = QWidget()
        switcher.setObjectName("languageSwitcher")
        switcher_layout = QHBoxLayout(switcher)
        switcher_layout.setContentsMargins(0, 0, 0, 0)
        switcher_layout.setSpacing(5)

        self._language_group = QButtonGroup(self)
        self._language_group.setExclusive(True)
        self._language_buttons: dict[AppLocale, QPushButton] = {}
        for label, button_locale in (
            ("DK", AppLocale.DANISH_DENMARK),
            ("ES", AppLocale.SPANISH_SPAIN),
            ("EN", AppLocale.ENGLISH),
        ):
            button = QPushButton(label)
            button.setObjectName("languageButton")
            button.setCheckable(True)
            button.setFixedSize(42, 34)
            button.setToolTip(button_locale.native_name)
            button.setAccessibleName(button_locale.native_name)
            button.clicked.connect(
                lambda checked=False, selected=button_locale: self.language_selected.emit(
                    selected.value
                )
            )
            self._language_group.addButton(button)
            self._language_buttons[button_locale] = button
            switcher_layout.addWidget(button)

        layout = QHBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(16)
        layout.addWidget(text_container, 1)
        layout.addWidget(switcher, 0)
        self.set_locale(locale)

    @property
    def selected_locale(self) -> AppLocale:
        """Return the locale represented by the checked button."""
        for locale, button in self._language_buttons.items():
            if button.isChecked():
                return locale
        return DEFAULT_LOCALE

    def set_text(self, title: str, subtitle: str) -> None:
        """Update header text for the active route."""
        self._title.setText(title)
        self._subtitle.setText(subtitle)

    def set_locale(self, locale: AppLocale | str) -> None:
        """Reflect the active locale without emitting a new selection."""
        resolved = locale if isinstance(locale, AppLocale) else AppLocale.resolve(locale)
        self._language_buttons[resolved].setChecked(True)
