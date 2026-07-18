"""Semester dashboard and course selection page."""

from __future__ import annotations

from collections.abc import Iterable

from PySide6.QtCore import Signal
from PySide6.QtWidgets import (
    QFrame,
    QGridLayout,
    QLabel,
    QPushButton,
    QVBoxLayout,
    QWidget,
)

from ...courses.models import CourseRegistration
from ...i18n import MessageKey, Translator


class CourseCard(QFrame):
    """Clickable localized summary card for one registered course."""

    selected = Signal(str)

    def __init__(
        self,
        course: CourseRegistration,
        translator: Translator,
        parent: QWidget | None = None,
    ) -> None:
        super().__init__(parent)
        self.setObjectName("courseCard")

        layout = QVBoxLayout(self)
        layout.setContentsMargins(18, 18, 18, 18)
        layout.setSpacing(8)

        code = QLabel(course.code)
        code.setObjectName("courseCardCode")
        layout.addWidget(code)

        title = QLabel(course.title_for(translator.locale))
        title.setObjectName("courseCardTitle")
        title.setWordWrap(True)
        layout.addWidget(title)

        metadata = QLabel(
            translator.text(
                MessageKey.COURSE_METADATA,
                semester=course.semester,
                ects=course.ects,
            )
        )
        metadata.setObjectName("courseCardMetadata")
        layout.addWidget(metadata)

        summary = QLabel(course.summary_for(translator.locale))
        summary.setObjectName("courseCardSummary")
        summary.setWordWrap(True)
        layout.addWidget(summary)
        layout.addStretch(1)

        open_button = QPushButton(translator.text(MessageKey.COURSE_OPEN))
        open_button.setObjectName("courseOpenButton")
        open_button.clicked.connect(
            lambda checked=False, route=course.route: self.selected.emit(route)
        )
        layout.addWidget(open_button)


class HomePage(QWidget):
    """Display localized registered courses and emit the selected route."""

    course_selected = Signal(str)

    def __init__(
        self,
        courses: Iterable[CourseRegistration],
        translator: Translator,
        parent: QWidget | None = None,
    ) -> None:
        super().__init__(parent)
        course_list = tuple(courses)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(16)

        heading = QLabel(translator.text(MessageKey.HOME_HEADING))
        heading.setObjectName("sectionHeading")
        layout.addWidget(heading)

        description = QLabel(translator.text(MessageKey.HOME_DESCRIPTION))
        description.setObjectName("homeDescription")
        description.setWordWrap(True)
        layout.addWidget(description)

        grid = QGridLayout()
        grid.setHorizontalSpacing(14)
        grid.setVerticalSpacing(14)

        for index, course in enumerate(course_list):
            card = CourseCard(course, translator)
            card.selected.connect(self.course_selected.emit)
            grid.addWidget(card, index // 2, index % 2)

        layout.addLayout(grid)
        layout.addStretch(1)
