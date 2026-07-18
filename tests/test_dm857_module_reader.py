from __future__ import annotations

from PySide6.QtCore import Qt
from PySide6.QtWidgets import QApplication, QFrame, QPushButton, QRadioButton, QTabWidget
from pytestqt.qtbot import QtBot

from computational_biomedicine_study_hub.content.dm857 import MODULE_01_FOUNDATIONS
from computational_biomedicine_study_hub.courses.dm857 import DM857Page
from computational_biomedicine_study_hub.ui.assessment_session_widget import (
    AssessmentSessionWidget,
)
from computational_biomedicine_study_hub.ui.pages.module_reader_page import ModuleReaderPage


def test_dm857_page_hosts_module_without_redundant_course_blocks(
    qapp: QApplication,
) -> None:
    page = DM857Page()

    reader = page.findChild(ModuleReaderPage, "moduleReaderPage")

    assert reader is not None
    assert reader.module is MODULE_01_FOUNDATIONS
    assert page.findChild(QFrame, "courseIdentityCard") is None
    assert page.findChild(QPushButton, "moduleSelectorButton") is None
    assert page.findChild(QFrame, "moduleCompactBar") is not None


def test_module_reader_exposes_five_study_sections(qapp: QApplication) -> None:
    page = DM857Page()
    reader = page.reader
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


def test_module_reader_renders_all_authored_learning_cards(qapp: QApplication) -> None:
    page = DM857Page()
    reader = page.reader

    assert len(reader.findChildren(QFrame, "conceptCard")) == len(MODULE_01_FOUNDATIONS.concepts)
    assert len(reader.findChildren(QFrame, "exampleCard")) == len(
        MODULE_01_FOUNDATIONS.worked_examples
    )
    assert len(reader.findChildren(QFrame, "practiceCard")) == len(
        MODULE_01_FOUNDATIONS.practice_exercises
    )
    assert reader.findChildren(QFrame, "assessmentCard") == []


def test_assessment_widget_uses_a_larger_random_bank(qapp: QApplication) -> None:
    page = DM857Page()
    widget = page.findChild(AssessmentSessionWidget, "assessmentSessionWidget")

    assert widget is not None
    assert widget.session.question_count == 6
    assert len(widget.session.item_ids) == 6
    assert len(set(widget.session.item_ids)) == 6


def test_student_can_select_and_autocorrect_an_answer(
    qapp: QApplication,
    qtbot: QtBot,
) -> None:
    page = DM857Page()
    widget = page.findChild(AssessmentSessionWidget, "assessmentSessionWidget")
    assert widget is not None

    correct_answer = widget.session.current_question.item.correct_answers[0]
    option = next(
        button
        for button in widget.findChildren(QRadioButton, "assessmentOption")
        if button.text() == correct_answer
    )
    check_button = widget.findChild(QPushButton, "primaryActionButton")
    assert check_button is not None

    qtbot.mouseClick(option, Qt.MouseButton.LeftButton)
    assert check_button.isEnabled()
    qtbot.mouseClick(check_button, Qt.MouseButton.LeftButton)

    assert widget.session.answered_count == 1
    assert widget.session.score == 1
    assert widget.feedback_text.startswith("Correcto.")
    assert not option.isEnabled()
