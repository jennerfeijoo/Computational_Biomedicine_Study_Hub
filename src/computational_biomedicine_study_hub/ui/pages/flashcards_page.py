"""Model-backed flashcards with persistent spaced repetition."""

from __future__ import annotations

import random
from datetime import UTC, datetime

from PySide6.QtCore import Slot
from PySide6.QtWidgets import (
    QComboBox,
    QFrame,
    QHBoxLayout,
    QLabel,
    QPushButton,
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


class FlashcardsPage(QWidget):
    """Study compact cards generated from authored concepts and misconceptions."""

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

        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        filters = QHBoxLayout()
        self.course_selector = QComboBox()
        self.course_selector.setObjectName("flashcardCourseSelector")
        self.course_selector.setAccessibleName(learning_text(locale, LearningPageCopyKey.COURSE))
        for course_code in catalog.course_codes:
            self.course_selector.addItem(course_code, course_code)
        self.module_selector = QComboBox()
        self.module_selector.setObjectName("flashcardModuleSelector")
        self.module_selector.setAccessibleName(learning_text(locale, LearningPageCopyKey.MODULE))
        self.shuffle_button = QPushButton(learning_text(locale, LearningPageCopyKey.SHUFFLE))
        self.shuffle_button.setObjectName("shuffleFlashcardsButton")
        self.shuffle_button.clicked.connect(self.shuffle)
        filters.addWidget(self.course_selector)
        filters.addWidget(self.module_selector, 1)
        filters.addWidget(self.shuffle_button)
        layout.addLayout(filters)

        self.stats_label = QLabel()
        self.stats_label.setObjectName("flashcardStats")
        layout.addWidget(self.stats_label)

        card = QFrame()
        card.setObjectName("flashcardStudyCard")
        card_layout = QVBoxLayout(card)
        self.front_label = QLabel()
        self.front_label.setObjectName("flashcardFront")
        self.front_label.setWordWrap(True)
        self.front_label.setAccessibleName("Flashcard front")
        card_layout.addWidget(self.front_label)
        self.reveal_button = QPushButton(learning_text(locale, LearningPageCopyKey.REVEAL))
        self.reveal_button.setObjectName("revealFlashcardButton")
        self.reveal_button.clicked.connect(self.reveal)
        card_layout.addWidget(self.reveal_button)
        self.back_label = QLabel()
        self.back_label.setObjectName("flashcardBack")
        self.back_label.setWordWrap(True)
        self.back_label.setAccessibleName("Flashcard back")
        self.back_label.hide()
        card_layout.addWidget(self.back_label)
        self.rating_panel = QWidget()
        rating_layout = QHBoxLayout(self.rating_panel)
        rating_layout.setContentsMargins(0, 0, 0, 0)
        for key, rating in (
            (LearningPageCopyKey.AGAIN, ReviewRating.AGAIN),
            (LearningPageCopyKey.HARD, ReviewRating.HARD),
            (LearningPageCopyKey.GOOD, ReviewRating.GOOD),
            (LearningPageCopyKey.EASY, ReviewRating.EASY),
        ):
            button = QPushButton(learning_text(locale, key))
            button.setObjectName(f"flashcardRating_{rating.name.casefold()}")
            button.clicked.connect(lambda checked=False, value=rating: self.rate(value))
            rating_layout.addWidget(button)
        self.rating_panel.hide()
        card_layout.addWidget(self.rating_panel)
        layout.addWidget(card, 1)

        self.empty_label = QLabel(learning_text(locale, LearningPageCopyKey.FLASHCARD_EMPTY))
        self.empty_label.setObjectName("flashcardEmptyState")
        self.empty_label.setWordWrap(True)
        self.empty_label.hide()
        layout.addWidget(self.empty_label)

        self.course_selector.currentIndexChanged.connect(self._refresh_modules)
        self.module_selector.currentIndexChanged.connect(self._refresh_deck)
        self._refresh_modules()

    @property
    def current_card(self) -> StudyFlashcard | None:
        if not self._cards:
            return None
        return self._cards[self._current_index]

    @property
    def card_count(self) -> int:
        return len(self._cards)

    @Slot()
    def _refresh_modules(self) -> None:
        course_code = self.course_selector.currentData()
        self.module_selector.blockSignals(True)
        self.module_selector.clear()
        self.module_selector.addItem(
            learning_text(self._locale, LearningPageCopyKey.ALL_MODULES),
            None,
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
        course_code = course_value if isinstance(course_value, str) else None
        module_id = module_value if isinstance(module_value, str) else None
        self._cards = list(
            self._catalog.flashcards(
                course_code=course_code,
                module_id=module_id,
            )
        )
        self._current_index = 0
        self._show_current()
        self._update_stats(course_code=course_code, module_id=module_id)

    @Slot()
    def shuffle(self) -> None:
        self._rng.shuffle(self._cards)
        self._current_index = 0
        self._show_current()

    @Slot()
    def reveal(self) -> None:
        if self.current_card is None:
            return
        self.back_label.show()
        self.rating_panel.show()
        self.reveal_button.setEnabled(False)

    def rate(self, rating: ReviewRating) -> None:
        card = self.current_card
        if card is None or self.back_label.isHidden():
            return
        now = datetime.now(UTC)
        previous = self._repository.get_flashcard_progress(
            card.course_code,
            card.module_id,
            card.card_id,
        )
        schedule = ReviewSchedule(
            course_code=card.course_code,
            module_id=card.module_id,
            item_id=card.card_id,
            item_kind=LearningItemKind.FLASHCARD,
            mastery_state=(previous.mastery_state if previous is not None else MasteryState.NEW),
            repetitions=previous.repetitions if previous is not None else 0,
            interval_days=previous.interval_days if previous is not None else 0,
            easiness=previous.easiness if previous is not None else 2.5,
            due_at=previous.due_at if previous is not None else now,
            last_reviewed_at=(previous.last_reviewed_at if previous is not None else None),
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
            )
        )
        self._current_index = (self._current_index + 1) % len(self._cards)
        self._show_current()
        course_value = self.course_selector.currentData()
        module_value = self.module_selector.currentData()
        self._update_stats(
            course_code=course_value if isinstance(course_value, str) else None,
            module_id=module_value if isinstance(module_value, str) else None,
        )

    def _show_current(self) -> None:
        card = self.current_card
        is_empty = card is None
        self.empty_label.setVisible(is_empty)
        self.front_label.setVisible(not is_empty)
        self.reveal_button.setVisible(not is_empty)
        self.back_label.hide()
        self.rating_panel.hide()
        self.reveal_button.setEnabled(not is_empty)
        if card is None:
            self.front_label.clear()
            self.back_label.clear()
            return
        self.front_label.setText(card.front)
        self.back_label.setText(card.back)

    def _update_stats(
        self,
        *,
        course_code: str | None,
        module_id: str | None,
    ) -> None:
        now = datetime.now(UTC)
        progress = self._repository.list_flashcard_progress(
            course_code=course_code,
            module_id=module_id,
        )
        self.stats_label.setText(
            learning_text(
                self._locale,
                LearningPageCopyKey.FLASHCARD_STATS,
                reviewed=len(progress),
                mastered=sum(item.mastery_state is MasteryState.MASTERED for item in progress),
                due=sum(item.due_at <= now for item in progress),
            )
        )


__all__ = ["FlashcardsPage"]
