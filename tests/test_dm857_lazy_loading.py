from __future__ import annotations

from PySide6.QtWidgets import QApplication, QStackedWidget

from computational_biomedicine_study_hub.content.dm857 import BUNDLES, MODULE_01_FOUNDATIONS
from computational_biomedicine_study_hub.courses.dm857 import DM857Page
from computational_biomedicine_study_hub.ui.pages.module_reader_page import ModuleReaderPage


def _constructed_readers(stack: QStackedWidget) -> tuple[ModuleReaderPage, ...]:
    return tuple(
        widget
        for index in range(stack.count())
        if isinstance((widget := stack.widget(index)), ModuleReaderPage)
    )


def test_course_page_constructs_only_the_initial_reader(qapp: QApplication) -> None:
    page = DM857Page()
    stack = page.findChild(QStackedWidget, "courseModuleStack")

    assert stack is not None
    assert stack.count() == page.module_count == len(BUNDLES)
    assert page.constructed_reader_count == 1
    assert page.has_constructed_reader(0)
    assert not page.has_constructed_reader(page.module_count - 1)
    assert len(_constructed_readers(stack)) == 1
    assert page.reader.module is MODULE_01_FOUNDATIONS


def test_selecting_a_module_constructs_it_once_and_reuses_it(qapp: QApplication) -> None:
    page = DM857Page()
    first_reader = page.reader
    last_index = page.module_count - 1

    assert page.select_module(last_index)
    last_reader = page.reader

    assert last_reader is not first_reader
    assert last_reader.module is BUNDLES[-1].module
    assert last_reader.property("contentVersion") == BUNDLES[-1].content_version
    assert page.constructed_reader_count == 2
    assert page.has_constructed_reader(last_index)

    assert page.select_module(0)
    assert page.reader is first_reader
    assert page.constructed_reader_count == 2
