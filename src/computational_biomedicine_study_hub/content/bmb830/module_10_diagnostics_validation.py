"""BMB830 module 10: model diagnostics and validation."""

from __future__ import annotations

from ...i18n import AppLocale
from ..models import AssessmentItem, LearningModule
from .standard import StandardModuleSpec, build_module, build_question_bank, materialize_bank

_SPEC = StandardModuleSpec(
    module_id="bmb830.m10",
    title=(
        "Diagnóstico y validación de modelos",
        "Model diagnostics and validation",
        "Modeldiagnostik og validering",
    ),
    summary=(
        "Evalúa supuestos, identifica observaciones influyentes y separa ajuste aparente de capacidad de generalización mediante diagnósticos y validación reproducible.",
        "Evaluate assumptions, identify influential observations, and separate apparent fit from generalisation using reproducible diagnostics and validation.",
        "Vurdér antagelser, identificér indflydelsesrige observationer, og adskil tilsyneladende tilpasning fra generalisering med reproducerbar diagnostik og validering.",
    ),
    objectives=(
        (
            "m10.o1",
            (
                "Interpretar residuos y valores ajustados para evaluar linealidad, varianza constante e independencia.",
                "Interpret residuals and fitted values to assess linearity, constant variance, and independence.",
                "Fortolke residualer og tilpassede værdier for at vurdere linearitet, konstant varians og uafhængighed.",
            ),
        ),
        (
            "m10.o2",
            (
                "Distinguir valores extremos, leverage e influencia mediante diagnósticos complementarios.",
                "Distinguish outliers, leverage, and influence using complementary diagnostics.",
                "Skelne mellem ekstreme værdier, leverage og indflydelse med komplementære diagnostikker.",
            ),
        ),
        (
            "m10.o3",
            (
                "Comparar modelos según objetivo científico, complejidad, ajuste y rendimiento fuera de muestra.",
                "Compare models according to scientific purpose, complexity, fit, and out-of-sample performance.",
                "Sammenligne modeller efter videnskabeligt formål, kompleksitet, tilpasning og præstation uden for stikprøven.",
            ),
        ),
        (
            "m10.o4",
            (
                "Diseñar una validación reproducible que evite fuga de información y conclusiones exageradas.",
                "Design reproducible validation that avoids information leakage and exaggerated conclusions.",
                "Designe reproducerbar validering, der undgår informationslækage og overdrevne konklusioner.",
            ),
        ),
    ),
    concepts=(
        (
            "residual-patterns",
            (
                "Residuos y supuestos",
                "Residuals and assumptions",
                "Residualer og antagelser",
            ),
            (
                "Un residuo es la diferencia entre la respuesta observada y la ajustada. Un gráfico de residuos frente a valores ajustados ayuda a detectar curvatura, heterocedasticidad y estructura no modelada. La independencia procede principalmente del diseño; no puede demostrarse solo con un gráfico.",
                "A residual is the difference between observed and fitted response. A residual-versus-fitted plot helps reveal curvature, heteroscedasticity, and unmodelled structure. Independence comes primarily from design and cannot be established by a plot alone.",
                "En residual er forskellen mellem observeret og tilpasset respons. Et plot af residualer mod tilpassede værdier kan afsløre krumning, heteroskedasticitet og umodelleret struktur. Uafhængighed kommer primært fra designet og kan ikke fastslås alene med et plot.",
            ),
            (
                (
                    "La normalidad de errores afecta sobre todo la inferencia en muestras pequeñas, no la existencia del ajuste lineal.",
                    "Error normality mainly affects small-sample inference, not the existence of the linear fit.",
                    "Normalitet af fejl påvirker især inferens i små stikprøver, ikke selve den lineære tilpasning.",
                ),
                (
                    "Un patrón en embudo sugiere que la variabilidad cambia con el nivel ajustado.",
                    "A funnel pattern suggests variability changes with the fitted level.",
                    "Et tragtmønster antyder, at variationen ændres med det tilpassede niveau.",
                ),
            ),
        ),
        (
            "influence",
            (
                "Leverage, residuos e influencia",
                "Leverage, residuals, and influence",
                "Leverage, residualer og indflydelse",
            ),
            (
                "Leverage mide cuán inusual es una combinación de predictores. Un residuo studentizado grande indica discrepancia en la respuesta. La distancia de Cook resume cuánto puede cambiar el ajuste al eliminar una observación. Ningún umbral automático justifica borrar datos sin revisar medición, diseño y sensibilidad.",
                "Leverage measures how unusual a predictor combination is. A large studentised residual indicates response discrepancy. Cook's distance summarises how much the fit may change when an observation is removed. No automatic threshold justifies deleting data without reviewing measurement, design, and sensitivity.",
                "Leverage måler, hvor usædvanlig en kombination af prædiktorer er. En stor studentiseret residual viser afvigelse i responsen. Cooks afstand opsummerer, hvor meget tilpasningen kan ændres, når en observation fjernes. Ingen automatisk grænse retfærdiggør sletning uden vurdering af måling, design og følsomhed.",
            ),
            (
                (
                    "Alto leverage no implica necesariamente alta influencia.",
                    "High leverage does not necessarily imply high influence.",
                    "Høj leverage indebærer ikke nødvendigvis høj indflydelse.",
                ),
                (
                    "El análisis de sensibilidad compara conclusiones con y sin observaciones justificadamente cuestionadas.",
                    "Sensitivity analysis compares conclusions with and without legitimately questioned observations.",
                    "Følsomhedsanalyse sammenligner konklusioner med og uden legitimt tvivlsomme observationer.",
                ),
            ),
        ),
        (
            "model-comparison",
            (
                "Comparación responsable de modelos",
                "Responsible model comparison",
                "Ansvarlig modelsammenligning",
            ),
            (
                "Un modelo más complejo casi siempre reduce el error de entrenamiento. La comparación debe considerar la pregunta científica, modelos anidados o no anidados, penalización por complejidad, incertidumbre y rendimiento fuera de muestra. Un valor p o R² aislado no define el mejor modelo.",
                "A more complex model almost always lowers training error. Comparison should consider the scientific question, nested or non-nested structure, complexity penalties, uncertainty, and out-of-sample performance. A single p-value or R-squared does not define the best model.",
                "En mere kompleks model reducerer næsten altid træningsfejlen. Sammenligning bør overveje det videnskabelige spørgsmål, indlejrede eller ikke-indlejrede modeller, kompleksitetsstraf, usikkerhed og præstation uden for stikprøven. En enkelt p-værdi eller R-kvadrat definerer ikke den bedste model.",
            ),
            (
                (
                    "La comparación anidada requiere que el modelo reducido sea un caso especial del completo.",
                    "Nested comparison requires the reduced model to be a special case of the full model.",
                    "Indlejret sammenligning kræver, at den reducerede model er et specialtilfælde af den fulde model.",
                ),
                (
                    "La parsimonia limita complejidad que no mejora la decisión o la generalización.",
                    "Parsimony limits complexity that does not improve decisions or generalisation.",
                    "Parsimoni begrænser kompleksitet, der ikke forbedrer beslutninger eller generalisering.",
                ),
            ),
        ),
        (
            "validation",
            (
                "Validación y fuga de información",
                "Validation and information leakage",
                "Validering og informationslækage",
            ),
            (
                "La validación estima el rendimiento en datos no utilizados para ajustar el modelo. Cualquier transformación, selección de variables o ajuste de hiperparámetros que use información del conjunto de prueba produce fuga de información. Con pocos datos, la validación cruzada reutiliza observaciones de forma estructurada, pero no elimina sesgo de selección ni sustituye una cohorte externa.",
                "Validation estimates performance on data not used to fit the model. Any transformation, variable selection, or tuning that uses test-set information creates leakage. With limited data, cross-validation reuses observations in a structured way, but it does not remove selection bias or replace an external cohort.",
                "Validering estimerer præstation på data, der ikke blev brugt til at tilpasse modellen. Transformation, variabelvalg eller tuning, der bruger information fra testsættet, skaber lækage. Ved få data genbruger krydsvalidering observationer struktureret, men fjerner ikke selektionsbias og erstatter ikke en ekstern kohorte.",
            ),
            (
                (
                    "La partición debe respetar pacientes, centros, tiempo y otras unidades de dependencia.",
                    "Splitting must respect patients, centres, time, and other dependence units.",
                    "Opdeling skal respektere patienter, centre, tid og andre afhængighedsenheder.",
                ),
                (
                    "El rendimiento debe acompañarse de incertidumbre y una definición explícita de la métrica.",
                    "Performance should include uncertainty and an explicit metric definition.",
                    "Præstation bør ledsages af usikkerhed og en eksplicit definition af metrikken.",
                ),
            ),
        ),
    ),
    examples=(
        (
            "m10.e01",
            (
                "Diagnóstico de influencia",
                "Influence diagnostics",
                "Indflydelsesdiagnostik",
            ),
            (
                "Identifica la observación con mayor distancia de Cook y examina su leverage.",
                "Identify the observation with the largest Cook's distance and inspect its leverage.",
                "Identificér observationen med størst Cooks afstand, og undersøg dens leverage.",
            ),
            (
                (
                    "La última respuesta se aparta de la tendencia y ocurre en el extremo de x.",
                    "The final response departs from the trend and occurs at the edge of x.",
                    "Det sidste respons afviger fra tendensen og ligger ved kanten af x.",
                ),
                (
                    "Cook combina discrepancia residual y posición en el espacio de predictores.",
                    "Cook combines residual discrepancy and predictor-space position.",
                    "Cook kombinerer residualafvigelse og position i prædiktorrummet.",
                ),
            ),
            """x <- 1:6
response <- c(1, 2, 3, 4, 5, 8)
fit <- lm(response ~ x)
leverage <- hatvalues(fit)
cook <- cooks.distance(fit)
index <- which.max(cook)
cat(sprintf("most_influential=%d\n", index))
cat(sprintf("leverage=%.3f\n", leverage[[index]]))
cat(sprintf("cook=%.3f", cook[[index]]))
""",
            """most_influential=6
leverage=0.524
cook=2.200""",
            (
                "La observación 6 merece revisión y análisis de sensibilidad, pero el diagnóstico por sí solo no autoriza eliminarla.",
                "Observation 6 deserves review and sensitivity analysis, but the diagnostic alone does not authorise deletion.",
                "Observation 6 bør undersøges og indgå i en følsomhedsanalyse, men diagnostikken alene berettiger ikke sletning.",
            ),
        ),
        (
            "m10.e02",
            (
                "Error de entrenamiento frente a validación",
                "Training error versus validation",
                "Træningsfejl kontra validering",
            ),
            (
                "Ajusta modelos lineal y cuadrático en siete observaciones y evalúalos en tres observaciones reservadas.",
                "Fit linear and quadratic models on seven observations and evaluate them on three held-out observations.",
                "Tilpas lineære og kvadratiske modeller på syv observationer, og evaluér dem på tre hold-out-observationer.",
            ),
            (
                (
                    "El conjunto de prueba no participa en el ajuste.",
                    "The test set does not participate in fitting.",
                    "Testsættet deltager ikke i tilpasningen.",
                ),
                (
                    "RMSE se calcula con la misma escala de respuesta para ambos modelos.",
                    "RMSE is calculated on the same response scale for both models.",
                    "RMSE beregnes på samme responsskala for begge modeller.",
                ),
            ),
            """data <- data.frame(x = 1:10, response = (1:10)^2)
train <- data[data$x <= 7, ]
test <- data[data$x > 7, ]
linear <- lm(response ~ x, data = train)
quadratic <- lm(response ~ x + I(x^2), data = train)
linear_rmse <- sqrt(mean((test$response - predict(linear, newdata = test))^2))
quadratic_rmse <- sqrt(mean((test$response - predict(quadratic, newdata = test))^2))
cat(sprintf("linear_rmse=%.3f\n", linear_rmse))
cat(sprintf("quadratic_rmse=%.3f", quadratic_rmse))
""",
            """linear_rmse=23.159
quadratic_rmse=0.000""",
            (
                "En este ejemplo construido, la forma cuadrática generaliza exactamente. En datos reales, la comparación necesita incertidumbre, repetición y protección frente a fuga de información.",
                "In this constructed example, the quadratic form generalises exactly. Real data require uncertainty, repetition, and protection against leakage.",
                "I dette konstruerede eksempel generaliserer den kvadratiske form præcist. Virkelige data kræver usikkerhed, gentagelse og beskyttelse mod lækage.",
            ),
        ),
    ),
    practices=(
        (
            "m10.p01",
            "DATA_INTERPRETATION",
            (
                "Un gráfico de residuos frente a ajustados muestra un embudo. ¿Qué supuesto cuestiona y qué debes investigar?",
                "A residual-versus-fitted plot shows a funnel. Which assumption is questioned and what should you investigate?",
                "Et plot af residualer mod tilpassede værdier viser en tragt. Hvilken antagelse udfordres, og hvad bør undersøges?",
            ),
            (("Relaciona dispersión vertical con nivel ajustado.", "Relate vertical spread to fitted level.", "Relatér lodret spredning til det tilpassede niveau."),),
            (
                "Sugiere heterocedasticidad; revisar escala, proceso de medición, grupos omitidos, especificación de varianza y métodos robustos.",
                "It suggests heteroscedasticity; inspect scale, measurement process, omitted groups, variance specification, and robust methods.",
                "Det antyder heteroskedasticitet; undersøg skala, måleproces, udeladte grupper, variansspecifikation og robuste metoder.",
            ),
            (
                "La respuesta no consiste en transformar automáticamente hasta obtener un gráfico plano.",
                "The answer is not to transform automatically until the plot looks flat.",
                "Svaret er ikke automatisk at transformere, indtil plottet ser fladt ud.",
            ),
            "",
        ),
        (
            "m10.p02",
            "CODE_COMPLETION",
            (
                "Completa el cálculo de leverage y distancia de Cook para un modelo fit.",
                "Complete the calculation of leverage and Cook's distance for a fitted model.",
                "Fuldfør beregningen af leverage og Cooks afstand for en tilpasset model.",
            ),
            (("Usa funciones diagnósticas de stats.", "Use diagnostic functions from stats.", "Brug diagnostiske funktioner fra stats."),),
            ("hatvalues(fit)\ncooks.distance(fit)",) * 3,
            (
                "Los dos diagnósticos describen propiedades diferentes y deben interpretarse juntos.",
                "The diagnostics describe different properties and should be interpreted together.",
                "Diagnostikkerne beskriver forskellige egenskaber og bør fortolkes sammen.",
            ),
            "leverage <- __________________\ncook <- __________________",
        ),
        (
            "m10.p03",
            "DEBUGGING",
            (
                "Corrige la regla: eliminar toda observación con distancia de Cook mayor que 4/n.",
                "Correct the rule: delete every observation with Cook's distance greater than 4/n.",
                "Ret reglen: slet enhver observation med Cooks afstand større end 4/n.",
            ),
            (("Un umbral es una señal, no una orden.", "A threshold is a signal, not an order.", "En grænse er et signal, ikke en ordre."),),
            (
                "Usar el umbral para revisión; comprobar errores de medición, diseño y plausibilidad; realizar análisis de sensibilidad y documentar cualquier exclusión.",
                "Use the threshold for review; check measurement errors, design, and plausibility; perform sensitivity analysis and document any exclusion.",
                "Brug grænsen til gennemgang; kontrollér målefejl, design og plausibilitet; udfør følsomhedsanalyse og dokumentér enhver udelukkelse.",
            ),
            (
                "Borrar por diagnóstico puede ocultar biología real o introducir sesgo.",
                "Deleting by diagnostic may hide real biology or introduce bias.",
                "Sletning efter diagnostik kan skjule reel biologi eller indføre bias.",
            ),
            "",
        ),
        (
            "m10.p04",
            "PIPELINE_DESIGN",
            (
                "Diseña una validación para muestras repetidas por paciente y procedentes de dos hospitales.",
                "Design validation for repeated samples per patient from two hospitals.",
                "Design validering for gentagne prøver pr. patient fra to hospitaler.",
            ),
            (("La unidad de partición no puede ser cada fila.", "The split unit cannot be each row.", "Opdelingsenheden kan ikke være hver række."),),
            (
                "Agrupar todas las muestras de un paciente en la misma partición; evaluar separación por hospital o validación externa; ajustar transformaciones solo en entrenamiento; fijar métrica y reportar incertidumbre.",
                "Keep all samples from one patient in the same split; evaluate hospital-based or external validation; fit transformations only on training data; define the metric and report uncertainty.",
                "Hold alle prøver fra én patient i samme opdeling; vurder hospitalsbaseret eller ekstern validering; tilpas transformationer kun på træningsdata; definér metrikken og rapportér usikkerhed.",
            ),
            (
                "Separar filas al azar permitiría que información del mismo paciente aparezca en entrenamiento y prueba.",
                "Random row splitting would allow information from the same patient in training and test sets.",
                "Tilfældig rækkeopdeling ville tillade information fra samme patient i både trænings- og testsæt.",
            ),
            "",
        ),
        (
            "m10.p05",
            "ORAL_EXPLANATION",
            (
                "Explica por qué el error de entrenamiento no estima por sí solo la generalización.",
                "Explain why training error alone does not estimate generalisation.",
                "Forklar hvorfor træningsfejl alene ikke estimerer generalisering.",
            ),
            (("El modelo fue elegido usando esos mismos datos.", "The model was chosen using those same data.", "Modellen blev valgt med de samme data."),),
            (
                "El ajuste optimiza el rendimiento sobre entrenamiento y puede aprender ruido; se necesitan datos no usados o resampling correctamente anidado para estimar rendimiento futuro.",
                "Fitting optimises training performance and may learn noise; unused data or correctly nested resampling are needed to estimate future performance.",
                "Tilpasning optimerer træningspræstation og kan lære støj; ubrugte data eller korrekt indlejret resampling kræves for at estimere fremtidig præstation.",
            ),
            (
                "La diferencia entre ambos errores aumenta con sobreajuste.",
                "The gap between the errors grows with overfitting.",
                "Forskellen mellem fejlene vokser ved overtilpasning.",
            ),
            "",
        ),
        (
            "m10.p06",
            "DATA_INTERPRETATION",
            (
                "Una observación tiene leverage alto pero residuo casi cero. ¿Es necesariamente influyente?",
                "An observation has high leverage but a near-zero residual. Is it necessarily influential?",
                "En observation har høj leverage men næsten nul residual. Er den nødvendigvis indflydelsesrig?",
            ),
            (("Influencia combina posición y discrepancia.", "Influence combines position and discrepancy.", "Indflydelse kombinerer position og afvigelse."),),
            (
                "No. Puede estar lejos en el espacio de predictores pero ajustarse a la tendencia; revisar Cook, cambios de coeficientes y sensibilidad.",
                "No. It may be remote in predictor space but align with the trend; inspect Cook's distance, coefficient changes, and sensitivity.",
                "Nej. Den kan ligge langt væk i prædiktorrummet men følge tendensen; undersøg Cooks afstand, koefficientændringer og følsomhed.",
            ),
            (
                "Leverage alto crea potencial de influencia, no influencia automática.",
                "High leverage creates potential influence, not automatic influence.",
                "Høj leverage skaber potentiale for indflydelse, ikke automatisk indflydelse.",
            ),
            "",
        ),
    ),
    mcqs=(
        (
            "001",
            ("¿Qué muestra un residuo?", "What does a residual represent?", "Hvad repræsenterer en residual?"),
            (("a", ("Observado menos ajustado", "Observed minus fitted", "Observeret minus tilpasset")), ("b", ("Solo error de medición", "Measurement error only", "Kun målefejl")), ("c", ("Probabilidad del modelo", "Model probability", "Modelsandsynlighed")), ("d", ("Leverage", "Leverage", "Leverage"))),
            "a",
            ("El residuo combina discrepancias de datos y modelo.", "The residual combines data and model discrepancies.", "Residualen kombinerer afvigelser i data og model."),
        ),
        (
            "002",
            ("¿Qué sugiere un embudo en residuos frente a ajustados?", "What does a funnel in residuals versus fitted suggest?", "Hvad antyder en tragt i residualer mod tilpassede værdier?"),
            (("a", ("Heterocedasticidad", "Heteroscedasticity", "Heteroskedasticitet")), ("b", ("Causalidad", "Causality", "Kausalitet")), ("c", ("Independencia demostrada", "Proven independence", "Bevist uafhængighed")), ("d", ("Ausencia de extremos", "No outliers", "Ingen ekstreme værdier"))),
            "a",
            ("La dispersión cambia con el nivel ajustado.", "Spread changes with fitted level.", "Spredningen ændres med det tilpassede niveau."),
        ),
        (
            "003",
            ("¿Qué mide leverage?", "What does leverage measure?", "Hvad måler leverage?"),
            (("a", ("Posición inusual de predictores", "Unusual predictor position", "Usædvanlig prædiktorposition")), ("b", ("Tamaño del residuo únicamente", "Residual size only", "Kun residualens størrelse")), ("c", ("Error de prueba", "Test error", "Testfejl")), ("d", ("Normalidad", "Normality", "Normalitet"))),
            "a",
            ("Leverage depende de la matriz de diseño.", "Leverage depends on the design matrix.", "Leverage afhænger af designmatricen."),
        ),
        (
            "004",
            ("¿Qué combina la distancia de Cook?", "What does Cook's distance combine?", "Hvad kombinerer Cooks afstand?"),
            (("a", ("Discrepancia y leverage", "Discrepancy and leverage", "Afvigelse og leverage")), ("b", ("Solo tamaño muestral", "Sample size only", "Kun stikprøvestørrelse")), ("c", ("Solo R²", "R-squared only", "Kun R-kvadrat")), ("d", ("Solo normalidad", "Normality only", "Kun normalitet"))),
            "a",
            ("Resume potencial de cambio del ajuste al omitir una observación.", "It summarises potential fit change when omitting an observation.", "Den opsummerer potentiel ændring i tilpasningen ved udeladelse af en observation."),
        ),
        (
            "005",
            ("¿Qué estima un conjunto de prueba intacto?", "What does an untouched test set estimate?", "Hvad estimerer et uberørt testsæt?"),
            (("a", ("Rendimiento fuera de muestra", "Out-of-sample performance", "Præstation uden for stikprøven")), ("b", ("Error de entrenamiento", "Training error", "Træningsfejl")), ("c", ("Causalidad", "Causality", "Kausalitet")), ("d", ("Leverage", "Leverage", "Leverage"))),
            "a",
            ("No participó en selección ni ajuste.", "It did not participate in selection or fitting.", "Det deltog ikke i valg eller tilpasning."),
        ),
        (
            "006",
            ("¿Qué constituye fuga de información?", "What constitutes information leakage?", "Hvad udgør informationslækage?"),
            (("a", ("Normalizar usando todo el conjunto antes de dividir", "Normalising with all data before splitting", "Normalisering med alle data før opdeling")), ("b", ("Fijar una métrica previamente", "Predefining a metric", "Foruddefinere en metrik")), ("c", ("Reservar pacientes completos", "Holding out complete patients", "Holde komplette patienter ude")), ("d", ("Documentar exclusiones", "Documenting exclusions", "Dokumentere udelukkelser"))),
            "a",
            ("La transformación usa información del futuro conjunto de prueba.", "The transformation uses information from the future test set.", "Transformationen bruger information fra det fremtidige testsæt."),
        ),
        (
            "007",
            ("¿Cuándo es válida una comparación ANOVA de modelos lm?", "When is an ANOVA comparison of lm models valid?", "Hvornår er en ANOVA-sammenligning af lm-modeller gyldig?"),
            (("a", ("Cuando son anidados y usan las mismas observaciones", "When nested and fitted to the same observations", "Når de er indlejrede og tilpasset de samme observationer")), ("b", ("Siempre que R² cambie", "Whenever R-squared changes", "Når R-kvadrat ændres")), ("c", ("Solo si ambos tienen igual número de parámetros", "Only with equal parameter counts", "Kun med samme antal parametre")), ("d", ("Solo con datos de prueba", "Only with test data", "Kun med testdata"))),
            "a",
            ("El modelo reducido debe ser un caso especial del completo.", "The reduced model must be a special case of the full model.", "Den reducerede model skal være et specialtilfælde af den fulde model."),
        ),
        (
            "008",
            ("¿Qué partición evita fuga con medidas repetidas?", "Which split avoids leakage with repeated measures?", "Hvilken opdeling undgår lækage ved gentagne målinger?"),
            (("a", ("Por paciente", "By patient", "Efter patient")), ("b", ("Por fila al azar", "Randomly by row", "Tilfældigt efter række")), ("c", ("Por variable", "By variable", "Efter variabel")), ("d", ("Después de seleccionar el modelo", "After model selection", "Efter modelvalg"))),
            "a",
            ("Todas las observaciones dependientes deben permanecer juntas.", "All dependent observations should remain together.", "Alle afhængige observationer bør forblive sammen."),
        ),
    ),
    true_false=(
        ("009", ("Un residuo grande demuestra que la observación es errónea.", "A large residual proves the observation is erroneous.", "En stor residual beviser, at observationen er forkert."), False, ("Puede reflejar error, biología real o especificación insuficiente.", "It may reflect error, real biology, or inadequate specification.", "Den kan afspejle fejl, reel biologi eller utilstrækkelig specifikation.")),
        ("010", ("La independencia depende principalmente del diseño.", "Independence depends primarily on design.", "Uafhængighed afhænger primært af designet."), True, ("Un gráfico no puede crear independencia ausente.", "A plot cannot create missing independence.", "Et plot kan ikke skabe manglende uafhængighed.")),
        ("011", ("Alto leverage implica siempre alta distancia de Cook.", "High leverage always implies high Cook's distance.", "Høj leverage indebærer altid stor Cooks afstand."), False, ("También se necesita discrepancia residual.", "Residual discrepancy is also needed.", "Residualafvigelse er også nødvendig.")),
        ("012", ("Eliminar puntos por un umbral diagnóstico puede introducir sesgo.", "Deleting points by a diagnostic threshold can introduce bias.", "Sletning af punkter efter en diagnostisk grænse kan indføre bias."), True, ("La exclusión requiere justificación y sensibilidad.", "Exclusion requires justification and sensitivity analysis.", "Udelukkelse kræver begrundelse og følsomhedsanalyse.")),
        ("013", ("El error de entrenamiento suele disminuir al añadir parámetros.", "Training error usually decreases when parameters are added.", "Træningsfejl falder normalt, når parametre tilføjes."), True, ("Esto no garantiza mejor generalización.", "This does not guarantee better generalisation.", "Det garanterer ikke bedre generalisering.")),
        ("014", ("Seleccionar variables usando el conjunto de prueba mantiene una validación imparcial.", "Selecting variables using the test set preserves unbiased validation.", "Variabelvalg med testsættet bevarer upartisk validering."), False, ("Contamina la estimación de rendimiento.", "It contaminates the performance estimate.", "Det forurener præstationsestimatet.")),
        ("015", ("La validación cruzada sustituye siempre una cohorte externa.", "Cross-validation always replaces an external cohort.", "Krydsvalidering erstatter altid en ekstern kohorte."), False, ("No evalúa todos los cambios de población o procedimiento.", "It does not assess every population or process shift.", "Den vurderer ikke alle ændringer i population eller procedure.")),
        ("016", ("La métrica de validación debe corresponder al uso previsto del modelo.", "The validation metric should match the model's intended use.", "Valideringsmetrikken bør passe til modellens tilsigtede brug."), True, ("Una métrica irrelevante puede premiar el modelo equivocado.", "An irrelevant metric may reward the wrong model.", "En irrelevant metrik kan belønne den forkerte model.")),
    ),
    tutor=(
        (
            "El diagnóstico de modelos combina residuos, estructura del diseño, influencia y validación fuera de muestra. Ningún gráfico, umbral o métrica aislada determina automáticamente si un modelo es válido.",
            "Model diagnosis combines residuals, design structure, influence, and out-of-sample validation. No single plot, threshold, or metric automatically determines model validity.",
            "Modeldiagnostik kombinerer residualer, designstruktur, indflydelse og validering uden for stikprøven. Intet enkelt plot, grænse eller metrik afgør automatisk modellens gyldighed.",
        ),
        (
            ("Residuos evalúan discrepancia, no solo error de medición.", "Residuals assess discrepancy, not only measurement error.", "Residualer vurderer afvigelse, ikke kun målefejl."),
            ("Leverage, residuo e influencia son conceptos distintos.", "Leverage, residual, and influence are distinct concepts.", "Leverage, residual og indflydelse er forskellige begreber."),
            ("La validación debe aislar todo el proceso de aprendizaje.", "Validation must isolate the entire learning process.", "Validering skal isolere hele læringsprocessen."),
            ("La comparación depende del objetivo científico.", "Comparison depends on the scientific purpose.", "Sammenligning afhænger af det videnskabelige formål."),
        ),
        (
            ("Eliminar observaciones automáticamente.", "Automatically deleting observations.", "Automatisk sletning af observationer."),
            ("Usar el conjunto de prueba durante el desarrollo.", "Using the test set during development.", "Brug af testsættet under udvikling."),
            ("Elegir por R² sin penalizar complejidad.", "Choosing by R-squared without considering complexity.", "Valg efter R-kvadrat uden hensyn til kompleksitet."),
        ),
        (
            ("¿Qué patrón exacto observas en los residuos?", "What exact residual pattern do you observe?", "Hvilket præcist residualmønster observerer du?"),
            ("¿La partición respeta la unidad experimental?", "Does the split respect the experimental unit?", "Respekterer opdelingen den eksperimentelle enhed?"),
            ("¿Cambian las conclusiones en sensibilidad?", "Do conclusions change in sensitivity analysis?", "Ændres konklusionerne i følsomhedsanalysen?"),
        ),
        (
            ("Interpreta diagnósticos conjuntamente.", "Interprets diagnostics jointly.", "Fortolker diagnostikker samlet."),
            ("Distingue entrenamiento y generalización.", "Distinguishes training and generalisation.", "Skelner mellem træning og generalisering."),
            ("Detecta y evita fuga de información.", "Detects and avoids information leakage.", "Opdager og undgår informationslækage."),
        ),
        (
            ("No ordenar borrar datos desde un umbral.", "Do not order data deletion from a threshold.", "Anbefal ikke datasletning ud fra en grænse."),
            ("No declarar validación externa a partir de resampling interno.", "Do not claim external validation from internal resampling.", "Erklær ikke ekstern validering ud fra intern resampling."),
            ("Responder en el idioma activo.", "Respond in the active language.", "Svar på det aktive sprog."),
        ),
        (
            "SDU ODIN BMB830 active course description approved 2025-03-06",
            "R base stats documentation: lm, residuals, fitted, hatvalues, cooks.distance, predict, anova",
            "Regression diagnostics and validation principles",
        ),
    ),
)

LOCALIZED_MODULE_10_DIAGNOSTICS_VALIDATION = build_module(_SPEC)
LOCALIZED_OBJECTIVE_QUESTION_BANK_10 = build_question_bank(_SPEC)
MODULE_10_DIAGNOSTICS_VALIDATION: LearningModule = (
    LOCALIZED_MODULE_10_DIAGNOSTICS_VALIDATION.materialize(AppLocale.SPANISH_SPAIN)
)
OBJECTIVE_QUESTION_BANK_10: tuple[AssessmentItem, ...] = materialize_bank(
    LOCALIZED_OBJECTIVE_QUESTION_BANK_10
)


def materialize_module_10_question_bank(
    locale: AppLocale | str = AppLocale.SPANISH_SPAIN,
) -> tuple[AssessmentItem, ...]:
    """Return the module-10 objective bank in one locale."""

    return materialize_bank(LOCALIZED_OBJECTIVE_QUESTION_BANK_10, locale)


__all__ = [
    "LOCALIZED_MODULE_10_DIAGNOSTICS_VALIDATION",
    "LOCALIZED_OBJECTIVE_QUESTION_BANK_10",
    "MODULE_10_DIAGNOSTICS_VALIDATION",
    "OBJECTIVE_QUESTION_BANK_10",
    "materialize_module_10_question_bank",
]
