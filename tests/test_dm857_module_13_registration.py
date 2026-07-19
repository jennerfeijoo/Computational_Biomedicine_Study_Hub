"""Registration tests for DM857 module 13."""

from computational_biomedicine_study_hub.content.dm857 import (
    BUNDLES,
    MODULE_13_SCIENTIFIC_LIBRARIES,
    MODULES,
    OBJECTIVE_QUESTION_BANK_13,
    OBJECTIVE_QUESTION_BANKS,
)


def test_module_13_is_the_final_registered_dm857_module() -> None:
    assert len(BUNDLES) == 13
    assert len(MODULES) == 13
    assert BUNDLES[-1].content_version == "1.0.0"
    assert MODULES[-1] is MODULE_13_SCIENTIFIC_LIBRARIES
    assert MODULES[-1].module_id == "dm857.m13"


def test_module_13_objective_bank_is_registered_by_module_id() -> None:
    assert OBJECTIVE_QUESTION_BANKS["dm857.m13"] == OBJECTIVE_QUESTION_BANK_13
    assert len(OBJECTIVE_QUESTION_BANK_13) == 30
