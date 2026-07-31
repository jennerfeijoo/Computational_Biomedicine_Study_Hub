"""BMB830 module 1: R foundations and reproducible biological-data workflows."""

from __future__ import annotations

from ...i18n import AppLocale
from ..models import AssessmentItem, LearningModule
from .standard import StandardModuleSpec, build_module, build_question_bank, materialize_bank

_SPEC = StandardModuleSpec(
    module_id="bmb830.m01",
    title=(
        "Fundamentos de R y flujo reproducible",
        "R foundations and reproducible workflow",
        "Grundlæggende R og reproducerbart workflow",
    ),
    summary=(
        "Representa datos biológicos con tipos adecuados, valida claves y ausencia, y construye scripts que puedan ejecutarse desde una sesión limpia.",
        "Represent biological data with appropriate types, validate keys and missingness, and build scripts that run from a clean session.",
        "Repræsentér biologiske data med passende typer, validér nøgler og manglende data, og byg scripts der kan køres fra en ren session.",
    ),
    objectives=(
        (
            "m01.o1",
            (
                "Distinguir vectores, factores, matrices, listas y data frames.",
                "Distinguish vectors, factors, matrices, lists, and data frames.",
                "Skelne mellem vektorer, faktorer, matricer, lister og data frames.",
            ),
        ),
        (
            "m01.o2",
            (
                "Representar identificadores, categorías, medidas y valores ausentes de forma explícita.",
                "Represent identifiers, categories, measurements, and missing values explicitly.",
                "Repræsentere identifikatorer, kategorier, målinger og manglende værdier eksplicit.",
            ),
        ),
        (
            "m01.o3",
            (
                "Separar entrada, validación, transformación, análisis y salida en un script reproducible.",
                "Separate input, validation, transformation, analysis, and output in a reproducible script.",
                "Adskille input, validering, transformation, analyse og output i et reproducerbart script.",
            ),
        ),
        (
            "m01.o4",
            (
                "Interpretar errores, advertencias y aserciones como evidencia sobre la validez del análisis.",
                "Interpret errors, warnings, and assertions as evidence about analytical validity.",
                "Fortolke fejl, advarsler og assertions som evidens for analysens gyldighed.",
            ),
        ),
    ),
    concepts=(
        (
            "r-objects",
            ("Objetos y tipos", "Objects and types", "Objekter og typer"),
            (
                "Los vectores atómicos son homogéneos; los factores representan categorías; las matrices son bidimensionales y homogéneas; las listas combinan tipos; y los data frames organizan variables heterogéneas por columnas.",
                "Atomic vectors are homogeneous; factors represent categories; matrices are two-dimensional and homogeneous; lists combine types; and data frames organise heterogeneous variables by columns.",
                "Atomare vektorer er homogene; faktorer repræsenterer kategorier; matricer er todimensionelle og homogene; lister kombinerer typer; og data frames organiserer heterogene variable i kolonner.",
            ),
            (
                (
                    "La estructura debe reflejar la unidad experimental.",
                    "Structure must reflect the experimental unit.",
                    "Strukturen skal afspejle den eksperimentelle enhed.",
                ),
                (
                    "Los niveles de un factor deben ser deliberados.",
                    "Factor levels should be deliberate.",
                    "Faktorniveauer bør være bevidste.",
                ),
            ),
        ),
        (
            "indexing",
            ("Indexación segura", "Safe indexing", "Sikker indeksering"),
            (
                "R permite seleccionar por posición, nombre o condición lógica. La selección debe conservar la correspondencia entre observaciones y variables; nombres estables suelen ser más robustos que posiciones cuando cambia el esquema.",
                "R supports selection by position, name, or logical condition. Selection must preserve correspondence between observations and variables; stable names are usually more robust than positions when schemas change.",
                "R understøtter valg efter position, navn eller logisk betingelse. Udvælgelse skal bevare sammenhængen mellem observationer og variable; stabile navne er normalt mere robuste end positioner, når skemaer ændres.",
            ),
            (
                (
                    "Comprueba dimensiones antes y después de seleccionar.",
                    "Check dimensions before and after selection.",
                    "Kontrollér dimensioner før og efter udvælgelse.",
                ),
                (
                    "Evita reciclado silencioso de vectores.",
                    "Avoid silent vector recycling.",
                    "Undgå stille genbrug af vektorer.",
                ),
            ),
        ),
        (
            "missingness",
            ("Valores ausentes", "Missing values", "Manglende værdier"),
            (
                "NA representa información ausente y se propaga por muchas operaciones. Eliminar o ignorar NA exige cuantificar cuántas observaciones se afectan y justificar el mecanismo asumido.",
                "NA represents missing information and propagates through many operations. Removing or ignoring NA requires quantifying affected observations and justifying the assumed mechanism.",
                "NA repræsenterer manglende information og spredes gennem mange operationer. Fjernelse eller ignorering af NA kræver kvantificering af berørte observationer og begrundelse af den antagne mekanisme.",
            ),
            (
                (
                    "Diferencia cero, cadena vacía y ausencia.",
                    "Distinguish zero, an empty string, and absence.",
                    "Skeln mellem nul, en tom streng og fravær.",
                ),
                (
                    "Cuenta los NA antes de resumir.",
                    "Count NA before summarising.",
                    "Tæl NA før opsummering.",
                ),
            ),
        ),
        (
            "reproducibility",
            (
                "Flujo reproducible",
                "Reproducible workflow",
                "Reproducerbart workflow",
            ),
            (
                "Un script reproducible declara datos, parámetros y semillas, valida supuestos, evita estado oculto y produce salidas trazables. Debe reconstruir el resultado desde una sesión limpia sin comandos manuales previos.",
                "A reproducible script declares data, parameters, and seeds, validates assumptions, avoids hidden state, and produces traceable outputs. It should reconstruct results from a clean session without prior manual commands.",
                "Et reproducerbart script erklærer data, parametre og seeds, validerer antagelser, undgår skjult tilstand og producerer sporbare outputs. Det bør genskabe resultater fra en ren session uden tidligere manuelle kommandoer.",
            ),
            (
                (
                    "stopifnot convierte supuestos en condiciones verificables.",
                    "stopifnot turns assumptions into verifiable conditions.",
                    "stopifnot gør antagelser til verificerbare betingelser.",
                ),
                (
                    "El orden de ejecución forma parte del análisis.",
                    "Execution order is part of the analysis.",
                    "Køreordenen er en del af analysen.",
                ),
            ),
        ),
    ),
    examples=(
        (
            "m01.e01",
            (
                "Tabla biológica validada",
                "Validated biological table",
                "Valideret biologisk tabel",
            ),
            (
                "Construye cuatro muestras con una clave única, grupo experimental y expresión.",
                "Construct four samples with a unique key, experimental group, and expression.",
                "Konstruér fire prøver med en unik nøgle, forsøgsgruppe og ekspression.",
            ),
            (
                (
                    "El identificador define la unidad observacional.",
                    "The identifier defines the observational unit.",
                    "Identifikatoren definerer observationsenheden.",
                ),
                (
                    "El grupo se almacena como factor.",
                    "The group is stored as a factor.",
                    "Gruppen lagres som en faktor.",
                ),
            ),
            """patients <- data.frame(
  patient_id = c("P01", "P02", "P03", "P04"),
  group = factor(c("control", "treated", "control", "treated")),
  expression = c(8.2, 10.1, 7.8, 11.0)
)
stopifnot(!anyDuplicated(patients$patient_id))
cat(sprintf("rows=%d cols=%d\n", nrow(patients), ncol(patients)))
cat(paste(levels(patients$group), collapse = ","))
""",
            """rows=4 cols=3
control,treated""",
            (
                "La comprobación falla antes de analizar si la clave deja de ser única.",
                "The assertion fails before analysis if the key ceases to be unique.",
                "Assertionen fejler før analysen, hvis nøglen ikke længere er unik.",
            ),
        ),
        (
            "m01.e02",
            (
                "Resumen con ausencia explícita",
                "Summary with explicit missingness",
                "Opsummering med eksplicit mangel",
            ),
            (
                "Calcula una media sin confundir NA con cero y registra la exclusión.",
                "Calculate a mean without confusing NA with zero and record the exclusion.",
                "Beregn et gennemsnit uden at forveksle NA med nul, og registrér udelukkelsen.",
            ),
            (
                (
                    "Primero se cuantifica la ausencia.",
                    "Missingness is quantified first.",
                    "Manglende data kvantificeres først.",
                ),
                (
                    "Después se resume lo disponible.",
                    "Available values are then summarised.",
                    "Tilgængelige værdier opsummeres derefter.",
                ),
            ),
            """expression <- c(8.2, 10.1, NA, 11.0)
cat(sprintf("missing=%d\n", sum(is.na(expression))))
cat(sprintf("mean=%.2f\n", mean(expression, na.rm = TRUE)))
""",
            """missing=1
mean=9.77""",
            (
                "na.rm = TRUE es interpretable porque se informa el número de valores excluidos.",
                "na.rm = TRUE is interpretable because the number of excluded values is reported.",
                "na.rm = TRUE kan fortolkes, fordi antallet af udelukkede værdier rapporteres.",
            ),
        ),
    ),
    practices=(
        (
            "m01.p01",
            "DATA_INTERPRETATION",
            (
                "Clasifica patient_id, treatment, concentration y detected por su papel analítico.",
                "Classify patient_id, treatment, concentration, and detected by analytical role.",
                "Klassificér patient_id, treatment, concentration og detected efter analytisk rolle.",
            ),
            (
                (
                    "Piensa en operaciones válidas.",
                    "Think about valid operations.",
                    "Tænk på gyldige operationer.",
                ),
            ),
            (
                "Identificador, factor, variable numérica y variable lógica.",
                "Identifier, factor, numeric variable, and logical variable.",
                "Identifikator, faktor, numerisk variabel og logisk variabel.",
            ),
            (
                "El significado analítico determina el tipo.",
                "Analytical meaning determines type.",
                "Analytisk betydning bestemmer typen.",
            ),
            "",
        ),
        (
            "m01.p02",
            "CODE_COMPLETION",
            (
                "Completa una aserción para detectar identificadores duplicados.",
                "Complete an assertion that detects duplicated identifiers.",
                "Fuldfør en assertion, der opdager dublerede identifikatorer.",
            ),
            (
                (
                    "anyDuplicated devuelve cero si no hay duplicados.",
                    "anyDuplicated returns zero when none exist.",
                    "anyDuplicated returnerer nul, når ingen findes.",
                ),
            ),
            ("stopifnot(!anyDuplicated(samples$sample_id))",) * 3,
            (
                "La aserción protege joins y resúmenes posteriores.",
                "The assertion protects later joins and summaries.",
                "Assertionen beskytter senere joins og opsummeringer.",
            ),
            "stopifnot(______________________________)",
        ),
        (
            "m01.p03",
            "DEBUGGING",
            (
                "Explica por qué mean(c(1, 2, NA)) devuelve NA y corrígelo de forma transparente.",
                "Explain why mean(c(1, 2, NA)) returns NA and correct it transparently.",
                "Forklar hvorfor mean(c(1, 2, NA)) returnerer NA, og korrigér det transparent.",
            ),
            (("Cuenta primero los NA.", "Count NA first.", "Tæl først NA."),),
            ("sum(is.na(x)); mean(x, na.rm = TRUE)",) * 3,
            (
                "NA se propaga deliberadamente y la exclusión debe documentarse.",
                "NA propagates deliberately and exclusion must be documented.",
                "NA spredes bevidst, og udelukkelse skal dokumenteres.",
            ),
            "x <- c(1, 2, NA)",
        ),
        (
            "m01.p04",
            "PIPELINE_DESIGN",
            (
                "Ordena un análisis reproducible desde datos crudos hasta salida.",
                "Order a reproducible analysis from raw data to output.",
                "Ordér en reproducerbar analyse fra rådata til output.",
            ),
            (
                (
                    "Valida antes de modelar.",
                    "Validate before modelling.",
                    "Validér før modellering.",
                ),
            ),
            (
                "Entrada → validación → limpieza → transformación → análisis → diagnóstico → salida.",
                "Input → validation → cleaning → transformation → analysis → diagnostics → output.",
                "Input → validering → rensning → transformation → analyse → diagnostik → output.",
            ),
            (
                "El orden conserva trazabilidad.",
                "The order preserves traceability.",
                "Rækkefølgen bevarer sporbarhed.",
            ),
            "",
        ),
        (
            "m01.p05",
            "CODE_TRACING",
            (
                "Predice los niveles de factor(c('B','A','B')).",
                "Predict the levels of factor(c('B','A','B')).",
                "Forudsig niveauerne i factor(c('B','A','B')).",
            ),
            (
                (
                    "R ordena niveles por defecto.",
                    "R sorts levels by default.",
                    "R sorterer niveauer som standard.",
                ),
            ),
            (
                "Los niveles son A y B.",
                "The levels are A and B.",
                "Niveauerne er A og B.",
            ),
            (
                "El orden de niveles puede cambiar contrastes.",
                "Level order can change contrasts.",
                "Niveaurækkefølgen kan ændre kontraster.",
            ),
            "factor(c('B', 'A', 'B'))",
        ),
        (
            "m01.p06",
            "ORAL_EXPLANATION",
            (
                "Defiende por qué un script dependiente de comandos manuales no es reproducible.",
                "Defend why a script that depends on manual commands is not reproducible.",
                "Begrund hvorfor et script, der afhænger af manuelle kommandoer, ikke er reproducerbart.",
            ),
            (("Considera estado oculto.", "Consider hidden state.", "Overvej skjult tilstand."),),
            (
                "No puede reconstruirse desde entradas declaradas en una sesión limpia.",
                "It cannot be reconstructed from declared inputs in a clean session.",
                "Det kan ikke genskabes fra erklærede input i en ren session.",
            ),
            (
                "Datos, parámetros, semillas y transformaciones deben estar codificados.",
                "Data, parameters, seeds, and transformations must be encoded.",
                "Data, parametre, seeds og transformationer skal være kodet.",
            ),
            "",
        ),
    ),
    mcqs=(
        (
            "001",
            (
                "¿Qué objeto admite columnas de tipos distintos?",
                "Which object supports columns of different types?",
                "Hvilket objekt understøtter kolonner af forskellige typer?",
            ),
            (
                ("vector", ("Vector",) * 3),
                ("matrix", ("Matriz", "Matrix", "Matrix")),
                ("data_frame", ("Data frame",) * 3),
                ("factor", ("Factor", "Factor", "Faktor")),
            ),
            "data_frame",
            (
                "Un data frame conserva tipos por columna.",
                "A data frame preserves column types.",
                "Et data frame bevarer kolonnetyper.",
            ),
        ),
        (
            "002",
            (
                "¿Qué detecta una clave duplicada?",
                "What detects a duplicated key?",
                "Hvad opdager en dubleret nøgle?",
            ),
            (
                ("a", ("mean(id)",) * 3),
                ("b", ("anyDuplicated(id)",) * 3),
                ("c", ("levels(id)",) * 3),
                ("d", ("is.numeric(id)",) * 3),
            ),
            "b",
            (
                "anyDuplicated devuelve cero si no hay duplicados.",
                "anyDuplicated returns zero when none exist.",
                "anyDuplicated returnerer nul, når ingen findes.",
            ),
        ),
        (
            "003",
            ("¿Qué representa NA?", "What does NA represent?", "Hvad repræsenterer NA?"),
            (
                ("zero", ("Cero", "Zero", "Nul")),
                ("missing", ("Valor ausente", "Missing value", "Manglende værdi")),
                ("empty", ("Cadena vacía", "Empty string", "Tom streng")),
                ("false", ("Falso", "False", "Falsk")),
            ),
            "missing",
            ("NA no equivale a cero.", "NA is not zero.", "NA er ikke nul."),
        ),
        (
            "004",
            (
                "¿Qué reduce estado oculto?",
                "What reduces hidden state?",
                "Hvad reducerer skjult tilstand?",
            ),
            (
                ("manual", ("Comandos manuales", "Manual commands", "Manuelle kommandoer")),
                (
                    "script",
                    (
                        "Codificar transformaciones",
                        "Encode transformations",
                        "Kod transformationer",
                    ),
                ),
                ("workspace", ("Guardar workspace", "Save workspace", "Gem workspace")),
                ("attach", ("Usar attach", "Use attach", "Brug attach")),
            ),
            "script",
            (
                "Un script reconstruye el estado.",
                "A script reconstructs state.",
                "Et script genskaber tilstanden.",
            ),
        ),
        (
            "005",
            (
                "¿Qué objeto representa categorías?",
                "Which object represents categories?",
                "Hvilket objekt repræsenterer kategorier?",
            ),
            (
                ("factor", ("Factor", "Factor", "Faktor")),
                ("matrix", ("Matriz", "Matrix", "Matrix")),
                ("date", ("Fecha", "Date", "Dato")),
                ("numeric", ("Numérico", "Numeric", "Numerisk")),
            ),
            "factor",
            (
                "Los factores conservan niveles.",
                "Factors preserve levels.",
                "Faktorer bevarer niveauer.",
            ),
        ),
        (
            "006",
            (
                "¿Qué debe ocurrir antes de modelar?",
                "What should occur before modelling?",
                "Hvad bør ske før modellering?",
            ),
            (
                ("validate", ("Validar datos", "Validate data", "Validér data")),
                ("publish", ("Publicar", "Publish", "Publicér")),
                ("hide", ("Ocultar advertencias", "Hide warnings", "Skjul advarsler")),
                ("round", ("Redondear todo", "Round everything", "Afrund alt")),
            ),
            "validate",
            (
                "La validación detecta errores tempranos.",
                "Validation detects early errors.",
                "Validering opdager tidlige fejl.",
            ),
        ),
        (
            "007",
            (
                "¿Qué hace reproducible una simulación?",
                "What makes a simulation reproducible?",
                "Hvad gør en simulation reproducerbar?",
            ),
            (
                ("seed", ("Fijar set.seed", "Set set.seed", "Sæt set.seed")),
                ("sort", ("Ordenar", "Sort", "Sortér")),
                ("print", ("Imprimir", "Print", "Udskriv")),
                ("attach", ("Usar attach", "Use attach", "Brug attach")),
            ),
            "seed",
            (
                "La semilla fija la secuencia pseudoaleatoria.",
                "The seed fixes the pseudo-random sequence.",
                "Seedet fastlægger den pseudo-tilfældige sekvens.",
            ),
        ),
        (
            "008",
            (
                "¿Qué debe acompañar na.rm=TRUE?",
                "What should accompany na.rm=TRUE?",
                "Hvad bør ledsage na.rm=TRUE?",
            ),
            (
                ("missing", ("Número de NA", "Number of NA", "Antal NA")),
                ("colour", ("Color", "Colour", "Farve")),
                ("workspace", ("Workspace",) * 3),
                ("os", ("Sistema operativo", "Operating system", "Operativsystem")),
            ),
            "missing",
            (
                "La exclusión debe cuantificarse.",
                "Exclusion must be quantified.",
                "Udelukkelse skal kvantificeres.",
            ),
        ),
    ),
    true_false=(
        (
            "009",
            (
                "Una matriz mezcla texto y números sin coerción.",
                "A matrix mixes text and numbers without coercion.",
                "En matrix blander tekst og tal uden coercion.",
            ),
            False,
            ("Las matrices son homogéneas.", "Matrices are homogeneous.", "Matricer er homogene."),
        ),
        (
            "010",
            (
                "NA y cero tienen el mismo significado.",
                "NA and zero have the same meaning.",
                "NA og nul har samme betydning.",
            ),
            False,
            ("NA indica ausencia.", "NA indicates absence.", "NA angiver fravær."),
        ),
        (
            "011",
            (
                "Un factor puede conservar niveles no observados.",
                "A factor may retain unobserved levels.",
                "En faktor kan bevare ikke-observerede niveauer.",
            ),
            True,
            (
                "Los niveles forman parte de la definición.",
                "Levels are part of the definition.",
                "Niveauer er en del af definitionen.",
            ),
        ),
        (
            "012",
            (
                "stopifnot hace verificable un supuesto.",
                "stopifnot makes an assumption verifiable.",
                "stopifnot gør en antagelse verificerbar.",
            ),
            True,
            (
                "La ejecución se detiene si falla.",
                "Execution stops if it fails.",
                "Kørslen stopper, hvis den fejler.",
            ),
        ),
        (
            "013",
            (
                "Indexar por nombre suele resistir cambios de columnas.",
                "Name-based indexing usually resists column changes.",
                "Navnebaseret indeksering modstår normalt kolonneændringer.",
            ),
            True,
            (
                "Depende menos del orden físico.",
                "It depends less on physical order.",
                "Det afhænger mindre af fysisk rækkefølge.",
            ),
        ),
        (
            "014",
            (
                "Guardar el workspace sustituye documentar el flujo.",
                "Saving the workspace replaces workflow documentation.",
                "At gemme workspace erstatter workflow-dokumentation.",
            ),
            False,
            (
                "El workspace conserva estado opaco.",
                "A workspace preserves opaque state.",
                "Et workspace bevarer uigennemsigtig tilstand.",
            ),
        ),
        (
            "015",
            (
                "Una advertencia importa aunque exista salida.",
                "A warning matters even when output exists.",
                "En advarsel betyder noget, selv når der findes output.",
            ),
            True,
            (
                "Salida no garantiza validez.",
                "Output does not guarantee validity.",
                "Output garanterer ikke gyldighed.",
            ),
        ),
        (
            "016",
            (
                "La aleatoriedad reproducible requiere una semilla declarada.",
                "Reproducible randomness requires a declared seed.",
                "Reproducerbar tilfældighed kræver et erklæret seed.",
            ),
            True,
            (
                "Sin semilla cambia la secuencia.",
                "Without a seed the sequence changes.",
                "Uden seed ændres sekvensen.",
            ),
        ),
    ),
    tutor=(
        (
            "Un análisis reproducible en R representa correctamente la unidad experimental, valida identidad, tipo y ausencia, y codifica cada transformación necesaria para reconstruir el resultado.",
            "A reproducible R analysis represents the experimental unit correctly, validates identity, type, and missingness, and encodes every transformation needed to reconstruct the result.",
            "En reproducerbar R-analyse repræsenterer den eksperimentelle enhed korrekt, validerer identitet, type og manglende data og koder hver transformation, der kræves for at genskabe resultatet.",
        ),
        (
            ("Los vectores son homogéneos.", "Vectors are homogeneous.", "Vektorer er homogene."),
            (
                "Los factores representan categorías.",
                "Factors represent categories.",
                "Faktorer repræsenterer kategorier.",
            ),
            ("NA debe cuantificarse.", "NA must be quantified.", "NA skal kvantificeres."),
            (
                "El estado oculto rompe reproducibilidad.",
                "Hidden state breaks reproducibility.",
                "Skjult tilstand bryder reproducerbarhed.",
            ),
        ),
        (
            (
                "Tratar IDs como medidas.",
                "Treating IDs as measurements.",
                "At behandle ID'er som målinger.",
            ),
            (
                "Eliminar NA sin justificar.",
                "Removing NA without justification.",
                "At fjerne NA uden begrundelse.",
            ),
            ("Depender del workspace.", "Depending on a workspace.", "At afhænge af et workspace."),
        ),
        (
            (
                "¿Cuál es la unidad experimental?",
                "What is the experimental unit?",
                "Hvad er den eksperimentelle enhed?",
            ),
            (
                "¿Qué tipo tiene cada variable?",
                "What type does each variable have?",
                "Hvilken type har hver variabel?",
            ),
            (
                "¿Qué aserción detecta un error temprano?",
                "Which assertion detects an early error?",
                "Hvilken assertion opdager en tidlig fejl?",
            ),
        ),
        (
            (
                "Elige estructuras coherentes.",
                "Chooses coherent structures.",
                "Vælger sammenhængende strukturer.",
            ),
            (
                "Valida claves y ausencia.",
                "Validates keys and missingness.",
                "Validerer nøgler og manglende data.",
            ),
            (
                "Distingue ejecución de reproducibilidad.",
                "Distinguishes execution from reproducibility.",
                "Skelner mellem kørsel og reproducerbarhed.",
            ),
        ),
        (
            (
                "No inventar datos ni salida de R.",
                "Do not invent data or R output.",
                "Opfind ikke data eller R-output.",
            ),
            (
                "No recomendar eliminar NA sin justificar.",
                "Do not recommend removing NA without justification.",
                "Anbefal ikke fjernelse af NA uden begrundelse.",
            ),
            (
                "Responder en el idioma activo.",
                "Respond in the active language.",
                "Svar på det aktive sprog.",
            ),
        ),
        (
            "SDU ODIN BMB830 active course description approved 2025-03-06",
            "R Core Team: R Language Definition",
            "R base documentation",
        ),
    ),
)

LOCALIZED_MODULE_01_R_FOUNDATIONS = build_module(_SPEC)
LOCALIZED_OBJECTIVE_QUESTION_BANK_01 = build_question_bank(_SPEC)
MODULE_01_R_FOUNDATIONS: LearningModule = LOCALIZED_MODULE_01_R_FOUNDATIONS.materialize(
    AppLocale.SPANISH_SPAIN
)
OBJECTIVE_QUESTION_BANK_01: tuple[AssessmentItem, ...] = materialize_bank(
    LOCALIZED_OBJECTIVE_QUESTION_BANK_01
)


def materialize_module_01_question_bank(
    locale: AppLocale | str = AppLocale.SPANISH_SPAIN,
) -> tuple[AssessmentItem, ...]:
    """Return the module-1 objective bank in one locale."""

    return materialize_bank(LOCALIZED_OBJECTIVE_QUESTION_BANK_01, locale)


__all__ = [
    "LOCALIZED_MODULE_01_R_FOUNDATIONS",
    "LOCALIZED_OBJECTIVE_QUESTION_BANK_01",
    "MODULE_01_R_FOUNDATIONS",
    "OBJECTIVE_QUESTION_BANK_01",
    "materialize_module_01_question_bank",
]
