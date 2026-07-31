"""Stylesheet for editable executable Python labs."""

PYTHON_LAB_STYLESHEET = """
QFrame#pythonLabWidget {
    background: #f7fafc;
    border: 1px solid #cbd5df;
    border-radius: 10px;
}

QLabel#pythonLabTitle {
    color: #1f2933;
    font-size: 16px;
    font-weight: 700;
}

QLabel#pythonLabIntro {
    color: #52606d;
}

QPlainTextEdit#pythonLabEditor,
QPlainTextEdit#pythonLabStdout,
QPlainTextEdit#pythonLabStderr,
QPlainTextEdit#pythonLabExpected {
    background: #101820;
    color: #e8eef4;
    border: 1px solid #2f3d4a;
    border-radius: 7px;
    font-family: monospace;
    selection-background-color: #2f80ed;
}

QPushButton#pythonLabRunButton {
    background: #2f80ed;
    color: #ffffff;
    border: none;
    border-radius: 7px;
    padding: 8px 14px;
    font-weight: 700;
}

QPushButton#pythonLabRunButton:hover {
    background: #2469c7;
}

QPushButton#pythonLabResetButton {
    background: #ffffff;
    color: #334e68;
    border: 1px solid #bcccdc;
    border-radius: 7px;
    padding: 8px 14px;
    font-weight: 600;
}

QPushButton#pythonLabRunButton:disabled,
QPushButton#pythonLabResetButton:disabled {
    background: #d9e2ec;
    color: #7b8794;
    border: 1px solid #cbd5df;
}

QLabel#pythonLabStatus {
    border-radius: 7px;
    padding: 9px 11px;
    font-weight: 700;
}

QLabel#pythonLabStatus[executionStatus="passed"] {
    background: #e7f6ef;
    color: #116149;
    border: 1px solid #8bd3b4;
}

QLabel#pythonLabStatus[executionStatus="output_mismatch"] {
    background: #fff7e6;
    color: #805500;
    border: 1px solid #e7c77a;
}

QLabel#pythonLabStatus[executionStatus="runtime_error"],
QLabel#pythonLabStatus[executionStatus="timed_out"],
QLabel#pythonLabStatus[executionStatus="rejected"],
QLabel#pythonLabStatus[executionStatus="output_limit"] {
    background: #fff0ee;
    color: #9f2d24;
    border: 1px solid #efaaa3;
}

QLabel#pythonLabOutputHeading {
    color: #334e68;
    font-size: 12px;
    font-weight: 700;
}
"""

__all__ = ["PYTHON_LAB_STYLESHEET"]
