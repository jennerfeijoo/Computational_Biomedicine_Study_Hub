"""Adaptive, objective-scoped review sessions built from authored activities."""

from __future__ import annotations

import random
from collections.abc import Mapping
from dataclasses import dataclass
from enum import StrEnum
from functools import lru_cache
from typing import TypeAlias

from ..content.dm847 import LOCALIZED_BUNDLES as DM847_LOCALIZED_BUNDLES
from ..content.dm857 import LOCALIZED_BUNDLES as DM857_LOCALIZED_BUNDLES
from ..content.models import AssessmentItem, LearningModule, PracticeExercise
from ..content.python_challenges import PythonChallenge, python_challenge_for
from ..i18n.locales import AppLocale
from .objective_assessment import ObjectiveSessionQuestion
from .progress import ReviewItem

ReviewObjectiveKey = tuple[str, str, str]


class ReviewActivityKind(StrEnum):
    """Supported deterministic activity families in one review session."""

    QUESTION = "question"
    PROGRAMMING = "programming"


ReviewActivityKey = tuple[ReviewActivityKind, str, str, str]


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
    def kind(self) -> ReviewActivityKind:
        return ReviewActivityKind.QUESTION

    @property
    def item_id(self) -> str:
        return self.item.item_id

    @property
    def activity_key(self) -> ReviewActivityKey:
        return (self.kind, self.course_code, self.module_id, self.item_id)


@dataclass(frozen=True, slots=True)
class ReviewProgrammingCandidate:
    """One executable practice exercise with explicit objective-linked tests."""

    learning_module: LearningModule
    exercise: PracticeExercise
    challenge: PythonChallenge

    def __post_init__(self) -> None:
        if self.challenge.course_code != self.learning_module.course_code:
            raise ValueError("Programming review candidates must match their course.")
        if self.challenge.module_id != self.learning_module.module_id:
            raise ValueError("Programming review candidates must match their module.")
        if self.challenge.exercise_id != self.exercise.exercise_id:
            raise ValueError("Programming review candidates must match their exercise.")
        if self.challenge.starter_code != self.exercise.starter_code:
            raise ValueError("Programming review candidates require identical starter code.")
        authored_objectives = {
            objective.objective_id for objective in self.learning_module.objectives
        }
        if not set(self.challenge.objective_ids).issubset(authored_objectives):
            raise ValueError("Programming review candidates cannot reference unknown objectives.")
        required_context = (
            self.exercise.prompt,
            self.exercise.solution,
            self.exercise.explanation,
        )
        if any(not value.strip() for value in required_context):
            raise ValueError(
                "Programming review candidates require complete authored feedback context."
            )

    @property
    def kind(self) -> ReviewActivityKind:
        return ReviewActivityKind.PROGRAMMING

    @property
    def course_code(self) -> str:
        return self.challenge.course_code

    @property
    def module_id(self) -> str:
        return self.challenge.module_id

    @property
    def objective_ids(self) -> tuple[str, ...]:
        return self.challenge.objective_ids

    @property
    def item_id(self) -> str:
        return self.challenge.exercise_id

    @property
    def activity_key(self) -> ReviewActivityKey:
        return (self.kind, self.course_code, self.module_id, self.item_id)


ReviewActivityCandidate: TypeAlias = ReviewQuestionCandidate | ReviewProgrammingCandidate


@dataclass(frozen=True, slots=True)
class AdaptiveReviewQuestion:
    """One selected objective question with stable randomized display options."""

    primary_key: ReviewObjectiveKey
    candidate: ReviewQuestionCandidate
    question: ObjectiveSessionQuestion

    @property
    def kind(self) -> ReviewActivityKind:
        return ReviewActivityKind.QUESTION

    @property
    def activity_key(self) -> ReviewActivityKey:
        return self.candidate.activity_key

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
class AdaptiveReviewProgramming:
    """One selected executable challenge for an objective-scoped review step."""

    primary_key: ReviewObjectiveKey
    candidate: ReviewProgrammingCandidate

    @property
    def kind(self) -> ReviewActivityKind:
        return ReviewActivityKind.PROGRAMMING

    @property
    def activity_key(self) -> ReviewActivityKey:
        return self.candidate.activity_key

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


AdaptiveReviewActivity: TypeAlias = AdaptiveReviewQuestion | AdaptiveReviewProgramming


@dataclass(frozen=True, slots=True)
class AdaptiveReviewSummary:
    """Immutable result summary for one completed or exhausted session."""

    answered: int
    correct: int
    target: int
    reviewed_objectives: tuple[ReviewObjectiveKey, ...]
    exhausted: bool
    question_activities: int
    programming_activities: int

    @property
    def accuracy(self) -> float:
        return self.correct / self.answered if self.answered else 0.0


@lru_cache(maxsize=len(AppLocale))
def authored_review_candidates(
    locale: AppLocale,
) -> dict[ReviewObjectiveKey, tuple[ReviewQuestionCandidate, ...]]:
    """Index authored objective-bank questions by explicit objective identity."""

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


@lru_cache(maxsize=len(AppLocale))
def authored_review_programming_candidates(
    locale: AppLocale,
) -> dict[ReviewObjectiveKey, tuple[ReviewProgrammingCandidate, ...]]:
    """Index executable DM857 challenges by their explicit objective mappings."""

    indexed: dict[ReviewObjectiveKey, list[ReviewProgrammingCandidate]] = {}
    for localized_bundle in DM857_LOCALIZED_BUNDLES:
        bundle = localized_bundle.materialize(locale)
        module = bundle.module
        for exercise in module.practice_exercises:
            if not exercise.starter_code.strip():
                continue
            challenge = python_challenge_for(
                exercise.exercise_id,
                exercise.starter_code,
                locale,
            )
            if challenge is None:
                continue
            candidate = ReviewProgrammingCandidate(
                learning_module=module,
                exercise=exercise,
                challenge=challenge,
            )
            for objective_id in candidate.objective_ids:
                key = (candidate.course_code, candidate.module_id, objective_id)
                indexed.setdefault(key, []).append(candidate)

    return {key: tuple(candidates) for key, candidates in indexed.items()}


@lru_cache(maxsize=len(AppLocale))
def authored_review_activity_candidates(
    locale: AppLocale,
) -> dict[ReviewObjectiveKey, tuple[ReviewActivityCandidate, ...]]:
    """Merge explicitly linked questions and programming challenges."""

    merged: dict[ReviewObjectiveKey, list[ReviewActivityCandidate]] = {}
    catalogs = (
        authored_review_candidates(locale),
        authored_review_programming_candidates(locale),
    )
    for catalog in catalogs:
        for key, candidates in catalog.items():
            merged.setdefault(key, []).extend(candidates)

    result: dict[ReviewObjectiveKey, tuple[ReviewActivityCandidate, ...]] = {}
    for key, candidates in merged.items():
        activity_keys = tuple(candidate.activity_key for candidate in candidates)
        if len(activity_keys) != len(set(activity_keys)):
            raise ValueError(f"Duplicate adaptive review activities are registered for {key!r}.")
        result[key] = tuple(candidates)
    return result


class AdaptiveReviewSession:
    """Select authored activities from weakness, outcomes and spacing constraints."""

    def __init__(
        self,
        due_items: tuple[ReviewItem, ...],
        *,
        locale: AppLocale,
        target_questions: int = 6,
        rng: random.Random | None = None,
        candidate_catalog: Mapping[
            ReviewObjectiveKey,
            tuple[ReviewActivityCandidate, ...],
        ]
        | None = None,
    ) -> None:
        if target_questions < 1:
            raise ValueError("Adaptive review sessions require at least one target activity.")
        keys = tuple(item.key for item in due_items)
        if len(keys) != len(set(keys)):
            raise ValueError("Adaptive review sessions cannot contain duplicate due objectives.")

        self._due_items = due_items
        self._target_questions = target_questions
        self._rng = rng or random.Random()
        source_catalog = (
            candidate_catalog
            if candidate_catalog is not None
            else authored_review_activity_candidates(locale)
        )
        self._catalog = {key: tuple(candidates) for key, candidates in source_catalog.items()}
        self._validate_catalog()
        self._eligible_items = tuple(item for item in due_items if self._catalog.get(item.key))
        self._unsupported_keys = tuple(
            item.key for item in due_items if not self._catalog.get(item.key)
        )
        self._asked_activity_keys: set[ReviewActivityKey] = set()
        self._results: list[tuple[AdaptiveReviewActivity, bool]] = []
        self._objective_correct: dict[ReviewObjectiveKey, int] = {}
        self._objective_incorrect: dict[ReviewObjectiveKey, int] = {}
        self._current: AdaptiveReviewActivity | None = self._select_next()
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
    def current_activity(self) -> AdaptiveReviewActivity | None:
        return self._current

    @property
    def current_question(self) -> AdaptiveReviewQuestion | None:
        current = self._current
        return current if isinstance(current, AdaptiveReviewQuestion) else None

    @property
    def current_programming_activity(self) -> AdaptiveReviewProgramming | None:
        current = self._current
        return current if isinstance(current, AdaptiveReviewProgramming) else None

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
        for activity, _ in self._results:
            if activity.primary_key not in reviewed:
                reviewed.append(activity.primary_key)
        return AdaptiveReviewSummary(
            answered=self.answered_count,
            correct=self.correct_count,
            target=self._target_questions,
            reviewed_objectives=tuple(reviewed),
            exhausted=self._exhausted,
            question_activities=sum(
                activity.kind is ReviewActivityKind.QUESTION for activity, _ in self._results
            ),
            programming_activities=sum(
                activity.kind is ReviewActivityKind.PROGRAMMING for activity, _ in self._results
            ),
        )

    def record_result(self, item_id: str, is_correct: bool) -> None:
        """Advance after accepting the deterministic result for the current activity."""

        current = self._current
        if current is None:
            raise RuntimeError("The adaptive review session is already complete.")
        if item_id != current.item_id:
            raise ValueError("Review results must match the current authored item.")

        self._results.append((current, is_correct))
        counter = self._objective_correct if is_correct else self._objective_incorrect
        counter[current.primary_key] = counter.get(current.primary_key, 0) + 1
        self._asked_activity_keys.add(current.activity_key)

        if self.answered_count >= self._target_questions:
            self._current = None
            return

        self._current = self._select_next()
        if self._current is None:
            self._exhausted = True

    def _select_next(self) -> AdaptiveReviewActivity | None:
        available = tuple(item for item in self._eligible_items if self._available_candidates(item))
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
        candidates = self._available_candidates(selected_item)
        scores = {
            candidate.activity_key: self._candidate_score(candidate, selected_item)
            for candidate in candidates
        }
        best_score = max(scores.values())
        preferred = [
            candidate for candidate in candidates if scores[candidate.activity_key] == best_score
        ]
        candidate = self._rng.choice(preferred)
        if isinstance(candidate, ReviewProgrammingCandidate):
            return AdaptiveReviewProgramming(
                primary_key=selected_item.key,
                candidate=candidate,
            )

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

    def _available_candidates(
        self,
        item: ReviewItem,
    ) -> tuple[ReviewActivityCandidate, ...]:
        return tuple(
            candidate
            for candidate in self._catalog[item.key]
            if candidate.activity_key not in self._asked_activity_keys
        )

    def _priority_score(self, item: ReviewItem) -> float:
        key = item.key
        state = item.state
        weakness = (1.0 - state.mastery_score) * 4.0
        lapses = min(state.lapse_count, 5) * 0.25
        incorrect_bonus = self._objective_incorrect.get(key, 0) * 1.5
        correct_penalty = self._objective_correct.get(key, 0) * 0.65
        return weakness + lapses + incorrect_bonus - correct_penalty

    def _candidate_score(
        self,
        candidate: ReviewActivityCandidate,
        item: ReviewItem,
    ) -> float:
        key = item.key
        correct = self._objective_correct.get(key, 0)
        incorrect = self._objective_incorrect.get(key, 0)
        previous_kind = self._results[-1][0].kind if self._results else None
        interleaving_bonus = (
            0.35 if previous_kind is not None and candidate.kind is not previous_kind else 0.0
        )

        if candidate.kind is ReviewActivityKind.PROGRAMMING:
            return (
                item.state.mastery_score * 0.8
                + correct * 1.25
                - incorrect * 0.9
                + interleaving_bonus
            )
        return (
            (1.0 - item.state.mastery_score) * 0.8 + incorrect - correct * 0.25 + interleaving_bonus
        )

    def _validate_catalog(self) -> None:
        for key, candidates in self._catalog.items():
            activity_keys = tuple(candidate.activity_key for candidate in candidates)
            if len(activity_keys) != len(set(activity_keys)):
                raise ValueError(f"Adaptive review catalog {key!r} contains duplicate activities.")
            for candidate in candidates:
                identity = (candidate.course_code, candidate.module_id)
                if identity != key[:2] or key[2] not in candidate.objective_ids:
                    raise ValueError(
                        "Adaptive review candidates must be indexed only by explicit "
                        "objective links."
                    )


__all__ = [
    "AdaptiveReviewActivity",
    "AdaptiveReviewProgramming",
    "AdaptiveReviewQuestion",
    "AdaptiveReviewSession",
    "AdaptiveReviewSummary",
    "ReviewActivityCandidate",
    "ReviewActivityKey",
    "ReviewActivityKind",
    "ReviewObjectiveKey",
    "ReviewProgrammingCandidate",
    "ReviewQuestionCandidate",
    "authored_review_activity_candidates",
    "authored_review_candidates",
    "authored_review_programming_candidates",
]
