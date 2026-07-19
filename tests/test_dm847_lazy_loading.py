"""Lazy navigation tests for the complete DM847 course page."""

from __future__ import annotations

from PySide6.QtWidgets import QApplication, QComboBox, QStackedWidget

from computational_biomedicine_study_hub.content.dm847 import (
    MODULE_01_MOLECULAR_INFORMATION,
    MODULE_10_OMICS_LEARNING_PROJECT,
)
from computational_biomedicine_study_hub.courses.dm847 import DM847Page
from computational_biomedicine_study_hub.i18n import AppLocale
from computational_biomedicine_study_hub.ui.pages.module_reader_page import ModuleReaderPage


def _constructed_readers(stack: QStackedWidget) -> tuple[ModuleReaderPage, ...]:
    return tuple(
        widget
        for index in range(stack.count())
        if isinstance((widget := stack.widget(index)), ModuleReaderPage)
    )


def test_dm847_page_constructs_only_the_initial_reader(qapp: QApplication) -> None:
    page = DM847Page()
    stack = page.findChild(QStackedWidget, "courseModuleStack")
    selector = page.findChild(QComboBox, "courseModuleSelector")

    assert stack is not None
    assert selector is not None
    assert stack.count() == selector.count() == page.module_count == 10
    assert page.constructed_reader_count == 1
    assert page.has_constructed_reader(0)
    assert not page.has_constructed_reader(9)
    assert len(_constructed_readers(stack)) == 1
    assert page.reader.module is MODULE_01_MOLECULAR_INFORMATION


def test_dm847_selecting_a_module_constructs_and_reuses_it(
    qapp: QApplication,
) -> None:
    page = DM847Page()
    first_reader = page.reader

    assert page.select_module(9)
    final_reader = page.reader

    assert final_reader is not first_reader
    assert final_reader.module is MODULE_10_OMICS_LEARNING_PROJECT
    assert final_reader.property("contentVersion") == "1.0.0"
    assert page.constructed_reader_count == 2
    assert page.has_constructed_reader(9)

    assert page.select_module(0)
    assert page.reader is first_reader
    assert page.constructed_reader_count == 2
    assert not page.select_module(-1)
    assert not page.select_module(10)


def test_dm847_page_materializes_the_selected_locale(qapp: QApplication) -> None:
    page = DM847Page(AppLocale.DANISH_DENMARK)
    selector = page.findChild(QComboBox, "courseModuleSelector")

    assert selector is not None
    assert page.reader.module.module_id == "dm847.m01"
    assert page.reader.module.title.startswith("Molekylær")
    assert selector.itemText(0).startswith("Modul")

    assert page.select_module(9)
    assert page.reader.module.module_id == "dm847.m10"
    assert page.reader.module.title.startswith("Læring")
