"""DM857 module 2: Boolean logic, comparisons, and conditional execution."""

from __future__ import annotations

from ...i18n import AppLocale
from ...learning.activity_types import ActivityType
from ..localized_models import (
    LocalizedAssessmentItem,
    LocalizedAssessmentOption,
    LocalizedConceptBlock,
    LocalizedLearningModule,
    LocalizedLearningObjective,
    LocalizedPracticeExercise,
    LocalizedText,
    LocalizedTutorSupportPacket,
    LocalizedWorkedExample,
)


def _t(spanish: str, english: str, danish: str) -> LocalizedText:
    return LocalizedText(spanish=spanish, english=english, danish=danish)


def _same(text: str) -> LocalizedText:
    return _t(text, text, text)


def _option(
    option_id: str,
    spanish: str,
    english: str,
    danish: str,
) -> LocalizedAssessmentOption:
    return LocalizedAssessmentOption(option_id=option_id, text=_t(spanish, english, danish))


LOCALIZED_MODULE_02_CONDITIONALS = LocalizedLearningModule(
    course_code="DM857",
    module_id="dm857.m02",
    title=_t(
        "Lógica booleana, comparaciones y estructuras condicionales",
        "Boolean logic, comparisons, and conditional statements",
        "Boolesk logik, sammenligninger og betingede sætninger",
    ),
    summary=_t(
        "Este módulo desarrolla la capacidad de expresar decisiones verificables en Python. "
        "Se estudian los valores booleanos, los operadores de comparación y lógicos, la "
        "evaluación en cortocircuito, las estructuras if, elif y else, la validación de "
        "entradas, los casos límite y el diseño de pruebas para ramas de ejecución.",
        "This module develops the ability to express verifiable decisions in Python. It covers "
        "Boolean values, comparison and logical operators, short-circuit evaluation, if, elif, "
        "and else statements, input validation, boundary cases, and tests for execution branches.",
        "Dette modul udvikler evnen til at udtrykke efterprøvelige beslutninger i Python. Det "
        "dækker booleske værdier, sammenlignings- og logiske operatorer, kortslutningsevaluering, "
        "if-, elif- og else-sætninger, validering af input, grænsetilfælde og test af programgrene.",
    ),
    objectives=(
        LocalizedLearningObjective(
            "m02.o1",
            _t(
                "Interpretar bool como un tipo con los valores True y False y construir predicados verificables.",
                "Interpret bool as a type with the values True and False and construct verifiable predicates.",
                "Fortolke bool som en type med værdierne True og False og opbygge efterprøvelige prædikater.",
            ),
        ),
        LocalizedLearningObjective(
            "m02.o2",
            _t(
                "Predecir el resultado de comparaciones simples y encadenadas antes de ejecutar el código.",
                "Predict the result of simple and chained comparisons before executing code.",
                "Forudsige resultatet af enkle og kædede sammenligninger før koden køres.",
            ),
        ),
        LocalizedLearningObjective(
            "m02.o3",
            _t(
                "Combinar condiciones con and, or y not respetando su precedencia y su significado.",
                "Combine conditions with and, or, and not while respecting precedence and meaning.",
                "Kombinere betingelser med and, or og not under hensyntagen til præcedens og betydning.",
            ),
        ),
        LocalizedLearningObjective(
            "m02.o4",
            _t(
                "Explicar y utilizar la evaluación en cortocircuito para evitar operaciones innecesarias o inválidas.",
                "Explain and use short-circuit evaluation to avoid unnecessary or invalid operations.",
                "Forklare og anvende kortslutningsevaluering for at undgå unødvendige eller ugyldige operationer.",
            ),
        ),
        LocalizedLearningObjective(
            "m02.o5",
            _t(
                "Diseñar estructuras if, elif y else cuyas ramas sean mutuamente coherentes y cubran el problema.",
                "Design if, elif, and else structures whose branches are coherent and cover the problem.",
                "Designe if-, elif- og else-strukturer, hvor grenene er sammenhængende og dækker problemet.",
            ),
        ),
        LocalizedLearningObjective(
            "m02.o6",
            _t(
                "Comparar condiciones compuestas con condicionales anidados y elegir la forma más legible.",
                "Compare compound conditions with nested conditionals and choose the more readable form.",
                "Sammenligne sammensatte betingelser med indlejrede betingelser og vælge den mest læsbare form.",
            ),
        ),
        LocalizedLearningObjective(
            "m02.o7",
            _t(
                "Diseñar casos de prueba normales, límite e inválidos para verificar todas las ramas relevantes.",
                "Design normal, boundary, and invalid test cases to verify every relevant branch.",
                "Designe normale, grænse- og ugyldige testtilfælde, der verificerer alle relevante grene.",
            ),
        ),
    ),
    concepts=(
        LocalizedConceptBlock(
            concept_id="boolean-values-and-predicates",
            title=_t(
                "Valores booleanos y predicados",
                "Boolean values and predicates",
                "Booleske værdier og prædikater",
            ),
            body=_t(
                "Un valor booleano pertenece al tipo bool y solo puede ser True o False. Una "
                "condición útil no es una frase imprecisa, sino un predicado que Python puede "
                "evaluar. Por ejemplo, concentration >= 20 expresa una afirmación verificable sobre "
                "el estado actual del programa. Conviene nombrar las variables booleanas como "
                "preguntas o propiedades, por ejemplo is_valid o has_control, para que su significado "
                "sea visible. No debe confundirse el valor booleano True con la cadena 'True'.",
                "A Boolean value belongs to type bool and can only be True or False. A useful "
                "condition is not a vague sentence but a predicate that Python can evaluate. For "
                "example, concentration >= 20 expresses a verifiable claim about the current program "
                "state. Boolean variables should be named as questions or properties, such as "
                "is_valid or has_control. The Boolean value True must not be confused with the string 'True'.",
                "En boolesk værdi tilhører typen bool og kan kun være True eller False. En nyttig "
                "betingelse er ikke en upræcis sætning, men et prædikat, som Python kan evaluere. "
                "Eksempelvis udtrykker concentration >= 20 en efterprøvelig påstand om programmets "
                "aktuelle tilstand. Booleske variable bør navngives som spørgsmål eller egenskaber, "
                "såsom is_valid eller has_control. Den booleske værdi True må ikke forveksles med teksten 'True'.",
            ),
            key_points=(
                _t(
                    "bool tiene exactamente dos valores: True y False.",
                    "bool has exactly two values: True and False.",
                    "bool har præcis to værdier: True og False.",
                ),
                _t(
                    "Un predicado es una expresión cuyo resultado es booleano.",
                    "A predicate is an expression whose result is Boolean.",
                    "Et prædikat er et udtryk, hvis resultat er boolesk.",
                ),
                _t(
                    "True no es lo mismo que la cadena 'True'.",
                    "True is not the same as the string 'True'.",
                    "True er ikke det samme som tekststrengen 'True'.",
                ),
                _t(
                    "Los nombres booleanos deben comunicar qué propiedad representan.",
                    "Boolean names should communicate which property they represent.",
                    "Booleske navne bør kommunikere, hvilken egenskab de repræsenterer.",
                ),
            ),
        ),
        LocalizedConceptBlock(
            concept_id="comparison-operators",
            title=_t(
                "Operadores de comparación",
                "Comparison operators",
                "Sammenligningsoperatorer",
            ),
            body=_t(
                "Python compara valores con ==, !=, <, <=, > y >=. El operador == pregunta si dos "
                "valores son iguales, mientras que = realiza una asignación. Las comparaciones deben "
                "tener sentido para los tipos implicados: comparar dos números es habitual, pero "
                "ordenar texto sigue reglas lexicográficas y puede no representar la intención del "
                "problema. Las comparaciones encadenadas, como 18 <= age <= 65, equivalen a combinar "
                "dos comparaciones con and y suelen expresar intervalos con mayor claridad.",
                "Python compares values with ==, !=, <, <=, >, and >=. The == operator asks whether "
                "two values are equal, whereas = performs assignment. Comparisons must make sense "
                "for the types involved. Chained comparisons such as 18 <= age <= 65 are equivalent "
                "to combining two comparisons with and and often express intervals more clearly.",
                "Python sammenligner værdier med ==, !=, <, <=, > og >=. Operatoren == undersøger, "
                "om to værdier er ens, mens = udfører en tildeling. Sammenligninger skal give mening "
                "for de involverede typer. Kædede sammenligninger som 18 <= age <= 65 svarer til to "
                "sammenligninger kombineret med and og udtrykker ofte intervaller tydeligere.",
            ),
            key_points=(
                _t(
                    "== compara; = asigna.",
                    "== compares; = assigns.",
                    "== sammenligner; = tildeler.",
                ),
                _t(
                    "<= y >= incluyen el valor límite.",
                    "<= and >= include the boundary value.",
                    "<= og >= inkluderer grænseværdien.",
                ),
                _t(
                    "Las comparaciones encadenadas son apropiadas para intervalos.",
                    "Chained comparisons are appropriate for intervals.",
                    "Kædede sammenligninger er velegnede til intervaller.",
                ),
                _t(
                    "El significado de una comparación depende de los tipos y del modelo.",
                    "The meaning of a comparison depends on the types and the model.",
                    "Betydningen af en sammenligning afhænger af typerne og modellen.",
                ),
            ),
        ),
        LocalizedConceptBlock(
            concept_id="logical-operators-and-precedence",
            title=_t(
                "Operadores lógicos y precedencia",
                "Logical operators and precedence",
                "Logiske operatorer og præcedens",
            ),
            body=_t(
                "Los operadores and, or y not combinan o invierten condiciones. and solo produce "
                "True cuando ambos operandos son verdaderos; or produce True cuando al menos uno lo "
                "es; not invierte la verdad de una condición. Entre estos operadores, not tiene mayor "
                "precedencia que and, y and mayor que or. Aunque la precedencia sea conocida, los "
                "paréntesis son recomendables cuando hacen explícita la lógica del problema. Aplicar "
                "las leyes de De Morgan ayuda a revisar negaciones compuestas sin cambiar su significado.",
                "The operators and, or, and not combine or invert conditions. and is True only when "
                "both operands are true; or is True when at least one is true; not reverses a "
                "condition. not has higher precedence than and, and and has higher precedence than "
                "or. Parentheses are still useful when they make the problem logic explicit. De "
                "Morgan's laws help verify compound negations without changing their meaning.",
                "Operatorerne and, or og not kombinerer eller vender betingelser. and er kun True, "
                "når begge operander er sande; or er True, når mindst én er sand; not vender en "
                "betingelses sandhedsværdi. not har højere præcedens end and, og and har højere "
                "præcedens end or. Parenteser er stadig nyttige, når de gør problemets logik tydelig. "
                "De Morgans love hjælper med at kontrollere sammensatte negationer.",
            ),
            key_points=(
                _t(
                    "and exige que todas las condiciones combinadas sean verdaderas.",
                    "and requires all combined conditions to be true.",
                    "and kræver, at alle kombinerede betingelser er sande.",
                ),
                _t(
                    "or exige al menos una condición verdadera.",
                    "or requires at least one true condition.",
                    "or kræver mindst én sand betingelse.",
                ),
                _t(
                    "La precedencia es not, después and y finalmente or.",
                    "Precedence is not, then and, then or.",
                    "Præcedensen er not, derefter and og til sidst or.",
                ),
                _t(
                    "Los paréntesis pueden documentar la intención aunque no sean obligatorios.",
                    "Parentheses can document intent even when not required.",
                    "Parenteser kan dokumentere hensigten, selv når de ikke er nødvendige.",
                ),
            ),
        ),
        LocalizedConceptBlock(
            concept_id="short-circuit-evaluation",
            title=_t(
                "Evaluación en cortocircuito",
                "Short-circuit evaluation",
                "Kortslutningsevaluering",
            ),
            body=_t(
                "Python evalúa and y or de izquierda a derecha y se detiene cuando el resultado ya "
                "está determinado. En A and B, si A es False, B no se evalúa. En A or B, si A es True, "
                "B no se evalúa. Este comportamiento permite proteger operaciones que solo son válidas "
                "bajo cierta condición. Por ejemplo, denominator != 0 and numerator / denominator > 2 "
                "evita la división cuando el denominador es cero. El orden de los operandos forma parte "
                "de la corrección y no debe elegirse al azar.",
                "Python evaluates and and or from left to right and stops when the result is already "
                "known. In A and B, B is not evaluated when A is False. In A or B, B is not evaluated "
                "when A is True. This can protect operations that are only valid under a condition. For "
                "example, denominator != 0 and numerator / denominator > 2 avoids division by zero. "
                "Operand order is therefore part of correctness.",
                "Python evaluerer and og or fra venstre mod højre og stopper, når resultatet allerede "
                "er bestemt. I A and B evalueres B ikke, hvis A er False. I A or B evalueres B ikke, "
                "hvis A er True. Det kan beskytte operationer, som kun er gyldige under en bestemt "
                "betingelse. Eksempelvis undgår denominator != 0 and numerator / denominator > 2 "
                "division med nul. Operandernes rækkefølge er derfor en del af korrektheden.",
            ),
            key_points=(
                _t(
                    "and se detiene ante el primer operando falso.",
                    "and stops at the first false operand.",
                    "and stopper ved den første falske operand.",
                ),
                _t(
                    "or se detiene ante el primer operando verdadero.",
                    "or stops at the first true operand.",
                    "or stopper ved den første sande operand.",
                ),
                _t(
                    "La condición protectora debe situarse antes de la operación sensible.",
                    "The guard condition must appear before the sensitive operation.",
                    "Beskyttelsesbetingelsen skal stå før den følsomme operation.",
                ),
                _t(
                    "El cortocircuito no sustituye una especificación clara de los casos inválidos.",
                    "Short-circuiting does not replace a clear specification of invalid cases.",
                    "Kortslutning erstatter ikke en klar specifikation af ugyldige tilfælde.",
                ),
            ),
        ),
        LocalizedConceptBlock(
            concept_id="if-elif-else-control-flow",
            title=_t(
                "Flujo condicional con if, elif y else",
                "Conditional flow with if, elif, and else",
                "Betinget kontrolflow med if, elif og else",
            ),
            body=_t(
                "Una estructura condicional selecciona qué bloque ejecutar según el primer predicado "
                "verdadero. if inicia la decisión, cada elif añade una alternativa y else cubre los "
                "casos restantes. En una misma cadena solo se ejecuta una rama. Por ello, el orden "
                "importa: las condiciones más específicas suelen colocarse antes que las más generales. "
                "La indentación delimita los bloques y forma parte de la sintaxis. Una cadena de ramas "
                "debe representar categorías coherentes, sin solapamientos accidentales ni huecos no previstos.",
                "A conditional statement selects which block to execute according to the first true "
                "predicate. if starts the decision, each elif adds an alternative, and else covers the "
                "remaining cases. Only one branch in the chain executes. Order matters, so more specific "
                "conditions usually precede more general ones. Indentation defines blocks and is part of "
                "the syntax. Branches should form coherent categories without accidental overlap or gaps.",
                "En betinget sætning vælger den blok, der skal udføres, ud fra det første sande prædikat. "
                "if starter beslutningen, hver elif tilføjer et alternativ, og else dækker de resterende "
                "tilfælde. Kun én gren i kæden udføres. Rækkefølgen er vigtig, så mere specifikke "
                "betingelser står normalt før mere generelle. Indrykning afgrænser blokkene og er en del "
                "af syntaksen. Grenene bør danne sammenhængende kategorier uden utilsigtet overlap eller huller.",
            ),
            key_points=(
                _t(
                    "Se ejecuta la primera rama cuya condición es True.",
                    "The first branch whose condition is True executes.",
                    "Den første gren med betingelsen True udføres.",
                ),
                _t(
                    "else no lleva condición y cubre los casos restantes.",
                    "else has no condition and covers the remaining cases.",
                    "else har ingen betingelse og dækker de resterende tilfælde.",
                ),
                _t(
                    "La indentación define qué sentencias pertenecen a cada rama.",
                    "Indentation defines which statements belong to each branch.",
                    "Indrykning definerer, hvilke sætninger der tilhører hver gren.",
                ),
                _t(
                    "El orden debe revisarse cuando las condiciones se solapan.",
                    "Order must be reviewed when conditions overlap.",
                    "Rækkefølgen skal kontrolleres, når betingelser overlapper.",
                ),
            ),
        ),
        LocalizedConceptBlock(
            concept_id="compound-versus-nested-conditionals",
            title=_t(
                "Condiciones compuestas y condicionales anidados",
                "Compound and nested conditionals",
                "Sammensatte og indlejrede betingelser",
            ),
            body=_t(
                "Una condición compuesta reúne varios predicados en una sola expresión. Un condicional "
                "anidado coloca otra decisión dentro de una rama. Ambas formas pueden producir el mismo "
                "resultado, pero no siempre comunican la misma estructura del problema. Una expresión "
                "compuesta suele ser adecuada cuando todos los requisitos pertenecen a una sola regla. "
                "El anidamiento resulta útil cuando la segunda decisión solo tiene sentido después de la "
                "primera. Debe evitarse una profundidad innecesaria: las condiciones guardián y la "
                "simplificación lógica suelen mejorar la legibilidad.",
                "A compound condition combines several predicates in one expression. A nested "
                "conditional places another decision inside a branch. Both forms may produce the same "
                "result, but they do not always communicate the same problem structure. A compound "
                "condition is suitable when all requirements belong to one rule. Nesting is useful when "
                "the second decision only makes sense after the first. Unnecessary depth should be avoided.",
                "En sammensat betingelse kombinerer flere prædikater i ét udtryk. En indlejret "
                "betingelse placerer en ny beslutning inde i en gren. Begge former kan give samme "
                "resultat, men kommunikerer ikke altid den samme problemstruktur. En sammensat betingelse "
                "er velegnet, når alle krav tilhører én regel. Indlejring er nyttig, når den anden "
                "beslutning kun giver mening efter den første. Unødvendig dybde bør undgås.",
            ),
            key_points=(
                _t(
                    "Las condiciones compuestas expresan varios requisitos de una misma decisión.",
                    "Compound conditions express several requirements of one decision.",
                    "Sammensatte betingelser udtrykker flere krav til én beslutning.",
                ),
                _t(
                    "El anidamiento expresa decisiones dependientes por etapas.",
                    "Nesting expresses dependent decisions in stages.",
                    "Indlejring udtrykker afhængige beslutninger i trin.",
                ),
                _t(
                    "La equivalencia lógica no garantiza igual legibilidad.",
                    "Logical equivalence does not guarantee equal readability.",
                    "Logisk ækvivalens garanterer ikke samme læsbarhed.",
                ),
                _t(
                    "La estructura elegida debe reflejar el modelo del problema.",
                    "The chosen structure should reflect the problem model.",
                    "Den valgte struktur bør afspejle problemets model.",
                ),
            ),
        ),
        LocalizedConceptBlock(
            concept_id="validation-boundaries-and-branch-testing",
            title=_t(
                "Validación, límites y pruebas de ramas",
                "Validation, boundaries, and branch testing",
                "Validering, grænser og test af grene",
            ),
            body=_t(
                "Las decisiones suelen fallar en los límites. Si una categoría incluye 20, debe "
                "escribirse >= 20; si lo excluye, > 20. Una validación separa entradas aceptables de "
                "entradas imposibles o fuera de especificación antes de aplicar reglas posteriores. "
                "Para probar una estructura condicional se necesita al menos un caso que active cada "
                "rama, además de valores exactamente en los límites y justo a ambos lados. Cuando una "
                "condición combina varios predicados, las pruebas deben variar cada componente de forma controlada.",
                "Decision logic often fails at boundaries. If a category includes 20, it must use >= 20; "
                "if it excludes 20, it must use > 20. Validation separates acceptable input from impossible "
                "or out-of-specification input before later rules are applied. Testing a conditional requires "
                "at least one case for every branch, values exactly on boundaries, and values immediately on "
                "both sides. Compound conditions require controlled variation of each component.",
                "Beslutningslogik fejler ofte ved grænser. Hvis en kategori inkluderer 20, skal den bruge "
                ">= 20; hvis 20 udelukkes, skal den bruge > 20. Validering adskiller acceptable input fra "
                "umulige eller uspecificerede input, før senere regler anvendes. Test af en betingelse kræver "
                "mindst ét tilfælde for hver gren samt værdier præcis på og lige på begge sider af grænserne. "
                "Sammensatte betingelser kræver kontrolleret variation af hver komponent.",
            ),
            key_points=(
                _t(
                    "Cada rama relevante necesita al menos un caso de prueba.",
                    "Every relevant branch needs at least one test case.",
                    "Hver relevant gren kræver mindst ét testtilfælde.",
                ),
                _t(
                    "Los operadores inclusivos y exclusivos cambian el comportamiento en el límite.",
                    "Inclusive and exclusive operators change boundary behaviour.",
                    "Inklusive og eksklusive operatorer ændrer adfærden ved grænsen.",
                ),
                _t(
                    "La validación debe ocurrir antes de usar un dato en reglas posteriores.",
                    "Validation should occur before data are used in later rules.",
                    "Validering bør ske, før data bruges i senere regler.",
                ),
                _t(
                    "Las pruebas deben cubrir valores normales, límite e inválidos.",
                    "Tests should cover normal, boundary, and invalid values.",
                    "Test bør dække normale, grænse- og ugyldige værdier.",
                ),
            ),
        ),
    ),
    worked_examples=(
        LocalizedWorkedExample(
            example_id="sample-quality-decision",
            title=_t(
                "Clasificar una muestra mediante dos criterios de calidad",
                "Classify a sample using two quality criteria",
                "Klassificér en prøve med to kvalitetskriterier",
            ),
            problem=_t(
                "En regla didáctica considera aceptable una muestra cuando concentration_ng_ul es "
                "al menos 20 y purity_ratio está entre 1.8 y 2.1, ambos límites incluidos. Mostrar "
                "'acceptable' o 'review'. Los umbrales son únicamente un ejemplo de programación.",
                "A teaching rule considers a sample acceptable when concentration_ng_ul is at least "
                "20 and purity_ratio is between 1.8 and 2.1 inclusive. Display 'acceptable' or "
                "'review'. The thresholds are only a programming example.",
                "En undervisningsregel betragter en prøve som acceptabel, når concentration_ng_ul er "
                "mindst 20, og purity_ratio ligger mellem 1.8 og 2.1 inklusive. Vis 'acceptable' eller "
                "'review'. Grænserne er kun et programmeringseksempel.",
            ),
            reasoning=(
                _t(
                    "Convertir cada requisito en un predicado independiente.",
                    "Convert each requirement into an independent predicate.",
                    "Omsæt hvert krav til et selvstændigt prædikat.",
                ),
                _t(
                    "Usar una comparación encadenada para el intervalo de pureza.",
                    "Use a chained comparison for the purity interval.",
                    "Brug en kædet sammenligning til renhedsintervallet.",
                ),
                _t(
                    "Combinar ambos requisitos con and porque los dos deben cumplirse.",
                    "Combine both requirements with and because both must hold.",
                    "Kombinér begge krav med and, fordi begge skal være opfyldt.",
                ),
                _t(
                    "Usar else para cubrir todos los casos no aceptables.",
                    "Use else to cover all non-acceptable cases.",
                    "Brug else til at dække alle ikke-acceptable tilfælde.",
                ),
            ),
            code=_same(
                "concentration_ng_ul = 24.0\n"
                "purity_ratio = 1.92\n"
                "\n"
                "has_enough_material = concentration_ng_ul >= 20\n"
                "purity_in_range = 1.8 <= purity_ratio <= 2.1\n"
                "\n"
                "if has_enough_material and purity_in_range:\n"
                "    print('acceptable')\n"
                "else:\n"
                "    print('review')"
            ),
            expected_output=_same("acceptable"),
            explanation=_t(
                "Los nombres booleanos hacen visible qué representa cada condición. La comparación "
                "encadenada incluye ambos límites y la rama else cubre cualquier incumplimiento.",
                "The Boolean names make each condition explicit. The chained comparison includes both "
                "boundaries, and the else branch covers any failed requirement.",
                "De booleske navne gør hver betingelse tydelig. Den kædede sammenligning inkluderer "
                "begge grænser, og else-grenen dækker ethvert krav, der ikke er opfyldt.",
            ),
        ),
        LocalizedWorkedExample(
            example_id="safe-ratio-check",
            title=_t(
                "Proteger una división con evaluación en cortocircuito",
                "Protect division with short-circuit evaluation",
                "Beskyt division med kortslutningsevaluering",
            ),
            problem=_t(
                "Determinar si signal/control es mayor que 1.5 sin dividir cuando control vale cero.",
                "Determine whether signal/control is greater than 1.5 without dividing when control is zero.",
                "Afgør, om signal/control er større end 1.5 uden at dividere, når control er nul.",
            ),
            reasoning=(
                _t(
                    "Comprobar primero que el denominador no sea cero.",
                    "Check first that the denominator is not zero.",
                    "Kontrollér først, at nævneren ikke er nul.",
                ),
                _t(
                    "Colocar la división como segundo operando de and.",
                    "Place the division as the second operand of and.",
                    "Placér divisionen som anden operand til and.",
                ),
                _t(
                    "Aprovechar que Python no evalúa el segundo operando si el primero es False.",
                    "Use the fact that Python skips the second operand when the first is False.",
                    "Udnyt, at Python springer anden operand over, når den første er False.",
                ),
            ),
            code=_same(
                "signal = 18.0\n"
                "control = 0.0\n"
                "\n"
                "ratio_is_high = control != 0 and signal / control > 1.5\n"
                "print(ratio_is_high)"
            ),
            expected_output=_same("False"),
            explanation=_t(
                "control != 0 es False, por lo que Python no evalúa signal / control. Si se invirtiera "
                "el orden, la protección desaparecería y se produciría ZeroDivisionError.",
                "control != 0 is False, so Python does not evaluate signal / control. Reversing the "
                "order would remove the protection and cause ZeroDivisionError.",
                "control != 0 er False, så Python evaluerer ikke signal / control. Hvis rækkefølgen "
                "blev vendt, ville beskyttelsen forsvinde, og ZeroDivisionError ville opstå.",
            ),
        ),
        LocalizedWorkedExample(
            example_id="three-way-temperature-label",
            title=_t(
                "Construir una clasificación de tres ramas",
                "Build a three-branch classification",
                "Opbyg en klassifikation med tre grene",
            ),
            problem=_t(
                "Una simulación de laboratorio etiqueta una lectura como 'below range' si es menor "
                "que 36.0, 'within range' si está entre 36.0 y 37.5 inclusive y 'above range' si es mayor.",
                "A laboratory simulation labels a reading as 'below range' below 36.0, 'within range' "
                "from 36.0 to 37.5 inclusive, and 'above range' above 37.5.",
                "En laboratoriesimulering mærker en måling som 'below range' under 36.0, 'within range' "
                "fra 36.0 til og med 37.5 og 'above range' over 37.5.",
            ),
            reasoning=(
                _t(
                    "Ordenar las ramas desde el intervalo inferior al superior.",
                    "Order branches from the lower interval to the upper interval.",
                    "Ordne grenene fra det laveste interval til det højeste.",
                ),
                _t(
                    "Usar elif con <= 37.5 porque los valores menores que 36.0 ya fueron descartados.",
                    "Use elif with <= 37.5 because values below 36.0 were already excluded.",
                    "Brug elif med <= 37.5, fordi værdier under 36.0 allerede er udelukket.",
                ),
                _t(
                    "Usar else para todos los valores superiores restantes.",
                    "Use else for all remaining higher values.",
                    "Brug else til alle resterende højere værdier.",
                ),
            ),
            code=_same(
                "temperature_c = 37.5\n"
                "\n"
                "if temperature_c < 36.0:\n"
                "    label = 'below range'\n"
                "elif temperature_c <= 37.5:\n"
                "    label = 'within range'\n"
                "else:\n"
                "    label = 'above range'\n"
                "\n"
                "print(label)"
            ),
            expected_output=_same("within range"),
            explanation=_t(
                "La segunda rama incluye 37.5. No necesita repetir temperature_c >= 36.0 porque llegar "
                "a elif implica que la primera condición ya fue falsa.",
                "The second branch includes 37.5. It need not repeat temperature_c >= 36.0 because "
                "reaching elif means the first condition was false.",
                "Den anden gren inkluderer 37.5. Den behøver ikke gentage temperature_c >= 36.0, "
                "fordi en nået elif betyder, at den første betingelse var falsk.",
            ),
        ),
        LocalizedWorkedExample(
            example_id="input-validation-before-classification",
            title=_t(
                "Validar una entrada antes de clasificarla",
                "Validate input before classification",
                "Validér input før klassifikation",
            ),
            problem=_t(
                "Un porcentaje debe estar entre 0 y 100. Si está fuera del intervalo se muestra "
                "'invalid'; si es válido, se clasifica como 'target met' cuando es al menos 90 y "
                "'target not met' en caso contrario.",
                "A percentage must be between 0 and 100. Out-of-range values display 'invalid'. A valid "
                "value is labelled 'target met' when at least 90 and 'target not met' otherwise.",
                "En procentværdi skal ligge mellem 0 og 100. Værdier uden for intervallet viser "
                "'invalid'. En gyldig værdi mærkes 'target met', når den er mindst 90, og ellers "
                "'target not met'.",
            ),
            reasoning=(
                _t(
                    "Comprobar primero el dominio válido completo.",
                    "Check the complete valid domain first.",
                    "Kontrollér først hele det gyldige domæne.",
                ),
                _t(
                    "Usar una rama elif solo después de saber que el porcentaje es válido.",
                    "Use elif only after establishing that the percentage is valid.",
                    "Brug kun elif, efter at procenten er fastslået som gyldig.",
                ),
                _t(
                    "Reservar else para el resto de valores válidos.",
                    "Reserve else for the remaining valid values.",
                    "Reservér else til de resterende gyldige værdier.",
                ),
            ),
            code=_same(
                "pass_percentage = 104.0\n"
                "\n"
                "if not 0 <= pass_percentage <= 100:\n"
                "    result = 'invalid'\n"
                "elif pass_percentage >= 90:\n"
                "    result = 'target met'\n"
                "else:\n"
                "    result = 'target not met'\n"
                "\n"
                "print(result)"
            ),
            expected_output=_same("invalid"),
            explanation=_t(
                "La validación se ejecuta antes que la clasificación. Así, un valor imposible no puede "
                "ser tratado accidentalmente como si perteneciera a una categoría válida.",
                "Validation occurs before classification, so an impossible value cannot accidentally "
                "be treated as a valid category member.",
                "Valideringen udføres før klassifikationen, så en umulig værdi ikke ved en fejl kan "
                "behandles som medlem af en gyldig kategori.",
            ),
        ),
    ),
    practice_exercises=(
        LocalizedPracticeExercise(
            exercise_id="m02.p01",
            activity_type=ActivityType.CODE_TRACING,
            prompt=_t(
                "Sin ejecutar el código, indica la salida exacta:\nvalue = 12\nif value > 10:\n    print('A')\nelif value > 5:\n    print('B')\nelse:\n    print('C')",
                "Without executing the code, give the exact output:\nvalue = 12\nif value > 10:\n    print('A')\nelif value > 5:\n    print('B')\nelse:\n    print('C')",
                "Uden at køre koden skal du angive det præcise output:\nvalue = 12\nif value > 10:\n    print('A')\nelif value > 5:\n    print('B')\nelse:\n    print('C')",
            ),
            hints=(
                _t(
                    "Busca la primera condición verdadera.",
                    "Find the first true condition.",
                    "Find den første sande betingelse.",
                ),
                _t(
                    "Una cadena if-elif-else ejecuta como máximo una rama.",
                    "An if-elif-else chain executes at most one branch.",
                    "En if-elif-else-kæde udfører højst én gren.",
                ),
            ),
            solution=_same("A"),
            explanation=_t(
                "value > 10 es True, por lo que se ejecuta la primera rama y las demás no se evalúan.",
                "value > 10 is True, so the first branch executes and the others are skipped.",
                "value > 10 er True, så den første gren udføres, og de øvrige springes over.",
            ),
        ),
        LocalizedPracticeExercise(
            exercise_id="m02.p02",
            activity_type=ActivityType.MATCHING,
            prompt=_t(
                "Relaciona and, or y not con su regla de verdad.",
                "Match and, or, and not with their truth rule.",
                "Match and, or og not med deres sandhedsregel.",
            ),
            hints=(
                _t(
                    "Distingue exigir todas las condiciones de exigir al menos una.",
                    "Distinguish requiring all conditions from requiring at least one.",
                    "Skeln mellem at kræve alle betingelser og mindst én.",
                ),
            ),
            solution=_t(
                "and → True solo si ambos operandos son True; or → True si al menos uno es True; not → invierte el valor booleano.",
                "and → True only if both operands are True; or → True if at least one is True; not → reverses the Boolean value.",
                "and → True kun hvis begge operander er True; or → True hvis mindst én er True; not → vender den booleske værdi.",
            ),
            explanation=_t(
                "Estas reglas permiten construir y comprobar condiciones compuestas mediante tablas de verdad.",
                "These rules support construction and verification of compound conditions with truth tables.",
                "Reglerne gør det muligt at opbygge og kontrollere sammensatte betingelser med sandhedstabeller.",
            ),
        ),
        LocalizedPracticeExercise(
            exercise_id="m02.p03",
            activity_type=ActivityType.CODE_COMPLETION,
            prompt=_t(
                "Completa la condición para aceptar valores entre 10 y 25, ambos incluidos.",
                "Complete the condition to accept values from 10 through 25 inclusive.",
                "Fuldfør betingelsen, så værdier fra 10 til og med 25 accepteres.",
            ),
            hints=(
                _t(
                    "Puedes usar una comparación encadenada.",
                    "You can use a chained comparison.",
                    "Du kan bruge en kædet sammenligning.",
                ),
                _t(
                    "Ambos límites son inclusivos.",
                    "Both boundaries are inclusive.",
                    "Begge grænser er inklusive.",
                ),
            ),
            starter_code=_same("value = 18\nif __________:\n    print('accepted')"),
            solution=_same("10 <= value <= 25"),
            explanation=_t(
                "Los operadores <= incluyen 10 y 25 y la forma encadenada expresa un único intervalo.",
                "The <= operators include 10 and 25, and the chained form expresses one interval.",
                "Operatorerne <= inkluderer 10 og 25, og den kædede form udtrykker ét interval.",
            ),
        ),
        LocalizedPracticeExercise(
            exercise_id="m02.p04",
            activity_type=ActivityType.DEBUGGING,
            prompt=_t(
                "Corrige el error y explica su causa:\nstatus = 'ready'\nif status = 'ready':\n    print('start')",
                "Correct the error and explain its cause:\nstatus = 'ready'\nif status = 'ready':\n    print('start')",
                "Ret fejlen og forklar årsagen:\nstatus = 'ready'\nif status = 'ready':\n    print('start')",
            ),
            hints=(
                _t(
                    "Distingue asignación de comparación de igualdad.",
                    "Distinguish assignment from equality comparison.",
                    "Skeln mellem tildeling og lighedssammenligning.",
                ),
            ),
            solution=_same("status = 'ready'\nif status == 'ready':\n    print('start')"),
            explanation=_t(
                "Dentro de la condición se necesita ==. Usar = en esa posición produce SyntaxError.",
                "The condition requires ==. Using = in that position causes SyntaxError.",
                "Betingelsen kræver ==. Brug af = på denne placering giver SyntaxError.",
            ),
        ),
        LocalizedPracticeExercise(
            exercise_id="m02.p05",
            activity_type=ActivityType.CODE_TRACING,
            prompt=_t(
                "Determina el valor de result sin ejecutar el código:\nx = 0\ny = 8\nresult = x != 0 and y / x > 2",
                "Determine result without executing the code:\nx = 0\ny = 8\nresult = x != 0 and y / x > 2",
                "Bestem result uden at køre koden:\nx = 0\ny = 8\nresult = x != 0 and y / x > 2",
            ),
            hints=(
                _t("Evalúa primero x != 0.", "Evaluate x != 0 first.", "Evaluér først x != 0."),
                _t(
                    "Recuerda el cortocircuito de and.",
                    "Remember short-circuiting for and.",
                    "Husk kortslutning for and.",
                ),
            ),
            solution=_same("False"),
            explanation=_t(
                "x != 0 es False, por lo que y / x no se evalúa y no aparece ZeroDivisionError.",
                "x != 0 is False, so y / x is not evaluated and no ZeroDivisionError occurs.",
                "x != 0 er False, så y / x evalueres ikke, og ZeroDivisionError opstår ikke.",
            ),
        ),
        LocalizedPracticeExercise(
            exercise_id="m02.p06",
            activity_type=ActivityType.SHORT_ANSWER,
            prompt=_t(
                "Explica por qué score >= 90 debe comprobarse antes que score >= 60 en una clasificación con if y elif.",
                "Explain why score >= 90 should be checked before score >= 60 in an if-elif classification.",
                "Forklar, hvorfor score >= 90 bør kontrolleres før score >= 60 i en if-elif-klassifikation.",
            ),
            hints=(
                _t(
                    "Piensa qué condiciones son verdaderas cuando score vale 95.",
                    "Consider which conditions are true when score is 95.",
                    "Overvej hvilke betingelser der er sande, når score er 95.",
                ),
            ),
            solution=_t(
                "Un valor de 95 cumple ambas condiciones. Como se ejecuta la primera rama verdadera, la condición más específica score >= 90 debe aparecer primero para no quedar absorbida por score >= 60.",
                "A value of 95 satisfies both conditions. Because the first true branch executes, the more specific score >= 90 condition must come first so it is not absorbed by score >= 60.",
                "Værdien 95 opfylder begge betingelser. Da den første sande gren udføres, skal den mere specifikke betingelse score >= 90 stå først, så den ikke opsluges af score >= 60.",
            ),
            explanation=_t(
                "Cuando las condiciones se solapan, el orden forma parte de la lógica del programa.",
                "When conditions overlap, their order is part of program logic.",
                "Når betingelser overlapper, er rækkefølgen en del af programmets logik.",
            ),
        ),
        LocalizedPracticeExercise(
            exercise_id="m02.p07",
            activity_type=ActivityType.FILL_IN_THE_BLANK,
            prompt=_t(
                "Completa: la precedencia de mayor a menor es ____ , ____ , ____ para los operadores lógicos de Python.",
                "Complete: from highest to lowest, Python logical-operator precedence is ____ , ____ , ____.",
                "Fuldfør: Fra højeste til laveste er præcedensen for Pythons logiske operatorer ____ , ____ , ____.",
            ),
            hints=(
                _t(
                    "La negación se evalúa antes que las combinaciones.",
                    "Negation is evaluated before combinations.",
                    "Negation evalueres før kombinationer.",
                ),
            ),
            solution=_same("not, and, or"),
            explanation=_t(
                "not tiene mayor precedencia, después and y finalmente or.",
                "not has the highest precedence, followed by and, then or.",
                "not har højeste præcedens, derefter and og til sidst or.",
            ),
        ),
        LocalizedPracticeExercise(
            exercise_id="m02.p08",
            activity_type=ActivityType.CODE_COMPLETION,
            prompt=_t(
                "Completa una validación que marque como inválido cualquier porcentaje menor que 0 o mayor que 100.",
                "Complete validation that marks any percentage below 0 or above 100 as invalid.",
                "Fuldfør en validering, der markerer enhver procent under 0 eller over 100 som ugyldig.",
            ),
            hints=(
                _t(
                    "Los dos casos inválidos se combinan con or.",
                    "The two invalid cases are combined with or.",
                    "De to ugyldige tilfælde kombineres med or.",
                ),
            ),
            starter_code=_same(
                "percentage = 112\nif __________________________:\n    print('invalid')"
            ),
            solution=_same("percentage < 0 or percentage > 100"),
            explanation=_t(
                "Basta con que se cumpla uno de los dos extremos inválidos para rechazar la entrada.",
                "Either invalid extreme is sufficient to reject the input.",
                "Det er tilstrækkeligt, at én af de to ugyldige ydergrænser er opfyldt, for at afvise inputtet.",
            ),
        ),
        LocalizedPracticeExercise(
            exercise_id="m02.p09",
            activity_type=ActivityType.ORAL_EXPLANATION,
            prompt=_t(
                "Explica oralmente la diferencia entre una condición compuesta y un condicional anidado. Incluye un ejemplo en el que el anidamiento sea justificable.",
                "Explain orally the difference between a compound condition and a nested conditional. Include one case where nesting is justified.",
                "Forklar mundtligt forskellen mellem en sammensat betingelse og en indlejret betingelse. Medtag et tilfælde, hvor indlejring er begrundet.",
            ),
            hints=(
                _t(
                    "Relaciona la forma del código con decisiones simultáneas o por etapas.",
                    "Relate code form to simultaneous or staged decisions.",
                    "Knyt kodens form til samtidige beslutninger eller beslutninger i trin.",
                ),
            ),
            solution=_t(
                "Una condición compuesta decide con varios requisitos a la vez. Un condicional anidado expresa que una segunda decisión solo se considera después de superar la primera, por ejemplo validar que un dato exista antes de clasificar su valor.",
                "A compound condition decides using several requirements at once. A nested conditional expresses that a second decision is considered only after the first succeeds, for example checking that data exist before classifying their value.",
                "En sammensat betingelse træffer en beslutning ud fra flere krav på én gang. En indlejret betingelse udtrykker, at en anden beslutning først overvejes efter den første, eksempelvis at data findes, før deres værdi klassificeres.",
            ),
            explanation=_t(
                "La respuesta debe justificar la estructura, no limitarse a describir la indentación.",
                "The answer should justify the structure, not merely describe indentation.",
                "Svaret bør begrunde strukturen og ikke kun beskrive indrykningen.",
            ),
        ),
        LocalizedPracticeExercise(
            exercise_id="m02.p10",
            activity_type=ActivityType.SHORT_ANSWER,
            prompt=_t(
                "Propón un conjunto mínimo de pruebas para una regla con tres ramas: x < 10, 10 <= x <= 20 y x > 20.",
                "Propose a minimal test set for three branches: x < 10, 10 <= x <= 20, and x > 20.",
                "Foreslå et minimalt testsæt til tre grene: x < 10, 10 <= x <= 20 og x > 20.",
            ),
            hints=(
                _t(
                    "Incluye cada rama y los dos límites.",
                    "Include every branch and both boundaries.",
                    "Medtag hver gren og begge grænser.",
                ),
                _t(
                    "Los valores justo a ambos lados revelan errores con < y <=.",
                    "Values immediately on either side expose < versus <= errors.",
                    "Værdier lige på begge sider afslører fejl mellem < og <=.",
                ),
            ),
            solution=_t(
                "Un conjunto sólido es 9, 10, 20 y 21. Activa las tres ramas y comprueba ambos límites y sus lados inmediatos.",
                "A strong set is 9, 10, 20, and 21. It activates all three branches and checks both boundaries and their immediate sides.",
                "Et stærkt sæt er 9, 10, 20 og 21. Det aktiverer alle tre grene og kontrollerer begge grænser og deres nærmeste sider.",
            ),
            explanation=_t(
                "Tres valores podrían activar las ramas, pero cuatro permiten verificar explícitamente las dos fronteras.",
                "Three values could activate the branches, but four explicitly verify both boundaries.",
                "Tre værdier kunne aktivere grenene, men fire verificerer eksplicit begge grænser.",
            ),
        ),
    ),
    assessment_items=(
        LocalizedAssessmentItem(
            item_id="m02.a01",
            activity_type=ActivityType.MULTIPLE_CHOICE,
            prompt=_t(
                "¿Cuál es el tipo de True?", "What is the type of True?", "Hvilken type har True?"
            ),
            options=(
                _option("bool", "bool", "bool", "bool"),
                _option("str", "str", "str", "str"),
                _option("int", "int", "int", "int"),
                _option("none", "NoneType", "NoneType", "NoneType"),
            ),
            correct_option_ids=("bool",),
            accepted_answers=(),
            explanation=_t(
                "True y False son los dos valores del tipo bool.",
                "True and False are the two bool values.",
                "True og False er de to værdier af typen bool.",
            ),
        ),
        LocalizedAssessmentItem(
            item_id="m02.a02",
            activity_type=ActivityType.TRUE_FALSE,
            prompt=_t(
                "El operador = compara si dos valores son iguales.",
                "The = operator compares two values for equality.",
                "Operatoren = sammenligner to værdier for lighed.",
            ),
            options=(
                _option("true", "Verdadero", "True", "Sandt"),
                _option("false", "Falso", "False", "Falsk"),
            ),
            correct_option_ids=("false",),
            accepted_answers=(),
            explanation=_t(
                "= asigna; == compara igualdad.",
                "= assigns; == compares equality.",
                "= tildeler; == sammenligner lighed.",
            ),
        ),
        LocalizedAssessmentItem(
            item_id="m02.a03",
            activity_type=ActivityType.MULTIPLE_SELECT,
            prompt=_t(
                "Selecciona todas las expresiones que producen True cuando x = 8.",
                "Select every expression that is True when x = 8.",
                "Vælg alle udtryk, der er True, når x = 8.",
            ),
            options=(
                _option("gt5", "x > 5", "x > 5", "x > 5"),
                _option("range", "5 <= x <= 8", "5 <= x <= 8", "5 <= x <= 8"),
                _option("eq7", "x == 7", "x == 7", "x == 7"),
                _option("neq8", "x != 8", "x != 8", "x != 8"),
            ),
            correct_option_ids=("gt5", "range"),
            accepted_answers=(),
            explanation=_t(
                "8 es mayor que 5 y pertenece al intervalo cerrado [5, 8].",
                "8 is greater than 5 and belongs to the closed interval [5, 8].",
                "8 er større end 5 og tilhører det lukkede interval [5, 8].",
            ),
        ),
        LocalizedAssessmentItem(
            item_id="m02.a04",
            activity_type=ActivityType.CODE_TRACING,
            prompt=_t(
                "Indica la salida exacta:\nx = 4\nif x > 5:\n    print('high')\nelse:\n    print('low')",
                "Give the exact output:\nx = 4\nif x > 5:\n    print('high')\nelse:\n    print('low')",
                "Angiv det præcise output:\nx = 4\nif x > 5:\n    print('high')\nelse:\n    print('low')",
            ),
            options=(),
            correct_option_ids=(),
            accepted_answers=(_same("low"),),
            explanation=_t(
                "x > 5 es False, por lo que se ejecuta else.",
                "x > 5 is False, so else executes.",
                "x > 5 er False, så else udføres.",
            ),
            rubric=(
                _t("Indica exactamente low.", "States exactly low.", "Angiver præcist low."),
                _t(
                    "Relaciona la salida con la condición falsa.",
                    "Links the output to the false condition.",
                    "Knytter outputtet til den falske betingelse.",
                ),
            ),
        ),
        LocalizedAssessmentItem(
            item_id="m02.a05",
            activity_type=ActivityType.FILL_IN_THE_BLANK,
            prompt=_t(
                "Completa el operador para expresar 'distinto de': x ____ 0.",
                "Complete the operator for 'not equal to': x ____ 0.",
                "Fuldfør operatoren for 'ikke lig med': x ____ 0.",
            ),
            options=(),
            correct_option_ids=(),
            accepted_answers=(_same("!="),),
            explanation=_t(
                "!= compara desigualdad.", "!= compares inequality.", "!= sammenligner ulighed."
            ),
        ),
        LocalizedAssessmentItem(
            item_id="m02.a06",
            activity_type=ActivityType.DEBUGGING,
            prompt=_t(
                "Corrige la condición para evitar dividir por cero: ratio = total / count if total / count > 2 else 0, suponiendo que se debe usar una estructura if normal.",
                "Correct the condition to avoid division by zero: ratio = total / count if total / count > 2 else 0, assuming a normal if statement should be used.",
                "Ret betingelsen for at undgå division med nul: ratio = total / count if total / count > 2 else 0, idet der skal bruges en almindelig if-sætning.",
            ),
            options=(),
            correct_option_ids=(),
            accepted_answers=(
                _same(
                    "if count != 0 and total / count > 2:\n    ratio = total / count\nelse:\n    ratio = 0"
                ),
            ),
            explanation=_t(
                "La comprobación count != 0 debe evaluarse antes de la división.",
                "count != 0 must be evaluated before division.",
                "count != 0 skal evalueres før divisionen.",
            ),
            rubric=(
                _t(
                    "Comprueba count != 0 antes de dividir.",
                    "Checks count != 0 before division.",
                    "Kontrollerer count != 0 før division.",
                ),
                _t(
                    "Conserva una rama alternativa definida.",
                    "Keeps a defined alternative branch.",
                    "Bevarer en defineret alternativ gren.",
                ),
                _t(
                    "Explica el papel del cortocircuito.",
                    "Explains the role of short-circuiting.",
                    "Forklarer kortslutningens rolle.",
                ),
            ),
        ),
        LocalizedAssessmentItem(
            item_id="m02.a07",
            activity_type=ActivityType.ORDERING,
            prompt=_t(
                "Ordena las comprobaciones para procesar una entrada de forma segura.",
                "Order the checks for safe input processing.",
                "Sæt kontrollerne i rækkefølge for sikker behandling af input.",
            ),
            options=(
                _option(
                    "parse",
                    "Convertir la representación al tipo requerido",
                    "Convert the representation to the required type",
                    "Konvertér repræsentationen til den krævede type",
                ),
                _option(
                    "validate",
                    "Validar el dominio permitido",
                    "Validate the allowed domain",
                    "Validér det tilladte domæne",
                ),
                _option(
                    "classify",
                    "Aplicar la clasificación",
                    "Apply the classification",
                    "Anvend klassifikationen",
                ),
                _option("report", "Mostrar el resultado", "Report the result", "Vis resultatet"),
            ),
            correct_option_ids=("parse", "validate", "classify", "report"),
            accepted_answers=(),
            explanation=_t(
                "Primero se obtiene un valor utilizable, después se valida, se clasifica y se comunica.",
                "First obtain a usable value, then validate, classify, and report it.",
                "Først opnås en anvendelig værdi, derefter valideres, klassificeres og rapporteres den.",
            ),
        ),
        LocalizedAssessmentItem(
            item_id="m02.a08",
            activity_type=ActivityType.MATCHING,
            prompt=_t(
                "Relaciona cada operador con su función.",
                "Match each operator with its function.",
                "Match hver operator med dens funktion.",
            ),
            options=(
                _option(
                    "and",
                    "and → exige ambas condiciones",
                    "and → requires both conditions",
                    "and → kræver begge betingelser",
                ),
                _option(
                    "or",
                    "or → exige al menos una condición",
                    "or → requires at least one condition",
                    "or → kræver mindst én betingelse",
                ),
                _option(
                    "not",
                    "not → invierte una condición",
                    "not → reverses a condition",
                    "not → vender en betingelse",
                ),
            ),
            correct_option_ids=("and", "or", "not"),
            accepted_answers=(),
            explanation=_t(
                "Las tres reglas corresponden a la semántica booleana de Python.",
                "The three rules are Python's Boolean semantics.",
                "De tre regler svarer til Pythons booleske semantik.",
            ),
        ),
        LocalizedAssessmentItem(
            item_id="m02.a09",
            activity_type=ActivityType.SHORT_ANSWER,
            prompt=_t(
                "Define qué significa que and se evalúe en cortocircuito.",
                "Define what it means for and to short-circuit.",
                "Definér, hvad det betyder, at and kortslutter.",
            ),
            options=(),
            correct_option_ids=(),
            accepted_answers=(
                _t(
                    "Si el primer operando es False, Python no evalúa el segundo porque el resultado total ya debe ser False.",
                    "If the first operand is False, Python does not evaluate the second because the complete result must already be False.",
                    "Hvis den første operand er False, evaluerer Python ikke den anden, fordi det samlede resultat allerede må være False.",
                ),
            ),
            explanation=_t(
                "El segundo operando solo se evalúa cuando el primero es verdadero.",
                "The second operand is evaluated only when the first is true.",
                "Den anden operand evalueres kun, når den første er sand.",
            ),
            rubric=(
                _t(
                    "Menciona la evaluación de izquierda a derecha.",
                    "Mentions left-to-right evaluation.",
                    "Nævner evaluering fra venstre mod højre.",
                ),
                _t(
                    "Indica que False en el primer operando detiene and.",
                    "States that False in the first operand stops and.",
                    "Angiver, at False i den første operand stopper and.",
                ),
                _t(
                    "Explica que el resultado ya está determinado.",
                    "Explains that the result is already determined.",
                    "Forklarer, at resultatet allerede er bestemt.",
                ),
            ),
        ),
        LocalizedAssessmentItem(
            item_id="m02.a10",
            activity_type=ActivityType.CODE_COMPLETION,
            prompt=_t(
                "Completa la condición: una muestra se revisa si concentration < 20 o purity no está entre 1.8 y 2.1.",
                "Complete the condition: a sample is reviewed if concentration < 20 or purity is not between 1.8 and 2.1.",
                "Fuldfør betingelsen: En prøve gennemgås, hvis concentration < 20, eller purity ikke ligger mellem 1.8 og 2.1.",
            ),
            options=(),
            correct_option_ids=(),
            accepted_answers=(_same("concentration < 20 or not 1.8 <= purity <= 2.1"),),
            explanation=_t(
                "or combina cualquiera de los motivos de revisión y not niega el intervalo válido.",
                "or combines either review reason and not negates the valid interval.",
                "or kombinerer begge mulige årsager til gennemgang, og not benægter det gyldige interval.",
            ),
        ),
        LocalizedAssessmentItem(
            item_id="m02.a11",
            activity_type=ActivityType.DATA_INTERPRETATION,
            prompt=_t(
                "Una regla usa if x < 10, elif x <= 20 y else. ¿Qué rama recibe x = 20 y por qué?",
                "A rule uses if x < 10, elif x <= 20, and else. Which branch receives x = 20, and why?",
                "En regel bruger if x < 10, elif x <= 20 og else. Hvilken gren modtager x = 20, og hvorfor?",
            ),
            options=(),
            correct_option_ids=(),
            accepted_answers=(
                _t(
                    "La rama elif, porque 20 no es menor que 10 pero sí cumple x <= 20.",
                    "The elif branch, because 20 is not below 10 but does satisfy x <= 20.",
                    "elif-grenen, fordi 20 ikke er mindre end 10, men opfylder x <= 20.",
                ),
            ),
            explanation=_t(
                "El operador <= incluye el límite 20.",
                "The <= operator includes the boundary 20.",
                "Operatoren <= inkluderer grænsen 20.",
            ),
            rubric=(
                _t(
                    "Identifica la rama elif.",
                    "Identifies the elif branch.",
                    "Identificerer elif-grenen.",
                ),
                _t(
                    "Explica ambos resultados de comparación.",
                    "Explains both comparison results.",
                    "Forklarer begge sammenligningsresultater.",
                ),
            ),
        ),
        LocalizedAssessmentItem(
            item_id="m02.a12",
            activity_type=ActivityType.SHORT_ANSWER,
            prompt=_t(
                "Propón cuatro valores para probar los límites de 10 <= x <= 20.",
                "Propose four values to test the boundaries of 10 <= x <= 20.",
                "Foreslå fire værdier til at teste grænserne for 10 <= x <= 20.",
            ),
            options=(),
            correct_option_ids=(),
            accepted_answers=(_same("9, 10, 20, 21"),),
            explanation=_t(
                "El conjunto comprueba cada límite y el valor inmediatamente exterior.",
                "The set checks each boundary and the immediately external value.",
                "Sættet kontrollerer hver grænse og den umiddelbart ydre værdi.",
            ),
            rubric=(
                _t("Incluye 10 y 20.", "Includes 10 and 20.", "Inkluderer 10 og 20."),
                _t(
                    "Incluye un valor menor que 10 y otro mayor que 20.",
                    "Includes one value below 10 and one above 20.",
                    "Inkluderer én værdi under 10 og én over 20.",
                ),
            ),
        ),
    ),
    tutor_support=LocalizedTutorSupportPacket(
        canonical_explanation=_t(
            "Este módulo enseña a representar decisiones como lógica verificable. Una condición debe "
            "producir bool y describir una propiedad concreta del estado. Las comparaciones construyen "
            "predicados; and, or y not permiten combinarlos, y su precedencia debe interpretarse antes de "
            "predecir el resultado. La evaluación en cortocircuito hace que el orden de los operandos sea "
            "significativo: una condición guardián puede impedir una operación inválida. Las estructuras "
            "if, elif y else seleccionan la primera rama verdadera, por lo que el orden de condiciones "
            "solapadas forma parte del algoritmo. Los límites deben expresarse con operadores inclusivos o "
            "exclusivos de acuerdo con la especificación. La comprensión se demuestra trazando qué "
            "condiciones se evalúan, justificando qué rama se ejecuta y diseñando pruebas que activen cada "
            "rama y ambos lados de cada frontera. Los ejemplos biomédicos del módulo son escenarios "
            "didácticos y no reglas clínicas ni de laboratorio reales.",
            "This module teaches decisions as verifiable logic. A condition must produce bool and describe "
            "a concrete property of program state. Comparisons construct predicates; and, or, and not combine "
            "them, and their precedence must be understood before predicting results. Short-circuit evaluation "
            "makes operand order meaningful because a guard can prevent an invalid operation. if, elif, and "
            "else select the first true branch, so the order of overlapping conditions is part of the algorithm. "
            "Boundaries must use inclusive or exclusive operators according to the specification. Understanding "
            "is demonstrated by tracing which conditions are evaluated, justifying the executed branch, and "
            "designing tests that activate every branch and both sides of each boundary. Biomedical examples are "
            "teaching scenarios, not real clinical or laboratory rules.",
            "Dette modul lærer at repræsentere beslutninger som efterprøvelig logik. En betingelse skal give bool "
            "og beskrive en konkret egenskab ved programmets tilstand. Sammenligninger opbygger prædikater; and, "
            "or og not kombinerer dem, og deres præcedens skal forstås, før resultatet forudsiges. "
            "Kortslutningsevaluering gør operandernes rækkefølge betydningsfuld, fordi en beskyttelsesbetingelse "
            "kan forhindre en ugyldig operation. if, elif og else vælger den første sande gren, så rækkefølgen "
            "af overlappende betingelser er en del af algoritmen. Grænser skal udtrykkes med inklusive eller "
            "eksklusive operatorer i overensstemmelse med specifikationen. Forståelse vises ved at gennemgå, "
            "hvilke betingelser der evalueres, begrunde den udførte gren og designe test, der aktiverer hver gren "
            "og begge sider af hver grænse. De biomedicinske eksempler er undervisningsscenarier og ikke virkelige "
            "kliniske eller laboratoriemæssige regler.",
        ),
        knowledge_fragments=(
            _t(
                "True y False son valores de bool; 'True' y 'False' son cadenas.",
                "True and False are bool values; 'True' and 'False' are strings.",
                "True og False er bool-værdier; 'True' og 'False' er tekststrenge.",
            ),
            _t(
                "== comprueba igualdad y = realiza asignación.",
                "== checks equality and = performs assignment.",
                "== kontrollerer lighed, og = udfører tildeling.",
            ),
            _t(
                "Las comparaciones encadenadas expresan intervalos sin repetir la variable.",
                "Chained comparisons express intervals without repeating the variable.",
                "Kædede sammenligninger udtrykker intervaller uden at gentage variablen.",
            ),
            _t(
                "La precedencia lógica es not, and y or, de mayor a menor.",
                "Logical precedence is not, and, then or from highest to lowest.",
                "Den logiske præcedens er not, and og or fra højeste til laveste.",
            ),
            _t(
                "A and B no evalúa B cuando A es False.",
                "A and B does not evaluate B when A is False.",
                "A and B evaluerer ikke B, når A er False.",
            ),
            _t(
                "A or B no evalúa B cuando A es True.",
                "A or B does not evaluate B when A is True.",
                "A or B evaluerer ikke B, når A er True.",
            ),
            _t(
                "Una cadena if-elif-else ejecuta solo la primera rama verdadera.",
                "An if-elif-else chain executes only the first true branch.",
                "En if-elif-else-kæde udfører kun den første sande gren.",
            ),
            _t(
                "else cubre los casos no capturados por condiciones anteriores.",
                "else covers cases not captured by previous conditions.",
                "else dækker tilfælde, som tidligere betingelser ikke fangede.",
            ),
            _t(
                "Las condiciones más específicas suelen preceder a las más generales cuando se solapan.",
                "More specific conditions usually precede more general overlapping conditions.",
                "Mere specifikke betingelser står normalt før mere generelle overlappende betingelser.",
            ),
            _t(
                "Una condición guardián valida antes de ejecutar una operación sensible.",
                "A guard condition validates before a sensitive operation executes.",
                "En beskyttelsesbetingelse validerer, før en følsom operation udføres.",
            ),
            _t(
                "Los límites exactos revelan errores entre < y <= o entre > y >=.",
                "Exact boundaries expose mistakes between < and <= or > and >=.",
                "Præcise grænser afslører fejl mellem < og <= eller > og >=.",
            ),
            _t(
                "Una prueba de ramas necesita casos normales, límite e inválidos.",
                "Branch testing needs normal, boundary, and invalid cases.",
                "Test af grene kræver normale, grænse- og ugyldige tilfælde.",
            ),
        ),
        common_misconceptions=(
            _t(
                "Confundir bool con las cadenas 'True' y 'False'.",
                "Confusing bool with the strings 'True' and 'False'.",
                "At forveksle bool med tekststrengene 'True' og 'False'.",
            ),
            _t(
                "Usar = cuando se pretende comparar con ==.",
                "Using = when == is intended.",
                "At bruge =, når == er tilsigtet.",
            ),
            _t(
                "Suponer que elif se evalúa aunque if ya haya sido verdadero.",
                "Assuming elif is evaluated after a true if branch.",
                "At antage, at elif evalueres efter en sand if-gren.",
            ),
            _t(
                "Creer que and y or siempre evalúan ambos operandos.",
                "Believing and and or always evaluate both operands.",
                "At tro, at and og or altid evaluerer begge operander.",
            ),
            _t(
                "Colocar una división antes de la condición que debía protegerla.",
                "Placing division before the guard that should protect it.",
                "At placere divisionen før den betingelse, der skulle beskytte den.",
            ),
            _t(
                "Ignorar la precedencia al mezclar not, and y or.",
                "Ignoring precedence when mixing not, and, and or.",
                "At ignorere præcedens ved blanding af not, and og or.",
            ),
            _t(
                "Ordenar primero una condición general que absorbe una categoría específica.",
                "Placing a general condition before a specific category it absorbs.",
                "At placere en generel betingelse før en specifik kategori, som den opsluger.",
            ),
            _t(
                "Tratar todos los límites como exclusivos sin revisar la especificación.",
                "Treating all boundaries as exclusive without checking the specification.",
                "At behandle alle grænser som eksklusive uden at kontrollere specifikationen.",
            ),
            _t(
                "Usar anidamiento profundo cuando una condición compuesta sería más clara.",
                "Using deep nesting when a compound condition would be clearer.",
                "At bruge dyb indlejring, når en sammensat betingelse ville være tydeligere.",
            ),
            _t(
                "Probar solo un valor central y declarar correcta toda la clasificación.",
                "Testing one central value and declaring the whole classification correct.",
                "At teste én central værdi og erklære hele klassifikationen korrekt.",
            ),
        ),
        socratic_questions=(
            _t(
                "¿Qué afirmación concreta debe ser True para entrar en esta rama?",
                "What concrete claim must be True to enter this branch?",
                "Hvilken konkret påstand skal være True for at gå ind i denne gren?",
            ),
            _t(
                "¿Qué tipo y valor produce cada comparación por separado?",
                "What type and value does each comparison produce separately?",
                "Hvilken type og værdi giver hver sammenligning separat?",
            ),
            _t(
                "¿Qué operador lógico corresponde a exigir todos los requisitos?",
                "Which logical operator represents requiring every condition?",
                "Hvilken logisk operator svarer til at kræve alle betingelser?",
            ),
            _t(
                "¿Puede decidirse el resultado sin evaluar el segundo operando?",
                "Can the result be determined without evaluating the second operand?",
                "Kan resultatet bestemmes uden at evaluere den anden operand?",
            ),
            _t(
                "¿Qué rama se ejecuta primero cuando varias condiciones son verdaderas?",
                "Which branch executes first when several conditions are true?",
                "Hvilken gren udføres først, når flere betingelser er sande?",
            ),
            _t(
                "¿El valor límite pertenece o no a la categoría según la especificación?",
                "Does the boundary value belong to the category according to the specification?",
                "Tilhører grænseværdien kategorien ifølge specifikationen?",
            ),
            _t(
                "¿La segunda decisión tiene sentido si la primera validación falla?",
                "Does the second decision make sense if the first validation fails?",
                "Giver den anden beslutning mening, hvis den første validering fejler?",
            ),
            _t(
                "¿Puedes escribir una tabla con condición, resultado y rama ejecutada?",
                "Can you write a table with condition, result, and executed branch?",
                "Kan du skrive en tabel med betingelse, resultat og udført gren?",
            ),
            _t(
                "¿Qué valor activaría cada rama de forma inequívoca?",
                "Which value would unambiguously activate each branch?",
                "Hvilken værdi ville entydigt aktivere hver gren?",
            ),
            _t(
                "¿Qué prueba distingue < de <= en este límite?",
                "Which test distinguishes < from <= at this boundary?",
                "Hvilken test skelner mellem < og <= ved denne grænse?",
            ),
        ),
        grading_criteria=(
            _t(
                "Distingue valores booleanos de representaciones textuales.",
                "Distinguishes Boolean values from text representations.",
                "Skelner booleske værdier fra tekstrepræsentationer.",
            ),
            _t(
                "Predice correctamente comparaciones y operadores lógicos.",
                "Correctly predicts comparisons and logical operators.",
                "Forudsiger sammenligninger og logiske operatorer korrekt.",
            ),
            _t(
                "Explica la precedencia o usa paréntesis sin alterar el significado.",
                "Explains precedence or uses parentheses without changing meaning.",
                "Forklarer præcedens eller bruger parenteser uden at ændre betydningen.",
            ),
            _t(
                "Reconoce cuándo el cortocircuito evita evaluar una operación.",
                "Recognises when short-circuiting prevents an operation from being evaluated.",
                "Genkender, hvornår kortslutning forhindrer evaluering af en operation.",
            ),
            _t(
                "Justifica la rama ejecutada y el efecto del orden.",
                "Justifies the executed branch and the effect of order.",
                "Begrunder den udførte gren og rækkefølgens betydning.",
            ),
            _t(
                "Distingue condiciones compuestas de decisiones anidadas.",
                "Distinguishes compound conditions from nested decisions.",
                "Skelner sammensatte betingelser fra indlejrede beslutninger.",
            ),
            _t(
                "Usa operadores inclusivos o exclusivos de acuerdo con el problema.",
                "Uses inclusive or exclusive operators according to the problem.",
                "Bruger inklusive eller eksklusive operatorer i overensstemmelse med problemet.",
            ),
            _t(
                "Propone pruebas que cubren ramas y límites.",
                "Proposes tests that cover branches and boundaries.",
                "Foreslår test, der dækker grene og grænser.",
            ),
            _t(
                "Mantiene los ejemplos dentro del alcance de condicionales sin introducir bucles o funciones innecesarias.",
                "Keeps examples within conditional logic without unnecessary loops or functions.",
                "Holder eksempler inden for betinget logik uden unødvendige løkker eller funktioner.",
            ),
        ),
        response_constraints=(
            _t(
                "Responder primero con una pista cuando el estudiante esté resolviendo un ejercicio.",
                "Give a hint first when the learner is solving an exercise.",
                "Giv først et hint, når den studerende løser en øvelse.",
            ),
            _t(
                "No presentar umbrales didácticos como recomendaciones clínicas o de laboratorio.",
                "Do not present teaching thresholds as clinical or laboratory recommendations.",
                "Præsentér ikke undervisningsgrænser som kliniske eller laboratoriemæssige anbefalinger.",
            ),
            _t(
                "No introducir bucles, funciones avanzadas ni clases para resolver ejercicios del módulo.",
                "Do not introduce loops, advanced functions, or classes to solve module exercises.",
                "Indfør ikke løkker, avancerede funktioner eller klasser til moduløvelser.",
            ),
            _t(
                "Separar el valor de cada condición de la rama finalmente ejecutada.",
                "Separate each condition's value from the branch ultimately executed.",
                "Adskil værdien af hver betingelse fra den gren, der til sidst udføres.",
            ),
            _t(
                "Cuando haya cortocircuito, indicar explícitamente qué operando no se evalúa.",
                "When short-circuiting occurs, state explicitly which operand is not evaluated.",
                "Når kortslutning forekommer, angiv eksplicit hvilken operand der ikke evalueres.",
            ),
            _t(
                "No aceptar una clasificación sin revisar los valores límite.",
                "Do not accept a classification without checking boundary values.",
                "Acceptér ikke en klassifikation uden at kontrollere grænseværdier.",
            ),
            _t(
                "Mantener el código en Python válido y respetar la indentación.",
                "Keep code valid Python and preserve indentation.",
                "Hold koden som gyldig Python og bevar indrykningen.",
            ),
            _t(
                "Si falta información de la especificación, declarar la ambigüedad en lugar de inventar un límite.",
                "If the specification lacks information, state the ambiguity instead of inventing a boundary.",
                "Hvis specifikationen mangler information, angiv tvetydigheden i stedet for at opfinde en grænse.",
            ),
        ),
        source_basis=(
            "Official DM857 course description, SDU, active version approved in 2025.",
            "Think Python, third edition, sections on Boolean expressions, logical operators, and conditional execution.",
            "Introduction to Computation and Programming Using Python, third edition, chapters on branching programs and testing.",
        ),
    ),
)

MODULE_02_CONDITIONALS = LOCALIZED_MODULE_02_CONDITIONALS.materialize(AppLocale.SPANISH_SPAIN)

__all__ = ["LOCALIZED_MODULE_02_CONDITIONALS", "MODULE_02_CONDITIONALS"]
