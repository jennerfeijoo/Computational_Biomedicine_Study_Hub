"""Strict trilingual copy for artifact-based technical reasoning stations."""

from __future__ import annotations

from enum import StrEnum

from ..learning.technical_stations import TechnicalStationKind
from .locales import AppLocale


class TechnicalStationCopyKey(StrEnum):
    TITLE = "title"
    DESCRIPTION = "description"
    STATION = "station"
    ARTIFACT = "artifact"
    RESPONSE = "response"
    SELF_REVIEW = "self_review"
    SAVE = "save"
    MARK_REVIEWED = "mark_reviewed"
    MENTOR = "mentor"
    EXPORT = "export"
    PROGRESS = "progress"
    ESTIMATED = "estimated"
    HINT_LEVEL = "hint_level"
    NO_STATIONS = "no_stations"
    SAVED = "saved"
    REVIEWED = "reviewed"
    RESPONSE_REQUIRED = "response_required"
    CRITERIA_REQUIRED = "criteria_required"
    FORMATIVE_BOUNDARY = "formative_boundary"
    EXPORT_DIALOG = "export_dialog"
    MARKDOWN_FILTER = "markdown_filter"
    EXPORTED = "exported"


_COPY: dict[TechnicalStationCopyKey, dict[AppLocale, str]] = {
    TechnicalStationCopyKey.TITLE: {
        AppLocale.SPANISH_SPAIN: "Razonamiento técnico con artefactos",
        AppLocale.ENGLISH: "Artifact-based technical reasoning",
        AppLocale.DANISH_DENMARK: "Artefaktbaseret teknisk ræsonnement",
    },
    TechnicalStationCopyKey.DESCRIPTION: {
        AppLocale.SPANISH_SPAIN: "Practica comprensión mediante código, trazas, errores y resultados concretos. No reproduce ni simula un examen oral.",
        AppLocale.ENGLISH: "Practise understanding through concrete code, traces, defects, and outputs. This does not reproduce or simulate an oral examination.",
        AppLocale.DANISH_DENMARK: "Øv forståelse gennem konkret kode, spor, fejl og output. Dette reproducerer eller simulerer ikke en mundtlig eksamen.",
    },
    TechnicalStationCopyKey.STATION: {
        AppLocale.SPANISH_SPAIN: "Estación",
        AppLocale.ENGLISH: "Station",
        AppLocale.DANISH_DENMARK: "Station",
    },
    TechnicalStationCopyKey.ARTIFACT: {
        AppLocale.SPANISH_SPAIN: "Artefacto técnico",
        AppLocale.ENGLISH: "Technical artifact",
        AppLocale.DANISH_DENMARK: "Teknisk artefakt",
    },
    TechnicalStationCopyKey.RESPONSE: {
        AppLocale.SPANISH_SPAIN: "Explicación técnica",
        AppLocale.ENGLISH: "Technical explanation",
        AppLocale.DANISH_DENMARK: "Teknisk forklaring",
    },
    TechnicalStationCopyKey.SELF_REVIEW: {
        AppLocale.SPANISH_SPAIN: "Revisión explícita de la respuesta",
        AppLocale.ENGLISH: "Explicit response self-review",
        AppLocale.DANISH_DENMARK: "Eksplicit selvgennemgang af svaret",
    },
    TechnicalStationCopyKey.SAVE: {
        AppLocale.SPANISH_SPAIN: "Guardar",
        AppLocale.ENGLISH: "Save",
        AppLocale.DANISH_DENMARK: "Gem",
    },
    TechnicalStationCopyKey.MARK_REVIEWED: {
        AppLocale.SPANISH_SPAIN: "Registrar como revisada",
        AppLocale.ENGLISH: "Record as reviewed",
        AppLocale.DANISH_DENMARK: "Registrér som gennemgået",
    },
    TechnicalStationCopyKey.MENTOR: {
        AppLocale.SPANISH_SPAIN: "Pedir revisión socrática",
        AppLocale.ENGLISH: "Request Socratic review",
        AppLocale.DANISH_DENMARK: "Bed om sokratisk gennemgang",
    },
    TechnicalStationCopyKey.EXPORT: {
        AppLocale.SPANISH_SPAIN: "Exportar evidencia",
        AppLocale.ENGLISH: "Export evidence",
        AppLocale.DANISH_DENMARK: "Eksportér evidens",
    },
    TechnicalStationCopyKey.PROGRESS: {
        AppLocale.SPANISH_SPAIN: "Estaciones autorrevisadas: {completed}/{total} ({percent} %)",
        AppLocale.ENGLISH: "Self-reviewed stations: {completed}/{total} ({percent}%)",
        AppLocale.DANISH_DENMARK: "Selvgennemgåede stationer: {completed}/{total} ({percent} %)",
    },
    TechnicalStationCopyKey.ESTIMATED: {
        AppLocale.SPANISH_SPAIN: "Tipo: {kind} · Tiempo estimado: {minutes} min",
        AppLocale.ENGLISH: "Type: {kind} · Estimated time: {minutes} min",
        AppLocale.DANISH_DENMARK: "Type: {kind} · Estimeret tid: {minutes} min",
    },
    TechnicalStationCopyKey.HINT_LEVEL: {
        AppLocale.SPANISH_SPAIN: "Nivel de ayuda solicitado: {level}/6",
        AppLocale.ENGLISH: "Requested support level: {level}/6",
        AppLocale.DANISH_DENMARK: "Anmodet støtteniveau: {level}/6",
    },
    TechnicalStationCopyKey.NO_STATIONS: {
        AppLocale.SPANISH_SPAIN: "Este laboratorio todavía no tiene estaciones técnicas.",
        AppLocale.ENGLISH: "This laboratory does not yet have technical stations.",
        AppLocale.DANISH_DENMARK: "Dette laboratorium har endnu ingen tekniske stationer.",
    },
    TechnicalStationCopyKey.SAVED: {
        AppLocale.SPANISH_SPAIN: "Respuesta guardada localmente.",
        AppLocale.ENGLISH: "Response saved locally.",
        AppLocale.DANISH_DENMARK: "Svaret er gemt lokalt.",
    },
    TechnicalStationCopyKey.REVIEWED: {
        AppLocale.SPANISH_SPAIN: "Estación registrada como intentada y autorrevisada. Esto no certifica dominio.",
        AppLocale.ENGLISH: "Station recorded as attempted and self-reviewed. This does not certify mastery.",
        AppLocale.DANISH_DENMARK: "Stationen er registreret som forsøgt og selvgennemgået. Dette certificerer ikke mestring.",
    },
    TechnicalStationCopyKey.RESPONSE_REQUIRED: {
        AppLocale.SPANISH_SPAIN: "La explicación todavía es demasiado breve para una revisión técnica sustantiva.",
        AppLocale.ENGLISH: "The explanation is still too brief for substantive technical review.",
        AppLocale.DANISH_DENMARK: "Forklaringen er stadig for kort til en substantiel teknisk gennemgang.",
    },
    TechnicalStationCopyKey.CRITERIA_REQUIRED: {
        AppLocale.SPANISH_SPAIN: "Comprueba explícitamente todos los elementos de revisión antes de registrar la estación.",
        AppLocale.ENGLISH: "Explicitly check every review element before recording the station.",
        AppLocale.DANISH_DENMARK: "Kontrollér eksplicit alle gennemgangselementer før stationen registreres.",
    },
    TechnicalStationCopyKey.FORMATIVE_BOUNDARY: {
        AppLocale.SPANISH_SPAIN: "La finalización significa respuesta + autorrevisión estructurada. No representa nota, predicción de examen ni dominio automático.",
        AppLocale.ENGLISH: "Completion means response plus structured self-review. It is not a grade, examination prediction, or automatic mastery claim.",
        AppLocale.DANISH_DENMARK: "Fuldførelse betyder svar plus struktureret selvgennemgang. Det er ikke en karakter, eksamensforudsigelse eller automatisk mestringspåstand.",
    },
    TechnicalStationCopyKey.EXPORT_DIALOG: {
        AppLocale.SPANISH_SPAIN: "Exportar evidencia técnica",
        AppLocale.ENGLISH: "Export technical evidence",
        AppLocale.DANISH_DENMARK: "Eksportér teknisk evidens",
    },
    TechnicalStationCopyKey.MARKDOWN_FILTER: {
        AppLocale.SPANISH_SPAIN: "Markdown (*.md)",
        AppLocale.ENGLISH: "Markdown (*.md)",
        AppLocale.DANISH_DENMARK: "Markdown (*.md)",
    },
    TechnicalStationCopyKey.EXPORTED: {
        AppLocale.SPANISH_SPAIN: "Evidencia exportada: {path}",
        AppLocale.ENGLISH: "Evidence exported: {path}",
        AppLocale.DANISH_DENMARK: "Evidens eksporteret: {path}",
    },
}

_KIND_COPY: dict[TechnicalStationKind, dict[AppLocale, str]] = {
    TechnicalStationKind.CODE_READING: {
        AppLocale.SPANISH_SPAIN: "lectura de código",
        AppLocale.ENGLISH: "code reading",
        AppLocale.DANISH_DENMARK: "kodelæsning",
    },
    TechnicalStationKind.EXECUTION_TRACE: {
        AppLocale.SPANISH_SPAIN: "traza de ejecución",
        AppLocale.ENGLISH: "execution trace",
        AppLocale.DANISH_DENMARK: "eksekveringsspor",
    },
    TechnicalStationKind.DEBUGGING: {
        AppLocale.SPANISH_SPAIN: "depuración",
        AppLocale.ENGLISH: "debugging",
        AppLocale.DANISH_DENMARK: "fejlfinding",
    },
    TechnicalStationKind.OUTPUT_INTERPRETATION: {
        AppLocale.SPANISH_SPAIN: "interpretación de salida",
        AppLocale.ENGLISH: "output interpretation",
        AppLocale.DANISH_DENMARK: "outputfortolkning",
    },
    TechnicalStationKind.METHOD_SELECTION: {
        AppLocale.SPANISH_SPAIN: "selección de método",
        AppLocale.ENGLISH: "method selection",
        AppLocale.DANISH_DENMARK: "metodevalg",
    },
    TechnicalStationKind.COMPLEXITY_ANALYSIS: {
        AppLocale.SPANISH_SPAIN: "análisis de complejidad",
        AppLocale.ENGLISH: "complexity analysis",
        AppLocale.DANISH_DENMARK: "kompleksitetsanalyse",
    },
    TechnicalStationKind.SCIENTIFIC_INTERPRETATION: {
        AppLocale.SPANISH_SPAIN: "interpretación científica",
        AppLocale.ENGLISH: "scientific interpretation",
        AppLocale.DANISH_DENMARK: "videnskabelig fortolkning",
    },
    TechnicalStationKind.PROJECT_REASONING: {
        AppLocale.SPANISH_SPAIN: "razonamiento del proyecto",
        AppLocale.ENGLISH: "project reasoning",
        AppLocale.DANISH_DENMARK: "projektræsonnement",
    },
}


def technical_station_text(
    locale: AppLocale,
    key: TechnicalStationCopyKey,
    **values: object,
) -> str:
    return _COPY[key][locale].format(**values)


def technical_station_kind_text(locale: AppLocale, kind: TechnicalStationKind) -> str:
    return _KIND_COPY[kind][locale]


__all__ = [
    "TechnicalStationCopyKey",
    "technical_station_kind_text",
    "technical_station_text",
]
