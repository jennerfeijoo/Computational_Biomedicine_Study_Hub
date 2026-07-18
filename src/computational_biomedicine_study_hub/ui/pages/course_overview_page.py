"""Reusable course landing components without imposing a shared module structure."""

from __future__ import annotations

from collections.abc import Sequence

from PySide6.QtCore import Qt
from PySide6.QtWidgets import QFrame, QLabel, QVBoxLayout, QWidget

from ...i18n import AppLocale, DEFAULT_LOCALE, UiCopyKey, ui_text


class CourseOverviewPage(QWidget):
    """Present course identity and the sections planned for its own implementation."""

    def __init__(
        self,
        *,
        code: str,
        ects: int,
        summary: str,
        planned_sections: Sequence[str],
        locale: AppLocale = DEFAULT_LOCALE,
        parent: QWidget | None = None,
    ) -> None:
        super().__init__(parent)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(16)

        identity = QFrame()
        identity.setObjectName("courseIdentityCard")
        identity_layout = QVBoxLayout(identity)
        identity_layout.setContentsMargins(20, 18, 20, 18)
        identity_layout.setSpacing(7)

        code_label = QLabel(f"{code} · {ects} ECTS")
        code_label.setObjectName("courseCode")
        identity_layout.addWidget(code_label)

        summary_label = QLabel(summary)
        summary_label.setObjectName("courseSummary")
        summary_label.setWordWrap(True)
        identity_layout.addWidget(summary_label)
        layout.addWidget(identity)

        section_heading = QLabel(ui_text(locale, UiCopyKey.COURSE_STRUCTURE_HEADING))
        section_heading.setObjectName("sectionHeading")
        layout.addWidget(section_heading)

        section_list = QLabel("\n".join(f"• {section}" for section in planned_sections))
        section_list.setObjectName("courseSectionList")
        section_list.setAlignment(Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignLeft)
        section_list.setWordWrap(True)
        layout.addWidget(section_list)

        notice = QLabel(ui_text(locale, UiCopyKey.COURSE_STRUCTURE_NOTICE))
        notice.setObjectName("courseNotice")
        notice.setWordWrap(True)
        layout.addWidget(notice)
        layout.addStretch(1)
