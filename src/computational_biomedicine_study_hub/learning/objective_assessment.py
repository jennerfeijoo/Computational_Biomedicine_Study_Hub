"""Randomized, deterministically graded objective assessment sessions."""

from __future__ import annotations

import random
from dataclasses import dataclass
from typing import Final

from ..content.models import AssessmentItem
from .activity_types import ActivityType

_SUPPORTED_TYPES: Final = {
    ActivityType.MULTIPLE_CHOICE,
    ActivityType.TRUE_FALSE,
}


@dataclass(frozen=True, slots=True)
class ObjectiveSessionQuestion:
    """One authored item with a session-specific option order."""

    item: AssessmentItem
    display_options: tuple[str, ...]


@dataclass(frozen=True, slots=True)
class ObjectiveAssessmentSession:
    """A randomized, immutable set of questions shown in one attempt."""

    questions: tuple[ObjectiveSessionQuestion, ...]

    @property
    def item_ids(self) -> tuple[str, ...]:
        """Return stable item identifiers in display order."""
        return tuple(question.item.item_id for question in self.questions)


@dataclass(frozen=True, slots=True)
class ObjectiveAnswerFeedback:
    """Deterministic grading output for one selected answer."""

    is_correct: bool
    selected_answer: str
    correct_answer: str
    explanation: str


class ObjectiveSessionGenerator:
    """Create varied sessions while preventing identical consecutive question sets."""

    def __init__(
        self,
        bank: tuple[AssessmentItem, ...],
        *,
        question_count: int = 6,
        rng: random.Random | None = None,
    ) -> None:
        if question_count < 1:
            raise ValueError("question_count must be at least 1.")
        if question_count > len(bank):
            raise ValueError("question_count cannot exceed the question-bank size.")
        if not bank:
            raise ValueError("The objective question bank cannot be empty.")

        item_ids = tuple(item.item_id for item in bank)
        if len(item_ids) != len(set(item_ids)):
            raise ValueError("Objective question-bank IDs must be unique.")

        unsupported = tuple(item.item_id for item in bank if item.activity_type not in _SUPPORTED_TYPES)
        if unsupported:
            raise ValueError(
                "The first objective engine supports only multiple choice and true/false: "
                + ", ".join(unsupported)
            )

        self._bank = bank
        self._question_count = question_count
        self._rng = rng or random.Random()
        self._previous_ids: frozenset[str] = frozenset()

    @property
    def bank_size(self) -> int:
        """Return the number of authored questions available for sampling."""
        return len(self._bank)

    @property
    def question_count(self) -> int:
        """Return the number of questions included in each session."""
        return self._question_count

    def new_session(self) -> ObjectiveAssessmentSession:
        """Generate a session with shuffled questions and shuffled options."""
        selected = self._sample_balanced_questions()
        selected = self._avoid_identical_consecutive_set(selected)
        self._rng.shuffle(selected)

        questions: list[ObjectiveSessionQuestion] = []
        for item in selected:
            options = list(item.options)
            self._rng.shuffle(options)
            questions.append(ObjectiveSessionQuestion(item=item, display_options=tuple(options)))

        session = ObjectiveAssessmentSession(tuple(questions))
        self._previous_ids = frozenset(session.item_ids)
        return session

    def _sample_balanced_questions(self) -> list[AssessmentItem]:
        multiple_choice = [
            item for item in self._bank if item.activity_type is ActivityType.MULTIPLE_CHOICE
        ]
        true_false = [item for item in self._bank if item.activity_type is ActivityType.TRUE_FALSE]

        selected: list[AssessmentItem] = []
        if self._question_count >= 2 and multiple_choice and true_false:
            selected.append(self._rng.choice(multiple_choice))
            selected.append(self._rng.choice(true_false))

        remaining = [item for item in self._bank if item not in selected]
        remaining_count = self._question_count - len(selected)
        selected.extend(self._rng.sample(remaining, remaining_count))
        return selected

    def _avoid_identical_consecutive_set(
        self,
        selected: list[AssessmentItem],
    ) -> list[AssessmentItem]:
        selected_ids = frozenset(item.item_id for item in selected)
        if not self._previous_ids or selected_ids != self._previous_ids:
            return selected

        alternatives = [item for item in self._bank if item.item_id not in self._previous_ids]
        if not alternatives:
            return selected

        replacement = self._rng.choice(alternatives)
        replaceable_indices = [
            index
            for index, item in enumerate(selected)
            if item.activity_type is replacement.activity_type
        ]
        replace_index = (
            self._rng.choice(replaceable_indices)
            if replaceable_indices
            else self._rng.randrange(len(selected))
        )
        selected[replace_index] = replacement
        return selected


def grade_objective_answer(
    question: ObjectiveSessionQuestion,
    selected_answer: str,
) -> ObjectiveAnswerFeedback:
    """Grade one objective answer exactly against authored ground truth."""
    answer = selected_answer.strip()
    if answer not in question.item.options:
        raise ValueError("The selected answer is not one of the question options.")

    correct_answer = question.item.correct_answers[0]
    return ObjectiveAnswerFeedback(
        is_correct=answer == correct_answer,
        selected_answer=answer,
        correct_answer=correct_answer,
        explanation=question.item.explanation,
    )


__all__ = [
    "ObjectiveAnswerFeedback",
    "ObjectiveAssessmentSession",
    "ObjectiveSessionGenerator",
    "ObjectiveSessionQuestion",
    "grade_objective_answer",
]
