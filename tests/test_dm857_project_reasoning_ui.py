"""Qt integration tests for project-grounded DM857 technical reasoning."""

# ruff: noqa: I001

from __future__ import annotations

from PySide6.QtWidgets import QCheckBox, QPlainTextEdit, QPushButton

from computational_biomedicine_study_hub.content.technical_stations import (
    DM857_PROJECT_ID,
    DM857_PROJECT_STATIONS,
)
from computational_biomedicine_study_hub.i18n import AppLocale
from computational_biomedicine_study_hub.storage import SQLiteProgressStore
from computational_biomedicine_study_hub.ui.pages.assessments_page import AssessmentsPage
from computational_biomedicine_study_hub.ui.pages.dm857_capstone_page import (
    DM857CapstonePage,
)


_PROJECT_RESPONSE = """<ARTIFACT>
def classify(value: float, threshold: float) -> bool:
    return value >= threshold

assert classify(4.2, 4.0) is True
</ARTIFACT>

<ANALYSIS>
The function accepts two finite numeric values and returns a Boolean. Equality belongs to the
positive branch because the implementation uses >=. It has no intentional side effects, but the
current contract does not reject NaN, infinity, strings, or a threshold expressed in incompatible
units. The shown assertion verifies one normal case only. Boundary equality, values below the
threshold, invalid types, non-finite values, and unit validation require explicit tests or a stated
upstream validation contract. Passing this test establishes implementation behaviour for one input;
it does not establish that the threshold is clinically valid or scientifically justified.
</ANALYSIS>"""


def test_capstone_embeds_eight_project_grounded_stations(qtbot) -> None:  # type: ignore[no-untyped-def]
    page = DM857CapstonePage(None, AppLocale.ENGLISH)
    qtbot.addWidget(page)

    panel = page.technical_station_panel

    assert panel.current_station == DM857_PROJECT_STATIONS[0]
    assert panel.current_station is not None
    assert panel.current_station.lab_id == DM857_PROJECT_ID
    assert panel.current_station.course_code == "DM857"
    assert len(DM857_PROJECT_STATIONS) == 8


def test_project_station_routes_real_code_to_socratic_mentor(qtbot) -> None:  # type: ignore[no-untyped-def]
    page = DM857CapstonePage(None, AppLocale.ENGLISH)
    qtbot.addWidget(page)
    panel = page.technical_station_panel
    editor = panel.findChild(QPlainTextEdit, "technicalStationResponse")
    mentor_button = panel.findChild(QPushButton, "technicalStationMentor")
    assert editor is not None
    assert mentor_button is not None

    editor.setPlainText(_PROJECT_RESPONSE)
    with qtbot.waitSignal(page.mentor_requested):
        mentor_button.click()

    context = page.mentor_context()
    assert "def classify" in context
    assert "Passing this test establishes implementation behaviour" in context
    assert "do not role-play an examiner" in context
    assert "official grading rubric are not available" in context
    assert panel.current_attempt is not None
    assert panel.current_attempt.hint_level == 1


def test_project_reasoning_self_review_persists_with_capstone(qtbot) -> None:  # type: ignore[no-untyped-def]
    progress = SQLiteProgressStore(":memory:")
    try:
        page = DM857CapstonePage(progress, AppLocale.ENGLISH)
        qtbot.addWidget(page)
        panel = page.technical_station_panel
        editor = panel.findChild(QPlainTextEdit, "technicalStationResponse")
        review_button = panel.findChild(QPushButton, "technicalStationReview")
        assert editor is not None
        assert review_button is not None

        editor.setPlainText(_PROJECT_RESPONSE)
        checkboxes = panel.findChildren(QCheckBox)
        assert len(checkboxes) == len(DM857_PROJECT_STATIONS[0].criteria)
        for checkbox in checkboxes:
            checkbox.setChecked(True)
        review_button.click()
        page.persist()

        restored = DM857CapstonePage(progress, AppLocale.ENGLISH)
        qtbot.addWidget(restored)
        restored_attempt = restored.technical_station_panel.current_attempt
        assert restored_attempt is not None
        assert restored_attempt.reviewed
        assert "def classify" in restored_attempt.response
    finally:
        progress.close()


def test_assessment_workspace_forwards_dm857_mentor_request(qtbot) -> None:  # type: ignore[no-untyped-def]
    page = AssessmentsPage(None, AppLocale.ENGLISH)
    qtbot.addWidget(page)
    assert page.select_assessment("dm857.capstone")
    panel = page.dm857_page.technical_station_panel
    editor = panel.findChild(QPlainTextEdit, "technicalStationResponse")
    mentor_button = panel.findChild(QPushButton, "technicalStationMentor")
    assert editor is not None
    assert mentor_button is not None
    editor.setPlainText(_PROJECT_RESPONSE)

    with qtbot.waitSignal(page.mentor_requested):
        mentor_button.click()

    assert "def classify" in page.mentor_context()
