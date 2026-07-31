"""Strict localized copy for the persistent appearance controls."""

from __future__ import annotations

from enum import StrEnum
from string import Formatter

from .locales import AppLocale


class AppearanceCopyKey(StrEnum):
    """Stable keys for theme selection and resolved-theme feedback."""

    GROUP = "appearance.group"
    EXPLANATION = "appearance.explanation"
    SYSTEM = "appearance.system"
    LIGHT = "appearance.light"
    DARK = "appearance.dark"
    ACTIVE_THEME = "appearance.active_theme"
    THEME_LIGHT = "appearance.theme_light"
    THEME_DARK = "appearance.theme_dark"


_CATALOGS: dict[AppLocale, dict[AppearanceCopyKey, str]] = {
    AppLocale.SPANISH_SPAIN: {
        AppearanceCopyKey.GROUP: "Apariencia",
        AppearanceCopyKey.EXPLANATION: (
            "Selecciona un tema fijo o permite que la aplicación siga la preferencia visual "
            "del sistema operativo. El cambio se aplica y se guarda inmediatamente."
        ),
        AppearanceCopyKey.SYSTEM: "Seguir el sistema",
        AppearanceCopyKey.LIGHT: "Claro",
        AppearanceCopyKey.DARK: "Oscuro",
        AppearanceCopyKey.ACTIVE_THEME: "Tema activo: {theme}",
        AppearanceCopyKey.THEME_LIGHT: "claro",
        AppearanceCopyKey.THEME_DARK: "oscuro",
    },
    AppLocale.ENGLISH: {
        AppearanceCopyKey.GROUP: "Appearance",
        AppearanceCopyKey.EXPLANATION: (
            "Choose a fixed theme or let the application follow the operating system appearance. "
            "The change is applied and saved immediately."
        ),
        AppearanceCopyKey.SYSTEM: "Follow system",
        AppearanceCopyKey.LIGHT: "Light",
        AppearanceCopyKey.DARK: "Dark",
        AppearanceCopyKey.ACTIVE_THEME: "Active theme: {theme}",
        AppearanceCopyKey.THEME_LIGHT: "light",
        AppearanceCopyKey.THEME_DARK: "dark",
    },
    AppLocale.DANISH_DENMARK: {
        AppearanceCopyKey.GROUP: "Udseende",
        AppearanceCopyKey.EXPLANATION: (
            "Vælg et fast tema, eller lad programmet følge operativsystemets udseende. "
            "Ændringen anvendes og gemmes med det samme."
        ),
        AppearanceCopyKey.SYSTEM: "Følg systemet",
        AppearanceCopyKey.LIGHT: "Lyst",
        AppearanceCopyKey.DARK: "Mørkt",
        AppearanceCopyKey.ACTIVE_THEME: "Aktivt tema: {theme}",
        AppearanceCopyKey.THEME_LIGHT: "lyst",
        AppearanceCopyKey.THEME_DARK: "mørkt",
    },
}


def appearance_text(
    locale: AppLocale,
    key: AppearanceCopyKey,
    **values: object,
) -> str:
    """Return one localized appearance string with strict placeholders."""

    template = _CATALOGS[locale][key]
    required = {
        field_name for _, field_name, _, _ in Formatter().parse(template) if field_name is not None
    }
    supplied = set(values)
    if supplied != required:
        raise ValueError(
            f"Appearance copy {key.value!r} requires {sorted(required)}, got {sorted(supplied)}."
        )
    return template.format(**values)


def validate_appearance_copy() -> None:
    """Require identical keys and placeholder contracts in every locale."""

    expected_keys = set(AppearanceCopyKey)
    reference_fields: dict[AppearanceCopyKey, set[str]] = {}
    for locale, catalog in _CATALOGS.items():
        if set(catalog) != expected_keys:
            missing = sorted(key.value for key in expected_keys - set(catalog))
            extra = sorted(key.value for key in set(catalog) - expected_keys)
            raise ValueError(
                f"Appearance catalog {locale.value} is incomplete: missing={missing}, extra={extra}."
            )
        for key, template in catalog.items():
            fields = {
                field_name
                for _, field_name, _, _ in Formatter().parse(template)
                if field_name is not None
            }
            reference = reference_fields.setdefault(key, fields)
            if fields != reference:
                raise ValueError(
                    f"Appearance placeholder mismatch for {key.value!r} in {locale.value}."
                )


__all__ = ["AppearanceCopyKey", "appearance_text", "validate_appearance_copy"]
