"""Searchable model-backed cross-course glossary."""

from __future__ import annotations

from PySide6.QtCore import Qt, Signal, Slot
from PySide6.QtWidgets import (
    QComboBox,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QListWidget,
    QListWidgetItem,
    QPushButton,
    QSplitter,
    QVBoxLayout,
    QWidget,
)

from ...i18n import DEFAULT_LOCALE, AppLocale
from ...learning.academic_catalog import AcademicCatalog, GlossaryEntry
from ...learning.progress import LearningItemKind
from ...learning.progress_repository import ProgressRepository
from ..learning_page_copy import LearningPageCopyKey, learning_text


class GlossaryPage(QWidget):
    """Aggregate terms directly from academic concept models."""

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

        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        filters = QHBoxLayout()
        self.search = QLineEdit()
        self.search.setObjectName("glossarySearch")
        self.search.setPlaceholderText(learning_text(locale, LearningPageCopyKey.SEARCH))
        self.search.setAccessibleName(self.search.placeholderText())
        self.course_selector = QComboBox()
        self.course_selector.setObjectName("glossaryCourseSelector")
        self.course_selector.addItem(
            learning_text(locale, LearningPageCopyKey.ALL_COURSES),
            None,
        )
        for course_code in catalog.course_codes:
            self.course_selector.addItem(course_code, course_code)
        filters.addWidget(self.search, 1)
        filters.addWidget(self.course_selector)
        layout.addLayout(filters)

        splitter = QSplitter()
        splitter.setObjectName("glossarySplitter")
        self.term_list = QListWidget()
        self.term_list.setObjectName("glossaryTermList")
        self.term_list.setAccessibleName("Glossary terms")
        splitter.addWidget(self.term_list)

        detail = QWidget()
        detail_layout = QVBoxLayout(detail)
        self.term_label = QLabel()
        self.term_label.setObjectName("glossaryTerm")
        self.term_label.setWordWrap(True)
        detail_layout.addWidget(self.term_label)
        detail_layout.addWidget(self._heading(LearningPageCopyKey.DEFINITION))
        self.definition_label = QLabel()
        self.definition_label.setObjectName("glossaryDefinition")
        self.definition_label.setWordWrap(True)
        self.definition_label.setTextInteractionFlags(Qt.TextInteractionFlag.TextSelectableByMouse)
        detail_layout.addWidget(self.definition_label)
        detail_layout.addWidget(self._heading(LearningPageCopyKey.SOURCE))
        self.source_label = QLabel()
        self.source_label.setObjectName("glossarySource")
        self.source_label.setWordWrap(True)
        detail_layout.addWidget(self.source_label)
        detail_layout.addWidget(self._heading(LearningPageCopyKey.RELATED))
        self.related_label = QLabel()
        self.related_label.setObjectName("glossaryRelatedTerms")
        self.related_label.setWordWrap(True)
        detail_layout.addWidget(self.related_label)
        detail_layout.addWidget(self._heading(LearningPageCopyKey.SYNONYMS))
        self.synonyms_label = QLabel()
        self.synonyms_label.setObjectName("glossarySynonyms")
        self.synonyms_label.setWordWrap(True)
        detail_layout.addWidget(self.synonyms_label)
        self.open_button = QPushButton(learning_text(locale, LearningPageCopyKey.OPEN_MODULE))
        self.open_button.setObjectName("openGlossarySourceButton")
        self.open_button.clicked.connect(self.open_source_module)
        detail_layout.addWidget(self.open_button)
        actions = QHBoxLayout()
        self.favorite_button = QPushButton()
        self.favorite_button.setObjectName("favoriteGlossaryTermButton")
        self.favorite_button.clicked.connect(self.toggle_favorite)
        self.cards_button = QPushButton(
            _copy(
                locale, "Abrir tarjetas relacionadas", "Open related cards", "Åbn relaterede kort"
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
        detail_layout.addLayout(actions)
        detail_layout.addStretch(1)
        splitter.addWidget(detail)
        splitter.setSizes([320, 640])
        layout.addWidget(splitter, 1)

        self.empty_label = QLabel(learning_text(locale, LearningPageCopyKey.GLOSSARY_EMPTY))
        self.empty_label.setObjectName("glossaryEmptyState")
        self.empty_label.setWordWrap(True)
        layout.addWidget(self.empty_label)

        self.search.textChanged.connect(self.refresh)
        self.course_selector.currentIndexChanged.connect(self.refresh)
        self.term_list.currentRowChanged.connect(self._show_entry)
        self.refresh()

    @property
    def entries(self) -> tuple[GlossaryEntry, ...]:
        return self._entries

    @Slot()
    def refresh(self) -> None:
        course_value = self.course_selector.currentData()
        course_code = course_value if isinstance(course_value, str) else None
        query = " ".join(self.search.text().casefold().split())
        entries = self._catalog.glossary(course_code=course_code)
        if query:
            entries = tuple(
                entry
                for entry in entries
                if query
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
        self._entries = tuple(sorted(entries, key=lambda entry: entry.term.casefold()))
        self.term_list.blockSignals(True)
        self.term_list.clear()
        for index, entry in enumerate(self._entries):
            row = QListWidgetItem(f"{entry.term}  ·  {entry.course_code}")
            row.setData(Qt.ItemDataRole.UserRole, index)
            self.term_list.addItem(row)
        self.term_list.blockSignals(False)
        self.empty_label.setVisible(not self._entries)
        if self._entries:
            self.term_list.setCurrentRow(0)
            self._show_entry(0)
        else:
            self._show_entry(-1)

    @Slot(int)
    def _show_entry(self, row: int) -> None:
        if not 0 <= row < len(self._entries):
            self._selected = None
            for label in (
                self.term_label,
                self.definition_label,
                self.source_label,
                self.related_label,
                self.synonyms_label,
            ):
                label.clear()
            self.open_button.setEnabled(False)
            for button in (self.favorite_button, self.cards_button, self.questions_button):
                button.setEnabled(False)
            return
        entry = self._entries[row]
        self._selected = entry
        self.term_label.setText(entry.term)
        self.definition_label.setText(entry.definition)
        self.source_label.setText(f"{entry.course_code} · {entry.module_title} · {entry.module_id}")
        self.related_label.setText(" · ".join(entry.related_terms) or "—")
        self.synonyms_label.setText(" · ".join(entry.synonyms) or "—")
        self.open_button.setEnabled(True)
        self.cards_button.setEnabled(True)
        self.questions_button.setEnabled(True)
        self.favorite_button.setEnabled(self._repository is not None)
        self._update_favorite_button()

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

    def _heading(self, key: LearningPageCopyKey) -> QLabel:
        label = QLabel(learning_text(self._locale, key))
        label.setObjectName("contentSubheading")
        return label


def _copy(locale: AppLocale, es: str, en: str, da: str) -> str:
    return {
        AppLocale.SPANISH_SPAIN: es,
        AppLocale.ENGLISH: en,
        AppLocale.DANISH_DENMARK: da,
    }[locale]


__all__ = ["GlossaryPage"]
