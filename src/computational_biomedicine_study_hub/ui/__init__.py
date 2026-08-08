"""UI package initialization and shared floating tutor presentation hooks."""

from __future__ import annotations

from PySide6.QtCore import QPoint, Qt
from PySide6.QtGui import QMouseEvent, QResizeEvent
from PySide6.QtWidgets import QSizeGrip, QSizePolicy

from . import widgets as _widgets_package
from .widgets import floating_tutor_chat as _floating_tutor_chat


class _TutorResizeGrip(QSizeGrip):
    """Resize the floating tutor panel itself rather than the application window."""

    def __init__(self, parent) -> None:
        super().__init__(parent)
        self.setCursor(Qt.CursorShape.SizeFDiagCursor)
        self._start_global: QPoint | None = None
        self._start_size = None

    def mousePressEvent(self, event: QMouseEvent) -> None:  # noqa: N802
        if event.button() == Qt.MouseButton.LeftButton:
            panel = self.parentWidget()
            if panel is not None:
                self._start_global = event.globalPosition().toPoint()
                self._start_size = panel.size()
                event.accept()
                return
        super().mousePressEvent(event)

    def mouseMoveEvent(self, event: QMouseEvent) -> None:  # noqa: N802
        if self._start_global is None or self._start_size is None:
            return
        panel = self.parentWidget()
        if panel is None:
            return
        delta = event.globalPosition().toPoint() - self._start_global
        panel.resize(self._start_size.width() + delta.x(), self._start_size.height() + delta.y())
        event.accept()

    def mouseReleaseEvent(self, event: QMouseEvent) -> None:  # noqa: N802
        self._start_global = None
        self._start_size = None
        event.accept()


class _ResizableFloatingTutorChat(_floating_tutor_chat.FloatingTutorChat):
    """Floating tutor with hidden context/observation metadata and a user-resizable viewport."""

    MIN_WIDTH = 420
    MAX_WIDTH = 960
    MIN_HEIGHT = 300
    MAX_HEIGHT = 900

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self._context.hide()
        self._note_frame.hide()
        self.setMinimumSize(self.MIN_WIDTH, self.MIN_HEIGHT)
        self.setMaximumSize(self.MAX_WIDTH, self.MAX_HEIGHT)
        self.setSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Preferred)
        self._transcript.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        self._transcript.setMinimumHeight(180)
        self._transcript.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        self._transcript.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOn)
        self._resize_grip = _TutorResizeGrip(self)
        self._resize_grip.setFixedSize(18, 18)
        self._resize_grip.raise_()
        self._position_resize_grip()

    def resizeEvent(self, event: QResizeEvent) -> None:  # noqa: N802
        super().resizeEvent(event)
        self._position_resize_grip()

    def _position_resize_grip(self) -> None:
        if hasattr(self, "_resize_grip"):
            margin = 3
            self._resize_grip.move(self.width() - self._resize_grip.width() - margin, self.height() - self._resize_grip.height() - margin)
            self._resize_grip.raise_()


_original_position_floating_tutor = _floating_tutor_chat.position_floating_tutor


def _position_resizable_floating_tutor(panel, launcher, host) -> None:
    """Preserve the original anchoring while keeping the panel resizable."""
    _original_position_floating_tutor(panel, launcher, host)
    if isinstance(panel, _ResizableFloatingTutorChat):
        panel.setMinimumSize(panel.MIN_WIDTH, panel.MIN_HEIGHT)
        panel.setMaximumSize(panel.MAX_WIDTH, panel.MAX_HEIGHT)
        panel._position_resize_grip()


_floating_tutor_chat.FloatingTutorChat = _ResizableFloatingTutorChat
_floating_tutor_chat.position_floating_tutor = _position_resizable_floating_tutor
_widgets_package.FloatingTutorChat = _ResizableFloatingTutorChat
_widgets_package.position_floating_tutor = _position_resizable_floating_tutor
