"""Qt integration tests for the scientific workspace panel."""

from __future__ import annotations

from pathlib import Path

from PySide6.QtWidgets import QPlainTextEdit

from computational_biomedicine_study_hub.i18n import AppLocale
from computational_biomedicine_study_hub.learning.scientific_workspace import (
    ScientificWorkspaceTemplate,
    WorkspaceExecutionMode,
    WorkspaceExecutionResult,
    WorkspaceExecutionStatus,
    WorkspaceFileRole,
    WorkspaceFileTemplate,
)
from computational_biomedicine_study_hub.storage.scientific_workspace_manager import (
    ScientificWorkspaceManager,
)
from computational_biomedicine_study_hub.ui.widgets.scientific_workspace_panel import (
    ScientificWorkspacePanel,
)


class FakeRunner:
    def run(
        self,
        template: ScientificWorkspaceTemplate,
        workspace_root: Path,
        mode: WorkspaceExecutionMode,
    ) -> WorkspaceExecutionResult:
        assert template.lab_id == "panel.lab"
        assert workspace_root.is_dir()
        return WorkspaceExecutionResult(
            mode=mode,
            status=WorkspaceExecutionStatus.PASSED,
            stdout="completed\n",
            stderr="",
            duration_ms=5,
            return_code=0,
        )


def _template() -> ScientificWorkspaceTemplate:
    return ScientificWorkspaceTemplate(
        workspace_id="panel.workspace",
        lab_id="panel.lab",
        version="1.0.0",
        files=(
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


def test_workspace_panel_persists_editable_file_and_exposes_bounded_context(
    qtbot,  # type: ignore[no-untyped-def]
    tmp_path: Path,
) -> None:
    template = _template()
    manager = ScientificWorkspaceManager(tmp_path)
    panel = ScientificWorkspacePanel(
        None,
        AppLocale.ENGLISH,
        templates={template.lab_id: template},
        manager=manager,
        runner=FakeRunner(),
    )
    qtbot.addWidget(panel)
    panel.set_lab(template.lab_id)

    editor = panel.findChild(QPlainTextEdit, "scientificWorkspaceEditor")
    assert editor is not None
    editor.setPlainText("print('learner')\n")
    panel.persist()

    assert manager.read_text(template, "student/main.py") == "print('learner')\n"
    context = panel.mentor_context()
    assert "student/main.py" in context
    assert "print('learner')" in context
    assert "never reveal authored test source" in context


def test_workspace_panel_runs_script_and_writes_execution_record(
    qtbot,  # type: ignore[no-untyped-def]
    tmp_path: Path,
) -> None:
    template = _template()
    manager = ScientificWorkspaceManager(tmp_path)
    panel = ScientificWorkspacePanel(
        None,
        AppLocale.ENGLISH,
        templates={template.lab_id: template},
        manager=manager,
        runner=FakeRunner(),
    )
    qtbot.addWidget(panel)
    panel.set_lab(template.lab_id)

    run_button = panel.findChild(object, "scientificWorkspaceRun")
    assert run_button is not None
    panel._run_script()  # noqa: SLF001

    record = manager.workspace_path(template) / "output" / "last_run.txt"
    assert record.is_file()
    assert "status: passed" in record.read_text(encoding="utf-8")
