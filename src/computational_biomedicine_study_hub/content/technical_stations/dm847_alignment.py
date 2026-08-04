"""Technical reasoning stations for DM847 pairwise alignment."""

from __future__ import annotations

from ...learning.technical_stations import TechnicalStation, TechnicalStationKind
from ._shared import criterion, localized

LAB_ID = "dm847.lab02.pairwise-alignment"

DM847_ALIGNMENT_STATIONS = (
    TechnicalStation(
        station_id="dm847.lab02.station.read-recurrence",
        course_code="DM847",
        lab_id=LAB_ID,
        kind=TechnicalStationKind.CODE_READING,
        title=localized(
            "Leer la recurrencia global",
            "Read the global recurrence",
            "Læs den globale rekurrens",
        ),
        artifact_title=localized("Código", "Code", "Kode"),
        artifact="""diagonal = score[i - 1][j - 1] + substitution(a[i - 1], b[j - 1])
up = score[i - 1][j] + gap
left = score[i][j - 1] + gap
score[i][j] = max(diagonal, up, left)""",
        prompt=localized(
            "Explica qué representa score[i][j], qué subproblema corresponde a cada "
            "transición y por qué la inicialización de fila y columna determina que el "
            "alineamiento sea global.",
            "Explain what score[i][j] represents, which subproblem each transition "
            "corresponds to, and why row and column initialization makes the alignment global.",
            "Forklar hvad score[i][j] repræsenterer, hvilket delproblem hver overgang svarer "
            "til, og hvorfor initialisering af række og kolonne gør aligneringen global.",
        ),
        criteria=(
            criterion(
                "state",
                "Define score[i][j] sobre prefijos de longitudes i y j.",
                "Define score[i][j] over prefixes of lengths i and j.",
                "Definér score[i][j] over præfikser med længder i og j.",
            ),
            criterion(
                "transitions",
                "Relaciona diagonal, up y left con sustitución y gaps.",
                "Relate diagonal, up, and left to substitution and gaps.",
                "Knyt diagonal, up og left til substitution og gaps.",
            ),
            criterion(
                "global",
                "Explica la penalización acumulada de prefijos contra vacío.",
                "Explain accumulated penalties for prefixes aligned to empty.",
                "Forklar akkumulerede straffe for præfikser alignet mod tom sekvens.",
            ),
        ),
        estimated_minutes=12,
        source_basis=(LAB_ID, "DM847 dynamic programming outcomes"),
    ),
    TechnicalStation(
        station_id="dm847.lab02.station.trace-cell",
        course_code="DM847",
        lab_id=LAB_ID,
        kind=TechnicalStationKind.EXECUTION_TRACE,
        title=localized(
            "Calcular una celda de alineamiento",
            "Calculate one alignment cell",
            "Beregn én aligneringscelle",
        ),
        artifact_title=localized(
            "Estado parcial",
            "Partial state",
            "Delvis tilstand",
        ),
        artifact="""a = "AG"
b = "AC"
match = 2
mismatch = -1
gap = -2

score[1][1] = 2
score[1][2] = 0
score[2][1] = 0

Compute score[2][2].""",
        prompt=localized(
            "Calcula diagonal, up y left para score[2][2], selecciona el máximo y explica "
            "qué columnas alineadas representa cada opción.",
            "Calculate diagonal, up, and left for score[2][2], select the maximum, and "
            "explain which aligned columns each option represents.",
            "Beregn diagonal, up og left for score[2][2], vælg maksimum og forklar hvilke "
            "alignerede kolonner hver mulighed repræsenterer.",
        ),
        criteria=(
            criterion(
                "values",
                "Obtiene diagonal=1, up=-2 y left=-2.",
                "Obtain diagonal=1, up=-2, and left=-2.",
                "Opnå diagonal=1, up=-2 og left=-2.",
            ),
            criterion(
                "choice",
                "Selecciona score[2][2]=1 mediante mismatch G/C.",
                "Select score[2][2]=1 through the G/C mismatch.",
                "Vælg score[2][2]=1 via G/C-mismatch.",
            ),
            criterion(
                "meaning",
                "Relaciona cada transición con consumo de caracteres en a y b.",
                "Relate each transition to character consumption in a and b.",
                "Knyt hver overgang til forbrug af tegn i a og b.",
            ),
        ),
        estimated_minutes=10,
        source_basis=(LAB_ID, "DM847 manual DP tracing"),
    ),
    TechnicalStation(
        station_id="dm847.lab02.station.debug-local-stop",
        course_code="DM847",
        lab_id=LAB_ID,
        kind=TechnicalStationKind.DEBUGGING,
        title=localized(
            "Depurar un traceback local que invade regiones negativas",
            "Debug a local traceback entering negative regions",
            "Fejlfind et lokalt traceback der går ind i negative områder",
        ),
        artifact_title=localized(
            "Código defectuoso",
            "Defective code",
            "Defekt kode",
        ),
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
        prompt=localized(
            "Explica qué condición de parada falta en Smith–Waterman, cómo el defecto altera "
            "las coordenadas locales y qué prueba mínima lo detecta.",
            "Explain which Smith–Waterman stopping condition is missing, how the defect changes "
            "local coordinates, and which minimal test detects it.",
            "Forklar hvilken stopbetingelse fra Smith–Waterman der mangler, hvordan fejlen "
            "ændrer lokale koordinater, og hvilken minimal test der opdager den.",
        ),
        criteria=(
            criterion(
                "stop",
                "Añade parada cuando score[i][j] == 0.",
                "Add a stop when score[i][j] == 0.",
                "Tilføj stop når score[i][j] == 0.",
            ),
            criterion(
                "coordinates",
                "Explica que continuar incorpora prefijos fuera de la región local óptima.",
                "Explain that continuing includes prefixes outside the optimal local region.",
                "Forklar at fortsættelse inkluderer præfikser uden for den optimale lokale region.",
            ),
            criterion(
                "test",
                "Propone secuencias con una coincidencia interna y flancos no relacionados.",
                "Propose sequences with an internal match and unrelated flanks.",
                "Foreslå sekvenser med et internt match og ikke-relaterede flanker.",
            ),
        ),
        estimated_minutes=12,
        source_basis=(LAB_ID, "DM847 Smith-Waterman traceback"),
    ),
    TechnicalStation(
        station_id="dm847.lab02.station.select-global-local",
        course_code="DM847",
        lab_id=LAB_ID,
        kind=TechnicalStationKind.METHOD_SELECTION,
        title=localized(
            "Elegir alineamiento global o local",
            "Choose global or local alignment",
            "Vælg global eller lokal alignment",
        ),
        artifact_title=localized("Escenario", "Scenario", "Scenarie"),
        artifact="""Sequence A: a full-length 900 bp gene candidate
Sequence B: a 120 bp conserved domain-like segment from another sample
Goal: determine whether B occurs as a high-scoring region inside A.""",
        prompt=localized(
            "Selecciona un método, justifica la elección, define qué resultado revisarías y "
            "explica dos razones por las que un score alto no demuestra homología ni función "
            "compartida.",
            "Select a method, justify the choice, define which result you would inspect, and "
            "explain two reasons why a high score does not establish homology or shared function.",
            "Vælg en metode, begrund valget, definér hvilket resultat du vil inspicere, og "
            "forklar to grunde til at en høj score ikke fastslår homologi eller delt funktion.",
        ),
        criteria=(
            criterion(
                "method",
                "Selecciona alineamiento local por la relación segmento-dentro-de-secuencia.",
                "Select local alignment for the segment-within-sequence relation.",
                "Vælg lokal alignment for segment-i-sekvens-relationen.",
            ),
            criterion(
                "output",
                "Menciona score, coordenadas, alineamiento y sensibilidad a parámetros.",
                "Mention score, coordinates, alignment, and parameter sensitivity.",
                "Nævn score, koordinater, alignment og parameterfølsomhed.",
            ),
            criterion(
                "boundary",
                "Separa similitud computacional de historia evolutiva y función.",
                "Separate computational similarity from evolutionary history and function.",
                "Adskil beregningsmæssig lighed fra evolutionær historie og funktion.",
            ),
        ),
        estimated_minutes=12,
        source_basis=(
            LAB_ID,
            "DM847 method selection and interpretation",
        ),
    ),
)

__all__ = ["DM847_ALIGNMENT_STATIONS"]
