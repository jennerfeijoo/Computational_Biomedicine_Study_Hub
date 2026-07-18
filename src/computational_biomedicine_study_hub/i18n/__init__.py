"""Strict Spanish, English and Danish internationalization support."""

from __future__ import annotations

from .locales import AppLocale, DEFAULT_LOCALE, SUPPORTED_LOCALES
from .messages import ALL_MESSAGE_KEYS, MessageKey
from .service import TranslationError, Translator, validate_catalogs

__all__ = [
    "ALL_MESSAGE_KEYS",
    "AppLocale",
    "DEFAULT_LOCALE",
    "MessageKey",
    "SUPPORTED_LOCALES",
    "TranslationError",
    "Translator",
    "validate_catalogs",
]
