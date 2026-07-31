"""Strict Spanish, English and Danish copy for the DM847 writing studio."""

from __future__ import annotations

from enum import StrEnum
from string import Formatter

from ..learning.dm847_written_assessment import DM847_WRITTEN_PROMPTS
from .locales import AppLocale

Triple = tuple[str, str, str]
PromptCopy = tuple[str, str, tuple[str, ...]]
LocalizedPromptCopy = tuple[PromptCopy, PromptCopy, PromptCopy]

_LOCALE_INDEX = {
    AppLocale.SPANISH_SPAIN: 0,
    AppLocale.ENGLISH: 1,
    AppLocale.DANISH_DENMARK: 2,
}


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
        "Redacta una respuesta propia y utiliza Ollama para revisar precisión científica, mejorar la redacción o desarrollar una estructura de ensayo. La retroalimentación se limita al contenido autorizado del módulo y no constituye una calificación oficial.",
        "Write your own response and use Ollama to review scientific accuracy, improve the writing, or develop an essay structure. Feedback is restricted to authorised module content and is not an official grade.",
        "Skriv dit eget svar, og brug Ollama til at gennemgå den videnskabelige præcision, forbedre formuleringen eller udvikle en essaystruktur. Feedback er begrænset til modulets autoriserede indhold og er ikke en officiel karakter.",
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
    WrittenAssessmentCopyKey.DRAFT: (
        "Tu borrador",
        "Your draft",
        "Dit udkast",
    ),
    WrittenAssessmentCopyKey.DRAFT_PLACEHOLDER: (
        "Escribe primero tu razonamiento. Incluye supuestos, evidencia, limitaciones y decisiones metodológicas cuando sean pertinentes.",
        "Write your reasoning first. Include assumptions, evidence, limitations, and methodological decisions where relevant.",
        "Skriv først din argumentation. Medtag antagelser, evidens, begrænsninger og metodiske beslutninger, hvor det er relevant.",
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
        "Ollama puede detectar omisiones o proponer una revisión, pero puede equivocarse. Verifica cada afirmación con el contenido del módulo. La aplicación no registra esta respuesta como correcta ni modifica automáticamente tu progreso.",
        "Ollama can detect omissions or suggest a revision, but it may be wrong. Verify every claim against the module content. The application does not record this response as correct or automatically change your progress.",
        "Ollama kan opdage udeladelser eller foreslå en revision, men modellen kan tage fejl. Kontrollér hver påstand mod modulets indhold. Applikationen registrerer ikke svaret som korrekt og ændrer ikke automatisk dine fremskridt.",
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
        "El borrador cambió. La retroalimentación anterior se eliminó para evitar asociarla con un texto diferente.",
        "The draft changed. Previous feedback was removed so it is not associated with different text.",
        "Udkastet blev ændret. Tidligere feedback blev fjernet, så den ikke forbindes med en anden tekst.",
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

_PROMPTS: dict[str, LocalizedPromptCopy] = {
    "dm847.w01": (
        (
            "Representar información molecular sin perder contexto",
            "Una muestra contiene lecturas con símbolos ambiguos y anotaciones procedentes de sistemas de coordenadas distintos. Explica cómo construirías una representación computable que conserve alfabeto, orientación, coordenadas, procedencia e incertidumbre, y cómo validarías las conversiones.",
            (
                "diferencia entre secuencia, anotación y señal experimental",
                "política explícita para símbolos ambiguos y orientación",
                "conversión y prueba de coordenadas sin errores de borde",
                "procedencia y validación de la representación",
            ),
        ),
        (
            "Represent molecular information without losing context",
            "A sample contains reads with ambiguous symbols and annotations from different coordinate systems. Explain how you would build a computable representation that preserves alphabet, orientation, coordinates, provenance, and uncertainty, and how you would validate the conversions.",
            (
                "distinction between sequence, annotation, and experimental signal",
                "explicit policy for ambiguous symbols and orientation",
                "tested coordinate conversion without boundary errors",
                "provenance and validation of the representation",
            ),
        ),
        (
            "Repræsentér molekylær information uden at miste kontekst",
            "En prøve indeholder reads med tvetydige symboler og annotationer fra forskellige koordinatsystemer. Forklar, hvordan du vil opbygge en beregnelig repræsentation, der bevarer alfabet, orientering, koordinater, proveniens og usikkerhed, og hvordan konverteringerne skal valideres.",
            (
                "forskel mellem sekvens, annotation og eksperimentelt signal",
                "eksplicit politik for tvetydige symboler og orientering",
                "testet koordinatkonvertering uden grænsefejl",
                "proveniens og validering af repræsentationen",
            ),
        ),
    ),
    "dm847.w02": (
        (
            "Diseñar una consulta bioinformática reproducible",
            "Debes recuperar genes relacionados con una enfermedad desde varias bases de datos y ontologías. Describe una estrategia reproducible que gestione identificadores, versiones, evidencia, relaciones ontológicas y resultados contradictorios.",
            (
                "identificadores estables y mapeos entre recursos",
                "versiones, fechas y procedencia de cada consulta",
                "uso correcto de jerarquías y relaciones ontológicas",
                "manejo explícito de evidencia conflictiva y datos ausentes",
            ),
        ),
        (
            "Design a reproducible bioinformatics query",
            "You must retrieve disease-related genes from several databases and ontologies. Describe a reproducible strategy that manages identifiers, versions, evidence, ontology relations, and conflicting results.",
            (
                "stable identifiers and mappings across resources",
                "versions, dates, and provenance for each query",
                "correct use of ontology hierarchies and relations",
                "explicit handling of conflicting evidence and missing data",
            ),
        ),
        (
            "Design en reproducerbar bioinformatisk forespørgsel",
            "Du skal hente sygdomsrelaterede gener fra flere databaser og ontologier. Beskriv en reproducerbar strategi, der håndterer identifikatorer, versioner, evidens, ontologiske relationer og modstridende resultater.",
            (
                "stabile identifikatorer og mapping mellem ressourcer",
                "versioner, datoer og proveniens for hver forespørgsel",
                "korrekt brug af ontologiske hierarkier og relationer",
                "eksplicit håndtering af modstridende evidens og manglende data",
            ),
        ),
    ),
    "dm847.w03": (
        (
            "Interpretar puntuaciones de secuencia y coincidencias",
            "Compara dos estrategias para detectar similitud entre secuencias cortas. Explica cómo elegirías el esquema de puntuación, el modelo de fondo y el umbral, y cómo distinguirías una coincidencia biológicamente informativa de una coincidencia esperable por azar.",
            (
                "supuestos del alfabeto, sustituciones y modelo de fondo",
                "relación entre score, longitud y frecuencia esperada",
                "control de múltiples búsquedas o candidatos",
                "separación entre significación estadística e interpretación biológica",
            ),
        ),
        (
            "Interpret sequence scores and matches",
            "Compare two strategies for detecting similarity between short sequences. Explain how you would choose the scoring scheme, background model, and threshold, and how you would distinguish a biologically informative match from one expected by chance.",
            (
                "assumptions about alphabet, substitutions, and background model",
                "relationship between score, length, and expected frequency",
                "control for multiple searches or candidates",
                "separation of statistical significance from biological interpretation",
            ),
        ),
        (
            "Fortolk sekvensscores og matches",
            "Sammenlign to strategier til at opdage lighed mellem korte sekvenser. Forklar, hvordan du vil vælge scoringsskema, baggrundsmodel og tærskel, og hvordan du vil skelne et biologisk informativt match fra et match, der forventes ved tilfældighed.",
            (
                "antagelser om alfabet, substitutioner og baggrundsmodel",
                "forhold mellem score, længde og forventet frekvens",
                "kontrol for flere søgninger eller kandidater",
                "adskillelse af statistisk signifikans og biologisk fortolkning",
            ),
        ),
    ),
    "dm847.w04": (
        (
            "Elegir y defender un alineamiento por pares",
            "Dos proteínas comparten un dominio conservado, pero difieren en longitud y contienen regiones de baja complejidad. Defiende la elección entre alineamiento global, local o semiglobal; justifica sustituciones y penalizaciones de gaps; y explica qué conclusiones no pueden extraerse del alineamiento.",
            (
                "elección del tipo de alineamiento según la pregunta",
                "efecto de matriz de sustitución y penalizaciones de gaps",
                "tratamiento de baja complejidad y alineamientos alternativos",
                "límites entre similitud, homología, función y causalidad",
            ),
        ),
        (
            "Choose and defend a pairwise alignment",
            "Two proteins share a conserved domain but differ in length and contain low-complexity regions. Defend the choice of global, local, or semiglobal alignment; justify substitutions and gap penalties; and explain which conclusions cannot be drawn from the alignment.",
            (
                "choice of alignment type according to the question",
                "effect of substitution matrix and gap penalties",
                "handling of low complexity and alternative alignments",
                "limits between similarity, homology, function, and causality",
            ),
        ),
        (
            "Vælg og forsvar en parvis alignment",
            "To proteiner deler et konserveret domæne, men har forskellig længde og indeholder lavkomplekse regioner. Forsvar valget mellem global, lokal eller semiglobal alignment; begrund substitutioner og gap-straffe; og forklar, hvilke konklusioner der ikke kan drages af alignmenten.",
            (
                "valg af alignmenttype ud fra spørgsmålet",
                "effekt af substitutionsmatrix og gap-straffe",
                "håndtering af lav kompleksitet og alternative alignments",
                "grænser mellem lighed, homologi, funktion og kausalitet",
            ),
        ),
    ),
    "dm847.w05": (
        (
            "Ensayo: modelos ocultos y supuestos biológicos",
            "Redacta un ensayo que explique cómo un modelo oculto de Markov transforma una hipótesis biológica en estados, emisiones y transiciones. Analiza identificabilidad, entrenamiento, decodificación, validación y riesgos de interpretar los estados como entidades biológicas reales.",
            (
                "correspondencia razonada entre hipótesis y componentes del HMM",
                "diferencia entre evaluación, decodificación y aprendizaje",
                "supuestos de independencia, duración e identificabilidad",
                "validación y límites de la interpretación biológica",
            ),
        ),
        (
            "Essay: hidden models and biological assumptions",
            "Write an essay explaining how a hidden Markov model turns a biological hypothesis into states, emissions, and transitions. Analyse identifiability, training, decoding, validation, and the risks of interpreting states as real biological entities.",
            (
                "reasoned mapping between hypothesis and HMM components",
                "difference between evaluation, decoding, and learning",
                "independence, duration, and identifiability assumptions",
                "validation and limits of biological interpretation",
            ),
        ),
        (
            "Essay: skjulte modeller og biologiske antagelser",
            "Skriv et essay, der forklarer, hvordan en skjult Markov-model omsætter en biologisk hypotese til tilstande, emissioner og transitioner. Analysér identificerbarhed, træning, dekodning, validering og risikoen ved at fortolke tilstande som virkelige biologiske enheder.",
            (
                "begrundet mapping mellem hypotese og HMM-komponenter",
                "forskel mellem evaluering, dekodning og læring",
                "antagelser om uafhængighed, varighed og identificerbarhed",
                "validering og grænser for biologisk fortolkning",
            ),
        ),
    ),
    "dm847.w06": (
        (
            "Explicar un índice de secuencias y la incertidumbre del mapeo",
            "Explica cómo suffix array, BWT y FM-index permiten buscar patrones sin almacenar todos los sufijos como texto. Después describe un flujo seed-and-extend y cómo reportarías multimapping, mismatches y calidad del mapeo sin inventar una coordenada única.",
            (
                "qué almacena cada estructura y papel del centinela",
                "backward search y diferencia entre count y locate",
                "verificación de candidatos en seed-and-extend",
                "representación explícita de multimapping e incertidumbre",
            ),
        ),
        (
            "Explain a sequence index and mapping uncertainty",
            "Explain how a suffix array, BWT, and FM-index support pattern search without storing every suffix as text. Then describe a seed-and-extend workflow and how you would report multimapping, mismatches, and mapping quality without inventing a unique coordinate.",
            (
                "what each structure stores and the role of the sentinel",
                "backward search and the distinction between count and locate",
                "candidate verification in seed-and-extend",
                "explicit representation of multimapping and uncertainty",
            ),
        ),
        (
            "Forklar et sekvensindeks og mapping-usikkerhed",
            "Forklar, hvordan suffix array, BWT og FM-index muliggør mønstersøgning uden at lagre alle suffikser som tekst. Beskriv derefter et seed-and-extend-forløb, og hvordan du vil rapportere multimapping, mismatches og mapping-kvalitet uden at opfinde en entydig koordinat.",
            (
                "hvad hver struktur lagrer og sentinelens rolle",
                "backward search og forskellen mellem count og locate",
                "verifikation af kandidater i seed-and-extend",
                "eksplicit repræsentation af multimapping og usikkerhed",
            ),
        ),
    ),
    "dm847.w07": (
        (
            "Inferir organización bacteriana sin sobrerinterpretar",
            "Dispones de proximidad genómica, orientación, RNA-seq y anotaciones funcionales para varios genes bacterianos. Explica cómo evaluarías si forman un operón, qué evidencia adicional buscarías y cómo distinguirías regulación compartida, transferencia horizontal y coincidencia contextual.",
            (
                "integración de evidencia genómica, transcripcional y funcional",
                "predicciones contrastables y evidencia independiente",
                "alternativas como promotores internos o terminación parcial",
                "incertidumbre, transferencia horizontal y límites de causalidad",
            ),
        ),
        (
            "Infer bacterial organisation without overinterpretation",
            "You have genomic proximity, orientation, RNA-seq, and functional annotations for several bacterial genes. Explain how you would assess whether they form an operon, which additional evidence you would seek, and how you would distinguish shared regulation, horizontal transfer, and contextual coincidence.",
            (
                "integration of genomic, transcriptomic, and functional evidence",
                "testable predictions and independent evidence",
                "alternatives such as internal promoters or partial termination",
                "uncertainty, horizontal transfer, and causal limits",
            ),
        ),
        (
            "Udled bakteriel organisering uden overfortolkning",
            "Du har genomisk nærhed, orientering, RNA-seq og funktionelle annotationer for flere bakterielle gener. Forklar, hvordan du vil vurdere, om de danner et operon, hvilken yderligere evidens du vil søge, og hvordan du vil skelne fælles regulering, horisontal overførsel og kontekstuel tilfældighed.",
            (
                "integration af genomisk, transkriptomisk og funktionel evidens",
                "testbare forudsigelser og uafhængig evidens",
                "alternativer som interne promotorer eller delvis terminering",
                "usikkerhed, horisontal overførsel og kausale grænser",
            ),
        ),
    ),
    "dm847.w08": (
        (
            "Ensayo: descubrimiento de motivos y validación",
            "Redacta un ensayo crítico sobre un análisis de motivos basado en PWM y EM. Explica el modelo de fondo, pseudoconteos, modelo de ocurrencia, inicializaciones, selección de anchura, óptimos locales y validación independiente. Discute por qué un logo no demuestra función.",
            (
                "construcción e interpretación de PWM y log-odds",
                "supuestos del fondo y del modelo de ocurrencia",
                "inicializaciones, óptimos locales y estabilidad",
                "validación retenida y evidencia funcional externa",
            ),
        ),
        (
            "Essay: motif discovery and validation",
            "Write a critical essay about a PWM- and EM-based motif analysis. Explain the background model, pseudocounts, occurrence model, initialisations, width selection, local optima, and independent validation. Discuss why a sequence logo does not demonstrate function.",
            (
                "construction and interpretation of PWM and log odds",
                "background and occurrence-model assumptions",
                "initialisations, local optima, and stability",
                "held-out validation and external functional evidence",
            ),
        ),
        (
            "Essay: motivopdagelse og validering",
            "Skriv et kritisk essay om en motivanalyse baseret på PWM og EM. Forklar baggrundsmodel, pseudotællinger, forekomstmodel, initialiseringer, valg af bredde, lokale optima og uafhængig validering. Diskutér, hvorfor et sekvenslogo ikke dokumenterer funktion.",
            (
                "konstruktion og fortolkning af PWM og log-odds",
                "antagelser om baggrund og forekomstmodel",
                "initialiseringer, lokale optima og stabilitet",
                "hold-out-validering og ekstern funktionel evidens",
            ),
        ),
    ),
    "dm847.w09": (
        (
            "Evaluar una red y un análisis de enriquecimiento",
            "Un conjunto de genes diferencialmente expresados produce módulos de red y términos enriquecidos. Explica un análisis que controle el universo de referencia, dependencia, múltiples pruebas y sesgos de anotación, y que evite convertir asociaciones de red en mecanismos causales.",
            (
                "definición adecuada del universo y de la unidad analítica",
                "control de múltiples pruebas y dependencia entre términos",
                "robustez de módulos, centralidad y sesgos de anotación",
                "separación entre asociación, prioridad experimental y causalidad",
            ),
        ),
        (
            "Evaluate a network and enrichment analysis",
            "A set of differentially expressed genes produces network modules and enriched terms. Explain an analysis that controls the reference universe, dependence, multiple testing, and annotation bias, while avoiding conversion of network associations into causal mechanisms.",
            (
                "appropriate definition of universe and analytical unit",
                "multiple-testing control and dependence among terms",
                "robustness of modules, centrality, and annotation bias",
                "separation of association, experimental priority, and causality",
            ),
        ),
        (
            "Vurdér en netværks- og berigelsesanalyse",
            "Et sæt differentielt udtrykte gener giver netværksmoduler og berigede termer. Forklar en analyse, der kontrollerer referenceunivers, afhængighed, multiple test og annotationsbias, og som undgår at gøre netværksassociationer til kausale mekanismer.",
            (
                "passende definition af univers og analytisk enhed",
                "kontrol af multiple test og afhængighed mellem termer",
                "robusthed af moduler, centralitet og annotationsbias",
                "adskillelse af association, eksperimentel prioritet og kausalitet",
            ),
        ),
    ),
    "dm847.w10": (
        (
            "Ensayo: diseñar un estudio ómico sin fuga",
            "Redacta un ensayo metodológico para un estudio ómico predictivo. Define unidad experimental, outcome, preprocesamiento, splits agrupados, validación anidada, métricas, calibración, interpretación, análisis de errores y artefactos reproducibles. Incluye amenazas a validez y decisiones que deben congelarse antes del test final.",
            (
                "unidad experimental y separación correcta de metadatos y features",
                "preprocesamiento aprendido exclusivamente dentro de entrenamiento",
                "validación agrupada y anidada con métricas justificadas",
                "calibración, estabilidad, limitaciones y reproducibilidad",
            ),
        ),
        (
            "Essay: design a leakage-free omics study",
            "Write a methodological essay for a predictive omics study. Define the experimental unit, outcome, preprocessing, grouped splits, nested validation, metrics, calibration, interpretation, error analysis, and reproducible artefacts. Include validity threats and decisions that must be frozen before the final test.",
            (
                "experimental unit and correct separation of metadata and features",
                "preprocessing learned exclusively within training data",
                "grouped and nested validation with justified metrics",
                "calibration, stability, limitations, and reproducibility",
            ),
        ),
        (
            "Essay: design et omikstudie uden leakage",
            "Skriv et metodisk essay til et prædiktivt omikstudie. Definér eksperimentel enhed, outcome, preprocessing, grupperede splits, nested validering, metrikker, kalibrering, fortolkning, fejlanalyse og reproducerbare artefakter. Medtag validitetstrusler og beslutninger, der skal fastlåses før den endelige test.",
            (
                "eksperimentel enhed og korrekt adskillelse af metadata og features",
                "preprocessing lært udelukkende i træningsdata",
                "grupperet og nested validering med begrundede metrikker",
                "kalibrering, stabilitet, begrænsninger og reproducerbarhed",
            ),
        ),
    ),
}


def written_assessment_text(
    locale: AppLocale,
    key: WrittenAssessmentCopyKey,
    **values: object,
) -> str:
    """Return one localized interface string with strict placeholders."""

    template = _STATIC[key][_LOCALE_INDEX[locale]]
    required = {
        field_name
        for _, field_name, _, _ in Formatter().parse(template)
        if field_name is not None
    }
    if set(values) != required:
        raise ValueError(
            f"Written-assessment copy {key.value!r} requires {sorted(required)}, "
            f"got {sorted(values)}."
        )
    return template.format(**values)


def written_prompt_copy(
    locale: AppLocale,
    prompt_id: str,
) -> PromptCopy:
    """Return localized title, task and focus points for one stable prompt."""

    return _PROMPTS[prompt_id][_LOCALE_INDEX[locale]]


def validate_written_assessment_copy() -> None:
    """Require complete static and authored prompt copy in every locale."""

    if set(_STATIC) != set(WrittenAssessmentCopyKey):
        raise ValueError("Written-assessment static copy is incomplete.")
    expected_prompts = {item.prompt_id for item in DM847_WRITTEN_PROMPTS}
    if set(_PROMPTS) != expected_prompts:
        raise ValueError("Written-assessment prompt copy does not match the authored catalog.")
    for prompt_id, localized in _PROMPTS.items():
        if len(localized) != len(_LOCALE_INDEX):
            raise ValueError(f"Prompt {prompt_id!r} does not define every locale.")
        for title, task, focus in localized:
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
