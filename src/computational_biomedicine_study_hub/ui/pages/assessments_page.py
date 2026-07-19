"""Functional cross-course assessments page."""

from __future__ import annotations

import json
import random
import uuid
from dataclasses import replace
from datetime import UTC, datetime
from functools import partial

from PySide6.QtCore import Slot
from PySide6.QtWidgets import (
    QComboBox,
    QFrame,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QScrollArea,
    QVBoxLayout,
    QWidget,
)

from ...content.models import AssessmentItem
from ...i18n import DEFAULT_LOCALE, AppLocale
from ...learning.academic_catalog import AcademicCatalog, CatalogModule
from ...learning.activity_submission import ActivitySubmission
from ...learning.activity_types import ActivityType
from ...learning.progress import (
    AssessmentScope,
    AssessmentSession,
    AttemptOutcome,
    AttemptRecord,
    LearningItemKind,
    MasteryState,
    ReviewSchedule,
)
from ...learning.progress_repository import ProgressRepository
from ...learning.spaced_repetition import ReviewRating, reschedule
from ..activities import (
    ActivityRendererRegistry,
    ActivityWidget,
    create_default_activity_registry,
)
from ..learning_page_copy import LearningPageCopyKey, learning_text


class AssessmentsPage(QWidget):
    """Compose authored module assessments into persistent interactive sessions."""

    def __init__(
        self,
        catalog: AcademicCatalog,
        repository: ProgressRepository,
        *,
        locale: AppLocale = DEFAULT_LOCALE,
        registry: ActivityRendererRegistry | None = None,
        parent: QWidget | None = None,
    ) -> None:
        super().__init__(parent)
        self.setObjectName("assessmentsPage")
        self._catalog = catalog
        self._repository = repository
        self._locale = locale
        self._registry = registry or create_default_activity_registry()
        self._session: AssessmentSession | None = None
        self._rendered: list[ActivityWidget] = []
        self._context_by_item_id: dict[str, CatalogModule] = {}

        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        filters = QFrame()
        filters.setObjectName("learningFilters")
        filter_layout = QHBoxLayout(filters)
        self.course_selector = self._combo(
            "assessmentCourseSelector",
            learning_text(locale, LearningPageCopyKey.COURSE),
        )
        for course_code in catalog.course_codes:
            self.course_selector.addItem(course_code, course_code)
        self.module_selector = self._combo(
            "assessmentModuleSelector",
            learning_text(locale, LearningPageCopyKey.MODULE),
        )
        self.mode_selector = self._combo(
            "assessmentModeSelector",
            learning_text(locale, LearningPageCopyKey.ASSESSMENT_MODE),
        )
        for key, scope in (
            (LearningPageCopyKey.QUICK_MODULE, AssessmentScope.QUICK_MODULE),
            (LearningPageCopyKey.COMPLETE_MODULE, AssessmentScope.COMPLETE_MODULE),
            (LearningPageCopyKey.COURSE_ASSESSMENT, AssessmentScope.COURSE),
            (LearningPageCopyKey.MIXED_ASSESSMENT, AssessmentScope.MIXED),
        ):
            self.mode_selector.addItem(learning_text(locale, key), scope.value)
        self.type_selector = self._combo(
            "assessmentTypeSelector",
            learning_text(locale, LearningPageCopyKey.TYPE),
        )
        self.type_selector.addItem(learning_text(locale, LearningPageCopyKey.ALL_TYPES), None)
        for activity_type in ActivityType:
            self.type_selector.addItem(
                activity_type.value.replace("_", " ").capitalize(),
                activity_type.value,
            )
        self.start_button = QPushButton(learning_text(locale, LearningPageCopyKey.START_ASSESSMENT))
        self.start_button.setObjectName("startAssessmentButton")
        self.start_button.setAccessibleName(self.start_button.text())
        self.start_button.clicked.connect(self.start_session)
        for widget in (
            self.course_selector,
            self.module_selector,
            self.mode_selector,
            self.type_selector,
            self.start_button,
        ):
            filter_layout.addWidget(widget)
        layout.addWidget(filters)

        self.progress_label = QLabel()
        self.progress_label.setObjectName("assessmentSessionProgress")
        self.progress_label.setWordWrap(True)
        layout.addWidget(self.progress_label)

        self._body = QWidget()
        self._body.setObjectName("assessmentSessionBody")
        self._body_layout = QVBoxLayout(self._body)
        self._body_layout.setContentsMargins(4, 8, 12, 12)
        self._body_layout.setSpacing(12)
        scroll = QScrollArea()
        scroll.setObjectName("assessmentsScroll")
        scroll.setWidgetResizable(True)
        scroll.setWidget(self._body)
        layout.addWidget(scroll, 1)

        self.course_selector.currentIndexChanged.connect(self._refresh_modules)
        self._refresh_modules()
        if not self._restore_latest_open_session():
            self._show_empty(LearningPageCopyKey.ASSESSMENT_EMPTY)

    @property
    def rendered_activities(self) -> tuple[ActivityWidget, ...]:
        return tuple(self._rendered)

    @property
    def session(self) -> AssessmentSession | None:
        return self._session

    @Slot()
    def start_session(self) -> None:
        scope = AssessmentScope(str(self.mode_selector.currentData()))
        records = self._records_for_scope(scope)
        activity_value = self.type_selector.currentData()
        if isinstance(activity_value, str):
            activity_type = ActivityType(activity_value)
            records = tuple(
                (record, item) for record, item in records if item.activity_type is activity_type
            )
        if not records:
            self._session = None
            self._show_empty(LearningPageCopyKey.ASSESSMENT_EMPTY)
            return

        seed = random.SystemRandom().randrange(0, 2**63)
        rng = random.Random(seed)
        values = list(records)
        rng.shuffle(values)
        if scope is AssessmentScope.QUICK_MODULE:
            values = values[: min(6, len(values))]
        elif scope in {AssessmentScope.COURSE, AssessmentScope.MIXED}:
            values = values[: min(20, len(values))]

        course_code = str(self.course_selector.currentData())
        module_id = (
            str(self.module_selector.currentData())
            if scope in {AssessmentScope.QUICK_MODULE, AssessmentScope.COMPLETE_MODULE}
            else ""
        )
        session = AssessmentSession(
            session_id=str(uuid.uuid4()),
            scope=scope,
            course_code=course_code,
            module_id=module_id,
            item_ids=tuple(item.item_id for _, item in values),
            seed=seed,
            locale=self._locale.value,
            started_at=datetime.now(UTC),
        )
        self._repository.save_assessment_session(session)
        self._render_session(session, tuple(values))

    def _records_for_scope(
        self,
        scope: AssessmentScope,
    ) -> tuple[tuple[CatalogModule, AssessmentItem], ...]:
        selected_course = str(self.course_selector.currentData())
        selected_module = str(self.module_selector.currentData())
        if scope in {AssessmentScope.QUICK_MODULE, AssessmentScope.COMPLETE_MODULE}:
            records: tuple[CatalogModule, ...] = (
                self._catalog.module(selected_course, selected_module),
            )
        elif scope is AssessmentScope.COURSE:
            records = self._catalog.modules(selected_course)
        else:
            records = self._catalog.modules()
        return tuple(
            (record, item) for record in records for item in record.module.assessment_items
        )

    def _render_session(
        self,
        session: AssessmentSession,
        records: tuple[tuple[CatalogModule, AssessmentItem], ...],
    ) -> None:
        self._clear_body()
        self._session = session
        self._context_by_item_id = {item.item_id: record for record, item in records}
        item_by_id = {item.item_id: item for _, item in records}
        for item_id in session.item_ids:
            item = item_by_id[item_id]
            record = self._context_by_item_id[item_id]
            widget = self._registry.render(item, locale=self._locale)
            widget.setProperty("moduleId", record.module_id)
            widget.setProperty("contentVersion", record.bundle.content_version)
            widget.submitted.connect(partial(self._record_submission, record, item))
            if item_id in session.answered_item_ids:
                widget.setProperty("answerPersisted", True)
            self._rendered.append(widget)
            self._body_layout.addWidget(widget)
        self._body_layout.addStretch(1)
        self._update_progress()

    @Slot(object)
    def _record_submission(
        self,
        record: CatalogModule,
        item: AssessmentItem,
        submission: object,
    ) -> None:
        if not isinstance(submission, ActivitySubmission) or self._session is None:
            return
        keyed_response = (
            json.dumps(dict(submission.keyed_option_ids), ensure_ascii=False)
            if submission.keyed_option_ids
            else submission.response_text
        )
        self._repository.record_attempt(
            AttemptRecord(
                attempt_id=str(uuid.uuid4()),
                course_code=record.course_code,
                module_id=record.module_id,
                item_id=item.item_id,
                item_kind=LearningItemKind.ASSESSMENT,
                activity_type=item.activity_type,
                outcome=submission.outcome,
                locale=self._locale.value,
                content_version=record.bundle.content_version,
                created_at=datetime.now(UTC),
                response_text=keyed_response,
                selected_option_ids=submission.selected_option_ids,
                is_correct=submission.is_correct,
                score=submission.score,
                session_id=self._session.session_id,
            )
        )
        self._schedule_review(record, item, submission)

        if item.item_id not in self._session.answered_item_ids:
            answered = self._session.answered_item_ids + (item.item_id,)
            correct = self._session.correct_count + int(submission.is_correct is True)
            completed = datetime.now(UTC) if len(answered) == len(self._session.item_ids) else None
            self._session = replace(
                self._session,
                answered_item_ids=answered,
                correct_count=correct,
                completed_at=completed,
            )
            self._repository.save_assessment_session(self._session)
        self._update_progress(saved=True)

    def _schedule_review(
        self,
        record: CatalogModule,
        item: AssessmentItem,
        submission: ActivitySubmission,
    ) -> None:
        now = datetime.now(UTC)
        initial = ReviewSchedule(
            course_code=record.course_code,
            module_id=record.module_id,
            item_id=item.item_id,
            item_kind=LearningItemKind.ASSESSMENT,
            mastery_state=MasteryState.NEW,
            repetitions=0,
            interval_days=0,
            easiness=2.5,
            due_at=now,
        )
        if submission.is_correct is True or submission.outcome is AttemptOutcome.SOLVED:
            self._repository.save_review_schedule(
                reschedule(initial, ReviewRating.GOOD, reviewed_at=now)
            )
            return
        self._repository.save_review_schedule(
            replace(
                initial,
                mastery_state=MasteryState.LEARNING,
                easiness=(2.35 if submission.outcome is AttemptOutcome.PARTIAL else 2.3),
            )
        )

    def _restore_latest_open_session(self) -> bool:
        candidates = tuple(
            session
            for record in self._catalog.modules()
            if (
                session := self._repository.latest_open_assessment_session(
                    course_code=record.course_code,
                    module_id=record.module_id,
                )
            )
            is not None
        )
        if not candidates:
            return False
        session = max(candidates, key=lambda value: value.started_at)
        records = tuple(
            (record, item)
            for record in self._catalog.modules()
            for item in record.module.assessment_items
            if item.item_id in session.item_ids
        )
        if len(records) != len(session.item_ids):
            return False
        course_index = self.course_selector.findData(session.course_code)
        if course_index >= 0:
            self.course_selector.setCurrentIndex(course_index)
        module_index = self.module_selector.findData(session.module_id)
        if module_index >= 0:
            self.module_selector.setCurrentIndex(module_index)
        mode_index = self.mode_selector.findData(session.scope.value)
        if mode_index >= 0:
            self.mode_selector.setCurrentIndex(mode_index)
        self._render_session(session, records)
        return True

    @Slot()
    def _refresh_modules(self) -> None:
        selected_course = self.course_selector.currentData()
        self.module_selector.clear()
        if isinstance(selected_course, str):
            for record in self._catalog.modules(selected_course):
                self.module_selector.addItem(record.title, record.module_id)

    def _update_progress(self, *, saved: bool = False) -> None:
        if self._session is None:
            self.progress_label.clear()
            return
        text = learning_text(
            self._locale,
            LearningPageCopyKey.SESSION_PROGRESS,
            answered=len(self._session.answered_item_ids),
            total=len(self._session.item_ids),
            correct=self._session.correct_count,
        )
        if saved:
            text += " · " + learning_text(
                self._locale,
                LearningPageCopyKey.RESULT_SAVED,
            )
        self.progress_label.setText(text)

    def _show_empty(self, key: LearningPageCopyKey) -> None:
        self._clear_body()
        label = QLabel(learning_text(self._locale, key))
        label.setObjectName("assessmentEmptyState")
        label.setWordWrap(True)
        self._body_layout.addWidget(label)
        self._body_layout.addStretch(1)

    def _clear_body(self) -> None:
        self._rendered.clear()
        while self._body_layout.count():
            item = self._body_layout.takeAt(0)
            if item is None:
                break
            widget = item.widget()
            if widget is not None:
                widget.setParent(None)
                widget.deleteLater()

    @staticmethod
    def _combo(object_name: str, accessible_name: str) -> QComboBox:
        combo = QComboBox()
        combo.setObjectName(object_name)
        combo.setAccessibleName(accessible_name)
        combo.setMinimumWidth(150)
        return combo


__all__ = ["AssessmentsPage"]
