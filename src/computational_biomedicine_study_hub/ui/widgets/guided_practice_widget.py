"""Interactive PySide6 widgets for randomized guided formative practice."""

from __future__ import annotations

from PySide6.QtCore import Qt, Signal, Slot
from PySide6.QtWidgets import (
    QFrame,
    QHBoxLayout,
    QLabel,
    QPlainTextEdit,
    QPushButton,
    QVBoxLayout,
    QWidget,
)

from ...content.models import PracticeExercise
from ...i18n import (
    DEFAULT_LOCALE,
    AppLocale,
    MessageKey,
    Translator,
    UiCopyKey,
    ui_text,
)
from ...learning.guided_practice import GuidedPracticeSessionGenerator
from .guided_practice_styles import GUIDED_PRACTICE_STYLESHEET

_ACTIVITY_KEYS = {
    "code_tracing": MessageKey.ACTIVITY_CODE_TRACING,
    "matching": MessageKey.ACTIVITY_MATCHING,
    "code_completion": MessageKey.ACTIVITY_CODE_COMPLETION,
    "debugging": MessageKey.ACTIVITY_DEBUGGING,
    "short_answer": MessageKey.ACTIVITY_SHORT_ANSWER,
    "fill_in_the_blank": MessageKey.ACTIVITY_FILL_BLANK,
    "oral_explanation": MessageKey.ACTIVITY_ORAL_EXPLANATION,
    "ordering": MessageKey.ACTIVITY_ORDERING,
    "data_interpretation": MessageKey.ACTIVITY_DATA_INTERPRETATION,
    "pipeline_design": MessageKey.ACTIVITY_PIPELINE_DESIGN,
}


class GuidedPracticeCard(QFrame):
    """Provide a localized workspace, progressive hints and reference feedback."""

    self_assessed = Signal(str, str)

    def __init__(
        self,
        number: int,
        exercise: PracticeExercise,
        parent: QWidget | None = None,
        *,
        locale: AppLocale = DEFAULT_LOCALE,
    ) -> None:
        super().__init__(parent)
        self.setObjectName("guidedPracticeCard")
        self._exercise = exercise
        self._locale = locale
        self._translator = Translator(locale)
        self._visible_hint_count = 0
        self._assessment_state = ""

        layout = QVBoxLayout(self)
        layout.setContentsMargins(18, 16, 18, 16)
        layout.setSpacing(11)

        identity = QHBoxLayout()
        identity.setContentsMargins(0, 0, 0, 0)
        identity.setSpacing(10)

        number_label = QLabel(
            ui_text(locale, UiCopyKey.PRACTICE_NUMBER, number=number)
        )
        number_label.setObjectName("guidedPracticeExerciseNumber")
        activity_label = QLabel(self._activity_label(exercise.activity_type.value))
        activity_label.setObjectName("guidedPracticeExerciseType")
        identity.addWidget(number_label)
        identity.addWidget(activity_label)
        identity.addStretch(1)
        layout.addLayout(identity)

        prompt = QLabel(exercise.prompt)
        prompt.setObjectName("guidedPracticePrompt")
        prompt.setWordWrap(True)
        layout.addWidget(prompt)

        answer_label = QLabel(ui_text(locale, UiCopyKey.PRACTICE_YOUR_ANSWER))
        answer_label.setObjectName("contentSubheading")
        layout.addWidget(answer_label)

        self._answer_editor = QPlainTextEdit()
        self._answer_editor.setObjectName("guidedPracticeAnswerEditor")
        self._answer_editor.setPlaceholderText(
            ui_text(locale, UiCopyKey.PRACTICE_ANSWER_PLACEHOLDER)
        )
        self._answer_editor.setMinimumHeight(125)
        self._answer_editor.setTabChangesFocus(False)
        if exercise.starter_code:
            self._answer_editor.setPlainText(exercise.starter_code)
        layout.addWidget(self._answer_editor)

        hint_actions = QHBoxLayout()
        hint_actions.setContentsMargins(0, 0, 0, 0)
        hint_actions.setSpacing(8)

        self._hint_button = QPushButton(ui_text(locale, UiCopyKey.PRACTICE_SHOW_HINT))
        self._hint_button.setObjectName("guidedPracticeSecondaryButton")
        self._hint_button.setEnabled(bool(exercise.hints))
        self._hint_button.clicked.connect(self.show_next_hint)

        self._solution_button = QPushButton(
            ui_text(locale, UiCopyKey.PRACTICE_REFERENCE_BUTTON)
        )
        self._solution_button.setObjectName("guidedPracticeSecondaryButton")
        self._solution_button.clicked.connect(self.reveal_solution)

        hint_actions.addWidget(self._hint_button)
        hint_actions.addWidget(self._solution_button)
        hint_actions.addStretch(1)
        layout.addLayout(hint_actions)

        self._hint = QLabel()
        self._hint.setObjectName("guidedPracticeHint")
        self._hint.setWordWrap(True)
        self._hint.hide()
        layout.addWidget(self._hint)

        self._solution_panel = QFrame()
        self._solution_panel.setObjectName("guidedPracticeSolution")
        solution_layout = QVBoxLayout(self._solution_panel)
        solution_layout.setContentsMargins(14, 12, 14, 12)
        solution_layout.setSpacing(7)

        solution_title = QLabel(
            ui_text(locale, UiCopyKey.PRACTICE_REFERENCE_TITLE)
        )
        solution_title.setObjectName("guidedPracticeSolutionTitle")
        solution_layout.addWidget(solution_title)

        self._solution = QLabel(exercise.solution)
        self._solution.setObjectName("guidedPracticeSolutionText")
        self._solution.setWordWrap(True)
        self._solution.setTextInteractionFlags(Qt.TextInteractionFlag.TextSelectableByMouse)
        solution_layout.addWidget(self._solution)

        explanation_title = QLabel(ui_text(locale, UiCopyKey.PRACTICE_WHY))
        explanation_title.setObjectName("guidedPracticeSolutionTitle")
        solution_layout.addWidget(explanation_title)

        explanation = QLabel(exercise.explanation)
        explanation.setObjectName("guidedPracticeExplanation")
        explanation.setWordWrap(True)
        solution_layout.addWidget(explanation)

        self._assessment_actions = QWidget()
        assessment_layout = QHBoxLayout(self._assessment_actions)
        assessment_layout.setContentsMargins(0, 4, 0, 0)
        assessment_layout.setSpacing(8)

        assessment_label = QLabel(
            ui_text(locale, UiCopyKey.PRACTICE_SELF_ASSESSMENT)
        )
        assessment_label.setObjectName("guidedPracticeExerciseType")
        self._solved_button = QPushButton(ui_text(locale, UiCopyKey.PRACTICE_SOLVED))
        self._solved_button.setObjectName("guidedPracticeSolvedButton")
        self._solved_button.setCheckable(True)
        self._solved_button.clicked.connect(self.mark_solved)

        self._review_button = QPushButton(ui_text(locale, UiCopyKey.PRACTICE_REVIEW))
        self._review_button.setObjectName("guidedPracticeReviewButton")
        self._review_button.setCheckable(True)
        self._review_button.clicked.connect(self.mark_review)

        assessment_layout.addWidget(assessment_label)
        assessment_layout.addWidget(self._solved_button)
        assessment_layout.addWidget(self._review_button)
        assessment_layout.addStretch(1)
        solution_layout.addWidget(self._assessment_actions)

        self._solution_panel.hide()
        layout.addWidget(self._solution_panel)

    @property
    def exercise_id(self) -> str:
        """Return the stable authored exercise identifier."""
        return self._exercise.exercise_id

    @property
    def visible_hint_count(self) -> int:
        """Return how many progressive hints are currently visible."""
        return self._visible_hint_count

    @property
    def hint_text(self) -> str:
        """Return the visible hint text."""
        return self._hint.text()

    @property
    def solution_revealed(self) -> bool:
        """Return whether the reference solution panel is visible."""
        return not self._solution_panel.isHidden()

    @property
    def solution_text(self) -> str:
        """Return the authored reference solution."""
        return self._solution.text()

    @property
    def answer_text(self) -> str:
        """Return the student's current workspace text."""
        return self._answer_editor.toPlainText()

    @property
    def assessment_state(self) -> str:
        """Return the student's current self-assessment state."""
        return self._assessment_state

    @Slot()
    def show_next_hint(self) -> None:
        """Reveal the next authored hint without exposing the solution."""
        if self._visible_hint_count >= len(self._exercise.hints):
            return

        self._visible_hint_count += 1
        visible_hints = self._exercise.hints[: self._visible_hint_count]
        self._hint.setText(
            "\n".join(
                ui_text(
                    self._locale,
                    UiCopyKey.PRACTICE_HINT_NUMBER,
                    number=index,
                    hint=hint,
                )
                for index, hint in enumerate(visible_hints, start=1)
            )
        )
        self._hint.show()

        if self._visible_hint_count == len(self._exercise.hints):
            self._hint_button.setText(
                ui_text(self._locale, UiCopyKey.PRACTICE_NO_MORE_HINTS)
            )
            self._hint_button.setEnabled(False)
        else:
            self._hint_button.setText(
                ui_text(self._locale, UiCopyKey.PRACTICE_SHOW_NEXT_HINT)
            )

    @Slot()
    def reveal_solution(self) -> None:
        """Reveal the authored solution and enable student self-assessment."""
        self._solution_panel.show()
        self._solution_button.setText(
            ui_text(self._locale, UiCopyKey.PRACTICE_SOLUTION_VISIBLE)
        )
        self._solution_button.setEnabled(False)

    @Slot()
    def mark_solved(self) -> None:
        """Record that the student considers the exercise solved."""
        self._set_assessment("solved")

    @Slot()
    def mark_review(self) -> None:
        """Record that the student wants to revisit the exercise."""
        self._set_assessment("review")

    def _set_assessment(self, state: str) -> None:
        if not self.solution_revealed:
            return
        self._assessment_state = state
        self._solved_button.setChecked(state == "solved")
        self._review_button.setChecked(state == "review")
        self.self_assessed.emit(self.exercise_id, state)

    def _activity_label(self, value: str) -> str:
        key = _ACTIVITY_KEYS.get(value)
        if key is not None:
            return self._translator.text(key)
        return value.replace("_", " ").capitalize()


class GuidedPracticeWidget(QWidget):
    """Manage repeated localized guided-practice sessions."""

    def __init__(
        self,
        bank: tuple[PracticeExercise, ...],
        *,
        exercise_count: int = 4,
        generator: GuidedPracticeSessionGenerator | None = None,
        locale: AppLocale = DEFAULT_LOCALE,
        parent: QWidget | None = None,
    ) -> None:
        super().__init__(parent)
        self.setObjectName("guidedPracticeWidget")
        self.setStyleSheet(GUIDED_PRACTICE_STYLESHEET)
        self._locale = locale

        self._generator = generator or GuidedPracticeSessionGenerator(
            bank,
            exercise_count=exercise_count,
        )
        self._results: dict[str, str] = {}
        self._current_exercise_ids: tuple[str, ...] = ()
        self._exercise_cards: list[GuidedPracticeCard] = []

        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(14)

        header = QFrame()
        header.setObjectName("guidedPracticeHeader")
        header_layout = QHBoxLayout(header)
        header_layout.setContentsMargins(18, 14, 18, 14)
        header_layout.setSpacing(14)

        header_text = QWidget()
        header_text_layout = QVBoxLayout(header_text)
        header_text_layout.setContentsMargins(0, 0, 0, 0)
        header_text_layout.setSpacing(3)

        title = QLabel(ui_text(locale, UiCopyKey.PRACTICE_TITLE))
        title.setObjectName("guidedPracticeTitle")
        header_text_layout.addWidget(title)

        self._metadata = QLabel()
        self._metadata.setObjectName("guidedPracticeMetadata")
        self._metadata.setWordWrap(True)
        header_text_layout.addWidget(self._metadata)

        self._progress = QLabel()
        self._progress.setObjectName("guidedPracticeProgress")

        self._new_session_button = QPushButton(
            ui_text(locale, UiCopyKey.PRACTICE_NEW_SESSION)
        )
        self._new_session_button.setObjectName("newGuidedPracticeButton")
        self._new_session_button.clicked.connect(self.new_session)

        header_layout.addWidget(header_text, 1)
        header_layout.addWidget(self._progress)
        header_layout.addWidget(self._new_session_button)
        layout.addWidget(header)

        self._cards_container = QWidget()
        self._cards_container.setObjectName("guidedPracticeCards")
        self._cards_layout = QVBoxLayout(self._cards_container)
        self._cards_layout.setContentsMargins(0, 0, 0, 0)
        self._cards_layout.setSpacing(12)
        layout.addWidget(self._cards_container)

        self.new_session()

    @property
    def current_exercise_ids(self) -> tuple[str, ...]:
        """Return IDs for the current randomized practice session."""
        return self._current_exercise_ids

    @property
    def exercise_cards(self) -> tuple[GuidedPracticeCard, ...]:
        """Return current practice cards in display order."""
        return tuple(self._exercise_cards)

    @property
    def progress_text(self) -> str:
        """Return the visible self-assessment summary."""
        return self._progress.text()

    @Slot()
    def new_session(self) -> None:
        """Replace the current session with a new non-identical random sample."""
        session = self._generator.new_session()
        self._results.clear()
        self._current_exercise_ids = session.exercise_ids
        self._exercise_cards.clear()
        self._clear_cards()

        for number, exercise in enumerate(session.exercises, start=1):
            card = GuidedPracticeCard(number, exercise, locale=self._locale)
            card.self_assessed.connect(self._record_self_assessment)
            self._exercise_cards.append(card)
            self._cards_layout.addWidget(card)

        self._metadata.setText(
            ui_text(
                self._locale,
                UiCopyKey.PRACTICE_METADATA,
                count=self._generator.exercise_count,
                bank=self._generator.bank_size,
            )
        )
        self._update_progress()

    @Slot(str, str)
    def _record_self_assessment(self, exercise_id: str, state: str) -> None:
        self._results[exercise_id] = state
        self._update_progress()

    def _update_progress(self) -> None:
        solved = sum(state == "solved" for state in self._results.values())
        review = sum(state == "review" for state in self._results.values())
        assessed = len(self._results)
        total = self._generator.exercise_count
        self._progress.setText(
            ui_text(
                self._locale,
                UiCopyKey.PRACTICE_PROGRESS,
                solved=solved,
                review=review,
                assessed=assessed,
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


__all__ = ["GuidedPracticeCard", "GuidedPracticeWidget"]
