from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path

from PySide6.QtCore import QSettings, Qt
from PySide6.QtWidgets import QApplication, QPlainTextEdit, QTextBrowser

from computational_biomedicine_study_hub.i18n import AppLocale
from computational_biomedicine_study_hub.integrations import (
    ChatMessage,
    ChatResponse,
    ChatRole,
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
    calls: list[tuple[str, tuple[ChatMessage, ...], str, AppLocale]] = field(default_factory=list)

    def ask(
        self,
        context: str,
        history: tuple[ChatMessage, ...],
        question: str,
        *,
        locale: AppLocale,
    ) -> ChatResponse:
        self.calls.append((context, history, question, locale))
        return ChatResponse(
            model="test-model",
            message=ChatMessage(ChatRole.ASSISTANT, self.response_text),
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


def test_floating_tutor_sends_current_context_and_keeps_history(
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

    assert runner.calls == [
        (
            "DM857 | Module 1 | Practice",
            (),
            "Why does round use tie-to-even?",
            AppLocale.ENGLISH,
        )
    ]
    assert tuple(message.role for message in panel.conversation) == (
        ChatRole.USER,
        ChatRole.ASSISTANT,
    )
    assert "Contextual answer" in panel.transcript_text


def test_floating_tutor_reset_and_minimize_are_local_only(
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

    panel.toggle_minimized()
    assert panel.is_minimized
    panel.toggle_minimized()
    assert not panel.is_minimized

    panel.reset_conversation()
    assert panel.conversation == ()
    assert panel.transcript_text == ""


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
    context, history, question, locale = runner.calls[0]
    assert context == "DM857 | Concepts"
    assert history == ()
    assert "representación binaria aproximada" in question
    assert locale is AppLocale.SPANISH_SPAIN


def test_tutor_renders_markdown_and_keeps_the_complete_latest_response(
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
