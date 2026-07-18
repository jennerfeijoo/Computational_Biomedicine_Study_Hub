"""Strict Spanish, English and Danish internationalization support."""

from __future__ import annotations

from .controller import LanguageController
from .locales import DEFAULT_LOCALE, SUPPORTED_LOCALES, AppLocale
from .messages import ALL_MESSAGE_KEYS, MessageKey
from .service import TranslationError, Translator, validate_catalogs
from .ui_copy import UiCopyKey, ui_text, validate_ui_copy

__all__ = [
    "ALL_MESSAGE_KEYS",
    "AppLocale",
    "DEFAULT_LOCALE",
    "LanguageController",
    "MessageKey",
    "SUPPORTED_LOCALES",
    "TranslationError",
    "Translator",
    "UiCopyKey",
    "ui_text",
    "validate_catalogs",
    "validate_ui_copy",
]
