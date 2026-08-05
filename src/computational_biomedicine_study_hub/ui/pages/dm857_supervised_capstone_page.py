"""DM857 capstone page extended with longitudinal weekly project supervision."""

from __future__ import annotations

from datetime import date

from PySide6.QtWidgets import QScrollArea, QVBoxLayout, QWidget

from ...i18n.locales import DEFAULT_LOCALE, AppLocale
from ...storage.dm857_capstone_store import DM857CapstoneStore
from ...storage.dm857_weekly_supervision_store import DM857WeeklySupervisionStore
from ...storage.sqlite_progress_store import SQLiteProgressStore
from ..widgets.dm857_weekly_supervision_panel import DM857WeeklySupervisionPanel
from .dm857_capstone_page import DM857CapstonePage


class DM857SupervisedCapstonePage(DM857CapstonePage):
    """Add a persistent weekly evidence cycle to the existing capstone scaffold."""

    def __init__(
        self,
        progress_store: SQLiteProgressStore | None,
        locale: AppLocale = DEFAULT_LOCALE,
        *,
        capstone_store: DM857CapstoneStore | None = None,
        supervision_store: DM857WeeklySupervisionStore | None = None,
        today: date | None = None,
        parent: QWidget | None = None,
    ) -> None:
        super().__init__(
            progress_store,
            locale,
            capstone_store=capstone_store,
            parent=parent,
        )
        self._weekly_supervision = DM857WeeklySupervisionPanel(
            progress_store,
            locale,
            supervision_store=supervision_store,
            today=today,
            parent=self,
        )
        self._weekly_supervision.mentor_requested.connect(self.mentor_requested.emit)
        self._insert_weekly_panel()

    @property
    def weekly_supervision_panel(self) -> DM857WeeklySupervisionPanel:
        """Return the longitudinal project-supervision panel."""

        return self._weekly_supervision

    def persist(self) -> None:
        """Persist both capstone milestones and longitudinal weekly evidence."""

        weekly_panel = getattr(self, "_weekly_supervision", None)
        if isinstance(weekly_panel, DM857WeeklySupervisionPanel):
            weekly_panel.persist()
        super().persist()

    def mentor_context(self) -> str:
        """Combine project scaffold, weekly evidence and technical-station context."""

        return "\n".join(
            (
                super().mentor_context(),
                self._weekly_supervision.mentor_context(),
            )
        )

    def _insert_weekly_panel(self) -> None:
        scroll = self.findChild(QScrollArea, "capstoneScroll")
        if scroll is None:
            raise RuntimeError("DM857 capstone scroll body is unavailable.")
        body = scroll.widget()
        if body is None:
            raise RuntimeError("DM857 capstone scroll body is unavailable.")
        body_layout = body.layout()
        if not isinstance(body_layout, QVBoxLayout):
            raise RuntimeError("DM857 capstone body must use a vertical layout.")
        station_index = body_layout.indexOf(self.technical_station_panel)
        insert_index = station_index if station_index >= 0 else max(0, body_layout.count() - 1)
        body_layout.insertWidget(insert_index, self._weekly_supervision)


__all__ = ["DM857SupervisedCapstonePage"]
