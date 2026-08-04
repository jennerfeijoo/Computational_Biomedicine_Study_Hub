"""Multi-file scientific workspace editor embedded in computational laboratories."""

from __future__ import annotations

import tempfile
from collections.abc import Mapping
from pathlib import Path

from PySide6.QtCore import QSignalBlocker, Slot
from PySide6.QtWidgets import (
    QComboBox,
    QFrame,
    QHBoxLayout,
    QLabel,
    QPlainTextEdit,
    QPushButton,
    QVBoxLayout,
    QWidget,
)

from ...content.labs.workspaces import WORKSPACE_TEMPLATES
from ...i18n.locales import DEFAULT_LOCALE, AppLocale
from ...i18n.scientific_workspace_copy import (
    ScientificWorkspaceCopyKey,
    scientific_workspace_text,
)
from ...learning.scientific_workspace import (
    ScientificWorkspaceTemplate,
    WorkspaceDefinitionError,
    WorkspaceExecutionMode,
)
from ...learning.scientific_workspace_execution import (
    ScientificWorkspaceRunner,
    ScientificWorkspaceRunnerProtocol,
)
from ...storage.scientific_workspace_manager import ScientificWorkspaceManager
from ...storage.sqlite_progress_store import SQLiteProgressStore


class ScientificWorkspacePanel(QFrame):
    """Persist, inspect, execute, and test one authored laboratory workspace."""

    def __init__(
        self,
        progress_store: SQLiteProgressStore | None,
        locale: AppLocale = DEFAULT_LOCALE,
        *,
        templates: Mapping[str, ScientificWorkspaceTemplate] = WORKSPACE_TEMPLATES,
        manager: ScientificWorkspaceManager | None = None,
        runner: ScientificWorkspaceRunnerProtocol | None = None,
        parent: QWidget | None = None,
    ) -> None:
        super().__init__(parent)
        self.setObjectName("scientificWorkspacePanel")
        self.setProperty("cardRole", "surface")
        self._locale = locale
        self._templates = dict(templates)
        if manager is not None:
            self._manager = manager
        elif progress_store is not None:
            self._manager = ScientificWorkspaceManager.for_progress_store(progress_store)
        else:
            self._manager = ScientificWorkspaceManager(
                Path(tempfile.mkdtemp(prefix="cb-study-workspaces-"))
            )
        self._runner: ScientificWorkspaceRunnerProtocol = runner or ScientificWorkspaceRunner()
        self._template: ScientificWorkspaceTemplate | None = None
        self._current_path = ""
        self._loading = False
        self._dirty = False
        self._last_execution = ""

        layout = QVBoxLayout(self)
        layout.setContentsMargins(16, 16, 16, 16)
        layout.setSpacing(10)

        self._title = QLabel(self._text(ScientificWorkspaceCopyKey.TITLE))
        self._title.setObjectName("sectionHeading")
        layout.addWidget(self._title)

        self._description = QLabel(self._text(ScientificWorkspaceCopyKey.DESCRIPTION))
        self._description.setWordWrap(True)
        self._description.setProperty("semanticTone", "muted")
        layout.addWidget(self._description)

        self._location = QLabel()
        self._location.setWordWrap(True)
        self._location.setProperty("semanticTone", "subtle")
        layout.addWidget(self._location)

        selector_row = QHBoxLayout()
        selector_label = QLabel(self._text(ScientificWorkspaceCopyKey.FILE))
        selector_label.setObjectName("fieldLabel")
        self._selector = QComboBox()
        self._selector.setObjectName("scientificWorkspaceFileSelector")
        self._selector.currentIndexChanged.connect(self._select_file)
        self._file_role = QLabel()
        self._file_role.setProperty("semanticTone", "subtle")
        selector_row.addWidget(selector_label)
        selector_row.addWidget(self._selector, 1)
        selector_row.addWidget(self._file_role)
        layout.addLayout(selector_row)

        self._editor = QPlainTextEdit()
        self._editor.setObjectName("scientificWorkspaceEditor")
        self._editor.setMinimumHeight(260)
        self._editor.textChanged.connect(self._editor_changed)
        layout.addWidget(self._editor)

        actions = QHBoxLayout()
        self._save = QPushButton(self._text(ScientificWorkspaceCopyKey.SAVE_FILE))
        self._save.setObjectName("scientificWorkspaceSave")
        self._save.clicked.connect(self._save_clicked)
        self._run = QPushButton(self._text(ScientificWorkspaceCopyKey.RUN_SCRIPT))
        self._run.setObjectName("scientificWorkspaceRun")
        self._run.setProperty("buttonRole", "primary")
        self._run.clicked.connect(self._run_script)
        self._tests = QPushButton(self._text(ScientificWorkspaceCopyKey.RUN_TESTS))
        self._tests.setObjectName("scientificWorkspaceTests")
        self._tests.clicked.connect(self._run_tests)
        self._refresh = QPushButton(self._text(ScientificWorkspaceCopyKey.REFRESH))
        self._refresh.setObjectName("scientificWorkspaceRefresh")
        self._refresh.clicked.connect(self._reload)
        for button in (self._save, self._run, self._tests, self._refresh):
            actions.addWidget(button)
        actions.addStretch(1)
        layout.addLayout(actions)

        output_label = QLabel(self._text(ScientificWorkspaceCopyKey.OUTPUT))
        output_label.setObjectName("fieldLabel")
        layout.addWidget(output_label)
        self._output = QPlainTextEdit()
        self._output.setObjectName("scientificWorkspaceOutput")
        self._output.setReadOnly(True)
        self._output.setMaximumHeight(190)
        layout.addWidget(self._output)

        self._status = QLabel()
        self._status.setWordWrap(True)
        self._status.setProperty("semanticTone", "muted")
        layout.addWidget(self._status)
        self._set_enabled(False)
        self._status.setText(self._text(ScientificWorkspaceCopyKey.NO_WORKSPACE))

    @property
    def current_template(self) -> ScientificWorkspaceTemplate | None:
        """Return the selected authored workspace template."""

        return self._template

    @property
    def current_file(self) -> str:
        """Return the active authored file path, or an empty string."""

        return self._current_path

    def set_lab(self, lab_id: str) -> None:
        """Persist the prior file and load the workspace attached to a laboratory."""

        self.persist()
        self._template = self._templates.get(lab_id)
        self._current_path = ""
        self._last_execution = ""
        self._output.clear()
        if self._template is None:
            blocker = QSignalBlocker(self._selector)
            self._selector.clear()
            del blocker
            self._editor.clear()
            self._location.clear()
            self._file_role.clear()
            self._set_enabled(False)
            self._status.setText(self._text(ScientificWorkspaceCopyKey.NO_WORKSPACE))
            return
        try:
            workspace = self._manager.materialize(self._template)
        except WorkspaceDefinitionError as exc:
            self._set_enabled(False)
            self._status.setText(self._text(ScientificWorkspaceCopyKey.LOAD_FAILED, error=str(exc)))
            return
        self._location.setText(self._text(ScientificWorkspaceCopyKey.LOCATION, path=str(workspace)))
        blocker = QSignalBlocker(self._selector)
        self._selector.clear()
        for file_template in self._template.files:
            self._selector.addItem(
                file_template.relative_path, userData=file_template.relative_path
            )
        self._selector.setCurrentIndex(0)
        del blocker
        self._set_enabled(True)
        self._current_path = str(self._selector.itemData(0) or "")
        self._load_selected_file()
        self._status.setText(self._text(ScientificWorkspaceCopyKey.MATERIALIZED))

    def persist(self) -> None:
        """Save the active learner-owned file without altering authored read-only files."""

        template = self._template
        if template is None or not self._current_path or not self._dirty:
            return
        file_template = template.file(self._current_path)
        if not file_template.editable:
            self._dirty = False
            return
        try:
            self._manager.write_text(template, self._current_path, self._editor.toPlainText())
        except WorkspaceDefinitionError as exc:
            self._status.setText(self._text(ScientificWorkspaceCopyKey.SAVE_FAILED, error=str(exc)))
            return
        self._dirty = False
        self._status.setText(self._text(ScientificWorkspaceCopyKey.SAVED, path=self._current_path))

    def mentor_context(self) -> str:
        """Return bounded workspace evidence for the Socratic laboratory mentor."""

        template = self._template
        if template is None:
            return "Scientific workspace: not available for this laboratory."
        self.persist()
        active = self._editor.toPlainText()[:8_000]
        execution = self._last_execution[:4_000]
        files = ", ".join(item.relative_path for item in template.files)
        return "\n".join(
            (
                f"Scientific workspace: {template.workspace_id} version {template.version}",
                f"Authored files: {files}",
                f"Active file: {self._current_path or '[none]'}",
                f"Active file content:\n{active or '[blank]'}",
                f"Latest workspace execution:\n{execution or '[none]'}",
                "Workspace mentor policy: reason from the active file and execution evidence; "
                "ask one diagnostic question before suggesting code; never reveal authored test "
                "source; distinguish implementation correctness from biomedical validity.",
            )
        )

    @Slot(int)
    def _select_file(self, index: int) -> None:
        if self._loading or index < 0:
            return
        self.persist()
        self._current_path = str(self._selector.itemData(index) or "")
        self._load_selected_file()

    def _load_selected_file(self) -> None:
        template = self._template
        if template is None or not self._current_path:
            return
        try:
            content = self._manager.read_text(template, self._current_path)
            file_template = template.file(self._current_path)
        except WorkspaceDefinitionError as exc:
            self._status.setText(self._text(ScientificWorkspaceCopyKey.LOAD_FAILED, error=str(exc)))
            return
        self._loading = True
        blocker = QSignalBlocker(self._editor)
        self._editor.setPlainText(content)
        del blocker
        self._editor.setReadOnly(not file_template.editable)
        self._save.setEnabled(file_template.editable)
        role_key = (
            ScientificWorkspaceCopyKey.EDITABLE
            if file_template.editable
            else ScientificWorkspaceCopyKey.READ_ONLY
        )
        self._file_role.setText(self._text(role_key))
        self._dirty = False
        self._loading = False

    @Slot()
    def _editor_changed(self) -> None:
        if self._loading or self._template is None or not self._current_path:
            return
        self._dirty = self._template.file(self._current_path).editable

    @Slot()
    def _save_clicked(self) -> None:
        self._dirty = True
        self.persist()

    @Slot()
    def _run_script(self) -> None:
        self._execute(WorkspaceExecutionMode.RUN)

    @Slot()
    def _run_tests(self) -> None:
        self._execute(WorkspaceExecutionMode.TEST)

    def _execute(self, mode: WorkspaceExecutionMode) -> None:
        template = self._template
        if template is None:
            return
        self.persist()
        try:
            workspace = self._manager.materialize(template)
            result = self._runner.run(template, workspace, mode)
            rendered = result.render()
            record_name = "last_run.txt" if mode is WorkspaceExecutionMode.RUN else "last_tests.txt"
            self._manager.write_execution_record(template, record_name, rendered)
        except WorkspaceDefinitionError as exc:
            self._status.setText(self._text(ScientificWorkspaceCopyKey.LOAD_FAILED, error=str(exc)))
            return
        self._last_execution = rendered
        self._output.setPlainText(rendered)
        key = (
            ScientificWorkspaceCopyKey.RUN_COMPLETE
            if mode is WorkspaceExecutionMode.RUN
            else ScientificWorkspaceCopyKey.TEST_COMPLETE
        )
        self._status.setText(self._text(key, status=result.status.value))

    @Slot()
    def _reload(self) -> None:
        self.persist()
        self._load_selected_file()

    def _set_enabled(self, enabled: bool) -> None:
        self._selector.setEnabled(enabled)
        self._editor.setEnabled(enabled)
        self._save.setEnabled(enabled)
        self._run.setEnabled(enabled)
        self._tests.setEnabled(enabled)
        self._refresh.setEnabled(enabled)

    def _text(self, key: ScientificWorkspaceCopyKey, **values: object) -> str:
        return scientific_workspace_text(self._locale, key, **values)


__all__ = ["ScientificWorkspacePanel"]
