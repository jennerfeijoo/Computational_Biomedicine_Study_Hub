"""Interactive widgets for authored assessment activities.

No widget executes learner code. Code-oriented activities use authored references and
rubrics with explicit self-assessment until a separately sandboxed runner is available.
"""

from __future__ import annotations

from collections.abc import Iterable

from PySide6.QtCore import Qt, Signal, Slot
from PySide6.QtWidgets import (
    QAbstractItemView,
    QCheckBox,
    QComboBox,
    QFrame,
    QHBoxLayout,
    QLabel,
    QListWidget,
    QListWidgetItem,
    QPlainTextEdit,
    QPushButton,
    QRadioButton,
    QVBoxLayout,
    QWidget,
)

from ...content.models import AssessmentItem
from ...i18n import DEFAULT_LOCALE, AppLocale
from ...learning.activity_submission import ActivitySubmission
from ...learning.cloze import evaluate_cloze
from ...learning.progress import AttemptOutcome
from .copy import ActivityCopyKey, activity_text


class ActivityWidget(QFrame):
    """Base widget exposing one renderer-neutral submission signal."""

    submitted = Signal(object)

    def __init__(
        self,
        item: AssessmentItem,
        *,
        locale: AppLocale = DEFAULT_LOCALE,
        parent: QWidget | None = None,
    ) -> None:
        super().__init__(parent)
        self.setObjectName("activityWidget")
        self.setFrameShape(QFrame.Shape.StyledPanel)
        self._item = item
        self._locale = locale
        self._last_submission: ActivitySubmission | None = None
        self.setAccessibleName(item.prompt)

    @property
    def item_id(self) -> str:
        return self._item.item_id

    @property
    def last_submission(self) -> ActivitySubmission | None:
        return self._last_submission

    def _prompt(self, layout: QVBoxLayout, text: str | None = None) -> None:
        prompt = QLabel(text or self._item.prompt)
        prompt.setObjectName("activityPrompt")
        prompt.setWordWrap(True)
        prompt.setTextInteractionFlags(Qt.TextInteractionFlag.TextSelectableByMouse)
        layout.addWidget(prompt)

    def _feedback_label(self, layout: QVBoxLayout) -> QLabel:
        feedback = QLabel()
        feedback.setObjectName("activityFeedback")
        feedback.setWordWrap(True)
        feedback.hide()
        layout.addWidget(feedback)
        return feedback

    def _publish(self, submission: ActivitySubmission) -> None:
        self._last_submission = submission
        self.submitted.emit(submission)

    def _objective_feedback(self, correct: bool) -> str:
        lead = activity_text(
            self._locale,
            ActivityCopyKey.CORRECT if correct else ActivityCopyKey.INCORRECT,
        )
        return f"{lead}\n{self._item.explanation}"


class MultipleChoiceActivityWidget(ActivityWidget):
    """Single- or multiple-selection activity graded by option IDs."""

    def __init__(
        self,
        item: AssessmentItem,
        *,
        multiple: bool = False,
        locale: AppLocale = DEFAULT_LOCALE,
        parent: QWidget | None = None,
    ) -> None:
        super().__init__(item, locale=locale, parent=parent)
        self.setObjectName(
            "multipleSelectActivityWidget" if multiple else "multipleChoiceActivityWidget"
        )
        self._multiple = multiple
        self._controls: list[tuple[QCheckBox | QRadioButton, str]] = []
        layout = QVBoxLayout(self)
        self._prompt(layout)
        for option in item.option_objects:
            control: QCheckBox | QRadioButton
            if multiple:
                control = QCheckBox(option.text)
            else:
                control = QRadioButton(option.text)
            control.setAccessibleName(option.text)
            self._controls.append((control, option.option_id))
            layout.addWidget(control)
        submit = QPushButton(activity_text(locale, ActivityCopyKey.SUBMIT))
        submit.setObjectName("activitySubmitButton")
        submit.clicked.connect(self.submit_answer)
        layout.addWidget(submit)
        self._feedback = self._feedback_label(layout)

    @property
    def option_controls(self) -> tuple[QCheckBox | QRadioButton, ...]:
        return tuple(control for control, _ in self._controls)

    @Slot()
    def submit_answer(self) -> None:
        selected = tuple(option_id for control, option_id in self._controls if control.isChecked())
        if not selected:
            self._feedback.setText(activity_text(self._locale, ActivityCopyKey.CHOOSE))
            self._feedback.show()
            return
        correct = set(selected) == set(self._item.correct_option_ids)
        self._feedback.setText(self._objective_feedback(correct))
        self._feedback.show()
        self._publish(
            ActivitySubmission(
                item_id=self.item_id,
                outcome=AttemptOutcome.SOLVED if correct else AttemptOutcome.REVIEW,
                selected_option_ids=selected,
                is_correct=correct,
                score=float(correct),
            )
        )


class FillBlankActivityWidget(ActivityWidget):
    """Free-text fill-in activity with deterministic authored-answer matching."""

    def __init__(
        self,
        item: AssessmentItem,
        *,
        locale: AppLocale = DEFAULT_LOCALE,
        parent: QWidget | None = None,
    ) -> None:
        super().__init__(item, locale=locale, parent=parent)
        self.setObjectName("fillBlankActivityWidget")
        layout = QVBoxLayout(self)
        self._prompt(layout)
        self.answer_editor = QPlainTextEdit()
        self.answer_editor.setObjectName("fillBlankAnswerEditor")
        self.answer_editor.setAccessibleName(activity_text(locale, ActivityCopyKey.YOUR_ANSWER))
        self.answer_editor.setMinimumHeight(80)
        layout.addWidget(self.answer_editor)
        submit = QPushButton(activity_text(locale, ActivityCopyKey.SUBMIT))
        submit.setObjectName("activitySubmitButton")
        submit.clicked.connect(self.submit_answer)
        layout.addWidget(submit)
        self._feedback = self._feedback_label(layout)

    @Slot()
    def submit_answer(self) -> None:
        response = self.answer_editor.toPlainText().strip()
        if not response:
            self._feedback.setText(activity_text(self._locale, ActivityCopyKey.CHOOSE))
            self._feedback.show()
            return
        normalized = " ".join(response.casefold().split())
        accepted = {" ".join(answer.casefold().split()) for answer in self._item.correct_answers}
        correct = normalized in accepted
        self._feedback.setText(self._objective_feedback(correct))
        self._feedback.show()
        self._publish(
            ActivitySubmission(
                item_id=self.item_id,
                outcome=AttemptOutcome.SOLVED if correct else AttemptOutcome.REVIEW,
                response_text=response,
                is_correct=correct,
                score=float(correct),
            )
        )


class ClozeChoiceActivityWidget(ActivityWidget):
    """One or more cloze gaps graded by stable gap and option IDs."""

    def __init__(
        self,
        item: AssessmentItem,
        *,
        locale: AppLocale = DEFAULT_LOCALE,
        parent: QWidget | None = None,
    ) -> None:
        super().__init__(item, locale=locale, parent=parent)
        self.setObjectName("clozeChoiceActivityWidget")
        self._selectors: list[tuple[str, QComboBox]] = []
        layout = QVBoxLayout(self)
        rendered_prompt = item.prompt
        for gap in item.cloze_gaps:
            rendered_prompt = rendered_prompt.replace(
                "{" + gap.gap_id + "}",
                f"____ [{gap.gap_id}] ____",
            )
        self._prompt(layout, rendered_prompt)
        for index, gap in enumerate(item.cloze_gaps, start=1):
            row = QHBoxLayout()
            label = QLabel(f"{activity_text(locale, ActivityCopyKey.GAP)} {index} ({gap.gap_id})")
            selector = QComboBox()
            selector.setObjectName(f"clozeGap_{gap.gap_id}")
            selector.setAccessibleName(label.text())
            selector.addItem(activity_text(locale, ActivityCopyKey.CHOOSE), None)
            for option in gap.options:
                selector.addItem(option.text, option.option_id)
            row.addWidget(label)
            row.addWidget(selector, 1)
            layout.addLayout(row)
            self._selectors.append((gap.gap_id, selector))
        submit = QPushButton(activity_text(locale, ActivityCopyKey.SUBMIT))
        submit.setObjectName("activitySubmitButton")
        submit.clicked.connect(self.submit_answer)
        layout.addWidget(submit)
        self._feedback = self._feedback_label(layout)

    @Slot()
    def submit_answer(self) -> None:
        answers: dict[str, str] = {}
        for gap_id, selector in self._selectors:
            selected = selector.currentData()
            if not isinstance(selected, str):
                self._feedback.setText(activity_text(self._locale, ActivityCopyKey.CHOOSE))
                self._feedback.show()
                return
            answers[gap_id] = selected
        correct = evaluate_cloze(self._item, answers)
        self._feedback.setText(self._objective_feedback(correct))
        self._feedback.show()
        keyed = tuple(answers.items())
        self._publish(
            ActivitySubmission(
                item_id=self.item_id,
                outcome=AttemptOutcome.SOLVED if correct else AttemptOutcome.REVIEW,
                selected_option_ids=tuple(answers.values()),
                keyed_option_ids=keyed,
                is_correct=correct,
                score=float(correct),
            )
        )


def _split_match_option(text: str) -> tuple[str, str]:
    for delimiter in ("→", "->", "⟶"):
        if delimiter in text:
            left, right = text.split(delimiter, maxsplit=1)
            return left.strip(), right.strip()
    return text, text


class MatchingActivityWidget(ActivityWidget):
    """Match each authored left-hand side to a right-hand option by stable ID."""

    def __init__(
        self,
        item: AssessmentItem,
        *,
        locale: AppLocale = DEFAULT_LOCALE,
        parent: QWidget | None = None,
    ) -> None:
        super().__init__(item, locale=locale, parent=parent)
        self.setObjectName("matchingActivityWidget")
        self._selectors: list[tuple[str, QComboBox]] = []
        pairs = tuple(
            (option.option_id, *_split_match_option(option.text)) for option in item.option_objects
        )
        layout = QVBoxLayout(self)
        self._prompt(layout)
        for option_id, left, _ in pairs:
            row = QHBoxLayout()
            label = QLabel(left)
            label.setWordWrap(True)
            selector = QComboBox()
            selector.setAccessibleName(
                f"{left}: {activity_text(locale, ActivityCopyKey.MATCH_WITH)}"
            )
            selector.addItem(activity_text(locale, ActivityCopyKey.MATCH_WITH), None)
            for right_id, _, right in reversed(pairs):
                selector.addItem(right, right_id)
            row.addWidget(label, 1)
            row.addWidget(selector, 1)
            layout.addLayout(row)
            self._selectors.append((option_id, selector))
        submit = QPushButton(activity_text(locale, ActivityCopyKey.SUBMIT))
        submit.setObjectName("activitySubmitButton")
        submit.clicked.connect(self.submit_answer)
        layout.addWidget(submit)
        self._feedback = self._feedback_label(layout)

    @Slot()
    def submit_answer(self) -> None:
        matches: list[tuple[str, str]] = []
        for left_id, selector in self._selectors:
            right_id = selector.currentData()
            if not isinstance(right_id, str):
                self._feedback.setText(activity_text(self._locale, ActivityCopyKey.CHOOSE))
                self._feedback.show()
                return
            matches.append((left_id, right_id))
        correct = all(left_id == right_id for left_id, right_id in matches)
        self._feedback.setText(self._objective_feedback(correct))
        self._feedback.show()
        self._publish(
            ActivitySubmission(
                item_id=self.item_id,
                outcome=AttemptOutcome.SOLVED if correct else AttemptOutcome.REVIEW,
                selected_option_ids=tuple(right for _, right in matches),
                keyed_option_ids=tuple(matches),
                is_correct=correct,
                score=float(correct),
            )
        )


class OrderingActivityWidget(ActivityWidget):
    """Reorder stable option IDs with keyboard-operable buttons or drag and drop."""

    def __init__(
        self,
        item: AssessmentItem,
        *,
        locale: AppLocale = DEFAULT_LOCALE,
        parent: QWidget | None = None,
    ) -> None:
        super().__init__(item, locale=locale, parent=parent)
        self.setObjectName("orderingActivityWidget")
        layout = QVBoxLayout(self)
        self._prompt(layout)
        self.list_widget = QListWidget()
        self.list_widget.setObjectName("orderingList")
        self.list_widget.setDragDropMode(QAbstractItemView.DragDropMode.InternalMove)
        self.list_widget.setDefaultDropAction(Qt.DropAction.MoveAction)
        text_by_id = {option.option_id: option.text for option in item.option_objects}
        initial_ids = item.correct_option_ids[1:] + item.correct_option_ids[:1]
        for option_id in initial_ids:
            row = QListWidgetItem(text_by_id[option_id])
            row.setData(Qt.ItemDataRole.UserRole, option_id)
            self.list_widget.addItem(row)
        layout.addWidget(self.list_widget)
        actions = QHBoxLayout()
        up = QPushButton(activity_text(locale, ActivityCopyKey.MOVE_UP))
        down = QPushButton(activity_text(locale, ActivityCopyKey.MOVE_DOWN))
        up.setObjectName("orderingMoveUpButton")
        down.setObjectName("orderingMoveDownButton")
        up.clicked.connect(self.move_up)
        down.clicked.connect(self.move_down)
        actions.addWidget(up)
        actions.addWidget(down)
        actions.addStretch(1)
        layout.addLayout(actions)
        submit = QPushButton(activity_text(locale, ActivityCopyKey.SUBMIT))
        submit.setObjectName("activitySubmitButton")
        submit.clicked.connect(self.submit_answer)
        layout.addWidget(submit)
        self._feedback = self._feedback_label(layout)

    def current_option_ids(self) -> tuple[str, ...]:
        return tuple(
            str(self.list_widget.item(index).data(Qt.ItemDataRole.UserRole))
            for index in range(self.list_widget.count())
        )

    @Slot()
    def move_up(self) -> None:
        row = self.list_widget.currentRow()
        if row <= 0:
            return
        item = self.list_widget.takeItem(row)
        if item is not None:
            self.list_widget.insertItem(row - 1, item)
            self.list_widget.setCurrentRow(row - 1)

    @Slot()
    def move_down(self) -> None:
        row = self.list_widget.currentRow()
        if row < 0 or row >= self.list_widget.count() - 1:
            return
        item = self.list_widget.takeItem(row)
        if item is not None:
            self.list_widget.insertItem(row + 1, item)
            self.list_widget.setCurrentRow(row + 1)

    @Slot()
    def submit_answer(self) -> None:
        selected = self.current_option_ids()
        correct = selected == self._item.correct_option_ids
        self._feedback.setText(self._objective_feedback(correct))
        self._feedback.show()
        self._publish(
            ActivitySubmission(
                item_id=self.item_id,
                outcome=AttemptOutcome.SOLVED if correct else AttemptOutcome.REVIEW,
                selected_option_ids=selected,
                is_correct=correct,
                score=float(correct),
            )
        )


class OpenResponseActivityWidget(ActivityWidget):
    """Honest open response with reference, rubric, and three-way self-assessment."""

    feedback_requested = Signal(str)

    def __init__(
        self,
        item: AssessmentItem,
        *,
        locale: AppLocale = DEFAULT_LOCALE,
        parent: QWidget | None = None,
    ) -> None:
        super().__init__(item, locale=locale, parent=parent)
        self.setObjectName("openResponseActivityWidget")
        layout = QVBoxLayout(self)
        self._prompt(layout)
        answer_label = QLabel(activity_text(locale, ActivityCopyKey.YOUR_ANSWER))
        layout.addWidget(answer_label)
        self.answer_editor = QPlainTextEdit()
        self.answer_editor.setObjectName("openResponseAnswerEditor")
        self.answer_editor.setAccessibleName(answer_label.text())
        self.answer_editor.setMinimumHeight(120)
        layout.addWidget(self.answer_editor)
        confidence_row = QHBoxLayout()
        confidence_row.addWidget(QLabel(activity_text(locale, ActivityCopyKey.CONFIDENCE)))
        self.confidence_selector = QComboBox()
        self.confidence_selector.setObjectName("openResponseConfidence")
        for key, value in (
            (ActivityCopyKey.CONFIDENCE_LOW, "low"),
            (ActivityCopyKey.CONFIDENCE_MEDIUM, "medium"),
            (ActivityCopyKey.CONFIDENCE_HIGH, "high"),
        ):
            self.confidence_selector.addItem(activity_text(locale, key), value)
        self.confidence_selector.setCurrentIndex(1)
        confidence_row.addWidget(self.confidence_selector)
        confidence_row.addStretch(1)
        layout.addLayout(confidence_row)
        feedback = QPushButton(activity_text(locale, ActivityCopyKey.LOCAL_FEEDBACK))
        feedback.setObjectName("requestLocalFeedbackButton")
        feedback.clicked.connect(self.request_feedback)
        layout.addWidget(feedback)
        reveal = QPushButton(activity_text(locale, ActivityCopyKey.REVEAL_REFERENCE))
        reveal.setObjectName("revealReferenceButton")
        reveal.clicked.connect(self.reveal_reference)
        layout.addWidget(reveal)

        self._reference_panel = QFrame()
        self._reference_panel.setObjectName("referencePanel")
        reference_layout = QVBoxLayout(self._reference_panel)
        reference_layout.addWidget(QLabel(activity_text(locale, ActivityCopyKey.REFERENCE)))
        reference = QLabel("\n".join(item.correct_answers))
        reference.setObjectName("referenceAnswer")
        reference.setWordWrap(True)
        reference.setTextInteractionFlags(Qt.TextInteractionFlag.TextSelectableByMouse)
        reference_layout.addWidget(reference)
        explanation = QLabel(item.explanation)
        explanation.setWordWrap(True)
        reference_layout.addWidget(explanation)
        if item.rubric:
            reference_layout.addWidget(QLabel(activity_text(locale, ActivityCopyKey.RUBRIC)))
            rubric = QLabel("\n".join(f"• {criterion}" for criterion in item.rubric))
            rubric.setObjectName("activityRubric")
            rubric.setWordWrap(True)
            reference_layout.addWidget(rubric)
        reference_layout.addWidget(QLabel(activity_text(locale, ActivityCopyKey.SELF_ASSESS)))
        buttons = QHBoxLayout()
        for key, outcome in (
            (ActivityCopyKey.SOLVED, AttemptOutcome.SOLVED),
            (ActivityCopyKey.PARTIAL, AttemptOutcome.PARTIAL),
            (ActivityCopyKey.REVIEW, AttemptOutcome.REVIEW),
        ):
            button = QPushButton(activity_text(locale, key))
            button.setObjectName(f"selfAssess_{outcome.value}")
            button.clicked.connect(lambda checked=False, value=outcome: self.self_assess(value))
            buttons.addWidget(button)
        reference_layout.addLayout(buttons)
        self._reference_panel.hide()
        layout.addWidget(self._reference_panel)

    @property
    def reference_visible(self) -> bool:
        return not self._reference_panel.isHidden()

    @Slot()
    def reveal_reference(self) -> None:
        self._reference_panel.show()

    @property
    def confidence(self) -> str:
        return str(self.confidence_selector.currentData())

    @Slot()
    def request_feedback(self) -> None:
        answer = self.answer_editor.toPlainText().strip()
        if answer:
            self.feedback_requested.emit(answer)

    def self_assess(self, outcome: AttemptOutcome) -> None:
        if not self.reference_visible:
            return
        self._publish(
            ActivitySubmission(
                item_id=self.item_id,
                outcome=outcome,
                response_text=self.answer_editor.toPlainText(),
                is_correct=None,
                score=None,
            )
        )


def widget_submission(widget: ActivityWidget) -> ActivitySubmission | None:
    """Return the latest submission; useful to coordinators and black-box tests."""
    return widget.last_submission


def activity_widgets(values: Iterable[QWidget]) -> tuple[ActivityWidget, ...]:
    """Narrow a heterogeneous widget collection to rendered activities."""
    return tuple(value for value in values if isinstance(value, ActivityWidget))


__all__ = [
    "ActivityWidget",
    "ClozeChoiceActivityWidget",
    "FillBlankActivityWidget",
    "MatchingActivityWidget",
    "MultipleChoiceActivityWidget",
    "OpenResponseActivityWidget",
    "OrderingActivityWidget",
    "activity_widgets",
    "widget_submission",
]
