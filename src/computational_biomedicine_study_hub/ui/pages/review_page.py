"""Functional adaptive review, spaced queue and authored error notebook."""

from __future__ import annotations

from collections.abc import Callable
from datetime import UTC, datetime

from PySide6.QtCore import Signal, Slot
from PySide6.QtWidgets import (
    QFrame,
    QHBoxLayout,
    QLabel,
    QProgressBar,
    QPushButton,
    QScrollArea,
    QTabWidget,
    QVBoxLayout,
    QWidget,
)

from ...i18n import AdaptiveReviewCopyKey, AppLocale, adaptive_review_text
from ...i18n.review_copy import ReviewCopyKey, review_text
from ...learning.adaptive_review import AdaptiveReviewSession
from ...learning.progress import ConfidenceLevel, ErrorKind, ErrorRecord, ReviewItem
from ...learning.progress_service import LearningProgressService
from ...learning.review_catalog import authored_objective_catalog
from ...storage import SQLiteProgressStore
from ..widgets.adaptive_review_session_widget import AdaptiveReviewSessionWidget

Clock = Callable[[], datetime]


def _now_utc() -> datetime:
    return datetime.now(UTC)


class ReviewPage(QWidget):
    """Present an adaptive session, scheduled objectives and persistent errors."""

    review_requested = Signal(str, str, str)

    def __init__(
        self,
        progress_store: SQLiteProgressStore | None,
        locale: AppLocale,
        *,
        clock: Clock | None = None,
        parent: QWidget | None = None,
    ) -> None:
        super().__init__(parent)
        self.setObjectName("reviewPage")
        self._store = progress_store
        self._locale = locale
        self._clock = clock if clock is not None else _now_utc
        self._catalog = authored_objective_catalog(locale)
        self._items: tuple[ReviewItem, ...] = ()
        self._errors: tuple[ErrorRecord, ...] = ()
        self._cards: list[QFrame] = []
        self._error_cards: list[QFrame] = []
        self._pending_session: AdaptiveReviewSession | None = None
        self._session_widget: AdaptiveReviewSessionWidget | None = None

        heading_row = QHBoxLayout()
        heading_row.setContentsMargins(0, 0, 0, 0)
        heading_row.setSpacing(12)

        title = QLabel(review_text(locale, ReviewCopyKey.TITLE))
        title.setObjectName("reviewPageTitle")
        heading_row.addWidget(title, 1)

        refresh_button = QPushButton(review_text(locale, ReviewCopyKey.REFRESH))
        refresh_button.setObjectName("reviewRefreshButton")
        refresh_button.clicked.connect(self.refresh)
        heading_row.addWidget(refresh_button)

        intro = QLabel(review_text(locale, ReviewCopyKey.INTRO))
        intro.setObjectName("reviewPageIntro")
        intro.setWordWrap(True)

        self._tabs = QTabWidget()
        self._tabs.setObjectName("reviewSystemTabs")
        self._tabs.addTab(
            self._build_session_tab(),
            adaptive_review_text(locale, AdaptiveReviewCopyKey.TAB),
        )
        self._tabs.addTab(
            self._build_queue_tab(),
            review_text(locale, ReviewCopyKey.QUEUE_TAB),
        )
        self._tabs.addTab(
            self._build_error_tab(),
            review_text(locale, ReviewCopyKey.ERROR_TAB),
        )

        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(16)
        layout.addLayout(heading_row)
        layout.addWidget(intro)
        layout.addWidget(self._tabs, 1)

        self.refresh()

    @property
    def due_count(self) -> int:
        """Return the number of objectives currently displayed."""

        return len(self._items)

    @property
    def review_items(self) -> tuple[ReviewItem, ...]:
        """Return the current ordered review queue."""

        return self._items

    @property
    def review_cards(self) -> tuple[QFrame, ...]:
        """Expose rendered review cards for deterministic UI testing."""

        return tuple(self._cards)

    @property
    def adaptive_session_widget(self) -> AdaptiveReviewSessionWidget | None:
        """Return the active adaptive session surface, when started."""

        return self._session_widget

    @property
    def pending_session(self) -> AdaptiveReviewSession | None:
        """Return the prepared session used by the launcher."""

        return self._pending_session

    @property
    def error_count(self) -> int:
        """Return the number of retained error events."""

        return len(self._errors)

    @property
    def open_error_count(self) -> int:
        """Return the number of unresolved error events."""

        return sum(not error.is_resolved for error in self._errors)

    @property
    def error_records(self) -> tuple[ErrorRecord, ...]:
        """Return the current ordered error history."""

        return self._errors

    @property
    def error_cards(self) -> tuple[QFrame, ...]:
        """Expose rendered error cards for deterministic UI testing."""

        return tuple(self._error_cards)

    @Slot()
    def refresh(self) -> None:
        """Reload review data and reset any in-memory adaptive session."""

        now = self._clock()
        if now.tzinfo is None or now.utcoffset() is None:
            raise ValueError("Review clock must return a timezone-aware datetime.")

        if self._store is None:
            self._items = ()
            self._errors = ()
        else:
            self._items = self._store.due_reviews(now)
            self._errors = self._store.list_errors()

        self._render_session_launcher()
        self._render_queue(now)
        self._render_error_notebook()

    def _build_session_tab(self) -> QWidget:
        tab = QWidget()
        tab.setObjectName("adaptiveReviewTab")

        title = QLabel(adaptive_review_text(self._locale, AdaptiveReviewCopyKey.TITLE))
        title.setObjectName("adaptiveReviewLauncherTitle")

        intro = QLabel(adaptive_review_text(self._locale, AdaptiveReviewCopyKey.INTRO))
        intro.setObjectName("adaptiveReviewLauncherIntro")
        intro.setWordWrap(True)

        self._session_status = QLabel()
        self._session_status.setObjectName("adaptiveReviewLauncherStatus")
        self._session_status.setWordWrap(True)

        actions = QHBoxLayout()
        actions.setContentsMargins(0, 0, 0, 0)
        actions.addStretch(1)
        self._session_start_button = QPushButton(
            adaptive_review_text(self._locale, AdaptiveReviewCopyKey.START)
        )
        self._session_start_button.setObjectName("adaptiveReviewStartButton")
        self._session_start_button.clicked.connect(self.start_adaptive_session)
        actions.addWidget(self._session_start_button)

        self._session_host = QWidget()
        self._session_host.setObjectName("adaptiveReviewSessionHost")
        self._session_layout = QVBoxLayout(self._session_host)
        self._session_layout.setContentsMargins(0, 0, 0, 0)
        self._session_layout.setSpacing(10)

        layout = QVBoxLayout(tab)
        layout.setContentsMargins(8, 12, 8, 8)
        layout.setSpacing(12)
        layout.addWidget(title)
        layout.addWidget(intro)
        layout.addWidget(self._session_status)
        layout.addLayout(actions)
        layout.addWidget(self._session_host, 1)
        return tab

    def _build_queue_tab(self) -> QWidget:
        tab = QWidget()
        tab.setObjectName("scheduledReviewTab")

        self._count_label = QLabel()
        self._count_label.setObjectName("reviewDueCount")

        self._queue_body = QWidget()
        self._queue_body.setObjectName("reviewQueueBody")
        self._queue_layout = QVBoxLayout(self._queue_body)
        self._queue_layout.setContentsMargins(0, 0, 0, 0)
        self._queue_layout.setSpacing(12)

        scroll = QScrollArea()
        scroll.setObjectName("reviewQueueScroll")
        scroll.setWidgetResizable(True)
        scroll.setFrameShape(QFrame.Shape.NoFrame)
        scroll.setWidget(self._queue_body)

        layout = QVBoxLayout(tab)
        layout.setContentsMargins(8, 12, 8, 8)
        layout.setSpacing(12)
        layout.addWidget(self._count_label)
        layout.addWidget(scroll, 1)
        return tab

    def _build_error_tab(self) -> QWidget:
        tab = QWidget()
        tab.setObjectName("errorNotebookTab")

        self._error_count_label = QLabel()
        self._error_count_label.setObjectName("errorNotebookCount")

        self._error_body = QWidget()
        self._error_body.setObjectName("errorNotebookBody")
        self._error_layout = QVBoxLayout(self._error_body)
        self._error_layout.setContentsMargins(0, 0, 0, 0)
        self._error_layout.setSpacing(12)

        scroll = QScrollArea()
        scroll.setObjectName("errorNotebookScroll")
        scroll.setWidgetResizable(True)
        scroll.setFrameShape(QFrame.Shape.NoFrame)
        scroll.setWidget(self._error_body)

        layout = QVBoxLayout(tab)
        layout.setContentsMargins(8, 12, 8, 8)
        layout.setSpacing(12)
        layout.addWidget(self._error_count_label)
        layout.addWidget(scroll, 1)
        return tab

    def _render_session_launcher(self) -> None:
        self._clear_layout(self._session_layout)
        self._session_widget = None
        self._pending_session = AdaptiveReviewSession(
            self._items,
            locale=self._locale,
            target_questions=6,
        )
        session = self._pending_session
        self._session_start_button.setEnabled(session.can_start)
        self._session_start_button.setText(
            adaptive_review_text(self._locale, AdaptiveReviewCopyKey.START)
        )

        if not self._items:
            self._session_status.setText(
                adaptive_review_text(self._locale, AdaptiveReviewCopyKey.NO_DUE)
            )
            return

        self._session_status.setText(
            adaptive_review_text(
                self._locale,
                AdaptiveReviewCopyKey.DUE_SUMMARY,
                due=len(self._items),
                eligible=session.eligible_objective_count,
                unsupported=len(session.unsupported_keys),
            )
        )
        if not session.can_start:
            unavailable = QLabel(
                adaptive_review_text(self._locale, AdaptiveReviewCopyKey.NO_ELIGIBLE)
            )
            unavailable.setObjectName("adaptiveReviewUnavailable")
            unavailable.setWordWrap(True)
            self._session_layout.addWidget(unavailable)

    @Slot()
    def start_adaptive_session(self) -> None:
        """Replace the launcher body with the prepared adaptive session."""

        session = self._pending_session
        if session is None or not session.can_start:
            return
        self._clear_layout(self._session_layout)
        recorder = LearningProgressService(self._store) if self._store is not None else None
        self._session_widget = AdaptiveReviewSessionWidget(
            session,
            locale=self._locale,
            progress_recorder=recorder,
        )
        self._session_widget.queue_refresh_requested.connect(self.refresh)
        self._session_layout.addWidget(self._session_widget)
        self._session_start_button.setEnabled(False)
        self._session_start_button.setText(
            adaptive_review_text(self._locale, AdaptiveReviewCopyKey.RESTART)
        )

    def _render_queue(self, now: datetime) -> None:
        self._count_label.setText(
            review_text(self._locale, ReviewCopyKey.DUE_COUNT, count=len(self._items))
        )
        self._clear_layout(self._queue_layout)
        self._cards.clear()

        if not self._items:
            self._render_queue_empty_state()
            return

        for item in self._items:
            card = self._build_review_card(item, now)
            self._cards.append(card)
            self._queue_layout.addWidget(card)
        self._queue_layout.addStretch(1)

    def _render_error_notebook(self) -> None:
        self._error_count_label.setText(
            review_text(
                self._locale,
                ReviewCopyKey.ERROR_COUNT,
                open_count=self.open_error_count,
                total_count=self.error_count,
            )
        )
        self._clear_layout(self._error_layout)
        self._error_cards.clear()

        if not self._errors:
            self._render_error_empty_state()
            return

        for error in self._errors:
            card = self._build_error_card(error)
            self._error_cards.append(card)
            self._error_layout.addWidget(card)
        self._error_layout.addStretch(1)

    def _build_review_card(self, item: ReviewItem, now: datetime) -> QFrame:
        descriptor = self._catalog.get(item.key)
        state = item.state

        card = QFrame()
        card.setObjectName("reviewItemCard")
        card.setProperty("courseCode", item.course_code)
        card.setProperty("moduleId", item.module_id)
        card.setProperty("objectiveId", item.objective_id)

        layout = QVBoxLayout(card)
        layout.setContentsMargins(18, 16, 18, 16)
        layout.setSpacing(9)

        module_line = QLabel(
            review_text(
                self._locale,
                ReviewCopyKey.MODULE_LINE,
                course_code=item.course_code,
                module_title=(
                    descriptor.module_title if descriptor is not None else item.module_id
                ),
            )
        )
        module_line.setObjectName("reviewModuleLine")
        layout.addWidget(module_line)

        objective = QLabel(descriptor.statement if descriptor is not None else item.objective_id)
        objective.setObjectName("reviewObjectiveStatement")
        objective.setWordWrap(True)
        layout.addWidget(objective)

        priority = QLabel(review_text(self._locale, self._priority_key(item, now)))
        priority.setObjectName("reviewPriority")
        layout.addWidget(priority)

        mastery_percent = round(state.mastery_score * 100)
        mastery = QProgressBar()
        mastery.setObjectName("reviewMasteryBar")
        mastery.setRange(0, 100)
        mastery.setValue(mastery_percent)
        mastery.setFormat(
            review_text(
                self._locale,
                ReviewCopyKey.MASTERY,
                percent=mastery_percent,
            )
        )
        layout.addWidget(mastery)

        metrics = QHBoxLayout()
        metrics.setContentsMargins(0, 0, 0, 0)
        metrics.setSpacing(14)
        attempts = QLabel(
            review_text(
                self._locale,
                ReviewCopyKey.ATTEMPTS,
                count=state.attempts,
            )
        )
        attempts.setObjectName("reviewAttemptCount")
        metrics.addWidget(attempts)
        lapses = QLabel(
            review_text(
                self._locale,
                ReviewCopyKey.LAPSES,
                count=state.lapse_count,
            )
        )
        lapses.setObjectName("reviewLapseCount")
        metrics.addWidget(lapses)
        metrics.addStretch(1)
        layout.addLayout(metrics)

        due = QLabel(
            review_text(
                self._locale,
                ReviewCopyKey.DUE,
                date=self._format_datetime(state.next_review_at),
            )
        )
        due.setObjectName("reviewDueDate")
        layout.addWidget(due)

        layout.addLayout(
            self._action_row(
                object_name="reviewOpenModuleButton",
                course_code=item.course_code,
                module_id=item.module_id,
                objective_id=item.objective_id,
            )
        )
        return card

    def _build_error_card(self, error: ErrorRecord) -> QFrame:
        first_objective = error.objective_ids[0]
        descriptor = self._catalog.get((error.course_code, error.module_id, first_objective))

        card = QFrame()
        card.setObjectName("errorNotebookCard")
        card.setProperty("errorId", error.error_id)
        card.setProperty("courseCode", error.course_code)
        card.setProperty("moduleId", error.module_id)
        card.setProperty("resolved", error.is_resolved)

        layout = QVBoxLayout(card)
        layout.setContentsMargins(18, 16, 18, 16)
        layout.setSpacing(9)

        module_line = QLabel(
            review_text(
                self._locale,
                ReviewCopyKey.MODULE_LINE,
                course_code=error.course_code,
                module_title=(
                    descriptor.module_title if descriptor is not None else error.module_id
                ),
            )
        )
        module_line.setObjectName("errorModuleLine")
        layout.addWidget(module_line)

        status_row = QHBoxLayout()
        status = QLabel(
            review_text(
                self._locale,
                ReviewCopyKey.ERROR_STATUS_RESOLVED
                if error.is_resolved
                else ReviewCopyKey.ERROR_STATUS_OPEN,
            )
        )
        status.setObjectName("errorStatus")
        status.setProperty("resolved", error.is_resolved)
        status_row.addWidget(status)

        kind = QLabel(review_text(self._locale, self._error_kind_key(error.kind)))
        kind.setObjectName("errorKind")
        status_row.addWidget(kind)
        status_row.addStretch(1)
        layout.addLayout(status_row)

        prompt = QLabel(review_text(self._locale, ReviewCopyKey.ERROR_PROMPT, text=error.prompt))
        prompt.setObjectName("errorPrompt")
        prompt.setWordWrap(True)
        layout.addWidget(prompt)

        selected = QLabel(
            review_text(
                self._locale,
                ReviewCopyKey.ERROR_SELECTED,
                text=error.selected_answer,
            )
        )
        selected.setObjectName("errorSelectedAnswer")
        selected.setWordWrap(True)
        layout.addWidget(selected)

        correct = QLabel(
            review_text(
                self._locale,
                ReviewCopyKey.ERROR_CORRECT,
                text=error.correct_answer,
            )
        )
        correct.setObjectName("errorCorrectAnswer")
        correct.setWordWrap(True)
        layout.addWidget(correct)

        explanation = QLabel(
            review_text(
                self._locale,
                ReviewCopyKey.ERROR_EXPLANATION,
                text=error.explanation,
            )
        )
        explanation.setObjectName("errorExplanation")
        explanation.setWordWrap(True)
        layout.addWidget(explanation)

        confidence = QLabel(
            review_text(
                self._locale,
                ReviewCopyKey.ERROR_CONFIDENCE,
                level=review_text(
                    self._locale,
                    self._confidence_key(error.confidence),
                ),
            )
        )
        confidence.setObjectName("errorConfidence")
        layout.addWidget(confidence)

        objectives = QLabel(
            review_text(
                self._locale,
                ReviewCopyKey.ERROR_OBJECTIVES,
                objectives=", ".join(error.objective_ids),
            )
        )
        objectives.setObjectName("errorObjectives")
        objectives.setWordWrap(True)
        layout.addWidget(objectives)

        occurred = QLabel(
            review_text(
                self._locale,
                ReviewCopyKey.ERROR_OCCURRED,
                date=self._format_datetime(error.occurred_at),
            )
        )
        occurred.setObjectName("errorOccurredAt")
        layout.addWidget(occurred)

        if error.resolved_at is not None:
            resolved = QLabel(
                review_text(
                    self._locale,
                    ReviewCopyKey.ERROR_RESOLVED,
                    date=self._format_datetime(error.resolved_at),
                )
            )
            resolved.setObjectName("errorResolvedAt")
            layout.addWidget(resolved)

        layout.addLayout(
            self._action_row(
                object_name="errorOpenModuleButton",
                course_code=error.course_code,
                module_id=error.module_id,
                objective_id=first_objective,
            )
        )
        return card

    def _action_row(
        self,
        *,
        object_name: str,
        course_code: str,
        module_id: str,
        objective_id: str,
    ) -> QHBoxLayout:
        row = QHBoxLayout()
        row.setContentsMargins(0, 0, 0, 0)
        row.addStretch(1)
        action = QPushButton(review_text(self._locale, ReviewCopyKey.OPEN_MODULE))
        action.setObjectName(object_name)
        action.setProperty("courseCode", course_code)
        action.setProperty("moduleId", module_id)
        action.setProperty("objectiveId", objective_id)
        action.clicked.connect(self._emit_review_request)
        row.addWidget(action)
        return row

    def _render_queue_empty_state(self) -> None:
        empty = QFrame()
        empty.setObjectName("reviewEmptyState")
        layout = QVBoxLayout(empty)
        layout.setContentsMargins(18, 18, 18, 18)
        layout.setSpacing(8)

        title = QLabel(review_text(self._locale, ReviewCopyKey.EMPTY_TITLE))
        title.setObjectName("reviewEmptyTitle")
        layout.addWidget(title)

        body = QLabel(review_text(self._locale, ReviewCopyKey.EMPTY_BODY))
        body.setObjectName("reviewEmptyBody")
        body.setWordWrap(True)
        layout.addWidget(body)

        self._queue_layout.addWidget(empty)
        self._queue_layout.addStretch(1)

    def _render_error_empty_state(self) -> None:
        empty = QFrame()
        empty.setObjectName("errorNotebookEmptyState")
        layout = QVBoxLayout(empty)
        layout.setContentsMargins(18, 18, 18, 18)
        layout.setSpacing(8)

        title = QLabel(review_text(self._locale, ReviewCopyKey.ERROR_EMPTY_TITLE))
        title.setObjectName("errorNotebookEmptyTitle")
        layout.addWidget(title)

        body = QLabel(review_text(self._locale, ReviewCopyKey.ERROR_EMPTY_BODY))
        body.setObjectName("errorNotebookEmptyBody")
        body.setWordWrap(True)
        layout.addWidget(body)

        self._error_layout.addWidget(empty)
        self._error_layout.addStretch(1)

    @staticmethod
    def _clear_layout(layout: QVBoxLayout) -> None:
        while layout.count():
            item = layout.takeAt(0)
            if item is None:
                continue
            widget = item.widget()
            if widget is not None:
                widget.setParent(None)
                widget.deleteLater()

    @staticmethod
    def _priority_key(item: ReviewItem, now: datetime) -> ReviewCopyKey:
        state = item.state
        overdue_days = max(0, int((now - state.next_review_at).total_seconds() // 86_400))
        if state.lapse_count > 0 or state.mastery_score < 0.45 or overdue_days >= 3:
            return ReviewCopyKey.PRIORITY_HIGH
        if state.mastery_score < 0.75 or overdue_days >= 1:
            return ReviewCopyKey.PRIORITY_MEDIUM
        return ReviewCopyKey.PRIORITY_LOW

    @staticmethod
    def _error_kind_key(kind: ErrorKind) -> ReviewCopyKey:
        return {
            ErrorKind.KNOWLEDGE_GAP: ReviewCopyKey.ERROR_KIND_KNOWLEDGE_GAP,
            ErrorKind.FRAGILE_UNDERSTANDING: ReviewCopyKey.ERROR_KIND_FRAGILE,
            ErrorKind.MISCONCEPTION: ReviewCopyKey.ERROR_KIND_MISCONCEPTION,
        }[kind]

    @staticmethod
    def _confidence_key(confidence: ConfidenceLevel) -> ReviewCopyKey:
        return {
            ConfidenceLevel.LOW: ReviewCopyKey.CONFIDENCE_LOW,
            ConfidenceLevel.MEDIUM: ReviewCopyKey.CONFIDENCE_MEDIUM,
            ConfidenceLevel.HIGH: ReviewCopyKey.CONFIDENCE_HIGH,
        }[confidence]

    @staticmethod
    def _format_datetime(value: datetime) -> str:
        return value.astimezone().strftime("%Y-%m-%d %H:%M")

    @Slot(bool)
    def _emit_review_request(self, checked: bool) -> None:
        del checked
        button = self.sender()
        if not isinstance(button, QPushButton):
            return
        self.review_requested.emit(
            str(button.property("courseCode")),
            str(button.property("moduleId")),
            str(button.property("objectiveId")),
        )


__all__ = ["ReviewPage"]
