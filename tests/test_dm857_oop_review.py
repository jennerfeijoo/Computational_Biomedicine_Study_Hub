from __future__ import annotations

from computational_biomedicine_study_hub.content import dm857
from computational_biomedicine_study_hub.content.models import LearningModule
from computational_biomedicine_study_hub.i18n import AppLocale

EXPECTED_IDS = (
    "substitution-safe-overrides",
    "m12.bg.e01",
    "m12.bg.p01",
    "dm857.m12.book.001",
)


def _module(locale: AppLocale | str) -> LearningModule:
    localized = next(
        module for module in dm857.LOCALIZED_MODULES if module.module_id == "dm857.m12"
    )
    return localized.materialize(locale)


def _signature(module: LearningModule) -> tuple[tuple[str, ...], ...]:
    return (
        tuple(item.objective_id for item in module.objectives),
        tuple(item.concept_id for item in module.concepts),
        tuple(item.example_id for item in module.worked_examples),
        tuple(item.exercise_id for item in module.practice_exercises),
        tuple(item.item_id for item in module.assessment_items),
    )


def test_oop_extension_is_complete_and_locale_independent() -> None:
    reference = _signature(_module(AppLocale.ENGLISH))
    concept_id, example_id, exercise_id, item_id = EXPECTED_IDS

    for locale in AppLocale:
        module = _module(locale)
        assert _signature(module) == reference
        assert concept_id in {item.concept_id for item in module.concepts}
        assert example_id in {item.example_id for item in module.worked_examples}
        assert exercise_id in {item.exercise_id for item in module.practice_exercises}
        assert item_id in {item.item_id for item in module.assessment_items}
        assert all(document.text.strip() for document in module.tutor_documents())


def test_oop_audit_records_review_and_named_sources() -> None:
    audit = {item.module_id: item for item in dm857.DM857_MODULE_SOURCE_AUDIT}
    item = audit["dm857.m12"]

    assert item.state == "consistent"
    assert set(item.source_ids) == {
        "guttag-2021-ch10-12",
        "downey-2024-files-oop",
    }
    assert item.finding
    assert item.implemented_change

    source_basis = _module(AppLocale.ENGLISH).tutor_support.source_basis
    assert "guttag-2021-ch10-12" in source_basis
    assert "downey-2024-files-oop" in source_basis


def test_oop_concept_preserves_substitution_contract_boundaries() -> None:
    module = _module(AppLocale.ENGLISH)
    concept = next(
        item for item in module.concepts if item.concept_id == "substitution-safe-overrides"
    )
    text = " ".join((concept.body, *concept.key_points)).casefold()

    assert "subclass" in text
    assert "precondition" in text
    assert "observable" in text
    assert "super()" in text
    assert "shared client suite" in text
    assert "composition" in text


def test_oop_override_example_executes_deterministically(capsys) -> None:
    module = _module(AppLocale.ENGLISH)
    worked_example = next(
        item for item in module.worked_examples if item.example_id == "m12.bg.e01"
    )

    exec(compile(worked_example.code, worked_example.example_id, "exec"), {})

    assert capsys.readouterr().out.rstrip("\n") == "2.0\nA:2.0\ncontract violation"
