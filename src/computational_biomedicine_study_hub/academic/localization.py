"""Localization helpers for nested academic values."""

from __future__ import annotations

from collections.abc import Mapping
from typing import Any

from .models import SUPPORTED_LOCALES, LocalizedText


def is_localized_mapping(value: object) -> bool:
    return isinstance(value, Mapping) and bool(set(value) & set(SUPPORTED_LOCALES))


def localize_value(value: Any, locale: str, *, fallback: str = "en") -> Any:
    """Return a localized copy of a nested academic value.

    IDs and structural keys are retained.  Only mappings containing locale
    keys are collapsed to a string.
    """
    if is_localized_mapping(value):
        return LocalizedText.from_value(value).resolve(locale, fallback=fallback)
    if isinstance(value, Mapping):
        return {
            str(key): localize_value(item, locale, fallback=fallback) for key, item in value.items()
        }
    if isinstance(value, list):
        return [localize_value(item, locale, fallback=fallback) for item in value]
    return value


__all__ = ["is_localized_mapping", "localize_value"]
