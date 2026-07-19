"""Interactive PySide6 widgets for deterministic objective assessment."""

from __future__ import annotations

import random
import uuid
from dataclasses import replace
from datetime import UTC, datetime

from PySide6.QtCore import Signal, Slot
from PySide6.QtWidgets import (
    QButtonGroup,
    QFrame,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QRadioButton,
    QVBoxLayout,
    QWidget,
)

from ...content.models import AssessmentItem
from ...i18n import DEFAULT_LOCALE, AppLocale, UiCopyKey, ui_text
from ...learning.objective_assessment import (
    ObjectiveAnswerFeedback,
    ObjectiveAssessmentSession,
    ObjectiveSessionGenerator,
    ObjectiveSessionQuestion,
    grade_objective_answer,
)
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
from .objective_assessment_styles import OBJECTIVE_ASSESSMENT_STYLESHEET


class ObjectiveQuestionCard(QFrame):
    """Render one selectable localized question with authored feedback."""

    answered = Signal(str, bool)
    answer_recorded = Signal(str, str, bool)

    def __init__(
        self,
        number: int,
        question: ObjectiveSessionQuestion,
        parent: QWidget | None = None,
        *,
        locale: AppLocale = DEFAULT_LOCALE,
    ) -> None:
        super().__init__(parent)
        self.setObjectName("objectiveQuestionCard")
        self._question = question
        self._locale = locale
        self._answered = False

        layout = QVBoxLayout(self)
        layout.setContentsMargins(18, 16, 18, 16)
        layout.setSpacing(10)

        number_label = QLabel(ui_text(locale, UiCopyKey.OBJECTIVE_QUESTION_NUMBER, number=number))
        number_label.setObjectName("objectiveQuestionNumber")
        layout.addWidget(number_label)

        prompt = QLabel(question.item.prompt)
        prompt.setObjectName("objectiveQuestionPrompt")
        prompt.setWordWrap(True)
        layout.addWidget(prompt)

        self._button_group = QButtonGroup(self)
        self._button_group.setExclusive(True)
        self._option_buttons: list[QRadioButton] = []
        for option in question.display_options:
            button = QRadioButton(option.text)
            button.setObjectName("objectiveOption")
            button.setProperty("answerId", option.option_id)
            button.setMinimumHeight(38)
            self._button_group.addButton(button)
            self._option_buttons.append(button)
            layout.addWidget(button)

        self._check_button = QPushButton(ui_text(locale, UiCopyKey.OBJECTIVE_CHECK))
        self._check_button.setObjectName("checkObjectiveAnswerButton")
        self._check_button.clicked.connect(self.check_answer)
        layout.addWidget(self._check_button, 0)

        self._feedback = QLabel()
        self._feedback.setObjectName("objectiveAnswerFeedback")
        self._feedback.setWordWrap(True)
        self._feedback.hide()
        layout.addWidget(self._feedback)

    @property
    def item_id(self) -> str:
        """Return the stable authored question identifier."""
        return self._question.item.item_id

    @property
    def selected_option_id(self) -> str:
        """Return the stable ID for the selected option or an empty string."""
        selected = self._button_group.checkedButton()
        if selected is None:
            return ""
        value = selected.property("answerId")
        return value if isinstance(value, str) else ""

    @property
    def selected_answer(self) -> str:
        """Return the visible text for the currently selected option."""
        selected = self._button_group.checkedButton()
        return selected.text() if selected is not None else ""

    @property
    def is_answered(self) -> bool:
        """Return whether this card has already been graded."""
        return self._answered

    @property
    def feedback_text(self) -> str:
        """Return visible feedback text for tests and accessibility."""
        return self._feedback.text()

    def choose_option(self, option_id: str) -> bool:
        """Select one option by its stable authored identifier."""
        for button in self._option_buttons:
            if button.property("answerId") == option_id:
                button.setChecked(True)
                return True
        return False

    def choose_answer(self, answer: str) -> bool:
        """Compatibility helper that accepts either an option ID or visible text."""
        if self.choose_option(answer):
            return True
        for button in self._option_buttons:
            if button.text() == answer:
                button.setChecked(True)
                return True
        return False

    @Slot()
    def check_answer(self) -> None:
        """Grade the selected answer once and expose immediate feedback."""
        if self._answered:
            return

        selected_option_id = self.selected_option_id
        if not selected_option_id:
            self._show_feedback(
                ui_text(self._locale, UiCopyKey.OBJECTIVE_SELECT_WARNING),
                "warning",
            )
            return

        feedback = grade_objective_answer(self._question, selected_option_id)
        self._apply_feedback(feedback)
        self.answered.emit(self.item_id, feedback.is_correct)
        self.answer_recorded.emit(
            self.item_id,
            feedback.selected_option_id,
            feedback.is_correct,
        )

    def restore_answer(self, option_id: str) -> bool:
        """Restore a persisted selection without emitting a second attempt."""
        if self._answered or not self.choose_option(option_id):
            return False
        feedback = grade_objective_answer(self._question, option_id)
        self._apply_feedback(feedback)
        return True

    def _apply_feedback(self, feedback: ObjectiveAnswerFeedback) -> None:
        if feedback.is_correct:
            message = ui_text(
                self._locale,
                UiCopyKey.OBJECTIVE_CORRECT,
                explanation=feedback.explanation,
            )
            state = "correct"
        else:
            message = ui_text(
                self._locale,
                UiCopyKey.OBJECTIVE_INCORRECT,
                answer=feedback.correct_answer,
                explanation=feedback.explanation,
            )
            state = "incorrect"

        self._answered = True
        for button in self._option_buttons:
            button.setEnabled(False)
        self._check_button.setEnabled(False)
        self._show_feedback(message, state)

    def _show_feedback(self, text: str, state: str) -> None:
        self._feedback.setText(text)
        self._feedback.setProperty("answerState", state)
        self._feedback.style().unpolish(self._feedback)
        self._feedback.style().polish(self._feedback)
        self._feedback.show()


class ObjectiveAssessmentWidget(QWidget):
    """Manage repeated localized sessions from one authored question bank."""

    def __init__(
        self,
        bank: tuple[AssessmentItem, ...],
        *,
        question_count: int = 6,
        generator: ObjectiveSessionGenerator | None = None,
        locale: AppLocale = DEFAULT_LOCALE,
        repository: ProgressRepository | None = None,
        course_code: str = "",
        module_id: str = "",
        content_version: str = "",
        parent: QWidget | None = None,
    ) -> None:
        super().__init__(parent)
        self.setObjectName("objectiveAssessmentWidget")
        self.setStyleSheet(OBJECTIVE_ASSESSMENT_STYLESHEET)
        self._locale = locale
        self._bank = bank
        self._question_count = question_count
        self._repository = repository
        self._course_code = course_code
        self._module_id = module_id
        self._content_version = content_version
        self._persistent_session: AssessmentSession | None = None
        if repository is not None and not all((course_code, module_id, content_version)):
            raise ValueError(
                "Persistent objective assessment requires course, module, and content version."
            )

        self._generator = generator or ObjectiveSessionGenerator(
            bank,
            question_count=question_count,
        )
        self._results: dict[str, bool] = {}
        self._current_item_ids: tuple[str, ...] = ()
        self._question_cards: list[ObjectiveQuestionCard] = []

        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(14)

        header = QFrame()
        header.setObjectName("objectiveAssessmentHeader")
        header_layout = QHBoxLayout(header)
        header_layout.setContentsMargins(18, 14, 18, 14)
        header_layout.setSpacing(14)

        header_text = QWidget()
        header_text_layout = QVBoxLayout(header_text)
        header_text_layout.setContentsMargins(0, 0, 0, 0)
        header_text_layout.setSpacing(3)

        title = QLabel(ui_text(locale, UiCopyKey.OBJECTIVE_TITLE))
        title.setObjectName("objectiveAssessmentTitle")
        header_text_layout.addWidget(title)

        self._metadata = QLabel()
        self._metadata.setObjectName("objectiveAssessmentMetadata")
        self._metadata.setWordWrap(True)
        header_text_layout.addWidget(self._metadata)

        self._score = QLabel()
        self._score.setObjectName("objectiveAssessmentScore")

        self._new_session_button = QPushButton(ui_text(locale, UiCopyKey.OBJECTIVE_NEW_SESSION))
        self._new_session_button.setObjectName("newAssessmentSessionButton")
        self._new_session_button.clicked.connect(self.new_session)

        header_layout.addWidget(header_text, 1)
        header_layout.addWidget(self._score)
        header_layout.addWidget(self._new_session_button)
        layout.addWidget(header)

        self._cards_container = QWidget()
        self._cards_container.setObjectName("objectiveAssessmentCards")
        self._cards_layout = QVBoxLayout(self._cards_container)
        self._cards_layout.setContentsMargins(0, 0, 0, 0)
        self._cards_layout.setSpacing(12)
        layout.addWidget(self._cards_container)

        if not self._restore_session():
            self.new_session()

    @property
    def current_item_ids(self) -> tuple[str, ...]:
        """Return IDs for the current randomized session."""
        return self._current_item_ids

    @property
    def question_cards(self) -> tuple[ObjectiveQuestionCard, ...]:
        """Return current question cards in display order."""
        return tuple(self._question_cards)

    @property
    def score_text(self) -> str:
        """Return the visible score summary."""
        return self._score.text()

    @Slot()
    def new_session(self) -> None:
        """Replace the current session with a new non-identical random sample."""
        if (
            self._repository is not None
            and self._persistent_session is not None
            and not self._persistent_session.is_complete
        ):
            self._repository.save_assessment_session(
                replace(self._persistent_session, completed_at=datetime.now(UTC))
            )
        if self._repository is None:
            session = self._generator.new_session()
        else:
            seed = random.SystemRandom().randrange(0, 2**63)
            session = self._session_for_seed(seed)
            self._persistent_session = AssessmentSession(
                session_id=str(uuid.uuid4()),
                scope=AssessmentScope.OBJECTIVE_MODULE,
                course_code=self._course_code,
                module_id=self._module_id,
                item_ids=session.item_ids,
                seed=seed,
                locale=self._locale.value,
                started_at=datetime.now(UTC),
            )
            self._repository.save_assessment_session(self._persistent_session)
        self._render_session(session)

    def _render_session(
        self,
        session: ObjectiveAssessmentSession,
        *,
        restored_attempts: dict[str, AttemptRecord] | None = None,
    ) -> None:
        self._results.clear()
        self._current_item_ids = session.item_ids
        self._question_cards.clear()
        self._clear_cards()

        for number, question in enumerate(session.questions, start=1):
            card = ObjectiveQuestionCard(number, question, locale=self._locale)
            restored = (
                restored_attempts.get(question.item.item_id)
                if restored_attempts is not None
                else None
            )
            if (
                restored is not None
                and restored.selected_option_ids
                and restored.is_correct is not None
                and card.restore_answer(restored.selected_option_ids[0])
            ):
                self._results[question.item.item_id] = restored.is_correct
            card.answer_recorded.connect(self._record_persistent_result)
            self._question_cards.append(card)
            self._cards_layout.addWidget(card)

        self._metadata.setText(
            ui_text(
                self._locale,
                UiCopyKey.OBJECTIVE_METADATA,
                count=self._generator.question_count,
                bank=self._generator.bank_size,
            )
        )
        self._update_score()

    @Slot(str, bool)
    def _record_result(self, item_id: str, is_correct: bool) -> None:
        self._results[item_id] = is_correct
        self._update_score()

    @Slot(str, str, bool)
    def _record_persistent_result(
        self,
        item_id: str,
        option_id: str,
        is_correct: bool,
    ) -> None:
        self._record_result(item_id, is_correct)
        if self._repository is None or self._persistent_session is None:
            return
        item = next(value for value in self._bank if value.item_id == item_id)
        now = datetime.now(UTC)
        self._repository.record_attempt(
            AttemptRecord(
                attempt_id=str(uuid.uuid4()),
                course_code=self._course_code,
                module_id=self._module_id,
                item_id=item_id,
                item_kind=LearningItemKind.ASSESSMENT,
                activity_type=item.activity_type,
                outcome=AttemptOutcome.SOLVED if is_correct else AttemptOutcome.REVIEW,
                locale=self._locale.value,
                content_version=self._content_version,
                created_at=now,
                selected_option_ids=(option_id,),
                is_correct=is_correct,
                score=float(is_correct),
                session_id=self._persistent_session.session_id,
            )
        )
        initial = ReviewSchedule(
            course_code=self._course_code,
            module_id=self._module_id,
            item_id=item_id,
            item_kind=LearningItemKind.ASSESSMENT,
            mastery_state=MasteryState.NEW,
            repetitions=0,
            interval_days=0,
            easiness=2.5,
            due_at=now,
        )
        self._repository.save_review_schedule(
            reschedule(
                initial,
                ReviewRating.GOOD if is_correct else ReviewRating.AGAIN,
                reviewed_at=now,
            )
            if is_correct
            else replace(initial, mastery_state=MasteryState.LEARNING, easiness=2.3)
        )
        if item_id not in self._persistent_session.answered_item_ids:
            answered = self._persistent_session.answered_item_ids + (item_id,)
            self._persistent_session = replace(
                self._persistent_session,
                answered_item_ids=answered,
                correct_count=self._persistent_session.correct_count + int(is_correct),
            )
            self._repository.save_assessment_session(self._persistent_session)

    def _restore_session(self) -> bool:
        if self._repository is None:
            return False
        persistent = self._repository.latest_open_assessment_session(
            course_code=self._course_code,
            module_id=self._module_id,
            scope=AssessmentScope.OBJECTIVE_MODULE.value,
        )
        if persistent is None:
            return False
        session = self._session_for_seed(persistent.seed)
        if session.item_ids != persistent.item_ids:
            return False
        attempts = self._repository.list_attempts(
            session_id=persistent.session_id,
        )
        latest_by_item: dict[str, AttemptRecord] = {}
        for attempt in attempts:
            latest_by_item.setdefault(attempt.item_id, attempt)
        self._persistent_session = persistent
        self._render_session(session, restored_attempts=latest_by_item)
        return True

    def _session_for_seed(self, seed: int) -> ObjectiveAssessmentSession:
        return ObjectiveSessionGenerator(
            self._bank,
            question_count=self._question_count,
            rng=random.Random(seed),
        ).new_session()

    def _update_score(self) -> None:
        answered = len(self._results)
        correct = sum(self._results.values())
        total = self._generator.question_count
        self._score.setText(
            ui_text(
                self._locale,
                UiCopyKey.OBJECTIVE_SCORE,
                correct=correct,
                answered=answered,
                total=total,
            )
        )

    def _clear_cards(self) -> None:
        while self._cards_layout.count():
            item = self._cards_layout.takeAt(0)
            if item is None:
                break
            widget = item.widget()
            if widget is not None:
                widget.setParent(None)
                widget.deleteLater()


__all__ = ["ObjectiveAssessmentWidget", "ObjectiveQuestionCard"]
