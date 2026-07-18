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


class CourseCard(QFrame):
    """Clickable summary card for one registered course."""

    selected = Signal(str)

    def __init__(
        self,
        course: CourseRegistration,
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

        title = QLabel(course.title)
        title.setObjectName("courseCardTitle")
        title.setWordWrap(True)
        layout.addWidget(title)

        metadata = QLabel(f"Semestre {course.semester} · {course.ects} ECTS")
        metadata.setObjectName("courseCardMetadata")
        layout.addWidget(metadata)

        summary = QLabel(course.summary)
        summary.setObjectName("courseCardSummary")
        summary.setWordWrap(True)
        layout.addWidget(summary)
        layout.addStretch(1)

        open_button = QPushButton("Abrir asignatura")
        open_button.setObjectName("courseOpenButton")
        open_button.clicked.connect(
            lambda checked=False, route=course.route: self.selected.emit(route)
        )
        layout.addWidget(open_button)


class HomePage(QWidget):
    """Display the registered courses and emit the selected course route."""

    course_selected = Signal(str)

    def __init__(
        self,
        courses: Iterable[CourseRegistration],
        parent: QWidget | None = None,
    ) -> None:
        super().__init__(parent)
        course_list = tuple(courses)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(16)

        heading = QLabel("Asignaturas del primer semestre")
        heading.setObjectName("sectionHeading")
        layout.addWidget(heading)

        description = QLabel(
            "Selecciona una asignatura para entrar en su espacio independiente. "
            "Cada curso podrá utilizar una estructura de aprendizaje diferente."
        )
        description.setObjectName("homeDescription")
        description.setWordWrap(True)
        layout.addWidget(description)

        grid = QGridLayout()
        grid.setHorizontalSpacing(14)
        grid.setVerticalSpacing(14)

        for index, course in enumerate(course_list):
            card = CourseCard(course)
            card.selected.connect(self.course_selected.emit)
            grid.addWidget(card, index // 2, index % 2)

        layout.addLayout(grid)
        layout.addStretch(1)
