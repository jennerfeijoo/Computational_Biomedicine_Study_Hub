"""Learner-facing, localized presentation of persisted review identities."""

from __future__ import annotations

import logging
from dataclasses import dataclass
from datetime import datetime

from ..content.models import AssessmentItem
from ..courses import COURSES
from ..i18n import AppLocale
from ..learning.academic_catalog import AcademicCatalog
from ..learning.activity_types import ActivityType
from ..learning.progress import (
    AttemptOutcome,
    AttemptRecord,
    LearningItemKind,
    MasteryState,
    ReviewSchedule,
)
from ..learning.progress_repository import ProgressRepository

logger = logging.getLogger(__name__)


_ITEM_LABELS = {
    AppLocale.SPANISH_SPAIN: {
        LearningItemKind.FLASHCARD: "Tarjeta de memoria",
        LearningItemKind.CONCEPT: "Concepto",
        LearningItemKind.ASSESSMENT: "Pregunta de evaluación",
        LearningItemKind.PRACTICE: "Ejercicio práctico",
    },
    AppLocale.ENGLISH: {
        LearningItemKind.FLASHCARD: "Flashcard",
        LearningItemKind.CONCEPT: "Concept",
        LearningItemKind.ASSESSMENT: "Assessment question",
        LearningItemKind.PRACTICE: "Practice exercise",
    },
    AppLocale.DANISH_DENMARK: {
        LearningItemKind.FLASHCARD: "Huskekort",
        LearningItemKind.CONCEPT: "Begreb",
        LearningItemKind.ASSESSMENT: "Evalueringsspørgsmål",
        LearningItemKind.PRACTICE: "Praktisk øvelse",
    },
}

_RESULT_LABELS = {
    AppLocale.SPANISH_SPAIN: {
        "review": "Necesita repaso",
        "partial": "Parcial",
        "solved": "Resuelto",
        "correct": "Correcto",
        "incorrect": "Incorrecto",
        "again": "Otra vez",
        "hard": "Difícil",
        "good": "Bien",
        "easy": "Fácil",
    },
    AppLocale.ENGLISH: {
        "review": "Needs review",
        "partial": "Partial",
        "solved": "Solved",
        "correct": "Correct",
        "incorrect": "Incorrect",
        "again": "Again",
        "hard": "Hard",
        "good": "Good",
        "easy": "Easy",
    },
    AppLocale.DANISH_DENMARK: {
        "review": "Kræver repetition",
        "partial": "Delvist",
        "solved": "Løst",
        "correct": "Korrekt",
        "incorrect": "Forkert",
        "again": "Igen",
        "hard": "Svært",
        "good": "Godt",
        "easy": "Let",
    },
}

_PRESENTATION_COPY = {
    AppLocale.SPANISH_SPAIN: {
        "unavailable": "Contenido no disponible",
        "course_unavailable": "Asignatura no disponible",
        "module_unavailable": "Módulo no disponible",
        "new": "Nuevo",
        "failed": "Fallado",
        "overdue": "Vencido",
        "due": "Vencido desde {date}",
    },
    AppLocale.ENGLISH: {
        "unavailable": "Content unavailable",
        "course_unavailable": "Course unavailable",
        "module_unavailable": "Module unavailable",
        "new": "New",
        "failed": "Failed",
        "overdue": "Due",
        "due": "Due since {date}",
    },
    AppLocale.DANISH_DENMARK: {
        "unavailable": "Indhold ikke tilgængeligt",
        "course_unavailable": "Kursus ikke tilgængeligt",
        "module_unavailable": "Modul ikke tilgængeligt",
        "new": "Nyt",
        "failed": "Fejlet",
        "overdue": "Forfalden",
        "due": "Forfalden siden {date}",
    },
}

_OPEN_PRACTICE_TYPES = {
    ActivityType.WORKED_EXAMPLE,
    ActivityType.FLASHCARD,
    ActivityType.CODE_COMPLETION,
    ActivityType.CODE_TRACING,
    ActivityType.DEBUGGING,
    ActivityType.SHORT_ANSWER,
    ActivityType.ORAL_EXPLANATION,
    ActivityType.DATA_INTERPRETATION,
    ActivityType.PIPELINE_DESIGN,
}


@dataclass(frozen=True, slots=True)
class ReviewItemPresentation:
    """Localized view of one stable persisted review schedule."""

    item_id: str
    course_code: str
    course_title: str
    module_id: str
    module_title: str
    item_type: LearningItemKind
    localized_type_label: str
    display_title: str
    display_prompt: str
    review_reason: str
    due_text: str
    last_result: str
    last_attempt_at: datetime | None
    source_route: str
    resolved: bool
    explanation: str = ""
    activity_item: AssessmentItem | None = None
    content_version: str = ""

    @property
    def technical_identity(self) -> str:
        """Return diagnostic identity for tooltips, never primary copy."""
        return f"{self.course_code} · {self.module_id} · {self.item_type.value} · {self.item_id}"


def localized_item_type(locale: AppLocale, kind: LearningItemKind) -> str:
    """Return a complete learner-facing label for every review kind."""
    return _ITEM_LABELS[locale][kind]


def localized_result(locale: AppLocale, value: str) -> str:
    """Translate persisted result/rating values without exposing raw tokens."""
    normalized = value.casefold()
    return _RESULT_LABELS[locale].get(normalized, value)


def localized_datetime(locale: AppLocale, value: datetime) -> str:
    """Format an aware timestamp in local time using locale-appropriate order."""
    local_value = value.astimezone()
    if locale is AppLocale.ENGLISH:
        return local_value.strftime("%Y-%m-%d %H:%M")
    return local_value.strftime("%d/%m/%Y %H:%M")


def course_title(locale: AppLocale, course_code: str) -> str:
    """Resolve a stable course code to its complete localized title."""
    course = next((item for item in COURSES if item.code == course_code.upper()), None)
    if course is None:
        return _PRESENTATION_COPY[locale]["course_unavailable"]
    return course.title_for(locale)


def shortened(text: str, limit: int = 96) -> str:
    """Return compact one-line learner copy without damaging short prompts."""
    compact = " ".join(text.split())
    if len(compact) <= limit:
        return compact
    return f"{compact[: limit - 1].rstrip()}…"


class ReviewPresentationResolver:
    """Resolve stable review identities against one localized academic catalog."""

    def __init__(
        self,
        catalog: AcademicCatalog,
        repository: ProgressRepository,
        locale: AppLocale,
    ) -> None:
        self._catalog = catalog
        self._repository = repository
        self._locale = locale

    def resolve(self, schedule: ReviewSchedule) -> ReviewItemPresentation:
        """Build localized content without persisting any visible text."""
        attempts = self._repository.list_attempts(
            course_code=schedule.course_code,
            module_id=schedule.module_id,
            item_id=schedule.item_id,
            limit=1,
        )
        latest = attempts[0] if attempts else None
        course_name = course_title(self._locale, schedule.course_code)
        type_label = localized_item_type(self._locale, schedule.item_kind)
        reason = self._review_reason(schedule, latest)
        due_text = _PRESENTATION_COPY[self._locale]["due"].format(
            date=localized_datetime(self._locale, schedule.due_at)
        )
        last_result = self._attempt_result(latest)

        try:
            record = self._catalog.module(schedule.course_code, schedule.module_id)
        except KeyError:
            return self._orphan(
                schedule,
                course_name=course_name,
                module_name=_PRESENTATION_COPY[self._locale]["module_unavailable"],
                type_label=type_label,
                reason=reason,
                due_text=due_text,
                latest=latest,
                last_result=last_result,
            )

        title = ""
        prompt = ""
        explanation = ""
        activity_item: AssessmentItem | None = None

        if schedule.item_kind is LearningItemKind.FLASHCARD:
            card = next(
                (
                    item
                    for item in self._catalog.flashcards(
                        course_code=schedule.course_code,
                        module_id=schedule.module_id,
                    )
                    if item.card_id == schedule.item_id
                ),
                None,
            )
            if card is not None:
                title = shortened(card.front)
                prompt = card.front
                explanation = card.back
        elif schedule.item_kind is LearningItemKind.CONCEPT:
            concept = next(
                (
                    item
                    for item in self._catalog.glossary(course_code=schedule.course_code)
                    if item.module_id == schedule.module_id and item.term_id == schedule.item_id
                ),
                None,
            )
            if concept is not None:
                title = concept.term
                prompt = concept.term
                explanation = concept.definition
        elif schedule.item_kind is LearningItemKind.ASSESSMENT:
            activity_item = next(
                (
                    item
                    for item in (
                        *record.objective_question_bank,
                        *record.assessment_items,
                    )
                    if item.item_id == schedule.item_id
                ),
                None,
            )
            if activity_item is not None:
                title = shortened(activity_item.prompt)
                prompt = activity_item.prompt
                explanation = activity_item.explanation
        else:
            exercise = next(
                (
                    item
                    for item in record.learning_module.practice_exercises
                    if item.exercise_id == schedule.item_id
                ),
                None,
            )
            if exercise is not None:
                answer = exercise.solution or exercise.explanation
                activity_type = (
                    exercise.activity_type
                    if exercise.activity_type in _OPEN_PRACTICE_TYPES
                    else ActivityType.SHORT_ANSWER
                )
                activity_item = AssessmentItem(
                    item_id=exercise.exercise_id,
                    activity_type=activity_type,
                    prompt=exercise.prompt,
                    options=(),
                    correct_answers=(answer,),
                    explanation=exercise.explanation or answer,
                )
                title = shortened(exercise.prompt)
                prompt = exercise.prompt
                explanation = answer

        if not title or not prompt:
            return self._orphan(
                schedule,
                course_name=course_name,
                module_name=record.title,
                type_label=type_label,
                reason=reason,
                due_text=due_text,
                latest=latest,
                last_result=last_result,
            )

        return ReviewItemPresentation(
            item_id=schedule.item_id,
            course_code=schedule.course_code,
            course_title=course_name,
            module_id=schedule.module_id,
            module_title=record.title,
            item_type=schedule.item_kind,
            localized_type_label=type_label,
            display_title=title,
            display_prompt=prompt,
            review_reason=reason,
            due_text=due_text,
            last_result=last_result,
            last_attempt_at=None if latest is None else latest.created_at,
            source_route=f"course/{schedule.course_code.casefold()}",
            resolved=True,
            explanation=explanation,
            activity_item=activity_item,
            content_version=record.content_version,
        )

    def resolve_attempt(self, attempt: AttemptRecord) -> ReviewItemPresentation:
        """Resolve a historical attempt through the same identity-only path."""
        schedule = ReviewSchedule(
            course_code=attempt.course_code,
            module_id=attempt.module_id,
            item_id=attempt.item_id,
            item_kind=attempt.item_kind,
            mastery_state=MasteryState.LEARNING,
            repetitions=0,
            interval_days=0,
            easiness=2.5,
            due_at=attempt.created_at,
            last_reviewed_at=None,
        )
        return self.resolve(schedule)

    def _review_reason(
        self,
        schedule: ReviewSchedule,
        latest: AttemptRecord | None,
    ) -> str:
        copy = _PRESENTATION_COPY[self._locale]
        if schedule.mastery_state is MasteryState.NEW and not schedule.repetitions:
            return copy["new"]
        if latest is not None and (
            latest.is_correct is False or latest.outcome is AttemptOutcome.REVIEW
        ):
            return copy["failed"]
        return copy["overdue"]

    def _attempt_result(self, attempt: AttemptRecord | None) -> str:
        if attempt is None:
            return ""
        if attempt.is_correct is True:
            return localized_result(self._locale, "correct")
        if attempt.is_correct is False:
            return localized_result(self._locale, "incorrect")
        return localized_result(self._locale, attempt.outcome.value)

    def _orphan(
        self,
        schedule: ReviewSchedule,
        *,
        course_name: str,
        module_name: str,
        type_label: str,
        reason: str,
        due_text: str,
        latest: AttemptRecord | None,
        last_result: str,
    ) -> ReviewItemPresentation:
        logger.warning(
            "Unresolved review reference: course=%s module=%s kind=%s item=%s",
            schedule.course_code,
            schedule.module_id,
            schedule.item_kind.value,
            schedule.item_id,
        )
        unavailable = _PRESENTATION_COPY[self._locale]["unavailable"]
        return ReviewItemPresentation(
            item_id=schedule.item_id,
            course_code=schedule.course_code,
            course_title=course_name,
            module_id=schedule.module_id,
            module_title=module_name,
            item_type=schedule.item_kind,
            localized_type_label=type_label,
            display_title=unavailable,
            display_prompt=unavailable,
            review_reason=reason,
            due_text=due_text,
            last_result=last_result,
            last_attempt_at=None if latest is None else latest.created_at,
            source_route=f"course/{schedule.course_code.casefold()}",
            resolved=False,
        )


__all__ = [
    "ReviewItemPresentation",
    "ReviewPresentationResolver",
    "course_title",
    "localized_datetime",
    "localized_item_type",
    "localized_result",
    "shortened",
]
