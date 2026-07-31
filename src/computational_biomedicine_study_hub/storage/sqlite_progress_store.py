"""SQLite persistence for attempts and objective-level mastery.

The store keeps study data local and uses only Python's standard library. Public
methods are transaction-safe so attempts and their resulting mastery states can be
saved atomically.
"""

from __future__ import annotations

import sqlite3
from datetime import datetime
from pathlib import Path
from types import TracebackType

from ..learning.progress import AttemptRecord, ConfidenceLevel, MasteryState, ReviewItem
from ..learning.review_scheduler import update_mastery

_SCHEMA_VERSION = 2


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

    @property
    def schema_version(self) -> int:
        """Return the currently installed local schema version."""

        row = self._connection.execute("PRAGMA user_version").fetchone()
        assert row is not None
        return int(row[0])

    def record_attempt(self, attempt: AttemptRecord) -> None:
        """Store one immutable attempt."""

        with self._connection:
            self._insert_attempt(attempt)

    def save_mastery(
        self,
        state: MasteryState,
        *,
        course_code: str,
        module_id: str,
    ) -> None:
        """Insert or replace one explicitly scoped objective state."""

        with self._connection:
            self._upsert_mastery(state, course_code=course_code, module_id=module_id)

    def record_and_update(self, attempt: AttemptRecord) -> MasteryState:
        """Atomically store one attempt and update its objective mastery."""

        return self.record_batch_and_update((attempt,))[0]

    def record_batch_and_update(
        self,
        attempts: tuple[AttemptRecord, ...],
    ) -> tuple[MasteryState, ...]:
        """Atomically store one interaction expanded across explicit objectives."""

        if not attempts:
            raise ValueError("Attempt batches cannot be empty.")
        attempt_ids = tuple(attempt.attempt_id for attempt in attempts)
        if len(attempt_ids) != len(set(attempt_ids)):
            raise ValueError("Attempt batches cannot contain duplicate attempt IDs.")

        states: list[MasteryState] = []
        staged: dict[tuple[str, str, str], MasteryState] = {}
        with self._connection:
            for attempt in attempts:
                key = (attempt.course_code, attempt.module_id, attempt.objective_id)
                previous = staged.get(key)
                if previous is None:
                    previous = self._get_mastery(*key)
                state = update_mastery(previous, attempt)
                self._insert_attempt(attempt)
                self._upsert_mastery(
                    state,
                    course_code=attempt.course_code,
                    module_id=attempt.module_id,
                )
                staged[key] = state
                states.append(state)
        return tuple(states)

    def get_attempt(self, attempt_id: str) -> AttemptRecord | None:
        """Return one attempt by stable ID."""

        row = self._connection.execute(
            "SELECT * FROM attempts WHERE attempt_id = ?",
            (attempt_id,),
        ).fetchone()
        return self._attempt_from_row(row) if row is not None else None

    def list_attempts(
        self,
        *,
        course_code: str | None = None,
        module_id: str | None = None,
        objective_id: str | None = None,
    ) -> tuple[AttemptRecord, ...]:
        """Return attempts chronologically with optional composite filtering."""

        clauses: list[str] = []
        parameters: list[object] = []
        for column, value in (
            ("course_code", course_code),
            ("module_id", module_id),
            ("objective_id", objective_id),
        ):
            if value is not None:
                clauses.append(f"{column} = ?")
                parameters.append(value)

        query = "SELECT * FROM attempts"
        if clauses:
            query += " WHERE " + " AND ".join(clauses)
        query += " ORDER BY attempted_at, attempt_id"
        rows = self._connection.execute(query, tuple(parameters)).fetchall()
        return tuple(self._attempt_from_row(row) for row in rows)

    def get_mastery(
        self,
        objective_id: str,
        *,
        course_code: str | None = None,
        module_id: str | None = None,
    ) -> MasteryState | None:
        """Return one mastery state, requiring scope when the ID is ambiguous."""

        if (course_code is None) != (module_id is None):
            raise ValueError("course_code and module_id must be provided together.")
        if course_code is not None and module_id is not None:
            return self._get_mastery(course_code, module_id, objective_id)

        rows = self._connection.execute(
            """
            SELECT * FROM mastery
            WHERE objective_id = ?
            ORDER BY course_code, module_id
            """,
            (objective_id,),
        ).fetchall()
        if not rows:
            return None
        if len(rows) > 1:
            raise ValueError(
                f"Objective {objective_id!r} is ambiguous; provide course_code and module_id."
            )
        return self._mastery_from_row(rows[0])

    def due_reviews(
        self,
        as_of: datetime,
        *,
        limit: int | None = None,
    ) -> tuple[ReviewItem, ...]:
        """Return due review items ordered by urgency and weakest mastery."""

        self._require_aware(as_of, "as_of")
        if limit is not None and limit < 1:
            raise ValueError("limit must be at least 1 when provided.")

        query = """
            SELECT * FROM mastery
            WHERE next_review_at <= ?
            ORDER BY next_review_at ASC, mastery_score ASC,
                     course_code ASC, module_id ASC, objective_id ASC
        """
        parameters: tuple[object, ...]
        if limit is None:
            parameters = (as_of.isoformat(),)
        else:
            query += " LIMIT ?"
            parameters = (as_of.isoformat(), limit)

        rows = self._connection.execute(query, parameters).fetchall()
        return tuple(
            ReviewItem(
                course_code=str(row["course_code"]),
                module_id=str(row["module_id"]),
                state=self._mastery_from_row(row),
            )
            for row in rows
        )

    def due_mastery(
        self,
        as_of: datetime,
        *,
        limit: int | None = None,
    ) -> tuple[MasteryState, ...]:
        """Return due mastery states for compatibility with the initial API."""

        return tuple(item.state for item in self.due_reviews(as_of, limit=limit))

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
        current_version = self.schema_version
        if current_version > _SCHEMA_VERSION:
            raise RuntimeError(
                f"Progress database schema {current_version} is newer than supported "
                f"version {_SCHEMA_VERSION}."
            )

        with self._connection:
            if current_version == 0:
                if self._table_exists("mastery") and not self._table_has_column(
                    "mastery", "course_code"
                ):
                    self._migrate_v1_to_v2()
                else:
                    self._create_schema_v2()
            elif current_version == 1:
                self._migrate_v1_to_v2()
            else:
                self._create_schema_v2()
            self._connection.execute(f"PRAGMA user_version = {_SCHEMA_VERSION}")

    def _create_schema_v2(self) -> None:
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
                ON attempts (course_code, module_id, objective_id, attempted_at);

            CREATE TABLE IF NOT EXISTS mastery (
                course_code TEXT NOT NULL,
                module_id TEXT NOT NULL,
                objective_id TEXT NOT NULL,
                mastery_score REAL NOT NULL CHECK (mastery_score BETWEEN 0 AND 1),
                attempts INTEGER NOT NULL CHECK (attempts >= 1),
                consecutive_correct INTEGER NOT NULL CHECK (consecutive_correct >= 0),
                lapse_count INTEGER NOT NULL CHECK (lapse_count >= 0),
                last_attempt_at TEXT NOT NULL,
                next_review_at TEXT NOT NULL,
                PRIMARY KEY (course_code, module_id, objective_id)
            );

            CREATE INDEX IF NOT EXISTS idx_mastery_due
                ON mastery (
                    next_review_at,
                    mastery_score,
                    course_code,
                    module_id,
                    objective_id
                );
            """
        )

    def _migrate_v1_to_v2(self) -> None:
        self._connection.executescript(
            """
            DROP INDEX IF EXISTS idx_mastery_due;
            DROP INDEX IF EXISTS idx_attempts_objective_time;
            ALTER TABLE mastery RENAME TO mastery_v1;
            """
        )
        self._create_schema_v2()
        self._connection.execute(
            """
            INSERT INTO mastery (
                course_code,
                module_id,
                objective_id,
                mastery_score,
                attempts,
                consecutive_correct,
                lapse_count,
                last_attempt_at,
                next_review_at
            )
            SELECT
                latest.course_code,
                latest.module_id,
                previous.objective_id,
                previous.mastery_score,
                previous.attempts,
                previous.consecutive_correct,
                previous.lapse_count,
                previous.last_attempt_at,
                previous.next_review_at
            FROM mastery_v1 AS previous
            JOIN attempts AS latest
              ON latest.attempt_id = (
                    SELECT candidate.attempt_id
                    FROM attempts AS candidate
                    WHERE candidate.objective_id = previous.objective_id
                    ORDER BY candidate.attempted_at DESC, candidate.attempt_id DESC
                    LIMIT 1
                )
            """
        )
        self._connection.execute("DROP TABLE mastery_v1")

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

    def _upsert_mastery(
        self,
        state: MasteryState,
        *,
        course_code: str,
        module_id: str,
    ) -> None:
        self._connection.execute(
            """
            INSERT INTO mastery (
                course_code,
                module_id,
                objective_id,
                mastery_score,
                attempts,
                consecutive_correct,
                lapse_count,
                last_attempt_at,
                next_review_at
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            ON CONFLICT(course_code, module_id, objective_id) DO UPDATE SET
                mastery_score = excluded.mastery_score,
                attempts = excluded.attempts,
                consecutive_correct = excluded.consecutive_correct,
                lapse_count = excluded.lapse_count,
                last_attempt_at = excluded.last_attempt_at,
                next_review_at = excluded.next_review_at
            """,
            (
                course_code,
                module_id,
                state.objective_id,
                state.mastery_score,
                state.attempts,
                state.consecutive_correct,
                state.lapse_count,
                state.last_attempt_at.isoformat(),
                state.next_review_at.isoformat(),
            ),
        )

    def _get_mastery(
        self,
        course_code: str,
        module_id: str,
        objective_id: str,
    ) -> MasteryState | None:
        row = self._connection.execute(
            """
            SELECT * FROM mastery
            WHERE course_code = ? AND module_id = ? AND objective_id = ?
            """,
            (course_code, module_id, objective_id),
        ).fetchone()
        return self._mastery_from_row(row) if row is not None else None

    def _table_exists(self, table_name: str) -> bool:
        row = self._connection.execute(
            """
            SELECT 1 FROM sqlite_master
            WHERE type = 'table' AND name = ?
            """,
            (table_name,),
        ).fetchone()
        return row is not None

    def _table_has_column(self, table_name: str, column_name: str) -> bool:
        rows = self._connection.execute(f"PRAGMA table_info({table_name})").fetchall()
        return any(str(row["name"]) == column_name for row in rows)

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
