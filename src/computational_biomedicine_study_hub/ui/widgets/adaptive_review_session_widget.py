"""Sequential PySide6 surface for mixed adaptive review activities."""

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
from ...learning.adaptive_review import (
    AdaptiveReviewProgramming,
    AdaptiveReviewQuestion,
    AdaptiveReviewSession,
)
from ...learning.progress_service import ObjectiveAttemptRecorder
from ...learning.review_catalog import authored_objective_catalog
from .objective_assessment_widget import ObjectiveQuestionCard
from .python_challenge_widget import PythonChallengeWidget


class AdaptiveReviewSessionWidget(QFrame):
    """Present one deterministic activity at a time and persist its outcomes."""

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
            raise ValueError(
                "Adaptive review widgets require a session with an available activity."
            )

        self.setObjectName("adaptiveReviewSessionWidget")
        self._session = session
        self._locale = locale
        self._progress_recorder = progress_recorder
        self._catalog = authored_objective_catalog(locale)
        self._current_card: QWidget | None = None
        self._pending_programming_result: tuple[str, bool] | None = None
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

        self._activity_label = QLabel()
        self._activity_label.setObjectName("adaptiveReviewActivityLabel")
        layout.addWidget(self._activity_label)

        self._programming_notice = QLabel(
            adaptive_review_text(
                locale,
                AdaptiveReviewCopyKey.PROGRAMMING_RETRY_NOTICE,
            )
        )
        self._programming_notice.setObjectName("adaptiveReviewProgrammingNotice")
        self._programming_notice.setWordWrap(True)
        self._programming_notice.hide()
        layout.addWidget(self._programming_notice)

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

        self._render_current_activity()

    @property
    def session(self) -> AdaptiveReviewSession:
        return self._session

    @property
    def current_card(self) -> QWidget | None:
        return self._current_card

    @property
    def current_question_card(self) -> ObjectiveQuestionCard | None:
        card = self._current_card
        return card if isinstance(card, ObjectiveQuestionCard) else None

    @property
    def current_challenge_widget(self) -> PythonChallengeWidget | None:
        card = self._current_card
        return card if isinstance(card, PythonChallengeWidget) else None

    @property
    def summary_visible(self) -> bool:
        return self._summary_visible

    @property
    def progress_text(self) -> str:
        return self._progress_label.text()

    @Slot(str, bool)
    def _record_question_result(self, item_id: str, is_correct: bool) -> None:
        current = self._session.current_activity
        if not isinstance(current, AdaptiveReviewQuestion):
            raise RuntimeError("Question feedback requires a question review activity.")
        self._session.record_result(item_id, is_correct)
        self._progress_bar.setValue(self._session.answered_count)
        self._update_progress_text()
        self._show_advance_button()

    @Slot(str, bool)
    def _capture_programming_result(self, item_id: str, is_correct: bool) -> None:
        current = self._session.current_activity
        if not isinstance(current, AdaptiveReviewProgramming):
            raise RuntimeError("Programming feedback requires a programming review activity.")
        if current.item_id != item_id:
            raise ValueError("Programming feedback must match the current challenge.")
        self._pending_programming_result = (item_id, is_correct)
        self._show_advance_button(pending_programming=True)

    @Slot()
    def advance(self) -> None:
        """Commit pending code feedback, then show the next activity or summary."""

        if self._pending_programming_result is not None:
            item_id, is_correct = self._pending_programming_result
            self._session.record_result(item_id, is_correct)
            self._pending_programming_result = None
            self._progress_bar.setValue(self._session.answered_count)
            self._update_progress_text()

        if self._session.is_complete:
            self._render_summary()
            return
        self._render_current_activity()

    def _render_current_activity(self) -> None:
        current = self._session.current_activity
        if current is None:
            self._render_summary()
            return

        self._clear_question_host()
        self._pending_programming_result = None
        self._summary_visible = False
        number = self._session.answered_count + 1

        card: ObjectiveQuestionCard | PythonChallengeWidget
        if isinstance(current, AdaptiveReviewQuestion):
            card = ObjectiveQuestionCard(
                number,
                current.question,
                locale=self._locale,
                course_code=current.course_code,
                module_id=current.module_id,
                objective_ids=current.objective_ids,
                progress_recorder=self._progress_recorder,
            )
            card.answered.connect(self._record_question_result)
            self._programming_notice.hide()
            activity_key = AdaptiveReviewCopyKey.QUESTION_ACTIVITY
        else:
            candidate = current.candidate
            exercise = candidate.exercise
            challenge = candidate.challenge
            card = PythonChallengeWidget(
                challenge.starter_code,
                challenge,
                locale=self._locale,
                activity_type=exercise.activity_type.value,
                prompt=exercise.prompt,
                reference_solution=exercise.solution,
                explanation=exercise.explanation,
                progress_recorder=self._progress_recorder,
                learning_module=candidate.learning_module,
            )
            card.tests_finished.connect(self._capture_programming_result)
            self._programming_notice.show()
            activity_key = AdaptiveReviewCopyKey.PROGRAMMING_ACTIVITY

        self._current_card = card
        self._question_layout.addWidget(card)
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
        self._activity_label.setText(
            adaptive_review_text(
                self._locale,
                AdaptiveReviewCopyKey.ACTIVITY_TYPE,
                activity=adaptive_review_text(self._locale, activity_key),
            )
        )
        self._activity_label.show()
        self._next_button.hide()
        self._update_progress_text()

    def _show_advance_button(self, *, pending_programming: bool = False) -> None:
        reaches_target = self._session.answered_count >= self._session.target_questions
        if pending_programming:
            reaches_target = self._session.answered_count + 1 >= self._session.target_questions
        key = (
            AdaptiveReviewCopyKey.FINISH
            if reaches_target or self._session.is_complete
            else AdaptiveReviewCopyKey.NEXT
        )
        self._next_button.setText(adaptive_review_text(self._locale, key))
        self._next_button.show()

    def _render_summary(self) -> None:
        self._clear_question_host()
        self._current_card = None
        self._pending_programming_result = None
        self._summary_visible = True
        self._objective_label.hide()
        self._activity_label.hide()
        self._programming_notice.hide()
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
                questions=summary.question_activities,
                programming=summary.programming_activities,
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
        refresh.clicked.connect(self.queue_refresh_requested.emit)
        layout.addWidget(refresh)

        self._question_layout.addWidget(panel)
        self.session_completed.emit(summary.correct, summary.answered)

    def _update_progress_text(self) -> None:
        current = min(
            self._session.answered_count + 1,
            self._session.target_questions,
        )
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
