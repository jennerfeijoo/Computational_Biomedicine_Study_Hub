"""Artifact-based DM847 technical reasoning stations for the four current labs."""

from __future__ import annotations

from ...i18n.locales import AppLocale
from ...learning.computational_labs import LocalizedText
from ...learning.technical_stations import (
    TechnicalStation,
    TechnicalStationCriterion,
    TechnicalStationKind,
)


def _lt(es: str, en: str, da: str) -> LocalizedText:
    return LocalizedText(
        {
            AppLocale.SPANISH_SPAIN: es,
            AppLocale.ENGLISH: en,
            AppLocale.DANISH_DENMARK: da,
        }
    )


def _criterion(
    identity: str,
    es: str,
    en: str,
    da: str,
) -> TechnicalStationCriterion:
    return TechnicalStationCriterion(identity, _lt(es, en, da))


DM847_TECHNICAL_STATIONS = (
    TechnicalStation(
        station_id="dm847.lab01.station.code-contract",
        course_code="DM847",
        lab_id="dm847.lab01.sequence-mapping",
        kind=TechnicalStationKind.CODE_READING,
        title=_lt(
            "Leer el contrato de una búsqueda aproximada",
            "Read an approximate-search contract",
            "Læs kontrakten for en tilnærmet søgning",
        ),
        artifact_title=_lt("Código", "Code", "Kode"),
        artifact="""def candidate_positions(reference: str, read: str, max_mismatches: int) -> list[int]:
    positions = []
    for start in range(len(reference) - len(read) + 1):
        window = reference[start : start + len(read)]
        mismatches = sum(a != b for a, b in zip(window, read, strict=True))
        if mismatches <= max_mismatches:
            positions.append(start)
    return positions""",
        prompt=_lt(
            "Explica el contrato de entrada y salida, por qué el límite del range incluye +1, qué supone zip(strict=True) y qué casos debe rechazar una implementación robusta.",
            "Explain the input/output contract, why the range bound includes +1, what zip(strict=True) assumes, and which cases a robust implementation should reject.",
            "Forklar input/output-kontrakten, hvorfor range-grænsen indeholder +1, hvad zip(strict=True) antager, og hvilke tilfælde en robust implementering bør afvise.",
        ),
        criteria=(
            _criterion(
                "contract",
                "Define tipos, coordenadas y significado de max_mismatches.",
                "Define types, coordinates, and the meaning of max_mismatches.",
                "Definér typer, koordinater og betydningen af max_mismatches.",
            ),
            _criterion(
                "boundary",
                "Explica el último inicio válido y el caso read más largo que reference.",
                "Explain the last valid start and the read-longer-than-reference case.",
                "Forklar den sidste gyldige start og tilfældet hvor read er længere end reference.",
            ),
            _criterion(
                "validation",
                "Identifica entradas inválidas y al menos una decisión de validación.",
                "Identify invalid inputs and at least one validation decision.",
                "Identificér ugyldige input og mindst én valideringsbeslutning.",
            ),
        ),
        estimated_minutes=12,
        source_basis=("dm847.lab01.sequence-mapping", "DM847 sequence matching outcomes"),
    ),
    TechnicalStation(
        station_id="dm847.lab01.station.trace-overlap",
        course_code="DM847",
        lab_id="dm847.lab01.sequence-mapping",
        kind=TechnicalStationKind.EXECUTION_TRACE,
        title=_lt(
            "Trazar coincidencias solapadas",
            "Trace overlapping matches",
            "Spor overlappende matches",
        ),
        artifact_title=_lt("Entrada", "Input", "Input"),
        artifact="""reference = "AAAAA"
read = "AAA"
max_mismatches = 0""",
        prompt=_lt(
            "Traza cada ventana examinada, calcula mismatches y determina la lista final. Después explica por qué eliminar solapamientos cambiaría el contrato del algoritmo.",
            "Trace every examined window, calculate mismatches, and determine the final list. Then explain why removing overlaps would change the algorithm contract.",
            "Spor hvert undersøgt vindue, beregn mismatches og bestem den endelige liste. Forklar derefter hvorfor fjernelse af overlap ville ændre algoritmens kontrakt.",
        ),
        criteria=(
            _criterion(
                "windows",
                "Enumera las tres ventanas y sus coordenadas de inicio.",
                "Enumerate the three windows and their start coordinates.",
                "Angiv de tre vinduer og deres startkoordinater.",
            ),
            _criterion(
                "result",
                "Obtiene [0, 1, 2] con mismatches cero.",
                "Obtain [0, 1, 2] with zero mismatches.",
                "Opnå [0, 1, 2] med nul mismatches.",
            ),
            _criterion(
                "semantics",
                "Distingue coincidencia solapada de duplicación accidental.",
                "Distinguish an overlapping match from accidental duplication.",
                "Skeln mellem et overlappende match og utilsigtet duplikering.",
            ),
        ),
        estimated_minutes=10,
        source_basis=("dm847.lab01.sequence-mapping", "DM847 exact matching practice"),
    ),
    TechnicalStation(
        station_id="dm847.lab01.station.debug-off-by-one",
        course_code="DM847",
        lab_id="dm847.lab01.sequence-mapping",
        kind=TechnicalStationKind.DEBUGGING,
        title=_lt(
            "Depurar una pérdida de la última posición",
            "Debug a missing final position",
            "Fejlfind en manglende sidste position",
        ),
        artifact_title=_lt("Código defectuoso", "Defective code", "Defekt kode"),
        artifact="""def exact_positions(reference: str, read: str) -> list[int]:
    hits = []
    for start in range(len(reference) - len(read)):
        if reference[start : start + len(read)] == read:
            hits.append(start)
    return hits

print(exact_positions("ACGT", "GT"))  # received []""",
        prompt=_lt(
            "Localiza el defecto, construye la tabla de valores de start realmente visitados, corrige la expresión y formula una prueba de regresión mínima.",
            "Locate the defect, build the table of start values actually visited, correct the expression, and formulate a minimal regression test.",
            "Find fejlen, opbyg tabellen over de start-værdier der faktisk besøges, ret udtrykket og formulér en minimal regressionstest.",
        ),
        criteria=(
            _criterion(
                "cause",
                "Explica por qué range excluye el límite superior.",
                "Explain why range excludes its upper bound.",
                "Forklar hvorfor range udelukker sin øvre grænse.",
            ),
            _criterion(
                "fix",
                "Corrige a len(reference) - len(read) + 1.",
                "Correct to len(reference) - len(read) + 1.",
                "Ret til len(reference) - len(read) + 1.",
            ),
            _criterion(
                "regression",
                "Incluye un test donde la única coincidencia termina al final de reference.",
                "Include a test where the only match ends at the end of reference.",
                "Medtag en test hvor det eneste match slutter ved reference-strengens slutning.",
            ),
        ),
        estimated_minutes=10,
        source_basis=("dm847.lab01.sequence-mapping", "DM847 debugging practice"),
    ),
    TechnicalStation(
        station_id="dm847.lab01.station.interpret-multimapping",
        course_code="DM847",
        lab_id="dm847.lab01.sequence-mapping",
        kind=TechnicalStationKind.SCIENTIFIC_INTERPRETATION,
        title=_lt(
            "Interpretar una lectura multimapeada",
            "Interpret a multimapped read",
            "Fortolk en multimappet read",
        ),
        artifact_title=_lt("Resultado", "Result", "Resultat"),
        artifact="""read_id: r17
read: CG
candidate_positions: [1, 4, 7]
classification: multimapping
reference: ACGTCGACG""",
        prompt=_lt(
            "Separa con precisión lo que demuestra el resultado, lo que podría sugerir y lo que no permite concluir sobre el origen biológico de la lectura.",
            "Separate precisely what the result establishes, what it may suggest, and what it does not permit you to conclude about the biological origin of the read.",
            "Adskil præcist hvad resultatet fastslår, hvad det kan antyde, og hvad det ikke gør det muligt at konkludere om readens biologiske oprindelse.",
        ),
        criteria=(
            _criterion(
                "establishes",
                "Afirma únicamente tres coincidencias exactas bajo este modelo y referencia.",
                "State only three exact matches under this model and reference.",
                "Angiv kun tre eksakte matches under denne model og reference.",
            ),
            _criterion(
                "uncertainty",
                "Explica que no se identifica cuál posición originó la lectura.",
                "Explain that the originating position is not identified.",
                "Forklar at den oprindelige position ikke identificeres.",
            ),
            _criterion(
                "limits",
                "Menciona referencia, hebra, errores, indels o calidad como límites relevantes.",
                "Mention reference, strand, errors, indels, or quality as relevant limits.",
                "Nævn reference, streng, fejl, indels eller kvalitet som relevante begrænsninger.",
            ),
        ),
        estimated_minutes=12,
        source_basis=("dm847.lab01.sequence-mapping", "DM847 biomedical interpretation boundary"),
    ),
    TechnicalStation(
        station_id="dm847.lab02.station.read-recurrence",
        course_code="DM847",
        lab_id="dm847.lab02.pairwise-alignment",
        kind=TechnicalStationKind.CODE_READING,
        title=_lt(
            "Leer la recurrencia global",
            "Read the global recurrence",
            "Læs den globale rekurrens",
        ),
        artifact_title=_lt("Código", "Code", "Kode"),
        artifact="""diagonal = score[i - 1][j - 1] + substitution(a[i - 1], b[j - 1])
up = score[i - 1][j] + gap
left = score[i][j - 1] + gap
score[i][j] = max(diagonal, up, left)""",
        prompt=_lt(
            "Explica qué representa score[i][j], qué subproblema corresponde a cada transición y por qué la inicialización de fila y columna determina que el alineamiento sea global.",
            "Explain what score[i][j] represents, which subproblem each transition corresponds to, and why row and column initialization makes the alignment global.",
            "Forklar hvad score[i][j] repræsenterer, hvilket delproblem hver overgang svarer til, og hvorfor initialisering af række og kolonne gør aligneringen global.",
        ),
        criteria=(
            _criterion(
                "state",
                "Define score[i][j] sobre prefijos de longitudes i y j.",
                "Define score[i][j] over prefixes of lengths i and j.",
                "Definér score[i][j] over præfikser med længder i og j.",
            ),
            _criterion(
                "transitions",
                "Relaciona diagonal, up y left con sustitución y gaps.",
                "Relate diagonal, up, and left to substitution and gaps.",
                "Knyt diagonal, up og left til substitution og gaps.",
            ),
            _criterion(
                "global",
                "Explica la penalización acumulada de prefijos contra vacío.",
                "Explain accumulated penalties for prefixes aligned to empty.",
                "Forklar akkumulerede straffe for præfikser alignet mod tom sekvens.",
            ),
        ),
        estimated_minutes=12,
        source_basis=("dm847.lab02.pairwise-alignment", "DM847 dynamic programming outcomes"),
    ),
    TechnicalStation(
        station_id="dm847.lab02.station.trace-cell",
        course_code="DM847",
        lab_id="dm847.lab02.pairwise-alignment",
        kind=TechnicalStationKind.EXECUTION_TRACE,
        title=_lt(
            "Calcular una celda de alineamiento",
            "Calculate one alignment cell",
            "Beregn én aligneringscelle",
        ),
        artifact_title=_lt("Estado parcial", "Partial state", "Delvis tilstand"),
        artifact="""a = "AG"
b = "AC"
match = 2
mismatch = -1
gap = -2

score[1][1] = 2
score[1][2] = 0
score[2][1] = 0

Compute score[2][2].""",
        prompt=_lt(
            "Calcula diagonal, up y left para score[2][2], selecciona el máximo y explica qué columnas alineadas representa cada opción.",
            "Calculate diagonal, up, and left for score[2][2], select the maximum, and explain which aligned columns each option represents.",
            "Beregn diagonal, up og left for score[2][2], vælg maksimum og forklar hvilke alignerede kolonner hver mulighed repræsenterer.",
        ),
        criteria=(
            _criterion(
                "values",
                "Obtiene diagonal=1, up=-2 y left=-2.",
                "Obtain diagonal=1, up=-2, and left=-2.",
                "Opnå diagonal=1, up=-2 og left=-2.",
            ),
            _criterion(
                "choice",
                "Selecciona score[2][2]=1 mediante mismatch G/C.",
                "Select score[2][2]=1 through the G/C mismatch.",
                "Vælg score[2][2]=1 via G/C-mismatch.",
            ),
            _criterion(
                "meaning",
                "Relaciona cada transición con consumo de caracteres en a y b.",
                "Relate each transition to character consumption in a and b.",
                "Knyt hver overgang til forbrug af tegn i a og b.",
            ),
        ),
        estimated_minutes=10,
        source_basis=("dm847.lab02.pairwise-alignment", "DM847 manual DP tracing"),
    ),
    TechnicalStation(
        station_id="dm847.lab02.station.debug-local-stop",
        course_code="DM847",
        lab_id="dm847.lab02.pairwise-alignment",
        kind=TechnicalStationKind.DEBUGGING,
        title=_lt(
            "Depurar un traceback local que invade regiones negativas",
            "Debug a local traceback entering negative regions",
            "Fejlfind et lokalt traceback der går ind i negative områder",
        ),
        artifact_title=_lt("Código defectuoso", "Defective code", "Defekt kode"),
        artifact="""while i > 0 and j > 0:
    direction = trace[i][j]
    if direction == "diag":
        aligned_a.append(a[i - 1])
        aligned_b.append(b[j - 1])
        i -= 1
        j -= 1
    elif direction == "up":
        aligned_a.append(a[i - 1])
        aligned_b.append("-")
        i -= 1
    else:
        aligned_a.append("-")
        aligned_b.append(b[j - 1])
        j -= 1""",
        prompt=_lt(
            "Explica qué condición de parada falta en Smith–Waterman, cómo el defecto altera las coordenadas locales y qué prueba mínima lo detecta.",
            "Explain which Smith–Waterman stopping condition is missing, how the defect changes local coordinates, and which minimal test detects it.",
            "Forklar hvilken stopbetingelse fra Smith–Waterman der mangler, hvordan fejlen ændrer lokale koordinater, og hvilken minimal test der opdager den.",
        ),
        criteria=(
            _criterion(
                "stop",
                "Añade parada cuando score[i][j] == 0.",
                "Add a stop when score[i][j] == 0.",
                "Tilføj stop når score[i][j] == 0.",
            ),
            _criterion(
                "coordinates",
                "Explica que continuar incorpora prefijos fuera de la región local óptima.",
                "Explain that continuing includes prefixes outside the optimal local region.",
                "Forklar at fortsættelse inkluderer præfikser uden for den optimale lokale region.",
            ),
            _criterion(
                "test",
                "Propone secuencias con una coincidencia interna y flancos no relacionados.",
                "Propose sequences with an internal match and unrelated flanks.",
                "Foreslå sekvenser med et internt match og ikke-relaterede flanker.",
            ),
        ),
        estimated_minutes=12,
        source_basis=("dm847.lab02.pairwise-alignment", "DM847 Smith-Waterman traceback"),
    ),
    TechnicalStation(
        station_id="dm847.lab02.station.select-global-local",
        course_code="DM847",
        lab_id="dm847.lab02.pairwise-alignment",
        kind=TechnicalStationKind.METHOD_SELECTION,
        title=_lt(
            "Elegir alineamiento global o local",
            "Choose global or local alignment",
            "Vælg global eller lokal alignment",
        ),
        artifact_title=_lt("Escenario", "Scenario", "Scenarie"),
        artifact="""Sequence A: a full-length 900 bp gene candidate
Sequence B: a 120 bp conserved domain-like segment from another sample
Goal: determine whether B occurs as a high-scoring region inside A.""",
        prompt=_lt(
            "Selecciona un método, justifica la elección, define qué resultado revisarías y explica dos razones por las que un score alto no demuestra homología ni función compartida.",
            "Select a method, justify the choice, define which result you would inspect, and explain two reasons why a high score does not establish homology or shared function.",
            "Vælg en metode, begrund valget, definér hvilket resultat du vil inspicere, og forklar to grunde til at en høj score ikke fastslår homologi eller delt funktion.",
        ),
        criteria=(
            _criterion(
                "method",
                "Selecciona alineamiento local por la relación segmento-dentro-de-secuencia.",
                "Select local alignment for the segment-within-sequence relation.",
                "Vælg lokal alignment for segment-i-sekvens-relationen.",
            ),
            _criterion(
                "output",
                "Menciona score, coordenadas, alineamiento y sensibilidad a parámetros.",
                "Mention score, coordinates, alignment, and parameter sensitivity.",
                "Nævn score, koordinater, alignment og parameterfølsomhed.",
            ),
            _criterion(
                "boundary",
                "Separa similitud computacional de historia evolutiva y función.",
                "Separate computational similarity from evolutionary history and function.",
                "Adskil beregningsmæssig lighed fra evolutionær historie og funktion.",
            ),
        ),
        estimated_minutes=12,
        source_basis=("dm847.lab02.pairwise-alignment", "DM847 method selection and interpretation"),
    ),
    TechnicalStation(
        station_id="dm847.lab03.station.read-occ",
        course_code="DM847",
        lab_id="dm847.lab03.sequence-index",
        kind=TechnicalStationKind.CODE_READING,
        title=_lt(
            "Leer la semántica de Occ",
            "Read Occ semantics",
            "Læs Occ-semantikken",
        ),
        artifact_title=_lt("Código", "Code", "Kode"),
        artifact="""def build_occ(bwt: str, alphabet: tuple[str, ...]) -> dict[str, list[int]]:
    occ = {symbol: [0] for symbol in alphabet}
    for char in bwt:
        for symbol in alphabet:
            occ[symbol].append(occ[symbol][-1] + int(char == symbol))
    return occ""",
        prompt=_lt(
            "Explica exactamente qué representa occ[c][k], por qué cada lista tiene len(bwt)+1 elementos y cómo esta convención evita errores en intervalos half-open.",
            "Explain exactly what occ[c][k] represents, why each list has len(bwt)+1 elements, and how this convention avoids errors in half-open intervals.",
            "Forklar præcist hvad occ[c][k] repræsenterer, hvorfor hver liste har len(bwt)+1 elementer, og hvordan denne konvention undgår fejl i halvåbne intervaller.",
        ),
        criteria=(
            _criterion(
                "meaning",
                "Define occ[c][k] como conteo en bwt[:k].",
                "Define occ[c][k] as the count in bwt[:k].",
                "Definér occ[c][k] som antallet i bwt[:k].",
            ),
            _criterion(
                "length",
                "Explica el prefijo vacío en k=0 y el prefijo completo en k=n.",
                "Explain the empty prefix at k=0 and complete prefix at k=n.",
                "Forklar det tomme præfiks ved k=0 og hele præfikset ved k=n.",
            ),
            _criterion(
                "interval",
                "Relaciona top/bottom con conteos sin ajustes -1 ad hoc.",
                "Relate top/bottom to counts without ad hoc -1 adjustments.",
                "Knyt top/bottom til tællinger uden ad hoc -1-justeringer.",
            ),
        ),
        estimated_minutes=12,
        source_basis=("dm847.lab03.sequence-index", "DM847 BWT occurrence tables"),
    ),
    TechnicalStation(
        station_id="dm847.lab03.station.trace-backward",
        course_code="DM847",
        lab_id="dm847.lab03.sequence-index",
        kind=TechnicalStationKind.EXECUTION_TRACE,
        title=_lt(
            "Trazar backward search",
            "Trace backward search",
            "Spor backward search",
        ),
        artifact_title=_lt("Índice", "Index", "Indeks"),
        artifact="""text = "GATTACA$"
BWT = "ACTGA$TA"
C = {"$": 0, "A": 1, "C": 4, "G": 5, "T": 6}
pattern = "TA"
Start interval: [0, 8)
Process pattern from right to left.""",
        prompt=_lt(
            "Actualiza el intervalo para A y luego para T. Explica qué conjunto de sufijos representa cada intervalo y cómo count se obtiene de su anchura.",
            "Update the interval for A and then T. Explain which suffix set each interval represents and how count is obtained from its width.",
            "Opdatér intervallet for A og derefter T. Forklar hvilket suffikssæt hvert interval repræsenterer, og hvordan count fås fra intervallets bredde.",
        ),
        criteria=(
            _criterion(
                "a-step",
                "Calcula correctamente el intervalo tras procesar A.",
                "Calculate the correct interval after processing A.",
                "Beregn det korrekte interval efter behandling af A.",
            ),
            _criterion(
                "t-step",
                "Calcula correctamente el intervalo final para TA.",
                "Calculate the correct final interval for TA.",
                "Beregn det korrekte slutinterval for TA.",
            ),
            _criterion(
                "semantics",
                "Interpreta filas del BWT y diferencia count de coordenadas de referencia.",
                "Interpret BWT rows and distinguish count from reference coordinates.",
                "Fortolk BWT-rækker og skeln count fra referencekoordinater.",
            ),
        ),
        estimated_minutes=15,
        source_basis=("dm847.lab03.sequence-index", "DM847 FM-index backward search"),
    ),
    TechnicalStation(
        station_id="dm847.lab03.station.debug-locate",
        course_code="DM847",
        lab_id="dm847.lab03.sequence-index",
        kind=TechnicalStationKind.DEBUGGING,
        title=_lt(
            "Depurar count confundido con locate",
            "Debug count confused with locate",
            "Fejlfind count forvekslet med locate",
        ),
        artifact_title=_lt("Código defectuoso", "Defective code", "Defekt kode"),
        artifact="""def locate(index: FMIndex, pattern: str) -> list[int]:
    top, bottom = backward_search(index, pattern)
    return list(range(top, bottom))

# Returned [2, 3] for a pattern whose reference positions are [1, 4].""",
        prompt=_lt(
            "Explica la confusión entre filas del suffix array y coordenadas de referencia, corrige la lógica y especifica un test que pueda pasar count pero fallar locate.",
            "Explain the confusion between suffix-array rows and reference coordinates, correct the logic, and specify a test that can pass count but fail locate.",
            "Forklar forvekslingen mellem suffix-array-rækker og referencekoordinater, ret logikken og angiv en test der kan bestå count men fejle locate.",
        ),
        criteria=(
            _criterion(
                "distinction",
                "Distingue índices de fila [top,bottom) de valores SA[row].",
                "Distinguish row indices [top,bottom) from SA[row] values.",
                "Skeln rækkeindekser [top,bottom) fra SA[row]-værdier.",
            ),
            _criterion(
                "fix",
                "Devuelve y ordena index.suffix_array[top:bottom].",
                "Return and sort index.suffix_array[top:bottom].",
                "Returnér og sortér index.suffix_array[top:bottom].",
            ),
            _criterion(
                "test",
                "Usa un patrón donde las filas no coincidan numéricamente con posiciones.",
                "Use a pattern where rows do not numerically equal positions.",
                "Brug et mønster hvor rækker ikke numerisk svarer til positioner.",
            ),
        ),
        estimated_minutes=12,
        source_basis=("dm847.lab03.sequence-index", "DM847 count versus locate distinction"),
    ),
    TechnicalStation(
        station_id="dm847.lab03.station.complexity-tradeoff",
        course_code="DM847",
        lab_id="dm847.lab03.sequence-index",
        kind=TechnicalStationKind.COMPLEXITY_ANALYSIS,
        title=_lt(
            "Defender el coste de un índice",
            "Defend the cost of an index",
            "Forsvar omkostningen ved et indeks",
        ),
        artifact_title=_lt("Escenario", "Scenario", "Scenarie"),
        artifact="""Reference length n = 3,000,000,000
Pattern length m = 100
Queries q = 50,000,000
Options:
A. exhaustive scan for every query
B. suffix array with binary search
C. FM-index with sampled suffix array""",
        prompt=_lt(
            "Compara preprocesamiento, tiempo por consulta, memoria y capacidad count/locate. Justifica una elección y menciona qué cambia cuando se permiten mismatches o indels.",
            "Compare preprocessing, per-query time, memory, and count/locate capability. Justify one choice and mention what changes when mismatches or indels are allowed.",
            "Sammenlign preprocessing, tid pr. forespørgsel, hukommelse og count/locate-kapacitet. Begrund ét valg og nævn hvad der ændres når mismatches eller indels tillades.",
        ),
        criteria=(
            _criterion(
                "variables",
                "Usa n, m y q y separa preprocesamiento de consultas.",
                "Use n, m, and q and separate preprocessing from queries.",
                "Brug n, m og q og adskil preprocessing fra forespørgsler.",
            ),
            _criterion(
                "tradeoff",
                "Explica memoria frente a velocidad y count frente a locate.",
                "Explain memory versus speed and count versus locate.",
                "Forklar hukommelse versus hastighed og count versus locate.",
            ),
            _criterion(
                "extension",
                "Reconoce que búsqueda aproximada y alineamiento requieren lógica adicional.",
                "Recognize that approximate search and alignment require additional logic.",
                "Anerkend at tilnærmet søgning og alignment kræver yderligere logik.",
            ),
        ),
        estimated_minutes=15,
        source_basis=("dm847.lab03.sequence-index", "DM847 complexity and index trade-offs"),
    ),
    TechnicalStation(
        station_id="dm847.lab04.station.read-logsumexp",
        course_code="DM847",
        lab_id="dm847.lab04.hidden-markov-model",
        kind=TechnicalStationKind.CODE_READING,
        title=_lt(
            "Leer log-sum-exp",
            "Read log-sum-exp",
            "Læs log-sum-exp",
        ),
        artifact_title=_lt("Código", "Code", "Kode"),
        artifact="""def logsumexp(values: list[float]) -> float:
    maximum = max(values)
    return maximum + log(sum(exp(value - maximum) for value in values))""",
        prompt=_lt(
            "Deriva por qué la expresión es equivalente a log(sum(exp(values))) y explica cómo restar maximum mejora la estabilidad numérica sin cambiar el resultado matemático.",
            "Derive why the expression equals log(sum(exp(values))) and explain how subtracting maximum improves numerical stability without changing the mathematical result.",
            "Udled hvorfor udtrykket er lig log(sum(exp(values))) og forklar hvordan subtraktion af maximum forbedrer numerisk stabilitet uden at ændre det matematiske resultat.",
        ),
        criteria=(
            _criterion(
                "identity",
                "Factoriza exp(maximum) dentro de la suma.",
                "Factor exp(maximum) out of the sum.",
                "Faktoriser exp(maximum) ud af summen.",
            ),
            _criterion(
                "stability",
                "Explica que los exponentes desplazados son <= 0 y evitan overflow.",
                "Explain that shifted exponents are <= 0 and avoid overflow.",
                "Forklar at forskudte eksponenter er <= 0 og undgår overflow.",
            ),
            _criterion(
                "edge",
                "Menciona el contrato necesario para lista vacía o valores -inf.",
                "Mention the required contract for an empty list or -inf values.",
                "Nævn den nødvendige kontrakt for en tom liste eller -inf-værdier.",
            ),
        ),
        estimated_minutes=12,
        source_basis=("dm847.lab04.hidden-markov-model", "DM847 numerical stability in HMMs"),
    ),
    TechnicalStation(
        station_id="dm847.lab04.station.trace-forward-viterbi",
        course_code="DM847",
        lab_id="dm847.lab04.hidden-markov-model",
        kind=TechnicalStationKind.EXECUTION_TRACE,
        title=_lt(
            "Separar Forward y Viterbi en una columna",
            "Separate Forward and Viterbi in one column",
            "Adskil Forward og Viterbi i én kolonne",
        ),
        artifact_title=_lt("Valores previos", "Previous values", "Tidligere værdier"),
        artifact="""Previous log scores for states H and L: [-1.0, -1.4]
Transitions into H: log(0.8), log(0.2)
Emission of G from H: log(0.4)

Compute:
1. Forward score for H at the next position
2. Viterbi score for H at the next position""",
        prompt=_lt(
            "Escribe las dos expresiones, identifica dónde se usa suma logarítmica y dónde máximo, y explica qué información descarta Viterbi.",
            "Write both expressions, identify where log-sum is used and where max is used, and explain which information Viterbi discards.",
            "Skriv begge udtryk, identificér hvor log-sum bruges og hvor max bruges, og forklar hvilken information Viterbi kasserer.",
        ),
        criteria=(
            _criterion(
                "forward",
                "Forward combina ambas rutas mediante logsumexp antes de la emisión.",
                "Forward combines both paths with logsumexp before the emission.",
                "Forward kombinerer begge stier med logsumexp før emissionen.",
            ),
            _criterion(
                "viterbi",
                "Viterbi conserva el máximo y registra su predecesor.",
                "Viterbi retains the maximum and records its predecessor.",
                "Viterbi bevarer maksimum og registrerer forgængeren.",
            ),
            _criterion(
                "information",
                "Explica que Viterbi descarta masa de probabilidad de rutas no máximas.",
                "Explain that Viterbi discards probability mass from non-maximal paths.",
                "Forklar at Viterbi kasserer sandsynlighedsmasse fra ikke-maksimale stier.",
            ),
        ),
        estimated_minutes=15,
        source_basis=("dm847.lab04.hidden-markov-model", "DM847 Forward versus Viterbi"),
    ),
    TechnicalStation(
        station_id="dm847.lab04.station.debug-backward-init",
        course_code="DM847",
        lab_id="dm847.lab04.hidden-markov-model",
        kind=TechnicalStationKind.DEBUGGING,
        title=_lt(
            "Depurar la inicialización Backward",
            "Debug Backward initialization",
            "Fejlfind Backward-initialisering",
        ),
        artifact_title=_lt("Código defectuoso", "Defective code", "Defekt kode"),
        artifact="""beta = [[float("-inf")] * K for _ in range(T)]
for state in range(K):
    beta[T - 1][state] = log(initial[state])

# Posterior rows no longer sum to 1 after combining alpha and beta.""",
        prompt=_lt(
            "Identifica el error conceptual, corrige la condición terminal y explica por qué usar initial dos veces distorsiona los posteriores.",
            "Identify the conceptual error, correct the terminal condition, and explain why using initial twice distorts the posteriors.",
            "Identificér den konceptuelle fejl, ret terminalbetingelsen og forklar hvorfor brug af initial to gange forvrider posteriorerne.",
        ),
        criteria=(
            _criterion(
                "terminal",
                "Establece beta[T-1][state] = 0.0 en espacio log.",
                "Set beta[T-1][state] = 0.0 in log space.",
                "Sæt beta[T-1][state] = 0.0 i log-rum.",
            ),
            _criterion(
                "meaning",
                "Explica que no queda evidencia futura tras la última observación.",
                "Explain that no future evidence remains after the final observation.",
                "Forklar at der ikke er fremtidig evidens efter den sidste observation.",
            ),
            _criterion(
                "effect",
                "Relaciona el doble uso de initial con normalización posterior incorrecta.",
                "Relate double use of initial to incorrect posterior normalization.",
                "Knyt dobbelt brug af initial til forkert posterior-normalisering.",
            ),
        ),
        estimated_minutes=12,
        source_basis=("dm847.lab04.hidden-markov-model", "DM847 Forward-Backward invariants"),
    ),
    TechnicalStation(
        station_id="dm847.lab04.station.interpret-path-posterior",
        course_code="DM847",
        lab_id="dm847.lab04.hidden-markov-model",
        kind=TechnicalStationKind.OUTPUT_INTERPRETATION,
        title=_lt(
            "Interpretar trayectoria y posteriores",
            "Interpret path and posteriors",
            "Fortolk sti og posteriorer",
        ),
        artifact_title=_lt("Salida", "Output", "Output"),
        artifact="""observations = ACGT
viterbi_path = HHHH
posterior P(H | full sequence) = [0.382, 0.732, 0.732, 0.382]""",
        prompt=_lt(
            "Explica por qué la trayectoria Viterbi puede ser HHHH aunque L tenga posterior marginal mayor en posiciones 1 y 4. Distingue trayectoria conjunta óptima, estado marginal y evidencia biológica.",
            "Explain why the Viterbi path can be HHHH even though L has the larger marginal posterior at positions 1 and 4. Distinguish optimal joint path, marginal state, and biological evidence.",
            "Forklar hvorfor Viterbi-stien kan være HHHH selv om L har større marginal posterior ved position 1 og 4. Skeln optimal fælles sti, marginal tilstand og biologisk evidens.",
        ),
        criteria=(
            _criterion(
                "joint",
                "Define Viterbi como una trayectoria conjunta global.",
                "Define Viterbi as one global joint path.",
                "Definér Viterbi som én global fælles sti.",
            ),
            _criterion(
                "marginal",
                "Define cada posterior como suma sobre trayectorias compatibles en una posición.",
                "Define each posterior as a sum over compatible paths at one position.",
                "Definér hver posterior som en sum over kompatible stier ved én position.",
            ),
            _criterion(
                "boundary",
                "Aclara que H/L son estados sintéticos y no anotaciones biológicas validadas.",
                "Clarify that H/L are synthetic states, not validated biological annotations.",
                "Præcisér at H/L er syntetiske tilstande, ikke validerede biologiske annoteringer.",
            ),
        ),
        estimated_minutes=12,
        source_basis=("dm847.lab04.hidden-markov-model", "DM847 posterior uncertainty interpretation"),
    ),
)


STATIONS_BY_LAB = {
    lab_id: tuple(station for station in DM847_TECHNICAL_STATIONS if station.lab_id == lab_id)
    for lab_id in {
        "dm847.lab01.sequence-mapping",
        "dm847.lab02.pairwise-alignment",
        "dm847.lab03.sequence-index",
        "dm847.lab04.hidden-markov-model",
    }
}

__all__ = ["DM847_TECHNICAL_STATIONS", "STATIONS_BY_LAB"]
