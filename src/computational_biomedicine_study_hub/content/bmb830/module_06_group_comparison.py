"""BMB830 module 6: group comparisons and method selection."""

from __future__ import annotations

from ...i18n import AppLocale
from ..models import AssessmentItem, LearningModule
from .standard import StandardModuleSpec, build_module, build_question_bank, materialize_bank

_SPEC = StandardModuleSpec(
    module_id="bmb830.m06",
    title=(
        "Comparación de grupos y selección del método",
        "Group comparison and method selection",
        "Gruppesammenligning og metodevalg",
    ),
    summary=(
        "Selecciona y ejecuta comparaciones para diseños independientes, pareados y con más de dos grupos, comprobando supuestos y reportando efectos e incertidumbre.",
        "Select and run comparisons for independent, paired, and multi-group designs while checking assumptions and reporting effects and uncertainty.",
        "Vælg og udfør sammenligninger for uafhængige, parrede og flergruppedesign, kontrollér antagelser, og rapportér effekter og usikkerhed.",
    ),
    objectives=(
        (
            "m06.o1",
            (
                "Identificar si las observaciones son independientes, pareadas, repetidas o agrupadas.",
                "Identify whether observations are independent, paired, repeated, or clustered.",
                "Identificere om observationer er uafhængige, parrede, gentagne eller grupperede.",
            ),
        ),
        (
            "m06.o2",
            (
                "Elegir entre prueba t de Welch, prueba pareada, ANOVA y alternativas por rangos según diseño y estimando.",
                "Choose among Welch's t test, paired test, ANOVA, and rank-based alternatives according to design and estimand.",
                "Vælge mellem Welchs t-test, parret test, ANOVA og rangbaserede alternativer efter design og estimand.",
            ),
        ),
        (
            "m06.o3",
            (
                "Evaluar supuestos mediante diseño, gráficos y residuos sin depender de una única prueba diagnóstica.",
                "Evaluate assumptions using design, plots, and residuals rather than a single diagnostic test.",
                "Vurdere antagelser med design, plots og residualer frem for én diagnostisk test.",
            ),
        ),
        (
            "m06.o4",
            (
                "Interpretar comparaciones globales y específicas sin inflar el error por múltiples contrastes.",
                "Interpret global and specific comparisons without inflating error through multiple contrasts.",
                "Fortolke globale og specifikke sammenligninger uden at øge fejl gennem multiple kontraster.",
            ),
        ),
    ),
    concepts=(
        (
            "design-dependence",
            (
                "Diseño y dependencia",
                "Design and dependence",
                "Design og afhængighed",
            ),
            (
                "La elección de prueba comienza por la unidad experimental y la relación entre observaciones. Medidas antes-después de la misma persona son pareadas; muestras de personas diferentes suelen ser independientes; réplicas técnicas y datos por centro crean dependencia adicional.",
                "Test choice begins with the experimental unit and the relationship among observations. Before-after measurements from the same person are paired; samples from different people are usually independent; technical replicates and centre-level data create additional dependence.",
                "Testvalg begynder med den eksperimentelle enhed og forholdet mellem observationer. Før-efter-målinger fra samme person er parrede; prøver fra forskellige personer er normalt uafhængige; tekniske replikater og centerdata skaber yderligere afhængighed.",
            ),
            (
                (
                    "Ignorar el pareamiento desperdicia información y altera el error estándar.",
                    "Ignoring pairing wastes information and changes the standard error.",
                    "At ignorere parring spilder information og ændrer standardfejlen.",
                ),
                (
                    "La dependencia no se corrige eligiendo una prueba no paramétrica.",
                    "Dependence is not fixed by choosing a non-parametric test.",
                    "Afhængighed løses ikke ved at vælge en ikkeparametrisk test.",
                ),
            ),
        ),
        (
            "two-groups",
            (
                "Dos grupos",
                "Two groups",
                "To grupper",
            ),
            (
                "Para dos grupos independientes con una variable continua, la prueba t de Welch es un punto de partida robusto porque no exige varianzas iguales. En datos pareados, el análisis se realiza sobre diferencias dentro de unidad. La pregunta científica debe expresarse como una diferencia y un intervalo.",
                "For two independent groups with a continuous outcome, Welch's t test is a robust default because it does not require equal variances. In paired data, analysis operates on within-unit differences. The scientific question should be expressed as a difference and interval.",
                "For to uafhængige grupper med et kontinuert udfald er Welchs t-test et robust udgangspunkt, fordi den ikke kræver ens varianser. For parrede data analyseres forskelle inden for enheden. Det videnskabelige spørgsmål bør udtrykkes som en forskel og et interval.",
            ),
            (
                (
                    "var.equal=FALSE corresponde a Welch.",
                    "var.equal=FALSE corresponds to Welch.",
                    "var.equal=FALSE svarer til Welch.",
                ),
                (
                    "En un diseño pareado, n es el número de pares completos.",
                    "In a paired design, n is the number of complete pairs.",
                    "I et parret design er n antallet af komplette par.",
                ),
            ),
        ),
        (
            "multiple-groups",
            (
                "Más de dos grupos",
                "More than two groups",
                "Flere end to grupper",
            ),
            (
                "ANOVA evalúa una hipótesis global sobre medias. Un resultado global no identifica qué grupos difieren; los contrastes posteriores deben estar predefinidos o ajustarse por multiplicidad. Ejecutar muchas pruebas t sin control eleva la probabilidad de falsos positivos.",
                "ANOVA evaluates a global hypothesis about means. A global result does not identify which groups differ; subsequent contrasts should be predefined or adjusted for multiplicity. Running many unadjusted t tests increases false-positive probability.",
                "ANOVA vurderer en global hypotese om middelværdier. Et globalt resultat viser ikke, hvilke grupper der adskiller sig; efterfølgende kontraster bør være foruddefinerede eller justeret for multiplicitet. Mange ujusterede t-tests øger sandsynligheden for falske positiver.",
            ),
            (
                (
                    "La prueba global y los contrastes responden preguntas distintas.",
                    "The global test and contrasts answer different questions.",
                    "Den globale test og kontraster besvarer forskellige spørgsmål.",
                ),
                (
                    "La estrategia de comparaciones debe definirse antes de explorar resultados.",
                    "The comparison strategy should be defined before exploring results.",
                    "Sammenligningsstrategien bør defineres før resultater udforskes.",
                ),
            ),
        ),
        (
            "assumptions-robustness",
            (
                "Supuestos y robustez",
                "Assumptions and robustness",
                "Antagelser og robusthed",
            ),
            (
                "La normalidad relevante se refiere a errores o diferencias según el modelo, no necesariamente a cada variable cruda. Gráficos, valores extremos, tamaño muestral y diseño aportan más que una decisión automática basada en Shapiro-Wilk. Las pruebas por rangos cambian el estimando y no eliminan problemas de dependencia o sesgo.",
                "Relevant normality concerns errors or differences under the model, not necessarily every raw variable. Plots, outliers, sample size, and design provide more information than an automatic Shapiro-Wilk decision. Rank tests change the estimand and do not remove dependence or bias problems.",
                "Relevant normalitet vedrører fejl eller forskelle under modellen, ikke nødvendigvis hver rå variabel. Plots, ekstreme værdier, stikprøvestørrelse og design giver mere information end en automatisk Shapiro-Wilk-beslutning. Rangtests ændrer estimanden og fjerner ikke afhængighed eller bias.",
            ),
            (
                (
                    "Transformación, método robusto y modelo alternativo deben justificarse.",
                    "Transformation, robust method, and alternative model should be justified.",
                    "Transformation, robust metode og alternativ model bør begrundes.",
                ),
                (
                    "Un diagnóstico no sustituye conocimiento del proceso de medición.",
                    "A diagnostic does not replace knowledge of the measurement process.",
                    "En diagnostik erstatter ikke viden om måleprocessen.",
                ),
            ),
        ),
    ),
    examples=(
        (
            "m06.e01",
            (
                "Comparación independiente con Welch",
                "Independent comparison with Welch",
                "Uafhængig sammenligning med Welch",
            ),
            (
                "Compara una respuesta continua entre cinco controles y cinco tratados sin asumir varianzas iguales.",
                "Compare a continuous response between five controls and five treated units without assuming equal variances.",
                "Sammenlign et kontinuert respons mellem fem kontroller og fem behandlede enheder uden at antage ens varianser.",
            ),
            (
                (
                    "Las unidades pertenecen a grupos distintos.",
                    "Units belong to different groups.",
                    "Enhederne tilhører forskellige grupper.",
                ),
                (
                    "Se reporta treated−control con intervalo.",
                    "The treated−control contrast is reported with an interval.",
                    "Kontrasten behandlet−kontrol rapporteres med et interval.",
                ),
            ),
            """control <- c(7.1, 7.4, 6.9, 7.3, 7.0)
treated <- c(8.0, 8.4, 7.8, 8.1, 8.3)
fit <- t.test(treated, control, var.equal = FALSE)
difference <- mean(treated) - mean(control)
cat(sprintf("difference=%.2f\n", difference))
cat(sprintf("ci=[%.2f, %.2f]\n", fit$conf.int[1], fit$conf.int[2]))
cat(sprintf("p=%.4f", fit$p.value))
""",
            """difference=0.98
ci=[0.65, 1.31]
p=0.0001""",
            (
                "Welch conserva el contraste de medias y ajusta los grados de libertad cuando las varianzas difieren.",
                "Welch preserves the mean contrast and adjusts degrees of freedom when variances differ.",
                "Welch bevarer middelkontrasten og justerer frihedsgraderne, når varianserne er forskellige.",
            ),
        ),
        (
            "m06.e02",
            (
                "Comparación pareada",
                "Paired comparison",
                "Parret sammenligning",
            ),
            (
                "Analiza seis mediciones antes y después calculando la diferencia dentro de cada participante.",
                "Analyse six before-after measurements using the within-participant difference.",
                "Analysér seks før-efter-målinger ved hjælp af forskellen inden for hver deltager.",
            ),
            (
                (
                    "Cada fila representa la misma unidad en dos momentos.",
                    "Each row represents the same unit at two times.",
                    "Hver række repræsenterer samme enhed på to tidspunkter.",
                ),
                (
                    "La variabilidad relevante es la de las diferencias.",
                    "The relevant variability is that of the differences.",
                    "Den relevante variation er variationen i forskellene.",
                ),
            ),
            """before <- c(10.2, 9.8, 10.5, 11.0, 9.9, 10.4)
after <- c(9.4, 9.3, 9.8, 10.2, 9.1, 9.7)
fit <- t.test(before, after, paired = TRUE)
difference <- before - after
cat(sprintf("mean_difference=%.2f\n", mean(difference)))
cat(sprintf("ci=[%.2f, %.2f]\n", fit$conf.int[1], fit$conf.int[2]))
cat(sprintf("p=%.4f", fit$p.value))
""",
            """mean_difference=0.72
ci=[0.59, 0.84]
p=0.0000""",
            (
                "El análisis pareado elimina variación estable entre participantes y estima el cambio medio.",
                "The paired analysis removes stable between-participant variation and estimates mean change.",
                "Den parrede analyse fjerner stabil variation mellem deltagere og estimerer den gennemsnitlige ændring.",
            ),
        ),
    ),
    practices=(
        (
            "m06.p01",
            "DATA_INTERPRETATION",
            (
                "Clasifica como independiente o pareado: pacientes distintos por tratamiento; antes-después de los mismos pacientes.",
                "Classify as independent or paired: different patients by treatment; before-after in the same patients.",
                "Klassificér som uafhængigt eller parret: forskellige patienter efter behandling; før-efter hos de samme patienter.",
            ),
            (
                (
                    "Busca si una observación puede emparejarse con otra por unidad.",
                    "Ask whether one observation can be matched to another by unit.",
                    "Spørg om en observation kan matches med en anden efter enhed.",
                ),
            ),
            (
                "Pacientes distintos: independiente. Mismos pacientes: pareado.",
                "Different patients: independent. Same patients: paired.",
                "Forskellige patienter: uafhængigt. Samme patienter: parret.",
            ),
            (
                "El diseño determina la estructura del error.",
                "Design determines the error structure.",
                "Designet bestemmer fejlstrukturen.",
            ),
            "",
        ),
        (
            "m06.p02",
            "CODE_COMPLETION",
            (
                "Completa una prueba de Welch bilateral entre x e y.",
                "Complete a two-sided Welch test between x and y.",
                "Fuldfør en tosidet Welch-test mellem x og y.",
            ),
            (
                (
                    "No impongas varianzas iguales.",
                    "Do not impose equal variances.",
                    "Antag ikke ens varianser.",
                ),
            ),
            ("t.test(x, y, var.equal = FALSE, alternative = 'two.sided')",) * 3,
            (
                "Welch es el comportamiento predeterminado de t.test para dos muestras.",
                "Welch is the default two-sample behaviour of t.test.",
                "Welch er standardadfærden for to stikprøver i t.test.",
            ),
            "fit <- __________________________________________",
        ),
        (
            "m06.p03",
            "DEBUGGING",
            (
                "Corrige un análisis antes-después ejecutado como dos muestras independientes.",
                "Correct a before-after analysis run as two independent samples.",
                "Ret en før-efter-analyse udført som to uafhængige stikprøver.",
            ),
            (
                (
                    "Conserva la identidad de cada participante.",
                    "Preserve participant identity.",
                    "Bevar deltagernes identitet.",
                ),
            ),
            (
                "Analizar diferencias dentro de participante o usar t.test(before, after, paired=TRUE).",
                "Analyse within-participant differences or use t.test(before, after, paired=TRUE).",
                "Analysér forskelle inden for deltageren eller brug t.test(before, after, paired=TRUE).",
            ),
            (
                "El análisis independiente ignora covariación y usa un error estándar incorrecto.",
                "The independent analysis ignores covariance and uses the wrong standard error.",
                "Den uafhængige analyse ignorerer kovarians og bruger forkert standardfejl.",
            ),
            "",
        ),
        (
            "m06.p04",
            "PIPELINE_DESIGN",
            (
                "Diseña la comparación de tres grupos con dos contrastes científicos predefinidos.",
                "Design the comparison of three groups with two predefined scientific contrasts.",
                "Design sammenligningen af tre grupper med to foruddefinerede videnskabelige kontraster.",
            ),
            (
                (
                    "Separa prueba global y contrastes.",
                    "Separate the global test and contrasts.",
                    "Adskil global test og kontraster.",
                ),
            ),
            (
                "Validar diseño; ajustar ANOVA; inspeccionar residuos; evaluar prueba global; estimar los dos contrastes con intervalos y control de multiplicidad.",
                "Validate design; fit ANOVA; inspect residuals; evaluate the global test; estimate the two contrasts with intervals and multiplicity control.",
                "Validér design; tilpas ANOVA; inspicér residualer; vurder global test; estimér de to kontraster med intervaller og multiplicitetskontrol.",
            ),
            (
                "Los contrastes predefinidos preservan la pregunta científica.",
                "Predefined contrasts preserve the scientific question.",
                "Foruddefinerede kontraster bevarer det videnskabelige spørgsmål.",
            ),
            "",
        ),
        (
            "m06.p05",
            "ORAL_EXPLANATION",
            (
                "Explica por qué Shapiro-Wilk no debe decidir automáticamente entre t y Wilcoxon.",
                "Explain why Shapiro-Wilk should not automatically decide between t and Wilcoxon.",
                "Forklar hvorfor Shapiro-Wilk ikke automatisk bør afgøre valget mellem t og Wilcoxon.",
            ),
            (
                (
                    "Considera diseño, tamaño, extremos y estimando.",
                    "Consider design, size, outliers, and estimand.",
                    "Overvej design, størrelse, ekstreme værdier og estimand.",
                ),
            ),
            (
                "Una prueba diagnóstica tiene potencia limitada o excesiva según n; la decisión debe integrar gráficos, robustez, escala y pregunta científica.",
                "A diagnostic test has limited or excessive power depending on n; the decision should integrate plots, robustness, scale, and the scientific question.",
                "En diagnostisk test har begrænset eller overdreven styrke afhængigt af n; beslutningen bør integrere plots, robusthed, skala og det videnskabelige spørgsmål.",
            ),
            (
                "Wilcoxon no es simplemente una t sin normalidad y puede apuntar a otro estimando.",
                "Wilcoxon is not simply a t test without normality and may target another estimand.",
                "Wilcoxon er ikke blot en t-test uden normalitet og kan målrette en anden estimand.",
            ),
            "",
        ),
        (
            "m06.p06",
            "DATA_INTERPRETATION",
            (
                "Interpreta ANOVA p=0,01 sin afirmar que todos los grupos difieren.",
                "Interpret ANOVA p=0.01 without claiming that every group differs.",
                "Fortolk ANOVA p=0,01 uden at hævde, at alle grupper er forskellige.",
            ),
            (
                (
                    "La hipótesis global es que todas las medias son iguales.",
                    "The global hypothesis is that all means are equal.",
                    "Den globale hypotese er, at alle middelværdier er ens.",
                ),
            ),
            (
                "Existe evidencia contra la igualdad global de medias; se necesitan contrastes definidos para localizar y cuantificar diferencias.",
                "There is evidence against global equality of means; defined contrasts are needed to locate and quantify differences.",
                "Der er evidens mod global lighed af middelværdier; definerede kontraster kræves for at lokalisere og kvantificere forskelle.",
            ),
            (
                "El valor p global no identifica pares concretos.",
                "The global p-value does not identify particular pairs.",
                "Den globale p-værdi identificerer ikke bestemte par.",
            ),
            "",
        ),
    ),
    mcqs=(
        (
            "001",
            (
                "¿Qué prueba compara dos grupos independientes sin asumir varianzas iguales?",
                "Which test compares two independent groups without assuming equal variances?",
                "Hvilken test sammenligner to uafhængige grupper uden at antage ens varianser?",
            ),
            (
                ("a", ("Welch", "Welch", "Welch")),
                ("b", ("t pareada", "Paired t", "Parret t")),
                ("c", ("McNemar", "McNemar", "McNemar")),
                ("d", ("Correlación", "Correlation", "Korrelation")),
            ),
            "a",
            (
                "Welch ajusta el error estándar y los grados de libertad.",
                "Welch adjusts standard error and degrees of freedom.",
                "Welch justerer standardfejl og frihedsgrader.",
            ),
        ),
        (
            "002",
            (
                "¿Cuál es la unidad de análisis en un diseño antes-después?",
                "What is the analysis unit in a before-after design?",
                "Hvad er analyseenheden i et før-efter-design?",
            ),
            (
                (
                    "a",
                    ("Cada medición aislada", "Each isolated measurement", "Hver isoleret måling"),
                ),
                (
                    "b",
                    (
                        "La diferencia por participante",
                        "The participant-level difference",
                        "Forskellen pr. deltager",
                    ),
                ),
                (
                    "c",
                    (
                        "Cada grupo como una observación",
                        "Each group as one observation",
                        "Hver gruppe som én observation",
                    ),
                ),
                ("d", ("La mediana global", "The global median", "Den globale median")),
            ),
            "b",
            (
                "El pareamiento se representa mediante diferencias dentro de unidad.",
                "Pairing is represented through within-unit differences.",
                "Parring repræsenteres gennem forskelle inden for enheden.",
            ),
        ),
        (
            "003",
            (
                "¿Qué evalúa primero ANOVA?",
                "What does ANOVA evaluate first?",
                "Hvad vurderer ANOVA først?",
            ),
            (
                (
                    "a",
                    (
                        "Una hipótesis global de medias",
                        "A global hypothesis about means",
                        "En global hypotese om middelværdier",
                    ),
                ),
                (
                    "b",
                    (
                        "Cada par sin ajuste",
                        "Every pair without adjustment",
                        "Hvert par uden justering",
                    ),
                ),
                (
                    "c",
                    ("Normalidad de datos crudos", "Normality of raw data", "Normalitet af rådata"),
                ),
                ("d", ("Equivalencia clínica", "Clinical equivalence", "Klinisk ækvivalens")),
            ),
            "a",
            (
                "La prueba global pregunta si todas las medias pueden ser iguales.",
                "The global test asks whether all means may be equal.",
                "Den globale test spørger, om alle middelværdier kan være ens.",
            ),
        ),
        (
            "004",
            (
                "¿Qué problema crean muchas pruebas t sin ajuste?",
                "What problem is created by many unadjusted t tests?",
                "Hvilket problem skaber mange ujusterede t-tests?",
            ),
            (
                ("a", ("Inflación del error tipo I", "Inflated type I error", "Øget type I-fejl")),
                ("b", ("Menor SD automática", "Automatically lower SD", "Automatisk lavere SD")),
                ("c", ("Mayor n", "Larger n", "Større n")),
                ("d", ("Pareamiento", "Pairing", "Parring")),
            ),
            "a",
            (
                "Cada contraste adicional ofrece otra oportunidad de falso positivo.",
                "Each additional contrast offers another false-positive opportunity.",
                "Hver ekstra kontrast giver endnu en mulighed for falsk positiv.",
            ),
        ),
        (
            "005",
            (
                "¿Qué supuesto no corrige una prueba por rangos?",
                "Which assumption problem is not fixed by a rank test?",
                "Hvilket antagelsesproblem løses ikke af en rangtest?",
            ),
            (
                ("a", ("Dependencia ignorada", "Ignored dependence", "Ignoreret afhængighed")),
                ("b", ("Escala ordinal", "Ordinal scale", "Ordinal skala")),
                ("c", ("Valores extremos", "Outliers", "Ekstreme værdier")),
                ("d", ("Asimetría", "Skewness", "Skævhed")),
            ),
            "a",
            (
                "La estructura de dependencia pertenece al diseño.",
                "Dependence structure belongs to the design.",
                "Afhængighedsstrukturen tilhører designet.",
            ),
        ),
        (
            "006",
            (
                "¿Qué debe inspeccionarse para una prueba t pareada?",
                "What should be inspected for a paired t test?",
                "Hvad bør inspiceres for en parret t-test?",
            ),
            (
                (
                    "a",
                    (
                        "Distribución de diferencias",
                        "Distribution of differences",
                        "Fordelingen af forskelle",
                    ),
                ),
                ("b", ("Solo cada margen", "Each margin only", "Kun hver marginalfordeling")),
                ("c", ("Color del grupo", "Group colour", "Gruppefarve")),
                ("d", ("Número de columnas", "Number of columns", "Antal kolonner")),
            ),
            "a",
            (
                "La prueba opera sobre diferencias dentro de unidad.",
                "The test operates on within-unit differences.",
                "Testen arbejder på forskelle inden for enheden.",
            ),
        ),
        (
            "007",
            (
                "¿Qué sigue a un ANOVA global significativo?",
                "What follows a significant global ANOVA?",
                "Hvad følger efter en signifikant global ANOVA?",
            ),
            (
                (
                    "a",
                    (
                        "Contrastes definidos con control de multiplicidad",
                        "Defined contrasts with multiplicity control",
                        "Definerede kontraster med multiplicitetskontrol",
                    ),
                ),
                (
                    "b",
                    (
                        "Afirmar que todos difieren",
                        "Claim all groups differ",
                        "Hævde at alle grupper er forskellige",
                    ),
                ),
                ("c", ("Eliminar grupos", "Delete groups", "Slette grupper")),
                ("d", ("Aceptar causalidad", "Accept causality", "Acceptere kausalitet")),
            ),
            "a",
            (
                "Los contrastes localizan y cuantifican diferencias.",
                "Contrasts locate and quantify differences.",
                "Kontraster lokaliserer og kvantificerer forskelle.",
            ),
        ),
        (
            "008",
            (
                "¿Qué determina primero la selección del método?",
                "What first determines method selection?",
                "Hvad bestemmer først metodevalget?",
            ),
            (
                ("a", ("Diseño y estimando", "Design and estimand", "Design og estimand")),
                ("b", ("Valor p observado", "Observed p-value", "Observeret p-værdi")),
                ("c", ("Prueba más familiar", "Most familiar test", "Mest kendte test")),
                ("d", ("Mayor significación", "Greatest significance", "Størst signifikans")),
            ),
            "a",
            (
                "La prueba debe representar la pregunta y la dependencia.",
                "The test must represent the question and dependence.",
                "Testen skal repræsentere spørgsmålet og afhængigheden.",
            ),
        ),
    ),
    true_false=(
        (
            "009",
            (
                "Welch requiere varianzas exactamente iguales.",
                "Welch requires exactly equal variances.",
                "Welch kræver præcis ens varianser.",
            ),
            False,
            (
                "Welch se diseñó para no imponer igualdad de varianzas.",
                "Welch was designed not to impose equal variances.",
                "Welch er designet til ikke at kræve ens varianser.",
            ),
        ),
        (
            "010",
            (
                "Un diseño pareado se analiza mediante diferencias dentro de unidad.",
                "A paired design is analysed through within-unit differences.",
                "Et parret design analyseres gennem forskelle inden for enheden.",
            ),
            True,
            (
                "La diferencia conserva el emparejamiento.",
                "The difference preserves pairing.",
                "Forskellen bevarer parringen.",
            ),
        ),
        (
            "011",
            (
                "ANOVA significativo implica que todos los pares difieren.",
                "A significant ANOVA implies every pair differs.",
                "En signifikant ANOVA indebærer, at alle par er forskellige.",
            ),
            False,
            (
                "Solo rechaza la igualdad global.",
                "It only rejects global equality.",
                "Den forkaster kun global lighed.",
            ),
        ),
        (
            "012",
            (
                "Múltiples contrastes pueden requerir ajuste.",
                "Multiple contrasts may require adjustment.",
                "Multiple kontraster kan kræve justering.",
            ),
            True,
            (
                "La multiplicidad aumenta oportunidades de error tipo I.",
                "Multiplicity increases type I error opportunities.",
                "Multiplicitet øger mulighederne for type I-fejl.",
            ),
        ),
        (
            "013",
            (
                "Una prueba no paramétrica corrige automáticamente la dependencia.",
                "A non-parametric test automatically fixes dependence.",
                "En ikkeparametrisk test løser automatisk afhængighed.",
            ),
            False,
            (
                "La dependencia debe modelarse según el diseño.",
                "Dependence must be handled according to design.",
                "Afhængighed skal håndteres efter designet.",
            ),
        ),
        (
            "014",
            (
                "Shapiro-Wilk por sí solo debe decidir el método.",
                "Shapiro-Wilk alone should decide the method.",
                "Shapiro-Wilk alene bør afgøre metoden.",
            ),
            False,
            (
                "La decisión integra diseño, gráficos, robustez y estimando.",
                "The decision integrates design, plots, robustness, and estimand.",
                "Beslutningen integrerer design, plots, robusthed og estimand.",
            ),
        ),
        (
            "015",
            (
                "Réplicas técnicas de una muestra son unidades biológicas independientes.",
                "Technical replicates from one sample are independent biological units.",
                "Tekniske replikater fra én prøve er uafhængige biologiske enheder.",
            ),
            False,
            (
                "Comparten la misma unidad experimental.",
                "They share the same experimental unit.",
                "De deler samme eksperimentelle enhed.",
            ),
        ),
        (
            "016",
            (
                "El resultado debe incluir diferencia, intervalo y supuestos relevantes.",
                "The result should include difference, interval, and relevant assumptions.",
                "Resultatet bør indeholde forskel, interval og relevante antagelser.",
            ),
            True,
            (
                "Esto comunica magnitud, precisión y validez del procedimiento.",
                "This communicates magnitude, precision, and procedural validity.",
                "Dette kommunikerer størrelse, præcision og procedurens gyldighed.",
            ),
        ),
    ),
    tutor=(
        (
            "La comparación de grupos válida comienza por el diseño y la unidad experimental, selecciona un estimando y método coherentes, evalúa supuestos y comunica contrastes con magnitud, intervalos y control de multiplicidad.",
            "Valid group comparison begins with design and experimental unit, selects a coherent estimand and method, evaluates assumptions, and communicates contrasts with magnitude, intervals, and multiplicity control.",
            "Gyldig gruppesammenligning begynder med design og eksperimentel enhed, vælger en sammenhængende estimand og metode, vurderer antagelser og kommunikerer kontraster med størrelse, intervaller og multiplicitetskontrol.",
        ),
        (
            (
                "Welch es el punto de partida para dos grupos independientes.",
                "Welch is the starting point for two independent groups.",
                "Welch er udgangspunktet for to uafhængige grupper.",
            ),
            (
                "El pareamiento cambia la unidad del análisis a diferencias.",
                "Pairing changes the analysis unit to differences.",
                "Parring ændrer analyseenheden til forskelle.",
            ),
            (
                "ANOVA global no localiza contrastes.",
                "Global ANOVA does not locate contrasts.",
                "Global ANOVA lokaliserer ikke kontraster.",
            ),
            (
                "Los supuestos se evalúan con diseño y diagnósticos.",
                "Assumptions are evaluated with design and diagnostics.",
                "Antagelser vurderes med design og diagnostik.",
            ),
        ),
        (
            ("Ignorar pareamiento.", "Ignoring pairing.", "At ignorere parring."),
            (
                "Asumir varianzas iguales por defecto.",
                "Assuming equal variances by default.",
                "At antage ens varianser som standard.",
            ),
            (
                "Interpretar ANOVA como diferencias en todos los pares.",
                "Interpreting ANOVA as differences in every pair.",
                "At fortolke ANOVA som forskelle i alle par.",
            ),
        ),
        (
            (
                "¿Cuál es la unidad experimental?",
                "What is the experimental unit?",
                "Hvad er den eksperimentelle enhed?",
            ),
            (
                "¿Las observaciones pueden emparejarse?",
                "Can observations be paired?",
                "Kan observationerne parres?",
            ),
            (
                "¿Qué contraste responde la pregunta?",
                "Which contrast answers the question?",
                "Hvilken kontrast besvarer spørgsmålet?",
            ),
        ),
        (
            (
                "Selecciona método según diseño.",
                "Selects method according to design.",
                "Vælger metode efter design.",
            ),
            (
                "Evalúa supuestos sin automatismos.",
                "Evaluates assumptions without automatic rules.",
                "Vurderer antagelser uden automatik.",
            ),
            (
                "Controla e interpreta comparaciones múltiples.",
                "Controls and interprets multiple comparisons.",
                "Kontrollerer og fortolker multiple sammenligninger.",
            ),
        ),
        (
            (
                "No inventar independencia ni pareamiento.",
                "Do not invent independence or pairing.",
                "Opfind ikke uafhængighed eller parring.",
            ),
            (
                "No recomendar pruebas solo por el valor p obtenido.",
                "Do not recommend tests based only on the obtained p-value.",
                "Anbefal ikke tests alene ud fra den opnåede p-værdi.",
            ),
            (
                "Responder en el idioma activo.",
                "Respond in the active language.",
                "Svar på det aktive sprog.",
            ),
        ),
        (
            "SDU ODIN BMB830 active course description approved 2025-03-06",
            "R base stats documentation: t.test, aov, pairwise.t.test, wilcox.test",
            "Frequentist model diagnostics and multiplicity principles",
        ),
    ),
)

LOCALIZED_MODULE_06_GROUP_COMPARISON = build_module(_SPEC)
LOCALIZED_OBJECTIVE_QUESTION_BANK_06 = build_question_bank(_SPEC)
MODULE_06_GROUP_COMPARISON: LearningModule = LOCALIZED_MODULE_06_GROUP_COMPARISON.materialize(
    AppLocale.SPANISH_SPAIN
)
OBJECTIVE_QUESTION_BANK_06: tuple[AssessmentItem, ...] = materialize_bank(
    LOCALIZED_OBJECTIVE_QUESTION_BANK_06
)


def materialize_module_06_question_bank(
    locale: AppLocale | str = AppLocale.SPANISH_SPAIN,
) -> tuple[AssessmentItem, ...]:
    """Return the module-6 objective bank in one locale."""

    return materialize_bank(LOCALIZED_OBJECTIVE_QUESTION_BANK_06, locale)


__all__ = [
    "LOCALIZED_MODULE_06_GROUP_COMPARISON",
    "LOCALIZED_OBJECTIVE_QUESTION_BANK_06",
    "MODULE_06_GROUP_COMPARISON",
    "OBJECTIVE_QUESTION_BANK_06",
    "materialize_module_06_question_bank",
]
