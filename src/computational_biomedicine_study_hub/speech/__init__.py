"""Local speech synthesis and temporary audio playback services."""

from __future__ import annotations

import os
from collections.abc import Callable
from pathlib import Path
from typing import Protocol, cast

from ..i18n.locales import AppLocale
from .core import (
    AudioFormatDescriptor,
    TutorSpeechController,
    VoicePlaybackState,
    speech_text_from_markdown,
    write_wave_file,
)


class _VoiceControllerFactory(Protocol):
    def __call__(
        self,
        parent: object | None = None,
        *,
        temporary_root: Path | None = None,
    ) -> TutorSpeechController: ...


class _UnavailableTutorVoice:
    """Headless controller that never imports native Qt audio modules."""

    def __init__(
        self,
        parent: object | None = None,
        *,
        temporary_root: Path | None = None,
    ) -> None:
        del parent, temporary_root
        self._state_callback: Callable[[VoicePlaybackState], None] = lambda state: None
        self._error_callback: Callable[[str], None] = lambda detail: None

    @property
    def available(self) -> bool:
        return False

    @property
    def state(self) -> VoicePlaybackState:
        return VoicePlaybackState.UNAVAILABLE

    def set_callbacks(
        self,
        *,
        state_changed: Callable[[VoicePlaybackState], None],
        error: Callable[[str], None],
    ) -> None:
        self._state_callback = state_changed
        self._error_callback = error
        state_changed(VoicePlaybackState.UNAVAILABLE)

    def play_text(self, text: str, locale: AppLocale, *, rate: float = 0.0) -> None:
        del text, locale, rate
        self._state_callback(VoicePlaybackState.UNAVAILABLE)
        self._error_callback(
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


if os.environ.get("QT_QPA_PLATFORM", "").strip().casefold() == "offscreen":
    QtTemporaryTutorVoice = cast(_VoiceControllerFactory, _UnavailableTutorVoice)
else:
    from .temporary_tutor_voice import QtTemporaryTutorVoice as _NativeTutorVoice

    QtTemporaryTutorVoice = cast(_VoiceControllerFactory, _NativeTutorVoice)


__all__ = [
    "AudioFormatDescriptor",
    "QtTemporaryTutorVoice",
    "TutorSpeechController",
    "VoicePlaybackState",
    "speech_text_from_markdown",
    "write_wave_file",
]
