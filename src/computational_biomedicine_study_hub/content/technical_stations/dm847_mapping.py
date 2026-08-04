"""Technical reasoning stations for DM847 short-read mapping."""

from __future__ import annotations

from ...learning.technical_stations import TechnicalStation, TechnicalStationKind
from ._shared import criterion, localized

LAB_ID = "dm847.lab01.short-read-mapping"

DM847_MAPPING_STATIONS = (
    TechnicalStation(
        station_id="dm847.lab01.station.code-contract",
        course_code="DM847",
        lab_id=LAB_ID,
        kind=TechnicalStationKind.CODE_READING,
        title=localized(
            "Leer el contrato de una búsqueda aproximada",
            "Read an approximate-search contract",
            "Læs kontrakten for en tilnærmet søgning",
        ),
        artifact_title=localized("Código", "Code", "Kode"),
        artifact="""def candidate_positions(reference: str, read: str, max_mismatches: int) -> list[int]:
    positions = []
    for start in range(len(reference) - len(read) + 1):
        window = reference[start : start + len(read)]
        mismatches = sum(a != b for a, b in zip(window, read, strict=True))
        if mismatches <= max_mismatches:
            positions.append(start)
    return positions""",
        prompt=localized(
            "Explica el contrato de entrada y salida, por qué el límite del range incluye +1, "
            "qué supone zip(strict=True) y qué casos debe rechazar una implementación robusta.",
            "Explain the input/output contract, why the range bound includes +1, what "
            "zip(strict=True) assumes, and which cases a robust implementation should reject.",
            "Forklar input/output-kontrakten, hvorfor range-grænsen indeholder +1, hvad "
            "zip(strict=True) antager, og hvilke tilfælde en robust implementering bør afvise.",
        ),
        criteria=(
            criterion(
                "contract",
                "Define tipos, coordenadas y significado de max_mismatches.",
                "Define types, coordinates, and the meaning of max_mismatches.",
                "Definér typer, koordinater og betydningen af max_mismatches.",
            ),
            criterion(
                "boundary",
                "Explica el último inicio válido y el caso read más largo que reference.",
                "Explain the last valid start and the read-longer-than-reference case.",
                "Forklar den sidste gyldige start og tilfældet hvor read er længere end reference.",
            ),
            criterion(
                "validation",
                "Identifica entradas inválidas y al menos una decisión de validación.",
                "Identify invalid inputs and at least one validation decision.",
                "Identificér ugyldige input og mindst én valideringsbeslutning.",
            ),
        ),
        estimated_minutes=12,
        source_basis=(LAB_ID, "DM847 sequence matching outcomes"),
    ),
    TechnicalStation(
        station_id="dm847.lab01.station.trace-overlap",
        course_code="DM847",
        lab_id=LAB_ID,
        kind=TechnicalStationKind.EXECUTION_TRACE,
        title=localized(
            "Trazar coincidencias solapadas",
            "Trace overlapping matches",
            "Spor overlappende matches",
        ),
        artifact_title=localized("Entrada", "Input", "Input"),
        artifact="""reference = "AAAAA"
read = "AAA"
max_mismatches = 0""",
        prompt=localized(
            "Traza cada ventana examinada, calcula mismatches y determina la lista final. "
            "Después explica por qué eliminar solapamientos cambiaría el contrato del algoritmo.",
            "Trace every examined window, calculate mismatches, and determine the final list. "
            "Then explain why removing overlaps would change the algorithm contract.",
            "Spor hvert undersøgt vindue, beregn mismatches og bestem den endelige liste. "
            "Forklar derefter hvorfor fjernelse af overlap ville ændre algoritmens kontrakt.",
        ),
        criteria=(
            criterion(
                "windows",
                "Enumera las tres ventanas y sus coordenadas de inicio.",
                "Enumerate the three windows and their start coordinates.",
                "Angiv de tre vinduer og deres startkoordinater.",
            ),
            criterion(
                "result",
                "Obtiene [0, 1, 2] con mismatches cero.",
                "Obtain [0, 1, 2] with zero mismatches.",
                "Opnå [0, 1, 2] med nul mismatches.",
            ),
            criterion(
                "semantics",
                "Distingue coincidencia solapada de duplicación accidental.",
                "Distinguish an overlapping match from accidental duplication.",
                "Skeln mellem et overlappende match og utilsigtet duplikering.",
            ),
        ),
        estimated_minutes=10,
        source_basis=(LAB_ID, "DM847 exact matching practice"),
    ),
    TechnicalStation(
        station_id="dm847.lab01.station.debug-off-by-one",
        course_code="DM847",
        lab_id=LAB_ID,
        kind=TechnicalStationKind.DEBUGGING,
        title=localized(
            "Depurar una pérdida de la última posición",
            "Debug a missing final position",
            "Fejlfind en manglende sidste position",
        ),
        artifact_title=localized(
            "Código defectuoso",
            "Defective code",
            "Defekt kode",
        ),
        artifact="""def exact_positions(reference: str, read: str) -> list[int]:
    hits = []
    for start in range(len(reference) - len(read)):
        if reference[start : start + len(read)] == read:
            hits.append(start)
    return hits

print(exact_positions("ACGT", "GT"))  # received []""",
        prompt=localized(
            "Localiza el defecto, construye la tabla de valores de start realmente visitados, "
            "corrige la expresión y formula una prueba de regresión mínima.",
            "Locate the defect, build the table of start values actually visited, correct the "
            "expression, and formulate a minimal regression test.",
            "Find fejlen, opbyg tabellen over de start-værdier der faktisk besøges, ret "
            "udtrykket og formulér en minimal regressionstest.",
        ),
        criteria=(
            criterion(
                "cause",
                "Explica por qué range excluye el límite superior.",
                "Explain why range excludes its upper bound.",
                "Forklar hvorfor range udelukker sin øvre grænse.",
            ),
            criterion(
                "fix",
                "Corrige a len(reference) - len(read) + 1.",
                "Correct to len(reference) - len(read) + 1.",
                "Ret til len(reference) - len(read) + 1.",
            ),
            criterion(
                "regression",
                "Incluye un test donde la única coincidencia termina al final de reference.",
                "Include a test where the only match ends at the end of reference.",
                "Medtag en test hvor det eneste match slutter ved reference-strengens slutning.",
            ),
        ),
        estimated_minutes=10,
        source_basis=(LAB_ID, "DM847 debugging practice"),
    ),
    TechnicalStation(
        station_id="dm847.lab01.station.interpret-multimapping",
        course_code="DM847",
        lab_id=LAB_ID,
        kind=TechnicalStationKind.SCIENTIFIC_INTERPRETATION,
        title=localized(
            "Interpretar una lectura multimapeada",
            "Interpret a multimapped read",
            "Fortolk en multimappet read",
        ),
        artifact_title=localized("Resultado", "Result", "Resultat"),
        artifact="""read_id: r17
read: CG
candidate_positions: [1, 4, 7]
classification: multimapping
reference: ACGTCGACG""",
        prompt=localized(
            "Separa con precisión lo que demuestra el resultado, lo que podría sugerir y lo "
            "que no permite concluir sobre el origen biológico de la lectura.",
            "Separate precisely what the result establishes, what it may suggest, and what it "
            "does not permit you to conclude about the biological origin of the read.",
            "Adskil præcist hvad resultatet fastslår, hvad det kan antyde, og hvad det ikke gør "
            "det muligt at konkludere om readens biologiske oprindelse.",
        ),
        criteria=(
            criterion(
                "establishes",
                "Afirma únicamente tres coincidencias exactas bajo este modelo y referencia.",
                "State only three exact matches under this model and reference.",
                "Angiv kun tre eksakte matches under denne model og reference.",
            ),
            criterion(
                "uncertainty",
                "Explica que no se identifica cuál posición originó la lectura.",
                "Explain that the originating position is not identified.",
                "Forklar at den oprindelige position ikke identificeres.",
            ),
            criterion(
                "limits",
                "Menciona referencia, hebra, errores, indels o calidad como límites relevantes.",
                "Mention reference, strand, errors, indels, or quality as relevant limits.",
                "Nævn reference, streng, fejl, indels eller kvalitet som relevante begrænsninger.",
            ),
        ),
        estimated_minutes=12,
        source_basis=(LAB_ID, "DM847 biomedical interpretation boundary"),
    ),
)

__all__ = ["DM847_MAPPING_STATIONS"]
