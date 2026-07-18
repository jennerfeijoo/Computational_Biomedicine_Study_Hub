"""Localized stylesheet for guided formative-practice widgets."""

GUIDED_PRACTICE_STYLESHEET = """
QFrame#guidedPracticeHeader,
QFrame#guidedPracticeCard,
QFrame#guidedPracticeSolution {
    background: #ffffff;
    border: 1px solid #d8e0e8;
    border-radius: 10px;
}

QFrame#guidedPracticeHeader {
    background: #f8fafc;
}

QLabel#guidedPracticeTitle {
    color: #1f2933;
    font-size: 17px;
    font-weight: 700;
}

QLabel#guidedPracticeMetadata,
QLabel#guidedPracticeProgress,
QLabel#guidedPracticeExerciseType {
    color: #66727f;
}

QLabel#guidedPracticeProgress {
    font-weight: 600;
}

QLabel#guidedPracticeExerciseNumber {
    color: #2f80ed;
    font-size: 13px;
    font-weight: 700;
}

QLabel#guidedPracticePrompt {
    color: #1f2933;
    font-size: 15px;
    font-weight: 600;
}

QPlainTextEdit#guidedPracticeAnswerEditor {
    background: #fbfcfd;
    color: #1f2933;
    border: 1px solid #cbd5df;
    border-radius: 7px;
    padding: 9px;
    font-family: "Cascadia Code", "Consolas", monospace;
    selection-background-color: #2f80ed;
}

QPlainTextEdit#guidedPracticeAnswerEditor:focus {
    border: 1px solid #2f80ed;
}

QLabel#guidedPracticeHint {
    background: #fff8e8;
    color: #6f4e00;
    border: 1px solid #eed59a;
    border-radius: 7px;
    padding: 10px;
}

QFrame#guidedPracticeSolution {
    background: #f6f9fc;
    padding: 2px;
}

QLabel#guidedPracticeSolutionTitle {
    color: #243b53;
    font-weight: 700;
}

QLabel#guidedPracticeSolutionText,
QLabel#guidedPracticeExplanation {
    color: #394b59;
}

QPushButton#guidedPracticeSecondaryButton,
QPushButton#guidedPracticeSolvedButton,
QPushButton#guidedPracticeReviewButton,
QPushButton#newGuidedPracticeButton {
    background: #ffffff;
    color: #245a96;
    border: 1px solid #9eb6cf;
    border-radius: 7px;
    padding: 8px 12px;
    font-weight: 600;
}

QPushButton#guidedPracticeSecondaryButton:hover,
QPushButton#newGuidedPracticeButton:hover {
    background: #edf4fb;
}

QPushButton#guidedPracticeSolvedButton:checked {
    background: #e8f7ef;
    color: #146c43;
    border: 1px solid #7bc69f;
}

QPushButton#guidedPracticeReviewButton:checked {
    background: #fff1ed;
    color: #a63a25;
    border: 1px solid #e8a293;
}

QPushButton#guidedPracticeSecondaryButton:disabled {
    color: #96a1ad;
    background: #edf1f5;
    border-color: #d8e0e8;
}
"""

__all__ = ["GUIDED_PRACTICE_STYLESHEET"]
