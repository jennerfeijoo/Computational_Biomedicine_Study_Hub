"""DM847 module 5: hidden Markov models for biological sequences."""

from __future__ import annotations

from ...i18n import AppLocale
from ..localized_models import LocalizedLearningModule
from ..models import AssessmentItem, LearningModule
from .standard import StandardModuleSpec, build_module, build_question_bank, materialize_bank

_SPEC = StandardModuleSpec(
    module_id="dm847.m05",
    title=(
        "Modelos ocultos de Markov para secuencias",
        "Hidden Markov models for sequences",
        "Skjulte Markov-modeller for sekvenser",
    ),
    summary=(
        "Construye HMM con estados, transiciones y emisiones; calcula probabilidades con Forward, decodifica con Viterbi, interpreta aprendizaje de parámetros y conecta el modelo con perfiles de secuencia.",
        "Build HMMs with states, transitions, and emissions; compute probabilities with Forward, decode with Viterbi, interpret parameter learning, and connect the model to sequence profiles.",
        "Byg HMM'er med tilstande, overgange og emissioner; beregn sandsynligheder med Forward, dekod med Viterbi, fortolk parameterlæring og forbind modellen med sekvensprofiler.",
    ),
    objectives=(
        (
            "m05.o1",
            (
                "Definir estados ocultos, observaciones, transiciones y emisiones.",
                "Define hidden states, observations, transitions, and emissions.",
                "Definere skjulte tilstande, observationer, overgange og emissioner.",
            ),
        ),
        (
            "m05.o2",
            (
                "Calcular la probabilidad conjunta de una ruta y una secuencia.",
                "Compute the joint probability of a path and sequence.",
                "Beregne den fælles sandsynlighed for en sti og en sekvens.",
            ),
        ),
        (
            "m05.o3",
            (
                "Aplicar el algoritmo Forward con escalado o logaritmos.",
                "Apply the Forward algorithm with scaling or logs.",
                "Anvende Forward-algoritmen med skalering eller logaritmer.",
            ),
        ),
        (
            "m05.o4",
            (
                "Aplicar Viterbi y distinguir ruta más probable de probabilidad total.",
                "Apply Viterbi and distinguish most probable path from total probability.",
                "Anvende Viterbi og skelne mest sandsynlige sti fra total sandsynlighed.",
            ),
        ),
        (
            "m05.o5",
            (
                "Explicar estimación supervisada y Baum–Welch.",
                "Explain supervised estimation and Baum–Welch.",
                "Forklare superviseret estimering og Baum–Welch.",
            ),
        ),
        (
            "m05.o6",
            (
                "Interpretar HMM de perfil y validar supuestos probabilísticos.",
                "Interpret profile HMMs and validate probabilistic assumptions.",
                "Fortolke profil-HMM'er og validere probabilistiske antagelser.",
            ),
        ),
    ),
    concepts=(
        (
            "hmm-components",
            ("Componentes de un HMM", "HMM components", "HMM-komponenter"),
            (
                "Un HMM contiene estados ocultos, distribución inicial, probabilidades de transición y distribuciones de emisión. La propiedad de Markov condiciona el siguiente estado al actual, y la emisión depende del estado actual. Las filas probabilísticas deben sumar uno y los ceros estructurales expresan transiciones imposibles.",
                "An HMM contains hidden states, an initial distribution, transition probabilities, and emission distributions. The Markov property conditions the next state on the current state, and emission depends on the current state. Probability rows should sum to one, and structural zeros express impossible transitions.",
                "En HMM indeholder skjulte tilstande, en initialfordeling, overgangssandsynligheder og emissionsfordelinger. Markov-egenskaben betinger næste tilstand på den aktuelle, og emissionen afhænger af den aktuelle tilstand. Sandsynlighedsrækker bør summere til én, og strukturelle nuller udtrykker umulige overgange.",
            ),
            (
                (
                    "Estados y observaciones no son la misma variable.",
                    "States and observations are not the same variable.",
                    "Tilstande og observationer er ikke samme variabel.",
                ),
                (
                    "Cada distribución debe normalizarse.",
                    "Each distribution must be normalized.",
                    "Hver fordeling skal normaliseres.",
                ),
            ),
        ),
        (
            "joint-probability",
            ("Probabilidad conjunta", "Joint probability", "Fælles sandsynlighed"),
            (
                "La probabilidad de una ruta y una secuencia es el producto de la probabilidad inicial, las emisiones y las transiciones correspondientes. Esta cantidad permite puntuar una ruta concreta, pero no es la probabilidad marginal de la secuencia, que requiere sumar sobre todas las rutas.",
                "The probability of a path and sequence is the product of the initial probability, corresponding emissions, and transitions. This quantity scores a specific path but is not the marginal probability of the sequence, which requires summing over all paths.",
                "Sandsynligheden for en sti og sekvens er produktet af initial sandsynlighed, relevante emissioner og overgange. Denne størrelse scorer en bestemt sti, men er ikke den marginale sandsynlighed for sekvensen, som kræver summering over alle stier.",
            ),
            (
                ("Ruta concreta: producto.", "Specific path: product.", "Bestemt sti: produkt."),
                (
                    "Secuencia marginal: suma sobre rutas.",
                    "Marginal sequence: sum over paths.",
                    "Marginal sekvens: sum over stier.",
                ),
            ),
        ),
        (
            "forward",
            ("Algoritmo Forward", "Forward algorithm", "Forward-algoritmen"),
            (
                "Forward acumula la probabilidad de todas las rutas que terminan en cada estado después de observar un prefijo. La recurrencia suma contribuciones de estados previos y multiplica por la emisión actual. El coste es O(TK²) para T observaciones y K estados densamente conectados.",
                "Forward accumulates the probability of all paths ending in each state after an observed prefix. The recurrence sums contributions from previous states and multiplies by the current emission. Cost is O(TK²) for T observations and K densely connected states.",
                "Forward akkumulerer sandsynligheden for alle stier, der ender i hver tilstand efter et observeret præfiks. Rekurrensen summerer bidrag fra tidligere tilstande og multiplicerer med den aktuelle emission. Omkostningen er O(TK²) for T observationer og K tæt forbundne tilstande.",
            ),
            (
                (
                    "Forward suma, no maximiza.",
                    "Forward sums; it does not maximize.",
                    "Forward summerer; den maksimerer ikke.",
                ),
                (
                    "El último total es la probabilidad de la secuencia.",
                    "The final total is sequence probability.",
                    "Den sidste sum er sekvensens sandsynlighed.",
                ),
            ),
        ),
        (
            "viterbi",
            ("Algoritmo Viterbi", "Viterbi algorithm", "Viterbi-algoritmen"),
            (
                "Viterbi sustituye la suma por un máximo y guarda predecesores para reconstruir la ruta más probable. La ruta Viterbi no representa la incertidumbre completa y puede diferir de elegir el estado posterior más probable de forma independiente en cada posición.",
                "Viterbi replaces summation with a maximum and stores predecessors to reconstruct the most probable path. The Viterbi path does not represent full uncertainty and may differ from independently selecting the most probable posterior state at each position.",
                "Viterbi erstatter summering med maksimum og lagrer forgængere for at rekonstruere den mest sandsynlige sti. Viterbi-stien repræsenterer ikke fuld usikkerhed og kan afvige fra uafhængigt valg af den mest sandsynlige posterior-tilstand ved hver position.",
            ),
            (
                (
                    "Viterbi maximiza una ruta global.",
                    "Viterbi maximizes one global path.",
                    "Viterbi maksimerer én global sti.",
                ),
                (
                    "Se requiere traceback de estados.",
                    "State traceback is required.",
                    "Traceback af tilstande kræves.",
                ),
            ),
        ),
        (
            "numerical-stability",
            ("Estabilidad numérica", "Numerical stability", "Numerisk stabilitet"),
            (
                "Productos de muchas probabilidades pequeñas producen underflow. El escalado normaliza vectores Forward en cada paso y acumula factores; el dominio log transforma productos en sumas y usa log-sum-exp para sumar probabilidades sin perder precisión.",
                "Products of many small probabilities cause underflow. Scaling normalizes Forward vectors at each step and accumulates factors; log space turns products into sums and uses log-sum-exp to add probabilities without losing precision.",
                "Produkter af mange små sandsynligheder giver underflow. Skalering normaliserer Forward-vektorer ved hvert trin og akkumulerer faktorer; log-rum omdanner produkter til summer og bruger log-sum-exp til at summere sandsynligheder uden præcisionstab.",
            ),
            (
                (
                    "El cero real y el underflow no son equivalentes.",
                    "A true zero and underflow are not equivalent.",
                    "Et ægte nul og underflow er ikke det samme.",
                ),
                (
                    "Log-sum-exp conserva sumas en logaritmos.",
                    "Log-sum-exp preserves sums in log space.",
                    "Log-sum-exp bevarer summer i log-rum.",
                ),
            ),
        ),
        (
            "learning-profile",
            ("Aprendizaje y HMM de perfil", "Learning and profile HMMs", "Læring og profil-HMM'er"),
            (
                "Con rutas conocidas, transiciones y emisiones se estiman por conteos suavizados. Baum–Welch usa expectativas de ocupación y transición para actualizar parámetros, pero puede converger a óptimos locales. Un HMM de perfil representa posiciones conservadas mediante estados match, inserciones y eliminaciones, y su arquitectura depende del alineamiento de entrenamiento.",
                "With known paths, transitions and emissions are estimated from smoothed counts. Baum–Welch uses expected occupancy and transition counts to update parameters but may converge to local optima. A profile HMM represents conserved positions through match, insertion, and deletion states, and its architecture depends on the training alignment.",
                "Med kendte stier estimeres overgange og emissioner fra smoothede tællinger. Baum–Welch bruger forventede opholds- og overgangstal til at opdatere parametre, men kan konvergere til lokale optima. En profil-HMM repræsenterer konserverede positioner gennem match-, insertions- og deletionstilstande, og arkitekturen afhænger af træningsalignmenten.",
            ),
            (
                (
                    "Suavizado evita probabilidades cero accidentales.",
                    "Smoothing avoids accidental zero probabilities.",
                    "Smoothing undgår utilsigtede nulsandsynligheder.",
                ),
                (
                    "El entrenamiento no garantiza óptimo global.",
                    "Training does not guarantee a global optimum.",
                    "Træning garanterer ikke globalt optimum.",
                ),
            ),
        ),
    ),
    examples=(
        (
            "m05.e01",
            ("Probabilidad de una ruta", "Path probability", "Stisandsynlighed"),
            (
                "Calcula la probabilidad conjunta para dos estados y tres observaciones.",
                "Compute joint probability for two states and three observations.",
                "Beregn fælles sandsynlighed for to tilstande og tre observationer.",
            ),
            (
                (
                    "Multiplica inicial y primera emisión.",
                    "Multiply initial and first emission.",
                    "Multiplicér initial og første emission.",
                ),
                (
                    "Después alterna transición y emisión.",
                    "Then alternate transition and emission.",
                    "Skift derefter mellem overgang og emission.",
                ),
            ),
            """def joint_probability(\n    path: list[str], observations: list[str], initial: dict[str, float],\n    transitions: dict[str, dict[str, float]], emissions: dict[str, dict[str, float]],\n) -> float:\n    probability = initial[path[0]] * emissions[path[0]][observations[0]]\n    for previous, current, symbol in zip(path, path[1:], observations[1:], strict=True):\n        probability *= transitions[previous][current] * emissions[current][symbol]\n    return probability\n\n\ninitial = {\"H\": 0.5, \"L\": 0.5}\ntransitions = {\"H\": {\"H\": 0.7, \"L\": 0.3}, \"L\": {\"H\": 0.4, \"L\": 0.6}}\nemissions = {\"H\": {\"G\": 0.8, \"A\": 0.2}, \"L\": {\"G\": 0.3, \"A\": 0.7}}\nprint(round(joint_probability([\"H\", \"H\", \"L\"], [\"G\", \"G\", \"A\"], initial, transitions, emissions), 4))\n""",
            "0.047",
            (
                "Es la probabilidad de esa ruta concreta, no de todas las rutas compatibles.",
                "This is the probability of that specific path, not all compatible paths.",
                "Det er sandsynligheden for den konkrete sti, ikke alle kompatible stier.",
            ),
        ),
        (
            "m05.e02",
            ("Forward para dos estados", "Forward for two states", "Forward for to tilstande"),
            (
                "Suma todas las rutas posibles para una secuencia corta.",
                "Sum all possible paths for a short sequence.",
                "Summér alle mulige stier for en kort sekvens.",
            ),
            (
                (
                    "Inicializa con emisión de la primera observación.",
                    "Initialize with the first observation emission.",
                    "Initialisér med emissionen for første observation.",
                ),
                (
                    "Cada paso suma entradas por transición.",
                    "Each step sums incoming transition contributions.",
                    "Hvert trin summerer indgående overgangsbidrag.",
                ),
            ),
            """def forward_probability(observations, states, initial, transitions, emissions):\n    forward = {state: initial[state] * emissions[state][observations[0]] for state in states}\n    for symbol in observations[1:]:\n        forward = {\n            state: emissions[state][symbol]\n            * sum(previous_score * transitions[previous][state] for previous, previous_score in forward.items())\n            for state in states\n        }\n    return sum(forward.values())\n\n\nstates = (\"H\", \"L\")\ninitial = {\"H\": 0.5, \"L\": 0.5}\ntransitions = {\"H\": {\"H\": 0.7, \"L\": 0.3}, \"L\": {\"H\": 0.4, \"L\": 0.6}}\nemissions = {\"H\": {\"G\": 0.8, \"A\": 0.2}, \"L\": {\"G\": 0.3, \"A\": 0.7}}\nprint(round(forward_probability(\"GA\", states, initial, transitions, emissions), 4))\n""",
            "0.22",
            (
                "El resultado marginaliza las cuatro rutas de longitud dos.",
                "The result marginalizes the four paths of length two.",
                "Resultatet marginaliserer de fire stier med længde to.",
            ),
        ),
        (
            "m05.e03",
            ("Viterbi en logaritmos", "Viterbi in log space", "Viterbi i log-rum"),
            (
                "Decodifica la ruta más probable evitando productos pequeños.",
                "Decode the most probable path while avoiding small products.",
                "Dekod den mest sandsynlige sti og undgå små produkter.",
            ),
            (
                (
                    "Los logs convierten productos en sumas.",
                    "Logs turn products into sums.",
                    "Logs omdanner produkter til summer.",
                ),
                (
                    "Cada estado guarda el mejor predecesor.",
                    "Each state stores the best predecessor.",
                    "Hver tilstand lagrer den bedste forgænger.",
                ),
            ),
            """from math import log\n\n\ndef viterbi(observations, states, initial, transitions, emissions):\n    scores = {state: log(initial[state]) + log(emissions[state][observations[0]]) for state in states}\n    paths = {state: [state] for state in states}\n    for symbol in observations[1:]:\n        new_scores, new_paths = {}, {}\n        for state in states:\n            previous = max(states, key=lambda candidate: scores[candidate] + log(transitions[candidate][state]))\n            new_scores[state] = scores[previous] + log(transitions[previous][state]) + log(emissions[state][symbol])\n            new_paths[state] = paths[previous] + [state]\n        scores, paths = new_scores, new_paths\n    final = max(states, key=scores.get)\n    return paths[final]\n\n\nstates = (\"H\", \"L\")\ninitial = {\"H\": 0.5, \"L\": 0.5}\ntransitions = {\"H\": {\"H\": 0.7, \"L\": 0.3}, \"L\": {\"H\": 0.4, \"L\": 0.6}}\nemissions = {\"H\": {\"G\": 0.8, \"A\": 0.2}, \"L\": {\"G\": 0.3, \"A\": 0.7}}\nprint(viterbi(\"GGA\", states, initial, transitions, emissions))\n""",
            "['H', 'H', 'L']",
            (
                "La ruta maximiza probabilidad conjunta, pero no resume rutas alternativas.",
                "The path maximizes joint probability but does not summarize alternative paths.",
                "Stien maksimerer fælles sandsynlighed, men opsummerer ikke alternative stier.",
            ),
        ),
    ),
    practices=(
        (
            "m05.p01",
            "SHORT_ANSWER",
            (
                "Distingue estado oculto y observación.",
                "Distinguish hidden state and observation.",
                "Skeln mellem skjult tilstand og observation.",
            ),
            (
                (
                    "Usa un ejemplo de región GC.",
                    "Use a GC-region example.",
                    "Brug et eksempel med GC-region.",
                ),
            ),
            (
                "El estado puede representar régimen GC alto o bajo; la observación es la base emitida. El estado no se observa directamente y se infiere desde la secuencia.",
                "The state may represent high- or low-GC regime; the observation is the emitted base. The state is not directly observed and is inferred from sequence.",
                "Tilstanden kan repræsentere et højt eller lavt GC-regime; observationen er den emitterede base. Tilstanden observeres ikke direkte og infereres fra sekvensen.",
            ),
            (
                "La interpretación biológica del estado debe justificarse.",
                "The biological interpretation of state must be justified.",
                "Den biologiske fortolkning af tilstanden skal begrundes.",
            ),
            "",
        ),
        (
            "m05.p02",
            "FILL_IN_THE_BLANK",
            (
                "Forward combina rutas entrantes mediante ____.",
                "Forward combines incoming paths using ____.",
                "Forward kombinerer indgående stier ved ____.",
            ),
            (("No usa máximo.", "It does not use maximum.", "Den bruger ikke maksimum."),),
            ("suma", "summation", "summering"),
            (
                "Viterbi usa máximo; Forward suma.",
                "Viterbi maximizes; Forward sums.",
                "Viterbi maksimerer; Forward summerer.",
            ),
            "",
        ),
        (
            "m05.p03",
            "CODE_TRACING",
            (
                "Una fila de transición [0.8, 0.2] suma ¿cuánto?",
                "What does transition row [0.8, 0.2] sum to?",
                "Hvad summerer overgangsrækken [0.8, 0.2] til?",
            ),
            (("Debe normalizarse.", "It should be normalized.", "Den bør være normaliseret."),),
            ("1.0", "1.0", "1.0"),
            (
                "Cada fila representa una distribución condicional.",
                "Each row is a conditional distribution.",
                "Hver række er en betinget fordeling.",
            ),
            "",
        ),
        (
            "m05.p04",
            "DATA_INTERPRETATION",
            (
                "Forward=0.02 y probabilidad Viterbi=0.008. Interpreta.",
                "Forward=0.02 and Viterbi probability=0.008. Interpret.",
                "Forward=0.02 og Viterbi-sandsynlighed=0.008. Fortolk.",
            ),
            (
                (
                    "Compara suma y máximo.",
                    "Compare sum and maximum.",
                    "Sammenlign sum og maksimum.",
                ),
            ),
            (
                "0.02 suma todas las rutas; 0.008 corresponde a la mejor ruta. Las demás rutas aportan 0.012 en conjunto.",
                "0.02 sums all paths; 0.008 corresponds to the best path. Other paths contribute 0.012 together.",
                "0.02 summerer alle stier; 0.008 svarer til den bedste sti. Andre stier bidrager tilsammen med 0.012.",
            ),
            (
                "La ruta dominante no agota la incertidumbre.",
                "The dominant path does not exhaust uncertainty.",
                "Den dominerende sti udtømmer ikke usikkerheden.",
            ),
            "",
        ),
        (
            "m05.p05",
            "DEBUGGING",
            (
                "Forward devuelve cero para una secuencia larga aunque no hay ceros en parámetros. Diagnostica.",
                "Forward returns zero for a long sequence although parameters contain no zeros. Diagnose it.",
                "Forward returnerer nul for en lang sekvens, selv om parametrene ikke indeholder nuller. Diagnosticér.",
            ),
            (("Piensa en underflow.", "Think underflow.", "Tænk på underflow."),),
            (
                "Usar escalado por posición o dominio log con log-sum-exp; verificar que no se confunde underflow con evento imposible.",
                "Use per-position scaling or log space with log-sum-exp; verify underflow is not confused with an impossible event.",
                "Brug skalering pr. position eller log-rum med log-sum-exp; verificér at underflow ikke forveksles med en umulig hændelse.",
            ),
            (
                "La estabilidad numérica es parte del algoritmo.",
                "Numerical stability is part of the algorithm.",
                "Numerisk stabilitet er en del af algoritmen.",
            ),
            "",
        ),
        (
            "m05.p06",
            "PIPELINE_DESIGN",
            (
                "Diseña validación de un HMM entrenado.",
                "Design validation for a trained HMM.",
                "Design validering af en trænet HMM.",
            ),
            (
                (
                    "Separa ajuste y evaluación.",
                    "Separate fitting and evaluation.",
                    "Adskil tilpasning og evaluering.",
                ),
            ),
            (
                "Comprobar normalización, likelihood en datos retenidos, estabilidad entre inicializaciones, calibración de estados, comparación con baselines y sensibilidad a estructura y smoothing.",
                "Check normalization, held-out likelihood, stability across initializations, state calibration, comparison with baselines, and sensitivity to structure and smoothing.",
                "Kontrollér normalisering, likelihood på hold-out-data, stabilitet mellem initialiseringer, kalibrering af tilstande, sammenligning med baselines og følsomhed over for struktur og smoothing.",
            ),
            (
                "Una likelihood de entrenamiento creciente no garantiza generalización.",
                "Increasing training likelihood does not guarantee generalization.",
                "Stigende trænings-likelihood garanterer ikke generalisering.",
            ),
            "",
        ),
        (
            "m05.p07",
            "ORAL_EXPLANATION",
            (
                "Explica Baum–Welch como EM.",
                "Explain Baum–Welch as EM.",
                "Forklar Baum–Welch som EM.",
            ),
            (("Incluye E y M.", "Include E and M.", "Medtag E og M."),),
            (
                "E-step calcula expectativas de ocupación y transiciones con Forward–Backward; M-step renormaliza conteos esperados para actualizar iniciales, transiciones y emisiones.",
                "The E-step computes expected state occupancy and transitions with Forward–Backward; the M-step renormalizes expected counts to update initial, transition, and emission probabilities.",
                "E-trinnet beregner forventet tilstandsophold og overgange med Forward–Backward; M-trinnet normaliserer forventede tællinger for at opdatere initial-, overgangs- og emissionssandsynligheder.",
            ),
            (
                "Puede converger a un óptimo local.",
                "It may converge to a local optimum.",
                "Den kan konvergere til et lokalt optimum.",
            ),
            "",
        ),
        (
            "m05.p08",
            "MATCHING",
            (
                "Relaciona match, insert y delete en un HMM de perfil.",
                "Match match, insert, and delete in a profile HMM.",
                "Match match, insert og delete i en profil-HMM.",
            ),
            (("Delete es silencioso.", "Delete is silent.", "Delete er tavs."),),
            (
                "Match modela una columna conservada; insert emite residuos adicionales; delete omite una columna de consenso sin emitir.",
                "Match models a conserved column; insert emits additional residues; delete skips a consensus column without emitting.",
                "Match modellerer en konserveret kolonne; insert emitterer ekstra rester; delete springer en konsensuskolonne over uden emission.",
            ),
            (
                "La arquitectura procede del alineamiento de entrenamiento.",
                "Architecture comes from the training alignment.",
                "Arkitekturen kommer fra træningsalignmenten.",
            ),
            "",
        ),
    ),
    mcqs=(
        (
            "001",
            (
                "¿Qué variable no se observa directamente en un HMM?",
                "Which variable is not directly observed in an HMM?",
                "Hvilken variabel observeres ikke direkte i en HMM?",
            ),
            (
                ("state", ("Estado oculto", "Hidden state", "Skjult tilstand")),
                ("symbol", ("Símbolo emitido", "Emitted symbol", "Emitteret symbol")),
                ("sequence", ("Secuencia observada", "Observed sequence", "Observeret sekvens")),
            ),
            "state",
            (
                "El estado se infiere desde observaciones.",
                "State is inferred from observations.",
                "Tilstanden infereres fra observationer.",
            ),
        ),
        (
            "002",
            (
                "¿Qué deben sumar las probabilidades salientes de un estado?",
                "What should outgoing probabilities from a state sum to?",
                "Hvad bør udgående sandsynligheder fra en tilstand summere til?",
            ),
            (
                ("one", ("1", "1", "1")),
                ("zero", ("0", "0", "0")),
                ("states", ("Número de estados", "Number of states", "Antal tilstande")),
            ),
            "one",
            (
                "Forman una distribución condicional.",
                "They form a conditional distribution.",
                "De danner en betinget fordeling.",
            ),
        ),
        (
            "003",
            ("¿Qué calcula Forward?", "What does Forward compute?", "Hvad beregner Forward?"),
            (
                (
                    "sum",
                    (
                        "Suma de probabilidades de todas las rutas",
                        "Sum of probabilities of all paths",
                        "Sum af sandsynligheder for alle stier",
                    ),
                ),
                ("best", ("Sólo mejor ruta", "Best path only", "Kun bedste sti")),
                ("count", ("Número de estados", "Number of states", "Antal tilstande")),
            ),
            "sum",
            (
                "Forward marginaliza rutas ocultas.",
                "Forward marginalizes hidden paths.",
                "Forward marginaliserer skjulte stier.",
            ),
        ),
        (
            "004",
            ("¿Qué calcula Viterbi?", "What does Viterbi compute?", "Hvad beregner Viterbi?"),
            (
                (
                    "best",
                    (
                        "Ruta global más probable",
                        "Most probable global path",
                        "Mest sandsynlige globale sti",
                    ),
                ),
                ("sum", ("Probabilidad total", "Total probability", "Total sandsynlighed")),
                ("mean", ("Estado medio", "Mean state", "Gennemsnitlig tilstand")),
            ),
            "best",
            (
                "Sustituye suma por máximo.",
                "It replaces summation with maximization.",
                "Den erstatter summering med maksimum.",
            ),
        ),
        (
            "005",
            (
                "¿Qué operación estable suma probabilidades en log?",
                "Which stable operation sums probabilities in log space?",
                "Hvilken stabil operation summerer sandsynligheder i log-rum?",
            ),
            (
                ("lse", ("log-sum-exp", "log-sum-exp", "log-sum-exp")),
                ("max", ("Sólo max", "Max only", "Kun max")),
                ("exp", ("Sólo exp", "Exp only", "Kun exp")),
            ),
            "lse",
            (
                "Evita salir innecesariamente del dominio log.",
                "It avoids unnecessarily leaving log space.",
                "Den undgår unødigt at forlade log-rummet.",
            ),
        ),
        (
            "006",
            (
                "¿Qué diferencia probabilidad conjunta y marginal?",
                "What distinguishes joint and marginal probability?",
                "Hvad skelner fælles og marginal sandsynlighed?",
            ),
            (
                (
                    "paths",
                    ("La marginal suma rutas", "Marginal sums paths", "Marginal summerer stier"),
                ),
                ("same", ("Son idénticas", "They are identical", "De er identiske")),
                ("logs", ("Sólo cambia el log", "Only log changes", "Kun log ændres")),
            ),
            "paths",
            (
                "La conjunta fija una ruta concreta.",
                "Joint probability fixes a specific path.",
                "Fælles sandsynlighed fastlægger en bestemt sti.",
            ),
        ),
        (
            "007",
            (
                "¿Qué usa Baum–Welch en el E-step?",
                "What does Baum–Welch use in the E-step?",
                "Hvad bruger Baum–Welch i E-trinnet?",
            ),
            (
                ("expected", ("Conteos esperados", "Expected counts", "Forventede tællinger")),
                (
                    "labels",
                    (
                        "Rutas conocidas obligatorias",
                        "Mandatory known paths",
                        "Obligatoriske kendte stier",
                    ),
                ),
                ("sorting", ("Ordenación", "Sorting", "Sortering")),
            ),
            "expected",
            (
                "Forward–Backward calcula responsabilidades.",
                "Forward–Backward computes responsibilities.",
                "Forward–Backward beregner ansvar.",
            ),
        ),
        (
            "008",
            (
                "¿Qué estado de perfil no emite?",
                "Which profile state does not emit?",
                "Hvilken profiltilstand emitterer ikke?",
            ),
            (
                ("delete", ("Delete", "Delete", "Delete")),
                ("match", ("Match", "Match", "Match")),
                ("insert", ("Insert", "Insert", "Insert")),
            ),
            "delete",
            (
                "Representa omitir una columna de consenso.",
                "It represents skipping a consensus column.",
                "Den repræsenterer overspringelse af en konsensuskolonne.",
            ),
        ),
        (
            "009",
            ("¿Qué evita smoothing?", "What does smoothing avoid?", "Hvad undgår smoothing?"),
            (
                ("zeros", ("Ceros accidentales", "Accidental zeros", "Utilsigtede nuller")),
                ("states", ("Estados ocultos", "Hidden states", "Skjulte tilstande")),
                ("logs", ("Todos los logaritmos", "All logarithms", "Alle logaritmer")),
            ),
            "zeros",
            (
                "Una observación no vista no debería ser necesariamente imposible.",
                "An unseen observation should not necessarily be impossible.",
                "En ikke-set observation bør ikke nødvendigvis være umulig.",
            ),
        ),
        (
            "010",
            (
                "¿Qué riesgo tiene Baum–Welch?",
                "What risk does Baum–Welch have?",
                "Hvilken risiko har Baum–Welch?",
            ),
            (
                ("local", ("Óptimos locales", "Local optima", "Lokale optima")),
                (
                    "linear",
                    ("Siempre solución lineal", "Always linear solution", "Altid lineær løsning"),
                ),
                (
                    "exact",
                    ("Garantía exacta global", "Exact global guarantee", "Eksakt global garanti"),
                ),
            ),
            "local",
            (
                "La likelihood puede depender de inicialización.",
                "Likelihood may depend on initialization.",
                "Likelihood kan afhænge af initialisering.",
            ),
        ),
    ),
    true_false=(
        (
            "011",
            (
                "Los estados ocultos y símbolos observados son idénticos.",
                "Hidden states and observed symbols are identical.",
                "Skjulte tilstande og observerede symboler er identiske.",
            ),
            False,
            (
                "Son variables distintas.",
                "They are different variables.",
                "De er forskellige variabler.",
            ),
        ),
        (
            "012",
            (
                "Las filas de transición deben normalizarse.",
                "Transition rows should be normalized.",
                "Overgangsrækker bør normaliseres.",
            ),
            True,
            (
                "Cada fila es una distribución.",
                "Each row is a distribution.",
                "Hver række er en fordeling.",
            ),
        ),
        (
            "013",
            (
                "Forward usa máximo en cada transición.",
                "Forward uses maximum at each transition.",
                "Forward bruger maksimum ved hver overgang.",
            ),
            False,
            (
                "Forward suma; Viterbi maximiza.",
                "Forward sums; Viterbi maximizes.",
                "Forward summerer; Viterbi maksimerer.",
            ),
        ),
        (
            "014",
            (
                "Viterbi resume toda la incertidumbre posterior.",
                "Viterbi summarizes all posterior uncertainty.",
                "Viterbi opsummerer al posterior usikkerhed.",
            ),
            False,
            (
                "Devuelve una ruta óptima.",
                "It returns one optimal path.",
                "Den returnerer én optimal sti.",
            ),
        ),
        (
            "015",
            (
                "Productos largos de probabilidades pueden causar underflow.",
                "Long products of probabilities can cause underflow.",
                "Lange produkter af sandsynligheder kan give underflow.",
            ),
            True,
            (
                "Escalado o logs lo mitigan.",
                "Scaling or logs mitigate it.",
                "Skalering eller logs reducerer det.",
            ),
        ),
        (
            "016",
            (
                "La probabilidad marginal suma todas las rutas.",
                "Marginal probability sums all paths.",
                "Marginal sandsynlighed summerer alle stier.",
            ),
            True,
            ("Es el objetivo de Forward.", "That is Forward's objective.", "Det er Forwards mål."),
        ),
        (
            "017",
            (
                "Baum–Welch garantiza el óptimo global.",
                "Baum–Welch guarantees the global optimum.",
                "Baum–Welch garanterer det globale optimum.",
            ),
            False,
            (
                "Puede converger localmente.",
                "It may converge locally.",
                "Den kan konvergere lokalt.",
            ),
        ),
        (
            "018",
            (
                "Un estado delete de perfil suele ser silencioso.",
                "A profile delete state is usually silent.",
                "En profil-delete-tilstand er normalt tavs.",
            ),
            True,
            (
                "Omite una posición de consenso.",
                "It skips a consensus position.",
                "Den springer en konsensusposition over.",
            ),
        ),
        (
            "019",
            (
                "Likelihood alta de entrenamiento garantiza generalización.",
                "High training likelihood guarantees generalization.",
                "Høj trænings-likelihood garanterer generalisering.",
            ),
            False,
            (
                "Se necesita evaluación retenida.",
                "Held-out evaluation is needed.",
                "Hold-out-evaluering kræves.",
            ),
        ),
        (
            "020",
            (
                "La estructura de un HMM es una decisión de modelado.",
                "HMM structure is a modeling decision.",
                "HMM-struktur er en modelleringsbeslutning.",
            ),
            True,
            (
                "Determina qué dependencias pueden expresarse.",
                "It determines which dependencies can be expressed.",
                "Den bestemmer, hvilke afhængigheder der kan udtrykkes.",
            ),
        ),
    ),
    tutor=(
        (
            "Un HMM modela una secuencia observada mediante una ruta de estados no observados. La distribución inicial, las transiciones y emisiones deben normalizarse. La probabilidad conjunta fija una ruta; Forward suma todas las rutas para obtener la probabilidad marginal; Viterbi maximiza una ruta y requiere traceback. Secuencias largas exigen escalado o log-sum-exp. Con rutas conocidas, los parámetros se estiman por conteos suavizados; Baum–Welch aplica EM con expectativas de Forward–Backward y puede converger a óptimos locales. Los HMM de perfil representan posiciones conservadas mediante estados match, insert y delete. La interpretación de estados, estructura, smoothing y validación fuera de muestra son partes esenciales del modelo.",
            "An HMM models an observed sequence through a path of unobserved states. Initial, transition, and emission distributions must be normalized. Joint probability fixes a path; Forward sums all paths to obtain marginal probability; Viterbi maximizes one path and requires traceback. Long sequences require scaling or log-sum-exp. With known paths, parameters are estimated from smoothed counts; Baum–Welch applies EM using Forward–Backward expectations and may converge to local optima. Profile HMMs represent conserved positions with match, insert, and delete states. State interpretation, structure, smoothing, and out-of-sample validation are essential parts of the model.",
            "En HMM modellerer en observeret sekvens gennem en sti af ikke-observerede tilstande. Initial-, overgangs- og emissionsfordelinger skal normaliseres. Fælles sandsynlighed fastlægger en sti; Forward summerer alle stier for at få marginal sandsynlighed; Viterbi maksimerer én sti og kræver traceback. Lange sekvenser kræver skalering eller log-sum-exp. Med kendte stier estimeres parametre fra smoothede tællinger; Baum–Welch anvender EM med Forward–Backward-forventninger og kan konvergere til lokale optima. Profil-HMM'er repræsenterer konserverede positioner med match-, insert- og delete-tilstande. Tilstandsfortolkning, struktur, smoothing og validering uden for træningsdata er essentielle dele af modellen.",
        ),
        (
            (
                "Estados y observaciones son distintos.",
                "States and observations are distinct.",
                "Tilstande og observationer er forskellige.",
            ),
            ("Forward suma rutas.", "Forward sums paths.", "Forward summerer stier."),
            (
                "Viterbi maximiza una ruta.",
                "Viterbi maximizes one path.",
                "Viterbi maksimerer én sti.",
            ),
            ("Logs evitan underflow.", "Logs avoid underflow.", "Logs undgår underflow."),
            ("Baum–Welch es EM.", "Baum–Welch is EM.", "Baum–Welch er EM."),
            (
                "Perfil usa match/insert/delete.",
                "Profile uses match/insert/delete.",
                "Profil bruger match/insert/delete.",
            ),
        ),
        (
            (
                "Confundir Forward y Viterbi.",
                "Confusing Forward and Viterbi.",
                "At forveksle Forward og Viterbi.",
            ),
            (
                "No normalizar probabilidades.",
                "Not normalizing probabilities.",
                "Ikke at normalisere sandsynligheder.",
            ),
            (
                "Interpretar underflow como probabilidad cero.",
                "Interpreting underflow as zero probability.",
                "At fortolke underflow som nul sandsynlighed.",
            ),
            (
                "Suponer que Viterbi refleja toda incertidumbre.",
                "Assuming Viterbi reflects all uncertainty.",
                "At antage at Viterbi afspejler al usikkerhed.",
            ),
            (
                "Ignorar óptimos locales de EM.",
                "Ignoring EM local optima.",
                "At ignorere lokale optima i EM.",
            ),
            (
                "Asignar significado biológico sin validación.",
                "Assigning biological meaning without validation.",
                "At tildele biologisk betydning uden validering.",
            ),
        ),
        (
            (
                "¿Qué representa cada estado?",
                "What does each state represent?",
                "Hvad repræsenterer hver tilstand?",
            ),
            (
                "¿Están normalizadas las distribuciones?",
                "Are distributions normalized?",
                "Er fordelingerne normaliserede?",
            ),
            (
                "¿Se necesita suma o ruta óptima?",
                "Is a sum or optimal path needed?",
                "Kræves en sum eller optimal sti?",
            ),
            ("¿Cómo se evita underflow?", "How is underflow avoided?", "Hvordan undgås underflow?"),
            (
                "¿Cómo se inicializan parámetros?",
                "How are parameters initialized?",
                "Hvordan initialiseres parametre?",
            ),
            (
                "¿Qué evaluación retenida se usará?",
                "What held-out evaluation will be used?",
                "Hvilken hold-out-evaluering bruges?",
            ),
        ),
        (
            (
                "Formula correctamente probabilidades.",
                "Correctly formulates probabilities.",
                "Formulerer sandsynligheder korrekt.",
            ),
            (
                "Distingue Forward y Viterbi.",
                "Distinguishes Forward and Viterbi.",
                "Skelner Forward og Viterbi.",
            ),
            (
                "Gestiona estabilidad numérica.",
                "Handles numerical stability.",
                "Håndterer numerisk stabilitet.",
            ),
            (
                "Explica EM y sus límites.",
                "Explains EM and its limits.",
                "Forklarer EM og dets begrænsninger.",
            ),
            ("Interpreta HMM de perfil.", "Interprets profile HMMs.", "Fortolker profil-HMM'er."),
            (
                "Propone validación fuera de muestra.",
                "Proposes out-of-sample validation.",
                "Foreslår validering uden for træningsdata.",
            ),
        ),
        (
            (
                "No inventar probabilidades o estados.",
                "Do not invent probabilities or states.",
                "Opfind ikke sandsynligheder eller tilstande.",
            ),
            (
                "No declarar certeza desde Viterbi.",
                "Do not claim certainty from Viterbi.",
                "Hævd ikke sikkerhed ud fra Viterbi.",
            ),
            (
                "No ocultar inicialización o smoothing.",
                "Do not hide initialization or smoothing.",
                "Skjul ikke initialisering eller smoothing.",
            ),
            (
                "No convertir ejemplos en modelos clínicos.",
                "Do not turn examples into clinical models.",
                "Omsæt ikke eksempler til kliniske modeller.",
            ),
            ("Responder en idioma activo.", "Answer in active language.", "Svar på aktivt sprog."),
        ),
        (
            "Rabiner tutorial on hidden Markov models.",
            "Durbin et al., Biological Sequence Analysis.",
            "Forward, backward, Viterbi, and Baum-Welch derivations.",
            "Profile HMM literature and HMMER documentation.",
            "Numerical stability with scaling and log-sum-exp.",
            "Active SDU DM847 HMM learning outcomes.",
        ),
    ),
)

LOCALIZED_MODULE_05_HIDDEN_MARKOV_MODELS: LocalizedLearningModule = build_module(_SPEC)
LOCALIZED_OBJECTIVE_QUESTION_BANK_05 = build_question_bank(_SPEC)


def materialize_module_05_question_bank(
    locale: AppLocale | str = AppLocale.SPANISH_SPAIN,
) -> tuple[AssessmentItem, ...]:
    return materialize_bank(LOCALIZED_OBJECTIVE_QUESTION_BANK_05, locale)


MODULE_05_HIDDEN_MARKOV_MODELS: LearningModule = (
    LOCALIZED_MODULE_05_HIDDEN_MARKOV_MODELS.materialize(AppLocale.SPANISH_SPAIN)
)
OBJECTIVE_QUESTION_BANK_05 = materialize_module_05_question_bank()

__all__ = [
    "LOCALIZED_MODULE_05_HIDDEN_MARKOV_MODELS",
    "LOCALIZED_OBJECTIVE_QUESTION_BANK_05",
    "MODULE_05_HIDDEN_MARKOV_MODELS",
    "OBJECTIVE_QUESTION_BANK_05",
    "materialize_module_05_question_bank",
]
