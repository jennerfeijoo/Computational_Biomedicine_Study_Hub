"""Model-backed catalog consumed by cross-course learning pages."""

from __future__ import annotations

from dataclasses import dataclass

from ..content.bundles import LocalizedModuleBundle, ModuleBundle
from ..content.dm857 import LOCALIZED_BUNDLES
from ..content.models import AssessmentItem, LearningModule
from ..i18n import DEFAULT_LOCALE, AppLocale


@dataclass(frozen=True, slots=True)
class CatalogModule:
    """One materialized module plus its versioned assessment bank."""

    course_code: str
    module_id: str
    title: str
    bundle: ModuleBundle

    @property
    def module(self) -> LearningModule:
        return self.bundle.module


@dataclass(frozen=True, slots=True)
class StudyFlashcard:
    """A compact original card derived from authored module content."""

    card_id: str
    course_code: str
    module_id: str
    concept_id: str
    front: str
    back: str
    tags: tuple[str, ...]


@dataclass(frozen=True, slots=True)
class GlossaryEntry:
    """One searchable term derived directly from a concept model."""

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
    """Locale-specific, widget-independent view over registered academic bundles."""

    def __init__(
        self,
        *,
        locale: AppLocale = DEFAULT_LOCALE,
        bundle_catalogs: tuple[tuple[LocalizedModuleBundle, ...], ...] = (LOCALIZED_BUNDLES,),
    ) -> None:
        self.locale = locale
        self._modules = tuple(
            CatalogModule(
                course_code=bundle.localized_module.course_code,
                module_id=bundle.localized_module.module_id,
                title=bundle.localized_module.title.for_locale(locale),
                bundle=bundle.materialize(locale),
            )
            for catalog in bundle_catalogs
            for bundle in catalog
        )
        identities = tuple((module.course_code, module.module_id) for module in self._modules)
        if len(identities) != len(set(identities)):
            raise ValueError("Academic catalog contains duplicate course/module identities.")

    @property
    def course_codes(self) -> tuple[str, ...]:
        """Return only courses that currently have academic bundles."""
        return tuple(dict.fromkeys(module.course_code for module in self._modules))

    def modules(self, course_code: str | None = None) -> tuple[CatalogModule, ...]:
        """Return modules in authored catalog order."""
        if course_code is None:
            return self._modules
        return tuple(module for module in self._modules if module.course_code == course_code)

    def module(self, course_code: str, module_id: str) -> CatalogModule:
        """Resolve one module by stable, language-independent identity."""
        for module in self._modules:
            if module.course_code == course_code and module.module_id == module_id:
                return module
        raise KeyError((course_code, module_id))

    def assessment_items(
        self,
        *,
        course_code: str | None = None,
        module_id: str | None = None,
        objective_bank: bool = False,
    ) -> tuple[AssessmentItem, ...]:
        """Return authored assessment items without reading any widget tree."""
        selected = self.modules(course_code)
        if module_id is not None:
            selected = tuple(module for module in selected if module.module_id == module_id)
        if objective_bank:
            return tuple(
                item for module in selected for item in module.bundle.objective_question_bank
            )
        return tuple(item for module in selected for item in module.module.assessment_items)

    def flashcards(
        self,
        *,
        course_code: str | None = None,
        module_id: str | None = None,
    ) -> tuple[StudyFlashcard, ...]:
        """Derive concise cards from concepts, key points, and misconceptions."""
        cards: list[StudyFlashcard] = []
        for record in self.modules(course_code):
            if module_id is not None and record.module_id != module_id:
                continue
            module = record.module
            for concept in module.concepts:
                tags = self._tags(concept.concept_id)
                cards.append(
                    StudyFlashcard(
                        card_id=f"{record.module_id}.concept.{concept.concept_id}",
                        course_code=record.course_code,
                        module_id=record.module_id,
                        concept_id=concept.concept_id,
                        front=concept.title,
                        back=concept.body + "\n\n• " + "\n• ".join(concept.key_points),
                        tags=tags,
                    )
                )
                for index, point in enumerate(concept.key_points, start=1):
                    cards.append(
                        StudyFlashcard(
                            card_id=(
                                f"{record.module_id}.concept.{concept.concept_id}.key-point.{index}"
                            ),
                            course_code=record.course_code,
                            module_id=record.module_id,
                            concept_id=concept.concept_id,
                            front=f"{concept.title} · {index}",
                            back=point,
                            tags=tags + ("key-point",),
                        )
                    )
            for index, misconception in enumerate(
                module.tutor_support.common_misconceptions,
                start=1,
            ):
                cards.append(
                    StudyFlashcard(
                        card_id=f"{record.module_id}.misconception.{index}",
                        course_code=record.course_code,
                        module_id=record.module_id,
                        concept_id="",
                        front=misconception,
                        back=module.tutor_support.canonical_explanation,
                        tags=("misconception",),
                    )
                )
        return tuple(cards)

    def glossary(
        self,
        *,
        course_code: str | None = None,
    ) -> tuple[GlossaryEntry, ...]:
        """Aggregate concept terms with source, related terms, and synonyms."""
        entries: list[GlossaryEntry] = []
        for record in self.modules(course_code):
            concepts = record.module.concepts
            titles = tuple(concept.title for concept in concepts)
            for index, concept in enumerate(concepts):
                identifier_words = concept.concept_id.replace("-", " ")
                synonyms = (
                    ()
                    if identifier_words.casefold() == concept.title.casefold()
                    else (identifier_words,)
                )
                related = tuple(
                    title for related_index, title in enumerate(titles) if related_index != index
                )[:3]
                entries.append(
                    GlossaryEntry(
                        term_id=f"{record.module_id}.term.{concept.concept_id}",
                        term=concept.title,
                        definition=concept.body,
                        course_code=record.course_code,
                        module_id=record.module_id,
                        module_title=record.title,
                        locale=self.locale,
                        tags=self._tags(concept.concept_id),
                        related_terms=related,
                        synonyms=synonyms,
                    )
                )
        return tuple(sorted(entries, key=lambda entry: entry.term.casefold()))

    @staticmethod
    def _tags(identifier: str) -> tuple[str, ...]:
        return tuple(part for part in identifier.split("-") if len(part) > 2)


__all__ = [
    "AcademicCatalog",
    "CatalogModule",
    "GlossaryEntry",
    "StudyFlashcard",
]
