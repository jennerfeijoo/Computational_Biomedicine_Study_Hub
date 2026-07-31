"""BMB830 module 7: correlation and simple linear regression."""

from __future__ import annotations

from ...i18n import AppLocale
from ..models import AssessmentItem, LearningModule
from .standard import StandardModuleSpec, build_module, build_question_bank, materialize_bank

_SPEC = StandardModuleSpec(
    module_id="bmb830.m07",
    title=(
        "Correlación y regresión lineal simple",
        "Correlation and simple linear regression",
        "Korrelation og simpel lineær regression",
    ),
    summary=(
        "Distingue asociación de causalidad, cuantifica relaciones lineales y ajusta, diagnostica e interpreta modelos de regresión lineal simple en R.",
        "Distinguish association from causation, quantify linear relationships, and fit, diagnose, and interpret simple linear regression models in R.",
        "Skeln mellem association og kausalitet, kvantificér lineære relationer, og tilpas, diagnosticér og fortolk simple lineære regressionsmodeller i R.",
    ),
    objectives=(
        (
            "m07.o1",
            (
                "Distinguir correlación, asociación y causalidad.",
                "Distinguish correlation, association, and causation.",
                "Skelne mellem korrelation, association og kausalitet.",
            ),
        ),
        (
            "m07.o2",
            (
                "Seleccionar e interpretar correlaciones de Pearson y Spearman.",
                "Select and interpret Pearson and Spearman correlations.",
                "Vælge og fortolke Pearson- og Spearman-korrelationer.",
            ),
        ),
        (
            "m07.o3",
            (
                "Ajustar un modelo lineal simple e interpretar intercepto, pendiente, intervalos y R².",
                "Fit a simple linear model and interpret intercept, slope, intervals, and R².",
                "Tilpasse en simpel lineær model og fortolke skæring, hældning, intervaller og R².",
            ),
        ),
        (
            "m07.o4",
            (
                "Distinguir intervalos de confianza para la media e intervalos de predicción individual.",
                "Distinguish confidence intervals for the mean from individual prediction intervals.",
                "Skelne mellem konfidensintervaller for middelværdien og individuelle prædiktionsintervaller.",
            ),
        ),
    ),
    concepts=(
        (
            "association-causation",
            (
                "Asociación no implica causalidad",
                "Association does not imply causation",
                "Association indebærer ikke kausalitet",
            ),
            (
                "Una asociación estadística describe cómo varían dos variables conjuntamente. No establece por sí sola que cambiar una variable provoque un cambio en la otra. La confusión, la selección, la causalidad inversa y el azar pueden producir asociaciones observadas.",
                "A statistical association describes how two variables vary together. It does not by itself establish that changing one variable causes a change in the other. Confounding, selection, reverse causation, and chance can produce observed associations.",
                "En statistisk association beskriver, hvordan to variable varierer sammen. Den fastslår ikke i sig selv, at en ændring i den ene variabel forårsager en ændring i den anden. Confounding, selektion, omvendt kausalitet og tilfældighed kan skabe observerede associationer.",
            ),
            (
                (
                    "El diseño del estudio determina qué afirmaciones causales son defendibles.",
                    "Study design determines which causal claims are defensible.",
                    "Studiedesignet bestemmer, hvilke kausale påstande der kan forsvares.",
                ),
                (
                    "Un coeficiente grande puede seguir siendo no causal.",
                    "A large coefficient can still be non-causal.",
                    "En stor koefficient kan stadig være ikke-kausal.",
                ),
            ),
        ),
        (
            "correlation",
            (
                "Correlación de Pearson y Spearman",
                "Pearson and Spearman correlation",
                "Pearson- og Spearman-korrelation",
            ),
            (
                "Pearson resume la fuerza de una relación lineal y es sensible a valores extremos. Spearman calcula una asociación monótona basada en rangos y puede ser más apropiada para relaciones no lineales pero monotónicas o escalas ordinales. Ninguna medida sustituye la inspección gráfica.",
                "Pearson summarises the strength of a linear relationship and is sensitive to outliers. Spearman measures monotonic rank association and may suit nonlinear but monotonic relationships or ordinal scales. Neither measure replaces graphical inspection.",
                "Pearson opsummerer styrken af en lineær relation og er følsom over for ekstreme værdier. Spearman måler monoton rangassociation og kan passe til ikke-lineære, men monotone relationer eller ordinale skalaer. Ingen af målene erstatter grafisk inspektion.",
            ),
            (
                (
                    "La correlación es adimensional y está entre −1 y 1.",
                    "Correlation is dimensionless and lies between −1 and 1.",
                    "Korrelation er dimensionsløs og ligger mellem −1 og 1.",
                ),
                (
                    "Correlación cero no descarta una relación no lineal.",
                    "Zero correlation does not rule out a nonlinear relationship.",
                    "Nulkorrelation udelukker ikke en ikke-lineær relation.",
                ),
            ),
        ),
        (
            "linear-model",
            (
                "Modelo lineal simple",
                "Simple linear model",
                "Simpel lineær model",
            ),
            (
                "El modelo Y = β0 + β1X + ε representa la media esperada de Y como una función lineal de X. El intercepto β0 es la media esperada cuando X=0; la pendiente β1 es el cambio medio esperado en Y por una unidad adicional de X.",
                "The model Y = β0 + β1X + ε represents the expected mean of Y as a linear function of X. The intercept β0 is the expected mean when X=0; the slope β1 is the expected mean change in Y for a one-unit increase in X.",
                "Modellen Y = β0 + β1X + ε repræsenterer den forventede middelværdi af Y som en lineær funktion af X. Skæringen β0 er den forventede middelværdi ved X=0; hældningen β1 er den forventede ændring i Y ved én enheds stigning i X.",
            ),
            (
                (
                    "La pendiente conserva unidades de Y por unidad de X.",
                    "The slope retains units of Y per unit of X.",
                    "Hældningen har enheden Y pr. enhed X.",
                ),
                (
                    "El intercepto puede carecer de interpretación si X=0 queda fuera del rango observado.",
                    "The intercept may lack interpretation if X=0 lies outside the observed range.",
                    "Skæringen kan mangle fortolkning, hvis X=0 ligger uden for det observerede område.",
                ),
            ),
        ),
        (
            "fit-prediction",
            (
                "Ajuste, incertidumbre y predicción",
                "Fit, uncertainty, and prediction",
                "Tilpasning, usikkerhed og prædiktion",
            ),
            (
                "R² resume la proporción de variabilidad muestral explicada por el modelo, pero no mide causalidad ni validez externa. Un intervalo de confianza estima la media esperada en un valor de X; un intervalo de predicción incorpora además la variabilidad individual y por ello es más ancho.",
                "R² summarises the proportion of sample variability explained by the model, but it does not measure causality or external validity. A confidence interval estimates the expected mean at a value of X; a prediction interval also includes individual variability and is therefore wider.",
                "R² opsummerer den andel af stikprøvevariationen, modellen forklarer, men måler hverken kausalitet eller ekstern validitet. Et konfidensinterval estimerer den forventede middelværdi ved en X-værdi; et prædiktionsinterval inkluderer også individuel variation og er derfor bredere.",
            ),
            (
                (
                    "La extrapolación fuera del rango observado requiere una justificación fuerte.",
                    "Extrapolation beyond the observed range requires strong justification.",
                    "Ekstrapolation uden for det observerede område kræver en stærk begrundelse.",
                ),
                (
                    "Un buen ajuste muestral no garantiza una buena predicción futura.",
                    "Good sample fit does not guarantee good future prediction.",
                    "God tilpasning i stikprøven garanterer ikke god fremtidig prædiktion.",
                ),
            ),
        ),
    ),
    examples=(
        (
            "m07.e01",
            (
                "Correlación y regresión sobre los mismos datos",
                "Correlation and regression on the same data",
                "Korrelation og regression på de samme data",
            ),
            (
                "Cuantifica la asociación lineal y estima el cambio medio de respuesta por unidad de exposición.",
                "Quantify linear association and estimate the mean response change per exposure unit.",
                "Kvantificér den lineære association og estimér den gennemsnitlige ændring i respons pr. eksponeringsenhed.",
            ),
            (
                (
                    "Primero se inspecciona la relación y se calcula Pearson.",
                    "First inspect the relationship and calculate Pearson correlation.",
                    "Inspicér først relationen og beregn Pearson-korrelationen.",
                ),
                (
                    "Después se ajusta lm para obtener una pendiente con unidades e incertidumbre.",
                    "Then fit lm to obtain a slope with units and uncertainty.",
                    "Tilpas derefter lm for at få en hældning med enheder og usikkerhed.",
                ),
            ),
            """exposure <- c(1, 2, 3, 4, 5, 6)
response <- c(2.1, 2.9, 4.2, 5.1, 5.8, 7.2)
correlation <- cor(exposure, response, method = "pearson")
fit <- lm(response ~ exposure)
coefs <- coef(fit)
r_squared <- summary(fit)$r.squared
cat(sprintf("r=%.3f\n", correlation))
cat(sprintf("intercept=%.2f\n", coefs[[1]]))
cat(sprintf("slope=%.3f\n", coefs[[2]]))
cat(sprintf("r2=%.3f", r_squared))
""",
            """r=0.996
intercept=1.04
slope=1.003
r2=0.992""",
            (
                "La pendiente estima aproximadamente una unidad adicional de respuesta por unidad de exposición. La alta correlación describe linealidad muestral, no causalidad.",
                "The slope estimates approximately one additional response unit per exposure unit. The high correlation describes sample linearity, not causation.",
                "Hældningen estimerer omtrent én ekstra responsenhed pr. eksponeringsenhed. Den høje korrelation beskriver lineæritet i stikprøven, ikke kausalitet.",
            ),
        ),
        (
            "m07.e02",
            (
                "Intervalo de confianza frente a predicción",
                "Confidence interval versus prediction interval",
                "Konfidensinterval kontra prædiktionsinterval",
            ),
            (
                "Predice la respuesta media y una observación individual cuando la exposición es 4,5.",
                "Predict the mean response and an individual observation when exposure is 4.5.",
                "Prædikér middelresponsen og en individuel observation, når eksponeringen er 4,5.",
            ),
            (
                (
                    "El modelo se ajusta solo con el rango observado.",
                    "The model is fitted only within the observed range.",
                    "Modellen tilpasses kun inden for det observerede område.",
                ),
                (
                    "La predicción individual incorpora error residual adicional.",
                    "Individual prediction includes additional residual error.",
                    "Individuel prædiktion inkluderer yderligere residualfejl.",
                ),
            ),
            """exposure <- c(1, 2, 3, 4, 5, 6)
response <- c(2.1, 2.9, 4.2, 5.1, 5.8, 7.2)
fit <- lm(response ~ exposure)
new_data <- data.frame(exposure = 4.5)
mean_ci <- predict(fit, newdata = new_data, interval = "confidence")
individual_pi <- predict(fit, newdata = new_data, interval = "prediction")
cat(sprintf("mean=%.2f\n", mean_ci[1, "fit"]))
cat(sprintf("mean_ci=[%.2f, %.2f]\n", mean_ci[1, "lwr"], mean_ci[1, "upr"]))
cat(sprintf("prediction=[%.2f, %.2f]", individual_pi[1, "lwr"], individual_pi[1, "upr"]))
""",
            """mean=5.55
mean_ci=[5.30, 5.81]
prediction=[4.91, 6.20]""",
            (
                "El intervalo de predicción es más ancho porque representa una nueva observación, no solo la media condicional.",
                "The prediction interval is wider because it represents a new observation, not only the conditional mean.",
                "Prædiktionsintervallet er bredere, fordi det repræsenterer en ny observation og ikke kun den betingede middelværdi.",
            ),
        ),
    ),
    practices=(
        (
            "m07.p01",
            "DATA_INTERPRETATION",
            (
                "Interpreta r=−0,70 sin afirmar causalidad.",
                "Interpret r=−0.70 without claiming causation.",
                "Fortolk r=−0,70 uden at hævde kausalitet.",
            ),
            (("Describe dirección, fuerza y límites.", "Describe direction, strength, and limits.", "Beskriv retning, styrke og begrænsninger."),),
            (
                "Existe una asociación lineal negativa relativamente fuerte en la muestra; no demuestra que una variable cause cambios en la otra.",
                "There is a relatively strong negative linear association in the sample; it does not show that one variable causes changes in the other.",
                "Der er en relativt stærk negativ lineær association i stikprøven; det viser ikke, at den ene variabel forårsager ændringer i den anden.",
            ),
            (
                "La interpretación causal requiere diseño y supuestos adicionales.",
                "Causal interpretation requires additional design and assumptions.",
                "Kausal fortolkning kræver yderligere design og antagelser.",
            ),
            "",
        ),
        (
            "m07.p02",
            "CODE_COMPLETION",
            (
                "Completa una correlación de Spearman entre x e y.",
                "Complete a Spearman correlation between x and y.",
                "Fuldfør en Spearman-korrelation mellem x og y.",
            ),
            (("Declara el método explícitamente.", "Declare the method explicitly.", "Angiv metoden eksplicit."),),
            ("cor(x, y, method = 'spearman')",) * 3,
            (
                "Spearman opera sobre rangos y resume asociación monótona.",
                "Spearman operates on ranks and summarises monotonic association.",
                "Spearman arbejder på rangordener og opsummerer monoton association.",
            ),
            "rho <- ______________________________",
        ),
        (
            "m07.p03",
            "CODE_COMPLETION",
            (
                "Completa un modelo lineal con respuesta y exposición.",
                "Complete a linear model with response and exposure.",
                "Fuldfør en lineær model med respons og eksponering.",
            ),
            (("La respuesta va a la izquierda de ~.", "The response goes to the left of ~.", "Responsen står til venstre for ~."),),
            ("lm(response ~ exposure, data = dataset)",) * 3,
            (
                "La fórmula define la media condicional que se modela.",
                "The formula defines the conditional mean being modelled.",
                "Formlen definerer den betingede middelværdi, der modelleres.",
            ),
            "fit <- ______________________________",
        ),
        (
            "m07.p04",
            "ORAL_EXPLANATION",
            (
                "Explica una pendiente de 2,4 mg/L por año.",
                "Explain a slope of 2.4 mg/L per year.",
                "Forklar en hældning på 2,4 mg/L pr. år.",
            ),
            (("Mantén las unidades y la condición media.", "Retain units and the mean condition.", "Bevar enhederne og middelbetingelsen."),),
            (
                "Por cada año adicional, el modelo estima un aumento medio de 2,4 mg/L en la respuesta dentro del rango estudiado.",
                "For each additional year, the model estimates a mean increase of 2.4 mg/L in the response within the studied range.",
                "For hvert ekstra år estimerer modellen en gennemsnitlig stigning på 2,4 mg/L i responsen inden for det undersøgte område.",
            ),
            (
                "No implica que cada individuo aumente exactamente 2,4 mg/L ni que el efecto sea causal.",
                "It does not imply that every individual increases by exactly 2.4 mg/L or that the effect is causal.",
                "Det betyder ikke, at hvert individ stiger præcis 2,4 mg/L, eller at effekten er kausal.",
            ),
            "",
        ),
        (
            "m07.p05",
            "DEBUGGING",
            (
                "Corrige la conclusión 'R²=0,90 demuestra que X causa Y'.",
                "Correct the conclusion 'R²=0.90 proves that X causes Y'.",
                "Ret konklusionen 'R²=0,90 beviser, at X forårsager Y'.",
            ),
            (("R² describe ajuste muestral, no causalidad.", "R² describes sample fit, not causation.", "R² beskriver tilpasning i stikprøven, ikke kausalitet."),),
            (
                "El modelo explica el 90 % de la variabilidad muestral de Y mediante una relación lineal con X; la causalidad requiere evidencia adicional.",
                "The model explains 90% of the sample variability in Y through a linear relationship with X; causality requires additional evidence.",
                "Modellen forklarer 90 % af stikprøvevariationen i Y gennem en lineær relation til X; kausalitet kræver yderligere evidens.",
            ),
            (
                "R² tampoco garantiza predicción externa ni ausencia de sesgo.",
                "R² also guarantees neither external prediction nor absence of bias.",
                "R² garanterer heller ikke ekstern prædiktion eller fravær af bias.",
            ),
            "",
        ),
        (
            "m07.p06",
            "PIPELINE_DESIGN",
            (
                "Diseña el análisis mínimo de una relación continua X–Y.",
                "Design the minimum analysis of a continuous X–Y relationship.",
                "Design minimumsanalysen af en kontinuert X–Y-relation.",
            ),
            (("Incluye gráfico, estimando, ajuste y diagnóstico.", "Include plot, estimand, fit, and diagnostics.", "Medtag plot, estimand, tilpasning og diagnostik."),),
            (
                "Definir unidades y estimando; inspeccionar dispersión; justificar Pearson o Spearman; ajustar lm si la media lineal es pertinente; reportar pendiente, intervalo y R²; revisar residuos y limitar extrapolación.",
                "Define units and estimand; inspect a scatterplot; justify Pearson or Spearman; fit lm when a linear mean is appropriate; report slope, interval, and R²; inspect residuals and limit extrapolation.",
                "Definér enheder og estimand; inspicér et spredningsplot; begrund Pearson eller Spearman; tilpas lm, når en lineær middelværdi er relevant; rapportér hældning, interval og R²; inspicér residualer og begræns ekstrapolation.",
            ),
            (
                "La secuencia evita seleccionar el método solo por significación.",
                "The sequence avoids choosing a method only for significance.",
                "Sekvensen undgår at vælge metode alene efter signifikans.",
            ),
            "",
        ),
    ),
    mcqs=(
        (
            "001",
            ("¿Qué resume Pearson?", "What does Pearson summarise?", "Hvad opsummerer Pearson?"),
            (("a", ("Relación lineal", "Linear relationship", "Lineær relation")), ("b", ("Causalidad", "Causation", "Kausalitet")), ("c", ("Diferencia de medianas", "Median difference", "Medianforskel")), ("d", ("Riesgo absoluto", "Absolute risk", "Absolut risiko"))),
            "a",
            ("Pearson cuantifica asociación lineal estandarizada.", "Pearson quantifies standardised linear association.", "Pearson kvantificerer standardiseret lineær association."),
        ),
        (
            "002",
            ("¿Cuándo puede ser preferible Spearman?", "When may Spearman be preferable?", "Hvornår kan Spearman være at foretrække?"),
            (("a", ("Relación monótona y datos ordinales", "Monotonic relationship and ordinal data", "Monoton relation og ordinale data")), ("b", ("Para demostrar causalidad", "To prove causation", "For at bevise kausalitet")), ("c", ("Solo con n grande", "Only with large n", "Kun ved stort n")), ("d", ("Para estimar una media", "To estimate a mean", "For at estimere et gennemsnit"))),
            "a",
            ("Spearman usa rangos y resume monotonicidad.", "Spearman uses ranks and summarises monotonicity.", "Spearman bruger rangordener og opsummerer monotonicitet."),
        ),
        (
            "003",
            ("¿Qué representa β1?", "What does β1 represent?", "Hvad repræsenterer β1?"),
            (("a", ("Cambio medio esperado en Y por unidad de X", "Expected mean change in Y per X unit", "Forventet gennemsnitlig ændring i Y pr. X-enhed")), ("b", ("Media de X", "Mean of X", "Gennemsnittet af X")), ("c", ("Error individual", "Individual error", "Individuel fejl")), ("d", ("R²", "R²", "R²"))),
            "a",
            ("La pendiente tiene unidades Y por unidad X.", "The slope has Y units per X unit.", "Hældningen har Y-enheder pr. X-enhed."),
        ),
        (
            "004",
            ("¿Qué representa β0?", "What does β0 represent?", "Hvad repræsenterer β0?"),
            (("a", ("Media esperada de Y cuando X=0", "Expected mean Y when X=0", "Forventet middelværdi af Y ved X=0")), ("b", ("Correlación", "Correlation", "Korrelation")), ("c", ("Varianza residual", "Residual variance", "Residualvarians")), ("d", ("Tamaño muestral", "Sample size", "Stikprøvestørrelse"))),
            "a",
            ("El intercepto debe interpretarse solo si X=0 es relevante.", "The intercept should be interpreted only when X=0 is relevant.", "Skæringen bør kun fortolkes, når X=0 er relevant."),
        ),
        (
            "005",
            ("¿Qué comunica R²?", "What does R² communicate?", "Hvad kommunikerer R²?"),
            (("a", ("Proporción de variabilidad muestral explicada", "Proportion of sample variability explained", "Andel af stikprøvevariation forklaret")), ("b", ("Probabilidad causal", "Causal probability", "Kausal sandsynlighed")), ("c", ("Ausencia de sesgo", "Absence of bias", "Fravær af bias")), ("d", ("Validez externa", "External validity", "Ekstern validitet"))),
            "a",
            ("R² es una medida de ajuste dentro de la muestra.", "R² is a within-sample fit measure.", "R² er et mål for tilpasning i stikprøven."),
        ),
        (
            "006",
            ("¿Qué intervalo suele ser más ancho?", "Which interval is usually wider?", "Hvilket interval er normalt bredere?"),
            (("a", ("Predicción individual", "Individual prediction", "Individuel prædiktion")), ("b", ("Confianza de la media", "Confidence for the mean", "Konfidens for middelværdien")), ("c", ("Ambos iguales", "Both equal", "Begge ens")), ("d", ("Ninguno", "Neither", "Ingen"))),
            "a",
            ("La predicción individual añade variabilidad residual.", "Individual prediction adds residual variability.", "Individuel prædiktion tilføjer residualvariation."),
        ),
        (
            "007",
            ("¿Qué función ajusta un modelo lineal en R?", "Which function fits a linear model in R?", "Hvilken funktion tilpasser en lineær model i R?"),
            (("a", ("lm", "lm", "lm")), ("b", ("cor", "cor", "cor")), ("c", ("mean", "mean", "mean")), ("d", ("table", "table", "table"))),
            "a",
            ("lm usa una fórmula para definir respuesta y predictores.", "lm uses a formula to define response and predictors.", "lm bruger en formel til at definere respons og prædiktorer."),
        ),
        (
            "008",
            ("¿Cuál es el principal riesgo de extrapolar?", "What is the main risk of extrapolation?", "Hvad er den største risiko ved ekstrapolation?"),
            (("a", ("La relación puede cambiar fuera del rango observado", "The relationship may change outside the observed range", "Relationen kan ændre sig uden for det observerede område")), ("b", ("R² siempre aumenta", "R² always increases", "R² stiger altid")), ("c", ("La pendiente se vuelve causal", "The slope becomes causal", "Hældningen bliver kausal")), ("d", ("El error desaparece", "Error disappears", "Fejlen forsvinder"))),
            "a",
            ("El modelo está respaldado principalmente dentro del rango de datos.", "The model is mainly supported within the data range.", "Modellen er primært understøttet inden for dataområdet."),
        ),
    ),
    true_false=(
        ("009", ("Una correlación alta demuestra causalidad.", "A high correlation proves causation.", "En høj korrelation beviser kausalitet."), False, ("La causalidad requiere diseño y supuestos adicionales.", "Causation requires additional design and assumptions.", "Kausalitet kræver yderligere design og antagelser.")),
        ("010", ("Pearson es sensible a valores extremos.", "Pearson is sensitive to outliers.", "Pearson er følsom over for ekstreme værdier."), True, ("Los extremos pueden cambiar fuertemente la covariación y las desviaciones.", "Outliers can strongly change covariance and deviations.", "Ekstreme værdier kan ændre kovarians og afvigelser markant.")),
        ("011", ("Correlación cero descarta cualquier relación.", "Zero correlation rules out any relationship.", "Nulkorrelation udelukker enhver relation."), False, ("Puede existir una relación no lineal.", "A nonlinear relationship may exist.", "Der kan eksistere en ikke-lineær relation.")),
        ("012", ("La pendiente conserva unidades de Y por unidad de X.", "The slope retains units of Y per X unit.", "Hældningen bevarer enheder af Y pr. X-enhed."), True, ("Por eso debe reportarse con unidades.", "That is why it should be reported with units.", "Derfor bør den rapporteres med enheder.")),
        ("013", ("R² mide validez causal.", "R² measures causal validity.", "R² måler kausal gyldighed."), False, ("R² describe ajuste muestral.", "R² describes sample fit.", "R² beskriver tilpasning i stikprøven.")),
        ("014", ("Un intervalo de predicción suele incluir más incertidumbre que uno para la media.", "A prediction interval usually includes more uncertainty than an interval for the mean.", "Et prædiktionsinterval indeholder normalt mere usikkerhed end et interval for middelværdien."), True, ("Incluye variabilidad individual además de incertidumbre de la media.", "It includes individual variability in addition to mean uncertainty.", "Det inkluderer individuel variation ud over usikkerheden på middelværdien.")),
        ("015", ("El intercepto siempre tiene una interpretación científica útil.", "The intercept always has a useful scientific interpretation.", "Skæringen har altid en nyttig videnskabelig fortolkning."), False, ("Puede corresponder a X=0 fuera del rango o sin significado.", "It may correspond to X=0 outside the range or without meaning.", "Den kan svare til X=0 uden for området eller uden betydning.")),
        ("016", ("La inspección gráfica sigue siendo necesaria aunque se calcule una correlación.", "Graphical inspection remains necessary even when a correlation is calculated.", "Grafisk inspektion er stadig nødvendig, selv når en korrelation beregnes."), True, ("Los gráficos muestran forma, grupos y valores extremos.", "Plots reveal shape, groups, and outliers.", "Plots viser form, grupper og ekstreme værdier.")),
    ),
    tutor=(
        (
            "La correlación resume asociación, mientras que la regresión lineal simple modela la media esperada de una respuesta mediante una pendiente interpretable. Ninguna de las dos establece causalidad sin diseño y supuestos adicionales.",
            "Correlation summarises association, whereas simple linear regression models an expected response mean through an interpretable slope. Neither establishes causation without additional design and assumptions.",
            "Korrelation opsummerer association, mens simpel lineær regression modellerer den forventede middelrespons gennem en fortolkelig hældning. Ingen af delene fastslår kausalitet uden yderligere design og antagelser.",
        ),
        (
            ("Pearson resume linealidad; Spearman resume monotonicidad por rangos.", "Pearson summarises linearity; Spearman summarises rank monotonicity.", "Pearson opsummerer lineæritet; Spearman opsummerer monoton rangassociation."),
            ("La pendiente debe interpretarse con unidades y rango.", "The slope should be interpreted with units and range.", "Hældningen bør fortolkes med enheder og område."),
            ("R² no mide causalidad.", "R² does not measure causation.", "R² måler ikke kausalitet."),
            ("Predicción individual y media requieren intervalos distintos.", "Individual and mean prediction require different intervals.", "Individuel prædiktion og middelprædiktion kræver forskellige intervaller."),
        ),
        (
            ("Convertir correlación en causalidad.", "Turning correlation into causation.", "At gøre korrelation til kausalitet."),
            ("Interpretar la pendiente sin unidades.", "Interpreting slope without units.", "At fortolke hældningen uden enheder."),
            ("Extrapolar sin justificar.", "Extrapolating without justification.", "At ekstrapolere uden begrundelse."),
        ),
        (
            ("¿La relación es lineal o solo monótona?", "Is the relationship linear or only monotonic?", "Er relationen lineær eller kun monoton?"),
            ("¿X=0 tiene significado?", "Is X=0 meaningful?", "Har X=0 en betydning?"),
            ("¿Se predice una media o un individuo?", "Are you predicting a mean or an individual?", "Prædikerer du en middelværdi eller et individ?"),
        ),
        (
            ("Distingue asociación y causalidad.", "Distinguishes association and causation.", "Skelner mellem association og kausalitet."),
            ("Interpreta pendiente, intervalo y R².", "Interprets slope, interval, and R².", "Fortolker hældning, interval og R²."),
            ("Limita predicción y extrapolación al soporte de datos.", "Limits prediction and extrapolation to data support.", "Begrænser prædiktion og ekstrapolation til dataunderstøttelsen."),
        ),
        (
            ("No inventar causalidad ni mecanismos.", "Do not invent causation or mechanisms.", "Opfind ikke kausalitet eller mekanismer."),
            ("No interpretar R² como probabilidad.", "Do not interpret R² as a probability.", "Fortolk ikke R² som en sandsynlighed."),
            ("Responder en el idioma activo.", "Respond in the active language.", "Svar på det aktive sprog."),
        ),
        (
            "SDU ODIN BMB830 active course description approved 2025-03-06",
            "R base stats documentation: cor, cor.test, lm, predict.lm",
            "Standard linear-model definitions and interpretation",
        ),
    ),
)

LOCALIZED_MODULE_07_CORRELATION_REGRESSION = build_module(_SPEC)
LOCALIZED_OBJECTIVE_QUESTION_BANK_07 = build_question_bank(_SPEC)
MODULE_07_CORRELATION_REGRESSION: LearningModule = (
    LOCALIZED_MODULE_07_CORRELATION_REGRESSION.materialize(AppLocale.SPANISH_SPAIN)
)
OBJECTIVE_QUESTION_BANK_07: tuple[AssessmentItem, ...] = materialize_bank(
    LOCALIZED_OBJECTIVE_QUESTION_BANK_07
)


def materialize_module_07_question_bank(
    locale: AppLocale | str = AppLocale.SPANISH_SPAIN,
) -> tuple[AssessmentItem, ...]:
    """Return the module-7 objective bank in one locale."""

    return materialize_bank(LOCALIZED_OBJECTIVE_QUESTION_BANK_07, locale)


__all__ = [
    "LOCALIZED_MODULE_07_CORRELATION_REGRESSION",
    "LOCALIZED_OBJECTIVE_QUESTION_BANK_07",
    "MODULE_07_CORRELATION_REGRESSION",
    "OBJECTIVE_QUESTION_BANK_07",
    "materialize_module_07_question_bank",
]
