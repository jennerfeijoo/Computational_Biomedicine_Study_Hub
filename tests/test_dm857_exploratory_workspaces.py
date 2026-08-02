from __future__ import annotations

from PySide6.QtWidgets import QApplication

from computational_biomedicine_study_hub.content.models import PracticeExercise
from computational_biomedicine_study_hub.courses.dm857 import DM857Page
from computational_biomedicine_study_hub.learning.activity_types import ActivityType
from computational_biomedicine_study_hub.ui.widgets import ObjectiveAssessmentWidget
from computational_biomedicine_study_hub.ui.widgets.dm857_practice_widget import DM857PracticeCard


def test_dm857_code_practice_starts_blank_and_executable(qapp: QApplication) -> None:
    exercise = PracticeExercise(
        exercise_id="dm857.test.exploration",
        activity_type=ActivityType.DATA_INTERPRETATION,
        prompt="Change the value and inspect the output.",
        hints=("Print the value.",),
        solution="print(3)",
        explanation="The printed value follows the assigned variable.",
        starter_code="value = 3\nprint(value)",
    )

    card = DM857PracticeCard(1, exercise)

    assert card.answer_text == ""
    assert card.exploration_lab is not None
    card.exploration_lab.set_source("value = 7\nprint(value)")
    assert card.answer_text.endswith("print(value)")
    assert "7" in card.answer_text
    assert not card.solution_revealed


def test_dm857_assessment_tab_does_not_dump_static_question_cards(
    qapp: QApplication,
) -> None:
    page = DM857Page()
    reader = page.reader

    assert reader.select_section_index(4)

    assert reader.findChild(ObjectiveAssessmentWidget) is not None
    assert reader.findChild(type(reader), "authoredAssessmentSectionTitle") is None
    assert not reader.findChildren(type(page), "assessmentCard")
