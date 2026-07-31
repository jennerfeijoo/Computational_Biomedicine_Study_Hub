from __future__ import annotations

import sqlite3
from datetime import UTC, datetime, timedelta
from pathlib import Path

import pytest
from PySide6.QtWidgets import QApplication, QLabel, QPushButton

from computational_biomedicine_study_hub.i18n import AppLocale
from computational_biomedicine_study_hub.learning.progress import (
    ConfidenceLevel,
    ErrorKind,
)
from computational_biomedicine_study_hub.learning.progress_service import (
    LearningProgressService,
    ObjectiveAnswerSubmission,
)
from computational_biomedicine_study_hub.storage import SQLiteProgressStore
from computational_biomedicine_study_hub.ui.pages.review_page import ReviewPage

_NOW = datetime(2026, 7, 31, 2, 0, tzinfo=UTC)


def _submission(
    *,
    is_correct: bool,
    confidence: ConfidenceLevel = ConfidenceLevel.HIGH,
    attempted_at: datetime = _NOW,
) -> ObjectiveAnswerSubmission:
    selected_answer = (
        "DNA can be transcribed into RNA." if is_correct else "DNA can only be copied into DNA."
    )
    return ObjectiveAnswerSubmission(
        course_code="DM847",
        module_id="dm847.m01",
        item_id="dm847.m01.bank.001",
        activity_type="multiple_choice",
        answer="option_b" if is_correct else "option_a",
        is_correct=is_correct,
        confidence=confidence,
        response_time_ms=4200,
        objective_ids=("m01.o1", "m01.o2"),
        attempted_at=attempted_at,
        prompt="Which statement best represents molecular information flow?",
        selected_answer=selected_answer,
        correct_answer="DNA can be transcribed into RNA.",
        explanation="Transcription produces RNA from a DNA template.",
    )


def test_incorrect_submission_creates_one_error_for_multiple_objectives() -> None:
    attempt_ids = iter(("attempt-1", "attempt-2"))
    with SQLiteProgressStore(":memory:") as store:
        service = LearningProgressService(
            store,
            attempt_id_factory=lambda: next(attempt_ids),
            error_id_factory=lambda: "error-1",
        )

        service.record_objective_answer(_submission(is_correct=False))
        errors = store.list_errors()

    assert len(errors) == 1
    error = errors[0]
    assert error.error_id == "error-1"
    assert error.objective_ids == ("m01.o1", "m01.o2")
    assert error.kind is ErrorKind.MISCONCEPTION
    assert not error.is_resolved
    assert "Transcription" in error.explanation


def test_later_correct_answer_resolves_open_errors_for_the_same_item() -> None:
    attempt_ids = iter(("attempt-1", "attempt-2", "attempt-3", "attempt-4"))
    with SQLiteProgressStore(":memory:") as store:
        service = LearningProgressService(
            store,
            attempt_id_factory=lambda: next(attempt_ids),
            error_id_factory=lambda: "error-1",
        )
        service.record_objective_answer(_submission(is_correct=False))
        corrected_at = _NOW + timedelta(days=1)
        service.record_objective_answer(_submission(is_correct=True, attempted_at=corrected_at))

        errors = store.list_errors()
        unresolved = store.list_errors(include_resolved=False)

    assert len(errors) == 1
    assert errors[0].resolved_at == corrected_at
    assert errors[0].is_resolved
    assert unresolved == ()


def test_error_kind_distinguishes_uncertainty_from_misconception() -> None:
    attempt_ids = iter(("a1", "a2", "a3", "a4"))
    error_ids = iter(("e-low", "e-medium"))
    with SQLiteProgressStore(":memory:") as store:
        service = LearningProgressService(
            store,
            attempt_id_factory=lambda: next(attempt_ids),
            error_id_factory=lambda: next(error_ids),
        )
        service.record_objective_answer(
            _submission(is_correct=False, confidence=ConfidenceLevel.LOW)
        )
        service.record_objective_answer(
            _submission(
                is_correct=False,
                confidence=ConfidenceLevel.MEDIUM,
                attempted_at=_NOW + timedelta(minutes=1),
            )
        )
        errors = store.list_errors()

    assert errors[0].kind is ErrorKind.FRAGILE_UNDERSTANDING
    assert errors[1].kind is ErrorKind.KNOWLEDGE_GAP


def test_error_creation_rolls_back_with_duplicate_attempt_ids() -> None:
    with SQLiteProgressStore(":memory:") as store:
        service = LearningProgressService(
            store,
            attempt_id_factory=lambda: "duplicate",
            error_id_factory=lambda: "error-1",
        )

        with pytest.raises(ValueError, match="duplicate attempt IDs"):
            service.record_objective_answer(_submission(is_correct=False))

        assert store.list_attempts() == ()
        assert store.list_errors() == ()


def test_schema_v2_is_upgraded_without_fabricating_error_history(tmp_path: Path) -> None:
    database = tmp_path / "v2.sqlite3"
    connection = sqlite3.connect(database)
    connection.executescript(
        """
        CREATE TABLE attempts (
            attempt_id TEXT PRIMARY KEY,
            course_code TEXT NOT NULL,
            module_id TEXT NOT NULL,
            objective_id TEXT NOT NULL,
            item_id TEXT NOT NULL,
            activity_type TEXT NOT NULL,
            answer TEXT NOT NULL,
            is_correct INTEGER NOT NULL,
            confidence TEXT NOT NULL,
            hints_used INTEGER NOT NULL,
            response_time_ms INTEGER NOT NULL,
            solution_revealed INTEGER NOT NULL,
            attempted_at TEXT NOT NULL
        );
        CREATE TABLE mastery (
            course_code TEXT NOT NULL,
            module_id TEXT NOT NULL,
            objective_id TEXT NOT NULL,
            mastery_score REAL NOT NULL,
            attempts INTEGER NOT NULL,
            consecutive_correct INTEGER NOT NULL,
            lapse_count INTEGER NOT NULL,
            last_attempt_at TEXT NOT NULL,
            next_review_at TEXT NOT NULL,
            PRIMARY KEY (course_code, module_id, objective_id)
        );
        PRAGMA user_version = 2;
        """
    )
    connection.commit()
    connection.close()

    with SQLiteProgressStore(database) as store:
        assert store.schema_version == 3
        assert store.list_errors() == ()


def test_review_page_renders_error_context_and_routes_to_module(
    qapp: QApplication,
) -> None:
    attempt_ids = iter(("attempt-1", "attempt-2"))
    with SQLiteProgressStore(":memory:") as store:
        service = LearningProgressService(
            store,
            attempt_id_factory=lambda: next(attempt_ids),
            error_id_factory=lambda: "error-1",
        )
        service.record_objective_answer(_submission(is_correct=False))
        page = ReviewPage(store, AppLocale.SPANISH_SPAIN, clock=lambda: _NOW)

        assert page.error_count == 1
        assert page.open_error_count == 1
        prompt = page.findChild(QLabel, "errorPrompt")
        status = page.findChild(QLabel, "errorStatus")
        kind = page.findChild(QLabel, "errorKind")
        assert prompt is not None
        assert status is not None
        assert kind is not None
        assert "molecular information flow" in prompt.text().casefold()
        assert status.text() == "Pendiente de corregir"
        assert "concepción errónea" in kind.text().casefold()

        received: list[tuple[str, str, str]] = []
        page.review_requested.connect(
            lambda course, module, objective: received.append((course, module, objective))
        )
        button = page.findChild(QPushButton, "errorOpenModuleButton")
        assert button is not None
        button.click()

    assert received == [("DM847", "dm847.m01", "m01.o1")]
