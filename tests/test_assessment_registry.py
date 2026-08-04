"""Regression tests for the extensible assessment registration catalog."""

from __future__ import annotations

import pytest
from PySide6.QtWidgets import QWidget

from computational_biomedicine_study_hub.i18n import AppLocale
from computational_biomedicine_study_hub.ui.assessment_registry import (
    ASSESSMENT_REGISTRATIONS,
    AssessmentRegistration,
    validate_assessment_registrations,
)


def _unused_page_factory(progress_store, locale, settings) -> QWidget:  # type: ignore[no-untyped-def]
    del progress_store, locale, settings
    return QWidget()


def test_default_assessment_registry_has_stable_order_and_localized_titles() -> None:
    assert tuple(item.assessment_id for item in ASSESSMENT_REGISTRATIONS) == (
        "dm847.written",
        "dm857.capstone",
        "bmb830.oral",
        "bmb831.report",
    )
    for locale in AppLocale:
        assert all(item.title_for(locale).strip() for item in ASSESSMENT_REGISTRATIONS)


def test_assessment_registry_rejects_duplicate_course_pages() -> None:
    first = AssessmentRegistration(
        "test.one",
        "TEST",
        1,
        lambda locale: locale.value,
        _unused_page_factory,
    )
    second = AssessmentRegistration(
        "test.two",
        "test",
        2,
        lambda locale: locale.value,
        _unused_page_factory,
    )

    with pytest.raises(ValueError, match="one top-level assessment page"):
        validate_assessment_registrations((first, second))


def test_assessment_registry_rejects_duplicate_identities_case_insensitively() -> None:
    first = AssessmentRegistration(
        "test.same",
        "TEST1",
        1,
        lambda locale: locale.value,
        _unused_page_factory,
    )
    second = AssessmentRegistration(
        "TEST.SAME",
        "TEST2",
        2,
        lambda locale: locale.value,
        _unused_page_factory,
    )

    with pytest.raises(ValueError, match="IDs must be unique"):
        validate_assessment_registrations((first, second))
