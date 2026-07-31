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
        LabCopyKey.INTRO: (
            "Edita el ejemplo y ejecútalo en un proceso local restringido. El acceso a archivos, "
            "red y procesos externos está deshabilitado."
        ),
        LabCopyKey.RUN: "Ejecutar",
        LabCopyKey.RESET: "Restablecer",
        LabCopyKey.RUNNING: "Ejecutando…",
        LabCopyKey.STDOUT: "Salida",
        LabCopyKey.STDERR: "Errores",
        LabCopyKey.EXPECTED: "Salida esperada",
        LabCopyKey.NO_OUTPUT: "(sin salida)",
        LabCopyKey.STATUS_PASSED: "Salida correcta",
        LabCopyKey.STATUS_MISMATCH: "El programa terminó, pero la salida no coincide",
        LabCopyKey.STATUS_RUNTIME_ERROR: "Error durante la ejecución",
        LabCopyKey.STATUS_TIMED_OUT: "Tiempo de ejecución agotado",
        LabCopyKey.STATUS_REJECTED: "Código rechazado por la política del laboratorio",
        LabCopyKey.STATUS_OUTPUT_LIMIT: "La salida superó el límite permitido",
        LabCopyKey.STATUS_WITH_DURATION: "{status} · {duration} ms",
    },
    AppLocale.ENGLISH: {
        LabCopyKey.TITLE: "Executable lab",
        LabCopyKey.INTRO: (
            "Edit the example and run it in a restricted local process. File, network and external "
            "process access are disabled."
        ),
        LabCopyKey.RUN: "Run",
        LabCopyKey.RESET: "Reset",
        LabCopyKey.RUNNING: "Running…",
        LabCopyKey.STDOUT: "Output",
        LabCopyKey.STDERR: "Errors",
        LabCopyKey.EXPECTED: "Expected output",
        LabCopyKey.NO_OUTPUT: "(no output)",
        LabCopyKey.STATUS_PASSED: "Output is correct",
        LabCopyKey.STATUS_MISMATCH: "The program finished, but its output does not match",
        LabCopyKey.STATUS_RUNTIME_ERROR: "Runtime error",
        LabCopyKey.STATUS_TIMED_OUT: "Execution timed out",
        LabCopyKey.STATUS_REJECTED: "Code rejected by the lab policy",
        LabCopyKey.STATUS_OUTPUT_LIMIT: "Output exceeded the permitted limit",
        LabCopyKey.STATUS_WITH_DURATION: "{status} · {duration} ms",
    },
    AppLocale.DANISH_DENMARK: {
        LabCopyKey.TITLE: "Kørbart laboratorium",
        LabCopyKey.INTRO: (
            "Redigér eksemplet og kør det i en begrænset lokal proces. Adgang til filer, netværk "
            "og eksterne processer er deaktiveret."
        ),
        LabCopyKey.RUN: "Kør",
        LabCopyKey.RESET: "Nulstil",
        LabCopyKey.RUNNING: "Kører…",
        LabCopyKey.STDOUT: "Output",
        LabCopyKey.STDERR: "Fejl",
        LabCopyKey.EXPECTED: "Forventet output",
        LabCopyKey.NO_OUTPUT: "(intet output)",
        LabCopyKey.STATUS_PASSED: "Outputtet er korrekt",
        LabCopyKey.STATUS_MISMATCH: "Programmet afsluttede, men outputtet stemmer ikke",
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
