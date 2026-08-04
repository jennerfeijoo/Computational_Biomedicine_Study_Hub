"""Integration tests for the BMB830 Socratic oral-exam workspace."""

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path

from PySide6.QtCore import QSettings
from PySide6.QtWidgets import QLabel, QPlainTextEdit

from computational_biomedicine_study_hub.i18n import AppLocale
from computational_biomedicine_study_hub.integrations import (
    ChatMessage,
    ChatResponse,
    ChatRole,
)
from computational_biomedicine_study_hub.integrations.bmb830_oral import (
    BMB830OralEvaluationResult,
)
from computational_biomedicine_study_hub.learning.bmb830_oral_exam import (
    BMB830OralEvaluation,
    BMB830OralPrompt,
    OralCriterion,
    OralCriterionScore,
)
from computational_biomedicine_study_hub.storage import (
    BMB830OralExamStore,
    MentorJournalStore,
    SQLiteProgressStore,
)
from computational_biomedicine_study_hub.ui.pages.bmb830_oral_exam_page import (
    BMB830OralExamPage,
    OralFailureCallback,
    OralSuccessCallback,
    OralTask,
)


@dataclass
class FakeEvaluator:
    calls: list[tuple[BMB830OralPrompt, str, str, AppLocale, str]] = field(
        default_factory=list
    )

    def evaluate(
        self,
        *,
        prompt: BMB830OralPrompt,
        transcript: str,
        authoritative_context: str,
        locale: AppLocale,
        previous_follow_up: str = "",
    ) -> BMB830OralEvaluationResult:
        self.calls.append(
            (prompt, transcript, authoritative_context, locale, previous_follow_up)
        )
        evaluation = BMB830OralEvaluation(
            feedback="The explanation is coherent but needs a more explicit assumption.",
            strengths=("Linked the method to the biological question",),
            gaps=("Did not justify independence",),
            misconceptions=(),
            scores=tuple(
                OralCriterionScore(
                    criterion,
                    3,
                    f"Transcript evidence for {criterion.value}",
                )
                for criterion in OralCriterion
            ),
            follow_up_question="Which assumption would you check first, and why?",
            recommended_next_action="Revise the answer around assumptions",
            confidence=0.83,
        )
        return BMB830OralEvaluationResult(
            evaluation=evaluation,
            response=ChatResponse(
                model="test-model",
                message=ChatMessage(ChatRole.ASSISTANT, "structured result"),
                prompt_eval_count=200,
                eval_count=90,
            ),
        )


@dataclass
class DeferredExecutor:
    submissions: list[tuple[int, OralTask, OralSuccessCallback, OralFailureCallback]] = field(
        default_factory=list
    )
    cancelled: list[int] = field(default_factory=list)

    def submit(
        self,
        request_id: int,
        task: OralTask,
        on_success: OralSuccessCallback,
        on_failure: OralFailureCallback,
    ) -> None:
        self.submissions.append((request_id, task, on_success, on_failure))

    def cancel(self, request_id: int) -> None:
        self.cancelled.append(request_id)

    def complete_next(self) -> None:
        request_id, task, on_success, _ = self.submissions.pop(0)
        on_success(request_id, task())


def _settings(tmp_path: Path) -> QSettings:
    return QSettings(str(tmp_path / "bmb830-oral.ini"), QSettings.Format.IniFormat)


def test_oral_page_evaluates_persists_and_feeds_longitudinal_mentor(
    qtbot,
    tmp_path: Path,
) -> None:  # type: ignore[no-untyped-def]
    progress = SQLiteProgressStore(":memory:")
    try:
        evaluator = FakeEvaluator()
        executor = DeferredExecutor()
        oral_store = BMB830OralExamStore.for_progress_store(progress)
        mentor_store = MentorJournalStore.for_progress_store(progress)
        page = BMB830OralExamPage(
            progress,
            AppLocale.ENGLISH,
            settings=_settings(tmp_path),
            oral_store=oral_store,
            mentor_store=mentor_store,
            evaluator=evaluator,
            executor=executor,
        )
        qtbot.addWidget(page)
        editor = page.findChild(QPlainTextEdit, "bmb830OralTranscript")
        assert editor is not None
        editor.setPlainText(
            "I would define the estimand, inspect the data-generating process, and then "
            "choose a model whose assumptions match the biological design."
        )

        page.evaluate_response()
        executor.complete_next()

        assert len(page.snapshot.attempts) == 1
        assert oral_store.load() == page.snapshot
        assert evaluator.calls[0][1].startswith("I would define the estimand")
        assert "<authoritative_tutor_support>" in evaluator.calls[0][2]
        feedback = page.findChild(QLabel, "bmb830OralFeedback")
        follow_up = page.findChild(QLabel, "bmb830OralFollowUp")
        assert feedback is not None and not feedback.isHidden()
        assert follow_up is not None
        assert "Which assumption" in follow_up.text()
        score = page.findChild(QLabel, "bmb830OralScore_accuracy")
        assert score is not None
        assert score.text().startswith("3/4")
        journal = mentor_store.load_or_empty()
        assert journal.turns[-1].context.endswith("oral exam practice")
        assert journal.turns[-1].observation.gaps == ("Did not justify independence",)
    finally:
        progress.close()


def test_oral_page_uses_previous_follow_up_on_repeated_attempt(
    qtbot,
    tmp_path: Path,
) -> None:  # type: ignore[no-untyped-def]
    progress = SQLiteProgressStore(":memory:")
    try:
        evaluator = FakeEvaluator()
        executor = DeferredExecutor()
        page = BMB830OralExamPage(
            progress,
            AppLocale.ENGLISH,
            settings=_settings(tmp_path),
            evaluator=evaluator,
            executor=executor,
        )
        qtbot.addWidget(page)
        page.transcript_editor.setPlainText("First answer")
        page.evaluate_response()
        executor.complete_next()
        page.transcript_editor.setPlainText("Revised answer")
        page.evaluate_response()
        executor.complete_next()

        assert evaluator.calls[0][4] == ""
        assert evaluator.calls[1][4] == "Which assumption would you check first, and why?"
        assert len(page.snapshot.attempts) == 2
    finally:
        progress.close()


def test_oral_page_balances_prompt_coverage_and_preserves_drafts(
    qtbot,
    tmp_path: Path,
) -> None:  # type: ignore[no-untyped-def]
    progress = SQLiteProgressStore(":memory:")
    try:
        settings = _settings(tmp_path)
        page = BMB830OralExamPage(
            progress,
            AppLocale.ENGLISH,
            settings=settings,
            evaluator=FakeEvaluator(),
            executor=DeferredExecutor(),
        )
        qtbot.addWidget(page)
        first_prompt = page.current_prompt.prompt_id
        page.transcript_editor.setPlainText("Persistent draft")
        page.persist()
        page._select_recommended_prompt()  # noqa: SLF001 - integration-level navigation
        assert page.current_prompt.prompt_id == first_prompt

        restored = BMB830OralExamPage(
            progress,
            AppLocale.ENGLISH,
            settings=settings,
            evaluator=FakeEvaluator(),
            executor=DeferredExecutor(),
        )
        qtbot.addWidget(restored)
        restored.select_prompt(first_prompt)
        assert restored.transcript_editor.toPlainText() == "Persistent draft"
    finally:
        progress.close()


def test_oral_page_rejects_empty_transcript_without_submitting(
    qtbot,
    tmp_path: Path,
) -> None:  # type: ignore[no-untyped-def]
    executor = DeferredExecutor()
    page = BMB830OralExamPage(
        None,
        AppLocale.ENGLISH,
        settings=_settings(tmp_path),
        evaluator=FakeEvaluator(),
        executor=executor,
    )
    qtbot.addWidget(page)

    page.evaluate_response()

    assert executor.submissions == []
