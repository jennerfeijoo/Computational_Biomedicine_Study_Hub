"""Stable route identifiers and page descriptors for the application shell."""

from __future__ import annotations

from dataclasses import dataclass
from enum import StrEnum


class RouteId(StrEnum):
    """Stable identifiers used by navigation, persistence and deep links."""

    HOME = "home"
    REVIEW = "review"
    ASSESSMENTS = "assessments"
    FLASHCARDS = "flashcards"
    GLOSSARY = "glossary"
    SETTINGS = "settings"


@dataclass(frozen=True, slots=True)
class PageDescriptor:
    """Metadata required by the shell to present a page."""

    route: RouteId
    title: str
    subtitle: str


PAGE_DESCRIPTORS: dict[RouteId, PageDescriptor] = {
    RouteId.HOME: PageDescriptor(RouteId.HOME, "Inicio", "Centro de estudio del MSc in Computational Biomedicine."),
    RouteId.REVIEW: PageDescriptor(RouteId.REVIEW, "Repaso", "Recuperación activa, práctica intercalada y revisión espaciada."),
    RouteId.ASSESSMENTS: PageDescriptor(RouteId.ASSESSMENTS, "Evaluaciones", "Preguntas, ejercicios y problemas con retroalimentación."),
    RouteId.FLASHCARDS: PageDescriptor(RouteId.FLASHCARDS, "Tarjetas de memoria", "Conceptos, fórmulas, código y relaciones esenciales."),
    RouteId.GLOSSARY: PageDescriptor(RouteId.GLOSSARY, "Glosario", "Definiciones transversales de programación, estadística y biología."),
    RouteId.SETTINGS: PageDescriptor(RouteId.SETTINGS, "Configuración", "Preferencias de la aplicación e integraciones locales."),
}
