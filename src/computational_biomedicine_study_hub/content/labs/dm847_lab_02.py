"""DM847 laboratory 2: global and local pairwise alignment."""

from __future__ import annotations

from ...i18n.locales import AppLocale
from ...learning.computational_labs import (
    ComputationalLab,
    LabStage,
    LabTask,
    LabTaskKind,
    LocalizedText,
)


def _text(es: str, en: str, da: str) -> LocalizedText:
    return LocalizedText(
        {
            AppLocale.SPANISH_SPAIN: es,
            AppLocale.ENGLISH: en,
            AppLocale.DANISH_DENMARK: da,
        }
    )


_GLOBAL_STARTER = '''def needleman_wunsch_score(
    sequence_a,
    sequence_b,
    match=2,
    mismatch=-1,
    gap=-2,
):
    """Return the optimal global-alignment score."""
    # Define the state, initialization, and recurrence before coding.
    raise NotImplementedError
'''

_GLOBAL_CHECKS = """
assert needleman_wunsch_score("", "") == 0
assert needleman_wunsch_score("A", "") == -2
assert needleman_wunsch_score("", "AC") == -4
print(needleman_wunsch_score("ACG", "AG"))
print(needleman_wunsch_score("ACGT", "ACCT"))
"""

_TRACEBACK_STARTER = '''def normalize_sequence(sequence):
    """Return uppercase DNA without whitespace; reject invalid symbols."""
    raise NotImplementedError


def needleman_wunsch(sequence_a, sequence_b, match=2, mismatch=-1, gap=-2):
    """Return (score, aligned_a, aligned_b) with deterministic traceback."""
    raise NotImplementedError


def smith_waterman(sequence_a, sequence_b, match=2, mismatch=-1, gap=-2):
    """Return score, aligned strings, and half-open coordinates in both inputs."""
    raise NotImplementedError
'''

_TRACEBACK_CHECKS = """
assert needleman_wunsch("", "") == (0, "", "")
assert needleman_wunsch("A", "") == (-2, "A", "-")
assert needleman_wunsch("", "A") == (-2, "-", "A")
assert smith_waterman("AAAA", "TTTT")[0] == 0
print(needleman_wunsch("ACG", "AG"))
print(smith_waterman("TTACG", "ACGAA"))
"""


DM847_LAB_02 = ComputationalLab(
    lab_id="dm847.lab02.pairwise-alignment",
    course_code="DM847",
    version="1.0.0",
    title=_text(
        "Laboratorio 2: alineamiento global y local",
        "Laboratory 2: global and local alignment",
        "Laboratorium 2: global og lokal alignment",
    ),
    research_question=_text(
        "¿Cómo cambia la correspondencia óptima entre dos secuencias cuando modificamos el objetivo de alineamiento y la función de puntuación?",
        "How does the optimal correspondence between two sequences change when the alignment objective and scoring function change?",
        "Hvordan ændres den optimale korrespondance mellem to sekvenser, når alignmentmålet og scoringsfunktionen ændres?",
    ),
    disclaimer=_text(
        "Preparación interna basada en los resultados de aprendizaje de DM847. No reproduce una hoja oficial de laboratorio de SDU.",
        "Internal preparation based on DM847 learning outcomes. It does not reproduce an official SDU laboratory sheet.",
        "Intern forberedelse baseret på læringsmålene i DM847. Den gengiver ikke et officielt SDU-laboratorieark.",
    ),
    data_provenance=_text(
        "Las secuencias son sintéticas y se diseñaron para enseñar programación dinámica. No representan pacientes, genes clínicos ni evidencia de homología real.",
        "The sequences are synthetic and were designed to teach dynamic programming. They do not represent patients, clinical genes, or evidence of real homology.",
        "Sekvenserne er syntetiske og designet til at undervise i dynamisk programmering. De repræsenterer ikke patienter, kliniske gener eller evidens for reel homologi.",
    ),
    objectives=(
        (
            "dm847.lab02.objective",
            _text(
                "Distinguir qué pregunta responden el alineamiento global, local y semiglobal.",
                "Distinguish the questions answered by global, local, and semiglobal alignment.",
                "Skelne mellem de spørgsmål, som global, lokal og semiglobal alignment besvarer.",
            ),
        ),
        (
            "dm847.lab02.recurrence",
            _text(
                "Derivar e implementar las recurrencias de Needleman–Wunsch y Smith–Waterman.",
                "Derive and implement the Needleman–Wunsch and Smith–Waterman recurrences.",
                "Udlede og implementere Needleman–Wunsch- og Smith–Waterman-rekurrenserne.",
            ),
        ),
        (
            "dm847.lab02.traceback",
            _text(
                "Reconstruir alineamientos mediante traceback determinista y validar sus invariantes.",
                "Reconstruct alignments with deterministic traceback and validate their invariants.",
                "Rekonstruere alignments med deterministisk traceback og validere deres invarianter.",
            ),
        ),
        (
            "dm847.lab02.parameters",
            _text(
                "Evaluar cómo match, mismatch y gaps modifican el óptimo y su interpretación.",
                "Evaluate how match, mismatch, and gaps alter the optimum and its interpretation.",
                "Vurdere hvordan match, mismatch og gaps ændrer optimum og fortolkning.",
            ),
        ),
        (
            "dm847.lab02.complexity",
            _text(
                "Explicar complejidad O(nm), memoria y el paso de gaps lineales a afines.",
                "Explain O(nm) complexity, memory, and the transition from linear to affine gaps.",
                "Forklare O(nm)-kompleksitet, hukommelse og overgangen fra lineære til affine gaps.",
            ),
        ),
        (
            "dm847.lab02.interpretation",
            _text(
                "Separar optimalidad algorítmica, similitud de secuencia y afirmaciones biológicas.",
                "Separate algorithmic optimality, sequence similarity, and biological claims.",
                "Adskille algoritmisk optimalitet, sekvenslighed og biologiske påstande.",
            ),
        ),
    ),
    prerequisites=(
        _text(
            "Matrices, índices, bucles anidados y funciones en Python.",
            "Matrices, indices, nested loops, and functions in Python.",
            "Matricer, indeks, indlejrede løkker og funktioner i Python.",
        ),
        _text(
            "Puntuación de sustituciones y penalizaciones de gap.",
            "Substitution scores and gap penalties.",
            "Substitutionsscore og gap-straffe.",
        ),
        _text(
            "Diferencia entre coincidencia exacta, mismatch e indel.",
            "The difference between an exact match, mismatch, and indel.",
            "Forskellen mellem eksakt match, mismatch og indel.",
        ),
    ),
    tasks=(
        LabTask(
            task_id="dm847.lab02.prepare.scoring-contract",
            stage=LabStage.PREPARE,
            kind=LabTaskKind.SHORT_ANSWER,
            title=_text(
                "Contrato de puntuación",
                "Scoring contract",
                "Scoringskontrakt",
            ),
            instructions=_text(
                "Define el significado de cada celda, los valores de match, mismatch y gap, el tratamiento de secuencias vacías y una política explícita para empates de traceback.",
                "Define the meaning of each cell, match, mismatch, and gap values, treatment of empty sequences, and an explicit traceback tie policy.",
                "Definér betydningen af hver celle, værdier for match, mismatch og gap, håndtering af tomme sekvenser og en eksplicit traceback-politik ved ties.",
            ),
            mentor_notes=_text(
                "Pregunta primero qué subproblema representa F[i][j]. Después exige inicialización y consecuencias biológicas de la función de score. No proporciones la recurrencia completa de inmediato.",
                "Ask first which subproblem F[i][j] represents. Then require initialization and biological consequences of the scoring function. Do not immediately provide the full recurrence.",
                "Spørg først hvilket delproblem F[i][j] repræsenterer. Kræv derefter initialisering og biologiske konsekvenser af scoringsfunktionen. Giv ikke straks hele rekurrensen.",
            ),
            objective_ids=("dm847.lab02.objective", "dm847.lab02.parameters"),
            estimated_minutes=15,
        ),
        LabTask(
            task_id="dm847.lab02.investigate.manual-matrix",
            stage=LabStage.INVESTIGATE,
            kind=LabTaskKind.SHORT_ANSWER,
            title=_text(
                "Matriz manual",
                "Manual matrix",
                "Manuel matrix",
            ),
            instructions=_text(
                "Con match=2, mismatch=-1 y gap=-2, calcula a mano la matriz global para ACG frente a AG. Identifica las transiciones de la celda final y predice un alineamiento óptimo.",
                "With match=2, mismatch=-1, and gap=-2, manually compute the global matrix for ACG versus AG. Identify transitions into the final cell and predict one optimal alignment.",
                "Med match=2, mismatch=-1 og gap=-2 skal du manuelt beregne den globale matrix for ACG mod AG. Identificér overgangene til den sidste celle og forudsig én optimal alignment.",
            ),
            mentor_notes=_text(
                "Pide fila y columna iniciales antes de revisar celdas internas. Ante un error, localiza la primera celda inconsistente en lugar de dar la matriz completa.",
                "Request the initial row and column before reviewing internal cells. When an error appears, locate the first inconsistent cell rather than giving the full matrix.",
                "Bed om første række og kolonne før interne celler gennemgås. Ved fejl skal den første inkonsistente celle lokaliseres i stedet for at give hele matricen.",
            ),
            objective_ids=("dm847.lab02.recurrence", "dm847.lab02.traceback"),
            estimated_minutes=15,
        ),
        LabTask(
            task_id="dm847.lab02.implement.global-score",
            stage=LabStage.IMPLEMENT,
            kind=LabTaskKind.PYTHON,
            title=_text(
                "Needleman–Wunsch: score",
                "Needleman–Wunsch score",
                "Needleman–Wunsch-score",
            ),
            instructions=_text(
                "Implementa needleman_wunsch_score con memoria O(nm). Debe inicializar bordes, aplicar las tres transiciones y funcionar con secuencias vacías.",
                "Implement needleman_wunsch_score with O(nm) memory. It must initialize borders, apply all three transitions, and support empty sequences.",
                "Implementér needleman_wunsch_score med O(nm)-hukommelse. Den skal initialisere kanter, anvende alle tre overgange og understøtte tomme sekvenser.",
            ),
            mentor_notes=_text(
                "Usa preguntas sobre estado, caso base e invariante de recorrido. Ofrece pseudocódigo sólo después de que el estudiante formule la recurrencia.",
                "Use questions about state, base case, and traversal invariant. Offer pseudocode only after the learner formulates the recurrence.",
                "Brug spørgsmål om tilstand, basistilfælde og gennemløbsinvariant. Giv kun pseudokode efter at den studerende har formuleret rekurrensen.",
            ),
            objective_ids=("dm847.lab02.recurrence", "dm847.lab02.complexity"),
            estimated_minutes=35,
            starter_response=_GLOBAL_STARTER,
            verification_source=_GLOBAL_CHECKS,
            expected_output="2\n5",
        ),
        LabTask(
            task_id="dm847.lab02.check.traceback-local",
            stage=LabStage.CHECK,
            kind=LabTaskKind.PYTHON,
            title=_text(
                "Traceback global y local",
                "Global and local traceback",
                "Globalt og lokalt traceback",
            ),
            instructions=_text(
                "Implementa Needleman–Wunsch y Smith–Waterman completos. Usa prioridad diagonal, vertical y horizontal en empates. Smith–Waterman debe reiniciar en cero, comenzar en el primer máximo encontrado y devolver coordenadas half-open.",
                "Implement complete Needleman–Wunsch and Smith–Waterman. Use diagonal, vertical, then horizontal priority for ties. Smith–Waterman must reset at zero, start at the first maximum found, and return half-open coordinates.",
                "Implementér komplette Needleman–Wunsch og Smith–Waterman. Brug prioriteten diagonal, vertikal og derefter horisontal ved ties. Smith–Waterman skal nulstille ved nul, starte ved det første fundne maksimum og returnere half-open-koordinater.",
            ),
            mentor_notes=_text(
                "Cuando falle, pide verificar primero tres invariantes: igual longitud de cadenas alineadas, recuperación de entradas al retirar gaps y score recalculado. No reveles las pruebas internas.",
                "When it fails, first request three invariants: equal aligned-string length, recovery of inputs after removing gaps, and recomputed score. Do not reveal internal tests.",
                "Ved fejl skal tre invarianter først kontrolleres: samme længde af alignede strenge, gendannelse af input efter fjernelse af gaps og genberegnet score. Afslør ikke interne tests.",
            ),
            objective_ids=(
                "dm847.lab02.recurrence",
                "dm847.lab02.traceback",
                "dm847.lab02.parameters",
            ),
            estimated_minutes=35,
            starter_response=_TRACEBACK_STARTER,
            verification_source=_TRACEBACK_CHECKS,
            expected_output="(2, 'ACG', 'A-G')\n(6, 'ACG', 'ACG', (2, 5), (0, 3))",
        ),
        LabTask(
            task_id="dm847.lab02.interpret.parameter-sensitivity",
            stage=LabStage.INTERPRET,
            kind=LabTaskKind.SHORT_ANSWER,
            title=_text(
                "Sensibilidad e interpretación",
                "Sensitivity and interpretation",
                "Følsomhed og fortolkning",
            ),
            instructions=_text(
                "Compara el alineamiento de dos pares sintéticos bajo al menos dos configuraciones de puntuación. Explica qué cambia, qué permanece estable y por qué un score alto no demuestra por sí solo homología ni función compartida.",
                "Compare the alignment of two synthetic pairs under at least two scoring configurations. Explain what changes, what remains stable, and why a high score alone does not demonstrate homology or shared function.",
                "Sammenlign alignment af to syntetiske par under mindst to scoringskonfigurationer. Forklar hvad der ændres, hvad der forbliver stabilt, og hvorfor en høj score alene ikke dokumenterer homologi eller fælles funktion.",
            ),
            mentor_notes=_text(
                "Exige separar observación, supuesto y conclusión. Pregunta por modelo nulo, longitud, composición, múltiples óptimos y evidencia externa.",
                "Require separation of observation, assumption, and conclusion. Ask about the null model, length, composition, multiple optima, and external evidence.",
                "Kræv adskillelse af observation, antagelse og konklusion. Spørg til nulmodel, længde, sammensætning, flere optima og ekstern evidens.",
            ),
            objective_ids=("dm847.lab02.parameters", "dm847.lab02.interpretation"),
            estimated_minutes=20,
        ),
        LabTask(
            task_id="dm847.lab02.defend.algorithm",
            stage=LabStage.DEFEND,
            kind=LabTaskKind.SHORT_ANSWER,
            title=_text(
                "Defensa algorítmica",
                "Algorithm defence",
                "Algoritmeforsvar",
            ),
            instructions=_text(
                "Defiende la elección entre global, local y semiglobal para tres escenarios. Explica tiempo O(nm), memoria O(nm), una optimización de memoria y por qué los gaps afines requieren estados adicionales.",
                "Defend the choice among global, local, and semiglobal alignment for three scenarios. Explain O(nm) time, O(nm) memory, one memory optimization, and why affine gaps require additional states.",
                "Forsvar valget mellem global, lokal og semiglobal alignment i tre scenarier. Forklar O(nm)-tid, O(nm)-hukommelse, én hukommelsesoptimering og hvorfor affine gaps kræver yderligere tilstande.",
            ),
            mentor_notes=_text(
                "Actúa como examinador. Pide una decisión, su supuesto, una alternativa y una consecuencia. Cuestiona respuestas que confundan ahorro de memoria del score con recuperación del traceback.",
                "Act as an examiner. Request a decision, its assumption, an alternative, and a consequence. Challenge answers that confuse score-only memory reduction with traceback recovery.",
                "Opfør dig som eksaminator. Bed om en beslutning, dens antagelse, et alternativ og en konsekvens. Udfordr svar der forveksler hukommelsesreduktion for score med gendannelse af traceback.",
            ),
            objective_ids=(
                "dm847.lab02.objective",
                "dm847.lab02.complexity",
                "dm847.lab02.parameters",
            ),
            estimated_minutes=15,
        ),
        LabTask(
            task_id="dm847.lab02.consolidate.error-model",
            stage=LabStage.CONSOLIDATE,
            kind=LabTaskKind.SHORT_ANSWER,
            title=_text(
                "Reflexión y siguiente modelo",
                "Reflection and next model",
                "Refleksion og næste model",
            ),
            instructions=_text(
                "Documenta el error de implementación o razonamiento más importante, la prueba que lo detectó y la corrección. Después identifica qué parte cambiarías para soportar gaps afines o enumerar múltiples alineamientos óptimos.",
                "Document the most important implementation or reasoning error, the test that detected it, and the correction. Then identify what must change to support affine gaps or enumerate multiple optimal alignments.",
                "Dokumentér den vigtigste implementerings- eller ræsonneringsfejl, testen der fandt den, og rettelsen. Identificér derefter hvad der skal ændres for at understøtte affine gaps eller enumerere flere optimale alignments.",
            ),
            mentor_notes=_text(
                "No aceptes una reflexión genérica. Pide evidencia concreta del código, matriz, traceback o prueba y una acción verificable para el siguiente intento.",
                "Do not accept a generic reflection. Request concrete evidence from code, matrix, traceback, or test and one verifiable action for the next attempt.",
                "Accepter ikke en generisk refleksion. Bed om konkret evidens fra kode, matrix, traceback eller test og én verificerbar handling til næste forsøg.",
            ),
            objective_ids=("dm847.lab02.traceback", "dm847.lab02.complexity"),
            estimated_minutes=15,
        ),
    ),
    estimated_minutes=150,
)


__all__ = ["DM847_LAB_02"]
