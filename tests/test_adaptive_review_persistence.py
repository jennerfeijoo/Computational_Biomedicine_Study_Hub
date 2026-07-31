from __future__ import annotations

import random
from datetime import UTC, datetime, timedelta
from pathlib import Path

import pytest
from PySide6.QtWidgets import QApplication, QPushButton

from computational_biomedicine_study_hub.content.models import AssessmentItem
from computational_biomedicine_study_hub.i18n import AppLocale
from computational_biomedicine_study_hub.learning.activity_types import ActivityType
from computational_biomedicine_study_hub.learning.adaptive_review import (
    AdaptiveReviewSession,
    AdaptiveReviewSnapshotError,
    ReviewQuestionCandidate,
)
from computational_biomedicine_study_hub.learning.progress import (
    AttemptRecord,
    ConfidenceLevel,
    MasteryState,
    ReviewItem,
)
from computational_biomedicine_study_hub.storage import (
    AdaptiveReviewSessionStore,
    SQLiteProgressStore,
)
from computational_biomedicine_study_hub.ui.pages.resumable_review_page import (
    ResumableReviewPage,
)

_NOW = datetime(2026, 7, 31, 10, 0, tzinfo=UTC)


def _review_item(objective_id: str, *, mastery: float = 0.25) -> ReviewItem:
    return ReviewItem(
        course_code="TEST",
        module_id="test.m01",
        state=MasteryState(
            objective_id=objective_id,
            mastery_score=mastery,
            attempts=2,
            consecutive_correct=0,
            lapse_count=1,
            last_attempt_at=_NOW - timedelta(days=3),
            next_review_at=_NOW - timedelta(days=1),
        ),
    )


def _candidate(objective_id: str, number: int) -> ReviewQuestionCandidate:
    item = AssessmentItem(
        item_id=f"test.m01.bank.{objective_id}.{number}",
        activity_type=ActivityType.MULTIPLE_CHOICE,
        prompt=f"Question {number}",
        options=("A", "B", "C"),
        correct_answers=("A",),
        explanation="Authored explanation.",
        option_ids=("a", "b", "c"),
        correct_option_ids=("a",),
    )
    return ReviewQuestionCandidate(
        course_code="TEST",
        module_id="test.m01",
        objective_ids=(objective_id,),
        item=item,
    )


def _due_attempt() -> AttemptRecord:
    return AttemptRecord(
        attempt_id="resume-seed",
        course_code="DM857",
        module_id="dm857.m07",
        objective_id="m07.o6",
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


def test_snapshot_round_trip_restores_results_and_question_order() -> None:
    due = _review_item("o1")
    catalog = {due.key: (_candidate("o1", 1), _candidate("o1", 2))}
    session = AdaptiveReviewSession(
        (due,),
        locale=AppLocale.ENGLISH,
        target_questions=2,
        rng=random.Random(8),
        candidate_catalog=catalog,
    )
    first = session.current_question
    assert first is not None
    session.record_result(first.item_id, False)
    second = session.current_question
    assert second is not None
    option_order = tuple(option.option_id for option in second.question.display_options)

    snapshot = session.to_snapshot(updated_at=_NOW)
    parsed = type(snapshot).from_json(snapshot.to_json())
    restored = AdaptiveReviewSession.from_snapshot(
        parsed,
        locale=AppLocale.DANISH_DENMARK,
        candidate_catalog=catalog,
    )

    assert restored.session_id == session.session_id
    assert restored.answered_count == 1
    assert restored.correct_count == 0
    assert restored.current_question is not None
    assert restored.current_question.item_id == second.item_id
    assert tuple(
        option.option_id for option in restored.current_question.question.display_options
    ) == option_order


def test_restore_rejects_changed_academic_contract() -> None:
    due = _review_item("o1")
    original = {due.key: (_candidate("o1", 1),)}
    session = AdaptiveReviewSession(
        (due,),
        locale=AppLocale.ENGLISH,
        candidate_catalog=original,
    )
    snapshot = session.to_snapshot(updated_at=_NOW)
    changed = {due.key: (_candidate("o1", 2),)}

    with pytest.raises(AdaptiveReviewSnapshotError, match="catalog changed"):
        AdaptiveReviewSession.from_snapshot(
            snapshot,
            locale=AppLocale.ENGLISH,
            candidate_catalog=changed,
        )


def test_sidecar_store_round_trips_and_discards_malformed_documents(tmp_path: Path) -> None:
    progress_path = tmp_path / "progress.sqlite3"
    due = _review_item("o1")
    catalog = {due.key: (_candidate("o1", 1),)}
    session = AdaptiveReviewSession(
        (due,),
        locale=AppLocale.ENGLISH,
        candidate_catalog=catalog,
    )
    snapshot = session.to_snapshot(updated_at=_NOW)
    store = AdaptiveReviewSessionStore(progress_path)

    store.save(snapshot)

    assert store.load() == snapshot
    assert store.path is not None
    store.path.write_text("{not-json", encoding="utf-8")
    assert store.load() is None
    assert not store.path.exists()


def test_resumable_page_restores_code_draft_and_pending_result(
    qapp: QApplication,
) -> None:
    with SQLiteProgressStore(":memory:") as progress:
        progress.record_and_update(_due_attempt())
        first_page = ResumableReviewPage(
            progress,
            AppLocale.ENGLISH,
            clock=lambda: _NOW,
        )
        start = first_page.findChild(QPushButton, "adaptiveReviewStartButton")
        assert start is not None
        start.click()
        first_widget = first_page.adaptive_session_widget
        assert first_widget is not None
        challenge = first_widget.current_challenge_widget
        assert challenge is not None

        draft = "def unique_count(values):\n    return len(set(values))"
        challenge.set_source(draft)
        challenge.choose_confidence(ConfidenceLevel.MEDIUM)
        challenge.run_tests()
        first_page.persist_active_session()

        second_page = ResumableReviewPage(
            progress,
            AppLocale.ENGLISH,
            clock=lambda: _NOW,
        )
        assert second_page.resumable_snapshot is not None
        resume = second_page.findChild(QPushButton, "adaptiveReviewStartButton")
        assert resume is not None
        assert resume.text() == "Resume session"
        resume.click()

        restored_widget = second_page.adaptive_session_widget
        assert restored_widget is not None
        restored_challenge = restored_widget.current_challenge_widget
        assert restored_challenge is not None
        assert restored_challenge.source == draft
        next_button = restored_widget.findChild(QPushButton, "adaptiveReviewNextButton")
        assert next_button is not None
        assert not next_button.isHidden()


def test_discard_saved_session_keeps_learning_evidence(qapp: QApplication) -> None:
    with SQLiteProgressStore(":memory:") as progress:
        progress.record_and_update(_due_attempt())
        page = ResumableReviewPage(progress, AppLocale.ENGLISH, clock=lambda: _NOW)
        start = page.findChild(QPushButton, "adaptiveReviewStartButton")
        assert start is not None
        start.click()
        page.persist_active_session()

        resumed = ResumableReviewPage(progress, AppLocale.ENGLISH, clock=lambda: _NOW)
        discard = resumed.discard_session_button
        assert discard is not None
        discard.click()

        assert resumed.resumable_snapshot is None
        assert progress.list_attempts(course_code="DM857")
