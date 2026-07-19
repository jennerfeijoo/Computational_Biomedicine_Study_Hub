"""Optional boundary for local tutor feedback on open responses."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Protocol

from .activity_types import ActivityType


@dataclass(frozen=True, slots=True)
class TutorFeedbackRequest:
    """Language- and course-scoped request for non-authoritative tutor feedback."""

    course_code: str
    module_id: str
    item_id: str
    activity_type: ActivityType
    response_text: str
    locale: str


@dataclass(frozen=True, slots=True)
class TutorFeedback:
    """Local model feedback kept separate from deterministic grading."""

    text: str
    source_ids: tuple[str, ...]


class LocalTutorFeedbackGateway(Protocol):
    """Optional adapter implemented by a future cancellable Ollama coordinator."""

    def request_feedback(self, request: TutorFeedbackRequest) -> TutorFeedback:
        """Return feedback without changing the application's objective score."""


__all__ = ["LocalTutorFeedbackGateway", "TutorFeedback", "TutorFeedbackRequest"]
