"""DM847 module 6: suffix arrays, BWT, FM-index, and read mapping."""

from __future__ import annotations

from ...i18n import AppLocale
from ..localized_models import LocalizedLearningModule
from ..models import AssessmentItem, LearningModule
from .standard import StandardModuleSpec, build_module, build_question_bank, materialize_bank

_SPEC = StandardModuleSpec(
    module_id="dm847.m06",
    title=(
        "Suffix arrays, BWT y mapeo de lecturas",
        "Suffix arrays, BWT, and read mapping",
        "Suffix arrays, BWT og read-mapping",
    ),
    summary=(
        "Construye índices de texto para búsqueda eficiente, deriva BWT y FM-index, aplica búsqueda hacia atrás y conecta sus propiedades con mapeo de lecturas y restricciones de memoria.",
        "Build text indexes for efficient search, derive BWT and the FM-index, apply backward search, and connect their properties to read mapping and memory constraints.",
        "Byg tekstindeks til effektiv søgning, udled BWT og FM-index, anvend backward search og forbind deres egenskaber med read-mapping og hukommelsesbegrænsninger.",
    ),
    objectives=(
        (
            "m06.o1",
            (
                "Construir y consultar un suffix array.",
                "Build and query a suffix array.",
                "Bygge og forespørge et suffix array.",
            ),
        ),
        (
            "m06.o2",
            (
                "Interpretar el LCP y su utilidad para prefijos compartidos.",
                "Interpret LCP and its use for shared prefixes.",
                "Fortolke LCP og dets brug til delte præfikser.",
            ),
        ),
        (
            "m06.o3",
            (
                "Derivar la transformación Burrows–Wheeler con centinela único.",
                "Derive the Burrows–Wheeler transform with a unique sentinel.",
                "Udlede Burrows–Wheeler-transformationen med en unik sentinel.",
            ),
        ),
        (
            "m06.o4",
            (
                "Explicar LF-mapping y búsqueda hacia atrás.",
                "Explain LF-mapping and backward search.",
                "Forklare LF-mapping og backward search.",
            ),
        ),
        (
            "m06.o5",
            (
                "Relacionar FM-index con compresión y memoria.",
                "Relate the FM-index to compression and memory.",
                "Knytte FM-index til komprimering og hukommelse.",
            ),
        ),
        (
            "m06.o6",
            (
                "Evaluar semillas, mismatches, calidad y ambigüedad en read mapping.",
                "Evaluate seeds, mismatches, quality, and ambiguity in read mapping.",
                "Vurdere seeds, mismatches, kvalitet og tvetydighed i read-mapping.",
            ),
        ),
    ),
    concepts=(
        (
            "suffix-array",
            ("Suffix array", "Suffix array", "Suffix array"),
            (
                "Un suffix array almacena las posiciones iniciales de todos los sufijos ordenados lexicográficamente. La búsqueda de un patrón se reduce a localizar el intervalo de sufijos que comparte ese prefijo mediante búsqueda binaria. Construirlo ingenuamente es costoso, pero existen algoritmos lineales o casi lineales.",
                "A suffix array stores starting positions of all suffixes in lexicographic order. Pattern search becomes locating the interval of suffixes sharing that prefix through binary search. Naive construction is expensive, but linear or near-linear algorithms exist.",
                "Et suffix array lagrer startpositionerne for alle suffikser i leksikografisk rækkefølge. Mønstersøgning bliver lokalisering af intervallet af suffikser med dette præfiks via binær søgning. Naiv konstruktion er dyr, men lineære eller næsten lineære algoritmer findes.",
            ),
            (
                (
                    "El array guarda posiciones, no cadenas completas.",
                    "The array stores positions, not complete strings.",
                    "Arrayet lagrer positioner, ikke komplette strenge.",
                ),
                (
                    "Las coincidencias forman un intervalo contiguo.",
                    "Matches form a contiguous interval.",
                    "Matches danner et sammenhængende interval.",
                ),
            ),
        ),
        (
            "lcp",
            ("Array LCP", "LCP array", "LCP-array"),
            (
                "LCP registra la longitud del prefijo común entre sufijos adyacentes en orden lexicográfico. Permite identificar repeticiones, acelerar consultas y construir estructuras implícitas relacionadas con suffix trees. Su definición debe especificar la convención para la primera entrada.",
                "LCP records the common-prefix length of adjacent suffixes in lexicographic order. It supports repeat detection, faster queries, and implicit structures related to suffix trees. Its definition should specify the convention for the first entry.",
                "LCP registrerer længden af det fælles præfiks mellem nabosuffikser i leksikografisk orden. Det understøtter detektion af gentagelser, hurtigere forespørgsler og implicitte strukturer relateret til suffix trees. Definitionen bør angive konventionen for første indgang.",
            ),
            (
                (
                    "LCP depende del orden del suffix array.",
                    "LCP depends on suffix-array order.",
                    "LCP afhænger af suffix-array-rækkefølgen.",
                ),
                (
                    "Valores altos indican prefijos repetidos largos.",
                    "Large values indicate long repeated prefixes.",
                    "Høje værdier indikerer lange gentagne præfikser.",
                ),
            ),
        ),
        (
            "bwt",
            (
                "Transformación Burrows–Wheeler",
                "Burrows–Wheeler transform",
                "Burrows–Wheeler-transformation",
            ),
            (
                "La BWT puede definirse ordenando rotaciones o, de forma equivalente, tomando el símbolo anterior a cada sufijo ordenado. Un centinela único menor que los demás símbolos hace la transformación reversible. La BWT agrupa contextos similares y suele contener runs útiles para compresión.",
                "BWT can be defined by sorting rotations or equivalently taking the symbol preceding each sorted suffix. A unique sentinel smaller than all other symbols makes the transform reversible. BWT groups similar contexts and often contains runs useful for compression.",
                "BWT kan defineres ved sortering af rotationer eller ækvivalent ved at tage symbolet før hvert sorteret suffiks. En unik sentinel mindre end alle andre symboler gør transformationen reversibel. BWT grupperer lignende kontekster og indeholder ofte runs, der er nyttige til komprimering.",
            ),
            (
                (
                    "El centinela debe ser único.",
                    "The sentinel must be unique.",
                    "Sentinellen skal være unik.",
                ),
                (
                    "BWT reordena; no pierde información con el centinela.",
                    "BWT reorders; it does not lose information with the sentinel.",
                    "BWT omordner; den mister ikke information med sentinellen.",
                ),
            ),
        ),
        (
            "lf-mapping",
            ("LF-mapping", "LF-mapping", "LF-mapping"),
            (
                "La primera columna F contiene los símbolos ordenados y la última L es la BWT. La k-ésima ocurrencia de un símbolo en L corresponde a la k-ésima en F. Esta propiedad LF permite recorrer el texto original y actualizar intervalos de coincidencia al añadir caracteres de derecha a izquierda.",
                "The first column F contains sorted symbols and the last column L is the BWT. The kth occurrence of a symbol in L corresponds to the kth occurrence in F. This LF property supports traversing the original text and updating match intervals when adding characters from right to left.",
                "Den første kolonne F indeholder sorterede symboler, og den sidste kolonne L er BWT. Den k'te forekomst af et symbol i L svarer til den k'te forekomst i F. Denne LF-egenskab gør det muligt at gennemløbe originalteksten og opdatere matchintervaller ved tilføjelse af tegn fra højre mod venstre.",
            ),
            (
                (
                    "Occurrence rank identifica copias iguales.",
                    "Occurrence rank identifies equal copies.",
                    "Occurrence-rank identificerer ens kopier.",
                ),
                (
                    "Backward search procesa el patrón al revés.",
                    "Backward search processes the pattern in reverse.",
                    "Backward search behandler mønstret baglæns.",
                ),
            ),
        ),
        (
            "fm-index",
            ("FM-index y memoria", "FM-index and memory", "FM-index og hukommelse"),
            (
                "El FM-index combina BWT, conteos acumulados C y consultas Occ/rank. Puede localizar el intervalo de un patrón en tiempo proporcional a su longitud, con estructuras comprimidas. Para recuperar posiciones se muestrea el suffix array y se aplica LF hasta una posición almacenada.",
                "The FM-index combines BWT, cumulative counts C, and Occ/rank queries. It locates a pattern interval in time proportional to pattern length using compressed structures. To recover positions, the suffix array is sampled and LF is applied until a stored position is reached.",
                "FM-index kombinerer BWT, kumulative tællinger C og Occ/rank-forespørgsler. Det lokaliserer et mønsterinterval i tid proportional med mønsterlængden ved hjælp af komprimerede strukturer. For at genskabe positioner samples suffix arrayet, og LF anvendes indtil en lagret position nås.",
            ),
            (
                (
                    "Contar y localizar son operaciones distintas.",
                    "Counting and locating are distinct operations.",
                    "Tælling og lokalisering er forskellige operationer.",
                ),
                (
                    "Más muestreo usa más memoria y menos tiempo.",
                    "More sampling uses more memory and less time.",
                    "Mere sampling bruger mere hukommelse og mindre tid.",
                ),
            ),
        ),
        (
            "read-mapping",
            (
                "Principios de read mapping",
                "Read-mapping principles",
                "Principper for read-mapping",
            ),
            (
                "Un mapper busca candidatos mediante semillas o índices y luego verifica con mismatches, gaps o alineamiento. Reads repetitivas pueden mapear a múltiples lugares; errores y variantes reales compiten; calidad de base y orientación importan. La puntuación MAPQ resume ambigüedad del mapeo bajo supuestos del programa y no es una probabilidad universal sin calibración.",
                "A mapper finds candidates through seeds or indexes and then verifies with mismatches, gaps, or alignment. Repetitive reads may map to multiple locations; sequencing errors compete with real variants; base quality and orientation matter. MAPQ summarizes mapping ambiguity under software assumptions and is not a universal probability without calibration.",
                "En mapper finder kandidater gennem seeds eller indeks og verificerer derefter med mismatches, gaps eller alignment. Repetitive reads kan mappe til flere steder; sekventeringsfejl konkurrerer med reelle varianter; basekvalitet og orientering er vigtige. MAPQ opsummerer mapping-tvetydighed under programmets antagelser og er ikke en universel sandsynlighed uden kalibrering.",
            ),
            (
                (
                    "Candidato y alineamiento final son etapas diferentes.",
                    "Candidate generation and final alignment are different stages.",
                    "Kandidatgenerering og endelig alignment er forskellige trin.",
                ),
                (
                    "Multimapping debe conservarse o tratarse explícitamente.",
                    "Multimapping must be retained or handled explicitly.",
                    "Multimapping skal bevares eller håndteres eksplicit.",
                ),
            ),
        ),
    ),
    examples=(
        (
            "m06.e01",
            ("Suffix array ingenuo", "Naive suffix array", "Naivt suffix array"),
            (
                "Ordena posiciones por el sufijo que comienza en cada una.",
                "Sort positions by the suffix beginning at each position.",
                "Sortér positioner efter suffikset, der starter ved hver position.",
            ),
            (
                (
                    "La clave de ordenación es text[i:].",
                    "The sorting key is text[i:].",
                    "Sorteringsnøglen er text[i:].",
                ),
                (
                    "Este método es didáctico, no eficiente para genomas.",
                    "This method is educational, not efficient for genomes.",
                    "Metoden er didaktisk, ikke effektiv for genomer.",
                ),
            ),
            """def suffix_array(text: str) -> list[int]:\n    return sorted(range(len(text)), key=lambda index: text[index:])\n\n\ntext = \"banana$\"\narray = suffix_array(text)\nprint(array)\nprint([text[index:] for index in array])\n""",
            "[6, 5, 3, 1, 0, 4, 2]\n['$', 'a$', 'ana$', 'anana$', 'banana$', 'na$', 'nana$']",
            (
                "Los sufijos que comparten prefijo quedan adyacentes.",
                "Suffixes sharing a prefix become adjacent.",
                "Suffikser med fælles præfiks bliver naboer.",
            ),
        ),
        (
            "m06.e02",
            (
                "Construir BWT desde suffix array",
                "Build BWT from a suffix array",
                "Byg BWT fra et suffix array",
            ),
            (
                "Toma el carácter anterior a cada sufijo ordenado.",
                "Take the character preceding each sorted suffix.",
                "Tag tegnet før hvert sorteret suffiks.",
            ),
            (
                (
                    "Para índice cero, el anterior es el último símbolo.",
                    "For index zero, the predecessor is the final symbol.",
                    "For indeks nul er forgængeren det sidste symbol.",
                ),
                (
                    "El centinela aparece una sola vez.",
                    "The sentinel appears exactly once.",
                    "Sentinellen forekommer præcis én gang.",
                ),
            ),
            """def bwt(text: str) -> str:\n    if text.count(\"$\") != 1 or not text.endswith(\"$\"):\n        raise ValueError(\"text must end with one sentinel\")\n    array = sorted(range(len(text)), key=lambda index: text[index:])\n    return \"\".join(text[index - 1] if index else text[-1] for index in array)\n\n\nprint(bwt(\"banana$\"))\n""",
            "annb$aa",
            (
                "La BWT conserva las mismas frecuencias de símbolos y reordena contextos.",
                "BWT preserves symbol frequencies and reorders contexts.",
                "BWT bevarer symbolfrekvenser og omordner kontekster.",
            ),
        ),
        (
            "m06.e03",
            (
                "Intervalo por búsqueda binaria",
                "Interval by binary search",
                "Interval med binær søgning",
            ),
            (
                "Encuentra suffixes que empiezan por un patrón usando límites lexicográficos.",
                "Find suffixes starting with a pattern using lexicographic bounds.",
                "Find suffikser, der starter med et mønster, ved leksikografiske grænser.",
            ),
            (
                (
                    "El límite inferior busca pattern.",
                    "The lower bound searches for pattern.",
                    "Nedre grænse søger efter pattern.",
                ),
                (
                    "El límite superior usa un símbolo mayor añadido.",
                    "The upper bound uses an appended larger symbol.",
                    "Øvre grænse bruger et tilføjet større symbol.",
                ),
            ),
            """from bisect import bisect_left\n\n\ndef suffix_interval(text: str, pattern: str) -> tuple[int, int]:\n    suffixes = sorted((text[index:], index) for index in range(len(text)))\n    keys = [suffix for suffix, _ in suffixes]\n    left = bisect_left(keys, pattern)\n    right = bisect_left(keys, pattern + chr(0x10FFFF))\n    return left, right\n\n\nprint(suffix_interval(\"banana$\", \"ana\"))\n""",
            "(2, 4)",
            (
                "El intervalo contiene dos sufijos: ana$ y anana$.",
                "The interval contains two suffixes: ana$ and anana$.",
                "Intervallet indeholder to suffikser: ana$ og anana$.",
            ),
        ),
    ),
    practices=(
        (
            "m06.p01",
            "CODE_TRACING",
            (
                "Ordena los sufijos de aba$.",
                "Order the suffixes of aba$.",
                "Ordén suffikserne i aba$.",
            ),
            (("$ es el menor símbolo.", "$ is the smallest symbol.", "$ er det mindste symbol."),),
            (
                "$, a$, aba$, ba$; posiciones [3, 2, 0, 1].",
                "$ , a$, aba$, ba$; positions [3, 2, 0, 1].",
                "$ , a$, aba$, ba$; positioner [3, 2, 0, 1].",
            ),
            (
                "Los prefijos comunes quedan juntos.",
                "Shared prefixes are adjacent.",
                "Delte præfikser er naboer.",
            ),
            "",
        ),
        (
            "m06.p02",
            "SHORT_ANSWER",
            (
                "Explica por qué coincidencias forman un intervalo en el suffix array.",
                "Explain why matches form an interval in a suffix array.",
                "Forklar hvorfor matches danner et interval i et suffix array.",
            ),
            (
                (
                    "Usa orden lexicográfico.",
                    "Use lexicographic order.",
                    "Brug leksikografisk orden.",
                ),
            ),
            (
                "Todos los sufijos con el mismo prefijo se ordenan consecutivamente porque ningún sufijo con un prefijo lexicográficamente diferente puede intercalarse dentro del bloque.",
                "All suffixes with the same prefix sort consecutively because no suffix with a lexicographically different prefix can be interleaved within the block.",
                "Alle suffikser med samme præfiks sorteres sammenhængende, fordi intet suffiks med et leksikografisk andet præfiks kan placeres inde i blokken.",
            ),
            (
                "Esto permite buscar límites en vez de cada posición.",
                "This enables boundary search instead of checking every position.",
                "Dette muliggør grænsesøgning frem for kontrol af hver position.",
            ),
            "",
        ),
        (
            "m06.p03",
            "FILL_IN_THE_BLANK",
            (
                "La BWT requiere un centinela ________.",
                "BWT requires a ________ sentinel.",
                "BWT kræver en ________ sentinel.",
            ),
            (
                (
                    "Debe identificar el final.",
                    "It must identify the end.",
                    "Den skal identificere slutningen.",
                ),
            ),
            ("único", "unique", "unik"),
            (
                "La unicidad hace reversible la transformación.",
                "Uniqueness makes the transform reversible.",
                "Unikhed gør transformationen reversibel.",
            ),
            "",
        ),
        (
            "m06.p04",
            "MATCHING",
            (
                "Relaciona C, Occ y suffix-array sampling.",
                "Match C, Occ, and suffix-array sampling.",
                "Match C, Occ og suffix-array sampling.",
            ),
            (
                (
                    "Cuenta, rank y posición.",
                    "Count, rank, and position.",
                    "Tælling, rank og position.",
                ),
            ),
            (
                "C cuenta símbolos menores; Occ cuenta ocurrencias hasta una posición; sampling permite recuperar coordenadas.",
                "C counts smaller symbols; Occ counts occurrences up to a position; sampling recovers coordinates.",
                "C tæller mindre symboler; Occ tæller forekomster til en position; sampling genskaber koordinater.",
            ),
            (
                "Juntos forman las operaciones principales del FM-index.",
                "Together they form core FM-index operations.",
                "Sammen danner de FM-indexets kerneoperationer.",
            ),
            "",
        ),
        (
            "m06.p05",
            "ORAL_EXPLANATION",
            ("Explica backward search.", "Explain backward search.", "Forklar backward search."),
            (
                (
                    "Procesa patrón de derecha a izquierda.",
                    "Process pattern right to left.",
                    "Behandl mønstret fra højre mod venstre.",
                ),
            ),
            (
                "Se mantiene un intervalo de suffix-array para el sufijo ya procesado; al anteponer un carácter, C y Occ transforman los límites al intervalo de suffixes cuyo prefijo extendido coincide.",
                "Maintain a suffix-array interval for the processed pattern suffix; when prepending a character, C and Occ transform bounds to suffixes matching the extended prefix.",
                "Et suffix-array-interval opretholdes for det behandlede mønstersuffiks; når et tegn foranstilles, transformerer C og Occ grænserne til suffikser, der matcher det udvidede præfiks.",
            ),
            (
                "Si el intervalo queda vacío, no hay coincidencia exacta.",
                "If the interval becomes empty, no exact match exists.",
                "Hvis intervallet bliver tomt, findes intet eksakt match.",
            ),
            "",
        ),
        (
            "m06.p06",
            "DATA_INTERPRETATION",
            (
                "Un read tiene 20 ubicaciones exactas. Interpreta.",
                "A read has 20 exact locations. Interpret.",
                "Et read har 20 eksakte placeringer. Fortolk.",
            ),
            (("Considera repetición.", "Consider repetition.", "Overvej gentagelse."),),
            (
                "El read es repetitivo o corto respecto al genoma. No existe una ubicación única sustentada por coincidencia exacta; debe marcarse multimapping, usar pares/longer context o excluir según el análisis.",
                "The read is repetitive or short relative to the genome. Exact matching does not support one unique location; retain multimapping, use pairs/longer context, or exclude according to analysis.",
                "Readet er repetitivt eller kort i forhold til genomet. Eksakt matching understøtter ikke én unik placering; bevar multimapping, brug par/længere kontekst eller ekskludér efter analysen.",
            ),
            (
                "Elegir arbitrariamente una posición introduce sesgo.",
                "Choosing one position arbitrarily introduces bias.",
                "Vilkårligt valg af én position introducerer bias.",
            ),
            "",
        ),
        (
            "m06.p07",
            "DEBUGGING",
            (
                "La BWT contiene dos centinelas y no se invierte correctamente. Diagnostica.",
                "BWT contains two sentinels and cannot be inverted correctly. Diagnose it.",
                "BWT indeholder to sentineller og kan ikke inverteres korrekt. Diagnosticér.",
            ),
            (("Revisa unicidad.", "Inspect uniqueness.", "Undersøg unikhed."),),
            (
                "Validar exactamente un centinela reservado y ausente del alfabeto original; reconstruir el índice sólo después de corregir la entrada.",
                "Validate exactly one reserved sentinel absent from the original alphabet; rebuild the index only after correcting input.",
                "Validér præcis én reserveret sentinel, som ikke findes i det oprindelige alfabet; genopbyg først indekset efter korrektion af input.",
            ),
            (
                "La ambigüedad rompe la fila inicial y LF-mapping.",
                "Ambiguity breaks the initial row and LF-mapping.",
                "Tvetydighed bryder den initiale række og LF-mapping.",
            ),
            "",
        ),
        (
            "m06.p08",
            "PIPELINE_DESIGN",
            (
                "Diseña un mapper simplificado seed-and-extend.",
                "Design a simplified seed-and-extend mapper.",
                "Design en forenklet seed-and-extend-mapper.",
            ),
            (
                (
                    "Separa candidatos y verificación.",
                    "Separate candidates and verification.",
                    "Adskil kandidater og verifikation.",
                ),
            ),
            (
                "Normalizar read y orientación; extraer semillas; consultar índice; combinar candidatos; extender con alineamiento limitado; puntuar calidad y gaps; conservar empates; reportar coordenadas, CIGAR, score y ambigüedad.",
                "Normalize read and orientation; extract seeds; query index; combine candidates; extend with bounded alignment; score quality and gaps; retain ties; report coordinates, CIGAR, score, and ambiguity.",
                "Normalisér read og orientering; udtræk seeds; forespørg indeks; kombinér kandidater; udvid med begrænset alignment; score kvalitet og gaps; bevar ties; rapportér koordinater, CIGAR, score og tvetydighed.",
            ),
            (
                "La validación requiere reads simuladas y regiones repetitivas.",
                "Validation requires simulated reads and repetitive regions.",
                "Validering kræver simulerede reads og repetitive regioner.",
            ),
            "",
        ),
    ),
    mcqs=(
        (
            "001",
            (
                "¿Qué almacena un suffix array?",
                "What does a suffix array store?",
                "Hvad lagrer et suffix array?",
            ),
            (
                (
                    "positions",
                    (
                        "Posiciones de sufijos ordenados",
                        "Positions of sorted suffixes",
                        "Positioner for sorterede suffikser",
                    ),
                ),
                (
                    "strings",
                    (
                        "Copias completas de sufijos",
                        "Full suffix copies",
                        "Fuldstændige suffikskopier",
                    ),
                ),
                ("scores", ("Scores de alineamiento", "Alignment scores", "Alignment-scores")),
            ),
            "positions",
            (
                "El texto original permite recuperar cada sufijo.",
                "Original text recovers each suffix.",
                "Originalteksten genskaber hvert suffiks.",
            ),
        ),
        (
            "002",
            (
                "¿Qué indica LCP alto?",
                "What does a large LCP indicate?",
                "Hvad indikerer en høj LCP?",
            ),
            (
                ("prefix", ("Prefijo común largo", "Long common prefix", "Langt fælles præfiks")),
                (
                    "distance",
                    ("Gran distancia genómica", "Large genomic distance", "Stor genomisk afstand"),
                ),
                ("quality", ("Alta calidad de base", "High base quality", "Høj basekvalitet")),
            ),
            "prefix",
            (
                "LCP mide prefijos de suffixes adyacentes.",
                "LCP measures prefixes of adjacent suffixes.",
                "LCP måler præfikser af nabosuffikser.",
            ),
        ),
        (
            "003",
            (
                "¿Qué necesita BWT para ser reversible?",
                "What does BWT need to be reversible?",
                "Hvad kræver BWT for at være reversibel?",
            ),
            (
                ("sentinel", ("Centinela único", "Unique sentinel", "Unik sentinel")),
                ("random", ("Semilla aleatoria", "Random seed", "Tilfældig seed")),
                ("matrix", ("Matriz de sustitución", "Substitution matrix", "Substitutionsmatrix")),
            ),
            "sentinel",
            (
                "Marca el final de texto de forma inequívoca.",
                "It unambiguously marks text end.",
                "Den markerer tekstens slutning entydigt.",
            ),
        ),
        (
            "004",
            ("¿Qué columna es la BWT?", "Which column is the BWT?", "Hvilken kolonne er BWT?"),
            (
                ("last", ("Última L", "Last L", "Sidste L")),
                ("first", ("Primera F", "First F", "Første F")),
                ("middle", ("Columna central", "Middle column", "Midterkolonne")),
            ),
            "last",
            (
                "F contiene símbolos ordenados; L es la transformación.",
                "F contains sorted symbols; L is the transform.",
                "F indeholder sorterede symboler; L er transformationen.",
            ),
        ),
        (
            "005",
            (
                "¿Qué preserva LF-mapping?",
                "What does LF-mapping preserve?",
                "Hvad bevarer LF-mapping?",
            ),
            (
                (
                    "rank",
                    (
                        "Rango de ocurrencia del símbolo",
                        "Occurrence rank of the symbol",
                        "Forekomstrang for symbolet",
                    ),
                ),
                (
                    "position",
                    (
                        "Posición original directa",
                        "Direct original position",
                        "Direkte original position",
                    ),
                ),
                ("quality", ("Calidad", "Quality", "Kvalitet")),
            ),
            "rank",
            (
                "La k-ésima ocurrencia en L corresponde a la k-ésima en F.",
                "The kth occurrence in L corresponds to kth in F.",
                "Den k'te forekomst i L svarer til den k'te i F.",
            ),
        ),
        (
            "006",
            (
                "¿En qué dirección procesa backward search?",
                "In which direction does backward search process?",
                "I hvilken retning behandler backward search?",
            ),
            (
                ("reverse", ("Derecha a izquierda", "Right to left", "Højre mod venstre")),
                ("forward", ("Izquierda a derecha", "Left to right", "Venstre mod højre")),
                ("random", ("Aleatoria", "Random", "Tilfældig")),
            ),
            "reverse",
            (
                "Cada paso antepone un símbolo.",
                "Each step prepends a symbol.",
                "Hvert trin foranstiller et symbol.",
            ),
        ),
        (
            "007",
            (
                "¿Qué operación del FM-index devuelve número de matches?",
                "Which FM-index operation returns match count?",
                "Hvilken FM-index-operation returnerer antal matches?",
            ),
            (
                ("count", ("Tamaño del intervalo", "Interval size", "Intervalstørrelse")),
                ("locate", ("Locate", "Locate", "Locate")),
                ("align", ("Alinear", "Align", "Align")),
            ),
            "count",
            (
                "El intervalo de suffix-array enumera coincidencias.",
                "The suffix-array interval enumerates matches.",
                "Suffix-array-intervallet opregner matches.",
            ),
        ),
        (
            "008",
            (
                "¿Qué compromiso introduce sampling del suffix array?",
                "What trade-off does suffix-array sampling introduce?",
                "Hvilket kompromis introducerer sampling af suffix array?",
            ),
            (
                (
                    "memory",
                    (
                        "Memoria frente a tiempo de locate",
                        "Memory versus locate time",
                        "Hukommelse mod locate-tid",
                    ),
                ),
                ("accuracy", ("Precisión biológica", "Biological accuracy", "Biologisk præcision")),
                ("alphabet", ("Tamaño de alfabeto", "Alphabet size", "Alfabetstørrelse")),
            ),
            "memory",
            (
                "Más muestras aceleran locate pero ocupan más.",
                "More samples speed locate but use more space.",
                "Flere samples accelererer locate, men bruger mere plads.",
            ),
        ),
        (
            "009",
            (
                "¿Qué etapa verifica candidatos de semillas?",
                "Which stage verifies seed candidates?",
                "Hvilket trin verificerer seed-kandidater?",
            ),
            (
                (
                    "extend",
                    ("Extensión/alineamiento", "Extension/alignment", "Udvidelse/alignment"),
                ),
                (
                    "index",
                    ("Sólo construir índice", "Index construction only", "Kun indekskonstruktion"),
                ),
                ("sort", ("Ordenar nombres", "Sort names", "Sortér navne")),
            ),
            "extend",
            (
                "Las semillas generan candidatos; la extensión evalúa el match completo.",
                "Seeds generate candidates; extension evaluates the full match.",
                "Seeds genererer kandidater; udvidelse evaluerer det fulde match.",
            ),
        ),
        (
            "010",
            (
                "¿Qué indica múltiples ubicaciones igualmente buenas?",
                "What do multiple equally good locations indicate?",
                "Hvad indikerer flere lige gode placeringer?",
            ),
            (
                ("ambiguous", ("Mapeo ambiguo", "Ambiguous mapping", "Tvetydig mapping")),
                ("unique", ("Mapeo único", "Unique mapping", "Unik mapping")),
                ("error", ("Error seguro", "Certain error", "Sikker fejl")),
            ),
            "ambiguous",
            (
                "La repetición impide asignación única.",
                "Repetition prevents unique assignment.",
                "Gentagelse forhindrer unik tildeling.",
            ),
        ),
    ),
    true_false=(
        (
            "011",
            (
                "Un suffix array almacena todos los sufijos completos.",
                "A suffix array stores every complete suffix.",
                "Et suffix array lagrer alle komplette suffikser.",
            ),
            False,
            (
                "Almacena posiciones ordenadas.",
                "It stores sorted positions.",
                "Det lagrer sorterede positioner.",
            ),
        ),
        (
            "012",
            (
                "Coincidencias exactas forman un intervalo contiguo.",
                "Exact matches form a contiguous interval.",
                "Eksakte matches danner et sammenhængende interval.",
            ),
            True,
            (
                "Comparten el mismo prefijo lexicográfico.",
                "They share the same lexicographic prefix.",
                "De deler samme leksikografiske præfiks.",
            ),
        ),
        (
            "013",
            (
                "BWT cambia las frecuencias de símbolos.",
                "BWT changes symbol frequencies.",
                "BWT ændrer symbolfrekvenser.",
            ),
            False,
            ("Sólo reordena símbolos.", "It only reorders symbols.", "Den omordner kun symboler."),
        ),
        (
            "014",
            (
                "El centinela puede aparecer varias veces.",
                "The sentinel may appear several times.",
                "Sentinellen kan forekomme flere gange.",
            ),
            False,
            (
                "Debe ser único para inversión inequívoca.",
                "It must be unique for unambiguous inversion.",
                "Den skal være unik for entydig inversion.",
            ),
        ),
        (
            "015",
            (
                "Backward search procesa el patrón desde el final.",
                "Backward search processes the pattern from the end.",
                "Backward search behandler mønstret fra slutningen.",
            ),
            True,
            (
                "Cada actualización antepone un símbolo.",
                "Each update prepends a symbol.",
                "Hver opdatering foranstiller et symbol.",
            ),
        ),
        (
            "016",
            (
                "FM-index puede usar estructuras comprimidas.",
                "FM-index can use compressed structures.",
                "FM-index kan bruge komprimerede strukturer.",
            ),
            True,
            (
                "La BWT suele favorecer runs y rank comprimido.",
                "BWT often supports runs and compressed rank.",
                "BWT understøtter ofte runs og komprimeret rank.",
            ),
        ),
        (
            "017",
            (
                "Contar matches y localizar coordenadas son idénticos.",
                "Counting matches and locating coordinates are identical.",
                "Tælling af matches og lokalisering af koordinater er identiske.",
            ),
            False,
            (
                "Locate requiere información adicional o LF hasta muestras.",
                "Locate requires extra information or LF to samples.",
                "Locate kræver ekstra information eller LF til samples.",
            ),
        ),
        (
            "018",
            (
                "Una seed exacta garantiza el mejor alineamiento completo.",
                "An exact seed guarantees the best full alignment.",
                "En eksakt seed garanterer den bedste fulde alignment.",
            ),
            False,
            (
                "La extensión y competidores deben evaluarse.",
                "Extension and competing candidates must be evaluated.",
                "Udvidelse og konkurrerende kandidater skal evalueres.",
            ),
        ),
        (
            "019",
            (
                "Reads repetitivas pueden tener multimapping.",
                "Repetitive reads may have multimapping.",
                "Repetitive reads kan have multimapping.",
            ),
            True,
            (
                "Varias regiones pueden producir el mismo match.",
                "Several regions may produce the same match.",
                "Flere regioner kan give samme match.",
            ),
        ),
        (
            "020",
            (
                "MAPQ es una probabilidad universal independiente del mapper.",
                "MAPQ is a universal probability independent of mapper.",
                "MAPQ er en universel sandsynlighed uafhængig af mapperen.",
            ),
            False,
            (
                "Su interpretación depende de modelo y calibración del programa.",
                "Its interpretation depends on software model and calibration.",
                "Fortolkningen afhænger af programmets model og kalibrering.",
            ),
        ),
    ),
    tutor=(
        (
            "Los índices de sufijos reorganizan un texto para responder muchas consultas. El suffix array almacena posiciones de sufijos ordenados; LCP resume prefijos compartidos. BWT reordena caracteres según el orden de sufijos y requiere un centinela único. LF-mapping conecta ocurrencias de L y F; con conteos C y Occ permite backward search. El FM-index comprime estas operaciones y separa count de locate, usando sampling para equilibrar memoria y tiempo. En mapeo de reads, el índice genera candidatos y una etapa de extensión verifica mismatches y gaps. Repeticiones, orientación, calidad y variantes crean ambigüedad que debe conservarse y validarse. La auditoría confirma que count, locate y coordenadas proceden de la misma versión del índice.",
            "Suffix indexes reorganize text to answer many queries. A suffix array stores positions of sorted suffixes; LCP summarizes shared prefixes. BWT reorders characters according to suffix order and requires a unique sentinel. LF-mapping connects occurrences in L and F; with C counts and Occ it enables backward search. The FM-index compresses these operations and separates count from locate, using sampling to trade memory for time. In read mapping, the index generates candidates and an extension stage verifies mismatches and gaps. Repeats, orientation, quality, and variants create ambiguity that should be retained and validated. Auditing confirms that count, locate, and coordinates come from the same index version.",
            "Suffiksindeks omorganiserer tekst for at besvare mange forespørgsler. Et suffix array lagrer positioner for sorterede suffikser; LCP opsummerer delte præfikser. BWT omordner tegn efter suffiksrækkefølge og kræver en unik sentinel. LF-mapping forbinder forekomster i L og F; med C-tællinger og Occ muliggør det backward search. FM-index komprimerer disse operationer og adskiller count fra locate med sampling som kompromis mellem hukommelse og tid. Ved read-mapping genererer indekset kandidater, og en udvidelsesfase verificerer mismatches og gaps. Gentagelser, orientering, kvalitet og varianter skaber tvetydighed, som bør bevares og valideres. Audit bekræfter, at count, locate og koordinater kommer fra samme indeksversion.",
        ),
        (
            (
                "Suffix array lagrer positioner.",
                "Suffix array stores positions.",
                "Suffix array lagrer positioner.",
            ),
            (
                "LCP måler delte præfikser.",
                "LCP measures shared prefixes.",
                "LCP måler delte præfikser.",
            ),
            (
                "BWT kræver unik sentinel.",
                "BWT requires a unique sentinel.",
                "BWT kræver unik sentinel.",
            ),
            (
                "LF bevarer occurrence-rank.",
                "LF preserves occurrence rank.",
                "LF bevarer occurrence-rank.",
            ),
            (
                "FM-index adskiller count og locate.",
                "FM-index separates count and locate.",
                "FM-index adskiller count og locate.",
            ),
            (
                "Read mapping kræver kandidatverifikation.",
                "Read mapping requires candidate verification.",
                "Read mapping kræver kandidatverifikation.",
            ),
        ),
        (
            (
                "Lagring af komplette suffikser.",
                "Storing complete suffixes.",
                "Lagring af komplette suffikser.",
            ),
            ("Flere sentineller.", "Using multiple sentinels.", "Brug af flere sentineller."),
            ("Forveksling af F og L.", "Confusing F and L.", "Forveksling af F og L."),
            (
                "At behandle count som locate.",
                "Treating count as locate.",
                "At behandle count som locate.",
            ),
            (
                "At vælge en multimapping-position vilkårligt.",
                "Choosing a multimapping position arbitrarily.",
                "At vælge en multimapping-position vilkårligt.",
            ),
            (
                "At fortolke MAPQ universelt.",
                "Interpreting MAPQ universally.",
                "At fortolke MAPQ universelt.",
            ),
        ),
        (
            ("Hvad lagres i indekset?", "What is stored in the index?", "Hvad lagres i indekset?"),
            ("Er sentinellen unik?", "Is the sentinel unique?", "Er sentinellen unik?"),
            (
                "Hvad betyder intervalgrænserne?",
                "What do interval bounds mean?",
                "Hvad betyder intervalgrænserne?",
            ),
            (
                "Kræves count eller locate?",
                "Is count or locate needed?",
                "Kræves count eller locate?",
            ),
            (
                "Hvordan håndteres mismatches?",
                "How are mismatches handled?",
                "Hvordan håndteres mismatches?",
            ),
            (
                "Hvordan rapporteres multimapping?",
                "How is multimapping reported?",
                "Hvordan rapporteres multimapping?",
            ),
        ),
        (
            (
                "Bygger korrekte suffix arrays og BWT.",
                "Builds correct suffix arrays and BWT.",
                "Bygger korrekte suffix arrays og BWT.",
            ),
            (
                "Forklarer LF og backward search.",
                "Explains LF and backward search.",
                "Forklarer LF og backward search.",
            ),
            (
                "Analyserer hukommelseskompromis.",
                "Analyzes memory trade-offs.",
                "Analyserer hukommelseskompromis.",
            ),
            (
                "Adskiller count og locate.",
                "Distinguishes count and locate.",
                "Adskiller count og locate.",
            ),
            (
                "Designer seed-and-extend korrekt.",
                "Designs seed-and-extend correctly.",
                "Designer seed-and-extend korrekt.",
            ),
            (
                "Bevarer mapping-usikkerhed.",
                "Retains mapping uncertainty.",
                "Bevarer mapping-usikkerhed.",
            ),
        ),
        (
            (
                "Opfind ikke mapping-koordinater.",
                "Do not invent mapping coordinates.",
                "Opfind ikke mapping-koordinater.",
            ),
            ("Skjul ikke multimapping.", "Do not hide multimapping.", "Skjul ikke multimapping."),
            (
                "Antag ikke at MAPQ er universelt kalibreret.",
                "Do not assume MAPQ is universally calibrated.",
                "Antag ikke at MAPQ er universelt kalibreret.",
            ),
            (
                "Brug ikke naive konstruktioner som genom-anbefaling.",
                "Do not recommend naive construction for genomes.",
                "Brug ikke naive konstruktioner som genom-anbefaling.",
            ),
            ("Svar på aktivt sprog.", "Answer in the active language.", "Svar på aktivt sprog."),
        ),
        (
            "Manber and Myers suffix-array literature.",
            "Burrows and Wheeler transform.",
            "Ferragina-Manzini FM-index.",
            "Backward-search and rank/select data structures.",
            "Modern seed-and-extend read mapping literature.",
            "Active SDU DM847 suffix-array and BWT learning outcomes.",
        ),
    ),
)

LOCALIZED_MODULE_06_SUFFIX_ARRAYS_BWT_MAPPING: LocalizedLearningModule = build_module(_SPEC)
LOCALIZED_OBJECTIVE_QUESTION_BANK_06 = build_question_bank(_SPEC)


def materialize_module_06_question_bank(
    locale: AppLocale | str = AppLocale.SPANISH_SPAIN,
) -> tuple[AssessmentItem, ...]:
    return materialize_bank(LOCALIZED_OBJECTIVE_QUESTION_BANK_06, locale)


MODULE_06_SUFFIX_ARRAYS_BWT_MAPPING: LearningModule = (
    LOCALIZED_MODULE_06_SUFFIX_ARRAYS_BWT_MAPPING.materialize(AppLocale.SPANISH_SPAIN)
)
OBJECTIVE_QUESTION_BANK_06 = materialize_module_06_question_bank()

__all__ = [
    "LOCALIZED_MODULE_06_SUFFIX_ARRAYS_BWT_MAPPING",
    "LOCALIZED_OBJECTIVE_QUESTION_BANK_06",
    "MODULE_06_SUFFIX_ARRAYS_BWT_MAPPING",
    "OBJECTIVE_QUESTION_BANK_06",
    "materialize_module_06_question_bank",
]
