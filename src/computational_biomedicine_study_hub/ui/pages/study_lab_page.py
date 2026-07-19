"""Grounded local-Qwen study laboratory."""

from __future__ import annotations

import json
import logging
from collections.abc import Callable
from dataclasses import dataclass
from enum import StrEnum
from html import escape
from time import perf_counter
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

from ...academic.retrieval import AcademicFragment, FragmentVisibility, LexicalRetriever
from ...academic.tutor import GroundedTutorRequest, TutorContextBuilder, TutorMode
from ...academic.tutor.context_builder import INSUFFICIENT_EVIDENCE
from ...academic.tutor.evaluation import FeedbackParseError, parse_open_response_feedback
from ...academic.tutor.response_models import OpenResponseFeedback
from ...courses import COURSES
from ...integrations.ollama import (
    OllamaClient,
    OllamaConfig,
    OllamaConfigurationError,
    OllamaConnectionError,
    OllamaModel,
    OllamaProtocolError,
    OllamaTimeoutError,
)
from ...integrations.ollama_chat import (
    DEFAULT_CHAT_MODEL,
    ChatMessage,
    ChatResponse,
    ChatRole,
    OllamaChatClient,
)
from ...learning.academic_catalog import AcademicCatalog
from ..pages.ollama_settings_page import OllamaSettingsPage

LOGGER = logging.getLogger(__name__)


class ChatClient(Protocol):
    def chat(
        self,
        messages: tuple[ChatMessage, ...],
        *,
        model: str,
        temperature: float = 0.2,
        keep_alive: str = "10m",
    ) -> ChatResponse: ...


class PreflightClient(Protocol):
    def get_version(self) -> str: ...

    def list_models(self) -> tuple[OllamaModel, ...]: ...


class StudyLabFailureKind(StrEnum):
    INVALID_URL = "invalid_url"
    CONNECTION = "connection"
    MODEL_MISSING = "model_missing"
    TIMEOUT = "timeout"
    EMPTY_RESPONSE = "empty_response"
    INVALID_RESPONSE = "invalid_response"


@dataclass(frozen=True, slots=True)
class StudyLabPreflight:
    version: str
    requested_model: str
    model_names: tuple[str, ...]
    duration_seconds: float


@dataclass(frozen=True, slots=True)
class StudyLabFailure:
    kind: StudyLabFailureKind
    detail: str = ""
    requested_model: str = ""
    model_names: tuple[str, ...] = ()


class StudyLabWorker(QObject):
    progress = Signal(str)
    preflight_succeeded = Signal(object)
    finished = Signal(object)
    failed = Signal(object)
    cancelled = Signal()

    def __init__(
        self,
        client: ChatClient,
        messages: tuple[ChatMessage, ...],
        model: str,
        *,
        preflight_client: PreflightClient | None = None,
        preflight_only: bool = False,
        normalized_base_url: str = "",
        preflight_timeout: float = 5.0,
        generation_timeout: float = 180.0,
    ) -> None:
        super().__init__()
        self._client = client
        self._preflight_client = preflight_client
        self._messages = messages
        self._model = model
        self._preflight_only = preflight_only
        self._normalized_base_url = normalized_base_url
        self._preflight_timeout = preflight_timeout
        self._generation_timeout = generation_timeout
        self._cancelled = False

    @Slot()
    def run(self) -> None:
        if self._cancelled:
            self.cancelled.emit()
            return

        if self._preflight_client is not None:
            self.progress.emit("checking")
            preflight_started = perf_counter()
            try:
                version = self._preflight_client.get_version()
                models = self._preflight_client.list_models()
            except Exception as error:
                self._emit_failure(error, phase="preflight", started=preflight_started)
                return

            duration = perf_counter() - preflight_started
            model_names = tuple(model.name for model in models)
            LOGGER.info(
                "Ollama preflight completed url=%s requested_model=%s models=%s "
                "duration_seconds=%.3f timeout_seconds=%s",
                self._normalized_base_url,
                self._model,
                model_names,
                duration,
                self._preflight_timeout,
            )
            if self._cancelled:
                self.cancelled.emit()
                return
            if self._model not in model_names:
                self.failed.emit(
                    StudyLabFailure(
                        StudyLabFailureKind.MODEL_MISSING,
                        requested_model=self._model,
                        model_names=model_names,
                    )
                )
                return

            preflight = StudyLabPreflight(version, self._model, model_names, duration)
            self.progress.emit("connected")
            self.preflight_succeeded.emit(preflight)
            self.progress.emit("model_available")
            if self._preflight_only:
                self.finished.emit(preflight)
                return

        if self._cancelled:
            self.cancelled.emit()
            return
        self.progress.emit("generating")
        generation_started = perf_counter()
        try:
            response = self._client.chat(self._messages, model=self._model)
        except Exception as error:
            self._emit_failure(error, phase="generation", started=generation_started)
            return
        LOGGER.info(
            "Ollama generation completed url=%s requested_model=%s "
            "duration_seconds=%.3f timeout_seconds=%s",
            self._normalized_base_url,
            self._model,
            perf_counter() - generation_started,
            self._generation_timeout,
        )
        if self._cancelled:
            self.cancelled.emit()
        else:
            self.finished.emit(response)

    @Slot()
    def cancel(self) -> None:
        self._cancelled = True

    def _emit_failure(self, error: Exception, *, phase: str, started: float) -> None:
        if self._cancelled:
            self.cancelled.emit()
            return
        if isinstance(error, OllamaConfigurationError):
            kind = StudyLabFailureKind.INVALID_URL
        elif isinstance(error, (OllamaTimeoutError, TimeoutError)):
            kind = StudyLabFailureKind.TIMEOUT
        elif isinstance(error, OllamaConnectionError):
            kind = StudyLabFailureKind.CONNECTION
        elif isinstance(error, OllamaProtocolError) and "empty" in str(error).casefold():
            kind = StudyLabFailureKind.EMPTY_RESPONSE
        else:
            kind = StudyLabFailureKind.INVALID_RESPONSE
        duration = perf_counter() - started
        LOGGER.warning(
            "Ollama request failed url=%s requested_model=%s phase=%s failure_type=%s "
            "duration_seconds=%.3f preflight_timeout_seconds=%s "
            "generation_timeout_seconds=%s",
            self._normalized_base_url,
            self._model,
            phase,
            kind.value,
            duration,
            self._preflight_timeout,
            self._generation_timeout,
        )
        self.failed.emit(StudyLabFailure(kind, detail=str(error)))


def _locale_code(value: str) -> str:
    normalized = value.casefold()
    if normalized.startswith("es"):
        return "es"
    if normalized.startswith("da"):
        return "da"
    return "en"


class StudyLabPage(QWidget):
    """Mode-driven study tool; Ollama is transport, never the source of truth."""

    settings_requested = Signal()

    def __init__(
        self,
        catalog: AcademicCatalog,
        settings: QSettings,
        *,
        client_factory: Callable[[OllamaConfig], ChatClient] | None = None,
        preflight_client_factory: Callable[[OllamaConfig], PreflightClient] | None = None,
        parent: QWidget | None = None,
    ) -> None:
        super().__init__(parent)
        self.setObjectName("studyLabPage")
        self._catalog = catalog
        self._settings = settings
        self._client_factory = client_factory or (lambda config: OllamaChatClient(config))
        self._preflight_client_factory = preflight_client_factory or OllamaClient
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
        self._source_ids: tuple[str, ...] = ()
        self._status_history: list[str] = []

        root = QVBoxLayout(self)
        root.setContentsMargins(0, 0, 0, 0)
        root.setSpacing(12)
        form = QFormLayout()
        self.course_selector = QComboBox()
        for course_code in catalog.course_codes:
            self.course_selector.addItem(self._course_title(course_code), course_code)
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
        self.model_label = QLabel(copy["model_unverified"])
        self.model_label.setObjectName("studyLabModel")
        self.model_label.setProperty("modelVerified", False)
        self.test_connection_button = QPushButton(copy["test_connection"])
        self.test_connection_button.setObjectName("secondaryActionButton")
        self.open_settings_button = QPushButton(copy["open_settings"])
        self.open_settings_button.setObjectName("secondaryActionButton")
        status_row.addWidget(self.status_label)
        status_row.addStretch(1)
        status_row.addWidget(self.model_label)
        status_row.addWidget(self.test_connection_button)
        status_row.addWidget(self.open_settings_button)
        root.addLayout(status_row)

        self.diagnostic_label = QLabel()
        self.diagnostic_label.setObjectName("studyLabDiagnostic")
        self.diagnostic_label.setWordWrap(True)
        self.diagnostic_label.hide()
        root.addWidget(self.diagnostic_label)

        self.history = QTextBrowser()
        self.history.setObjectName("studyLabHistory")
        self.history.setAccessibleName(copy["history"])
        root.addWidget(self.history, 1)

        self.sources = QTextBrowser()
        self.sources.setObjectName("studyLabSources")
        self.sources.setMaximumHeight(110)
        self.sources.setPlaceholderText(copy["sources"])
        root.addWidget(self.sources)

        self.source_details_button = QPushButton(copy["source_details"])
        self.source_details_button.setObjectName("studyLabSourceDetailsButton")
        self.source_details_button.setCheckable(True)
        self.source_details_button.setVisible(False)
        root.addWidget(self.source_details_button)
        self.source_details = QTextBrowser()
        self.source_details.setObjectName("studyLabTechnicalSources")
        self.source_details.setMaximumHeight(90)
        self.source_details.setVisible(False)
        root.addWidget(self.source_details)

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
        self.test_connection_button.clicked.connect(self.test_connection)
        self.open_settings_button.clicked.connect(self.settings_requested.emit)
        self.source_details_button.toggled.connect(self.source_details.setVisible)
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
        copy = _LAB_COPY[self._locale_code]
        self.history.append(f"<b>{copy['you']}</b><br>{escape(question)}")
        if context is None:
            answer = INSUFFICIENT_EVIDENCE[request.locale]
            self.history.append(f"<b>{copy['lab']}</b><br>{escape(answer)}")
            self._set_status("insufficient")
            return
        visible_sources = tuple(
            item
            for item in context.sources
            if item.fragment.visibility is FragmentVisibility.VISIBLE
        )
        self._source_ids = tuple(item.fragment.source_id for item in visible_sources)
        self.sources.setPlainText(
            "\n".join(f"• {self._friendly_source(item.fragment)}" for item in visible_sources)
        )
        self.source_details.setPlainText("\n".join(self._source_ids))
        self.source_details_button.setVisible(bool(self._source_ids))
        self.source_details_button.setChecked(False)
        messages = (
            ChatMessage(ChatRole.SYSTEM, context.system_prompt),
            ChatMessage(ChatRole.USER, context.user_prompt),
        )
        self._start_operation(messages, preflight_only=False)

    @Slot()
    def test_connection(self) -> None:
        """Check server, installed models, and selected model without sending a prompt."""
        if self._thread is not None:
            return
        self._start_operation((), preflight_only=True)

    def _start_operation(
        self,
        messages: tuple[ChatMessage, ...],
        *,
        preflight_only: bool,
    ) -> None:
        raw_config = OllamaConfig(base_url=self._selected_base_url())
        try:
            normalized_url = raw_config.normalized_base_url()
        except OllamaConfigurationError as error:
            self._fail(
                StudyLabFailure(
                    StudyLabFailureKind.INVALID_URL,
                    detail=str(error),
                )
            )
            return

        config = OllamaConfig(
            base_url=normalized_url,
            timeout_seconds=raw_config.timeout_seconds,
            generation_timeout_seconds=raw_config.generation_timeout_seconds,
        )
        model = self._selected_model()
        worker = StudyLabWorker(
            self._client_factory(config),
            messages,
            model,
            preflight_client=self._preflight_client_factory(config),
            preflight_only=preflight_only,
            normalized_base_url=normalized_url,
            preflight_timeout=config.timeout_seconds,
            generation_timeout=config.generation_timeout_seconds,
        )
        thread = QThread(self)
        worker.moveToThread(thread)
        thread.started.connect(worker.run)
        worker.progress.connect(self._progress)
        worker.preflight_succeeded.connect(self._preflight_succeeded)
        worker.finished.connect(self._operation_complete)
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
        self.test_connection_button.setEnabled(False)
        self.model_label.setText(_LAB_COPY[self._locale_code]["model_unverified"])
        self.diagnostic_label.hide()
        self._progress("checking")
        thread.start()

    @Slot()
    def cancel(self) -> None:
        if self._worker is not None:
            self._worker.cancel()
            self._set_status("cancelling")
            self.cancel_button.setEnabled(False)

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
            self.source_details.clear()
            self.source_details_button.setVisible(False)
            self.question.clear()
            self._last_answer = ""
            self._source_ids = ()

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
                "source_ids": self._source_ids,
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
                "source_ids": self._source_ids,
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
        if state in _LAB_COPY[self._locale_code]:
            self._set_status(state)

    @Slot(object)
    def _preflight_succeeded(self, value: object) -> None:
        if not isinstance(value, StudyLabPreflight):
            return
        copy = _LAB_COPY[self._locale_code]
        self.model_label.setText(f"{copy['model_verified']}: {value.requested_model}")
        self.model_label.setProperty("modelVerified", True)
        self.model_label.style().unpolish(self.model_label)
        self.model_label.style().polish(self.model_label)
        self.diagnostic_label.setText(
            copy["preflight_details"].format(
                version=value.version,
                count=len(value.model_names),
            )
        )
        self.diagnostic_label.show()

    @Slot(object)
    def _operation_complete(self, value: object) -> None:
        if isinstance(value, StudyLabPreflight):
            self._set_status("model_available")
            return
        self._complete(value)

    @Slot(object)
    def _complete(self, value: object) -> None:
        if not isinstance(value, ChatResponse):
            self._fail(StudyLabFailure(StudyLabFailureKind.INVALID_RESPONSE))
            return
        copy = _LAB_COPY[self._locale_code]
        self._last_answer = value.content
        if self._active_mode is TutorMode.EVALUATE_OPEN:
            try:
                feedback = parse_open_response_feedback(value.content)
            except (FeedbackParseError, ValueError) as error:
                self.status_label.setText(
                    f"{_LAB_COPY[self._locale_code]['invalid_feedback']}: {error}"
                )
                self.history.append(f"<b>{copy['lab']}</b><br>{copy['invalid_feedback_message']}")
                return
            self.history.append(
                _feedback_html(
                    feedback,
                    self._catalog.locale.value,
                    speaker=copy["lab"],
                )
            )
        else:
            self.history.append(f"<b>{copy['lab']}</b><br>{escape(value.content)}")
        self.model_label.setText(f"{copy['model_verified']}: {value.model}")
        self._set_status("complete")

    @Slot(object)
    def _fail(self, value: object) -> None:
        failure = (
            value
            if isinstance(value, StudyLabFailure)
            else StudyLabFailure(StudyLabFailureKind.INVALID_RESPONSE, detail=str(value))
        )
        copy = _LAB_COPY[self._locale_code]
        self._set_status(f"error_{failure.kind.value}")
        self.model_label.setText(copy["model_unverified"])
        self.model_label.setProperty("modelVerified", False)
        self.model_label.style().unpolish(self.model_label)
        self.model_label.style().polish(self.model_label)
        if failure.kind is StudyLabFailureKind.MODEL_MISSING:
            detected = ", ".join(failure.model_names) or copy["none_detected"]
            self.diagnostic_label.setText(
                copy["missing_model_details"].format(
                    requested=failure.requested_model,
                    detected=detected,
                )
            )
        else:
            self.diagnostic_label.clear()
        self.diagnostic_label.setVisible(bool(self.diagnostic_label.text()))
        self.history.append(f"<b>{copy['lab']}</b><br>{copy['fallback']}")

    @Slot()
    def _cancelled(self) -> None:
        self._set_status("cancelled")

    @Slot()
    def _thread_finished(self) -> None:
        self._thread = None
        self._worker = None
        self.send_button.setEnabled(True)
        self.cancel_button.setEnabled(False)
        self.test_connection_button.setEnabled(True)

    def _selected_base_url(self) -> str:
        return str(
            self._settings.value(
                OllamaSettingsPage.BASE_URL_KEY,
                OllamaConfig().normalized_base_url(),
            )
        ).strip()

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

    def _set_status(self, key: str) -> None:
        text = _LAB_COPY[self._locale_code][key]
        self.status_label.setText(text)
        self.status_label.setProperty("labState", key)
        self.status_label.style().unpolish(self.status_label)
        self.status_label.style().polish(self.status_label)
        self._status_history.append(key)

    def _course_title(self, course_code: str) -> str:
        course = next(
            (item for item in COURSES if item.code.casefold() == course_code.casefold()),
            None,
        )
        return course.title_for(self._catalog.locale) if course is not None else course_code

    def _friendly_source(self, fragment: AcademicFragment) -> str:
        copy = _LAB_COPY[self._locale_code]
        module = next(
            (
                item
                for item in self._catalog.modules(fragment.course_id)
                if item.module_id == fragment.module_id
            ),
            None,
        )
        module_suffix = fragment.module_id.rsplit(".", 1)[-1].casefold().removeprefix("m")
        try:
            module_number = str(int(module_suffix))
        except ValueError:
            module_number = ""
        module_label = (
            copy["module_number"].format(number=module_number) if module_number else copy["module"]
        )
        if module is not None and module.title.strip():
            module_label = f"{module_label}: {module.title}"
        kind = _SOURCE_KIND_LABELS[self._locale_code].get(fragment.kind, copy["source"])
        normalized_text = " ".join(fragment.text.split())
        summary = normalized_text[:88].rstrip()
        if len(normalized_text) > len(summary):
            summary = f"{summary}…"
        return f"{self._course_title(fragment.course_id)} — {module_label}\n{kind}: {summary}"

    def _stored_list(self, key: str) -> list[dict[str, object]]:
        raw = str(self._settings.value(key, "[]"))
        try:
            value = json.loads(raw)
        except json.JSONDecodeError:
            return []
        return [item for item in value if isinstance(item, dict)] if isinstance(value, list) else []


def _feedback_html(
    feedback: OpenResponseFeedback,
    locale: str,
    *,
    speaker: str = "Study Lab",
) -> str:
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
        f"<b>{escape(speaker)}</b><br><i>{escape(disclaimer)}</i>"
        f"<p>{escape(feedback.summary)}</p>"
        f"{listing(headings['strengths'], feedback.strengths)}"
        f"{listing(headings['missing'], feedback.missing_concepts)}"
        f"{listing(headings['misconceptions'], feedback.misconceptions)}"
        f"{listing(headings['unsupported'], feedback.unsupported_claims)}"
        f"<h4>{headings['rubric']}</h4><ul>{dimensions}</ul>"
        f"<h4>{headings['revision']}</h4><p>{escape(feedback.suggested_revision)}</p>"
        f"<h4>{headings['follow_up']}</h4><p>{escape(feedback.follow_up_question)}</p>"
        f"<p><b>{headings['confidence']}:</b> {escape(feedback.evaluator_confidence)}</p>"
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
        "checking": "Comprobando Ollama…",
        "connected": "Ollama conectado.",
        "model_available": "Modelo disponible.",
        "generating": "Generando respuesta…",
        "model_unverified": "Modelo no verificado",
        "model_verified": "Modelo activo",
        "preflight_details": "Ollama {version}; {count} modelos detectados.",
        "missing_model_details": ("Modelo solicitado: {requested}\nModelos detectados: {detected}"),
        "none_detected": "ninguno",
        "test_connection": "Probar conexión",
        "open_settings": "Abrir configuración",
        "history": "Historial de conversación de estudio",
        "sources": "Fuentes académicas utilizadas",
        "source": "Fuente",
        "source_details": "Detalles de fuente",
        "module_number": "Módulo {number}",
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
        "invalid_feedback_message": (
            "El modelo local devolvió una estructura de retroalimentación no válida. "
            "La respuesta no se trató como evaluación."
        ),
        "complete": "Ollama: completado",
        "error_connection": "Servicio de Ollama no accesible.",
        "error_invalid_url": "URL de Ollama no válida.",
        "error_model_missing": "El modelo seleccionado no está instalado.",
        "error_timeout": "La solicitud superó el tiempo máximo.",
        "error_empty_response": "Ollama devolvió una respuesta vacía.",
        "error_invalid_response": "Ollama devolvió una respuesta inválida.",
        "cancelled": "Solicitud cancelada.",
        "fallback": (
            "El modelo local no está disponible. Las funciones de estudio estáticas "
            "siguen funcionando."
        ),
        "you": "Tú",
        "lab": "Laboratorio de estudio",
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
        "checking": "Checking Ollama…",
        "connected": "Ollama connected.",
        "model_available": "Model available.",
        "generating": "Generating response…",
        "model_unverified": "Model not verified",
        "model_verified": "Active model",
        "preflight_details": "Ollama {version}; {count} models detected.",
        "missing_model_details": ("Requested model: {requested}\nDetected models: {detected}"),
        "none_detected": "none",
        "test_connection": "Test connection",
        "open_settings": "Open settings",
        "history": "Study conversation history",
        "sources": "Academic sources used",
        "source": "Source",
        "source_details": "Source details",
        "module_number": "Module {number}",
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
        "invalid_feedback_message": (
            "The local model returned an invalid feedback structure. "
            "The response was not treated as an evaluation."
        ),
        "complete": "Ollama: complete",
        "error_connection": "The Ollama service is not accessible.",
        "error_invalid_url": "The Ollama URL is invalid.",
        "error_model_missing": "The selected model is not installed.",
        "error_timeout": "The request exceeded its time limit.",
        "error_empty_response": "Ollama returned an empty response.",
        "error_invalid_response": "Ollama returned an invalid response.",
        "cancelled": "Request cancelled.",
        "fallback": ("The local model is unavailable. All static study features remain usable."),
        "you": "You",
        "lab": "Study Lab",
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
        "checking": "Kontrollerer Ollama…",
        "connected": "Ollama er forbundet.",
        "model_available": "Modellen er tilgængelig.",
        "generating": "Genererer svar…",
        "model_unverified": "Model ikke bekræftet",
        "model_verified": "Aktiv model",
        "preflight_details": "Ollama {version}; {count} modeller fundet.",
        "missing_model_details": ("Anmodet model: {requested}\nFundne modeller: {detected}"),
        "none_detected": "ingen",
        "test_connection": "Test forbindelse",
        "open_settings": "Åbn indstillinger",
        "history": "Studiesamtalens historik",
        "sources": "Anvendte faglige kilder",
        "source": "Kilde",
        "source_details": "Kildedetaljer",
        "module_number": "Modul {number}",
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
        "invalid_feedback_message": (
            "Den lokale model returnerede en ugyldig feedbackstruktur. "
            "Svaret blev ikke behandlet som en evaluering."
        ),
        "complete": "Ollama: færdig",
        "error_connection": "Ollama-tjenesten kan ikke nås.",
        "error_invalid_url": "Ollama-URL'en er ugyldig.",
        "error_model_missing": "Den valgte model er ikke installeret.",
        "error_timeout": "Anmodningen overskred tidsgrænsen.",
        "error_empty_response": "Ollama returnerede et tomt svar.",
        "error_invalid_response": "Ollama returnerede et ugyldigt svar.",
        "cancelled": "Anmodningen blev annulleret.",
        "fallback": (
            "Den lokale model er ikke tilgængelig. Alle statiske "
            "studiefunktioner kan fortsat bruges."
        ),
        "you": "Du",
        "lab": "Studielaboratorium",
    },
}

_SOURCE_KIND_LABELS = {
    "es": {
        "Concept": "Concepto",
        "Key point": "Punto clave",
        "Worked example": "Ejemplo resuelto",
        "Example explanation": "Explicación del ejemplo",
        "Practice": "Práctica",
        "Objective question": "Pregunta objetiva",
        "Open question": "Pregunta abierta",
        "Flashcard": "Tarjeta",
        "Glossary": "Glosario",
    },
    "en": {
        "Concept": "Concept",
        "Key point": "Key point",
        "Worked example": "Worked example",
        "Example explanation": "Example explanation",
        "Practice": "Practice",
        "Objective question": "Objective question",
        "Open question": "Open question",
        "Flashcard": "Flashcard",
        "Glossary": "Glossary",
    },
    "da": {
        "Concept": "Begreb",
        "Key point": "Nøglepunkt",
        "Worked example": "Gennemarbejdet eksempel",
        "Example explanation": "Eksempelforklaring",
        "Practice": "Øvelse",
        "Objective question": "Objektivt spørgsmål",
        "Open question": "Åbent spørgsmål",
        "Flashcard": "Huskekort",
        "Glossary": "Ordliste",
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


__all__ = [
    "ChatClient",
    "PreflightClient",
    "StudyLabFailure",
    "StudyLabFailureKind",
    "StudyLabPage",
    "StudyLabPreflight",
    "StudyLabWorker",
]
