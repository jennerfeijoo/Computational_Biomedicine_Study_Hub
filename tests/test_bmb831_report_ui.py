"""PySide6 integration tests for the BMB831 report studio."""

from __future__ import annotations

from PySide6.QtWidgets import QApplication, QComboBox, QLabel, QTabWidget

from computational_biomedicine_study_hub.i18n import AppLocale
from computational_biomedicine_study_hub.storage.bmb831_report_store import BMB831ReportStore
from computational_biomedicine_study_hub.storage.sqlite_progress_store import SQLiteProgressStore
from computational_biomedicine_study_hub.ui.pages.assessments_page import AssessmentsPage
from computational_biomedicine_study_hub.ui.pages.bmb831_report_page import BMB831ReportPage


def test_report_page_preserves_sections_and_drafts(qapp: QApplication) -> None:
    del qapp
    progress = SQLiteProgressStore(":memory:")
    store = BMB831ReportStore.for_progress_store(progress)
    page = BMB831ReportPage(progress, AppLocale.ENGLISH, report_store=store)
    selector = page.findChild(QComboBox, "bmb831ReportSectionSelector")

    assert selector is not None
    assert selector.count() == 10
    assert page.current_section_id == "bmb831.report.question"
    page.editor.setPlainText("We estimate a batch-adjusted treatment contrast.")
    assert page.select_section(page.current_section_id)
    assert page.editor.toPlainText() == "We estimate a batch-adjusted treatment contrast."
    page.persist()

    assert page.select_section("bmb831.report.results")
    page.editor.setPlainText("The adjusted log2 fold change was 1.20.")
    page.persist()

    restored = BMB831ReportPage(progress, AppLocale.ENGLISH, report_store=store)
    assert restored.current_section_id == "bmb831.report.results"
    assert restored.editor.toPlainText().startswith("The adjusted")
    assert restored.select_section("bmb831.report.question")
    assert restored.editor.toPlainText().startswith("We estimate")
    assert restored.snapshot.completed_section_count == 2


def test_report_page_localizes_controls_but_preserves_english_requirement(
    qapp: QApplication,
) -> None:
    del qapp
    progress = SQLiteProgressStore(":memory:")
    page = BMB831ReportPage(progress, AppLocale.SPANISH_SPAIN)
    selector = page.findChild(QComboBox, "bmb831ReportSectionSelector")
    boundary = page.findChild(QLabel, "bmb831EnglishBoundary")

    assert selector is not None
    assert boundary is not None
    assert "inglés" in boundary.text().casefold()
    assert page.select_section("bmb831.report.abstract")
    assert page.current_section_id == "bmb831.report.abstract"


def test_assessments_page_hosts_four_course_workflows(qapp: QApplication) -> None:
    del qapp
    progress = SQLiteProgressStore(":memory:")
    page = AssessmentsPage(progress, AppLocale.ENGLISH)
    tabs = page.findChild(QTabWidget, "assessmentCourseTabs")

    assert tabs is not None
    assert tabs.count() == 4
    assert page.dm847_page is not None
    assert page.capstone_page is not None
    assert page.bmb830_oral_page is not None
    assert page.bmb831_report_page is not None
    assert "BMB830" in tabs.tabText(2)
    assert "BMB831" in tabs.tabText(3)

    page.bmb831_report_page.editor.setPlainText("An English report draft.")
    page.persist()
    assert page.bmb831_report_page.snapshot.completed_section_count == 1
