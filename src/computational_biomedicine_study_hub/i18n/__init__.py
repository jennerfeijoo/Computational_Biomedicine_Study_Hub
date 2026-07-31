"""Strict Spanish, English and Danish internationalization support."""

from __future__ import annotations

from .challenge_copy import ChallengeCopyKey, challenge_text, validate_challenge_copy
from .challenge_tutor_copy import (
    ChallengeTutorCopyKey,
    challenge_tutor_text,
    validate_challenge_tutor_copy,
)
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
    "ChallengeCopyKey",
    "ChallengeTutorCopyKey",
    "ConfidenceCopyKey",
    "DEFAULT_LOCALE",
    "LabCopyKey",
    "LanguageController",
    "MessageKey",
    "SUPPORTED_LOCALES",
    "TranslationError",
    "Translator",
    "UiCopyKey",
    "challenge_text",
    "challenge_tutor_text",
    "confidence_text",
    "lab_text",
    "ui_text",
    "validate_catalogs",
    "validate_challenge_copy",
    "validate_challenge_tutor_copy",
    "validate_confidence_copy",
    "validate_lab_copy",
    "validate_ui_copy",
]
