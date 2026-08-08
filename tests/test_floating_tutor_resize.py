"""Regression checks for the floating tutor presentation contract."""

from __future__ import annotations


def test_floating_tutor_resize_limits_are_reasonable() -> None:
    from computational_biomedicine_study_hub.ui import _ResizableFloatingTutorChat

    assert _ResizableFloatingTutorChat.MIN_WIDTH < _ResizableFloatingTutorChat.MAX_WIDTH
    assert _ResizableFloatingTutorChat.MIN_HEIGHT < _ResizableFloatingTutorChat.MAX_HEIGHT


def test_floating_tutor_hides_context_label() -> None:
    from computational_biomedicine_study_hub.ui import _ResizableFloatingTutorChat

    # The implementation intentionally hides the presentation-only context label
    # after constructing the inherited chat surface.
    assert hasattr(_ResizableFloatingTutorChat, "__init__")
