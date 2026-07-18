from __future__ import annotations

from PySide6.QtWidgets import QApplication, QComboBox, QFrame, QLabel, QTabWidget

from computational_biomedicine_study_hub.content.dm857 import (
    MODULE_01_FOUNDATIONS,
    MODULE_02_CONDITIONALS,
    MODULE_03_ITERATION,
)
from computational_biomedicine_study_hub.courses.dm857 import DM857Page
from computational_biomedicine_study_hub.ui.pages.module_reader_page import ModuleReaderPage
from computational_biomedicine_study_hub.ui.widgets import (
    GuidedPracticeWidget,
    ObjectiveAssessmentWidget,
)


def test_dm857_page_hosts_completed_modules_without_duplicate_identity_cards(
    qapp: QApplication,
) -> None:
    page = DM857Page()

    context_bar = page.findChild(QFrame, "moduleContextBar")
    context_title = page.findChild(QLabel, "moduleContextTitle")
    selector = page.findChild(QComboBox, "courseModuleSelector")

    assert page.module_count == 3
    assert page.reader.module is MODULE_01_FOUNDATIONS
    assert context_bar is not None
    assert context_title is not None
    assert context_title.text() == MODULE_01_FOUNDATIONS.title
    assert selector is not None
    assert selector.count() == 3
    assert [selector.itemText(index) for index in range(selector.count())] == [
        "Módulo 1",
        "Módulo 2",
        "Módulo 3",
    ]
    assert page.findChild(QFrame, "courseIdentityCard") is None
    assert page.findChild(QFrame, "moduleIdentityCard") is None


def test_dm857_page_switches_between_completed_modules_in_the_same_compact_layout(
    qapp: QApplication,
) -> None:
    page = DM857Page()
    context_title = page.findChild(QLabel, "moduleContextTitle")

    assert context_title is not None
    assert page.select_module(1)
    assert page.current_module_index == 1
    assert page.reader.module is MODULE_02_CONDITIONALS
    assert context_title.text() == MODULE_02_CONDITIONALS.title

    assert page.select_module(2)
    assert page.current_module_index == 2
    assert page.reader.module is MODULE_03_ITERATION
    assert context_title.text() == MODULE_03_ITERATION.title

    assert not page.select_module(-1)
    assert not page.select_module(3)


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


def test_module_reader_uses_module_id_for_the_context_number(qapp: QApplication) -> None:
    reader = ModuleReaderPage(MODULE_03_ITERATION)
    kicker = reader.findChild(QLabel, "moduleContextKicker")

    assert kicker is not None
    assert kicker.text() == "DM857 · Módulo 3"


def test_module_reader_renders_authored_content_and_guided_practice(
    qapp: QApplication,
) -> None:
    reader = ModuleReaderPage(MODULE_01_FOUNDATIONS)
    practice = reader.findChild(GuidedPracticeWidget, "guidedPracticeWidget")

    assert len(reader.findChildren(QFrame, "conceptCard")) == len(MODULE_01_FOUNDATIONS.concepts)
    assert len(reader.findChildren(QFrame, "exampleCard")) == len(
        MODULE_01_FOUNDATIONS.worked_examples
    )
    assert practice is not None
    assert len(practice.exercise_cards) == 4
    assert reader.findChildren(QFrame, "practiceCard") == []
    assert len(reader.findChildren(QFrame, "assessmentCard")) == len(
        MODULE_01_FOUNDATIONS.assessment_items
    )


def test_course_reader_shows_objective_practice_and_complete_assessment(
    qapp: QApplication,
) -> None:
    page = DM857Page()
    reader = page.reader

    assert reader.findChild(ObjectiveAssessmentWidget, "objectiveAssessmentWidget") is not None
    assert reader.findChild(QLabel, "objectiveAssessmentSectionTitle") is not None
    assert reader.findChild(QLabel, "authoredAssessmentSectionTitle") is not None
    assert len(reader.findChildren(QFrame, "assessmentCard")) == len(reader.module.assessment_items)


def test_assessment_reader_does_not_render_answer_feedback(qapp: QApplication) -> None:
    reader = ModuleReaderPage(MODULE_01_FOUNDATIONS)

    assert reader.findChild(QLabel, "assessmentAnswer") is None
    assert reader.findChild(QLabel, "assessmentExplanation") is None
