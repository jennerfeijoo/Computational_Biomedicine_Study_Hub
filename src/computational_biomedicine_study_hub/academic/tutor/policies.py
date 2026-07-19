"""Academic safety and hidden-support authorization."""

from __future__ import annotations

from dataclasses import dataclass

from .prompt_templates import TutorMode


@dataclass(frozen=True, slots=True)
class TutorAccessContext:
    mode: TutorMode
    learner_submitted_response: bool = False
    follow_up_after_feedback: bool = False


def hidden_support_allowed(context: TutorAccessContext) -> bool:
    return (
        context.learner_submitted_response
        and context.mode
        in {
            TutorMode.EVALUATE_OPEN,
            TutorMode.EXPLAIN_ERROR,
            TutorMode.ORAL_EXAM,
        }
    ) or context.follow_up_after_feedback


__all__ = ["TutorAccessContext", "hidden_support_allowed"]
