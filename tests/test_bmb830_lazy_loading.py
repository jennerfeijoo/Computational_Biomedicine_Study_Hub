"""Lazy navigation and R-lab tests for BMB830."""

from __future__ import annotations

from PySide6.QtWidgets import QApplication, QComboBox, QStackedWidget

from computational_biomedicine_study_hub.content.bmb830 import (
    MODULE_01_R_FOUNDATIONS,
    MODULE_03_PROBABILITY,
)
from computational_biomedicine_study_hub.courses.bmb830 import (
    BMB830ModuleReaderPage,
    BMB830Page,
)
from computational_biomedicine_study_hub.i18n import AppLocale
from computational_biomedicine_study_hub.ui.widgets import RLabWidget


def _constructed_readers(
    stack: QStackedWidget,
) -> tuple[BMB830ModuleReaderPage, ...]:
    return tuple(
        widget
        for index in range(stack.count())
        if isinstance((widget := stack.widget(index)), BMB830ModuleReaderPage)
    )


def test_bmb830_page_constructs_only_the_initial_reader(qapp: QApplication) -> None:
    del qapp
    page = BMB830Page()
    stack = page.findChild(QStackedWidget, "courseModuleStack")
    selector = page.findChild(QComboBox, "courseModuleSelector")

    assert stack is not None
    assert selector is not None
    assert stack.count() == selector.count() == page.module_count == 3
    assert page.constructed_reader_count == 1
    assert page.has_constructed_reader(0)
    assert not page.has_constructed_reader(2)
    assert len(_constructed_readers(stack)) == 1
    assert page.reader.module is MODULE_01_R_FOUNDATIONS


def test_bmb830_selecting_a_module_constructs_and_reuses_it(
    qapp: QApplication,
) -> None:
    del qapp
    page = BMB830Page()
    first_reader = page.reader

    assert page.select_module_by_id("bmb830.m03")
    final_reader = page.reader

    assert final_reader is not first_reader
    assert final_reader.module is MODULE_03_PROBABILITY
    assert final_reader.property("contentVersion") == "1.0.0"
    assert page.constructed_reader_count == 2

    assert page.select_module(0)
    assert page.reader is first_reader
    assert page.constructed_reader_count == 2
    assert not page.select_module(-1)
    assert not page.select_module(3)


def test_bmb830_page_materializes_danish_and_attaches_r_labs(
    qapp: QApplication,
) -> None:
    del qapp
    page = BMB830Page(AppLocale.DANISH_DENMARK)
    selector = page.findChild(QComboBox, "courseModuleSelector")

    assert selector is not None
    assert page.reader.module.module_id == "bmb830.m01"
    assert page.reader.module.title.startswith("Grundlæggende")
    assert selector.itemText(0).startswith("Modul")

    assert page.reader.select_section_index(2)
    labs = page.reader.findChildren(RLabWidget)
    assert len(labs) == len(page.reader.module.worked_examples) == 2
