"""Deterministic validation for the semester-one academic corpus."""

from __future__ import annotations

import re
from collections import Counter
from collections.abc import Iterable, Mapping, Sequence
from dataclasses import dataclass
from difflib import SequenceMatcher
from enum import StrEnum
from pathlib import Path
from typing import Any, cast

import yaml

from .catalog import AcademicCatalog
from .models import SUPPORTED_LOCALES, LocalizedText, ModuleContent

EXPECTED_COURSES = ("bmb830", "bmb831", "dm847", "dm857")
EXPECTED_MODULES = 54
EXPECTED_CARDS = {
    "bmb830": 246,
    "bmb831": 300,
    "dm847": 372,
    "dm857": 426,
}


class Severity(StrEnum):
    BLOCKER = "blocker"
    ERROR = "error"
    WARNING = "warning"


@dataclass(frozen=True, slots=True)
class ContentIssue:
    severity: Severity
    code: str
    message: str
    path: str = ""
    entity_id: str = ""


@dataclass(frozen=True, slots=True)
class ValidationReport:
    issues: tuple[ContentIssue, ...]

    @property
    def blockers(self) -> tuple[ContentIssue, ...]:
        return tuple(issue for issue in self.issues if issue.severity is Severity.BLOCKER)

    @property
    def errors(self) -> tuple[ContentIssue, ...]:
        return tuple(issue for issue in self.issues if issue.severity is Severity.ERROR)

    @property
    def warnings(self) -> tuple[ContentIssue, ...]:
        return tuple(issue for issue in self.issues if issue.severity is Severity.WARNING)

    @property
    def is_valid(self) -> bool:
        return not self.blockers and not self.errors


def _issue(
    severity: Severity,
    code: str,
    message: str,
    *,
    path: Path | str = "",
    entity_id: str = "",
) -> ContentIssue:
    return ContentIssue(severity, code, message, str(path), entity_id)


def _normalize_text(value: str) -> str:
    return " ".join(re.findall(r"\w+", value.casefold(), flags=re.UNICODE))


def _qualified_reference(module: ModuleContent, reference: str) -> str:
    if reference.startswith(f"{module.course_id}."):
        return reference
    if re.match(r"^m\d{2}\.", reference):
        return f"{module.course_id}.{reference}"
    return f"{module.id}.{reference}"


def _missing_locales(value: LocalizedText) -> tuple[str, ...]:
    return tuple(
        locale for locale in SUPPORTED_LOCALES if not value.translations.get(locale, "").strip()
    )


def _iter_localized_mappings(
    value: object, path: str = "$"
) -> Iterable[tuple[str, Mapping[str, Any]]]:
    if isinstance(value, Mapping):
        mapping = cast(Mapping[str, Any], value)
        if set(mapping) & set(SUPPORTED_LOCALES):
            yield path, mapping
            return
        for key, item in mapping.items():
            yield from _iter_localized_mappings(item, f"{path}.{key}")
    elif isinstance(value, Sequence) and not isinstance(value, (str, bytes)):
        for index, item in enumerate(value):
            yield from _iter_localized_mappings(item, f"{path}[{index}]")


def _load_document(path: Path, issues: list[ContentIssue]) -> Mapping[str, Any] | None:
    try:
        text = path.read_text(encoding="utf-8")
    except OSError as error:
        issues.append(_issue(Severity.BLOCKER, "file.unreadable", str(error), path=path))
        return None
    if not text.strip():
        issues.append(_issue(Severity.BLOCKER, "file.empty", "YAML file is empty", path=path))
        return None
    try:
        value = yaml.safe_load(text)
    except yaml.YAMLError as error:
        mark = getattr(error, "problem_mark", None)
        location = f"line {mark.line + 1}, column {mark.column + 1}: " if mark else ""
        problem = getattr(error, "problem", None) or str(error)
        issues.append(_issue(Severity.BLOCKER, "yaml.invalid", f"{location}{problem}", path=path))
        return None
    if not isinstance(value, Mapping):
        issues.append(
            _issue(
                Severity.BLOCKER,
                "yaml.root_type",
                "Top-level YAML value must be a mapping",
                path=path,
            )
        )
        return None
    return cast(Mapping[str, Any], value)


def validate_catalog(catalog: AcademicCatalog, root: Path) -> ValidationReport:
    """Validate source documents, normalized models, IDs, and references."""
    issues: list[ContentIssue] = []
    yaml_paths = sorted(root.rglob("*.yaml"))
    documents: dict[Path, Mapping[str, Any]] = {}
    for path in yaml_paths:
        document = _load_document(path, issues)
        if document is not None:
            documents[path] = document

    actual_courses = tuple(sorted(catalog.courses_by_id))
    if actual_courses != EXPECTED_COURSES:
        issues.append(
            _issue(
                Severity.BLOCKER,
                "semester.course_count",
                f"Expected {EXPECTED_COURSES}; found {actual_courses}",
            )
        )
    if catalog.module_count != EXPECTED_MODULES:
        issues.append(
            _issue(
                Severity.BLOCKER,
                "semester.module_count",
                f"Expected {EXPECTED_MODULES} modules; found {catalog.module_count}",
            )
        )

    actual_total = catalog.flashcard_count
    expected_total = sum(EXPECTED_CARDS.values())
    if actual_total != expected_total:
        issues.append(
            _issue(
                Severity.BLOCKER,
                "semester.flashcard_count",
                f"Expected {expected_total} cards; found {actual_total}",
            )
        )

    known_modules = set(catalog.modules_by_id)
    all_card_ids: list[str] = []
    all_source_ids: list[str] = []
    all_qualified_ids: list[str] = []
    for course in catalog.courses:
        course_cards = sum(len(module.flashcards) for module in course.modules)
        expected_course_cards = EXPECTED_CARDS[course.id]
        if course_cards != expected_course_cards:
            issues.append(
                _issue(
                    Severity.BLOCKER,
                    "course.flashcard_count",
                    f"Expected {expected_course_cards} cards; found {course_cards}",
                    entity_id=course.id,
                )
            )
        if course.cumulative_assessment is None:
            issues.append(
                _issue(
                    Severity.BLOCKER,
                    "course.cumulative_missing",
                    "Cumulative assessment file is missing",
                    entity_id=course.id,
                )
            )

        for module in course.modules:
            module_items = tuple(
                item
                for collection in (
                    module.objectives,
                    module.concepts,
                    module.worked_examples,
                    module.practice,
                    module.objective_questions,
                    module.open_assessments,
                    module.glossary,
                )
                for item in collection
            )
            all_source_ids.extend(item.id for item in module_items)
            all_qualified_ids.extend(item.qualified_id for item in module_items)
            _validate_module(module, known_modules, issues)
            all_card_ids.extend(card.id for card in module.flashcards)

    for identity, count in Counter(all_card_ids).items():
        if count > 1:
            issues.append(
                _issue(
                    Severity.BLOCKER,
                    "id.flashcard_duplicate",
                    f"Flashcard ID occurs {count} times",
                    entity_id=identity,
                )
            )
    for identity, count in Counter(all_qualified_ids).items():
        if count > 1:
            issues.append(
                _issue(
                    Severity.ERROR,
                    "id.entity_duplicate",
                    f"Qualified academic ID occurs {count} times",
                    entity_id=identity,
                )
            )
    duplicated_source_ids = {
        identity: count for identity, count in Counter(all_source_ids).items() if count > 1
    }
    if duplicated_source_ids:
        examples = ", ".join(sorted(duplicated_source_ids)[:8])
        issues.append(
            _issue(
                Severity.ERROR,
                "id.source_not_global",
                f"{len(duplicated_source_ids)} source IDs are reused across modules "
                f"(examples: {examples}); runtime qualification is collision-free",
            )
        )

    _validate_documents(documents, root, issues)
    return ValidationReport(tuple(issues))


def _validate_module(
    module: ModuleContent, known_modules: set[str], issues: list[ContentIssue]
) -> None:
    required_collections = {
        "objectives": module.objectives,
        "concepts": module.concepts,
        "worked_examples": module.worked_examples,
        "practice": module.practice,
        "objective_questions": module.objective_questions,
        "open_assessments": module.open_assessments,
        "glossary": module.glossary,
    }
    for name, collection in required_collections.items():
        if not collection:
            issues.append(
                _issue(
                    Severity.ERROR,
                    f"module.{name}_missing",
                    f"Required collection '{name}' is empty",
                    entity_id=module.id,
                )
            )
    if not module.hidden_support.raw:
        issues.append(
            _issue(
                Severity.ERROR,
                "module.hidden_support_missing",
                "Hidden tutor support is empty",
                entity_id=module.id,
            )
        )

    for label, value in (("title", module.title), ("summary", module.summary)):
        missing = _missing_locales(value)
        if missing:
            issues.append(
                _issue(
                    Severity.ERROR,
                    "locale.incomplete",
                    f"{label} is missing locales: {', '.join(missing)}",
                    entity_id=module.id,
                )
            )

    objective_ids = {objective.qualified_id for objective in module.objectives}
    concept_ids = {concept.qualified_id for concept in module.concepts}
    fronts: list[tuple[str, str]] = []
    expected_prefix = f"{module.id}.f"
    for card in module.flashcards:
        if not card.id.startswith(expected_prefix):
            issues.append(
                _issue(
                    Severity.ERROR,
                    "id.flashcard_prefix",
                    f"Expected prefix '{expected_prefix}'",
                    entity_id=card.id,
                )
            )
        for side_name, side in (("front", card.front), ("back", card.back)):
            missing = _missing_locales(side)
            if missing:
                issues.append(
                    _issue(
                        Severity.BLOCKER,
                        "flashcard.locale_incomplete",
                        f"{side_name} is missing locales: {', '.join(missing)}",
                        entity_id=card.id,
                    )
                )
            if not side.resolve("en").strip():
                issues.append(
                    _issue(
                        Severity.BLOCKER,
                        "flashcard.side_empty",
                        f"{side_name} is empty",
                        entity_id=card.id,
                    )
                )
        for reference in card.linked_objectives:
            if _qualified_reference(module, reference) not in objective_ids:
                issues.append(
                    _issue(
                        Severity.ERROR,
                        "reference.objective_missing",
                        f"Linked objective does not exist: {reference}",
                        entity_id=card.id,
                    )
                )
        for reference in card.linked_concepts:
            if _qualified_reference(module, reference) not in concept_ids:
                issues.append(
                    _issue(
                        Severity.WARNING,
                        "reference.concept_missing",
                        f"Linked concept does not exist: {reference}",
                        entity_id=card.id,
                    )
                )
        fronts.append((card.id, _normalize_text(card.front.resolve("en"))))

    for prerequisite in module.prerequisites:
        if re.fullmatch(r"[a-z]+\d+\.m\d{2}", prerequisite) and prerequisite not in known_modules:
            issues.append(
                _issue(
                    Severity.ERROR,
                    "reference.prerequisite_missing",
                    f"Prerequisite module does not exist: {prerequisite}",
                    entity_id=module.id,
                )
            )

    for left_index, (left_id, left_text) in enumerate(fronts):
        if not left_text:
            continue
        for right_id, right_text in fronts[left_index + 1 :]:
            if left_text == right_text:
                issues.append(
                    _issue(
                        Severity.ERROR,
                        "flashcard.duplicate",
                        f"Same English front as {right_id}",
                        entity_id=left_id,
                    )
                )
            elif (
                len(left_text) >= 24
                and SequenceMatcher(None, left_text, right_text).ratio() >= 0.94
            ):
                issues.append(
                    _issue(
                        Severity.WARNING,
                        "flashcard.near_duplicate",
                        f"Near-identical English front to {right_id}",
                        entity_id=left_id,
                    )
                )


def _validate_documents(
    documents: Mapping[Path, Mapping[str, Any]],
    root: Path,
    issues: list[ContentIssue],
) -> None:
    for path, document in documents.items():
        relative = path.relative_to(root)
        parts = relative.parts
        for value_path, mapping in _iter_localized_mappings(document):
            missing = [
                locale for locale in SUPPORTED_LOCALES if not str(mapping.get(locale, "")).strip()
            ]
            if missing:
                issues.append(
                    _issue(
                        Severity.ERROR,
                        "locale.mapping_incomplete",
                        f"{value_path} is missing locales: {', '.join(missing)}",
                        path=relative,
                    )
                )

        if "modules" in parts:
            course_id = parts[0]
            module_id = str(document.get("module_id", ""))
            expected_stem = module_id.replace(".", "_")
            if str(document.get("course_code", "")).lower() != course_id:
                issues.append(
                    _issue(
                        Severity.BLOCKER,
                        "path.course_mismatch",
                        "course_code does not match directory",
                        path=relative,
                        entity_id=module_id,
                    )
                )
            if path.stem != expected_stem:
                issues.append(
                    _issue(
                        Severity.ERROR,
                        "path.module_mismatch",
                        f"Expected filename {expected_stem}.yaml",
                        path=relative,
                        entity_id=module_id,
                    )
                )

        if "flashcards" in parts:
            cards = document.get("cards", ())
            actual = len(cards) if isinstance(cards, Sequence) else 0
            declared = document.get("count", document.get("card_count"))
            if declared != actual:
                issues.append(
                    _issue(
                        Severity.BLOCKER,
                        "flashcard.declared_count",
                        f"Declared {declared}; found {actual}",
                        path=relative,
                    )
                )
            course_id = parts[0]
            module_id = str(document.get("module_id", path.stem.split("_flashcards")[0]))
            if str(document.get("course_code", course_id)).lower() != course_id:
                issues.append(
                    _issue(
                        Severity.BLOCKER,
                        "path.card_course_mismatch",
                        "course_code does not match directory",
                        path=relative,
                    )
                )
            if module_id and not module_id.startswith(f"{course_id}."):
                issues.append(
                    _issue(
                        Severity.ERROR,
                        "path.card_module_mismatch",
                        f"module_id '{module_id}' does not belong to {course_id}",
                        path=relative,
                    )
                )


__all__ = [
    "ContentIssue",
    "EXPECTED_CARDS",
    "EXPECTED_COURSES",
    "EXPECTED_MODULES",
    "Severity",
    "ValidationReport",
    "validate_catalog",
]
