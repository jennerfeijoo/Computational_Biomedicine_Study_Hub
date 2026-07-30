"""DM847 course registration and lazy authored-module navigation."""

from __future__ import annotations

from PySide6.QtCore import Slot
from PySide6.QtWidgets import (
    QComboBox,
    QFrame,
    QHBoxLayout,
    QLabel,
    QStackedWidget,
    QVBoxLayout,
    QWidget,
)

from ..content.bundles import ModuleBundle
from ..content.dm847 import BUNDLES, LOCALIZED_BUNDLES
from ..i18n import DEFAULT_LOCALE, AppLocale, MessageKey, Translator
from ..ui.pages.module_reader_page import ModuleReaderPage
from .models import CourseRegistration


class DM847Page(QWidget):
    """Construct each completed localized DM847 module reader on first selection."""

    def __init__(self, locale: AppLocale = DEFAULT_LOCALE) -> None:
        super().__init__()
        self.setObjectName("dm847CoursePage")
        self._translator = Translator(locale)
        self._bundles: tuple[ModuleBundle, ...] = (
            BUNDLES
            if locale == DEFAULT_LOCALE
            else tuple(bundle.materialize(locale) for bundle in LOCALIZED_BUNDLES)
        )

        self._module_selector = QComboBox()
        self._module_selector.setObjectName("courseModuleSelector")
        self._module_stack = QStackedWidget()
        self._module_stack.setObjectName("courseModuleStack")
        self._module_title = QLabel()
        self._module_title.setObjectName("moduleContextTitle")
        self._module_title.setWordWrap(True)
        self._reader_cache: dict[int, ModuleReaderPage] = {}

        for number, bundle in enumerate(self._bundles, start=1):
            label = self._translator.text(MessageKey.MODULE_LABEL, number=number)
            self._module_selector.addItem(label, bundle.module.module_id)
            placeholder = QWidget()
            placeholder.setObjectName("moduleReaderPlaceholder")
            placeholder.setProperty("moduleId", bundle.module.module_id)
            self._module_stack.addWidget(placeholder)

        context_bar = QFrame()
        context_bar.setObjectName("moduleContextBar")
        context_layout = QHBoxLayout(context_bar)
        context_layout.setContentsMargins(14, 8, 14, 8)
        context_layout.setSpacing(12)

        course_code = QLabel("DM847")
        course_code.setObjectName("moduleContextKicker")
        context_layout.addWidget(course_code)
        context_layout.addWidget(self._module_selector)
        context_layout.addWidget(self._module_title, 1)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(8)
        layout.addWidget(context_bar)
        layout.addWidget(self._module_stack, 1)

        self._module_selector.currentIndexChanged.connect(self._activate_module)
        self._activate_module(0)

    @property
    def reader(self) -> ModuleReaderPage:
        """Return the reader for the currently selected module."""
        return self._reader_for_index(self.current_module_index)

    @property
    def module_count(self) -> int:
        """Return the number of completed modules available in the course page."""
        return len(self._bundles)

    @property
    def current_module_index(self) -> int:
        """Return the zero-based selected module index."""
        return self._module_selector.currentIndex()

    @property
    def constructed_reader_count(self) -> int:
        """Return the number of readers constructed during this page lifetime."""
        return len(self._reader_cache)

    def has_constructed_reader(self, index: int) -> bool:
        """Return whether a module reader has been constructed for one index."""
        return index in self._reader_cache

    def select_module(self, index: int) -> bool:
        """Select a completed module by zero-based index."""
        if not 0 <= index < self.module_count:
            return False
        if index == self.current_module_index:
            self._activate_module(index)
        else:
            self._module_selector.setCurrentIndex(index)
        return True

    @Slot(int)
    def _activate_module(self, index: int) -> None:
        if not 0 <= index < self.module_count:
            return
        reader = self._reader_for_index(index)
        self._module_stack.setCurrentWidget(reader)
        self._module_title.setText(reader.module.title)

    def _reader_for_index(self, index: int) -> ModuleReaderPage:
        if not 0 <= index < self.module_count:
            raise IndexError(index)
        cached = self._reader_cache.get(index)
        if cached is not None:
            return cached

        bundle = self._bundles[index]
        reader = ModuleReaderPage(
            bundle.module,
            objective_question_bank=bundle.objective_question_bank,
            show_context_bar=False,
            translator=self._translator,
        )
        reader.setProperty("contentVersion", bundle.content_version)

        placeholder = self._module_stack.widget(index)
        if placeholder is None:
            raise RuntimeError(f"Missing module placeholder at index {index}.")
        self._module_stack.removeWidget(placeholder)
        placeholder.deleteLater()
        self._module_stack.insertWidget(index, reader)
        self._reader_cache[index] = reader
        return reader


def create_page(locale: AppLocale = DEFAULT_LOCALE) -> QWidget:
    """Create the DM847 page without constructing widgets during import."""
    return DM847Page(locale)


COURSE = CourseRegistration(
    code="DM847",
    title="Introducción a la bioinformática",
    ects=10,
    semester=1,
    summary="Algoritmos, secuencias, modelos probabilísticos, redes y ómicas.",
    page_factory=create_page,
    localized_titles={
        AppLocale.SPANISH_SPAIN: "Introducción a la bioinformática",
        AppLocale.ENGLISH: "Introduction to Bioinformatics",
        AppLocale.DANISH_DENMARK: "Introduktion til bioinformatik",
    },
    localized_summaries={
        AppLocale.SPANISH_SPAIN: (
            "Algoritmos, secuencias, modelos probabilísticos, redes y datos ómicos."
        ),
        AppLocale.ENGLISH: (
            "Algorithms, sequences, probabilistic models, networks and omics data."
        ),
        AppLocale.DANISH_DENMARK: (
            "Algoritmer, sekvenser, probabilistiske modeller, netværk og omikdata."
        ),
    },
)
