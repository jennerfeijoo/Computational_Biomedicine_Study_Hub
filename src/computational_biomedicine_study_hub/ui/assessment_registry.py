"""Registration catalog for independent course assessment workflows."""

from __future__ import annotations

from collections.abc import Callable, Iterable
from dataclasses import dataclass
from typing import Protocol, runtime_checkable

from PySide6.QtCore import QSettings
from PySide6.QtWidgets import QWidget

from ..i18n.bmb831_report_copy import BMB831ReportCopyKey, bmb831_report_text
from ..i18n.locales import AppLocale
from ..i18n.written_assessment_copy import (
    WrittenAssessmentCopyKey,
    written_assessment_text,
)
from ..storage.sqlite_progress_store import SQLiteProgressStore
from .pages.bmb831_report_page import BMB831ReportPage
from .pages.dm847_written_assessment_page import DM847WrittenAssessmentPage
from .pages.dm857_capstone_page import DM857CapstonePage


@runtime_checkable
class PersistableAssessmentPage(Protocol):
    """Minimal lifecycle contract required by the assessment workspace."""

    def persist(self) -> None:
        """Persist visible learner-owned assessment work."""


AssessmentPageFactory = Callable[
    [SQLiteProgressStore | None, AppLocale, QSettings | None],
    QWidget,
]
AssessmentTitleFactory = Callable[[AppLocale], str]


@dataclass(frozen=True, slots=True)
class AssessmentRegistration:
    """Describe one course-specific assessment page without central UI branching."""

    assessment_id: str
    course_code: str
    order: int
    title_factory: AssessmentTitleFactory
    page_factory: AssessmentPageFactory

    def __post_init__(self) -> None:
        if not self.assessment_id.strip():
            raise ValueError("Assessment registrations require a stable ID.")
        if not self.course_code.strip():
            raise ValueError("Assessment registrations require a course code.")
        if self.order < 0:
            raise ValueError("Assessment registration order cannot be negative.")

    def title_for(self, locale: AppLocale) -> str:
        """Return the strict localized tab title."""

        title = self.title_factory(locale).strip()
        if not title:
            raise ValueError(f"Assessment {self.assessment_id!r} produced an empty title.")
        return title

    def create_page(
        self,
        progress_store: SQLiteProgressStore | None,
        locale: AppLocale,
        settings: QSettings | None,
    ) -> QWidget:
        """Construct and validate one registered assessment page."""

        page = self.page_factory(progress_store, locale, settings)
        if not isinstance(page, PersistableAssessmentPage):
            raise TypeError(f"Assessment page {self.assessment_id!r} must implement persist().")
        return page


def _dm847_page(
    progress_store: SQLiteProgressStore | None,
    locale: AppLocale,
    settings: QSettings | None,
) -> QWidget:
    return DM847WrittenAssessmentPage(
        progress_store,
        locale,
        settings=settings,
    )


def _dm857_page(
    progress_store: SQLiteProgressStore | None,
    locale: AppLocale,
    settings: QSettings | None,
) -> QWidget:
    del settings
    return DM857CapstonePage(progress_store, locale)


def _bmb831_page(
    progress_store: SQLiteProgressStore | None,
    locale: AppLocale,
    settings: QSettings | None,
) -> QWidget:
    del settings
    return BMB831ReportPage(progress_store, locale)


ASSESSMENT_REGISTRATIONS: tuple[AssessmentRegistration, ...] = (
    AssessmentRegistration(
        assessment_id="dm847.written",
        course_code="DM847",
        order=10,
        title_factory=lambda locale: written_assessment_text(
            locale,
            WrittenAssessmentCopyKey.TAB_DM847,
        ),
        page_factory=_dm847_page,
    ),
    AssessmentRegistration(
        assessment_id="dm857.capstone",
        course_code="DM857",
        order=20,
        title_factory=lambda locale: written_assessment_text(
            locale,
            WrittenAssessmentCopyKey.TAB_DM857,
        ),
        page_factory=_dm857_page,
    ),
    AssessmentRegistration(
        assessment_id="bmb831.report",
        course_code="BMB831",
        order=30,
        title_factory=lambda locale: bmb831_report_text(
            locale,
            BMB831ReportCopyKey.TAB,
        ),
        page_factory=_bmb831_page,
    ),
)


def validate_assessment_registrations(
    registrations: Iterable[AssessmentRegistration] = ASSESSMENT_REGISTRATIONS,
) -> tuple[AssessmentRegistration, ...]:
    """Validate identities and return registrations in deterministic display order."""

    ordered = tuple(sorted(registrations, key=lambda item: (item.order, item.assessment_id)))
    identities = tuple(item.assessment_id.casefold() for item in ordered)
    if len(identities) != len(set(identities)):
        raise ValueError("Assessment registration IDs must be unique.")
    course_codes = tuple(item.course_code.casefold() for item in ordered)
    if len(course_codes) != len(set(course_codes)):
        raise ValueError("Each course may register only one top-level assessment page.")
    return ordered


ASSESSMENT_REGISTRATIONS = validate_assessment_registrations()

__all__ = [
    "ASSESSMENT_REGISTRATIONS",
    "AssessmentRegistration",
    "PersistableAssessmentPage",
    "validate_assessment_registrations",
]
