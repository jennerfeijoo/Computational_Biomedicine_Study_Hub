"""Book-grounded extension for DM857 scientific-library data ingestion."""

from __future__ import annotations

from dataclasses import replace

from ...learning.activity_types import ActivityType
from ..localized_models import LocalizedLearningModule, LocalizedTutorSupportPacket
from .authoring import concept, example, objective, objective_mcq, practice
from .book_grounded_extensions import ModuleSourceAudit


def _with_source_basis(
    module: LocalizedLearningModule,
    source_ids: tuple[str, ...],
) -> LocalizedLearningModule:
    tutor = module.tutor_support
    merged = tuple(dict.fromkeys((*tutor.source_basis, *source_ids)))
    updated_tutor: LocalizedTutorSupportPacket = replace(
        tutor,
        source_basis=merged,
    )
    return replace(module, tutor_support=updated_tutor)


def update_scientific_libraries_audit(
    audit: tuple[ModuleSourceAudit, ...],
) -> tuple[ModuleSourceAudit, ...]:
    """Mark M13 reviewed after its focused ingestion extension is present."""
    updated: list[ModuleSourceAudit] = []
    for item in audit:
        if item.module_id == "dm857.m13":
            updated.append(
                replace(
                    item,
                    state="consistent",
                    finding=(
                        "Existing coverage of imports, environments, NumPy arrays, broadcasting, "
                        "pandas selection, missing data, joins, plotting, and result validation is "
                        "consistent. Explicit file-to-DataFrame ingestion contracts and schema "
                        "checks needed one focused treatment."
                    ),
                    implemented_change=(
                        "Added an original tabular-ingestion explanation, in-memory CSV example, "
                        "schema-debugging practice, and stable objective item."
                    ),
                )
            )
        else:
            updated.append(item)
    return tuple(updated)


def _extend_scientific_libraries(
    module: LocalizedLearningModule,
) -> LocalizedLearningModule:
    """Add explicit CSV ingestion and schema contracts to M13."""
    extended = replace(
        module,
        objectives=module.objectives
        + (
            objective(
                "m13.bg.o1",
                (
                    "Convertir una tabla textual en un DataFrame y validar su esquema antes del análisis.",
                    "Convert a text table into a DataFrame and validate its schema before analysis.",
                    "Konvertere en teksttabel til en DataFrame og validere dens schema før analyse.",
                ),
            ),
        ),
        concepts=module.concepts
        + (
            concept(
                "tabular-ingestion-and-schema-contracts",
                (
                    "Ingesta tabular y contratos de esquema",
                    "Tabular ingestion and schema contracts",
                    "Tabelindlæsning og schema-kontrakter",
                ),
                (
                    "Leer un CSV no es una operación neutral: el separador, los nombres de columnas, "
                    "los símbolos de ausencia, la codificación y la inferencia de tipos determinan el "
                    "DataFrame resultante. Antes de calcular, el programa debe comprobar las columnas "
                    "esperadas, el orden o conjunto permitido, los tipos relevantes, la unicidad de "
                    "las claves, la cantidad de filas, los valores ausentes y los rangos imposibles. "
                    "Parámetros como usecols y dtype convierten parte del esquema en una instrucción "
                    "ejecutable. Después de cargar, las validaciones convierten supuestos científicos "
                    "en fallos visibles. Un DataFrame puede contener columnas de tipos diferentes; "
                    "convertirlo sin cuidado a ndarray puede promover todo a un tipo común y perder "
                    "semántica. Para enseñar y probar el flujo sin depender de archivos externos, una "
                    "tabla pequeña puede mantenerse en memoria con StringIO.",
                    "Reading CSV is not a neutral operation: the separator, column names, missing-value "
                    "tokens, encoding, and dtype inference determine the resulting DataFrame. Before "
                    "computing, the program should check expected columns, allowed order or set, "
                    "relevant dtypes, key uniqueness, row count, missingness, and impossible ranges. "
                    "Parameters such as usecols and dtype turn part of the schema into an executable "
                    "instruction. Post-load validation turns scientific assumptions into visible "
                    "failures. A DataFrame may contain columns with different dtypes; careless ndarray "
                    "conversion can promote everything to one common type and discard semantics. For "
                    "teaching and testing without external files, a small table can remain in memory "
                    "through StringIO.",
                    "Læsning af CSV er ikke en neutral operation: separator, kolonnenavne, symboler for "
                    "manglende værdier, encoding og typeinferens bestemmer den resulterende DataFrame. "
                    "Før beregning bør programmet kontrollere forventede kolonner, tilladt orden eller "
                    "mængde, relevante datatyper, nøglers entydighed, rækkeantal, manglende værdier og "
                    "umulige intervaller. Parametre som usecols og dtype gør en del af schemaet til en "
                    "eksekverbar instruktion. Validering efter indlæsning gør videnskabelige antagelser "
                    "til synlige fejl. En DataFrame kan have kolonner med forskellige datatyper; en "
                    "ukritisk konvertering til ndarray kan fremme alt til én fælles type og miste "
                    "semantik. Til undervisning og test uden eksterne filer kan en lille tabel holdes i "
                    "hukommelsen med StringIO.",
                ),
                (
                    (
                        "La lectura interpreta texto; no garantiza por sí sola un esquema correcto.",
                        "Parsing interprets text; it does not by itself guarantee a correct schema.",
                        "Parsing fortolker tekst; den garanterer ikke i sig selv et korrekt schema.",
                    ),
                    (
                        "usecols y dtype expresan parte del contrato de entrada.",
                        "usecols and dtype express part of the input contract.",
                        "usecols og dtype udtrykker en del af inputkontrakten.",
                    ),
                    (
                        "Las claves, filas, ausentes y rangos deben validarse después de cargar.",
                        "Keys, rows, missingness, and ranges require post-load validation.",
                        "Nøgler, rækker, manglende værdier og intervaller skal valideres efter indlæsning.",
                    ),
                    (
                        "La conversión a ndarray puede perder tipos y etiquetas tabulares.",
                        "Conversion to ndarray may lose tabular dtypes and labels.",
                        "Konvertering til ndarray kan miste tabeldatatyper og etiketter.",
                    ),
                ),
            ),
        ),
        worked_examples=module.worked_examples
        + (
            example(
                "m13.bg.e01",
                (
                    "Cargar y validar una tabla mínima",
                    "Load and validate a minimal table",
                    "Indlæs og validér en minimal tabel",
                ),
                (
                    "Lee un CSV mantenido en memoria, declara columnas y tipos, y comprueba el contrato "
                    "antes de calcular un total.",
                    "Read an in-memory CSV, declare columns and dtypes, and check the contract before "
                    "computing a total.",
                    "Læs en CSV i hukommelsen, deklarér kolonner og datatyper, og kontrollér kontrakten "
                    "før beregning af en total.",
                ),
                (
                    (
                        "StringIO evita depender de un archivo o una descarga externa.",
                        "StringIO avoids depending on an external file or download.",
                        "StringIO undgår afhængighed af en ekstern fil eller download.",
                    ),
                    (
                        "usecols y dtype hacen explícito el esquema esperado.",
                        "usecols and dtype make the expected schema explicit.",
                        "usecols og dtype gør det forventede schema eksplicit.",
                    ),
                    (
                        "Las comprobaciones se ejecutan antes de usar los valores.",
                        "Checks run before the values are used.",
                        "Kontrollerne køres før værdierne anvendes.",
                    ),
                ),
                "from io import StringIO\n"
                "\n"
                "import pandas as pd\n"
                "\n"
                "raw = StringIO('sample,count\\nS1,12\\nS2,15\\n')\n"
                "df = pd.read_csv(\n"
                "    raw,\n"
                "    usecols=['sample', 'count'],\n"
                "    dtype={'sample': 'string', 'count': 'Int64'},\n"
                ")\n"
                "expected_columns = ('sample', 'count')\n"
                "if tuple(df.columns) != expected_columns:\n"
                "    raise ValueError('unexpected columns')\n"
                "if not df['sample'].is_unique:\n"
                "    raise ValueError('sample must be unique')\n"
                "if df['count'].isna().any() or (df['count'] < 0).any():\n"
                "    raise ValueError('count contract violated')\n"
                "print(df.shape)\n"
                "print(tuple(df.columns))\n"
                "print(int(df['count'].sum()))",
                "(2, 2)\n('sample', 'count')\n27",
                (
                    "El cálculo sólo ocurre después de confirmar estructura, clave y dominio. La tabla "
                    "es deliberadamente pequeña y sintética; demuestra el contrato de ingesta, no un "
                    "protocolo para datos experimentales.",
                    "Computation occurs only after structure, key, and domain are confirmed. The table "
                    "is deliberately small and synthetic; it demonstrates an ingestion contract, not "
                    "an experimental-data protocol.",
                    "Beregningen sker først efter bekræftelse af struktur, nøgle og domæne. Tabellen er "
                    "bevidst lille og syntetisk; den demonstrerer en indlæsningskontrakt, ikke en "
                    "protokol for eksperimentelle data.",
                ),
            ),
        ),
        practice_exercises=module.practice_exercises
        + (
            practice(
                "m13.bg.p01",
                ActivityType.PIPELINE_DESIGN,
                (
                    "Una tabla CSV debería contener sample y count, con una fila por muestra y count "
                    "entero no negativo. Al cargarla aparecen una columna extra, muestras duplicadas, "
                    "un valor ausente y count como float. Diseña una secuencia de carga y validación que "
                    "rechace el archivo antes del análisis.",
                    "A CSV table should contain sample and count, with one row per sample and a "
                    "non-negative integer count. Loading reveals an extra column, duplicate samples, a "
                    "missing value, and count as float. Design a load-and-validation sequence that "
                    "rejects the file before analysis.",
                    "En CSV-tabel bør indeholde sample og count med én række pr. prøve og et "
                    "ikke-negativt heltals-count. Ved indlæsning ses en ekstra kolonne, dublerede prøver, "
                    "en manglende værdi og count som float. Design en indlæsnings- og valideringssekvens, "
                    "der afviser filen før analyse.",
                ),
                (
                    (
                        "Haz que columnas y tipos formen parte de read_csv.",
                        "Make columns and dtypes part of read_csv.",
                        "Gør kolonner og datatyper til en del af read_csv.",
                    ),
                    (
                        "Después valida unicidad, ausencia, dominio y número de filas.",
                        "Then validate uniqueness, missingness, domain, and row count.",
                        "Validér derefter entydighed, manglende værdier, domæne og rækkeantal.",
                    ),
                ),
                (
                    "Leer sólo sample y count con usecols; declarar sample como string y count con un "
                    "tipo entero anulable; comprobar exactamente las columnas esperadas; rechazar "
                    "sample duplicado; rechazar count ausente; comprobar count >= 0 y que no se perdió "
                    "ninguna fila esperada. No convertir ausentes a cero ni eliminar duplicados sin una "
                    "regla científica documentada.",
                    "Read only sample and count with usecols; declare sample as string and count with a "
                    "nullable integer dtype; check the exact expected columns; reject duplicate sample "
                    "keys; reject missing count values; check count >= 0 and that no expected rows were "
                    "lost. Do not turn missing values into zero or drop duplicates without a documented "
                    "scientific rule.",
                    "Læs kun sample og count med usecols; deklarér sample som string og count med en "
                    "nullable heltalstype; kontrollér de præcise forventede kolonner; afvis dublerede "
                    "sample-nøgler; afvis manglende count; kontrollér count >= 0 og at ingen forventede "
                    "rækker gik tabt. Manglende værdier må ikke ændres til nul, og dubletter må ikke "
                    "fjernes uden en dokumenteret videnskabelig regel.",
                ),
                (
                    "La solución separa interpretación del archivo, validación del esquema y política "
                    "científica. Un archivo legible puede seguir siendo inválido para el análisis.",
                    "The solution separates file interpretation, schema validation, and scientific "
                    "policy. A readable file may still be invalid for analysis.",
                    "Løsningen adskiller filfortolkning, schema-validering og videnskabelig politik. En "
                    "læsbar fil kan stadig være ugyldig til analyse.",
                ),
            ),
        ),
        assessment_items=module.assessment_items
        + (
            objective_mcq(
                "dm857.m13.book.001",
                (
                    "¿Qué flujo protege mejor el análisis al cargar una tabla CSV?",
                    "Which workflow best protects an analysis when loading a CSV table?",
                    "Hvilket workflow beskytter bedst en analyse ved indlæsning af en CSV-tabel?",
                ),
                (
                    (
                        "read_and_trust",
                        (
                            "Leer el archivo y comenzar el cálculo si pandas no genera una excepción.",
                            "Read the file and start computing if pandas raises no exception.",
                            "Læs filen og begynd beregningen, hvis pandas ikke giver en exception.",
                        ),
                    ),
                    (
                        "explicit_contract",
                        (
                            "Declarar columnas y tipos, cargar, validar claves, filas, ausentes y rangos, "
                            "y sólo entonces calcular.",
                            "Declare columns and dtypes, load, validate keys, rows, missingness, and "
                            "ranges, and only then compute.",
                            "Deklarér kolonner og datatyper, indlæs, validér nøgler, rækker, manglende "
                            "værdier og intervaller, og beregn først derefter.",
                        ),
                    ),
                    (
                        "repair_silently",
                        (
                            "Eliminar duplicados y reemplazar ausentes por cero sin registrar la decisión.",
                            "Drop duplicates and replace missing values with zero without recording it.",
                            "Fjern dubletter og erstat manglende værdier med nul uden registrering.",
                        ),
                    ),
                ),
                "explicit_contract",
                (
                    "La ausencia de errores de lectura sólo demuestra que el texto pudo interpretarse. "
                    "El análisis necesita además un contrato explícito y comprobaciones observables.",
                    "The absence of parsing errors only shows that the text was readable. Analysis also "
                    "requires an explicit contract and observable checks.",
                    "Fravær af parsing-fejl viser kun, at teksten kunne læses. Analysen kræver også en "
                    "eksplicit kontrakt og observerbare kontroller.",
                ),
            ),
        ),
    )
    return _with_source_basis(extended, ("guttag-2021-ch13-15-23",))


def apply_scientific_libraries_book_extension(
    modules: tuple[LocalizedLearningModule, ...],
) -> tuple[LocalizedLearningModule, ...]:
    """Apply the focused M13 extension without changing other modules."""
    return tuple(
        _extend_scientific_libraries(module) if module.module_id == "dm857.m13" else module
        for module in modules
    )
