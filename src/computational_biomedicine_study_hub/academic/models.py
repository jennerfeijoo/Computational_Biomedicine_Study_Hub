"""Immutable academic domain models.

The YAML corpus has several historical key variants.  These models expose one
stable runtime contract while retaining the source mapping for traceability.
They deliberately contain no Qt types.
"""

from __future__ import annotations

from collections.abc import Mapping
from dataclasses import dataclass, field
from typing import Any

SUPPORTED_LOCALES = ("es", "en", "da")


@dataclass(frozen=True, slots=True)
class LocalizedText:
    translations: Mapping[str, str]

    @classmethod
    def from_value(cls, value: object) -> LocalizedText:
        if isinstance(value, Mapping):
            translations = {
                locale: str(value[locale]).strip()
                for locale in SUPPORTED_LOCALES
                if locale in value and str(value[locale]).strip()
            }
            return cls(translations)
        if value is None:
            return cls({})
        text = str(value).strip()
        return cls({"en": text} if text else {})

    def resolve(self, locale: str, *, fallback: str = "en") -> str:
        """Resolve by locale, then English, then the first available value."""
        if locale in self.translations:
            return self.translations[locale]
        if fallback in self.translations:
            return self.translations[fallback]
        return next(iter(self.translations.values()), "")

    @property
    def complete(self) -> bool:
        return all(self.translations.get(locale, "").strip() for locale in SUPPORTED_LOCALES)


@dataclass(frozen=True, slots=True)
class AcademicItem:
    id: str
    module_id: str
    raw: Mapping[str, Any] = field(repr=False)

    @property
    def qualified_id(self) -> str:
        """Return an unambiguous runtime identity without changing the source ID."""
        course_id = self.module_id.split(".", 1)[0]
        if self.id.startswith(f"{course_id}."):
            return self.id
        if self.id.startswith("m") and "." in self.id:
            return f"{course_id}.{self.id}"
        return f"{self.module_id}.{self.id}"


@dataclass(frozen=True, slots=True)
class LearningObjective(AcademicItem):
    statement: LocalizedText
    bloom_level: str = ""


@dataclass(frozen=True, slots=True)
class ConceptBlock(AcademicItem):
    title: LocalizedText
    explanation: LocalizedText
    key_points: tuple[LocalizedText, ...] = ()


@dataclass(frozen=True, slots=True)
class WorkedExample(AcademicItem):
    title: LocalizedText
    prompt: LocalizedText
    explanation: LocalizedText


@dataclass(frozen=True, slots=True)
class PracticeExercise(AcademicItem):
    prompt: LocalizedText
    activity_type: str
    difficulty: str


@dataclass(frozen=True, slots=True)
class ObjectiveQuestion(AcademicItem):
    prompt: LocalizedText
    question_type: str
    difficulty: str
    correct_option_ids: tuple[str, ...]


@dataclass(frozen=True, slots=True)
class OpenAssessmentItem(AcademicItem):
    prompt: LocalizedText
    activity_type: str
    difficulty: str


@dataclass(frozen=True, slots=True)
class Flashcard(AcademicItem):
    front: LocalizedText
    back: LocalizedText
    card_type: str
    mode: str
    difficulty: str
    linked_objectives: tuple[str, ...]
    linked_concepts: tuple[str, ...]


@dataclass(frozen=True, slots=True)
class GlossaryEntry(AcademicItem):
    term: LocalizedText
    definition: LocalizedText
    related_terms: tuple[str, ...]


@dataclass(frozen=True, slots=True)
class HiddenTutorSupport:
    module_id: str
    raw: Mapping[str, Any] = field(repr=False)


@dataclass(frozen=True, slots=True)
class CumulativeAssessment:
    id: str
    course_id: str
    title: LocalizedText
    raw: Mapping[str, Any] = field(repr=False)


@dataclass(frozen=True, slots=True)
class ModuleContent:
    id: str
    course_id: str
    title: LocalizedText
    summary: LocalizedText
    prerequisites: tuple[str, ...]
    objectives: tuple[LearningObjective, ...]
    concepts: tuple[ConceptBlock, ...]
    worked_examples: tuple[WorkedExample, ...]
    practice: tuple[PracticeExercise, ...]
    objective_questions: tuple[ObjectiveQuestion, ...]
    open_assessments: tuple[OpenAssessmentItem, ...]
    flashcards: tuple[Flashcard, ...]
    glossary: tuple[GlossaryEntry, ...]
    hidden_support: HiddenTutorSupport
    raw: Mapping[str, Any] = field(repr=False)


@dataclass(frozen=True, slots=True)
class CourseContent:
    id: str
    title: LocalizedText
    summary: LocalizedText
    learning_outcomes: tuple[LearningObjective, ...]
    modules: tuple[ModuleContent, ...]
    cumulative_assessment: CumulativeAssessment | None
    raw: Mapping[str, Any] = field(repr=False)
