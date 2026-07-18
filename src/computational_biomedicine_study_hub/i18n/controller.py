"""Persistent application-wide locale controller."""

from __future__ import annotations

from PySide6.QtCore import QObject, QSettings, Signal

from .locales import DEFAULT_LOCALE, AppLocale
from .service import Translator


class LanguageController(QObject):
    """Own the active locale, translator and persisted language preference."""

    locale_changed = Signal(str)
    SETTINGS_KEY = "ui/locale"

    def __init__(
        self,
        settings: QSettings | None = None,
        parent: QObject | None = None,
    ) -> None:
        super().__init__(parent)
        self._settings = settings if settings is not None else QSettings()
        stored = self._settings.value(self.SETTINGS_KEY, DEFAULT_LOCALE.value)
        self._translator = Translator(AppLocale.resolve(str(stored)))

    @property
    def locale(self) -> AppLocale:
        """Return the active supported locale."""
        return self._translator.locale

    @property
    def translator(self) -> Translator:
        """Return the shared translator bound to the active locale."""
        return self._translator

    def set_locale(self, locale: AppLocale | str) -> bool:
        """Persist and announce a locale change; return whether it changed."""
        resolved = locale if isinstance(locale, AppLocale) else AppLocale.resolve(locale)
        if resolved == self.locale:
            return False

        self._translator.set_locale(resolved)
        self._settings.setValue(self.SETTINGS_KEY, resolved.value)
        self._settings.sync()
        self.locale_changed.emit(resolved.value)
        return True


__all__ = ["LanguageController"]
