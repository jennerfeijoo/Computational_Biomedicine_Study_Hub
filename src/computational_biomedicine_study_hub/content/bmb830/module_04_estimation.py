"""BMB830 module 4: estimation, uncertainty, and confidence intervals."""

from __future__ import annotations

from ...i18n import AppLocale
from ..models import AssessmentItem, LearningModule
from .standard import StandardModuleSpec, build_module, build_question_bank, materialize_bank

_SPEC = StandardModuleSpec(
    module_id="bmb830.m04",
    title=(
        "Estimación e intervalos de confianza",
        "Estimation and confidence intervals",
        "Estimation og konfidensintervaller",
    ),
    summary=(
        "Define estimandos, cuantifica error estándar y construye intervalos de confianza que separan precisión muestral de variabilidad biológica.",
        "Define estimands, quantify standard error, and construct confidence intervals that separate sampling precision from biological variability.",
        "Definér estimander, kvantificér standardfejl, og konstruér konfidensintervaller, der adskiller stikprævepræcision fra biologisk variation.",
    ),
    objectives=(
        (
            "m04.o1",
            (
                "Distinguir parámetro, estimando, estimador y estimación.",
                "Distinguish parameter, estimand, estimator, and estimate.",
                "Skelne mellem parameter, estimand, estimator og estimat.",
            ),
        ),
        (
            "m04.o2",
            (
                "Calcular e interpretar error estándar y distribución muestral.",
                "Calculate and interpret standard error and the sampling distribution.",
                "Beregne og fortolke standardfejl og stikprøvefordelingen.",
            ),
        ),
        (
            "m04.o3",
            (
                "Construir e interpretar intervalos de confianza para medias y proporciones.",
                "Construct and interpret confidence intervals for means and proportions.",
                "Konstruere og fortolke konfidensintervaller for middelværdier og proportioner.",
            ),
        ),
        (
            "m04.o4",
            (
                "Relacionar anchura del intervalo con variabilidad, tamaño muestral y nivel de confianza.",
                "Relate interval width to variability, sample size, and confidence level.",
                "Relatere intervalbredde til variation, stikprøvestørrelse og konfidensniveau.",
            ),
        ),
    ),
    concepts=(
        (
            "estimands",
            ("Estimando y estimador", "Estimand and estimator", "Estimand og estimator"),
            (
                "El estimando es la cantidad científica objetivo, por ejemplo una media poblacional o una diferencia de medias. El estimador es la regla aplicada a los datos y la estimación es el valor obtenido en la muestra.",
                "The estimand is the scientific target quantity, such as a population mean or mean difference. The estimator is the rule applied to the data, and the estimate is the value obtained in the sample.",
                "Estimanden er den videnskabelige målstørrelse, såsom et populationsgennemsnit eller en middelforskel. Estimatoren er reglen anvendt på data, og estimatet er værdien fra stikprøven.",
            ),
            (
                (
                    "El diseño define qué estimando es identificable.",
                    "The design determines which estimand is identifiable.",
                    "Designet bestemmer, hvilken estimand der kan identificeres.",
                ),
                (
                    "Una estimación puntual no expresa por sí sola su precisión.",
                    "A point estimate alone does not express precision.",
                    "Et punktestimat udtrykker ikke i sig selv præcision.",
                ),
            ),
        ),
        (
            "standard-error",
            ("Error estándar", "Standard error", "Standardfejl"),
            (
                "La desviación estándar describe dispersión entre observaciones; el error estándar describe dispersión del estimador entre muestras hipotéticas repetidas. Para una media independiente, SE = s/√n cuando las unidades son comparables e independientes.",
                "Standard deviation describes spread among observations; standard error describes spread of the estimator across hypothetical repeated samples. For an independent mean, SE = s/√n when units are comparable and independent.",
                "Standardafvigelsen beskriver spredning mellem observationer; standardfejlen beskriver estimatorens spredning på tværs af hypotetiske gentagne stikprøver. For et uafhængigt gennemsnit er SE = s/√n.",
            ),
            (
                (
                    "Más datos independientes suelen reducir el error estándar.",
                    "More independent data usually reduce standard error.",
                    "Flere uafhængige data reducerer normalt standardfejlen.",
                ),
                (
                    "La pseudorreplicación no aumenta el tamaño muestral efectivo.",
                    "Pseudoreplication does not increase effective sample size.",
                    "Pseudoreplikation øger ikke den effektive stikprøvestørrelse.",
                ),
            ),
        ),
        (
            "confidence-interval",
            (
                "Intervalo de confianza",
                "Confidence interval",
                "Konfidensinterval",
            ),
            (
                "Un procedimiento de intervalo del 95 % produce intervalos que contienen el parámetro verdadero en aproximadamente el 95 % de muestreos repetidos bajo el modelo. No significa que el parámetro fijo tenga una probabilidad posterior del 95 % de estar en este intervalo.",
                "A 95% interval procedure produces intervals containing the true parameter in about 95% of repeated samples under the model. It does not mean that the fixed parameter has a 95% posterior probability of lying in this realised interval.",
                "En 95 %-intervalprocedure giver intervaller, der indeholder den sande parameter i omtrent 95 % af gentagne stikprøver under modellen. Det betyder ikke, at den faste parameter har 95 % posterior sandsynlighed for at ligge i dette realiserede interval.",
            ),
            (
                (
                    "El intervalo combina estimación y precisión.",
                    "The interval combines estimate and precision.",
                    "Intervallet kombinerer estimat og præcision.",
                ),
                (
                    "La interpretación depende de los supuestos del procedimiento.",
                    "Interpretation depends on the procedure's assumptions.",
                    "Fortolkningen afhænger af procedurens antagelser.",
                ),
            ),
        ),
        (
            "interval-width",
            (
                "Anchura y diseño",
                "Width and design",
                "Bredde og design",
            ),
            (
                "Intervalos más estrechos requieren menor variabilidad, mayor tamaño muestral efectivo o menor nivel de confianza. Aumentar mediciones técnicas de la misma unidad no sustituye reclutar unidades biológicas independientes.",
                "Narrower intervals require lower variability, larger effective sample size, or a lower confidence level. Increasing technical measurements of the same unit does not replace recruiting independent biological units.",
                "Smallere intervaller kræver lavere variation, større effektiv stikprøvestørrelse eller lavere konfidensniveau. Flere tekniske målinger af samme enhed erstatter ikke uafhængige biologiske enheder.",
            ),
            (
                (
                    "Precisión no equivale a ausencia de sesgo.",
                    "Precision is not absence of bias.",
                    "Præcision er ikke det samme som fravær af bias.",
                ),
                (
                    "El intervalo debe reportarse junto con unidades y estimando.",
                    "The interval should be reported with units and estimand.",
                    "Intervallet bør rapporteres sammen med enheder og estimand.",
                ),
            ),
        ),
    ),
    examples=(
        (
            "m04.e01",
            (
                "Intervalo t para una media",
                "t interval for a mean",
                "t-interval for et gennemsnit",
            ),
            (
                "Estima la concentración media y su intervalo del 95 % en seis unidades independientes.",
                "Estimate the mean concentration and its 95% interval in six independent units.",
                "Estimér middelkoncentrationen og dens 95 %-interval i seks uafhængige enheder.",
            ),
            (
                (
                    "La desviación muestral estima la variabilidad entre unidades.",
                    "The sample deviation estimates variability among units.",
                    "Stikprøvens standardafvigelse estimerer variation mellem enheder.",
                ),
                (
                    "La distribución t incorpora la incertidumbre de estimar la desviación.",
                    "The t distribution incorporates uncertainty from estimating the deviation.",
                    "t-fordelingen indarbejder usikkerheden ved at estimere standardafvigelsen.",
                ),
            ),
            """x <- c(12.1, 11.8, 12.4, 12.0, 11.7, 12.3)
n <- length(x)
estimate <- mean(x)
se <- sd(x) / sqrt(n)
critical <- qt(0.975, df = n - 1)
ci <- estimate + c(-1, 1) * critical * se
cat(sprintf("mean=%.2f\n", estimate))
cat(sprintf("se=%.3f\n", se))
cat(sprintf("ci=[%.2f, %.2f]", ci[1], ci[2]))
""",
            """mean=12.05
se=0.112
ci=[11.76, 12.34]""",
            (
                "El intervalo expresa precisión de la media, no el rango esperado de observaciones individuales.",
                "The interval expresses precision of the mean, not the expected range of individual observations.",
                "Intervallet udtrykker præcisionen af gennemsnittet, ikke det forventede område for individuelle observationer.",
            ),
        ),
        (
            "m04.e02",
            (
                "Intervalo de Wilson para una proporción",
                "Wilson interval for a proportion",
                "Wilson-interval for en proportion",
            ),
            (
                "Estima la proporción de 42 respuestas positivas entre 60 unidades sin usar la aproximación simétrica ingenua.",
                "Estimate the proportion of 42 positive responses among 60 units without using the naive symmetric approximation.",
                "Estimér proportionen af 42 positive svar blandt 60 enheder uden den naive symmetriske approksimation.",
            ),
            (
                (
                    "La proporción muestral es el estimador puntual.",
                    "The sample proportion is the point estimator.",
                    "Stikprøveproportionen er punktestimatoren.",
                ),
                (
                    "Wilson mantiene mejor comportamiento cerca de los límites 0 y 1.",
                    "Wilson behaves better near the boundaries 0 and 1.",
                    "Wilson opfører sig bedre nær grænserne 0 og 1.",
                ),
            ),
            """positive <- 42
n <- 60
p_hat <- positive / n
z <- qnorm(0.975)
denominator <- 1 + z^2 / n
centre <- (p_hat + z^2 / (2 * n)) / denominator
half_width <- z * sqrt(p_hat * (1 - p_hat) / n + z^2 / (4 * n^2)) / denominator
ci <- centre + c(-1, 1) * half_width
cat(sprintf("p=%.2f\n", p_hat))
cat(sprintf("ci=[%.3f, %.3f]", ci[1], ci[2]))
""",
            """p=0.70
ci=[0.575, 0.801]""",
            (
                "La asimetría del intervalo refleja que una proporción está restringida entre cero y uno.",
                "The interval's asymmetry reflects that a proportion is constrained between zero and one.",
                "Intervallets asymmetri afspejler, at en proportion er begrænset mellem nul og ét.",
            ),
        ),
    ),
    practices=(
        (
            "m04.p01",
            "DATA_INTERPRETATION",
            (
                "Distingue parámetro, estimador y estimación al reportar una media muestral de 8,4.",
                "Distinguish parameter, estimator, and estimate when reporting a sample mean of 8.4.",
                "Skeln mellem parameter, estimator og estimat ved rapportering af et stikprøvegennemsnit på 8,4.",
            ),
            (("La media poblacional no se observa directamente.", "The population mean is not observed directly.", "Populationsgennemsnittet observeres ikke direkte."),),
            (
                "Parámetro: media poblacional; estimador: media muestral; estimación: 8,4.",
                "Parameter: population mean; estimator: sample mean; estimate: 8.4.",
                "Parameter: populationsgennemsnit; estimator: stikprøvegennemsnit; estimat: 8,4.",
            ),
            (
                "Los tres conceptos ocupan niveles distintos del proceso inferencial.",
                "The three concepts occupy different levels of the inferential process.",
                "De tre begreber ligger på forskellige niveauer i inferensprocessen.",
            ),
            "",
        ),
        (
            "m04.p02",
            "CODE_COMPLETION",
            (
                "Completa el cálculo del error estándar de una media independiente.",
                "Complete the standard-error calculation for an independent mean.",
                "Fuldfør beregningen af standardfejlen for et uafhængigt gennemsnit.",
            ),
            (("Usa la desviación muestral y el tamaño efectivo.", "Use the sample deviation and effective sample size.", "Brug stikprøvens standardafvigelse og den effektive stikprøvestørrelse."),),
            ("sd(x) / sqrt(length(x))",) * 3,
            (
                "El denominador es la raíz del número de unidades independientes.",
                "The denominator is the square root of independent units.",
                "Nævneren er kvadratroden af antallet af uafhængige enheder.",
            ),
            "se <- __________________________",
        ),
        (
            "m04.p03",
            "ORAL_EXPLANATION",
            (
                "Explica por qué un intervalo del 95 % no asigna probabilidad del 95 % al parámetro fijo.",
                "Explain why a 95% interval does not assign 95% probability to the fixed parameter.",
                "Forklar hvorfor et 95 %-interval ikke tildeler 95 % sandsynlighed til den faste parameter.",
            ),
            (("La aleatoriedad pertenece al procedimiento de muestreo.", "Randomness belongs to the sampling procedure.", "Tilfældigheden tilhører stikprøveproceduren."),),
            (
                "La cobertura del 95 % describe el rendimiento del procedimiento en muestreos repetidos.",
                "The 95% coverage describes procedure performance over repeated samples.",
                "95 %-dækningen beskriver procedurens ydelse over gentagne stikprøver.",
            ),
            (
                "Después de observar los datos, el intervalo concreto contiene o no contiene el parámetro.",
                "After observing data, the realised interval either contains the parameter or it does not.",
                "Efter data er observeret, indeholder det konkrete interval enten parameteren eller ikke.",
            ),
            "",
        ),
        (
            "m04.p04",
            "DATA_INTERPRETATION",
            (
                "Predice cómo cambia un intervalo al cuadruplicar el tamaño muestral efectivo con variabilidad constante.",
                "Predict how an interval changes when effective sample size is quadrupled at constant variability.",
                "Forudsig hvordan et interval ændres, når den effektive stikprøvestørrelse firedobles ved konstant variation.",
            ),
            (("El error estándar escala aproximadamente con 1/√n.", "Standard error scales approximately with 1/√n.", "Standardfejlen skalerer omtrent med 1/√n."),),
            (
                "El error estándar y la semianchura se reducen aproximadamente a la mitad.",
                "Standard error and half-width are reduced by about half.",
                "Standardfejlen og halvbredden reduceres omtrent til det halve.",
            ),
            (
                "La relación asume unidades adicionales independientes y el mismo diseño.",
                "The relation assumes additional independent units and the same design.",
                "Relationen antager yderligere uafhængige enheder og samme design.",
            ),
            "",
        ),
        (
            "m04.p05",
            "DEBUGGING",
            (
                "Corrige un informe que presenta media ± desviación estándar como intervalo de confianza.",
                "Correct a report that presents mean ± standard deviation as a confidence interval.",
                "Ret en rapport, der præsenterer gennemsnit ± standardafvigelse som konfidensinterval.",
            ),
            (("La desviación describe observaciones, no precisión del estimador.", "Deviation describes observations, not estimator precision.", "Standardafvigelsen beskriver observationer, ikke estimatorens præcision."),),
            (
                "Calcular SE y usar el cuantil apropiado; reportar SD por separado como dispersión.",
                "Calculate SE and use the appropriate quantile; report SD separately as spread.",
                "Beregn SE og brug den relevante fraktil; rapportér SD separat som spredning.",
            ),
            (
                "La corrección separa variabilidad biológica y precisión inferencial.",
                "The correction separates biological variability and inferential precision.",
                "Korrektionen adskiller biologisk variation og inferentiel præcision.",
            ),
            "",
        ),
        (
            "m04.p06",
            "PIPELINE_DESIGN",
            (
                "Diseña el reporte mínimo de una estimación de diferencia de medias.",
                "Design the minimum report for an estimated mean difference.",
                "Design minimumsrapporteringen for en estimeret middelforskel.",
            ),
            (("Incluye dirección, unidades e incertidumbre.", "Include direction, units, and uncertainty.", "Medtag retning, enheder og usikkerhed."),),
            (
                "Definir grupos y contraste, estimación con unidades, intervalo de confianza, tamaño muestral y supuestos.",
                "Define groups and contrast, estimate with units, confidence interval, sample size, and assumptions.",
                "Definér grupper og kontrast, estimat med enheder, konfidensinterval, stikprøvestørrelse og antagelser.",
            ),
            (
                "Un valor p aislado no describe magnitud ni precisión.",
                "A p-value alone does not describe magnitude or precision.",
                "En p-værdi alene beskriver hverken størrelse eller præcision.",
            ),
            "",
        ),
    ),
    mcqs=(
        (
            "001",
            ("¿Qué describe el error estándar de la media?", "What does the standard error of the mean describe?", "Hvad beskriver standardfejlen for gennemsnittet?"),
            (("a", ("Dispersión individual", "Individual spread", "Individuel spredning")), ("b", ("Precisión del estimador", "Estimator precision", "Estimatorens præcision")), ("c", ("Sesgo del diseño", "Design bias", "Designbias")), ("d", ("Rango total", "Total range", "Samlet variationsbredde"))),
            "b",
            ("El error estándar cuantifica variación muestral del estimador.", "Standard error quantifies sampling variation of the estimator.", "Standardfejlen kvantificerer estimatorens stikprøvevariation."),
        ),
        (
            "002",
            ("¿Qué hace más estrecho un intervalo, manteniendo lo demás constante?", "What narrows an interval, all else equal?", "Hvad gør et interval smallere, alt andet lige?"),
            (("a", ("Menor n", "Smaller n", "Mindre n")), ("b", ("Mayor n efectivo", "Larger effective n", "Større effektivt n")), ("c", ("Mayor confianza", "Higher confidence", "Højere konfidens")), ("d", ("Mayor variabilidad", "Higher variability", "Større variation"))),
            "b",
            ("Más unidades independientes reducen el error estándar.", "More independent units reduce standard error.", "Flere uafhængige enheder reducerer standardfejlen."),
        ),
        (
            "003",
            ("¿Cuál es la estimación en una media muestral de 8,4?", "What is the estimate when the sample mean is 8.4?", "Hvad er estimatet, når stikprøvegennemsnittet er 8,4?"),
            (("a", ("La media poblacional", "The population mean", "Populationsgennemsnittet")), ("b", ("8,4", "8.4", "8,4")), ("c", ("La fórmula de la media", "The mean formula", "Formlen for gennemsnittet")), ("d", ("El diseño", "The design", "Designet"))),
            "b",
            ("La estimación es el valor observado del estimador.", "The estimate is the observed value of the estimator.", "Estimatet er estimatorens observerede værdi."),
        ),
        (
            "004",
            ("¿Qué intervalo es adecuado para una media con desviación poblacional desconocida y n pequeño?", "Which interval suits a mean with unknown population deviation and small n?", "Hvilket interval passer til et gennemsnit med ukendt populationsafvigelse og lille n?"),
            (("a", ("Intervalo t", "t interval", "t-interval")), ("b", ("Rango", "Range", "Variationsbredde")), ("c", ("Media ± SD", "Mean ± SD", "Gennemsnit ± SD")), ("d", ("Solo estimación", "Estimate only", "Kun estimat"))),
            "a",
            ("La distribución t refleja estimación de la variabilidad.", "The t distribution reflects estimation of variability.", "t-fordelingen afspejler estimering af variationen."),
        ),
        (
            "005",
            ("¿Qué describe una desviación estándar?", "What does a standard deviation describe?", "Hvad beskriver en standardafvigelse?"),
            (("a", ("Precisión de la media", "Precision of the mean", "Præcisionen af gennemsnittet")), ("b", ("Dispersión entre observaciones", "Spread among observations", "Spredning mellem observationer")), ("c", ("Cobertura", "Coverage", "Dækning")), ("d", ("Sesgo", "Bias", "Bias"))),
            "b",
            ("SD resume dispersión observacional.", "SD summarises observational spread.", "SD opsummerer observationsspredning."),
        ),
        (
            "006",
            ("¿Qué debe acompañar a un intervalo de confianza?", "What should accompany a confidence interval?", "Hvad bør ledsage et konfidensinterval?"),
            (("a", ("Estimando y unidades", "Estimand and units", "Estimand og enheder")), ("b", ("Solo color", "Colour only", "Kun farve")), ("c", ("Solo valor p", "p-value only", "Kun p-værdi")), ("d", ("Workspace", "Workspace", "Workspace"))),
            "a",
            ("Sin estimando y unidades el intervalo es ambiguo.", "Without estimand and units the interval is ambiguous.", "Uden estimand og enheder er intervallet tvetydigt."),
        ),
        (
            "007",
            ("¿Qué aumenta la cobertura nominal?", "What increases nominal coverage?", "Hvad øger den nominelle dækning?"),
            (("a", ("Usar 99 % en vez de 95 %", "Use 99% instead of 95%", "Brug 99 % i stedet for 95 %")), ("b", ("Reducir n", "Reduce n", "Reducér n")), ("c", ("Eliminar SD", "Remove SD", "Fjern SD")), ("d", ("Truncar datos", "Truncate data", "Afkort data"))),
            "a",
            ("Mayor cobertura requiere un intervalo más ancho.", "Higher coverage requires a wider interval.", "Højere dækning kræver et bredere interval."),
        ),
        (
            "008",
            ("¿Qué intervalo respeta mejor los límites de una proporción?", "Which interval better respects proportion boundaries?", "Hvilket interval respekterer bedst grænserne for en proportion?"),
            (("a", ("Wilson", "Wilson", "Wilson")), ("b", ("Media ± SD", "Mean ± SD", "Gennemsnit ± SD")), ("c", ("Rango", "Range", "Variationsbredde")), ("d", ("Ninguno", "None", "Ingen"))),
            "a",
            ("Wilson evita parte del mal comportamiento de la aproximación simétrica.", "Wilson avoids some poor behaviour of the symmetric approximation.", "Wilson undgår noget af den symmetriske approksimations dårlige adfærd."),
        ),
    ),
    true_false=(
        ("009", ("La desviación estándar y el error estándar responden a la misma pregunta.", "Standard deviation and standard error answer the same question.", "Standardafvigelse og standardfejl besvarer samme spørgsmål."), False, ("SD describe observaciones; SE describe precisión del estimador.", "SD describes observations; SE describes estimator precision.", "SD beskriver observationer; SE beskriver estimatorens præcision.")),
        ("010", ("Cuadruplicar n efectivo reduce aproximadamente a la mitad el SE.", "Quadrupling effective n approximately halves SE.", "En firedobling af effektivt n halverer omtrent SE."), True, ("SE escala con 1/√n.", "SE scales with 1/√n.", "SE skalerer med 1/√n.")),
        ("011", ("Un intervalo estrecho demuestra ausencia de sesgo.", "A narrow interval proves absence of bias.", "Et smalt interval beviser fravær af bias."), False, ("Precisión y sesgo son propiedades distintas.", "Precision and bias are distinct properties.", "Præcision og bias er forskellige egenskaber.")),
        ("012", ("Un intervalo del 99 % suele ser más ancho que uno del 95 %.", "A 99% interval is usually wider than a 95% interval.", "Et 99 %-interval er normalt bredere end et 95 %-interval."), True, ("Mayor cobertura requiere un valor crítico mayor.", "Higher coverage requires a larger critical value.", "Højere dækning kræver en større kritisk værdi.")),
        ("013", ("La pseudorreplicación reduce válidamente el SE como nuevas unidades biológicas.", "Pseudoreplication validly reduces SE as new biological units.", "Pseudoreplikation reducerer gyldigt SE som nye biologiske enheder."), False, ("Las mediciones dependientes no aumentan n efectivo del mismo modo.", "Dependent measurements do not increase effective n in the same way.", "Afhængige målinger øger ikke effektivt n på samme måde.")),
        ("014", ("La cobertura es una propiedad del procedimiento bajo supuestos.", "Coverage is a property of the procedure under assumptions.", "Dækning er en egenskab ved proceduren under antagelser."), True, ("Se evalúa sobre muestreos repetidos.", "It is evaluated over repeated samples.", "Den vurderes over gentagne stikprøver.")),
        ("015", ("Un valor puntual comunica magnitud pero no precisión.", "A point value communicates magnitude but not precision.", "Et punktestimat kommunikerer størrelse, men ikke præcision."), True, ("Se necesita una medida de incertidumbre.", "A measure of uncertainty is needed.", "Der kræves et mål for usikkerhed.")),
        ("016", ("La media ± SD es automáticamente un intervalo de confianza.", "Mean ± SD is automatically a confidence interval.", "Gennemsnit ± SD er automatisk et konfidensinterval."), False, ("SD no es el error estándar ni incorpora un valor crítico.", "SD is neither standard error nor a critical-value interval.", "SD er hverken standardfejl eller et interval med kritisk værdi.")),
    ),
    tutor=(
        (
            "La estimación rigurosa declara el estimando, presenta una estimación con unidades y acompaña la magnitud con incertidumbre calculada para el diseño y el modelo adecuados.",
            "Rigorous estimation declares the estimand, presents an estimate with units, and accompanies magnitude with uncertainty calculated for the appropriate design and model.",
            "Grundig estimation erklærer estimanden, præsenterer et estimat med enheder og ledsager størrelsen med usikkerhed beregnet for passende design og model.",
        ),
        (("El error estándar pertenece al estimador.", "Standard error belongs to the estimator.", "Standardfejlen tilhører estimatoren."), ("La cobertura es frecuentista y procedimental.", "Coverage is frequentist and procedural.", "Dækning er frekventistisk og proceduremæssig."), ("La independencia determina n efectivo.", "Independence determines effective n.", "Uafhængighed bestemmer effektivt n."), ("Precisión y sesgo deben evaluarse por separado.", "Precision and bias must be evaluated separately.", "Præcision og bias skal vurderes separat.")),
        (("Interpretar CI como probabilidad posterior.", "Interpreting a CI as posterior probability.", "At fortolke KI som posterior sandsynlighed."), ("Confundir SD y SE.", "Confusing SD and SE.", "At forveksle SD og SE."), ("Contar réplicas técnicas como n independiente.", "Counting technical replicates as independent n.", "At tælle tekniske replikater som uafhængigt n.")),
        (("¿Cuál es el estimando?", "What is the estimand?", "Hvad er estimanden?"), ("¿Cuál es la unidad independiente?", "What is the independent unit?", "Hvad er den uafhængige enhed?"), ("¿Qué supuesto justifica el intervalo?", "Which assumption justifies the interval?", "Hvilken antagelse begrunder intervallet?")),
        (("Distingue SD y SE.", "Distinguishes SD and SE.", "Skelner mellem SD og SE."), ("Interpreta cobertura correctamente.", "Interprets coverage correctly.", "Fortolker dækning korrekt."), ("Reporta magnitud, unidades e incertidumbre.", "Reports magnitude, units, and uncertainty.", "Rapporterer størrelse, enheder og usikkerhed.")),
        (("No inventar tamaños muestrales ni intervalos.", "Do not invent sample sizes or intervals.", "Opfind ikke stikprøvestørrelser eller intervaller."), ("No convertir CI frecuentista en probabilidad posterior.", "Do not convert a frequentist CI into posterior probability.", "Konvertér ikke et frekventistisk KI til posterior sandsynlighed."), ("Responder en el idioma activo.", "Respond in the active language.", "Svar på det aktive sprog.")),
        ("SDU ODIN BMB830 active course description approved 2025-03-06", "R base stats documentation: qt, qnorm, t.test", "Wilson score interval derivation"),
    ),
)

LOCALIZED_MODULE_04_ESTIMATION = build_module(_SPEC)
LOCALIZED_OBJECTIVE_QUESTION_BANK_04 = build_question_bank(_SPEC)
MODULE_04_ESTIMATION: LearningModule = LOCALIZED_MODULE_04_ESTIMATION.materialize(
    AppLocale.SPANISH_SPAIN
)
OBJECTIVE_QUESTION_BANK_04: tuple[AssessmentItem, ...] = materialize_bank(
    LOCALIZED_OBJECTIVE_QUESTION_BANK_04
)


def materialize_module_04_question_bank(
    locale: AppLocale | str = AppLocale.SPANISH_SPAIN,
) -> tuple[AssessmentItem, ...]:
    """Return the module-4 objective bank in one locale."""

    return materialize_bank(LOCALIZED_OBJECTIVE_QUESTION_BANK_04, locale)


__all__ = [
    "LOCALIZED_MODULE_04_ESTIMATION",
    "LOCALIZED_OBJECTIVE_QUESTION_BANK_04",
    "MODULE_04_ESTIMATION",
    "OBJECTIVE_QUESTION_BANK_04",
    "materialize_module_04_question_bank",
]
