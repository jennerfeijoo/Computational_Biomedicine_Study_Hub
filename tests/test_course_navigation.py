from __future__ import annotations

from PySide6.QtWidgets import QApplication

from computational_biomedicine_study_hub.ui.main_window import MainWindow


def test_main_window_can_navigate_to_each_first_semester_course(
    qapp: QApplication,
) -> None:
    window = MainWindow()

    for route in (
        "course/dm857",
        "course/dm847",
        "course/bmb830",
        "course/bmb831",
    ):
        window.navigate(route)
        assert window.current_route == route
