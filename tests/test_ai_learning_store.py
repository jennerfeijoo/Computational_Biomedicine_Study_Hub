from __future__ import annotations

from pathlib import Path

from computational_biomedicine_study_hub.storage.ai_learning_store import (
    AILearningStore,
    FlashcardRecord,
    GeneratedQuestion,
)


def test_ai_store_migrates_and_persists_flashcards(tmp_path: Path) -> None:
    database = tmp_path / "ai.sqlite3"
    with AILearningStore(database) as store:
        assert store.schema_version == 1
        store.save_flashcards(
            (
                FlashcardRecord(
                    "card-1",
                    "DM857",
                    "module-01",
                    "What is a function?",
                    "A reusable unit of computation.",
                    "hash",
                    "2026-08-10T00:00:00+00:00",
                ),
            )
        )
        assert len(store.list_flashcards("DM857", "module-01")) == 1


def test_module_performance_is_updated_atomically(tmp_path: Path) -> None:
    with AILearningStore(tmp_path / "ai.sqlite3") as store:
        question = GeneratedQuestion(
            "q-1",
            "DM857",
            "module-01",
            "multiple_choice",
            "Question",
            ("A", "B"),
            "A",
            "Because A.",
            (),
            "2026-08-10T00:00:00+00:00",
        )
        store.save_generated_questions((question,))
        store.record_question_attempt(
            question_id="q-1",
            course_code="DM857",
            module_id="module-01",
            is_correct=False,
            user_answer="B",
            feedback="Incorrect.",
        )
        store.record_question_attempt(
            question_id="q-1",
            course_code="DM857",
            module_id="module-01",
            is_correct=True,
            user_answer="A",
            feedback="Correct.",
        )
        assert store.module_performance("DM857")["module-01"] == (2, 1)
