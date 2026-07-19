"""Learner-facing persistent review queue and mastery summary."""

from __future__ import annotations

import json
import uuid
from collections import Counter
from datetime import UTC, datetime
from functools import partial

from PySide6.QtCore import Qt, Signal, Slot
from PySide6.QtWidgets import (
    QCheckBox,
    QComboBox,
    QFrame,
    QGridLayout,
    QHBoxLayout,
    QLabel,
    QListWidget,
    QListWidgetItem,
    QPushButton,
    QSplitter,
    QVBoxLayout,
    QWidget,
)

from ...i18n import DEFAULT_LOCALE, AppLocale
from ...learning.academic_catalog import AcademicCatalog
from ...learning.activity_submission import ActivitySubmission
from ...learning.progress import (
    AttemptRecord,
    LearningItemKind,
    MasteryState,
    ReviewSchedule,
)
from ...learning.progress_repository import ProgressRepository
from ...learning.recommendations import RecommendationCategory
from ...learning.spaced_repetition import ReviewRating, reschedule
from ..activities import (
    ActivityRendererRegistry,
    ActivityWidget,
    OpenResponseActivityWidget,
    create_default_activity_registry,
)
from ..learning_page_copy import LearningPageCopyKey, learning_text
from ..review_presentation import (
    ReviewItemPresentation,
    ReviewPresentationResolver,
    course_title,
    localized_datetime,
    localized_item_type,
    localized_result,
    shortened,
)

_COPY = {
    AppLocale.SPANISH_SPAIN: {
        "queue": "Cola de repaso",
        "study": "Panel de estudio",
        "select": "Selecciona un elemento para empezar a estudiar.",
        "explanation": "Ver explicación",
        "open_module": "Abrir módulo",
        "skip": "Omitir por ahora",
        "retry": "Reintentar pregunta",
        "review_now": "Repasar ahora",
        "view_all": "Ver todos",
        "continue": "Continuar",
        "answer_saved": "Respuesta registrada. Ya puedes valorar este repaso.",
        "revealed": "Explicación mostrada. Ya puedes valorar este repaso.",
        "unavailable": (
            "Esta referencia ya no existe en el catálogo académico. No se puede calificar."
        ),
        "mastery_none": "Todavía no hay actividad suficiente para estimar el dominio.",
        "mastery_semester": "Dominio estimado del semestre: {percent} %",
        "mastery_course": "Dominio de {title}: {percent} %",
        "mastery_module": "Dominio de {title}: {percent} %",
        "today_empty": "No hay actividades vencidas.",
        "reinforce_empty": "No hay temas que necesiten refuerzo.",
        "failed_empty": "No hay preguntas falladas.",
        "cards_empty": "No hay tarjetas pendientes.",
        "continue_empty": "Todavía no hay actividad para continuar.",
        "progress_empty": "No hay asignaturas en el ámbito activo.",
        "history_empty": "Todavía no existe historial.",
        "filter_empty": "No hay elementos para los filtros seleccionados.",
        "errors": "{title}: {count} errores.",
        "failed_attempts": "{title}: {count} intentos incorrectos.",
        "cards": "{count} pendientes: {titles}",
        "last_activity": "{title} · {module} · {date}",
        "course_progress": "{title}: {percent} % en {count} intentos.",
        "no_attempts": "{title}: Sin intentos.",
        "new_session_tip": (
            "Reconstruye la cola vencida con los filtros actuales y comienza por "
            "el primer elemento."
        ),
        "new_concepts_tip": (
            "Añade hasta diez conceptos nuevos de los filtros activos, sin duplicar "
            "elementos ya programados."
        ),
        "technical_tip": "Identidad técnica: {identity}",
    },
    AppLocale.ENGLISH: {
        "queue": "Review queue",
        "study": "Study panel",
        "select": "Select an item to start studying.",
        "explanation": "View explanation",
        "open_module": "Open module",
        "skip": "Skip for now",
        "retry": "Retry question",
        "review_now": "Review now",
        "view_all": "View all",
        "continue": "Continue",
        "answer_saved": "Answer recorded. You can now rate this review.",
        "revealed": "Explanation revealed. You can now rate this review.",
        "unavailable": (
            "This reference no longer exists in the academic catalog. It cannot be rated."
        ),
        "mastery_none": "There is not enough activity yet to estimate mastery.",
        "mastery_semester": "Estimated semester mastery: {percent}%",
        "mastery_course": "{title} mastery: {percent}%",
        "mastery_module": "{title} mastery: {percent}%",
        "today_empty": "There are no due activities.",
        "reinforce_empty": "No topics need reinforcement.",
        "failed_empty": "There are no failed questions.",
        "cards_empty": "There are no pending flashcards.",
        "continue_empty": "There is no activity to continue yet.",
        "progress_empty": "There are no courses in the active scope.",
        "history_empty": "There is no history yet.",
        "filter_empty": "There are no items for the selected filters.",
        "errors": "{title}: {count} errors.",
        "failed_attempts": "{title}: {count} incorrect attempts.",
        "cards": "{count} pending: {titles}",
        "last_activity": "{title} · {module} · {date}",
        "course_progress": "{title}: {percent}% across {count} attempts.",
        "no_attempts": "{title}: No attempts.",
        "new_session_tip": (
            "Rebuilds the due queue with the current filters and starts at the first item."
        ),
        "new_concepts_tip": (
            "Adds up to ten new concepts from the active filters without duplicating "
            "already scheduled items."
        ),
        "technical_tip": "Technical identity: {identity}",
    },
    AppLocale.DANISH_DENMARK: {
        "queue": "Repetitionskø",
        "study": "Studiepanel",
        "select": "Vælg et element for at begynde.",
        "explanation": "Vis forklaring",
        "open_module": "Åbn modul",
        "skip": "Spring over indtil videre",
        "retry": "Prøv spørgsmålet igen",
        "review_now": "Repetér nu",
        "view_all": "Vis alle",
        "continue": "Fortsæt",
        "answer_saved": "Svaret er registreret. Du kan nu bedømme repetitionen.",
        "revealed": "Forklaringen vises. Du kan nu bedømme repetitionen.",
        "unavailable": (
            "Denne reference findes ikke længere i det akademiske katalog. Den kan ikke bedømmes."
        ),
        "mastery_none": "Der er endnu ikke nok aktivitet til at estimere mestring.",
        "mastery_semester": "Estimeret mestring for semesteret: {percent} %",
        "mastery_course": "Mestring af {title}: {percent} %",
        "mastery_module": "Mestring af {title}: {percent} %",
        "today_empty": "Der er ingen forfaldne aktiviteter.",
        "reinforce_empty": "Ingen emner kræver styrkelse.",
        "failed_empty": "Der er ingen forkerte spørgsmål.",
        "cards_empty": "Der er ingen ventende kort.",
        "continue_empty": "Der er endnu ingen aktivitet at fortsætte.",
        "progress_empty": "Der er ingen kurser i det aktive omfang.",
        "history_empty": "Der er endnu ingen historik.",
        "filter_empty": "Der er ingen elementer til de valgte filtre.",
        "errors": "{title}: {count} fejl.",
        "failed_attempts": "{title}: {count} forkerte forsøg.",
        "cards": "{count} ventende: {titles}",
        "last_activity": "{title} · {module} · {date}",
        "course_progress": "{title}: {percent} % i {count} forsøg.",
        "no_attempts": "{title}: Ingen forsøg.",
        "new_session_tip": (
            "Genopbygger den forfaldne kø med de aktive filtre og starter med det første element."
        ),
        "new_concepts_tip": (
            "Tilføjer op til ti nye begreber fra de aktive filtre uden at duplikere "
            "planlagte elementer."
        ),
        "technical_tip": "Teknisk identitet: {identity}",
    },
}

_CATEGORY_TITLES = {
    AppLocale.SPANISH_SPAIN: {
        RecommendationCategory.TODAY: "Para hoy",
        RecommendationCategory.REINFORCE: "Necesita refuerzo",
        RecommendationCategory.FAILED_QUESTIONS: "Preguntas falladas",
        RecommendationCategory.PENDING_CARDS: "Tarjetas pendientes",
        RecommendationCategory.CONTINUE: "Continuar donde lo dejaste",
        RecommendationCategory.COURSE_PROGRESS: "Progreso por asignatura",
    },
    AppLocale.ENGLISH: {
        RecommendationCategory.TODAY: "For today",
        RecommendationCategory.REINFORCE: "Needs reinforcement",
        RecommendationCategory.FAILED_QUESTIONS: "Failed questions",
        RecommendationCategory.PENDING_CARDS: "Pending flashcards",
        RecommendationCategory.CONTINUE: "Continue where you left off",
        RecommendationCategory.COURSE_PROGRESS: "Progress by course",
    },
    AppLocale.DANISH_DENMARK: {
        RecommendationCategory.TODAY: "Til i dag",
        RecommendationCategory.REINFORCE: "Kræver styrkelse",
        RecommendationCategory.FAILED_QUESTIONS: "Forkerte spørgsmål",
        RecommendationCategory.PENDING_CARDS: "Ventende kort",
        RecommendationCategory.CONTINUE: "Fortsæt hvor du slap",
        RecommendationCategory.COURSE_PROGRESS: "Fremskridt pr. kursus",
    },
}


class ReviewPage(QWidget):
    """Resolve, study and reschedule a filtered queue of stable identities."""

    module_requested = Signal(str, str)
    assessments_requested = Signal(str, str)
    flashcards_requested = Signal(str, str)
    open_feedback_requested = Signal(str, str, str, str, str)

    def __init__(
        self,
        catalog: AcademicCatalog,
        repository: ProgressRepository,
        *,
        locale: AppLocale = DEFAULT_LOCALE,
        registry: ActivityRendererRegistry | None = None,
        parent: QWidget | None = None,
    ) -> None:
        super().__init__(parent)
        self.setObjectName("reviewPage")
        self._catalog = catalog
        self._repository = repository
        self._locale = locale
        self._registry = registry or create_default_activity_registry()
        self._resolver = ReviewPresentationResolver(catalog, repository, locale)
        self._queue: tuple[ReviewSchedule, ...] = ()
        self._presentations: tuple[ReviewItemPresentation, ...] = ()
        self._ready_identity: tuple[str, str, str, LearningItemKind] | None = None
        self._activity_widget: ActivityWidget | None = None
        self._summary_targets: dict[RecommendationCategory, tuple[str, str, str]] = {}

        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(10)
        layout.addWidget(self._build_filters())

        summary = QHBoxLayout()
        self.due_label = QLabel()
        self.due_label.setObjectName("reviewDueCount")
        self.mastery_label = QLabel()
        self.mastery_label.setObjectName("reviewMastery")
        self.mastery_label.setWordWrap(True)
        summary.addWidget(self.due_label)
        summary.addWidget(self.mastery_label, 1)
        layout.addLayout(summary)

        self._recommendation_labels: dict[RecommendationCategory, QLabel] = {}
        recommendation_grid = QGridLayout()
        recommendation_grid.setSpacing(8)
        for index, category in enumerate(RecommendationCategory):
            recommendation_grid.addWidget(
                self._build_summary_card(category),
                index // 3,
                index % 3,
            )
        layout.addLayout(recommendation_grid)

        splitter = QSplitter(Qt.Orientation.Horizontal)
        splitter.setObjectName("reviewStudySplitter")
        splitter.addWidget(self._build_queue_panel())
        splitter.addWidget(self._build_study_panel())
        splitter.setStretchFactor(0, 2)
        splitter.setStretchFactor(1, 3)
        layout.addWidget(splitter, 1)

        ratings = QHBoxLayout()
        self._rating_buttons: list[QPushButton] = []
        for key, rating in (
            (LearningPageCopyKey.AGAIN, ReviewRating.AGAIN),
            (LearningPageCopyKey.HARD, ReviewRating.HARD),
            (LearningPageCopyKey.GOOD, ReviewRating.GOOD),
            (LearningPageCopyKey.EASY, ReviewRating.EASY),
        ):
            button = QPushButton(learning_text(locale, key))
            button.setObjectName(f"reviewRating_{rating.name.casefold()}")
            button.setEnabled(False)
            button.clicked.connect(lambda checked=False, value=rating: self.rate_selected(value))
            self._rating_buttons.append(button)
            ratings.addWidget(button)
        ratings.addStretch(1)
        layout.addLayout(ratings)

        history_title = QLabel(learning_text(locale, LearningPageCopyKey.HISTORY))
        history_title.setObjectName("sectionHeading")
        self.history_label = QLabel()
        self.history_label.setObjectName("reviewHistory")
        self.history_label.setWordWrap(True)
        self.history_label.setTextInteractionFlags(Qt.TextInteractionFlag.TextSelectableByMouse)
        layout.addWidget(history_title)
        layout.addWidget(self.history_label)

        self.course_selector.currentIndexChanged.connect(self._refresh_modules)
        self.module_selector.currentIndexChanged.connect(self.refresh_queue)
        self.kind_selector.currentIndexChanged.connect(self.refresh_queue)
        self.mix_courses.toggled.connect(self._mix_toggled)
        self.queue_list.currentRowChanged.connect(self._show_selected)
        self._refresh_modules()
        self._mix_toggled(self.mix_courses.isChecked())

    @property
    def queue(self) -> tuple[ReviewSchedule, ...]:
        return self._queue

    @property
    def presentations(self) -> tuple[ReviewItemPresentation, ...]:
        return self._presentations

    def _build_filters(self) -> QFrame:
        filters = QFrame()
        filters.setObjectName("learningFilters")
        row = QHBoxLayout(filters)
        self.mix_courses = QCheckBox(learning_text(self._locale, LearningPageCopyKey.MIX_COURSES))
        self.mix_courses.setObjectName("reviewMixCourses")
        self.mix_courses.setChecked(True)

        self.course_selector = QComboBox()
        self.course_selector.setObjectName("reviewCourseSelector")
        self.course_selector.setAccessibleName(
            learning_text(self._locale, LearningPageCopyKey.COURSE)
        )
        for course_code in self._catalog.course_codes:
            self.course_selector.addItem(
                course_title(self._locale, course_code),
                course_code,
            )
            self.course_selector.setItemData(
                self.course_selector.count() - 1,
                course_code,
                Qt.ItemDataRole.ToolTipRole,
            )

        self.module_selector = QComboBox()
        self.module_selector.setObjectName("reviewModuleSelector")
        self.module_selector.setAccessibleName(
            learning_text(self._locale, LearningPageCopyKey.MODULE)
        )

        self.kind_selector = QComboBox()
        self.kind_selector.setObjectName("reviewTypeSelector")
        self.kind_selector.setAccessibleName(learning_text(self._locale, LearningPageCopyKey.TYPE))
        self.kind_selector.addItem(
            learning_text(self._locale, LearningPageCopyKey.ALL_TYPES),
            None,
        )
        for kind in LearningItemKind:
            self.kind_selector.addItem(
                localized_item_type(self._locale, kind),
                kind.value,
            )

        self.start_button = QPushButton(
            learning_text(self._locale, LearningPageCopyKey.START_REVIEW)
        )
        self.start_button.setObjectName("startReviewSessionButton")
        self.start_button.setToolTip(_COPY[self._locale]["new_session_tip"])
        self.start_button.clicked.connect(self.start_review)

        self.new_concepts_button = QPushButton(
            learning_text(self._locale, LearningPageCopyKey.NEW_CONCEPTS)
        )
        self.new_concepts_button.setObjectName("addNewConceptsButton")
        self.new_concepts_button.setToolTip(_COPY[self._locale]["new_concepts_tip"])
        self.new_concepts_button.clicked.connect(self.add_new_concepts)

        for widget in (
            self.mix_courses,
            self.course_selector,
            self.module_selector,
            self.kind_selector,
            self.start_button,
            self.new_concepts_button,
        ):
            row.addWidget(widget)
        return filters

    def _build_summary_card(self, category: RecommendationCategory) -> QFrame:
        frame = QFrame()
        frame.setObjectName(f"reviewBlock_{category.value}")
        frame.setFrameShape(QFrame.Shape.StyledPanel)
        block = QVBoxLayout(frame)
        title = QLabel(_CATEGORY_TITLES[self._locale][category])
        title.setObjectName("sectionHeading")
        content = QLabel()
        content.setObjectName(f"reviewReasons_{category.value}")
        content.setWordWrap(True)
        content.setTextInteractionFlags(Qt.TextInteractionFlag.TextSelectableByMouse)
        block.addWidget(title)
        block.addWidget(content, 1)
        self._recommendation_labels[category] = content

        actions = QHBoxLayout()
        if category is RecommendationCategory.TODAY:
            primary = QPushButton(_COPY[self._locale]["review_now"])
            primary.setObjectName("reviewNowButton")
            primary.clicked.connect(self.start_review)
            secondary = QPushButton(_COPY[self._locale]["view_all"])
            secondary.setObjectName("viewAllDueButton")
            secondary.clicked.connect(self._focus_queue)
            actions.addWidget(primary)
            actions.addWidget(secondary)
        elif category is RecommendationCategory.REINFORCE:
            button = QPushButton(_COPY[self._locale]["open_module"])
            button.setObjectName("openReinforcementModuleButton")
            button.clicked.connect(lambda: self._activate_summary(RecommendationCategory.REINFORCE))
            actions.addWidget(button)
        elif category is RecommendationCategory.FAILED_QUESTIONS:
            button = QPushButton(_COPY[self._locale]["retry"])
            button.setObjectName("retryFailedQuestionButton")
            button.clicked.connect(
                lambda: self._activate_summary(RecommendationCategory.FAILED_QUESTIONS)
            )
            actions.addWidget(button)
        elif category is RecommendationCategory.PENDING_CARDS:
            button = QPushButton(_COPY[self._locale]["view_all"])
            button.setObjectName("viewPendingCardsButton")
            button.clicked.connect(
                lambda: self._activate_summary(RecommendationCategory.PENDING_CARDS)
            )
            actions.addWidget(button)
        elif category is RecommendationCategory.CONTINUE:
            button = QPushButton(_COPY[self._locale]["continue"])
            button.setObjectName("continueReviewButton")
            button.clicked.connect(lambda: self._activate_summary(RecommendationCategory.CONTINUE))
            actions.addWidget(button)
        actions.addStretch(1)
        block.addLayout(actions)
        return frame

    def _build_queue_panel(self) -> QWidget:
        panel = QWidget()
        panel.setObjectName("reviewQueuePanel")
        layout = QVBoxLayout(panel)
        heading = QLabel(_COPY[self._locale]["queue"])
        heading.setObjectName("sectionHeading")
        layout.addWidget(heading)
        self.queue_list = QListWidget()
        self.queue_list.setObjectName("reviewQueue")
        self.queue_list.setAccessibleName(_COPY[self._locale]["queue"])
        layout.addWidget(self.queue_list, 1)
        self.empty_label = QLabel(_COPY[self._locale]["filter_empty"])
        self.empty_label.setObjectName("reviewEmptyState")
        self.empty_label.setWordWrap(True)
        layout.addWidget(self.empty_label)
        return panel

    def _build_study_panel(self) -> QFrame:
        panel = QFrame()
        panel.setObjectName("reviewStudyPanel")
        panel.setFrameShape(QFrame.Shape.StyledPanel)
        layout = QVBoxLayout(panel)
        heading = QLabel(_COPY[self._locale]["study"])
        heading.setObjectName("sectionHeading")
        layout.addWidget(heading)
        self.study_type_label = QLabel()
        self.study_type_label.setObjectName("reviewStudyType")
        self.study_title_label = QLabel(_COPY[self._locale]["select"])
        self.study_title_label.setObjectName("reviewStudyTitle")
        self.study_title_label.setWordWrap(True)
        self.study_context_label = QLabel()
        self.study_context_label.setObjectName("reviewStudyContext")
        self.study_context_label.setWordWrap(True)
        layout.addWidget(self.study_type_label)
        layout.addWidget(self.study_title_label)
        layout.addWidget(self.study_context_label)

        self._study_content = QWidget()
        self._study_content.setObjectName("reviewStudyContent")
        self._study_content_layout = QVBoxLayout(self._study_content)
        self._study_content_layout.setContentsMargins(0, 4, 0, 4)
        layout.addWidget(self._study_content, 1)

        self.study_status_label = QLabel()
        self.study_status_label.setObjectName("reviewStudyStatus")
        self.study_status_label.setWordWrap(True)
        layout.addWidget(self.study_status_label)

        actions = QHBoxLayout()
        self.reveal_button = QPushButton(_COPY[self._locale]["explanation"])
        self.reveal_button.setObjectName("reviewRevealButton")
        self.reveal_button.clicked.connect(self.reveal_selected)
        self.open_module_button = QPushButton(_COPY[self._locale]["open_module"])
        self.open_module_button.setObjectName("reviewOpenModuleButton")
        self.open_module_button.clicked.connect(self.open_selected_module)
        self.retry_button = QPushButton(_COPY[self._locale]["retry"])
        self.retry_button.setObjectName("reviewRetryQuestionButton")
        self.retry_button.clicked.connect(self.retry_selected)
        self.skip_button = QPushButton(_COPY[self._locale]["skip"])
        self.skip_button.setObjectName("reviewSkipButton")
        self.skip_button.clicked.connect(self.skip_selected)
        for button in (
            self.reveal_button,
            self.open_module_button,
            self.retry_button,
            self.skip_button,
        ):
            button.hide()
            actions.addWidget(button)
        actions.addStretch(1)
        layout.addLayout(actions)
        return panel

    @Slot()
    def _refresh_modules(self) -> None:
        course = self.course_selector.currentData()
        self.module_selector.blockSignals(True)
        self.module_selector.clear()
        self.module_selector.addItem(
            learning_text(self._locale, LearningPageCopyKey.ALL_MODULES),
            None,
        )
        if isinstance(course, str):
            for record in self._catalog.modules(course):
                self.module_selector.addItem(record.title, record.module_id)
                self.module_selector.setItemData(
                    self.module_selector.count() - 1,
                    record.module_id,
                    Qt.ItemDataRole.ToolTipRole,
                )
        self.module_selector.blockSignals(False)
        self.refresh_queue()

    @Slot(bool)
    def _mix_toggled(self, checked: bool) -> None:
        self.course_selector.setEnabled(not checked)
        self.module_selector.setEnabled(not checked)
        self.refresh_queue()

    def _active_filters(self) -> tuple[str | None, str | None, LearningItemKind | None]:
        course_value = self.course_selector.currentData()
        module_value = self.module_selector.currentData()
        course_code = (
            None
            if self.mix_courses.isChecked()
            else (course_value if isinstance(course_value, str) else None)
        )
        module_id = (
            None
            if self.mix_courses.isChecked()
            else (module_value if isinstance(module_value, str) else None)
        )
        kind_value = self.kind_selector.currentData()
        kind = LearningItemKind(kind_value) if isinstance(kind_value, str) else None
        return course_code, module_id, kind

    @Slot()
    def refresh_queue(self) -> None:
        course_code, module_id, kind = self._active_filters()
        due = self._repository.list_due_reviews(
            due_at=datetime.now(UTC),
            course_code=course_code,
            module_id=module_id,
            limit=100,
        )
        if kind is not None:
            due = tuple(item for item in due if item.item_kind is kind)
        self._queue = due
        self._presentations = tuple(self._resolver.resolve(item) for item in due)
        self._ready_identity = None
        self._set_rating_enabled(False)

        self.queue_list.blockSignals(True)
        self.queue_list.clear()
        for index, presentation in enumerate(self._presentations):
            row = QListWidgetItem(self._queue_text(presentation))
            row.setData(Qt.ItemDataRole.UserRole, index)
            row.setToolTip(
                _COPY[self._locale]["technical_tip"].format(
                    identity=presentation.technical_identity
                )
            )
            row.setData(
                Qt.ItemDataRole.AccessibleTextRole,
                f"{presentation.display_title}. "
                f"{presentation.localized_type_label}. "
                f"{presentation.course_title}. {presentation.module_title}.",
            )
            self.queue_list.addItem(row)
        self.queue_list.blockSignals(False)

        if due:
            self.queue_list.setCurrentRow(0)
            self._show_selected(0)
        else:
            self._show_selected(-1)
        self.empty_label.setVisible(not due)
        self.empty_label.setText(_COPY[self._locale]["filter_empty"])
        self.due_label.setText(
            learning_text(
                self._locale,
                LearningPageCopyKey.DUE_COUNT,
                count=len(due),
            )
        )
        self._update_mastery(course_code, module_id)
        self._update_history(course_code, module_id, kind)
        self._update_recommendations(course_code, module_id, kind)

    def _queue_text(self, item: ReviewItemPresentation) -> str:
        return (
            f"{item.display_title}\n"
            f"{item.localized_type_label} · {item.course_title} · {item.module_title}\n"
            f"{item.review_reason} · {item.due_text}"
        )

    @Slot()
    def start_review(self) -> None:
        self.refresh_queue()
        self._focus_queue()

    @Slot()
    def _focus_queue(self) -> None:
        if self.queue_list.count():
            self.queue_list.setCurrentRow(0)
            self.queue_list.setFocus(Qt.FocusReason.OtherFocusReason)

    @Slot()
    def add_new_concepts(self) -> None:
        course_code, module_id, kind = self._active_filters()
        if kind not in {None, LearningItemKind.CONCEPT}:
            return
        now = datetime.now(UTC)
        added = 0
        for entry in self._catalog.glossary(course_code=course_code):
            if module_id is not None and entry.module_id != module_id:
                continue
            existing = self._repository.get_review_schedule(
                entry.course_code,
                entry.module_id,
                entry.term_id,
                LearningItemKind.CONCEPT.value,
            )
            if existing is not None:
                continue
            self._repository.save_review_schedule(
                ReviewSchedule(
                    course_code=entry.course_code,
                    module_id=entry.module_id,
                    item_id=entry.term_id,
                    item_kind=LearningItemKind.CONCEPT,
                    mastery_state=MasteryState.NEW,
                    repetitions=0,
                    interval_days=0,
                    easiness=2.5,
                    due_at=now,
                )
            )
            added += 1
            if added >= 10:
                break
        self.refresh_queue()

    @Slot(int)
    def _show_selected(self, row: int) -> None:
        self._clear_study_content()
        self._ready_identity = None
        self._set_rating_enabled(False)
        self.study_status_label.clear()
        for button in (
            self.reveal_button,
            self.open_module_button,
            self.retry_button,
            self.skip_button,
        ):
            button.hide()

        if not 0 <= row < len(self._presentations):
            self.study_type_label.clear()
            self.study_title_label.setText(_COPY[self._locale]["select"])
            self.study_context_label.clear()
            return

        presentation = self._presentations[row]
        self.study_type_label.setText(presentation.localized_type_label)
        self.study_title_label.setText(presentation.display_title)
        self.study_context_label.setText(
            f"{presentation.course_title} · {presentation.module_title}\n"
            f"{presentation.review_reason} · {presentation.due_text}"
        )
        self.study_title_label.setToolTip(
            _COPY[self._locale]["technical_tip"].format(identity=presentation.technical_identity)
        )
        self.open_module_button.setVisible(presentation.resolved)
        self.skip_button.show()
        self.retry_button.setVisible(
            presentation.resolved and presentation.item_type is LearningItemKind.ASSESSMENT
        )

        if not presentation.resolved:
            message = QLabel(_COPY[self._locale]["unavailable"])
            message.setObjectName("reviewUnavailableContent")
            message.setWordWrap(True)
            self._study_content_layout.addWidget(message)
            return

        if presentation.activity_item is not None:
            self._render_activity(presentation)
            return

        prompt = QLabel(presentation.display_prompt)
        prompt.setObjectName("reviewStudyPrompt")
        prompt.setWordWrap(True)
        prompt.setTextInteractionFlags(Qt.TextInteractionFlag.TextSelectableByMouse)
        self._study_content_layout.addWidget(prompt)
        self.reveal_button.show()

    def _render_activity(self, presentation: ReviewItemPresentation) -> None:
        item = presentation.activity_item
        if item is None:
            return
        widget = self._registry.render(item, locale=self._locale)
        widget.submitted.connect(partial(self._record_study_submission, presentation, item))
        if isinstance(widget, OpenResponseActivityWidget):
            widget.feedback_requested.connect(
                partial(self._open_feedback_lab, presentation, widget)
            )
        self._activity_widget = widget
        self._study_content_layout.addWidget(widget)

    @Slot()
    def reveal_selected(self) -> None:
        presentation = self._selected_presentation()
        if presentation is None or not presentation.resolved:
            return
        self.reveal_button.hide()
        explanation = QLabel(presentation.explanation)
        explanation.setObjectName("reviewStudyExplanation")
        explanation.setWordWrap(True)
        explanation.setTextInteractionFlags(Qt.TextInteractionFlag.TextSelectableByMouse)
        self._study_content_layout.addWidget(explanation)
        self._mark_ready(presentation, _COPY[self._locale]["revealed"])

    @Slot()
    def retry_selected(self) -> None:
        row = self.queue_list.currentRow()
        if row >= 0:
            self._show_selected(row)

    @Slot()
    def skip_selected(self) -> None:
        count = self.queue_list.count()
        if count < 2:
            return
        self.queue_list.setCurrentRow((self.queue_list.currentRow() + 1) % count)

    @Slot()
    def open_selected_module(self) -> None:
        presentation = self._selected_presentation()
        if presentation is not None and presentation.resolved:
            self.module_requested.emit(
                presentation.course_code,
                presentation.module_id,
            )

    @Slot(object)
    def _record_study_submission(
        self,
        presentation: ReviewItemPresentation,
        item: object,
        submission: object,
    ) -> None:
        if (
            not isinstance(submission, ActivitySubmission)
            or presentation != self._selected_presentation()
            or presentation.activity_item is None
            or item is not presentation.activity_item
        ):
            return
        response_text = (
            json.dumps(dict(submission.keyed_option_ids), ensure_ascii=False)
            if submission.keyed_option_ids
            else submission.response_text
        )
        self._repository.record_attempt(
            AttemptRecord(
                attempt_id=str(uuid.uuid4()),
                course_code=presentation.course_code,
                module_id=presentation.module_id,
                item_id=presentation.item_id,
                item_kind=presentation.item_type,
                activity_type=presentation.activity_item.activity_type,
                outcome=submission.outcome,
                locale=self._locale.value,
                content_version=presentation.content_version,
                created_at=datetime.now(UTC),
                response_text=response_text,
                selected_option_ids=submission.selected_option_ids,
                is_correct=submission.is_correct,
                score=submission.score,
            )
        )
        self._mark_ready(presentation, _COPY[self._locale]["answer_saved"])
        course_code, module_id, kind = self._active_filters()
        self._update_history(course_code, module_id, kind)
        self._update_mastery(course_code, module_id)
        self._update_recommendations(course_code, module_id, kind)

    def _open_feedback_lab(
        self,
        presentation: ReviewItemPresentation,
        widget: OpenResponseActivityWidget,
        response_text: str,
    ) -> None:
        self.open_feedback_requested.emit(
            presentation.course_code,
            presentation.module_id,
            presentation.item_id,
            response_text,
            widget.confidence,
        )

    def _mark_ready(
        self,
        presentation: ReviewItemPresentation,
        message: str,
    ) -> None:
        self._ready_identity = self._identity(presentation)
        self.study_status_label.setText(message)
        self._set_rating_enabled(True)

    def rate_selected(self, rating: ReviewRating) -> None:
        row = self.queue_list.currentRow()
        presentation = self._selected_presentation()
        if (
            presentation is None
            or not presentation.resolved
            or self._ready_identity != self._identity(presentation)
            or not 0 <= row < len(self._queue)
        ):
            return
        current = self._queue[row]
        self._repository.save_review_schedule(
            reschedule(current, rating, reviewed_at=datetime.now(UTC))
        )
        self.refresh_queue()

    def _selected_presentation(self) -> ReviewItemPresentation | None:
        row = self.queue_list.currentRow()
        if 0 <= row < len(self._presentations):
            return self._presentations[row]
        return None

    @staticmethod
    def _identity(
        item: ReviewItemPresentation,
    ) -> tuple[str, str, str, LearningItemKind]:
        return item.course_code, item.module_id, item.item_id, item.item_type

    def _set_rating_enabled(self, enabled: bool) -> None:
        for button in self._rating_buttons:
            button.setEnabled(enabled)

    def _clear_study_content(self) -> None:
        self._activity_widget = None
        while self._study_content_layout.count():
            item = self._study_content_layout.takeAt(0)
            if item is None:
                continue
            widget = item.widget()
            if widget is not None:
                widget.setParent(None)
                widget.deleteLater()

    def _update_mastery(
        self,
        course_code: str | None,
        module_id: str | None,
    ) -> None:
        records = self._catalog.modules(course_code)
        if module_id is not None:
            records = tuple(record for record in records if record.module_id == module_id)
        summaries = tuple(
            self._repository.module_progress(record.course_code, record.module_id)
            for record in records
        )
        attempts = sum(summary.attempt_count for summary in summaries)
        if not attempts:
            self.mastery_label.setText(_COPY[self._locale]["mastery_none"])
            return
        correct = sum(summary.correct_count for summary in summaries)
        percent = round((correct / attempts) * 100)
        if module_id is not None and records:
            template = _COPY[self._locale]["mastery_module"]
            title = records[0].title
        elif course_code is not None:
            template = _COPY[self._locale]["mastery_course"]
            title = course_title(self._locale, course_code)
        else:
            template = _COPY[self._locale]["mastery_semester"]
            title = ""
        self.mastery_label.setText(template.format(title=title, percent=percent))

    def _update_history(
        self,
        course_code: str | None,
        module_id: str | None,
        kind: LearningItemKind | None,
    ) -> None:
        attempts = self._repository.list_attempts(
            course_code=course_code,
            module_id=module_id,
            limit=50,
        )
        if kind is not None:
            attempts = tuple(item for item in attempts if item.item_kind is kind)
        attempts = attempts[:8]
        if not attempts:
            self.history_label.setText(_COPY[self._locale]["history_empty"])
            return
        rows: list[str] = []
        for attempt in attempts:
            presentation = self._resolver.resolve_attempt(attempt)
            if attempt.is_correct is True:
                result = localized_result(self._locale, "correct")
            elif attempt.is_correct is False:
                result = localized_result(self._locale, "incorrect")
            else:
                result = localized_result(self._locale, attempt.outcome.value)
            rows.append(
                f"{localized_datetime(self._locale, attempt.created_at)} · "
                f"{presentation.display_title} · {presentation.course_title} · "
                f"{presentation.module_title} · {result}"
            )
        self.history_label.setText("\n".join(rows))

    def _update_recommendations(
        self,
        course_code: str | None,
        module_id: str | None,
        kind: LearningItemKind | None,
    ) -> None:
        now = datetime.now(UTC)
        attempts = self._repository.list_attempts(
            course_code=course_code,
            module_id=module_id,
            limit=500,
        )
        if kind is not None:
            attempts = tuple(item for item in attempts if item.item_kind is kind)
        failures = tuple(item for item in attempts if item.is_correct is False)
        values: dict[RecommendationCategory, list[str]] = {
            category: [] for category in RecommendationCategory
        }
        self._summary_targets.clear()

        for item in self._presentations[:3]:
            values[RecommendationCategory.TODAY].append(
                f"{item.display_title} — {item.review_reason}"
            )
        if self._presentations:
            first = self._presentations[0]
            self._summary_targets[RecommendationCategory.TODAY] = (
                first.course_code,
                first.module_id,
                first.item_id,
            )

        failure_by_module = Counter((item.course_code, item.module_id) for item in failures)
        for (failed_course, failed_module), count in failure_by_module.most_common(3):
            title = self._module_title(failed_course, failed_module)
            values[RecommendationCategory.REINFORCE].append(
                _COPY[self._locale]["errors"].format(title=title, count=count)
            )
            self._summary_targets.setdefault(
                RecommendationCategory.REINFORCE,
                (failed_course, failed_module, ""),
            )

        failure_counts = Counter(
            (item.course_code, item.module_id, item.item_id) for item in failures
        )
        seen_failures: set[tuple[str, str, str]] = set()
        for attempt in failures:
            identity = (attempt.course_code, attempt.module_id, attempt.item_id)
            if identity in seen_failures:
                continue
            seen_failures.add(identity)
            presentation = self._resolver.resolve_attempt(attempt)
            values[RecommendationCategory.FAILED_QUESTIONS].append(
                _COPY[self._locale]["failed_attempts"].format(
                    title=presentation.display_title,
                    count=failure_counts[identity],
                )
            )
            self._summary_targets.setdefault(
                RecommendationCategory.FAILED_QUESTIONS,
                identity,
            )
            if len(values[RecommendationCategory.FAILED_QUESTIONS]) >= 3:
                break

        if kind in {None, LearningItemKind.FLASHCARD}:
            due_cards = tuple(
                item
                for item in self._repository.list_flashcard_progress(
                    course_code=course_code,
                    module_id=module_id,
                )
                if item.due_at <= now
            )
            cards_by_module: dict[tuple[str, str], list[str]] = {}
            for progress in due_cards:
                card = next(
                    (
                        candidate
                        for candidate in self._catalog.flashcards(
                            course_code=progress.course_code,
                            module_id=progress.module_id,
                        )
                        if candidate.card_id == progress.card_id
                    ),
                    None,
                )
                if card is not None:
                    cards_by_module.setdefault(
                        (progress.course_code, progress.module_id), []
                    ).append(shortened(card.front, 56))
            for (card_course, card_module), titles in tuple(
                sorted(
                    cards_by_module.items(),
                    key=lambda item: (-len(item[1]), item[0]),
                )
            )[:3]:
                values[RecommendationCategory.PENDING_CARDS].append(
                    _COPY[self._locale]["cards"].format(
                        count=len(titles),
                        titles=", ".join(titles[:3]),
                    )
                )
                self._summary_targets.setdefault(
                    RecommendationCategory.PENDING_CARDS,
                    (card_course, card_module, ""),
                )

        if attempts:
            latest = attempts[0]
            latest_presentation = self._resolver.resolve_attempt(latest)
            values[RecommendationCategory.CONTINUE].append(
                _COPY[self._locale]["last_activity"].format(
                    title=latest_presentation.display_title,
                    module=latest_presentation.module_title,
                    date=localized_datetime(self._locale, latest.created_at),
                )
            )
            self._summary_targets[RecommendationCategory.CONTINUE] = (
                latest.course_code,
                latest.module_id,
                latest.item_id,
            )

        active_course_codes = (
            (course_code,) if course_code is not None else self._catalog.course_codes
        )
        for active_course in active_course_codes:
            summaries = tuple(
                self._repository.module_progress(record.course_code, record.module_id)
                for record in self._catalog.modules(active_course)
                if module_id is None or record.module_id == module_id
            )
            attempt_count = sum(item.attempt_count for item in summaries)
            title = course_title(self._locale, active_course)
            if not attempt_count:
                text = _COPY[self._locale]["no_attempts"].format(title=title)
            else:
                correct_count = sum(item.correct_count for item in summaries)
                text = _COPY[self._locale]["course_progress"].format(
                    title=title,
                    percent=round(100 * correct_count / attempt_count),
                    count=attempt_count,
                )
            values[RecommendationCategory.COURSE_PROGRESS].append(text)

        empty_copy = {
            RecommendationCategory.TODAY: "today_empty",
            RecommendationCategory.REINFORCE: "reinforce_empty",
            RecommendationCategory.FAILED_QUESTIONS: "failed_empty",
            RecommendationCategory.PENDING_CARDS: "cards_empty",
            RecommendationCategory.CONTINUE: "continue_empty",
            RecommendationCategory.COURSE_PROGRESS: "progress_empty",
        }
        for category, label in self._recommendation_labels.items():
            entries = values[category]
            label.setText(
                "\n".join(f"• {value}" for value in entries[:4])
                if entries
                else _COPY[self._locale][empty_copy[category]]
            )

    def _module_title(self, course_code: str, module_id: str) -> str:
        try:
            return self._catalog.module(course_code, module_id).title
        except KeyError:
            return _COPY[self._locale]["unavailable"].split(".")[0]

    def _activate_summary(self, category: RecommendationCategory) -> None:
        target = self._summary_targets.get(category)
        if target is None:
            return
        course_code, module_id, item_id = target
        if category is RecommendationCategory.PENDING_CARDS:
            self.flashcards_requested.emit(course_code, module_id)
            return
        if category is RecommendationCategory.FAILED_QUESTIONS:
            for index, presentation in enumerate(self._presentations):
                if (
                    presentation.course_code,
                    presentation.module_id,
                    presentation.item_id,
                ) == target:
                    self.queue_list.setCurrentRow(index)
                    return
            self.assessments_requested.emit(course_code, module_id)
            return
        self.module_requested.emit(course_code, module_id)


__all__ = ["ReviewPage"]
