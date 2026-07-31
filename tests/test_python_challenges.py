from __future__ import annotations

from computational_biomedicine_study_hub.content.dm857 import (
    MODULE_07_MAPPINGS_SETS,
    MODULE_09_RECURSION,
)
from computational_biomedicine_study_hub.content.python_challenges import (
    python_challenge_for,
    validate_python_challenge_catalog,
)
from computational_biomedicine_study_hub.i18n import AppLocale
from computational_biomedicine_study_hub.learning.python_challenge import (
    ChallengeCaseStatus,
    PythonChallengeEvaluator,
)


def _unique_count_challenge(locale: AppLocale = AppLocale.ENGLISH):
    challenge = python_challenge_for(
        "m07.p04",
        "def unique_count(values):\n    pass",
        locale,
    )
    assert challenge is not None
    return challenge


def _recursive_length_challenge(locale: AppLocale = AppLocale.ENGLISH):
    challenge = python_challenge_for(
        "m09.p04",
        "def recursive_length(values, index=0):\n    pass",
        locale,
    )
    assert challenge is not None
    return challenge


def test_catalog_materializes_complete_trilingual_challenges() -> None:
    validate_python_challenge_catalog()

    descriptions = {
        locale: _unique_count_challenge(locale).visible_cases[0].description for locale in AppLocale
    }

    assert len(set(descriptions.values())) == 3
    assert all(description.strip() for description in descriptions.values())


def test_challenges_use_explicit_authored_objective_links() -> None:
    mappings = (
        (_unique_count_challenge(), MODULE_07_MAPPINGS_SETS),
        (_recursive_length_challenge(), MODULE_09_RECURSION),
    )

    for challenge, module in mappings:
        authored_ids = {objective.objective_id for objective in module.objectives}
        assert challenge.objective_ids
        assert set(challenge.objective_ids) <= authored_ids

    assert _unique_count_challenge().objective_ids == ("m07.o6", "m07.o8")
    assert _recursive_length_challenge().objective_ids == (
        "m09.o2",
        "m09.o3",
        "m09.o5",
    )


def test_reference_unique_count_solution_passes_visible_and_hidden_tests() -> None:
    result = PythonChallengeEvaluator().evaluate(
        "def unique_count(values):\n    return len(set(values))",
        _unique_count_challenge(),
    )

    assert result.all_passed
    assert all(case.passed for case in result.visible_results)
    assert result.hidden_passed == result.hidden_total == 2


def test_hidden_tests_reject_a_solution_hard_coded_for_visible_examples() -> None:
    source = (
        "def unique_count(values):\n"
        "    if values == [1, 1, 2, 3, 3]:\n"
        "        return 3\n"
        "    if values == []:\n"
        "        return 0\n"
        "    return 999"
    )

    result = PythonChallengeEvaluator().evaluate(source, _unique_count_challenge())

    assert all(case.passed for case in result.visible_results)
    assert result.hidden_passed == 0
    assert not result.all_passed


def test_recursive_length_contract_includes_nonzero_start_index() -> None:
    source = (
        "def recursive_length(values, index=0):\n"
        "    if index == len(values):\n"
        "        return 0\n"
        "    return 1 + recursive_length(values, index + 1)"
    )

    result = PythonChallengeEvaluator().evaluate(source, _recursive_length_challenge())

    assert result.all_passed
    assert result.hidden_passed == 2


def test_policy_rejection_is_reported_without_running_hidden_tests() -> None:
    result = PythonChallengeEvaluator().evaluate(
        "def unique_count(values):\n    open('answer.txt', 'w')\n    return 0",
        _unique_count_challenge(),
    )

    assert not result.all_passed
    assert result.hidden_passed == 0
    assert all(case.status is ChallengeCaseStatus.REJECTED for case in result.visible_results)
