"""Randomized assessment sessions for deterministic closed questions."""

from __future__ import annotations

from dataclasses import dataclass
from random import Random
from secrets import randbits

from ..content.models import AssessmentItem
from .activity_types import ActivityType

SUPPORTED_ACTIVITY_TYPES = frozenset(
    {
        ActivityType.MULTIPLE_CHOICE,
        ActivityType.TRUE_FALSE,
    }
)


@dataclass(frozen=True, slots=True)
class PresentedQuestion:
    """One assessment item with its display order fixed for a session."""

    item: AssessmentItem
    options: tuple[str, ...]


@dataclass(frozen=True, slots=True)
class AnswerFeedback:
    """Deterministic result returned after one submitted answer."""

    item_id: str
    selected_answer: str
    correct_answer: str
    is_correct: bool
    explanation: str


class AssessmentSession:
    """Manage one randomized, non-repeating set of closed questions."""

    def __init__(
        self,
        question_bank: tuple[AssessmentItem, ...],
        *,
        question_count: int = 6,
        seed: int | None = None,
        previous_item_ids: tuple[str, ...] = (),
    ) -> None:
        self._validate_bank(question_bank, question_count)
        self._rng = Random(seed if seed is not None else randbits(64))
        self._questions = self._sample_questions(
            question_bank,
            question_count,
            previous_item_ids,
        )
        self._current_index = 0
        self._feedback: list[AnswerFeedback] = []

    @property
    def questions(self) -> tuple[PresentedQuestion, ...]:
        """Return all questions selected for this session."""
        return self._questions

    @property
    def item_ids(self) -> tuple[str, ...]:
        """Return the stable IDs selected for this session."""
        return tuple(question.item.item_id for question in self._questions)

    @property
    def current_question(self) -> PresentedQuestion:
        """Return the question currently awaiting an answer."""
        return self._questions[self._current_index]

    @property
    def current_number(self) -> int:
        """Return the one-based position of the current question."""
        return self._current_index + 1

    @property
    def question_count(self) -> int:
        """Return the number of questions in the session."""
        return len(self._questions)

    @property
    def answered_count(self) -> int:
        """Return how many answers have been submitted."""
        return len(self._feedback)

    @property
    def score(self) -> int:
        """Return the number of correct submitted answers."""
        return sum(result.is_correct for result in self._feedback)

    @property
    def is_complete(self) -> bool:
        """Return whether every selected question has been answered."""
        return self.answered_count == self.question_count

    @property
    def current_is_answered(self) -> bool:
        """Return whether the current question already has feedback."""
        return self.answered_count > self._current_index

    def submit(self, selected_answer: str) -> AnswerFeedback:
        """Grade the current answer without using a language model."""
        if self.current_is_answered:
            raise RuntimeError("The current question has already been answered.")

        normalized = selected_answer.strip()
        if normalized not in self.current_question.options:
            raise ValueError("The selected answer is not an option for the current question.")

        item = self.current_question.item
        correct_answer = item.correct_answers[0]
        result = AnswerFeedback(
            item_id=item.item_id,
            selected_answer=normalized,
            correct_answer=correct_answer,
            is_correct=normalized == correct_answer,
            explanation=item.explanation,
        )
        self._feedback.append(result)
        return result

    def advance(self) -> bool:
        """Move to the next question after grading the current one."""
        if not self.current_is_answered:
            raise RuntimeError("Submit an answer before advancing.")
        if self._current_index >= self.question_count - 1:
            return False
        self._current_index += 1
        return True

    def _sample_questions(
        self,
        question_bank: tuple[AssessmentItem, ...],
        question_count: int,
        previous_item_ids: tuple[str, ...],
    ) -> tuple[PresentedQuestion, ...]:
        selected = self._rng.sample(question_bank, question_count)
        selected_ids = tuple(item.item_id for item in selected)

        if (
            previous_item_ids
            and selected_ids == previous_item_ids
            and len(question_bank) > question_count
        ):
            selected = self._replace_last_question(selected, question_bank)

        questions: list[PresentedQuestion] = []
        for item in selected:
            options = list(item.options)
            self._rng.shuffle(options)
            questions.append(PresentedQuestion(item=item, options=tuple(options)))
        return tuple(questions)

    def _replace_last_question(
        self,
        selected: list[AssessmentItem],
        question_bank: tuple[AssessmentItem, ...],
    ) -> list[AssessmentItem]:
        selected_ids = {item.item_id for item in selected}
        alternatives = [item for item in question_bank if item.item_id not in selected_ids]
        replacement = self._rng.choice(alternatives)
        return [*selected[:-1], replacement]

    @staticmethod
    def _validate_bank(
        question_bank: tuple[AssessmentItem, ...],
        question_count: int,
    ) -> None:
        if question_count < 1:
            raise ValueError("An assessment session requires at least one question.")
        if question_count > len(question_bank):
            raise ValueError("The requested session is larger than the question bank.")

        item_ids = [item.item_id for item in question_bank]
        if len(item_ids) != len(set(item_ids)):
            raise ValueError("Assessment question IDs must be unique.")

        unsupported = [
            item.item_id
            for item in question_bank
            if item.activity_type not in SUPPORTED_ACTIVITY_TYPES
        ]
        if unsupported:
            raise ValueError(
                "The first interactive engine supports only multiple choice and true/false: "
                + ", ".join(unsupported)
            )
