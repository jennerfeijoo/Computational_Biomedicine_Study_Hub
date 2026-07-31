"""Domain and persistence tests for DM847 written assessment support."""

from __future__ import annotations

from datetime import UTC, datetime

import pytest

from computational_biomedicine_study_hub.content.dm847 import BUNDLES
from computational_biomedicine_study_hub.learning.dm847_written_assessment import (
    DM847_WRITTEN_PROMPTS,
    WrittenAssessmentSnapshot,
    WrittenAssessmentSnapshotError,
    WrittenFeedbackMode,
    WrittenTaskKind,
)
from computational_biomedicine_study_hub.storage import (
    DM847WrittenAssessmentStore,
    SQLiteProgressStore,
)


def test_written_prompt_catalog_maps_to_real_dm847_objectives() -> None:
    modules = {bundle.module.module_id: bundle.module for bundle in BUNDLES}

    assert len(DM847_WRITTEN_PROMPTS) == 10
    assert {item.module_id for item in DM847_WRITTEN_PROMPTS} == set(modules)
    assert any(item.kind is WrittenTaskKind.ESSAY for item in DM847_WRITTEN_PROMPTS)
    for prompt in DM847_WRITTEN_PROMPTS:
        objective_ids = {item.objective_id for item in modules[prompt.module_id].objectives}
        assert set(prompt.objective_ids) <= objective_ids


def test_written_snapshot_round_trip_and_edit_invalidation() -> None:
    timestamp = datetime(2026, 7, 31, 15, 0, tzinfo=UTC)
    snapshot = WrittenAssessmentSnapshot.empty(now=timestamp)
    prompt_id = DM847_WRITTEN_PROMPTS[0].prompt_id
    snapshot = snapshot.with_response(
        prompt_id,
        "A sufficiently developed learner response with explicit assumptions and validation.",
        now=timestamp,
    ).with_feedback(
        prompt_id,
        feedback_text="The response should distinguish sequence from annotation.",
        feedback_mode=WrittenFeedbackMode.CONTENT_REVIEW,
        source_ids=("dm847.m01.overview",),
        now=timestamp,
    )

    restored = WrittenAssessmentSnapshot.from_json(snapshot.to_json())

    assert restored == snapshot
    changed = restored.with_response(prompt_id, "A revised learner response.")
    assert changed.draft(prompt_id).feedback_text == ""
    assert changed.draft(prompt_id).feedback_mode is None
    assert changed.draft(prompt_id).source_ids == ()


def test_written_snapshot_rejects_corrupt_or_unknown_documents() -> None:
    with pytest.raises(WrittenAssessmentSnapshotError):
        WrittenAssessmentSnapshot.from_json("not-json")
    with pytest.raises(WrittenAssessmentSnapshotError):
        WrittenAssessmentSnapshot.from_json(
            '{"schema_version":99,"active_prompt_id":"dm847.w01","drafts":[],"updated_at":"2026-07-31T15:00:00+00:00"}'
        )


def test_written_store_persists_across_progress_store_lifetime() -> None:
    progress_store = SQLiteProgressStore(":memory:")
    store = DM847WrittenAssessmentStore.for_progress_store(progress_store)
    prompt_id = DM847_WRITTEN_PROMPTS[-1].prompt_id
    snapshot = (
        WrittenAssessmentSnapshot.empty()
        .with_active_prompt(prompt_id)
        .with_response(
            prompt_id,
            "Nested validation must keep every learned preprocessing step inside training folds.",
        )
    )

    store.save(snapshot)

    restored = DM847WrittenAssessmentStore.for_progress_store(progress_store).load()
    assert restored is not None
    assert restored.active_prompt_id == prompt_id
    assert "Nested validation" in restored.draft(prompt_id).response_text
    progress_store.close()
