"""Focused source-grounded extensions for DM847 molecular foundations and OMICS learning."""

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


def update_omics_foundations_audit(
    audit: tuple[ModuleSourceAudit, ...],
) -> tuple[ModuleSourceAudit, ...]:
    """Mark M01 and M10 reviewed only after their focused extensions exist."""

    findings = {
        "dm847.m01": (
            "Existing coverage of molecular information flow, alphabets, ambiguity, strand, "
            "coordinates, regulation, bacterial genetics, phages, provenance, and biological "
            "question framing is consistent. The explicit transition from a biological question "
            "to a computational problem contract required one focused treatment."
        ),
        "dm847.m10": (
            "Existing coverage of OMICS matrices, preprocessing, unsupervised and supervised "
            "learning, leakage control, nested validation, metrics, interpretation, and "
            "reproducibility is consistent. Clustering objectives, initialization dependence, "
            "hard versus soft assignments, and stability required one explicit treatment."
        ),
    }
    changes = {
        "dm847.m01": (
            "Added an original trilingual computational-problem contract, deterministic exact-"
            "position example, specification exercise, and stable objective item."
        ),
        "dm847.m10": (
            "Added an original trilingual clustering-objective explanation, deterministic Lloyd "
            "restart comparison, interpretation exercise, and stable objective item."
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


def _extend_molecular_information(
    module: LocalizedLearningModule,
) -> LocalizedLearningModule:
    """Add explicit computational problem contracts to M01."""

    extended = replace(
        module,
        objectives=module.objectives
        + (
            objective(
                "m01.bg.o1",
                (
                    "Convertir una pregunta biológica en un contrato computacional con entradas, "
                    "salidas, supuestos, casos límite y validación explícitos.",
                    "Convert a biological question into a computational contract with explicit "
                    "inputs, outputs, assumptions, edge cases, and validation.",
                    "Omsætte et biologisk spørgsmål til en beregningskontrakt med eksplicitte "
                    "input, output, antagelser, grænsetilfælde og validering.",
                ),
            ),
        ),
        concepts=module.concepts
        + (
            concept(
                "computational-problem-contracts",
                (
                    "De la pregunta biológica al contrato computacional",
                    "From a biological question to a computational contract",
                    "Fra biologisk spørgsmål til beregningskontrakt",
                ),
                (
                    "Una pregunta como «¿dónde aparece este motivo?» todavía no define un "
                    "problema ejecutable. El contrato debe declarar qué cadenas se reciben, su "
                    "alfabeto y orientación, si se normalizan espacios o minúsculas, si se busca "
                    "también el complemento inverso, cómo se tratan símbolos ambiguos y si se "
                    "permiten solapamientos. La salida debe fijar tipo, orden y convención de "
                    "coordenadas. También deben definirse el patrón vacío, las entradas más cortas "
                    "que el patrón, los caracteres inválidos y las secuencias palindrómicas. La "
                    "validación combina ejemplos pequeños con respuesta conocida, invariantes y "
                    "casos límite. Formalizar entrada y salida no demuestra relevancia biológica; "
                    "separa una operación reproducible de la interpretación posterior.",
                    "A question such as 'where does this motif occur?' does not yet define an "
                    "executable problem. The contract must state which strings are received, their "
                    "alphabet and orientation, whether whitespace or case is normalized, whether "
                    "the reverse complement is also searched, how ambiguous symbols are handled, "
                    "and whether overlaps are allowed. The output must fix type, ordering, and "
                    "coordinate convention. Empty patterns, inputs shorter than the pattern, "
                    "invalid symbols, and palindromic sequences also need explicit behavior. "
                    "Validation combines small examples with known answers, invariants, and edge "
                    "cases. Formalizing input and output does not establish biological relevance; "
                    "it separates a reproducible operation from later interpretation.",
                    "Et spørgsmål som 'hvor forekommer dette motiv?' definerer endnu ikke et "
                    "eksekverbart problem. Kontrakten skal angive hvilke strenge der modtages, "
                    "deres alfabet og orientering, om mellemrum eller bogstavstørrelse normaliseres, "
                    "om det omvendte komplement også søges, hvordan tvetydige symboler håndteres, "
                    "og om overlap tillades. Output skal fastlægge type, rækkefølge og "
                    "koordinatkonvention. Tomme mønstre, input kortere end mønstret, ugyldige "
                    "symboler og palindromiske sekvenser kræver også eksplicit adfærd. Validering "
                    "kombinerer små eksempler med kendte svar, invariants og grænsetilfælde. En "
                    "formel input-output-definition beviser ikke biologisk relevans; den adskiller "
                    "en reproducerbar operation fra den efterfølgende fortolkning.",
                ),
                (
                    (
                        "Entrada y salida deben ser verificables antes de elegir un algoritmo.",
                        "Inputs and outputs should be testable before choosing an algorithm.",
                        "Input og output bør kunne testes før valg af algoritme.",
                    ),
                    (
                        "Hebra, coordenadas, solapamientos y ambigüedad forman parte del contrato.",
                        "Strand, coordinates, overlaps, and ambiguity are part of the contract.",
                        "Streng, koordinater, overlap og tvetydighed er en del af kontrakten.",
                    ),
                    (
                        "Los casos límite no deben depender de comportamiento accidental del código.",
                        "Edge cases should not depend on accidental code behavior.",
                        "Grænsetilfælde bør ikke afhænge af tilfældig kodeadfærd.",
                    ),
                    (
                        "Un resultado computacional correcto todavía requiere interpretación biológica.",
                        "A correct computational result still requires biological interpretation.",
                        "Et korrekt beregningsresultat kræver stadig biologisk fortolkning.",
                    ),
                ),
            ),
        ),
        worked_examples=module.worked_examples
        + (
            example(
                "m01.bg.e01",
                (
                    "Contrato exacto con solapamientos",
                    "An exact contract with overlaps",
                    "En eksakt kontrakt med overlap",
                ),
                (
                    "Implementa el contrato: ADN canónico en la hebra suministrada, patrón no "
                    "vacío, posiciones 0-based, orden ascendente y solapamientos permitidos.",
                    "Implement the contract: canonical DNA on the supplied strand, a nonempty "
                    "pattern, zero-based positions, ascending order, and overlaps allowed.",
                    "Implementér kontrakten: kanonisk DNA på den leverede streng, et ikke-tomt "
                    "mønster, nulbaserede positioner, stigende rækkefølge og tilladte overlap.",
                ),
                (
                    (
                        "La normalización elimina espacios y unifica mayúsculas.",
                        "Normalization removes whitespace and unifies case.",
                        "Normalisering fjerner mellemrum og ensretter bogstavstørrelse.",
                    ),
                    (
                        "El rango incluye cada ventana completa, también las solapadas.",
                        "The range includes every complete window, including overlapping ones.",
                        "Intervallet omfatter alle komplette vinduer, også overlappende vinduer.",
                    ),
                    (
                        "El complemento inverso queda fuera porque el contrato no lo solicita.",
                        "The reverse complement is excluded because the contract does not request it.",
                        "Det omvendte komplement er udeladt, fordi kontrakten ikke kræver det.",
                    ),
                ),
                "def exact_positions(raw_text: str, raw_pattern: str) -> list[int]:\n"
                "    text = ''.join(raw_text.split()).upper()\n"
                "    pattern = ''.join(raw_pattern.split()).upper()\n"
                "    alphabet = set('ACGT')\n"
                "    if not pattern:\n"
                "        raise ValueError('pattern must be nonempty')\n"
                "    if set(text) - alphabet or set(pattern) - alphabet:\n"
                "        raise ValueError('canonical DNA required')\n"
                "    width = len(pattern)\n"
                "    return [\n"
                "        start\n"
                "        for start in range(len(text) - width + 1)\n"
                "        if text[start : start + width] == pattern\n"
                "    ]\n"
                "\n"
                "\n"
                "print(exact_positions('ATATAT', 'ATAT'))",
                "[0, 2]",
                (
                    "Las dos coincidencias comparten posiciones. El resultado es correcto para "
                    "este contrato concreto, no para una búsqueda automática en ambas hebras.",
                    "The two matches share positions. The result is correct for this specific "
                    "contract, not for an automatic search on both strands.",
                    "De to matches deler positioner. Resultatet er korrekt for denne konkrete "
                    "kontrakt, ikke for en automatisk søgning på begge strenge.",
                ),
            ),
        ),
        practice_exercises=module.practice_exercises
        + (
            practice(
                "m01.bg.p01",
                ActivityType.PIPELINE_DESIGN,
                (
                    "La pregunta «¿está enriquecido un motivo cerca de genes?» es demasiado vaga. "
                    "Redáctala como un contrato computacional reproducible antes de proponer un "
                    "algoritmo.",
                    "The question 'is a motif enriched near genes?' is too vague. Rewrite it as a "
                    "reproducible computational contract before proposing an algorithm.",
                    "Spørgsmålet 'er et motiv beriget nær gener?' er for uklart. Omskriv det som "
                    "en reproducerbar beregningskontrakt før en algoritme foreslås.",
                ),
                (
                    (
                        "Define organismo, ensamblaje, genes y ventana genómica.",
                        "Define organism, assembly, genes, and genomic window.",
                        "Definér organisme, assembly, gener og genomisk vindue.",
                    ),
                    (
                        "Separa el conteo de motivos del modelo nulo de enriquecimiento.",
                        "Separate motif counting from the enrichment null model.",
                        "Adskil motivoptælling fra berigelsens nulmodel.",
                    ),
                ),
                (
                    "Especificar: ensamblaje y versión de anotación; conjunto de genes y regla de "
                    "inclusión; intervalo relativo al TSS con convención de coordenadas; motivo, "
                    "alfabeto, mismatch y política de ambas hebras; tratamiento de solapamientos y "
                    "regiones ambiguas; salida como conteos y tasa por base; conjunto de fondo o "
                    "permutación que conserve longitud y composición; estadístico, corrección por "
                    "multiplicidad y casos de prueba. Después se elige el algoritmo y se interpreta "
                    "la asociación sin convertirla automáticamente en causalidad regulatoria.",
                    "Specify: assembly and annotation release; gene set and inclusion rule; region "
                    "relative to the TSS with coordinate convention; motif, alphabet, mismatch, and "
                    "both-strand policy; handling of overlaps and ambiguous regions; output as "
                    "counts and rate per base; a background set or permutation preserving length "
                    "and composition; statistic, multiplicity correction, and test cases. Only then "
                    "choose the algorithm and interpret association without turning it automatically "
                    "into regulatory causality.",
                    "Specificér: assembly og annotationsversion; gensæt og inklusionsregel; region "
                    "relativt til TSS med koordinatkonvention; motiv, alfabet, mismatch og politik "
                    "for begge strenge; håndtering af overlap og tvetydige regioner; output som "
                    "tællinger og rate pr. base; baggrundssæt eller permutation, der bevarer længde "
                    "og sammensætning; statistik, multiplicitetskorrektion og testcases. Først "
                    "derefter vælges algoritmen, og associationen fortolkes uden automatisk at blive "
                    "gjort til regulatorisk kausalitet.",
                ),
                (
                    "El contrato distingue representación, operación, comparación nula y alcance "
                    "de la conclusión.",
                    "The contract separates representation, operation, null comparison, and the "
                    "scope of the conclusion.",
                    "Kontrakten adskiller repræsentation, operation, nulsammenligning og "
                    "konklusionens rækkevidde.",
                ),
            ),
        ),
        assessment_items=module.assessment_items
        + (
            objective_mcq(
                "dm847.m01.book.001",
                (
                    "¿Qué debe fijarse antes de implementar una búsqueda de motivos reproducible?",
                    "What should be fixed before implementing a reproducible motif search?",
                    "Hvad bør fastlægges før implementering af en reproducerbar motivsøgning?",
                ),
                (
                    (
                        "contract",
                        (
                            "Entradas, orientación, coordenadas, casos límite y salida.",
                            "Inputs, orientation, coordinates, edge cases, and output.",
                            "Input, orientering, koordinater, grænsetilfælde og output.",
                        ),
                    ),
                    (
                        "algorithm_first",
                        (
                            "Sólo el algoritmo más rápido disponible.",
                            "Only the fastest available algorithm.",
                            "Kun den hurtigste tilgængelige algoritme.",
                        ),
                    ),
                    (
                        "interpretation",
                        (
                            "La función biológica definitiva del motivo.",
                            "The motif's definitive biological function.",
                            "Motivets endelige biologiske funktion.",
                        ),
                    ),
                ),
                "contract",
                (
                    "Una especificación verificable precede a la implementación; la función "
                    "biológica requiere evidencia adicional.",
                    "A testable specification precedes implementation; biological function "
                    "requires additional evidence.",
                    "En testbar specifikation går forud for implementering; biologisk funktion "
                    "kræver yderligere evidens.",
                ),
            ),
        ),
    )
    return _with_source_basis(
        extended,
        ("sdu-dm847-active-2025", "compeau-pevzner-v1-ch01"),
    )


def _extend_omics_learning(
    module: LocalizedLearningModule,
) -> LocalizedLearningModule:
    """Add clustering objectives, restart sensitivity, and stability to M10."""

    extended = replace(
        module,
        objectives=module.objectives
        + (
            objective(
                "m10.bg.o1",
                (
                    "Comparar clustering hard y soft, interpretar la distorsión y evaluar "
                    "dependencia de inicialización y estabilidad.",
                    "Compare hard and soft clustering, interpret distortion, and evaluate "
                    "initialization dependence and stability.",
                    "Sammenligne hard og soft clustering, fortolke distortion og evaluere "
                    "afhængighed af initialisering og stabilitet.",
                ),
            ),
        ),
        concepts=module.concepts
        + (
            concept(
                "clustering-objectives-initialization-and-stability",
                (
                    "Objetivos, inicialización y estabilidad del clustering",
                    "Clustering objectives, initialization, and stability",
                    "Clusteringmål, initialisering og stabilitet",
                ),
                (
                    "En k-means hard, cada muestra se asigna al centro más cercano y los centros "
                    "se actualizan como medias. La distorsión resume la distancia cuadrática dentro "
                    "de los clusters para el espacio y escalado elegidos. Lloyd alterna asignación "
                    "y actualización y no aumenta esa función objetivo, pero puede converger a "
                    "óptimos locales distintos según la inicialización. Por eso se ejecutan varios "
                    "reinicios, se conserva el mejor objetivo comparable y se reporta su "
                    "variabilidad. En clustering soft, cada muestra distribuye responsabilidades "
                    "que suman uno entre centros; un parámetro de rigidez controla cuán cercanas "
                    "son las asignaciones a decisiones hard. Clustering jerárquico depende de la "
                    "distancia y del linkage, no de un centroide único. En OMICS, transformación, "
                    "filtrado, escalado, selección de features y batch pueden cambiar por completo "
                    "la geometría. Un objetivo bajo no demuestra subtipos verdaderos: deben "
                    "evaluarse estabilidad bajo remuestreo y perturbación, replicación externa y "
                    "coherencia con la pregunta biológica.",
                    "In hard k-means, each sample is assigned to the nearest center and centers are "
                    "updated as means. Distortion summarizes squared within-cluster distance for "
                    "the chosen space and scaling. Lloyd alternates assignment and update and does "
                    "not increase this objective, but it may converge to different local optima "
                    "depending on initialization. Multiple restarts are therefore run, the best "
                    "comparable objective is retained, and variability is reported. In soft "
                    "clustering, each sample distributes responsibilities that sum to one across "
                    "centers; a stiffness parameter controls how close assignments are to hard "
                    "decisions. Hierarchical clustering depends on distance and linkage rather than "
                    "one centroid objective. In OMICS, transformation, filtering, scaling, feature "
                    "selection, and batch can completely alter geometry. A low objective does not "
                    "prove true subtypes: stability under resampling and perturbation, external "
                    "replication, and coherence with the biological question must be assessed.",
                    "I hard k-means tildeles hver prøve det nærmeste center, og centre opdateres som "
                    "middelværdier. Distortion opsummerer den kvadrerede afstand inden for clusters "
                    "for det valgte rum og den valgte skalering. Lloyd skifter mellem tildeling og "
                    "opdatering og øger ikke dette mål, men kan konvergere til forskellige lokale "
                    "optima afhængigt af initialiseringen. Derfor køres flere genstarter, det bedste "
                    "sammenlignelige mål bevares, og variationen rapporteres. I soft clustering "
                    "fordeler hver prøve ansvar, der summerer til én på tværs af centre; en "
                    "stivhedsparameter styrer, hvor tæt tildelingerne er på hard beslutninger. "
                    "Hierarkisk clustering afhænger af afstand og linkage frem for ét centroidmål. "
                    "I OMICS kan transformation, filtrering, skalering, feature-selektion og batch "
                    "ændre geometrien fuldstændigt. Et lavt mål beviser ikke sande subtyper: "
                    "stabilitet under resampling og perturbation, ekstern replikation og sammenhæng "
                    "med det biologiske spørgsmål skal vurderes.",
                ),
                (
                    (
                        "La distorsión sólo es comparable bajo el mismo preprocesamiento y k.",
                        "Distortion is comparable only under the same preprocessing and k.",
                        "Distortion kan kun sammenlignes under samme preprocessing og k.",
                    ),
                    (
                        "Lloyd es monótono para su objetivo, no globalmente óptimo.",
                        "Lloyd is monotonic for its objective, not globally optimal.",
                        "Lloyd er monoton for sit mål, ikke globalt optimal.",
                    ),
                    (
                        "Las responsabilidades soft suman uno por muestra.",
                        "Soft responsibilities sum to one per sample.",
                        "Soft ansvar summerer til én pr. prøve.",
                    ),
                    (
                        "Estabilidad y replicación son diferentes de una buena visualización.",
                        "Stability and replication differ from an attractive visualization.",
                        "Stabilitet og replikation er noget andet end en flot visualisering.",
                    ),
                ),
            ),
        ),
        worked_examples=module.worked_examples
        + (
            example(
                "m10.bg.e01",
                (
                    "Dos reinicios de Lloyd",
                    "Two Lloyd restarts",
                    "To Lloyd-genstarter",
                ),
                (
                    "Ejecuta k-means unidimensional con dos inicializaciones y compara los centros "
                    "finales y la distorsión.",
                    "Run one-dimensional k-means from two initializations and compare final centers "
                    "and distortion.",
                    "Kør endimensional k-means fra to initialiseringer og sammenlign endelige "
                    "centre og distortion.",
                ),
                (
                    (
                        "Los empates se resuelven por el índice de centro para reproducibilidad.",
                        "Ties are resolved by center index for reproducibility.",
                        "Ligheder afgøres efter centerindeks for reproducerbarhed.",
                    ),
                    (
                        "Un cluster vacío conserva temporalmente su centro anterior.",
                        "An empty cluster temporarily retains its previous center.",
                        "Et tomt cluster bevarer midlertidigt sit tidligere center.",
                    ),
                    (
                        "La distorsión se calcula después de la convergencia.",
                        "Distortion is computed after convergence.",
                        "Distortion beregnes efter konvergens.",
                    ),
                ),
                "def lloyd_1d(\n"
                "    points: list[float], initial_centers: list[float], max_iter: int = 100\n"
                ") -> tuple[tuple[float, ...], float]:\n"
                "    centers = [float(value) for value in initial_centers]\n"
                "    for _ in range(max_iter):\n"
                "        assignments = [\n"
                "            min(\n"
                "                range(len(centers)),\n"
                "                key=lambda index: (abs(point - centers[index]), index),\n"
                "            )\n"
                "            for point in points\n"
                "        ]\n"
                "        updated = []\n"
                "        for index, center in enumerate(centers):\n"
                "            members = [\n"
                "                point\n"
                "                for point, assignment in zip(points, assignments, strict=True)\n"
                "                if assignment == index\n"
                "            ]\n"
                "            updated.append(sum(members) / len(members) if members else center)\n"
                "        if updated == centers:\n"
                "            break\n"
                "        centers = updated\n"
                "    assignments = [\n"
                "        min(\n"
                "            range(len(centers)),\n"
                "            key=lambda index: (abs(point - centers[index]), index),\n"
                "        )\n"
                "        for point in points\n"
                "    ]\n"
                "    distortion = sum(\n"
                "        (point - centers[assignment]) ** 2\n"
                "        for point, assignment in zip(points, assignments, strict=True)\n"
                "    ) / len(points)\n"
                "    return tuple(round(value, 3) for value in centers), round(distortion, 3)\n"
                "\n"
                "\n"
                "points = [0.0, 1.0, 2.0, 9.0, 10.0, 11.0, 20.0]\n"
                "print(\n"
                "    {\n"
                "        'left_start': lloyd_1d(points, [0.0, 1.0]),\n"
                "        'right_start': lloyd_1d(points, [9.0, 20.0]),\n"
                "    }\n"
                ")",
                "{'left_start': ((1.0, 12.5), 11.286), 'right_start': ((5.5, 20.0), 17.929)}",
                (
                    "Los reinicios convergen a soluciones diferentes. Bajo el mismo espacio y k, "
                    "la primera tiene menor distorsión, pero todavía requiere evaluación de "
                    "estabilidad y significado biológico.",
                    "The restarts converge to different solutions. Under the same space and k, the "
                    "first has lower distortion, but stability and biological meaning still need "
                    "evaluation.",
                    "Genstarterne konvergerer til forskellige løsninger. Under samme rum og k har "
                    "den første lavere distortion, men stabilitet og biologisk betydning skal stadig "
                    "evalueres.",
                ),
            ),
        ),
        practice_exercises=module.practice_exercises
        + (
            practice(
                "m10.bg.p01",
                ActivityType.DATA_INTERPRETATION,
                (
                    "Veinte reinicios de k-means producen dos soluciones frecuentes con "
                    "distorsiones similares, pero los clusters cambian al retirar un 5% de las "
                    "muestras. Interpreta y diseña el siguiente análisis.",
                    "Twenty k-means restarts produce two frequent solutions with similar "
                    "distortions, but clusters change after removing 5% of samples. Interpret this "
                    "and design the next analysis.",
                    "Tyve k-means-genstarter giver to hyppige løsninger med lignende distortion, "
                    "men clusters ændres, når 5 % af prøverne fjernes. Fortolk dette og design den "
                    "næste analyse.",
                ),
                (
                    (
                        "Diferencia óptimo local de estabilidad de la partición.",
                        "Separate local optimum from partition stability.",
                        "Adskil lokalt optimum fra partitionens stabilitet.",
                    ),
                    (
                        "Revisa preprocesamiento, batch, k y métrica de distancia.",
                        "Review preprocessing, batch, k, and distance metric.",
                        "Gennemgå preprocessing, batch, k og afstandsmål.",
                    ),
                ),
                (
                    "No declarar subtipos robustos. Registrar distribución de objetivos por "
                    "reinicio; cuantificar concordancia de asignaciones; repetir con remuestreo de "
                    "muestras y features; comprobar sensibilidad a transformación, escalado, k, "
                    "distancia y batch; comparar con clustering jerárquico o soft cuando responda a "
                    "la pregunta; buscar replicación externa. La solución de menor distorsión puede "
                    "ser el óptimo numérico preferido bajo un pipeline fijo, pero la inestabilidad "
                    "indica que la estructura inferida no es todavía una conclusión biológica "
                    "robusta.",
                    "Do not declare robust subtypes. Record the objective distribution across "
                    "restarts; quantify assignment agreement; repeat with sample and feature "
                    "resampling; test sensitivity to transformation, scaling, k, distance, and "
                    "batch; compare with hierarchical or soft clustering when aligned with the "
                    "question; seek external replication. The lowest-distortion solution may be the "
                    "preferred numerical optimum under a fixed pipeline, but instability means the "
                    "inferred structure is not yet a robust biological conclusion.",
                    "Erklær ikke robuste subtyper. Registrér fordelingen af mål på tværs af "
                    "genstarter; kvantificér enighed i tildelinger; gentag med resampling af prøver "
                    "og features; test følsomhed over for transformation, skalering, k, afstand og "
                    "batch; sammenlign med hierarkisk eller soft clustering, når det passer til "
                    "spørgsmålet; søg ekstern replikation. Løsningen med lavest distortion kan være "
                    "det foretrukne numeriske optimum under en fast pipeline, men ustabilitet betyder, "
                    "at den infererede struktur endnu ikke er en robust biologisk konklusion.",
                ),
                (
                    "Un objetivo optimizado describe el algoritmo; estabilidad y replicación "
                    "evalúan la afirmación científica.",
                    "An optimized objective describes the algorithm; stability and replication "
                    "evaluate the scientific claim.",
                    "Et optimeret mål beskriver algoritmen; stabilitet og replikation evaluerer den "
                    "videnskabelige påstand.",
                ),
            ),
        ),
        assessment_items=module.assessment_items
        + (
            objective_mcq(
                "dm847.m10.book.001",
                (
                    "¿Qué concluye correctamente una menor distorsión tras varios reinicios?",
                    "What is correctly concluded from lower distortion across several restarts?",
                    "Hvad kan korrekt konkluderes fra lavere distortion på tværs af flere genstarter?",
                ),
                (
                    (
                        "objective",
                        (
                            "Es una mejor solución para ese objetivo, k y preprocesamiento.",
                            "It is a better solution for that objective, k, and preprocessing.",
                            "Det er en bedre løsning for dette mål, k og preprocessing.",
                        ),
                    ),
                    (
                        "truth",
                        (
                            "Demuestra que los clusters son subtipos biológicos verdaderos.",
                            "It proves that clusters are true biological subtypes.",
                            "Det beviser, at clusters er sande biologiske subtyper.",
                        ),
                    ),
                    (
                        "stable",
                        (
                            "Garantiza estabilidad frente a remuestreo y batch.",
                            "It guarantees stability under resampling and batch.",
                            "Det garanterer stabilitet under resampling og batch.",
                        ),
                    ),
                ),
                "objective",
                (
                    "La distorsión compara soluciones bajo un contrato fijo; no sustituye pruebas "
                    "de estabilidad, replicación o interpretación biológica.",
                    "Distortion compares solutions under a fixed contract; it does not replace "
                    "stability, replication, or biological interpretation.",
                    "Distortion sammenligner løsninger under en fast kontrakt; den erstatter ikke "
                    "stabilitet, replikation eller biologisk fortolkning.",
                ),
            ),
        ),
    )
    return _with_source_basis(
        extended,
        ("sdu-dm847-active-2025", "compeau-pevzner-v2-ch08"),
    )


def apply_omics_foundations_extensions(
    modules: tuple[LocalizedLearningModule, ...],
) -> tuple[LocalizedLearningModule, ...]:
    """Apply focused M01 and M10 extensions without changing other modules."""

    return tuple(
        _extend_molecular_information(module)
        if module.module_id == "dm847.m01"
        else _extend_omics_learning(module)
        if module.module_id == "dm847.m10"
        else module
        for module in modules
    )


__all__ = [
    "apply_omics_foundations_extensions",
    "update_omics_foundations_audit",
]
