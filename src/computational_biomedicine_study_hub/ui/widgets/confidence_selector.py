"""Reusable confidence judgement control shown before assessment feedback."""

from __future__ import annotations

from PySide6.QtWidgets import (
    QButtonGroup,
    QFrame,
    QHBoxLayout,
    QLabel,
    QRadioButton,
    QVBoxLayout,
    QWidget,
)

from ...i18n.confidence_copy import ConfidenceCopyKey, confidence_text
from ...i18n.locales import DEFAULT_LOCALE, AppLocale
from ...learning.progress import ConfidenceLevel


class ConfidenceSelector(QFrame):
    """Collect a low, medium or high confidence judgement."""

    def __init__(
        self,
        parent: QWidget | None = None,
        *,
        locale: AppLocale = DEFAULT_LOCALE,
    ) -> None:
        super().__init__(parent)
        self.setObjectName("confidenceSelector")

        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 4, 0, 4)
        layout.setSpacing(6)

        prompt = QLabel(confidence_text(locale, ConfidenceCopyKey.PROMPT))
        prompt.setObjectName("confidencePrompt")
        prompt.setWordWrap(True)
        layout.addWidget(prompt)

        choices = QWidget()
        choices_layout = QHBoxLayout(choices)
        choices_layout.setContentsMargins(0, 0, 0, 0)
        choices_layout.setSpacing(12)

        self._button_group = QButtonGroup(self)
        self._button_group.setExclusive(True)
        self._buttons: dict[ConfidenceLevel, QRadioButton] = {}
        for level in ConfidenceLevel:
            button = QRadioButton(confidence_text(locale, level))
            button.setObjectName("confidenceOption")
            button.setProperty("confidenceLevel", level.value)
            self._button_group.addButton(button)
            self._buttons[level] = button
            choices_layout.addWidget(button)
        choices_layout.addStretch(1)
        layout.addWidget(choices)

    @property
    def selected_confidence(self) -> ConfidenceLevel | None:
        """Return the selected confidence level, or ``None`` before selection."""

        selected = self._button_group.checkedButton()
        if selected is None:
            return None
        value = selected.property("confidenceLevel")
        return ConfidenceLevel(value) if isinstance(value, str) else None

    def choose(self, level: ConfidenceLevel) -> None:
        """Select one confidence level programmatically."""

        self._buttons[level].setChecked(True)

    def clear(self) -> None:
        """Clear the current judgement so a later attempt requires a fresh choice."""

        self._button_group.setExclusive(False)
        for button in self._buttons.values():
            button.setChecked(False)
        self._button_group.setExclusive(True)

    def set_interaction_enabled(self, enabled: bool) -> None:
        """Enable or disable all confidence choices."""

        for button in self._buttons.values():
            button.setEnabled(enabled)


__all__ = ["ConfidenceSelector"]
