"""Renderer-neutral activity submission values."""

from __future__ import annotations

from dataclasses import dataclass

from .progress import AttemptOutcome, require_identifier


@dataclass(frozen=True, slots=True)
class ActivitySubmission:
    """One UI submission before a persistence coordinator adds course context."""

    item_id: str
    outcome: AttemptOutcome
    response_text: str = ""
    selected_option_ids: tuple[str, ...] = ()
    keyed_option_ids: tuple[tuple[str, str], ...] = ()
    is_correct: bool | None = None
    score: float | None = None

    def __post_init__(self) -> None:
        require_identifier(self.item_id, "item_id")
        keys = tuple(key for key, _ in self.keyed_option_ids)
        if len(keys) != len(set(keys)):
            raise ValueError("keyed_option_ids cannot contain duplicate keys.")
        if self.score is not None and not 0.0 <= self.score <= 1.0:
            raise ValueError("score must be between 0 and 1.")
        if self.is_correct is None and self.score is not None:
            raise ValueError("Open submissions cannot claim an objective score.")


__all__ = ["ActivitySubmission"]
