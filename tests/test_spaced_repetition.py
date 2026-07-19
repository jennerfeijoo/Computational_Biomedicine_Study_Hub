from dataclasses import replace
from datetime import UTC, datetime, timedelta

from computational_biomedicine_study_hub.learning.progress import (
    LearningItemKind,
    MasteryState,
    ReviewSchedule,
)
from computational_biomedicine_study_hub.learning.spaced_repetition import (
    ReviewRating,
    reschedule,
)

NOW = datetime(2026, 7, 19, 12, 0, tzinfo=UTC)


def _new_schedule() -> ReviewSchedule:
    return ReviewSchedule(
        course_code="DM857",
        module_id="dm857.m01",
        item_id="m01.p01",
        item_kind=LearningItemKind.PRACTICE,
        mastery_state=MasteryState.NEW,
        repetitions=0,
        interval_days=0,
        easiness=2.5,
        due_at=NOW,
    )


def test_good_reviews_follow_first_and_second_sm2_intervals() -> None:
    first = reschedule(_new_schedule(), ReviewRating.GOOD, reviewed_at=NOW)
    second = reschedule(first, ReviewRating.GOOD, reviewed_at=first.due_at)

    assert first.repetitions == 1
    assert first.interval_days == 1
    assert first.due_at == NOW + timedelta(days=1)
    assert second.repetitions == 2
    assert second.interval_days == 6
    assert second.mastery_state is MasteryState.REVIEWING


def test_again_resets_repetitions_and_reduces_easiness() -> None:
    established = replace(
        _new_schedule(),
        repetitions=4,
        interval_days=20,
        easiness=2.7,
        mastery_state=MasteryState.REVIEWING,
    )

    result = reschedule(established, ReviewRating.AGAIN, reviewed_at=NOW)

    assert result.repetitions == 0
    assert result.interval_days == 1
    assert result.easiness == 2.5
    assert result.mastery_state is MasteryState.LEARNING


def test_easiness_is_clamped_and_algorithm_is_deterministic() -> None:
    hard = replace(_new_schedule(), easiness=1.3, interval_days=1)
    easy = replace(_new_schedule(), easiness=3.0, interval_days=10, repetitions=3)

    hard_result = reschedule(hard, ReviewRating.HARD, reviewed_at=NOW)
    easy_result = reschedule(easy, ReviewRating.EASY, reviewed_at=NOW)

    assert hard_result.easiness == 1.3
    assert easy_result.easiness == 3.0
    assert easy_result.interval_days == 39
    assert reschedule(easy, ReviewRating.EASY, reviewed_at=NOW) == easy_result
