"""Persistent section-based studio for the BMB831 individual English report."""

from __future__ import annotations

from PySide6.QtCore import QTimer, Slot
from PySide6.QtWidgets import (
    QComboBox,
    QGroupBox,
    QLabel,
    QPlainTextEdit,
    QPushButton,
    QScrollArea,
    QVBoxLayout,
    QWidget,
)

from ...i18n.bmb831_report_copy import (
    BMB831ReportCopyKey,
    bmb831_report_section_title,
    bmb831_report_text,
)
from ...i18n.locales import DEFAULT_LOCALE, AppLocale
from ...learning.bmb831_report import (
    BMB831_REPORT_SECTIONS,
    BMB831ReportSnapshot,
    report_section,
)
from ...storage.bmb831_report_store import BMB831ReportStore
from ...storage.sqlite_progress_store import SQLiteProgressStore


class BMB831ReportPage(QWidget):
    """Edit and persist learner-owned English report sections."""

    def __init__(
        self,
        progress_store: SQLiteProgressStore | None,
        locale: AppLocale = DEFAULT_LOCALE,
        *,
        report_store: BMB831ReportStore | None = None,
        parent: QWidget | None = None,
    ) -> None:
        super().__init__(parent)
        self.setObjectName("bmb831ReportPage")
        self._locale = locale
        self._store = report_store
        if self._store is None and progress_store is not None:
            self._store = BMB831ReportStore.for_progress_store(progress_store)
        loaded = self._store.load() if self._store is not None else None
        self._snapshot = loaded or BMB831ReportSnapshot.empty()
        self._loaded_section_id = self._snapshot.active_section_id
        self._loading = False

        self._save_timer = QTimer(self)
        self._save_timer.setSingleShot(True)
        self._save_timer.setInterval(350)
        self._save_timer.timeout.connect(self.persist)

        root = QVBoxLayout(self)
        root.setContentsMargins(0, 0, 0, 0)
        scroll = QScrollArea()
        scroll.setObjectName("bmb831ReportScroll")
        scroll.setWidgetResizable(True)
        body = QWidget()
        body.setObjectName("bmb831ReportBody")
        layout = QVBoxLayout(body)
        layout.setContentsMargins(4, 4, 12, 24)
        layout.setSpacing(14)

        title = QLabel(self._text(BMB831ReportCopyKey.TITLE))
        title.setObjectName("bmb831ReportTitle")
        intro = QLabel(self._text(BMB831ReportCopyKey.INTRO))
        intro.setWordWrap(True)
        boundary = QLabel(self._text(BMB831ReportCopyKey.ENGLISH_BOUNDARY))
        boundary.setObjectName("bmb831EnglishBoundary")
        boundary.setProperty("tone", "warning")
        boundary.setWordWrap(True)
        layout.addWidget(title)
        layout.addWidget(intro)
        layout.addWidget(boundary)

        selector_group = QGroupBox(self._text(BMB831ReportCopyKey.SECTION))
        selector_layout = QVBoxLayout(selector_group)
        self._selector = QComboBox()
        self._selector.setObjectName("bmb831ReportSectionSelector")
        for section in BMB831_REPORT_SECTIONS:
            self._selector.addItem(
                bmb831_report_section_title(locale, section.section_id),
                section.section_id,
            )
        self._selector.currentIndexChanged.connect(self._section_changed)
        selector_layout.addWidget(self._selector)
        layout.addWidget(selector_group)

        checklist_group = QGroupBox(self._text(BMB831ReportCopyKey.CHECKLIST))
        checklist_layout = QVBoxLayout(checklist_group)
        self._checklist = QLabel()
        self._checklist.setObjectName("bmb831ReportChecklist")
        self._checklist.setWordWrap(True)
        checklist_layout.addWidget(self._checklist)
        layout.addWidget(checklist_group)

        draft_group = QGroupBox(self._text(BMB831ReportCopyKey.DRAFT))
        draft_layout = QVBoxLayout(draft_group)
        self._editor = QPlainTextEdit()
        self._editor.setObjectName("bmb831ReportDraft")
        self._editor.setMinimumHeight(300)
        self._editor.textChanged.connect(self._draft_changed)
        draft_layout.addWidget(self._editor)
        self._word_count = QLabel()
        self._word_count.setObjectName("bmb831ReportWordCount")
        draft_layout.addWidget(self._word_count)
        self._save_button = QPushButton(self._text(BMB831ReportCopyKey.SAVE))
        self._save_button.setObjectName("bmb831ReportSaveButton")
        self._save_button.clicked.connect(self.persist)
        draft_layout.addWidget(self._save_button)
        self._save_status = QLabel()
        self._save_status.setObjectName("bmb831ReportSaveStatus")
        draft_layout.addWidget(self._save_status)
        layout.addWidget(draft_group)

        self._progress = QLabel()
        self._progress.setObjectName("bmb831ReportProgress")
        layout.addWidget(self._progress)
        boundary_note = QLabel(self._text(BMB831ReportCopyKey.NO_OFFICIAL_GRADE))
        boundary_note.setWordWrap(True)
        boundary_note.setProperty("tone", "muted")
        layout.addWidget(boundary_note)
        layout.addStretch(1)

        scroll.setWidget(body)
        root.addWidget(scroll)
        self._load_section(self._snapshot.active_section_id)

    @property
    def snapshot(self) -> BMB831ReportSnapshot:
        """Return current state including visible editor text."""

        return self._capture_visible_text()

    @property
    def editor(self) -> QPlainTextEdit:
        """Expose the report editor for integration tests."""

        return self._editor

    @property
    def current_section_id(self) -> str:
        """Return the selected stable section ID."""

        value = self._selector.currentData()
        return str(value or BMB831_REPORT_SECTIONS[0].section_id)

    def select_section(self, section_id: str) -> bool:
        """Select one report section by stable ID."""

        index = self._selector.findData(section_id)
        if index < 0:
            return False
        if index == self._selector.currentIndex():
            self._load_section(section_id)
        else:
            self._selector.setCurrentIndex(index)
        return True

    @Slot()
    def persist(self) -> None:
        """Capture and atomically save the full learner report."""

        self._save_timer.stop()
        self._snapshot = self._capture_visible_text()
        if self._store is not None:
            self._store.save(self._snapshot)
        self._save_status.setText(self._text(BMB831ReportCopyKey.SAVED))
        self._update_counts()

    @Slot(int)
    def _section_changed(self, _index: int) -> None:
        if self._loading:
            return
        self._snapshot = self._capture_visible_text()
        section_id = self.current_section_id
        self._snapshot = self._snapshot.with_active_section(section_id)
        self._load_section(section_id)
        self._schedule_save()

    @Slot()
    def _draft_changed(self) -> None:
        if self._loading:
            return
        self._save_status.clear()
        self._update_counts()
        self._schedule_save()

    def _load_section(self, section_id: str) -> None:
        self._loading = True
        self._loaded_section_id = section_id
        self._snapshot = self._snapshot.with_active_section(section_id)
        index = self._selector.findData(section_id)
        if index >= 0:
            self._selector.setCurrentIndex(index)
        self._editor.setPlainText(self._snapshot.draft(section_id).text)
        spec = report_section(section_id)
        self._checklist.setText("\n".join(f"• {item}" for item in spec.checklist))
        self._loading = False
        self._update_counts()

    def _capture_visible_text(self) -> BMB831ReportSnapshot:
        return self._snapshot.with_text(
            self._loaded_section_id,
            self._editor.toPlainText(),
        )

    def _schedule_save(self) -> None:
        if self._store is not None:
            self._save_timer.start()

    def _update_counts(self) -> None:
        snapshot = self._capture_visible_text() if hasattr(self, "_editor") else self._snapshot
        current_words = len(self._editor.toPlainText().split())
        self._word_count.setText(
            f"{self._text(BMB831ReportCopyKey.WORD_COUNT)}: {current_words}"
        )
        self._progress.setText(
            f"{self._text(BMB831ReportCopyKey.PROGRESS)}: "
            f"{snapshot.completed_section_count}/{len(BMB831_REPORT_SECTIONS)} — "
            f"{self._text(BMB831ReportCopyKey.WORD_COUNT)}: {snapshot.total_word_count}"
        )

    def _text(self, key: BMB831ReportCopyKey) -> str:
        return bmb831_report_text(self._locale, key)


__all__ = ["BMB831ReportPage"]
