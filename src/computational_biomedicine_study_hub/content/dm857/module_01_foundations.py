"""DM857 module 1: computational problem solving and Python foundations."""

from __future__ import annotations

from ...learning.activity_types import ActivityType
from ..models import (
    AssessmentItem,
    ConceptBlock,
    LearningModule,
    LearningObjective,
    PracticeExercise,
    TutorSupportPacket,
    WorkedExample,
)


MODULE = LearningModule(
    course_code="DM857",
    module_id="dm857.m01",
    title="Resolución de problemas, valores, tipos y estado del programa",
    summary=(
        "Introducción al razonamiento computacional y a los elementos mínimos de un "
        "programa Python: problema, modelo, algoritmo, expresiones, valores, tipos, "
        "variables, asignación, conversión de tipos, entrada y salida, trazado y errores."
    ),
    objectives=(
        LearningObjective(
            "m01.o1",
            "Separar una situación concreta en entradas, transformaciones, restricciones "
            "y salidas observables.",
        ),
        LearningObjective(
            "m01.o2",
            "Distinguir con precisión expresión, valor, tipo, variable, asignación y "
            "sentencia.",
        ),
        LearningObjective(
            "m01.o3",
            "Predecir el valor y el tipo de expresiones aritméticas y de texto antes de "
            "ejecutarlas.",
        ),
        LearningObjective(
            "m01.o4",
            "Representar el estado de un programa mediante una tabla de trazado de "
            "variables.",
        ),
        LearningObjective(
            "m01.o5",
            "Aplicar conversiones explícitas entre int, float y str cuando el problema lo "
            "requiera.",
        ),
        LearningObjective(
            "m01.o6",
            "Diferenciar errores de sintaxis, errores de ejecución y errores lógicos, y "
            "proponer una prueba mínima para detectarlos.",
        ),
    ),
    concepts=(
        ConceptBlock(
            concept_id="problem-model-algorithm-program",
            title="Del problema al programa",
            body=(
                "Programar no comienza escribiendo sintaxis. Comienza construyendo una "
                "representación operativa de un problema. Una situación del mundo real "
                "contiene detalles relevantes y detalles accidentales; el modelo conserva "
                "solo aquello necesario para producir una respuesta verificable. A partir "
                "del modelo se diseña un algoritmo, es decir, una secuencia finita y no "
                "ambigua de pasos. El programa es una implementación concreta de ese "
                "algoritmo en un lenguaje. Separar estas capas permite preguntar, en orden: "
                "¿el modelo representa bien el problema?, ¿el algoritmo resuelve el modelo?, "
                "¿el código implementa correctamente el algoritmo? Un resultado incorrecto "
                "puede originarse en cualquiera de las tres capas."
            ),
            key_points=(
                "Problema, modelo, algoritmo y programa no son sinónimos.",
                "Las entradas y salidas deben definirse antes de codificar.",
                "Una restricción indica qué valores son válidos o qué comportamiento se espera.",
                "La corrección se evalúa respecto al problema especificado, no respecto a la "
                "intención informal del autor.",
            ),
        ),
        ConceptBlock(
            concept_id="expressions-values-types",
            title="Expresiones, valores y tipos",
            body=(
                "Una expresión es una combinación de literales, variables, operadores y "
                "llamadas que Python puede evaluar para obtener un valor. El valor es el "
                "resultado concreto de esa evaluación. Todo valor pertenece a un tipo, y el "
                "tipo determina qué operaciones son válidas y cómo se interpretan. Por "
                "ejemplo, 3 + 4 produce el entero 7, mientras que '3' + '4' produce la cadena "
                "'34'. La notación visual puede parecer similar, pero el tipo cambia la "
                "semántica. Python utiliza tipado dinámico: las variables no quedan ligadas de "
                "forma permanente a un tipo, aunque cada valor sí posee un tipo en todo momento."
            ),
            key_points=(
                "Una expresión se evalúa; una sentencia produce una acción o cambio de estado.",
                "int representa enteros, float números en coma flotante y str texto.",
                "El operador / produce float, incluso cuando la división es exacta.",
                "La función type permite inspeccionar el tipo de un valor durante el aprendizaje "
                "y la depuración.",
            ),
        ),
        ConceptBlock(
            concept_id="variables-assignment-state",
            title="Variables, asignación y estado",
            body=(
                "Una variable es un nombre asociado a un valor. La sentencia de asignación "
                "evalúa primero la expresión situada a la derecha y después vincula el nombre "
                "de la izquierda con el resultado. Por eso x = x + 1 es válida en programación: "
                "no expresa una igualdad matemática, sino una actualización de estado. El estado "
                "de un programa es el conjunto de asociaciones nombre-valor existentes en un "
                "instante. Cuando una variable se reasigna, el valor anterior deja de ser el "
                "valor actual de ese nombre. Una tabla de trazado registra cada sentencia y el "
                "estado resultante; es una herramienta esencial para explicar y depurar código."
            ),
            key_points=(
                "La asignación usa = y no afirma igualdad matemática.",
                "La expresión derecha se evalúa antes de modificar la variable izquierda.",
                "Los nombres deben describir el significado de los datos, no solo su tipo.",
                "El trazado manual reduce errores al razonar sobre varias reasignaciones.",
            ),
        ),
        ConceptBlock(
            concept_id="operators-precedence-conversion",
            title="Operadores, precedencia y conversión",
            body=(
                "Los operadores aritméticos básicos son +, -, *, /, //, % y **. Python aplica "
                "reglas de precedencia: primero paréntesis, luego exponenciación, después "
                "multiplicación, división, división entera y módulo, y finalmente suma y resta. "
                "Aunque una expresión sea válida, puede ser difícil de leer; los paréntesis "
                "deben utilizarse cuando aclaran la intención. Las conversiones int(), float() y "
                "str() crean valores de otro tipo cuando la conversión es posible. Convertir no "
                "es decorar el dato: cambia las operaciones disponibles y puede perder "
                "información, como ocurre con int(4.9), que produce 4 sin redondear al entero más "
                "cercano."
            ),
            key_points=(
                "// realiza división entera hacia abajo; % devuelve el resto.",
                "** representa exponenciación; ^ no es exponenciación en Python.",
                "La precedencia puede cambiarse con paréntesis.",
                "Una conversión explícita debe justificarse por el significado esperado del dato.",
            ),
        ),
        ConceptBlock(
            concept_id="statements-input-output-tracing",
            title="Sentencias, entrada, salida y trazado",
            body=(
                "Una sentencia es una instrucción ejecutable. La asignación y una llamada a "
                "print son ejemplos de sentencias. input devuelve siempre una cadena, incluso "
                "cuando el usuario escribe dígitos; si se requiere una cantidad numérica, la "
                "conversión debe ser explícita. print permite observar resultados, pero imprimir "
                "no es lo mismo que devolver un valor desde una función, concepto que se "
                "desarrollará más adelante. En esta etapa, el trazado consiste en ejecutar "
                "mentalmente cada sentencia, registrar las variables modificadas y anotar la "
                "salida producida. Este procedimiento obliga a distinguir el código escrito del "
                "estado que ese código genera."
            ),
            key_points=(
                "input siempre devuelve str.",
                "La salida visible es un efecto del programa y debe corresponder a la especificación.",
                "Un trazado correcto sigue el orden real de ejecución.",
                "El valor mostrado por print puede diferir de la representación interna del dato.",
            ),
        ),
        ConceptBlock(
            concept_id="errors-tests-and-evidence",
            title="Errores, pruebas y evidencia de corrección",
            body=(
                "Un error de sintaxis impide que Python interprete la estructura del código. Un "
                "error de ejecución aparece durante la ejecución de una sentencia válida, por "
                "ejemplo al dividir por cero o combinar tipos incompatibles. Un error lógico "
                "produce una ejecución aparentemente normal pero un resultado incorrecto. La "
                "ausencia de excepciones no demuestra corrección. Una prueba compara el resultado "
                "observado con un resultado esperado para una entrada concreta. Los casos de prueba "
                "deben incluir ejemplos normales, límites relevantes y casos capaces de revelar "
                "confusiones de tipo o de unidades. La depuración efectiva formula hipótesis y usa "
                "evidencia; no consiste en cambiar líneas al azar."
            ),
            key_points=(
                "Sintaxis, ejecución y lógica describen fallos diferentes.",
                "Un mensaje de error debe leerse desde la última línea y relacionarse con la operación.",
                "Una prueba necesita entrada, resultado esperado y criterio de comparación.",
                "Un caso que pasa no garantiza corrección general; varios casos bien elegidos aumentan "
                "la evidencia.",
            ),
        ),
    ),
    worked_examples=(
        WorkedExample(
            example_id="sequencing-yield",
            title="Calcular el rendimiento útil de una corrida de secuenciación",
            problem=(
                "Una corrida produce 48_000_000 lecturas. El 92.5 % supera el control de calidad. "
                "Calcular cuántas lecturas útiles se esperan y mostrar el resultado como entero."
            ),
            reasoning=(
                "Representar el total como int y el porcentaje como float.",
                "Convertir 92.5 % a la fracción 0.925.",
                "Multiplicar total por fracción para obtener un float.",
                "Convertir a int únicamente porque el conteo de lecturas debe ser entero.",
            ),
            code=(
                "total_reads = 48_000_000\n"
                "passing_fraction = 92.5 / 100\n"
                "usable_reads = int(total_reads * passing_fraction)\n"
                "print(usable_reads)"
            ),
            expected_output="44400000",
            explanation=(
                "Los guiones bajos mejoran la lectura del literal sin cambiar su valor. La "
                "división produce 0.925 como float. El producto también es float y se convierte "
                "al final porque un conteo no admite fracciones. En este caso el producto es exacto; "
                "en otros casos convendría decidir explícitamente si truncar o redondear."
            ),
        ),
        WorkedExample(
            example_id="sample-volume",
            title="Convertir volumen total entre microlitros y mililitros",
            problem=(
                "Se preparan 24 muestras y cada una requiere 35 microlitros. Calcular el volumen "
                "total en microlitros y mililitros."
            ),
            reasoning=(
                "Identificar dos entradas enteras: número de muestras y volumen por muestra.",
                "Multiplicar para obtener el total en microlitros.",
                "Dividir por 1000 para convertir a mililitros.",
                "Conservar nombres que incluyan la unidad para evitar errores dimensionales.",
            ),
            code=(
                "sample_count = 24\n"
                "volume_per_sample_ul = 35\n"
                "total_volume_ul = sample_count * volume_per_sample_ul\n"
                "total_volume_ml = total_volume_ul / 1000\n"
                "print(total_volume_ul)\n"
                "print(total_volume_ml)"
            ),
            expected_output="840\n0.84",
            explanation=(
                "Los nombres terminados en _ul y _ml convierten la unidad en parte explícita del "
                "modelo. La primera operación conserva int; la división con / produce float. El "
                "resultado puede comprobarse dimensionalmente: 840 µL es menor que 1 mL."
            ),
        ),
        WorkedExample(
            example_id="numeric-text-input",
            title="Transformar una entrada textual en un conteo numérico",
            problem=(
                "El usuario introduce el número de muestras como texto. El programa debe añadir "
                "dos controles y mostrar el total de tubos necesarios."
            ),
            reasoning=(
                "Reconocer que input devuelve str.",
                "Convertir la cadena a int antes de realizar suma aritmética.",
                "Mantener separadas la representación textual y la cantidad numérica.",
            ),
            code=(
                "raw_sample_count = '18'\n"
                "sample_count = int(raw_sample_count)\n"
                "control_count = 2\n"
                "tube_count = sample_count + control_count\n"
                "print(tube_count)"
            ),
            expected_output="20",
            explanation=(
                "Sin int(), la operación '18' + 2 produciría TypeError porque no se puede sumar "
                "directamente str e int. Convertir una vez y asignar el resultado a un nombre "
                "diferente hace visible el cambio de representación."
            ),
        ),
    ),
    practice_exercises=(
        PracticeExercise(
            exercise_id="m01.p01",
            activity_type=ActivityType.CODE_TRACING,
            prompt=(
                "Sin ejecutar el código, determina el valor y el tipo final de a, b y c:\n"
                "a = 7\nb = a / 2\nc = a // 2"
            ),
            hints=(
                "Compara / con //.",
                "La división con / produce float.",
            ),
            solution="a = 7 (int), b = 3.5 (float), c = 3 (int)",
            explanation=(
                "a conserva el literal entero. / representa división real y produce 3.5. // "
                "aplica división entera hacia abajo y produce 3."
            ),
        ),
        PracticeExercise(
            exercise_id="m01.p02",
            activity_type=ActivityType.MATCHING,
            prompt=(
                "Relaciona cada término con su definición: expresión, valor, tipo, variable y "
                "sentencia de asignación."
            ),
            hints=(
                "Pregunta qué se evalúa, qué se obtiene y qué cambia el estado.",
            ),
            solution=(
                "expresión → código evaluable; valor → resultado concreto; tipo → categoría que "
                "define operaciones; variable → nombre asociado a un valor; asignación → sentencia "
                "que evalúa la derecha y actualiza el nombre de la izquierda"
            ),
            explanation=(
                "La separación evita errores de vocabulario y permite describir con precisión la "
                "ejecución de un programa."
            ),
        ),
        PracticeExercise(
            exercise_id="m01.p03",
            activity_type=ActivityType.CODE_TRACING,
            prompt=(
                "Construye una tabla de trazado para:\ncount = 12\ncount = count + 3\n"
                "double_count = count * 2\ncount = 5"
            ),
            hints=(
                "Registra el estado después de cada asignación.",
                "Reasignar count no modifica automáticamente double_count.",
            ),
            solution=(
                "Después de la línea 1: count=12. Línea 2: count=15. Línea 3: count=15, "
                "double_count=30. Línea 4: count=5, double_count=30."
            ),
            explanation=(
                "double_count recibe el valor calculado en la tercera línea; no mantiene un vínculo "
                "dinámico con count."
            ),
        ),
        PracticeExercise(
            exercise_id="m01.p04",
            activity_type=ActivityType.CODE_COMPLETION,
            prompt=(
                "Completa un programa que convierta 2.75 mL a microlitros y almacene el resultado "
                "como entero."
            ),
            hints=(
                "1 mL equivale a 1000 µL.",
                "Realiza la conversión de unidad antes de convertir el tipo.",
            ),
            starter_code=(
                "volume_ml = 2.75\n"
                "volume_ul = ______\n"
                "print(volume_ul)"
            ),
            solution="volume_ul = int(volume_ml * 1000)",
            explanation=(
                "La multiplicación produce 2750.0; int lo representa como el conteo entero 2750."
            ),
        ),
        PracticeExercise(
            exercise_id="m01.p05",
            activity_type=ActivityType.DEBUGGING,
            prompt=(
                "Corrige el error y explica su causa:\nsample_count = '16'\n"
                "total = sample_count + 2\nprint(total)"
            ),
            hints=(
                "Inspecciona los tipos de ambos operandos de +.",
                "Decide si se busca concatenación o suma aritmética.",
            ),
            solution=(
                "sample_count = int('16')\ntotal = sample_count + 2\nprint(total)"
            ),
            explanation=(
                "El código original combina str e int. Como sample_count representa una cantidad, "
                "la corrección semánticamente adecuada es convertirlo a int."
            ),
        ),
        PracticeExercise(
            exercise_id="m01.p06",
            activity_type=ActivityType.SHORT_ANSWER,
            prompt=(
                "Explica por qué (8 + 4) * 3 y 8 + 4 * 3 producen resultados diferentes."
            ),
            hints=(
                "Describe la precedencia y el efecto de los paréntesis.",
            ),
            solution=(
                "Los paréntesis obligan a sumar primero: 12 * 3 = 36. Sin paréntesis, la "
                "multiplicación tiene mayor precedencia: 8 + 12 = 20."
            ),
            explanation=(
                "La respuesta debe justificar el orden de evaluación, no limitarse a dar ambos "
                "resultados."
            ),
        ),
        PracticeExercise(
            exercise_id="m01.p07",
            activity_type=ActivityType.FILL_IN_THE_BLANK,
            prompt=(
                "Completa: input devuelve siempre un valor de tipo ____; para usarlo como número "
                "entero se puede aplicar ____()."
            ),
            hints=(
                "La primera respuesta es el tipo de texto.",
            ),
            solution="str; int",
            explanation=(
                "input produce texto. int convierte una cadena numérica válida en un entero."
            ),
        ),
        PracticeExercise(
            exercise_id="m01.p08",
            activity_type=ActivityType.ORAL_EXPLANATION,
            prompt=(
                "Explica oralmente la diferencia entre un programa que se ejecuta sin excepciones "
                "y un programa correcto. Incluye un ejemplo de error lógico."
            ),
            hints=(
                "Define corrección respecto a una especificación.",
                "Usa un ejemplo con unidades o precedencia.",
            ),
            solution=(
                "Un programa puede ejecutar todas sus sentencias y aun producir una respuesta "
                "distinta de la especificada. Por ejemplo, dividir microlitros por 100 en vez de "
                "1000 no genera excepción, pero produce una conversión de unidad incorrecta."
            ),
            explanation=(
                "Una respuesta sólida distingue evidencia de ejecución de evidencia de corrección."
            ),
        ),
    ),
    assessment_items=(
        AssessmentItem(
            item_id="m01.a01",
            activity_type=ActivityType.MULTIPLE_CHOICE,
            prompt="¿Cuál afirmación describe mejor una expresión en Python?",
            options=(
                "Una combinación evaluable que produce un valor",
                "Un nombre asociado permanentemente a un tipo",
                "Cualquier línea que imprime texto",
                "Un error detectado durante la ejecución",
            ),
            correct_answers=("Una combinación evaluable que produce un valor",),
            explanation=(
                "Una expresión puede incluir literales, variables, operadores y llamadas, y su "
                "evaluación produce un valor."
            ),
        ),
        AssessmentItem(
            item_id="m01.a02",
            activity_type=ActivityType.TRUE_FALSE,
            prompt="La sentencia x = x + 1 expresa una igualdad matemática.",
            options=("Verdadero", "Falso"),
            correct_answers=("Falso",),
            explanation=(
                "Es una actualización de estado: se evalúa x + 1 usando el valor actual y después "
                "se reasigna x."
            ),
        ),
        AssessmentItem(
            item_id="m01.a03",
            activity_type=ActivityType.MULTIPLE_SELECT,
            prompt="Selecciona todas las expresiones cuyo resultado es de tipo float.",
            options=("5 / 2", "5 // 2", "float(5)", "5 + 2", "int(2.9)"),
            correct_answers=("5 / 2", "float(5)"),
            explanation=(
                "/ produce float y float(5) crea 5.0. Las demás expresiones producen int."
            ),
        ),
        AssessmentItem(
            item_id="m01.a04",
            activity_type=ActivityType.CODE_TRACING,
            prompt=(
                "Indica la salida exacta:\nx = 4\ny = x + 3\nx = 10\nprint(y)"
            ),
            options=(),
            correct_answers=("7",),
            explanation=(
                "y recibe 7 antes de que x sea reasignada. La reasignación posterior de x no "
                "modifica y."
            ),
            rubric=(
                "1 punto por la salida 7.",
                "1 punto por explicar que las variables no mantienen una dependencia automática.",
            ),
        ),
        AssessmentItem(
            item_id="m01.a05",
            activity_type=ActivityType.FILL_IN_THE_BLANK,
            prompt="El operador de exponenciación en Python es ____.",
            options=(),
            correct_answers=("**",),
            explanation="Python usa **; ^ representa una operación bit a bit diferente.",
        ),
        AssessmentItem(
            item_id="m01.a06",
            activity_type=ActivityType.DEBUGGING,
            prompt=(
                "Identifica el tipo de error principal en: total = '12' / 3 y propón una corrección."
            ),
            options=(),
            correct_answers=("TypeError; total = int('12') / 3",),
            explanation=(
                "La sintaxis es válida, pero / no admite str como operando numérico. La cadena debe "
                "convertirse antes de dividir."
            ),
            rubric=(
                "Identifica TypeError o incompatibilidad de tipos.",
                "Convierte la cadena a int o float antes de la división.",
                "Explica por qué la corrección coincide con el significado numérico del dato.",
            ),
        ),
        AssessmentItem(
            item_id="m01.a07",
            activity_type=ActivityType.ORDERING,
            prompt="Ordena las fases desde la situación real hasta la ejecución concreta.",
            options=("Programa", "Problema", "Algoritmo", "Modelo"),
            correct_answers=("Problema", "Modelo", "Algoritmo", "Programa"),
            explanation=(
                "Primero se delimita el problema, después se modela, se diseña un algoritmo y se "
                "implementa como programa."
            ),
        ),
        AssessmentItem(
            item_id="m01.a08",
            activity_type=ActivityType.MATCHING,
            prompt="Relaciona cada error con su descripción.",
            options=(
                "SyntaxError → estructura no válida",
                "TypeError → operación incompatible con los tipos",
                "Error lógico → resultado incorrecto sin excepción necesaria",
            ),
            correct_answers=(
                "SyntaxError → estructura no válida",
                "TypeError → operación incompatible con los tipos",
                "Error lógico → resultado incorrecto sin excepción necesaria",
            ),
            explanation=(
                "Las tres categorías requieren estrategias de diagnóstico diferentes."
            ),
        ),
        AssessmentItem(
            item_id="m01.a09",
            activity_type=ActivityType.SHORT_ANSWER,
            prompt=(
                "Define qué información mínima debe contener una prueba de programa."
            ),
            options=(),
            correct_answers=(
                "Una entrada concreta, un resultado esperado y un criterio para comparar el "
                "resultado observado con el esperado.",
            ),
            explanation=(
                "Sin resultado esperado no existe una prueba, solo una ejecución."
            ),
            rubric=(
                "Menciona la entrada.",
                "Menciona el resultado esperado.",
                "Menciona la comparación o criterio de aceptación.",
            ),
        ),
        AssessmentItem(
            item_id="m01.a10",
            activity_type=ActivityType.CODE_COMPLETION,
            prompt=(
                "Completa la conversión para que la salida sea 1500:\nvolume_ml = 1.5\n"
                "volume_ul = ____\nprint(volume_ul)"
            ),
            options=(),
            correct_answers=("int(volume_ml * 1000)",),
            explanation=(
                "Multiplicar por 1000 convierte mL a µL y la conversión a int representa el conteo "
                "sin parte decimal."
            ),
        ),
    ),
    tutor_support=TutorSupportPacket(
        canonical_explanation=(
            "Este módulo enseña a interpretar un programa como una transformación verificable de "
            "entradas en salidas. El estudiante debe aprender a separar cuatro niveles: el problema "
            "concreto, el modelo que conserva las variables relevantes, el algoritmo que especifica "
            "los pasos y el programa Python que los ejecuta. Dentro del programa, una expresión se "
            "evalúa para producir un valor; cada valor tiene un tipo; una variable es un nombre que "
            "apunta al valor actual; y una asignación modifica el estado después de evaluar por "
            "completo su lado derecho. La comprensión se demuestra prediciendo resultados, trazando "
            "estados y justificando conversiones, no memorizando símbolos de forma aislada. La "
            "corrección exige comparar el comportamiento con una especificación mediante pruebas."
        ),
        knowledge_fragments=(
            "En Python, / produce float y // produce el cociente entero hacia abajo.",
            "input devuelve str; una cadena numérica debe convertirse antes de operaciones aritméticas.",
            "Una variable puede asociarse sucesivamente con valores de tipos diferentes, pero cada "
            "valor tiene un tipo definido.",
            "La asignación evalúa primero el lado derecho y después actualiza el nombre de la izquierda.",
            "Reasignar una variable no recalcula automáticamente otras variables obtenidas de ella.",
            "int aplicado a float elimina la parte fraccionaria hacia cero; no equivale a round.",
            "Los paréntesis pueden alterar la precedencia y también documentar la intención.",
            "Un programa sin excepciones puede seguir siendo incorrecto por un error lógico.",
            "Una prueba requiere un resultado esperado definido antes de observar el resultado real.",
            "Los nombres que incluyen unidades reducen la probabilidad de errores dimensionales.",
        ),
        common_misconceptions=(
            "Confundir = con igualdad matemática en lugar de asignación.",
            "Creer que '12' es un número porque contiene dígitos.",
            "Suponer que int(4.9) redondea a 5.",
            "Usar ^ como exponenciación.",
            "Pensar que cambiar x actualiza automáticamente y si y fue calculada previamente con x.",
            "Interpretar cualquier error como error de sintaxis.",
            "Considerar que una ejecución sin excepción demuestra que el programa es correcto.",
            "Omitir las unidades al definir variables numéricas.",
        ),
        socratic_questions=(
            "¿Cuáles son exactamente las entradas y qué tipo debería tener cada una?",
            "¿Qué valor produce primero la expresión situada a la derecha?",
            "¿Qué nombres cambian después de esta sentencia y cuáles permanecen iguales?",
            "¿La operación que intentas realizar está definida para esos tipos?",
            "¿Qué unidad representa cada variable antes y después de la operación?",
            "¿Qué resultado esperabas para una entrada pequeña que puedas calcular a mano?",
            "¿El fallo impide ejecutar el código o produce una respuesta equivocada?",
            "¿Puedes construir una tabla con una fila por sentencia y una columna por variable?",
        ),
        grading_criteria=(
            "Usa vocabulario técnico con significado correcto.",
            "Predice tanto el valor como el tipo cuando la pregunta lo exige.",
            "Justifica conversiones y no las añade por ensayo y error.",
            "Mantiene consistencia de unidades en el modelo y en el código.",
            "Explica el orden de evaluación de forma explícita.",
            "Distingue correctamente sintaxis, ejecución y lógica.",
            "Propone pruebas con entrada y resultado esperado concretos.",
            "En explicaciones orales, conecta el código con la especificación del problema.",
        ),
        response_constraints=(
            "Responder primero con una pista cuando el estudiante esté resolviendo un ejercicio, "
            "salvo que solicite explícitamente la solución completa.",
            "No inventar reglas de Python; cuando exista duda, recomendar una prueba mínima reproducible.",
            "No evaluar como correcto un resultado sin revisar también el razonamiento y los tipos.",
            "No introducir condicionales, bucles, funciones avanzadas u objetos para resolver ejercicios "
            "que solo requieren los conceptos de este módulo.",
            "Separar claramente explicación conceptual, trazado y código corregido.",
            "Cuando haya un error de unidades, señalarlo antes de discutir detalles sintácticos.",
            "Usar ejemplos biomédicos únicamente como contexto computacional, sin convertirlos en "
            "recomendaciones clínicas.",
        ),
        source_basis=(
            "Descripción oficial de DM857, SDU, versión activa aprobada en 2025.",
            "Think Python, tercera edición, capítulos introductorios sobre programación, expresiones, "
            "valores, tipos, variables y práctica con asistentes virtuales.",
            "Introduction to Computation and Programming Using Python, tercera edición, fundamentos "
            "de modelado, control de estado y resolución computacional de problemas.",
        ),
    ),
)
