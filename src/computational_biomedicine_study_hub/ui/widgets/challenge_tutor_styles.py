"""Scoped stylesheet for the contextual programming tutor."""

CHALLENGE_TUTOR_STYLESHEET = """
QFrame#challengeTutorPanel {
    background: #f7f8fb;
    border: 1px solid #cfd5df;
    border-radius: 8px;
}
QLabel#challengeTutorTitle {
    font-size: 15px;
    font-weight: 700;
}
QLabel#challengeTutorIntro,
QLabel#challengeTutorStatus,
QLabel#challengeTutorNotice,
QLabel#challengeTutorSources,
QLabel#challengeTutorModel {
    color: #3f4754;
}
QLabel#challengeTutorStatus[state="ready"] {
    color: #22543d;
}
QLabel#challengeTutorStatus[state="running"] {
    color: #744210;
}
QLabel#challengeTutorStatus[state="error"] {
    color: #9b2c2c;
}
QPlainTextEdit#challengeTutorQuestion,
QTextBrowser#challengeTutorResponse {
    background: #ffffff;
    border: 1px solid #c4cad4;
    border-radius: 6px;
    padding: 7px;
}
QPushButton#challengeTutorPrimaryButton {
    font-weight: 600;
    padding: 6px 12px;
}
QPushButton#challengeTutorSecondaryButton {
    padding: 6px 12px;
}
QPushButton#challengeTutorCancelButton {
    padding: 6px 12px;
}
"""

__all__ = ["CHALLENGE_TUTOR_STYLESHEET"]
