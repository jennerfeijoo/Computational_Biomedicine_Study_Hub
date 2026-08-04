"""Temporary local text-to-speech files for mentor responses.

The controller synthesizes raw PCM data with Qt TextToSpeech, writes one ephemeral
WAV file, and plays it through Qt Multimedia. Only the latest response is retained;
resetting or shutting down the mentor removes the file and temporary directory.
"""

from __future__ import annotations

import hashlib
import html
import re
import struct
import tempfile
from collections.abc import Callable
from dataclasses import dataclass
from enum import StrEnum
from pathlib import Path
from typing import Protocol

from PySide6.QtCore import QByteArray, QLocale, QObject, QUrl, Slot
from PySide6.QtMultimedia import QAudioFormat, QAudioOutput, QMediaPlayer
from PySide6.QtTextToSpeech import QTextToSpeech

from ..i18n.locales import AppLocale

VoiceStateCallback = Callable[["VoicePlaybackState"], None]
VoiceErrorCallback = Callable[[str], None]


class VoicePlaybackState(StrEnum):
    """Stable speech states consumed by the mentor interface."""

    UNAVAILABLE = "unavailable"
    IDLE = "idle"
    SYNTHESIZING = "synthesizing"
    PLAYING = "playing"
    PAUSED = "paused"
    ERROR = "error"


class TutorSpeechController(Protocol):
    """Minimal controller contract required by the floating mentor."""

    @property
    def available(self) -> bool:
        """Return whether temporary synthesis is currently supported."""

    @property
    def state(self) -> VoicePlaybackState:
        """Return the current synthesis or playback state."""

    def set_callbacks(
        self,
        *,
        state_changed: VoiceStateCallback,
        error: VoiceErrorCallback,
    ) -> None:
        """Register interface callbacks."""

    def play_text(self, text: str, locale: AppLocale, *, rate: float = 0.0) -> None:
        """Synthesize or replay the supplied text."""

    def pause(self) -> None:
        """Pause current playback."""

    def resume(self) -> None:
        """Resume paused playback."""

    def stop(self) -> None:
        """Stop current playback without deleting the cached response."""

    def discard(self) -> None:
        """Stop playback and remove the temporary audio file."""

    def shutdown(self) -> None:
        """Release playback resources and remove all temporary files."""


@dataclass(frozen=True, slots=True)
class AudioFormatDescriptor:
    """WAV-relevant subset of a Qt audio format."""

    sample_rate: int
    channel_count: int
    sample_width: int
    floating_point: bool = False

    def __post_init__(self) -> None:
        if self.sample_rate <= 0:
            raise ValueError("Audio sample rate must be positive.")
        if self.channel_count <= 0:
            raise ValueError("Audio channel count must be positive.")
        if self.sample_width not in {1, 2, 4}:
            raise ValueError("Temporary WAV output supports 8-, 16-, and 32-bit samples.")
        if self.floating_point and self.sample_width != 4:
            raise ValueError("Floating-point WAV output requires 32-bit samples.")

    @classmethod
    def from_qt(cls, audio_format: QAudioFormat) -> AudioFormatDescriptor:
        """Create a validated descriptor from Qt's PCM format."""

        sample_format = audio_format.sampleFormat()
        if sample_format is QAudioFormat.SampleFormat.Unknown:
            raise ValueError("The speech engine returned an unknown sample format.")
        floating = sample_format is QAudioFormat.SampleFormat.Float
        return cls(
            sample_rate=audio_format.sampleRate(),
            channel_count=audio_format.channelCount(),
            sample_width=audio_format.bytesPerSample(),
            floating_point=floating,
        )


def write_wave_file(
    path: Path,
    audio_format: AudioFormatDescriptor,
    pcm_data: bytes,
) -> None:
    """Write PCM or IEEE-float samples to a standards-compliant WAV container."""

    if not pcm_data:
        raise ValueError("Cannot write an empty speech audio file.")
    block_align = audio_format.channel_count * audio_format.sample_width
    if len(pcm_data) % block_align:
        raise ValueError("PCM byte count is not aligned to complete audio frames.")

    format_code = 3 if audio_format.floating_point else 1
    bits_per_sample = audio_format.sample_width * 8
    byte_rate = audio_format.sample_rate * block_align
    fmt_chunk = struct.pack(
        "<HHIIHH",
        format_code,
        audio_format.channel_count,
        audio_format.sample_rate,
        byte_rate,
        block_align,
        bits_per_sample,
    )
    padding = b"\x00" if len(pcm_data) % 2 else b""
    riff_size = 4 + (8 + len(fmt_chunk)) + (8 + len(pcm_data) + len(padding))
    payload = b"".join(
        (
            b"RIFF",
            struct.pack("<I", riff_size),
            b"WAVE",
            b"fmt ",
            struct.pack("<I", len(fmt_chunk)),
            fmt_chunk,
            b"data",
            struct.pack("<I", len(pcm_data)),
            pcm_data,
            padding,
        )
    )
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(payload)


def speech_text_from_markdown(text: str, *, limit: int = 8_000) -> str:
    """Convert mentor Markdown into a compact, speakable plain-text utterance."""

    if limit <= 0:
        raise ValueError("Speech text limit must be positive.")
    normalized = html.unescape(text).replace("\r\n", "\n")
    normalized = re.sub(r"```[^\n]*\n(.*?)```", r"\1", normalized, flags=re.DOTALL)
    normalized = re.sub(r"`([^`]+)`", r"\1", normalized)
    normalized = re.sub(r"!\[([^]]*)\]\([^)]*\)", r"\1", normalized)
    normalized = re.sub(r"\[([^]]+)\]\((?:https?://|file:)[^)]*\)", r"\1", normalized)
    normalized = re.sub(r"https?://\S+", "", normalized)
    normalized = re.sub(r"(?m)^\s{0,3}#{1,6}\s*", "", normalized)
    normalized = re.sub(r"(?m)^\s*[-*+]\s+", "", normalized)
    normalized = re.sub(r"(?m)^\s*\d+[.)]\s+", "", normalized)
    normalized = re.sub(r"[*_~>|]", "", normalized)
    normalized = re.sub(r"\[([A-Za-z0-9_.:-]{5,})\]", "", normalized)
    replacements = {
        "≤": " less than or equal to ",
        "≥": " greater than or equal to ",
        "≠": " not equal to ",
        "≈": " approximately ",
        "→": " leads to ",
        "←": " follows from ",
        "±": " plus or minus ",
    }
    for source, target in replacements.items():
        normalized = normalized.replace(source, target)
    normalized = re.sub(r"[ \t]+", " ", normalized)
    normalized = re.sub(r"\n{3,}", "\n\n", normalized).strip()
    return normalized[:limit].rstrip()


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
        self._speech = QTextToSpeech(self)
        self._player = QMediaPlayer(self)
        self._audio_output = QAudioOutput(self)
        self._player.setAudioOutput(self._audio_output)
        self._player.playbackStateChanged.connect(self._playback_state_changed)
        self._player.errorOccurred.connect(self._player_error)
        self._speech.stateChanged.connect(self._speech_state_changed)
        self._speech.errorOccurred.connect(self._speech_error)
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
        """Return whether the active engine can expose raw PCM synthesis."""

        if not QTextToSpeech.availableEngines():
            return False
        capabilities = self._speech.engineCapabilities()
        return bool(capabilities & QTextToSpeech.Capability.Synthesize)

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
            self._error_callback(
                "No installed Qt text-to-speech engine supports temporary audio synthesis."
            )
            return

        bounded_rate = min(1.0, max(-1.0, rate))
        cache_key = hashlib.sha256(
            f"{locale.value}\0{bounded_rate:.3f}\0{spoken}".encode()
        ).hexdigest()
        if (
            self._audio_path is not None
            and self._audio_path.exists()
            and cache_key == self._cache_key
        ):
            self._player.setSource(QUrl.fromLocalFile(str(self._audio_path)))
            self._player.play()
            return

        self.discard()
        self._cache_key = cache_key
        self._pending_format = None
        self._pending_chunks = []
        self._synthesizing = True
        self._speech.setLocale(QLocale(locale.value))
        self._speech.setRate(bounded_rate)
        self._emit_state(VoicePlaybackState.SYNTHESIZING)
        try:
            self._speech.synthesize(spoken, self._collect_pcm)  # type: ignore[call-overload]
        except (RuntimeError, TypeError, ValueError) as exc:
            self._fail(str(exc).strip() or exc.__class__.__name__)

    def pause(self) -> None:
        if self._player.playbackState() is QMediaPlayer.PlaybackState.PlayingState:
            self._player.pause()

    def resume(self) -> None:
        if self._player.playbackState() is QMediaPlayer.PlaybackState.PausedState:
            self._player.play()

    def stop(self) -> None:
        if self._synthesizing:
            self._synthesizing = False
            self._pending_chunks = []
            self._pending_format = None
            self._speech.stop()
        self._player.stop()
        if self._state not in {VoicePlaybackState.UNAVAILABLE, VoicePlaybackState.ERROR}:
            self._emit_state(VoicePlaybackState.IDLE)

    def discard(self) -> None:
        self._synthesizing = False
        self._pending_chunks = []
        self._pending_format = None
        self._speech.stop()
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
        if self.available:
            self._emit_state(VoicePlaybackState.IDLE)
        else:
            self._emit_state(VoicePlaybackState.UNAVAILABLE)

    def shutdown(self) -> None:
        self.discard()
        self._temporary_directory.cleanup()

    def _collect_pcm(self, audio_format: QAudioFormat, data: QByteArray) -> None:
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
        chunk = bytes(data)
        if chunk:
            self._pending_chunks.append(chunk)

    @Slot(QTextToSpeech.State)
    def _speech_state_changed(self, state: QTextToSpeech.State) -> None:
        if state is QTextToSpeech.State.Error:
            self._fail(self._speech.errorString() or "Text-to-speech synthesis failed.")
            return
        if state is QTextToSpeech.State.Ready and self._synthesizing:
            self._finalize_synthesis()

    @Slot(QTextToSpeech.ErrorReason, str)
    def _speech_error(self, reason: QTextToSpeech.ErrorReason, message: str) -> None:
        del reason
        self._fail(message.strip() or "Text-to-speech synthesis failed.")

    @Slot(QMediaPlayer.PlaybackState)
    def _playback_state_changed(self, state: QMediaPlayer.PlaybackState) -> None:
        if self._synthesizing:
            return
        mapped = {
            QMediaPlayer.PlaybackState.PlayingState: VoicePlaybackState.PLAYING,
            QMediaPlayer.PlaybackState.PausedState: VoicePlaybackState.PAUSED,
            QMediaPlayer.PlaybackState.StoppedState: VoicePlaybackState.IDLE,
        }[state]
        self._emit_state(mapped)

    @Slot(QMediaPlayer.Error, str)
    def _player_error(self, error: QMediaPlayer.Error, message: str) -> None:
        if error is QMediaPlayer.Error.NoError:
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
        self._player.setSource(QUrl.fromLocalFile(str(path)))
        self._player.play()

    def _fail(self, message: str) -> None:
        self._synthesizing = False
        self._pending_chunks = []
        self._pending_format = None
        self._emit_state(VoicePlaybackState.ERROR)
        self._error_callback(message)

    def _emit_state(self, state: VoicePlaybackState) -> None:
        self._state = state
        self._state_callback(state)


__all__ = [
    "AudioFormatDescriptor",
    "QtTemporaryTutorVoice",
    "TutorSpeechController",
    "VoicePlaybackState",
    "speech_text_from_markdown",
    "write_wave_file",
]
