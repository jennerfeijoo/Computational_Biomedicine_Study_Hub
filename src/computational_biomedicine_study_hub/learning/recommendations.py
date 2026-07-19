"""Auditable review recommendations derived only from local progress evidence."""

from __future__ import annotations

from collections import Counter
from dataclasses import dataclass
from datetime import datetime
from enum import StrEnum

from .academic_catalog import AcademicCatalog
from .progress_repository import ProgressRepository


class RecommendationCategory(StrEnum):
    TODAY = "today"
    REINFORCE = "reinforce"
    FAILED_QUESTIONS = "failed_questions"
    PENDING_CARDS = "pending_cards"
    CONTINUE = "continue"
    COURSE_PROGRESS = "course_progress"


class RecommendationReason(StrEnum):
    DUE_ITEM = "due_item"
    REPEATED_FAILURE = "repeated_failure"
    FAILED_QUESTION = "failed_question"
    DUE_CARDS = "due_cards"
    LAST_ACTIVITY = "last_activity"
    COURSE_MASTERY = "course_mastery"
    UNSTUDIED_MODULE = "unstudied_module"


@dataclass(frozen=True, slots=True)
class ReviewRecommendation:
    category: RecommendationCategory
    reason: RecommendationReason
    course_code: str
    module_id: str = ""
    item_id: str = ""
    count: int = 0
    percent: int = 0


def build_review_recommendations(
    catalog: AcademicCatalog,
    repository: ProgressRepository,
    *,
    now: datetime,
) -> tuple[ReviewRecommendation, ...]:
    """Build a small, deterministic recommendation set with traceable reasons."""
    recommendations: list[ReviewRecommendation] = []
    due = repository.list_due_reviews(due_at=now, limit=100)
    for due_item in due[:3]:
        recommendations.append(
            ReviewRecommendation(
                RecommendationCategory.TODAY,
                RecommendationReason.DUE_ITEM,
                due_item.course_code,
                due_item.module_id,
                due_item.item_id,
            )
        )

    attempts = repository.list_attempts(limit=500)
    failures = tuple(item for item in attempts if item.is_correct is False)
    failure_by_module = Counter((item.course_code, item.module_id) for item in failures)
    for (course_code, module_id), count in failure_by_module.most_common(3):
        recommendations.append(
            ReviewRecommendation(
                RecommendationCategory.REINFORCE,
                RecommendationReason.REPEATED_FAILURE,
                course_code,
                module_id,
                count=count,
            )
        )
    for failed_attempt in failures[:3]:
        recommendations.append(
            ReviewRecommendation(
                RecommendationCategory.FAILED_QUESTIONS,
                RecommendationReason.FAILED_QUESTION,
                failed_attempt.course_code,
                failed_attempt.module_id,
                failed_attempt.item_id,
            )
        )

    due_cards = tuple(item for item in repository.list_flashcard_progress() if item.due_at <= now)
    cards_by_module = Counter((item.course_code, item.module_id) for item in due_cards)
    for (course_code, module_id), count in cards_by_module.most_common(3):
        recommendations.append(
            ReviewRecommendation(
                RecommendationCategory.PENDING_CARDS,
                RecommendationReason.DUE_CARDS,
                course_code,
                module_id,
                count=count,
            )
        )

    if attempts:
        latest = attempts[0]
        recommendations.append(
            ReviewRecommendation(
                RecommendationCategory.CONTINUE,
                RecommendationReason.LAST_ACTIVITY,
                latest.course_code,
                latest.module_id,
                latest.item_id,
            )
        )
    else:
        first_module = next(iter(catalog.modules()), None)
        if first_module is not None:
            recommendations.append(
                ReviewRecommendation(
                    RecommendationCategory.CONTINUE,
                    RecommendationReason.UNSTUDIED_MODULE,
                    first_module.course_code,
                    first_module.module_id,
                )
            )

    for course_code in catalog.course_codes:
        summaries = tuple(
            repository.module_progress(record.course_code, record.module_id)
            for record in catalog.modules(course_code)
        )
        attempt_count = sum(item.attempt_count for item in summaries)
        correct_count = sum(item.correct_count for item in summaries)
        percent = round(100 * correct_count / attempt_count) if attempt_count else 0
        recommendations.append(
            ReviewRecommendation(
                RecommendationCategory.COURSE_PROGRESS,
                RecommendationReason.COURSE_MASTERY,
                course_code,
                count=attempt_count,
                percent=percent,
            )
        )
    return tuple(recommendations)


__all__ = [
    "RecommendationCategory",
    "RecommendationReason",
    "ReviewRecommendation",
    "build_review_recommendations",
]
