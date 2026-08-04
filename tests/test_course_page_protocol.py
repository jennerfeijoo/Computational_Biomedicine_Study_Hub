"""Regression tests for structural modular-course shell integration."""

from __future__ import annotations

from computational_biomedicine_study_hub.ui.course_page_protocol import (
    ModularCoursePageProtocol,
)


class FakeReader:
    current_section_index = 0


class FakeModularCoursePage:
    def __init__(self) -> None:
        self._index = 0
        self._reader = FakeReader()

    @property
    def current_module_index(self) -> int:
        return self._index

    @property
    def reader(self) -> FakeReader:
        return self._reader

    def select_module(self, index: int) -> bool:
        self._index = index
        return True

    def select_module_by_id(self, module_id: str) -> bool:
        return bool(module_id)


class IncompleteCoursePage:
    current_module_index = 0


def test_complete_structural_course_page_satisfies_runtime_protocol() -> None:
    assert isinstance(FakeModularCoursePage(), ModularCoursePageProtocol)


def test_incomplete_course_page_is_rejected_by_runtime_protocol() -> None:
    assert not isinstance(IncompleteCoursePage(), ModularCoursePageProtocol)
