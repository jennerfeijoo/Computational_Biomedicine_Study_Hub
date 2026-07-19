"""DM847 module 1: molecular information and computable representations."""

from __future__ import annotations

from ...i18n import AppLocale
from ...learning.activity_types import ActivityType
from ..localized_models import LocalizedLearningModule
from ..models import AssessmentItem, LearningModule
from .authoring import (
    authored_item,
    concept,
    example,
    objective,
    objective_mcq,
    objective_tf,
    practice,
    t,
    tutor_support,
)

_OBJECTIVES = (
    (
        "m01.o1",
        (
            "Relacionar el dogma central con objetos de datos y transformaciones computables.",
            "Relate the central dogma to data objects and computable transformations.",
            "Knytte det centrale dogme til dataobjekter og beregnelige transformationer.",
        ),
    ),
    (
        "m01.o2",
        (
            "Representar ADN, ARN y proteínas con alfabetos, identidad y orientación explícitos.",
            "Represent DNA, RNA, and proteins with explicit alphabets, identity, and orientation.",
            "Repræsentere DNA, RNA og proteiner med eksplicitte alfabeter, identitet og orientering.",
        ),
    ),
    (
        "m01.o3",
        (
            "Calcular complemento inverso y composición sin perder la semántica de hebra.",
            "Compute reverse complements and composition without losing strand semantics.",
            "Beregne omvendt komplement og sammensætning uden at miste strengsemantik.",
        ),
    ),
    (
        "m01.o4",
        (
            "Convertir coordenadas biológicas a índices de programación con validaciones explícitas.",
            "Convert biological coordinates to programming indexes with explicit validation.",
            "Konvertere biologiske koordinater til programmeringsindeks med eksplicit validering.",
        ),
    ),
    (
        "m01.o5",
        (
            "Separar secuencia, anotación, señal experimental y condición biológica.",
            "Separate sequence, annotation, experimental signal, and biological condition.",
            "Adskille sekvens, annotation, eksperimentelt signal og biologisk betingelse.",
        ),
    ),
    (
        "m01.o6",
        (
            "Transformar una pregunta biomédica en representación, operación y validación reproducibles.",
            "Transform a biomedical question into reproducible representation, operation, and validation.",
            "Omsætte et biomedicinsk spørgsmål til reproducerbar repræsentation, operation og validering.",
        ),
    ),
)

_CONCEPTS = (
    (
        "central-dogma-as-data-flow",
        (
            "Dogma central como flujo de información",
            "The central dogma as information flow",
            "Det centrale dogme som informationsflow",
        ),
        (
            "El dogma central relaciona ADN, ARN y proteína, pero una cadena de caracteres no identifica por sí sola un gen, un transcrito o una proteína. Cada transformación requiere declarar región, hebra, marco de lectura, código genético y contexto. El modelo computacional debe conservar estos supuestos como metadatos.",
            "The central dogma relates DNA, RNA, and protein, but a character string alone does not identify a gene, transcript, or protein. Each transformation requires an explicit region, strand, reading frame, genetic code, and context. The computational model should preserve these assumptions as metadata.",
            "Det centrale dogme forbinder DNA, RNA og protein, men en tegnstreng identificerer ikke alene et gen, transkript eller protein. Hver transformation kræver eksplicit region, streng, læseramme, genetisk kode og kontekst. Beregningsmodellen bør bevare disse antagelser som metadata.",
        ),
        (
            (
                "Entidad biológica y cadena computacional no son sinónimos.",
                "A biological entity and a computational string are not synonyms.",
                "En biologisk enhed og en beregningsstreng er ikke synonymer.",
            ),
            (
                "Hebra, marco y procedencia forman parte del dato.",
                "Strand, frame, and provenance are part of the data.",
                "Streng, læseramme og proveniens er en del af data.",
            ),
        ),
    ),
    (
        "alphabets-and-ambiguity",
        (
            "Alfabetos y símbolos ambiguos",
            "Alphabets and ambiguous symbols",
            "Alfabeter og tvetydige symboler",
        ),
        (
            "ADN canónico usa A, C, G y T; ARN usa U en lugar de T; proteínas emplean códigos de aminoácidos. Los códigos IUPAC permiten ambigüedad, por ejemplo N para una base no determinada. Aceptar o rechazar ambigüedad debe depender de la operación y quedar documentado.",
            "Canonical DNA uses A, C, G, and T; RNA uses U instead of T; proteins use amino-acid codes. IUPAC symbols permit ambiguity, such as N for an undetermined base. Whether ambiguity is accepted or rejected should depend on the operation and be documented.",
            "Kanonisk DNA bruger A, C, G og T; RNA bruger U i stedet for T; proteiner bruger aminosyrekoder. IUPAC-symboler tillader tvetydighed, for eksempel N for en ubestemt base. Accept eller afvisning af tvetydighed bør afhænge af operationen og dokumenteres.",
        ),
        (
            (
                "No mezcles T y U sin una conversión definida.",
                "Do not mix T and U without a defined conversion.",
                "Bland ikke T og U uden en defineret konvertering.",
            ),
            (
                "Declara si aceptas códigos IUPAC.",
                "State whether IUPAC codes are accepted.",
                "Angiv om IUPAC-koder accepteres.",
            ),
        ),
    ),
    (
        "strand-and-reverse-complement",
        (
            "Hebra y complemento inverso",
            "Strand and reverse complement",
            "Streng og omvendt komplement",
        ),
        (
            "Las hebras de ADN son antiparalelas. Para expresar la hebra opuesta en orientación 5'→3' se complementan las bases y se invierte el orden. Complementar sin invertir no produce el complemento inverso. La orientación debe acompañar búsquedas de motivos y anotaciones.",
            "DNA strands are antiparallel. To express the opposite strand in 5'→3' orientation, bases are complemented and order is reversed. Complementing without reversing does not produce the reverse complement. Orientation should accompany motif searches and annotations.",
            "DNA-strenge er antiparallelle. For at udtrykke den modsatte streng i 5'→3'-retning komplementeres baserne, og rækkefølgen vendes. Komplementering uden vending giver ikke det omvendte komplement. Orientering bør følge motivsøgninger og annotationer.",
        ),
        (
            (
                "Complemento e inversión son operaciones distintas.",
                "Complement and reversal are distinct operations.",
                "Komplement og vending er forskellige operationer.",
            ),
            (
                "El resultado se expresa normalmente 5'→3'.",
                "The result is normally expressed 5'→3'.",
                "Resultatet udtrykkes normalt 5'→3'.",
            ),
        ),
    ),
    (
        "coordinates-and-intervals",
        (
            "Coordenadas e intervalos",
            "Coordinates and intervals",
            "Koordinater og intervaller",
        ),
        (
            "Los formatos biológicos no comparten una convención única. Una anotación puede usar coordenadas 1-based inclusivas, mientras Python usa índices 0-based y cortes con final exclusivo. El intervalo biológico [inicio, fin] se convierte a sequence[inicio - 1:fin]. La longitud esperada es fin - inicio + 1.",
            "Biological formats do not share one convention. An annotation may use 1-based inclusive coordinates, while Python uses 0-based indexes and half-open slices. Biological interval [start, end] converts to sequence[start - 1:end]. Expected length is end - start + 1.",
            "Biologiske formater deler ikke én konvention. En annotation kan bruge 1-baserede inklusive koordinater, mens Python bruger 0-baserede indeks og halvåbne slices. Det biologiske interval [start, slut] konverteres til sequence[start - 1:end]. Forventet længde er slut - start + 1.",
        ),
        (
            (
                "Guarda la convención junto al intervalo.",
                "Store the convention with the interval.",
                "Gem konventionen sammen med intervallet.",
            ),
            (
                "Verifica la longitud antes y después de convertir.",
                "Verify length before and after conversion.",
                "Kontrollér længden før og efter konvertering.",
            ),
        ),
    ),
    (
        "regulatory-context",
        (
            "Regulación y contexto epigenético",
            "Regulation and epigenetic context",
            "Regulering og epigenetisk kontekst",
        ),
        (
            "La misma secuencia puede tener consecuencias distintas según tipo celular, estado, accesibilidad de cromatina, metilación y factores de transcripción. Una marca epigenética es una observación asociada a posición, muestra y ensayo; no es necesariamente un cambio en la cadena de bases. Secuencia, anotación, señal y condición deben modelarse por separado.",
            "The same sequence may have different consequences depending on cell type, state, chromatin accessibility, methylation, and transcription factors. An epigenetic mark is an observation linked to position, sample, and assay; it is not necessarily a change in the base string. Sequence, annotation, signal, and condition should be modelled separately.",
            "Den samme sekvens kan have forskellige konsekvenser afhængigt af celletype, tilstand, kromatintilgængelighed, methylering og transkriptionsfaktorer. Et epigenetisk mærke er en observation knyttet til position, prøve og assay; det er ikke nødvendigvis en ændring i basestrengen. Sekvens, annotation, signal og betingelse bør modelleres separat.",
        ),
        (
            (
                "Secuencia y señal experimental son capas distintas.",
                "Sequence and experimental signal are distinct layers.",
                "Sekvens og eksperimentelt signal er forskellige lag.",
            ),
            (
                "Correlación no demuestra causalidad.",
                "Correlation does not establish causality.",
                "Korrelation viser ikke kausalitet.",
            ),
        ),
    ),
    (
        "question-to-computation",
        (
            "De la pregunta al problema computacional",
            "From question to computational problem",
            "Fra spørgsmål til beregningsproblem",
        ),
        (
            "Un flujo bioinformático comienza con una pregunta delimitada y una unidad de análisis. Después define representación, operación, criterio de éxito y validación. Preguntar si una región es rica en GC exige definir región, referencia, tratamiento de símbolos ambiguos, estadístico y comparación. El resultado debe regresar al contexto biológico con incertidumbre y limitaciones.",
            "A bioinformatics workflow begins with a bounded question and a unit of analysis. It then defines representation, operation, success criterion, and validation. Asking whether a region is GC-rich requires a region, reference, ambiguity policy, statistic, and comparison. The result should return to biological context with uncertainty and limitations.",
            "Et bioinformatikworkflow begynder med et afgrænset spørgsmål og en analyseenhed. Derefter defineres repræsentation, operation, succeskriterium og validering. At spørge om en region er GC-rig kræver region, reference, tvetydighedspolitik, statistik og sammenligning. Resultatet bør føres tilbage til biologisk kontekst med usikkerhed og begrænsninger.",
        ),
        (
            (
                "Define la unidad de análisis.",
                "Define the unit of analysis.",
                "Definér analyseenheden.",
            ),
            (
                "Separa representación, algoritmo y validación.",
                "Separate representation, algorithm, and validation.",
                "Adskil repræsentation, algoritme og validering.",
            ),
        ),
    ),
)

_EXAMPLES = (
    (
        "m01.e01",
        ("Validar ADN", "Validate DNA", "Validér DNA"),
        (
            "Normaliza una secuencia, valida A/C/G/T/N y calcula GC sobre bases conocidas.",
            "Normalize a sequence, validate A/C/G/T/N, and compute GC over known bases.",
            "Normalisér en sekvens, validér A/C/G/T/N og beregn GC over kendte baser.",
        ),
        (
            (
                "Normalizar mayúsculas y espacios.",
                "Normalize case and whitespace.",
                "Normalisér store bogstaver og mellemrum.",
            ),
            (
                "Excluir N del denominador declarado.",
                "Exclude N from the declared denominator.",
                "Udeluk N fra den deklarerede nævner.",
            ),
        ),
        """def gc_summary(raw: str) -> tuple[str, float, int]:
    sequence = \"\".join(raw.split()).upper()
    if set(sequence) - set(\"ACGTN\"):
        raise ValueError(\"invalid DNA symbol\")
    known = [base for base in sequence if base in \"ACGT\"]
    gc = sum(base in \"GC\" for base in known)
    fraction = gc / len(known) if known else 0.0
    return sequence, round(fraction, 3), len(known)


print(gc_summary(\"acg tnn gc\"))
""",
        "('ACGTNNGC', 0.667, 6)",
        (
            "El denominador se informa porque el tratamiento de N cambia la interpretación.",
            "The denominator is reported because handling N changes interpretation.",
            "Nævneren rapporteres fordi behandling af N ændrer fortolkningen.",
        ),
    ),
    (
        "m01.e02",
        ("Complemento inverso", "Reverse complement", "Omvendt komplement"),
        (
            "Obtén la hebra opuesta 5'→3' con validación explícita.",
            "Obtain the opposite 5'→3' strand with explicit validation.",
            "Find den modsatte 5'→3'-streng med eksplicit validering.",
        ),
        (
            (
                "Complementar las bases.",
                "Complement the bases.",
                "Komplementér baserne.",
            ),
            (
                "Invertir el orden.",
                "Reverse the order.",
                "Vend rækkefølgen.",
            ),
        ),
        """def reverse_complement(sequence: str) -> str:
    normalized = sequence.upper()
    if set(normalized) - set(\"ACGTN\"):
        raise ValueError(\"unsupported symbol\")
    table = str.maketrans(\"ACGTN\", \"TGCAN\")
    return normalized.translate(table)[::-1]


print(reverse_complement(\"ATGCN\"))
""",
        "NGCAT",
        (
            "translate complementa y [::-1] cambia la orientación.",
            "translate complements and [::-1] changes orientation.",
            "translate komplementerer og [::-1] ændrer orientering.",
        ),
    ),
    (
        "m01.e03",
        ("Convertir coordenadas", "Convert coordinates", "Konvertér koordinater"),
        (
            "Extrae una región 1-based inclusiva usando un corte Python.",
            "Extract a 1-based inclusive region using a Python slice.",
            "Udtræk en 1-baseret inklusiv region med et Python-slice.",
        ),
        (
            (
                "Validar límites.",
                "Validate boundaries.",
                "Validér grænser.",
            ),
            (
                "Conservar la longitud esperada.",
                "Preserve expected length.",
                "Bevar forventet længde.",
            ),
        ),
        """def extract_region(sequence: str, start: int, end: int) -> str:
    if not 1 <= start <= end <= len(sequence):
        raise ValueError(\"invalid interval\")
    result = sequence[start - 1:end]
    if len(result) != end - start + 1:
        raise AssertionError(\"length mismatch\")
    return result


print(extract_region(\"AACCGGTT\", 3, 6))
""",
        "CCGG",
        (
            "La invariante de longitud detecta errores de desplazamiento de uno.",
            "The length invariant detects off-by-one errors.",
            "Længdeinvarianten opdager off-by-one-fejl.",
        ),
    ),
)

_PRACTICES = (
    (
        "m01.p01",
        "SHORT_ANSWER",
        (
            "Distingue secuencia de referencia, gen, transcrito y proteína.",
            "Distinguish reference sequence, gene, transcript, and protein.",
            "Skeln mellem referencesekvens, gen, transkript og protein.",
        ),
        (("Describe entidades y relaciones.", "Describe entities and relationships.", "Beskriv enheder og relationer."),),
        (
            "La referencia es una representación ensamblada; un gen es una unidad anotada; un transcrito es un producto de ARN; una proteína es un producto traducido.",
            "A reference is an assembled representation; a gene is an annotated unit; a transcript is an RNA product; a protein is a translated product.",
            "En reference er en samlet repræsentation; et gen er en annoteret enhed; et transkript er et RNA-produkt; et protein er et translateret produkt.",
        ),
        (
            "Una misma región puede asociarse a varios transcritos.",
            "One region may be associated with several transcripts.",
            "Én region kan være knyttet til flere transkripter.",
        ),
        "",
    ),
    (
        "m01.p02",
        "CODE_TRACING",
        (
            "Traza el complemento inverso de AAGTC.",
            "Trace the reverse complement of AAGTC.",
            "Gennemgå det omvendte komplement af AAGTC.",
        ),
        (("Complementa y luego invierte.", "Complement and then reverse.", "Komplementér og vend derefter."),),
        ("TTCAG → GACTT", "TTCAG → GACTT", "TTCAG → GACTT"),
        (
            "El resultado final representa la hebra opuesta 5'→3'.",
            "The final result represents the opposite strand 5'→3'.",
            "Slutresultatet repræsenterer den modsatte streng 5'→3'.",
        ),
        "",
    ),
    (
        "m01.p03",
        "DEBUGGING",
        (
            "Corrige sequence[start:end] para coordenadas 1-based inclusivas.",
            "Fix sequence[start:end] for 1-based inclusive coordinates.",
            "Ret sequence[start:end] for 1-baserede inklusive koordinater.",
        ),
        (("Desplaza sólo el inicio.", "Shift only the start.", "Forskyd kun start."),),
        (
            "Usar sequence[start - 1:end] y comprobar end - start + 1.",
            "Use sequence[start - 1:end] and check end - start + 1.",
            "Brug sequence[start - 1:end] og kontrollér end - start + 1.",
        ),
        (
            "La conversión depende de la convención original.",
            "The conversion depends on the original convention.",
            "Konverteringen afhænger af den oprindelige konvention.",
        ),
        "",
    ),
    (
        "m01.p04",
        "FILL_IN_THE_BLANK",
        (
            "Completa: la hebra opuesta 5'→3' se obtiene con el ________.",
            "Complete: the opposite 5'→3' strand is obtained with the ________.",
            "Udfyld: den modsatte 5'→3'-streng findes med det ________.",
        ),
        (("Requiere dos operaciones.", "It requires two operations.", "Det kræver to operationer."),),
        ("complemento inverso", "reverse complement", "omvendte komplement"),
        (
            "Complementar sin invertir no basta.",
            "Complementing without reversing is insufficient.",
            "Komplementering uden vending er utilstrækkelig.",
        ),
        "",
    ),
    (
        "m01.p05",
        "CODE_COMPLETION",
        (
            "Completa una validación de ADN con A/C/G/T/N.",
            "Complete DNA validation for A/C/G/T/N.",
            "Færdiggør DNA-validering for A/C/G/T/N.",
        ),
        (("Normaliza antes de validar.", "Normalize before validation.", "Normalisér før validering."),),
        (
            "def validate_dna(sequence):\n    normalized = sequence.upper()\n    if set(normalized) - set('ACGTN'):\n        raise ValueError('unsupported symbol')\n    return normalized",
            "def validate_dna(sequence):\n    normalized = sequence.upper()\n    if set(normalized) - set('ACGTN'):\n        raise ValueError('unsupported symbol')\n    return normalized",
            "def validate_dna(sequence):\n    normalized = sequence.upper()\n    if set(normalized) - set('ACGTN'):\n        raise ValueError('unsupported symbol')\n    return normalized",
        ),
        (
            "La función declara un alfabeto restringido.",
            "The function declares a restricted alphabet.",
            "Funktionen deklarerer et begrænset alfabet.",
        ),
        "def validate_dna(sequence: str) -> str:\n    normalized = sequence.upper()\n    # Validate here.\n    return normalized\n",
    ),
    (
        "m01.p06",
        "DATA_INTERPRETATION",
        (
            "Una región tiene 80 % GC pero sólo cinco bases conocidas. Interpreta.",
            "A region has 80% GC but only five known bases. Interpret it.",
            "En region har 80 % GC men kun fem kendte baser. Fortolk den.",
        ),
        (("Considera tamaño y ambigüedad.", "Consider size and ambiguity.", "Overvej størrelse og tvetydighed."),),
        (
            "La estimación es inestable; deben informarse el denominador, la política de ambigüedad y una referencia adecuada.",
            "The estimate is unstable; report the denominator, ambiguity policy, and a suitable reference.",
            "Estimatet er ustabilt; rapportér nævneren, tvetydighedspolitikken og en passende reference.",
        ),
        (
            "Un porcentaje sin tamaño puede inducir a error.",
            "A percentage without size can mislead.",
            "En procent uden størrelse kan vildlede.",
        ),
        "",
    ),
    (
        "m01.p07",
        "ORDERING",
        (
            "Ordena: pregunta, representación, validación de entrada, algoritmo, validación de salida, interpretación.",
            "Order: question, representation, input validation, algorithm, output validation, interpretation.",
            "Ordén: spørgsmål, repræsentation, inputvalidering, algoritme, outputvalidering, fortolkning.",
        ),
        (("La interpretación sigue a la verificación.", "Interpretation follows verification.", "Fortolkning følger verifikation."),),
        (
            "Pregunta → representación → validación de entrada → algoritmo → validación de salida → interpretación.",
            "Question → representation → input validation → algorithm → output validation → interpretation.",
            "Spørgsmål → repræsentation → inputvalidering → algoritme → outputvalidering → fortolkning.",
        ),
        (
            "Cada etapa debe ser identificable aunque el flujo itere.",
            "Each stage should remain identifiable even when the workflow iterates.",
            "Hvert trin bør kunne identificeres selv når workflowet itererer.",
        ),
        "",
    ),
    (
        "m01.p08",
        "PIPELINE_DESIGN",
        (
            "Diseña un flujo para buscar un motivo en ambas hebras.",
            "Design a workflow for searching a motif on both strands.",
            "Design et workflow til motivsøgning på begge strenge.",
        ),
        (("Incluye hebra y validación sintética.", "Include strand and synthetic validation.", "Medtag streng og syntetisk validering."),),
        (
            "Registrar fuente → validar alfabeto → normalizar → buscar motivo directo y complemento inverso → guardar posición y hebra → probar casos pequeños → resumir.",
            "Record source → validate alphabet → normalize → search motif and reverse complement → store position and strand → test small cases → summarize.",
            "Registrér kilde → validér alfabet → normalisér → søg motiv og omvendt komplement → gem position og streng → test små tilfælde → opsummér.",
        ),
        (
            "Contar ambas hebras sin orientación confunde resultados.",
            "Counting both strands without orientation confuses results.",
            "Optælling af begge strenge uden orientering forvirrer resultater.",
        ),
        "",
    ),
)

LOCALIZED_MODULE_01_MOLECULAR_INFORMATION = LocalizedLearningModule(
    course_code="DM847",
    module_id="dm847.m01",
    title=t(
        "Información molecular y representaciones computables",
        "Molecular information and computable representations",
        "Molekylær information og beregnelige repræsentationer",
    ),
    summary=t(
        "Fundamentos para representar secuencias, hebras, coordenadas y contexto regulador sin perder significado biológico.",
        "Foundations for representing sequences, strands, coordinates, and regulatory context without losing biological meaning.",
        "Grundlag for repræsentation af sekvenser, strenge, koordinater og regulatorisk kontekst uden at miste biologisk betydning.",
    ),
    objectives=tuple(objective(item_id, text) for item_id, text in _OBJECTIVES),
    concepts=tuple(
        concept(concept_id, title, body, key_points)
        for concept_id, title, body, key_points in _CONCEPTS
    ),
    worked_examples=tuple(
        example(example_id, title, problem, reasoning, code, expected_output, explanation)
        for example_id, title, problem, reasoning, code, expected_output, explanation in _EXAMPLES
    ),
    practice_exercises=tuple(
        practice(
            exercise_id,
            ActivityType[activity_type],
            prompt,
            hints,
            solution,
            explanation,
            starter_code,
        )
        for exercise_id, activity_type, prompt, hints, solution, explanation, starter_code in _PRACTICES
    ),
    assessment_items=(
        authored_item(
            "dm847.m01.assessment.001",
            ActivityType.MULTIPLE_CHOICE,
            (
                "¿Qué metadato es esencial en una búsqueda de motivos?",
                "Which metadata is essential in a motif search?",
                "Hvilke metadata er nødvendige i en motivsøgning?",
            ),
            (),
            (
                "La hebra determina la orientación buscada.",
                "Strand determines the searched orientation.",
                "Streng bestemmer den søgte orientering.",
            ),
            options=(
                ("strand", ("Hebra", "Strand", "Streng")),
                ("font", ("Fuente tipográfica", "Font", "Skrifttype")),
                ("screen", ("Pantalla", "Screen", "Skærm")),
            ),
            correct_option_ids=("strand",),
        ),
        authored_item(
            "dm847.m01.assessment.002",
            ActivityType.MULTIPLE_SELECT,
            (
                "Selecciona elementos de un contrato de secuencia.",
                "Select elements of a sequence contract.",
                "Vælg elementer i en sekvenskontrakt.",
            ),
            (),
            (
                "Alfabeto, hebra, coordenadas y procedencia condicionan las operaciones.",
                "Alphabet, strand, coordinates, and provenance condition operations.",
                "Alfabet, streng, koordinater og proveniens betinger operationer.",
            ),
            options=(
                ("alphabet", ("Alfabeto", "Alphabet", "Alfabet")),
                ("strand", ("Hebra", "Strand", "Streng")),
                ("coordinates", ("Coordenadas", "Coordinates", "Koordinater")),
                ("provenance", ("Procedencia", "Provenance", "Proveniens")),
                ("theme", ("Tema visual", "Visual theme", "Visuelt tema")),
            ),
            correct_option_ids=("alphabet", "strand", "coordinates", "provenance"),
        ),
        authored_item(
            "dm847.m01.assessment.003",
            ActivityType.TRUE_FALSE,
            (
                "Complementar sin invertir produce el complemento inverso.",
                "Complementing without reversing produces the reverse complement.",
                "Komplementering uden vending giver det omvendte komplement.",
            ),
            (),
            (
                "El complemento inverso requiere ambas operaciones.",
                "The reverse complement requires both operations.",
                "Det omvendte komplement kræver begge operationer.",
            ),
            options=(
                ("true", ("Verdadero", "True", "Sandt")),
                ("false", ("Falso", "False", "Falsk")),
            ),
            correct_option_ids=("false",),
        ),
        authored_item(
            "dm847.m01.assessment.004",
            ActivityType.FILL_IN_THE_BLANK,
            (
                "Convierte el intervalo 1-based inclusivo 4–7 a un corte Python.",
                "Convert the 1-based inclusive interval 4–7 to a Python slice.",
                "Konvertér det 1-baserede inklusive interval 4–7 til et Python-slice.",
            ),
            (("sequence[3:7]", "sequence[3:7]", "sequence[3:7]"),),
            (
                "Se resta uno al inicio y se mantiene el final.",
                "Subtract one from start and keep end.",
                "Træk én fra start og behold slut.",
            ),
        ),
        authored_item(
            "dm847.m01.assessment.005",
            ActivityType.ORDERING,
            (
                "Ordena el complemento inverso.",
                "Order the reverse-complement workflow.",
                "Ordén workflowet for omvendt komplement.",
            ),
            (),
            (
                "Normalizar → validar → complementar → invertir.",
                "Normalize → validate → complement → reverse.",
                "Normalisér → validér → komplementér → vend.",
            ),
            options=(
                ("normalize", ("Normalizar", "Normalize", "Normalisér")),
                ("validate", ("Validar", "Validate", "Validér")),
                ("complement", ("Complementar", "Complement", "Komplementér")),
                ("reverse", ("Invertir", "Reverse", "Vend")),
            ),
            correct_option_ids=("normalize", "validate", "complement", "reverse"),
        ),
        authored_item(
            "dm847.m01.assessment.006",
            ActivityType.CODE_TRACING,
            (
                "Traza el complemento inverso de ATGC.",
                "Trace the reverse complement of ATGC.",
                "Gennemgå det omvendte komplement af ATGC.",
            ),
            (("GCAT", "GCAT", "GCAT"),),
            (
                "ATGC se complementa a TACG y se invierte a GCAT.",
                "ATGC complements to TACG and reverses to GCAT.",
                "ATGC komplementeres til TACG og vendes til GCAT.",
            ),
        ),
        authored_item(
            "dm847.m01.assessment.007",
            ActivityType.DEBUGGING,
            (
                "Una función calcula GC con N en el denominador sin declararlo. Corrige el contrato.",
                "A function includes N in the GC denominator without declaring it. Fix the contract.",
                "En funktion medtager N i GC-nævneren uden at deklarere det. Ret kontrakten.",
            ),
            (
                (
                    "Definir si N se excluye o invalida el cálculo, aplicar la política y devolver el denominador.",
                    "Define whether N is excluded or invalidates the calculation, apply the policy, and return the denominator.",
                    "Definér om N udelukkes eller ugyldiggør beregningen, anvend politikken og returnér nævneren.",
                ),
            ),
            (
                "La fórmula necesita una política de ambigüedad.",
                "The formula needs an ambiguity policy.",
                "Formlen kræver en tvetydighedspolitik.",
            ),
        ),
        authored_item(
            "dm847.m01.assessment.008",
            ActivityType.DATA_INTERPRETATION,
            (
                "Dos muestras comparten secuencia, pero difieren en accesibilidad de cromatina. Interpreta.",
                "Two samples share sequence but differ in chromatin accessibility. Interpret.",
                "To prøver deler sekvens men adskiller sig i kromatintilgængelighed. Fortolk.",
            ),
            (
                (
                    "La diferencia pertenece a la capa reguladora y a la condición, no a la cadena de bases.",
                    "The difference belongs to the regulatory layer and condition, not the base string.",
                    "Forskellen hører til det regulatoriske lag og betingelsen, ikke basestrengen.",
                ),
            ),
            (
                "Deben considerarse ensayo, calidad y replicación.",
                "Assay, quality, and replication should be considered.",
                "Assay, kvalitet og replikation bør overvejes.",
            ),
        ),
        authored_item(
            "dm847.m01.assessment.009",
            ActivityType.PIPELINE_DESIGN,
            (
                "Diseña un flujo reproducible para extraer regiones anotadas.",
                "Design a reproducible workflow for extracting annotated regions.",
                "Design et reproducerbart workflow til udtræk af annoterede regioner.",
            ),
            (
                (
                    "Registrar versiones → validar referencias y coordenadas → convertir → extraer → comprobar longitud y hebra → guardar procedencia.",
                    "Record versions → validate references and coordinates → convert → extract → check length and strand → save provenance.",
                    "Registrér versioner → validér referencer og koordinater → konvertér → udtræk → kontrollér længde og streng → gem proveniens.",
                ),
            ),
            (
                "La referencia y la anotación deben corresponder a la misma versión.",
                "Reference and annotation should correspond to the same version.",
                "Reference og annotation bør svare til samme version.",
            ),
            rubric=(
                ("Declara convenciones.", "States conventions.", "Angiver konventioner."),
                ("Incluye validaciones.", "Includes validation.", "Medtager validering."),
            ),
        ),
        authored_item(
            "dm847.m01.assessment.010",
            ActivityType.ORAL_EXPLANATION,
            (
                "Explica por qué una cadena de ADN no equivale automáticamente a una proteína.",
                "Explain why a DNA string does not automatically equal a protein.",
                "Forklar hvorfor en DNA-streng ikke automatisk svarer til et protein.",
            ),
            (
                (
                    "Se requieren región transcrita, hebra, transcrito, marco de lectura, código genético y contexto.",
                    "A transcribed region, strand, transcript, reading frame, genetic code, and context are required.",
                    "Der kræves transkriberet region, streng, transkript, læseramme, genetisk kode og kontekst.",
                ),
            ),
            (
                "La traducción es una transformación condicionada.",
                "Translation is a conditional transformation.",
                "Translation er en betinget transformation.",
            ),
        ),
    ),
    tutor_support=tutor_support(
        (
            "Este módulo establece el contrato conceptual para convertir información molecular en objetos computables sin perder significado biológico. El dogma central conecta ADN, ARN y proteína, pero cada transformación depende de región, hebra, marco, código genético y contexto. Una cadena debe acompañarse de alfabeto, identidad, orientación y procedencia. Los símbolos IUPAC representan ambigüedad y su tratamiento debe elegirse según la operación. El complemento inverso combina emparejamiento de bases e inversión para expresar la hebra opuesta 5'→3'. Las coordenadas son otro contrato crítico: muchos formatos usan 1-based inclusivo, mientras Python usa 0-based y final exclusivo. La conversión segura conserva longitud y valida límites. La secuencia no contiene toda la actividad biológica; anotación, señal experimental, tipo celular, estado y ensayo son capas distintas. Una asociación entre señal reguladora y expresión no demuestra por sí sola causalidad. Un flujo bioinformático responsable parte de una pregunta delimitada, define unidad de análisis y representación, valida entradas, ejecuta una operación, valida salidas y vuelve al contexto con incertidumbre y limitaciones. Los ejemplos son ejercicios didácticos de bioinformática y programación; no representan protocolos de laboratorio, criterios diagnósticos ni recomendaciones clínicas.",
            "This module establishes the conceptual contract for converting molecular information into computable objects without losing biological meaning. The central dogma connects DNA, RNA, and protein, but each transformation depends on region, strand, frame, genetic code, and context. A string should carry an alphabet, identity, orientation, and provenance. IUPAC symbols represent ambiguity, and their treatment should match the operation. The reverse complement combines base pairing and reversal to express the opposite strand in 5'→3'. Coordinates are another critical contract: many formats use 1-based inclusive coordinates, while Python uses 0-based indexes and an exclusive end. Safe conversion preserves length and validates boundaries. Sequence does not contain all biological activity; annotation, experimental signal, cell type, state, and assay are distinct layers. An association between regulatory signal and expression does not establish causality by itself. A responsible bioinformatics workflow begins with a bounded question, defines the unit of analysis and representation, validates inputs, runs an operation, validates outputs, and returns to context with uncertainty and limitations. The examples are teaching exercises in bioinformatics and programming; they are not laboratory protocols, diagnostic criteria, or clinical recommendations.",
            "Dette modul fastlægger den konceptuelle kontrakt for at omsætte molekylær information til beregnelige objekter uden at miste biologisk betydning. Det centrale dogme forbinder DNA, RNA og protein, men hver transformation afhænger af region, streng, læseramme, genetisk kode og kontekst. En streng bør ledsages af alfabet, identitet, orientering og proveniens. IUPAC-symboler repræsenterer tvetydighed, og behandlingen bør passe til operationen. Det omvendte komplement kombinerer baseparring og vending for at udtrykke den modsatte streng i 5'→3'. Koordinater er en anden kritisk kontrakt: mange formater bruger 1-baserede inklusive koordinater, mens Python bruger 0-baserede indeks og eksklusiv slutgrænse. Sikker konvertering bevarer længden og validerer grænser. Sekvens indeholder ikke al biologisk aktivitet; annotation, eksperimentelt signal, celletype, tilstand og assay er forskellige lag. En association mellem regulatorisk signal og ekspression viser ikke alene kausalitet. Et ansvarligt bioinformatikworkflow starter med et afgrænset spørgsmål, definerer analyseenhed og repræsentation, validerer input, udfører en operation, validerer output og vender tilbage til konteksten med usikkerhed og begrænsninger. Eksemplerne er undervisningsøvelser i bioinformatik og programmering; de er ikke laboratorieprotokoller, diagnostiske kriterier eller kliniske anbefalinger.",
        ),
        (
            (
                "El dogma central describe relaciones, no conversiones automáticas.",
                "The central dogma describes relationships, not automatic conversions.",
                "Det centrale dogme beskriver relationer, ikke automatiske konverteringer.",
            ),
            (
                "Alfabeto, hebra y procedencia forman parte del dato.",
                "Alphabet, strand, and provenance are part of the data.",
                "Alfabet, streng og proveniens er en del af data.",
            ),
            (
                "El complemento inverso requiere complementar e invertir.",
                "The reverse complement requires complementing and reversing.",
                "Det omvendte komplement kræver komplementering og vending.",
            ),
            (
                "Las coordenadas requieren una convención declarada.",
                "Coordinates require a declared convention.",
                "Koordinater kræver en deklareret konvention.",
            ),
            (
                "La longitud valida conversiones de intervalos.",
                "Length validates interval conversions.",
                "Længde validerer intervalkonverteringer.",
            ),
            (
                "Secuencia, anotación, señal y condición son capas distintas.",
                "Sequence, annotation, signal, and condition are distinct layers.",
                "Sekvens, annotation, signal og betingelse er forskellige lag.",
            ),
            (
                "Correlación reguladora no demuestra causalidad.",
                "Regulatory correlation does not establish causality.",
                "Regulatorisk korrelation viser ikke kausalitet.",
            ),
            (
                "Toda pregunta necesita unidad de análisis y validación.",
                "Every question needs a unit of analysis and validation.",
                "Hvert spørgsmål kræver analyseenhed og validering.",
            ),
        ),
        (
            (
                "Creer que cualquier ADN representa un gen completo.",
                "Believing any DNA represents a complete gene.",
                "At tro at enhver DNA-sekvens repræsenterer et komplet gen.",
            ),
            (
                "Usar complemento y complemento inverso como sinónimos.",
                "Using complement and reverse complement as synonyms.",
                "At bruge komplement og omvendt komplement som synonymer.",
            ),
            (
                "Tratar N como una quinta base concreta.",
                "Treating N as a concrete fifth base.",
                "At behandle N som en konkret femte base.",
            ),
            (
                "Aplicar cortes Python directamente a coordenadas 1-based.",
                "Applying Python slices directly to 1-based coordinates.",
                "At anvende Python-slices direkte på 1-baserede koordinater.",
            ),
            (
                "Confundir señal epigenética con cambio de secuencia.",
                "Confusing epigenetic signal with sequence change.",
                "At forveksle epigenetisk signal med sekvensændring.",
            ),
            (
                "Interpretar una salida sin referencia ni contexto.",
                "Interpreting an output without reference or context.",
                "At fortolke et output uden reference eller kontekst.",
            ),
        ),
        (
            (
                "¿Qué entidad representa esta cadena?",
                "What entity does this string represent?",
                "Hvilken enhed repræsenterer denne streng?",
            ),
            (
                "¿Qué alfabeto y ambigüedad se permiten?",
                "Which alphabet and ambiguity are allowed?",
                "Hvilket alfabet og hvilken tvetydighed tillades?",
            ),
            (
                "¿En qué orientación está la secuencia?",
                "In which orientation is the sequence?",
                "I hvilken orientering er sekvensen?",
            ),
            (
                "¿Qué convención de coordenadas usa la fuente?",
                "Which coordinate convention does the source use?",
                "Hvilken koordinatkonvention bruger kilden?",
            ),
            (
                "¿Qué capa corresponde a la observación?",
                "Which layer does the observation belong to?",
                "Hvilket lag tilhører observationen?",
            ),
            (
                "¿Cómo validarías el resultado con un caso pequeño?",
                "How would you validate the result with a small case?",
                "Hvordan ville du validere resultatet med et lille tilfælde?",
            ),
        ),
        (
            (
                "Explicar primero la entidad y luego la representación.",
                "Explain the entity before the representation.",
                "Forklar enheden før repræsentationen.",
            ),
            (
                "Declarar alfabeto, hebra y coordenadas.",
                "State alphabet, strand, and coordinates.",
                "Angiv alfabet, streng og koordinater.",
            ),
            (
                "Justificar la política de ambigüedad.",
                "Justify the ambiguity policy.",
                "Begrund tvetydighedspolitikken.",
            ),
            (
                "Verificar límites y longitud.",
                "Verify boundaries and length.",
                "Kontrollér grænser og længde.",
            ),
            (
                "Separar secuencia, señal y condición.",
                "Separate sequence, signal, and condition.",
                "Adskil sekvens, signal og betingelse.",
            ),
            (
                "Interpretar con referencia e incertidumbre.",
                "Interpret with reference and uncertainty.",
                "Fortolk med reference og usikkerhed.",
            ),
        ),
        (
            (
                "No inventar coordenadas, versiones o hebras ausentes.",
                "Do not invent missing coordinates, versions, or strands.",
                "Opfind ikke manglende koordinater, versioner eller strenge.",
            ),
            (
                "No confundir una cadena con una entidad completa.",
                "Do not confuse a string with a complete entity.",
                "Forveksl ikke en streng med en komplet enhed.",
            ),
            (
                "No presentar correlación como causalidad demostrada.",
                "Do not present correlation as demonstrated causality.",
                "Præsenter ikke korrelation som bevist kausalitet.",
            ),
            (
                "No ocultar el tratamiento de símbolos ambiguos.",
                "Do not hide the treatment of ambiguous symbols.",
                "Skjul ikke behandlingen af tvetydige symboler.",
            ),
            (
                "Distinguir ejercicios didácticos de protocolos experimentales.",
                "Distinguish teaching exercises from experimental protocols.",
                "Skeln mellem undervisningsøvelser og eksperimentelle protokoller.",
            ),
            (
                "Responder en el idioma activo con términos técnicos precisos.",
                "Answer in the active language with precise technical terms.",
                "Svar på det aktive sprog med præcise tekniske termer.",
            ),
        ),
        (
            "SDU DM847 active course description and expected learning outcomes.",
            "NCBI Bookshelf resources on molecular information and sequence representation.",
            "NCBI GenBank and RefSeq documentation on identifiers and versions.",
            "IUPAC nucleotide ambiguity code conventions.",
            "Sequence Ontology terminology for biological sequence features.",
        ),
    ),
)

_BANK_MCQS = (
    (
        "001",
        (
            "¿Qué diferencia al ADN del ARN en el alfabeto canónico?",
            "What distinguishes DNA from RNA in the canonical alphabet?",
            "Hvad adskiller DNA fra RNA i det kanoniske alfabet?",
        ),
        (
            ("tu", ("ADN usa T y ARN usa U", "DNA uses T and RNA uses U", "DNA bruger T og RNA bruger U")),
            ("nog", ("ADN no contiene G", "DNA contains no G", "DNA indeholder ikke G")),
            ("noc", ("ARN no contiene C", "RNA contains no C", "RNA indeholder ikke C")),
        ),
        "tu",
        (
            "La diferencia canónica es T frente a U.",
            "The canonical difference is T versus U.",
            "Den kanoniske forskel er T mod U.",
        ),
    ),
    (
        "002",
        (
            "¿Qué representa N en IUPAC?",
            "What does N represent in IUPAC?",
            "Hvad repræsenterer N i IUPAC?",
        ),
        (
            ("any", ("Cualquier base", "Any base", "Enhver base")),
            ("none", ("Ninguna base", "No base", "Ingen base")),
            ("stop", ("Parada", "Stop", "Stop")),
        ),
        "any",
        (
            "N representa una base no determinada.",
            "N represents an undetermined base.",
            "N repræsenterer en ubestemt base.",
        ),
    ),
    (
        "003",
        (
            "¿Qué produce la hebra opuesta 5'→3'?",
            "What produces the opposite 5'→3' strand?",
            "Hvad giver den modsatte 5'→3'-streng?",
        ),
        (
            ("rc", ("Complemento inverso", "Reverse complement", "Omvendt komplement")),
            ("sort", ("Ordenación", "Sorting", "Sortering")),
            ("upper", ("Mayúsculas", "Uppercase", "Store bogstaver")),
        ),
        "rc",
        (
            "Se complementan bases y se invierte el orden.",
            "Bases are complemented and order is reversed.",
            "Baser komplementeres og rækkefølgen vendes.",
        ),
    ),
    (
        "004",
        (
            "¿Cuál es el corte para 1-based inclusivo 2–5?",
            "What is the slice for 1-based inclusive 2–5?",
            "Hvad er slicet for 1-baseret inklusiv 2–5?",
        ),
        (
            ("correct", ("sequence[1:5]", "sequence[1:5]", "sequence[1:5]")),
            ("late", ("sequence[2:5]", "sequence[2:5]", "sequence[2:5]")),
            ("short", ("sequence[1:4]", "sequence[1:4]", "sequence[1:4]")),
        ),
        "correct",
        (
            "Se resta uno al inicio.",
            "Subtract one from start.",
            "Træk én fra start.",
        ),
    ),
    (
        "005",
        (
            "¿Qué invariante detecta errores de coordenadas?",
            "Which invariant detects coordinate errors?",
            "Hvilken invariant opdager koordinatfejl?",
        ),
        (
            ("length", ("Longitud", "Length", "Længde")),
            ("color", ("Color", "Color", "Farve")),
            ("font", ("Fuente", "Font", "Skrifttype")),
        ),
        "length",
        (
            "La longitud debe conservar la definición del intervalo.",
            "Length should preserve the interval definition.",
            "Længden bør bevare intervaldefinitionen.",
        ),
    ),
    (
        "006",
        (
            "¿Qué capa describe un exón?",
            "Which layer describes an exon?",
            "Hvilket lag beskriver et ekson?",
        ),
        (
            ("annotation", ("Anotación", "Annotation", "Annotation")),
            ("signal", ("Señal", "Signal", "Signal")),
            ("condition", ("Condición", "Condition", "Betingelse")),
        ),
        "annotation",
        (
            "Un exón es una característica anotada.",
            "An exon is an annotated feature.",
            "Et ekson er et annoteret træk.",
        ),
    ),
    (
        "007",
        (
            "¿Qué capa incluye accesibilidad de cromatina medida?",
            "Which layer includes measured chromatin accessibility?",
            "Hvilket lag omfatter målt kromatintilgængelighed?",
        ),
        (
            ("signal", ("Señal experimental", "Experimental signal", "Eksperimentelt signal")),
            ("sequence", ("Secuencia", "Sequence", "Sekvens")),
            ("font", ("Tipografía", "Typography", "Typografi")),
        ),
        "signal",
        (
            "La accesibilidad es una medición dependiente de muestra y ensayo.",
            "Accessibility is a sample- and assay-dependent measurement.",
            "Tilgængelighed er en prøve- og assayafhængig måling.",
        ),
    ),
    (
        "008",
        (
            "¿Qué formaliza una pregunta bioinformática?",
            "What formalizes a bioinformatics question?",
            "Hvad formaliserer et bioinformatikspørgsmål?",
        ),
        (
            ("contract", ("Representación, operación y validación", "Representation, operation, and validation", "Repræsentation, operation og validering")),
            ("more", ("Más datos sin definición", "More undefined data", "Flere udefinerede data")),
            ("plot", ("Una figura aislada", "An isolated plot", "En isoleret figur")),
        ),
        "contract",
        (
            "Esos elementos convierten la pregunta en un problema computable.",
            "Those elements turn the question into a computable problem.",
            "Disse elementer omsætter spørgsmålet til et beregneligt problem.",
        ),
    ),
    (
        "009",
        (
            "¿Qué debe definirse antes de calcular GC?",
            "What should be defined before computing GC?",
            "Hvad bør defineres før beregning af GC?",
        ),
        (
            ("ambiguity", ("Política de ambigüedad", "Ambiguity policy", "Tvetydighedspolitik")),
            ("theme", ("Tema visual", "Visual theme", "Visuelt tema")),
            ("mouse", ("Ratón", "Mouse", "Mus")),
        ),
        "ambiguity",
        (
            "El tratamiento de N cambia el denominador.",
            "Handling N changes the denominator.",
            "Behandling af N ændrer nævneren.",
        ),
    ),
    (
        "010",
        (
            "¿Qué orientación se usa normalmente al escribir secuencias?",
            "Which orientation is normally used when writing sequences?",
            "Hvilken orientering bruges normalt ved skrivning af sekvenser?",
        ),
        (
            ("five", ("5'→3'", "5'→3'", "5'→3'")),
            ("three", ("Sólo 3'→5'", "Only 3'→5'", "Kun 3'→5'")),
            ("none", ("Sin orientación", "No orientation", "Ingen orientering")),
        ),
        "five",
        (
            "La convención habitual es 5'→3'.",
            "The usual convention is 5'→3'.",
            "Den sædvanlige konvention er 5'→3'.",
        ),
    ),
)

_BANK_TFS = (
    (
        "011",
        (
            "Una cadena de ADN es siempre un gen completo.",
            "A DNA string is always a complete gene.",
            "En DNA-streng er altid et komplet gen.",
        ),
        False,
        (
            "Puede representar cualquier región y requiere anotación.",
            "It may represent any region and requires annotation.",
            "Den kan repræsentere enhver region og kræver annotation.",
        ),
    ),
    (
        "012",
        (
            "El complemento inverso combina complementación e inversión.",
            "A reverse complement combines complementation and reversal.",
            "Et omvendt komplement kombinerer komplementering og vending.",
        ),
        True,
        (
            "Ambas operaciones son necesarias.",
            "Both operations are required.",
            "Begge operationer er nødvendige.",
        ),
    ),
    (
        "013",
        (
            "Los cortes Python usan final exclusivo.",
            "Python slices use an exclusive end.",
            "Python-slices bruger en eksklusiv slutgrænse.",
        ),
        True,
        (
            "La posición final no se incluye.",
            "The end position is not included.",
            "Slutpositionen medtages ikke.",
        ),
    ),
    (
        "014",
        (
            "Todas las fuentes biológicas usan coordenadas 0-based.",
            "All biological sources use 0-based coordinates.",
            "Alle biologiske kilder bruger 0-baserede koordinater.",
        ),
        False,
        (
            "Las convenciones varían entre formatos.",
            "Conventions vary across formats.",
            "Konventioner varierer mellem formater.",
        ),
    ),
    (
        "015",
        (
            "Una marca epigenética cambia necesariamente las letras del ADN.",
            "An epigenetic mark necessarily changes DNA letters.",
            "Et epigenetisk mærke ændrer nødvendigvis DNA-bogstaverne.",
        ),
        False,
        (
            "Normalmente es una observación asociada a posición, muestra y ensayo.",
            "It is usually an observation associated with position, sample, and assay.",
            "Det er normalt en observation knyttet til position, prøve og assay.",
        ),
    ),
    (
        "016",
        (
            "Secuencia y señal experimental son la misma capa.",
            "Sequence and experimental signal are the same layer.",
            "Sekvens og eksperimentelt signal er samme lag.",
        ),
        False,
        (
            "Tienen semántica, unidades y procedencia distintas.",
            "They have different semantics, units, and provenance.",
            "De har forskellig semantik, enheder og proveniens.",
        ),
    ),
    (
        "017",
        (
            "Una fracción GC debería informar su denominador.",
            "A GC fraction should report its denominator.",
            "En GC-andel bør rapportere sin nævner.",
        ),
        True,
        (
            "El denominador muestra cuántas bases aportaron información.",
            "The denominator shows how many bases contributed information.",
            "Nævneren viser hvor mange baser der bidrog med information.",
        ),
    ),
    (
        "018",
        (
            "Los casos pequeños pueden detectar errores sistemáticos.",
            "Small cases can detect systematic errors.",
            "Små tilfælde kan opdage systematiske fejl.",
        ),
        True,
        (
            "Hacen visibles coordenadas, orientación y conteos.",
            "They expose coordinates, orientation, and counts.",
            "De synliggør koordinater, orientering og optællinger.",
        ),
    ),
    (
        "019",
        (
            "La unidad de análisis debe definirse antes de interpretar.",
            "The unit of analysis should be defined before interpretation.",
            "Analyseenheden bør defineres før fortolkning.",
        ),
        True,
        (
            "Determina qué observaciones se comparan.",
            "It determines which observations are compared.",
            "Den bestemmer hvilke observationer der sammenlignes.",
        ),
    ),
    (
        "020",
        (
            "Los ejemplos del módulo sustituyen protocolos de laboratorio.",
            "The module examples replace laboratory protocols.",
            "Modulets eksempler erstatter laboratorieprotokoller.",
        ),
        False,
        (
            "Son ejercicios didácticos de representación y programación.",
            "They are teaching exercises in representation and programming.",
            "De er undervisningsøvelser i repræsentation og programmering.",
        ),
    ),
)

LOCALIZED_OBJECTIVE_QUESTION_BANK_01 = tuple(
    objective_mcq(
        f"dm847.m01.bank.{item_id}",
        prompt,
        options,
        correct_option_id,
        explanation,
    )
    for item_id, prompt, options, correct_option_id, explanation in _BANK_MCQS
) + tuple(
    objective_tf(
        f"dm847.m01.bank.{item_id}",
        prompt,
        correct=correct,
        explanation=explanation,
    )
    for item_id, prompt, correct, explanation in _BANK_TFS
)


def materialize_module_01_question_bank(
    locale: AppLocale | str = AppLocale.SPANISH_SPAIN,
) -> tuple[AssessmentItem, ...]:
    """Materialize the objective bank in one supported locale."""
    resolved = locale if isinstance(locale, AppLocale) else AppLocale.resolve(locale)
    return tuple(item.materialize(resolved) for item in LOCALIZED_OBJECTIVE_QUESTION_BANK_01)


MODULE_01_MOLECULAR_INFORMATION: LearningModule = (
    LOCALIZED_MODULE_01_MOLECULAR_INFORMATION.materialize(AppLocale.SPANISH_SPAIN)
)
OBJECTIVE_QUESTION_BANK_01 = materialize_module_01_question_bank()

__all__ = [
    "LOCALIZED_MODULE_01_MOLECULAR_INFORMATION",
    "LOCALIZED_OBJECTIVE_QUESTION_BANK_01",
    "MODULE_01_MOLECULAR_INFORMATION",
    "OBJECTIVE_QUESTION_BANK_01",
    "materialize_module_01_question_bank",
]
