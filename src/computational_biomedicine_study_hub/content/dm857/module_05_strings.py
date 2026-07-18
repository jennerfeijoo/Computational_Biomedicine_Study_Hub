"""DM857 module 5: strings and text processing."""

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

LOCALIZED_MODULE_05_STRINGS = LocalizedLearningModule(
    course_code="DM857",
    module_id="dm857.m05",
    title=t(
        "Cadenas y procesamiento de texto",
        "Strings and text processing",
        "Strenge og tekstbehandling",
    ),
    summary=t(
        "Este módulo estudia las cadenas como secuencias inmutables de caracteres. Incluye índices, "
        "slicing, recorridos, búsqueda, conteo, métodos, normalización, separación, unión, validación, "
        "formato y diseño de funciones para procesar identificadores y texto biomédico de forma reproducible.",
        "This module studies strings as immutable sequences of characters. It covers indexing, slicing, "
        "traversal, search, counting, methods, normalization, splitting, joining, validation, formatting, "
        "and functions for reproducible processing of identifiers and biomedical text.",
        "Dette modul behandler strenge som uforanderlige sekvenser af tegn. Det dækker indeksering, slicing, "
        "gennemløb, søgning, optælling, metoder, normalisering, opdeling, sammenføjning, validering, formatering "
        "og funktioner til reproducerbar behandling af id'er og biomedicinsk tekst.",
    ),
    objectives=(
        objective("m05.o1", ("Interpretar cadenas como secuencias indexadas e inmutables.", "Interpret strings as indexed, immutable sequences.", "Fortolke strenge som indekserede, uforanderlige sekvenser.")),
        objective("m05.o2", ("Aplicar índices positivos, negativos y slicing sin errores de límites.", "Apply positive and negative indices and slicing without boundary errors.", "Anvende positive og negative indeks samt slicing uden grænsefejl.")),
        objective("m05.o3", ("Recorrer, buscar y contar patrones en texto.", "Traverse, search, and count patterns in text.", "Gennemløbe, søge og tælle mønstre i tekst.")),
        objective("m05.o4", ("Usar métodos de cadenas distinguiendo transformación de mutación.", "Use string methods while distinguishing transformation from mutation.", "Bruge strengmetoder og skelne mellem transformation og mutation.")),
        objective("m05.o5", ("Normalizar y validar texto mediante reglas explícitas.", "Normalize and validate text using explicit rules.", "Normalisere og validere tekst med eksplicitte regler.")),
        objective("m05.o6", ("Separar, unir y formatear campos de forma segura.", "Split, join, and format fields safely.", "Opdele, sammenføje og formatere felter sikkert.")),
        objective("m05.o7", ("Diseñar pruebas para entradas vacías, delimitadores ausentes y Unicode.", "Design tests for empty input, missing delimiters, and Unicode.", "Designe test for tomt input, manglende separatorer og Unicode.")),
        objective("m05.o8", ("Construir funciones pequeñas para pipelines de limpieza textual.", "Build small functions for text-cleaning pipelines.", "Bygge små funktioner til pipelines for tekstrensning.")),
    ),
    concepts=(
        concept(
            "string-sequence-and-immutability",
            ("Secuencia e inmutabilidad", "Sequence and immutability", "Sekvens og uforanderlighed"),
            (
                "Una cadena es una secuencia ordenada de caracteres. len devuelve su longitud y cada posición "
                "puede leerse mediante un índice. Las cadenas son inmutables: no se puede reemplazar un carácter "
                "en una posición existente. Las operaciones de transformación crean una cadena nueva, por lo que "
                "el resultado debe almacenarse o retornarse si se quiere conservar.",
                "A string is an ordered sequence of characters. len returns its length and each position can be read "
                "through an index. Strings are immutable: an existing character cannot be replaced in place. "
                "Transformation operations create a new string, so the result must be stored or returned.",
                "En streng er en ordnet sekvens af tegn. len returnerer længden, og hver position kan læses via et indeks. "
                "Strenge er uforanderlige: et eksisterende tegn kan ikke erstattes på stedet. Transformationer opretter en ny streng.",
            ),
            (
                ("El primer índice es 0.", "The first index is 0.", "Det første indeks er 0."),
                ("El último índice válido positivo es len(text) - 1.", "The last valid positive index is len(text) - 1.", "Det sidste gyldige positive indeks er len(text) - 1."),
                ("Los métodos no modifican la cadena original.", "Methods do not mutate the original string.", "Metoder ændrer ikke den oprindelige streng."),
            ),
        ),
        concept(
            "indices-and-slices",
            ("Índices y slicing", "Indices and slicing", "Indeks og slicing"),
            (
                "Los índices negativos cuentan desde el final: -1 es el último carácter. Un slice text[start:stop:step] "
                "incluye start y excluye stop. Los límites omitidos se ajustan al inicio o final según el paso. Un slice "
                "fuera del rango se recorta de forma segura, mientras que un índice individual fuera del rango produce IndexError.",
                "Negative indices count from the end: -1 is the last character. A slice text[start:stop:step] includes start "
                "and excludes stop. Omitted bounds adapt to the beginning or end according to the step. Out-of-range slices "
                "are clipped safely, whereas an out-of-range single index raises IndexError.",
                "Negative indeks tæller fra slutningen: -1 er det sidste tegn. Et slice text[start:stop:step] inkluderer start "
                "og udelukker stop. Udeladte grænser tilpasses efter step. Slices uden for intervallet beskæres sikkert, mens "
                "et enkelt ugyldigt indeks giver IndexError.",
            ),
            (
                ("stop es exclusivo.", "stop is exclusive.", "stop er eksklusiv."),
                ("text[::-1] crea una cadena invertida.", "text[::-1] creates a reversed string.", "text[::-1] opretter en omvendt streng."),
                ("Un slice puede producir la cadena vacía sin error.", "A slice may produce an empty string without error.", "Et slice kan give en tom streng uden fejl."),
            ),
        ),
        concept(
            "traversal-search-and-count",
            ("Recorrido, búsqueda y conteo", "Traversal, search, and counting", "Gennemløb, søgning og optælling"),
            (
                "Un for recorre caracteres en orden sin gestionar índices manuales. enumerate añade posición cuando se necesita. "
                "El operador in comprueba pertenencia de una subcadena; find retorna la primera posición o -1; count cuenta "
                "ocurrencias no solapadas. Para reglas más complejas puede mantenerse un contador, un indicador o un estado parcial.",
                "A for loop traverses characters in order without manual index management. enumerate adds position when needed. "
                "The in operator checks substring membership; find returns the first position or -1; count counts non-overlapping "
                "occurrences. More complex rules may use a counter, flag, or partial state.",
                "En for-løkke gennemløber tegn i rækkefølge uden manuel indeksstyring. enumerate tilføjer position ved behov. "
                "Operatoren in kontrollerer delstrenge; find returnerer første position eller -1; count tæller ikke-overlappende forekomster.",
            ),
            (
                ("Recorrer caracteres suele ser más claro que recorrer índices.", "Traversing characters is often clearer than traversing indices.", "Gennemløb af tegn er ofte klarere end gennemløb af indeks."),
                ("find y index no tienen el mismo comportamiento al fallar.", "find and index behave differently when no match exists.", "find og index opfører sig forskelligt uden match."),
                ("count no cuenta coincidencias solapadas.", "count does not count overlapping matches.", "count tæller ikke overlappende match."),
            ),
        ),
        concept(
            "methods-and-normalization",
            ("Métodos y normalización", "Methods and normalization", "Metoder og normalisering"),
            (
                "strip elimina caracteres de los extremos, lower y casefold normalizan mayúsculas, replace sustituye patrones y "
                "startswith/endswith verifican prefijos o sufijos. La normalización debe definirse según el propósito: convertir todo "
                "a minúsculas puede ser correcto para comparar etiquetas, pero incorrecto si la capitalización contiene significado.",
                "strip removes characters at the ends, lower and casefold normalize case, replace substitutes patterns, and "
                "startswith/endswith check prefixes or suffixes. Normalization must follow purpose: lowercasing may be correct for "
                "label comparison but wrong when capitalization carries meaning.",
                "strip fjerner tegn i enderne, lower og casefold normaliserer store/små bogstaver, replace erstatter mønstre, og "
                "startswith/endswith kontrollerer præfikser og suffikser. Normalisering skal følge formålet.",
            ),
            (
                ("casefold es más agresivo que lower para comparación Unicode.", "casefold is more aggressive than lower for Unicode comparison.", "casefold er mere omfattende end lower til Unicode-sammenligning."),
                ("strip no elimina caracteres internos.", "strip does not remove internal characters.", "strip fjerner ikke interne tegn."),
                ("Cada método retorna una cadena nueva.", "Each method returns a new string.", "Hver metode returnerer en ny streng."),
            ),
        ),
        concept(
            "split-join-and-parsing",
            ("Separar, unir y analizar", "Splitting, joining, and parsing", "Opdeling, sammenføjning og parsing"),
            (
                "split divide una cadena en campos; join combina una secuencia de cadenas usando un separador. Antes de desempaquetar "
                "campos conviene validar su cantidad. partition siempre devuelve tres partes y puede ser útil cuando se espera un único "
                "separador. El análisis robusto distingue estructura ausente, campos vacíos y contenido inválido.",
                "split divides a string into fields; join combines a sequence of strings using a separator. Validate field count before "
                "unpacking. partition always returns three parts and is useful when one separator is expected. Robust parsing distinguishes "
                "missing structure, empty fields, and invalid content.",
                "split opdeler en streng i felter; join kombinerer en sekvens af strenge med en separator. Validér antallet af felter før "
                "udpakning. partition returnerer altid tre dele og er nyttig ved én forventet separator. Robust parsing skelner mellem "
                "manglende struktur, tomme felter og ugyldigt indhold.",
            ),
            (
                ("separator.join(parts) coloca el separador entre elementos.", "separator.join(parts) places the separator between elements.", "separator.join(parts) placerer separatoren mellem elementer."),
                ("split puede producir campos vacíos.", "split may produce empty fields.", "split kan producere tomme felter."),
                ("Validar antes de desempaquetar evita ValueError ambiguos.", "Validating before unpacking avoids ambiguous ValueError failures.", "Validering før udpakning undgår tvetydige ValueError-fejl."),
            ),
        ),
        concept(
            "validation-and-predicates",
            ("Validación y predicados", "Validation and predicates", "Validering og prædikater"),
            (
                "Métodos como isalpha, isdigit, isalnum e isspace expresan reglas sobre todos los caracteres y suelen requerir una "
                "cadena no vacía. Una regla real puede combinar longitud, prefijo, separadores y conjuntos permitidos. La validación "
                "debe retornar un bool o un resultado estructurado; mezclarla con impresión dificulta reutilización y pruebas.",
                "Methods such as isalpha, isdigit, isalnum, and isspace express rules over all characters and usually require non-empty "
                "input. A real rule may combine length, prefix, separators, and allowed sets. Validation should return a bool or structured "
                "result; mixing it with printing reduces reuse and testability.",
                "Metoder som isalpha, isdigit, isalnum og isspace udtrykker regler for alle tegn og kræver normalt ikke-tomt input. "
                "En reel regel kan kombinere længde, præfiks, separatorer og tilladte tegn. Validering bør returnere bool eller et struktureret resultat.",
            ),
            (
                ("''.isdigit() es False.", "''.isdigit() is False.", "''.isdigit() er False."),
                ("Una validación debe documentar exactamente su alfabeto permitido.", "Validation should document its exact allowed alphabet.", "Validering bør dokumentere det præcise tilladte alfabet."),
                ("La normalización puede preceder a la validación, pero ambas reglas deben ser explícitas.", "Normalization may precede validation, but both rules must be explicit.", "Normalisering kan gå forud for validering, men begge regler skal være eksplicitte."),
            ),
        ),
        concept(
            "formatting-and-reproducibility",
            ("Formato y reproducibilidad", "Formatting and reproducibility", "Formatering og reproducerbarhed"),
            (
                "Las f-strings integran valores con especificaciones de ancho, alineación y precisión. El formato debe aplicarse al presentar, "
                "no durante el cálculo, para conservar tipos numéricos. En pipelines reproducibles conviene definir separadores, codificación, "
                "capitalización y representación de valores ausentes de forma consistente.",
                "F-strings combine values with width, alignment, and precision specifications. Formatting should occur during presentation, "
                "not calculation, so numeric types are preserved. Reproducible pipelines define separators, encoding, capitalization, and "
                "missing-value representation consistently.",
                "F-strings kombinerer værdier med bredde, justering og præcision. Formatering bør ske ved præsentation, ikke under beregning, "
                "så numeriske typer bevares. Reproducerbare pipelines definerer separatorer, kodning, kapitalisering og manglende værdier konsekvent.",
            ),
            (
                ("El formato no debe sustituir la validación.", "Formatting does not replace validation.", "Formatering erstatter ikke validering."),
                ("Redondear para mostrar no implica cambiar el valor interno.", "Rounding for display need not change the internal value.", "Afrunding til visning behøver ikke ændre den interne værdi."),
                ("Una salida estable facilita comparaciones y pruebas.", "Stable output supports comparisons and tests.", "Stabilt output understøtter sammenligninger og test."),
            ),
        ),
        concept(
            "text-pipeline-design",
            ("Diseño de pipelines textuales", "Text pipeline design", "Design af tekstpipelines"),
            (
                "Un pipeline textual separa lectura, limpieza, validación, transformación y presentación. Cada etapa recibe y retorna "
                "una representación definida. El orden importa: limpiar espacios antes de validar puede ser correcto, mientras que "
                "eliminar símbolos antes de registrarlos puede ocultar errores. Las etapas deben conservar trazabilidad de decisiones.",
                "A text pipeline separates reading, cleaning, validation, transformation, and presentation. Each stage receives and returns "
                "a defined representation. Order matters: trimming before validation may be correct, whereas deleting symbols before recording "
                "them may hide errors. Stages should preserve decision traceability.",
                "En tekstpipeline adskiller læsning, rensning, validering, transformation og præsentation. Hvert trin modtager og returnerer "
                "en defineret repræsentation. Rækkefølgen betyder noget, og trinnene bør bevare sporbarhed af beslutninger.",
            ),
            (
                ("Cada etapa debe tener contrato propio.", "Each stage should have its own contract.", "Hvert trin bør have sin egen kontrakt."),
                ("La limpieza no debe ocultar silenciosamente datos inválidos.", "Cleaning should not silently hide invalid data.", "Rensning bør ikke lydløst skjule ugyldige data."),
                ("Los casos problemáticos deben poder diagnosticarse.", "Problematic cases should remain diagnosable.", "Problematiske tilfælde bør kunne diagnosticeres."),
            ),
        ),
    ),
    worked_examples=(
        example(
            "m05.e1",
            ("Normalizar un identificador", "Normalize an identifier", "Normalisér et id"),
            ("Elimina espacios externos y normaliza mayúsculas.", "Remove external spaces and normalize case.", "Fjern ydre mellemrum og normalisér store/små bogstaver."),
            (("strip trata extremos.", "strip handles the ends.", "strip håndterer enderne."), ("casefold prepara comparaciones robustas.", "casefold prepares robust comparisons.", "casefold forbereder robuste sammenligninger.")),
            "def normalize_identifier(text: str) -> str:\n    return text.strip().casefold()\n\nprint(normalize_identifier(\"  Sample-A  \"))",
            "sample-a",
            ("La cadena original no cambia; se retorna una nueva.", "The original string does not change; a new one is returned.", "Den oprindelige streng ændres ikke; en ny returneres."),
        ),
        example(
            "m05.e2",
            ("Extraer campos con partition", "Extract fields with partition", "Udtræk felter med partition"),
            ("Separa una etiqueta clave=valor y valida el separador.", "Split a key=value label and validate the separator.", "Opdel en nøgle=værdi-etiket og validér separatoren."),
            (("partition siempre entrega tres partes.", "partition always returns three parts.", "partition returnerer altid tre dele."), ("Un separador vacío indica ausencia.", "An empty separator component signals absence.", "En tom separatordel angiver fravær.")),
            "def parse_label(text: str) -> tuple[str, str] | None:\n    key, separator, value = text.partition(\"=\")\n    if not separator or not key or not value:\n        return None\n    return key.strip(), value.strip()\n\nprint(parse_label(\"gene = TP53\"))",
            "('gene', 'TP53')",
            ("La función distingue estructura ausente de campos válidos.", "The function distinguishes missing structure from valid fields.", "Funktionen skelner mellem manglende struktur og gyldige felter."),
        ),
        example(
            "m05.e3",
            ("Contar caracteres permitidos", "Count allowed characters", "Tæl tilladte tegn"),
            ("Cuenta letras, dígitos y guiones en un identificador.", "Count letters, digits, and hyphens in an identifier.", "Tæl bogstaver, cifre og bindestreger i et id."),
            (("Recorre caracteres directamente.", "Traverse characters directly.", "Gennemløb tegn direkte."), ("Un conjunto expresa pertenencia permitida.", "A set expresses allowed membership.", "Et sæt udtrykker tilladt medlemskab.")),
            "def count_allowed(text: str) -> int:\n    allowed_extra = {\"-\", \"_\"}\n    total = 0\n    for character in text:\n        if character.isalnum() or character in allowed_extra:\n            total += 1\n    return total\n\nprint(count_allowed(\"A-12?\"))",
            "4",
            ("El signo de interrogación no cumple la regla y no incrementa el contador.", "The question mark does not satisfy the rule and does not increment the counter.", "Spørgsmålstegnet opfylder ikke reglen og øger ikke tælleren."),
        ),
        example(
            "m05.e4",
            ("Formatear sin perder el valor numérico", "Format without losing the numeric value", "Formatér uden at miste den numeriske værdi"),
            ("Calcula un promedio y presenta dos decimales.", "Calculate a mean and present two decimals.", "Beregn et gennemsnit og vis to decimaler."),
            (("El cálculo retorna float.", "The calculation returns float.", "Beregningen returnerer float."), ("La presentación crea str al final.", "Presentation creates str at the end.", "Præsentationen opretter str til sidst.")),
            "def mean_two(a: float, b: float) -> float:\n    return (a + b) / 2\n\ndef format_result(value: float) -> str:\n    return f\"{value:.2f}\"\n\nresult = mean_two(3.1, 4.2)\nprint(format_result(result))",
            "3.65",
            ("Separar cálculo y formato conserva el resultado para usos posteriores.", "Separating calculation and formatting preserves the result for later use.", "Adskillelse af beregning og formatering bevarer resultatet til senere brug."),
        ),
        example(
            "m05.e5",
            ("Pipeline de limpieza y validación", "Cleaning and validation pipeline", "Pipeline til rensning og validering"),
            ("Limpia un código y valida un prefijo didáctico.", "Clean a code and validate a didactic prefix.", "Rens en kode og validér et didaktisk præfiks."),
            (("La limpieza retorna una representación canónica.", "Cleaning returns a canonical representation.", "Rensning returnerer en kanonisk repræsentation."), ("La validación opera sobre esa representación.", "Validation operates on that representation.", "Validering arbejder på denne repræsentation.")),
            "def clean_code(text: str) -> str:\n    return text.strip().upper()\n\ndef is_valid_code(text: str) -> bool:\n    return text.startswith(\"SMP-\") and text[4:].isdigit()\n\ncode = clean_code(\" smp-104 \" )\nprint(code, is_valid_code(code))",
            "SMP-104 True",
            ("Los valores son ejemplos didácticos, no identificadores clínicos oficiales.", "The values are teaching examples, not official clinical identifiers.", "Værdierne er undervisningseksempler, ikke officielle kliniske id'er."),
        ),
    ),
    practice_exercises=(
        practice("m05.p01", ActivityType.CODE_TRACING, ("Traza text[1:5:2] para text='ABCDEFG'.", "Trace text[1:5:2] for text='ABCDEFG'.", "Gennemgå text[1:5:2] for text='ABCDEFG'."), (("stop no se incluye.", "stop is excluded.", "stop er udelukket."), ("Usa posiciones 1 y 3.", "Use positions 1 and 3.", "Brug position 1 og 3.")), ("'BD'", "'BD'", "'BD'"), ("El slice toma índices 1 y 3 antes de alcanzar 5.", "The slice takes indices 1 and 3 before reaching 5.", "Slicet tager indeks 1 og 3 før 5."), "text = 'ABCDEFG'\nresult = text[1:5:2]"),
        practice("m05.p02", ActivityType.DEBUGGING, ("Corrige text[0] = 'X'.", "Fix text[0] = 'X'.", "Ret text[0] = 'X'."), (("Las cadenas son inmutables.", "Strings are immutable.", "Strenge er uforanderlige."), ("Construye una cadena nueva con slicing.", "Build a new string with slicing.", "Byg en ny streng med slicing.")), ("text = 'X' + text[1:]", "text = 'X' + text[1:]", "text = 'X' + text[1:]"), ("La reasignación sustituye el nombre por una cadena nueva.", "Reassignment binds the name to a new string.", "Gentildeling binder navnet til en ny streng."), "text = 'ABCDE'\ntext[0] = 'X'"),
        practice("m05.p03", ActivityType.FILL_IN_THE_BLANK, ("Completa: text[-1] devuelve el carácter ____.", "Complete: text[-1] returns the ____ character.", "Udfyld: text[-1] returnerer det ____ tegn."), (("Cuenta desde el final.", "Count from the end.", "Tæl fra slutningen."),), ("último", "last", "sidste"), ("-1 identifica la última posición.", "-1 identifies the last position.", "-1 identificerer den sidste position.")),
        practice("m05.p04", ActivityType.CODE_COMPLETION, ("Escribe una función que cuente guiones.", "Write a function that counts hyphens.", "Skriv en funktion, der tæller bindestreger."), (("Puedes usar count.", "You may use count.", "Du kan bruge count."), ("Retorna int.", "Return int.", "Returnér int.")), ("def count_hyphens(text: str) -> int:\n    return text.count('-')", "def count_hyphens(text: str) -> int:\n    return text.count('-')", "def count_hyphens(text: str) -> int:\n    return text.count('-')"), ("count cuenta coincidencias no solapadas.", "count counts non-overlapping matches.", "count tæller ikke-overlappende match."), "def count_hyphens(text: str) -> int:\n    # completa"),
        practice("m05.p05", ActivityType.SHORT_ANSWER, ("Explica por qué text.strip() sin asignación puede no tener efecto posterior.", "Explain why text.strip() without assignment may have no later effect.", "Forklar, hvorfor text.strip() uden tildeling muligvis ikke har senere effekt."), (("strip retorna una cadena nueva.", "strip returns a new string.", "strip returnerer en ny streng."),), ("La cadena es inmutable y strip no modifica text. Debe usarse text = text.strip() o retornarse el resultado.", "The string is immutable and strip does not mutate text. Use text = text.strip() or return the result.", "Strengen er uforanderlig, og strip ændrer ikke text. Brug text = text.strip() eller returnér resultatet."), ("Ignorar el retorno descarta la transformación.", "Ignoring the return discards the transformation.", "Ignorering af returværdien kasserer transformationen.")),
        practice("m05.p06", ActivityType.ORDERING, ("Ordena un pipeline: leer, strip, validar, transformar, formatear.", "Order a pipeline: read, strip, validate, transform, format.", "Ordén en pipeline: læs, strip, validér, transformér, formatér."), (("La validación debe operar sobre la representación prevista.", "Validation should operate on the intended representation.", "Validering bør arbejde på den tilsigtede repræsentation."),), ("1. Leer. 2. strip. 3. Validar. 4. Transformar. 5. Formatear.", "1. Read. 2. strip. 3. Validate. 4. Transform. 5. Format.", "1. Læs. 2. strip. 3. Validér. 4. Transformér. 5. Formatér."), ("El orden hace explícitas las decisiones de limpieza.", "The order makes cleaning decisions explicit.", "Rækkefølgen gør rensningsbeslutninger eksplicitte.")),
        practice("m05.p07", ActivityType.DATA_INTERPRETATION, ("find devolvió -1. ¿Qué significa?", "find returned -1. What does it mean?", "find returnerede -1. Hvad betyder det?"), (("No es el último índice.", "It is not the last index.", "Det er ikke det sidste indeks."),), ("La subcadena no fue encontrada.", "The substring was not found.", "Delstrengen blev ikke fundet."), ("find usa -1 como centinela de ausencia.", "find uses -1 as an absence sentinel.", "find bruger -1 som stopværdi for fravær.")),
        practice("m05.p08", ActivityType.CODE_COMPLETION, ("Completa una validación de texto no vacío y alfanumérico.", "Complete validation for non-empty alphanumeric text.", "Færdiggør validering af ikke-tom alfanumerisk tekst."), (("isalnum ya es False para cadena vacía.", "isalnum is already False for an empty string.", "isalnum er allerede False for en tom streng."),), ("return text.isalnum()", "return text.isalnum()", "return text.isalnum()"), ("El predicado combina no vacío y caracteres alfanuméricos.", "The predicate combines non-empty input and alphanumeric characters.", "Prædikatet kombinerer ikke-tomt input og alfanumeriske tegn."), "def is_simple_code(text: str) -> bool:\n    # completa"),
        practice("m05.p09", ActivityType.ORAL_EXPLANATION, ("Compara lower y casefold.", "Compare lower and casefold.", "Sammenlign lower og casefold."), (("Piensa en Unicode.", "Think about Unicode.", "Tænk på Unicode."),), ("Ambos normalizan mayúsculas, pero casefold aplica transformaciones Unicode más amplias para comparación sin distinción de caso.", "Both normalize case, but casefold applies broader Unicode transformations for case-insensitive comparison.", "Begge normaliserer store/små bogstaver, men casefold anvender bredere Unicode-transformationer til sammenligning uden forskel på store og små bogstaver."), ("La elección depende del propósito de normalización.", "The choice depends on normalization purpose.", "Valget afhænger af normaliseringsformålet.")),
        practice("m05.p10", ActivityType.DEBUGGING, ("Corrige key, value = text.split('=') cuando pueden existir varios '='.", "Fix key, value = text.split('=') when multiple '=' may occur.", "Ret key, value = text.split('=') når flere '=' kan forekomme."), (("Limita la división o usa partition.", "Limit splitting or use partition.", "Begræns opdelingen eller brug partition."),), ("key, separator, value = text.partition('='); validar separator.", "key, separator, value = text.partition('='); validate separator.", "key, separator, value = text.partition('='); validér separator."), ("partition separa sólo en la primera coincidencia y siempre retorna tres partes.", "partition splits only at the first match and always returns three parts.", "partition opdeler kun ved første match og returnerer altid tre dele."), "key, value = text.split('=')"),
        practice("m05.p11", ActivityType.SHORT_ANSWER, ("Diseña tres casos límite para parse_label.", "Design three boundary cases for parse_label.", "Design tre grænsetilfælde for parse_label."), (("Incluye separador ausente y campos vacíos.", "Include missing separator and empty fields.", "Medtag manglende separator og tomme felter."),), ("Sin '=', clave vacía '=x', valor vacío 'x=', y opcionalmente espacios alrededor.", "No '=', empty key '=x', empty value 'x=', and optionally surrounding spaces.", "Ingen '=', tom nøgle '=x', tom værdi 'x=' og eventuelt omgivende mellemrum."), ("Los casos prueban estructura y contenido por separado.", "The cases test structure and content separately.", "Tilfældene tester struktur og indhold separat.")),
        practice("m05.p12", ActivityType.PIPELINE_DESIGN, ("Descompón un pipeline para etiquetas separadas por comas.", "Decompose a pipeline for comma-separated labels.", "Dekomponér en pipeline til kommaseparerede etiketter."), (("Incluye limpieza por campo.", "Include per-field cleaning.", "Medtag rensning pr. felt."),), ("split_labels(text)->list[str], clean_label(label)->str, is_valid_label(label)->bool, join_labels(labels)->str y una coordinadora.", "split_labels(text)->list[str], clean_label(label)->str, is_valid_label(label)->bool, join_labels(labels)->str, and a coordinator.", "split_labels(text)->list[str], clean_label(label)->str, is_valid_label(label)->bool, join_labels(labels)->str og en koordinator."), ("Las responsabilidades separadas permiten probar delimitación, limpieza y validación.", "Separate responsibilities allow delimiter, cleaning, and validation tests.", "Adskilte ansvarsområder gør test af separator, rensning og validering mulig.")),
    ),
    assessment_items=(
        authored_item("dm857.m05.assessment.001", ActivityType.CODE_TRACING, ("Predice 'ABCDE'[1:4].", "Predict 'ABCDE'[1:4].", "Forudsig 'ABCDE'[1:4]."), (("'BCD'", "'BCD'", "'BCD'"),), ("Incluye 1 y excluye 4.", "It includes 1 and excludes 4.", "Det inkluderer 1 og udelukker 4.")),
        authored_item("dm857.m05.assessment.002", ActivityType.DEBUGGING, ("Corrige una asignación a text[2].", "Fix an assignment to text[2].", "Ret en tildeling til text[2]."), (("Construir una cadena nueva con slicing o replace según el contrato.", "Build a new string with slicing or replace according to the contract.", "Byg en ny streng med slicing eller replace efter kontrakten."),), ("Las cadenas son inmutables.", "Strings are immutable.", "Strenge er uforanderlige.")),
        authored_item("dm857.m05.assessment.003", ActivityType.FILL_IN_THE_BLANK, ("Completa: el límite stop de un slice es ____.", "Complete: the stop bound of a slice is ____.", "Udfyld: stop-grænsen i et slice er ____."), (("exclusivo", "exclusive", "eksklusiv"),), ("El carácter en stop no se incluye.", "The character at stop is excluded.", "Tegnet ved stop er udelukket.")),
        authored_item("dm857.m05.assessment.004", ActivityType.MULTIPLE_SELECT, ("Selecciona operaciones que crean una cadena nueva.", "Select operations that create a new string.", "Vælg operationer, der opretter en ny streng."), (), ("Las transformaciones de cadenas no mutan el original.", "String transformations do not mutate the original.", "Strengtransformationer ændrer ikke originalen."), options=(("strip", ("strip", "strip", "strip")), ("replace", ("replace", "replace", "replace")), ("lower", ("lower", "lower", "lower")), ("index_assign", ("text[0] = 'A'", "text[0] = 'A'", "text[0] = 'A'"))), correct_option_ids=("strip", "replace", "lower")),
        authored_item("dm857.m05.assessment.005", ActivityType.MATCHING, ("Relaciona método y resultado de ausencia.", "Match method and absence result.", "Match metode og resultat ved fravær."), (), ("find→-1; in→False; partition→separador vacío.", "find→-1; in→False; partition→empty separator.", "find→-1; in→False; partition→tom separator."), options=(("find", ("find → -1", "find → -1", "find → -1")), ("membership", ("in → False", "in → False", "in → False")), ("partition", ("partition → separador vacío", "partition → empty separator", "partition → tom separator"))), correct_option_ids=("find", "membership", "partition")),
        authored_item("dm857.m05.assessment.006", ActivityType.ORDERING, ("Ordena limpieza, validación y formato.", "Order cleaning, validation, and formatting.", "Ordén rensning, validering og formatering."), (), ("Limpiar, validar, transformar, formatear.", "Clean, validate, transform, format.", "Rens, validér, transformér, formatér."), options=(("clean", ("Limpiar", "Clean", "Rens")), ("validate", ("Validar", "Validate", "Validér")), ("transform", ("Transformar", "Transform", "Transformér")), ("format", ("Formatear", "Format", "Formatér"))), correct_option_ids=("clean", "validate", "transform", "format")),
        authored_item("dm857.m05.assessment.007", ActivityType.CODE_COMPLETION, ("Implementa first_character o None para cadena vacía.", "Implement first_character or None for empty input.", "Implementér first_character eller None for tomt input."), (("def first_character(text):\n    if not text:\n        return None\n    return text[0]", "def first_character(text):\n    if not text:\n        return None\n    return text[0]", "def first_character(text):\n    if not text:\n        return None\n    return text[0]"),), ("La condición evita IndexError.", "The condition avoids IndexError.", "Betingelsen undgår IndexError.")),
        authored_item("dm857.m05.assessment.008", ActivityType.SHORT_ANSWER, ("Explica por qué split puede producir campos vacíos.", "Explain why split may produce empty fields.", "Forklar, hvorfor split kan producere tomme felter."), (("Separadores consecutivos o situados en extremos delimitan contenido de longitud cero.", "Consecutive separators or separators at the ends delimit zero-length content.", "Gentagne separatorer eller separatorer i enderne afgrænser indhold med længde nul."),), ("La estructura debe validarse antes de desempaquetar.", "Structure should be validated before unpacking.", "Strukturen bør valideres før udpakning.")),
        authored_item("dm857.m05.assessment.009", ActivityType.DATA_INTERPRETATION, ("Interpreta count('ana') en 'banana'.", "Interpret count('ana') in 'banana'.", "Fortolk count('ana') i 'banana'."), (("1, porque count no cuenta coincidencias solapadas.", "1, because count does not count overlapping matches.", "1, fordi count ikke tæller overlappende match."),), ("Las coincidencias posibles se solapan.", "The possible matches overlap.", "De mulige match overlapper.")),
        authored_item("dm857.m05.assessment.010", ActivityType.ORAL_EXPLANATION, ("Explica cuándo casefold es preferible a lower.", "Explain when casefold is preferable to lower.", "Forklar, hvornår casefold er bedre end lower."), (("En comparación Unicode sin distinción de mayúsculas que requiere normalización más amplia.", "For Unicode case-insensitive comparison requiring broader normalization.", "Ved Unicode-sammenligning uden forskel på store og små bogstaver, der kræver bredere normalisering."),), ("La decisión depende del contrato de comparación.", "The choice depends on the comparison contract.", "Valget afhænger af sammenligningskontrakten.")),
        authored_item("dm857.m05.assessment.011", ActivityType.PIPELINE_DESIGN, ("Diseña un pipeline para códigos clave=valor.", "Design a pipeline for key=value codes.", "Design en pipeline til nøgle=værdi-koder."), (("clean_text, parse_pair, validate_key, validate_value, format_pair.", "clean_text, parse_pair, validate_key, validate_value, format_pair.", "clean_text, parse_pair, validate_key, validate_value, format_pair."),), ("Cada etapa debe distinguir error estructural de contenido inválido.", "Each stage should distinguish structural error from invalid content.", "Hvert trin bør skelne mellem strukturfejl og ugyldigt indhold.")),
        authored_item("dm857.m05.assessment.012", ActivityType.DEBUGGING, ("Corrige una prueba que espera que strip modifique text.", "Fix a test expecting strip to mutate text.", "Ret en test, der forventer, at strip ændrer text."), (("Asignar cleaned = text.strip() y comprobar cleaned, manteniendo text sin cambios.", "Assign cleaned = text.strip() and test cleaned while text remains unchanged.", "Tildel cleaned = text.strip() og test cleaned, mens text forbliver uændret."),), ("La prueba debe reflejar inmutabilidad y retorno nuevo.", "The test should reflect immutability and a new return value.", "Testen bør afspejle uforanderlighed og en ny returværdi.")),
        authored_item("dm857.m05.assessment.013", ActivityType.CODE_TRACING, ("Traza enumerate('AC') y registra pares.", "Trace enumerate('AC') and record pairs.", "Gennemgå enumerate('AC') og registrér par."), (("(0, 'A'), (1, 'C')", "(0, 'A'), (1, 'C')", "(0, 'A'), (1, 'C')"),), ("enumerate produce índice y elemento.", "enumerate produces index and element.", "enumerate producerer indeks og element.")),
        authored_item("dm857.m05.assessment.014", ActivityType.SHORT_ANSWER, ("Justifica separar cálculo numérico de formato textual.", "Justify separating numeric calculation from text formatting.", "Begrund adskillelse af numerisk beregning og tekstformatering."), (("Mantiene tipos numéricos para cálculos, pruebas y reutilización; el formato se aplica sólo al presentar.", "It preserves numeric types for calculation, testing, and reuse; formatting is applied only for presentation.", "Det bevarer numeriske typer til beregning, test og genbrug; formatering anvendes kun ved præsentation."),), ("La separación evita convertir prematuramente datos en texto.", "The separation avoids premature conversion to text.", "Adskillelsen undgår for tidlig konvertering til tekst.")),
    ),
    tutor_support=tutor_support(
        (
            "Las cadenas son secuencias inmutables: permiten lectura por índice y slicing, pero toda transformación produce un objeto nuevo. "
            "Los índices positivos comienzan en cero, los negativos cuentan desde el final y el límite stop de un slice es exclusivo. "
            "Recorrer caracteres suele ser más claro que gestionar índices, mientras enumerate aporta posición cuando es necesaria. "
            "in, find y count expresan búsquedas distintas y sus comportamientos de ausencia deben conocerse. strip, casefold, replace, split, "
            "partition y join permiten construir pipelines de limpieza y análisis, pero su orden debe estar definido por el contrato. La validación "
            "debe distinguir estructura ausente, campos vacíos y caracteres no permitidos. El formato pertenece a la presentación y no debe destruir "
            "tipos numéricos. Los ejemplos biomédicos son escenarios de programación didácticos y no representan protocolos ni identificadores oficiales.",
            "Strings are immutable sequences: they support indexed reads and slicing, but every transformation creates a new object. Positive "
            "indices start at zero, negative indices count from the end, and a slice stop bound is exclusive. Traversing characters is often clearer "
            "than managing indices, while enumerate adds position when needed. in, find, and count express different searches and their absence behavior "
            "must be understood. strip, casefold, replace, split, partition, and join support cleaning and parsing pipelines, but their order follows the "
            "contract. Validation distinguishes missing structure, empty fields, and forbidden characters. Formatting belongs to presentation and should "
            "not destroy numeric types. Biomedical examples are programming exercises, not protocols or official identifiers.",
            "Strenge er uforanderlige sekvenser: de understøtter indekseret læsning og slicing, men hver transformation opretter et nyt objekt. Positive "
            "indeks starter ved nul, negative indeks tæller fra slutningen, og stop-grænsen i et slice er eksklusiv. Gennemløb af tegn er ofte klarere end "
            "manuel indeksstyring. in, find og count udtrykker forskellige søgninger. strip, casefold, replace, split, partition og join understøtter rensning "
            "og parsing, men rækkefølgen følger kontrakten. Validering skelner mellem manglende struktur, tomme felter og forbudte tegn. Biomedicinske "
            "eksempler er programmeringsøvelser og ikke protokoller eller officielle id'er.",
        ),
        (
            ("Las cadenas son inmutables.", "Strings are immutable.", "Strenge er uforanderlige."),
            ("El primer índice es 0.", "The first index is 0.", "Det første indeks er 0."),
            ("-1 representa el último carácter.", "-1 represents the last character.", "-1 repræsenterer det sidste tegn."),
            ("El stop de un slice es exclusivo.", "A slice stop is exclusive.", "Stop i et slice er eksklusiv."),
            ("Un índice inválido produce IndexError.", "An invalid index raises IndexError.", "Et ugyldigt indeks giver IndexError."),
            ("Un slice fuera de rango se recorta.", "An out-of-range slice is clipped.", "Et slice uden for intervallet beskæres."),
            ("find retorna -1 si no encuentra.", "find returns -1 when absent.", "find returnerer -1 ved fravær."),
            ("count no cuenta solapamientos.", "count does not count overlaps.", "count tæller ikke overlap."),
            ("strip sólo actúa en extremos.", "strip acts only at the ends.", "strip virker kun i enderne."),
            ("casefold favorece comparación Unicode.", "casefold supports Unicode comparison.", "casefold understøtter Unicode-sammenligning."),
            ("split puede producir campos vacíos.", "split may produce empty fields.", "split kan producere tomme felter."),
            ("partition siempre retorna tres partes.", "partition always returns three parts.", "partition returnerer altid tre dele."),
            ("join inserta el separador entre elementos.", "join inserts the separator between elements.", "join indsætter separatoren mellem elementer."),
            ("La validación debe retornar información reutilizable.", "Validation should return reusable information.", "Validering bør returnere genanvendelig information."),
        ),
        (
            ("Intentar asignar a un índice de cadena.", "Trying to assign to a string index.", "At forsøge at tildele til et strengindeks."),
            ("Creer que stop se incluye.", "Believing stop is included.", "At tro, at stop inkluderes."),
            ("Confundir find=-1 con último índice.", "Confusing find=-1 with the last index.", "At forveksle find=-1 med sidste indeks."),
            ("Ignorar el retorno de strip o replace.", "Ignoring the return from strip or replace.", "At ignorere returværdien fra strip eller replace."),
            ("Desempaquetar split sin validar campos.", "Unpacking split without validating fields.", "At udpakke split uden at validere felter."),
            ("Suponer que count incluye solapamientos.", "Assuming count includes overlaps.", "At antage, at count inkluderer overlap."),
            ("Convertir números a texto demasiado pronto.", "Converting numbers to text too early.", "At konvertere tal til tekst for tidligt."),
            ("Normalizar sin definir propósito.", "Normalizing without defining purpose.", "At normalisere uden at definere formålet."),
            ("Eliminar silenciosamente símbolos inválidos.", "Silently deleting invalid symbols.", "Lydløst at slette ugyldige symboler."),
            ("Probar sólo ASCII.", "Testing only ASCII.", "Kun at teste ASCII."),
            ("Mezclar lectura, limpieza y validación.", "Mixing reading, cleaning, and validation.", "At blande læsning, rensning og validering."),
            ("Usar index cuando la ausencia es esperable.", "Using index when absence is expected.", "At bruge index, når fravær er forventeligt."),
        ),
        (
            ("¿Qué longitud tiene la cadena?", "What is the string length?", "Hvad er strengens længde?"),
            ("¿Qué índices exactos toma el slice?", "Which exact indices does the slice take?", "Hvilke præcise indeks tager slicet?"),
            ("¿La operación modifica o retorna?", "Does the operation mutate or return?", "Ændrer operationen eller returnerer den?"),
            ("¿Qué significa -1 en este método?", "What does -1 mean for this method?", "Hvad betyder -1 for denne metode?"),
            ("¿Puede haber campos vacíos?", "Can empty fields occur?", "Kan der forekomme tomme felter?"),
            ("¿Qué regla de normalización se aplica?", "Which normalization rule applies?", "Hvilken normaliseringsregel gælder?"),
            ("¿Se conserva la cadena original?", "Is the original string preserved?", "Bevares den oprindelige streng?"),
            ("¿Qué ocurre con Unicode?", "What happens with Unicode?", "Hvad sker der med Unicode?"),
            ("¿La validación distingue ausencia e invalidez?", "Does validation distinguish absence from invalidity?", "Skelner validering mellem fravær og ugyldighed?"),
            ("¿Cuándo se convierte a texto?", "When is the value converted to text?", "Hvornår konverteres værdien til tekst?"),
            ("¿Qué etapa debe registrar el error?", "Which stage should record the error?", "Hvilket trin bør registrere fejlen?"),
            ("¿Qué casos límite faltan?", "Which boundary cases are missing?", "Hvilke grænsetilfælde mangler?"),
        ),
        (
            ("Calcula índices y slices correctamente.", "Computes indices and slices correctly.", "Beregner indeks og slices korrekt."),
            ("Reconoce inmutabilidad.", "Recognizes immutability.", "Genkender uforanderlighed."),
            ("Distingue métodos de búsqueda.", "Distinguishes search methods.", "Skelner mellem søgemetoder."),
            ("Normaliza con una regla explícita.", "Normalizes using an explicit rule.", "Normaliserer med en eksplicit regel."),
            ("Valida estructura y contenido.", "Validates structure and content.", "Validerer struktur og indhold."),
            ("Usa split, partition y join adecuadamente.", "Uses split, partition, and join appropriately.", "Bruger split, partition og join korrekt."),
            ("Separa cálculo y formato.", "Separates calculation and formatting.", "Adskiller beregning og formatering."),
            ("Prueba entradas vacías y Unicode.", "Tests empty input and Unicode.", "Tester tomt input og Unicode."),
            ("Mantiene trazabilidad del pipeline.", "Maintains pipeline traceability.", "Bevarer pipeline-sporbarhed."),
            ("Explica errores de límites.", "Explains boundary errors.", "Forklarer grænsefejl."),
        ),
        (
            ("Dar primero una pista.", "Give a hint first.", "Giv først et hint."),
            ("Enumerar índices concretos al explicar slices.", "Enumerate concrete indices when explaining slices.", "Angiv konkrete indeks ved forklaring af slices."),
            ("No afirmar que los métodos mutan la cadena.", "Do not claim methods mutate strings.", "Påstå ikke, at metoder ændrer strenge."),
            ("Distinguir find de index.", "Distinguish find from index.", "Skeln mellem find og index."),
            ("Hacer explícita la regla Unicode.", "Make the Unicode rule explicit.", "Gør Unicode-reglen eksplicit."),
            ("No ocultar datos inválidos mediante limpieza silenciosa.", "Do not hide invalid data through silent cleaning.", "Skjul ikke ugyldige data gennem lydløs rensning."),
            ("No presentar códigos didácticos como estándares clínicos.", "Do not present teaching codes as clinical standards.", "Præsenter ikke undervisningskoder som kliniske standarder."),
            ("Separar transformación y presentación.", "Separate transformation and presentation.", "Adskil transformation og præsentation."),
            ("Relacionar pruebas con contratos de texto.", "Relate tests to text contracts.", "Knyt test til tekstkontrakter."),
        ),
        (
            "Official DM857 course description, SDU, active version approved in 2025.",
            "Think Python, third edition, chapters on strings, traversal, search, and debugging.",
            "Introduction to Computation and Programming Using Python, third edition, sections on strings and structured data processing.",
        ),
    ),
)

LOCALIZED_OBJECTIVE_QUESTION_BANK_05 = (
    objective_mcq("dm857.m05.bank.001", ("¿Cuál es el primer índice?", "What is the first index?", "Hvad er det første indeks?"), (("zero", ("0", "0", "0")), ("one", ("1", "1", "1")), ("minus", ("-1", "-1", "-1")), ("len", ("len(text)", "len(text)", "len(text)"))), "zero", ("Python indexa desde cero.", "Python indexes from zero.", "Python indekserer fra nul.")),
    objective_tf("dm857.m05.bank.002", ("Las cadenas son mutables.", "Strings are mutable.", "Strenge er muterbare."), correct=False, explanation=("Las transformaciones crean cadenas nuevas.", "Transformations create new strings.", "Transformationer opretter nye strenge.")),
    objective_mcq("dm857.m05.bank.003", ("¿Qué índice representa el último carácter?", "Which index represents the last character?", "Hvilket indeks repræsenterer det sidste tegn?"), (("minus1", ("-1", "-1", "-1")), ("zero", ("0", "0", "0")), ("len", ("len(text)", "len(text)", "len(text)")), ("one", ("1", "1", "1"))), "minus1", ("Los índices negativos cuentan desde el final.", "Negative indices count from the end.", "Negative indeks tæller fra slutningen.")),
    objective_tf("dm857.m05.bank.004", ("El stop de un slice se incluye.", "A slice stop is included.", "Stop i et slice inkluderes."), correct=False, explanation=("El límite stop es exclusivo.", "The stop bound is exclusive.", "Stop-grænsen er eksklusiv.")),
    objective_mcq("dm857.m05.bank.005", ("¿Qué produce 'ABCDE'[1:4]?", "What does 'ABCDE'[1:4] produce?", "Hvad producerer 'ABCDE'[1:4]?"), (("bcd", ("'BCD'", "'BCD'", "'BCD'")), ("bcde", ("'BCDE'", "'BCDE'", "'BCDE'")), ("abc", ("'ABC'", "'ABC'", "'ABC'")), ("cd", ("'CD'", "'CD'", "'CD'"))), "bcd", ("Toma índices 1, 2 y 3.", "It takes indices 1, 2, and 3.", "Det tager indeks 1, 2 og 3.")),
    objective_tf("dm857.m05.bank.006", ("Un slice fuera de rango siempre produce IndexError.", "An out-of-range slice always raises IndexError.", "Et slice uden for intervallet giver altid IndexError."), correct=False, explanation=("Los límites del slice se recortan.", "Slice bounds are clipped.", "Slice-grænser beskæres.")),
    objective_mcq("dm857.m05.bank.007", ("¿Qué retorna find si no encuentra?", "What does find return when no match exists?", "Hvad returnerer find uden match?"), (("minus1", ("-1", "-1", "-1")), ("none", ("None", "None", "None")), ("false", ("False", "False", "False")), ("error", ("Siempre error", "Always error", "Altid fejl"))), "minus1", ("find usa -1 como señal de ausencia.", "find uses -1 as an absence signal.", "find bruger -1 som signal for fravær.")),
    objective_tf("dm857.m05.bank.008", ("count cuenta coincidencias solapadas.", "count counts overlapping matches.", "count tæller overlappende match."), correct=False, explanation=("count usa coincidencias no solapadas.", "count uses non-overlapping matches.", "count bruger ikke-overlappende match.")),
    objective_mcq("dm857.m05.bank.009", ("¿Qué método elimina espacios externos?", "Which method removes external spaces?", "Hvilken metode fjerner ydre mellemrum?"), (("strip", ("strip", "strip", "strip")), ("split", ("split", "split", "split")), ("join", ("join", "join", "join")), ("find", ("find", "find", "find"))), "strip", ("strip actúa en los extremos.", "strip acts at the ends.", "strip virker i enderne.")),
    objective_tf("dm857.m05.bank.010", ("strip elimina todos los espacios internos.", "strip removes all internal spaces.", "strip fjerner alle interne mellemrum."), correct=False, explanation=("Sólo elimina caracteres de los extremos.", "It removes characters only at the ends.", "Den fjerner kun tegn i enderne.")),
    objective_mcq("dm857.m05.bank.011", ("¿Qué método es más amplio para comparación Unicode sin mayúsculas?", "Which method is broader for Unicode case-insensitive comparison?", "Hvilken metode er bredere til Unicode-sammenligning uden forskel på store og små bogstaver?"), (("casefold", ("casefold", "casefold", "casefold")), ("lower", ("lower", "lower", "lower")), ("upper", ("upper", "upper", "upper")), ("strip", ("strip", "strip", "strip"))), "casefold", ("casefold aplica normalización de caso más amplia.", "casefold applies broader case normalization.", "casefold anvender bredere normalisering af store/små bogstaver.")),
    objective_tf("dm857.m05.bank.012", ("''.isdigit() es True.", "''.isdigit() is True.", "''.isdigit() er True."), correct=False, explanation=("Los predicados de este tipo son False para cadena vacía.", "These predicates are False for an empty string.", "Disse prædikater er False for en tom streng.")),
    objective_mcq("dm857.m05.bank.013", ("¿Qué combina campos con un separador?", "What combines fields with a separator?", "Hvad kombinerer felter med en separator?"), (("join", ("join", "join", "join")), ("split", ("split", "split", "split")), ("find", ("find", "find", "find")), ("count", ("count", "count", "count"))), "join", ("separator.join(parts) inserta el separador.", "separator.join(parts) inserts the separator.", "separator.join(parts) indsætter separatoren.")),
    objective_tf("dm857.m05.bank.014", ("split puede producir cadenas vacías entre separadores consecutivos.", "split can produce empty strings between consecutive separators.", "split kan producere tomme strenge mellem gentagne separatorer."), correct=True, explanation=("Dos separadores delimitan un campo de longitud cero.", "Two separators delimit a zero-length field.", "To separatorer afgrænser et felt med længde nul.")),
    objective_mcq("dm857.m05.bank.015", ("¿Cuántas partes retorna partition?", "How many parts does partition return?", "Hvor mange dele returnerer partition?"), (("three", ("3", "3", "3")), ("two", ("2", "2", "2")), ("variable", ("Variable", "Variable", "Variabel")), ("one", ("1", "1", "1"))), "three", ("Antes, separador y después.", "Before, separator, and after.", "Før, separator og efter.")),
    objective_tf("dm857.m05.bank.016", ("partition es útil cuando se espera un único separador principal.", "partition is useful when one main separator is expected.", "partition er nyttig, når én hovedseparator forventes."), correct=True, explanation=("Separa en la primera coincidencia y conserva el resto.", "It splits at the first match and preserves the rest.", "Den opdeler ved første match og bevarer resten.")),
    objective_mcq("dm857.m05.bank.017", ("¿Qué conserva tipos numéricos?", "What preserves numeric types?", "Hvad bevarer numeriske typer?"), (("format_last", ("Formatear sólo al presentar", "Format only for presentation", "Formatér kun ved præsentation")), ("string_early", ("Convertir a str antes de calcular", "Convert to str before calculation", "Konvertér til str før beregning")), ("round_text", ("Guardar sólo texto redondeado", "Store only rounded text", "Gem kun afrundet tekst")), ("concat", ("Concatenar números como texto", "Concatenate numbers as text", "Sammenkæd tal som tekst"))), "format_last", ("El cálculo permanece numérico hasta la salida.", "Calculation remains numeric until output.", "Beregningen forbliver numerisk indtil output.")),
    objective_tf("dm857.m05.bank.018", ("Una f-string siempre cambia el valor numérico original.", "An f-string always changes the original numeric value.", "En f-string ændrer altid den oprindelige numeriske værdi."), correct=False, explanation=("Crea una representación textual nueva.", "It creates a new textual representation.", "Den opretter en ny tekstlig repræsentation.")),
    objective_mcq("dm857.m05.bank.019", ("¿Qué evita IndexError al leer el primer carácter?", "What avoids IndexError when reading the first character?", "Hvad undgår IndexError ved læsning af første tegn?"), (("check_empty", ("Comprobar que la cadena no esté vacía", "Check that the string is not empty", "Kontrollér, at strengen ikke er tom")), ("slice_none", ("Usar siempre text[0]", "Always use text[0]", "Brug altid text[0]")), ("print", ("Imprimir primero", "Print first", "Udskriv først")), ("lower", ("Aplicar lower", "Apply lower", "Anvend lower"))), "check_empty", ("Una cadena vacía no tiene índice 0.", "An empty string has no index 0.", "En tom streng har intet indeks 0.")),
    objective_tf("dm857.m05.bank.020", ("enumerate produce índice y elemento.", "enumerate produces index and element.", "enumerate producerer indeks og element."), correct=True, explanation=("Permite recorrer con posición explícita.", "It supports traversal with explicit position.", "Det understøtter gennemløb med eksplicit position.")),
    objective_mcq("dm857.m05.bank.021", ("¿Qué expresa 'abc' in text?", "What does 'abc' in text express?", "Hvad udtrykker 'abc' in text?"), (("membership", ("Pertenencia de subcadena", "Substring membership", "Medlemskab af delstreng")), ("index", ("Índice exacto", "Exact index", "Præcist indeks")), ("count", ("Número de coincidencias", "Number of matches", "Antal match")), ("mutation", ("Mutación", "Mutation", "Mutation"))), "membership", ("El resultado es bool.", "The result is bool.", "Resultatet er bool.")),
    objective_tf("dm857.m05.bank.022", ("replace modifica la cadena original.", "replace mutates the original string.", "replace ændrer den oprindelige streng."), correct=False, explanation=("Retorna una nueva cadena.", "It returns a new string.", "Den returnerer en ny streng.")),
    objective_mcq("dm857.m05.bank.023", ("¿Qué debe validarse antes de key, value = parts?", "What should be validated before key, value = parts?", "Hvad bør valideres før key, value = parts?"), (("length", ("Que haya exactamente dos campos", "That exactly two fields exist", "At der findes præcis to felter")), ("color", ("Color del texto", "Text color", "Tekstfarve")), ("case_only", ("Sólo mayúsculas", "Uppercase only", "Kun store bogstaver")), ("print", ("Que se haya impreso", "That it was printed", "At det blev udskrevet"))), "length", ("El desempaquetado exige la cantidad correcta.", "Unpacking requires the correct count.", "Udpakning kræver det korrekte antal.")),
    objective_tf("dm857.m05.bank.024", ("La limpieza debe documentar si elimina símbolos inválidos.", "Cleaning should document whether it removes invalid symbols.", "Rensning bør dokumentere, om ugyldige symboler fjernes."), correct=True, explanation=("La decisión afecta trazabilidad y significado.", "The decision affects traceability and meaning.", "Beslutningen påvirker sporbarhed og betydning.")),
    objective_mcq("dm857.m05.bank.025", ("¿Qué produce text[::-1]?", "What does text[::-1] produce?", "Hvad producerer text[::-1]?"), (("reversed", ("Una cadena invertida", "A reversed string", "En omvendt streng")), ("same", ("La misma cadena", "The same string", "Den samme streng")), ("error", ("Siempre error", "Always error", "Altid fejl")), ("list", ("Una lista", "A list", "En liste"))), "reversed", ("El paso -1 recorre desde el final.", "Step -1 traverses from the end.", "Step -1 gennemløber fra slutningen.")),
    objective_tf("dm857.m05.bank.026", ("Un slice vacío puede ser un resultado válido.", "An empty slice can be a valid result.", "Et tomt slice kan være et gyldigt resultat."), correct=True, explanation=("Los límites pueden no seleccionar caracteres.", "The bounds may select no characters.", "Grænserne kan vælge ingen tegn.")),
    objective_mcq("dm857.m05.bank.027", ("¿Qué método verifica un prefijo?", "Which method checks a prefix?", "Hvilken metode kontrollerer et præfiks?"), (("startswith", ("startswith", "startswith", "startswith")), ("endswith", ("endswith", "endswith", "endswith")), ("count", ("count", "count", "count")), ("join", ("join", "join", "join"))), "startswith", ("startswith compara el comienzo.", "startswith compares the beginning.", "startswith sammenligner begyndelsen.")),
    objective_tf("dm857.m05.bank.028", ("El orden de las etapas textuales puede cambiar el resultado.", "The order of text-processing stages can change the result.", "Rækkefølgen af tekstbehandlingstrin kan ændre resultatet."), correct=True, explanation=("Limpiar antes o después de validar no siempre es equivalente.", "Cleaning before or after validation is not always equivalent.", "Rensning før eller efter validering er ikke altid ækvivalent.")),
    objective_mcq("dm857.m05.bank.029", ("¿Qué prueba cubre Unicode?", "Which test covers Unicode?", "Hvilken test dækker Unicode?"), (("accent", ("Una entrada con acentos o caracteres no ASCII", "Input with accents or non-ASCII characters", "Input med accenter eller ikke-ASCII-tegn")), ("empty_only", ("Sólo cadena vacía", "Only empty string", "Kun tom streng")), ("digits", ("Sólo dígitos ASCII", "ASCII digits only", "Kun ASCII-cifre")), ("none", ("No hace falta", "No test needed", "Ingen test nødvendig"))), "accent", ("Los casos Unicode verifican la regla real de normalización.", "Unicode cases verify the actual normalization rule.", "Unicode-tilfælde verificerer den reelle normaliseringsregel.")),
    objective_tf("dm857.m05.bank.030", ("Los códigos del módulo son estándares clínicos oficiales.", "The module codes are official clinical standards.", "Modulets koder er officielle kliniske standarder."), correct=False, explanation=("Son ejemplos didácticos de programación.", "They are programming teaching examples.", "De er undervisningseksempler i programmering.")),
)


def materialize_module_05_question_bank(locale: AppLocale | str) -> tuple[AssessmentItem, ...]:
    resolved = locale if isinstance(locale, AppLocale) else AppLocale.resolve(locale)
    return tuple(item.materialize(resolved) for item in LOCALIZED_OBJECTIVE_QUESTION_BANK_05)


MODULE_05_STRINGS: LearningModule = LOCALIZED_MODULE_05_STRINGS.materialize(AppLocale.SPANISH_SPAIN)
OBJECTIVE_QUESTION_BANK_05 = materialize_module_05_question_bank(AppLocale.SPANISH_SPAIN)

__all__ = [
    "LOCALIZED_MODULE_05_STRINGS",
    "LOCALIZED_OBJECTIVE_QUESTION_BANK_05",
    "MODULE_05_STRINGS",
    "OBJECTIVE_QUESTION_BANK_05",
    "materialize_module_05_question_bank",
]
