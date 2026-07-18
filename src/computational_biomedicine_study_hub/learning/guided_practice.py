"""Randomized guided-practice sessions for authored formative exercises."""

from __future__ import annotations

import random
from dataclasses import dataclass

from ..content.models import PracticeExercise


@dataclass(frozen=True, slots=True)
class GuidedPracticeSession:
    """Immutable randomized set of formative exercises shown in one session."""

    exercises: tuple[PracticeExercise, ...]

    @property
    def exercise_ids(self) -> tuple[str, ...]:
        """Return stable authored exercise identifiers in display order."""
        return tuple(exercise.exercise_id for exercise in self.exercises)


class GuidedPracticeSessionGenerator:
    """Create varied sessions while preventing identical consecutive exercise sets."""

    def __init__(
        self,
        bank: tuple[PracticeExercise, ...],
        *,
        exercise_count: int = 4,
        rng: random.Random | None = None,
    ) -> None:
        if not bank:
            raise ValueError("The guided-practice bank cannot be empty.")
        if exercise_count < 1:
            raise ValueError("exercise_count must be at least 1.")
        if exercise_count > len(bank):
            raise ValueError("exercise_count cannot exceed the practice-bank size.")

        exercise_ids = tuple(exercise.exercise_id for exercise in bank)
        if len(exercise_ids) != len(set(exercise_ids)):
            raise ValueError("Guided-practice exercise IDs must be unique.")

        self._bank = bank
        self._exercise_count = exercise_count
        self._rng = rng or random.Random()
        self._previous_ids: frozenset[str] = frozenset()

    @property
    def bank_size(self) -> int:
        """Return the number of authored exercises available for sampling."""
        return len(self._bank)

    @property
    def exercise_count(self) -> int:
        """Return the number of exercises included in each session."""
        return self._exercise_count

    def new_session(self) -> GuidedPracticeSession:
        """Generate a shuffled session that differs from the previous set when possible."""
        selected = self._rng.sample(list(self._bank), self._exercise_count)
        selected = self._avoid_identical_consecutive_set(selected)
        self._rng.shuffle(selected)

        session = GuidedPracticeSession(tuple(selected))
        self._previous_ids = frozenset(session.exercise_ids)
        return session

    def _avoid_identical_consecutive_set(
        self,
        selected: list[PracticeExercise],
    ) -> list[PracticeExercise]:
        selected_ids = frozenset(exercise.exercise_id for exercise in selected)
        if not self._previous_ids or selected_ids != self._previous_ids:
            return selected

        alternatives = [
            exercise for exercise in self._bank if exercise.exercise_id not in self._previous_ids
        ]
        if not alternatives:
            return selected

        selected[self._rng.randrange(len(selected))] = self._rng.choice(alternatives)
        return selected


__all__ = ["GuidedPracticeSession", "GuidedPracticeSessionGenerator"]
