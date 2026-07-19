"""Complete translation catalogs for the currently defined application messages."""

from __future__ import annotations

from .locales import AppLocale
from .messages import MessageKey

Catalog = dict[MessageKey, str]

SPANISH_CATALOG: Catalog = {
    MessageKey.APP_NAME: "Computational Biomedicine Study Hub",
    MessageKey.PRODUCT_NAME: "Computational\nBiomedicine Hub",
    MessageKey.NAV_GENERAL: "GENERAL",
    MessageKey.NAV_SEMESTER: "SEMESTRE {semester}",
    MessageKey.NAV_LEARNING: "APRENDIZAJE",
    MessageKey.NAV_RESOURCES: "RECURSOS",
    MessageKey.NAV_SYSTEM: "SISTEMA",
    MessageKey.NAV_HOME: "Inicio",
    MessageKey.NAV_REVIEW: "Repaso",
    MessageKey.NAV_ASSESSMENTS: "Evaluaciones",
    MessageKey.NAV_FLASHCARDS: "Tarjetas de memoria",
    MessageKey.NAV_STUDY_LAB: "Laboratorio de estudio",
    MessageKey.NAV_GLOSSARY: "Glosario",
    MessageKey.NAV_SETTINGS: "Configuración",
    MessageKey.PAGE_HOME_TITLE: "Inicio",
    MessageKey.PAGE_HOME_SUBTITLE: "Centro de estudio del MSc in Computational Biomedicine.",
    MessageKey.PAGE_REVIEW_TITLE: "Repaso",
    MessageKey.PAGE_REVIEW_SUBTITLE: "Recuperación activa, práctica intercalada y revisión espaciada.",
    MessageKey.PAGE_ASSESSMENTS_TITLE: "Evaluaciones",
    MessageKey.PAGE_ASSESSMENTS_SUBTITLE: "Preguntas, ejercicios y problemas con retroalimentación.",
    MessageKey.PAGE_FLASHCARDS_TITLE: "Tarjetas de memoria",
    MessageKey.PAGE_FLASHCARDS_SUBTITLE: "Conceptos, fórmulas, código y relaciones esenciales.",
    MessageKey.PAGE_STUDY_LAB_TITLE: "Laboratorio de estudio",
    MessageKey.PAGE_STUDY_LAB_SUBTITLE: "Tutor local con recuperación trazable del contenido académico.",
    MessageKey.PAGE_GLOSSARY_TITLE: "Glosario",
    MessageKey.PAGE_GLOSSARY_SUBTITLE: "Definiciones de programación, estadística y biología.",
    MessageKey.PAGE_SETTINGS_TITLE: "Configuración",
    MessageKey.PAGE_SETTINGS_SUBTITLE: "Preferencias de la aplicación e integraciones locales.",
    MessageKey.HOME_HEADING: "Asignaturas del primer semestre",
    MessageKey.HOME_DESCRIPTION: (
        "Selecciona una asignatura para entrar en su espacio independiente. "
        "Cada curso puede utilizar una estructura de aprendizaje diferente."
    ),
    MessageKey.COURSE_METADATA: "Semestre {semester} · {ects} ECTS",
    MessageKey.COURSE_OPEN: "Abrir asignatura",
    MessageKey.SETTINGS_LANGUAGE_GROUP: "Idioma",
    MessageKey.SETTINGS_LANGUAGE_LABEL: "Idioma de la aplicación:",
    MessageKey.SETTINGS_LANGUAGE_HELP: (
        "El idioma seleccionado se aplicará a la interfaz, al contenido académico y al tutor."
    ),
    MessageKey.SETTINGS_LANGUAGE_SAVED: "Idioma guardado: {language}.",
    MessageKey.MODULE_LABEL: "Módulo {number}",
    MessageKey.MODULE_TAB_OVERVIEW: "Resumen",
    MessageKey.MODULE_TAB_CONCEPTS: "Conceptos",
    MessageKey.MODULE_TAB_EXAMPLES: "Ejemplos",
    MessageKey.MODULE_TAB_PRACTICE: "Práctica",
    MessageKey.MODULE_TAB_ASSESSMENT: "Evaluación",
    MessageKey.MODULE_PURPOSE: "Propósito del módulo",
    MessageKey.MODULE_OBJECTIVES: "Objetivos de aprendizaje",
    MessageKey.MODULE_STUDY_SEQUENCE: "Secuencia de estudio",
    MessageKey.MODULE_STUDY_SEQUENCE_TEXT: (
        "Teoría conectada → ejemplos resueltos → práctica formativa → evaluación del aprendizaje."
    ),
    MessageKey.MODULE_ESSENTIAL_POINTS: "Puntos esenciales",
    MessageKey.MODULE_PROBLEM: "Problema",
    MessageKey.MODULE_REASONING: "Razonamiento",
    MessageKey.MODULE_CODE: "Código",
    MessageKey.MODULE_EXPECTED_OUTPUT: "Salida esperada",
    MessageKey.MODULE_EXPLANATION: "Explicación",
    MessageKey.MODULE_OPTIONS: "Opciones",
    MessageKey.MODULE_GRADING_CRITERIA: "Criterios que se evaluarán",
    MessageKey.MODULE_QUESTION: "Pregunta {number} · {activity}",
    MessageKey.MODULE_PRACTICE_NOTICE: (
        "Cada sesión selecciona una combinación diferente de ejercicios. Escribe tu respuesta, "
        "revela pistas progresivamente y compara después con la solución de referencia."
    ),
    MessageKey.MODULE_ASSESSMENT_NOTICE: (
        "Responde cada pregunta y pulsa Comprobar respuesta para obtener corrección inmediata. "
        "Una nueva sesión genera otra combinación del banco y vuelve a barajar las opciones."
    ),
    MessageKey.ACTIVITY_WORKED_EXAMPLE: "Ejemplo resuelto",
    MessageKey.ACTIVITY_FLASHCARD: "Tarjeta de memoria",
    MessageKey.ACTIVITY_MULTIPLE_CHOICE: "Opción múltiple",
    MessageKey.ACTIVITY_MULTIPLE_SELECT: "Selección múltiple",
    MessageKey.ACTIVITY_TRUE_FALSE: "Verdadero o falso",
    MessageKey.ACTIVITY_FILL_BLANK: "Rellenar espacios",
    MessageKey.ACTIVITY_MATCHING: "Relacionar elementos",
    MessageKey.ACTIVITY_ORDERING: "Ordenar pasos",
    MessageKey.ACTIVITY_CODE_COMPLETION: "Completar código",
    MessageKey.ACTIVITY_CODE_TRACING: "Trazado de código",
    MessageKey.ACTIVITY_DEBUGGING: "Depuración",
    MessageKey.ACTIVITY_SHORT_ANSWER: "Respuesta breve",
    MessageKey.ACTIVITY_ORAL_EXPLANATION: "Explicación oral",
    MessageKey.ACTIVITY_DATA_INTERPRETATION: "Interpretación de datos",
    MessageKey.ACTIVITY_PIPELINE_DESIGN: "Diseño de pipeline",
}

ENGLISH_CATALOG: Catalog = {
    MessageKey.APP_NAME: "Computational Biomedicine Study Hub",
    MessageKey.PRODUCT_NAME: "Computational\nBiomedicine Hub",
    MessageKey.NAV_GENERAL: "GENERAL",
    MessageKey.NAV_SEMESTER: "SEMESTER {semester}",
    MessageKey.NAV_LEARNING: "LEARNING",
    MessageKey.NAV_RESOURCES: "RESOURCES",
    MessageKey.NAV_SYSTEM: "SYSTEM",
    MessageKey.NAV_HOME: "Home",
    MessageKey.NAV_REVIEW: "Review",
    MessageKey.NAV_ASSESSMENTS: "Assessments",
    MessageKey.NAV_FLASHCARDS: "Flashcards",
    MessageKey.NAV_STUDY_LAB: "Study Lab",
    MessageKey.NAV_GLOSSARY: "Glossary",
    MessageKey.NAV_SETTINGS: "Settings",
    MessageKey.PAGE_HOME_TITLE: "Home",
    MessageKey.PAGE_HOME_SUBTITLE: "Study centre for the MSc in Computational Biomedicine.",
    MessageKey.PAGE_REVIEW_TITLE: "Review",
    MessageKey.PAGE_REVIEW_SUBTITLE: "Active recall, interleaved practice and spaced review.",
    MessageKey.PAGE_ASSESSMENTS_TITLE: "Assessments",
    MessageKey.PAGE_ASSESSMENTS_SUBTITLE: "Questions, exercises and problems with feedback.",
    MessageKey.PAGE_FLASHCARDS_TITLE: "Flashcards",
    MessageKey.PAGE_FLASHCARDS_SUBTITLE: "Essential concepts, formulas, code and relationships.",
    MessageKey.PAGE_STUDY_LAB_TITLE: "Study Lab",
    MessageKey.PAGE_STUDY_LAB_SUBTITLE: "Local tutor grounded in traceable academic content.",
    MessageKey.PAGE_GLOSSARY_TITLE: "Glossary",
    MessageKey.PAGE_GLOSSARY_SUBTITLE: "Definitions from programming, statistics and biology.",
    MessageKey.PAGE_SETTINGS_TITLE: "Settings",
    MessageKey.PAGE_SETTINGS_SUBTITLE: "Application preferences and local integrations.",
    MessageKey.HOME_HEADING: "First-semester courses",
    MessageKey.HOME_DESCRIPTION: (
        "Select a course to enter its dedicated study space. "
        "Each course may use a different learning structure."
    ),
    MessageKey.COURSE_METADATA: "Semester {semester} · {ects} ECTS",
    MessageKey.COURSE_OPEN: "Open course",
    MessageKey.SETTINGS_LANGUAGE_GROUP: "Language",
    MessageKey.SETTINGS_LANGUAGE_LABEL: "Application language:",
    MessageKey.SETTINGS_LANGUAGE_HELP: (
        "The selected language will apply to the interface, academic content and tutor."
    ),
    MessageKey.SETTINGS_LANGUAGE_SAVED: "Language saved: {language}.",
    MessageKey.MODULE_LABEL: "Module {number}",
    MessageKey.MODULE_TAB_OVERVIEW: "Overview",
    MessageKey.MODULE_TAB_CONCEPTS: "Concepts",
    MessageKey.MODULE_TAB_EXAMPLES: "Examples",
    MessageKey.MODULE_TAB_PRACTICE: "Practice",
    MessageKey.MODULE_TAB_ASSESSMENT: "Assessment",
    MessageKey.MODULE_PURPOSE: "Module purpose",
    MessageKey.MODULE_OBJECTIVES: "Learning objectives",
    MessageKey.MODULE_STUDY_SEQUENCE: "Study sequence",
    MessageKey.MODULE_STUDY_SEQUENCE_TEXT: (
        "Connected theory → worked examples → formative practice → learning assessment."
    ),
    MessageKey.MODULE_ESSENTIAL_POINTS: "Essential points",
    MessageKey.MODULE_PROBLEM: "Problem",
    MessageKey.MODULE_REASONING: "Reasoning",
    MessageKey.MODULE_CODE: "Code",
    MessageKey.MODULE_EXPECTED_OUTPUT: "Expected output",
    MessageKey.MODULE_EXPLANATION: "Explanation",
    MessageKey.MODULE_OPTIONS: "Options",
    MessageKey.MODULE_GRADING_CRITERIA: "Assessment criteria",
    MessageKey.MODULE_QUESTION: "Question {number} · {activity}",
    MessageKey.MODULE_PRACTICE_NOTICE: (
        "Each session selects a different combination of exercises. Write your answer, "
        "reveal hints progressively and then compare it with the reference solution."
    ),
    MessageKey.MODULE_ASSESSMENT_NOTICE: (
        "Answer each question and select Check answer for immediate correction. "
        "A new session selects another set from the bank and reshuffles the options."
    ),
    MessageKey.ACTIVITY_WORKED_EXAMPLE: "Worked example",
    MessageKey.ACTIVITY_FLASHCARD: "Flashcard",
    MessageKey.ACTIVITY_MULTIPLE_CHOICE: "Multiple choice",
    MessageKey.ACTIVITY_MULTIPLE_SELECT: "Multiple select",
    MessageKey.ACTIVITY_TRUE_FALSE: "True or false",
    MessageKey.ACTIVITY_FILL_BLANK: "Fill in the blanks",
    MessageKey.ACTIVITY_MATCHING: "Match items",
    MessageKey.ACTIVITY_ORDERING: "Order steps",
    MessageKey.ACTIVITY_CODE_COMPLETION: "Complete code",
    MessageKey.ACTIVITY_CODE_TRACING: "Code tracing",
    MessageKey.ACTIVITY_DEBUGGING: "Debugging",
    MessageKey.ACTIVITY_SHORT_ANSWER: "Short answer",
    MessageKey.ACTIVITY_ORAL_EXPLANATION: "Oral explanation",
    MessageKey.ACTIVITY_DATA_INTERPRETATION: "Data interpretation",
    MessageKey.ACTIVITY_PIPELINE_DESIGN: "Pipeline design",
}

DANISH_CATALOG: Catalog = {
    MessageKey.APP_NAME: "Computational Biomedicine Study Hub",
    MessageKey.PRODUCT_NAME: "Computational\nBiomedicine Hub",
    MessageKey.NAV_GENERAL: "GENERELT",
    MessageKey.NAV_SEMESTER: "SEMESTER {semester}",
    MessageKey.NAV_LEARNING: "LÆRING",
    MessageKey.NAV_RESOURCES: "RESSOURCER",
    MessageKey.NAV_SYSTEM: "SYSTEM",
    MessageKey.NAV_HOME: "Forside",
    MessageKey.NAV_REVIEW: "Repetition",
    MessageKey.NAV_ASSESSMENTS: "Evalueringer",
    MessageKey.NAV_FLASHCARDS: "Huskekort",
    MessageKey.NAV_STUDY_LAB: "Studielaboratorium",
    MessageKey.NAV_GLOSSARY: "Ordliste",
    MessageKey.NAV_SETTINGS: "Indstillinger",
    MessageKey.PAGE_HOME_TITLE: "Forside",
    MessageKey.PAGE_HOME_SUBTITLE: "Studiecenter for MSc in Computational Biomedicine.",
    MessageKey.PAGE_REVIEW_TITLE: "Repetition",
    MessageKey.PAGE_REVIEW_SUBTITLE: "Aktiv genkaldelse, varieret træning og tidsfordelt repetition.",
    MessageKey.PAGE_ASSESSMENTS_TITLE: "Evalueringer",
    MessageKey.PAGE_ASSESSMENTS_SUBTITLE: "Spørgsmål, øvelser og problemer med feedback.",
    MessageKey.PAGE_FLASHCARDS_TITLE: "Huskekort",
    MessageKey.PAGE_FLASHCARDS_SUBTITLE: "Centrale begreber, formler, kode og sammenhænge.",
    MessageKey.PAGE_STUDY_LAB_TITLE: "Studielaboratorium",
    MessageKey.PAGE_STUDY_LAB_SUBTITLE: "Lokal tutor baseret på sporbart fagligt indhold.",
    MessageKey.PAGE_GLOSSARY_TITLE: "Ordliste",
    MessageKey.PAGE_GLOSSARY_SUBTITLE: "Definitioner fra programmering, statistik og biologi.",
    MessageKey.PAGE_SETTINGS_TITLE: "Indstillinger",
    MessageKey.PAGE_SETTINGS_SUBTITLE: "Programindstillinger og lokale integrationer.",
    MessageKey.HOME_HEADING: "Kurser på første semester",
    MessageKey.HOME_DESCRIPTION: (
        "Vælg et kursus for at åbne dets selvstændige studieområde. "
        "Hvert kursus kan anvende en forskellig læringsstruktur."
    ),
    MessageKey.COURSE_METADATA: "Semester {semester} · {ects} ECTS",
    MessageKey.COURSE_OPEN: "Åbn kursus",
    MessageKey.SETTINGS_LANGUAGE_GROUP: "Sprog",
    MessageKey.SETTINGS_LANGUAGE_LABEL: "Programsprog:",
    MessageKey.SETTINGS_LANGUAGE_HELP: (
        "Det valgte sprog anvendes i brugerfladen, det faglige indhold og tutorens svar."
    ),
    MessageKey.SETTINGS_LANGUAGE_SAVED: "Sprog gemt: {language}.",
    MessageKey.MODULE_LABEL: "Modul {number}",
    MessageKey.MODULE_TAB_OVERVIEW: "Oversigt",
    MessageKey.MODULE_TAB_CONCEPTS: "Begreber",
    MessageKey.MODULE_TAB_EXAMPLES: "Eksempler",
    MessageKey.MODULE_TAB_PRACTICE: "Træning",
    MessageKey.MODULE_TAB_ASSESSMENT: "Evaluering",
    MessageKey.MODULE_PURPOSE: "Modulets formål",
    MessageKey.MODULE_OBJECTIVES: "Læringsmål",
    MessageKey.MODULE_STUDY_SEQUENCE: "Studieforløb",
    MessageKey.MODULE_STUDY_SEQUENCE_TEXT: (
        "Sammenhængende teori → gennemarbejdede eksempler → formativ træning → evaluering."
    ),
    MessageKey.MODULE_ESSENTIAL_POINTS: "Centrale punkter",
    MessageKey.MODULE_PROBLEM: "Problem",
    MessageKey.MODULE_REASONING: "Ræsonnement",
    MessageKey.MODULE_CODE: "Kode",
    MessageKey.MODULE_EXPECTED_OUTPUT: "Forventet output",
    MessageKey.MODULE_EXPLANATION: "Forklaring",
    MessageKey.MODULE_OPTIONS: "Svarmuligheder",
    MessageKey.MODULE_GRADING_CRITERIA: "Vurderingskriterier",
    MessageKey.MODULE_QUESTION: "Spørgsmål {number} · {activity}",
    MessageKey.MODULE_PRACTICE_NOTICE: (
        "Hver session vælger en ny kombination af øvelser. Skriv dit svar, "
        "vis ledetråde gradvist, og sammenlign derefter med referencesvaret."
    ),
    MessageKey.MODULE_ASSESSMENT_NOTICE: (
        "Besvar hvert spørgsmål, og vælg Kontrollér svar for at få feedback med det samme. "
        "En ny session vælger et andet sæt fra banken og blander svarmulighederne igen."
    ),
    MessageKey.ACTIVITY_WORKED_EXAMPLE: "Gennemarbejdet eksempel",
    MessageKey.ACTIVITY_FLASHCARD: "Huskekort",
    MessageKey.ACTIVITY_MULTIPLE_CHOICE: "Ét svar",
    MessageKey.ACTIVITY_MULTIPLE_SELECT: "Flere svar",
    MessageKey.ACTIVITY_TRUE_FALSE: "Sandt eller falsk",
    MessageKey.ACTIVITY_FILL_BLANK: "Udfyld felterne",
    MessageKey.ACTIVITY_MATCHING: "Match elementer",
    MessageKey.ACTIVITY_ORDERING: "Sæt trin i rækkefølge",
    MessageKey.ACTIVITY_CODE_COMPLETION: "Færdiggør kode",
    MessageKey.ACTIVITY_CODE_TRACING: "Kodegennemgang",
    MessageKey.ACTIVITY_DEBUGGING: "Fejlfinding",
    MessageKey.ACTIVITY_SHORT_ANSWER: "Kort svar",
    MessageKey.ACTIVITY_ORAL_EXPLANATION: "Mundtlig forklaring",
    MessageKey.ACTIVITY_DATA_INTERPRETATION: "Datafortolkning",
    MessageKey.ACTIVITY_PIPELINE_DESIGN: "Design af pipeline",
}

CATALOGS: dict[AppLocale, Catalog] = {
    AppLocale.SPANISH_SPAIN: SPANISH_CATALOG,
    AppLocale.ENGLISH: ENGLISH_CATALOG,
    AppLocale.DANISH_DENMARK: DANISH_CATALOG,
}

__all__ = [
    "CATALOGS",
    "Catalog",
    "DANISH_CATALOG",
    "ENGLISH_CATALOG",
    "SPANISH_CATALOG",
]
