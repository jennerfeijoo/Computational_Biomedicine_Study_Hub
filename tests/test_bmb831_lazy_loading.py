"""Lazy navigation and R-lab tests for BMB831."""

from __future__ import annotations

from PySide6.QtWidgets import QApplication, QComboBox, QStackedWidget

from computational_biomedicine_study_hub.content.bmb831 import (
    MODULE_01_SYNTHEA_WORKFLOWS,
    MODULE_03_DIFFERENTIAL_MODELING,
)
from computational_biomedicine_study_hub.courses.bmb831 import (
    BMB831ModuleReaderPage,
    BMB831Page,
)
from computational_biomedicine_study_hub.i18n import AppLocale
from computational_biomedicine_study_hub.ui.widgets import RLabWidget


def _constructed_readers(
    stack: QStackedWidget,
) -> tuple[BMB831ModuleReaderPage, ...]:
    return tuple(
        widget
        for index in range(stack.count())
        if isinstance((widget := stack.widget(index)), BMB831ModuleReaderPage)
    )


def test_bmb831_page_constructs_readers_lazily(qapp: QApplication) -> None:
    del qapp
    page = BMB831Page()
    stack = page.findChild(QStackedWidget, "courseModuleStack")
    selector = page.findChild(QComboBox, "courseModuleSelector")

    assert stack is not None
    assert selector is not None
    assert stack.count() == selector.count() == page.module_count == 3
    assert page.constructed_reader_count == 1
    assert page.has_constructed_reader(0)
    assert not page.has_constructed_reader(1)
    assert not page.has_constructed_reader(2)
    assert len(_constructed_readers(stack)) == 1
    assert page.reader.module is MODULE_01_SYNTHEA_WORKFLOWS
    assert not page.select_module(-1)
    assert not page.select_module(3)

    assert page.select_module(2)
    assert page.current_module_index == 2
    assert page.reader.module is MODULE_03_DIFFERENTIAL_MODELING
    assert page.constructed_reader_count == 2
    assert page.has_constructed_reader(2)
    assert not page.has_constructed_reader(1)
    assert len(_constructed_readers(stack)) == 2


def test_bmb831_page_materializes_danish_and_attaches_r_labs(
    qapp: QApplication,
) -> None:
    del qapp
    page = BMB831Page(AppLocale.DANISH_DENMARK)
    selector = page.findChild(QComboBox, "courseModuleSelector")

    assert selector is not None
    assert page.reader.module.module_id == "bmb831.m01"
    assert page.reader.module.title.startswith("Reproducerbare")
    assert selector.itemText(0).startswith("Modul")

    assert page.select_module_by_id("bmb831.m02")
    assert page.reader.module.title.startswith("Omikmatricer")
    assert page.reader.select_section_index(2)
    labs = page.reader.findChildren(RLabWidget)
    assert len(labs) == len(page.reader.module.worked_examples) == 2
