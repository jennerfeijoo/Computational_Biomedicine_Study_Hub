"""Styles for the persistent language selector."""

LANGUAGE_STYLESHEET = """
QWidget#languageSwitcher {
    background: #ffffff;
    border: 1px solid #d8e0e8;
    border-radius: 9px;
    padding: 4px;
}

QPushButton#languageButton {
    background: transparent;
    color: #52606d;
    border: 1px solid transparent;
    border-radius: 6px;
    font-size: 12px;
    font-weight: 700;
}

QPushButton#languageButton:hover {
    background: #edf4fb;
    color: #1d5fa7;
}

QPushButton#languageButton:checked {
    background: #2f80ed;
    color: #ffffff;
    border-color: #2f80ed;
}
"""

__all__ = ["LANGUAGE_STYLESHEET"]
