from __future__ import annotations

from PySide6.QtWidgets import QApplication, QFrame, QLabel, QPushButton, QTabWidget

from computational_biomedicine_study_hub.content.dm857 import MODULE_01_FOUNDATIONS
from computational_biomedicine_study_hub.courses.dm857 import DM857Page
from computational_biomedicine_study_hub.ui.pages.module_reader_page import ModuleReaderPage


def test_dm857_page_hosts_the_first_authored_module(qapp: QApplication) -> None:
    page = DM857Page()

    reader = page.findChild(ModuleReaderPage, "moduleReaderPage")
    selector = page.findChild(QPushButton, "moduleSelectorButton")

    assert reader is not None
    assert reader.module is MODULE_01_FOUNDATIONS
    assert selector is not None
    assert selector.isChecked()
    assert not selector.isEnabled()
    assert MODULE_01_FOUNDATIONS.title in selector.text()


def test_module_reader_exposes_five_study_sections(qapp: QApplication) -> None:
    reader = ModuleReaderPage(MODULE_01_FOUNDATIONS)
    tabs = reader.findChild(QTabWidget, "moduleTabs")

    assert tabs is not None
    assert tabs.count() == 5
    assert [tabs.tabText(index) for index in range(tabs.count())] == [
        "Resumen",
        "Conceptos",
        "Ejemplos",
        "Práctica",
        "Evaluación",
    ]
    assert reader.current_section == "Resumen"
    assert reader.select_section("Ejemplos")
    assert reader.current_section == "Ejemplos"
    assert not reader.select_section("Sección inexistente")


def test_module_reader_renders_all_authored_content_cards(qapp: QApplication) -> None:
    reader = ModuleReaderPage(MODULE_01_FOUNDATIONS)

    assert len(reader.findChildren(QFrame, "conceptCard")) == len(MODULE_01_FOUNDATIONS.concepts)
    assert len(reader.findChildren(QFrame, "exampleCard")) == len(
        MODULE_01_FOUNDATIONS.worked_examples
    )
    assert len(reader.findChildren(QFrame, "practiceCard")) == len(
        MODULE_01_FOUNDATIONS.practice_exercises
    )
    assert len(reader.findChildren(QFrame, "assessmentCard")) == len(
        MODULE_01_FOUNDATIONS.assessment_items
    )


def test_assessment_reader_does_not_render_answer_feedback(qapp: QApplication) -> None:
    reader = ModuleReaderPage(MODULE_01_FOUNDATIONS)

    assert reader.findChild(QLabel, "assessmentAnswer") is None
    assert reader.findChild(QLabel, "assessmentExplanation") is None
