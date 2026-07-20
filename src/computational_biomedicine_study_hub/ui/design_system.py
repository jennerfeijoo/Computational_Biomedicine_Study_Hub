"""Visual design tokens and reusable effects for the academic interface."""

from __future__ import annotations

from dataclasses import dataclass

from PySide6.QtGui import QColor
from PySide6.QtWidgets import QGraphicsDropShadowEffect, QWidget


@dataclass(frozen=True, slots=True)
class DesignTokens:
    """Stable visual constants shared across learner-facing pages."""

    canvas: str = "#F7F9FC"
    surface: str = "#FFFFFF"
    surface_muted: str = "#F1F5F9"
    border: str = "#D8E1EA"
    border_strong: str = "#B9C7D5"
    text: str = "#172033"
    text_muted: str = "#64748B"
    primary: str = "#2563EB"
    primary_hover: str = "#1D4ED8"
    primary_soft: str = "#E8F0FF"
    success: str = "#16805C"
    warning: str = "#B7791F"
    danger: str = "#C0392B"
    sidebar: str = "#121C28"
    sidebar_hover: str = "#1E2D3D"
    sidebar_active: str = "#2563EB"
    radius_small: int = 8
    radius_medium: int = 12
    radius_large: int = 18
    spacing_small: int = 8
    spacing_medium: int = 16
    spacing_large: int = 24


TOKENS = DesignTokens()

COURSE_ACCENTS: dict[str, str] = {
    "DM857": "#0EA5E9",
    "DM847": "#0F9D78",
    "BMB830": "#7C3AED",
    "BMB831": "#4F46E5",
}


def apply_elevation(widget: QWidget, *, blur_radius: int = 24, y_offset: int = 6) -> None:
    """Apply a restrained shadow suitable for cards on the light canvas."""

    shadow = QGraphicsDropShadowEffect(widget)
    shadow.setBlurRadius(float(blur_radius))
    shadow.setOffset(0.0, float(y_offset))
    shadow.setColor(QColor(15, 23, 42, 34))
    widget.setGraphicsEffect(shadow)


DESIGN_SYSTEM_STYLESHEET = f"""
QMainWindow,
QWidget#mainShell,
QWidget#mainContent,
QStackedWidget#mainPageStack {{
    background: {TOKENS.canvas};
}}

QWidget {{
    color: {TOKENS.text};
    font-family: "Segoe UI Variable", "Segoe UI", "Inter", sans-serif;
    font-size: 14px;
}}

QLabel#pageTitle {{
    color: {TOKENS.text};
    font-size: 30px;
    font-weight: 750;
}}

QLabel#pageSubtitle {{
    color: {TOKENS.text_muted};
    font-size: 14px;
}}

QWidget#navigationSidebar,
QWidget#navigationContainer,
QScrollArea#navigationScroll {{
    background: {TOKENS.sidebar};
    border: none;
}}

QWidget#navigationTopBar {{
    background: transparent;
}}

QLabel#navigationMonogram {{
    color: #FFFFFF;
    background: #243447;
    border: 1px solid #35506A;
    border-radius: 10px;
    min-width: 38px;
    min-height: 38px;
    max-width: 38px;
    max-height: 38px;
    font-size: 14px;
    font-weight: 800;
    qproperty-alignment: AlignCenter;
}}

QToolButton#navigationCollapseButton {{
    color: #DCE7F1;
    background: transparent;
    border: 1px solid transparent;
    border-radius: 8px;
    min-width: 34px;
    min-height: 34px;
}}

QToolButton#navigationCollapseButton:hover {{
    background: {TOKENS.sidebar_hover};
    border-color: #31465A;
}}

QPushButton#navigationButton {{
    min-height: 42px;
    padding: 8px 12px;
    border-radius: 10px;
    font-size: 14px;
}}

QWidget#navigationSidebar[collapsed="true"] QPushButton#navigationButton {{
    padding: 8px;
}}

QScrollArea#dashboardScroll,
QWidget#dashboardBody,
QWidget#homeDashboardPage {{
    background: transparent;
    border: none;
}}

QFrame#dashboardHero,
QFrame#dashboardMetricCard,
QFrame#courseCard[dashboardCard="true"],
QFrame#academicCard,
QFrame#emptyStateCard {{
    background: {TOKENS.surface};
    border: 1px solid {TOKENS.border};
    border-radius: {TOKENS.radius_large}px;
}}

QFrame#dashboardHero {{
    background: #F1F6FF;
    border-color: #C8D8F2;
}}

QLabel#dashboardEyebrow {{
    color: {TOKENS.primary};
    font-size: 12px;
    font-weight: 800;
    letter-spacing: 1px;
}}

QLabel#dashboardHeroTitle {{
    color: {TOKENS.text};
    font-size: 25px;
    font-weight: 780;
}}

QLabel[dashboardRole="heroBody"],
QLabel#dashboardMetricCaption,
QLabel#courseCardMetadata,
QLabel#courseCardSummary,
QLabel#dashboardCourseStatus {{
    color: {TOKENS.text_muted};
}}

QLabel#dashboardMetricValue {{
    color: {TOKENS.text};
    font-size: 27px;
    font-weight: 800;
}}

QLabel#dashboardMetricTitle {{
    color: {TOKENS.text};
    font-size: 14px;
    font-weight: 700;
}}

QLabel#courseCardCode {{
    color: {TOKENS.primary};
    font-size: 13px;
    font-weight: 800;
}}

QLabel#courseCardTitle {{
    color: {TOKENS.text};
    font-size: 18px;
    font-weight: 760;
}}

QFrame#courseCard[dashboardCard="true"]:hover {{
    border-color: {TOKENS.primary};
}}

QFrame#courseCard[courseCode="DM857"] {{
    border-top: 4px solid {COURSE_ACCENTS["DM857"]};
}}

QFrame#courseCard[courseCode="DM847"] {{
    border-top: 4px solid {COURSE_ACCENTS["DM847"]};
}}

QFrame#courseCard[courseCode="BMB830"] {{
    border-top: 4px solid {COURSE_ACCENTS["BMB830"]};
}}

QFrame#courseCard[courseCode="BMB831"] {{
    border-top: 4px solid {COURSE_ACCENTS["BMB831"]};
}}

QProgressBar#dashboardCourseProgress {{
    min-height: 9px;
    max-height: 9px;
    border: none;
    border-radius: 4px;
    background: #E7EDF4;
    text-align: center;
    color: transparent;
}}

QProgressBar#dashboardCourseProgress::chunk {{
    border-radius: 4px;
    background: {TOKENS.primary};
}}

QProgressBar#dashboardCourseProgress[courseCode="DM857"]::chunk {{
    background: {COURSE_ACCENTS["DM857"]};
}}

QProgressBar#dashboardCourseProgress[courseCode="DM847"]::chunk {{
    background: {COURSE_ACCENTS["DM847"]};
}}

QProgressBar#dashboardCourseProgress[courseCode="BMB830"]::chunk {{
    background: {COURSE_ACCENTS["BMB830"]};
}}

QProgressBar#dashboardCourseProgress[courseCode="BMB831"]::chunk {{
    background: {COURSE_ACCENTS["BMB831"]};
}}

QPushButton#dashboardPrimaryAction,
QPushButton#dashboardReviewAction {{
    min-height: 38px;
    padding: 0 16px;
    border: none;
    border-radius: 10px;
    color: #FFFFFF;
    background: {TOKENS.primary};
    font-weight: 700;
}}

QPushButton#dashboardPrimaryAction:hover,
QPushButton#dashboardReviewAction:hover {{
    background: {TOKENS.primary_hover};
}}

QPushButton#courseOpenButton[dashboardVariant="secondary"],
QPushButton#dashboardSecondaryAction {{
    min-height: 38px;
    padding: 0 16px;
    border: 1px solid {TOKENS.border_strong};
    border-radius: 10px;
    color: #294A70;
    background: {TOKENS.surface};
    font-weight: 700;
}}

QPushButton#courseOpenButton[dashboardVariant="secondary"]:hover,
QPushButton#dashboardSecondaryAction:hover {{
    background: {TOKENS.primary_soft};
    border-color: #8BADE0;
}}

QLabel[dashboardRole="sectionTitle"] {{
    color: {TOKENS.text};
    font-size: 19px;
    font-weight: 780;
}}

QLabel#statusSuccess {{
    color: {TOKENS.success};
    font-weight: 700;
}}

QLabel#statusWarning {{
    color: {TOKENS.warning};
    font-weight: 700;
}}

QLabel#statusDanger {{
    color: {TOKENS.danger};
    font-weight: 700;
}}

QToolTip {{
    color: {TOKENS.text};
    background: #FFFFFF;
    border: 1px solid {TOKENS.border_strong};
    padding: 6px 8px;
}}
"""


__all__ = [
    "COURSE_ACCENTS",
    "DESIGN_SYSTEM_STYLESHEET",
    "DesignTokens",
    "TOKENS",
    "apply_elevation",
]
