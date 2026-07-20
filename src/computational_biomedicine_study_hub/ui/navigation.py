"""Responsive sidebar navigation for the application shell."""

from __future__ import annotations

from collections.abc import Iterable
from dataclasses import dataclass

from PySide6.QtCore import (
    QEasingCurve,
    QParallelAnimationGroup,
    QPropertyAnimation,
    QSize,
    Qt,
    Signal,
)
from PySide6.QtWidgets import (
    QButtonGroup,
    QFrame,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QScrollArea,
    QSizePolicy,
    QStyle,
    QToolButton,
    QVBoxLayout,
    QWidget,
)

from ..courses.models import CourseRegistration
from ..i18n import AppLocale, MessageKey, Translator
from .routes import RouteId, RouteLike, route_value


@dataclass(frozen=True, slots=True)
class NavigationEntry:
    """One visible item in the sidebar."""

    route: str
    label: str
    section: str
    icon: QStyle.StandardPixmap


def build_navigation(
    courses: Iterable[CourseRegistration],
    translator: Translator | None = None,
) -> tuple[NavigationEntry, ...]:
    """Build localized navigation without hard-coding future semesters."""

    active_translator = translator or Translator()
    entries: list[NavigationEntry] = [
        NavigationEntry(
            RouteId.HOME.value,
            active_translator.text(MessageKey.NAV_HOME),
            active_translator.text(MessageKey.NAV_GENERAL),
            QStyle.StandardPixmap.SP_ComputerIcon,
        )
    ]

    semester_ordered_courses = sorted(courses, key=lambda course: course.semester)
    for course in semester_ordered_courses:
        entries.append(
            NavigationEntry(
                course.route,
                course.navigation_label_for(active_translator.locale),
                active_translator.text(MessageKey.NAV_SEMESTER, semester=course.semester),
                QStyle.StandardPixmap.SP_DirIcon,
            )
        )

    learning = active_translator.text(MessageKey.NAV_LEARNING)
    entries.extend(
        [
            NavigationEntry(
                RouteId.REVIEW.value,
                active_translator.text(MessageKey.NAV_REVIEW),
                learning,
                QStyle.StandardPixmap.SP_BrowserReload,
            ),
            NavigationEntry(
                RouteId.ASSESSMENTS.value,
                active_translator.text(MessageKey.NAV_ASSESSMENTS),
                learning,
                QStyle.StandardPixmap.SP_DialogApplyButton,
            ),
            NavigationEntry(
                RouteId.FLASHCARDS.value,
                active_translator.text(MessageKey.NAV_FLASHCARDS),
                learning,
                QStyle.StandardPixmap.SP_FileDialogDetailedView,
            ),
            NavigationEntry(
                RouteId.STUDY_LAB.value,
                active_translator.text(MessageKey.NAV_STUDY_LAB),
                learning,
                QStyle.StandardPixmap.SP_DesktopIcon,
            ),
            NavigationEntry(
                RouteId.GLOSSARY.value,
                active_translator.text(MessageKey.NAV_GLOSSARY),
                active_translator.text(MessageKey.NAV_RESOURCES),
                QStyle.StandardPixmap.SP_FileIcon,
            ),
            NavigationEntry(
                RouteId.SETTINGS.value,
                active_translator.text(MessageKey.NAV_SETTINGS),
                active_translator.text(MessageKey.NAV_SYSTEM),
                QStyle.StandardPixmap.SP_FileDialogContentsView,
            ),
        ]
    )
    return tuple(entries)


def _collapse_copy(locale: AppLocale, *, collapsed: bool) -> str:
    translations = {
        AppLocale.SPANISH_SPAIN: ("Contraer navegación", "Expandir navegación"),
        AppLocale.ENGLISH: ("Collapse navigation", "Expand navigation"),
        AppLocale.DANISH_DENMARK: ("Skjul navigation", "Udvid navigation"),
    }
    expanded_text, collapsed_text = translations[locale]
    return collapsed_text if collapsed else expanded_text


class NavigationSidebar(QWidget):
    """Render grouped navigation entries with an animated compact state."""

    route_selected = Signal(str)
    collapsed_changed = Signal(bool)

    def __init__(
        self,
        courses: Iterable[CourseRegistration],
        translator: Translator | None = None,
        parent: QWidget | None = None,
        *,
        collapsed: bool = False,
    ) -> None:
        super().__init__(parent)
        self.setObjectName("navigationSidebar")
        self.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Expanding)

        self._expanded_width = 300
        self._collapsed_width = 76
        self._collapsed = False
        self._courses = tuple(courses)
        self._translator = translator or Translator()
        self._buttons: dict[str, QPushButton] = {}
        self._section_labels: list[QLabel] = []
        self._button_group = QButtonGroup(self)
        self._button_group.setExclusive(True)
        self._width_animation: QParallelAnimationGroup | None = None

        root_layout = QVBoxLayout(self)
        root_layout.setContentsMargins(12, 14, 12, 14)
        root_layout.setSpacing(8)

        top_bar = QWidget()
        top_bar.setObjectName("navigationTopBar")
        top_layout = QHBoxLayout(top_bar)
        top_layout.setContentsMargins(4, 0, 2, 4)
        top_layout.setSpacing(9)

        self._monogram = QLabel("CB")
        self._monogram.setObjectName("navigationMonogram")
        self._monogram.setToolTip("Computational Biomedicine Hub")
        top_layout.addWidget(self._monogram)

        self._product_name = QLabel()
        self._product_name.setObjectName("productName")
        self._product_name.setWordWrap(True)
        top_layout.addWidget(self._product_name, 1)

        self._collapse_button = QToolButton()
        self._collapse_button.setObjectName("navigationCollapseButton")
        self._collapse_button.setIconSize(QSize(18, 18))
        self._collapse_button.clicked.connect(self._toggle_collapsed)
        top_layout.addWidget(self._collapse_button)
        root_layout.addWidget(top_bar)

        scroll = QScrollArea()
        scroll.setObjectName("navigationScroll")
        scroll.setWidgetResizable(True)
        scroll.setFrameShape(QFrame.Shape.NoFrame)
        scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)

        self._container = QWidget()
        self._container.setObjectName("navigationContainer")
        self._layout = QVBoxLayout(self._container)
        self._layout.setContentsMargins(0, 0, 0, 0)
        self._layout.setSpacing(6)
        scroll.setWidget(self._container)
        root_layout.addWidget(scroll, 1)

        self.setMinimumWidth(self._expanded_width)
        self.setMaximumWidth(self._expanded_width)
        self.retranslate(self._translator)
        if collapsed:
            self.set_collapsed(True, animate=False)
        else:
            self._apply_collapsed_visuals()

    @property
    def is_collapsed(self) -> bool:
        """Return whether only navigation icons are currently visible."""

        return self._collapsed

    def retranslate(self, translator: Translator) -> None:
        """Rebuild visible labels while preserving stable routes and compact state."""

        self._translator = translator
        active_route = next(
            (route for route, button in self._buttons.items() if button.isChecked()),
            RouteId.HOME.value,
        )
        self._clear_entries()
        self._product_name.setText(translator.text(MessageKey.PRODUCT_NAME))
        self._button_group = QButtonGroup(self)
        self._button_group.setExclusive(True)

        current_section = ""
        for entry in build_navigation(self._courses, translator):
            if entry.section != current_section:
                current_section = entry.section
                section_label = QLabel(current_section)
                section_label.setObjectName("navigationSection")
                self._section_labels.append(section_label)
                self._layout.addWidget(section_label)

            button = QPushButton(entry.label)
            button.setObjectName("navigationButton")
            button.setCheckable(True)
            button.setIcon(self.style().standardIcon(entry.icon))
            button.setIconSize(QSize(20, 20))
            button.setToolTip(entry.label)
            button.setAccessibleName(entry.label)
            button.setProperty("expandedText", entry.label)
            button.clicked.connect(
                lambda checked=False, route=entry.route: self.route_selected.emit(route)
            )
            self._button_group.addButton(button)
            self._buttons[entry.route] = button
            self._layout.addWidget(button)

        self._layout.addStretch(1)
        self.set_active_route(active_route)
        self._apply_collapsed_visuals()

    def set_active_route(self, route: RouteLike) -> None:
        """Reflect the current route in the sidebar selection."""

        button = self._buttons.get(route_value(route))
        if button is not None:
            button.setChecked(True)

    def set_collapsed(self, collapsed: bool, *, animate: bool = True) -> None:
        """Switch between expanded labels and a compact icon-only navigation rail."""

        if collapsed == self._collapsed:
            self._apply_collapsed_visuals()
            return

        self._collapsed = collapsed
        self._apply_collapsed_visuals()
        target_width = self._collapsed_width if collapsed else self._expanded_width

        if not animate:
            self.setMinimumWidth(target_width)
            self.setMaximumWidth(target_width)
        else:
            current_width = self.width()
            group = QParallelAnimationGroup(self)
            for property_name in (b"minimumWidth", b"maximumWidth"):
                animation = QPropertyAnimation(self, property_name, group)
                animation.setStartValue(current_width)
                animation.setEndValue(target_width)
                animation.setDuration(180)
                animation.setEasingCurve(QEasingCurve.Type.OutCubic)
                group.addAnimation(animation)
            self._width_animation = group
            group.start()

        self.collapsed_changed.emit(collapsed)

    def _toggle_collapsed(self) -> None:
        self.set_collapsed(not self._collapsed)

    def _apply_collapsed_visuals(self) -> None:
        self.setProperty("collapsed", "true" if self._collapsed else "false")
        self.style().unpolish(self)
        self.style().polish(self)

        self._product_name.setVisible(not self._collapsed)
        for label in self._section_labels:
            label.setVisible(not self._collapsed)
        for button in self._buttons.values():
            expanded_text = str(button.property("expandedText") or "")
            button.setText("" if self._collapsed else expanded_text)

        arrow = (
            QStyle.StandardPixmap.SP_ArrowRight
            if self._collapsed
            else QStyle.StandardPixmap.SP_ArrowLeft
        )
        self._collapse_button.setIcon(self.style().standardIcon(arrow))
        tooltip = _collapse_copy(self._translator.locale, collapsed=self._collapsed)
        self._collapse_button.setToolTip(tooltip)
        self._collapse_button.setAccessibleName(tooltip)

    def _clear_entries(self) -> None:
        self._buttons.clear()
        self._section_labels.clear()
        while self._layout.count():
            item = self._layout.takeAt(0)
            if item is None:
                break
            widget = item.widget()
            if widget is not None:
                widget.setParent(None)
                widget.deleteLater()
        self._button_group.deleteLater()
