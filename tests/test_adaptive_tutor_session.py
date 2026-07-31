from __future__ import annotations

import pytest

from computational_biomedicine_study_hub.tutoring import (
    TutorAssistanceLevel,
    TutorSessionSnapshot,
    TutorSessionTurn,
    bounded_history,
)


def _turn(
    number: int,
    *,
    level: TutorAssistanceLevel = TutorAssistanceLevel.SOCRATIC,
    response: str | None = None,
) -> TutorSessionTurn:
    return TutorSessionTurn(
        question=f"Question {number}",
        response=response or f"Response {number}",
        assistance_level=level,
        model="qwen3.5:9b-q8_0",
        source_ids=(f"source.{number}",),
    )


def test_assistance_levels_have_stable_escalation_order() -> None:
    assert TutorAssistanceLevel.SOCRATIC.next_level is TutorAssistanceLevel.CONCEPTUAL
    assert TutorAssistanceLevel.CONCEPTUAL.next_level is TutorAssistanceLevel.STRUCTURAL
    assert TutorAssistanceLevel.STRUCTURAL.next_level is TutorAssistanceLevel.EXPLANATION
    assert TutorAssistanceLevel.EXPLANATION.next_level is TutorAssistanceLevel.EXPLANATION


def test_snapshot_tracks_help_count_strongest_level_and_solution_support() -> None:
    snapshot = TutorSessionSnapshot()
    snapshot = snapshot.append(_turn(1, level=TutorAssistanceLevel.CONCEPTUAL))
    snapshot = snapshot.append(_turn(2, level=TutorAssistanceLevel.EXPLANATION))

    assert snapshot.assistance_count == 2
    assert snapshot.strongest_level is TutorAssistanceLevel.EXPLANATION
    assert snapshot.solution_revealed


def test_snapshot_rates_latest_turn_without_mutating_previous_turns() -> None:
    snapshot = TutorSessionSnapshot((_turn(1), _turn(2)))

    rated = snapshot.rate_latest(False)

    assert snapshot.turns[-1].helpful is None
    assert rated.turns[0].helpful is None
    assert rated.turns[-1].helpful is False


def test_snapshot_retains_only_the_newest_local_turns() -> None:
    snapshot = TutorSessionSnapshot()
    for number in range(1, 6):
        snapshot = snapshot.append(_turn(number), max_turns=3)

    assert tuple(turn.question for turn in snapshot.turns) == (
        "Question 3",
        "Question 4",
        "Question 5",
    )


def test_bounded_history_keeps_newest_turns_within_character_budget() -> None:
    turns = tuple(_turn(number, response="x" * 500) for number in range(1, 6))

    selected = bounded_history(turns, max_turns=3, max_characters=1_400)

    assert selected
    assert selected[-1].question == "Question 5"
    assert len(selected) <= 3
    assert sum(len(turn.response) for turn in selected) <= 1_400


def test_bounded_history_truncates_one_oversized_latest_response() -> None:
    selected = bounded_history(
        (_turn(1, response="x" * 4_000),),
        max_characters=600,
    )

    assert len(selected) == 1
    assert selected[0].response.endswith("…")
    assert len(selected[0].response) < 600


def test_session_models_reject_invalid_state() -> None:
    with pytest.raises(ValueError, match="source ID"):
        TutorSessionTurn(
            question="Question",
            response="Response",
            assistance_level=TutorAssistanceLevel.SOCRATIC,
            model="model",
            source_ids=(),
        )
    with pytest.raises(ValueError, match="empty tutor session"):
        TutorSessionSnapshot().rate_latest(True)
    with pytest.raises(ValueError, match="max_turns"):
        TutorSessionSnapshot().append(_turn(1), max_turns=0)
