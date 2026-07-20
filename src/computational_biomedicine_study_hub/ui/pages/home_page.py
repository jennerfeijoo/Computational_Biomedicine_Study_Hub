"""Learner-centred semester dashboard and course selection page."""

from __future__ import annotations

from collections.abc import Iterable
from dataclasses import dataclass
from datetime import UTC, datetime

from PySide6.QtCore import Qt, Signal
from PySide6.QtWidgets import (
    QFrame,
    QGridLayout,
    QHBoxLayout,
    QLabel,
    QProgressBar,
    QPushButton,
    QScrollArea,
    QVBoxLayout,
    QWidget,
)

from ...courses.models import CourseRegistration
from ...i18n import AppLocale, MessageKey, Translator
from ...learning.academic_catalog import AcademicCatalog
from ...learning.progress import MasteryState
from ...learning.progress_repository import ProgressRepository
from ..design_system import apply_elevation


@dataclass(frozen=True, slots=True)
class DashboardCopy:
    eyebrow: str
    hero_title_active: str
    hero_title_empty: str
    hero_body: str
    continue_action: str
    review_action: str
    due_title: str
    due_caption: str
    modules_title: str
    modules_caption: str
    activity_title: str
    no_activity: str
    courses_title: str
    course_progress: str
    course_status: str
    attempts: str
    no_attempts: str


_DASHBOARD_COPY: dict[AppLocale, DashboardCopy] = {
    AppLocale.SPANISH_SPAIN: DashboardCopy(
        eyebrow="PLAN DE ESTUDIO",
        hero_title_active="Continúa desde donde lo dejaste",
        hero_title_empty="Tu semestre, organizado para aprender",
        hero_body=(
            "Accede al siguiente módulo, completa el repaso pendiente y mantén visible "
            "tu progreso en las cuatro asignaturas."
        ),
        continue_action="Continuar estudiando",
        review_action="Repasar ahora",
        due_title="Repaso de hoy",
        due_caption="actividades listas",
        modules_title="Módulos iniciados",
        modules_caption="de {total} módulos",
        activity_title="Actividad reciente",
        no_activity="Sin actividad registrada",
        courses_title="Asignaturas",
        course_progress="{progress}% de progreso estimado",
        course_status="{started}/{total} módulos iniciados · {pending} pendientes",
        attempts="{attempts} intentos · {success}% correctos",
        no_attempts="Sin intentos todavía",
    ),
    AppLocale.ENGLISH: DashboardCopy(
        eyebrow="STUDY PLAN",
        hero_title_active="Continue where you left off",
        hero_title_empty="Your semester, organised for learning",
        hero_body=(
            "Open the next module, complete due review and keep your progress across all "
            "four courses visible."
        ),
        continue_action="Continue studying",
        review_action="Review now",
        due_title="Review today",
        due_caption="activities ready",
        modules_title="Modules started",
        modules_caption="of {total} modules",
        activity_title="Recent activity",
        no_activity="No activity recorded",
        courses_title="Courses",
        course_progress="{progress}% estimated progress",
        course_status="{started}/{total} modules started · {pending} pending",
        attempts="{attempts} attempts · {success}% correct",
        no_attempts="No attempts yet",
    ),
    AppLocale.DANISH_DENMARK: DashboardCopy(
        eyebrow="STUDIEPLAN",
        hero_title_active="Fortsæt, hvor du slap",
        hero_title_empty="Dit semester, organiseret til læring",
        hero_body=(
            "Åbn det næste modul, gennemfør dagens repetition og følg din fremgang på "
            "tværs af alle fire kurser."
        ),
        continue_action="Fortsæt studiet",
        review_action="Repetér nu",
        due_title="Dagens repetition",
        due_caption="aktiviteter klar",
        modules_title="Påbegyndte moduler",
        modules_caption="af {total} moduler",
        activity_title="Seneste aktivitet",
        no_activity="Ingen aktivitet registreret",
        courses_title="Kurser",
        course_progress="{progress}% estimeret fremgang",
        course_status="{started}/{total} moduler påbegyndt · {pending} afventer",
        attempts="{attempts} forsøg · {success}% korrekte",
        no_attempts="Ingen forsøg endnu",
    ),
}


@dataclass(frozen=True, slots=True)
class CourseDashboardState:
    started_modules: int
    total_modules: int
    pending_reviews: int
    attempt_count: int
    correct_count: int
    progress_percent: int
    last_activity_at: datetime | None

    @property
    def success_percent(self) -> int:
        if not self.attempt_count:
            return 0
        return round(100 * self.correct_count / self.attempt_count)


class DashboardMetricCard(QFrame):
    """Compact metric with a large value and explicit interpretation."""

    def __init__(
        self,
        *,
        value: str,
        title: str,
        caption: str,
        parent: QWidget | None = None,
    ) -> None:
        super().__init__(parent)
        self.setObjectName("dashboardMetricCard")
        self.setMinimumHeight(118)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(18, 16, 18, 16)
        layout.setSpacing(4)

        value_label = QLabel(value)
        value_label.setObjectName("dashboardMetricValue")
        layout.addWidget(value_label)

        title_label = QLabel(title)
        title_label.setObjectName("dashboardMetricTitle")
        layout.addWidget(title_label)

        caption_label = QLabel(caption)
        caption_label.setObjectName("dashboardMetricCaption")
        caption_label.setWordWrap(True)
        layout.addWidget(caption_label)
        layout.addStretch(1)


class CourseCard(QFrame):
    """Clickable localized course card with evidence-based progress."""

    selected = Signal(str)

    def __init__(
        self,
        course: CourseRegistration,
        translator: Translator,
        state: CourseDashboardState,
        copy: DashboardCopy,
        parent: QWidget | None = None,
    ) -> None:
        super().__init__(parent)
        self.setObjectName("dashboardCourseCard")
        self.setProperty("courseCode", course.code)
        self.setMinimumHeight(260)
        apply_elevation(self, blur_radius=20, y_offset=4)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 18, 20, 18)
        layout.setSpacing(9)

        top_row = QHBoxLayout()
        code = QLabel(course.code)
        code.setObjectName("dashboardCourseCode")
        top_row.addWidget(code)
        top_row.addStretch(1)

        metadata = QLabel(
            translator.text(
                MessageKey.COURSE_METADATA,
                semester=course.semester,
                ects=course.ects,
            )
        )
        metadata.setObjectName("dashboardCourseMetadata")
        top_row.addWidget(metadata)
        layout.addLayout(top_row)

        title = QLabel(course.title_for(translator.locale))
        title.setObjectName("dashboardCourseTitle")
        title.setWordWrap(True)
        layout.addWidget(title)

        summary = QLabel(course.summary_for(translator.locale))
        summary.setObjectName("dashboardCourseSummary")
        summary.setWordWrap(True)
        summary.setMaximumHeight(48)
        layout.addWidget(summary)

        progress = QProgressBar()
        progress.setObjectName("dashboardCourseProgress")
        progress.setProperty("courseCode", course.code)
        progress.setRange(0, 100)
        progress.setValue(state.progress_percent)
        progress.setTextVisible(False)
        progress.setAccessibleName(copy.course_progress.format(progress=state.progress_percent))
        layout.addWidget(progress)

        progress_text = QLabel(copy.course_progress.format(progress=state.progress_percent))
        progress_text.setObjectName("dashboardCourseStatus")
        layout.addWidget(progress_text)

        status = QLabel(
            copy.course_status.format(
                started=state.started_modules,
                total=state.total_modules,
                pending=state.pending_reviews,
            )
        )
        status.setObjectName("dashboardCourseStatus")
        status.setWordWrap(True)
        layout.addWidget(status)

        attempts_text = (
            copy.attempts.format(
                attempts=state.attempt_count,
                success=state.success_percent,
            )
            if state.attempt_count
            else copy.no_attempts
        )
        attempts = QLabel(attempts_text)
        attempts.setObjectName("dashboardCourseStatus")
        layout.addWidget(attempts)
        layout.addStretch(1)

        open_button = QPushButton(translator.text(MessageKey.COURSE_OPEN))
        open_button.setObjectName("dashboardSecondaryAction")
        open_button.setCursor(Qt.CursorShape.PointingHandCursor)
        open_button.clicked.connect(
            lambda checked=False, route=course.route: self.selected.emit(route)
        )
        layout.addWidget(open_button)


class HomePage(QWidget):
    """Display a dynamic semester dashboard and emit study-navigation requests."""

    course_selected = Signal(str)
    module_selected = Signal(str, str)
    review_selected = Signal()

    def __init__(
        self,
        courses: Iterable[CourseRegistration],
        translator: Translator,
        parent: QWidget | None = None,
        *,
        catalog: AcademicCatalog | None = None,
        repository: ProgressRepository | None = None,
    ) -> None:
        super().__init__(parent)
        self.setObjectName("homeDashboardPage")
        course_list = tuple(courses)
        copy = _DASHBOARD_COPY[translator.locale]

        root_layout = QVBoxLayout(self)
        root_layout.setContentsMargins(0, 0, 0, 0)

        scroll = QScrollArea()
        scroll.setObjectName("dashboardScroll")
        scroll.setWidgetResizable(True)
        scroll.setFrameShape(QFrame.Shape.NoFrame)

        body = QWidget()
        body.setObjectName("dashboardBody")
        layout = QVBoxLayout(body)
        layout.setContentsMargins(2, 2, 10, 18)
        layout.setSpacing(18)

        states = {
            course.code: _course_state(course.code, catalog, repository) for course in course_list
        }
        latest = _latest_attempt(repository)
        latest_module_title = _module_title(catalog, latest[0], latest[1]) if latest else ""
        due_count = _due_count(repository)
        started_modules = sum(state.started_modules for state in states.values())
        total_modules = sum(state.total_modules for state in states.values())
        last_activity = max(
            (state.last_activity_at for state in states.values() if state.last_activity_at is not None),
            default=None,
        )

        hero = QFrame()
        hero.setObjectName("dashboardHero")
        hero_layout = QHBoxLayout(hero)
        hero_layout.setContentsMargins(24, 22, 24, 22)
        hero_layout.setSpacing(20)

        hero_copy = QVBoxLayout()
        hero_copy.setSpacing(7)
        eyebrow = QLabel(copy.eyebrow)
        eyebrow.setObjectName("dashboardEyebrow")
        hero_copy.addWidget(eyebrow)

        title = QLabel(copy.hero_title_active if latest else copy.hero_title_empty)
        title.setObjectName("dashboardHeroTitle")
        title.setWordWrap(True)
        hero_copy.addWidget(title)

        body_text = copy.hero_body
        if latest_module_title:
            body_text = f"{latest_module_title}\n{body_text}"
        hero_body = QLabel(body_text)
        hero_body.setObjectName("dashboardHeroBody")
        hero_body.setWordWrap(True)
        hero_copy.addWidget(hero_body)

        actions = QHBoxLayout()
        continue_button = QPushButton(copy.continue_action)
        continue_button.setObjectName("dashboardPrimaryAction")
        continue_button.setCursor(Qt.CursorShape.PointingHandCursor)
        if latest is not None:
            continue_button.clicked.connect(
                lambda checked=False, context=latest: self.module_selected.emit(*context)
            )
        elif course_list:
            continue_button.clicked.connect(
                lambda checked=False, route=course_list[0].route: self.course_selected.emit(route)
            )
        actions.addWidget(continue_button)

        review_button = QPushButton(
            f"{copy.review_action} · {due_count}" if due_count else copy.review_action
        )
        review_button.setObjectName("dashboardReviewAction")
        review_button.setCursor(Qt.CursorShape.PointingHandCursor)
        review_button.clicked.connect(lambda checked=False: self.review_selected.emit())
        actions.addWidget(review_button)
        actions.addStretch(1)
        hero_copy.addLayout(actions)
        hero_layout.addLayout(hero_copy, 1)

        due_visual = QLabel(str(due_count))
        due_visual.setObjectName("dashboardMetricValue")
        due_visual.setAlignment(Qt.AlignmentFlag.AlignCenter)
        due_visual.setMinimumWidth(90)
        due_visual.setToolTip(copy.due_title)
        hero_layout.addWidget(due_visual)
        apply_elevation(hero, blur_radius=28, y_offset=7)
        layout.addWidget(hero)

        metrics = QHBoxLayout()
        metrics.setSpacing(12)
        metrics.addWidget(
            DashboardMetricCard(
                value=str(due_count),
                title=copy.due_title,
                caption=copy.due_caption,
            ),
            1,
        )
        metrics.addWidget(
            DashboardMetricCard(
                value=str(started_modules),
                title=copy.modules_title,
                caption=copy.modules_caption.format(total=total_modules),
            ),
            1,
        )
        metrics.addWidget(
            DashboardMetricCard(
                value=_format_activity(last_activity, translator.locale),
                title=copy.activity_title,
                caption=copy.no_activity if last_activity is None else _format_time(last_activity),
            ),
            1,
        )
        layout.addLayout(metrics)

        course_heading = QLabel(copy.courses_title)
        course_heading.setObjectName("dashboardSectionTitle")
        layout.addWidget(course_heading)

        grid = QGridLayout()
        grid.setHorizontalSpacing(14)
        grid.setVerticalSpacing(14)
        grid.setColumnStretch(0, 1)
        grid.setColumnStretch(1, 1)

        for index, course in enumerate(course_list):
            card = CourseCard(course, translator, states[course.code], copy)
            card.selected.connect(self.course_selected.emit)
            grid.addWidget(card, index // 2, index % 2)

        layout.addLayout(grid)
        layout.addStretch(1)
        scroll.setWidget(body)
        root_layout.addWidget(scroll)


def _course_state(
    course_code: str,
    catalog: AcademicCatalog | None,
    repository: ProgressRepository | None,
) -> CourseDashboardState:
    if catalog is None:
        return CourseDashboardState(0, 0, 0, 0, 0, 0, None)

    modules = catalog.modules(course_code)
    if repository is None:
        return CourseDashboardState(0, len(modules), 0, 0, 0, 0, None)

    started = 0
    pending = 0
    attempts = 0
    correct = 0
    last_activity: datetime | None = None
    mastery_total = 0.0
    mastery_weight = {
        MasteryState.NEW: 0.0,
        MasteryState.LEARNING: 0.35,
        MasteryState.REVIEWING: 0.60,
        MasteryState.MASTERED: 1.0,
    }

    for module in modules:
        progress = repository.module_progress(course_code, module.module_id)
        attempts += progress.attempt_count
        correct += progress.correct_count
        pending += progress.pending_review_count
        mastery_total += mastery_weight[progress.mastery_state]
        if progress.attempt_count or progress.pending_review_count or progress.last_activity_at:
            started += 1
        if progress.last_activity_at is not None and (
            last_activity is None or progress.last_activity_at > last_activity
        ):
            last_activity = progress.last_activity_at

    progress_percent = round(100 * mastery_total / len(modules)) if modules else 0
    return CourseDashboardState(
        started_modules=started,
        total_modules=len(modules),
        pending_reviews=pending,
        attempt_count=attempts,
        correct_count=correct,
        progress_percent=progress_percent,
        last_activity_at=last_activity,
    )


def _latest_attempt(repository: ProgressRepository | None) -> tuple[str, str] | None:
    if repository is None:
        return None
    attempts = repository.list_attempts(limit=1)
    if not attempts:
        return None
    return attempts[0].course_code, attempts[0].module_id


def _due_count(repository: ProgressRepository | None) -> int:
    if repository is None:
        return 0
    return len(repository.list_due_reviews(due_at=datetime.now(UTC)))


def _module_title(
    catalog: AcademicCatalog | None,
    course_code: str,
    module_id: str,
) -> str:
    if catalog is None:
        return ""
    try:
        return catalog.module(course_code, module_id).title
    except KeyError:
        return ""


def _format_activity(value: datetime | None, locale: AppLocale) -> str:
    if value is None:
        return "—"
    local_value = value.astimezone()
    today = datetime.now().astimezone().date()
    if local_value.date() == today:
        return local_value.strftime("%H:%M")
    if locale is AppLocale.ENGLISH:
        return local_value.strftime("%b %d")
    return local_value.strftime("%d/%m")


def _format_time(value: datetime) -> str:
    return value.astimezone().strftime("%Y-%m-%d · %H:%M")
