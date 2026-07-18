"""DM857 module 8: files, validation, and exception handling."""

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

LOCALIZED_MODULE_08_FILES_EXCEPTIONS = LocalizedLearningModule(
    course_code="DM857",
    module_id="dm857.m08",
    title=t(
        "Archivos, validación y excepciones",
        "Files, validation, and exceptions",
        "Filer, validering og undtagelser",
    ),
    summary=t(
        "Este módulo introduce rutas, archivos de texto, codificación, gestores de contexto, lectura y escritura, CSV básico, validación, conversión, excepciones, propagación, limpieza de recursos y pruebas de fallos. El objetivo es separar entrada/salida de la lógica de análisis y hacer explícitas las fronteras de error.",
        "This module introduces paths, text files, encodings, context managers, reading and writing, basic CSV, validation, conversion, exceptions, propagation, resource cleanup, and failure testing. The goal is to separate input/output from analysis logic and make error boundaries explicit.",
        "Dette modul introducerer stier, tekstfiler, kodning, context managers, læsning og skrivning, grundlæggende CSV, validering, konvertering, undtagelser, propagation, ressourceoprydning og fejltest. Målet er at adskille input/output fra analyselogik og gøre fejlgrænser eksplicitte.",
    ),
    objectives=(
        objective(
            "m08.o1",
            (
                "Construir y manipular rutas de forma portable.",
                "Construct and manipulate paths portably.",
                "Konstruere og håndtere stier portabelt.",
            ),
        ),
        objective(
            "m08.o2",
            (
                "Abrir archivos con modo, codificación y cierre correctos.",
                "Open files with correct mode, encoding, and closure.",
                "Åbne filer med korrekt tilstand, kodning og lukning.",
            ),
        ),
        objective(
            "m08.o3",
            (
                "Elegir entre lectura completa, por líneas y mediante csv.",
                "Choose among whole-file, line-based, and csv reading.",
                "Vælge mellem helfilslæsning, linjelæsning og csv-læsning.",
            ),
        ),
        objective(
            "m08.o4",
            (
                "Escribir resultados sin mezclar representación y cálculo.",
                "Write results without mixing representation and computation.",
                "Skrive resultater uden at blande repræsentation og beregning.",
            ),
        ),
        objective(
            "m08.o5",
            (
                "Validar estructura y contenido antes del análisis.",
                "Validate structure and content before analysis.",
                "Validere struktur og indhold før analyse.",
            ),
        ),
        objective(
            "m08.o6",
            (
                "Capturar excepciones específicas y preservar información diagnóstica.",
                "Catch specific exceptions and preserve diagnostic information.",
                "Fange specifikke undtagelser og bevare diagnostisk information.",
            ),
        ),
        objective(
            "m08.o7",
            (
                "Usar try, except, else, finally y raise con contratos claros.",
                "Use try, except, else, finally, and raise with clear contracts.",
                "Bruge try, except, else, finally og raise med klare kontrakter.",
            ),
        ),
        objective(
            "m08.o8",
            (
                "Diseñar pruebas para rutas ausentes, datos corruptos y escritura fallida.",
                "Design tests for missing paths, corrupt data, and failed writes.",
                "Designe test for manglende stier, korrupte data og mislykket skrivning.",
            ),
        ),
    ),
    concepts=(
        concept(
            "paths-and-boundaries",
            (
                "Rutas y fronteras del sistema",
                "Paths and system boundaries",
                "Stier og systemgrænser",
            ),
            (
                "Una ruta identifica una ubicación, no garantiza que exista ni que sea accesible. pathlib.Path compone rutas sin concatenar separadores manualmente y permite consultar nombre, sufijo, padre y existencia. Las rutas relativas dependen del directorio de trabajo; las absolutas fijan una ubicación concreta. La aplicación debe recibir rutas como entrada y validar expectativas en la frontera.",
                "A path identifies a location but does not guarantee existence or access. pathlib.Path composes paths without manual separators and exposes name, suffix, parent, and existence. Relative paths depend on the working directory; absolute paths fix a specific location. Applications should receive paths as input and validate expectations at the boundary.",
                "En sti identificerer en placering, men garanterer ikke eksistens eller adgang. pathlib.Path sammensætter stier uden manuelle separatorer og giver navn, suffiks, overmappe og eksistens. Relative stier afhænger af arbejdsmappen; absolutte stier fastlægger en placering. Applikationen bør modtage stier som input og validere ved grænsen.",
            ),
            (
                (
                    "Path une componentes de forma portable.",
                    "Path joins components portably.",
                    "Path samler komponenter portabelt.",
                ),
                (
                    "Una ruta relativa depende del contexto de ejecución.",
                    "A relative path depends on execution context.",
                    "En relativ sti afhænger af kørselskonteksten.",
                ),
                (
                    "Existencia, tipo y permisos son comprobaciones distintas.",
                    "Existence, type, and permissions are distinct checks.",
                    "Eksistens, type og rettigheder er forskellige kontroller.",
                ),
            ),
        ),
        concept(
            "open-modes-encoding-context",
            (
                "Apertura, modos, codificación y contexto",
                "Opening, modes, encoding, and context",
                "Åbning, tilstande, kodning og kontekst",
            ),
            (
                "open necesita una ruta y un modo: r lee, w reemplaza, a añade y x exige que el archivo no exista. En texto debe declararse encoding, normalmente utf-8. with open(...) as handle garantiza el cierre incluso si ocurre una excepción. El modo incorrecto puede destruir contenido o impedir una operación, por lo que forma parte del contrato.",
                "open needs a path and mode: r reads, w replaces, a appends, and x requires a new file. Text files should declare an encoding, commonly utf-8. with open(...) as handle guarantees closure even when an exception occurs. A wrong mode may destroy content or block an operation, so mode belongs in the contract.",
                "open kræver sti og tilstand: r læser, w erstatter, a tilføjer, og x kræver en ny fil. Tekstfiler bør angive kodning, typisk utf-8. with open(...) as handle garanterer lukning selv ved en undtagelse. Forkert tilstand kan ødelægge indhold eller blokere en operation.",
            ),
            (
                (
                    "with administra la vida del recurso.",
                    "with manages resource lifetime.",
                    "with styrer ressourcens levetid.",
                ),
                (
                    "w trunca un archivo existente.",
                    "w truncates an existing file.",
                    "w afkorter en eksisterende fil.",
                ),
                (
                    "encoding hace explícita la interpretación de bytes.",
                    "encoding makes byte interpretation explicit.",
                    "encoding gør fortolkningen af bytes eksplicit.",
                ),
            ),
        ),
        concept(
            "reading-strategies",
            ("Estrategias de lectura", "Reading strategies", "Læsestrategier"),
            (
                "read carga el contenido completo; readline obtiene una línea y recorrer el archivo procesa líneas de forma incremental. strip elimina espacios en ambos extremos y puede borrar información si se usa sin criterio; rstrip('\\n') elimina sólo saltos finales especificados. Para datos delimitados, csv.reader y csv.DictReader gestionan comillas y separadores mejor que split manual.",
                "read loads all content; readline obtains one line, and iterating over the file processes incrementally. strip removes whitespace from both ends and may erase meaningful data if used carelessly; rstrip('\\n') removes specified trailing newlines only. For delimited data, csv.reader and csv.DictReader handle quoting and delimiters better than manual split.",
                "read indlæser hele indholdet; readline henter én linje, og iteration over filen behandler inkrementelt. strip fjerner whitespace i begge ender og kan slette betydningsfulde data; rstrip('\\n') fjerner kun angivne afsluttende linjeskift. Til afgrænsede data håndterer csv.reader og csv.DictReader citationstegn bedre end manuel split.",
            ),
            (
                (
                    "La estrategia depende del tamaño y del formato.",
                    "Strategy depends on size and format.",
                    "Strategien afhænger af størrelse og format.",
                ),
                (
                    "Iterar evita cargar todo el archivo.",
                    "Iteration avoids loading the whole file.",
                    "Iteration undgår at indlæse hele filen.",
                ),
                (
                    "CSV no debe analizarse con split ingenuo.",
                    "CSV should not be parsed with naive split.",
                    "CSV bør ikke analyseres med naiv split.",
                ),
            ),
        ),
        concept(
            "writing-and-representation",
            (
                "Escritura y representación",
                "Writing and representation",
                "Skrivning og repræsentation",
            ),
            (
                "La lógica de cálculo debe producir valores y una capa separada debe convertirlos a texto o filas. write espera cadenas y no añade saltos automáticamente; writelines tampoco inserta separadores. csv.writer aplica reglas de escapado. La escritura debe definir si reemplaza, añade o crea, cómo representa ausentes y qué ocurre si el destino ya existe.",
                "Computation should produce values, while a separate layer converts them to text or rows. write expects strings and adds no newline automatically; writelines also inserts no separators. csv.writer applies escaping rules. Writing must define whether it replaces, appends, or creates, how missing values are represented, and what happens if the destination exists.",
                "Beregning bør producere værdier, mens et separat lag konverterer dem til tekst eller rækker. write forventer strenge og tilføjer ikke automatisk linjeskift; writelines indsætter heller ingen separatorer. csv.writer anvender escaping. Skrivning skal definere erstatning, tilføjelse eller oprettelse og håndtering af manglende værdier.",
            ),
            (
                ("write requiere str.", "write requires str.", "write kræver str."),
                (
                    "Los separadores deben añadirse explícitamente.",
                    "Separators must be added explicitly.",
                    "Separatorer skal tilføjes eksplicit.",
                ),
                (
                    "El formato de salida es un contrato.",
                    "Output format is a contract.",
                    "Outputformatet er en kontrakt.",
                ),
            ),
        ),
        concept(
            "validation-and-conversion",
            ("Validación y conversión", "Validation and conversion", "Validering og konvertering"),
            (
                "Leer texto no produce automáticamente números ni registros válidos. La validación estructural comprueba columnas, cabeceras y número de campos; la semántica comprueba rangos, categorías y coherencia. La conversión int o float puede fallar con ValueError. Conviene conservar número de línea y valor original para informar errores precisos y decidir si se rechaza el archivo o una fila.",
                "Reading text does not automatically produce numbers or valid records. Structural validation checks columns, headers, and field counts; semantic validation checks ranges, categories, and consistency. int or float conversion may raise ValueError. Preserve line number and original value for precise errors and decide whether to reject the file or one row.",
                "Læsning af tekst producerer ikke automatisk tal eller gyldige poster. Strukturel validering kontrollerer kolonner, headere og antal felter; semantisk validering kontrollerer intervaller, kategorier og konsistens. int eller float kan give ValueError. Bevar linjenummer og original værdi for præcise fejl.",
            ),
            (
                (
                    "Validar precede al análisis.",
                    "Validation precedes analysis.",
                    "Validering går forud for analyse.",
                ),
                (
                    "Conversión y validación son pasos distintos.",
                    "Conversion and validation are distinct steps.",
                    "Konvertering og validering er forskellige trin.",
                ),
                (
                    "Los errores deben conservar contexto.",
                    "Errors should preserve context.",
                    "Fejl bør bevare kontekst.",
                ),
            ),
        ),
        concept(
            "exceptions-and-specificity",
            (
                "Excepciones y especificidad",
                "Exceptions and specificity",
                "Undtagelser og specificitet",
            ),
            (
                "Una excepción interrumpe el flujo normal y busca un manejador compatible. FileNotFoundError, PermissionError, UnicodeDecodeError, ValueError y OSError describen fallos distintos. Capturar Exception de forma amplia puede ocultar defectos de programación. Debe capturarse sólo lo que puede manejarse y permitir que lo inesperado conserve su traceback.",
                "An exception interrupts normal flow and searches for a compatible handler. FileNotFoundError, PermissionError, UnicodeDecodeError, ValueError, and OSError describe different failures. Broadly catching Exception may hide programming defects. Catch only what can be handled and let unexpected failures preserve their traceback.",
                "En undtagelse afbryder normal kontrolstrøm og søger en kompatibel handler. FileNotFoundError, PermissionError, UnicodeDecodeError, ValueError og OSError beskriver forskellige fejl. Bred fangst af Exception kan skjule programmeringsfejl. Fang kun det, der kan håndteres.",
            ),
            (
                (
                    "Captura excepciones específicas.",
                    "Catch specific exceptions.",
                    "Fang specifikke undtagelser.",
                ),
                (
                    "No silencies errores sin registrar contexto.",
                    "Do not silence errors without context.",
                    "Skjul ikke fejl uden kontekst.",
                ),
                (
                    "El traceback ayuda a localizar defectos inesperados.",
                    "The traceback helps locate unexpected defects.",
                    "Traceback hjælper med at lokalisere uventede fejl.",
                ),
            ),
        ),
        concept(
            "try-else-finally-raise",
            (
                "try, except, else, finally y raise",
                "try, except, else, finally, and raise",
                "try, except, else, finally og raise",
            ),
            (
                "El bloque try debe contener la operación que puede fallar, no código unrelated. except maneja tipos previstos; else se ejecuta sólo si no hubo excepción y separa el camino exitoso; finally se ejecuta siempre y sirve para limpieza no cubierta por un gestor de contexto. raise crea o vuelve a propagar una excepción. raise NewError(...) from error conserva la causa original.",
                "The try block should contain the operation that may fail, not unrelated code. except handles expected types; else runs only when no exception occurred and separates the success path; finally always runs and supports cleanup not handled by a context manager. raise creates or re-raises an exception. raise NewError(...) from error preserves the original cause.",
                "try-blokken bør indeholde operationen, der kan fejle, ikke uvedkommende kode. except håndterer forventede typer; else kører kun uden undtagelse og adskiller succesvejen; finally kører altid og bruges til oprydning. raise opretter eller videresender en undtagelse. raise NewError(...) from error bevarer årsagen.",
            ),
            (
                ("Mantén try pequeño.", "Keep try small.", "Hold try lille."),
                (
                    "else expresa el camino sin error.",
                    "else expresses the no-error path.",
                    "else udtrykker vejen uden fejl.",
                ),
                (
                    "from conserva causalidad.",
                    "from preserves causality.",
                    "from bevarer årsagssammenhæng.",
                ),
            ),
        ),
        concept(
            "propagation-boundaries-testing",
            (
                "Propagación, fronteras y pruebas",
                "Propagation, boundaries, and tests",
                "Propagation, grænser og test",
            ),
            (
                "Las funciones de bajo nivel deben añadir contexto técnico o propagar; las fronteras de aplicación traducen fallos a mensajes comprensibles. Una excepción propia es útil cuando expresa un concepto del dominio del programa. Las pruebas deben cubrir éxito, archivo ausente, permiso denegado simulado, codificación inválida, fila incompleta, número no convertible y limpieza de recursos.",
                "Low-level functions should add technical context or propagate; application boundaries translate failures into understandable messages. A custom exception is useful when it expresses a program-domain concept. Tests cover success, missing files, simulated permission denial, invalid encoding, incomplete rows, non-convertible numbers, and resource cleanup.",
                "Lavniveau-funktioner bør tilføje teknisk kontekst eller propagere; applikationsgrænser oversætter fejl til forståelige beskeder. En brugerdefineret undtagelse er nyttig, når den udtrykker et domænebegreb. Test dækker succes, manglende filer, simulerede rettighedsfejl, ugyldig kodning, ufuldstændige rækker og oprydning.",
            ),
            (
                (
                    "No todas las capas deben capturar.",
                    "Not every layer should catch.",
                    "Ikke alle lag bør fange.",
                ),
                (
                    "Añadir contexto no significa borrar la causa.",
                    "Adding context does not mean erasing the cause.",
                    "At tilføje kontekst betyder ikke at slette årsagen.",
                ),
                (
                    "Los fallos previstos forman parte de la suite.",
                    "Expected failures belong in the test suite.",
                    "Forventede fejl hører til i testsuiten.",
                ),
            ),
        ),
    ),
    worked_examples=(
        example(
            "read-nonempty-lines",
            ("Leer líneas no vacías", "Read non-empty lines", "Læs ikke-tomme linjer"),
            (
                "Lee un archivo UTF-8 y conserva el procesamiento incremental.",
                "Read a UTF-8 file incrementally.",
                "Læs en UTF-8-fil inkrementelt.",
            ),
            (
                (
                    "Abrir con with y encoding.",
                    "Open with with and encoding.",
                    "Åbn med with og encoding.",
                ),
                ("Recorrer líneas.", "Iterate through lines.", "Gennemløb linjer."),
                (
                    "Eliminar sólo el salto final y filtrar vacías.",
                    "Remove trailing newline only and filter empty lines.",
                    "Fjern kun afsluttende linjeskift og filtrér tomme linjer.",
                ),
            ),
            "from pathlib import Path\n\npath = Path('labels.txt')\nwith path.open('r', encoding='utf-8') as handle:\n    labels = [line.rstrip('\\n') for line in handle if line.rstrip('\\n')]\nprint(labels)",
            "['control', 'case']",
            (
                "El gestor de contexto cierra el archivo al salir.",
                "The context manager closes the file on exit.",
                "Context manageren lukker filen ved afslutning.",
            ),
        ),
        example(
            "parse-csv",
            ("Leer CSV con cabecera", "Read CSV with a header", "Læs CSV med header"),
            (
                "Convierte filas en diccionarios sin split manual.",
                "Convert rows to dictionaries without manual split.",
                "Konvertér rækker til ordbøger uden manuel split.",
            ),
            (
                ("Usar csv.DictReader.", "Use csv.DictReader.", "Brug csv.DictReader."),
                (
                    "Validar columnas obligatorias.",
                    "Validate required columns.",
                    "Validér krævede kolonner.",
                ),
                (
                    "Convertir valores después.",
                    "Convert values afterward.",
                    "Konvertér værdier bagefter.",
                ),
            ),
            "import csv\n\nwith open('values.csv', encoding='utf-8', newline='') as handle:\n    rows = list(csv.DictReader(handle))\nprint(rows[0]['sample_id'])",
            "S1",
            (
                "DictReader respeta reglas de CSV y usa la cabecera como claves.",
                "DictReader follows CSV rules and uses the header as keys.",
                "DictReader følger CSV-regler og bruger headeren som nøgler.",
            ),
        ),
        example(
            "convert-with-context",
            (
                "Convertir con contexto de línea",
                "Convert with line context",
                "Konvertér med linjekontekst",
            ),
            (
                "Informa qué línea contiene un número inválido.",
                "Report which line contains an invalid number.",
                "Rapportér hvilken linje der indeholder et ugyldigt tal.",
            ),
            (
                (
                    "Enumerar desde la línea real.",
                    "Enumerate from the real line number.",
                    "Enumerér fra det faktiske linjenummer.",
                ),
                ("Capturar ValueError.", "Catch ValueError.", "Fang ValueError."),
                (
                    "Volver a lanzar con contexto y causa.",
                    "Raise again with context and cause.",
                    "Kast igen med kontekst og årsag.",
                ),
            ),
            "def parse_value(text, line_number):\n    try:\n        return float(text)\n    except ValueError as error:\n        raise ValueError(f'line {line_number}: invalid value {text!r}') from error\n\nprint(parse_value('2.5', 3))",
            "2.5",
            (
                "from error conserva la excepción original como causa.",
                "from error preserves the original exception as cause.",
                "from error bevarer den oprindelige undtagelse som årsag.",
            ),
        ),
        example(
            "write-summary",
            ("Escribir un resumen", "Write a summary", "Skriv et resumé"),
            (
                "Separa el cálculo de la serialización.",
                "Separate computation from serialization.",
                "Adskil beregning fra serialisering.",
            ),
            (
                (
                    "Construir los valores del resumen.",
                    "Build summary values.",
                    "Byg resuméværdier.",
                ),
                ("Convertir a líneas.", "Convert to lines.", "Konvertér til linjer."),
                (
                    "Escribir con modo explícito.",
                    "Write with an explicit mode.",
                    "Skriv med eksplicit tilstand.",
                ),
            ),
            "summary = {'rows': 3, 'invalid': 1}\nlines = [f'{key}={value}\\n' for key, value in summary.items()]\nwith open('summary.txt', 'w', encoding='utf-8') as handle:\n    handle.writelines(lines)",
            "rows=3\ninvalid=1",
            (
                "w reemplaza el destino; la decisión debe ser intencional.",
                "w replaces the destination; the decision must be intentional.",
                "w erstatter destinationen; beslutningen skal være bevidst.",
            ),
        ),
        example(
            "custom-error",
            (
                "Excepción propia para esquema",
                "Custom schema exception",
                "Brugerdefineret skemaundtagelse",
            ),
            (
                "Expresa un fallo del contrato de registros.",
                "Express a record-contract failure.",
                "Udtryk en fejl i postkontrakten.",
            ),
            (
                (
                    "Definir una excepción específica.",
                    "Define a specific exception.",
                    "Definér en specifik undtagelse.",
                ),
                ("Calcular claves ausentes.", "Compute missing keys.", "Beregn manglende nøgler."),
                ("Lanzarla con detalle.", "Raise it with detail.", "Kast den med detaljer."),
            ),
            "class RecordSchemaError(ValueError):\n    pass\n\ndef validate_record(record):\n    missing = {'sample_id', 'value'} - record.keys()\n    if missing:\n        raise RecordSchemaError(f'missing keys: {sorted(missing)}')\n\nvalidate_record({'sample_id': 'S1', 'value': 2.0})",
            "Sin excepción",
            (
                "La excepción comunica el concepto de error sin perder compatibilidad con ValueError.",
                "The exception communicates the error concept while remaining a ValueError subtype.",
                "Undtagelsen kommunikerer fejlbegrebet og er stadig en subtype af ValueError.",
            ),
        ),
    ),
    practice_exercises=(
        practice(
            "m08.p01",
            ActivityType.CODE_TRACING,
            (
                "Traza Path('data') / 'values.csv'.",
                "Trace Path('data') / 'values.csv'.",
                "Gennemgå Path('data') / 'values.csv'.",
            ),
            (
                (
                    "El operador / compone componentes.",
                    "The / operator joins components.",
                    "/-operatoren samler komponenter.",
                ),
            ),
            (
                "Una ruta equivalente a data/values.csv en el sistema.",
                "A path equivalent to data/values.csv on the system.",
                "En sti svarende til data/values.csv på systemet.",
            ),
            (
                "Path usa el separador apropiado.",
                "Path uses the appropriate separator.",
                "Path bruger den passende separator.",
            ),
        ),
        practice(
            "m08.p02",
            ActivityType.FILL_IN_THE_BLANK,
            (
                "Completa: with path.open('r', encoding='____') as handle.",
                "Complete: with path.open('r', encoding='____') as handle.",
                "Udfyld: with path.open('r', encoding='____') as handle.",
            ),
            (
                (
                    "Usa la codificación habitual del proyecto.",
                    "Use the project's standard encoding.",
                    "Brug projektets standardkodning.",
                ),
            ),
            ("utf-8", "utf-8", "utf-8"),
            (
                "La codificación queda explícita.",
                "The encoding becomes explicit.",
                "Kodningen bliver eksplicit.",
            ),
        ),
        practice(
            "m08.p03",
            ActivityType.DEBUGGING,
            (
                "Corrige open(path, 'w') cuando sólo se quería leer.",
                "Fix open(path, 'w') when the intent was only to read.",
                "Ret open(path, 'w'), når hensigten kun var læsning.",
            ),
            (("w puede truncar.", "w may truncate.", "w kan afkorte."),),
            (
                "Usar open(path, 'r', encoding='utf-8').",
                "Use open(path, 'r', encoding='utf-8').",
                "Brug open(path, 'r', encoding='utf-8').",
            ),
            (
                "El modo debe corresponder a la operación.",
                "Mode must match the operation.",
                "Tilstanden skal passe til operationen.",
            ),
        ),
        practice(
            "m08.p04",
            ActivityType.CODE_COMPLETION,
            (
                "Escribe read_text(path) con cierre garantizado.",
                "Write read_text(path) with guaranteed closure.",
                "Skriv read_text(path) med garanteret lukning.",
            ),
            (("Usa un gestor de contexto.", "Use a context manager.", "Brug en context manager."),),
            (
                "def read_text(path):\n    with open(path, 'r', encoding='utf-8') as handle:\n        return handle.read()",
                "def read_text(path):\n    with open(path, 'r', encoding='utf-8') as handle:\n        return handle.read()",
                "def read_text(path):\n    with open(path, 'r', encoding='utf-8') as handle:\n        return handle.read()",
            ),
            (
                "El archivo se cierra al abandonar with.",
                "The file closes when leaving with.",
                "Filen lukkes ved udgang fra with.",
            ),
            "def read_text(path):\n    pass",
        ),
        practice(
            "m08.p05",
            ActivityType.ORDERING,
            (
                "Ordena: abrir, leer, validar, convertir, analizar.",
                "Order: open, read, validate, convert, analyze.",
                "Ordén: åbn, læs, validér, konvertér, analysér.",
            ),
            (
                (
                    "El análisis usa datos ya validados.",
                    "Analysis uses already validated data.",
                    "Analysen bruger allerede validerede data.",
                ),
            ),
            (
                "Abrir → leer → validar → convertir → analizar.",
                "Open → read → validate → convert → analyze.",
                "Åbn → læs → validér → konvertér → analysér.",
            ),
            (
                "La secuencia separa responsabilidades.",
                "The sequence separates responsibilities.",
                "Sekvensen adskiller ansvarsområder.",
            ),
        ),
        practice(
            "m08.p06",
            ActivityType.SHORT_ANSWER,
            (
                "Explica por qué split(',') no es un lector CSV completo.",
                "Explain why split(',') is not a complete CSV reader.",
                "Forklar, hvorfor split(',') ikke er en komplet CSV-læser.",
            ),
            (
                (
                    "Piensa en campos entre comillas.",
                    "Think about quoted fields.",
                    "Tænk på felter i citationstegn.",
                ),
            ),
            (
                "No maneja correctamente comas dentro de campos, comillas ni reglas de escapado.",
                "It does not correctly handle commas inside fields, quoting, or escaping rules.",
                "Det håndterer ikke korrekt kommaer i felter, citationstegn eller escaping.",
            ),
            (
                "El módulo csv implementa esas reglas.",
                "The csv module implements those rules.",
                "csv-modulet implementerer reglerne.",
            ),
        ),
        practice(
            "m08.p07",
            ActivityType.CODE_TRACING,
            (
                "Traza try: int('x') except ValueError: result='invalid'.",
                "Trace try: int('x') except ValueError: result='invalid'.",
                "Gennemgå try: int('x') except ValueError: result='invalid'.",
            ),
            (("La conversión falla.", "Conversion fails.", "Konverteringen fejler."),),
            ("result vale 'invalid'.", "result equals 'invalid'.", "result er 'invalid'."),
            (
                "ValueError activa el manejador específico.",
                "ValueError activates the specific handler.",
                "ValueError aktiverer den specifikke handler.",
            ),
        ),
        practice(
            "m08.p08",
            ActivityType.DEBUGGING,
            (
                "Corrige except Exception: pass.",
                "Fix except Exception: pass.",
                "Ret except Exception: pass.",
            ),
            (
                (
                    "Captura sólo lo manejable y conserva contexto.",
                    "Catch only what can be handled and preserve context.",
                    "Fang kun det håndterbare og bevar kontekst.",
                ),
            ),
            (
                "Capturar la excepción específica, registrar o transformar con causa, y dejar propagar lo inesperado.",
                "Catch the specific exception, log or transform it with cause, and let unexpected failures propagate.",
                "Fang den specifikke undtagelse, log eller transformér med årsag, og lad uventede fejl propagere.",
            ),
            (
                "Silenciar Exception oculta defectos.",
                "Silencing Exception hides defects.",
                "At skjule Exception gemmer fejl.",
            ),
        ),
        practice(
            "m08.p09",
            ActivityType.DATA_INTERPRETATION,
            (
                "Interpreta un UnicodeDecodeError al leer UTF-8.",
                "Interpret a UnicodeDecodeError while reading UTF-8.",
                "Fortolk en UnicodeDecodeError ved læsning som UTF-8.",
            ),
            (
                (
                    "Los bytes no son válidos bajo esa codificación.",
                    "The bytes are not valid under that encoding.",
                    "Bytefølgen er ikke gyldig under den kodning.",
                ),
            ),
            (
                "La codificación declarada no coincide con el contenido o el archivo está dañado.",
                "The declared encoding does not match the content or the file is damaged.",
                "Den angivne kodning matcher ikke indholdet, eller filen er beskadiget.",
            ),
            (
                "No debe ignorarse sin una política explícita.",
                "It should not be ignored without an explicit policy.",
                "Den bør ikke ignoreres uden en eksplicit politik.",
            ),
        ),
        practice(
            "m08.p10",
            ActivityType.PIPELINE_DESIGN,
            (
                "Diseña un flujo de importación de filas.",
                "Design a row-import flow.",
                "Design et flow til import af rækker.",
            ),
            (
                (
                    "Incluye contexto de archivo y línea.",
                    "Include file and line context.",
                    "Medtag fil- og linjekontekst.",
                ),
            ),
            (
                "Resolver ruta → abrir → leer cabecera → validar columnas → convertir cada fila con número de línea → acumular errores o detener según política → devolver registros.",
                "Resolve path → open → read header → validate columns → convert each row with line number → accumulate errors or stop by policy → return records.",
                "Løs sti → åbn → læs header → validér kolonner → konvertér hver række med linjenummer → saml fejl eller stop efter politik → returnér poster.",
            ),
            (
                "La política de error debe ser explícita.",
                "Error policy must be explicit.",
                "Fejlpolitikken skal være eksplicit.",
            ),
        ),
        practice(
            "m08.p11",
            ActivityType.ORAL_EXPLANATION,
            (
                "Explica cuándo usar else después de except.",
                "Explain when to use else after except.",
                "Forklar, hvornår else bruges efter except.",
            ),
            (
                (
                    "Separa la operación riesgosa del camino exitoso.",
                    "Separate the risky operation from the success path.",
                    "Adskil den risikable operation fra succesvejen.",
                ),
            ),
            (
                "Cuando el código posterior debe ejecutarse sólo si try terminó sin excepción y no conviene ampliarlo dentro de try.",
                "When following code should run only if try completed without exception and should not broaden the try block.",
                "Når efterfølgende kode kun skal køre, hvis try sluttede uden undtagelse, og try-blokken ikke bør udvides.",
            ),
            (
                "else reduce capturas accidentales.",
                "else reduces accidental catches.",
                "else reducerer utilsigtede fangster.",
            ),
        ),
        practice(
            "m08.p12",
            ActivityType.CODE_COMPLETION,
            (
                "Completa la cadena causal: raise RecordError(message) ____ error.",
                "Complete exception chaining: raise RecordError(message) ____ error.",
                "Udfyld exception chaining: raise RecordError(message) ____ error.",
            ),
            (
                (
                    "Usa la palabra que conserva la causa.",
                    "Use the word that preserves the cause.",
                    "Brug ordet der bevarer årsagen.",
                ),
            ),
            ("from", "from", "from"),
            (
                "from enlaza ambas excepciones.",
                "from links both exceptions.",
                "from forbinder begge undtagelser.",
            ),
        ),
    ),
    assessment_items=(
        authored_item(
            "dm857.m08.assessment.001",
            ActivityType.CODE_TRACING,
            (
                "Traza Path('a') / 'b.txt'.",
                "Trace Path('a') / 'b.txt'.",
                "Gennemgå Path('a') / 'b.txt'.",
            ),
            (
                (
                    "Una ruta compuesta a/b.txt según el sistema.",
                    "A composed a/b.txt path for the system.",
                    "En sammensat a/b.txt-sti for systemet.",
                ),
            ),
            (
                "Path evita separadores manuales.",
                "Path avoids manual separators.",
                "Path undgår manuelle separatorer.",
            ),
        ),
        authored_item(
            "dm857.m08.assessment.002",
            ActivityType.MULTIPLE_SELECT,
            (
                "Selecciona modos que pueden modificar contenido.",
                "Select modes that may modify content.",
                "Vælg tilstande der kan ændre indhold.",
            ),
            (),
            ("w, a y x.", "w, a, and x.", "w, a og x."),
            options=(
                ("w", ("w", "w", "w")),
                ("a", ("a", "a", "a")),
                ("x", ("x", "x", "x")),
                ("r", ("r", "r", "r")),
            ),
            correct_option_ids=("w", "a", "x"),
        ),
        authored_item(
            "dm857.m08.assessment.003",
            ActivityType.DEBUGGING,
            (
                "Corrige un archivo abierto sin cierre garantizado.",
                "Fix a file opened without guaranteed closure.",
                "Ret en fil åbnet uden garanteret lukning.",
            ),
            (
                (
                    "Encapsular la apertura en with.",
                    "Wrap opening in with.",
                    "Indkapsl åbningen i with.",
                ),
            ),
            (
                "with gestiona el recurso incluso ante excepciones.",
                "with manages the resource even on exceptions.",
                "with styrer ressourcen selv ved undtagelser.",
            ),
        ),
        authored_item(
            "dm857.m08.assessment.004",
            ActivityType.FILL_IN_THE_BLANK,
            (
                "Completa la excepción de conversión numérica: ____Error.",
                "Complete the numeric conversion exception: ____Error.",
                "Udfyld undtagelsen for talkonvertering: ____Error.",
            ),
            (("Value", "Value", "Value"),),
            (
                "int y float producen ValueError con texto inválido.",
                "int and float raise ValueError for invalid text.",
                "int og float giver ValueError ved ugyldig tekst.",
            ),
        ),
        authored_item(
            "dm857.m08.assessment.005",
            ActivityType.MATCHING,
            (
                "Relaciona fallo y excepción típica.",
                "Match failure and typical exception.",
                "Match fejl og typisk undtagelse.",
            ),
            (),
            (
                "Ausente-FileNotFoundError; permiso-PermissionError; conversión-ValueError; codificación-UnicodeDecodeError.",
                "Missing-FileNotFoundError; permission-PermissionError; conversion-ValueError; encoding-UnicodeDecodeError.",
                "Manglende-FileNotFoundError; rettighed-PermissionError; konvertering-ValueError; kodning-UnicodeDecodeError.",
            ),
            options=(
                (
                    "missing",
                    (
                        "Ausente → FileNotFoundError",
                        "Missing → FileNotFoundError",
                        "Manglende → FileNotFoundError",
                    ),
                ),
                (
                    "permission",
                    (
                        "Permiso → PermissionError",
                        "Permission → PermissionError",
                        "Rettighed → PermissionError",
                    ),
                ),
                (
                    "conversion",
                    (
                        "Conversión → ValueError",
                        "Conversion → ValueError",
                        "Konvertering → ValueError",
                    ),
                ),
                (
                    "encoding",
                    (
                        "Codificación → UnicodeDecodeError",
                        "Encoding → UnicodeDecodeError",
                        "Kodning → UnicodeDecodeError",
                    ),
                ),
            ),
            correct_option_ids=("missing", "permission", "conversion", "encoding"),
        ),
        authored_item(
            "dm857.m08.assessment.006",
            ActivityType.ORDERING,
            ("Ordena la importación segura.", "Order safe import.", "Ordén sikker import."),
            (),
            (
                "Resolver ruta → abrir → leer → validar → convertir → analizar.",
                "Resolve path → open → read → validate → convert → analyze.",
                "Løs sti → åbn → læs → validér → konvertér → analysér.",
            ),
            options=(
                ("path", ("Resolver ruta", "Resolve path", "Løs sti")),
                ("open", ("Abrir", "Open", "Åbn")),
                ("read", ("Leer", "Read", "Læs")),
                ("validate", ("Validar", "Validate", "Validér")),
                ("convert", ("Convertir", "Convert", "Konvertér")),
                ("analyze", ("Analizar", "Analyze", "Analysér")),
            ),
            correct_option_ids=("path", "open", "read", "validate", "convert", "analyze"),
        ),
        authored_item(
            "dm857.m08.assessment.007",
            ActivityType.CODE_COMPLETION,
            (
                "Escribe parse_int(text, line_number) con contexto causal.",
                "Write parse_int(text, line_number) with causal context.",
                "Skriv parse_int(text, line_number) med årsagskontekst.",
            ),
            (
                (
                    "def parse_int(text, line_number):\n    try:\n        return int(text)\n    except ValueError as error:\n        raise ValueError(f'line {line_number}: {text!r}') from error",
                    "def parse_int(text, line_number):\n    try:\n        return int(text)\n    except ValueError as error:\n        raise ValueError(f'line {line_number}: {text!r}') from error",
                    "def parse_int(text, line_number):\n    try:\n        return int(text)\n    except ValueError as error:\n        raise ValueError(f'line {line_number}: {text!r}') from error",
                ),
            ),
            (
                "La nueva excepción añade contexto y conserva la causa.",
                "The new exception adds context and preserves cause.",
                "Den nye undtagelse tilføjer kontekst og bevarer årsagen.",
            ),
            rubric=(
                ("Captura sólo ValueError.", "Catches only ValueError.", "Fanger kun ValueError."),
            ),
        ),
        authored_item(
            "dm857.m08.assessment.008",
            ActivityType.SHORT_ANSWER,
            (
                "Distingue validación estructural y semántica.",
                "Distinguish structural and semantic validation.",
                "Skeln mellem strukturel og semantisk validering.",
            ),
            (
                (
                    "La estructural comprueba forma y campos; la semántica comprueba significado, rangos y coherencia.",
                    "Structural validation checks shape and fields; semantic validation checks meaning, ranges, and consistency.",
                    "Strukturel validering kontrollerer form og felter; semantisk validering kontrollerer betydning, intervaller og konsistens.",
                ),
            ),
            (
                "Ambas preceden al análisis.",
                "Both precede analysis.",
                "Begge går forud for analyse.",
            ),
        ),
        authored_item(
            "dm857.m08.assessment.009",
            ActivityType.DATA_INTERPRETATION,
            (
                "Interpreta una fila con cuatro columnas cuando se esperan tres.",
                "Interpret a row with four columns when three are expected.",
                "Fortolk en række med fire kolonner, når tre forventes.",
            ),
            (
                (
                    "Es un fallo estructural que debe señalar número de línea y política de rechazo.",
                    "It is a structural failure that should report line number and rejection policy.",
                    "Det er en strukturel fejl, som bør angive linjenummer og afvisningspolitik.",
                ),
            ),
            (
                "No debe convertirse antes de validar la forma.",
                "It should not be converted before shape validation.",
                "Den bør ikke konverteres før validering af formen.",
            ),
        ),
        authored_item(
            "dm857.m08.assessment.010",
            ActivityType.ORAL_EXPLANATION,
            (
                "Explica por qué except Exception: pass es peligroso.",
                "Explain why except Exception: pass is dangerous.",
                "Forklar, hvorfor except Exception: pass er farlig.",
            ),
            (
                (
                    "Oculta errores previstos e inesperados, elimina diagnóstico y puede dejar resultados incompletos como si fueran válidos.",
                    "It hides expected and unexpected failures, removes diagnostics, and may present incomplete results as valid.",
                    "Det skjuler forventede og uventede fejl, fjerner diagnostik og kan præsentere ufuldstændige resultater som gyldige.",
                ),
            ),
            (
                "La captura debe ser específica y observable.",
                "Catching should be specific and observable.",
                "Fangst bør være specifik og observerbar.",
            ),
        ),
        authored_item(
            "dm857.m08.assessment.011",
            ActivityType.PIPELINE_DESIGN,
            (
                "Diseña una canalización didáctica de lectura y validación.",
                "Design a teaching pipeline for reading and validation.",
                "Design en undervisningspipeline til læsning og validering.",
            ),
            (
                (
                    "Ruta → apertura → decodificación → estructura → conversión → semántica → análisis → informe.",
                    "Path → open → decode → structure → conversion → semantics → analysis → report.",
                    "Sti → åbning → dekodning → struktur → konvertering → semantik → analyse → rapport.",
                ),
            ),
            (
                "Cada frontera puede producir un tipo de error distinto.",
                "Each boundary may produce a different error type.",
                "Hver grænse kan give en forskellig fejltype.",
            ),
            rubric=(
                (
                    "Define política de filas inválidas.",
                    "Defines invalid-row policy.",
                    "Definerer politik for ugyldige rækker.",
                ),
            ),
        ),
        authored_item(
            "dm857.m08.assessment.012",
            ActivityType.DEBUGGING,
            (
                "Corrige un try que contiene apertura, análisis y visualización completos.",
                "Fix a try block containing opening, analysis, and visualization.",
                "Ret en try-blok med åbning, analyse og visualisering.",
            ),
            (
                (
                    "Reducir try a la operación que puede producir la excepción capturada y mover el camino exitoso a else.",
                    "Reduce try to the operation that may raise the caught exception and move success logic to else.",
                    "Reducer try til operationen, der kan give den fangede undtagelse, og flyt succeslogik til else.",
                ),
            ),
            (
                "Un try pequeño evita capturar errores no relacionados.",
                "A small try avoids catching unrelated errors.",
                "En lille try undgår at fange uvedkommende fejl.",
            ),
        ),
        authored_item(
            "dm857.m08.assessment.013",
            ActivityType.CODE_TRACING,
            (
                "Traza try sin error, con else y finally.",
                "Trace a successful try with else and finally.",
                "Gennemgå en succesfuld try med else og finally.",
            ),
            (
                (
                    "Se ejecutan try, else y finally; except no.",
                    "try, else, and finally run; except does not.",
                    "try, else og finally kører; except gør ikke.",
                ),
            ),
            ("finally se ejecuta siempre.", "finally always runs.", "finally kører altid."),
        ),
        authored_item(
            "dm857.m08.assessment.014",
            ActivityType.SHORT_ANSWER,
            (
                "Justifica una excepción propia para esquema inválido.",
                "Justify a custom exception for invalid schema.",
                "Begrund en brugerdefineret undtagelse for ugyldigt skema.",
            ),
            (
                (
                    "Permite distinguir un fallo del contrato de datos, capturarlo específicamente y añadir contexto coherente.",
                    "It distinguishes a data-contract failure, supports specific catching, and carries consistent context.",
                    "Den skelner en datakontraktfejl, muliggør specifik fangst og bærer konsistent kontekst.",
                ),
            ),
            (
                "Debe usarse cuando el concepto mejora el contrato, no por cada mensaje.",
                "Use it when the concept improves the contract, not for every message.",
                "Brug den når begrebet forbedrer kontrakten, ikke for hver besked.",
            ),
        ),
    ),
    tutor_support=tutor_support(
        (
            "El trabajo con archivos atraviesa una frontera entre el programa y el sistema operativo. pathlib.Path permite componer rutas de forma portable, pero una ruta no garantiza existencia, tipo ni permisos. Los archivos de texto deben abrirse con modo y codificación explícitos; r lee, w reemplaza, a añade y x exige creación nueva. Un gestor de contexto garantiza cierre incluso ante excepciones. La estrategia de lectura depende del tamaño y el formato: read carga todo, la iteración procesa líneas y el módulo csv maneja delimitadores y comillas. La lógica de cálculo debe permanecer separada de la serialización. Leer texto no valida estructura ni significado: primero se comprueban columnas y campos, después se convierten tipos y se validan rangos o categorías. Las excepciones describen fallos y deben capturarse de forma específica. try contiene la operación riesgosa, except maneja lo previsto, else expresa éxito y finally asegura limpieza. raise from añade contexto preservando causalidad. Las capas internas pueden propagar; la frontera de la aplicación traduce errores a mensajes comprensibles. Las pruebas incluyen rutas ausentes, permisos, codificación, filas incompletas, conversiones inválidas y cierre de recursos. Los ejemplos biomédicos son escenarios didácticos de programación y no representan protocolos, procesos clínicos ni recomendaciones de laboratorio.",
            "File handling crosses a boundary between the program and the operating system. pathlib.Path composes paths portably, but a path does not guarantee existence, type, or permissions. Text files should use explicit mode and encoding; r reads, w replaces, a appends, and x requires new creation. A context manager guarantees closure even on exceptions. Reading strategy depends on size and format: read loads everything, iteration processes lines, and csv handles delimiters and quoting. Computation should remain separate from serialization. Reading text validates neither structure nor meaning: first check columns and fields, then convert types and validate ranges or categories. Exceptions describe failures and should be caught specifically. try contains the risky operation, except handles expected failures, else expresses success, and finally ensures cleanup. raise from adds context while preserving causality. Internal layers may propagate; the application boundary translates errors into understandable messages. Tests include missing paths, permissions, encoding, incomplete rows, invalid conversions, and resource closure. Biomedical examples are programming exercises, not protocols, clinical processes, or laboratory recommendations.",
            "Filhåndtering krydser en grænse mellem programmet og operativsystemet. pathlib.Path sammensætter stier portabelt, men en sti garanterer ikke eksistens, type eller rettigheder. Tekstfiler bør bruge eksplicit tilstand og kodning; r læser, w erstatter, a tilføjer, og x kræver ny oprettelse. En context manager garanterer lukning selv ved undtagelser. Læsestrategien afhænger af størrelse og format: read indlæser alt, iteration behandler linjer, og csv håndterer separatorer og citationstegn. Beregning bør adskilles fra serialisering. Læsning validerer hverken struktur eller betydning: kontrollér først kolonner og felter, konvertér derefter typer og validér intervaller. Undtagelser bør fanges specifikt. try indeholder den risikable operation, except håndterer forventede fejl, else udtrykker succes, og finally sikrer oprydning. raise from bevarer årsag. Biomedicinske eksempler er programmeringsøvelser, ikke protokoller, kliniske processer eller laboratorieanbefalinger.",
        ),
        tuple(
            (es, en, da)
            for es, en, da in (
                (
                    "Path compone rutas portables.",
                    "Path composes portable paths.",
                    "Path sammensætter portable stier.",
                ),
                (
                    "Las rutas relativas dependen del directorio de trabajo.",
                    "Relative paths depend on the working directory.",
                    "Relative stier afhænger af arbejdsmappen.",
                ),
                ("with garantiza cierre.", "with guarantees closure.", "with garanterer lukning."),
                (
                    "w reemplaza contenido existente.",
                    "w replaces existing content.",
                    "w erstatter eksisterende indhold.",
                ),
                (
                    "La codificación debe ser explícita.",
                    "Encoding should be explicit.",
                    "Kodning bør være eksplicit.",
                ),
                (
                    "La iteración procesa archivos incrementalmente.",
                    "Iteration processes files incrementally.",
                    "Iteration behandler filer inkrementelt.",
                ),
                (
                    "csv maneja comillas y separadores.",
                    "csv handles quoting and delimiters.",
                    "csv håndterer citationstegn og separatorer.",
                ),
                (
                    "write no añade saltos automáticamente.",
                    "write adds no newline automatically.",
                    "write tilføjer ikke automatisk linjeskift.",
                ),
                (
                    "Validación estructural precede a conversión.",
                    "Structural validation precedes conversion.",
                    "Strukturel validering går forud for konvertering.",
                ),
                (
                    "ValueError expresa conversión inválida.",
                    "ValueError expresses invalid conversion.",
                    "ValueError udtrykker ugyldig konvertering.",
                ),
                (
                    "Las capturas deben ser específicas.",
                    "Catches should be specific.",
                    "Fangster bør være specifikke.",
                ),
                (
                    "else expresa el camino exitoso.",
                    "else expresses the success path.",
                    "else udtrykker succesvejen.",
                ),
                ("finally se ejecuta siempre.", "finally always runs.", "finally kører altid."),
                (
                    "raise from preserva causalidad.",
                    "raise from preserves causality.",
                    "raise from bevarer årsag.",
                ),
            )
        ),
        tuple(
            (es, en, da)
            for es, en, da in (
                (
                    "Concatenar rutas con separadores manuales.",
                    "Concatenating paths with manual separators.",
                    "At sammenkæde stier med manuelle separatorer.",
                ),
                (
                    "Abrir para leer con modo w.",
                    "Opening for reading with mode w.",
                    "At åbne til læsning med tilstand w.",
                ),
                ("Omitir encoding.", "Omitting encoding.", "At udelade encoding."),
                ("Olvidar el cierre.", "Forgetting closure.", "At glemme lukning."),
                (
                    "Usar read para cualquier tamaño.",
                    "Using read for every size.",
                    "At bruge read til enhver størrelse.",
                ),
                (
                    "Analizar CSV con split ingenuo.",
                    "Parsing CSV with naive split.",
                    "At analysere CSV med naiv split.",
                ),
                (
                    "Convertir antes de validar columnas.",
                    "Converting before validating columns.",
                    "At konvertere før validering af kolonner.",
                ),
                (
                    "Perder número de línea en errores.",
                    "Losing line number in errors.",
                    "At miste linjenummer i fejl.",
                ),
                (
                    "Capturar Exception de forma amplia.",
                    "Catching Exception broadly.",
                    "At fange Exception bredt.",
                ),
                (
                    "Silenciar errores con pass.",
                    "Silencing errors with pass.",
                    "At skjule fejl med pass.",
                ),
                (
                    "Poner demasiado código en try.",
                    "Putting too much code in try.",
                    "At placere for meget kode i try.",
                ),
                (
                    "Transformar una excepción sin conservar causa.",
                    "Transforming an exception without preserving cause.",
                    "At transformere en undtagelse uden at bevare årsagen.",
                ),
            )
        ),
        tuple(
            (es, en, da)
            for es, en, da in (
                (
                    "¿La ruta es relativa o absoluta?",
                    "Is the path relative or absolute?",
                    "Er stien relativ eller absolut?",
                ),
                (
                    "¿Qué modo corresponde a la intención?",
                    "Which mode matches the intent?",
                    "Hvilken tilstand matcher hensigten?",
                ),
                (
                    "¿Qué codificación se espera?",
                    "Which encoding is expected?",
                    "Hvilken kodning forventes?",
                ),
                (
                    "¿El archivo cabe razonablemente en memoria?",
                    "Does the file reasonably fit in memory?",
                    "Kan filen rimeligt være i hukommelsen?",
                ),
                (
                    "¿El formato admite comillas o separadores internos?",
                    "Does the format allow quoting or internal delimiters?",
                    "Tillader formatet citationstegn eller interne separatorer?",
                ),
                (
                    "¿Qué se valida antes de convertir?",
                    "What is validated before conversion?",
                    "Hvad valideres før konvertering?",
                ),
                (
                    "¿Qué contexto necesita el error?",
                    "What context does the error need?",
                    "Hvilken kontekst behøver fejlen?",
                ),
                (
                    "¿Qué excepción concreta puede ocurrir?",
                    "Which concrete exception may occur?",
                    "Hvilken konkret undtagelse kan forekomme?",
                ),
                (
                    "¿Puede esta capa manejar el fallo?",
                    "Can this layer handle the failure?",
                    "Kan dette lag håndtere fejlen?",
                ),
                (
                    "¿El try contiene sólo la operación riesgosa?",
                    "Does try contain only the risky operation?",
                    "Indeholder try kun den risikable operation?",
                ),
                (
                    "¿Debe preservarse la causa?",
                    "Should the cause be preserved?",
                    "Skal årsagen bevares?",
                ),
                (
                    "¿Qué casos de fallo cubren las pruebas?",
                    "Which failure cases do tests cover?",
                    "Hvilke fejltilfælde dækker testene?",
                ),
            )
        ),
        tuple(
            (es, en, da)
            for es, en, da in (
                ("Construye rutas portables.", "Builds portable paths.", "Bygger portable stier."),
                (
                    "Elige modos sin pérdida accidental.",
                    "Chooses modes without accidental data loss.",
                    "Vælger tilstande uden utilsigtet datatab.",
                ),
                (
                    "Gestiona recursos con with.",
                    "Manages resources with with.",
                    "Styrer ressourcer med with.",
                ),
                (
                    "Selecciona estrategia de lectura.",
                    "Selects a reading strategy.",
                    "Vælger en læsestrategi.",
                ),
                (
                    "Usa csv para datos delimitados.",
                    "Uses csv for delimited data.",
                    "Bruger csv til afgrænsede data.",
                ),
                (
                    "Separa cálculo y representación.",
                    "Separates computation and representation.",
                    "Adskiller beregning og repræsentation.",
                ),
                (
                    "Valida estructura y semántica.",
                    "Validates structure and semantics.",
                    "Validerer struktur og semantik.",
                ),
                (
                    "Captura excepciones específicas.",
                    "Catches specific exceptions.",
                    "Fanger specifikke undtagelser.",
                ),
                (
                    "Preserva contexto y causa.",
                    "Preserves context and cause.",
                    "Bevarer kontekst og årsag.",
                ),
                ("Prueba caminos de fallo.", "Tests failure paths.", "Tester fejlveje."),
            )
        ),
        tuple(
            (es, en, da)
            for es, en, da in (
                ("Dar primero una pista.", "Give a hint first.", "Giv først et hint."),
                (
                    "Advertir que w puede destruir contenido.",
                    "Warn that w may destroy content.",
                    "Advar om at w kan ødelægge indhold.",
                ),
                (
                    "Declarar siempre la codificación en ejemplos de texto.",
                    "Always declare encoding in text examples.",
                    "Angiv altid kodning i teksteksempler.",
                ),
                (
                    "Preferir with para recursos.",
                    "Prefer with for resources.",
                    "Foretræk with til ressourcer.",
                ),
                (
                    "No recomendar split para CSV general.",
                    "Do not recommend split for general CSV.",
                    "Anbefal ikke split til generel CSV.",
                ),
                (
                    "Conservar archivo y línea en errores.",
                    "Preserve file and line in errors.",
                    "Bevar fil og linje i fejl.",
                ),
                ("No silenciar Exception.", "Do not silence Exception.", "Skjul ikke Exception."),
                (
                    "No presentar ejemplos didácticos como protocolos.",
                    "Do not present teaching examples as protocols.",
                    "Præsenter ikke undervisningseksempler som protokoller.",
                ),
                (
                    "Relacionar cada captura con una recuperación real.",
                    "Relate each catch to actual recovery.",
                    "Knyt hver fangst til reel genopretning.",
                ),
            )
        ),
        (
            "Official DM857 course description, SDU, active version approved in 2025.",
            "Think Python, third edition, chapters on files and exceptions.",
            "Introduction to Computation and Programming Using Python, third edition, sections on files, exceptions, and testing.",
        ),
    ),
)

_BANK_08_MCQ = (
    (
        "001",
        (
            "¿Qué objeto compone rutas portables?",
            "Which object composes portable paths?",
            "Hvilket objekt sammensætter portable stier?",
        ),
        (
            ("path", ("pathlib.Path", "pathlib.Path", "pathlib.Path")),
            ("string", ("Concatenación de str", "String concatenation", "Strengsammenkædning")),
            ("list", ("list", "list", "list")),
            ("set", ("set", "set", "set")),
        ),
        "path",
        (
            "Path conoce reglas del sistema.",
            "Path knows system path rules.",
            "Path kender systemets stiregler.",
        ),
    ),
    (
        "003",
        ("¿Qué modo sólo lee?", "Which mode only reads?", "Hvilken tilstand læser kun?"),
        (
            ("r", ("r", "r", "r")),
            ("w", ("w", "w", "w")),
            ("a", ("a", "a", "a")),
            ("x", ("x", "x", "x")),
        ),
        "r",
        ("r abre para lectura.", "r opens for reading.", "r åbner til læsning."),
    ),
    (
        "005",
        (
            "¿Qué construcción garantiza cierre?",
            "Which construct guarantees closure?",
            "Hvilken konstruktion garanterer lukning?",
        ),
        (
            ("with", ("with", "with", "with")),
            ("if", ("if", "if", "if")),
            ("for", ("for", "for", "for")),
            ("match", ("match", "match", "match")),
        ),
        "with",
        (
            "with invoca el protocolo de contexto.",
            "with invokes the context protocol.",
            "with anvender kontekstprotokollen.",
        ),
    ),
    (
        "007",
        (
            "¿Qué estrategia evita cargar todo el archivo?",
            "Which strategy avoids loading the whole file?",
            "Hvilken strategi undgår at indlæse hele filen?",
        ),
        (
            ("iterate", ("Iterar por líneas", "Iterate by lines", "Iterér over linjer")),
            ("read", ("read()", "read()", "read()")),
            ("copy", ("Copiar dos veces", "Copy twice", "Kopiér to gange")),
            ("set", ("Convertir a set", "Convert to set", "Konvertér til set")),
        ),
        "iterate",
        ("La iteración es incremental.", "Iteration is incremental.", "Iteration er inkrementel."),
    ),
    (
        "009",
        (
            "¿Qué módulo maneja comillas CSV?",
            "Which module handles CSV quoting?",
            "Hvilket modul håndterer CSV-citationstegn?",
        ),
        (
            ("csv", ("csv", "csv", "csv")),
            ("math", ("math", "math", "math")),
            ("random", ("random", "random", "random")),
            ("pathlib", ("pathlib", "pathlib", "pathlib")),
        ),
        "csv",
        (
            "csv implementa las reglas del formato.",
            "csv implements format rules.",
            "csv implementerer formatreglerne.",
        ),
    ),
    (
        "011",
        (
            "¿Qué debe validarse primero?",
            "What should be validated first?",
            "Hvad bør valideres først?",
        ),
        (
            ("structure", ("Estructura y campos", "Structure and fields", "Struktur og felter")),
            ("plot", ("Visualización", "Visualization", "Visualisering")),
            ("mean", ("Media", "Mean", "Gennemsnit")),
            ("export", ("Exportación", "Export", "Eksport")),
        ),
        "structure",
        (
            "La forma precede a conversión y análisis.",
            "Shape precedes conversion and analysis.",
            "Form går forud for konvertering og analyse.",
        ),
    ),
    (
        "013",
        (
            "¿Qué excepción produce int('x')?",
            "Which exception does int('x') raise?",
            "Hvilken undtagelse giver int('x')?",
        ),
        (
            ("value", ("ValueError", "ValueError", "ValueError")),
            ("file", ("FileNotFoundError", "FileNotFoundError", "FileNotFoundError")),
            ("permission", ("PermissionError", "PermissionError", "PermissionError")),
            ("type", ("KeyError", "KeyError", "KeyError")),
        ),
        "value",
        (
            "El texto no representa un entero.",
            "The text does not represent an integer.",
            "Teksten repræsenterer ikke et heltal.",
        ),
    ),
    (
        "015",
        (
            "¿Qué bloque se ejecuta sólo sin excepción?",
            "Which block runs only without an exception?",
            "Hvilken blok kører kun uden en undtagelse?",
        ),
        (
            ("else", ("else", "else", "else")),
            ("finally", ("finally", "finally", "finally")),
            ("except", ("except", "except", "except")),
            ("raise", ("raise", "raise", "raise")),
        ),
        "else",
        (
            "else representa el camino exitoso.",
            "else represents the success path.",
            "else repræsenterer succesvejen.",
        ),
    ),
    (
        "017",
        (
            "¿Qué bloque se ejecuta siempre?",
            "Which block always runs?",
            "Hvilken blok kører altid?",
        ),
        (
            ("finally", ("finally", "finally", "finally")),
            ("else", ("else", "else", "else")),
            ("except", ("except", "except", "except")),
            ("case", ("case", "case", "case")),
        ),
        "finally",
        (
            "finally ejecuta limpieza final.",
            "finally performs final cleanup.",
            "finally udfører afsluttende oprydning.",
        ),
    ),
    (
        "019",
        (
            "¿Qué sintaxis conserva la causa?",
            "Which syntax preserves the cause?",
            "Hvilken syntaks bevarer årsagen?",
        ),
        (
            (
                "from",
                (
                    "raise NewError() from error",
                    "raise NewError() from error",
                    "raise NewError() from error",
                ),
            ),
            ("pass", ("except: pass", "except: pass", "except: pass")),
            ("return", ("return error", "return error", "return error")),
            ("print", ("print(error)", "print(error)", "print(error)")),
        ),
        "from",
        (
            "from establece exception chaining.",
            "from establishes exception chaining.",
            "from etablerer exception chaining.",
        ),
    ),
    (
        "021",
        (
            "¿Qué excepción indica archivo ausente?",
            "Which exception indicates a missing file?",
            "Hvilken undtagelse angiver en manglende fil?",
        ),
        (
            ("missing", ("FileNotFoundError", "FileNotFoundError", "FileNotFoundError")),
            ("value", ("ValueError", "ValueError", "ValueError")),
            ("unicode", ("UnicodeDecodeError", "UnicodeDecodeError", "UnicodeDecodeError")),
            ("key", ("KeyError", "KeyError", "KeyError")),
        ),
        "missing",
        (
            "Es una subclase específica de OSError.",
            "It is a specific OSError subtype.",
            "Det er en specifik subtype af OSError.",
        ),
    ),
    (
        "023",
        (
            "¿Qué conserva un buen error de fila?",
            "What does a good row error preserve?",
            "Hvad bevarer en god rækkefejl?",
        ),
        (
            ("context", ("Archivo, línea y valor", "File, line, and value", "Fil, linje og værdi")),
            ("none", ("Nada", "Nothing", "Intet")),
            ("only_type", ("Sólo el tipo", "Only the type", "Kun typen")),
            ("random", ("Un número aleatorio", "A random number", "Et tilfældigt tal")),
        ),
        "context",
        (
            "El contexto permite localizar y corregir.",
            "Context supports locating and correcting.",
            "Kontekst gør lokalisering og rettelse mulig.",
        ),
    ),
    (
        "025",
        (
            "¿Dónde traducir un error técnico para el usuario?",
            "Where should a technical error be translated for the user?",
            "Hvor bør en teknisk fejl oversættes for brugeren?",
        ),
        (
            (
                "boundary",
                (
                    "En la frontera de la aplicación",
                    "At the application boundary",
                    "Ved applikationsgrænsen",
                ),
            ),
            ("every", ("En cada función", "In every function", "I hver funktion")),
            ("never", ("Nunca", "Never", "Aldrig")),
            ("import", ("Durante import", "During import", "Under import")),
        ),
        "boundary",
        (
            "Las capas internas pueden propagar con contexto.",
            "Inner layers may propagate with context.",
            "Indre lag kan propagere med kontekst.",
        ),
    ),
    (
        "027",
        (
            "¿Qué prueba cubre decodificación?",
            "Which test covers decoding?",
            "Hvilken test dækker dekodning?",
        ),
        (
            (
                "invalid_bytes",
                (
                    "Bytes inválidos para la codificación",
                    "Bytes invalid for the encoding",
                    "Bytes ugyldige for kodningen",
                ),
            ),
            ("empty_list", ("Lista vacía", "Empty list", "Tom liste")),
            ("sort", ("Ordenación", "Sorting", "Sortering")),
            ("dict", ("Clave ausente", "Missing key", "Manglende nøgle")),
        ),
        "invalid_bytes",
        (
            "Debe verificarse UnicodeDecodeError o la política elegida.",
            "It should verify UnicodeDecodeError or the chosen policy.",
            "Den bør verificere UnicodeDecodeError eller den valgte politik.",
        ),
    ),
    (
        "029",
        (
            "¿Qué separa cálculo y salida?",
            "What separates computation and output?",
            "Hvad adskiller beregning og output?",
        ),
        (
            (
                "layers",
                (
                    "Funciones de cálculo y serialización distintas",
                    "Separate computation and serialization functions",
                    "Separate funktioner til beregning og serialisering",
                ),
            ),
            (
                "print",
                (
                    "Imprimir dentro de todo cálculo",
                    "Print inside every computation",
                    "Udskriv i hver beregning",
                ),
            ),
            ("global", ("Variable global", "Global variable", "Global variabel")),
            ("catch", ("except Exception", "except Exception", "except Exception")),
        ),
        "layers",
        (
            "La separación mejora pruebas y reutilización.",
            "Separation improves testing and reuse.",
            "Adskillelse forbedrer test og genbrug.",
        ),
    ),
)
_BANK_08_TF = (
    (
        "002",
        (
            "Una ruta garantiza que el archivo exista.",
            "A path guarantees that a file exists.",
            "En sti garanterer, at en fil eksisterer.",
        ),
        False,
        (
            "La existencia debe comprobarse o manejarse al abrir.",
            "Existence must be checked or handled when opening.",
            "Eksistens skal kontrolleres eller håndteres ved åbning.",
        ),
    ),
    (
        "004",
        (
            "El modo w puede truncar un archivo existente.",
            "Mode w may truncate an existing file.",
            "Tilstand w kan afkorte en eksisterende fil.",
        ),
        True,
        ("w reemplaza el contenido.", "w replaces content.", "w erstatter indhold."),
    ),
    (
        "006",
        (
            "with cierra el archivo aunque ocurra una excepción.",
            "with closes the file even when an exception occurs.",
            "with lukker filen selv ved en undtagelse.",
        ),
        True,
        (
            "El gestor de contexto garantiza la salida.",
            "The context manager guarantees exit handling.",
            "Context manageren garanterer exit-håndtering.",
        ),
    ),
    (
        "008",
        (
            "read() siempre es la mejor estrategia para archivos grandes.",
            "read() is always the best strategy for large files.",
            "read() er altid den bedste strategi til store filer.",
        ),
        False,
        (
            "La iteración puede reducir memoria.",
            "Iteration may reduce memory use.",
            "Iteration kan reducere hukommelsesforbrug.",
        ),
    ),
    (
        "010",
        (
            "split(',') maneja correctamente cualquier CSV.",
            "split(',') correctly handles any CSV.",
            "split(',') håndterer enhver CSV korrekt.",
        ),
        False,
        (
            "No gestiona comillas ni comas internas.",
            "It does not handle quoting or internal commas.",
            "Det håndterer ikke citationstegn eller interne kommaer.",
        ),
    ),
    (
        "012",
        (
            "La conversión numérica sustituye la validación semántica.",
            "Numeric conversion replaces semantic validation.",
            "Talkonvertering erstatter semantisk validering.",
        ),
        False,
        (
            "Un número convertible puede seguir fuera del rango permitido.",
            "A convertible number may still be outside the allowed range.",
            "Et konvertibelt tal kan stadig ligge uden for det tilladte interval.",
        ),
    ),
    (
        "014",
        (
            "Capturar Exception de forma amplia puede ocultar defectos.",
            "Catching Exception broadly may hide defects.",
            "Bred fangst af Exception kan skjule fejl.",
        ),
        True,
        (
            "Debe capturarse sólo lo manejable.",
            "Catch only what can be handled.",
            "Fang kun det, der kan håndteres.",
        ),
    ),
    (
        "016",
        (
            "else se ejecuta cuando except manejó una excepción.",
            "else runs when except handled an exception.",
            "else kører, når except håndterede en undtagelse.",
        ),
        False,
        (
            "else se ejecuta sólo si try no produjo excepción.",
            "else runs only if try raised no exception.",
            "else kører kun, hvis try ikke gav en undtagelse.",
        ),
    ),
    (
        "018",
        (
            "finally puede usarse para limpieza.",
            "finally can be used for cleanup.",
            "finally kan bruges til oprydning.",
        ),
        True,
        (
            "Se ejecuta en caminos de éxito y error.",
            "It runs on success and failure paths.",
            "Den kører på succes- og fejlveje.",
        ),
    ),
    (
        "020",
        (
            "raise from elimina la excepción original.",
            "raise from removes the original exception.",
            "raise from fjerner den oprindelige undtagelse.",
        ),
        False,
        ("La conserva como causa.", "It preserves it as the cause.", "Den bevarer den som årsag."),
    ),
    (
        "022",
        (
            "Todas las capas deben capturar todas las excepciones.",
            "Every layer should catch every exception.",
            "Alle lag bør fange alle undtagelser.",
        ),
        False,
        (
            "Las capas pueden propagar lo que no pueden manejar.",
            "Layers may propagate what they cannot handle.",
            "Lag kan propagere det, de ikke kan håndtere.",
        ),
    ),
    (
        "024",
        (
            "Una excepción propia puede expresar un fallo del contrato de datos.",
            "A custom exception can express a data-contract failure.",
            "En brugerdefineret undtagelse kan udtrykke en datakontraktfejl.",
        ),
        True,
        (
            "Permite captura y mensajes específicos.",
            "It supports specific catching and messages.",
            "Den muliggør specifik fangst og beskeder.",
        ),
    ),
    (
        "026",
        (
            "Los errores de fila deben conservar el número de línea.",
            "Row errors should preserve line number.",
            "Rækkefejl bør bevare linjenummer.",
        ),
        True,
        (
            "El contexto facilita diagnóstico.",
            "Context supports diagnosis.",
            "Kontekst understøtter diagnose.",
        ),
    ),
    (
        "028",
        (
            "Las pruebas sólo necesitan cubrir el camino exitoso.",
            "Tests only need to cover the success path.",
            "Test behøver kun at dække succesvejen.",
        ),
        False,
        (
            "Los fallos previstos forman parte del contrato.",
            "Expected failures belong to the contract.",
            "Forventede fejl er en del af kontrakten.",
        ),
    ),
    (
        "030",
        (
            "Los ejemplos del módulo son protocolos de laboratorio.",
            "The module examples are laboratory protocols.",
            "Modulets eksempler er laboratorieprotokoller.",
        ),
        False,
        (
            "Son ejercicios didácticos de programación.",
            "They are teaching programming exercises.",
            "De er didaktiske programmeringsøvelser.",
        ),
    ),
)

LOCALIZED_OBJECTIVE_QUESTION_BANK_08 = tuple(
    sorted(
        (
            *(objective_mcq(f"dm857.m08.bank.{n}", p, o, c, e) for n, p, o, c, e in _BANK_08_MCQ),
            *(
                objective_tf(f"dm857.m08.bank.{n}", p, correct=c, explanation=e)
                for n, p, c, e in _BANK_08_TF
            ),
        ),
        key=lambda item: item.item_id,
    )
)


def materialize_module_08_question_bank(locale: AppLocale | str) -> tuple[AssessmentItem, ...]:
    resolved = locale if isinstance(locale, AppLocale) else AppLocale.resolve(locale)
    return tuple(item.materialize(resolved) for item in LOCALIZED_OBJECTIVE_QUESTION_BANK_08)


MODULE_08_FILES_EXCEPTIONS: LearningModule = LOCALIZED_MODULE_08_FILES_EXCEPTIONS.materialize(
    AppLocale.SPANISH_SPAIN
)
OBJECTIVE_QUESTION_BANK_08 = materialize_module_08_question_bank(AppLocale.SPANISH_SPAIN)

__all__ = [
    "LOCALIZED_MODULE_08_FILES_EXCEPTIONS",
    "LOCALIZED_OBJECTIVE_QUESTION_BANK_08",
    "MODULE_08_FILES_EXCEPTIONS",
    "OBJECTIVE_QUESTION_BANK_08",
    "materialize_module_08_question_bank",
]
