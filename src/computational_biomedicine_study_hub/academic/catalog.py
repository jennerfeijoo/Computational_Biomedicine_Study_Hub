"""Indexed semester catalog."""

from __future__ import annotations

from collections.abc import Mapping
from dataclasses import dataclass, field
from types import MappingProxyType

from .models import CourseContent, Flashcard, GlossaryEntry, ModuleContent


@dataclass(frozen=True, slots=True)
class AcademicCatalog:
    courses: tuple[CourseContent, ...]
    courses_by_id: Mapping[str, CourseContent] = field(init=False, repr=False)
    modules_by_id: Mapping[str, ModuleContent] = field(init=False, repr=False)
    flashcards_by_id: Mapping[str, Flashcard] = field(init=False, repr=False)
    glossary_by_id: Mapping[str, GlossaryEntry] = field(init=False, repr=False)

    def __post_init__(self) -> None:
        courses = {course.id: course for course in self.courses}
        modules = {module.id: module for course in self.courses for module in course.modules}
        flashcards = {
            card.id: card
            for course in self.courses
            for module in course.modules
            for card in module.flashcards
        }
        glossary = {
            entry.qualified_id: entry
            for course in self.courses
            for module in course.modules
            for entry in module.glossary
        }
        object.__setattr__(self, "courses_by_id", MappingProxyType(courses))
        object.__setattr__(self, "modules_by_id", MappingProxyType(modules))
        object.__setattr__(self, "flashcards_by_id", MappingProxyType(flashcards))
        object.__setattr__(self, "glossary_by_id", MappingProxyType(glossary))

    @property
    def module_count(self) -> int:
        return len(self.modules_by_id)

    @property
    def flashcard_count(self) -> int:
        return len(self.flashcards_by_id)

    def course(self, course_id: str) -> CourseContent:
        return self.courses_by_id[course_id.lower()]

    def module(self, module_id: str) -> ModuleContent:
        return self.modules_by_id[module_id.lower()]

    def flashcard(self, card_id: str) -> Flashcard:
        return self.flashcards_by_id[card_id.lower()]
