from __future__ import annotations

from contextlib import redirect_stdout
from io import StringIO

from computational_biomedicine_study_hub.content import dm857
from computational_biomedicine_study_hub.i18n import AppLocale

EXPECTED_EXTENSIONS = {
    "dm857.m01": (
        "floating-point-and-rounding-policy",
        "m01.bg.e01",
        "m01.bg.p01",
        "dm857.m01.book.001",
    ),
    "dm857.m02": (
        "branch-ordering-and-shadowing",
        "m02.bg.e01",
        "m02.bg.p01",
        "dm857.m02.book.001",
    ),
    "dm857.m03": (
        "bisection-search-and-tolerance",
        "m03.bg.e01",
        "m03.bg.p01",
        "dm857.m03.book.001",
    ),
}


def _materialized_modules(locale: AppLocale) -> dict[str, object]:
    return {module.module_id: module.materialize(locale) for module in dm857.LOCALIZED_MODULES}


def _identifier_signature(module: object) -> tuple[tuple[str, ...], ...]:
    return (
        tuple(item.objective_id for item in module.objectives),
        tuple(item.concept_id for item in module.concepts),
        tuple(item.example_id for item in module.worked_examples),
        tuple(item.exercise_id for item in module.practice_exercises),
        tuple(item.item_id for item in module.assessment_items),
    )


def test_foundation_modules_are_marked_reviewed_after_the_extensions() -> None:
    audit_by_module = {item.module_id: item for item in dm857.DM857_MODULE_SOURCE_AUDIT}

    for module_id in EXPECTED_EXTENSIONS:
        audit = audit_by_module[module_id]
        assert audit.state == "consistent"
        assert audit.finding
        assert audit.implemented_change
        assert set(audit.source_ids) == {
            "guttag-2021-ch01-03",
            "downey-2024-foundations",
        }


def test_foundation_extensions_are_complete_in_all_locales() -> None:
    for locale in AppLocale:
        modules = _materialized_modules(locale)
        for module_id, expected_ids in EXPECTED_EXTENSIONS.items():
            module = modules[module_id]
            concept_id, example_id, exercise_id, item_id = expected_ids

            assert concept_id in {item.concept_id for item in module.concepts}
            assert example_id in {item.example_id for item in module.worked_examples}
            assert exercise_id in {item.exercise_id for item in module.practice_exercises}
            assert item_id in {item.item_id for item in module.assessment_items}
            assert {
                "guttag-2021-ch01-03",
                "downey-2024-foundations",
            }.issubset(set(module.tutor_support.source_basis))


def test_foundation_extension_ids_are_locale_independent() -> None:
    reference = _materialized_modules(AppLocale.SPANISH_SPAIN)
    reference_signatures = {
        module_id: _identifier_signature(reference[module_id])
        for module_id in EXPECTED_EXTENSIONS
    }

    for locale in AppLocale:
        modules = _materialized_modules(locale)
        assert {
            module_id: _identifier_signature(modules[module_id])
            for module_id in EXPECTED_EXTENSIONS
        } == reference_signatures


def test_foundation_examples_execute_with_the_documented_output() -> None:
    modules = _materialized_modules(AppLocale.ENGLISH)

    for module_id, (_, example_id, _, _) in EXPECTED_EXTENSIONS.items():
        module = modules[module_id]
        worked_example = next(
            item for item in module.worked_examples if item.example_id == example_id
        )
        output = StringIO()
        with redirect_stdout(output):
            exec(compile(worked_example.code, example_id, "exec"), {})

        assert output.getvalue().strip() == worked_example.expected_output.strip()
