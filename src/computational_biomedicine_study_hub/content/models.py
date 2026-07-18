"""Validated domain models for authored academic content.

The models are deliberately independent from PySide6 so academic material can be
unit-tested, indexed for retrieval and reused by multiple interfaces.
"""

from __future__ import annotations

from dataclasses import dataclass

from ..learning.activity_types import ActivityType


@dataclass(frozen=True, slots=True)
class LearningObjective:
    """One observable outcome for a learning module."""

    objective_id: str
    statement: str


@dataclass(frozen=True, slots=True)
class ConceptBlock:
    """A concise but complete explanation of one connected concept."""

    concept_id: str
    title: str
    body: str
    key_points: tuple[str, ...]


@dataclass(frozen=True, slots=True)
class WorkedExample:
    """A solved example connecting a problem statement to executable code."""

    example_id: str
    title: str
    problem: str
    reasoning: tuple[str, ...]
    code: str
    expected_output: str
    explanation: str


@dataclass(frozen=True, slots=True)
class PracticeExercise:
    """A formative exercise with hints and an authored reference solution."""

    exercise_id: str
    activity_type: ActivityType
    prompt: str
    hints: tuple[str, ...]
    solution: str
    explanation: str
    starter_code: str = ""


@dataclass(frozen=True, slots=True)
class AssessmentItem:
    """An assessable item with deterministic answers and feedback."""

    item_id: str
    activity_type: ActivityType
    prompt: str
    options: tuple[str, ...]
    correct_answers: tuple[str, ...]
    explanation: str
    rubric: tuple[str, ...] = ()

    def __post_init__(self) -> None:
        if not self.item_id.strip():
            raise ValueError("Assessment item IDs cannot be empty.")
        if not self.prompt.strip():
            raise ValueError(f"Assessment item {self.item_id!r} has an empty prompt.")
        if not self.correct_answers:
            raise ValueError(
                f"Assessment item {self.item_id!r} must define a correct answer."
            )

        option_based = {
            ActivityType.MULTIPLE_CHOICE,
            ActivityType.MULTIPLE_SELECT,
            ActivityType.TRUE_FALSE,
            ActivityType.MATCHING,
            ActivityType.ORDERING,
        }
        if self.activity_type in option_based and not self.options:
            raise ValueError(
                f"Assessment item {self.item_id!r} requires answer options."
            )

        if self.activity_type in {
            ActivityType.MULTIPLE_CHOICE,
            ActivityType.TRUE_FALSE,
        } and len(self.correct_answers) != 1:
            raise ValueError(
                f"Assessment item {self.item_id!r} requires exactly one answer."
            )

        invalid_answers = set(self.correct_answers) - set(self.options)
        if self.options and invalid_answers:
            raise ValueError(
                f"Assessment item {self.item_id!r} contains answers outside its options: "
                f"{sorted(invalid_answers)}"
            )


@dataclass(frozen=True, slots=True)
class TutorSupportPacket:
    """Authoritative material supplied to a local tutor model.

    This packet is not a free-form system prompt. It is authored subject matter that
    can later be split into retrieval documents and injected only when relevant.
    """

    canonical_explanation: str
    knowledge_fragments: tuple[str, ...]
    common_misconceptions: tuple[str, ...]
    socratic_questions: tuple[str, ...]
    grading_criteria: tuple[str, ...]
    response_constraints: tuple[str, ...]
    source_basis: tuple[str, ...]


@dataclass(frozen=True, slots=True)
class TutorKnowledgeDocument:
    """One indexable document derived from an authored learning module."""

    document_id: str
    title: str
    text: str
    tags: tuple[str, ...]


@dataclass(frozen=True, slots=True)
class LearningModule:
    """Complete authored unit for teaching, practice, assessment and tutoring."""

    course_code: str
    module_id: str
    title: str
    summary: str
    objectives: tuple[LearningObjective, ...]
    concepts: tuple[ConceptBlock, ...]
    worked_examples: tuple[WorkedExample, ...]
    practice_exercises: tuple[PracticeExercise, ...]
    assessment_items: tuple[AssessmentItem, ...]
    tutor_support: TutorSupportPacket

    def __post_init__(self) -> None:
        required_text = {
            "course_code": self.course_code,
            "module_id": self.module_id,
            "title": self.title,
            "summary": self.summary,
        }
        for field_name, value in required_text.items():
            if not value.strip():
                raise ValueError(f"Learning module field {field_name!r} cannot be empty.")

        required_collections = {
            "objectives": self.objectives,
            "concepts": self.concepts,
            "worked_examples": self.worked_examples,
            "practice_exercises": self.practice_exercises,
            "assessment_items": self.assessment_items,
        }
        for collection_name, values in required_collections.items():
            if not values:
                raise ValueError(
                    f"Learning module {self.module_id!r} requires {collection_name}."
                )

        self._validate_unique_ids(
            "objective",
            tuple(objective.objective_id for objective in self.objectives),
        )
        self._validate_unique_ids(
            "concept",
            tuple(concept.concept_id for concept in self.concepts),
        )
        self._validate_unique_ids(
            "worked example",
            tuple(example.example_id for example in self.worked_examples),
        )
        self._validate_unique_ids(
            "practice exercise",
            tuple(exercise.exercise_id for exercise in self.practice_exercises),
        )
        self._validate_unique_ids(
            "assessment item",
            tuple(item.item_id for item in self.assessment_items),
        )

    def tutor_documents(self) -> tuple[TutorKnowledgeDocument, ...]:
        """Build deterministic retrieval documents from the authored module."""
        tags = (self.course_code, self.module_id)
        documents: list[TutorKnowledgeDocument] = [
            TutorKnowledgeDocument(
                document_id=f"{self.module_id}.overview",
                title=f"{self.title}: authoritative overview",
                text=(
                    f"Module summary:\n{self.summary}\n\n"
                    f"Canonical explanation:\n"
                    f"{self.tutor_support.canonical_explanation}"
                ),
                tags=tags + ("overview",),
            )
        ]

        for concept in self.concepts:
            documents.append(
                TutorKnowledgeDocument(
                    document_id=f"{self.module_id}.concept.{concept.concept_id}",
                    title=concept.title,
                    text=(
                        f"{concept.body}\n\nKey points:\n- "
                        + "\n- ".join(concept.key_points)
                    ),
                    tags=tags + ("concept", concept.concept_id),
                )
            )

        for example in self.worked_examples:
            documents.append(
                TutorKnowledgeDocument(
                    document_id=f"{self.module_id}.example.{example.example_id}",
                    title=example.title,
                    text=(
                        f"Problem:\n{example.problem}\n\nReasoning:\n- "
                        + "\n- ".join(example.reasoning)
                        + f"\n\nCode:\n{example.code}\n\nExpected output:\n"
                        + example.expected_output
                        + f"\n\nExplanation:\n{example.explanation}"
                    ),
                    tags=tags + ("worked_example", example.example_id),
                )
            )

        for exercise in self.practice_exercises:
            documents.append(
                TutorKnowledgeDocument(
                    document_id=f"{self.module_id}.practice.{exercise.exercise_id}",
                    title=f"Practice: {exercise.exercise_id}",
                    text=(
                        f"Prompt:\n{exercise.prompt}\n\nReference solution:\n"
                        f"{exercise.solution}\n\nFeedback explanation:\n"
                        f"{exercise.explanation}"
                    ),
                    tags=tags + ("practice", exercise.activity_type.value),
                )
            )

        for item in self.assessment_items:
            documents.append(
                TutorKnowledgeDocument(
                    document_id=f"{self.module_id}.assessment.{item.item_id}",
                    title=f"Assessment: {item.item_id}",
                    text=(
                        f"Prompt:\n{item.prompt}\n\nCorrect answer(s):\n- "
                        + "\n- ".join(item.correct_answers)
                        + f"\n\nExplanation:\n{item.explanation}\n\nRubric:\n- "
                        + "\n- ".join(item.rubric)
                    ),
                    tags=tags + ("assessment", item.activity_type.value),
                )
            )

        documents.append(
            TutorKnowledgeDocument(
                document_id=f"{self.module_id}.tutor-guidance",
                title=f"{self.title}: tutor guidance",
                text=(
                    "Knowledge fragments:\n- "
                    + "\n- ".join(self.tutor_support.knowledge_fragments)
                    + "\n\nCommon misconceptions:\n- "
                    + "\n- ".join(self.tutor_support.common_misconceptions)
                    + "\n\nSocratic questions:\n- "
                    + "\n- ".join(self.tutor_support.socratic_questions)
                    + "\n\nGrading criteria:\n- "
                    + "\n- ".join(self.tutor_support.grading_criteria)
                    + "\n\nResponse constraints:\n- "
                    + "\n- ".join(self.tutor_support.response_constraints)
                ),
                tags=tags + ("tutor_guidance",),
            )
        )
        return tuple(documents)

    @staticmethod
    def _validate_unique_ids(label: str, identifiers: tuple[str, ...]) -> None:
        normalized = tuple(identifier.strip().casefold() for identifier in identifiers)
        if any(not identifier for identifier in normalized):
            raise ValueError(f"A {label} ID cannot be empty.")
        if len(normalized) != len(set(normalized)):
            raise ValueError(f"Duplicate {label} IDs are not allowed.")
