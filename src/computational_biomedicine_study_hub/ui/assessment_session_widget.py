"""Interactive PySide6 widget for randomized closed-question sessions."""

from __future__ import annotations

from PySide6.QtCore import Qt, Slot
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

from ..content.models import AssessmentItem
from ..learning.assessment_session import AnswerFeedback, AssessmentSession


class AssessmentSessionWidget(QWidget):
    """Present one randomized question at a time with deterministic correction."""

    def __init__(
        self,
        question_bank: tuple[AssessmentItem, ...],
        *,
        question_count: int = 6,
        seed: int | None = None,
        parent: QWidget | None = None,
    ) -> None:
        super().__init__(parent)
        self.setObjectName("assessmentSessionWidget")
        self._question_bank = question_bank
        self._question_count = question_count
        self._fixed_seed = seed
        self._session_number = 0
        self._session: AssessmentSession | None = None
        self._previous_item_ids: tuple[str, ...] = ()
        self._option_group = QButtonGroup(self)
        self._option_group.setExclusive(True)

        self._bank_summary = QLabel()
        self._bank_summary.setObjectName("assessmentBankSummary")
        self._bank_summary.setWordWrap(True)

        self._new_session_button = QPushButton("Nueva sesión aleatoria")
        self._new_session_button.setObjectName("secondaryActionButton")
        self._new_session_button.clicked.connect(self.start_new_session)

        toolbar = QHBoxLayout()
        toolbar.setContentsMargins(0, 0, 0, 0)
        toolbar.addWidget(self._bank_summary, 1)
        toolbar.addWidget(self._new_session_button)

        self._card = QFrame()
        self._card.setObjectName("interactiveAssessmentCard")
        card_layout = QVBoxLayout(self._card)
        card_layout.setContentsMargins(22, 20, 22, 20)
        card_layout.setSpacing(14)

        self._progress = QLabel()
        self._progress.setObjectName("assessmentProgress")
        self._prompt = QLabel()
        self._prompt.setObjectName("interactiveAssessmentPrompt")
        self._prompt.setWordWrap(True)
        self._prompt.setTextInteractionFlags(Qt.TextInteractionFlag.TextSelectableByMouse)

        self._options_widget = QWidget()
        self._options_layout = QVBoxLayout(self._options_widget)
        self._options_layout.setContentsMargins(0, 0, 0, 0)
        self._options_layout.setSpacing(9)

        self._feedback = QLabel()
        self._feedback.setObjectName("assessmentFeedback")
        self._feedback.setWordWrap(True)
        self._feedback.setTextInteractionFlags(Qt.TextInteractionFlag.TextSelectableByMouse)
        self._feedback.hide()

        self._check_button = QPushButton("Comprobar respuesta")
        self._check_button.setObjectName("primaryActionButton")
        self._check_button.setEnabled(False)
        self._check_button.clicked.connect(self.check_answer)

        self._next_button = QPushButton("Siguiente pregunta")
        self._next_button.setObjectName("secondaryActionButton")
        self._next_button.hide()
        self._next_button.clicked.connect(self.advance)

        actions = QHBoxLayout()
        actions.setContentsMargins(0, 0, 0, 0)
        actions.addWidget(self._check_button)
        actions.addWidget(self._next_button)
        actions.addStretch(1)

        card_layout.addWidget(self._progress)
        card_layout.addWidget(self._prompt)
        card_layout.addWidget(self._options_widget)
        card_layout.addWidget(self._feedback)
        card_layout.addLayout(actions)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(4, 8, 12, 12)
        layout.setSpacing(14)
        layout.addLayout(toolbar)
        layout.addWidget(self._card)
        layout.addStretch(1)

        self.start_new_session()

    @property
    def session(self) -> AssessmentSession:
        """Return the active assessment session."""
        if self._session is None:
            raise RuntimeError("The assessment session has not been initialized.")
        return self._session

    @property
    def feedback_text(self) -> str:
        """Return the currently visible feedback text."""
        return self._feedback.text()

    @Slot()
    def start_new_session(self) -> None:
        """Build a fresh sample while avoiding an identical previous selection."""
        seed = None if self._fixed_seed is None else self._fixed_seed + self._session_number
        self._session = AssessmentSession(
            self._question_bank,
            question_count=self._question_count,
            seed=seed,
            previous_item_ids=self._previous_item_ids,
        )
        self._session_number += 1
        self._previous_item_ids = self.session.item_ids
        self._bank_summary.setText(
            f"Banco: {len(self._question_bank)} preguntas · "
            f"Sesión: {self._question_count} preguntas sin repetición."
        )
        self._render_current_question()

    @Slot()
    def check_answer(self) -> None:
        """Grade the selected option and reveal authored feedback."""
        selected = self._option_group.checkedButton()
        if selected is None:
            return

        result = self.session.submit(selected.text())
        for button in self._option_group.buttons():
            button.setEnabled(False)

        self._show_feedback(result)
        self._check_button.setEnabled(False)
        self._next_button.setText(
            "Nueva sesión aleatoria" if self.session.is_complete else "Siguiente pregunta"
        )
        self._next_button.show()
        self._update_progress()

    @Slot()
    def advance(self) -> None:
        """Advance after feedback or start a new random session at the end."""
        if self.session.is_complete:
            self.start_new_session()
            return
        self.session.advance()
        self._render_current_question()

    def _render_current_question(self) -> None:
        self._clear_options()
        question = self.session.current_question
        self._prompt.setText(question.item.prompt)

        for option in question.options:
            button = QRadioButton(option)
            button.setObjectName("assessmentOption")
            button.setProperty("answerState", "unanswered")
            button.toggled.connect(self._enable_check_when_selected)
            self._option_group.addButton(button)
            self._options_layout.addWidget(button)

        self._feedback.clear()
        self._feedback.setProperty("resultState", "idle")
        self._feedback.hide()
        self._next_button.hide()
        self._check_button.setEnabled(False)
        self._update_progress()

    def _clear_options(self) -> None:
        for button in self._option_group.buttons():
            self._option_group.removeButton(button)
            button.deleteLater()

        while self._options_layout.count():
            item = self._options_layout.takeAt(0)
            widget = item.widget()
            if widget is not None:
                widget.deleteLater()

    @Slot(bool)
    def _enable_check_when_selected(self, checked: bool) -> None:
        if checked and not self.session.current_is_answered:
            self._check_button.setEnabled(True)

    def _show_feedback(self, result: AnswerFeedback) -> None:
        if result.is_correct:
            heading = "Correcto."
            state = "correct"
        else:
            heading = f"Incorrecto. Respuesta correcta: {result.correct_answer}."
            state = "incorrect"

        self._feedback.setText(f"{heading}\n{result.explanation}")
        self._feedback.setProperty("resultState", state)
        self._feedback.style().unpolish(self._feedback)
        self._feedback.style().polish(self._feedback)
        self._feedback.show()

        for button in self._option_group.buttons():
            if button.text() == result.correct_answer:
                answer_state = "correct"
            elif button.text() == result.selected_answer and not result.is_correct:
                answer_state = "incorrect"
            else:
                answer_state = "neutral"
            button.setProperty("answerState", answer_state)
            button.style().unpolish(button)
            button.style().polish(button)

    def _update_progress(self) -> None:
        self._progress.setText(
            f"Pregunta {self.session.current_number} de {self.session.question_count} · "
            f"Aciertos: {self.session.score}/{self.session.answered_count}"
        )
