"""Strict Spanish, English and Danish internationalization support."""

from __future__ import annotations

from .confidence_copy import ConfidenceCopyKey, confidence_text, validate_confidence_copy
from .controller import LanguageController
from .lab_copy import LabCopyKey, lab_text, validate_lab_copy
from .locales import DEFAULT_LOCALE, SUPPORTED_LOCALES, AppLocale
from .messages import ALL_MESSAGE_KEYS, MessageKey
from .service import TranslationError, Translator, validate_catalogs
from .ui_copy import UiCopyKey, ui_text, validate_ui_copy

__all__ = [
    "ALL_MESSAGE_KEYS",
    "AppLocale",
    "ConfidenceCopyKey",
    "DEFAULT_LOCALE",
    "LabCopyKey",
    "LanguageController",
    "MessageKey",
    "SUPPORTED_LOCALES",
    "TranslationError",
    "Translator",
    "UiCopyKey",
    "confidence_text",
    "lab_text",
    "ui_text",
    "validate_catalogs",
    "validate_confidence_copy",
    "validate_lab_copy",
    "validate_ui_copy",
]
