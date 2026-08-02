"""Strict localized copy for executable Python learning labs."""

from __future__ import annotations

from enum import StrEnum
from string import Formatter

from .locales import AppLocale


class LabCopyKey(StrEnum):
    """Stable text keys used by executable code labs."""

    TITLE = "lab.title"
    INTRO = "lab.intro"
    RUN = "lab.run"
    RESET = "lab.reset"
    RUNNING = "lab.running"
    SOURCE_REQUIRED = "lab.source_required"
    STDOUT = "lab.stdout"
    STDERR = "lab.stderr"
    EXPECTED = "lab.expected"
    NO_OUTPUT = "lab.no_output"
    STATUS_PASSED = "lab.status.passed"
    STATUS_MISMATCH = "lab.status.mismatch"
    STATUS_RUNTIME_ERROR = "lab.status.runtime_error"
    STATUS_TIMED_OUT = "lab.status.timed_out"
    STATUS_REJECTED = "lab.status.rejected"
    STATUS_OUTPUT_LIMIT = "lab.status.output_limit"
    STATUS_WITH_DURATION = "lab.status.with_duration"


_CATALOGS: dict[AppLocale, dict[LabCopyKey, str]] = {
    AppLocale.SPANISH_SPAIN: {
        LabCopyKey.TITLE: "Laboratorio ejecutable",
        LabCopyKey.INTRO: "",
        LabCopyKey.RUN: "Ejecutar",
        LabCopyKey.RESET: "Restablecer",
        LabCopyKey.RUNNING: "Ejecutando…",
        LabCopyKey.SOURCE_REQUIRED: "Escribe código antes de ejecutarlo.",
        LabCopyKey.STDOUT: "Salida",
        LabCopyKey.STDERR: "Errores",
        LabCopyKey.EXPECTED: "Salida de referencia",
        LabCopyKey.NO_OUTPUT: "(sin salida)",
        LabCopyKey.STATUS_PASSED: "Ejecución completada",
        LabCopyKey.STATUS_MISMATCH: "Ejecución completada",
        LabCopyKey.STATUS_RUNTIME_ERROR: "Error durante la ejecución",
        LabCopyKey.STATUS_TIMED_OUT: "Tiempo de ejecución agotado",
        LabCopyKey.STATUS_REJECTED: "Código rechazado por la política del laboratorio",
        LabCopyKey.STATUS_OUTPUT_LIMIT: "La salida superó el límite permitido",
        LabCopyKey.STATUS_WITH_DURATION: "{status} · {duration} ms",
    },
    AppLocale.ENGLISH: {
        LabCopyKey.TITLE: "Executable lab",
        LabCopyKey.INTRO: "",
        LabCopyKey.RUN: "Run",
        LabCopyKey.RESET: "Reset",
        LabCopyKey.RUNNING: "Running…",
        LabCopyKey.SOURCE_REQUIRED: "Write some code before running it.",
        LabCopyKey.STDOUT: "Output",
        LabCopyKey.STDERR: "Errors",
        LabCopyKey.EXPECTED: "Reference output",
        LabCopyKey.NO_OUTPUT: "(no output)",
        LabCopyKey.STATUS_PASSED: "Execution completed",
        LabCopyKey.STATUS_MISMATCH: "Execution completed",
        LabCopyKey.STATUS_RUNTIME_ERROR: "Runtime error",
        LabCopyKey.STATUS_TIMED_OUT: "Execution timed out",
        LabCopyKey.STATUS_REJECTED: "Code rejected by the lab policy",
        LabCopyKey.STATUS_OUTPUT_LIMIT: "Output exceeded the permitted limit",
        LabCopyKey.STATUS_WITH_DURATION: "{status} · {duration} ms",
    },
    AppLocale.DANISH_DENMARK: {
        LabCopyKey.TITLE: "Kørbart laboratorium",
        LabCopyKey.INTRO: "",
        LabCopyKey.RUN: "Kør",
        LabCopyKey.RESET: "Nulstil",
        LabCopyKey.RUNNING: "Kører…",
        LabCopyKey.SOURCE_REQUIRED: "Skriv kode, før du kører den.",
        LabCopyKey.STDOUT: "Output",
        LabCopyKey.STDERR: "Fejl",
        LabCopyKey.EXPECTED: "Referenceoutput",
        LabCopyKey.NO_OUTPUT: "(intet output)",
        LabCopyKey.STATUS_PASSED: "Kørslen er afsluttet",
        LabCopyKey.STATUS_MISMATCH: "Kørslen er afsluttet",
        LabCopyKey.STATUS_RUNTIME_ERROR: "Kørselsfejl",
        LabCopyKey.STATUS_TIMED_OUT: "Kørselstiden udløb",
        LabCopyKey.STATUS_REJECTED: "Koden blev afvist af laboratoriets regler",
        LabCopyKey.STATUS_OUTPUT_LIMIT: "Outputtet overskred den tilladte grænse",
        LabCopyKey.STATUS_WITH_DURATION: "{status} · {duration} ms",
    },
}


def lab_text(
    locale: AppLocale | str,
    key: LabCopyKey,
    **values: object,
) -> str:
    """Return one localized lab string with strict placeholders."""

    resolved = locale if isinstance(locale, AppLocale) else AppLocale.resolve(locale)
    template = _CATALOGS[resolved][key]
    required = {
        field_name for _, field_name, _, _ in Formatter().parse(template) if field_name is not None
    }
    provided = set(values)
    if required != provided:
        raise ValueError(
            f"Lab copy {key.value!r} requires placeholders {sorted(required)}; "
            f"received {sorted(provided)}."
        )
    return template.format(**values)


def validate_lab_copy() -> None:
    """Reject missing keys or placeholder drift across languages."""

    expected_keys = set(LabCopyKey)
    expected_placeholders: dict[LabCopyKey, set[str]] | None = None
    for locale, catalog in _CATALOGS.items():
        if set(catalog) != expected_keys:
            missing = expected_keys - set(catalog)
            extra = set(catalog) - expected_keys
            raise ValueError(
                f"Incomplete lab copy for {locale.value}: missing={sorted(missing)}, "
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
            raise ValueError(f"Lab placeholders differ for locale {locale.value}.")


validate_lab_copy()

__all__ = ["LabCopyKey", "lab_text", "validate_lab_copy"]
