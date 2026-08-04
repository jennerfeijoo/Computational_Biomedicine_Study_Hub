"""Local speech synthesis and temporary audio playback services."""

from __future__ import annotations

import os
from collections.abc import Callable
from pathlib import Path

from PySide6.QtCore import QObject

from ..i18n.locales import AppLocale
from .temporary_tutor_voice import (
    AudioFormatDescriptor,
    QtTemporaryTutorVoice as _QtTemporaryTutorVoice,
    TutorSpeechController,
    VoicePlaybackState,
    speech_text_from_markdown,
    write_wave_file,
)


class _UnavailableTutorVoice(_QtTemporaryTutorVoice):
    """Avoid constructing native audio objects on Qt's headless platform."""

    def __init__(
        self,
        parent: QObject | None = None,
        *,
        temporary_root: Path | None = None,
    ) -> None:
        del temporary_root
        QObject.__init__(self, parent)
        self._voice_state_callback: Callable[[VoicePlaybackState], None] = lambda state: None
        self._voice_error_callback: Callable[[str], None] = lambda detail: None

    @property
    def available(self) -> bool:
        return False

    @property
    def state(self) -> VoicePlaybackState:
        return VoicePlaybackState.UNAVAILABLE

    @property
    def temporary_audio_path(self) -> Path | None:
        return None

    def set_callbacks(
        self,
        *,
        state_changed: Callable[[VoicePlaybackState], None],
        error: Callable[[str], None],
    ) -> None:
        self._voice_state_callback = state_changed
        self._voice_error_callback = error
        state_changed(VoicePlaybackState.UNAVAILABLE)

    def play_text(self, text: str, locale: AppLocale, *, rate: float = 0.0) -> None:
        del text, locale, rate
        self._voice_state_callback(VoicePlaybackState.UNAVAILABLE)
        self._voice_error_callback(
            "Temporary speech is disabled while Qt uses the offscreen platform."
        )

    def pause(self) -> None:
        pass

    def resume(self) -> None:
        pass

    def stop(self) -> None:
        pass

    def discard(self) -> None:
        pass

    def shutdown(self) -> None:
        pass


QtTemporaryTutorVoice: type[_QtTemporaryTutorVoice] = (
    _UnavailableTutorVoice
    if os.environ.get("QT_QPA_PLATFORM", "").strip().casefold() == "offscreen"
    else _QtTemporaryTutorVoice
)

__all__ = [
    "AudioFormatDescriptor",
    "QtTemporaryTutorVoice",
    "TutorSpeechController",
    "VoicePlaybackState",
    "speech_text_from_markdown",
    "write_wave_file",
]
