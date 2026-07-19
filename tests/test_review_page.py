from __future__ import annotations

from datetime import UTC, datetime, timedelta
from pathlib import Path

import pytest
from PySide6.QtWidgets import QLabel, QPushButton

from computational_biomedicine_study_hub.i18n import AppLocale
from computational_biomedicine_study_hub.learning.academic_catalog import (
    AcademicCatalog,
    CatalogModule,
)
from computational_biomedicine_study_hub.learning.progress import (
    AttemptOutcome,
    AttemptRecord,
    LearningItemKind,
    MasteryState,
    ReviewSchedule,
)
from computational_biomedicine_study_hub.learning.spaced_repetition import ReviewRating
from computational_biomedicine_study_hub.persistence import SQLiteProgressRepository
from computational_biomedicine_study_hub.ui.activities import (
    MultipleChoiceActivityWidget,
)
from computational_biomedicine_study_hub.ui.pages.review_page import ReviewPage
from computational_biomedicine_study_hub.ui.review_presentation import (
    localized_item_type,
    localized_result,
)


def _repository(tmp_path: Path) -> SQLiteProgressRepository:
    return SQLiteProgressRepository(tmp_path / "review.sqlite3")


def _module(catalog: AcademicCatalog) -> CatalogModule:
    return catalog.module("DM857", "dm857.m01")


def _schedule(
    item_id: str,
    kind: LearningItemKind,
    *,
    mastery: MasteryState = MasteryState.NEW,
) -> ReviewSchedule:
    return ReviewSchedule(
        course_code="DM857",
        module_id="dm857.m01",
        item_id=item_id,
        item_kind=kind,
        mastery_state=mastery,
        repetitions=0,
        interval_days=0,
        easiness=2.5,
        due_at=datetime.now(UTC) - timedelta(minutes=5),
    )


def _save_all_item_kinds(
    catalog: AcademicCatalog,
    repository: SQLiteProgressRepository,
) -> tuple[str, ...]:
    record = _module(catalog)
    card = catalog.flashcards(course_code="DM857", module_id=record.module_id)[0]
    concept = next(
        item for item in catalog.glossary(course_code="DM857") if item.module_id == record.module_id
    )
    objective = record.objective_question_bank[0]
    practice = record.learning_module.practice_exercises[2]
    identities = (
        (card.card_id, LearningItemKind.FLASHCARD),
        (concept.term_id, LearningItemKind.CONCEPT),
        (objective.item_id, LearningItemKind.ASSESSMENT),
        (practice.exercise_id, LearningItemKind.PRACTICE),
    )
    for item_id, kind in identities:
        repository.save_review_schedule(_schedule(item_id, kind))
    return tuple(item_id for item_id, _ in identities)


def _rating_buttons(page: ReviewPage) -> tuple[QPushButton, ...]:
    return tuple(
        button
        for button in page.findChildren(QPushButton)
        if button.objectName().startswith("reviewRating_")
    )


def test_review_resolves_every_item_kind_without_learner_facing_ids(
    qtbot,
    tmp_path: Path,
) -> None:
    catalog = AcademicCatalog(locale=AppLocale.SPANISH_SPAIN)
    repository = _repository(tmp_path)
    technical_ids = _save_all_item_kinds(catalog, repository)

    page = ReviewPage(catalog, repository, locale=AppLocale.SPANISH_SPAIN)
    qtbot.addWidget(page)

    assert {item.item_type for item in page.presentations} == set(LearningItemKind)
    assert all(item.resolved for item in page.presentations)
    assert {item.localized_type_label for item in page.presentations} == {
        "Tarjeta de memoria",
        "Concepto",
        "Pregunta de evaluación",
        "Ejercicio práctico",
    }
    visible_queue = "\n".join(
        page.queue_list.item(index).text() for index in range(page.queue_list.count())
    )
    assert "dm857.m01" not in visible_queue
    assert "p03" not in visible_queue
    assert "term." not in visible_queue
    assert all(item_id not in visible_queue for item_id in technical_ids)


def test_orphan_review_is_warned_and_cannot_be_rated(
    qtbot,
    tmp_path: Path,
    caplog: pytest.LogCaptureFixture,
) -> None:
    repository = _repository(tmp_path)
    orphan_id = "dm857.m01.bank.003"
    repository.save_review_schedule(_schedule(orphan_id, LearningItemKind.ASSESSMENT))

    with caplog.at_level("WARNING"):
        page = ReviewPage(
            AcademicCatalog(locale=AppLocale.SPANISH_SPAIN),
            repository,
            locale=AppLocale.SPANISH_SPAIN,
        )
    qtbot.addWidget(page)

    assert page.presentations[0].resolved is False
    assert page.queue_list.item(0).text().startswith("Contenido no disponible")
    assert orphan_id not in page.queue_list.item(0).text()
    assert all(not button.isEnabled() for button in _rating_buttons(page))
    page.rate_selected(ReviewRating.GOOD)
    assert (
        repository.get_review_schedule(
            "DM857",
            "dm857.m01",
            orphan_id,
            LearningItemKind.ASSESSMENT.value,
        )
        is not None
    )
    assert "Unresolved review reference" in caplog.text


def test_reveal_is_required_before_rating_and_rating_removes_due_item(
    qtbot,
    tmp_path: Path,
) -> None:
    catalog = AcademicCatalog(locale=AppLocale.SPANISH_SPAIN)
    repository = _repository(tmp_path)
    concept = next(
        item for item in catalog.glossary(course_code="DM857") if item.module_id == "dm857.m01"
    )
    schedule = _schedule(concept.term_id, LearningItemKind.CONCEPT)
    repository.save_review_schedule(schedule)
    page = ReviewPage(catalog, repository, locale=AppLocale.SPANISH_SPAIN)
    qtbot.addWidget(page)

    assert all(not button.isEnabled() for button in _rating_buttons(page))
    page.rate_selected(ReviewRating.GOOD)
    assert page.queue

    page.reveal_selected()
    explanation = page.findChild(QLabel, "reviewStudyExplanation")
    assert explanation is not None
    assert explanation.text() == concept.definition
    assert all(button.isEnabled() for button in _rating_buttons(page))

    page.rate_selected(ReviewRating.GOOD)
    assert page.queue == ()
    persisted = repository.get_review_schedule(
        schedule.course_code,
        schedule.module_id,
        schedule.item_id,
        schedule.item_kind.value,
    )
    assert persisted is not None
    assert persisted.due_at > datetime.now(UTC)


def test_objective_review_records_attempt_before_enabling_rating(
    qtbot,
    tmp_path: Path,
) -> None:
    catalog = AcademicCatalog(locale=AppLocale.ENGLISH)
    repository = _repository(tmp_path)
    question = _module(catalog).objective_question_bank[0]
    repository.save_review_schedule(
        _schedule(
            question.item_id,
            LearningItemKind.ASSESSMENT,
            mastery=MasteryState.LEARNING,
        )
    )
    page = ReviewPage(catalog, repository, locale=AppLocale.ENGLISH)
    qtbot.addWidget(page)
    widget = page.findChild(MultipleChoiceActivityWidget)
    assert widget is not None
    assert all(not button.isEnabled() for button in _rating_buttons(page))

    for control, option in zip(widget.option_controls, question.option_objects, strict=True):
        control.setChecked(option.option_id in question.correct_option_ids)
    widget.submit_answer()

    attempts = repository.list_attempts(item_id=question.item_id)
    assert len(attempts) == 1
    assert attempts[0].is_correct is True
    assert all(button.isEnabled() for button in _rating_buttons(page))

    page.rate_selected(ReviewRating.GOOD)
    assert page.queue == ()


def test_empty_states_mastery_and_course_progress_do_not_invent_measurements(
    qtbot,
    tmp_path: Path,
) -> None:
    page = ReviewPage(
        AcademicCatalog(locale=AppLocale.SPANISH_SPAIN),
        _repository(tmp_path),
        locale=AppLocale.SPANISH_SPAIN,
    )
    qtbot.addWidget(page)

    assert "Todavía no hay actividad suficiente" in page.mastery_label.text()
    progress = page.findChild(QLabel, "reviewReasons_course_progress")
    assert progress is not None
    assert "Sin intentos" in progress.text()
    assert "0 %" not in progress.text()
    all_summary_text = "\n".join(
        label.text()
        for label in page.findChildren(QLabel)
        if label.objectName().startswith("reviewReasons_")
    )
    assert "—" not in all_summary_text
    assert "No hay actividades vencidas." in all_summary_text
    assert "No hay preguntas falladas." in all_summary_text
    assert "No hay tarjetas pendientes." in all_summary_text
    assert page.history_label.text() == "Todavía no existe historial."


def test_mix_filter_disables_course_and_module_without_contradiction(
    qtbot,
    tmp_path: Path,
) -> None:
    page = ReviewPage(
        AcademicCatalog(locale=AppLocale.SPANISH_SPAIN),
        _repository(tmp_path),
        locale=AppLocale.SPANISH_SPAIN,
    )
    qtbot.addWidget(page)

    assert page.mix_courses.isChecked()
    assert not page.course_selector.isEnabled()
    assert not page.module_selector.isEnabled()
    assert page.course_selector.currentText() != page.course_selector.currentData()

    page.mix_courses.setChecked(False)
    assert page.course_selector.isEnabled()
    assert page.module_selector.isEnabled()


def test_add_new_concepts_respects_active_filters_and_never_duplicates(
    qtbot,
    tmp_path: Path,
) -> None:
    repository = _repository(tmp_path)
    page = ReviewPage(
        AcademicCatalog(locale=AppLocale.SPANISH_SPAIN),
        repository,
        locale=AppLocale.SPANISH_SPAIN,
    )
    qtbot.addWidget(page)
    page.mix_courses.setChecked(False)
    page.course_selector.setCurrentIndex(page.course_selector.findData("DM857"))
    page.module_selector.setCurrentIndex(page.module_selector.findData("dm857.m01"))
    page.kind_selector.setCurrentIndex(page.kind_selector.findData(LearningItemKind.CONCEPT.value))

    page.add_new_concepts()
    first_identities = {(item.course_code, item.module_id, item.item_id) for item in page.queue}
    assert first_identities
    assert all(
        course == "DM857" and module == "dm857.m01" for course, module, _ in first_identities
    )

    page.add_new_concepts()
    assert {
        (item.course_code, item.module_id, item.item_id) for item in page.queue
    } == first_identities


def test_locale_change_preserves_queue_ids_and_localizes_type_labels(
    qtbot,
    tmp_path: Path,
) -> None:
    repository = _repository(tmp_path)
    source = AcademicCatalog(locale=AppLocale.SPANISH_SPAIN)
    technical_ids = _save_all_item_kinds(source, repository)
    pages: list[ReviewPage] = []

    for locale in AppLocale:
        page = ReviewPage(
            AcademicCatalog(locale=locale),
            repository,
            locale=locale,
        )
        qtbot.addWidget(page)
        pages.append(page)
        assert tuple(item.item_id for item in page.queue) == tuple(
            item.item_id for item in page.presentations
        )
        assert set(item.item_id for item in page.presentations) == set(technical_ids)
        assert {item.localized_type_label for item in page.presentations} == {
            localized_item_type(locale, kind) for kind in LearningItemKind
        }

    assert pages[0].presentations[0].display_title != pages[1].presentations[0].display_title


def test_history_uses_human_title_and_translated_result(
    qtbot,
    tmp_path: Path,
) -> None:
    catalog = AcademicCatalog(locale=AppLocale.SPANISH_SPAIN)
    repository = _repository(tmp_path)
    question = _module(catalog).objective_question_bank[0]
    repository.record_attempt(
        AttemptRecord(
            attempt_id="attempt-review-history",
            course_code="DM857",
            module_id="dm857.m01",
            item_id=question.item_id,
            item_kind=LearningItemKind.ASSESSMENT,
            activity_type=question.activity_type,
            outcome=AttemptOutcome.REVIEW,
            locale=AppLocale.SPANISH_SPAIN.value,
            content_version=_module(catalog).content_version,
            created_at=datetime.now(UTC),
            is_correct=False,
            score=0.0,
        )
    )
    page = ReviewPage(catalog, repository, locale=AppLocale.SPANISH_SPAIN)
    qtbot.addWidget(page)

    assert shortened_prompt(question.prompt) in page.history_label.text()
    assert "Incorrecto" in page.history_label.text()
    assert question.item_id not in page.history_label.text()
    assert "dm857.m01" not in page.history_label.text()


def shortened_prompt(prompt: str) -> str:
    compact = " ".join(prompt.split())
    return compact if len(compact) <= 96 else f"{compact[:95].rstrip()}…"


@pytest.mark.parametrize(
    ("locale", "expected"),
    (
        (AppLocale.SPANISH_SPAIN, "Necesita repaso"),
        (AppLocale.ENGLISH, "Needs review"),
        (AppLocale.DANISH_DENMARK, "Kræver repetition"),
    ),
)
def test_all_persisted_results_are_localized(
    locale: AppLocale,
    expected: str,
) -> None:
    assert localized_result(locale, "review") == expected
    for value in (
        "partial",
        "solved",
        "correct",
        "incorrect",
        "again",
        "hard",
        "good",
        "easy",
    ):
        assert localized_result(locale, value) != value
