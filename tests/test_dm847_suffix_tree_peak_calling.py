from computational_biomedicine_study_hub.content.dm847 import (
    DM847_MODULE_SOURCE_AUDIT,
    MODULE_06_SUFFIX_ARRAYS_BWT_MAPPING,
    MODULE_10_OMICS_LEARNING_PROJECT,
)


def test_m06_explicitly_covers_suffix_trees() -> None:
    text = " ".join(
        [
            MODULE_06_SUFFIX_ARRAYS_BWT_MAPPING.summary,
            *(concept.body for concept in MODULE_06_SUFFIX_ARRAYS_BWT_MAPPING.concepts),
            *(example.explanation for example in MODULE_06_SUFFIX_ARRAYS_BWT_MAPPING.worked_examples),
        ]
    ).lower()
    assert "suffix tree" in text
    assert any(item.item_id == "dm847.m06.audit.001" for item in MODULE_06_SUFFIX_ARRAYS_BWT_MAPPING.assessment_items)


def test_m10_explicitly_covers_bimodal_peak_calling() -> None:
    text = " ".join(
        [
            MODULE_10_OMICS_LEARNING_PROJECT.summary,
            *(concept.body for concept in MODULE_10_OMICS_LEARNING_PROJECT.concepts),
            *(example.explanation for example in MODULE_10_OMICS_LEARNING_PROJECT.worked_examples),
        ]
    ).lower()
    assert "bimodal" in text
    assert "peak calling" in text
    assert any(item.item_id == "dm847.m10.audit.001" for item in MODULE_10_OMICS_LEARNING_PROJECT.assessment_items)


def test_dm847_audit_marks_the_two_previous_gaps_consistent() -> None:
    audit = {item.module_id: item for item in DM847_MODULE_SOURCE_AUDIT}
    assert audit["dm847.m06"].state == "consistent"
    assert audit["dm847.m10"].state == "consistent"
    assert "suffix tree" in audit["dm847.m06"].finding.lower()
    assert "peak calling" in audit["dm847.m10"].finding.lower()
