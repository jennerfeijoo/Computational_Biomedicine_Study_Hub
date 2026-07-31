"""Sequential PySide6 surface for one adaptive review session."""

from __future__ import annotations

from PySide6.QtCore import Signal, Slot
from PySide6.QtWidgets import (
    QFrame,
    QHBoxLayout,
    QLabel,
    QProgressBar,
    QPushButton,
    QVBoxLayout,
    QWidget,
)

from ...i18n import AdaptiveReviewCopyKey, AppLocale, adaptive_review_text
from ...learning.adaptive_review import AdaptiveReviewSession
from ...learning.progress_service import ObjectiveAttemptRecorder
from ...learning.review_catalog import authored_objective_catalog
from .objective_assessment_widget import ObjectiveQuestionCard


class AdaptiveReviewSessionWidget(QFrame):
    """Present one question at a time and advance from deterministic outcomes."""

    session_completed = Signal(int, int)
    queue_refresh_requested = Signal()

    def __init__(
        self,
        session: AdaptiveReviewSession,
        *,
        locale: AppLocale,
        progress_recorder: ObjectiveAttemptRecorder | None = None,
        parent: QWidget | None = None,
    ) -> None:
        super().__init__(parent)
        if not session.can_start:
            raise ValueError("Adaptive review widgets require a session with an available question.")

        self.setObjectName("adaptiveReviewSessionWidget")
        self._session = session
        self._locale = locale
        self._progress_recorder = progress_recorder
        self._catalog = authored_objective_catalog(locale)
        self._current_card: ObjectiveQuestionCard | None = None
        self._summary_visible = False

        layout = QVBoxLayout(self)
        layout.setContentsMargins(18, 16, 18, 16)
        layout.setSpacing(12)

        title = QLabel(adaptive_review_text(locale, AdaptiveReviewCopyKey.TITLE))
        title.setObjectName("adaptiveReviewSessionTitle")
        layout.addWidget(title)

        intro = QLabel(adaptive_review_text(locale, AdaptiveReviewCopyKey.INTRO))
        intro.setObjectName("adaptiveReviewSessionIntro")
        intro.setWordWrap(True)
        layout.addWidget(intro)

        self._progress_label = QLabel()
        self._progress_label.setObjectName("adaptiveReviewProgressLabel")
        layout.addWidget(self._progress_label)

        self._progress_bar = QProgressBar()
        self._progress_bar.setObjectName("adaptiveReviewProgressBar")
        self._progress_bar.setRange(0, session.target_questions)
        self._progress_bar.setValue(0)
        self._progress_bar.setTextVisible(False)
        layout.addWidget(self._progress_bar)

        self._objective_label = QLabel()
        self._objective_label.setObjectName("adaptiveReviewObjectiveLabel")
        self._objective_label.setWordWrap(True)
        layout.addWidget(self._objective_label)

        self._question_host = QWidget()
        self._question_host.setObjectName("adaptiveReviewQuestionHost")
        self._question_layout = QVBoxLayout(self._question_host)
        self._question_layout.setContentsMargins(0, 0, 0, 0)
        self._question_layout.setSpacing(0)
        layout.addWidget(self._question_host)

        actions = QHBoxLayout()
        actions.setContentsMargins(0, 0, 0, 0)
        actions.addStretch(1)
        self._next_button = QPushButton(adaptive_review_text(locale, AdaptiveReviewCopyKey.NEXT))
        self._next_button.setObjectName("adaptiveReviewNextButton")
        self._next_button.clicked.connect(self.advance)
        self._next_button.hide()
        actions.addWidget(self._next_button)
        layout.addLayout(actions)

        self._render_current_question()

    @property
    def session(self) -> AdaptiveReviewSession:
        return self._session

    @property
    def current_card(self) -> ObjectiveQuestionCard | None:
        return self._current_card

    @property
    def summary_visible(self) -> bool:
        return self._summary_visible

    @property
    def progress_text(self) -> str:
        return self._progress_label.text()

    @Slot(str, bool)
    def _record_result(self, item_id: str, is_correct: bool) -> None:
        self._session.record_result(item_id, is_correct)
        self._progress_bar.setValue(self._session.answered_count)
        self._update_progress_text()
        key = (
            AdaptiveReviewCopyKey.FINISH
            if self._session.is_complete
            else AdaptiveReviewCopyKey.NEXT
        )
        self._next_button.setText(adaptive_review_text(self._locale, key))
        self._next_button.show()

    @Slot()
    def advance(self) -> None:
        """Show the next selected question or the completed-session summary."""

        if self._session.is_complete:
            self._render_summary()
            return
        self._render_current_question()

    def _render_current_question(self) -> None:
        current = self._session.current_question
        if current is None:
            self._render_summary()
            return

        self._clear_question_host()
        number = self._session.answered_count + 1
        self._current_card = ObjectiveQuestionCard(
            number,
            current.question,
            locale=self._locale,
            course_code=current.course_code,
            module_id=current.module_id,
            objective_ids=current.objective_ids,
            progress_recorder=self._progress_recorder,
        )
        self._current_card.answered.connect(self._record_result)
        self._question_layout.addWidget(self._current_card)
        descriptor = self._catalog.get(current.primary_key)
        statement = descriptor.statement if descriptor is not None else current.primary_key[2]
        self._objective_label.setText(
            adaptive_review_text(
                self._locale,
                AdaptiveReviewCopyKey.PRIMARY_OBJECTIVE,
                objective=statement,
            )
        )
        self._objective_label.show()
        self._next_button.hide()
        self._update_progress_text()

    def _render_summary(self) -> None:
        self._clear_question_host()
        self._current_card = None
        self._summary_visible = True
        self._objective_label.hide()
        self._next_button.hide()
        summary = self._session.summary

        panel = QFrame()
        panel.setObjectName("adaptiveReviewSummary")
        layout = QVBoxLayout(panel)
        layout.setContentsMargins(18, 16, 18, 16)
        layout.setSpacing(9)

        title = QLabel(adaptive_review_text(self._locale, AdaptiveReviewCopyKey.SUMMARY_TITLE))
        title.setObjectName("adaptiveReviewSummaryTitle")
        layout.addWidget(title)

        objective_labels: list[str] = []
        for key in summary.reviewed_objectives:
            descriptor = self._catalog.get(key)
            objective_labels.append(descriptor.statement if descriptor is not None else key[2])
        summary_text = QLabel(
            adaptive_review_text(
                self._locale,
                AdaptiveReviewCopyKey.SUMMARY,
                answered=summary.answered,
                correct=summary.correct,
                accuracy=round(summary.accuracy * 100),
                objectives="; ".join(objective_labels) or "—",
            )
        )
        summary_text.setObjectName("adaptiveReviewSummaryText")
        summary_text.setWordWrap(True)
        layout.addWidget(summary_text)

        state_key = (
            AdaptiveReviewCopyKey.EXHAUSTED
            if summary.exhausted and summary.answered < summary.target
            else AdaptiveReviewCopyKey.COMPLETE
        )
        state = QLabel(adaptive_review_text(self._locale, state_key))
        state.setObjectName("adaptiveReviewSummaryState")
        state.setWordWrap(True)
        layout.addWidget(state)

        refresh = QPushButton(
            adaptive_review_text(self._locale, AdaptiveReviewCopyKey.RETURN_TO_QUEUE)
        )
        refresh.setObjectName("adaptiveReviewRefreshQueueButton")
        refresh.clicked.connect(self.queue_refresh_requested)
        layout.addWidget(refresh)

        self._question_layout.addWidget(panel)
        self.session_completed.emit(summary.correct, summary.answered)

    def _update_progress_text(self) -> None:
        current = min(self._session.answered_count + 1, self._session.target_questions)
        if self._session.is_complete:
            current = self._session.answered_count
        self._progress_label.setText(
            adaptive_review_text(
                self._locale,
                AdaptiveReviewCopyKey.PROGRESS,
                current=current,
                target=self._session.target_questions,
                correct=self._session.correct_count,
            )
        )

    def _clear_question_host(self) -> None:
        while self._question_layout.count():
            item = self._question_layout.takeAt(0)
            if item is None:
                break
            widget = item.widget()
            if widget is not None:
                widget.setParent(None)
                widget.deleteLater()


__all__ = ["AdaptiveReviewSessionWidget"]
