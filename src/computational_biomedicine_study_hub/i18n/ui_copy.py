"""Strict localized copy for interactive widgets not yet covered by MessageKey."""

from __future__ import annotations

from enum import StrEnum
from string import Formatter

from .locales import AppLocale


class UiCopyKey(StrEnum):
    """Stable keys for the current interactive application surface."""

    REVIEW_PLACEHOLDER = "placeholder.review"
    ASSESSMENTS_PLACEHOLDER = "placeholder.assessments"
    FLASHCARDS_PLACEHOLDER = "placeholder.flashcards"
    GLOSSARY_PLACEHOLDER = "placeholder.glossary"
    COURSE_STRUCTURE_HEADING = "course.structure.heading"
    COURSE_STRUCTURE_NOTICE = "course.structure.notice"

    MODULE_OBJECTIVE_SECTION = "module.objective_section"
    MODULE_COMPLETE_ASSESSMENT = "module.complete_assessment"
    MODULE_COMPLETE_ASSESSMENT_NOTICE = "module.complete_assessment_notice"

    PRACTICE_NUMBER = "practice.number"
    PRACTICE_YOUR_ANSWER = "practice.your_answer"
    PRACTICE_ANSWER_PLACEHOLDER = "practice.answer_placeholder"
    PRACTICE_SHOW_HINT = "practice.show_hint"
    PRACTICE_SHOW_NEXT_HINT = "practice.show_next_hint"
    PRACTICE_NO_MORE_HINTS = "practice.no_more_hints"
    PRACTICE_REFERENCE_BUTTON = "practice.reference_button"
    PRACTICE_REFERENCE_TITLE = "practice.reference_title"
    PRACTICE_WHY = "practice.why"
    PRACTICE_SELF_ASSESSMENT = "practice.self_assessment"
    PRACTICE_SOLVED = "practice.solved"
    PRACTICE_REVIEW = "practice.review"
    PRACTICE_SOLUTION_VISIBLE = "practice.solution_visible"
    PRACTICE_HINT_NUMBER = "practice.hint_number"
    PRACTICE_TITLE = "practice.title"
    PRACTICE_NEW_SESSION = "practice.new_session"
    PRACTICE_METADATA = "practice.metadata"
    PRACTICE_PROGRESS = "practice.progress"

    OBJECTIVE_QUESTION_NUMBER = "objective.question_number"
    OBJECTIVE_CHECK = "objective.check"
    OBJECTIVE_SELECT_WARNING = "objective.select_warning"
    OBJECTIVE_CORRECT = "objective.correct"
    OBJECTIVE_INCORRECT = "objective.incorrect"
    OBJECTIVE_TITLE = "objective.title"
    OBJECTIVE_NEW_SESSION = "objective.new_session"
    OBJECTIVE_METADATA = "objective.metadata"
    OBJECTIVE_SCORE = "objective.score"

    OLLAMA_RECONNECT = "ollama.reconnect"
    OLLAMA_PENDING = "ollama.pending"
    OLLAMA_SAVE = "ollama.save"
    OLLAMA_URL = "ollama.url"
    OLLAMA_STATUS = "ollama.status"
    OLLAMA_VERSION = "ollama.version"
    OLLAMA_MODEL = "ollama.model"
    OLLAMA_GROUP = "ollama.group"
    OLLAMA_EXPLANATION = "ollama.explanation"
    OLLAMA_CONNECTING = "ollama.connecting"
    OLLAMA_NO_MODELS = "ollama.no_models"
    OLLAMA_CONNECTED = "ollama.connected"
    OLLAMA_PREFERRED_MISSING = "ollama.preferred_missing"
    OLLAMA_SAVED = "ollama.saved"


SPANISH_UI_COPY: dict[UiCopyKey, str] = {
    UiCopyKey.REVIEW_PLACEHOLDER: (
        "El motor de repaso incorporará recuperación activa, intercalado y repetición espaciada."
    ),
    UiCopyKey.ASSESSMENTS_PLACEHOLDER: (
        "Las evaluaciones incluirán opción múltiple, selección múltiple, rellenar espacios, "
        "relacionar elementos, ordenar pasos, código y explicación oral."
    ),
    UiCopyKey.FLASHCARDS_PLACEHOLDER: (
        "Las tarjetas cubrirán conceptos, fórmulas, código, errores frecuentes y conexiones "
        "entre asignaturas."
    ),
    UiCopyKey.GLOSSARY_PLACEHOLDER: "El glosario se poblará junto con cada módulo académico.",
    UiCopyKey.COURSE_STRUCTURE_HEADING: "Estructura propia de la asignatura",
    UiCopyKey.COURSE_STRUCTURE_NOTICE: (
        "Esta pantalla confirma la selección de la asignatura. Los módulos y el contenido "
        "académico se añadirán en entregas independientes."
    ),
    UiCopyKey.MODULE_OBJECTIVE_SECTION: "Práctica objetiva aleatoria",
    UiCopyKey.MODULE_COMPLETE_ASSESSMENT: "Evaluación completa del módulo",
    UiCopyKey.MODULE_COMPLETE_ASSESSMENT_NOTICE: (
        "Estas actividades cubren trazado, depuración, ordenación, relación de conceptos, código, "
        "interpretación y respuestas abiertas. Las soluciones permanecen separadas del lector "
        "para conservar su función evaluativa."
    ),
    UiCopyKey.PRACTICE_NUMBER: "Práctica {number}",
    UiCopyKey.PRACTICE_YOUR_ANSWER: "Tu respuesta",
    UiCopyKey.PRACTICE_ANSWER_PLACEHOLDER: (
        "Escribe aquí tu razonamiento, tabla de trazado, código o explicación."
    ),
    UiCopyKey.PRACTICE_SHOW_HINT: "Mostrar pista",
    UiCopyKey.PRACTICE_SHOW_NEXT_HINT: "Mostrar siguiente pista",
    UiCopyKey.PRACTICE_NO_MORE_HINTS: "No hay más pistas",
    UiCopyKey.PRACTICE_REFERENCE_BUTTON: "Ver solución de referencia",
    UiCopyKey.PRACTICE_REFERENCE_TITLE: "Solución de referencia",
    UiCopyKey.PRACTICE_WHY: "Por qué",
    UiCopyKey.PRACTICE_SELF_ASSESSMENT: "Autoevaluación:",
    UiCopyKey.PRACTICE_SOLVED: "Lo resolví",
    UiCopyKey.PRACTICE_REVIEW: "Necesito repasar",
    UiCopyKey.PRACTICE_SOLUTION_VISIBLE: "Solución visible",
    UiCopyKey.PRACTICE_HINT_NUMBER: "Pista {number}: {hint}",
    UiCopyKey.PRACTICE_TITLE: "Práctica guiada aleatoria",
    UiCopyKey.PRACTICE_NEW_SESSION: "Nueva práctica",
    UiCopyKey.PRACTICE_METADATA: (
        "{count} ejercicios seleccionados de un banco de {bank}. La combinación y el orden "
        "cambian entre sesiones."
    ),
    UiCopyKey.PRACTICE_PROGRESS: (
        "{solved} resueltos · {review} para repasar · {assessed}/{total} valorados"
    ),
    UiCopyKey.OBJECTIVE_QUESTION_NUMBER: "Pregunta {number}",
    UiCopyKey.OBJECTIVE_CHECK: "Comprobar respuesta",
    UiCopyKey.OBJECTIVE_SELECT_WARNING: "Selecciona una respuesta antes de comprobar.",
    UiCopyKey.OBJECTIVE_CORRECT: "Correcto. {explanation}",
    UiCopyKey.OBJECTIVE_INCORRECT: (
        "Incorrecto. Respuesta correcta: {answer}. {explanation}"
    ),
    UiCopyKey.OBJECTIVE_TITLE: "Evaluación objetiva aleatoria",
    UiCopyKey.OBJECTIVE_NEW_SESSION: "Nueva práctica",
    UiCopyKey.OBJECTIVE_METADATA: (
        "{count} preguntas seleccionadas de un banco de {bank}. El conjunto, el orden y las "
        "opciones cambian entre sesiones."
    ),
    UiCopyKey.OBJECTIVE_SCORE: "{correct} aciertos · {answered}/{total}",
    UiCopyKey.OLLAMA_RECONNECT: "Reconectar",
    UiCopyKey.OLLAMA_PENDING: "Conexión pendiente.",
    UiCopyKey.OLLAMA_SAVE: "Guardar configuración",
    UiCopyKey.OLLAMA_URL: "URL local:",
    UiCopyKey.OLLAMA_STATUS: "Estado:",
    UiCopyKey.OLLAMA_VERSION: "Versión detectada:",
    UiCopyKey.OLLAMA_MODEL: "Modelo:",
    UiCopyKey.OLLAMA_GROUP: "Ollama local",
    UiCopyKey.OLLAMA_EXPLANATION: (
        "La aplicación se conecta automáticamente con Ollama y prioriza {model}. El botón "
        "Reconectar permite repetir la comprobación."
    ),
    UiCopyKey.OLLAMA_CONNECTING: "Conectando automáticamente con Ollama…",
    UiCopyKey.OLLAMA_NO_MODELS: "Conexión correcta, pero Ollama no informó modelos instalados.",
    UiCopyKey.OLLAMA_CONNECTED: "Conectado automáticamente con {model}.",
    UiCopyKey.OLLAMA_PREFERRED_MISSING: (
        "Conexión correcta, pero no se encontró {model}. Se seleccionó un modelo local disponible."
    ),
    UiCopyKey.OLLAMA_SAVED: "Configuración guardada para el modelo {model}.",
}

ENGLISH_UI_COPY: dict[UiCopyKey, str] = {
    UiCopyKey.REVIEW_PLACEHOLDER: (
        "The review engine will include active recall, interleaving and spaced repetition."
    ),
    UiCopyKey.ASSESSMENTS_PLACEHOLDER: (
        "Assessments will include multiple choice, multiple select, fill-in-the-blank, matching, "
        "ordering, code and oral explanation."
    ),
    UiCopyKey.FLASHCARDS_PLACEHOLDER: (
        "Flashcards will cover concepts, formulas, code, common errors and links between courses."
    ),
    UiCopyKey.GLOSSARY_PLACEHOLDER: "The glossary will grow with each academic module.",
    UiCopyKey.COURSE_STRUCTURE_HEADING: "Course-specific structure",
    UiCopyKey.COURSE_STRUCTURE_NOTICE: (
        "This screen confirms the selected course. Modules and academic content will be added in "
        "independent deliveries."
    ),
    UiCopyKey.MODULE_OBJECTIVE_SECTION: "Randomized objective practice",
    UiCopyKey.MODULE_COMPLETE_ASSESSMENT: "Complete module assessment",
    UiCopyKey.MODULE_COMPLETE_ASSESSMENT_NOTICE: (
        "These activities cover tracing, debugging, ordering, concept matching, code, interpretation "
        "and open responses. Solutions remain separate from the reader to preserve their assessment role."
    ),
    UiCopyKey.PRACTICE_NUMBER: "Practice {number}",
    UiCopyKey.PRACTICE_YOUR_ANSWER: "Your answer",
    UiCopyKey.PRACTICE_ANSWER_PLACEHOLDER: (
        "Write your reasoning, trace table, code or explanation here."
    ),
    UiCopyKey.PRACTICE_SHOW_HINT: "Show hint",
    UiCopyKey.PRACTICE_SHOW_NEXT_HINT: "Show next hint",
    UiCopyKey.PRACTICE_NO_MORE_HINTS: "No more hints",
    UiCopyKey.PRACTICE_REFERENCE_BUTTON: "View reference solution",
    UiCopyKey.PRACTICE_REFERENCE_TITLE: "Reference solution",
    UiCopyKey.PRACTICE_WHY: "Why",
    UiCopyKey.PRACTICE_SELF_ASSESSMENT: "Self-assessment:",
    UiCopyKey.PRACTICE_SOLVED: "I solved it",
    UiCopyKey.PRACTICE_REVIEW: "I need to review",
    UiCopyKey.PRACTICE_SOLUTION_VISIBLE: "Solution visible",
    UiCopyKey.PRACTICE_HINT_NUMBER: "Hint {number}: {hint}",
    UiCopyKey.PRACTICE_TITLE: "Randomized guided practice",
    UiCopyKey.PRACTICE_NEW_SESSION: "New practice",
    UiCopyKey.PRACTICE_METADATA: (
        "{count} exercises selected from a bank of {bank}. The combination and order change between sessions."
    ),
    UiCopyKey.PRACTICE_PROGRESS: (
        "{solved} solved · {review} to review · {assessed}/{total} assessed"
    ),
    UiCopyKey.OBJECTIVE_QUESTION_NUMBER: "Question {number}",
    UiCopyKey.OBJECTIVE_CHECK: "Check answer",
    UiCopyKey.OBJECTIVE_SELECT_WARNING: "Select an answer before checking.",
    UiCopyKey.OBJECTIVE_CORRECT: "Correct. {explanation}",
    UiCopyKey.OBJECTIVE_INCORRECT: (
        "Incorrect. Correct answer: {answer}. {explanation}"
    ),
    UiCopyKey.OBJECTIVE_TITLE: "Randomized objective assessment",
    UiCopyKey.OBJECTIVE_NEW_SESSION: "New practice",
    UiCopyKey.OBJECTIVE_METADATA: (
        "{count} questions selected from a bank of {bank}. The set, order and options change between sessions."
    ),
    UiCopyKey.OBJECTIVE_SCORE: "{correct} correct · {answered}/{total}",
    UiCopyKey.OLLAMA_RECONNECT: "Reconnect",
    UiCopyKey.OLLAMA_PENDING: "Connection pending.",
    UiCopyKey.OLLAMA_SAVE: "Save configuration",
    UiCopyKey.OLLAMA_URL: "Local URL:",
    UiCopyKey.OLLAMA_STATUS: "Status:",
    UiCopyKey.OLLAMA_VERSION: "Detected version:",
    UiCopyKey.OLLAMA_MODEL: "Model:",
    UiCopyKey.OLLAMA_GROUP: "Local Ollama",
    UiCopyKey.OLLAMA_EXPLANATION: (
        "The application connects to Ollama automatically and prioritizes {model}. Use Reconnect "
        "to repeat the check."
    ),
    UiCopyKey.OLLAMA_CONNECTING: "Connecting to Ollama automatically…",
    UiCopyKey.OLLAMA_NO_MODELS: "Connection succeeded, but Ollama reported no installed models.",
    UiCopyKey.OLLAMA_CONNECTED: "Connected automatically with {model}.",
    UiCopyKey.OLLAMA_PREFERRED_MISSING: (
        "Connection succeeded, but {model} was not found. An available local model was selected."
    ),
    UiCopyKey.OLLAMA_SAVED: "Configuration saved for model {model}.",
}

DANISH_UI_COPY: dict[UiCopyKey, str] = {
    UiCopyKey.REVIEW_PLACEHOLDER: (
        "Repetitionsmotoren vil omfatte aktiv genkaldelse, variation og tidsfordelt repetition."
    ),
    UiCopyKey.ASSESSMENTS_PLACEHOLDER: (
        "Evalueringer vil omfatte ét svar, flere svar, udfyldning, matching, rækkefølge, kode og mundtlig forklaring."
    ),
    UiCopyKey.FLASHCARDS_PLACEHOLDER: (
        "Huskekort vil dække begreber, formler, kode, almindelige fejl og forbindelser mellem kurser."
    ),
    UiCopyKey.GLOSSARY_PLACEHOLDER: "Ordlisten udbygges sammen med hvert fagligt modul.",
    UiCopyKey.COURSE_STRUCTURE_HEADING: "Kursets egen struktur",
    UiCopyKey.COURSE_STRUCTURE_NOTICE: (
        "Denne skærm bekræfter det valgte kursus. Moduler og fagligt indhold tilføjes i separate leverancer."
    ),
    UiCopyKey.MODULE_OBJECTIVE_SECTION: "Tilfældig objektiv træning",
    UiCopyKey.MODULE_COMPLETE_ASSESSMENT: "Komplet modulevaluering",
    UiCopyKey.MODULE_COMPLETE_ASSESSMENT_NOTICE: (
        "Aktiviteterne dækker kodegennemgang, fejlfinding, rækkefølge, matching af begreber, kode, "
        "fortolkning og åbne svar. Løsningerne holdes adskilt fra læseren for at bevare evalueringens formål."
    ),
    UiCopyKey.PRACTICE_NUMBER: "Øvelse {number}",
    UiCopyKey.PRACTICE_YOUR_ANSWER: "Dit svar",
    UiCopyKey.PRACTICE_ANSWER_PLACEHOLDER: (
        "Skriv dit ræsonnement, din gennemgangstabel, kode eller forklaring her."
    ),
    UiCopyKey.PRACTICE_SHOW_HINT: "Vis ledetråd",
    UiCopyKey.PRACTICE_SHOW_NEXT_HINT: "Vis næste ledetråd",
    UiCopyKey.PRACTICE_NO_MORE_HINTS: "Ingen flere ledetråde",
    UiCopyKey.PRACTICE_REFERENCE_BUTTON: "Vis referenceløsning",
    UiCopyKey.PRACTICE_REFERENCE_TITLE: "Referenceløsning",
    UiCopyKey.PRACTICE_WHY: "Hvorfor",
    UiCopyKey.PRACTICE_SELF_ASSESSMENT: "Selvevaluering:",
    UiCopyKey.PRACTICE_SOLVED: "Jeg løste den",
    UiCopyKey.PRACTICE_REVIEW: "Jeg skal repetere",
    UiCopyKey.PRACTICE_SOLUTION_VISIBLE: "Løsning synlig",
    UiCopyKey.PRACTICE_HINT_NUMBER: "Ledetråd {number}: {hint}",
    UiCopyKey.PRACTICE_TITLE: "Tilfældig guidet træning",
    UiCopyKey.PRACTICE_NEW_SESSION: "Ny træning",
    UiCopyKey.PRACTICE_METADATA: (
        "{count} øvelser valgt fra en bank med {bank}. Kombinationen og rækkefølgen ændres mellem sessioner."
    ),
    UiCopyKey.PRACTICE_PROGRESS: (
        "{solved} løst · {review} til repetition · {assessed}/{total} vurderet"
    ),
    UiCopyKey.OBJECTIVE_QUESTION_NUMBER: "Spørgsmål {number}",
    UiCopyKey.OBJECTIVE_CHECK: "Kontrollér svar",
    UiCopyKey.OBJECTIVE_SELECT_WARNING: "Vælg et svar før kontrollen.",
    UiCopyKey.OBJECTIVE_CORRECT: "Korrekt. {explanation}",
    UiCopyKey.OBJECTIVE_INCORRECT: (
        "Forkert. Korrekt svar: {answer}. {explanation}"
    ),
    UiCopyKey.OBJECTIVE_TITLE: "Tilfældig objektiv evaluering",
    UiCopyKey.OBJECTIVE_NEW_SESSION: "Ny træning",
    UiCopyKey.OBJECTIVE_METADATA: (
        "{count} spørgsmål valgt fra en bank med {bank}. Sæt, rækkefølge og svarmuligheder ændres mellem sessioner."
    ),
    UiCopyKey.OBJECTIVE_SCORE: "{correct} korrekte · {answered}/{total}",
    UiCopyKey.OLLAMA_RECONNECT: "Forbind igen",
    UiCopyKey.OLLAMA_PENDING: "Forbindelse afventer.",
    UiCopyKey.OLLAMA_SAVE: "Gem konfiguration",
    UiCopyKey.OLLAMA_URL: "Lokal URL:",
    UiCopyKey.OLLAMA_STATUS: "Status:",
    UiCopyKey.OLLAMA_VERSION: "Registreret version:",
    UiCopyKey.OLLAMA_MODEL: "Model:",
    UiCopyKey.OLLAMA_GROUP: "Lokal Ollama",
    UiCopyKey.OLLAMA_EXPLANATION: (
        "Programmet opretter automatisk forbindelse til Ollama og prioriterer {model}. Brug Forbind igen for at gentage kontrollen."
    ),
    UiCopyKey.OLLAMA_CONNECTING: "Opretter automatisk forbindelse til Ollama…",
    UiCopyKey.OLLAMA_NO_MODELS: "Forbindelsen lykkedes, men Ollama rapporterede ingen installerede modeller.",
    UiCopyKey.OLLAMA_CONNECTED: "Automatisk forbundet med {model}.",
    UiCopyKey.OLLAMA_PREFERRED_MISSING: (
        "Forbindelsen lykkedes, men {model} blev ikke fundet. En tilgængelig lokal model blev valgt."
    ),
    UiCopyKey.OLLAMA_SAVED: "Konfiguration gemt for modellen {model}.",
}

_UI_CATALOGS = {
    AppLocale.SPANISH_SPAIN: SPANISH_UI_COPY,
    AppLocale.ENGLISH: ENGLISH_UI_COPY,
    AppLocale.DANISH_DENMARK: DANISH_UI_COPY,
}
_FORMATTER = Formatter()


def ui_text(locale: AppLocale | str, key: UiCopyKey, **values: object) -> str:
    """Return one validated localized interactive string."""
    resolved = locale if isinstance(locale, AppLocale) else AppLocale.resolve(locale)
    template = _UI_CATALOGS[resolved][key]
    expected = {
        field_name.split(".", maxsplit=1)[0].split("[", maxsplit=1)[0]
        for _, field_name, _, _ in _FORMATTER.parse(template)
        if field_name
    }
    if expected != set(values):
        raise ValueError(
            f"Invalid values for {key.value}: expected={sorted(expected)}, actual={sorted(values)}"
        )
    return template.format(**values)


def validate_ui_copy() -> None:
    """Require exact non-empty coverage and identical placeholders."""
    expected_keys = set(UiCopyKey)
    reference = SPANISH_UI_COPY
    for locale, catalog in _UI_CATALOGS.items():
        if set(catalog) != expected_keys:
            raise ValueError(f"Incomplete UI copy for {locale.value}.")
        for key in expected_keys:
            if not catalog[key].strip():
                raise ValueError(f"Empty UI copy for {locale.value}: {key.value}")
            reference_fields = {
                field_name for _, field_name, _, _ in _FORMATTER.parse(reference[key]) if field_name
            }
            localized_fields = {
                field_name for _, field_name, _, _ in _FORMATTER.parse(catalog[key]) if field_name
            }
            if localized_fields != reference_fields:
                raise ValueError(f"Placeholder mismatch for {locale.value}: {key.value}")


validate_ui_copy()

__all__ = ["UiCopyKey", "ui_text", "validate_ui_copy"]
