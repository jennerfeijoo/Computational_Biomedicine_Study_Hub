"""Strict Spanish, English and Danish copy for the DM857 capstone workflow."""

from __future__ import annotations

from enum import StrEnum
from string import Formatter

from ..learning.dm857_capstone import DM857_CAPSTONE_MILESTONES, DM857_CAPSTONE_RUBRIC
from .locales import AppLocale

Triple = tuple[str, str, str]
MilestoneCopy = tuple[str, str, tuple[str, ...]]
LocalizedMilestoneCopy = tuple[MilestoneCopy, MilestoneCopy, MilestoneCopy]

_LOCALE_INDEX = {
    AppLocale.SPANISH_SPAIN: 0,
    AppLocale.ENGLISH: 1,
    AppLocale.DANISH_DENMARK: 2,
}


class CapstoneCopyKey(StrEnum):
    """Stable keys for project metadata, evidence, readiness and reporting."""

    TITLE = "capstone.title"
    SOURCE_BOUNDARY = "capstone.source_boundary"
    METADATA = "capstone.metadata"
    PROJECT_TITLE = "capstone.project_title"
    GROUP_MEMBERS = "capstone.group_members"
    GROUP_PLACEHOLDER = "capstone.group_placeholder"
    REPOSITORY_URL = "capstone.repository_url"
    REPORT_PATH = "capstone.report_path"
    SAVE = "capstone.save"
    SAVED = "capstone.saved"
    PROGRESS = "capstone.progress"
    READY_SUMMARY = "capstone.ready_summary"
    INCOMPLETE_SUMMARY = "capstone.incomplete_summary"
    STATUS_NOT_STARTED = "capstone.status_not_started"
    STATUS_IN_PROGRESS = "capstone.status_in_progress"
    STATUS_READY = "capstone.status_ready"
    EVIDENCE_NOTE = "capstone.evidence_note"
    EVIDENCE_PLACEHOLDER = "capstone.evidence_placeholder"
    COMMIT_REFERENCE = "capstone.commit_reference"
    COMMIT_PLACEHOLDER = "capstone.commit_placeholder"
    RUBRIC_TITLE = "capstone.rubric_title"
    RUBRIC_NOTICE = "capstone.rubric_notice"
    RUBRIC_SCORE = "capstone.rubric_score"
    NOT_SCORED = "capstone.not_scored"
    REPORT_TITLE = "capstone.report_title"
    REPORT_NOTICE = "capstone.report_notice"
    REPORT_TEMPLATE = "capstone.report_template"


_STATIC: dict[CapstoneCopyKey, Triple] = {
    CapstoneCopyKey.TITLE: (
        "Capstone DM857: proyecto e informe",
        "DM857 capstone: project and report",
        "DM857-capstone: projekt og rapport",
    ),
    CapstoneCopyKey.SOURCE_BOUNDARY: (
        "Este flujo prepara el proyecto grupal y el informe de un máximo de diez páginas descritos "
        "públicamente por SDU. La consigna detallada y la rúbrica oficial de itslearning no están "
        "disponibles; la plantilla y la rúbrica mostradas aquí son apoyos internos de preparación.",
        "This workflow prepares the group project and maximum ten-page report described publicly "
        "by SDU. The detailed brief and official itslearning rubric are unavailable; the template "
        "and rubric shown here are internal preparation aids.",
        "Dette forløb forbereder gruppeprojektet og rapporten på højst ti sider, som SDU beskriver "
        "offentligt. Den detaljerede opgave og den officielle itslearning-rubrik er ikke tilgængelige; "
        "skabelonen og rubrikken her er interne forberedelsesværktøjer.",
    ),
    CapstoneCopyKey.METADATA: (
        "Identidad y artefactos del proyecto",
        "Project identity and artefacts",
        "Projektidentitet og artefakter",
    ),
    CapstoneCopyKey.PROJECT_TITLE: (
        "Título del proyecto",
        "Project title",
        "Projekttitel",
    ),
    CapstoneCopyKey.GROUP_MEMBERS: (
        "Integrantes del grupo",
        "Group members",
        "Gruppemedlemmer",
    ),
    CapstoneCopyKey.GROUP_PLACEHOLDER: (
        "Nombres separados por comas",
        "Comma-separated names",
        "Navne adskilt med komma",
    ),
    CapstoneCopyKey.REPOSITORY_URL: (
        "URL del repositorio",
        "Repository URL",
        "Repository-URL",
    ),
    CapstoneCopyKey.REPORT_PATH: (
        "Ruta o enlace del borrador del informe",
        "Report draft path or link",
        "Sti eller link til rapportudkast",
    ),
    CapstoneCopyKey.SAVE: (
        "Guardar progreso",
        "Save progress",
        "Gem fremskridt",
    ),
    CapstoneCopyKey.SAVED: (
        "Progreso guardado localmente.",
        "Progress saved locally.",
        "Fremskridt gemt lokalt.",
    ),
    CapstoneCopyKey.PROGRESS: (
        "{ready}/{total} hitos listos · {percent}%",
        "{ready}/{total} milestones ready · {percent}%",
        "{ready}/{total} milepæle klar · {percent}%",
    ),
    CapstoneCopyKey.READY_SUMMARY: (
        "El andamiaje interno está completo. Conserva los artefactos y compáralos con la consigna "
        "oficial cuando esté disponible.",
        "The internal scaffold is complete. Preserve the artefacts and compare them with the "
        "official brief when it becomes available.",
        "Det interne stillads er komplet. Bevar artefakterne og sammenlign dem med den officielle "
        "opgave, når den bliver tilgængelig.",
    ),
    CapstoneCopyKey.INCOMPLETE_SUMMARY: (
        "Completa metadatos, evidencias, cinco hitos, borrador del informe y autoevaluación.",
        "Complete metadata, evidence, five milestones, the report draft and self-assessment.",
        "Udfyld metadata, evidens, fem milepæle, rapportudkast og selvevaluering.",
    ),
    CapstoneCopyKey.STATUS_NOT_STARTED: (
        "No iniciado",
        "Not started",
        "Ikke startet",
    ),
    CapstoneCopyKey.STATUS_IN_PROGRESS: (
        "En progreso",
        "In progress",
        "I gang",
    ),
    CapstoneCopyKey.STATUS_READY: ("Listo", "Ready", "Klar"),
    CapstoneCopyKey.EVIDENCE_NOTE: (
        "Nota de evidencia",
        "Evidence note",
        "Evidensnote",
    ),
    CapstoneCopyKey.EVIDENCE_PLACEHOLDER: (
        "Describe la decisión, el artefacto producido y cómo puede verificarse.",
        "Describe the decision, produced artefact and how it can be verified.",
        "Beskriv beslutningen, det producerede artefakt og hvordan det kan verificeres.",
    ),
    CapstoneCopyKey.COMMIT_REFERENCE: (
        "Commit o referencia verificable",
        "Commit or verifiable reference",
        "Commit eller verificerbar reference",
    ),
    CapstoneCopyKey.COMMIT_PLACEHOLDER: (
        "SHA, etiqueta o referencia estable",
        "SHA, tag or stable reference",
        "SHA, tag eller stabil reference",
    ),
    CapstoneCopyKey.RUBRIC_TITLE: (
        "Rúbrica interna de preparación",
        "Internal preparation rubric",
        "Intern forberedelsesrubrik",
    ),
    CapstoneCopyKey.RUBRIC_NOTICE: (
        "Escala de autoevaluación de 0 a 4. No sustituye la rúbrica oficial de SDU.",
        "Self-assessment scale from 0 to 4. This does not replace the official SDU rubric.",
        "Selvevalueringsskala fra 0 til 4. Den erstatter ikke SDU's officielle rubrik.",
    ),
    CapstoneCopyKey.RUBRIC_SCORE: (
        "{weight}% · puntuación",
        "{weight}% · score",
        "{weight}% · score",
    ),
    CapstoneCopyKey.NOT_SCORED: (
        "Sin valorar",
        "Not scored",
        "Ikke vurderet",
    ),
    CapstoneCopyKey.REPORT_TITLE: (
        "Plantilla interna del informe",
        "Internal report template",
        "Intern rapportskabelon",
    ),
    CapstoneCopyKey.REPORT_NOTICE: (
        "La única restricción pública confirmada es un máximo de diez páginas. La distribución "
        "siguiente es una propuesta de trabajo, no una estructura oficial.",
        "The only confirmed public restriction is a maximum of ten pages. The allocation below "
        "is a working proposal, not an official structure.",
        "Den eneste bekræftede offentlige begrænsning er højst ti sider. Fordelingen nedenfor er "
        "et arbejdsforslag og ikke en officiel struktur.",
    ),
    CapstoneCopyKey.REPORT_TEMPLATE: (
        "1. Portada y resumen ejecutivo — 0,5 páginas\n"
        "2. Problema, alcance y modelo — 1,5 páginas\n"
        "3. Diseño del programa y estructuras de datos — 1,5 páginas\n"
        "4. Implementación y decisiones de biblioteca — 2 páginas\n"
        "5. Estrategia de pruebas, resultados y depuración — 2 páginas\n"
        "6. Discusión, limitaciones y trabajo futuro — 1,5 páginas\n"
        "7. Conclusiones y contribuciones del grupo — 0,5 páginas\n\n"
        "Presupuesto sugerido: 9,5 páginas, dejando margen para ajustes.",
        "1. Cover and executive summary — 0.5 pages\n"
        "2. Problem, scope and model — 1.5 pages\n"
        "3. Program design and data structures — 1.5 pages\n"
        "4. Implementation and library decisions — 2 pages\n"
        "5. Testing strategy, results and debugging — 2 pages\n"
        "6. Discussion, limitations and future work — 1.5 pages\n"
        "7. Conclusions and group contributions — 0.5 pages\n\n"
        "Suggested budget: 9.5 pages, leaving room for adjustments.",
        "1. Forside og resumé — 0,5 sider\n"
        "2. Problem, afgrænsning og model — 1,5 sider\n"
        "3. Programdesign og datastrukturer — 1,5 sider\n"
        "4. Implementering og biblioteksvalg — 2 sider\n"
        "5. Teststrategi, resultater og fejlfinding — 2 sider\n"
        "6. Diskussion, begrænsninger og fremtidigt arbejde — 1,5 sider\n"
        "7. Konklusioner og gruppebidrag — 0,5 sider\n\n"
        "Foreslået budget: 9,5 sider med plads til justeringer.",
    ),
}

_MILESTONES: dict[str, LocalizedMilestoneCopy] = {
    "dm857.capstone.m01": (
        (
            "Hito 1 — Problema y modelo",
            "Convierte un problema concreto en un modelo programable y criterios de éxito verificables.",
            (
                "El problema, el alcance y los usuarios están definidos.",
                "El modelo identifica entradas, salidas, estados y restricciones.",
                "Los criterios de éxito pueden comprobarse con ejemplos o pruebas.",
            ),
        ),
        (
            "Milestone 1 — Problem and model",
            "Turn a concrete problem into a programmable model and verifiable success criteria.",
            (
                "The problem, scope and intended users are defined.",
                "The model identifies inputs, outputs, states and constraints.",
                "Success criteria can be checked with examples or tests.",
            ),
        ),
        (
            "Milepæl 1 — Problem og model",
            "Omsæt et konkret problem til en programmerbar model og verificerbare succeskriterier.",
            (
                "Problemet, afgrænsningen og de tilsigtede brugere er defineret.",
                "Modellen identificerer input, output, tilstande og begrænsninger.",
                "Succeskriterier kan kontrolleres med eksempler eller test.",
            ),
        ),
    ),
    "dm857.capstone.m02": (
        (
            "Hito 2 — Diseño del programa",
            "Descompón el modelo en componentes, contratos, datos y responsabilidades.",
            (
                "La estructura del programa está representada antes de implementar.",
                "Las estructuras de datos están justificadas.",
                "Las interfaces y responsabilidades tienen contratos claros.",
            ),
        ),
        (
            "Milestone 2 — Program design",
            "Decompose the model into components, contracts, data and responsibilities.",
            (
                "The program structure is represented before implementation.",
                "Data structures are justified.",
                "Interfaces and responsibilities have clear contracts.",
            ),
        ),
        (
            "Milepæl 2 — Programdesign",
            "Opdel modellen i komponenter, kontrakter, data og ansvar.",
            (
                "Programstrukturen er repræsenteret før implementering.",
                "Datastrukturerne er begrundet.",
                "Grænseflader og ansvar har tydelige kontrakter.",
            ),
        ),
    ),
    "dm857.capstone.m03": (
        (
            "Hito 3 — Implementación reproducible",
            "Implementa el diseño en Python y conserva evidencia versionada de las decisiones.",
            (
                "La implementación principal se ejecuta en un entorno documentado.",
                "Las bibliotecas utilizadas están justificadas y documentadas.",
                "El código y sus cambios relevantes están versionados.",
            ),
        ),
        (
            "Milestone 3 — Reproducible implementation",
            "Implement the design in Python and preserve versioned evidence of decisions.",
            (
                "The main implementation runs in a documented environment.",
                "Used libraries are justified and documented.",
                "Code and relevant changes are version controlled.",
            ),
        ),
        (
            "Milepæl 3 — Reproducerbar implementering",
            "Implementer designet i Python og bevar versionsstyret evidens for beslutninger.",
            (
                "Hovedimplementeringen kører i et dokumenteret miljø.",
                "Anvendte biblioteker er begrundet og dokumenteret.",
                "Kode og relevante ændringer er versionsstyret.",
            ),
        ),
    ),
    "dm857.capstone.m04": (
        (
            "Hito 4 — Pruebas y calidad",
            "Planifica, ejecuta e interpreta pruebas que cubran comportamiento normal y límites.",
            (
                "Existe un plan de pruebas vinculado a los criterios de éxito.",
                "Las pruebas fueron ejecutadas y sus resultados están registrados.",
                "Los fallos, correcciones y casos límite están analizados.",
            ),
        ),
        (
            "Milestone 4 — Testing and quality",
            "Plan, execute and interpret tests covering normal behaviour and boundaries.",
            (
                "A test plan is linked to the success criteria.",
                "Tests were executed and results were recorded.",
                "Failures, corrections and boundary cases are analysed.",
            ),
        ),
        (
            "Milepæl 4 — Test og kvalitet",
            "Planlæg, udfør og fortolk test af normal adfærd og grænsetilfælde.",
            (
                "En testplan er knyttet til succeskriterierne.",
                "Testene er udført, og resultaterne er registreret.",
                "Fejl, rettelser og grænsetilfælde er analyseret.",
            ),
        ),
    ),
    "dm857.capstone.m05": (
        (
            "Hito 5 — Informe trazable",
            "Conecta afirmaciones del informe con código, pruebas, resultados y contribuciones.",
            (
                "Las afirmaciones principales enlazan con evidencia verificable.",
                "Las limitaciones y decisiones alternativas están discutidas.",
                "El borrador respeta el máximo confirmado de diez páginas.",
            ),
        ),
        (
            "Milestone 5 — Traceable report",
            "Connect report claims to code, tests, results and group contributions.",
            (
                "Major claims link to verifiable evidence.",
                "Limitations and alternative decisions are discussed.",
                "The draft respects the confirmed maximum of ten pages.",
            ),
        ),
        (
            "Milepæl 5 — Sporbar rapport",
            "Forbind rapportens påstande med kode, test, resultater og gruppebidrag.",
            (
                "Vigtige påstande linker til verificerbar evidens.",
                "Begrænsninger og alternative beslutninger er diskuteret.",
                "Udkastet overholder det bekræftede maksimum på ti sider.",
            ),
        ),
    ),
}

_RUBRIC: dict[str, Triple] = {
    "dm857.capstone.r01": (
        "Modelo del problema y criterios de éxito",
        "Problem model and success criteria",
        "Problemmodel og succeskriterier",
    ),
    "dm857.capstone.r02": (
        "Arquitectura, contratos y estructuras de datos",
        "Architecture, contracts and data structures",
        "Arkitektur, kontrakter og datastrukturer",
    ),
    "dm857.capstone.r03": (
        "Implementación y uso razonado de bibliotecas",
        "Implementation and reasoned library use",
        "Implementering og begrundet biblioteksbrug",
    ),
    "dm857.capstone.r04": (
        "Diseño, ejecución e interpretación de pruebas",
        "Test design, execution and interpretation",
        "Testdesign, udførelse og fortolkning",
    ),
    "dm857.capstone.r05": (
        "Calidad, reproducibilidad y trazabilidad del código",
        "Code quality, reproducibility and traceability",
        "Kodekvalitet, reproducerbarhed og sporbarhed",
    ),
    "dm857.capstone.r06": (
        "Claridad y evidencia del informe",
        "Report clarity and evidence",
        "Rapportens klarhed og evidens",
    ),
    "dm857.capstone.r07": (
        "Registro de contribuciones del grupo",
        "Group contribution record",
        "Registrering af gruppebidrag",
    ),
}


def _select(values: Triple, locale: AppLocale) -> str:
    return values[_LOCALE_INDEX[locale]]


def capstone_text(locale: AppLocale, key: CapstoneCopyKey, **values: object) -> str:
    """Return one localized static string with strict placeholders."""

    template = _select(_STATIC[key], locale)
    required = {
        field_name for _, field_name, _, _ in Formatter().parse(template) if field_name is not None
    }
    if set(values) != required:
        raise ValueError(
            f"Capstone copy {key.value!r} requires {sorted(required)}, got {sorted(values)}."
        )
    return template.format(**values)


def capstone_milestone_copy(
    locale: AppLocale,
    milestone_id: str,
) -> MilestoneCopy:
    """Return title, description and checklist labels for one stable milestone."""

    return _MILESTONES[milestone_id][_LOCALE_INDEX[locale]]


def capstone_rubric_text(locale: AppLocale, criterion_id: str) -> str:
    """Return one localized internal rubric criterion."""

    return _select(_RUBRIC[criterion_id], locale)


def validate_capstone_copy() -> None:
    """Require complete keys, placeholders and authored identities in all locales."""

    if set(_STATIC) != set(CapstoneCopyKey):
        raise ValueError("The capstone static copy catalog is incomplete.")

    expected_milestones = {item.milestone_id for item in DM857_CAPSTONE_MILESTONES}
    if set(_MILESTONES) != expected_milestones:
        raise ValueError("The capstone milestone copy catalog is incomplete.")

    expected_rubric = {item.criterion_id for item in DM857_CAPSTONE_RUBRIC}
    if set(_RUBRIC) != expected_rubric:
        raise ValueError("The capstone rubric copy catalog is incomplete.")

    for key, localized in _STATIC.items():
        reference_fields: set[str] | None = None
        for template in localized:
            fields = {
                field_name
                for _, field_name, _, _ in Formatter().parse(template)
                if field_name is not None
            }
            if reference_fields is None:
                reference_fields = fields
            elif fields != reference_fields:
                raise ValueError(f"Capstone placeholder mismatch for {key.value!r}.")

    for spec in DM857_CAPSTONE_MILESTONES:
        for title, description, checklist in _MILESTONES[spec.milestone_id]:
            if not title.strip() or not description.strip():
                raise ValueError(f"Empty capstone copy for {spec.milestone_id!r}.")
            if len(checklist) != len(spec.checklist_item_ids):
                raise ValueError(f"Invalid checklist copy for {spec.milestone_id!r}.")
            if any(not item.strip() for item in checklist):
                raise ValueError(f"Empty checklist copy for {spec.milestone_id!r}.")


validate_capstone_copy()

__all__ = [
    "CapstoneCopyKey",
    "capstone_milestone_copy",
    "capstone_rubric_text",
    "capstone_text",
    "validate_capstone_copy",
]
