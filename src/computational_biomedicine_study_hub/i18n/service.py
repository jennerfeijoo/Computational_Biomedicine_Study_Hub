"""Strict translation access and catalog validation."""

from __future__ import annotations

from collections.abc import Mapping
from dataclasses import dataclass
from string import Formatter
from typing import Final

from .catalogs import CATALOGS
from .locales import AppLocale, DEFAULT_LOCALE
from .messages import ALL_MESSAGE_KEYS, MessageKey

_FORMATTER: Final = Formatter()
CatalogView = Mapping[MessageKey, str]
CatalogRegistry = Mapping[AppLocale, CatalogView]


class TranslationError(RuntimeError):
    """Raised when a translation catalog or formatted message is invalid."""


@dataclass(slots=True)
class Translator:
    """Resolve complete messages for one supported locale.

    Missing translations are programming errors. The service therefore raises instead
    of displaying a key or silently falling back to another language.
    """

    locale: AppLocale = DEFAULT_LOCALE

    def set_locale(self, locale: AppLocale | str) -> None:
        """Select a supported locale."""
        self.locale = locale if isinstance(locale, AppLocale) else AppLocale.resolve(locale)

    def text(self, key: MessageKey, **values: object) -> str:
        """Return one translated and safely formatted message."""
        catalog = CATALOGS[self.locale]
        try:
            template = catalog[key]
        except KeyError as exc:
            raise TranslationError(
                f"Missing translation {key.value!r} for locale {self.locale.value!r}."
            ) from exc

        expected = _placeholder_names(template)
        provided = frozenset(values)
        missing = expected - provided
        unexpected = provided - expected
        if missing or unexpected:
            raise TranslationError(
                f"Invalid format values for {key.value!r}: "
                f"missing={sorted(missing)}, unexpected={sorted(unexpected)}."
            )

        try:
            return template.format(**values)
        except (KeyError, ValueError, IndexError) as exc:
            raise TranslationError(
                f"Could not format translation {key.value!r} for {self.locale.value!r}."
            ) from exc


def validate_catalogs(catalogs: CatalogRegistry | None = None) -> None:
    """Require exact key coverage and matching placeholders in every locale."""
    registry = CATALOGS if catalogs is None else catalogs
    supported = set(AppLocale)
    available = set(registry)
    if available != supported:
        raise TranslationError(
            "Translation catalogs must exist for every supported locale: "
            f"missing={sorted(locale.value for locale in supported - available)}, "
            f"unexpected={sorted(locale.value for locale in available - supported)}."
        )

    reference = registry[DEFAULT_LOCALE]
    for locale, catalog in registry.items():
        keys = frozenset(catalog)
        missing = ALL_MESSAGE_KEYS - keys
        unexpected = keys - ALL_MESSAGE_KEYS
        if missing or unexpected:
            raise TranslationError(
                f"Catalog {locale.value!r} has invalid key coverage: "
                f"missing={sorted(key.value for key in missing)}, "
                f"unexpected={sorted(key.value for key in unexpected)}."
            )

        for key in ALL_MESSAGE_KEYS:
            text = catalog[key]
            if not text.strip():
                raise TranslationError(
                    f"Catalog {locale.value!r} contains an empty translation for {key.value!r}."
                )
            reference_placeholders = _placeholder_names(reference[key])
            localized_placeholders = _placeholder_names(text)
            if localized_placeholders != reference_placeholders:
                raise TranslationError(
                    f"Catalog {locale.value!r} has incompatible placeholders for {key.value!r}: "
                    f"expected={sorted(reference_placeholders)}, "
                    f"actual={sorted(localized_placeholders)}."
                )


def _placeholder_names(template: str) -> frozenset[str]:
    names: set[str] = set()
    for _, field_name, _, _ in _FORMATTER.parse(template):
        if field_name:
            root_name = field_name.split(".", maxsplit=1)[0].split("[", maxsplit=1)[0]
            names.add(root_name)
    return frozenset(names)


validate_catalogs()

__all__ = ["TranslationError", "Translator", "validate_catalogs"]
