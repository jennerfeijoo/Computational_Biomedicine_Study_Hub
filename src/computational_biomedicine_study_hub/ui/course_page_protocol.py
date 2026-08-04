"""Structural contract for authored modular course pages.

The application shell must not depend on concrete course-page classes. Every course
keeps an independent implementation, while pages that expose this small contract can
participate in navigation restoration, review routing, tutor context, and future
learning-path recommendations.
"""

from __future__ import annotations

from typing import Protocol, runtime_checkable

from .pages.module_reader_page import ModuleReaderPage


@runtime_checkable
class ModularCoursePageProtocol(Protocol):
    """Runtime-checkable navigation contract shared by modular course pages."""

    @property
    def current_module_index(self) -> int:
        """Return the zero-based selected module index."""

    @property
    def reader(self) -> ModuleReaderPage:
        """Return the currently selected module reader."""

    def select_module(self, index: int) -> bool:
        """Select a module by zero-based index."""

    def select_module_by_id(self, module_id: str) -> bool:
        """Select a module by stable language-independent identity."""


__all__ = ["ModularCoursePageProtocol"]
