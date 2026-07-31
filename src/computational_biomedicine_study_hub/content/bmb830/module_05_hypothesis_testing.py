"""BMB830 module 5: hypothesis tests, errors, power, and effect sizes."""

from __future__ import annotations

from ...i18n import AppLocale
from ..models import AssessmentItem, LearningModule
from .standard import StandardModuleSpec, build_module, build_question_bank, materialize_bank

_SPEC = StandardModuleSpec(
    module_id="bmb830.m05",
    title=(
        "Pruebas de hipótesis, errores y potencia",
        "Hypothesis tests, errors, and power",
        "Hypotesetest, fejl og styrke",
    ),
    summary=(
        "Formula hipótesis, interpreta valores p, distingue errores tipo I y II, planifica potencia y reporta tamaños de efecto junto con incertidumbre.",
        "Formulate hypotheses, interpret p-values, distinguish type I and II errors, plan power, and report effect sizes with uncertainty.",
        "Formulér hypoteser, fortolk p-værdier, skeln mellem type I- og type II-fejl, planlæg styrke, og rapportér effektstørrelser med usikkerhed.",
    ),
    objectives=(
        (
            "m05.o1",
            (
                "Formular hipótesis nula y alternativa antes de inspeccionar resultados.",
                "Formulate null and alternative hypotheses before inspecting results.",
                "Formulere nul- og alternativhypoteser før resultaterne inspiceres.",
            ),
        ),
        (
            "m05.o2",
            (
                "Interpretar estadístico de prueba y valor p sin convertirlos en probabilidad de la hipótesis.",
                "Interpret test statistics and p-values without turning them into hypothesis probabilities.",
                "Fortolke teststatistik og p-værdi uden at gøre dem til hypotesesandsynligheder.",
            ),
        ),
        (
            "m05.o3",
            (
                "Distinguir errores tipo I y II, potencia y factores que los modifican.",
                "Distinguish type I and II errors, power, and the factors that change them.",
                "Skelne mellem type I- og type II-fejl, styrke og de faktorer, der ændrer dem.",
            ),
        ),
        (
            "m05.o4",
            (
                "Reportar tamaño de efecto, intervalo de confianza y relevancia científica.",
                "Report effect size, confidence interval, and scientific relevance.",
                "Rapportere effektstørrelse, konfidensinterval og videnskabelig relevans.",
            ),
        ),
    ),
    concepts=(
        (
            "hypotheses",
            (
                "Hipótesis y contraste",
                "Hypotheses and contrasts",
                "Hypoteser og kontraster",
            ),
            (
                "La hipótesis nula especifica un valor o estructura de referencia para el estimando; la alternativa define las desviaciones científicamente relevantes. Una prueba bilateral debe elegirse cuando importan cambios en ambas direcciones.",
                "The null hypothesis specifies a reference value or structure for the estimand; the alternative defines scientifically relevant departures. A two-sided test should be chosen when changes in either direction matter.",
                "Nulhypotesen angiver en referenceværdi eller struktur for estimanden; alternativet definerer videnskabeligt relevante afvigelser. En tosidet test bør vælges, når ændringer i begge retninger er relevante.",
            ),
            (
                (
                    "La dirección del contraste se fija antes de ver los datos.",
                    "Test direction is fixed before viewing data.",
                    "Testretningen fastlægges før data ses.",
                ),
                (
                    "La hipótesis debe corresponder al estimando y al diseño.",
                    "The hypothesis must match the estimand and design.",
                    "Hypotesen skal passe til estimanden og designet.",
                ),
            ),
        ),
        (
            "p-values",
            ("Valor p", "p-value", "p-værdi"),
            (
                "El valor p es la probabilidad, bajo la hipótesis nula y el modelo, de obtener un resultado al menos tan incompatible con la nulidad como el observado. No es la probabilidad de que la hipótesis nula sea verdadera ni mide el tamaño del efecto.",
                "The p-value is the probability, under the null hypothesis and model, of obtaining a result at least as incompatible with the null as the observed one. It is not the probability that the null is true and does not measure effect size.",
                "P-værdien er sandsynligheden under nulhypotesen og modellen for et resultat mindst lige så uforeneligt med nulhypotesen som det observerede. Den er ikke sandsynligheden for, at nulhypotesen er sand, og måler ikke effektstørrelse.",
            ),
            (
                (
                    "Un valor p depende del tamaño muestral y la variabilidad.",
                    "A p-value depends on sample size and variability.",
                    "En p-værdi afhænger af stikprøvestørrelse og variation.",
                ),
                (
                    "El umbral alfa es una decisión previa, no una propiedad de los datos.",
                    "The alpha threshold is a prior decision, not a property of the data.",
                    "Alfa-grænsen er en forudgående beslutning, ikke en egenskab ved data.",
                ),
            ),
        ),
        (
            "errors-power",
            (
                "Errores y potencia",
                "Errors and power",
                "Fejl og styrke",
            ),
            (
                "Un error tipo I rechaza una nulidad verdadera y está controlado por alfa. Un error tipo II no rechaza una nulidad falsa; su probabilidad es beta y la potencia es 1−beta. Potencia aumenta con mayor efecto, menor variabilidad, mayor tamaño muestral o alfa menos estricto.",
                "A type I error rejects a true null and is controlled by alpha. A type II error fails to reject a false null; its probability is beta and power is 1−beta. Power rises with larger effects, lower variability, larger samples, or a less stringent alpha.",
                "En type I-fejl forkaster en sand nulhypotese og styres af alfa. En type II-fejl undlader at forkaste en falsk nulhypotese; sandsynligheden er beta og styrken er 1−beta. Styrken øges med større effekt, lavere variation, større stikprøve eller mindre strengt alfa.",
            ),
            (
                (
                    "No rechazar no demuestra equivalencia.",
                    "Failure to reject does not prove equivalence.",
                    "Manglende forkastelse beviser ikke ækvivalens.",
                ),
                (
                    "La potencia debe planificarse con un efecto mínimo relevante.",
                    "Power should be planned around a minimum relevant effect.",
                    "Styrke bør planlægges omkring en mindste relevant effekt.",
                ),
            ),
        ),
        (
            "effect-size",
            (
                "Magnitud y relevancia",
                "Magnitude and relevance",
                "Størrelse og relevans",
            ),
            (
                "El tamaño de efecto expresa magnitud en unidades originales o estandarizadas. Debe acompañarse de intervalo de confianza y contexto biomédico; significación estadística no garantiza importancia clínica o biológica.",
                "Effect size expresses magnitude in original or standardised units. It should be accompanied by a confidence interval and biomedical context; statistical significance does not guarantee clinical or biological importance.",
                "Effektstørrelsen udtrykker størrelsen i originale eller standardiserede enheder. Den bør ledsages af et konfidensinterval og biomedicinsk kontekst; statistisk signifikans garanterer ikke klinisk eller biologisk betydning.",
            ),
            (
                (
                    "Las unidades originales suelen facilitar interpretación.",
                    "Original units often aid interpretation.",
                    "Originale enheder letter ofte fortolkningen.",
                ),
                (
                    "Un efecto pequeño puede ser preciso y un efecto grande puede ser incierto.",
                    "A small effect can be precise and a large effect can be uncertain.",
                    "En lille effekt kan være præcis, og en stor effekt kan være usikker.",
                ),
            ),
        ),
    ),
    examples=(
        (
            "m05.e01",
            (
                "Prueba t de una media de diferencias",
                "t test for a mean difference",
                "t-test for en gennemsnitlig forskel",
            ),
            (
                "Evalúa si la media de seis diferencias independientes es compatible con cero y reporta magnitud e intervalo.",
                "Assess whether the mean of six independent differences is compatible with zero and report magnitude and interval.",
                "Vurdér om gennemsnittet af seks uafhængige forskelle er foreneligt med nul, og rapportér størrelse og interval.",
            ),
            (
                (
                    "La hipótesis nula fija la diferencia media en cero.",
                    "The null fixes the mean difference at zero.",
                    "Nulhypotesen fastsætter den gennemsnitlige forskel til nul.",
                ),
                (
                    "El resultado debe incluir estimación, intervalo y valor p.",
                    "The result should include estimate, interval, and p-value.",
                    "Resultatet bør indeholde estimat, interval og p-værdi.",
                ),
            ),
            """delta <- c(1.2, 0.8, 1.5, 0.9, 1.1, 1.4)
fit <- t.test(delta, mu = 0)
cat(sprintf("effect=%.2f\n", unname(fit$estimate)))
cat(sprintf("ci=[%.2f, %.2f]\n", fit$conf.int[1], fit$conf.int[2]))
cat(sprintf("p=%.4f", fit$p.value))
""",
            """effect=1.15
ci=[0.86, 1.44]
p=0.0001""",
            (
                "El valor p pequeño describe incompatibilidad con una diferencia nula bajo el modelo; la magnitud de 1,15 conserva la interpretación científica.",
                "The small p-value describes incompatibility with a zero difference under the model; the magnitude of 1.15 retains scientific interpretation.",
                "Den lille p-værdi beskriver uforenelighed med en nulforskel under modellen; størrelsen 1,15 bevarer den videnskabelige fortolkning.",
            ),
        ),
        (
            "m05.e02",
            (
                "Planificación de potencia",
                "Power planning",
                "Styrkeplanlægning",
            ),
            (
                "Calcula el número mínimo aproximado por grupo para detectar una diferencia de 0,6 con SD 1, potencia 80 % y alfa 0,05.",
                "Calculate the approximate minimum per group to detect a difference of 0.6 with SD 1, 80% power, and alpha 0.05.",
                "Beregn det omtrentlige minimum pr. gruppe for at opdage en forskel på 0,6 med SD 1, 80 % styrke og alfa 0,05.",
            ),
            (
                (
                    "La diferencia de 0,6 debe representar un efecto mínimo relevante.",
                    "The difference of 0.6 should represent a minimum relevant effect.",
                    "Forskellen på 0,6 bør repræsentere en mindste relevant effekt.",
                ),
                (
                    "El resultado se redondea hacia arriba.",
                    "The result is rounded upward.",
                    "Resultatet afrundes opad.",
                ),
            ),
            """plan <- power.t.test(
  delta = 0.6,
  sd = 1,
  sig.level = 0.05,
  power = 0.80,
  type = "two.sample",
  alternative = "two.sided"
)
cat(sprintf("n_per_group=%d", ceiling(plan$n)))
""",
            "n_per_group=45",
            (
                "La planificación depende de supuestos sobre variabilidad, pérdidas, independencia y análisis final.",
                "Planning depends on assumptions about variability, attrition, independence, and the final analysis.",
                "Planlægningen afhænger af antagelser om variation, frafald, uafhængighed og den endelige analyse.",
            ),
        ),
    ),
    practices=(
        (
            "m05.p01",
            "ORAL_EXPLANATION",
            (
                "Explica por qué p=0,03 no significa que la nulidad tenga 3 % de probabilidad.",
                "Explain why p=0.03 does not mean that the null has 3% probability.",
                "Forklar hvorfor p=0,03 ikke betyder, at nulhypotesen har 3 % sandsynlighed.",
            ),
            (
                (
                    "Condiciona la probabilidad en H0, no al revés.",
                    "Condition the probability on H0, not the reverse.",
                    "Beting sandsynligheden på H0, ikke omvendt.",
                ),
            ),
            (
                "Es una probabilidad de datos extremos bajo H0 y el modelo, no una probabilidad posterior de H0.",
                "It is a probability of extreme data under H0 and the model, not a posterior probability of H0.",
                "Det er en sandsynlighed for ekstreme data under H0 og modellen, ikke en posterior sandsynlighed for H0.",
            ),
            (
                "La inversión de la condición es una falacia común.",
                "Reversing the condition is a common fallacy.",
                "At vende betingelsen om er en almindelig fejlslutning.",
            ),
            "",
        ),
        (
            "m05.p02",
            "DATA_INTERPRETATION",
            (
                "Clasifica como tipo I o tipo II: declarar un biomarcador eficaz cuando no lo es; no detectarlo cuando sí lo es.",
                "Classify as type I or II: declaring an ineffective biomarker effective; failing to detect it when effective.",
                "Klassificér som type I eller II: at erklære en ineffektiv biomarkør effektiv; ikke at opdage den, når den er effektiv.",
            ),
            (
                (
                    "Compara la decisión con el estado real.",
                    "Compare the decision with the real state.",
                    "Sammenlign beslutningen med den virkelige tilstand.",
                ),
            ),
            (
                "Falso positivo: tipo I. Falso negativo inferencial: tipo II.",
                "False positive: type I. Inferential false negative: type II.",
                "Falsk positiv: type I. Inferentiel falsk negativ: type II.",
            ),
            (
                "Las consecuencias científicas pueden hacer que los costes sean asimétricos.",
                "Scientific consequences may make the costs asymmetric.",
                "Videnskabelige konsekvenser kan gøre omkostningerne asymmetriske.",
            ),
            "",
        ),
        (
            "m05.p03",
            "CODE_COMPLETION",
            (
                "Completa una prueba bilateral de una media frente a cero.",
                "Complete a two-sided one-mean test against zero.",
                "Fuldfør en tosidet test af ét gennemsnit mod nul.",
            ),
            (
                (
                    "t.test usa alternative='two.sided' por defecto, pero decláralo.",
                    "t.test defaults to alternative='two.sided', but declare it.",
                    "t.test bruger som standard alternative='two.sided', men erklær det.",
                ),
            ),
            ("t.test(x, mu = 0, alternative = 'two.sided')",) * 3,
            (
                "La dirección queda explícita y auditable.",
                "The direction becomes explicit and auditable.",
                "Retningen bliver eksplicit og kan revideres.",
            ),
            "fit <- ______________________________",
        ),
        (
            "m05.p04",
            "DATA_INTERPRETATION",
            (
                "Compara un efecto de 0,2 con CI [0,18; 0,22] y uno de 1,0 con CI [-0,5; 2,5].",
                "Compare an effect of 0.2 with CI [0.18, 0.22] and one of 1.0 with CI [-0.5, 2.5].",
                "Sammenlign en effekt på 0,2 med KI [0,18; 0,22] og en på 1,0 med KI [-0,5; 2,5].",
            ),
            (
                (
                    "Separa magnitud y precisión.",
                    "Separate magnitude and precision.",
                    "Adskil størrelse og præcision.",
                ),
            ),
            (
                "El primero es pequeño y preciso; el segundo es mayor pero muy incierto e incluye cero.",
                "The first is small and precise; the second is larger but highly uncertain and includes zero.",
                "Den første er lille og præcis; den anden er større, men meget usikker og inkluderer nul.",
            ),
            (
                "La relevancia requiere contexto, no solo significación.",
                "Relevance requires context, not significance alone.",
                "Relevans kræver kontekst, ikke kun signifikans.",
            ),
            "",
        ),
        (
            "m05.p05",
            "PIPELINE_DESIGN",
            (
                "Diseña una planificación de potencia antes de recoger datos.",
                "Design a power plan before collecting data.",
                "Design en styrkeplan før dataindsamling.",
            ),
            (
                (
                    "Empieza por un efecto mínimo relevante.",
                    "Begin with a minimum relevant effect.",
                    "Begynd med en mindste relevant effekt.",
                ),
            ),
            (
                "Definir estimando, contraste, alfa, potencia, efecto mínimo, variabilidad, diseño, pérdidas y análisis previsto.",
                "Define estimand, contrast, alpha, power, minimum effect, variability, design, attrition, and planned analysis.",
                "Definér estimand, kontrast, alfa, styrke, mindste effekt, variation, design, frafald og planlagt analyse.",
            ),
            (
                "La potencia post hoc basada en el efecto observado no sustituye la planificación.",
                "Post-hoc power based on the observed effect does not replace planning.",
                "Post hoc-styrke baseret på den observerede effekt erstatter ikke planlægning.",
            ),
            "",
        ),
        (
            "m05.p06",
            "DEBUGGING",
            (
                "Corrige la conclusión 'p>0,05 demuestra que los grupos son iguales'.",
                "Correct the conclusion 'p>0.05 proves the groups are equal'.",
                "Ret konklusionen 'p>0,05 beviser, at grupperne er ens'.",
            ),
            (
                (
                    "No rechazar no es aceptar equivalencia.",
                    "Failure to reject is not accepting equivalence.",
                    "Manglende forkastelse er ikke accept af ækvivalens.",
                ),
            ),
            (
                "Los datos no aportan evidencia suficiente contra H0 bajo este análisis; revisar intervalo, potencia y un margen de equivalencia predefinido.",
                "The data do not provide sufficient evidence against H0 under this analysis; inspect the interval, power, and a predefined equivalence margin.",
                "Data giver ikke tilstrækkelig evidens mod H0 under denne analyse; undersøg interval, styrke og en foruddefineret ækvivalensmargin.",
            ),
            (
                "La equivalencia requiere un diseño y procedimiento específicos.",
                "Equivalence requires a specific design and procedure.",
                "Ækvivalens kræver et specifikt design og en specifik procedure.",
            ),
            "",
        ),
    ),
    mcqs=(
        (
            "001",
            ("¿Qué es un valor p?", "What is a p-value?", "Hvad er en p-værdi?"),
            (
                ("a", ("P(H0 verdadera)", "P(H0 true)", "P(H0 sand)")),
                (
                    "b",
                    (
                        "Probabilidad de datos al menos tan extremos bajo H0",
                        "Probability of data at least as extreme under H0",
                        "Sandsynlighed for mindst lige så ekstreme data under H0",
                    ),
                ),
                ("c", ("Tamaño del efecto", "Effect size", "Effektstørrelse")),
                ("d", ("Potencia", "Power", "Styrke")),
            ),
            "b",
            (
                "El valor p condiciona en H0 y el modelo.",
                "The p-value conditions on H0 and the model.",
                "P-værdien betinger på H0 og modellen.",
            ),
        ),
        (
            "002",
            ("¿Qué es un error tipo I?", "What is a type I error?", "Hvad er en type I-fejl?"),
            (
                (
                    "a",
                    ("No rechazar H0 falsa", "Fail to reject false H0", "Ikke forkaste falsk H0"),
                ),
                ("b", ("Rechazar H0 verdadera", "Reject true H0", "Forkaste sand H0")),
                ("c", ("Estimar SD", "Estimate SD", "Estimere SD")),
                ("d", ("Aumentar n", "Increase n", "Øge n")),
            ),
            "b",
            (
                "Alfa controla la tasa de rechazo de una nulidad verdadera.",
                "Alpha controls rejection of a true null.",
                "Alfa styrer forkastelse af en sand nulhypotese.",
            ),
        ),
        (
            "003",
            ("¿Qué es potencia?", "What is power?", "Hvad er styrke?"),
            (
                ("a", ("1−beta", "1−beta", "1−beta")),
                ("b", ("1−alpha", "1−alpha", "1−alpha")),
                ("c", ("Valor p", "p-value", "p-værdi")),
                ("d", ("SD", "SD", "SD")),
            ),
            "a",
            (
                "Potencia es la probabilidad de rechazar H0 cuando la alternativa especificada es verdadera.",
                "Power is the probability of rejecting H0 when the specified alternative is true.",
                "Styrke er sandsynligheden for at forkaste H0, når det specificerede alternativ er sandt.",
            ),
        ),
        (
            "004",
            (
                "¿Qué suele aumentar potencia?",
                "What usually increases power?",
                "Hvad øger normalt styrken?",
            ),
            (
                ("a", ("Menor n", "Smaller n", "Mindre n")),
                ("b", ("Mayor variabilidad", "Higher variability", "Større variation")),
                ("c", ("Mayor n independiente", "Larger independent n", "Større uafhængigt n")),
                ("d", ("Alfa más estricto", "More stringent alpha", "Strengere alfa")),
            ),
            "c",
            (
                "Más unidades independientes mejoran precisión.",
                "More independent units improve precision.",
                "Flere uafhængige enheder forbedrer præcisionen.",
            ),
        ),
        (
            "005",
            (
                "¿Qué debe definir una planificación de potencia?",
                "What should power planning define?",
                "Hvad bør styrkeplanlægning definere?",
            ),
            (
                (
                    "a",
                    (
                        "Efecto mínimo relevante",
                        "Minimum relevant effect",
                        "Mindste relevante effekt",
                    ),
                ),
                (
                    "b",
                    (
                        "Efecto observado futuro",
                        "Future observed effect",
                        "Fremtidig observeret effekt",
                    ),
                ),
                ("c", ("Solo color del gráfico", "Plot colour only", "Kun plotfarve")),
                ("d", ("Valor p deseado", "Desired p-value", "Ønsket p-værdi")),
            ),
            "a",
            (
                "El efecto de planificación debe tener significado científico previo.",
                "The planning effect should have prior scientific meaning.",
                "Planlægningseffekten bør have forudgående videnskabelig betydning.",
            ),
        ),
        (
            "006",
            (
                "¿Qué comunica un tamaño de efecto?",
                "What does an effect size communicate?",
                "Hvad kommunikerer en effektstørrelse?",
            ),
            (
                ("a", ("Magnitud", "Magnitude", "Størrelse")),
                ("b", ("Probabilidad de H0", "Probability of H0", "Sandsynlighed for H0")),
                ("c", ("Solo precisión", "Precision only", "Kun præcision")),
                ("d", ("Número de variables", "Number of variables", "Antal variable")),
            ),
            "a",
            (
                "La magnitud debe contextualizarse e incluir incertidumbre.",
                "Magnitude should be contextualised and include uncertainty.",
                "Størrelsen bør sættes i kontekst og inkludere usikkerhed.",
            ),
        ),
        (
            "007",
            ("¿Qué significa p>0,05?", "What does p>0.05 mean?", "Hvad betyder p>0,05?"),
            (
                ("a", ("H0 demostrada", "H0 proven", "H0 bevist")),
                (
                    "b",
                    (
                        "Evidencia insuficiente para rechazar H0 con ese procedimiento",
                        "Insufficient evidence to reject H0 with that procedure",
                        "Utilstrækkelig evidens til at forkaste H0 med den procedure",
                    ),
                ),
                ("c", ("Grupos equivalentes", "Equivalent groups", "Ækvivalente grupper")),
                ("d", ("Efecto cero", "Zero effect", "Nuleffekt")),
            ),
            "b",
            (
                "No rechazo no prueba nulidad ni equivalencia.",
                "Non-rejection proves neither nullity nor equivalence.",
                "Manglende forkastelse beviser hverken nul eller ækvivalens.",
            ),
        ),
        (
            "008",
            (
                "¿Qué debe fijarse antes de inspeccionar resultados?",
                "What should be fixed before inspecting results?",
                "Hvad bør fastlægges før resultater inspiceres?",
            ),
            (
                ("a", ("Dirección y alfa", "Direction and alpha", "Retning og alfa")),
                ("b", ("Conclusión", "Conclusion", "Konklusion")),
                ("c", ("Efecto observado", "Observed effect", "Observeret effekt")),
                ("d", ("Valor p", "p-value", "p-værdi")),
            ),
            "a",
            (
                "Las decisiones previas reducen flexibilidad analítica oportunista.",
                "Prior decisions reduce opportunistic analytical flexibility.",
                "Forudgående beslutninger reducerer opportunistisk analytisk fleksibilitet.",
            ),
        ),
    ),
    true_false=(
        (
            "009",
            (
                "p=0,01 significa que H0 tiene 1 % de probabilidad.",
                "p=0.01 means H0 has 1% probability.",
                "p=0,01 betyder, at H0 har 1 % sandsynlighed.",
            ),
            False,
            (
                "El valor p no es una probabilidad posterior de H0.",
                "The p-value is not a posterior probability of H0.",
                "P-værdien er ikke en posterior sandsynlighed for H0.",
            ),
        ),
        (
            "010",
            (
                "Alfa controla el error tipo I bajo el procedimiento.",
                "Alpha controls type I error under the procedure.",
                "Alfa styrer type I-fejl under proceduren.",
            ),
            True,
            (
                "Es la tasa nominal de falsos rechazos bajo H0.",
                "It is the nominal false-rejection rate under H0.",
                "Det er den nominelle rate af falske forkastelser under H0.",
            ),
        ),
        (
            "011",
            (
                "Potencia y beta suman uno.",
                "Power and beta sum to one.",
                "Styrke og beta summerer til ét.",
            ),
            True,
            ("Potencia = 1−beta.", "Power = 1−beta.", "Styrke = 1−beta."),
        ),
        (
            "012",
            (
                "Un resultado no significativo demuestra equivalencia.",
                "A non-significant result proves equivalence.",
                "Et ikke-signifikant resultat beviser ækvivalens.",
            ),
            False,
            (
                "La equivalencia necesita margen y procedimiento específicos.",
                "Equivalence needs a specific margin and procedure.",
                "Ækvivalens kræver en specifik margin og procedure.",
            ),
        ),
        (
            "013",
            (
                "Un efecto estadísticamente significativo puede ser científicamente trivial.",
                "A statistically significant effect may be scientifically trivial.",
                "En statistisk signifikant effekt kan være videnskabeligt triviel.",
            ),
            True,
            (
                "Significación y relevancia responden preguntas distintas.",
                "Significance and relevance answer different questions.",
                "Signifikans og relevans besvarer forskellige spørgsmål.",
            ),
        ),
        (
            "014",
            (
                "Mayor variabilidad suele reducir potencia.",
                "Higher variability usually reduces power.",
                "Større variation reducerer normalt styrken.",
            ),
            True,
            (
                "Aumenta el error estándar.",
                "It increases standard error.",
                "Det øger standardfejlen.",
            ),
        ),
        (
            "015",
            (
                "Elegir una prueba unilateral después de ver la dirección observada es válido.",
                "Choosing a one-sided test after seeing the observed direction is valid.",
                "Det er gyldigt at vælge en ensidet test efter at have set den observerede retning.",
            ),
            False,
            (
                "La dirección debe justificarse y fijarse previamente.",
                "Direction should be justified and fixed in advance.",
                "Retningen bør begrundes og fastlægges på forhånd.",
            ),
        ),
        (
            "016",
            (
                "El tamaño de efecto debe acompañarse de incertidumbre.",
                "Effect size should be accompanied by uncertainty.",
                "Effektstørrelse bør ledsages af usikkerhed.",
            ),
            True,
            (
                "Un intervalo muestra precisión y valores compatibles.",
                "An interval shows precision and compatible values.",
                "Et interval viser præcision og kompatible værdier.",
            ),
        ),
    ),
    tutor=(
        (
            "Una prueba de hipótesis rigurosa parte de un estimando y contraste predefinidos, interpreta el valor p condicionalmente al modelo y comunica magnitud, incertidumbre, potencia y relevancia científica.",
            "A rigorous hypothesis test starts from a predefined estimand and contrast, interprets the p-value conditionally on the model, and communicates magnitude, uncertainty, power, and scientific relevance.",
            "En grundig hypotesetest starter med en foruddefineret estimand og kontrast, fortolker p-værdien betinget på modellen og kommunikerer størrelse, usikkerhed, styrke og videnskabelig relevans.",
        ),
        (
            ("El valor p no es P(H0).", "The p-value is not P(H0).", "P-værdien er ikke P(H0)."),
            (
                "Alfa y beta describen errores distintos.",
                "Alpha and beta describe different errors.",
                "Alfa og beta beskriver forskellige fejl.",
            ),
            (
                "Potencia depende del efecto de planificación.",
                "Power depends on the planning effect.",
                "Styrke afhænger af planlægningseffekten.",
            ),
            (
                "La magnitud debe reportarse en contexto.",
                "Magnitude should be reported in context.",
                "Størrelsen bør rapporteres i kontekst.",
            ),
        ),
        (
            (
                "Aceptar H0 tras p>0,05.",
                "Accepting H0 after p>0.05.",
                "At acceptere H0 efter p>0,05.",
            ),
            (
                "Confundir significación con importancia.",
                "Confusing significance with importance.",
                "At forveksle signifikans med betydning.",
            ),
            (
                "Calcular potencia post hoc como evidencia.",
                "Using post-hoc power as evidence.",
                "At bruge post hoc-styrke som evidens.",
            ),
        ),
        (
            (
                "¿Cuál es el error científico más costoso?",
                "Which scientific error is most costly?",
                "Hvilken videnskabelig fejl er dyrest?",
            ),
            (
                "¿Qué efecto mínimo importa?",
                "What minimum effect matters?",
                "Hvilken mindste effekt betyder noget?",
            ),
            (
                "¿Qué valores admite el intervalo?",
                "Which values are compatible with the interval?",
                "Hvilke værdier er kompatible med intervallet?",
            ),
        ),
        (
            (
                "Formula hipótesis coherentes.",
                "Formulates coherent hypotheses.",
                "Formulerer sammenhængende hypoteser.",
            ),
            (
                "Interpreta p sin inversión condicional.",
                "Interprets p without conditional inversion.",
                "Fortolker p uden betinget omvending.",
            ),
            (
                "Integra efecto, intervalo y potencia.",
                "Integrates effect, interval, and power.",
                "Integrerer effekt, interval og styrke.",
            ),
        ),
        (
            (
                "No asignar probabilidades a H0 desde un valor p.",
                "Do not assign probabilities to H0 from a p-value.",
                "Tildel ikke H0 sandsynligheder ud fra en p-værdi.",
            ),
            (
                "No declarar equivalencia sin margen y prueba.",
                "Do not declare equivalence without a margin and test.",
                "Erklær ikke ækvivalens uden margin og test.",
            ),
            (
                "Responder en el idioma activo.",
                "Respond in the active language.",
                "Svar på det aktive sprog.",
            ),
        ),
        (
            "SDU ODIN BMB830 active course description approved 2025-03-06",
            "R base stats documentation: t.test and power.t.test",
            "Frequentist hypothesis-testing definitions",
        ),
    ),
)

LOCALIZED_MODULE_05_HYPOTHESIS_TESTING = build_module(_SPEC)
LOCALIZED_OBJECTIVE_QUESTION_BANK_05 = build_question_bank(_SPEC)
MODULE_05_HYPOTHESIS_TESTING: LearningModule = LOCALIZED_MODULE_05_HYPOTHESIS_TESTING.materialize(
    AppLocale.SPANISH_SPAIN
)
OBJECTIVE_QUESTION_BANK_05: tuple[AssessmentItem, ...] = materialize_bank(
    LOCALIZED_OBJECTIVE_QUESTION_BANK_05
)


def materialize_module_05_question_bank(
    locale: AppLocale | str = AppLocale.SPANISH_SPAIN,
) -> tuple[AssessmentItem, ...]:
    """Return the module-5 objective bank in one locale."""

    return materialize_bank(LOCALIZED_OBJECTIVE_QUESTION_BANK_05, locale)


__all__ = [
    "LOCALIZED_MODULE_05_HYPOTHESIS_TESTING",
    "LOCALIZED_OBJECTIVE_QUESTION_BANK_05",
    "MODULE_05_HYPOTHESIS_TESTING",
    "OBJECTIVE_QUESTION_BANK_05",
    "materialize_module_05_question_bank",
]
