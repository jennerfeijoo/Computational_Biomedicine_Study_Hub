"""DM857 module 13: libraries, environments, and scientific computing."""

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
        "m13.o1",
        (
            "Explicar cómo se resuelven imports, módulos, paquetes y espacios de nombres.",
            "Explain how imports, modules, packages, and namespaces are resolved.",
            "Forklare hvordan imports, moduler, pakker og namespaces opløses.",
        ),
    ),
    (
        "m13.o2",
        (
            "Crear entornos reproducibles y registrar versiones relevantes.",
            "Create reproducible environments and record relevant versions.",
            "Oprette reproducerbare miljøer og registrere relevante versioner.",
        ),
    ),
    (
        "m13.o3",
        (
            "Construir y examinar arrays NumPy con formas y tipos explícitos.",
            "Construct and inspect NumPy arrays with explicit shapes and dtypes.",
            "Konstruere og undersøge NumPy-arrays med eksplicitte former og datatyper.",
        ),
    ),
    (
        "m13.o4",
        (
            "Aplicar vectorización y broadcasting sin ocultar supuestos dimensionales.",
            "Apply vectorization and broadcasting without hiding dimensional assumptions.",
            "Anvende vektorisering og broadcasting uden at skjule dimensionelle antagelser.",
        ),
    ),
    (
        "m13.o5",
        (
            "Crear, seleccionar y transformar DataFrames de pandas de forma verificable.",
            "Create, select, and transform pandas DataFrames in a verifiable way.",
            "Oprette, vælge og transformere pandas-DataFrames på en verificerbar måde.",
        ),
    ),
    (
        "m13.o6",
        (
            "Tratar valores ausentes, índices y tipos de columna explícitamente.",
            "Handle missing values, indexes, and column types explicitly.",
            "Håndtere manglende værdier, indeks og kolonnetyper eksplicit.",
        ),
    ),
    (
        "m13.o7",
        (
            "Construir visualizaciones que representen los datos sin distorsión.",
            "Build visualizations that represent data without distortion.",
            "Bygge visualiseringer der repræsenterer data uden forvrængning.",
        ),
    ),
    (
        "m13.o8",
        (
            "Validar resultados científicos mediante controles de forma, rango y equivalencia.",
            "Validate scientific results through shape, range, and equivalence checks.",
            "Validere videnskabelige resultater gennem kontrol af form, interval og ækvivalens.",
        ),
    ),
)

_CONCEPTS = (
    (
        "imports-and-namespaces",
        (
            "Imports, módulos y espacios de nombres",
            "Imports, modules, and namespaces",
            "Imports, moduler og namespaces",
        ),
        (
            "Un módulo es un archivo Python importable y un paquete organiza módulos bajo un espacio de "
            "nombres. import nombre vincula el módulo; from nombre import objeto vincula un objeto "
            "concreto. Los alias reducen repetición, pero deben conservar legibilidad. La búsqueda "
            "depende de sys.path y del entorno activo. Los imports deben ser explícitos, ubicarse al "
            "inicio y evitar comodines porque dificultan saber de dónde procede cada símbolo.",
            "A module is an importable Python file and a package organizes modules under a namespace. "
            "import name binds the module; from name import object binds a specific object. Aliases "
            "reduce repetition but should preserve readability. Resolution depends on sys.path and the "
            "active environment. Imports should be explicit, placed near the top, and avoid wildcards "
            "because wildcards obscure symbol provenance.",
            "Et modul er en importérbar Python-fil, og en pakke organiserer moduler under et namespace. "
            "import navn binder modulet; from navn import objekt binder et bestemt objekt. Aliasser "
            "reducerer gentagelse, men skal bevare læsbarhed. Opløsning afhænger af sys.path og det "
            "aktive miljø. Imports bør være eksplicitte og undgå jokertegn, fordi de skjuler "
            "symbolernes oprindelse.",
        ),
        [
            (
                "Importa el módulo cuando necesitas varios nombres.",
                "Import the module when you need several names.",
                "Importér modulet når du behøver flere navne.",
            ),
            (
                "Evita from paquete import *.",
                "Avoid from package import *.",
                "Undgå from package import *.",
            ),
            (
                "El entorno activo determina qué paquete se carga.",
                "The active environment determines which package loads.",
                "Det aktive miljø bestemmer hvilken pakke der indlæses.",
            ),
        ],
    ),
    (
        "documentation-and-api",
        (
            "Documentación y contratos de API",
            "Documentation and API contracts",
            "Dokumentation og API-kontrakter",
        ),
        (
            "Usar una biblioteca exige leer su documentación, firma, tipos aceptados, forma de retorno, "
            "errores y convenciones. help(), docstrings y documentación oficial permiten comprobar el "
            "contrato. Los ejemplos mínimos verifican una hipótesis de uso, pero no sustituyen las "
            "pruebas del propio programa. Una API puede cambiar entre versiones; por eso conviene "
            "distinguir funciones públicas de detalles internos.",
            "Using a library requires reading its documentation, signature, accepted types, return "
            "shape, errors, and conventions. help(), docstrings, and official documentation expose the "
            "contract. Minimal examples test a usage hypothesis but do not replace program tests. APIs "
            "may change across versions, so public functions should be distinguished from internal "
            "details.",
            "Brug af et bibliotek kræver læsning af dokumentation, signatur, accepterede typer, "
            "returform, fejl og konventioner. help(), docstrings og officiel dokumentation viser "
            "kontrakten. Små eksempler afprøver en brugsantagelse, men erstatter ikke programtest. "
            "API'er kan ændres mellem versioner.",
        ),
        [
            (
                "Comprueba parámetros y forma de retorno.",
                "Check parameters and return shape.",
                "Kontrollér parametre og returform.",
            ),
            (
                "Prefiere API pública documentada.",
                "Prefer documented public APIs.",
                "Foretræk dokumenterede offentlige API'er.",
            ),
            (
                "Registra la versión usada al reproducir resultados.",
                "Record the version used for reproducibility.",
                "Registrér den anvendte version for reproducerbarhed.",
            ),
        ],
    ),
    (
        "environments-and-versions",
        (
            "Entornos y versiones reproducibles",
            "Reproducible environments and versions",
            "Reproducerbare miljøer og versioner",
        ),
        (
            "Un entorno virtual aísla dependencias por proyecto. Un archivo de requisitos o "
            "configuración declara paquetes y restricciones; un archivo de bloqueo puede fijar "
            "resoluciones exactas. La reproducibilidad también requiere versión de Python, sistema, "
            "semilla aleatoria cuando proceda y datos de entrada. Fijar cada parche para siempre impide "
            "actualizaciones; no fijar nada permite cambios silenciosos. La estrategia debe equilibrar "
            "reproducibilidad, seguridad y mantenimiento.",
            "A virtual environment isolates dependencies per project. A requirements or project file "
            "declares packages and constraints; a lock file may preserve exact resolutions. "
            "Reproducibility also requires the Python version, platform, random seed when relevant, and "
            "input data. Pinning every patch forever blocks updates; pinning nothing allows silent "
            "changes. The strategy should balance reproducibility, security, and maintenance.",
            "Et virtuelt miljø isolerer afhængigheder pr. projekt. En krav- eller projektfil angiver "
            "pakker og begrænsninger; en låsefil kan fastholde præcise løsninger. Reproducerbarhed "
            "kræver også Python-version, platform, tilfældig seed når relevant og inputdata. Strategien "
            "skal balancere reproducerbarhed, sikkerhed og vedligeholdelse.",
        ),
        [
            (
                "Un proyecto debe declarar sus dependencias.",
                "A project should declare its dependencies.",
                "Et projekt bør deklarere sine afhængigheder.",
            ),
            (
                "Registra Python y paquetes relevantes.",
                "Record Python and relevant package versions.",
                "Registrér Python og relevante pakkeversioner.",
            ),
            (
                "Reproduce en un entorno limpio.",
                "Reproduce in a clean environment.",
                "Reproducer i et rent miljø.",
            ),
        ],
    ),
    (
        "numpy-array-model",
        ("Modelo de arrays NumPy", "The NumPy array model", "NumPy-arraymodellen"),
        (
            "ndarray almacena elementos de tipo homogéneo en una estructura n-dimensional. shape "
            "describe dimensiones, ndim su número, size el total de elementos y dtype la "
            "representación. Crear un array desde datos mixtos puede promover tipos y cambiar la "
            "semántica. reshape exige conservar size; axis determina sobre qué dimensión se reduce. Una "
            "vista puede compartir memoria con el original, mientras una copia es independiente.",
            "ndarray stores homogeneous elements in an n-dimensional structure. shape describes "
            "dimensions, ndim their count, size the total elements, and dtype the representation. "
            "Building an array from mixed data may promote types and change semantics. reshape must "
            "preserve size; axis determines the reduction dimension. A view may share memory with the "
            "original, whereas a copy is independent.",
            "ndarray lagrer homogene elementer i en n-dimensional struktur. shape beskriver "
            "dimensionerne, ndim deres antal, size det samlede antal elementer og dtype "
            "repræsentationen. Blandede data kan fremme typen. reshape skal bevare size; axis bestemmer "
            "reduktionsdimensionen. Et view kan dele hukommelse med originalen.",
        ),
        [
            (
                "Inspecciona shape y dtype antes de calcular.",
                "Inspect shape and dtype before computing.",
                "Undersøg shape og dtype før beregning.",
            ),
            (
                "reshape no cambia el número de elementos.",
                "reshape does not change element count.",
                "reshape ændrer ikke antallet af elementer.",
            ),
            (
                "Distingue vista y copia.",
                "Distinguish views and copies.",
                "Skeln mellem view og kopi.",
            ),
        ],
    ),
    (
        "vectorization-broadcasting",
        (
            "Vectorización y broadcasting",
            "Vectorization and broadcasting",
            "Vektorisering og broadcasting",
        ),
        (
            "La vectorización expresa operaciones sobre arrays completos y delega bucles a "
            "implementaciones optimizadas. Broadcasting alinea dimensiones desde la derecha y permite "
            "operar cuando cada par es igual o una dimensión vale uno. Que una operación sea válida no "
            "significa que sea conceptualmente correcta: una forma accidental puede producir un "
            "resultado plausible pero equivocado. Deben verificarse shapes, unidades y orientación de "
            "muestras y variables.",
            "Vectorization expresses operations over complete arrays and delegates loops to optimized "
            "implementations. Broadcasting aligns dimensions from the right and permits operations when "
            "each pair matches or one dimension is one. A valid operation is not automatically "
            "conceptually correct: an accidental shape may produce a plausible but wrong result. "
            "Shapes, units, and sample-variable orientation must be checked.",
            "Vektorisering udtrykker operationer over hele arrays og delegerer løkker til optimerede "
            "implementeringer. Broadcasting justerer dimensioner fra højre og tillader operationer når "
            "hvert par er ens eller én dimension er én. En gyldig operation er ikke nødvendigvis "
            "konceptuelt korrekt; former, enheder og orientering skal kontrolleres.",
        ),
        [
            (
                "Alinea dimensiones desde la derecha.",
                "Align dimensions from the right.",
                "Juster dimensioner fra højre.",
            ),
            (
                "Una dimensión uno puede expandirse.",
                "A size-one dimension may expand.",
                "En dimension på én kan udvides.",
            ),
            (
                "Valida la semántica además de la compatibilidad.",
                "Validate semantics as well as compatibility.",
                "Validér semantik såvel som kompatibilitet.",
            ),
        ],
    ),
    (
        "pandas-tabular-model",
        (
            "Series, DataFrame e índices",
            "Series, DataFrame, and indexes",
            "Series, DataFrame og indeks",
        ),
        (
            "Una Series combina valores e índice; un DataFrame alinea columnas por índice. El índice no "
            "es sólo una posición: puede representar una identidad y participa en alineaciones. loc "
            "selecciona por etiqueta e iloc por posición. Las operaciones encadenadas pueden crear "
            "ambigüedad sobre vistas y copias; conviene seleccionar filas y columnas explícitamente y "
            "asignar mediante loc. Los nombres y tipos de columnas forman parte del contrato tabular.",
            "A Series combines values and an index; a DataFrame aligns columns by index. The index is "
            "not merely a position: it may represent identity and participates in alignment. loc "
            "selects by label and iloc by position. Chained operations may create ambiguity about views "
            "and copies; select explicitly and assign through loc. Column names and dtypes form part of "
            "the tabular contract.",
            "En Series kombinerer værdier og indeks; en DataFrame justerer kolonner efter indeks. "
            "Indekset er ikke kun en position, men kan repræsentere identitet. loc vælger efter etiket "
            "og iloc efter position. Kædede operationer kan skabe tvivl om views og kopier; vælg "
            "eksplicit og tildel gennem loc.",
        ),
        [
            (
                "loc usa etiquetas; iloc usa posiciones.",
                "loc uses labels; iloc uses positions.",
                "loc bruger etiketter; iloc bruger positioner.",
            ),
            (
                "La alineación por índice puede introducir NaN.",
                "Index alignment may introduce NaN.",
                "Indeksjustering kan introducere NaN.",
            ),
            (
                "Valida nombres y dtypes de columnas.",
                "Validate column names and dtypes.",
                "Validér kolonnenavne og datatyper.",
            ),
        ],
    ),
    (
        "missing-data-and-transforms",
        (
            "Valores ausentes y transformaciones",
            "Missing data and transformations",
            "Manglende data og transformationer",
        ),
        (
            "NaN, None y pd.NA no son intercambiables en todos los tipos. isna detecta ausencia; dropna "
            "elimina según una política; fillna imputa un valor que debe justificarse. groupby divide, "
            "aplica y combina; merge une tablas según claves y puede multiplicar filas si las claves no "
            "son únicas. Cada transformación debe documentar qué filas conserva, qué claves espera y "
            "cómo cambia el tipo o la granularidad.",
            "NaN, None, and pd.NA are not interchangeable across all dtypes. isna detects absence; "
            "dropna removes under a policy; fillna imputes a value that must be justified. groupby "
            "splits, applies, and combines; merge joins tables by keys and may multiply rows when keys "
            "are not unique. Each transformation should document retained rows, expected keys, and "
            "changes in dtype or granularity.",
            "NaN, None og pd.NA er ikke udskiftelige for alle datatyper. isna opdager fravær; dropna "
            "fjerner efter en politik; fillna imputerer en værdi der skal begrundes. groupby opdeler, "
            "anvender og kombinerer; merge forbinder tabeller efter nøgler og kan mangedoble rækker ved "
            "ikke-unikke nøgler.",
        ),
        [
            (
                "Ausencia no implica cero.",
                "Missingness does not mean zero.",
                "Manglende værdi betyder ikke nul.",
            ),
            (
                "Comprueba cardinalidad antes y después de merge.",
                "Check cardinality before and after merge.",
                "Kontrollér kardinalitet før og efter merge.",
            ),
            (
                "Documenta la política de imputación.",
                "Document the imputation policy.",
                "Dokumentér imputationspolitikken.",
            ),
        ],
    ),
    (
        "visualization-validation",
        (
            "Visualización y validación científica",
            "Visualization and scientific validation",
            "Visualisering og videnskabelig validering",
        ),
        (
            "Una figura debe corresponder al tipo de variable y a la pregunta: líneas para evolución "
            "ordenada, dispersión para relaciones, barras para categorías y histogramas para "
            "distribuciones. Ejes, unidades, límites y leyendas deben ser explícitos. El gráfico no "
            "sustituye controles numéricos: forma, rango, conteos, valores ausentes y comparación con "
            "una implementación simple ayudan a detectar errores. Guardar la figura con parámetros "
            "reproducibles completa el proceso.",
            "A figure should match the variable type and question: lines for ordered evolution, scatter "
            "for relationships, bars for categories, and histograms for distributions. Axes, units, "
            "limits, and legends should be explicit. A plot does not replace numeric checks: shape, "
            "range, counts, missingness, and comparison with a simple implementation help detect "
            "errors. Saving the figure with reproducible parameters completes the process.",
            "En figur skal passe til variabeltype og spørgsmål: linjer til ordnet udvikling, spredning "
            "til relationer, søjler til kategorier og histogrammer til fordelinger. Akser, enheder, "
            "grænser og signaturforklaring skal være eksplicitte. Et plot erstatter ikke numeriske "
            "kontroller af form, interval, antal og manglende værdier.",
        ),
        [
            ("Etiqueta ejes y unidades.", "Label axes and units.", "Mærk akser og enheder."),
            (
                "No truncar ejes para exagerar diferencias.",
                "Do not truncate axes to exaggerate differences.",
                "Afkort ikke akser for at overdrive forskelle.",
            ),
            (
                "Combina gráficos con controles numéricos.",
                "Combine plots with numeric checks.",
                "Kombinér plots med numeriske kontroller.",
            ),
        ],
    ),
)

_EXAMPLES = (
    (
        "array-standardization",
        (
            "Estandarización por columnas",
            "Column-wise standardization",
            "Kolonnevis standardisering",
        ),
        (
            "Estandariza tres variables y verifica media y desviación.",
            "Standardize three variables and verify mean and deviation.",
            "Standardisér tre variable og kontrollér middelværdi og afvigelse.",
        ),
        [
            (
                "Representar muestras por filas.",
                "Represent samples by rows.",
                "Repræsentér prøver som rækker.",
            ),
            ("Calcular por axis=0.", "Compute along axis=0.", "Beregn langs axis=0."),
            ("Comprobar el resultado.", "Check the result.", "Kontrollér resultatet."),
        ],
        "import numpy as np\n"
        "\n"
        "x = np.array([[1.0, 10.0], [2.0, 12.0], [3.0, 14.0]])\n"
        "mean = x.mean(axis=0)\n"
        "std = x.std(axis=0)\n"
        "z = (x - mean) / std\n"
        "print(z.shape)\n"
        "print(np.allclose(z.mean(axis=0), 0.0))",
        "(3, 2)\nTrue",
        (
            "axis=0 reduce las filas y conserva una estadística por columna.",
            "axis=0 reduces rows and keeps one statistic per column.",
            "axis=0 reducerer rækker og bevarer én statistik pr. kolonne.",
        ),
    ),
    (
        "broadcast-centering",
        (
            "Centrado mediante broadcasting",
            "Centering through broadcasting",
            "Centrering med broadcasting",
        ),
        (
            "Resta una media por variable a una matriz de muestras.",
            "Subtract one mean per variable from a sample matrix.",
            "Træk ét middel pr. variabel fra en prøvematrix.",
        ),
        [
            (
                "La matriz tiene forma (n, p).",
                "The matrix has shape (n, p).",
                "Matricen har formen (n, p).",
            ),
            (
                "La media tiene forma (p,).",
                "The mean has shape (p,).",
                "Middelværdien har formen (p,).",
            ),
            (
                "La última dimensión coincide.",
                "The final dimension matches.",
                "Den sidste dimension matcher.",
            ),
        ],
        "import numpy as np\n"
        "\n"
        "x = np.array([[2.0, 5.0], [4.0, 9.0]])\n"
        "centered = x - x.mean(axis=0)\n"
        "print(centered.tolist())",
        "[[-1.0, -2.0], [1.0, 2.0]]",
        (
            "El vector se expande conceptualmente sobre las filas.",
            "The vector conceptually expands across rows.",
            "Vektoren udvides konceptuelt over rækkerne.",
        ),
    ),
    (
        "dataframe-filter",
        (
            "Filtrado explícito de una tabla",
            "Explicit table filtering",
            "Eksplicit filtrering af en tabel",
        ),
        (
            "Selecciona registros válidos y conserva columnas definidas.",
            "Select valid records and keep defined columns.",
            "Vælg gyldige poster og behold definerede kolonner.",
        ),
        [
            ("Construir una máscara booleana.", "Build a Boolean mask.", "Byg en boolesk maske."),
            ("Seleccionar con loc.", "Select with loc.", "Vælg med loc."),
            (
                "Copiar antes de transformar.",
                "Copy before transforming.",
                "Kopiér før transformering.",
            ),
        ],
        "import pandas as pd\n"
        "\n"
        "df = pd.DataFrame({'sample': ['A', 'B', 'C'], 'value': [2.1, None, 4.3]})\n"
        "valid = df.loc[df['value'].notna(), ['sample', 'value']].copy()\n"
        "print(valid['sample'].tolist())",
        "['A', 'C']",
        (
            "La política de ausencia se expresa en la máscara y no convierte NaN en cero.",
            "The missingness policy is explicit in the mask and does not turn NaN into zero.",
            "Politikken for manglende værdier er eksplicit i masken og gør ikke NaN til nul.",
        ),
    ),
    (
        "safe-merge",
        (
            "Unión con validación de cardinalidad",
            "Join with cardinality validation",
            "Sammenføjning med kardinalitetsvalidering",
        ),
        (
            "Une metadatos uno-a-uno y rechaza claves duplicadas.",
            "Join one-to-one metadata and reject duplicate keys.",
            "Sammenføj en-til-en-metadata og afvis dublerede nøgler.",
        ),
        [
            ("Definir la clave.", "Define the key.", "Definér nøglen."),
            (
                "Declarar la cardinalidad esperada.",
                "Declare expected cardinality.",
                "Angiv forventet kardinalitet.",
            ),
            ("Comprobar filas.", "Check rows.", "Kontrollér rækker."),
        ],
        "import pandas as pd\n"
        "\n"
        "left = pd.DataFrame({'sample': ['A', 'B'], 'value': [1.2, 2.3]})\n"
        "right = pd.DataFrame({'sample': ['A', 'B'], 'group': ['x', 'y']})\n"
        "joined = left.merge(right, on='sample', validate='one_to_one')\n"
        "print(joined.shape)",
        "(2, 3)",
        (
            "validate convierte una suposición de cardinalidad en una comprobación ejecutable.",
            "validate turns a cardinality assumption into an executable check.",
            "validate gør en kardinalitetsantagelse til en eksekverbar kontrol.",
        ),
    ),
    (
        "reproducible-plot",
        ("Figura reproducible", "Reproducible figure", "Reproducerbar figur"),
        (
            "Crea una figura con etiquetas y la guarda con tamaño definido.",
            "Create a labeled figure and save it with a defined size.",
            "Opret en mærket figur og gem den med defineret størrelse.",
        ),
        [
            (
                "Crear figure y axes explícitos.",
                "Create figure and axes explicitly.",
                "Opret figure og axes eksplicit.",
            ),
            ("Etiquetar unidades.", "Label units.", "Mærk enheder."),
            ("Cerrar la figura.", "Close the figure.", "Luk figuren."),
        ],
        "import matplotlib.pyplot as plt\n"
        "\n"
        "fig, ax = plt.subplots(figsize=(5, 3))\n"
        "ax.plot([0, 1, 2], [1.0, 1.5, 1.2], marker='o')\n"
        "ax.set_xlabel('Time (h)')\n"
        "ax.set_ylabel('Normalized signal')\n"
        "fig.tight_layout()\n"
        "fig.savefig('signal.png', dpi=150)\n"
        "plt.close(fig)\n"
        "print('signal.png')",
        "signal.png",
        (
            "La creación explícita evita depender del estado global de pyplot.",
            "Explicit creation avoids relying on pyplot global state.",
            "Eksplicit oprettelse undgår afhængighed af pyplots globale tilstand.",
        ),
    ),
)

_PRACTICES = (
    (
        "m13.p01",
        "CODE_TRACING",
        (
            "Indica shape, ndim y size de np.zeros((4, 3, 2)).",
            "State shape, ndim, and size for np.zeros((4, 3, 2)).",
            "Angiv shape, ndim og size for np.zeros((4, 3, 2)).",
        ),
        [("Multiplica las dimensiones.", "Multiply dimensions.", "Multiplicér dimensionerne.")],
        (
            "shape=(4, 3, 2), ndim=3, size=24.",
            "shape=(4, 3, 2), ndim=3, size=24.",
            "shape=(4, 3, 2), ndim=3, size=24.",
        ),
        (
            "ndim cuenta ejes y size cuenta elementos.",
            "ndim counts axes and size counts elements.",
            "ndim tæller akser og size tæller elementer.",
        ),
        "",
    ),
    (
        "m13.p02",
        "FILL_IN_THE_BLANK",
        (
            "Completa la reducción por columnas: x.mean(axis=____).",
            "Complete column-wise reduction: x.mean(axis=____).",
            "Udfyld kolonnevis reduktion: x.mean(axis=____).",
        ),
        [("Las muestras están en filas.", "Samples are rows.", "Prøver er rækker.")],
        ("0", "0", "0"),
        (
            "axis=0 reduce el eje de filas.",
            "axis=0 reduces the row axis.",
            "axis=0 reducerer rækkeaksen.",
        ),
        "",
    ),
    (
        "m13.p03",
        "DEBUGGING",
        (
            "Corrige una resta entre x de forma (5, 3) y mean de forma (5,).",
            "Fix subtraction between x with shape (5, 3) and mean with shape (5,).",
            "Ret subtraktion mellem x med form (5, 3) og mean med form (5,).",
        ),
        [
            (
                "La media por variable debe tener longitud 3.",
                "A per-variable mean must have length 3.",
                "Et middel pr. variabel skal have længde 3.",
            )
        ],
        (
            "Calcular mean = x.mean(axis=0).",
            "Compute mean = x.mean(axis=0).",
            "Beregn mean = x.mean(axis=0).",
        ),
        (
            "La forma (3,) se alinea con la última dimensión.",
            "Shape (3,) aligns with the final dimension.",
            "Formen (3,) justeres med den sidste dimension.",
        ),
        "",
    ),
    (
        "m13.p04",
        "CODE_COMPLETION",
        (
            "Escribe una función que devuelva filas sin valores ausentes en columnas requeridas.",
            "Write a function returning rows without missing values in required columns.",
            "Skriv en funktion der returnerer rækker uden manglende værdier i krævede kolonner.",
        ),
        [("Usa dropna(subset=...).", "Use dropna(subset=...).", "Brug dropna(subset=...).")],
        (
            "def complete_rows(df, required):\n    return df.dropna(subset=required).copy()",
            "def complete_rows(df, required):\n    return df.dropna(subset=required).copy()",
            "def complete_rows(df, required):\n    return df.dropna(subset=required).copy()",
        ),
        (
            "La lista required hace explícita la política.",
            "The required list makes the policy explicit.",
            "Listen required gør politikken eksplicit.",
        ),
        "def complete_rows(df, required):\n    pass",
    ),
    (
        "m13.p05",
        "SHORT_ANSWER",
        (
            "Explica por qué una vista NumPy puede producir cambios inesperados.",
            "Explain why a NumPy view may produce unexpected changes.",
            "Forklar hvorfor et NumPy-view kan give uventede ændringer.",
        ),
        [("Considera memoria compartida.", "Consider shared memory.", "Overvej delt hukommelse.")],
        (
            "Una vista comparte el almacenamiento del array original; mutar la vista puede modificar el "
            "original. copy() crea independencia.",
            "A view shares storage with the original array; mutating the view may modify the original. "
            "copy() creates independence.",
            "Et view deler lagring med det oprindelige array; mutation kan ændre originalen. copy() "
            "skaber uafhængighed.",
        ),
        (
            "La diferencia es semántica y afecta pruebas.",
            "The difference is semantic and affects tests.",
            "Forskellen er semantisk og påvirker test.",
        ),
        "",
    ),
    (
        "m13.p06",
        "DATA_INTERPRETATION",
        (
            "Un merge aumenta 100 filas a 460. Interpreta la señal.",
            "A merge increases 100 rows to 460. Interpret the signal.",
            "En merge øger 100 rækker til 460. Fortolk signalet.",
        ),
        [("Revisa unicidad de claves.", "Check key uniqueness.", "Kontrollér nøglers entydighed.")],
        (
            "Existe una relación muchos-a-muchos o claves duplicadas; debe comprobarse la cardinalidad "
            "antes de aceptar el resultado.",
            "A many-to-many relation or duplicate keys exists; cardinality must be checked before "
            "accepting the result.",
            "Der findes en mange-til-mange-relation eller dublerede nøgler; kardinaliteten skal "
            "kontrolleres.",
        ),
        (
            "El número de filas es una invariante útil.",
            "Row count is a useful invariant.",
            "Antallet af rækker er en nyttig invariant.",
        ),
        "",
    ),
    (
        "m13.p07",
        "ORDERING",
        (
            "Ordena un flujo reproducible: crear entorno, instalar, registrar versiones, ejecutar, "
            "validar.",
            "Order a reproducible workflow: create environment, install, record versions, run, "
            "validate.",
            "Ordén et reproducerbart workflow: opret miljø, installér, registrér versioner, kør, "
            "validér.",
        ),
        [
            (
                "La ejecución ocurre después de preparar dependencias.",
                "Execution follows dependency setup.",
                "Kørsel følger opsætning af afhængigheder.",
            )
        ],
        (
            "Crear entorno → instalar dependencias → registrar versiones → ejecutar análisis → validar "
            "salidas.",
            "Create environment → install dependencies → record versions → run analysis → validate "
            "outputs.",
            "Opret miljø → installér afhængigheder → registrér versioner → kør analyse → validér "
            "output.",
        ),
        (
            "El registro permite reconstruir el contexto.",
            "The record reconstructs context.",
            "Registreringen gør konteksten rekonstruerbar.",
        ),
        "",
    ),
    (
        "m13.p08",
        "CODE_TRACING",
        (
            "Traza df.loc[df['value'] > 0, ['sample']] para tres filas.",
            "Trace df.loc[df['value'] > 0, ['sample']] for three rows.",
            "Gennemgå df.loc[df['value'] > 0, ['sample']] for tre rækker.",
        ),
        [("Primero evalúa la máscara.", "Evaluate the mask first.", "Evaluér masken først.")],
        (
            "Conserva sólo filas con value positivo y devuelve un DataFrame con la columna sample.",
            "It keeps rows with positive value and returns a DataFrame containing sample.",
            "Den beholder kun rækker med positiv value og returnerer en DataFrame med sample.",
        ),
        (
            "Los dobles corchetes conservan estructura tabular.",
            "Double brackets preserve tabular structure.",
            "Dobbelte klammer bevarer tabelstruktur.",
        ),
        "",
    ),
    (
        "m13.p09",
        "PIPELINE_DESIGN",
        (
            "Diseña controles para cargar, limpiar, agrupar y visualizar una tabla.",
            "Design checks for loading, cleaning, grouping, and visualizing a table.",
            "Design kontroller til indlæsning, rensning, gruppering og visualisering af en tabel.",
        ),
        [
            (
                "Incluye esquema y cardinalidad.",
                "Include schema and cardinality.",
                "Medtag schema og kardinalitet.",
            )
        ],
        (
            "Validar columnas y tipos → cuantificar ausentes → aplicar política documentada → verificar "
            "grupos y conteos → generar figura etiquetada → guardar parámetros y versiones.",
            "Validate columns and dtypes → quantify missingness → apply documented policy → verify "
            "groups and counts → generate labeled figure → save parameters and versions.",
            "Validér kolonner og datatyper → kvantificér manglende værdier → anvend dokumenteret "
            "politik → verificér grupper og antal → generér mærket figur → gem parametre og versioner.",
        ),
        (
            "Cada etapa produce controles observables.",
            "Each stage produces observable checks.",
            "Hvert trin producerer observerbare kontroller.",
        ),
        "",
    ),
    (
        "m13.p10",
        "ORAL_EXPLANATION",
        (
            "Explica broadcasting a una persona que conoce listas pero no arrays.",
            "Explain broadcasting to someone who knows lists but not arrays.",
            "Forklar broadcasting til en person der kender lister men ikke arrays.",
        ),
        [
            (
                "Usa dimensiones compatibles.",
                "Use compatible dimensions.",
                "Brug kompatible dimensioner.",
            )
        ],
        (
            "NumPy alinea formas desde la derecha y repite conceptualmente dimensiones de tamaño uno, "
            "sin exigir construir manualmente todas las copias.",
            "NumPy aligns shapes from the right and conceptually repeats size-one dimensions without "
            "requiring manual copies.",
            "NumPy justerer former fra højre og gentager konceptuelt dimensioner på én uden manuelle "
            "kopier.",
        ),
        (
            "Debe mencionarse que compatibilidad no garantiza corrección conceptual.",
            "Mention that compatibility does not guarantee conceptual correctness.",
            "Nævn at kompatibilitet ikke garanterer konceptuel korrekthed.",
        ),
        "",
    ),
    (
        "m13.p11",
        "DEBUGGING",
        (
            "Corrige una figura sin etiquetas ni cierre.",
            "Fix a figure without labels or closure.",
            "Ret en figur uden etiketter eller lukning.",
        ),
        [
            (
                "Usa fig, ax y plt.close(fig).",
                "Use fig, ax, and plt.close(fig).",
                "Brug fig, ax og plt.close(fig).",
            )
        ],
        (
            "Crear fig, ax; dibujar; definir xlabel/ylabel; tight_layout; guardar; cerrar con "
            "plt.close(fig).",
            "Create fig, ax; plot; set xlabel/ylabel; tight_layout; save; close with plt.close(fig).",
            "Opret fig, ax; plot; sæt xlabel/ylabel; tight_layout; gem; luk med plt.close(fig).",
        ),
        (
            "Cerrar evita acumular figuras en procesos repetidos.",
            "Closing avoids accumulating figures in repeated processes.",
            "Lukning undgår ophobning af figurer i gentagne processer.",
        ),
        "",
    ),
    (
        "m13.p12",
        "SHORT_ANSWER",
        (
            "Distingue requisitos, restricciones y archivo de bloqueo.",
            "Distinguish requirements, constraints, and a lock file.",
            "Skeln mellem krav, begrænsninger og en låsefil.",
        ),
        [
            (
                "Piensa en intención frente a resolución exacta.",
                "Think intent versus exact resolution.",
                "Tænk hensigt mod præcis løsning.",
            )
        ],
        (
            "Los requisitos declaran dependencias directas; las restricciones limitan versiones "
            "aceptables; el bloqueo registra una resolución concreta y transitiva.",
            "Requirements declare direct dependencies; constraints limit acceptable versions; a lock "
            "file records a concrete transitive resolution.",
            "Krav deklarerer direkte afhængigheder; begrænsninger afgrænser acceptable versioner; en "
            "låsefil registrerer en konkret transitiv løsning.",
        ),
        (
            "La terminología depende de la herramienta, pero la distinción conceptual es estable.",
            "Tool terminology varies, but the conceptual distinction is stable.",
            "Terminologien varierer, men den konceptuelle forskel er stabil.",
        ),
        "",
    ),
)

LOCALIZED_MODULE_13_SCIENTIFIC_LIBRARIES = LocalizedLearningModule(
    course_code="DM857",
    module_id="dm857.m13",
    title=t(
        *(
            "Bibliotecas, entornos y computación científica",
            "Libraries, environments, and scientific computing",
            "Biblioteker, miljøer og videnskabelig beregning",
        )
    ),
    summary=t(
        *(
            "Este módulo desarrolla el uso responsable de bibliotecas de Python y entornos reproducibles. "
            "Cubre importación, documentación, versiones, entornos virtuales, NumPy, pandas y Matplotlib, "
            "con atención a formas, tipos, valores ausentes, vectorización, selección tabular, "
            "visualización y validación de resultados.",
            "This module develops responsible use of Python libraries and reproducible environments. It "
            "covers imports, documentation, versions, virtual environments, NumPy, pandas, and "
            "Matplotlib, with attention to shapes, dtypes, missing values, vectorization, tabular "
            "selection, visualization, and result validation.",
            "Dette modul udvikler ansvarlig brug af Python-biblioteker og reproducerbare miljøer. Det "
            "dækker imports, dokumentation, versioner, virtuelle miljøer, NumPy, pandas og Matplotlib med "
            "fokus på former, datatyper, manglende værdier, vektorisering, tabeludvælgelse, visualisering "
            "og validering af resultater.",
        )
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
            "dm857.m13.assessment.001",
            ActivityType.MULTIPLE_CHOICE,
            (
                "¿Qué atributo describe las dimensiones de un ndarray?",
                "Which attribute describes ndarray dimensions?",
                "Hvilken attribut beskriver dimensionerne i et ndarray?",
            ),
            (),
            (
                "shape contiene una tupla de dimensiones.",
                "shape contains a tuple of dimensions.",
                "shape indeholder en tuple af dimensioner.",
            ),
            options=(
                ("shape", ("shape", "shape", "shape")),
                ("dtype", ("dtype", "dtype", "dtype")),
                ("size", ("size únicamente", "size only", "kun size")),
            ),
            correct_option_ids=("shape",),
        ),
        authored_item(
            "dm857.m13.assessment.002",
            ActivityType.MULTIPLE_SELECT,
            (
                "Selecciona comprobaciones previas a una operación vectorizada.",
                "Select checks before a vectorized operation.",
                "Vælg kontroller før en vektoriseret operation.",
            ),
            (),
            (
                "Revisar shapes, dtypes, unidades y orientación.",
                "Check shapes, dtypes, units, and orientation.",
                "Kontrollér former, datatyper, enheder og orientering.",
            ),
            options=(
                ("shape", ("Shapes", "Shapes", "Former")),
                ("dtype", ("Dtypes", "Dtypes", "Datatyper")),
                ("units", ("Unidades", "Units", "Enheder")),
                ("orientation", ("Orientación", "Orientation", "Orientering")),
                ("print", ("Sólo imprimir", "Only print", "Kun udskriv")),
            ),
            correct_option_ids=("shape", "dtype", "units", "orientation"),
        ),
        authored_item(
            "dm857.m13.assessment.003",
            ActivityType.DEBUGGING,
            (
                "Un DataFrame se modifica mediante df[df['x'] > 0]['y'] = 1. Corrige el patrón.",
                "A DataFrame is modified with df[df['x'] > 0]['y'] = 1. Fix the pattern.",
                "En DataFrame ændres med df[df['x'] > 0]['y'] = 1. Ret mønstret.",
            ),
            (
                (
                    "Usar df.loc[df['x'] > 0, 'y'] = 1.",
                    "Use df.loc[df['x'] > 0, 'y'] = 1.",
                    "Brug df.loc[df['x'] > 0, 'y'] = 1.",
                ),
            ),
            (
                "loc expresa una única selección y asignación.",
                "loc expresses one selection and assignment.",
                "loc udtrykker én udvælgelse og tildeling.",
            ),
        ),
        authored_item(
            "dm857.m13.assessment.004",
            ActivityType.FILL_IN_THE_BLANK,
            (
                "Completa: np.arange(12).reshape(3, ____).",
                "Complete: np.arange(12).reshape(3, ____).",
                "Udfyld: np.arange(12).reshape(3, ____).",
            ),
            (("4", "4", "4"),),
            (
                "El producto debe ser doce.",
                "The product must be twelve.",
                "Produktet skal være tolv.",
            ),
        ),
        authored_item(
            "dm857.m13.assessment.005",
            ActivityType.MATCHING,
            (
                "Relaciona herramienta y propósito.",
                "Match tool and purpose.",
                "Match værktøj og formål.",
            ),
            (),
            (
                "shape-dimensiones; dtype-representación; loc-etiquetas; iloc-posiciones.",
                "shape-dimensions; dtype-representation; loc-labels; iloc-positions.",
                "shape-dimensioner; dtype-repræsentation; loc-etiketter; iloc-positioner.",
            ),
            options=(
                ("shape", ("shape → dimensiones", "shape → dimensions", "shape → dimensioner")),
                (
                    "dtype",
                    ("dtype → representación", "dtype → representation", "dtype → repræsentation"),
                ),
                ("loc", ("loc → etiquetas", "loc → labels", "loc → etiketter")),
                ("iloc", ("iloc → posiciones", "iloc → positions", "iloc → positioner")),
            ),
            correct_option_ids=("shape", "dtype", "loc", "iloc"),
        ),
        authored_item(
            "dm857.m13.assessment.006",
            ActivityType.ORDERING,
            (
                "Ordena la validación de un merge.",
                "Order merge validation.",
                "Ordén validering af en merge.",
            ),
            (),
            (
                "Definir clave → comprobar unicidad → declarar validate → ejecutar merge → comparar filas.",
                "Define key → check uniqueness → declare validate → run merge → compare rows.",
                "Definér nøgle → kontrollér entydighed → angiv validate → kør merge → sammenlign rækker.",
            ),
            options=(
                ("key", ("Definir clave", "Define key", "Definér nøgle")),
                ("unique", ("Comprobar unicidad", "Check uniqueness", "Kontrollér entydighed")),
                ("validate", ("Declarar validate", "Declare validate", "Angiv validate")),
                ("merge", ("Ejecutar merge", "Run merge", "Kør merge")),
                ("rows", ("Comparar filas", "Compare rows", "Sammenlign rækker")),
            ),
            correct_option_ids=("key", "unique", "validate", "merge", "rows"),
        ),
        authored_item(
            "dm857.m13.assessment.007",
            ActivityType.CODE_COMPLETION,
            (
                "Escribe una función que compruebe que un array es bidimensional y no vacío.",
                "Write a function checking that an array is two-dimensional and non-empty.",
                "Skriv en funktion der kontrollerer at et array er todimensionalt og ikke tomt.",
            ),
            (
                (
                    "def validate_matrix(x):\n"
                    "    if x.ndim != 2:\n"
                    "        raise ValueError('expected 2D array')\n"
                    "    if x.size == 0:\n"
                    "        raise ValueError('array is empty')\n"
                    "    return x",
                    "def validate_matrix(x):\n"
                    "    if x.ndim != 2:\n"
                    "        raise ValueError('expected 2D array')\n"
                    "    if x.size == 0:\n"
                    "        raise ValueError('array is empty')\n"
                    "    return x",
                    "def validate_matrix(x):\n"
                    "    if x.ndim != 2:\n"
                    "        raise ValueError('expected 2D array')\n"
                    "    if x.size == 0:\n"
                    "        raise ValueError('array is empty')\n"
                    "    return x",
                ),
            ),
            (
                "Las comprobaciones convierten supuestos de forma en contrato.",
                "The checks turn shape assumptions into a contract.",
                "Kontrollerne gør formantagelser til en kontrakt.",
            ),
            rubric=(
                ("Comprueba ndim.", "Checks ndim.", "Kontrollerer ndim."),
                ("Rechaza size cero.", "Rejects zero size.", "Afviser size nul."),
            ),
        ),
        authored_item(
            "dm857.m13.assessment.008",
            ActivityType.SHORT_ANSWER,
            (
                "Explica por qué fillna(0) no es una decisión neutral.",
                "Explain why fillna(0) is not a neutral decision.",
                "Forklar hvorfor fillna(0) ikke er en neutral beslutning.",
            ),
            (
                (
                    "Cero añade un valor observado o imputado con significado propio; puede cambiar "
                    "distribuciones, promedios y relaciones. La política debe justificarse por el contexto.",
                    "Zero adds an observed or imputed value with its own meaning; it may change distributions, "
                    "means, and relationships. The policy requires contextual justification.",
                    "Nul tilføjer en observeret eller imputeret værdi med egen betydning og kan ændre "
                    "fordelinger, middelværdier og relationer. Politikken skal begrundes.",
                ),
            ),
            (
                "Ausencia y cero representan estados distintos.",
                "Missingness and zero represent different states.",
                "Manglende værdi og nul repræsenterer forskellige tilstande.",
            ),
        ),
        authored_item(
            "dm857.m13.assessment.009",
            ActivityType.DATA_INTERPRETATION,
            (
                "Un array cambia de dtype int64 a float64 tras introducir NaN. Interpreta el cambio.",
                "An array changes from int64 to float64 after introducing NaN. Interpret the change.",
                "Et array ændrer dtype fra int64 til float64 efter introduktion af NaN. Fortolk ændringen.",
            ),
            (
                (
                    "NaN clásico se representa como punto flotante, por lo que NumPy promueve el dtype. Debe "
                    "evaluarse si esa representación y precisión son aceptables.",
                    "Classic NaN is represented as floating point, so NumPy promotes the dtype. The "
                    "representation and precision should be evaluated.",
                    "Klassisk NaN repræsenteres som flydende tal, så NumPy fremmer datatypen. Repræsentation og "
                    "præcision skal vurderes.",
                ),
            ),
            (
                "El dtype forma parte del resultado y puede afectar memoria y operaciones.",
                "dtype is part of the result and may affect memory and operations.",
                "Datatypen er en del af resultatet og kan påvirke hukommelse og operationer.",
            ),
        ),
        authored_item(
            "dm857.m13.assessment.010",
            ActivityType.ORAL_EXPLANATION,
            (
                "Explica la diferencia entre loc e iloc con un ejemplo.",
                "Explain the difference between loc and iloc with an example.",
                "Forklar forskellen mellem loc og iloc med et eksempel.",
            ),
            (
                (
                    "loc selecciona por etiquetas de índice y columnas; iloc selecciona por posiciones enteras. "
                    "df.loc['A', 'value'] usa etiquetas, mientras df.iloc[0, 1] usa posiciones.",
                    "loc selects by index and column labels; iloc selects by integer positions. df.loc['A', "
                    "'value'] uses labels, while df.iloc[0, 1] uses positions.",
                    "loc vælger efter indeks- og kolonneetiketter; iloc vælger efter heltalspositioner. "
                    "df.loc['A', 'value'] bruger etiketter, mens df.iloc[0, 1] bruger positioner.",
                ),
            ),
            (
                "Confundirlos puede seleccionar datos distintos sin error.",
                "Confusing them may select different data without an error.",
                "Forveksling kan vælge andre data uden fejl.",
            ),
        ),
        authored_item(
            "dm857.m13.assessment.011",
            ActivityType.PIPELINE_DESIGN,
            (
                "Diseña un proceso reproducible para una tabla y una figura final.",
                "Design a reproducible process for a table and final figure.",
                "Design en reproducerbar proces for en tabel og en slutfigur.",
            ),
            (
                (
                    "Definir entorno y versiones → cargar datos inmutables → validar esquema → limpiar con "
                    "política documentada → calcular con controles → visualizar con ejes y unidades → guardar "
                    "datos derivados, figura y metadatos.",
                    "Define environment and versions → load immutable data → validate schema → clean under a "
                    "documented policy → compute with checks → visualize with axes and units → save derived "
                    "data, figure, and metadata.",
                    "Definér miljø og versioner → indlæs uforanderlige data → validér schema → rens efter "
                    "dokumenteret politik → beregn med kontroller → visualisér med akser og enheder → gem "
                    "afledte data, figur og metadata.",
                ),
            ),
            (
                "La reproducibilidad depende tanto del entorno como de las transformaciones.",
                "Reproducibility depends on both environment and transformations.",
                "Reproducerbarhed afhænger af både miljø og transformationer.",
            ),
            rubric=(
                ("Incluye versiones.", "Includes versions.", "Medtager versioner."),
                ("Incluye validaciones.", "Includes validation.", "Medtager validering."),
            ),
        ),
        authored_item(
            "dm857.m13.assessment.012",
            ActivityType.DEBUGGING,
            (
                "Una operación produce shape (100, 100) cuando se esperaba (100,). Diagnostica.",
                "An operation produces shape (100, 100) when (100,) was expected. Diagnose it.",
                "En operation producerer formen (100, 100), men (100,) var forventet. Diagnosticér.",
            ),
            (
                (
                    "Probablemente se combinaron formas (100, 1) y (100,), activando broadcasting exterior. "
                    "Inspeccionar shapes y usar squeeze, reshape o selección coherente según el contrato.",
                    "Shapes (100, 1) and (100,) were probably combined, triggering outer broadcasting. Inspect "
                    "shapes and use squeeze, reshape, or coherent selection according to the contract.",
                    "Formerne (100, 1) og (100,) blev sandsynligvis kombineret og udløste ydre broadcasting. "
                    "Undersøg former og brug squeeze, reshape eller konsistent udvælgelse efter kontrakten.",
                ),
            ),
            (
                "El resultado es válido para NumPy pero incorrecto para la intención.",
                "The result is valid for NumPy but wrong for the intent.",
                "Resultatet er gyldigt for NumPy men forkert for hensigten.",
            ),
        ),
        authored_item(
            "dm857.m13.assessment.013",
            ActivityType.CODE_TRACING,
            (
                "Traza np.array([1, 2, 3]) + np.array([[10], [20]]).",
                "Trace np.array([1, 2, 3]) + np.array([[10], [20]]).",
                "Gennemgå np.array([1, 2, 3]) + np.array([[10], [20]]).",
            ),
            (
                (
                    "Produce [[11, 12, 13], [21, 22, 23]] con forma (2, 3).",
                    "It produces [[11, 12, 13], [21, 22, 23]] with shape (2, 3).",
                    "Det producerer [[11, 12, 13], [21, 22, 23]] med formen (2, 3).",
                ),
            ),
            (
                "Las formas (3,) y (2,1) se expanden a (2,3).",
                "Shapes (3,) and (2,1) expand to (2,3).",
                "Formerne (3,) og (2,1) udvides til (2,3).",
            ),
        ),
        authored_item(
            "dm857.m13.assessment.014",
            ActivityType.SHORT_ANSWER,
            (
                "Justifica cuándo usar una lista de Python en lugar de un ndarray.",
                "Justify when to use a Python list instead of an ndarray.",
                "Begrund hvornår en Python-liste bør bruges frem for et ndarray.",
            ),
            (
                (
                    "Cuando los elementos son heterogéneos, la longitud cambia frecuentemente, no se requieren "
                    "operaciones numéricas vectorizadas o la claridad de una estructura general supera la "
                    "ventaja de almacenamiento homogéneo.",
                    "Use a list when elements are heterogeneous, length changes frequently, vectorized numeric "
                    "operations are unnecessary, or a general structure is clearer than homogeneous storage.",
                    "Brug en liste når elementer er heterogene, længden ændres ofte, vektoriserede numeriske "
                    "operationer ikke er nødvendige, eller en generel struktur er tydeligere end homogen "
                    "lagring.",
                ),
            ),
            (
                "La estructura debe elegirse por operaciones y contrato, no por moda.",
                "Choose the structure by operations and contract, not fashion.",
                "Vælg struktur efter operationer og kontrakt, ikke mode.",
            ),
        ),
    ),
    tutor_support=tutor_support(
        (
            "Las bibliotecas amplían Python mediante módulos y paquetes que exponen una API. Usarlas "
            "correctamente exige distinguir el espacio de nombres importado, leer firmas y documentación, "
            "comprobar tipos y formas de retorno y registrar las versiones que sostienen un resultado. Un "
            "entorno virtual aísla dependencias y evita que instalaciones de otros proyectos cambien el "
            "comportamiento. La reproducibilidad incluye versión de Python, paquetes directos y "
            "transitivos, sistema, semillas aleatorias, datos de entrada y parámetros. NumPy representa "
            "datos numéricos mediante ndarray homogéneos. shape, ndim, size y dtype son parte del "
            "contrato; axis define la dimensión reducida y reshape sólo es válido si conserva el número "
            "de elementos. Las vistas pueden compartir memoria, por lo que una modificación puede "
            "propagarse al array original. La vectorización expresa operaciones sobre arrays completos y "
            "broadcasting alinea dimensiones desde la derecha. Una operación compatible puede seguir "
            "siendo científicamente incorrecta si las muestras, variables o unidades están orientadas de "
            "forma equivocada. pandas organiza datos en Series y DataFrame alineados por índice. loc "
            "selecciona etiquetas e iloc posiciones; los índices pueden representar identidad y causar "
            "alineaciones que introducen valores ausentes. NaN, None y pd.NA requieren una política "
            "explícita. dropna y fillna no son simples detalles técnicos: cambian la población analizada. "
            "groupby modifica la granularidad y merge puede multiplicar filas cuando las claves no son "
            "únicas, por lo que deben comprobarse cardinalidad y conteos. Matplotlib permite crear "
            "figuras reproducibles mediante objetos figure y axes. El tipo de gráfico, los ejes, las "
            "unidades, los límites y la leyenda deben corresponder a la pregunta sin exagerar "
            "diferencias. La validación científica combina gráficos con controles numéricos de forma, "
            "rango, tipos, ausencias, conteos y equivalencia con implementaciones simples. Los ejemplos "
            "biomédicos del módulo son ejercicios didácticos de programación y análisis de datos; no "
            "representan protocolos de laboratorio, criterios diagnósticos ni recomendaciones clínicas.",
            "Libraries extend Python through modules and packages that expose an API. Correct use "
            "requires knowing the imported namespace, reading signatures and documentation, checking "
            "accepted types and return shapes, and recording the versions supporting a result. A virtual "
            "environment isolates dependencies so unrelated projects cannot silently change behavior. "
            "Reproducibility includes the Python version, direct and transitive packages, platform, "
            "random seeds, input data, and parameters. NumPy represents numeric data with homogeneous "
            "ndarray objects. shape, ndim, size, and dtype are contractual properties; axis identifies "
            "the reduced dimension and reshape is valid only when element count is preserved. Views may "
            "share memory, so mutation can propagate to the original array. Vectorization expresses "
            "operations over complete arrays and broadcasting aligns dimensions from the right. A "
            "compatible operation may still be scientifically wrong when samples, variables, or units are "
            "oriented incorrectly. pandas organizes data as index-aligned Series and DataFrame objects. "
            "loc selects labels and iloc positions; indexes may represent identity and alignment may "
            "introduce missing values. NaN, None, and pd.NA require an explicit policy. dropna and fillna "
            "change the analyzed population. groupby changes granularity and merge may multiply rows when "
            "keys are not unique, so cardinality and counts must be checked. Matplotlib supports "
            "reproducible figures through explicit figure and axes objects. Plot type, axes, units, "
            "limits, and legend should match the question without exaggerating differences. Scientific "
            "validation combines plots with numeric checks of shape, range, dtypes, missingness, counts, "
            "and equivalence to simple implementations. Biomedical examples in this module are "
            "programming and data-analysis exercises; they are not laboratory protocols, diagnostic "
            "criteria, or clinical recommendations.",
            "Biblioteker udvider Python gennem moduler og pakker der eksponerer en API. Korrekt brug "
            "kræver kendskab til det importerede namespace, læsning af signaturer og dokumentation, "
            "kontrol af accepterede typer og returformer samt registrering af versioner. Et virtuelt "
            "miljø isolerer afhængigheder, så andre projekter ikke lydløst ændrer adfærd. "
            "Reproducerbarhed omfatter Python-version, direkte og transitive pakker, platform, tilfældige "
            "seeds, inputdata og parametre. NumPy repræsenterer numeriske data med homogene "
            "ndarray-objekter. shape, ndim, size og dtype er kontraktlige egenskaber; axis angiver "
            "reduktionsdimensionen, og reshape er kun gyldig når antallet af elementer bevares. Views kan "
            "dele hukommelse, så mutation kan påvirke originalen. Vektorisering udtrykker operationer "
            "over hele arrays, og broadcasting justerer dimensioner fra højre. En kompatibel operation "
            "kan stadig være videnskabeligt forkert hvis prøver, variable eller enheder er orienteret "
            "forkert. pandas organiserer data i Series og DataFrame justeret efter indeks. loc vælger "
            "etiketter og iloc positioner; indeks kan repræsentere identitet og justering kan introducere "
            "manglende værdier. NaN, None og pd.NA kræver en eksplicit politik. groupby ændrer "
            "granularitet, og merge kan mangedoble rækker ved ikke-entydige nøgler. Matplotlib "
            "understøtter reproducerbare figurer med eksplicitte figure- og axes-objekter. Validering "
            "kombinerer plots med numeriske kontroller af form, interval, datatyper, manglende værdier og "
            "antal. Biomedicinske eksempler er programmerings- og dataanalyseøvelser; de er ikke "
            "laboratorieprotokoller, diagnostiske kriterier eller kliniske anbefalinger.",
        ),
        (
            (
                "Un import vincula nombres dentro de un espacio de nombres.",
                "An import binds names inside a namespace.",
                "En import binder navne i et namespace.",
            ),
            (
                "La API pública documentada es el contrato estable esperado.",
                "The documented public API is the expected stable contract.",
                "Den dokumenterede offentlige API er den forventede stabile kontrakt.",
            ),
            (
                "Un entorno virtual aísla dependencias por proyecto.",
                "A virtual environment isolates dependencies per project.",
                "Et virtuelt miljø isolerer afhængigheder pr. projekt.",
            ),
            (
                "La reproducibilidad incluye versiones, datos y parámetros.",
                "Reproducibility includes versions, data, and parameters.",
                "Reproducerbarhed omfatter versioner, data og parametre.",
            ),
            (
                "shape, ndim, size y dtype describen un ndarray.",
                "shape, ndim, size, and dtype describe an ndarray.",
                "shape, ndim, size og dtype beskriver et ndarray.",
            ),
            (
                "axis determina la dimensión reducida.",
                "axis determines the reduced dimension.",
                "axis bestemmer reduktionsdimensionen.",
            ),
            (
                "Una vista puede compartir memoria con el array original.",
                "A view may share memory with the original array.",
                "Et view kan dele hukommelse med det oprindelige array.",
            ),
            (
                "Broadcasting alinea dimensiones desde la derecha.",
                "Broadcasting aligns dimensions from the right.",
                "Broadcasting justerer dimensioner fra højre.",
            ),
            (
                "Compatibilidad de formas no garantiza corrección semántica.",
                "Shape compatibility does not guarantee semantic correctness.",
                "Formkompatibilitet garanterer ikke semantisk korrekthed.",
            ),
            (
                "loc usa etiquetas e iloc posiciones.",
                "loc uses labels and iloc positions.",
                "loc bruger etiketter og iloc positioner.",
            ),
            (
                "La alineación por índice puede introducir ausencias.",
                "Index alignment may introduce missingness.",
                "Indeksjustering kan introducere manglende værdier.",
            ),
            (
                "merge debe validar cardinalidad y conteos.",
                "merge should validate cardinality and counts.",
                "merge bør validere kardinalitet og antal.",
            ),
            (
                "Una figura necesita ejes, unidades y límites honestos.",
                "A figure needs honest axes, units, and limits.",
                "En figur behøver ærlige akser, enheder og grænser.",
            ),
            (
                "Los gráficos deben acompañarse de controles numéricos.",
                "Plots should be paired with numeric checks.",
                "Plots bør ledsages af numeriske kontroller.",
            ),
        ),
        (
            (
                "Suponer que import * mejora la claridad.",
                "Assuming import * improves clarity.",
                "At antage at import * forbedrer klarhed.",
            ),
            (
                "Confundir el entorno global con el entorno del proyecto.",
                "Confusing the global environment with the project environment.",
                "At forveksle globalt miljø med projektmiljø.",
            ),
            (
                "Creer que fijar ninguna versión es reproducible.",
                "Believing no version constraints are reproducible.",
                "At tro at ingen versionsbegrænsninger er reproducerbare.",
            ),
            (
                "Ignorar dtype porque los valores se ven correctos.",
                "Ignoring dtype because values look correct.",
                "At ignorere dtype fordi værdierne ser korrekte ud.",
            ),
            (
                "Confundir axis=0 y axis=1.",
                "Confusing axis=0 and axis=1.",
                "At forveksle axis=0 og axis=1.",
            ),
            (
                "Suponer que reshape copia siempre los datos.",
                "Assuming reshape always copies data.",
                "At antage at reshape altid kopierer data.",
            ),
            (
                "Aceptar cualquier broadcasting que no lance error.",
                "Accepting any broadcasting that raises no error.",
                "At acceptere broadcasting blot fordi der ikke opstår fejl.",
            ),
            (
                "Usar loc e iloc como sinónimos.",
                "Using loc and iloc as synonyms.",
                "At bruge loc og iloc som synonymer.",
            ),
            ("Tratar NaN como cero.", "Treating NaN as zero.", "At behandle NaN som nul."),
            (
                "Hacer merge sin revisar claves duplicadas.",
                "Merging without checking duplicate keys.",
                "At merge uden at kontrollere dublerede nøgler.",
            ),
            (
                "Creer que una figura sustituye la validación numérica.",
                "Believing a figure replaces numeric validation.",
                "At tro at en figur erstatter numerisk validering.",
            ),
            (
                "Usar ejes truncados para magnificar diferencias.",
                "Using truncated axes to magnify differences.",
                "At bruge afkortede akser til at forstørre forskelle.",
            ),
        ),
        (
            (
                "¿Qué nombre introduce exactamente este import?",
                "Which exact name does this import introduce?",
                "Hvilket præcist navn introducerer denne import?",
            ),
            (
                "¿Qué versión y entorno produjeron el resultado?",
                "Which version and environment produced the result?",
                "Hvilken version og hvilket miljø producerede resultatet?",
            ),
            (
                "¿Qué shape y dtype esperas antes de calcular?",
                "Which shape and dtype do you expect before computing?",
                "Hvilken shape og dtype forventer du før beregning?",
            ),
            (
                "¿Qué eje representa muestras y cuál variables?",
                "Which axis represents samples and which variables?",
                "Hvilken akse repræsenterer prøver og hvilken variable?",
            ),
            (
                "¿Las formas son compatibles por intención o por accidente?",
                "Are the shapes compatible by intent or accident?",
                "Er formerne kompatible med vilje eller ved et tilfælde?",
            ),
            (
                "¿Esta selección usa etiquetas o posiciones?",
                "Does this selection use labels or positions?",
                "Bruger denne udvælgelse etiketter eller positioner?",
            ),
            (
                "¿Qué significa un valor ausente en este conjunto?",
                "What does a missing value mean in this dataset?",
                "Hvad betyder en manglende værdi i dette datasæt?",
            ),
            (
                "¿Las claves del merge son únicas en ambos lados?",
                "Are merge keys unique on both sides?",
                "Er merge-nøglerne entydige på begge sider?",
            ),
            (
                "¿Cómo cambió el número de filas tras la transformación?",
                "How did row count change after the transformation?",
                "Hvordan ændrede antallet af rækker sig efter transformationen?",
            ),
            (
                "¿Qué tipo de gráfico responde a la pregunta?",
                "Which plot type answers the question?",
                "Hvilken plottype besvarer spørgsmålet?",
            ),
            (
                "¿Las unidades y límites de los ejes están explícitos?",
                "Are axis units and limits explicit?",
                "Er akseenheder og grænser eksplicitte?",
            ),
            (
                "¿Qué control simple podría detectar un resultado erróneo?",
                "Which simple check could detect a wrong result?",
                "Hvilken enkel kontrol kunne opdage et forkert resultat?",
            ),
        ),
        (
            (
                "Usa imports explícitos y legibles.",
                "Uses explicit readable imports.",
                "Bruger eksplicitte læsbare imports.",
            ),
            (
                "Registra entorno y versiones.",
                "Records environment and versions.",
                "Registrerer miljø og versioner.",
            ),
            ("Comprueba shape y dtype.", "Checks shape and dtype.", "Kontrollerer shape og dtype."),
            (
                "Interpreta axis correctamente.",
                "Interprets axis correctly.",
                "Fortolker axis korrekt.",
            ),
            ("Justifica broadcasting.", "Justifies broadcasting.", "Begrunder broadcasting."),
            ("Distingue loc e iloc.", "Distinguishes loc and iloc.", "Skelner mellem loc og iloc."),
            (
                "Define una política de ausencias.",
                "Defines a missing-data policy.",
                "Definerer en politik for manglende data.",
            ),
            (
                "Valida cardinalidad de joins.",
                "Validates join cardinality.",
                "Validerer join-kardinalitet.",
            ),
            (
                "Construye figuras honestas y etiquetadas.",
                "Builds honest labeled figures.",
                "Bygger ærlige mærkede figurer.",
            ),
            (
                "Acompaña resultados con controles numéricos.",
                "Pairs results with numeric checks.",
                "Ledsager resultater med numeriske kontroller.",
            ),
        ),
        (
            (
                "No inventar APIs ni parámetros que no estén documentados.",
                "Do not invent undocumented APIs or parameters.",
                "Opfind ikke udokumenterede API'er eller parametre.",
            ),
            (
                "No asumir que broadcasting válido es científicamente correcto.",
                "Do not assume valid broadcasting is scientifically correct.",
                "Antag ikke at gyldig broadcasting er videnskabeligt korrekt.",
            ),
            (
                "No tratar ausencias como cero sin justificación.",
                "Do not treat missing values as zero without justification.",
                "Behandl ikke manglende værdier som nul uden begrundelse.",
            ),
            (
                "No aceptar merges sin revisar cardinalidad.",
                "Do not accept merges without checking cardinality.",
                "Accepter ikke merges uden at kontrollere kardinalitet.",
            ),
            (
                "No usar gráficos para ocultar escala o variabilidad.",
                "Do not use plots to hide scale or variability.",
                "Brug ikke plots til at skjule skala eller variation.",
            ),
            (
                "Dar pistas antes de soluciones completas.",
                "Give hints before full solutions.",
                "Giv ledetråde før fulde løsninger.",
            ),
            (
                "Separar corrección técnica de interpretación científica.",
                "Separate technical correctness from scientific interpretation.",
                "Adskil teknisk korrekthed fra videnskabelig fortolkning.",
            ),
            (
                "Mantener ejemplos biomédicos como ejercicios didácticos.",
                "Keep biomedical examples as teaching exercises.",
                "Bevar biomedicinske eksempler som undervisningsøvelser.",
            ),
            (
                "Indicar incertidumbre cuando falte contexto.",
                "State uncertainty when context is missing.",
                "Angiv usikkerhed når kontekst mangler.",
            ),
        ),
        (
            "Guttag, Introduction to Computation and Programming Using Python, 3rd ed.",
            "Python documentation: modules, venv, and package management foundations.",
            "NumPy, pandas, and Matplotlib official documentation.",
        ),
    ),
)

_OBJECTIVE_MCQS = (
    (
        "001",
        (
            "¿Qué evita colisiones de nombres con mayor claridad?",
            "What most clearly avoids name collisions?",
            "Hvad undgår tydeligst navnekollisioner?",
        ),
        [
            (
                "module",
                (
                    "import statistics y statistics.mean",
                    "import statistics and statistics.mean",
                    "import statistics og statistics.mean",
                ),
            ),
            (
                "star",
                (
                    "from statistics import *",
                    "from statistics import *",
                    "from statistics import *",
                ),
            ),
            (
                "global",
                (
                    "Copiar funciones al ámbito global",
                    "Copy functions to global scope",
                    "Kopiér funktioner til globalt scope",
                ),
            ),
        ],
        "module",
        (
            "El prefijo conserva procedencia.",
            "The prefix preserves provenance.",
            "Præfikset bevarer oprindelsen.",
        ),
    ),
    (
        "002",
        (
            "¿Qué propiedad informa la representación numérica?",
            "Which property reports numeric representation?",
            "Hvilken egenskab angiver numerisk repræsentation?",
        ),
        [
            ("dtype", ("dtype", "dtype", "dtype")),
            ("shape", ("shape", "shape", "shape")),
            ("ndim", ("ndim", "ndim", "ndim")),
        ],
        "dtype",
        (
            "dtype describe el tipo almacenado.",
            "dtype describes the stored type.",
            "dtype beskriver den lagrede type.",
        ),
    ),
    (
        "003",
        ("¿Qué conserva reshape?", "What does reshape preserve?", "Hvad bevarer reshape?"),
        [
            ("size", ("Número de elementos", "Element count", "Antal elementer")),
            ("axis", ("Nombre del eje", "Axis name", "Aksenavn")),
            (
                "dtype_change",
                (
                    "Cambio obligatorio de dtype",
                    "Mandatory dtype change",
                    "Obligatorisk dtype-ændring",
                ),
            ),
        ],
        "size",
        (
            "El producto de dimensiones debe coincidir.",
            "Dimension products must match.",
            "Produktet af dimensioner skal matche.",
        ),
    ),
    (
        "004",
        (
            "¿Desde qué lado alinea broadcasting?",
            "From which side does broadcasting align?",
            "Fra hvilken side justerer broadcasting?",
        ),
        [
            ("right", ("Desde la derecha", "From the right", "Fra højre")),
            ("left", ("Desde la izquierda", "From the left", "Fra venstre")),
            ("random", ("De forma aleatoria", "Randomly", "Tilfældigt")),
        ],
        "right",
        (
            "Las dimensiones finales se comparan primero.",
            "Trailing dimensions are compared first.",
            "De sidste dimensioner sammenlignes først.",
        ),
    ),
    (
        "005",
        (
            "¿Qué selector usa etiquetas?",
            "Which selector uses labels?",
            "Hvilken vælger bruger etiketter?",
        ),
        [
            ("loc", ("loc", "loc", "loc")),
            ("iloc", ("iloc", "iloc", "iloc")),
            ("shape", ("shape", "shape", "shape")),
        ],
        "loc",
        ("loc opera por etiquetas.", "loc operates by labels.", "loc arbejder med etiketter."),
    ),
    (
        "006",
        (
            "¿Qué selector usa posiciones enteras?",
            "Which selector uses integer positions?",
            "Hvilken vælger bruger heltalspositioner?",
        ),
        [
            ("iloc", ("iloc", "iloc", "iloc")),
            ("loc", ("loc", "loc", "loc")),
            ("merge", ("merge", "merge", "merge")),
        ],
        "iloc",
        ("iloc opera por posición.", "iloc operates by position.", "iloc arbejder med position."),
    ),
    (
        "007",
        (
            "¿Qué función detecta ausencias en pandas?",
            "Which function detects missing values in pandas?",
            "Hvilken funktion opdager manglende værdier i pandas?",
        ),
        [
            ("isna", ("isna", "isna", "isna")),
            ("astype", ("astype", "astype", "astype")),
            ("sort", ("sort_values", "sort_values", "sort_values")),
        ],
        "isna",
        (
            "isna produce una máscara booleana.",
            "isna produces a Boolean mask.",
            "isna producerer en boolesk maske.",
        ),
    ),
    (
        "008",
        (
            "¿Qué argumento valida una unión uno-a-uno?",
            "Which argument validates a one-to-one join?",
            "Hvilket argument validerer en en-til-en-sammenføjning?",
        ),
        [
            (
                "validate",
                ("validate='one_to_one'", "validate='one_to_one'", "validate='one_to_one'"),
            ),
            ("axis", ("axis=1", "axis=1", "axis=1")),
            ("dtype", ("dtype='object'", "dtype='object'", "dtype='object'")),
        ],
        "validate",
        (
            "La cardinalidad se comprueba durante merge.",
            "Cardinality is checked during merge.",
            "Kardinalitet kontrolleres under merge.",
        ),
    ),
    (
        "009",
        (
            "¿Qué estructura almacena valores homogéneos n-dimensionales?",
            "Which structure stores homogeneous n-dimensional values?",
            "Hvilken struktur lagrer homogene n-dimensionale værdier?",
        ),
        [
            ("ndarray", ("ndarray", "ndarray", "ndarray")),
            ("dict", ("dict", "dict", "dict")),
            ("set", ("set", "set", "set")),
        ],
        "ndarray",
        (
            "ndarray es la estructura central de NumPy.",
            "ndarray is NumPy's core structure.",
            "ndarray er NumPys centrale struktur.",
        ),
    ),
    (
        "010",
        (
            "¿Qué opción crea listas independientes en dataclasses?",
            "Which option creates independent lists in dataclasses?",
            "Hvilken mulighed opretter uafhængige lister i dataclasses?",
        ),
        [
            ("factory", ("default_factory=list", "default_factory=list", "default_factory=list")),
            ("default", ("items=[]", "items=[]", "items=[]")),
            ("none", ("No declarar campo", "Do not declare a field", "Deklarér ikke et felt")),
        ],
        "factory",
        (
            "La fábrica se ejecuta por instancia.",
            "The factory runs per instance.",
            "Fabrikken kører pr. instans.",
        ),
    ),
    (
        "011",
        (
            "¿Qué gráfico suele representar una relación entre dos variables continuas?",
            "Which plot usually represents a relationship between two continuous variables?",
            "Hvilket plot repræsenterer normalt en relation mellem to kontinuerte variable?",
        ),
        [
            ("scatter", ("Dispersión", "Scatter", "Spredning")),
            ("pie", ("Circular", "Pie", "Cirkeldiagram")),
            ("table", ("Sólo tabla", "Table only", "Kun tabel")),
        ],
        "scatter",
        (
            "La dispersión muestra pares de observaciones.",
            "Scatter shows observation pairs.",
            "Spredning viser observationspar.",
        ),
    ),
    (
        "012",
        (
            "¿Qué objeto de Matplotlib representa el área de dibujo?",
            "Which Matplotlib object represents the plotting area?",
            "Hvilket Matplotlib-objekt repræsenterer tegneområdet?",
        ),
        [
            ("axes", ("Axes", "Axes", "Axes")),
            ("dtype", ("dtype", "dtype", "dtype")),
            ("series", ("Series", "Series", "Series")),
        ],
        "axes",
        (
            "Axes contiene ejes y artistas.",
            "Axes contains axes and artists.",
            "Axes indeholder akser og artists.",
        ),
    ),
    (
        "013",
        (
            "¿Qué debe registrarse para reproducir un entorno?",
            "What should be recorded to reproduce an environment?",
            "Hvad bør registreres for at reproducere et miljø?",
        ),
        [
            (
                "versions",
                (
                    "Python y versiones de paquetes",
                    "Python and package versions",
                    "Python- og pakkeversioner",
                ),
            ),
            ("screen", ("Sólo una captura", "Only a screenshot", "Kun et skærmbillede")),
            ("memory", ("Sólo RAM total", "Only total RAM", "Kun samlet RAM")),
        ],
        "versions",
        (
            "Las versiones afectan APIs y resultados.",
            "Versions affect APIs and results.",
            "Versioner påvirker API'er og resultater.",
        ),
    ),
    (
        "014",
        (
            "¿Qué puede introducir alineación por índice?",
            "What may index alignment introduce?",
            "Hvad kan indeksjustering introducere?",
        ),
        [
            ("missing", ("Valores ausentes", "Missing values", "Manglende værdier")),
            (
                "syntax",
                ("Errores de sintaxis siempre", "Always syntax errors", "Altid syntaksfejl"),
            ),
            ("imports", ("Nuevos imports", "New imports", "Nye imports")),
        ],
        "missing",
        (
            "Etiquetas no coincidentes producen ausencias.",
            "Mismatched labels produce missingness.",
            "Ikke-matchende etiketter producerer manglende værdier.",
        ),
    ),
    (
        "015",
        (
            "¿Qué operación reduce por columnas si las muestras son filas?",
            "Which operation reduces by columns when samples are rows?",
            "Hvilken operation reducerer pr. kolonne når prøver er rækker?",
        ),
        [
            ("axis0", ("axis=0", "axis=0", "axis=0")),
            ("axis1", ("axis=1", "axis=1", "axis=1")),
            ("none", ("Sin axis siempre", "Always without axis", "Altid uden axis")),
        ],
        "axis0",
        ("Se reduce el eje de filas.", "The row axis is reduced.", "Rækkeaksen reduceres."),
    ),
    (
        "016",
        (
            "¿Qué crea independencia de memoria explícita?",
            "What explicitly creates memory independence?",
            "Hvad skaber eksplicit hukommelsesuafhængighed?",
        ),
        [
            ("copy", ("copy()", "copy()", "copy()")),
            ("view", ("view()", "view()", "view()")),
            ("reshape", ("reshape siempre", "reshape always", "reshape altid")),
        ],
        "copy",
        (
            "copy crea almacenamiento independiente.",
            "copy creates independent storage.",
            "copy skaber uafhængig lagring.",
        ),
    ),
    (
        "017",
        (
            "¿Qué método agrupa y agrega datos tabulares?",
            "Which method groups and aggregates tabular data?",
            "Hvilken metode grupperer og aggregerer tabeldata?",
        ),
        [
            ("groupby", ("groupby", "groupby", "groupby")),
            ("reshape", ("reshape", "reshape", "reshape")),
            ("import", ("import", "import", "import")),
        ],
        "groupby",
        (
            "groupby aplica dividir-aplicar-combinar.",
            "groupby applies split-apply-combine.",
            "groupby anvender opdel-anvend-kombinér.",
        ),
    ),
    (
        "018",
        (
            "¿Qué debe comprobarse tras una transformación tabular?",
            "What should be checked after a table transformation?",
            "Hvad bør kontrolleres efter en tabeltransformation?",
        ),
        [
            (
                "counts",
                (
                    "Filas, columnas y tipos",
                    "Rows, columns, and dtypes",
                    "Rækker, kolonner og datatyper",
                ),
            ),
            ("font", ("Sólo la fuente", "Only the font", "Kun skrifttypen")),
            ("screen", ("Sólo tamaño de pantalla", "Only screen size", "Kun skærmstørrelse")),
        ],
        "counts",
        (
            "Los invariantes estructurales detectan errores.",
            "Structural invariants detect errors.",
            "Strukturelle invarianter opdager fejl.",
        ),
    ),
    (
        "019",
        (
            "¿Qué comando muestra ayuda interactiva de un objeto?",
            "Which command shows interactive help for an object?",
            "Hvilken kommando viser interaktiv hjælp til et objekt?",
        ),
        [
            ("help", ("help(obj)", "help(obj)", "help(obj)")),
            ("len", ("len(obj)", "len(obj)", "len(obj)")),
            ("repr", ("repr(obj)", "repr(obj)", "repr(obj)")),
        ],
        "help",
        (
            "help consulta documentación disponible.",
            "help consults available documentation.",
            "help viser tilgængelig dokumentation.",
        ),
    ),
    (
        "020",
        (
            "¿Qué completa una figura reproducible?",
            "What completes a reproducible figure?",
            "Hvad fuldender en reproducerbar figur?",
        ),
        [
            (
                "metadata",
                (
                    "Datos, parámetros, etiquetas y versión",
                    "Data, parameters, labels, and version",
                    "Data, parametre, etiketter og version",
                ),
            ),
            (
                "color",
                ("Sólo colores atractivos", "Only attractive colors", "Kun attraktive farver"),
            ),
            ("title", ("Sólo un título", "Only a title", "Kun en titel")),
        ],
        "metadata",
        (
            "La figura necesita contexto y procedencia.",
            "The figure needs context and provenance.",
            "Figuren behøver kontekst og proveniens.",
        ),
    ),
)

_OBJECTIVE_TFS = (
    (
        "021",
        (
            "Un ndarray tiene dtype homogéneo.",
            "An ndarray has a homogeneous dtype.",
            "Et ndarray har en homogen datatype.",
        ),
        True,
        (
            "Los elementos comparten representación.",
            "Elements share a representation.",
            "Elementer deler en repræsentation.",
        ),
    ),
    (
        "022",
        (
            "Broadcasting compara dimensiones desde la izquierda.",
            "Broadcasting compares dimensions from the left.",
            "Broadcasting sammenligner dimensioner fra venstre.",
        ),
        False,
        (
            "Las compara desde la derecha.",
            "It compares from the right.",
            "Det sammenligner fra højre.",
        ),
    ),
    (
        "023",
        ("loc selecciona por etiquetas.", "loc selects by labels.", "loc vælger efter etiketter."),
        True,
        (
            "El contrato de loc es basado en etiquetas.",
            "loc is label-based.",
            "loc er etiketbaseret.",
        ),
    ),
    (
        "024",
        (
            "iloc selecciona por etiquetas textuales.",
            "iloc selects by text labels.",
            "iloc vælger efter tekstetiketter.",
        ),
        False,
        (
            "iloc usa posiciones enteras.",
            "iloc uses integer positions.",
            "iloc bruger heltalspositioner.",
        ),
    ),
    (
        "025",
        (
            "fillna(0) siempre es neutral.",
            "fillna(0) is always neutral.",
            "fillna(0) er altid neutral.",
        ),
        False,
        (
            "La imputación cambia los datos y requiere justificación.",
            "Imputation changes data and requires justification.",
            "Imputation ændrer data og kræver begrundelse.",
        ),
    ),
    (
        "026",
        (
            "merge puede multiplicar filas.",
            "merge may multiply rows.",
            "merge kan mangedoble rækker.",
        ),
        True,
        (
            "Ocurre con claves repetidas y relaciones muchos-a-muchos.",
            "It occurs with repeated keys and many-to-many relations.",
            "Det sker ved gentagne nøgler og mange-til-mange-relationer.",
        ),
    ),
    (
        "027",
        (
            "Una vista NumPy puede compartir memoria.",
            "A NumPy view may share memory.",
            "Et NumPy-view kan dele hukommelse.",
        ),
        True,
        (
            "Por eso la mutación puede propagarse.",
            "Therefore mutation may propagate.",
            "Derfor kan mutation sprede sig.",
        ),
    ),
    (
        "028",
        (
            "Un gráfico sustituye las comprobaciones numéricas.",
            "A plot replaces numeric checks.",
            "Et plot erstatter numeriske kontroller.",
        ),
        False,
        (
            "Ambos tipos de evidencia se complementan.",
            "Both evidence types complement each other.",
            "Begge evidenstyper supplerer hinanden.",
        ),
    ),
    (
        "029",
        (
            "Un entorno virtual ayuda a aislar dependencias.",
            "A virtual environment helps isolate dependencies.",
            "Et virtuelt miljø hjælper med at isolere afhængigheder.",
        ),
        True,
        (
            "Cada proyecto puede resolver su propio conjunto.",
            "Each project can resolve its own set.",
            "Hvert projekt kan løse sit eget sæt.",
        ),
    ),
    (
        "030",
        (
            "La compatibilidad de shapes garantiza significado correcto.",
            "Shape compatibility guarantees correct meaning.",
            "Formkompatibilitet garanterer korrekt betydning.",
        ),
        False,
        (
            "La semántica de ejes y unidades debe validarse.",
            "Axis and unit semantics must be validated.",
            "Semantik for akser og enheder skal valideres.",
        ),
    ),
)

LOCALIZED_OBJECTIVE_QUESTION_BANK_13 = tuple(
    objective_mcq(f"dm857.m13.bank.{suffix}", prompt, options, correct_option_id, explanation)
    for suffix, prompt, options, correct_option_id, explanation in _OBJECTIVE_MCQS
) + tuple(
    objective_tf(
        f"dm857.m13.bank.{suffix}",
        prompt,
        correct=correct,
        explanation=explanation,
    )
    for suffix, prompt, correct, explanation in _OBJECTIVE_TFS
)


def materialize_module_13_question_bank(
    locale: AppLocale | str = AppLocale.SPANISH_SPAIN,
) -> tuple[AssessmentItem, ...]:
    """Materialize the stable objective bank in one supported locale."""
    resolved = locale if isinstance(locale, AppLocale) else AppLocale.resolve(locale)
    return tuple(item.materialize(resolved) for item in LOCALIZED_OBJECTIVE_QUESTION_BANK_13)


MODULE_13_SCIENTIFIC_LIBRARIES: LearningModule = (
    LOCALIZED_MODULE_13_SCIENTIFIC_LIBRARIES.materialize(AppLocale.SPANISH_SPAIN)
)
OBJECTIVE_QUESTION_BANK_13 = materialize_module_13_question_bank()

__all__ = [
    "LOCALIZED_MODULE_13_SCIENTIFIC_LIBRARIES",
    "LOCALIZED_OBJECTIVE_QUESTION_BANK_13",
    "MODULE_13_SCIENTIFIC_LIBRARIES",
    "OBJECTIVE_QUESTION_BANK_13",
    "materialize_module_13_question_bank",
]
