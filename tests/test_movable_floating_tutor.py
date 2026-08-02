from __future__ import annotations

from pathlib import Path

from PySide6.QtCore import QPoint, QSettings, Qt
from PySide6.QtWidgets import QApplication, QFrame, QPushButton, QWidget

from computational_biomedicine_study_hub.ui.widgets.floating_tutor_chat import (
    FloatingTutorChat,
    position_floating_tutor,
)


def _settings(path: Path) -> QSettings:
    return QSettings(str(path), QSettings.Format.IniFormat)


def test_floating_tutor_can_be_dragged_and_keeps_its_position(
    qapp: QApplication,
    qtbot,
    tmp_path: Path,
) -> None:
    host = QWidget()
    host.resize(1000, 800)
    qtbot.addWidget(host)

    launcher = QPushButton("Tutor", host)
    panel = FloatingTutorChat(
        settings=_settings(tmp_path / "settings.ini"),
        context_provider=lambda: "DM857 · Practice",
        parent=host,
    )
    host.show()
    panel.show_panel()
    position_floating_tutor(panel, launcher, host)
    qapp.processEvents()

    original_position = panel.pos()
    handle = panel.findChild(QFrame, "floatingTutorDragHandle")
    assert handle is not None

    qtbot.mousePress(
        handle,
        Qt.MouseButton.LeftButton,
        pos=QPoint(40, 15),
    )
    qtbot.mouseMove(handle, QPoint(180, 75))
    qtbot.mouseRelease(
        handle,
        Qt.MouseButton.LeftButton,
        pos=QPoint(180, 75),
    )
    qapp.processEvents()

    assert panel.has_custom_position
    assert panel.pos() != original_position
    moved_position = panel.pos()

    position_floating_tutor(panel, launcher, host)

    assert panel.pos() == moved_position
    assert panel.geometry().left() >= 0
    assert panel.geometry().top() >= 0
    assert panel.geometry().right() < host.width()
    assert panel.geometry().bottom() < host.height()
