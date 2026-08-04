"""DM847 laboratory 3: suffix arrays, BWT, and FM-index search."""

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


_SUFFIX_STARTER = '''def validate_terminated_text(text):
    """Return uppercase text with exactly one terminal '$'."""
    raise NotImplementedError


def suffix_array(text):
    """Return suffix starting positions in lexicographic order."""
    raise NotImplementedError


def bwt_from_suffix_array(text, suffixes):
    """Return the Burrows-Wheeler transform for a terminated text."""
    raise NotImplementedError
'''

_SUFFIX_CHECKS = """
text = validate_terminated_text("GATTACA$")
sa = suffix_array(text)
assert sorted(sa) == list(range(len(text)))
assert [text[position:] for position in sa] == sorted(text[position:] for position in sa)
print(sa)
print(bwt_from_suffix_array(text, sa))
"""

_FM_STARTER = '''def validate_terminated_text(text):
    """Return uppercase text with exactly one terminal '$'."""
    raise NotImplementedError


def suffix_array(text):
    """Return suffix starting positions in lexicographic order."""
    raise NotImplementedError


def bwt_from_suffix_array(text, suffixes):
    """Return the Burrows-Wheeler transform for a terminated text."""
    raise NotImplementedError


def build_occurrence_table(bwt):
    """Return counts-before-position for every symbol in BWT."""
    raise NotImplementedError


def build_fm_index(text):
    """Return a dictionary containing text, suffix_array, bwt, first, and occ."""
    raise NotImplementedError


def backward_search(pattern, index):
    """Return the half-open suffix-array row interval matching pattern."""
    raise NotImplementedError


def locate(pattern, index):
    """Return sorted zero-based reference positions for exact matches."""
    raise NotImplementedError
'''

_FM_CHECKS = """
index = build_fm_index("ACGTCGACG$")
assert index["suffix_array"] == suffix_array(index["text"])
assert len(index["bwt"]) == len(index["text"])
assert all(len(counts) == len(index["bwt"]) + 1 for counts in index["occ"].values())
print(backward_search("ACG", index))
print(locate("ACG", index))
print(locate("CG", index))
print(locate("TTA", index))
"""


DM847_LAB_03 = ComputationalLab(
    lab_id="dm847.lab03.sequence-indexes",
    course_code="DM847",
    version="1.0.0",
    estimated_minutes=170,
    title=_text(
        "Laboratorio 3: índices de secuencia y FM-index",
        "Laboratory 3: sequence indexes and the FM-index",
        "Laboratorium 3: sekvensindekser og FM-index",
    ),
    research_question=_text(
        "¿Cómo podemos reutilizar un índice de una referencia para contar y localizar patrones exactos sin volver a recorrer toda la secuencia en cada consulta?",
        "How can a reference index be reused to count and locate exact patterns without rescanning the entire sequence for every query?",
        "Hvordan kan et referenceindeks genbruges til at tælle og lokalisere eksakte mønstre uden at gennemløbe hele sekvensen for hver forespørgsel?",
    ),
    disclaimer=_text(
        "Preparación interna basada en los resultados de aprendizaje de DM847. No reproduce una hoja oficial de laboratorio de SDU.",
        "Internal preparation based on DM847 learning outcomes. It does not reproduce an official SDU laboratory sheet.",
        "Intern forberedelse baseret på læringsmålene i DM847. Den gengiver ikke et officielt SDU-laboratorieark.",
    ),
    data_provenance=_text(
        "La referencia y los patrones son sintéticos. Fueron diseñados para comprobar índices de texto pequeños y no representan un genoma, paciente ni resultado diagnóstico.",
        "The reference and patterns are synthetic. They were designed to verify small text indexes and do not represent a genome, patient, or diagnostic result.",
        "Referencen og mønstrene er syntetiske. De er designet til at kontrollere små tekstindekser og repræsenterer ikke et genom, en patient eller et diagnostisk resultat.",
    ),
    objectives=(
        (
            "dm847.lab03.contract",
            _text(
                "Definir el contrato del texto indexado, el centinela y las coordenadas devueltas.",
                "Define the indexed-text contract, sentinel, and returned coordinates.",
                "Definere kontrakten for den indekserede tekst, sentinel og returnerede koordinater.",
            ),
        ),
        (
            "dm847.lab03.suffix-array",
            _text(
                "Construir y validar un suffix array y un LCP conceptual para una referencia pequeña.",
                "Construct and validate a suffix array and conceptual LCP for a small reference.",
                "Konstruere og validere et suffix array og konceptuelt LCP for en lille reference.",
            ),
        ),
        (
            "dm847.lab03.bwt",
            _text(
                "Derivar la BWT desde el orden de sufijos y explicar el papel del centinela.",
                "Derive the BWT from suffix order and explain the role of the sentinel.",
                "Udlede BWT fra suffixrækkefølgen og forklare sentinelens rolle.",
            ),
        ),
        (
            "dm847.lab03.fm-index",
            _text(
                "Implementar C, Occ y backward search con intervalos half-open.",
                "Implement C, Occ, and backward search with half-open intervals.",
                "Implementere C, Occ og backward search med half-open-intervaller.",
            ),
        ),
        (
            "dm847.lab03.locate",
            _text(
                "Distinguir count de locate y recuperar posiciones mediante filas del suffix array.",
                "Distinguish count from locate and recover positions through suffix-array rows.",
                "Skelne count fra locate og gendanne positioner gennem suffix-array-rækker.",
            ),
        ),
        (
            "dm847.lab03.complexity",
            _text(
                "Comparar construcción, memoria y consultas con la búsqueda exhaustiva.",
                "Compare construction, memory, and queries with exhaustive search.",
                "Sammenligne konstruktion, hukommelse og forespørgsler med udtømmende søgning.",
            ),
        ),
        (
            "dm847.lab03.interpretation",
            _text(
                "Interpretar multimapping y límites del matching exacto sin sobreafirmar origen biológico.",
                "Interpret multimapping and exact-matching limits without overstating biological origin.",
                "Fortolke multimapping og grænser for eksakt matching uden at overdrive biologisk oprindelse.",
            ),
        ),
    ),
    prerequisites=(
        _text(
            "Orden lexicográfico, slicing, diccionarios y tuplas en Python.",
            "Lexicographic order, slicing, dictionaries, and tuples in Python.",
            "Leksikografisk orden, slicing, dictionaries og tuples i Python.",
        ),
        _text(
            "Búsqueda exacta y clasificación de lecturas del Laboratorio 1.",
            "Exact search and read classification from Laboratory 1.",
            "Eksakt søgning og read-klassifikation fra Laboratorium 1.",
        ),
        _text(
            "Intervalos half-open y coordenadas de secuencia de base cero.",
            "Half-open intervals and zero-based sequence coordinates.",
            "Half-open-intervaller og nulbaserede sekvenskoordinater.",
        ),
    ),
    tasks=(
        LabTask(
            task_id="dm847.lab03.prepare.index-contract",
            stage=LabStage.PREPARE,
            kind=LabTaskKind.SHORT_ANSWER,
            title=_text("Contrato del índice", "Index contract", "Indekskontrakt"),
            instructions=_text(
                "Define alfabeto, normalización, centinela, coordenadas, tratamiento del patrón vacío y diferencia entre una coincidencia exacta y una inferencia biológica.",
                "Define the alphabet, normalization, sentinel, coordinates, empty-pattern treatment, and difference between an exact match and a biological inference.",
                "Definér alfabet, normalisering, sentinel, koordinater, håndtering af tomt mønster og forskellen mellem et eksakt match og en biologisk inferens.",
            ),
            mentor_notes=_text(
                "Pregunta por qué el centinela debe ser único y lexicográficamente mínimo. Exige una decisión explícita sobre el patrón vacío antes de hablar de implementación.",
                "Ask why the sentinel must be unique and lexicographically smallest. Require an explicit empty-pattern decision before discussing implementation.",
                "Spørg hvorfor sentinelen skal være unik og leksikografisk mindst. Kræv en eksplicit beslutning om tomt mønster før implementering diskuteres.",
            ),
            objective_ids=("dm847.lab03.contract", "dm847.lab03.interpretation"),
            estimated_minutes=15,
        ),
        LabTask(
            task_id="dm847.lab03.investigate.manual-suffixes",
            stage=LabStage.INVESTIGATE,
            kind=LabTaskKind.SHORT_ANSWER,
            title=_text(
                "Sufijos, SA y BWT a mano",
                "Manual suffixes, SA, and BWT",
                "Manuelle suffixer, SA og BWT",
            ),
            instructions=_text(
                "Para GATTACA$, enumera todos los sufijos, ordénalos, deriva SA=[7,6,4,1,5,0,3,2], calcula el LCP entre filas adyacentes y deriva la BWT. Explica qué conserva y qué reordena la transformación.",
                "For GATTACA$, enumerate and sort all suffixes, derive SA=[7,6,4,1,5,0,3,2], calculate adjacent-row LCP values, and derive the BWT. Explain what the transform preserves and reorders.",
                "For GATTACA$ skal du opstille og sortere alle suffixer, udlede SA=[7,6,4,1,5,0,3,2], beregne LCP mellem naborækker og udlede BWT. Forklar hvad transformationen bevarer og omordner.",
            ),
            mentor_notes=_text(
                "No entregues la tabla completa. Revisa primero el orden de $, A, C, G y T; después localiza el primer par de sufijos mal ordenado.",
                "Do not provide the complete table. First review the order of $, A, C, G, and T; then locate the first incorrectly ordered suffix pair.",
                "Giv ikke hele tabellen. Gennemgå først rækkefølgen $, A, C, G og T; lokalisér derefter det første forkert ordnede suffixpar.",
            ),
            objective_ids=("dm847.lab03.suffix-array", "dm847.lab03.bwt"),
            estimated_minutes=20,
        ),
        LabTask(
            task_id="dm847.lab03.implement.suffix-bwt",
            stage=LabStage.IMPLEMENT,
            kind=LabTaskKind.PYTHON,
            title=_text(
                "Construir suffix array y BWT",
                "Build the suffix array and BWT",
                "Byg suffix array og BWT",
            ),
            instructions=_text(
                "Implementa validación del texto terminado, un suffix array pedagógico y la BWT derivada del SA. Prioriza claridad y contratos; esta versión puede ordenar sufijos completos.",
                "Implement terminated-text validation, a pedagogical suffix array, and BWT derived from the SA. Prioritize clarity and contracts; this version may sort complete suffixes.",
                "Implementér validering af termineret tekst, et pædagogisk suffix array og BWT udledt fra SA. Prioritér klarhed og kontrakter; denne version må sortere hele suffixer.",
            ),
            mentor_notes=_text(
                "Pregunta qué propiedad debe cumplir una permutación válida del SA y cómo comprobar orden sin conocer la respuesta exacta. No optimices prematuramente.",
                "Ask which property a valid SA permutation must satisfy and how to check order without knowing the exact answer. Do not optimize prematurely.",
                "Spørg hvilken egenskab en gyldig SA-permutation skal opfylde, og hvordan orden kan kontrolleres uden at kende det præcise svar. Optimér ikke for tidligt.",
            ),
            objective_ids=(
                "dm847.lab03.contract",
                "dm847.lab03.suffix-array",
                "dm847.lab03.bwt",
            ),
            estimated_minutes=30,
            starter_response=_SUFFIX_STARTER,
            verification_source=_SUFFIX_CHECKS,
            expected_output="[7, 6, 4, 1, 5, 0, 3, 2]\nACTGA$TA",
        ),
        LabTask(
            task_id="dm847.lab03.check.fm-search",
            stage=LabStage.CHECK,
            kind=LabTaskKind.PYTHON,
            title=_text(
                "Backward search y locate",
                "Backward search and locate",
                "Backward search og locate",
            ),
            instructions=_text(
                "Construye first occurrence y Occ como conteos antes de cada posición. Implementa backward_search con intervalo [top,bottom) y locate usando las filas correspondientes del SA. Rechaza patrones vacíos, símbolos fuera del alfabeto y '$' en la consulta.",
                "Build first occurrence and Occ as counts before each position. Implement backward_search with interval [top,bottom) and locate through corresponding SA rows. Reject empty patterns, symbols outside the alphabet, and '$' in the query.",
                "Byg first occurrence og Occ som tællinger før hver position. Implementér backward_search med intervallet [top,bottom) og locate gennem de tilsvarende SA-rækker. Afvis tomme mønstre, symboler uden for alfabetet og '$' i forespørgslen.",
            ),
            mentor_notes=_text(
                "Haz que el estudiante trace una iteración desde el último símbolo. Verifica el significado de Occ(c,k) y los límites half-open antes de sugerir fórmulas.",
                "Have the learner trace one iteration from the final symbol. Verify the meaning of Occ(c,k) and half-open boundaries before suggesting formulas.",
                "Lad den studerende følge én iteration fra det sidste symbol. Kontrollér betydningen af Occ(c,k) og half-open-grænser før formler foreslås.",
            ),
            objective_ids=(
                "dm847.lab03.fm-index",
                "dm847.lab03.locate",
                "dm847.lab03.complexity",
            ),
            estimated_minutes=45,
            starter_response=_FM_STARTER,
            verification_source=_FM_CHECKS,
            expected_output="(1, 3)\n[0, 6]\n[1, 4, 7]\n[]",
        ),
        LabTask(
            task_id="dm847.lab03.interpret.multimapping",
            stage=LabStage.INTERPRET,
            kind=LabTaskKind.SHORT_ANSWER,
            title=_text(
                "Count, locate y multimapping",
                "Count, locate, and multimapping",
                "Count, locate og multimapping",
            ),
            instructions=_text(
                "Compara ACG, CG y TTA en la referencia sintética. Explica qué demuestra el tamaño del intervalo, por qué count puede resolverse sin posiciones y por qué múltiples posiciones no identifican el origen verdadero de una lectura.",
                "Compare ACG, CG, and TTA in the synthetic reference. Explain what interval size establishes, why count can be answered without positions, and why multiple positions do not identify the true origin of a read.",
                "Sammenlign ACG, CG og TTA i den syntetiske reference. Forklar hvad intervalstørrelsen viser, hvorfor count kan besvares uden positioner, og hvorfor flere positioner ikke identificerer et reads sande oprindelse.",
            ),
            mentor_notes=_text(
                "Exige separar resultado del índice, decisión del mapper e inferencia biológica. Pregunta qué cambiaría con hebra reversa, mismatches, indels o referencia incompleta.",
                "Require separation of index result, mapper decision, and biological inference. Ask what changes with reverse strand, mismatches, indels, or an incomplete reference.",
                "Kræv adskillelse af indeksresultat, mapperbeslutning og biologisk inferens. Spørg hvad der ændres med reverse strand, mismatches, indels eller en ufuldstændig reference.",
            ),
            objective_ids=("dm847.lab03.locate", "dm847.lab03.interpretation"),
            estimated_minutes=20,
        ),
        LabTask(
            task_id="dm847.lab03.defend.complexity",
            stage=LabStage.DEFEND,
            kind=LabTaskKind.SHORT_ANSWER,
            title=_text(
                "Defensa de arquitectura y complejidad",
                "Architecture and complexity defence",
                "Forsvar af arkitektur og kompleksitet",
            ),
            instructions=_text(
                "Defiende cuándo compensa construir un índice. Compara búsqueda exhaustiva, SA con búsqueda binaria y FM-index en construcción, memoria, count y locate. Explica por qué conservar el SA completo simplifica locate pero no representa un FM-index comprimido de producción.",
                "Defend when index construction is worthwhile. Compare exhaustive search, suffix-array binary search, and the FM-index in construction, memory, count, and locate. Explain why retaining the full SA simplifies locate but is not a production compressed FM-index.",
                "Forsvar hvornår indekskonstruktion kan betale sig. Sammenlign udtømmende søgning, binær søgning i suffix array og FM-index med hensyn til konstruktion, hukommelse, count og locate. Forklar hvorfor et fuldt SA forenkler locate, men ikke er et komprimeret produktions-FM-index.",
            ),
            mentor_notes=_text(
                "Solicita primero variables n, m y q. Después pide costes separados para preprocesamiento y consulta, y una justificación para muestreo del SA.",
                "First request variables n, m, and q. Then request separate preprocessing and query costs, plus a justification for SA sampling.",
                "Bed først om variablerne n, m og q. Bed derefter om separate omkostninger for preprocessing og forespørgsler samt en begrundelse for SA-sampling.",
            ),
            objective_ids=("dm847.lab03.complexity", "dm847.lab03.fm-index"),
            estimated_minutes=25,
        ),
        LabTask(
            task_id="dm847.lab03.consolidate.index-reflection",
            stage=LabStage.CONSOLIDATE,
            kind=LabTaskKind.SHORT_ANSWER,
            title=_text(
                "Auditoría del índice",
                "Index audit",
                "Indeksaudit",
            ),
            instructions=_text(
                "Registra el error más importante, cómo lo detectaste y la prueba que evita su regreso. Añade una extensión prioritaria: LCP eficiente, SA muestreado, búsqueda aproximada o integración con alineamiento.",
                "Record the most important error, how you detected it, and the test that prevents recurrence. Add one priority extension: efficient LCP, sampled SA, approximate search, or alignment integration.",
                "Registrér den vigtigste fejl, hvordan du fandt den, og testen der forhindrer gentagelse. Tilføj én prioriteret udvidelse: effektiv LCP, samplet SA, approksimativ søgning eller integration med alignment.",
            ),
            mentor_notes=_text(
                "No aceptes una reflexión genérica. Exige síntoma, causa, corrección, regresión y razón para priorizar la extensión elegida.",
                "Do not accept a generic reflection. Require symptom, cause, correction, regression test, and rationale for the selected extension.",
                "Acceptér ikke en generisk refleksion. Kræv symptom, årsag, rettelse, regressionstest og begrundelse for den valgte udvidelse.",
            ),
            objective_ids=(
                "dm847.lab03.contract",
                "dm847.lab03.complexity",
                "dm847.lab03.interpretation",
            ),
            estimated_minutes=15,
        ),
    ),
)


__all__ = ["DM847_LAB_03"]
