"""Strict parsing for local formative-evaluation JSON."""

from __future__ import annotations

import json

from .response_models import OpenResponseFeedback


class FeedbackParseError(ValueError):
    pass


def parse_open_response_feedback(raw: str) -> OpenResponseFeedback:
    try:
        value = json.loads(raw)
    except json.JSONDecodeError as error:
        raise FeedbackParseError("Tutor feedback is not valid JSON.") from error
    if not isinstance(value, dict):
        raise FeedbackParseError("Tutor feedback must be a JSON object.")
    feedback = OpenResponseFeedback.from_mapping(value)
    if not feedback.summary or not feedback.source_ids:
        raise FeedbackParseError("Tutor feedback is missing its summary or source IDs.")
    return feedback


__all__ = ["FeedbackParseError", "parse_open_response_feedback"]
