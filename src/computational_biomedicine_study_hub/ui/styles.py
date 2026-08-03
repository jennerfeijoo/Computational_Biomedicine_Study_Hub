"""Application stylesheet rendered from semantic visual tokens."""

from __future__ import annotations

from .theme import ThemePalette, VisualTheme, palette_for

_STYLE_TEMPLATE = """
QMainWindow {
    background: @window;
}

QWidget {
    color: @text;
    font-family: "Segoe UI", "Inter", sans-serif;
    font-size: 14px;
}

QToolTip {
    background: @surface_alt;
    color: @text;
    border: 1px solid @border_strong;
    border-radius: 5px;
    padding: 6px 8px;
}

QWidget#navigationSidebar,
QWidget#navigationContainer,
QScrollArea#navigationScroll {
    background: @sidebar;
}

QLabel#productName {
    color: @sidebar_text;
    font-size: 19px;
    font-weight: 700;
    padding: 4px 8px 18px 8px;
}

QLabel#navigationSection {
    color: @sidebar_muted;
    font-size: 11px;
    font-weight: 700;
    padding: 16px 8px 4px 8px;
}

QPushButton#navigationButton {
    background: transparent;
    color: @sidebar_text;
    border: 1px solid transparent;
    border-radius: 7px;
    padding: 10px 12px;
    text-align: left;
}

QPushButton#navigationButton:hover {
    background: @sidebar_hover;
}

QPushButton#navigationButton:focus {
    border: 1px solid @focus;
}

QPushButton#navigationButton:checked {
    background: @accent;
    color: @accent_text;
    font-weight: 700;
}

QLabel#pageTitle {
    color: @text;
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
QLabel#moduleSectionNotice,
QLabel[semanticTone="muted"] {
    color: @text_muted;
}

QLabel[semanticTone="subtle"] {
    color: @text_subtle;
}

QLabel[semanticTone="success"] {
    color: @success;
}

QLabel[semanticTone="warning"] {
    color: @warning;
}

QLabel[semanticTone="error"] {
    color: @error;
}

QLabel#sectionHeading,
QLabel#adaptiveReviewSessionTitle {
    color: @text;
    font-size: 18px;
    font-weight: 700;
}

QFrame[cardRole="surface"],
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
QFrame#adaptiveReviewSessionWidget,
QFrame#reviewEmptyState,
QFrame#errorNotebookEmptyState,
QFrame#errorNotebookCard,
QGroupBox#settingsGroup {
    background: @surface;
    border: 1px solid @border;
    border-radius: 10px;
}

QFrame[cardRole="subtle"] {
    background: @surface_alt;
    border: 1px solid @border;
    border-radius: 10px;
}

QFrame#moduleContextBar {
    background: @accent_soft;
    border: none;
    border-left: 4px solid @accent;
    border-radius: 6px;
}

QGroupBox#settingsGroup {
    margin-top: 12px;
    padding: 16px;
    font-weight: 700;
}

QGroupBox#settingsGroup::title {
    color: @text;
    subcontrol-origin: margin;
    left: 12px;
    padding: 0 6px;
}

QFrame#courseCard:hover {
    border: 1px solid @accent;
}

QLabel#courseCardCode,
QLabel#courseCode,
QLabel#moduleKicker {
    color: @accent;
    font-size: 17px;
    font-weight: 700;
}

QLabel#moduleContextKicker {
    color: @accent;
    font-size: 12px;
    font-weight: 700;
}

QLabel#moduleContextTitle {
    color: @text;
    font-size: 15px;
    font-weight: 700;
}

QLabel#courseCardTitle {
    color: @text;
    font-size: 16px;
    font-weight: 600;
}

QLabel#moduleTitle {
    color: @text;
    font-size: 21px;
    font-weight: 700;
}

QLabel#contentCardTitle {
    color: @text;
    font-size: 17px;
    font-weight: 700;
}

QLabel#contentSubheading {
    color: @text_subtle;
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

QLabel#moduleSectionNotice,
QLabel#adaptiveReviewProgrammingNotice,
QLabel#adaptiveReviewRestoredResult {
    background: @accent_soft;
    color: @text;
    border: 1px solid @accent_soft_border;
    border-radius: 8px;
    padding: 12px;
}

QLineEdit,
QComboBox,
QSpinBox,
QDoubleSpinBox,
QTextEdit,
QPlainTextEdit {
    background: @surface;
    color: @text;
    border: 1px solid @border_strong;
    border-radius: 7px;
    selection-background-color: @selection;
    selection-color: @accent_text;
}

QLineEdit,
QComboBox,
QSpinBox,
QDoubleSpinBox {
    min-height: 34px;
    padding: 0 10px;
}

QTextEdit,
QPlainTextEdit {
    padding: 9px;
}

QTextBrowser#floatingTutorTranscript {
    padding: 9px 9px 18px 9px;
}

QLineEdit:focus,
QComboBox:focus,
QSpinBox:focus,
QDoubleSpinBox:focus,
QTextEdit:focus,
QPlainTextEdit:focus {
    border: 2px solid @focus;
}

QComboBox::drop-down {
    border: none;
    width: 28px;
}

QComboBox QAbstractItemView {
    background: @surface;
    color: @text;
    border: 1px solid @border_strong;
    selection-background-color: @accent_soft;
    selection-color: @text;
}

QPushButton#courseOpenButton,
QPushButton#primaryActionButton,
QPushButton[buttonRole="primary"],
QPushButton#adaptiveReviewStartButton,
QPushButton#adaptiveReviewNextButton {
    background: @accent;
    color: @accent_text;
    border: 1px solid @accent;
    border-radius: 7px;
    padding: 9px 12px;
    font-weight: 700;
}

QPushButton#courseOpenButton:hover,
QPushButton#primaryActionButton:hover,
QPushButton[buttonRole="primary"]:hover,
QPushButton#adaptiveReviewStartButton:hover,
QPushButton#adaptiveReviewNextButton:hover {
    background: @accent_hover;
    border-color: @accent_hover;
}

QPushButton#secondaryActionButton,
QPushButton[buttonRole="secondary"],
QPushButton#adaptiveReviewDiscardButton {
    background: @surface;
    color: @accent;
    border: 1px solid @border_strong;
    border-radius: 7px;
    padding: 8px 12px;
    font-weight: 700;
}

QPushButton#secondaryActionButton:hover,
QPushButton[buttonRole="secondary"]:hover,
QPushButton#adaptiveReviewDiscardButton:hover {
    background: @surface_hover;
}

QPushButton[buttonRole="danger"] {
    background: @surface;
    color: @error;
    border: 1px solid @error;
    border-radius: 7px;
    padding: 8px 12px;
    font-weight: 700;
}

QPushButton:focus {
    outline: none;
    border: 2px solid @focus;
}

QPushButton#moduleSelectorButton {
    background: @accent_soft;
    color: @accent;
    border: 1px solid @accent_soft_border;
    border-radius: 8px;
    padding: 10px 14px;
    text-align: left;
    font-weight: 600;
}

QPushButton:disabled,
QComboBox:disabled,
QLineEdit:disabled,
QTextEdit:disabled,
QPlainTextEdit:disabled {
    color: @disabled_text;
    background: @disabled_background;
    border-color: @border;
}

QPushButton#moduleSelectorButton:disabled {
    background: @accent_soft;
    color: @accent;
    border: 1px solid @accent_soft_border;
}

QTabWidget#moduleTabs::pane {
    background: @window;
    border: none;
    top: -1px;
}

QTabWidget#moduleTabs QTabBar::tab {
    background: @surface_alt;
    color: @text_subtle;
    border: 1px solid @border;
    border-bottom: none;
    padding: 9px 15px;
    margin-right: 3px;
}

QTabWidget#moduleTabs QTabBar::tab:hover {
    background: @surface_hover;
}

QTabWidget#moduleTabs QTabBar::tab:selected {
    background: @surface;
    color: @text;
    font-weight: 700;
}

QWidget#moduleScrollBody,
QScrollArea#moduleOverviewScroll,
QScrollArea#moduleConceptsScroll,
QScrollArea#moduleExamplesScroll,
QScrollArea#modulePracticeScroll,
QScrollArea#moduleAssessmentScroll {
    background: @window;
}

QScrollArea {
    border: none;
}

QScrollBar:vertical {
    background: @window;
    width: 12px;
    margin: 0;
}

QScrollBar::handle:vertical {
    background: @border_strong;
    min-height: 30px;
    border-radius: 5px;
    margin: 2px;
}

QScrollBar::handle:vertical:hover {
    background: @text_muted;
}

QScrollBar::add-line:vertical,
QScrollBar::sub-line:vertical,
QScrollBar::add-page:vertical,
QScrollBar::sub-page:vertical {
    background: transparent;
    border: none;
    height: 0;
}

QPlainTextEdit#exampleCode,
QPlainTextEdit#exampleOutput,
QPlainTextEdit#practiceCode,
QPlainTextEdit#pythonChallengeEditor,
QPlainTextEdit#pythonLabEditor {
    background: @code_background;
    color: @code_text;
    border: 1px solid @code_border;
    border-radius: 7px;
    padding: 9px;
    font-family: "Cascadia Code", "Consolas", monospace;
    font-size: 13px;
    selection-background-color: @selection;
    selection-color: @code_text;
}

QProgressBar#adaptiveReviewProgressBar {
    background: @surface_alt;
    border: 1px solid @border;
    border-radius: 5px;
    min-height: 9px;
    max-height: 9px;
}

QProgressBar#adaptiveReviewProgressBar::chunk {
    background: @accent;
    border-radius: 4px;
}

QWidget#languageSwitcher {
    background: @surface;
    border: 1px solid @border;
    border-radius: 9px;
    padding: 4px;
}

QPushButton#languageButton,
QPushButton#appearanceModeButton {
    background: transparent;
    color: @text_subtle;
    border: 1px solid transparent;
    border-radius: 6px;
    font-size: 12px;
    font-weight: 700;
}

QPushButton#languageButton:hover,
QPushButton#appearanceModeButton:hover {
    background: @surface_hover;
    color: @accent;
}

QPushButton#languageButton:checked,
QPushButton#appearanceModeButton:checked {
    background: @accent;
    color: @accent_text;
    border-color: @accent;
}

QLabel#appearanceResolvedTheme {
    color: @text_muted;
    font-size: 12px;
    font-weight: 600;
}

QLabel#ollamaStatus[connectionState="idle"] {
    color: @text_muted;
}

QLabel#ollamaStatus[connectionState="pending"] {
    color: @warning;
}

QLabel#ollamaStatus[connectionState="success"] {
    color: @success;
}

QLabel#ollamaStatus[connectionState="error"] {
    color: @error;
}

QLabel#placeholderMessage {
    color: @text_subtle;
    font-size: 16px;
    padding: 32px;
}
"""


def build_application_stylesheet(theme: VisualTheme) -> str:
    """Render the complete stylesheet from one concrete semantic palette."""

    palette = palette_for(theme)
    return _render_palette(_STYLE_TEMPLATE, palette)


def _render_palette(template: str, palette: ThemePalette) -> str:
    replacements = {
        "@window": palette.window,
        "@surface_selected": palette.surface_selected,
        "@surface_hover": palette.surface_hover,
        "@surface_alt": palette.surface_alt,
        "@surface": palette.surface,
        "@sidebar_hover": palette.sidebar_hover,
        "@sidebar_text": palette.sidebar_text,
        "@sidebar_muted": palette.sidebar_muted,
        "@sidebar": palette.sidebar,
        "@text_muted": palette.text_muted,
        "@text_subtle": palette.text_subtle,
        "@text": palette.text,
        "@border_strong": palette.border_strong,
        "@border": palette.border,
        "@accent_soft_border": palette.accent_soft_border,
        "@accent_soft": palette.accent_soft,
        "@accent_hover": palette.accent_hover,
        "@accent_text": palette.accent_text,
        "@accent": palette.accent,
        "@focus": palette.focus,
        "@success": palette.success,
        "@warning": palette.warning,
        "@error": palette.error,
        "@code_background": palette.code_background,
        "@code_text": palette.code_text,
        "@code_border": palette.code_border,
        "@disabled_background": palette.disabled_background,
        "@disabled_text": palette.disabled_text,
        "@selection": palette.selection,
    }
    rendered = template
    for token in sorted(replacements, key=len, reverse=True):
        rendered = rendered.replace(token, replacements[token])
    if "@" in rendered:
        raise ValueError("Application stylesheet contains unresolved semantic tokens.")
    return rendered


APPLICATION_STYLESHEET = build_application_stylesheet(VisualTheme.LIGHT)

__all__ = ["APPLICATION_STYLESHEET", "build_application_stylesheet"]
