"""Native Qt implementation for disposable local mentor speech.

This module is imported only on interactive Qt platforms. It synthesizes the latest
mentor response to one ephemeral WAV file and plays it locally. The pure contracts and
serialization utilities live in :mod:`computational_biomedicine_study_hub.speech.core`.
"""

from __future__ import annotations

import hashlib
import importlib
import tempfile
from collections.abc import Callable
from pathlib import Path
from typing import Any, cast

from PySide6.QtCore import QByteArray, QLocale, QObject, QUrl

from ..i18n.locales import AppLocale
from .core import (
    AudioFormatDescriptor,
    VoiceErrorCallback,
    VoicePlaybackState,
    VoiceStateCallback,
    speech_text_from_markdown,
    write_wave_file,
)

SynthesizeCallback = Callable[[Any, QByteArray], None]
SynthesizeMethod = Callable[[str, SynthesizeCallback], None]


class QtTemporaryTutorVoice(QObject):
    """Synthesize the latest mentor reply to one disposable WAV file."""

    def __init__(
        self,
        parent: QObject | None = None,
        *,
        temporary_root: Path | None = None,
    ) -> None:
        super().__init__(parent)
        self._state_callback: VoiceStateCallback = lambda state: None
        self._error_callback: VoiceErrorCallback = lambda message: None
        self._state = VoicePlaybackState.IDLE
        self._speech_module: Any | None = None
        self._speech: Any | None = None
        self._speech_import_error = ""
        self._multimedia: Any | None = None
        self._multimedia_error = ""
        self._player: Any | None = None
        self._audio_output: Any | None = None

        try:
            speech_module = importlib.import_module("PySide6.QtTextToSpeech")
        except ImportError as exc:
            self._speech_import_error = str(exc).strip() or exc.__class__.__name__
        else:
            self._speech_module = speech_module
            self._speech = speech_module.QTextToSpeech(self)
            self._speech.stateChanged.connect(self._speech_state_changed)
            self._speech.errorOccurred.connect(self._speech_error)

        try:
            multimedia = importlib.import_module("PySide6.QtMultimedia")
        except ImportError as exc:
            self._multimedia_error = str(exc).strip() or exc.__class__.__name__
        else:
            self._multimedia = multimedia
            self._player = multimedia.QMediaPlayer(self)
            self._audio_output = multimedia.QAudioOutput(self)
            self._player.setAudioOutput(self._audio_output)
            self._player.playbackStateChanged.connect(self._playback_state_changed)
            self._player.errorOccurred.connect(self._player_error)

        self._temporary_directory = tempfile.TemporaryDirectory(
            prefix="cb-study-hub-tts-",
            dir=str(temporary_root) if temporary_root is not None else None,
        )
        self._audio_path: Path | None = None
        self._cache_key = ""
        self._pending_format: AudioFormatDescriptor | None = None
        self._pending_chunks: list[bytes] = []
        self._synthesizing = False
        if not self.available:
            self._state = VoicePlaybackState.UNAVAILABLE

    @property
    def available(self) -> bool:
        """Return whether synthesis and local playback are both available."""

        if self._speech_module is None or self._speech is None:
            return False
        if self._multimedia is None or self._player is None:
            return False
        if not self._speech_module.QTextToSpeech.availableEngines():
            return False
        capabilities = self._speech.engineCapabilities()
        synthesize = self._speech_module.QTextToSpeech.Capability.Synthesize
        return bool(capabilities & synthesize)

    @property
    def state(self) -> VoicePlaybackState:
        return self._state

    @property
    def temporary_audio_path(self) -> Path | None:
        """Return the current disposable file for diagnostics and tests."""

        return self._audio_path

    def set_callbacks(
        self,
        *,
        state_changed: VoiceStateCallback,
        error: VoiceErrorCallback,
    ) -> None:
        self._state_callback = state_changed
        self._error_callback = error
        self._emit_state(self._state)

    def play_text(self, text: str, locale: AppLocale, *, rate: float = 0.0) -> None:
        spoken = speech_text_from_markdown(text)
        if not spoken:
            self._fail("The mentor response does not contain speakable text.")
            return
        if not self.available:
            self._emit_state(VoicePlaybackState.UNAVAILABLE)
            detail = (
                self._speech_import_error
                or self._multimedia_error
                or "No installed local speech engine supports temporary audio synthesis."
            )
            self._error_callback(detail)
            return

        speech = self._require_speech()
        player = self._require_player()
        bounded_rate = min(1.0, max(-1.0, rate))
        cache_key = hashlib.sha256(
            f"{locale.value}\0{bounded_rate:.3f}\0{spoken}".encode()
        ).hexdigest()
        if (
            self._audio_path is not None
            and self._audio_path.exists()
            and cache_key == self._cache_key
        ):
            player.setSource(QUrl.fromLocalFile(str(self._audio_path)))
            player.play()
            return

        self.discard()
        self._cache_key = cache_key
        self._pending_format = None
        self._pending_chunks = []
        self._synthesizing = True
        speech.setLocale(QLocale(locale.value))
        speech.setRate(bounded_rate)
        self._emit_state(VoicePlaybackState.SYNTHESIZING)
        try:
            synthesize = cast(SynthesizeMethod, speech.synthesize)
            synthesize(spoken, self._collect_pcm)
        except (AttributeError, RuntimeError, TypeError, ValueError) as exc:
            self._fail(str(exc).strip() or exc.__class__.__name__)

    def pause(self) -> None:
        if self._multimedia is None or self._player is None:
            return
        playing = self._multimedia.QMediaPlayer.PlaybackState.PlayingState
        if self._player.playbackState() is playing:
            self._player.pause()

    def resume(self) -> None:
        if self._multimedia is None or self._player is None:
            return
        paused = self._multimedia.QMediaPlayer.PlaybackState.PausedState
        if self._player.playbackState() is paused:
            self._player.play()

    def stop(self) -> None:
        if self._synthesizing:
            self._synthesizing = False
            self._pending_chunks = []
            self._pending_format = None
            if self._speech is not None:
                self._speech.stop()
        if self._player is not None:
            self._player.stop()
        if self._state not in {VoicePlaybackState.UNAVAILABLE, VoicePlaybackState.ERROR}:
            self._emit_state(VoicePlaybackState.IDLE)

    def discard(self) -> None:
        self._synthesizing = False
        self._pending_chunks = []
        self._pending_format = None
        if self._speech is not None:
            self._speech.stop()
        if self._player is not None:
            self._player.stop()
            self._player.setSource(QUrl())
        path = self._audio_path
        self._audio_path = None
        self._cache_key = ""
        if path is not None:
            try:
                path.unlink()
            except FileNotFoundError:
                pass
        self._emit_state(
            VoicePlaybackState.IDLE if self.available else VoicePlaybackState.UNAVAILABLE
        )

    def shutdown(self) -> None:
        self.discard()
        self._temporary_directory.cleanup()

    def _collect_pcm(self, audio_format: Any, data: QByteArray) -> None:
        if not self._synthesizing:
            return
        try:
            descriptor = AudioFormatDescriptor.from_qt(audio_format)
        except ValueError as exc:
            self._fail(str(exc))
            return
        if self._pending_format is None:
            self._pending_format = descriptor
        elif descriptor != self._pending_format:
            self._fail("The speech engine changed PCM format during one utterance.")
            return
        chunk = cast(bytes, data.data())
        if chunk:
            self._pending_chunks.append(chunk)

    def _speech_state_changed(self, state: Any) -> None:
        if self._speech_module is None or self._speech is None:
            return
        speech_state = self._speech_module.QTextToSpeech.State
        if state is speech_state.Error:
            self._fail(self._speech.errorString() or "Text-to-speech synthesis failed.")
            return
        if state is speech_state.Ready and self._synthesizing:
            self._finalize_synthesis()

    def _speech_error(self, reason: Any, message: str) -> None:
        del reason
        self._fail(message.strip() or "Text-to-speech synthesis failed.")

    def _playback_state_changed(self, state: Any) -> None:
        if self._synthesizing or self._multimedia is None:
            return
        playback_state = self._multimedia.QMediaPlayer.PlaybackState
        mapped = {
            playback_state.PlayingState: VoicePlaybackState.PLAYING,
            playback_state.PausedState: VoicePlaybackState.PAUSED,
            playback_state.StoppedState: VoicePlaybackState.IDLE,
        }.get(state)
        if mapped is not None:
            self._emit_state(mapped)

    def _player_error(self, error: Any, message: str) -> None:
        if self._multimedia is None:
            return
        if error is self._multimedia.QMediaPlayer.Error.NoError:
            return
        self._fail(message.strip() or "Temporary speech playback failed.")

    def _finalize_synthesis(self) -> None:
        self._synthesizing = False
        audio_format = self._pending_format
        pcm_data = b"".join(self._pending_chunks)
        self._pending_chunks = []
        self._pending_format = None
        if audio_format is None or not pcm_data:
            self._fail("The speech engine completed without returning PCM audio data.")
            return
        path = Path(self._temporary_directory.name) / f"mentor-{self._cache_key[:16]}.wav"
        try:
            write_wave_file(path, audio_format, pcm_data)
        except (OSError, ValueError) as exc:
            self._fail(str(exc).strip() or exc.__class__.__name__)
            return
        self._audio_path = path
        player = self._require_player()
        player.setSource(QUrl.fromLocalFile(str(path)))
        player.play()

    def _require_speech(self) -> Any:
        if self._speech is None:
            raise RuntimeError(self._speech_import_error or "Qt TextToSpeech is unavailable.")
        return self._speech

    def _require_player(self) -> Any:
        if self._player is None:
            raise RuntimeError(self._multimedia_error or "Qt Multimedia is unavailable.")
        return self._player

    def _fail(self, message: str) -> None:
        self._synthesizing = False
        self._pending_chunks = []
        self._pending_format = None
        self._emit_state(VoicePlaybackState.ERROR)
        self._error_callback(message)

    def _emit_state(self, state: VoicePlaybackState) -> None:
        self._state = state
        self._state_callback(state)


__all__ = ["QtTemporaryTutorVoice"]
