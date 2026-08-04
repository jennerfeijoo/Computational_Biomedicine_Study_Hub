"""Authoritative course and objective evidence supplied to the local mentor."""

from __future__ import annotations

from typing import Protocol

from ..content.models import LearningModule
from .progress import MasteryState

MAX_ACTIVE_SECTION_CHARACTERS = 18_000


class MentorProgressReader(Protocol):
    """Read-only objective evidence required for mentor grounding."""

    def get_mastery(
        self,
        objective_id: str,
        *,
        course_code: str | None = None,
        module_id: str | None = None,
    ) -> MasteryState | None:
        """Return deterministic objective mastery evidence."""


def build_module_mentor_context(
    module: LearningModule,
    *,
    section_index: int,
    section_label: str,
    progress: MentorProgressReader | None,
) -> str:
    """Build bounded authoritative context for Socratic mentoring.

    Reference solutions and answer keys are clearly delimited so the mentor can evaluate
    learner work without immediately disclosing them. Objective evidence comes only from
    deterministic stored attempts; it is not inferred by the language model.
    """

    if not 0 <= section_index <= 4:
        raise ValueError("Module mentor context requires a section index from zero to four.")

    return "\n\n".join(
        (
            _module_identity(module, section_index, section_label),
            _objective_evidence(module, progress),
            _active_section_material(module, section_index),
            _tutor_support(module),
        )
    )


def _module_identity(module: LearningModule, section_index: int, section_label: str) -> str:
    return (
        "<module_identity>\n"
        f"course_code: {module.course_code}\n"
        f"module_id: {module.module_id}\n"
        f"title: {module.title}\n"
        f"summary: {module.summary}\n"
        f"visible_section_index: {section_index}\n"
        f"visible_section_label: {section_label.strip()}\n"
        "</module_identity>"
    )


def _objective_evidence(
    module: LearningModule,
    progress: MentorProgressReader | None,
) -> str:
    lines = [
        "<deterministic_objective_evidence>",
        "This evidence is generated from stored assessment attempts, not from model inference.",
    ]
    for objective in module.objectives:
        state = (
            progress.get_mastery(
                objective.objective_id,
                course_code=module.course_code,
                module_id=module.module_id,
            )
            if progress is not None
            else None
        )
        if state is None:
            lines.append(
                f"- {objective.objective_id}: {objective.statement} | no recorded evidence"
            )
            continue
        lines.append(
            f"- {objective.objective_id}: {objective.statement} | "
            f"mastery_score={state.mastery_score:.3f}; attempts={state.attempts}; "
            f"consecutive_correct={state.consecutive_correct}; lapses={state.lapse_count}; "
            f"next_review={state.next_review_at.isoformat()}"
        )
    lines.append("</deterministic_objective_evidence>")
    return "\n".join(lines)


def _active_section_material(module: LearningModule, section_index: int) -> str:
    material = {
        0: _overview_material(module),
        1: _concept_material(module),
        2: _example_material(module),
        3: _practice_material(module),
        4: _assessment_material(module),
    }[section_index]
    bounded = material[:MAX_ACTIVE_SECTION_CHARACTERS]
    truncation = (
        "\n[The authored section exceeded the mentor context limit; additional material was "
        "not supplied in this turn.]"
        if len(material) > MAX_ACTIVE_SECTION_CHARACTERS
        else ""
    )
    return f"<authoritative_active_section>\n{bounded}{truncation}\n</authoritative_active_section>"


def _overview_material(module: LearningModule) -> str:
    objectives = "\n".join(
        f"- {objective.objective_id}: {objective.statement}" for objective in module.objectives
    )
    return f"Module purpose:\n{module.summary}\n\nLearning objectives:\n{objectives}"


def _concept_material(module: LearningModule) -> str:
    blocks: list[str] = []
    for concept in module.concepts:
        blocks.append(
            f"Concept {concept.concept_id}: {concept.title}\n"
            f"{concept.body}\n"
            "Key points:\n- " + "\n- ".join(concept.key_points)
        )
    return "\n\n".join(blocks)


def _example_material(module: LearningModule) -> str:
    blocks: list[str] = []
    for example in module.worked_examples:
        blocks.append(
            f"Worked example {example.example_id}: {example.title}\n"
            f"Problem:\n{example.problem}\n"
            "Reasoning:\n- " + "\n- ".join(example.reasoning) + f"\nCode:\n{example.code}\n"
            f"Expected output:\n{example.expected_output}\n"
            f"Explanation:\n{example.explanation}"
        )
    return "\n\n".join(blocks)


def _practice_material(module: LearningModule) -> str:
    blocks: list[str] = [
        "The following reference solutions are private mentor material. In Socratic and practice "
        "modes, do not reveal a complete solution before the learner attempts the task."
    ]
    for exercise in module.practice_exercises:
        blocks.append(
            f"Practice {exercise.exercise_id} ({exercise.activity_type.value})\n"
            f"Prompt:\n{exercise.prompt}\n"
            "Hints:\n- "
            + "\n- ".join(exercise.hints)
            + f"\nStarter code:\n{exercise.starter_code or '[none]'}\n"
            f"<private_reference_solution>\n{exercise.solution}\n"
            f"Explanation:\n{exercise.explanation}\n</private_reference_solution>"
        )
    return "\n\n".join(blocks)


def _assessment_material(module: LearningModule) -> str:
    blocks: list[str] = [
        "The following keys and rubrics are private mentor material. Do not disclose an answer key "
        "before the learner submits an attempt. Use it for targeted feedback and follow-up questions."
    ]
    for item in module.assessment_items:
        options = "\n- ".join(item.options) if item.options else "[free response]"
        rubric = "\n- ".join(item.rubric) if item.rubric else "[no authored rubric]"
        blocks.append(
            f"Assessment {item.item_id} ({item.activity_type.value})\n"
            f"Prompt:\n{item.prompt}\n"
            f"Options:\n- {options}\n"
            "<private_answer_key>\nCorrect answer(s):\n- "
            + "\n- ".join(item.correct_answers)
            + f"\nExplanation:\n{item.explanation}\nRubric:\n- {rubric}\n"
            "</private_answer_key>"
        )
    return "\n\n".join(blocks)


def _tutor_support(module: LearningModule) -> str:
    support = module.tutor_support
    return (
        "<authoritative_tutor_support>\n"
        f"Canonical explanation:\n{support.canonical_explanation}\n\n"
        "Knowledge fragments:\n- "
        + "\n- ".join(support.knowledge_fragments)
        + "\n\nCommon misconceptions:\n- "
        + "\n- ".join(support.common_misconceptions)
        + "\n\nAuthored Socratic questions:\n- "
        + "\n- ".join(support.socratic_questions)
        + "\n\nGrading criteria:\n- "
        + "\n- ".join(support.grading_criteria)
        + "\n\nResponse constraints:\n- "
        + "\n- ".join(support.response_constraints)
        + "\n\nSource basis:\n- "
        + "\n- ".join(support.source_basis)
        + "\n</authoritative_tutor_support>"
    )


__all__ = [
    "MAX_ACTIVE_SECTION_CHARACTERS",
    "MentorProgressReader",
    "build_module_mentor_context",
]
