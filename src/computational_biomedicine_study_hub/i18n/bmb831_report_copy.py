"""Strict trilingual copy for the BMB831 individual-report studio."""

from __future__ import annotations

from enum import StrEnum

from .locales import AppLocale


class BMB831ReportCopyKey(StrEnum):
    TAB = "tab"
    TITLE = "title"
    INTRO = "intro"
    ENGLISH_BOUNDARY = "english_boundary"
    SECTION = "section"
    CHECKLIST = "checklist"
    DRAFT = "draft"
    SAVE = "save"
    SAVED = "saved"
    WORD_COUNT = "word_count"
    PROGRESS = "progress"
    NO_OFFICIAL_GRADE = "no_official_grade"


_COPY: dict[BMB831ReportCopyKey, dict[AppLocale, str]] = {
    BMB831ReportCopyKey.TAB: {
        AppLocale.SPANISH_SPAIN: "BMB831 — Informe",
        AppLocale.ENGLISH: "BMB831 — Report",
        AppLocale.DANISH_DENMARK: "BMB831 — Rapport",
    },
    BMB831ReportCopyKey.TITLE: {
        AppLocale.SPANISH_SPAIN: "Estudio del informe individual BMB831",
        AppLocale.ENGLISH: "BMB831 individual report studio",
        AppLocale.DANISH_DENMARK: "BMB831-studie til individuel rapport",
    },
    BMB831ReportCopyKey.INTRO: {
        AppLocale.SPANISH_SPAIN: "Redacta el informe por secciones con trazabilidad entre pregunta, datos, métodos, resultados, figuras, interpretación y limitaciones.",
        AppLocale.ENGLISH: "Draft the report section by section with traceability among question, data, methods, results, figures, interpretation, and limitations.",
        AppLocale.DANISH_DENMARK: "Skriv rapporten afsnit for afsnit med sporbarhed mellem spørgsmål, data, metoder, resultater, figurer, fortolkning og begrænsninger.",
    },
    BMB831ReportCopyKey.ENGLISH_BOUNDARY: {
        AppLocale.SPANISH_SPAIN: "El examen publicado exige un informe individual en inglés. Los controles pueden mostrarse en el idioma de la aplicación, pero el texto del informe debe redactarse en inglés.",
        AppLocale.ENGLISH: "The published examination requires an individual report in English. Interface controls may follow the application language, but the report prose must be written in English.",
        AppLocale.DANISH_DENMARK: "Den offentliggjorte eksamen kræver en individuel rapport på engelsk. Kontroller kan følge applikationens sprog, men rapportteksten skal skrives på engelsk.",
    },
    BMB831ReportCopyKey.SECTION: {
        AppLocale.SPANISH_SPAIN: "Sección",
        AppLocale.ENGLISH: "Section",
        AppLocale.DANISH_DENMARK: "Afsnit",
    },
    BMB831ReportCopyKey.CHECKLIST: {
        AppLocale.SPANISH_SPAIN: "Lista interna de preparación",
        AppLocale.ENGLISH: "Internal preparation checklist",
        AppLocale.DANISH_DENMARK: "Intern forberedelsestjekliste",
    },
    BMB831ReportCopyKey.DRAFT: {
        AppLocale.SPANISH_SPAIN: "Borrador en inglés",
        AppLocale.ENGLISH: "English draft",
        AppLocale.DANISH_DENMARK: "Engelsk udkast",
    },
    BMB831ReportCopyKey.SAVE: {
        AppLocale.SPANISH_SPAIN: "Guardar",
        AppLocale.ENGLISH: "Save",
        AppLocale.DANISH_DENMARK: "Gem",
    },
    BMB831ReportCopyKey.SAVED: {
        AppLocale.SPANISH_SPAIN: "Guardado localmente",
        AppLocale.ENGLISH: "Saved locally",
        AppLocale.DANISH_DENMARK: "Gemt lokalt",
    },
    BMB831ReportCopyKey.WORD_COUNT: {
        AppLocale.SPANISH_SPAIN: "Palabras",
        AppLocale.ENGLISH: "Words",
        AppLocale.DANISH_DENMARK: "Ord",
    },
    BMB831ReportCopyKey.PROGRESS: {
        AppLocale.SPANISH_SPAIN: "Secciones con texto",
        AppLocale.ENGLISH: "Sections with text",
        AppLocale.DANISH_DENMARK: "Afsnit med tekst",
    },
    BMB831ReportCopyKey.NO_OFFICIAL_GRADE: {
        AppLocale.SPANISH_SPAIN: "Esta herramienta organiza la preparación. No reproduce la rúbrica privada de Itslearning ni asigna una calificación oficial.",
        AppLocale.ENGLISH: "This tool structures preparation. It does not reproduce the private Itslearning rubric or assign an official grade.",
        AppLocale.DANISH_DENMARK: "Værktøjet strukturerer forberedelsen. Det gengiver ikke den private Itslearning-rubrik og giver ikke en officiel karakter.",
    },
}


_SECTION_TITLES: dict[str, dict[AppLocale, str]] = {
    "bmb831.report.question": {
        AppLocale.SPANISH_SPAIN: "Pregunta de investigación y estimando",
        AppLocale.ENGLISH: "Research question and estimand",
        AppLocale.DANISH_DENMARK: "Forskningsspørgsmål og estimand",
    },
    "bmb831.report.data": {
        AppLocale.SPANISH_SPAIN: "Datos, procedencia y diseño",
        AppLocale.ENGLISH: "Data, provenance, and design",
        AppLocale.DANISH_DENMARK: "Data, proveniens og design",
    },
    "bmb831.report.methods": {
        AppLocale.SPANISH_SPAIN: "Métodos y diseño estadístico",
        AppLocale.ENGLISH: "Methods and statistical design",
        AppLocale.DANISH_DENMARK: "Metoder og statistisk design",
    },
    "bmb831.report.qc": {
        AppLocale.SPANISH_SPAIN: "Control de calidad y preprocesamiento",
        AppLocale.ENGLISH: "Quality control and preprocessing",
        AppLocale.DANISH_DENMARK: "Kvalitetskontrol og præprocessering",
    },
    "bmb831.report.results": {
        AppLocale.SPANISH_SPAIN: "Resultados estadísticos",
        AppLocale.ENGLISH: "Statistical results",
        AppLocale.DANISH_DENMARK: "Statistiske resultater",
    },
    "bmb831.report.figures": {
        AppLocale.SPANISH_SPAIN: "Figuras y tablas",
        AppLocale.ENGLISH: "Figures and tables",
        AppLocale.DANISH_DENMARK: "Figurer og tabeller",
    },
    "bmb831.report.interpretation": {
        AppLocale.SPANISH_SPAIN: "Interpretación biológica",
        AppLocale.ENGLISH: "Biological interpretation",
        AppLocale.DANISH_DENMARK: "Biologisk fortolkning",
    },
    "bmb831.report.limitations": {
        AppLocale.SPANISH_SPAIN: "Limitaciones y generalización",
        AppLocale.ENGLISH: "Limitations and generalisation",
        AppLocale.DANISH_DENMARK: "Begrænsninger og generalisering",
    },
    "bmb831.report.reproducibility": {
        AppLocale.SPANISH_SPAIN: "Reproducibilidad y disponibilidad",
        AppLocale.ENGLISH: "Reproducibility and data availability",
        AppLocale.DANISH_DENMARK: "Reproducerbarhed og datatilgængelighed",
    },
    "bmb831.report.abstract": {
        AppLocale.SPANISH_SPAIN: "Resumen",
        AppLocale.ENGLISH: "Abstract",
        AppLocale.DANISH_DENMARK: "Abstract",
    },
}


def bmb831_report_text(locale: AppLocale, key: BMB831ReportCopyKey) -> str:
    """Return strict localized interface copy."""

    return _COPY[key][locale]


def bmb831_report_section_title(locale: AppLocale, section_id: str) -> str:
    """Return one localized report-section title by stable ID."""

    try:
        return _SECTION_TITLES[section_id][locale]
    except KeyError as exc:
        raise ValueError(f"Unknown BMB831 report section {section_id!r}.") from exc


__all__ = [
    "BMB831ReportCopyKey",
    "bmb831_report_section_title",
    "bmb831_report_text",
]
