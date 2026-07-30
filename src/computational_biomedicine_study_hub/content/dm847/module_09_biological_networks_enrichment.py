"""DM847 module 9: biological networks, enrichment, and propagation."""

from __future__ import annotations

from ...i18n import AppLocale
from ..localized_models import LocalizedLearningModule
from ..models import AssessmentItem, LearningModule
from .standard import StandardModuleSpec, build_module, build_question_bank, materialize_bank

_SPEC = StandardModuleSpec(
    module_id="dm847.m09",
    title=(
        "Redes biológicas, enriquecimiento y propagación",
        "Biological networks, enrichment, and propagation",
        "Biologiske netværk, berigelse og propagation",
    ),
    summary=(
        "Representa redes moleculares con semántica explícita, evalúa enriquecimiento de conjuntos, controla multiplicidad y aplica métodos de propagación y módulos con nulos que respetan la estructura.",
        "Represent molecular networks with explicit semantics, evaluate gene-set enrichment, control multiplicity, and apply propagation and module methods using structure-aware null models.",
        "Repræsentér molekylære netværk med eksplicit semantik, evaluér gensætberigelse, kontrollér multiplicitet og anvend propagation- og modulmetoder med strukturbevidste nulmodeller.",
    ),
    objectives=(
        (
            "m09.o1",
            (
                "Distinguir nodos, aristas, dirección, peso y capas de evidencia.",
                "Distinguish nodes, edges, direction, weight, and evidence layers.",
                "Skelne mellem noder, kanter, retning, vægt og evidenslag.",
            ),
        ),
        (
            "m09.o2",
            (
                "Interpretar grado, componentes, caminos y centralidad sin sobreafirmar función.",
                "Interpret degree, components, paths, and centrality without overclaiming function.",
                "Fortolke grad, komponenter, stier og centralitet uden at overfortolke funktion.",
            ),
        ),
        (
            "m09.o3",
            (
                "Formular enriquecimiento mediante el modelo hipergeométrico.",
                "Formulate enrichment through the hypergeometric model.",
                "Formulere berigelse gennem den hypergeometriske model.",
            ),
        ),
        (
            "m09.o4",
            (
                "Definir correctamente universo, anotaciones y corrección por múltiples pruebas.",
                "Correctly define universe, annotations, and multiple-testing correction.",
                "Definere univers, annotationer og korrektion for multiple tests korrekt.",
            ),
        ),
        (
            "m09.o5",
            (
                "Aplicar propagación, random walk y detección de módulos con parámetros explícitos.",
                "Apply propagation, random walks, and module detection with explicit parameters.",
                "Anvende propagation, random walks og moduldetektion med eksplicitte parametre.",
            ),
        ),
        (
            "m09.o6",
            (
                "Diseñar nulos que conserven grado, anotación y sesgos de selección.",
                "Design null models preserving degree, annotation, and selection biases.",
                "Designe nulmodeller, der bevarer grad, annotation og selektionsbias.",
            ),
        ),
    ),
    concepts=(
        (
            "network-semantics",
            ("Semántica de una red", "Network semantics", "Netværkssemantik"),
            (
                "Una red biológica no es sólo una matriz de adyacencia. Los nodos pueden representar genes, proteínas, metabolitos, fenotipos o muestras; las aristas pueden indicar unión física, regulación, coexpresión, similitud o inferencia. Dirección, signo, peso, condición, especie, fuente y nivel de evidencia determinan qué operaciones e interpretaciones son válidas.",
                "A biological network is more than an adjacency matrix. Nodes may represent genes, proteins, metabolites, phenotypes, or samples; edges may encode physical binding, regulation, co-expression, similarity, or inference. Direction, sign, weight, condition, species, source, and evidence level determine which operations and interpretations are valid.",
                "Et biologisk netværk er mere end en nabomatrix. Noder kan repræsentere gener, proteiner, metabolitter, fænotyper eller prøver; kanter kan kode fysisk binding, regulering, co-ekspression, lighed eller inferens. Retning, fortegn, vægt, betingelse, art, kilde og evidensniveau bestemmer, hvilke operationer og fortolkninger der er gyldige.",
            ),
            (
                (
                    "Combinar tipos de arista sin etiquetarlos destruye semántica.",
                    "Combining edge types without labels destroys semantics.",
                    "Kombination af kanttyper uden labels ødelægger semantik.",
                ),
                (
                    "Una arista inferida no equivale a una interacción física observada.",
                    "An inferred edge is not equivalent to an observed physical interaction.",
                    "En infereret kant er ikke det samme som en observeret fysisk interaktion.",
                ),
            ),
        ),
        (
            "topology",
            ("Topología y centralidad", "Topology and centrality", "Topologi og centralitet"),
            (
                "El grado cuenta vecinos; betweenness resume participación en caminos mínimos; closeness depende de distancias y conectividad; PageRank pondera importancia por vecinos. Estas métricas describen una representación y son sensibles a cobertura, sesgo de publicación, reglas de proyección y tratamiento de componentes desconectados. Centralidad no implica esencialidad ni causalidad.",
                "Degree counts neighbors; betweenness summarizes participation in shortest paths; closeness depends on distances and connectivity; PageRank weights importance through neighbors. These metrics describe a representation and are sensitive to coverage, publication bias, projection rules, and disconnected components. Centrality does not imply essentiality or causality.",
                "Grad tæller naboer; betweenness opsummerer deltagelse i korteste stier; closeness afhænger af afstande og konnektivitet; PageRank vægter betydning gennem naboer. Disse mål beskriver en repræsentation og er følsomme over for dækning, publikationsbias, projektionsregler og afkoblede komponenter. Centralitet indebærer ikke essentialitet eller kausalitet.",
            ),
            (
                (
                    "Comparar centralidades exige la misma definición de red.",
                    "Comparing centralities requires the same network definition.",
                    "Sammenligning af centraliteter kræver samme netværksdefinition.",
                ),
                (
                    "Los hubs pueden reflejar mayor estudio experimental.",
                    "Hubs may reflect greater experimental study.",
                    "Hubs kan afspejle større eksperimentel undersøgelse.",
                ),
            ),
        ),
        (
            "ora",
            (
                "Enriquecimiento sobrerrepresentado",
                "Over-representation analysis",
                "Overrepræsentationsanalyse",
            ),
            (
                "El análisis hipergeométrico compara la superposición observada entre una lista seleccionada y un conjunto funcional con la distribución esperada al extraer sin reemplazo desde un universo. Requiere tamaños N del universo, K anotados, n seleccionados y k superpuestos. La hipótesis nula supone selección intercambiable dentro del universo definido.",
                "Hypergeometric analysis compares observed overlap between a selected list and a functional set with the distribution expected from sampling without replacement from a universe. It requires universe size N, annotated count K, selected count n, and overlap k. The null assumes exchangeable selection within the defined universe.",
                "Hypergeometrisk analyse sammenligner det observerede overlap mellem en valgt liste og et funktionelt sæt med fordelingen forventet ved udtræk uden tilbagelægning fra et univers. Den kræver universstørrelse N, antal annoterede K, antal valgte n og overlap k. Nulhypotesen antager udskiftelig selektion inden for det definerede univers.",
            ),
            (
                (
                    "El universo debe ser el conjunto realmente detectable o evaluado.",
                    "The universe should be the set actually detectable or evaluated.",
                    "Universet bør være det sæt, der faktisk kunne detekteres eller evalueres.",
                ),
                (
                    "Un p-valor pequeño no mide tamaño de efecto.",
                    "A small p-value does not measure effect size.",
                    "En lille p-værdi måler ikke effektstørrelse.",
                ),
            ),
        ),
        (
            "multiplicity-redundancy",
            (
                "Multiplicidad y redundancia",
                "Multiplicity and redundancy",
                "Multiplicitet og redundans",
            ),
            (
                "Probar cientos o miles de conjuntos exige control de FDR u otra familia de error. Los conjuntos comparten genes y relaciones jerárquicas, por lo que los tests no son independientes y los resultados suelen ser redundantes. Reportar odds ratio, proporción de cobertura, genes responsables y estructura entre términos mejora la interpretación.",
                "Testing hundreds or thousands of sets requires FDR or another error-family control. Sets share genes and hierarchical relationships, so tests are dependent and results are often redundant. Reporting odds ratio, coverage proportion, driving genes, and term structure improves interpretation.",
                "Test af hundredvis eller tusindvis af sæt kræver FDR eller anden kontrol af fejlfamilie. Sæt deler gener og hierarkiske relationer, så tests er afhængige, og resultater er ofte redundante. Rapportering af odds ratio, dækningsandel, drivende gener og termstruktur forbedrer fortolkningen.",
            ),
            (
                (
                    "FDR controla una expectativa de descubrimientos falsos.",
                    "FDR controls an expectation of false discoveries.",
                    "FDR kontrollerer en forventning om falske fund.",
                ),
                (
                    "Términos similares no constituyen hallazgos independientes.",
                    "Similar terms are not independent findings.",
                    "Lignende termer er ikke uafhængige fund.",
                ),
            ),
        ),
        (
            "propagation-modules",
            ("Propagación y módulos", "Propagation and modules", "Propagation og moduler"),
            (
                "La propagación difunde puntuaciones iniciales a través de aristas normalizadas. Random walk with restart equilibra difusión y retorno a semillas mediante un parámetro de reinicio. Los algoritmos de comunidades buscan grupos densos, pero la resolución, pesos, signo y aleatoriedad afectan los módulos. Un módulo computacional no es automáticamente una vía biológica.",
                "Propagation diffuses initial scores through normalized edges. Random walk with restart balances diffusion and return to seeds through a restart parameter. Community algorithms seek dense groups, but resolution, weights, sign, and randomness affect modules. A computational module is not automatically a biological pathway.",
                "Propagation spreder initiale scores gennem normaliserede kanter. Random walk with restart balancerer diffusion og tilbagevenden til seeds gennem en restartparameter. Community-algoritmer søger tætte grupper, men opløsning, vægte, fortegn og tilfældighed påvirker moduler. Et beregningsmodul er ikke automatisk en biologisk pathway.",
            ),
            (
                (
                    "La normalización evita que grado domine mecánicamente.",
                    "Normalization prevents degree from mechanically dominating.",
                    "Normalisering forhindrer, at grad mekanisk dominerer.",
                ),
                (
                    "La estabilidad de módulos debe evaluarse entre reinicios y perturbaciones.",
                    "Module stability should be evaluated across restarts and perturbations.",
                    "Modulstabilitet bør evalueres mellem genstarter og perturbationer.",
                ),
            ),
        ),
        (
            "network-nulls",
            (
                "Nulos y validación de red",
                "Network nulls and validation",
                "Netværksnulmodeller og validering",
            ),
            (
                "Permutar etiquetas de nodo prueba asociación manteniendo topología; reconfigurar aristas preservando grado prueba estructura más allá del grado; muestrear genes emparejados por anotación o expresión controla detectabilidad. El nulo debe conservar los sesgos que no son la señal de interés. La validación incluye redes independientes, perturbaciones y replicación por condición.",
                "Permuting node labels tests association while retaining topology; rewiring edges with degree preservation tests structure beyond degree; sampling genes matched by annotation or expression controls detectability. The null should preserve biases that are not the signal of interest. Validation includes independent networks, perturbations, and replication by condition.",
                "Permutation af nodelabels tester association med bevaret topologi; rewiring af kanter med bevaret grad tester struktur ud over grad; sampling af gener matchet på annotation eller ekspression kontrollerer detekterbarhed. Nulmodellen bør bevare bias, der ikke er signalet af interesse. Validering omfatter uafhængige netværk, perturbationer og replikation efter betingelse.",
            ),
            (
                (
                    "Un nulo uniforme suele ignorar sesgo de grado y anotación.",
                    "A uniform null often ignores degree and annotation bias.",
                    "En uniform nulmodel ignorerer ofte grad- og annotationsbias.",
                ),
                (
                    "La red de validación no debe derivarse de la misma evidencia.",
                    "The validation network should not derive from the same evidence.",
                    "Valideringsnetværket bør ikke afledes af samme evidens.",
                ),
            ),
        ),
    ),
    examples=(
        (
            "m09.e01",
            ("Grado y componentes", "Degree and components", "Grad og komponenter"),
            (
                "Calcula grados y componentes conectados en una red no dirigida pequeña.",
                "Compute degrees and connected components in a small undirected network.",
                "Beregn grader og sammenhængende komponenter i et lille urettet netværk.",
            ),
            (
                (
                    "La lista de adyacencia conserva vecinos únicos.",
                    "The adjacency list retains unique neighbors.",
                    "Nabolisten bevarer unikke naboer.",
                ),
                (
                    "DFS identifica nodos alcanzables.",
                    "DFS identifies reachable nodes.",
                    "DFS identificerer nåelige noder.",
                ),
            ),
            """def graph_summary(edges: list[tuple[str, str]]):
    adjacency: dict[str, set[str]] = {}
    for left, right in edges:
        adjacency.setdefault(left, set()).add(right)
        adjacency.setdefault(right, set()).add(left)

    components: list[set[str]] = []
    unseen = set(adjacency)
    while unseen:
        start = unseen.pop()
        component = {start}
        stack = [start]
        while stack:
            node = stack.pop()
            new_nodes = adjacency[node] - component
            component.update(new_nodes)
            unseen.difference_update(new_nodes)
            stack.extend(new_nodes)
        components.append(component)
    degrees = {node: len(neighbors) for node, neighbors in adjacency.items()}
    return degrees, sorted(len(component) for component in components)


print(graph_summary([("A", "B"), ("B", "C"), ("D", "E")]))
""",
            "({'A': 1, 'B': 2, 'C': 1, 'D': 1, 'E': 1}, [2, 3])",
            (
                "El resumen describe topología; no asigna función a los nodos.",
                "The summary describes topology; it does not assign function to nodes.",
                "Opsummeringen beskriver topologi; den tildeler ikke funktion til noderne.",
            ),
        ),
        (
            "m09.e02",
            (
                "Probabilidad hipergeométrica",
                "Hypergeometric probability",
                "Hypergeometrisk sandsynlighed",
            ),
            (
                "Calcula la probabilidad exacta de observar k éxitos en una selección sin reemplazo.",
                "Compute the exact probability of observing k successes in sampling without replacement.",
                "Beregn den eksakte sandsynlighed for at observere k succeser ved udtræk uden tilbagelægning.",
            ),
            (
                (
                    "El numerador combina elecciones anotadas y no anotadas.",
                    "The numerator combines annotated and unannotated choices.",
                    "Tælleren kombinerer valg af annoterede og ikke-annoterede elementer.",
                ),
                (
                    "El denominador cuenta todas las listas de tamaño n.",
                    "The denominator counts all lists of size n.",
                    "Nævneren tæller alle lister med størrelse n.",
                ),
            ),
            """from math import comb


def hypergeom_probability(N: int, K: int, n: int, k: int) -> float:
    return comb(K, k) * comb(N - K, n - k) / comb(N, n)


print(round(hypergeom_probability(100, 20, 10, 4), 5))
""",
            "0.08411",
            (
                "El p-valor de enriquecimiento requiere sumar probabilidades para k o más, no sólo esta masa puntual.",
                "An enrichment p-value requires summing probabilities for k or more, not only this point mass.",
                "En berigelses-p-værdi kræver summering af sandsynligheder for k eller mere, ikke kun denne punktmasse.",
            ),
        ),
        (
            "m09.e03",
            ("Random walk with restart", "Random walk with restart", "Random walk with restart"),
            (
                "Propaga una semilla en una red normalizada hasta convergencia.",
                "Propagate a seed through a normalized network until convergence.",
                "Propagér en seed gennem et normaliseret netværk indtil konvergens.",
            ),
            (
                (
                    "Cada nodo reparte masa entre sus vecinos.",
                    "Each node distributes mass among its neighbors.",
                    "Hver node fordeler masse mellem sine naboer.",
                ),
                (
                    "El reinicio conserva proximidad a la semilla.",
                    "Restart preserves proximity to the seed.",
                    "Restart bevarer nærhed til seeden.",
                ),
            ),
            """def random_walk_with_restart(
    adjacency: list[list[float]], seed: list[float], restart: float = 0.4, steps: int = 50
) -> list[float]:
    scores = seed[:]
    for _ in range(steps):
        propagated = [0.0] * len(scores)
        for source, row in enumerate(adjacency):
            for target, probability in enumerate(row):
                propagated[target] += scores[source] * probability
        scores = [
            restart * seed[index] + (1.0 - restart) * propagated[index]
            for index in range(len(scores))
        ]
    return scores


transition = [[0.0, 1.0, 0.0], [0.5, 0.0, 0.5], [0.0, 1.0, 0.0]]
print([round(value, 3) for value in random_walk_with_restart(transition, [1.0, 0.0, 0.0])])
""",
            "[0.583, 0.292, 0.125]",
            (
                "Los valores dependen de normalización, dirección y parámetro de reinicio.",
                "Values depend on normalization, direction, and restart parameter.",
                "Værdierne afhænger af normalisering, retning og restartparameter.",
            ),
        ),
    ),
    practices=(
        (
            "m09.p01",
            "SHORT_ANSWER",
            (
                "Distingue red de interacción física y red de coexpresión.",
                "Distinguish a physical-interaction network from a co-expression network.",
                "Skeln mellem et fysisk interaktionsnetværk og et co-ekspressionsnetværk.",
            ),
            (
                (
                    "Compara significado de arista.",
                    "Compare edge meaning.",
                    "Sammenlign kantbetydning.",
                ),
            ),
            (
                "Una arista física representa evidencia de contacto molecular; una arista de coexpresión representa asociación estadística entre perfiles y no demuestra contacto ni regulación directa.",
                "A physical edge represents evidence of molecular contact; a co-expression edge represents statistical association between profiles and does not prove contact or direct regulation.",
                "En fysisk kant repræsenterer evidens for molekylær kontakt; en co-ekspressionskant repræsenterer statistisk association mellem profiler og beviser ikke kontakt eller direkte regulering.",
            ),
            (
                "Ambas pueden ser útiles, pero no deben fusionarse sin conservar el tipo.",
                "Both may be useful, but they should not be merged without retaining type.",
                "Begge kan være nyttige, men bør ikke flettes uden bevaret type.",
            ),
            "",
        ),
        (
            "m09.p02",
            "CODE_TRACING",
            (
                "En estrella de cinco nodos tiene ¿qué grado central?",
                "What is the center degree in a five-node star?",
                "Hvilken grad har centrum i en stjerne med fem noder?",
            ),
            (("Cuenta las hojas.", "Count the leaves.", "Tæl bladene."),),
            ("4", "4", "4"),
            (
                "Cada hoja tiene grado uno y el centro conecta con cuatro.",
                "Each leaf has degree one and the center connects to four.",
                "Hvert blad har grad én, og centrum forbinder til fire.",
            ),
            "",
        ),
        (
            "m09.p03",
            "FILL_IN_THE_BLANK",
            (
                "En análisis hipergeométrico, el conjunto de todos los genes evaluables es el ________.",
                "In hypergeometric analysis, the set of all evaluable genes is the ________.",
                "I hypergeometrisk analyse er sættet af alle evaluerbare gener ________.",
            ),
            (("Define N.", "It defines N.", "Det definerer N."),),
            ("universo", "universe", "univers"),
            (
                "Usar todo el genoma cuando sólo algunos genes podían detectarse sesga el nulo.",
                "Using the whole genome when only some genes were detectable biases the null.",
                "Brug af hele genomet, når kun nogle gener kunne detekteres, skævvrider nulmodellen.",
            ),
            "",
        ),
        (
            "m09.p04",
            "DATA_INTERPRETATION",
            (
                "Un término tiene FDR=0.01 pero sólo dos genes de la lista. Interpreta.",
                "A term has FDR=0.01 but only two list genes. Interpret it.",
                "En term har FDR=0,01 men kun to gener fra listen. Fortolk.",
            ),
            (
                (
                    "Considera tamaño de efecto y estabilidad.",
                    "Consider effect size and stability.",
                    "Overvej effektstørrelse og stabilitet.",
                ),
            ),
            (
                "Es estadísticamente priorizable bajo el modelo, pero puede ser frágil y depender de dos genes. Deben reportarse k, K, odds ratio, identidad de genes, sensibilidad a retirar uno y redundancia con otros términos.",
                "It is statistically prioritized under the model but may be fragile and driven by two genes. Report k, K, odds ratio, gene identities, leave-one-out sensitivity, and redundancy with other terms.",
                "Det er statistisk prioriteret under modellen, men kan være skrøbeligt og drevet af to gener. Rapportér k, K, odds ratio, genidentiteter, leave-one-out-følsomhed og redundans med andre termer.",
            ),
            (
                "Significancia ajustada no sustituye interpretación biológica.",
                "Adjusted significance does not replace biological interpretation.",
                "Justeret signifikans erstatter ikke biologisk fortolkning.",
            ),
            "",
        ),
        (
            "m09.p05",
            "PIPELINE_DESIGN",
            (
                "Diseña un enriquecimiento reproducible para genes diferencialmente expresados.",
                "Design a reproducible enrichment analysis for differentially expressed genes.",
                "Design en reproducerbar berigelsesanalyse for differentielt udtrykte gener.",
            ),
            (
                (
                    "Incluye universo y versión.",
                    "Include universe and version.",
                    "Medtag univers og version.",
                ),
            ),
            (
                "Fijar release de anotación; definir universo como genes incluidos en el test; mapear IDs con auditoría; elegir lista y dirección; ejecutar ORA; ajustar FDR; reportar solapamientos y tamaños; resumir redundancia; validar con ranking continuo o cohortes independientes.",
                "Fix annotation release; define the universe as genes included in testing; audit ID mapping; choose list and direction; run ORA; adjust FDR; report overlaps and sizes; summarize redundancy; validate using continuous ranking or independent cohorts.",
                "Fastlås annotationsrelease; definér universet som gener inkluderet i testen; auditér ID-mapping; vælg liste og retning; kør ORA; justér FDR; rapportér overlap og størrelser; opsummér redundans; validér med kontinuerlig ranking eller uafhængige kohorter.",
            ),
            (
                "Cada decisión debe quedar en metadatos y código.",
                "Every decision should be retained in metadata and code.",
                "Hver beslutning bør bevares i metadata og kode.",
            ),
            "",
        ),
        (
            "m09.p06",
            "DEBUGGING",
            (
                "El enriquecimiento devuelve cientos de términos significativos dominados por genes muy estudiados. Diagnostica.",
                "Enrichment returns hundreds of significant terms dominated by heavily studied genes. Diagnose it.",
                "Berigelse returnerer hundredvis af signifikante termer domineret af meget studerede gener. Diagnosticér.",
            ),
            (
                (
                    "Revisa universo y sesgo de anotación.",
                    "Inspect universe and annotation bias.",
                    "Undersøg univers og annotationsbias.",
                ),
            ),
            (
                "Comprobar mapeos duplicados, universo inadecuado, profundidad de anotación y dependencia de hubs anotados; usar controles emparejados por detectabilidad/anotación, resumir términos redundantes y repetir sin genes dominantes.",
                "Check duplicate mappings, an inappropriate universe, annotation depth, and dependence on annotated hubs; use controls matched by detectability/annotation, summarize redundant terms, and repeat without dominant genes.",
                "Kontrollér duplikerede mappings, et uhensigtsmæssigt univers, annotationsdybde og afhængighed af annoterede hubs; brug kontroller matchet på detekterbarhed/annotation, opsummér redundante termer og gentag uden dominerende gener.",
            ),
            (
                "El sesgo de conocimiento puede parecer señal biológica.",
                "Knowledge bias can resemble biological signal.",
                "Vidensbias kan ligne biologisk signal.",
            ),
            "",
        ),
        (
            "m09.p07",
            "ORAL_EXPLANATION",
            (
                "Explica un nulo que preserve grado para evaluar proximidad de genes enfermedad.",
                "Explain a degree-preserving null for evaluating disease-gene proximity.",
                "Forklar en gradbevarende nulmodel til evaluering af nærhed mellem sygdomsgener.",
            ),
            (
                (
                    "Compara con selección uniforme.",
                    "Compare with uniform selection.",
                    "Sammenlign med uniform selektion.",
                ),
            ),
            (
                "Muestrear conjuntos de nodos con distribución de grado similar o reconfigurar aristas preservando grados, recalcular la proximidad y comparar la observada. Así el resultado no se explica sólo porque los genes sean hubs.",
                "Sample node sets with a similar degree distribution or rewire edges while preserving degrees, recompute proximity, and compare with observed proximity. Then the result is not explained only by genes being hubs.",
                "Sample noder med en lignende gradfordeling eller rewire kanter med bevarede grader, genberegn nærhed og sammenlign med den observerede. Dermed forklares resultatet ikke kun af, at generne er hubs.",
            ),
            (
                "La elección entre ambos nulos depende de qué parte de la red se considera fija.",
                "The choice between nulls depends on which part of the network is treated as fixed.",
                "Valget mellem nulmodeller afhænger af, hvilken del af netværket der behandles som fast.",
            ),
            "",
        ),
        (
            "m09.p08",
            "ORDERING",
            (
                "Ordena: definir red, armonizar IDs, fijar universo, calcular estadístico, generar nulo, ajustar multiplicidad, validar.",
                "Order: define network, harmonize IDs, fix universe, compute statistic, generate null, adjust multiplicity, validate.",
                "Ordén: definér netværk, harmonisér ID'er, fastlås univers, beregn statistik, generér nulmodel, justér multiplicitet, validér.",
            ),
            (
                (
                    "La semántica precede al cálculo.",
                    "Semantics precede computation.",
                    "Semantik går forud for beregning.",
                ),
            ),
            (
                "Definir red → armonizar IDs/versiones → fijar universo → calcular estadístico → generar nulo compatible → estimar significancia → ajustar multiplicidad → validar en evidencia independiente.",
                "Define network → harmonize IDs/versions → fix universe → compute statistic → generate compatible null → estimate significance → adjust multiplicity → validate with independent evidence.",
                "Definér netværk → harmonisér ID'er/versioner → fastlås univers → beregn statistik → generér kompatibel nulmodel → estimer signifikans → justér multiplicitet → validér med uafhængig evidens.",
            ),
            (
                "El orden evita interpretar una red mal definida.",
                "The order prevents interpreting a poorly defined network.",
                "Rækkefølgen forhindrer fortolkning af et dårligt defineret netværk.",
            ),
            "",
        ),
    ),
    mcqs=(
        (
            "001",
            (
                "¿Qué debe acompañar a una arista?",
                "What should accompany an edge?",
                "Hvad bør følge en kant?",
            ),
            (
                (
                    "semantics",
                    (
                        "Tipo, dirección y evidencia",
                        "Type, direction, and evidence",
                        "Type, retning og evidens",
                    ),
                ),
                ("color", ("Sólo color", "Color only", "Kun farve")),
                ("rank", ("Sólo rango", "Rank only", "Kun rang")),
            ),
            "semantics",
            (
                "Sin semántica no se sabe qué relación representa.",
                "Without semantics the represented relationship is unknown.",
                "Uden semantik er den repræsenterede relation ukendt.",
            ),
        ),
        (
            "002",
            ("¿Qué mide el grado?", "What does degree measure?", "Hvad måler grad?"),
            (
                ("neighbors", ("Número de vecinos", "Number of neighbors", "Antal naboer")),
                ("causality", ("Causalidad", "Causality", "Kausalitet")),
                ("expression", ("Expresión", "Expression", "Ekspression")),
            ),
            "neighbors",
            (
                "En red simple no dirigida cuenta aristas incidentes.",
                "In a simple undirected graph it counts incident edges.",
                "I en simpel urettet graf tæller det incidentkanter.",
            ),
        ),
        (
            "003",
            (
                "¿Qué distribución usa ORA clásica?",
                "Which distribution does classical ORA use?",
                "Hvilken fordeling bruger klassisk ORA?",
            ),
            (
                ("hyper", ("Hipergeométrica", "Hypergeometric", "Hypergeometrisk")),
                ("normal", ("Siempre normal", "Always normal", "Altid normal")),
                ("poisson", ("Siempre Poisson", "Always Poisson", "Altid Poisson")),
            ),
            "hyper",
            (
                "Modela extracción sin reemplazo.",
                "It models sampling without replacement.",
                "Den modellerer udtræk uden tilbagelægning.",
            ),
        ),
        (
            "004",
            ("¿Qué define N en ORA?", "What defines N in ORA?", "Hvad definerer N i ORA?"),
            (
                ("universe", ("Tamaño del universo", "Universe size", "Universstørrelse")),
                ("list", ("Solapamiento", "Overlap", "Overlap")),
                ("terms", ("Número de términos", "Number of terms", "Antal termer")),
            ),
            "universe",
            (
                "N es el conjunto de elementos elegibles.",
                "N is the set of eligible elements.",
                "N er sættet af kvalificerede elementer.",
            ),
        ),
        (
            "005",
            (
                "¿Qué controla Benjamini–Hochberg?",
                "What does Benjamini–Hochberg control?",
                "Hvad kontrollerer Benjamini–Hochberg?",
            ),
            (
                ("fdr", ("FDR", "FDR", "FDR")),
                ("degree", ("Grado", "Degree", "Grad")),
                ("coverage", ("Cobertura de red", "Network coverage", "Netværksdækning")),
            ),
            "fdr",
            (
                "Controla la tasa esperada de falsos descubrimientos bajo condiciones apropiadas.",
                "It controls the expected false-discovery rate under appropriate conditions.",
                "Det kontrollerer den forventede falske opdagelsesrate under passende betingelser.",
            ),
        ),
        (
            "006",
            (
                "¿Qué parámetro retiene masa en semillas en RWR?",
                "Which parameter retains mass at seeds in RWR?",
                "Hvilken parameter bevarer masse ved seeds i RWR?",
            ),
            (
                (
                    "restart",
                    ("Probabilidad de reinicio", "Restart probability", "Restart-sandsynlighed"),
                ),
                ("degree", ("Grado máximo", "Maximum degree", "Maksimal grad")),
                ("pvalue", ("p-valor", "p-value", "p-værdi")),
            ),
            "restart",
            (
                "Equilibra difusión y retorno.",
                "It balances diffusion and return.",
                "Den balancerer diffusion og tilbagevenden.",
            ),
        ),
        (
            "007",
            (
                "¿Qué nulo controla hubs?",
                "Which null controls for hubs?",
                "Hvilken nulmodel kontrollerer hubs?",
            ),
            (
                (
                    "degree",
                    (
                        "Preservar distribución de grado",
                        "Preserve degree distribution",
                        "Bevar gradfordeling",
                    ),
                ),
                (
                    "uniform",
                    ("Sólo muestreo uniforme", "Uniform sampling only", "Kun uniform sampling"),
                ),
                (
                    "labels",
                    ("Cambiar nombres visuales", "Change display names", "Skift visningsnavne"),
                ),
            ),
            "degree",
            (
                "Impide que centralidad trivial explique el resultado.",
                "It prevents trivial centrality from explaining the result.",
                "Det forhindrer, at triviel centralitet forklarer resultatet.",
            ),
        ),
        (
            "008",
            (
                "¿Qué describe un módulo de comunidad?",
                "What does a community module describe?",
                "Hvad beskriver et community-modul?",
            ),
            (
                (
                    "dense",
                    ("Grupo relativamente denso", "Relatively dense group", "Relativt tæt gruppe"),
                ),
                (
                    "pathway",
                    (
                        "Vía biológica demostrada",
                        "Proven biological pathway",
                        "Bevist biologisk pathway",
                    ),
                ),
                ("causal", ("Mecanismo causal", "Causal mechanism", "Kausal mekanisme")),
            ),
            "dense",
            (
                "La interpretación funcional requiere evidencia adicional.",
                "Functional interpretation requires additional evidence.",
                "Funktionel fortolkning kræver yderligere evidens.",
            ),
        ),
        (
            "009",
            (
                "¿Qué mejora interpretación de un término enriquecido?",
                "What improves interpretation of an enriched term?",
                "Hvad forbedrer fortolkningen af en beriget term?",
            ),
            (
                (
                    "effect",
                    (
                        "Tamaño de efecto y genes responsables",
                        "Effect size and driving genes",
                        "Effektstørrelse og drivende gener",
                    ),
                ),
                ("pvalue", ("Sólo p-valor", "P-value only", "Kun p-værdi")),
                ("title", ("Título largo", "Long title", "Lang titel")),
            ),
            "effect",
            (
                "La significancia no explica magnitud ni mecanismo.",
                "Significance does not explain magnitude or mechanism.",
                "Signifikans forklarer ikke størrelse eller mekanisme.",
            ),
        ),
        (
            "010",
            (
                "¿Qué red es mejor para validación?",
                "Which network is better for validation?",
                "Hvilket netværk er bedre til validering?",
            ),
            (
                (
                    "independent",
                    (
                        "Derivada de evidencia independiente",
                        "Derived from independent evidence",
                        "Afledt af uafhængig evidens",
                    ),
                ),
                (
                    "same",
                    (
                        "La misma usada para descubrir",
                        "The same used for discovery",
                        "Den samme som til discovery",
                    ),
                ),
                (
                    "random",
                    (
                        "Una red sin metadatos",
                        "A network without metadata",
                        "Et netværk uden metadata",
                    ),
                ),
            ),
            "independent",
            (
                "Reduce circularidad de evidencia.",
                "It reduces evidence circularity.",
                "Det reducerer cirkularitet i evidens.",
            ),
        ),
    ),
    true_false=(
        (
            "011",
            (
                "Una arista de coexpresión demuestra interacción física.",
                "A co-expression edge proves physical interaction.",
                "En co-ekspressionskant beviser fysisk interaktion.",
            ),
            False,
            (
                "Representa asociación de perfiles.",
                "It represents profile association.",
                "Den repræsenterer profilassociation.",
            ),
        ),
        (
            "012",
            (
                "Centralidad alta demuestra causalidad.",
                "High centrality proves causality.",
                "Høj centralitet beviser kausalitet.",
            ),
            False,
            (
                "Es una propiedad topológica de la red observada.",
                "It is a topological property of the observed network.",
                "Det er en topologisk egenskab ved det observerede netværk.",
            ),
        ),
        (
            "013",
            (
                "El universo de ORA debe reflejar elementos evaluables.",
                "The ORA universe should reflect evaluable elements.",
                "ORA-universet bør afspejle evaluerbare elementer.",
            ),
            True,
            (
                "Define la población bajo el nulo.",
                "It defines the null population.",
                "Det definerer populationen under nulmodellen.",
            ),
        ),
        (
            "014",
            (
                "Un p-valor pequeño mide directamente tamaño de efecto.",
                "A small p-value directly measures effect size.",
                "En lille p-værdi måler direkte effektstørrelse.",
            ),
            False,
            (
                "Significancia y magnitud son distintas.",
                "Significance and magnitude are distinct.",
                "Signifikans og størrelse er forskellige.",
            ),
        ),
        (
            "015",
            (
                "Los términos funcionales suelen compartir genes.",
                "Functional terms often share genes.",
                "Funktionelle termer deler ofte gener.",
            ),
            True,
            (
                "Esto crea dependencia y redundancia.",
                "This creates dependence and redundancy.",
                "Det skaber afhængighed og redundans.",
            ),
        ),
        (
            "016",
            (
                "Random walk with restart depende del parámetro de reinicio.",
                "Random walk with restart depends on the restart parameter.",
                "Random walk with restart afhænger af restartparameteren.",
            ),
            True,
            (
                "Controla cuánto se conserva la señal inicial.",
                "It controls how much initial signal is retained.",
                "Den kontrollerer, hvor meget initialt signal bevares.",
            ),
        ),
        (
            "017",
            (
                "Un módulo de comunidad es automáticamente una vía.",
                "A community module is automatically a pathway.",
                "Et community-modul er automatisk en pathway.",
            ),
            False,
            (
                "La densidad computacional necesita anotación y validación.",
                "Computational density needs annotation and validation.",
                "Beregningsmæssig tæthed kræver annotation og validering.",
            ),
        ),
        (
            "018",
            (
                "Un nulo que preserva grado puede controlar sesgo de hubs.",
                "A degree-preserving null can control hub bias.",
                "En gradbevarende nulmodel kan kontrollere hub-bias.",
            ),
            True,
            (
                "Mantiene la distribución topológica relevante.",
                "It retains the relevant topological distribution.",
                "Den bevarer den relevante topologiske fordeling.",
            ),
        ),
        (
            "019",
            (
                "La versión de la red afecta reproducibilidad.",
                "Network version affects reproducibility.",
                "Netværksversion påvirker reproducerbarhed.",
            ),
            True,
            (
                "Nodos, aristas y evidencia cambian entre releases.",
                "Nodes, edges, and evidence change across releases.",
                "Noder, kanter og evidens ændres mellem releases.",
            ),
        ),
        (
            "020",
            (
                "En enriquecimiento significativo constituye recomendación clínica.",
                "Significant enrichment constitutes a clinical recommendation.",
                "Signifikant berigelse udgør en klinisk anbefaling.",
            ),
            False,
            (
                "Es evidencia exploratoria dependiente del modelo.",
                "It is model-dependent exploratory evidence.",
                "Det er modelafhængig eksplorativ evidens.",
            ),
        ),
    ),
    tutor=(
        (
            "El análisis de redes comienza definiendo qué representan nodos y aristas, con dirección, peso, condición, fuente y evidencia explícitos. Las métricas de centralidad describen una red observada y son sensibles a cobertura y sesgo, por lo que no demuestran función o causalidad. El enriquecimiento hipergeométrico compara una lista con conjuntos anotados dentro de un universo elegible; requiere corrección por multiplicidad, tamaño de efecto y genes responsables. La propagación y random walk difunden señal según topología y parámetros, mientras la detección de comunidades produce módulos computacionales que deben validarse. Los nulos deben preservar grado, anotación o detectabilidad cuando estos factores podrían explicar el resultado. Versiones, IDs y evidencia independiente son esenciales para reproducibilidad.",
            "Network analysis begins by defining what nodes and edges represent, with explicit direction, weight, condition, source, and evidence. Centrality metrics describe an observed network and are sensitive to coverage and bias, so they do not prove function or causality. Hypergeometric enrichment compares a list with annotated sets within an eligible universe; it requires multiplicity correction, effect size, and driving genes. Propagation and random walks diffuse signal according to topology and parameters, while community detection yields computational modules that require validation. Nulls should preserve degree, annotation, or detectability when those factors could explain the result. Versions, IDs, and independent evidence are essential for reproducibility.",
            "Netværksanalyse begynder med at definere, hvad noder og kanter repræsenterer, med eksplicit retning, vægt, betingelse, kilde og evidens. Centralitetsmål beskriver et observeret netværk og er følsomme over for dækning og bias, så de beviser ikke funktion eller kausalitet. Hypergeometrisk berigelse sammenligner en liste med annoterede sæt inden for et kvalificeret univers; den kræver korrektion for multiplicitet, effektstørrelse og drivende gener. Propagation og random walks spreder signal efter topologi og parametre, mens community-detektion giver beregningsmoduler, der kræver validering. Nulmodeller bør bevare grad, annotation eller detekterbarhed, når disse faktorer kan forklare resultatet. Versioner, ID'er og uafhængig evidens er essentielle for reproducerbarhed.",
        ),
        (
            (
                "La semántica precede a la topología.",
                "Semantics precede topology.",
                "Semantik går forud for topologi.",
            ),
            (
                "Centralidad no implica causalidad.",
                "Centrality does not imply causality.",
                "Centralitet indebærer ikke kausalitet.",
            ),
            (
                "ORA depende del universo.",
                "ORA depends on the universe.",
                "ORA afhænger af universet.",
            ),
            (
                "FDR y tamaño de efecto son complementarios.",
                "FDR and effect size are complementary.",
                "FDR og effektstørrelse er komplementære.",
            ),
            (
                "Propagación depende de normalización y parámetros.",
                "Propagation depends on normalization and parameters.",
                "Propagation afhænger af normalisering og parametre.",
            ),
            (
                "Los nulos deben conservar sesgos relevantes.",
                "Nulls should preserve relevant biases.",
                "Nulmodeller bør bevare relevante bias.",
            ),
        ),
        (
            (
                "Fusionar redes heterogéneas sin tipo de arista.",
                "Merging heterogeneous networks without edge type.",
                "At flette heterogene netværk uden kanttype.",
            ),
            (
                "Interpretar hubs como genes esenciales.",
                "Interpreting hubs as essential genes.",
                "At fortolke hubs som essentielle gener.",
            ),
            (
                "Usar todo el genoma como universo por defecto.",
                "Using the whole genome as the default universe.",
                "At bruge hele genomet som standardunivers.",
            ),
            (
                "Reportar sólo términos y p-valores.",
                "Reporting only terms and p-values.",
                "At rapportere kun termer og p-værdier.",
            ),
            (
                "Ignorar redundancia ontológica.",
                "Ignoring ontology redundancy.",
                "At ignorere ontologisk redundans.",
            ),
            (
                "Usar un nulo uniforme con hubs.",
                "Using a uniform null with hubs.",
                "At bruge en uniform nulmodel med hubs.",
            ),
        ),
        (
            (
                "¿Qué significa exactamente esta arista?",
                "What exactly does this edge mean?",
                "Hvad betyder denne kant præcist?",
            ),
            (
                "¿Qué nodos podían aparecer en el análisis?",
                "Which nodes could appear in the analysis?",
                "Hvilke noder kunne indgå i analysen?",
            ),
            (
                "¿Qué genes impulsan el término?",
                "Which genes drive the term?",
                "Hvilke gener driver termen?",
            ),
            (
                "¿Cómo se controló multiplicidad?",
                "How was multiplicity controlled?",
                "Hvordan blev multiplicitet kontrolleret?",
            ),
            (
                "¿Qué sesgo conserva el nulo?",
                "Which bias does the null preserve?",
                "Hvilket bias bevarer nulmodellen?",
            ),
            (
                "¿Es estable en otra red o condición?",
                "Is it stable in another network or condition?",
                "Er det stabilt i et andet netværk eller en anden betingelse?",
            ),
        ),
        (
            (
                "Define nodos y aristas con precisión.",
                "Defines nodes and edges precisely.",
                "Definerer noder og kanter præcist.",
            ),
            (
                "Interpreta topología con cautela.",
                "Interprets topology cautiously.",
                "Fortolker topologi forsigtigt.",
            ),
            (
                "Formula ORA y universo correctamente.",
                "Formulates ORA and universe correctly.",
                "Formulerer ORA og univers korrekt.",
            ),
            (
                "Reporta FDR, efecto y genes.",
                "Reports FDR, effect, and genes.",
                "Rapporterer FDR, effekt og gener.",
            ),
            (
                "Explica propagación y módulos.",
                "Explains propagation and modules.",
                "Forklarer propagation og moduler.",
            ),
            (
                "Diseña nulos estructuralmente apropiados.",
                "Designs structurally appropriate nulls.",
                "Designer strukturelt passende nulmodeller.",
            ),
        ),
        (
            (
                "No inventar interacciones o vías.",
                "Do not invent interactions or pathways.",
                "Opfind ikke interaktioner eller pathways.",
            ),
            (
                "No presentar centralidad como mecanismo.",
                "Do not present centrality as mechanism.",
                "Præsenter ikke centralitet som mekanisme.",
            ),
            (
                "No ocultar universo o release.",
                "Do not hide universe or release.",
                "Skjul ikke univers eller release.",
            ),
            (
                "No convertir enriquecimiento en consejo clínico.",
                "Do not turn enrichment into clinical advice.",
                "Omsæt ikke berigelse til klinisk rådgivning.",
            ),
            (
                "Responder en el idioma activo.",
                "Answer in the active language.",
                "Svar på det aktive sprog.",
            ),
        ),
        (
            "Graph theory foundations for biological networks.",
            "Hypergeometric over-representation analysis and gene-set methods.",
            "Benjamini-Hochberg false-discovery-rate control.",
            "Random walk with restart and network-propagation literature.",
            "Degree-preserving network null models and configuration models.",
            "Active SDU DM847 biological-network learning outcomes.",
        ),
    ),
)

LOCALIZED_MODULE_09_BIOLOGICAL_NETWORKS_ENRICHMENT: LocalizedLearningModule = build_module(_SPEC)
LOCALIZED_OBJECTIVE_QUESTION_BANK_09 = build_question_bank(_SPEC)


def materialize_module_09_question_bank(
    locale: AppLocale | str = AppLocale.SPANISH_SPAIN,
) -> tuple[AssessmentItem, ...]:
    return materialize_bank(LOCALIZED_OBJECTIVE_QUESTION_BANK_09, locale)


MODULE_09_BIOLOGICAL_NETWORKS_ENRICHMENT: LearningModule = (
    LOCALIZED_MODULE_09_BIOLOGICAL_NETWORKS_ENRICHMENT.materialize(AppLocale.SPANISH_SPAIN)
)
OBJECTIVE_QUESTION_BANK_09 = materialize_module_09_question_bank()

__all__ = [
    "LOCALIZED_MODULE_09_BIOLOGICAL_NETWORKS_ENRICHMENT",
    "LOCALIZED_OBJECTIVE_QUESTION_BANK_09",
    "MODULE_09_BIOLOGICAL_NETWORKS_ENRICHMENT",
    "OBJECTIVE_QUESTION_BANK_09",
    "materialize_module_09_question_bank",
]
