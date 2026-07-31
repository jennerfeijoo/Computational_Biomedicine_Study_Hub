"""PySide6 integration tests for the persistent DM857 capstone page."""

from __future__ import annotations

from PySide6.QtWidgets import (
    QApplication,
    QCheckBox,
    QLabel,
    QLineEdit,
    QPlainTextEdit,
)

from computational_biomedicine_study_hub.i18n import AppLocale
from computational_biomedicine_study_hub.learning.dm857_capstone import (
    DM857_CAPSTONE_MILESTONES,
    DM857_CAPSTONE_RUBRIC,
    CapstoneMilestoneStatus,
)
from computational_biomedicine_study_hub.storage import SQLiteProgressStore
from computational_biomedicine_study_hub.ui.main_window import MainWindow
from computational_biomedicine_study_hub.ui.pages.dm857_capstone_page import (
    DM857CapstonePage,
)
from computational_biomedicine_study_hub.ui.routes import RouteId


def _complete_editor(page: DM857CapstonePage, milestone_id: str) -> None:
    editor = page.milestone_editor(milestone_id)
    for checkbox in editor.findChildren(QCheckBox, "capstoneChecklistItem"):
        checkbox.setChecked(True)
    evidence = editor.findChild(QPlainTextEdit, "capstoneEvidenceNote")
    commit = editor.findChild(QLineEdit, "capstoneCommitReference")
    assert evidence is not None
    assert commit is not None
    evidence.setPlainText(f"Evidence for {milestone_id}")
    commit.setText(f"commit-{milestone_id}")


def test_capstone_page_persists_metadata_and_milestone_evidence(
    qapp: QApplication,
) -> None:
    del qapp
    progress_store = SQLiteProgressStore(":memory:")
    page = DM857CapstonePage(progress_store, AppLocale.ENGLISH)

    title = page.findChild(QLineEdit, "capstoneProjectTitle")
    members = page.findChild(QLineEdit, "capstoneGroupMembers")
    repository = page.findChild(QLineEdit, "capstoneRepositoryUrl")
    report = page.findChild(QLineEdit, "capstoneReportPath")
    assert title is not None
    assert members is not None
    assert repository is not None
    assert report is not None

    title.setText("Clinical sample tracker")
    members.setText("Ada, Linus")
    repository.setText("https://example.invalid/group/sample-tracker")
    report.setText("reports/dm857-report.pdf")
    first_id = DM857_CAPSTONE_MILESTONES[0].milestone_id
    _complete_editor(page, first_id)
    page.persist()

    restored = DM857CapstonePage(progress_store, AppLocale.DANISH_DENMARK)

    assert restored.progress.project_title == "Clinical sample tracker"
    assert restored.progress.group_members == ("Ada", "Linus")
    assert restored.progress.repository_url.endswith("sample-tracker")
    assert restored.progress.milestone(first_id).status is CapstoneMilestoneStatus.READY
    progress_store.close()


def test_capstone_page_reaches_internal_readiness_only_with_all_evidence(
    qapp: QApplication,
) -> None:
    del qapp
    progress_store = SQLiteProgressStore(":memory:")
    page = DM857CapstonePage(progress_store, AppLocale.ENGLISH)

    metadata = {
        "capstoneProjectTitle": "Tree quality analyser",
        "capstoneGroupMembers": "Ada, Grace",
        "capstoneRepositoryUrl": "https://example.invalid/group/tree-quality",
        "capstoneReportPath": "report.pdf",
    }
    for object_name, value in metadata.items():
        field = page.findChild(QLineEdit, object_name)
        assert field is not None
        field.setText(value)

    for spec in DM857_CAPSTONE_MILESTONES:
        _complete_editor(page, spec.milestone_id)
    for criterion in DM857_CAPSTONE_RUBRIC:
        combo = page.rubric_combo(criterion.criterion_id)
        combo.setCurrentIndex(combo.findData(3))
    page.persist()

    assert page.progress.preparation_ready
    assert page.progress.ready_milestone_count == 5
    assert page.progress.weighted_rubric_percent == 75
    readiness = page.findChild(QLabel, "capstoneReadiness")
    assert readiness is not None
    assert readiness.property("preparationReady") is True
    progress_store.close()


def test_assessments_route_hosts_the_dm857_capstone(
    qapp: QApplication,
) -> None:
    del qapp
    progress_store = SQLiteProgressStore(":memory:")
    window = MainWindow(progress_store=progress_store)

    window.navigate(RouteId.ASSESSMENTS)

    assert window.current_route is RouteId.ASSESSMENTS
    page = window.findChild(DM857CapstonePage, "dm857CapstonePage")
    assert page is not None
    assert len(page.findChildren(QCheckBox, "capstoneChecklistItem")) == 15
    progress_store.close()
