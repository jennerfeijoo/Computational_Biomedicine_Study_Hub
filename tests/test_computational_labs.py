"""Regression tests for the computational laboratory domain and pilot content."""

from __future__ import annotations

from datetime import UTC, datetime

import pytest

from computational_biomedicine_study_hub.content.labs import DM857_LAB_01, LABS
from computational_biomedicine_study_hub.i18n.locales import AppLocale
from computational_biomedicine_study_hub.learning.computational_labs import (
    LabAttempt,
    LabNotebookSnapshot,
    LabSnapshotError,
    LabStage,
    LabTaskKind,
    render_lab_record,
)
from computational_biomedicine_study_hub.learning.python_execution import (
    ExecutionStatus,
    PythonExecutionRequest,
    PythonSubprocessRunner,
)

_REFERENCE_IMPLEMENTATION = '''def summarize_measurements(values, lower, upper):
    if isinstance(lower, bool) or isinstance(upper, bool):
        raise TypeError("limits must be numeric")
    if not isinstance(lower, (int, float)) or not isinstance(upper, (int, float)):
        raise TypeError("limits must be numeric")
    if lower > upper:
        raise ValueError("lower cannot exceed upper")
    valid = []
    invalid_count = 0
    for value in values:
        if (
            isinstance(value, (int, float))
            and not isinstance(value, bool)
            and lower <= value <= upper
        ):
            valid.append(value)
        else:
            invalid_count += 1
    mean = None if not valid else round(sum(valid) / len(valid), 2)
    return len(valid), invalid_count, mean
'''


def test_pilot_lab_covers_the_complete_pedagogical_cycle() -> None:
    assert LABS == (DM857_LAB_01,)
    assert tuple(dict.fromkeys(task.stage for task in DM857_LAB_01.tasks)) == tuple(LabStage)
    assert DM857_LAB_01.estimated_minutes == 120
    assert all(task.objective_ids for task in DM857_LAB_01.tasks)
    for locale in AppLocale:
        assert DM857_LAB_01.title.text(locale)
        assert DM857_LAB_01.research_question.text(locale)
        assert "SDU" in DM857_LAB_01.disclaimer.text(locale)


def test_reference_implementation_passes_every_python_checkpoint() -> None:
    runner = PythonSubprocessRunner()
    python_tasks = tuple(
        task for task in DM857_LAB_01.tasks if task.kind is LabTaskKind.PYTHON
    )
    assert len(python_tasks) == 2
    for task in python_tasks:
        result = runner.run(
            PythonExecutionRequest(
                source=f"{_REFERENCE_IMPLEMENTATION}\n{task.verification_source}",
                expected_output=task.expected_output,
                timeout_seconds=4.0,
            )
        )
        assert result.status is ExecutionStatus.PASSED, result.stderr


def test_attempt_roundtrip_preserves_evidence_and_progress() -> None:
    now = datetime(2026, 8, 4, 10, 0, tzinfo=UTC)
    attempt = LabAttempt.new(DM857_LAB_01, now=now)
    first_task = DM857_LAB_01.tasks[0]
    attempt = attempt.with_response(
        first_task.task_id,
        "A sufficiently detailed learner response.",
        now=now,
    )
    attempt = attempt.mark_complete(first_task.task_id, now=now)
    attempt = attempt.with_requested_hint(first_task.task_id, now=now)
    snapshot = LabNotebookSnapshot((attempt,))

    restored = LabNotebookSnapshot.from_json(snapshot.to_json()).attempt_for(DM857_LAB_01)

    assert restored.response_for(first_task.task_id).startswith("A sufficiently")
    assert first_task.task_id in restored.completed_tasks
    assert restored.hint_level_for(first_task.task_id) == 1
    assert restored.completion_ratio(DM857_LAB_01) == pytest.approx(1 / 7)


def test_export_record_never_exposes_hidden_verification_source() -> None:
    task = next(task for task in DM857_LAB_01.tasks if task.kind is LabTaskKind.PYTHON)
    attempt = LabAttempt.new(DM857_LAB_01).with_response(
        task.task_id,
        _REFERENCE_IMPLEMENTATION,
    )

    record = render_lab_record(DM857_LAB_01, attempt, AppLocale.ENGLISH)

    assert task.verification_source not in record
    assert _REFERENCE_IMPLEMENTATION in record
    assert "Internal preparation" in record


def test_invalid_notebook_json_is_rejected() -> None:
    with pytest.raises(LabSnapshotError):
        LabNotebookSnapshot.from_json('{"schema_version": 1, "attempts": "invalid"}')
