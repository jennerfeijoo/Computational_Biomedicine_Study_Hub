"""Project-grounded technical reasoning stations for the DM857 capstone."""

from __future__ import annotations

from ...learning.technical_stations import TechnicalStation, TechnicalStationKind
from ._shared import criterion, localized

PROJECT_ID = "dm857.capstone.project-defence"

_EVIDENCE_PACKET = """Use evidence from the real group project. In the response editor, include:

<ARTIFACT>
Paste the exact code, diff, failing test, traceback, command output, table, or result required by the station. Keep enough surrounding context to make the artifact interpretable.
</ARTIFACT>

<ANALYSIS>
Write your own technical explanation. Distinguish observed behaviour from inference, identify assumptions, and connect the explanation to the project decision being defended.
</ANALYSIS>

Do not paste secrets, credentials, personal data, or unpublished sensitive biomedical data."""

DM857_PROJECT_STATIONS = (
    TechnicalStation(
        station_id="dm857.capstone.station.function-contract",
        course_code="DM857",
        lab_id=PROJECT_ID,
        kind=TechnicalStationKind.CODE_READING,
        title=localized(
            "Defender el contrato de una función real",
            "Defend the contract of a real function",
            "Forsvar kontrakten for en reel funktion",
        ),
        artifact_title=localized(
            "Paquete de evidencia del proyecto",
            "Project evidence packet",
            "Projektets evidenspakke",
        ),
        artifact=_EVIDENCE_PACKET,
        prompt=localized(
            "Pega una función, método o clase del proyecto y una llamada representativa. Explica "
            "entradas, salida, invariantes, efectos secundarios, errores esperados y qué parte de "
            "ese contrato está comprobada por tests.",
            "Paste one project function, method, or class and a representative call. Explain its "
            "inputs, output, invariants, side effects, expected failures, and which parts of the "
            "contract are verified by tests.",
            "Indsæt en funktion, metode eller klasse fra projektet samt et repræsentativt kald. "
            "Forklar input, output, invarianter, sideeffekter, forventede fejl og hvilke dele af "
            "kontrakten der verificeres af tests.",
        ),
        criteria=(
            criterion(
                "artifact",
                "Incluye código real y contexto suficiente para identificar su uso.",
                "Include real code and enough context to identify how it is used.",
                "Medtag reel kode og tilstrækkelig kontekst til at identificere anvendelsen.",
            ),
            criterion(
                "contract",
                "Define tipos, precondiciones, postcondiciones y efectos secundarios.",
                "Define types, preconditions, postconditions, and side effects.",
                "Definér typer, forudsætninger, efterbetingelser og sideeffekter.",
            ),
            criterion(
                "failure",
                "Distingue entrada inválida, error de ejecución y resultado válido pero inesperado.",
                "Distinguish invalid input, execution failure, and a valid but unexpected result.",
                "Skeln mellem ugyldigt input, kørselsfejl og et gyldigt men uventet resultat.",
            ),
            criterion(
                "tests",
                "Relaciona afirmaciones concretas con tests existentes o identifica la ausencia.",
                "Tie concrete claims to existing tests or identify the missing coverage.",
                "Knyt konkrete påstande til eksisterende tests eller identificér manglende dækning.",
            ),
        ),
        estimated_minutes=18,
        source_basis=(PROJECT_ID, "dm857.capstone.m02", "dm857.capstone.m03"),
        minimum_response_chars=220,
    ),
    TechnicalStation(
        station_id="dm857.capstone.station.execution-trace",
        course_code="DM857",
        lab_id=PROJECT_ID,
        kind=TechnicalStationKind.EXECUTION_TRACE,
        title=localized(
            "Trazar una ejecución del proyecto",
            "Trace a project execution",
            "Spor en projektkørsel",
        ),
        artifact_title=localized(
            "Código, entrada y salida observada",
            "Code, input, and observed output",
            "Kode, input og observeret output",
        ),
        artifact=_EVIDENCE_PACKET,
        prompt=localized(
            "Pega el fragmento ejecutado, una entrada concreta y la salida real. Reconstruye los "
            "cambios de estado y decisiones de control hasta explicar exactamente cómo se obtiene "
            "la salida, incluyendo una rama o caso límite relevante.",
            "Paste the executed fragment, one concrete input, and the real output. Reconstruct "
            "state changes and control decisions until you can explain exactly how the output is "
            "produced, including one relevant branch or boundary case.",
            "Indsæt det kørte fragment, et konkret input og det reelle output. Rekonstruér "
            "tilstandsændringer og kontrolbeslutninger, indtil du præcist kan forklare outputtet, "
            "inklusive en relevant gren eller grænsetilfælde.",
        ),
        criteria=(
            criterion(
                "evidence",
                "Incluye código, entrada y salida reales, no un ejemplo inventado sin referencia.",
                "Include real code, input, and output rather than an unsupported invented example.",
                "Medtag reel kode, input og output frem for et udokumenteret opdigtet eksempel.",
            ),
            criterion(
                "state",
                "Explica las variables o estructuras que cambian y en qué orden.",
                "Explain which variables or structures change and in what order.",
                "Forklar hvilke variabler eller strukturer der ændres og i hvilken rækkefølge.",
            ),
            criterion(
                "control",
                "Justifica cada rama, iteración o llamada relevante.",
                "Justify every relevant branch, iteration, or call.",
                "Begrund hver relevant gren, iteration eller kald.",
            ),
            criterion(
                "boundary",
                "Contrasta la traza con al menos un caso límite o ruta alternativa.",
                "Contrast the trace with at least one boundary case or alternative path.",
                "Sammenlign sporet med mindst ét grænsetilfælde eller en alternativ sti.",
            ),
        ),
        estimated_minutes=18,
        source_basis=(PROJECT_ID, "dm857.capstone.m03"),
        minimum_response_chars=220,
    ),
    TechnicalStation(
        station_id="dm857.capstone.station.debug-failure",
        course_code="DM857",
        lab_id=PROJECT_ID,
        kind=TechnicalStationKind.DEBUGGING,
        title=localized(
            "Diagnosticar un fallo reproducible",
            "Diagnose a reproducible failure",
            "Diagnosticér en reproducerbar fejl",
        ),
        artifact_title=localized(
            "Implementación, test y fallo",
            "Implementation, test, and failure",
            "Implementering, test og fejl",
        ),
        artifact=_EVIDENCE_PACKET,
        prompt=localized(
            "Pega la implementación relevante, el test o comando que falla y el traceback o salida. "
            "Formula una hipótesis causal, localiza la primera desviación observable, propone el "
            "cambio mínimo y especifica el test de regresión que impediría la reaparición.",
            "Paste the relevant implementation, failing test or command, and traceback or output. "
            "Form a causal hypothesis, locate the first observable divergence, propose the minimal "
            "change, and specify the regression test that would prevent recurrence.",
            "Indsæt den relevante implementering, den fejlede test eller kommando samt traceback "
            "eller output. Formulér en kausal hypotese, find den første observerbare afvigelse, "
            "foreslå den mindste ændring og specificér regressionstesten.",
        ),
        criteria=(
            criterion(
                "reproduction",
                "Documenta una reproducción concreta y la salida exacta.",
                "Document one concrete reproduction and the exact output.",
                "Dokumentér én konkret reproduktion og det præcise output.",
            ),
            criterion(
                "cause",
                "Separa síntoma, primera desviación y causa propuesta.",
                "Separate the symptom, first divergence, and proposed cause.",
                "Adskil symptom, første afvigelse og foreslået årsag.",
            ),
            criterion(
                "minimal-fix",
                "Propone un cambio mínimo y explica por qué no altera otros contratos.",
                "Propose a minimal change and explain why it preserves other contracts.",
                "Foreslå en minimal ændring og forklar hvorfor andre kontrakter bevares.",
            ),
            criterion(
                "regression",
                "Define un test que falle antes y pase después del cambio.",
                "Define a test that fails before and passes after the change.",
                "Definér en test der fejler før og består efter ændringen.",
            ),
        ),
        estimated_minutes=20,
        source_basis=(PROJECT_ID, "dm857.capstone.m03", "dm857.capstone.m04"),
        minimum_response_chars=240,
    ),
    TechnicalStation(
        station_id="dm857.capstone.station.test-adequacy",
        course_code="DM857",
        lab_id=PROJECT_ID,
        kind=TechnicalStationKind.PROJECT_REASONING,
        title=localized(
            "Evaluar la suficiencia de los tests",
            "Evaluate test adequacy",
            "Vurdér testenes tilstrækkelighed",
        ),
        artifact_title=localized(
            "Código y suite de tests",
            "Code and test suite",
            "Kode og testsuite",
        ),
        artifact=_EVIDENCE_PACKET,
        prompt=localized(
            "Pega una unidad de código y los tests actuales que la cubren. Construye una matriz de "
            "comportamientos normales, vacíos, límites, tipos inválidos y fallos esperados. Indica "
            "qué riesgos permanecen aunque todos los tests actuales pasen.",
            "Paste one code unit and its current tests. Build a matrix covering normal, empty, "
            "boundary, invalid-type, and expected-failure behaviours. State which risks remain even "
            "when all current tests pass.",
            "Indsæt en kodeenhed og dens nuværende tests. Byg en matrix over normal, tom, grænse-, "
            "ugyldig type- og forventet fejladfærd. Angiv hvilke risici der består selv når alle "
            "nuværende tests består.",
        ),
        criteria=(
            criterion(
                "mapping",
                "Relaciona cada test con un comportamiento o contrato específico.",
                "Map each test to a specific behaviour or contract.",
                "Knyt hver test til en specifik adfærd eller kontrakt.",
            ),
            criterion(
                "boundaries",
                "Incluye casos normales, vacíos, de frontera y entradas inválidas.",
                "Include normal, empty, boundary, and invalid-input cases.",
                "Medtag normale, tomme, grænse- og ugyldige inputtilfælde.",
            ),
            criterion(
                "oracle",
                "Explica por qué el resultado esperado es correcto y no solo conveniente.",
                "Explain why the expected result is correct rather than merely convenient.",
                "Forklar hvorfor det forventede resultat er korrekt og ikke blot praktisk.",
            ),
            criterion(
                "residual-risk",
                "Identifica riesgos no cubiertos por tests unitarios o deterministas.",
                "Identify risks not covered by unit or deterministic tests.",
                "Identificér risici der ikke dækkes af enheds- eller deterministiske tests.",
            ),
        ),
        estimated_minutes=20,
        source_basis=(PROJECT_ID, "dm857.capstone.m04"),
        minimum_response_chars=240,
    ),
    TechnicalStation(
        station_id="dm857.capstone.station.design-choice",
        course_code="DM857",
        lab_id=PROJECT_ID,
        kind=TechnicalStationKind.METHOD_SELECTION,
        title=localized(
            "Justificar una decisión de diseño",
            "Justify a design decision",
            "Begrund en designbeslutning",
        ),
        artifact_title=localized(
            "Código o diff de la decisión",
            "Code or diff for the decision",
            "Kode eller diff for beslutningen",
        ),
        artifact=_EVIDENCE_PACKET,
        prompt=localized(
            "Pega el código o diff donde se materializa una decisión de estructura de datos, API, "
            "algoritmo o descomposición. Compara al menos una alternativa y defiende la elección "
            "mediante corrección, mantenibilidad, coste y restricciones del proyecto.",
            "Paste the code or diff that implements a data-structure, API, algorithm, or "
            "decomposition decision. Compare at least one alternative and defend the choice using "
            "correctness, maintainability, cost, and project constraints.",
            "Indsæt koden eller diffen der realiserer en beslutning om datastruktur, API, algoritme "
            "eller dekomponering. Sammenlign mindst ét alternativ og forsvar valget ud fra korrekthed, "
            "vedligeholdelse, omkostning og projektkrav.",
        ),
        criteria=(
            criterion(
                "decision",
                "Identifica exactamente dónde y cómo se implementa la decisión.",
                "Identify exactly where and how the decision is implemented.",
                "Identificér præcist hvor og hvordan beslutningen implementeres.",
            ),
            criterion(
                "alternative",
                "Compara una alternativa plausible bajo los mismos requisitos.",
                "Compare one plausible alternative under the same requirements.",
                "Sammenlign ét plausibelt alternativ under de samme krav.",
            ),
            criterion(
                "tradeoff",
                "Expone ventajas, costes y condiciones en las que la decisión dejaría de ser adecuada.",
                "State benefits, costs, and conditions under which the choice would stop being suitable.",
                "Angiv fordele, omkostninger og betingelser hvor valget ikke længere er passende.",
            ),
            criterion(
                "evidence",
                "Apoya la defensa con tests, medidas, complejidad o evidencia del repositorio.",
                "Support the defence with tests, measurements, complexity, or repository evidence.",
                "Understøt forsvaret med tests, målinger, kompleksitet eller repository-evidens.",
            ),
        ),
        estimated_minutes=20,
        source_basis=(PROJECT_ID, "dm857.capstone.m02", "dm857.capstone.m03"),
        minimum_response_chars=240,
    ),
    TechnicalStation(
        station_id="dm857.capstone.station.performance",
        course_code="DM857",
        lab_id=PROJECT_ID,
        kind=TechnicalStationKind.COMPLEXITY_ANALYSIS,
        title=localized(
            "Analizar coste y escalabilidad",
            "Analyse cost and scalability",
            "Analysér omkostning og skalerbarhed",
        ),
        artifact_title=localized(
            "Bucle, algoritmo o medición",
            "Loop, algorithm, or measurement",
            "Løkke, algoritme eller måling",
        ),
        artifact=_EVIDENCE_PACKET,
        prompt=localized(
            "Pega una ruta de ejecución relevante y, cuando exista, una medición reproducible. "
            "Deriva el coste temporal y espacial en función del tamaño de entrada, identifica el "
            "cuello de botella y separa complejidad asintótica de rendimiento observado.",
            "Paste one relevant execution path and, when available, a reproducible measurement. "
            "Derive time and space cost as functions of input size, identify the bottleneck, and "
            "separate asymptotic complexity from observed performance.",
            "Indsæt en relevant kørselssti og, når muligt, en reproducerbar måling. Udled tids- og "
            "pladsomkostning som funktion af inputstørrelse, identificér flaskehalsen og adskil "
            "asymptotisk kompleksitet fra observeret ydelse.",
        ),
        criteria=(
            criterion(
                "parameter",
                "Define con claridad qué representa el tamaño de entrada.",
                "Clearly define what the input-size parameter represents.",
                "Definér klart hvad inputstørrelsesparameteren repræsenterer.",
            ),
            criterion(
                "derivation",
                "Deriva el coste a partir de operaciones y estructuras concretas.",
                "Derive cost from concrete operations and structures.",
                "Udled omkostningen fra konkrete operationer og strukturer.",
            ),
            criterion(
                "measurement",
                "Distingue medición, variabilidad experimental y complejidad teórica.",
                "Distinguish measurement, experimental variability, and theoretical complexity.",
                "Skeln mellem måling, eksperimentel variation og teoretisk kompleksitet.",
            ),
            criterion(
                "decision",
                "Conecta el análisis con una decisión de optimización o con la decisión de no optimizar.",
                "Connect the analysis to an optimisation decision or a justified decision not to optimise.",
                "Knyt analysen til en optimeringsbeslutning eller en begrundet beslutning om ikke at optimere.",
            ),
        ),
        estimated_minutes=20,
        source_basis=(PROJECT_ID, "dm857.capstone.m03", "dm857.capstone.m04"),
        minimum_response_chars=240,
    ),
    TechnicalStation(
        station_id="dm857.capstone.station.scientific-output",
        course_code="DM857",
        lab_id=PROJECT_ID,
        kind=TechnicalStationKind.SCIENTIFIC_INTERPRETATION,
        title=localized(
            "Interpretar una salida biomédica sin sobreafirmar",
            "Interpret biomedical output without overclaiming",
            "Fortolk biomedicinsk output uden at overfortolke",
        ),
        artifact_title=localized(
            "Código de análisis y resultado",
            "Analysis code and result",
            "Analysekode og resultat",
        ),
        artifact=_EVIDENCE_PACKET,
        prompt=localized(
            "Pega el código que produce una tabla, métrica o figura y el resultado observado. "
            "Separa qué demuestra computacionalmente, qué interpretación biomédica es razonable, "
            "qué supuestos la sostienen y qué no puede concluirse con los datos disponibles.",
            "Paste the code producing a table, metric, or figure and the observed result. Separate "
            "what is computationally established, what biomedical interpretation is reasonable, "
            "which assumptions support it, and what cannot be concluded from the available data.",
            "Indsæt koden der producerer en tabel, måling eller figur samt det observerede resultat. "
            "Adskil hvad der beregningsmæssigt fastslås, hvilken biomedicinsk fortolkning der er rimelig, "
            "hvilke antagelser den bygger på, og hvad data ikke tillader at konkludere.",
        ),
        criteria=(
            criterion(
                "pipeline",
                "Relaciona el resultado con transformaciones y parámetros concretos del código.",
                "Relate the result to concrete transformations and parameters in the code.",
                "Knyt resultatet til konkrete transformationer og parametre i koden.",
            ),
            criterion(
                "established",
                "Distingue observación calculada de explicación causal o clínica.",
                "Distinguish a computed observation from a causal or clinical explanation.",
                "Skeln mellem en beregnet observation og en kausal eller klinisk forklaring.",
            ),
            criterion(
                "assumptions",
                "Explicita calidad de datos, selección, unidades y supuestos analíticos relevantes.",
                "State relevant data-quality, selection, unit, and analytical assumptions.",
                "Angiv relevante antagelser om datakvalitet, udvælgelse, enheder og analyse.",
            ),
            criterion(
                "limits",
                "Formula al menos una limitación y una comprobación adicional necesaria.",
                "Formulate at least one limitation and one required additional check.",
                "Formulér mindst én begrænsning og én nødvendig yderligere kontrol.",
            ),
        ),
        estimated_minutes=22,
        source_basis=(PROJECT_ID, "dm857.capstone.m04", "dm857.capstone.m05"),
        minimum_response_chars=260,
    ),
    TechnicalStation(
        station_id="dm857.capstone.station.contribution-defence",
        course_code="DM857",
        lab_id=PROJECT_ID,
        kind=TechnicalStationKind.PROJECT_REASONING,
        title=localized(
            "Defender una contribución individual",
            "Defend an individual contribution",
            "Forsvar et individuelt bidrag",
        ),
        artifact_title=localized(
            "Commit, diff y evidencia asociada",
            "Commit, diff, and associated evidence",
            "Commit, diff og tilknyttet evidens",
        ),
        artifact=_EVIDENCE_PACKET,
        prompt=localized(
            "Pega un commit o diff propio y la evidencia que demuestra su efecto. Explica el problema "
            "previo, tu razonamiento, los cambios realizados, cómo verificaste la integración y qué "
            "limitaciones o deuda técnica permanecen. No atribuyas trabajo de otras personas.",
            "Paste one of your own commits or diffs and evidence demonstrating its effect. Explain "
            "the prior problem, your reasoning, the changes made, how integration was verified, and "
            "which limitations or technical debt remain. Do not claim other people's work.",
            "Indsæt et af dine egne commits eller diffs samt evidens for effekten. Forklar det tidligere "
            "problem, din ræsonnering, ændringerne, hvordan integrationen blev verificeret, og hvilke "
            "begrænsninger eller teknisk gæld der består. Tilskriv ikke andres arbejde til dig selv.",
        ),
        criteria=(
            criterion(
                "ownership",
                "Delimita con precisión tu contribución y las dependencias del trabajo grupal.",
                "Precisely delimit your contribution and its dependencies on group work.",
                "Afgræns præcist dit bidrag og dets afhængigheder af gruppearbejdet.",
            ),
            criterion(
                "reasoning",
                "Explica el problema y la cadena de decisiones que condujo al cambio.",
                "Explain the problem and the chain of decisions leading to the change.",
                "Forklar problemet og beslutningskæden der førte til ændringen.",
            ),
            criterion(
                "verification",
                "Incluye tests, revisión, ejecución o evidencia de integración.",
                "Include tests, review, execution, or integration evidence.",
                "Medtag tests, review, kørsel eller integrationsevidens.",
            ),
            criterion(
                "limits",
                "Reconoce limitaciones, riesgos pendientes o deuda técnica.",
                "Acknowledge limitations, outstanding risks, or technical debt.",
                "Anerkend begrænsninger, udestående risici eller teknisk gæld.",
            ),
        ),
        estimated_minutes=22,
        source_basis=(PROJECT_ID, "dm857.capstone.m03", "dm857.capstone.m05"),
        minimum_response_chars=260,
    ),
)

__all__ = ["DM857_PROJECT_STATIONS", "PROJECT_ID"]
