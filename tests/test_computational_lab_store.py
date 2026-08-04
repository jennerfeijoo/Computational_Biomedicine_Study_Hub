"""Persistence tests for computational laboratory notebooks."""

from __future__ import annotations

from computational_biomedicine_study_hub.content.labs import DM857_LAB_01
from computational_biomedicine_study_hub.learning.computational_labs import (
    LabAttempt,
    LabNotebookSnapshot,
)
from computational_biomedicine_study_hub.storage.computational_lab_store import (
    ComputationalLabStore,
)
from computational_biomedicine_study_hub.storage.sqlite_progress_store import (
    SQLiteProgressStore,
)


def test_in_memory_lab_store_roundtrip_is_namespaced() -> None:
    progress = SQLiteProgressStore(":memory:")
    try:
        store = ComputationalLabStore.for_progress_store(progress)
        task = DM857_LAB_01.tasks[0]
        attempt = LabAttempt.new(DM857_LAB_01).with_response(
            task.task_id,
            "A persistent answer that is long enough for the laboratory.",
        )
        store.save(LabNotebookSnapshot((attempt,)))

        restored = store.load()

        assert restored is not None
        assert (
            restored.attempt_for(DM857_LAB_01)
            .response_for(task.task_id)
            .startswith("A persistent")
        )
    finally:
        progress.close()
