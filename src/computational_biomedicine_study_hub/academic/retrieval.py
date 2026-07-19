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
    expansion_terms: tuple[str, ...] = ()

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


def _text_leaves(value: object, path: tuple[str, ...] = ()) -> Iterable[tuple[str, str]]:
    if isinstance(value, str) and value.strip():
        yield (".".join(path) or "support", value.strip())
    elif isinstance(value, Mapping):
        for key, item in value.items():
            yield from _text_leaves(item, (*path, str(key)))
    elif isinstance(value, list):
        for index, item in enumerate(value, start=1):
            yield from _text_leaves(item, (*path, str(index)))


def _safe_path(value: str) -> str:
    return re.sub(r"[^a-z0-9_.-]+", "-", value.casefold()).strip(".-") or "support"


def build_fragments(catalog: AcademicCatalog, locale: str) -> tuple[AcademicFragment, ...]:
    fragments: list[AcademicFragment] = []

    def append(
        *,
        source_id: str,
        course_id: str,
        module_id: str,
        kind: str,
        text: str,
        visibility: FragmentVisibility = FragmentVisibility.VISIBLE,
        expansion_terms: tuple[str, ...] = (),
    ) -> None:
        clean_text = text.strip()
        if not clean_text:
            return
        fragments.append(
            AcademicFragment(
                id=f"{source_id}:{locale}:{visibility.value}",
                source_id=source_id,
                course_id=course_id,
                module_id=module_id,
                kind=kind,
                locale=locale,
                text=clean_text,
                visibility=visibility,
                expansion_terms=expansion_terms,
            )
        )

    for course in catalog.courses:
        for module in course.modules:
            for concept in module.concepts:
                append(
                    source_id=concept.qualified_id,
                    course_id=course.id,
                    module_id=module.id,
                    kind="Concept",
                    text=f"{concept.title.resolve(locale)} {concept.explanation.resolve(locale)}",
                )
                for index, point in enumerate(concept.key_points, start=1):
                    append(
                        source_id=f"{concept.qualified_id}.key_point.{index}",
                        course_id=course.id,
                        module_id=module.id,
                        kind="Key point",
                        text=point.resolve(locale),
                    )
            for example in module.worked_examples:
                append(
                    source_id=f"{example.qualified_id}.prompt",
                    course_id=course.id,
                    module_id=module.id,
                    kind="Worked example",
                    text=f"{example.title.resolve(locale)} {example.prompt.resolve(locale)}",
                )
                append(
                    source_id=f"{example.qualified_id}.explanation",
                    course_id=course.id,
                    module_id=module.id,
                    kind="Example explanation",
                    text=example.explanation.resolve(locale),
                )
            for exercise in module.practice:
                append(
                    source_id=exercise.qualified_id,
                    course_id=course.id,
                    module_id=module.id,
                    kind="Practice",
                    text=exercise.prompt.resolve(locale),
                )
            for objective_question in module.objective_questions:
                append(
                    source_id=objective_question.qualified_id,
                    course_id=course.id,
                    module_id=module.id,
                    kind="Objective question",
                    text=objective_question.prompt.resolve(locale),
                )
            for open_question in module.open_assessments:
                append(
                    source_id=open_question.qualified_id,
                    course_id=course.id,
                    module_id=module.id,
                    kind="Open question",
                    text=open_question.prompt.resolve(locale),
                )
            for card in module.flashcards:
                append(
                    source_id=card.id,
                    course_id=course.id,
                    module_id=module.id,
                    kind="Flashcard",
                    text=f"{card.front.resolve(locale)} {card.back.resolve(locale)}",
                )
            for entry in module.glossary:
                term = entry.term.resolve(locale)
                append(
                    source_id=entry.qualified_id,
                    course_id=course.id,
                    module_id=module.id,
                    kind="Glossary",
                    text=f"{term} {entry.definition.resolve(locale)}",
                    expansion_terms=tuple(
                        dict.fromkeys(
                            (
                                *_tokens(term),
                                *(
                                    token
                                    for related in entry.related_terms
                                    for token in _tokens(related)
                                ),
                            )
                        )
                    ),
                )

            localized_hidden = localize_value(module.hidden_support.raw, locale)
            for path, hidden_text in _text_leaves(localized_hidden):
                source_id = f"{module.id}.hidden.{_safe_path(path)}"
                append(
                    source_id=source_id,
                    course_id=course.id,
                    module_id=module.id,
                    kind="Tutor support",
                    text=hidden_text,
                    visibility=FragmentVisibility.HIDDEN_TUTOR,
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
        expanded_tokens = list(query_tokens)
        query_token_set = set(query_tokens)
        for fragment in self._fragments:
            if fragment.kind == "Glossary" and query_token_set.intersection(
                fragment.expansion_terms
            ):
                expanded_tokens.extend(_tokens(fragment.text)[:24])
        query_tokens = tuple(dict.fromkeys(expanded_tokens))
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
