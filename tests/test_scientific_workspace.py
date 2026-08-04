"""Regression tests for persistent scientific workspace definitions and storage."""

from __future__ import annotations

from pathlib import Path

import pytest

from computational_biomedicine_study_hub.learning.scientific_workspace import (
    ScientificWorkspaceTemplate,
    WorkspaceDefinitionError,
    WorkspaceFileRole,
    WorkspaceFileTemplate,
    normalize_workspace_path,
)
from computational_biomedicine_study_hub.storage.scientific_workspace_manager import (
    ScientificWorkspaceManager,
)


def _template() -> ScientificWorkspaceTemplate:
    return ScientificWorkspaceTemplate(
        workspace_id="test.workspace",
        lab_id="test.lab",
        version="1.0.0",
        files=(
            WorkspaceFileTemplate(
                "README.md",
                "authored",
                WorkspaceFileRole.README,
            ),
            WorkspaceFileTemplate(
                "student/main.py",
                "print('starter')\n",
                WorkspaceFileRole.SOURCE,
                editable=True,
            ),
            WorkspaceFileTemplate(
                "tests/check.py",
                "print('tests')\n",
                WorkspaceFileRole.TEST,
            ),
        ),
        entrypoint="student/main.py",
        test_entrypoint="tests/check.py",
        allowed_import_roots=frozenset(),
    )


def test_workspace_paths_reject_escape_and_absolute_locations() -> None:
    assert normalize_workspace_path("student/main.py") == "student/main.py"
    with pytest.raises(WorkspaceDefinitionError):
        normalize_workspace_path("../outside.py")
    with pytest.raises(WorkspaceDefinitionError):
        normalize_workspace_path("/tmp/outside.py")


def test_materialization_preserves_learner_files_and_refreshes_authored_files(
    tmp_path: Path,
) -> None:
    template = _template()
    manager = ScientificWorkspaceManager(tmp_path)
    workspace = manager.materialize(template)

    manager.write_text(template, "student/main.py", "print('learner')\n")
    (workspace / "README.md").write_text("tampered", encoding="utf-8")
    manager.materialize(template)

    assert manager.read_text(template, "student/main.py") == "print('learner')\n"
    assert manager.read_text(template, "README.md") == "authored"
    assert (workspace / ".workspace-manifest.json").is_file()


def test_read_only_workspace_files_cannot_be_replaced(tmp_path: Path) -> None:
    template = _template()
    manager = ScientificWorkspaceManager(tmp_path)
    manager.materialize(template)

    with pytest.raises(WorkspaceDefinitionError, match="read-only"):
        manager.write_text(template, "README.md", "changed")


def test_execution_records_remain_inside_output(tmp_path: Path) -> None:
    template = _template()
    manager = ScientificWorkspaceManager(tmp_path)

    record = manager.write_execution_record(template, "last_run.txt", "passed")

    assert record.read_text(encoding="utf-8") == "passed"
    assert record.parent.name == "output"
