"""Interactive PySide6 widgets for deterministic objective assessment."""

from __future__ import annotations

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
    ObjectiveSessionGenerator,
    ObjectiveSessionQuestion,
    grade_objective_answer,
)
from .objective_assessment_styles import OBJECTIVE_ASSESSMENT_STYLESHEET


class ObjectiveQuestionCard(QFrame):
    """Render one selectable localized question with authored feedback."""

    answered = Signal(str, bool)

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
        self.answered.emit(self.item_id, feedback.is_correct)

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
        parent: QWidget | None = None,
    ) -> None:
        super().__init__(parent)
        self.setObjectName("objectiveAssessmentWidget")
        self.setStyleSheet(OBJECTIVE_ASSESSMENT_STYLESHEET)
        self._locale = locale

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
        session = self._generator.new_session()
        self._results.clear()
        self._current_item_ids = session.item_ids
        self._question_cards.clear()
        self._clear_cards()

        for number, question in enumerate(session.questions, start=1):
            card = ObjectiveQuestionCard(number, question, locale=self._locale)
            card.answered.connect(self._record_result)
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
