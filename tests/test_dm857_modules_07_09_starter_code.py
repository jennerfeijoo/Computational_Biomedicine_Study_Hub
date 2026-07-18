from __future__ import annotations

from computational_biomedicine_study_hub.content.dm857 import (
    MODULE_07_MAPPINGS_SETS,
    MODULE_08_FILES_EXCEPTIONS,
    MODULE_09_RECURSION,
)


def test_non_empty_starter_code_is_valid_python() -> None:
    modules = (
        MODULE_07_MAPPINGS_SETS,
        MODULE_08_FILES_EXCEPTIONS,
        MODULE_09_RECURSION,
    )

    for module in modules:
        for exercise in module.practice_exercises:
            if exercise.starter_code:
                compile(exercise.starter_code, f"<{exercise.exercise_id}>", "exec")
