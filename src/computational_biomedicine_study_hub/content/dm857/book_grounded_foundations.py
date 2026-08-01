"""Book-grounded extensions for DM857 foundations, conditionals, and iteration."""

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


def update_foundations_audit(
    audit: tuple[ModuleSourceAudit, ...],
) -> tuple[ModuleSourceAudit, ...]:
    """Mark M01-M03 reviewed only after their extensions are present."""
    findings = {
        "dm857.m01": (
            "Existing coverage of problem modelling, values, types, bindings, tracing, "
            "conversion, and error classes is consistent. Approximate floating-point "
            "representation and explicit rounding policy needed one focused treatment."
        ),
        "dm857.m02": (
            "Existing coverage of predicates, comparisons, Boolean operators, short-circuit "
            "evaluation, conditionals, validation, and branch testing is consistent. Branch "
            "ordering and shadowed branches needed one explicit diagnostic."
        ),
        "dm857.m03": (
            "Existing coverage of while, for, range, state transitions, progress measures, "
            "invariants, sentinels, nested loops, and testing is consistent. Numerical search "
            "with tolerance and interval shrinkage needed one integrative example."
        ),
    }
    changes = {
        "dm857.m01": (
            "Added an original floating-point and rounding explanation, deterministic example, "
            "interpretation exercise, and stable objective item."
        ),
        "dm857.m02": (
            "Added an original branch-ordering explanation, deterministic example, debugging "
            "exercise, and stable objective item."
        ),
        "dm857.m03": (
            "Added an original bisection-search explanation, deterministic example, completion "
            "exercise, and stable objective item."
        ),
    }

    updated: list[ModuleSourceAudit] = []
    for item in audit:
        if item.module_id in findings:
            updated.append(
                replace(
                    item,
                    state="consistent",
                    finding=findings[item.module_id],
                    implemented_change=changes[item.module_id],
                )
            )
        else:
            updated.append(item)
    return tuple(updated)


def _extend_foundations(module: LocalizedLearningModule) -> LocalizedLearningModule:
    """Add floating-point approximation and explicit rounding policy to M01."""
    extended = replace(
        module,
        objectives=module.objectives
        + (
            objective(
                "m01.bg.o1",
                (
                    "Distinguir representación numérica aproximada, formato y política de "
                    "redondeo.",
                    "Distinguish approximate numeric representation, formatting, and rounding "
                    "policy.",
                    "Skelne mellem tilnærmet talrepræsentation, formatering og "
                    "afrundingspolitik.",
                ),
            ),
        ),
        concepts=module.concepts
        + (
            concept(
                "floating-point-and-rounding-policy",
                (
                    "Coma flotante y política de redondeo",
                    "Floating point and rounding policy",
                    "Flydende tal og afrundingspolitik",
                ),
                (
                    "Muchos valores decimales no tienen una representación binaria finita. Por "
                    "eso una operación con float puede producir un valor interno muy próximo al "
                    "resultado matemático, pero no idéntico. El formato controla cómo se muestra "
                    "un número; no modifica necesariamente el valor almacenado. round aplica la "
                    "regla de Python para el empate y no debe asumirse que toda terminación en "
                    ".5 sube. En datos científicos debe declararse si se conserva precisión, se "
                    "redondea para presentación o se convierte a una unidad discreta.",
                    "Many decimal values do not have a finite binary representation. A float "
                    "operation can therefore produce an internal value very close to, but not "
                    "identical to, the mathematical result. Formatting controls display and "
                    "does not necessarily modify the stored value. round applies Python's tie "
                    "rule, so a value ending in .5 must not be assumed always to round upward. "
                    "Scientific code should state whether precision is retained, display is "
                    "rounded, or a discrete unit is being produced.",
                    "Mange decimaltal har ikke en endelig binær repræsentation. En beregning med "
                    "float kan derfor give en intern værdi, som ligger meget tæt på, men ikke er "
                    "identisk med, det matematiske resultat. Formatering styrer visningen og "
                    "ændrer ikke nødvendigvis den lagrede værdi. round anvender Pythons regel "
                    "ved lighed, så en værdi der ender på .5 ikke altid afrundes opad. "
                    "Videnskabelig kode bør angive, om præcision bevares, visningen afrundes, "
                    "eller der dannes en diskret enhed.",
                ),
                (
                    (
                        "float representa muchos decimales mediante aproximaciones binarias.",
                        "float represents many decimals with binary approximations.",
                        "float repræsenterer mange decimaltal med binære tilnærmelser.",
                    ),
                    (
                        "Formatear una salida no demuestra que el valor interno sea exacto.",
                        "Formatting output does not prove that the internal value is exact.",
                        "Formatering af output beviser ikke, at den interne værdi er eksakt.",
                    ),
                    (
                        "Python redondea empates al valor par representable más cercano.",
                        "Python rounds ties to the nearest representable even value.",
                        "Python afrunder lighed til den nærmeste repræsenterbare lige værdi.",
                    ),
                    (
                        "La política de redondeo debe derivarse del significado del dato.",
                        "Rounding policy must follow from the meaning of the data.",
                        "Afrundingspolitikken skal følge af dataenes betydning.",
                    ),
                ),
            ),
        ),
        worked_examples=module.worked_examples
        + (
            example(
                "m01.bg.e01",
                (
                    "Predecir redondeo y presentación decimal",
                    "Predict rounding and decimal presentation",
                    "Forudsig afrunding og decimalvisning",
                ),
                (
                    "Compara dos empates de redondeo y muestra una suma decimal con una cifra, "
                    "sin confundir presentación con exactitud interna.",
                    "Compare two rounding ties and display a decimal sum with one digit without "
                    "confusing presentation with internal exactness.",
                    "Sammenlign to afrundingsligheder og vis en decimalsum med ét ciffer uden "
                    "at forveksle visning med intern nøjagtighed.",
                ),
                (
                    (
                        "Predice cada resultado antes de ejecutar el código.",
                        "Predict every result before running the code.",
                        "Forudsig hvert resultat før koden køres.",
                    ),
                    (
                        "Separa la regla de round del formato aplicado a floating_sum.",
                        "Separate the round rule from the format applied to floating_sum.",
                        "Adskil reglen for round fra formatet anvendt på floating_sum.",
                    ),
                ),
                'print(round(18.5))\nprint(round(19.5))\n'
                'floating_sum = 0.1 + 0.2\nprint(f"{floating_sum:.1f}")',
                "18\n20\n0.3",
                (
                    "Los dos empates terminan en enteros pares distintos. La última línea muestra "
                    "0.3 por formato, aunque la representación interna de la suma puede contener "
                    "más cifras.",
                    "The two ties end at different even integers. The final line displays 0.3 "
                    "because of formatting, although the internal sum can contain more digits.",
                    "De to ligheder ender ved forskellige lige heltal. Den sidste linje viser "
                    "0.3 på grund af formatering, selv om den interne sum kan indeholde flere "
                    "cifre.",
                ),
            ),
        ),
        practice_exercises=module.practice_exercises
        + (
            practice(
                "m01.bg.p01",
                ActivityType.DATA_INTERPRETATION,
                (
                    "Predice round(24.5), round(25.5) y 0.1 + 0.2. Explica qué parte es una "
                    "regla de redondeo y qué parte es representación aproximada.",
                    "Predict round(24.5), round(25.5), and 0.1 + 0.2. Explain which part is a "
                    "rounding rule and which part is approximate representation.",
                    "Forudsig round(24.5), round(25.5) og 0.1 + 0.2. Forklar hvilken del der er "
                    "en afrundingsregel, og hvilken del der er tilnærmet repræsentation.",
                ),
                (
                    (
                        "Observa la paridad de los enteros vecinos en los dos empates.",
                        "Inspect the parity of the neighbouring integers in both ties.",
                        "Undersøg pariteten af de tilstødende heltal i begge ligheder.",
                    ),
                    (
                        "No uses el texto mostrado como prueba de exactitud interna.",
                        "Do not use displayed text as proof of internal exactness.",
                        "Brug ikke den viste tekst som bevis for intern nøjagtighed.",
                    ),
                ),
                (
                    "Los resultados son 24, 26 y aproximadamente 0.30000000000000004. Los dos "
                    "primeros siguen la regla de empate al par; el tercero deriva de la "
                    "representación binaria aproximada.",
                    "The results are 24, 26, and approximately 0.30000000000000004. The first "
                    "two follow tie-to-even; the third comes from approximate binary "
                    "representation.",
                    "Resultaterne er 24, 26 og omtrent 0.30000000000000004. De to første følger "
                    "afrunding til lige; det tredje skyldes tilnærmet binær repræsentation.",
                ),
                (
                    "Una respuesta completa predice valores y distingue mecanismo de redondeo, "
                    "representación y formato.",
                    "A complete answer predicts values and distinguishes rounding mechanism, "
                    "representation, and formatting.",
                    "Et fuldstændigt svar forudsiger værdier og skelner mellem afrunding, "
                    "repræsentation og formatering.",
                ),
                "print(round(24.5))\nprint(round(25.5))\nprint(0.1 + 0.2)",
            ),
        ),
        assessment_items=module.assessment_items
        + (
            objective_mcq(
                "dm857.m01.book.001",
                (
                    "¿Qué afirmación interpreta correctamente float y formato?",
                    "Which statement correctly interprets float and formatting?",
                    "Hvilket udsagn fortolker float og formatering korrekt?",
                ),
                (
                    (
                        "format_changes_storage",
                        (
                            "Mostrar una cifra decimal vuelve exacto el valor almacenado.",
                            "Displaying one decimal digit makes the stored value exact.",
                            "Visning af ét decimaltal gør den lagrede værdi eksakt.",
                        ),
                    ),
                    (
                        "approximate_and_explicit",
                        (
                            "Un float puede ser aproximado y la política de redondeo debe "
                            "declararse.",
                            "A float can be approximate and the rounding policy should be "
                            "stated.",
                            "Et float kan være tilnærmet, og afrundingspolitikken bør angives.",
                        ),
                    ),
                    (
                        "half_always_up",
                        (
                            "round siempre redondea los empates .5 hacia arriba.",
                            "round always rounds .5 ties upward.",
                            "round afrunder altid .5-ligheder opad.",
                        ),
                    ),
                ),
                "approximate_and_explicit",
                (
                    "La representación, el formato y la regla de redondeo son decisiones "
                    "diferentes.",
                    "Representation, formatting, and the rounding rule are different decisions.",
                    "Repræsentation, formatering og afrundingsregel er forskellige beslutninger.",
                ),
            ),
        ),
    )
    return _with_source_basis(
        extended,
        ("guttag-2021-ch01-03", "downey-2024-foundations"),
    )


def _extend_conditionals(module: LocalizedLearningModule) -> LocalizedLearningModule:
    """Add branch ordering and shadowed-branch analysis to M02."""
    extended = replace(
        module,
        objectives=module.objectives
        + (
            objective(
                "m02.bg.o1",
                (
                    "Ordenar ramas para conservar categorías y detectar condiciones "
                    "inalcanzables.",
                    "Order branches to preserve categories and detect unreachable conditions.",
                    "Ordne grene, så kategorier bevares, og utilgængelige betingelser opdages.",
                ),
            ),
        ),
        concepts=module.concepts
        + (
            concept(
                "branch-ordering-and-shadowing",
                (
                    "Orden de ramas y condiciones ocultas",
                    "Branch ordering and shadowed conditions",
                    "Grenrækkefølge og skjulte betingelser",
                ),
                (
                    "En cadena if-elif-else se ejecuta como máximo una rama: la primera condición "
                    "verdadera. Por eso el orden forma parte de la lógica. Si una condición amplia "
                    "aparece antes que otra más específica, puede absorber todos sus casos y "
                    "volver inalcanzable la rama posterior. En clasificaciones por umbrales suele "
                    "ser más claro ordenar de la condición más restrictiva a la más general y "
                    "comprobar cada frontera con ejemplos concretos.",
                    "An if-elif-else chain executes at most one branch: the first true condition. "
                    "Order is therefore part of the logic. If a broad condition appears before a "
                    "more specific one, it can absorb all of its cases and make the later branch "
                    "unreachable. Threshold classifications are often clearest when ordered from "
                    "the most restrictive condition to the most general, with every boundary "
                    "checked by concrete examples.",
                    "En if-elif-else-kæde udfører højst én gren: den første sande betingelse. "
                    "Rækkefølgen er derfor en del af logikken. Hvis en bred betingelse står før en "
                    "mere specifik, kan den opsluge alle dens tilfælde og gøre den senere gren "
                    "utilgængelig. Tærskelklassifikationer er ofte tydeligst fra den mest "
                    "restriktive betingelse til den mest generelle, med konkrete test af hver "
                    "grænse.",
                ),
                (
                    (
                        "Sólo se ejecuta la primera rama verdadera.",
                        "Only the first true branch executes.",
                        "Kun den første sande gren udføres.",
                    ),
                    (
                        "Una condición amplia puede ocultar una condición posterior.",
                        "A broad condition can shadow a later condition.",
                        "En bred betingelse kan skjule en senere betingelse.",
                    ),
                    (
                        "Los umbrales descendentes suelen preservar categorías anidadas.",
                        "Descending thresholds often preserve nested categories.",
                        "Faldende tærskler bevarer ofte indlejrede kategorier.",
                    ),
                    (
                        "Cada frontera debe probarse junto con valores a ambos lados.",
                        "Each boundary should be tested with values on both sides.",
                        "Hver grænse bør testes med værdier på begge sider.",
                    ),
                ),
            ),
        ),
        worked_examples=module.worked_examples
        + (
            example(
                "m02.bg.e01",
                (
                    "Clasificar un resultado sin ocultar la categoría superior",
                    "Classify a result without shadowing the highest category",
                    "Klassificér et resultat uden at skjule den højeste kategori",
                ),
                (
                    "Clasifica un indicador didáctico: al menos 95 es excelente, al menos 80 "
                    "es aceptable y el resto requiere revisión.",
                    "Classify a teaching indicator: at least 95 is excellent, at least 80 is "
                    "acceptable, and the remainder requires review.",
                    "Klassificér en undervisningsindikator: mindst 95 er fremragende, mindst 80 "
                    "er acceptabelt, og resten kræver gennemgang.",
                ),
                (
                    (
                        "La categoría más específica usa el umbral más alto.",
                        "The most specific category uses the highest threshold.",
                        "Den mest specifikke kategori bruger den højeste tærskel.",
                    ),
                    (
                        "Al colocarla primero, una puntuación de 97 no queda atrapada por >= 80.",
                        "Putting it first prevents a score of 97 from being captured by >= 80.",
                        "Når den står først, fanges en score på 97 ikke af >= 80.",
                    ),
                ),
                'score = 97\nif score >= 95:\n    label = "excellent"\n'
                'elif score >= 80:\n    label = "acceptable"\n'
                'else:\n    label = "review"\nprint(label)',
                "excellent",
                (
                    "El orden descendente conserva las tres categorías. Invertir los dos primeros "
                    "umbrales haría inalcanzable la categoría excellent.",
                    "Descending order preserves all three categories. Reversing the first two "
                    "thresholds would make excellent unreachable.",
                    "Faldende rækkefølge bevarer alle tre kategorier. Hvis de to første tærskler "
                    "byttes, bliver excellent utilgængelig.",
                ),
            ),
        ),
        practice_exercises=module.practice_exercises
        + (
            practice(
                "m02.bg.p01",
                ActivityType.DEBUGGING,
                (
                    "El código clasifica 98 como acceptable porque comprueba score >= 80 antes "
                    "de score >= 95. Reconstruye el fallo y corrige el orden sin cambiar los "
                    "umbrales.",
                    "The code classifies 98 as acceptable because it checks score >= 80 before "
                    "score >= 95. Reconstruct the failure and fix the order without changing the "
                    "thresholds.",
                    "Koden klassificerer 98 som acceptable, fordi den kontrollerer score >= 80 "
                    "før score >= 95. Rekonstruér fejlen og ret rækkefølgen uden at ændre "
                    "tærsklerne.",
                ),
                (
                    (
                        "Pregunta qué rama verdadera se encuentra primero.",
                        "Ask which true branch is encountered first.",
                        "Spørg hvilken sand gren der mødes først.",
                    ),
                    (
                        "Ordena desde el caso más específico al más general.",
                        "Order from the most specific case to the most general.",
                        "Ordne fra det mest specifikke tilfælde til det mest generelle.",
                    ),
                ),
                (
                    "Coloca if score >= 95 antes de elif score >= 80. La condición >= 80 contiene "
                    "también los valores de la categoría superior y por eso no puede ir primero.",
                    "Place if score >= 95 before elif score >= 80. The >= 80 condition also "
                    "contains the higher category values and therefore cannot come first.",
                    "Placér if score >= 95 før elif score >= 80. Betingelsen >= 80 indeholder "
                    "også værdierne i den højere kategori og kan derfor ikke stå først.",
                ),
                (
                    "El defecto no está en los operadores, sino en la prioridad impuesta por la "
                    "cadena de control.",
                    "The defect is not in the operators but in the priority imposed by the "
                    "control-flow chain.",
                    "Fejlen ligger ikke i operatorerne, men i den prioritet som kontrolkæden "
                    "påtvinger.",
                ),
                'score = 98\nif score >= 80:\n    label = "acceptable"\n'
                'elif score >= 95:\n    label = "excellent"\n'
                'else:\n    label = "review"',
            ),
        ),
        assessment_items=module.assessment_items
        + (
            objective_mcq(
                "dm857.m02.book.001",
                (
                    "¿Qué orden mantiene accesibles las tres categorías?",
                    "Which order keeps all three categories reachable?",
                    "Hvilken rækkefølge holder alle tre kategorier tilgængelige?",
                ),
                (
                    (
                        "ascending",
                        (
                            "Primero score >= 80, después score >= 95 y finalmente else.",
                            "First score >= 80, then score >= 95, and finally else.",
                            "Først score >= 80, derefter score >= 95 og til sidst else.",
                        ),
                    ),
                    (
                        "descending",
                        (
                            "Primero score >= 95, después score >= 80 y finalmente else.",
                            "First score >= 95, then score >= 80, and finally else.",
                            "Først score >= 95, derefter score >= 80 og til sidst else.",
                        ),
                    ),
                    (
                        "duplicate",
                        (
                            "Usar score >= 80 en ambas ramas.",
                            "Use score >= 80 in both branches.",
                            "Brug score >= 80 i begge grene.",
                        ),
                    ),
                ),
                "descending",
                (
                    "La primera condición verdadera termina la cadena; el caso específico debe "
                    "aparecer antes que el caso que lo contiene.",
                    "The first true condition ends the chain; the specific case must appear before "
                    "the broader case that contains it.",
                    "Den første sande betingelse afslutter kæden; det specifikke tilfælde skal stå "
                    "før det bredere tilfælde, som indeholder det.",
                ),
            ),
        ),
    )
    return _with_source_basis(
        extended,
        ("guttag-2021-ch01-03", "downey-2024-foundations"),
    )


def _extend_iteration(module: LocalizedLearningModule) -> LocalizedLearningModule:
    """Add tolerance-based bisection search to M03."""
    extended = replace(
        module,
        objectives=module.objectives
        + (
            objective(
                "m03.bg.o1",
                (
                    "Diseñar una búsqueda iterativa con intervalo, tolerancia y criterio de "
                    "parada verificable.",
                    "Design an iterative search with an interval, tolerance, and verifiable "
                    "stopping rule.",
                    "Designe en iterativ søgning med interval, tolerance og efterprøvelig "
                    "stopregel.",
                ),
            ),
        ),
        concepts=module.concepts
        + (
            concept(
                "bisection-search-and-tolerance",
                (
                    "Búsqueda por bisección y tolerancia",
                    "Bisection search and tolerance",
                    "Bisektionssøgning og tolerance",
                ),
                (
                    "Una búsqueda numérica iterativa mantiene un intervalo que contiene una "
                    "solución posible y lo reduce en cada paso. En bisección se prueba el punto "
                    "medio y se descarta la mitad incompatible con el objetivo. La tolerancia "
                    "define cuándo una aproximación es suficientemente cercana; no es lo mismo "
                    "que igualdad exacta. Para justificar el algoritmo deben explicarse el "
                    "invariante del intervalo, la reducción de su anchura y la condición que "
                    "detiene el bucle.",
                    "An iterative numerical search maintains an interval containing a possible "
                    "solution and reduces it at every step. Bisection tests the midpoint and "
                    "discards the half incompatible with the target. Tolerance defines when an "
                    "approximation is close enough and is not the same as exact equality. The "
                    "algorithm should be justified through the interval invariant, shrinking "
                    "width, and the condition that stops the loop.",
                    "En iterativ numerisk søgning vedligeholder et interval, som indeholder en "
                    "mulig løsning, og reducerer det ved hvert trin. Bisektion tester midtpunktet "
                    "og forkaster den halvdel, der ikke passer til målet. Tolerancen definerer, "
                    "hvornår en tilnærmelse er tæt nok, og er ikke det samme som eksakt lighed. "
                    "Algoritmen bør begrundes med intervalinvarianten, den faldende bredde og "
                    "betingelsen, der stopper løkken.",
                ),
                (
                    (
                        "El intervalo debe conservar una solución posible.",
                        "The interval must retain a possible solution.",
                        "Intervallet skal bevare en mulig løsning.",
                    ),
                    (
                        "Cada actualización debe reducir el intervalo.",
                        "Every update must shrink the interval.",
                        "Hver opdatering skal mindske intervallet.",
                    ),
                    (
                        "epsilon expresa precisión requerida, no igualdad matemática.",
                        "epsilon expresses required precision, not mathematical equality.",
                        "epsilon udtrykker krævet præcision, ikke matematisk lighed.",
                    ),
                    (
                        "Un criterio de parada debe ser medible y alcanzable.",
                        "A stopping rule must be measurable and reachable.",
                        "En stopregel skal være målbar og opnåelig.",
                    ),
                ),
            ),
        ),
        worked_examples=module.worked_examples
        + (
            example(
                "m03.bg.e01",
                (
                    "Aproximar una raíz cuadrada por bisección",
                    "Approximate a square root by bisection",
                    "Tilnærm en kvadratrod med bisektion",
                ),
                (
                    "Aproxima la raíz cuadrada de 2 hasta que el error en el cuadrado sea menor "
                    "que 0.001 y registra cuántas actualizaciones se realizan.",
                    "Approximate the square root of 2 until the squared error is below 0.001 and "
                    "record how many updates are performed.",
                    "Tilnærm kvadratroden af 2, indtil fejlen i kvadratet er under 0.001, og "
                    "registrér antallet af opdateringer.",
                ),
                (
                    (
                        "Inicia un intervalo [0, 2] que contiene la raíz.",
                        "Start with an interval [0, 2] containing the root.",
                        "Start med et interval [0, 2], som indeholder roden.",
                    ),
                    (
                        "Conserva la mitad compatible con el signo del error.",
                        "Keep the half compatible with the sign of the error.",
                        "Bevar den halvdel, der passer til fejlens fortegn.",
                    ),
                    (
                        "Detén el bucle cuando el error absoluto sea menor que epsilon.",
                        "Stop when the absolute error is smaller than epsilon.",
                        "Stop når den absolutte fejl er mindre end epsilon.",
                    ),
                ),
                "target = 2.0\nepsilon = 0.001\nlow = 0.0\nhigh = target\n"
                "guess = (low + high) / 2\nsteps = 0\n"
                "while abs(guess**2 - target) >= epsilon:\n"
                "    if guess**2 < target:\n        low = guess\n"
                "    else:\n        high = guess\n"
                "    guess = (low + high) / 2\n    steps += 1\n"
                "print(round(guess, 4))\nprint(steps)",
                "1.4141\n7",
                (
                    "El intervalo se reduce a la mitad en cada actualización. El resultado no "
                    "afirma igualdad exacta: satisface el criterio de error elegido.",
                    "The interval halves on every update. The result does not claim exact "
                    "equality; it satisfies the chosen error criterion.",
                    "Intervallet halveres ved hver opdatering. Resultatet hævder ikke eksakt "
                    "lighed; det opfylder det valgte fejlkriterium.",
                ),
            ),
        ),
        practice_exercises=module.practice_exercises
        + (
            practice(
                "m03.bg.p01",
                ActivityType.CODE_COMPLETION,
                (
                    "Completa las dos actualizaciones de límites para aproximar la raíz cuadrada "
                    "de 10 por bisección. Explica por qué ambas reducen el intervalo.",
                    "Complete the two bound updates used to approximate the square root of 10 by "
                    "bisection. Explain why both shrink the interval.",
                    "Udfyld de to grænseopdateringer, der tilnærmer kvadratroden af 10 med "
                    "bisektion. Forklar hvorfor begge mindsker intervallet.",
                ),
                (
                    (
                        "Si guess**2 es demasiado pequeño, la raíz queda a la derecha.",
                        "If guess**2 is too small, the root remains to the right.",
                        "Hvis guess**2 er for lille, ligger roden til højre.",
                    ),
                    (
                        "Si guess**2 es demasiado grande, la raíz queda a la izquierda.",
                        "If guess**2 is too large, the root remains to the left.",
                        "Hvis guess**2 er for stor, ligger roden til venstre.",
                    ),
                ),
                (
                    "Usa low = guess en la primera rama y high = guess en la segunda. En ambos "
                    "casos se conserva la mitad que todavía puede contener la raíz.",
                    "Use low = guess in the first branch and high = guess in the second. In both "
                    "cases, retain the half that can still contain the root.",
                    "Brug low = guess i den første gren og high = guess i den anden. I begge "
                    "tilfælde bevares den halvdel, der stadig kan indeholde roden.",
                ),
                (
                    "La respuesta debe relacionar cada actualización con el invariante del "
                    "intervalo, no sólo completar la sintaxis.",
                    "The answer should connect each update to the interval invariant, not merely "
                    "complete the syntax.",
                    "Svaret bør knytte hver opdatering til intervalinvarianten og ikke blot "
                    "udfylde syntaksen.",
                ),
                "target = 10.0\nepsilon = 0.01\nlow = 0.0\nhigh = target\n"
                "guess = (low + high) / 2\n"
                "while abs(guess**2 - target) >= epsilon:\n"
                "    if guess**2 < target:\n        # update low\n"
                "    else:\n        # update high\n"
                "    guess = (low + high) / 2",
            ),
        ),
        assessment_items=module.assessment_items
        + (
            objective_mcq(
                "dm857.m03.book.001",
                (
                    "¿Qué propiedad explica el progreso de la bisección?",
                    "Which property explains the progress of bisection?",
                    "Hvilken egenskab forklarer fremdriften i bisektion?",
                ),
                (
                    (
                        "same_interval",
                        (
                            "El intervalo conserva siempre la misma anchura.",
                            "The interval always keeps the same width.",
                            "Intervallet beholder altid samme bredde.",
                        ),
                    ),
                    (
                        "shrinking_interval",
                        (
                            "Cada paso conserva una mitad posible y reduce la anchura.",
                            "Each step retains one possible half and reduces the width.",
                            "Hvert trin bevarer en mulig halvdel og reducerer bredden.",
                        ),
                    ),
                    (
                        "exact_float",
                        (
                            "Los float garantizan encontrar igualdad exacta.",
                            "Floats guarantee exact equality will be found.",
                            "Float-værdier garanterer, at eksakt lighed findes.",
                        ),
                    ),
                ),
                "shrinking_interval",
                (
                    "El progreso proviene de reducir sistemáticamente el espacio de búsqueda "
                    "mientras se conserva una solución posible.",
                    "Progress comes from systematically reducing the search space while retaining "
                    "a possible solution.",
                    "Fremdrift kommer af systematisk at reducere søgerummet, mens en mulig "
                    "løsning bevares.",
                ),
            ),
        ),
    )
    return _with_source_basis(
        extended,
        ("guttag-2021-ch01-03", "downey-2024-foundations"),
    )


def apply_foundations_book_extensions(
    modules: tuple[LocalizedLearningModule, ...],
) -> tuple[LocalizedLearningModule, ...]:
    """Apply M01-M03 extensions without changing module order or stable IDs."""
    extended: list[LocalizedLearningModule] = []
    for module in modules:
        if module.module_id == "dm857.m01":
            extended.append(_extend_foundations(module))
        elif module.module_id == "dm857.m02":
            extended.append(_extend_conditionals(module))
        elif module.module_id == "dm857.m03":
            extended.append(_extend_iteration(module))
        else:
            extended.append(module)
    return tuple(extended)


__all__ = [
    "apply_foundations_book_extensions",
    "update_foundations_audit",
]
