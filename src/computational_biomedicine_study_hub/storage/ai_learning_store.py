"""SQLite persistence for AI-generated study material and feedback.

This store is intentionally separate from the deterministic progress database. It owns
AI-generated flashcards/questions, their provenance, assessment attempts, module-level
reinforcement statistics, and code-feedback records. Schema changes are versioned through
explicit migrations so generated content survives application upgrades.
"""

from __future__ import annotations

import json
import sqlite3
from dataclasses import dataclass
from datetime import UTC, datetime
from pathlib import Path
from typing import Any
from uuid import uuid4

_SCHEMA_VERSION = 1


@dataclass(frozen=True, slots=True)
class FlashcardRecord:
    card_id: str
    course_code: str
    module_id: str
    front: str
    back: str
    source_hash: str
    created_at: str


@dataclass(frozen=True, slots=True)
class GeneratedQuestion:
    question_id: str
    course_code: str
    module_id: str
    question_type: str
    prompt: str
    options: tuple[str, ...]
    correct_answer: str
    rationale: str
    rubric: tuple[str, ...]
    created_at: str


class AILearningStore:
    """Persist AI learning artifacts in a local SQLite database."""

    def __init__(self, database: str | Path) -> None:
        self._database = str(database)
        self._connection = sqlite3.connect(self._database)
        self._connection.row_factory = sqlite3.Row
        self._connection.execute("PRAGMA foreign_keys = ON")
        self._migrate()

    @property
    def database(self) -> str:
        return self._database

    @property
    def schema_version(self) -> int:
        row = self._connection.execute("PRAGMA user_version").fetchone()
        return int(row[0]) if row is not None else 0

    def close(self) -> None:
        self._connection.close()

    def __enter__(self) -> "AILearningStore":
        return self

    def __exit__(self, exc_type: Any, exc_value: Any, traceback: Any) -> None:
        del exc_type, exc_value, traceback
        self.close()

    def list_flashcards(self, course_code: str, module_id: str) -> tuple[FlashcardRecord, ...]:
        rows = self._connection.execute(
            """
            SELECT card_id, course_code, module_id, front, back, source_hash, created_at
            FROM flashcards
            WHERE course_code = ? AND module_id = ?
            ORDER BY created_at, card_id
            """,
            (course_code, module_id),
        ).fetchall()
        return tuple(self._flashcard_from_row(row) for row in rows)

    def save_flashcards(self, cards: tuple[FlashcardRecord, ...]) -> None:
        if not cards:
            return
        with self._connection:
            self._connection.executemany(
                """
                INSERT INTO flashcards
                    (card_id, course_code, module_id, front, back, source_hash, created_at)
                VALUES (?, ?, ?, ?, ?, ?, ?)
                ON CONFLICT(card_id) DO UPDATE SET
                    front=excluded.front,
                    back=excluded.back,
                    source_hash=excluded.source_hash
                """,
                [
                    (
                        card.card_id,
                        card.course_code,
                        card.module_id,
                        card.front,
                        card.back,
                        card.source_hash,
                        card.created_at,
                    )
                    for card in cards
                ],
            )

    def save_generated_questions(self, questions: tuple[GeneratedQuestion, ...]) -> None:
        if not questions:
            return
        with self._connection:
            self._connection.executemany(
                """
                INSERT INTO generated_questions
                    (question_id, course_code, module_id, question_type, prompt,
                     options_json, correct_answer, rationale, rubric_json, created_at)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                ON CONFLICT(question_id) DO UPDATE SET
                    prompt=excluded.prompt,
                    options_json=excluded.options_json,
                    correct_answer=excluded.correct_answer,
                    rationale=excluded.rationale,
                    rubric_json=excluded.rubric_json
                """,
                [
                    (
                        q.question_id,
                        q.course_code,
                        q.module_id,
                        q.question_type,
                        q.prompt,
                        json.dumps(q.options, ensure_ascii=False),
                        q.correct_answer,
                        q.rationale,
                        json.dumps(q.rubric, ensure_ascii=False),
                        q.created_at,
                    )
                    for q in questions
                ],
            )

    def record_question_attempt(
        self,
        *,
        question_id: str,
        course_code: str,
        module_id: str,
        is_correct: bool,
        user_answer: str,
        feedback: str,
    ) -> None:
        now = datetime.now(UTC).isoformat()
        with self._connection:
            self._connection.execute(
                """
                INSERT INTO assessment_attempts
                    (attempt_id, question_id, course_code, module_id, is_correct,
                     user_answer, feedback, attempted_at)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    str(uuid4()),
                    question_id,
                    course_code,
                    module_id,
                    int(is_correct),
                    user_answer,
                    feedback,
                    now,
                ),
            )
            self._connection.execute(
                """
                INSERT INTO module_performance
                    (course_code, module_id, attempts, correct, updated_at)
                VALUES (?, ?, 1, ?, ?)
                ON CONFLICT(course_code, module_id) DO UPDATE SET
                    attempts=module_performance.attempts + 1,
                    correct=module_performance.correct + excluded.correct,
                    updated_at=excluded.updated_at
                """,
                (course_code, module_id, int(is_correct), now),
            )

    def module_performance(self, course_code: str) -> dict[str, tuple[int, int]]:
        rows = self._connection.execute(
            """
            SELECT module_id, attempts, correct
            FROM module_performance
            WHERE course_code = ?
            """,
            (course_code,),
        ).fetchall()
        return {
            str(row["module_id"]): (int(row["attempts"]), int(row["correct"]))
            for row in rows
        }

    def save_code_feedback(
        self,
        *,
        course_code: str,
        module_id: str,
        exercise_id: str,
        source_code: str,
        correctness: str,
        complexity: str,
        best_practices: str,
        improvement: str,
    ) -> str:
        feedback_id = str(uuid4())
        with self._connection:
            self._connection.execute(
                """
                INSERT INTO code_feedback
                    (feedback_id, course_code, module_id, exercise_id, source_code,
                     correctness, complexity, best_practices, improvement, created_at)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    feedback_id,
                    course_code,
                    module_id,
                    exercise_id,
                    source_code,
                    correctness,
                    complexity,
                    best_practices,
                    improvement,
                    datetime.now(UTC).isoformat(),
                ),
            )
        return feedback_id

    def _migrate(self) -> None:
        version = self.schema_version
        if version > _SCHEMA_VERSION:
            raise RuntimeError(
                f"AI learning schema {version} is newer than supported {_SCHEMA_VERSION}."
            )
        with self._connection:
            if version == 0:
                self._connection.executescript(
                    """
                    CREATE TABLE IF NOT EXISTS flashcards (
                        card_id TEXT PRIMARY KEY,
                        course_code TEXT NOT NULL,
                        module_id TEXT NOT NULL,
                        front TEXT NOT NULL,
                        back TEXT NOT NULL,
                        source_hash TEXT NOT NULL,
                        created_at TEXT NOT NULL
                    );
                    CREATE INDEX IF NOT EXISTS idx_flashcards_module
                        ON flashcards(course_code, module_id, created_at);

                    CREATE TABLE IF NOT EXISTS generated_questions (
                        question_id TEXT PRIMARY KEY,
                        course_code TEXT NOT NULL,
                        module_id TEXT NOT NULL,
                        question_type TEXT NOT NULL CHECK(question_type IN ('multiple_choice', 'short_reasoning')),
                        prompt TEXT NOT NULL,
                        options_json TEXT NOT NULL,
                        correct_answer TEXT NOT NULL,
                        rationale TEXT NOT NULL,
                        rubric_json TEXT NOT NULL,
                        created_at TEXT NOT NULL
                    );
                    CREATE INDEX IF NOT EXISTS idx_generated_questions_module
                        ON generated_questions(course_code, module_id, created_at);

                    CREATE TABLE IF NOT EXISTS assessment_attempts (
                        attempt_id TEXT PRIMARY KEY,
                        question_id TEXT NOT NULL REFERENCES generated_questions(question_id) ON DELETE CASCADE,
                        course_code TEXT NOT NULL,
                        module_id TEXT NOT NULL,
                        is_correct INTEGER NOT NULL CHECK(is_correct IN (0,1)),
                        user_answer TEXT NOT NULL,
                        feedback TEXT NOT NULL,
                        attempted_at TEXT NOT NULL
                    );
                    CREATE INDEX IF NOT EXISTS idx_assessment_attempts_module
                        ON assessment_attempts(course_code, module_id, attempted_at);

                    CREATE TABLE IF NOT EXISTS module_performance (
                        course_code TEXT NOT NULL,
                        module_id TEXT NOT NULL,
                        attempts INTEGER NOT NULL CHECK(attempts >= 0),
                        correct INTEGER NOT NULL CHECK(correct >= 0 AND correct <= attempts),
                        updated_at TEXT NOT NULL,
                        PRIMARY KEY(course_code, module_id)
                    );

                    CREATE TABLE IF NOT EXISTS code_feedback (
                        feedback_id TEXT PRIMARY KEY,
                        course_code TEXT NOT NULL,
                        module_id TEXT NOT NULL,
                        exercise_id TEXT NOT NULL,
                        source_code TEXT NOT NULL,
                        correctness TEXT NOT NULL,
                        complexity TEXT NOT NULL,
                        best_practices TEXT NOT NULL,
                        improvement TEXT NOT NULL,
                        created_at TEXT NOT NULL
                    );
                    CREATE INDEX IF NOT EXISTS idx_code_feedback_exercise
                        ON code_feedback(course_code, module_id, exercise_id, created_at);
                    """
                )
            self._connection.execute(f"PRAGMA user_version = {_SCHEMA_VERSION}")

    @staticmethod
    def _flashcard_from_row(row: sqlite3.Row) -> FlashcardRecord:
        return FlashcardRecord(
            card_id=str(row["card_id"]),
            course_code=str(row["course_code"]),
            module_id=str(row["module_id"]),
            front=str(row["front"]),
            back=str(row["back"]),
            source_hash=str(row["source_hash"]),
            created_at=str(row["created_at"]),
        )


__all__ = ["AILearningStore", "FlashcardRecord", "GeneratedQuestion"]
