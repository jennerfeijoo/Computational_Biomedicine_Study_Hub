"""Shared builders for authored technical reasoning stations."""

from __future__ import annotations

from ...i18n.locales import AppLocale
from ...learning.computational_labs import LocalizedText
from ...learning.technical_stations import TechnicalStationCriterion


def localized(es: str, en: str, da: str) -> LocalizedText:
    return LocalizedText(
        {
            AppLocale.SPANISH_SPAIN: es,
            AppLocale.ENGLISH: en,
            AppLocale.DANISH_DENMARK: da,
        }
    )


def criterion(
    identity: str,
    es: str,
    en: str,
    da: str,
) -> TechnicalStationCriterion:
    return TechnicalStationCriterion(identity, localized(es, en, da))


__all__ = ["criterion", "localized"]
