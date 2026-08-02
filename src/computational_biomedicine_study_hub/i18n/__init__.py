"""Strict Spanish, English and Danish internationalization support."""

from __future__ import annotations

from .adaptive_review_copy import (
    AdaptiveReviewCopyKey,
    adaptive_review_text,
    validate_adaptive_review_copy,
)
from .adaptive_tutor_copy import (
    AdaptiveTutorCopyKey,
    adaptive_tutor_text,
    validate_adaptive_tutor_copy,
)
from .appearance_copy import (
    AppearanceCopyKey,
    appearance_text,
    validate_appearance_copy,
)
from .capstone_copy import (
    CapstoneCopyKey,
    capstone_milestone_copy,
    capstone_rubric_text,
    capstone_text,
    validate_capstone_copy,
)
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
from .tutor_chat_copy import TutorChatCopyKey, tutor_chat_text, validate_tutor_chat_copy
from .ui_copy import UiCopyKey, ui_text, validate_ui_copy

__all__ = [
    "ALL_MESSAGE_KEYS",
    "AdaptiveReviewCopyKey",
    "AdaptiveTutorCopyKey",
    "AppearanceCopyKey",
    "AppLocale",
    "CapstoneCopyKey",
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
    "TutorChatCopyKey",
    "UiCopyKey",
    "adaptive_review_text",
    "adaptive_tutor_text",
    "appearance_text",
    "capstone_milestone_copy",
    "capstone_rubric_text",
    "capstone_text",
    "challenge_text",
    "challenge_tutor_text",
    "confidence_text",
    "lab_text",
    "tutor_chat_text",
    "ui_text",
    "validate_adaptive_review_copy",
    "validate_adaptive_tutor_copy",
    "validate_appearance_copy",
    "validate_capstone_copy",
    "validate_catalogs",
    "validate_challenge_copy",
    "validate_challenge_tutor_copy",
    "validate_confidence_copy",
    "validate_lab_copy",
    "validate_tutor_chat_copy",
    "validate_ui_copy",
]
