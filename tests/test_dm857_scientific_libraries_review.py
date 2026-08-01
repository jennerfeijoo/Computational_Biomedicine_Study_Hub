"""Focused tests for the DM857 M13 book-grounded source review."""

from computational_biomedicine_study_hub.content import dm857
from computational_biomedicine_study_hub.i18n import AppLocale


def _localized_module(locale: AppLocale | str):
    return dm857.LOCALIZED_MODULE_13_SCIENTIFIC_LIBRARIES.materialize(locale)


def test_m13_audit_is_complete_and_names_the_ingestion_gap() -> None:
    audit = next(item for item in dm857.DM857_MODULE_SOURCE_AUDIT if item.module_id == "dm857.m13")

    assert audit.state == "consistent"
    assert "file-to-DataFrame" in audit.finding
    assert "schema" in audit.finding
    assert "tabular-ingestion" in audit.implemented_change


def test_m13_extension_has_stable_ids_in_every_locale() -> None:
    reference = _localized_module(AppLocale.SPANISH_SPAIN)
    reference_ids = (
        tuple(item.objective_id for item in reference.objectives),
        tuple(item.concept_id for item in reference.concepts),
        tuple(item.example_id for item in reference.worked_examples),
        tuple(item.exercise_id for item in reference.practice_exercises),
        tuple(item.item_id for item in reference.assessment_items),
    )

    for locale in AppLocale:
        module = _localized_module(locale)
        assert (
            tuple(item.objective_id for item in module.objectives),
            tuple(item.concept_id for item in module.concepts),
            tuple(item.example_id for item in module.worked_examples),
            tuple(item.exercise_id for item in module.practice_exercises),
            tuple(item.item_id for item in module.assessment_items),
        ) == reference_ids

    assert "m13.bg.o1" in reference_ids[0]
    assert "tabular-ingestion-and-schema-contracts" in reference_ids[1]
    assert "m13.bg.e01" in reference_ids[2]
    assert "m13.bg.p01" in reference_ids[3]
    assert "dm857.m13.book.001" in reference_ids[4]


def test_m13_example_turns_schema_assumptions_into_executable_checks() -> None:
    module = _localized_module(AppLocale.ENGLISH)
    example = next(item for item in module.worked_examples if item.example_id == "m13.bg.e01")

    compile(example.code, "<m13.bg.e01>", "exec")
    assert "StringIO" in example.code
    assert "pd.read_csv" in example.code
    assert "usecols" in example.code
    assert "dtype" in example.code
    assert "is_unique" in example.code
    assert "isna" in example.code
    assert "(2, 2)" in example.expected_output
    assert "27" in example.expected_output


def test_m13_practice_rejects_silent_repairs() -> None:
    module = _localized_module(AppLocale.ENGLISH)
    practice = next(item for item in module.practice_exercises if item.exercise_id == "m13.bg.p01")
    exported = "\n".join(
        (
            practice.prompt,
            *practice.hints,
            practice.solution,
            practice.explanation,
        )
    ).casefold()

    assert "usecols" in exported
    assert "nullable integer" in exported
    assert "duplicate" in exported
    assert "missing" in exported
    assert "do not turn missing values into zero" in exported
    assert "documented scientific rule" in exported


def test_m13_objective_item_rewards_explicit_contract_validation() -> None:
    module = _localized_module(AppLocale.ENGLISH)
    item = next(item for item in module.assessment_items if item.item_id == "dm857.m13.book.001")

    assert item.correct_option_ids == ("explicit_contract",)
    assert set(item.option_ids) == {
        "read_and_trust",
        "explicit_contract",
        "repair_silently",
    }
    assert "explicit contract" in item.explanation.casefold()


def test_m13_exposes_the_named_book_source() -> None:
    module = dm857.LOCALIZED_MODULE_13_SCIENTIFIC_LIBRARIES
    assert "guttag-2021-ch13-15-23" in module.tutor_support.source_basis
