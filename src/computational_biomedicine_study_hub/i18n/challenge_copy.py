"""Strict localized copy for starter-code test challenges."""

from __future__ import annotations

from enum import StrEnum
from string import Formatter

from .locales import AppLocale


class ChallengeCopyKey(StrEnum):
    """Stable text keys used by starter-code challenge widgets."""

    TITLE = "challenge.title"
    INTRO = "challenge.intro"
    RUN = "challenge.run"
    RESET = "challenge.reset"
    RUNNING = "challenge.running"
    SOURCE_REQUIRED = "challenge.source_required"
    VISIBLE_TESTS = "challenge.visible_tests"
    HIDDEN_SUMMARY = "challenge.hidden_summary"
    STATUS_ALL_PASSED = "challenge.status.all_passed"
    STATUS_INCOMPLETE = "challenge.status.incomplete"
    STATUS_WITH_DURATION = "challenge.status.with_duration"
    CASE_PASSED = "challenge.case.passed"
    CASE_FAILED = "challenge.case.failed"
    CASE_ERROR = "challenge.case.error"
    CASE_TIMED_OUT = "challenge.case.timed_out"
    CASE_REJECTED = "challenge.case.rejected"
    CASE_OUTPUT_LIMIT = "challenge.case.output_limit"


_CATALOGS: dict[AppLocale, dict[ChallengeCopyKey, str]] = {
    AppLocale.SPANISH_SPAIN: {
        ChallengeCopyKey.TITLE: "Reto de programación",
        ChallengeCopyKey.INTRO: (
            "Completa el código y ejecútalo contra pruebas visibles y ocultas. Las pruebas ocultas "
            "comprueban el contrato sin revelar sus entradas."
        ),
        ChallengeCopyKey.RUN: "Ejecutar pruebas",
        ChallengeCopyKey.RESET: "Restablecer código",
        ChallengeCopyKey.RUNNING: "Ejecutando pruebas…",
        ChallengeCopyKey.SOURCE_REQUIRED: "Escribe una solución antes de ejecutar las pruebas.",
        ChallengeCopyKey.VISIBLE_TESTS: "Pruebas visibles",
        ChallengeCopyKey.HIDDEN_SUMMARY: "Pruebas ocultas superadas: {passed}/{total}",
        ChallengeCopyKey.STATUS_ALL_PASSED: "Todas las pruebas fueron superadas",
        ChallengeCopyKey.STATUS_INCOMPLETE: "La solución todavía no satisface todo el contrato",
        ChallengeCopyKey.STATUS_WITH_DURATION: "{status} · {duration} ms",
        ChallengeCopyKey.CASE_PASSED: "Superada",
        ChallengeCopyKey.CASE_FAILED: "Resultado incorrecto",
        ChallengeCopyKey.CASE_ERROR: "Error de ejecución",
        ChallengeCopyKey.CASE_TIMED_OUT: "Tiempo agotado",
        ChallengeCopyKey.CASE_REJECTED: "Código rechazado",
        ChallengeCopyKey.CASE_OUTPUT_LIMIT: "Salida excesiva",
    },
    AppLocale.ENGLISH: {
        ChallengeCopyKey.TITLE: "Programming challenge",
        ChallengeCopyKey.INTRO: (
            "Complete the code and run it against visible and hidden tests. Hidden tests verify the "
            "contract without revealing their inputs."
        ),
        ChallengeCopyKey.RUN: "Run tests",
        ChallengeCopyKey.RESET: "Reset code",
        ChallengeCopyKey.RUNNING: "Running tests…",
        ChallengeCopyKey.SOURCE_REQUIRED: "Write a solution before running the tests.",
        ChallengeCopyKey.VISIBLE_TESTS: "Visible tests",
        ChallengeCopyKey.HIDDEN_SUMMARY: "Hidden tests passed: {passed}/{total}",
        ChallengeCopyKey.STATUS_ALL_PASSED: "All tests passed",
        ChallengeCopyKey.STATUS_INCOMPLETE: "The solution does not yet satisfy the full contract",
        ChallengeCopyKey.STATUS_WITH_DURATION: "{status} · {duration} ms",
        ChallengeCopyKey.CASE_PASSED: "Passed",
        ChallengeCopyKey.CASE_FAILED: "Incorrect result",
        ChallengeCopyKey.CASE_ERROR: "Runtime error",
        ChallengeCopyKey.CASE_TIMED_OUT: "Timed out",
        ChallengeCopyKey.CASE_REJECTED: "Code rejected",
        ChallengeCopyKey.CASE_OUTPUT_LIMIT: "Excessive output",
    },
    AppLocale.DANISH_DENMARK: {
        ChallengeCopyKey.TITLE: "Programmeringsudfordring",
        ChallengeCopyKey.INTRO: (
            "Færdiggør koden og kør den mod synlige og skjulte test. Skjulte test kontrollerer "
            "kontrakten uden at afsløre deres input."
        ),
        ChallengeCopyKey.RUN: "Kør test",
        ChallengeCopyKey.RESET: "Nulstil kode",
        ChallengeCopyKey.RUNNING: "Kører test…",
        ChallengeCopyKey.SOURCE_REQUIRED: "Skriv en løsning, før du kører testene.",
        ChallengeCopyKey.VISIBLE_TESTS: "Synlige test",
        ChallengeCopyKey.HIDDEN_SUMMARY: "Beståede skjulte test: {passed}/{total}",
        ChallengeCopyKey.STATUS_ALL_PASSED: "Alle test er bestået",
        ChallengeCopyKey.STATUS_INCOMPLETE: "Løsningen opfylder endnu ikke hele kontrakten",
        ChallengeCopyKey.STATUS_WITH_DURATION: "{status} · {duration} ms",
        ChallengeCopyKey.CASE_PASSED: "Bestået",
        ChallengeCopyKey.CASE_FAILED: "Forkert resultat",
        ChallengeCopyKey.CASE_ERROR: "Kørselsfejl",
        ChallengeCopyKey.CASE_TIMED_OUT: "Tiden udløb",
        ChallengeCopyKey.CASE_REJECTED: "Kode afvist",
        ChallengeCopyKey.CASE_OUTPUT_LIMIT: "For stort output",
    },
}


def challenge_text(
    locale: AppLocale | str,
    key: ChallengeCopyKey,
    **values: object,
) -> str:
    """Return one localized challenge string with strict placeholders."""

    resolved = locale if isinstance(locale, AppLocale) else AppLocale.resolve(locale)
    template = _CATALOGS[resolved][key]
    required = {
        field_name for _, field_name, _, _ in Formatter().parse(template) if field_name is not None
    }
    provided = set(values)
    if required != provided:
        raise ValueError(
            f"Challenge copy {key.value!r} requires placeholders {sorted(required)}; "
            f"received {sorted(provided)}."
        )
    return template.format(**values)


def validate_challenge_copy() -> None:
    """Reject missing keys or placeholder drift across languages."""

    expected_keys = set(ChallengeCopyKey)
    expected_placeholders: dict[ChallengeCopyKey, set[str]] | None = None
    for locale, catalog in _CATALOGS.items():
        if set(catalog) != expected_keys:
            missing = expected_keys - set(catalog)
            extra = set(catalog) - expected_keys
            raise ValueError(
                f"Incomplete challenge copy for {locale.value}: missing={sorted(missing)}, "
                f"extra={sorted(extra)}"
            )
        placeholders = {
            key: {
                field_name
                for _, field_name, _, _ in Formatter().parse(template)
                if field_name is not None
            }
            for key, template in catalog.items()
        }
        if expected_placeholders is None:
            expected_placeholders = placeholders
        elif placeholders != expected_placeholders:
            raise ValueError(f"Challenge placeholders differ for locale {locale.value}.")


validate_challenge_copy()

__all__ = ["ChallengeCopyKey", "challenge_text", "validate_challenge_copy"]
