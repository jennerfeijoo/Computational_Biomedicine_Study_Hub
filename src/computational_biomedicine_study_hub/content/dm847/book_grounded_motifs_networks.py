"""Focused source-grounded extensions for DM847 motifs and biological networks."""

from __future__ import annotations

from dataclasses import replace

from ...learning.activity_types import ActivityType
from ..localized_models import LocalizedLearningModule, LocalizedTutorSupportPacket
from .authoring import concept, example, objective, objective_mcq, practice
from .book_grounded_audit import AcademicReference, ModuleSourceAudit

DM847_NETWORK_SOURCES: tuple[AcademicReference, ...] = (
    AcademicReference(
        source_id="ideker-2002-active-modules",
        citation=(
            "Trey Ideker, Owen Ozier, Benno Schwikowski, and Andrew F. Siegel, "
            "Discovering regulatory and signalling circuits in molecular interaction "
            "networks, Bioinformatics 18 Suppl. 1 (2002), "
            "doi:10.1093/bioinformatics/18.suppl_1.s233."
        ),
        relevant_scope=(
            "vertex-weighted molecular networks, connected active-module scoring, "
            "heuristic module search, and interpretation of high-scoring subnetworks"
        ),
    ),
    AcademicReference(
        source_id="alcaraz-2012-keypathwayminer",
        citation=(
            "Nicolas Alcaraz et al., Efficient key pathway mining: combining networks "
            "and OMICS data, Integrative Biology 4 (2012), doi:10.1039/C2IB00133K."
        ),
        relevant_scope=(
            "connected de novo pathway extraction, integration of interaction networks "
            "with OMICS measurements, and explicit exception constraints"
        ),
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


def update_motif_network_source_catalog(
    sources: tuple[AcademicReference, ...],
) -> tuple[AcademicReference, ...]:
    """Correct chapter 11 scope and append primary network-method references."""

    corrected: list[AcademicReference] = []
    for source in sources:
        if source.source_id == "compeau-pevzner-v2-ch11":
            corrected.append(
                replace(
                    source,
                    relevant_scope=(
                        "peptide sequencing, peptide-spectrum matching, spectral dictionaries, "
                        "false-discovery reasoning, and spectral alignment; not biological "
                        "network enrichment"
                    ),
                )
            )
        else:
            corrected.append(source)
    return (*corrected, *DM847_NETWORK_SOURCES)


def update_motif_network_audit(
    audit: tuple[ModuleSourceAudit, ...],
) -> tuple[ModuleSourceAudit, ...]:
    """Mark M08 and M09 reviewed after their focused extensions and source correction."""

    updated: list[ModuleSourceAudit] = []
    for item in audit:
        if item.module_id == "dm847.m08":
            updated.append(
                replace(
                    item,
                    state="consistent",
                    finding=(
                        "Existing coverage of PWMs, pseudocounts, entropy, log-odds, occurrence "
                        "models, latent motif positions, EM responsibilities, local optima, "
                        "background choice, and independent validation is consistent. A complete "
                        "auditable transition from soft responsibilities to fractional M-step "
                        "counts and objective-based stopping required one explicit treatment."
                    ),
                    implemented_change=(
                        "Added an original trilingual fractional-count and convergence explanation, "
                        "deterministic weighted-PWM example, debugging exercise, and stable "
                        "objective item."
                    ),
                )
            )
        elif item.module_id == "dm847.m09":
            updated.append(
                replace(
                    item,
                    source_ids=(
                        "sdu-dm847-active-2025",
                        "ideker-2002-active-modules",
                        "alcaraz-2012-keypathwayminer",
                    ),
                    source_scope=(
                        "network semantics and over-representation analysis",
                        "connected active-module scoring",
                        "constraint-based de novo pathway extraction",
                        "selection-aware null models and validation",
                    ),
                    state="consistent",
                    finding=(
                        "Existing coverage of network semantics, topology, centrality, "
                        "hypergeometric over-representation, multiplicity, propagation, modules, "
                        "and structure-aware null models is consistent. The distinction between "
                        "testing predefined gene sets and selecting connected active subnetworks "
                        "required one explicit treatment. The previous chapter-11 mapping was "
                        "incorrect because that chapter concerns peptide sequencing rather than "
                        "network enrichment."
                    ),
                    implemented_change=(
                        "Corrected the source traceability and added an original trilingual "
                        "comparison of ORA, jActiveModules-style scoring, and "
                        "KeyPathwayMiner-style connected extraction, with a deterministic module "
                        "score example, design exercise, and stable objective item."
                    ),
                )
            )
        else:
            updated.append(item)
    return tuple(updated)


def _extend_motif_discovery(module: LocalizedLearningModule) -> LocalizedLearningModule:
    """Add an explicit fractional-count M-step and auditable stopping rule to M08."""

    extended = replace(
        module,
        objectives=module.objectives
        + (
            objective(
                "m08.bg.o1",
                (
                    "Ejecutar y auditar una actualización EM usando responsabilidades "
                    "normalizadas, conteos fraccionarios, pseudoconteos y un criterio explícito "
                    "de convergencia.",
                    "Execute and audit an EM update using normalized responsibilities, "
                    "fractional counts, pseudocounts, and an explicit convergence criterion.",
                    "Udføre og auditere en EM-opdatering med normaliserede ansvar, "
                    "fraktionelle tællinger, pseudotællinger og et eksplicit "
                    "konvergenskriterium.",
                ),
            ),
        ),
        concepts=module.concepts
        + (
            concept(
                "fractional-counts-and-em-convergence",
                (
                    "Conteos fraccionarios y convergencia de EM",
                    "Fractional counts and EM convergence",
                    "Fraktionelle tællinger og EM-konvergens",
                ),
                (
                    "En el E-step, cada posición candidata recibe una responsabilidad posterior "
                    "según el modelo de ocurrencia. En OOPS, las responsabilidades de las "
                    "posiciones de una misma secuencia deben sumar uno. El M-step no convierte "
                    "estas probabilidades en etiquetas duras: cada ventana contribuye a los "
                    "conteos de bases con un peso fraccionario igual a su responsabilidad. Los "
                    "pseudoconteos se añaden a esos conteos esperados y cada columna se normaliza "
                    "para obtener una nueva PWM. Cuando E-step y M-step optimizan la misma "
                    "likelihood observada y usan el mismo fondo y modelo de ocurrencia, la "
                    "likelihood no debe disminuir salvo error numérico. Una implementación debe "
                    "registrar la trayectoria del objetivo, detenerse cuando la mejora absoluta o "
                    "relativa sea menor que una tolerancia y mantener un máximo de iteraciones. "
                    "Terminar tras un número fijo de pasos no demuestra convergencia. Reemplazar "
                    "responsabilidades por su argmax produce una variante de asignación dura y no "
                    "es el mismo algoritmo EM suave. Como EM alcanza óptimos locales, los "
                    "reinicios sólo son comparables si usan la misma función objetivo, datos y "
                    "convenciones.",
                    "In the E-step, every candidate position receives a posterior responsibility "
                    "under the occurrence model. In OOPS, responsibilities for positions within "
                    "one sequence must sum to one. The M-step does not turn these probabilities "
                    "into hard labels: every window contributes to base counts with a fractional "
                    "weight equal to its responsibility. Pseudocounts are added to these expected "
                    "counts and each column is normalized to obtain the new PWM. When the E-step "
                    "and M-step optimize the same observed-data likelihood using the same "
                    "background and occurrence model, likelihood should not decrease except for "
                    "numerical error. An implementation should record the objective trajectory, "
                    "stop when absolute or relative improvement falls below a tolerance, and retain "
                    "a maximum iteration limit. Stopping after a fixed number of steps does not "
                    "demonstrate convergence. Replacing responsibilities by their argmax creates "
                    "a hard-assignment variant and is not the same soft EM algorithm. Because EM "
                    "reaches local optima, restarts are comparable only when they use the same "
                    "objective, data, and conventions.",
                    "I E-trinnet får hver kandidatposition et posterior-ansvar under "
                    "forekomstmodellen. I OOPS skal ansvarene for positioner i samme sekvens "
                    "summere til én. M-trinnet gør ikke sandsynlighederne til hårde labels: hvert "
                    "vindue bidrager til basetællingerne med en fraktionel vægt lig sit ansvar. "
                    "Pseudotællinger lægges til de forventede tællinger, og hver kolonne "
                    "normaliseres til den nye PWM. Når E- og M-trinnet optimerer den samme "
                    "observerede likelihood med samme baggrund og forekomstmodel, bør likelihood "
                    "ikke falde bortset fra numerisk fejl. En implementering bør registrere "
                    "objektivets forløb, stoppe når den absolutte eller relative forbedring er "
                    "mindre end en tolerance og bevare en maksimal iterationsgrænse. Et fast antal "
                    "trin dokumenterer ikke konvergens. Udskiftning af ansvar med deres argmax "
                    "giver en hård tildelingsvariant og er ikke den samme bløde EM-algoritme. Da "
                    "EM når lokale optima, kan genstarter kun sammenlignes, når de bruger samme "
                    "objektiv, data og konventioner.",
                ),
                (
                    (
                        "Las responsabilidades se normalizan dentro del conjunto candidato definido "
                        "por el modelo de ocurrencia.",
                        "Responsibilities are normalized within the candidate set defined by the "
                        "occurrence model.",
                        "Ansvar normaliseres inden for kandidatsættet defineret af "
                        "forekomstmodellen.",
                    ),
                    (
                        "El M-step usa conteos esperados fraccionarios, no sólo ventanas argmax.",
                        "The M-step uses fractional expected counts, not only argmax windows.",
                        "M-trinnet bruger fraktionelle forventede tællinger, ikke kun "
                        "argmax-vinduer.",
                    ),
                    (
                        "La likelihood observada debe ser monótona salvo tolerancia numérica.",
                        "Observed-data likelihood should be monotone up to numerical tolerance.",
                        "Observeret likelihood bør være monoton inden for numerisk tolerance.",
                    ),
                    (
                        "La tolerancia y el máximo de iteraciones son partes distintas del contrato.",
                        "Tolerance and maximum iterations are distinct parts of the contract.",
                        "Tolerance og maksimalt antal iterationer er forskellige dele af "
                        "kontrakten.",
                    ),
                ),
            ),
        ),
        worked_examples=module.worked_examples
        + (
            example(
                "m08.bg.e01",
                (
                    "Actualizar una PWM con responsabilidades fraccionarias",
                    "Update a PWM with fractional responsibilities",
                    "Opdatér en PWM med fraktionelle ansvar",
                ),
                (
                    "Dos secuencias tienen dos ventanas candidatas cada una. Usa las "
                    "responsabilidades OOPS y un pseudoconteo de uno para construir la nueva PWM.",
                    "Two sequences have two candidate windows each. Use OOPS responsibilities "
                    "and a pseudocount of one to build the new PWM.",
                    "To sekvenser har hver to kandidatvinduer. Brug OOPS-ansvar og en "
                    "pseudotælling på én til at bygge den nye PWM.",
                ),
                (
                    (
                        "Las responsabilidades de cada secuencia deben sumar uno.",
                        "Responsibilities for each sequence must sum to one.",
                        "Ansvarene for hver sekvens skal summere til én.",
                    ),
                    (
                        "Cada base recibe el peso de la ventana que la contiene.",
                        "Each base receives the weight of the window containing it.",
                        "Hver base modtager vægten fra vinduet, der indeholder den.",
                    ),
                    (
                        "La normalización se realiza por columna después de añadir el prior.",
                        "Normalization is performed by column after adding the prior.",
                        "Normalisering udføres pr. kolonne efter tilføjelse af prioren.",
                    ),
                ),
                "def weighted_pwm(\n"
                "    candidate_sites: tuple[tuple[str, ...], ...],\n"
                "    responsibilities: tuple[tuple[float, ...], ...],\n"
                "    pseudocount: float = 1.0,\n"
                ") -> list[dict[str, float]]:\n"
                "    alphabet = 'ACGT'\n"
                "    width = len(candidate_sites[0][0])\n"
                "    counts = [{base: pseudocount for base in alphabet} for _ in range(width)]\n"
                "    for sites, weights in zip(candidate_sites, responsibilities, strict=True):\n"
                "        if len(sites) != len(weights) or abs(sum(weights) - 1.0) > 1e-9:\n"
                "            raise ValueError('responsibilities must align and sum to one')\n"
                "        for site, weight in zip(sites, weights, strict=True):\n"
                "            if len(site) != width:\n"
                "                raise ValueError('all candidate sites must share a width')\n"
                "            for position, base in enumerate(site):\n"
                "                counts[position][base] += weight\n"
                "    pwm = []\n"
                "    for column in counts:\n"
                "        total = sum(column.values())\n"
                "        pwm.append({base: round(column[base] / total, 3) for base in alphabet})\n"
                "    return pwm\n"
                "\n"
                "\n"
                "sites = (('AC', 'GT'), ('AT', 'GC'))\n"
                "weights = ((0.8, 0.2), (0.6, 0.4))\n"
                "print(weighted_pwm(sites, weights))",
                "[{'A': 0.4, 'C': 0.167, 'G': 0.267, 'T': 0.167}, "
                "{'A': 0.167, 'C': 0.367, 'G': 0.167, 'T': 0.3}]",
                (
                    "Cada columna contiene dos unidades esperadas procedentes de las dos "
                    "secuencias y cuatro unidades de pseudoconteo. El resultado es una "
                    "actualización suave; no se descartaron las ventanas con responsabilidad "
                    "menor.",
                    "Each column contains two expected units from the two sequences and four "
                    "pseudocount units. The result is a soft update; lower-responsibility windows "
                    "were not discarded.",
                    "Hver kolonne indeholder to forventede enheder fra de to sekvenser og fire "
                    "pseudotællingsenheder. Resultatet er en blød opdatering; vinduer med lavere "
                    "ansvar blev ikke kasseret.",
                ),
            ),
        ),
        practice_exercises=module.practice_exercises
        + (
            practice(
                "m08.bg.p01",
                ActivityType.DEBUGGING,
                (
                    "Tras un M-step, la likelihood observada cae de -120.4 a -126.1. La "
                    "implementación también convierte responsabilidades en argmax antes de contar. "
                    "Diagnostica el problema y define una comprobación de convergencia válida.",
                    "After an M-step, observed-data likelihood falls from -120.4 to -126.1. The "
                    "implementation also converts responsibilities to argmax before counting. "
                    "Diagnose the problem and define a valid convergence check.",
                    "Efter et M-trin falder den observerede likelihood fra -120,4 til -126,1. "
                    "Implementeringen konverterer også ansvar til argmax før optælling. "
                    "Diagnosticér problemet og definér en gyldig konvergenskontrol.",
                ),
                (
                    (
                        "EM suave conserva pesos fraccionarios.",
                        "Soft EM retains fractional weights.",
                        "Blød EM bevarer fraktionelle vægte.",
                    ),
                    (
                        "Evalúa exactamente el mismo objetivo antes y después.",
                        "Evaluate exactly the same objective before and after.",
                        "Evaluér præcis det samme objektiv før og efter.",
                    ),
                ),
                (
                    "El argmax cambia el algoritmo a asignación dura y rompe la garantía del "
                    "M-step suave. Restaurar responsabilidades normalizadas, usar conteos "
                    "fraccionarios, el mismo fondo, pseudoconteos y modelo de ocurrencia en ambos "
                    "pasos, y recalcular la misma likelihood observada. Permitir sólo una caída "
                    "compatible con error numérico; una caída material debe detener la ejecución. "
                    "Declarar convergencia cuando la mejora absoluta o relativa sea menor que la "
                    "tolerancia, con un máximo de iteraciones como salvaguarda y registro completo "
                    "de la trayectoria.",
                    "Argmax changes the algorithm to hard assignment and breaks the soft M-step "
                    "guarantee. Restore normalized responsibilities, fractional counts, and the "
                    "same background, pseudocounts, and occurrence model in both steps, then "
                    "recompute the same observed-data likelihood. Allow only a decrease compatible "
                    "with numerical error; a material decrease should stop execution. Declare "
                    "convergence when absolute or relative improvement is below tolerance, with a "
                    "maximum iteration safeguard and a complete objective trace.",
                    "Argmax ændrer algoritmen til hård tildeling og bryder garantien for det bløde "
                    "M-trin. Gendan normaliserede ansvar, fraktionelle tællinger og samme baggrund, "
                    "pseudotællinger og forekomstmodel i begge trin, og genberegn den samme "
                    "observerede likelihood. Tillad kun et fald svarende til numerisk fejl; et "
                    "materielt fald bør stoppe kørslen. Erklær konvergens, når den absolutte eller "
                    "relative forbedring er under tolerancen, med en maksimal iterationsgrænse som "
                    "sikkerhed og et komplet objektivspor.",
                ),
                (
                    "Convergencia, monotonía y límite de iteraciones deben registrarse por separado.",
                    "Convergence, monotonicity, and iteration limit should be recorded separately.",
                    "Konvergens, monotoni og iterationsgrænse bør registreres separat.",
                ),
            ),
        ),
        assessment_items=module.assessment_items
        + (
            objective_mcq(
                "dm847.m08.book.001",
                (
                    "¿Qué cantidades deben alimentar el M-step de un EM suave para motivos?",
                    "Which quantities should feed the M-step of soft EM for motifs?",
                    "Hvilke størrelser bør indgå i M-trinnet i blød EM for motiver?",
                ),
                (
                    (
                        "fractional_counts",
                        (
                            "Conteos de bases ponderados por responsabilidades posteriores.",
                            "Base counts weighted by posterior responsibilities.",
                            "Basetællinger vægtet med posterior-ansvar.",
                        ),
                    ),
                    (
                        "argmax_only",
                        (
                            "Sólo la ventana argmax de cada secuencia.",
                            "Only the argmax window from each sequence.",
                            "Kun argmax-vinduet fra hver sekvens.",
                        ),
                    ),
                    (
                        "unscaled_scores",
                        (
                            "Scores sin normalizar tratados como probabilidades.",
                            "Unnormalized scores treated as probabilities.",
                            "Ikke-normaliserede scores behandlet som sandsynligheder.",
                        ),
                    ),
                ),
                "fractional_counts",
                (
                    "El M-step suave usa expectativas fraccionarias. Argmax corresponde a una "
                    "variante de asignación dura, y los scores deben normalizarse antes de actuar "
                    "como responsabilidades.",
                    "The soft M-step uses fractional expectations. Argmax belongs to a "
                    "hard-assignment variant, and scores must be normalized before acting as "
                    "responsibilities.",
                    "Det bløde M-trin bruger fraktionelle forventninger. Argmax hører til en "
                    "variant med hård tildeling, og scores skal normaliseres, før de fungerer som "
                    "ansvar.",
                ),
            ),
        ),
    )
    return _with_source_basis(
        extended,
        (
            "sdu-dm847-active-2025",
            "compeau-pevzner-v1-ch02",
            "compeau-pevzner-v2-ch08",
        ),
    )


def _extend_biological_networks(module: LocalizedLearningModule) -> LocalizedLearningModule:
    """Distinguish predefined enrichment from connected active-subnetwork extraction."""

    extended = replace(
        module,
        objectives=module.objectives
        + (
            objective(
                "m09.bg.o1",
                (
                    "Distinguir enriquecimiento sobre conjuntos predefinidos de extracción de "
                    "subredes activas conectadas y declarar la hipótesis, score, restricciones y "
                    "nulo de cada análisis.",
                    "Distinguish enrichment over predefined sets from connected active-subnetwork "
                    "extraction and state the hypothesis, score, constraints, and null model for "
                    "each analysis.",
                    "Skelne berigelse over prædefinerede sæt fra udtræk af forbundne aktive "
                    "subnetværk og angive hypotese, score, begrænsninger og nulmodel for hver "
                    "analyse.",
                ),
            ),
        ),
        concepts=module.concepts
        + (
            concept(
                "predefined-enrichment-vs-active-subnetworks",
                (
                    "Conjuntos predefinidos frente a subredes activas",
                    "Predefined sets versus active subnetworks",
                    "Prædefinerede sæt versus aktive subnetværk",
                ),
                (
                    "El análisis de sobrerrepresentación parte de conjuntos funcionales "
                    "predefinidos y pregunta si una lista seleccionada se solapa con cada conjunto "
                    "más de lo esperado bajo un universo e hipótesis hipergeométrica. La unidad de "
                    "resultado es un término ya definido. La extracción de subredes activas parte "
                    "de una red de interacción y evidencia cuantitativa o binaria en sus nodos, y "
                    "busca subconjuntos conectados que satisfagan un objetivo o restricciones. "
                    "jActiveModules representa los nodos mediante scores, por ejemplo Z-scores "
                    "derivados de evidencia por gen, y busca módulos conectados con un agregado "
                    "normalizado por tamaño; el procedimiento de búsqueda es heurístico y no "
                    "garantiza el óptimo global. KeyPathwayMiner busca subredes conectadas que "
                    "contienen principalmente nodos activos y permite excepciones explícitas entre "
                    "genes o casos según sus parámetros. Estos métodos responden preguntas "
                    "distintas: un módulo seleccionado no es automáticamente una pathway anotada, "
                    "su score no es necesariamente un p-valor calibrado y su significación no puede "
                    "evaluarse como si el módulo hubiese sido fijado antes de observar los datos. "
                    "La validación debe reproducir el proceso de selección bajo un nulo apropiado, "
                    "perturbar red y datos, conservar conectividad y reportar versiones, IDs, "
                    "evidencia de aristas, parámetros y soluciones alternativas.",
                    "Over-representation analysis begins with predefined functional sets and asks "
                    "whether a selected list overlaps each set more than expected under a defined "
                    "universe and hypergeometric null. Its result unit is an already defined term. "
                    "Active-subnetwork extraction begins with an interaction network and "
                    "quantitative or binary node evidence, then searches for connected subsets "
                    "satisfying an objective or constraints. jActiveModules represents nodes with "
                    "scores, such as Z-scores derived from gene-level evidence, and searches for "
                    "connected modules with a size-normalized aggregate; its search is heuristic "
                    "and does not guarantee the global optimum. KeyPathwayMiner searches for "
                    "connected subnetworks containing mostly active nodes while allowing explicit "
                    "gene- or case-level exceptions through its parameters. These methods answer "
                    "different questions: a selected module is not automatically an annotated "
                    "pathway, its score is not necessarily a calibrated p-value, and significance "
                    "cannot be assessed as though the module had been fixed before seeing the data. "
                    "Validation should reproduce the selection process under an appropriate null, "
                    "perturb the network and measurements, preserve connectivity, and report "
                    "versions, identifiers, edge evidence, parameters, and alternative solutions.",
                    "Overrepræsentationsanalyse starter med prædefinerede funktionelle sæt og "
                    "spørger, om en valgt liste overlapper hvert sæt mere end forventet under et "
                    "defineret univers og en hypergeometrisk nulmodel. Resultatenheden er en "
                    "allerede defineret term. Udtræk af aktive subnetværk starter med et "
                    "interaktionsnetværk og kvantitativ eller binær evidens på noderne og søger "
                    "efter forbundne delmængder, der opfylder et objektiv eller begrænsninger. "
                    "jActiveModules repræsenterer noder med scores, eksempelvis Z-scores afledt af "
                    "evidens pr. gen, og søger efter forbundne moduler med et størrelsesnormaliseret "
                    "aggregat; søgningen er heuristisk og garanterer ikke det globale optimum. "
                    "KeyPathwayMiner søger efter forbundne subnetværk med hovedsageligt aktive "
                    "noder og tillader eksplicitte undtagelser mellem gener eller cases gennem "
                    "parametrene. Metoderne besvarer forskellige spørgsmål: et valgt modul er ikke "
                    "automatisk en annoteret pathway, dets score er ikke nødvendigvis en kalibreret "
                    "p-værdi, og signifikans kan ikke vurderes, som om modulet var fastlagt før "
                    "dataene blev set. Validering bør gentage selektionsprocessen under en passende "
                    "nulmodel, perturbere netværk og målinger, bevare konnektivitet og rapportere "
                    "versioner, identifikatorer, kantevidens, parametre og alternative løsninger.",
                ),
                (
                    (
                        "ORA prueba términos fijados antes del análisis; active-module mining "
                        "selecciona una subred a partir de los datos.",
                        "ORA tests terms fixed before analysis; active-module mining selects a "
                        "subnetwork from the data.",
                        "ORA tester termer fastlagt før analysen; active-module mining vælger et "
                        "subnetværk fra dataene.",
                    ),
                    (
                        "La conectividad forma parte de la definición de una subred activa.",
                        "Connectivity is part of the active-subnetwork definition.",
                        "Konnektivitet er en del af definitionen af et aktivt subnetværk.",
                    ),
                    (
                        "Un score de módulo no debe etiquetarse como p-valor sin calibración.",
                        "A module score should not be labeled a p-value without calibration.",
                        "En modulscore bør ikke kaldes en p-værdi uden kalibrering.",
                    ),
                    (
                        "El nulo debe repetir selección, restricciones y sesgos de la red.",
                        "The null model should repeat selection, constraints, and network biases.",
                        "Nulmodellen bør gentage selektion, begrænsninger og netværksbias.",
                    ),
                ),
            ),
        ),
        worked_examples=module.worked_examples
        + (
            example(
                "m09.bg.e01",
                (
                    "Comparar scores de módulos conectados",
                    "Compare connected-module scores",
                    "Sammenlign scores for forbundne moduler",
                ),
                (
                    "Calcula un agregado normalizado por tamaño para dos subredes conectadas. "
                    "Observa que añadir un nodo con evidencia negativa puede reducir el score.",
                    "Compute a size-normalized aggregate for two connected subnetworks. Observe "
                    "that adding a node with negative evidence can reduce the score.",
                    "Beregn et størrelsesnormaliseret aggregat for to forbundne subnetværk. "
                    "Bemærk, at tilføjelse af en node med negativ evidens kan reducere scoren.",
                ),
                (
                    (
                        "Verifica conectividad antes de puntuar.",
                        "Verify connectivity before scoring.",
                        "Kontrollér konnektivitet før scoring.",
                    ),
                    (
                        "Suma los Z-scores y divide por la raíz del tamaño.",
                        "Sum Z-scores and divide by the square root of size.",
                        "Summér Z-scores og dividér med kvadratroden af størrelsen.",
                    ),
                    (
                        "El valor sirve para comparar candidatos bajo la misma convención.",
                        "The value compares candidates under the same convention.",
                        "Værdien sammenligner kandidater under samme konvention.",
                    ),
                ),
                "from math import sqrt\n"
                "\n"
                "\n"
                "def connected_module_score(\n"
                "    nodes: set[str],\n"
                "    z_scores: dict[str, float],\n"
                "    adjacency: dict[str, set[str]],\n"
                ") -> float:\n"
                "    if not nodes:\n"
                "        raise ValueError('module cannot be empty')\n"
                "    start = next(iter(nodes))\n"
                "    visited = {start}\n"
                "    stack = [start]\n"
                "    while stack:\n"
                "        node = stack.pop()\n"
                "        for neighbor in adjacency[node] & nodes:\n"
                "            if neighbor not in visited:\n"
                "                visited.add(neighbor)\n"
                "                stack.append(neighbor)\n"
                "    if visited != nodes:\n"
                "        raise ValueError('module must be connected')\n"
                "    return sum(z_scores[node] for node in nodes) / sqrt(len(nodes))\n"
                "\n"
                "\n"
                "adjacency = {\n"
                "    'A': {'B'},\n"
                "    'B': {'A', 'C'},\n"
                "    'C': {'B'},\n"
                "}\n"
                "z_scores = {'A': 3.0, 'B': 2.0, 'C': -1.0}\n"
                "modules = {'AB': {'A', 'B'}, 'ABC': {'A', 'B', 'C'}}\n"
                "print(\n"
                "    {\n"
                "        name: round(connected_module_score(nodes, z_scores, adjacency), 3)\n"
                "        for name, nodes in modules.items()\n"
                "    }\n"
                ")",
                "{'AB': 3.536, 'ABC': 2.309}",
                (
                    "Ambos candidatos son conectados, pero ABC recibe un score menor porque C "
                    "aporta evidencia negativa. El score no es un p-valor y no corrige el hecho de "
                    "que muchos módulos pudieron ser examinados.",
                    "Both candidates are connected, but ABC scores lower because C contributes "
                    "negative evidence. The score is not a p-value and does not correct for the "
                    "many modules that may have been examined.",
                    "Begge kandidater er forbundne, men ABC får en lavere score, fordi C bidrager "
                    "med negativ evidens. Scoren er ikke en p-værdi og korrigerer ikke for de mange "
                    "moduler, der kan være blevet undersøgt.",
                ),
            ),
        ),
        practice_exercises=module.practice_exercises
        + (
            practice(
                "m09.bg.p01",
                ActivityType.PIPELINE_DESIGN,
                (
                    "Dispones de genes diferencialmente expresados, una colección de pathways "
                    "curadas y una red PPI. Diseña dos análisis separados: uno de "
                    "sobrerrepresentación y otro de subred activa. Define pregunta, entrada, "
                    "salida, nulo y validación para cada uno.",
                    "You have differentially expressed genes, a curated pathway collection, and a "
                    "PPI network. Design two separate analyses: over-representation and active "
                    "subnetwork extraction. Define the question, input, output, null, and "
                    "validation for each.",
                    "Du har differentielt udtrykte gener, en kurateret pathway-samling og et "
                    "PPI-netværk. Design to separate analyser: overrepræsentation og udtræk af et "
                    "aktivt subnetværk. Definér spørgsmål, input, output, nulmodel og validering "
                    "for hver.",
                ),
                (
                    (
                        "No uses el mismo p-valor para preguntas distintas.",
                        "Do not use the same p-value for different questions.",
                        "Brug ikke den samme p-værdi til forskellige spørgsmål.",
                    ),
                    (
                        "La selección de módulos debe reproducirse en el nulo.",
                        "Module selection should be reproduced in the null model.",
                        "Modulselektion bør gentages i nulmodellen.",
                    ),
                ),
                (
                    "ORA: preguntar qué pathways predefinidas están sobrerrepresentadas; usar la "
                    "lista, conjuntos curados y universo detectable; devolver términos, overlap, "
                    "efecto y FDR; usar el nulo hipergeométrico y validar sensibilidad al universo, "
                    "mapeo y redundancia. Subred activa: preguntar qué región conectada concentra "
                    "evidencia; usar la PPI versionada, scores por nodo y parámetros de score o "
                    "excepciones; devolver nodos, aristas, score y soluciones alternativas; "
                    "calibrar mediante permutaciones o simulaciones que repitan búsqueda, "
                    "conectividad, grado y sesgos, y validar por perturbación de scores, red "
                    "independiente y estabilidad. No llamar pathway al módulo sólo por ser "
                    "conectado.",
                    "ORA: ask which predefined pathways are over-represented; use the list, "
                    "curated sets, and detectable universe; return terms, overlap, effect, and FDR; "
                    "use the hypergeometric null and validate sensitivity to universe, mapping, and "
                    "redundancy. Active subnetwork: ask which connected region concentrates "
                    "evidence; use a versioned PPI network, node scores, and score or exception "
                    "parameters; return nodes, edges, score, and alternative solutions; calibrate "
                    "with permutations or simulations that repeat search, connectivity, degree, "
                    "and biases, and validate through score perturbation, an independent network, "
                    "and stability. Do not call a module a pathway merely because it is connected.",
                    "ORA: spørg hvilke prædefinerede pathways der er overrepræsenterede; brug "
                    "listen, kuraterede sæt og det detekterbare univers; returnér termer, overlap, "
                    "effekt og FDR; brug den hypergeometriske nulmodel og validér følsomhed over for "
                    "univers, mapping og redundans. Aktivt subnetværk: spørg hvilken forbundet "
                    "region der koncentrerer evidens; brug et versioneret PPI-netværk, nodescores og "
                    "score- eller undtagelsesparametre; returnér noder, kanter, score og alternative "
                    "løsninger; kalibrér med permutationer eller simuleringer, der gentager søgning, "
                    "konnektivitet, grad og bias, og validér gennem scoreperturbation, et uafhængigt "
                    "netværk og stabilitet. Kald ikke et modul en pathway alene, fordi det er "
                    "forbundet.",
                ),
                (
                    "Los dos análisis pueden complementarse, pero sus hipótesis y procesos de "
                    "selección no son intercambiables.",
                    "The two analyses can complement each other, but their hypotheses and "
                    "selection processes are not interchangeable.",
                    "De to analyser kan supplere hinanden, men deres hypoteser og "
                    "selektionsprocesser er ikke udskiftelige.",
                ),
            ),
        ),
        assessment_items=module.assessment_items
        + (
            objective_mcq(
                "dm847.m09.book.001",
                (
                    "¿Qué rasgo distingue principalmente la extracción de una subred activa de "
                    "un ORA convencional?",
                    "Which feature primarily distinguishes active-subnetwork extraction from "
                    "conventional ORA?",
                    "Hvilket træk adskiller primært udtræk af aktive subnetværk fra konventionel "
                    "ORA?",
                ),
                (
                    (
                        "connected_selection",
                        (
                            "Selecciona desde los datos un conjunto conectado bajo un score o "
                            "restricciones.",
                            "It selects a connected set from the data under a score or constraints.",
                            "Den vælger et forbundet sæt fra data under en score eller "
                            "begrænsninger.",
                        ),
                    ),
                    (
                        "fixed_terms",
                        (
                            "Sólo prueba términos funcionales fijados previamente.",
                            "It only tests functional terms fixed in advance.",
                            "Den tester kun funktionelle termer fastlagt på forhånd.",
                        ),
                    ),
                    (
                        "universal_pvalue",
                        (
                            "Produce siempre un p-valor universalmente calibrado.",
                            "It always produces a universally calibrated p-value.",
                            "Den producerer altid en universelt kalibreret p-værdi.",
                        ),
                    ),
                ),
                "connected_selection",
                (
                    "La subred se selecciona usando topología y evidencia. Esa selección debe "
                    "formar parte de la calibración; ORA convencional prueba conjuntos definidos "
                    "antes de observar la lista.",
                    "The subnetwork is selected using topology and evidence. That selection must "
                    "be part of calibration; conventional ORA tests sets defined before observing "
                    "the list.",
                    "Subnetværket vælges med topologi og evidens. Denne selektion skal indgå i "
                    "kalibreringen; konventionel ORA tester sæt defineret før listen observeres.",
                ),
            ),
        ),
    )
    return _with_source_basis(
        extended,
        (
            "sdu-dm847-active-2025",
            "ideker-2002-active-modules",
            "alcaraz-2012-keypathwayminer",
        ),
    )


def apply_motif_network_extensions(
    modules: tuple[LocalizedLearningModule, ...],
) -> tuple[LocalizedLearningModule, ...]:
    """Apply focused M08 and M09 extensions without changing other modules."""

    return tuple(
        _extend_motif_discovery(module)
        if module.module_id == "dm847.m08"
        else _extend_biological_networks(module)
        if module.module_id == "dm847.m09"
        else module
        for module in modules
    )


__all__ = [
    "DM847_NETWORK_SOURCES",
    "apply_motif_network_extensions",
    "update_motif_network_audit",
    "update_motif_network_source_catalog",
]
