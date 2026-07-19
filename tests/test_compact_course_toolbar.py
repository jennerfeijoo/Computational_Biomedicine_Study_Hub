from __future__ import annotations

from itertools import pairwise

import pytest
from PySide6.QtCore import Qt
from PySide6.QtWidgets import QFrame, QLabel

from computational_biomedicine_study_hub.courses.dm857 import DM857Page
from computational_biomedicine_study_hub.i18n import AppLocale
from computational_biomedicine_study_hub.learning.academic_catalog import AcademicCatalog
from computational_biomedicine_study_hub.ui.course_module_toolbar import (
    CourseInformationDialog,
    CourseModuleToolbar,
)
from computational_biomedicine_study_hub.ui.pages.course_study_page import CourseStudyPage


def _course_page(course_code: str, locale: AppLocale):
    if course_code == "DM857":
        return DM857Page(locale)
    return CourseStudyPage(
        course_code,
        AcademicCatalog(locale=locale),
        locale=locale,
    )


@pytest.mark.parametrize("course_code", ["DM847", "BMB830", "BMB831", "DM857"])
@pytest.mark.parametrize("locale", list(AppLocale))
def test_every_course_uses_the_same_compact_toolbar(
    qtbot,
    course_code: str,
    locale: AppLocale,
) -> None:
    page = _course_page(course_code, locale)
    qtbot.addWidget(page)
    toolbar = page.findChild(CourseModuleToolbar)

    assert toolbar is not None
    assert len(page.findChildren(CourseModuleToolbar)) == 1
    assert toolbar.maximumHeight() <= 64
    assert toolbar.module_selector.width() == 76
    assert toolbar.module_title.minimumWidth() >= 160
    assert toolbar.module_title.maximumHeight() <= (
        toolbar.module_title.fontMetrics().lineSpacing() * 2 + 8
    )
    assert toolbar.module_selector.itemText(0) == "M01"
    assert toolbar.module_selector.itemData(0).startswith(course_code.casefold())
    assert toolbar.module_selector.itemData(0) not in toolbar.module_selector.itemText(0)
    assert toolbar.module_title.toolTip() == toolbar.module_title.text()
    assert toolbar.findChild(QLabel, "moduleContextKicker") is None
    assert page.findChild(QFrame, "courseOverviewPanel") is None

    page.resize(904, 672)
    page.show()
    qtbot.wait(1)
    visible_controls = tuple(
        control
        for control in (
            toolbar.module_selector,
            toolbar.module_title,
            toolbar.progress_summary,
            toolbar.continue_button,
            toolbar.cumulative_button,
            toolbar.information_button,
        )
        if not control.isHidden()
    )
    assert all(
        control.geometry().right() <= toolbar.contentsRect().right() for control in visible_controls
    )
    assert all(
        left.geometry().right() < right.geometry().left()
        for left, right in pairwise(visible_controls)
    )


def test_cumulative_button_is_present_only_for_authored_course_content(qtbot) -> None:
    catalog = AcademicCatalog(locale=AppLocale.ENGLISH)
    authored = CourseStudyPage("BMB830", catalog, locale=AppLocale.ENGLISH)
    missing = DM857Page(AppLocale.ENGLISH)
    qtbot.addWidget(authored)
    qtbot.addWidget(missing)

    authored_toolbar = authored.findChild(CourseModuleToolbar)
    missing_toolbar = missing.findChild(CourseModuleToolbar)
    assert authored_toolbar is not None
    assert missing_toolbar is not None
    assert not authored_toolbar.cumulative_button.isHidden()
    assert missing_toolbar.cumulative_button.isHidden()


@pytest.mark.parametrize(
    ("locale", "button_text", "field_heading"),
    [
        (AppLocale.SPANISH_SPAIN, "Información", "Resultados de aprendizaje"),
        (AppLocale.ENGLISH, "Information", "Learning outcomes"),
        (AppLocale.DANISH_DENMARK, "Information", "Læringsudbytte"),
    ],
)
def test_course_information_dialog_is_localized_and_returns_keyboard_focus(
    qtbot,
    locale: AppLocale,
    button_text: str,
    field_heading: str,
) -> None:
    page = CourseStudyPage(
        "BMB830",
        AcademicCatalog(locale=locale),
        locale=locale,
    )
    qtbot.addWidget(page)
    page.show()
    toolbar = page.findChild(CourseModuleToolbar)
    assert toolbar is not None
    assert toolbar.information_button.text() == button_text

    qtbot.mouseClick(toolbar.information_button, Qt.MouseButton.LeftButton)
    dialog = page.findChild(CourseInformationDialog)
    assert dialog is not None
    qtbot.waitUntil(dialog.isVisible)

    headings = {
        label.text() for label in dialog.findChildren(QLabel, "courseInformationFieldTitle")
    }
    bodies = tuple(
        label.text() for label in dialog.findChildren(QLabel, "courseInformationFieldBody")
    )
    assert field_heading in headings
    assert "ECTS" in headings
    assert bodies
    assert not any(body.startswith(("{", "[")) for body in bodies)

    dialog.close()
    qtbot.waitUntil(toolbar.information_button.hasFocus)


@pytest.mark.parametrize("course_code", ["BMB830", "DM857"])
def test_module_and_tab_state_survive_rebuilding_the_course_in_another_locale(
    qtbot,
    course_code: str,
) -> None:
    original = _course_page(course_code, AppLocale.ENGLISH)
    qtbot.addWidget(original)
    assert original.select_module(4)
    original.reader.select_section_index(2)
    state = original.capture_state(f"course:{course_code.casefold()}")

    rebuilt = _course_page(course_code, AppLocale.DANISH_DENMARK)
    qtbot.addWidget(rebuilt)
    rebuilt.restore_state(state)

    assert rebuilt.current_module_index == 4
    assert rebuilt.reader.module.module_id == state.module_id
    assert rebuilt.reader.current_section_index == 2
    assert rebuilt.findChild(CourseModuleToolbar).module_selector.itemText(4) == "M05"
