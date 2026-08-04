"""Integration tests for disposable audio on the persistent mentor."""

from __future__ import annotations

from collections.abc import Callable
from dataclasses import dataclass, field
from pathlib import Path

from PySide6.QtCore import QSettings
from PySide6.QtWidgets import QApplication, QCheckBox, QComboBox, QPlainTextEdit, QPushButton

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
from computational_biomedicine_study_hub.speech import VoicePlaybackState
from computational_biomedicine_study_hub.ui.widgets.floating_tutor_chat import (
    TutorFailureCallback,
    TutorSuccessCallback,
    TutorTask,
)
from computational_biomedicine_study_hub.ui.widgets.voiced_floating_tutor_chat import (
    VoicedFloatingTutorChat,
)


@dataclass
class _FakeRunner:
    response_text: str = "What evidence would distinguish association from causation?"

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
        del context, history, question, locale, mode, memory
        return MentorTurnResult(
            response=ChatResponse(
                model="test-model",
                message=ChatMessage(ChatRole.ASSISTANT, self.response_text),
            ),
            observation=MentorObservation.empty(),
        )


class _ImmediateExecutor:
    def submit(
        self,
        request_id: int,
        task: TutorTask,
        on_success: TutorSuccessCallback,
        on_failure: TutorFailureCallback,
    ) -> None:
        try:
            result = task()
        except Exception as exc:  # pragma: no cover - defensive test boundary
            on_failure(request_id, exc)
        else:
            on_success(request_id, result)

    def cancel(self, request_id: int) -> None:
        del request_id


@dataclass
class _FakeSpeechController:
    available: bool = True
    state: VoicePlaybackState = VoicePlaybackState.IDLE
    played: list[tuple[str, AppLocale, float]] = field(default_factory=list)
    discarded: int = 0
    shutdowns: int = 0
    _state_callback: Callable[[VoicePlaybackState], None] = field(
        default=lambda state: None
    )
    _error_callback: Callable[[str], None] = field(default=lambda detail: None)

    def set_callbacks(
        self,
        *,
        state_changed: Callable[[VoicePlaybackState], None],
        error: Callable[[str], None],
    ) -> None:
        self._state_callback = state_changed
        self._error_callback = error
        state_changed(self.state)

    def play_text(self, text: str, locale: AppLocale, *, rate: float = 0.0) -> None:
        self.played.append((text, locale, rate))
        self.state = VoicePlaybackState.PLAYING
        self._state_callback(self.state)

    def pause(self) -> None:
        self.state = VoicePlaybackState.PAUSED
        self._state_callback(self.state)

    def resume(self) -> None:
        self.state = VoicePlaybackState.PLAYING
        self._state_callback(self.state)

    def stop(self) -> None:
        self.state = VoicePlaybackState.IDLE
        self._state_callback(self.state)

    def discard(self) -> None:
        self.discarded += 1
        self.stop()

    def shutdown(self) -> None:
        self.shutdowns += 1
        self.discard()


def _settings(tmp_path: Path) -> QSettings:
    return QSettings(str(tmp_path / "voice.ini"), QSettings.Format.IniFormat)


def _panel(
    tmp_path: Path,
    speech: _FakeSpeechController,
    *,
    locale: AppLocale = AppLocale.ENGLISH,
) -> VoicedFloatingTutorChat:
    return VoicedFloatingTutorChat(
        settings=_settings(tmp_path),
        context_provider=lambda: "BMB830 | Oral practice",
        locale=locale,
        runner=_FakeRunner(),
        executor=_ImmediateExecutor(),
        speech_controller=speech,
    )


def _complete_one_turn(panel: VoicedFloatingTutorChat) -> None:
    question = panel.findChild(QPlainTextEdit, "floatingTutorQuestion")
    assert question is not None
    question.setPlainText("My current reasoning")
    panel.send_question()


def test_voice_controls_generate_audio_only_for_latest_mentor_reply(
    qapp: QApplication,
    tmp_path: Path,
) -> None:
    del qapp
    speech = _FakeSpeechController()
    panel = _panel(tmp_path, speech, locale=AppLocale.SPANISH_SPAIN)
    _complete_one_turn(panel)

    panel.play_latest_response()

    assert speech.played == [
        (
            "What evidence would distinguish association from causation?",
            AppLocale.SPANISH_SPAIN,
            0.0,
        )
    ]
    pause = panel.findChild(QPushButton, "mentorVoicePauseButton")
    stop = panel.findChild(QPushButton, "mentorVoiceStopButton")
    assert pause is not None and pause.isEnabled()
    assert stop is not None and stop.isEnabled()

    panel.toggle_voice_pause()
    assert speech.state is VoicePlaybackState.PAUSED
    panel.toggle_voice_pause()
    assert speech.state is VoicePlaybackState.PLAYING
    panel.stop_voice()
    assert speech.state is VoicePlaybackState.IDLE


def test_voice_autoplay_and_rate_are_persisted_and_applied(
    qapp: QApplication,
    tmp_path: Path,
) -> None:
    del qapp
    speech = _FakeSpeechController()
    panel = _panel(tmp_path, speech)
    autoplay = panel.findChild(QCheckBox, "mentorVoiceAutoplay")
    rate = panel.findChild(QComboBox, "mentorVoiceRateSelector")
    assert autoplay is not None
    assert rate is not None

    autoplay.setChecked(True)
    rate.setCurrentIndex(rate.findData(0.2))
    _complete_one_turn(panel)

    assert speech.played[-1][2] == 0.2
    assert panel.voice_autoplay
    assert panel.voice_rate == 0.2

    restored_speech = _FakeSpeechController()
    restored = _panel(tmp_path, restored_speech)
    assert restored.voice_autoplay
    assert restored.voice_rate == 0.2


def test_reset_and_shutdown_remove_temporary_audio_state(
    qapp: QApplication,
    tmp_path: Path,
) -> None:
    del qapp
    speech = _FakeSpeechController()
    panel = _panel(tmp_path, speech)
    _complete_one_turn(panel)
    panel.play_latest_response()

    panel.reset_conversation()
    panel.shutdown()

    assert speech.discarded == 2
    assert speech.shutdowns == 1
    assert panel.conversation == ()


def test_unavailable_voice_disables_controls_without_affecting_text_chat(
    qapp: QApplication,
    tmp_path: Path,
) -> None:
    del qapp
    speech = _FakeSpeechController(
        available=False,
        state=VoicePlaybackState.UNAVAILABLE,
    )
    panel = _panel(tmp_path, speech, locale=AppLocale.ENGLISH)
    _complete_one_turn(panel)

    play = panel.findChild(QPushButton, "mentorVoicePlayButton")
    autoplay = panel.findChild(QCheckBox, "mentorVoiceAutoplay")
    assert play is not None and not play.isEnabled()
    assert autoplay is not None and not autoplay.isEnabled()
    assert "association from causation" in panel.transcript_text
