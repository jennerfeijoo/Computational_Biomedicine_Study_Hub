"""Strict trilingual academic models and runtime materialization.

These models are the authoring contract for content that is complete in Spanish,
English and Danish. They convert into the existing monolingual runtime models so the
reader, assessment engine and tutor can remain locale-agnostic.
"""

from __future__ import annotations

from dataclasses import dataclass

from ..i18n import AppLocale
from ..learning.activity_types import ActivityType
from .models import (
    AssessmentItem,
    AssessmentOption,
    ClozeGap,
    ConceptBlock,
    LearningModule,
    LearningObjective,
    PracticeExercise,
    TutorSupportPacket,
    WorkedExample,
)


@dataclass(frozen=True, slots=True)
class LocalizedText:
    """One required non-empty text in every supported application locale."""

    spanish: str
    english: str
    danish: str

    def __post_init__(self) -> None:
        values = {
            AppLocale.SPANISH_SPAIN: self.spanish,
            AppLocale.ENGLISH: self.english,
            AppLocale.DANISH_DENMARK: self.danish,
        }
        for locale, value in values.items():
            if not value.strip():
                raise ValueError(f"Localized text cannot be empty for locale {locale.value!r}.")

    def for_locale(self, locale: AppLocale | str) -> str:
        """Return the text for one supported locale without fallback."""
        resolved = locale if isinstance(locale, AppLocale) else AppLocale.resolve(locale)
        if resolved is AppLocale.SPANISH_SPAIN:
            return self.spanish
        if resolved is AppLocale.ENGLISH:
            return self.english
        return self.danish

    def as_dict(self) -> dict[AppLocale, str]:
        """Return an explicit locale-to-text mapping for validation and export."""
        return {
            AppLocale.SPANISH_SPAIN: self.spanish,
            AppLocale.ENGLISH: self.english,
            AppLocale.DANISH_DENMARK: self.danish,
        }


@dataclass(frozen=True, slots=True)
class LocalizedLearningObjective:
    """One stable learning objective with a trilingual statement."""

    objective_id: str
    statement: LocalizedText

    def materialize(self, locale: AppLocale) -> LearningObjective:
        return LearningObjective(self.objective_id, self.statement.for_locale(locale))


@dataclass(frozen=True, slots=True)
class LocalizedConceptBlock:
    """One trilingual concept explanation with aligned key points."""

    concept_id: str
    title: LocalizedText
    body: LocalizedText
    key_points: tuple[LocalizedText, ...]

    def __post_init__(self) -> None:
        if not self.key_points:
            raise ValueError(f"Concept {self.concept_id!r} requires key points.")

    def materialize(self, locale: AppLocale) -> ConceptBlock:
        return ConceptBlock(
            concept_id=self.concept_id,
            title=self.title.for_locale(locale),
            body=self.body.for_locale(locale),
            key_points=tuple(point.for_locale(locale) for point in self.key_points),
        )


@dataclass(frozen=True, slots=True)
class LocalizedWorkedExample:
    """One solved example whose complete visible content is localized."""

    example_id: str
    title: LocalizedText
    problem: LocalizedText
    reasoning: tuple[LocalizedText, ...]
    code: LocalizedText
    expected_output: LocalizedText
    explanation: LocalizedText

    def __post_init__(self) -> None:
        if not self.reasoning:
            raise ValueError(f"Worked example {self.example_id!r} requires reasoning steps.")

    def materialize(self, locale: AppLocale) -> WorkedExample:
        return WorkedExample(
            example_id=self.example_id,
            title=self.title.for_locale(locale),
            problem=self.problem.for_locale(locale),
            reasoning=tuple(step.for_locale(locale) for step in self.reasoning),
            code=self.code.for_locale(locale),
            expected_output=self.expected_output.for_locale(locale),
            explanation=self.explanation.for_locale(locale),
        )


@dataclass(frozen=True, slots=True)
class LocalizedPracticeExercise:
    """One trilingual formative exercise with hints and reference solution."""

    exercise_id: str
    activity_type: ActivityType
    prompt: LocalizedText
    hints: tuple[LocalizedText, ...]
    solution: LocalizedText
    explanation: LocalizedText
    starter_code: LocalizedText | None = None

    def __post_init__(self) -> None:
        if not self.hints:
            raise ValueError(f"Practice exercise {self.exercise_id!r} requires hints.")

    def materialize(self, locale: AppLocale) -> PracticeExercise:
        return PracticeExercise(
            exercise_id=self.exercise_id,
            activity_type=self.activity_type,
            prompt=self.prompt.for_locale(locale),
            hints=tuple(hint.for_locale(locale) for hint in self.hints),
            solution=self.solution.for_locale(locale),
            explanation=self.explanation.for_locale(locale),
            starter_code=(
                self.starter_code.for_locale(locale) if self.starter_code is not None else ""
            ),
        )


@dataclass(frozen=True, slots=True)
class LocalizedAssessmentOption:
    """One answer option with a language-independent identity."""

    option_id: str
    text: LocalizedText

    def __post_init__(self) -> None:
        if not self.option_id.strip():
            raise ValueError("Assessment option IDs cannot be empty.")
        if self.option_id != self.option_id.strip():
            raise ValueError("Assessment option IDs cannot contain surrounding whitespace.")


@dataclass(frozen=True, slots=True)
class LocalizedClozeGap:
    """One stable cloze gap whose visible options are aligned in three locales."""

    gap_id: str
    options: tuple[LocalizedAssessmentOption, ...]
    correct_option_id: str

    def __post_init__(self) -> None:
        if not self.gap_id.strip():
            raise ValueError("Cloze gap IDs cannot be empty.")
        if self.gap_id != self.gap_id.strip():
            raise ValueError("Cloze gap IDs cannot contain surrounding whitespace.")
        if len(self.options) < 2:
            raise ValueError(f"Cloze gap {self.gap_id!r} requires at least two options.")
        option_ids = tuple(option.option_id for option in self.options)
        if len(option_ids) != len(set(option_id.casefold() for option_id in option_ids)):
            raise ValueError(f"Cloze gap {self.gap_id!r} has duplicate option IDs.")
        if self.correct_option_id not in option_ids:
            raise ValueError(
                f"Cloze gap {self.gap_id!r} references unknown correct option ID "
                f"{self.correct_option_id!r}."
            )
        for locale in AppLocale:
            texts = tuple(
                option.text.for_locale(locale).strip().casefold() for option in self.options
            )
            if len(texts) != len(set(texts)):
                raise ValueError(
                    f"Cloze gap {self.gap_id!r} has duplicate option text for "
                    f"locale {locale.value!r}."
                )

    def materialize(self, locale: AppLocale) -> ClozeGap:
        return ClozeGap(
            gap_id=self.gap_id,
            options=tuple(
                AssessmentOption(option.option_id, option.text.for_locale(locale))
                for option in self.options
            ),
            correct_option_id=self.correct_option_id,
        )


@dataclass(frozen=True, slots=True)
class LocalizedAssessmentItem:
    """An assessment item whose grading remains stable across translations."""

    item_id: str
    activity_type: ActivityType
    prompt: LocalizedText
    options: tuple[LocalizedAssessmentOption, ...]
    correct_option_ids: tuple[str, ...]
    accepted_answers: tuple[LocalizedText, ...]
    explanation: LocalizedText
    rubric: tuple[LocalizedText, ...] = ()
    cloze_gaps: tuple[LocalizedClozeGap, ...] = ()

    def __post_init__(self) -> None:
        if not self.item_id.strip():
            raise ValueError("Assessment item IDs cannot be empty.")
        if self.item_id != self.item_id.strip():
            raise ValueError("Assessment item IDs cannot contain surrounding whitespace.")

        option_ids = tuple(option.option_id for option in self.options)
        normalized_ids = tuple(option_id.casefold() for option_id in option_ids)
        if len(normalized_ids) != len(set(normalized_ids)):
            raise ValueError(f"Assessment item {self.item_id!r} has duplicate option IDs.")

        for locale in AppLocale:
            localized_texts = tuple(
                option.text.for_locale(locale).strip().casefold() for option in self.options
            )
            if len(localized_texts) != len(set(localized_texts)):
                raise ValueError(
                    f"Assessment item {self.item_id!r} has duplicate option text for "
                    f"locale {locale.value!r}."
                )

        is_cloze = self.activity_type is ActivityType.CLOZE_CHOICE
        if is_cloze:
            if not self.cloze_gaps:
                raise ValueError(f"Cloze item {self.item_id!r} requires at least one gap.")
            if self.options or self.correct_option_ids or self.accepted_answers:
                raise ValueError(f"Cloze item {self.item_id!r} must keep answers inside its gaps.")
            gap_ids = tuple(gap.gap_id for gap in self.cloze_gaps)
            if len(gap_ids) != len(set(gap_id.casefold() for gap_id in gap_ids)):
                raise ValueError(f"Cloze item {self.item_id!r} has duplicate gap IDs.")
            for locale in AppLocale:
                localized_prompt = self.prompt.for_locale(locale)
                missing = tuple(
                    gap_id for gap_id in gap_ids if "{" + gap_id + "}" not in localized_prompt
                )
                if missing:
                    raise ValueError(
                        f"Cloze item {self.item_id!r} is missing prompt markers for "
                        f"locale {locale.value!r}: {list(missing)}"
                    )
            return

        if self.cloze_gaps:
            raise ValueError(
                f"Assessment item {self.item_id!r} cannot define cloze gaps for "
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

        if is_option_based:
            if not self.options:
                raise ValueError(f"Assessment item {self.item_id!r} requires options.")
            if not self.correct_option_ids:
                raise ValueError(f"Assessment item {self.item_id!r} requires correct option IDs.")
            if self.accepted_answers:
                raise ValueError(
                    f"Assessment item {self.item_id!r} cannot mix option IDs "
                    "with accepted free-text answers."
                )
        else:
            if self.correct_option_ids:
                raise ValueError(
                    f"Assessment item {self.item_id!r} cannot use option IDs "
                    "for a non-option activity."
                )
            if not self.accepted_answers:
                raise ValueError(f"Assessment item {self.item_id!r} requires accepted answers.")

        invalid_ids = set(self.correct_option_ids) - set(option_ids)
        if invalid_ids:
            raise ValueError(
                f"Assessment item {self.item_id!r} references unknown option IDs: "
                f"{sorted(invalid_ids)}"
            )

        if (
            self.activity_type in {ActivityType.MULTIPLE_CHOICE, ActivityType.TRUE_FALSE}
            and len(self.correct_option_ids) != 1
        ):
            raise ValueError(f"Assessment item {self.item_id!r} requires one correct option.")

    def materialize(self, locale: AppLocale) -> AssessmentItem:
        option_text_by_id = {
            option.option_id: option.text.for_locale(locale) for option in self.options
        }
        correct_answers = (
            tuple(option_text_by_id[option_id] for option_id in self.correct_option_ids)
            if self.correct_option_ids
            else tuple(answer.for_locale(locale) for answer in self.accepted_answers)
        )
        return AssessmentItem(
            item_id=self.item_id,
            activity_type=self.activity_type,
            prompt=self.prompt.for_locale(locale),
            options=tuple(option.text.for_locale(locale) for option in self.options),
            correct_answers=correct_answers,
            explanation=self.explanation.for_locale(locale),
            rubric=tuple(criterion.for_locale(locale) for criterion in self.rubric),
            option_ids=tuple(option.option_id for option in self.options),
            correct_option_ids=self.correct_option_ids,
            cloze_gaps=tuple(gap.materialize(locale) for gap in self.cloze_gaps),
        )


@dataclass(frozen=True, slots=True)
class LocalizedTutorSupportPacket:
    """Complete trilingual subject-matter support for the local tutor."""

    canonical_explanation: LocalizedText
    knowledge_fragments: tuple[LocalizedText, ...]
    common_misconceptions: tuple[LocalizedText, ...]
    socratic_questions: tuple[LocalizedText, ...]
    grading_criteria: tuple[LocalizedText, ...]
    response_constraints: tuple[LocalizedText, ...]
    source_basis: tuple[str, ...]

    def __post_init__(self) -> None:
        required = {
            "knowledge_fragments": self.knowledge_fragments,
            "common_misconceptions": self.common_misconceptions,
            "socratic_questions": self.socratic_questions,
            "grading_criteria": self.grading_criteria,
            "response_constraints": self.response_constraints,
            "source_basis": self.source_basis,
        }
        for name, values in required.items():
            if not values:
                raise ValueError(f"Tutor support requires {name}.")

    def materialize(self, locale: AppLocale) -> TutorSupportPacket:
        return TutorSupportPacket(
            canonical_explanation=self.canonical_explanation.for_locale(locale),
            knowledge_fragments=tuple(
                fragment.for_locale(locale) for fragment in self.knowledge_fragments
            ),
            common_misconceptions=tuple(
                misconception.for_locale(locale) for misconception in self.common_misconceptions
            ),
            socratic_questions=tuple(
                question.for_locale(locale) for question in self.socratic_questions
            ),
            grading_criteria=tuple(
                criterion.for_locale(locale) for criterion in self.grading_criteria
            ),
            response_constraints=tuple(
                constraint.for_locale(locale) for constraint in self.response_constraints
            ),
            source_basis=self.source_basis,
        )


@dataclass(frozen=True, slots=True)
class LocalizedLearningModule:
    """A complete module that cannot exist with a missing supported language."""

    course_code: str
    module_id: str
    title: LocalizedText
    summary: LocalizedText
    objectives: tuple[LocalizedLearningObjective, ...]
    concepts: tuple[LocalizedConceptBlock, ...]
    worked_examples: tuple[LocalizedWorkedExample, ...]
    practice_exercises: tuple[LocalizedPracticeExercise, ...]
    assessment_items: tuple[LocalizedAssessmentItem, ...]
    tutor_support: LocalizedTutorSupportPacket

    def __post_init__(self) -> None:
        if not self.course_code.strip():
            raise ValueError("Localized learning modules require a course code.")
        if not self.module_id.strip():
            raise ValueError("Localized learning modules require a module ID.")

        required = {
            "objectives": self.objectives,
            "concepts": self.concepts,
            "worked_examples": self.worked_examples,
            "practice_exercises": self.practice_exercises,
            "assessment_items": self.assessment_items,
        }
        for name, values in required.items():
            if not values:
                raise ValueError(f"Localized learning module {self.module_id!r} requires {name}.")

        self._validate_unique_ids("objective", tuple(item.objective_id for item in self.objectives))
        self._validate_unique_ids("concept", tuple(item.concept_id for item in self.concepts))
        self._validate_unique_ids(
            "worked example", tuple(item.example_id for item in self.worked_examples)
        )
        self._validate_unique_ids(
            "practice exercise", tuple(item.exercise_id for item in self.practice_exercises)
        )
        self._validate_unique_ids(
            "assessment item", tuple(item.item_id for item in self.assessment_items)
        )

    def materialize(self, locale: AppLocale | str) -> LearningModule:
        """Create the existing runtime module in one selected language."""
        resolved = locale if isinstance(locale, AppLocale) else AppLocale.resolve(locale)
        return LearningModule(
            course_code=self.course_code,
            module_id=self.module_id,
            title=self.title.for_locale(resolved),
            summary=self.summary.for_locale(resolved),
            objectives=tuple(item.materialize(resolved) for item in self.objectives),
            concepts=tuple(item.materialize(resolved) for item in self.concepts),
            worked_examples=tuple(item.materialize(resolved) for item in self.worked_examples),
            practice_exercises=tuple(
                item.materialize(resolved) for item in self.practice_exercises
            ),
            assessment_items=tuple(item.materialize(resolved) for item in self.assessment_items),
            tutor_support=self.tutor_support.materialize(resolved),
        )

    @staticmethod
    def _validate_unique_ids(label: str, identifiers: tuple[str, ...]) -> None:
        normalized = tuple(identifier.strip().casefold() for identifier in identifiers)
        if any(not identifier for identifier in normalized):
            raise ValueError(f"A localized {label} ID cannot be empty.")
        if len(normalized) != len(set(normalized)):
            raise ValueError(f"Duplicate localized {label} IDs are not allowed.")
