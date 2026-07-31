"""Adaptive, objective-scoped review sessions built from authored question banks."""

from __future__ import annotations

import random
from dataclasses import dataclass
from functools import lru_cache

from ..content.dm847 import LOCALIZED_BUNDLES as DM847_LOCALIZED_BUNDLES
from ..content.dm857 import LOCALIZED_BUNDLES as DM857_LOCALIZED_BUNDLES
from ..content.models import AssessmentItem
from ..i18n.locales import AppLocale
from .objective_assessment import ObjectiveSessionQuestion
from .progress import ReviewItem

ReviewObjectiveKey = tuple[str, str, str]


@dataclass(frozen=True, slots=True)
class ReviewQuestionCandidate:
    """One authored bank item explicitly linked to a learning objective."""

    course_code: str
    module_id: str
    objective_ids: tuple[str, ...]
    item: AssessmentItem

    def __post_init__(self) -> None:
        if not self.course_code.strip() or not self.module_id.strip():
            raise ValueError("Review candidates require course and module identifiers.")
        if not self.objective_ids:
            raise ValueError("Review candidates require explicit objective links.")
        if len(self.objective_ids) != len(set(self.objective_ids)):
            raise ValueError("Review candidates cannot contain duplicate objective links.")

    @property
    def item_id(self) -> str:
        return self.item.item_id


@dataclass(frozen=True, slots=True)
class AdaptiveReviewQuestion:
    """One session question selected for a primary due objective."""

    primary_key: ReviewObjectiveKey
    candidate: ReviewQuestionCandidate
    question: ObjectiveSessionQuestion

    @property
    def item_id(self) -> str:
        return self.candidate.item_id

    @property
    def course_code(self) -> str:
        return self.candidate.course_code

    @property
    def module_id(self) -> str:
        return self.candidate.module_id

    @property
    def objective_ids(self) -> tuple[str, ...]:
        return self.candidate.objective_ids


@dataclass(frozen=True, slots=True)
class AdaptiveReviewSummary:
    """Immutable result summary for one completed or exhausted session."""

    answered: int
    correct: int
    target: int
    reviewed_objectives: tuple[ReviewObjectiveKey, ...]
    exhausted: bool

    @property
    def accuracy(self) -> float:
        return self.correct / self.answered if self.answered else 0.0


@lru_cache(maxsize=len(AppLocale))
def authored_review_candidates(
    locale: AppLocale,
) -> dict[ReviewObjectiveKey, tuple[ReviewQuestionCandidate, ...]]:
    """Index authored objective-bank items by explicit objective identity."""

    indexed: dict[ReviewObjectiveKey, list[ReviewQuestionCandidate]] = {}
    for localized_bundle in (*DM847_LOCALIZED_BUNDLES, *DM857_LOCALIZED_BUNDLES):
        bundle = localized_bundle.materialize(locale)
        links = bundle.objective_links
        if links is None:
            continue
        for item in bundle.objective_question_bank:
            objective_ids = links.objectives_for(item.item_id)
            if not objective_ids:
                continue
            candidate = ReviewQuestionCandidate(
                course_code=bundle.module.course_code,
                module_id=bundle.module.module_id,
                objective_ids=objective_ids,
                item=item,
            )
            for objective_id in objective_ids:
                key = (bundle.module.course_code, bundle.module.module_id, objective_id)
                indexed.setdefault(key, []).append(candidate)

    return {key: tuple(candidates) for key, candidates in indexed.items()}


class AdaptiveReviewSession:
    """Select the next authored question from weakness, outcomes and spacing constraints."""

    def __init__(
        self,
        due_items: tuple[ReviewItem, ...],
        *,
        locale: AppLocale,
        target_questions: int = 6,
        rng: random.Random | None = None,
        candidate_catalog: dict[ReviewObjectiveKey, tuple[ReviewQuestionCandidate, ...]]
        | None = None,
    ) -> None:
        if target_questions < 1:
            raise ValueError("Adaptive review sessions require at least one target question.")
        keys = tuple(item.key for item in due_items)
        if len(keys) != len(set(keys)):
            raise ValueError("Adaptive review sessions cannot contain duplicate due objectives.")

        self._due_items = due_items
        self._target_questions = target_questions
        self._rng = rng or random.Random()
        self._catalog = (
            candidate_catalog
            if candidate_catalog is not None
            else authored_review_candidates(locale)
        )
        self._eligible_items = tuple(item for item in due_items if self._catalog.get(item.key))
        self._unsupported_keys = tuple(
            item.key for item in due_items if not self._catalog.get(item.key)
        )
        self._asked_item_ids: set[str] = set()
        self._results: list[tuple[AdaptiveReviewQuestion, bool]] = []
        self._objective_correct: dict[ReviewObjectiveKey, int] = {}
        self._objective_incorrect: dict[ReviewObjectiveKey, int] = {}
        self._current: AdaptiveReviewQuestion | None = self._select_next()
        self._exhausted = self._current is None and bool(self._eligible_items)

    @property
    def target_questions(self) -> int:
        return self._target_questions

    @property
    def eligible_objective_count(self) -> int:
        return len(self._eligible_items)

    @property
    def unsupported_keys(self) -> tuple[ReviewObjectiveKey, ...]:
        return self._unsupported_keys

    @property
    def current_question(self) -> AdaptiveReviewQuestion | None:
        return self._current

    @property
    def answered_count(self) -> int:
        return len(self._results)

    @property
    def correct_count(self) -> int:
        return sum(is_correct for _, is_correct in self._results)

    @property
    def is_complete(self) -> bool:
        return self._current is None

    @property
    def can_start(self) -> bool:
        return self._current is not None

    @property
    def summary(self) -> AdaptiveReviewSummary:
        reviewed: list[ReviewObjectiveKey] = []
        for question, _ in self._results:
            if question.primary_key not in reviewed:
                reviewed.append(question.primary_key)
        return AdaptiveReviewSummary(
            answered=self.answered_count,
            correct=self.correct_count,
            target=self._target_questions,
            reviewed_objectives=tuple(reviewed),
            exhausted=self._exhausted,
        )

    def record_result(self, item_id: str, is_correct: bool) -> None:
        """Advance after accepting the deterministic result for the current question."""

        current = self._current
        if current is None:
            raise RuntimeError("The adaptive review session is already complete.")
        if item_id != current.item_id:
            raise ValueError("Review results must match the current authored item.")

        self._results.append((current, is_correct))
        counter = self._objective_correct if is_correct else self._objective_incorrect
        counter[current.primary_key] = counter.get(current.primary_key, 0) + 1
        self._asked_item_ids.add(item_id)

        if self.answered_count >= self._target_questions:
            self._current = None
            return

        self._current = self._select_next()
        if self._current is None:
            self._exhausted = True

    def _select_next(self) -> AdaptiveReviewQuestion | None:
        available = tuple(
            item
            for item in self._eligible_items
            if any(
                candidate.item_id not in self._asked_item_ids
                for candidate in self._catalog[item.key]
            )
        )
        if not available:
            return None

        previous_key = self._results[-1][0].primary_key if self._results else None
        alternatives = tuple(item for item in available if item.key != previous_key)
        selectable = alternatives or available
        selected_item = max(
            selectable,
            key=lambda item: (
                self._priority_score(item),
                -self._due_items.index(item),
            ),
        )
        candidates = [
            candidate
            for candidate in self._catalog[selected_item.key]
            if candidate.item_id not in self._asked_item_ids
        ]
        candidate = self._rng.choice(candidates)
        options = list(candidate.item.option_objects)
        self._rng.shuffle(options)
        return AdaptiveReviewQuestion(
            primary_key=selected_item.key,
            candidate=candidate,
            question=ObjectiveSessionQuestion(
                item=candidate.item,
                display_options=tuple(options),
            ),
        )

    def _priority_score(self, item: ReviewItem) -> float:
        key = item.key
        state = item.state
        weakness = (1.0 - state.mastery_score) * 4.0
        lapses = min(state.lapse_count, 5) * 0.25
        incorrect_bonus = self._objective_incorrect.get(key, 0) * 1.5
        correct_penalty = self._objective_correct.get(key, 0) * 0.65
        return weakness + lapses + incorrect_bonus - correct_penalty


__all__ = [
    "AdaptiveReviewQuestion",
    "AdaptiveReviewSession",
    "AdaptiveReviewSummary",
    "ReviewObjectiveKey",
    "ReviewQuestionCandidate",
    "authored_review_candidates",
]
