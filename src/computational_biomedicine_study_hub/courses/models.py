"""Course registration models used by the application shell."""

from __future__ import annotations

from collections.abc import Callable
from dataclasses import dataclass

from PySide6.QtWidgets import QWidget


@dataclass(frozen=True, slots=True)
class CourseRegistration:
    """Describe one course and provide its page factory."""

    code: str
    title: str
    ects: int
    semester: int
    summary: str
    page_factory: Callable[[], QWidget]

    @property
    def route(self) -> str:
        """Return the stable route used by navigation and persistence."""
        return f"course/{self.code.casefold()}"

    @property
    def navigation_label(self) -> str:
        """Return a compact label suitable for the sidebar."""
        return f"{self.code} · {self.title}"
