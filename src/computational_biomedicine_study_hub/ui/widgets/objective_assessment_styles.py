"""Localized stylesheet for randomized objective assessments."""

OBJECTIVE_ASSESSMENT_STYLESHEET = """
QFrame#objectiveAssessmentHeader,
QFrame#objectiveQuestionCard {
    background: #ffffff;
    border: 1px solid #d8e0e8;
    border-radius: 10px;
}

QLabel#objectiveAssessmentTitle {
    color: #1f2933;
    font-size: 17px;
    font-weight: 700;
}

QLabel#objectiveAssessmentMetadata {
    color: #66727f;
}

QLabel#objectiveAssessmentScore {
    background: #eaf2fd;
    color: #1d5fa7;
    border: 1px solid #b7d0ed;
    border-radius: 14px;
    padding: 5px 10px;
    font-weight: 700;
}

QLabel#objectiveQuestionNumber {
    color: #2f80ed;
    font-size: 12px;
    font-weight: 700;
}

QLabel#objectiveQuestionPrompt {
    color: #1f2933;
    font-size: 15px;
    font-weight: 600;
}

QRadioButton#objectiveOption {
    background: #f8fafc;
    color: #334e68;
    border: 1px solid #d8e0e8;
    border-radius: 7px;
    padding: 8px 10px;
    spacing: 9px;
}

QRadioButton#objectiveOption:hover {
    background: #edf4fb;
    border: 1px solid #9fc1e8;
}

QRadioButton#objectiveOption:checked {
    background: #eaf2fd;
    color: #174f8a;
    border: 1px solid #2f80ed;
    font-weight: 600;
}

QRadioButton#objectiveOption:disabled {
    color: #66727f;
}

QPushButton#checkObjectiveAnswerButton,
QPushButton#newAssessmentSessionButton {
    background: #2f80ed;
    color: #ffffff;
    border: none;
    border-radius: 7px;
    padding: 8px 12px;
    font-weight: 600;
}

QPushButton#checkObjectiveAnswerButton:hover,
QPushButton#newAssessmentSessionButton:hover {
    background: #2469c7;
}

QPushButton#checkObjectiveAnswerButton:disabled {
    background: #cbd5df;
    color: #66727f;
}

QLabel#objectiveAnswerFeedback {
    border-radius: 7px;
    padding: 10px;
}

QLabel#objectiveAnswerFeedback[answerState="correct"] {
    background: #e7f6ef;
    color: #116149;
    border: 1px solid #8bd3b4;
}

QLabel#objectiveAnswerFeedback[answerState="incorrect"] {
    background: #fff0ee;
    color: #9f2d24;
    border: 1px solid #efaaa3;
}

QLabel#objectiveAnswerFeedback[answerState="warning"] {
    background: #fff7e6;
    color: #805500;
    border: 1px solid #e7c77a;
}
"""

__all__ = ["OBJECTIVE_ASSESSMENT_STYLESHEET"]
