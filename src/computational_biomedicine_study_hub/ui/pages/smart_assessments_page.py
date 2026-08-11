"""Module-aware intelligent assessment UI.

Programming review is part of an assessment session and is shown only when the selected
modules contain explicit programming exercises.
"""

from __future__ import annotations

from dataclasses import dataclass

from PySide6.QtCore import QRegularExpression, Qt
from PySide6.QtGui import QFont, QSyntaxHighlighter, QTextCharFormat
from PySide6.QtWidgets import (
    QComboBox,
    QHBoxLayout,
    QLabel,
    QListWidget,
    QListWidgetItem,
    QPlainTextEdit,
    QRadioButton,
    QPushButton,
    QTextEdit,
    QVBoxLayout,
    QWidget,
)

from ...content.models import LearningModule
from ...i18n import AppLocale
from ...integrations.ollama import OllamaConfig
from ...integrations.ollama_chat import OllamaChatClient
from ...learning.ai_study_service import CodeFeedback
from ...learning.module_catalog import modules_for_course
from ...learning.smart_assessment_service import SmartAssessmentService, programming_exercises
from ...storage.ai_learning_store import AILearningStore, GeneratedQuestion
from .ai_study_pages import _AsyncResult, _Worker


class PythonHighlighter(QSyntaxHighlighter):
    """Small dependency-free syntax highlighter for Python-like student code."""

    def __init__(self, document: object) -> None:
        super().__init__(document)
        keyword = QTextCharFormat()
        keyword.setFontWeight(QFont.Weight.Bold)
        self._rules = [
            (QRegularExpression(rf"\\b{word}\\b"), keyword)
            for word in (
                "and or not if else elif for while in def return class import from as "
                "try except finally with lambda yield True False None"
            ).split()
        ]

    def highlightBlock(self, text: str) -> None:  # noqa: N802
        for pattern, fmt in self._rules:
            match = pattern.match(text)
            while match.hasMatch():
                self.setFormat(match.capturedStart(), match.capturedLength(), fmt)
                match = pattern.match(text, match.capturedEnd())


@dataclass(frozen=True, slots=True)
class _AssessmentState:
    questions: tuple[GeneratedQuestion, ...] = ()
    index: int = 0


class SmartAssessmentsPage(QWidget):
    """Run mixed module assessments and optional module-specific code review."""

    def __init__(self, store: AILearningStore, locale: AppLocale, settings=None, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self._store = store
        self._locale = locale
        base_url = str(settings.value("ollama/base_url", "") if settings is not None else "").strip()
        selected_model = str(settings.value("ollama/model", "") if settings is not None else "").strip()
        client = OllamaChatClient(OllamaConfig(base_url=base_url)) if base_url else OllamaChatClient()
        self._service = SmartAssessmentService(store, client=client, model=selected_model)
        self._state = _AssessmentState()
        self._worker: _Worker | None = None
        self._modules: tuple[LearningModule, ...] = ()

        layout = QVBoxLayout(self)
        course_row = QHBoxLayout()
        self._course = QComboBox()
        self._course.addItems(["DM857", "DM847", "BMB830", "BMB831"])
        self._course.currentTextChanged.connect(self._refresh_module_list)
        course_row.addWidget(QLabel(self._text("Asignatura", "Course", "Kursus")))
        course_row.addWidget(self._course, 1)
        layout.addLayout(course_row)

        self._module_list = QListWidget()
        self._module_list.setSelectionMode(QListWidget.SelectionMode.NoSelection)
        layout.addWidget(QLabel(self._text(
            "Selecciona uno o varios módulos. Las preguntas se mezclarán y nunca mostrarán el módulo de origen.",
            "Select one or more modules. Questions are mixed and never show their source module.",
            "Vælg et eller flere moduler. Spørgsmål blandes og viser aldrig kildemodulet.",
        )))
        layout.addWidget(self._module_list)

        self._start = QPushButton(self._text("Iniciar evaluación", "Start assessment", "Start evaluering"))
        self._start.clicked.connect(self._start_assessment)
        layout.addWidget(self._start)

        self._question = QLabel()
        self._question.setWordWrap(True)
        self._answer_area = QWidget()
        self._answer_layout = QVBoxLayout(self._answer_area)
        self._feedback = QLabel()
        self._feedback.setWordWrap(True)
        self._submit = QPushButton(self._text("Responder", "Submit", "Svar"))
        self._submit.clicked.connect(self._submit_answer)
        self._submit.setEnabled(False)
        layout.addWidget(self._question)
        layout.addWidget(self._answer_area)
        layout.addWidget(self._submit)
        layout.addWidget(self._feedback)

        self._code_title = QLabel(self._text(
            "Parte práctica de programación",
            "Programming component",
            "Programmeringsdel",
        ))
        self._code_title.setVisible(False)
        layout.addWidget(self._code_title)
        self._code_module = QComboBox()
        self._code_module.setVisible(False)
        self._code_module.currentIndexChanged.connect(self._refresh_code_exercises)
        layout.addWidget(self._code_module)
        self._code_exercise = QComboBox()
        self._code_exercise.setVisible(False)
        self._code_exercise.currentIndexChanged.connect(self._show_code_exercise)
        layout.addWidget(self._code_exercise)
        self._code_prompt = QLabel()
        self._code_prompt.setWordWrap(True)
        self._code_prompt.setVisible(False)
        layout.addWidget(self._code_prompt)
        self._code_editor = QPlainTextEdit()
        self._code_editor.setFont(QFont("Consolas", 10))
        self._code_editor.setVisible(False)
        PythonHighlighter(self._code_editor.document())
        layout.addWidget(self._code_editor, 1)
        self._send_code = QPushButton(self._text("Analizar código con IA", "Review code with AI", "Analyser kode med AI"))
        self._send_code.setVisible(False)
        self._send_code.clicked.connect(self._review_code)
        layout.addWidget(self._send_code)
        self._code_feedback = QTextEdit()
        self._code_feedback.setReadOnly(True)
        self._code_feedback.setVisible(False)
        layout.addWidget(self._code_feedback, 1)

        self._refresh_module_list("DM857")

    def _refresh_module_list(self, course_code: str) -> None:
        self._module_list.clear()
        for module in modules_for_course(course_code, self._locale):
            item = QListWidgetItem(module.title)
            item.setData(Qt.ItemDataRole.UserRole, module.module_id)
            item.setFlags(item.flags() | Qt.ItemFlag.ItemIsUserCheckable)
            item.setCheckState(Qt.CheckState.Unchecked)
            self._module_list.addItem(item)
        self._hide_code_component()

    def _selected_modules(self) -> tuple[LearningModule, ...]:
        ids = {
            str(self._module_list.item(index).data(Qt.ItemDataRole.UserRole))
            for index in range(self._module_list.count())
            if self._module_list.item(index).checkState() == Qt.CheckState.Checked
        }
        return tuple(
            module
            for module in modules_for_course(self._course.currentText(), self._locale)
            if module.module_id in ids
        )

    def _start_assessment(self) -> None:
        modules = self._selected_modules()
        if not modules:
            self._feedback.setText(self._text("Selecciona al menos un módulo.", "Select at least one module.", "Vælg mindst ét modul."))
            return
        self._modules = modules
        self._start.setEnabled(False)
        self._submit.setEnabled(False)
        self._feedback.setText(self._text("Generando evaluación…", "Generating assessment…", "Genererer evaluering…"))
        self._worker = _Worker(lambda: self._service.generate_assessment(modules))
        self._worker.completed.connect(self._assessment_generated)
        self._worker.start()

    def _assessment_generated(self, result: _AsyncResult) -> None:
        self._start.setEnabled(True)
        if result.error is not None:
            self._feedback.setText(self._text("Error al generar: ", "Generation error: ", "Genereringsfejl: ") + str(result.error))
            return
        questions = tuple(result.value)
        self._state = _AssessmentState(questions=questions, index=0)
        self._refresh_code_component()
        self._render_question()

    def _render_question(self) -> None:
        self._clear_answer_area()
        if not self._state.questions or self._state.index >= len(self._state.questions):
            self._question.setText(self._text("Evaluación completada.", "Assessment completed.", "Evaluering afsluttet."))
            self._submit.setEnabled(False)
            return
        question = self._state.questions[self._state.index]
        self._question.setText(f"{self._state.index + 1}/{len(self._state.questions)}\n\n{question.prompt}")
        if question.question_type == "multiple_choice":
            for option in question.options:
                self._answer_layout.addWidget(QRadioButton(option))
        else:
            editor = QTextEdit()
            editor.setObjectName("shortReasoningAnswer")
            editor.setPlaceholderText(self._text("Explica tu razonamiento…", "Explain your reasoning…", "Forklar din begrundelse…"))
            self._answer_layout.addWidget(editor)
        self._feedback.clear()
        self._submit.setEnabled(True)
        self._submit.setText(self._text("Responder", "Submit", "Svar"))

    def _current_answer(self) -> str:
        question = self._state.questions[self._state.index]
        if question.question_type == "multiple_choice":
            for index in range(self._answer_layout.count()):
                widget = self._answer_layout.itemAt(index).widget()
                if isinstance(widget, QRadioButton) and widget.isChecked():
                    return widget.text()
            return ""
        editor = self.findChild(QTextEdit, "shortReasoningAnswer")
        return editor.toPlainText().strip() if editor is not None else ""

    def _submit_answer(self) -> None:
        if not self._state.questions:
            return
        answer = self._current_answer()
        if not answer:
            self._feedback.setText(self._text("Introduce una respuesta.", "Enter an answer.", "Indtast et svar."))
            return
        question = self._state.questions[self._state.index]
        if question.question_type == "multiple_choice":
            correct, feedback = self._service.grade_multiple_choice(question, answer)
            self._finish_question(correct, feedback, answer)
            return
        self._submit.setEnabled(False)
        self._worker = _Worker(lambda: self._service.grade_short_answer(question, answer))
        self._worker.completed.connect(lambda result, q=question, a=answer: self._short_graded(result, q, a))
        self._worker.start()

    def _short_graded(self, result: _AsyncResult, question: GeneratedQuestion, answer: str) -> None:
        if result.error is not None:
            self._submit.setEnabled(True)
            self._feedback.setText(str(result.error))
            return
        correct, feedback = result.value
        self._finish_question(bool(correct), str(feedback), answer)

    def _finish_question(self, correct: bool, feedback: str, answer: str) -> None:
        question = self._state.questions[self._state.index]
        self._store.record_question_attempt(
            question_id=question.question_id,
            course_code=question.course_code,
            module_id=question.module_id,
            is_correct=correct,
            user_answer=answer,
            feedback=feedback,
        )
        self._feedback.setText(("✓ " if correct else "✗ ") + feedback)
        self._submit.setText(self._text("Siguiente", "Next", "Næste"))
        try:
            self._submit.clicked.disconnect()
        except RuntimeError:
            pass
        self._submit.clicked.connect(self._next_question)

    def _next_question(self) -> None:
        try:
            self._submit.clicked.disconnect()
        except RuntimeError:
            pass
        self._submit.clicked.connect(self._submit_answer)
        self._state = _AssessmentState(self._state.questions, self._state.index + 1)
        self._render_question()

    def _refresh_code_component(self) -> None:
        eligible = tuple(module for module in self._modules if programming_exercises(module))
        if not eligible:
            self._hide_code_component()
            return
        self._code_module.blockSignals(True)
        self._code_module.clear()
        for module in eligible:
            self._code_module.addItem(module.title, module.module_id)
        self._code_module.blockSignals(False)
        self._show_code_component()
        self._refresh_code_exercises()

    def _refresh_code_exercises(self) -> None:
        self._code_exercise.blockSignals(True)
        self._code_exercise.clear()
        module_id = self._code_module.currentData()
        module = next((m for m in self._modules if m.module_id == module_id), None)
        if module is None:
            self._code_exercise.blockSignals(False)
            self._code_prompt.clear()
            return
        for exercise in programming_exercises(module):
            self._code_exercise.addItem(exercise.exercise_id, exercise.exercise_id)
        self._code_exercise.blockSignals(False)
        self._show_code_exercise()

    def _show_code_exercise(self) -> None:
        module_id = self._code_module.currentData()
        exercise_id = self._code_exercise.currentData()
        module = next((m for m in self._modules if m.module_id == module_id), None)
        if module is None or not exercise_id:
            self._code_prompt.clear()
            self._code_editor.clear()
            return
        exercise = next((e for e in programming_exercises(module) if e.exercise_id == exercise_id), None)
        if exercise is None:
            return
        self._code_prompt.setText(exercise.prompt)
        self._code_editor.setPlainText(exercise.starter_code)

    def _review_code(self) -> None:
        module_id = self._code_module.currentData()
        exercise_id = self._code_exercise.currentData()
        module = next((m for m in self._modules if m.module_id == module_id), None)
        if module is None or not exercise_id:
            return
        exercise = next((e for e in programming_exercises(module) if e.exercise_id == exercise_id), None)
        if exercise is None:
            return
        source = self._code_editor.toPlainText().strip()
        if not source:
            self._code_feedback.setPlainText(self._text(
                "Escribe o modifica el código antes de enviarlo.",
                "Write or modify the code before submitting.",
                "Skriv eller rediger koden før indsendelse.",
            ))
            return
        self._send_code.setEnabled(False)
        self._code_feedback.setPlainText(self._text("Analizando…", "Reviewing…", "Analyserer…"))
        self._worker = _Worker(lambda: self._service.review_code(
            course_code=module.course_code,
            module=module,
            exercise_id=exercise.exercise_id,
            prompt=exercise.prompt,
            source_code=source,
        ))
        self._worker.completed.connect(self._code_review_finished)
        self._worker.start()

    def _code_review_finished(self, result: _AsyncResult) -> None:
        self._send_code.setEnabled(True)
        if result.error is not None:
            self._code_feedback.setPlainText(str(result.error))
            return
        feedback: CodeFeedback = result.value
        self._code_feedback.setPlainText(
            "1. Corrección\n" + feedback.correctness
            + "\n\n2. Complejidad y eficiencia\n" + feedback.complexity
            + "\n\n3. Buenas prácticas\n" + feedback.best_practices
            + "\n\n4. Sugerencia de mejora\n" + feedback.improvement
        )

    def _show_code_component(self) -> None:
        for widget in (
            self._code_title, self._code_module, self._code_exercise, self._code_prompt,
            self._code_editor, self._send_code, self._code_feedback,
        ):
            widget.setVisible(True)

    def _hide_code_component(self) -> None:
        for widget in (
            self._code_title, self._code_module, self._code_exercise, self._code_prompt,
            self._code_editor, self._send_code, self._code_feedback,
        ):
            widget.setVisible(False)

    def _clear_answer_area(self) -> None:
        while self._answer_layout.count():
            item = self._answer_layout.takeAt(0)
            widget = item.widget()
            if widget is not None:
                widget.deleteLater()

    def _text(self, es: str, en: str, da: str) -> str:
        return {AppLocale.SPANISH_SPAIN: es, AppLocale.ENGLISH: en, AppLocale.DANISH_DENMARK: da}[self._locale]


__all__ = ["SmartAssessmentsPage"]
