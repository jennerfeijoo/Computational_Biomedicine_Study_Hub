"""PySide6 integration tests for the DM847 written-assessment studio."""

from __future__ import annotations

from collections.abc import Callable
from dataclasses import dataclass, field

from PySide6.QtWidgets import QApplication, QTabWidget

from computational_biomedicine_study_hub.content.models import LearningModule
from computational_biomedicine_study_hub.i18n import AppLocale
from computational_biomedicine_study_hub.learning.dm847_written_assessment import (
    WrittenFeedbackMode,
)
from computational_biomedicine_study_hub.storage import SQLiteProgressStore
from computational_biomedicine_study_hub.tutoring import (
    WrittenFeedbackRequest,
    WrittenFeedbackResponse,
)
from computational_biomedicine_study_hub.ui.main_window import MainWindow
from computational_biomedicine_study_hub.ui.pages.assessments_page import AssessmentsPage
from computational_biomedicine_study_hub.ui.pages.dm847_written_assessment_page import (
    DM847WrittenAssessmentPage,
)
from computational_biomedicine_study_hub.ui.pages.dm857_capstone_page import DM857CapstonePage
from computational_biomedicine_study_hub.ui.routes import RouteId


@dataclass
class FakeWrittenRunner:
    model: str = "local-test-model"
    requests: list[WrittenFeedbackRequest] = field(default_factory=list)

    def generate(
        self,
        module: LearningModule,
        request: WrittenFeedbackRequest,
    ) -> WrittenFeedbackResponse:
        self.requests.append(request)
        return WrittenFeedbackResponse(
            content=(
                f"Feedback for {request.prompt_id}: retain the valid design and expand limitations "
                f"[{module.module_id}.overview]."
            ),
            source_ids=(f"{module.module_id}.overview",),
            model=self.model,
            mode=request.mode,
        )


class ImmediateExecutor:
    def submit(
        self,
        request_id: int,
        task: Callable[[], WrittenFeedbackResponse],
        on_success: Callable[[int, WrittenFeedbackResponse], None],
        on_failure: Callable[[int, Exception], None],
    ) -> None:
        try:
            response = task()
        except Exception as exc:  # pragma: no cover - defensive test executor boundary
            on_failure(request_id, exc)
        else:
            on_success(request_id, response)

    def cancel(self, request_id: int) -> None:
        del request_id


def _long_draft() -> str:
    return " ".join(
        (
            "The patient is the independent experimental unit and all repeated samples remain in "
            "the same split. Filtering, transformation, imputation, scaling, and feature selection "
            "are fitted only on training data. Grouped nested validation separates hyperparameter "
            "selection from performance estimation. The final test set is evaluated once after the "
            "pipeline is frozen. Results include discrimination, calibration, uncertainty, error "
            "analysis, limitations, and reproducible code and environment records."
        ).split()
    )


def test_written_page_generates_and_persists_source_traceable_feedback(
    qapp: QApplication,
) -> None:
    del qapp
    progress_store = SQLiteProgressStore(":memory:")
    runner = FakeWrittenRunner()
    page = DM847WrittenAssessmentPage(
        progress_store,
        AppLocale.ENGLISH,
        feedback_runner=runner,
        executor=ImmediateExecutor(),
    )
    assert page.select_prompt("dm847.w10")
    page.draft_editor.setPlainText(_long_draft())

    page.request_feedback(WrittenFeedbackMode.CONTENT_REVIEW)
    page.persist()

    assert runner.requests
    assert runner.requests[-1].prompt_id == "dm847.w10"
    assert "Feedback for dm847.w10" in page.feedback_text
    assert page.snapshot.draft("dm847.w10").source_ids == ("dm847.m10.overview",)

    restored = DM847WrittenAssessmentPage(
        progress_store,
        AppLocale.DANISH_DENMARK,
        feedback_runner=FakeWrittenRunner(),
        executor=ImmediateExecutor(),
    )
    assert restored.current_prompt_id == "dm847.w10"
    assert "patient" in restored.draft_editor.toPlainText()
    assert "Feedback for dm847.w10" in restored.feedback_text
    progress_store.close()


def test_editing_a_reviewed_draft_invalidates_stale_feedback(qapp: QApplication) -> None:
    del qapp
    progress_store = SQLiteProgressStore(":memory:")
    page = DM847WrittenAssessmentPage(
        progress_store,
        AppLocale.ENGLISH,
        feedback_runner=FakeWrittenRunner(),
        executor=ImmediateExecutor(),
    )
    page.draft_editor.setPlainText(_long_draft())
    page.request_feedback(WrittenFeedbackMode.WRITING_REVISION)
    assert page.feedback_text

    page.draft_editor.appendPlainText("This sentence changes the learner-owned draft.")

    assert page.feedback_text == ""
    assert page.snapshot.draft(page.current_prompt_id).feedback_mode is None
    progress_store.close()


def test_switching_tasks_keeps_each_learner_draft_under_its_prompt(
    qapp: QApplication,
) -> None:
    del qapp
    progress_store = SQLiteProgressStore(":memory:")
    page = DM847WrittenAssessmentPage(
        progress_store,
        AppLocale.ENGLISH,
        feedback_runner=FakeWrittenRunner(),
        executor=ImmediateExecutor(),
    )
    first_text = "The first response defines molecular representation and coordinate assumptions."
    second_text = "The second response records database versions, identifiers, and provenance."

    page.draft_editor.setPlainText(first_text)
    assert page.select_prompt("dm847.w02")
    page.draft_editor.setPlainText(second_text)
    assert page.select_prompt("dm847.w01")

    assert page.draft_editor.toPlainText() == first_text
    assert page.snapshot.draft("dm847.w01").response_text == first_text
    assert page.snapshot.draft("dm847.w02").response_text == second_text
    progress_store.close()


def test_assessments_route_hosts_dm847_writing_and_dm857_project(
    qapp: QApplication,
) -> None:
    del qapp
    progress_store = SQLiteProgressStore(":memory:")
    window = MainWindow(progress_store=progress_store)

    window.navigate(RouteId.ASSESSMENTS)

    assert window.current_route is RouteId.ASSESSMENTS
    hub = window.findChild(AssessmentsPage, "assessmentsPage")
    tabs = window.findChild(QTabWidget, "assessmentCourseTabs")
    assert hub is not None
    assert tabs is not None
    assert tabs.count() == 2
    assert window.findChild(DM847WrittenAssessmentPage, "dm847WrittenAssessmentPage") is not None
    assert window.findChild(DM857CapstonePage, "dm857CapstonePage") is not None
    progress_store.close()
