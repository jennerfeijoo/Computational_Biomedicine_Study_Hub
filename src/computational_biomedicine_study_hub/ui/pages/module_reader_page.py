"""PySide6 renderer for one authored learning module."""

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
from ..widgets import GuidedPracticeWidget, ObjectiveAssessmentWidget

_ACTIVITY_LABELS = {
    "worked_example": "Ejemplo resuelto",
    "flashcard": "Tarjeta de memoria",
    "multiple_choice": "Opción múltiple",
    "multiple_select": "Selección múltiple",
    "true_false": "Verdadero o falso",
    "fill_in_the_blank": "Rellenar espacios",
    "matching": "Relacionar elementos",
    "ordering": "Ordenar pasos",
    "code_completion": "Completar código",
    "code_tracing": "Trazado de código",
    "debugging": "Depuración",
    "short_answer": "Respuesta breve",
    "oral_explanation": "Explicación oral",
    "data_interpretation": "Interpretación de datos",
    "pipeline_design": "Diseño de pipeline",
}


class ModuleReaderPage(QWidget):
    """Render one module while constructing heavy sections on first use."""

    def __init__(
        self,
        module: LearningModule,
        parent: QWidget | None = None,
        *,
        objective_question_bank: tuple[AssessmentItem, ...] = (),
        show_context_bar: bool = True,
    ) -> None:
        super().__init__(parent)
        self.setObjectName("moduleReaderPage")
        self._module = module
        self._objective_question_bank = objective_question_bank
        self._section_cache: dict[int, QWidget] = {}
        self._tab_builders: tuple[tuple[str, Callable[[], QWidget]], ...] = (
            ("Resumen", self._build_overview_tab),
            ("Conceptos", self._build_concepts_tab),
            ("Ejemplos", self._build_examples_tab),
            ("Práctica", self._build_practice_tab),
            ("Evaluación", self._build_assessment_tab),
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
        for index, (label, _) in enumerate(self._tab_builders):
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
        """Return the visible section label."""
        return self._tabs.tabText(self._tabs.currentIndex())

    @property
    def constructed_section_count(self) -> int:
        """Return the number of fully constructed reader sections."""
        return len(self._section_cache)

    def has_constructed_section(self, label: str) -> bool:
        """Return whether the named section has already been constructed."""
        for index, (section_label, _) in enumerate(self._tab_builders):
            if section_label == label:
                return index in self._section_cache
        return False

    def select_section(self, label: str) -> bool:
        """Select a section by its visible label and construct it if required."""
        for index in range(self._tabs.count()):
            if self._tabs.tabText(index) == label:
                if index == self._tabs.currentIndex():
                    self._ensure_section_loaded(index)
                else:
                    self._tabs.setCurrentIndex(index)
                return True
        return False

    @Slot(int)
    def _ensure_section_loaded(self, index: int) -> None:
        if not 0 <= index < len(self._tab_builders) or index in self._section_cache:
            return

        label, builder = self._tab_builders[index]
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
        kicker = self._label(
            f"{self._module.course_code} · Módulo {number_text}",
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
                "Propósito del módulo",
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
                "Objetivos de aprendizaje",
                objectives,
                object_name="moduleObjectivesCard",
            )
        )

        sequence = (
            "Teoría conectada → ejemplos resueltos → práctica formativa → "
            "evaluación del aprendizaje."
        )
        layout.addWidget(
            self._text_card(
                "Secuencia de estudio",
                sequence,
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
            "Cada sesión selecciona una combinación diferente de ejercicios. Escribe tu respuesta, "
            "revela pistas progresivamente y compara después con la solución de referencia.",
            "moduleSectionNotice",
        )
        layout.addWidget(notice)
        layout.addWidget(GuidedPracticeWidget(self._module.practice_exercises))
        layout.addStretch(1)
        return self._scroll_area(body, "modulePracticeScroll")

    def _build_assessment_tab(self) -> QScrollArea:
        body = self._scroll_body()
        layout = body.layout()
        assert isinstance(layout, QVBoxLayout)

        if self._objective_question_bank:
            objective_heading = self._subheading("Práctica objetiva aleatoria")
            objective_heading.setObjectName("objectiveAssessmentSectionTitle")
            layout.addWidget(objective_heading)
            notice = self._label(
                "Responde cada pregunta y pulsa Comprobar respuesta para obtener corrección "
                "inmediata. Nueva práctica genera otra combinación del banco y vuelve a "
                "barajar las opciones.",
                "moduleSectionNotice",
            )
            layout.addWidget(notice)
            layout.addWidget(ObjectiveAssessmentWidget(self._objective_question_bank))

        complete_heading = self._subheading("Evaluación completa del módulo")
        complete_heading.setObjectName("authoredAssessmentSectionTitle")
        layout.addWidget(complete_heading)
        complete_notice = self._label(
            "Estas actividades cubren trazado, depuración, ordenación, relación de conceptos, "
            "código, interpretación y respuestas abiertas. Las soluciones permanecen separadas "
            "del lector para conservar su función evaluativa.",
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
        layout.addWidget(self._subheading("Puntos esenciales"))
        layout.addWidget(self._label(self._bullets(concept.key_points), "contentBulletList"))
        return card

    def _example_card(self, example: WorkedExample) -> QFrame:
        card, layout = self._card("exampleCard", example.title)
        layout.addWidget(self._subheading("Problema"))
        layout.addWidget(self._label(example.problem, "contentBody"))
        layout.addWidget(self._subheading("Razonamiento"))
        layout.addWidget(self._label(self._numbered(example.reasoning), "contentBulletList"))
        layout.addWidget(self._subheading("Código"))
        layout.addWidget(self._code_block(example.code, "exampleCode"))
        layout.addWidget(self._subheading("Salida esperada"))
        layout.addWidget(self._code_block(example.expected_output, "exampleOutput"))
        layout.addWidget(self._subheading("Explicación"))
        layout.addWidget(self._label(example.explanation, "contentBody"))
        return card

    def _assessment_card(self, number: int, item: AssessmentItem) -> QFrame:
        activity = self._activity_label(item.activity_type.value)
        card, layout = self._card("assessmentCard", f"Pregunta {number} · {activity}")
        layout.addWidget(self._label(item.prompt, "assessmentPrompt"))

        if item.options:
            layout.addWidget(self._subheading("Opciones"))
            layout.addWidget(self._label(self._bullets(item.options), "assessmentOptions"))

        if item.rubric:
            layout.addWidget(self._subheading("Criterios que se evaluarán"))
            layout.addWidget(self._label(self._bullets(item.rubric), "assessmentRubric"))
        return card

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

    @staticmethod
    def _activity_label(value: str) -> str:
        return _ACTIVITY_LABELS.get(value, value.replace("_", " ").capitalize())
