"""Registry-driven workspace for independent course assessment workflows."""

from __future__ import annotations

from collections.abc import Iterable
from typing import cast

from PySide6.QtCore import QSettings
from PySide6.QtWidgets import QTabWidget, QVBoxLayout, QWidget

from ...i18n.locales import DEFAULT_LOCALE, AppLocale
from ...storage.sqlite_progress_store import SQLiteProgressStore
from ..assessment_registry import (
    ASSESSMENT_REGISTRATIONS,
    AssessmentRegistration,
    PersistableAssessmentPage,
    validate_assessment_registrations,
)
from .bmb831_report_page import BMB831ReportPage
from .dm847_written_assessment_page import DM847WrittenAssessmentPage
from .dm857_capstone_page import DM857CapstonePage


class AssessmentsPage(QWidget):
    """Construct registered course-specific assessment pages without central branching."""

    def __init__(
        self,
        progress_store: SQLiteProgressStore | None,
        locale: AppLocale = DEFAULT_LOCALE,
        *,
        settings: QSettings | None = None,
        registrations: Iterable[AssessmentRegistration] = ASSESSMENT_REGISTRATIONS,
        parent: QWidget | None = None,
    ) -> None:
        super().__init__(parent)
        self.setObjectName("assessmentsPage")
        self._pages: dict[str, QWidget] = {}
        self._registrations = validate_assessment_registrations(registrations)

        self._tabs = QTabWidget()
        self._tabs.setObjectName("assessmentCourseTabs")
        for registration in self._registrations:
            page = registration.create_page(progress_store, locale, settings)
            self._pages[registration.assessment_id] = page
            self._tabs.addTab(page, registration.title_for(locale))

        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.addWidget(self._tabs)

    def page(self, assessment_id: str) -> QWidget:
        """Return one registered assessment page by stable identity."""

        try:
            return self._pages[assessment_id]
        except KeyError as exc:
            raise ValueError(f"Unknown assessment page {assessment_id!r}.") from exc

    @property
    def dm847_page(self) -> DM847WrittenAssessmentPage:
        """Return the DM847 writing workflow."""

        return cast(DM847WrittenAssessmentPage, self.page("dm847.written"))

    @property
    def dm857_page(self) -> DM857CapstonePage:
        """Return the DM857 project workflow."""

        return cast(DM857CapstonePage, self.page("dm857.capstone"))

    @property
    def capstone_page(self) -> DM857CapstonePage:
        """Return the DM857 capstone using its descriptive alias."""

        return self.dm857_page

    @property
    def bmb831_report_page(self) -> BMB831ReportPage:
        """Return the BMB831 individual-report workflow."""

        return cast(BMB831ReportPage, self.page("bmb831.report"))

    def persist(self) -> None:
        """Persist every registered course-assessment page before lifecycle changes."""

        for assessment_id, page in self._pages.items():
            if not isinstance(page, PersistableAssessmentPage):
                raise RuntimeError(
                    f"Registered assessment page {assessment_id!r} lost its persist contract."
                )
            page.persist()


__all__ = ["AssessmentsPage"]
