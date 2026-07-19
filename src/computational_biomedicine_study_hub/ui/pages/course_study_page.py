"""Generic lazy course and module study page."""

from __future__ import annotations

from datetime import UTC, datetime

from PySide6.QtCore import Signal, Slot
from PySide6.QtWidgets import (
    QComboBox,
    QFrame,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QStackedWidget,
    QVBoxLayout,
    QWidget,
)

from ...i18n import DEFAULT_LOCALE, AppLocale, Translator
from ...learning.academic_catalog import AcademicCatalog, CatalogModule
from ...learning.progress_repository import ProgressRepository
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

        self._module_selector = QComboBox()
        self._module_selector.setObjectName("courseModuleSelector")
        self._module_selector.setAccessibleName(learning_text(locale, LearningPageCopyKey.MODULE))
        self._module_stack = QStackedWidget()
        self._module_stack.setObjectName("courseModuleStack")
        self._module_title = QLabel()
        self._module_title.setObjectName("moduleContextTitle")
        self._module_title.setWordWrap(True)
        self._progress_summary = QLabel()
        self._progress_summary.setObjectName("courseProgressSummary")
        self._progress_summary.setWordWrap(True)
        self._continue_button = QPushButton(learning_text(locale, LearningPageCopyKey.CONTINUE))
        self._continue_button.setObjectName("continueCourseButton")
        self._continue_button.clicked.connect(self.continue_learning)
        self._cumulative_button = QPushButton(
            {
                AppLocale.SPANISH_SPAIN: "Evaluación acumulativa",
                AppLocale.ENGLISH: "Cumulative assessment",
                AppLocale.DANISH_DENMARK: "Kumulativ evaluering",
            }[locale]
        )
        self._cumulative_button.setObjectName("openCumulativeAssessmentButton")
        self._cumulative_button.clicked.connect(
            lambda: self.cumulative_requested.emit(self.course_code)
        )
        source_course = catalog.source_course(self.course_code)
        available = source_course.cumulative_assessment is not None
        self._cumulative_button.setEnabled(available)
        if not available:
            self._cumulative_button.setToolTip(
                {
                    AppLocale.SPANISH_SPAIN: "El contenido acumulativo aún no existe.",
                    AppLocale.ENGLISH: "Cumulative content is not yet available.",
                    AppLocale.DANISH_DENMARK: "Kumulativt indhold er endnu ikke tilgængeligt.",
                }[locale]
            )

        for number, record in enumerate(self._records, start=1):
            self._module_selector.addItem(
                f"M{number:02} · {record.title}",
                record.module_id,
            )
            placeholder = QWidget()
            placeholder.setObjectName("moduleReaderPlaceholder")
            placeholder.setProperty("moduleId", record.module_id)
            self._module_stack.addWidget(placeholder)

        context = QFrame()
        context.setObjectName("moduleContextBar")
        context_layout = QHBoxLayout(context)
        context_layout.setContentsMargins(14, 8, 14, 8)
        context_layout.setSpacing(12)
        kicker = QLabel(self.course_code)
        kicker.setObjectName("moduleContextKicker")
        context_layout.addWidget(kicker)
        context_layout.addWidget(self._module_selector)
        context_layout.addWidget(self._module_title, 1)
        context_layout.addWidget(self._progress_summary)
        context_layout.addWidget(self._continue_button)
        context_layout.addWidget(self._cumulative_button)

        overview = QFrame()
        overview.setObjectName("courseOverviewPanel")
        overview_layout = QVBoxLayout(overview)
        overview_layout.setContentsMargins(14, 10, 14, 10)
        self._course_summary = QLabel(source_course.summary.resolve(_locale_code(locale)))
        self._course_summary.setObjectName("courseAcademicSummary")
        self._course_summary.setWordWrap(True)
        outcomes = tuple(
            outcome.statement.resolve(_locale_code(locale))
            for outcome in source_course.learning_outcomes
        )
        self._course_outcomes = QLabel("\n".join(f"• {value}" for value in outcomes))
        self._course_outcomes.setObjectName("courseLearningOutcomes")
        self._course_outcomes.setWordWrap(True)
        self._course_stats = QLabel()
        self._course_stats.setObjectName("courseSemesterProgress")
        self._course_stats.setWordWrap(True)
        overview_layout.addWidget(self._course_summary)
        if outcomes:
            overview_layout.addWidget(self._course_outcomes)
        overview_layout.addWidget(self._course_stats)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(8)
        layout.addWidget(overview)
        layout.addWidget(context)
        layout.addWidget(self._module_stack, 1)

        self._module_selector.currentIndexChanged.connect(self._activate_module)
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
        self._module_title.setText(reader.module.title)
        self._update_progress(reader.module.course_code, reader.module.module_id)

    def _update_progress(self, course_code: str, module_id: str) -> None:
        if self._progress_repository is None:
            self._progress_summary.clear()
            return
        progress = self._progress_repository.module_progress(course_code, module_id)
        self._progress_summary.setText(
            learning_text(
                self._locale,
                LearningPageCopyKey.MODULE_PROGRESS,
                percent=round(progress.success_ratio * 100),
                pending=progress.pending_review_count,
                attempts=progress.attempt_count,
            )
        )
        self._update_course_stats()

    def _update_course_stats(self) -> None:
        if self._progress_repository is None:
            self._course_stats.clear()
            return
        progress = tuple(
            self._progress_repository.module_progress(record.course_code, record.module_id)
            for record in self._records
        )
        started = tuple(item for item in progress if item.attempt_count or item.last_activity_at)
        completion = round(100 * len(started) / len(progress)) if progress else 0
        cards = self._progress_repository.list_flashcard_progress(course_code=self.course_code)
        due_cards = sum(item.due_at <= datetime.now(UTC) for item in cards)
        recent = tuple(item.last_activity_at for item in progress if item.last_activity_at)
        last_activity = max(recent).strftime("%Y-%m-%d %H:%M") if recent else "—"
        templates = {
            AppLocale.SPANISH_SPAIN: (
                "{completion}% de módulos iniciados · {due} tarjetas pendientes · "
                "última actividad: {last}"
            ),
            AppLocale.ENGLISH: (
                "{completion}% of modules started · {due} cards due · last activity: {last}"
            ),
            AppLocale.DANISH_DENMARK: (
                "{completion}% af moduler startet · {due} kort forfalder · "
                "seneste aktivitet: {last}"
            ),
        }
        self._course_stats.setText(
            templates[self._locale].format(
                completion=completion,
                due=due_cards,
                last=last_activity,
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


def _locale_code(locale: AppLocale) -> str:
    if locale is AppLocale.SPANISH_SPAIN:
        return "es"
    if locale is AppLocale.DANISH_DENMARK:
        return "da"
    return "en"


__all__ = ["CourseStudyPage"]
