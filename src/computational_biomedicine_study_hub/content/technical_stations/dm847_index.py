"""Technical reasoning stations for DM847 sequence indexes."""

from __future__ import annotations

from ...learning.technical_stations import TechnicalStation, TechnicalStationKind
from ._shared import criterion, localized

LAB_ID = "dm847.lab03.sequence-indexes"

DM847_INDEX_STATIONS = (
    TechnicalStation(
        station_id="dm847.lab03.station.read-occ",
        course_code="DM847",
        lab_id=LAB_ID,
        kind=TechnicalStationKind.CODE_READING,
        title=localized(
            "Leer la semántica de Occ",
            "Read Occ semantics",
            "Læs Occ-semantikken",
        ),
        artifact_title=localized("Código", "Code", "Kode"),
        artifact="""def build_occ(bwt: str, alphabet: tuple[str, ...]) -> dict[str, list[int]]:
    occ = {symbol: [0] for symbol in alphabet}
    for char in bwt:
        for symbol in alphabet:
            occ[symbol].append(occ[symbol][-1] + int(char == symbol))
    return occ""",
        prompt=localized(
            "Explica exactamente qué representa occ[c][k], por qué cada lista tiene "
            "len(bwt)+1 elementos y cómo esta convención evita errores en intervalos half-open.",
            "Explain exactly what occ[c][k] represents, why each list has len(bwt)+1 "
            "elements, and how this convention avoids errors in half-open intervals.",
            "Forklar præcist hvad occ[c][k] repræsenterer, hvorfor hver liste har "
            "len(bwt)+1 elementer, og hvordan denne konvention undgår fejl i halvåbne "
            "intervaller.",
        ),
        criteria=(
            criterion(
                "meaning",
                "Define occ[c][k] como conteo en bwt[:k].",
                "Define occ[c][k] as the count in bwt[:k].",
                "Definér occ[c][k] som antallet i bwt[:k].",
            ),
            criterion(
                "length",
                "Explica el prefijo vacío en k=0 y el prefijo completo en k=n.",
                "Explain the empty prefix at k=0 and complete prefix at k=n.",
                "Forklar det tomme præfiks ved k=0 og hele præfikset ved k=n.",
            ),
            criterion(
                "interval",
                "Relaciona top/bottom con conteos sin ajustes -1 ad hoc.",
                "Relate top/bottom to counts without ad hoc -1 adjustments.",
                "Knyt top/bottom til tællinger uden ad hoc -1-justeringer.",
            ),
        ),
        estimated_minutes=12,
        source_basis=(LAB_ID, "DM847 BWT occurrence tables"),
    ),
    TechnicalStation(
        station_id="dm847.lab03.station.trace-backward",
        course_code="DM847",
        lab_id=LAB_ID,
        kind=TechnicalStationKind.EXECUTION_TRACE,
        title=localized(
            "Trazar backward search",
            "Trace backward search",
            "Spor backward search",
        ),
        artifact_title=localized("Índice", "Index", "Indeks"),
        artifact="""text = "GATTACA$"
BWT = "ACTGA$TA"
C = {"$": 0, "A": 1, "C": 4, "G": 5, "T": 6}
pattern = "TA"
Start interval: [0, 8)
Process pattern from right to left.""",
        prompt=localized(
            "Actualiza el intervalo para A y luego para T. Explica qué conjunto de sufijos "
            "representa cada intervalo y cómo count se obtiene de su anchura.",
            "Update the interval for A and then T. Explain which suffix set each interval "
            "represents and how count is obtained from its width.",
            "Opdatér intervallet for A og derefter T. Forklar hvilket suffikssæt hvert "
            "interval repræsenterer, og hvordan count fås fra intervallets bredde.",
        ),
        criteria=(
            criterion(
                "a-step",
                "Calcula correctamente el intervalo tras procesar A.",
                "Calculate the correct interval after processing A.",
                "Beregn det korrekte interval efter behandling af A.",
            ),
            criterion(
                "t-step",
                "Calcula correctamente el intervalo final para TA.",
                "Calculate the correct final interval for TA.",
                "Beregn det korrekte slutinterval for TA.",
            ),
            criterion(
                "semantics",
                "Interpreta filas del BWT y diferencia count de coordenadas de referencia.",
                "Interpret BWT rows and distinguish count from reference coordinates.",
                "Fortolk BWT-rækker og skeln count fra referencekoordinater.",
            ),
        ),
        estimated_minutes=15,
        source_basis=(LAB_ID, "DM847 FM-index backward search"),
    ),
    TechnicalStation(
        station_id="dm847.lab03.station.debug-locate",
        course_code="DM847",
        lab_id=LAB_ID,
        kind=TechnicalStationKind.DEBUGGING,
        title=localized(
            "Depurar count confundido con locate",
            "Debug count confused with locate",
            "Fejlfind count forvekslet med locate",
        ),
        artifact_title=localized(
            "Código defectuoso",
            "Defective code",
            "Defekt kode",
        ),
        artifact="""def locate(index: FMIndex, pattern: str) -> list[int]:
    top, bottom = backward_search(index, pattern)
    return list(range(top, bottom))

# Returned [2, 3] for a pattern whose reference positions are [1, 4].""",
        prompt=localized(
            "Explica la confusión entre filas del suffix array y coordenadas de referencia, "
            "corrige la lógica y especifica un test que pueda pasar count pero fallar locate.",
            "Explain the confusion between suffix-array rows and reference coordinates, "
            "correct the logic, and specify a test that can pass count but fail locate.",
            "Forklar forvekslingen mellem suffix-array-rækker og referencekoordinater, ret "
            "logikken og angiv en test der kan bestå count men fejle locate.",
        ),
        criteria=(
            criterion(
                "distinction",
                "Distingue índices de fila [top,bottom) de valores SA[row].",
                "Distinguish row indices [top,bottom) from SA[row] values.",
                "Skeln rækkeindekser [top,bottom) fra SA[row]-værdier.",
            ),
            criterion(
                "fix",
                "Devuelve y ordena index.suffix_array[top:bottom].",
                "Return and sort index.suffix_array[top:bottom].",
                "Returnér og sortér index.suffix_array[top:bottom].",
            ),
            criterion(
                "test",
                "Usa un patrón donde las filas no coincidan numéricamente con posiciones.",
                "Use a pattern where rows do not numerically equal positions.",
                "Brug et mønster hvor rækker ikke numerisk svarer til positioner.",
            ),
        ),
        estimated_minutes=12,
        source_basis=(LAB_ID, "DM847 count versus locate distinction"),
    ),
    TechnicalStation(
        station_id="dm847.lab03.station.complexity-tradeoff",
        course_code="DM847",
        lab_id=LAB_ID,
        kind=TechnicalStationKind.COMPLEXITY_ANALYSIS,
        title=localized(
            "Defender el coste de un índice",
            "Defend the cost of an index",
            "Forsvar omkostningen ved et indeks",
        ),
        artifact_title=localized("Escenario", "Scenario", "Scenarie"),
        artifact="""Reference length n = 3,000,000,000
Pattern length m = 100
Queries q = 50,000,000
Options:
A. exhaustive scan for every query
B. suffix array with binary search
C. FM-index with sampled suffix array""",
        prompt=localized(
            "Compara preprocesamiento, tiempo por consulta, memoria y capacidad count/locate. "
            "Justifica una elección y menciona qué cambia cuando se permiten mismatches o indels.",
            "Compare preprocessing, per-query time, memory, and count/locate capability. "
            "Justify one choice and mention what changes when mismatches or indels are allowed.",
            "Sammenlign preprocessing, tid pr. forespørgsel, hukommelse og count/locate-"
            "kapacitet. Begrund ét valg og nævn hvad der ændres når mismatches eller indels "
            "tillades.",
        ),
        criteria=(
            criterion(
                "variables",
                "Usa n, m y q y separa preprocesamiento de consultas.",
                "Use n, m, and q and separate preprocessing from queries.",
                "Brug n, m og q og adskil preprocessing fra forespørgsler.",
            ),
            criterion(
                "tradeoff",
                "Explica memoria frente a velocidad y count frente a locate.",
                "Explain memory versus speed and count versus locate.",
                "Forklar hukommelse versus hastighed og count versus locate.",
            ),
            criterion(
                "extension",
                "Reconoce que búsqueda aproximada y alineamiento requieren lógica adicional.",
                "Recognize that approximate search and alignment require additional logic.",
                "Anerkend at tilnærmet søgning og alignment kræver yderligere logik.",
            ),
        ),
        estimated_minutes=15,
        source_basis=(LAB_ID, "DM847 complexity and index trade-offs"),
    ),
)

__all__ = ["DM847_INDEX_STATIONS"]
