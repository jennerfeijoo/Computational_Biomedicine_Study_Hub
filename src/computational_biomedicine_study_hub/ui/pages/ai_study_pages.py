"""Interactive AI study pages: flashcards, anonymous mixed assessments and code review."""

from __future__ import annotations

from dataclasses import dataclass

from PySide6.QtCore import QRegularExpression, QThread, Qt, Signal
from PySide6.QtGui import QFont, QSyntaxHighlighter, QTextCharFormat
from PySide6.QtWidgets import (
    QComboBox,
    QGroupBox,
    QHBoxLayout,
    QLabel,
    QListWidget,
    QListWidgetItem,
    QMessageBox,
    QPushButton,
    QPlainTextEdit,
    QRadioButton,
    QScrollArea,
    QTabWidget,
    QTextEdit,
    QVBoxLayout,
    QWidget,
)

from ...content.models import LearningModule
from ...i18n import AppLocale
from ...learning.ai_study_service import AIStudyService, CodeFeedback
from ...learning.module_catalog import modules_for_course, modules_for_locale
from ...storage.ai_learning_store import AILearningStore, FlashcardRecord, GeneratedQuestion


class PythonHighlighter(QSyntaxHighlighter):
    """Small dependency-free syntax highlighter for Python-like student code."""

    def __init__(self, document: object) -> None:
        super().__init__(document)
        self._rules = []
        keyword = QTextCharFormat()
        keyword.setFontWeight(QFont.Weight.Bold)
        for word in (
            "and or not if else elif for while in def return class import from as try except finally with lambda yield True False None",
        )[0].split():
            self._rules.append((QRegularExpression(rf"\\b{word}\\b"), keyword))

    def highlightBlock(self, text: str) -> None:  # noqa: N802
        for pattern, fmt in self._rules:
            match = pattern.match(text)
            while match.hasMatch():
                self.setFormat(match.capturedStart(), match.capturedLength(), fmt)
                match = pattern.match(text, match.capturedEnd())


@dataclass(frozen=True, slots=True)
class _AsyncResult:
    value: object
    error: Exception | None = None


class _Worker(QThread):
    """Run one AI operation off the Qt GUI thread and return a typed result."""

    completed = Signal(object)

    def __init__(self, operation) -> None:
        super().__init__()
        self._operation = operation

    def run(self) -> None:
        try:
            self.completed.emit(_AsyncResult(self._operation()))
        except Exception as exc:  # pragma: no cover - transport-specific failures
            self.completed.emit(_AsyncResult(None, exc))


class FlashcardsPage(QWidget):
    """Load persisted flashcards and generate them from the currently selected module."""

    def __init__(self, store: AILearningStore, locale: AppLocale, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self._store = store
        self._locale = locale
        self._service = AIStudyService(store)
        self._cards: tuple[FlashcardRecord, ...] = ()
        self._index = 0
        self._worker: _Worker | None = None

        self._course = QComboBox()
        self._module = QComboBox()
        self._course.addItems(["DM857", "DM847", "BMB830", "BMB831"])
        self._course.currentTextChanged.connect(self._refresh_modules)
        self._module.currentIndexChanged.connect(self._load_cards)

        self._status = QLabel()
        self._status.setWordWrap(True)
        self._card = QLabel()
        self._card.setWordWrap(True)
        self._card.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self._card.setMinimumHeight(220)
        self._card.setObjectName("flashcardContent")

        self._generate = QPushButton(self._text("Generar tarjetas con IA", "Generate flashcards with AI", "AI-kaartjes genereren"))
        self._generate.clicked.connect(self._generate_cards)
        self._previous = QPushButton("←")
        self._next = QPushButton("→")
        self._previous.clicked.connect(lambda: self._move(-1))
        self._next.clicked.connect(lambda: self._move(1))
        self._reveal = QPushButton(self._text("Mostrar respuesta", "Show answer", "Vis svar"))
        self._reveal.clicked.connect(self._reveal_card)

        controls = QHBoxLayout()
        controls.addWidget(QLabel(self._text("Asignatura", "Course", "Kursus")))
        controls.addWidget(self._course)
        controls.addWidget(QLabel(self._text("Módulo", "Module", "Modul")))
        controls.addWidget(self._module, 1)

        navigation = QHBoxLayout()
        navigation.addWidget(self._previous)
        navigation.addWidget(self._reveal, 1)
        navigation.addWidget(self._next)

        layout = QVBoxLayout(self)
        layout.addLayout(controls)
        layout.addWidget(self._status)
        layout.addWidget(self._card, 1)
        layout.addWidget(self._generate)
        layout.addLayout(navigation)
        self._refresh_modules("DM857")

    def _refresh_modules(self, course_code: str) -> None:
        self._module.blockSignals(True)
        self._module.clear()
        for module in modules_for_course(course_code, self._locale):
            self._module.addItem(module.title, module.module_id)
        self._module.blockSignals(False)
        self._load_cards()

    def _load_cards(self) -> None:
        module_id = self._module.currentData()
        if not module_id:
            self._cards = ()
            self._render_empty()
            return
        self._cards = self._store.list_flashcards(self._course.currentText(), str(module_id))
        self._index = 0
        if self._cards:
            self._render_front()
        else:
            self._render_empty()

    def _render_empty(self) -> None:
        self._card.setText(self._text(
            "No hay tarjetas guardadas para este módulo. Usa el botón para generarlas con IA.",
            "No saved flashcards exist for this module. Use the button to generate them with AI.",
            "Der er ingen gemte kort for dette modul. Brug knappen til at generere dem med AI.",
        ))
        self._status.setText(self._text("0 tarjetas", "0 cards", "0 kort"))
        self._previous.setEnabled(False)
        self._next.setEnabled(False)
        self._reveal.setEnabled(False)

    def _render_front(self) -> None:
        card = self._cards[self._index]
        self._card.setText(card.front)
        self._status.setText(f"{self._index + 1}/{len(self._cards)}")
        self._previous.setEnabled(self._index > 0)
        self._next.setEnabled(self._index < len(self._cards) - 1)
        self._reveal.setEnabled(True)

    def _reveal_card(self) -> None:
        if self._cards:
            card = self._cards[self._index]
            self._card.setText(f"{card.front}\n\n—\n\n{card.back}")

    def _move(self, delta: int) -> None:
        if not self._cards:
            return
        self._index = max(0, min(len(self._cards) - 1, self._index + delta))
        self._render_front()

    def _generate_cards(self) -> None:
        module_id = self._module.currentData()
        if not module_id:
            return
        module = next(module for module in modules_for_locale(self._locale) if module.module_id == module_id)
        self._generate.setEnabled(False)
        self._status.setText(self._text("Generando…", "Generating…", "Genererer…"))
        self._worker = _Worker(lambda: self._service.generate_flashcards(module))
        self._worker.completed.connect(self._generation_finished)
        self._worker.start()

    def _generation_finished(self, result: _AsyncResult) -> None:
        self._generate.setEnabled(True)
        if result.error is not None:
            self._status.setText(str(result.error))
            return
        self._load_cards()

    def _text(self, es: str, en: str, da: str) -> str:
        return {AppLocale.SPANISH_SPAIN: es, AppLocale.ENGLISH: en, AppLocale.DANISH_DENMARK: da}[self._locale]


class SmartAssessmentsPage(QWidget):
    """Generate mixed, anonymous questions and provide AI-assisted programming feedback."""

    def __init__(self, store: AILearningStore, locale: AppLocale, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self._store = store
        self._locale = locale
        self._service = AIStudyService(store)
        self._questions: tuple[GeneratedQuestion, ...] = ()
        self._question_index = 0
        self._worker: _Worker | None = None
        self._modules: tuple[LearningModule, ...] = ()

        tabs = QTabWidget()
        tabs.addTab(self._build_assessment_tab(), self._text("Evaluación inteligente", "Smart assessment", "Intelligent evaluering"))
        tabs.addTab(self._build_code_tab(), self._text("Ejercicios de programación", "Programming exercises", "Programmeringsøvelser"))
        layout = QVBoxLayout(self)
        layout.addWidget(tabs)

    def _build_assessment_tab(self) -> QWidget:
        page = QWidget()
        layout = QVBoxLayout(page)
        course_row = QHBoxLayout()
        self._course = QComboBox()
        self._course.addItems(["DM857", "DM847", "BMB830", "BMB831"])
        self._course.currentTextChanged.connect(self._refresh_module_list)
        course_row.addWidget(QLabel(self._text("Asignatura", "Course", "Kursus")))
        course_row.addWidget(self._course)
        layout.addLayout(course_row)

        self._module_list = QListWidget()
        self._module_list.setSelectionMode(QListWidget.SelectionMode.NoSelection)
        layout.addWidget(QLabel(self._text("Selecciona uno o varios módulos. Las preguntas aparecerán mezcladas y sin etiquetas de módulo.", "Select one or more modules. Questions are mixed and never labelled by module.", "Vælg et eller flere moduler. Spørgsmål blandes og mærkes aldrig med modulnavn.")))
        layout.addWidget(self._module_list)

        self._start = QPushButton(self._text("Iniciar evaluación", "Start assessment", "Start evaluering"))
        self._start.clicked.connect(self._start_assessment)
        layout.addWidget(self._start)

        self._question = QLabel()
        self._question.setWordWrap(True)
        self._question.setMinimumHeight(100)
        self._answer_area = QWidget()
        self._answer_layout = QVBoxLayout(self._answer_area)
        self._feedback = QLabel()
        self._feedback.setWordWrap(True)
        self._submit = QPushButton(self._text("Responder", "Submit", "Svar"))
        self._submit.clicked.connect(self._submit_answer)
        layout.addWidget(self._question)
        layout.addWidget(self._answer_area)
        layout.addWidget(self._submit)
        layout.addWidget(self._feedback)
        self._submit.setEnabled(False)
        self._refresh_module_list("DM857")
        return page

    def _refresh_module_list(self, course_code: str) -> None:
        self._module_list.clear()
        for module in modules_for_course(course_code, self._locale):
            item = QListWidgetItem(module.title)
            item.setData(Qt.ItemDataRole.UserRole, module.module_id)
            item.setFlags(item.flags() | Qt.ItemFlag.ItemIsUserCheckable)
            item.setCheckState(Qt.CheckState.Unchecked)
            self._module_list.addItem(item)

    def _selected_modules(self) -> tuple[LearningModule, ...]:
        ids = {
            str(self._module_list.item(index).data(Qt.ItemDataRole.UserRole))
            for index in range(self._module_list.count())
            if self._module_list.item(index).checkState() == Qt.CheckState.Checked
        }
        return tuple(module for module in modules_for_course(self._course.currentText(), self._locale) if module.module_id in ids)

    def _start_assessment(self) -> None:
        modules = self._selected_modules()
        if not modules:
            self._feedback.setText(self._text("Selecciona al menos un módulo.", "Select at least one module.", "Vælg mindst ét modul."))
            return
        self._modules = modules
        self._start.setEnabled(False)
        self._submit.setEnabled(False)
        self._feedback.setText(self._text("Generando preguntas…", "Generating questions…", "Genererer spørgsmål…"))
        self._worker = _Worker(lambda: self._service.generate_assessment(modules))
        self._worker.completed.connect(self._assessment_generated)
        self._worker.start()

    def _assessment_generated(self, result: _AsyncResult) -> None:
        self._start.setEnabled(True)
        if result.error is not None:
            self._feedback.setText(str(result.error))
            return
        self._questions = tuple(result.value)
        self._question_index = 0
        self._render_question()

    def _render_question(self) -> None:
        self._clear_answer_area()
        if not self._questions or self._question_index >= len(self._questions):
            self._question.setText(self._text("Evaluación completada.", "Assessment completed.", "Evaluering afsluttet."))
            self._submit.setEnabled(False)
            return
        question = self._questions[self._question_index]
        self._question.setText(f"{self._question_index + 1}/{len(self._questions)}\n\n{question.prompt}")
        if question.question_type == "multiple_choice":
            group = []
            for option in question.options:
                button = QRadioButton(option)
                group.append(button)
                self._answer_layout.addWidget(button)
        else:
            editor = QTextEdit()
            editor.setObjectName("shortReasoningAnswer")
            editor.setPlaceholderText(self._text("Explica tu razonamiento…", "Explain your reasoning…", "Forklar din begrundelse…"))
            self._answer_layout.addWidget(editor)
        self._submit.setEnabled(True)
        self._feedback.clear()

    def _current_answer(self) -> str:
        question = self._questions[self._question_index]
        if question.question_type == "multiple_choice":
            for index in range(self._answer_layout.count()):
                widget = self._answer_layout.itemAt(index).widget()
                if isinstance(widget, QRadioButton) and widget.isChecked():
                    return widget.text()
            return ""
        editor = self.findChild(QTextEdit, "shortReasoningAnswer")
        return editor.toPlainText().strip() if editor is not None else ""

    def _submit_answer(self) -> None:
        if not self._questions:
            return
        answer = self._current_answer()
        if not answer:
            self._feedback.setText(self._text("Introduce una respuesta.", "Enter an answer.", "Indtast et svar."))
            return
        question = self._questions[self._question_index]
        if question.question_type == "multiple_choice":
            correct, feedback = self._service.grade_multiple_choice(question, answer)
            self._finish_question(correct, feedback, answer)
        else:
            self._submit.setEnabled(False)
            self._worker = _Worker(lambda: self._service.grade_short_answer(question, answer))
            self._worker.completed.connect(lambda result, q=question, a=answer: self._short_graded(result, q, a))
            self._worker.start()

    def _short_graded(self, result: _AsyncResult, question: GeneratedQuestion, answer: str) -> None:
        self._submit.setEnabled(True)
        if result.error is not None:
            self._feedback.setText(str(result.error))
            return
        correct, feedback = result.value
        self._finish_question(bool(correct), str(feedback), answer)

    def _finish_question(self, correct: bool, feedback: str, answer: str) -> None:
        question = self._questions[self._question_index]
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
        self._submit.setText(self._text("Responder", "Submit", "Svar"))
        self._question_index += 1
        self._render_question()

    def _clear_answer_area(self) -> None:
        while self._answer_layout.count():
            item = self._answer_layout.takeAt(0)
            widget = item.widget()
            if widget is not None:
                widget.deleteLater()

    def _build_code_tab(self) -> QWidget:
        page = QWidget()
        layout = QVBoxLayout(page)
        row = QHBoxLayout()
        self._code_course = QComboBox()
        self._code_course.addItems(["DM857", "DM847", "BMB830", "BMB831"])
        self._code_module = QComboBox()
        self._code_course.currentTextChanged.connect(self._refresh_code_modules)
        self._code_module.currentIndexChanged.connect(self._refresh_code_exercises)
        self._code_exercise = QComboBox()
        row.addWidget(self._code_course)
        row.addWidget(self._code_module, 1)
        row.addWidget(self._code_exercise, 1)
        layout.addLayout(row)

        self._code_prompt = QLabel()
        self._code_prompt.setWordWrap(True)
        layout.addWidget(self._code_prompt)
        self._code_editor = QPlainTextEdit()
        self._code_editor.setFont(QFont("Consolas", 10))
        PythonHighlighter(self._code_editor.document())
        layout.addWidget(self._code_editor, 1)
        self._send_code = QPushButton(self._text("Analizar código con IA", "Review code with AI", "Analyser kode med AI"))
        self._send_code.clicked.connect(self._review_code)
        layout.addWidget(self._send_code)
        self._code_feedback = QTextEdit()
        self._code_feedback.setReadOnly(True)
        layout.addWidget(self._code_feedback, 1)
        self._refresh_code_modules("DM857")
        return page

    def _refresh_code_modules(self, course_code: str) -> None:
        self._code_module.clear()
        for module in modules_for_course(course_code, self._locale):
            self._code_module.addItem(module.title, module.module_id)
        self._refresh_code_exercises()

    def _refresh_code_exercises(self) -> None:
        self._code_exercise.clear()
        module_id = self._code_module.currentData()
        if not module_id:
            self._code_prompt.clear()
            return
        module = next((m for m in modules_for_locale(self._locale) if m.module_id == module_id), None)
        if module is None:
            return
        for exercise in module.practice_exercises:
            if exercise.starter_code or exercise.solution:
                self._code_exercise.addItem(exercise.exercise_id, exercise.exercise_id)
        self._code_exercise.currentIndexChanged.connect(self._show_code_exercise)
        self._show_code_exercise()

    def _show_code_exercise(self) -> None:
        module_id = self._code_module.currentData()
        exercise_id = self._code_exercise.currentData()
        if not module_id or not exercise_id:
            return
        module = next((m for m in modules_for_locale(self._locale) if m.module_id == module_id), None)
        if module is None:
            return
        exercise = next((e for e in module.practice_exercises if e.exercise_id == exercise_id), None)
        if exercise is None:
            return
        self._code_prompt.setText(exercise.prompt)
        self._code_editor.setPlainText(exercise.starter_code)

    def _review_code(self) -> None:
        module_id = self._code_module.currentData()
        exercise_id = self._code_exercise.currentData()
        if not module_id or not exercise_id:
            return
        module = next(m for m in modules_for_locale(self._locale) if m.module_id == module_id)
        exercise = next(e for e in module.practice_exercises if e.exercise_id == exercise_id)
        source = self._code_editor.toPlainText().strip()
        if not source:
            self._code_feedback.setPlainText(self._text("Escribe o modifica el código antes de enviarlo.", "Write or modify the code before submitting.", "Skriv eller rediger koden før indsendelse."))
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

    def _text(self, es: str, en: str, da: str) -> str:
        return {AppLocale.SPANISH_SPAIN: es, AppLocale.ENGLISH: en, AppLocale.DANISH_DENMARK: da}[self._locale]


__all__ = ["FlashcardsPage", "SmartAssessmentsPage"]
