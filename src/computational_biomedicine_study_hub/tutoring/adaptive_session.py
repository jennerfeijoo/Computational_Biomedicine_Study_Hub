"""Bounded adaptive tutoring state for one verified programming diagnostic."""

from __future__ import annotations

from dataclasses import dataclass, replace
from enum import StrEnum


class TutorAssistanceLevel(StrEnum):
    """Ordered pedagogical support levels offered by the contextual tutor."""

    SOCRATIC = "socratic"
    CONCEPTUAL = "conceptual"
    STRUCTURAL = "structural"
    EXPLANATION = "explanation"

    @property
    def rank(self) -> int:
        """Return the stable zero-based assistance rank."""

        return tuple(type(self)).index(self)

    @property
    def next_level(self) -> TutorAssistanceLevel:
        """Return the next stronger level, capped at a full explanation."""

        levels = tuple(type(self))
        return levels[min(self.rank + 1, len(levels) - 1)]


@dataclass(frozen=True, slots=True)
class TutorSessionTurn:
    """One source-traceable question and response within a diagnostic session."""

    question: str
    response: str
    assistance_level: TutorAssistanceLevel
    model: str
    source_ids: tuple[str, ...]
    helpful: bool | None = None

    def __post_init__(self) -> None:
        required = {
            "question": self.question,
            "response": self.response,
            "model": self.model,
        }
        for field_name, value in required.items():
            if not value.strip():
                raise ValueError(f"Tutor turn field {field_name!r} cannot be empty.")
            if value != value.strip():
                raise ValueError(
                    f"Tutor turn field {field_name!r} cannot contain surrounding whitespace."
                )
        if not self.source_ids:
            raise ValueError("Tutor turns require at least one authored source ID.")
        normalized = tuple(source_id.strip().casefold() for source_id in self.source_ids)
        if any(not source_id for source_id in normalized):
            raise ValueError("Tutor source IDs cannot be empty.")
        if any(source_id != source_id.strip() for source_id in self.source_ids):
            raise ValueError("Tutor source IDs cannot contain surrounding whitespace.")
        if len(normalized) != len(set(normalized)):
            raise ValueError("Tutor source IDs cannot contain duplicates.")

    def rated(self, helpful: bool) -> TutorSessionTurn:
        """Return a copy carrying the learner's usefulness judgement."""

        return replace(self, helpful=helpful)


@dataclass(frozen=True, slots=True)
class TutorSessionSnapshot:
    """Immutable bounded conversation state supplied to the next model request."""

    turns: tuple[TutorSessionTurn, ...] = ()

    @property
    def assistance_count(self) -> int:
        """Return the number of accepted tutor responses in this session."""

        return len(self.turns)

    @property
    def strongest_level(self) -> TutorAssistanceLevel | None:
        """Return the strongest assistance level used in the session."""

        if not self.turns:
            return None
        return max((turn.assistance_level for turn in self.turns), key=lambda level: level.rank)

    @property
    def solution_revealed(self) -> bool:
        """Return whether a full-explanation response was requested."""

        return any(turn.assistance_level is TutorAssistanceLevel.EXPLANATION for turn in self.turns)

    def append(self, turn: TutorSessionTurn, *, max_turns: int = 6) -> TutorSessionSnapshot:
        """Append one turn while retaining only the newest local session context."""

        if max_turns < 1:
            raise ValueError("max_turns must be at least 1.")
        return TutorSessionSnapshot((*self.turns, turn)[-max_turns:])

    def rate_latest(self, helpful: bool) -> TutorSessionSnapshot:
        """Rate the newest response without mutating earlier source evidence."""

        if not self.turns:
            raise ValueError("Cannot rate an empty tutor session.")
        return TutorSessionSnapshot((*self.turns[:-1], self.turns[-1].rated(helpful)))


def bounded_history(
    turns: tuple[TutorSessionTurn, ...],
    *,
    max_turns: int = 3,
    max_characters: int = 3_000,
) -> tuple[TutorSessionTurn, ...]:
    """Return the newest complete turns that fit a deterministic prompt budget."""

    if max_turns < 1:
        raise ValueError("max_turns must be at least 1.")
    if max_characters < 400:
        raise ValueError("max_characters must be at least 400.")

    selected: list[TutorSessionTurn] = []
    used = 0
    for turn in reversed(turns[-max_turns:]):
        cost = len(turn.question) + len(turn.response) + sum(map(len, turn.source_ids)) + 120
        if selected and used + cost > max_characters:
            break
        if not selected and cost > max_characters:
            response_budget = max(120, max_characters - len(turn.question) - 180)
            selected.append(
                replace(
                    turn,
                    response=_truncate(turn.response, response_budget),
                )
            )
            break
        selected.append(turn)
        used += cost
    return tuple(reversed(selected))


def _truncate(text: str, limit: int) -> str:
    if len(text) <= limit:
        return text
    candidate = text[: max(1, limit - 1)]
    boundary = max(candidate.rfind("\n\n"), candidate.rfind(". "))
    if boundary >= int(limit * 0.55):
        candidate = candidate[: boundary + 1]
    return candidate.rstrip() + "…"


__all__ = [
    "TutorAssistanceLevel",
    "TutorSessionSnapshot",
    "TutorSessionTurn",
    "bounded_history",
]
