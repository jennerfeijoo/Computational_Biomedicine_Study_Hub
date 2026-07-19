"""Safe loader for the complete semester-one curriculum."""

from __future__ import annotations

import os
from collections.abc import Mapping, Sequence
from pathlib import Path
from typing import Any, cast

import yaml

from .catalog import AcademicCatalog
from .models import (
    ConceptBlock,
    CourseContent,
    CumulativeAssessment,
    Flashcard,
    GlossaryEntry,
    HiddenTutorSupport,
    LearningObjective,
    LocalizedText,
    ModuleContent,
    ObjectiveQuestion,
    OpenAssessmentItem,
    PracticeExercise,
    WorkedExample,
)


class AcademicContentError(RuntimeError):
    """A traceable content loading failure."""

    def __init__(self, path: Path, message: str) -> None:
        self.path = path
        self.detail = message
        super().__init__(f"{path}: {message}")


def default_content_root() -> Path:
    """Locate the corpus in development and installed distributions."""
    configured = os.environ.get("CB_STUDY_CONTENT_DIR")
    candidates = [
        Path(configured) if configured else None,
        Path(__file__).resolve().parents[1] / "academic_content" / "semester_1",
        Path(__file__).resolve().parents[3] / "academic_content" / "semester_1",
    ]
    for candidate in candidates:
        if candidate is not None and candidate.is_dir():
            return candidate
    attempted = ", ".join(str(path) for path in candidates if path is not None)
    raise FileNotFoundError(f"Semester-one academic content was not found. Tried: {attempted}")


def _mapping(value: object) -> Mapping[str, Any]:
    if not isinstance(value, Mapping):
        return {}
    return cast(Mapping[str, Any], value)


def _items(value: object) -> tuple[Mapping[str, Any], ...]:
    if not isinstance(value, Sequence) or isinstance(value, (str, bytes)):
        return ()
    return tuple(_mapping(item) for item in value if isinstance(item, Mapping))


def _strings(value: object) -> tuple[str, ...]:
    if isinstance(value, str):
        return (value,)
    if not isinstance(value, Sequence):
        return ()
    return tuple(str(item) for item in value if item is not None)


def _first(mapping: Mapping[str, Any], *keys: str) -> object:
    for key in keys:
        if key in mapping:
            return mapping[key]
    return None


def _localized(mapping: Mapping[str, Any], *keys: str) -> LocalizedText:
    return LocalizedText.from_value(_first(mapping, *keys))


def _item_id(raw: Mapping[str, Any], fallback: str) -> str:
    return str(raw.get("id", fallback)).strip()


class SemesterContentLoader:
    """Load and normalize all four courses without importing the UI."""

    def __init__(self, root: Path | None = None) -> None:
        self.root = (root or default_content_root()).resolve()

    def load(self) -> AcademicCatalog:
        course_directories = sorted(
            path
            for path in self.root.iterdir()
            if path.is_dir() and (path / "course.yaml").is_file()
        )
        courses = tuple(self._load_course(path) for path in course_directories)
        return AcademicCatalog(courses)

    def load_yaml(self, path: Path) -> Mapping[str, Any]:
        try:
            text = path.read_text(encoding="utf-8")
        except OSError as error:
            raise AcademicContentError(path, str(error)) from error
        if not text.strip():
            raise AcademicContentError(path, "file is empty")
        try:
            document = yaml.safe_load(text)
        except yaml.YAMLError as error:
            mark = getattr(error, "problem_mark", None)
            location = f"line {mark.line + 1}, column {mark.column + 1}: " if mark else ""
            problem = getattr(error, "problem", None) or str(error)
            raise AcademicContentError(path, f"{location}{problem}") from error
        if not isinstance(document, Mapping):
            raise AcademicContentError(path, "top-level YAML value must be a mapping")
        return cast(Mapping[str, Any], document)

    def _load_course(self, directory: Path) -> CourseContent:
        raw = self.load_yaml(directory / "course.yaml")
        course_id = str(raw.get("course_code", directory.name)).lower()
        metadata = _mapping(raw.get("metadata"))
        identity = _mapping(raw.get("identity"))

        modules = tuple(
            self._load_module(path, course_id)
            for path in sorted((directory / "modules").glob("*.yaml"))
        )
        card_sets = {
            str(document.get("module_id", "")): document
            for path in sorted((directory / "flashcards").glob("*.yaml"))
            for document in (self.load_yaml(path),)
        }
        modules = tuple(
            self._with_flashcards(module, card_sets.get(module.id, {})) for module in modules
        )

        assessment_paths = sorted((directory / "assessments").glob("*.yaml"))
        cumulative = (
            self._load_cumulative(assessment_paths[0], course_id) if assessment_paths else None
        )
        outcomes = tuple(
            self._learning_objective(item, course_id, index)
            for index, item in enumerate(_items(raw.get("official_learning_outcomes")), start=1)
        )
        title = _localized(metadata, "title", "name")
        if not title.translations:
            title = _localized(identity, "title", "name")
        summary = _localized(metadata, "summary", "description", "purpose")
        if not summary.translations:
            summary = LocalizedText.from_value(raw.get("course_purpose"))
        return CourseContent(
            id=course_id,
            title=title,
            summary=summary,
            learning_outcomes=outcomes,
            modules=modules,
            cumulative_assessment=cumulative,
            raw=raw,
        )

    def _load_module(self, path: Path, course_id: str) -> ModuleContent:
        raw = self.load_yaml(path)
        module_id = str(raw.get("module_id", path.stem)).lower()
        metadata = _mapping(raw.get("metadata"))
        objectives = tuple(
            self._learning_objective(item, module_id, index)
            for index, item in enumerate(_items(raw.get("objectives")), start=1)
        )
        concepts = tuple(
            self._concept(item, module_id, index)
            for index, item in enumerate(_items(raw.get("concepts")), start=1)
        )
        worked_examples = tuple(
            self._worked_example(item, module_id, index)
            for index, item in enumerate(_items(raw.get("worked_examples")), start=1)
        )
        practice_items = _items(_first(raw, "practice_exercises", "guided_practice", "practice"))
        objective_items = _items(raw.get("objective_bank")) + _items(
            raw.get("objective_question_bank")
        )
        open_items = (
            _items(raw.get("open_assessment"))
            + _items(raw.get("open_assessment_items"))
            + _items(raw.get("assessment_items"))
        )
        glossary = tuple(
            self._glossary(item, module_id, index)
            for index, item in enumerate(_items(raw.get("glossary")), start=1)
        )
        hidden = _mapping(
            _first(raw, "hidden_tutor_support", "hidden_support", "hidden_guided_support")
        )
        prerequisites = _strings(_first(metadata, "prerequisites", "prerequisite_modules"))
        return ModuleContent(
            id=module_id,
            course_id=course_id,
            title=_localized(metadata, "title", "name"),
            summary=_localized(metadata, "summary", "description"),
            prerequisites=prerequisites,
            objectives=objectives,
            concepts=concepts,
            worked_examples=worked_examples,
            practice=tuple(
                self._practice(item, module_id, index)
                for index, item in enumerate(practice_items, start=1)
            ),
            objective_questions=tuple(
                self._objective_question(item, module_id, index)
                for index, item in enumerate(objective_items, start=1)
            ),
            open_assessments=tuple(
                self._open_assessment(item, module_id, index)
                for index, item in enumerate(open_items, start=1)
            ),
            flashcards=(),
            glossary=glossary,
            hidden_support=HiddenTutorSupport(module_id, hidden),
            raw=raw,
        )

    def _with_flashcards(
        self, module: ModuleContent, card_document: Mapping[str, Any]
    ) -> ModuleContent:
        cards = tuple(
            self._flashcard(item, module.id, index)
            for index, item in enumerate(_items(card_document.get("cards")), start=1)
        )
        return ModuleContent(
            id=module.id,
            course_id=module.course_id,
            title=module.title,
            summary=module.summary,
            prerequisites=module.prerequisites,
            objectives=module.objectives,
            concepts=module.concepts,
            worked_examples=module.worked_examples,
            practice=module.practice,
            objective_questions=module.objective_questions,
            open_assessments=module.open_assessments,
            flashcards=cards,
            glossary=module.glossary,
            hidden_support=module.hidden_support,
            raw=module.raw,
        )

    def _learning_objective(
        self, raw: Mapping[str, Any], owner_id: str, index: int
    ) -> LearningObjective:
        return LearningObjective(
            id=_item_id(raw, f"{owner_id}.o{index:02}"),
            module_id=owner_id,
            raw=raw,
            statement=_localized(raw, "statement", "text", "description"),
            bloom_level=str(raw.get("bloom_level", "")),
        )

    def _concept(self, raw: Mapping[str, Any], module_id: str, index: int) -> ConceptBlock:
        key_points = tuple(
            LocalizedText.from_value(value)
            for value in cast(Sequence[object], raw.get("key_points", ()))
        )
        return ConceptBlock(
            id=_item_id(raw, f"{module_id}.c{index:02}"),
            module_id=module_id,
            raw=raw,
            title=_localized(raw, "title", "name", "term"),
            explanation=_localized(raw, "explanation", "body", "text", "definition", "summary"),
            key_points=key_points,
        )

    def _worked_example(self, raw: Mapping[str, Any], module_id: str, index: int) -> WorkedExample:
        return WorkedExample(
            id=_item_id(raw, f"{module_id}.e{index:02}"),
            module_id=module_id,
            raw=raw,
            title=_localized(raw, "title", "name"),
            prompt=_localized(raw, "prompt", "problem", "scenario"),
            explanation=_localized(raw, "explanation", "solution", "walkthrough", "interpretation"),
        )

    def _practice(self, raw: Mapping[str, Any], module_id: str, index: int) -> PracticeExercise:
        return PracticeExercise(
            id=_item_id(raw, f"{module_id}.p{index:02}"),
            module_id=module_id,
            raw=raw,
            prompt=_localized(raw, "prompt", "task", "question"),
            activity_type=str(raw.get("activity_type", raw.get("type", "practice"))),
            difficulty=str(raw.get("difficulty", "")),
        )

    def _objective_question(
        self, raw: Mapping[str, Any], module_id: str, index: int
    ) -> ObjectiveQuestion:
        correct = raw.get("correct_option_ids", ())
        if not correct and "correct_option_id" in raw:
            correct = (raw["correct_option_id"],)
        return ObjectiveQuestion(
            id=_item_id(raw, f"{module_id}.q{index:02}"),
            module_id=module_id,
            raw=raw,
            prompt=_localized(raw, "prompt", "question", "stem", "template"),
            question_type=str(raw.get("type", raw.get("activity_type", "multiple_choice"))),
            difficulty=str(raw.get("difficulty", "")),
            correct_option_ids=_strings(correct),
        )

    def _open_assessment(
        self, raw: Mapping[str, Any], module_id: str, index: int
    ) -> OpenAssessmentItem:
        return OpenAssessmentItem(
            id=_item_id(raw, f"{module_id}.a{index:02}"),
            module_id=module_id,
            raw=raw,
            prompt=_localized(raw, "prompt", "question", "task"),
            activity_type=str(raw.get("activity_type", raw.get("type", "open_response"))),
            difficulty=str(raw.get("difficulty", "")),
        )

    def _flashcard(self, raw: Mapping[str, Any], module_id: str, index: int) -> Flashcard:
        return Flashcard(
            id=_item_id(raw, f"{module_id}.f{index:02}"),
            module_id=module_id,
            raw=raw,
            front=_localized(raw, "front"),
            back=_localized(raw, "back"),
            card_type=str(raw.get("card_type", raw.get("type", "concept"))),
            mode=str(raw.get("mode", "conceptual")),
            difficulty=str(raw.get("difficulty", "")),
            linked_objectives=_strings(raw.get("linked_objectives", ())),
            linked_concepts=_strings(raw.get("linked_concepts", ())),
        )

    def _glossary(self, raw: Mapping[str, Any], module_id: str, index: int) -> GlossaryEntry:
        return GlossaryEntry(
            id=_item_id(raw, f"{module_id}.term{index:02}"),
            module_id=module_id,
            raw=raw,
            term=_localized(raw, "term", "title", "name"),
            definition=_localized(raw, "definition", "text", "explanation"),
            related_terms=_strings(_first(raw, "related_terms", "related", "see_also")),
        )

    def _load_cumulative(self, path: Path, course_id: str) -> CumulativeAssessment:
        raw = self.load_yaml(path)
        metadata = _mapping(raw.get("metadata"))
        return CumulativeAssessment(
            id=str(raw.get("assessment_id", f"{course_id}.cumulative")),
            course_id=course_id,
            title=_localized(metadata, "title", "name"),
            raw=raw,
        )
