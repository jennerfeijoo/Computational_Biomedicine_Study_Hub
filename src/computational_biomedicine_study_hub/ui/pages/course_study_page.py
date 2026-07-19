"""Generic lazy course and module study page."""

from __future__ import annotations

from PySide6.QtCore import Signal, Slot
from PySide6.QtWidgets import (
    QStackedWidget,
    QVBoxLayout,
    QWidget,
)

from ...i18n import DEFAULT_LOCALE, AppLocale, Translator
from ...learning.academic_catalog import AcademicCatalog, CatalogModule
from ...learning.progress_repository import ProgressRepository
from ..course_module_toolbar import (
    CourseModuleToolbar,
    course_information_from_source,
)
from ..learning_page_copy import LearningPageCopyKey, learning_text
from ..study_state import StudyLocation
from .module_reader_page import ModuleReaderPage


class CourseStudyPage(QWidget):
    """Render any YAML-backed course with one reusable lazy module engine."""

    cumulative_requested = Signal(str)

    def __init__(
        self,
        course_code: str,
        catalog: AcademicCatalog,
        *,
        locale: AppLocale = DEFAULT_LOCALE,
        progress_repository: ProgressRepository | None = None,
        parent: QWidget | None = None,
    ) -> None:
        super().__init__(parent)
        self.course_code = course_code.upper()
        self._catalog = catalog
        self._locale = locale
        self._translator = Translator(locale)
        self._progress_repository = progress_repository
        self._records = catalog.modules(self.course_code)
        self._reader_cache: dict[int, ModuleReaderPage] = {}
        self.setObjectName("courseStudyPage")
        self.setProperty("courseCode", self.course_code)

        source_course = catalog.source_course(self.course_code)
        self._toolbar = CourseModuleToolbar(
            course_code=self.course_code,
            locale=locale,
            information=course_information_from_source(source_course, locale),
            cumulative_available=source_course.cumulative_assessment is not None,
        )
        self._module_selector = self._toolbar.module_selector
        self._module_title = self._toolbar.module_title
        self._progress_summary = self._toolbar.progress_summary
        self._continue_button = self._toolbar.continue_button
        self._cumulative_button = self._toolbar.cumulative_button

        self._module_stack = QStackedWidget()
        self._module_stack.setObjectName("courseModuleStack")

        for number, record in enumerate(self._records, start=1):
            self._toolbar.add_module(number, record.module_id)
            placeholder = QWidget()
            placeholder.setObjectName("moduleReaderPlaceholder")
            placeholder.setProperty("moduleId", record.module_id)
            self._module_stack.addWidget(placeholder)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(8)
        layout.addWidget(self._toolbar)
        layout.addWidget(self._module_stack, 1)

        self._toolbar.module_changed.connect(self._activate_module)
        self._toolbar.continue_requested.connect(self.continue_learning)
        self._toolbar.cumulative_requested.connect(
            lambda: self.cumulative_requested.emit(self.course_code)
        )
        if self._records:
            self._activate_module(0)

    @property
    def records(self) -> tuple[CatalogModule, ...]:
        return self._records

    @property
    def module_count(self) -> int:
        return len(self._records)

    @property
    def current_module_index(self) -> int:
        return self._module_selector.currentIndex()

    @property
    def constructed_reader_count(self) -> int:
        return len(self._reader_cache)

    @property
    def reader(self) -> ModuleReaderPage:
        return self._reader_for_index(self.current_module_index)

    def has_constructed_reader(self, index: int) -> bool:
        return index in self._reader_cache

    def select_module(self, index: int) -> bool:
        if not 0 <= index < self.module_count:
            return False
        if index == self.current_module_index:
            self._activate_module(index)
        else:
            self._module_selector.setCurrentIndex(index)
        return True

    def select_module_id(self, module_id: str) -> bool:
        return self.select_module(self._module_selector.findData(module_id))

    def capture_state(self, route: str = "") -> StudyLocation:
        record = self._records[self.current_module_index]
        return StudyLocation(
            route=route,
            course_code=self.course_code,
            module_id=record.module_id,
            tab_index=self.reader.current_section_index,
            logical_position=self.current_module_index,
        )

    def restore_state(self, state: StudyLocation) -> None:
        if state.course_code and state.course_code.upper() != self.course_code:
            return
        if state.module_id:
            self.select_module_id(state.module_id)
        elif 0 <= state.logical_position < self.module_count:
            self.select_module(state.logical_position)
        self.reader.select_section_index(state.tab_index)

    @Slot()
    def continue_learning(self) -> None:
        if self._progress_repository is None:
            return
        candidates = tuple(
            (
                index,
                self._progress_repository.module_progress(record.course_code, record.module_id),
            )
            for index, record in enumerate(self._records)
        )
        recent = tuple(
            candidate for candidate in candidates if candidate[1].last_activity_at is not None
        )
        if recent:
            index, _ = max(
                recent,
                key=lambda candidate: (
                    candidate[1].last_activity_at.timestamp()
                    if candidate[1].last_activity_at is not None
                    else 0.0
                ),
            )
            self.select_module(index)

    @Slot(int)
    def _activate_module(self, index: int) -> None:
        if not 0 <= index < self.module_count:
            return
        reader = self._reader_for_index(index)
        self._module_stack.setCurrentWidget(reader)
        self._toolbar.set_module_title(reader.module.title)
        self._update_progress(reader.module.course_code, reader.module.module_id)

    def _update_progress(self, course_code: str, module_id: str) -> None:
        if self._progress_repository is None:
            self._toolbar.set_progress("")
            return
        progress = self._progress_repository.module_progress(course_code, module_id)
        self._toolbar.set_progress(
            learning_text(
                self._locale,
                LearningPageCopyKey.MODULE_PROGRESS,
                percent=round(progress.success_ratio * 100),
                pending=progress.pending_review_count,
                attempts=progress.attempt_count,
            )
        )

    def _reader_for_index(self, index: int) -> ModuleReaderPage:
        if not 0 <= index < self.module_count:
            raise IndexError(index)
        cached = self._reader_cache.get(index)
        if cached is not None:
            return cached
        record = self._records[index]
        reader = ModuleReaderPage(
            record.module,
            objective_question_bank=record.objective_question_bank,
            show_context_bar=False,
            translator=self._translator,
            progress_repository=self._progress_repository,
            content_version=record.content_version,
        )
        reader.setProperty("contentVersion", record.content_version)
        placeholder = self._module_stack.widget(index)
        if placeholder is None:
            raise RuntimeError(f"Missing module placeholder at index {index}.")
        self._module_stack.removeWidget(placeholder)
        placeholder.deleteLater()
        self._module_stack.insertWidget(index, reader)
        self._reader_cache[index] = reader
        return reader


__all__ = ["CourseStudyPage"]
