"""Deterministic objective-level mastery updates and review scheduling."""

from __future__ import annotations

from datetime import timedelta

from .progress import AttemptRecord, ConfidenceLevel, MasteryState

_INITIAL_MASTERY = 0.35
_UPDATE_RATE = 0.45
_MAX_REVIEW_DAYS = 30


def evidence_score(attempt: AttemptRecord) -> float:
    """Convert one attempt into bounded evidence of independent recall.

    Correctness remains authoritative. Hints, revealed solutions and low confidence
    reduce the strength of a correct response because they indicate weaker retrieval.
    """

    if not attempt.is_correct:
        return 0.0

    score = 1.0
    if attempt.confidence is ConfidenceLevel.LOW:
        score -= 0.10
    elif attempt.confidence is ConfidenceLevel.MEDIUM:
        score -= 0.03

    score -= min(attempt.hints_used, 3) * 0.10
    if attempt.solution_revealed:
        score = min(score, 0.35)
    return max(0.0, min(score, 1.0))


def review_interval(attempt: AttemptRecord, consecutive_correct: int) -> timedelta:
    """Return the next review interval for one graded attempt."""

    if not attempt.is_correct or attempt.solution_revealed:
        return timedelta(days=1)
    if attempt.hints_used:
        return timedelta(days=2)

    base_days = {
        ConfidenceLevel.LOW: 2,
        ConfidenceLevel.MEDIUM: 4,
        ConfidenceLevel.HIGH: 7,
    }[attempt.confidence]
    multiplier = 2 ** min(max(consecutive_correct - 1, 0), 3)
    return timedelta(days=min(base_days * multiplier, _MAX_REVIEW_DAYS))


def update_mastery(
    previous: MasteryState | None,
    attempt: AttemptRecord,
) -> MasteryState:
    """Create the objective state produced by one new attempt."""

    if previous is not None and previous.objective_id != attempt.objective_id:
        raise ValueError("Attempt and mastery state must reference the same objective.")
    if previous is not None and attempt.attempted_at < previous.last_attempt_at:
        raise ValueError("Attempts cannot be applied before the latest stored attempt.")

    prior_score = previous.mastery_score if previous is not None else _INITIAL_MASTERY
    evidence = evidence_score(attempt)
    mastery_score = prior_score + _UPDATE_RATE * (evidence - prior_score)

    attempts = (previous.attempts if previous is not None else 0) + 1
    previous_streak = previous.consecutive_correct if previous is not None else 0
    consecutive_correct = previous_streak + 1 if attempt.is_correct else 0
    previous_lapses = previous.lapse_count if previous is not None else 0
    lapse_count = previous_lapses + (0 if attempt.is_correct else 1)
    interval = review_interval(attempt, consecutive_correct)

    return MasteryState(
        objective_id=attempt.objective_id,
        mastery_score=round(mastery_score, 6),
        attempts=attempts,
        consecutive_correct=consecutive_correct,
        lapse_count=lapse_count,
        last_attempt_at=attempt.attempted_at,
        next_review_at=attempt.attempted_at + interval,
    )


__all__ = ["evidence_score", "review_interval", "update_mastery"]
