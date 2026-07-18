"""DM857 module 6: lists, tuples, and sequence processing."""

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

LOCALIZED_MODULE_06_SEQUENCES = LocalizedLearningModule(
    course_code="DM857",
    module_id="dm857.m06",
    title=t(
        "Listas, tuplas y procesamiento de secuencias",
        "Lists, tuples, and sequence processing",
        "Lister, tupler og sekvensbehandling",
    ),
    summary=t(
        "Este módulo desarrolla el uso de listas y tuplas para representar colecciones ordenadas. "
        "Incluye acceso, slicing, mutabilidad, aliasing, copias, métodos, recorridos, búsqueda, "
        "agregación, listas anidadas, matrices sencillas, desempaquetado, retorno múltiple y "
        "criterios para elegir una estructura adecuada.",
        "This module develops the use of lists and tuples to represent ordered collections. It "
        "covers access, slicing, mutability, aliasing, copies, methods, traversal, search, "
        "aggregation, nested lists, simple matrices, unpacking, multiple return values, and "
        "criteria for choosing an appropriate structure.",
        "Dette modul udvikler brugen af lister og tupler til ordnede samlinger. Det dækker adgang, "
        "slicing, muterbarhed, aliasing, kopier, metoder, gennemløb, søgning, aggregering, indlejrede "
        "lister, simple matricer, udpakning, flere returværdier og valg af passende struktur.",
    ),
    objectives=(
        objective("m06.o1", ("Crear y acceder a listas y tuplas mediante índices y slices.", "Create and access lists and tuples using indices and slices.", "Oprette og tilgå lister og tupler med indeks og slices.")),
        objective("m06.o2", ("Distinguir mutabilidad, reasignación y aliasing.", "Distinguish mutability, reassignment, and aliasing.", "Skelne mellem muterbarhed, gentildeling og aliasing.")),
        objective("m06.o3", ("Aplicar append, extend, insert, remove, pop y clear con precisión.", "Apply append, extend, insert, remove, pop, and clear precisely.", "Anvende append, extend, insert, remove, pop og clear præcist.")),
        objective("m06.o4", ("Recorrer secuencias y construir resultados sin mutaciones accidentales.", "Traverse sequences and build results without accidental mutation.", "Gennemløbe sekvenser og bygge resultater uden utilsigtet mutation.")),
        objective("m06.o5", ("Implementar búsqueda, conteo, suma, mínimos y máximos de forma segura.", "Implement search, counting, sums, minima, and maxima safely.", "Implementere søgning, optælling, summer, minima og maksima sikkert.")),
        objective("m06.o6", ("Razonar sobre listas anidadas y formas rectangulares.", "Reason about nested lists and rectangular shapes.", "Ræsonnere om indlejrede lister og rektangulære former.")),
        objective("m06.o7", ("Usar tuplas y desempaquetado para registros pequeños y retornos múltiples.", "Use tuples and unpacking for small records and multiple return values.", "Bruge tupler og udpakning til små poster og flere returværdier.")),
        objective("m06.o8", ("Diseñar pruebas para colecciones vacías, aliasing y dimensiones irregulares.", "Design tests for empty collections, aliasing, and irregular dimensions.", "Designe test for tomme samlinger, aliasing og uregelmæssige dimensioner.")),
    ),
    concepts=(
        concept(
            "ordered-sequences",
            ("Secuencias ordenadas", "Ordered sequences", "Ordnede sekvenser"),
            (
                "Listas y tuplas conservan un orden y admiten len, índices, slices, pertenencia e iteración. "
                "Una lista se escribe con corchetes y una tupla normalmente con paréntesis o comas. El índice "
                "identifica posición, no valor. Los slices crean una nueva secuencia superficial del mismo tipo.",
                "Lists and tuples preserve order and support len, indices, slices, membership, and iteration. A list "
                "uses brackets and a tuple normally uses parentheses or commas. An index identifies position, not value. "
                "Slices create a new shallow sequence of the same type.",
                "Lister og tupler bevarer rækkefølge og understøtter len, indeks, slices, medlemskab og iteration. En liste "
                "bruger kantede parenteser, og en tuple bruger normalt parenteser eller kommaer. Et indeks angiver position, "
                "ikke værdi. Slices opretter en ny overfladisk sekvens af samme type.",
            ),
            (
                ("El primer índice es 0.", "The first index is 0.", "Det første indeks er 0."),
                ("Un slice excluye stop.", "A slice excludes stop.", "Et slice udelukker stop."),
                ("in comprueba valores, no posiciones.", "in checks values, not positions.", "in kontrollerer værdier, ikke positioner."),
            ),
        ),
        concept(
            "mutability-and-aliasing",
            ("Mutabilidad y aliasing", "Mutability and aliasing", "Muterbarhed og aliasing"),
            (
                "Las listas son mutables: sus elementos pueden cambiar sin crear otra lista. Si dos nombres apuntan a la "
                "misma lista, una mutación observada mediante uno también aparece mediante el otro; esto es aliasing. Reasignar "
                "un nombre no modifica el objeto anterior. Las tuplas son inmutables, aunque pueden contener objetos mutables.",
                "Lists are mutable: their elements can change without creating another list. If two names refer to the same list, "
                "a mutation through one is visible through the other; this is aliasing. Reassigning a name does not mutate the old "
                "object. Tuples are immutable, although they may contain mutable objects.",
                "Lister er muterbare: elementerne kan ændres uden at oprette en ny liste. Hvis to navne refererer til samme liste, "
                "er en mutation gennem det ene synlig gennem det andet; dette er aliasing. Gentildeling af et navn ændrer ikke det "
                "gamle objekt. Tupler er uforanderlige, men kan indeholde muterbare objekter.",
            ),
            (
                ("a = b crea aliasing, no una copia.", "a = b creates aliasing, not a copy.", "a = b skaber aliasing, ikke en kopi."),
                ("a[:] o list(a) crea una copia superficial.", "a[:] or list(a) creates a shallow copy.", "a[:] eller list(a) opretter en overfladisk kopi."),
                ("Una copia superficial comparte objetos internos anidados.", "A shallow copy shares nested inner objects.", "En overfladisk kopi deler indlejrede objekter."),
            ),
        ),
        concept(
            "list-methods",
            ("Métodos de listas", "List methods", "Listemetoder"),
            (
                "append añade un objeto como un elemento; extend incorpora los elementos de un iterable. insert añade en una "
                "posición; remove elimina la primera coincidencia y falla si no existe; pop elimina y retorna un elemento; clear "
                "vacía la lista. La mayoría de estos métodos mutan y retornan None, por lo que no deben asignarse esperando una lista.",
                "append adds one object as one element; extend incorporates elements from an iterable. insert adds at a position; "
                "remove deletes the first match and fails when absent; pop removes and returns an element; clear empties the list. "
                "Most of these methods mutate and return None, so they should not be assigned expecting a list.",
                "append tilføjer ét objekt som ét element; extend tilføjer elementerne fra en iterable. insert tilføjer på en position; "
                "remove fjerner første match og fejler ved fravær; pop fjerner og returnerer et element; clear tømmer listen. De fleste "
                "metoder muterer og returnerer None.",
            ),
            (
                ("append([2, 3]) añade una lista anidada.", "append([2, 3]) adds a nested list.", "append([2, 3]) tilføjer en indlejret liste."),
                ("extend([2, 3]) añade dos elementos.", "extend([2, 3]) adds two elements.", "extend([2, 3]) tilføjer to elementer."),
                ("pop combina mutación y retorno.", "pop combines mutation and return.", "pop kombinerer mutation og retur."),
            ),
        ),
        concept(
            "traversal-and-construction",
            ("Recorrido y construcción", "Traversal and construction", "Gennemløb og konstruktion"),
            (
                "Un for puede recorrer valores directamente; enumerate añade índice; zip recorre secuencias en paralelo hasta "
                "la más corta. Para construir una lista nueva puede iniciarse una lista vacía y usar append. Mutar la misma lista "
                "mientras se recorre puede saltar elementos o producir lógica difícil de verificar; suele ser más seguro construir otra.",
                "A for loop may traverse values directly; enumerate adds an index; zip traverses sequences in parallel until the "
                "shortest ends. A new list can be built from an empty list using append. Mutating a list while traversing it may skip "
                "elements or create hard-to-verify logic; building another list is usually safer.",
                "En for-løkke kan gennemløbe værdier direkte; enumerate tilføjer indeks; zip gennemløber sekvenser parallelt indtil den "
                "korteste slutter. En ny liste kan bygges fra en tom liste med append. Mutation af samme liste under gennemløb kan springe "
                "elementer over og bør normalt undgås.",
            ),
            (
                ("Recorre valores si no necesitas posiciones.", "Traverse values when positions are unnecessary.", "Gennemløb værdier, når positioner ikke er nødvendige."),
                ("zip se detiene con la secuencia más corta.", "zip stops with the shortest sequence.", "zip stopper med den korteste sekvens."),
                ("Construir una salida nueva reduce efectos secundarios.", "Building a new output reduces side effects.", "Opbygning af et nyt output reducerer sideeffekter."),
            ),
        ),
        concept(
            "aggregation-and-empty-input",
            ("Agregación y colecciones vacías", "Aggregation and empty collections", "Aggregering og tomme samlinger"),
            (
                "sum y len permiten promedios cuando la colección no está vacía. min y max requieren al menos un elemento o un "
                "default cuando corresponde. Una búsqueda puede retornar índice, valor, bool o None; el contrato debe especificarlo. "
                "Inicializar máximos con un número arbitrario puede fallar; usar el primer elemento exige validar que exista.",
                "sum and len support means when the collection is non-empty. min and max require at least one element or an appropriate "
                "default. A search may return an index, value, bool, or None; the contract should specify which. Initializing a maximum "
                "with an arbitrary number may fail; using the first element requires non-empty input.",
                "sum og len understøtter gennemsnit for ikke-tomme samlinger. min og max kræver mindst ét element eller en passende "
                "default. En søgning kan returnere indeks, værdi, bool eller None; kontrakten skal angive hvad. Initialisering af maksimum "
                "med et vilkårligt tal kan fejle.",
            ),
            (
                ("Un promedio requiere decidir qué hacer con entrada vacía.", "A mean requires a decision for empty input.", "Et gennemsnit kræver en beslutning for tomt input."),
                ("min([]) y max([]) producen ValueError.", "min([]) and max([]) raise ValueError.", "min([]) og max([]) giver ValueError."),
                ("El contrato de ausencia debe ser consistente.", "The absence contract should be consistent.", "Kontrakten for fravær bør være konsistent."),
            ),
        ),
        concept(
            "nested-lists-and-matrices",
            ("Listas anidadas y matrices", "Nested lists and matrices", "Indlejrede lister og matricer"),
            (
                "Una lista anidada puede representar filas. matrix[row][column] realiza dos accesos. Una matriz rectangular requiere "
                "que todas las filas tengan la misma longitud; las listas irregulares también son válidas, pero necesitan otro contrato. "
                "La expresión [[0] * cols] * rows crea aliasing entre filas; una construcción por iteración crea filas independientes.",
                "A nested list may represent rows. matrix[row][column] performs two accesses. A rectangular matrix requires every row "
                "to have the same length; ragged lists are also valid but require a different contract. The expression [[0] * cols] * rows "
                "aliases rows; constructing rows iteratively creates independent rows.",
                "En indlejret liste kan repræsentere rækker. matrix[row][column] udfører to opslag. En rektangulær matrix kræver samme "
                "rækkelængde; ujævne lister er også gyldige, men kræver en anden kontrakt. Udtrykket [[0] * cols] * rows skaber aliasing "
                "mellem rækker, mens iterativ konstruktion skaber uafhængige rækker.",
            ),
            (
                ("Validar forma evita IndexError inesperados.", "Shape validation prevents unexpected IndexError failures.", "Formvalidering forhindrer uventede IndexError-fejl."),
                ("Las filas repetidas con * pueden compartir identidad.", "Rows repeated with * may share identity.", "Rækker gentaget med * kan dele identitet."),
                ("Dos bucles anidados recorren filas y columnas.", "Two nested loops traverse rows and columns.", "To indlejrede løkker gennemløber rækker og kolonner."),
            ),
        ),
        concept(
            "tuples-and-unpacking",
            ("Tuplas y desempaquetado", "Tuples and unpacking", "Tupler og udpakning"),
            (
                "Una tupla representa una secuencia fija. El desempaquetado asigna elementos a varios nombres y exige una cantidad "
                "compatible, salvo uso de *. Una función que retorna varios valores en realidad retorna una tupla. Las tuplas son útiles "
                "para registros pequeños cuyo tamaño y significado por posición están bien definidos.",
                "A tuple represents a fixed sequence. Unpacking assigns elements to several names and requires a compatible count unless "
                "* is used. A function returning several values actually returns a tuple. Tuples are useful for small records whose size "
                "and positional meaning are well defined.",
                "En tuple repræsenterer en fast sekvens. Udpakning tildeler elementer til flere navne og kræver et kompatibelt antal, medmindre "
                "* bruges. En funktion, der returnerer flere værdier, returnerer faktisk en tuple. Tupler er nyttige til små poster med klart "
                "defineret størrelse og positionsbetydning.",
            ),
            (
                ("Una tupla de un elemento requiere coma: (value,).", "A one-element tuple requires a comma: (value,).", "En tuple med ét element kræver komma: (value,)."),
                ("El desempaquetado documenta roles mediante nombres.", "Unpacking documents roles through names.", "Udpakning dokumenterer roller gennem navne."),
                ("Retornar a, b equivale a retornar (a, b).", "Returning a, b is equivalent to returning (a, b).", "At returnere a, b svarer til at returnere (a, b)."),
            ),
        ),
        concept(
            "choosing-and-testing-structures",
            ("Elección y pruebas de estructuras", "Choosing and testing structures", "Valg og test af strukturer"),
            (
                "Una lista es apropiada cuando la colección debe crecer, reducirse o cambiar. Una tupla comunica una agrupación fija. "
                "La elección debe basarse en operaciones y contrato, no sólo en sintaxis. Las pruebas deben cubrir vacíos, un elemento, "
                "duplicados, valores ausentes, aliasing, copias y dimensiones irregulares.",
                "A list is appropriate when a collection must grow, shrink, or change. A tuple communicates a fixed grouping. The choice "
                "should follow operations and contract, not syntax alone. Tests should cover empty input, one element, duplicates, absence, "
                "aliasing, copies, and irregular dimensions.",
                "En liste er passende, når en samling skal vokse, mindskes eller ændres. En tuple kommunikerer en fast gruppering. Valget "
                "bør følge operationer og kontrakt. Test bør dække tomt input, ét element, dubletter, fravær, aliasing, kopier og uregelmæssige dimensioner.",
            ),
            (
                ("Mutabilidad es una decisión de diseño.", "Mutability is a design decision.", "Muterbarhed er en designbeslutning."),
                ("El contrato debe indicar si una función modifica su argumento.", "The contract should state whether a function mutates its argument.", "Kontrakten bør angive, om en funktion ændrer sit argument."),
                ("Las pruebas de identidad complementan las pruebas de igualdad.", "Identity tests complement equality tests.", "Identitetstest supplerer lighedstest."),
            ),
        ),
    ),
    worked_examples=(
        example(
            "m06.e1",
            ("append frente a extend", "append versus extend", "append versus extend"),
            ("Compara cómo se añaden dos valores.", "Compare how two values are added.", "Sammenlign, hvordan to værdier tilføjes."),
            (("append recibe un objeto.", "append receives one object.", "append modtager ét objekt."), ("extend recorre el iterable recibido.", "extend traverses the received iterable.", "extend gennemløber den modtagne iterable.")),
            "a = [1]\na.append([2, 3])\n\nb = [1]\nb.extend([2, 3])\n\nprint(a)\nprint(b)",
            "[1, [2, 3]]\n[1, 2, 3]",
            ("append crea un elemento anidado; extend añade los dos enteros.", "append creates one nested element; extend adds both integers.", "append opretter ét indlejret element; extend tilføjer begge heltal."),
        ),
        example(
            "m06.e2",
            ("Aliasing y copia superficial", "Aliasing and shallow copy", "Aliasing og overfladisk kopi"),
            ("Muestra la diferencia entre asignar y copiar.", "Show the difference between assignment and copying.", "Vis forskellen mellem tildeling og kopiering."),
            (("alias apunta al mismo objeto.", "alias refers to the same object.", "alias refererer til samme objekt."), ("copy obtiene una lista exterior nueva.", "copy obtains a new outer list.", "copy får en ny ydre liste.")),
            "original = [10, 20]\nalias = original\ncopy = original.copy()\n\nalias.append(30)\ncopy.append(40)\n\nprint(original)\nprint(copy)",
            "[10, 20, 30]\n[10, 20, 40]",
            ("La mutación mediante alias afecta original; la copia exterior es independiente.", "Mutation through alias affects original; the outer copy is independent.", "Mutation gennem alias påvirker original; den ydre kopi er uafhængig."),
        ),
        example(
            "m06.e3",
            ("Construir una lista filtrada", "Build a filtered list", "Byg en filtreret liste"),
            ("Conserva sólo valores no negativos sin modificar la entrada.", "Keep only non-negative values without mutating the input.", "Bevar kun ikke-negative værdier uden at ændre input."),
            (("Se crea una salida vacía.", "An empty output is created.", "Et tomt output oprettes."), ("Cada valor válido se añade con append.", "Each valid value is added with append.", "Hver gyldig værdi tilføjes med append.")),
            "def non_negative(values: list[float]) -> list[float]:\n    result: list[float] = []\n    for value in values:\n        if value >= 0:\n            result.append(value)\n    return result\n\ndata = [-1.0, 0.0, 2.5]\nprint(non_negative(data))\nprint(data)",
            "[0.0, 2.5]\n[-1.0, 0.0, 2.5]",
            ("La función retorna una lista nueva y preserva el argumento.", "The function returns a new list and preserves the argument.", "Funktionen returnerer en ny liste og bevarer argumentet."),
        ),
        example(
            "m06.e4",
            ("Sumas por fila", "Row sums", "Rækkesummer"),
            ("Calcula la suma de cada fila rectangular.", "Calculate the sum of each rectangular row.", "Beregn summen af hver rektangulær række."),
            (("El bucle exterior recorre filas.", "The outer loop traverses rows.", "Den ydre løkke gennemløber rækker."), ("sum agrega cada fila.", "sum aggregates each row.", "sum aggregerer hver række.")),
            "def row_sums(matrix: list[list[int]]) -> list[int]:\n    result: list[int] = []\n    for row in matrix:\n        result.append(sum(row))\n    return result\n\nprint(row_sums([[1, 2], [3, 4]]))",
            "[3, 7]",
            ("La salida contiene una suma por fila y no modifica la matriz.", "The output contains one sum per row and does not mutate the matrix.", "Output indeholder én sum pr. række og ændrer ikke matricen."),
        ),
        example(
            "m06.e5",
            ("Retorno múltiple con tupla", "Multiple return with a tuple", "Flere returværdier med tuple"),
            ("Retorna mínimo y máximo de una secuencia no vacía.", "Return the minimum and maximum of a non-empty sequence.", "Returnér minimum og maksimum for en ikke-tom sekvens."),
            (("La precondición exige al menos un valor.", "The precondition requires at least one value.", "Forudsætningen kræver mindst én værdi."), ("El llamador desempaqueta la tupla.", "The caller unpacks the tuple.", "Den kaldende kode udpakker tuplen.")),
            "def bounds(values: list[float]) -> tuple[float, float]:\n    if not values:\n        raise ValueError(\"values cannot be empty\")\n    return min(values), max(values)\n\nlow, high = bounds([3.0, 1.0, 4.0])\nprint(low, high)",
            "1.0 4.0",
            ("El retorno contiene dos valores con significado posicional documentado.", "The return contains two values with documented positional meaning.", "Returen indeholder to værdier med dokumenteret positionsbetydning."),
        ),
    ),
    practice_exercises=(
        practice("m06.p01", ActivityType.CODE_TRACING, ("Traza aliasing después de b = a y b.append(3).", "Trace aliasing after b = a and b.append(3).", "Gennemgå aliasing efter b = a og b.append(3)."), (("a y b apuntan al mismo objeto.", "a and b refer to the same object.", "a og b refererer til samme objekt."),), ("Si a era [1, 2], ambos muestran [1, 2, 3].", "If a was [1, 2], both show [1, 2, 3].", "Hvis a var [1, 2], viser begge [1, 2, 3]."), ("La mutación se observa mediante todos los alias.", "Mutation is visible through every alias.", "Mutation er synlig gennem alle aliaser."), "a = [1, 2]\nb = a\nb.append(3)"),
        practice("m06.p02", ActivityType.DEBUGGING, ("Corrige result = values.append(4).", "Fix result = values.append(4).", "Ret result = values.append(4)."), (("append retorna None.", "append returns None.", "append returnerer None."),), ("values.append(4); result = values, o result = values + [4] si se desea una lista nueva.", "values.append(4); result = values, or result = values + [4] for a new list.", "values.append(4); result = values, eller result = values + [4] for en ny liste."), ("La solución depende de si el contrato permite mutación.", "The solution depends on whether the contract allows mutation.", "Løsningen afhænger af, om kontrakten tillader mutation."), "values = [1, 2, 3]\nresult = values.append(4)"),
        practice("m06.p03", ActivityType.FILL_IN_THE_BLANK, ("Completa: append añade ____ objeto como un elemento.", "Complete: append adds ____ object as one element.", "Udfyld: append tilføjer ____ objekt som ét element."), (("Contrasta con extend.", "Contrast with extend.", "Sammenlign med extend."),), ("un", "one", "ét"), ("El iterable no se expande automáticamente con append.", "The iterable is not automatically expanded by append.", "Den iterable udvides ikke automatisk med append.")),
        practice("m06.p04", ActivityType.CODE_COMPLETION, ("Escribe una función que retorne una copia superficial.", "Write a function returning a shallow copy.", "Skriv en funktion, der returnerer en overfladisk kopi."), (("Usa copy o slicing completo.", "Use copy or full slicing.", "Brug copy eller fuldt slice."),), ("def clone(values):\n    return values.copy()", "def clone(values):\n    return values.copy()", "def clone(values):\n    return values.copy()"), ("La lista exterior es nueva, pero objetos internos pueden compartirse.", "The outer list is new, but inner objects may be shared.", "Den ydre liste er ny, men indre objekter kan deles."), "def clone(values):\n    # completa"),
        practice("m06.p05", ActivityType.SHORT_ANSWER, ("Explica por qué una copia superficial no basta siempre para listas anidadas.", "Explain why a shallow copy is not always sufficient for nested lists.", "Forklar, hvorfor en overfladisk kopi ikke altid er nok til indlejrede lister."), (("La copia exterior conserva referencias internas.", "The outer copy preserves inner references.", "Den ydre kopi bevarer indre referencer."),), ("Las filas u objetos internos pueden seguir siendo compartidos; mutarlos se observa desde ambas estructuras.", "Rows or inner objects may remain shared; mutating them is visible from both structures.", "Rækker eller indre objekter kan fortsat deles; mutation er synlig fra begge strukturer."), ("Igualdad exterior distinta no implica independencia profunda.", "A distinct outer object does not imply deep independence.", "Et forskelligt ydre objekt indebærer ikke dyb uafhængighed.")),
        practice("m06.p06", ActivityType.ORDERING, ("Ordena una agregación de máximo manual.", "Order a manual maximum aggregation.", "Ordén en manuel maksimumaggregering."), (("Valida vacío antes de usar el primer elemento.", "Validate empty input before using the first element.", "Validér tomt input før første element bruges."),), ("1. Validar no vacío. 2. best = values[0]. 3. Recorrer restantes. 4. Actualizar si value > best. 5. Retornar best.", "1. Validate non-empty. 2. best = values[0]. 3. Traverse remaining values. 4. Update if value > best. 5. Return best.", "1. Validér ikke-tomt. 2. best = values[0]. 3. Gennemløb resten. 4. Opdatér hvis value > best. 5. Returnér best."), ("El primer elemento evita un centinela numérico arbitrario.", "The first element avoids an arbitrary numeric sentinel.", "Det første element undgår en vilkårlig numerisk stopværdi.")),
        practice("m06.p07", ActivityType.CODE_COMPLETION, ("Completa una función que retorne índices y valores con enumerate.", "Complete a function returning indices and values using enumerate.", "Færdiggør en funktion, der returnerer indeks og værdier med enumerate."), (("Construye una lista de tuplas.", "Build a list of tuples.", "Byg en liste af tupler."),), ("result = []\nfor index, value in enumerate(values):\n    result.append((index, value))\nreturn result", "result = []\nfor index, value in enumerate(values):\n    result.append((index, value))\nreturn result", "result = []\nfor index, value in enumerate(values):\n    result.append((index, value))\nreturn result"), ("Cada elemento de salida es una tupla (índice, valor).", "Each output element is an (index, value) tuple.", "Hvert outputelement er en tuple (indeks, værdi)."), "def indexed(values):\n    # completa"),
        practice("m06.p08", ActivityType.DATA_INTERPRETATION, ("zip produjo dos pares para listas de longitudes 2 y 4. Interpreta.", "zip produced two pairs for lists of lengths 2 and 4. Interpret.", "zip producerede to par for lister med længde 2 og 4. Fortolk."), (("zip se detiene al terminar la secuencia más corta.", "zip stops when the shortest sequence ends.", "zip stopper, når den korteste sekvens slutter."),), ("Los dos elementos extra de la lista larga no participan.", "The two extra elements in the longer list do not participate.", "De to ekstra elementer i den længere liste deltager ikke."), ("Si se requiere igualdad de longitudes, debe validarse antes.", "If equal lengths are required, validate first.", "Hvis samme længde kræves, skal det valideres først.")),
        practice("m06.p09", ActivityType.DEBUGGING, ("Corrige matrix = [[0] * 3] * 2 cuando las filas deben ser independientes.", "Fix matrix = [[0] * 3] * 2 when rows must be independent.", "Ret matrix = [[0] * 3] * 2 når rækkerne skal være uafhængige."), (("La multiplicación repite referencias.", "Multiplication repeats references.", "Multiplikation gentager referencer."),), ("matrix = [[0] * 3 for _ in range(2)]", "matrix = [[0] * 3 for _ in range(2)]", "matrix = [[0] * 3 for _ in range(2)]"), ("Cada iteración crea una fila nueva.", "Each iteration creates a new row.", "Hver iteration opretter en ny række."), "matrix = [[0] * 3] * 2\nmatrix[0][0] = 1"),
        practice("m06.p10", ActivityType.ORAL_EXPLANATION, ("Compara lista y tupla para un par (mínimo, máximo).", "Compare list and tuple for a (minimum, maximum) pair.", "Sammenlign liste og tuple til et par (minimum, maksimum)."), (("Piensa en tamaño fijo y mutabilidad.", "Think fixed size and mutability.", "Tænk fast størrelse og muterbarhed."),), ("Una tupla comunica que el registro tiene dos posiciones fijas y no necesita cambios estructurales; una lista sería adecuada si el conjunto debiera crecer o modificarse.", "A tuple communicates a fixed two-position record with no structural changes; a list would fit a collection that must grow or change.", "En tuple kommunikerer en fast post med to positioner uden strukturelle ændringer; en liste passer til en samling, der skal vokse eller ændres."), ("La elección expresa intención además de capacidad técnica.", "The choice expresses intent as well as technical capability.", "Valget udtrykker intention ud over teknisk kapacitet.")),
        practice("m06.p11", ActivityType.SHORT_ANSWER, ("Diseña casos para mean(values).", "Design cases for mean(values).", "Design tilfælde for mean(values)."), (("Incluye vacío, uno y varios.", "Include empty, one, and several.", "Medtag tomt, ét og flere."),), ("Lista vacía según contrato; un elemento; varios positivos; mezcla con negativos; valores decimales.", "Empty list according to contract; one element; several positives; mixed negatives; decimal values.", "Tom liste efter kontrakt; ét element; flere positive; blandede negative; decimaltal."), ("Los casos prueban división, longitud y política para vacío.", "The cases test division, length, and empty-input policy.", "Tilfældene tester division, længde og politik for tomt input.")),
        practice("m06.p12", ActivityType.PIPELINE_DESIGN, ("Descompón un flujo para validar una matriz y calcular sumas de columna.", "Decompose a flow to validate a matrix and calculate column sums.", "Dekomponér et flow til at validere en matrix og beregne kolonnesummer."), (("Separa forma y agregación.", "Separate shape and aggregation.", "Adskil form og aggregering."),), ("is_rectangular(matrix)->bool; column_count(matrix)->int; column_sums(matrix)->list[float]; una coordinadora valida antes de agregar.", "is_rectangular(matrix)->bool; column_count(matrix)->int; column_sums(matrix)->list[float]; a coordinator validates before aggregation.", "is_rectangular(matrix)->bool; column_count(matrix)->int; column_sums(matrix)->list[float]; en koordinator validerer før aggregering."), ("La agregación puede asumir forma válida después de la frontera de validación.", "Aggregation may assume valid shape after the validation boundary.", "Aggregering kan antage gyldig form efter valideringsgrænsen.")),
    ),
    assessment_items=(
        authored_item("dm857.m06.assessment.001", ActivityType.CODE_TRACING, ("Traza a=[1]; b=a; b.append(2).", "Trace a=[1]; b=a; b.append(2).", "Gennemgå a=[1]; b=a; b.append(2)."), (("a y b son [1, 2].", "a and b are [1, 2].", "a og b er [1, 2]."),), ("Los dos nombres son alias del mismo objeto.", "Both names alias the same object.", "Begge navne er aliaser for samme objekt.")),
        authored_item("dm857.m06.assessment.002", ActivityType.MULTIPLE_SELECT, ("Selecciona operaciones que mutan una lista.", "Select operations that mutate a list.", "Vælg operationer, der muterer en liste."), (), ("append, extend y clear modifican el objeto.", "append, extend, and clear modify the object.", "append, extend og clear ændrer objektet."), options=(("append", ("append", "append", "append")), ("extend", ("extend", "extend", "extend")), ("clear", ("clear", "clear", "clear")), ("slice", ("values[:]", "values[:]", "values[:]"))), correct_option_ids=("append", "extend", "clear")),
        authored_item("dm857.m06.assessment.003", ActivityType.DEBUGGING, ("Corrige values = values.sort().", "Fix values = values.sort().", "Ret values = values.sort()."), (("Usar values.sort() sin asignar, o sorted_values = sorted(values).", "Use values.sort() without assignment, or sorted_values = sorted(values).", "Brug values.sort() uden tildeling, eller sorted_values = sorted(values)."),), ("sort muta y retorna None; sorted retorna una lista nueva.", "sort mutates and returns None; sorted returns a new list.", "sort muterer og returnerer None; sorted returnerer en ny liste.")),
        authored_item("dm857.m06.assessment.004", ActivityType.FILL_IN_THE_BLANK, ("Completa: a = b crea un ____ de la misma lista.", "Complete: a = b creates an ____ to the same list.", "Udfyld: a = b opretter et ____ til samme liste."), (("alias", "alias", "alias"),), ("No se crea una copia.", "No copy is created.", "Der oprettes ingen kopi.")),
        authored_item("dm857.m06.assessment.005", ActivityType.MATCHING, ("Relaciona método y comportamiento.", "Match each method to its behavior.", "Match hver metode med dens adfærd."), (), ("append→un objeto; extend→elementos; pop→elimina y retorna; remove→primera coincidencia.", "append→one object; extend→elements; pop→remove and return; remove→first match.", "append→ét objekt; extend→elementer; pop→fjern og returnér; remove→første match."), options=(("append", ("append → un objeto", "append → one object", "append → ét objekt")), ("extend", ("extend → elementos", "extend → elements", "extend → elementer")), ("pop", ("pop → elimina y retorna", "pop → removes and returns", "pop → fjerner og returnerer")), ("remove", ("remove → primera coincidencia", "remove → first match", "remove → første match"))), correct_option_ids=("append", "extend", "pop", "remove")),
        authored_item("dm857.m06.assessment.006", ActivityType.ORDERING, ("Ordena una búsqueda manual.", "Order a manual search.", "Ordén en manuel søgning."), (), ("Recorrer, comparar, retornar al encontrar, retornar ausencia al final.", "Traverse, compare, return when found, return absence at the end.", "Gennemløb, sammenlign, returnér ved fund, returnér fravær til sidst."), options=(("traverse", ("Recorrer", "Traverse", "Gennemløb")), ("compare", ("Comparar", "Compare", "Sammenlign")), ("found", ("Retornar al encontrar", "Return when found", "Returnér ved fund")), ("absent", ("Retornar ausencia al final", "Return absence at the end", "Returnér fravær til sidst"))), correct_option_ids=("traverse", "compare", "found", "absent")),
        authored_item("dm857.m06.assessment.007", ActivityType.CODE_COMPLETION, ("Implementa una copia exterior con slicing.", "Implement an outer copy using slicing.", "Implementér en ydre kopi med slicing."), (("copy = values[:]", "copy = values[:]", "copy = values[:]"),), ("El slice completo crea una lista exterior nueva.", "The full slice creates a new outer list.", "Det fulde slice opretter en ny ydre liste.")),
        authored_item("dm857.m06.assessment.008", ActivityType.SHORT_ANSWER, ("Explica igualdad frente a identidad para listas.", "Explain equality versus identity for lists.", "Forklar lighed versus identitet for lister."), (("== compara contenido; is comprueba si es el mismo objeto.", "== compares content; is checks whether it is the same object.", "== sammenligner indhold; is kontrollerer, om det er samme objekt."),), ("Dos listas distintas pueden ser iguales sin ser idénticas.", "Two distinct lists may be equal without being identical.", "To forskellige lister kan være lige uden at være identiske.")),
        authored_item("dm857.m06.assessment.009", ActivityType.DATA_INTERPRETATION, ("Interpreta min([]) produciendo ValueError.", "Interpret min([]) raising ValueError.", "Fortolk min([]), der giver ValueError."), (("No existe un mínimo sin política adicional para una colección vacía.", "No minimum exists for an empty collection without an additional policy.", "Der findes intet minimum for en tom samling uden en ekstra politik."),), ("El contrato debe rechazar vacío o definir un valor alternativo.", "The contract should reject empty input or define an alternative value.", "Kontrakten bør afvise tomt input eller definere en alternativ værdi.")),
        authored_item("dm857.m06.assessment.010", ActivityType.ORAL_EXPLANATION, ("Explica el peligro de [[0]*3]*2.", "Explain the danger of [[0]*3]*2.", "Forklar faren ved [[0]*3]*2."), (("Las dos filas son referencias al mismo objeto interno; cambiar una celda puede cambiar ambas filas.", "Both rows reference the same inner object; changing one cell may change both rows.", "Begge rækker refererer til samme indre objekt; ændring af én celle kan ændre begge rækker."),), ("La multiplicación repite referencias, no construye filas independientes.", "Multiplication repeats references rather than constructing independent rows.", "Multiplikation gentager referencer i stedet for at konstruere uafhængige rækker.")),
        authored_item("dm857.m06.assessment.011", ActivityType.PIPELINE_DESIGN, ("Diseña un flujo para limpiar, validar y resumir una lista de valores.", "Design a flow to clean, validate, and summarize a value list.", "Design et flow til at rense, validere og opsummere en værdiliste."), (("clean_values, validate_values, summarize_values y una coordinadora.", "clean_values, validate_values, summarize_values, and a coordinator.", "clean_values, validate_values, summarize_values og en koordinator."),), ("Cada función debe declarar si conserva o modifica la entrada.", "Each function should state whether it preserves or mutates input.", "Hver funktion bør angive, om input bevares eller ændres.")),
        authored_item("dm857.m06.assessment.012", ActivityType.DEBUGGING, ("Corrige un bucle que elimina negativos de la misma lista mientras la recorre.", "Fix a loop that removes negatives from the same list while traversing it.", "Ret en løkke, der fjerner negative værdier fra samme liste under gennemløb."), (("Construir una nueva lista con valores permitidos o recorrer una copia.", "Build a new list with allowed values or traverse a copy.", "Byg en ny liste med tilladte værdier eller gennemløb en kopi."),), ("La mutación durante el recorrido puede desplazar índices y omitir elementos.", "Mutation during traversal may shift indices and skip elements.", "Mutation under gennemløb kan forskyde indeks og springe elementer over.")),
        authored_item("dm857.m06.assessment.013", ActivityType.CODE_TRACING, ("Traza x, y = (3, 4).", "Trace x, y = (3, 4).", "Gennemgå x, y = (3, 4)."), (("x = 3; y = 4", "x = 3; y = 4", "x = 3; y = 4"),), ("El desempaquetado vincula por posición.", "Unpacking binds by position.", "Udpakning binder efter position.")),
        authored_item("dm857.m06.assessment.014", ActivityType.SHORT_ANSWER, ("Justifica cuándo preferir una tupla a una lista.", "Justify when to prefer a tuple over a list.", "Begrund, hvornår en tuple bør foretrækkes frem for en liste."), (("Cuando el grupo tiene tamaño y roles fijos y no necesita mutación estructural.", "When the group has fixed size and roles and needs no structural mutation.", "Når gruppen har fast størrelse og roller og ikke behøver strukturel mutation."),), ("La tupla comunica intención de estructura fija.", "A tuple communicates fixed-structure intent.", "En tuple kommunikerer intention om fast struktur.")),
    ),
    tutor_support=tutor_support(
        (
            "Listas y tuplas son secuencias ordenadas, pero difieren en mutabilidad. Una lista puede modificarse; una tupla comunica una "
            "agrupación fija. La asignación entre nombres no copia una lista y puede crear aliasing. Las copias superficiales crean un contenedor "
            "exterior nuevo, pero conservan referencias internas. append añade un objeto, extend añade elementos, y métodos como append, extend, "
            "sort y clear suelen retornar None. Recorrer y construir una salida nueva reduce mutaciones accidentales. Las agregaciones deben definir "
            "su comportamiento para colecciones vacías. En listas anidadas, la forma y la identidad de las filas deben validarse; multiplicar una "
            "fila puede crear aliasing. Las tuplas permiten desempaquetado y retornos múltiples. Los ejemplos biomédicos son escenarios didácticos de "
            "programación y no representan protocolos ni recomendaciones clínicas.",
            "Lists and tuples are ordered sequences but differ in mutability. A list may change; a tuple communicates a fixed grouping. Assignment "
            "between names does not copy a list and may create aliasing. Shallow copies create a new outer container while preserving inner references. "
            "append adds one object, extend adds elements, and methods such as append, extend, sort, and clear usually return None. Traversing and building "
            "a new output reduces accidental mutation. Aggregations must define behavior for empty collections. For nested lists, shape and row identity "
            "must be validated; multiplying one row may create aliasing. Tuples support unpacking and multiple returns. Biomedical examples are programming "
            "exercises, not protocols or clinical recommendations.",
            "Lister og tupler er ordnede sekvenser, men adskiller sig i muterbarhed. En liste kan ændres; en tuple kommunikerer en fast gruppering. "
            "Tildeling mellem navne kopierer ikke en liste og kan skabe aliasing. Overfladiske kopier opretter en ny ydre container, men bevarer indre "
            "referencer. append tilføjer ét objekt, extend tilføjer elementer, og metoder som append, extend, sort og clear returnerer normalt None. "
            "Aggregeringer skal definere adfærd for tomme samlinger. Ved indlejrede lister skal form og rækkeidentitet valideres. Biomedicinske eksempler "
            "er programmeringsøvelser og ikke protokoller eller kliniske anbefalinger.",
        ),
        (
            ("Listas y tuplas conservan orden.", "Lists and tuples preserve order.", "Lister og tupler bevarer rækkefølge."),
            ("Las listas son mutables.", "Lists are mutable.", "Lister er muterbare."),
            ("Las tuplas son inmutables.", "Tuples are immutable.", "Tupler er uforanderlige."),
            ("a = b no copia una lista.", "a = b does not copy a list.", "a = b kopierer ikke en liste."),
            ("Una copia superficial comparte objetos internos.", "A shallow copy shares inner objects.", "En overfladisk kopi deler indre objekter."),
            ("append añade un objeto.", "append adds one object.", "append tilføjer ét objekt."),
            ("extend añade elementos.", "extend adds elements.", "extend tilføjer elementer."),
            ("pop elimina y retorna.", "pop removes and returns.", "pop fjerner og returnerer."),
            ("La mayoría de métodos mutadores retorna None.", "Most mutating methods return None.", "De fleste muterende metoder returnerer None."),
            ("zip se detiene con la secuencia más corta.", "zip stops with the shortest sequence.", "zip stopper med den korteste sekvens."),
            ("min y max requieren entrada no vacía.", "min and max require non-empty input.", "min og max kræver ikke-tomt input."),
            ("Una matriz rectangular tiene filas de igual longitud.", "A rectangular matrix has equal-length rows.", "En rektangulær matrix har rækker med samme længde."),
            ("El desempaquetado vincula por posición.", "Unpacking binds by position.", "Udpakning binder efter position."),
            ("Retornar varios valores crea una tupla.", "Returning multiple values creates a tuple.", "Flere returværdier opretter en tuple."),
        ),
        (
            ("Confundir alias con copia.", "Confusing an alias with a copy.", "At forveksle alias med kopi."),
            ("Asignar el resultado de append o sort.", "Assigning the result of append or sort.", "At tildele resultatet af append eller sort."),
            ("Confundir append y extend.", "Confusing append and extend.", "At forveksle append og extend."),
            ("Mutar una lista durante su recorrido.", "Mutating a list during traversal.", "At mutere en liste under gennemløb."),
            ("Suponer que una copia superficial es profunda.", "Assuming a shallow copy is deep.", "At antage, at en overfladisk kopi er dyb."),
            ("Inicializar máximo con cero arbitrariamente.", "Initializing a maximum arbitrarily with zero.", "At initialisere maksimum vilkårligt med nul."),
            ("Ignorar colecciones vacías.", "Ignoring empty collections.", "At ignorere tomme samlinger."),
            ("Suponer que zip exige igual longitud.", "Assuming zip requires equal lengths.", "At antage, at zip kræver samme længde."),
            ("Crear filas con multiplicación y compartir identidad.", "Creating rows by multiplication and sharing identity.", "At oprette rækker med multiplikation og dele identitet."),
            ("Confundir igualdad con identidad.", "Confusing equality with identity.", "At forveksle lighed med identitet."),
            ("Desempaquetar una cantidad incompatible.", "Unpacking an incompatible count.", "At udpakke et inkompatibelt antal."),
            ("Usar una lista cuando el contrato es fijo sin justificarlo.", "Using a list for a fixed contract without justification.", "At bruge en liste til en fast kontrakt uden begrundelse."),
        ),
        (
            ("¿Cuántos elementos contiene la secuencia?", "How many elements does the sequence contain?", "Hvor mange elementer indeholder sekvensen?"),
            ("¿Los nombres apuntan al mismo objeto?", "Do the names refer to the same object?", "Refererer navnene til samme objekt?"),
            ("¿La operación muta o retorna una colección nueva?", "Does the operation mutate or return a new collection?", "Muterer operationen eller returnerer den en ny samling?"),
            ("¿append o extend corresponde al contrato?", "Does append or extend match the contract?", "Matcher append eller extend kontrakten?"),
            ("¿Qué ocurre con entrada vacía?", "What happens with empty input?", "Hvad sker der med tomt input?"),
            ("¿La copia comparte objetos internos?", "Does the copy share inner objects?", "Deler kopien indre objekter?"),
            ("¿Se modifica la lista durante el recorrido?", "Is the list modified during traversal?", "Ændres listen under gennemløb?"),
            ("¿zip descarta elementos?", "Does zip discard elements?", "Kasserer zip elementer?"),
            ("¿La matriz es rectangular?", "Is the matrix rectangular?", "Er matricen rektangulær?"),
            ("¿Las filas son independientes?", "Are the rows independent?", "Er rækkerne uafhængige?"),
            ("¿Cuántos nombres exige el desempaquetado?", "How many names does unpacking require?", "Hvor mange navne kræver udpakning?"),
            ("¿La estructura elegida comunica intención?", "Does the chosen structure communicate intent?", "Kommunikerer den valgte struktur intention?"),
        ),
        (
            ("Distingue mutación y reasignación.", "Distinguishes mutation and reassignment.", "Skelner mellem mutation og gentildeling."),
            ("Traza aliasing correctamente.", "Traces aliasing correctly.", "Gennemgår aliasing korrekt."),
            ("Usa métodos de listas con retornos correctos.", "Uses list methods with correct return behavior.", "Bruger listemetoder med korrekt returadfærd."),
            ("Construye salidas sin mutación accidental.", "Builds outputs without accidental mutation.", "Bygger output uden utilsigtet mutation."),
            ("Gestiona colecciones vacías.", "Handles empty collections.", "Håndterer tomme samlinger."),
            ("Razona sobre copias superficiales.", "Reasons about shallow copies.", "Ræsonnerer om overfladiske kopier."),
            ("Valida formas anidadas.", "Validates nested shapes.", "Validerer indlejrede former."),
            ("Usa tuplas y desempaquetado correctamente.", "Uses tuples and unpacking correctly.", "Bruger tupler og udpakning korrekt."),
            ("Diseña pruebas de identidad y límites.", "Designs identity and boundary tests.", "Designer identitets- og grænsetest."),
            ("Justifica la estructura elegida.", "Justifies the chosen structure.", "Begrunder den valgte struktur."),
        ),
        (
            ("Dar primero una pista.", "Give a hint first.", "Giv først et hint."),
            ("Dibujar referencias al explicar aliasing.", "Describe references explicitly when explaining aliasing.", "Beskriv referencer eksplicit ved forklaring af aliasing."),
            ("No afirmar que append retorna la lista.", "Do not claim append returns the list.", "Påstå ikke, at append returnerer listen."),
            ("Distinguir copia superficial de profunda.", "Distinguish shallow from deep copy.", "Skeln mellem overfladisk og dyb kopi."),
            ("Comprobar el contrato para colecciones vacías.", "Check the contract for empty collections.", "Kontrollér kontrakten for tomme samlinger."),
            ("No ocultar aliasing de filas.", "Do not hide row aliasing.", "Skjul ikke aliasing mellem rækker."),
            ("No introducir NumPy antes de comprender listas anidadas.", "Do not introduce NumPy before nested lists are understood.", "Introducér ikke NumPy før indlejrede lister er forstået."),
            ("No presentar datos didácticos como protocolos clínicos.", "Do not present teaching data as clinical protocols.", "Præsenter ikke undervisningsdata som kliniske protokoller."),
            ("Relacionar pruebas con mutabilidad e identidad.", "Relate tests to mutability and identity.", "Knyt test til muterbarhed og identitet."),
        ),
        (
            "Official DM857 course description, SDU, active version approved in 2025.",
            "Think Python, third edition, chapters on lists, tuples, aliasing, and debugging.",
            "Introduction to Computation and Programming Using Python, third edition, sections on structured types, mutability, and testing.",
        ),
    ),
)

LOCALIZED_OBJECTIVE_QUESTION_BANK_06 = (
    objective_mcq("dm857.m06.bank.001", ("¿Qué estructura es mutable?", "Which structure is mutable?", "Hvilken struktur er muterbar?"), (("list", ("list", "list", "list")), ("tuple", ("tuple", "tuple", "tuple")), ("str", ("str", "str", "str")), ("int", ("int", "int", "int"))), "list", ("Las listas permiten cambiar elementos.", "Lists allow elements to change.", "Lister tillader ændring af elementer.")),
    objective_tf("dm857.m06.bank.002", ("a = b crea una copia de la lista b.", "a = b creates a copy of list b.", "a = b opretter en kopi af listen b."), correct=False, explanation=("La asignación crea otro nombre para el mismo objeto.", "Assignment creates another name for the same object.", "Tildeling opretter et andet navn for samme objekt.")),
    objective_mcq("dm857.m06.bank.003", ("¿Qué añade append([2,3])?", "What does append([2,3]) add?", "Hvad tilføjer append([2,3])?"), (("one_list", ("Una lista como un elemento", "One list as one element", "En liste som ét element")), ("two", ("Dos enteros", "Two integers", "To heltal")), ("none", ("Nada", "Nothing", "Intet")), ("tuple", ("Una tupla", "A tuple", "En tuple"))), "one_list", ("append recibe un objeto.", "append receives one object.", "append modtager ét objekt.")),
    objective_tf("dm857.m06.bank.004", ("extend([2,3]) añade dos elementos.", "extend([2,3]) adds two elements.", "extend([2,3]) tilføjer to elementer."), correct=True, explanation=("extend recorre el iterable.", "extend traverses the iterable.", "extend gennemløber den iterable.")),
    objective_mcq("dm857.m06.bank.005", ("¿Qué retorna append normalmente?", "What does append normally return?", "Hvad returnerer append normalt?"), (("none", ("None", "None", "None")), ("list", ("La lista", "The list", "Listen")), ("item", ("El elemento", "The item", "Elementet")), ("length", ("La longitud", "The length", "Længden"))), "none", ("append muta y retorna None.", "append mutates and returns None.", "append muterer og returnerer None.")),
    objective_tf("dm857.m06.bank.006", ("pop elimina y retorna un elemento.", "pop removes and returns an element.", "pop fjerner og returnerer et element."), correct=True, explanation=("Combina mutación con un valor retornado.", "It combines mutation with a returned value.", "Den kombinerer mutation med en returværdi.")),
    objective_mcq("dm857.m06.bank.007", ("¿Qué crea values[:] ?", "What does values[:] create?", "Hvad opretter values[:]?"), (("shallow", ("Una copia superficial", "A shallow copy", "En overfladisk kopi")), ("alias", ("Un alias", "An alias", "Et alias")), ("deep", ("Siempre copia profunda", "Always a deep copy", "Altid en dyb kopi")), ("tuple", ("Una tupla", "A tuple", "En tuple"))), "shallow", ("El contenedor exterior es nuevo.", "The outer container is new.", "Den ydre container er ny.")),
    objective_tf("dm857.m06.bank.008", ("Una copia superficial duplica recursivamente todos los objetos internos.", "A shallow copy recursively duplicates all inner objects.", "En overfladisk kopi duplikerer rekursivt alle indre objekter."), correct=False, explanation=("Las referencias internas pueden compartirse.", "Inner references may be shared.", "Indre referencer kan deles.")),
    objective_mcq("dm857.m06.bank.009", ("¿Qué compara == para listas?", "What does == compare for lists?", "Hvad sammenligner == for lister?"), (("content", ("Contenido", "Content", "Indhold")), ("identity", ("Identidad", "Identity", "Identitet")), ("memory_only", ("Sólo dirección", "Address only", "Kun adresse")), ("type_only", ("Sólo tipo", "Type only", "Kun type"))), "content", ("is se usa para identidad.", "is is used for identity.", "is bruges til identitet.")),
    objective_tf("dm857.m06.bank.010", ("Dos listas distintas pueden ser iguales.", "Two distinct lists may be equal.", "To forskellige lister kan være lige."), correct=True, explanation=("Pueden tener el mismo contenido y distinta identidad.", "They may have equal content and different identity.", "De kan have samme indhold og forskellig identitet.")),
    objective_mcq("dm857.m06.bank.011", ("¿Qué ocurre con min([])?", "What happens with min([])?", "Hvad sker der med min([])?"), (("value_error", ("ValueError", "ValueError", "ValueError")), ("none", ("None", "None", "None")), ("zero", ("0", "0", "0")), ("false", ("False", "False", "False"))), "value_error", ("No existe elemento mínimo.", "No minimum element exists.", "Der findes intet minimumselement.")),
    objective_tf("dm857.m06.bank.012", ("Un promedio debe definir qué ocurre con lista vacía.", "A mean should define behavior for an empty list.", "Et gennemsnit bør definere adfærd for en tom liste."), correct=True, explanation=("La división por len requiere una política de vacío.", "Division by len requires an empty-input policy.", "Division med len kræver en politik for tomt input.")),
    objective_mcq("dm857.m06.bank.013", ("¿Qué produce enumerate(['a'])?", "What does enumerate(['a']) produce?", "Hvad producerer enumerate(['a'])?"), (("pair", ("(0, 'a')", "(0, 'a')", "(0, 'a')")), ("a_only", ("'a'", "'a'", "'a'")), ("one", ("(1, 'a')", "(1, 'a')", "(1, 'a')")), ("none", ("None", "None", "None"))), "pair", ("enumerate comienza en 0 por defecto.", "enumerate starts at 0 by default.", "enumerate starter ved 0 som standard.")),
    objective_tf("dm857.m06.bank.014", ("zip continúa hasta la secuencia más larga por defecto.", "zip continues to the longest sequence by default.", "zip fortsætter til den længste sekvens som standard."), correct=False, explanation=("Se detiene con la más corta.", "It stops with the shortest.", "Den stopper med den korteste.")),
    objective_mcq("dm857.m06.bank.015", ("¿Qué método elimina la primera coincidencia por valor?", "Which method removes the first matching value?", "Hvilken metode fjerner den første matchende værdi?"), (("remove", ("remove", "remove", "remove")), ("pop", ("pop", "pop", "pop")), ("clear", ("clear", "clear", "clear")), ("extend", ("extend", "extend", "extend"))), "remove", ("remove busca por valor.", "remove searches by value.", "remove søger efter værdi.")),
    objective_tf("dm857.m06.bank.016", ("remove retorna el elemento eliminado.", "remove returns the removed element.", "remove returnerer det fjernede element."), correct=False, explanation=("remove muta y retorna None.", "remove mutates and returns None.", "remove muterer og returnerer None.")),
    objective_mcq("dm857.m06.bank.017", ("¿Cómo se escribe una tupla de un elemento?", "How is a one-element tuple written?", "Hvordan skrives en tuple med ét element?"), (("comma", ("(value,)", "(value,)", "(value,)")), ("plain", ("(value)", "(value)", "(value)")), ("list", ("[value]", "[value]", "[value]")), ("brace", ("{value}", "{value}", "{value}"))), "comma", ("La coma crea la tupla.", "The comma creates the tuple.", "Kommaet opretter tuplen.")),
    objective_tf("dm857.m06.bank.018", ("return a, b retorna una tupla.", "return a, b returns a tuple.", "return a, b returnerer en tuple."), correct=True, explanation=("La coma agrupa ambos valores.", "The comma groups both values.", "Kommaet grupperer begge værdier.")),
    objective_mcq("dm857.m06.bank.019", ("¿Qué exige x, y = values?", "What does x, y = values require?", "Hvad kræver x, y = values?"), (("two", ("Exactamente dos elementos", "Exactly two elements", "Præcis to elementer")), ("one", ("Uno", "One", "Ét")), ("any", ("Cualquier cantidad", "Any count", "Ethvert antal")), ("empty", ("Vacío", "Empty", "Tomt"))), "two", ("El desempaquetado debe coincidir en cantidad.", "Unpacking must match the count.", "Udpakning skal matche antallet.")),
    objective_tf("dm857.m06.bank.020", ("Una tupla puede contener una lista mutable.", "A tuple may contain a mutable list.", "En tuple kan indeholde en muterbar liste."), correct=True, explanation=("La tupla no cambia sus referencias, pero el objeto interno puede mutar.", "The tuple does not change its references, but the inner object may mutate.", "Tuplen ændrer ikke sine referencer, men det indre objekt kan mutere.")),
    objective_mcq("dm857.m06.bank.021", ("¿Qué peligro tiene [[0]*3]*2?", "What is the danger of [[0]*3]*2?", "Hvad er faren ved [[0]*3]*2?"), (("row_alias", ("Filas alias", "Aliased rows", "Alias-rækker")), ("empty", ("Matriz vacía", "Empty matrix", "Tom matrix")), ("tuple", ("Crea tuplas", "Creates tuples", "Opretter tupler")), ("syntax", ("Error de sintaxis", "Syntax error", "Syntaksfejl"))), "row_alias", ("La misma fila se repite por referencia.", "The same row is repeated by reference.", "Samme række gentages ved reference.")),
    objective_tf("dm857.m06.bank.022", ("Una matriz rectangular tiene filas de igual longitud.", "A rectangular matrix has equal-length rows.", "En rektangulær matrix har rækker med samme længde."), correct=True, explanation=("Esa es la forma rectangular esperada.", "That is the expected rectangular shape.", "Det er den forventede rektangulære form.")),
    objective_mcq("dm857.m06.bank.023", ("¿Qué estrategia evita mutar durante recorrido?", "Which strategy avoids mutation during traversal?", "Hvilken strategi undgår mutation under gennemløb?"), (("new_list", ("Construir una lista nueva", "Build a new list", "Byg en ny liste")), ("remove_loop", ("Usar remove en el mismo for", "Use remove in the same for", "Brug remove i samme for")), ("clear", ("Vaciar primero", "Clear first", "Tøm først")), ("alias", ("Crear alias", "Create an alias", "Opret et alias"))), "new_list", ("La entrada permanece estable durante el recorrido.", "Input remains stable during traversal.", "Input forbliver stabilt under gennemløb.")),
    objective_tf("dm857.m06.bank.024", ("Mutar una lista durante su recorrido puede omitir elementos.", "Mutating a list during traversal may skip elements.", "Mutation af en liste under gennemløb kan springe elementer over."), correct=True, explanation=("Los índices y posiciones cambian mientras el iterador avanza.", "Indices and positions change while the iterator advances.", "Indeks og positioner ændres, mens iteratoren bevæger sig.")),
    objective_mcq("dm857.m06.bank.025", ("¿Cuándo es adecuada una tupla?", "When is a tuple appropriate?", "Hvornår er en tuple passende?"), (("fixed", ("Registro fijo sin cambios estructurales", "Fixed record without structural changes", "Fast post uden strukturelle ændringer")), ("growing", ("Colección que crece constantemente", "Collection that constantly grows", "Samling der konstant vokser")), ("remove", ("Datos con eliminaciones frecuentes", "Data with frequent removals", "Data med hyppige fjernelser")), ("append", ("Necesita append", "Needs append", "Behøver append"))), "fixed", ("La tupla comunica estructura fija.", "A tuple communicates fixed structure.", "En tuple kommunikerer fast struktur.")),
    objective_tf("dm857.m06.bank.026", ("La elección entre lista y tupla es sólo estética.", "The choice between list and tuple is only aesthetic.", "Valget mellem liste og tuple er kun æstetisk."), correct=False, explanation=("Comunica mutabilidad y contrato.", "It communicates mutability and contract.", "Det kommunikerer muterbarhed og kontrakt.")),
    objective_mcq("dm857.m06.bank.027", ("¿Qué retorna sorted(values)?", "What does sorted(values) return?", "Hvad returnerer sorted(values)?"), (("new_list", ("Una lista nueva ordenada", "A new sorted list", "En ny sorteret liste")), ("none", ("None", "None", "None")), ("same", ("La misma lista mutada", "The same mutated list", "Den samme muterede liste")), ("tuple", ("Una tupla", "A tuple", "En tuple"))), "new_list", ("sorted no muta el argumento.", "sorted does not mutate the argument.", "sorted ændrer ikke argumentet.")),
    objective_tf("dm857.m06.bank.028", ("list.sort() retorna una lista ordenada.", "list.sort() returns a sorted list.", "list.sort() returnerer en sorteret liste."), correct=False, explanation=("sort muta la lista y retorna None.", "sort mutates the list and returns None.", "sort muterer listen og returnerer None.")),
    objective_mcq("dm857.m06.bank.029", ("¿Qué prueba detecta aliasing?", "Which test detects aliasing?", "Hvilken test opdager aliasing?"), (("mutate_one", ("Mutar mediante un nombre y observar el otro", "Mutate through one name and observe the other", "Mutér gennem ét navn og observer det andet")), ("equal_only", ("Comprobar sólo ==", "Check only ==", "Kontrollér kun ==")), ("print_len", ("Imprimir longitud", "Print length", "Udskriv længde")), ("sort", ("Ordenar", "Sort", "Sortér"))), "mutate_one", ("La mutación compartida revela identidad común.", "Shared mutation reveals common identity.", "Delt mutation afslører fælles identitet.")),
    objective_tf("dm857.m06.bank.030", ("Los valores del módulo son ejemplos didácticos, no protocolos clínicos.", "The module values are teaching examples, not clinical protocols.", "Modulets værdier er undervisningseksempler, ikke kliniske protokoller."), correct=True, explanation=("El módulo enseña estructuras de programación.", "The module teaches programming structures.", "Modulet underviser i programmeringsstrukturer.")),
)


def materialize_module_06_question_bank(locale: AppLocale | str) -> tuple[AssessmentItem, ...]:
    resolved = locale if isinstance(locale, AppLocale) else AppLocale.resolve(locale)
    return tuple(item.materialize(resolved) for item in LOCALIZED_OBJECTIVE_QUESTION_BANK_06)


MODULE_06_SEQUENCES: LearningModule = LOCALIZED_MODULE_06_SEQUENCES.materialize(AppLocale.SPANISH_SPAIN)
OBJECTIVE_QUESTION_BANK_06 = materialize_module_06_question_bank(AppLocale.SPANISH_SPAIN)

__all__ = [
    "LOCALIZED_MODULE_06_SEQUENCES",
    "LOCALIZED_OBJECTIVE_QUESTION_BANK_06",
    "MODULE_06_SEQUENCES",
    "OBJECTIVE_QUESTION_BANK_06",
    "materialize_module_06_question_bank",
]
