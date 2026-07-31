"""Stylesheet for executable starter-code challenges."""

PYTHON_CHALLENGE_STYLESHEET = """
QFrame#pythonChallengeWidget {
    background: #f8fafc;
    border: 1px solid #cbd5df;
    border-radius: 10px;
}

QLabel#pythonChallengeTitle {
    color: #1f2933;
    font-size: 16px;
    font-weight: 700;
}

QLabel#pythonChallengeIntro,
QLabel#pythonChallengeHeading {
    color: #52606d;
}

QLabel#pythonChallengeHeading {
    font-weight: 700;
}

QPlainTextEdit#pythonChallengeEditor {
    background: #111827;
    color: #f8fafc;
    border: 1px solid #334155;
    border-radius: 7px;
    padding: 8px;
    font-family: monospace;
}

QPushButton#pythonChallengeRunButton {
    background: #2f80ed;
    color: #ffffff;
    border: none;
    border-radius: 7px;
    padding: 8px 12px;
    font-weight: 600;
}

QPushButton#pythonChallengeRunButton:hover {
    background: #2469c7;
}

QPushButton#pythonChallengeResetButton {
    background: #ffffff;
    color: #334e68;
    border: 1px solid #aebdcc;
    border-radius: 7px;
    padding: 8px 12px;
    font-weight: 600;
}

QPushButton#pythonChallengeRunButton:disabled,
QPushButton#pythonChallengeResetButton:disabled {
    background: #d9e2ec;
    color: #7b8794;
}

QLabel#pythonChallengeStatus,
QLabel#pythonChallengeHiddenSummary,
QLabel#pythonChallengeCaseResult {
    border-radius: 7px;
    padding: 9px;
}

QLabel#pythonChallengeStatus[resultState="passed"],
QLabel#pythonChallengeCaseResult[resultState="passed"] {
    background: #e7f6ef;
    color: #116149;
    border: 1px solid #8bd3b4;
}

QLabel#pythonChallengeStatus[resultState="incomplete"],
QLabel#pythonChallengeCaseResult[resultState="failed"],
QLabel#pythonChallengeCaseResult[resultState="error"] {
    background: #fff0ee;
    color: #9f2d24;
    border: 1px solid #efaaa3;
}

QLabel#pythonChallengeCaseResult[resultState="timed_out"],
QLabel#pythonChallengeCaseResult[resultState="rejected"],
QLabel#pythonChallengeCaseResult[resultState="output_limit"] {
    background: #fff7e6;
    color: #805500;
    border: 1px solid #e7c77a;
}

QLabel#pythonChallengeHiddenSummary {
    background: #edf4fb;
    color: #174f8a;
    border: 1px solid #b7d0ed;
    font-weight: 600;
}
"""

__all__ = ["PYTHON_CHALLENGE_STYLESHEET"]
