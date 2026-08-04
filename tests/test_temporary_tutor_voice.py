"""Tests for disposable mentor speech text and WAV generation."""

from __future__ import annotations

import struct
from pathlib import Path

import pytest

from computational_biomedicine_study_hub.speech import (
    AudioFormatDescriptor,
    speech_text_from_markdown,
    write_wave_file,
)


def test_speech_text_removes_markdown_links_and_source_ids() -> None:
    source = (
        "## Main point\n\n"
        "- Compare `group_a` with **group_b**.\n"
        "- Read [the documentation](https://example.org).\n\n"
        "```python\nprint('diagnostic')\n```\n\n"
        "The interval is ≤ 5 [bmb830.m04.overview]."
    )

    spoken = speech_text_from_markdown(source)

    assert "##" not in spoken
    assert "https://" not in spoken
    assert "bmb830.m04.overview" not in spoken
    assert "group_a" in spoken
    assert "print('diagnostic')" in spoken
    assert "less than or equal to" in spoken


def test_speech_text_enforces_a_positive_bounded_limit() -> None:
    assert speech_text_from_markdown("abcdef", limit=4) == "abcd"
    with pytest.raises(ValueError, match="positive"):
        speech_text_from_markdown("text", limit=0)


def test_write_wave_file_emits_valid_pcm_riff_header(tmp_path: Path) -> None:
    path = tmp_path / "mentor.wav"
    audio_format = AudioFormatDescriptor(
        sample_rate=16_000,
        channel_count=1,
        sample_width=2,
    )
    pcm_data = struct.pack("<hhhh", 0, 100, -100, 0)

    write_wave_file(path, audio_format, pcm_data)

    payload = path.read_bytes()
    assert payload[:4] == b"RIFF"
    assert payload[8:12] == b"WAVE"
    assert payload[12:16] == b"fmt "
    assert struct.unpack("<H", payload[20:22])[0] == 1
    assert struct.unpack("<H", payload[22:24])[0] == 1
    assert struct.unpack("<I", payload[24:28])[0] == 16_000
    assert payload[36:40] == b"data"
    assert struct.unpack("<I", payload[40:44])[0] == len(pcm_data)
    assert payload[44:] == pcm_data


def test_write_wave_file_rejects_misaligned_or_empty_pcm(tmp_path: Path) -> None:
    path = tmp_path / "mentor.wav"
    audio_format = AudioFormatDescriptor(16_000, 2, 2)

    with pytest.raises(ValueError, match="empty"):
        write_wave_file(path, audio_format, b"")
    with pytest.raises(ValueError, match="aligned"):
        write_wave_file(path, audio_format, b"\x00\x01")
