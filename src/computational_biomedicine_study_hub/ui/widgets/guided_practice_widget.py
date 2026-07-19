"""Interactive PySide6 widgets for randomized guided formative practice."""

from __future__ import annotations

import random
import uuid
from dataclasses import replace
from datetime import UTC, datetime

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
from ...learning.guided_practice import (
    GuidedPracticeSession,
    GuidedPracticeSessionGenerator,
)
from ...learning.progress import (
    AssessmentScope,
    AssessmentSession,
    AttemptOutcome,
    AttemptRecord,
    LearningItemKind,
    MasteryState,
    PracticeProgress,
    ReviewSchedule,
)
from ...learning.progress_repository import ProgressRepository
from ...learning.spaced_repetition import ReviewRating, reschedule
from ..activities.copy import ActivityCopyKey, activity_text
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

        number_label = QLabel(ui_text(locale, UiCopyKey.PRACTICE_NUMBER, number=number))
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
        self._answer_editor.setAccessibleName(answer_label.text())
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

        self._solution_button = QPushButton(ui_text(locale, UiCopyKey.PRACTICE_REFERENCE_BUTTON))
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

        solution_title = QLabel(ui_text(locale, UiCopyKey.PRACTICE_REFERENCE_TITLE))
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

        assessment_label = QLabel(ui_text(locale, UiCopyKey.PRACTICE_SELF_ASSESSMENT))
        assessment_label.setObjectName("guidedPracticeExerciseType")
        self._solved_button = QPushButton(ui_text(locale, UiCopyKey.PRACTICE_SOLVED))
        self._solved_button.setObjectName("guidedPracticeSolvedButton")
        self._solved_button.setCheckable(True)
        self._solved_button.clicked.connect(self.mark_solved)

        self._partial_button = QPushButton(activity_text(locale, ActivityCopyKey.PARTIAL))
        self._partial_button.setObjectName("guidedPracticePartialButton")
        self._partial_button.setCheckable(True)
        self._partial_button.clicked.connect(self.mark_partial)

        self._review_button = QPushButton(ui_text(locale, UiCopyKey.PRACTICE_REVIEW))
        self._review_button.setObjectName("guidedPracticeReviewButton")
        self._review_button.setCheckable(True)
        self._review_button.clicked.connect(self.mark_review)

        assessment_layout.addWidget(assessment_label)
        assessment_layout.addWidget(self._solved_button)
        assessment_layout.addWidget(self._partial_button)
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

    def set_answer_text(self, text: str) -> None:
        """Set the learner workspace text for restoration and accessible tests."""
        self._answer_editor.setPlainText(text)

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
            self._hint_button.setText(ui_text(self._locale, UiCopyKey.PRACTICE_NO_MORE_HINTS))
            self._hint_button.setEnabled(False)
        else:
            self._hint_button.setText(ui_text(self._locale, UiCopyKey.PRACTICE_SHOW_NEXT_HINT))

    @Slot()
    def reveal_solution(self) -> None:
        """Reveal the authored solution and enable student self-assessment."""
        self._solution_panel.show()
        self._solution_button.setText(ui_text(self._locale, UiCopyKey.PRACTICE_SOLUTION_VISIBLE))
        self._solution_button.setEnabled(False)

    @Slot()
    def mark_solved(self) -> None:
        """Record that the student considers the exercise solved."""
        self._set_assessment("solved")

    @Slot()
    def mark_review(self) -> None:
        """Record that the student wants to revisit the exercise."""
        self._set_assessment("review")

    @Slot()
    def mark_partial(self) -> None:
        """Record that the response is only partially complete."""
        self._set_assessment("partial")

    def restore_progress(self, response_text: str, state: str) -> None:
        """Restore persisted response and self-assessment without emitting a new attempt."""
        self._answer_editor.setPlainText(response_text)
        self.reveal_solution()
        self._assessment_state = state
        self._solved_button.setChecked(state == "solved")
        self._partial_button.setChecked(state == "partial")
        self._review_button.setChecked(state == "review")

    def _set_assessment(self, state: str) -> None:
        if not self.solution_revealed:
            return
        self._assessment_state = state
        self._solved_button.setChecked(state == "solved")
        self._partial_button.setChecked(state == "partial")
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
        repository: ProgressRepository | None = None,
        course_code: str = "",
        module_id: str = "",
        content_version: str = "",
        parent: QWidget | None = None,
    ) -> None:
        super().__init__(parent)
        self.setObjectName("guidedPracticeWidget")
        self.setStyleSheet(GUIDED_PRACTICE_STYLESHEET)
        self._locale = locale
        self._bank = bank
        self._exercise_count = exercise_count
        self._repository = repository
        self._course_code = course_code
        self._module_id = module_id
        self._content_version = content_version
        self._persistent_session: AssessmentSession | None = None
        if repository is not None and not all((course_code, module_id, content_version)):
            raise ValueError(
                "Persistent guided practice requires course, module, and content version."
            )

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

        self._new_session_button = QPushButton(ui_text(locale, UiCopyKey.PRACTICE_NEW_SESSION))
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

        if not self._restore_session():
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
                scope=AssessmentScope.PRACTICE_MODULE,
                course_code=self._course_code,
                module_id=self._module_id,
                item_ids=session.exercise_ids,
                seed=seed,
                locale=self._locale.value,
                started_at=datetime.now(UTC),
            )
            self._repository.save_assessment_session(self._persistent_session)
        self._render_session(session)

    def _render_session(self, session: GuidedPracticeSession) -> None:
        self._results.clear()
        self._current_exercise_ids = session.exercise_ids
        self._exercise_cards.clear()
        self._clear_cards()

        for number, exercise in enumerate(session.exercises, start=1):
            card = GuidedPracticeCard(number, exercise, locale=self._locale)
            if self._repository is not None:
                progress = self._repository.get_practice_progress(
                    self._course_code,
                    self._module_id,
                    exercise.exercise_id,
                )
                if progress is not None:
                    card.restore_progress(
                        progress.response_text,
                        progress.last_outcome.value,
                    )
                    self._results[exercise.exercise_id] = progress.last_outcome.value
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
        if self._repository is not None and self._persistent_session is not None:
            self._persist_self_assessment(exercise_id, AttemptOutcome(state))
        self._update_progress()

    def _persist_self_assessment(
        self,
        exercise_id: str,
        outcome: AttemptOutcome,
    ) -> None:
        assert self._repository is not None
        assert self._persistent_session is not None
        exercise = next(value for value in self._bank if value.exercise_id == exercise_id)
        card = next(value for value in self._exercise_cards if value.exercise_id == exercise_id)
        previous = self._repository.get_practice_progress(
            self._course_code,
            self._module_id,
            exercise_id,
        )
        now = datetime.now(UTC)
        attempt_count = 1 if previous is None else previous.attempt_count + 1
        mastery = (
            MasteryState.REVIEWING if outcome is AttemptOutcome.SOLVED else MasteryState.LEARNING
        )
        self._repository.record_attempt(
            AttemptRecord(
                attempt_id=str(uuid.uuid4()),
                course_code=self._course_code,
                module_id=self._module_id,
                item_id=exercise_id,
                item_kind=LearningItemKind.PRACTICE,
                activity_type=exercise.activity_type,
                outcome=outcome,
                locale=self._locale.value,
                content_version=self._content_version,
                created_at=now,
                response_text=card.answer_text,
                session_id=self._persistent_session.session_id,
            )
        )
        self._repository.save_practice_progress(
            PracticeProgress(
                course_code=self._course_code,
                module_id=self._module_id,
                exercise_id=exercise_id,
                mastery_state=mastery,
                attempt_count=attempt_count,
                last_outcome=outcome,
                updated_at=now,
                response_text=card.answer_text,
            )
        )
        initial = ReviewSchedule(
            course_code=self._course_code,
            module_id=self._module_id,
            item_id=exercise_id,
            item_kind=LearningItemKind.PRACTICE,
            mastery_state=MasteryState.NEW,
            repetitions=0,
            interval_days=0,
            easiness=2.5,
            due_at=now,
        )
        if outcome is AttemptOutcome.SOLVED:
            schedule = reschedule(initial, ReviewRating.GOOD, reviewed_at=now)
        else:
            schedule = replace(
                initial,
                mastery_state=MasteryState.LEARNING,
                easiness=2.35 if outcome is AttemptOutcome.PARTIAL else 2.3,
            )
        self._repository.save_review_schedule(schedule)
        if exercise_id not in self._persistent_session.answered_item_ids:
            self._persistent_session = replace(
                self._persistent_session,
                answered_item_ids=(self._persistent_session.answered_item_ids + (exercise_id,)),
            )
            self._repository.save_assessment_session(self._persistent_session)

    def _restore_session(self) -> bool:
        if self._repository is None:
            return False
        persistent = self._repository.latest_open_assessment_session(
            course_code=self._course_code,
            module_id=self._module_id,
            scope=AssessmentScope.PRACTICE_MODULE.value,
        )
        if persistent is None:
            return False
        session = self._session_for_seed(persistent.seed)
        if session.exercise_ids != persistent.item_ids:
            return False
        self._persistent_session = persistent
        self._render_session(session)
        return True

    def _session_for_seed(self, seed: int) -> GuidedPracticeSession:
        return GuidedPracticeSessionGenerator(
            self._bank,
            exercise_count=self._exercise_count,
            rng=random.Random(seed),
        ).new_session()

    def _update_progress(self) -> None:
        solved = sum(state == "solved" for state in self._results.values())
        partial = sum(state == "partial" for state in self._results.values())
        review = sum(state == "review" for state in self._results.values())
        assessed = len(self._results)
        total = self._generator.exercise_count
        self._progress.setText(
            ui_text(
                self._locale,
                UiCopyKey.PRACTICE_PROGRESS,
                solved=solved,
                review=review + partial,
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
