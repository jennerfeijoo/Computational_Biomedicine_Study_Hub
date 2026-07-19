from __future__ import annotations

import pytest

from computational_biomedicine_study_hub.content import (
    AssessmentItem,
    AssessmentOption,
    ClozeGap,
    LocalizedAssessmentItem,
    LocalizedAssessmentOption,
    LocalizedClozeGap,
    LocalizedText,
)
from computational_biomedicine_study_hub.i18n import AppLocale
from computational_biomedicine_study_hub.learning import ActivityType
from computational_biomedicine_study_hub.learning.cloze import (
    cloze_item_from_dict,
    cloze_item_to_dict,
    evaluate_cloze,
)


def _text(spanish: str, english: str, danish: str) -> LocalizedText:
    return LocalizedText(spanish, english, danish)


def _localized_cloze() -> LocalizedAssessmentItem:
    return LocalizedAssessmentItem(
        item_id="dm857.m02.cloze.001",
        activity_type=ActivityType.CLOZE_CHOICE,
        prompt=_text(
            "Si {condition} entonces se ejecuta {branch}.",
            "If {condition}, then {branch} runs.",
            "Hvis {condition}, så køres {branch}.",
        ),
        options=(),
        correct_option_ids=(),
        accepted_answers=(),
        explanation=_text(
            "La condición controla la rama.",
            "The condition controls the branch.",
            "Betingelsen styrer grenen.",
        ),
        cloze_gaps=(
            LocalizedClozeGap(
                gap_id="condition",
                options=(
                    LocalizedAssessmentOption(
                        "true",
                        _text("es verdadera", "is true", "er sand"),
                    ),
                    LocalizedAssessmentOption(
                        "false",
                        _text("es falsa", "is false", "er falsk"),
                    ),
                ),
                correct_option_id="true",
            ),
            LocalizedClozeGap(
                gap_id="branch",
                options=(
                    LocalizedAssessmentOption(
                        "if",
                        _text("la rama if", "the if branch", "if-grenen"),
                    ),
                    LocalizedAssessmentOption(
                        "else",
                        _text("la rama else", "the else branch", "else-grenen"),
                    ),
                ),
                correct_option_id="if",
            ),
        ),
    )


def test_cloze_materialization_keeps_gap_and_option_ids_across_locales() -> None:
    localized = _localized_cloze()

    spanish = localized.materialize(AppLocale.SPANISH_SPAIN)
    english = localized.materialize(AppLocale.ENGLISH)
    danish = localized.materialize(AppLocale.DANISH_DENMARK)

    assert tuple(gap.gap_id for gap in spanish.cloze_gaps) == ("condition", "branch")
    assert tuple(gap.correct_option_id for gap in english.cloze_gaps) == ("true", "if")
    assert danish.cloze_gaps[0].options[0].text == "er sand"
    assert spanish.cloze_gaps[0].options[0].option_id == "true"


def test_cloze_serialization_round_trip_uses_stable_ids() -> None:
    item = _localized_cloze().materialize(AppLocale.ENGLISH)

    payload = cloze_item_to_dict(item)
    restored = cloze_item_from_dict(payload)

    assert restored == item
    assert payload["gaps"][0]["correct_option_id"] == "true"
    assert payload["gaps"][0]["options"][0]["option_id"] == "true"


def test_cloze_evaluation_requires_every_gap_and_uses_option_ids() -> None:
    item = _localized_cloze().materialize(AppLocale.SPANISH_SPAIN)

    assert evaluate_cloze(item, {"condition": "true", "branch": "if"})
    assert not evaluate_cloze(item, {"condition": "false", "branch": "if"})
    assert not evaluate_cloze(item, {"condition": "true"})


def test_cloze_rejects_missing_prompt_marker_and_unknown_answer_id() -> None:
    options = (
        AssessmentOption("one", "One"),
        AssessmentOption("two", "Two"),
    )
    with pytest.raises(ValueError, match="unknown correct option ID"):
        ClozeGap("gap", options, "missing")

    gap = ClozeGap("gap", options, "one")
    with pytest.raises(ValueError, match="missing prompt markers"):
        AssessmentItem(
            item_id="invalid-cloze",
            activity_type=ActivityType.CLOZE_CHOICE,
            prompt="No marker here",
            options=(),
            correct_answers=(),
            explanation="Explanation",
            cloze_gaps=(gap,),
        )
