"""BMB830 module 9: interactions and nonlinear terms."""

from __future__ import annotations

from ...i18n import AppLocale
from ..models import AssessmentItem, LearningModule
from .standard import StandardModuleSpec, build_module, build_question_bank, materialize_bank

_SPEC = StandardModuleSpec(
    module_id="bmb830.m09",
    title=(
        "Interacciones y términos no lineales",
        "Interactions and nonlinear terms",
        "Interaktioner og ikke-lineære led",
    ),
    summary=(
        "Modela modificación de efecto, interpreta pendientes condicionadas y representa curvatura sin confundir complejidad matemática con causalidad.",
        "Model effect modification, interpret conditional slopes, and represent curvature without confusing mathematical complexity with causality.",
        "Modellér effektmodifikation, fortolk betingede hældninger, og repræsentér krumning uden at forveksle matematisk kompleksitet med kausalitet.",
    ),
    objectives=(
        (
            "m09.o1",
            (
                "Distinguir interacción estadística, modificación de efecto y confusión.",
                "Distinguish statistical interaction, effect modification, and confounding.",
                "Skelne mellem statistisk interaktion, effektmodifikation og confounding.",
            ),
        ),
        (
            "m09.o2",
            (
                "Interpretar coeficientes de interacción y obtener pendientes específicas por grupo.",
                "Interpret interaction coefficients and derive group-specific slopes.",
                "Fortolke interaktionskoefficienter og udlede gruppespecifikke hældninger.",
            ),
        ),
        (
            "m09.o3",
            (
                "Usar centrado y predicciones condicionadas para comunicar modelos con interacción.",
                "Use centring and conditional predictions to communicate interaction models.",
                "Bruge centrering og betingede prædiktioner til at kommunikere interaktionsmodeller.",
            ),
        ),
        (
            "m09.o4",
            (
                "Representar curvatura con términos polinomiales y comparar modelos anidados sin extrapolación injustificada.",
                "Represent curvature with polynomial terms and compare nested models without unjustified extrapolation.",
                "Repræsentere krumning med polynomielle led og sammenligne indlejrede modeller uden uberettiget ekstrapolation.",
            ),
        ),
    ),
    concepts=(
        (
            "effect-modification",
            (
                "Interacción y modificación de efecto",
                "Interaction and effect modification",
                "Interaktion og effektmodifikation",
            ),
            (
                "Existe interacción en la escala del modelo cuando la asociación entre una exposición y la respuesta cambia según el valor de otra variable. La modificación de efecto puede ser científicamente relevante; no debe tratarse automáticamente como un sesgo que haya que eliminar. La conclusión depende de la escala elegida.",
                "Interaction exists on the model scale when the association between an exposure and the outcome changes with another variable. Effect modification may be scientifically important and should not automatically be treated as bias to remove. The conclusion depends on the chosen scale.",
                "Interaktion findes på modellens skala, når sammenhængen mellem en eksponering og udfaldet ændres med en anden variabel. Effektmodifikation kan være videnskabeligt vigtig og bør ikke automatisk behandles som bias, der skal fjernes. Konklusionen afhænger af den valgte skala.",
            ),
            (
                (
                    "Confusión distorsiona una asociación; interacción describe heterogeneidad de la asociación.",
                    "Confounding distorts an association; interaction describes heterogeneity of the association.",
                    "Confounding forvrænger en association; interaktion beskriver heterogenitet i associationen.",
                ),
                (
                    "La interacción debe interpretarse mediante efectos condicionados, no solo mediante un valor p.",
                    "Interaction should be interpreted through conditional effects, not only a p-value.",
                    "Interaktion bør fortolkes gennem betingede effekter, ikke kun en p-værdi.",
                ),
            ),
        ),
        (
            "product-term",
            (
                "Término producto y jerarquía",
                "Product term and hierarchy",
                "Produktled og hierarki",
            ),
            (
                "En el modelo Y=β0+β1X+β2G+β3XG+ε, β1 es la pendiente de X cuando G=0 y β3 es la diferencia de pendientes cuando G pasa de 0 a 1. La pendiente para G=1 es β1+β3. Mantener los términos principales preserva la jerarquía y evita parametrizaciones difíciles de interpretar.",
                "In Y=β0+β1X+β2G+β3XG+ε, β1 is the slope of X when G=0 and β3 is the difference in slopes when G moves from 0 to 1. The slope for G=1 is β1+β3. Retaining main effects preserves hierarchy and avoids hard-to-interpret parameterisations.",
                "I Y=β0+β1X+β2G+β3XG+ε er β1 hældningen for X, når G=0, og β3 er forskellen i hældninger, når G går fra 0 til 1. Hældningen for G=1 er β1+β3. Bevarelse af hovedled opretholder hierarkiet og undgår svære parametriseringer.",
            ),
            (
                (
                    "Con interacción, un efecto principal es condicional, no promedio global.",
                    "With interaction, a main effect is conditional, not a global average.",
                    "Ved interaktion er en hovedeffekt betinget, ikke et globalt gennemsnit.",
                ),
                (
                    "La fórmula `x * group` expande a `x + group + x:group`.",
                    "The formula `x * group` expands to `x + group + x:group`.",
                    "Formlen `x * group` udvides til `x + group + x:group`.",
                ),
            ),
        ),
        (
            "centring-prediction",
            (
                "Centrado y predicción condicionada",
                "Centring and conditional prediction",
                "Centrering og betinget prædiktion",
            ),
            (
                "Centrar un predictor continuo cambia el punto en el que se interpretan interceptos y efectos principales, pero no cambia los valores ajustados ni el contraste de interacción. Las predicciones para combinaciones científicamente relevantes suelen comunicar mejor el modelo que una lista aislada de coeficientes.",
                "Centring a continuous predictor changes the point at which intercepts and main effects are interpreted, but does not change fitted values or the interaction contrast. Predictions for scientifically relevant combinations often communicate the model better than an isolated coefficient list.",
                "Centrering af en kontinuert prædiktor ændrer det punkt, hvor skæringer og hovedeffekter fortolkes, men ændrer ikke de tilpassede værdier eller interaktionskontrasten. Prædiktioner for videnskabeligt relevante kombinationer kommunikerer ofte modellen bedre end en isoleret koefficientliste.",
            ),
            (
                (
                    "Centrar no elimina colinealidad estructural ni confusión.",
                    "Centring does not remove structural collinearity or confounding.",
                    "Centrering fjerner ikke strukturel kollinearitet eller confounding.",
                ),
                (
                    "Las curvas o líneas por grupo deben mostrarse dentro del rango observado.",
                    "Group-specific curves or lines should be shown within the observed range.",
                    "Gruppespecifikke kurver eller linjer bør vises inden for det observerede område.",
                ),
            ),
        ),
        (
            "nonlinearity",
            (
                "Curvatura y términos polinomiales",
                "Curvature and polynomial terms",
                "Krumning og polynomielle led",
            ),
            (
                "Un término cuadrático permite que la pendiente cambie con X: E(Y|X)=β0+β1X+β2X². β1 ya no es una pendiente constante; la derivada local es β1+2β2X. Los polinomios son una aproximación dentro del rango observado y pueden comportarse mal al extrapolar.",
                "A quadratic term allows the slope to change with X: E(Y|X)=β0+β1X+β2X². β1 is no longer a constant slope; the local derivative is β1+2β2X. Polynomials are an approximation within the observed range and may behave poorly under extrapolation.",
                "Et kvadratisk led tillader, at hældningen ændres med X: E(Y|X)=β0+β1X+β2X². β1 er ikke længere en konstant hældning; den lokale afledte er β1+2β2X. Polynomier er en approksimation inden for det observerede område og kan opføre sig dårligt ved ekstrapolation.",
            ),
            (
                (
                    "La comparación de modelos debe considerar ajuste, complejidad y objetivo científico.",
                    "Model comparison should consider fit, complexity, and the scientific aim.",
                    "Modelsammenligning bør overveje tilpasning, kompleksitet og det videnskabelige mål.",
                ),
                (
                    "Un patrón curvo no convierte el modelo en causal.",
                    "A curved pattern does not make the model causal.",
                    "Et buet mønster gør ikke modellen kausal.",
                ),
            ),
        ),
    ),
    examples=(
        (
            "m09.e01",
            (
                "Pendientes específicas por grupo",
                "Group-specific slopes",
                "Gruppespecifikke hældninger",
            ),
            (
                "Ajusta una interacción entre exposición continua y grupo, y deriva las pendientes de ambos grupos.",
                "Fit an interaction between a continuous exposure and group, and derive both group-specific slopes.",
                "Tilpas en interaktion mellem en kontinuert eksponering og gruppe, og udled begge gruppers hældninger.",
            ),
            (
                (
                    "El grupo control es la referencia.",
                    "The control group is the reference.",
                    "Kontrolgruppen er reference.",
                ),
                (
                    "La pendiente del grupo tratado suma la pendiente base y la interacción.",
                    "The treated-group slope adds the baseline slope and interaction.",
                    "Hældningen for den behandlede gruppe summerer basishældningen og interaktionen.",
                ),
            ),
            """exposure <- rep(1:5, 2)
group <- factor(rep(c("control", "treated"), each = 5), levels = c("control", "treated"))
response <- c(2.0, 3.0, 4.0, 5.0, 6.0, 1.5, 3.0, 4.5, 6.0, 7.5)
fit <- lm(response ~ exposure * group)
b <- coef(fit)
control_slope <- b[["exposure"]]
treated_slope <- b[["exposure"]] + b[["exposure:grouptreated"]]
cat(sprintf("control_slope=%.2f\n", control_slope))
cat(sprintf("treated_slope=%.2f\n", treated_slope))
cat(sprintf("interaction=%.2f", b[["exposure:grouptreated"]]))
""",
            """control_slope=1.00
treated_slope=1.50
interaction=0.50""",
            (
                "La interacción de 0,50 indica que la pendiente estimada es medio punto mayor en el grupo tratado sobre la escala de respuesta.",
                "The interaction of 0.50 indicates that the estimated slope is half a response unit larger in the treated group.",
                "Interaktionen på 0,50 angiver, at den estimerede hældning er en halv responsenhed større i den behandlede gruppe.",
            ),
        ),
        (
            "m09.e02",
            (
                "Modelo lineal frente a cuadrático",
                "Linear versus quadratic model",
                "Lineær kontra kvadratisk model",
            ),
            (
                "Compara un modelo lineal con uno cuadrático para una respuesta curvada dentro del rango observado.",
                "Compare a linear model with a quadratic model for a curved response within the observed range.",
                "Sammenlign en lineær model med en kvadratisk model for et buet respons inden for det observerede område.",
            ),
            (
                (
                    "`I(x^2)` incluye el cuadrado aritmético de x.",
                    "`I(x^2)` includes the arithmetic square of x.",
                    "`I(x^2)` inkluderer det aritmetiske kvadrat af x.",
                ),
                (
                    "La comparación anidada pregunta si el término adicional mejora el ajuste bajo los supuestos.",
                    "The nested comparison asks whether the added term improves fit under the assumptions.",
                    "Den indlejrede sammenligning spørger, om det ekstra led forbedrer tilpasningen under antagelserne.",
                ),
            ),
            """x <- 0:6
response <- c(4.0, 2.4, 1.3, 1.0, 1.4, 2.6, 4.2)
linear <- lm(response ~ x)
quadratic <- lm(response ~ x + I(x^2))
comparison <- anova(linear, quadratic)
new_data <- data.frame(x = c(1, 3, 5))
predicted <- predict(quadratic, newdata = new_data)
cat(sprintf("quadratic=%.3f\n", coef(quadratic)[["I(x^2)"]]))
cat(sprintf("comparison_p=%.4f\n", comparison[2, "Pr(>F)"]))
cat(paste(sprintf("%.2f", predicted), collapse = ", "))
""",
            """quadratic=0.350
comparison_p=0.0003
2.39, 0.93, 2.67""",
            (
                "El término cuadrático representa curvatura; la interpretación debe apoyarse en predicciones dentro del rango y diagnóstico posterior.",
                "The quadratic term represents curvature; interpretation should rely on within-range predictions and subsequent diagnostics.",
                "Det kvadratiske led repræsenterer krumning; fortolkningen bør baseres på prædiktioner inden for området og efterfølgende diagnostik.",
            ),
        ),
    ),
    practices=(
        (
            "m09.p01",
            "DATA_INTERPRETATION",
            (
                "Interpreta β1=1,2 y β3=−0,4 en un modelo X*grupo con control como referencia.",
                "Interpret β1=1.2 and β3=−0.4 in an X-by-group model with control as reference.",
                "Fortolk β1=1,2 og β3=−0,4 i en X-ganget-med-gruppe-model med kontrol som reference.",
            ),
            (("Calcula ambas pendientes.", "Calculate both slopes.", "Beregn begge hældninger."),),
            (
                "Pendiente control=1,2; pendiente del otro grupo=1,2−0,4=0,8 por unidad de X.",
                "Control slope=1.2; other-group slope=1.2−0.4=0.8 per X unit.",
                "Kontrolhældning=1,2; den anden gruppes hældning=1,2−0,4=0,8 pr. X-enhed.",
            ),
            (
                "El coeficiente de interacción es una diferencia de pendientes.",
                "The interaction coefficient is a difference in slopes.",
                "Interaktionskoefficienten er en forskel i hældninger.",
            ),
            "",
        ),
        (
            "m09.p02",
            "CODE_COMPLETION",
            (
                "Completa una fórmula con interacción entre exposure y group.",
                "Complete a formula with an interaction between exposure and group.",
                "Fuldfør en formel med interaktion mellem exposure og group.",
            ),
            (
                (
                    "Usa el operador que incluye términos principales y producto.",
                    "Use the operator that includes main effects and the product term.",
                    "Brug operatoren, der inkluderer hovedled og produktled.",
                ),
            ),
            ("lm(response ~ exposure * group, data = d)",) * 3,
            (
                "El asterisco expande la jerarquía completa.",
                "The asterisk expands the complete hierarchy.",
                "Stjernen udvider det fulde hierarki.",
            ),
            "fit <- _________________________________",
        ),
        (
            "m09.p03",
            "ORAL_EXPLANATION",
            (
                "Explica por qué el efecto principal de exposición es condicional cuando existe interacción.",
                "Explain why the exposure main effect is conditional when an interaction is present.",
                "Forklar hvorfor eksponeringens hovedeffekt er betinget, når der er en interaktion.",
            ),
            (
                (
                    "Identifica el valor de referencia del modificador.",
                    "Identify the modifier's reference value.",
                    "Identificér modifikatorens referenceværdi.",
                ),
            ),
            (
                "Representa la pendiente cuando el modificador vale cero o está en su nivel de referencia; en otros valores debe combinarse con la interacción.",
                "It represents the slope when the modifier equals zero or is at its reference level; at other values it must be combined with the interaction.",
                "Den repræsenterer hældningen, når modifikatoren er nul eller på referenceniveauet; ved andre værdier skal den kombineres med interaktionen.",
            ),
            (
                "No es una pendiente promedio para toda la población.",
                "It is not an average slope for the whole population.",
                "Det er ikke en gennemsnitlig hældning for hele populationen.",
            ),
            "",
        ),
        (
            "m09.p04",
            "DEBUGGING",
            (
                "Corrige un modelo que incluye X:G pero elimina X y G sin justificación.",
                "Correct a model that includes X:G but removes X and G without justification.",
                "Ret en model, der inkluderer X:G, men fjerner X og G uden begrundelse.",
            ),
            (
                (
                    "Aplica el principio jerárquico.",
                    "Apply the hierarchy principle.",
                    "Anvend hierarkiprincippet.",
                ),
            ),
            (
                "Usar X*G o incluir explícitamente X + G + X:G, salvo una parametrización científica especial claramente documentada.",
                "Use X*G or explicitly include X + G + X:G unless a special scientific parameterisation is clearly documented.",
                "Brug X*G eller inkluder eksplicit X + G + X:G, medmindre en særlig videnskabelig parametrisering er tydeligt dokumenteret.",
            ),
            (
                "Eliminar términos principales cambia el significado del producto y suele imponer restricciones no deseadas.",
                "Removing main effects changes the product term's meaning and usually imposes unwanted constraints.",
                "Fjernelse af hovedled ændrer produktleddets betydning og pålægger normalt uønskede begrænsninger.",
            ),
            "",
        ),
        (
            "m09.p05",
            "PIPELINE_DESIGN",
            (
                "Diseña el reporte de una interacción exposición*sexo.",
                "Design the report for an exposure-by-sex interaction.",
                "Design rapporteringen af en eksponering-ganget-med-køn-interaktion.",
            ),
            (
                (
                    "No te limites al valor p del producto.",
                    "Do not stop at the product-term p-value.",
                    "Stop ikke ved produktleddets p-værdi.",
                ),
            ),
            (
                "Definir escala y referencia; reportar coeficientes e intervalos; calcular pendientes o contrastes por sexo; mostrar predicciones dentro del rango; discutir plausibilidad y precisión.",
                "Define scale and reference; report coefficients and intervals; calculate sex-specific slopes or contrasts; show within-range predictions; discuss plausibility and precision.",
                "Definér skala og reference; rapportér koefficienter og intervaller; beregn kønsspecifikke hældninger eller kontraster; vis prædiktioner inden for området; diskutér plausibilitet og præcision.",
            ),
            (
                "La comunicación debe permitir reconstruir el patrón heterogéneo.",
                "Communication should allow the heterogeneous pattern to be reconstructed.",
                "Kommunikationen bør gøre det muligt at rekonstruere det heterogene mønster.",
            ),
            "",
        ),
        (
            "m09.p06",
            "DATA_INTERPRETATION",
            (
                "Interpreta un coeficiente cuadrático positivo sin llamarlo una pendiente constante.",
                "Interpret a positive quadratic coefficient without calling it a constant slope.",
                "Fortolk en positiv kvadratisk koefficient uden at kalde den en konstant hældning.",
            ),
            (
                (
                    "La pendiente depende de X.",
                    "The slope depends on X.",
                    "Hældningen afhænger af X.",
                ),
            ),
            (
                "El modelo presenta curvatura convexa en la escala de respuesta; el cambio local se calcula como β1+2β2X y debe evaluarse en valores concretos de X.",
                "The model has convex curvature on the response scale; the local change is β1+2β2X and should be evaluated at specific X values.",
                "Modellen har konveks krumning på responsskalaen; den lokale ændring er β1+2β2X og bør vurderes ved konkrete X-værdier.",
            ),
            (
                "El signo aislado no resume toda la forma ni justifica extrapolar.",
                "The sign alone does not summarise the whole shape or justify extrapolation.",
                "Fortegnet alene opsummerer ikke hele formen og begrunder ikke ekstrapolation.",
            ),
            "",
        ),
    ),
    mcqs=(
        (
            "001",
            (
                "¿Qué representa β3 en Y=β0+β1X+β2G+β3XG?",
                "What does β3 represent in Y=β0+β1X+β2G+β3XG?",
                "Hvad repræsenterer β3 i Y=β0+β1X+β2G+β3XG?",
            ),
            (
                (
                    "a",
                    (
                        "Pendiente de X cuando G=0",
                        "Slope of X when G=0",
                        "Hældningen for X når G=0",
                    ),
                ),
                (
                    "b",
                    (
                        "Diferencia de pendientes entre niveles de G",
                        "Difference in slopes between G levels",
                        "Forskel i hældninger mellem G-niveauer",
                    ),
                ),
                ("c", ("Media global", "Global mean", "Globalt gennemsnit")),
                ("d", ("Varianza residual", "Residual variance", "Residualvarians")),
            ),
            "b",
            (
                "El término producto cuantifica cuánto cambia la pendiente.",
                "The product term quantifies how much the slope changes.",
                "Produktleddet kvantificerer, hvor meget hældningen ændres.",
            ),
        ),
        (
            "002",
            (
                "¿Cuál es la pendiente para G=1?",
                "What is the slope for G=1?",
                "Hvad er hældningen for G=1?",
            ),
            (
                ("a", ("β1", "β1", "β1")),
                ("b", ("β2", "β2", "β2")),
                ("c", ("β1+β3", "β1+β3", "β1+β3")),
                ("d", ("β0+β2", "β0+β2", "β0+β2")),
            ),
            "c",
            (
                "Se suma la pendiente de referencia y el cambio de pendiente.",
                "Add the reference slope and the slope change.",
                "Læg referencehældningen og hældningsændringen sammen.",
            ),
        ),
        (
            "003",
            (
                "¿Qué expande `x * group` en una fórmula de R?",
                "What does `x * group` expand to in an R formula?",
                "Hvad udvides `x * group` til i en R-formel?",
            ),
            (
                ("a", ("Solo x:group", "Only x:group", "Kun x:group")),
                ("b", ("x + group + x:group", "x + group + x:group", "x + group + x:group")),
                ("c", ("x + group", "x + group", "x + group")),
                ("d", ("I(x^2)", "I(x^2)", "I(x^2)")),
            ),
            "b",
            (
                "El asterisco incluye términos principales e interacción.",
                "The asterisk includes main effects and interaction.",
                "Stjernen inkluderer hovedled og interaktion.",
            ),
        ),
        (
            "004",
            (
                "¿Qué cambia al centrar X?",
                "What changes when X is centred?",
                "Hvad ændres, når X centreres?",
            ),
            (
                ("a", ("Valores ajustados", "Fitted values", "Tilpassede værdier")),
                (
                    "b",
                    (
                        "Punto de interpretación del intercepto",
                        "Interpretation point of the intercept",
                        "Skæringens fortolkningspunkt",
                    ),
                ),
                ("c", ("Número de observaciones", "Number of observations", "Antal observationer")),
                ("d", ("Respuesta observada", "Observed response", "Observeret respons")),
            ),
            "b",
            (
                "El origen de la escala cambia, pero no las predicciones ajustadas.",
                "The scale origin changes, but fitted predictions do not.",
                "Skalaens nulpunkt ændres, men de tilpassede prædiktioner gør ikke.",
            ),
        ),
        (
            "005",
            (
                "¿Qué significa un término cuadrático?",
                "What does a quadratic term mean?",
                "Hvad betyder et kvadratisk led?",
            ),
            (
                ("a", ("Pendiente constante", "Constant slope", "Konstant hældning")),
                (
                    "b",
                    (
                        "Pendiente que cambia con X",
                        "Slope that changes with X",
                        "Hældning der ændres med X",
                    ),
                ),
                ("c", ("Ausencia de error", "Absence of error", "Fravær af fejl")),
                ("d", ("Causalidad", "Causality", "Kausalitet")),
            ),
            "b",
            (
                "La derivada local depende del valor de X.",
                "The local derivative depends on X.",
                "Den lokale afledte afhænger af X.",
            ),
        ),
        (
            "006",
            (
                "¿Qué diferencia confusión de modificación de efecto?",
                "What distinguishes confounding from effect modification?",
                "Hvad adskiller confounding fra effektmodifikation?",
            ),
            (
                (
                    "a",
                    (
                        "La primera distorsiona; la segunda describe heterogeneidad",
                        "The first distorts; the second describes heterogeneity",
                        "Den første forvrænger; den anden beskriver heterogenitet",
                    ),
                ),
                ("b", ("Son idénticas", "They are identical", "De er identiske")),
                ("c", ("Solo el tamaño muestral", "Only sample size", "Kun stikprøvestørrelsen")),
                ("d", ("El software", "The software", "Softwaren")),
            ),
            "a",
            (
                "Tienen funciones científicas diferentes.",
                "They have different scientific roles.",
                "De har forskellige videnskabelige roller.",
            ),
        ),
        (
            "007",
            (
                "¿Cómo debe comunicarse una interacción?",
                "How should an interaction be communicated?",
                "Hvordan bør en interaktion kommunikeres?",
            ),
            (
                ("a", ("Solo con p", "Only with p", "Kun med p")),
                (
                    "b",
                    (
                        "Con efectos o predicciones condicionadas e intervalos",
                        "With conditional effects or predictions and intervals",
                        "Med betingede effekter eller prædiktioner og intervaller",
                    ),
                ),
                ("c", ("Eliminando grupos", "By deleting groups", "Ved at slette grupper")),
                (
                    "d",
                    ("Ocultando referencias", "By hiding references", "Ved at skjule referencer"),
                ),
            ),
            "b",
            (
                "La magnitud y la forma requieren valores condicionados.",
                "Magnitude and shape require conditional values.",
                "Størrelse og form kræver betingede værdier.",
            ),
        ),
        (
            "008",
            (
                "¿Dónde es más segura la interpretación de un polinomio?",
                "Where is polynomial interpretation safest?",
                "Hvor er fortolkning af et polynomium sikrest?",
            ),
            (
                ("a", ("Muy lejos de los datos", "Far beyond the data", "Langt uden for data")),
                (
                    "b",
                    (
                        "Dentro del rango observado",
                        "Within the observed range",
                        "Inden for det observerede område",
                    ),
                ),
                ("c", ("Solo en X=0", "Only at X=0", "Kun ved X=0")),
                ("d", ("Sin gráficos", "Without plots", "Uden plots")),
            ),
            "b",
            (
                "La extrapolación polinomial puede ser inestable.",
                "Polynomial extrapolation can be unstable.",
                "Polynomiel ekstrapolation kan være ustabil.",
            ),
        ),
    ),
    true_false=(
        (
            "009",
            (
                "Una interacción significativa demuestra causalidad.",
                "A significant interaction proves causality.",
                "En signifikant interaktion beviser kausalitet.",
            ),
            False,
            (
                "La interpretación causal requiere diseño y supuestos adicionales.",
                "Causal interpretation requires additional design and assumptions.",
                "Kausal fortolkning kræver yderligere design og antagelser.",
            ),
        ),
        (
            "010",
            (
                "Con interacción, β1 suele ser la pendiente en el nivel de referencia.",
                "With interaction, β1 is usually the slope at the reference level.",
                "Ved interaktion er β1 normalt hældningen på referenceniveauet.",
            ),
            True,
            (
                "Su significado depende de cómo se codifica el modificador.",
                "Its meaning depends on modifier coding.",
                "Betydningen afhænger af modifikatorens kodning.",
            ),
        ),
        (
            "011",
            (
                "Centrar X cambia los valores ajustados del modelo equivalente.",
                "Centring X changes fitted values of the equivalent model.",
                "Centrering af X ændrer de tilpassede værdier i den ækvivalente model.",
            ),
            False,
            (
                "Solo reparametriza el origen de X.",
                "It only reparameterises the origin of X.",
                "Det omparametriserer kun X's nulpunkt.",
            ),
        ),
        (
            "012",
            (
                "La interacción puede depender de la escala de respuesta.",
                "Interaction may depend on the response scale.",
                "Interaktion kan afhænge af responsskalaen.",
            ),
            True,
            (
                "Aditividad en una escala no implica aditividad en otra.",
                "Additivity on one scale does not imply additivity on another.",
                "Additivitet på én skala indebærer ikke additivitet på en anden.",
            ),
        ),
        (
            "013",
            (
                "Eliminar términos principales siempre mejora la interpretación.",
                "Removing main effects always improves interpretation.",
                "Fjernelse af hovedled forbedrer altid fortolkningen.",
            ),
            False,
            (
                "Suele romper la jerarquía e imponer restricciones.",
                "It usually breaks hierarchy and imposes constraints.",
                "Det bryder normalt hierarkiet og pålægger begrænsninger.",
            ),
        ),
        (
            "014",
            (
                "En un modelo cuadrático la pendiente local depende de X.",
                "In a quadratic model the local slope depends on X.",
                "I en kvadratisk model afhænger den lokale hældning af X.",
            ),
            True,
            ("Es β1+2β2X.", "It is β1+2β2X.", "Den er β1+2β2X."),
        ),
        (
            "015",
            (
                "Un R² mayor basta para elegir el modelo más complejo.",
                "A larger R² is sufficient to choose the more complex model.",
                "Et større R² er tilstrækkeligt til at vælge den mere komplekse model.",
            ),
            False,
            (
                "También importan complejidad, objetivo, diagnóstico y validación.",
                "Complexity, aim, diagnostics, and validation also matter.",
                "Kompleksitet, mål, diagnostik og validering betyder også noget.",
            ),
        ),
        (
            "016",
            (
                "Las predicciones por grupo pueden aclarar una interacción.",
                "Group-specific predictions can clarify an interaction.",
                "Gruppespecifikke prædiktioner kan tydeliggøre en interaktion.",
            ),
            True,
            (
                "Muestran la magnitud condicionada en valores relevantes.",
                "They show conditional magnitude at relevant values.",
                "De viser den betingede størrelse ved relevante værdier.",
            ),
        ),
    ),
    tutor=(
        (
            "Los modelos con interacción y curvatura deben interpretarse mediante efectos condicionados, predicciones dentro del rango observado e intervalos, manteniendo la jerarquía y separando heterogeneidad estadística de causalidad.",
            "Models with interaction and curvature should be interpreted through conditional effects, within-range predictions, and intervals while preserving hierarchy and separating statistical heterogeneity from causality.",
            "Modeller med interaktion og krumning bør fortolkes gennem betingede effekter, prædiktioner inden for det observerede område og intervaller, samtidig med at hierarki bevares og statistisk heterogenitet adskilles fra kausalitet.",
        ),
        (
            (
                "Una interacción es una diferencia de efectos sobre una escala definida.",
                "An interaction is a difference in effects on a defined scale.",
                "En interaktion er en forskel i effekter på en defineret skala.",
            ),
            (
                "Los efectos principales son condicionales.",
                "Main effects are conditional.",
                "Hovedeffekter er betingede.",
            ),
            (
                "Centrar mejora interpretación, no validez causal.",
                "Centring improves interpretation, not causal validity.",
                "Centrering forbedrer fortolkning, ikke kausal validitet.",
            ),
            (
                "Los polinomios se interpretan mediante forma y predicción.",
                "Polynomials are interpreted through shape and prediction.",
                "Polynomier fortolkes gennem form og prædiktion.",
            ),
        ),
        (
            (
                "Interpretar β1 como efecto global cuando existe interacción.",
                "Interpreting β1 as a global effect when interaction is present.",
                "At fortolke β1 som en global effekt, når der er interaktion.",
            ),
            (
                "Reportar solo el valor p del producto.",
                "Reporting only the product-term p-value.",
                "Kun at rapportere produktleddets p-værdi.",
            ),
            (
                "Extrapolar polinomios lejos del rango observado.",
                "Extrapolating polynomials far beyond the observed range.",
                "At ekstrapolere polynomier langt uden for det observerede område.",
            ),
        ),
        (
            (
                "¿Cuál es el nivel de referencia?",
                "What is the reference level?",
                "Hvad er referenceniveauet?",
            ),
            (
                "¿Qué pendiente corresponde a cada grupo?",
                "Which slope belongs to each group?",
                "Hvilken hældning tilhører hver gruppe?",
            ),
            (
                "¿En qué escala se define la interacción?",
                "On which scale is the interaction defined?",
                "På hvilken skala er interaktionen defineret?",
            ),
        ),
        (
            (
                "Deriva efectos condicionados correctamente.",
                "Correctly derives conditional effects.",
                "Udleder betingede effekter korrekt.",
            ),
            (
                "Mantiene la jerarquía del modelo.",
                "Preserves model hierarchy.",
                "Bevarer modelhierarkiet.",
            ),
            (
                "Interpreta curvatura mediante predicciones dentro del rango.",
                "Interprets curvature through within-range predictions.",
                "Fortolker krumning gennem prædiktioner inden for området.",
            ),
        ),
        (
            (
                "No declarar causalidad desde una interacción estadística.",
                "Do not declare causality from statistical interaction.",
                "Erklær ikke kausalitet ud fra statistisk interaktion.",
            ),
            (
                "No inventar niveles de referencia ni rangos observados.",
                "Do not invent reference levels or observed ranges.",
                "Opfind ikke referenceniveauer eller observerede områder.",
            ),
            (
                "Responder en el idioma activo.",
                "Respond in the active language.",
                "Svar på det aktive sprog.",
            ),
        ),
        (
            "SDU ODIN BMB830 active course description approved 2025-03-06",
            "R base stats documentation: lm, model.matrix, predict, anova",
            "Hierarchical interaction and polynomial-model principles",
        ),
    ),
)

LOCALIZED_MODULE_09_INTERACTIONS_NONLINEARITY = build_module(_SPEC)
LOCALIZED_OBJECTIVE_QUESTION_BANK_09 = build_question_bank(_SPEC)
MODULE_09_INTERACTIONS_NONLINEARITY: LearningModule = (
    LOCALIZED_MODULE_09_INTERACTIONS_NONLINEARITY.materialize(AppLocale.SPANISH_SPAIN)
)
OBJECTIVE_QUESTION_BANK_09: tuple[AssessmentItem, ...] = materialize_bank(
    LOCALIZED_OBJECTIVE_QUESTION_BANK_09
)


def materialize_module_09_question_bank(
    locale: AppLocale | str = AppLocale.SPANISH_SPAIN,
) -> tuple[AssessmentItem, ...]:
    """Return the module-9 objective bank in one locale."""

    return materialize_bank(LOCALIZED_OBJECTIVE_QUESTION_BANK_09, locale)


__all__ = [
    "LOCALIZED_MODULE_09_INTERACTIONS_NONLINEARITY",
    "LOCALIZED_OBJECTIVE_QUESTION_BANK_09",
    "MODULE_09_INTERACTIONS_NONLINEARITY",
    "OBJECTIVE_QUESTION_BANK_09",
    "materialize_module_09_question_bank",
]
