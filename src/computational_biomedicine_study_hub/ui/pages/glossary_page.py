"""Searchable learner-facing cross-course glossary."""

from __future__ import annotations

import logging
from collections.abc import Iterable

from PySide6.QtCore import Qt, Signal, Slot
from PySide6.QtWidgets import (
    QCheckBox,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QListWidget,
    QListWidgetItem,
    QMenu,
    QPushButton,
    QSplitter,
    QToolButton,
    QVBoxLayout,
    QWidget,
    QWidgetAction,
)

from ...courses import COURSES
from ...i18n import DEFAULT_LOCALE, AppLocale
from ...learning.academic_catalog import AcademicCatalog, GlossaryEntry
from ...learning.progress import LearningItemKind
from ...learning.progress_repository import ProgressRepository
from ..learning_page_copy import LearningPageCopyKey, learning_text
from ..study_state import StudyLocation

LOGGER = logging.getLogger(__name__)


class CourseMultiSelector(QToolButton):
    """Compact checked menu with stable course-code values."""

    selection_changed = Signal()

    def __init__(
        self,
        course_codes: Iterable[str],
        *,
        locale: AppLocale,
        parent: QWidget | None = None,
    ) -> None:
        super().__init__(parent)
        self.setObjectName("glossaryCourseSelector")
        self.setPopupMode(QToolButton.ToolButtonPopupMode.InstantPopup)
        self._locale = locale
        self._course_codes = tuple(course_codes)
        self._titles = {
            course.code: course.title_for(locale)
            for course in COURSES
            if course.code in self._course_codes
        }
        menu = QMenu(self)
        menu.setObjectName("glossaryCourseMenu")
        self.setMenu(menu)

        self._all_checkbox = self._checkbox(
            learning_text(locale, LearningPageCopyKey.ALL_COURSES),
            "glossaryCourseOption_all",
        )
        self._all_checkbox.setChecked(True)
        self._all_checkbox.toggled.connect(self._all_toggled)
        self._checkboxes: dict[str, QCheckBox] = {}
        for course_code in self._course_codes:
            checkbox = self._checkbox(
                self._titles.get(course_code, course_code),
                f"glossaryCourseOption_{course_code}",
            )
            checkbox.setProperty("courseCode", course_code)
            checkbox.setChecked(True)
            checkbox.toggled.connect(self._course_toggled)
            self._checkboxes[course_code] = checkbox
        self._update_text()

    @property
    def selected_course_codes(self) -> tuple[str, ...]:
        return tuple(
            course_code
            for course_code in self._course_codes
            if self._checkboxes[course_code].isChecked()
        )

    def set_selected_course_codes(self, course_codes: Iterable[str]) -> None:
        selected = set(course_codes) & set(self._course_codes)
        for checkbox in (self._all_checkbox, *self._checkboxes.values()):
            checkbox.blockSignals(True)
        for course_code, checkbox in self._checkboxes.items():
            checkbox.setChecked(course_code in selected)
        self._all_checkbox.setChecked(
            bool(self._course_codes) and len(selected) == len(self._course_codes)
        )
        for checkbox in (self._all_checkbox, *self._checkboxes.values()):
            checkbox.blockSignals(False)
        self._update_text()
        self.selection_changed.emit()

    @Slot(bool)
    def _all_toggled(self, checked: bool) -> None:
        for checkbox in self._checkboxes.values():
            checkbox.blockSignals(True)
            checkbox.setChecked(checked)
            checkbox.blockSignals(False)
        self._update_text()
        self.selection_changed.emit()

    @Slot()
    def _course_toggled(self) -> None:
        all_selected = bool(self._course_codes) and all(
            checkbox.isChecked() for checkbox in self._checkboxes.values()
        )
        self._all_checkbox.blockSignals(True)
        self._all_checkbox.setChecked(all_selected)
        self._all_checkbox.blockSignals(False)
        self._update_text()
        self.selection_changed.emit()

    def _update_text(self) -> None:
        selected = self.selected_course_codes
        if selected and len(selected) == len(self._course_codes):
            text = learning_text(self._locale, LearningPageCopyKey.ALL_COURSES)
        elif len(selected) == 1:
            text = self._titles.get(selected[0], selected[0])
        else:
            text = _copy(
                self._locale,
                f"{len(selected)} asignaturas seleccionadas",
                f"{len(selected)} courses selected",
                f"{len(selected)} kurser valgt",
            )
        self.setText(text)
        self.setAccessibleName(text)
        self.setToolTip(
            "\n".join(self._titles.get(code, code) for code in selected)
            or _copy(
                self._locale,
                "Ninguna asignatura seleccionada",
                "No courses selected",
                "Ingen kurser valgt",
            )
        )

    def _checkbox(self, text: str, object_name: str) -> QCheckBox:
        checkbox = QCheckBox(text)
        checkbox.setObjectName(object_name)
        checkbox.setMinimumHeight(32)
        action = QWidgetAction(self)
        action.setDefaultWidget(checkbox)
        menu = self.menu()
        assert menu is not None
        menu.addAction(action)
        return checkbox


class GlossaryPage(QWidget):
    """Aggregate valid authored terms while keeping technical IDs internal."""

    module_requested = Signal(str, str)
    flashcards_requested = Signal(str, str)
    assessments_requested = Signal(str, str)

    def __init__(
        self,
        catalog: AcademicCatalog,
        *,
        locale: AppLocale = DEFAULT_LOCALE,
        repository: ProgressRepository | None = None,
        parent: QWidget | None = None,
    ) -> None:
        super().__init__(parent)
        self.setObjectName("glossaryPage")
        self._catalog = catalog
        self._locale = locale
        self._repository = repository
        self._entries: tuple[GlossaryEntry, ...] = ()
        self._selected: GlossaryEntry | None = None
        self._all_entries = self._validated_entries(catalog.glossary())

        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(12)
        filters = QHBoxLayout()
        self.search = QLineEdit()
        self.search.setObjectName("glossarySearch")
        self.search.setPlaceholderText(learning_text(locale, LearningPageCopyKey.SEARCH))
        self.search.setAccessibleName(self.search.placeholderText())
        self.course_selector = CourseMultiSelector(catalog.course_codes, locale=locale)
        filters.addWidget(self.search, 1)
        filters.addWidget(self.course_selector)
        layout.addLayout(filters)

        splitter = QSplitter()
        splitter.setObjectName("glossarySplitter")
        self.term_list = QListWidget()
        self.term_list.setObjectName("glossaryTermList")
        self.term_list.setAccessibleName(
            _copy(locale, "Términos del glosario", "Glossary terms", "Ordlistebegreber")
        )
        splitter.addWidget(self.term_list)

        detail = QWidget()
        detail.setObjectName("glossaryDetailPanel")
        detail_layout = QVBoxLayout(detail)
        self.detail_empty_label = QLabel(
            _copy(
                locale,
                "Selecciona un término para ver su definición.",
                "Select a term to view its definition.",
                "Vælg et begreb for at se definitionen.",
            )
        )
        self.detail_empty_label.setObjectName("glossaryDetailEmptyState")
        self.detail_empty_label.setWordWrap(True)
        detail_layout.addWidget(self.detail_empty_label)

        self.detail_content = QWidget()
        self.detail_content.setObjectName("glossaryDetailContent")
        content_layout = QVBoxLayout(self.detail_content)
        content_layout.setContentsMargins(0, 0, 0, 0)
        self.term_label = QLabel()
        self.term_label.setObjectName("glossaryTerm")
        self.term_label.setWordWrap(True)
        content_layout.addWidget(self.term_label)
        content_layout.addWidget(self._heading(LearningPageCopyKey.DEFINITION))
        self.definition_label = QLabel()
        self.definition_label.setObjectName("glossaryDefinition")
        self.definition_label.setWordWrap(True)
        self.definition_label.setTextInteractionFlags(Qt.TextInteractionFlag.TextSelectableByMouse)
        content_layout.addWidget(self.definition_label)
        content_layout.addWidget(self._heading(LearningPageCopyKey.SOURCE))
        self.source_label = QLabel()
        self.source_label.setObjectName("glossarySource")
        self.source_label.setWordWrap(True)
        content_layout.addWidget(self.source_label)
        content_layout.addWidget(self._heading(LearningPageCopyKey.RELATED))
        self.related_label = QLabel()
        self.related_label.setObjectName("glossaryRelatedTerms")
        self.related_label.setWordWrap(True)
        content_layout.addWidget(self.related_label)
        content_layout.addWidget(self._heading(LearningPageCopyKey.SYNONYMS))
        self.synonyms_label = QLabel()
        self.synonyms_label.setObjectName("glossarySynonyms")
        self.synonyms_label.setWordWrap(True)
        content_layout.addWidget(self.synonyms_label)
        self.open_button = QPushButton(learning_text(locale, LearningPageCopyKey.OPEN_MODULE))
        self.open_button.setObjectName("openGlossarySourceButton")
        self.open_button.clicked.connect(self.open_source_module)
        content_layout.addWidget(self.open_button)
        actions = QHBoxLayout()
        self.favorite_button = QPushButton()
        self.favorite_button.setObjectName("favoriteGlossaryTermButton")
        self.favorite_button.clicked.connect(self.toggle_favorite)
        self.cards_button = QPushButton(
            _copy(
                locale,
                "Abrir tarjetas relacionadas",
                "Open related cards",
                "Åbn relaterede kort",
            )
        )
        self.cards_button.setObjectName("openGlossaryCardsButton")
        self.cards_button.clicked.connect(self.open_related_cards)
        self.questions_button = QPushButton(
            _copy(
                locale,
                "Abrir preguntas relacionadas",
                "Open related questions",
                "Åbn relaterede spørgsmål",
            )
        )
        self.questions_button.setObjectName("openGlossaryQuestionsButton")
        self.questions_button.clicked.connect(self.open_related_questions)
        for button in (self.favorite_button, self.cards_button, self.questions_button):
            actions.addWidget(button)
        content_layout.addLayout(actions)
        content_layout.addStretch(1)
        detail_layout.addWidget(self.detail_content, 1)
        splitter.addWidget(detail)
        splitter.setSizes([360, 640])
        layout.addWidget(splitter, 1)

        self.empty_label = QLabel(learning_text(locale, LearningPageCopyKey.GLOSSARY_EMPTY))
        self.empty_label.setObjectName("glossaryEmptyState")
        self.empty_label.setWordWrap(True)
        layout.addWidget(self.empty_label)

        self.search.textChanged.connect(self.refresh)
        self.course_selector.selection_changed.connect(self.refresh)
        self.term_list.currentRowChanged.connect(self._show_entry)
        self.refresh()

    @property
    def entries(self) -> tuple[GlossaryEntry, ...]:
        return self._entries

    @property
    def selected_entry(self) -> GlossaryEntry | None:
        return self._selected

    @Slot()
    def refresh(self) -> None:
        selected_id = self._selected.term_id if self._selected is not None else ""
        selected_courses = set(self.course_selector.selected_course_codes)
        query = " ".join(self.search.text().casefold().split())
        entries = tuple(
            entry
            for entry in self._all_entries
            if entry.course_code in selected_courses
            and (
                not query
                or query
                in " ".join(
                    (
                        entry.term,
                        entry.definition,
                        *entry.tags,
                        *entry.synonyms,
                        *entry.related_terms,
                    )
                ).casefold()
            )
        )
        self._entries = tuple(sorted(entries, key=lambda entry: entry.term.casefold()))
        self.term_list.blockSignals(True)
        self.term_list.clear()
        selected_row = -1
        for index, entry in enumerate(self._entries):
            row = QListWidgetItem(entry.term)
            row.setData(Qt.ItemDataRole.UserRole, entry.term_id)
            row.setToolTip(entry.term)
            self.term_list.addItem(row)
            if entry.term_id == selected_id:
                selected_row = index
        self.term_list.blockSignals(False)
        self.empty_label.setVisible(not self._entries)
        if selected_row >= 0:
            self.term_list.setCurrentRow(selected_row)
            self._show_entry(selected_row)
        elif self._entries and not selected_id:
            self.term_list.setCurrentRow(0)
            self._show_entry(0)
        else:
            self.term_list.setCurrentRow(-1)
            self.term_list.clearSelection()
            self._show_entry(-1)

    @Slot(int)
    def _show_entry(self, row: int) -> None:
        if not 0 <= row < len(self._entries):
            self._selected = None
            self.detail_content.hide()
            self.detail_empty_label.show()
            return
        entry = self._entries[row]
        self._selected = entry
        self.term_label.setText(entry.term)
        self.definition_label.setText(entry.definition)
        self.source_label.setText(f"{self._course_title(entry.course_code)}\n{entry.module_title}")
        self.related_label.setText(" · ".join(entry.related_terms) or "—")
        self.synonyms_label.setText(" · ".join(entry.synonyms) or "—")
        self.open_button.setEnabled(True)
        self.cards_button.setEnabled(True)
        self.questions_button.setEnabled(True)
        self.favorite_button.setEnabled(self._repository is not None)
        self._update_favorite_button()
        self.detail_empty_label.hide()
        self.detail_content.show()

    def capture_state(self) -> StudyLocation:
        return StudyLocation(
            route="glossary",
            course_code="",
            module_id=self._selected.module_id if self._selected else "",
            activity_id=self._selected.term_id if self._selected else "",
            filters={
                "courses": ",".join(self.course_selector.selected_course_codes),
                "query": self.search.text(),
            },
        )

    def restore_state(self, state: StudyLocation) -> None:
        selected_courses = tuple(
            value for value in state.filters.get("courses", "").split(",") if value
        )
        if selected_courses:
            self.course_selector.set_selected_course_codes(selected_courses)
        self.search.setText(state.filters.get("query", ""))
        if state.activity_id:
            row = next(
                (
                    index
                    for index, entry in enumerate(self._entries)
                    if entry.term_id == state.activity_id
                ),
                -1,
            )
            if row >= 0:
                self.term_list.setCurrentRow(row)
                self._show_entry(row)

    @Slot()
    def open_source_module(self) -> None:
        if self._selected is not None:
            self.module_requested.emit(
                self._selected.course_code,
                self._selected.module_id,
            )

    @Slot()
    def toggle_favorite(self) -> None:
        if self._selected is None or self._repository is None:
            return
        bookmarked = self._repository.is_bookmarked(
            item_id=self._selected.term_id,
            item_kind=LearningItemKind.CONCEPT.value,
        )
        self._repository.set_bookmark(
            item_id=self._selected.term_id,
            item_kind=LearningItemKind.CONCEPT.value,
            course_code=self._selected.course_code,
            module_id=self._selected.module_id,
            bookmarked=not bookmarked,
        )
        self._update_favorite_button()

    @Slot()
    def open_related_cards(self) -> None:
        if self._selected is not None:
            self.flashcards_requested.emit(
                self._selected.course_code,
                self._selected.module_id,
            )

    @Slot()
    def open_related_questions(self) -> None:
        if self._selected is not None:
            self.assessments_requested.emit(
                self._selected.course_code,
                self._selected.module_id,
            )

    def _update_favorite_button(self) -> None:
        favorite = (
            self._selected is not None
            and self._repository is not None
            and self._repository.is_bookmarked(
                item_id=self._selected.term_id,
                item_kind=LearningItemKind.CONCEPT.value,
            )
        )
        self.favorite_button.setText(
            ("★ " if favorite else "☆ ") + _copy(self._locale, "Favorito", "Favorite", "Favorit")
        )

    def _course_title(self, course_code: str) -> str:
        course = next((item for item in COURSES if item.code == course_code), None)
        return course.title_for(self._locale) if course is not None else course_code

    def _heading(self, key: LearningPageCopyKey) -> QLabel:
        label = QLabel(learning_text(self._locale, key))
        label.setObjectName("contentSubheading")
        return label

    @staticmethod
    def _validated_entries(
        entries: Iterable[GlossaryEntry],
    ) -> tuple[GlossaryEntry, ...]:
        valid: list[GlossaryEntry] = []
        for entry in entries:
            if entry.term.strip() and entry.definition.strip():
                valid.append(entry)
                continue
            LOGGER.warning(
                "Discarded incomplete glossary entry course=%s module=%s id=%s",
                entry.course_code,
                entry.module_id,
                entry.term_id,
            )
        return tuple(valid)


def _copy(locale: AppLocale, es: str, en: str, da: str) -> str:
    return {
        AppLocale.SPANISH_SPAIN: es,
        AppLocale.ENGLISH: en,
        AppLocale.DANISH_DENMARK: da,
    }[locale]


__all__ = ["CourseMultiSelector", "GlossaryPage"]
