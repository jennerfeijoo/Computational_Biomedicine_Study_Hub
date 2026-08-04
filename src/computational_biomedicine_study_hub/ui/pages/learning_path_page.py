"""Evidence-driven next-action dashboard for all registered first-semester courses."""

from __future__ import annotations

from datetime import UTC, datetime

from PySide6.QtCore import Signal, Slot
from PySide6.QtWidgets import (
    QFrame,
    QGridLayout,
    QLabel,
    QPushButton,
    QScrollArea,
    QVBoxLayout,
    QWidget,
)

from ...courses import COURSES
from ...i18n.learning_path_copy import (
    LearningPathCopyKey,
    learning_path_text,
    learning_reason_text,
    learning_stage_text,
)
from ...i18n.locales import DEFAULT_LOCALE, AppLocale
from ...learning.pathway import (
    LearningPathEngine,
    LearningPathRecommendation,
    LearningPathSnapshot,
)
from ...storage.sqlite_progress_store import SQLiteProgressStore
from ..assessment_registry import ASSESSMENT_REGISTRATIONS


class LearningPathPage(QWidget):
    """Render deterministic recommendations and emit stable navigation targets."""

    destination_requested = Signal(str, str, int, str)

    def __init__(
        self,
        progress_store: SQLiteProgressStore | None,
        locale: AppLocale = DEFAULT_LOCALE,
        *,
        engine: LearningPathEngine | None = None,
        assessment_ids: tuple[str, ...] | None = None,
        parent: QWidget | None = None,
    ) -> None:
        super().__init__(parent)
        self.setObjectName("learningPathPage")
        self._progress_store = progress_store
        self._locale = locale
        self._engine = engine or LearningPathEngine()
        self._assessment_ids = assessment_ids or tuple(
            item.assessment_id for item in ASSESSMENT_REGISTRATIONS
        )
        self._course_titles = {
            course.code: course.title_for(locale) for course in COURSES
        }
        self._snapshot: LearningPathSnapshot | None = None

        root = QVBoxLayout(self)
        root.setContentsMargins(0, 0, 0, 0)

        scroll = QScrollArea()
        scroll.setObjectName("learningPathScroll")
        scroll.setWidgetResizable(True)
        body = QWidget()
        body.setObjectName("learningPathBody")
        self._layout = QVBoxLayout(body)
        self._layout.setContentsMargins(4, 4, 12, 24)
        self._layout.setSpacing(14)

        title = QLabel(self._text(LearningPathCopyKey.PAGE_TITLE))
        title.setObjectName("learningPathTitle")
        self._layout.addWidget(title)

        intro = QLabel(self._text(LearningPathCopyKey.INTRO))
        intro.setObjectName("learningPathIntro")
        intro.setWordWrap(True)
        self._layout.addWidget(intro)

        self._due_heading = QLabel(self._text(LearningPathCopyKey.DUE_TITLE))
        self._due_heading.setObjectName("learningPathSectionHeading")
        self._layout.addWidget(self._due_heading)

        self._due_container = QWidget()
        self._due_layout = QVBoxLayout(self._due_container)
        self._due_layout.setContentsMargins(0, 0, 0, 0)
        self._layout.addWidget(self._due_container)

        course_heading = QLabel(self._text(LearningPathCopyKey.COURSE_TITLE))
        course_heading.setObjectName("learningPathSectionHeading")
        self._layout.addWidget(course_heading)

        self._course_container = QWidget()
        self._course_grid = QGridLayout(self._course_container)
        self._course_grid.setContentsMargins(0, 0, 0, 0)
        self._course_grid.setHorizontalSpacing(14)
        self._course_grid.setVerticalSpacing(14)
        self._layout.addWidget(self._course_container)
        self._layout.addStretch(1)

        scroll.setWidget(body)
        root.addWidget(scroll)
        self.refresh()

    @property
    def snapshot(self) -> LearningPathSnapshot:
        """Return the latest deterministic recommendation snapshot."""

        if self._snapshot is None:
            raise RuntimeError("Learning-path recommendations have not been generated.")
        return self._snapshot

    @Slot()
    def refresh(self) -> None:
        """Recompute recommendations from current local learning evidence."""

        self._snapshot = self._engine.snapshot(
            self._progress_store,
            as_of=datetime.now(UTC),
            assessment_ids=self._assessment_ids,
        )
        self._render_due(self._snapshot)
        self._render_courses(self._snapshot)

    def _render_due(self, snapshot: LearningPathSnapshot) -> None:
        self._clear_layout(self._due_layout)
        recommendation = snapshot.due_review
        if recommendation is None:
            label = QLabel(self._text(LearningPathCopyKey.NO_DUE))
            label.setObjectName("learningPathNoDue")
            label.setWordWrap(True)
            self._due_layout.addWidget(label)
            return
        self._due_layout.addWidget(
            self._recommendation_card(
                recommendation,
                f"{recommendation.course_code} · {recommendation.module_id or ''}".rstrip(),
            )
        )

    def _render_courses(self, snapshot: LearningPathSnapshot) -> None:
        self._clear_layout(self._course_grid)
        for index, recommendation in enumerate(snapshot.course_recommendations):
            title = self._course_titles.get(
                recommendation.course_code,
                recommendation.course_code,
            )
            self._course_grid.addWidget(
                self._recommendation_card(recommendation, title),
                index // 2,
                index % 2,
            )

    def _recommendation_card(
        self,
        recommendation: LearningPathRecommendation,
        title_text: str,
    ) -> QFrame:
        card = QFrame()
        card.setObjectName("learningPathCard")
        layout = QVBoxLayout(card)
        layout.setContentsMargins(16, 16, 16, 16)
        layout.setSpacing(8)

        course = QLabel(f"{recommendation.course_code} · {title_text}")
        course.setObjectName("learningPathCourse")
        course.setWordWrap(True)
        layout.addWidget(course)

        stage = QLabel(learning_stage_text(self._locale, recommendation.stage))
        stage.setObjectName("learningPathStage")
        stage.setWordWrap(True)
        layout.addWidget(stage)

        if recommendation.module_id is not None:
            module = QLabel(recommendation.module_id)
            module.setObjectName("learningPathModule")
            layout.addWidget(module)

        reason = QLabel(learning_reason_text(self._locale, recommendation.reason))
        reason.setObjectName("learningPathReason")
        reason.setWordWrap(True)
        layout.addWidget(reason)

        mastery = QLabel(
            self._text(
                LearningPathCopyKey.MASTERY,
                percent=round(100 * recommendation.mastery_ratio),
            )
        )
        mastery.setObjectName("learningPathMastery")
        layout.addWidget(mastery)

        objectives = QLabel(
            self._text(
                LearningPathCopyKey.OBJECTIVES,
                count=len(recommendation.objective_ids),
            )
        )
        objectives.setObjectName("learningPathObjectives")
        layout.addWidget(objectives)
        layout.addStretch(1)

        open_button = QPushButton(self._text(LearningPathCopyKey.OPEN))
        open_button.setObjectName("learningPathOpenButton")
        open_button.clicked.connect(
            lambda checked=False, item=recommendation: self._emit_destination(item)
        )
        layout.addWidget(open_button)
        return card

    def _emit_destination(self, recommendation: LearningPathRecommendation) -> None:
        destination = recommendation.destination
        self.destination_requested.emit(
            destination.route,
            destination.module_id or "",
            destination.section_index if destination.section_index is not None else -1,
            destination.assessment_id or "",
        )

    def _text(self, key: LearningPathCopyKey, **values: object) -> str:
        return learning_path_text(self._locale, key, **values)

    @staticmethod
    def _clear_layout(layout: QVBoxLayout | QGridLayout) -> None:
        while layout.count():
            item = layout.takeAt(0)
            if item is None:
                break
            widget = item.widget()
            if widget is not None:
                widget.setParent(None)
                widget.deleteLater()


__all__ = ["LearningPathPage"]
