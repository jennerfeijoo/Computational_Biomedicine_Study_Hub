"""Tests for authoritative mentor grounding and deterministic objective evidence."""

from __future__ import annotations

from datetime import UTC, datetime, timedelta

from computational_biomedicine_study_hub.content.dm857 import BUNDLES
from computational_biomedicine_study_hub.learning.mentor_context import (
    build_module_mentor_context,
)
from computational_biomedicine_study_hub.learning.progress import MasteryState

NOW = datetime(2026, 8, 4, 12, 0, tzinfo=UTC)


class FakeProgress:
    def __init__(self, state: MasteryState) -> None:
        self._state = state
        self.calls: list[tuple[str, str | None, str | None]] = []

    def get_mastery(
        self,
        objective_id: str,
        *,
        course_code: str | None = None,
        module_id: str | None = None,
    ) -> MasteryState | None:
        self.calls.append((objective_id, course_code, module_id))
        return self._state if objective_id == self._state.objective_id else None


def _state(objective_id: str) -> MasteryState:
    return MasteryState(
        objective_id=objective_id,
        mastery_score=0.625,
        attempts=4,
        consecutive_correct=2,
        lapse_count=1,
        last_attempt_at=NOW,
        next_review_at=NOW + timedelta(days=2),
    )


def test_context_contains_authored_support_and_scoped_objective_evidence() -> None:
    module = BUNDLES[0].module
    progress = FakeProgress(_state(module.objectives[0].objective_id))

    context = build_module_mentor_context(
        module,
        section_index=1,
        section_label="Concepts",
        progress=progress,
    )

    assert f"course_code: {module.course_code}" in context
    assert f"module_id: {module.module_id}" in context
    assert "<deterministic_objective_evidence>" in context
    assert "mastery_score=0.625" in context
    assert "attempts=4" in context
    assert "no recorded evidence" in context
    assert "<authoritative_active_section>" in context
    assert module.concepts[0].body in context
    assert "<authoritative_tutor_support>" in context
    assert module.tutor_support.canonical_explanation in context
    assert progress.calls[0][1:] == (module.course_code, module.module_id)


def test_practice_context_protects_reference_solutions() -> None:
    module = BUNDLES[0].module

    context = build_module_mentor_context(
        module,
        section_index=3,
        section_label="Practice",
        progress=None,
    )

    assert "do not reveal a complete solution before the learner attempts" in context
    assert "<private_reference_solution>" in context
    assert module.practice_exercises[0].prompt in context
    assert module.practice_exercises[0].solution in context


def test_assessment_context_contains_private_keys_and_rubrics() -> None:
    module = BUNDLES[0].module

    context = build_module_mentor_context(
        module,
        section_index=4,
        section_label="Assessment",
        progress=None,
    )

    assert "Do not disclose an answer key before the learner submits an attempt" in context
    assert "<private_answer_key>" in context
    assert module.assessment_items[0].prompt in context
    assert module.assessment_items[0].correct_answers[0] in context


def test_context_rejects_unknown_reader_section() -> None:
    module = BUNDLES[0].module

    try:
        build_module_mentor_context(
            module,
            section_index=8,
            section_label="Unknown",
            progress=None,
        )
    except ValueError as exc:
        assert "section index" in str(exc)
    else:
        raise AssertionError("Unknown sections must be rejected.")
