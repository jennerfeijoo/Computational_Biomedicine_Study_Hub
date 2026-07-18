from __future__ import annotations

from computational_biomedicine_study_hub.content.dm857 import (
    LOCALIZED_MODULE_01_FOUNDATIONS,
    LOCALIZED_OBJECTIVE_QUESTION_BANK,
    MODULE_01_FOUNDATIONS,
    OBJECTIVE_QUESTION_BANK,
    materialize_objective_question_bank,
)
from computational_biomedicine_study_hub.i18n import AppLocale


def test_module_one_materializes_complete_content_in_every_locale() -> None:
    modules = {locale: LOCALIZED_MODULE_01_FOUNDATIONS.materialize(locale) for locale in AppLocale}

    for module in modules.values():
        assert len(module.objectives) == 6
        assert len(module.concepts) == 6
        assert len(module.worked_examples) == 3
        assert len(module.practice_exercises) == 8
        assert len(module.assessment_items) == 10
        assert len(module.tutor_documents()) == 29
        assert all(document.text.strip() for document in module.tutor_documents())

    assert modules[AppLocale.SPANISH_SPAIN].title.startswith("Resolución")
    assert modules[AppLocale.ENGLISH].title.startswith("Problem solving")
    assert modules[AppLocale.DANISH_DENMARK].title.startswith("Problemløsning")


def test_spanish_runtime_module_matches_localized_source() -> None:
    expected = LOCALIZED_MODULE_01_FOUNDATIONS.materialize(AppLocale.SPANISH_SPAIN)

    assert MODULE_01_FOUNDATIONS == expected
    assert "proceso de secuenciación" in MODULE_01_FOUNDATIONS.worked_examples[0].title
    exported_text = " ".join(
        document.text.casefold() for document in MODULE_01_FOUNDATIONS.tutor_documents()
    )
    assert "corrida" not in exported_text


def test_assessment_correctness_is_stable_across_languages() -> None:
    modules = [LOCALIZED_MODULE_01_FOUNDATIONS.materialize(locale) for locale in AppLocale]

    item_ids = [tuple(item.item_id for item in module.assessment_items) for module in modules]
    assert item_ids[0] == item_ids[1] == item_ids[2]

    spanish_true_false = modules[0].assessment_items[1]
    english_true_false = modules[1].assessment_items[1]
    danish_true_false = modules[2].assessment_items[1]

    assert spanish_true_false.correct_answers == ("Falso",)
    assert english_true_false.correct_answers == ("False",)
    assert danish_true_false.correct_answers == ("Falsk",)


def test_objective_question_bank_is_complete_in_every_locale() -> None:
    assert len(LOCALIZED_OBJECTIVE_QUESTION_BANK) == 20

    banks = {locale: materialize_objective_question_bank(locale) for locale in AppLocale}
    for bank in banks.values():
        assert len(bank) == 20
        assert len({item.item_id for item in bank}) == 20
        assert all(item.options for item in bank)
        assert all(item.correct_answers for item in bank)

    assert banks[AppLocale.SPANISH_SPAIN] == OBJECTIVE_QUESTION_BANK
    assert banks[AppLocale.SPANISH_SPAIN][2].correct_answers == ("Verdadero",)
    assert banks[AppLocale.ENGLISH][2].correct_answers == ("True",)
    assert banks[AppLocale.DANISH_DENMARK][2].correct_answers == ("Sandt",)


def test_every_localized_visible_field_is_non_empty() -> None:
    module = LOCALIZED_MODULE_01_FOUNDATIONS

    texts = [module.title, module.summary]
    texts.extend(objective.statement for objective in module.objectives)
    for concept in module.concepts:
        texts.extend((concept.title, concept.body, *concept.key_points))
    for example in module.worked_examples:
        texts.extend(
            (
                example.title,
                example.problem,
                *example.reasoning,
                example.code,
                example.expected_output,
                example.explanation,
            )
        )
    for exercise in module.practice_exercises:
        texts.extend((exercise.prompt, *exercise.hints, exercise.solution, exercise.explanation))
        if exercise.starter_code is not None:
            texts.append(exercise.starter_code)
    for item in (*module.assessment_items, *LOCALIZED_OBJECTIVE_QUESTION_BANK):
        texts.extend((item.prompt, item.explanation, *item.accepted_answers, *item.rubric))
        texts.extend(option.text for option in item.options)

    assert texts
    for text in texts:
        assert all(value.strip() for value in text.as_dict().values())
