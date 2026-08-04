"""Regression tests for controlled multi-file workspace execution."""

from __future__ import annotations

from pathlib import Path

from computational_biomedicine_study_hub.learning.scientific_workspace import (
    ScientificWorkspaceTemplate,
    WorkspaceExecutionMode,
    WorkspaceExecutionStatus,
    WorkspaceFileRole,
    WorkspaceFileTemplate,
)
from computational_biomedicine_study_hub.learning.scientific_workspace_execution import (
    ScientificWorkspaceRunner,
)
from computational_biomedicine_study_hub.storage.scientific_workspace_manager import (
    ScientificWorkspaceManager,
)


def _template(source: str) -> ScientificWorkspaceTemplate:
    return ScientificWorkspaceTemplate(
        workspace_id="execution.workspace",
        lab_id="execution.lab",
        version="1.0.0",
        files=(
            WorkspaceFileTemplate(
                "student/main.py",
                source,
                WorkspaceFileRole.SOURCE,
                editable=True,
            ),
            WorkspaceFileTemplate(
                "tests/check.py",
                "from pathlib import Path\n"
                "value = (Path('output.txt').read_text(encoding='utf-8')).strip()\n"
                "assert value == '42', value\n"
                "print('tests passed')\n",
                WorkspaceFileRole.TEST,
            ),
        ),
        entrypoint="student/main.py",
        test_entrypoint="tests/check.py",
        allowed_import_roots=frozenset({"pathlib"}),
        timeout_seconds=5.0,
    )


def test_workspace_runner_executes_authored_script_and_tests(tmp_path: Path) -> None:
    template = _template("from pathlib import Path\nPath('output.txt').write_text('42')\nprint(42)\n")
    manager = ScientificWorkspaceManager(tmp_path)
    workspace = manager.materialize(template)
    runner = ScientificWorkspaceRunner()

    run_result = runner.run(template, workspace, WorkspaceExecutionMode.RUN)
    test_result = runner.run(template, workspace, WorkspaceExecutionMode.TEST)

    assert run_result.status is WorkspaceExecutionStatus.PASSED
    assert run_result.stdout.strip() == "42"
    assert test_result.status is WorkspaceExecutionStatus.PASSED
    assert "tests passed" in test_result.stdout


def test_workspace_runner_rejects_unauthorized_network_import(tmp_path: Path) -> None:
    template = _template("import socket\nprint(socket.gethostname())\n")
    manager = ScientificWorkspaceManager(tmp_path)
    workspace = manager.materialize(template)

    result = ScientificWorkspaceRunner().run(
        template,
        workspace,
        WorkspaceExecutionMode.RUN,
    )

    assert result.status is WorkspaceExecutionStatus.REJECTED
    assert "not authorized" in result.stderr


def test_workspace_runner_blocks_writes_outside_workspace(tmp_path: Path) -> None:
    template = _template("from pathlib import Path\nPath('../outside.txt').write_text('blocked')\n")
    manager = ScientificWorkspaceManager(tmp_path / "root")
    workspace = manager.materialize(template)

    result = ScientificWorkspaceRunner().run(
        template,
        workspace,
        WorkspaceExecutionMode.RUN,
    )

    assert result.status is WorkspaceExecutionStatus.FAILED
    assert "outside the laboratory workspace" in result.stderr
    assert not (workspace.parent / "outside.txt").exists()
