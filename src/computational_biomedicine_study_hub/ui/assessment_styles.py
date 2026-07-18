"""Styles for the compact module reader and interactive assessments."""

ASSESSMENT_STYLESHEET = """
QFrame#moduleCompactBar {
    background: #ffffff;
    border: 1px solid #d8e0e8;
    border-radius: 8px;
}

QLabel#moduleKicker {
    color: #2f80ed;
    font-size: 13px;
    font-weight: 700;
}

QLabel#moduleCompactTitle {
    color: #1f2933;
    font-size: 16px;
    font-weight: 700;
}

QTabWidget#moduleTabs QTabBar::tab {
    padding: 7px 13px;
}

QWidget#assessmentSessionWidget {
    background: #f4f6f8;
}

QLabel#assessmentBankSummary {
    color: #52606d;
    font-size: 13px;
}

QFrame#interactiveAssessmentCard {
    background: #ffffff;
    border: 1px solid #d8e0e8;
    border-radius: 10px;
}

QLabel#assessmentProgress {
    color: #2f80ed;
    font-size: 13px;
    font-weight: 700;
}

QLabel#interactiveAssessmentPrompt {
    color: #1f2933;
    font-size: 17px;
    font-weight: 650;
    line-height: 1.35;
}

QRadioButton#assessmentOption {
    background: #f8fafc;
    border: 1px solid #d8e0e8;
    border-radius: 8px;
    padding: 10px 12px;
    spacing: 10px;
}

QRadioButton#assessmentOption:hover {
    background: #edf4fb;
    border: 1px solid #9fc1e8;
}

QRadioButton#assessmentOption:checked {
    background: #eaf2fd;
    border: 1px solid #2f80ed;
}

QRadioButton#assessmentOption[answerState="correct"] {
    background: #ecfdf3;
    border: 1px solid #4cae7c;
    color: #146c43;
}

QRadioButton#assessmentOption[answerState="incorrect"] {
    background: #fff1f0;
    border: 1px solid #e59a93;
    color: #9f2d24;
}

QRadioButton#assessmentOption[answerState="neutral"] {
    color: #66727f;
}

QLabel#assessmentFeedback {
    border-radius: 8px;
    padding: 12px;
    line-height: 1.35;
}

QLabel#assessmentFeedback[resultState="correct"] {
    background: #ecfdf3;
    border: 1px solid #9bd5b6;
    color: #146c43;
}

QLabel#assessmentFeedback[resultState="incorrect"] {
    background: #fff1f0;
    border: 1px solid #efb0aa;
    color: #8f271f;
}
"""
