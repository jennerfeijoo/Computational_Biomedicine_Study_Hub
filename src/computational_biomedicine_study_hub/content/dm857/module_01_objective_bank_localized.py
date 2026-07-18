"""Complete trilingual objective-question bank for DM857 module 1."""

from __future__ import annotations

from ...i18n import AppLocale
from ..localized_models import LocalizedAssessmentItem, LocalizedAssessmentOption, LocalizedText
from ..models import AssessmentItem
from .module_01_objective_bank import OBJECTIVE_QUESTION_BANK as _ES_BANK


def _t(spanish: str, english: str, danish: str) -> LocalizedText:
    return LocalizedText(spanish=spanish, english=english, danish=danish)


_BANK_TRANSLATIONS = (
    (
        "Which sequence best represents the path from a real situation to executable code?",
        (
            "Problem → model → algorithm → program",
            "Program → algorithm → model → problem",
            "Model → problem → program → algorithm",
            "Algorithm → program → problem → model",
        ),
        "First delimit the problem, then model it, design an algorithm, and implement it as a program.",
        "Hvilken rækkefølge beskriver bedst vejen fra en virkelig situation til kode, der kan køres?",
        (
            "Problem → model → algoritme → program",
            "Program → algoritme → model → problem",
            "Model → problem → program → algoritme",
            "Algoritme → program → problem → model",
        ),
        "Først afgrænses problemet, derefter modelleres det, en algoritme designes, og den implementeres som et program.",
    ),
    (
        "What is the main role of a computational model in this module?",
        (
            "Retain relevant variables and relationships",
            "Copy every detail of reality",
            "Replace program tests",
            "Choose Python syntax automatically",
        ),
        "A model retains only the information needed to produce a verifiable answer.",
        "Hvad er en computationel models vigtigste rolle i dette modul?",
        (
            "Bevare relevante variable og relationer",
            "Kopiere alle detaljer fra virkeligheden",
            "Erstatte programtest",
            "Vælge Python-syntaks automatisk",
        ),
        "En model bevarer kun den information, der er nødvendig for at give et efterprøveligt svar.",
    ),
    (
        "An expression is code that Python can evaluate to produce a value.",
        ("True", "False"),
        "An expression combines evaluable elements and produces a concrete value.",
        "Et udtryk er kode, som Python kan evaluere for at frembringe en værdi.",
        ("Sandt", "Falsk"),
        "Et udtryk kombinerer elementer, der kan evalueres, og giver en konkret værdi.",
    ),
    (
        "What are the value and type of 9 / 3 in Python?",
        ("3.0, float", "3, int", "3.0, int", "9/3, str"),
        "/ performs true division and returns float even when the division is exact.",
        "Hvad er værdien og typen af 9 / 3 i Python?",
        ("3.0, float", "3, int", "3.0, int", "9/3, str"),
        "/ udfører reel division og returnerer float, selv når divisionen går op.",
    ),
    (
        "What is the result of 9 // 4?",
        ("2", "2.25", "3", "1"),
        "// performs floor division.",
        "Hvad er resultatet af 9 // 4?",
        ("2", "2.25", "3", "1"),
        "// udfører heltalsdivision nedad.",
    ),
    (
        "input() returns an integer when the user types only digits.",
        ("True", "False"),
        "input() returns str; numeric conversion must be explicit.",
        "input() returnerer et heltal, når brugeren kun skriver cifre.",
        ("Sandt", "Falsk"),
        "input() returnerer str; numerisk konvertering skal være eksplicit.",
    ),
    (
        "What does int(4.9) produce?",
        ("4", "5", "4.9", "TypeError"),
        "int() removes the fractional part toward zero; it does not round to the nearest integer.",
        "Hvad giver int(4.9)?",
        ("4", "5", "4.9", "TypeError"),
        "int() fjerner decimaldelen mod nul; den afrunder ikke til nærmeste heltal.",
    ),
    (
        "The ^ operator represents exponentiation in Python.",
        ("True", "False"),
        "Exponentiation is written **; ^ is a bitwise operation.",
        "Operatoren ^ repræsenterer potens i Python.",
        ("Sandt", "Falsk"),
        "Potens skrives **; ^ er en bitvis operation.",
    ),
    (
        "How should x = x + 1 be interpreted?",
        (
            "Evaluate x + 1, then reassign x",
            "It is mathematical equality",
            "Increment x before evaluation",
            "Create a second variable x",
        ),
        "The right-hand side is evaluated using the current state and x is then updated.",
        "Hvordan skal x = x + 1 fortolkes?",
        (
            "Evaluér x + 1, og gentildel derefter x",
            "Det er matematisk lighed",
            "Øg x før evaluering",
            "Opret en anden variabel x",
        ),
        "Højresiden evalueres med den aktuelle tilstand, og derefter opdateres x.",
    ),
    (
        "What does x = 4; y = x + 2; x = 10; print(y) print?",
        ("6", "12", "10", "4"),
        "y stores 6 before x is reassigned.",
        "Hvad udskriver x = 4; y = x + 2; x = 10; print(y)?",
        ("6", "12", "10", "4"),
        "y gemmer 6, før x gentildeles.",
    ),
    (
        "Reassigning x automatically updates every variable previously calculated from x.",
        ("True", "False"),
        "Variables keep the value assigned to them.",
        "Gentildeling af x opdaterer automatisk alle variable, der tidligere er beregnet ud fra x.",
        ("Sandt", "Falsk"),
        "Variable bevarer den værdi, de fik tildelt.",
    ),
    (
        "What happens when '12' + 3 is executed?",
        (
            "TypeError from combining str and int",
            "The result is 15",
            "The result is '123'",
            "SyntaxError",
        ),
        "Direct addition between str and int is not defined.",
        "Hvad sker der, når '12' + 3 køres?",
        (
            "TypeError ved kombination af str og int",
            "Resultatet er 15",
            "Resultatet er '123'",
            "SyntaxError",
        ),
        "Direkte addition mellem str og int er ikke defineret.",
    ),
    (
        "Which situation describes a logic error?",
        (
            "Using 100 instead of 1000 to convert mL to µL without an exception",
            "An unclosed parenthesis",
            "Dividing by zero",
            "Adding str and int",
        ),
        "The program executes, but the result violates the specification.",
        "Hvilken situation beskriver en logisk fejl?",
        (
            "At bruge 100 i stedet for 1000 ved konvertering fra mL til µL uden undtagelse",
            "En parentes, der ikke er lukket",
            "Division med nul",
            "Addition af str og int",
        ),
        "Programmet kører, men resultatet bryder specifikationen.",
    ),
    (
        "What minimum information turns an execution into a test?",
        (
            "Input, expected result, and comparison criterion",
            "Only source code",
            "An input without an expected result",
            "The absence of errors",
        ),
        "A test compares an observed result with an expected result for a concrete input.",
        "Hvilken minimal information gør en kørsel til en test?",
        (
            "Input, forventet resultat og sammenligningskriterium",
            "Kun kildekoden",
            "Et input uden forventet resultat",
            "Fravær af fejl",
        ),
        "En test sammenligner et observeret resultat med et forventet resultat for et konkret input.",
    ),
    (
        "The absence of exceptions proves that a program is correct.",
        ("True", "False"),
        "A logic error may exist even when the program finishes.",
        "Fravær af undtagelser beviser, at et program er korrekt.",
        ("Sandt", "Falsk"),
        "Der kan være en logisk fejl, selv om programmet afslutter.",
    ),
    (
        "Which name best reduces the risk of confusing units?",
        ("total_volume_ul", "value", "number", "x"),
        "The name includes meaning and unit.",
        "Hvilket navn reducerer bedst risikoen for at forveksle enheder?",
        ("total_volume_ul", "value", "number", "x"),
        "Navnet indeholder betydning og enhed.",
    ),
    (
        "What is the result of 8 + 4 * 3?",
        ("20", "36", "24", "12"),
        "Multiplication is evaluated before addition.",
        "Hvad er resultatet af 8 + 4 * 3?",
        ("20", "36", "24", "12"),
        "Multiplikation evalueres før addition.",
    ),
    (
        "What is the result of (8 + 4) * 3?",
        ("36", "20", "24", "15"),
        "Parentheses force addition before multiplication.",
        "Hvad er resultatet af (8 + 4) * 3?",
        ("36", "20", "24", "15"),
        "Parenteserne tvinger addition før multiplikation.",
    ),
    (
        "A variable can refer to values of different types at different times.",
        ("True", "False"),
        "Python is dynamically typed, although every value has a concrete type.",
        "En variabel kan henvise til værdier af forskellige typer på forskellige tidspunkter.",
        ("Sandt", "Falsk"),
        "Python er dynamisk typet, selv om hver værdi har en konkret type.",
    ),
    (
        "Why is it appropriate to convert to int at the end of the usable-read calculation?",
        (
            "The result is a count and the calculation may require float",
            "int always improves precision",
            "Python does not allow int times float",
            "All biomedical data must be integers",
        ),
        "The conversion follows the meaning of the result; decimals may need to be preserved during calculation.",
        "Hvorfor er det passende at konvertere til int til sidst i beregningen af anvendelige reads?",
        (
            "Resultatet er et antal, og beregningen kan kræve float",
            "int forbedrer altid præcisionen",
            "Python tillader ikke int gange float",
            "Alle biomedicinske data skal være heltal",
        ),
        "Konverteringen følger resultatets betydning; decimaler kan være nødvendige under beregningen.",
    ),
)


def _localized_item(index: int) -> LocalizedAssessmentItem:
    source = _ES_BANK[index]
    prompt_en, options_en, explanation_en, prompt_da, options_da, explanation_da = (
        _BANK_TRANSLATIONS[index]
    )
    correct_indexes = tuple(source.options.index(answer) for answer in source.correct_answers)
    option_ids = tuple(f"o{position}" for position in range(len(source.options)))
    return LocalizedAssessmentItem(
        item_id=source.item_id,
        activity_type=source.activity_type,
        prompt=_t(source.prompt, prompt_en, prompt_da),
        options=tuple(
            LocalizedAssessmentOption(
                option_id=option_id,
                text=_t(spanish, english, danish),
            )
            for option_id, spanish, english, danish in zip(
                option_ids,
                source.options,
                options_en,
                options_da,
                strict=True,
            )
        ),
        correct_option_ids=tuple(option_ids[position] for position in correct_indexes),
        accepted_answers=(),
        explanation=_t(source.explanation, explanation_en, explanation_da),
    )


LOCALIZED_OBJECTIVE_QUESTION_BANK = tuple(_localized_item(index) for index in range(len(_ES_BANK)))


def materialize_objective_question_bank(
    locale: AppLocale | str,
) -> tuple[AssessmentItem, ...]:
    """Create the deterministic objective bank in one selected language."""
    resolved = locale if isinstance(locale, AppLocale) else AppLocale.resolve(locale)
    return tuple(item.materialize(resolved) for item in LOCALIZED_OBJECTIVE_QUESTION_BANK)


__all__ = ["LOCALIZED_OBJECTIVE_QUESTION_BANK", "materialize_objective_question_bank"]
