"""Focused book-grounded extensions for DM847 hidden models and text indexes."""

from __future__ import annotations

from dataclasses import replace

from ...learning.activity_types import ActivityType
from ..localized_models import LocalizedLearningModule, LocalizedTutorSupportPacket
from .authoring import concept, example, objective, objective_mcq, practice
from .book_grounded_audit import ModuleSourceAudit


def _with_source_basis(
    module: LocalizedLearningModule,
    source_ids: tuple[str, ...],
) -> LocalizedLearningModule:
    tutor = module.tutor_support
    merged = tuple(dict.fromkeys((*tutor.source_basis, *source_ids)))
    updated_tutor: LocalizedTutorSupportPacket = replace(tutor, source_basis=merged)
    return replace(module, tutor_support=updated_tutor)


def update_hmm_bwt_audit(
    audit: tuple[ModuleSourceAudit, ...],
) -> tuple[ModuleSourceAudit, ...]:
    """Mark M05 and M06 reviewed only after their focused extensions exist."""

    findings = {
        "dm847.m05": (
            "Existing coverage of HMM components, joint and marginal probability, Forward, "
            "Viterbi, numerical stability, supervised estimation, Baum-Welch, and profile "
            "HMMs is consistent. Soft decoding with Forward-Backward posterior state "
            "probabilities required one explicit treatment."
        ),
        "dm847.m06": (
            "Existing coverage of suffix arrays, LCP, BWT, LF-mapping, backward search, "
            "FM-index count and locate operations, sampling, multimapping, and seed-and-extend "
            "is consistent. The pigeonhole guarantee that reduces mismatch-bounded search to "
            "exact seed searches required one explicit treatment."
        ),
    }
    changes = {
        "dm847.m05": (
            "Added an original trilingual soft-decoding explanation, deterministic "
            "Forward-Backward posterior example, debugging exercise, and stable objective item."
        ),
        "dm847.m06": (
            "Added an original trilingual pigeonhole-seeding explanation, deterministic "
            "candidate-generation and verification example, design exercise, and stable "
            "objective item."
        ),
    }

    updated: list[ModuleSourceAudit] = []
    for item in audit:
        if item.module_id in findings:
            updated.append(
                replace(
                    item,
                    state="consistent",
                    finding=findings[item.module_id],
                    implemented_change=changes[item.module_id],
                )
            )
        else:
            updated.append(item)
    return tuple(updated)


def _extend_hidden_markov_models(
    module: LocalizedLearningModule,
) -> LocalizedLearningModule:
    """Add explicit soft decoding and posterior-state interpretation to M05."""

    extended = replace(
        module,
        objectives=module.objectives
        + (
            objective(
                "m05.bg.o1",
                (
                    "Calcular probabilidades posteriores de estado con Forward-Backward y "
                    "distinguir decodificación suave de la ruta Viterbi.",
                    "Compute posterior state probabilities with Forward-Backward and distinguish "
                    "soft decoding from the Viterbi path.",
                    "Beregne posterior-tilstandssandsynligheder med Forward-Backward og skelne "
                    "soft decoding fra Viterbi-stien.",
                ),
            ),
        ),
        concepts=module.concepts
        + (
            concept(
                "soft-decoding-forward-backward",
                (
                    "Decodificación suave con Forward-Backward",
                    "Soft decoding with Forward-Backward",
                    "Soft decoding med Forward-Backward",
                ),
                (
                    "Forward calcula para cada posición y estado la probabilidad conjunta del "
                    "prefijo observado y de terminar en ese estado. Backward calcula la "
                    "probabilidad del sufijo restante condicionada al estado actual. El producto "
                    "de ambos valores, dividido por la probabilidad total de la secuencia, produce "
                    "la probabilidad posterior del estado en esa posición. Estas probabilidades "
                    "deben sumar uno por posición y expresan incertidumbre local. Viterbi responde "
                    "otra pregunta: encuentra una sola ruta global con probabilidad conjunta "
                    "máxima. Elegir independientemente el estado posterior más probable en cada "
                    "posición no equivale necesariamente a Viterbi y puede incluso producir una "
                    "secuencia de estados incompatible con transiciones estructuralmente "
                    "imposibles. Los valores Forward normalizados usando sólo el prefijo son "
                    "probabilidades filtradas, no posteriores suavizadas con toda la secuencia.",
                    "Forward computes, for each position and state, the joint probability of the "
                    "observed prefix and ending in that state. Backward computes the probability "
                    "of the remaining suffix conditional on the current state. Their product, "
                    "divided by total sequence probability, yields the posterior probability of "
                    "the state at that position. These probabilities must sum to one at each "
                    "position and express local uncertainty. Viterbi answers a different question: "
                    "it finds one global path with maximum joint probability. Independently "
                    "choosing the most probable posterior state at every position is not "
                    "necessarily equivalent to Viterbi and may even create a state sequence that "
                    "violates structurally impossible transitions. Forward values normalized from "
                    "the prefix alone are filtered probabilities, not posteriors smoothed with the "
                    "complete sequence.",
                    "Forward beregner for hver position og tilstand den fælles sandsynlighed for "
                    "det observerede præfiks og for at ende i tilstanden. Backward beregner "
                    "sandsynligheden for det resterende suffiks betinget af den aktuelle tilstand. "
                    "Produktet divideret med sekvensens totale sandsynlighed giver den posterior "
                    "sandsynlighed for tilstanden på positionen. Sandsynlighederne skal summere "
                    "til én pr. position og udtrykker lokal usikkerhed. Viterbi besvarer et andet "
                    "spørgsmål: den finder én global sti med maksimal fælles sandsynlighed. "
                    "Uafhængigt valg af den mest sandsynlige posterior-tilstand på hver position "
                    "er ikke nødvendigvis det samme som Viterbi og kan endda skabe en "
                    "tilstandssekvens med strukturelt umulige overgange. Forward-værdier "
                    "normaliseret ud fra præfikset alene er filtrerede sandsynligheder, ikke "
                    "posteriorer udglattet med hele sekvensen.",
                ),
                (
                    (
                        "Posterior_t(k) es proporcional a Forward_t(k) por Backward_t(k).",
                        "Posterior_t(k) is proportional to Forward_t(k) times Backward_t(k).",
                        "Posterior_t(k) er proportional med Forward_t(k) gange Backward_t(k).",
                    ),
                    (
                        "Las probabilidades posteriores suman uno en cada posición.",
                        "Posterior probabilities sum to one at each position.",
                        "Posterior-sandsynligheder summerer til én på hver position.",
                    ),
                    (
                        "La decodificación suave resume incertidumbre local; Viterbi devuelve una "
                        "ruta global.",
                        "Soft decoding summarizes local uncertainty; Viterbi returns one global "
                        "path.",
                        "Soft decoding opsummerer lokal usikkerhed; Viterbi returnerer én global "
                        "sti.",
                    ),
                    (
                        "Normalizar sólo Forward no incorpora evidencia futura.",
                        "Normalizing Forward alone does not incorporate future evidence.",
                        "Normalisering af Forward alene indarbejder ikke fremtidig evidens.",
                    ),
                ),
            ),
        ),
        worked_examples=module.worked_examples
        + (
            example(
                "m05.bg.e01",
                (
                    "Posteriores de estado para una secuencia corta",
                    "State posteriors for a short sequence",
                    "Tilstandsposteriorer for en kort sekvens",
                ),
                (
                    "Calcula Forward y Backward para la secuencia GA y normaliza su producto en "
                    "cada posición.",
                    "Compute Forward and Backward for sequence GA and normalize their product at "
                    "each position.",
                    "Beregn Forward og Backward for sekvensen GA og normalisér deres produkt på "
                    "hver position.",
                ),
                (
                    (
                        "Forward incorpora el prefijo hasta la posición actual.",
                        "Forward incorporates the prefix through the current position.",
                        "Forward indarbejder præfikset til og med den aktuelle position.",
                    ),
                    (
                        "Backward incorpora las observaciones posteriores.",
                        "Backward incorporates later observations.",
                        "Backward indarbejder de efterfølgende observationer.",
                    ),
                    (
                        "La normalización final se realiza separadamente por posición.",
                        "Final normalization is performed separately at each position.",
                        "Den endelige normalisering udføres separat på hver position.",
                    ),
                ),
                "states = ('H', 'L')\n"
                "initial = {'H': 0.5, 'L': 0.5}\n"
                "transitions = {\n"
                "    'H': {'H': 0.7, 'L': 0.3},\n"
                "    'L': {'H': 0.4, 'L': 0.6},\n"
                "}\n"
                "emissions = {\n"
                "    'H': {'G': 0.8, 'A': 0.2},\n"
                "    'L': {'G': 0.3, 'A': 0.7},\n"
                "}\n"
                "observations = 'GA'\n"
                "\n"
                "forward = [\n"
                "    {state: initial[state] * emissions[state][observations[0]] for state in states}\n"
                "]\n"
                "for symbol in observations[1:]:\n"
                "    forward.append(\n"
                "        {\n"
                "            state: emissions[state][symbol]\n"
                "            * sum(\n"
                "                forward[-1][previous] * transitions[previous][state]\n"
                "                for previous in states\n"
                "            )\n"
                "            for state in states\n"
                "        }\n"
                "    )\n"
                "\n"
                "backward = [{} for _ in observations]\n"
                "backward[-1] = {state: 1.0 for state in states}\n"
                "for position in range(len(observations) - 2, -1, -1):\n"
                "    symbol = observations[position + 1]\n"
                "    backward[position] = {\n"
                "        state: sum(\n"
                "            transitions[state][following]\n"
                "            * emissions[following][symbol]\n"
                "            * backward[position + 1][following]\n"
                "            for following in states\n"
                "        )\n"
                "        for state in states\n"
                "    }\n"
                "\n"
                "posteriors = []\n"
                "for position in range(len(observations)):\n"
                "    weights = {\n"
                "        state: forward[position][state] * backward[position][state]\n"
                "        for state in states\n"
                "    }\n"
                "    total = sum(weights.values())\n"
                "    posteriors.append(\n"
                "        {state: round(weights[state] / total, 3) for state in states}\n"
                "    )\n"
                "\n"
                "print(posteriors)",
                "[{'H': 0.651, 'L': 0.349}, {'H': 0.316, 'L': 0.684}]",
                (
                    "La primera posición favorece H y la segunda L, pero ambas conservan "
                    "incertidumbre. Estos marginales no sustituyen la probabilidad de una ruta "
                    "completa.",
                    "The first position favors H and the second favors L, but both retain "
                    "uncertainty. These marginals do not replace the probability of a complete "
                    "path.",
                    "Den første position favoriserer H og den anden L, men begge bevarer "
                    "usikkerhed. Disse marginaler erstatter ikke sandsynligheden for en komplet "
                    "sti.",
                ),
            ),
        ),
        practice_exercises=module.practice_exercises
        + (
            practice(
                "m05.bg.p01",
                ActivityType.DEBUGGING,
                (
                    "Una implementación divide cada vector Forward por su suma y presenta el "
                    "resultado como P(estado_t | secuencia completa). Diagnostica el error y "
                    "define el cálculo correcto.",
                    "An implementation divides every Forward vector by its sum and reports the "
                    "result as P(state_t | complete sequence). Diagnose the error and define the "
                    "correct calculation.",
                    "En implementering dividerer hver Forward-vektor med dens sum og rapporterer "
                    "resultatet som P(tilstand_t | komplet sekvens). Diagnosticér fejlen og "
                    "definér den korrekte beregning.",
                ),
                (
                    (
                        "Forward sólo utiliza observaciones hasta t.",
                        "Forward uses observations only through t.",
                        "Forward bruger kun observationer til og med t.",
                    ),
                    (
                        "La evidencia posterior a t entra mediante Backward.",
                        "Evidence after t enters through Backward.",
                        "Evidens efter t indgår gennem Backward.",
                    ),
                ),
                (
                    "El vector Forward normalizado representa filtrado condicionado al prefijo, "
                    "no suavizado condicionado a toda la secuencia. Calcular también Backward; "
                    "para cada posición multiplicar alpha_t(k) por beta_t(k), normalizar sobre los "
                    "estados y comprobar suma uno. Mantener separadas esta distribución posterior, "
                    "la probabilidad marginal de la secuencia y la ruta Viterbi.",
                    "The normalized Forward vector represents filtering conditional on the prefix, "
                    "not smoothing conditional on the whole sequence. Also compute Backward; at "
                    "each position multiply alpha_t(k) by beta_t(k), normalize across states, and "
                    "check that the result sums to one. Keep this posterior distribution separate "
                    "from sequence marginal probability and the Viterbi path.",
                    "Den normaliserede Forward-vektor repræsenterer filtrering betinget af "
                    "præfikset, ikke smoothing betinget af hele sekvensen. Beregn også Backward; "
                    "multiplicér alpha_t(k) med beta_t(k) på hver position, normalisér over "
                    "tilstandene og kontrollér sum én. Hold posteriorfordelingen adskilt fra "
                    "sekvensens marginale sandsynlighed og Viterbi-stien.",
                ),
                (
                    "El diagnóstico distingue evidencia pasada, evidencia futura y el objetivo "
                    "probabilístico de cada algoritmo.",
                    "The diagnosis separates past evidence, future evidence, and the probabilistic "
                    "target of each algorithm.",
                    "Diagnosen adskiller tidligere evidens, fremtidig evidens og det "
                    "probabilistiske mål for hver algoritme.",
                ),
            ),
        ),
        assessment_items=module.assessment_items
        + (
            objective_mcq(
                "dm847.m05.book.001",
                (
                    "¿Qué cálculo produce P(estado_t | secuencia completa)?",
                    "Which computation produces P(state_t | complete sequence)?",
                    "Hvilken beregning giver P(tilstand_t | komplet sekvens)?",
                ),
                (
                    (
                        "forward_backward",
                        (
                            "Normalizar alpha_t(k) por beta_t(k) sobre los estados.",
                            "Normalize alpha_t(k) times beta_t(k) across states.",
                            "Normalisér alpha_t(k) gange beta_t(k) over tilstandene.",
                        ),
                    ),
                    (
                        "viterbi",
                        (
                            "Tomar únicamente el predecesor máximo de Viterbi.",
                            "Use only the maximizing Viterbi predecessor.",
                            "Brug kun den maksimerende Viterbi-forgænger.",
                        ),
                    ),
                    (
                        "forward_only",
                        (
                            "Normalizar Forward sin usar las observaciones posteriores.",
                            "Normalize Forward without using later observations.",
                            "Normalisér Forward uden at bruge senere observationer.",
                        ),
                    ),
                ),
                "forward_backward",
                (
                    "Forward aporta evidencia del prefijo y Backward del sufijo restante; su "
                    "producto normalizado produce el posterior suavizado.",
                    "Forward contributes prefix evidence and Backward the remaining suffix; their "
                    "normalized product yields the smoothed posterior.",
                    "Forward bidrager med præfiksevidens og Backward med det resterende suffiks; "
                    "deres normaliserede produkt giver den udglattede posterior.",
                ),
            ),
        ),
    )
    return _with_source_basis(
        extended,
        ("sdu-dm847-active-2025", "compeau-pevzner-v2-ch10"),
    )


def _extend_bwt_mapping(module: LocalizedLearningModule) -> LocalizedLearningModule:
    """Add the pigeonhole seed guarantee and full-candidate verification to M06."""

    extended = replace(
        module,
        objectives=module.objectives
        + (
            objective(
                "m06.bg.o1",
                (
                    "Reducir búsqueda con hasta d mismatches a d+1 búsquedas exactas de semillas "
                    "y verificar cada candidato completo.",
                    "Reduce matching with at most d mismatches to d+1 exact seed searches and "
                    "verify every complete candidate.",
                    "Reducere matching med højst d mismatches til d+1 eksakte seed-søgninger og "
                    "verificere hver komplet kandidat.",
                ),
            ),
        ),
        concepts=module.concepts
        + (
            concept(
                "pigeonhole-seeding-and-verification",
                (
                    "Semillas por principio del palomar y verificación",
                    "Pigeonhole seeding and verification",
                    "Pigeonhole-seeding og verifikation",
                ),
                (
                    "Si un patrón de igual longitud que la ventana contiene como máximo d "
                    "mismatches, puede dividirse en d+1 bloques disjuntos y no vacíos. Si todos "
                    "los bloques contuvieran al menos un mismatch, existirían al menos d+1 "
                    "diferencias, contradiciendo el límite; por tanto, al menos una semilla debe "
                    "coincidir exactamente. Cada hit exacto se traduce a un inicio candidato "
                    "restando el offset de la semilla. Los candidatos fuera de límites se "
                    "descartan, los duplicados se unifican y la ventana completa se verifica con "
                    "distancia de Hamming. La garantía reduce generación de candidatos, pero no "
                    "elimina la verificación: una semilla exacta puede coexistir con demasiados "
                    "mismatches fuera de ella. Esta formulación asume sustituciones y ventanas de "
                    "igual longitud; los indels desplazan bloques y requieren alineamiento, seeds "
                    "espaciadas u otra estrategia. La elección de longitud de semillas afecta "
                    "rendimiento y número de candidatos, no la necesidad de verificar.",
                    "If an equal-length pattern and window differ in at most d positions, the "
                    "pattern can be split into d+1 disjoint nonempty blocks. If every block "
                    "contained at least one mismatch, there would be at least d+1 differences, "
                    "contradicting the limit; therefore at least one seed must match exactly. Each "
                    "exact hit is translated to a candidate start by subtracting the seed offset. "
                    "Out-of-bounds candidates are discarded, duplicates are merged, and the full "
                    "window is verified with Hamming distance. The guarantee reduces candidate "
                    "generation but does not remove verification: an exact seed may coexist with "
                    "too many mismatches outside it. This formulation assumes substitutions and "
                    "equal-length windows; indels shift blocks and require alignment, spaced seeds, "
                    "or another strategy. Seed length affects performance and candidate count, not "
                    "the need to verify.",
                    "Hvis et mønster og et vindue med samme længde højst har d mismatches, kan "
                    "mønstret opdeles i d+1 disjunkte, ikke-tomme blokke. Hvis hver blok indeholdt "
                    "mindst ét mismatch, ville der være mindst d+1 forskelle, hvilket modsiger "
                    "grænsen; derfor skal mindst ét seed matche eksakt. Hvert eksakt hit omregnes "
                    "til en kandidatstart ved at trække seedets offset fra. Kandidater uden for "
                    "grænser kasseres, dubletter samles, og hele vinduet verificeres med "
                    "Hamming-afstand. Garantien reducerer kandidatgenerering, men fjerner ikke "
                    "verifikation: et eksakt seed kan sameksistere med for mange mismatches uden "
                    "for seedet. Formuleringen antager substitutioner og vinduer med samme længde; "
                    "indels forskyder blokke og kræver alignment, spaced seeds eller en anden "
                    "strategi. Seedlængde påvirker ydeevne og kandidatantal, ikke behovet for "
                    "verifikation.",
                ),
                (
                    (
                        "Con d mismatches se necesitan d+1 bloques para la garantía.",
                        "The guarantee uses d+1 blocks for d mismatches.",
                        "Garantien bruger d+1 blokke for d mismatches.",
                    ),
                    (
                        "Un hit de semilla genera un candidato, no una coincidencia final.",
                        "A seed hit generates a candidate, not a final match.",
                        "Et seed-hit genererer en kandidat, ikke et endeligt match.",
                    ),
                    (
                        "Restar el offset convierte la posición del seed en inicio del patrón.",
                        "Subtracting the offset converts a seed position into a pattern start.",
                        "Fratrækning af offset omdanner seed-positionen til mønsterets start.",
                    ),
                    (
                        "La garantía de Hamming no cubre indels.",
                        "The Hamming guarantee does not cover indels.",
                        "Hamming-garantien dækker ikke indels.",
                    ),
                ),
            ),
        ),
        worked_examples=module.worked_examples
        + (
            example(
                "m06.bg.e01",
                (
                    "Generar candidatos con dos semillas",
                    "Generate candidates with two seeds",
                    "Generér kandidater med to seeds",
                ),
                (
                    "Busca un patrón permitiendo un mismatch. Divide el patrón en dos semillas, "
                    "convierte hits exactos en candidatos y verifica las ventanas completas.",
                    "Search a pattern allowing one mismatch. Split it into two seeds, convert "
                    "exact hits into candidates, and verify complete windows.",
                    "Søg efter et mønster med ét tilladt mismatch. Opdel det i to seeds, omdan "
                    "eksakte hits til kandidater og verificér komplette vinduer.",
                ),
                (
                    (
                        "Las semillas cubren el patrón sin solaparse.",
                        "The seeds cover the pattern without overlap.",
                        "Seeds dækker mønstret uden overlap.",
                    ),
                    (
                        "El offset de cada semilla se conserva.",
                        "Each seed offset is retained.",
                        "Hvert seed-offset bevares.",
                    ),
                    (
                        "La verificación final rechaza candidatos espurios.",
                        "Final verification rejects spurious candidates.",
                        "Den endelige verifikation afviser falske kandidater.",
                    ),
                ),
                "def hamming(left: str, right: str) -> int:\n"
                "    if len(left) != len(right):\n"
                "        raise ValueError('equal lengths required')\n"
                "    return sum(a != b for a, b in zip(left, right, strict=True))\n"
                "\n"
                "\n"
                "def seeds(pattern: str, parts: int) -> list[tuple[int, str]]:\n"
                "    if parts < 1 or parts > len(pattern):\n"
                "        raise ValueError('parts must create nonempty seeds')\n"
                "    return [\n"
                "        (\n"
                "            len(pattern) * index // parts,\n"
                "            pattern[\n"
                "                len(pattern) * index // parts\n"
                "                : len(pattern) * (index + 1) // parts\n"
                "            ],\n"
                "        )\n"
                "        for index in range(parts)\n"
                "    ]\n"
                "\n"
                "\n"
                "def mismatch_candidates(text: str, pattern: str, d: int) -> tuple[list[int], list[int]]:\n"
                "    if d < 0 or d >= len(pattern):\n"
                "        raise ValueError('d must satisfy 0 <= d < len(pattern)')\n"
                "    candidates: set[int] = set()\n"
                "    for offset, seed in seeds(pattern, d + 1):\n"
                "        for hit in range(len(text) - len(seed) + 1):\n"
                "            if text.startswith(seed, hit):\n"
                "                start = hit - offset\n"
                "                if 0 <= start <= len(text) - len(pattern):\n"
                "                    candidates.add(start)\n"
                "    ordered = sorted(candidates)\n"
                "    verified = [\n"
                "        start\n"
                "        for start in ordered\n"
                "        if hamming(text[start : start + len(pattern)], pattern) <= d\n"
                "    ]\n"
                "    return ordered, verified\n"
                "\n"
                "\n"
                "print(mismatch_candidates('ACGTTACGTAACTTT', 'ACGTA', 1))",
                "([0, 5, 10], [0, 5])",
                (
                    "Las posiciones 0 y 5 cumplen el límite. La posición 10 comparte una semilla "
                    "exacta, pero contiene dos mismatches y se elimina durante la verificación.",
                    "Positions 0 and 5 satisfy the limit. Position 10 shares an exact seed but "
                    "contains two mismatches and is removed during verification.",
                    "Position 0 og 5 opfylder grænsen. Position 10 deler et eksakt seed, men har "
                    "to mismatches og fjernes under verifikationen.",
                ),
            ),
        ),
        practice_exercises=module.practice_exercises
        + (
            practice(
                "m06.bg.p01",
                ActivityType.PIPELINE_DESIGN,
                (
                    "Diseña una búsqueda para un patrón de longitud 30 con hasta dos mismatches. "
                    "Especifica semillas, traducción de coordenadas, deduplicación, verificación y "
                    "el límite frente a indels.",
                    "Design a search for a length-30 pattern with at most two mismatches. Specify "
                    "seeds, coordinate translation, deduplication, verification, and the boundary "
                    "with indels.",
                    "Design en søgning efter et mønster med længde 30 og højst to mismatches. "
                    "Angiv seeds, koordinatoversættelse, deduplikering, verifikation og grænsen "
                    "over for indels.",
                ),
                (
                    (
                        "La garantía necesita tres bloques no vacíos.",
                        "The guarantee needs three nonempty blocks.",
                        "Garantien kræver tre ikke-tomme blokke.",
                    ),
                    (
                        "Una posición de seed no es todavía una posición de patrón.",
                        "A seed position is not yet a pattern position.",
                        "En seed-position er endnu ikke en mønsterposition.",
                    ),
                ),
                (
                    "Particionar el patrón en tres bloques disjuntos de aproximadamente diez "
                    "símbolos y conservar offsets 0, 10 y 20. Consultar cada seed exactamente en "
                    "el índice; para cada hit calcular start=hit-offset; descartar starts fuera del "
                    "texto; unificar candidatos repetidos; comparar la ventana completa de 30 "
                    "símbolos y aceptar sólo Hamming <=2. Registrar orientación y convención de "
                    "coordenadas. Esta garantía no cubre inserciones o deleciones, porque desplazan "
                    "los bloques; para ellas se necesita una estrategia de alineamiento o seeds "
                    "tolerantes a desplazamiento.",
                    "Partition the pattern into three disjoint blocks of about ten symbols and "
                    "retain offsets 0, 10, and 20. Query every seed exactly in the index; for each "
                    "hit compute start=hit-offset; discard starts outside the text; merge duplicate "
                    "candidates; compare the complete length-30 window and accept only Hamming <=2. "
                    "Record orientation and coordinate convention. This guarantee does not cover "
                    "insertions or deletions because they shift blocks; those require alignment or "
                    "shift-tolerant seeding.",
                    "Opdel mønstret i tre disjunkte blokke på cirka ti symboler og bevar offsets "
                    "0, 10 og 20. Forespørg hvert seed eksakt i indekset; beregn start=hit-offset "
                    "for hvert hit; kassér starts uden for teksten; saml dublerede kandidater; "
                    "sammenlign hele vinduet med længde 30 og acceptér kun Hamming <=2. Registrér "
                    "orientering og koordinatkonvention. Garantien dækker ikke insertioner eller "
                    "deletioner, fordi de forskyder blokkene; de kræver alignment eller "
                    "forskydningstolerante seeds.",
                ),
                (
                    "Diseño convierte una garantía combinatoria en un pipeline reproducible de "
                    "candidatos y verificación.",
                    "The design turns a combinatorial guarantee into a reproducible candidate-and-"
                    "verification pipeline.",
                    "Designet omsætter en kombinatorisk garanti til et reproducerbart kandidat- "
                    "og verifikationspipeline.",
                ),
            ),
        ),
        assessment_items=module.assessment_items
        + (
            objective_mcq(
                "dm847.m06.book.001",
                (
                    "¿Por qué d+1 semillas cubren una búsqueda con hasta d mismatches?",
                    "Why do d+1 seeds cover a search with at most d mismatches?",
                    "Hvorfor dækker d+1 seeds en søgning med højst d mismatches?",
                ),
                (
                    (
                        "pigeonhole",
                        (
                            "Al menos un bloque debe quedar sin mismatches.",
                            "At least one block must contain no mismatches.",
                            "Mindst én blok skal være uden mismatches.",
                        ),
                    ),
                    (
                        "all_exact",
                        (
                            "Todos los bloques deben coincidir exactamente.",
                            "Every block must match exactly.",
                            "Alle blokke skal matche eksakt.",
                        ),
                    ),
                    (
                        "indels",
                        (
                            "La división elimina automáticamente cualquier indel.",
                            "The split automatically removes every indel.",
                            "Opdelingen fjerner automatisk alle indels.",
                        ),
                    ),
                ),
                "pigeonhole",
                (
                    "Si cada uno de los d+1 bloques tuviera una diferencia, el total superaría d. "
                    "La conclusión sólo garantiza una semilla exacta y aún exige verificar el "
                    "patrón completo.",
                    "If each of the d+1 blocks had one difference, the total would exceed d. The "
                    "conclusion guarantees only one exact seed and still requires full-pattern "
                    "verification.",
                    "Hvis hver af de d+1 blokke havde én forskel, ville totalen overstige d. "
                    "Konklusionen garanterer kun ét eksakt seed og kræver stadig verifikation af "
                    "hele mønstret.",
                ),
            ),
        ),
    )
    return _with_source_basis(
        extended,
        ("sdu-dm847-active-2025", "compeau-pevzner-v2-ch09"),
    )


def apply_hmm_bwt_extensions(
    modules: tuple[LocalizedLearningModule, ...],
) -> tuple[LocalizedLearningModule, ...]:
    """Apply focused M05 and M06 extensions without changing other modules."""

    return tuple(
        _extend_hidden_markov_models(module)
        if module.module_id == "dm847.m05"
        else _extend_bwt_mapping(module)
        if module.module_id == "dm847.m06"
        else module
        for module in modules
    )


__all__ = [
    "apply_hmm_bwt_extensions",
    "update_hmm_bwt_audit",
]
