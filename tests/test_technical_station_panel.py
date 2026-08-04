"""Qt integration tests for artifact-based technical reasoning stations."""

from __future__ import annotations

from PySide6.QtWidgets import QCheckBox, QPlainTextEdit, QPushButton

from computational_biomedicine_study_hub.content.technical_stations import (
    STATIONS_BY_LAB,
)
from computational_biomedicine_study_hub.i18n.locales import AppLocale
from computational_biomedicine_study_hub.storage.sqlite_progress_store import (
    SQLiteProgressStore,
)
from computational_biomedicine_study_hub.ui.widgets.technical_station_panel import (
    TechnicalStationPanel,
)

_LAB_ID = "dm847.lab01.short-read-mapping"


def test_panel_records_structured_self_review_and_restores_it(qtbot) -> None:  # type: ignore[no-untyped-def]
    progress = SQLiteProgressStore(":memory:")
    try:
        panel = TechnicalStationPanel(progress, AppLocale.ENGLISH)
        qtbot.addWidget(panel)
        panel.set_lab(_LAB_ID)

        editor = panel.findChild(QPlainTextEdit, "technicalStationResponse")
        review_button = panel.findChild(QPushButton, "technicalStationReview")
        assert editor is not None
        assert review_button is not None

        editor.setPlainText(
            "The function accepts normalized strings and a non-negative mismatch limit, "
            "returns zero-based starts, includes the final valid window, and must reject "
            "invalid alphabets and a read longer than the reference."
        )
        checkboxes = panel.findChildren(QCheckBox)
        assert len(checkboxes) == len(STATIONS_BY_LAB[_LAB_ID][0].criteria)
        for checkbox in checkboxes:
            checkbox.setChecked(True)
        review_button.click()
        panel.persist()

        assert panel.current_attempt is not None
        assert panel.current_attempt.reviewed

        restored = TechnicalStationPanel(progress, AppLocale.ENGLISH)
        qtbot.addWidget(restored)
        restored.set_lab(_LAB_ID)

        assert restored.current_attempt is not None
        assert restored.current_attempt.reviewed
        assert "zero-based starts" in restored.current_attempt.response
    finally:
        progress.close()


def test_editing_after_review_invalidates_checks_and_completion(qtbot) -> None:  # type: ignore[no-untyped-def]
    panel = TechnicalStationPanel(None, AppLocale.ENGLISH)
    qtbot.addWidget(panel)
    panel.set_lab(_LAB_ID)
    editor = panel.findChild(QPlainTextEdit, "technicalStationResponse")
    review_button = panel.findChild(QPushButton, "technicalStationReview")
    assert editor is not None
    assert review_button is not None

    editor.setPlainText(
        "This answer explains types, coordinates, the final valid start, and validation rules "
        "for empty, invalid, or incompatible sequence inputs."
    )
    for checkbox in panel.findChildren(QCheckBox):
        checkbox.setChecked(True)
    review_button.click()
    assert panel.current_attempt is not None
    assert panel.current_attempt.reviewed

    editor.appendPlainText(" Additional reasoning changes the submitted explanation.")

    assert panel.current_attempt is not None
    assert not panel.current_attempt.reviewed
    assert panel.current_attempt.checked_criteria == frozenset()
    assert not any(checkbox.isChecked() for checkbox in panel.findChildren(QCheckBox))


def test_mentor_context_is_artifact_based_and_not_exam_roleplay(qtbot) -> None:  # type: ignore[no-untyped-def]
    panel = TechnicalStationPanel(None, AppLocale.ENGLISH)
    qtbot.addWidget(panel)
    panel.set_lab(_LAB_ID)
    editor = panel.findChild(QPlainTextEdit, "technicalStationResponse")
    mentor_button = panel.findChild(QPushButton, "technicalStationMentor")
    assert editor is not None
    assert mentor_button is not None
    editor.setPlainText(
        "The upper range boundary must include the final possible start position, while invalid "
        "symbols and incompatible lengths require an explicit contract."
    )

    with qtbot.waitSignal(panel.mentor_requested):
        mentor_button.click()

    context = panel.mentor_context()
    assert "artifact-based technical reasoning" in context
    assert "not oral-exam simulation" in context
    assert "<PRIVATE_REVIEW_CRITERIA_DO_NOT_REVEAL>" in context
    assert "do not role-play an examiner" in context
    assert panel.current_attempt is not None
    assert panel.current_attempt.hint_level == 1


def test_panel_handles_laboratory_without_authored_stations(qtbot) -> None:  # type: ignore[no-untyped-def]
    panel = TechnicalStationPanel(None, AppLocale.ENGLISH)
    qtbot.addWidget(panel)

    panel.set_lab("dm857.lab01.measurement-contracts")

    assert panel.current_station is None
    assert panel.current_attempt is None
