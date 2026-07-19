from __future__ import annotations

from datetime import UTC, datetime, timedelta
from pathlib import Path

from PySide6.QtCore import QSettings
from PySide6.QtWidgets import (
    QApplication,
    QComboBox,
    QLabel,
    QPushButton,
    QStackedWidget,
    QTabWidget,
)

from computational_biomedicine_study_hub.content.dm857 import LOCALIZED_BUNDLES
from computational_biomedicine_study_hub.courses.dm857 import DM857Page
from computational_biomedicine_study_hub.i18n import AppLocale
from computational_biomedicine_study_hub.learning.activity_types import ActivityType
from computational_biomedicine_study_hub.learning.progress import (
    AttemptOutcome,
    AttemptRecord,
    LearningItemKind,
)
from computational_biomedicine_study_hub.persistence import SQLiteProgressRepository
from computational_biomedicine_study_hub.ui.main_window import MainWindow
from computational_biomedicine_study_hub.ui.widgets import (
    GuidedPracticeWidget,
    ObjectiveAssessmentWidget,
)


def _repository(tmp_path: Path) -> SQLiteProgressRepository:
    return SQLiteProgressRepository(tmp_path / "progress.sqlite3")


def test_objective_session_and_selected_id_survive_restart_and_locale_change(
    qapp: QApplication,
    tmp_path: Path,
) -> None:
    localized = LOCALIZED_BUNDLES[0]
    spanish_bundle = localized.materialize(AppLocale.SPANISH_SPAIN)
    english_bundle = localized.materialize(AppLocale.ENGLISH)
    database_path = tmp_path / "progress.sqlite3"
    spanish = ObjectiveAssessmentWidget(
        spanish_bundle.objective_question_bank,
        locale=AppLocale.SPANISH_SPAIN,
        repository=SQLiteProgressRepository(database_path),
        course_code="DM857",
        module_id=spanish_bundle.module.module_id,
        content_version=spanish_bundle.content_version,
    )
    first_ids = spanish.current_item_ids
    first_card = spanish.question_cards[0]
    spanish_item = next(
        item
        for item in spanish_bundle.objective_question_bank
        if item.item_id == first_card.item_id
    )
    selected_id = spanish_item.correct_option_ids[0]
    assert first_card.choose_option(selected_id)
    first_card.check_answer()

    english = ObjectiveAssessmentWidget(
        english_bundle.objective_question_bank,
        locale=AppLocale.ENGLISH,
        repository=SQLiteProgressRepository(database_path),
        course_code="DM857",
        module_id=english_bundle.module.module_id,
        content_version=english_bundle.content_version,
    )

    assert english.current_item_ids == first_ids
    restored = english.question_cards[0]
    assert restored.item_id == first_card.item_id
    assert restored.is_answered
    assert restored.selected_option_id == selected_id
    assert restored.feedback_text.startswith("Correct.")
    assert english.score_text == "1 correct · 1/6"


def test_guided_practice_restores_session_response_and_partial_state(
    qapp: QApplication,
    tmp_path: Path,
) -> None:
    localized = LOCALIZED_BUNDLES[0]
    spanish_bundle = localized.materialize(AppLocale.SPANISH_SPAIN)
    english_bundle = localized.materialize(AppLocale.ENGLISH)
    database_path = tmp_path / "progress.sqlite3"
    spanish = GuidedPracticeWidget(
        spanish_bundle.module.practice_exercises,
        locale=AppLocale.SPANISH_SPAIN,
        repository=SQLiteProgressRepository(database_path),
        course_code="DM857",
        module_id=spanish_bundle.module.module_id,
        content_version=spanish_bundle.content_version,
    )
    first_ids = spanish.current_exercise_ids
    card = spanish.exercise_cards[0]
    card.set_answer_text("stable learner response")
    card.reveal_solution()
    card.mark_partial()

    english = GuidedPracticeWidget(
        english_bundle.module.practice_exercises,
        locale=AppLocale.ENGLISH,
        repository=SQLiteProgressRepository(database_path),
        course_code="DM857",
        module_id=english_bundle.module.module_id,
        content_version=english_bundle.content_version,
    )

    assert english.current_exercise_ids == first_ids
    restored = english.exercise_cards[0]
    assert restored.exercise_id == card.exercise_id
    assert restored.answer_text == "stable learner response"
    assert restored.assessment_state == "partial"
    assert restored.solution_revealed


def test_main_window_language_change_restores_practice_answer_end_to_end(
    qapp: QApplication,
    tmp_path: Path,
) -> None:
    settings = QSettings(
        str(tmp_path / "application.ini"),
        QSettings.Format.IniFormat,
    )
    window = MainWindow(settings=settings)
    window.navigate("course/dm857")
    stack = window.findChild(QStackedWidget, "mainPageStack")
    assert stack is not None
    page = stack.currentWidget()
    assert isinstance(page, DM857Page)
    assert page.reader.select_section_index(3)
    practice = page.reader.findChild(GuidedPracticeWidget, "guidedPracticeWidget")
    assert practice is not None
    item_ids = practice.current_exercise_ids
    card = practice.exercise_cards[0]
    card.set_answer_text("answer retained by stable exercise ID")
    card.reveal_solution()
    card.mark_review()

    english_button = next(
        button
        for button in window.findChildren(QPushButton, "languageButton")
        if button.text() == "EN"
    )
    english_button.click()
    qapp.processEvents()

    translated_page = stack.currentWidget()
    assert isinstance(translated_page, DM857Page)
    translated_practice = translated_page.reader.findChild(
        GuidedPracticeWidget,
        "guidedPracticeWidget",
    )
    assert translated_practice is not None
    assert translated_practice.current_exercise_ids == item_ids
    restored = translated_practice.exercise_cards[0]
    assert restored.answer_text == "answer retained by stable exercise ID"
    assert restored.assessment_state == "review"


def test_course_continue_button_opens_most_recent_module_and_shows_progress(
    qapp: QApplication,
    tmp_path: Path,
) -> None:
    repository = _repository(tmp_path)
    earlier = datetime(2026, 7, 19, 10, 0, tzinfo=UTC)
    for attempt_id, module_id, created_at in (
        ("a1", "dm857.m01", earlier),
        ("a2", "dm857.m05", earlier + timedelta(hours=1)),
    ):
        repository.record_attempt(
            AttemptRecord(
                attempt_id=attempt_id,
                course_code="DM857",
                module_id=module_id,
                item_id=f"{module_id}.item",
                item_kind=LearningItemKind.PRACTICE,
                activity_type=ActivityType.SHORT_ANSWER,
                outcome=AttemptOutcome.SOLVED,
                locale="en",
                content_version="test",
                created_at=created_at,
                is_correct=True,
                score=1.0,
            )
        )
    page = DM857Page(AppLocale.ENGLISH, progress_repository=repository)

    page.continue_learning()

    assert page.current_module_index == 4
    summary = page.findChild(QLabel, "courseProgressSummary")
    assert summary is not None
    assert "1 attempts" in summary.text()


def test_learning_controls_expose_accessible_names(
    qapp: QApplication,
    tmp_path: Path,
) -> None:
    page = DM857Page(
        AppLocale.DANISH_DENMARK,
        progress_repository=_repository(tmp_path),
    )

    selector = page.findChild(QComboBox, "courseModuleSelector")
    continue_button = page.findChild(QPushButton, "continueCourseButton")
    tabs = page.reader.findChild(QTabWidget, "moduleTabs")
    assert selector is not None
    assert continue_button is not None
    assert tabs is not None
    assert selector.accessibleName()
    assert continue_button.accessibleName()
    assert tabs.accessibleName() == page.reader.module.title
