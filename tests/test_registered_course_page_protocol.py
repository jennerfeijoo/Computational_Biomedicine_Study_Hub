"""Ensure every registered course page participates in generic shell navigation."""

from __future__ import annotations

from PySide6.QtWidgets import QWidget

from computational_biomedicine_study_hub.courses import COURSES
from computational_biomedicine_study_hub.i18n import AppLocale
from computational_biomedicine_study_hub.ui.course_page_protocol import (
    ModularCoursePageProtocol,
)


def test_all_registered_course_pages_satisfy_modular_protocol(qtbot) -> None:  # type: ignore[no-untyped-def]
    pages: list[QWidget] = []
    for course in COURSES:
        page = course.page_factory(AppLocale.ENGLISH)
        pages.append(page)
        qtbot.addWidget(page)
        assert isinstance(page, ModularCoursePageProtocol), course.code
        assert page.select_module(0)
        assert page.select_module_by_id(page.reader.module.module_id)

    assert len(pages) == 4
