"""Regression tests for the DM857 book-grounded audit and extensions."""

from computational_biomedicine_study_hub.content import dm857

_EXPECTED_MODULE_IDS = {f"dm857.m{index:02d}" for index in range(1, 15)}
_REVIEWED_MODULE_IDS = {
    "dm857.m01",
    "dm857.m02",
    "dm857.m03",
    "dm857.m04",
    "dm857.m05",
    "dm857.m06",
    "dm857.m07",
    "dm857.m08",
    "dm857.m09",
    "dm857.m14",
}


def _run_example(module_id: str, example_id: str) -> None:
    localized_module = next(
        module for module in dm857.LOCALIZED_MODULES if module.module_id == module_id
    )
    module = localized_module.materialize("en")
    worked_example = next(item for item in module.worked_examples if item.example_id == example_id)
    exec(compile(worked_example.code, example_id, "exec"), {})


def test_dm857_source_audit_maps_every_module_once() -> None:
    audited_ids = tuple(item.module_id for item in dm857.DM857_MODULE_SOURCE_AUDIT)
    assert len(audited_ids) == 14
    assert len(set(audited_ids)) == 14
    assert set(audited_ids) == _EXPECTED_MODULE_IDS


def test_dm857_source_catalog_has_unique_stable_ids() -> None:
    source_ids = tuple(source.source_id for source in dm857.DM857_BOOK_SOURCES)
    assert len(source_ids) == len(set(source_ids))
    assert "guttag-2021-ch04" in source_ids
    assert "downey-2024-testing" in source_ids


def test_reviewed_modules_are_explicit_and_unreviewed_modules_remain_pending() -> None:
    state_by_module = {item.module_id: item.state for item in dm857.DM857_MODULE_SOURCE_AUDIT}
    assert {
        module_id for module_id, state in state_by_module.items() if state == "consistent"
    } == _REVIEWED_MODULE_IDS
    assert {
        module_id for module_id, state in state_by_module.items() if state == "pending"
    } == _EXPECTED_MODULE_IDS - _REVIEWED_MODULE_IDS


def test_book_grounded_extensions_are_complete_in_every_locale() -> None:
    module_by_id = {module.module_id: module for module in dm857.LOCALIZED_MODULES}

    for locale in ("es-ES", "en", "da-DK"):
        functions = module_by_id["dm857.m04"].materialize(locale)
        strings = module_by_id["dm857.m05"].materialize(locale)
        mappings = module_by_id["dm857.m07"].materialize(locale)
        files = module_by_id["dm857.m08"].materialize(locale)

        assert "mutable-default-arguments" in {item.concept_id for item in functions.concepts}
        assert "m04.bg.e01" in {item.example_id for item in functions.worked_examples}
        assert "m04.bg.p01" in {item.exercise_id for item in functions.practice_exercises}
        assert "dm857.m04.book.001" in {item.item_id for item in functions.assessment_items}

        assert "regex-validation-boundaries" in {item.concept_id for item in strings.concepts}
        assert "m05.bg.e01" in {item.example_id for item in strings.worked_examples}
        assert "m05.bg.p01" in {item.exercise_id for item in strings.practice_exercises}
        assert "dm857.m05.book.001" in {item.item_id for item in strings.assessment_items}

        assert "hash-tables-collisions-and-cost" in {item.concept_id for item in mappings.concepts}
        assert "m07.bg.e01" in {item.example_id for item in mappings.worked_examples}
        assert "m07.bg.p01" in {item.exercise_id for item in mappings.practice_exercises}
        assert "dm857.m07.book.001" in {item.item_id for item in mappings.assessment_items}

        assert "exceptions-versus-assertions" in {item.concept_id for item in files.concepts}
        assert "m08.bg.e01" in {item.example_id for item in files.worked_examples}
        assert "m08.bg.p01" in {item.exercise_id for item in files.practice_exercises}
        assert "dm857.m08.book.001" in {item.item_id for item in files.assessment_items}


def test_reviewed_modules_expose_named_source_basis() -> None:
    module_by_id = {module.module_id: module for module in dm857.LOCALIZED_MODULES}

    assert "guttag-2021-ch04" in module_by_id["dm857.m04"].tutor_support.source_basis
    assert "downey-2024-strings-collections" in module_by_id["dm857.m05"].tutor_support.source_basis
    assert "guttag-2021-ch05" in module_by_id["dm857.m06"].tutor_support.source_basis
    assert "guttag-2021-ch10-12" in module_by_id["dm857.m07"].tutor_support.source_basis
    assert "guttag-2021-ch07-09" in module_by_id["dm857.m08"].tutor_support.source_basis
    assert "guttag-2021-ch06" in module_by_id["dm857.m09"].tutor_support.source_basis
    assert "downey-2024-testing" in module_by_id["dm857.m14"].tutor_support.source_basis


def test_new_examples_execute_deterministically(capsys) -> None:
    _run_example("dm857.m04", "m04.bg.e01")
    assert capsys.readouterr().out.rstrip("\n") == "['rna']\n['protein']"

    _run_example("dm857.m05", "m05.bg.e01")
    assert capsys.readouterr().out.rstrip("\n") == "True\nFalse\nFalse"

    _run_example("dm857.m07", "m07.bg.e01")
    assert capsys.readouterr().out.rstrip("\n") == "{1: [11, 16, 21]}"

    _run_example("dm857.m08", "m08.bg.e01")
    assert capsys.readouterr().out.rstrip("\n") == "0.125"
