"""Stable route identifiers and localized page descriptors."""

from __future__ import annotations

from dataclasses import dataclass
from enum import StrEnum

from ..i18n import MessageKey, Translator


class RouteId(StrEnum):
    """Stable identifiers for application-wide pages."""

    HOME = "home"
    REVIEW = "review"
    ASSESSMENTS = "assessments"
    FLASHCARDS = "flashcards"
    STUDY_LAB = "study_lab"
    GLOSSARY = "glossary"
    SETTINGS = "settings"


RouteLike = RouteId | str


@dataclass(frozen=True, slots=True)
class PageDescriptor:
    """Metadata required by the shell to present a page."""

    route: str
    title: str
    subtitle: str


def route_value(route: RouteLike) -> str:
    """Normalize core and dynamic routes to their persisted string value."""
    if isinstance(route, RouteId):
        return route.value
    return route


_DESCRIPTOR_KEYS = {
    RouteId.HOME: (MessageKey.PAGE_HOME_TITLE, MessageKey.PAGE_HOME_SUBTITLE),
    RouteId.REVIEW: (MessageKey.PAGE_REVIEW_TITLE, MessageKey.PAGE_REVIEW_SUBTITLE),
    RouteId.ASSESSMENTS: (
        MessageKey.PAGE_ASSESSMENTS_TITLE,
        MessageKey.PAGE_ASSESSMENTS_SUBTITLE,
    ),
    RouteId.FLASHCARDS: (
        MessageKey.PAGE_FLASHCARDS_TITLE,
        MessageKey.PAGE_FLASHCARDS_SUBTITLE,
    ),
    RouteId.STUDY_LAB: (
        MessageKey.PAGE_STUDY_LAB_TITLE,
        MessageKey.PAGE_STUDY_LAB_SUBTITLE,
    ),
    RouteId.GLOSSARY: (MessageKey.PAGE_GLOSSARY_TITLE, MessageKey.PAGE_GLOSSARY_SUBTITLE),
    RouteId.SETTINGS: (MessageKey.PAGE_SETTINGS_TITLE, MessageKey.PAGE_SETTINGS_SUBTITLE),
}


def localized_page_descriptors(translator: Translator) -> dict[str, PageDescriptor]:
    """Return complete shell descriptors in the translator's active locale."""
    return {
        route.value: PageDescriptor(
            route=route.value,
            title=translator.text(title_key),
            subtitle=translator.text(subtitle_key),
        )
        for route, (title_key, subtitle_key) in _DESCRIPTOR_KEYS.items()
    }


PAGE_DESCRIPTORS = localized_page_descriptors(Translator())

__all__ = [
    "PAGE_DESCRIPTORS",
    "PageDescriptor",
    "RouteId",
    "RouteLike",
    "localized_page_descriptors",
    "route_value",
]
