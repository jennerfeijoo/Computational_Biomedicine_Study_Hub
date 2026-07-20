"""Regression coverage for the first academic UI redesign phase."""

from __future__ import annotations

from PySide6.QtWidgets import QFrame, QPushButton

from computational_biomedicine_study_hub.courses import COURSES
from computational_biomedicine_study_hub.i18n import Translator
from computational_biomedicine_study_hub.ui.navigation import NavigationSidebar
from computational_biomedicine_study_hub.ui.pages.home_page import HomePage


def test_navigation_collapses_without_losing_accessible_labels(qtbot) -> None:
    navigation = NavigationSidebar(COURSES, Translator(), collapsed=False)
    qtbot.addWidget(navigation)

    buttons = navigation.findChildren(QPushButton, "navigationButton")
    assert buttons
    assert all(button.text() for button in buttons)

    navigation.set_collapsed(True, animate=False)

    assert navigation.is_collapsed
    assert all(not button.text() for button in buttons)
    assert all(button.toolTip() for button in buttons)
    assert all(button.accessibleName() for button in buttons)

    navigation.set_collapsed(False, animate=False)

    assert not navigation.is_collapsed
    assert all(button.text() for button in buttons)


def test_home_dashboard_preserves_course_card_contract(qtbot) -> None:
    page = HomePage(COURSES, Translator())
    qtbot.addWidget(page)

    cards = page.findChildren(QFrame, "courseCard")
    open_buttons = page.findChildren(QPushButton, "courseOpenButton")

    assert len(cards) == len(COURSES)
    assert len(open_buttons) == len(COURSES)
    assert all(card.property("dashboardCard") == "true" for card in cards)
    assert all(button.property("dashboardVariant") == "secondary" for button in open_buttons)


def test_home_dashboard_refresh_rebuilds_visible_cards(qtbot) -> None:
    page = HomePage(COURSES, Translator())
    qtbot.addWidget(page)

    first_cards = page.findChildren(QFrame, "courseCard")
    page.refresh()
    qtbot.wait(1)
    refreshed_cards = page.findChildren(QFrame, "courseCard")

    assert len(first_cards) == len(COURSES)
    assert len(refreshed_cards) == len(COURSES)
