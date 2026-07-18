"""Stable route identifiers and page descriptors for the application shell."""

from __future__ import annotations

from dataclasses import dataclass
from enum import StrEnum


class RouteId(StrEnum):
    """Stable identifiers for application-wide pages."""

    HOME = "home"
    REVIEW = "review"
    ASSESSMENTS = "assessments"
    FLASHCARDS = "flashcards"
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


PAGE_DESCRIPTORS: dict[str, PageDescriptor] = {
    RouteId.HOME.value: PageDescriptor(
        RouteId.HOME.value,
        "Inicio",
        "Centro de estudio del MSc in Computational Biomedicine.",
    ),
    RouteId.REVIEW.value: PageDescriptor(
        RouteId.REVIEW.value,
        "Repaso",
        "Recuperación activa, práctica intercalada y revisión espaciada.",
    ),
    RouteId.ASSESSMENTS.value: PageDescriptor(
        RouteId.ASSESSMENTS.value,
        "Evaluaciones",
        "Preguntas, ejercicios y problemas con retroalimentación.",
    ),
    RouteId.FLASHCARDS.value: PageDescriptor(
        RouteId.FLASHCARDS.value,
        "Tarjetas de memoria",
        "Conceptos, fórmulas, código y relaciones esenciales.",
    ),
    RouteId.GLOSSARY.value: PageDescriptor(
        RouteId.GLOSSARY.value,
        "Glosario",
        "Definiciones transversales de programación, estadística y biología.",
    ),
    RouteId.SETTINGS.value: PageDescriptor(
        RouteId.SETTINGS.value,
        "Configuración",
        "Preferencias de la aplicación e integraciones locales.",
    ),
}
