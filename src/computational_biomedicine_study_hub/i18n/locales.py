"""Supported locales and deterministic locale resolution."""

from __future__ import annotations

from enum import StrEnum


class AppLocale(StrEnum):
    """Locales supported by the complete application."""

    SPANISH_SPAIN = "es-ES"
    ENGLISH = "en"
    DANISH_DENMARK = "da-DK"

    @property
    def native_name(self) -> str:
        """Return the language name as it should appear in the selector."""
        return {
            AppLocale.SPANISH_SPAIN: "Español",
            AppLocale.ENGLISH: "English",
            AppLocale.DANISH_DENMARK: "Dansk",
        }[self]

    @classmethod
    def resolve(cls, value: str | None) -> AppLocale:
        """Resolve persisted, operating-system and user-provided locale codes.

        Region variants map to the supported locale for their language. Unknown or
        blank values use Spanish because it is the current authored source language.
        """
        normalized = (value or "").strip().replace("_", "-").casefold()
        if normalized.startswith("es"):
            return cls.SPANISH_SPAIN
        if normalized.startswith("da"):
            return cls.DANISH_DENMARK
        if normalized.startswith("en"):
            return cls.ENGLISH
        return cls.SPANISH_SPAIN


SUPPORTED_LOCALES: tuple[AppLocale, ...] = tuple(AppLocale)
DEFAULT_LOCALE = AppLocale.SPANISH_SPAIN

__all__ = ["AppLocale", "DEFAULT_LOCALE", "SUPPORTED_LOCALES"]
