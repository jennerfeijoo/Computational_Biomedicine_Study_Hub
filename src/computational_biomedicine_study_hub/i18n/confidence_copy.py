"""Localized text for confidence judgements collected before objective feedback."""

from __future__ import annotations

from enum import StrEnum

from ..learning.progress import ConfidenceLevel
from .locales import AppLocale


class ConfidenceCopyKey(StrEnum):
    """Stable keys for the confidence-selection interaction."""

    PROMPT = "confidence.prompt"
    REQUIRED = "confidence.required"


_COPY: dict[AppLocale, dict[ConfidenceCopyKey | ConfidenceLevel, str]] = {
    AppLocale.SPANISH_SPAIN: {
        ConfidenceCopyKey.PROMPT: "¿Qué seguridad tienes antes de ver el resultado?",
        ConfidenceCopyKey.REQUIRED: "Selecciona tu nivel de confianza antes de comprobar.",
        ConfidenceLevel.LOW: "Baja",
        ConfidenceLevel.MEDIUM: "Media",
        ConfidenceLevel.HIGH: "Alta",
    },
    AppLocale.ENGLISH: {
        ConfidenceCopyKey.PROMPT: "How confident are you before seeing the result?",
        ConfidenceCopyKey.REQUIRED: "Select your confidence level before checking.",
        ConfidenceLevel.LOW: "Low",
        ConfidenceLevel.MEDIUM: "Medium",
        ConfidenceLevel.HIGH: "High",
    },
    AppLocale.DANISH_DENMARK: {
        ConfidenceCopyKey.PROMPT: "Hvor sikker er du, før du ser resultatet?",
        ConfidenceCopyKey.REQUIRED: "Vælg dit sikkerhedsniveau, før du kontrollerer svaret.",
        ConfidenceLevel.LOW: "Lav",
        ConfidenceLevel.MEDIUM: "Middel",
        ConfidenceLevel.HIGH: "Høj",
    },
}


def confidence_text(
    locale: AppLocale | str,
    key: ConfidenceCopyKey | ConfidenceLevel,
) -> str:
    """Return strict confidence copy for one supported locale."""

    resolved = locale if isinstance(locale, AppLocale) else AppLocale.resolve(locale)
    try:
        return _COPY[resolved][key]
    except KeyError as error:
        raise ValueError(f"Missing confidence copy for {resolved.value!r} and {key!r}.") from error


def validate_confidence_copy() -> None:
    """Require every locale to define every confidence interaction string."""

    required: set[ConfidenceCopyKey | ConfidenceLevel] = {
        *ConfidenceCopyKey,
        *ConfidenceLevel,
    }
    for locale in AppLocale:
        missing = required - set(_COPY[locale])
        if missing:
            raise ValueError(
                f"Confidence copy for {locale.value!r} is missing: "
                + ", ".join(sorted(str(key) for key in missing))
            )


validate_confidence_copy()

__all__ = ["ConfidenceCopyKey", "confidence_text", "validate_confidence_copy"]
