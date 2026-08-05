"""PySide6 integration tests for longitudinal DM857 project supervision."""

from __future__ import annotations

from datetime import date

from PySide6.QtWidgets import (
    QApplication,
    QCheckBox,
    QComboBox,
    QLineEdit,
    QPlainTextEdit,
    QPushButton,
)

from computational_biomedicine_study_hub.i18n import AppLocale
from computational_biomedicine_study_hub.learning.dm857_weekly_supervision import (
    WeeklyCycleStatus,
)
from computational_biomedicine_study_hub.storage import SQLiteProgressStore
from computational_biomedicine_study_hub.ui.pages.assessments_page import AssessmentsPage
from computational_biomedicine_study_hub.ui.pages.dm857_supervised_capstone_page import (
    DM857SupervisedCapstonePage,
)
from computational_biomedicine_study_hub.ui.widgets.dm857_weekly_supervision_panel import (
    DM857WeeklySupervisionPanel,
)


def _set_multiline(page: DM857SupervisedCapstonePage, object_name: str, value: str) -> None:
    editor = page.findChild(QPlainTextEdit, object_name)
    assert editor is not None
    editor.setPlainText(value)


def _set_line(page: DM857SupervisedCapstonePage, object_name: str, value: str) -> None:
    editor = page.findChild(QLineEdit, object_name)
    assert editor is not None
    editor.setText(value)


def _complete_week(page: DM857SupervisedCapstonePage) -> None:
    _set_multiline(page, "weeklyObjective", "Validate sample metadata before analysis")
    _set_multiline(
        page,
        "weeklySuccessCriteria",
        "Malformed sample IDs fail deterministic tests",
    )
    _set_line(page, "weeklyStartReference", "abc123")
    _set_line(page, "weeklyEndReference", "def456")
    _set_multiline(page, "weeklyChangedFiles", "src/validation.py\ntests/test_validation.py")
    _set_multiline(page, "weeklyTestEvidence", "pytest: 12 passed")
    _set_multiline(
        page,
        "weeklyDecisionRationale",
        "A pure validator isolates input errors from downstream statistics",
    )
    _set_multiline(
        page,
        "weeklyIndividualContribution",
        "Implemented the validator and boundary tests in commits abc123..def456",
    )
    _set_multiline(
        page,
        "weeklyBiomedicalInterpretation",
        "Rejecting malformed identifiers protects sample traceability",
    )
    _set_multiline(
        page,
        "weeklyReflection",
        "I can now separate data-contract validation from model validation",
    )
    _set_multiline(
        page,
        "weeklyNextCommitment",
        "Add duplicate-sample detection with explicit tests",
    )


def test_supervised_capstone_persists_and_restores_weekly_repository_evidence(
    qapp: QApplication,
) -> None:
    del qapp
    progress_store = SQLiteProgressStore(":memory:")
    page = DM857SupervisedCapstonePage(
        progress_store,
        AppLocale.ENGLISH,
        today=date(2026, 8, 5),
    )
    _complete_week(page)

    page.persist()
    restored = DM857SupervisedCapstonePage(
        progress_store,
        AppLocale.SPANISH_SPAIN,
        today=date(2026, 8, 5),
    )
    cycle = restored.weekly_supervision_panel.current_cycle

    assert cycle.week_start == date(2026, 8, 3)
    assert cycle.status is WeeklyCycleStatus.COMPLETE
    assert cycle.start_reference == "abc123"
    assert cycle.end_reference == "def456"
    assert cycle.test_evidence == "pytest: 12 passed"
    assert cycle.individual_contribution.startswith("Implemented")
    progress_store.close()


def test_weekly_panel_creates_ordered_history_without_overwriting_prior_week(
    qapp: QApplication,
) -> None:
    del qapp
    progress_store = SQLiteProgressStore(":memory:")
    page = DM857SupervisedCapstonePage(
        progress_store,
        AppLocale.ENGLISH,
        today=date(2026, 8, 5),
    )
    _set_multiline(page, "weeklyObjective", "Finish the input contract")
    page.persist()

    button = page.findChild(QPushButton, "weeklyNewCycleButton")
    selector = page.findChild(QComboBox, "weeklyCycleSelector")
    assert button is not None
    assert selector is not None
    button.click()

    snapshot = page.weekly_supervision_panel.snapshot
    assert tuple(cycle.week_start for cycle in snapshot.cycles) == (
        date(2026, 8, 3),
        date(2026, 8, 10),
    )
    assert snapshot.cycles[0].objective == "Finish the input contract"
    assert snapshot.selected_cycle_id == snapshot.cycles[1].cycle_id
    assert selector.count() == 2
    progress_store.close()


def test_weekly_mentor_request_propagates_exact_evidence_and_next_commitment(
    qapp: QApplication,
) -> None:
    del qapp
    progress_store = SQLiteProgressStore(":memory:")
    page = DM857SupervisedCapstonePage(
        progress_store,
        AppLocale.ENGLISH,
        today=date(2026, 8, 5),
    )
    _complete_week(page)
    emitted: list[bool] = []
    page.mentor_requested.connect(lambda: emitted.append(True))
    mentor = page.findChild(QPushButton, "weeklyMentorButton")
    assert mentor is not None

    mentor.click()
    context = page.mentor_context()

    assert emitted == [True]
    assert "Validate sample metadata before analysis" in context
    assert "pytest: 12 passed" in context
    assert "abc123" in context and "def456" in context
    assert "Add duplicate-sample detection" in context
    assert "do not assign an official grade" in context
    progress_store.close()


def test_assessment_registry_uses_supervised_capstone_and_preserves_base_identity(
    qapp: QApplication,
) -> None:
    del qapp
    progress_store = SQLiteProgressStore(":memory:")
    assessments = AssessmentsPage(progress_store, AppLocale.ENGLISH)

    page = assessments.dm857_page
    panel = page.findChild(DM857WeeklySupervisionPanel, "weeklySupervisionPanel")
    blocked = page.findChild(QCheckBox, "weeklyBlocked")

    assert isinstance(page, DM857SupervisedCapstonePage)
    assert page.objectName() == "dm857CapstonePage"
    assert panel is page.weekly_supervision_panel
    assert blocked is not None
    progress_store.close()
