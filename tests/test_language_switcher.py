from __future__ import annotations

from PySide6.QtCore import QSettings
from PySide6.QtWidgets import QApplication, QPushButton, QStackedWidget, QTabWidget

from computational_biomedicine_study_hub.courses.dm857 import DM857Page
from computational_biomedicine_study_hub.i18n import AppLocale, validate_ui_copy
from computational_biomedicine_study_hub.ui.main_window import MainWindow


def _settings(tmp_path: object) -> QSettings:
    path = getattr(tmp_path, "__truediv__")("language.ini")
    return QSettings(str(path), QSettings.Format.IniFormat)


def _language_button(window: MainWindow, label: str) -> QPushButton:
    for button in window.findChildren(QPushButton, "languageButton"):
        if button.text() == label:
            return button
    raise AssertionError(f"Missing language button {label!r}")


def _active_dm857_page(window: MainWindow) -> DM857Page:
    stack = window.findChild(QStackedWidget)
    assert stack is not None
    page = stack.currentWidget()
    assert isinstance(page, DM857Page)
    return page


def test_ui_copy_is_complete_for_all_three_languages() -> None:
    validate_ui_copy()


def test_header_exposes_exact_dk_es_en_buttons(
    qapp: QApplication,
    tmp_path: object,
) -> None:
    window = MainWindow(settings=_settings(tmp_path))
    buttons = window.findChildren(QPushButton, "languageButton")

    assert [button.text() for button in buttons] == ["DK", "ES", "EN"]
    assert _language_button(window, "ES").isChecked()


def test_language_change_is_immediate_and_preserves_dm857_location(
    qapp: QApplication,
    tmp_path: object,
) -> None:
    settings = _settings(tmp_path)
    window = MainWindow(settings=settings)
    window.navigate("course/dm857")
    page = _active_dm857_page(window)
    assert page.select_module(4)
    assert page.reader.select_section_index(2)

    _language_button(window, "EN").click()
    qapp.processEvents()

    assert window.current_locale is AppLocale.ENGLISH
    assert str(window.current_route) == "course/dm857"
    translated_page = _active_dm857_page(window)
    assert translated_page.current_module_index == 4
    assert translated_page.reader.current_section_index == 2
    assert translated_page.reader.module.title.startswith("Strings")
    tabs = translated_page.reader.findChild(QTabWidget, "moduleTabs")
    assert tabs is not None
    assert [tabs.tabText(index) for index in range(tabs.count())] == [
        "Overview",
        "Concepts",
        "Examples",
        "Practice",
        "Assessment",
    ]
    assert settings.value("ui/locale") == "en"


def test_persisted_danish_locale_is_restored(
    qapp: QApplication,
    tmp_path: object,
) -> None:
    settings = _settings(tmp_path)
    first = MainWindow(settings=settings)
    _language_button(first, "DK").click()
    qapp.processEvents()
    first.close()

    second = MainWindow(settings=settings)

    assert second.current_locale is AppLocale.DANISH_DENMARK
    assert _language_button(second, "DK").isChecked()
