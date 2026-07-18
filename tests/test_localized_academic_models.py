from __future__ import annotations

import pytest

from computational_biomedicine_study_hub.content import (
    LocalizedAssessmentItem,
    LocalizedAssessmentOption,
    LocalizedConceptBlock,
    LocalizedLearningModule,
    LocalizedLearningObjective,
    LocalizedPracticeExercise,
    LocalizedText,
    LocalizedTutorSupportPacket,
    LocalizedWorkedExample,
)
from computational_biomedicine_study_hub.i18n import AppLocale
from computational_biomedicine_study_hub.learning.activity_types import ActivityType


def _text(spanish: str, english: str, danish: str) -> LocalizedText:
    return LocalizedText(spanish=spanish, english=english, danish=danish)


def _localized_module() -> LocalizedLearningModule:
    true_option = LocalizedAssessmentOption(
        "true",
        _text("Verdadero", "True", "Sandt"),
    )
    false_option = LocalizedAssessmentOption(
        "false",
        _text("Falso", "False", "Falsk"),
    )
    return LocalizedLearningModule(
        course_code="DM857",
        module_id="dm857.m01",
        title=_text("Variables", "Variables", "Variabler"),
        summary=_text(
            "Estudia valores y estado.",
            "Study values and state.",
            "Studér værdier og tilstand.",
        ),
        objectives=(
            LocalizedLearningObjective(
                "objective-1",
                _text(
                    "Explicar una asignación.",
                    "Explain an assignment.",
                    "Forklar en tildeling.",
                ),
            ),
        ),
        concepts=(
            LocalizedConceptBlock(
                concept_id="assignment",
                title=_text("Asignación", "Assignment", "Tildeling"),
                body=_text(
                    "Una asignación actualiza el estado.",
                    "An assignment updates state.",
                    "En tildeling opdaterer tilstanden.",
                ),
                key_points=(
                    _text(
                        "El nombre referencia un valor.",
                        "The name refers to a value.",
                        "Navnet henviser til en værdi.",
                    ),
                ),
            ),
        ),
        worked_examples=(
            LocalizedWorkedExample(
                example_id="example-1",
                title=_text("Contador", "Counter", "Tæller"),
                problem=_text(
                    "Incrementa un contador.",
                    "Increment a counter.",
                    "Forøg en tæller.",
                ),
                reasoning=(
                    _text(
                        "Lee el valor anterior.",
                        "Read the previous value.",
                        "Læs den forrige værdi.",
                    ),
                ),
                code=_text(
                    "count = 1\ncount += 1", "count = 1\ncount += 1", "count = 1\ncount += 1"
                ),
                expected_output=_text("2", "2", "2"),
                explanation=_text(
                    "El estado final contiene 2.",
                    "The final state contains 2.",
                    "Den endelige tilstand indeholder 2.",
                ),
            ),
        ),
        practice_exercises=(
            LocalizedPracticeExercise(
                exercise_id="practice-1",
                activity_type=ActivityType.CODE_TRACING,
                prompt=_text(
                    "Traza el código.",
                    "Trace the code.",
                    "Gennemgå koden.",
                ),
                hints=(
                    _text(
                        "Anota cada asignación.",
                        "Write down each assignment.",
                        "Notér hver tildeling.",
                    ),
                ),
                solution=_text("El resultado es 2.", "The result is 2.", "Resultatet er 2."),
                explanation=_text(
                    "La segunda instrucción incrementa el valor.",
                    "The second statement increments the value.",
                    "Den anden sætning øger værdien.",
                ),
                starter_code=_text("count = 1", "count = 1", "count = 1"),
            ),
        ),
        assessment_items=(
            LocalizedAssessmentItem(
                item_id="assessment-1",
                activity_type=ActivityType.TRUE_FALSE,
                prompt=_text(
                    "Una asignación puede cambiar el estado.",
                    "An assignment can change state.",
                    "En tildeling kan ændre tilstanden.",
                ),
                options=(true_option, false_option),
                correct_option_ids=("true",),
                accepted_answers=(),
                explanation=_text(
                    "La variable puede recibir otro valor.",
                    "The variable can receive another value.",
                    "Variablen kan få en anden værdi.",
                ),
            ),
        ),
        tutor_support=LocalizedTutorSupportPacket(
            canonical_explanation=_text(
                "El estado reúne los valores actuales.",
                "State contains current values.",
                "Tilstanden indeholder de aktuelle værdier.",
            ),
            knowledge_fragments=(
                _text("Asignar actualiza.", "Assignment updates.", "Tildeling opdaterer."),
            ),
            common_misconceptions=(
                _text(
                    "Confundir asignación con igualdad.",
                    "Confusing assignment with equality.",
                    "At forveksle tildeling med lighed.",
                ),
            ),
            socratic_questions=(
                _text(
                    "¿Qué valor tenía antes?",
                    "What value did it have before?",
                    "Hvilken værdi havde den før?",
                ),
            ),
            grading_criteria=(
                _text(
                    "Identifica el estado inicial.",
                    "Identify the initial state.",
                    "Identificér den oprindelige tilstand.",
                ),
            ),
            response_constraints=(
                _text(
                    "No inventar contenido.",
                    "Do not invent content.",
                    "Opfind ikke indhold.",
                ),
            ),
            source_basis=("Think Python, 3rd ed.",),
        ),
    )


def test_localized_text_requires_every_language_to_be_non_empty() -> None:
    with pytest.raises(ValueError, match="da-DK"):
        LocalizedText(spanish="Texto", english="Text", danish="   ")


def test_module_materializes_complete_runtime_content_in_each_locale() -> None:
    module = _localized_module()

    spanish = module.materialize(AppLocale.SPANISH_SPAIN)
    english = module.materialize("en-GB")
    danish = module.materialize("da_DK")

    assert spanish.title == "Variables"
    assert english.summary == "Study values and state."
    assert danish.concepts[0].title == "Tildeling"
    assert danish.practice_exercises[0].hints == ("Notér hver tildeling.",)
    assert english.tutor_support.response_constraints == ("Do not invent content.",)


def test_assessment_grading_identity_is_stable_across_languages() -> None:
    module = _localized_module()

    spanish_item = module.materialize("es-ES").assessment_items[0]
    english_item = module.materialize("en").assessment_items[0]
    danish_item = module.materialize("da-DK").assessment_items[0]

    assert spanish_item.correct_answers == ("Verdadero",)
    assert english_item.correct_answers == ("True",)
    assert danish_item.correct_answers == ("Sandt",)
    assert spanish_item.options == ("Verdadero", "Falso")
    assert english_item.options == ("True", "False")


def test_assessment_rejects_unknown_correct_option_ids() -> None:
    option = LocalizedAssessmentOption("yes", _text("Sí", "Yes", "Ja"))

    with pytest.raises(ValueError, match="unknown option IDs"):
        LocalizedAssessmentItem(
            item_id="invalid",
            activity_type=ActivityType.MULTIPLE_CHOICE,
            prompt=_text("Pregunta", "Question", "Spørgsmål"),
            options=(option,),
            correct_option_ids=("missing",),
            accepted_answers=(),
            explanation=_text("Explicación", "Explanation", "Forklaring"),
        )


def test_free_text_items_use_localized_accepted_answers() -> None:
    item = LocalizedAssessmentItem(
        item_id="short-answer",
        activity_type=ActivityType.SHORT_ANSWER,
        prompt=_text("Define estado.", "Define state.", "Definér tilstand."),
        options=(),
        correct_option_ids=(),
        accepted_answers=(
            _text(
                "Valores actuales",
                "Current values",
                "Aktuelle værdier",
            ),
        ),
        explanation=_text("Explicación", "Explanation", "Forklaring"),
    )

    assert item.materialize(AppLocale.DANISH_DENMARK).correct_answers == ("Aktuelle værdier",)


def test_localized_module_rejects_duplicate_stable_ids() -> None:
    module = _localized_module()
    duplicate = module.objectives[0]

    with pytest.raises(ValueError, match="Duplicate localized objective IDs"):
        LocalizedLearningModule(
            course_code=module.course_code,
            module_id=module.module_id,
            title=module.title,
            summary=module.summary,
            objectives=(duplicate, duplicate),
            concepts=module.concepts,
            worked_examples=module.worked_examples,
            practice_exercises=module.practice_exercises,
            assessment_items=module.assessment_items,
            tutor_support=module.tutor_support,
        )
