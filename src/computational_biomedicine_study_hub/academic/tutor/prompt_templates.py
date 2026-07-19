"""Versioned prompt modes kept outside widgets."""

from __future__ import annotations

from enum import StrEnum

PROMPT_VERSION = "semester1-tutor-v1"


class TutorMode(StrEnum):
    ASK_CONTENT = "ask_content"
    SOCRATIC = "socratic"
    GENERATE_PRACTICE = "generate_practice"
    EVALUATE_OPEN = "evaluate_open"
    EXPLAIN_ERROR = "explain_error"
    ORAL_EXAM = "oral_exam"
    REVIEW_PLAN = "review_plan"
    COMPARE_METHODS = "compare_methods"
    ANALYZE_CODE = "analyze_code"
    CONTINUE_MODULE = "continue_module"


MODE_INSTRUCTIONS: dict[TutorMode, str] = {
    TutorMode.ASK_CONTENT: (
        "Explain progressively, give one grounded example, name a frequent error, "
        "and finish with one checking question."
    ),
    TutorMode.SOCRATIC: (
        "Ask exactly one question at a time. Do not reveal the answer immediately; "
        "offer a gradual hint and close only when the learner has reasoned it through."
    ),
    TutorMode.GENERATE_PRACTICE: (
        "Create one new question from the cited concepts. State difficulty and objective. "
        "Keep its reference answer and rubric out of the learner-visible prompt."
    ),
    TutorMode.EVALUATE_OPEN: (
        "Evaluate meaning rather than literal wording. Return only one valid JSON object "
        "with keys summary, strengths, missing_concepts, misconceptions, "
        "unsupported_claims, rubric_dimensions, suggested_revision, follow_up_question, "
        "source_ids, and evaluator_confidence. Each rubric_dimensions entry has name, "
        "score from 0 to 4, and evidence. Source IDs must come from supplied evidence. "
        "This is formative feedback, never an official grade."
    ),
    TutorMode.EXPLAIN_ERROR: (
        "Identify the mechanism behind the error, show a minimal correction, explain why "
        "it works, and ask the learner to predict one nearby case."
    ),
    TutorMode.ORAL_EXAM: (
        "Ask one oral question, require reasoning, then probe an assumption, alternative, "
        "interpretation, or limitation. Do not ask several questions at once."
    ),
    TutorMode.REVIEW_PLAN: (
        "Build a short ordered review session from the supplied evidence. Explain why each "
        "step is selected; do not invent mastery data."
    ),
    TutorMode.COMPARE_METHODS: (
        "Compare assumptions, target quantity, strengths, failure modes, and when each "
        "method is defensible."
    ),
    TutorMode.ANALYZE_CODE: (
        "Analyze the supplied code or output as text. Do not execute it. Trace relevant "
        "state, identify assumptions, and propose a testable correction."
    ),
    TutorMode.CONTINUE_MODULE: (
        "Continue from the cited module context and learner question without changing "
        "course, language, or difficulty."
    ),
}


__all__ = ["MODE_INSTRUCTIONS", "PROMPT_VERSION", "TutorMode"]
