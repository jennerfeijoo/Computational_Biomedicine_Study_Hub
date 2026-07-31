from __future__ import annotations

from collections.abc import Callable
from dataclasses import dataclass, field

from PySide6.QtWidgets import QApplication, QLabel, QPushButton

from computational_biomedicine_study_hub.content.dm857 import BUNDLES
from computational_biomedicine_study_hub.content.python_challenges import (
    PythonChallenge,
    python_challenge_for,
)
from computational_biomedicine_study_hub.i18n import AppLocale
from computational_biomedicine_study_hub.integrations import OllamaConnectionError
from computational_biomedicine_study_hub.learning.progress import ConfidenceLevel
from computational_biomedicine_study_hub.learning.progress_service import LearningProgressService
from computational_biomedicine_study_hub.learning.python_challenge import (
    ChallengeCaseStatus,
    PythonChallengeCaseResult,
    PythonChallengeResult,
)
from computational_biomedicine_study_hub.storage import SQLiteProgressStore
from computational_biomedicine_study_hub.tutoring import (
    ChallengeDiagnostic,
    ChallengeTutorPromptBuilder,
    ChallengeTutorResponse,
    TutorAssistanceLevel,
    TutorSessionTurn,
)
from computational_biomedicine_study_hub.ui.widgets import (
    ChallengeTutorPanel,
    GuidedPracticeCard,
    PythonChallengeWidget,
)


def _module(module_id: str = "dm857.m07"):
    return next(bundle.module for bundle in BUNDLES if bundle.module.module_id == module_id)


def _challenge(locale: AppLocale = AppLocale.ENGLISH) -> PythonChallenge:
    challenge = python_challenge_for(
        "m07.p04",
        "def unique_count(values):\n    pass",
        locale,
    )
    assert challenge is not None
    return challenge


def _result(*, all_passed: bool = False) -> PythonChallengeResult:
    return PythonChallengeResult(
        exercise_id="m07.p04",
        visible_results=(
            PythonChallengeCaseResult(
                case_id="duplicates",
                description="Counts repeated integers correctly.",
                status=(ChallengeCaseStatus.PASSED if all_passed else ChallengeCaseStatus.FAILED),
            ),
            PythonChallengeCaseResult(
                case_id="empty",
                description="An empty collection contains zero unique elements.",
                status=ChallengeCaseStatus.PASSED,
            ),
        ),
        hidden_passed=2 if all_passed else 1,
        hidden_total=2,
        duration_ms=21,
    )


def _diagnostic(source: str = "def unique_count(values):\n    return len(values)"):
    return ChallengeDiagnostic.from_attempt(
        challenge=_challenge(),
        result=_result(),
        confidence=ConfidenceLevel.HIGH,
        submitted_source=source,
        prompt="Write unique_count(values).",
        reference_solution="def unique_count(values):\n    return len(set(values))",
        explanation="A set removes duplicates before len counts the remaining values.",
    )


@dataclass
class _FakeTutor:
    response: ChallengeTutorResponse = field(
        default_factory=lambda: ChallengeTutorResponse(
            content="Check which collection you count before calling len.",
            model="qwen3.5:9b-q8_0",
            source_ids=(
                "dm857.m07.overview",
                "dm857.m07.concept.dictionaries-and-sets",
            ),
        )
    )
    calls: list[
        tuple[
            ChallengeDiagnostic,
            str,
            TutorAssistanceLevel,
            tuple[TutorSessionTurn, ...],
        ]
    ] = field(default_factory=list)

    def ask(
        self,
        diagnostic: ChallengeDiagnostic,
        question: str,
        *,
        assistance_level: TutorAssistanceLevel = TutorAssistanceLevel.SOCRATIC,
        history: tuple[TutorSessionTurn, ...] = (),
    ) -> ChallengeTutorResponse:
        self.calls.append((diagnostic, question, assistance_level, history))
        return self.response


TutorTask = Callable[[], ChallengeTutorResponse]
SuccessCallback = Callable[[int, ChallengeTutorResponse], None]
FailureCallback = Callable[[int, Exception], None]


class _DeferredExecutor:
    def __init__(self) -> None:
        self.pending: dict[
            int,
            tuple[TutorTask, SuccessCallback, FailureCallback],
        ] = {}
        self.cancelled: list[int] = []

    def submit(
        self,
        request_id: int,
        task: TutorTask,
        on_success: SuccessCallback,
        on_failure: FailureCallback,
    ) -> None:
        self.pending[request_id] = (task, on_success, on_failure)

    def cancel(self, request_id: int) -> None:
        self.cancelled.append(request_id)

    def succeed(self, request_id: int) -> None:
        task, on_success, _ = self.pending[request_id]
        on_success(request_id, task())

    def fail(self, request_id: int, error: Exception) -> None:
        _, _, on_failure = self.pending[request_id]
        on_failure(request_id, error)


class _FakeEvaluator:
    def __init__(self, result: PythonChallengeResult) -> None:
        self.result = result

    def evaluate(self, source: str, challenge: PythonChallenge) -> PythonChallengeResult:
        del source, challenge
        return self.result


def test_panel_requires_a_verified_diagnostic_before_enabling_tutoring(
    qapp: QApplication,
) -> None:
    panel = ChallengeTutorPanel(_FakeTutor(), locale=AppLocale.ENGLISH)
    ask_button = panel.findChild(QPushButton, "challengeTutorPrimaryButton")
    hint_button = panel.findChild(QPushButton, "challengeTutorSecondaryButton")

    assert ask_button is not None
    assert hint_button is not None
    assert not ask_button.isEnabled()
    assert not hint_button.isEnabled()
    assert panel.diagnostic is None
    assert panel.status_text == "Run the tests to generate a verifiable diagnostic."

    panel.set_diagnostic(_diagnostic())
    panel.set_question("Why does the duplicate case fail?")

    assert ask_button.isEnabled()
    assert hint_button.isEnabled()
    assert panel.status_text == "The diagnostic is ready for a question."


def test_panel_runs_asynchronously_and_retains_sources_for_each_turn(
    qapp: QApplication,
) -> None:
    tutor = _FakeTutor()
    executor = _DeferredExecutor()
    panel = ChallengeTutorPanel(tutor, locale=AppLocale.ENGLISH, executor=executor)
    diagnostic = _diagnostic()
    panel.set_diagnostic(diagnostic)
    panel.set_question("Give me a hint.")

    panel.ask_question()

    assert panel.is_busy
    assert panel.status_text == "Ollama is generating a response…"
    assert tutor.calls == []
    executor.succeed(1)

    assert not panel.is_busy
    assert tutor.calls[0][:3] == (
        diagnostic,
        "Give me a hint.",
        TutorAssistanceLevel.SOCRATIC,
    )
    assert tutor.calls[0][3] == ()
    assert panel.response_text.startswith("Check which collection")
    assert "dm857.m07.overview" in panel.sources_text
    assert "dm857.m07.overview" in panel.history_text
    assert panel.model_text == "Local model: qwen3.5:9b-q8_0"
    assert panel.assistance_count == 1


def test_follow_up_receives_bounded_prior_turns_and_selected_level(
    qapp: QApplication,
) -> None:
    tutor = _FakeTutor()
    executor = _DeferredExecutor()
    panel = ChallengeTutorPanel(tutor, locale=AppLocale.ENGLISH, executor=executor)
    panel.set_diagnostic(_diagnostic())
    panel.set_question("What should I inspect first?")
    panel.ask_question()
    executor.succeed(1)

    panel.set_assistance_level(TutorAssistanceLevel.CONCEPTUAL)
    panel.set_question("Why does a set change the count?")
    panel.ask_question()
    executor.succeed(2)

    assert len(tutor.calls) == 2
    assert tutor.calls[1][2] is TutorAssistanceLevel.CONCEPTUAL
    assert len(tutor.calls[1][3]) == 1
    assert tutor.calls[1][3][0].question == "What should I inspect first?"
    assert panel.assistance_count == 2
    assert "Turn 2" in panel.history_text


def test_negative_feedback_escalates_help_and_preserves_the_rating(
    qapp: QApplication,
) -> None:
    executor = _DeferredExecutor()
    panel = ChallengeTutorPanel(_FakeTutor(), locale=AppLocale.ENGLISH, executor=executor)
    panel.set_diagnostic(_diagnostic())
    panel.request_hint()
    executor.succeed(1)

    panel.mark_not_helpful()

    assert panel.session_turns[-1].helpful is False
    assert panel.selected_level is TutorAssistanceLevel.CONCEPTUAL
    assert "next suggested level" in panel.status_text
    assert "Insufficient" in panel.history_text


def test_full_explanation_marks_solution_support_for_the_next_attempt(
    qapp: QApplication,
) -> None:
    executor = _DeferredExecutor()
    panel = ChallengeTutorPanel(_FakeTutor(), locale=AppLocale.ENGLISH, executor=executor)
    panel.set_diagnostic(_diagnostic())
    panel.set_assistance_level(TutorAssistanceLevel.EXPLANATION)
    panel.request_hint()
    executor.succeed(1)

    assert panel.assistance_count == 1
    assert panel.solution_revealed
    assert panel.session_turns[-1].assistance_level is TutorAssistanceLevel.EXPLANATION


def test_cancelled_requests_cannot_overwrite_the_interface(qapp: QApplication) -> None:
    tutor = _FakeTutor()
    executor = _DeferredExecutor()
    panel = ChallengeTutorPanel(tutor, locale=AppLocale.ENGLISH, executor=executor)
    panel.set_diagnostic(_diagnostic())
    panel.set_question("Explain the failure.")
    panel.ask_question()

    panel.cancel_request()
    executor.succeed(1)

    assert executor.cancelled == [1]
    assert not panel.is_busy
    assert panel.last_response is None
    assert panel.response_text == ""
    assert "cancelled" in panel.status_text.casefold()


def test_panel_distinguishes_missing_model_from_offline_ollama(qapp: QApplication) -> None:
    executor = _DeferredExecutor()
    panel = ChallengeTutorPanel(_FakeTutor(), locale=AppLocale.ENGLISH, executor=executor)
    panel.set_diagnostic(_diagnostic())
    panel.set_question("Help me.")
    panel.ask_question()

    executor.fail(
        1,
        OllamaConnectionError("Ollama returned HTTP 404: model not found, pull it first"),
    )

    assert "qwen3.5:9b-q8_0" in panel.status_text
    assert "not installed" in panel.status_text

    panel.set_question("Try again.")
    panel.ask_question()
    executor.fail(2, OllamaConnectionError("connection refused"))

    assert "Could not connect to Ollama" in panel.status_text


def test_new_test_run_resets_session_and_records_prior_help_in_mastery(
    qapp: QApplication,
) -> None:
    tutor = _FakeTutor()
    executor = _DeferredExecutor()
    evaluator = _FakeEvaluator(_result())
    attempt_ids = iter(("attempt-1", "attempt-2", "attempt-3", "attempt-4"))

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
            prompt="Write unique_count(values).",
            reference_solution="def unique_count(values):\n    return len(set(values))",
            explanation="A set removes duplicates before len counts the remaining values.",
            progress_recorder=service,
            tutor_runner=tutor,
            tutor_executor=executor,
        )
        widget.set_source("def unique_count(values):\n    return len(values)")
        widget.choose_confidence(ConfidenceLevel.HIGH)
        widget.run_tests()
        panel = widget.tutor_panel
        assert panel is not None

        panel.set_assistance_level(TutorAssistanceLevel.CONCEPTUAL)
        panel.request_hint()
        executor.succeed(1)
        assert panel.assistance_count == 1

        evaluator.result = _result(all_passed=True)
        widget.set_source("def unique_count(values):\n    return len(set(values))")
        widget.choose_confidence(ConfidenceLevel.HIGH)
        widget.run_tests()

        attempts = store.list_attempts(course_code="DM857", module_id="dm857.m07")
        assert all(attempt.hints_used == 0 for attempt in attempts[:2])
        assert all(attempt.hints_used == 1 for attempt in attempts[2:])
        assert all(not attempt.solution_revealed for attempt in attempts)
        assert panel.assistance_count == 0
        assert panel.history_text == ""
        mastery = store.get_mastery(
            "m07.o6",
            course_code="DM857",
            module_id="dm857.m07",
        )
        assert mastery is not None
        assert (mastery.next_review_at - mastery.last_attempt_at).days == 2


def test_guided_practice_supplies_module_context_to_authored_challenges(
    qapp: QApplication,
) -> None:
    module = _module()
    exercise = next(item for item in module.practice_exercises if item.exercise_id == "m07.p04")

    card = GuidedPracticeCard(
        1,
        exercise,
        locale=AppLocale.SPANISH_SPAIN,
        learning_module=module,
    )

    assert card.challenge_widget is not None
    assert card.challenge_widget.tutor_panel is not None


def test_challenge_prompt_requests_active_language_and_assistance_level() -> None:
    english = ChallengeTutorPromptBuilder(
        _module(),
        locale=AppLocale.ENGLISH,
    ).build(
        _diagnostic(),
        "Why does my function fail?",
        assistance_level=TutorAssistanceLevel.STRUCTURAL,
    )
    danish = ChallengeTutorPromptBuilder(
        _module(),
        locale=AppLocale.DANISH_DENMARK,
    ).build(_diagnostic(), "Hvorfor fejler min funktion?")

    assert "Respond in English" in english.messages[0].content
    assert "Requested level: structural hint" in english.messages[0].content
    assert "Learner question:" in english.messages[1].content
    assert "Svar på dansk" in danish.messages[0].content
    assert "Den studerendes spørgsmål:" in danish.messages[1].content


def test_new_diagnostic_clears_history_and_returns_to_socratic_level(
    qapp: QApplication,
) -> None:
    executor = _DeferredExecutor()
    panel = ChallengeTutorPanel(_FakeTutor(), locale=AppLocale.ENGLISH, executor=executor)
    panel.set_diagnostic(_diagnostic())
    panel.set_assistance_level(TutorAssistanceLevel.STRUCTURAL)
    panel.request_hint()
    executor.succeed(1)

    panel.set_diagnostic(_diagnostic("def unique_count(values):\n    return len(set(values))"))

    assert panel.session_turns == ()
    assert panel.history_text == ""
    assert panel.selected_level is TutorAssistanceLevel.SOCRATIC


def test_danish_panel_copy_is_complete(qapp: QApplication) -> None:
    panel = ChallengeTutorPanel(_FakeTutor(), locale=AppLocale.DANISH_DENMARK)
    title = panel.findChild(QLabel, "challengeTutorTitle")
    hint = panel.findChild(QPushButton, "challengeTutorSecondaryButton")

    assert title is not None
    assert hint is not None
    assert title.text() == "Kontekstuel tutor"
    assert hint.text() == "Anmod om dette niveau"
