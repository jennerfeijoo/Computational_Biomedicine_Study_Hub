"""SQLite persistence for attempts and objective-level mastery.

The store keeps study data local and uses only Python's standard library. Public
methods are transaction-safe so an attempt and its resulting mastery state can be
saved atomically.
"""

from __future__ import annotations

import sqlite3
from datetime import datetime
from pathlib import Path
from types import TracebackType

from ..learning.progress import AttemptRecord, ConfidenceLevel, MasteryState
from ..learning.review_scheduler import update_mastery

_SCHEMA_VERSION = 1


class SQLiteProgressStore:
    """Persist private learning progress in one local SQLite database."""

    def __init__(self, database: str | Path) -> None:
        self._database = str(database)
        self._connection = sqlite3.connect(self._database)
        self._connection.row_factory = sqlite3.Row
        self._connection.execute("PRAGMA foreign_keys = ON")
        self._initialize_schema()

    @property
    def database(self) -> str:
        """Return the configured database path or ``:memory:`` identifier."""

        return self._database

    def record_attempt(self, attempt: AttemptRecord) -> None:
        """Store one immutable attempt."""

        with self._connection:
            self._insert_attempt(attempt)

    def save_mastery(self, state: MasteryState) -> None:
        """Insert or replace the current state for one objective."""

        with self._connection:
            self._upsert_mastery(state)

    def record_and_update(self, attempt: AttemptRecord) -> MasteryState:
        """Atomically store an attempt and update its objective mastery."""

        with self._connection:
            previous = self._get_mastery(attempt.objective_id)
            state = update_mastery(previous, attempt)
            self._insert_attempt(attempt)
            self._upsert_mastery(state)
        return state

    def get_attempt(self, attempt_id: str) -> AttemptRecord | None:
        """Return one attempt by stable ID."""

        row = self._connection.execute(
            "SELECT * FROM attempts WHERE attempt_id = ?",
            (attempt_id,),
        ).fetchone()
        return self._attempt_from_row(row) if row is not None else None

    def list_attempts(self, *, objective_id: str | None = None) -> tuple[AttemptRecord, ...]:
        """Return attempts in chronological order, optionally for one objective."""

        if objective_id is None:
            rows = self._connection.execute(
                "SELECT * FROM attempts ORDER BY attempted_at, attempt_id"
            ).fetchall()
        else:
            rows = self._connection.execute(
                """
                SELECT * FROM attempts
                WHERE objective_id = ?
                ORDER BY attempted_at, attempt_id
                """,
                (objective_id,),
            ).fetchall()
        return tuple(self._attempt_from_row(row) for row in rows)

    def get_mastery(self, objective_id: str) -> MasteryState | None:
        """Return the latest mastery state for one objective."""

        return self._get_mastery(objective_id)

    def due_mastery(self, as_of: datetime, *, limit: int | None = None) -> tuple[MasteryState, ...]:
        """Return due objectives ordered by urgency and weakest mastery."""

        self._require_aware(as_of, "as_of")
        if limit is not None and limit < 1:
            raise ValueError("limit must be at least 1 when provided.")

        query = """
            SELECT * FROM mastery
            WHERE next_review_at <= ?
            ORDER BY next_review_at ASC, mastery_score ASC, objective_id ASC
        """
        parameters: tuple[object, ...]
        if limit is None:
            parameters = (as_of.isoformat(),)
        else:
            query += " LIMIT ?"
            parameters = (as_of.isoformat(), limit)

        rows = self._connection.execute(query, parameters).fetchall()
        return tuple(self._mastery_from_row(row) for row in rows)

    def close(self) -> None:
        """Close the underlying SQLite connection."""

        self._connection.close()

    def __enter__(self) -> SQLiteProgressStore:
        return self

    def __exit__(
        self,
        exc_type: type[BaseException] | None,
        exc_value: BaseException | None,
        traceback: TracebackType | None,
    ) -> None:
        del exc_type, exc_value, traceback
        self.close()

    def _initialize_schema(self) -> None:
        with self._connection:
            self._connection.executescript(
                """
                CREATE TABLE IF NOT EXISTS attempts (
                    attempt_id TEXT PRIMARY KEY,
                    course_code TEXT NOT NULL,
                    module_id TEXT NOT NULL,
                    objective_id TEXT NOT NULL,
                    item_id TEXT NOT NULL,
                    activity_type TEXT NOT NULL,
                    answer TEXT NOT NULL,
                    is_correct INTEGER NOT NULL CHECK (is_correct IN (0, 1)),
                    confidence TEXT NOT NULL CHECK (confidence IN ('low', 'medium', 'high')),
                    hints_used INTEGER NOT NULL CHECK (hints_used >= 0),
                    response_time_ms INTEGER NOT NULL CHECK (response_time_ms >= 0),
                    solution_revealed INTEGER NOT NULL CHECK (solution_revealed IN (0, 1)),
                    attempted_at TEXT NOT NULL
                );

                CREATE INDEX IF NOT EXISTS idx_attempts_objective_time
                    ON attempts (objective_id, attempted_at);

                CREATE TABLE IF NOT EXISTS mastery (
                    objective_id TEXT PRIMARY KEY,
                    mastery_score REAL NOT NULL CHECK (mastery_score BETWEEN 0 AND 1),
                    attempts INTEGER NOT NULL CHECK (attempts >= 1),
                    consecutive_correct INTEGER NOT NULL CHECK (consecutive_correct >= 0),
                    lapse_count INTEGER NOT NULL CHECK (lapse_count >= 0),
                    last_attempt_at TEXT NOT NULL,
                    next_review_at TEXT NOT NULL
                );

                CREATE INDEX IF NOT EXISTS idx_mastery_due
                    ON mastery (next_review_at, mastery_score);
                """
            )
            self._connection.execute(f"PRAGMA user_version = {_SCHEMA_VERSION}")

    def _insert_attempt(self, attempt: AttemptRecord) -> None:
        self._connection.execute(
            """
            INSERT INTO attempts (
                attempt_id,
                course_code,
                module_id,
                objective_id,
                item_id,
                activity_type,
                answer,
                is_correct,
                confidence,
                hints_used,
                response_time_ms,
                solution_revealed,
                attempted_at
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                attempt.attempt_id,
                attempt.course_code,
                attempt.module_id,
                attempt.objective_id,
                attempt.item_id,
                attempt.activity_type,
                attempt.answer,
                int(attempt.is_correct),
                attempt.confidence.value,
                attempt.hints_used,
                attempt.response_time_ms,
                int(attempt.solution_revealed),
                attempt.attempted_at.isoformat(),
            ),
        )

    def _upsert_mastery(self, state: MasteryState) -> None:
        self._connection.execute(
            """
            INSERT INTO mastery (
                objective_id,
                mastery_score,
                attempts,
                consecutive_correct,
                lapse_count,
                last_attempt_at,
                next_review_at
            ) VALUES (?, ?, ?, ?, ?, ?, ?)
            ON CONFLICT(objective_id) DO UPDATE SET
                mastery_score = excluded.mastery_score,
                attempts = excluded.attempts,
                consecutive_correct = excluded.consecutive_correct,
                lapse_count = excluded.lapse_count,
                last_attempt_at = excluded.last_attempt_at,
                next_review_at = excluded.next_review_at
            """,
            (
                state.objective_id,
                state.mastery_score,
                state.attempts,
                state.consecutive_correct,
                state.lapse_count,
                state.last_attempt_at.isoformat(),
                state.next_review_at.isoformat(),
            ),
        )

    def _get_mastery(self, objective_id: str) -> MasteryState | None:
        row = self._connection.execute(
            "SELECT * FROM mastery WHERE objective_id = ?",
            (objective_id,),
        ).fetchone()
        return self._mastery_from_row(row) if row is not None else None

    @staticmethod
    def _attempt_from_row(row: sqlite3.Row) -> AttemptRecord:
        return AttemptRecord(
            attempt_id=str(row["attempt_id"]),
            course_code=str(row["course_code"]),
            module_id=str(row["module_id"]),
            objective_id=str(row["objective_id"]),
            item_id=str(row["item_id"]),
            activity_type=str(row["activity_type"]),
            answer=str(row["answer"]),
            is_correct=bool(int(row["is_correct"])),
            confidence=ConfidenceLevel(str(row["confidence"])),
            hints_used=int(row["hints_used"]),
            response_time_ms=int(row["response_time_ms"]),
            solution_revealed=bool(int(row["solution_revealed"])),
            attempted_at=datetime.fromisoformat(str(row["attempted_at"])),
        )

    @staticmethod
    def _mastery_from_row(row: sqlite3.Row) -> MasteryState:
        return MasteryState(
            objective_id=str(row["objective_id"]),
            mastery_score=float(row["mastery_score"]),
            attempts=int(row["attempts"]),
            consecutive_correct=int(row["consecutive_correct"]),
            lapse_count=int(row["lapse_count"]),
            last_attempt_at=datetime.fromisoformat(str(row["last_attempt_at"])),
            next_review_at=datetime.fromisoformat(str(row["next_review_at"])),
        )

    @staticmethod
    def _require_aware(value: datetime, field_name: str) -> None:
        if value.tzinfo is None or value.utcoffset() is None:
            raise ValueError(f"{field_name} must be timezone-aware.")


__all__ = ["SQLiteProgressStore"]
