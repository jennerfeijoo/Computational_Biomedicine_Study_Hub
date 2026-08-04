"""DM847 pilot laboratory: exact and approximate short-read mapping."""

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


_DISTANCE_STARTER = '''def normalize_dna(sequence):
    """Return an uppercase DNA sequence without whitespace."""
    # Reject empty sequences and symbols outside A, C, G, and T.
    raise NotImplementedError


def hamming_distance(left, right):
    """Return the number of substitutions between equal-length DNA strings."""
    raise NotImplementedError
'''

_DISTANCE_CHECKS = """
print(normalize_dna(" ac gt\\n"))
print(hamming_distance("ACGTT", "ACGTA"))
"""

_MAPPING_CHECKS = """
assert hamming_distance("AAAA", "AAAT") == 1
assert find_matches("ACGTTGCATG", "ACGTA", 1) == [(0, 1)]
assert find_matches("GCATGCATG", "GCATG", 0) == [(0, 0), (4, 0)]
assert classify_mapping([]) == "unmapped"
assert classify_mapping([(3, 0)]) == "unique"
assert classify_mapping([(0, 0), (4, 0)]) == "multimapping"
try:
    find_matches("ACGT", "ACGTA", 1)
except ValueError:
    pass
else:
    raise AssertionError("A read longer than the reference must raise ValueError")
try:
    find_matches("ACGT", "ACG", -1)
except ValueError:
    pass
else:
    raise AssertionError("Negative mismatch limits must raise ValueError")
print(find_matches("ACGTT", "ACGTA", 1))
print(classify_mapping([(0, 0), (4, 0)]))
print("edge cases passed")
"""


DM847_LAB_01 = ComputationalLab(
    lab_id="dm847.lab01.short-read-mapping",
    course_code="DM847",
    version="1.0.0",
    title=_text(
        "Laboratorio 1: mapeo exacto y aproximado de lecturas",
        "Laboratory 1: exact and approximate read mapping",
        "Laboratorium 1: eksakt og tilnærmet read-mapping",
    ),
    research_question=_text(
        "¿Cómo cambian la asignación y la incertidumbre de una lectura corta cuando permitimos sustituciones durante el mapeo?",
        "How do the assignment and uncertainty of a short read change when substitutions are allowed during mapping?",
        "Hvordan ændres tildelingen og usikkerheden for et kort read, når substitutioner tillades under mapping?",
    ),
    disclaimer=_text(
        "Preparación interna alineada con los resultados de aprendizaje de DM847 sobre representación de secuencias, coincidencia y mapeo. No reproduce una hoja oficial de SDU.",
        "Internal preparation aligned with DM847 learning outcomes on sequence representation, matching, and mapping. It does not reproduce an official SDU sheet.",
        "Intern forberedelse i overensstemmelse med læringsmålene i DM847 om sekvensrepræsentation, matching og mapping. Den gengiver ikke et officielt SDU-ark.",
    ),
    data_provenance=_text(
        "La referencia y las lecturas son secuencias sintéticas diseñadas para exponer coincidencias únicas, multimapeo, una sustitución y ausencia de alineamiento. No representan muestras reales.",
        "The reference and reads are synthetic sequences designed to expose unique matches, multimapping, one substitution, and no alignment. They do not represent real samples.",
        "Referencen og reads er syntetiske sekvenser designet til at vise unikke matches, multimapping, én substitution og manglende alignment. De repræsenterer ikke virkelige prøver.",
    ),
    objectives=(
        (
            "dm847.lab01.sequence-contract",
            _text(
                "Definir un contrato explícito para secuencias de ADN, longitudes y límites de mismatches.",
                "Define an explicit contract for DNA sequences, lengths, and mismatch limits.",
                "Definér en eksplicit kontrakt for DNA-sekvenser, længder og mismatch-grænser.",
            ),
        ),
        (
            "dm847.lab01.distance",
            _text(
                "Implementar y justificar distancia de Hamming para lecturas de igual longitud.",
                "Implement and justify Hamming distance for equal-length reads.",
                "Implementér og begrund Hamming-afstand for reads med samme længde.",
            ),
        ),
        (
            "dm847.lab01.mapping",
            _text(
                "Enumerar coincidencias exactas y aproximadas mediante una búsqueda exhaustiva reproducible.",
                "Enumerate exact and approximate matches using a reproducible exhaustive search.",
                "Enumerér eksakte og tilnærmede matches med en reproducerbar udtømmende søgning.",
            ),
        ),
        (
            "dm847.lab01.uncertainty",
            _text(
                "Distinguir lecturas no mapeadas, únicas y multimapeadas sin inventar certeza biológica.",
                "Distinguish unmapped, unique, and multimapping reads without inventing biological certainty.",
                "Skeln mellem ikke-mappede, unikke og multimappede reads uden at opfinde biologisk sikkerhed.",
            ),
        ),
    ),
    prerequisites=(
        _text(
            "Cadenas, listas, tuplas, bucles y funciones en Python.",
            "Strings, lists, tuples, loops, and functions in Python.",
            "Strenge, lister, tupler, løkker og funktioner i Python.",
        ),
        _text(
            "Alfabeto de ADN y orientación 5′→3′.",
            "The DNA alphabet and 5′→3′ orientation.",
            "DNA-alfabetet og 5′→3′-retningen.",
        ),
        _text(
            "Diferencia entre una coincidencia de cadena y una afirmación sobre origen biológico.",
            "The difference between a string match and a claim about biological origin.",
            "Forskellen mellem et strengmatch og en påstand om biologisk oprindelse.",
        ),
    ),
    tasks=(
        LabTask(
            task_id="dm847.lab01.prepare.contract",
            stage=LabStage.PREPARE,
            kind=LabTaskKind.SHORT_ANSWER,
            title=_text("Contrato de secuencia", "Sequence contract", "Sekvenskontrakt"),
            instructions=_text(
                "Define qué símbolos aceptarás, cómo tratarás espacios y minúsculas, qué ocurrirá con secuencias vacías, lecturas más largas que la referencia y límites de mismatches negativos o no enteros.",
                "Define which symbols you will accept, how whitespace and lowercase letters are handled, and what happens for empty sequences, reads longer than the reference, and negative or non-integer mismatch limits.",
                "Definér hvilke symboler du accepterer, hvordan mellemrum og små bogstaver håndteres, og hvad der sker for tomme sekvenser, reads længere end referencen samt negative eller ikke-heltallige mismatch-grænser.",
            ),
            mentor_notes=_text(
                "Pregunta por el alfabeto, la normalización, bool como subtipo de int y la relación entre longitud de lectura y referencia. No proporciones código todavía.",
                "Ask about the alphabet, normalization, bool as an int subtype, and the relationship between read and reference length. Do not provide code yet.",
                "Spørg til alfabetet, normalisering, bool som en undertype af int og forholdet mellem read- og referencelængde. Giv endnu ikke kode.",
            ),
            objective_ids=("dm847.lab01.sequence-contract",),
            estimated_minutes=15,
        ),
        LabTask(
            task_id="dm847.lab01.investigate.manual-mapping",
            stage=LabStage.INVESTIGATE,
            kind=LabTaskKind.SHORT_ANSWER,
            title=_text("Mapeo manual", "Manual mapping", "Manuel mapping"),
            instructions=_text(
                "Usa la referencia ACGTTGCATGTCGCATGATGCATGAGAGCT. Localiza exactamente GATGC y GCATG; después localiza ACGTA permitiendo una sustitución. Reporta posiciones con índice cero y clasifica cada lectura.",
                "Use the reference ACGTTGCATGTCGCATGATGCATGAGAGCT. Locate GATGC and GCATG exactly; then locate ACGTA allowing one substitution. Report zero-based positions and classify each read.",
                "Brug referencen ACGTTGCATGTCGCATGATGCATGAGAGCT. Find GATGC og GCATG eksakt; find derefter ACGTA med én tilladt substitution. Rapportér nulbaserede positioner og klassificér hvert read.",
            ),
            mentor_notes=_text(
                "Exige mostrar ventanas comparadas y número de diferencias. Verifica que GATGC sea única, GCATG multimapeada y ACGTA única solo con una sustitución.",
                "Require the compared windows and mismatch counts. Verify that GATGC is unique, GCATG multimaps, and ACGTA becomes unique only with one substitution.",
                "Kræv de sammenlignede vinduer og mismatch-antal. Kontrollér at GATGC er unik, GCATG multimapper, og ACGTA kun bliver unik med én substitution.",
            ),
            objective_ids=(
                "dm847.lab01.distance",
                "dm847.lab01.mapping",
                "dm847.lab01.uncertainty",
            ),
            estimated_minutes=20,
        ),
        LabTask(
            task_id="dm847.lab01.implement.distance",
            stage=LabStage.IMPLEMENT,
            kind=LabTaskKind.PYTHON,
            title=_text(
                "Normalización y distancia",
                "Normalization and distance",
                "Normalisering og afstand",
            ),
            instructions=_text(
                "Implementa normalize_dna y hamming_distance. Normaliza espacios y minúsculas, rechaza alfabetos inválidos y exige longitudes iguales para calcular Hamming.",
                "Implement normalize_dna and hamming_distance. Normalize whitespace and lowercase letters, reject invalid alphabets, and require equal lengths for Hamming distance.",
                "Implementér normalize_dna og hamming_distance. Normalisér mellemrum og små bogstaver, afvis ugyldige alfabeter og kræv samme længde ved Hamming-afstand.",
            ),
            mentor_notes=_text(
                "Pregunta primero por precondiciones y por qué Hamming no admite inserciones ni deleciones. Ofrece una comprensión por zip solo después de que el estudiante formule el algoritmo.",
                "Ask first about preconditions and why Hamming distance does not model insertions or deletions. Offer a zip comprehension only after the learner states the algorithm.",
                "Spørg først til forudsætninger og hvorfor Hamming-afstand ikke modellerer insertioner eller deletioner. Tilbyd først en zip-komprehension efter at den studerende har formuleret algoritmen.",
            ),
            objective_ids=(
                "dm847.lab01.sequence-contract",
                "dm847.lab01.distance",
            ),
            estimated_minutes=35,
            starter_response=_DISTANCE_STARTER,
            verification_source=_DISTANCE_CHECKS,
            expected_output="ACGT\n1",
        ),
        LabTask(
            task_id="dm847.lab01.check.mapper",
            stage=LabStage.CHECK,
            kind=LabTaskKind.PYTHON,
            title=_text(
                "Búsqueda y clasificación",
                "Search and classification",
                "Søgning og klassifikation",
            ),
            instructions=_text(
                "Amplía el código con find_matches(reference, read, max_mismatches) y classify_mapping(matches). Devuelve pares (posición, mismatches) ordenados por posición y clasifica como unmapped, unique o multimapping.",
                "Extend the code with find_matches(reference, read, max_mismatches) and classify_mapping(matches). Return (position, mismatches) pairs ordered by position and classify as unmapped, unique, or multimapping.",
                "Udvid koden med find_matches(reference, read, max_mismatches) og classify_mapping(matches). Returnér par af (position, mismatches) sorteret efter position og klassificér som unmapped, unique eller multimapping.",
            ),
            mentor_notes=_text(
                "Cuando falle, pide identificar si el error está en la ventana, el rango final, la validación o la clasificación. No reveles las comprobaciones internas.",
                "When it fails, ask whether the error lies in the window, final range, validation, or classification. Do not reveal internal checks.",
                "Ved fejl skal du spørge, om fejlen ligger i vinduet, slutområdet, valideringen eller klassifikationen. Afslør ikke de interne kontroller.",
            ),
            objective_ids=(
                "dm847.lab01.sequence-contract",
                "dm847.lab01.mapping",
                "dm847.lab01.uncertainty",
            ),
            estimated_minutes=50,
            verification_source=_MAPPING_CHECKS,
            expected_output="[(0, 1)]\nmultimapping\nedge cases passed",
            seed_from_task_id="dm847.lab01.implement.distance",
        ),
        LabTask(
            task_id="dm847.lab01.interpret.mapping",
            stage=LabStage.INTERPRET,
            kind=LabTaskKind.SHORT_ANSWER,
            title=_text(
                "Interpretación del mapeo",
                "Mapping interpretation",
                "Fortolkning af mapping",
            ),
            instructions=_text(
                "Explica qué significa que una lectura tenga cero, una o varias posiciones candidatas. Separa evidencia algorítmica de afirmaciones sobre gen, variante, expresión u origen biológico. Incluye el efecto de permitir más mismatches.",
                "Explain what zero, one, or several candidate positions mean. Separate algorithmic evidence from claims about genes, variants, expression, or biological origin. Include the effect of allowing more mismatches.",
                "Forklar hvad nul, én eller flere kandidatpositioner betyder. Adskil algoritmisk evidens fra påstande om gener, varianter, ekspression eller biologisk oprindelse. Medtag effekten af at tillade flere mismatches.",
            ),
            mentor_notes=_text(
                "Exige mencionar repetitividad, calidad de base, hebra inversa, indels, referencia incompleta y política de multimapeo. No aceptes 'único' como sinónimo automático de 'correcto'.",
                "Require discussion of repetitiveness, base quality, reverse strand, indels, incomplete reference, and multimapping policy. Do not accept 'unique' as an automatic synonym for 'correct'.",
                "Kræv omtale af repetitivitet, basekvalitet, reverse strand, indels, ufuldstændig reference og multimapping-politik. Accepter ikke 'unique' som automatisk synonym for 'correct'.",
            ),
            objective_ids=("dm847.lab01.uncertainty",),
            estimated_minutes=25,
        ),
        LabTask(
            task_id="dm847.lab01.defend.algorithm",
            stage=LabStage.DEFEND,
            kind=LabTaskKind.SHORT_ANSWER,
            title=_text(
                "Defensa algorítmica",
                "Algorithmic defence",
                "Algoritmisk forsvar",
            ),
            instructions=_text(
                "Defiende la búsqueda exhaustiva como referencia didáctica y compárala con un índice de sufijos o FM-index. Expón complejidad, memoria, verificabilidad y qué cambia al admitir mismatches.",
                "Defend exhaustive search as a teaching reference and compare it with a suffix index or FM-index. Discuss complexity, memory, verifiability, and what changes when mismatches are allowed.",
                "Forsvar udtømmende søgning som didaktisk reference og sammenlign med et suffix-indeks eller FM-index. Diskutér kompleksitet, hukommelse, verificerbarhed og hvad der ændres, når mismatches tillades.",
            ),
            mentor_notes=_text(
                "Actúa como examinador. Solicita complejidad en función de referencia, lectura y número de lecturas; después pide una consecuencia práctica y una limitación del método alternativo.",
                "Act as an examiner. Request complexity in terms of reference length, read length, and read count; then ask for one practical consequence and one limitation of the alternative method.",
                "Opfør dig som eksaminator. Bed om kompleksitet som funktion af referencelængde, read-længde og antal reads; spørg derefter efter en praktisk konsekvens og en begrænsning ved alternativet.",
            ),
            objective_ids=(
                "dm847.lab01.mapping",
                "dm847.lab01.uncertainty",
            ),
            estimated_minutes=25,
        ),
        LabTask(
            task_id="dm847.lab01.consolidate.error",
            stage=LabStage.CONSOLIDATE,
            kind=LabTaskKind.SHORT_ANSWER,
            title=_text(
                "Registro de error y siguiente modelo",
                "Error record and next model",
                "Fejlregistrering og næste model",
            ),
            instructions=_text(
                "Documenta el error más importante, el caso que lo reveló y la prueba que evita su regreso. Después identifica qué cambio exigiría pasar de Hamming a alineamiento con inserciones y deleciones.",
                "Document the most important error, the case that revealed it, and the test that prevents recurrence. Then identify what must change to move from Hamming distance to alignment with insertions and deletions.",
                "Dokumentér den vigtigste fejl, casen der afslørede den, og testen der forhindrer gentagelse. Identificér derefter hvad der skal ændres for at gå fra Hamming-afstand til alignment med insertioner og deletioner.",
            ),
            mentor_notes=_text(
                "Comprueba que la reflexión conecte error, causa, corrección y prueba. Para el siguiente modelo, busca la necesidad de programación dinámica y una función de puntuación explícita.",
                "Check that the reflection connects error, cause, correction, and test. For the next model, look for the need for dynamic programming and an explicit scoring function.",
                "Kontrollér at refleksionen forbinder fejl, årsag, rettelse og test. For næste model skal du lede efter behovet for dynamisk programmering og en eksplicit scoringsfunktion.",
            ),
            objective_ids=(
                "dm847.lab01.distance",
                "dm847.lab01.mapping",
                "dm847.lab01.uncertainty",
            ),
            estimated_minutes=20,
        ),
    ),
    estimated_minutes=190,
)

__all__ = ["DM847_LAB_01"]
