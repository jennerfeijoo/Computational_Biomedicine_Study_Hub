"""DM857 module 14: testing, debugging, and software quality."""

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

_OBJECTIVES = (
    (
        "m14.o1",
        (
            "Explicar qué verifica una prueba y cómo se relaciona con un contrato de comportamiento.",
            "Explain what a test verifies and how it relates to a behavioral contract.",
            "Forklare hvad en test verificerer, og hvordan den relaterer til en adfærdskontrakt.",
        ),
    ),
    (
        "m14.o2",
        (
            "Escribir pruebas pytest legibles con aserciones diagnósticas y casos aislados.",
            "Write readable pytest tests with diagnostic assertions and isolated cases.",
            "Skrive læsbare pytest-tests med diagnostiske assertions og isolerede tilfælde.",
        ),
    ),
    (
        "m14.o3",
        (
            "Usar fixtures y parametrización sin introducir estado compartido accidental.",
            "Use fixtures and parametrization without introducing accidental shared state.",
            "Bruge fixtures og parametrisering uden utilsigtet delt tilstand.",
        ),
    ),
    (
        "m14.o4",
        (
            "Comprobar excepciones, advertencias, límites e invariantes de forma explícita.",
            "Check exceptions, warnings, boundaries, and invariants explicitly.",
            "Kontrollere exceptions, advarsler, grænser og invarianter eksplicit.",
        ),
    ),
    (
        "m14.o5",
        (
            "Depurar fallos mediante trazas, reducción del caso y comprobación de hipótesis.",
            "Debug failures through tracebacks, case reduction, and hypothesis checking.",
            "Fejlsøge fejl gennem tracebacks, reduktion af cases og kontrol af hypoteser.",
        ),
    ),
    (
        "m14.o6",
        (
            "Diseñar logging útil sin mezclar observabilidad con la salida funcional.",
            "Design useful logging without mixing observability with functional output.",
            "Designe nyttig logging uden at blande observerbarhed med funktionelt output.",
        ),
    ),
    (
        "m14.o7",
        (
            "Diseñar funciones y dependencias para que sean fáciles de probar.",
            "Design functions and dependencies so they are easy to test.",
            "Designe funktioner og afhængigheder så de er nemme at teste.",
        ),
    ),
    (
        "m14.o8",
        (
            "Aplicar pruebas basadas en propiedades e invariantes como complemento de ejemplos concretos.",
            "Apply property- and invariant-based tests as a complement to concrete examples.",
            "Anvende egenskabs- og invariantbaserede tests som supplement til konkrete eksempler.",
        ),
    ),
)

_CONCEPTS = (
    (
        "tests-as-contracts",
        (
            "Pruebas como contratos ejecutables",
            "Tests as executable contracts",
            "Tests som eksekverbare kontrakter",
        ),
        (
            "Una prueba automatizada prepara un estado, ejecuta una conducta y comprueba un resultado observable. No demuestra que un programa sea correcto en todos los casos, pero protege contratos específicos frente a regresiones. Una buena prueba indica qué propiedad importa, usa entradas controladas y falla con información suficiente para localizar la discrepancia.",
            "An automated test prepares state, executes behavior, and checks an observable result. It does not prove that a program is correct in every case, but it protects specific contracts against regressions. A good test states which property matters, uses controlled inputs, and fails with enough information to locate the discrepancy.",
            "En automatiseret test forbereder en tilstand, udfører adfærd og kontrollerer et observerbart resultat. Den beviser ikke at et program er korrekt i alle tilfælde, men beskytter bestemte kontrakter mod regressioner. En god test angiver den vigtige egenskab, bruger kontrollerede input og fejler med tilstrækkelig information.",
        ),
        (
            (
                "Prueba comportamiento observable, no detalles irrelevantes.",
                "Test observable behavior, not irrelevant details.",
                "Test observerbar adfærd, ikke irrelevante detaljer.",
            ),
            (
                "Una prueba debe poder fallar por la razón correcta.",
                "A test should be able to fail for the right reason.",
                "En test bør kunne fejle af den rigtige grund.",
            ),
            (
                "Las regresiones convierten errores corregidos en casos permanentes.",
                "Regression tests turn fixed bugs into permanent cases.",
                "Regressionstests gør rettede fejl til permanente cases.",
            ),
        ),
    ),
    (
        "pytest-structure",
        (
            "Estructura de pruebas con pytest",
            "Test structure with pytest",
            "Teststruktur med pytest",
        ),
        (
            "pytest descubre funciones test_* y utiliza assert de Python para producir diagnósticos detallados. El patrón Arrange–Act–Assert separa preparación, ejecución y comprobación. Cada prueba debe concentrarse en una conducta coherente. Las aserciones múltiples son válidas cuando describen el mismo resultado, pero mezclar escenarios independientes dificulta interpretar el fallo.",
            "pytest discovers test_* functions and uses Python assert statements to produce detailed diagnostics. Arrange–Act–Assert separates setup, execution, and checking. Each test should focus on one coherent behavior. Multiple assertions are valid when they describe the same result, but mixing independent scenarios makes failures harder to interpret.",
            "pytest finder test_*-funktioner og bruger Python-assertions til detaljerede diagnoser. Arrange–Act–Assert adskiller forberedelse, udførelse og kontrol. Hver test bør fokusere på én sammenhængende adfærd. Flere assertions er acceptable når de beskriver samme resultat, men uafhængige scenarier bør ikke blandes.",
        ),
        (
            (
                "Nombra la conducta esperada.",
                "Name the expected behavior.",
                "Navngiv den forventede adfærd.",
            ),
            (
                "Mantén separadas preparación, acción y comprobación.",
                "Keep setup, action, and assertion separate.",
                "Hold forberedelse, handling og kontrol adskilt.",
            ),
            (
                "Usa mensajes y valores que expliquen el fallo.",
                "Use messages and values that explain failure.",
                "Brug beskeder og værdier der forklarer fejlen.",
            ),
        ),
    ),
    (
        "fixtures-and-isolation",
        (
            "Fixtures, aislamiento y ciclo de vida",
            "Fixtures, isolation, and lifecycle",
            "Fixtures, isolation og livscyklus",
        ),
        (
            "Una fixture declara datos o recursos reutilizables y puede encargarse de su limpieza. El alcance function crea una instancia por prueba y suele ser la opción más segura. Alcances más amplios reducen coste, pero aumentan el riesgo de estado compartido. Las fixtures deben representar dependencias reales, ser pequeñas y devolver objetos listos para usar sin ocultar demasiada lógica.",
            "A fixture declares reusable data or resources and may handle cleanup. Function scope creates one instance per test and is usually the safest choice. Broader scopes reduce cost but increase the risk of shared state. Fixtures should represent real dependencies, remain small, and return ready-to-use objects without hiding excessive logic.",
            "En fixture deklarerer genbrugelige data eller ressourcer og kan håndtere oprydning. Function-scope opretter én instans pr. test og er normalt det sikreste valg. Bredere scopes reducerer omkostning men øger risikoen for delt tilstand. Fixtures bør repræsentere reelle afhængigheder og forblive små.",
        ),
        (
            (
                "Prefiere aislamiento por prueba.",
                "Prefer isolation per test.",
                "Foretræk isolation pr. test.",
            ),
            (
                "Usa yield cuando la fixture necesita limpieza.",
                "Use yield when a fixture needs cleanup.",
                "Brug yield når en fixture kræver oprydning.",
            ),
            (
                "No conviertas fixtures en un segundo programa oculto.",
                "Do not turn fixtures into a hidden second program.",
                "Gør ikke fixtures til et skjult andet program.",
            ),
        ),
    ),
    (
        "parametrization-boundaries-exceptions",
        (
            "Parametrización, límites y errores esperados",
            "Parametrization, boundaries, and expected errors",
            "Parametrisering, grænser og forventede fejl",
        ),
        (
            "La parametrización ejecuta el mismo contrato sobre entradas distintas y evita duplicar estructura. Los casos deben incluir valores típicos, límites, entradas vacías, tipos inválidos y datos ambiguos cuando sean relevantes. pytest.raises comprueba que una excepción esperada se produce en la operación concreta; una prueba demasiado amplia puede pasar por una excepción originada en otro lugar.",
            "Parametrization executes the same contract over different inputs and avoids duplicated structure. Cases should include typical values, boundaries, empty inputs, invalid types, and ambiguous data when relevant. pytest.raises checks that an expected exception occurs in the specific operation; an overly broad context may pass because an exception arose elsewhere.",
            "Parametrisering udfører samme kontrakt på forskellige input og undgår duplikeret struktur. Cases bør omfatte typiske værdier, grænser, tomme input, ugyldige typer og tvetydige data når relevant. pytest.raises kontrollerer at en forventet exception opstår i den konkrete operation; en for bred kontekst kan bestå af forkert grund.",
        ),
        (
            (
                "Parametriza una conducta, no problemas distintos.",
                "Parametrize one behavior, not unrelated problems.",
                "Parametrisér én adfærd, ikke forskellige problemer.",
            ),
            (
                "Incluye casos frontera con intención explícita.",
                "Include boundary cases intentionally.",
                "Medtag grænsetilfælde med tydelig hensigt.",
            ),
            (
                "Limita el bloque raises a la llamada esperada.",
                "Limit the raises block to the expected call.",
                "Begræns raises-blokken til det forventede kald.",
            ),
        ),
    ),
    (
        "debugging-workflow",
        (
            "Flujo sistemático de depuración",
            "A systematic debugging workflow",
            "Et systematisk fejlsøgningsworkflow",
        ),
        (
            "Depurar no consiste en cambiar líneas al azar. Primero se reproduce el fallo, se conserva el traceback y se reduce el caso. Después se formula una hipótesis, se inspecciona el estado relevante con un depurador, logging o aserciones temporales y se cambia una causa a la vez. La corrección termina con una prueba de regresión y la eliminación de diagnósticos accidentales.",
            "Debugging is not random line editing. First reproduce the failure, preserve the traceback, and reduce the case. Then form a hypothesis, inspect relevant state with a debugger, logging, or temporary assertions, and change one cause at a time. A fix ends with a regression test and removal of accidental diagnostics.",
            "Fejlsøgning er ikke tilfældig ændring af linjer. Reproducer først fejlen, bevar traceback og reducer casen. Formulér derefter en hypotese, undersøg relevant tilstand med debugger, logging eller midlertidige assertions, og ændr én årsag ad gangen. En rettelse afsluttes med en regressionstest og fjernelse af midlertidig diagnostik.",
        ),
        (
            (
                "Reproduce antes de corregir.",
                "Reproduce before fixing.",
                "Reproducer før rettelse.",
            ),
            (
                "Reduce el caso hasta conservar sólo la causa.",
                "Reduce the case while preserving the cause.",
                "Reducer casen mens årsagen bevares.",
            ),
            (
                "Añade una prueba que falle antes de la corrección.",
                "Add a test that fails before the fix.",
                "Tilføj en test der fejler før rettelsen.",
            ),
        ),
    ),
    (
        "logging-observability",
        (
            "Logging y observabilidad",
            "Logging and observability",
            "Logging og observerbarhed",
        ),
        (
            "logging registra eventos con nivel, contexto y destino configurables. DEBUG describe detalles de diagnóstico; INFO confirma hitos normales; WARNING indica una situación recuperable; ERROR registra un fallo que impide una operación. Una biblioteca no debe configurar globalmente el logging ni usar print como sustituto. Los mensajes deben aportar identificadores, cantidades y decisiones sin exponer datos sensibles.",
            "logging records events with configurable level, context, and destination. DEBUG describes diagnostic detail; INFO confirms normal milestones; WARNING indicates a recoverable situation; ERROR records a failure preventing an operation. A library should not configure global logging or use print as a substitute. Messages should add identifiers, counts, and decisions without exposing sensitive data.",
            "logging registrerer hændelser med konfigurerbart niveau, kontekst og destination. DEBUG beskriver diagnostiske detaljer; INFO bekræfter normale milepæle; WARNING angiver en situation der kan håndteres; ERROR registrerer en fejl der forhindrer en operation. Et bibliotek bør ikke konfigurere global logging eller bruge print som erstatning.",
        ),
        (
            (
                "Registra decisiones y contexto, no ruido repetitivo.",
                "Log decisions and context, not repetitive noise.",
                "Log beslutninger og kontekst, ikke gentaget støj.",
            ),
            (
                "Usa niveles coherentes.",
                "Use levels consistently.",
                "Brug niveauer konsekvent.",
            ),
            (
                "No registres datos sensibles ni secuencias completas por defecto.",
                "Do not log sensitive data or full sequences by default.",
                "Log ikke følsomme data eller fulde sekvenser som standard.",
            ),
        ),
    ),
    (
        "design-for-testability",
        (
            "Diseño para testabilidad",
            "Design for testability",
            "Design for testbarhed",
        ),
        (
            "El código es más fácil de probar cuando separa cálculo puro de entrada/salida, recibe dependencias explícitas y produce resultados deterministas. Inyectar un lector, reloj o generador aleatorio permite sustituirlo por un doble controlado. Las funciones pequeñas no son un objetivo por sí mismas: deben representar responsabilidades coherentes y exponer contratos estables.",
            "Code is easier to test when it separates pure computation from input/output, receives dependencies explicitly, and produces deterministic results. Injecting a reader, clock, or random generator allows replacement with a controlled double. Small functions are not an end in themselves: they should represent coherent responsibilities and expose stable contracts.",
            "Kode er lettere at teste når ren beregning adskilles fra input/output, afhængigheder modtages eksplicit, og resultater er deterministiske. Injektion af en læser, et ur eller en tilfældighedsgenerator gør det muligt at erstatte den med en kontrolleret test-double. Små funktioner bør repræsentere sammenhængende ansvar.",
        ),
        (
            (
                "Separa lógica de dominio y efectos externos.",
                "Separate domain logic from external effects.",
                "Adskil domænelogik fra eksterne effekter.",
            ),
            (
                "Inyecta dependencias variables.",
                "Inject variable dependencies.",
                "Injicér variable afhængigheder.",
            ),
            (
                "Haz explícita la fuente de no determinismo.",
                "Make the source of nondeterminism explicit.",
                "Gør kilden til ikke-determinisme eksplicit.",
            ),
        ),
    ),
    (
        "property-based-testing",
        (
            "Pruebas basadas en propiedades",
            "Property-based testing",
            "Egenskabsbaseret testning",
        ),
        (
            "Una prueba basada en propiedades genera muchos ejemplos y verifica un invariante general. Por ejemplo, aplicar complemento inverso dos veces debe recuperar una secuencia válida normalizada. Las propiedades complementan casos concretos, pero no sustituyen ejemplos de regresión ni una especificación precisa. Una propiedad mal formulada puede confirmar un algoritmo incorrecto de manera consistente.",
            "A property-based test generates many examples and checks a general invariant. For example, applying reverse complement twice should recover a valid normalized sequence. Properties complement concrete cases but do not replace regression examples or a precise specification. A poorly formulated property may consistently confirm an incorrect algorithm.",
            "En egenskabsbaseret test genererer mange eksempler og kontrollerer en generel invariant. For eksempel bør to anvendelser af omvendt komplement genskabe en gyldig normaliseret sekvens. Egenskaber supplerer konkrete cases, men erstatter ikke regressionseksempler eller en præcis specifikation.",
        ),
        (
            (
                "Formula invariantes independientes de la implementación.",
                "Formulate invariants independently of implementation.",
                "Formulér invarianter uafhængigt af implementeringen.",
            ),
            (
                "Conserva ejemplos concretos para fallos conocidos.",
                "Keep concrete examples for known failures.",
                "Bevar konkrete eksempler for kendte fejl.",
            ),
            (
                "Revisa que el generador cubra entradas relevantes.",
                "Check that the generator covers relevant inputs.",
                "Kontrollér at generatoren dækker relevante input.",
            ),
        ),
    ),
)

_EXAMPLES = (
    (
        "m14.e01",
        (
            "Parametrizar una función de normalización",
            "Parametrize a normalization function",
            "Parametrisér en normaliseringsfunktion",
        ),
        (
            "Prueba varios formatos de entrada sin duplicar la estructura del test.",
            "Test several input formats without duplicating test structure.",
            "Test flere inputformater uden at duplikere teststrukturen.",
        ),
        (
            (
                "Cada fila representa el mismo contrato.",
                "Each row represents the same contract.",
                "Hver række repræsenterer samme kontrakt.",
            ),
            (
                "Los IDs describen el escenario cuando falla.",
                "IDs describe the scenario when it fails.",
                "ID'er beskriver scenariet når det fejler.",
            ),
        ),
        """import pytest


def normalize_sequence(raw: str) -> str:
    return \"\".join(raw.split()).upper()


@pytest.mark.parametrize(
    (\"raw\", \"expected\"),
    [(\"acgt\", \"ACGT\"), (\"A C G T\", \"ACGT\"), (\"\", \"\")],
    ids=[\"lowercase\", \"whitespace\", \"empty\"],
)
def test_normalize_sequence(raw: str, expected: str) -> None:
    assert normalize_sequence(raw) == expected
""",
        "3 passed",
        (
            "La parametrización mantiene visible la relación entrada–salida y permite añadir límites.",
            "Parametrization keeps the input-output relationship visible and makes boundaries easy to add.",
            "Parametrisering holder input-output-forholdet synligt og gør grænsetilfælde lette at tilføje.",
        ),
    ),
    (
        "m14.e02",
        (
            "Fixture temporal aislada",
            "An isolated temporary fixture",
            "En isoleret midlertidig fixture",
        ),
        (
            "Usa tmp_path para probar lectura de archivos sin depender del sistema real.",
            "Use tmp_path to test file reading without depending on the real filesystem.",
            "Brug tmp_path til at teste filindlæsning uden afhængighed af det virkelige filsystem.",
        ),
        (
            (
                "La prueba crea su propio archivo.",
                "The test creates its own file.",
                "Testen opretter sin egen fil.",
            ),
            (
                "pytest elimina el directorio temporal después.",
                "pytest removes the temporary directory afterward.",
                "pytest fjerner den midlertidige mappe bagefter.",
            ),
        ),
        """from pathlib import Path


def read_sequence(path: Path) -> str:
    return \"\".join(path.read_text(encoding=\"utf-8\").split()).upper()


def test_read_sequence_uses_isolated_file(tmp_path: Path) -> None:
    source = tmp_path / \"sample.txt\"
    source.write_text(\"ac gt\\n\", encoding=\"utf-8\")

    result = read_sequence(source)

    assert result == \"ACGT\"
""",
        "1 passed",
        (
            "El recurso se prepara dentro de la prueba y no requiere rutas globales ni limpieza manual.",
            "The resource is prepared inside the test and needs no global paths or manual cleanup.",
            "Ressourcen forberedes inde i testen og kræver ingen globale stier eller manuel oprydning.",
        ),
    ),
    (
        "m14.e03",
        (
            "Comprobar una excepción concreta",
            "Check a specific exception",
            "Kontrollér en bestemt exception",
        ),
        (
            "Verifica tipo y mensaje sin ampliar innecesariamente el bloque raises.",
            "Verify type and message without unnecessarily widening the raises block.",
            "Kontrollér type og besked uden unødigt at udvide raises-blokken.",
        ),
        (
            (
                "La preparación ocurre fuera del contexto.",
                "Setup occurs outside the context.",
                "Forberedelsen sker uden for konteksten.",
            ),
            (
                "Sólo la llamada esperada puede satisfacer raises.",
                "Only the expected call can satisfy raises.",
                "Kun det forventede kald kan opfylde raises.",
            ),
        ),
        """import pytest


def require_non_empty(values: list[float]) -> float:
    if not values:
        raise ValueError(\"values cannot be empty\")
    return sum(values) / len(values)


def test_require_non_empty_rejects_empty_input() -> None:
    values: list[float] = []

    with pytest.raises(ValueError, match=\"cannot be empty\"):
        require_non_empty(values)
""",
        "1 passed",
        (
            "El test protege tanto la clase de error como una parte estable del mensaje.",
            "The test protects both the exception class and a stable part of the message.",
            "Testen beskytter både exception-klassen og en stabil del af beskeden.",
        ),
    ),
    (
        "m14.e04",
        (
            "Logging comprobable",
            "Testable logging",
            "Testbar logging",
        ),
        (
            "Registra una decisión recuperable y comprueba el evento con caplog.",
            "Log a recoverable decision and check the event with caplog.",
            "Log en håndterbar beslutning og kontrollér hændelsen med caplog.",
        ),
        (
            (
                "La función devuelve el resultado funcional.",
                "The function returns the functional result.",
                "Funktionen returnerer det funktionelle resultat.",
            ),
            (
                "El log aporta contexto adicional sin sustituirlo.",
                "The log adds context without replacing the result.",
                "Loggen tilføjer kontekst uden at erstatte resultatet.",
            ),
        ),
        """import logging


LOGGER = logging.getLogger(__name__)


def safe_fraction(numerator: int, denominator: int) -> float:
    if denominator == 0:
        LOGGER.warning(\"zero denominator; returning 0.0\")
        return 0.0
    return numerator / denominator


def test_safe_fraction_logs_zero_denominator(caplog) -> None:
    with caplog.at_level(logging.WARNING):
        result = safe_fraction(3, 0)

    assert result == 0.0
    assert \"zero denominator\" in caplog.text
""",
        "1 passed",
        (
            "La salida funcional y la observabilidad se comprueban por canales separados.",
            "Functional output and observability are checked through separate channels.",
            "Funktionelt output og observerbarhed kontrolleres gennem separate kanaler.",
        ),
    ),
    (
        "m14.e05",
        (
            "Comprobar una propiedad",
            "Check a property",
            "Kontrollér en egenskab",
        ),
        (
            "Valida que aplicar dos veces el complemento inverso conserva secuencias válidas.",
            "Validate that applying reverse complement twice preserves valid sequences.",
            "Validér at to anvendelser af omvendt komplement bevarer gyldige sekvenser.",
        ),
        (
            (
                "La propiedad no depende de una salida concreta.",
                "The property does not depend on one concrete output.",
                "Egenskaben afhænger ikke af ét konkret output.",
            ),
            (
                "Se usan casos reproducibles para ilustrar el principio.",
                "Reproducible cases illustrate the principle.",
                "Reproducerbare cases illustrerer princippet.",
            ),
        ),
        """from random import Random


def reverse_complement(sequence: str) -> str:
    return sequence.translate(str.maketrans(\"ACGT\", \"TGCA\"))[::-1]


def test_reverse_complement_is_an_involution() -> None:
    rng = Random(7)
    for length in range(1, 30):
        sequence = \"\".join(rng.choice(\"ACGT\") for _ in range(length))
        assert reverse_complement(reverse_complement(sequence)) == sequence
""",
        "1 passed",
        (
            "El bucle representa una propiedad; una herramienta especializada puede ampliar y reducir casos.",
            "The loop represents a property; a specialized tool can broaden and shrink cases.",
            "Løkken repræsenterer en egenskab; et specialiseret værktøj kan udvide og minimere cases.",
        ),
    ),
)

_PRACTICES = (
    (
        "m14.p01",
        "SHORT_ANSWER",
        (
            "Distingue fallo, error y defecto en un flujo de pruebas.",
            "Distinguish failure, error, and defect in a testing workflow.",
            "Skeln mellem failure, error og defect i et testworkflow.",
        ),
        (
            (
                "Relaciona observación y causa.",
                "Relate observation and cause.",
                "Knyt observation og årsag.",
            ),
        ),
        (
            "Un fallo es una conducta observada incorrecta; un error puede describir un estado o acción humana incorrecta; un defecto es la causa incorporada al artefacto.",
            "A failure is observed incorrect behavior; an error may describe an incorrect human action or state; a defect is the cause embedded in the artifact.",
            "En failure er observeret forkert adfærd; en error kan beskrive en forkert menneskelig handling eller tilstand; en defect er årsagen indlejret i artefaktet.",
        ),
        (
            "La terminología puede variar, pero debe mantenerse coherente en el análisis.",
            "Terminology varies, but it should remain consistent within the analysis.",
            "Terminologien kan variere, men bør bruges konsekvent i analysen.",
        ),
        "",
    ),
    (
        "m14.p02",
        "CODE_TRACING",
        (
            "Traza qué casos ejecuta @pytest.mark.parametrize con tres filas.",
            "Trace which cases a three-row @pytest.mark.parametrize executes.",
            "Gennemgå hvilke cases en @pytest.mark.parametrize med tre rækker udfører.",
        ),
        (
            (
                "Cada fila crea una invocación.",
                "Each row creates one invocation.",
                "Hver række skaber ét kald.",
            ),
        ),
        (
            "La función de prueba se ejecuta tres veces, una por conjunto de argumentos, y cada caso se informa de forma independiente.",
            "The test function runs three times, once per argument set, and each case is reported independently.",
            "Testfunktionen kører tre gange, én gang pr. argumentsæt, og hver case rapporteres separat.",
        ),
        (
            "Un fallo no impide identificar los otros casos.",
            "One failure does not hide the identities of the other cases.",
            "Én fejl skjuler ikke identiteten af de andre cases.",
        ),
        "",
    ),
    (
        "m14.p03",
        "DEBUGGING",
        (
            "Una prueba pasa aunque la función incorrecta nunca se ejecuta. Diagnostica.",
            "A test passes although the incorrect function never executes. Diagnose it.",
            "En test består selv om den forkerte funktion aldrig udføres. Diagnosticér.",
        ),
        (
            (
                "Revisa acción y aserción.",
                "Inspect action and assertion.",
                "Undersøg handling og assertion.",
            ),
        ),
        (
            "La prueba puede limitarse a comprobar datos preparados o una constante. Debe ejecutar la unidad real y verificar un resultado que cambie si la implementación falla.",
            "The test may only check prepared data or a constant. It should execute the real unit and verify a result that changes when the implementation is wrong.",
            "Testen kontrollerer måske kun forberedte data eller en konstant. Den bør udføre den reelle enhed og kontrollere et resultat der ændres ved forkert implementering.",
        ),
        (
            "Una prueba que no puede fallar no protege el contrato.",
            "A test that cannot fail does not protect the contract.",
            "En test der ikke kan fejle beskytter ikke kontrakten.",
        ),
        "",
    ),
    (
        "m14.p04",
        "FILL_IN_THE_BLANK",
        (
            "Completa: pytest comprueba una excepción con ________.",
            "Complete: pytest checks an exception with ________.",
            "Udfyld: pytest kontrollerer en exception med ________.",
        ),
        (("Es un context manager.", "It is a context manager.", "Det er en context manager."),),
        ("pytest.raises", "pytest.raises", "pytest.raises"),
        (
            "El contexto debe envolver sólo la operación que se espera que falle.",
            "The context should wrap only the operation expected to fail.",
            "Konteksten bør kun omslutte operationen der forventes at fejle.",
        ),
        "",
    ),
    (
        "m14.p05",
        "CODE_COMPLETION",
        (
            "Completa una prueba parametrizada para valores límite.",
            "Complete a parametrized test for boundary values.",
            "Færdiggør en parametriseret test for grænseværdier.",
        ),
        (
            (
                "Incluye el decorador y una aserción.",
                "Include the decorator and an assertion.",
                "Medtag decorator og assertion.",
            ),
        ),
        (
            "@pytest.mark.parametrize(('value', 'expected'), [(0, False), (1, True)])\ndef test_is_positive(value, expected):\n    assert is_positive(value) is expected",
            "@pytest.mark.parametrize(('value', 'expected'), [(0, False), (1, True)])\ndef test_is_positive(value, expected):\n    assert is_positive(value) is expected",
            "@pytest.mark.parametrize(('value', 'expected'), [(0, False), (1, True)])\ndef test_is_positive(value, expected):\n    assert is_positive(value) is expected",
        ),
        (
            "Los límites cero y uno definen la transición del contrato.",
            "Zero and one define the contract boundary.",
            "Nul og én definerer kontraktens grænse.",
        ),
        "import pytest\n\n\ndef is_positive(value: int) -> bool:\n    return value > 0\n\n\n# Add a parametrized test.\n",
    ),
    (
        "m14.p06",
        "DATA_INTERPRETATION",
        (
            "Una suite tiene 99 % de cobertura pero falla con entradas vacías. Interpreta.",
            "A suite has 99% coverage but fails on empty inputs. Interpret it.",
            "En suite har 99 % coverage men fejler på tomme input. Fortolk.",
        ),
        (
            (
                "Cobertura mide ejecución, no calidad del contrato.",
                "Coverage measures execution, not contract quality.",
                "Coverage måler udførelse, ikke kontraktkvalitet.",
            ),
        ),
        (
            "La cobertura alta no garantiza casos frontera ni aserciones significativas. Debe añadirse el caso vacío y revisar qué conductas están realmente verificadas.",
            "High coverage does not guarantee boundary cases or meaningful assertions. Add the empty case and review which behaviors are actually verified.",
            "Høj coverage garanterer ikke grænsetilfælde eller meningsfulde assertions. Tilføj den tomme case og gennemgå hvilke adfærdsmønstre der faktisk verificeres.",
        ),
        (
            "La cobertura es una señal auxiliar, no un objetivo suficiente.",
            "Coverage is an auxiliary signal, not a sufficient objective.",
            "Coverage er et hjælpesignal, ikke et tilstrækkeligt mål.",
        ),
        "",
    ),
    (
        "m14.p07",
        "ORDERING",
        (
            "Ordena un flujo de depuración: reproducir, reducir, formular hipótesis, inspeccionar, corregir, probar regresión.",
            "Order a debugging workflow: reproduce, reduce, hypothesize, inspect, fix, regression-test.",
            "Ordén et fejlsøgningsworkflow: reproducer, reducer, formulér hypotese, undersøg, ret, regressionstest.",
        ),
        (
            (
                "La corrección sigue a la evidencia.",
                "The fix follows evidence.",
                "Rettelsen følger evidensen.",
            ),
        ),
        (
            "Reproducir → reducir → formular hipótesis → inspeccionar → corregir → añadir prueba de regresión.",
            "Reproduce → reduce → form a hypothesis → inspect → fix → add a regression test.",
            "Reproducer → reducer → formulér hypotese → undersøg → ret → tilføj regressionstest.",
        ),
        (
            "El proceso puede iterar, pero cada cambio debe responder a una hipótesis.",
            "The process may iterate, but each change should answer a hypothesis.",
            "Processen kan iterere, men hver ændring bør besvare en hypotese.",
        ),
        "",
    ),
    (
        "m14.p08",
        "PIPELINE_DESIGN",
        (
            "Diseña pruebas para una función que carga, valida y resume una tabla.",
            "Design tests for a function that loads, validates, and summarizes a table.",
            "Design tests for en funktion der indlæser, validerer og opsummerer en tabel.",
        ),
        (
            (
                "Separa responsabilidades y niveles.",
                "Separate responsibilities and levels.",
                "Adskil ansvar og niveauer.",
            ),
        ),
        (
            "Probar validadores puros con casos parametrizados; probar carga con archivos temporales; comprobar errores de esquema; integrar con una tabla pequeña; validar conteos, tipos y ausencia de estado compartido.",
            "Test pure validators with parametrized cases; test loading with temporary files; check schema errors; integrate with a small table; validate counts, types, and absence of shared state.",
            "Test rene validatorer med parametriserede cases; test indlæsning med midlertidige filer; kontrollér schemafejl; integrér med en lille tabel; validér antal, typer og fravær af delt tilstand.",
        ),
        (
            "Las pruebas unitarias e integradas responden preguntas distintas.",
            "Unit and integration tests answer different questions.",
            "Enheds- og integrationstests besvarer forskellige spørgsmål.",
        ),
        "",
    ),
    (
        "m14.p09",
        "ORAL_EXPLANATION",
        (
            "Explica por qué mockear todo puede reducir la confianza.",
            "Explain why mocking everything can reduce confidence.",
            "Forklar hvorfor mocking af alt kan reducere tilliden.",
        ),
        (
            (
                "Compara aislamiento y realidad.",
                "Compare isolation and reality.",
                "Sammenlign isolation og virkelighed.",
            ),
        ),
        (
            "Los mocks aíslan dependencias, pero una prueba puede terminar verificando sólo interacciones artificiales. Deben usarse en límites variables y combinarse con pruebas que integren componentes reales.",
            "Mocks isolate dependencies, but a test may end up checking only artificial interactions. Use them at variable boundaries and combine them with tests integrating real components.",
            "Mocks isolerer afhængigheder, men en test kan ende med kun at kontrollere kunstige interaktioner. Brug dem ved variable grænser og kombiner med tests af reelle komponenter.",
        ),
        (
            "El objetivo es controlar incertidumbre, no reemplazar todo el sistema.",
            "The goal is to control uncertainty, not replace the whole system.",
            "Målet er at kontrollere usikkerhed, ikke erstatte hele systemet.",
        ),
        "",
    ),
    (
        "m14.p10",
        "DEBUGGING",
        (
            "Un test depende del orden de ejecución. Propón una corrección.",
            "A test depends on execution order. Propose a fix.",
            "En test afhænger af udførelsesrækkefølgen. Foreslå en rettelse.",
        ),
        (
            (
                "Busca estado global mutable.",
                "Look for mutable global state.",
                "Søg efter mutabel global tilstand.",
            ),
        ),
        (
            "Crear estado nuevo por prueba, restaurar recursos modificados, evitar mutación global y usar fixtures con alcance function. Ejecutar la prueba sola y en orden aleatorio para confirmar aislamiento.",
            "Create fresh state per test, restore modified resources, avoid global mutation, and use function-scoped fixtures. Run the test alone and in randomized order to confirm isolation.",
            "Opret ny tilstand pr. test, gendan ændrede ressourcer, undgå global mutation og brug function-scoped fixtures. Kør testen alene og i tilfældig rækkefølge for at bekræfte isolation.",
        ),
        (
            "Las pruebas deben ser independientes y repetibles.",
            "Tests should be independent and repeatable.",
            "Tests bør være uafhængige og gentagelige.",
        ),
        "",
    ),
    (
        "m14.p11",
        "SHORT_ANSWER",
        (
            "Distingue DEBUG, INFO, WARNING y ERROR.",
            "Distinguish DEBUG, INFO, WARNING, and ERROR.",
            "Skeln mellem DEBUG, INFO, WARNING og ERROR.",
        ),
        (("Relaciona nivel e impacto.", "Relate level and impact.", "Knyt niveau og påvirkning."),),
        (
            "DEBUG detalla diagnóstico; INFO confirma funcionamiento normal; WARNING señala una condición recuperable; ERROR registra que una operación no pudo completarse.",
            "DEBUG provides diagnostic detail; INFO confirms normal operation; WARNING marks a recoverable condition; ERROR records that an operation could not complete.",
            "DEBUG giver diagnostiske detaljer; INFO bekræfter normal drift; WARNING markerer en håndterbar tilstand; ERROR registrerer at en operation ikke kunne fuldføres.",
        ),
        (
            "La política concreta debe ser coherente dentro de la aplicación.",
            "The concrete policy should remain consistent within the application.",
            "Den konkrete politik bør være konsekvent i applikationen.",
        ),
        "",
    ),
    (
        "m14.p12",
        "PIPELINE_DESIGN",
        (
            "Diseña una estrategia de propiedades para complemento inverso.",
            "Design a property strategy for reverse complement.",
            "Design en egenskabsstrategi for omvendt komplement.",
        ),
        (
            (
                "Incluye dominio y oráculo alternativo.",
                "Include domain and an alternative oracle.",
                "Medtag domæne og alternativt orakel.",
            ),
        ),
        (
            "Generar cadenas A/C/G/T de longitudes variadas; comprobar doble aplicación, conservación de longitud y alfabeto; conservar ejemplos conocidos; comparar algunos casos con una implementación simple independiente.",
            "Generate A/C/G/T strings of varied lengths; check double application, length and alphabet preservation; retain known examples; compare selected cases with an independent simple implementation.",
            "Generér A/C/G/T-strenge med varierede længder; kontrollér dobbelt anvendelse, bevarelse af længde og alfabet; behold kendte eksempler; sammenlign udvalgte cases med en uafhængig simpel implementering.",
        ),
        (
            "Las propiedades deben fallar ante implementaciones plausibles pero incorrectas.",
            "Properties should fail for plausible but incorrect implementations.",
            "Egenskaber bør fejle for plausible men forkerte implementeringer.",
        ),
        "",
    ),
)

LOCALIZED_MODULE_14_TESTING_DEBUGGING_QUALITY = LocalizedLearningModule(
    course_code="DM857",
    module_id="dm857.m14",
    title=t(
        "Testing, depuración y calidad del software",
        "Testing, debugging, and software quality",
        "Testning, fejlsøgning og softwarekvalitet",
    ),
    summary=t(
        "Este módulo desarrolla pruebas automatizadas con pytest, fixtures, parametrización, errores esperados, depuración sistemática, logging, diseño para testabilidad y propiedades.",
        "This module develops automated testing with pytest, fixtures, parametrization, expected errors, systematic debugging, logging, design for testability, and properties.",
        "Dette modul udvikler automatiseret testning med pytest, fixtures, parametrisering, forventede fejl, systematisk fejlsøgning, logging, design for testbarhed og egenskaber.",
    ),
    objectives=tuple(objective(item_id, text) for item_id, text in _OBJECTIVES),
    concepts=tuple(
        concept(concept_id, title, body, key_points)
        for concept_id, title, body, key_points in _CONCEPTS
    ),
    worked_examples=tuple(
        example(example_id, title, problem, reasoning, code, expected_output, explanation)
        for example_id, title, problem, reasoning, code, expected_output, explanation in _EXAMPLES
    ),
    practice_exercises=tuple(
        practice(
            exercise_id,
            ActivityType[activity_type],
            prompt,
            hints,
            solution,
            explanation,
            starter_code,
        )
        for exercise_id, activity_type, prompt, hints, solution, explanation, starter_code in _PRACTICES
    ),
    assessment_items=(
        authored_item(
            "dm857.m14.assessment.001",
            ActivityType.MULTIPLE_CHOICE,
            (
                "¿Qué protege principalmente una prueba de regresión?",
                "What does a regression test primarily protect?",
                "Hvad beskytter en regressionstest primært?",
            ),
            (),
            (
                "Protege una conducta previamente corregida frente a reapariciones.",
                "It protects previously fixed behavior from reappearing.",
                "Den beskytter tidligere rettet adfærd mod at dukke op igen.",
            ),
            options=(
                (
                    "fixed",
                    (
                        "Un fallo previamente corregido",
                        "A previously fixed failure",
                        "En tidligere rettet fejl",
                    ),
                ),
                ("style", ("Sólo el estilo visual", "Only visual style", "Kun visuel stil")),
                (
                    "speed",
                    (
                        "Toda degradación de velocidad",
                        "Every speed degradation",
                        "Enhver hastighedsforringelse",
                    ),
                ),
            ),
            correct_option_ids=("fixed",),
        ),
        authored_item(
            "dm857.m14.assessment.002",
            ActivityType.MULTIPLE_SELECT,
            (
                "Selecciona propiedades de una prueba fiable.",
                "Select properties of a reliable test.",
                "Vælg egenskaber ved en pålidelig test.",
            ),
            (),
            (
                "Una prueba fiable es aislada, determinista, legible y verifica conducta observable.",
                "A reliable test is isolated, deterministic, readable, and checks observable behavior.",
                "En pålidelig test er isoleret, deterministisk, læsbar og kontrollerer observerbar adfærd.",
            ),
            options=(
                ("isolated", ("Aislada", "Isolated", "Isoleret")),
                ("deterministic", ("Determinista", "Deterministic", "Deterministisk")),
                ("readable", ("Legible", "Readable", "Læsbar")),
                ("behavior", ("Comprueba conducta", "Checks behavior", "Kontrollerer adfærd")),
                ("ordered", ("Depende del orden", "Depends on order", "Afhænger af rækkefølge")),
            ),
            correct_option_ids=("isolated", "deterministic", "readable", "behavior"),
        ),
        authored_item(
            "dm857.m14.assessment.003",
            ActivityType.TRUE_FALSE,
            (
                "Una cobertura del 100 % demuestra que el programa es correcto.",
                "One hundred percent coverage proves the program is correct.",
                "Hundrede procent coverage beviser at programmet er korrekt.",
            ),
            (),
            (
                "La cobertura indica ejecución, no suficiencia de casos ni aserciones.",
                "Coverage indicates execution, not sufficient cases or assertions.",
                "Coverage viser udførelse, ikke tilstrækkelige cases eller assertions.",
            ),
            options=(
                ("true", ("Verdadero", "True", "Sandt")),
                ("false", ("Falso", "False", "Falsk")),
            ),
            correct_option_ids=("false",),
        ),
        authored_item(
            "dm857.m14.assessment.004",
            ActivityType.MATCHING,
            (
                "Relaciona el síntoma con la primera acción adecuada.",
                "Match the symptom to the appropriate first action.",
                "Match symptomet med den passende første handling.",
            ),
            (),
            (
                "Los fallos intermitentes requieren control de no determinismo; los de orden requieren aislamiento; una excepción exige leer el traceback.",
                "Intermittent failures require control of nondeterminism; order failures require isolation; an exception requires reading the traceback.",
                "Intermitterende fejl kræver kontrol af ikke-determinisme; rækkefølgefejl kræver isolation; en exception kræver læsning af traceback.",
            ),
            options=(
                (
                    "flaky-seed",
                    (
                        "Intermitente → fijar semilla y entorno",
                        "Flaky → fix seed and environment",
                        "Intermitterende → fastsæt seed og miljø",
                    ),
                ),
                (
                    "order-state",
                    (
                        "Depende del orden → revisar estado compartido",
                        "Order-dependent → inspect shared state",
                        "Rækkefølgeafhængig → undersøg delt tilstand",
                    ),
                ),
                (
                    "exception-trace",
                    (
                        "Excepción → leer traceback",
                        "Exception → read traceback",
                        "Exception → læs traceback",
                    ),
                ),
            ),
            correct_option_ids=("flaky-seed", "order-state", "exception-trace"),
        ),
        authored_item(
            "dm857.m14.assessment.005",
            ActivityType.ORDERING,
            (
                "Ordena un ciclo de corrección de defectos.",
                "Order a defect-fixing cycle.",
                "Ordén en cyklus for fejlrettelse.",
            ),
            (),
            (
                "Reproducir → prueba fallida → localizar causa → corregir → validar suite.",
                "Reproduce → failing test → locate cause → fix → validate suite.",
                "Reproducer → fejlet test → lokalisér årsag → ret → validér suite.",
            ),
            options=(
                ("reproduce", ("Reproducir", "Reproduce", "Reproducer")),
                ("test", ("Crear prueba que falla", "Create failing test", "Opret fejlet test")),
                ("locate", ("Localizar causa", "Locate cause", "Lokalisér årsag")),
                ("fix", ("Corregir", "Fix", "Ret")),
                ("validate", ("Validar suite", "Validate suite", "Validér suite")),
            ),
            correct_option_ids=("reproduce", "test", "locate", "fix", "validate"),
        ),
        authored_item(
            "dm857.m14.assessment.006",
            ActivityType.FILL_IN_THE_BLANK,
            (
                "Completa la fixture integrada que ofrece un directorio temporal: ________.",
                "Complete the built-in fixture providing a temporary directory: ________.",
                "Udfyld den indbyggede fixture der giver en midlertidig mappe: ________.",
            ),
            (("tmp_path", "tmp_path", "tmp_path"),),
            (
                "tmp_path entrega un objeto Path aislado por prueba.",
                "tmp_path provides a Path object isolated per test.",
                "tmp_path giver et Path-objekt isoleret pr. test.",
            ),
        ),
        authored_item(
            "dm857.m14.assessment.007",
            ActivityType.CODE_COMPLETION,
            (
                "Escribe una prueba que rechace una lista vacía con ValueError.",
                "Write a test rejecting an empty list with ValueError.",
                "Skriv en test der afviser en tom liste med ValueError.",
            ),
            (
                (
                    "def test_mean_rejects_empty():\n    with pytest.raises(ValueError):\n        mean([])",
                    "def test_mean_rejects_empty():\n    with pytest.raises(ValueError):\n        mean([])",
                    "def test_mean_rejects_empty():\n    with pytest.raises(ValueError):\n        mean([])",
                ),
            ),
            (
                "El contexto envuelve únicamente la llamada que debe fallar.",
                "The context wraps only the call expected to fail.",
                "Konteksten omslutter kun kaldet der forventes at fejle.",
            ),
            rubric=(
                ("Usa pytest.raises.", "Uses pytest.raises.", "Bruger pytest.raises."),
                ("Ejecuta mean([]).", "Executes mean([]).", "Udfører mean([])."),
            ),
        ),
        authored_item(
            "dm857.m14.assessment.008",
            ActivityType.DEBUGGING,
            (
                "Dos pruebas pasan por separado y fallan juntas. Diagnostica y corrige.",
                "Two tests pass separately and fail together. Diagnose and fix.",
                "To tests består separat men fejler sammen. Diagnosticér og ret.",
            ),
            (
                (
                    "Buscar estado mutable compartido, cachés, variables globales o recursos no restaurados; crear estado nuevo por prueba y añadir limpieza mediante fixtures.",
                    "Look for shared mutable state, caches, globals, or unrestored resources; create fresh state per test and add fixture cleanup.",
                    "Søg efter delt mutabel tilstand, caches, globale variabler eller ikke-gendannede ressourcer; opret ny tilstand pr. test og tilføj fixture-oprydning.",
                ),
            ),
            (
                "La dependencia del orden indica pérdida de aislamiento.",
                "Order dependence indicates lost isolation.",
                "Rækkefølgeafhængighed viser manglende isolation.",
            ),
        ),
        authored_item(
            "dm857.m14.assessment.009",
            ActivityType.SHORT_ANSWER,
            (
                "Explica cuándo una fixture de alcance session es justificable.",
                "Explain when a session-scoped fixture is justified.",
                "Forklar hvornår en session-scoped fixture er berettiget.",
            ),
            (
                (
                    "Cuando crear un recurso inmutable o cuidadosamente restablecido es costoso y compartirlo no permite que una prueba altere el estado observado por otra.",
                    "When creating an immutable or carefully reset resource is expensive and sharing it cannot let one test alter state observed by another.",
                    "Når oprettelse af en uforanderlig eller omhyggeligt nulstillet ressource er dyr, og deling ikke lader én test ændre tilstand observeret af en anden.",
                ),
            ),
            (
                "El rendimiento no debe comprarse a costa de aislamiento oculto.",
                "Performance should not be bought at the cost of hidden coupling.",
                "Ydelse bør ikke købes på bekostning af skjult kobling.",
            ),
        ),
        authored_item(
            "dm857.m14.assessment.010",
            ActivityType.DATA_INTERPRETATION,
            (
                "Una prueba falla una vez de cada cien ejecuciones. Interpreta la señal.",
                "A test fails once in every hundred runs. Interpret the signal.",
                "En test fejler én gang pr. hundrede kørsler. Fortolk signalet.",
            ),
            (
                (
                    "Es una prueba flaky o un defecto no determinista. Deben registrarse semillas, tiempo, concurrencia y entorno, y reducirse el caso antes de reintentar ciegamente.",
                    "It is a flaky test or nondeterministic defect. Record seeds, timing, concurrency, and environment, then reduce the case instead of blindly retrying.",
                    "Det er en flaky test eller ikke-deterministisk fejl. Registrér seeds, timing, samtidighed og miljø, og reducer casen i stedet for blindt at genkøre.",
                ),
            ),
            (
                "Reintentar puede ocultar el problema sin eliminarlo.",
                "Retrying may hide the problem without removing it.",
                "Genkørsel kan skjule problemet uden at fjerne det.",
            ),
        ),
        authored_item(
            "dm857.m14.assessment.011",
            ActivityType.PIPELINE_DESIGN,
            (
                "Diseña la estrategia de pruebas para un pequeño pipeline de secuencias.",
                "Design a testing strategy for a small sequence pipeline.",
                "Design en teststrategi for et lille sekvenspipeline.",
            ),
            (
                (
                    "Pruebas unitarias para normalización y validación; parametrización de alfabetos y límites; archivos temporales para E/S; integración con una muestra pequeña; errores esperados; propiedades de longitud y complemento; regresiones para defectos conocidos.",
                    "Unit tests for normalization and validation; parametrized alphabets and boundaries; temporary files for I/O; integration with a small sample; expected errors; length and complement properties; regressions for known defects.",
                    "Enhedstests for normalisering og validering; parametriserede alfabeter og grænser; midlertidige filer til I/O; integration med en lille prøve; forventede fejl; længde- og komplementeegenskaber; regressioner for kendte fejl.",
                ),
            ),
            (
                "La estrategia combina niveles y oráculos distintos.",
                "The strategy combines different levels and oracles.",
                "Strategien kombinerer forskellige niveauer og orakler.",
            ),
            rubric=(
                ("Incluye límites.", "Includes boundaries.", "Medtager grænser."),
                ("Incluye integración.", "Includes integration.", "Medtager integration."),
                ("Incluye propiedades.", "Includes properties.", "Medtager egenskaber."),
            ),
        ),
        authored_item(
            "dm857.m14.assessment.012",
            ActivityType.ORAL_EXPLANATION,
            (
                "Explica diseño para testabilidad con una dependencia de tiempo.",
                "Explain design for testability using a time dependency.",
                "Forklar design for testbarhed med en tidsafhængighed.",
            ),
            (
                (
                    "En función no debería leer siempre el reloj global. Puede recibir una función clock o un timestamp; la prueba inyecta un valor fijo y verifica el comportamiento de forma determinista.",
                    "A function should not always read the global clock. It can receive a clock function or timestamp; the test injects a fixed value and checks behavior deterministically.",
                    "En funktion bør ikke altid læse det globale ur. Den kan modtage en clock-funktion eller timestamp; testen injicerer en fast værdi og kontrollerer adfærd deterministisk.",
                ),
            ),
            (
                "La dependencia explícita convierte el tiempo en entrada controlable.",
                "The explicit dependency turns time into a controllable input.",
                "Den eksplicitte afhængighed gør tid til et kontrollerbart input.",
            ),
        ),
        authored_item(
            "dm857.m14.assessment.013",
            ActivityType.CODE_TRACING,
            (
                "Traza una fixture function usada por tres pruebas.",
                "Trace a function-scoped fixture used by three tests.",
                "Gennemgå en function-scoped fixture brugt af tre tests.",
            ),
            (
                (
                    "La fixture se prepara tres veces y cada prueba recibe una instancia independiente; la limpieza ocurre después de cada caso si usa yield.",
                    "The fixture is set up three times and each test receives an independent instance; cleanup occurs after each case when yield is used.",
                    "Fixturen opsættes tre gange og hver test modtager en uafhængig instans; oprydning sker efter hver case når yield bruges.",
                ),
            ),
            (
                "El alcance function prioriza aislamiento.",
                "Function scope prioritizes isolation.",
                "Function-scope prioriterer isolation.",
            ),
        ),
        authored_item(
            "dm857.m14.assessment.014",
            ActivityType.MULTIPLE_CHOICE,
            (
                "¿Qué propiedad es adecuada para complemento inverso?",
                "Which property is suitable for reverse complement?",
                "Hvilken egenskab er passende for omvendt komplement?",
            ),
            (),
            (
                "Aplicarlo dos veces recupera la secuencia válida original.",
                "Applying it twice recovers the original valid sequence.",
                "To anvendelser genskaber den oprindelige gyldige sekvens.",
            ),
            options=(
                ("twice", ("rc(rc(s)) == s", "rc(rc(s)) == s", "rc(rc(s)) == s")),
                (
                    "empty",
                    (
                        "Siempre devuelve vacío",
                        "Always returns empty",
                        "Returnerer altid tom streng",
                    ),
                ),
                (
                    "longer",
                    ("Siempre aumenta longitud", "Always increases length", "Øger altid længden"),
                ),
            ),
            correct_option_ids=("twice",),
        ),
    ),
    tutor_support=tutor_support(
        (
            "Las pruebas automatizadas convierten contratos de comportamiento en comprobaciones ejecutables. Una prueba prepara entradas y dependencias, ejecuta una conducta y verifica resultados observables. No demuestra corrección universal, pero reduce regresiones y documenta expectativas. pytest descubre funciones de prueba y mejora los diagnósticos de assert. Arrange–Act–Assert mantiene visible la separación entre preparación, ejecución y comprobación. La parametrización aplica el mismo contrato a casos típicos, límites, entradas vacías e inválidas sin duplicar estructura. Las fixtures gestionan datos y recursos reutilizables; el alcance function favorece aislamiento, mientras alcances más amplios requieren demostrar que el estado no se comparte de forma peligrosa. pytest.raises debe envolver sólo la llamada que se espera que genere una excepción. Las advertencias y logs también pueden formar parte del contrato cuando su presencia es relevante. Depurar exige reproducir, conservar el traceback, reducir el caso, formular una hipótesis e inspeccionar el estado antes de modificar código. Una corrección completa añade una prueba de regresión y elimina diagnósticos temporales. logging separa observabilidad de salida funcional mediante niveles y contexto; no debe exponer datos sensibles ni configurarse globalmente desde bibliotecas. El diseño para testabilidad separa cálculo puro de E/S, inyecta dependencias variables y hace explícito el no determinismo. Las pruebas basadas en propiedades generan múltiples entradas y comprueban invariantes independientes, como conservación de longitud o doble complemento inverso. Estas propiedades complementan ejemplos concretos, pruebas de integración y casos de regresión. La cobertura de código indica qué líneas se ejecutaron, no si se probaron contratos suficientes. Los ejemplos biomédicos son ejercicios didácticos de programación y control de calidad; no representan protocolos de laboratorio, validación clínica ni recomendaciones diagnósticas.",
            "Automated tests turn behavioral contracts into executable checks. A test prepares inputs and dependencies, executes behavior, and verifies observable results. It does not prove universal correctness, but it reduces regressions and documents expectations. pytest discovers test functions and improves assert diagnostics. Arrange–Act–Assert keeps setup, execution, and checking visibly separate. Parametrization applies the same contract to typical cases, boundaries, empty inputs, and invalid inputs without duplicating structure. Fixtures manage reusable data and resources; function scope favors isolation, while broader scopes require evidence that state is not shared dangerously. pytest.raises should wrap only the call expected to raise. Warnings and logs may also belong to the contract when their presence matters. Debugging requires reproducing the failure, preserving the traceback, reducing the case, forming a hypothesis, and inspecting state before editing code. A complete fix adds a regression test and removes temporary diagnostics. logging separates observability from functional output through levels and context; libraries should not configure it globally or expose sensitive data. Design for testability separates pure computation from I/O, injects variable dependencies, and makes nondeterminism explicit. Property-based tests generate multiple inputs and check implementation-independent invariants such as length preservation or double reverse complement. These properties complement concrete examples, integration tests, and regression cases. Code coverage shows which lines ran, not whether enough contracts were tested. Biomedical examples are teaching exercises in programming and quality control; they are not laboratory protocols, clinical validation, or diagnostic recommendations.",
            "Automatiserede tests omsætter adfærdskontrakter til eksekverbare kontroller. En test forbereder input og afhængigheder, udfører adfærd og verificerer observerbare resultater. Den beviser ikke universel korrekthed, men reducerer regressioner og dokumenterer forventninger. pytest finder testfunktioner og forbedrer assert-diagnostik. Arrange–Act–Assert holder forberedelse, udførelse og kontrol synligt adskilt. Parametrisering anvender samme kontrakt på typiske cases, grænser, tomme og ugyldige input uden duplikeret struktur. Fixtures håndterer genbrugelige data og ressourcer; function-scope fremmer isolation, mens bredere scopes kræver dokumentation for at tilstand ikke deles farligt. pytest.raises bør kun omslutte kaldet der forventes at give en exception. Advarsler og logs kan også være en del af kontrakten. Fejlsøgning kræver reproduktion, bevarelse af traceback, reduktion af casen, formulering af hypotese og inspektion af tilstand før kode ændres. En komplet rettelse tilføjer en regressionstest og fjerner midlertidig diagnostik. logging adskiller observerbarhed fra funktionelt output gennem niveauer og kontekst og bør ikke eksponere følsomme data. Design for testbarhed adskiller ren beregning fra I/O, injicerer variable afhængigheder og gør ikke-determinisme eksplicit. Egenskabsbaserede tests genererer flere input og kontrollerer implementeringsuafhængige invarianter som bevarelse af længde eller dobbelt omvendt komplement. Disse egenskaber supplerer konkrete eksempler, integrationstests og regressioner. Code coverage viser hvilke linjer der blev udført, ikke om tilstrækkelige kontrakter blev testet. Biomedicinske eksempler er undervisningsøvelser i programmering og kvalitetskontrol; de er ikke laboratorieprotokoller, klinisk validering eller diagnostiske anbefalinger.",
        ),
        (
            (
                "Una prueba protege un contrato observable.",
                "A test protects an observable contract.",
                "En test beskytter en observerbar kontrakt.",
            ),
            (
                "Arrange–Act–Assert separa responsabilidades.",
                "Arrange–Act–Assert separates responsibilities.",
                "Arrange–Act–Assert adskiller ansvar.",
            ),
            (
                "La parametrización reutiliza estructura para una conducta.",
                "Parametrization reuses structure for one behavior.",
                "Parametrisering genbruger struktur for én adfærd.",
            ),
            (
                "Las fixtures deben conservar aislamiento.",
                "Fixtures should preserve isolation.",
                "Fixtures bør bevare isolation.",
            ),
            (
                "pytest.raises debe tener alcance estrecho.",
                "pytest.raises should have narrow scope.",
                "pytest.raises bør have smalt scope.",
            ),
            (
                "Los límites deben elegirse por el contrato.",
                "Boundaries should follow the contract.",
                "Grænser bør følge kontrakten.",
            ),
            (
                "El traceback contiene evidencia causal.",
                "The traceback contains causal evidence.",
                "Traceback indeholder kausal evidens.",
            ),
            (
                "Una corrección requiere una prueba de regresión.",
                "A fix requires a regression test.",
                "En rettelse kræver en regressionstest.",
            ),
            (
                "Logging y resultado funcional son canales distintos.",
                "Logging and functional output are separate channels.",
                "Logging og funktionelt output er separate kanaler.",
            ),
            (
                "La inyección controla dependencias variables.",
                "Injection controls variable dependencies.",
                "Injektion kontrollerer variable afhængigheder.",
            ),
            (
                "Las propiedades comprueban invariantes generales.",
                "Properties check general invariants.",
                "Egenskaber kontrollerer generelle invarianter.",
            ),
            (
                "La cobertura no equivale a corrección.",
                "Coverage does not equal correctness.",
                "Coverage er ikke det samme som korrekthed.",
            ),
            (
                "Las pruebas unitarias e integradas responden preguntas distintas.",
                "Unit and integration tests answer different questions.",
                "Enheds- og integrationstests besvarer forskellige spørgsmål.",
            ),
            (
                "Las pruebas deben ser repetibles y diagnósticas.",
                "Tests should be repeatable and diagnostic.",
                "Tests bør være gentagelige og diagnostiske.",
            ),
        ),
        (
            (
                "Creer que una prueba que pasa demuestra corrección total.",
                "Believing a passing test proves total correctness.",
                "At tro at en bestået test beviser total korrekthed.",
            ),
            (
                "Confundir cobertura con calidad de pruebas.",
                "Confusing coverage with test quality.",
                "At forveksle coverage med testkvalitet.",
            ),
            (
                "Parametrizar conductas no relacionadas.",
                "Parametrizing unrelated behaviors.",
                "At parametrisere urelateret adfærd.",
            ),
            (
                "Compartir estado mutable entre pruebas.",
                "Sharing mutable state between tests.",
                "At dele mutabel tilstand mellem tests.",
            ),
            (
                "Usar raises alrededor de demasiadas operaciones.",
                "Wrapping too many operations in raises.",
                "At omslutte for mange operationer i raises.",
            ),
            (
                "Corregir sin reproducir el fallo.",
                "Fixing without reproducing the failure.",
                "At rette uden at reproducere fejlen.",
            ),
            (
                "Cambiar varias causas a la vez.",
                "Changing several causes at once.",
                "At ændre flere årsager på én gang.",
            ),
            (
                "Usar print como sistema de logging.",
                "Using print as a logging system.",
                "At bruge print som loggingsystem.",
            ),
            (
                "Mockear toda dependencia real.",
                "Mocking every real dependency.",
                "At mocke enhver reel afhængighed.",
            ),
            (
                "Ocultar el no determinismo dentro de funciones.",
                "Hiding nondeterminism inside functions.",
                "At skjule ikke-determinisme inde i funktioner.",
            ),
            (
                "Formular propiedades que repiten la implementación.",
                "Writing properties that repeat the implementation.",
                "At formulere egenskaber der gentager implementeringen.",
            ),
            (
                "Aceptar pruebas flaky como normales.",
                "Accepting flaky tests as normal.",
                "At acceptere flaky tests som normale.",
            ),
        ),
        (
            (
                "¿Qué contrato protege esta prueba?",
                "Which contract does this test protect?",
                "Hvilken kontrakt beskytter denne test?",
            ),
            (
                "¿Puede la prueba fallar si la implementación es incorrecta?",
                "Can the test fail when the implementation is wrong?",
                "Kan testen fejle når implementeringen er forkert?",
            ),
            (
                "¿Qué caso frontera falta?",
                "Which boundary case is missing?",
                "Hvilket grænsetilfælde mangler?",
            ),
            ("¿Existe estado compartido?", "Is there shared state?", "Findes der delt tilstand?"),
            (
                "¿El bloque raises es más amplio de lo necesario?",
                "Is the raises block wider than necessary?",
                "Er raises-blokken bredere end nødvendigt?",
            ),
            (
                "¿Cuál es la primera línea relevante del traceback?",
                "What is the first relevant traceback line?",
                "Hvad er den første relevante traceback-linje?",
            ),
            (
                "¿Qué hipótesis explica el fallo?",
                "Which hypothesis explains the failure?",
                "Hvilken hypotese forklarer fejlen?",
            ),
            (
                "¿Cómo reducirías el caso?",
                "How would you reduce the case?",
                "Hvordan ville du reducere casen?",
            ),
            (
                "¿Qué información debería registrar el log?",
                "Which information should the log record?",
                "Hvilke oplysninger bør loggen registrere?",
            ),
            (
                "¿Qué dependencia debe inyectarse?",
                "Which dependency should be injected?",
                "Hvilken afhængighed bør injiceres?",
            ),
            (
                "¿Qué invariante es independiente de la implementación?",
                "Which invariant is independent of implementation?",
                "Hvilken invariant er uafhængig af implementeringen?",
            ),
            (
                "¿Qué prueba de regresión conservará la corrección?",
                "Which regression test will preserve the fix?",
                "Hvilken regressionstest vil bevare rettelsen?",
            ),
        ),
        (
            (
                "Identifica el contrato verificable.",
                "Identifies the verifiable contract.",
                "Identificerer den verificerbare kontrakt.",
            ),
            (
                "Separa preparación, acción y aserción.",
                "Separates setup, action, and assertion.",
                "Adskiller forberedelse, handling og assertion.",
            ),
            (
                "Incluye casos normales y frontera.",
                "Includes normal and boundary cases.",
                "Medtager normale cases og grænsetilfælde.",
            ),
            (
                "Mantiene aislamiento y determinismo.",
                "Maintains isolation and determinism.",
                "Bevarer isolation og determinisme.",
            ),
            (
                "Comprueba errores esperados con alcance preciso.",
                "Checks expected errors with precise scope.",
                "Kontrollerer forventede fejl med præcist scope.",
            ),
            (
                "Usa evidencia del traceback y estado.",
                "Uses traceback and state evidence.",
                "Bruger evidens fra traceback og tilstand.",
            ),
            (
                "Propone una corrección ligada a la causa.",
                "Proposes a fix tied to the cause.",
                "Foreslår en rettelse knyttet til årsagen.",
            ),
            (
                "Añade una prueba de regresión.",
                "Adds a regression test.",
                "Tilføjer en regressionstest.",
            ),
            (
                "Distingue logging de salida funcional.",
                "Distinguishes logging from functional output.",
                "Skelner logging fra funktionelt output.",
            ),
            (
                "Formula propiedades independientes.",
                "Formulates independent properties.",
                "Formulerer uafhængige egenskaber.",
            ),
        ),
        (
            (
                "No afirmar que las pruebas demuestran corrección universal.",
                "Do not claim tests prove universal correctness.",
                "Påstå ikke at tests beviser universel korrekthed.",
            ),
            (
                "No ocultar pruebas flaky mediante reintentos.",
                "Do not hide flaky tests with retries.",
                "Skjul ikke flaky tests med genkørsler.",
            ),
            (
                "No recomendar estado global mutable para facilitar pruebas.",
                "Do not recommend mutable global state to ease testing.",
                "Anbefal ikke mutabel global tilstand for at lette tests.",
            ),
            (
                "No registrar datos biomédicos sensibles.",
                "Do not log sensitive biomedical data.",
                "Log ikke følsomme biomedicinske data.",
            ),
            (
                "No tratar cobertura como métrica suficiente.",
                "Do not treat coverage as a sufficient metric.",
                "Behandl ikke coverage som en tilstrækkelig metrik.",
            ),
            (
                "No confundir mock con evidencia de integración real.",
                "Do not confuse mocks with evidence of real integration.",
                "Forveksl ikke mocks med evidens for reel integration.",
            ),
            (
                "No inventar resultados de ejecución.",
                "Do not invent execution results.",
                "Opfind ikke udførelsesresultater.",
            ),
            (
                "Distinguir ejercicios didácticos de validación clínica.",
                "Distinguish teaching exercises from clinical validation.",
                "Skeln mellem undervisningsøvelser og klinisk validering.",
            ),
            (
                "Responder en el idioma activo con terminología técnica precisa.",
                "Answer in the active language with precise technical terminology.",
                "Svar på det aktive sprog med præcis teknisk terminologi.",
            ),
        ),
        (
            "pytest official documentation on test discovery, fixtures, parametrization, exceptions, logging, and warnings.",
            "Python documentation for assertions, exceptions, pdb, logging, and unittest.mock.",
            "Hypothesis documentation on property-based testing and shrinking.",
            "Software testing principles on isolation, regression testing, boundaries, and test doubles.",
            "Python packaging and reproducibility practices used by the project quality workflow.",
        ),
    ),
)

_BANK_MCQS = (
    (
        "001",
        ("¿Qué verifica una prueba?", "What does a test verify?", "Hvad verificerer en test?"),
        (
            (
                "behavior",
                ("Comportamiento observable", "Observable behavior", "Observerbar adfærd"),
            ),
            (
                "intent",
                (
                    "La intención privada del autor",
                    "The author's private intent",
                    "Forfatterens private hensigt",
                ),
            ),
            ("future", ("Todos los casos futuros", "All future cases", "Alle fremtidige cases")),
        ),
        "behavior",
        (
            "Una prueba ejecuta y observa un contrato concreto.",
            "A test executes and observes a concrete contract.",
            "En test udfører og observerer en konkret kontrakt.",
        ),
    ),
    (
        "002",
        (
            "¿Qué patrón separa preparación, acción y comprobación?",
            "Which pattern separates setup, action, and assertion?",
            "Hvilket mønster adskiller forberedelse, handling og assertion?",
        ),
        (
            ("aaa", ("Arrange–Act–Assert", "Arrange–Act–Assert", "Arrange–Act–Assert")),
            ("mvc", ("Model–View–Controller", "Model–View–Controller", "Model–View–Controller")),
            ("fifo", ("FIFO", "FIFO", "FIFO")),
        ),
        "aaa",
        (
            "AAA estructura una prueba legible.",
            "AAA structures a readable test.",
            "AAA strukturerer en læsbar test.",
        ),
    ),
    (
        "003",
        (
            "¿Qué descubre pytest por convención?",
            "What does pytest discover by convention?",
            "Hvad finder pytest efter konvention?",
        ),
        (
            ("test", ("Funciones test_*", "test_* functions", "test_*-funktioner")),
            ("main", ("Sólo main()", "Only main()", "Kun main()")),
            (
                "private",
                ("Sólo funciones privadas", "Only private functions", "Kun private funktioner"),
            ),
        ),
        "test",
        (
            "pytest usa convenciones de nombres para descubrir pruebas.",
            "pytest uses naming conventions for discovery.",
            "pytest bruger navnekonventioner til discovery.",
        ),
    ),
    (
        "004",
        (
            "¿Qué scope crea una fixture por prueba?",
            "Which scope creates a fixture per test?",
            "Hvilket scope opretter en fixture pr. test?",
        ),
        (
            ("function", ("function", "function", "function")),
            ("session", ("session", "session", "session")),
            ("module", ("module", "module", "module")),
        ),
        "function",
        (
            "function maximiza aislamiento por defecto.",
            "function maximizes isolation by default.",
            "function maksimerer isolation som standard.",
        ),
    ),
    (
        "005",
        (
            "¿Qué fixture ofrece una ruta temporal?",
            "Which fixture provides a temporary path?",
            "Hvilken fixture giver en midlertidig sti?",
        ),
        (
            ("tmp", ("tmp_path", "tmp_path", "tmp_path")),
            ("capsys", ("capsys", "capsys", "capsys")),
            ("monkey", ("monkeypatch", "monkeypatch", "monkeypatch")),
        ),
        "tmp",
        (
            "tmp_path entrega un Path temporal aislado.",
            "tmp_path provides an isolated temporary Path.",
            "tmp_path giver en isoleret midlertidig Path.",
        ),
    ),
    (
        "006",
        (
            "¿Qué herramienta ejecuta el mismo test con varios datos?",
            "Which tool runs the same test with several data sets?",
            "Hvilket værktøj kører samme test med flere datasæt?",
        ),
        (
            ("param", ("parametrize", "parametrize", "parametrize")),
            ("skip", ("skip", "skip", "skip")),
            ("xfail", ("xfail", "xfail", "xfail")),
        ),
        "param",
        (
            "parametrize genera una invocación por fila.",
            "parametrize creates one invocation per row.",
            "parametrize skaber ét kald pr. række.",
        ),
    ),
    (
        "007",
        (
            "¿Cómo se comprueba ValueError?",
            "How is ValueError checked?",
            "Hvordan kontrolleres ValueError?",
        ),
        (
            (
                "raises",
                (
                    "pytest.raises(ValueError)",
                    "pytest.raises(ValueError)",
                    "pytest.raises(ValueError)",
                ),
            ),
            ("print", ("print(ValueError)", "print(ValueError)", "print(ValueError)")),
            ("pass", ("pass", "pass", "pass")),
        ),
        "raises",
        (
            "raises verifica una excepción esperada.",
            "raises checks an expected exception.",
            "raises kontrollerer en forventet exception.",
        ),
    ),
    (
        "008",
        (
            "¿Qué indica un test dependiente del orden?",
            "What does an order-dependent test indicate?",
            "Hvad viser en rækkefølgeafhængig test?",
        ),
        (
            ("shared", ("Estado compartido", "Shared state", "Delt tilstand")),
            ("quality", ("Aislamiento perfecto", "Perfect isolation", "Perfekt isolation")),
            ("speed", ("Sólo lentitud", "Only slowness", "Kun langsomhed")),
        ),
        "shared",
        (
            "La dependencia del orden suele revelar estado mutable compartido.",
            "Order dependence often reveals shared mutable state.",
            "Rækkefølgeafhængighed afslører ofte delt mutabel tilstand.",
        ),
    ),
    (
        "009",
        (
            "¿Qué se consulta primero ante una excepción?",
            "What should be inspected first after an exception?",
            "Hvad bør undersøges først efter en exception?",
        ),
        (
            ("trace", ("Traceback", "Traceback", "Traceback")),
            ("theme", ("Tema visual", "Visual theme", "Visuelt tema")),
            ("coverage", ("Porcentaje de cobertura", "Coverage percentage", "Coverage-procent")),
        ),
        "trace",
        (
            "El traceback localiza la ruta y el punto del fallo.",
            "The traceback locates the path and point of failure.",
            "Traceback lokaliserer fejlens vej og punkt.",
        ),
    ),
    (
        "010",
        (
            "¿Qué nivel describe detalle diagnóstico?",
            "Which level describes diagnostic detail?",
            "Hvilket niveau beskriver diagnostiske detaljer?",
        ),
        (
            ("debug", ("DEBUG", "DEBUG", "DEBUG")),
            ("warning", ("WARNING", "WARNING", "WARNING")),
            ("critical", ("CRITICAL exclusivamente", "CRITICAL exclusively", "Kun CRITICAL")),
        ),
        "debug",
        (
            "DEBUG se usa para detalle de diagnóstico.",
            "DEBUG is used for diagnostic detail.",
            "DEBUG bruges til diagnostiske detaljer.",
        ),
    ),
    (
        "011",
        (
            "¿Qué mejora la testabilidad?",
            "What improves testability?",
            "Hvad forbedrer testbarhed?",
        ),
        (
            ("inject", ("Inyectar dependencias", "Inject dependencies", "Injicér afhængigheder")),
            ("global", ("Aumentar estado global", "Increase global state", "Øg global tilstand")),
            ("random", ("Ocultar aleatoriedad", "Hide randomness", "Skjul tilfældighed")),
        ),
        "inject",
        (
            "La inyección permite sustituir dependencias variables.",
            "Injection allows variable dependencies to be replaced.",
            "Injektion gør det muligt at erstatte variable afhængigheder.",
        ),
    ),
    (
        "012",
        (
            "¿Qué es una propiedad de doble complemento inverso?",
            "What is the double reverse-complement property?",
            "Hvad er egenskaben for dobbelt omvendt komplement?",
        ),
        (
            ("same", ("rc(rc(s)) == s", "rc(rc(s)) == s", "rc(rc(s)) == s")),
            ("empty", ("rc(s) siempre vacío", "rc(s) always empty", "rc(s) altid tom")),
            (
                "double",
                (
                    "La longitud siempre se duplica",
                    "Length always doubles",
                    "Længden fordobles altid",
                ),
            ),
        ),
        "same",
        (
            "La operación es una involución sobre secuencias válidas.",
            "The operation is an involution on valid sequences.",
            "Operationen er en involution på gyldige sekvenser.",
        ),
    ),
    (
        "013",
        (
            "¿Qué prueba combina componentes reales?",
            "Which test combines real components?",
            "Hvilken test kombinerer reelle komponenter?",
        ),
        (
            ("integration", ("Prueba de integración", "Integration test", "Integrationstest")),
            ("lint", ("Lint", "Lint", "Lint")),
            ("format", ("Formateo", "Formatting", "Formatering")),
        ),
        "integration",
        (
            "La integración verifica interacción entre componentes.",
            "Integration checks interaction between components.",
            "Integration kontrollerer samspil mellem komponenter.",
        ),
    ),
    (
        "014",
        (
            "¿Qué debe seguir a una corrección?",
            "What should follow a fix?",
            "Hvad bør følge en rettelse?",
        ),
        (
            ("regression", ("Prueba de regresión", "Regression test", "Regressionstest")),
            ("delete", ("Eliminar todas las pruebas", "Delete all tests", "Slet alle tests")),
            ("retry", ("Sólo reintentar", "Only retry", "Kun genkør")),
        ),
        "regression",
        (
            "La regresión conserva el defecto como caso verificable.",
            "The regression keeps the defect as a verifiable case.",
            "Regressionen bevarer fejlen som en verificerbar case.",
        ),
    ),
    (
        "015",
        (
            "¿Qué mide cobertura de líneas?",
            "What does line coverage measure?",
            "Hvad måler line coverage?",
        ),
        (
            ("executed", ("Líneas ejecutadas", "Executed lines", "Udførte linjer")),
            (
                "correct",
                ("Corrección matemática", "Mathematical correctness", "Matematisk korrekthed"),
            ),
            ("requirements", ("Todos los requisitos", "All requirements", "Alle krav")),
        ),
        "executed",
        (
            "La cobertura describe ejecución, no suficiencia semántica.",
            "Coverage describes execution, not semantic sufficiency.",
            "Coverage beskriver udførelse, ikke semantisk tilstrækkelighed.",
        ),
    ),
)

_BANK_TFS = (
    (
        "016",
        (
            "Una prueba puede pasar por una razón incorrecta.",
            "A test can pass for the wrong reason.",
            "En test kan bestå af den forkerte grund.",
        ),
        True,
        (
            "Debe verificarse que ejecuta y observa el contrato real.",
            "Check that it executes and observes the real contract.",
            "Kontrollér at den udfører og observerer den reelle kontrakt.",
        ),
    ),
    (
        "017",
        (
            "Cada prueba debe depender de la anterior.",
            "Each test should depend on the previous one.",
            "Hver test bør afhænge af den foregående.",
        ),
        False,
        (
            "Las pruebas deben ser independientes.",
            "Tests should be independent.",
            "Tests bør være uafhængige.",
        ),
    ),
    (
        "018",
        (
            "Una fixture puede encargarse de limpieza.",
            "A fixture can handle cleanup.",
            "En fixture kan håndtere oprydning.",
        ),
        True,
        (
            "yield permite preparar y limpiar recursos.",
            "yield supports setup and cleanup.",
            "yield understøtter opsætning og oprydning.",
        ),
    ),
    (
        "019",
        (
            "Session scope siempre es mejor que function scope.",
            "Session scope is always better than function scope.",
            "Session-scope er altid bedre end function-scope.",
        ),
        False,
        (
            "El alcance depende del coste y del aislamiento requerido.",
            "Scope depends on cost and required isolation.",
            "Scope afhænger af omkostning og nødvendig isolation.",
        ),
    ),
    (
        "020",
        (
            "Parametrización elimina la necesidad de casos frontera.",
            "Parametrization removes the need for boundary cases.",
            "Parametrisering fjerner behovet for grænsetilfælde.",
        ),
        False,
        (
            "Los casos aún deben seleccionarse según el contrato.",
            "Cases still need to be selected from the contract.",
            "Cases skal stadig vælges ud fra kontrakten.",
        ),
    ),
    (
        "021",
        (
            "pytest.raises debe envolver sólo la operación esperada.",
            "pytest.raises should wrap only the expected operation.",
            "pytest.raises bør kun omslutte den forventede operation.",
        ),
        True,
        (
            "Un bloque estrecho evita falsos positivos.",
            "A narrow block avoids false positives.",
            "En smal blok undgår falske positiver.",
        ),
    ),
    (
        "022",
        (
            "Un traceback es irrelevante después de reproducir el fallo.",
            "A traceback is irrelevant after reproducing the failure.",
            "Et traceback er irrelevant efter reproduktion af fejlen.",
        ),
        False,
        (
            "Contiene la ruta de llamadas y el punto de excepción.",
            "It contains the call path and exception point.",
            "Det indeholder kaldestien og exception-punktet.",
        ),
    ),
    (
        "023",
        (
            "Depurar implica comprobar hipótesis.",
            "Debugging involves testing hypotheses.",
            "Fejlsøgning indebærer kontrol af hypoteser.",
        ),
        True,
        (
            "Los cambios deben responder a evidencia.",
            "Changes should respond to evidence.",
            "Ændringer bør reagere på evidens.",
        ),
    ),
    (
        "024",
        (
            "Una prueba flaky debe ignorarse permanentemente.",
            "A flaky test should be ignored permanently.",
            "En flaky test bør ignoreres permanent.",
        ),
        False,
        (
            "Debe diagnosticarse su fuente de no determinismo.",
            "Its source of nondeterminism should be diagnosed.",
            "Kilden til ikke-determinisme bør diagnosticeres.",
        ),
    ),
    (
        "025",
        (
            "Una biblioteca debe configurar siempre el logging raíz.",
            "A library should always configure root logging.",
            "Et bibliotek bør altid konfigurere root-logging.",
        ),
        False,
        (
            "La aplicación consumidora decide la configuración global.",
            "The consuming application decides global configuration.",
            "Den forbrugende applikation beslutter global konfiguration.",
        ),
    ),
    (
        "026",
        (
            "Los logs pueden exponer datos sensibles si ayudan a depurar.",
            "Logs may expose sensitive data if debugging benefits.",
            "Logs må eksponere følsomme data hvis det hjælper fejlsøgning.",
        ),
        False,
        (
            "La observabilidad debe minimizar y proteger datos.",
            "Observability should minimize and protect data.",
            "Observerbarhed bør minimere og beskytte data.",
        ),
    ),
    (
        "027",
        (
            "Separar E/S de cálculo mejora testabilidad.",
            "Separating I/O from computation improves testability.",
            "Adskillelse af I/O fra beregning forbedrer testbarhed.",
        ),
        True,
        (
            "El cálculo puro se prueba con entradas controladas.",
            "Pure computation is tested with controlled inputs.",
            "Ren beregning testes med kontrollerede input.",
        ),
    ),
    (
        "028",
        (
            "Las propiedades sustituyen todos los ejemplos concretos.",
            "Properties replace all concrete examples.",
            "Egenskaber erstatter alle konkrete eksempler.",
        ),
        False,
        (
            "Complementan ejemplos y regresiones.",
            "They complement examples and regressions.",
            "De supplerer eksempler og regressioner.",
        ),
    ),
    (
        "029",
        (
            "Una propiedad debe ser independiente de la implementación.",
            "A property should be independent of implementation.",
            "En egenskab bør være uafhængig af implementeringen.",
        ),
        True,
        (
            "Así puede detectar implementaciones plausibles pero incorrectas.",
            "That allows it to detect plausible but wrong implementations.",
            "Så kan den opdage plausible men forkerte implementeringer.",
        ),
    ),
    (
        "030",
        (
            "Cobertura alta garantiza aserciones significativas.",
            "High coverage guarantees meaningful assertions.",
            "Høj coverage garanterer meningsfulde assertions.",
        ),
        False,
        (
            "Las líneas pueden ejecutarse sin verificar resultados útiles.",
            "Lines may execute without useful result checks.",
            "Linjer kan udføres uden nyttige resultatkontroller.",
        ),
    ),
)

LOCALIZED_OBJECTIVE_QUESTION_BANK_14 = tuple(
    objective_mcq(
        f"dm857.m14.bank.{item_id}",
        prompt,
        options,
        correct_option_id,
        explanation,
    )
    for item_id, prompt, options, correct_option_id, explanation in _BANK_MCQS
) + tuple(
    objective_tf(
        f"dm857.m14.bank.{item_id}",
        prompt,
        correct=correct,
        explanation=explanation,
    )
    for item_id, prompt, correct, explanation in _BANK_TFS
)


def materialize_module_14_question_bank(
    locale: AppLocale | str = AppLocale.SPANISH_SPAIN,
) -> tuple[AssessmentItem, ...]:
    """Materialize the module 14 objective bank in one supported locale."""
    resolved = locale if isinstance(locale, AppLocale) else AppLocale.resolve(locale)
    return tuple(item.materialize(resolved) for item in LOCALIZED_OBJECTIVE_QUESTION_BANK_14)


MODULE_14_TESTING_DEBUGGING_QUALITY: LearningModule = (
    LOCALIZED_MODULE_14_TESTING_DEBUGGING_QUALITY.materialize(AppLocale.SPANISH_SPAIN)
)
OBJECTIVE_QUESTION_BANK_14 = materialize_module_14_question_bank()

__all__ = [
    "LOCALIZED_MODULE_14_TESTING_DEBUGGING_QUALITY",
    "LOCALIZED_OBJECTIVE_QUESTION_BANK_14",
    "MODULE_14_TESTING_DEBUGGING_QUALITY",
    "OBJECTIVE_QUESTION_BANK_14",
    "materialize_module_14_question_bank",
]
