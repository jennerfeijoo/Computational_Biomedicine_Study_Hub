"""DM857 module 4: functions, parameters, return values, and decomposition."""

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

LOCALIZED_MODULE_04_FUNCTIONS = LocalizedLearningModule(
    course_code="DM857",
    module_id="dm857.m04",
    title=t(
        "Funciones, parámetros, retorno y descomposición",
        "Functions, parameters, return values, and decomposition",
        "Funktioner, parametre, returværdier og dekomponering",
    ),
    summary=t(
        "Este módulo desarrolla el diseño de funciones pequeñas, comprobables y reutilizables. "
        "Se estudian definición y llamada, parámetros, argumentos, valores predeterminados, "
        "retorno, ámbito local, funciones puras, efectos secundarios, composición, contratos, "
        "documentación, pruebas unitarias y descomposición de problemas.",
        "This module develops the design of small, testable, and reusable functions. It covers "
        "definition and calls, parameters, arguments, default values, return, local scope, pure "
        "functions, side effects, composition, contracts, documentation, unit tests, and problem decomposition.",
        "Dette modul udvikler design af små, testbare og genanvendelige funktioner. Det dækker "
        "definition og kald, parametre, argumenter, standardværdier, returnering, lokalt scope, "
        "rene funktioner, sideeffekter, komposition, kontrakter, dokumentation, enhedstest og dekomponering.",
    ),
    objectives=(
        objective(
            "m04.o1",
            (
                "Definir y llamar funciones con nombres y responsabilidades precisas.",
                "Define and call functions with precise names and responsibilities.",
                "Definere og kalde funktioner med præcise navne og ansvarsområder.",
            ),
        ),
        objective(
            "m04.o2",
            (
                "Distinguir parámetros, argumentos posicionales, nombrados y predeterminados.",
                "Distinguish parameters, positional arguments, keyword arguments, and defaults.",
                "Skelne mellem parametre, positionelle argumenter, nøgleordsargumenter og standardværdier.",
            ),
        ),
        objective(
            "m04.o3",
            (
                "Explicar y aplicar return, incluida la diferencia entre retornar e imprimir.",
                "Explain and apply return, including the difference between returning and printing.",
                "Forklare og anvende return, herunder forskellen mellem at returnere og udskrive.",
            ),
        ),
        objective(
            "m04.o4",
            (
                "Razonar sobre variables locales, ámbito y tiempo de vida.",
                "Reason about local variables, scope, and lifetime.",
                "Ræsonnere om lokale variable, scope og levetid.",
            ),
        ),
        objective(
            "m04.o5",
            (
                "Distinguir funciones puras de funciones con efectos secundarios.",
                "Distinguish pure functions from functions with side effects.",
                "Skelne mellem rene funktioner og funktioner med sideeffekter.",
            ),
        ),
        objective(
            "m04.o6",
            (
                "Descomponer problemas y componer funciones mediante interfaces claras.",
                "Decompose problems and compose functions through clear interfaces.",
                "Dekomponere problemer og sammensætte funktioner gennem klare grænseflader.",
            ),
        ),
        objective(
            "m04.o7",
            (
                "Especificar precondiciones, poscondiciones y docstrings verificables.",
                "Specify verifiable preconditions, postconditions, and docstrings.",
                "Specificere verificerbare forudsætninger, efterbetingelser og docstrings.",
            ),
        ),
        objective(
            "m04.o8",
            (
                "Diseñar pruebas unitarias y depurar errores de interfaz, retorno y ámbito.",
                "Design unit tests and debug interface, return, and scope errors.",
                "Designe enhedstest og fejlfinde grænseflade-, retur- og scopefejl.",
            ),
        ),
    ),
    concepts=(
        concept(
            "definition-call-and-interface",
            (
                "Definición, llamada e interfaz",
                "Definition, call, and interface",
                "Definition, kald og grænseflade",
            ),
            (
                "Una función asigna un nombre a una operación. La definición describe parámetros y cuerpo; "
                "la llamada proporciona argumentos y activa una nueva ejecución del cuerpo. Una interfaz útil "
                "indica qué recibe la función, qué produce y qué supuestos exige. El nombre debe describir una "
                "responsabilidad concreta, no una secuencia vaga de acciones.",
                "A function gives a name to an operation. The definition describes parameters and body; a call "
                "supplies arguments and activates a new execution of the body. A useful interface states what the "
                "function receives, what it produces, and what assumptions it requires. Its name should describe "
                "one concrete responsibility rather than a vague sequence of actions.",
                "En funktion giver et navn til en operation. Definitionen beskriver parametre og krop; et kald "
                "leverer argumenter og starter en ny udførelse af kroppen. En nyttig grænseflade angiver input, "
                "resultat og nødvendige antagelser. Navnet bør beskrive ét konkret ansvar.",
            ),
            (
                (
                    "def crea la función; la llamada la ejecuta.",
                    "def creates the function; a call executes it.",
                    "def opretter funktionen; et kald udfører den.",
                ),
                (
                    "Una función debe tener una responsabilidad principal.",
                    "A function should have one primary responsibility.",
                    "En funktion bør have ét primært ansvar.",
                ),
                (
                    "La interfaz debe poder entenderse sin leer toda la implementación.",
                    "The interface should be understandable without reading the full implementation.",
                    "Grænsefladen bør kunne forstås uden at læse hele implementeringen.",
                ),
            ),
        ),
        concept(
            "parameters-arguments-and-defaults",
            (
                "Parámetros, argumentos y valores predeterminados",
                "Parameters, arguments, and default values",
                "Parametre, argumenter og standardværdier",
            ),
            (
                "Los parámetros son nombres locales definidos en la cabecera; los argumentos son valores entregados "
                "en una llamada. Los argumentos posicionales se asocian por orden y los nombrados por nombre. Un valor "
                "predeterminado debe representar un caso habitual y seguro. Los parámetros obligatorios deben preceder "
                "a los predeterminados, y una llamada no puede proporcionar el mismo parámetro dos veces.",
                "Parameters are local names declared in the header; arguments are values supplied by a call. Positional "
                "arguments bind by order and keyword arguments by name. A default should represent a common and safe case. "
                "Required parameters precede defaulted ones, and a call cannot provide one parameter twice.",
                "Parametre er lokale navne i funktionshovedet; argumenter er værdier i et kald. Positionelle argumenter "
                "bindes efter rækkefølge og nøgleordsargumenter efter navn. En standardværdi bør være et almindeligt og "
                "sikkert tilfælde. Obligatoriske parametre står før parametre med standardværdi.",
            ),
            (
                (
                    "Parámetro pertenece a la definición; argumento pertenece a la llamada.",
                    "A parameter belongs to the definition; an argument belongs to the call.",
                    "En parameter hører til definitionen; et argument hører til kaldet.",
                ),
                (
                    "Los argumentos nombrados mejoran la legibilidad cuando hay varios valores similares.",
                    "Keyword arguments improve readability when several values look similar.",
                    "Nøgleordsargumenter forbedrer læsbarheden, når flere værdier ligner hinanden.",
                ),
                (
                    "Los valores predeterminados se evalúan al definir la función.",
                    "Default values are evaluated when the function is defined.",
                    "Standardværdier evalueres, når funktionen defineres.",
                ),
            ),
        ),
        concept(
            "return-versus-print",
            (
                "Retornar no es imprimir",
                "Returning is not printing",
                "At returnere er ikke at udskrive",
            ),
            (
                "return finaliza la llamada y entrega un valor al código que la realizó. print sólo envía una representación "
                "a la salida estándar y devuelve None. Un valor retornado puede almacenarse, combinarse, probarse o pasarse "
                "a otra función. Si no se ejecuta un return explícito, Python retorna None. El código posterior a un return "
                "ejecutado es inalcanzable dentro de esa llamada.",
                "return ends the call and gives a value to the calling code. print only sends a representation to standard "
                "output and returns None. A returned value can be stored, combined, tested, or passed to another function. "
                "Without an executed explicit return, Python returns None. Code after an executed return is unreachable in that call.",
                "return afslutter kaldet og giver en værdi til den kaldende kode. print sender kun en repræsentation til "
                "standardoutput og returnerer None. En returværdi kan gemmes, kombineres, testes eller sendes videre. Uden "
                "en udført eksplicit return returnerer Python None.",
            ),
            (
                (
                    "return produce datos reutilizables; print produce una salida visible.",
                    "return produces reusable data; print produces visible output.",
                    "return producerer genanvendelige data; print producerer synligt output.",
                ),
                (
                    "Una función puede tener varias rutas de retorno, pero cada ruta debe estar razonada.",
                    "A function may have several return paths, but each path must be reasoned about.",
                    "En funktion kan have flere returveje, men hver vej skal analyseres.",
                ),
                (
                    "None puede revelar que una rama no retornó lo esperado.",
                    "None may reveal that one branch did not return as expected.",
                    "None kan afsløre, at en gren ikke returnerede som forventet.",
                ),
            ),
        ),
        concept(
            "local-scope-and-lifetime",
            (
                "Ámbito local y tiempo de vida",
                "Local scope and lifetime",
                "Lokalt scope og levetid",
            ),
            (
                "Cada llamada crea un espacio local con parámetros y variables propias. Una variable local no está disponible "
                "fuera de la función y deja de ser accesible cuando termina la llamada. Dos llamadas pueden usar el mismo nombre "
                "local sin compartir su estado. Leer datos globales aumenta dependencias ocultas; modificarlos dificulta las pruebas "
                "y debe evitarse salvo que exista una razón arquitectónica explícita.",
                "Each call creates a local space containing its own parameters and variables. A local variable is unavailable "
                "outside the function and becomes inaccessible when the call ends. Two calls may use the same local name without "
                "sharing state. Reading global data adds hidden dependencies; modifying it makes tests harder and should be avoided "
                "unless an explicit architectural reason exists.",
                "Hvert kald opretter et lokalt rum med egne parametre og variable. En lokal variabel er ikke tilgængelig uden for "
                "funktionen og kan ikke tilgås efter kaldet. To kald kan bruge samme lokale navn uden at dele tilstand. Globale data "
                "skaber skjulte afhængigheder og gør test vanskeligere.",
            ),
            (
                (
                    "Los parámetros son variables locales inicializadas por la llamada.",
                    "Parameters are local variables initialized by the call.",
                    "Parametre er lokale variable initialiseret af kaldet.",
                ),
                (
                    "El mismo nombre puede referirse a objetos distintos en ámbitos distintos.",
                    "The same name may refer to different objects in different scopes.",
                    "Det samme navn kan referere til forskellige objekter i forskellige scopes.",
                ),
                (
                    "La dependencia explícita mediante parámetros es preferible a leer globales.",
                    "Explicit dependency through parameters is preferable to reading globals.",
                    "Eksplicit afhængighed gennem parametre er bedre end at læse globale værdier.",
                ),
            ),
        ),
        concept(
            "purity-and-side-effects",
            (
                "Funciones puras y efectos secundarios",
                "Pure functions and side effects",
                "Rene funktioner og sideeffekter",
            ),
            (
                "Una función pura determina su resultado únicamente a partir de sus argumentos y no modifica estado externo. "
                "Esto facilita pruebas, reutilización y razonamiento. Imprimir, escribir archivos, modificar una colección recibida "
                "o cambiar una variable global son efectos secundarios. Los efectos no son siempre incorrectos, pero conviene "
                "concentrarlos en funciones claramente nombradas y separar cálculo de entrada/salida.",
                "A pure function determines its result only from its arguments and does not modify external state. This simplifies "
                "testing, reuse, and reasoning. Printing, writing files, mutating a received collection, or changing a global are "
                "side effects. Effects are not always wrong, but they should be concentrated in clearly named functions and kept "
                "separate from calculation.",
                "En ren funktion bestemmer resultatet udelukkende ud fra argumenterne og ændrer ikke ekstern tilstand. Det gør test, "
                "genbrug og ræsonnement lettere. Udskrivning, filskrivning, mutation af en modtaget samling eller ændring af en global "
                "variabel er sideeffekter. Effekter bør samles i tydeligt navngivne funktioner.",
            ),
            (
                (
                    "La pureza permite repetir una llamada con el mismo resultado.",
                    "Purity allows a call to be repeated with the same result.",
                    "Renhed gør det muligt at gentage et kald med samme resultat.",
                ),
                (
                    "El cálculo y la presentación deben separarse cuando sea posible.",
                    "Calculation and presentation should be separated when possible.",
                    "Beregning og præsentation bør adskilles, når det er muligt.",
                ),
                (
                    "Un efecto secundario debe estar documentado.",
                    "A side effect should be documented.",
                    "En sideeffekt bør dokumenteres.",
                ),
            ),
        ),
        concept(
            "decomposition-and-composition",
            (
                "Descomposición y composición",
                "Decomposition and composition",
                "Dekomponering og komposition",
            ),
            (
                "Descomponer consiste en dividir un problema en responsabilidades con entradas y salidas definidas. Una función "
                "de alto nivel puede coordinar funciones más pequeñas sin duplicar sus detalles. La composición usa el resultado "
                "de una función como argumento de otra. Una buena frontera reduce acoplamiento, evita duplicación y permite probar "
                "cada parte de forma independiente antes de integrar el flujo completo.",
                "Decomposition divides a problem into responsibilities with defined inputs and outputs. A high-level function may "
                "coordinate smaller functions without duplicating their details. Composition passes one function's result into another. "
                "A good boundary reduces coupling, avoids duplication, and allows each part to be tested before integration.",
                "Dekomponering opdeler et problem i ansvarsområder med definerede input og output. En funktion på højt niveau kan "
                "koordinere mindre funktioner uden at duplikere detaljer. Komposition sender resultatet fra én funktion til en anden. "
                "Gode grænser reducerer kobling og gør delene testbare.",
            ),
            (
                (
                    "Cada función debe operar al mismo nivel de abstracción.",
                    "Each function should operate at one level of abstraction.",
                    "Hver funktion bør arbejde på ét abstraktionsniveau.",
                ),
                (
                    "La composición explícita hace visible el flujo de datos.",
                    "Explicit composition makes data flow visible.",
                    "Eksplicit komposition gør datastrømmen synlig.",
                ),
                (
                    "La duplicación suele indicar una función ausente.",
                    "Duplication often indicates a missing function.",
                    "Duplikering peger ofte på en manglende funktion.",
                ),
            ),
        ),
        concept(
            "contracts-and-documentation",
            (
                "Contratos y documentación",
                "Contracts and documentation",
                "Kontrakter og dokumentation",
            ),
            (
                "Una precondición describe lo que debe ser cierto antes de la llamada; una poscondición describe el resultado "
                "garantizado si se cumplen las precondiciones. La docstring debe resumir propósito, parámetros, retorno, errores "
                "esperables y efectos secundarios relevantes. Las comprobaciones de entrada pueden convertir supuestos críticos "
                "en errores explícitos, pero no sustituyen una interfaz bien diseñada.",
                "A precondition states what must hold before a call; a postcondition states what is guaranteed when the preconditions "
                "hold. A docstring should summarize purpose, parameters, return value, expected errors, and relevant side effects. "
                "Input checks can turn critical assumptions into explicit errors, but they do not replace a well-designed interface.",
                "En forudsætning beskriver, hvad der skal gælde før et kald; en efterbetingelse beskriver garantien, når forudsætningerne "
                "er opfyldt. En docstring bør opsummere formål, parametre, returværdi, forventede fejl og relevante sideeffekter. "
                "Inputkontrol gør kritiske antagelser eksplicitte.",
            ),
            (
                (
                    "El contrato describe comportamiento observable, no detalles internos.",
                    "The contract describes observable behavior, not internal details.",
                    "Kontrakten beskriver observerbar adfærd, ikke interne detaljer.",
                ),
                (
                    "Las precondiciones deben poder comprobarse o justificarse.",
                    "Preconditions should be checkable or justifiable.",
                    "Forudsætninger bør kunne kontrolleres eller begrundes.",
                ),
                (
                    "Una docstring no debe repetir línea por línea el código.",
                    "A docstring should not repeat the code line by line.",
                    "En docstring bør ikke gentage koden linje for linje.",
                ),
            ),
        ),
        concept(
            "unit-testing-and-debugging",
            (
                "Pruebas unitarias y depuración",
                "Unit testing and debugging",
                "Enhedstest og fejlfinding",
            ),
            (
                "Una prueba unitaria llama a una función con una entrada controlada y compara el valor retornado con un resultado "
                "esperado. Deben cubrir casos normales, límites, entradas inválidas y rutas de retorno. Cuando falla una prueba, conviene "
                "aislar si el defecto pertenece al contrato, a la llamada, al cálculo, al tipo retornado o a una dependencia externa. "
                "Las funciones pequeñas reducen el espacio de búsqueda durante la depuración.",
                "A unit test calls a function with controlled input and compares the returned value with an expected result. Tests "
                "should cover normal cases, boundaries, invalid input, and return paths. When a test fails, isolate whether the defect "
                "belongs to the contract, call, calculation, returned type, or an external dependency. Small functions reduce the search space.",
                "En enhedstest kalder en funktion med kontrolleret input og sammenligner returværdien med et forventet resultat. "
                "Test bør dække normale tilfælde, grænser, ugyldigt input og returveje. Ved fejl isoleres kontrakt, kald, beregning, "
                "returtype eller ekstern afhængighed. Små funktioner gør fejlfinding lettere.",
            ),
            (
                (
                    "Las pruebas deben comprobar valores retornados, no texto impreso accidentalmente.",
                    "Tests should check returned values, not accidentally printed text.",
                    "Test bør kontrollere returværdier, ikke utilsigtet udskrevet tekst.",
                ),
                (
                    "Cada rama de retorno necesita al menos un caso representativo.",
                    "Each return branch needs at least one representative case.",
                    "Hver returgren behøver mindst ét repræsentativt tilfælde.",
                ),
                (
                    "Una prueba fallida debe producir información diagnóstica específica.",
                    "A failing test should produce specific diagnostic information.",
                    "En fejlet test bør give specifik diagnostisk information.",
                ),
            ),
        ),
    ),
    worked_examples=(
        example(
            "m04.e1",
            ("Conversión pura de unidades", "Pure unit conversion", "Ren enhedskonvertering"),
            (
                "Convierte una temperatura Celsius a kelvin y reutiliza el resultado.",
                "Convert a Celsius temperature to kelvin and reuse the result.",
                "Konvertér en Celsius-temperatur til kelvin og genbrug resultatet.",
            ),
            (
                (
                    "La entrada y la salida son numéricas; no se necesita entrada/salida dentro de la función.",
                    "Input and output are numeric; no input/output is needed inside the function.",
                    "Input og output er numeriske; funktionen behøver ingen ind- eller udlæsning.",
                ),
                (
                    "La función retorna el valor para que la llamada decida cómo utilizarlo.",
                    "The function returns the value so the caller decides how to use it.",
                    "Funktionen returnerer værdien, så den kaldende kode bestemmer anvendelsen.",
                ),
            ),
            "def celsius_to_kelvin(celsius: float) -> float:\n    return celsius + 273.15\n\nvalue = celsius_to_kelvin(20.0)\nprint(round(value, 2))",
            "293.15",
            (
                "La función es pura: el mismo argumento produce el mismo retorno y no modifica estado externo.",
                "The function is pure: the same argument produces the same return value and changes no external state.",
                "Funktionen er ren: samme argument giver samme returværdi uden at ændre ekstern tilstand.",
            ),
        ),
        example(
            "m04.e2",
            (
                "Parámetro predeterminado y argumento nombrado",
                "Default parameter and keyword argument",
                "Standardparameter og nøgleordsargument",
            ),
            (
                "Redondea una medición con una precisión configurable.",
                "Round a measurement with configurable precision.",
                "Afrund en måling med konfigurerbar præcision.",
            ),
            (
                (
                    "Dos decimales representan el caso habitual del ejemplo.",
                    "Two decimal places represent the common case in the example.",
                    "To decimaler repræsenterer det almindelige tilfælde i eksemplet.",
                ),
                (
                    "El argumento nombrado hace explícita una precisión distinta.",
                    "The keyword argument makes a different precision explicit.",
                    "Nøgleordsargumentet gør en anden præcision eksplicit.",
                ),
            ),
            'def format_measurement(value: float, digits: int = 2) -> str:\n    return f"{value:.{digits}f}"\n\nprint(format_measurement(12.3456))\nprint(format_measurement(12.3456, digits=3))',
            "12.35\n12.346",
            (
                "El valor predeterminado reduce ruido en llamadas habituales y el argumento nombrado evita ambigüedad.",
                "The default reduces noise in common calls and the keyword argument avoids ambiguity.",
                "Standardværdien reducerer støj i almindelige kald, og nøgleordsargumentet undgår tvetydighed.",
            ),
        ),
        example(
            "m04.e3",
            (
                "Retorno temprano para validar",
                "Early return for validation",
                "Tidlig returnering til validering",
            ),
            (
                "Clasifica una cadena como identificador no vacío o inválido.",
                "Classify a string as a non-empty identifier or invalid.",
                "Klassificér en streng som et ikke-tomt id eller ugyldigt.",
            ),
            (
                (
                    "Primero se trata la condición inválida.",
                    "The invalid condition is handled first.",
                    "Den ugyldige betingelse håndteres først.",
                ),
                (
                    "Cada ruta retorna un bool explícito.",
                    "Each path returns an explicit bool.",
                    "Hver vej returnerer en eksplicit bool.",
                ),
            ),
            'def has_identifier(text: str) -> bool:\n    if not text.strip():\n        return False\n    return True\n\nprint(has_identifier("  "))\nprint(has_identifier("sample_04"))',
            "False\nTrue",
            (
                "El retorno temprano mantiene plana la estructura y evita una rama else innecesaria.",
                "The early return keeps the structure flat and avoids an unnecessary else branch.",
                "Den tidlige returnering holder strukturen flad og undgår en unødvendig else-gren.",
            ),
        ),
        example(
            "m04.e4",
            (
                "Composición de funciones",
                "Function composition",
                "Funktionskomposition",
            ),
            (
                "Normaliza una fracción y después conviértela en porcentaje.",
                "Normalize a fraction and then convert it into a percentage.",
                "Normalisér en brøk og konvertér den derefter til procent.",
            ),
            (
                (
                    "La primera función limita el valor al intervalo de trabajo didáctico.",
                    "The first function limits the value to the didactic working interval.",
                    "Den første funktion begrænser værdien til det didaktiske arbejdsinterval.",
                ),
                (
                    "La segunda transforma una fracción ya normalizada.",
                    "The second transforms an already normalized fraction.",
                    "Den anden transformerer en allerede normaliseret brøk.",
                ),
            ),
            "def clamp_fraction(value: float) -> float:\n    return max(0.0, min(1.0, value))\n\ndef to_percent(fraction: float) -> float:\n    return fraction * 100.0\n\nprint(to_percent(clamp_fraction(1.2)))",
            "100.0",
            (
                "La composición separa dos responsabilidades y hace explícito el flujo de datos.",
                "Composition separates two responsibilities and makes the data flow explicit.",
                "Komposition adskiller to ansvarsområder og gør datastrømmen eksplicit.",
            ),
        ),
        example(
            "m04.e5",
            (
                "Prueba unitaria de rutas de retorno",
                "Unit test for return paths",
                "Enhedstest af returveje",
            ),
            (
                "Comprueba una función que evita dividir entre cero.",
                "Test a function that avoids division by zero.",
                "Test en funktion, der undgår division med nul.",
            ),
            (
                (
                    "Se necesita un caso normal y un caso para denominador cero.",
                    "A normal case and a zero-denominator case are required.",
                    "Der kræves et normalt tilfælde og et tilfælde med nævner nul.",
                ),
                (
                    "Las aserciones comparan valores retornados.",
                    "Assertions compare returned values.",
                    "Assertions sammenligner returværdier.",
                ),
            ),
            'def safe_ratio(numerator: float, denominator: float) -> float | None:\n    if denominator == 0:\n        return None\n    return numerator / denominator\n\nassert safe_ratio(6, 3) == 2\nassert safe_ratio(6, 0) is None\nprint("tests passed")',
            "tests passed",
            (
                "Cada ruta de retorno queda cubierta por una prueba específica.",
                "Each return path is covered by a specific test.",
                "Hver returvej dækkes af en specifik test.",
            ),
        ),
    ),
    practice_exercises=(
        practice(
            "m04.p01",
            ActivityType.CODE_TRACING,
            (
                "Traza dos llamadas a add_offset y registra el valor local result en cada llamada.",
                "Trace two calls to add_offset and record the local value result in each call.",
                "Gennemgå to kald til add_offset og registrér den lokale værdi result i hvert kald.",
            ),
            (
                (
                    "Cada llamada crea un ámbito local nuevo.",
                    "Each call creates a new local scope.",
                    "Hvert kald opretter et nyt lokalt scope.",
                ),
                (
                    "Sustituye primero el parámetro value por el argumento.",
                    "First substitute the argument for parameter value.",
                    "Erstat først parameteren value med argumentet.",
                ),
            ),
            (
                "Primera llamada: result = 7. Segunda llamada: result = 12. Los dos nombres locales no comparten estado.",
                "First call: result = 7. Second call: result = 12. The two local names do not share state.",
                "Første kald: result = 7. Andet kald: result = 12. De to lokale navne deler ikke tilstand.",
            ),
            (
                "El ejercicio demuestra que el ámbito local se crea por llamada.",
                "The exercise demonstrates that local scope is created per call.",
                "Øvelsen viser, at lokalt scope oprettes for hvert kald.",
            ),
            "def add_offset(value: int, offset: int = 2) -> int:\n    result = value + offset\n    return result\n\na = add_offset(5)\nb = add_offset(10)",
        ),
        practice(
            "m04.p02",
            ActivityType.CODE_COMPLETION,
            (
                "Completa una función square que retorne el cuadrado sin imprimirlo.",
                "Complete a square function that returns the square without printing it.",
                "Færdiggør en square-funktion, der returnerer kvadratet uden at udskrive det.",
            ),
            (
                ("Usa return.", "Use return.", "Brug return."),
                (
                    "El resultado debe poder asignarse a una variable.",
                    "The result must be assignable to a variable.",
                    "Resultatet skal kunne tildeles en variabel.",
                ),
            ),
            ("return value * value", "return value * value", "return value * value"),
            (
                "Retornar permite reutilizar el resultado en otra expresión.",
                "Returning allows the result to be reused in another expression.",
                "Returnering gør det muligt at genbruge resultatet i et andet udtryk.",
            ),
            "def square(value: float) -> float:\n    # completa aquí",
        ),
        practice(
            "m04.p03",
            ActivityType.DEBUGGING,
            (
                "Corrige una función que imprime el promedio pero retorna None.",
                "Fix a function that prints the mean but returns None.",
                "Ret en funktion, der udskriver gennemsnittet, men returnerer None.",
            ),
            (
                (
                    "La llamada necesita utilizar el valor después.",
                    "The caller needs to use the value afterwards.",
                    "Den kaldende kode skal bruge værdien bagefter.",
                ),
                (
                    "Sustituye print por return dentro de la función.",
                    "Replace print with return inside the function.",
                    "Erstat print med return inde i funktionen.",
                ),
            ),
            (
                "def mean_two(a, b):\n    return (a + b) / 2",
                "def mean_two(a, b):\n    return (a + b) / 2",
                "def mean_two(a, b):\n    return (a + b) / 2",
            ),
            (
                "print muestra texto; return entrega el valor a la llamada.",
                "print displays text; return gives the value to the caller.",
                "print viser tekst; return giver værdien til den kaldende kode.",
            ),
            "def mean_two(a, b):\n    print((a + b) / 2)\n\nresult = mean_two(4, 8)",
        ),
        practice(
            "m04.p04",
            ActivityType.SHORT_ANSWER,
            (
                "Explica por qué leer una variable global reduce la capacidad de probar una función.",
                "Explain why reading a global variable reduces function testability.",
                "Forklar, hvorfor læsning af en global variabel reducerer funktionens testbarhed.",
            ),
            (
                (
                    "Piensa en dependencias que no aparecen en los parámetros.",
                    "Think about dependencies absent from the parameters.",
                    "Tænk på afhængigheder, der ikke fremgår af parametrene.",
                ),
                (
                    "Compara llamadas idénticas bajo estados globales distintos.",
                    "Compare identical calls under different global states.",
                    "Sammenlign identiske kald under forskellige globale tilstande.",
                ),
            ),
            (
                "La función tiene una dependencia oculta: la misma llamada puede producir resultados distintos si cambia el estado global. "
                "La prueba debe configurar y restaurar ese estado, por lo que es menos aislada.",
                "The function has a hidden dependency: the same call may produce different results when global state changes. The test must "
                "configure and restore that state, so it is less isolated.",
                "Funktionen har en skjult afhængighed: samme kald kan give forskellige resultater, hvis global tilstand ændres. Testen skal "
                "opsætte og gendanne tilstanden og bliver derfor mindre isoleret.",
            ),
            (
                "Las dependencias explícitas mediante parámetros facilitan pruebas reproducibles.",
                "Explicit dependencies through parameters support reproducible tests.",
                "Eksplicitte afhængigheder gennem parametre gør test reproducerbare.",
            ),
        ),
        practice(
            "m04.p05",
            ActivityType.FILL_IN_THE_BLANK,
            (
                "Completa: una variable definida dentro de una función suele tener ámbito ____.",
                "Complete: a variable defined inside a function usually has ____ scope.",
                "Udfyld: en variabel defineret inde i en funktion har normalt ____ scope.",
            ),
            (
                (
                    "Piensa en local frente a global.",
                    "Think local versus global.",
                    "Tænk lokalt versus globalt.",
                ),
            ),
            ("local", "local", "lokalt"),
            (
                "El nombre sólo está disponible dentro del ámbito de la llamada.",
                "The name is available only within the call's scope.",
                "Navnet er kun tilgængeligt i kaldets scope.",
            ),
        ),
        practice(
            "m04.p06",
            ActivityType.ORDERING,
            (
                "Ordena el diseño: definir contrato, elegir parámetros, implementar, probar casos.",
                "Order the design steps: define contract, choose parameters, implement, test cases.",
                "Ordén designtrinnene: definér kontrakt, vælg parametre, implementér, test tilfælde.",
            ),
            (
                (
                    "El comportamiento esperado debe fijarse antes del código.",
                    "Expected behavior should be fixed before code.",
                    "Forventet adfærd bør fastlægges før koden.",
                ),
                (
                    "Las pruebas verifican el contrato después de implementar.",
                    "Tests verify the contract after implementation.",
                    "Test verificerer kontrakten efter implementering.",
                ),
            ),
            (
                "1. Definir contrato. 2. Elegir parámetros y retorno. 3. Implementar. 4. Probar casos normales, límite e inválidos.",
                "1. Define contract. 2. Choose parameters and return. 3. Implement. 4. Test normal, boundary, and invalid cases.",
                "1. Definér kontrakt. 2. Vælg parametre og retur. 3. Implementér. 4. Test normale, grænse- og ugyldige tilfælde.",
            ),
            (
                "El orden reduce el riesgo de escribir una interfaz que no corresponde al problema.",
                "The order reduces the risk of writing an interface that does not match the problem.",
                "Rækkefølgen reducerer risikoen for en grænseflade, der ikke matcher problemet.",
            ),
        ),
        practice(
            "m04.p07",
            ActivityType.CODE_COMPLETION,
            (
                'Añade un valor predeterminado separator="," a una función join_pair.',
                'Add a default value separator="," to a join_pair function.',
                'Tilføj standardværdien separator="," til funktionen join_pair.',
            ),
            (
                (
                    "El parámetro obligatorio debe aparecer antes del predeterminado.",
                    "Required parameters must appear before the defaulted parameter.",
                    "Obligatoriske parametre skal stå før parameteren med standardværdi.",
                ),
                (
                    "La función debe retornar una cadena.",
                    "The function must return a string.",
                    "Funktionen skal returnere en streng.",
                ),
            ),
            (
                'def join_pair(left: str, right: str, separator: str = ",") -> str:\n    return left + separator + right',
                'def join_pair(left: str, right: str, separator: str = ",") -> str:\n    return left + separator + right',
                'def join_pair(left: str, right: str, separator: str = ",") -> str:\n    return left + separator + right',
            ),
            (
                "El valor predeterminado se usa cuando la llamada omite separator.",
                "The default is used when the call omits separator.",
                "Standardværdien bruges, når kaldet udelader separator.",
            ),
            "def join_pair(left: str, right: str):\n    pass",
        ),
        practice(
            "m04.p08",
            ActivityType.ORAL_EXPLANATION,
            (
                "Explica cómo una función pura reduce la incertidumbre durante la depuración.",
                "Explain how a pure function reduces uncertainty during debugging.",
                "Forklar, hvordan en ren funktion reducerer usikkerhed under fejlfinding.",
            ),
            (
                (
                    "Relaciona argumentos iguales con resultados iguales.",
                    "Relate equal arguments to equal results.",
                    "Knyt ens argumenter til ens resultater.",
                ),
                (
                    "Menciona la ausencia de estado externo modificado.",
                    "Mention the absence of modified external state.",
                    "Nævn fraværet af ændret ekstern tilstand.",
                ),
            ),
            (
                "Una función pura depende sólo de sus argumentos y no modifica estado externo. Por tanto, un fallo puede investigarse "
                "reproduciendo la misma entrada sin preparar otras dependencias ocultas.",
                "A pure function depends only on its arguments and changes no external state. A failure can therefore be investigated by "
                "reproducing the same input without preparing hidden dependencies.",
                "En ren funktion afhænger kun af sine argumenter og ændrer ikke ekstern tilstand. En fejl kan derfor undersøges ved at "
                "gentage samme input uden skjulte afhængigheder.",
            ),
            (
                "La pureza no garantiza que el cálculo sea correcto, pero facilita aislarlo.",
                "Purity does not guarantee a correct calculation, but it makes isolation easier.",
                "Renhed garanterer ikke korrekt beregning, men gør isolering lettere.",
            ),
        ),
        practice(
            "m04.p09",
            ActivityType.DEBUGGING,
            (
                "Detecta la ruta que retorna None en una función con if.",
                "Find the path that returns None in a function containing if.",
                "Find den vej, der returnerer None i en funktion med if.",
            ),
            (
                (
                    "Comprueba qué ocurre cuando value no es positivo.",
                    "Check what happens when value is not positive.",
                    "Kontrollér, hvad der sker, når value ikke er positiv.",
                ),
                (
                    "Toda ruta debe terminar con un retorno coherente.",
                    "Every path should end with a coherent return.",
                    "Hver vej bør slutte med en sammenhængende returværdi.",
                ),
            ),
            (
                "Añadir return 0 después del if, o usar una rama else explícita.",
                "Add return 0 after the if, or use an explicit else branch.",
                "Tilføj return 0 efter if, eller brug en eksplicit else-gren.",
            ),
            (
                "Sin retorno ejecutado, Python devuelve None.",
                "Without an executed return, Python returns None.",
                "Uden en udført return returnerer Python None.",
            ),
            "def positive_or_zero(value: int) -> int:\n    if value > 0:\n        return value",
        ),
        practice(
            "m04.p10",
            ActivityType.SHORT_ANSWER,
            (
                "Propón una precondición y una poscondición para reciprocal(value).",
                "Propose a precondition and a postcondition for reciprocal(value).",
                "Foreslå en forudsætning og en efterbetingelse for reciprocal(value).",
            ),
            (
                (
                    "El denominador no puede ser cero.",
                    "The denominator cannot be zero.",
                    "Nævneren må ikke være nul.",
                ),
                (
                    "Describe la relación entre entrada y retorno.",
                    "Describe the relation between input and return value.",
                    "Beskriv forholdet mellem input og returværdi.",
                ),
            ),
            (
                "Precondición: value != 0. Poscondición: el retorno r satisface r * value == 1 dentro de la precisión numérica esperada.",
                "Precondition: value != 0. Postcondition: return value r satisfies r * value == 1 within expected numeric precision.",
                "Forudsætning: value != 0. Efterbetingelse: returværdien r opfylder r * value == 1 inden for forventet numerisk præcision.",
            ),
            (
                "El contrato especifica comportamiento observable y una restricción de entrada.",
                "The contract specifies observable behavior and an input restriction.",
                "Kontrakten specificerer observerbar adfærd og en inputbegrænsning.",
            ),
        ),
        practice(
            "m04.p11",
            ActivityType.DATA_INTERPRETATION,
            (
                "Una prueba esperaba 4.0 y recibió None. Enumera dos causas plausibles en la función.",
                "A test expected 4.0 and received None. List two plausible causes in the function.",
                "En test forventede 4.0 og modtog None. Angiv to sandsynlige årsager i funktionen.",
            ),
            (
                (
                    "Distingue imprimir de retornar.",
                    "Distinguish printing from returning.",
                    "Skel mellem udskrivning og returnering.",
                ),
                (
                    "Revisa rutas condicionales sin return.",
                    "Inspect conditional paths without return.",
                    "Undersøg betingede veje uden return.",
                ),
            ),
            (
                "La función podría imprimir 4.0 en lugar de retornarlo, o podría alcanzar una rama sin return explícito.",
                "The function may print 4.0 instead of returning it, or it may reach a branch without an explicit return.",
                "Funktionen kan udskrive 4.0 i stedet for at returnere det, eller nå en gren uden eksplicit return.",
            ),
            (
                "Ambas causas producen None para la llamada aunque la consola pueda mostrar un número.",
                "Both causes produce None for the call even if the console displays a number.",
                "Begge årsager giver None fra kaldet, selv om konsollen kan vise et tal.",
            ),
        ),
        practice(
            "m04.p12",
            ActivityType.PIPELINE_DESIGN,
            (
                "Descompón un flujo que limpia un identificador, lo valida y genera una etiqueta.",
                "Decompose a flow that cleans an identifier, validates it, and creates a label.",
                "Dekomponér et flow, der renser et id, validerer det og opretter en etiket.",
            ),
            (
                (
                    "Propón una función por responsabilidad.",
                    "Propose one function per responsibility.",
                    "Foreslå én funktion pr. ansvarsområde.",
                ),
                (
                    "Haz explícito qué retorna cada función.",
                    "Make each function's return value explicit.",
                    "Gør hver funktions returværdi eksplicit.",
                ),
            ),
            (
                "clean_identifier(text) -> str; is_valid_identifier(cleaned) -> bool; build_label(cleaned) -> str; process_identifier(text) "
                "coordina las tres y decide qué hacer si la validación falla.",
                "clean_identifier(text) -> str; is_valid_identifier(cleaned) -> bool; build_label(cleaned) -> str; process_identifier(text) "
                "coordinates the three and decides what to do when validation fails.",
                "clean_identifier(text) -> str; is_valid_identifier(cleaned) -> bool; build_label(cleaned) -> str; process_identifier(text) "
                "koordinerer de tre og beslutter, hvad der sker ved mislykket validering.",
            ),
            (
                "La descomposición separa transformación, decisión y presentación.",
                "The decomposition separates transformation, decision, and presentation.",
                "Dekomponeringen adskiller transformation, beslutning og præsentation.",
            ),
        ),
    ),
    assessment_items=(
        authored_item(
            "dm857.m04.assessment.001",
            ActivityType.CODE_TRACING,
            (
                "Predice result y el valor final de x al ejecutar una función con parámetro local.",
                "Predict result and the final value of x when a function uses a local parameter.",
                "Forudsig result og den endelige værdi af x, når en funktion bruger en lokal parameter.",
            ),
            (("result = 8; x = 3", "result = 8; x = 3", "result = 8; x = 3"),),
            (
                "Modificar el nombre local value no reasigna x en el ámbito de la llamada.",
                "Reassigning local name value does not reassign x in the caller's scope.",
                "Gentildeling af det lokale navn value gentildeler ikke x i det kaldende scope.",
            ),
            rubric=(
                (
                    "Traza ámbitos por separado.",
                    "Traces scopes separately.",
                    "Gennemgår scopes separat.",
                ),
            ),
        ),
        authored_item(
            "dm857.m04.assessment.002",
            ActivityType.MULTIPLE_SELECT,
            (
                "Selecciona propiedades de una función pura.",
                "Select properties of a pure function.",
                "Vælg egenskaber ved en ren funktion.",
            ),
            (),
            (
                "Una función pura depende de argumentos y no modifica estado externo.",
                "A pure function depends on arguments and does not modify external state.",
                "En ren funktion afhænger af argumenter og ændrer ikke ekstern tilstand.",
            ),
            options=(
                (
                    "same_input",
                    (
                        "Mismo input, mismo resultado",
                        "Same input, same result",
                        "Samme input, samme resultat",
                    ),
                ),
                (
                    "no_external_mutation",
                    (
                        "No modifica estado externo",
                        "Does not mutate external state",
                        "Ændrer ikke ekstern tilstand",
                    ),
                ),
                ("must_print", ("Siempre imprime", "Always prints", "Udskriver altid")),
                (
                    "must_global",
                    ("Debe leer una global", "Must read a global", "Skal læse en global variabel"),
                ),
            ),
            correct_option_ids=("same_input", "no_external_mutation"),
        ),
        authored_item(
            "dm857.m04.assessment.003",
            ActivityType.DEBUGGING,
            (
                "Corrige una llamada que proporciona el parámetro digits dos veces.",
                "Fix a call that supplies parameter digits twice.",
                "Ret et kald, der leverer parameteren digits to gange.",
            ),
            (
                (
                    "Usar sólo format_value(3.2, digits=3).",
                    "Use only format_value(3.2, digits=3).",
                    "Brug kun format_value(3.2, digits=3).",
                ),
            ),
            (
                "Un parámetro no puede recibir simultáneamente un argumento posicional y otro nombrado.",
                "A parameter cannot receive both a positional and a keyword argument.",
                "En parameter kan ikke modtage både et positionelt argument og et nøgleordsargument.",
            ),
        ),
        authored_item(
            "dm857.m04.assessment.004",
            ActivityType.FILL_IN_THE_BLANK,
            (
                "Completa: si ninguna sentencia return se ejecuta, la llamada produce ____.",
                "Complete: if no return statement executes, the call produces ____.",
                "Udfyld: hvis ingen return-sætning udføres, producerer kaldet ____.",
            ),
            (("None", "None", "None"),),
            (
                "Python retorna None implícitamente.",
                "Python implicitly returns None.",
                "Python returnerer implicit None.",
            ),
        ),
        authored_item(
            "dm857.m04.assessment.005",
            ActivityType.MATCHING,
            (
                "Relaciona término e interpretación.",
                "Match each term to its interpretation.",
                "Match hvert begreb med dets fortolkning.",
            ),
            (),
            (
                "Parámetro-definición; argumento-llamada; precondición-antes; poscondición-después.",
                "Parameter-definition; argument-call; precondition-before; postcondition-after.",
                "Parameter-definition; argument-kald; forudsætning-før; efterbetingelse-efter.",
            ),
            options=(
                (
                    "parameter_definition",
                    ("Parámetro → definición", "Parameter → definition", "Parameter → definition"),
                ),
                ("argument_call", ("Argumento → llamada", "Argument → call", "Argument → kald")),
                (
                    "pre_before",
                    ("Precondición → antes", "Precondition → before", "Forudsætning → før"),
                ),
                (
                    "post_after",
                    ("Poscondición → después", "Postcondition → after", "Efterbetingelse → efter"),
                ),
            ),
            correct_option_ids=(
                "parameter_definition",
                "argument_call",
                "pre_before",
                "post_after",
            ),
        ),
        authored_item(
            "dm857.m04.assessment.006",
            ActivityType.ORDERING,
            (
                "Ordena los pasos de una llamada de función.",
                "Order the steps of a function call.",
                "Ordén trinnene i et funktionskald.",
            ),
            (),
            (
                "Evaluar argumentos, vincular parámetros, ejecutar cuerpo, entregar retorno.",
                "Evaluate arguments, bind parameters, execute body, deliver return value.",
                "Evaluér argumenter, bind parametre, udfør kroppen, lever returværdi.",
            ),
            options=(
                ("evaluate", ("Evaluar argumentos", "Evaluate arguments", "Evaluér argumenter")),
                ("bind", ("Vincular parámetros", "Bind parameters", "Bind parametre")),
                ("execute", ("Ejecutar cuerpo", "Execute body", "Udfør kroppen")),
                ("return", ("Entregar retorno", "Deliver return value", "Lever returværdi")),
            ),
            correct_option_ids=("evaluate", "bind", "execute", "return"),
        ),
        authored_item(
            "dm857.m04.assessment.007",
            ActivityType.CODE_COMPLETION,
            (
                "Escribe una función is_even(value) que retorne bool.",
                "Write an is_even(value) function returning bool.",
                "Skriv en is_even(value)-funktion, der returnerer bool.",
            ),
            (
                (
                    "def is_even(value):\n    return value % 2 == 0",
                    "def is_even(value):\n    return value % 2 == 0",
                    "def is_even(value):\n    return value % 2 == 0",
                ),
            ),
            (
                "La comparación ya produce un bool y puede retornarse directamente.",
                "The comparison already produces a bool and can be returned directly.",
                "Sammenligningen producerer allerede en bool og kan returneres direkte.",
            ),
            rubric=(
                (
                    "Retorna bool sin imprimir.",
                    "Returns bool without printing.",
                    "Returnerer bool uden udskrivning.",
                ),
            ),
        ),
        authored_item(
            "dm857.m04.assessment.008",
            ActivityType.SHORT_ANSWER,
            (
                "Distingue contrato de implementación en una función.",
                "Distinguish a function's contract from its implementation.",
                "Skeln mellem en funktions kontrakt og implementering.",
            ),
            (
                (
                    "El contrato describe comportamiento observable; la implementación describe cómo se obtiene.",
                    "The contract describes observable behavior; implementation describes how it is obtained.",
                    "Kontrakten beskriver observerbar adfærd; implementeringen beskriver, hvordan den opnås.",
                ),
            ),
            (
                "Esta separación permite cambiar el algoritmo sin alterar a los llamadores.",
                "This separation allows the algorithm to change without altering callers.",
                "Adskillelsen gør det muligt at ændre algoritmen uden at ændre den kaldende kode.",
            ),
        ),
        authored_item(
            "dm857.m04.assessment.009",
            ActivityType.DATA_INTERPRETATION,
            (
                "Interpreta por qué tres pruebas pasan y una entrada vacía falla.",
                "Interpret why three tests pass and an empty input fails.",
                "Fortolk, hvorfor tre test består, og et tomt input fejler.",
            ),
            (
                (
                    "Falta cubrir o implementar la precondición para entrada vacía.",
                    "The precondition for empty input is missing from tests or implementation.",
                    "Forudsætningen for tomt input mangler i test eller implementering.",
                ),
            ),
            (
                "Un conjunto de pruebas puede ser verde y seguir omitiendo una frontera importante.",
                "A test set can be green while still omitting an important boundary.",
                "Et testsæt kan være grønt og stadig udelade en vigtig grænse.",
            ),
        ),
        authored_item(
            "dm857.m04.assessment.010",
            ActivityType.ORAL_EXPLANATION,
            (
                "Explica cuándo un efecto secundario es justificable.",
                "Explain when a side effect is justified.",
                "Forklar, hvornår en sideeffekt er berettiget.",
            ),
            (
                (
                    "Cuando la responsabilidad exige interactuar con estado externo y el efecto está aislado y documentado.",
                    "When the responsibility requires interaction with external state and the effect is isolated and documented.",
                    "Når ansvaret kræver interaktion med ekstern tilstand, og effekten er isoleret og dokumenteret.",
                ),
            ),
            (
                "Entrada/salida y persistencia requieren efectos, pero deben quedar en fronteras explícitas.",
                "Input/output and persistence require effects, but they should remain at explicit boundaries.",
                "Input/output og persistens kræver effekter, men de bør ligge ved eksplicitte grænser.",
            ),
        ),
        authored_item(
            "dm857.m04.assessment.011",
            ActivityType.PIPELINE_DESIGN,
            (
                "Diseña funciones para validar, transformar y resumir una medición didáctica.",
                "Design functions to validate, transform, and summarize a didactic measurement.",
                "Design funktioner til at validere, transformere og opsummere en didaktisk måling.",
            ),
            (
                (
                    "validate_measurement, transform_measurement, summarize_measurement y una función coordinadora.",
                    "validate_measurement, transform_measurement, summarize_measurement, and one coordinating function.",
                    "validate_measurement, transform_measurement, summarize_measurement og en koordinerende funktion.",
                ),
            ),
            (
                "Separar responsabilidades permite probar cada contrato.",
                "Separating responsibilities allows each contract to be tested.",
                "Adskilte ansvarsområder gør hver kontrakt testbar.",
            ),
            rubric=(
                (
                    "Define entradas y retornos.",
                    "Defines inputs and returns.",
                    "Definerer input og returværdier.",
                ),
            ),
        ),
        authored_item(
            "dm857.m04.assessment.012",
            ActivityType.DEBUGGING,
            (
                "Corrige una función que modifica una lista global durante un cálculo.",
                "Fix a function that mutates a global list during a calculation.",
                "Ret en funktion, der ændrer en global liste under en beregning.",
            ),
            (
                (
                    "Recibir los datos como parámetro y retornar un resultado nuevo sin modificar la global.",
                    "Receive data as a parameter and return a new result without mutating the global.",
                    "Modtag data som parameter og returnér et nyt resultat uden at ændre den globale liste.",
                ),
            ),
            (
                "La dependencia y el efecto se vuelven explícitos o se eliminan.",
                "The dependency and effect become explicit or are removed.",
                "Afhængigheden og effekten bliver eksplicitte eller fjernes.",
            ),
        ),
        authored_item(
            "dm857.m04.assessment.013",
            ActivityType.CODE_TRACING,
            (
                "Traza una función con dos return y determina qué líneas quedan inalcanzables.",
                "Trace a function with two return statements and identify unreachable lines.",
                "Gennemgå en funktion med to return-sætninger og identificér utilgængelige linjer.",
            ),
            (
                (
                    "Las líneas posteriores al primer return ejecutado no se ejecutan en esa llamada.",
                    "Lines after the first executed return do not run in that call.",
                    "Linjer efter den første udførte return kører ikke i det kald.",
                ),
            ),
            (
                "return finaliza inmediatamente la llamada actual.",
                "return immediately ends the current call.",
                "return afslutter straks det aktuelle kald.",
            ),
        ),
        authored_item(
            "dm857.m04.assessment.014",
            ActivityType.SHORT_ANSWER,
            (
                "Justifica por qué una función de veinte responsabilidades es difícil de probar.",
                "Justify why a function with twenty responsibilities is hard to test.",
                "Begrund, hvorfor en funktion med tyve ansvarsområder er vanskelig at teste.",
            ),
            (
                (
                    "Combina muchas entradas, rutas, efectos y causas de fallo, por lo que los casos crecen y los defectos son difíciles de aislar.",
                    "It combines many inputs, paths, effects, and failure causes, so cases grow and defects are hard to isolate.",
                    "Den kombinerer mange input, veje, effekter og fejlkilder, så antallet af tilfælde vokser, og fejl er svære at isolere.",
                ),
            ),
            (
                "La descomposición reduce el espacio de estados de cada prueba.",
                "Decomposition reduces the state space of each test.",
                "Dekomponering reducerer tilstandsrummet for hver test.",
            ),
        ),
    ),
    tutor_support=tutor_support(
        (
            "Una función es una unidad de comportamiento con una interfaz explícita. Su definición establece parámetros y cuerpo; cada "
            "llamada evalúa argumentos, crea un ámbito local, ejecuta el cuerpo y entrega el primer valor retornado. Los parámetros "
            "deben representar dependencias necesarias y los valores predeterminados deben corresponder a casos habituales seguros. "
            "return y print no son equivalentes: return transmite datos reutilizables, mientras print produce un efecto visible y retorna "
            "None. Las funciones puras dependen sólo de argumentos y no modifican estado externo, lo que facilita pruebas y composición. "
            "Los efectos secundarios son válidos en fronteras de entrada/salida, pero deben aislarse y documentarse. La descomposición divide "
            "un problema en responsabilidades con contratos verificables; la composición conecta sus retornos. Una precondición limita entradas "
            "aceptables y una poscondición expresa la garantía observable. Las pruebas unitarias deben cubrir rutas de retorno, límites, errores "
            "de ámbito y efectos. Los ejemplos biomédicos del módulo son escenarios de programación didácticos y no representan protocolos, "
            "umbrales clínicos ni recomendaciones de laboratorio.",
            "A function is a unit of behavior with an explicit interface. Its definition establishes parameters and body; each call evaluates "
            "arguments, creates local scope, executes the body, and delivers the first returned value. Parameters should represent necessary "
            "dependencies, and defaults should correspond to safe common cases. return and print are not equivalent: return transmits reusable "
            "data, while print creates a visible effect and returns None. Pure functions depend only on arguments and do not modify external state, "
            "which supports testing and composition. Side effects are valid at input/output boundaries but should be isolated and documented. "
            "Decomposition divides a problem into responsibilities with verifiable contracts; composition connects their results. A precondition "
            "limits acceptable input and a postcondition states the observable guarantee. Unit tests should cover return paths, boundaries, scope "
            "errors, and effects. Biomedical examples are programming exercises, not protocols, clinical thresholds, or laboratory advice.",
            "En funktion er en adfærdsenhed med en eksplicit grænseflade. Definitionen fastlægger parametre og krop; hvert kald evaluerer argumenter, "
            "opretter lokalt scope, udfører kroppen og leverer den første returværdi. Parametre bør repræsentere nødvendige afhængigheder, og "
            "standardværdier bør svare til sikre almindelige tilfælde. return og print er ikke ækvivalente: return overfører genanvendelige data, "
            "mens print skaber en synlig effekt og returnerer None. Rene funktioner afhænger kun af argumenter og ændrer ikke ekstern tilstand. "
            "Sideeffekter er gyldige ved input/output-grænser, men bør isoleres og dokumenteres. Dekomponering opdeler et problem i ansvarsområder "
            "med verificerbare kontrakter, og komposition forbinder resultaterne. Biomedicinske eksempler er programmeringsøvelser og ikke protokoller.",
        ),
        (
            (
                "Una llamada crea un ámbito local nuevo.",
                "A call creates a new local scope.",
                "Et kald opretter et nyt lokalt scope.",
            ),
            (
                "Los parámetros reciben argumentos.",
                "Parameters receive arguments.",
                "Parametre modtager argumenter.",
            ),
            (
                "Los argumentos nombrados se vinculan por nombre.",
                "Keyword arguments bind by name.",
                "Nøgleordsargumenter bindes efter navn.",
            ),
            (
                "return finaliza la llamada actual.",
                "return ends the current call.",
                "return afslutter det aktuelle kald.",
            ),
            ("print retorna None.", "print returns None.", "print returnerer None."),
            (
                "Sin return ejecutado, una función retorna None.",
                "Without an executed return, a function returns None.",
                "Uden udført return returnerer en funktion None.",
            ),
            (
                "Una función pura no modifica estado externo.",
                "A pure function does not modify external state.",
                "En ren funktion ændrer ikke ekstern tilstand.",
            ),
            (
                "Los efectos secundarios deben aislarse.",
                "Side effects should be isolated.",
                "Sideeffekter bør isoleres.",
            ),
            (
                "Una precondición restringe entradas.",
                "A precondition restricts inputs.",
                "En forudsætning begrænser input.",
            ),
            (
                "Una poscondición describe la garantía.",
                "A postcondition describes the guarantee.",
                "En efterbetingelse beskriver garantien.",
            ),
            (
                "La composición conecta retornos con argumentos.",
                "Composition connects returns to arguments.",
                "Komposition forbinder returværdier med argumenter.",
            ),
            (
                "Las pruebas deben cubrir cada ruta de retorno.",
                "Tests should cover every return path.",
                "Test bør dække hver returvej.",
            ),
            (
                "Las dependencias explícitas mejoran testabilidad.",
                "Explicit dependencies improve testability.",
                "Eksplicitte afhængigheder forbedrer testbarhed.",
            ),
            (
                "Una responsabilidad pequeña reduce acoplamiento.",
                "A small responsibility reduces coupling.",
                "Et lille ansvar reducerer kobling.",
            ),
        ),
        (
            (
                "Confundir parámetro con argumento.",
                "Confusing a parameter with an argument.",
                "At forveksle parameter og argument.",
            ),
            (
                "Creer que print devuelve el valor mostrado.",
                "Believing print returns the displayed value.",
                "At tro, at print returnerer den viste værdi.",
            ),
            (
                "Olvidar una ruta sin return.",
                "Forgetting a path without return.",
                "At glemme en vej uden return.",
            ),
            (
                "Suponer que una variable local existe fuera de la función.",
                "Assuming a local variable exists outside the function.",
                "At antage, at en lokal variabel findes uden for funktionen.",
            ),
            (
                "Usar globales como dependencias ocultas.",
                "Using globals as hidden dependencies.",
                "At bruge globale værdier som skjulte afhængigheder.",
            ),
            (
                "Mezclar cálculo y presentación.",
                "Mixing calculation and presentation.",
                "At blande beregning og præsentation.",
            ),
            (
                "Usar valores predeterminados mutables sin comprenderlos.",
                "Using mutable defaults without understanding them.",
                "At bruge muterbare standardværdier uden forståelse.",
            ),
            (
                "Crear funciones con demasiadas responsabilidades.",
                "Creating functions with too many responsibilities.",
                "At skabe funktioner med for mange ansvarsområder.",
            ),
            (
                "Documentar implementación en lugar de contrato.",
                "Documenting implementation instead of contract.",
                "At dokumentere implementering i stedet for kontrakt.",
            ),
            (
                "Probar sólo el caso normal.",
                "Testing only the normal case.",
                "Kun at teste det normale tilfælde.",
            ),
            (
                "Creer que una función pura es automáticamente correcta.",
                "Believing a pure function is automatically correct.",
                "At tro, at en ren funktion automatisk er korrekt.",
            ),
            (
                "Añadir parámetros que la función no necesita.",
                "Adding parameters the function does not need.",
                "At tilføje parametre, som funktionen ikke behøver.",
            ),
        ),
        (
            (
                "¿Qué recibe exactamente esta función?",
                "What exactly does this function receive?",
                "Hvad modtager denne funktion præcist?",
            ),
            (
                "¿Qué valor retorna cada ruta?",
                "What value does each path return?",
                "Hvilken værdi returnerer hver vej?",
            ),
            (
                "¿Qué dependencia no aparece en los parámetros?",
                "Which dependency is absent from the parameters?",
                "Hvilken afhængighed fremgår ikke af parametrene?",
            ),
            (
                "¿Este print debería ser un return?",
                "Should this print be a return?",
                "Burde dette print være en return?",
            ),
            (
                "¿Qué nombre local existe durante la llamada?",
                "Which local name exists during the call?",
                "Hvilket lokalt navn findes under kaldet?",
            ),
            (
                "¿La función modifica estado externo?",
                "Does the function modify external state?",
                "Ændrer funktionen ekstern tilstand?",
            ),
            ("¿Cuál es la precondición?", "What is the precondition?", "Hvad er forudsætningen?"),
            (
                "¿Cuál es la poscondición observable?",
                "What is the observable postcondition?",
                "Hvad er den observerbare efterbetingelse?",
            ),
            (
                "¿Puede separarse una responsabilidad?",
                "Can one responsibility be separated?",
                "Kan ét ansvarsområde adskilles?",
            ),
            (
                "¿Qué prueba cubre esta rama?",
                "Which test covers this branch?",
                "Hvilken test dækker denne gren?",
            ),
            (
                "¿Qué ocurre si se omite el argumento opcional?",
                "What happens when the optional argument is omitted?",
                "Hvad sker der, når det valgfrie argument udelades?",
            ),
            (
                "¿Cómo reutilizará el llamador el retorno?",
                "How will the caller reuse the return value?",
                "Hvordan genbruger den kaldende kode returværdien?",
            ),
        ),
        (
            (
                "Define con precisión parámetros y retorno.",
                "Precisely defines parameters and return.",
                "Definerer parametre og retur præcist.",
            ),
            (
                "Distingue return de print.",
                "Distinguishes return from print.",
                "Skelner mellem return og print.",
            ),
            (
                "Traza ámbitos locales correctamente.",
                "Traces local scopes correctly.",
                "Gennemgår lokale scopes korrekt.",
            ),
            (
                "Reconoce efectos secundarios.",
                "Recognizes side effects.",
                "Genkender sideeffekter.",
            ),
            (
                "Formula contratos verificables.",
                "Formulates verifiable contracts.",
                "Formulerer verificerbare kontrakter.",
            ),
            (
                "Descompone responsabilidades coherentemente.",
                "Decomposes responsibilities coherently.",
                "Dekomponerer ansvarsområder sammenhængende.",
            ),
            (
                "Compone funciones sin ocultar flujo.",
                "Composes functions without hiding flow.",
                "Sammensætter funktioner uden at skjule flow.",
            ),
            (
                "Cubre rutas de retorno con pruebas.",
                "Covers return paths with tests.",
                "Dækker returveje med test.",
            ),
            (
                "Evita dependencias globales innecesarias.",
                "Avoids unnecessary global dependencies.",
                "Undgår unødvendige globale afhængigheder.",
            ),
            (
                "Explica errores con vocabulario técnico correcto.",
                "Explains errors with correct technical vocabulary.",
                "Forklarer fejl med korrekt teknisk ordforråd.",
            ),
        ),
        (
            (
                "Dar primero una pista en ejercicios.",
                "Give a hint first in exercises.",
                "Giv først et hint i øvelser.",
            ),
            (
                "No sustituir return por print.",
                "Do not substitute print for return.",
                "Erstat ikke return med print.",
            ),
            (
                "Hacer visible el ámbito de cada nombre.",
                "Make each name's scope visible.",
                "Gør hvert navns scope synligt.",
            ),
            (
                "Separar cálculo de entrada/salida.",
                "Separate calculation from input/output.",
                "Adskil beregning fra input/output.",
            ),
            (
                "No introducir clases antes de tiempo.",
                "Do not introduce classes prematurely.",
                "Introducér ikke klasser for tidligt.",
            ),
            (
                "No usar bibliotecas para ocultar el concepto.",
                "Do not use libraries to hide the concept.",
                "Brug ikke biblioteker til at skjule konceptet.",
            ),
            (
                "No presentar ejemplos como recomendaciones clínicas.",
                "Do not present examples as clinical advice.",
                "Præsenter ikke eksempler som kliniske anbefalinger.",
            ),
            (
                "Relacionar pruebas con contratos.",
                "Relate tests to contracts.",
                "Knyt test til kontrakter.",
            ),
            (
                "Indicar cuando una ruta retorna None.",
                "Indicate when a path returns None.",
                "Angiv, når en vej returnerer None.",
            ),
        ),
        (
            "Official DM857 course description, SDU, active version approved in 2025.",
            "Think Python, third edition, chapters on functions, fruitful functions, scope, and testing.",
            "Introduction to Computation and Programming Using Python, third edition, sections on functions, abstraction, and testing.",
        ),
    ),
)

LOCALIZED_OBJECTIVE_QUESTION_BANK_04 = (
    objective_mcq(
        "dm857.m04.bank.001",
        (
            "¿Qué describe un parámetro?",
            "What does a parameter describe?",
            "Hvad beskriver en parameter?",
        ),
        (
            (
                "definition_name",
                (
                    "Un nombre en la definición",
                    "A name in the definition",
                    "Et navn i definitionen",
                ),
            ),
            ("call_value", ("Un valor en la llamada", "A value in the call", "En værdi i kaldet")),
            ("printed_text", ("Texto impreso", "Printed text", "Udskrevet tekst")),
            ("global_only", ("Siempre una global", "Always a global", "Altid en global variabel")),
        ),
        "definition_name",
        (
            "El parámetro es el nombre declarado en la cabecera.",
            "A parameter is the name declared in the header.",
            "En parameter er navnet i funktionshovedet.",
        ),
    ),
    objective_tf(
        "dm857.m04.bank.002",
        (
            "print y return son equivalentes.",
            "print and return are equivalent.",
            "print og return er ækvivalente.",
        ),
        correct=False,
        explanation=(
            "print produce salida y retorna None; return entrega un valor.",
            "print produces output and returns None; return delivers a value.",
            "print producerer output og returnerer None; return leverer en værdi.",
        ),
    ),
    objective_mcq(
        "dm857.m04.bank.003",
        (
            "¿Qué retorna una función sin return ejecutado?",
            "What does a function return when no return executes?",
            "Hvad returnerer en funktion, når ingen return udføres?",
        ),
        (
            ("none", ("None", "None", "None")),
            ("zero", ("0", "0", "0")),
            ("false", ("False", "False", "False")),
            ("error", ("Siempre error", "Always an error", "Altid en fejl")),
        ),
        "none",
        (
            "Python retorna None implícitamente.",
            "Python implicitly returns None.",
            "Python returnerer implicit None.",
        ),
    ),
    objective_tf(
        "dm857.m04.bank.004",
        (
            "Cada llamada crea variables locales nuevas.",
            "Each call creates new local variables.",
            "Hvert kald opretter nye lokale variable.",
        ),
        correct=True,
        explanation=(
            "El ámbito local pertenece a la llamada.",
            "Local scope belongs to the call.",
            "Lokalt scope tilhører kaldet.",
        ),
    ),
    objective_mcq(
        "dm857.m04.bank.005",
        (
            "¿Qué argumento mejora claridad cuando hay varios números similares?",
            "Which argument style improves clarity when several numbers look similar?",
            "Hvilken argumentstil forbedrer klarheden, når flere tal ligner hinanden?",
        ),
        (
            ("keyword", ("Nombrado", "Keyword", "Nøgleord")),
            ("positional", ("Sólo posicional", "Positional only", "Kun positionelt")),
            ("global", ("Global", "Global", "Global")),
            ("printed", ("Impreso", "Printed", "Udskrevet")),
        ),
        "keyword",
        (
            "El nombre hace explícito el significado del valor.",
            "The name makes the value's meaning explicit.",
            "Navnet gør værdiens betydning eksplicit.",
        ),
    ),
    objective_tf(
        "dm857.m04.bank.006",
        (
            "Una función pura modifica una lista global.",
            "A pure function mutates a global list.",
            "En ren funktion ændrer en global liste.",
        ),
        correct=False,
        explanation=(
            "Modificar estado externo es un efecto secundario.",
            "Mutating external state is a side effect.",
            "Ændring af ekstern tilstand er en sideeffekt.",
        ),
    ),
    objective_mcq(
        "dm857.m04.bank.007",
        (
            "¿Qué palabra finaliza una llamada y entrega un valor?",
            "Which keyword ends a call and delivers a value?",
            "Hvilket nøgleord afslutter et kald og leverer en værdi?",
        ),
        (
            ("return", ("return", "return", "return")),
            ("print", ("print", "print", "print")),
            ("def", ("def", "def", "def")),
            ("pass", ("pass", "pass", "pass")),
        ),
        "return",
        (
            "return transfiere el valor al llamador.",
            "return transfers the value to the caller.",
            "return overfører værdien til den kaldende kode.",
        ),
    ),
    objective_tf(
        "dm857.m04.bank.008",
        (
            "El código posterior a un return ejecutado se ejecuta normalmente.",
            "Code after an executed return runs normally.",
            "Kode efter en udført return kører normalt.",
        ),
        correct=False,
        explanation=(
            "La llamada termina al ejecutar return.",
            "The call ends when return executes.",
            "Kaldet slutter, når return udføres.",
        ),
    ),
    objective_mcq(
        "dm857.m04.bank.009",
        (
            "¿Qué describe una precondición?",
            "What does a precondition describe?",
            "Hvad beskriver en forudsætning?",
        ),
        (
            (
                "before",
                ("Lo que debe cumplirse antes", "What must hold before", "Hvad der skal gælde før"),
            ),
            ("after", ("Sólo el resultado final", "Only the final result", "Kun slutresultatet")),
            ("implementation", ("Cada línea interna", "Every internal line", "Hver intern linje")),
            ("format", ("El color del editor", "The editor color", "Editorens farve")),
        ),
        "before",
        (
            "La precondición restringe entradas válidas.",
            "A precondition restricts valid inputs.",
            "En forudsætning begrænser gyldige input.",
        ),
    ),
    objective_tf(
        "dm857.m04.bank.010",
        (
            "Una poscondición describe una garantía observable.",
            "A postcondition describes an observable guarantee.",
            "En efterbetingelse beskriver en observerbar garanti.",
        ),
        correct=True,
        explanation=(
            "Se aplica cuando se cumplen las precondiciones.",
            "It applies when preconditions hold.",
            "Den gælder, når forudsætningerne er opfyldt.",
        ),
    ),
    objective_mcq(
        "dm857.m04.bank.011",
        (
            "¿Qué facilita una función pequeña?",
            "What does a small function facilitate?",
            "Hvad gør en lille funktion lettere?",
        ),
        (
            ("testing", ("Pruebas y aislamiento", "Testing and isolation", "Test og isolering")),
            ("hidden_state", ("Más estado oculto", "More hidden state", "Mere skjult tilstand")),
            ("duplication", ("Más duplicación", "More duplication", "Mere duplikering")),
            ("ambiguity", ("Más ambigüedad", "More ambiguity", "Mere tvetydighed")),
        ),
        "testing",
        (
            "Una responsabilidad reducida limita causas de fallo.",
            "A narrow responsibility limits failure causes.",
            "Et begrænset ansvar begrænser fejlkilder.",
        ),
    ),
    objective_tf(
        "dm857.m04.bank.012",
        (
            "Los parámetros son globales por definición.",
            "Parameters are global by definition.",
            "Parametre er globale pr. definition.",
        ),
        correct=False,
        explanation=(
            "Los parámetros son locales a cada llamada.",
            "Parameters are local to each call.",
            "Parametre er lokale for hvert kald.",
        ),
    ),
    objective_mcq(
        "dm857.m04.bank.013",
        ("¿Qué es composición?", "What is composition?", "Hvad er komposition?"),
        (
            (
                "chain",
                (
                    "Usar el retorno como argumento de otra función",
                    "Use one return as another function's argument",
                    "Brug én returværdi som argument til en anden funktion",
                ),
            ),
            ("copy", ("Copiar código", "Copy code", "Kopiér kode")),
            ("global", ("Crear una global", "Create a global", "Opret en global variabel")),
            ("print", ("Imprimir dos veces", "Print twice", "Udskriv to gange")),
        ),
        "chain",
        (
            "La composición conecta interfaces mediante valores.",
            "Composition connects interfaces through values.",
            "Komposition forbinder grænseflader gennem værdier.",
        ),
    ),
    objective_tf(
        "dm857.m04.bank.014",
        (
            "Un efecto secundario siempre es un error.",
            "A side effect is always an error.",
            "En sideeffekt er altid en fejl.",
        ),
        correct=False,
        explanation=(
            "Puede ser necesario, pero debe aislarse y documentarse.",
            "It may be necessary, but should be isolated and documented.",
            "Den kan være nødvendig, men bør isoleres og dokumenteres.",
        ),
    ),
    objective_mcq(
        "dm857.m04.bank.015",
        (
            "¿Qué prueba detecta una ruta sin return?",
            "Which test exposes a path without return?",
            "Hvilken test afslører en vej uden return?",
        ),
        (
            (
                "branch_input",
                (
                    "Una entrada que active esa rama",
                    "An input that activates that branch",
                    "Et input, der aktiverer grenen",
                ),
            ),
            (
                "same_only",
                ("Repetir el caso normal", "Repeat the normal case", "Gentag det normale tilfælde"),
            ),
            ("format", ("Cambiar formato", "Change formatting", "Skift formatering")),
            ("comment", ("Añadir comentario", "Add a comment", "Tilføj en kommentar")),
        ),
        "branch_input",
        (
            "La prueba debe ejecutar la ruta defectuosa.",
            "The test must execute the defective path.",
            "Testen skal udføre den fejlbehæftede vej.",
        ),
    ),
    objective_tf(
        "dm857.m04.bank.016",
        (
            "Una docstring debe repetir cada línea del cuerpo.",
            "A docstring should repeat every body line.",
            "En docstring bør gentage hver linje i kroppen.",
        ),
        correct=False,
        explanation=(
            "Debe describir contrato y uso, no narrar cada instrucción.",
            "It should describe contract and use, not narrate every statement.",
            "Den bør beskrive kontrakt og brug, ikke hver instruktion.",
        ),
    ),
    objective_mcq(
        "dm857.m04.bank.017",
        ("¿Qué retorna print(3)?", "What does print(3) return?", "Hvad returnerer print(3)?"),
        (
            ("none", ("None", "None", "None")),
            ("three", ("3", "3", "3")),
            ("string", ("'3'", "'3'", "'3'")),
            ("true", ("True", "True", "True")),
        ),
        "none",
        (
            "La función muestra 3 y retorna None.",
            "The function displays 3 and returns None.",
            "Funktionen viser 3 og returnerer None.",
        ),
    ),
    objective_tf(
        "dm857.m04.bank.018",
        (
            "Dos llamadas pueden usar el mismo nombre local sin compartir valor.",
            "Two calls may use the same local name without sharing a value.",
            "To kald kan bruge samme lokale navn uden at dele værdi.",
        ),
        correct=True,
        explanation=(
            "Cada llamada tiene su propio ámbito local.",
            "Each call has its own local scope.",
            "Hvert kald har sit eget lokale scope.",
        ),
    ),
    objective_mcq(
        "dm857.m04.bank.019",
        (
            "¿Qué hace un valor predeterminado?",
            "What does a default value do?",
            "Hvad gør en standardværdi?",
        ),
        (
            (
                "omission",
                (
                    "Se usa si se omite el argumento",
                    "It is used when the argument is omitted",
                    "Den bruges, når argumentet udelades",
                ),
            ),
            (
                "mandatory",
                (
                    "Hace obligatorio el argumento",
                    "It makes the argument mandatory",
                    "Den gør argumentet obligatorisk",
                ),
            ),
            ("global", ("Lo convierte en global", "It makes it global", "Den gør det globalt")),
            ("print", ("Lo imprime", "It prints it", "Den udskriver det")),
        ),
        "omission",
        (
            "La llamada puede aceptar el valor establecido en la definición.",
            "The call may accept the value established in the definition.",
            "Kaldet kan bruge værdien fra definitionen.",
        ),
    ),
    objective_tf(
        "dm857.m04.bank.020",
        (
            "Un argumento nombrado se vincula por el nombre del parámetro.",
            "A keyword argument binds by parameter name.",
            "Et nøgleordsargument bindes efter parameternavnet.",
        ),
        correct=True,
        explanation=(
            "Por eso puede mejorar la legibilidad.",
            "That is why it can improve readability.",
            "Derfor kan det forbedre læsbarheden.",
        ),
    ),
    objective_mcq(
        "dm857.m04.bank.021",
        (
            "¿Qué debe comprobar una prueba unitaria?",
            "What should a unit test check?",
            "Hvad bør en enhedstest kontrollere?",
        ),
        (
            (
                "return",
                (
                    "Valor retornado y contrato",
                    "Returned value and contract",
                    "Returværdi og kontrakt",
                ),
            ),
            ("color", ("Color de ventana", "Window color", "Vinduesfarve")),
            ("typing_speed", ("Velocidad al escribir", "Typing speed", "Skrivehastighed")),
            ("global_count", ("Número de globales", "Number of globals", "Antal globale variable")),
        ),
        "return",
        (
            "La prueba verifica comportamiento observable.",
            "The test verifies observable behavior.",
            "Testen verificerer observerbar adfærd.",
        ),
    ),
    objective_tf(
        "dm857.m04.bank.022",
        (
            "Una función puede retornar una tupla.",
            "A function may return a tuple.",
            "En funktion kan returnere en tuple.",
        ),
        correct=True,
        explanation=(
            "return puede entregar cualquier objeto de Python.",
            "return can deliver any Python object.",
            "return kan levere ethvert Python-objekt.",
        ),
    ),
    objective_mcq(
        "dm857.m04.bank.023",
        ("¿Qué reduce acoplamiento?", "What reduces coupling?", "Hvad reducerer kobling?"),
        (
            (
                "clear_interface",
                (
                    "Interfaces claras y responsabilidades pequeñas",
                    "Clear interfaces and small responsibilities",
                    "Klare grænseflader og små ansvarsområder",
                ),
            ),
            ("global_state", ("Más estado global", "More global state", "Mere global tilstand")),
            ("duplicate", ("Duplicar código", "Duplicate code", "Duplikér kode")),
            ("hidden_io", ("Entrada/salida oculta", "Hidden input/output", "Skjult input/output")),
        ),
        "clear_interface",
        (
            "Las fronteras explícitas limitan dependencias.",
            "Explicit boundaries limit dependencies.",
            "Eksplicitte grænser begrænser afhængigheder.",
        ),
    ),
    objective_tf(
        "dm857.m04.bank.024",
        (
            "Una función pura puede seguir conteniendo un error lógico.",
            "A pure function may still contain a logic error.",
            "En ren funktion kan stadig indeholde en logisk fejl.",
        ),
        correct=True,
        explanation=(
            "La pureza facilita razonar, pero no garantiza la fórmula.",
            "Purity aids reasoning but does not guarantee the formula.",
            "Renhed hjælper ræsonnement, men garanterer ikke formlen.",
        ),
    ),
    objective_mcq(
        "dm857.m04.bank.025",
        (
            "¿Qué ocurre al llamar f(x=2, 3)?",
            "What happens when calling f(x=2, 3)?",
            "Hvad sker der ved kaldet f(x=2, 3)?",
        ),
        (
            (
                "syntax",
                (
                    "Error: posicional después de nombrado",
                    "Error: positional after keyword",
                    "Fejl: positionelt argument efter nøgleordsargument",
                ),
            ),
            ("valid", ("Es válido", "It is valid", "Det er gyldigt")),
            ("none", ("Retorna None siempre", "Always returns None", "Returnerer altid None")),
            ("global", ("x se vuelve global", "x becomes global", "x bliver global")),
        ),
        "syntax",
        (
            "Los posicionales deben aparecer antes de los nombrados.",
            "Positional arguments must precede keyword arguments.",
            "Positionelle argumenter skal stå før nøgleordsargumenter.",
        ),
    ),
    objective_tf(
        "dm857.m04.bank.026",
        (
            "Una variable local queda accesible después de terminar la llamada.",
            "A local variable remains accessible after the call ends.",
            "En lokal variabel forbliver tilgængelig efter kaldet.",
        ),
        correct=False,
        explanation=(
            "El nombre local deja de estar disponible fuera de su ámbito.",
            "The local name is unavailable outside its scope.",
            "Det lokale navn er ikke tilgængeligt uden for sit scope.",
        ),
    ),
    objective_mcq(
        "dm857.m04.bank.027",
        (
            "¿Qué representa una poscondición de square(x)?",
            "What is a postcondition for square(x)?",
            "Hvad er en efterbetingelse for square(x)?",
        ),
        (
            (
                "relation",
                ("El retorno es x * x", "The return equals x * x", "Returværdien er x * x"),
            ),
            ("parameter", ("x es parámetro", "x is a parameter", "x er en parameter")),
            ("line", ("Usa una línea", "It uses one line", "Den bruger én linje")),
            ("print", ("Imprime x", "It prints x", "Den udskriver x")),
        ),
        "relation",
        (
            "La poscondición expresa la garantía del resultado.",
            "The postcondition states the result guarantee.",
            "Efterbetingelsen angiver resultatgarantien.",
        ),
    ),
    objective_tf(
        "dm857.m04.bank.028",
        (
            "La descomposición puede permitir probar partes antes de integrarlas.",
            "Decomposition can allow parts to be tested before integration.",
            "Dekomponering kan gøre det muligt at teste dele før integration.",
        ),
        correct=True,
        explanation=(
            "Cada función pequeña puede verificarse de forma aislada.",
            "Each small function can be verified in isolation.",
            "Hver lille funktion kan verificeres isoleret.",
        ),
    ),
    objective_mcq(
        "dm857.m04.bank.029",
        ("¿Cuál es un efecto secundario?", "Which is a side effect?", "Hvad er en sideeffekt?"),
        (
            ("write_file", ("Escribir un archivo", "Writing a file", "At skrive en fil")),
            ("add", ("Retornar a + b", "Returning a + b", "At returnere a + b")),
            ("compare", ("Retornar a == b", "Returning a == b", "At returnere a == b")),
            ("tuple", ("Retornar una tupla", "Returning a tuple", "At returnere en tuple")),
        ),
        "write_file",
        (
            "Escribir modifica estado fuera de la función.",
            "Writing changes state outside the function.",
            "Filskrivning ændrer tilstand uden for funktionen.",
        ),
    ),
    objective_tf(
        "dm857.m04.bank.030",
        (
            "Un parámetro obligatorio puede aparecer después de uno con valor predeterminado en la misma lista simple.",
            "A required parameter may follow a defaulted parameter in the same simple parameter list.",
            "En obligatorisk parameter kan stå efter en parameter med standardværdi i samme simple parameterliste.",
        ),
        correct=False,
        explanation=(
            "Los parámetros obligatorios deben preceder a los predeterminados.",
            "Required parameters must precede defaulted parameters.",
            "Obligatoriske parametre skal stå før parametre med standardværdi.",
        ),
    ),
)


def materialize_module_04_question_bank(
    locale: AppLocale | str,
) -> tuple[AssessmentItem, ...]:
    resolved = locale if isinstance(locale, AppLocale) else AppLocale.resolve(locale)
    return tuple(item.materialize(resolved) for item in LOCALIZED_OBJECTIVE_QUESTION_BANK_04)


MODULE_04_FUNCTIONS: LearningModule = LOCALIZED_MODULE_04_FUNCTIONS.materialize(
    AppLocale.SPANISH_SPAIN
)
OBJECTIVE_QUESTION_BANK_04 = materialize_module_04_question_bank(AppLocale.SPANISH_SPAIN)

__all__ = [
    "LOCALIZED_MODULE_04_FUNCTIONS",
    "LOCALIZED_OBJECTIVE_QUESTION_BANK_04",
    "MODULE_04_FUNCTIONS",
    "OBJECTIVE_QUESTION_BANK_04",
    "materialize_module_04_question_bank",
]
