"""Deterministic, UI-independent spaced repetition."""

from __future__ import annotations

from dataclasses import replace
from datetime import datetime, timedelta
from enum import IntEnum

from .progress import MasteryState, ReviewSchedule, require_aware


class ReviewRating(IntEnum):
    """SM-2-compatible response quality exposed by the four review buttons."""

    AGAIN = 0
    HARD = 2
    GOOD = 4
    EASY = 5


def reschedule(
    previous: ReviewSchedule,
    rating: ReviewRating,
    *,
    reviewed_at: datetime,
) -> ReviewSchedule:
    """Return the next schedule using a small, inspectable SM-2 variant."""
    require_aware(reviewed_at, "reviewed_at")

    if rating is ReviewRating.AGAIN:
        repetitions = 0
        interval_days = 1
        easiness = max(1.3, previous.easiness - 0.2)
    elif rating is ReviewRating.HARD:
        repetitions = previous.repetitions + 1
        interval_days = max(1, round(max(1, previous.interval_days) * 1.2))
        easiness = max(1.3, previous.easiness - 0.15)
    elif rating is ReviewRating.GOOD:
        repetitions = previous.repetitions + 1
        if repetitions == 1:
            interval_days = 1
        elif repetitions == 2:
            interval_days = 6
        else:
            interval_days = max(1, round(previous.interval_days * previous.easiness))
        easiness = previous.easiness
    else:
        repetitions = previous.repetitions + 1
        if repetitions == 1:
            interval_days = 4
        elif repetitions == 2:
            interval_days = 10
        else:
            interval_days = max(1, round(previous.interval_days * previous.easiness * 1.3))
        easiness = min(3.0, previous.easiness + 0.15)

    if repetitions >= 5:
        mastery = MasteryState.MASTERED
    elif repetitions >= 2:
        mastery = MasteryState.REVIEWING
    else:
        mastery = MasteryState.LEARNING

    return replace(
        previous,
        mastery_state=mastery,
        repetitions=repetitions,
        interval_days=interval_days,
        easiness=easiness,
        due_at=reviewed_at + timedelta(days=interval_days),
        last_reviewed_at=reviewed_at,
    )


__all__ = ["ReviewRating", "reschedule"]
