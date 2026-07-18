"""Course registration models used by the application shell."""

from __future__ import annotations

from collections.abc import Callable, Mapping
from dataclasses import dataclass, field

from PySide6.QtWidgets import QWidget

from ..i18n import AppLocale, DEFAULT_LOCALE


@dataclass(frozen=True, slots=True)
class CourseRegistration:
    """Describe one course and provide its localized page factory."""

    code: str
    title: str
    ects: int
    semester: int
    summary: str
    page_factory: Callable[[AppLocale], QWidget]
    localized_titles: Mapping[AppLocale, str] = field(default_factory=dict)
    localized_summaries: Mapping[AppLocale, str] = field(default_factory=dict)

    @property
    def route(self) -> str:
        """Return the stable route used by navigation and persistence."""
        return f"course/{self.code.casefold()}"

    @property
    def navigation_label(self) -> str:
        """Return the Spanish compact label retained for compatibility."""
        return self.navigation_label_for(DEFAULT_LOCALE)

    def title_for(self, locale: AppLocale | str) -> str:
        """Return the localized course title."""
        resolved = locale if isinstance(locale, AppLocale) else AppLocale.resolve(locale)
        return self.localized_titles.get(resolved, self.title)

    def summary_for(self, locale: AppLocale | str) -> str:
        """Return the localized course summary."""
        resolved = locale if isinstance(locale, AppLocale) else AppLocale.resolve(locale)
        return self.localized_summaries.get(resolved, self.summary)

    def navigation_label_for(self, locale: AppLocale | str) -> str:
        """Return a compact localized label suitable for the sidebar."""
        return f"{self.code} · {self.title_for(locale)}"
