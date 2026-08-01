"""Book-grounded audit and focused extensions for DM847.

The audit maps every authored module to the active course scope and to the
relevant chapters of Compeau and Pevzner. A module is marked ``consistent``
only after a focused comparison and regression coverage. The visible teaching
material is original paraphrase and adaptation rather than reproduced textbook
prose or proprietary exercises.
"""

from __future__ import annotations

from dataclasses import dataclass, replace
from typing import Literal

from ...learning.activity_types import ActivityType
from ..localized_models import LocalizedLearningModule, LocalizedTutorSupportPacket
from .authoring import concept, example, objective, objective_mcq, practice

VerificationState = Literal["pending", "consistent", "improve", "correct", "outside_scope"]


@dataclass(frozen=True, slots=True)
class AcademicReference:
    """One stable source used by the DM847 content audit."""

    source_id: str
    citation: str
    relevant_scope: str


@dataclass(frozen=True, slots=True)
class ModuleSourceAudit:
    """Source mapping and verification state for one DM847 module."""

    module_id: str
    source_ids: tuple[str, ...]
    source_scope: tuple[str, ...]
    state: VerificationState
    finding: str
    implemented_change: str = ""


DM847_BOOK_SOURCES: tuple[AcademicReference, ...] = (
    AcademicReference(
        source_id="sdu-dm847-active-2025",
        citation="SDU, DM847: Introduction to Bioinformatics, approved active course description (2025).",
        relevant_scope=(
            "biological-question framing, computational models, sequence analysis, HMMs, "
            "suffix structures, BWT, operons, motif discovery, networks, and OMICS learning"
        ),
    ),
    AcademicReference(
        source_id="compeau-pevzner-v1-ch01",
        citation=(
            "Phillip Compeau and Pavel Pevzner, Bioinformatics Algorithms: "
            "An Active Learning Approach, 2nd ed., vol. I (2015), chapter 1."
        ),
        relevant_scope=(
            "exact and approximate pattern matching, Hamming distance, frequent words, "
            "clumps, reverse complements, and biological problem formulation"
        ),
    ),
    AcademicReference(
        source_id="compeau-pevzner-v1-ch02",
        citation=(
            "Phillip Compeau and Pavel Pevzner, Bioinformatics Algorithms: "
            "An Active Learning Approach, 2nd ed., vol. I (2015), chapter 2."
        ),
        relevant_scope=(
            "motif finding, profile models, entropy, greedy and randomized searches, "
            "and biological validation boundaries"
        ),
    ),
    AcademicReference(
        source_id="compeau-pevzner-v1-ch05",
        citation=(
            "Phillip Compeau and Pavel Pevzner, Bioinformatics Algorithms: "
            "An Active Learning Approach, 2nd ed., vol. I (2015), chapter 5."
        ),
        relevant_scope=(
            "sequence alignment, longest paths in DAGs, dynamic programming, global and "
            "local alignment, affine gaps, and linear-space alignment"
        ),
    ),
    AcademicReference(
        source_id="compeau-pevzner-v2-ch08",
        citation=(
            "Phillip Compeau and Pavel Pevzner, Bioinformatics Algorithms: "
            "An Active Learning Approach, 2nd ed., vol. II (2015), chapter 8."
        ),
        relevant_scope=(
            "hard and soft clustering, distortion, Lloyd iteration, expectation maximization, "
            "and hierarchical clustering"
        ),
    ),
    AcademicReference(
        source_id="compeau-pevzner-v2-ch09",
        citation=(
            "Phillip Compeau and Pavel Pevzner, Bioinformatics Algorithms: "
            "An Active Learning Approach, 2nd ed., vol. II (2015), chapter 9."
        ),
        relevant_scope=(
            "Burrows-Wheeler transform, first-last mapping, backward search, "
            "string reconstruction, and read-mapping foundations"
        ),
    ),
    AcademicReference(
        source_id="compeau-pevzner-v2-ch10",
        citation=(
            "Phillip Compeau and Pavel Pevzner, Bioinformatics Algorithms: "
            "An Active Learning Approach, 2nd ed., vol. II (2015), chapter 10."
        ),
        relevant_scope="hidden Markov models, decoding, learning, and sequence applications",
    ),
    AcademicReference(
        source_id="compeau-pevzner-v2-ch11",
        citation=(
            "Phillip Compeau and Pavel Pevzner, Bioinformatics Algorithms: "
            "An Active Learning Approach, 2nd ed., vol. II (2015), chapter 11."
        ),
        relevant_scope="biological networks, graph algorithms, and network-based interpretation",
    ),
)


DM847_MODULE_SOURCE_AUDIT: tuple[ModuleSourceAudit, ...] = (
    ModuleSourceAudit(
        "dm847.m01",
        ("sdu-dm847-active-2025", "compeau-pevzner-v1-ch01"),
        (
            "biological question to computational representation",
            "sequence orientation and reverse complements",
            "regulatory and bacterial context",
        ),
        "pending",
        "Course scope is mapped; focused source comparison remains pending.",
    ),
    ModuleSourceAudit(
        "dm847.m02",
        ("sdu-dm847-active-2025",),
        ("biomedical ontologies", "database design", "provenance and identifiers"),
        "pending",
        (
            "The active course scope is mapped. The Compeau-Pevzner volumes are not a "
            "complete reference for ontology and database engineering, so a suitable "
            "specialized source review remains pending."
        ),
    ),
    ModuleSourceAudit(
        "dm847.m03",
        (
            "sdu-dm847-active-2025",
            "compeau-pevzner-v1-ch01",
            "compeau-pevzner-v1-ch05",
        ),
        (
            "k-mer composition",
            "exact and approximate pattern matching",
            "sequence scoring and statistical evidence",
        ),
        "consistent",
        (
            "Existing coverage of k-mer composition, substitution matrices, log-odds, "
            "exact search, null models, and multiplicity is consistent. Approximate "
            "pattern matching through Hamming neighborhoods required one explicit treatment."
        ),
        (
            "Added an original trilingual explanation, deterministic approximate-search "
            "example, debugging practice, and stable objective item."
        ),
    ),
    ModuleSourceAudit(
        "dm847.m04",
        ("sdu-dm847-active-2025", "compeau-pevzner-v1-ch05"),
        (
            "dynamic-programming state and recurrence",
            "global, local, and affine-gap alignment",
            "score-only memory reduction and traceback",
        ),
        "consistent",
        (
            "Existing coverage of alignment objectives, recurrences, initialization, "
            "traceback, affine gaps, ties, and validation is consistent. The memory boundary "
            "between score-only dynamic programming and alignment reconstruction required "
            "one explicit treatment."
        ),
        (
            "Added an original linear-memory score explanation, rolling-row example, "
            "design exercise, and stable objective item."
        ),
    ),
    ModuleSourceAudit(
        "dm847.m05",
        ("sdu-dm847-active-2025", "compeau-pevzner-v2-ch10"),
        ("HMM state models", "decoding", "parameter learning and profile HMMs"),
        "pending",
        "Source scope is mapped; focused source comparison remains pending.",
    ),
    ModuleSourceAudit(
        "dm847.m06",
        ("sdu-dm847-active-2025", "compeau-pevzner-v2-ch09"),
        ("suffix structures", "BWT and backward search", "memory-aware read mapping"),
        "pending",
        "Source scope is mapped; focused source comparison remains pending.",
    ),
    ModuleSourceAudit(
        "dm847.m07",
        ("sdu-dm847-active-2025",),
        ("bacterial genetics", "operon prediction", "integration of genomic evidence"),
        "pending",
        (
            "The active course scope is mapped. A specialized bacterial-genetics and "
            "operon-prediction source review remains pending."
        ),
    ),
    ModuleSourceAudit(
        "dm847.m08",
        (
            "sdu-dm847-active-2025",
            "compeau-pevzner-v1-ch02",
            "compeau-pevzner-v2-ch08",
        ),
        ("motif profiles and entropy", "EM and soft assignments", "independent validation"),
        "pending",
        "Source scope is mapped; focused source comparison remains pending.",
    ),
    ModuleSourceAudit(
        "dm847.m09",
        ("sdu-dm847-active-2025", "compeau-pevzner-v2-ch11"),
        ("biological networks", "network enrichment", "null models and propagation"),
        "pending",
        "Source scope is mapped; focused source comparison remains pending.",
    ),
    ModuleSourceAudit(
        "dm847.m10",
        ("sdu-dm847-active-2025", "compeau-pevzner-v2-ch08"),
        (
            "supervised and unsupervised OMICS learning",
            "clustering objectives and validation",
            "integrative computational project reasoning",
        ),
        "pending",
        "Source scope is mapped; focused source comparison remains pending.",
    ),
)


def _with_source_basis(
    module: LocalizedLearningModule,
    source_ids: tuple[str, ...],
) -> LocalizedLearningModule:
    tutor = module.tutor_support
    merged = tuple(dict.fromkeys((*tutor.source_basis, *source_ids)))
    updated_tutor: LocalizedTutorSupportPacket = replace(tutor, source_basis=merged)
    return replace(module, tutor_support=updated_tutor)


def _extend_sequence_matching(module: LocalizedLearningModule) -> LocalizedLearningModule:
    extended = replace(
        module,
        objectives=module.objectives
        + (
            objective(
                "m03.bg.o1",
                (
                    "Implementar coincidencia aproximada con distancia de Hamming y distinguirla del alineamiento con inserciones o deleciones.",
                    "Implement approximate matching with Hamming distance and distinguish it from alignment with insertions or deletions.",
                    "Implementere approksimativ matching med Hamming-afstand og skelne den fra alignment med insertioner eller deletioner.",
                ),
            ),
        ),
        concepts=module.concepts
        + (
            concept(
                "approximate-pattern-matching-and-neighborhoods",
                (
                    "Coincidencia aproximada y vecindarios de patrones",
                    "Approximate pattern matching and pattern neighborhoods",
                    "Approksimativ mønstermatching og mønsternabolag",
                ),
                (
                    "La búsqueda exacta acepta una ventana sólo cuando todos sus símbolos coinciden. La distancia de Hamming cuenta posiciones diferentes entre cadenas de igual longitud y permite definir una coincidencia aproximada cuando la distancia es como máximo d. El d-vecindario de un patrón contiene todas las cadenas que cumplen ese límite; su tamaño crece rápidamente con la longitud, el alfabeto y d, por lo que enumerarlo no siempre es la estrategia adecuada. d=0 recupera la búsqueda exacta. Hamming no modela inserciones ni deleciones porque compara posiciones alineadas una a una; cuando los gaps forman parte de la pregunta se necesita un algoritmo de alineamiento. Si ambas hebras son relevantes, patrón y complemento inverso deben incorporarse mediante una política explícita para evitar dobles conteos.",
                    "Exact search accepts a window only when every symbol matches. Hamming distance counts differing positions between equal-length strings and defines an approximate match when distance is at most d. The d-neighborhood of a pattern contains every string within that limit; its size grows rapidly with pattern length, alphabet size, and d, so explicit enumeration is not always appropriate. Setting d=0 recovers exact search. Hamming distance does not model insertions or deletions because it compares aligned positions one by one; questions involving gaps require an alignment algorithm. When both strands matter, the pattern and reverse complement need an explicit policy to avoid double counting.",
                    "Eksakt søgning accepterer kun et vindue, når alle symboler matcher. Hamming-afstand tæller forskellige positioner mellem strenge med samme længde og definerer et approksimativt match, når afstanden højst er d. Et mønsters d-nabolag indeholder alle strenge inden for grænsen; størrelsen vokser hurtigt med mønsterlængde, alfabet og d, så eksplicit enumeration er ikke altid passende. d=0 giver eksakt søgning. Hamming-afstand modellerer ikke insertioner eller deletioner, fordi positioner sammenlignes én til én; spørgsmål med gaps kræver en alignment-algoritme. Når begge strenge er relevante, kræver mønster og omvendt komplement en eksplicit politik for at undgå dobbeltoptælling.",
                ),
                (
                    (
                        "Hamming requiere cadenas de igual longitud.",
                        "Hamming distance requires equal-length strings.",
                        "Hamming-afstand kræver strenge med samme længde.",
                    ),
                    (
                        "d=0 equivale a coincidencia exacta.",
                        "d=0 is equivalent to exact matching.",
                        "d=0 svarer til eksakt matching.",
                    ),
                    (
                        "Un mismatch sustituye un símbolo; no abre un gap.",
                        "A mismatch substitutes a symbol; it does not open a gap.",
                        "Et mismatch substituerer et symbol; det åbner ikke et gap.",
                    ),
                    (
                        "La política de hebras debe evitar contar dos veces una coincidencia palindrómica.",
                        "The strand policy should avoid counting a palindromic match twice.",
                        "Strengpolitikken bør undgå at tælle et palindromisk match to gange.",
                    ),
                ),
            ),
        ),
        worked_examples=module.worked_examples
        + (
            example(
                "m03.bg.e01",
                (
                    "Localizar coincidencias con un mismatch",
                    "Locate matches with one mismatch",
                    "Find matches med ét mismatch",
                ),
                (
                    "Busca un patrón en todas las ventanas del texto y conserva las posiciones cuya distancia de Hamming no supera uno.",
                    "Search every text window and retain positions whose Hamming distance is at most one.",
                    "Søg i alle tekstvinduer og behold positioner, hvis Hamming-afstanden højst er én.",
                ),
                (
                    (
                        "Cada ventana tiene la misma longitud que el patrón.",
                        "Every window has the same length as the pattern.",
                        "Hvert vindue har samme længde som mønstret.",
                    ),
                    (
                        "La comparación se detiene conceptualmente al superar d.",
                        "The comparison can conceptually stop after exceeding d.",
                        "Sammenligningen kan principielt stoppe, når d overskrides.",
                    ),
                    (
                        "Las posiciones devueltas son 0-based.",
                        "Returned positions are zero-based.",
                        "De returnerede positioner er nulbaserede.",
                    ),
                ),
                "def hamming(left: str, right: str) -> int:\n"
                "    if len(left) != len(right):\n"
                "        raise ValueError('equal lengths required')\n"
                "    return sum(a != b for a, b in zip(left, right, strict=True))\n"
                "\n"
                "\n"
                "def approximate_positions(text: str, pattern: str, d: int) -> list[int]:\n"
                "    if d < 0:\n"
                "        raise ValueError('d must be non-negative')\n"
                "    width = len(pattern)\n"
                "    return [\n"
                "        start\n"
                "        for start in range(len(text) - width + 1)\n"
                "        if hamming(text[start : start + width], pattern) <= d\n"
                "    ]\n"
                "\n"
                "\n"
                "print(approximate_positions('ACGTTACGTA', 'ACGTA', 1))",
                "[0, 5]",
                (
                    "La posición 0 contiene un mismatch y la posición 5 es exacta. El procedimiento no permite gaps y no afirma significación biológica.",
                    "Position 0 contains one mismatch and position 5 is exact. The procedure allows no gaps and makes no claim of biological significance.",
                    "Position 0 indeholder ét mismatch, og position 5 er eksakt. Proceduren tillader ingen gaps og hævder ikke biologisk signifikans.",
                ),
            ),
        ),
        practice_exercises=module.practice_exercises
        + (
            practice(
                "m03.bg.p01",
                ActivityType.DEBUGGING,
                (
                    "Una función de búsqueda aproximada usa zip(window, pattern) sin comprobar longitudes y acepta d=-1. Explica los fallos y define el contrato corregido.",
                    "An approximate-search function uses zip(window, pattern) without checking lengths and accepts d=-1. Explain the failures and define the corrected contract.",
                    "En funktion til approksimativ søgning bruger zip(window, pattern) uden længdekontrol og accepterer d=-1. Forklar fejlene og definér den korrigerede kontrakt.",
                ),
                (
                    (
                        "zip puede ocultar una cola no comparada.",
                        "zip can hide an uncompared suffix.",
                        "zip kan skjule en ikke-sammenlignet hale.",
                    ),
                    (
                        "La tolerancia representa un número de diferencias permitido.",
                        "Tolerance represents an allowed number of differences.",
                        "Tolerancen repræsenterer et tilladt antal forskelle.",
                    ),
                ),
                (
                    "Exigir d >= 0; comparar sólo ventanas completas de longitud len(pattern); hacer que Hamming rechace longitudes diferentes; devolver posiciones con distancia <= d; definir por separado si se busca también el complemento inverso. Una ventana parcial nunca debe aceptarse por truncamiento de zip.",
                    "Require d >= 0; compare only complete windows of length len(pattern); make Hamming distance reject unequal lengths; return positions with distance <= d; define separately whether the reverse complement is also searched. A partial window must never be accepted because zip truncated it.",
                    "Kræv d >= 0; sammenlign kun komplette vinduer med længden len(pattern); lad Hamming-afstand afvise forskellige længder; returnér positioner med afstand <= d; definér separat om omvendt komplement også søges. Et delvist vindue må aldrig accepteres, fordi zip afkortede sammenligningen.",
                ),
                (
                    "El contrato separa validación de entrada, definición de distancia, política de hebras y semántica de salida.",
                    "The contract separates input validation, distance definition, strand policy, and output semantics.",
                    "Kontrakten adskiller inputvalidering, afstandsdefinition, strengpolitik og outputsemantik.",
                ),
            ),
        ),
        assessment_items=module.assessment_items
        + (
            objective_mcq(
                "dm847.m03.book.001",
                (
                    "¿Qué afirmación describe correctamente la distancia de Hamming?",
                    "Which statement correctly describes Hamming distance?",
                    "Hvilket udsagn beskriver Hamming-afstand korrekt?",
                ),
                (
                    (
                        "equal_length",
                        (
                            "Cuenta sustituciones posicionales entre cadenas de igual longitud.",
                            "It counts positional substitutions between equal-length strings.",
                            "Den tæller positionssubstitutioner mellem strenge med samme længde.",
                        ),
                    ),
                    (
                        "gaps",
                        (
                            "Encuentra automáticamente la mejor colocación de gaps.",
                            "It automatically finds the best placement of gaps.",
                            "Den finder automatisk den bedste placering af gaps.",
                        ),
                    ),
                    (
                        "significance",
                        (
                            "Demuestra que una coincidencia es estadísticamente significativa.",
                            "It proves that a match is statistically significant.",
                            "Den beviser, at et match er statistisk signifikant.",
                        ),
                    ),
                ),
                "equal_length",
                (
                    "Hamming compara posiciones ya enfrentadas y no modela inserciones, deleciones ni significación.",
                    "Hamming compares already paired positions and models neither insertions, deletions, nor significance.",
                    "Hamming sammenligner allerede parrede positioner og modellerer hverken insertioner, deletioner eller signifikans.",
                ),
            ),
        ),
    )
    return _with_source_basis(
        extended,
        (
            "sdu-dm847-active-2025",
            "compeau-pevzner-v1-ch01",
            "compeau-pevzner-v1-ch05",
        ),
    )


def _extend_pairwise_alignment(module: LocalizedLearningModule) -> LocalizedLearningModule:
    extended = replace(
        module,
        objectives=module.objectives
        + (
            objective(
                "m04.bg.o1",
                (
                    "Reducir la memoria del cálculo de score a una fila y explicar por qué esa reducción no conserva por sí sola el traceback.",
                    "Reduce score computation memory to one row and explain why that reduction alone does not preserve traceback.",
                    "Reducere hukommelsen til scoreberegning til én række og forklare, hvorfor reduktionen ikke i sig selv bevarer traceback.",
                ),
            ),
        ),
        concepts=module.concepts
        + (
            concept(
                "linear-space-scoring-and-traceback-boundary",
                (
                    "Score con memoria lineal y límite del traceback",
                    "Linear-memory scoring and the traceback boundary",
                    "Score med lineær hukommelse og traceback-grænsen",
                ),
                (
                    "Para calcular la siguiente fila de una matriz de alineamiento global sólo se necesitan la fila anterior y el prefijo ya calculado de la fila actual. Por ello, si sólo se solicita el score óptimo, las filas antiguas pueden descartarse y la memoria baja de O(nm) a O(min(n,m)), manteniendo O(nm) tiempo. Esta optimización cambia el contrato del resultado: la última fila conserva el score, pero no todos los predecesores necesarios para reconstruir un alineamiento. Un traceback directo suele almacenar la matriz o sus punteros, mientras un algoritmo divide y vencerás puede reconstruir mediante nodos o aristas centrales con memoria lineal y trabajo adicional. Debe declararse si la función devuelve sólo score, un alineamiento, todos los óptimos o uno de ellos.",
                    "To compute the next row of a global-alignment matrix, only the previous row and the computed prefix of the current row are needed. Therefore, when only the optimal score is requested, older rows can be discarded and memory falls from O(nm) to O(min(n,m)) while time remains O(nm). This optimization changes the result contract: the final row preserves the score but not all predecessors required to reconstruct an alignment. Direct traceback commonly stores the matrix or its pointers, whereas a divide-and-conquer algorithm can reconstruct through middle nodes or edges with linear memory and additional work. The function must state whether it returns only a score, one alignment, all optima, or one arbitrary optimum.",
                    "For at beregne næste række i en global alignment-matrix kræves kun den foregående række og det beregnede præfiks af den aktuelle række. Hvis kun den optimale score ønskes, kan ældre rækker derfor kasseres, og hukommelsen falder fra O(nm) til O(min(n,m)), mens tiden forbliver O(nm). Optimeringen ændrer resultatkontrakten: den sidste række bevarer scoren, men ikke alle forgængere, der kræves for at rekonstruere en alignment. Direkte traceback gemmer normalt matricen eller dens pointere, mens en divide-and-conquer-algoritme kan rekonstruere gennem midterknuder eller -kanter med lineær hukommelse og ekstra arbejde. Funktionen skal angive, om den returnerer kun score, én alignment, alle optima eller ét vilkårligt optimum.",
                ),
                (
                    (
                        "Score-only puede usar O(min(n,m)) memoria.",
                        "Score-only computation can use O(min(n,m)) memory.",
                        "Score-only-beregning kan bruge O(min(n,m)) hukommelse.",
                    ),
                    (
                        "El tiempo básico sigue siendo O(nm).",
                        "Basic running time remains O(nm).",
                        "Den grundlæggende køretid forbliver O(nm).",
                    ),
                    (
                        "La última fila no contiene un traceback completo.",
                        "The final row does not contain a complete traceback.",
                        "Den sidste række indeholder ikke et komplet traceback.",
                    ),
                    (
                        "Memoria y tipo de salida deben formar parte del contrato.",
                        "Memory and output type should be part of the contract.",
                        "Hukommelse og outputtype bør være en del af kontrakten.",
                    ),
                ),
            ),
        ),
        worked_examples=module.worked_examples
        + (
            example(
                "m04.bg.e01",
                (
                    "Score global con una fila móvil",
                    "Global score with a rolling row",
                    "Global score med en rullende række",
                ),
                (
                    "Calcula el score global con match=1, mismatch=-1 y gap=-1, colocando la secuencia más corta en las columnas.",
                    "Compute the global score with match=1, mismatch=-1, and gap=-1, placing the shorter sequence in the columns.",
                    "Beregn den globale score med match=1, mismatch=-1 og gap=-1, hvor den korteste sekvens placeres i kolonnerne.",
                ),
                (
                    (
                        "La fila anterior inicializa los gaps contra el prefijo vacío.",
                        "The previous row initializes gaps against the empty prefix.",
                        "Den foregående række initialiserer gaps mod det tomme præfiks.",
                    ),
                    (
                        "Cada celda usa diagonal previa, celda superior y celda izquierda actual.",
                        "Each cell uses the previous diagonal, upper cell, and current left cell.",
                        "Hver celle bruger den foregående diagonal, den øvre celle og den aktuelle venstre celle.",
                    ),
                    (
                        "Sólo se conserva len(shorter)+1 valores al terminar cada fila.",
                        "Only len(shorter)+1 values are retained after each row.",
                        "Kun len(shorter)+1 værdier bevares efter hver række.",
                    ),
                ),
                "def global_score_linear(a: str, b: str) -> tuple[int, int]:\n"
                "    if len(b) > len(a):\n"
                "        a, b = b, a\n"
                "    previous = [-column for column in range(len(b) + 1)]\n"
                "    for row, left in enumerate(a, start=1):\n"
                "        current = [-row]\n"
                "        for column, right in enumerate(b, start=1):\n"
                "            substitution = 1 if left == right else -1\n"
                "            current.append(\n"
                "                max(\n"
                "                    previous[column - 1] + substitution,\n"
                "                    previous[column] - 1,\n"
                "                    current[column - 1] - 1,\n"
                "                )\n"
                "            )\n"
                "        previous = current\n"
                "    return previous[-1], len(previous)\n"
                "\n"
                "\n"
                "print(global_score_linear('ACG', 'AG'))",
                "(1, 3)",
                (
                    "El primer valor es el score óptimo y el segundo muestra tres celdas activas para la secuencia corta de longitud dos. La función no devuelve un alineamiento porque descartó los predecesores.",
                    "The first value is the optimal score and the second shows three active cells for the shorter sequence of length two. The function returns no alignment because predecessor information was discarded.",
                    "Den første værdi er den optimale score, og den anden viser tre aktive celler for den kortere sekvens med længde to. Funktionen returnerer ingen alignment, fordi forgængerinformationen blev kasseret.",
                ),
            ),
        ),
        practice_exercises=module.practice_exercises
        + (
            practice(
                "m04.bg.p01",
                ActivityType.PIPELINE_DESIGN,
                (
                    "Debes comparar dos secuencias largas. Primero necesitas sólo el score para filtrar candidatos; después debes reconstruir un alineamiento para los candidatos retenidos. Diseña la estrategia de memoria y salida para ambas etapas.",
                    "You must compare two long sequences. First you need only the score to filter candidates; then you must reconstruct an alignment for retained candidates. Design the memory and output strategy for both stages.",
                    "Du skal sammenligne to lange sekvenser. Først kræves kun scoren til filtrering af kandidater; derefter skal en alignment rekonstrueres for de bevarede kandidater. Design hukommelses- og outputstrategien for begge trin.",
                ),
                (
                    (
                        "No almacenes punteros cuando la primera etapa no los consume.",
                        "Do not store pointers when the first stage does not consume them.",
                        "Gem ikke pointere, når første trin ikke bruger dem.",
                    ),
                    (
                        "La segunda etapa necesita una estrategia explícita de reconstrucción.",
                        "The second stage needs an explicit reconstruction strategy.",
                        "Andet trin kræver en eksplicit rekonstruktionsstrategi.",
                    ),
                ),
                (
                    "Etapa 1: usar filas móviles con la secuencia corta en columnas, devolver sólo score y registrar parámetros; coste O(nm) tiempo y O(min(n,m)) memoria. Etapa 2: para candidatos retenidos, usar matriz y punteros si el tamaño lo permite o una reconstrucción divide y vencerás por nodo/arista central si la memoria es el límite. Validar que al retirar gaps se recuperan las entradas y que el score reconstruido coincide con el score óptimo.",
                    "Stage 1: use rolling rows with the shorter sequence in columns, return only the score, and record parameters; cost O(nm) time and O(min(n,m)) memory. Stage 2: for retained candidates, use a matrix and pointers when size permits or divide-and-conquer reconstruction through a middle node/edge when memory is limiting. Validate that removing gaps recovers the inputs and that the reconstructed score equals the optimum.",
                    "Trin 1: brug rullende rækker med den kortere sekvens i kolonner, returnér kun scoren og registrér parametre; O(nm) tid og O(min(n,m)) hukommelse. Trin 2: brug matrix og pointere for bevarede kandidater, når størrelsen tillader det, eller divide-and-conquer-rekonstruktion gennem en midterknude/-kant, når hukommelsen er begrænsningen. Validér at fjernelse af gaps genskaber input, og at den rekonstruerede score svarer til optimum.",
                ),
                (
                    "Diseño separa un filtro score-only de una operación que promete un alineamiento verificable.",
                    "The design separates a score-only filter from an operation that promises a verifiable alignment.",
                    "Designet adskiller et score-only-filter fra en operation, der lover en verificerbar alignment.",
                ),
            ),
        ),
        assessment_items=module.assessment_items
        + (
            objective_mcq(
                "dm847.m04.book.001",
                (
                    "¿Qué se pierde al conservar sólo la última fila de la programación dinámica?",
                    "What is lost when only the final dynamic-programming row is retained?",
                    "Hvad går tabt, når kun den sidste række i dynamisk programmering bevares?",
                ),
                (
                    (
                        "traceback",
                        (
                            "Los predecesores necesarios para un traceback directo completo.",
                            "The predecessors needed for a complete direct traceback.",
                            "De forgængere, der kræves til et komplet direkte traceback.",
                        ),
                    ),
                    (
                        "score",
                        (
                            "El score óptimo final.",
                            "The final optimal score.",
                            "Den endelige optimale score.",
                        ),
                    ),
                    (
                        "time",
                        (
                            "La necesidad de calcular O(nm) transiciones.",
                            "The need to compute O(nm) transitions.",
                            "Behovet for at beregne O(nm) overgange.",
                        ),
                    ),
                ),
                "traceback",
                (
                    "Las filas móviles conservan el score, pero descartan la historia de decisiones necesaria para reconstruir directamente el camino.",
                    "Rolling rows retain the score but discard the decision history needed to reconstruct the path directly.",
                    "Rullende rækker bevarer scoren, men kasserer beslutningshistorikken, der kræves for direkte rekonstruktion af stien.",
                ),
            ),
        ),
    )
    return _with_source_basis(
        extended,
        ("sdu-dm847-active-2025", "compeau-pevzner-v1-ch05"),
    )


def apply_book_grounded_extensions(
    modules: tuple[LocalizedLearningModule, ...],
) -> tuple[LocalizedLearningModule, ...]:
    """Apply the first focused DM847 book-grounded extensions."""

    return tuple(
        _extend_sequence_matching(module)
        if module.module_id == "dm847.m03"
        else _extend_pairwise_alignment(module)
        if module.module_id == "dm847.m04"
        else module
        for module in modules
    )


__all__ = [
    "AcademicReference",
    "DM847_BOOK_SOURCES",
    "DM847_MODULE_SOURCE_AUDIT",
    "ModuleSourceAudit",
    "VerificationState",
    "apply_book_grounded_extensions",
]
