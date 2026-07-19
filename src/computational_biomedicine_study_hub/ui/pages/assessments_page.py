"""Functional cross-course assessments page."""

from __future__ import annotations

import json
import random
import uuid
from dataclasses import replace
from datetime import UTC, datetime
from functools import partial

from PySide6.QtCore import Signal, Slot
from PySide6.QtWidgets import (
    QComboBox,
    QFrame,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QScrollArea,
    QTextBrowser,
    QVBoxLayout,
    QWidget,
)

from ...content.models import AssessmentItem
from ...courses import COURSES
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
    OpenResponseAttempt,
    OpenResponseDraft,
    ReviewSchedule,
)
from ...learning.progress_repository import ProgressRepository
from ...learning.spaced_repetition import ReviewRating, reschedule
from ..activities import (
    ActivityRendererRegistry,
    ActivityWidget,
    OpenResponseActivityWidget,
    create_default_activity_registry,
)
from ..cumulative_assessment_renderer import CumulativeAssessmentRenderer
from ..learning_page_copy import LearningPageCopyKey, learning_text


class AssessmentsPage(QWidget):
    """Compose authored module assessments into persistent interactive sessions."""

    open_feedback_requested = Signal(str, str, str, str, str)

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
            course = next((item for item in COURSES if item.code == course_code), None)
            title = course.title_for(locale) if course is not None else course_code
            self.course_selector.addItem(title, course_code)
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
        self.category_selector = self._combo(
            "assessmentCategorySelector",
            learning_text(locale, LearningPageCopyKey.ASSESSMENT_CATEGORY),
        )
        for key, value in (
            (LearningPageCopyKey.OBJECTIVE_ASSESSMENTS, "objective"),
            (LearningPageCopyKey.OPEN_RESPONSES, "open"),
            (LearningPageCopyKey.CUMULATIVE_ASSESSMENTS, "cumulative"),
        ):
            self.category_selector.addItem(learning_text(locale, key), value)
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
        self.save_drafts_button = QPushButton(
            learning_text(locale, LearningPageCopyKey.SAVE_DRAFTS)
        )
        self.save_drafts_button.setObjectName("saveOpenResponseDraftsButton")
        self.save_drafts_button.clicked.connect(self.save_drafts)
        for widget in (
            self.course_selector,
            self.module_selector,
            self.mode_selector,
            self.category_selector,
            self.type_selector,
            self.start_button,
            self.save_drafts_button,
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
        self.category_selector.currentIndexChanged.connect(self._category_changed)
        self._refresh_modules()
        self._category_changed()
        if not self._restore_latest_open_session():
            self._show_empty(LearningPageCopyKey.ASSESSMENT_EMPTY)

    @property
    def rendered_activities(self) -> tuple[ActivityWidget, ...]:
        return tuple(self._rendered)

    @property
    def session(self) -> AssessmentSession | None:
        return self._session

    def show_cumulative_assessment(self, course_code: str) -> bool:
        """Select and render a course cumulative by stable course identity."""
        course_index = self.course_selector.findData(course_code.upper())
        category_index = self.category_selector.findData("cumulative")
        if course_index < 0 or category_index < 0:
            return False
        self.course_selector.setCurrentIndex(course_index)
        self.category_selector.setCurrentIndex(category_index)
        self.start_session()
        return self._catalog.source_course(course_code).cumulative_assessment is not None

    def show_module_assessments(self, course_code: str, module_id: str) -> bool:
        """Select objective assessment practice for one stable module identity."""
        course_index = self.course_selector.findData(course_code.upper())
        category_index = self.category_selector.findData("objective")
        if course_index < 0 or category_index < 0:
            return False
        self.course_selector.setCurrentIndex(course_index)
        module_index = self.module_selector.findData(module_id)
        if module_index < 0:
            return False
        self.module_selector.setCurrentIndex(module_index)
        self.category_selector.setCurrentIndex(category_index)
        return True

    @Slot()
    def start_session(self) -> None:
        if self.category_selector.currentData() == "cumulative":
            self._render_cumulative()
            return
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
            (record, item)
            for record in records
            for item in (
                record.assessment_items
                if self.category_selector.currentData() == "open"
                else record.objective_question_bank
            )
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
            if isinstance(widget, OpenResponseActivityWidget):
                draft = self._repository.get_open_response_draft(
                    record.course_code,
                    record.module_id,
                    item.item_id,
                    self._locale.value,
                )
                if draft is not None:
                    widget.answer_editor.setPlainText(draft.response_text)
                widget.feedback_requested.connect(
                    partial(self._request_open_feedback, record, item, widget)
                )
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
        open_widget = next(
            (
                candidate
                for candidate in self._rendered
                if candidate.item_id == item.item_id
                and isinstance(candidate, OpenResponseActivityWidget)
            ),
            None,
        )
        if open_widget is not None:
            previous = self._repository.list_open_response_attempts(
                course_code=record.course_code,
                module_id=record.module_id,
                item_id=item.item_id,
            )
            self._repository.record_open_response_attempt(
                OpenResponseAttempt(
                    attempt_id=str(uuid.uuid4()),
                    item_id=item.item_id,
                    course_code=record.course_code,
                    module_id=record.module_id,
                    locale=self._locale.value,
                    confidence=open_widget.confidence,
                    response_text=submission.response_text,
                    version=len(previous) + 1,
                    created_at=datetime.now(UTC),
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
        identities = {
            (record.course_code, record.module_id) for record in self._catalog.modules()
        } | {(course_code, "") for course_code in self._catalog.course_codes}
        candidates = tuple(
            session
            for course_code, module_id in identities
            if (
                session := self._repository.latest_open_assessment_session(
                    course_code=course_code,
                    module_id=module_id,
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
            for item in record.assessment_items + record.objective_question_bank
            if item.item_id in session.item_ids
        )
        if len(records) != len(session.item_ids):
            return False
        open_item_ids = {
            item.item_id for record in self._catalog.modules() for item in record.assessment_items
        }
        category = (
            "open" if all(item.item_id in open_item_ids for _, item in records) else "objective"
        )
        category_index = self.category_selector.findData(category)
        if category_index >= 0:
            self.category_selector.setCurrentIndex(category_index)
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
    def save_drafts(self) -> None:
        saved = 0
        now = datetime.now(UTC)
        for widget in self._rendered:
            if not isinstance(widget, OpenResponseActivityWidget):
                continue
            record = self._context_by_item_id[widget.item_id]
            self._repository.save_open_response_draft(
                OpenResponseDraft(
                    course_code=record.course_code,
                    module_id=record.module_id,
                    item_id=widget.item_id,
                    locale=self._locale.value,
                    response_text=widget.answer_editor.toPlainText(),
                    updated_at=now,
                )
            )
            saved += 1
        if saved:
            self.progress_label.setText(
                learning_text(self._locale, LearningPageCopyKey.DRAFTS_SAVED)
            )

    def _request_open_feedback(
        self,
        record: CatalogModule,
        item: AssessmentItem,
        widget: OpenResponseActivityWidget,
        answer: str,
    ) -> None:
        self._repository.save_open_response_draft(
            OpenResponseDraft(
                course_code=record.course_code,
                module_id=record.module_id,
                item_id=item.item_id,
                locale=self._locale.value,
                response_text=answer,
                updated_at=datetime.now(UTC),
            )
        )
        previous = self._repository.list_open_response_attempts(
            course_code=record.course_code,
            module_id=record.module_id,
            item_id=item.item_id,
        )
        self._repository.record_open_response_attempt(
            OpenResponseAttempt(
                attempt_id=str(uuid.uuid4()),
                item_id=item.item_id,
                course_code=record.course_code,
                module_id=record.module_id,
                locale=self._locale.value,
                confidence=widget.confidence,
                response_text=answer,
                version=len(previous) + 1,
                created_at=datetime.now(UTC),
            )
        )
        self.open_feedback_requested.emit(
            record.course_code,
            record.module_id,
            item.item_id,
            answer,
            widget.confidence,
        )

    @Slot()
    def _category_changed(self) -> None:
        category = self.category_selector.currentData()
        is_cumulative = category == "cumulative"
        self.module_selector.setEnabled(not is_cumulative)
        self.mode_selector.setEnabled(not is_cumulative)
        self.type_selector.setEnabled(not is_cumulative)
        self.save_drafts_button.setVisible(category == "open")

    def _render_cumulative(self) -> None:
        self._clear_body()
        self._session = None
        course_code = str(self.course_selector.currentData())
        if not course_code:
            self._show_empty(LearningPageCopyKey.CUMULATIVE_UNAVAILABLE)
            return
        course = self._catalog.source_course(course_code)
        cumulative = course.cumulative_assessment
        if cumulative is None:
            self._show_empty(LearningPageCopyKey.CUMULATIVE_UNAVAILABLE)
            return
        locale_code = self._locale.value.split("-", 1)[0].split("_", 1)[0]
        registration = next((item for item in COURSES if item.code == course_code), None)
        course_title = (
            registration.title_for(self._locale)
            if registration is not None
            else course.title.resolve(locale_code)
        )
        browser = QTextBrowser()
        browser.setObjectName("cumulativeAssessmentContent")
        browser.setAccessibleName(cumulative.title.resolve(locale_code))
        browser.setOpenExternalLinks(False)
        browser.setHtml(
            CumulativeAssessmentRenderer(
                cumulative,
                course,
                course_title=course_title,
                locale=locale_code,
            ).render_html()
        )
        self._body_layout.addWidget(browser)

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
