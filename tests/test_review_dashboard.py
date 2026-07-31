from __future__ import annotations

import sqlite3
from datetime import UTC, datetime, timedelta
from pathlib import Path

import pytest
from PySide6.QtCore import QSettings
from PySide6.QtWidgets import QApplication, QLabel, QPushButton

from computational_biomedicine_study_hub.courses.dm847 import DM847Page
from computational_biomedicine_study_hub.i18n import AppLocale
from computational_biomedicine_study_hub.learning.progress import (
    AttemptRecord,
    ConfidenceLevel,
)
from computational_biomedicine_study_hub.storage import SQLiteProgressStore
from computational_biomedicine_study_hub.ui.main_window import MainWindow
from computational_biomedicine_study_hub.ui.pages.review_page import ReviewPage
from computational_biomedicine_study_hub.ui.routes import RouteId

_NOW = datetime(2026, 7, 31, 1, 0, tzinfo=UTC)


def _attempt(
    attempt_id: str,
    *,
    course_code: str = "DM847",
    module_id: str = "dm847.m01",
    objective_id: str = "m01.o1",
    attempted_at: datetime = _NOW - timedelta(days=2),
) -> AttemptRecord:
    return AttemptRecord(
        attempt_id=attempt_id,
        course_code=course_code,
        module_id=module_id,
        objective_id=objective_id,
        item_id=f"{module_id}.bank.test",
        activity_type="multiple_choice",
        answer="option_a",
        is_correct=False,
        confidence=ConfidenceLevel.HIGH,
        hints_used=0,
        response_time_ms=2500,
        solution_revealed=False,
        attempted_at=attempted_at,
    )


def test_mastery_identity_is_scoped_by_course_and_module() -> None:
    with SQLiteProgressStore(":memory:") as store:
        dm847 = store.record_and_update(_attempt("attempt-dm847"))
        dm857 = store.record_and_update(
            _attempt(
                "attempt-dm857",
                course_code="DM857",
                module_id="dm857.m01",
            )
        )

        assert store.get_mastery("m01.o1", course_code="DM847", module_id="dm847.m01") == dm847
        assert store.get_mastery("m01.o1", course_code="DM857", module_id="dm857.m01") == dm857
        with pytest.raises(ValueError, match="ambiguous"):
            store.get_mastery("m01.o1")

        due = store.due_reviews(_NOW)

    assert tuple(item.key for item in due) == (
        ("DM847", "dm847.m01", "m01.o1"),
        ("DM857", "dm857.m01", "m01.o1"),
    )


def test_schema_v1_is_migrated_without_losing_mastery(tmp_path: Path) -> None:
    database = tmp_path / "legacy.sqlite3"
    attempted_at = (_NOW - timedelta(days=2)).isoformat()
    next_review_at = (_NOW - timedelta(days=1)).isoformat()
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
            objective_id TEXT PRIMARY KEY,
            mastery_score REAL NOT NULL,
            attempts INTEGER NOT NULL,
            consecutive_correct INTEGER NOT NULL,
            lapse_count INTEGER NOT NULL,
            last_attempt_at TEXT NOT NULL,
            next_review_at TEXT NOT NULL
        );
        PRAGMA user_version = 1;
        """
    )
    connection.execute(
        "INSERT INTO attempts VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
        (
            "legacy-attempt",
            "DM847",
            "dm847.m01",
            "m01.o1",
            "legacy-item",
            "multiple_choice",
            "option_a",
            0,
            "high",
            0,
            1000,
            0,
            attempted_at,
        ),
    )
    connection.execute(
        "INSERT INTO mastery VALUES (?, ?, ?, ?, ?, ?, ?)",
        ("m01.o1", 0.2, 1, 0, 1, attempted_at, next_review_at),
    )
    connection.commit()
    connection.close()

    with SQLiteProgressStore(database) as store:
        assert store.schema_version == 3
        state = store.get_mastery("m01.o1", course_code="DM847", module_id="dm847.m01")
        due = store.due_reviews(_NOW)
        assert store.list_errors() == ()

    assert state is not None
    assert state.mastery_score == pytest.approx(0.2)
    assert tuple(item.key for item in due) == (("DM847", "dm847.m01", "m01.o1"),)


def test_review_page_renders_localized_due_objective(qapp: QApplication) -> None:
    with SQLiteProgressStore(":memory:") as store:
        store.record_and_update(_attempt("review-attempt"))
        page = ReviewPage(
            store,
            AppLocale.SPANISH_SPAIN,
            clock=lambda: _NOW,
        )

        assert page.due_count == 1
        assert page.review_items[0].key == ("DM847", "dm847.m01", "m01.o1")
        objective = page.findChild(QLabel, "reviewObjectiveStatement")
        assert objective is not None
        assert "dogma central" in objective.text().casefold()

        received: list[tuple[str, str, str]] = []
        page.review_requested.connect(
            lambda course, module, objective_id: received.append((course, module, objective_id))
        )
        button = page.findChild(QPushButton, "reviewOpenModuleButton")
        assert button is not None
        button.click()

        assert received == [("DM847", "dm847.m01", "m01.o1")]


def test_review_page_has_a_real_empty_state(qapp: QApplication) -> None:
    with SQLiteProgressStore(":memory:") as store:
        page = ReviewPage(store, AppLocale.ENGLISH, clock=lambda: _NOW)

        assert page.due_count == 0
        empty_title = page.findChild(QLabel, "reviewEmptyTitle")
        assert empty_title is not None
        assert empty_title.text() == "No reviews are due"


def test_review_action_opens_the_module_assessment(
    qapp: QApplication,
    tmp_path: Path,
) -> None:
    settings = QSettings(str(tmp_path / "settings.ini"), QSettings.Format.IniFormat)
    with SQLiteProgressStore(":memory:") as store:
        store.record_and_update(_attempt("window-review-attempt"))
        window = MainWindow(settings=settings, progress_store=store)
        window.navigate(RouteId.REVIEW)

        review_page = window.findChild(ReviewPage, "reviewPage")
        assert review_page is not None
        button = review_page.findChild(QPushButton, "reviewOpenModuleButton")
        assert button is not None
        button.click()

        assert window.current_route == "course/dm847"
        course_page = window.findChild(DM847Page, "dm847CoursePage")
        assert course_page is not None
        assert course_page.current_module_index == 0
        assert course_page.reader.current_section_index == 4
