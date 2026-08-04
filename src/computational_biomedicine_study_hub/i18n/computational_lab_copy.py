"""Strict trilingual interface copy for computational laboratory work."""

from __future__ import annotations

from enum import StrEnum

from ..learning.computational_labs import LabStage
from .locales import AppLocale


class ComputationalLabCopyKey(StrEnum):
    NAVIGATION = "navigation"
    PAGE_TITLE = "page_title"
    PAGE_SUBTITLE = "page_subtitle"
    LAB = "lab"
    RESEARCH_QUESTION = "research_question"
    DATA_PROVENANCE = "data_provenance"
    OBJECTIVES = "objectives"
    PREREQUISITES = "prerequisites"
    PROGRESS = "progress"
    TASK = "task"
    PREVIOUS = "previous"
    NEXT = "next"
    SAVE = "save"
    VERIFY = "verify"
    COMPLETE = "complete"
    MENTOR = "mentor"
    EXPORT = "export"
    OUTPUT = "output"
    CHECKPOINT_PASSED = "checkpoint_passed"
    CHECKPOINT_FAILED = "checkpoint_failed"
    ANSWER_REQUIRED = "answer_required"
    SAVED = "saved"
    EXPORTED = "exported"
    EXPORT_DIALOG = "export_dialog"
    MARKDOWN_FILTER = "markdown_filter"
    HINT_LEVEL = "hint_level"


_COPY: dict[ComputationalLabCopyKey, dict[AppLocale, str]] = {
    ComputationalLabCopyKey.NAVIGATION: {
        AppLocale.SPANISH_SPAIN: "Laboratorios",
        AppLocale.ENGLISH: "Laboratories",
        AppLocale.DANISH_DENMARK: "Laboratorier",
    },
    ComputationalLabCopyKey.PAGE_TITLE: {
        AppLocale.SPANISH_SPAIN: "Laboratorios de biomedicina computacional",
        AppLocale.ENGLISH: "Computational biomedicine laboratories",
        AppLocale.DANISH_DENMARK: "Laboratorier i beregningsbiomedicin",
    },
    ComputationalLabCopyKey.PAGE_SUBTITLE: {
        AppLocale.SPANISH_SPAIN: "Miniinvestigaciones persistentes con implementación, validación, interpretación y defensa.",
        AppLocale.ENGLISH: "Persistent mini-investigations with implementation, validation, interpretation, and defence.",
        AppLocale.DANISH_DENMARK: "Vedvarende miniundersøgelser med implementering, validering, fortolkning og forsvar.",
    },
    ComputationalLabCopyKey.LAB: {
        AppLocale.SPANISH_SPAIN: "Laboratorio",
        AppLocale.ENGLISH: "Laboratory",
        AppLocale.DANISH_DENMARK: "Laboratorium",
    },
    ComputationalLabCopyKey.RESEARCH_QUESTION: {
        AppLocale.SPANISH_SPAIN: "Pregunta de investigación",
        AppLocale.ENGLISH: "Research question",
        AppLocale.DANISH_DENMARK: "Forskningsspørgsmål",
    },
    ComputationalLabCopyKey.DATA_PROVENANCE: {
        AppLocale.SPANISH_SPAIN: "Datos y procedencia",
        AppLocale.ENGLISH: "Data and provenance",
        AppLocale.DANISH_DENMARK: "Data og proveniens",
    },
    ComputationalLabCopyKey.OBJECTIVES: {
        AppLocale.SPANISH_SPAIN: "Objetivos observables",
        AppLocale.ENGLISH: "Observable objectives",
        AppLocale.DANISH_DENMARK: "Observerbare læringsmål",
    },
    ComputationalLabCopyKey.PREREQUISITES: {
        AppLocale.SPANISH_SPAIN: "Prerrequisitos",
        AppLocale.ENGLISH: "Prerequisites",
        AppLocale.DANISH_DENMARK: "Forudsætninger",
    },
    ComputationalLabCopyKey.PROGRESS: {
        AppLocale.SPANISH_SPAIN: "Progreso: {percent}%",
        AppLocale.ENGLISH: "Progress: {percent}%",
        AppLocale.DANISH_DENMARK: "Fremskridt: {percent}%",
    },
    ComputationalLabCopyKey.TASK: {
        AppLocale.SPANISH_SPAIN: "Tarea {current} de {total}",
        AppLocale.ENGLISH: "Task {current} of {total}",
        AppLocale.DANISH_DENMARK: "Opgave {current} af {total}",
    },
    ComputationalLabCopyKey.PREVIOUS: {
        AppLocale.SPANISH_SPAIN: "Anterior",
        AppLocale.ENGLISH: "Previous",
        AppLocale.DANISH_DENMARK: "Forrige",
    },
    ComputationalLabCopyKey.NEXT: {
        AppLocale.SPANISH_SPAIN: "Siguiente",
        AppLocale.ENGLISH: "Next",
        AppLocale.DANISH_DENMARK: "Næste",
    },
    ComputationalLabCopyKey.SAVE: {
        AppLocale.SPANISH_SPAIN: "Guardar progreso",
        AppLocale.ENGLISH: "Save progress",
        AppLocale.DANISH_DENMARK: "Gem fremskridt",
    },
    ComputationalLabCopyKey.VERIFY: {
        AppLocale.SPANISH_SPAIN: "Ejecutar checkpoint",
        AppLocale.ENGLISH: "Run checkpoint",
        AppLocale.DANISH_DENMARK: "Kør checkpoint",
    },
    ComputationalLabCopyKey.COMPLETE: {
        AppLocale.SPANISH_SPAIN: "Registrar evidencia",
        AppLocale.ENGLISH: "Record evidence",
        AppLocale.DANISH_DENMARK: "Registrér evidens",
    },
    ComputationalLabCopyKey.MENTOR: {
        AppLocale.SPANISH_SPAIN: "Pedir guía socrática",
        AppLocale.ENGLISH: "Request Socratic guidance",
        AppLocale.DANISH_DENMARK: "Bed om sokratisk vejledning",
    },
    ComputationalLabCopyKey.EXPORT: {
        AppLocale.SPANISH_SPAIN: "Exportar registro",
        AppLocale.ENGLISH: "Export record",
        AppLocale.DANISH_DENMARK: "Eksportér journal",
    },
    ComputationalLabCopyKey.OUTPUT: {
        AppLocale.SPANISH_SPAIN: "Resultado del checkpoint",
        AppLocale.ENGLISH: "Checkpoint result",
        AppLocale.DANISH_DENMARK: "Checkpointresultat",
    },
    ComputationalLabCopyKey.CHECKPOINT_PASSED: {
        AppLocale.SPANISH_SPAIN: "Checkpoint superado. La evidencia quedó registrada.",
        AppLocale.ENGLISH: "Checkpoint passed. Evidence was recorded.",
        AppLocale.DANISH_DENMARK: "Checkpoint bestået. Evidensen blev registreret.",
    },
    ComputationalLabCopyKey.CHECKPOINT_FAILED: {
        AppLocale.SPANISH_SPAIN: "El checkpoint no se superó. Revisa el resultado y tu contrato de entrada.",
        AppLocale.ENGLISH: "The checkpoint did not pass. Review the result and your input contract.",
        AppLocale.DANISH_DENMARK: "Checkpointet blev ikke bestået. Gennemgå resultatet og din inputkontrakt.",
    },
    ComputationalLabCopyKey.ANSWER_REQUIRED: {
        AppLocale.SPANISH_SPAIN: "Escribe una respuesta sustantiva antes de registrar la evidencia.",
        AppLocale.ENGLISH: "Write a substantive response before recording evidence.",
        AppLocale.DANISH_DENMARK: "Skriv et fyldestgørende svar, før evidensen registreres.",
    },
    ComputationalLabCopyKey.SAVED: {
        AppLocale.SPANISH_SPAIN: "Progreso guardado localmente.",
        AppLocale.ENGLISH: "Progress saved locally.",
        AppLocale.DANISH_DENMARK: "Fremskridt gemt lokalt.",
    },
    ComputationalLabCopyKey.EXPORTED: {
        AppLocale.SPANISH_SPAIN: "Registro exportado: {path}",
        AppLocale.ENGLISH: "Record exported: {path}",
        AppLocale.DANISH_DENMARK: "Journal eksporteret: {path}",
    },
    ComputationalLabCopyKey.EXPORT_DIALOG: {
        AppLocale.SPANISH_SPAIN: "Exportar registro del laboratorio",
        AppLocale.ENGLISH: "Export laboratory record",
        AppLocale.DANISH_DENMARK: "Eksportér laboratoriejournal",
    },
    ComputationalLabCopyKey.MARKDOWN_FILTER: {
        AppLocale.SPANISH_SPAIN: "Markdown (*.md)",
        AppLocale.ENGLISH: "Markdown (*.md)",
        AppLocale.DANISH_DENMARK: "Markdown (*.md)",
    },
    ComputationalLabCopyKey.HINT_LEVEL: {
        AppLocale.SPANISH_SPAIN: "Nivel de ayuda solicitado: {level}/6",
        AppLocale.ENGLISH: "Requested support level: {level}/6",
        AppLocale.DANISH_DENMARK: "Anmodet støtteniveau: {level}/6",
    },
}


_STAGE_COPY: dict[LabStage, dict[AppLocale, str]] = {
    LabStage.PREPARE: {
        AppLocale.SPANISH_SPAIN: "Preparar",
        AppLocale.ENGLISH: "Prepare",
        AppLocale.DANISH_DENMARK: "Forbered",
    },
    LabStage.INVESTIGATE: {
        AppLocale.SPANISH_SPAIN: "Investigar",
        AppLocale.ENGLISH: "Investigate",
        AppLocale.DANISH_DENMARK: "Undersøg",
    },
    LabStage.IMPLEMENT: {
        AppLocale.SPANISH_SPAIN: "Implementar",
        AppLocale.ENGLISH: "Implement",
        AppLocale.DANISH_DENMARK: "Implementér",
    },
    LabStage.CHECK: {
        AppLocale.SPANISH_SPAIN: "Comprobar",
        AppLocale.ENGLISH: "Check",
        AppLocale.DANISH_DENMARK: "Kontrollér",
    },
    LabStage.INTERPRET: {
        AppLocale.SPANISH_SPAIN: "Interpretar",
        AppLocale.ENGLISH: "Interpret",
        AppLocale.DANISH_DENMARK: "Fortolk",
    },
    LabStage.DEFEND: {
        AppLocale.SPANISH_SPAIN: "Defender",
        AppLocale.ENGLISH: "Defend",
        AppLocale.DANISH_DENMARK: "Forsvar",
    },
    LabStage.CONSOLIDATE: {
        AppLocale.SPANISH_SPAIN: "Consolidar",
        AppLocale.ENGLISH: "Consolidate",
        AppLocale.DANISH_DENMARK: "Konsolidér",
    },
}


def computational_lab_text(
    locale: AppLocale,
    key: ComputationalLabCopyKey,
    **values: object,
) -> str:
    return _COPY[key][locale].format(**values)


def lab_stage_text(locale: AppLocale, stage: LabStage) -> str:
    return _STAGE_COPY[stage][locale]


__all__ = [
    "ComputationalLabCopyKey",
    "computational_lab_text",
    "lab_stage_text",
]
