"""Integration tests for DM857 module navigation and lazy reader sections."""

from __future__ import annotations

from PySide6.QtWidgets import QApplication, QComboBox, QFrame, QLabel, QTabWidget

from computational_biomedicine_study_hub.content.dm857 import (
    MODULE_01_FOUNDATIONS,
    MODULE_09_RECURSION,
    MODULES,
)
from computational_biomedicine_study_hub.courses.dm857 import DM857Page
from computational_biomedicine_study_hub.ui.pages.module_reader_page import ModuleReaderPage
from computational_biomedicine_study_hub.ui.widgets import (
    GuidedPracticeWidget,
    ObjectiveAssessmentWidget,
)

EXPECTED_MODULES = MODULES


def test_dm857_page_hosts_completed_modules_without_duplicate_identity_cards(
    qapp: QApplication,
) -> None:
    page = DM857Page()

    context_bar = page.findChild(QFrame, "moduleContextBar")
    context_title = page.findChild(QLabel, "moduleContextTitle")
    selector = page.findChild(QComboBox, "courseModuleSelector")

    assert page.module_count == len(EXPECTED_MODULES)
    assert page.reader.module is MODULE_01_FOUNDATIONS
    assert context_bar is not None
    assert context_title is not None
    assert context_title.text() == MODULE_01_FOUNDATIONS.title
    assert selector is not None
    assert selector.count() == len(EXPECTED_MODULES)
    assert [selector.itemText(index) for index in range(selector.count())] == [
        f"Módulo {number}" for number in range(1, len(EXPECTED_MODULES) + 1)
    ]
    assert page.findChild(QFrame, "courseIdentityCard") is None
    assert page.findChild(QFrame, "moduleIdentityCard") is None


def test_dm857_page_switches_between_completed_modules_in_the_same_compact_layout(
    qapp: QApplication,
) -> None:
    page = DM857Page()
    context_title = page.findChild(QLabel, "moduleContextTitle")
    assert context_title is not None

    for index, module in enumerate(EXPECTED_MODULES):
        assert page.select_module(index)
        assert page.current_module_index == index
        assert page.reader.module is module
        assert context_title.text() == module.title

    assert not page.select_module(-1)
    assert not page.select_module(len(EXPECTED_MODULES))


def test_module_reader_exposes_five_lazy_study_sections(qapp: QApplication) -> None:
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
    assert reader.constructed_section_count == 1
    assert reader.has_constructed_section("Resumen")
    assert not reader.has_constructed_section("Ejemplos")
    assert reader.select_section("Ejemplos")
    assert reader.current_section == "Ejemplos"
    assert reader.constructed_section_count == 2
    assert reader.has_constructed_section("Ejemplos")
    assert reader.select_section("Resumen")
    assert reader.select_section("Ejemplos")
    assert reader.constructed_section_count == 2
    assert not reader.select_section("Sección inexistente")


def test_module_reader_uses_module_id_for_the_context_number(qapp: QApplication) -> None:
    reader = ModuleReaderPage(MODULE_09_RECURSION)
    kicker = reader.findChild(QLabel, "moduleContextKicker")

    assert kicker is not None
    assert kicker.text() == "DM857 · Módulo 9"


def test_module_reader_constructs_authored_sections_only_when_selected(
    qapp: QApplication,
) -> None:
    reader = ModuleReaderPage(MODULE_01_FOUNDATIONS)

    assert reader.findChildren(QFrame, "conceptCard") == []
    assert reader.findChildren(QFrame, "exampleCard") == []
    assert reader.findChild(GuidedPracticeWidget, "guidedPracticeWidget") is None
    assert reader.findChildren(QFrame, "assessmentCard") == []

    assert reader.select_section("Conceptos")
    assert len(reader.findChildren(QFrame, "conceptCard")) == len(MODULE_01_FOUNDATIONS.concepts)

    assert reader.select_section("Ejemplos")
    assert len(reader.findChildren(QFrame, "exampleCard")) == len(
        MODULE_01_FOUNDATIONS.worked_examples
    )

    assert reader.select_section("Práctica")
    practice = reader.findChild(GuidedPracticeWidget, "guidedPracticeWidget")
    assert practice is not None
    assert len(practice.exercise_cards) == 4
    assert reader.findChildren(QFrame, "practiceCard") == []

    assert reader.select_section("Evaluación")
    assert len(reader.findChildren(QFrame, "assessmentCard")) == len(
        MODULE_01_FOUNDATIONS.assessment_items
    )
    assert reader.constructed_section_count == 5


def test_course_reader_shows_objective_practice_and_complete_assessment(
    qapp: QApplication,
) -> None:
    page = DM857Page()

    for index in range(page.module_count):
        assert page.select_module(index)
        reader = page.reader
        assert reader.select_section("Evaluación")
        assert reader.findChild(ObjectiveAssessmentWidget, "objectiveAssessmentWidget") is not None
        assert reader.findChild(QLabel, "objectiveAssessmentSectionTitle") is not None
        assert reader.findChild(QLabel, "authoredAssessmentSectionTitle") is not None
        assert len(reader.findChildren(QFrame, "assessmentCard")) == len(
            reader.module.assessment_items
        )


def test_assessment_reader_does_not_render_answer_feedback(qapp: QApplication) -> None:
    reader = ModuleReaderPage(MODULE_01_FOUNDATIONS)
    assert reader.select_section("Evaluación")

    assert reader.findChild(QLabel, "assessmentAnswer") is None
    assert reader.findChild(QLabel, "assessmentExplanation") is None
