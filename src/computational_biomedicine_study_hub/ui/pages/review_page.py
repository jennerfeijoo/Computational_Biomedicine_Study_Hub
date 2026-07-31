"""Functional spaced review and an authored error notebook."""

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

from ...i18n.locales import AppLocale
from ...i18n.review_copy import ReviewCopyKey, review_text
from ...learning.progress import ConfidenceLevel, ErrorKind, ErrorRecord, ReviewItem
from ...learning.review_catalog import authored_objective_catalog
from ...storage import SQLiteProgressStore

Clock = Callable[[], datetime]


def _now_utc() -> datetime:
    return datetime.now(UTC)


class ReviewPage(QWidget):
    """Present scheduled objectives and persistent authored error history."""

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
        """Reload scheduled review and error history from the local database."""

        now = self._clock()
        if now.tzinfo is None or now.utcoffset() is None:
            raise ValueError("Review clock must return a timezone-aware datetime.")

        if self._store is None:
            self._items = ()
            self._errors = ()
        else:
            self._items = self._store.due_reviews(now)
            self._errors = self._store.list_errors()

        self._render_queue(now)
        self._render_error_notebook()

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
        descriptor = self._catalog.get(
            (error.course_code, error.module_id, first_objective)
        )

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

        prompt = QLabel(
            review_text(self._locale, ReviewCopyKey.ERROR_PROMPT, text=error.prompt)
        )
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
