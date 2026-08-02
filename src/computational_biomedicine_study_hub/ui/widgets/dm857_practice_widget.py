"""DM857 practice surfaces with blank executable workspaces."""

from __future__ import annotations

from PySide6.QtCore import Slot
from PySide6.QtWidgets import QVBoxLayout, QWidget

from ...content.models import LearningModule, PracticeExercise
from ...i18n import DEFAULT_LOCALE, AppLocale, UiCopyKey, ui_text
from ...learning.guided_practice import GuidedPracticeSessionGenerator
from ...learning.progress_service import ObjectiveAttemptRecorder
from ...learning.python_challenge import PythonChallengeRunner
from .guided_practice_widget import GuidedPracticeCard, GuidedPracticeWidget
from .python_lab_widget import PythonLabWidget


class DM857PracticeCard(GuidedPracticeCard):
    """Start coding practice blank and make untested code prompts executable."""

    def __init__(
        self,
        number: int,
        exercise: PracticeExercise,
        parent: QWidget | None = None,
        *,
        locale: AppLocale = DEFAULT_LOCALE,
        challenge_runner: PythonChallengeRunner | None = None,
        progress_recorder: ObjectiveAttemptRecorder | None = None,
        learning_module: LearningModule | None = None,
    ) -> None:
        super().__init__(
            number,
            exercise,
            parent,
            locale=locale,
            challenge_runner=challenge_runner,
            progress_recorder=progress_recorder,
            learning_module=learning_module,
        )
        self._exploration_lab: PythonLabWidget | None = None

        if self._challenge_widget is not None:
            self._challenge_widget.set_source("")
            return

        if self._answer_editor is None or not exercise.starter_code:
            return

        lab = PythonLabWidget("", locale=locale)
        layout = self.layout()
        if not isinstance(layout, QVBoxLayout):
            raise RuntimeError("DM857 practice cards require a vertical layout.")
        layout.replaceWidget(self._answer_editor, lab)
        self._answer_editor.setParent(None)
        self._answer_editor.deleteLater()
        self._answer_editor = None
        self._exploration_lab = lab

    @property
    def answer_text(self) -> str:
        """Return code from the active blank executable workspace."""

        if self._exploration_lab is not None:
            return self._exploration_lab.source
        return super().answer_text

    @property
    def exploration_lab(self) -> PythonLabWidget | None:
        """Return the free-execution lab used by an untested code exercise."""

        return self._exploration_lab


class DM857GuidedPracticeWidget(GuidedPracticeWidget):
    """Build randomized DM857 sessions with blank executable coding cards."""

    def __init__(
        self,
        bank: tuple[PracticeExercise, ...],
        *,
        exercise_count: int = 4,
        generator: GuidedPracticeSessionGenerator | None = None,
        locale: AppLocale = DEFAULT_LOCALE,
        challenge_runner: PythonChallengeRunner | None = None,
        progress_recorder: ObjectiveAttemptRecorder | None = None,
        learning_module: LearningModule | None = None,
        parent: QWidget | None = None,
    ) -> None:
        super().__init__(
            bank,
            exercise_count=exercise_count,
            generator=generator,
            locale=locale,
            challenge_runner=challenge_runner,
            progress_recorder=progress_recorder,
            learning_module=learning_module,
            parent=parent,
        )

    @Slot()
    def new_session(self) -> None:
        """Replace the session using DM857-specific executable cards."""

        session = self._generator.new_session()
        self._results.clear()
        self._current_exercise_ids = session.exercise_ids
        self._exercise_cards.clear()
        self._clear_cards()

        for number, exercise in enumerate(session.exercises, start=1):
            card = DM857PracticeCard(
                number,
                exercise,
                locale=self._locale,
                challenge_runner=self._challenge_runner,
                progress_recorder=self._progress_recorder,
                learning_module=self._learning_module,
            )
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


__all__ = ["DM857GuidedPracticeWidget", "DM857PracticeCard"]
