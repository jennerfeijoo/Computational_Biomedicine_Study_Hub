from __future__ import annotations

import random
from datetime import UTC, datetime, timedelta
from pathlib import Path

from PySide6.QtWidgets import QLabel

from computational_biomedicine_study_hub.i18n import AppLocale
from computational_biomedicine_study_hub.learning.academic_catalog import AcademicCatalog
from computational_biomedicine_study_hub.learning.activity_types import ActivityType
from computational_biomedicine_study_hub.learning.progress import (
    LearningItemKind,
    MasteryState,
    ReviewSchedule,
)
from computational_biomedicine_study_hub.learning.spaced_repetition import ReviewRating
from computational_biomedicine_study_hub.persistence import SQLiteProgressRepository
from computational_biomedicine_study_hub.ui.activities import (
    MultipleChoiceActivityWidget,
)
from computational_biomedicine_study_hub.ui.learning_page_copy import (
    validate_learning_page_copy,
)
from computational_biomedicine_study_hub.ui.pages.assessments_page import AssessmentsPage
from computational_biomedicine_study_hub.ui.pages.flashcards_page import FlashcardsPage
from computational_biomedicine_study_hub.ui.pages.glossary_page import GlossaryPage
from computational_biomedicine_study_hub.ui.pages.review_page import ReviewPage


def _repository(tmp_path: Path) -> SQLiteProgressRepository:
    return SQLiteProgressRepository(tmp_path / "progress.sqlite3")


def test_learning_page_copy_is_complete_in_all_locales() -> None:
    validate_learning_page_copy()


def test_assessments_page_reuses_authored_items_and_persists_wrong_answer(
    qtbot,
    tmp_path: Path,
) -> None:
    catalog = AcademicCatalog(locale=AppLocale.ENGLISH)
    repository = _repository(tmp_path)
    page = AssessmentsPage(catalog, repository, locale=AppLocale.ENGLISH)
    qtbot.addWidget(page)
    page.type_selector.setCurrentIndex(
        page.type_selector.findData(ActivityType.MULTIPLE_CHOICE.value)
    )

    page.start_session()

    assert page.session is not None
    assert page.rendered_activities
    widget = page.rendered_activities[0]
    assert isinstance(widget, MultipleChoiceActivityWidget)
    source = next(
        item
        for item in catalog.assessment_items(
            course_code="DM857",
            module_id="dm857.m01",
        )
        if item.item_id == widget.item_id
    )
    wrong_index = next(
        index
        for index, option_id in enumerate(source.option_ids)
        if option_id not in source.correct_option_ids
    )
    widget.option_controls[wrong_index].setChecked(True)
    widget.submit_answer()

    attempts = repository.list_attempts(item_id=widget.item_id)
    assert len(attempts) == 1
    assert attempts[0].is_correct is False
    assert attempts[0].locale == "en"
    assert page.session is not None
    assert widget.item_id in page.session.answered_item_ids
    due = repository.list_due_reviews(due_at=datetime.now(UTC) + timedelta(seconds=1))
    assert tuple(item.item_id for item in due) == (widget.item_id,)


def test_assessments_page_restores_open_session_after_locale_rebuild(
    qtbot,
    tmp_path: Path,
) -> None:
    repository = _repository(tmp_path)
    spanish = AssessmentsPage(
        AcademicCatalog(locale=AppLocale.SPANISH_SPAIN),
        repository,
        locale=AppLocale.SPANISH_SPAIN,
    )
    qtbot.addWidget(spanish)
    spanish.start_session()
    assert spanish.session is not None
    session_id = spanish.session.session_id
    item_ids = spanish.session.item_ids

    english = AssessmentsPage(
        AcademicCatalog(locale=AppLocale.ENGLISH),
        SQLiteProgressRepository(repository.database_path),
        locale=AppLocale.ENGLISH,
    )
    qtbot.addWidget(english)

    assert english.session is not None
    assert english.session.session_id == session_id
    assert english.session.item_ids == item_ids
    assert tuple(widget.item_id for widget in english.rendered_activities) == item_ids


def test_flashcard_rating_persists_schedule_and_advances_card(
    qtbot,
    tmp_path: Path,
) -> None:
    repository = _repository(tmp_path)
    page = FlashcardsPage(
        AcademicCatalog(locale=AppLocale.DANISH_DENMARK),
        repository,
        locale=AppLocale.DANISH_DENMARK,
        rng=random.Random(857),
    )
    qtbot.addWidget(page)
    first = page.current_card
    assert first is not None

    page.reveal()
    page.rate(ReviewRating.GOOD)

    persisted = repository.get_flashcard_progress(
        first.course_code,
        first.module_id,
        first.card_id,
    )
    assert persisted is not None
    assert persisted.repetitions == 1
    assert persisted.interval_days == 1
    assert page.current_card != first


def test_review_page_filters_due_queue_and_reschedules_selected_item(
    qtbot,
    tmp_path: Path,
) -> None:
    repository = _repository(tmp_path)
    repository.save_review_schedule(
        ReviewSchedule(
            course_code="DM857",
            module_id="dm857.m01",
            item_id="m01.p01",
            item_kind=LearningItemKind.PRACTICE,
            mastery_state=MasteryState.LEARNING,
            repetitions=0,
            interval_days=0,
            easiness=2.5,
            due_at=datetime.now(UTC) - timedelta(minutes=1),
        )
    )
    page = ReviewPage(
        AcademicCatalog(locale=AppLocale.SPANISH_SPAIN),
        repository,
    )
    qtbot.addWidget(page)

    assert tuple(item.item_id for item in page.queue) == ("m01.p01",)
    page.rate_selected(ReviewRating.GOOD)
    assert page.queue == ()
    assert page.findChild(QLabel, "reviewEmptyState") is not None


def test_review_can_add_low_mastery_concepts_to_an_empty_queue(
    qtbot,
    tmp_path: Path,
) -> None:
    page = ReviewPage(AcademicCatalog(), _repository(tmp_path))
    qtbot.addWidget(page)
    assert page.queue == ()

    page.add_new_concepts()

    assert 1 <= len(page.queue) <= 10
    assert all(item.item_kind is LearningItemKind.CONCEPT for item in page.queue)


def test_glossary_searches_models_and_emits_stable_source_identity(qtbot) -> None:
    page = GlossaryPage(AcademicCatalog(locale=AppLocale.ENGLISH), locale=AppLocale.ENGLISH)
    qtbot.addWidget(page)

    page.search.setText("recursion")

    assert page.entries
    assert all(
        "recurs"
        in " ".join(
            (
                entry.term,
                entry.definition,
                *entry.tags,
                *entry.synonyms,
                *entry.related_terms,
            )
        ).casefold()
        for entry in page.entries
    )
    with qtbot.waitSignal(page.module_requested, timeout=1000) as signal:
        page.open_source_module()
    assert signal.args[0] == "DM857"
    assert str(signal.args[1]).startswith("dm857.")


def test_global_pages_have_explicit_empty_states(qtbot, tmp_path: Path) -> None:
    catalog = AcademicCatalog(bundle_catalogs=())
    repository = _repository(tmp_path)
    assessment = AssessmentsPage(catalog, repository)
    flashcards = FlashcardsPage(catalog, repository)
    glossary = GlossaryPage(catalog)
    review = ReviewPage(catalog, repository)
    for page in (assessment, flashcards, glossary, review):
        qtbot.addWidget(page)

    assert assessment.findChild(QLabel, "assessmentEmptyState") is not None
    assert not flashcards.empty_label.isHidden()
    assert not glossary.empty_label.isHidden()
    assert not review.empty_label.isHidden()
