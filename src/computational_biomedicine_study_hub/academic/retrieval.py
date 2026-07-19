"""Deterministic lexical retrieval with strict visible/hidden separation."""

from __future__ import annotations

import math
import re
from collections import Counter
from collections.abc import Iterable, Mapping
from dataclasses import dataclass
from enum import StrEnum

from .catalog import AcademicCatalog
from .localization import localize_value


class FragmentVisibility(StrEnum):
    VISIBLE = "visible"
    HIDDEN_TUTOR = "hidden_tutor"


@dataclass(frozen=True, slots=True)
class AcademicFragment:
    id: str
    source_id: str
    course_id: str
    module_id: str
    kind: str
    locale: str
    text: str
    visibility: FragmentVisibility

    @property
    def source_label(self) -> str:
        module_number = self.module_id.rsplit(".", 1)[-1].upper()
        return f"{self.course_id.upper()} · {module_number} · {self.kind} {self.source_id}"


@dataclass(frozen=True, slots=True)
class RetrievalQuery:
    text: str
    locale: str
    course_id: str | None = None
    module_id: str | None = None
    limit: int = 6
    allow_hidden: bool = False


@dataclass(frozen=True, slots=True)
class RetrievedFragment:
    fragment: AcademicFragment
    score: float


def _tokens(text: str) -> tuple[str, ...]:
    return tuple(re.findall(r"[\w+#.-]+", text.casefold(), flags=re.UNICODE))


def _flatten_text(value: object) -> str:
    if isinstance(value, str):
        return value
    if isinstance(value, Mapping):
        return " ".join(_flatten_text(item) for item in value.values())
    if isinstance(value, list):
        return " ".join(_flatten_text(item) for item in value)
    return ""


def build_fragments(catalog: AcademicCatalog, locale: str) -> tuple[AcademicFragment, ...]:
    fragments: list[AcademicFragment] = []
    for course in catalog.courses:
        for module in course.modules:
            visible_items: Iterable[tuple[str, str, str]] = (
                (
                    concept.qualified_id,
                    "Concept",
                    " ".join(
                        (
                            concept.title.resolve(locale),
                            concept.explanation.resolve(locale),
                            *(point.resolve(locale) for point in concept.key_points),
                        )
                    ),
                )
                for concept in module.concepts
            )
            visible_items = (
                *visible_items,
                *(
                    (
                        example.qualified_id,
                        "Worked example",
                        " ".join(
                            (
                                example.title.resolve(locale),
                                example.prompt.resolve(locale),
                                example.explanation.resolve(locale),
                            )
                        ),
                    )
                    for example in module.worked_examples
                ),
                *(
                    (exercise.qualified_id, "Practice", exercise.prompt.resolve(locale))
                    for exercise in module.practice
                ),
                *(
                    (
                        card.id,
                        "Flashcard",
                        f"{card.front.resolve(locale)} {card.back.resolve(locale)}",
                    )
                    for card in module.flashcards
                ),
                *(
                    (
                        entry.qualified_id,
                        "Glossary",
                        f"{entry.term.resolve(locale)} {entry.definition.resolve(locale)}",
                    )
                    for entry in module.glossary
                ),
            )
            for source_id, kind, text in visible_items:
                clean_text = text.strip()
                if not clean_text:
                    continue
                fragments.append(
                    AcademicFragment(
                        id=f"{source_id}:{locale}:visible",
                        source_id=source_id,
                        course_id=course.id,
                        module_id=module.id,
                        kind=kind,
                        locale=locale,
                        text=clean_text,
                        visibility=FragmentVisibility.VISIBLE,
                    )
                )

            localized_hidden = localize_value(module.hidden_support.raw, locale)
            hidden_text = _flatten_text(localized_hidden).strip()
            if hidden_text:
                fragments.append(
                    AcademicFragment(
                        id=f"{module.id}:hidden:{locale}",
                        source_id=f"{module.id}.hidden",
                        course_id=course.id,
                        module_id=module.id,
                        kind="Tutor support",
                        locale=locale,
                        text=hidden_text,
                        visibility=FragmentVisibility.HIDDEN_TUTOR,
                    )
                )
    return tuple(fragments)


class LexicalRetriever:
    """Small-corpus BM25 retriever with explicit hidden-index authorization."""

    def __init__(self, fragments: Iterable[AcademicFragment]) -> None:
        self._fragments = tuple(fragments)
        self._tokens = tuple(_tokens(fragment.text) for fragment in self._fragments)
        self._document_frequency = Counter(
            token for document in self._tokens for token in set(document)
        )
        self._average_length = (
            sum(len(document) for document in self._tokens) / len(self._tokens)
            if self._tokens
            else 1.0
        )

    @classmethod
    def from_catalog(cls, catalog: AcademicCatalog, locale: str) -> LexicalRetriever:
        return cls(build_fragments(catalog, locale))

    def search(self, query: RetrievalQuery) -> tuple[RetrievedFragment, ...]:
        query_tokens = _tokens(query.text)
        if not query_tokens:
            return ()
        candidates: list[RetrievedFragment] = []
        total_documents = max(1, len(self._fragments))
        for fragment, document in zip(self._fragments, self._tokens, strict=True):
            if query.course_id and fragment.course_id != query.course_id:
                continue
            if query.module_id and fragment.module_id != query.module_id:
                continue
            if fragment.visibility is FragmentVisibility.HIDDEN_TUTOR and not query.allow_hidden:
                continue
            frequencies = Counter(document)
            score = 0.0
            for token in query_tokens:
                frequency = frequencies[token]
                if not frequency:
                    continue
                document_frequency = self._document_frequency[token]
                inverse_frequency = math.log(
                    1 + (total_documents - document_frequency + 0.5) / (document_frequency + 0.5)
                )
                denominator = frequency + 1.5 * (0.25 + 0.75 * len(document) / self._average_length)
                score += inverse_frequency * frequency * 2.5 / denominator
            if score > 0:
                kind_weight = {
                    "Concept": 1.25,
                    "Glossary": 1.15,
                    "Tutor support": 1.1,
                }.get(fragment.kind, 1.0)
                candidates.append(RetrievedFragment(fragment, score * kind_weight))
        candidates.sort(key=lambda item: (-item.score, item.fragment.id))
        return tuple(candidates[: max(1, query.limit)])


__all__ = [
    "AcademicFragment",
    "FragmentVisibility",
    "LexicalRetriever",
    "RetrievalQuery",
    "RetrievedFragment",
    "build_fragments",
]
