from __future__ import annotations

from PySide6.QtCore import Qt
from PySide6.QtWidgets import QComboBox

from computational_biomedicine_study_hub.content import (
    AssessmentItem,
    AssessmentOption,
    ClozeGap,
)
from computational_biomedicine_study_hub.i18n import AppLocale
from computational_biomedicine_study_hub.learning import ActivityType
from computational_biomedicine_study_hub.learning.progress import AttemptOutcome
from computational_biomedicine_study_hub.ui.activities import (
    ClozeChoiceActivityWidget,
    FillBlankActivityWidget,
    MatchingActivityWidget,
    MultipleChoiceActivityWidget,
    OpenResponseActivityWidget,
    OrderingActivityWidget,
    create_default_activity_registry,
)

OPTION_TYPES = {
    ActivityType.MULTIPLE_CHOICE,
    ActivityType.MULTIPLE_SELECT,
    ActivityType.TRUE_FALSE,
    ActivityType.MATCHING,
    ActivityType.ORDERING,
}


def _item(activity_type: ActivityType) -> AssessmentItem:
    if activity_type is ActivityType.CLOZE_CHOICE:
        return AssessmentItem(
            item_id="cloze",
            activity_type=activity_type,
            prompt="A {first} and {second}.",
            options=(),
            correct_answers=(),
            explanation="Reference explanation.",
            cloze_gaps=(
                ClozeGap(
                    "first",
                    (AssessmentOption("a", "A"), AssessmentOption("b", "B")),
                    "a",
                ),
                ClozeGap(
                    "second",
                    (AssessmentOption("c", "C"), AssessmentOption("d", "D")),
                    "d",
                ),
            ),
        )
    if activity_type in OPTION_TYPES:
        if activity_type is ActivityType.MATCHING:
            options = ("A → 1", "B → 2", "C → 3")
            option_ids = ("a", "b", "c")
            correct_ids = option_ids
            correct = options
        elif activity_type is ActivityType.ORDERING:
            options = ("Second", "First", "Third")
            option_ids = ("second", "first", "third")
            correct_ids = ("first", "second", "third")
            correct = ("First", "Second", "Third")
        else:
            options = ("Correct", "Wrong", "Also correct")
            option_ids = ("correct", "wrong", "also")
            correct_ids = (
                ("correct", "also")
                if activity_type is ActivityType.MULTIPLE_SELECT
                else ("correct",)
            )
            correct = (
                ("Correct", "Also correct")
                if activity_type is ActivityType.MULTIPLE_SELECT
                else ("Correct",)
            )
        return AssessmentItem(
            item_id=f"item-{activity_type.value}",
            activity_type=activity_type,
            prompt="Choose.",
            options=options,
            correct_answers=correct,
            explanation="Reference explanation.",
            option_ids=option_ids,
            correct_option_ids=correct_ids,
        )
    return AssessmentItem(
        item_id=f"item-{activity_type.value}",
        activity_type=activity_type,
        prompt="Respond.",
        options=(),
        correct_answers=("Authored reference",),
        explanation="Reference explanation.",
        rubric=("Criterion one", "Criterion two"),
    )


def test_default_registry_has_a_renderer_for_every_activity_type(qtbot) -> None:
    registry = create_default_activity_registry()

    rendered = {kind: registry.render(_item(kind)) for kind in ActivityType}
    for widget in rendered.values():
        qtbot.addWidget(widget)

    assert set(registry) == set(ActivityType)
    assert isinstance(rendered[ActivityType.MULTIPLE_CHOICE], MultipleChoiceActivityWidget)
    assert isinstance(rendered[ActivityType.MULTIPLE_SELECT], MultipleChoiceActivityWidget)
    assert isinstance(rendered[ActivityType.TRUE_FALSE], MultipleChoiceActivityWidget)
    assert isinstance(rendered[ActivityType.FILL_IN_THE_BLANK], FillBlankActivityWidget)
    assert isinstance(rendered[ActivityType.CLOZE_CHOICE], ClozeChoiceActivityWidget)
    assert isinstance(rendered[ActivityType.MATCHING], MatchingActivityWidget)
    assert isinstance(rendered[ActivityType.ORDERING], OrderingActivityWidget)
    assert isinstance(rendered[ActivityType.ORAL_EXPLANATION], OpenResponseActivityWidget)


def test_objective_choice_renderer_grades_by_option_id(qtbot) -> None:
    widget = MultipleChoiceActivityWidget(
        _item(ActivityType.MULTIPLE_CHOICE),
        locale=AppLocale.DANISH_DENMARK,
    )
    qtbot.addWidget(widget)

    widget.option_controls[0].setChecked(True)
    widget.submit_answer()

    assert widget.last_submission is not None
    assert widget.last_submission.selected_option_ids == ("correct",)
    assert widget.last_submission.is_correct is True


def test_multiple_select_renderer_requires_the_exact_option_id_set(qtbot) -> None:
    widget = MultipleChoiceActivityWidget(
        _item(ActivityType.MULTIPLE_SELECT),
        multiple=True,
    )
    qtbot.addWidget(widget)

    widget.option_controls[0].setChecked(True)
    widget.submit_answer()
    assert widget.last_submission is not None
    assert widget.last_submission.is_correct is False

    widget.option_controls[2].setChecked(True)
    widget.submit_answer()
    assert widget.last_submission is not None
    assert widget.last_submission.is_correct is True


def test_fill_blank_renderer_normalizes_free_text_deterministically(qtbot) -> None:
    widget = FillBlankActivityWidget(_item(ActivityType.FILL_IN_THE_BLANK))
    qtbot.addWidget(widget)
    widget.answer_editor.setPlainText("  AUTHORED   reference ")

    widget.submit_answer()

    assert widget.last_submission is not None
    assert widget.last_submission.is_correct is True


def test_cloze_renderer_grades_each_gap_by_id(qtbot) -> None:
    widget = ClozeChoiceActivityWidget(_item(ActivityType.CLOZE_CHOICE))
    qtbot.addWidget(widget)
    selectors = widget.findChildren(QComboBox)
    selectors[0].setCurrentIndex(selectors[0].findData("a"))
    selectors[1].setCurrentIndex(selectors[1].findData("d"))

    widget.submit_answer()

    assert widget.last_submission is not None
    assert widget.last_submission.keyed_option_ids == (("first", "a"), ("second", "d"))
    assert widget.last_submission.is_correct is True


def test_matching_renderer_uses_stable_pair_ids(qtbot) -> None:
    widget = MatchingActivityWidget(_item(ActivityType.MATCHING))
    qtbot.addWidget(widget)
    selectors = widget.findChildren(QComboBox)
    for selector, expected in zip(selectors, ("a", "b", "c"), strict=True):
        selector.setCurrentIndex(selector.findData(expected))

    widget.submit_answer()

    assert widget.last_submission is not None
    assert widget.last_submission.keyed_option_ids == (("a", "a"), ("b", "b"), ("c", "c"))
    assert widget.last_submission.is_correct is True


def test_ordering_renderer_starts_shuffled_and_checks_sequence_ids(qtbot) -> None:
    item = _item(ActivityType.ORDERING)
    widget = OrderingActivityWidget(item)
    qtbot.addWidget(widget)
    assert widget.current_option_ids() != item.correct_option_ids

    for target_row, expected_id in enumerate(item.correct_option_ids):
        source_row = next(
            row
            for row in range(widget.list_widget.count())
            if widget.list_widget.item(row).data(Qt.ItemDataRole.UserRole) == expected_id
        )
        list_item = widget.list_widget.takeItem(source_row)
        assert list_item is not None
        widget.list_widget.insertItem(target_row, list_item)
    widget.submit_answer()

    assert widget.last_submission is not None
    assert widget.last_submission.is_correct is True


def test_open_renderer_never_claims_objective_grading(qtbot) -> None:
    widget = OpenResponseActivityWidget(_item(ActivityType.ORAL_EXPLANATION))
    qtbot.addWidget(widget)
    widget.answer_editor.setPlainText("My explanation")

    widget.reveal_reference()
    widget.self_assess(AttemptOutcome.PARTIAL)

    assert widget.reference_visible
    assert widget.last_submission is not None
    assert widget.last_submission.outcome is AttemptOutcome.PARTIAL
    assert widget.last_submission.is_correct is None
    assert widget.last_submission.score is None
