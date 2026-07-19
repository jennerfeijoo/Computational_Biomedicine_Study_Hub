from __future__ import annotations

import logging
import time
from pathlib import Path
from threading import Event

import pytest
from PySide6.QtCore import QSettings, Qt
from PySide6.QtWidgets import QTextBrowser

from computational_biomedicine_study_hub.academic.models import LocalizedText
from computational_biomedicine_study_hub.i18n import AppLocale
from computational_biomedicine_study_hub.integrations.ollama import (
    OllamaConnectionError,
    OllamaModel,
    OllamaTimeoutError,
)
from computational_biomedicine_study_hub.integrations.ollama_chat import (
    ChatMessage,
    ChatResponse,
    ChatRole,
)
from computational_biomedicine_study_hub.learning.academic_catalog import (
    AcademicCatalog,
    GlossaryEntry,
)
from computational_biomedicine_study_hub.persistence import SQLiteProgressRepository
from computational_biomedicine_study_hub.ui.pages.assessments_page import AssessmentsPage
from computational_biomedicine_study_hub.ui.pages.flashcards_page import (
    AdaptiveCardBrowser,
    FlashcardsPage,
)
from computational_biomedicine_study_hub.ui.pages.glossary_page import GlossaryPage
from computational_biomedicine_study_hub.ui.pages.ollama_settings_page import (
    OllamaSettingsPage,
)
from computational_biomedicine_study_hub.ui.pages.study_lab_page import StudyLabPage


def _settings(path: Path) -> QSettings:
    settings = QSettings(str(path), QSettings.Format.IniFormat)
    settings.setValue(OllamaSettingsPage.MODEL_KEY, "qwen3.6:27b")
    return settings


class FakePreflightClient:
    def __init__(
        self,
        *,
        models: tuple[str, ...] = ("qwen3.6:27b",),
        error: Exception | None = None,
        delay: float = 0.0,
    ) -> None:
        self.models = models
        self.error = error
        self.delay = delay
        self.calls: list[str] = []

    def get_version(self) -> str:
        self.calls.append("version")
        if self.delay:
            time.sleep(self.delay)
        if self.error is not None:
            raise self.error
        return "0.12.0"

    def list_models(self) -> tuple[OllamaModel, ...]:
        self.calls.append("models")
        if self.error is not None:
            raise self.error
        return tuple(OllamaModel(name) for name in self.models)


class FakeChatClient:
    def __init__(
        self,
        *,
        response: str = "Grounded response.",
        error: Exception | None = None,
        delay: float = 0.0,
    ) -> None:
        self.response = response
        self.error = error
        self.delay = delay
        self.calls: list[tuple[tuple[ChatMessage, ...], str]] = []
        self.started = Event()

    def chat(
        self,
        messages: tuple[ChatMessage, ...],
        *,
        model: str,
        temperature: float = 0.2,
        keep_alive: str = "10m",
    ) -> ChatResponse:
        del temperature, keep_alive
        self.calls.append((messages, model))
        self.started.set()
        if self.delay:
            time.sleep(self.delay)
        if self.error is not None:
            raise self.error
        return ChatResponse(model, ChatMessage(ChatRole.ASSISTANT, self.response))


def _study_page(
    qtbot,
    tmp_path: Path,
    *,
    locale: AppLocale = AppLocale.ENGLISH,
    probe: FakePreflightClient | None = None,
    chat: FakeChatClient | None = None,
) -> tuple[StudyLabPage, FakePreflightClient, FakeChatClient]:
    probe = probe or FakePreflightClient()
    chat = chat or FakeChatClient()
    page = StudyLabPage(
        AcademicCatalog(locale=locale),
        _settings(tmp_path / f"study-{locale.value}.ini"),
        client_factory=lambda _config: chat,
        preflight_client_factory=lambda _config: probe,
    )
    qtbot.addWidget(page)
    page.show()
    return page, probe, chat


def _set_grounded_question(page: StudyLabPage) -> None:
    course = page._catalog.source_catalog.courses[0]
    module = course.modules[0]
    page.question.setPlainText(module.concepts[0].title.resolve("en"))


def test_glossary_rows_are_human_text_with_internal_identity(qtbot) -> None:
    page = GlossaryPage(
        AcademicCatalog(locale=AppLocale.SPANISH_SPAIN),
        locale=AppLocale.SPANISH_SPAIN,
    )
    qtbot.addWidget(page)

    visible = [page.term_list.item(index).text() for index in range(page.term_list.count())]
    assert visible
    assert all(text.strip() and not text.startswith("·") for text in visible)
    assert not any(
        code in text for text in visible for code in ("DM857", "DM847", "BMB830", "BMB831")
    )

    first = page.term_list.item(0)
    term_id = first.data(Qt.ItemDataRole.UserRole)
    entry = next(item for item in page.entries if item.term_id == term_id)
    assert entry.course_code
    assert entry.module_id
    assert term_id not in first.text()


def test_glossary_multi_course_filter_state_and_removed_selection(qtbot) -> None:
    spanish = GlossaryPage(
        AcademicCatalog(locale=AppLocale.SPANISH_SPAIN),
        locale=AppLocale.SPANISH_SPAIN,
    )
    qtbot.addWidget(spanish)
    all_count = len(spanish.entries)

    selected = ("DM847", "BMB831")
    spanish.course_selector.set_selected_course_codes(selected)
    assert set(item.course_code for item in spanish.entries) == set(selected)
    assert set(spanish.course_selector.selected_course_codes) == set(selected)

    spanish.term_list.setCurrentRow(0)
    chosen = spanish.selected_entry
    assert chosen is not None
    other = next(code for code in selected if code != chosen.course_code)
    spanish.course_selector.set_selected_course_codes((other,))
    assert spanish.selected_entry is None
    assert not spanish.detail_empty_label.isHidden()

    spanish.course_selector.set_selected_course_codes(spanish._catalog.course_codes)
    assert len(spanish.entries) == all_count

    spanish.course_selector.set_selected_course_codes(selected)
    state = spanish.capture_state()
    english = GlossaryPage(
        AcademicCatalog(locale=AppLocale.ENGLISH),
        locale=AppLocale.ENGLISH,
    )
    qtbot.addWidget(english)
    english.restore_state(state)
    assert set(english.course_selector.selected_course_codes) == set(selected)


def test_glossary_uses_english_fallback_and_logs_invalid_entries(
    qtbot,
    caplog: pytest.LogCaptureFixture,
) -> None:
    fallback_entry = GlossaryEntry(
        term_id="term.fallback",
        term=LocalizedText({"en": "English fallback term"}).resolve("es"),
        definition=LocalizedText({"en": "English fallback definition"}).resolve("es"),
        course_code="DM857",
        module_id="dm857.m01",
        module_title="Fallback module",
        locale=AppLocale.SPANISH_SPAIN,
        tags=(),
        related_terms=(),
        synonyms=(),
    )
    assert GlossaryPage._validated_entries((fallback_entry,)) == (fallback_entry,)
    assert fallback_entry.term == "English fallback term"
    assert fallback_entry.definition == "English fallback definition"

    invalid = GlossaryEntry(
        term_id="term.invalid",
        term="",
        definition="",
        course_code="DM857",
        module_id="dm857.m01",
        module_title="Module",
        locale=AppLocale.ENGLISH,
        tags=(),
        related_terms=(),
        synonyms=(),
    )
    with caplog.at_level(logging.WARNING):
        assert GlossaryPage._validated_entries((invalid,)) == ()
    assert "course=DM857" in caplog.text
    assert "module=dm857.m01" in caplog.text
    assert "id=term.invalid" in caplog.text


def test_adaptive_card_centers_text_and_left_aligns_code(qtbot) -> None:
    browser = AdaptiveCardBrowser("adaptiveTest")
    qtbot.addWidget(browser)
    browser.resize(760, 380)
    browser.show()

    browser.set_card_content("Short, focused question?")
    short_size = browser.font_pixel_size
    assert browser.content_alignment == Qt.AlignmentFlag.AlignHCenter
    assert not browser.is_code_content

    browser.set_card_content("Long explanation " * 500)
    assert browser.font_pixel_size < short_size
    assert browser.font_pixel_size >= browser.NORMAL_MIN_PX
    assert browser.requires_vertical_scroll
    assert browser.verticalScrollBar().maximum() > 0

    browser.set_card_content("```python\nfor item in values:\n    print(item)\n```")
    assert browser.is_code_content
    assert browser.content_alignment == Qt.AlignmentFlag.AlignLeft
    assert browser.CODE_MIN_PX <= browser.font_pixel_size <= browser.CODE_MAX_PX


def test_adaptive_card_recalculates_on_resize_and_content_change(qtbot) -> None:
    browser = AdaptiveCardBrowser("adaptiveResizeTest")
    qtbot.addWidget(browser)
    browser.resize(700, 360)
    browser.show()
    browser.set_card_content("Una pregunta breve")
    initial_revision = browser.presentation_revision

    browser.resize(420, 240)
    qtbot.waitUntil(lambda: browser.presentation_revision > initial_revision)
    resized_revision = browser.presentation_revision
    browser.set_card_content("Et kort spørgsmål på dansk")
    assert browser.presentation_revision > resized_revision
    assert browser.font_pixel_size >= browser.NORMAL_MIN_PX


def test_flashcard_click_space_and_rating_state(qtbot, tmp_path: Path) -> None:
    page = FlashcardsPage(
        AcademicCatalog(locale=AppLocale.ENGLISH),
        SQLiteProgressRepository(tmp_path / "flashcards.sqlite3"),
        locale=AppLocale.ENGLISH,
    )
    qtbot.addWidget(page)
    page.resize(900, 720)
    page.show()

    assert page.current_card is not None
    assert all(not button.isEnabled() for button in page.rating_buttons)
    qtbot.mouseClick(page.front_label.viewport(), Qt.MouseButton.LeftButton)
    assert page.back_label.isVisible()
    assert all(button.isEnabled() for button in page.rating_buttons)

    page.flip()
    assert page.front_label.isVisible()
    qtbot.keyClick(page.card_frame, Qt.Key.Key_Space)
    assert page.back_label.isVisible()
    assert all(button.isEnabled() for button in page.rating_buttons)


def test_study_lab_invalid_url_never_starts_clients(qtbot, tmp_path: Path) -> None:
    probe = FakePreflightClient()
    chat = FakeChatClient()
    settings = _settings(tmp_path / "invalid-url.ini")
    settings.setValue(OllamaSettingsPage.BASE_URL_KEY, "not-a-url")
    page = StudyLabPage(
        AcademicCatalog(locale=AppLocale.ENGLISH),
        settings,
        client_factory=lambda _config: chat,
        preflight_client_factory=lambda _config: probe,
    )
    qtbot.addWidget(page)

    page.test_connection()

    assert page._thread is None
    assert "invalid" in page.status_label.text().casefold()
    assert not probe.calls
    assert not chat.calls
    assert page.send_button.isEnabled()


def test_study_lab_connection_failure_is_specific_and_recovers(qtbot, tmp_path: Path) -> None:
    page, _probe, chat = _study_page(
        qtbot,
        tmp_path,
        probe=FakePreflightClient(error=OllamaConnectionError("offline")),
    )
    page.test_connection()
    qtbot.waitUntil(lambda: page._thread is None)

    assert "not accessible" in page.status_label.text().casefold()
    assert not chat.calls
    assert page.send_button.isEnabled()
    assert page.test_connection_button.isEnabled()


def test_study_lab_missing_model_lists_detected_models_without_chat(
    qtbot,
    tmp_path: Path,
) -> None:
    page, _probe, chat = _study_page(
        qtbot,
        tmp_path,
        probe=FakePreflightClient(models=("llama3.2:latest", "qwen2.5:7b")),
    )
    page.test_connection()
    qtbot.waitUntil(lambda: page._thread is None)

    assert "not installed" in page.status_label.text().casefold()
    assert "qwen3.6:27b" in page.diagnostic_label.text()
    assert "llama3.2:latest" in page.diagnostic_label.text()
    assert not chat.calls
    assert "not verified" in page.model_label.text().casefold()


def test_study_lab_preflight_precedes_generation_and_sources_are_friendly(
    qtbot,
    tmp_path: Path,
) -> None:
    page, probe, chat = _study_page(qtbot, tmp_path)
    _set_grounded_question(page)

    page.send()
    qtbot.waitUntil(lambda: page._thread is None)

    assert probe.calls == ["version", "models"]
    assert len(chat.calls) == 1
    assert page._status_history.index("checking") < page._status_history.index("generating")
    assert page._status_history.index("model_available") < page._status_history.index("generating")
    assert "complete" in page.status_label.text().casefold()
    assert "active model" in page.model_label.text().casefold()
    assert ".m01" not in page.sources.toPlainText().casefold()
    assert page.source_details.toPlainText()
    assert not page.source_details.isVisible()


def test_study_lab_timeout_reactivates_send(qtbot, tmp_path: Path) -> None:
    page, _probe, _chat = _study_page(
        qtbot,
        tmp_path,
        chat=FakeChatClient(error=OllamaTimeoutError("too slow")),
    )
    _set_grounded_question(page)
    page.send()
    qtbot.waitUntil(lambda: page._thread is None)

    assert "time limit" in page.status_label.text().casefold()
    assert page.send_button.isEnabled()
    assert not page.cancel_button.isEnabled()


def test_study_lab_cancel_discards_late_response(qtbot, tmp_path: Path) -> None:
    chat = FakeChatClient(response="This must not be published.", delay=0.15)
    page, _probe, _chat = _study_page(qtbot, tmp_path, chat=chat)
    _set_grounded_question(page)
    page.send()
    qtbot.waitUntil(chat.started.is_set)
    page.cancel()
    qtbot.waitUntil(lambda: page._thread is None)

    assert "cancelled" in page.status_label.text().casefold()
    assert "This must not be published." not in page.history.toPlainText()
    assert page.send_button.isEnabled()


@pytest.mark.parametrize(
    ("locale", "speaker", "fallback"),
    (
        (
            AppLocale.SPANISH_SPAIN,
            "Laboratorio de estudio",
            "Las funciones de estudio estáticas siguen funcionando.",
        ),
        (
            AppLocale.DANISH_DENMARK,
            "Studielaboratorium",
            "statiske studiefunktioner",
        ),
    ),
)
def test_study_lab_failure_copy_follows_interface_language(
    qtbot,
    tmp_path: Path,
    locale: AppLocale,
    speaker: str,
    fallback: str,
) -> None:
    page, _probe, _chat = _study_page(
        qtbot,
        tmp_path,
        locale=locale,
        probe=FakePreflightClient(error=OllamaConnectionError("offline")),
    )
    page.test_connection()
    qtbot.waitUntil(lambda: page._thread is None)

    history = page.history.toPlainText()
    assert speaker in history
    assert fallback.casefold() in history.casefold()
    assert "The local model is unavailable" not in history


def test_study_lab_probe_is_non_blocking_and_sends_no_prompt(qtbot, tmp_path: Path) -> None:
    page, probe, chat = _study_page(
        qtbot,
        tmp_path,
        probe=FakePreflightClient(delay=0.15),
    )
    started = time.perf_counter()
    page.test_connection()
    elapsed = time.perf_counter() - started

    assert elapsed < 0.1
    assert page._thread is not None
    qtbot.waitUntil(lambda: page._thread is None)
    assert probe.calls == ["version", "models"]
    assert not chat.calls
    assert "available" in page.status_label.text().casefold()


def test_study_lab_open_settings_is_explicit(qtbot, tmp_path: Path) -> None:
    page, _probe, _chat = _study_page(qtbot, tmp_path)
    with qtbot.waitSignal(page.settings_requested):
        page.open_settings_button.click()


@pytest.mark.parametrize("course_code", ("BMB830", "DM847", "BMB831"))
def test_each_cumulative_assessment_is_a_semantic_learner_document(
    qtbot,
    tmp_path: Path,
    course_code: str,
) -> None:
    page = AssessmentsPage(
        AcademicCatalog(locale=AppLocale.SPANISH_SPAIN),
        SQLiteProgressRepository(tmp_path / f"{course_code}.sqlite3"),
        locale=AppLocale.SPANISH_SPAIN,
    )
    qtbot.addWidget(page)

    assert page.show_cumulative_assessment(course_code)
    browser = page.findChild(QTextBrowser, "cumulativeAssessmentContent")
    assert browser is not None
    text = browser.toPlainText()
    for heading in (
        "Propósito",
        "Competencias evaluadas",
        "Componentes obligatorios",
        "Líneas de proyecto",
        "Estructura recomendada",
        "Rúbrica",
        "Preguntas de defensa",
        "Checklist",
    ):
        assert heading in text
    assert "Metadata" not in text
    assert "Covered modules" not in text
    assert f"{course_code.casefold()}.m01" not in text.casefold()
    assert "hidden_examiner_support" not in text
    assert "expected_elements" not in text


def test_cumulative_renderer_excludes_examiner_guidance(qtbot, tmp_path: Path) -> None:
    page = AssessmentsPage(
        AcademicCatalog(locale=AppLocale.ENGLISH),
        SQLiteProgressRepository(tmp_path / "hidden.sqlite3"),
        locale=AppLocale.ENGLISH,
    )
    qtbot.addWidget(page)
    assert page.show_cumulative_assessment("DM847")
    browser = page.findChild(QTextBrowser, "cumulativeAssessmentContent")
    assert browser is not None
    text = browser.toPlainText()
    assert "What assumption makes that algorithm valid?" not in text
    assert "expected elements" not in text.casefold()
