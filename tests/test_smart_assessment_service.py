from __future__ import annotations

from types import SimpleNamespace

from computational_biomedicine_study_hub.learning.activity_types import ActivityType
from computational_biomedicine_study_hub.learning.smart_assessment_service import (
    _allocate_quotas,
    programming_exercises,
)


def _module(module_id: str, activity_types: tuple[ActivityType, ...]):
    exercises = tuple(
        SimpleNamespace(
            exercise_id=f"{module_id}-{index}",
            activity_type=activity_type,
            starter_code="def solve():\n    pass" if activity_type == ActivityType.CODE_COMPLETION else "",
        )
        for index, activity_type in enumerate(activity_types)
    )
    return SimpleNamespace(module_id=module_id, practice_exercises=exercises)


def test_programming_exercises_only_returns_explicit_code_activities():
    module = _module(
        "DM857-M01",
        (
            ActivityType.SHORT_ANSWER,
            ActivityType.CODE_COMPLETION,
            ActivityType.DATA_INTERPRETATION,
            ActivityType.DEBUGGING,
        ),
    )

    exercises = programming_exercises(module)

    assert [exercise.activity_type for exercise in exercises] == [
        ActivityType.CODE_COMPLETION,
        ActivityType.DEBUGGING,
    ]


def test_generic_activity_with_starter_code_is_not_treated_as_programming():
    module = SimpleNamespace(
        module_id="BMB830-M01",
        practice_exercises=(
            SimpleNamespace(
                exercise_id="generic-1",
                activity_type=ActivityType.SHORT_ANSWER,
                starter_code="print('x')",
            ),
        ),
    )

    assert programming_exercises(module) == ()


def test_weak_modules_receive_more_assessment_quota():
    modules = (_module("M1", ()), _module("M2", ()), _module("M3", ()))
    weights = {"M1": 2.0, "M2": 1.0, "M3": 0.6}

    quotas = _allocate_quotas(8, modules, weights)

    assert sum(quotas.values()) == 8
    assert quotas["M1"] >= quotas["M2"] >= quotas["M3"]
    assert all(value >= 1 for value in quotas.values())
