"""Locale-specific adapter from the canonical YAML catalog to learning pages."""

from __future__ import annotations

from collections.abc import Mapping, Sequence
from dataclasses import dataclass
from functools import lru_cache
from typing import Any, cast

from ..academic import SemesterContentLoader
from ..academic.catalog import AcademicCatalog as SourceCatalog
from ..academic.localization import localize_value
from ..academic.models import CourseContent, ModuleContent
from ..content.models import (
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
from ..i18n import DEFAULT_LOCALE, AppLocale
from .activity_types import ActivityType


@lru_cache(maxsize=1)
def _load_default_source_catalog() -> SourceCatalog:
    return SemesterContentLoader().load()


def _locale_code(locale: AppLocale) -> str:
    return {
        AppLocale.SPANISH_SPAIN: "es",
        AppLocale.ENGLISH: "en",
        AppLocale.DANISH_DENMARK: "da",
    }[locale]


def _mapping(value: object) -> Mapping[str, Any]:
    return cast(Mapping[str, Any], value) if isinstance(value, Mapping) else {}


def _sequence(value: object) -> tuple[object, ...]:
    if not isinstance(value, Sequence) or isinstance(value, (str, bytes)):
        return ()
    return tuple(value)


def _string_values(value: object, locale: str) -> tuple[str, ...]:
    localized = localize_value(value, locale)
    if isinstance(localized, str):
        return (localized,) if localized.strip() else ()
    if isinstance(localized, Mapping):
        return tuple(
            text
            for item in localized.values()
            for text in _string_values(item, locale)
            if text.strip()
        )
    if isinstance(localized, Sequence):
        return tuple(
            text for item in localized for text in _string_values(item, locale) if text.strip()
        )
    return ()


def _activity_type(value: str, *, objective: bool) -> ActivityType:
    try:
        return ActivityType(value)
    except ValueError:
        normalized = value.casefold()
        if "oral" in normalized:
            return ActivityType.ORAL_EXPLANATION
        if "debug" in normalized or "audit" in normalized:
            return ActivityType.DEBUGGING
        if "data" in normalized or "interpret" in normalized or "output" in normalized:
            return ActivityType.DATA_INTERPRETATION
        if "code" in normalized or "algorithm" in normalized:
            return ActivityType.CODE_TRACING
        if "pipeline" in normalized or "design" in normalized or "architecture" in normalized:
            return ActivityType.PIPELINE_DESIGN
        return ActivityType.MULTIPLE_CHOICE if objective else ActivityType.SHORT_ANSWER


def _option_id(value: object) -> str:
    if isinstance(value, bool):
        return "true" if value else "false"
    return str(value)


def _visible_option(raw: Mapping[str, Any], locale: str) -> AssessmentOption:
    option_id = _option_id(raw.get("id", ""))
    text_value = raw.get("text", raw)
    text = str(localize_value(text_value, locale)).strip()
    return AssessmentOption(option_id=option_id, text=text)


def _objective_item(raw: Mapping[str, Any], locale: str) -> AssessmentItem:
    item_id = str(raw["id"])
    raw_type = str(raw.get("type", raw.get("activity_type", "multiple_choice")))
    activity_type = _activity_type(raw_type, objective=True)
    explanation = str(localize_value(raw.get("explanation", ""), locale)).strip()

    if activity_type is ActivityType.CLOZE_CHOICE:
        prompt = str(localize_value(raw.get("template", raw.get("prompt", "")), locale))
        gaps: list[ClozeGap] = []
        for blank_value in _sequence(raw.get("blanks")):
            blank = _mapping(blank_value)
            options = tuple(
                _visible_option(_mapping(value), locale)
                for value in _sequence(blank.get("options"))
            )
            gap_id = str(blank.get("id", ""))
            gaps.append(
                ClozeGap(
                    gap_id=gap_id,
                    options=options,
                    correct_option_id=_option_id(blank.get("correct_option_id", "")),
                )
            )
            prompt = prompt.replace(f"[[{gap_id}]]", f"{{{gap_id}}}")
        return AssessmentItem(
            item_id=item_id,
            activity_type=activity_type,
            prompt=prompt,
            options=(),
            correct_answers=(),
            explanation=explanation,
            cloze_gaps=tuple(gaps),
        )

    options = tuple(
        _visible_option(_mapping(value), locale) for value in _sequence(raw.get("options"))
    )
    if activity_type is ActivityType.TRUE_FALSE and not options:
        translated = {
            "es": ("Verdadero", "Falso"),
            "en": ("True", "False"),
            "da": ("Sandt", "Falsk"),
        }[locale]
        options = (
            AssessmentOption("true", translated[0]),
            AssessmentOption("false", translated[1]),
        )

    correct_values = _sequence(raw.get("correct_option_ids"))
    if not correct_values:
        if "correct" in raw:
            correct_values = (raw["correct"],)
        elif "correct_answer" in raw:
            correct_values = (raw["correct_answer"],)
    correct_ids = tuple(_option_id(value) for value in correct_values)
    text_by_id = {option.option_id: option.text for option in options}
    correct_answers = tuple(text_by_id[value] for value in correct_ids if value in text_by_id)
    if not explanation:
        explanation = " / ".join(correct_answers)
    return AssessmentItem(
        item_id=item_id,
        activity_type=activity_type,
        prompt=str(localize_value(raw.get("prompt", ""), locale)),
        options=tuple(option.text for option in options),
        correct_answers=correct_answers,
        explanation=explanation,
        option_ids=tuple(option.option_id for option in options),
        correct_option_ids=correct_ids,
    )


def _open_item(raw: Mapping[str, Any], locale: str) -> AssessmentItem:
    activity_type = _activity_type(
        str(raw.get("activity_type", raw.get("type", "short_answer"))),
        objective=False,
    )
    answers = (
        _string_values(raw.get("canonical_answer"), locale)
        or _string_values(raw.get("solution"), locale)
        or _string_values(raw.get("expected_answer"), locale)
        or _string_values(raw.get("accepted_answer_elements"), locale)
        or _string_values(raw.get("expected_elements"), locale)
        or _string_values(raw.get("rubric"), locale)
    )
    if not answers:
        raise ValueError(f"Open assessment {raw.get('id')!r} has no authored answer or rubric.")
    explanation = (
        _string_values(raw.get("explanation"), locale)
        or _string_values(raw.get("feedback"), locale)
        or answers
    )
    rubric = _string_values(raw.get("rubric"), locale)
    return AssessmentItem(
        item_id=str(raw["id"]),
        activity_type=activity_type,
        prompt=str(
            localize_value(raw.get("prompt", raw.get("question", raw.get("task", ""))), locale)
        ),
        options=(),
        correct_answers=answers,
        explanation="\n".join(explanation),
        rubric=rubric,
    )


def _localized_text(raw: Mapping[str, Any], locale: str, *keys: str) -> str:
    for key in keys:
        if key in raw:
            values = _string_values(raw[key], locale)
            if values:
                return "\n".join(values)
    return ""


def _learning_module(
    source: ModuleContent,
    course_code: str,
    locale: str,
    open_items: tuple[AssessmentItem, ...],
) -> LearningModule:
    concepts = tuple(
        ConceptBlock(
            concept_id=concept.qualified_id,
            title=concept.title.resolve(locale),
            body=concept.explanation.resolve(locale),
            key_points=tuple(point.resolve(locale) for point in concept.key_points),
        )
        for concept in source.concepts
    )
    examples = tuple(
        WorkedExample(
            example_id=example.qualified_id,
            title=example.title.resolve(locale) or example.id,
            problem=example.prompt.resolve(locale),
            reasoning=_string_values(example.raw.get("reasoning"), locale),
            code=_localized_text(example.raw, locale, "code", "implementation"),
            expected_output=_localized_text(
                example.raw, locale, "expected_output", "output", "result"
            ),
            explanation=example.explanation.resolve(locale),
        )
        for example in source.worked_examples
    )
    practice = tuple(
        PracticeExercise(
            exercise_id=exercise.qualified_id,
            activity_type=_activity_type(exercise.activity_type, objective=False),
            prompt=exercise.prompt.resolve(locale),
            hints=_string_values(exercise.raw.get("hints"), locale),
            solution=_localized_text(
                exercise.raw,
                locale,
                "solution",
                "canonical_answer",
                "expected_answer",
                "accepted_answer_elements",
                "expected_elements",
            ),
            explanation=_localized_text(exercise.raw, locale, "explanation", "feedback", "rubric"),
            starter_code=_localized_text(exercise.raw, locale, "starter_code"),
        )
        for exercise in source.practice
    )
    hidden_value = localize_value(source.hidden_support.raw, locale)
    hidden = _mapping(hidden_value)
    hidden_flat = _string_values(hidden, locale)
    canonical = _localized_text(
        hidden, locale, "canonical_explanation", "canonical_answer", "explanation"
    )
    return LearningModule(
        course_code=course_code,
        module_id=source.id,
        title=source.title.resolve(locale),
        summary=source.summary.resolve(locale),
        objectives=tuple(
            LearningObjective(
                objective_id=objective.qualified_id,
                statement=objective.statement.resolve(locale),
            )
            for objective in source.objectives
        ),
        concepts=concepts,
        worked_examples=examples,
        practice_exercises=practice,
        assessment_items=open_items,
        tutor_support=TutorSupportPacket(
            canonical_explanation=canonical or "\n".join(hidden_flat),
            knowledge_fragments=_string_values(
                hidden.get("knowledge_fragments", hidden.get("concept_guidance")), locale
            )
            or hidden_flat,
            common_misconceptions=_string_values(
                hidden.get("common_misconceptions", hidden.get("misconceptions")), locale
            ),
            socratic_questions=_string_values(
                hidden.get("socratic_questions", hidden.get("questions")), locale
            ),
            grading_criteria=_string_values(
                hidden.get("grading_criteria", hidden.get("rubric")), locale
            ),
            response_constraints=_string_values(hidden.get("response_constraints"), locale),
            source_basis=_string_values(hidden.get("source_basis"), locale),
        ),
    )


@dataclass(frozen=True, slots=True)
class CatalogModule:
    """One localized module and both assessment categories."""

    course_code: str
    module_id: str
    title: str
    content_version: str
    assessment_items: tuple[AssessmentItem, ...]
    objective_question_bank: tuple[AssessmentItem, ...]
    learning_module: LearningModule
    source: ModuleContent

    @property
    def module(self) -> LearningModule:
        return self.learning_module

    @property
    def bundle(self) -> CatalogModule:
        return self


@dataclass(frozen=True, slots=True)
class StudyFlashcard:
    card_id: str
    course_code: str
    module_id: str
    concept_id: str
    front: str
    back: str
    tags: tuple[str, ...]
    card_type: str = "concept"
    difficulty: str = ""


@dataclass(frozen=True, slots=True)
class GlossaryEntry:
    term_id: str
    term: str
    definition: str
    course_code: str
    module_id: str
    module_title: str
    locale: AppLocale
    tags: tuple[str, ...]
    related_terms: tuple[str, ...]
    synonyms: tuple[str, ...]


class AcademicCatalog:
    """Learning-page view over all canonical YAML content."""

    def __init__(
        self,
        *,
        locale: AppLocale = DEFAULT_LOCALE,
        bundle_catalogs: tuple[object, ...] | None = None,
        source_catalog: SourceCatalog | None = None,
    ) -> None:
        self.locale = locale
        self._locale_code = _locale_code(locale)
        self._modules: tuple[CatalogModule, ...]
        if bundle_catalogs == ():
            self._source_catalog = SourceCatalog(())
            self._modules = ()
            return
        self._source_catalog = source_catalog or _load_default_source_catalog()
        self._modules = tuple(
            self._adapt_module(course.id, module)
            for course in self._source_catalog.courses
            for module in course.modules
        )

    def _adapt_module(self, course_id: str, module: ModuleContent) -> CatalogModule:
        version = str(module.raw.get("content_version", "1"))
        open_items = tuple(
            _open_item(item.raw, self._locale_code) for item in module.open_assessments
        )
        return CatalogModule(
            course_code=course_id.upper(),
            module_id=module.id,
            title=module.title.resolve(self._locale_code),
            content_version=version,
            assessment_items=open_items,
            objective_question_bank=tuple(
                _objective_item(item.raw, self._locale_code) for item in module.objective_questions
            ),
            learning_module=_learning_module(
                module,
                course_id.upper(),
                self._locale_code,
                open_items,
            ),
            source=module,
        )

    @property
    def course_codes(self) -> tuple[str, ...]:
        return tuple(dict.fromkeys(module.course_code for module in self._modules))

    @property
    def source_catalog(self) -> SourceCatalog:
        return self._source_catalog

    def source_course(self, course_code: str) -> CourseContent:
        """Return the typed canonical course for metadata not materialized in widgets."""
        return self._source_catalog.course(course_code.casefold())

    def modules(self, course_code: str | None = None) -> tuple[CatalogModule, ...]:
        if course_code is None:
            return self._modules
        normalized = course_code.upper()
        return tuple(module for module in self._modules if module.course_code == normalized)

    def module(self, course_code: str, module_id: str) -> CatalogModule:
        normalized = course_code.upper()
        for module in self._modules:
            if module.course_code == normalized and module.module_id == module_id:
                return module
        raise KeyError((course_code, module_id))

    def assessment_items(
        self,
        *,
        course_code: str | None = None,
        module_id: str | None = None,
        objective_bank: bool = False,
    ) -> tuple[AssessmentItem, ...]:
        selected = self.modules(course_code)
        if module_id is not None:
            selected = tuple(module for module in selected if module.module_id == module_id)
        if objective_bank:
            return tuple(item for module in selected for item in module.objective_question_bank)
        return tuple(item for module in selected for item in module.assessment_items)

    def flashcards(
        self,
        *,
        course_code: str | None = None,
        module_id: str | None = None,
    ) -> tuple[StudyFlashcard, ...]:
        cards: list[StudyFlashcard] = []
        for record in self.modules(course_code):
            if module_id is not None and record.module_id != module_id:
                continue
            for card in record.source.flashcards:
                cards.append(
                    StudyFlashcard(
                        card_id=card.id,
                        course_code=record.course_code,
                        module_id=record.module_id,
                        concept_id=(card.linked_concepts[0] if card.linked_concepts else ""),
                        front=card.front.resolve(self._locale_code),
                        back=card.back.resolve(self._locale_code),
                        tags=tuple(str(value) for value in _sequence(card.raw.get("tags"))),
                        card_type=card.card_type,
                        difficulty=card.difficulty,
                    )
                )
        return tuple(cards)

    def glossary(self, *, course_code: str | None = None) -> tuple[GlossaryEntry, ...]:
        entries: list[GlossaryEntry] = []
        for record in self.modules(course_code):
            for entry in record.source.glossary:
                term = entry.term.resolve(self._locale_code)
                tags = tuple(part for part in re_split_identifier(entry.id) if len(part) > 2)
                entries.append(
                    GlossaryEntry(
                        term_id=entry.qualified_id,
                        term=term,
                        definition=entry.definition.resolve(self._locale_code),
                        course_code=record.course_code,
                        module_id=record.module_id,
                        module_title=record.title,
                        locale=self.locale,
                        tags=tags,
                        related_terms=entry.related_terms,
                        synonyms=(),
                    )
                )
        return tuple(sorted(entries, key=lambda entry: entry.term.casefold()))


def re_split_identifier(identifier: str) -> tuple[str, ...]:
    return tuple(
        part
        for section in identifier.replace("_", ".").replace("-", ".").split(".")
        for part in (section.strip(),)
        if part
    )


__all__ = ["AcademicCatalog", "CatalogModule", "GlossaryEntry", "StudyFlashcard"]
