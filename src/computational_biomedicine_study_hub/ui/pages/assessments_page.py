"""Course-aware assessment workspace without presentation-rehearsal features."""

from __future__ import annotations

from PySide6.QtCore import QSettings
from PySide6.QtWidgets import QTabWidget, QVBoxLayout, QWidget

from ...i18n.bmb831_report_copy import (
    BMB831ReportCopyKey,
    bmb831_report_text,
)
from ...i18n.locales import DEFAULT_LOCALE, AppLocale
from ...i18n.written_assessment_copy import (
    WrittenAssessmentCopyKey,
    written_assessment_text,
)
from ...storage.sqlite_progress_store import SQLiteProgressStore
from .bmb831_report_page import BMB831ReportPage
from .dm847_written_assessment_page import DM847WrittenAssessmentPage
from .dm857_capstone_page import DM857CapstonePage


class AssessmentsPage(QWidget):
    """Host independent written and project workflows for completed courses."""

    def __init__(
        self,
        progress_store: SQLiteProgressStore | None,
        locale: AppLocale = DEFAULT_LOCALE,
        *,
        settings: QSettings | None = None,
        parent: QWidget | None = None,
    ) -> None:
        super().__init__(parent)
        self.setObjectName("assessmentsPage")
        self._dm847 = DM847WrittenAssessmentPage(
            progress_store,
            locale,
            settings=settings,
        )
        self._dm857 = DM857CapstonePage(progress_store, locale)
        self._bmb831 = BMB831ReportPage(progress_store, locale)

        self._tabs = QTabWidget()
        self._tabs.setObjectName("assessmentCourseTabs")
        self._tabs.addTab(
            self._dm847,
            written_assessment_text(locale, WrittenAssessmentCopyKey.TAB_DM847),
        )
        self._tabs.addTab(
            self._dm857,
            written_assessment_text(locale, WrittenAssessmentCopyKey.TAB_DM857),
        )
        self._tabs.addTab(
            self._bmb831,
            bmb831_report_text(locale, BMB831ReportCopyKey.TAB),
        )

        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.addWidget(self._tabs)

    @property
    def dm847_page(self) -> DM847WrittenAssessmentPage:
        """Return the DM847 writing workflow."""

        return self._dm847

    @property
    def dm857_page(self) -> DM857CapstonePage:
        """Return the DM857 project workflow."""

        return self._dm857

    @property
    def capstone_page(self) -> DM857CapstonePage:
        """Return the DM857 capstone using its descriptive alias."""

        return self._dm857

    @property
    def bmb831_report_page(self) -> BMB831ReportPage:
        """Return the BMB831 individual-report workflow."""

        return self._bmb831

    def persist(self) -> None:
        """Persist all visible course-assessment work before lifecycle changes."""

        self._dm847.persist()
        self._dm857.persist()
        self._bmb831.persist()


__all__ = ["AssessmentsPage"]
