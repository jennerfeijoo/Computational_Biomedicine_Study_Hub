"""DM857 module 9: recursion, call stacks, termination, and testing."""

from __future__ import annotations

from ...i18n import AppLocale
from ...learning.activity_types import ActivityType
from ..localized_models import LocalizedLearningModule
from ..models import AssessmentItem, LearningModule
from .authoring import (
    authored_item,
    concept,
    example,
    objective,
    objective_mcq,
    objective_tf,
    practice,
    t,
    tutor_support,
)

LOCALIZED_MODULE_09_RECURSION = LocalizedLearningModule(
    course_code="DM857",
    module_id="dm857.m09",
    title=t(
        "Recursión, pila de llamadas y terminación",
        "Recursion, call stack, and termination",
        "Rekursion, kaldstak og terminering",
    ),
    summary=t(
        "Este módulo desarrolla la recursión como técnica para resolver un problema mediante versiones más pequeñas del mismo problema. Cubre casos base, progreso, pila de llamadas, trazado, secuencias, estructuras anidadas, equivalencia con iteración, complejidad, memoización introductoria y pruebas de terminación.",
        "This module develops recursion as a technique for solving a problem through smaller instances of the same problem. It covers base cases, progress, the call stack, tracing, sequences, nested structures, equivalence with iteration, complexity, introductory memoization, and termination tests.",
        "Dette modul udvikler rekursion som en teknik til at løse et problem gennem mindre instanser af samme problem. Det dækker basistilfælde, fremskridt, kaldstakken, gennemgang, sekvenser, indlejrede strukturer, ækvivalens med iteration, kompleksitet, introducerende memoization og termineringstest.",
    ),
    objectives=(
        objective(
            "m09.o1",
            (
                "Identificar la estructura recursiva de un problema.",
                "Identify the recursive structure of a problem.",
                "Identificere et problems rekursive struktur.",
            ),
        ),
        objective(
            "m09.o2",
            (
                "Diseñar casos base completos y alcanzables.",
                "Design complete and reachable base cases.",
                "Designe komplette og opnåelige basistilfælde.",
            ),
        ),
        objective(
            "m09.o3",
            (
                "Demostrar que cada llamada progresa hacia la terminación.",
                "Show that every call progresses toward termination.",
                "Vise at hvert kald bevæger sig mod terminering.",
            ),
        ),
        objective(
            "m09.o4",
            (
                "Trazar marcos, parámetros y retornos en la pila de llamadas.",
                "Trace frames, parameters, and returns on the call stack.",
                "Gennemgå frames, parametre og returværdier på kaldstakken.",
            ),
        ),
        objective(
            "m09.o5",
            (
                "Implementar recursión sobre números y secuencias.",
                "Implement recursion over numbers and sequences.",
                "Implementere rekursion over tal og sekvenser.",
            ),
        ),
        objective(
            "m09.o6",
            (
                "Procesar estructuras anidadas mediante descomposición recursiva.",
                "Process nested structures through recursive decomposition.",
                "Behandle indlejrede strukturer gennem rekursiv dekomponering.",
            ),
        ),
        objective(
            "m09.o7",
            (
                "Comparar soluciones recursivas e iterativas.",
                "Compare recursive and iterative solutions.",
                "Sammenligne rekursive og iterative løsninger.",
            ),
        ),
        objective(
            "m09.o8",
            (
                "Analizar coste, repetición de subproblemas, límites y pruebas.",
                "Analyze cost, repeated subproblems, limits, and tests.",
                "Analysere omkostning, gentagne delproblemer, grænser og test.",
            ),
        ),
    ),
    concepts=(
        concept(
            "recursive-contract",
            ("Contrato recursivo", "Recursive contract", "Rekursiv kontrakt"),
            (
                "Una función recursiva se llama directa o indirectamente para resolver una instancia más pequeña. Su contrato debe describir el dominio válido y permitir asumir que la llamada recursiva resuelve correctamente ese subproblema. El cuerpo combina ese resultado con el trabajo de la instancia actual. Recursión no significa repetición arbitraria: exige una relación estructural entre problema y subproblema.",
                "A recursive function calls itself directly or indirectly to solve a smaller instance. Its contract should define the valid domain and allow assuming that the recursive call correctly solves that subproblem. The body combines that result with work for the current instance. Recursion is not arbitrary repetition; it requires a structural relation between problem and subproblem.",
                "En rekursiv funktion kalder sig selv direkte eller indirekte for at løse en mindre instans. Kontrakten bør definere det gyldige domæne og tillade antagelsen om, at det rekursive kald løser delproblemet korrekt. Kroppen kombinerer resultatet med arbejdet for den aktuelle instans. Rekursion er ikke vilkårlig gentagelse.",
            ),
            (
                (
                    "El subproblema conserva la misma forma.",
                    "The subproblem keeps the same form.",
                    "Delproblemet bevarer samme form.",
                ),
                (
                    "La llamada recursiva tiene su propio marco.",
                    "The recursive call has its own frame.",
                    "Det rekursive kald har sin egen frame.",
                ),
                (
                    "La combinación reconstruye la solución actual.",
                    "Combination reconstructs the current solution.",
                    "Kombinationen rekonstruerer den aktuelle løsning.",
                ),
            ),
        ),
        concept(
            "base-cases",
            ("Casos base", "Base cases", "Basistilfælde"),
            (
                "El caso base resuelve directamente una instancia que ya no necesita descomposición. Debe cubrir las instancias mínimas del dominio y producir un valor compatible con la combinación posterior. Un caso base ausente causa llamadas sin fin; uno incorrecto contamina todos los retornos. Varias formas de entrada pueden requerir varios casos base.",
                "A base case directly solves an instance that needs no further decomposition. It must cover minimal domain instances and produce a value compatible with later combination. A missing base case causes endless calls; an incorrect one contaminates all returns. Several input shapes may require several base cases.",
                "Et basistilfælde løser direkte en instans, der ikke behøver yderligere dekomponering. Det skal dække minimale instanser og producere en værdi, som passer til den efterfølgende kombination. Et manglende basistilfælde giver uendelige kald; et forkert tilfælde forurener alle returværdier.",
            ),
            (
                (
                    "El caso base debe ser alcanzable.",
                    "The base case must be reachable.",
                    "Basistilfældet skal kunne nås.",
                ),
                (
                    "Su retorno debe respetar el tipo del contrato.",
                    "Its return must respect the contract type.",
                    "Returværdien skal følge kontraktens type.",
                ),
                (
                    "Entrada vacía suele ser una frontera importante.",
                    "Empty input is often an important boundary.",
                    "Tomt input er ofte en vigtig grænse.",
                ),
            ),
        ),
        concept(
            "progress-and-termination",
            ("Progreso y terminación", "Progress and termination", "Fremskridt og terminering"),
            (
                "Cada llamada debe reducir una medida bien fundada: un entero no negativo, la longitud de una secuencia o la profundidad restante de una estructura. La medida no puede decrecer indefinidamente y debe acercarse al caso base. Cambiar n por n+1 o enviar la misma secuencia rompe el progreso. La terminación se razona con la medida, no sólo observando ejemplos.",
                "Every call must reduce a well-founded measure: a non-negative integer, sequence length, or remaining structural depth. The measure cannot decrease indefinitely and must approach a base case. Changing n to n+1 or passing the same sequence breaks progress. Termination is reasoned from the measure, not merely observed in examples.",
                "Hvert kald skal reducere et velfunderet mål: et ikke-negativt heltal, sekvenslængde eller resterende strukturel dybde. Målet kan ikke falde uendeligt og skal nærme sig et basistilfælde. At ændre n til n+1 eller sende samme sekvens bryder fremskridtet. Terminering begrundes med målet.",
            ),
            (
                (
                    "Define una medida de progreso.",
                    "Define a progress measure.",
                    "Definér et fremskridtsmål.",
                ),
                (
                    "Cada rama recursiva debe reducirla.",
                    "Every recursive branch must reduce it.",
                    "Hver rekursiv gren skal reducere det.",
                ),
                (
                    "Todas las ramas deben alcanzar un caso base.",
                    "All branches must reach a base case.",
                    "Alle grene skal nå et basistilfælde.",
                ),
            ),
        ),
        concept(
            "call-stack-and-unwinding",
            ("Pila de llamadas y retorno", "Call stack and return", "Kaldstak og retur"),
            (
                "Cada llamada crea un marco con sus parámetros, variables locales y punto de retorno. Las llamadas se apilan hasta un caso base. Después la pila se desenrolla en orden inverso y cada marco combina el valor recibido. El trabajo antes del llamado ocurre al descender; el trabajo posterior ocurre al regresar. Un trazado debe mostrar ambos movimientos.",
                "Each call creates a frame with parameters, local variables, and a return point. Calls accumulate until a base case. The stack then unwinds in reverse order, and each frame combines the received value. Work before the call happens while descending; work after it happens while returning. A trace should show both movements.",
                "Hvert kald opretter en frame med parametre, lokale variable og returpunkt. Kald stables indtil et basistilfælde. Derefter afvikles stakken i omvendt rækkefølge, og hver frame kombinerer den modtagne værdi. Arbejde før kaldet sker på vej ned; arbejde efter kaldet sker på vej tilbage.",
            ),
            (
                (
                    "Los marcos locales son independientes.",
                    "Local frames are independent.",
                    "Lokale frames er uafhængige.",
                ),
                (
                    "El orden de retorno es LIFO.",
                    "Return order is LIFO.",
                    "Returrækkefølgen er LIFO.",
                ),
                (
                    "Descenso y desenrollado pueden producir órdenes distintos.",
                    "Descent and unwinding may produce different orders.",
                    "Nedstigning og afvikling kan give forskellige rækkefølger.",
                ),
            ),
        ),
        concept(
            "numeric-and-sequence-recursion",
            (
                "Recursión sobre números y secuencias",
                "Recursion over numbers and sequences",
                "Rekursion over tal og sekvenser",
            ),
            (
                "En problema numérico suele reducir n; una secuencia suele dividirse en cabeza y resto o en mitades. El slicing crea nuevas secuencias y puede añadir coste, por lo que un índice puede ser preferible. La combinación debe usar el retorno recursivo, no volver a calcular el subproblema. El dominio negativo o la secuencia vacía deben definirse explícitamente.",
                "A numeric problem often reduces n; a sequence is often split into head and rest or into halves. Slicing creates new sequences and may add cost, so an index can be preferable. Combination should use the recursive return rather than recomputing the subproblem. Negative domains and empty sequences must be defined explicitly.",
                "Et numerisk problem reducerer ofte n; en sekvens opdeles ofte i hoved og rest eller i halvdele. Slicing opretter nye sekvenser og kan tilføje omkostning, så et indeks kan være bedre. Kombinationen bør bruge den rekursive returværdi frem for at genberegne delproblemet. Negative domæner og tomme sekvenser skal defineres.",
            ),
            (
                (
                    "Cabeza y resto es un patrón conceptual.",
                    "Head and rest is a conceptual pattern.",
                    "Hoved og rest er et konceptuelt mønster.",
                ),
                (
                    "Slicing puede cambiar la complejidad.",
                    "Slicing may change complexity.",
                    "Slicing kan ændre kompleksiteten.",
                ),
                (
                    "El caso vacío define muchas reducciones.",
                    "The empty case defines many reductions.",
                    "Det tomme tilfælde definerer mange reduktioner.",
                ),
            ),
        ),
        concept(
            "nested-structures",
            ("Estructuras anidadas", "Nested structures", "Indlejrede strukturer"),
            (
                "Las estructuras anidadas tienen profundidad variable y no siempre caben en un número fijo de bucles. Una función puede distinguir entre elemento simple y contenedor: procesa directamente el primero y recorre recursivamente el segundo. Debe evitar tratar cadenas como contenedores genéricos cuando eso descompone caracteres sin intención y debe definir qué tipos son válidos.",
                "Nested structures have variable depth and do not always fit a fixed number of loops. A function may distinguish a simple element from a container: process the former directly and recursively traverse the latter. It should avoid treating strings as generic containers when that unintentionally decomposes characters and should define valid types.",
                "Indlejrede strukturer har variabel dybde og passer ikke altid til et fast antal løkker. En funktion kan skelne mellem et simpelt element og en container: behandl det første direkte og gennemløb det andet rekursivt. Strenge bør ikke behandles som generiske containere, hvis tegnopdeling ikke er tilsigtet.",
            ),
            (
                (
                    "La profundidad puede ser desconocida.",
                    "Depth may be unknown.",
                    "Dybden kan være ukendt.",
                ),
                (
                    "Define qué cuenta como contenedor.",
                    "Define what counts as a container.",
                    "Definér hvad der tæller som container.",
                ),
                (
                    "Cada hijo es un subproblema.",
                    "Each child is a subproblem.",
                    "Hvert barn er et delproblem.",
                ),
            ),
        ),
        concept(
            "recursion-versus-iteration",
            (
                "Recursión frente a iteración",
                "Recursion versus iteration",
                "Rekursion versus iteration",
            ),
            (
                "Muchos cálculos lineales admiten bucle y recursión. La versión iterativa mantiene estado explícito; la recursiva usa marcos de pila. La recursión puede reflejar mejor árboles y definiciones inductivas, pero en Python tiene sobrecarga y un límite de profundidad. No debe elegirse por brevedad, sino por claridad estructural, coste y restricciones de entrada.",
                "Many linear computations support both loops and recursion. The iterative version keeps explicit state; recursion uses stack frames. Recursion may better reflect trees and inductive definitions, but Python has call overhead and a depth limit. Choose it for structural clarity, cost, and input constraints rather than brevity.",
                "Mange lineære beregninger kan bruge både løkker og rekursion. Den iterative version holder eksplicit tilstand; rekursion bruger stack frames. Rekursion kan bedre afspejle træer og induktive definitioner, men Python har kaldeomkostning og dybdegrænse. Vælg efter strukturel klarhed, omkostning og inputbegrænsninger.",
            ),
            (
                (
                    "Iteración evita crecimiento de la pila.",
                    "Iteration avoids stack growth.",
                    "Iteration undgår vækst i stakken.",
                ),
                (
                    "Recursión puede reflejar una estructura recursiva.",
                    "Recursion may mirror a recursive structure.",
                    "Rekursion kan afspejle en rekursiv struktur.",
                ),
                (
                    "La equivalencia funcional no implica igual coste.",
                    "Functional equivalence does not imply equal cost.",
                    "Funktionel ækvivalens betyder ikke samme omkostning.",
                ),
            ),
        ),
        concept(
            "complexity-memoization-testing",
            (
                "Coste, memoización y pruebas",
                "Cost, memoization, and testing",
                "Omkostning, memoization og test",
            ),
            (
                "Una sola llamada recursiva sobre una entrada reducida suele producir profundidad lineal; varias llamadas pueden formar un árbol y repetir subproblemas. La memoización almacena resultados por entrada para evitar repetición cuando la función es pura y las claves son adecuadas. Las pruebas cubren casos base, un paso, varios pasos, entradas fuera del dominio, ramas distintas, profundidad y equivalencia con una versión iterativa de referencia.",
                "One recursive call on a reduced input often yields linear depth; multiple calls may form a tree and repeat subproblems. Memoization stores results by input to avoid repetition when the function is pure and keys are suitable. Tests cover base cases, one step, several steps, out-of-domain inputs, different branches, depth, and equivalence with an iterative reference.",
                "Ét rekursivt kald på reduceret input giver ofte lineær dybde; flere kald kan danne et træ og gentage delproblemer. Memoization gemmer resultater efter input for at undgå gentagelse, når funktionen er ren og nøglerne egnede. Test dækker basistilfælde, ét trin, flere trin, input uden for domænet, forskellige grene, dybde og ækvivalens med en iterativ reference.",
            ),
            (
                (
                    "Cuenta llamadas además de profundidad.",
                    "Count calls as well as depth.",
                    "Tæl kald såvel som dybde.",
                ),
                (
                    "Memoización requiere una clave estable.",
                    "Memoization requires a stable key.",
                    "Memoization kræver en stabil nøgle.",
                ),
                (
                    "Prueba el caso base de forma directa.",
                    "Test the base case directly.",
                    "Test basistilfældet direkte.",
                ),
            ),
        ),
    ),
    worked_examples=(
        example(
            "factorial",
            (
                "Factorial con dominio explícito",
                "Factorial with an explicit domain",
                "Fakultet med eksplicit domæne",
            ),
            (
                "Calcula n! para enteros no negativos.",
                "Compute n! for non-negative integers.",
                "Beregn n! for ikke-negative heltal.",
            ),
            (
                ("Rechazar negativos.", "Reject negatives.", "Afvis negative."),
                ("Usar 0 como caso base.", "Use 0 as the base case.", "Brug 0 som basistilfælde."),
                (
                    "Combinar n con factorial(n-1).",
                    "Combine n with factorial(n-1).",
                    "Kombinér n med factorial(n-1).",
                ),
            ),
            "def factorial(n):\n    if n < 0:\n        raise ValueError('n must be non-negative')\n    if n == 0:\n        return 1\n    return n * factorial(n - 1)\n\nprint(factorial(4))",
            "24",
            (
                "La medida n disminuye hasta cero.",
                "The measure n decreases to zero.",
                "Målet n falder til nul.",
            ),
        ),
        example(
            "sum-sequence",
            ("Suma recursiva por índice", "Recursive sum by index", "Rekursiv sum efter indeks"),
            (
                "Suma sin crear slices en cada llamada.",
                "Sum without creating slices on every call.",
                "Summér uden at oprette slices i hvert kald.",
            ),
            (
                (
                    "Usar el índice como progreso.",
                    "Use the index as progress.",
                    "Brug indeks som fremskridt.",
                ),
                ("Finalizar al alcanzar len.", "Stop at len.", "Stop ved len."),
                (
                    "Combinar elemento y resto.",
                    "Combine element and rest.",
                    "Kombinér element og rest.",
                ),
            ),
            "def recursive_sum(values, index=0):\n    if index == len(values):\n        return 0\n    return values[index] + recursive_sum(values, index + 1)\n\nprint(recursive_sum([2, 3, 4]))",
            "9",
            (
                "La distancia len(values)-index disminuye.",
                "The distance len(values)-index decreases.",
                "Afstanden len(values)-index falder.",
            ),
        ),
        example(
            "gcd",
            ("Máximo común divisor", "Greatest common divisor", "Største fælles divisor"),
            (
                "Aplica la reducción de Euclides.",
                "Apply Euclid's reduction.",
                "Anvend Euklids reduktion.",
            ),
            (
                ("Usar b==0 como base.", "Use b==0 as base.", "Brug b==0 som base."),
                (
                    "Reducir a gcd(b, a % b).",
                    "Reduce to gcd(b, a % b).",
                    "Reducer til gcd(b, a % b).",
                ),
            ),
            "def gcd(a, b):\n    if b == 0:\n        return abs(a)\n    return gcd(b, a % b)\n\nprint(gcd(48, 18))",
            "6",
            (
                "El segundo argumento disminuye bajo las precondiciones habituales.",
                "The second argument decreases under the usual preconditions.",
                "Det andet argument falder under de sædvanlige forudsætninger.",
            ),
        ),
        example(
            "flatten",
            (
                "Aplanar una estructura anidada",
                "Flatten a nested structure",
                "Udflad en indlejret struktur",
            ),
            (
                "Convierte listas anidadas de enteros en una lista plana.",
                "Convert nested integer lists into a flat list.",
                "Konvertér indlejrede heltalslister til en flad liste.",
            ),
            (
                (
                    "Un entero es caso simple.",
                    "An integer is a simple case.",
                    "Et heltal er et simpelt tilfælde.",
                ),
                (
                    "Una lista se descompone en hijos.",
                    "A list decomposes into children.",
                    "En liste dekomponeres i børn.",
                ),
                ("Concatenar los resultados.", "Concatenate results.", "Sammenkæd resultaterne."),
            ),
            "def flatten(node):\n    if isinstance(node, int):\n        return [node]\n    result = []\n    for child in node:\n        result.extend(flatten(child))\n    return result\n\nprint(flatten([1, [2, [3]], 4]))",
            "[1, 2, 3, 4]",
            (
                "Cada hijo es una estructura de la misma familia.",
                "Each child belongs to the same structure family.",
                "Hvert barn tilhører samme strukturfamilie.",
            ),
        ),
        example(
            "memoized-fibonacci",
            ("Fibonacci con memoización", "Memoized Fibonacci", "Fibonacci med memoization"),
            (
                "Evita recalcular subproblemas repetidos.",
                "Avoid recomputing repeated subproblems.",
                "Undgå genberegning af gentagne delproblemer.",
            ),
            (
                ("Definir bases 0 y 1.", "Define bases 0 and 1.", "Definér baser 0 og 1."),
                ("Consultar caché.", "Check cache.", "Kontrollér cache."),
                ("Guardar antes de retornar.", "Store before returning.", "Gem før retur."),
            ),
            "def fib(n, cache=None):\n    if cache is None:\n        cache = {}\n    if n < 2:\n        return n\n    if n not in cache:\n        cache[n] = fib(n - 1, cache) + fib(n - 2, cache)\n    return cache[n]\n\nprint(fib(8))",
            "21",
            (
                "La caché convierte subproblemas repetidos en consultas.",
                "The cache turns repeated subproblems into lookups.",
                "Cachen omdanner gentagne delproblemer til opslag.",
            ),
        ),
    ),
    practice_exercises=(
        practice(
            "m09.p01",
            ActivityType.CODE_TRACING,
            (
                "Traza factorial(3) mostrando descenso y retornos.",
                "Trace factorial(3), showing descent and returns.",
                "Gennemgå factorial(3) med nedstigning og retur.",
            ),
            (("Desciende 3,2,1,0.", "Descend through 3,2,1,0.", "Gå ned gennem 3,2,1,0."),),
            (
                "factorial(0)=1; factorial(1)=1; factorial(2)=2; factorial(3)=6.",
                "factorial(0)=1; factorial(1)=1; factorial(2)=2; factorial(3)=6.",
                "factorial(0)=1; factorial(1)=1; factorial(2)=2; factorial(3)=6.",
            ),
            (
                "Los productos ocurren al desenrollar.",
                "Products occur while unwinding.",
                "Produkterne beregnes under afvikling.",
            ),
        ),
        practice(
            "m09.p02",
            ActivityType.FILL_IN_THE_BLANK,
            (
                "Completa el caso base de suma: if index == len(values): return ____.",
                "Complete the sum base case: if index == len(values): return ____.",
                "Udfyld sum-basistilfældet: if index == len(values): return ____.",
            ),
            (
                (
                    "Necesitas la identidad aditiva.",
                    "You need the additive identity.",
                    "Du behøver den additive identitet.",
                ),
            ),
            ("0", "0", "0"),
            (
                "Cero no altera la suma durante el retorno.",
                "Zero does not alter the sum during return.",
                "Nul ændrer ikke summen under retur.",
            ),
        ),
        practice(
            "m09.p03",
            ActivityType.DEBUGGING,
            (
                "Corrige countdown(n) que llama countdown(n+1).",
                "Fix countdown(n) that calls countdown(n+1).",
                "Ret countdown(n), der kalder countdown(n+1).",
            ),
            (
                (
                    "La medida debe acercarse a cero.",
                    "The measure must approach zero.",
                    "Målet skal nærme sig nul.",
                ),
            ),
            (
                "Llamar countdown(n - 1) y definir el comportamiento para n <= 0.",
                "Call countdown(n - 1) and define behavior for n <= 0.",
                "Kald countdown(n - 1) og definér adfærd for n <= 0.",
            ),
            ("n+1 rompe el progreso.", "n+1 breaks progress.", "n+1 bryder fremskridtet."),
        ),
        practice(
            "m09.p04",
            ActivityType.CODE_COMPLETION,
            (
                "Escribe recursive_length(values, index=0).",
                "Write recursive_length(values, index=0).",
                "Skriv recursive_length(values, index=0).",
            ),
            (
                (
                    "La base ocurre al alcanzar len.",
                    "The base occurs at len.",
                    "Basen opstår ved len.",
                ),
            ),
            (
                "def recursive_length(values, index=0):\n    if index == len(values):\n        return 0\n    return 1 + recursive_length(values, index + 1)",
                "def recursive_length(values, index=0):\n    if index == len(values):\n        return 0\n    return 1 + recursive_length(values, index + 1)",
                "def recursive_length(values, index=0):\n    if index == len(values):\n        return 0\n    return 1 + recursive_length(values, index + 1)",
            ),
            (
                "Cada marco aporta uno.",
                "Each frame contributes one.",
                "Hver frame bidrager med én.",
            ),
            "def recursive_length(values, index=0):\n    pass",
        ),
        practice(
            "m09.p05",
            ActivityType.ORDERING,
            (
                "Ordena: comprobar base, reducir, llamar, combinar, retornar.",
                "Order: check base, reduce, call, combine, return.",
                "Ordén: kontrollér base, reducer, kald, kombinér, returnér.",
            ),
            (
                (
                    "El caso base se comprueba antes de otra llamada.",
                    "The base case is checked before another call.",
                    "Basistilfældet kontrolleres før et nyt kald.",
                ),
            ),
            (
                "Comprobar base → reducir → llamar → combinar → retornar.",
                "Check base → reduce → call → combine → return.",
                "Kontrollér base → reducer → kald → kombinér → returnér.",
            ),
            (
                "La secuencia expresa el contrato recursivo.",
                "The sequence expresses the recursive contract.",
                "Sekvensen udtrykker den rekursive kontrakt.",
            ),
        ),
        practice(
            "m09.p06",
            ActivityType.SHORT_ANSWER,
            (
                "Explica por qué un caso base correcto puede seguir siendo inalcanzable.",
                "Explain why a correct base case may still be unreachable.",
                "Forklar, hvorfor et korrekt basistilfælde stadig kan være uopnåeligt.",
            ),
            (
                (
                    "Observa la transformación del argumento.",
                    "Inspect argument transformation.",
                    "Undersøg argumentets transformation.",
                ),
            ),
            (
                "La llamada recursiva puede mantener o alejar la medida, por lo que nunca produce la entrada del caso base.",
                "The recursive call may preserve or increase the measure, so it never produces the base-case input.",
                "Det rekursive kald kan bevare eller øge målet og producerer derfor aldrig basistilfældets input.",
            ),
            (
                "Base y progreso son obligaciones separadas.",
                "Base and progress are separate obligations.",
                "Base og fremskridt er separate forpligtelser.",
            ),
        ),
        practice(
            "m09.p07",
            ActivityType.CODE_TRACING,
            (
                "Indica el orden de print antes y después de recurse(n-1).",
                "State print order before and after recurse(n-1).",
                "Angiv print-rækkefølgen før og efter recurse(n-1).",
            ),
            (
                (
                    "Antes ocurre al descender; después al regresar.",
                    "Before happens on descent; after on return.",
                    "Før sker på nedstigning; efter på retur.",
                ),
            ),
            (
                "Los mensajes previos aparecen de n a base; los posteriores de base a n.",
                "Pre-call messages appear from n to base; post-call messages from base to n.",
                "Beskeder før kald vises fra n til base; efter-kald fra base til n.",
            ),
            (
                "La pila invierte el orden de retorno.",
                "The stack reverses return order.",
                "Stakken vender returrækkefølgen.",
            ),
        ),
        practice(
            "m09.p08",
            ActivityType.DEBUGGING,
            (
                "Corrige fibonacci recursivo que recalcula subproblemas sin límite práctico.",
                "Fix recursive Fibonacci that repeatedly recomputes subproblems.",
                "Ret rekursiv Fibonacci, der gentager delproblemer uden praktisk grænse.",
            ),
            (
                (
                    "Guarda resultados por n o usa iteración.",
                    "Store results by n or use iteration.",
                    "Gem resultater efter n eller brug iteration.",
                ),
            ),
            (
                "Añadir memoización con una caché compartida por la llamada superior o reemplazar por un bucle.",
                "Add memoization with a cache shared by the top-level call or replace it with a loop.",
                "Tilføj memoization med en cache delt af topkaldet eller erstat med en løkke.",
            ),
            (
                "Dos ramas crean un árbol de llamadas repetidas.",
                "Two branches create a tree of repeated calls.",
                "To grene skaber et træ af gentagne kald.",
            ),
        ),
        practice(
            "m09.p09",
            ActivityType.DATA_INTERPRETATION,
            (
                "Interpreta RecursionError para una lista muy larga.",
                "Interpret RecursionError for a very long list.",
                "Fortolk RecursionError for en meget lang liste.",
            ),
            (
                (
                    "Python limita la profundidad de la pila.",
                    "Python limits stack depth.",
                    "Python begrænser stakdybden.",
                ),
            ),
            (
                "La estructura lineal produjo más marcos de los permitidos; una solución iterativa es más adecuada para esa escala.",
                "The linear structure produced more frames than allowed; an iterative solution is more suitable at that scale.",
                "Den lineære struktur producerede flere frames end tilladt; en iterativ løsning er mere passende i den skala.",
            ),
            (
                "No implica necesariamente que el caso base sea incorrecto.",
                "It does not necessarily mean the base case is wrong.",
                "Det betyder ikke nødvendigvis, at basistilfældet er forkert.",
            ),
        ),
        practice(
            "m09.p10",
            ActivityType.PIPELINE_DESIGN,
            (
                "Diseña un proceso recursivo para validar una estructura anidada.",
                "Design a recursive process to validate a nested structure.",
                "Design en rekursiv proces til validering af en indlejret struktur.",
            ),
            (
                (
                    "Distingue hoja y contenedor.",
                    "Distinguish leaf and container.",
                    "Skeln mellem blad og container.",
                ),
            ),
            (
                "Si es hoja, validar valor; si es contenedor válido, validar cada hijo; si es otro tipo, producir error con la ruta estructural.",
                "If it is a leaf, validate the value; if it is a valid container, validate every child; otherwise raise an error with the structural path.",
                "Hvis det er et blad, validér værdien; hvis det er en gyldig container, validér hvert barn; ellers giv en fejl med den strukturelle sti.",
            ),
            (
                "La ruta permite localizar una hoja inválida.",
                "The path locates an invalid leaf.",
                "Stien lokaliserer et ugyldigt blad.",
            ),
        ),
        practice(
            "m09.p11",
            ActivityType.ORAL_EXPLANATION,
            (
                "Compara suma recursiva e iterativa en Python.",
                "Compare recursive and iterative sum in Python.",
                "Sammenlign rekursiv og iterativ sum i Python.",
            ),
            (
                (
                    "Considera claridad, pila y escala.",
                    "Consider clarity, stack, and scale.",
                    "Overvej klarhed, stak og skala.",
                ),
            ),
            (
                "Ambas pueden producir el mismo resultado; el bucle evita marcos y soporta secuencias largas, mientras la recursión ilustra la definición inductiva pero tiene sobrecarga y límite de profundidad.",
                "Both may produce the same result; the loop avoids frames and supports long sequences, while recursion illustrates the inductive definition but has overhead and a depth limit.",
                "Begge kan give samme resultat; løkken undgår frames og understøtter lange sekvenser, mens rekursion viser den induktive definition men har overhead og dybdegrænse.",
            ),
            (
                "La elección depende de estructura y restricciones.",
                "Choice depends on structure and constraints.",
                "Valget afhænger af struktur og begrænsninger.",
            ),
        ),
        practice(
            "m09.p12",
            ActivityType.CODE_COMPLETION,
            (
                "Completa el paso de Euclides: return gcd(b, ____).",
                "Complete Euclid's step: return gcd(b, ____).",
                "Udfyld Euklids trin: return gcd(b, ____).",
            ),
            (
                (
                    "Usa el resto de a entre b.",
                    "Use the remainder of a divided by b.",
                    "Brug resten af a divideret med b.",
                ),
            ),
            ("a % b", "a % b", "a % b"),
            (
                "El resto reduce el segundo argumento.",
                "The remainder reduces the second argument.",
                "Resten reducerer det andet argument.",
            ),
        ),
    ),
    assessment_items=(
        authored_item(
            "dm857.m09.assessment.001",
            ActivityType.CODE_TRACING,
            (
                "Traza sum_to(3) = 3 + sum_to(2), con base cero.",
                "Trace sum_to(3) = 3 + sum_to(2), with zero base.",
                "Gennemgå sum_to(3) = 3 + sum_to(2), med nul som base.",
            ),
            (
                (
                    "sum_to(0)=0; luego 1, 3 y 6.",
                    "sum_to(0)=0; then 1, 3, and 6.",
                    "sum_to(0)=0; derefter 1, 3 og 6.",
                ),
            ),
            (
                "La suma se reconstruye al desenrollar.",
                "The sum is reconstructed while unwinding.",
                "Summen rekonstrueres under afvikling.",
            ),
        ),
        authored_item(
            "dm857.m09.assessment.002",
            ActivityType.MULTIPLE_SELECT,
            (
                "Selecciona obligaciones de terminación.",
                "Select termination obligations.",
                "Vælg termineringsforpligtelser.",
            ),
            (),
            (
                "Caso base alcanzable, medida bien fundada y reducción en cada rama.",
                "Reachable base case, well-founded measure, and reduction in every branch.",
                "Opnåeligt basistilfælde, velfunderet mål og reduktion i hver gren.",
            ),
            options=(
                (
                    "base",
                    ("Caso base alcanzable", "Reachable base case", "Opnåeligt basistilfælde"),
                ),
                ("measure", ("Medida bien fundada", "Well-founded measure", "Velfunderet mål")),
                (
                    "decrease",
                    (
                        "Reducción en cada rama",
                        "Reduction in every branch",
                        "Reduktion i hver gren",
                    ),
                ),
                ("print", ("Al menos un print", "At least one print", "Mindst ét print")),
            ),
            correct_option_ids=("base", "measure", "decrease"),
        ),
        authored_item(
            "dm857.m09.assessment.003",
            ActivityType.DEBUGGING,
            (
                "Corrige recursive_sum(values) que llama con values sin cambiar.",
                "Fix recursive_sum(values) that calls itself with unchanged values.",
                "Ret recursive_sum(values), der kalder sig selv med uændrede values.",
            ),
            (
                (
                    "Reducir mediante índice+1 o resto y definir el caso vacío.",
                    "Reduce through index+1 or the rest and define the empty case.",
                    "Reducer via indeks+1 eller resten og definér det tomme tilfælde.",
                ),
            ),
            (
                "La entrada sin cambios no progresa.",
                "Unchanged input makes no progress.",
                "Uændret input giver intet fremskridt.",
            ),
        ),
        authored_item(
            "dm857.m09.assessment.004",
            ActivityType.FILL_IN_THE_BLANK,
            (
                "Completa la identidad multiplicativa de factorial: factorial(0) = ____.",
                "Complete factorial's multiplicative identity: factorial(0) = ____.",
                "Udfyld fakultets multiplikative identitet: factorial(0) = ____.",
            ),
            (("1", "1", "1"),),
            (
                "Uno permite reconstruir productos.",
                "One supports product reconstruction.",
                "Én muliggør rekonstruktion af produkter.",
            ),
        ),
        authored_item(
            "dm857.m09.assessment.005",
            ActivityType.MATCHING,
            ("Relaciona concepto y función.", "Match concept and role.", "Match begreb og rolle."),
            (),
            (
                "Base-detiene; medida-demuestra progreso; marco-guarda locales; memo-evita repetición.",
                "Base-stops; measure-shows progress; frame-stores locals; memo-avoids repetition.",
                "Base-stopper; mål-viser fremskridt; frame-gemmer lokale; memo-undgår gentagelse.",
            ),
            options=(
                ("base", ("Base → detiene", "Base → stops", "Base → stopper")),
                ("measure", ("Medida → progreso", "Measure → progress", "Mål → fremskridt")),
                (
                    "frame",
                    (
                        "Marco → variables locales",
                        "Frame → local variables",
                        "Frame → lokale variable",
                    ),
                ),
                (
                    "memo",
                    (
                        "Memoización → evita repetición",
                        "Memoization → avoids repetition",
                        "Memoization → undgår gentagelse",
                    ),
                ),
            ),
            correct_option_ids=("base", "measure", "frame", "memo"),
        ),
        authored_item(
            "dm857.m09.assessment.006",
            ActivityType.ORDERING,
            (
                "Ordena el comportamiento de una llamada recursiva.",
                "Order recursive-call behavior.",
                "Ordén adfærden i et rekursivt kald.",
            ),
            (),
            (
                "Crear marco → comprobar base → reducir → llamar → combinar → retornar.",
                "Create frame → check base → reduce → call → combine → return.",
                "Opret frame → kontrollér base → reducer → kald → kombinér → returnér.",
            ),
            options=(
                ("frame", ("Crear marco", "Create frame", "Opret frame")),
                ("base", ("Comprobar base", "Check base", "Kontrollér base")),
                ("reduce", ("Reducir", "Reduce", "Reducer")),
                ("call", ("Llamar", "Call", "Kald")),
                ("combine", ("Combinar", "Combine", "Kombinér")),
                ("return", ("Retornar", "Return", "Returnér")),
            ),
            correct_option_ids=("frame", "base", "reduce", "call", "combine", "return"),
        ),
        authored_item(
            "dm857.m09.assessment.007",
            ActivityType.CODE_COMPLETION,
            (
                "Escribe contains(values, target, index=0) recursivo.",
                "Write recursive contains(values, target, index=0).",
                "Skriv rekursiv contains(values, target, index=0).",
            ),
            (
                (
                    "def contains(values, target, index=0):\n    if index == len(values):\n        return False\n    if values[index] == target:\n        return True\n    return contains(values, target, index + 1)",
                    "def contains(values, target, index=0):\n    if index == len(values):\n        return False\n    if values[index] == target:\n        return True\n    return contains(values, target, index + 1)",
                    "def contains(values, target, index=0):\n    if index == len(values):\n        return False\n    if values[index] == target:\n        return True\n    return contains(values, target, index + 1)",
                ),
            ),
            (
                "La función tiene bases para agotamiento y coincidencia.",
                "The function has bases for exhaustion and match.",
                "Funktionen har baser for udtømning og match.",
            ),
            rubric=(
                (
                    "Reduce la distancia al final.",
                    "Reduces distance to the end.",
                    "Reducerer afstanden til slutningen.",
                ),
            ),
        ),
        authored_item(
            "dm857.m09.assessment.008",
            ActivityType.SHORT_ANSWER,
            (
                "Distingue caso base y medida de progreso.",
                "Distinguish base case and progress measure.",
                "Skeln mellem basistilfælde og fremskridtsmål.",
            ),
            (
                (
                    "El caso base resuelve una instancia mínima; la medida demuestra que las llamadas se acercan a esa instancia.",
                    "The base case solves a minimal instance; the measure shows calls approach that instance.",
                    "Basistilfældet løser en minimal instans; målet viser at kaldene nærmer sig den.",
                ),
            ),
            (
                "Ambos son necesarios para justificar terminación.",
                "Both are needed to justify termination.",
                "Begge er nødvendige for at begrunde terminering.",
            ),
        ),
        authored_item(
            "dm857.m09.assessment.009",
            ActivityType.DATA_INTERPRETATION,
            (
                "Interpreta un crecimiento de llamadas cercano a 2^n.",
                "Interpret call growth near 2^n.",
                "Fortolk vækst i kald tæt på 2^n.",
            ),
            (
                (
                    "Varias ramas recalculan subproblemas; memoización o una formulación iterativa puede reducir el coste.",
                    "Multiple branches recompute subproblems; memoization or an iterative formulation may reduce cost.",
                    "Flere grene genberegner delproblemer; memoization eller en iterativ formulering kan reducere omkostningen.",
                ),
            ),
            (
                "La profundidad y el número total de llamadas son medidas distintas.",
                "Depth and total call count are distinct measures.",
                "Dybde og samlet antal kald er forskellige mål.",
            ),
        ),
        authored_item(
            "dm857.m09.assessment.010",
            ActivityType.ORAL_EXPLANATION,
            (
                "Explica el desenrollado de la pila.",
                "Explain stack unwinding.",
                "Forklar afvikling af stakken.",
            ),
            (
                (
                    "Tras el caso base, cada marco suspendido recibe un retorno, ejecuta su combinación pendiente y retorna al marco anterior en orden LIFO.",
                    "After the base case, each suspended frame receives a return, performs its pending combination, and returns to the previous frame in LIFO order.",
                    "Efter basistilfældet modtager hver suspenderet frame en returværdi, udfører sin ventende kombination og returnerer til den forrige frame i LIFO-rækkefølge.",
                ),
            ),
            (
                "El retorno no ocurre simultáneamente en todos los marcos.",
                "Return does not occur simultaneously in all frames.",
                "Retur sker ikke samtidigt i alle frames.",
            ),
        ),
        authored_item(
            "dm857.m09.assessment.011",
            ActivityType.PIPELINE_DESIGN,
            (
                "Diseña un recorrido recursivo de nodos anidados.",
                "Design a recursive traversal of nested nodes.",
                "Design et rekursivt gennemløb af indlejrede noder.",
            ),
            (
                (
                    "Validar tipo → resolver hoja o recorrer hijos → combinar resultados → preservar ruta de error.",
                    "Validate type → solve leaf or traverse children → combine results → preserve error path.",
                    "Validér type → løs blad eller gennemløb børn → kombinér resultater → bevar fejlsti.",
                ),
            ),
            (
                "La forma variable motiva la descomposición recursiva.",
                "Variable shape motivates recursive decomposition.",
                "Variabel form motiverer rekursiv dekomponering.",
            ),
            rubric=(
                (
                    "Define hojas y contenedores válidos.",
                    "Defines valid leaves and containers.",
                    "Definerer gyldige blade og containere.",
                ),
            ),
        ),
        authored_item(
            "dm857.m09.assessment.012",
            ActivityType.DEBUGGING,
            (
                "Corrige fib(n, cache={}) como valor predeterminado mutable.",
                "Fix fib(n, cache={}) as a mutable default.",
                "Ret fib(n, cache={}) som muterbar standardværdi.",
            ),
            (
                (
                    "Usar cache=None y crear un diccionario dentro de la llamada superior.",
                    "Use cache=None and create a dictionary inside the top-level call.",
                    "Brug cache=None og opret en ordbog inde i topkaldet.",
                ),
            ),
            (
                "El diccionario predeterminado se compartiría entre llamadas independientes.",
                "The default dictionary would be shared across independent calls.",
                "Standardordbogen ville blive delt mellem uafhængige kald.",
            ),
        ),
        authored_item(
            "dm857.m09.assessment.013",
            ActivityType.CODE_TRACING,
            ("Traza gcd(20, 8).", "Trace gcd(20, 8).", "Gennemgå gcd(20, 8)."),
            (
                (
                    "gcd(20,8) → gcd(8,4) → gcd(4,0) → 4.",
                    "gcd(20,8) → gcd(8,4) → gcd(4,0) → 4.",
                    "gcd(20,8) → gcd(8,4) → gcd(4,0) → 4.",
                ),
            ),
            (
                "El resto reduce el problema.",
                "The remainder reduces the problem.",
                "Resten reducerer problemet.",
            ),
        ),
        authored_item(
            "dm857.m09.assessment.014",
            ActivityType.SHORT_ANSWER,
            (
                "Justifica cuándo preferir iteración en Python.",
                "Justify when to prefer iteration in Python.",
                "Begrund, hvornår iteration bør foretrækkes i Python.",
            ),
            (
                (
                    "Cuando el problema es lineal, la entrada puede ser muy profunda o el crecimiento de pila y la sobrecarga no aportan claridad estructural.",
                    "When the problem is linear, input may be very deep, or stack growth and overhead add no structural clarity.",
                    "Når problemet er lineært, input kan være meget dybt, eller stakvækst og overhead ikke giver strukturel klarhed.",
                ),
            ),
            (
                "La elección debe considerar escala y legibilidad.",
                "Choice should consider scale and readability.",
                "Valget bør tage højde for skala og læsbarhed.",
            ),
        ),
    ),
    tutor_support=tutor_support(
        (
            "La recursión resuelve una instancia mediante instancias más pequeñas de la misma forma. Un contrato recursivo define el dominio, los casos base y cómo combinar retornos. El caso base resuelve directamente una instancia mínima y debe ser correcto, completo y alcanzable. La terminación requiere una medida bien fundada que disminuya en cada rama, como n, la longitud restante o la profundidad estructural. Cada llamada crea un marco con parámetros y variables locales; los marcos se apilan al descender y se desenrollan en orden inverso después del caso base. El trabajo antes del llamado ocurre en descenso y el trabajo posterior ocurre al retorno. En secuencias, cabeza-resto es un patrón conceptual, pero slicing puede añadir coste y un índice puede ser preferible. Las estructuras anidadas de profundidad variable se procesan distinguiendo hojas y contenedores. Muchas funciones lineales tienen una versión iterativa que evita crecimiento de pila; Python impone un límite de recursión y no optimiza tail recursion. Varias ramas pueden repetir subproblemas y producir crecimiento exponencial; la memoización almacena resultados cuando la función y las claves lo permiten. Las pruebas cubren cada caso base, uno y varios pasos, ramas, entradas fuera del dominio, profundidad, número de llamadas y equivalencia iterativa. Los ejemplos biomédicos son escenarios didácticos de programación y no representan protocolos, algoritmos clínicos ni recomendaciones de laboratorio.",
            "Recursion solves an instance through smaller instances of the same form. A recursive contract defines the domain, base cases, and how returns are combined. A base case directly solves a minimal instance and must be correct, complete, and reachable. Termination requires a well-founded measure that decreases in every branch, such as n, remaining length, or structural depth. Each call creates a frame with parameters and local variables; frames stack during descent and unwind in reverse order after the base case. Work before the call occurs on descent, and work after it occurs on return. For sequences, head-rest is a conceptual pattern, but slicing may add cost and an index may be preferable. Variable-depth nested structures are processed by distinguishing leaves and containers. Many linear functions have an iterative version that avoids stack growth; Python imposes a recursion limit and does not optimize tail recursion. Multiple branches may repeat subproblems and yield exponential growth; memoization stores results when the function and keys allow it. Tests cover every base case, one and several steps, branches, out-of-domain inputs, depth, call count, and iterative equivalence. Biomedical examples are programming exercises, not protocols, clinical algorithms, or laboratory recommendations.",
            "Rekursion løser en instans gennem mindre instanser af samme form. En rekursiv kontrakt definerer domænet, basistilfælde og kombination af returværdier. Et basistilfælde løser direkte en minimal instans og skal være korrekt, komplet og opnåeligt. Terminering kræver et velfunderet mål, der falder i hver gren, såsom n, resterende længde eller strukturel dybde. Hvert kald opretter en frame med parametre og lokale variable; frames stables under nedstigning og afvikles i omvendt rækkefølge efter basistilfældet. Ved sekvenser er hoved-rest et konceptuelt mønster, men slicing kan tilføje omkostning. Strukturer med variabel dybde behandles ved at skelne blade og containere. Mange lineære funktioner har en iterativ version, som undgår stakvækst; Python har en rekursionsgrænse og optimerer ikke tail recursion. Flere grene kan gentage delproblemer; memoization gemmer resultater. Biomedicinske eksempler er programmeringsøvelser, ikke protokoller, kliniske algoritmer eller laboratorieanbefalinger.",
        ),
        tuple(
            (es, en, da)
            for es, en, da in (
                (
                    "Recursión requiere subproblemas de la misma forma.",
                    "Recursion requires subproblems of the same form.",
                    "Rekursion kræver delproblemer af samme form.",
                ),
                (
                    "Los casos base resuelven instancias mínimas.",
                    "Base cases solve minimal instances.",
                    "Basistilfælde løser minimale instanser.",
                ),
                (
                    "El caso base debe ser alcanzable.",
                    "The base case must be reachable.",
                    "Basistilfældet skal kunne nås.",
                ),
                (
                    "Cada rama debe reducir una medida.",
                    "Every branch must reduce a measure.",
                    "Hver gren skal reducere et mål.",
                ),
                (
                    "Cada llamada crea un marco.",
                    "Each call creates a frame.",
                    "Hvert kald opretter en frame.",
                ),
                (
                    "La pila retorna en orden LIFO.",
                    "The stack returns in LIFO order.",
                    "Stakken returnerer i LIFO-rækkefølge.",
                ),
                (
                    "El trabajo posterior ocurre al desenrollar.",
                    "Post-call work occurs while unwinding.",
                    "Arbejde efter kald sker under afvikling.",
                ),
                (
                    "El caso vacío es central en secuencias.",
                    "The empty case is central for sequences.",
                    "Det tomme tilfælde er centralt for sekvenser.",
                ),
                (
                    "Slicing puede añadir coste.",
                    "Slicing may add cost.",
                    "Slicing kan tilføje omkostning.",
                ),
                (
                    "La recursión refleja estructuras anidadas.",
                    "Recursion mirrors nested structures.",
                    "Rekursion afspejler indlejrede strukturer.",
                ),
                (
                    "Iteración evita crecimiento de pila.",
                    "Iteration avoids stack growth.",
                    "Iteration undgår stakvækst.",
                ),
                (
                    "Python limita profundidad recursiva.",
                    "Python limits recursion depth.",
                    "Python begrænser rekursionsdybde.",
                ),
                (
                    "Varias ramas pueden repetir subproblemas.",
                    "Multiple branches may repeat subproblems.",
                    "Flere grene kan gentage delproblemer.",
                ),
                (
                    "Memoización reutiliza resultados.",
                    "Memoization reuses results.",
                    "Memoization genbruger resultater.",
                ),
            )
        ),
        tuple(
            (es, en, da)
            for es, en, da in (
                (
                    "Confundir recursión con repetición sin estructura.",
                    "Confusing recursion with unstructured repetition.",
                    "At forveksle rekursion med ustruktureret gentagelse.",
                ),
                ("Omitir el caso base.", "Omitting the base case.", "At udelade basistilfældet."),
                (
                    "Crear un caso base inalcanzable.",
                    "Creating an unreachable base case.",
                    "At skabe et uopnåeligt basistilfælde.",
                ),
                ("Pasar la misma entrada.", "Passing the same input.", "At sende samme input."),
                (
                    "Aumentar la medida por error.",
                    "Increasing the measure by mistake.",
                    "At øge målet ved en fejl.",
                ),
                (
                    "Mezclar variables de distintos marcos.",
                    "Mixing variables from different frames.",
                    "At blande variable fra forskellige frames.",
                ),
                (
                    "Olvidar combinar el retorno.",
                    "Forgetting to combine the return.",
                    "At glemme at kombinere returværdien.",
                ),
                (
                    "Confundir orden de descenso y retorno.",
                    "Confusing descent and return order.",
                    "At forveksle nedstignings- og returrækkefølge.",
                ),
                (
                    "Usar slicing sin considerar coste.",
                    "Using slicing without considering cost.",
                    "At bruge slicing uden at overveje omkostning.",
                ),
                (
                    "Tratar cadenas como contenedores genéricos sin intención.",
                    "Treating strings as generic containers unintentionally.",
                    "At behandle strenge som generiske containere utilsigtet.",
                ),
                (
                    "Suponer que Python optimiza tail recursion.",
                    "Assuming Python optimizes tail recursion.",
                    "At antage at Python optimerer tail recursion.",
                ),
                (
                    "Memoizar con un predeterminado mutable compartido.",
                    "Memoizing with a shared mutable default.",
                    "At memoize med en delt muterbar standard.",
                ),
            )
        ),
        tuple(
            (es, en, da)
            for es, en, da in (
                ("¿Cuál es el subproblema?", "What is the subproblem?", "Hvad er delproblemet?"),
                (
                    "¿Cuál es el dominio válido?",
                    "What is the valid domain?",
                    "Hvad er det gyldige domæne?",
                ),
                (
                    "¿Qué casos base se necesitan?",
                    "Which base cases are needed?",
                    "Hvilke basistilfælde behøves?",
                ),
                ("¿Son alcanzables?", "Are they reachable?", "Kan de nås?"),
                (
                    "¿Cuál es la medida de progreso?",
                    "What is the progress measure?",
                    "Hvad er fremskridtsmålet?",
                ),
                (
                    "¿Disminuye en cada rama?",
                    "Does it decrease in every branch?",
                    "Falder det i hver gren?",
                ),
                (
                    "¿Qué guarda cada marco?",
                    "What does each frame store?",
                    "Hvad gemmer hver frame?",
                ),
                (
                    "¿Qué ocurre al desenrollar?",
                    "What happens while unwinding?",
                    "Hvad sker under afvikling?",
                ),
                (
                    "¿El slicing añade coste?",
                    "Does slicing add cost?",
                    "Tilføjer slicing omkostning?",
                ),
                (
                    "¿La profundidad de entrada está acotada?",
                    "Is input depth bounded?",
                    "Er inputdybden begrænset?",
                ),
                (
                    "¿Se repiten subproblemas?",
                    "Are subproblems repeated?",
                    "Gentages delproblemer?",
                ),
                (
                    "¿Sería más clara una versión iterativa?",
                    "Would an iterative version be clearer?",
                    "Ville en iterativ version være klarere?",
                ),
            )
        ),
        tuple(
            (es, en, da)
            for es, en, da in (
                (
                    "Define un contrato recursivo preciso.",
                    "Defines a precise recursive contract.",
                    "Definerer en præcis rekursiv kontrakt.",
                ),
                (
                    "Diseña casos base correctos.",
                    "Designs correct base cases.",
                    "Designer korrekte basistilfælde.",
                ),
                ("Justifica terminación.", "Justifies termination.", "Begrunder terminering."),
                (
                    "Traza marcos y retornos.",
                    "Traces frames and returns.",
                    "Gennemgår frames og returværdier.",
                ),
                (
                    "Combina el retorno correctamente.",
                    "Combines return values correctly.",
                    "Kombinerer returværdier korrekt.",
                ),
                (
                    "Procesa secuencias sin coste oculto innecesario.",
                    "Processes sequences without unnecessary hidden cost.",
                    "Behandler sekvenser uden unødvendig skjult omkostning.",
                ),
                (
                    "Maneja estructuras anidadas.",
                    "Handles nested structures.",
                    "Håndterer indlejrede strukturer.",
                ),
                (
                    "Compara recursión e iteración.",
                    "Compares recursion and iteration.",
                    "Sammenligner rekursion og iteration.",
                ),
                (
                    "Detecta subproblemas repetidos.",
                    "Detects repeated subproblems.",
                    "Opdager gentagne delproblemer.",
                ),
                (
                    "Prueba bases, ramas y límites.",
                    "Tests bases, branches, and limits.",
                    "Tester baser, grene og grænser.",
                ),
            )
        ),
        tuple(
            (es, en, da)
            for es, en, da in (
                ("Dar primero una pista.", "Give a hint first.", "Giv først et hint."),
                (
                    "Pedir caso base y medida antes de mostrar código.",
                    "Ask for base case and measure before showing code.",
                    "Bed om basistilfælde og mål før kode vises.",
                ),
                (
                    "Mostrar descenso y desenrollado por separado.",
                    "Show descent and unwinding separately.",
                    "Vis nedstigning og afvikling separat.",
                ),
                (
                    "No afirmar que los marcos comparten locales.",
                    "Do not claim frames share locals.",
                    "Påstå ikke at frames deler lokale variable.",
                ),
                (
                    "Advertir el coste de slicing.",
                    "Warn about slicing cost.",
                    "Advar om slicing-omkostning.",
                ),
                (
                    "Advertir el límite de profundidad de Python.",
                    "Warn about Python's depth limit.",
                    "Advar om Pythons dybdegrænse.",
                ),
                (
                    "No asumir optimización de tail recursion.",
                    "Do not assume tail-recursion optimization.",
                    "Antag ikke optimering af tail recursion.",
                ),
                (
                    "No presentar ejemplos didácticos como protocolos.",
                    "Do not present teaching examples as protocols.",
                    "Præsenter ikke undervisningseksempler som protokoller.",
                ),
                (
                    "Relacionar memoización con subproblemas repetidos.",
                    "Relate memoization to repeated subproblems.",
                    "Knyt memoization til gentagne delproblemer.",
                ),
            )
        ),
        (
            "Official DM857 course description, SDU, active version approved in 2025.",
            "Think Python, third edition, chapter on recursion and recursive data.",
            "Introduction to Computation and Programming Using Python, third edition, sections on recursion, complexity, and testing.",
        ),
    ),
)

_BANK_09_MCQ = (
    (
        "001",
        (
            "¿Qué resuelve un caso base?",
            "What does a base case solve?",
            "Hvad løser et basistilfælde?",
        ),
        (
            ("minimal", ("Una instancia mínima", "A minimal instance", "En minimal instans")),
            ("largest", ("La instancia más grande", "The largest instance", "Den største instans")),
            ("random", ("Una instancia aleatoria", "A random instance", "En tilfældig instans")),
            ("none", ("Ninguna", "None", "Ingen")),
        ),
        "minimal",
        (
            "La base no necesita más descomposición.",
            "The base needs no further decomposition.",
            "Basen behøver ingen yderligere dekomponering.",
        ),
    ),
    (
        "003",
        (
            "¿Qué demuestra terminación?",
            "What demonstrates termination?",
            "Hvad demonstrerer terminering?",
        ),
        (
            ("measure", ("Una medida que disminuye", "A decreasing measure", "Et faldende mål")),
            ("print", ("Un print", "A print", "Et print")),
            ("name", ("El nombre de la función", "The function name", "Funktionsnavnet")),
            ("global", ("Una global", "A global", "En global")),
        ),
        "measure",
        (
            "La medida debe ser bien fundada.",
            "The measure must be well founded.",
            "Målet skal være velfunderet.",
        ),
    ),
    (
        "005",
        (
            "¿Qué orden usa la pila al retornar?",
            "Which order does the stack use on return?",
            "Hvilken rækkefølge bruger stakken ved retur?",
        ),
        (
            ("lifo", ("LIFO", "LIFO", "LIFO")),
            ("fifo", ("FIFO", "FIFO", "FIFO")),
            ("sorted", ("Ordenado", "Sorted", "Sorteret")),
            ("random", ("Aleatorio", "Random", "Tilfældigt")),
        ),
        "lifo",
        (
            "El último marco creado retorna primero.",
            "The last frame created returns first.",
            "Den senest oprettede frame returnerer først.",
        ),
    ),
    (
        "007",
        (
            "¿Qué ocurre antes de la llamada recursiva?",
            "What happens before the recursive call?",
            "Hvad sker før det rekursive kald?",
        ),
        (
            ("descent", ("Trabajo de descenso", "Descent work", "Nedstigningsarbejde")),
            ("unwind", ("Trabajo de desenrollado", "Unwinding work", "Afviklingsarbejde")),
            ("memo", ("Memoización automática", "Automatic memoization", "Automatisk memoization")),
            ("return", ("Retorno final", "Final return", "Endelig retur")),
        ),
        "descent",
        (
            "Se ejecuta al crear marcos.",
            "It runs while creating frames.",
            "Det kører mens frames oprettes.",
        ),
    ),
    (
        "009",
        (
            "¿Qué base corresponde a una suma de secuencia vacía?",
            "Which base fits the sum of an empty sequence?",
            "Hvilken base passer til summen af en tom sekvens?",
        ),
        (
            ("zero", ("0", "0", "0")),
            ("one", ("1", "1", "1")),
            ("none", ("None", "None", "None")),
            ("error", ("Siempre error", "Always error", "Altid fejl")),
        ),
        "zero",
        (
            "Cero es la identidad aditiva.",
            "Zero is the additive identity.",
            "Nul er den additive identitet.",
        ),
    ),
    (
        "011",
        (
            "¿Qué puede evitar slices repetidos?",
            "What can avoid repeated slices?",
            "Hvad kan undgå gentagne slices?",
        ),
        (
            ("index", ("Un índice", "An index", "Et indeks")),
            ("print", ("print", "print", "print")),
            ("set", ("set", "set", "set")),
            ("global", ("Una global", "A global", "En global")),
        ),
        "index",
        (
            "El índice representa el resto sin copiarlo.",
            "The index represents the remainder without copying it.",
            "Indekset repræsenterer resten uden kopiering.",
        ),
    ),
    (
        "013",
        (
            "¿Qué problema encaja naturalmente con recursión?",
            "Which problem naturally fits recursion?",
            "Hvilket problem passer naturligt til rekursion?",
        ),
        (
            (
                "nested",
                (
                    "Estructura anidada de profundidad variable",
                    "Variable-depth nested structure",
                    "Indlejret struktur med variabel dybde",
                ),
            ),
            ("single", ("Una suma de dos números", "Adding two numbers", "Addition af to tal")),
            ("print", ("Imprimir una palabra", "Printing a word", "Udskrivning af et ord")),
            (
                "constant",
                ("Retornar una constante", "Returning a constant", "Returnering af en konstant"),
            ),
        ),
        "nested",
        (
            "Cada hijo conserva la forma del problema.",
            "Each child preserves the problem form.",
            "Hvert barn bevarer problemets form.",
        ),
    ),
    (
        "015",
        (
            "¿Qué evita crecimiento de pila en un cálculo lineal?",
            "What avoids stack growth in a linear computation?",
            "Hvad undgår stakvækst i en lineær beregning?",
        ),
        (
            ("iteration", ("Iteración", "Iteration", "Iteration")),
            ("recursion", ("Más recursión", "More recursion", "Mere rekursion")),
            ("slice", ("Más slicing", "More slicing", "Mere slicing")),
            ("global", ("Una global", "A global", "En global")),
        ),
        "iteration",
        (
            "El bucle mantiene estado en un marco.",
            "The loop keeps state in one frame.",
            "Løkken holder tilstand i én frame.",
        ),
    ),
    (
        "017",
        (
            "¿Qué indica RecursionError normalmente?",
            "What does RecursionError usually indicate?",
            "Hvad angiver RecursionError normalt?",
        ),
        (
            (
                "depth",
                (
                    "Se superó la profundidad permitida",
                    "Allowed depth was exceeded",
                    "Tilladt dybde blev overskredet",
                ),
            ),
            ("syntax", ("Error de sintaxis", "Syntax error", "Syntaksfejl")),
            ("file", ("Archivo ausente", "Missing file", "Manglende fil")),
            ("key", ("Clave ausente", "Missing key", "Manglende nøgle")),
        ),
        "depth",
        (
            "Puede ocurrir incluso con terminación teórica.",
            "It may occur even with theoretical termination.",
            "Det kan ske selv med teoretisk terminering.",
        ),
    ),
    (
        "019",
        (
            "¿Qué técnica evita subproblemas repetidos?",
            "Which technique avoids repeated subproblems?",
            "Hvilken teknik undgår gentagne delproblemer?",
        ),
        (
            ("memo", ("Memoización", "Memoization", "Memoization")),
            ("print", ("print", "print", "print")),
            ("slice", ("Slicing", "Slicing", "Slicing")),
            ("global_clear", ("Borrar todo", "Clear everything", "Ryd alt")),
        ),
        "memo",
        (
            "La caché reutiliza resultados.",
            "The cache reuses results.",
            "Cachen genbruger resultater.",
        ),
    ),
    (
        "021",
        (
            "¿Qué clave es adecuada para memoizar fib(n)?",
            "Which key is suitable for memoizing fib(n)?",
            "Hvilken nøgle er egnet til memoization af fib(n)?",
        ),
        (
            ("n", ("n", "n", "n")),
            ("random", ("Un aleatorio", "A random value", "En tilfældig værdi")),
            ("time", ("La hora", "The time", "Tiden")),
            ("list", ("Una lista mutable", "A mutable list", "En muterbar liste")),
        ),
        "n",
        ("El resultado depende de n.", "The result depends on n.", "Resultatet afhænger af n."),
    ),
    (
        "023",
        (
            "¿Qué prueba verifica directamente una base?",
            "Which test directly verifies a base?",
            "Hvilken test verificerer direkte en base?",
        ),
        (
            (
                "base",
                (
                    "Llamar con la entrada mínima",
                    "Call with the minimal input",
                    "Kald med det minimale input",
                ),
            ),
            ("large", ("Sólo una entrada enorme", "Only a huge input", "Kun et enormt input")),
            ("print", ("Inspeccionar el nombre", "Inspect the name", "Undersøg navnet")),
            ("random", ("No ejecutar", "Do not run", "Kør ikke")),
        ),
        "base",
        (
            "Cada base debe tener una prueba propia.",
            "Every base should have its own test.",
            "Hver base bør have sin egen test.",
        ),
    ),
    (
        "025",
        (
            "¿Qué mide el número total de nodos del árbol de llamadas?",
            "What measures total nodes in the call tree?",
            "Hvad måler det samlede antal noder i kaldstræet?",
        ),
        (
            ("calls", ("Número de llamadas", "Call count", "Antal kald")),
            ("depth", ("Sólo profundidad", "Depth only", "Kun dybde")),
            (
                "locals",
                (
                    "Número de variables locales",
                    "Number of local variables",
                    "Antal lokale variable",
                ),
            ),
            ("prints", ("Número de print", "Number of prints", "Antal print")),
        ),
        "calls",
        (
            "Profundidad y llamadas totales son distintas.",
            "Depth and total calls differ.",
            "Dybde og samlede kald er forskellige.",
        ),
    ),
    (
        "027",
        (
            "¿Qué error tiene cache={} como predeterminado?",
            "What is wrong with cache={} as a default?",
            "Hvad er problemet med cache={} som standard?",
        ),
        (
            (
                "shared",
                (
                    "Se comparte entre llamadas",
                    "It is shared across calls",
                    "Den deles mellem kald",
                ),
            ),
            ("immutable", ("Es inmutable", "It is immutable", "Den er uforanderlig")),
            (
                "syntax",
                ("No es sintaxis Python", "It is not Python syntax", "Det er ikke Python-syntaks"),
            ),
            ("none", ("Ninguno", "None", "Ingen")),
        ),
        "shared",
        (
            "Los predeterminados se evalúan una vez.",
            "Defaults are evaluated once.",
            "Standardværdier evalueres én gang.",
        ),
    ),
    (
        "029",
        (
            "¿Qué comparar para validar una versión recursiva lineal?",
            "What can validate a linear recursive version?",
            "Hvad kan validere en lineær rekursiv version?",
        ),
        (
            (
                "iterative",
                (
                    "Una implementación iterativa de referencia",
                    "An iterative reference implementation",
                    "En iterativ referenceimplementering",
                ),
            ),
            (
                "random",
                (
                    "Un valor aleatorio sin oráculo",
                    "A random value without an oracle",
                    "En tilfældig værdi uden orakel",
                ),
            ),
            ("name", ("El nombre", "The name", "Navnet")),
            ("style", ("Sólo estilo", "Style only", "Kun stil")),
        ),
        "iterative",
        (
            "La equivalencia en casos variados detecta errores.",
            "Equivalence across varied cases detects errors.",
            "Ækvivalens på tværs af tilfælde opdager fejl.",
        ),
    ),
)
_BANK_09_TF = (
    (
        "002",
        (
            "Una función recursiva puede carecer de caso base y terminar siempre.",
            "A recursive function can lack a base case and always terminate.",
            "En rekursiv funktion kan mangle basistilfælde og altid terminere.",
        ),
        False,
        (
            "Sin una salida no puede justificarse terminación.",
            "Without an exit, termination cannot be justified.",
            "Uden en udgang kan terminering ikke begrundes.",
        ),
    ),
    (
        "004",
        (
            "Un caso base correcto garantiza terminación aunque la entrada no cambie.",
            "A correct base case guarantees termination even if input never changes.",
            "Et korrekt basistilfælde garanterer terminering, selv om input aldrig ændres.",
        ),
        False,
        (
            "La base debe ser alcanzable mediante progreso.",
            "The base must be reachable through progress.",
            "Basen skal kunne nås gennem fremskridt.",
        ),
    ),
    (
        "006",
        (
            "Cada llamada recursiva tiene variables locales propias.",
            "Each recursive call has its own local variables.",
            "Hvert rekursivt kald har egne lokale variable.",
        ),
        True,
        (
            "Cada llamada crea un marco.",
            "Each call creates a frame.",
            "Hvert kald opretter en frame.",
        ),
    ),
    (
        "008",
        (
            "El trabajo posterior a la llamada ocurre al desenrollar.",
            "Work after the call happens while unwinding.",
            "Arbejde efter kaldet sker under afvikling.",
        ),
        True,
        (
            "Se ejecuta cuando el subproblema retorna.",
            "It runs when the subproblem returns.",
            "Det kører, når delproblemet returnerer.",
        ),
    ),
    (
        "010",
        (
            "Slicing es siempre gratuito en una recursión de secuencia.",
            "Slicing is always free in sequence recursion.",
            "Slicing er altid gratis i sekvensrekursion.",
        ),
        False,
        (
            "Puede copiar elementos y añadir coste.",
            "It may copy elements and add cost.",
            "Det kan kopiere elementer og tilføje omkostning.",
        ),
    ),
    (
        "012",
        (
            "Una estructura de profundidad variable puede motivar recursión.",
            "A variable-depth structure may motivate recursion.",
            "En struktur med variabel dybde kan motivere rekursion.",
        ),
        True,
        (
            "Cada hijo puede tratarse como subproblema.",
            "Each child can be treated as a subproblem.",
            "Hvert barn kan behandles som et delproblem.",
        ),
    ),
    (
        "014",
        (
            "Python optimiza automáticamente toda tail recursion.",
            "Python automatically optimizes all tail recursion.",
            "Python optimerer automatisk al tail recursion.",
        ),
        False,
        (
            "Python conserva marcos y limita profundidad.",
            "Python keeps frames and limits depth.",
            "Python bevarer frames og begrænser dybde.",
        ),
    ),
    (
        "016",
        (
            "Una solución iterativa puede ser preferible para entradas lineales profundas.",
            "An iterative solution may be preferable for deep linear inputs.",
            "En iterativ løsning kan være bedre til dybe lineære input.",
        ),
        True,
        ("Evita crecimiento de pila.", "It avoids stack growth.", "Den undgår stakvækst."),
    ),
    (
        "018",
        (
            "Dos llamadas recursivas pueden repetir subproblemas.",
            "Two recursive calls may repeat subproblems.",
            "To rekursive kald kan gentage delproblemer.",
        ),
        True,
        (
            "El árbol puede contener entradas iguales.",
            "The tree may contain identical inputs.",
            "Træet kan indeholde identiske input.",
        ),
    ),
    (
        "020",
        (
            "Memoización es útil aunque el resultado cambie aleatoriamente para la misma entrada.",
            "Memoization is useful even when the result changes randomly for the same input.",
            "Memoization er nyttig, selv når resultatet ændres tilfældigt for samme input.",
        ),
        False,
        (
            "Reutilizar un resultado no es válido si la función no es estable.",
            "Reusing a result is invalid if the function is not stable.",
            "Genbrug af et resultat er ugyldigt, hvis funktionen ikke er stabil.",
        ),
    ),
    (
        "022",
        (
            "La profundidad máxima y el número total de llamadas son la misma medida.",
            "Maximum depth and total call count are the same measure.",
            "Maksimal dybde og samlet antal kald er samme mål.",
        ),
        False,
        (
            "Un árbol puede tener poca profundidad y muchas llamadas.",
            "A tree may have limited depth and many calls.",
            "Et træ kan have begrænset dybde og mange kald.",
        ),
    ),
    (
        "024",
        (
            "Las pruebas deben ejecutar cada caso base.",
            "Tests should execute every base case.",
            "Test bør udføre hvert basistilfælde.",
        ),
        True,
        (
            "Las bases son rutas independientes.",
            "Bases are independent paths.",
            "Baser er uafhængige veje.",
        ),
    ),
    (
        "026",
        (
            "Una versión recursiva e iterativa equivalentes tienen siempre igual coste.",
            "Equivalent recursive and iterative versions always have equal cost.",
            "Ækvivalente rekursive og iterative versioner har altid samme omkostning.",
        ),
        False,
        (
            "La pila, slicing y llamadas pueden cambiar el coste.",
            "Stack, slicing, and calls may change cost.",
            "Stak, slicing og kald kan ændre omkostningen.",
        ),
    ),
    (
        "028",
        (
            "cache=None evita compartir un diccionario predeterminado mutable.",
            "cache=None avoids sharing a mutable default dictionary.",
            "cache=None undgår deling af en muterbar standardordbog.",
        ),
        True,
        (
            "La caché se crea por llamada superior.",
            "The cache is created per top-level call.",
            "Cachen oprettes per topkald.",
        ),
    ),
    (
        "030",
        (
            "Los ejemplos recursivos del módulo son algoritmos clínicos validados.",
            "The module's recursive examples are validated clinical algorithms.",
            "Modulets rekursive eksempler er validerede kliniske algoritmer.",
        ),
        False,
        (
            "Son ejercicios didácticos de programación.",
            "They are teaching programming exercises.",
            "De er didaktiske programmeringsøvelser.",
        ),
    ),
)

LOCALIZED_OBJECTIVE_QUESTION_BANK_09 = tuple(
    sorted(
        (
            *(objective_mcq(f"dm857.m09.bank.{n}", p, o, c, e) for n, p, o, c, e in _BANK_09_MCQ),
            *(
                objective_tf(f"dm857.m09.bank.{n}", p, correct=c, explanation=e)
                for n, p, c, e in _BANK_09_TF
            ),
        ),
        key=lambda item: item.item_id,
    )
)


def materialize_module_09_question_bank(locale: AppLocale | str) -> tuple[AssessmentItem, ...]:
    resolved = locale if isinstance(locale, AppLocale) else AppLocale.resolve(locale)
    return tuple(item.materialize(resolved) for item in LOCALIZED_OBJECTIVE_QUESTION_BANK_09)


MODULE_09_RECURSION: LearningModule = LOCALIZED_MODULE_09_RECURSION.materialize(
    AppLocale.SPANISH_SPAIN
)
OBJECTIVE_QUESTION_BANK_09 = materialize_module_09_question_bank(AppLocale.SPANISH_SPAIN)

__all__ = [
    "LOCALIZED_MODULE_09_RECURSION",
    "LOCALIZED_OBJECTIVE_QUESTION_BANK_09",
    "MODULE_09_RECURSION",
    "OBJECTIVE_QUESTION_BANK_09",
    "materialize_module_09_question_bank",
]
