"""Integration tests for technical stations inside the laboratory route."""

from __future__ import annotations

from PySide6.QtWidgets import QComboBox, QPushButton

from computational_biomedicine_study_hub.i18n.locales import AppLocale
from computational_biomedicine_study_hub.ui.pages.computational_labs_page import (
    ComputationalLabsPage,
)


def test_dm847_lab_exposes_stations_and_routes_mentor_context(qtbot) -> None:  # type: ignore[no-untyped-def]
    page = ComputationalLabsPage(None, AppLocale.ENGLISH)
    qtbot.addWidget(page)
    lab_selector = page.findChild(QComboBox, "computationalLabSelector")
    mentor_button = page.findChild(QPushButton, "technicalStationMentor")
    assert lab_selector is not None
    assert mentor_button is not None

    lab_selector.setCurrentIndex(1)

    assert page.current_lab.lab_id == "dm847.lab01.short-read-mapping"
    assert page.technical_station_panel.current_station is not None
    with qtbot.waitSignal(page.mentor_requested):
        mentor_button.click()

    context = page.mentor_context()
    assert "Mentor focus: artifact-based technical reasoning" in context
    assert "not oral-exam simulation" in context
    assert "Scientific workspace" in context


def test_dm857_lab_keeps_station_panel_outside_mastery_evidence(qtbot) -> None:  # type: ignore[no-untyped-def]
    page = ComputationalLabsPage(None, AppLocale.ENGLISH)
    qtbot.addWidget(page)

    assert page.current_lab.course_code == "DM857"
    assert page.technical_station_panel.current_station is None
    assert page.attempt.completion_ratio(page.current_lab) == 0.0
