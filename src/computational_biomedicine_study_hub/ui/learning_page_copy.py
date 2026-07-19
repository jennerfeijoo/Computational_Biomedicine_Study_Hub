"""Strict trilingual copy for functional cross-course learning pages."""

from __future__ import annotations

from enum import StrEnum

from ..i18n import AppLocale


class LearningPageCopyKey(StrEnum):
    COURSE = "course"
    MODULE = "module"
    TYPE = "type"
    ALL_COURSES = "all_courses"
    ALL_MODULES = "all_modules"
    ALL_TYPES = "all_types"
    EMPTY = "empty"
    START_REVIEW = "start_review"
    REVIEW_EMPTY = "review_empty"
    MIX_COURSES = "mix_courses"
    HISTORY = "history"
    MASTERY = "mastery"
    DUE_COUNT = "due_count"
    AGAIN = "again"
    HARD = "hard"
    GOOD = "good"
    EASY = "easy"
    ASSESSMENT_MODE = "assessment_mode"
    QUICK_MODULE = "quick_module"
    COMPLETE_MODULE = "complete_module"
    COURSE_ASSESSMENT = "course_assessment"
    MIXED_ASSESSMENT = "mixed_assessment"
    START_ASSESSMENT = "start_assessment"
    ASSESSMENT_EMPTY = "assessment_empty"
    SESSION_PROGRESS = "session_progress"
    RESULT_SAVED = "result_saved"
    REVEAL = "reveal"
    SHUFFLE = "shuffle"
    FLASHCARD_EMPTY = "flashcard_empty"
    FLASHCARD_STATS = "flashcard_stats"
    SEARCH = "search"
    GLOSSARY_EMPTY = "glossary_empty"
    DEFINITION = "definition"
    SOURCE = "source"
    RELATED = "related"
    SYNONYMS = "synonyms"
    OPEN_MODULE = "open_module"
    NEW_CONCEPTS = "new_concepts"
    MODULE_PROGRESS = "module_progress"
    CONTINUE = "continue"
    ASSESSMENT_CATEGORY = "assessment_category"
    OBJECTIVE_ASSESSMENTS = "objective_assessments"
    OPEN_RESPONSES = "open_responses"
    CUMULATIVE_ASSESSMENTS = "cumulative_assessments"
    SAVE_DRAFTS = "save_drafts"
    DRAFTS_SAVED = "drafts_saved"
    CUMULATIVE_UNAVAILABLE = "cumulative_unavailable"


_ES = {
    LearningPageCopyKey.COURSE: "Asignatura",
    LearningPageCopyKey.MODULE: "Módulo",
    LearningPageCopyKey.TYPE: "Tipo de actividad",
    LearningPageCopyKey.ALL_COURSES: "Todas las asignaturas",
    LearningPageCopyKey.ALL_MODULES: "Todos los módulos",
    LearningPageCopyKey.ALL_TYPES: "Todos los tipos",
    LearningPageCopyKey.EMPTY: "Todavía no hay contenido disponible para este filtro.",
    LearningPageCopyKey.START_REVIEW: "Nueva sesión de repaso",
    LearningPageCopyKey.REVIEW_EMPTY: (
        "No hay elementos vencidos. Puedes incorporar conceptos nuevos a la cola."
    ),
    LearningPageCopyKey.MIX_COURSES: "Mezclar asignaturas",
    LearningPageCopyKey.HISTORY: "Historial reciente",
    LearningPageCopyKey.MASTERY: "Dominio estimado: {percent} %",
    LearningPageCopyKey.DUE_COUNT: "{count} elementos pendientes",
    LearningPageCopyKey.AGAIN: "Otra vez",
    LearningPageCopyKey.HARD: "Difícil",
    LearningPageCopyKey.GOOD: "Bien",
    LearningPageCopyKey.EASY: "Fácil",
    LearningPageCopyKey.ASSESSMENT_MODE: "Modalidad",
    LearningPageCopyKey.QUICK_MODULE: "Rápida por módulo",
    LearningPageCopyKey.COMPLETE_MODULE: "Completa de módulo",
    LearningPageCopyKey.COURSE_ASSESSMENT: "Acumulativa de asignatura",
    LearningPageCopyKey.MIXED_ASSESSMENT: "Mixta entre asignaturas",
    LearningPageCopyKey.START_ASSESSMENT: "Iniciar evaluación",
    LearningPageCopyKey.ASSESSMENT_EMPTY: (
        "No hay preguntas compatibles con la modalidad y el filtro seleccionados."
    ),
    LearningPageCopyKey.SESSION_PROGRESS: "{answered}/{total} respuestas · {correct} correctas",
    LearningPageCopyKey.RESULT_SAVED: "Resultado guardado localmente.",
    LearningPageCopyKey.REVEAL: "Mostrar reverso",
    LearningPageCopyKey.SHUFFLE: "Barajar",
    LearningPageCopyKey.FLASHCARD_EMPTY: "No hay tarjetas para este filtro.",
    LearningPageCopyKey.FLASHCARD_STATS: (
        "{reviewed} estudiadas · {mastered} dominadas · {due} vencidas"
    ),
    LearningPageCopyKey.SEARCH: "Buscar término, sinónimo o etiqueta…",
    LearningPageCopyKey.GLOSSARY_EMPTY: "No hay términos que coincidan con la búsqueda.",
    LearningPageCopyKey.DEFINITION: "Definición",
    LearningPageCopyKey.SOURCE: "Origen",
    LearningPageCopyKey.RELATED: "Términos relacionados",
    LearningPageCopyKey.SYNONYMS: "Sinónimos",
    LearningPageCopyKey.OPEN_MODULE: "Abrir módulo de origen",
    LearningPageCopyKey.NEW_CONCEPTS: "Añadir conceptos nuevos",
    LearningPageCopyKey.MODULE_PROGRESS: "{percent}% · {pending} pendientes · {attempts} intentos",
    LearningPageCopyKey.CONTINUE: "Continuar",
    LearningPageCopyKey.ASSESSMENT_CATEGORY: "Categoría",
    LearningPageCopyKey.OBJECTIVE_ASSESSMENTS: "Evaluaciones objetivas",
    LearningPageCopyKey.OPEN_RESPONSES: "Preguntas abiertas",
    LearningPageCopyKey.CUMULATIVE_ASSESSMENTS: "Evaluación acumulativa",
    LearningPageCopyKey.SAVE_DRAFTS: "Guardar borradores",
    LearningPageCopyKey.DRAFTS_SAVED: "Borradores guardados localmente.",
    LearningPageCopyKey.CUMULATIVE_UNAVAILABLE: (
        "Esta asignatura no contiene todavía una evaluación acumulativa canónica."
    ),
}

_EN = {
    LearningPageCopyKey.COURSE: "Course",
    LearningPageCopyKey.MODULE: "Module",
    LearningPageCopyKey.TYPE: "Activity type",
    LearningPageCopyKey.ALL_COURSES: "All courses",
    LearningPageCopyKey.ALL_MODULES: "All modules",
    LearningPageCopyKey.ALL_TYPES: "All types",
    LearningPageCopyKey.EMPTY: "There is no content available for this filter yet.",
    LearningPageCopyKey.START_REVIEW: "New review session",
    LearningPageCopyKey.REVIEW_EMPTY: ("No items are due. You can add new concepts to the queue."),
    LearningPageCopyKey.MIX_COURSES: "Mix courses",
    LearningPageCopyKey.HISTORY: "Recent history",
    LearningPageCopyKey.MASTERY: "Estimated mastery: {percent}%",
    LearningPageCopyKey.DUE_COUNT: "{count} pending items",
    LearningPageCopyKey.AGAIN: "Again",
    LearningPageCopyKey.HARD: "Hard",
    LearningPageCopyKey.GOOD: "Good",
    LearningPageCopyKey.EASY: "Easy",
    LearningPageCopyKey.ASSESSMENT_MODE: "Mode",
    LearningPageCopyKey.QUICK_MODULE: "Quick module",
    LearningPageCopyKey.COMPLETE_MODULE: "Complete module",
    LearningPageCopyKey.COURSE_ASSESSMENT: "Cumulative course",
    LearningPageCopyKey.MIXED_ASSESSMENT: "Mixed courses",
    LearningPageCopyKey.START_ASSESSMENT: "Start assessment",
    LearningPageCopyKey.ASSESSMENT_EMPTY: (
        "No questions match the selected mode and activity filter."
    ),
    LearningPageCopyKey.SESSION_PROGRESS: "{answered}/{total} answers · {correct} correct",
    LearningPageCopyKey.RESULT_SAVED: "Result saved locally.",
    LearningPageCopyKey.REVEAL: "Reveal back",
    LearningPageCopyKey.SHUFFLE: "Shuffle",
    LearningPageCopyKey.FLASHCARD_EMPTY: "There are no flashcards for this filter.",
    LearningPageCopyKey.FLASHCARD_STATS: ("{reviewed} studied · {mastered} mastered · {due} due"),
    LearningPageCopyKey.SEARCH: "Search term, synonym, or tag…",
    LearningPageCopyKey.GLOSSARY_EMPTY: "No terms match the search.",
    LearningPageCopyKey.DEFINITION: "Definition",
    LearningPageCopyKey.SOURCE: "Source",
    LearningPageCopyKey.RELATED: "Related terms",
    LearningPageCopyKey.SYNONYMS: "Synonyms",
    LearningPageCopyKey.OPEN_MODULE: "Open source module",
    LearningPageCopyKey.NEW_CONCEPTS: "Add new concepts",
    LearningPageCopyKey.MODULE_PROGRESS: "{percent}% · {pending} pending · {attempts} attempts",
    LearningPageCopyKey.CONTINUE: "Continue",
    LearningPageCopyKey.ASSESSMENT_CATEGORY: "Category",
    LearningPageCopyKey.OBJECTIVE_ASSESSMENTS: "Objective assessments",
    LearningPageCopyKey.OPEN_RESPONSES: "Open responses",
    LearningPageCopyKey.CUMULATIVE_ASSESSMENTS: "Cumulative assessment",
    LearningPageCopyKey.SAVE_DRAFTS: "Save drafts",
    LearningPageCopyKey.DRAFTS_SAVED: "Drafts saved locally.",
    LearningPageCopyKey.CUMULATIVE_UNAVAILABLE: (
        "This course does not yet contain a canonical cumulative assessment."
    ),
}

_DA = {
    LearningPageCopyKey.COURSE: "Kursus",
    LearningPageCopyKey.MODULE: "Modul",
    LearningPageCopyKey.TYPE: "Aktivitetstype",
    LearningPageCopyKey.ALL_COURSES: "Alle kurser",
    LearningPageCopyKey.ALL_MODULES: "Alle moduler",
    LearningPageCopyKey.ALL_TYPES: "Alle typer",
    LearningPageCopyKey.EMPTY: "Der er endnu intet indhold til dette filter.",
    LearningPageCopyKey.START_REVIEW: "Ny repetitionssession",
    LearningPageCopyKey.REVIEW_EMPTY: (
        "Ingen elementer er forfaldne. Du kan tilføje nye begreber til køen."
    ),
    LearningPageCopyKey.MIX_COURSES: "Bland kurser",
    LearningPageCopyKey.HISTORY: "Seneste historik",
    LearningPageCopyKey.MASTERY: "Estimeret mestring: {percent} %",
    LearningPageCopyKey.DUE_COUNT: "{count} ventende elementer",
    LearningPageCopyKey.AGAIN: "Igen",
    LearningPageCopyKey.HARD: "Svært",
    LearningPageCopyKey.GOOD: "Godt",
    LearningPageCopyKey.EASY: "Let",
    LearningPageCopyKey.ASSESSMENT_MODE: "Form",
    LearningPageCopyKey.QUICK_MODULE: "Hurtigt modul",
    LearningPageCopyKey.COMPLETE_MODULE: "Komplet modul",
    LearningPageCopyKey.COURSE_ASSESSMENT: "Kumulativt kursus",
    LearningPageCopyKey.MIXED_ASSESSMENT: "Blandede kurser",
    LearningPageCopyKey.START_ASSESSMENT: "Start evaluering",
    LearningPageCopyKey.ASSESSMENT_EMPTY: (
        "Ingen spørgsmål matcher den valgte form og aktivitetsfilteret."
    ),
    LearningPageCopyKey.SESSION_PROGRESS: "{answered}/{total} svar · {correct} korrekte",
    LearningPageCopyKey.RESULT_SAVED: "Resultatet er gemt lokalt.",
    LearningPageCopyKey.REVEAL: "Vis bagside",
    LearningPageCopyKey.SHUFFLE: "Bland",
    LearningPageCopyKey.FLASHCARD_EMPTY: "Der er ingen kort til dette filter.",
    LearningPageCopyKey.FLASHCARD_STATS: ("{reviewed} læst · {mastered} mestret · {due} forfaldne"),
    LearningPageCopyKey.SEARCH: "Søg efter term, synonym eller tag…",
    LearningPageCopyKey.GLOSSARY_EMPTY: "Ingen termer matcher søgningen.",
    LearningPageCopyKey.DEFINITION: "Definition",
    LearningPageCopyKey.SOURCE: "Kilde",
    LearningPageCopyKey.RELATED: "Relaterede termer",
    LearningPageCopyKey.SYNONYMS: "Synonymer",
    LearningPageCopyKey.OPEN_MODULE: "Åbn kildemodul",
    LearningPageCopyKey.NEW_CONCEPTS: "Tilføj nye begreber",
    LearningPageCopyKey.MODULE_PROGRESS: "{percent}% · {pending} ventende · {attempts} forsøg",
    LearningPageCopyKey.CONTINUE: "Fortsæt",
    LearningPageCopyKey.ASSESSMENT_CATEGORY: "Kategori",
    LearningPageCopyKey.OBJECTIVE_ASSESSMENTS: "Objektive evalueringer",
    LearningPageCopyKey.OPEN_RESPONSES: "Åbne svar",
    LearningPageCopyKey.CUMULATIVE_ASSESSMENTS: "Kumulativ evaluering",
    LearningPageCopyKey.SAVE_DRAFTS: "Gem kladder",
    LearningPageCopyKey.DRAFTS_SAVED: "Kladder er gemt lokalt.",
    LearningPageCopyKey.CUMULATIVE_UNAVAILABLE: (
        "Dette kursus indeholder endnu ikke en kanonisk kumulativ evaluering."
    ),
}

_COPY = {
    AppLocale.SPANISH_SPAIN: _ES,
    AppLocale.ENGLISH: _EN,
    AppLocale.DANISH_DENMARK: _DA,
}


def learning_text(
    locale: AppLocale,
    key: LearningPageCopyKey,
    **values: object,
) -> str:
    """Return complete localized page copy with optional named interpolation."""
    return _COPY[locale][key].format(**values)


def validate_learning_page_copy() -> None:
    """Fail when a locale does not cover the complete page vocabulary."""
    expected = set(LearningPageCopyKey)
    for locale, catalog in _COPY.items():
        if set(catalog) != expected:
            raise ValueError(f"Incomplete learning-page copy for {locale.value}.")


__all__ = ["LearningPageCopyKey", "learning_text", "validate_learning_page_copy"]
