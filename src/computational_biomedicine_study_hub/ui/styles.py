"""Application-level stylesheet."""

APPLICATION_STYLESHEET = """
QMainWindow {
    background: #f4f6f8;
}

QWidget {
    color: #1f2933;
    font-family: "Segoe UI", "Inter", sans-serif;
    font-size: 14px;
}

QWidget#navigationSidebar,
QWidget#navigationContainer,
QScrollArea#navigationScroll {
    background: #17212b;
}

QLabel#productName {
    color: #ffffff;
    font-size: 19px;
    font-weight: 700;
    padding: 4px 8px 18px 8px;
}

QLabel#navigationSection {
    color: #8fa1b3;
    font-size: 11px;
    font-weight: 700;
    padding: 16px 8px 4px 8px;
}

QPushButton#navigationButton {
    background: transparent;
    color: #dbe4ec;
    border: none;
    border-radius: 7px;
    padding: 10px 12px;
    text-align: left;
}

QPushButton#navigationButton:hover {
    background: #243443;
}

QPushButton#navigationButton:checked {
    background: #2f80ed;
    color: #ffffff;
    font-weight: 600;
}

QLabel#pageTitle {
    font-size: 26px;
    font-weight: 700;
}

QLabel#pageSubtitle,
QLabel#homeDescription,
QLabel#courseCardMetadata,
QLabel#courseCardSummary,
QLabel#courseSummary,
QLabel#courseNotice,
QLabel#settingsExplanation,
QLabel#moduleSummary,
QLabel#moduleSectionNotice {
    color: #66727f;
}

QLabel#sectionHeading {
    font-size: 18px;
    font-weight: 700;
}

QFrame#courseCard,
QFrame#courseIdentityCard,
QFrame#moduleIdentityCard,
QFrame#moduleOverviewCard,
QFrame#moduleObjectivesCard,
QFrame#moduleSequenceCard,
QFrame#conceptCard,
QFrame#exampleCard,
QFrame#practiceCard,
QFrame#assessmentCard,
QGroupBox#settingsGroup {
    background: #ffffff;
    border: 1px solid #d8e0e8;
    border-radius: 10px;
}

QFrame#moduleContextBar {
    background: #eaf2fd;
    border: none;
    border-left: 4px solid #2f80ed;
    border-radius: 6px;
}

QGroupBox#settingsGroup {
    margin-top: 12px;
    padding: 16px;
    font-weight: 700;
}

QGroupBox#settingsGroup::title {
    subcontrol-origin: margin;
    left: 12px;
    padding: 0 6px;
}

QFrame#courseCard:hover {
    border: 1px solid #2f80ed;
}

QLabel#courseCardCode,
QLabel#courseCode,
QLabel#moduleKicker {
    color: #2f80ed;
    font-size: 17px;
    font-weight: 700;
}

QLabel#moduleContextKicker {
    color: #1d5fa7;
    font-size: 12px;
    font-weight: 700;
}

QLabel#moduleContextTitle {
    color: #243b53;
    font-size: 15px;
    font-weight: 700;
}

QLabel#courseCardTitle {
    font-size: 16px;
    font-weight: 600;
}

QLabel#moduleTitle {
    font-size: 21px;
    font-weight: 700;
}

QLabel#contentCardTitle {
    font-size: 17px;
    font-weight: 700;
}

QLabel#contentSubheading {
    color: #394b59;
    font-size: 13px;
    font-weight: 700;
    padding-top: 4px;
}

QLabel#courseCardSummary,
QLabel#courseSummary,
QLabel#courseSectionList,
QLabel#courseNotice,
QLabel#moduleSummary,
QLabel#contentBody,
QLabel#contentPrompt,
QLabel#contentBulletList,
QLabel#assessmentPrompt,
QLabel#assessmentOptions,
QLabel#assessmentRubric {
    line-height: 1.35;
}

QLabel#moduleSectionNotice {
    background: #edf4fb;
    border: 1px solid #c7d9ec;
    border-radius: 8px;
    padding: 12px;
}

QLineEdit#ollamaBaseUrl,
QComboBox#ollamaModelSelector {
    background: #ffffff;
    border: 1px solid #cbd5df;
    border-radius: 7px;
    min-height: 34px;
    padding: 0 10px;
}

QLineEdit#ollamaBaseUrl:focus,
QComboBox#ollamaModelSelector:focus {
    border: 1px solid #2f80ed;
}

QPushButton#courseOpenButton,
QPushButton#primaryActionButton {
    background: #2f80ed;
    color: #ffffff;
    border: none;
    border-radius: 7px;
    padding: 9px 12px;
    font-weight: 600;
}

QPushButton#courseOpenButton:hover,
QPushButton#primaryActionButton:hover {
    background: #2469c7;
}

QPushButton#secondaryActionButton {
    background: #ffffff;
    color: #245a96;
    border: 1px solid #9eb6cf;
    border-radius: 7px;
    padding: 8px 12px;
    font-weight: 600;
}

QPushButton#secondaryActionButton:hover {
    background: #edf4fb;
}

QPushButton#moduleSelectorButton {
    background: #eaf2fd;
    color: #1d5fa7;
    border: 1px solid #9fc1e8;
    border-radius: 8px;
    padding: 10px 14px;
    text-align: left;
    font-weight: 600;
}

QPushButton:disabled,
QComboBox:disabled {
    color: #96a1ad;
    background: #edf1f5;
}

QPushButton#moduleSelectorButton:disabled {
    background: #eaf2fd;
    color: #1d5fa7;
    border: 1px solid #9fc1e8;
}

QTabWidget#moduleTabs::pane {
    background: #f4f6f8;
    border: none;
    top: -1px;
}

QTabWidget#moduleTabs QTabBar::tab {
    background: #e5eaf0;
    color: #52606d;
    border: 1px solid #cbd5df;
    border-bottom: none;
    padding: 9px 15px;
    margin-right: 3px;
}

QTabWidget#moduleTabs QTabBar::tab:selected {
    background: #ffffff;
    color: #1f2933;
    font-weight: 700;
}

QWidget#moduleScrollBody,
QScrollArea#moduleOverviewScroll,
QScrollArea#moduleConceptsScroll,
QScrollArea#moduleExamplesScroll,
QScrollArea#modulePracticeScroll,
QScrollArea#moduleAssessmentScroll {
    background: #f4f6f8;
}

QPlainTextEdit#exampleCode,
QPlainTextEdit#exampleOutput,
QPlainTextEdit#practiceCode {
    background: #101820;
    color: #e6edf3;
    border: 1px solid #263746;
    border-radius: 7px;
    padding: 9px;
    font-family: "Cascadia Code", "Consolas", monospace;
    font-size: 13px;
    selection-background-color: #2f80ed;
}

QLabel#ollamaStatus[connectionState="idle"] {
    color: #66727f;
}

QLabel#ollamaStatus[connectionState="pending"] {
    color: #8a5a00;
}

QLabel#ollamaStatus[connectionState="success"] {
    color: #16734a;
}

QLabel#ollamaStatus[connectionState="error"] {
    color: #b42318;
}

QLabel#placeholderMessage {
    color: #52606d;
    font-size: 16px;
    padding: 32px;
}
"""
