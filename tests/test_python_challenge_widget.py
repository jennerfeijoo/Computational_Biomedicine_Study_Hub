from __future__ import annotations

from collections.abc import Iterator

from PySide6.QtWidgets import QApplication, QPushButton

from computational_biomedicine_study_hub.content.python_challenges import (
    PythonChallenge,
    python_challenge_for,
)
from computational_biomedicine_study_hub.i18n import AppLocale
from computational_biomedicine_study_hub.learning.progress import ConfidenceLevel
from computational_biomedicine_study_hub.learning.progress_service import LearningProgressService
from computational_biomedicine_study_hub.learning.python_challenge import (
    ChallengeCaseStatus,
    PythonChallengeCaseResult,
    PythonChallengeResult,
)
from computational_biomedicine_study_hub.storage import SQLiteProgressStore
from computational_biomedicine_study_hub.ui.widgets import PythonChallengeWidget


class _FakeEvaluator:
    def __init__(self, result: PythonChallengeResult) -> None:
        self.result = result
        self.calls: list[tuple[str, PythonChallenge]] = []

    def evaluate(self, source: str, challenge: PythonChallenge) -> PythonChallengeResult:
        self.calls.append((source, challenge))
        return self.result


class _Clock:
    def __init__(self, values: Iterator[float]) -> None:
        self._values = values

    def __call__(self) -> float:
        return next(self._values)


def _challenge(locale: AppLocale = AppLocale.ENGLISH) -> PythonChallenge:
    challenge = python_challenge_for(
        "m07.p04",
        "def unique_count(values):\n    pass",
        locale,
    )
    assert challenge is not None
    return challenge


def _result(*, all_passed: bool) -> PythonChallengeResult:
    status = ChallengeCaseStatus.PASSED if all_passed else ChallengeCaseStatus.FAILED
    return PythonChallengeResult(
        exercise_id="m07.p04",
        visible_results=(
            PythonChallengeCaseResult(
                case_id="duplicates",
                description="Counts repeated integers correctly.",
                status=status,
            ),
            PythonChallengeCaseResult(
                case_id="empty",
                description="An empty collection contains zero unique elements.",
                status=ChallengeCaseStatus.PASSED,
            ),
        ),
        hidden_passed=2 if all_passed else 1,
        hidden_total=2,
        duration_ms=17,
    )


def test_widget_requires_confidence_before_revealing_test_feedback(
    qapp: QApplication,
) -> None:
    evaluator = _FakeEvaluator(_result(all_passed=False))
    widget = PythonChallengeWidget(
        "def unique_count(values):\n    pass",
        _challenge(),
        locale=AppLocale.ENGLISH,
        evaluator=evaluator,
    )

    widget.run_tests()

    assert evaluator.calls == []
    assert widget.last_result is None
    assert "confidence" in widget.status_text.casefold()


def test_widget_evaluates_edited_source_and_hides_test_inputs(qapp: QApplication) -> None:
    evaluator = _FakeEvaluator(_result(all_passed=False))
    widget = PythonChallengeWidget(
        "def unique_count(values):\n    pass",
        _challenge(),
        locale=AppLocale.ENGLISH,
        evaluator=evaluator,
    )
    source = "def unique_count(values):\n    return len(set(values))"
    widget.set_source(source)
    widget.choose_confidence(ConfidenceLevel.MEDIUM)

    widget.run_tests()

    assert evaluator.calls[0][0] == source
    assert widget.last_result is evaluator.result
    assert "does not yet satisfy" in widget.status_text
    assert "17 ms" in widget.status_text
    assert widget.hidden_summary_text == "Hidden tests passed: 1/2"
    assert all("['A'" not in text for text in widget.visible_result_texts)
    assert widget.selected_confidence is None


def test_challenge_attempts_update_mastery_and_error_notebook(qapp: QApplication) -> None:
    evaluator = _FakeEvaluator(_result(all_passed=False))
    attempt_ids = iter(("attempt-1", "attempt-2", "attempt-3", "attempt-4"))
    clock = _Clock(iter((10.0, 13.5, 13.5, 16.0, 16.0)))
    source = "def unique_count(values):\n    return len(set(values))"
    reference = "def unique_count(values):\n    return len(set(values))"

    with SQLiteProgressStore(":memory:") as store:
        service = LearningProgressService(
            store,
            attempt_id_factory=lambda: next(attempt_ids),
            error_id_factory=lambda: "error-1",
        )
        widget = PythonChallengeWidget(
            "def unique_count(values):\n    pass",
            _challenge(),
            locale=AppLocale.ENGLISH,
            evaluator=evaluator,
            activity_type="code_completion",
            prompt="Write unique_count(values).",
            reference_solution=reference,
            explanation="A set removes duplicates before len counts the remaining values.",
            progress_recorder=service,
            clock=clock,
        )
        widget.set_source(source)
        widget.choose_confidence(ConfidenceLevel.HIGH)

        widget.run_tests()

        attempts = store.list_attempts(course_code="DM857", module_id="dm857.m07")
        errors = store.list_errors()
        assert len(attempts) == 2
        assert {attempt.objective_id for attempt in attempts} == {"m07.o6", "m07.o8"}
        assert all(attempt.answer == source for attempt in attempts)
        assert all(not attempt.is_correct for attempt in attempts)
        assert all(attempt.confidence is ConfidenceLevel.HIGH for attempt in attempts)
        assert all(attempt.response_time_ms == 3500 for attempt in attempts)
        assert len(errors) == 1
        assert errors[0].selected_answer == source
        assert errors[0].correct_answer == reference
        assert not errors[0].is_resolved

        evaluator.result = _result(all_passed=True)
        widget.choose_confidence(ConfidenceLevel.MEDIUM)
        widget.run_tests()

        attempts = store.list_attempts(course_code="DM857", module_id="dm857.m07")
        errors = store.list_errors()
        assert len(attempts) == 4
        assert all(attempt.is_correct for attempt in attempts[2:])
        assert all(attempt.response_time_ms == 2500 for attempt in attempts[2:])
        assert errors[0].is_resolved
        assert (
            store.get_mastery(
                "m07.o6",
                course_code="DM857",
                module_id="dm857.m07",
            )
            is not None
        )


def test_widget_reset_restores_starter_code_and_clears_feedback(qapp: QApplication) -> None:
    evaluator = _FakeEvaluator(_result(all_passed=True))
    starter = "def unique_count(values):\n    pass"
    widget = PythonChallengeWidget(starter, _challenge(), evaluator=evaluator)
    widget.set_source("def unique_count(values):\n    return 99")
    widget.choose_confidence(ConfidenceLevel.LOW)
    widget.run_tests()

    widget.reset_code()

    assert widget.source == starter
    assert widget.selected_confidence is None
    assert widget.last_result is None
    assert widget.status_text == ""
    assert widget.hidden_summary_text == ""
    assert widget.visible_result_texts == ()


def test_widget_buttons_are_localized_in_danish(qapp: QApplication) -> None:
    widget = PythonChallengeWidget(
        "def unique_count(values):\n    pass",
        _challenge(AppLocale.DANISH_DENMARK),
        locale=AppLocale.DANISH_DENMARK,
        evaluator=_FakeEvaluator(_result(all_passed=True)),
    )

    run_button = widget.findChild(QPushButton, "pythonChallengeRunButton")
    reset_button = widget.findChild(QPushButton, "pythonChallengeResetButton")

    assert run_button is not None
    assert reset_button is not None
    assert run_button.text() == "Kør test"
    assert reset_button.text() == "Nulstil kode"
