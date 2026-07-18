"""DM857 module 7: dictionaries, sets, grouping, and structure selection."""

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

LOCALIZED_MODULE_07_MAPPINGS_SETS = LocalizedLearningModule(
    course_code="DM857",
    module_id="dm857.m07",
    title=t(
        "Diccionarios, conjuntos y organización de datos",
        "Dictionaries, sets, and data organization",
        "Ordbøger, mængder og dataorganisering",
    ),
    summary=t(
        "Este módulo desarrolla el uso razonado de diccionarios y conjuntos para representar asociaciones, contar, agrupar, eliminar duplicados y comparar colecciones. También cubre acceso seguro, claves válidas, recorridos, estructuras anidadas, operaciones de conjuntos, selección de estructura y pruebas de contratos.",
        "This module develops reasoned use of dictionaries and sets for associations, counting, grouping, deduplication, and collection comparison. It also covers safe access, valid keys, traversal, nested structures, set operations, structure selection, and contract testing.",
        "Dette modul udvikler velbegrundet brug af ordbøger og mængder til relationer, optælling, gruppering, deduplikering og sammenligning af samlinger. Det dækker også sikker adgang, gyldige nøgler, gennemløb, indlejrede strukturer, mængdeoperationer, strukturvalg og kontrakttest.",
    ),
    objectives=(
        objective(
            "m07.o1",
            (
                "Crear diccionarios con claves únicas y valores adecuados.",
                "Create dictionaries with unique keys and suitable values.",
                "Oprette ordbøger med unikke nøgler og passende værdier.",
            ),
        ),
        objective(
            "m07.o2",
            (
                "Acceder, actualizar y eliminar entradas de forma segura.",
                "Access, update, and remove entries safely.",
                "Tilgå, opdatere og fjerne poster sikkert.",
            ),
        ),
        objective(
            "m07.o3",
            (
                "Recorrer claves, valores y pares sin depender de un orden accidental.",
                "Traverse keys, values, and pairs without relying on accidental order.",
                "Gennemløbe nøgler, værdier og par uden at afhænge af tilfældig rækkefølge.",
            ),
        ),
        objective(
            "m07.o4",
            (
                "Construir tablas de frecuencia y agrupaciones.",
                "Build frequency tables and groupings.",
                "Bygge frekvenstabeller og grupperinger.",
            ),
        ),
        objective(
            "m07.o5",
            (
                "Diseñar y validar diccionarios anidados.",
                "Design and validate nested dictionaries.",
                "Designe og validere indlejrede ordbøger.",
            ),
        ),
        objective(
            "m07.o6",
            (
                "Usar conjuntos para unicidad y pertenencia eficiente.",
                "Use sets for uniqueness and efficient membership.",
                "Bruge mængder til entydighed og effektiv medlemskabstest.",
            ),
        ),
        objective(
            "m07.o7",
            (
                "Aplicar unión, intersección, diferencia y diferencia simétrica.",
                "Apply union, intersection, difference, and symmetric difference.",
                "Anvende union, snit, differens og symmetrisk differens.",
            ),
        ),
        objective(
            "m07.o8",
            (
                "Elegir entre lista, tupla, diccionario y conjunto mediante contratos y pruebas.",
                "Choose among list, tuple, dictionary, and set through contracts and tests.",
                "Vælge mellem liste, tuple, ordbog og mængde gennem kontrakter og test.",
            ),
        ),
    ),
    concepts=(
        concept(
            "mapping-model-and-keys",
            (
                "Diccionarios como asociaciones",
                "Dictionaries as associations",
                "Ordbøger som relationer",
            ),
            (
                "Un diccionario asocia cada clave con un valor. Las claves son únicas y deben ser hashables; cadenas, números y tuplas inmutables suelen servir, mientras una lista no. Asignar una clave existente reemplaza su valor. La estructura es adecuada cuando el dato se consulta por identidad y no por posición.",
                "A dictionary maps each key to one value. Keys are unique and must be hashable; strings, numbers, and immutable tuples commonly work, while a list does not. Assigning an existing key replaces its value. The structure fits data retrieved by identity rather than position.",
                "En ordbog knytter hver nøgle til én værdi. Nøgler er unikke og skal være hashbare; strenge, tal og uforanderlige tupler fungerer ofte, mens en liste ikke gør. Tildeling til en eksisterende nøgle erstatter værdien. Strukturen passer til opslag efter identitet frem for position.",
            ),
            (
                (
                    "Las claves identifican; los valores describen.",
                    "Keys identify; values describe.",
                    "Nøgler identificerer; værdier beskriver.",
                ),
                (
                    "Una clave aparece como máximo una vez.",
                    "A key appears at most once.",
                    "En nøgle forekommer højst én gang.",
                ),
                (
                    "La clave debe ser hashable y estable.",
                    "A key must be hashable and stable.",
                    "En nøgle skal være hashbar og stabil.",
                ),
            ),
        ),
        concept(
            "safe-access-and-membership",
            (
                "Acceso seguro y pertenencia",
                "Safe access and membership",
                "Sikker adgang og medlemskab",
            ),
            (
                "d[key] exige que la clave exista y produce KeyError si falta. d.get(key, default) expresa un valor alternativo sin modificar el diccionario. El operador in comprueba claves, no valores. La elección entre acceso estricto y tolerante debe formar parte del contrato, no ocultar datos ausentes de manera arbitraria.",
                "d[key] requires the key and raises KeyError when it is absent. d.get(key, default) expresses an alternative without modifying the dictionary. The in operator checks keys, not values. Strict versus tolerant access belongs in the contract rather than silently hiding missing data.",
                "d[key] kræver nøglen og giver KeyError, hvis den mangler. d.get(key, default) angiver et alternativ uden at ændre ordbogen. Operatoren in kontrollerer nøgler, ikke værdier. Streng eller tolerant adgang skal være en del af kontrakten.",
            ),
            (
                (
                    "d[key] es apropiado cuando faltar es un error.",
                    "d[key] is appropriate when absence is an error.",
                    "d[key] er passende, når fravær er en fejl.",
                ),
                (
                    "get no inserta el valor predeterminado.",
                    "get does not insert the default value.",
                    "get indsætter ikke standardværdien.",
                ),
                ("key in d consulta claves.", "key in d tests keys.", "key in d tester nøgler."),
            ),
        ),
        concept(
            "mutation-deletion-and-traversal",
            (
                "Actualización, eliminación y recorrido",
                "Update, deletion, and traversal",
                "Opdatering, sletning og gennemløb",
            ),
            (
                "La asignación actualiza o inserta; del exige una clave existente y pop elimina y retorna. keys(), values() e items() proporcionan vistas dinámicas. No debe modificarse el tamaño del diccionario mientras se recorre directamente; para eliminar varias entradas se recorre una copia de las claves o se construye un resultado nuevo.",
                "Assignment updates or inserts; del requires an existing key, and pop removes and returns. keys(), values(), and items() provide dynamic views. Dictionary size should not change during direct traversal; remove several entries by traversing a key copy or constructing a new result.",
                "Tildeling opdaterer eller indsætter; del kræver en eksisterende nøgle, og pop fjerner og returnerer. keys(), values() og items() giver dynamiske views. Ordbogens størrelse bør ikke ændres under direkte gennemløb; gennemløb en kopi af nøglerne eller byg et nyt resultat.",
            ),
            (
                (
                    "items() entrega pares clave-valor.",
                    "items() yields key-value pairs.",
                    "items() giver nøgle-værdi-par.",
                ),
                (
                    "pop combina eliminación y retorno.",
                    "pop combines removal and return.",
                    "pop kombinerer fjernelse og retur.",
                ),
                (
                    "Evita cambiar el tamaño durante el recorrido.",
                    "Avoid changing size during traversal.",
                    "Undgå at ændre størrelsen under gennemløb.",
                ),
            ),
        ),
        concept(
            "frequency-and-grouping",
            ("Frecuencias y agrupación", "Frequencies and grouping", "Frekvenser og gruppering"),
            (
                "Una tabla de frecuencia usa cada categoría como clave y su conteo como valor. El patrón count[key] = count.get(key, 0) + 1 evita ramas innecesarias. Para agrupar, cada clave puede almacenar una lista; setdefault o una comprobación explícita crea el grupo antes de añadir. La normalización debe ocurrir antes de contar para no fragmentar categorías equivalentes.",
                "A frequency table uses each category as a key and its count as the value. The pattern count[key] = count.get(key, 0) + 1 avoids unnecessary branches. For grouping, each key may store a list; setdefault or an explicit check creates the group before appending. Normalize before counting to avoid splitting equivalent categories.",
                "En frekvenstabel bruger hver kategori som nøgle og dens antal som værdi. Mønsteret count[key] = count.get(key, 0) + 1 undgår unødige grene. Ved gruppering kan hver nøgle gemme en liste; setdefault eller en eksplicit kontrol opretter gruppen før tilføjelse. Normalisér før optælling.",
            ),
            (
                (
                    "Inicializa conteos en cero.",
                    "Initialize counts at zero.",
                    "Initialisér antal til nul.",
                ),
                (
                    "Agrupar suele producir listas como valores.",
                    "Grouping often produces lists as values.",
                    "Gruppering giver ofte lister som værdier.",
                ),
                (
                    "Normaliza antes de usar la clave.",
                    "Normalize before using the key.",
                    "Normalisér før nøglen bruges.",
                ),
            ),
        ),
        concept(
            "nested-records-and-schema",
            (
                "Registros anidados y esquema",
                "Nested records and schema",
                "Indlejrede poster og skema",
            ),
            (
                "Un diccionario puede contener otros diccionarios, listas y valores escalares. Esta flexibilidad exige un esquema explícito: claves obligatorias, tipos esperados, valores opcionales y comportamiento ante datos desconocidos. Encadenar muchos accesos directos vuelve frágil el código; conviene validar en la frontera y separar extracción, transformación y resumen.",
                "A dictionary may contain dictionaries, lists, and scalar values. This flexibility requires an explicit schema: required keys, expected types, optional values, and behavior for unknown data. Long chains of direct access are fragile; validate at the boundary and separate extraction, transformation, and summary.",
                "En ordbog kan indeholde ordbøger, lister og skalære værdier. Fleksibiliteten kræver et eksplicit skema: obligatoriske nøgler, forventede typer, valgfrie værdier og adfærd ved ukendte data. Lange kæder af direkte opslag er skrøbelige; validér ved grænsen.",
            ),
            (
                (
                    "La forma del registro es parte del contrato.",
                    "Record shape is part of the contract.",
                    "Postens form er en del af kontrakten.",
                ),
                (
                    "Valida antes de calcular.",
                    "Validate before computing.",
                    "Validér før beregning.",
                ),
                (
                    "Separa extracción y análisis.",
                    "Separate extraction and analysis.",
                    "Adskil udtræk og analyse.",
                ),
            ),
        ),
        concept(
            "set-semantics",
            (
                "Conjuntos, unicidad y pertenencia",
                "Sets, uniqueness, and membership",
                "Mængder, entydighed og medlemskab",
            ),
            (
                "Un conjunto almacena elementos únicos y hashables. No representa posiciones ni duplicados y no debe usarse cuando la multiplicidad sea información. set(values) elimina duplicados; add inserta, discard elimina sin error si falta y remove exige presencia. La pertenencia suele expresar mejor la intención que una búsqueda repetida en una lista.",
                "A set stores unique hashable elements. It represents neither positions nor duplicates and should not be used when multiplicity matters. set(values) removes duplicates; add inserts, discard removes without error when absent, and remove requires presence. Membership often expresses intent better than repeated list search.",
                "En mængde gemmer unikke hashbare elementer. Den repræsenterer hverken positioner eller dubletter og bør ikke bruges, når multiplicitet er information. set(values) fjerner dubletter; add indsætter, discard fjerner uden fejl, og remove kræver tilstedeværelse.",
            ),
            (
                (
                    "Un conjunto no conserva multiplicidad.",
                    "A set does not preserve multiplicity.",
                    "En mængde bevarer ikke multiplicitet.",
                ),
                (
                    "discard es tolerante; remove es estricto.",
                    "discard is tolerant; remove is strict.",
                    "discard er tolerant; remove er streng.",
                ),
                (
                    "Los elementos deben ser hashables.",
                    "Elements must be hashable.",
                    "Elementer skal være hashbare.",
                ),
            ),
        ),
        concept(
            "set-algebra",
            ("Álgebra de conjuntos", "Set algebra", "Mængdealgebra"),
            (
                "A | B o union reúne elementos; A & B o intersection conserva los comunes; A - B conserva los exclusivos de A; A ^ B conserva los presentes en exactamente uno. <= expresa subconjunto y isdisjoint ausencia de elementos comunes. El orden de la diferencia importa y cada operación debe vincularse con una pregunta concreta.",
                "A | B or union combines elements; A & B or intersection keeps common elements; A - B keeps elements exclusive to A; A ^ B keeps elements present in exactly one. <= expresses subset and isdisjoint no overlap. Difference is directional, and every operation should answer a concrete question.",
                "A | B eller union samler elementer; A & B eller intersection beholder fælles elementer; A - B beholder elementer kun i A; A ^ B beholder elementer i præcis én mængde. <= udtrykker delmængde, og isdisjoint intet overlap. Differens er retningsbestemt.",
            ),
            (
                (
                    "La intersección responde qué comparten.",
                    "Intersection answers what they share.",
                    "Snit svarer på, hvad de deler.",
                ),
                (
                    "A - B y B - A suelen diferir.",
                    "A - B and B - A usually differ.",
                    "A - B og B - A er ofte forskellige.",
                ),
                (
                    "La diferencia simétrica excluye la intersección.",
                    "Symmetric difference excludes the intersection.",
                    "Symmetrisk differens udelukker snittet.",
                ),
            ),
        ),
        concept(
            "structure-selection-and-testing",
            (
                "Selección de estructura y pruebas",
                "Structure selection and testing",
                "Strukturvalg og test",
            ),
            (
                "La lista conserva orden y duplicados; la tupla comunica una agrupación fija; el diccionario asocia claves con valores; el conjunto representa unicidad y pertenencia. La selección debe seguir las operaciones dominantes y el contrato observable. Las pruebas incluyen claves ausentes, duplicados, entradas vacías, orden no garantizado, mutación, aliasing de valores y operaciones de conjuntos en ambos sentidos.",
                "A list preserves order and duplicates; a tuple communicates a fixed grouping; a dictionary maps keys to values; a set represents uniqueness and membership. Selection follows dominant operations and observable contract. Tests cover missing keys, duplicates, empty inputs, unspecified order, mutation, aliased values, and set operations in both directions.",
                "En liste bevarer rækkefølge og dubletter; en tuple kommunikerer en fast gruppering; en ordbog knytter nøgler til værdier; en mængde repræsenterer entydighed og medlemskab. Valget følger de dominerende operationer og den observerbare kontrakt. Test dækker manglende nøgler, dubletter, tomme input og mutation.",
            ),
            (
                (
                    "El contrato decide qué información conservar.",
                    "The contract decides which information to preserve.",
                    "Kontrakten afgør, hvilke oplysninger der bevares.",
                ),
                (
                    "No conviertas a set si los duplicados importan.",
                    "Do not convert to a set when duplicates matter.",
                    "Konvertér ikke til en mængde, når dubletter betyder noget.",
                ),
                (
                    "Prueba casos ausentes y vacíos.",
                    "Test absent and empty cases.",
                    "Test manglende og tomme tilfælde.",
                ),
            ),
        ),
    ),
    worked_examples=(
        example(
            "frequency-table",
            (
                "Contar etiquetas normalizadas",
                "Count normalized labels",
                "Optæl normaliserede etiketter",
            ),
            (
                "Construye una frecuencia sin separar variantes de mayúsculas.",
                "Build a frequency table without splitting case variants.",
                "Byg en frekvenstabel uden at opdele store og små bogstaver.",
            ),
            (
                ("Normalizar cada etiqueta.", "Normalize each label.", "Normalisér hver etiket."),
                ("Usar get con cero.", "Use get with zero.", "Brug get med nul."),
                ("Actualizar el conteo.", "Update the count.", "Opdatér antallet."),
            ),
            'labels = ["Control", "case", "CONTROL"]\ncounts = {}\nfor label in labels:\n    key = label.casefold()\n    counts[key] = counts.get(key, 0) + 1\nprint(counts)',
            "{'control': 2, 'case': 1}",
            (
                "La clave normalizada concentra categorías equivalentes.",
                "The normalized key combines equivalent categories.",
                "Den normaliserede nøgle samler ækvivalente kategorier.",
            ),
        ),
        example(
            "group-values",
            (
                "Agrupar valores por muestra",
                "Group values by sample",
                "Gruppér værdier efter prøve",
            ),
            (
                "Agrupa pares de identificador y valor.",
                "Group identifier-value pairs.",
                "Gruppér identifikator-værdi-par.",
            ),
            (
                (
                    "Crear el grupo cuando falte.",
                    "Create the group when absent.",
                    "Opret gruppen, når den mangler.",
                ),
                (
                    "Añadir el valor al grupo.",
                    "Append the value to the group.",
                    "Tilføj værdien til gruppen.",
                ),
            ),
            'rows = [("S1", 2.1), ("S2", 3.0), ("S1", 2.4)]\ngroups = {}\nfor sample, value in rows:\n    groups.setdefault(sample, []).append(value)\nprint(groups)',
            "{'S1': [2.1, 2.4], 'S2': [3.0]}",
            (
                "Cada clave almacena la secuencia de valores asociados.",
                "Each key stores its associated value sequence.",
                "Hver nøgle gemmer den tilknyttede værdisekvens.",
            ),
        ),
        example(
            "compare-identifiers",
            ("Comparar identificadores", "Compare identifiers", "Sammenlign identifikatorer"),
            (
                "Encuentra identificadores comunes y ausentes.",
                "Find common and missing identifiers.",
                "Find fælles og manglende identifikatorer.",
            ),
            (
                ("Convertir a conjuntos.", "Convert to sets.", "Konvertér til mængder."),
                (
                    "Usar intersección y diferencia.",
                    "Use intersection and difference.",
                    "Brug snit og differens.",
                ),
            ),
            'expected = {"A", "B", "C"}\nobserved = {"B", "C", "D"}\nprint(sorted(expected & observed))\nprint(sorted(expected - observed))',
            "['B', 'C']\n['A']",
            (
                "La diferencia se calcula desde el conjunto de referencia.",
                "The difference is computed from the reference set.",
                "Differensen beregnes fra referencemængden.",
            ),
        ),
        example(
            "validate-record",
            (
                "Validar un registro anidado",
                "Validate a nested record",
                "Validér en indlejret post",
            ),
            (
                "Comprueba claves obligatorias antes de resumir.",
                "Check required keys before summarizing.",
                "Kontrollér obligatoriske nøgler før opsummering.",
            ),
            (
                (
                    "Definir las claves exigidas.",
                    "Define required keys.",
                    "Definér krævede nøgler.",
                ),
                (
                    "Compararlas con las observadas.",
                    "Compare them with observed keys.",
                    "Sammenlign med observerede nøgler.",
                ),
                ("Rechazar faltantes.", "Reject missing keys.", "Afvis manglende nøgler."),
            ),
            'record = {"sample_id": "S1", "values": [1.2, 1.5]}\nrequired = {"sample_id", "values"}\nmissing = required - record.keys()\nprint(missing)',
            "set()",
            (
                "dict_keys participa en operaciones de conjunto compatibles.",
                "dict_keys supports compatible set operations.",
                "dict_keys understøtter kompatible mængdeoperationer.",
            ),
        ),
        example(
            "detect-duplicates",
            ("Detectar valores repetidos", "Detect duplicate values", "Find gentagne værdier"),
            (
                "Identifica valores asociados a más de una clave.",
                "Identify values associated with more than one key.",
                "Identificér værdier knyttet til mere end én nøgle.",
            ),
            (
                (
                    "Invertir hacia conjuntos de claves.",
                    "Invert into sets of keys.",
                    "Invertér til mængder af nøgler.",
                ),
                (
                    "Filtrar grupos con más de una clave.",
                    "Filter groups with more than one key.",
                    "Filtrér grupper med mere end én nøgle.",
                ),
            ),
            'mapping = {"a": 1, "b": 2, "c": 1}\nreverse = {}\nfor key, value in mapping.items():\n    reverse.setdefault(value, set()).add(key)\nprint({value: keys for value, keys in reverse.items() if len(keys) > 1})',
            "{1: {'a', 'c'}}",
            (
                "Un conjunto representa las claves únicas asociadas a cada valor.",
                "A set represents the unique keys associated with each value.",
                "En mængde repræsenterer de unikke nøgler for hver værdi.",
            ),
        ),
    ),
    practice_exercises=(
        practice(
            "m07.p01",
            ActivityType.CODE_TRACING,
            (
                "Traza {'a': 1}.get('b', 0).",
                "Trace {'a': 1}.get('b', 0).",
                "Gennemgå {'a': 1}.get('b', 0).",
            ),
            (("La clave no existe.", "The key is absent.", "Nøglen mangler."),),
            ("0", "0", "0"),
            (
                "get retorna el valor predeterminado sin insertar.",
                "get returns the default without insertion.",
                "get returnerer standardværdien uden indsættelse.",
            ),
        ),
        practice(
            "m07.p02",
            ActivityType.DEBUGGING,
            (
                "Corrige un intento de usar una lista como clave.",
                "Fix an attempt to use a list as a key.",
                "Ret et forsøg på at bruge en liste som nøgle.",
            ),
            (
                (
                    "La clave debe ser hashable.",
                    "The key must be hashable.",
                    "Nøglen skal være hashbar.",
                ),
            ),
            (
                "Usar una tupla inmutable, por ejemplo d[(1, 2)] = value.",
                "Use an immutable tuple, for example d[(1, 2)] = value.",
                "Brug en uforanderlig tuple, fx d[(1, 2)] = value.",
            ),
            (
                "Las listas son mutables y no pueden ser claves.",
                "Lists are mutable and cannot be keys.",
                "Lister er muterbare og kan ikke være nøgler.",
            ),
        ),
        practice(
            "m07.p03",
            ActivityType.FILL_IN_THE_BLANK,
            (
                "Completa el patrón de conteo: counts[key] = counts.____(key, 0) + 1.",
                "Complete the counting pattern: counts[key] = counts.____(key, 0) + 1.",
                "Udfyld optællingsmønsteret: counts[key] = counts.____(key, 0) + 1.",
            ),
            (
                (
                    "Busca un método con valor predeterminado.",
                    "Look for a method with a default.",
                    "Find en metode med standardværdi.",
                ),
            ),
            ("get", "get", "get"),
            (
                "get evita una rama de inicialización.",
                "get avoids an initialization branch.",
                "get undgår en initialiseringsgren.",
            ),
        ),
        practice(
            "m07.p04",
            ActivityType.CODE_COMPLETION,
            (
                "Escribe unique_count(values).",
                "Write unique_count(values).",
                "Skriv unique_count(values).",
            ),
            (
                (
                    "Convierte a una estructura de elementos únicos.",
                    "Convert to a unique-element structure.",
                    "Konvertér til en struktur med unikke elementer.",
                ),
            ),
            (
                "def unique_count(values):\n    return len(set(values))",
                "def unique_count(values):\n    return len(set(values))",
                "def unique_count(values):\n    return len(set(values))",
            ),
            (
                "El conjunto elimina duplicados y len cuenta elementos únicos.",
                "The set removes duplicates and len counts unique elements.",
                "Mængden fjerner dubletter, og len tæller unikke elementer.",
            ),
            "def unique_count(values):\n    pass",
        ),
        practice(
            "m07.p05",
            ActivityType.ORDERING,
            (
                "Ordena: normalizar, crear clave, actualizar grupo, resumir.",
                "Order: normalize, create key, update group, summarize.",
                "Ordén: normalisér, opret nøgle, opdatér gruppe, opsummér.",
            ),
            (
                (
                    "La normalización precede al uso como clave.",
                    "Normalization precedes key use.",
                    "Normalisering går forud for brug som nøgle.",
                ),
            ),
            (
                "Normalizar → crear clave → actualizar grupo → resumir.",
                "Normalize → create key → update group → summarize.",
                "Normalisér → opret nøgle → opdatér gruppe → opsummér.",
            ),
            (
                "El orden evita categorías fragmentadas.",
                "The order avoids fragmented categories.",
                "Rækkefølgen undgår fragmenterede kategorier.",
            ),
        ),
        practice(
            "m07.p06",
            ActivityType.SHORT_ANSWER,
            (
                "Explica cuándo d[key] es preferible a get.",
                "Explain when d[key] is preferable to get.",
                "Forklar, hvornår d[key] er bedre end get.",
            ),
            (
                (
                    "Piensa si la ausencia es válida.",
                    "Consider whether absence is valid.",
                    "Overvej om fravær er gyldigt.",
                ),
            ),
            (
                "Cuando la clave es obligatoria y su ausencia debe producir un error visible.",
                "When the key is required and absence should produce a visible error.",
                "Når nøglen er obligatorisk, og fravær skal give en synlig fejl.",
            ),
            (
                "El acceso estricto hace cumplir el contrato.",
                "Strict access enforces the contract.",
                "Streng adgang håndhæver kontrakten.",
            ),
        ),
        practice(
            "m07.p07",
            ActivityType.DATA_INTERPRETATION,
            (
                "Interpreta A - B frente a B - A.",
                "Interpret A - B versus B - A.",
                "Fortolk A - B i forhold til B - A.",
            ),
            (
                (
                    "La diferencia es direccional.",
                    "Difference is directional.",
                    "Differens er retningsbestemt.",
                ),
            ),
            (
                "A - B son elementos sólo en A; B - A son elementos sólo en B.",
                "A - B contains elements only in A; B - A contains elements only in B.",
                "A - B indeholder elementer kun i A; B - A kun i B.",
            ),
            (
                "Intercambiar operandos cambia la pregunta.",
                "Swapping operands changes the question.",
                "Bytning af operander ændrer spørgsmålet.",
            ),
        ),
        practice(
            "m07.p08",
            ActivityType.DEBUGGING,
            (
                "Corrige un bucle que elimina claves mientras recorre d.",
                "Fix a loop that deletes keys while traversing d.",
                "Ret en løkke, der sletter nøgler under gennemløb af d.",
            ),
            (
                (
                    "Recorre una instantánea.",
                    "Traverse a snapshot.",
                    "Gennemløb et øjebliksbillede.",
                ),
            ),
            (
                "for key in list(d):\n    if should_remove(key):\n        del d[key]",
                "for key in list(d):\n    if should_remove(key):\n        del d[key]",
                "for key in list(d):\n    if should_remove(key):\n        del d[key]",
            ),
            (
                "list(d) separa el recorrido de la mutación.",
                "list(d) separates traversal from mutation.",
                "list(d) adskiller gennemløb fra mutation.",
            ),
        ),
        practice(
            "m07.p09",
            ActivityType.CODE_TRACING,
            (
                "Traza {1, 2, 3} & {2, 3, 4}.",
                "Trace {1, 2, 3} & {2, 3, 4}.",
                "Gennemgå {1, 2, 3} & {2, 3, 4}.",
            ),
            (("Conserva los comunes.", "Keep common elements.", "Behold fælles elementer."),),
            ("{2, 3}", "{2, 3}", "{2, 3}"),
            ("& calcula la intersección.", "& computes intersection.", "& beregner snittet."),
        ),
        practice(
            "m07.p10",
            ActivityType.PIPELINE_DESIGN,
            (
                "Diseña un flujo para agrupar registros por categoría.",
                "Design a flow to group records by category.",
                "Design et flow til gruppering af poster efter kategori.",
            ),
            (
                (
                    "Incluye validación y normalización.",
                    "Include validation and normalization.",
                    "Medtag validering og normalisering.",
                ),
            ),
            (
                "Validar registro → normalizar categoría → crear/obtener grupo → añadir → resumir.",
                "Validate record → normalize category → create/get group → append → summarize.",
                "Validér post → normalisér kategori → opret/hent gruppe → tilføj → opsummér.",
            ),
            (
                "Cada etapa tiene un contrato comprobable.",
                "Each stage has a testable contract.",
                "Hvert trin har en testbar kontrakt.",
            ),
        ),
        practice(
            "m07.p11",
            ActivityType.ORAL_EXPLANATION,
            (
                "Compara lista, diccionario y conjunto para buscar identificadores.",
                "Compare list, dictionary, and set for identifier lookup.",
                "Sammenlign liste, ordbog og mængde til identifikatoropslag.",
            ),
            (
                (
                    "Considera qué información acompaña al identificador.",
                    "Consider what information accompanies the identifier.",
                    "Overvej hvilke oplysninger der følger identifikatoren.",
                ),
            ),
            (
                "Lista conserva orden y duplicados; conjunto representa pertenencia única; diccionario asocia cada identificador con datos.",
                "A list preserves order and duplicates; a set represents unique membership; a dictionary maps each identifier to data.",
                "En liste bevarer rækkefølge og dubletter; en mængde repræsenterer unikt medlemskab; en ordbog knytter hver identifikator til data.",
            ),
            (
                "La operación dominante determina la estructura.",
                "The dominant operation determines the structure.",
                "Den dominerende operation bestemmer strukturen.",
            ),
        ),
        practice(
            "m07.p12",
            ActivityType.CODE_COMPLETION,
            (
                "Completa missing = required ____ observed.",
                "Complete missing = required ____ observed.",
                "Udfyld missing = required ____ observed.",
            ),
            (
                (
                    "Necesitas elementos exigidos no observados.",
                    "You need required elements not observed.",
                    "Du behøver krævede elementer, som ikke er observeret.",
                ),
            ),
            ("-", "-", "-"),
            (
                "La diferencia required - observed produce los faltantes.",
                "The difference required - observed produces missing elements.",
                "Differensen required - observed giver manglende elementer.",
            ),
        ),
    ),
    assessment_items=(
        authored_item(
            "dm857.m07.assessment.001",
            ActivityType.CODE_TRACING,
            (
                "Traza d = {'x': 1}; d['x'] = 2.",
                "Trace d = {'x': 1}; d['x'] = 2.",
                "Gennemgå d = {'x': 1}; d['x'] = 2.",
            ),
            (("{'x': 2}", "{'x': 2}", "{'x': 2}"),),
            (
                "La clave existente se actualiza.",
                "The existing key is updated.",
                "Den eksisterende nøgle opdateres.",
            ),
        ),
        authored_item(
            "dm857.m07.assessment.002",
            ActivityType.MULTIPLE_SELECT,
            (
                "Selecciona estructuras que eliminan duplicados por definición.",
                "Select structures that remove duplicates by definition.",
                "Vælg strukturer, der per definition fjerner dubletter.",
            ),
            (),
            ("set y frozenset.", "set and frozenset.", "set og frozenset."),
            options=(
                ("set", ("set", "set", "set")),
                ("frozenset", ("frozenset", "frozenset", "frozenset")),
                ("list", ("list", "list", "list")),
                ("tuple", ("tuple", "tuple", "tuple")),
            ),
            correct_option_ids=("set", "frozenset"),
        ),
        authored_item(
            "dm857.m07.assessment.003",
            ActivityType.DEBUGGING,
            (
                "Corrige values = d.values(); if target in d.",
                "Fix values = d.values(); if target in d.",
                "Ret values = d.values(); if target in d.",
            ),
            (
                (
                    "Usar if target in d.values() cuando se buscan valores.",
                    "Use if target in d.values() when searching values.",
                    "Brug if target in d.values(), når der søges i værdier.",
                ),
            ),
            (
                "in sobre el diccionario consulta claves.",
                "in on a dictionary checks keys.",
                "in på en ordbog kontrollerer nøgler.",
            ),
        ),
        authored_item(
            "dm857.m07.assessment.004",
            ActivityType.FILL_IN_THE_BLANK,
            (
                "Completa la intersección: common = A ____ B.",
                "Complete the intersection: common = A ____ B.",
                "Udfyld snittet: common = A ____ B.",
            ),
            (("&", "&", "&"),),
            (
                "& conserva elementos comunes.",
                "& keeps common elements.",
                "& beholder fælles elementer.",
            ),
        ),
        authored_item(
            "dm857.m07.assessment.005",
            ActivityType.MATCHING,
            (
                "Relaciona estructura y propiedad.",
                "Match structure and property.",
                "Match struktur og egenskab.",
            ),
            (),
            (
                "Lista-orden y duplicados; diccionario-asociación; conjunto-unicidad; tupla-registro fijo.",
                "List-order and duplicates; dictionary-mapping; set-uniqueness; tuple-fixed record.",
                "Liste-rækkefølge og dubletter; ordbog-relation; mængde-entydighed; tuple-fast post.",
            ),
            options=(
                (
                    "list",
                    (
                        "Lista → orden y duplicados",
                        "List → order and duplicates",
                        "Liste → rækkefølge og dubletter",
                    ),
                ),
                ("dict", ("Diccionario → asociación", "Dictionary → mapping", "Ordbog → relation")),
                ("set", ("Conjunto → unicidad", "Set → uniqueness", "Mængde → entydighed")),
                ("tuple", ("Tupla → registro fijo", "Tuple → fixed record", "Tuple → fast post")),
            ),
            correct_option_ids=("list", "dict", "set", "tuple"),
        ),
        authored_item(
            "dm857.m07.assessment.006",
            ActivityType.ORDERING,
            (
                "Ordena un conteo robusto.",
                "Order a robust counting workflow.",
                "Ordén et robust optællingsflow.",
            ),
            (),
            (
                "Validar → normalizar → consultar conteo → incrementar → resumir.",
                "Validate → normalize → read count → increment → summarize.",
                "Validér → normalisér → læs antal → øg → opsummér.",
            ),
            options=(
                ("validate", ("Validar", "Validate", "Validér")),
                ("normalize", ("Normalizar", "Normalize", "Normalisér")),
                ("read", ("Consultar conteo", "Read count", "Læs antal")),
                ("increment", ("Incrementar", "Increment", "Øg")),
                ("summarize", ("Resumir", "Summarize", "Opsummér")),
            ),
            correct_option_ids=("validate", "normalize", "read", "increment", "summarize"),
        ),
        authored_item(
            "dm857.m07.assessment.007",
            ActivityType.CODE_COMPLETION,
            (
                "Escribe una función missing_keys(record, required).",
                "Write missing_keys(record, required).",
                "Skriv en funktion missing_keys(record, required).",
            ),
            (
                (
                    "def missing_keys(record, required):\n    return set(required) - record.keys()",
                    "def missing_keys(record, required):\n    return set(required) - record.keys()",
                    "def missing_keys(record, required):\n    return set(required) - record.keys()",
                ),
            ),
            (
                "La diferencia devuelve claves obligatorias ausentes.",
                "Difference returns absent required keys.",
                "Differensen returnerer manglende obligatoriske nøgler.",
            ),
            rubric=(
                (
                    "Retorna un conjunto sin mutar el registro.",
                    "Returns a set without mutating the record.",
                    "Returnerer en mængde uden at ændre posten.",
                ),
            ),
        ),
        authored_item(
            "dm857.m07.assessment.008",
            ActivityType.SHORT_ANSWER,
            (
                "Explica por qué get no siempre es más seguro.",
                "Explain why get is not always safer.",
                "Forklar, hvorfor get ikke altid er sikrere.",
            ),
            (
                (
                    "Puede ocultar la ausencia de una clave obligatoria y mezclar datos ausentes con un valor predeterminado válido.",
                    "It may hide a missing required key and conflate absence with a valid default.",
                    "Det kan skjule en manglende obligatorisk nøgle og sammenblande fravær med en gyldig standardværdi.",
                ),
            ),
            (
                "La seguridad depende del contrato.",
                "Safety depends on the contract.",
                "Sikkerhed afhænger af kontrakten.",
            ),
        ),
        authored_item(
            "dm857.m07.assessment.009",
            ActivityType.DATA_INTERPRETATION,
            (
                "Interpreta por qué len(values) cambia tras set(values).",
                "Interpret why len(values) changes after set(values).",
                "Fortolk, hvorfor len(values) ændres efter set(values).",
            ),
            (
                (
                    "Había duplicados y el conjunto conserva una sola instancia de cada valor.",
                    "Duplicates existed and the set keeps one instance of each value.",
                    "Der var dubletter, og mængden beholder én forekomst af hver værdi.",
                ),
            ),
            (
                "La conversión pierde multiplicidad.",
                "Conversion loses multiplicity.",
                "Konverteringen mister multiplicitet.",
            ),
        ),
        authored_item(
            "dm857.m07.assessment.010",
            ActivityType.ORAL_EXPLANATION,
            (
                "Explica la dirección de expected - observed.",
                "Explain the direction of expected - observed.",
                "Forklar retningen i expected - observed.",
            ),
            (
                (
                    "Produce lo esperado que no se observó; invertir operandos produce observaciones inesperadas.",
                    "It yields expected elements not observed; reversing operands yields unexpected observations.",
                    "Det giver forventede elementer, som ikke blev observeret; omvendte operander giver uventede observationer.",
                ),
            ),
            (
                "La diferencia responde una pregunta orientada.",
                "Difference answers a directional question.",
                "Differens besvarer et retningsbestemt spørgsmål.",
            ),
        ),
        authored_item(
            "dm857.m07.assessment.011",
            ActivityType.PIPELINE_DESIGN,
            (
                "Diseña una canalización didáctica para validar y agrupar registros.",
                "Design a teaching pipeline to validate and group records.",
                "Design en undervisningspipeline til validering og gruppering af poster.",
            ),
            (
                (
                    "Validar esquema → normalizar clave → agrupar → comprobar grupos vacíos → resumir.",
                    "Validate schema → normalize key → group → check empty groups → summarize.",
                    "Validér skema → normalisér nøgle → gruppér → kontrollér tomme grupper → opsummér.",
                ),
            ),
            (
                "La validación precede al acceso anidado.",
                "Validation precedes nested access.",
                "Validering går forud for indlejret adgang.",
            ),
            rubric=(
                (
                    "Define contratos de entrada y salida.",
                    "Defines input and output contracts.",
                    "Definerer input- og outputkontrakter.",
                ),
            ),
        ),
        authored_item(
            "dm857.m07.assessment.012",
            ActivityType.DEBUGGING,
            (
                "Corrige groups = dict.fromkeys(labels, []).",
                "Fix groups = dict.fromkeys(labels, []).",
                "Ret groups = dict.fromkeys(labels, []).",
            ),
            (
                (
                    "Usar {label: [] for label in labels} para crear listas independientes.",
                    "Use {label: [] for label in labels} to create independent lists.",
                    "Brug {label: [] for label in labels} for at oprette uafhængige lister.",
                ),
            ),
            (
                "fromkeys reutiliza el mismo objeto mutable como valor.",
                "fromkeys reuses the same mutable object as the value.",
                "fromkeys genbruger samme muterbare objekt som værdi.",
            ),
        ),
        authored_item(
            "dm857.m07.assessment.013",
            ActivityType.CODE_TRACING,
            ("Traza {1, 2} ^ {2, 3}.", "Trace {1, 2} ^ {2, 3}.", "Gennemgå {1, 2} ^ {2, 3}."),
            (("{1, 3}", "{1, 3}", "{1, 3}"),),
            (
                "La diferencia simétrica excluye el elemento común.",
                "Symmetric difference excludes the common element.",
                "Symmetrisk differens udelukker det fælles element.",
            ),
        ),
        authored_item(
            "dm857.m07.assessment.014",
            ActivityType.SHORT_ANSWER,
            (
                "Justifica cuándo no convertir una lista en conjunto.",
                "Justify when not to convert a list to a set.",
                "Begrund, hvornår en liste ikke bør konverteres til en mængde.",
            ),
            (
                (
                    "Cuando importan el orden, los duplicados o la posición de cada elemento.",
                    "When order, duplicates, or element positions matter.",
                    "Når rækkefølge, dubletter eller elementpositioner betyder noget.",
                ),
            ),
            (
                "La conversión debe conservar la semántica necesaria.",
                "Conversion must preserve required semantics.",
                "Konverteringen skal bevare den nødvendige semantik.",
            ),
        ),
    ),
    tutor_support=tutor_support(
        (
            "Los diccionarios representan asociaciones entre claves únicas y valores. Una clave debe ser hashable y estable; el acceso directo d[key] hace cumplir presencia, mientras get expresa un caso alternativo sin insertar datos. Asignar una clave existente actualiza el valor y pop elimina y retorna. keys, values e items proporcionan vistas para recorridos distintos, pero el tamaño no debe cambiar durante un recorrido directo. Las tablas de frecuencia combinan normalización y actualización de conteos; las agrupaciones almacenan colecciones como valores y deben evitar aliasing accidental. Los diccionarios anidados requieren un esquema explícito y validación antes del cálculo. Los conjuntos representan unicidad y pertenencia, no posiciones ni multiplicidad. Unión, intersección, diferencia y diferencia simétrica responden preguntas diferentes; la diferencia es direccional. La selección entre lista, tupla, diccionario y conjunto depende de la información que el contrato debe conservar. Las pruebas deben cubrir claves ausentes, valores predeterminados, colecciones vacías, duplicados, mutación durante recorridos y operaciones de conjuntos en ambos sentidos. Los ejemplos biomédicos son escenarios didácticos de programación y no representan protocolos, criterios clínicos ni recomendaciones de laboratorio.",
            "Dictionaries represent mappings from unique keys to values. A key must be hashable and stable; direct access d[key] enforces presence, while get expresses an alternative without inserting data. Assigning an existing key updates its value, and pop removes and returns. keys, values, and items provide different traversal views, but dictionary size must not change during direct traversal. Frequency tables combine normalization with count updates; grouping stores collections as values and must avoid accidental aliasing. Nested dictionaries require an explicit schema and validation before computation. Sets represent uniqueness and membership, not positions or multiplicity. Union, intersection, difference, and symmetric difference answer different questions; difference is directional. Choosing among list, tuple, dictionary, and set depends on information the contract must preserve. Tests cover missing keys, defaults, empty collections, duplicates, mutation during traversal, and set operations in both directions. Biomedical examples are programming exercises, not protocols, clinical criteria, or laboratory recommendations.",
            "Ordbøger repræsenterer relationer fra unikke nøgler til værdier. En nøgle skal være hashbar og stabil; direkte adgang d[key] håndhæver tilstedeværelse, mens get angiver et alternativ uden at indsætte data. Tildeling til en eksisterende nøgle opdaterer værdien, og pop fjerner og returnerer. keys, values og items giver forskellige views, men størrelsen må ikke ændres under direkte gennemløb. Frekvenstabeller kombinerer normalisering med optælling; gruppering gemmer samlinger som værdier og skal undgå utilsigtet aliasing. Indlejrede ordbøger kræver et eksplicit skema og validering før beregning. Mængder repræsenterer entydighed og medlemskab, ikke positioner eller multiplicitet. Union, snit, differens og symmetrisk differens besvarer forskellige spørgsmål. Valget mellem liste, tuple, ordbog og mængde afhænger af kontrakten. Biomedicinske eksempler er programmeringsøvelser, ikke protokoller, kliniske kriterier eller laboratorieanbefalinger.",
        ),
        tuple(
            (es, en, da)
            for es, en, da in (
                (
                    "Las claves de un diccionario son únicas.",
                    "Dictionary keys are unique.",
                    "Ordbogsnøgler er unikke.",
                ),
                (
                    "Las claves deben ser hashables.",
                    "Keys must be hashable.",
                    "Nøgler skal være hashbare.",
                ),
                (
                    "in sobre dict consulta claves.",
                    "in on dict checks keys.",
                    "in på dict kontrollerer nøgler.",
                ),
                (
                    "get no inserta el predeterminado.",
                    "get does not insert the default.",
                    "get indsætter ikke standardværdien.",
                ),
                ("items entrega pares.", "items yields pairs.", "items giver par."),
                (
                    "No se cambia el tamaño durante recorrido directo.",
                    "Size is not changed during direct traversal.",
                    "Størrelsen ændres ikke under direkte gennemløb.",
                ),
                (
                    "Las frecuencias requieren normalización coherente.",
                    "Frequencies require consistent normalization.",
                    "Frekvenser kræver konsistent normalisering.",
                ),
                (
                    "Agrupar suele usar listas como valores.",
                    "Grouping often uses lists as values.",
                    "Gruppering bruger ofte lister som værdier.",
                ),
                (
                    "Los esquemas anidados se validan en la frontera.",
                    "Nested schemas are validated at the boundary.",
                    "Indlejrede skemaer valideres ved grænsen.",
                ),
                (
                    "Los conjuntos eliminan duplicados.",
                    "Sets remove duplicates.",
                    "Mængder fjerner dubletter.",
                ),
                (
                    "discard tolera ausencia.",
                    "discard tolerates absence.",
                    "discard tolererer fravær.",
                ),
                (
                    "La intersección conserva comunes.",
                    "Intersection keeps common elements.",
                    "Snit beholder fælles elementer.",
                ),
                (
                    "La diferencia es direccional.",
                    "Difference is directional.",
                    "Differens er retningsbestemt.",
                ),
                (
                    "La estructura debe conservar la semántica del contrato.",
                    "The structure must preserve contract semantics.",
                    "Strukturen skal bevare kontraktens semantik.",
                ),
            )
        ),
        tuple(
            (es, en, da)
            for es, en, da in (
                (
                    "Confundir claves y valores en in.",
                    "Confusing keys and values in in.",
                    "Forveksling af nøgler og værdier i in.",
                ),
                (
                    "Creer que get inserta el predeterminado.",
                    "Believing get inserts the default.",
                    "At tro at get indsætter standardværdien.",
                ),
                ("Usar listas como claves.", "Using lists as keys.", "At bruge lister som nøgler."),
                (
                    "Eliminar claves durante el recorrido directo.",
                    "Deleting keys during direct traversal.",
                    "At slette nøgler under direkte gennemløb.",
                ),
                (
                    "Compartir una lista mutable entre grupos.",
                    "Sharing one mutable list across groups.",
                    "At dele én muterbar liste mellem grupper.",
                ),
                (
                    "Contar antes de normalizar.",
                    "Counting before normalization.",
                    "At tælle før normalisering.",
                ),
                (
                    "Ocultar claves obligatorias con get.",
                    "Hiding required keys with get.",
                    "At skjule obligatoriske nøgler med get.",
                ),
                (
                    "Suponer que un conjunto conserva duplicados.",
                    "Assuming a set preserves duplicates.",
                    "At antage at en mængde bevarer dubletter.",
                ),
                (
                    "Confundir diferencia con diferencia simétrica.",
                    "Confusing difference with symmetric difference.",
                    "At forveksle differens med symmetrisk differens.",
                ),
                (
                    "Suponer A-B igual a B-A.",
                    "Assuming A-B equals B-A.",
                    "At antage A-B er lig B-A.",
                ),
                (
                    "Depender del orden de representación de un set.",
                    "Relying on set representation order.",
                    "At afhænge af en mængdes visningsrækkefølge.",
                ),
                (
                    "Elegir estructura por hábito y no por contrato.",
                    "Choosing a structure by habit rather than contract.",
                    "At vælge struktur af vane frem for kontrakt.",
                ),
            )
        ),
        tuple(
            (es, en, da)
            for es, en, da in (
                ("¿La clave es obligatoria?", "Is the key required?", "Er nøglen obligatorisk?"),
                ("¿La clave es hashable?", "Is the key hashable?", "Er nøglen hashbar?"),
                (
                    "¿Buscas una clave o un valor?",
                    "Are you searching for a key or a value?",
                    "Søger du en nøgle eller en værdi?",
                ),
                (
                    "¿El predeterminado es un dato válido?",
                    "Is the default a valid datum?",
                    "Er standardværdien gyldig data?",
                ),
                (
                    "¿Se modifica el tamaño durante el recorrido?",
                    "Does size change during traversal?",
                    "Ændres størrelsen under gennemløb?",
                ),
                (
                    "¿Las categorías están normalizadas?",
                    "Are categories normalized?",
                    "Er kategorier normaliseret?",
                ),
                (
                    "¿Los grupos comparten un objeto mutable?",
                    "Do groups share a mutable object?",
                    "Deler grupper et muterbart objekt?",
                ),
                (
                    "¿El esquema fue validado?",
                    "Was the schema validated?",
                    "Blev skemaet valideret?",
                ),
                ("¿Importan los duplicados?", "Do duplicates matter?", "Betyder dubletter noget?"),
                (
                    "¿Qué pregunta responde la operación de conjunto?",
                    "What question does the set operation answer?",
                    "Hvilket spørgsmål besvarer mængdeoperationen?",
                ),
                (
                    "¿Importa la dirección de la diferencia?",
                    "Does difference direction matter?",
                    "Betyder retningen af differensen noget?",
                ),
                (
                    "¿Qué semántica debe conservarse?",
                    "Which semantics must be preserved?",
                    "Hvilken semantik skal bevares?",
                ),
            )
        ),
        tuple(
            (es, en, da)
            for es, en, da in (
                (
                    "Distingue claves de valores.",
                    "Distinguishes keys from values.",
                    "Skelner nøgler fra værdier.",
                ),
                (
                    "Elige acceso estricto o tolerante con justificación.",
                    "Chooses strict or tolerant access with justification.",
                    "Vælger streng eller tolerant adgang med begrundelse.",
                ),
                (
                    "Construye conteos correctos.",
                    "Builds correct counts.",
                    "Bygger korrekte optællinger.",
                ),
                (
                    "Agrupa sin aliasing accidental.",
                    "Groups without accidental aliasing.",
                    "Grupperer uden utilsigtet aliasing.",
                ),
                (
                    "Valida registros anidados.",
                    "Validates nested records.",
                    "Validerer indlejrede poster.",
                ),
                (
                    "Usa conjuntos sin perder información necesaria.",
                    "Uses sets without losing required information.",
                    "Bruger mængder uden at miste nødvendige oplysninger.",
                ),
                (
                    "Aplica operaciones de conjuntos correctamente.",
                    "Applies set operations correctly.",
                    "Anvender mængdeoperationer korrekt.",
                ),
                (
                    "Razona sobre mutación durante recorridos.",
                    "Reasons about mutation during traversal.",
                    "Ræsonnerer om mutation under gennemløb.",
                ),
                ("Diseña casos límite.", "Designs boundary cases.", "Designer grænsetilfælde."),
                (
                    "Justifica la estructura elegida.",
                    "Justifies the selected structure.",
                    "Begrunder den valgte struktur.",
                ),
            )
        ),
        tuple(
            (es, en, da)
            for es, en, da in (
                ("Dar primero una pista.", "Give a hint first.", "Giv først et hint."),
                (
                    "No confundir get con inserción.",
                    "Do not confuse get with insertion.",
                    "Forveksl ikke get med indsættelse.",
                ),
                (
                    "Explicitar si la ausencia es error.",
                    "State whether absence is an error.",
                    "Angiv om fravær er en fejl.",
                ),
                (
                    "Mostrar la dirección de la diferencia.",
                    "Show difference direction.",
                    "Vis differensens retning.",
                ),
                (
                    "Advertir pérdida de duplicados al usar set.",
                    "Warn about duplicate loss with set.",
                    "Advar om tab af dubletter ved set.",
                ),
                (
                    "No depender del orden visual de un conjunto.",
                    "Do not rely on visual set order.",
                    "Afhæng ikke af en mængdes visuelle rækkefølge.",
                ),
                (
                    "Separar validación y cálculo.",
                    "Separate validation and computation.",
                    "Adskil validering og beregning.",
                ),
                (
                    "No presentar ejemplos didácticos como protocolos.",
                    "Do not present teaching examples as protocols.",
                    "Præsenter ikke undervisningseksempler som protokoller.",
                ),
                (
                    "Relacionar cada estructura con su contrato.",
                    "Relate each structure to its contract.",
                    "Knyt hver struktur til dens kontrakt.",
                ),
            )
        ),
        (
            "Official DM857 course description, SDU, active version approved in 2025.",
            "Think Python, third edition, chapters on dictionaries and tuples.",
            "Introduction to Computation and Programming Using Python, third edition, sections on dictionaries, sets, and testing.",
        ),
    ),
)

_BANK_07_MCQ = (
    (
        "001",
        ("¿Qué consulta key in d?", "What does key in d test?", "Hvad tester key in d?"),
        (
            ("keys", ("Claves", "Keys", "Nøgler")),
            ("values", ("Valores", "Values", "Værdier")),
            ("pairs", ("Pares", "Pairs", "Par")),
            ("positions", ("Posiciones", "Positions", "Positioner")),
        ),
        "keys",
        ("in consulta claves.", "in checks keys.", "in kontrollerer nøgler."),
    ),
    (
        "003",
        (
            "¿Qué método retorna un predeterminado sin insertar?",
            "Which method returns a default without inserting?",
            "Hvilken metode returnerer en standard uden indsættelse?",
        ),
        (
            ("get", ("get", "get", "get")),
            ("setdefault", ("setdefault", "setdefault", "setdefault")),
            ("pop", ("pop", "pop", "pop")),
            ("update", ("update", "update", "update")),
        ),
        "get",
        (
            "get no modifica el diccionario.",
            "get does not modify the dictionary.",
            "get ændrer ikke ordbogen.",
        ),
    ),
    (
        "005",
        (
            "¿Qué método entrega pares clave-valor?",
            "Which method yields key-value pairs?",
            "Hvilken metode giver nøgle-værdi-par?",
        ),
        (
            ("items", ("items", "items", "items")),
            ("keys", ("keys", "keys", "keys")),
            ("values", ("values", "values", "values")),
            ("get", ("get", "get", "get")),
        ),
        "items",
        ("items produce pares.", "items yields pairs.", "items giver par."),
    ),
    (
        "007",
        (
            "¿Qué patrón incrementa una frecuencia?",
            "Which pattern increments a frequency?",
            "Hvilket mønster øger en frekvens?",
        ),
        (
            ("get", ("c[k] = c.get(k, 0) + 1", "c[k] = c.get(k, 0) + 1", "c[k] = c.get(k, 0) + 1")),
            ("replace", ("c = {k: 1}", "c = {k: 1}", "c = {k: 1}")),
            ("clear", ("c.clear()", "c.clear()", "c.clear()")),
            ("values", ("c.values()", "c.values()", "c.values()")),
        ),
        "get",
        (
            "El patrón conserva conteos previos.",
            "The pattern preserves prior counts.",
            "Mønsteret bevarer tidligere antal.",
        ),
    ),
    (
        "009",
        (
            "¿Qué crea grupos independientes?",
            "What creates independent groups?",
            "Hvad opretter uafhængige grupper?",
        ),
        (
            (
                "comprehension",
                ("{k: [] for k in keys}", "{k: [] for k in keys}", "{k: [] for k in keys}"),
            ),
            (
                "fromkeys",
                ("dict.fromkeys(keys, [])", "dict.fromkeys(keys, [])", "dict.fromkeys(keys, [])"),
            ),
            (
                "same",
                (
                    "shared = []; {k: shared for k in keys}",
                    "shared = []; {k: shared for k in keys}",
                    "shared = []; {k: shared for k in keys}",
                ),
            ),
            ("tuple", ("tuple(keys)", "tuple(keys)", "tuple(keys)")),
        ),
        "comprehension",
        (
            "La comprensión crea una lista por clave.",
            "The comprehension creates one list per key.",
            "Comprehension opretter én liste per nøgle.",
        ),
    ),
    (
        "011",
        (
            "¿Qué estructura representa pertenencia única?",
            "Which structure represents unique membership?",
            "Hvilken struktur repræsenterer unikt medlemskab?",
        ),
        (
            ("set", ("set", "set", "set")),
            ("list", ("list", "list", "list")),
            ("tuple", ("tuple", "tuple", "tuple")),
            ("str", ("str", "str", "str")),
        ),
        "set",
        ("set elimina duplicados.", "set removes duplicates.", "set fjerner dubletter."),
    ),
    (
        "013",
        (
            "¿Qué operación obtiene elementos comunes?",
            "Which operation obtains common elements?",
            "Hvilken operation finder fælles elementer?",
        ),
        (
            ("intersection", ("A & B", "A & B", "A & B")),
            ("union", ("A | B", "A | B", "A | B")),
            ("difference", ("A - B", "A - B", "A - B")),
            ("symmetric", ("A ^ B", "A ^ B", "A ^ B")),
        ),
        "intersection",
        ("& calcula intersección.", "& computes intersection.", "& beregner snit."),
    ),
    (
        "015",
        (
            "¿Qué obtiene required - observed?",
            "What does required - observed yield?",
            "Hvad giver required - observed?",
        ),
        (
            (
                "missing",
                ("Requeridos ausentes", "Missing required elements", "Manglende krævede elementer"),
            ),
            (
                "extra",
                ("Observados extra", "Extra observed elements", "Ekstra observerede elementer"),
            ),
            ("common", ("Comunes", "Common elements", "Fælles elementer")),
            ("all", ("Todos", "All", "Alle")),
        ),
        "missing",
        (
            "La diferencia parte de required.",
            "Difference starts from required.",
            "Differensen starter fra required.",
        ),
    ),
    (
        "017",
        (
            "¿Qué método elimina sin error si falta?",
            "Which method removes without error when absent?",
            "Hvilken metode fjerner uden fejl ved fravær?",
        ),
        (
            ("discard", ("discard", "discard", "discard")),
            ("remove", ("remove", "remove", "remove")),
            ("pop", ("pop", "pop", "pop")),
            ("clear", ("clear", "clear", "clear")),
        ),
        "discard",
        ("discard tolera ausencia.", "discard tolerates absence.", "discard tolererer fravær."),
    ),
    (
        "019",
        (
            "¿Qué operación conserva elementos de exactamente un conjunto?",
            "Which operation keeps elements from exactly one set?",
            "Hvilken operation beholder elementer fra præcis én mængde?",
        ),
        (
            ("symmetric", ("A ^ B", "A ^ B", "A ^ B")),
            ("intersection", ("A & B", "A & B", "A & B")),
            ("union", ("A | B", "A | B", "A | B")),
            ("subset", ("A <= B", "A <= B", "A <= B")),
        ),
        "symmetric",
        ("^ excluye la intersección.", "^ excludes intersection.", "^ udelukker snittet."),
    ),
    (
        "021",
        (
            "¿Qué estructura asocia identificadores con registros?",
            "Which structure maps identifiers to records?",
            "Hvilken struktur knytter identifikatorer til poster?",
        ),
        (
            ("dict", ("dict", "dict", "dict")),
            ("set", ("set", "set", "set")),
            ("list", ("list", "list", "list")),
            ("tuple", ("tuple", "tuple", "tuple")),
        ),
        "dict",
        (
            "El diccionario implementa una asociación.",
            "A dictionary implements a mapping.",
            "En ordbog implementerer en relation.",
        ),
    ),
    (
        "023",
        (
            "¿Qué acceso hace visible una clave obligatoria ausente?",
            "Which access exposes a missing required key?",
            "Hvilken adgang synliggør en manglende obligatorisk nøgle?",
        ),
        (
            ("index", ("d[key]", "d[key]", "d[key]")),
            ("get_none", ("d.get(key)", "d.get(key)", "d.get(key)")),
            ("values", ("d.values()", "d.values()", "d.values()")),
            ("copy", ("d.copy()", "d.copy()", "d.copy()")),
        ),
        "index",
        ("d[key] produce KeyError.", "d[key] raises KeyError.", "d[key] giver KeyError."),
    ),
    (
        "025",
        (
            "¿Qué prueba detecta una lista compartida entre grupos?",
            "Which test detects a shared list across groups?",
            "Hvilken test opdager en delt liste mellem grupper?",
        ),
        (
            (
                "mutate",
                (
                    "Añadir a un grupo y observar otro",
                    "Append to one group and observe another",
                    "Tilføj til én gruppe og observer en anden",
                ),
            ),
            (
                "len",
                (
                    "Comprobar sólo el número de claves",
                    "Check only key count",
                    "Kontrollér kun antal nøgler",
                ),
            ),
            ("print", ("Imprimir una clave", "Print one key", "Udskriv én nøgle")),
            ("sort", ("Ordenar claves", "Sort keys", "Sortér nøgler")),
        ),
        "mutate",
        (
            "La mutación compartida revela aliasing.",
            "Shared mutation reveals aliasing.",
            "Delt mutation afslører aliasing.",
        ),
    ),
    (
        "027",
        (
            "¿Qué conserva una lista que un conjunto pierde?",
            "What does a list preserve that a set loses?",
            "Hvad bevarer en liste, som en mængde mister?",
        ),
        (
            (
                "duplicates",
                ("Duplicados y posiciones", "Duplicates and positions", "Dubletter og positioner"),
            ),
            ("membership", ("Pertenencia", "Membership", "Medlemskab")),
            ("hash", ("Hash", "Hash", "Hash")),
            ("keys", ("Claves", "Keys", "Nøgler")),
        ),
        "duplicates",
        (
            "El conjunto no representa multiplicidad ni posición.",
            "A set represents neither multiplicity nor position.",
            "En mængde repræsenterer hverken multiplicitet eller position.",
        ),
    ),
    (
        "029",
        (
            "¿Qué debe ocurrir antes del acceso anidado?",
            "What should happen before nested access?",
            "Hvad bør ske før indlejret adgang?",
        ),
        (
            ("validate", ("Validar el esquema", "Validate the schema", "Validér skemaet")),
            ("sort", ("Ordenar claves", "Sort keys", "Sortér nøgler")),
            ("convert", ("Convertir a conjunto", "Convert to a set", "Konvertér til en mængde")),
            ("print", ("Imprimir", "Print", "Udskriv")),
        ),
        "validate",
        (
            "La validación protege los supuestos del cálculo.",
            "Validation protects computation assumptions.",
            "Validering beskytter beregningens antagelser.",
        ),
    ),
)
_BANK_07_TF = (
    (
        "002",
        (
            "Las claves de un diccionario pueden repetirse simultáneamente.",
            "Dictionary keys can occur more than once simultaneously.",
            "Ordbogsnøgler kan forekomme flere gange samtidigt.",
        ),
        False,
        ("Cada clave es única.", "Each key is unique.", "Hver nøgle er unik."),
    ),
    (
        "004",
        (
            "get inserta automáticamente su valor predeterminado.",
            "get automatically inserts its default value.",
            "get indsætter automatisk sin standardværdi.",
        ),
        False,
        (
            "get sólo retorna el predeterminado.",
            "get only returns the default.",
            "get returnerer kun standardværdien.",
        ),
    ),
    (
        "006",
        (
            "Modificar el tamaño de un diccionario durante su recorrido directo es seguro.",
            "Changing dictionary size during direct traversal is safe.",
            "Det er sikkert at ændre en ordbogs størrelse under direkte gennemløb.",
        ),
        False,
        (
            "Debe recorrerse una copia o construirse otro resultado.",
            "Traverse a copy or build another result.",
            "Gennemløb en kopi eller byg et andet resultat.",
        ),
    ),
    (
        "008",
        (
            "Normalizar después de contar puede fragmentar categorías.",
            "Normalizing after counting may fragment categories.",
            "Normalisering efter optælling kan fragmentere kategorier.",
        ),
        True,
        (
            "La normalización debe preceder a la clave.",
            "Normalization should precede key creation.",
            "Normalisering bør gå forud for nøglen.",
        ),
    ),
    (
        "010",
        (
            "dict.fromkeys(keys, []) crea una lista independiente por clave.",
            "dict.fromkeys(keys, []) creates an independent list per key.",
            "dict.fromkeys(keys, []) opretter en uafhængig liste per nøgle.",
        ),
        False,
        (
            "Todas las claves comparten el mismo objeto.",
            "All keys share the same object.",
            "Alle nøgler deler samme objekt.",
        ),
    ),
    (
        "012",
        (
            "Un conjunto conserva el número de apariciones de cada valor.",
            "A set preserves the number of occurrences of each value.",
            "En mængde bevarer antallet af forekomster af hver værdi.",
        ),
        False,
        (
            "Un conjunto elimina multiplicidad.",
            "A set removes multiplicity.",
            "En mængde fjerner multiplicitet.",
        ),
    ),
    (
        "014",
        (
            "A - B siempre es igual a B - A.",
            "A - B always equals B - A.",
            "A - B er altid lig B - A.",
        ),
        False,
        (
            "La diferencia es direccional.",
            "Difference is directional.",
            "Differens er retningsbestemt.",
        ),
    ),
    (
        "016",
        (
            "discard puede usarse aunque el elemento no exista.",
            "discard can be used when the element is absent.",
            "discard kan bruges, selv om elementet mangler.",
        ),
        True,
        (
            "discard no produce error por ausencia.",
            "discard does not error on absence.",
            "discard giver ikke fejl ved fravær.",
        ),
    ),
    (
        "018",
        (
            "La intersección contiene elementos presentes en ambos conjuntos.",
            "Intersection contains elements present in both sets.",
            "Snittet indeholder elementer i begge mængder.",
        ),
        True,
        (
            "Ésa es la definición de intersección.",
            "That is the definition of intersection.",
            "Det er definitionen af snit.",
        ),
    ),
    (
        "020",
        (
            "Un diccionario es preferible siempre que los datos tengan orden.",
            "A dictionary is always preferable whenever data have order.",
            "En ordbog er altid bedst, når data har rækkefølge.",
        ),
        False,
        (
            "La elección depende de operaciones y contrato.",
            "Choice depends on operations and contract.",
            "Valget afhænger af operationer og kontrakt.",
        ),
    ),
    (
        "022",
        (
            "d.values() comprueba claves.",
            "d.values() checks keys.",
            "d.values() kontrollerer nøgler.",
        ),
        False,
        ("values proporciona valores.", "values provides values.", "values giver værdier."),
    ),
    (
        "024",
        (
            "Una tupla inmutable puede servir como clave.",
            "An immutable tuple can serve as a key.",
            "En uforanderlig tuple kan bruges som nøgle.",
        ),
        True,
        (
            "Sus componentes también deben ser hashables.",
            "Its components must also be hashable.",
            "Dens komponenter skal også være hashbare.",
        ),
    ),
    (
        "026",
        (
            "setdefault puede crear un grupo antes de añadir.",
            "setdefault can create a group before appending.",
            "setdefault kan oprette en gruppe før tilføjelse.",
        ),
        True,
        (
            "Retorna el valor existente o inserta el predeterminado.",
            "It returns the existing value or inserts the default.",
            "Den returnerer den eksisterende værdi eller indsætter standarden.",
        ),
    ),
    (
        "028",
        (
            "Las operaciones de conjuntos deben vincularse con una pregunta concreta.",
            "Set operations should be tied to a concrete question.",
            "Mængdeoperationer bør knyttes til et konkret spørgsmål.",
        ),
        True,
        (
            "Cada operación conserva información diferente.",
            "Each operation preserves different information.",
            "Hver operation bevarer forskellige oplysninger.",
        ),
    ),
    (
        "030",
        (
            "Los ejemplos del módulo son protocolos clínicos.",
            "The module examples are clinical protocols.",
            "Modulets eksempler er kliniske protokoller.",
        ),
        False,
        (
            "Son ejercicios de programación didácticos.",
            "They are teaching programming exercises.",
            "De er didaktiske programmeringsøvelser.",
        ),
    ),
)

LOCALIZED_OBJECTIVE_QUESTION_BANK_07 = tuple(
    sorted(
        (
            *(
                objective_mcq(f"dm857.m07.bank.{number}", prompt, options, correct, explanation)
                for number, prompt, options, correct, explanation in _BANK_07_MCQ
            ),
            *(
                objective_tf(
                    f"dm857.m07.bank.{number}", prompt, correct=correct, explanation=explanation
                )
                for number, prompt, correct, explanation in _BANK_07_TF
            ),
        ),
        key=lambda item: item.item_id,
    )
)


def materialize_module_07_question_bank(locale: AppLocale | str) -> tuple[AssessmentItem, ...]:
    resolved = locale if isinstance(locale, AppLocale) else AppLocale.resolve(locale)
    return tuple(item.materialize(resolved) for item in LOCALIZED_OBJECTIVE_QUESTION_BANK_07)


MODULE_07_MAPPINGS_SETS: LearningModule = LOCALIZED_MODULE_07_MAPPINGS_SETS.materialize(
    AppLocale.SPANISH_SPAIN
)
OBJECTIVE_QUESTION_BANK_07 = materialize_module_07_question_bank(AppLocale.SPANISH_SPAIN)

__all__ = [
    "LOCALIZED_MODULE_07_MAPPINGS_SETS",
    "LOCALIZED_OBJECTIVE_QUESTION_BANK_07",
    "MODULE_07_MAPPINGS_SETS",
    "OBJECTIVE_QUESTION_BANK_07",
    "materialize_module_07_question_bank",
]
