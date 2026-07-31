from __future__ import annotations

from datetime import UTC, datetime, timedelta

from PySide6.QtWidgets import QApplication, QLabel, QPushButton

from computational_biomedicine_study_hub.i18n import AppLocale
from computational_biomedicine_study_hub.learning.progress import (
    AttemptRecord,
    ConfidenceLevel,
)
from computational_biomedicine_study_hub.storage import SQLiteProgressStore
from computational_biomedicine_study_hub.ui.pages.review_page import ReviewPage
from computational_biomedicine_study_hub.ui.widgets import AdaptiveReviewSessionWidget

_NOW = datetime(2026, 7, 31, 8, 0, tzinfo=UTC)


def _due_attempt(
    attempt_id: str,
    *,
    course_code: str = "DM847",
    module_id: str = "dm847.m01",
    objective_id: str = "m01.o1",
) -> AttemptRecord:
    return AttemptRecord(
        attempt_id=attempt_id,
        course_code=course_code,
        module_id=module_id,
        objective_id=objective_id,
        item_id="seed-item",
        activity_type="multiple_choice",
        answer="wrong",
        is_correct=False,
        confidence=ConfidenceLevel.HIGH,
        hints_used=0,
        response_time_ms=1000,
        solution_revealed=False,
        attempted_at=_NOW - timedelta(days=2),
    )


def test_review_page_starts_and_persists_an_adaptive_question(
    qapp: QApplication,
) -> None:
    with SQLiteProgressStore(":memory:") as store:
        store.record_and_update(_due_attempt("seed"))
        page = ReviewPage(store, AppLocale.ENGLISH, clock=lambda: _NOW)
        start = page.findChild(QPushButton, "adaptiveReviewStartButton")

        assert start is not None
        assert start.isEnabled()
        assert page.pending_session is not None
        assert page.pending_session.eligible_objective_count == 1

        start.click()
        widget = page.adaptive_session_widget

        assert isinstance(widget, AdaptiveReviewSessionWidget)
        current = widget.session.current_question
        card = widget.current_card
        assert current is not None
        assert card is not None
        assert card.choose_option(current.question.item.correct_option_ids[0])
        card.choose_confidence(ConfidenceLevel.HIGH)
        card.check_answer()

        assert widget.session.answered_count == 1
        assert widget.session.correct_count == 1
        saved = store.list_attempts(course_code="DM847", module_id="dm847.m01")
        assert any(attempt.item_id == current.item_id for attempt in saved)
        next_button = widget.findChild(QPushButton, "adaptiveReviewNextButton")
        assert next_button is not None
        assert not next_button.isHidden()

        next_button.click()
        next_question = widget.session.current_question
        assert next_question is not None
        assert next_question.item_id != current.item_id


def test_review_page_disables_session_without_due_objectives(qapp: QApplication) -> None:
    with SQLiteProgressStore(":memory:") as store:
        page = ReviewPage(store, AppLocale.ENGLISH, clock=lambda: _NOW)
        start = page.findChild(QPushButton, "adaptiveReviewStartButton")
        status = page.findChild(QLabel, "adaptiveReviewLauncherStatus")

        assert start is not None
        assert status is not None
        assert not start.isEnabled()
        assert status.text() == "No objectives are currently due for review."


def test_review_page_keeps_unmapped_due_objectives_in_the_module_queue(
    qapp: QApplication,
) -> None:
    with SQLiteProgressStore(":memory:") as store:
        store.record_and_update(
            _due_attempt(
                "dm857-seed",
                course_code="DM857",
                module_id="dm857.m07",
                objective_id="m07.o1",
            )
        )
        page = ReviewPage(store, AppLocale.ENGLISH, clock=lambda: _NOW)
        start = page.findChild(QPushButton, "adaptiveReviewStartButton")
        unavailable = page.findChild(QLabel, "adaptiveReviewUnavailable")

        assert start is not None
        assert unavailable is not None
        assert not start.isEnabled()
        assert page.due_count == 1
        assert page.pending_session is not None
        assert page.pending_session.unsupported_keys == (("DM857", "dm857.m07", "m07.o1"),)
        assert "module queue" in unavailable.text()
