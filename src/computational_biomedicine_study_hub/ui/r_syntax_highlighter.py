"""Small, execution-free syntax highlighter for authored R examples."""

from __future__ import annotations

from dataclasses import dataclass

from PySide6.QtCore import QRegularExpression
from PySide6.QtGui import QColor, QSyntaxHighlighter, QTextCharFormat, QTextDocument


def _format(color: str, *, bold: bool = False, italic: bool = False) -> QTextCharFormat:
    value = QTextCharFormat()
    value.setForeground(QColor(color))
    value.setFontWeight(700 if bold else 400)
    value.setFontItalic(italic)
    return value


@dataclass(frozen=True, slots=True)
class _Rule:
    pattern: QRegularExpression
    text_format: QTextCharFormat


class RSyntaxHighlighter(QSyntaxHighlighter):
    """Highlight common R tokens without parsing or executing source code."""

    def __init__(self, document: QTextDocument) -> None:
        super().__init__(document)
        self._rules = (
            _Rule(
                QRegularExpression(r"\b(if|else|repeat|while|function|for|in|next|break)\b"),
                _format("#ff7b72", bold=True),
            ),
            _Rule(
                QRegularExpression(r"\b(TRUE|FALSE|NA|NaN|Inf|NULL)\b"),
                _format("#79c0ff", bold=True),
            ),
            _Rule(
                QRegularExpression(r"\b(?:\d+(?:\.\d*)?|\.\d+)(?:[eE][+-]?\d+)?L?\b"),
                _format("#a5d6ff"),
            ),
            _Rule(
                QRegularExpression(r"\b[A-Za-z.][A-Za-z0-9._]*(?=\s*\()"),
                _format("#d2a8ff"),
            ),
            _Rule(
                QRegularExpression(r"(?:<<-|<-|->>|->|\|>|%[^%\r\n]+%|~|:::{0,1})"),
                _format("#ffa657", bold=True),
            ),
            _Rule(
                QRegularExpression(r'"(?:\\.|[^"\\])*"|\'(?:\\.|[^\'\\])*\''),
                _format("#a5d6ff"),
            ),
        )
        self._comment_format = _format("#8b949e", italic=True)

    def highlightBlock(self, text: str) -> None:  # noqa: N802
        """Apply deterministic lexical rules to one visible line."""
        for rule in self._rules:
            matches = rule.pattern.globalMatch(text)
            while matches.hasNext():
                match = matches.next()
                self.setFormat(
                    match.capturedStart(),
                    match.capturedLength(),
                    rule.text_format,
                )
        comment_start = self._comment_start(text)
        if comment_start >= 0:
            self.setFormat(
                comment_start,
                len(text) - comment_start,
                self._comment_format,
            )

    @staticmethod
    def _comment_start(text: str) -> int:
        quote = ""
        escaped = False
        for index, character in enumerate(text):
            if escaped:
                escaped = False
                continue
            if character == "\\":
                escaped = True
                continue
            if quote:
                if character == quote:
                    quote = ""
                continue
            if character in {"'", '"'}:
                quote = character
            elif character == "#":
                return index
        return -1


__all__ = ["RSyntaxHighlighter"]
