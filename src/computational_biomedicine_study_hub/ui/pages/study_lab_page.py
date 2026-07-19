"""Grounded local-Qwen study laboratory."""

from __future__ import annotations

import json
from collections.abc import Callable
from html import escape
from typing import Protocol

from PySide6.QtCore import QObject, QSettings, QThread, Signal, Slot
from PySide6.QtWidgets import (
    QComboBox,
    QFormLayout,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QTextBrowser,
    QTextEdit,
    QVBoxLayout,
    QWidget,
)

from ...academic.retrieval import LexicalRetriever
from ...academic.tutor import GroundedTutorRequest, TutorContextBuilder, TutorMode
from ...academic.tutor.context_builder import INSUFFICIENT_EVIDENCE
from ...academic.tutor.evaluation import FeedbackParseError, parse_open_response_feedback
from ...academic.tutor.response_models import OpenResponseFeedback
from ...integrations.ollama import OllamaConfig
from ...integrations.ollama_chat import (
    DEFAULT_CHAT_MODEL,
    ChatMessage,
    ChatResponse,
    ChatRole,
    OllamaChatClient,
)
from ...learning.academic_catalog import AcademicCatalog
from ..pages.ollama_settings_page import OllamaSettingsPage


class ChatClient(Protocol):
    def chat(
        self,
        messages: tuple[ChatMessage, ...],
        *,
        model: str,
        temperature: float = 0.2,
        keep_alive: str = "10m",
    ) -> ChatResponse: ...


class StudyLabWorker(QObject):
    progress = Signal(str)
    finished = Signal(object)
    failed = Signal(str)
    cancelled = Signal()

    def __init__(
        self,
        client: ChatClient,
        messages: tuple[ChatMessage, ...],
        model: str,
    ) -> None:
        super().__init__()
        self._client = client
        self._messages = messages
        self._model = model
        self._cancelled = False

    @Slot()
    def run(self) -> None:
        self.progress.emit("generating")
        try:
            response = self._client.chat(self._messages, model=self._model)
        except Exception as error:  # UI boundary translates local transport errors
            if self._cancelled:
                self.cancelled.emit()
            else:
                self.failed.emit(str(error))
            return
        if self._cancelled:
            self.cancelled.emit()
        else:
            self.finished.emit(response)

    @Slot()
    def cancel(self) -> None:
        self._cancelled = True


def _locale_code(value: str) -> str:
    normalized = value.casefold()
    if normalized.startswith("es"):
        return "es"
    if normalized.startswith("da"):
        return "da"
    return "en"


class StudyLabPage(QWidget):
    """Mode-driven study tool; Ollama is transport, never the source of truth."""

    def __init__(
        self,
        catalog: AcademicCatalog,
        settings: QSettings,
        *,
        client_factory: Callable[[OllamaConfig], ChatClient] | None = None,
        parent: QWidget | None = None,
    ) -> None:
        super().__init__(parent)
        self.setObjectName("studyLabPage")
        self._catalog = catalog
        self._settings = settings
        self._client_factory = client_factory or (lambda config: OllamaChatClient(config))
        locale = _locale_code(catalog.locale.value)
        self._locale_code = locale
        copy = _LAB_COPY[locale]
        self._retriever = LexicalRetriever.from_catalog(catalog.source_catalog, locale)
        self._builder = TutorContextBuilder(self._retriever)
        self._thread: QThread | None = None
        self._worker: StudyLabWorker | None = None
        self._last_question = ""
        self._last_answer = ""
        self._active_mode = TutorMode.ASK_CONTENT

        root = QVBoxLayout(self)
        form = QFormLayout()
        self.course_selector = QComboBox()
        for course_code in catalog.course_codes:
            self.course_selector.addItem(course_code, course_code)
        self.module_selector = QComboBox()
        self.scope_selector = QComboBox()
        self.scope_selector.addItem(copy["scope_module"], "module")
        self.scope_selector.addItem(copy["course"], "course")
        self.scope_selector.addItem(copy["semester"], "semester")
        self.mode_selector = QComboBox()
        for mode in TutorMode:
            self.mode_selector.addItem(_mode_label(locale, mode), mode.value)
        self.difficulty_selector = QComboBox()
        for difficulty in ("foundational", "intermediate", "advanced"):
            self.difficulty_selector.addItem(copy[difficulty], difficulty)
        self.language_selector = QComboBox()
        self.language_selector.addItem("Español", "es")
        self.language_selector.addItem("English", "en")
        self.language_selector.addItem("Dansk", "da")
        language_index = self.language_selector.findData(locale)
        self.language_selector.setCurrentIndex(max(0, language_index))
        form.addRow(copy["course"], self.course_selector)
        form.addRow(copy["module"], self.module_selector)
        form.addRow(copy["scope"], self.scope_selector)
        form.addRow(copy["mode"], self.mode_selector)
        form.addRow(copy["difficulty"], self.difficulty_selector)
        form.addRow(copy["language"], self.language_selector)
        root.addLayout(form)

        status_row = QHBoxLayout()
        self.status_label = QLabel(copy["ready"])
        self.status_label.setObjectName("studyLabStatus")
        self.model_label = QLabel(f"{copy['model']}: {self._selected_model()}")
        self.model_label.setObjectName("studyLabModel")
        status_row.addWidget(self.status_label)
        status_row.addStretch(1)
        status_row.addWidget(self.model_label)
        root.addLayout(status_row)

        self.history = QTextBrowser()
        self.history.setObjectName("studyLabHistory")
        self.history.setAccessibleName(copy["history"])
        root.addWidget(self.history, 1)

        self.sources = QTextBrowser()
        self.sources.setObjectName("studyLabSources")
        self.sources.setMaximumHeight(110)
        self.sources.setPlaceholderText(copy["sources"])
        root.addWidget(self.sources)

        self.question = QTextEdit()
        self.question.setObjectName("studyLabQuestion")
        self.question.setPlaceholderText(copy["question"])
        self.question.setMaximumHeight(130)
        root.addWidget(self.question)

        actions = QHBoxLayout()
        self.send_button = QPushButton(copy["send"])
        self.cancel_button = QPushButton(copy["cancel"])
        self.retry_button = QPushButton(copy["retry"])
        self.clear_button = QPushButton(copy["clear"])
        self.save_note_button = QPushButton(copy["save_note"])
        self.convert_card_button = QPushButton(copy["convert_card"])
        self.follow_up_button = QPushButton(copy["follow_up"])
        self.cancel_button.setEnabled(False)
        for button in (
            self.send_button,
            self.cancel_button,
            self.retry_button,
            self.clear_button,
            self.save_note_button,
            self.convert_card_button,
            self.follow_up_button,
        ):
            button.setMinimumHeight(38)
            actions.addWidget(button)
        root.addLayout(actions)

        self.send_button.clicked.connect(self.send)
        self.cancel_button.clicked.connect(self.cancel)
        self.retry_button.clicked.connect(self.retry)
        self.clear_button.clicked.connect(self.clear)
        self.save_note_button.clicked.connect(self.save_note)
        self.convert_card_button.clicked.connect(self.convert_to_card)
        self.follow_up_button.clicked.connect(self.create_follow_up)
        self.course_selector.currentIndexChanged.connect(self._refresh_modules)
        self._refresh_modules()

    def prefill_open_response_evaluation(
        self,
        *,
        course_code: str,
        module_id: str,
        item_id: str,
        response_text: str,
        confidence: str,
    ) -> None:
        """Carry a submitted authored response into the grounded evaluation mode."""
        course_index = self.course_selector.findData(course_code)
        if course_index >= 0:
            self.course_selector.setCurrentIndex(course_index)
        module_index = self.module_selector.findData(module_id)
        if module_index >= 0:
            self.module_selector.setCurrentIndex(module_index)
        mode_index = self.mode_selector.findData(TutorMode.EVALUATE_OPEN.value)
        if mode_index >= 0:
            self.mode_selector.setCurrentIndex(mode_index)
        scope_index = self.scope_selector.findData("module")
        if scope_index >= 0:
            self.scope_selector.setCurrentIndex(scope_index)
        authored = next(
            (
                item
                for item in self._catalog.assessment_items(
                    course_code=course_code,
                    module_id=module_id,
                )
                if item.item_id == item_id
            ),
            None,
        )
        prompt = authored.prompt if authored is not None else item_id
        self.question.setPlainText(
            f"Authored question ({item_id}):\n{prompt}\n\n"
            f"Learner confidence: {confidence}\n"
            f"Learner response:\n{response_text}\n\n"
            "Return the requested structured formative feedback grounded in the "
            "retrieved rubric and sources."
        )
        self.question.setFocus()

    @Slot()
    def _refresh_modules(self) -> None:
        course = self.course_selector.currentData()
        self.module_selector.clear()
        if isinstance(course, str):
            for record in self._catalog.modules(course):
                self.module_selector.addItem(record.title, record.module_id)

    @Slot()
    def send(self) -> None:
        if self._thread is not None:
            return
        question = self.question.toPlainText().strip()
        if not question:
            return
        self._last_question = question
        mode = TutorMode(str(self.mode_selector.currentData()))
        self._active_mode = mode
        scope = str(self.scope_selector.currentData())
        course = str(self.course_selector.currentData())
        module = str(self.module_selector.currentData()) if scope == "module" else None
        if scope == "semester":
            course = ""
        request = GroundedTutorRequest(
            question=question,
            course_id=course.casefold(),
            module_id=module,
            locale=str(self.language_selector.currentData()),
            difficulty=str(self.difficulty_selector.currentData()),
            mode=mode,
            learner_submitted_response=mode is TutorMode.EVALUATE_OPEN,
        )
        context = self._builder.build(request)
        self.history.append(f"<b>You</b><br>{question}")
        if context is None:
            answer = INSUFFICIENT_EVIDENCE[request.locale]
            self.history.append(f"<b>Study Lab</b><br>{answer}")
            self.status_label.setText(_LAB_COPY[self._locale_code]["insufficient"])
            return
        self.sources.setPlainText(
            "\n".join(f"• {item.fragment.source_label}" for item in context.sources)
        )
        messages = (
            ChatMessage(ChatRole.SYSTEM, context.system_prompt),
            ChatMessage(ChatRole.USER, context.user_prompt),
        )
        config = OllamaConfig(base_url=self._selected_base_url())
        worker = StudyLabWorker(self._client_factory(config), messages, self._selected_model())
        thread = QThread(self)
        worker.moveToThread(thread)
        thread.started.connect(worker.run)
        worker.progress.connect(self._progress)
        worker.finished.connect(self._complete)
        worker.failed.connect(self._fail)
        worker.cancelled.connect(self._cancelled)
        for signal in (worker.finished, worker.failed, worker.cancelled):
            signal.connect(thread.quit)
        thread.finished.connect(worker.deleteLater)
        thread.finished.connect(thread.deleteLater)
        thread.finished.connect(self._thread_finished)
        self._worker = worker
        self._thread = thread
        self.send_button.setEnabled(False)
        self.cancel_button.setEnabled(True)
        thread.start()

    @Slot()
    def cancel(self) -> None:
        if self._worker is not None:
            self._worker.cancel()
            self.status_label.setText(_LAB_COPY[self._locale_code]["cancelling"])

    @Slot()
    def retry(self) -> None:
        if self._last_question and self._thread is None:
            self.question.setPlainText(self._last_question)
            self.send()

    @Slot()
    def clear(self) -> None:
        if self._thread is None:
            self.history.clear()
            self.sources.clear()
            self.question.clear()
            self._last_answer = ""

    @Slot()
    def save_note(self) -> None:
        if not self._last_answer:
            return
        notes = self._stored_list("study_lab/notes")
        notes.append(
            {
                "question": self._last_question,
                "answer": self._last_answer,
                "sources": self.sources.toPlainText(),
            }
        )
        self._settings.setValue("study_lab/notes", json.dumps(notes, ensure_ascii=False))
        self.status_label.setText(_LAB_COPY[self._locale_code]["note_saved"])

    @Slot()
    def convert_to_card(self) -> None:
        if not self._last_answer:
            return
        cards = self._stored_list("study_lab/user_cards")
        cards.append(
            {
                "front": self._last_question,
                "back": self._last_answer,
                "course_id": str(self.course_selector.currentData()),
                "module_id": str(self.module_selector.currentData()),
                "source_ids": self.sources.toPlainText().splitlines(),
            }
        )
        self._settings.setValue("study_lab/user_cards", json.dumps(cards, ensure_ascii=False))
        self.status_label.setText(_LAB_COPY[self._locale_code]["card_saved"])

    @Slot()
    def create_follow_up(self) -> None:
        if self._last_answer:
            self.question.setPlainText(_LAB_COPY[self._locale_code]["follow_up_prompt"])

    @Slot(str)
    def _progress(self, state: str) -> None:
        self.status_label.setText(f"Ollama: {state}…")

    @Slot(object)
    def _complete(self, value: object) -> None:
        if not isinstance(value, ChatResponse):
            self._fail("Ollama returned an unexpected response.")
            return
        self._last_answer = value.content
        if self._active_mode is TutorMode.EVALUATE_OPEN:
            try:
                feedback = parse_open_response_feedback(value.content)
            except (FeedbackParseError, ValueError) as error:
                self.status_label.setText(
                    f"{_LAB_COPY[self._locale_code]['invalid_feedback']}: {error}"
                )
                self.history.append(
                    "<b>Study Lab</b><br>The local model returned an invalid "
                    "feedback structure. The response was not treated as an evaluation."
                )
                return
            self.history.append(_feedback_html(feedback, self._catalog.locale.value))
        else:
            self.history.append(f"<b>Study Lab</b><br>{escape(value.content)}")
        self.model_label.setText(f"{_LAB_COPY[self._locale_code]['model']}: {value.model}")
        self.status_label.setText(_LAB_COPY[self._locale_code]["complete"])

    @Slot(str)
    def _fail(self, message: str) -> None:
        self.status_label.setText(f"{_LAB_COPY[self._locale_code]['unavailable']}: {message}")
        self.history.append(
            "<b>Study Lab</b><br>The local model is unavailable. "
            "All static study features remain usable."
        )

    @Slot()
    def _cancelled(self) -> None:
        self.status_label.setText(_LAB_COPY[self._locale_code]["cancelled"])

    @Slot()
    def _thread_finished(self) -> None:
        self._thread = None
        self._worker = None
        self.send_button.setEnabled(True)
        self.cancel_button.setEnabled(False)

    def _selected_base_url(self) -> str:
        value = str(
            self._settings.value(
                OllamaSettingsPage.BASE_URL_KEY,
                OllamaConfig().normalized_base_url(),
            )
        )
        return OllamaConfig(base_url=value).normalized_base_url()

    def _selected_model(self) -> str:
        return (
            str(
                self._settings.value(
                    OllamaSettingsPage.MODEL_KEY,
                    DEFAULT_CHAT_MODEL,
                )
            ).strip()
            or DEFAULT_CHAT_MODEL
        )

    def _stored_list(self, key: str) -> list[dict[str, object]]:
        raw = str(self._settings.value(key, "[]"))
        try:
            value = json.loads(raw)
        except json.JSONDecodeError:
            return []
        return [item for item in value if isinstance(item, dict)] if isinstance(value, list) else []


def _feedback_html(feedback: OpenResponseFeedback, locale: str) -> str:
    language = _locale_code(locale)
    disclaimer = {
        "es": "Evaluación formativa local. No equivale a una calificación oficial.",
        "en": "Local formative evaluation. It is not an official grade.",
        "da": "Lokal formativ evaluering. Det er ikke en officiel karakter.",
    }[language]

    headings = _FEEDBACK_HEADINGS[language]

    def listing(title: str, values: tuple[str, ...]) -> str:
        if not values:
            return ""
        items = "".join(f"<li>{escape(item)}</li>" for item in values)
        return f"<h4>{escape(title)}</h4><ul>{items}</ul>"

    dimensions = "".join(
        f"<li><b>{escape(item.name)}: {item.score}/4</b> — {escape(item.evidence)}</li>"
        for item in feedback.rubric_dimensions
    )
    return (
        f"<b>Study Lab</b><br><i>{escape(disclaimer)}</i>"
        f"<p>{escape(feedback.summary)}</p>"
        f"{listing(headings['strengths'], feedback.strengths)}"
        f"{listing(headings['missing'], feedback.missing_concepts)}"
        f"{listing(headings['misconceptions'], feedback.misconceptions)}"
        f"{listing(headings['unsupported'], feedback.unsupported_claims)}"
        f"<h4>{headings['rubric']}</h4><ul>{dimensions}</ul>"
        f"<h4>{headings['revision']}</h4><p>{escape(feedback.suggested_revision)}</p>"
        f"<h4>{headings['follow_up']}</h4><p>{escape(feedback.follow_up_question)}</p>"
        f"<p><b>{headings['confidence']}:</b> {escape(feedback.evaluator_confidence)}</p>"
        f"<p><b>{headings['sources']}:</b> {escape(', '.join(feedback.source_ids))}</p>"
    )


_LAB_COPY = {
    "es": {
        "course": "Asignatura",
        "module": "Módulo",
        "scope": "Ámbito",
        "scope_module": "Módulo actual",
        "semester": "Semestre",
        "mode": "Modo",
        "difficulty": "Dificultad",
        "language": "Idioma",
        "foundational": "Fundacional",
        "intermediate": "Intermedia",
        "advanced": "Avanzada",
        "ready": "Ollama: preparado para conectar",
        "model": "Modelo",
        "history": "Historial de conversación de estudio",
        "sources": "Fuentes académicas utilizadas",
        "question": "Formula una pregunta de estudio fundamentada…",
        "send": "Enviar",
        "cancel": "Cancelar",
        "retry": "Reintentar",
        "clear": "Limpiar",
        "save_note": "Guardar como nota",
        "convert_card": "Convertir en tarjeta",
        "follow_up": "Crear seguimiento",
        "insufficient": "Evidencia insuficiente en el corpus",
        "cancelling": "Cancelación solicitada…",
        "note_saved": "Guardado como nota local",
        "card_saved": "Convertido en tarjeta local del usuario",
        "follow_up_prompt": "Crea una pregunta de seguimiento basada en las mismas fuentes.",
        "invalid_feedback": "Retroalimentación formativa no válida",
        "complete": "Ollama: completado",
        "unavailable": "Ollama no disponible",
        "cancelled": "Generación cancelada",
    },
    "en": {
        "course": "Course",
        "module": "Module",
        "scope": "Scope",
        "scope_module": "Current module",
        "semester": "Semester",
        "mode": "Mode",
        "difficulty": "Difficulty",
        "language": "Language",
        "foundational": "Foundational",
        "intermediate": "Intermediate",
        "advanced": "Advanced",
        "ready": "Ollama: ready to connect",
        "model": "Model",
        "history": "Study conversation history",
        "sources": "Academic sources used",
        "question": "Ask a grounded study question…",
        "send": "Send",
        "cancel": "Cancel",
        "retry": "Retry",
        "clear": "Clear",
        "save_note": "Save as note",
        "convert_card": "Convert to card",
        "follow_up": "Create follow-up",
        "insufficient": "Insufficient corpus evidence",
        "cancelling": "Cancellation requested…",
        "note_saved": "Saved as a local note",
        "card_saved": "Converted to a local user card",
        "follow_up_prompt": "Create one follow-up question grounded in the same sources.",
        "invalid_feedback": "Invalid formative feedback",
        "complete": "Ollama: complete",
        "unavailable": "Ollama unavailable",
        "cancelled": "Generation cancelled",
    },
    "da": {
        "course": "Kursus",
        "module": "Modul",
        "scope": "Omfang",
        "scope_module": "Aktuelt modul",
        "semester": "Semester",
        "mode": "Tilstand",
        "difficulty": "Sværhedsgrad",
        "language": "Sprog",
        "foundational": "Grundlæggende",
        "intermediate": "Mellem",
        "advanced": "Avanceret",
        "ready": "Ollama: klar til forbindelse",
        "model": "Model",
        "history": "Studiesamtalens historik",
        "sources": "Anvendte faglige kilder",
        "question": "Stil et fagligt funderet spørgsmål…",
        "send": "Send",
        "cancel": "Annullér",
        "retry": "Prøv igen",
        "clear": "Ryd",
        "save_note": "Gem som note",
        "convert_card": "Konvertér til kort",
        "follow_up": "Opret opfølgning",
        "insufficient": "Utilstrækkelig evidens i materialet",
        "cancelling": "Annullering anmodet…",
        "note_saved": "Gemt som lokal note",
        "card_saved": "Konverteret til lokalt brugerkort",
        "follow_up_prompt": "Opret ét opfølgende spørgsmål baseret på de samme kilder.",
        "invalid_feedback": "Ugyldig formativ feedback",
        "complete": "Ollama: færdig",
        "unavailable": "Ollama er ikke tilgængelig",
        "cancelled": "Generering annulleret",
    },
}

_MODE_LABELS = {
    "es": {
        TutorMode.ASK_CONTENT: "Preguntar sobre contenido",
        TutorMode.SOCRATIC: "Socrático",
        TutorMode.GENERATE_PRACTICE: "Generar práctica",
        TutorMode.EVALUATE_OPEN: "Evaluar respuesta abierta",
        TutorMode.EXPLAIN_ERROR: "Explicar error",
        TutorMode.ORAL_EXAM: "Preparar examen oral",
        TutorMode.REVIEW_PLAN: "Planificar repaso",
        TutorMode.COMPARE_METHODS: "Comparar métodos",
        TutorMode.ANALYZE_CODE: "Analizar código",
        TutorMode.CONTINUE_MODULE: "Continuar módulo",
    },
    "en": {mode: mode.value.replace("_", " ").title() for mode in TutorMode},
    "da": {
        TutorMode.ASK_CONTENT: "Spørg om indhold",
        TutorMode.SOCRATIC: "Sokratisk",
        TutorMode.GENERATE_PRACTICE: "Generér øvelse",
        TutorMode.EVALUATE_OPEN: "Vurdér åbent svar",
        TutorMode.EXPLAIN_ERROR: "Forklar fejl",
        TutorMode.ORAL_EXAM: "Forbered mundtlig eksamen",
        TutorMode.REVIEW_PLAN: "Planlæg repetition",
        TutorMode.COMPARE_METHODS: "Sammenlign metoder",
        TutorMode.ANALYZE_CODE: "Analysér kode",
        TutorMode.CONTINUE_MODULE: "Fortsæt modul",
    },
}

_FEEDBACK_HEADINGS = {
    "es": {
        "strengths": "Fortalezas",
        "missing": "Conceptos ausentes",
        "misconceptions": "Errores conceptuales",
        "unsupported": "Afirmaciones no respaldadas",
        "rubric": "Rúbrica",
        "revision": "Revisión sugerida",
        "follow_up": "Seguimiento",
        "confidence": "Confianza del evaluador",
        "sources": "Fuentes",
    },
    "en": {
        "strengths": "Strengths",
        "missing": "Missing concepts",
        "misconceptions": "Misconceptions",
        "unsupported": "Unsupported claims",
        "rubric": "Rubric",
        "revision": "Suggested revision",
        "follow_up": "Follow-up",
        "confidence": "Evaluator confidence",
        "sources": "Sources",
    },
    "da": {
        "strengths": "Styrker",
        "missing": "Manglende begreber",
        "misconceptions": "Misforståelser",
        "unsupported": "Udokumenterede påstande",
        "rubric": "Rubrik",
        "revision": "Foreslået revision",
        "follow_up": "Opfølgning",
        "confidence": "Evaluatorens sikkerhed",
        "sources": "Kilder",
    },
}


def _mode_label(locale: str, mode: TutorMode) -> str:
    return _MODE_LABELS[locale][mode]


__all__ = ["ChatClient", "StudyLabPage", "StudyLabWorker"]
