"""Voice-enabled extension of the persistent floating mentor."""

from __future__ import annotations

from PySide6.QtCore import QSettings, Slot
from PySide6.QtWidgets import (
    QCheckBox,
    QComboBox,
    QFrame,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QVBoxLayout,
    QWidget,
)

from ...i18n.locales import DEFAULT_LOCALE, AppLocale
from ...i18n.tutor_chat_copy import TutorChatCopyKey, tutor_chat_text
from ...integrations import ChatRole
from ...learning.mentor import MentorTurnResult
from ...speech import (
    QtTemporaryTutorVoice,
    TutorSpeechController,
    VoicePlaybackState,
)
from ...storage.mentor_journal_store import MentorJournalStore
from .floating_tutor_chat import (
    ContextProvider,
    FloatingTutorChat,
    TutorChatExecutor,
    TutorChatRunner,
    TutorSelectionEventFilter,
    position_floating_tutor,
)


class VoicedFloatingTutorChat(FloatingTutorChat):
    """Add disposable local audio playback to the persistent Socratic mentor."""

    AUTOPLAY_KEY = "mentor/voice/autoplay"
    RATE_KEY = "mentor/voice/rate"

    def __init__(
        self,
        *,
        settings: QSettings,
        context_provider: ContextProvider,
        locale: AppLocale = DEFAULT_LOCALE,
        runner: TutorChatRunner | None = None,
        executor: TutorChatExecutor | None = None,
        journal_store: MentorJournalStore | None = None,
        speech_controller: TutorSpeechController | None = None,
        parent: QWidget | None = None,
    ) -> None:
        super().__init__(
            settings=settings,
            context_provider=context_provider,
            locale=locale,
            runner=runner,
            executor=executor,
            journal_store=journal_store,
            parent=parent,
        )
        self._speech = speech_controller or QtTemporaryTutorVoice(self)
        self._voice_frame = self._build_voice_controls()
        body_layout = self._body.layout()
        if not isinstance(body_layout, QVBoxLayout):
            raise RuntimeError("The floating mentor body requires a vertical layout.")
        body_layout.insertWidget(3, self._voice_frame)
        self._speech.set_callbacks(
            state_changed=self._apply_voice_state,
            error=self._show_voice_error,
        )
        self._retranslate_voice_controls()
        self._apply_voice_state(self._speech.state)

    @property
    def voice_state(self) -> VoicePlaybackState:
        """Return the current temporary-audio state."""

        return self._speech.state

    @property
    def voice_rate(self) -> float:
        """Return the selected Qt speech-rate value."""

        value = self._voice_rate_selector.currentData()
        try:
            return float(value)
        except (TypeError, ValueError):
            return 0.0

    @property
    def voice_autoplay(self) -> bool:
        """Return whether new mentor replies should be read automatically."""

        return self._voice_autoplay.isChecked()

    def set_locale(self, locale: AppLocale | str) -> None:
        """Retranslate mentor and voice controls without discarding state."""

        super().set_locale(locale)
        if hasattr(self, "_voice_play_button"):
            self._retranslate_voice_controls()
            self._apply_voice_state(self._speech.state)

    @Slot()
    def play_latest_response(self) -> None:
        """Generate and play temporary audio for the latest mentor message."""

        latest = next(
            (
                message.content
                for message in reversed(self.conversation)
                if message.role is ChatRole.ASSISTANT and message.content.strip()
            ),
            "",
        )
        if not latest:
            return
        self._speech.play_text(latest, self._locale, rate=self.voice_rate)

    @Slot()
    def toggle_voice_pause(self) -> None:
        """Pause or resume the current disposable audio file."""

        if self._speech.state is VoicePlaybackState.PAUSED:
            self._speech.resume()
        else:
            self._speech.pause()

    @Slot()
    def stop_voice(self) -> None:
        """Stop playback while retaining the latest temporary file for replay."""

        self._speech.stop()

    def reset_conversation(self) -> None:
        """Reset visible dialogue and remove its temporary audio."""

        self._speech.discard()
        super().reset_conversation()

    def close_panel(self) -> None:
        """Stop temporary playback before hiding the mentor."""

        self._speech.stop()
        super().close_panel()

    def shutdown(self) -> None:
        """Cancel generation and remove all temporary speech resources."""

        self.cancel_request()
        self._speech.shutdown()

    def _accept_response(self, request_id: int, result: MentorTurnResult) -> None:
        previous_count = len(self.conversation)
        super()._accept_response(request_id, result)
        if len(self.conversation) > previous_count and self.voice_autoplay:
            self.play_latest_response()
        else:
            self._apply_voice_state(self._speech.state)

    def _build_voice_controls(self) -> QFrame:
        frame = QFrame()
        frame.setObjectName("mentorVoiceFrame")
        frame.setProperty("cardRole", "surface")
        layout = QVBoxLayout(frame)
        layout.setContentsMargins(10, 8, 10, 8)
        layout.setSpacing(6)

        controls = QHBoxLayout()
        controls.setSpacing(6)

        self._voice_play_button = QPushButton("▶")
        self._voice_play_button.setObjectName("mentorVoicePlayButton")
        self._voice_play_button.setProperty("buttonRole", "secondary")
        self._voice_play_button.clicked.connect(self.play_latest_response)
        controls.addWidget(self._voice_play_button)

        self._voice_pause_button = QPushButton("Ⅱ")
        self._voice_pause_button.setObjectName("mentorVoicePauseButton")
        self._voice_pause_button.setProperty("buttonRole", "secondary")
        self._voice_pause_button.clicked.connect(self.toggle_voice_pause)
        controls.addWidget(self._voice_pause_button)

        self._voice_stop_button = QPushButton("■")
        self._voice_stop_button.setObjectName("mentorVoiceStopButton")
        self._voice_stop_button.setProperty("buttonRole", "secondary")
        self._voice_stop_button.clicked.connect(self.stop_voice)
        controls.addWidget(self._voice_stop_button)

        controls.addStretch(1)
        self._voice_rate_label = QLabel()
        self._voice_rate_label.setProperty("semanticTone", "subtle")
        controls.addWidget(self._voice_rate_label)

        self._voice_rate_selector = QComboBox()
        self._voice_rate_selector.setObjectName("mentorVoiceRateSelector")
        self._voice_rate_selector.addItem("0.85×", -0.20)
        self._voice_rate_selector.addItem("1.00×", 0.00)
        self._voice_rate_selector.addItem("1.15×", 0.20)
        self._voice_rate_selector.addItem("1.30×", 0.35)
        stored_rate = self._stored_rate()
        index = min(
            range(self._voice_rate_selector.count()),
            key=lambda item: abs(float(self._voice_rate_selector.itemData(item)) - stored_rate),
        )
        self._voice_rate_selector.setCurrentIndex(index)
        self._voice_rate_selector.currentIndexChanged.connect(self._persist_voice_preferences)
        controls.addWidget(self._voice_rate_selector)
        layout.addLayout(controls)

        lower = QHBoxLayout()
        self._voice_autoplay = QCheckBox()
        self._voice_autoplay.setObjectName("mentorVoiceAutoplay")
        self._voice_autoplay.setChecked(self._stored_autoplay())
        self._voice_autoplay.toggled.connect(self._persist_voice_preferences)
        lower.addWidget(self._voice_autoplay)
        lower.addStretch(1)
        layout.addLayout(lower)

        self._voice_status = QLabel()
        self._voice_status.setObjectName("mentorVoiceStatus")
        self._voice_status.setProperty("semanticTone", "subtle")
        self._voice_status.setWordWrap(True)
        self._voice_status.hide()
        layout.addWidget(self._voice_status)
        return frame

    def _retranslate_voice_controls(self) -> None:
        self._voice_play_button.setToolTip(
            tutor_chat_text(self._locale, TutorChatCopyKey.VOICE_PLAY)
        )
        self._voice_stop_button.setToolTip(
            tutor_chat_text(self._locale, TutorChatCopyKey.VOICE_STOP)
        )
        self._voice_autoplay.setText(tutor_chat_text(self._locale, TutorChatCopyKey.VOICE_AUTOPLAY))
        self._voice_rate_label.setText(tutor_chat_text(self._locale, TutorChatCopyKey.VOICE_RATE))

    def _apply_voice_state(self, state: VoicePlaybackState) -> None:
        has_response = any(message.role is ChatRole.ASSISTANT for message in self.conversation)
        available = self._speech.available and state is not VoicePlaybackState.UNAVAILABLE
        busy = state is VoicePlaybackState.SYNTHESIZING
        playing = state is VoicePlaybackState.PLAYING
        paused = state is VoicePlaybackState.PAUSED

        self._voice_play_button.setEnabled(available and has_response and not busy)
        self._voice_pause_button.setEnabled(available and (playing or paused))
        self._voice_stop_button.setEnabled(available and (busy or playing or paused))
        self._voice_rate_selector.setEnabled(available and not busy and not playing and not paused)
        self._voice_autoplay.setEnabled(available)

        pause_key = TutorChatCopyKey.VOICE_RESUME if paused else TutorChatCopyKey.VOICE_PAUSE
        self._voice_pause_button.setText("▶" if paused else "Ⅱ")
        self._voice_pause_button.setToolTip(tutor_chat_text(self._locale, pause_key))

        status_key = {
            VoicePlaybackState.UNAVAILABLE: TutorChatCopyKey.VOICE_UNAVAILABLE,
            VoicePlaybackState.SYNTHESIZING: TutorChatCopyKey.VOICE_SYNTHESIZING,
            VoicePlaybackState.PLAYING: TutorChatCopyKey.VOICE_PLAYING,
            VoicePlaybackState.PAUSED: TutorChatCopyKey.VOICE_PAUSED,
        }.get(state)
        if status_key is None:
            if state is not VoicePlaybackState.ERROR:
                self._voice_status.hide()
            return
        self._voice_status.setText(tutor_chat_text(self._locale, status_key))
        self._voice_status.show()

    def _show_voice_error(self, detail: str) -> None:
        self._voice_status.setText(
            tutor_chat_text(
                self._locale,
                TutorChatCopyKey.VOICE_ERROR,
                detail=detail,
            )
        )
        self._voice_status.show()
        self._apply_voice_state(VoicePlaybackState.ERROR)

    @Slot()
    def _persist_voice_preferences(self) -> None:
        self._settings.setValue(self.AUTOPLAY_KEY, self.voice_autoplay)
        self._settings.setValue(self.RATE_KEY, self.voice_rate)

    def _stored_autoplay(self) -> bool:
        raw = self._settings.value(self.AUTOPLAY_KEY, False)
        if isinstance(raw, bool):
            return raw
        return str(raw).strip().casefold() in {"1", "true", "yes", "on"}

    def _stored_rate(self) -> float:
        raw = self._settings.value(self.RATE_KEY, 0.0)
        try:
            return min(1.0, max(-1.0, float(str(raw))))
        except (TypeError, ValueError):
            return 0.0


__all__ = [
    "TutorSelectionEventFilter",
    "VoicedFloatingTutorChat",
    "position_floating_tutor",
]
