from __future__ import annotations

import pytest

from computational_biomedicine_study_hub.i18n import (
    ALL_MESSAGE_KEYS,
    AppLocale,
    MessageKey,
    TranslationError,
    Translator,
    validate_catalogs,
)
from computational_biomedicine_study_hub.i18n.catalogs import CATALOGS


def test_supported_locales_resolve_common_system_codes() -> None:
    assert AppLocale.resolve("es_ES") is AppLocale.SPANISH_SPAIN
    assert AppLocale.resolve("en-GB") is AppLocale.ENGLISH
    assert AppLocale.resolve("da_DK") is AppLocale.DANISH_DENMARK
    assert AppLocale.resolve("") is AppLocale.SPANISH_SPAIN
    assert AppLocale.resolve("unknown") is AppLocale.SPANISH_SPAIN


def test_every_catalog_has_exactly_the_defined_message_keys() -> None:
    validate_catalogs()

    for catalog in CATALOGS.values():
        assert frozenset(catalog) == ALL_MESSAGE_KEYS


def test_translator_returns_complete_messages_in_all_languages() -> None:
    expected = {
        AppLocale.SPANISH_SPAIN: "Semestre 1 · 10 ECTS",
        AppLocale.ENGLISH: "Semester 1 · 10 ECTS",
        AppLocale.DANISH_DENMARK: "Semester 1 · 10 ECTS",
    }

    for locale, rendered in expected.items():
        translator = Translator(locale)
        assert translator.text(MessageKey.COURSE_METADATA, semester=1, ects=10) == rendered


def test_translator_can_change_locale_without_reconstruction() -> None:
    translator = Translator()
    assert translator.text(MessageKey.NAV_HOME) == "Inicio"

    translator.set_locale("en-US")
    assert translator.text(MessageKey.NAV_HOME) == "Home"

    translator.set_locale(AppLocale.DANISH_DENMARK)
    assert translator.text(MessageKey.NAV_HOME) == "Forside"


def test_translator_rejects_missing_or_unexpected_format_values() -> None:
    translator = Translator(AppLocale.ENGLISH)

    with pytest.raises(TranslationError, match="missing"):
        translator.text(MessageKey.COURSE_METADATA, semester=1)

    with pytest.raises(TranslationError, match="unexpected"):
        translator.text(MessageKey.NAV_HOME, unused="value")


def test_native_language_names_are_stable_and_not_translated() -> None:
    assert [locale.native_name for locale in AppLocale] == [
        "Español",
        "English",
        "Dansk",
    ]
