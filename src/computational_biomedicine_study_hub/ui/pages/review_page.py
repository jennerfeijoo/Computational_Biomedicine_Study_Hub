"""Functional spaced-review queue backed by local objective mastery."""

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
    QVBoxLayout,
    QWidget,
)

from ...i18n.locales import AppLocale
from ...i18n.review_copy import ReviewCopyKey, review_text
from ...learning.progress import ReviewItem
from ...learning.review_catalog import authored_objective_catalog
from ...storage import SQLiteProgressStore

Clock = Callable[[], datetime]


def _now_utc() -> datetime:
    return datetime.now(UTC)


class ReviewPage(QWidget):
    """Present due objectives and route the learner back to retrieval practice."""

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
        self._cards: list[QFrame] = []

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

        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(16)
        layout.addLayout(heading_row)
        layout.addWidget(intro)
        layout.addWidget(self._count_label)
        layout.addWidget(scroll, 1)

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
        """Expose rendered cards for deterministic UI testing."""

        return tuple(self._cards)

    @Slot()
    def refresh(self) -> None:
        """Reload due objectives from the local database."""

        now = self._clock()
        if now.tzinfo is None or now.utcoffset() is None:
            raise ValueError("Review clock must return a timezone-aware datetime.")

        self._items = self._store.due_reviews(now) if self._store is not None else ()
        self._count_label.setText(
            review_text(self._locale, ReviewCopyKey.DUE_COUNT, count=len(self._items))
        )
        self._clear_queue()

        if not self._items:
            self._render_empty_state()
            return

        for item in self._items:
            card = self._build_card(item, now)
            self._cards.append(card)
            self._queue_layout.addWidget(card)
        self._queue_layout.addStretch(1)

    def _build_card(self, item: ReviewItem, now: datetime) -> QFrame:
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
                date=state.next_review_at.astimezone().strftime("%Y-%m-%d %H:%M"),
            )
        )
        due.setObjectName("reviewDueDate")
        layout.addWidget(due)

        action_row = QHBoxLayout()
        action_row.setContentsMargins(0, 0, 0, 0)
        action_row.addStretch(1)
        action = QPushButton(review_text(self._locale, ReviewCopyKey.OPEN_MODULE))
        action.setObjectName("reviewOpenModuleButton")
        action.setProperty("courseCode", item.course_code)
        action.setProperty("moduleId", item.module_id)
        action.setProperty("objectiveId", item.objective_id)
        action.clicked.connect(self._emit_review_request)
        action_row.addWidget(action)
        layout.addLayout(action_row)
        return card

    def _render_empty_state(self) -> None:
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

    def _clear_queue(self) -> None:
        self._cards.clear()
        while self._queue_layout.count():
            item = self._queue_layout.takeAt(0)
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
