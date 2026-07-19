"""DM847 module 3: sequence scoring, exact matching, and statistical evidence."""

from __future__ import annotations

from ...i18n import AppLocale
from ..localized_models import LocalizedLearningModule
from ..models import AssessmentItem, LearningModule
from .standard import StandardModuleSpec, build_module, build_question_bank, materialize_bank

_SPEC = StandardModuleSpec(
    module_id="dm847.m03",
    title=(
        "Puntuación de secuencias, coincidencia exacta y evidencia estadística",
        "Sequence scoring, exact matching, and statistical evidence",
        "Sekvensscoring, eksakt matching og statistisk evidens",
    ),
    summary=(
        "Desarrolla representaciones por k-mers, puntuaciones de sustitución, modelos log-odds, búsqueda exacta y evaluación estadística de coincidencias evitando confundir puntuación con evidencia.",
        "Develop k-mer representations, substitution scores, log-odds models, exact search, and statistical evaluation of matches without confusing score with evidence.",
        "Udvikl k-mer-repræsentationer, substitutionsscores, log-odds-modeller, eksakt søgning og statistisk evaluering af matches uden at forveksle score med evidens.",
    ),
    objectives=(
        ("m03.o1", ("Representar secuencias mediante composición y k-mers.", "Represent sequences through composition and k-mers.", "Repræsentere sekvenser gennem sammensætning og k-mers.")),
        ("m03.o2", ("Interpretar puntuaciones de coincidencia, desajuste y sustitución.", "Interpret match, mismatch, and substitution scores.", "Fortolke match-, mismatch- og substitutionsscores.")),
        ("m03.o3", ("Explicar matrices log-odds y frecuencias de fondo.", "Explain log-odds matrices and background frequencies.", "Forklare log-odds-matricer og baggrundsfrekvenser.")),
        ("m03.o4", ("Implementar búsqueda exacta y analizar su complejidad.", "Implement exact search and analyze its complexity.", "Implementere eksakt søgning og analysere kompleksiteten.")),
        ("m03.o5", ("Distinguir puntuación bruta, identidad y significación estadística.", "Distinguish raw score, identity, and statistical significance.", "Skelne mellem rå score, identitet og statistisk signifikans.")),
        ("m03.o6", ("Diseñar validaciones con controles nulos y corrección por búsquedas múltiples.", "Design validation with null controls and multiple-search correction.", "Designe validering med nulkontroller og korrektion for multiple søgninger.")),
    ),
    concepts=(
        (
            "composition-kmers",
            ("Composición y k-mers", "Composition and k-mers", "Sammensætning og k-mers"),
            (
                "La composición resume frecuencias de símbolos; los k-mers incorporan contexto local de longitud k. Aumentar k mejora especificidad, pero expande el espacio posible exponencialmente y vuelve dispersos los conteos. La orientación, símbolos ambiguos y longitud efectiva deben definirse antes de comparar perfiles.",
                "Composition summarizes symbol frequencies; k-mers add local context of length k. Increasing k improves specificity but expands the possible space exponentially and makes counts sparse. Orientation, ambiguous symbols, and effective length must be defined before comparing profiles.",
                "Sammensætning opsummerer symbolfrekvenser; k-mers tilføjer lokal kontekst af længde k. Større k øger specificiteten, men udvider det mulige rum eksponentielt og gør tællinger sparsomme. Orientering, tvetydige symboler og effektiv længde skal defineres før profiler sammenlignes.",
            ),
            (("Una secuencia de longitud n contiene n-k+1 ventanas completas.", "A sequence of length n contains n-k+1 complete windows.", "En sekvens med længde n indeholder n-k+1 komplette vinduer."), ("k grande aumenta dispersión y coste.", "Large k increases sparsity and cost.", "Stor k øger sparsitet og omkostning.")),
        ),
        (
            "substitution-scores",
            ("Puntuaciones de sustitución", "Substitution scores", "Substitutionsscores"),
            (
                "Una función de puntuación asigna recompensa o penalización a pares de símbolos. En proteínas, matrices como PAM o BLOSUM reflejan sustituciones observadas en familias y no sólo identidad química. La matriz elegida expresa un régimen evolutivo implícito y afecta sensibilidad y especificidad.",
                "A scoring function assigns rewards or penalties to symbol pairs. For proteins, matrices such as PAM or BLOSUM reflect substitutions observed in families rather than simple chemical identity. The selected matrix encodes an implicit evolutionary regime and affects sensitivity and specificity.",
                "En scoringsfunktion tildeler belønning eller straf til symbolpar. For proteiner afspejler matricer som PAM og BLOSUM substitutioner observeret i familier frem for simpel kemisk identitet. Den valgte matrix udtrykker et implicit evolutionært regime og påvirker sensitivitet og specificitet.",
            ),
            (("La matriz es parte del modelo, no decoración.", "The matrix is part of the model, not decoration.", "Matricen er en del af modellen, ikke dekoration."), ("Comparar scores requiere misma escala y parámetros.", "Comparing scores requires the same scale and parameters.", "Sammenligning af scores kræver samme skala og parametre.")),
        ),
        (
            "log-odds",
            ("Puntuaciones log-odds", "Log-odds scores", "Log-odds-scores"),
            (
                "Una puntuación log-odds compara la probabilidad de observar un par bajo un modelo relacionado con la probabilidad bajo un modelo de fondo. Valores positivos favorecen el modelo relacionado; negativos favorecen el fondo. Ceros de frecuencia requieren suavizado y la base del logaritmo define la unidad.",
                "A log-odds score compares the probability of a pair under a related model with its probability under a background model. Positive values favor the related model; negative values favor background. Zero frequencies require smoothing, and the logarithm base defines the unit.",
                "En log-odds-score sammenligner sandsynligheden for et par under en relateret model med sandsynligheden under en baggrundsmodel. Positive værdier favoriserer den relaterede model; negative favoriserer baggrunden. Nulfrekvenser kræver smoothing, og logaritmens base definerer enheden.",
            ),
            (("El fondo cambia la interpretación del score.", "Background changes score interpretation.", "Baggrunden ændrer fortolkningen af scoren."), ("Suavizado evita logaritmos de cero.", "Smoothing avoids logarithms of zero.", "Smoothing undgår logaritmer af nul.")),
        ),
        (
            "exact-search",
            ("Búsqueda exacta", "Exact search", "Eksakt søgning"),
            (
                "La búsqueda ingenua compara el patrón en cada posición candidata y cuesta O((n-m+1)m) en el peor caso. Algoritmos como KMP reutilizan información de prefijos y alcanzan O(n+m). La elección depende de número de consultas, longitud, memoria y necesidad de índices reutilizables.",
                "Naive search compares the pattern at every candidate position and costs O((n-m+1)m) in the worst case. Algorithms such as KMP reuse prefix information and achieve O(n+m). Choice depends on query count, length, memory, and whether a reusable index is needed.",
                "Naiv søgning sammenligner mønstret ved hver kandidatposition og koster O((n-m+1)m) i værste fald. Algoritmer som KMP genbruger præfiksinformation og opnår O(n+m). Valget afhænger af antal forespørgsler, længde, hukommelse og behov for et genanvendeligt indeks.",
            ),
            (("Preprocesar un patrón puede ahorrar comparaciones.", "Preprocessing a pattern can save comparisons.", "Forbehandling af et mønster kan spare sammenligninger."), ("Muchos patrones pueden justificar un índice del texto.", "Many patterns may justify indexing the text.", "Mange mønstre kan retfærdiggøre indeksering af teksten.")),
        ),
        (
            "score-versus-significance",
            ("Score, identidad y significación", "Score, identity, and significance", "Score, identitet og signifikans"),
            (
                "La identidad es una proporción de posiciones iguales dentro de una comparación definida. El score incorpora un modelo de sustitución y gaps. La significación pregunta cuán extremo es el resultado bajo un modelo nulo y depende del tamaño de la búsqueda. Un score alto no tiene un significado universal sin distribución de referencia.",
                "Identity is the proportion of equal positions within a defined comparison. Score incorporates a substitution and gap model. Significance asks how extreme the result is under a null model and depends on search-space size. A high score has no universal meaning without a reference distribution.",
                "Identitet er andelen af ens positioner i en defineret sammenligning. Score inkluderer en substitutions- og gapmodel. Signifikans spørger, hvor ekstremt resultatet er under en nulmodel og afhænger af søgerummets størrelse. En høj score har ingen universel betydning uden en referencefordeling.",
            ),
            (("Identidad no equivale a homología.", "Identity is not equivalent to homology.", "Identitet er ikke det samme som homologi."), ("El espacio de búsqueda afecta falsos positivos.", "Search-space size affects false positives.", "Søgerummets størrelse påvirker falske positiver.")),
        ),
        (
            "null-models",
            ("Modelos nulos y múltiples búsquedas", "Null models and multiple searches", "Nulmodeller og multiple søgninger"),
            (
                "Un control nulo puede permutar la secuencia preservando composición, generar secuencias desde un modelo de fondo o usar una distribución analítica. Debe conservar las propiedades irrelevantes pero romper la estructura bajo estudio. Al evaluar miles de patrones, el umbral individual no controla el número total de hallazgos espurios.",
                "A null control may shuffle sequence while preserving composition, generate sequences from a background model, or use an analytical distribution. It should retain irrelevant properties while breaking the structure under study. When thousands of patterns are evaluated, an individual threshold does not control the total number of spurious findings.",
                "En nulkontrol kan permutere sekvensen med bevaret sammensætning, generere sekvenser fra en baggrundsmodel eller bruge en analytisk fordeling. Den bør bevare irrelevante egenskaber, men bryde den struktur, der undersøges. Når tusindvis af mønstre evalueres, kontrollerer en individuel tærskel ikke det samlede antal falske fund.",
            ),
            (("El nulo debe responder a la pregunta concreta.", "The null must match the specific question.", "Nulmodellen skal passe til det konkrete spørgsmål."), ("Más búsquedas exigen control de multiplicidad.", "More searches require multiplicity control.", "Flere søgninger kræver kontrol af multiplicitet.")),
        ),
    ),
    examples=(
        (
            "m03.e01",
            ("Conteo de k-mers", "Count k-mers", "Tæl k-mers"),
            ("Cuenta 3-mers solapados y verifica el número de ventanas.", "Count overlapping 3-mers and verify the number of windows.", "Tæl overlappende 3-mers og verificér antallet af vinduer."),
            (("Las ventanas avanzan una posición.", "Windows advance by one position.", "Vinduer flyttes én position."), ("La suma de conteos debe ser n-k+1.", "The count sum should be n-k+1.", "Summen af tællinger bør være n-k+1.")),
            """from collections import Counter\n\n\ndef kmer_counts(sequence: str, k: int) -> Counter[str]:\n    if k < 1 or k > len(sequence):\n        raise ValueError(\"invalid k\")\n    counts = Counter(sequence[index : index + k] for index in range(len(sequence) - k + 1))\n    assert sum(counts.values()) == len(sequence) - k + 1\n    return counts\n\n\nprint(sorted(kmer_counts(\"ACGACG\", 3).items()))\n""",
            "[('ACG', 2), ('CGA', 1), ('GAC', 1)]",
            ("Los k-mers preservan contexto local pero no posiciones globales.", "K-mers preserve local context but not global positions.", "K-mers bevarer lokal kontekst, men ikke globale positioner."),
        ),
        (
            "m03.e02",
            ("Score log-odds", "Log-odds score", "Log-odds-score"),
            ("Calcula evidencia en bits para una observación frente a un fondo.", "Compute evidence in bits for an observation against background.", "Beregn evidens i bits for en observation mod en baggrund."),
            (("El numerador representa el modelo alternativo.", "The numerator represents the alternative model.", "Tælleren repræsenterer den alternative model."), ("Base 2 expresa bits.", "Base 2 expresses bits.", "Base 2 udtrykker bits.")),
            """from math import log2\n\n\ndef log_odds(observed_probability: float, background_probability: float) -> float:\n    if observed_probability <= 0 or background_probability <= 0:\n        raise ValueError(\"probabilities must be positive\")\n    return round(log2(observed_probability / background_probability), 3)\n\n\nprint(log_odds(0.20, 0.05))\n""",
            "2.0",
            ("Dos bits indican una razón de probabilidades de cuatro a uno a favor del modelo alternativo.", "Two bits indicate a four-to-one probability ratio in favor of the alternative model.", "To bits angiver et sandsynlighedsforhold på fire til én til fordel for den alternative model."),
        ),
        (
            "m03.e03",
            ("p-valor empírico", "Empirical p-value", "Empirisk p-værdi"),
            ("Compara un score observado con scores nulos e incluye la corrección +1.", "Compare an observed score with null scores using the +1 correction.", "Sammenlign en observeret score med nulscores med +1-korrektionen."),
            (("Se cuentan nulos al menos tan extremos.", "Null values at least as extreme are counted.", "Nulværdier mindst lige så ekstreme tælles."), ("La corrección evita p=0 con simulación finita.", "The correction avoids p=0 with finite simulation.", "Korrektionen undgår p=0 ved endelig simulering.")),
            """def empirical_p_value(observed: float, null_scores: list[float]) -> float:\n    extreme = sum(score >= observed for score in null_scores)\n    return (extreme + 1) / (len(null_scores) + 1)\n\n\nprint(round(empirical_p_value(8.0, [2.0, 4.0, 8.5, 6.0]), 3))\n""",
            "0.4",
            ("El resultado depende de cómo se generó el nulo y del número de simulaciones.", "The result depends on how the null was generated and on simulation count.", "Resultatet afhænger af, hvordan nulmodellen blev genereret, og antallet af simuleringer."),
        ),
    ),
    practices=(
        ("m03.p01", "CODE_TRACING", ("¿Cuántos 4-mers tiene una secuencia de longitud 10?", "How many 4-mers does a sequence of length 10 have?", "Hvor mange 4-mers har en sekvens med længde 10?"), (("Usa n-k+1.", "Use n-k+1.", "Brug n-k+1."),), ("7", "7", "7"), ("Se cuentan ventanas solapadas completas.", "Complete overlapping windows are counted.", "Komplette overlappende vinduer tælles."), ""),
        ("m03.p02", "SHORT_ANSWER", ("Explica el compromiso al aumentar k.", "Explain the trade-off when increasing k.", "Forklar kompromiset ved større k."), (("Compara especificidad y dispersión.", "Compare specificity and sparsity.", "Sammenlign specificitet og sparsitet."),), ("k mayor captura contexto más específico, pero genera 4^k posibles palabras en ADN, más ceros, mayor memoria y menor robustez con datos limitados.", "Larger k captures more specific context but creates 4^k possible DNA words, more zeros, higher memory use, and lower robustness with limited data.", "Større k fanger mere specifik kontekst, men skaber 4^k mulige DNA-ord, flere nuller, større hukommelsesbrug og mindre robusthed ved begrænsede data."), ("La elección depende de longitud y pregunta.", "Choice depends on length and question.", "Valget afhænger af længde og spørgsmål."), ""),
        ("m03.p03", "DATA_INTERPRETATION", ("Dos matrices producen scores 40 y 55. ¿Puede afirmarse que 55 es mejor?", "Two matrices produce scores 40 and 55. Can 55 be called better?", "To matricer giver scores 40 og 55. Kan 55 kaldes bedre?"), (("Revisa escalas.", "Inspect scales.", "Undersøg skalaer."),), ("No sin conocer escalas, parámetros, distribución nula y objetivo. Scores de matrices distintas no son directamente comparables.", "Not without knowing scales, parameters, null distribution, and objective. Scores from different matrices are not directly comparable.", "Ikke uden kendskab til skalaer, parametre, nulfordeling og formål. Scores fra forskellige matricer er ikke direkte sammenlignelige."), ("Debe compararse evidencia calibrada.", "Calibrated evidence should be compared.", "Kalibreret evidens bør sammenlignes."), ""),
        ("m03.p04", "FILL_IN_THE_BLANK", ("La complejidad peor de la búsqueda ingenua es O(____).", "The worst-case complexity of naive search is O(____).", "Værste-fald-kompleksiteten for naiv søgning er O(____)."), (("Incluye texto y patrón.", "Include text and pattern.", "Medtag tekst og mønster."),), ("(n-m+1)m", "(n-m+1)m", "(n-m+1)m"), ("En aproximación común es O(nm).", "A common approximation is O(nm).", "En almindelig tilnærmelse er O(nm)."), ""),
        ("m03.p05", "PIPELINE_DESIGN", ("Diseña un nulo para enriquecimiento de un motivo conservando GC.", "Design a null for motif enrichment while preserving GC.", "Design en nulmodel for motivberigelse med bevaret GC."), (("Rompe posiciones pero conserva composición.", "Break positions while retaining composition.", "Bryd positioner, men bevar sammensætning."),), ("Permutar bases dentro de cada secuencia o generar con un modelo de Markov ajustado, repetir el conteo del motivo y comparar con la distribución nula.", "Shuffle bases within each sequence or generate from a fitted Markov model, repeat motif counting, and compare with the null distribution.", "Permutér baser i hver sekvens eller generér fra en tilpasset Markov-model, gentag motivtællingen og sammenlign med nulfordelingen."), ("El nulo debe preservar propiedades que podrían explicar el conteo.", "The null should preserve properties that could explain the count.", "Nulmodellen bør bevare egenskaber, der kan forklare tællingen."), ""),
        ("m03.p06", "ORAL_EXPLANATION", ("Distingue identidad, similitud y homología.", "Distinguish identity, similarity, and homology.", "Skeln mellem identitet, lighed og homologi."), (("Homología es una hipótesis histórica.", "Homology is a historical hypothesis.", "Homologi er en historisk hypotese."),), ("Identidad es igualdad posicional; similitud incorpora sustituciones favorables; homología afirma ascendencia común y no se expresa como porcentaje.", "Identity is positional equality; similarity includes favorable substitutions; homology asserts common ancestry and is not a percentage.", "Identitet er positionslighed; lighed inkluderer favorable substitutioner; homologi hævder fælles afstamning og udtrykkes ikke som procent."), ("La similitud aporta evidencia, no demostración automática.", "Similarity provides evidence, not automatic proof.", "Lighed giver evidens, ikke automatisk bevis."), ""),
        ("m03.p07", "DEBUGGING", ("Un p-valor empírico resulta cero con 100 permutaciones. Corrige.", "An empirical p-value is zero with 100 permutations. Correct it.", "En empirisk p-værdi er nul med 100 permutationer. Ret den."), (("Usa corrección +1.", "Use the +1 correction.", "Brug +1-korrektionen."),), ("Calcular (extremos+1)/(B+1), reportar resolución mínima 1/(B+1) y aumentar B si se necesita mayor precisión.", "Compute (extreme+1)/(B+1), report minimum resolution 1/(B+1), and increase B if finer precision is needed.", "Beregn (ekstreme+1)/(B+1), rapportér minimumsopløsningen 1/(B+1), og øg B hvis finere præcision kræves."), ("La simulación finita no justifica probabilidad exactamente cero.", "Finite simulation does not justify an exact zero probability.", "Endelig simulering retfærdiggør ikke præcis nul sandsynlighed."), ""),
        ("m03.p08", "ORDERING", ("Ordena: definir score, definir nulo, calcular observado, simular, estimar p, corregir multiplicidad.", "Order: define score, define null, compute observed, simulate, estimate p, correct multiplicity.", "Ordén: definér score, definér nulmodel, beregn observeret, simulér, estimer p, korrigér multiplicitet."), (("El score precede a la simulación.", "The score precedes simulation.", "Scoren kommer før simulering."),), ("Definir score → definir nulo → calcular observado → simular → estimar p → corregir multiplicidad.", "Define score → define null → compute observed → simulate → estimate p → correct multiplicity.", "Definér score → definér nulmodel → beregn observeret → simulér → estimer p → korrigér multiplicitet."), ("El flujo separa modelo, cálculo e inferencia.", "The workflow separates model, computation, and inference.", "Workflowet adskiller model, beregning og inferens."), ""),
    ),
    mcqs=(
        ("001", ("¿Cuántos k-mers completos hay en longitud n?", "How many complete k-mers are in length n?", "Hvor mange komplette k-mers findes i længde n?"), (("formula", ("n-k+1", "n-k+1", "n-k+1")), ("nk", ("nk", "nk", "nk")), ("nplus", ("n+k", "n+k", "n+k"))), "formula", ("Las ventanas empiezan en 0 hasta n-k.", "Windows start from 0 through n-k.", "Vinduer starter fra 0 til n-k.")),
        ("002", ("¿Qué ocurre al aumentar k?", "What happens when k increases?", "Hvad sker der, når k øges?"), (("sparse", ("Aumentan especificidad y dispersión", "Specificity and sparsity increase", "Specificitet og sparsitet øges")), ("same", ("Nada cambia", "Nothing changes", "Intet ændres")), ("linear", ("El espacio crece linealmente", "Space grows linearly", "Rummet vokser lineært"))), "sparse", ("El espacio de ADN crece como 4^k.", "DNA space grows as 4^k.", "DNA-rummet vokser som 4^k.")),
        ("003", ("¿Qué representa una matriz BLOSUM?", "What does a BLOSUM matrix represent?", "Hvad repræsenterer en BLOSUM-matrix?"), (("substitutions", ("Sustituciones observadas y log-odds", "Observed substitutions and log-odds", "Observerede substitutioner og log-odds")), ("positions", ("Coordenadas genómicas", "Genomic coordinates", "Genomiske koordinater")), ("reads", ("Calidad de reads", "Read quality", "Read-kvalitet"))), "substitutions", ("La matriz modela preferencia de sustituciones proteicas.", "The matrix models protein substitution preferences.", "Matricen modellerer præferencer for proteinsubstitutioner.")),
        ("004", ("¿Qué significa un log-odds positivo?", "What does a positive log-odds mean?", "Hvad betyder en positiv log-odds?"), (("alternative", ("Favorece el modelo alternativo", "Favors the alternative model", "Favoriserer den alternative model")), ("impossible", ("Evento imposible", "Impossible event", "Umulig hændelse")), ("equal", ("Probabilidades iguales", "Equal probabilities", "Lige sandsynligheder"))), "alternative", ("El numerador supera al fondo.", "The numerator exceeds background.", "Tælleren overstiger baggrunden.")),
        ("005", ("¿Qué algoritmo de patrón único logra O(n+m)?", "Which single-pattern algorithm achieves O(n+m)?", "Hvilken algoritme for ét mønster opnår O(n+m)?"), (("kmp", ("KMP", "KMP", "KMP")), ("naive", ("Búsqueda ingenua", "Naive search", "Naiv søgning")), ("bubble", ("Bubble sort", "Bubble sort", "Bubble sort"))), "kmp", ("KMP reutiliza prefijos del patrón.", "KMP reuses pattern prefixes.", "KMP genbruger mønsterpræfikser.")),
        ("006", ("¿Qué mide identidad?", "What does identity measure?", "Hvad måler identitet?"), (("equal", ("Proporción de posiciones iguales", "Proportion of equal positions", "Andel af ens positioner")), ("ancestry", ("Ascendencia común demostrada", "Proven common ancestry", "Bevist fælles afstamning")), ("pvalue", ("p-valor", "p-value", "p-værdi"))), "equal", ("La identidad depende de una comparación definida.", "Identity depends on a defined comparison.", "Identitet afhænger af en defineret sammenligning.")),
        ("007", ("¿Qué determina significación?", "What determines significance?", "Hvad bestemmer signifikans?"), (("null", ("Distribución nula y espacio de búsqueda", "Null distribution and search space", "Nulfordeling og søgerum")), ("color", ("Color", "Color", "Farve")), ("lengthonly", ("Sólo longitud", "Length only", "Kun længde"))), "null", ("El score debe calibrarse contra resultados esperados por azar.", "Score must be calibrated against chance expectations.", "Scoren skal kalibreres mod forventninger ved tilfældighed.")),
        ("008", ("¿Qué evita la corrección +1 en permutaciones?", "What does the +1 permutation correction avoid?", "Hvad undgår +1-korrektionen ved permutationer?"), (("zero", ("p=0 artificial", "Artificial p=0", "Kunstig p=0")), ("ties", ("Todos los empates", "All ties", "Alle ties")), ("memory", ("Uso de memoria", "Memory use", "Hukommelsesbrug"))), "zero", ("Una muestra finita no demuestra probabilidad nula.", "A finite sample does not prove zero probability.", "En endelig prøve beviser ikke nul sandsynlighed.")),
        ("009", ("¿Qué debe preservar un nulo de motivo sensible a GC?", "What should a GC-sensitive motif null preserve?", "Hvad bør en GC-følsom motivnulmodel bevare?"), (("gc", ("Composición GC", "GC composition", "GC-sammensætning")), ("motif", ("El motivo exacto", "The exact motif", "Det præcise motiv")), ("labels", ("Etiquetas de salida", "Output labels", "Outputlabels"))), "gc", ("Así GC no explica artificialmente el enriquecimiento.", "Then GC does not artificially explain enrichment.", "Så forklarer GC ikke kunstigt berigelsen.")),
        ("010", ("¿Qué requiere evaluar miles de patrones?", "What is required when evaluating thousands of patterns?", "Hvad kræves ved evaluering af tusindvis af mønstre?"), (("multiple", ("Control de multiplicidad", "Multiplicity control", "Kontrol af multiplicitet")), ("ignore", ("Ignorar p-valores", "Ignore p-values", "Ignorér p-værdier")), ("same", ("El mismo umbral sin ajuste", "Same unadjusted threshold", "Samme ujusterede tærskel"))), "multiple", ("Muchas pruebas aumentan hallazgos por azar.", "Many tests increase chance findings.", "Mange tests øger tilfældige fund.")),
    ),
    true_false=(
        ("011", ("Los k-mers conservan todas las posiciones globales.", "K-mers preserve all global positions.", "K-mers bevarer alle globale positioner."), False, ("Los conteos pierden orden global.", "Counts lose global order.", "Tællinger mister global rækkefølge.")),
        ("012", ("El número posible de k-mers de ADN crece como 4^k.", "The number of possible DNA k-mers grows as 4^k.", "Antallet af mulige DNA-k-mers vokser som 4^k."), True, ("Hay cuatro símbolos canónicos por posición.", "There are four canonical symbols per position.", "Der er fire kanoniske symboler pr. position.")),
        ("013", ("Scores de matrices distintas son siempre comparables.", "Scores from different matrices are always comparable.", "Scores fra forskellige matricer er altid sammenlignelige."), False, ("Escala y modelo pueden diferir.", "Scale and model may differ.", "Skala og model kan variere.")),
        ("014", ("Una puntuación log-odds depende del modelo de fondo.", "A log-odds score depends on the background model.", "En log-odds-score afhænger af baggrundsmodellen."), True, ("El fondo aparece en el denominador.", "Background appears in the denominator.", "Baggrunden står i nævneren.")),
        ("015", ("La búsqueda ingenua puede costar O(nm).", "Naive search may cost O(nm).", "Naiv søgning kan koste O(nm)."), True, ("En comparación completa por posición produce ese peor caso.", "Full comparison at each position yields that worst case.", "Fuld sammenligning ved hver position giver dette værste tilfælde.")),
        ("016", ("Homología es un porcentaje de identidad.", "Homology is a percentage identity.", "Homologi er en procentidentitet."), False, ("Homología es una relación histórica binaria o hipótesis de ascendencia.", "Homology is a historical relationship or ancestry hypothesis.", "Homologi er en historisk relation eller hypotese om afstamning.")),
        ("017", ("Un score alto siempre es significativo.", "A high score is always significant.", "En høj score er altid signifikant."), False, ("Se necesita calibración nula y tamaño de búsqueda.", "Null calibration and search size are needed.", "Nulkalibrering og søgerumsstørrelse er nødvendige.")),
        ("018", ("Un nulo debe romper la estructura que se investiga.", "A null should break the structure under investigation.", "En nulmodel bør bryde den struktur, der undersøges."), True, ("Debe conservar sólo propiedades irrelevantes o confusoras.", "It should retain only irrelevant or confounding properties.", "Den bør kun bevare irrelevante eller confoundende egenskaber.")),
        ("019", ("Con más pruebas aumenta el riesgo de falsos positivos.", "With more tests, false-positive risk increases.", "Med flere tests øges risikoen for falske positiver."), True, ("Por eso se controla multiplicidad.", "That is why multiplicity is controlled.", "Derfor kontrolleres multiplicitet.")),
        ("020", ("Un p-valor empírico cero con pocas permutaciones es exacto.", "An empirical p-value of zero with few permutations is exact.", "En empirisk p-værdi på nul med få permutationer er præcis."), False, ("La resolución está limitada por el número de permutaciones.", "Resolution is limited by permutation count.", "Opløsningen begrænses af antallet af permutationer.")),
    ),
    tutor=(
        (
            "El análisis de secuencias requiere separar representación, puntuación e inferencia. Los k-mers resumen contexto local y su espacio crece exponencialmente con k. Las matrices de sustitución expresan un modelo biológico y deben compararse sólo bajo parámetros compatibles. Las puntuaciones log-odds contrastan un modelo relacionado con un fondo y requieren suavizado cuando hay frecuencias cero. La búsqueda exacta puede resolverse ingenuamente o mediante algoritmos e índices que reutilizan estructura. Identidad, similitud, score y homología no son sinónimos. La significación depende de una distribución nula y del tamaño del espacio de búsqueda. Los controles nulos deben preservar composición u otras propiedades confusoras y romper la señal evaluada. Muchas búsquedas requieren corrección de multiplicidad.",
            "Sequence analysis requires separating representation, scoring, and inference. K-mers summarize local context and their space grows exponentially with k. Substitution matrices express a biological model and should be compared only under compatible parameters. Log-odds scores contrast a related model with background and require smoothing for zero frequencies. Exact search can be solved naively or with algorithms and indexes that reuse structure. Identity, similarity, score, and homology are not synonyms. Significance depends on a null distribution and search-space size. Null controls should preserve composition or other confounders while breaking the signal being evaluated. Multiple searches require multiplicity correction.",
            "Sekvensanalyse kræver adskillelse af repræsentation, scoring og inferens. K-mers opsummerer lokal kontekst, og deres rum vokser eksponentielt med k. Substitutionsmatricer udtrykker en biologisk model og bør kun sammenlignes under kompatible parametre. Log-odds-scores sammenligner en relateret model med baggrund og kræver smoothing ved nulfrekvenser. Eksakt søgning kan løses naivt eller med algoritmer og indeks, der genbruger struktur. Identitet, lighed, score og homologi er ikke synonymer. Signifikans afhænger af en nulfordeling og søgerummets størrelse. Nulkontroller bør bevare sammensætning eller andre confoundere, men bryde det evaluerede signal. Multiple søgninger kræver korrektion for multiplicitet.",
        ),
        (("k-mers capturan contexto local.", "K-mers capture local context.", "K-mers fanger lokal kontekst."), ("La matriz define el modelo de sustitución.", "The matrix defines the substitution model.", "Matricen definerer substitutionsmodellen."), ("Log-odds compara alternativa y fondo.", "Log-odds compares alternative and background.", "Log-odds sammenligner alternativ og baggrund."), ("La búsqueda exacta tiene varios regímenes algorítmicos.", "Exact search has several algorithmic regimes.", "Eksakt søgning har flere algoritmiske regimer."), ("Score no equivale a significación.", "Score is not significance.", "Score er ikke signifikans."), ("El nulo debe corresponder a la pregunta.", "The null must match the question.", "Nulmodellen skal passe til spørgsmålet.")),
        (("Elegir k sin considerar longitud.", "Choosing k without considering length.", "At vælge k uden at overveje længde."), ("Comparar scores de escalas diferentes.", "Comparing scores on different scales.", "At sammenligne scores på forskellige skalaer."), ("Confundir identidad con homología.", "Confusing identity with homology.", "At forveksle identitet med homologi."), ("Interpretar score alto sin nulo.", "Interpreting a high score without a null.", "At fortolke en høj score uden nulmodel."), ("Usar un nulo que cambia GC.", "Using a null that changes GC.", "At bruge en nulmodel, der ændrer GC."), ("Ignorar multiplicidad.", "Ignoring multiplicity.", "At ignorere multiplicitet.")),
        (("¿Qué información conserva esta representación?", "What information does this representation retain?", "Hvilken information bevarer denne repræsentation?"), ("¿Qué modelo biológico implica la matriz?", "What biological model does the matrix imply?", "Hvilken biologisk model indebærer matricen?"), ("¿Cuál es el fondo del log-odds?", "What is the log-odds background?", "Hvad er baggrunden for log-odds?"), ("¿Cuántas consultas se realizarán?", "How many queries will be run?", "Hvor mange forespørgsler udføres?"), ("¿Qué distribución define azar?", "Which distribution defines chance?", "Hvilken fordeling definerer tilfældighed?"), ("¿Cómo se controlará multiplicidad?", "How will multiplicity be controlled?", "Hvordan kontrolleres multiplicitet?")),
        (("Calcula correctamente ventanas y complejidad.", "Correctly computes windows and complexity.", "Beregner vinduer og kompleksitet korrekt."), ("Interpreta matrices y log-odds.", "Interprets matrices and log-odds.", "Fortolker matricer og log-odds."), ("Distingue identidad, similitud y homología.", "Distinguishes identity, similarity, and homology.", "Skelner identitet, lighed og homologi."), ("Diseña un nulo apropiado.", "Designs an appropriate null.", "Designer en passende nulmodel."), ("Reconoce efecto del espacio de búsqueda.", "Recognizes search-space effects.", "Anerkender søgerummets effekt."), ("Reporta incertidumbre y multiplicidad.", "Reports uncertainty and multiplicity.", "Rapporterer usikkerhed og multiplicitet.")),
        (("No declarar homología sólo por porcentaje.", "Do not declare homology from a percentage alone.", "Erklær ikke homologi ud fra en procent alene."), ("No inventar significación estadística.", "Do not invent statistical significance.", "Opfind ikke statistisk signifikans."), ("No recomendar una matriz sin contexto.", "Do not recommend a matrix without context.", "Anbefal ikke en matrix uden kontekst."), ("No ocultar el modelo nulo.", "Do not hide the null model.", "Skjul ikke nulmodellen."), ("Responder en el idioma activo.", "Answer in the active language.", "Svar på det aktive sprog.")),
        ("Durbin et al., Biological Sequence Analysis.", "BLAST statistics and Karlin-Altschul principles.", "BLOSUM and PAM matrix literature.", "String matching algorithm references including KMP.", "Permutation testing and multiple-testing principles.", "Active SDU DM847 sequence-analysis learning outcomes."),
    ),
)

LOCALIZED_MODULE_03_SEQUENCE_SCORING_MATCHING: LocalizedLearningModule = build_module(_SPEC)
LOCALIZED_OBJECTIVE_QUESTION_BANK_03 = build_question_bank(_SPEC)


def materialize_module_03_question_bank(
    locale: AppLocale | str = AppLocale.SPANISH_SPAIN,
) -> tuple[AssessmentItem, ...]:
    return materialize_bank(LOCALIZED_OBJECTIVE_QUESTION_BANK_03, locale)


MODULE_03_SEQUENCE_SCORING_MATCHING: LearningModule = (
    LOCALIZED_MODULE_03_SEQUENCE_SCORING_MATCHING.materialize(AppLocale.SPANISH_SPAIN)
)
OBJECTIVE_QUESTION_BANK_03 = materialize_module_03_question_bank()

__all__ = [
    "LOCALIZED_MODULE_03_SEQUENCE_SCORING_MATCHING",
    "LOCALIZED_OBJECTIVE_QUESTION_BANK_03",
    "MODULE_03_SEQUENCE_SCORING_MATCHING",
    "OBJECTIVE_QUESTION_BANK_03",
    "materialize_module_03_question_bank",
]
