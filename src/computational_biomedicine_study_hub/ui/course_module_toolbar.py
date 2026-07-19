"""Shared compact navigation and course-information surface."""

from __future__ import annotations

from collections.abc import Mapping, Sequence
from dataclasses import dataclass
from typing import Any

from PySide6.QtCore import Qt, Signal
from PySide6.QtWidgets import (
    QComboBox,
    QDialog,
    QFrame,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QScrollArea,
    QSizePolicy,
    QVBoxLayout,
    QWidget,
)

from ..academic.localization import localize_value
from ..academic.models import CourseContent
from ..i18n import AppLocale
from .learning_page_copy import LearningPageCopyKey, learning_text


@dataclass(frozen=True, slots=True)
class CourseInformation:
    """Reader-facing course information without source-format details."""

    title: str
    description: str
    outcomes: tuple[str, ...]
    ects: str = ""
    assessment: tuple[str, ...] = ()
    prerequisites: tuple[str, ...] = ()
    connections: tuple[str, ...] = ()


_COPY = {
    AppLocale.SPANISH_SPAIN: {
        "information": "Información",
        "dialog_title": "Información del curso",
        "description": "Descripción",
        "outcomes": "Resultados de aprendizaje",
        "ects": "ECTS",
        "assessment": "Evaluación",
        "prerequisites": "Conocimientos previos",
        "connections": "Conexiones con otras asignaturas",
        "close": "Cerrar",
        "cumulative": "Acumulativa",
        "cumulative_accessible": "Evaluación acumulativa",
    },
    AppLocale.ENGLISH: {
        "information": "Information",
        "dialog_title": "Course information",
        "description": "Description",
        "outcomes": "Learning outcomes",
        "ects": "ECTS",
        "assessment": "Assessment",
        "prerequisites": "Prerequisites",
        "connections": "Connections to other courses",
        "close": "Close",
        "cumulative": "Cumulative",
        "cumulative_accessible": "Cumulative assessment",
    },
    AppLocale.DANISH_DENMARK: {
        "information": "Information",
        "dialog_title": "Kursusinformation",
        "description": "Beskrivelse",
        "outcomes": "Læringsudbytte",
        "ects": "ECTS",
        "assessment": "Evaluering",
        "prerequisites": "Forudsætninger",
        "connections": "Forbindelser til andre kurser",
        "close": "Luk",
        "cumulative": "Kumulativ",
        "cumulative_accessible": "Kumulativ evaluering",
    },
}


class CourseInformationDialog(QDialog):
    """Present the available course metadata in a compact, scrollable dialog."""

    def __init__(
        self,
        information: CourseInformation,
        *,
        locale: AppLocale,
        parent: QWidget | None = None,
    ) -> None:
        super().__init__(parent)
        copy = _COPY[locale]
        self.setObjectName("courseInformationDialog")
        self.setWindowTitle(copy["dialog_title"])
        self.setModal(False)
        self.resize(680, 560)

        content = QWidget()
        content.setObjectName("courseInformationContent")
        content_layout = QVBoxLayout(content)
        content_layout.setContentsMargins(18, 16, 18, 16)
        content_layout.setSpacing(12)

        heading = QLabel(information.title)
        heading.setObjectName("courseInformationTitle")
        heading.setWordWrap(True)
        content_layout.addWidget(heading)

        fields: tuple[tuple[str, str, tuple[str, ...]], ...] = (
            (copy["description"], information.description, ()),
            (copy["outcomes"], "", information.outcomes),
            (copy["ects"], information.ects, ()),
            (copy["assessment"], "", information.assessment),
            (copy["prerequisites"], "", information.prerequisites),
            (copy["connections"], "", information.connections),
        )
        for label, value, values in fields:
            visible_values = tuple(item.strip() for item in values if item.strip())
            visible_value = value.strip()
            if not visible_value and not visible_values:
                continue
            field_heading = QLabel(label)
            field_heading.setObjectName("courseInformationFieldTitle")
            body = QLabel(
                visible_value
                if visible_value
                else "\n".join(f"• {item}" for item in visible_values)
            )
            body.setObjectName("courseInformationFieldBody")
            body.setWordWrap(True)
            body.setTextInteractionFlags(
                Qt.TextInteractionFlag.TextSelectableByMouse
                | Qt.TextInteractionFlag.TextSelectableByKeyboard
            )
            content_layout.addWidget(field_heading)
            content_layout.addWidget(body)
        content_layout.addStretch(1)

        scroll = QScrollArea()
        scroll.setObjectName("courseInformationScroll")
        scroll.setWidgetResizable(True)
        scroll.setFrameShape(QFrame.Shape.NoFrame)
        scroll.setWidget(content)

        close_button = QPushButton(copy["close"])
        close_button.setObjectName("closeCourseInformationButton")
        close_button.clicked.connect(self.close)
        close_row = QHBoxLayout()
        close_row.addStretch(1)
        close_row.addWidget(close_button)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 12)
        layout.addWidget(scroll, 1)
        layout.addLayout(close_row)


class CourseModuleToolbar(QFrame):
    """Shared compact course toolbar used by every semester-one course."""

    module_changed = Signal(int)
    continue_requested = Signal()
    cumulative_requested = Signal()

    def __init__(
        self,
        *,
        course_code: str,
        locale: AppLocale,
        information: CourseInformation,
        cumulative_available: bool,
        parent: QWidget | None = None,
    ) -> None:
        super().__init__(parent)
        copy = _COPY[locale]
        self._locale = locale
        self._information = information
        self._information_dialog: CourseInformationDialog | None = None
        self.setObjectName("moduleContextBar")
        self.setProperty("courseCode", course_code)
        self.setAccessibleName(f"{information.title} — {course_code}")
        self.setToolTip(course_code)
        self.setMaximumHeight(64)

        self.module_selector = QComboBox()
        self.module_selector.setObjectName("courseModuleSelector")
        self.module_selector.setAccessibleName(learning_text(locale, LearningPageCopyKey.MODULE))
        self.module_selector.setSizeAdjustPolicy(
            QComboBox.SizeAdjustPolicy.AdjustToMinimumContentsLengthWithIcon
        )
        self.module_selector.setMinimumContentsLength(5)
        self.module_selector.setFixedWidth(76)

        self.module_title = QLabel()
        self.module_title.setObjectName("moduleContextTitle")
        self.module_title.setWordWrap(True)
        self.module_title.setMinimumWidth(160)
        self.module_title.setMaximumHeight(self.module_title.fontMetrics().lineSpacing() * 2 + 8)
        self.module_title.setSizePolicy(
            QSizePolicy.Policy.Expanding,
            QSizePolicy.Policy.Preferred,
        )

        self.progress_summary = QLabel()
        self.progress_summary.setObjectName("courseProgressSummary")
        self.progress_summary.setWordWrap(False)
        self.progress_summary.setMinimumWidth(150)
        self.progress_summary.setMaximumWidth(210)

        self.continue_button = QPushButton(learning_text(locale, LearningPageCopyKey.CONTINUE))
        self.continue_button.setObjectName("continueCourseButton")
        self.continue_button.setAccessibleName(self.continue_button.text())
        self.continue_button.setMaximumWidth(105)

        self.cumulative_button = QPushButton(copy["cumulative"])
        self.cumulative_button.setObjectName("openCumulativeAssessmentButton")
        self.cumulative_button.setAccessibleName(copy["cumulative_accessible"])
        self.cumulative_button.setToolTip(copy["cumulative_accessible"])
        self.cumulative_button.setMaximumWidth(145)
        self.cumulative_button.setVisible(cumulative_available)

        self.information_button = QPushButton(copy["information"])
        self.information_button.setObjectName("courseInformationButton")
        self.information_button.setAccessibleName(self.information_button.text())
        self.information_button.setMaximumWidth(110)

        layout = QHBoxLayout(self)
        layout.setContentsMargins(12, 6, 12, 6)
        layout.setSpacing(10)
        layout.addWidget(self.module_selector)
        layout.addWidget(self.module_title, 1)
        layout.addWidget(self.progress_summary)
        layout.addWidget(self.continue_button)
        layout.addWidget(self.cumulative_button)
        layout.addWidget(self.information_button)

        self.module_selector.currentIndexChanged.connect(self.module_changed)
        self.continue_button.clicked.connect(self.continue_requested)
        self.cumulative_button.clicked.connect(self.cumulative_requested)
        self.information_button.clicked.connect(self.open_information)

    def add_module(self, number: int, module_id: str) -> None:
        """Add a module without exposing its internal identity in visible text."""
        self.module_selector.addItem(f"M{number:02}", module_id)

    def set_module_title(self, title: str) -> None:
        """Update the flexible title and retain the full value in a tooltip."""
        self.module_title.setText(title)
        self.module_title.setToolTip(title)
        self.module_title.setAccessibleName(title)

    def set_progress(self, summary: str) -> None:
        """Update the selected-module progress summary."""
        self.progress_summary.setText(summary)
        self.progress_summary.setToolTip(summary)

    def open_information(self) -> None:
        """Show or raise the non-modal course-information dialog."""
        if self._information_dialog is None:
            self._information_dialog = CourseInformationDialog(
                self._information,
                locale=self._locale,
                parent=self,
            )
            self._information_dialog.finished.connect(self._restore_information_focus)
        self._information_dialog.show()
        self._information_dialog.raise_()
        self._information_dialog.activateWindow()

    def _restore_information_focus(self) -> None:
        self.information_button.setFocus(Qt.FocusReason.OtherFocusReason)


def course_information_from_source(
    course: CourseContent,
    locale: AppLocale,
) -> CourseInformation:
    """Adapt heterogeneous source metadata to one safe reader-facing model."""
    locale_code = {
        AppLocale.SPANISH_SPAIN: "es",
        AppLocale.ENGLISH: "en",
        AppLocale.DANISH_DENMARK: "da",
    }[locale]
    raw = course.raw
    metadata = _mapping(raw.get("metadata"))
    identity = _mapping(raw.get("identity"))
    identity_source = metadata or identity

    ects_value = identity_source.get("ects", "")
    assessment = _text_values(metadata.get("assessment"), locale_code)
    if not assessment:
        assessment_strategy = _mapping(raw.get("assessment_strategy"))
        assessment = _text_values(
            assessment_strategy.get("cumulative_assessment"),
            locale_code,
        )

    precondition_source = _mapping(raw.get("academic_preconditions", raw.get("prerequisites")))
    prerequisites = tuple(
        value
        for key in ("required", "recommended")
        for value in _text_values(precondition_source.get(key), locale_code)
    )

    connections = tuple(
        target
        for item in _mapping_items(raw.get("cross_course_bridges"))
        for target in _text_values(item.get("target_course"), locale_code)
    )

    return CourseInformation(
        title=course.title.resolve(locale_code),
        description=course.summary.resolve(locale_code),
        outcomes=tuple(
            outcome.statement.resolve(locale_code) for outcome in course.learning_outcomes
        ),
        ects=str(ects_value).strip(),
        assessment=assessment,
        prerequisites=prerequisites,
        connections=connections,
    )


def _mapping(value: object) -> Mapping[str, Any]:
    return value if isinstance(value, Mapping) else {}


def _mapping_items(value: object) -> tuple[Mapping[str, Any], ...]:
    if not isinstance(value, Sequence) or isinstance(value, (str, bytes)):
        return ()
    return tuple(item for item in value if isinstance(item, Mapping))


def _text_values(value: object, locale: str) -> tuple[str, ...]:
    localized = localize_value(value, locale)
    if isinstance(localized, str):
        return (localized.strip(),) if localized.strip() else ()
    if isinstance(localized, Sequence) and not isinstance(localized, (str, bytes)):
        return tuple(str(item).strip() for item in localized if str(item).strip())
    return ()


__all__ = [
    "CourseInformation",
    "CourseInformationDialog",
    "CourseModuleToolbar",
    "course_information_from_source",
]
