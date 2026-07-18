"""Trilingual randomized objective bank for DM857 module 3."""

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
        correct_option_ids=("true" if correct else "false",),
        accepted_answers=(),
        explanation=explanation,
    )


LOCALIZED_OBJECTIVE_QUESTION_BANK_03: tuple[LocalizedAssessmentItem, ...] = (
    _mcq(
        "dm857.m03.bank.001",
        _t("¿Cuántos valores produce range(6)?", "How many values does range(6) produce?", "Hvor mange værdier producerer range(6)?"),
        (
            _option("five", "5", "5", "5"),
            _option("six", "6", "6", "6"),
            _option("seven", "7", "7", "7"),
            _option("unknown", "Depende del sistema", "It depends on the system", "Det afhænger af systemet"),
        ),
        "six",
        _t("range(6) produce 0, 1, 2, 3, 4 y 5.", "range(6) produces 0, 1, 2, 3, 4, and 5.", "range(6) producerer 0, 1, 2, 3, 4 og 5."),
    ),
    _tf(
        "dm857.m03.bank.002",
        _t("range(1, 5) incluye el valor 5.", "range(1, 5) includes the value 5.", "range(1, 5) medtager værdien 5."),
        correct=False,
        explanation=_t("El límite stop es exclusivo.", "The stop bound is exclusive.", "Stopgrænsen er eksklusiv."),
    ),
    _mcq(
        "dm857.m03.bank.003",
        _t("¿Qué valores produce range(2, 9, 3)?", "Which values does range(2, 9, 3) produce?", "Hvilke værdier producerer range(2, 9, 3)?"),
        (
            _option("a", "2, 5, 8", "2, 5, 8", "2, 5, 8"),
            _option("b", "2, 5, 8, 11", "2, 5, 8, 11", "2, 5, 8, 11"),
            _option("c", "3, 6, 9", "3, 6, 9", "3, 6, 9"),
            _option("d", "2, 4, 6, 8", "2, 4, 6, 8", "2, 4, 6, 8"),
        ),
        "a",
        _t("Se comienza en 2 y se suma 3 hasta antes de 9.", "Start at 2 and add 3 until before 9.", "Start ved 2 og læg 3 til indtil før 9."),
    ),
    _tf(
        "dm857.m03.bank.004",
        _t("Un while puede ejecutar cero iteraciones.", "A while loop may execute zero iterations.", "En while-løkke kan udføre nul iterationer."),
        correct=True,
        explanation=_t("La condición se evalúa antes del cuerpo.", "The condition is checked before the body.", "Betingelsen kontrolleres før kroppen."),
    ),
    _mcq(
        "dm857.m03.bank.005",
        _t("¿Qué componente suele faltar en un while infinito accidental?", "Which component is commonly missing from an accidental infinite while loop?", "Hvilken komponent mangler ofte i en utilsigtet uendelig while-løkke?"),
        (
            _option("update", "Una actualización que produzca progreso", "An update that creates progress", "En opdatering der skaber fremdrift"),
            _option("comment", "Un comentario", "A comment", "En kommentar"),
            _option("print", "Una llamada a print", "A print call", "Et print-kald"),
            _option("import", "Una importación", "An import", "En import"),
        ),
        "update",
        _t("Si el estado de la condición no cambia, la salida puede no alcanzarse.", "If condition state does not change, exit may never be reached.", "Hvis betingelsens tilstand ikke ændres, nås afslutningen muligvis aldrig."),
    ),
    _tf(
        "dm857.m03.bank.006",
        _t("Terminar siempre demuestra que el resultado de un bucle es correcto.", "Termination always proves that a loop result is correct.", "Afslutning beviser altid, at en løkkes resultat er korrekt."),
        correct=False,
        explanation=_t("Terminación y corrección del resultado son argumentos distintos.", "Termination and result correctness are separate arguments.", "Afslutning og resultatkorrekthed er separate argumenter."),
    ),
    _mcq(
        "dm857.m03.bank.007",
        _t("¿Cuál es el mejor valor inicial para un acumulador de suma?", "What is the best initial value for a summation accumulator?", "Hvad er den bedste startværdi for en sumakkumulator?"),
        (
            _option("zero", "0", "0", "0"),
            _option("one", "1", "1", "1"),
            _option("minus", "-1", "-1", "-1"),
            _option("none", "Siempre None", "Always None", "Altid None"),
        ),
        "zero",
        _t("0 es la identidad de la suma.", "0 is the additive identity.", "0 er additionens neutrale element."),
    ),
    _mcq(
        "dm857.m03.bank.008",
        _t("¿Qué patrón registra cuántas veces ocurre una condición?", "Which pattern records how often a condition occurs?", "Hvilket mønster registrerer, hvor ofte en betingelse forekommer?"),
        (
            _option("counter", "Contador", "Counter", "Tæller"),
            _option("accumulator", "Acumulador", "Accumulator", "Akkumulator"),
            _option("sentinel", "Centinela", "Sentinel", "Stopværdi"),
            _option("invariant", "Invariante", "Invariant", "Invariant"),
        ),
        "counter",
        _t("Un contador aumenta cuando ocurre el evento definido.", "A counter increases when the defined event occurs.", "En tæller øges, når den definerede hændelse forekommer."),
    ),
    _tf(
        "dm857.m03.bank.009",
        _t("Un invariante debe seguir siendo verdadero después de cada iteración.", "An invariant must remain true after every iteration.", "En invariant skal forblive sand efter hver iteration."),
        correct=True,
        explanation=_t("Esa estabilidad permite relacionar estados parciales y resultado final.", "That stability relates partial states to the final result.", "Denne stabilitet knytter deltilstande til slutresultatet."),
    ),
    _mcq(
        "dm857.m03.bank.010",
        _t("¿Qué imprime este código?\ntotal = 0\nfor n in range(1, 4):\n    total += n\nprint(total)", "What does this code print?\ntotal = 0\nfor n in range(1, 4):\n    total += n\nprint(total)", "Hvad udskriver denne kode?\ntotal = 0\nfor n in range(1, 4):\n    total += n\nprint(total)"),
        (
            _option("three", "3", "3", "3"),
            _option("six", "6", "6", "6"),
            _option("ten", "10", "10", "10"),
            _option("error", "Error", "Error", "Fejl"),
        ),
        "six",
        _t("Se suman 1 + 2 + 3.", "The loop adds 1 + 2 + 3.", "Løkken lægger 1 + 2 + 3 sammen."),
    ),
    _tf(
        "dm857.m03.bank.011",
        _t("continue termina el bucle actual.", "continue terminates the current loop.", "continue afslutter den aktuelle løkke."),
        correct=False,
        explanation=_t("continue pasa a la siguiente iteración; break termina el bucle.", "continue moves to the next iteration; break terminates the loop.", "continue går til næste iteration; break afslutter løkken."),
    ),
    _mcq(
        "dm857.m03.bank.012",
        _t("¿Qué efecto tiene break dentro de dos bucles anidados?", "What is the effect of break inside two nested loops?", "Hvilken effekt har break inde i to indlejrede løkker?"),
        (
            _option("inner", "Termina solo el bucle más interno", "It terminates only the innermost loop", "Den afslutter kun den inderste løkke"),
            _option("both", "Termina ambos bucles", "It terminates both loops", "Den afslutter begge løkker"),
            _option("program", "Termina el programa", "It terminates the program", "Den afslutter programmet"),
            _option("none", "No tiene efecto", "It has no effect", "Den har ingen effekt"),
        ),
        "inner",
        _t("break afecta al bucle que lo contiene directamente.", "break affects the loop that directly contains it.", "break påvirker den løkke, der direkte indeholder den."),
    ),
    _tf(
        "dm857.m03.bank.013",
        _t("Un valor centinela debe sumarse antes de comprobar si termina la entrada.", "A sentinel value should be added before checking whether it ends input.", "En stopværdi bør lægges til, før det kontrolleres, om den afslutter input."),
        correct=False,
        explanation=_t("El centinela controla la terminación y no forma parte de los datos.", "The sentinel controls termination and is not part of the data.", "Stopværdien styrer afslutningen og er ikke en del af dataene."),
    ),
    _mcq(
        "dm857.m03.bank.014",
        _t("¿Qué rango imprime 5, 4, 3, 2, 1?", "Which range prints 5, 4, 3, 2, 1?", "Hvilken range udskriver 5, 4, 3, 2, 1?"),
        (
            _option("a", "range(5, 0, -1)", "range(5, 0, -1)", "range(5, 0, -1)"),
            _option("b", "range(5, 1, -1)", "range(5, 1, -1)", "range(5, 1, -1)"),
            _option("c", "range(1, 6)", "range(1, 6)", "range(1, 6)"),
            _option("d", "range(5)", "range(5)", "range(5)"),
        ),
        "a",
        _t("Con step=-1, el stop 0 queda excluido y 1 se incluye.", "With step=-1, stop 0 is excluded and 1 is included.", "Med step=-1 udelukkes stop 0, og 1 medtages."),
    ),
    _mcq(
        "dm857.m03.bank.015",
        _t("Dos bucles realizan 3 y 8 iteraciones. ¿Cuántas veces se ejecuta el cuerpo interior?", "Two nested loops perform 3 and 8 iterations. How many times does the inner body execute?", "To indlejrede løkker udfører 3 og 8 iterationer. Hvor mange gange udføres den indre krop?"),
        (
            _option("eleven", "11", "11", "11"),
            _option("twenty_four", "24", "24", "24"),
            _option("eight", "8", "8", "8"),
            _option("three", "3", "3", "3"),
        ),
        "twenty_four",
        _t("Los recuentos se multiplican: 3 × 8.", "The counts multiply: 3 × 8.", "Antallene multipliceres: 3 × 8."),
    ),
    _tf(
        "dm857.m03.bank.016",
        _t("range(4) produce 0, 1, 2 y 3.", "range(4) produces 0, 1, 2, and 3.", "range(4) producerer 0, 1, 2 og 3."),
        correct=True,
        explanation=_t("range(4) contiene cuatro enteros y excluye 4.", "range(4) contains four integers and excludes 4.", "range(4) indeholder fire heltal og udelukker 4."),
    ),
    _mcq(
        "dm857.m03.bank.017",
        _t("¿Qué caso prueba que un while puede ejecutar cero veces?", "Which case tests that a while loop may execute zero times?", "Hvilket tilfælde tester, at en while-løkke kan udføres nul gange?"),
        (
            _option("false_initial", "Una entrada que haga falsa la condición inicial", "An input that makes the initial condition false", "Et input der gør startbetingelsen falsk"),
            _option("many", "Una entrada con muchas iteraciones", "An input with many iterations", "Et input med mange iterationer"),
            _option("print", "Añadir más print", "Add more print calls", "Tilføj flere print-kald"),
            _option("sleep", "Añadir una pausa", "Add a delay", "Tilføj en pause"),
        ),
        "false_initial",
        _t("Si la condición inicial es falsa, el cuerpo no se ejecuta.", "If the initial condition is false, the body does not execute.", "Hvis startbetingelsen er falsk, udføres kroppen ikke."),
    ),
    _tf(
        "dm857.m03.bank.018",
        _t("Un tiempo máximo de ejecución demuestra que el resultado acumulado es correcto.", "A maximum execution time proves that an accumulated result is correct.", "En maksimal udførelsestid beviser, at et akkumuleret resultat er korrekt."),
        correct=False,
        explanation=_t("El tiempo puede detectar no terminación, pero no valida el resultado.", "Time may detect non-termination but does not validate the result.", "Tid kan opdage manglende afslutning, men validerer ikke resultatet."),
    ),
    _mcq(
        "dm857.m03.bank.019",
        _t("¿Cuál es una medida de progreso para count += 1 mientras count < 10?", "What is a progress measure for count += 1 while count < 10?", "Hvad er et fremdriftsmål for count += 1 mens count < 10?"),
        (
            _option("distance", "10 - count", "10 - count", "10 - count"),
            _option("print", "Número de llamadas a print sin límite", "Number of print calls without a bound", "Antal print-kald uden grænse"),
            _option("name", "La longitud del nombre count", "The length of the name count", "Længden af navnet count"),
            _option("comment", "Número de comentarios", "Number of comments", "Antal kommentarer"),
        ),
        "distance",
        _t("10 - count disminuye hasta 0.", "10 - count decreases towards 0.", "10 - count falder mod 0."),
    ),
    _mcq(
        "dm857.m03.bank.020",
        _t("¿Qué patrón conserva la suma parcial de valores procesados?", "Which pattern stores the partial sum of processed values?", "Hvilket mønster gemmer delsummen af behandlede værdier?"),
        (
            _option("accumulator", "Acumulador", "Accumulator", "Akkumulator"),
            _option("counter", "Contador", "Counter", "Tæller"),
            _option("sentinel", "Centinela", "Sentinel", "Stopværdi"),
            _option("condition", "Condición", "Condition", "Betingelse"),
        ),
        "accumulator",
        _t("El acumulador combina cada valor con un resultado parcial.", "The accumulator combines each value with a partial result.", "Akkumulatoren kombinerer hver værdi med et delresultat."),
    ),
    _tf(
        "dm857.m03.bank.021",
        _t("Un step de range puede ser cero.", "The step of range may be zero.", "Trinnet i range kan være nul."),
        correct=False,
        explanation=_t("Un step cero no produciría progreso y Python lo rechaza.", "A zero step would make no progress and Python rejects it.", "Et trin på nul ville ikke skabe fremdrift, og Python afviser det."),
    ),
    _mcq(
        "dm857.m03.bank.022",
        _t("¿Qué imprime?\ncount = 0\nwhile count < 3:\n    count += 1\nprint(count)", "What is printed?\ncount = 0\nwhile count < 3:\n    count += 1\nprint(count)", "Hvad udskrives?\ncount = 0\nwhile count < 3:\n    count += 1\nprint(count)"),
        (
            _option("zero", "0", "0", "0"),
            _option("two", "2", "2", "2"),
            _option("three", "3", "3", "3"),
            _option("infinite", "No termina", "It does not terminate", "Den afslutter ikke"),
        ),
        "three",
        _t("El bucle termina cuando count alcanza 3.", "The loop stops when count reaches 3.", "Løkken stopper, når count når 3."),
    ),
    _tf(
        "dm857.m03.bank.023",
        _t("for suele ser más claro cuando el número de repeticiones se conoce de antemano.", "for is usually clearer when the repetition count is known in advance.", "for er normalt tydeligere, når antallet af gentagelser kendes på forhånd."),
        correct=True,
        explanation=_t("for expresa directamente un recorrido acotado.", "for directly expresses bounded traversal.", "for udtrykker direkte et afgrænset gennemløb."),
    ),
    _mcq(
        "dm857.m03.bank.024",
        _t("¿Cuál es un buen invariante al contar valores positivos?", "What is a good invariant when counting positive values?", "Hvad er en god invariant ved optælling af positive værdier?"),
        (
            _option("processed", "count es el número de positivos entre los valores ya procesados", "count is the number of positives among values processed so far", "count er antallet af positive blandt de hidtil behandlede værdier"),
            _option("future", "count es el número de positivos aún no vistos", "count is the number of unseen positives", "count er antallet af positive værdier, der endnu ikke er set"),
            _option("always_zero", "count siempre es 0", "count is always 0", "count er altid 0"),
            _option("last", "count es el último valor", "count is the last value", "count er den sidste værdi"),
        ),
        "processed",
        _t("El invariante debe relacionar count con la parte ya recorrida.", "The invariant should relate count to the traversed portion.", "Invarianten bør knytte count til den del, der allerede er gennemløbet."),
    ),
    _tf(
        "dm857.m03.bank.025",
        _t("Añadir break siempre mejora la legibilidad de un bucle.", "Adding break always improves loop readability.", "Tilføjelse af break forbedrer altid en løkkes læsbarhed."),
        correct=False,
        explanation=_t("break es útil en casos claros, pero múltiples salidas pueden ocultar la lógica.", "break is useful in clear cases, but multiple exits may obscure logic.", "break er nyttig i klare tilfælde, men flere udgange kan skjule logikken."),
    ),
    _mcq(
        "dm857.m03.bank.026",
        _t("¿Qué hace continue?", "What does continue do?", "Hvad gør continue?"),
        (
            _option("next", "Omite el resto del cuerpo y pasa a la siguiente iteración", "Skips the rest of the body and moves to the next iteration", "Springer resten af kroppen over og går til næste iteration"),
            _option("exit", "Termina el bucle", "Terminates the loop", "Afslutter løkken"),
            _option("restart", "Reinicia el programa", "Restarts the program", "Genstarter programmet"),
            _option("return", "Devuelve un valor", "Returns a value", "Returnerer en værdi"),
        ),
        "next",
        _t("continue conserva el bucle y comienza la siguiente iteración.", "continue preserves the loop and starts the next iteration.", "continue bevarer løkken og starter næste iteration."),
    ),
    _mcq(
        "dm857.m03.bank.027",
        _t("¿Qué resultado produce sumando 2 en cinco iteraciones desde total = 0?", "What result is produced by adding 2 in five iterations from total = 0?", "Hvilket resultat fås ved at lægge 2 til i fem iterationer fra total = 0?"),
        (
            _option("two", "2", "2", "2"),
            _option("five", "5", "5", "5"),
            _option("ten", "10", "10", "10"),
            _option("twelve", "12", "12", "12"),
        ),
        "ten",
        _t("Cinco actualizaciones de +2 producen 10.", "Five +2 updates produce 10.", "Fem opdateringer på +2 giver 10."),
    ),
    _tf(
        "dm857.m03.bank.028",
        _t("En dos bucles anidados con 2 y 4 iteraciones, el cuerpo interior se ejecuta 6 veces.", "With nested loops of 2 and 4 iterations, the inner body executes 6 times.", "Med indlejrede løkker på 2 og 4 iterationer udføres den indre krop 6 gange."),
        correct=False,
        explanation=_t("Se ejecuta 2 × 4 = 8 veces.", "It executes 2 × 4 = 8 times.", "Den udføres 2 × 4 = 8 gange."),
    ),
    _mcq(
        "dm857.m03.bank.029",
        _t("¿Qué prueba revela mejor un error entre < y <= en un while?", "Which test best exposes a < versus <= mistake in a while loop?", "Hvilken test afslører bedst en fejl mellem < og <= i en while-løkke?"),
        (
            _option("boundary", "El valor exacto del límite", "The exact boundary value", "Den præcise grænseværdi"),
            _option("middle", "Solo un valor central", "Only a middle value", "Kun en midterværdi"),
            _option("comment", "Un comentario más largo", "A longer comment", "En længere kommentar"),
            _option("rename", "Cambiar el nombre de la variable", "Renaming the variable", "At omdøbe variablen"),
        ),
        "boundary",
        _t("El valor exacto activa la diferencia entre inclusión y exclusión.", "The exact boundary activates the inclusion-versus-exclusion difference.", "Den præcise grænse aktiverer forskellen mellem inklusion og eksklusion."),
    ),
    _tf(
        "dm857.m03.bank.030",
        _t("Los ejemplos biomédicos del módulo representan recomendaciones clínicas reales.", "The biomedical examples in the module represent real clinical recommendations.", "De biomedicinske eksempler i modulet repræsenterer virkelige kliniske anbefalinger."),
        correct=False,
        explanation=_t("Son escenarios didácticos para aprender programación.", "They are teaching scenarios for learning programming.", "De er undervisningsscenarier til at lære programmering."),
    ),
)


def materialize_module_03_question_bank(
    locale: AppLocale | str,
) -> tuple[AssessmentItem, ...]:
    """Materialize the complete randomized bank in one supported locale."""
    resolved = locale if isinstance(locale, AppLocale) else AppLocale.resolve(locale)
    return tuple(item.materialize(resolved) for item in LOCALIZED_OBJECTIVE_QUESTION_BANK_03)


OBJECTIVE_QUESTION_BANK_03 = materialize_module_03_question_bank(AppLocale.SPANISH_SPAIN)

__all__ = [
    "LOCALIZED_OBJECTIVE_QUESTION_BANK_03",
    "OBJECTIVE_QUESTION_BANK_03",
    "materialize_module_03_question_bank",
]
