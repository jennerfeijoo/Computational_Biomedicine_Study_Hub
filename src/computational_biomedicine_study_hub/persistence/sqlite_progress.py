"""Versioned SQLite adapter for language-independent learning progress."""

from __future__ import annotations

import json
import sqlite3
from collections.abc import Iterator
from contextlib import contextmanager
from datetime import UTC, datetime
from pathlib import Path
from threading import Lock

from ..learning.activity_types import ActivityType
from ..learning.progress import (
    AssessmentScope,
    AssessmentSession,
    AttemptOutcome,
    AttemptRecord,
    FlashcardProgress,
    LearningItemKind,
    MasteryState,
    ModuleProgress,
    PracticeProgress,
    ReviewSchedule,
    require_aware,
)

SCHEMA_VERSION = 1


def _dump_ids(values: tuple[str, ...]) -> str:
    return json.dumps(values, ensure_ascii=False, separators=(",", ":"))


def _load_ids(value: str) -> tuple[str, ...]:
    decoded = json.loads(value)
    if not isinstance(decoded, list) or not all(isinstance(item, str) for item in decoded):
        raise ValueError("Persisted identifier list is invalid.")
    return tuple(decoded)


def _dump_datetime(value: datetime | None) -> str | None:
    if value is None:
        return None
    require_aware(value, "persisted datetime")
    return value.isoformat()


def _load_datetime(value: str | None) -> datetime | None:
    if value is None:
        return None
    parsed = datetime.fromisoformat(value)
    require_aware(parsed, "persisted datetime")
    return parsed


class SQLiteProgressRepository:
    """SQLite implementation with atomic, idempotent schema initialization."""

    def __init__(self, database_path: str | Path) -> None:
        self.database_path = Path(database_path)
        self._initialization_lock = Lock()
        self._initialized = False

    def initialize(self) -> None:
        """Create parent directories and apply all known migrations once."""
        if self._initialized:
            return
        with self._initialization_lock:
            if self._initialized:
                return
            self.database_path.parent.mkdir(parents=True, exist_ok=True)
            with self._connect_uninitialized() as connection:
                current = int(connection.execute("PRAGMA user_version").fetchone()[0])
                if current > SCHEMA_VERSION:
                    raise RuntimeError(
                        f"Progress database schema {current} is newer than supported "
                        f"version {SCHEMA_VERSION}."
                    )
                if current < 1:
                    self._migrate_to_v1(connection)
                connection.execute(f"PRAGMA user_version = {SCHEMA_VERSION}")
            self._initialized = True

    @staticmethod
    def _migrate_to_v1(connection: sqlite3.Connection) -> None:
        connection.executescript(
            """
            CREATE TABLE IF NOT EXISTS attempts (
                attempt_id TEXT PRIMARY KEY,
                course_code TEXT NOT NULL,
                module_id TEXT NOT NULL,
                item_id TEXT NOT NULL,
                item_kind TEXT NOT NULL,
                activity_type TEXT NOT NULL,
                outcome TEXT NOT NULL,
                locale TEXT NOT NULL,
                content_version TEXT NOT NULL,
                created_at TEXT NOT NULL,
                response_text TEXT NOT NULL,
                selected_option_ids TEXT NOT NULL,
                is_correct INTEGER,
                score REAL,
                session_id TEXT NOT NULL
            );
            CREATE INDEX IF NOT EXISTS idx_attempts_scope
                ON attempts(course_code, module_id, item_id, created_at DESC);

            CREATE TABLE IF NOT EXISTS practice_progress (
                course_code TEXT NOT NULL,
                module_id TEXT NOT NULL,
                exercise_id TEXT NOT NULL,
                mastery_state TEXT NOT NULL,
                attempt_count INTEGER NOT NULL,
                last_outcome TEXT NOT NULL,
                updated_at TEXT NOT NULL,
                response_text TEXT NOT NULL,
                selected_option_ids TEXT NOT NULL,
                PRIMARY KEY(course_code, module_id, exercise_id)
            );

            CREATE TABLE IF NOT EXISTS assessment_sessions (
                session_id TEXT PRIMARY KEY,
                scope TEXT NOT NULL,
                course_code TEXT NOT NULL,
                module_id TEXT NOT NULL,
                item_ids TEXT NOT NULL,
                seed INTEGER NOT NULL,
                locale TEXT NOT NULL,
                started_at TEXT NOT NULL,
                answered_item_ids TEXT NOT NULL,
                correct_count INTEGER NOT NULL,
                completed_at TEXT
            );
            CREATE INDEX IF NOT EXISTS idx_sessions_open
                ON assessment_sessions(course_code, module_id, completed_at, started_at DESC);

            CREATE TABLE IF NOT EXISTS flashcard_progress (
                course_code TEXT NOT NULL,
                module_id TEXT NOT NULL,
                card_id TEXT NOT NULL,
                mastery_state TEXT NOT NULL,
                repetitions INTEGER NOT NULL,
                interval_days INTEGER NOT NULL,
                easiness REAL NOT NULL,
                due_at TEXT NOT NULL,
                last_reviewed_at TEXT,
                PRIMARY KEY(course_code, module_id, card_id)
            );

            CREATE TABLE IF NOT EXISTS review_schedule (
                course_code TEXT NOT NULL,
                module_id TEXT NOT NULL,
                item_id TEXT NOT NULL,
                item_kind TEXT NOT NULL,
                mastery_state TEXT NOT NULL,
                repetitions INTEGER NOT NULL,
                interval_days INTEGER NOT NULL,
                easiness REAL NOT NULL,
                due_at TEXT NOT NULL,
                last_reviewed_at TEXT,
                PRIMARY KEY(course_code, module_id, item_id, item_kind)
            );
            CREATE INDEX IF NOT EXISTS idx_review_due
                ON review_schedule(due_at, course_code, module_id);
            """
        )

    @contextmanager
    def _connect(self) -> Iterator[sqlite3.Connection]:
        self.initialize()
        with self._connect_uninitialized() as connection:
            yield connection

    @contextmanager
    def _connect_uninitialized(self) -> Iterator[sqlite3.Connection]:
        connection = sqlite3.connect(self.database_path, timeout=10.0)
        connection.row_factory = sqlite3.Row
        connection.execute("PRAGMA foreign_keys = ON")
        connection.execute("PRAGMA busy_timeout = 10000")
        try:
            with connection:
                yield connection
        finally:
            connection.close()

    def record_attempt(self, attempt: AttemptRecord) -> None:
        with self._connect() as connection:
            connection.execute(
                """
                INSERT INTO attempts (
                    attempt_id, course_code, module_id, item_id, item_kind,
                    activity_type, outcome, locale, content_version, created_at,
                    response_text, selected_option_ids, is_correct, score, session_id
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    attempt.attempt_id,
                    attempt.course_code,
                    attempt.module_id,
                    attempt.item_id,
                    attempt.item_kind.value,
                    attempt.activity_type.value,
                    attempt.outcome.value,
                    attempt.locale,
                    attempt.content_version,
                    _dump_datetime(attempt.created_at),
                    attempt.response_text,
                    _dump_ids(attempt.selected_option_ids),
                    None if attempt.is_correct is None else int(attempt.is_correct),
                    attempt.score,
                    attempt.session_id,
                ),
            )

    def list_attempts(
        self,
        *,
        course_code: str | None = None,
        module_id: str | None = None,
        item_id: str | None = None,
        limit: int | None = None,
    ) -> tuple[AttemptRecord, ...]:
        if limit is not None and limit < 1:
            raise ValueError("limit must be positive.")
        clauses: list[str] = []
        parameters: list[object] = []
        for column, value in (
            ("course_code", course_code),
            ("module_id", module_id),
            ("item_id", item_id),
        ):
            if value is not None:
                clauses.append(f"{column} = ?")
                parameters.append(value)
        where = f" WHERE {' AND '.join(clauses)}" if clauses else ""
        suffix = " ORDER BY created_at DESC, attempt_id DESC"
        if limit is not None:
            suffix += " LIMIT ?"
            parameters.append(limit)
        with self._connect() as connection:
            rows = connection.execute(
                "SELECT * FROM attempts" + where + suffix,
                parameters,
            ).fetchall()
        return tuple(self._attempt_from_row(row) for row in rows)

    @staticmethod
    def _attempt_from_row(row: sqlite3.Row) -> AttemptRecord:
        created_at = _load_datetime(str(row["created_at"]))
        assert created_at is not None
        raw_correct = row["is_correct"]
        return AttemptRecord(
            attempt_id=str(row["attempt_id"]),
            course_code=str(row["course_code"]),
            module_id=str(row["module_id"]),
            item_id=str(row["item_id"]),
            item_kind=LearningItemKind(str(row["item_kind"])),
            activity_type=ActivityType(str(row["activity_type"])),
            outcome=AttemptOutcome(str(row["outcome"])),
            locale=str(row["locale"]),
            content_version=str(row["content_version"]),
            created_at=created_at,
            response_text=str(row["response_text"]),
            selected_option_ids=_load_ids(str(row["selected_option_ids"])),
            is_correct=None if raw_correct is None else bool(raw_correct),
            score=None if row["score"] is None else float(row["score"]),
            session_id=str(row["session_id"]),
        )

    def save_practice_progress(self, progress: PracticeProgress) -> None:
        with self._connect() as connection:
            connection.execute(
                """
                INSERT INTO practice_progress (
                    course_code, module_id, exercise_id, mastery_state, attempt_count,
                    last_outcome, updated_at, response_text, selected_option_ids
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                ON CONFLICT(course_code, module_id, exercise_id) DO UPDATE SET
                    mastery_state=excluded.mastery_state,
                    attempt_count=excluded.attempt_count,
                    last_outcome=excluded.last_outcome,
                    updated_at=excluded.updated_at,
                    response_text=excluded.response_text,
                    selected_option_ids=excluded.selected_option_ids
                """,
                (
                    progress.course_code,
                    progress.module_id,
                    progress.exercise_id,
                    progress.mastery_state.value,
                    progress.attempt_count,
                    progress.last_outcome.value,
                    _dump_datetime(progress.updated_at),
                    progress.response_text,
                    _dump_ids(progress.selected_option_ids),
                ),
            )

    def get_practice_progress(
        self,
        course_code: str,
        module_id: str,
        exercise_id: str,
    ) -> PracticeProgress | None:
        with self._connect() as connection:
            row = connection.execute(
                """
                SELECT * FROM practice_progress
                WHERE course_code = ? AND module_id = ? AND exercise_id = ?
                """,
                (course_code, module_id, exercise_id),
            ).fetchone()
        if row is None:
            return None
        updated_at = _load_datetime(str(row["updated_at"]))
        assert updated_at is not None
        return PracticeProgress(
            course_code=str(row["course_code"]),
            module_id=str(row["module_id"]),
            exercise_id=str(row["exercise_id"]),
            mastery_state=MasteryState(str(row["mastery_state"])),
            attempt_count=int(row["attempt_count"]),
            last_outcome=AttemptOutcome(str(row["last_outcome"])),
            updated_at=updated_at,
            response_text=str(row["response_text"]),
            selected_option_ids=_load_ids(str(row["selected_option_ids"])),
        )

    def save_assessment_session(self, session: AssessmentSession) -> None:
        with self._connect() as connection:
            connection.execute(
                """
                INSERT INTO assessment_sessions (
                    session_id, scope, course_code, module_id, item_ids, seed, locale,
                    started_at, answered_item_ids, correct_count, completed_at
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                ON CONFLICT(session_id) DO UPDATE SET
                    scope=excluded.scope,
                    course_code=excluded.course_code,
                    module_id=excluded.module_id,
                    item_ids=excluded.item_ids,
                    seed=excluded.seed,
                    locale=excluded.locale,
                    started_at=excluded.started_at,
                    answered_item_ids=excluded.answered_item_ids,
                    correct_count=excluded.correct_count,
                    completed_at=excluded.completed_at
                """,
                (
                    session.session_id,
                    session.scope.value,
                    session.course_code,
                    session.module_id,
                    _dump_ids(session.item_ids),
                    session.seed,
                    session.locale,
                    _dump_datetime(session.started_at),
                    _dump_ids(session.answered_item_ids),
                    session.correct_count,
                    _dump_datetime(session.completed_at),
                ),
            )

    def get_assessment_session(self, session_id: str) -> AssessmentSession | None:
        with self._connect() as connection:
            row = connection.execute(
                "SELECT * FROM assessment_sessions WHERE session_id = ?",
                (session_id,),
            ).fetchone()
        return None if row is None else self._session_from_row(row)

    def latest_open_assessment_session(
        self,
        *,
        course_code: str,
        module_id: str,
    ) -> AssessmentSession | None:
        with self._connect() as connection:
            row = connection.execute(
                """
                SELECT * FROM assessment_sessions
                WHERE course_code = ? AND module_id = ? AND completed_at IS NULL
                ORDER BY started_at DESC, session_id DESC
                LIMIT 1
                """,
                (course_code, module_id),
            ).fetchone()
        return None if row is None else self._session_from_row(row)

    @staticmethod
    def _session_from_row(row: sqlite3.Row) -> AssessmentSession:
        started_at = _load_datetime(str(row["started_at"]))
        assert started_at is not None
        completed_raw = row["completed_at"]
        return AssessmentSession(
            session_id=str(row["session_id"]),
            scope=AssessmentScope(str(row["scope"])),
            course_code=str(row["course_code"]),
            module_id=str(row["module_id"]),
            item_ids=_load_ids(str(row["item_ids"])),
            seed=int(row["seed"]),
            locale=str(row["locale"]),
            started_at=started_at,
            answered_item_ids=_load_ids(str(row["answered_item_ids"])),
            correct_count=int(row["correct_count"]),
            completed_at=_load_datetime(None if completed_raw is None else str(completed_raw)),
        )

    def save_flashcard_progress(self, progress: FlashcardProgress) -> None:
        with self._connect() as connection:
            connection.execute(
                """
                INSERT INTO flashcard_progress (
                    course_code, module_id, card_id, mastery_state, repetitions,
                    interval_days, easiness, due_at, last_reviewed_at
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                ON CONFLICT(course_code, module_id, card_id) DO UPDATE SET
                    mastery_state=excluded.mastery_state,
                    repetitions=excluded.repetitions,
                    interval_days=excluded.interval_days,
                    easiness=excluded.easiness,
                    due_at=excluded.due_at,
                    last_reviewed_at=excluded.last_reviewed_at
                """,
                (
                    progress.course_code,
                    progress.module_id,
                    progress.card_id,
                    progress.mastery_state.value,
                    progress.repetitions,
                    progress.interval_days,
                    progress.easiness,
                    _dump_datetime(progress.due_at),
                    _dump_datetime(progress.last_reviewed_at),
                ),
            )

    def get_flashcard_progress(
        self,
        course_code: str,
        module_id: str,
        card_id: str,
    ) -> FlashcardProgress | None:
        with self._connect() as connection:
            row = connection.execute(
                """
                SELECT * FROM flashcard_progress
                WHERE course_code = ? AND module_id = ? AND card_id = ?
                """,
                (course_code, module_id, card_id),
            ).fetchone()
        if row is None:
            return None
        due_at = _load_datetime(str(row["due_at"]))
        assert due_at is not None
        reviewed_raw = row["last_reviewed_at"]
        return FlashcardProgress(
            course_code=str(row["course_code"]),
            module_id=str(row["module_id"]),
            card_id=str(row["card_id"]),
            mastery_state=MasteryState(str(row["mastery_state"])),
            repetitions=int(row["repetitions"]),
            interval_days=int(row["interval_days"]),
            easiness=float(row["easiness"]),
            due_at=due_at,
            last_reviewed_at=_load_datetime(None if reviewed_raw is None else str(reviewed_raw)),
        )

    def save_review_schedule(self, schedule: ReviewSchedule) -> None:
        with self._connect() as connection:
            connection.execute(
                """
                INSERT INTO review_schedule (
                    course_code, module_id, item_id, item_kind, mastery_state,
                    repetitions, interval_days, easiness, due_at, last_reviewed_at
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                ON CONFLICT(course_code, module_id, item_id, item_kind) DO UPDATE SET
                    mastery_state=excluded.mastery_state,
                    repetitions=excluded.repetitions,
                    interval_days=excluded.interval_days,
                    easiness=excluded.easiness,
                    due_at=excluded.due_at,
                    last_reviewed_at=excluded.last_reviewed_at
                """,
                (
                    schedule.course_code,
                    schedule.module_id,
                    schedule.item_id,
                    schedule.item_kind.value,
                    schedule.mastery_state.value,
                    schedule.repetitions,
                    schedule.interval_days,
                    schedule.easiness,
                    _dump_datetime(schedule.due_at),
                    _dump_datetime(schedule.last_reviewed_at),
                ),
            )

    def get_review_schedule(
        self,
        course_code: str,
        module_id: str,
        item_id: str,
        item_kind: str,
    ) -> ReviewSchedule | None:
        kind = LearningItemKind(item_kind)
        with self._connect() as connection:
            row = connection.execute(
                """
                SELECT * FROM review_schedule
                WHERE course_code = ? AND module_id = ? AND item_id = ?
                  AND item_kind = ?
                """,
                (course_code, module_id, item_id, kind.value),
            ).fetchone()
        return None if row is None else self._review_from_row(row)

    def list_flashcard_progress(
        self,
        *,
        course_code: str | None = None,
        module_id: str | None = None,
    ) -> tuple[FlashcardProgress, ...]:
        clauses: list[str] = []
        parameters: list[object] = []
        if course_code is not None:
            clauses.append("course_code = ?")
            parameters.append(course_code)
        if module_id is not None:
            clauses.append("module_id = ?")
            parameters.append(module_id)
        where = f" WHERE {' AND '.join(clauses)}" if clauses else ""
        with self._connect() as connection:
            rows = connection.execute(
                "SELECT * FROM flashcard_progress"
                + where
                + " ORDER BY course_code, module_id, card_id",
                parameters,
            ).fetchall()
        values: list[FlashcardProgress] = []
        for row in rows:
            due_at = _load_datetime(str(row["due_at"]))
            assert due_at is not None
            reviewed_raw = row["last_reviewed_at"]
            values.append(
                FlashcardProgress(
                    course_code=str(row["course_code"]),
                    module_id=str(row["module_id"]),
                    card_id=str(row["card_id"]),
                    mastery_state=MasteryState(str(row["mastery_state"])),
                    repetitions=int(row["repetitions"]),
                    interval_days=int(row["interval_days"]),
                    easiness=float(row["easiness"]),
                    due_at=due_at,
                    last_reviewed_at=_load_datetime(
                        None if reviewed_raw is None else str(reviewed_raw)
                    ),
                )
            )
        return tuple(values)

    def list_due_reviews(
        self,
        *,
        due_at: datetime,
        course_code: str | None = None,
        module_id: str | None = None,
        limit: int | None = None,
    ) -> tuple[ReviewSchedule, ...]:
        require_aware(due_at, "due_at")
        if limit is not None and limit < 1:
            raise ValueError("limit must be positive.")
        clauses = ["due_at <= ?"]
        parameters: list[object] = [_dump_datetime(due_at)]
        if course_code is not None:
            clauses.append("course_code = ?")
            parameters.append(course_code)
        if module_id is not None:
            clauses.append("module_id = ?")
            parameters.append(module_id)
        suffix = " ORDER BY due_at, course_code, module_id, item_id, item_kind"
        if limit is not None:
            suffix += " LIMIT ?"
            parameters.append(limit)
        with self._connect() as connection:
            rows = connection.execute(
                "SELECT * FROM review_schedule WHERE " + " AND ".join(clauses) + suffix,
                parameters,
            ).fetchall()
        return tuple(self._review_from_row(row) for row in rows)

    @staticmethod
    def _review_from_row(row: sqlite3.Row) -> ReviewSchedule:
        due_at = _load_datetime(str(row["due_at"]))
        assert due_at is not None
        reviewed_raw = row["last_reviewed_at"]
        return ReviewSchedule(
            course_code=str(row["course_code"]),
            module_id=str(row["module_id"]),
            item_id=str(row["item_id"]),
            item_kind=LearningItemKind(str(row["item_kind"])),
            mastery_state=MasteryState(str(row["mastery_state"])),
            repetitions=int(row["repetitions"]),
            interval_days=int(row["interval_days"]),
            easiness=float(row["easiness"]),
            due_at=due_at,
            last_reviewed_at=_load_datetime(None if reviewed_raw is None else str(reviewed_raw)),
        )

    def module_progress(self, course_code: str, module_id: str) -> ModuleProgress:
        with self._connect() as connection:
            attempts = connection.execute(
                """
                SELECT COUNT(*) AS attempt_count,
                       SUM(CASE WHEN is_correct = 1 THEN 1 ELSE 0 END) AS correct_count,
                       MAX(created_at) AS last_activity_at
                FROM attempts
                WHERE course_code = ? AND module_id = ?
                """,
                (course_code, module_id),
            ).fetchone()
            pending = connection.execute(
                """
                SELECT COUNT(*) AS pending_count
                FROM review_schedule
                WHERE course_code = ? AND module_id = ?
                  AND due_at <= ?
                """,
                (course_code, module_id, _dump_datetime(datetime.now(UTC))),
            ).fetchone()
            mastery_rows = connection.execute(
                """
                SELECT mastery_state FROM (
                    SELECT mastery_state FROM practice_progress
                    WHERE course_code = ? AND module_id = ?
                    UNION ALL
                    SELECT mastery_state FROM review_schedule
                    WHERE course_code = ? AND module_id = ?
                )
                """,
                (course_code, module_id, course_code, module_id),
            ).fetchall()

        attempt_count = int(attempts["attempt_count"] or 0)
        correct_count = int(attempts["correct_count"] or 0)
        states = tuple(MasteryState(str(row["mastery_state"])) for row in mastery_rows)
        mastery_state = self._aggregate_mastery(states)
        last_raw = attempts["last_activity_at"]
        return ModuleProgress(
            course_code=course_code,
            module_id=module_id,
            mastery_state=mastery_state,
            attempt_count=attempt_count,
            correct_count=correct_count,
            pending_review_count=int(pending["pending_count"] or 0),
            last_activity_at=_load_datetime(None if last_raw is None else str(last_raw)),
        )

    @staticmethod
    def _aggregate_mastery(states: tuple[MasteryState, ...]) -> MasteryState:
        if not states:
            return MasteryState.NEW
        weights = {
            MasteryState.NEW: 0,
            MasteryState.LEARNING: 1,
            MasteryState.REVIEWING: 2,
            MasteryState.MASTERED: 3,
        }
        average = sum(weights[state] for state in states) / len(states)
        if average >= 2.5:
            return MasteryState.MASTERED
        if average >= 1.5:
            return MasteryState.REVIEWING
        return MasteryState.LEARNING

    def schema_version(self) -> int:
        """Return the on-disk schema version for diagnostics and migration tests."""
        with self._connect() as connection:
            return int(connection.execute("PRAGMA user_version").fetchone()[0])


__all__ = ["SCHEMA_VERSION", "SQLiteProgressRepository"]
