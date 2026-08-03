from __future__ import annotations

from collections.abc import Callable

import pytest
from PySide6.QtWidgets import QApplication, QFrame, QLabel

from computational_biomedicine_study_hub.courses.bmb830 import BMB830Page
from computational_biomedicine_study_hub.courses.bmb831 import BMB831Page
from computational_biomedicine_study_hub.courses.dm847 import DM847Page
from computational_biomedicine_study_hub.courses.dm857 import DM857Page
from computational_biomedicine_study_hub.ui.pages.module_reader_page import ModuleReaderPage
from computational_biomedicine_study_hub.ui.widgets import ObjectiveAssessmentWidget

CoursePage = DM857Page | DM847Page | BMB830Page | BMB831Page
CoursePageFactory = Callable[[], CoursePage]


@pytest.mark.parametrize(
    "page_factory",
    (
        DM857Page,
        DM847Page,
        BMB830Page,
        BMB831Page,
    ),
)
def test_course_assessment_tabs_show_only_questions_in_the_active_evaluator(
    qapp: QApplication,
    page_factory: CoursePageFactory,
) -> None:
    page = page_factory()
    reader = page.reader
    assert isinstance(reader, ModuleReaderPage)

    assert reader.select_section_index(4)

    assert reader.findChild(ObjectiveAssessmentWidget) is not None
    assert reader.findChild(QLabel, "authoredAssessmentSectionTitle") is None
    assert reader.findChildren(QFrame, "assessmentCard") == []
