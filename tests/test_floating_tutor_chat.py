from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path

from PySide6.QtCore import QSettings, Qt
from PySide6.QtWidgets import QApplication, QComboBox, QLabel, QPlainTextEdit, QTextBrowser

from computational_biomedicine_study_hub.i18n import AppLocale
from computational_biomedicine_study_hub.integrations import (
    ChatMessage,
    ChatResponse,
    ChatRole,
)
from computational_biomedicine_study_hub.learning.mentor import (
    MentorMode,
    MentorObservation,
    MentorTurnResult,
)
from computational_biomedicine_study_hub.storage import (
    MentorJournalStore,
    SQLiteProgressStore,
)
from computational_biomedicine_study_hub.ui.widgets.floating_tutor_chat import (
    FloatingTutorChat,
    TutorFailureCallback,
    TutorSuccessCallback,
    TutorTask,
)


@dataclass
class _FakeRunner:
    response_text: str = "Contextual answer"
    observation: MentorObservation = MentorObservation(
        demonstrated=("Explained one relevant relationship",),
        gaps=("Needs a more explicit justification",),
        recommended_next_action="Answer the mentor's next question",
        next_question="What evidence supports the claim?",
        confidence=0.75,
    )
    calls: list[
        tuple[
            str,
            tuple[ChatMessage, ...],
            str,
            AppLocale,
            MentorMode,
            str,
        ]
    ] = field(default_factory=list)

    def ask(
        self,
        context: str,
        history: tuple[ChatMessage, ...],
        question: str,
        *,
        locale: AppLocale,
        mode: MentorMode,
        memory: str,
    ) -> MentorTurnResult:
        self.calls.append((context, history, question, locale, mode, memory))
        return MentorTurnResult(
            response=ChatResponse(
                model="test-model",
                message=ChatMessage(ChatRole.ASSISTANT, self.response_text),
            ),
            observation=self.observation,
        )


@dataclass
class _DeferredExecutor:
    submissions: list[tuple[int, TutorTask, TutorSuccessCallback, TutorFailureCallback]] = field(
        default_factory=list
    )
    cancelled: list[int] = field(default_factory=list)

    def submit(
        self,
        request_id: int,
        task: TutorTask,
        on_success: TutorSuccessCallback,
        on_failure: TutorFailureCallback,
    ) -> None:
        self.submissions.append((request_id, task, on_success, on_failure))

    def cancel(self, request_id: int) -> None:
        self.cancelled.append(request_id)

    def complete_next(self) -> None:
        request_id, task, on_success, _ = self.submissions.pop(0)
        on_success(request_id, task())


def _settings(tmp_path: Path) -> QSettings:
    return QSettings(str(tmp_path / "tutor.ini"), QSettings.Format.IniFormat)


def test_floating_mentor_sends_context_mode_memory_and_keeps_history(
    qapp: QApplication,
    tmp_path: Path,
) -> None:
    runner = _FakeRunner()
    executor = _DeferredExecutor()
    panel = FloatingTutorChat(
        settings=_settings(tmp_path),
        context_provider=lambda: "DM857 | Module 1 | Practice",
        locale=AppLocale.ENGLISH,
        runner=runner,
        executor=executor,
    )
    question = panel.findChild(QPlainTextEdit, "floatingTutorQuestion")
    assert question is not None
    question.setPlainText("Why does round use tie-to-even?")

    panel.send_question()
    executor.complete_next()

    assert len(runner.calls) == 1
    context, history, prompt, locale, mode, memory = runner.calls[0]
    assert context == "DM857 | Module 1 | Practice"
    assert history == ()
    assert prompt == "Why does round use tie-to-even?"
    assert locale is AppLocale.ENGLISH
    assert mode is MentorMode.SOCRATIC
    assert memory == "No previous mentor observations are available."
    assert tuple(message.role for message in panel.conversation) == (
        ChatRole.USER,
        ChatRole.ASSISTANT,
    )
    assert "Contextual answer" in panel.transcript_text


def test_floating_mentor_reset_and_minimize_are_local_only(
    qapp: QApplication,
    tmp_path: Path,
) -> None:
    runner = _FakeRunner()
    executor = _DeferredExecutor()
    panel = FloatingTutorChat(
        settings=_settings(tmp_path),
        context_provider=lambda: "Current topic",
        runner=runner,
        executor=executor,
    )
    question = panel.findChild(QPlainTextEdit, "floatingTutorQuestion")
    assert question is not None
    question.setPlainText("Explain this topic")
    panel.send_question()
    executor.complete_next()
    journal_turns = panel.journal.turns

    panel.toggle_minimized()
    assert panel.is_minimized
    panel.toggle_minimized()
    assert not panel.is_minimized

    panel.reset_conversation()
    assert panel.conversation == ()
    assert panel.transcript_text == ""
    assert panel.journal.turns == journal_turns


def test_selection_explanation_opens_chat_and_uses_selected_text(
    qapp: QApplication,
    tmp_path: Path,
) -> None:
    runner = _FakeRunner()
    executor = _DeferredExecutor()
    panel = FloatingTutorChat(
        settings=_settings(tmp_path),
        context_provider=lambda: "DM857 | Concepts",
        locale=AppLocale.SPANISH_SPAIN,
        runner=runner,
        executor=executor,
    )

    panel.explain_selection("  representación   binaria aproximada  ")
    executor.complete_next()

    assert panel.isVisible()
    assert runner.calls
    context, history, question, locale, mode, _ = runner.calls[0]
    assert context == "DM857 | Concepts"
    assert history == ()
    assert "representación binaria aproximada" in question
    assert locale is AppLocale.SPANISH_SPAIN
    assert mode is MentorMode.SOCRATIC


def test_mentor_renders_markdown_and_keeps_the_complete_latest_response(
    qapp: QApplication,
    tmp_path: Path,
) -> None:
    tail_marker = "COMPLETE-RESPONSE-END"
    response = (
        "## Idea principal\n\n"
        "- Primer punto\n"
        "- Segundo punto\n\n"
        "```python\nvalue = 3\nprint(value)\n```\n\n"
        + ("Explicación extensa. " * 1200)
        + tail_marker
    )
    runner = _FakeRunner(response_text=response)
    executor = _DeferredExecutor()
    panel = FloatingTutorChat(
        settings=_settings(tmp_path),
        context_provider=lambda: "DM857 | Concepts",
        locale=AppLocale.SPANISH_SPAIN,
        runner=runner,
        executor=executor,
    )
    question = panel.findChild(QPlainTextEdit, "floatingTutorQuestion")
    transcript = panel.findChild(QTextBrowser, "floatingTutorTranscript")
    assert question is not None
    assert transcript is not None
    question.setPlainText("Explica el concepto")

    panel.send_question()
    executor.complete_next()

    assert tail_marker in panel.transcript_text
    assert len(panel.conversation) == 2
    html = transcript.toHtml().casefold()
    assert "idea principal" in html
    assert "<ul" in html
    assert "<pre" in html
    assert transcript.verticalScrollBarPolicy() is Qt.ScrollBarPolicy.ScrollBarAlwaysOn


def test_mentor_mode_is_selectable_and_persisted(
    qapp: QApplication,
    tmp_path: Path,
) -> None:
    settings = _settings(tmp_path)
    panel = FloatingTutorChat(
        settings=settings,
        context_provider=lambda: "BMB830 | Assessment",
        runner=_FakeRunner(),
        executor=_DeferredExecutor(),
    )
    selector = panel.findChild(QComboBox, "mentorModeSelector")
    assert selector is not None
    assert panel.current_mode is MentorMode.SOCRATIC

    selector.setCurrentIndex(selector.findData(MentorMode.EVALUATE.value))

    assert panel.current_mode is MentorMode.EVALUATE
    assert settings.value("mentor/mode") == MentorMode.EVALUATE.value


def test_mentor_observation_is_visible_but_marked_provisional(
    qapp: QApplication,
    tmp_path: Path,
) -> None:
    runner = _FakeRunner()
    executor = _DeferredExecutor()
    panel = FloatingTutorChat(
        settings=_settings(tmp_path),
        context_provider=lambda: "DM847 | Evaluation",
        locale=AppLocale.ENGLISH,
        runner=runner,
        executor=executor,
    )
    question = panel.findChild(QPlainTextEdit, "floatingTutorQuestion")
    assert question is not None
    question.setPlainText("Evaluate my answer")

    panel.send_question()
    executor.complete_next()

    note = panel.findChild(QLabel, "mentorObservationBody")
    assert note is not None
    assert note.isVisible()
    assert "Observed evidence" in note.text()
    assert "Suggested next action" in note.text()


def test_mentor_journal_restores_conversation_and_memory(
    qapp: QApplication,
    tmp_path: Path,
) -> None:
    progress = SQLiteProgressStore(":memory:")
    try:
        store = MentorJournalStore.for_progress_store(progress)
        runner = _FakeRunner()
        executor = _DeferredExecutor()
        panel = FloatingTutorChat(
            settings=_settings(tmp_path),
            context_provider=lambda: "BMB830 | Correlation",
            runner=runner,
            executor=executor,
            journal_store=store,
        )
        question = panel.findChild(QPlainTextEdit, "floatingTutorQuestion")
        assert question is not None
        question.setPlainText("My first explanation")
        panel.send_question()
        executor.complete_next()

        restored_runner = _FakeRunner()
        restored_executor = _DeferredExecutor()
        restored = FloatingTutorChat(
            settings=_settings(tmp_path),
            context_provider=lambda: "BMB830 | Correlation",
            runner=restored_runner,
            executor=restored_executor,
            journal_store=MentorJournalStore.for_progress_store(progress),
        )
        restored_question = restored.findChild(QPlainTextEdit, "floatingTutorQuestion")
        assert restored_question is not None
        assert len(restored.conversation) == 2
        restored_question.setPlainText("Continue")
        restored.send_question()
        restored_executor.complete_next()

        assert "provisional model-generated mentor observations" in restored_runner.calls[0][5]
        assert "demonstrated=Explained one relevant relationship" in restored_runner.calls[0][5]
    finally:
        progress.close()
