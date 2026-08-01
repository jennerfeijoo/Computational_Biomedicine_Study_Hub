"""Textbook-grounded enrichment for DM847 authored modules.

The additions are independently authored paraphrases. The evidence records point to
the textbook sections used to verify the concepts and exercise structure without
embedding source text in the application.
"""

from __future__ import annotations

from dataclasses import replace

from ...learning.activity_types import ActivityType
from ..bibliography import (
    ContentEvidence,
    EvidenceStatus,
    validate_evidence_catalog,
)
from ..localized_models import LocalizedLearningModule
from .authoring import concept, example, practice, t


DM847_TEXTBOOK_EVIDENCE: tuple[ContentEvidence, ...] = (
    ContentEvidence(
        evidence_id="dm847.m06.compeau-pevzner-indexes",
        course_code="DM847",
        module_id="dm847.m06",
        content_ids=(
            "m06.o1",
            "m06.o2",
            "m06.o3",
            "m06.o4",
            "m06.o5",
            "m06.o6",
            "suffix-array",
            "lcp",
            "suffix-tree",
            "index-equivalence",
            "bwt",
            "lf-mapping",
            "fm-index",
            "read-mapping",
            "m06.e04",
            "m06.p09",
            "m06.p10",
        ),
        source_id="compeau-pevzner-v2-2e-2015",
        locator=(
            "Chapter 9, pp. 120–177; suffix trees pp. 131–133; suffix arrays "
            "pp. 133–136; BWT and matching pp. 136–159; mismatch-tolerant read "
            "mapping pp. 159–162; implementation challenges 9I–9R."
        ),
        supported_scope=(
            "Multiple-pattern indexing, suffix tries and compacted suffix trees, "
            "suffix arrays, BWT inversion and backward matching, partial suffix "
            "arrays, and approximate pattern matching."
        ),
        status=EvidenceStatus.VERIFIED,
        review_note=(
            "The Study Hub explanations, code, and exercises are original paraphrases; "
            "the textbook is used only to verify scope and algorithmic relationships."
        ),
    ),
)
validate_evidence_catalog(DM847_TEXTBOOK_EVIDENCE)


def enrich_module_06(module: LocalizedLearningModule) -> LocalizedLearningModule:
    """Add suffix-tree coverage and exact textbook provenance to DM847 module 6."""

    if module.module_id != "dm847.m06":
        raise ValueError("DM847 module 6 enrichment received the wrong module.")
    if any(item.concept_id == "suffix-tree" for item in module.concepts):
        return module

    suffix_tree = concept(
        "suffix-tree",
        ("Suffix tree compactado", "Compacted suffix tree", "Komprimeret suffix tree"),
        (
            "Un suffix tree es un trie de todos los sufijos en el que cada camino no "
            "ramificado se comprime en una sola arista etiquetada por un intervalo del "
            "texto. El centinela único hace que cada sufijo termine en una hoja distinta. "
            "Después de construir el índice, un patrón se recorre carácter por carácter "
            "a lo largo de etiquetas de arista; las hojas bajo el punto alcanzado "
            "representan sus ocurrencias. Una implementación real guarda límites de "
            "subcadenas, no copias de todas las etiquetas.",
            "A suffix tree is a trie of all suffixes in which each non-branching path is "
            "compressed into one edge labelled by an interval of the text. The unique "
            "sentinel makes every suffix terminate at a distinct leaf. After index "
            "construction, a pattern is traversed character by character along edge "
            "labels; leaves below the reached locus represent its occurrences. A real "
            "implementation stores substring boundaries rather than copies of every label.",
            "Et suffix tree er en trie over alle suffikser, hvor hver ikke-forgrenende "
            "sti komprimeres til én kant mærket med et interval i teksten. Den unikke "
            "sentinel gør, at hvert suffiks ender i et særskilt blad. Efter konstruktion "
            "gennemløbes et mønster tegn for tegn langs kantetiketter; bladene under det "
            "nåede sted repræsenterer forekomsterne. En reel implementering lagrer "
            "delstrengsgrænser frem for kopier af alle etiketter.",
        ),
        (
            (
                "Comprimir caminos no ramificados distingue un suffix tree de un suffix trie.",
                "Compressing non-branching paths distinguishes a suffix tree from a suffix trie.",
                "Komprimering af ikke-forgrenende stier adskiller et suffix tree fra en suffix trie.",
            ),
            (
                "Las aristas deben referenciar intervalos del texto para evitar duplicación masiva.",
                "Edges should reference text intervals to avoid massive duplication.",
                "Kanter bør referere til tekstintervaller for at undgå massiv duplikering.",
            ),
            (
                "Las hojas descendientes permiten recuperar posiciones de coincidencia.",
                "Descendant leaves recover matching positions.",
                "Efterkommerblade gør det muligt at genskabe matchpositioner.",
            ),
        ),
    )
    index_equivalence = concept(
        "index-equivalence",
        (
            "Relación entre tree, array, LCP y BWT",
            "Relationship among tree, array, LCP, and BWT",
            "Forholdet mellem tree, array, LCP og BWT",
        ),
        (
            "Suffix tree, suffix array con LCP y FM-index representan relaciones "
            "estrechamente conectadas, pero optimizan operaciones y memoria de forma "
            "distinta. El orden de izquierda a derecha de las hojas del tree produce el "
            "suffix array; los ancestros comunes profundos se reflejan en valores LCP "
            "altos. La BWT se deriva del mismo orden de sufijos y el FM-index añade rank "
            "y conteos para buscar sin almacenar el tree explícito. La equivalencia "
            "conceptual no implica que todas las estructuras tengan el mismo coste.",
            "A suffix tree, a suffix array with LCP, and an FM-index encode closely "
            "connected relationships while optimizing different operations and memory "
            "costs. Reading tree leaves from left to right yields the suffix array; deep "
            "common ancestors appear as large LCP values. BWT is derived from the same "
            "suffix order, and the FM-index adds rank and cumulative counts to search "
            "without storing the explicit tree. Conceptual equivalence does not imply "
            "identical computational cost.",
            "Et suffix tree, et suffix array med LCP og et FM-index koder nært forbundne "
            "relationer, men optimerer forskellige operationer og hukommelsesomkostninger. "
            "Læsning af træets blade fra venstre mod højre giver suffix arrayet; dybe "
            "fælles forfædre ses som høje LCP-værdier. BWT afledes af samme suffiksorden, "
            "og FM-indexet tilføjer rank og kumulative tællinger for at søge uden at "
            "lagre træet eksplicit. Konceptuel ækvivalens betyder ikke samme beregningspris.",
        ),
        (
            (
                "El máximo LCP identifica la longitud de la repetición más larga entre sufijos adyacentes.",
                "The maximum LCP identifies the longest repeat length among adjacent suffixes.",
                "Maksimal LCP identificerer længden af den længste gentagelse blandt nabosuffikser.",
            ),
            (
                "Suffix array y LCP pueden representar información estructural del tree de forma compacta.",
                "A suffix array and LCP can compactly represent structural tree information.",
                "Et suffix array og LCP kan kompakt repræsentere strukturel information fra træet.",
            ),
            (
                "La elección del índice depende de count, locate, memoria y patrón de consultas.",
                "Index choice depends on count, locate, memory, and query pattern.",
                "Valget af indeks afhænger af count, locate, hukommelse og forespørgselsmønster.",
            ),
        ),
    )
    longest_repeat_example = example(
        "m06.e04",
        (
            "Repetición más larga mediante suffix array y LCP",
            "Longest repeat through a suffix array and LCP",
            "Længste gentagelse via suffix array og LCP",
        ),
        (
            "Calcula el prefijo común de cada par de sufijos adyacentes y conserva el mayor.",
            "Compute the common prefix of every adjacent suffix pair and retain the largest.",
            "Beregn det fælles præfiks for hvert par af nabosuffikser og behold det største.",
        ),
        (
            (
                "Los sufijos se ordenan una sola vez.",
                "Suffixes are sorted once.",
                "Suffikserne sorteres én gang.",
            ),
            (
                "Una repetición aparece como prefijo común de sufijos próximos en orden lexicográfico.",
                "A repeat appears as a shared prefix of nearby suffixes in lexicographic order.",
                "En gentagelse fremstår som et fælles præfiks for nærliggende suffikser i leksikografisk orden.",
            ),
            (
                "El resultado equivale a la etiqueta del camino interno más profundo del suffix tree.",
                "The result corresponds to the deepest internal path label in the suffix tree.",
                "Resultatet svarer til etiketten på den dybeste interne sti i suffix tree'et.",
            ),
        ),
        """def suffix_array(text: str) -> list[int]:
    return sorted(range(len(text)), key=lambda index: text[index:])


def common_prefix(left: str, right: str) -> str:
    length = 0
    while length < min(len(left), len(right)) and left[length] == right[length]:
        length += 1
    return left[:length]


def longest_repeated_substring(text: str) -> str:
    array = suffix_array(text)
    best = ""
    for first, second in zip(array, array[1:], strict=False):
        candidate = common_prefix(text[first:], text[second:])
        if len(candidate) > len(best):
            best = candidate
    return best


print(longest_repeated_substring("banana$"))
""",
        "ana",
        (
            "El máximo prefijo común es ana. El ejemplo es deliberadamente ingenuo: "
            "materializa sufijos y sirve para razonar, no para indexar un genoma.",
            "The maximum common prefix is ana. The example is deliberately naive: it "
            "materializes suffixes for reasoning and is not a genome-scale index.",
            "Det maksimale fælles præfiks er ana. Eksemplet er bevidst naivt: det "
            "materialiserer suffikser til ræsonnement og er ikke et genomskalaindeks.",
        ),
    )
    tree_comparison_practice = practice(
        "m06.p09",
        ActivityType.SHORT_ANSWER,
        (
            "Compara suffix trie, suffix tree y suffix array para el mismo texto.",
            "Compare a suffix trie, suffix tree, and suffix array for the same text.",
            "Sammenlign en suffix trie, et suffix tree og et suffix array for samme tekst.",
        ),
        (
            (
                "Distingue nodos explícitos, compresión de caminos y orden de posiciones.",
                "Distinguish explicit nodes, path compression, and ordered positions.",
                "Skeln mellem eksplicitte noder, stikomprimering og ordnede positioner.",
            ),
            (
                "No afirmes que el código ingenuo tiene coste genómico aceptable.",
                "Do not claim that naive code has acceptable genome-scale cost.",
                "Påstå ikke, at naiv kode har acceptabel genomskalaomkostning.",
            ),
        ),
        (
            "El suffix trie representa cada carácter mediante una arista y contiene "
            "muchos nodos; el suffix tree comprime cada camino no ramificado y suele "
            "guardar intervalos del texto; el suffix array conserva sólo las posiciones "
            "iniciales en orden lexicográfico. Los tres apoyan pattern matching, pero "
            "difieren en memoria, navegación y operaciones auxiliares.",
            "The suffix trie represents every character with an edge and contains many "
            "nodes; the suffix tree compresses non-branching paths and usually stores "
            "text intervals; the suffix array retains only starting positions in "
            "lexicographic order. All support pattern matching but differ in memory, "
            "navigation, and auxiliary operations.",
            "Suffix trie'en repræsenterer hvert tegn med en kant og indeholder mange "
            "noder; suffix tree'et komprimerer ikke-forgrenende stier og lagrer normalt "
            "tekstintervaller; suffix arrayet bevarer kun startpositioner i leksikografisk "
            "orden. Alle understøtter pattern matching, men adskiller sig i hukommelse, "
            "navigation og hjælpeoperationer.",
        ),
        (
            "La comparación debe separar representación lógica de implementación eficiente.",
            "The comparison must separate logical representation from efficient implementation.",
            "Sammenligningen skal adskille logisk repræsentation fra effektiv implementering.",
        ),
    )
    lcp_practice = practice(
        "m06.p10",
        ActivityType.DATA_INTERPRETATION,
        (
            "Para banana$, el suffix array es [6, 5, 3, 1, 0, 4, 2] y el LCP entre "
            "entradas adyacentes es [0, 0, 1, 3, 0, 0, 2]. ¿Qué concluyes?",
            "For banana$, the suffix array is [6, 5, 3, 1, 0, 4, 2] and the LCP between "
            "adjacent entries is [0, 0, 1, 3, 0, 0, 2]. What do you conclude?",
            "For banana$ er suffix arrayet [6, 5, 3, 1, 0, 4, 2], og LCP mellem "
            "naboposter er [0, 0, 1, 3, 0, 0, 2]. Hvad konkluderer du?",
        ),
        (
            (
                "Localiza el valor máximo y los dos sufijos correspondientes.",
                "Locate the maximum value and its two corresponding suffixes.",
                "Find maksimumsværdien og de to tilsvarende suffikser.",
            ),
            (
                "Interpreta repetición, no distancia genómica.",
                "Interpret repetition, not genomic distance.",
                "Fortolk gentagelse, ikke genomisk afstand.",
            ),
        ),
        (
            "El máximo LCP es 3 entre los sufijos que comienzan en 3 y 1, por lo que ana "
            "es la repetición más larga. El valor 2 entre las posiciones 4 y 2 identifica "
            "na como otra repetición. Los valores no indican proximidad física entre las "
            "ocurrencias.",
            "The maximum LCP is 3 between suffixes starting at 3 and 1, so ana is the "
            "longest repeat. The value 2 between positions 4 and 2 identifies na as "
            "another repeat. The values do not indicate physical proximity between "
            "occurrences.",
            "Maksimal LCP er 3 mellem suffikserne, der starter ved 3 og 1, så ana er den "
            "længste gentagelse. Værdien 2 mellem position 4 og 2 identificerer na som en "
            "anden gentagelse. Værdierne angiver ikke fysisk nærhed mellem forekomsterne.",
        ),
        (
            "LCP resume longitud de prefijo compartido y conecta array con estructura de tree.",
            "LCP summarizes shared-prefix length and connects the array to tree structure.",
            "LCP opsummerer længden af fælles præfiks og forbinder arrayet med træstrukturen.",
        ),
    )

    tutor = module.tutor_support
    canonical = t(
        tutor.canonical_explanation.spanish
        + " Un suffix tree añade la vista estructural: comprime caminos no ramificados del "
        "suffix trie, y sus hojas en orden producen el suffix array. El LCP conserva parte "
        "de esa estructura sin almacenar el tree explícito.",
        tutor.canonical_explanation.english
        + " A suffix tree adds the structural view: it compresses non-branching paths of "
        "the suffix trie, and its ordered leaves yield the suffix array. LCP retains part "
        "of that structure without storing the explicit tree.",
        tutor.canonical_explanation.danish
        + " Et suffix tree tilføjer den strukturelle visning: det komprimerer "
        "ikke-forgrenende stier i suffix trie'en, og de ordnede blade giver suffix arrayet. "
        "LCP bevarer en del af strukturen uden at lagre træet eksplicit.",
    )

    return replace(
        module,
        concepts=module.concepts + (suffix_tree, index_equivalence),
        worked_examples=module.worked_examples + (longest_repeat_example,),
        practice_exercises=module.practice_exercises
        + (tree_comparison_practice, lcp_practice),
        tutor_support=replace(
            tutor,
            canonical_explanation=canonical,
            knowledge_fragments=tutor.knowledge_fragments
            + (
                t(
                    "Suffix tree comprime caminos no ramificados.",
                    "A suffix tree compresses non-branching paths.",
                    "Et suffix tree komprimerer ikke-forgrenende stier.",
                ),
                t(
                    "El orden de hojas del tree produce el suffix array.",
                    "Tree leaf order yields the suffix array.",
                    "Træets bladrækkefølge giver suffix arrayet.",
                ),
            ),
            common_misconceptions=tutor.common_misconceptions
            + (
                t(
                    "Confundir suffix trie con suffix tree compactado.",
                    "Confusing a suffix trie with a compacted suffix tree.",
                    "At forveksle en suffix trie med et komprimeret suffix tree.",
                ),
            ),
            socratic_questions=tutor.socratic_questions
            + (
                t(
                    "¿Qué caminos se comprimen y qué información debe conservarse?",
                    "Which paths are compressed, and what information must be retained?",
                    "Hvilke stier komprimeres, og hvilke oplysninger skal bevares?",
                ),
            ),
            grading_criteria=tutor.grading_criteria
            + (
                t(
                    "Relaciona correctamente suffix tree, suffix array y LCP.",
                    "Correctly relates the suffix tree, suffix array, and LCP.",
                    "Relaterer suffix tree, suffix array og LCP korrekt.",
                ),
            ),
            source_basis=tutor.source_basis
            + (
                "Compeau and Pevzner, Bioinformatics Algorithms, 2nd ed., Volume 2 "
                "(2015), Chapter 9, pp. 120–177.",
                "Compeau and Pevzner, Volume 2, Chapter 9 implementation challenges "
                "9I–9R for BWT, partial suffix arrays, and suffix-tree reconstruction.",
            ),
        ),
    )


__all__ = ["DM847_TEXTBOOK_EVIDENCE", "enrich_module_06"]
