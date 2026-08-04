"""Strict trilingual copy for scientific laboratory workspaces."""

from __future__ import annotations

from enum import StrEnum

from .locales import AppLocale


class ScientificWorkspaceCopyKey(StrEnum):
    TITLE = "title"
    DESCRIPTION = "description"
    LOCATION = "location"
    FILE = "file"
    SAVE_FILE = "save_file"
    RUN_SCRIPT = "run_script"
    RUN_TESTS = "run_tests"
    REFRESH = "refresh"
    OUTPUT = "output"
    READ_ONLY = "read_only"
    EDITABLE = "editable"
    NO_WORKSPACE = "no_workspace"
    MATERIALIZED = "materialized"
    SAVED = "saved"
    RUN_COMPLETE = "run_complete"
    TEST_COMPLETE = "test_complete"
    SAVE_FAILED = "save_failed"
    LOAD_FAILED = "load_failed"


_COPY: dict[ScientificWorkspaceCopyKey, dict[AppLocale, str]] = {
    ScientificWorkspaceCopyKey.TITLE: {
        AppLocale.SPANISH_SPAIN: "Workspace científico",
        AppLocale.ENGLISH: "Scientific workspace",
        AppLocale.DANISH_DENMARK: "Videnskabeligt arbejdsområde",
    },
    ScientificWorkspaceCopyKey.DESCRIPTION: {
        AppLocale.SPANISH_SPAIN: "Archivos persistentes, datos, pruebas y resultados para desarrollar el laboratorio como una investigación reproducible.",
        AppLocale.ENGLISH: "Persistent files, data, tests, and outputs for developing the laboratory as a reproducible investigation.",
        AppLocale.DANISH_DENMARK: "Vedvarende filer, data, test og output til at udvikle laboratoriet som en reproducerbar undersøgelse.",
    },
    ScientificWorkspaceCopyKey.LOCATION: {
        AppLocale.SPANISH_SPAIN: "Ubicación local: {path}",
        AppLocale.ENGLISH: "Local location: {path}",
        AppLocale.DANISH_DENMARK: "Lokal placering: {path}",
    },
    ScientificWorkspaceCopyKey.FILE: {
        AppLocale.SPANISH_SPAIN: "Archivo",
        AppLocale.ENGLISH: "File",
        AppLocale.DANISH_DENMARK: "Fil",
    },
    ScientificWorkspaceCopyKey.SAVE_FILE: {
        AppLocale.SPANISH_SPAIN: "Guardar archivo",
        AppLocale.ENGLISH: "Save file",
        AppLocale.DANISH_DENMARK: "Gem fil",
    },
    ScientificWorkspaceCopyKey.RUN_SCRIPT: {
        AppLocale.SPANISH_SPAIN: "Ejecutar análisis",
        AppLocale.ENGLISH: "Run analysis",
        AppLocale.DANISH_DENMARK: "Kør analyse",
    },
    ScientificWorkspaceCopyKey.RUN_TESTS: {
        AppLocale.SPANISH_SPAIN: "Ejecutar pruebas",
        AppLocale.ENGLISH: "Run tests",
        AppLocale.DANISH_DENMARK: "Kør test",
    },
    ScientificWorkspaceCopyKey.REFRESH: {
        AppLocale.SPANISH_SPAIN: "Recargar",
        AppLocale.ENGLISH: "Reload",
        AppLocale.DANISH_DENMARK: "Genindlæs",
    },
    ScientificWorkspaceCopyKey.OUTPUT: {
        AppLocale.SPANISH_SPAIN: "Resultado del workspace",
        AppLocale.ENGLISH: "Workspace result",
        AppLocale.DANISH_DENMARK: "Resultat fra arbejdsområdet",
    },
    ScientificWorkspaceCopyKey.READ_ONLY: {
        AppLocale.SPANISH_SPAIN: "Archivo autorado de solo lectura",
        AppLocale.ENGLISH: "Authored read-only file",
        AppLocale.DANISH_DENMARK: "Forfatterdefineret skrivebeskyttet fil",
    },
    ScientificWorkspaceCopyKey.EDITABLE: {
        AppLocale.SPANISH_SPAIN: "Archivo del estudiante",
        AppLocale.ENGLISH: "Learner-owned file",
        AppLocale.DANISH_DENMARK: "Studenterstyret fil",
    },
    ScientificWorkspaceCopyKey.NO_WORKSPACE: {
        AppLocale.SPANISH_SPAIN: "Este laboratorio todavía no tiene un workspace multiarquivo.",
        AppLocale.ENGLISH: "This laboratory does not yet have a multi-file workspace.",
        AppLocale.DANISH_DENMARK: "Dette laboratorium har endnu ikke et arbejdsområde med flere filer.",
    },
    ScientificWorkspaceCopyKey.MATERIALIZED: {
        AppLocale.SPANISH_SPAIN: "Workspace preparado. Los archivos editables se conservan entre sesiones.",
        AppLocale.ENGLISH: "Workspace prepared. Editable files persist between sessions.",
        AppLocale.DANISH_DENMARK: "Arbejdsområdet er klargjort. Redigerbare filer bevares mellem sessioner.",
    },
    ScientificWorkspaceCopyKey.SAVED: {
        AppLocale.SPANISH_SPAIN: "Archivo guardado: {path}",
        AppLocale.ENGLISH: "File saved: {path}",
        AppLocale.DANISH_DENMARK: "Fil gemt: {path}",
    },
    ScientificWorkspaceCopyKey.RUN_COMPLETE: {
        AppLocale.SPANISH_SPAIN: "Ejecución finalizada con estado: {status}",
        AppLocale.ENGLISH: "Execution completed with status: {status}",
        AppLocale.DANISH_DENMARK: "Kørsel afsluttet med status: {status}",
    },
    ScientificWorkspaceCopyKey.TEST_COMPLETE: {
        AppLocale.SPANISH_SPAIN: "Pruebas finalizadas con estado: {status}",
        AppLocale.ENGLISH: "Tests completed with status: {status}",
        AppLocale.DANISH_DENMARK: "Test afsluttet med status: {status}",
    },
    ScientificWorkspaceCopyKey.SAVE_FAILED: {
        AppLocale.SPANISH_SPAIN: "No se pudo guardar el archivo: {error}",
        AppLocale.ENGLISH: "The file could not be saved: {error}",
        AppLocale.DANISH_DENMARK: "Filen kunne ikke gemmes: {error}",
    },
    ScientificWorkspaceCopyKey.LOAD_FAILED: {
        AppLocale.SPANISH_SPAIN: "No se pudo cargar el workspace: {error}",
        AppLocale.ENGLISH: "The workspace could not be loaded: {error}",
        AppLocale.DANISH_DENMARK: "Arbejdsområdet kunne ikke indlæses: {error}",
    },
}


def scientific_workspace_text(
    locale: AppLocale,
    key: ScientificWorkspaceCopyKey,
    **values: object,
) -> str:
    """Return strict localized workspace copy."""

    return _COPY[key][locale].format(**values)


__all__ = ["ScientificWorkspaceCopyKey", "scientific_workspace_text"]
