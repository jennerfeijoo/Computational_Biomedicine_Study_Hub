"""Strict Spanish, English and Danish copy for the DM847 writing studio."""

from __future__ import annotations

from enum import StrEnum
from string import Formatter

from ..learning.dm847_written_assessment import (
    DM847_WRITTEN_PROMPTS,
    WrittenTaskKind,
)
from .locales import AppLocale

Triple = tuple[str, str, str]
PromptCopy = tuple[str, str, tuple[str, ...]]
PromptTopic = tuple[Triple, Triple]

_LOCALE_INDEX = {
    AppLocale.SPANISH_SPAIN: 0,
    AppLocale.ENGLISH: 1,
    AppLocale.DANISH_DENMARK: 2,
}
_PROMPT_BY_ID = {item.prompt_id: item for item in DM847_WRITTEN_PROMPTS}


class WrittenAssessmentCopyKey(StrEnum):
    """Stable interface-copy identities for written assessment support."""

    TITLE = "written.title"
    INTRO = "written.intro"
    MODULE = "written.module"
    TASK = "written.task"
    TASK_KIND = "written.task_kind"
    OPEN_RESPONSE = "written.open_response"
    ESSAY = "written.essay"
    OBJECTIVES = "written.objectives"
    FOCUS = "written.focus"
    DRAFT = "written.draft"
    DRAFT_PLACEHOLDER = "written.draft_placeholder"
    WORD_COUNT = "written.word_count"
    SAVE = "written.save"
    SAVED = "written.saved"
    FEEDBACK_TITLE = "written.feedback_title"
    FEEDBACK_NOTICE = "written.feedback_notice"
    CONTENT_REVIEW = "written.content_review"
    WRITING_REVISION = "written.writing_revision"
    ESSAY_COACH = "written.essay_coach"
    GENERATING = "written.generating"
    CANCEL = "written.cancel"
    SOURCES = "written.sources"
    MODEL = "written.model"
    EMPTY_DRAFT = "written.empty_draft"
    TOO_SHORT = "written.too_short"
    NO_FEEDBACK = "written.no_feedback"
    FEEDBACK_STALE = "written.feedback_stale"
    REQUEST_FAILED = "written.request_failed"
    TAB_DM847 = "written.tab_dm847"
    TAB_DM857 = "written.tab_dm857"


_STATIC: dict[WrittenAssessmentCopyKey, Triple] = {
    WrittenAssessmentCopyKey.TITLE: (
        "DM847: respuestas abiertas y ensayos",
        "DM847: open responses and essays",
        "DM847: åbne svar og essays",
    ),
    WrittenAssessmentCopyKey.INTRO: (
        "Redacta una respuesta propia y utiliza Ollama para revisar precisión científica, mejorar "
        "la redacción o desarrollar un ensayo. La retroalimentación se limita al contenido "
        "autorizado del módulo y no constituye una calificación oficial.",
        "Write your own response and use Ollama to review scientific accuracy, improve the "
        "writing, or develop an essay. Feedback is restricted to authorised module content and "
        "is not an official grade.",
        "Skriv dit eget svar, og brug Ollama til at gennemgå den videnskabelige præcision, "
        "forbedre formuleringen eller udvikle et essay. Feedback er begrænset til modulets "
        "autoriserede indhold og er ikke en officiel karakter.",
    ),
    WrittenAssessmentCopyKey.MODULE: ("Módulo", "Module", "Modul"),
    WrittenAssessmentCopyKey.TASK: ("Pregunta", "Task", "Opgave"),
    WrittenAssessmentCopyKey.TASK_KIND: ("Formato", "Format", "Format"),
    WrittenAssessmentCopyKey.OPEN_RESPONSE: (
        "Respuesta abierta",
        "Open response",
        "Åbent svar",
    ),
    WrittenAssessmentCopyKey.ESSAY: ("Ensayo", "Essay", "Essay"),
    WrittenAssessmentCopyKey.OBJECTIVES: (
        "Objetivos vinculados: {objectives}",
        "Linked objectives: {objectives}",
        "Tilknyttede læringsmål: {objectives}",
    ),
    WrittenAssessmentCopyKey.FOCUS: (
        "La respuesta debe cubrir",
        "The response should cover",
        "Svaret bør dække",
    ),
    WrittenAssessmentCopyKey.DRAFT: ("Tu borrador", "Your draft", "Dit udkast"),
    WrittenAssessmentCopyKey.DRAFT_PLACEHOLDER: (
        "Escribe primero tu razonamiento. Incluye supuestos, evidencia, limitaciones y decisiones "
        "metodológicas cuando sean pertinentes.",
        "Write your reasoning first. Include assumptions, evidence, limitations, and "
        "methodological decisions where relevant.",
        "Skriv først din argumentation. Medtag antagelser, evidens, begrænsninger og metodiske "
        "beslutninger, hvor det er relevant.",
    ),
    WrittenAssessmentCopyKey.WORD_COUNT: (
        "{words} palabras",
        "{words} words",
        "{words} ord",
    ),
    WrittenAssessmentCopyKey.SAVE: (
        "Guardar borrador",
        "Save draft",
        "Gem udkast",
    ),
    WrittenAssessmentCopyKey.SAVED: (
        "Borrador guardado localmente.",
        "Draft saved locally.",
        "Udkast gemt lokalt.",
    ),
    WrittenAssessmentCopyKey.FEEDBACK_TITLE: (
        "Asistencia local con Ollama",
        "Local Ollama support",
        "Lokal Ollama-støtte",
    ),
    WrittenAssessmentCopyKey.FEEDBACK_NOTICE: (
        "Ollama puede detectar omisiones o proponer una revisión, pero puede equivocarse. Verifica "
        "cada afirmación con el módulo. La aplicación no registra la respuesta como correcta ni "
        "modifica automáticamente tu progreso.",
        "Ollama can detect omissions or suggest a revision, but it may be wrong. Verify every "
        "claim against the module. The application does not record the response as correct or "
        "automatically change your progress.",
        "Ollama kan opdage udeladelser eller foreslå en revision, men modellen kan tage fejl. "
        "Kontrollér hver påstand mod modulet. Applikationen registrerer ikke svaret som korrekt og "
        "ændrer ikke automatisk dine fremskridt.",
    ),
    WrittenAssessmentCopyKey.CONTENT_REVIEW: (
        "Revisar contenido",
        "Review content",
        "Gennemgå indhold",
    ),
    WrittenAssessmentCopyKey.WRITING_REVISION: (
        "Mejorar redacción",
        "Improve writing",
        "Forbedr formulering",
    ),
    WrittenAssessmentCopyKey.ESSAY_COACH: (
        "Desarrollar ensayo",
        "Develop essay",
        "Udvikl essay",
    ),
    WrittenAssessmentCopyKey.GENERATING: (
        "Ollama está analizando el borrador…",
        "Ollama is analysing the draft…",
        "Ollama analyserer udkastet…",
    ),
    WrittenAssessmentCopyKey.CANCEL: ("Cancelar", "Cancel", "Annuller"),
    WrittenAssessmentCopyKey.SOURCES: (
        "Fuentes internas utilizadas",
        "Internal sources used",
        "Anvendte interne kilder",
    ),
    WrittenAssessmentCopyKey.MODEL: (
        "Modelo local: {model}",
        "Local model: {model}",
        "Lokal model: {model}",
    ),
    WrittenAssessmentCopyKey.EMPTY_DRAFT: (
        "Escribe una respuesta antes de solicitar retroalimentación.",
        "Write a response before requesting feedback.",
        "Skriv et svar, før du anmoder om feedback.",
    ),
    WrittenAssessmentCopyKey.TOO_SHORT: (
        "El borrador necesita al menos 40 palabras para una revisión útil.",
        "The draft needs at least 40 words for a useful review.",
        "Udkastet skal indeholde mindst 40 ord for at give en nyttig gennemgang.",
    ),
    WrittenAssessmentCopyKey.NO_FEEDBACK: (
        "Todavía no hay retroalimentación para este borrador.",
        "There is no feedback for this draft yet.",
        "Der er endnu ingen feedback til dette udkast.",
    ),
    WrittenAssessmentCopyKey.FEEDBACK_STALE: (
        "El borrador cambió. La retroalimentación anterior se eliminó para no asociarla con un "
        "texto diferente.",
        "The draft changed. Previous feedback was removed so it is not associated with different "
        "text.",
        "Udkastet blev ændret. Tidligere feedback blev fjernet, så den ikke forbindes med en anden "
        "tekst.",
    ),
    WrittenAssessmentCopyKey.REQUEST_FAILED: (
        "No se pudo obtener retroalimentación: {message}",
        "Feedback could not be generated: {message}",
        "Feedback kunne ikke genereres: {message}",
    ),
    WrittenAssessmentCopyKey.TAB_DM847: (
        "DM847 · Escritura",
        "DM847 · Writing",
        "DM847 · Skrivning",
    ),
    WrittenAssessmentCopyKey.TAB_DM857: (
        "DM857 · Proyecto",
        "DM857 · Project",
        "DM857 · Projekt",
    ),
}

_PROMPT_TOPICS: dict[str, PromptTopic] = {
    "dm847.w01": (
        (
            "Información molecular y contexto",
            "Molecular information and context",
            "Molekylær information og kontekst",
        ),
        (
            "Explica cómo representarías lecturas ambiguas y anotaciones procedentes de distintos "
            "sistemas de coordenadas sin perder alfabeto, orientación, procedencia, incertidumbre "
            "ni validación de las conversiones.",
            "Explain how you would represent ambiguous reads and annotations from different "
            "coordinate systems without losing alphabet, orientation, provenance, uncertainty, or "
            "validation of the conversions.",
            "Forklar, hvordan du vil repræsentere tvetydige reads og annotationer fra forskellige "
            "koordinatsystemer uden at miste alfabet, orientering, proveniens, usikkerhed eller "
            "validering af konverteringerne.",
        ),
    ),
    "dm847.w02": (
        (
            "Consultas y ontologías reproducibles",
            "Reproducible queries and ontologies",
            "Reproducerbare forespørgsler og ontologier",
        ),
        (
            "Diseña una consulta reproducible de genes relacionados con una enfermedad que integre "
            "varias bases de datos, identificadores, versiones, relaciones ontológicas y evidencia "
            "contradictoria.",
            "Design a reproducible disease-gene query that integrates several databases, "
            "identifiers, versions, ontology relations, and conflicting evidence.",
            "Design en reproducerbar forespørgsel efter sygdomsrelaterede gener, der integrerer "
            "flere databaser, identifikatorer, versioner, ontologiske relationer og modstridende "
            "evidens.",
        ),
    ),
    "dm847.w03": (
        (
            "Puntuaciones y coincidencias de secuencia",
            "Sequence scores and matches",
            "Sekvensscores og matches",
        ),
        (
            "Compara estrategias para detectar similitud entre secuencias cortas y justifica el "
            "esquema de puntuación, modelo de fondo, umbral y separación entre azar, significación "
            "estadística e interpretación biológica.",
            "Compare strategies for detecting similarity between short sequences and justify the "
            "scoring scheme, background model, threshold, and separation of chance, statistical "
            "significance, and biological interpretation.",
            "Sammenlign strategier til at opdage lighed mellem korte sekvenser, og begrund "
            "scoringsskema, baggrundsmodel, tærskel og adskillelsen mellem tilfældighed, statistisk "
            "signifikans og biologisk fortolkning.",
        ),
    ),
    "dm847.w04": (
        (
            "Elección de alineamiento por pares",
            "Choosing a pairwise alignment",
            "Valg af parvis alignment",
        ),
        (
            "Dos proteínas comparten un dominio pero difieren en longitud y baja complejidad. "
            "Defiende un alineamiento global, local o semiglobal, sus parámetros y los límites de "
            "las conclusiones biológicas.",
            "Two proteins share a domain but differ in length and low complexity. Defend a global, "
            "local, or semiglobal alignment, its parameters, and the limits of the biological "
            "conclusions.",
            "To proteiner deler et domæne, men adskiller sig i længde og lav kompleksitet. Forsvar "
            "en global, lokal eller semiglobal alignment, dens parametre og grænserne for de "
            "biologiske konklusioner.",
        ),
    ),
    "dm847.w05": (
        (
            "HMM y supuestos biológicos",
            "HMMs and biological assumptions",
            "HMM'er og biologiske antagelser",
        ),
        (
            "Analiza cómo un modelo oculto de Markov convierte una hipótesis biológica en estados, "
            "emisiones y transiciones, incluyendo entrenamiento, decodificación, identificabilidad, "
            "validación y riesgos interpretativos.",
            "Analyse how a hidden Markov model turns a biological hypothesis into states, "
            "emissions, and transitions, including training, decoding, identifiability, validation, "
            "and interpretive risks.",
            "Analysér, hvordan en skjult Markov-model omsætter en biologisk hypotese til tilstande, "
            "emissioner og transitioner, herunder træning, dekodning, identificerbarhed, validering "
            "og fortolkningsrisici.",
        ),
    ),
    "dm847.w06": (
        (
            "Índices de secuencia y mapeo incierto",
            "Sequence indexes and uncertain mapping",
            "Sekvensindekser og usikker mapping",
        ),
        (
            "Explica cómo suffix array, BWT y FM-index permiten buscar patrones y cómo un flujo "
            "seed-and-extend debe representar mismatches, multimapping y calidad sin inventar una "
            "coordenada única.",
            "Explain how a suffix array, BWT, and FM-index support pattern search and how a "
            "seed-and-extend workflow should represent mismatches, multimapping, and quality "
            "without inventing a unique coordinate.",
            "Forklar, hvordan suffix array, BWT og FM-index understøtter mønstersøgning, og hvordan "
            "et seed-and-extend-forløb bør repræsentere mismatches, multimapping og kvalitet uden at "
            "opfinde en entydig koordinat.",
        ),
    ),
    "dm847.w07": (
        (
            "Organización bacteriana y evidencia",
            "Bacterial organisation and evidence",
            "Bakteriel organisering og evidens",
        ),
        (
            "Integra proximidad genómica, orientación, RNA-seq y anotaciones para evaluar un posible "
            "operón, proponer evidencia adicional y distinguir regulación compartida, transferencia "
            "horizontal y coincidencia contextual.",
            "Integrate genomic proximity, orientation, RNA-seq, and annotations to assess a possible "
            "operon, propose additional evidence, and distinguish shared regulation, horizontal "
            "transfer, and contextual coincidence.",
            "Integrér genomisk nærhed, orientering, RNA-seq og annotationer for at vurdere et muligt "
            "operon, foreslå yderligere evidens og skelne fælles regulering, horisontal overførsel og "
            "kontekstuel tilfældighed.",
        ),
    ),
    "dm847.w08": (
        (
            "Descubrimiento y validación de motivos",
            "Motif discovery and validation",
            "Motivopdagelse og validering",
        ),
        (
            "Evalúa críticamente un análisis de motivos con PWM y EM: modelo de fondo, "
            "pseudoconteos, ocurrencia, inicializaciones, anchura, óptimos locales, estabilidad y "
            "validación funcional independiente.",
            "Critically evaluate a PWM- and EM-based motif analysis: background model, pseudocounts, "
            "occurrence model, initialisations, width, local optima, stability, and independent "
            "functional validation.",
            "Vurdér kritisk en motivanalyse baseret på PWM og EM: baggrundsmodel, pseudotællinger, "
            "forekomstmodel, initialiseringer, bredde, lokale optima, stabilitet og uafhængig "
            "funktionel validering.",
        ),
    ),
    "dm847.w09": (
        (
            "Redes y enriquecimiento",
            "Networks and enrichment",
            "Netværk og berigelse",
        ),
        (
            "Diseña un análisis de módulos de red y términos enriquecidos que controle universo de "
            "referencia, dependencia, múltiples pruebas, robustez y sesgo de anotación sin convertir "
            "asociaciones en mecanismos causales.",
            "Design an analysis of network modules and enriched terms that controls the reference "
            "universe, dependence, multiple testing, robustness, and annotation bias without turning "
            "associations into causal mechanisms.",
            "Design en analyse af netværksmoduler og berigede termer, der kontrollerer "
            "referenceunivers, afhængighed, multiple test, robusthed og annotationsbias uden at gøre "
            "associationer til kausale mekanismer.",
        ),
    ),
    "dm847.w10": (
        (
            "Estudio ómico predictivo sin fuga",
            "Leakage-free predictive omics study",
            "Prædiktivt omikstudie uden leakage",
        ),
        (
            "Diseña un estudio ómico predictivo con unidad experimental, outcome, preprocesamiento, "
            "splits agrupados, validación anidada, métricas, calibración, análisis de errores, "
            "limitaciones y artefactos reproducibles.",
            "Design a predictive omics study with an experimental unit, outcome, preprocessing, "
            "grouped splits, nested validation, metrics, calibration, error analysis, limitations, "
            "and reproducible artefacts.",
            "Design et prædiktivt omikstudie med eksperimentel enhed, outcome, preprocessing, "
            "grupperede splits, nested validering, metrikker, kalibrering, fejlanalyse, begrænsninger "
            "og reproducerbare artefakter.",
        ),
    ),
}

_OPEN_FOCUS: tuple[Triple, ...] = (
    (
        "supuestos y representaciones explícitos",
        "explicit assumptions and representations",
        "eksplicitte antagelser og repræsentationer",
    ),
    (
        "elección y justificación del método",
        "choice and justification of method",
        "valg og begrundelse af metode",
    ),
    (
        "evidencia y estrategia de validación",
        "evidence and validation strategy",
        "evidens og valideringsstrategi",
    ),
    (
        "incertidumbre, alternativas y limitaciones",
        "uncertainty, alternatives, and limitations",
        "usikkerhed, alternativer og begrænsninger",
    ),
)
_ESSAY_FOCUS: tuple[Triple, ...] = (
    (
        "tesis o posición central claramente formulada",
        "a clearly stated thesis or central position",
        "en klart formuleret tese eller central position",
    ),
    (
        "argumento organizado con conceptos del módulo",
        "an organised argument using module concepts",
        "en organiseret argumentation med modulets begreber",
    ),
    (
        "evidencia, validación y contraargumentos",
        "evidence, validation, and counterarguments",
        "evidens, validering og modargumenter",
    ),
    (
        "limitaciones y conclusiones proporcionales",
        "limitations and proportionate conclusions",
        "begrænsninger og proportionale konklusioner",
    ),
)


def written_assessment_text(
    locale: AppLocale,
    key: WrittenAssessmentCopyKey,
    **values: object,
) -> str:
    """Return one localized interface string with strict placeholders."""

    template = _STATIC[key][_LOCALE_INDEX[locale]]
    required = {
        field_name for _, field_name, _, _ in Formatter().parse(template) if field_name is not None
    }
    if set(values) != required:
        raise ValueError(
            f"Written-assessment copy {key.value!r} requires {sorted(required)}, "
            f"got {sorted(values)}."
        )
    return template.format(**values)


def written_prompt_copy(locale: AppLocale, prompt_id: str) -> PromptCopy:
    """Return localized title, task, and focus points for one stable prompt."""

    index = _LOCALE_INDEX[locale]
    title, task = _PROMPT_TOPICS[prompt_id]
    focus_catalog = (
        _ESSAY_FOCUS
        if _PROMPT_BY_ID[prompt_id].kind is WrittenTaskKind.ESSAY
        else _OPEN_FOCUS
    )
    return title[index], task[index], tuple(item[index] for item in focus_catalog)


def validate_written_assessment_copy() -> None:
    """Require complete static and authored prompt copy in every locale."""

    if set(_STATIC) != set(WrittenAssessmentCopyKey):
        raise ValueError("Written-assessment static copy is incomplete.")
    expected_prompts = {item.prompt_id for item in DM847_WRITTEN_PROMPTS}
    if set(_PROMPT_TOPICS) != expected_prompts:
        raise ValueError("Written-assessment prompt copy does not match the authored catalog.")
    for prompt_id in expected_prompts:
        for locale in _LOCALE_INDEX:
            title, task, focus = written_prompt_copy(locale, prompt_id)
            if not title.strip() or not task.strip() or not focus:
                raise ValueError(f"Prompt {prompt_id!r} contains incomplete localized copy.")
            if any(not item.strip() for item in focus):
                raise ValueError(f"Prompt {prompt_id!r} contains an empty focus point.")


validate_written_assessment_copy()

__all__ = [
    "WrittenAssessmentCopyKey",
    "validate_written_assessment_copy",
    "written_assessment_text",
    "written_prompt_copy",
]
