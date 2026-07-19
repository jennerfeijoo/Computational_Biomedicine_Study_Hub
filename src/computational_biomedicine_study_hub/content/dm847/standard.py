"""Validated compact authoring contract for complete DM847 modules."""

from __future__ import annotations

from dataclasses import dataclass

from ...i18n import AppLocale
from ...learning.activity_types import ActivityType
from ..localized_models import LocalizedAssessmentItem, LocalizedLearningModule
from ..models import AssessmentItem
from .authoring import (
    Triple,
    concept,
    example,
    objective,
    objective_mcq,
    objective_tf,
    practice,
    t,
    tutor_support,
)

ConceptSpec = tuple[str, Triple, Triple, tuple[Triple, ...]]
ExampleSpec = tuple[str, Triple, Triple, tuple[Triple, ...], str, str, Triple]
PracticeSpec = tuple[str, str, Triple, tuple[Triple, ...], Triple, Triple, str]
OptionSpec = tuple[str, Triple]
McqSpec = tuple[str, Triple, tuple[OptionSpec, ...], str, Triple]
TfSpec = tuple[str, Triple, bool, Triple]
TutorSpec = tuple[
    Triple,
    tuple[Triple, ...],
    tuple[Triple, ...],
    tuple[Triple, ...],
    tuple[Triple, ...],
    tuple[Triple, ...],
    tuple[str, ...],
]


@dataclass(frozen=True, slots=True)
class StandardModuleSpec:
    """A dense DM847 module with enforced academic coverage."""

    module_id: str
    title: Triple
    summary: Triple
    objectives: tuple[tuple[str, Triple], ...]
    concepts: tuple[ConceptSpec, ...]
    examples: tuple[ExampleSpec, ...]
    practices: tuple[PracticeSpec, ...]
    mcqs: tuple[McqSpec, ...]
    true_false: tuple[TfSpec, ...]
    tutor: TutorSpec

    def __post_init__(self) -> None:
        minimums = {
            "objectives": (len(self.objectives), 6),
            "concepts": (len(self.concepts), 6),
            "examples": (len(self.examples), 3),
            "practices": (len(self.practices), 8),
            "mcqs": (len(self.mcqs), 10),
            "true_false": (len(self.true_false), 10),
        }
        for name, (actual, minimum) in minimums.items():
            if actual < minimum:
                raise ValueError(
                    f"DM847 module {self.module_id!r} requires at least {minimum} {name}; "
                    f"received {actual}."
                )


def _assessment_items(spec: StandardModuleSpec) -> tuple[LocalizedAssessmentItem, ...]:
    sampled_mcqs = tuple(
        objective_mcq(
            f"{spec.module_id}.assessment.{index:03d}",
            prompt,
            options,
            correct_option_id,
            explanation,
        )
        for index, (_, prompt, options, correct_option_id, explanation) in enumerate(
            spec.mcqs[:5], start=1
        )
    )
    sampled_tf = tuple(
        objective_tf(
            f"{spec.module_id}.assessment.{index:03d}",
            prompt,
            correct=correct,
            explanation=explanation,
        )
        for index, (_, prompt, correct, explanation) in enumerate(spec.true_false[:5], start=6)
    )
    return sampled_mcqs + sampled_tf


def build_module(spec: StandardModuleSpec) -> LocalizedLearningModule:
    """Build and validate one complete trilingual DM847 learning module."""
    canonical, fragments, misconceptions, questions, criteria, constraints, sources = spec.tutor
    return LocalizedLearningModule(
        course_code="DM847",
        module_id=spec.module_id,
        title=t(*spec.title),
        summary=t(*spec.summary),
        objectives=tuple(objective(item_id, text) for item_id, text in spec.objectives),
        concepts=tuple(
            concept(concept_id, title, body, key_points)
            for concept_id, title, body, key_points in spec.concepts
        ),
        worked_examples=tuple(
            example(example_id, title, problem, reasoning, code, output, explanation)
            for example_id, title, problem, reasoning, code, output, explanation in spec.examples
        ),
        practice_exercises=tuple(
            practice(
                exercise_id,
                ActivityType[activity_type],
                prompt,
                hints,
                solution,
                explanation,
                starter_code,
            )
            for exercise_id, activity_type, prompt, hints, solution, explanation, starter_code in spec.practices
        ),
        assessment_items=_assessment_items(spec),
        tutor_support=tutor_support(
            canonical,
            fragments,
            misconceptions,
            questions,
            criteria,
            constraints,
            sources,
        ),
    )


def build_question_bank(spec: StandardModuleSpec) -> tuple[LocalizedAssessmentItem, ...]:
    """Build the stable 20-item objective bank for one module."""
    mcqs = tuple(
        objective_mcq(
            f"{spec.module_id}.bank.{item_id}",
            prompt,
            options,
            correct_option_id,
            explanation,
        )
        for item_id, prompt, options, correct_option_id, explanation in spec.mcqs
    )
    true_false = tuple(
        objective_tf(
            f"{spec.module_id}.bank.{item_id}",
            prompt,
            correct=correct,
            explanation=explanation,
        )
        for item_id, prompt, correct, explanation in spec.true_false
    )
    return mcqs + true_false


def materialize_bank(
    bank: tuple[LocalizedAssessmentItem, ...],
    locale: AppLocale | str = AppLocale.SPANISH_SPAIN,
) -> tuple[AssessmentItem, ...]:
    """Materialize one localized objective bank without changing answer identity."""
    resolved = locale if isinstance(locale, AppLocale) else AppLocale.resolve(locale)
    return tuple(item.materialize(resolved) for item in bank)


__all__ = [
    "ConceptSpec",
    "ExampleSpec",
    "McqSpec",
    "OptionSpec",
    "PracticeSpec",
    "StandardModuleSpec",
    "TfSpec",
    "TutorSpec",
    "build_module",
    "build_question_bank",
    "materialize_bank",
]
