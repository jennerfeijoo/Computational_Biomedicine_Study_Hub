"""Authored visible and hidden tests for executable starter-code exercises."""

from __future__ import annotations

from dataclasses import dataclass

from ..i18n.locales import AppLocale
from .localized_models import LocalizedText


@dataclass(frozen=True, slots=True)
class PythonChallengeCase:
    """One materialized behavioral test for a learner submission."""

    case_id: str
    description: str
    assertion: str

    def __post_init__(self) -> None:
        if not self.case_id.strip():
            raise ValueError("Python challenge cases require a non-empty case ID.")
        if self.case_id != self.case_id.strip():
            raise ValueError("Python challenge case IDs cannot contain surrounding whitespace.")
        if not self.description.strip():
            raise ValueError(f"Python challenge case {self.case_id!r} requires a description.")
        if not self.assertion.strip():
            raise ValueError(f"Python challenge case {self.case_id!r} requires test code.")
        compile(self.assertion, f"<python-challenge:{self.case_id}>", "exec")


@dataclass(frozen=True, slots=True)
class PythonChallenge:
    """Runtime challenge with explicit objectives and undisclosed behavioral tests."""

    course_code: str
    module_id: str
    exercise_id: str
    starter_code: str
    objective_ids: tuple[str, ...]
    visible_cases: tuple[PythonChallengeCase, ...]
    hidden_cases: tuple[PythonChallengeCase, ...]
    timeout_seconds: float = 1.0

    def __post_init__(self) -> None:
        required = {
            "course_code": self.course_code,
            "module_id": self.module_id,
            "exercise_id": self.exercise_id,
            "starter_code": self.starter_code,
        }
        for field_name, value in required.items():
            if not value.strip():
                raise ValueError(f"Python challenge field {field_name!r} cannot be empty.")
        if not self.objective_ids:
            raise ValueError(f"Python challenge {self.exercise_id!r} requires objective links.")
        normalized_objectives = tuple(
            objective_id.strip().casefold() for objective_id in self.objective_ids
        )
        if any(not objective_id for objective_id in normalized_objectives):
            raise ValueError("Python challenge objective IDs cannot be empty.")
        if any(objective_id != objective_id.strip() for objective_id in self.objective_ids):
            raise ValueError("Python challenge objective IDs cannot contain surrounding whitespace.")
        if len(normalized_objectives) != len(set(normalized_objectives)):
            raise ValueError("Python challenge objective IDs cannot contain duplicates.")

        local_module_id = self.module_id.rsplit(".", maxsplit=1)[-1]
        expected_prefix = f"{local_module_id}.o"
        invalid_objectives = tuple(
            objective_id
            for objective_id in self.objective_ids
            if not objective_id.startswith(expected_prefix)
        )
        if invalid_objectives:
            raise ValueError(
                f"Python challenge {self.exercise_id!r} has out-of-module objectives: "
                + ", ".join(invalid_objectives)
            )

        if not self.visible_cases:
            raise ValueError(f"Python challenge {self.exercise_id!r} requires visible tests.")
        if not self.hidden_cases:
            raise ValueError(f"Python challenge {self.exercise_id!r} requires hidden tests.")
        if not 0.1 <= self.timeout_seconds <= 5.0:
            raise ValueError("Python challenge timeouts must be between 0.1 and 5.0 seconds.")

        case_ids = tuple(case.case_id for case in (*self.visible_cases, *self.hidden_cases))
        normalized = tuple(case_id.casefold() for case_id in case_ids)
        if len(normalized) != len(set(normalized)):
            raise ValueError(f"Python challenge {self.exercise_id!r} has duplicate case IDs.")


@dataclass(frozen=True, slots=True)
class LocalizedPythonChallengeCase:
    """One language-independent test with a trilingual learner-facing description."""

    case_id: str
    description: LocalizedText
    assertion: str

    def materialize(self, locale: AppLocale) -> PythonChallengeCase:
        return PythonChallengeCase(
            case_id=self.case_id,
            description=self.description.for_locale(locale),
            assertion=self.assertion,
        )


@dataclass(frozen=True, slots=True)
class LocalizedPythonChallenge:
    """Strict trilingual authoring contract for one starter-code challenge."""

    course_code: str
    module_id: str
    exercise_id: str
    starter_code: str
    objective_ids: tuple[str, ...]
    visible_cases: tuple[LocalizedPythonChallengeCase, ...]
    hidden_cases: tuple[LocalizedPythonChallengeCase, ...]
    timeout_seconds: float = 1.0

    def materialize(self, locale: AppLocale) -> PythonChallenge:
        return PythonChallenge(
            course_code=self.course_code,
            module_id=self.module_id,
            exercise_id=self.exercise_id,
            starter_code=self.starter_code,
            objective_ids=self.objective_ids,
            visible_cases=tuple(case.materialize(locale) for case in self.visible_cases),
            hidden_cases=tuple(case.materialize(locale) for case in self.hidden_cases),
            timeout_seconds=self.timeout_seconds,
        )


def _text(spanish: str, english: str, danish: str) -> LocalizedText:
    return LocalizedText(spanish=spanish, english=english, danish=danish)


def _case(
    case_id: str,
    description: tuple[str, str, str],
    assertion: str,
) -> LocalizedPythonChallengeCase:
    return LocalizedPythonChallengeCase(
        case_id=case_id,
        description=_text(*description),
        assertion=assertion,
    )


_CHALLENGES: tuple[LocalizedPythonChallenge, ...] = (
    LocalizedPythonChallenge(
        course_code="DM857",
        module_id="dm857.m07",
        exercise_id="m07.p04",
        starter_code="def unique_count(values):\n    pass",
        objective_ids=("m07.o6", "m07.o8"),
        visible_cases=(
            _case(
                "duplicates",
                (
                    "Cuenta correctamente enteros repetidos.",
                    "Counts repeated integers correctly.",
                    "Tæller gentagne heltal korrekt.",
                ),
                "assert unique_count([1, 1, 2, 3, 3]) == 3",
            ),
            _case(
                "empty",
                (
                    "La colección vacía contiene cero elementos únicos.",
                    "An empty collection contains zero unique elements.",
                    "En tom samling indeholder nul unikke elementer.",
                ),
                "assert unique_count([]) == 0",
            ),
        ),
        hidden_cases=(
            _case(
                "strings",
                (
                    "Comprueba categorías de texto repetidas.",
                    "Checks repeated text categories.",
                    "Kontrollerer gentagne tekstkategorier.",
                ),
                "assert unique_count(['A', 'A', 'B', 'A']) == 2",
            ),
            _case(
                "hashable-records",
                (
                    "Comprueba registros hashables repetidos.",
                    "Checks repeated hashable records.",
                    "Kontrollerer gentagne hashbare poster.",
                ),
                "assert unique_count([('S1', 1), ('S1', 1), ('S2', 2)]) == 2",
            ),
        ),
    ),
    LocalizedPythonChallenge(
        course_code="DM857",
        module_id="dm857.m09",
        exercise_id="m09.p04",
        starter_code="def recursive_length(values, index=0):\n    pass",
        objective_ids=("m09.o2", "m09.o3", "m09.o5"),
        visible_cases=(
            _case(
                "three-elements",
                (
                    "Cuenta una secuencia de tres elementos.",
                    "Counts a three-element sequence.",
                    "Tæller en sekvens med tre elementer.",
                ),
                "assert recursive_length([10, 20, 30]) == 3",
            ),
            _case(
                "empty",
                (
                    "El caso base devuelve cero para una secuencia vacía.",
                    "The base case returns zero for an empty sequence.",
                    "Basistilfældet returnerer nul for en tom sekvens.",
                ),
                "assert recursive_length([]) == 0",
            ),
        ),
        hidden_cases=(
            _case(
                "tuple",
                (
                    "Comprueba otra secuencia indexable.",
                    "Checks another indexable sequence.",
                    "Kontrollerer en anden indekserbar sekvens.",
                ),
                "assert recursive_length(('A', 'B', 'C', 'D')) == 4",
            ),
            _case(
                "nonzero-index",
                (
                    "Comprueba el contrato cuando el índice inicial no es cero.",
                    "Checks the contract when the initial index is not zero.",
                    "Kontrollerer kontrakten, når startindekset ikke er nul.",
                ),
                "assert recursive_length([1, 2, 3, 4], 2) == 2",
            ),
        ),
    ),
)


def python_challenge_for(
    exercise_id: str,
    starter_code: str,
    locale: AppLocale,
) -> PythonChallenge | None:
    """Return the uniquely authored challenge matching one starter-code exercise."""

    for challenge in _CHALLENGES:
        if challenge.exercise_id == exercise_id and challenge.starter_code == starter_code:
            return challenge.materialize(locale)
    return None


def validate_python_challenge_catalog() -> None:
    """Reject duplicate match keys and invalid materializations in any locale."""

    keys = tuple((challenge.exercise_id, challenge.starter_code) for challenge in _CHALLENGES)
    if len(keys) != len(set(keys)):
        raise ValueError("Python challenge match keys must be unique.")
    for challenge in _CHALLENGES:
        for locale in AppLocale:
            challenge.materialize(locale)


validate_python_challenge_catalog()

__all__ = [
    "LocalizedPythonChallenge",
    "LocalizedPythonChallengeCase",
    "PythonChallenge",
    "PythonChallengeCase",
    "python_challenge_for",
    "validate_python_challenge_catalog",
]
