"""Persistent review queue and mastery summary."""

from __future__ import annotations

from datetime import UTC, datetime

from PySide6.QtCore import Qt, Slot
from PySide6.QtWidgets import (
    QCheckBox,
    QComboBox,
    QHBoxLayout,
    QLabel,
    QListWidget,
    QListWidgetItem,
    QPushButton,
    QVBoxLayout,
    QWidget,
)

from ...i18n import DEFAULT_LOCALE, AppLocale
from ...learning.academic_catalog import AcademicCatalog
from ...learning.progress import (
    LearningItemKind,
    MasteryState,
    ReviewSchedule,
)
from ...learning.progress_repository import ProgressRepository
from ...learning.spaced_repetition import ReviewRating, reschedule
from ..learning_page_copy import LearningPageCopyKey, learning_text


class ReviewPage(QWidget):
    """Build and reschedule a filtered queue from persisted learning evidence."""

    def __init__(
        self,
        catalog: AcademicCatalog,
        repository: ProgressRepository,
        *,
        locale: AppLocale = DEFAULT_LOCALE,
        parent: QWidget | None = None,
    ) -> None:
        super().__init__(parent)
        self.setObjectName("reviewPage")
        self._catalog = catalog
        self._repository = repository
        self._locale = locale
        self._queue: tuple[ReviewSchedule, ...] = ()

        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        filters = QHBoxLayout()
        self.mix_courses = QCheckBox(learning_text(locale, LearningPageCopyKey.MIX_COURSES))
        self.mix_courses.setObjectName("reviewMixCourses")
        self.course_selector = QComboBox()
        self.course_selector.setObjectName("reviewCourseSelector")
        for course_code in catalog.course_codes:
            self.course_selector.addItem(course_code, course_code)
        self.module_selector = QComboBox()
        self.module_selector.setObjectName("reviewModuleSelector")
        self.kind_selector = QComboBox()
        self.kind_selector.setObjectName("reviewTypeSelector")
        self.kind_selector.addItem(
            learning_text(locale, LearningPageCopyKey.ALL_TYPES),
            None,
        )
        for kind in LearningItemKind:
            self.kind_selector.addItem(
                kind.value.replace("_", " ").capitalize(),
                kind.value,
            )
        self.start_button = QPushButton(learning_text(locale, LearningPageCopyKey.START_REVIEW))
        self.start_button.setObjectName("startReviewSessionButton")
        self.start_button.clicked.connect(self.refresh_queue)
        self.new_concepts_button = QPushButton(
            learning_text(locale, LearningPageCopyKey.NEW_CONCEPTS)
        )
        self.new_concepts_button.setObjectName("addNewConceptsButton")
        self.new_concepts_button.clicked.connect(self.add_new_concepts)
        for widget in (
            self.mix_courses,
            self.course_selector,
            self.module_selector,
            self.kind_selector,
            self.start_button,
            self.new_concepts_button,
        ):
            filters.addWidget(widget)
        layout.addLayout(filters)

        summary = QHBoxLayout()
        self.due_label = QLabel()
        self.due_label.setObjectName("reviewDueCount")
        self.mastery_label = QLabel()
        self.mastery_label.setObjectName("reviewMastery")
        summary.addWidget(self.due_label)
        summary.addWidget(self.mastery_label)
        summary.addStretch(1)
        layout.addLayout(summary)

        self.queue_list = QListWidget()
        self.queue_list.setObjectName("reviewQueue")
        self.queue_list.setAccessibleName("Review queue")
        layout.addWidget(self.queue_list, 1)
        self.empty_label = QLabel(learning_text(locale, LearningPageCopyKey.REVIEW_EMPTY))
        self.empty_label.setObjectName("reviewEmptyState")
        self.empty_label.setWordWrap(True)
        layout.addWidget(self.empty_label)

        ratings = QHBoxLayout()
        self._rating_buttons: list[QPushButton] = []
        for key, rating in (
            (LearningPageCopyKey.AGAIN, ReviewRating.AGAIN),
            (LearningPageCopyKey.HARD, ReviewRating.HARD),
            (LearningPageCopyKey.GOOD, ReviewRating.GOOD),
            (LearningPageCopyKey.EASY, ReviewRating.EASY),
        ):
            button = QPushButton(learning_text(locale, key))
            button.setObjectName(f"reviewRating_{rating.name.casefold()}")
            button.clicked.connect(lambda checked=False, value=rating: self.rate_selected(value))
            self._rating_buttons.append(button)
            ratings.addWidget(button)
        ratings.addStretch(1)
        layout.addLayout(ratings)

        history_title = QLabel(learning_text(locale, LearningPageCopyKey.HISTORY))
        history_title.setObjectName("sectionHeading")
        self.history_label = QLabel()
        self.history_label.setObjectName("reviewHistory")
        self.history_label.setWordWrap(True)
        layout.addWidget(history_title)
        layout.addWidget(self.history_label)

        self.course_selector.currentIndexChanged.connect(self._refresh_modules)
        self.module_selector.currentIndexChanged.connect(self.refresh_queue)
        self.kind_selector.currentIndexChanged.connect(self.refresh_queue)
        self.mix_courses.toggled.connect(self._mix_toggled)
        self._refresh_modules()

    @property
    def queue(self) -> tuple[ReviewSchedule, ...]:
        return self._queue

    @Slot()
    def _refresh_modules(self) -> None:
        course = self.course_selector.currentData()
        self.module_selector.blockSignals(True)
        self.module_selector.clear()
        self.module_selector.addItem(
            learning_text(self._locale, LearningPageCopyKey.ALL_MODULES),
            None,
        )
        if isinstance(course, str):
            for record in self._catalog.modules(course):
                self.module_selector.addItem(record.title, record.module_id)
        self.module_selector.blockSignals(False)
        self.refresh_queue()

    @Slot(bool)
    def _mix_toggled(self, checked: bool) -> None:
        self.course_selector.setEnabled(not checked)
        self.module_selector.setEnabled(not checked)
        self.refresh_queue()

    @Slot()
    def refresh_queue(self) -> None:
        course_value = self.course_selector.currentData()
        module_value = self.module_selector.currentData()
        course_code = (
            None
            if self.mix_courses.isChecked()
            else (course_value if isinstance(course_value, str) else None)
        )
        module_id = (
            None
            if self.mix_courses.isChecked()
            else (module_value if isinstance(module_value, str) else None)
        )
        kind_value = self.kind_selector.currentData()
        due = self._repository.list_due_reviews(
            due_at=datetime.now(UTC),
            course_code=course_code,
            module_id=module_id,
            limit=100,
        )
        if isinstance(kind_value, str):
            kind = LearningItemKind(kind_value)
            due = tuple(item for item in due if item.item_kind is kind)
        self._queue = due
        self.queue_list.clear()
        for index, schedule in enumerate(due):
            row = QListWidgetItem(
                f"{schedule.course_code} · {schedule.module_id} · "
                f"{schedule.item_kind.value} · {schedule.item_id}"
            )
            row.setData(Qt.ItemDataRole.UserRole, index)
            self.queue_list.addItem(row)
        if due:
            self.queue_list.setCurrentRow(0)
        self.empty_label.setVisible(not due)
        for button in self._rating_buttons:
            button.setEnabled(bool(due))
        self.due_label.setText(
            learning_text(
                self._locale,
                LearningPageCopyKey.DUE_COUNT,
                count=len(due),
            )
        )
        self._update_mastery(course_code, module_id)
        self._update_history(course_code, module_id)

    @Slot()
    def add_new_concepts(self) -> None:
        course_value = self.course_selector.currentData()
        module_value = self.module_selector.currentData()
        course_code = (
            None
            if self.mix_courses.isChecked()
            else (course_value if isinstance(course_value, str) else None)
        )
        module_id = (
            None
            if self.mix_courses.isChecked()
            else (module_value if isinstance(module_value, str) else None)
        )
        now = datetime.now(UTC)
        added = 0
        for entry in self._catalog.glossary(course_code=course_code):
            if module_id is not None and entry.module_id != module_id:
                continue
            existing = self._repository.get_review_schedule(
                entry.course_code,
                entry.module_id,
                entry.term_id,
                LearningItemKind.CONCEPT.value,
            )
            if existing is not None:
                continue
            self._repository.save_review_schedule(
                ReviewSchedule(
                    course_code=entry.course_code,
                    module_id=entry.module_id,
                    item_id=entry.term_id,
                    item_kind=LearningItemKind.CONCEPT,
                    mastery_state=MasteryState.NEW,
                    repetitions=0,
                    interval_days=0,
                    easiness=2.5,
                    due_at=now,
                )
            )
            added += 1
            if added >= 10:
                break
        self.refresh_queue()

    def rate_selected(self, rating: ReviewRating) -> None:
        row = self.queue_list.currentRow()
        if not 0 <= row < len(self._queue):
            return
        current = self._queue[row]
        self._repository.save_review_schedule(
            reschedule(current, rating, reviewed_at=datetime.now(UTC))
        )
        self.refresh_queue()

    def _update_mastery(
        self,
        course_code: str | None,
        module_id: str | None,
    ) -> None:
        records = self._catalog.modules(course_code)
        if module_id is not None:
            records = tuple(record for record in records if record.module_id == module_id)
        summaries = tuple(
            self._repository.module_progress(record.course_code, record.module_id)
            for record in records
        )
        attempts = sum(summary.attempt_count for summary in summaries)
        correct = sum(summary.correct_count for summary in summaries)
        percent = round((correct / attempts) * 100) if attempts else 0
        self.mastery_label.setText(
            learning_text(
                self._locale,
                LearningPageCopyKey.MASTERY,
                percent=percent,
            )
        )

    def _update_history(
        self,
        course_code: str | None,
        module_id: str | None,
    ) -> None:
        attempts = self._repository.list_attempts(
            course_code=course_code,
            module_id=module_id,
            limit=8,
        )
        if not attempts:
            self.history_label.setText(learning_text(self._locale, LearningPageCopyKey.EMPTY))
            return
        self.history_label.setText(
            "\n".join(
                f"{attempt.created_at:%Y-%m-%d %H:%M} · {attempt.module_id} · "
                f"{attempt.item_id} · {attempt.outcome.value}"
                for attempt in attempts
            )
        )


__all__ = ["ReviewPage"]
