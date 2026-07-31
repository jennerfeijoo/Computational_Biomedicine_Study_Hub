from __future__ import annotations

import random
from datetime import UTC, datetime, timedelta

import pytest

from computational_biomedicine_study_hub.content.models import AssessmentItem
from computational_biomedicine_study_hub.i18n import AppLocale
from computational_biomedicine_study_hub.learning.activity_types import ActivityType
from computational_biomedicine_study_hub.learning.adaptive_review import (
    AdaptiveReviewSession,
    ReviewQuestionCandidate,
    authored_review_candidates,
)
from computational_biomedicine_study_hub.learning.progress import MasteryState, ReviewItem

_NOW = datetime(2026, 7, 31, 8, 0, tzinfo=UTC)


def _review_item(objective_id: str, *, mastery: float, lapses: int = 0) -> ReviewItem:
    return ReviewItem(
        course_code="TEST",
        module_id="test.m01",
        state=MasteryState(
            objective_id=objective_id,
            mastery_score=mastery,
            attempts=2,
            consecutive_correct=0,
            lapse_count=lapses,
            last_attempt_at=_NOW - timedelta(days=3),
            next_review_at=_NOW - timedelta(days=1),
        ),
    )


def _candidate(objective_id: str, item_number: int) -> ReviewQuestionCandidate:
    item = AssessmentItem(
        item_id=f"test.m01.bank.{objective_id}.{item_number}",
        activity_type=ActivityType.MULTIPLE_CHOICE,
        prompt=f"Question {objective_id}-{item_number}",
        options=("Correct", "Incorrect"),
        correct_answers=("Correct",),
        explanation="Authored explanation.",
        option_ids=("correct", "incorrect"),
        correct_option_ids=("correct",),
    )
    return ReviewQuestionCandidate(
        course_code="TEST",
        module_id="test.m01",
        objective_ids=(objective_id,),
        item=item,
    )


def test_session_prioritizes_weakness_then_interleaves_objectives() -> None:
    weak = _review_item("o1", mastery=0.2, lapses=2)
    stronger = _review_item("o2", mastery=0.65)
    catalog = {
        weak.key: (_candidate("o1", 1), _candidate("o1", 2)),
        stronger.key: (_candidate("o2", 1), _candidate("o2", 2)),
    }
    session = AdaptiveReviewSession(
        (weak, stronger),
        locale=AppLocale.ENGLISH,
        target_questions=3,
        rng=random.Random(7),
        candidate_catalog=catalog,
    )

    first = session.current_question
    assert first is not None
    assert first.primary_key == weak.key

    session.record_result(first.item_id, False)
    second = session.current_question
    assert second is not None
    assert second.primary_key == stronger.key
    assert second.item_id != first.item_id

    session.record_result(second.item_id, True)
    third = session.current_question
    assert third is not None
    assert third.primary_key == weak.key
    assert third.item_id not in {first.item_id, second.item_id}

    session.record_result(third.item_id, True)

    assert session.is_complete
    assert session.summary.answered == 3
    assert session.summary.correct == 2
    assert session.summary.reviewed_objectives == (weak.key, stronger.key)
    assert not session.summary.exhausted


def test_session_reports_unsupported_due_objectives_without_inference() -> None:
    due = _review_item("o1", mastery=0.3)
    session = AdaptiveReviewSession(
        (due,),
        locale=AppLocale.ENGLISH,
        candidate_catalog={},
    )

    assert not session.can_start
    assert session.eligible_objective_count == 0
    assert session.unsupported_keys == (due.key,)
    assert session.summary.answered == 0


def test_session_stops_when_unique_authored_questions_are_exhausted() -> None:
    due = _review_item("o1", mastery=0.3)
    candidate = _candidate("o1", 1)
    session = AdaptiveReviewSession(
        (due,),
        locale=AppLocale.ENGLISH,
        target_questions=3,
        candidate_catalog={due.key: (candidate,)},
    )
    current = session.current_question
    assert current is not None

    session.record_result(current.item_id, True)

    assert session.is_complete
    assert session.summary.answered == 1
    assert session.summary.exhausted


def test_session_rejects_results_for_a_different_item() -> None:
    due = _review_item("o1", mastery=0.3)
    session = AdaptiveReviewSession(
        (due,),
        locale=AppLocale.ENGLISH,
        candidate_catalog={due.key: (_candidate("o1", 1),)},
    )

    with pytest.raises(ValueError, match="current authored item"):
        session.record_result("another-item", True)


def test_authored_catalog_exposes_only_explicitly_linked_bank_items() -> None:
    catalog = authored_review_candidates(AppLocale.ENGLISH)
    key = ("DM847", "dm847.m01", "m01.o1")

    assert key in catalog
    assert catalog[key]
    assert all(candidate.item_id.startswith("dm847.m01.bank.") for candidate in catalog[key])
    assert all("m01.o1" in candidate.objective_ids for candidate in catalog[key])
    assert ("DM857", "dm857.m07", "m07.o1") not in catalog
