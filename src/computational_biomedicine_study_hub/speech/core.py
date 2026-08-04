"""Pure-Python contracts and utilities for disposable mentor speech.

This module deliberately avoids importing Qt. Headless tests and deployments can use
text normalization, WAV serialization, and the controller protocol without loading
native speech or multimedia libraries.
"""

from __future__ import annotations

import html
import re
import struct
from collections.abc import Callable
from dataclasses import dataclass
from enum import StrEnum
from pathlib import Path
from typing import Any, Protocol

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
    def from_qt(cls, audio_format: Any) -> AudioFormatDescriptor:
        """Create a validated descriptor from a Qt PCM-format object."""

        sample_format = audio_format.sampleFormat()
        sample_name = str(getattr(sample_format, "name", ""))
        sample_width = int(audio_format.bytesPerSample())
        if sample_name == "Unknown" or sample_width <= 0:
            raise ValueError("The speech engine returned an unknown sample format.")
        return cls(
            sample_rate=int(audio_format.sampleRate()),
            channel_count=int(audio_format.channelCount()),
            sample_width=sample_width,
            floating_point=sample_name == "Float",
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
    normalized = re.sub(r"[*~>|]", "", normalized)
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


__all__ = [
    "AudioFormatDescriptor",
    "TutorSpeechController",
    "VoiceErrorCallback",
    "VoicePlaybackState",
    "VoiceStateCallback",
    "speech_text_from_markdown",
    "write_wave_file",
]
