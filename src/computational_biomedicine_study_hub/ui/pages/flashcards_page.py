"""Full-semester flashcard study with persistent spaced repetition."""

from __future__ import annotations

import random
import re
from datetime import UTC, datetime

from PySide6.QtCore import (
    QEasingCurve,
    QEvent,
    QObject,
    QPropertyAnimation,
    QSize,
    Qt,
    QTimer,
    Signal,
    Slot,
)
from PySide6.QtGui import (
    QFont,
    QFontDatabase,
    QKeyEvent,
    QKeySequence,
    QMouseEvent,
    QResizeEvent,
    QShortcut,
    QTextBlockFormat,
    QTextCursor,
    QTextDocument,
)
from PySide6.QtWidgets import (
    QCheckBox,
    QComboBox,
    QFrame,
    QGraphicsOpacityEffect,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QTextBrowser,
    QVBoxLayout,
    QWidget,
)

from ...i18n import DEFAULT_LOCALE, AppLocale
from ...learning.academic_catalog import AcademicCatalog, StudyFlashcard
from ...learning.progress import (
    FlashcardProgress,
    LearningItemKind,
    MasteryState,
    ReviewSchedule,
)
from ...learning.progress_repository import ProgressRepository
from ...learning.spaced_repetition import ReviewRating, reschedule
from ..learning_page_copy import LearningPageCopyKey, learning_text
from ..study_state import StudyLocation


class FlipCardFrame(QFrame):
    activated = Signal()

    def __init__(self) -> None:
        super().__init__()
        self.setFocusPolicy(Qt.FocusPolicy.StrongFocus)
        self.setAccessibleName("Interactive flashcard")

    def mouseReleaseEvent(self, event: QMouseEvent) -> None:  # noqa: N802
        if event.button() == Qt.MouseButton.LeftButton:
            self.activated.emit()
        super().mouseReleaseEvent(event)

    def keyPressEvent(self, event: QKeyEvent) -> None:  # noqa: N802
        if event.key() in {Qt.Key.Key_Space, Qt.Key.Key_Return, Qt.Key.Key_Enter}:
            self.activated.emit()
            event.accept()
            return
        super().keyPressEvent(event)


class AdaptiveCardBrowser(QTextBrowser):
    """Fit learner text to the available card area without clipping it."""

    NORMAL_MIN_PX = 18
    NORMAL_MAX_PX = 42
    CODE_MIN_PX = 18
    CODE_MAX_PX = 24
    HORIZONTAL_PADDING = 48
    MIN_VERTICAL_PADDING = 18

    def __init__(self, object_name: str, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self.setObjectName(object_name)
        self.setOpenExternalLinks(False)
        self.setFrameShape(QFrame.Shape.NoFrame)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self._markdown = ""
        self._is_code = False
        self._font_pixel_size = self.NORMAL_MIN_PX
        self._presentation_revision = 0
        self._requires_vertical_scroll = False
        self._recalculating = False
        self._presentation_style = ""
        self._last_layout_signature: tuple[int, int, str, bool] | None = None

    @property
    def font_pixel_size(self) -> int:
        return self._font_pixel_size

    @property
    def is_code_content(self) -> bool:
        return self._is_code

    @property
    def content_alignment(self) -> Qt.AlignmentFlag:
        return Qt.AlignmentFlag.AlignLeft if self._is_code else Qt.AlignmentFlag.AlignHCenter

    @property
    def presentation_revision(self) -> int:
        return self._presentation_revision

    @property
    def requires_vertical_scroll(self) -> bool:
        return self._requires_vertical_scroll

    def set_card_content(self, markdown: str) -> None:
        self._markdown = markdown
        self._is_code = _contains_code(markdown)
        self._last_layout_signature = None
        self.setHorizontalScrollBarPolicy(
            Qt.ScrollBarPolicy.ScrollBarAsNeeded
            if self._is_code
            else Qt.ScrollBarPolicy.ScrollBarAlwaysOff
        )
        self.recalculate_presentation()

    def sizeHint(self) -> QSize:  # noqa: N802
        return QSize(620, 340)

    def resizeEvent(self, event: QResizeEvent) -> None:  # noqa: N802
        super().resizeEvent(event)
        QTimer.singleShot(0, self.recalculate_presentation)

    @Slot()
    def recalculate_presentation(self) -> None:
        if self._recalculating:
            return
        if not self._markdown:
            self.clear()
            return
        signature = (
            self.viewport().width(),
            self.viewport().height(),
            self._markdown,
            self._is_code,
        )
        if signature == self._last_layout_signature:
            return
        self._recalculating = True
        try:
            useful_width = max(160, self.viewport().width() - 2 * self.HORIZONTAL_PADDING)
            useful_height = max(120, self.viewport().height() - 2 * self.MIN_VERTICAL_PADDING)
            minimum = self.CODE_MIN_PX if self._is_code else self.NORMAL_MIN_PX
            maximum = self.CODE_MAX_PX if self._is_code else self.NORMAL_MAX_PX
            low, high = minimum, maximum
            best = minimum
            while low <= high:
                candidate = (low + high) // 2
                if self._measured_height(candidate, useful_width) <= useful_height:
                    best = candidate
                    low = candidate + 1
                else:
                    high = candidate - 1

            measured = self._measured_height(best, useful_width)
            self._requires_vertical_scroll = measured > useful_height
            self.setVerticalScrollBarPolicy(
                Qt.ScrollBarPolicy.ScrollBarAlwaysOn
                if self._requires_vertical_scroll
                else Qt.ScrollBarPolicy.ScrollBarAlwaysOff
            )
            vertical_padding = (
                self.MIN_VERTICAL_PADDING
                if self._requires_vertical_scroll
                else max(self.MIN_VERTICAL_PADDING, round((useful_height - measured) / 2))
            )
            self._font_pixel_size = best
            font = self._presentation_font()
            font.setPixelSize(best)
            self.document().setDefaultFont(font)
            style = (
                "QTextBrowser {"
                "background: transparent; border: none;"
                f"padding: {vertical_padding}px {self.HORIZONTAL_PADDING}px;"
                "selection-background-color: #2f80ed;"
                "}"
            )
            if style != self._presentation_style:
                self._presentation_style = style
                self.setStyleSheet(style)
            self.setMarkdown(self._markdown)
            cursor = QTextCursor(self.document())
            cursor.select(QTextCursor.SelectionType.Document)
            block_format = QTextBlockFormat()
            block_format.setAlignment(self.content_alignment)
            cursor.mergeBlockFormat(block_format)
            cursor.clearSelection()
            self.verticalScrollBar().setValue(0)
            self.horizontalScrollBar().setValue(0)
            self._presentation_revision += 1
            self._last_layout_signature = (
                self.viewport().width(),
                self.viewport().height(),
                self._markdown,
                self._is_code,
            )
        finally:
            self._recalculating = False

    def _measured_height(self, pixel_size: int, width: int) -> float:
        document = QTextDocument()
        font = self._presentation_font()
        font.setPixelSize(pixel_size)
        document.setDefaultFont(font)
        document.setMarkdown(self._markdown)
        document.setTextWidth(width)
        return document.size().height()

    def _presentation_font(self) -> QFont:
        if self._is_code:
            return QFontDatabase.systemFont(QFontDatabase.SystemFont.FixedFont)
        return QFont("Segoe UI")


def _copy(locale: AppLocale, es: str, en: str, da: str) -> str:
    return {
        AppLocale.SPANISH_SPAIN: es,
        AppLocale.ENGLISH: en,
        AppLocale.DANISH_DENMARK: da,
    }[locale]


class FlashcardsPage(QWidget):
    """Study authored cards using stable IDs and an inspectable SM-2 variant."""

    module_requested = Signal(str, str)

    def __init__(
        self,
        catalog: AcademicCatalog,
        repository: ProgressRepository,
        *,
        locale: AppLocale = DEFAULT_LOCALE,
        rng: random.Random | None = None,
        parent: QWidget | None = None,
    ) -> None:
        super().__init__(parent)
        self.setObjectName("flashcardsPage")
        self._catalog = catalog
        self._repository = repository
        self._locale = locale
        self._rng = rng or random.Random()
        self._cards: list[StudyFlashcard] = []
        self._current_index = 0
        self._animation: QPropertyAnimation | None = None

        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(10)

        filters = QHBoxLayout()
        self.course_selector = QComboBox()
        self.course_selector.setObjectName("flashcardCourseSelector")
        for course_code in catalog.course_codes:
            self.course_selector.addItem(course_code, course_code)
        self.module_selector = QComboBox()
        self.module_selector.setObjectName("flashcardModuleSelector")
        self.type_selector = QComboBox()
        self.type_selector.setObjectName("flashcardTypeSelector")
        self.type_selector.addItem(
            _copy(locale, "Todos los tipos", "All card types", "Alle korttyper"),
            None,
        )
        card_types = sorted({card.card_type for card in catalog.flashcards()})
        for card_type in card_types:
            self.type_selector.addItem(card_type.replace("_", " ").title(), card_type)
        filters.addWidget(self.course_selector)
        filters.addWidget(self.module_selector, 1)
        filters.addWidget(self.type_selector)
        layout.addLayout(filters)

        filter_flags = QHBoxLayout()
        self.due_only = QCheckBox(_copy(locale, "Pendientes", "Due", "Forfaldne"))
        self.new_only = QCheckBox(_copy(locale, "Nuevas", "New", "Nye"))
        self.difficult_only = QCheckBox(_copy(locale, "Difíciles", "Difficult", "Vanskelige"))
        self.favorite_only = QCheckBox(_copy(locale, "Favoritas", "Favorites", "Favoritter"))
        self.mixed_session = QCheckBox(
            _copy(locale, "Sesión mixta", "Mixed session", "Blandet session")
        )
        for checkbox in (
            self.due_only,
            self.new_only,
            self.difficult_only,
            self.favorite_only,
            self.mixed_session,
        ):
            checkbox.setMinimumHeight(32)
            filter_flags.addWidget(checkbox)
            checkbox.toggled.connect(self._refresh_deck)
        filter_flags.addStretch(1)
        layout.addLayout(filter_flags)

        self.stats_label = QLabel()
        self.stats_label.setObjectName("flashcardStats")
        self.progress_label = QLabel()
        self.progress_label.setObjectName("flashcardPosition")
        header = QHBoxLayout()
        header.addWidget(self.stats_label)
        header.addStretch(1)
        header.addWidget(self.progress_label)
        layout.addLayout(header)

        self.card_frame = FlipCardFrame()
        self.card_frame.setObjectName("flashcardStudyCard")
        self.card_frame.setMinimumHeight(300)
        self.card_frame.setCursor(Qt.CursorShape.PointingHandCursor)
        self.card_frame.activated.connect(self.flip)
        card_layout = QVBoxLayout(self.card_frame)
        card_layout.setContentsMargins(20, 16, 20, 20)
        self.side_label = QLabel()
        self.side_label.setObjectName("flashcardSideIndicator")
        self.side_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        card_layout.addWidget(self.side_label)
        self.front_label = AdaptiveCardBrowser("flashcardFront")
        self.front_label.setAccessibleName(
            _copy(locale, "Anverso de tarjeta", "Flashcard front", "Kortets forside")
        )
        self.front_label.viewport().installEventFilter(self)
        self.back_label = AdaptiveCardBrowser("flashcardBack")
        self.back_label.setAccessibleName(
            _copy(locale, "Reverso de tarjeta", "Flashcard back", "Kortets bagside")
        )
        self.back_label.viewport().installEventFilter(self)
        self.back_label.hide()
        card_layout.addWidget(self.front_label, 1)
        card_layout.addWidget(self.back_label, 1)
        layout.addWidget(self.card_frame, 1)

        navigation = QHBoxLayout()
        self.previous_button = QPushButton(_copy(locale, "Anterior", "Previous", "Forrige"))
        self.next_button = QPushButton(_copy(locale, "Siguiente", "Next", "Næste"))
        self.reveal_button = QPushButton(_copy(locale, "Voltear", "Flip", "Vend kort"))
        self.favorite_button = QPushButton()
        self.reset_button = QPushButton(
            _copy(locale, "Reiniciar sesión", "Reset session", "Nulstil session")
        )
        self.back_to_module_button = QPushButton(
            _copy(locale, "Volver al módulo", "Back to module", "Tilbage til modul")
        )
        self.previous_button.setObjectName("previousFlashcardButton")
        self.next_button.setObjectName("nextFlashcardButton")
        self.reveal_button.setObjectName("revealFlashcardButton")
        self.favorite_button.setObjectName("favoriteFlashcardButton")
        self.reset_button.setObjectName("resetFlashcardSessionButton")
        self.back_to_module_button.setObjectName("backToFlashcardModuleButton")
        self.previous_button.clicked.connect(self.previous_card)
        self.next_button.clicked.connect(self.next_card)
        self.reveal_button.clicked.connect(self.flip)
        self.favorite_button.clicked.connect(self.toggle_favorite)
        self.reset_button.clicked.connect(self.reset_session)
        self.back_to_module_button.clicked.connect(self.open_module)
        for button in (
            self.previous_button,
            self.next_button,
            self.reveal_button,
            self.favorite_button,
            self.reset_button,
            self.back_to_module_button,
        ):
            button.setMinimumHeight(38)
            navigation.addWidget(button)
        layout.addLayout(navigation)

        self.rating_panel = QWidget()
        rating_layout = QHBoxLayout(self.rating_panel)
        rating_layout.setContentsMargins(0, 0, 0, 0)
        self.rating_buttons: list[QPushButton] = []
        for shortcut, key, rating in (
            ("1", LearningPageCopyKey.AGAIN, ReviewRating.AGAIN),
            ("2", LearningPageCopyKey.HARD, ReviewRating.HARD),
            ("3", LearningPageCopyKey.GOOD, ReviewRating.GOOD),
            ("4", LearningPageCopyKey.EASY, ReviewRating.EASY),
        ):
            button = QPushButton(f"{shortcut} · {learning_text(locale, key)}")
            button.setObjectName(f"flashcardRating_{rating.name.casefold()}")
            button.setMinimumHeight(52)
            button.setToolTip(shortcut)
            button.setEnabled(False)
            button.clicked.connect(lambda checked=False, value=rating: self.rate(value))
            rating_layout.addWidget(button)
            self.rating_buttons.append(button)
        self.rating_panel.hide()
        layout.addWidget(self.rating_panel)

        self.empty_label = QLabel(learning_text(locale, LearningPageCopyKey.FLASHCARD_EMPTY))
        self.empty_label.setObjectName("flashcardEmptyState")
        self.empty_label.setWordWrap(True)
        self.empty_label.hide()
        layout.addWidget(self.empty_label)

        self.course_selector.currentIndexChanged.connect(self._refresh_modules)
        self.module_selector.currentIndexChanged.connect(self._refresh_deck)
        self.type_selector.currentIndexChanged.connect(self._refresh_deck)
        self._install_shortcuts()
        self._refresh_modules()

    def eventFilter(self, watched: QObject, event: QEvent) -> bool:  # noqa: N802
        if (
            watched in {self.front_label.viewport(), self.back_label.viewport()}
            and event.type() == QEvent.Type.MouseButtonRelease
        ):
            self.flip()
            return True
        return super().eventFilter(watched, event)

    @property
    def current_card(self) -> StudyFlashcard | None:
        if not self._cards:
            return None
        return self._cards[self._current_index]

    @property
    def card_count(self) -> int:
        return len(self._cards)

    def select_context(self, course_code: str, module_id: str) -> bool:
        """Filter the deck by stable course and module identities."""
        course_index = self.course_selector.findData(course_code.upper())
        if course_index < 0:
            return False
        self.course_selector.setCurrentIndex(course_index)
        module_index = self.module_selector.findData(module_id)
        if module_index < 0:
            return False
        self.module_selector.setCurrentIndex(module_index)
        return True

    def _install_shortcuts(self) -> None:
        shortcuts = (
            ("Space", self.flip),
            ("Return", self.flip),
            ("Left", self.previous_card),
            ("Right", self.next_card),
            ("1", lambda: self.rate(ReviewRating.AGAIN)),
            ("2", lambda: self.rate(ReviewRating.HARD)),
            ("3", lambda: self.rate(ReviewRating.GOOD)),
            ("4", lambda: self.rate(ReviewRating.EASY)),
        )
        self._shortcuts: list[QShortcut] = []
        for sequence, callback in shortcuts:
            shortcut = QShortcut(QKeySequence(sequence), self)
            shortcut.activated.connect(callback)
            self._shortcuts.append(shortcut)

    @Slot()
    def _refresh_modules(self) -> None:
        course_code = self.course_selector.currentData()
        self.module_selector.blockSignals(True)
        self.module_selector.clear()
        self.module_selector.addItem(
            learning_text(self._locale, LearningPageCopyKey.ALL_MODULES), None
        )
        if isinstance(course_code, str):
            for record in self._catalog.modules(course_code):
                self.module_selector.addItem(record.title, record.module_id)
        self.module_selector.blockSignals(False)
        self._refresh_deck()

    @Slot()
    def _refresh_deck(self) -> None:
        course_value = self.course_selector.currentData()
        module_value = self.module_selector.currentData()
        type_value = self.type_selector.currentData()
        course_code = course_value if isinstance(course_value, str) else None
        module_id = module_value if isinstance(module_value, str) else None
        cards = list(self._catalog.flashcards(course_code=course_code, module_id=module_id))
        now = datetime.now(UTC)
        progress = {
            item.card_id: item
            for item in self._repository.list_flashcard_progress(
                course_code=course_code, module_id=module_id
            )
        }
        if isinstance(type_value, str):
            cards = [card for card in cards if card.card_type == type_value]
        if self.due_only.isChecked():
            cards = [
                card
                for card in cards
                if (item := progress.get(card.card_id)) is not None and item.due_at <= now
            ]
        if self.new_only.isChecked():
            cards = [
                card
                for card in cards
                if (item := progress.get(card.card_id)) is None or item.total_reviews == 0
            ]
        if self.difficult_only.isChecked():
            cards = [
                card
                for card in cards
                if card.difficulty in {"advanced", "difficult", "hard"}
                or (
                    (item := progress.get(card.card_id)) is not None
                    and (
                        item.last_rating in {"AGAIN", "HARD"}
                        or item.mastery_state is MasteryState.LEARNING
                    )
                )
            ]
        if self.favorite_only.isChecked():
            cards = [
                card
                for card in cards
                if (item := progress.get(card.card_id)) is not None and item.bookmarked
            ]
        if self.mixed_session.isChecked():
            self._rng.shuffle(cards)
        self._cards = cards
        self._current_index = 0
        self._show_current()
        self._update_stats(course_code=course_code, module_id=module_id)

    @Slot()
    def reset_session(self) -> None:
        self._current_index = 0
        if self.mixed_session.isChecked():
            self._rng.shuffle(self._cards)
        self._show_current()

    @Slot()
    def previous_card(self) -> None:
        if not self._cards:
            return
        self._current_index = (self._current_index - 1) % len(self._cards)
        self._show_current()

    @Slot()
    def next_card(self) -> None:
        if not self._cards:
            return
        self._current_index = (self._current_index + 1) % len(self._cards)
        self._show_current()

    @Slot()
    def reveal(self) -> None:
        if self.back_label.isHidden():
            self.flip()

    @Slot()
    def flip(self) -> None:
        if self.current_card is None:
            return
        show_back = self.back_label.isHidden()
        self.front_label.setVisible(not show_back)
        self.back_label.setVisible(show_back)
        self.rating_panel.setVisible(show_back)
        for button in self.rating_buttons:
            button.setEnabled(show_back)
        self.side_label.setText(
            _copy(self._locale, "Reverso", "Back", "Bagside")
            if show_back
            else _copy(self._locale, "Anverso", "Front", "Forside")
        )
        self.card_frame.setProperty("cardSide", "back" if show_back else "front")
        self.card_frame.style().unpolish(self.card_frame)
        self.card_frame.style().polish(self.card_frame)
        visible = self.back_label if show_back else self.front_label
        visible.recalculate_presentation()
        self._animate_card()

    def _animate_card(self) -> None:
        effect = QGraphicsOpacityEffect(self.card_frame)
        self.card_frame.setGraphicsEffect(effect)
        animation = QPropertyAnimation(effect, b"opacity", self)
        animation.setDuration(140)
        animation.setStartValue(0.35)
        animation.setEndValue(1.0)
        animation.setEasingCurve(QEasingCurve.Type.OutCubic)
        self._animation = animation
        animation.start()

    def rate(self, rating: ReviewRating) -> None:
        card = self.current_card
        if card is None or self.back_label.isHidden():
            return
        now = datetime.now(UTC)
        previous = self._repository.get_flashcard_progress(
            card.course_code, card.module_id, card.card_id
        )
        schedule = ReviewSchedule(
            course_code=card.course_code,
            module_id=card.module_id,
            item_id=card.card_id,
            item_kind=LearningItemKind.FLASHCARD,
            mastery_state=previous.mastery_state if previous else MasteryState.NEW,
            repetitions=previous.repetitions if previous else 0,
            interval_days=previous.interval_days if previous else 0,
            easiness=previous.easiness if previous else 2.5,
            due_at=previous.due_at if previous else now,
            last_reviewed_at=previous.last_reviewed_at if previous else None,
        )
        updated = reschedule(schedule, rating, reviewed_at=now)
        self._repository.save_review_schedule(updated)
        self._repository.save_flashcard_progress(
            FlashcardProgress(
                course_code=updated.course_code,
                module_id=updated.module_id,
                card_id=updated.item_id,
                mastery_state=updated.mastery_state,
                repetitions=updated.repetitions,
                interval_days=updated.interval_days,
                easiness=updated.easiness,
                due_at=updated.due_at,
                last_reviewed_at=updated.last_reviewed_at,
                first_seen_at=previous.first_seen_at if previous else now,
                lapse_count=(previous.lapse_count if previous else 0)
                + int(rating is ReviewRating.AGAIN),
                last_rating=rating.name,
                total_reviews=(previous.total_reviews if previous else 0) + 1,
                bookmarked=previous.bookmarked if previous else False,
            )
        )
        self.next_card()
        self._update_stats(
            course_code=card.course_code,
            module_id=(
                self.module_selector.currentData()
                if isinstance(self.module_selector.currentData(), str)
                else None
            ),
        )

    @Slot()
    def toggle_favorite(self) -> None:
        card = self.current_card
        if card is None:
            return
        now = datetime.now(UTC)
        previous = self._repository.get_flashcard_progress(
            card.course_code, card.module_id, card.card_id
        )
        self._repository.save_flashcard_progress(
            FlashcardProgress(
                course_code=card.course_code,
                module_id=card.module_id,
                card_id=card.card_id,
                mastery_state=previous.mastery_state if previous else MasteryState.NEW,
                repetitions=previous.repetitions if previous else 0,
                interval_days=previous.interval_days if previous else 0,
                easiness=previous.easiness if previous else 2.5,
                due_at=previous.due_at if previous else now,
                last_reviewed_at=previous.last_reviewed_at if previous else None,
                first_seen_at=previous.first_seen_at if previous else now,
                lapse_count=previous.lapse_count if previous else 0,
                last_rating=previous.last_rating if previous else "",
                total_reviews=previous.total_reviews if previous else 0,
                bookmarked=not previous.bookmarked if previous else True,
            )
        )
        self._update_favorite_button()
        if self.favorite_only.isChecked():
            self._refresh_deck()

    @Slot()
    def open_module(self) -> None:
        card = self.current_card
        if card is not None:
            self.module_requested.emit(card.course_code, card.module_id)

    def capture_state(self) -> StudyLocation:
        card = self.current_card
        return StudyLocation(
            route="flashcards",
            course_code=card.course_code if card else "",
            module_id=card.module_id if card else "",
            card_id=card.card_id if card else "",
            logical_position=self._current_index,
            filters={
                "type": str(self.type_selector.currentData() or ""),
                "due": str(self.due_only.isChecked()),
                "new": str(self.new_only.isChecked()),
                "difficult": str(self.difficult_only.isChecked()),
                "favorite": str(self.favorite_only.isChecked()),
                "mixed": str(self.mixed_session.isChecked()),
            },
        )

    def restore_state(self, state: StudyLocation) -> None:
        course_index = self.course_selector.findData(state.course_code)
        if course_index >= 0:
            self.course_selector.setCurrentIndex(course_index)
        module_index = self.module_selector.findData(state.module_id)
        if module_index >= 0:
            self.module_selector.setCurrentIndex(module_index)
        type_index = self.type_selector.findData(state.filters.get("type") or None)
        if type_index >= 0:
            self.type_selector.setCurrentIndex(type_index)
        for key, checkbox in (
            ("due", self.due_only),
            ("new", self.new_only),
            ("difficult", self.difficult_only),
            ("favorite", self.favorite_only),
            ("mixed", self.mixed_session),
        ):
            checkbox.setChecked(state.filters.get(key) == "True")
        card_index = next(
            (index for index, card in enumerate(self._cards) if card.card_id == state.card_id),
            -1,
        )
        if card_index >= 0:
            self._current_index = card_index
            self._show_current()

    def _show_current(self) -> None:
        card = self.current_card
        is_empty = card is None
        self.empty_label.setVisible(is_empty)
        self.card_frame.setVisible(not is_empty)
        self.rating_panel.hide()
        for button in self.rating_buttons:
            button.setEnabled(False)
        self.front_label.setVisible(not is_empty)
        self.back_label.hide()
        for button in (
            self.previous_button,
            self.next_button,
            self.reveal_button,
            self.favorite_button,
            self.reset_button,
            self.back_to_module_button,
        ):
            button.setEnabled(not is_empty)
        if card is None:
            self.front_label.clear()
            self.back_label.clear()
            self.side_label.clear()
            self.progress_label.setText("0 / 0")
            return
        self.front_label.set_card_content(card.front)
        self.back_label.set_card_content(card.back)
        self.side_label.setText(_copy(self._locale, "Anverso", "Front", "Forside"))
        self.card_frame.setProperty("cardSide", "front")
        self.card_frame.style().unpolish(self.card_frame)
        self.card_frame.style().polish(self.card_frame)
        self.progress_label.setText(f"{self._current_index + 1} / {len(self._cards)}")
        self._update_favorite_button()
        self.card_frame.setFocus()

    def _update_favorite_button(self) -> None:
        card = self.current_card
        progress = (
            self._repository.get_flashcard_progress(card.course_code, card.module_id, card.card_id)
            if card is not None
            else None
        )
        favorite = progress.bookmarked if progress else False
        self.favorite_button.setText(
            ("★ " if favorite else "☆ ") + _copy(self._locale, "Favorita", "Favorite", "Favorit")
        )
        self.favorite_button.setAccessibleName(self.favorite_button.text())

    def _update_stats(self, *, course_code: str | None, module_id: str | None) -> None:
        now = datetime.now(UTC)
        progress = self._repository.list_flashcard_progress(
            course_code=course_code, module_id=module_id
        )
        self.stats_label.setText(
            learning_text(
                self._locale,
                LearningPageCopyKey.FLASHCARD_STATS,
                reviewed=sum(item.total_reviews > 0 for item in progress),
                mastered=sum(item.mastery_state is MasteryState.MASTERED for item in progress),
                due=sum(item.due_at <= now and item.total_reviews > 0 for item in progress),
            )
        )


_CODE_PATTERN = re.compile(
    r"(^|\n)\s*```|(^|\n)(?: {4}|\t)\S|"
    r"\b(?:def|class|import|from|for|while|return|function)\b|"
    r"(?:<-|::|library\s*\()",
    flags=re.IGNORECASE,
)


def _contains_code(markdown: str) -> bool:
    return bool(_CODE_PATTERN.search(markdown))


__all__ = ["AdaptiveCardBrowser", "FlashcardsPage", "FlipCardFrame"]
