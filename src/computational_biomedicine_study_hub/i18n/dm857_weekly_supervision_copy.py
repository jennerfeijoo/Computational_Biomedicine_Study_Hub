"""Spanish, English and Danish copy for DM857 weekly supervision."""

from __future__ import annotations

from enum import StrEnum

from ..learning.dm857_weekly_supervision import WeeklyCycleStatus
from .locales import AppLocale

Triple = tuple[str, str, str]

_LOCALE_INDEX = {
    AppLocale.SPANISH_SPAIN: 0,
    AppLocale.ENGLISH: 1,
    AppLocale.DANISH_DENMARK: 2,
}


class WeeklySupervisionCopyKey(StrEnum):
    """Stable UI keys for longitudinal project supervision."""

    TITLE = "dm857.weekly.title"
    DESCRIPTION = "dm857.weekly.description"
    BOUNDARY = "dm857.weekly.boundary"
    WEEK = "dm857.weekly.week"
    NEW_WEEK = "dm857.weekly.new_week"
    PROGRESS = "dm857.weekly.progress"
    PLANNING = "dm857.weekly.planning"
    OBJECTIVE = "dm857.weekly.objective"
    OBJECTIVE_PLACEHOLDER = "dm857.weekly.objective_placeholder"
    SUCCESS_CRITERIA = "dm857.weekly.success_criteria"
    SUCCESS_PLACEHOLDER = "dm857.weekly.success_placeholder"
    REPOSITORY_EVIDENCE = "dm857.weekly.repository_evidence"
    START_REFERENCE = "dm857.weekly.start_reference"
    END_REFERENCE = "dm857.weekly.end_reference"
    REFERENCE_PLACEHOLDER = "dm857.weekly.reference_placeholder"
    CHANGED_FILES = "dm857.weekly.changed_files"
    TEST_EVIDENCE = "dm857.weekly.test_evidence"
    REASONING = "dm857.weekly.reasoning"
    DECISION_RATIONALE = "dm857.weekly.decision_rationale"
    INDIVIDUAL_CONTRIBUTION = "dm857.weekly.individual_contribution"
    BIOMEDICAL_INTERPRETATION = "dm857.weekly.biomedical_interpretation"
    BLOCKED = "dm857.weekly.blocked"
    BLOCKERS = "dm857.weekly.blockers"
    REVIEW = "dm857.weekly.review"
    REFLECTION = "dm857.weekly.reflection"
    NEXT_COMMITMENT = "dm857.weekly.next_commitment"
    SAVE = "dm857.weekly.save"
    SAVED = "dm857.weekly.saved"
    MENTOR = "dm857.weekly.mentor"
    EMPTY_HINT = "dm857.weekly.empty_hint"


_STATIC: dict[WeeklySupervisionCopyKey, Triple] = {
    WeeklySupervisionCopyKey.TITLE: (
        "Supervisión semanal del proyecto DM857",
        "DM857 weekly project supervision",
        "Ugentlig supervision af DM857-projektet",
    ),
    WeeklySupervisionCopyKey.DESCRIPTION: (
        "Planifica una contribución verificable, registra el cambio real del repositorio y cierra "
        "la semana con pruebas, razonamiento, reflexión y un compromiso siguiente.",
        "Plan one verifiable contribution, record the real repository change, and close the week "
        "with tests, reasoning, reflection and a next commitment.",
        "Planlæg ét verificerbart bidrag, registrer den faktiske repository-ændring, og afslut ugen "
        "med test, ræsonnement, refleksion og en næste forpligtelse.",
    ),
    WeeklySupervisionCopyKey.BOUNDARY: (
        "La completitud mide evidencia registrada, no dominio académico ni calificación oficial. "
        "No incluyas credenciales, datos personales ni datos biomédicos sensibles.",
        "Completeness measures recorded evidence, not academic mastery or an official grade. Do "
        "not include credentials, personal data or sensitive biomedical data.",
        "Fuldstændighed måler registreret evidens, ikke faglig beherskelse eller en officiel karakter. "
        "Medtag ikke legitimationsoplysninger, persondata eller følsomme biomedicinske data.",
    ),
    WeeklySupervisionCopyKey.WEEK: ("Semana", "Week", "Uge"),
    WeeklySupervisionCopyKey.NEW_WEEK: (
        "Crear semana siguiente",
        "Create next week",
        "Opret næste uge",
    ),
    WeeklySupervisionCopyKey.PROGRESS: (
        "{status} · {completed}/{total} evidencias · {percent}%",
        "{status} · {completed}/{total} evidence fields · {percent}%",
        "{status} · {completed}/{total} evidensfelter · {percent}%",
    ),
    WeeklySupervisionCopyKey.PLANNING: (
        "1. Planificación",
        "1. Planning",
        "1. Planlægning",
    ),
    WeeklySupervisionCopyKey.OBJECTIVE: (
        "Objetivo semanal",
        "Weekly objective",
        "Ugens mål",
    ),
    WeeklySupervisionCopyKey.OBJECTIVE_PLACEHOLDER: (
        "Una contribución concreta que pueda demostrarse al final de la semana.",
        "One concrete contribution that can be demonstrated at the end of the week.",
        "Ét konkret bidrag, der kan demonstreres ved ugens afslutning.",
    ),
    WeeklySupervisionCopyKey.SUCCESS_CRITERIA: (
        "Criterios de éxito verificables",
        "Verifiable success criteria",
        "Verificerbare succeskriterier",
    ),
    WeeklySupervisionCopyKey.SUCCESS_PLACEHOLDER: (
        "Resultados observables, pruebas o condiciones que indiquen que el objetivo se cumplió.",
        "Observable outputs, tests or conditions showing that the objective was met.",
        "Observerbare resultater, test eller betingelser, der viser, at målet blev nået.",
    ),
    WeeklySupervisionCopyKey.REPOSITORY_EVIDENCE: (
        "2. Evidencia del repositorio",
        "2. Repository evidence",
        "2. Repository-evidens",
    ),
    WeeklySupervisionCopyKey.START_REFERENCE: (
        "Referencia inicial",
        "Start reference",
        "Startreference",
    ),
    WeeklySupervisionCopyKey.END_REFERENCE: (
        "Referencia final",
        "End reference",
        "Slutreference",
    ),
    WeeklySupervisionCopyKey.REFERENCE_PLACEHOLDER: (
        "SHA, etiqueta, rama o referencia estable",
        "SHA, tag, branch or stable reference",
        "SHA, tag, branch eller stabil reference",
    ),
    WeeklySupervisionCopyKey.CHANGED_FILES: (
        "Archivos o componentes modificados",
        "Changed files or components",
        "Ændrede filer eller komponenter",
    ),
    WeeklySupervisionCopyKey.TEST_EVIDENCE: (
        "Comandos, pruebas y resultados",
        "Commands, tests and results",
        "Kommandoer, test og resultater",
    ),
    WeeklySupervisionCopyKey.REASONING: (
        "3. Razonamiento y contribución",
        "3. Reasoning and contribution",
        "3. Ræsonnement og bidrag",
    ),
    WeeklySupervisionCopyKey.DECISION_RATIONALE: (
        "Decisión técnica y justificación",
        "Technical decision and rationale",
        "Teknisk beslutning og begrundelse",
    ),
    WeeklySupervisionCopyKey.INDIVIDUAL_CONTRIBUTION: (
        "Contribución individual demostrable",
        "Demonstrable individual contribution",
        "Dokumenterbart individuelt bidrag",
    ),
    WeeklySupervisionCopyKey.BIOMEDICAL_INTERPRETATION: (
        "Interpretación o relevancia biomédica",
        "Biomedical interpretation or relevance",
        "Biomedicinsk fortolkning eller relevans",
    ),
    WeeklySupervisionCopyKey.BLOCKED: (
        "La semana está bloqueada",
        "The week is blocked",
        "Ugen er blokeret",
    ),
    WeeklySupervisionCopyKey.BLOCKERS: (
        "Bloqueos, dependencias y acción de desbloqueo",
        "Blockers, dependencies and unblocking action",
        "Blokeringer, afhængigheder og handling for at komme videre",
    ),
    WeeklySupervisionCopyKey.REVIEW: (
        "4. Revisión y continuidad",
        "4. Review and continuity",
        "4. Evaluering og kontinuitet",
    ),
    WeeklySupervisionCopyKey.REFLECTION: (
        "Qué cambió en mi comprensión",
        "What changed in my understanding",
        "Hvad ændrede sig i min forståelse",
    ),
    WeeklySupervisionCopyKey.NEXT_COMMITMENT: (
        "Siguiente compromiso concreto",
        "Next concrete commitment",
        "Næste konkrete forpligtelse",
    ),
    WeeklySupervisionCopyKey.SAVE: (
        "Guardar semana",
        "Save week",
        "Gem uge",
    ),
    WeeklySupervisionCopyKey.SAVED: (
        "Ciclo semanal guardado localmente.",
        "Weekly cycle saved locally.",
        "Ugecyklussen er gemt lokalt.",
    ),
    WeeklySupervisionCopyKey.MENTOR: (
        "Revisar con mentor",
        "Review with mentor",
        "Gennemgå med mentor",
    ),
    WeeklySupervisionCopyKey.EMPTY_HINT: (
        "Comienza definiendo un objetivo semanal y criterios que puedan verificarse.",
        "Begin by defining a weekly objective and criteria that can be verified.",
        "Begynd med at definere et ugentligt mål og kriterier, der kan verificeres.",
    ),
}

_STATUS: dict[WeeklyCycleStatus, Triple] = {
    WeeklyCycleStatus.EMPTY: ("Vacía", "Empty", "Tom"),
    WeeklyCycleStatus.PLANNED: ("Planificada", "Planned", "Planlagt"),
    WeeklyCycleStatus.ACTIVE: ("Activa", "Active", "Aktiv"),
    WeeklyCycleStatus.BLOCKED: ("Bloqueada", "Blocked", "Blokeret"),
    WeeklyCycleStatus.COMPLETE: ("Completa", "Complete", "Færdig"),
}


def weekly_supervision_text(
    locale: AppLocale,
    key: WeeklySupervisionCopyKey,
    **values: object,
) -> str:
    """Return localized copy and interpolate named values."""

    template = _STATIC[key][_LOCALE_INDEX[locale]]
    return template.format(**values)


def weekly_cycle_status_text(locale: AppLocale, status: WeeklyCycleStatus) -> str:
    """Return a localized derived weekly-cycle status."""

    return _STATUS[status][_LOCALE_INDEX[locale]]


__all__ = [
    "WeeklySupervisionCopyKey",
    "weekly_cycle_status_text",
    "weekly_supervision_text",
]
