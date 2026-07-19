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
class AssessmentOption:
    """One visible answer option with a language-independent identity."""

    option_id: str
    text: str

    def __post_init__(self) -> None:
        if not self.option_id.strip():
            raise ValueError("Assessment option IDs cannot be empty.")
        if self.option_id != self.option_id.strip():
            raise ValueError("Assessment option IDs cannot contain surrounding whitespace.")
        if not self.text.strip():
            raise ValueError(f"Assessment option {self.option_id!r} cannot have empty text.")


@dataclass(frozen=True, slots=True)
class ClozeGap:
    """One language-independent gap with localized visible options."""

    gap_id: str
    options: tuple[AssessmentOption, ...]
    correct_option_id: str

    def __post_init__(self) -> None:
        if not self.gap_id.strip():
            raise ValueError("Cloze gap IDs cannot be empty.")
        if self.gap_id != self.gap_id.strip():
            raise ValueError("Cloze gap IDs cannot contain surrounding whitespace.")
        if len(self.options) < 2:
            raise ValueError(f"Cloze gap {self.gap_id!r} requires at least two options.")
        option_ids = tuple(option.option_id for option in self.options)
        normalized = tuple(option_id.casefold() for option_id in option_ids)
        if len(normalized) != len(set(normalized)):
            raise ValueError(f"Cloze gap {self.gap_id!r} has duplicate option IDs.")
        if self.correct_option_id not in option_ids:
            raise ValueError(
                f"Cloze gap {self.gap_id!r} references unknown correct option ID "
                f"{self.correct_option_id!r}."
            )


@dataclass(frozen=True, slots=True)
class AssessmentItem:
    """An assessable item with deterministic, locale-independent answer keys.

    ``options`` and ``correct_answers`` remain as compatibility-facing visible text.
    ``option_ids`` and ``correct_option_ids`` are the authoritative identities used by
    objective grading and future persistence. Legacy monolingual content receives
    deterministic generated IDs during validation.
    """

    item_id: str
    activity_type: ActivityType
    prompt: str
    options: tuple[str, ...]
    correct_answers: tuple[str, ...]
    explanation: str
    rubric: tuple[str, ...] = ()
    option_ids: tuple[str, ...] = ()
    correct_option_ids: tuple[str, ...] = ()
    cloze_gaps: tuple[ClozeGap, ...] = ()

    def __post_init__(self) -> None:
        if not self.item_id.strip():
            raise ValueError("Assessment item IDs cannot be empty.")
        if self.item_id != self.item_id.strip():
            raise ValueError("Assessment item IDs cannot contain surrounding whitespace.")
        if not self.prompt.strip():
            raise ValueError(f"Assessment item {self.item_id!r} has an empty prompt.")
        if not self.explanation.strip():
            raise ValueError(f"Assessment item {self.item_id!r} has an empty explanation.")
        is_cloze = self.activity_type is ActivityType.CLOZE_CHOICE
        if not is_cloze and not self.correct_answers:
            raise ValueError(f"Assessment item {self.item_id!r} must define a correct answer.")

        if is_cloze:
            if not self.cloze_gaps:
                raise ValueError(f"Cloze item {self.item_id!r} requires at least one gap.")
            if self.options or self.option_ids or self.correct_option_ids or self.correct_answers:
                raise ValueError(f"Cloze item {self.item_id!r} must keep answers inside its gaps.")
            gap_ids = tuple(gap.gap_id for gap in self.cloze_gaps)
            if len(gap_ids) != len(set(gap_id.casefold() for gap_id in gap_ids)):
                raise ValueError(f"Cloze item {self.item_id!r} has duplicate gap IDs.")
            missing_markers = tuple(
                gap_id for gap_id in gap_ids if "{" + gap_id + "}" not in self.prompt
            )
            if missing_markers:
                raise ValueError(
                    f"Cloze item {self.item_id!r} is missing prompt markers for gaps: "
                    f"{list(missing_markers)}"
                )
            return

        if self.cloze_gaps:
            raise ValueError(
                f"Assessment item {self.item_id!r} cannot define gaps for "
                f"{self.activity_type.value!r}."
            )

        option_based = {
            ActivityType.MULTIPLE_CHOICE,
            ActivityType.MULTIPLE_SELECT,
            ActivityType.TRUE_FALSE,
            ActivityType.MATCHING,
            ActivityType.ORDERING,
        }
        is_option_based = self.activity_type in option_based

        if is_option_based and not self.options:
            raise ValueError(f"Assessment item {self.item_id!r} requires answer options.")
        if not is_option_based and (self.option_ids or self.correct_option_ids):
            raise ValueError(
                f"Assessment item {self.item_id!r} cannot use option IDs for free-text grading."
            )

        if (
            self.activity_type
            in {
                ActivityType.MULTIPLE_CHOICE,
                ActivityType.TRUE_FALSE,
            }
            and len(self.correct_answers) != 1
        ):
            raise ValueError(f"Assessment item {self.item_id!r} requires exactly one answer.")

        if self.options:
            self._validate_visible_options()
            effective_option_ids = self.option_ids or tuple(
                f"option_{index}" for index in range(1, len(self.options) + 1)
            )
            self._validate_option_ids(effective_option_ids)
            object.__setattr__(self, "option_ids", effective_option_ids)

            invalid_answers = set(self.correct_answers) - set(self.options)
            if invalid_answers:
                raise ValueError(
                    f"Assessment item {self.item_id!r} contains answers outside its options: "
                    f"{sorted(invalid_answers)}"
                )

            effective_correct_ids = self.correct_option_ids or tuple(
                effective_option_ids[self.options.index(answer)] for answer in self.correct_answers
            )
            invalid_ids = set(effective_correct_ids) - set(effective_option_ids)
            if invalid_ids:
                raise ValueError(
                    f"Assessment item {self.item_id!r} references unknown option IDs: "
                    f"{sorted(invalid_ids)}"
                )
            if len(effective_correct_ids) != len(self.correct_answers):
                raise ValueError(
                    f"Assessment item {self.item_id!r} has misaligned answer text and option IDs."
                )

            text_by_id = dict(zip(effective_option_ids, self.options, strict=True))
            for answer_text, option_id in zip(
                self.correct_answers,
                effective_correct_ids,
                strict=True,
            ):
                if text_by_id[option_id] != answer_text:
                    raise ValueError(
                        f"Assessment item {self.item_id!r} maps option ID {option_id!r} "
                        "to the wrong visible answer."
                    )
            object.__setattr__(self, "correct_option_ids", effective_correct_ids)

    @property
    def option_objects(self) -> tuple[AssessmentOption, ...]:
        """Return stable IDs paired with their visible localized text."""
        return tuple(
            AssessmentOption(option_id=option_id, text=text)
            for option_id, text in zip(self.option_ids, self.options, strict=True)
        )

    def option_text(self, option_id: str) -> str:
        """Resolve visible text for one stable option ID."""
        for option in self.option_objects:
            if option.option_id == option_id:
                return option.text
        raise KeyError(option_id)

    def _validate_visible_options(self) -> None:
        normalized = tuple(option.strip().casefold() for option in self.options)
        if any(not option for option in normalized):
            raise ValueError(f"Assessment item {self.item_id!r} contains an empty option.")
        if len(normalized) != len(set(normalized)):
            raise ValueError(
                f"Assessment item {self.item_id!r} contains duplicate visible options."
            )

    def _validate_option_ids(self, option_ids: tuple[str, ...]) -> None:
        if len(option_ids) != len(self.options):
            raise ValueError(
                f"Assessment item {self.item_id!r} must define one option ID per option."
            )
        normalized = tuple(option_id.strip().casefold() for option_id in option_ids)
        if any(not option_id for option_id in normalized):
            raise ValueError(f"Assessment item {self.item_id!r} contains an empty option ID.")
        if any(option_id != option_id.strip() for option_id in option_ids):
            raise ValueError(
                f"Assessment item {self.item_id!r} has option IDs with surrounding whitespace."
            )
        if len(normalized) != len(set(normalized)):
            raise ValueError(f"Assessment item {self.item_id!r} has duplicate option IDs.")


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
                raise ValueError(f"Learning module {self.module_id!r} requires {collection_name}.")

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
                    text=(f"{concept.body}\n\nKey points:\n- " + "\n- ".join(concept.key_points)),
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
