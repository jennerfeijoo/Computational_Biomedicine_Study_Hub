from __future__ import annotations

from PySide6.QtWidgets import QApplication, QLabel

from computational_biomedicine_study_hub.content.dm857 import OBJECTIVE_QUESTION_BANK
from computational_biomedicine_study_hub.ui.widgets import ObjectiveAssessmentWidget


def test_objective_assessment_header_omits_redundant_bank_metadata(
    qapp: QApplication,
) -> None:
    widget = ObjectiveAssessmentWidget(OBJECTIVE_QUESTION_BANK)

    assert widget.findChild(QLabel, "objectiveAssessmentTitle") is not None
    assert widget.findChild(QLabel, "objectiveAssessmentScore") is not None
    assert widget.findChild(QLabel, "objectiveAssessmentMetadata") is None
