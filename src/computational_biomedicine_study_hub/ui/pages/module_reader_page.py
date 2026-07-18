"""PySide6 renderer for one localized authored learning module."""

from __future__ import annotations

from collections.abc import Callable, Iterable

from PySide6.QtCore import QSignalBlocker, Qt, Slot
from PySide6.QtWidgets import (
    QFrame,
    QHBoxLayout,
    QLabel,
    QPlainTextEdit,
    QScrollArea,
    QSizePolicy,
    QTabWidget,
    QVBoxLayout,
    QWidget,
)

from ...content.models import AssessmentItem, ConceptBlock, LearningModule, WorkedExample
from ...i18n import MessageKey, Translator, UiCopyKey, ui_text
from ..widgets import GuidedPracticeWidget, ObjectiveAssessmentWidget

_ACTIVITY_KEYS = {
    "worked_example": MessageKey.ACTIVITY_WORKED_EXAMPLE,
    "flashcard": MessageKey.ACTIVITY_FLASHCARD,
    "multiple_choice": MessageKey.ACTIVITY_MULTIPLE_CHOICE,
    "multiple_select": MessageKey.ACTIVITY_MULTIPLE_SELECT,
    "true_false": MessageKey.ACTIVITY_TRUE_FALSE,
    "fill_in_the_blank": MessageKey.ACTIVITY_FILL_BLANK,
    "matching": MessageKey.ACTIVITY_MATCHING,
    "ordering": MessageKey.ACTIVITY_ORDERING,
    "code_completion": MessageKey.ACTIVITY_CODE_COMPLETION,
    "code_tracing": MessageKey.ACTIVITY_CODE_TRACING,
    "debugging": MessageKey.ACTIVITY_DEBUGGING,
    "short_answer": MessageKey.ACTIVITY_SHORT_ANSWER,
    "oral_explanation": MessageKey.ACTIVITY_ORAL_EXPLANATION,
    "data_interpretation": MessageKey.ACTIVITY_DATA_INTERPRETATION,
    "pipeline_design": MessageKey.ACTIVITY_PIPELINE_DESIGN,
}


class ModuleReaderPage(QWidget):
    """Render one localized module while constructing heavy sections on first use."""

    def __init__(
        self,
        module: LearningModule,
        parent: QWidget | None = None,
        *,
        objective_question_bank: tuple[AssessmentItem, ...] = (),
        show_context_bar: bool = True,
        translator: Translator | None = None,
    ) -> None:
        super().__init__(parent)
        self.setObjectName("moduleReaderPage")
        self._module = module
        self._objective_question_bank = objective_question_bank
        self._translator = translator or Translator()
        self._section_cache: dict[int, QWidget] = {}
        self._tab_builders: tuple[tuple[MessageKey, Callable[[], QWidget]], ...] = (
            (MessageKey.MODULE_TAB_OVERVIEW, self._build_overview_tab),
            (MessageKey.MODULE_TAB_CONCEPTS, self._build_concepts_tab),
            (MessageKey.MODULE_TAB_EXAMPLES, self._build_examples_tab),
            (MessageKey.MODULE_TAB_PRACTICE, self._build_practice_tab),
            (MessageKey.MODULE_TAB_ASSESSMENT, self._build_assessment_tab),
        )

        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(8)
        if show_context_bar:
            layout.addWidget(self._build_context_bar())

        self._tabs = QTabWidget()
        self._tabs.setObjectName("moduleTabs")
        self._tabs.setDocumentMode(True)
        self._tabs.setUsesScrollButtons(True)
        for index, (key, _) in enumerate(self._tab_builders):
            label = self._translator.text(key)
            placeholder = QWidget()
            placeholder.setObjectName("moduleTabPlaceholder")
            placeholder.setProperty("sectionIndex", index)
            placeholder.setProperty("sectionLabel", label)
            self._tabs.addTab(placeholder, label)
        self._tabs.currentChanged.connect(self._ensure_section_loaded)
        self._ensure_section_loaded(0)
        self._tabs.setCurrentIndex(0)
        layout.addWidget(self._tabs, 1)

    @property
    def module(self) -> LearningModule:
        """Return the module rendered by this page."""
        return self._module

    @property
    def current_section(self) -> str:
        """Return the visible localized section label."""
        return self._tabs.tabText(self._tabs.currentIndex())

    @property
    def current_section_index(self) -> int:
        """Return the stable zero-based section index."""
        return self._tabs.currentIndex()

    @property
    def constructed_section_count(self) -> int:
        """Return the number of fully constructed reader sections."""
        return len(self._section_cache)

    def has_constructed_section(self, label: str) -> bool:
        """Return whether the named localized section has already been constructed."""
        for index, (key, _) in enumerate(self._tab_builders):
            if self._translator.text(key) == label:
                return index in self._section_cache
        return False

    def select_section(self, label: str) -> bool:
        """Select a section by its visible label and construct it if required."""
        for index in range(self._tabs.count()):
            if self._tabs.tabText(index) == label:
                return self.select_section_index(index)
        return False

    def select_section_index(self, index: int) -> bool:
        """Select a section by stable index and construct it if required."""
        if not 0 <= index < self._tabs.count():
            return False
        if index == self._tabs.currentIndex():
            self._ensure_section_loaded(index)
        else:
            self._tabs.setCurrentIndex(index)
        return True

    @Slot(int)
    def _ensure_section_loaded(self, index: int) -> None:
        if not 0 <= index < len(self._tab_builders) or index in self._section_cache:
            return

        key, builder = self._tab_builders[index]
        label = self._translator.text(key)
        page = builder()
        self._section_cache[index] = page
        placeholder = self._tabs.widget(index)
        current_index = self._tabs.currentIndex()

        blocker = QSignalBlocker(self._tabs)
        self._tabs.removeTab(index)
        self._tabs.insertTab(index, page, label)
        self._tabs.setCurrentIndex(current_index if current_index >= 0 else index)
        del blocker

        if placeholder is not None:
            placeholder.deleteLater()

    def _build_context_bar(self) -> QFrame:
        bar = QFrame()
        bar.setObjectName("moduleContextBar")
        bar_layout = QHBoxLayout(bar)
        bar_layout.setContentsMargins(14, 8, 14, 8)
        bar_layout.setSpacing(12)

        module_token = self._module.module_id.rsplit(".", maxsplit=1)[-1]
        number_text = module_token.removeprefix("m").lstrip("0") or "0"
        module_label = self._translator.text(MessageKey.MODULE_LABEL, number=number_text)
        kicker = self._label(
            f"{self._module.course_code} · {module_label}",
            "moduleContextKicker",
        )
        kicker.setWordWrap(False)
        title = self._label(self._module.title, "moduleContextTitle")
        title.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Preferred)

        bar_layout.addWidget(kicker)
        bar_layout.addWidget(title, 1)
        return bar

    def _build_overview_tab(self) -> QScrollArea:
        body = self._scroll_body()
        layout = body.layout()
        assert isinstance(layout, QVBoxLayout)

        layout.addWidget(
            self._text_card(
                self._translator.text(MessageKey.MODULE_PURPOSE),
                self._module.summary,
                object_name="moduleOverviewCard",
            )
        )

        objectives = "\n".join(
            f"{index}. {objective.statement}"
            for index, objective in enumerate(self._module.objectives, start=1)
        )
        layout.addWidget(
            self._text_card(
                self._translator.text(MessageKey.MODULE_OBJECTIVES),
                objectives,
                object_name="moduleObjectivesCard",
            )
        )

        layout.addWidget(
            self._text_card(
                self._translator.text(MessageKey.MODULE_STUDY_SEQUENCE),
                self._translator.text(MessageKey.MODULE_STUDY_SEQUENCE_TEXT),
                object_name="moduleSequenceCard",
            )
        )
        layout.addStretch(1)
        return self._scroll_area(body, "moduleOverviewScroll")

    def _build_concepts_tab(self) -> QScrollArea:
        body = self._scroll_body()
        layout = body.layout()
        assert isinstance(layout, QVBoxLayout)

        for concept in self._module.concepts:
            layout.addWidget(self._concept_card(concept))
        layout.addStretch(1)
        return self._scroll_area(body, "moduleConceptsScroll")

    def _build_examples_tab(self) -> QScrollArea:
        body = self._scroll_body()
        layout = body.layout()
        assert isinstance(layout, QVBoxLayout)

        for example in self._module.worked_examples:
            layout.addWidget(self._example_card(example))
        layout.addStretch(1)
        return self._scroll_area(body, "moduleExamplesScroll")

    def _build_practice_tab(self) -> QScrollArea:
        body = self._scroll_body()
        layout = body.layout()
        assert isinstance(layout, QVBoxLayout)

        notice = self._label(
            self._translator.text(MessageKey.MODULE_PRACTICE_NOTICE),
            "moduleSectionNotice",
        )
        layout.addWidget(notice)
        layout.addWidget(
            GuidedPracticeWidget(
                self._module.practice_exercises,
                locale=self._translator.locale,
            )
        )
        layout.addStretch(1)
        return self._scroll_area(body, "modulePracticeScroll")

    def _build_assessment_tab(self) -> QScrollArea:
        body = self._scroll_body()
        layout = body.layout()
        assert isinstance(layout, QVBoxLayout)

        if self._objective_question_bank:
            objective_heading = self._subheading(
                ui_text(self._translator.locale, UiCopyKey.MODULE_OBJECTIVE_SECTION)
            )
            objective_heading.setObjectName("objectiveAssessmentSectionTitle")
            layout.addWidget(objective_heading)
            notice = self._label(
                self._translator.text(MessageKey.MODULE_ASSESSMENT_NOTICE),
                "moduleSectionNotice",
            )
            layout.addWidget(notice)
            layout.addWidget(
                ObjectiveAssessmentWidget(
                    self._objective_question_bank,
                    locale=self._translator.locale,
                )
            )

        complete_heading = self._subheading(
            ui_text(self._translator.locale, UiCopyKey.MODULE_COMPLETE_ASSESSMENT)
        )
        complete_heading.setObjectName("authoredAssessmentSectionTitle")
        layout.addWidget(complete_heading)
        complete_notice = self._label(
            ui_text(
                self._translator.locale,
                UiCopyKey.MODULE_COMPLETE_ASSESSMENT_NOTICE,
            ),
            "moduleSectionNotice",
        )
        layout.addWidget(complete_notice)

        for number, item in enumerate(self._module.assessment_items, start=1):
            layout.addWidget(self._assessment_card(number, item))

        layout.addStretch(1)
        return self._scroll_area(body, "moduleAssessmentScroll")

    def _concept_card(self, concept: ConceptBlock) -> QFrame:
        card, layout = self._card("conceptCard", concept.title)
        layout.addWidget(self._label(concept.body, "contentBody"))
        layout.addWidget(self._subheading(self._translator.text(MessageKey.MODULE_ESSENTIAL_POINTS)))
        layout.addWidget(self._label(self._bullets(concept.key_points), "contentBulletList"))
        return card

    def _example_card(self, example: WorkedExample) -> QFrame:
        card, layout = self._card("exampleCard", example.title)
        layout.addWidget(self._subheading(self._translator.text(MessageKey.MODULE_PROBLEM)))
        layout.addWidget(self._label(example.problem, "contentBody"))
        layout.addWidget(self._subheading(self._translator.text(MessageKey.MODULE_REASONING)))
        layout.addWidget(self._label(self._numbered(example.reasoning), "contentBulletList"))
        layout.addWidget(self._subheading(self._translator.text(MessageKey.MODULE_CODE)))
        layout.addWidget(self._code_block(example.code, "exampleCode"))
        layout.addWidget(self._subheading(self._translator.text(MessageKey.MODULE_EXPECTED_OUTPUT)))
        layout.addWidget(self._code_block(example.expected_output, "exampleOutput"))
        layout.addWidget(self._subheading(self._translator.text(MessageKey.MODULE_EXPLANATION)))
        layout.addWidget(self._label(example.explanation, "contentBody"))
        return card

    def _assessment_card(self, number: int, item: AssessmentItem) -> QFrame:
        activity = self._activity_label(item.activity_type.value)
        title = self._translator.text(
            MessageKey.MODULE_QUESTION,
            number=number,
            activity=activity,
        )
        card, layout = self._card("assessmentCard", title)
        layout.addWidget(self._label(item.prompt, "assessmentPrompt"))

        if item.options:
            layout.addWidget(self._subheading(self._translator.text(MessageKey.MODULE_OPTIONS)))
            layout.addWidget(self._label(self._bullets(item.options), "assessmentOptions"))

        if item.rubric:
            layout.addWidget(
                self._subheading(self._translator.text(MessageKey.MODULE_GRADING_CRITERIA))
            )
            layout.addWidget(self._label(self._bullets(item.rubric), "assessmentRubric"))
        return card

    def _activity_label(self, value: str) -> str:
        key = _ACTIVITY_KEYS.get(value)
        if key is not None:
            return self._translator.text(key)
        return value.replace("_", " ").capitalize()

    def _text_card(self, title: str, text: str, *, object_name: str) -> QFrame:
        card, layout = self._card(object_name, title)
        layout.addWidget(self._label(text, "contentBody"))
        return card

    @staticmethod
    def _scroll_body() -> QWidget:
        body = QWidget()
        body.setObjectName("moduleScrollBody")
        layout = QVBoxLayout(body)
        layout.setContentsMargins(4, 8, 12, 12)
        layout.setSpacing(14)
        return body

    @staticmethod
    def _scroll_area(body: QWidget, object_name: str) -> QScrollArea:
        area = QScrollArea()
        area.setObjectName(object_name)
        area.setWidgetResizable(True)
        area.setFrameShape(QFrame.Shape.NoFrame)
        area.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        area.setWidget(body)
        return area

    @staticmethod
    def _card(object_name: str, title: str) -> tuple[QFrame, QVBoxLayout]:
        card = QFrame()
        card.setObjectName(object_name)
        card.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Maximum)
        layout = QVBoxLayout(card)
        layout.setContentsMargins(20, 18, 20, 18)
        layout.setSpacing(10)

        heading = QLabel(title)
        heading.setObjectName("contentCardTitle")
        heading.setWordWrap(True)
        layout.addWidget(heading)
        return card, layout

    @staticmethod
    def _label(text: str, object_name: str) -> QLabel:
        label = QLabel(text)
        label.setObjectName(object_name)
        label.setWordWrap(True)
        label.setTextInteractionFlags(Qt.TextInteractionFlag.TextSelectableByMouse)
        return label

    @staticmethod
    def _subheading(text: str) -> QLabel:
        label = QLabel(text)
        label.setObjectName("contentSubheading")
        return label

    @staticmethod
    def _code_block(text: str, object_name: str) -> QPlainTextEdit:
        editor = QPlainTextEdit(text)
        editor.setObjectName(object_name)
        editor.setReadOnly(True)
        editor.setLineWrapMode(QPlainTextEdit.LineWrapMode.NoWrap)
        editor.setTabChangesFocus(True)
        line_count = max(1, text.count("\n") + 1)
        editor.setFixedHeight(min(220, 32 + line_count * 21))
        return editor

    @staticmethod
    def _bullets(values: Iterable[str]) -> str:
        return "\n".join(f"• {value}" for value in values)

    @staticmethod
    def _numbered(values: Iterable[str]) -> str:
        return "\n".join(f"{index}. {value}" for index, value in enumerate(values, start=1))
