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
from computational_biomedicine_study_hub.learning.python_challenge import (
    ChallengeCaseStatus,
    PythonChallengeCaseResult,
    PythonChallengeResult,
)
from computational_biomedicine_study_hub.tutoring import (
    ChallengeDiagnostic,
    ChallengeTutorPromptBuilder,
    ChallengeTutorResponse,
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
    calls: list[tuple[ChallengeDiagnostic, str]] = field(default_factory=list)

    def ask(self, diagnostic: ChallengeDiagnostic, question: str) -> ChallengeTutorResponse:
        self.calls.append((diagnostic, question))
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


def test_panel_runs_outside_the_ui_flow_and_renders_sources(qapp: QApplication) -> None:
    tutor = _FakeTutor()
    executor = _DeferredExecutor()
    panel = ChallengeTutorPanel(
        tutor,
        locale=AppLocale.ENGLISH,
        executor=executor,
    )
    diagnostic = _diagnostic()
    panel.set_diagnostic(diagnostic)
    panel.set_question("Give me a hint.")

    panel.ask_question()

    assert panel.is_busy
    assert panel.status_text == "Ollama is generating a response…"
    assert tutor.calls == []
    assert tuple(executor.pending) == (1,)

    executor.succeed(1)

    assert not panel.is_busy
    assert tutor.calls == [(diagnostic, "Give me a hint.")]
    assert panel.response_text.startswith("Check which collection")
    assert "dm857.m07.overview" in panel.sources_text
    assert panel.model_text == "Local model: qwen3.5:9b-q8_0"


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
    panel = ChallengeTutorPanel(
        _FakeTutor(),
        locale=AppLocale.ENGLISH,
        executor=executor,
    )
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


def test_new_test_run_invalidates_old_tutor_output_but_source_edits_do_not(
    qapp: QApplication,
) -> None:
    tutor = _FakeTutor()
    executor = _DeferredExecutor()
    evaluator = _FakeEvaluator(_result())
    widget = PythonChallengeWidget(
        "def unique_count(values):\n    pass",
        _challenge(),
        locale=AppLocale.ENGLISH,
        evaluator=evaluator,
        prompt="Write unique_count(values).",
        reference_solution="def unique_count(values):\n    return len(set(values))",
        explanation="A set removes duplicates before len counts the remaining values.",
        tutor_runner=tutor,
        tutor_executor=executor,
    )
    widget.set_source("def unique_count(values):\n    return len(values)")
    widget.choose_confidence(ConfidenceLevel.HIGH)
    widget.run_tests()
    panel = widget.tutor_panel
    assert panel is not None
    first_diagnostic = panel.diagnostic

    widget.set_source("def unique_count(values):\n    return len(set(values))")

    assert panel.diagnostic is first_diagnostic

    panel.set_question("Why did the first attempt fail?")
    panel.ask_question()
    executor.succeed(1)
    assert panel.response_text

    evaluator.result = _result(all_passed=True)
    widget.choose_confidence(ConfidenceLevel.MEDIUM)
    widget.run_tests()

    assert panel.response_text == ""
    assert panel.diagnostic is widget.last_diagnostic
    assert panel.diagnostic is not first_diagnostic
    assert panel.diagnostic is not None
    assert panel.diagnostic.submitted_source.endswith("len(set(values))")


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


def test_challenge_prompt_requests_the_active_interface_language() -> None:
    english = ChallengeTutorPromptBuilder(
        _module(),
        locale=AppLocale.ENGLISH,
    ).build(_diagnostic(), "Why does my function fail?")
    danish = ChallengeTutorPromptBuilder(
        _module(),
        locale=AppLocale.DANISH_DENMARK,
    ).build(_diagnostic(), "Hvorfor fejler min funktion?")

    assert "Respond in English" in english.messages[0].content
    assert "Learner question:" in english.messages[1].content
    assert "Svar på dansk" in danish.messages[0].content
    assert "Den studerendes spørgsmål:" in danish.messages[1].content


def test_danish_panel_copy_is_complete(qapp: QApplication) -> None:
    panel = ChallengeTutorPanel(_FakeTutor(), locale=AppLocale.DANISH_DENMARK)
    title = panel.findChild(QLabel, "challengeTutorTitle")
    hint = panel.findChild(QPushButton, "challengeTutorSecondaryButton")

    assert title is not None
    assert hint is not None
    assert title.text() == "Kontekstuel tutor"
    assert hint.text() == "Bed om et hint"
