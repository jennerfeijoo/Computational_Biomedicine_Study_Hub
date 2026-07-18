"""Trilingual objective-question bank for DM857 module 2."""

from __future__ import annotations

from ...i18n import AppLocale
from ...learning.activity_types import ActivityType
from ..localized_models import (
    LocalizedAssessmentItem,
    LocalizedAssessmentOption,
    LocalizedText,
)
from ..models import AssessmentItem


def _t(spanish: str, english: str, danish: str) -> LocalizedText:
    return LocalizedText(spanish=spanish, english=english, danish=danish)


def _option(
    option_id: str,
    spanish: str,
    english: str,
    danish: str,
) -> LocalizedAssessmentOption:
    return LocalizedAssessmentOption(option_id=option_id, text=_t(spanish, english, danish))


def _mcq(
    item_id: str,
    prompt: LocalizedText,
    options: tuple[LocalizedAssessmentOption, ...],
    correct_option_id: str,
    explanation: LocalizedText,
) -> LocalizedAssessmentItem:
    return LocalizedAssessmentItem(
        item_id=item_id,
        activity_type=ActivityType.MULTIPLE_CHOICE,
        prompt=prompt,
        options=options,
        correct_option_ids=(correct_option_id,),
        accepted_answers=(),
        explanation=explanation,
    )


def _tf(
    item_id: str,
    prompt: LocalizedText,
    *,
    correct: bool,
    explanation: LocalizedText,
) -> LocalizedAssessmentItem:
    return LocalizedAssessmentItem(
        item_id=item_id,
        activity_type=ActivityType.TRUE_FALSE,
        prompt=prompt,
        options=(
            _option("true", "Verdadero", "True", "Sandt"),
            _option("false", "Falso", "False", "Falsk"),
        ),
        correct_option_ids=(("true",) if correct else ("false",)),
        accepted_answers=(),
        explanation=explanation,
    )


LOCALIZED_OBJECTIVE_QUESTION_BANK_02: tuple[LocalizedAssessmentItem, ...] = (
    _mcq(
        "dm857.m02.bank.001",
        _t("¿Qué valor pertenece al tipo bool?", "Which value belongs to type bool?", "Hvilken værdi tilhører typen bool?"),
        (
            _option("true", "True", "True", "True"),
            _option("text", "'True'", "'True'", "'True'"),
            _option("one", "1.0", "1.0", "1.0"),
            _option("none", "None", "None", "None"),
        ),
        "true",
        _t("True es un valor booleano; 'True' es una cadena.", "True is Boolean; 'True' is a string.", "True er boolesk; 'True' er en tekststreng."),
    ),
    _tf(
        "dm857.m02.bank.002",
        _t("Un predicado es una expresión cuyo resultado es True o False.", "A predicate is an expression whose result is True or False.", "Et prædikat er et udtryk, hvis resultat er True eller False."),
        correct=True,
        explanation=_t("Los predicados producen valores de tipo bool.", "Predicates produce values of type bool.", "Prædikater giver værdier af typen bool."),
    ),
    _mcq(
        "dm857.m02.bank.003",
        _t("¿Qué operador compara igualdad?", "Which operator compares equality?", "Hvilken operator sammenligner lighed?"),
        (
            _option("eq", "==", "==", "=="),
            _option("assign", "=", "=", "="),
            _option("neq", "!=", "!=", "!="),
            _option("ge", ">=", ">=", ">="),
        ),
        "eq",
        _t("== compara dos valores; = realiza una asignación.", "== compares two values; = assigns.", "== sammenligner to værdier; = tildeler."),
    ),
    _tf(
        "dm857.m02.bank.004",
        _t("La expresión 10 <= x <= 20 incluye los valores 10 y 20.", "The expression 10 <= x <= 20 includes 10 and 20.", "Udtrykket 10 <= x <= 20 inkluderer 10 og 20."),
        correct=True,
        explanation=_t("<= es inclusivo en ambos límites.", "<= is inclusive at both boundaries.", "<= er inklusiv ved begge grænser."),
    ),
    _mcq(
        "dm857.m02.bank.005",
        _t("¿Cuál es el resultado de 7 != 7?", "What is the result of 7 != 7?", "Hvad er resultatet af 7 != 7?"),
        (
            _option("false", "False", "False", "False"),
            _option("true", "True", "True", "True"),
            _option("seven", "7", "7", "7"),
            _option("error", "Error", "Error", "Fejl"),
        ),
        "false",
        _t("Ambos valores son iguales, por lo que la desigualdad es False.", "The values are equal, so inequality is False.", "Værdierne er ens, så ulighed er False."),
    ),
    _mcq(
        "dm857.m02.bank.006",
        _t("¿Cuándo produce True la expresión A and B?", "When is A and B True?", "Hvornår er A and B True?"),
        (
            _option("both", "Cuando A y B son True", "When A and B are True", "Når A og B er True"),
            _option("either", "Cuando al menos una es True", "When at least one is True", "Når mindst én er True"),
            _option("a_false", "Cuando A es False", "When A is False", "Når A er False"),
            _option("different", "Cuando son diferentes", "When they differ", "Når de er forskellige"),
        ),
        "both",
        _t("and exige que ambos operandos sean verdaderos.", "and requires both operands to be true.", "and kræver, at begge operander er sande."),
    ),
    _mcq(
        "dm857.m02.bank.007",
        _t("¿Cuándo produce False la expresión A or B?", "When is A or B False?", "Hvornår er A or B False?"),
        (
            _option("both_false", "Cuando A y B son False", "When A and B are False", "Når A og B er False"),
            _option("a_false", "Cuando solo A es False", "When only A is False", "Når kun A er False"),
            _option("b_false", "Cuando solo B es False", "When only B is False", "Når kun B er False"),
            _option("both_true", "Cuando ambas son True", "When both are True", "Når begge er True"),
        ),
        "both_false",
        _t("or solo es False cuando ninguno de sus operandos es verdadero.", "or is False only when neither operand is true.", "or er kun False, når ingen operand er sand."),
    ),
    _mcq(
        "dm857.m02.bank.008",
        _t("¿Cuál es la precedencia lógica de mayor a menor?", "What is logical precedence from highest to lowest?", "Hvad er den logiske præcedens fra højeste til laveste?"),
        (
            _option("correct", "not, and, or", "not, and, or", "not, and, or"),
            _option("reverse", "or, and, not", "or, and, not", "or, and, not"),
            _option("and_first", "and, not, or", "and, not, or", "and, not, or"),
            _option("same", "Todos tienen la misma", "All are equal", "Alle er ens"),
        ),
        "correct",
        _t("not se evalúa antes que and, y and antes que or.", "not is evaluated before and, and and before or.", "not evalueres før and, og and før or."),
    ),
    _tf(
        "dm857.m02.bank.009",
        _t("Los paréntesis pueden aclarar una condición aunque la precedencia ya determine el resultado.", "Parentheses can clarify a condition even when precedence already determines the result.", "Parenteser kan tydeliggøre en betingelse, selv når præcedensen allerede bestemmer resultatet."),
        correct=True,
        explanation=_t("Los paréntesis también documentan la intención lógica.", "Parentheses also document logical intent.", "Parenteser dokumenterer også den logiske hensigt."),
    ),
    _mcq(
        "dm857.m02.bank.010",
        _t("En condición usa valid and has_control. ¿Qué significa?", "A condition uses valid and has_control. What does it mean?", "En betingelse bruger valid and has_control. Hvad betyder det?"),
        (
            _option("both", "Ambas propiedades deben ser True", "Both properties must be True", "Begge egenskaber skal være True"),
            _option("either", "Basta con una propiedad True", "Either property is enough", "Én sand egenskab er nok"),
            _option("inverse", "Se niegan ambas propiedades", "Both properties are negated", "Begge egenskaber benægtes"),
            _option("compare", "Se comparan como texto", "They are compared as text", "De sammenlignes som tekst"),
        ),
        "both",
        _t("and representa requisitos simultáneos.", "and represents simultaneous requirements.", "and repræsenterer samtidige krav."),
    ),
    _tf(
        "dm857.m02.bank.011",
        _t("En comparación encadenada puede escribirse como 0 <= percentage <= 100.", "A chained comparison can be written as 0 <= percentage <= 100.", "En kædet sammenligning kan skrives som 0 <= percentage <= 100."),
        correct=True,
        explanation=_t("Python permite expresar intervalos con comparaciones encadenadas.", "Python supports intervals through chained comparisons.", "Python understøtter intervaller gennem kædede sammenligninger."),
    ),
    _mcq(
        "dm857.m02.bank.012",
        _t("¿Qué ocurre en False and expensive_check()?", "What happens in False and expensive_check()?", "Hvad sker der i False and expensive_check()?"),
        (
            _option("skip", "expensive_check() no se evalúa", "expensive_check() is not evaluated", "expensive_check() evalueres ikke"),
            _option("run", "expensive_check() siempre se evalúa", "expensive_check() is always evaluated", "expensive_check() evalueres altid"),
            _option("syntax", "Se produce SyntaxError", "SyntaxError occurs", "SyntaxError opstår"),
            _option("none", "El resultado es None", "The result is None", "Resultatet er None"),
        ),
        "skip",
        _t("and se detiene tras un primer operando falso.", "and stops after a false first operand.", "and stopper efter en falsk første operand."),
    ),
    _mcq(
        "dm857.m02.bank.013",
        _t("¿Qué ocurre en True or expensive_check()?", "What happens in True or expensive_check()?", "Hvad sker der i True or expensive_check()?"),
        (
            _option("skip", "expensive_check() no se evalúa", "expensive_check() is not evaluated", "expensive_check() evalueres ikke"),
            _option("run", "expensive_check() se evalúa", "expensive_check() is evaluated", "expensive_check() evalueres"),
            _option("false", "El resultado es False", "The result is False", "Resultatet er False"),
            _option("error", "Se produce un error", "An error occurs", "Der opstår en fejl"),
        ),
        "skip",
        _t("or se detiene tras un primer operando verdadero.", "or stops after a true first operand.", "or stopper efter en sand første operand."),
    ),
    _mcq(
        "dm857.m02.bank.014",
        _t("¿Qué condición protege correctamente total / count?", "Which condition safely protects total / count?", "Hvilken betingelse beskytter total / count korrekt?"),
        (
            _option("safe", "count != 0 and total / count > 2", "count != 0 and total / count > 2", "count != 0 and total / count > 2"),
            _option("unsafe", "total / count > 2 and count != 0", "total / count > 2 and count != 0", "total / count > 2 and count != 0"),
            _option("or", "count != 0 or total / count > 2", "count != 0 or total / count > 2", "count != 0 or total / count > 2"),
            _option("not", "not count and total / count > 2", "not count and total / count > 2", "not count and total / count > 2"),
        ),
        "safe",
        _t("La condición guardián debe evaluarse antes de la división.", "The guard must be evaluated before division.", "Beskyttelsesbetingelsen skal evalueres før divisionen."),
    ),
    _tf(
        "dm857.m02.bank.015",
        _t("En cadena if-elif-else puede ejecutar dos ramas si ambas condiciones son True.", "An if-elif-else chain may execute two branches when both conditions are True.", "En if-elif-else-kæde kan udføre to grene, hvis begge betingelser er True."),
        correct=False,
        explanation=_t("Solo se ejecuta la primera rama verdadera.", "Only the first true branch executes.", "Kun den første sande gren udføres."),
    ),
    _mcq(
        "dm857.m02.bank.016",
        _t("¿Qué palabra cubre todos los casos restantes sin añadir otra condición?", "Which keyword covers all remaining cases without another condition?", "Hvilket nøgleord dækker alle resterende tilfælde uden en ny betingelse?"),
        (
            _option("else", "else", "else", "else"),
            _option("elif", "elif", "elif", "elif"),
            _option("if", "if", "if", "if"),
            _option("then", "then", "then", "then"),
        ),
        "else",
        _t("else no lleva condición y recibe los casos restantes.", "else has no condition and receives remaining cases.", "else har ingen betingelse og modtager de resterende tilfælde."),
    ),
    _mcq(
        "dm857.m02.bank.017",
        _t("Con score = 95, ¿qué orden clasifica correctamente >= 90 y >= 60?", "With score = 95, which order correctly classifies >= 90 and >= 60?", "Med score = 95, hvilken rækkefølge klassificerer >= 90 og >= 60 korrekt?"),
        (
            _option("specific", "Comprobar >= 90 antes de >= 60", "Check >= 90 before >= 60", "Kontrollér >= 90 før >= 60"),
            _option("general", "Comprobar >= 60 antes de >= 90", "Check >= 60 before >= 90", "Kontrollér >= 60 før >= 90"),
            _option("equal", "El orden no importa", "Order does not matter", "Rækkefølgen er ligegyldig"),
            _option("else", "Usar solo else", "Use only else", "Brug kun else"),
        ),
        "specific",
        _t("La condición general >= 60 también es verdadera para 95 y absorbería la rama específica.", "The general >= 60 condition is also true for 95 and would absorb the specific branch.", "Den generelle betingelse >= 60 er også sand for 95 og ville opsluge den specifikke gren."),
    ),
    _tf(
        "dm857.m02.bank.018",
        _t("La indentación determina qué sentencias pertenecen a una rama condicional.", "Indentation determines which statements belong to a conditional branch.", "Indrykning bestemmer, hvilke sætninger der tilhører en betinget gren."),
        correct=True,
        explanation=_t("La indentación forma parte de la sintaxis de bloques en Python.", "Indentation is part of Python block syntax.", "Indrykning er en del af Pythons bloksyntaks."),
    ),
    _mcq(
        "dm857.m02.bank.019",
        _t("¿Cuándo es preferible un condicional anidado?", "When is a nested conditional preferable?", "Hvornår er en indlejret betingelse at foretrække?"),
        (
            _option("dependent", "Cuando la segunda decisión solo tiene sentido tras la primera", "When the second decision only makes sense after the first", "Når den anden beslutning kun giver mening efter den første"),
            _option("all", "Siempre que existan dos condiciones", "Whenever two conditions exist", "Hver gang der findes to betingelser"),
            _option("short", "Para evitar escribir and", "To avoid writing and", "For at undgå at skrive and"),
            _option("none", "Nunca", "Never", "Aldrig"),
        ),
        "dependent",
        _t("El anidamiento expresa decisiones dependientes por etapas.", "Nesting expresses staged dependent decisions.", "Indlejring udtrykker afhængige beslutninger i trin."),
    ),
    _mcq(
        "dm857.m02.bank.020",
        _t("¿Qué condición detecta un porcentaje inválido?", "Which condition detects an invalid percentage?", "Hvilken betingelse registrerer en ugyldig procent?"),
        (
            _option("invalid", "percentage < 0 or percentage > 100", "percentage < 0 or percentage > 100", "percentage < 0 or percentage > 100"),
            _option("inside", "0 <= percentage <= 100", "0 <= percentage <= 100", "0 <= percentage <= 100"),
            _option("and", "percentage < 0 and percentage > 100", "percentage < 0 and percentage > 100", "percentage < 0 and percentage > 100"),
            _option("equal", "percentage == 0 or 100", "percentage == 0 or 100", "percentage == 0 or 100"),
        ),
        "invalid",
        _t("Un valor es inválido si cae por debajo de 0 o por encima de 100.", "A value is invalid below 0 or above 100.", "En værdi er ugyldig under 0 eller over 100."),
    ),
    _tf(
        "dm857.m02.bank.021",
        _t("Para probar una clasificación basta con un valor situado en el centro de una categoría.", "One value from the middle of a category is enough to test a classification.", "Én værdi fra midten af en kategori er nok til at teste en klassifikation."),
        correct=False,
        explanation=_t("También deben probarse las demás ramas y los valores límite.", "Other branches and boundary values must also be tested.", "Andre grene og grænseværdier skal også testes."),
    ),
    _mcq(
        "dm857.m02.bank.022",
        _t("Para 10 <= x <= 20, ¿qué conjunto prueba mejor los límites?", "For 10 <= x <= 20, which set best tests the boundaries?", "For 10 <= x <= 20, hvilket sæt tester bedst grænserne?"),
        (
            _option("boundaries", "9, 10, 20, 21", "9, 10, 20, 21", "9, 10, 20, 21"),
            _option("middle", "14, 15, 16, 17", "14, 15, 16, 17", "14, 15, 16, 17"),
            _option("inside", "10, 12, 18, 20", "10, 12, 18, 20", "10, 12, 18, 20"),
            _option("outside", "1, 2, 30, 40", "1, 2, 30, 40", "1, 2, 30, 40"),
        ),
        "boundaries",
        _t("9, 10, 20 y 21 cubren ambos límites y sus lados exteriores inmediatos.", "9, 10, 20, and 21 cover both boundaries and their immediate outer sides.", "9, 10, 20 og 21 dækker begge grænser og deres umiddelbare ydersider."),
    ),
    _mcq(
        "dm857.m02.bank.023",
        _t("¿Qué rama recibe x = 20 en if x < 10; elif x <= 20; else?", "Which branch receives x = 20 in if x < 10; elif x <= 20; else?", "Hvilken gren modtager x = 20 i if x < 10; elif x <= 20; else?"),
        (
            _option("elif", "elif", "elif", "elif"),
            _option("if", "if", "if", "if"),
            _option("else", "else", "else", "else"),
            _option("none", "Ninguna", "None", "Ingen"),
        ),
        "elif",
        _t("20 no es menor que 10, pero sí cumple x <= 20.", "20 is not below 10 but does satisfy x <= 20.", "20 er ikke mindre end 10, men opfylder x <= 20."),
    ),
    _tf(
        "dm857.m02.bank.024",
        _t("Los umbrales de los ejemplos biomédicos del módulo son reglas didácticas, no recomendaciones clínicas.", "The biomedical thresholds in this module are teaching rules, not clinical recommendations.", "De biomedicinske grænser i modulet er undervisningsregler og ikke kliniske anbefalinger."),
        correct=True,
        explanation=_t("Los contextos sirven para practicar programación y no para tomar decisiones reales.", "The contexts are for programming practice, not real decisions.", "Konteksterne bruges til programmeringsøvelse og ikke virkelige beslutninger."),
    ),
)


def materialize_module_02_question_bank(
    locale: AppLocale | str,
) -> tuple[AssessmentItem, ...]:
    """Return the deterministic closed-question bank in one supported locale."""
    resolved = locale if isinstance(locale, AppLocale) else AppLocale.resolve(locale)
    return tuple(item.materialize(resolved) for item in LOCALIZED_OBJECTIVE_QUESTION_BANK_02)


OBJECTIVE_QUESTION_BANK_02 = materialize_module_02_question_bank(AppLocale.SPANISH_SPAIN)

__all__ = [
    "LOCALIZED_OBJECTIVE_QUESTION_BANK_02",
    "OBJECTIVE_QUESTION_BANK_02",
    "materialize_module_02_question_bank",
]
