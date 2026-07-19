"""Registration tests for DM857 module 14."""

from computational_biomedicine_study_hub.content.dm857 import (
    BUNDLES,
    MODULE_14_TESTING_DEBUGGING_QUALITY,
    MODULES,
    OBJECTIVE_QUESTION_BANK_14,
    OBJECTIVE_QUESTION_BANKS,
)


def test_module_14_is_the_final_registered_dm857_module() -> None:
    assert len(BUNDLES) == 14
    assert len(MODULES) == 14
    assert BUNDLES[-1].content_version == "1.0.0"
    assert MODULES[-1] is MODULE_14_TESTING_DEBUGGING_QUALITY
    assert MODULES[-1].module_id == "dm857.m14"


def test_module_14_objective_bank_is_registered_by_module_id() -> None:
    assert OBJECTIVE_QUESTION_BANKS["dm857.m14"] == OBJECTIVE_QUESTION_BANK_14
    assert len(OBJECTIVE_QUESTION_BANK_14) == 30
