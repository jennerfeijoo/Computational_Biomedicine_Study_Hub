"""PySide6 renderer for one authored learning module."""

from __future__ import annotations

from collections.abc import Iterable

from PySide6.QtCore import Qt
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
    """Render theory, examples, guided practice and module-specific assessment."""

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

        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(8)
        if show_context_bar:
            layout.addWidget(self._build_context_bar())

        self._tabs = QTabWidget()
        self._tabs.setObjectName("moduleTabs")
        self._tabs.setDocumentMode(True)
        self._tabs.setUsesScrollButtons(True)
        self._tabs.addTab(self._build_overview_tab(), "Resumen")
        self._tabs.addTab(self._build_concepts_tab(), "Conceptos")
        self._tabs.addTab(self._build_examples_tab(), "Ejemplos")
        self._tabs.addTab(self._build_practice_tab(), "Práctica")
        self._tabs.addTab(self._build_assessment_tab(), "Evaluación")
        layout.addWidget(self._tabs, 1)

    @property
    def module(self) -> LearningModule:
        """Return the module rendered by this page."""
        return self._module

    @property
    def current_section(self) -> str:
        """Return the visible section label."""
        return self._tabs.tabText(self._tabs.currentIndex())

    def select_section(self, label: str) -> bool:
        """Select a section by its visible label."""
        for index in range(self._tabs.count()):
            if self._tabs.tabText(index) == label:
                self._tabs.setCurrentIndex(index)
                return True
        return False

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
            notice = self._label(
                "Responde cada pregunta y pulsa Comprobar respuesta para obtener corrección "
                "inmediata. Nueva práctica genera otra combinación del banco y vuelve a "
                "barajar las opciones.",
                "moduleSectionNotice",
            )
            layout.addWidget(notice)
            layout.addWidget(ObjectiveAssessmentWidget(self._objective_question_bank))
        else:
            notice = self._label(
                "Las respuestas correctas permanecen separadas del lector. Los controles "
                "interactivos se activarán cuando el módulo disponga de un banco objetivo.",
                "moduleSectionNotice",
            )
            layout.addWidget(notice)

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
