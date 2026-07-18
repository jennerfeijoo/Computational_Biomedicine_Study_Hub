"""DM857 module 3: controlled iteration with while and for."""

from __future__ import annotations

from ...i18n import AppLocale
from ...learning.activity_types import ActivityType
from ..localized_models import (
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


def _t(spanish: str, english: str, danish: str) -> LocalizedText:
    return LocalizedText(spanish=spanish, english=english, danish=danish)


def _same(text: str) -> LocalizedText:
    return _t(text, text, text)


def _option(
    option_id: str,
    spanish: str,
    english: str,
    danish: str,
) -> LocalizedAssessmentOption:
    return LocalizedAssessmentOption(option_id=option_id, text=_t(spanish, english, danish))


LOCALIZED_MODULE_03_ITERATION = LocalizedLearningModule(
    course_code="DM857",
    module_id="dm857.m03",
    title=_t(
        "Iteración controlada con while y for",
        "Controlled iteration with while and for",
        "Kontrolleret iteration med while og for",
    ),
    summary=_t(
        "Este módulo desarrolla la capacidad de repetir operaciones de forma finita, verificable y "
        "legible. Se estudian los bucles while y for, range, contadores, acumuladores, recorridos, "
        "condiciones de terminación, invariantes introductorios, valores centinela, break, continue, "
        "bucles anidados y pruebas capaces de detectar errores de límites o bucles infinitos.",
        "This module develops the ability to repeat operations in a finite, verifiable, and readable "
        "way. It covers while and for loops, range, counters, accumulators, traversal, termination "
        "conditions, introductory invariants, sentinel values, break, continue, nested loops, and "
        "tests that expose boundary mistakes or infinite loops.",
        "Dette modul udvikler evnen til at gentage operationer på en endelig, efterprøvelig og læsbar "
        "måde. Det dækker while- og for-løkker, range, tællere, akkumulatorer, gennemløb, "
        "afslutningsbetingelser, indledende invarianter, stopværdier, break, continue, indlejrede "
        "løkker og test, der afslører grænsefejl eller uendelige løkker.",
    ),
    objectives=(
        LocalizedLearningObjective(
            "m03.o1",
            _t(
                "Explicar la iteración como una secuencia de transiciones de estado gobernada por una regla de continuación.",
                "Explain iteration as a sequence of state transitions governed by a continuation rule.",
                "Forklare iteration som en række tilstandsovergange styret af en fortsættelsesregel.",
            ),
        ),
        LocalizedLearningObjective(
            "m03.o2",
            _t(
                "Diseñar bucles while con inicialización, condición, actualización y terminación demostrables.",
                "Design while loops with demonstrable initialization, condition, update, and termination.",
                "Designe while-løkker med påviselig initialisering, betingelse, opdatering og afslutning.",
            ),
        ),
        LocalizedLearningObjective(
            "m03.o3",
            _t(
                "Utilizar for y range para expresar repeticiones acotadas sin errores de uno en uno.",
                "Use for and range to express bounded repetition without off-by-one errors.",
                "Bruge for og range til at udtrykke afgrænset gentagelse uden én-for-meget- eller én-for-lidt-fejl.",
            ),
        ),
        LocalizedLearningObjective(
            "m03.o4",
            _t(
                "Distinguir y aplicar contadores, acumuladores, indicadores y variables de mejor valor.",
                "Distinguish and apply counters, accumulators, flags, and best-value variables.",
                "Skelne mellem og anvende tællere, akkumulatorer, flag og variable for bedste værdi.",
            ),
        ),
        LocalizedLearningObjective(
            "m03.o5",
            _t(
                "Trazar manualmente un bucle registrando condición, estado, salida y número de iteración.",
                "Trace a loop manually by recording its condition, state, output, and iteration number.",
                "Gennemgå en løkke manuelt ved at registrere betingelse, tilstand, output og iterationsnummer.",
            ),
        ),
        LocalizedLearningObjective(
            "m03.o6",
            _t(
                "Justificar el uso de break, continue y valores centinela sin ocultar la lógica de terminación.",
                "Justify break, continue, and sentinel values without hiding termination logic.",
                "Begrunde brugen af break, continue og stopværdier uden at skjule afslutningslogikken.",
            ),
        ),
        LocalizedLearningObjective(
            "m03.o7",
            _t(
                "Analizar bucles anidados y relacionar sus límites con el número total de operaciones.",
                "Analyse nested loops and relate their bounds to the total number of operations.",
                "Analysere indlejrede løkker og knytte deres grænser til det samlede antal operationer.",
            ),
        ),
        LocalizedLearningObjective(
            "m03.o8",
            _t(
                "Diseñar pruebas normales, límite y adversas para verificar cobertura, terminación y resultados acumulados.",
                "Design normal, boundary, and adversarial tests for coverage, termination, and accumulated results.",
                "Designe normale, grænse- og udfordrende test, der verificerer dækning, afslutning og akkumulerede resultater.",
            ),
        ),
    ),
    concepts=(
        LocalizedConceptBlock(
            concept_id="iteration-as-state-transition",
            title=_t(
                "La iteración como transición de estado",
                "Iteration as state transition",
                "Iteration som tilstandsovergang",
            ),
            body=_t(
                "Un bucle no significa simplemente repetir líneas. En cada iteración, el programa observa un estado, "
                "evalúa una regla, ejecuta un cuerpo y produce un estado nuevo. Para razonar con precisión conviene "
                "identificar qué variables forman el estado, qué propiedad permite continuar y qué actualización "
                "acerca el programa a la terminación. Un bucle correcto conserva las propiedades necesarias del "
                "problema y finaliza con un estado que satisface el objetivo.",
                "A loop is not merely repeated lines. During each iteration, the program observes a state, evaluates "
                "a rule, executes a body, and produces a new state. Precise reasoning identifies the state variables, "
                "the property that permits continuation, and the update that moves the program towards termination. "
                "A correct loop preserves the required problem properties and finishes in a state that satisfies the goal.",
                "En løkke er ikke blot gentagne linjer. I hver iteration observerer programmet en tilstand, evaluerer "
                "en regel, udfører en krop og skaber en ny tilstand. Præcis ræsonnering identificerer tilstandsvariablene, "
                "egenskaben der tillader fortsættelse, og opdateringen der fører programmet mod afslutning. En korrekt "
                "løkke bevarer problemets nødvendige egenskaber og slutter i en tilstand, der opfylder målet.",
            ),
            key_points=(
                _t("El estado cambia entre iteraciones.", "State changes between iterations.", "Tilstanden ændres mellem iterationer."),
                _t("La condición decide si se ejecuta otra iteración.", "The condition decides whether another iteration executes.", "Betingelsen afgør, om endnu en iteration udføres."),
                _t("La actualización debe contribuir al progreso.", "The update must contribute to progress.", "Opdateringen skal bidrage til fremdrift."),
                _t("El resultado final depende tanto del cuerpo como de la terminación.", "The final result depends on both the body and termination.", "Det endelige resultat afhænger både af kroppen og afslutningen."),
            ),
        ),
        LocalizedConceptBlock(
            concept_id="while-loop-anatomy",
            title=_t(
                "Anatomía de un bucle while",
                "Anatomy of a while loop",
                "Anatomi af en while-løkke",
            ),
            body=_t(
                "while repite su cuerpo mientras una condición sea verdadera. Antes del bucle se inicializan las "
                "variables necesarias; al comienzo de cada iteración se evalúa la condición; dentro del cuerpo se "
                "realiza el trabajo y se actualiza el estado. Si la condición ya es falsa al inicio, el cuerpo puede "
                "ejecutarse cero veces. Esta posibilidad debe formar parte del diseño y de las pruebas.",
                "while repeats its body while a condition is true. Required variables are initialized before the loop; "
                "the condition is evaluated at the start of each iteration; the body performs work and updates state. "
                "If the condition is initially false, the body may execute zero times. That possibility belongs in the design and tests.",
                "while gentager sin krop, mens en betingelse er sand. Nødvendige variable initialiseres før løkken; "
                "betingelsen evalueres i begyndelsen af hver iteration; kroppen udfører arbejdet og opdaterer tilstanden. "
                "Hvis betingelsen er falsk fra starten, kan kroppen udføres nul gange. Denne mulighed skal indgå i design og test.",
            ),
            key_points=(
                _t("while comprueba la condición antes del cuerpo.", "while checks the condition before the body.", "while kontrollerer betingelsen før kroppen."),
                _t("La inicialización debe establecer un estado válido.", "Initialization must establish a valid state.", "Initialiseringen skal etablere en gyldig tilstand."),
                _t("La actualización suele modificar una variable presente en la condición.", "The update usually changes a variable used by the condition.", "Opdateringen ændrer normalt en variabel, der indgår i betingelsen."),
                _t("Cero iteraciones puede ser el comportamiento correcto.", "Zero iterations may be correct behaviour.", "Nul iterationer kan være korrekt adfærd."),
            ),
        ),
        LocalizedConceptBlock(
            concept_id="termination-progress-and-invariants",
            title=_t(
                "Terminación, progreso e invariantes",
                "Termination, progress, and invariants",
                "Afslutning, fremdrift og invarianter",
            ),
            body=_t(
                "Para argumentar que un bucle termina se identifica una medida de progreso que cambia en una dirección "
                "predecible y está acotada, como un contador que aumenta hasta un límite. Un invariante es una propiedad "
                "que debe ser verdadera antes y después de cada iteración; por ejemplo, que total contiene la suma de "
                "los valores ya procesados. Los invariantes ayudan a detectar actualizaciones fuera de orden y permiten "
                "explicar por qué el resultado final es correcto, no solo por qué el bucle se detiene.",
                "To argue that a loop terminates, identify a bounded progress measure that changes predictably, such as "
                "a counter increasing towards a limit. An invariant is a property that must hold before and after every "
                "iteration; for example, total contains the sum of the values processed so far. Invariants expose "
                "updates in the wrong order and explain why the final result is correct, not merely why the loop stops.",
                "For at argumentere for at en løkke afslutter, identificeres et afgrænset fremdriftsmål, der ændres "
                "forudsigeligt, eksempelvis en tæller der stiger mod en grænse. En invariant er en egenskab, der skal "
                "gælde før og efter hver iteration; eksempelvis at total indeholder summen af de hidtil behandlede værdier. "
                "Invarianter afslører opdateringer i forkert rækkefølge og forklarer, hvorfor slutresultatet er korrekt.",
            ),
            key_points=(
                _t("Una medida de progreso debe acercarse a un límite.", "A progress measure must move towards a bound.", "Et fremdriftsmål skal bevæge sig mod en grænse."),
                _t("Un invariante describe lo que sigue siendo cierto.", "An invariant describes what remains true.", "En invariant beskriver det, der forbliver sandt."),
                _t("Olvidar la actualización puede producir un bucle infinito.", "Omitting the update can produce an infinite loop.", "En manglende opdatering kan skabe en uendelig løkke."),
                _t("Terminar no basta: el estado final también debe ser correcto.", "Termination is not enough: the final state must also be correct.", "Afslutning er ikke nok: sluttilstanden skal også være korrekt."),
            ),
        ),
        LocalizedConceptBlock(
            concept_id="for-loop-and-range",
            title=_t(
                "Bucles for y semántica de range",
                "for loops and range semantics",
                "for-løkker og range-semantik",
            ),
            body=_t(
                "for expresa una repetición sobre una secuencia de valores. range(stop) produce enteros desde 0 hasta "
                "stop sin incluirlo; range(start, stop) comienza en start; range(start, stop, step) utiliza el incremento "
                "indicado. El límite superior exclusivo permite que range(n) produzca exactamente n valores. Cuando el "
                "número de repeticiones está determinado por adelantado, for suele ser más claro y menos propenso a "
                "errores que un while con contador manual.",
                "for expresses repetition over a sequence of values. range(stop) produces integers from 0 up to but not "
                "including stop; range(start, stop) begins at start; range(start, stop, step) uses the specified increment. "
                "The exclusive upper bound means range(n) produces exactly n values. When the repetition count is known "
                "in advance, for is usually clearer and less error-prone than a while loop with a manual counter.",
                "for udtrykker gentagelse over en sekvens af værdier. range(stop) producerer heltal fra 0 til, men ikke "
                "med, stop; range(start, stop) begynder ved start; range(start, stop, step) bruger det angivne trin. Den "
                "eksklusive øvre grænse betyder, at range(n) producerer præcis n værdier. Når antallet af gentagelser er "
                "kendt på forhånd, er for normalt tydeligere og mindre fejludsat end en while-løkke med manuel tæller.",
            ),
            key_points=(
                _t("El valor stop de range no se incluye.", "The stop value of range is excluded.", "Stopværdien i range medtages ikke."),
                _t("range(n) genera n valores: 0 hasta n - 1.", "range(n) generates n values: 0 through n - 1.", "range(n) genererer n værdier: 0 til n - 1."),
                _t("step no puede ser cero.", "step cannot be zero.", "step kan ikke være nul."),
                _t("for comunica que el recorrido está acotado por un iterable.", "for communicates that traversal is bounded by an iterable.", "for kommunikerer, at gennemløbet er afgrænset af et iterabelt objekt."),
            ),
        ),
        LocalizedConceptBlock(
            concept_id="counters-accumulators-and-best-values",
            title=_t(
                "Contadores, acumuladores y mejores valores",
                "Counters, accumulators, and best values",
                "Tællere, akkumulatorer og bedste værdier",
            ),
            body=_t(
                "Un contador registra cuántas veces ocurre una condición y suele comenzar en 0. Un acumulador combina "
                "valores, por ejemplo sumándolos, y necesita una identidad compatible como 0 para la suma o 1 para el "
                "producto. Para localizar un máximo o mínimo se mantiene una variable con el mejor valor observado y se "
                "actualiza solo cuando aparece uno mejor. La inicialización debe representar un estado válido; utilizar "
                "un número arbitrario puede producir errores cuando los datos reales quedan fuera de ese supuesto.",
                "A counter records how often a condition occurs and usually starts at 0. An accumulator combines values, "
                "for example by addition, and needs a compatible identity such as 0 for a sum or 1 for a product. To find "
                "a maximum or minimum, keep the best value observed and update it only when a better one appears. "
                "Initialization must represent a valid state; an arbitrary number can fail when real data violate that assumption.",
                "En tæller registrerer, hvor ofte en betingelse optræder, og begynder normalt ved 0. En akkumulator "
                "kombinerer værdier, eksempelvis ved addition, og kræver et passende neutralt element som 0 for en sum "
                "eller 1 for et produkt. For at finde et maksimum eller minimum bevares den bedste observerede værdi, "
                "som kun opdateres, når en bedre værdi findes. Initialiseringen skal repræsentere en gyldig tilstand.",
            ),
            key_points=(
                _t("Un contador responde cuántos.", "A counter answers how many.", "En tæller svarer på hvor mange."),
                _t("Un acumulador conserva un resultado parcial.", "An accumulator stores a partial result.", "En akkumulator gemmer et delresultat."),
                _t("La identidad inicial depende de la operación.", "The initial identity depends on the operation.", "Startidentiteten afhænger af operationen."),
                _t("Máximos y mínimos requieren una inicialización válida.", "Maximum and minimum tracking requires valid initialization.", "Sporing af maksimum og minimum kræver gyldig initialisering."),
            ),
        ),
        LocalizedConceptBlock(
            concept_id="sentinels-break-and-continue",
            title=_t(
                "Valores centinela, break y continue",
                "Sentinels, break, and continue",
                "Stopværdier, break og continue",
            ),
            body=_t(
                "Un valor centinela indica que una secuencia de entradas ha terminado y no forma parte de los datos que "
                "deben procesarse. break termina inmediatamente el bucle actual; continue omite el resto del cuerpo y "
                "pasa a la siguiente iteración. Estas herramientas pueden simplificar una condición excepcional, pero "
                "deben utilizarse con moderación. Si aparecen en muchos puntos, la lógica de terminación y las propiedades "
                "del bucle se vuelven difíciles de verificar.",
                "A sentinel value signals that an input sequence has ended and is not part of the data to process. break "
                "terminates the current loop immediately; continue skips the rest of the body and moves to the next "
                "iteration. These tools can simplify an exceptional condition, but should be used sparingly. Multiple "
                "exit or skip points make termination logic and loop properties harder to verify.",
                "En stopværdi signalerer, at en inputsekvens er afsluttet, og er ikke en del af de data, der skal behandles. "
                "break afslutter den aktuelle løkke straks; continue springer resten af kroppen over og går til næste "
                "iteration. Værktøjerne kan forenkle en undtagelsestilstand, men bør bruges sparsomt. Mange afslutnings- "
                "eller overspringspunkter gør løkkens logik vanskeligere at verificere.",
            ),
            key_points=(
                _t("El centinela controla el final y no se acumula como dato.", "The sentinel controls termination and is not accumulated as data.", "Stopværdien styrer afslutningen og akkumuleres ikke som data."),
                _t("break finaliza el bucle más interno.", "break terminates the innermost loop.", "break afslutter den inderste løkke."),
                _t("continue no finaliza el bucle; salta a la siguiente iteración.", "continue does not terminate the loop; it skips to the next iteration.", "continue afslutter ikke løkken; den går videre til næste iteration."),
                _t("La estructura más simple que expresa correctamente el algoritmo suele ser preferible.", "The simplest structure that correctly expresses the algorithm is usually preferable.", "Den enkleste struktur, der korrekt udtrykker algoritmen, er normalt at foretrække."),
            ),
        ),
        LocalizedConceptBlock(
            concept_id="nested-loops-and-operation-count",
            title=_t(
                "Bucles anidados y número de operaciones",
                "Nested loops and operation count",
                "Indlejrede løkker og antal operationer",
            ),
            body=_t(
                "En iteración completa del bucle exterior ejecuta todo el bucle interior. Si el exterior realiza r "
                "iteraciones y el interior c en cada una, el cuerpo interior se ejecuta r × c veces. Esta multiplicación "
                "explica por qué pequeños cambios en ambos límites pueden aumentar mucho el trabajo. En un bucle anidado, "
                "break afecta solo al bucle más interno; abandonar varios niveles requiere rediseñar el control o utilizar "
                "una condición compartida explícita.",
                "One complete outer-loop iteration executes the entire inner loop. If the outer loop performs r iterations "
                "and the inner loop performs c each time, the inner body executes r × c times. This multiplication explains "
                "why small increases in both bounds can greatly increase work. In nested loops, break affects only the "
                "innermost loop; leaving several levels requires redesigned control or an explicit shared condition.",
                "En fuld iteration af den ydre løkke udfører hele den indre løkke. Hvis den ydre løkke udfører r iterationer "
                "og den indre c hver gang, udføres den indre krop r × c gange. Denne multiplikation forklarer, hvorfor små "
                "stigninger i begge grænser kan øge arbejdet betydeligt. I indlejrede løkker påvirker break kun den inderste løkke.",
            ),
            key_points=(
                _t("Los recuentos de bucles anidados suelen multiplicarse.", "Nested-loop counts usually multiply.", "Antallet af iterationer i indlejrede løkker multipliceres normalt."),
                _t("Cada variable de control debe tener un significado independiente.", "Each control variable needs an independent meaning.", "Hver kontrolvariabel skal have en selvstændig betydning."),
                _t("break solo abandona el bucle más interno.", "break exits only the innermost loop.", "break forlader kun den inderste løkke."),
                _t("El coste debe relacionarse con los límites del problema.", "Cost should be related to the problem bounds.", "Omkostningen bør knyttes til problemets grænser."),
            ),
        ),
        LocalizedConceptBlock(
            concept_id="loop-tracing-and-testing",
            title=_t(
                "Trazado y pruebas de bucles",
                "Loop tracing and testing",
                "Gennemgang og test af løkker",
            ),
            body=_t(
                "Una tabla de trazado de bucles registra al menos el número de iteración, el resultado de la condición, "
                "las variables modificadas y la salida producida. Las pruebas deben incluir cero iteraciones, una iteración, "
                "varias iteraciones, el límite exacto y una entrada que pueda revelar falta de progreso. Para acumuladores "
                "también se verifica el valor inicial y el resultado parcial después de cada paso. Un tiempo máximo de "
                "ejecución puede detectar un bucle infinito, pero no sustituye el razonamiento sobre la terminación.",
                "A loop trace table records at least the iteration number, condition result, modified variables, and produced "
                "output. Tests should cover zero iterations, one iteration, several iterations, the exact boundary, and an "
                "input that may expose missing progress. For accumulators, verify the initial value and each partial result. "
                "A time limit may detect an infinite loop, but does not replace a termination argument.",
                "En gennemgangstabel for løkker registrerer mindst iterationsnummer, betingelsens resultat, ændrede variable "
                "og produceret output. Test bør dække nul iterationer, én iteration, flere iterationer, den præcise grænse "
                "og et input, der kan afsløre manglende fremdrift. For akkumulatorer kontrolleres startværdien og hvert "
                "delresultat. En tidsgrænse kan opdage en uendelig løkke, men erstatter ikke et afslutningsargument.",
            ),
            key_points=(
                _t("El trazado sigue el orden real de evaluación.", "Tracing follows the actual evaluation order.", "Gennemgang følger den faktiske evalueringsrækkefølge."),
                _t("Cero, una y varias iteraciones son casos distintos.", "Zero, one, and many iterations are distinct cases.", "Nul, én og mange iterationer er forskellige tilfælde."),
                _t("Los límites revelan errores de uno en uno.", "Boundary cases expose off-by-one errors.", "Grænsetilfælde afslører én-for-meget- eller én-for-lidt-fejl."),
                _t("Una prueba de tiempo no demuestra corrección.", "A time limit does not prove correctness.", "En tidsgrænse beviser ikke korrekthed."),
            ),
        ),
    ),
    worked_examples=(
        LocalizedWorkedExample(
            example_id="m03.e01",
            title=_t(
                "Repetir una medición simulada hasta alcanzar estabilidad",
                "Repeat a simulated measurement until stability",
                "Gentag en simuleret måling indtil stabilitet",
            ),
            problem=_t(
                "Una simulación comienza con una señal de 0.42 y aumenta 0.11 por intento. Detén el proceso cuando la señal alcance 0.75 o después de cuatro intentos. Informa intentos y señal final. Los valores son didácticos.",
                "A simulation starts with a signal of 0.42 and increases by 0.11 per attempt. Stop when the signal reaches 0.75 or after four attempts. Report attempts and final signal. Values are for teaching only.",
                "En simulering starter med et signal på 0.42 og øges med 0.11 pr. forsøg. Stop når signalet når 0.75 eller efter fire forsøg. Vis antal forsøg og slutsignal. Værdierne er kun til undervisning.",
            ),
            reasoning=(
                _t("El estado está formado por signal y attempts.", "The state consists of signal and attempts.", "Tilstanden består af signal og attempts."),
                _t("El bucle continúa solo mientras falten ambos criterios de parada.", "The loop continues only while both stopping criteria remain unmet.", "Løkken fortsætter kun, mens begge stopkriterier endnu ikke er opfyldt."),
                _t("Cada iteración aumenta attempts y modifica signal.", "Each iteration increments attempts and modifies signal.", "Hver iteration øger attempts og ændrer signal."),
                _t("attempts está acotado por 4, por lo que la terminación es demostrable.", "attempts is bounded by 4, so termination is demonstrable.", "attempts er afgrænset af 4, så afslutningen kan påvises."),
            ),
            code=_same(
                "signal = 0.42\nattempts = 0\n\nwhile signal < 0.75 and attempts < 4:\n    attempts += 1\n    signal += 0.11\n\nprint(attempts)\nprint(round(signal, 2))"
            ),
            expected_output=_same("3\n0.75"),
            explanation=_t(
                "La condición se comprueba antes de cada intento. Después del tercer incremento, signal es aproximadamente 0.75 y la siguiente evaluación impide otra iteración.",
                "The condition is checked before each attempt. After the third increment, signal is approximately 0.75 and the next evaluation prevents another iteration.",
                "Betingelsen kontrolleres før hvert forsøg. Efter den tredje stigning er signal omtrent 0.75, og næste evaluering forhindrer endnu en iteration.",
            ),
        ),
        LocalizedWorkedExample(
            example_id="m03.e02",
            title=_t(
                "Calcular volumen acumulado para réplicas",
                "Calculate cumulative volume for replicates",
                "Beregn akkumuleret volumen for replikater",
            ),
            problem=_t(
                "Se preparan seis réplicas y cada una requiere 18 microlitros. Utiliza for y range para calcular el volumen total y mostrar el subtotal después de cada réplica.",
                "Six replicates are prepared and each requires 18 microlitres. Use for and range to calculate total volume and display the subtotal after each replicate.",
                "Der forberedes seks replikater, og hver kræver 18 mikroliter. Brug for og range til at beregne totalvolumen og vise subtotalen efter hvert replikat.",
            ),
            reasoning=(
                _t("El número de repeticiones se conoce de antemano, por lo que for es apropiado.", "The repetition count is known in advance, so for is appropriate.", "Antallet af gentagelser kendes på forhånd, så for er passende."),
                _t("range(1, 7) produce los identificadores 1 a 6.", "range(1, 7) produces identifiers 1 through 6.", "range(1, 7) producerer identifikatorerne 1 til 6."),
                _t("total_ul comienza en 0 porque acumula una suma.", "total_ul starts at 0 because it accumulates a sum.", "total_ul begynder ved 0, fordi variablen akkumulerer en sum."),
                _t("Después de cada iteración, total_ul representa el volumen de las réplicas ya procesadas.", "After each iteration, total_ul represents the volume of the replicates processed so far.", "Efter hver iteration repræsenterer total_ul volumenet for de hidtil behandlede replikater."),
            ),
            code=_same(
                "volume_per_replicate_ul = 18\ntotal_ul = 0\n\nfor replicate in range(1, 7):\n    total_ul += volume_per_replicate_ul\n    print(replicate, total_ul)"
            ),
            expected_output=_same("1 18\n2 36\n3 54\n4 72\n5 90\n6 108"),
            explanation=_t(
                "El invariante es que total_ul contiene 18 multiplicado por el número de réplicas completadas. El límite superior 7 no se incluye.",
                "The invariant is that total_ul contains 18 times the number of completed replicates. The upper bound 7 is excluded.",
                "Invarianten er, at total_ul indeholder 18 gange antallet af færdige replikater. Den øvre grænse 7 medtages ikke.",
            ),
        ),
        LocalizedWorkedExample(
            example_id="m03.e03",
            title=_t(
                "Contar ciclos que cumplen un criterio didáctico",
                "Count cycles that satisfy a teaching criterion",
                "Tæl cyklusser der opfylder et undervisningskriterium",
            ),
            problem=_t(
                "En señal simulada aumenta 0.08 por ciclo durante ocho ciclos. Cuenta cuántos valores son al menos 0.40 y calcula la suma de esos valores. El umbral es exclusivamente didáctico.",
                "A simulated signal increases by 0.08 per cycle for eight cycles. Count how many values are at least 0.40 and calculate their sum. The threshold is exclusively for teaching.",
                "Et simuleret signal stiger med 0.08 pr. cyklus i otte cyklusser. Tæl hvor mange værdier der er mindst 0.40, og beregn deres sum. Grænsen er kun til undervisning.",
            ),
            reasoning=(
                _t("range(1, 9) genera ocho números de ciclo.", "range(1, 9) generates eight cycle numbers.", "range(1, 9) genererer otte cyklusnumre."),
                _t("passing_count es un contador y passing_sum un acumulador.", "passing_count is a counter and passing_sum an accumulator.", "passing_count er en tæller, og passing_sum er en akkumulator."),
                _t("Ambos se actualizan únicamente cuando la condición es verdadera.", "Both update only when the condition is true.", "Begge opdateres kun, når betingelsen er sand."),
                _t("round se utiliza solo para presentar la suma con claridad.", "round is used only to present the sum clearly.", "round bruges kun til at præsentere summen tydeligt."),
            ),
            code=_same(
                "passing_count = 0\npassing_sum = 0.0\n\nfor cycle in range(1, 9):\n    signal = cycle * 0.08\n    if signal >= 0.40:\n        passing_count += 1\n        passing_sum += signal\n\nprint(passing_count)\nprint(round(passing_sum, 2))"
            ),
            expected_output=_same("4\n2.08"),
            explanation=_t(
                "Los ciclos 5, 6, 7 y 8 producen 0.40, 0.48, 0.56 y 0.64. El límite 0.40 se incluye porque se usa >=.",
                "Cycles 5, 6, 7, and 8 produce 0.40, 0.48, 0.56, and 0.64. The 0.40 boundary is included because >= is used.",
                "Cyklus 5, 6, 7 og 8 giver 0.40, 0.48, 0.56 og 0.64. Grænsen 0.40 medtages, fordi >= anvendes.",
            ),
        ),
        LocalizedWorkedExample(
            example_id="m03.e04",
            title=_t(
                "Detener la búsqueda en la primera coincidencia",
                "Stop a search at the first match",
                "Stop en søgning ved første match",
            ),
            problem=_t(
                "Una señal simulada sigue signal = 0.12 × cycle. Encuentra el primer ciclo entre 1 y 10 en el que signal sea mayor o igual que 0.60 y detén la búsqueda.",
                "A simulated signal follows signal = 0.12 × cycle. Find the first cycle from 1 to 10 where signal is at least 0.60 and stop searching.",
                "Et simuleret signal følger signal = 0.12 × cycle. Find den første cyklus fra 1 til 10, hvor signal er mindst 0.60, og stop søgningen.",
            ),
            reasoning=(
                _t("El objetivo es la primera coincidencia, no todas las coincidencias.", "The goal is the first match, not all matches.", "Målet er den første match, ikke alle matches."),
                _t("for limita la búsqueda a diez ciclos.", "for bounds the search to ten cycles.", "for afgrænser søgningen til ti cyklusser."),
                _t("Cuando la condición es verdadera se registra el ciclo y break evita trabajo posterior.", "When the condition is true, the cycle is recorded and break avoids later work.", "Når betingelsen er sand, registreres cyklussen, og break undgår senere arbejde."),
                _t("found_cycle se inicializa con None para representar que aún no existe coincidencia.", "found_cycle starts as None to represent that no match exists yet.", "found_cycle initialiseres med None for at repræsentere, at der endnu ikke findes et match."),
            ),
            code=_same(
                "found_cycle = None\n\nfor cycle in range(1, 11):\n    signal = cycle * 0.12\n    if signal >= 0.60:\n        found_cycle = cycle\n        break\n\nprint(found_cycle)"
            ),
            expected_output=_same("5"),
            explanation=_t(
                "En el ciclo 5, signal es 0.60. break termina el for inmediatamente; no se calculan los ciclos 6 a 10.",
                "At cycle 5, signal is 0.60. break terminates the for loop immediately; cycles 6 through 10 are not calculated.",
                "Ved cyklus 5 er signal 0.60. break afslutter for-løkken straks; cyklus 6 til 10 beregnes ikke.",
            ),
        ),
        LocalizedWorkedExample(
            example_id="m03.e05",
            title=_t(
                "Recorrer una cuadrícula de posiciones",
                "Traverse a grid of positions",
                "Gennemløb et gitter af positioner",
            ),
            problem=_t(
                "Genera las coordenadas de una cuadrícula didáctica con 3 filas y 4 columnas. Cuenta cuántas posiciones se visitan.",
                "Generate the coordinates of a teaching grid with 3 rows and 4 columns. Count how many positions are visited.",
                "Generér koordinaterne for et undervisningsgitter med 3 rækker og 4 kolonner. Tæl hvor mange positioner der besøges.",
            ),
            reasoning=(
                _t("El bucle exterior representa las filas.", "The outer loop represents rows.", "Den ydre løkke repræsenterer rækker."),
                _t("Para cada fila, el bucle interior recorre cuatro columnas.", "For each row, the inner loop traverses four columns.", "For hver række gennemløber den indre løkke fire kolonner."),
                _t("visited aumenta una vez por combinación fila-columna.", "visited increases once per row-column combination.", "visited øges én gang pr. række-kolonne-kombination."),
                _t("El cuerpo interior se ejecuta 3 × 4 = 12 veces.", "The inner body executes 3 × 4 = 12 times.", "Den indre krop udføres 3 × 4 = 12 gange."),
            ),
            code=_same(
                "visited = 0\n\nfor row in range(1, 4):\n    for column in range(1, 5):\n        print(row, column)\n        visited += 1\n\nprint('total', visited)"
            ),
            expected_output=_same(
                "1 1\n1 2\n1 3\n1 4\n2 1\n2 2\n2 3\n2 4\n3 1\n3 2\n3 3\n3 4\ntotal 12"
            ),
            explanation=_t(
                "Cada una de las tres iteraciones exteriores inicia cuatro iteraciones interiores. El orden muestra que se completa una fila antes de pasar a la siguiente.",
                "Each of the three outer iterations starts four inner iterations. The order shows that one row is completed before moving to the next.",
                "Hver af de tre ydre iterationer starter fire indre iterationer. Rækkefølgen viser, at én række afsluttes, før den næste begynder.",
            ),
        ),
    ),
    practice_exercises=(
        LocalizedPracticeExercise(
            exercise_id="m03.p01",
            activity_type=ActivityType.CODE_TRACING,
            prompt=_t(
                "Traza el código e indica los valores impresos: x = 2; while x < 9: print(x); x += 3.",
                "Trace the code and give the printed values: x = 2; while x < 9: print(x); x += 3.",
                "Gennemgå koden og angiv de udskrevne værdier: x = 2; while x < 9: print(x); x += 3.",
            ),
            hints=(
                _t("Comprueba la condición antes de imprimir.", "Check the condition before printing.", "Kontrollér betingelsen før udskrivning."),
                _t("Registra x después de sumar 3.", "Record x after adding 3.", "Registrér x efter at have lagt 3 til."),
            ),
            starter_code=_same("x = 2\nwhile x < 9:\n    print(x)\n    x += 3"),
            solution=_same("2\n5\n8"),
            explanation=_t(
                "Los estados iniciales de las tres iteraciones son 2, 5 y 8. Después, x pasa a 11 y la condición es falsa.",
                "The three iteration-start states are 2, 5, and 8. Then x becomes 11 and the condition is false.",
                "Tilstandene ved starten af de tre iterationer er 2, 5 og 8. Derefter bliver x 11, og betingelsen er falsk.",
            ),
        ),
        LocalizedPracticeExercise(
            exercise_id="m03.p02",
            activity_type=ActivityType.DEBUGGING,
            prompt=_t(
                "Corrige el bucle infinito y explica por qué no progresa.",
                "Correct the infinite loop and explain why it makes no progress.",
                "Ret den uendelige løkke og forklar, hvorfor den ikke gør fremskridt.",
            ),
            hints=(
                _t("La condición depende de count.", "The condition depends on count.", "Betingelsen afhænger af count."),
                _t("Alguna instrucción del cuerpo debe acercar count a 5.", "A body statement must move count towards 5.", "En instruktion i kroppen skal føre count mod 5."),
            ),
            starter_code=_same("count = 0\nwhile count < 5:\n    print(count)"),
            solution=_same("count = 0\nwhile count < 5:\n    print(count)\n    count += 1"),
            explanation=_t(
                "Sin count += 1, count permanece en 0 y count < 5 nunca cambia a False.",
                "Without count += 1, count remains 0 and count < 5 never becomes False.",
                "Uden count += 1 forbliver count 0, og count < 5 bliver aldrig False.",
            ),
        ),
        LocalizedPracticeExercise(
            exercise_id="m03.p03",
            activity_type=ActivityType.FILL_IN_THE_BLANK,
            prompt=_t(
                "Completa range para producir 2, 5, 8 y 11.",
                "Complete range to produce 2, 5, 8, and 11.",
                "Fuldfør range, så den producerer 2, 5, 8 og 11.",
            ),
            hints=(
                _t("El incremento es 3.", "The increment is 3.", "Trinnet er 3."),
                _t("stop debe quedar después de 11 porque no se incluye.", "stop must lie beyond 11 because it is excluded.", "stop skal ligge efter 11, fordi værdien ikke medtages."),
            ),
            starter_code=_same("for value in range(____, ____, ____):\n    print(value)"),
            solution=_same("range(2, 12, 3)"),
            explanation=_t(
                "range(2, 12, 3) comienza en 2, añade 3 y se detiene antes de 12.",
                "range(2, 12, 3) starts at 2, adds 3, and stops before 12.",
                "range(2, 12, 3) starter ved 2, lægger 3 til og stopper før 12.",
            ),
        ),
        LocalizedPracticeExercise(
            exercise_id="m03.p04",
            activity_type=ActivityType.CODE_COMPLETION,
            prompt=_t(
                "Completa un contador que registre cuántos enteros de 1 a 20 son divisibles por 4.",
                "Complete a counter that records how many integers from 1 to 20 are divisible by 4.",
                "Fuldfør en tæller, der registrerer hvor mange heltal fra 1 til 20 der er delelige med 4.",
            ),
            hints=(
                _t("El resto de dividir por 4 debe ser 0.", "The remainder after division by 4 must be 0.", "Resten efter division med 4 skal være 0."),
                _t("range debe incluir 20.", "range must include 20.", "range skal medtage 20."),
            ),
            starter_code=_same(
                "count = 0\nfor value in range(1, ____):\n    if __________________:\n        count += 1\nprint(count)"
            ),
            solution=_same(
                "count = 0\nfor value in range(1, 21):\n    if value % 4 == 0:\n        count += 1\nprint(count)"
            ),
            explanation=_t(
                "Los valores 4, 8, 12, 16 y 20 cumplen el criterio, por lo que el resultado es 5.",
                "The values 4, 8, 12, 16, and 20 satisfy the criterion, so the result is 5.",
                "Værdierne 4, 8, 12, 16 og 20 opfylder kriteriet, så resultatet er 5.",
            ),
        ),
        LocalizedPracticeExercise(
            exercise_id="m03.p05",
            activity_type=ActivityType.SHORT_ANSWER,
            prompt=_t(
                "Explica por qué range(5) produce cinco valores aunque 5 no aparezca.",
                "Explain why range(5) produces five values even though 5 does not appear.",
                "Forklar hvorfor range(5) producerer fem værdier, selv om 5 ikke forekommer.",
            ),
            hints=(
                _t("Enumera los valores desde 0.", "List the values starting from 0.", "Angiv værdierne fra 0."),
            ),
            solution=_t(
                "range(5) produce 0, 1, 2, 3 y 4. El límite superior es exclusivo, pero el conjunto contiene cinco enteros.",
                "range(5) produces 0, 1, 2, 3, and 4. The upper bound is exclusive, but the sequence contains five integers.",
                "range(5) producerer 0, 1, 2, 3 og 4. Den øvre grænse er eksklusiv, men sekvensen indeholder fem heltal.",
            ),
            explanation=_t(
                "Contar elementos y observar el último valor son preguntas diferentes.",
                "Counting elements and observing the last value are different questions.",
                "At tælle elementer og observere den sidste værdi er to forskellige spørgsmål.",
            ),
        ),
        LocalizedPracticeExercise(
            exercise_id="m03.p06",
            activity_type=ActivityType.CODE_TRACING,
            prompt=_t(
                "Traza total después de cada iteración: total = 0; for n in range(1, 5): total += n.",
                "Trace total after each iteration: total = 0; for n in range(1, 5): total += n.",
                "Gennemgå total efter hver iteration: total = 0; for n in range(1, 5): total += n.",
            ),
            hints=(
                _t("range(1, 5) genera 1, 2, 3 y 4.", "range(1, 5) generates 1, 2, 3, and 4.", "range(1, 5) genererer 1, 2, 3 og 4."),
            ),
            starter_code=_same("total = 0\nfor n in range(1, 5):\n    total += n"),
            solution=_same("n=1 → total=1\nn=2 → total=3\nn=3 → total=6\nn=4 → total=10"),
            explanation=_t(
                "El invariante es que total contiene la suma de los enteros ya recorridos.",
                "The invariant is that total contains the sum of the integers already traversed.",
                "Invarianten er, at total indeholder summen af de heltal, der allerede er gennemløbet.",
            ),
        ),
        LocalizedPracticeExercise(
            exercise_id="m03.p07",
            activity_type=ActivityType.DEBUGGING,
            prompt=_t(
                "Corrige el error de uno en uno para imprimir 1, 2, 3, 4 y 5.",
                "Correct the off-by-one error to print 1, 2, 3, 4, and 5.",
                "Ret én-for-lidt-fejlen, så 1, 2, 3, 4 og 5 udskrives.",
            ),
            hints=(
                _t("El valor stop no se incluye.", "The stop value is excluded.", "Stopværdien medtages ikke."),
            ),
            starter_code=_same("for number in range(1, 5):\n    print(number)"),
            solution=_same("for number in range(1, 6):\n    print(number)"),
            explanation=_t(
                "Para incluir 5, el límite exclusivo debe ser 6.",
                "To include 5, the exclusive bound must be 6.",
                "For at medtage 5 skal den eksklusive grænse være 6.",
            ),
        ),
        LocalizedPracticeExercise(
            exercise_id="m03.p08",
            activity_type=ActivityType.ORDERING,
            prompt=_t(
                "Ordena los elementos conceptuales de un while correcto: inicialización, comprobación, trabajo, actualización y nueva comprobación.",
                "Order the conceptual parts of a correct while loop: initialization, check, work, update, and new check.",
                "Sæt de konceptuelle dele af en korrekt while-løkke i rækkefølge: initialisering, kontrol, arbejde, opdatering og ny kontrol.",
            ),
            hints=(
                _t("La primera comprobación ocurre antes del cuerpo.", "The first check occurs before the body.", "Den første kontrol sker før kroppen."),
            ),
            solution=_t(
                "Inicialización → comprobación → trabajo → actualización → nueva comprobación.",
                "Initialization → check → work → update → new check.",
                "Initialisering → kontrol → arbejde → opdatering → ny kontrol.",
            ),
            explanation=_t(
                "La nueva comprobación decide si comienza otra iteración.",
                "The new check decides whether another iteration begins.",
                "Den nye kontrol afgør, om endnu en iteration begynder.",
            ),
        ),
        LocalizedPracticeExercise(
            exercise_id="m03.p09",
            activity_type=ActivityType.CODE_COMPLETION,
            prompt=_t(
                "Completa un bucle con centinela -1 que sume valores no negativos sin sumar el centinela.",
                "Complete a loop with sentinel -1 that sums non-negative values without adding the sentinel.",
                "Fuldfør en løkke med stopværdien -1, der summerer ikke-negative værdier uden at medtage stopværdien.",
            ),
            hints=(
                _t("Lee el primer valor antes del while.", "Read the first value before the while loop.", "Læs den første værdi før while-løkken."),
                _t("Lee el siguiente valor al final del cuerpo.", "Read the next value at the end of the body.", "Læs den næste værdi sidst i kroppen."),
            ),
            starter_code=_same(
                "total = 0\nvalue = int(input())\nwhile __________:\n    total += value\n    value = int(input())"
            ),
            solution=_same(
                "total = 0\nvalue = int(input())\nwhile value != -1:\n    total += value\n    value = int(input())"
            ),
            explanation=_t(
                "La condición se comprueba antes de sumar, por lo que -1 termina el bucle sin formar parte del total.",
                "The condition is checked before addition, so -1 ends the loop without becoming part of the total.",
                "Betingelsen kontrolleres før addition, så -1 afslutter løkken uden at indgå i totalen.",
            ),
        ),
        LocalizedPracticeExercise(
            exercise_id="m03.p10",
            activity_type=ActivityType.SHORT_ANSWER,
            prompt=_t(
                "Propón una medida de progreso para un while que reduce remaining en 2 hasta llegar a 0 o menos.",
                "Propose a progress measure for a while loop that reduces remaining by 2 until it reaches 0 or less.",
                "Foreslå et fremdriftsmål for en while-løkke, der reducerer remaining med 2, indtil den når 0 eller mindre.",
            ),
            hints=(
                _t("Relaciona la medida con la distancia hasta el límite.", "Relate the measure to distance from the bound.", "Knyt målet til afstanden fra grænsen."),
            ),
            solution=_t(
                "remaining es una medida de progreso: disminuye en 2 en cada iteración y está acotada inferiormente por el criterio de salida remaining <= 0.",
                "remaining is a progress measure: it decreases by 2 each iteration and is bounded below by the exit criterion remaining <= 0.",
                "remaining er et fremdriftsmål: det falder med 2 i hver iteration og er nedad afgrænset af afslutningskriteriet remaining <= 0.",
            ),
            explanation=_t(
                "La combinación de cambio monótono y límite permite argumentar la terminación.",
                "Monotonic change plus a bound supports a termination argument.",
                "Monoton ændring kombineret med en grænse understøtter et afslutningsargument.",
            ),
        ),
        LocalizedPracticeExercise(
            exercise_id="m03.p11",
            activity_type=ActivityType.CODE_TRACING,
            prompt=_t(
                "Indica cuántas veces se ejecuta print: for row in range(2): for col in range(3): print(row, col).",
                "State how many times print executes: for row in range(2): for col in range(3): print(row, col).",
                "Angiv hvor mange gange print udføres: for row in range(2): for col in range(3): print(row, col).",
            ),
            hints=(
                _t("Multiplica las iteraciones exterior e interior.", "Multiply outer and inner iteration counts.", "Multiplicér antallet af ydre og indre iterationer."),
            ),
            solution=_same("6"),
            explanation=_t(
                "El bucle exterior se ejecuta 2 veces y, en cada una, el interior 3 veces: 2 × 3 = 6.",
                "The outer loop executes 2 times and the inner loop 3 times each: 2 × 3 = 6.",
                "Den ydre løkke udføres 2 gange og den indre 3 gange hver gang: 2 × 3 = 6.",
            ),
        ),
        LocalizedPracticeExercise(
            exercise_id="m03.p12",
            activity_type=ActivityType.ORAL_EXPLANATION,
            prompt=_t(
                "Explica cuándo elegirías while y cuándo for. Incluye un ejemplo y una prueba de límite para cada uno.",
                "Explain when you would choose while and when for. Include one example and one boundary test for each.",
                "Forklar hvornår du ville vælge while, og hvornår for. Medtag et eksempel og en grænsetest for hver.",
            ),
            hints=(
                _t("Distingue repetición controlada por condición y repetición acotada por un iterable.", "Distinguish condition-controlled repetition from iterable-bounded repetition.", "Skeln mellem betingelsesstyret gentagelse og gentagelse afgrænset af et iterabelt objekt."),
            ),
            solution=_t(
                "while es apropiado cuando el número de iteraciones depende de una condición que cambia durante la ejecución; debe probarse también el caso de cero iteraciones. for es apropiado cuando se recorre un rango o iterable conocido; debe probarse el límite superior exclusivo.",
                "while is appropriate when iteration count depends on a condition that changes during execution; the zero-iteration case should be tested. for is appropriate for a known range or iterable; its exclusive upper bound should be tested.",
                "while er passende, når antallet af iterationer afhænger af en betingelse, der ændres under udførelsen; nul-iterations-tilfældet bør testes. for er passende for et kendt interval eller iterabelt objekt; den eksklusive øvre grænse bør testes.",
            ),
            explanation=_t(
                "La elección debe comunicar la estructura real del problema y facilitar la verificación.",
                "The choice should communicate the real problem structure and support verification.",
                "Valget bør kommunikere problemets reelle struktur og understøtte verificering.",
            ),
        ),
    ),
    assessment_items=(
        LocalizedAssessmentItem(
            item_id="m03.a01",
            activity_type=ActivityType.MULTIPLE_CHOICE,
            prompt=_t("¿Qué estructura es más directa para repetir exactamente 12 veces?", "Which structure is most direct for repeating exactly 12 times?", "Hvilken struktur er mest direkte til at gentage præcis 12 gange?"),
            options=(
                _option("for", "for con range(12)", "for with range(12)", "for med range(12)"),
                _option("while_true", "while True sin break", "while True without break", "while True uden break"),
                _option("if", "if ejecutado 12 veces", "if executed 12 times", "if udført 12 gange"),
                _option("recursion", "Recursión sin caso base", "Recursion without a base case", "Rekursion uden basistilfælde"),
            ),
            correct_option_ids=("for",),
            accepted_answers=(),
            explanation=_t("for con range expresa de forma directa una repetición acotada conocida.", "for with range directly expresses known bounded repetition.", "for med range udtrykker direkte en kendt afgrænset gentagelse."),
        ),
        LocalizedAssessmentItem(
            item_id="m03.a02",
            activity_type=ActivityType.TRUE_FALSE,
            prompt=_t("Un while puede ejecutar su cuerpo cero veces.", "A while loop may execute its body zero times.", "En while-løkke kan udføre sin krop nul gange."),
            options=(_option("true", "Verdadero", "True", "Sandt"), _option("false", "Falso", "False", "Falsk")),
            correct_option_ids=("true",),
            accepted_answers=(),
            explanation=_t("La condición se evalúa antes del cuerpo.", "The condition is evaluated before the body.", "Betingelsen evalueres før kroppen."),
        ),
        LocalizedAssessmentItem(
            item_id="m03.a03",
            activity_type=ActivityType.CODE_TRACING,
            prompt=_t("Indica la salida exacta:\nfor n in range(2, 8, 2):\n    print(n)", "Give the exact output:\nfor n in range(2, 8, 2):\n    print(n)", "Angiv det præcise output:\nfor n in range(2, 8, 2):\n    print(n)"),
            options=(),
            correct_option_ids=(),
            accepted_answers=(_same("2\n4\n6"),),
            explanation=_t("8 es el límite exclusivo.", "8 is the exclusive bound.", "8 er den eksklusive grænse."),
            rubric=(_t("Incluye 2, 4 y 6 en ese orden.", "Includes 2, 4, and 6 in that order.", "Medtager 2, 4 og 6 i den rækkefølge."),),
        ),
        LocalizedAssessmentItem(
            item_id="m03.a04",
            activity_type=ActivityType.FILL_IN_THE_BLANK,
            prompt=_t("Completa la actualización para garantizar progreso: while count < 10: count ____ 1.", "Complete the update to guarantee progress: while count < 10: count ____ 1.", "Fuldfør opdateringen for at sikre fremdrift: while count < 10: count ____ 1."),
            options=(),
            correct_option_ids=(),
            accepted_answers=(_same("+=\n"), _same("+=")),
            explanation=_t("count += 1 aumenta la variable utilizada por la condición.", "count += 1 increases the variable used by the condition.", "count += 1 øger variablen, der bruges i betingelsen."),
        ),
        LocalizedAssessmentItem(
            item_id="m03.a05",
            activity_type=ActivityType.DEBUGGING,
            prompt=_t("Corrige el bucle para imprimir 5, 4, 3, 2, 1 y terminar.", "Correct the loop to print 5, 4, 3, 2, 1 and terminate.", "Ret løkken, så den udskriver 5, 4, 3, 2, 1 og afslutter."),
            options=(),
            correct_option_ids=(),
            accepted_answers=(_same("value = 5\nwhile value > 0:\n    print(value)\n    value -= 1"),),
            explanation=_t("La actualización debe reducir value hacia el límite 0.", "The update must reduce value towards the bound 0.", "Opdateringen skal reducere value mod grænsen 0."),
            rubric=(
                _t("Usa una condición que excluye 0.", "Uses a condition that excludes 0.", "Bruger en betingelse, der udelukker 0."),
                _t("Reduce value en cada iteración.", "Decreases value each iteration.", "Reducerer value i hver iteration."),
                _t("Conserva el orden 5 a 1.", "Preserves the order 5 to 1.", "Bevarer rækkefølgen 5 til 1."),
            ),
        ),
        LocalizedAssessmentItem(
            item_id="m03.a06",
            activity_type=ActivityType.MULTIPLE_SELECT,
            prompt=_t("Selecciona todas las propiedades necesarias para argumentar la terminación de un while.", "Select every property needed to argue that a while loop terminates.", "Vælg alle egenskaber, der er nødvendige for at argumentere for, at en while-løkke afslutter."),
            options=(
                _option("progress", "Existe una medida de progreso", "A progress measure exists", "Der findes et fremdriftsmål"),
                _option("bound", "La medida está acotada", "The measure is bounded", "Målet er afgrænset"),
                _option("change", "Cada iteración acerca la medida al límite", "Each iteration moves the measure towards the bound", "Hver iteration fører målet mod grænsen"),
                _option("print", "El cuerpo contiene print", "The body contains print", "Kroppen indeholder print"),
            ),
            correct_option_ids=("progress", "bound", "change"),
            accepted_answers=(),
            explanation=_t("La salida visible no garantiza progreso ni terminación.", "Visible output does not guarantee progress or termination.", "Synligt output garanterer ikke fremdrift eller afslutning."),
        ),
        LocalizedAssessmentItem(
            item_id="m03.a07",
            activity_type=ActivityType.MATCHING,
            prompt=_t("Relaciona cada patrón con su propósito.", "Match each pattern with its purpose.", "Match hvert mønster med dets formål."),
            options=(
                _option("counter", "contador → número de ocurrencias", "counter → number of occurrences", "tæller → antal forekomster"),
                _option("accumulator", "acumulador → resultado parcial combinado", "accumulator → combined partial result", "akkumulator → kombineret delresultat"),
                _option("flag", "indicador → estado booleano recordado", "flag → remembered Boolean state", "flag → husket boolesk tilstand"),
                _option("best", "mejor valor → máximo o mínimo observado", "best value → observed maximum or minimum", "bedste værdi → observeret maksimum eller minimum"),
            ),
            correct_option_ids=("counter", "accumulator", "flag", "best"),
            accepted_answers=(),
            explanation=_t("Cada patrón mantiene una forma distinta de estado durante el recorrido.", "Each pattern maintains a different form of state during traversal.", "Hvert mønster vedligeholder en forskellig form for tilstand under gennemløbet."),
        ),
        LocalizedAssessmentItem(
            item_id="m03.a08",
            activity_type=ActivityType.ORDERING,
            prompt=_t("Ordena las acciones de un acumulador de suma.", "Order the actions of a summation accumulator.", "Sæt handlingerne for en sumakkumulator i rækkefølge."),
            options=(
                _option("initialize", "Inicializar total en 0", "Initialize total to 0", "Initialisér total til 0"),
                _option("obtain", "Obtener el siguiente valor", "Obtain the next value", "Hent den næste værdi"),
                _option("combine", "Sumar el valor a total", "Add the value to total", "Læg værdien til total"),
                _option("repeat", "Repetir mientras queden valores", "Repeat while values remain", "Gentag mens der er værdier tilbage"),
                _option("report", "Mostrar total final", "Report the final total", "Vis den endelige total"),
            ),
            correct_option_ids=("initialize", "obtain", "combine", "repeat", "report"),
            accepted_answers=(),
            explanation=_t("La identidad 0 se establece antes de combinar valores y el resultado se informa al final.", "The identity 0 is established before combining values and the result is reported at the end.", "Identiteten 0 etableres før værdier kombineres, og resultatet vises til sidst."),
        ),
        LocalizedAssessmentItem(
            item_id="m03.a09",
            activity_type=ActivityType.SHORT_ANSWER,
            prompt=_t("Define un invariante adecuado para sumar los enteros 1 a n con un bucle.", "Define a suitable invariant for summing the integers 1 through n with a loop.", "Definér en passende invariant til at summere heltallene 1 til n med en løkke."),
            options=(),
            correct_option_ids=(),
            accepted_answers=(_t("Después de procesar k, total contiene la suma de 1 hasta k.", "After processing k, total contains the sum from 1 through k.", "Efter behandling af k indeholder total summen fra 1 til k."),),
            explanation=_t("El invariante relaciona el estado parcial con los elementos ya procesados.", "The invariant relates partial state to the elements already processed.", "Invarianten knytter deltilstanden til de elementer, der allerede er behandlet."),
            rubric=(
                _t("Identifica qué elementos se han procesado.", "Identifies which elements have been processed.", "Identificerer hvilke elementer der er behandlet."),
                _t("Relaciona total con la suma parcial correcta.", "Relates total to the correct partial sum.", "Knytter total til den korrekte delsum."),
            ),
        ),
        LocalizedAssessmentItem(
            item_id="m03.a10",
            activity_type=ActivityType.CODE_COMPLETION,
            prompt=_t("Completa un for que imprima 10, 8, 6, 4 y 2.", "Complete a for loop that prints 10, 8, 6, 4, and 2.", "Fuldfør en for-løkke, der udskriver 10, 8, 6, 4 og 2."),
            options=(),
            correct_option_ids=(),
            accepted_answers=(_same("for value in range(10, 1, -2):\n    print(value)"),),
            explanation=_t("El step negativo reduce value y stop=1 permite incluir 2.", "The negative step reduces value and stop=1 allows 2 to be included.", "Det negative trin reducerer value, og stop=1 gør det muligt at medtage 2."),
        ),
        LocalizedAssessmentItem(
            item_id="m03.a11",
            activity_type=ActivityType.DATA_INTERPRETATION,
            prompt=_t("Una tabla de trazado muestra count: 0, 1, 2, 3, 4 y después la condición count < 4 es False. ¿Cuántas veces se ejecutó el cuerpo?", "A trace table shows count: 0, 1, 2, 3, 4 and then count < 4 is False. How many times did the body execute?", "En gennemgangstabel viser count: 0, 1, 2, 3, 4, og derefter er count < 4 False. Hvor mange gange blev kroppen udført?"),
            options=(),
            correct_option_ids=(),
            accepted_answers=(_same("4"),),
            explanation=_t("El cuerpo se ejecutó con count igual a 0, 1, 2 y 3.", "The body executed with count equal to 0, 1, 2, and 3.", "Kroppen blev udført med count lig 0, 1, 2 og 3."),
        ),
        LocalizedAssessmentItem(
            item_id="m03.a12",
            activity_type=ActivityType.TRUE_FALSE,
            prompt=_t("continue termina inmediatamente el bucle actual.", "continue immediately terminates the current loop.", "continue afslutter straks den aktuelle løkke."),
            options=(_option("true", "Verdadero", "True", "Sandt"), _option("false", "Falso", "False", "Falsk")),
            correct_option_ids=("false",),
            accepted_answers=(),
            explanation=_t("continue salta a la siguiente iteración; break termina el bucle.", "continue skips to the next iteration; break terminates the loop.", "continue går videre til næste iteration; break afslutter løkken."),
        ),
        LocalizedAssessmentItem(
            item_id="m03.a13",
            activity_type=ActivityType.SHORT_ANSWER,
            prompt=_t("¿Cuántas veces se ejecuta el cuerpo interior si range(4) contiene el exterior y range(7) el interior? Justifica.", "How many times does the inner body execute when range(4) controls the outer loop and range(7) the inner loop? Justify.", "Hvor mange gange udføres den indre krop, når range(4) styrer den ydre løkke og range(7) den indre? Begrund."),
            options=(),
            correct_option_ids=(),
            accepted_answers=(_t("28, porque 4 iteraciones exteriores ejecutan 7 iteraciones interiores cada una.", "28, because 4 outer iterations each execute 7 inner iterations.", "28, fordi 4 ydre iterationer hver udfører 7 indre iterationer."),),
            explanation=_t("Los recuentos se multiplican: 4 × 7.", "The counts multiply: 4 × 7.", "Antallene multipliceres: 4 × 7."),
            rubric=(
                _t("Indica 28.", "States 28.", "Angiver 28."),
                _t("Explica el producto de los dos límites.", "Explains the product of the two bounds.", "Forklarer produktet af de to grænser."),
            ),
        ),
        LocalizedAssessmentItem(
            item_id="m03.a14",
            activity_type=ActivityType.ORAL_EXPLANATION,
            prompt=_t("Explica cómo probarías un while que procesa hasta encontrar un centinela, incluyendo el caso de entrada vacía.", "Explain how you would test a while loop that processes until a sentinel, including empty input.", "Forklar hvordan du ville teste en while-løkke, der behandler indtil en stopværdi, inklusive tomt input."),
            options=(),
            correct_option_ids=(),
            accepted_answers=(_t("Probaría el centinela como primer valor, un dato seguido del centinela, varios datos, un dato límite y comprobaría que el centinela no se procesa.", "I would test the sentinel as the first value, one datum followed by the sentinel, several data values, a boundary value, and verify that the sentinel is not processed.", "Jeg ville teste stopværdien som første værdi, én dataværdi efterfulgt af stopværdien, flere dataværdier, en grænseværdi og kontrollere, at stopværdien ikke behandles."),),
            explanation=_t("Las pruebas deben verificar terminación, cero iteraciones y exclusión del centinela.", "Tests should verify termination, zero iterations, and exclusion of the sentinel.", "Test bør verificere afslutning, nul iterationer og udelukkelse af stopværdien."),
            rubric=(
                _t("Incluye el centinela como primera entrada.", "Includes the sentinel as the first input.", "Medtager stopværdien som første input."),
                _t("Incluye una y varias iteraciones.", "Includes one and several iterations.", "Medtager én og flere iterationer."),
                _t("Comprueba que el centinela no se acumula.", "Checks that the sentinel is not accumulated.", "Kontrollerer at stopværdien ikke akkumuleres."),
                _t("Verifica que el bucle termina.", "Verifies that the loop terminates.", "Verificerer at løkken afslutter."),
            ),
        ),
    ),
    tutor_support=LocalizedTutorSupportPacket(
        canonical_explanation=_t(
            "La iteración controlada modela una secuencia de estados. Antes de escribir un bucle deben identificarse el "
            "estado inicial, la regla de continuación, el trabajo de una iteración, la actualización y el estado final "
            "esperado. while es adecuado cuando el número de iteraciones depende de una condición que cambia durante la "
            "ejecución. for es preferible cuando el recorrido está acotado por un rango o iterable conocido. range usa "
            "un límite superior exclusivo, por lo que range(n) genera exactamente n valores desde 0 hasta n - 1. Un "
            "contador registra ocurrencias; un acumulador conserva un resultado parcial; una variable de mejor valor "
            "mantiene el máximo o mínimo observado. La corrección requiere dos argumentos distintos: terminación y "
            "resultado. Para la terminación se busca una medida de progreso acotada que se acerque al límite en cada "
            "iteración. Para el resultado se formula un invariante que relaciona el estado actual con los elementos ya "
            "procesados. Los valores centinela, break y continue son válidos cuando expresan una condición excepcional "
            "de forma más clara, pero no deben dispersar la lógica de control. Los bucles anidados multiplican sus "
            "recuentos de iteración y break solo abandona el bucle más interno. La verificación debe cubrir cero, una y "
            "varias iteraciones, límites exactos, falta de progreso, acumuladores inicializados correctamente y todas "
            "las salidas posibles. Los ejemplos biomédicos del módulo son escenarios de programación didácticos y no "
            "representan protocolos, umbrales clínicos ni recomendaciones de laboratorio.",
            "Controlled iteration models a sequence of states. Before writing a loop, identify the initial state, "
            "continuation rule, work performed by one iteration, update, and expected final state. while is suitable when "
            "the iteration count depends on a condition that changes during execution. for is preferable when traversal "
            "is bounded by a known range or iterable. range uses an exclusive upper bound, so range(n) generates exactly "
            "n values from 0 through n - 1. A counter records occurrences; an accumulator preserves a partial result; a "
            "best-value variable retains the maximum or minimum observed. Correctness requires two distinct arguments: "
            "termination and result. Termination uses a bounded progress measure that moves towards its limit each "
            "iteration. Result correctness uses an invariant relating current state to elements already processed. "
            "Sentinels, break, and continue are valid when they express an exceptional condition more clearly, but they "
            "should not scatter control logic. Nested loops multiply their iteration counts and break exits only the "
            "innermost loop. Verification should cover zero, one, and several iterations, exact boundaries, missing "
            "progress, correctly initialized accumulators, and every possible exit. Biomedical examples in this module "
            "are programming exercises, not protocols, clinical thresholds, or laboratory recommendations.",
            "Kontrolleret iteration modellerer en sekvens af tilstande. Før en løkke skrives, identificeres starttilstanden, "
            "fortsættelsesreglen, arbejdet i én iteration, opdateringen og den forventede sluttilstand. while er passende, "
            "når antallet af iterationer afhænger af en betingelse, der ændres under udførelsen. for er at foretrække, når "
            "gennemløbet er afgrænset af et kendt interval eller iterabelt objekt. range bruger en eksklusiv øvre grænse, "
            "så range(n) genererer præcis n værdier fra 0 til n - 1. En tæller registrerer forekomster; en akkumulator "
            "bevarer et delresultat; en variabel for bedste værdi bevarer det observerede maksimum eller minimum. "
            "Korrekthed kræver to forskellige argumenter: afslutning og resultat. Afslutning bruger et afgrænset "
            "fremdriftsmål, der bevæger sig mod sin grænse i hver iteration. Resultatkorrekthed bruger en invariant, der "
            "knytter den aktuelle tilstand til allerede behandlede elementer. Stopværdier, break og continue er gyldige, "
            "når de tydeliggør en undtagelsestilstand, men de bør ikke sprede kontrollogikken. Indlejrede løkker "
            "multiplicerer deres iterationsantal, og break forlader kun den inderste løkke. Verificering bør dække nul, "
            "én og flere iterationer, præcise grænser, manglende fremdrift, korrekt initialiserede akkumulatorer og alle "
            "mulige afslutninger. Modulets biomedicinske eksempler er programmeringsøvelser og ikke protokoller, kliniske "
            "grænser eller laboratorieanbefalinger.",
        ),
        knowledge_fragments=(
            _t("while evalúa su condición antes de cada iteración.", "while evaluates its condition before every iteration.", "while evaluerer sin betingelse før hver iteration."),
            _t("Un while puede ejecutar cero veces.", "A while loop may execute zero times.", "En while-løkke kan udføres nul gange."),
            _t("Una medida de progreso acotada sustenta el argumento de terminación.", "A bounded progress measure supports a termination argument.", "Et afgrænset fremdriftsmål understøtter et afslutningsargument."),
            _t("Un invariante debe mantenerse antes y después de cada iteración.", "An invariant must hold before and after each iteration.", "En invariant skal gælde før og efter hver iteration."),
            _t("range(stop) excluye stop.", "range(stop) excludes stop.", "range(stop) udelukker stop."),
            _t("range(n) genera exactamente n enteros desde 0.", "range(n) generates exactly n integers starting at 0.", "range(n) genererer præcis n heltal fra 0."),
            _t("Un contador registra ocurrencias y suele comenzar en 0.", "A counter records occurrences and usually starts at 0.", "En tæller registrerer forekomster og begynder normalt ved 0."),
            _t("Un acumulador de suma utiliza 0 como identidad inicial.", "A summation accumulator uses 0 as its initial identity.", "En sumakkumulator bruger 0 som startidentitet."),
            _t("El centinela controla el final y no debe procesarse como dato.", "A sentinel controls termination and should not be processed as data.", "En stopværdi styrer afslutningen og bør ikke behandles som data."),
            _t("break termina el bucle más interno.", "break terminates the innermost loop.", "break afslutter den inderste løkke."),
            _t("continue omite el resto del cuerpo y pasa a la siguiente iteración.", "continue skips the rest of the body and moves to the next iteration.", "continue springer resten af kroppen over og går til næste iteration."),
            _t("Los recuentos de dos bucles anidados suelen multiplicarse.", "The counts of two nested loops usually multiply.", "Antallene for to indlejrede løkker multipliceres normalt."),
            _t("Cero, una y varias iteraciones requieren pruebas distintas.", "Zero, one, and many iterations require distinct tests.", "Nul, én og mange iterationer kræver forskellige test."),
            _t("Un límite de tiempo detecta una posible no terminación, pero no demuestra corrección.", "A time limit detects possible non-termination but does not prove correctness.", "En tidsgrænse opdager mulig manglende afslutning, men beviser ikke korrekthed."),
        ),
        common_misconceptions=(
            _t("Creer que while ejecuta el cuerpo al menos una vez.", "Believing while always executes at least once.", "At tro at while altid udføres mindst én gang."),
            _t("Olvidar actualizar una variable de la condición.", "Forgetting to update a variable used by the condition.", "At glemme at opdatere en variabel i betingelsen."),
            _t("Suponer que range incluye su límite superior.", "Assuming range includes its upper bound.", "At antage at range medtager sin øvre grænse."),
            _t("Inicializar una suma en 1.", "Initializing a sum to 1.", "At initialisere en sum til 1."),
            _t("Usar un número arbitrario como máximo inicial sin justificarlo.", "Using an arbitrary initial maximum without justification.", "At bruge et vilkårligt startmaksimum uden begrundelse."),
            _t("Sumar el valor centinela antes de comprobarlo.", "Adding the sentinel before checking it.", "At lægge stopværdien til før den kontrolleres."),
            _t("Creer que continue termina el bucle.", "Believing continue terminates the loop.", "At tro at continue afslutter løkken."),
            _t("Creer que break abandona todos los bucles anidados.", "Believing break exits every nested loop.", "At tro at break forlader alle indlejrede løkker."),
            _t("Confundir número de iteraciones con último valor de range.", "Confusing iteration count with the last range value.", "At forveksle iterationsantal med den sidste range-værdi."),
            _t("Probar solo un caso con varias iteraciones.", "Testing only one many-iteration case.", "Kun at teste ét tilfælde med mange iterationer."),
            _t("Considerar correcto un bucle solo porque termina.", "Considering a loop correct merely because it terminates.", "At betragte en løkke som korrekt alene fordi den afslutter."),
            _t("Añadir break para ocultar una condición de bucle mal diseñada.", "Adding break to hide a poorly designed loop condition.", "At tilføje break for at skjule en dårligt designet løkkebetingelse."),
        ),
        socratic_questions=(
            _t("¿Qué variables describen el estado antes de la primera iteración?", "Which variables describe state before the first iteration?", "Hvilke variable beskriver tilstanden før første iteration?"),
            _t("¿Qué condición exacta permite otra iteración?", "What exact condition permits another iteration?", "Hvilken præcis betingelse tillader endnu en iteration?"),
            _t("¿Qué instrucción demuestra progreso hacia la salida?", "Which statement demonstrates progress towards exit?", "Hvilken instruktion viser fremdrift mod afslutning?"),
            _t("¿Qué propiedad permanece cierta después de cada iteración?", "Which property remains true after every iteration?", "Hvilken egenskab forbliver sand efter hver iteration?"),
            _t("¿Cuáles son exactamente los valores producidos por range?", "What exact values are produced by range?", "Hvilke præcise værdier produceres af range?"),
            _t("¿Esta variable es contador, acumulador, indicador o mejor valor?", "Is this variable a counter, accumulator, flag, or best value?", "Er denne variabel en tæller, akkumulator, et flag eller en bedste værdi?"),
            _t("¿El centinela se comprueba antes o después de procesar el dato?", "Is the sentinel checked before or after processing the datum?", "Kontrolleres stopværdien før eller efter behandling af data?"),
            _t("¿Qué instrucciones se omiten cuando se ejecuta continue?", "Which statements are skipped when continue executes?", "Hvilke instruktioner springes over, når continue udføres?"),
            _t("¿Qué bucle abandona este break?", "Which loop does this break exit?", "Hvilken løkke forlader dette break?"),
            _t("¿Cuántas combinaciones produce el producto de los límites?", "How many combinations does the product of the bounds produce?", "Hvor mange kombinationer giver produktet af grænserne?"),
            _t("¿Qué entrada produce cero iteraciones?", "Which input produces zero iterations?", "Hvilket input giver nul iterationer?"),
            _t("¿Qué prueba distingue n de n + 1 iteraciones?", "Which test distinguishes n from n + 1 iterations?", "Hvilken test skelner mellem n og n + 1 iterationer?"),
        ),
        grading_criteria=(
            _t("Identifica correctamente estado, condición y actualización.", "Correctly identifies state, condition, and update.", "Identificerer korrekt tilstand, betingelse og opdatering."),
            _t("Distingue while de for según la estructura del problema.", "Distinguishes while from for according to problem structure.", "Skelner while fra for ud fra problemets struktur."),
            _t("Predice con precisión los valores de range.", "Accurately predicts range values.", "Forudsiger range-værdier præcist."),
            _t("Traza el orden real de condición, cuerpo y actualización.", "Traces the actual order of condition, body, and update.", "Gennemgår den faktiske rækkefølge af betingelse, krop og opdatering."),
            _t("Formula una medida de progreso y un límite.", "States a progress measure and a bound.", "Angiver et fremdriftsmål og en grænse."),
            _t("Formula un invariante relacionado con el resultado parcial.", "States an invariant related to the partial result.", "Angiver en invariant knyttet til delresultatet."),
            _t("Inicializa contadores y acumuladores con valores coherentes.", "Initializes counters and accumulators coherently.", "Initialiserer tællere og akkumulatorer sammenhængende."),
            _t("Utiliza break y continue solo con una justificación clara.", "Uses break and continue only with clear justification.", "Bruger kun break og continue med klar begrundelse."),
            _t("Calcula correctamente el número de operaciones de bucles anidados.", "Correctly calculates nested-loop operation counts.", "Beregner korrekt antallet af operationer i indlejrede løkker."),
            _t("Diseña pruebas para cero, una, varias iteraciones y límites.", "Designs tests for zero, one, many iterations, and boundaries.", "Designer test for nul, én, mange iterationer og grænser."),
        ),
        response_constraints=(
            _t("Responder primero con una pista cuando el estudiante esté resolviendo un ejercicio.", "Give a hint first when the learner is solving an exercise.", "Giv først et hint, når den studerende løser en øvelse."),
            _t("No introducir funciones, clases ni comprensión de listas como atajos del módulo.", "Do not introduce functions, classes, or list comprehensions as shortcuts for this module.", "Indfør ikke funktioner, klasser eller list comprehensions som genveje i modulet."),
            _t("Separar siempre el argumento de terminación del argumento de resultado.", "Always separate the termination argument from the result argument.", "Adskil altid afslutningsargumentet fra resultatargumentet."),
            _t("Al explicar range, enumerar los valores concretos cuando sea útil.", "When explaining range, enumerate concrete values when useful.", "Ved forklaring af range skal konkrete værdier angives, når det er nyttigt."),
            _t("No aceptar un acumulador sin revisar su valor inicial.", "Do not accept an accumulator without checking its initial value.", "Acceptér ikke en akkumulator uden at kontrollere startværdien."),
            _t("Cuando aparezca break, indicar exactamente qué bucle termina.", "When break appears, state exactly which loop terminates.", "Når break forekommer, angiv præcist hvilken løkke der afsluttes."),
            _t("No presentar los valores didácticos como umbrales clínicos o de laboratorio.", "Do not present teaching values as clinical or laboratory thresholds.", "Præsentér ikke undervisningsværdier som kliniske eller laboratoriemæssige grænser."),
            _t("Mantener los ejemplos dentro del alcance de iteración, sin ocultar el proceso con bibliotecas avanzadas.", "Keep examples within iteration scope without hiding the process behind advanced libraries.", "Hold eksempler inden for iteration uden at skjule processen bag avancerede biblioteker."),
            _t("Si un bucle puede no terminar, señalar la entrada y la actualización responsables.", "If a loop may not terminate, identify the responsible input and update.", "Hvis en løkke muligvis ikke afslutter, identificér det ansvarlige input og opdateringen."),
        ),
        source_basis=(
            "Official DM857 course description, SDU, active version approved in 2025.",
            "Think Python, third edition, chapters on iteration, debugging, and incremental development.",
            "Introduction to Computation and Programming Using Python, third edition, sections on iteration, approximation, and testing.",
        ),
    ),
)

MODULE_03_ITERATION = LOCALIZED_MODULE_03_ITERATION.materialize(AppLocale.SPANISH_SPAIN)

__all__ = ["LOCALIZED_MODULE_03_ITERATION", "MODULE_03_ITERATION"]
