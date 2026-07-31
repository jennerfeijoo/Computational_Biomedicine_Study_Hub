"""BMB830 module 3: probability, sampling, and reference distributions."""

from __future__ import annotations

from ...i18n import AppLocale
from ..localized_models import LocalizedLearningModule
from ..models import AssessmentItem, LearningModule
from .standard import StandardModuleSpec, build_module, build_question_bank, materialize_bank

_SPEC = StandardModuleSpec(
    module_id="bmb830.m03",
    title=(
        "Probabilidad, muestreo y distribuciones",
        "Probability, sampling, and distributions",
        "Sandsynlighed, stikprøver og fordelinger",
    ),
    summary=(
        "Conecta eventos, probabilidad condicionada, modelos de Bernoulli y binomial, distribución normal, error estándar y simulación con preguntas biomédicas reproducibles.",
        "Connect events, conditional probability, Bernoulli and binomial models, the normal distribution, standard error, and simulation to reproducible biomedical questions.",
        "Forbind hændelser, betinget sandsynlighed, Bernoulli- og binomialmodeller, normalfordelingen, standardfejl og simulation med reproducerbare biomedicinske spørgsmål.",
    ),
    objectives=(
        (
            "m03.o1",
            (
                "Calcular probabilidades conjuntas, marginales y condicionadas.",
                "Calculate joint, marginal, and conditional probabilities.",
                "Beregne fælles, marginale og betingede sandsynligheder.",
            ),
        ),
        (
            "m03.o2",
            (
                "Seleccionar distribuciones discretas o continuas según el mecanismo de datos.",
                "Select discrete or continuous distributions according to the data mechanism.",
                "Vælge diskrete eller kontinuerte fordelinger ud fra datamekanismen.",
            ),
        ),
        (
            "m03.o3",
            (
                "Distinguir variabilidad de observaciones, distribución muestral y error estándar.",
                "Distinguish observation variability, sampling distribution, and standard error.",
                "Skelne mellem observationsvariation, stikprøvefordeling og standardfejl.",
            ),
        ),
        (
            "m03.o4",
            (
                "Usar simulación reproducible para verificar cálculos y explorar supuestos.",
                "Use reproducible simulation to verify calculations and explore assumptions.",
                "Bruge reproducerbar simulation til at kontrollere beregninger og undersøge antagelser.",
            ),
        ),
    ),
    concepts=(
        (
            "events-conditioning",
            (
                "Eventos y condicionamiento",
                "Events and conditioning",
                "Hændelser og betingning",
            ),
            (
                "Una probabilidad se refiere a un espacio de resultados y a un evento definido. La probabilidad condicionada P(A|B) restringe el espacio a B. Confundir P(A|B) con P(B|A) es especialmente peligroso al interpretar pruebas diagnósticas.",
                "A probability refers to an outcome space and a defined event. Conditional probability P(A|B) restricts the space to B. Confusing P(A|B) with P(B|A) is especially dangerous when interpreting diagnostic tests.",
                "En sandsynlighed refererer til et udfaldsrum og en defineret hændelse. Betinget sandsynlighed P(A|B) begrænser rummet til B. At forveksle P(A|B) med P(B|A) er særligt farligt ved fortolkning af diagnostiske tests.",
            ),
            (
                (
                    "Declara siempre qué evento aparece en el denominador.",
                    "Always state which event is in the denominator.",
                    "Angiv altid hvilken hændelse der står i nævneren.",
                ),
                (
                    "Independencia implica P(A|B)=P(A), no ausencia de asociación observada en una muestra.",
                    "Independence implies P(A|B)=P(A), not absence of observed association in one sample.",
                    "Uafhængighed indebærer P(A|B)=P(A), ikke fravær af observeret association i én stikprøve.",
                ),
            ),
        ),
        (
            "discrete-models",
            (
                "Bernoulli y binomial",
                "Bernoulli and binomial",
                "Bernoulli og binomial",
            ),
            (
                "Bernoulli representa un ensayo con dos resultados y probabilidad p. La binomial cuenta éxitos en n ensayos con el mismo p e independencia condicionada. Si p varía entre unidades o existen dependencias, la variabilidad puede superar la binomial.",
                "Bernoulli represents one trial with two outcomes and probability p. The binomial counts successes in n trials with the same p and conditional independence. If p varies between units or trials are dependent, variability may exceed the binomial model.",
                "Bernoulli repræsenterer ét forsøg med to udfald og sandsynlighed p. Binomialfordelingen tæller succeser i n forsøg med samme p og betinget uafhængighed. Hvis p varierer mellem enheder, eller forsøg er afhængige, kan variationen overstige binomialmodellen.",
            ),
            (
                (
                    "Comprueba número fijo de ensayos y definición estable de éxito.",
                    "Check fixed trial count and a stable definition of success.",
                    "Kontrollér fast antal forsøg og en stabil definition af succes.",
                ),
                (
                    "La sobredispersión indica que el modelo puede ser insuficiente.",
                    "Overdispersion indicates the model may be insufficient.",
                    "Overdispersion indikerer at modellen kan være utilstrækkelig.",
                ),
            ),
        ),
        (
            "continuous-models",
            (
                "Distribución normal y estandarización",
                "Normal distribution and standardisation",
                "Normalfordeling og standardisering",
            ),
            (
                "La normal es una distribución continua simétrica definida por media y desviación estándar. Un z-score expresa distancia a la media en unidades de desviación estándar. La normalidad es un supuesto del modelo o una aproximación, no una propiedad automática de toda medición biológica.",
                "The normal is a symmetric continuous distribution defined by mean and standard deviation. A z-score expresses distance from the mean in standard-deviation units. Normality is a model assumption or approximation, not an automatic property of every biological measurement.",
                "Normalfordelingen er en symmetrisk kontinuert fordeling defineret ved gennemsnit og standardafvigelse. En z-score udtrykker afstand fra gennemsnittet i standardafvigelsesenheder. Normalitet er en modelantagelse eller approximation, ikke en automatisk egenskab ved enhver biologisk måling.",
            ),
            (
                (
                    "Inspecciona escala y forma antes de usar una aproximación normal.",
                    "Inspect scale and shape before using a normal approximation.",
                    "Undersøg skala og form før en normalapproximation anvendes.",
                ),
                (
                    "Un z-score no convierte una observación en probabilidad por sí solo.",
                    "A z-score does not by itself turn an observation into a probability.",
                    "En z-score omdanner ikke i sig selv en observation til en sandsynlighed.",
                ),
            ),
        ),
        (
            "sampling-simulation",
            (
                "Distribución muestral y simulación",
                "Sampling distribution and simulation",
                "Stikprøvefordeling og simulation",
            ),
            (
                "Una estadística cambia entre muestras hipotéticas. Su distribución muestral cuantifica esa variación y su desviación estándar es el error estándar. La simulación puede aproximarla si reproduce el mecanismo de muestreo; set.seed hace reproducible la secuencia pseudoaleatoria.",
                "A statistic changes across hypothetical samples. Its sampling distribution quantifies that variation, and its standard deviation is the standard error. Simulation can approximate it when it reproduces the sampling mechanism; set.seed makes the pseudo-random sequence reproducible.",
                "En statistik ændrer sig mellem hypotetiske stikprøver. Dens stikprøvefordeling kvantificerer variationen, og dens standardafvigelse er standardfejlen. Simulation kan approksimere den, når stikprøvemekanismen gengives; set.seed gør den pseudo-tilfældige sekvens reproducerbar.",
            ),
            (
                (
                    "El error estándar no describe dispersión entre individuos.",
                    "Standard error does not describe spread among individuals.",
                    "Standardfejl beskriver ikke spredning mellem individer.",
                ),
                (
                    "La unidad independiente determina el tamaño muestral efectivo.",
                    "The independent unit determines effective sample size.",
                    "Den uafhængige enhed bestemmer den effektive stikprøvestørrelse.",
                ),
            ),
        ),
    ),
    examples=(
        (
            "m03.e01",
            (
                "Probabilidad binomial exacta",
                "Exact binomial probability",
                "Eksakt binomial sandsynlighed",
            ),
            (
                "Calcula la probabilidad de exactamente tres respuestas en cinco ensayos con p=0,2.",
                "Calculate the probability of exactly three responses in five trials with p=0.2.",
                "Beregn sandsynligheden for præcis tre responser i fem forsøg med p=0,2.",
            ),
            (
                (
                    "El número de ensayos es fijo y cada resultado es binario.",
                    "The number of trials is fixed and each outcome is binary.",
                    "Antallet af forsøg er fast, og hvert udfald er binært.",
                ),
                (
                    "dbinom devuelve la masa en un número exacto de éxitos.",
                    "dbinom returns the mass at an exact number of successes.",
                    "dbinom returnerer massen ved et præcist antal succeser.",
                ),
            ),
            """probability <- dbinom(3, size = 5, prob = 0.2)
cat(sprintf("P(X=3)=%.4f\n", probability))
""",
            "P(X=3)=0.2048",
            (
                "El cálculo depende de que los cinco ensayos compartan p y sean independientes bajo el modelo.",
                "The calculation depends on the five trials sharing p and being independent under the model.",
                "Beregningen afhænger af at de fem forsøg deler p og er uafhængige under modellen.",
            ),
        ),
        (
            "m03.e02",
            (
                "Error estándar de una proporción",
                "Standard error of a proportion",
                "Standardfejl for en proportion",
            ),
            (
                "Aproxima la incertidumbre de una proporción 0,30 obtenida de 100 unidades independientes.",
                "Approximate uncertainty for a proportion of 0.30 obtained from 100 independent units.",
                "Approksimér usikkerheden for en proportion på 0,30 fra 100 uafhængige enheder.",
            ),
            (
                (
                    "El error estándar usa p(1-p)/n.",
                    "The standard error uses p(1-p)/n.",
                    "Standardfejlen bruger p(1-p)/n.",
                ),
                (
                    "El intervalo aproximado usa 1,96 errores estándar.",
                    "The approximate interval uses 1.96 standard errors.",
                    "Det omtrentlige interval bruger 1,96 standardfejl.",
                ),
            ),
            """p <- 0.30
n <- 100
se <- sqrt(p * (1 - p) / n)
lower <- p - 1.96 * se
upper <- p + 1.96 * se
cat(sprintf("SE=%.4f\n", se))
cat(sprintf("interval=%.3f to %.3f\n", lower, upper))
""",
            """SE=0.0458
interval=0.210 to 0.390""",
            (
                "La aproximación requiere unidades independientes y puede ser deficiente cerca de 0 o 1 o con muestras pequeñas.",
                "The approximation requires independent units and may be poor near 0 or 1 or with small samples.",
                "Approksimationen kræver uafhængige enheder og kan være dårlig nær 0 eller 1 eller ved små stikprøver.",
            ),
        ),
    ),
    practices=(
        (
            "m03.p01",
            "DATA_INTERPRETATION",
            (
                "Distingue P(enfermedad|positivo) de P(positivo|enfermedad).",
                "Distinguish P(disease|positive) from P(positive|disease).",
                "Skeln mellem P(sygdom|positiv) og P(positiv|sygdom).",
            ),
            (("Observa qué evento restringe el denominador.", "Observe which event restricts the denominator.", "Se hvilken hændelse der begrænser nævneren."),),
            (
                "La primera es valor predictivo positivo; la segunda es sensibilidad.",
                "The first is positive predictive value; the second is sensitivity.",
                "Den første er positiv prædiktiv værdi; den anden er sensitivitet.",
            ),
            (
                "Invertir el condicionamiento cambia la población de referencia.",
                "Reversing conditioning changes the reference population.",
                "At vende betingningen ændrer referencepopulationen.",
            ),
            "",
        ),
        (
            "m03.p02",
            "MULTIPLE_CHOICE",
            (
                "Elige un modelo para el número de positivos entre 20 ensayos comparables.",
                "Choose a model for the number of positives among 20 comparable trials.",
                "Vælg en model for antallet af positive blandt 20 sammenlignelige forsøg.",
            ),
            (("El resultado individual es binario.", "The individual outcome is binary.", "Det individuelle udfald er binært."),),
            (
                "Binomial, si p es común y existe independencia condicionada.",
                "Binomial, if p is common and conditional independence holds.",
                "Binomial, hvis p er fælles og betinget uafhængighed gælder.",
            ),
            (
                "El mecanismo, no solo el tipo numérico, define la distribución.",
                "The mechanism, not merely the numeric type, defines the distribution.",
                "Mekanismen, ikke kun den numeriske type, definerer fordelingen.",
            ),
            "",
        ),
        (
            "m03.p03",
            "CODE_COMPLETION",
            (
                "Completa la probabilidad de exactamente k éxitos.",
                "Complete the probability of exactly k successes.",
                "Fuldfør sandsynligheden for præcis k succeser.",
            ),
            (("Usa dbinom.", "Use dbinom.", "Brug dbinom."),),
            (
                "dbinom(k, size = n, prob = p)",
                "dbinom(k, size = n, prob = p)",
                "dbinom(k, size = n, prob = p)",
            ),
            (
                "dbinom calcula una masa puntual, no una acumulada.",
                "dbinom calculates point mass, not a cumulative probability.",
                "dbinom beregner punktmasse, ikke kumuleret sandsynlighed.",
            ),
            "probability <- __________________________",
        ),
        (
            "m03.p04",
            "CODE_TRACING",
            (
                "Explica qué fija set.seed(42) y qué no fija.",
                "Explain what set.seed(42) fixes and what it does not fix.",
                "Forklar hvad set.seed(42) fastlægger og ikke fastlægger.",
            ),
            (("Piensa en la secuencia pseudoaleatoria.", "Think about the pseudo-random sequence.", "Tænk på den pseudo-tilfældige sekvens."),),
            (
                "Fija la secuencia para el mismo generador y código; no valida el modelo de simulación.",
                "It fixes the sequence for the same generator and code; it does not validate the simulation model.",
                "Det fastlægger sekvensen for samme generator og kode; det validerer ikke simulationsmodellen.",
            ),
            (
                "Reproducibilidad computacional y validez científica son distintas.",
                "Computational reproducibility and scientific validity are distinct.",
                "Beregningsmæssig reproducerbarhed og videnskabelig gyldighed er forskellige.",
            ),
            "set.seed(42)",
        ),
        (
            "m03.p05",
            "DEBUGGING",
            (
                "Corrige el uso de n=300 cuando existen 100 pacientes con tres réplicas cada uno.",
                "Correct the use of n=300 when there are 100 patients with three replicates each.",
                "Korrigér brugen af n=300 når der er 100 patienter med tre replikater hver.",
            ),
            (("Identifica unidades independientes.", "Identify independent units.", "Identificér uafhængige enheder."),),
            (
                "El tamaño efectivo básico es 100; las réplicas requieren un modelo de dependencia.",
                "The basic effective size is 100; replicates require a dependence model.",
                "Den grundlæggende effektive størrelse er 100; replikater kræver en afhængighedsmodel.",
            ),
            (
                "Contar mediciones como unidades independientes subestima incertidumbre.",
                "Counting measurements as independent units underestimates uncertainty.",
                "At tælle målinger som uafhængige enheder undervurderer usikkerhed.",
            ),
            "se <- sd(values) / sqrt(300)",
        ),
        (
            "m03.p06",
            "ORAL_EXPLANATION",
            (
                "Explica la diferencia entre desviación estándar y error estándar.",
                "Explain the difference between standard deviation and standard error.",
                "Forklar forskellen mellem standardafvigelse og standardfejl.",
            ),
            (("Una describe individuos; la otra, un estimador.", "One describes individuals; the other an estimator.", "Den ene beskriver individer; den anden en estimator."),),
            (
                "La desviación estándar resume variación de observaciones; el error estándar resume variación de una estadística entre muestras.",
                "Standard deviation summarises variation among observations; standard error summarises variation of a statistic across samples.",
                "Standardafvigelse opsummerer variation mellem observationer; standardfejl opsummerer variation af en statistik mellem stikprøver.",
            ),
            (
                "Un error estándar pequeño no implica poca variabilidad biológica individual.",
                "A small standard error does not imply little individual biological variability.",
                "En lille standardfejl indebærer ikke lille individuel biologisk variation.",
            ),
            "",
        ),
    ),
    mcqs=(
        ("001", ("¿Cuál expresa sensibilidad?", "Which expression represents sensitivity?", "Hvilket udtryk repræsenterer sensitivitet?"), (("a", ("P(enfermedad|positivo)", "P(disease|positive)", "P(sygdom|positiv)")), ("b", ("P(positivo|enfermedad)", "P(positive|disease)", "P(positiv|sygdom)")), ("c", ("P(enfermedad)", "P(disease)", "P(sygdom)")), ("d", ("P(positivo)", "P(positive)", "P(positiv)"))), "b", ("Sensibilidad condiciona en enfermedad.", "Sensitivity conditions on disease.", "Sensitivitet betinger på sygdom.")),
        ("002", ("¿Qué modelo cuenta éxitos en n ensayos?", "Which model counts successes in n trials?", "Hvilken model tæller succeser i n forsøg?"), (("binomial", ("Binomial", "Binomial", "Binomial")), ("normal", ("Normal", "Normal", "Normal")), ("uniform", ("Uniforme", "Uniform", "Uniform")), ("exponential", ("Exponencial", "Exponential", "Eksponential"))), "binomial", ("La binomial modela conteos de éxitos.", "The binomial models success counts.", "Binomialfordelingen modellerer antal succeser.")),
        ("003", ("¿Qué devuelve dbinom(k,...)?", "What does dbinom(k,...) return?", "Hvad returnerer dbinom(k,...)?"), (("point", ("P(X=k)", "P(X=k)", "P(X=k)")), ("cum", ("P(X≤k)", "P(X≤k)", "P(X≤k)")), ("sample", ("Una muestra", "A sample", "En stikprøve")), ("mean", ("La media", "The mean", "Gennemsnittet"))), "point", ("dbinom es masa puntual.", "dbinom is point mass.", "dbinom er punktmasse.")),
        ("004", ("¿Qué describe el error estándar?", "What does standard error describe?", "Hvad beskriver standardfejl?"), (("statistic", ("Variación del estimador", "Estimator variation", "Estimatorens variation")), ("individual", ("Variación individual", "Individual variation", "Individuel variation")), ("range", ("Rango observado", "Observed range", "Observeret interval")), ("missing", ("Ausencia", "Missingness", "Manglende data"))), "statistic", ("Es la desviación estándar de la distribución muestral.", "It is the standard deviation of the sampling distribution.", "Det er standardafvigelsen for stikprøvefordelingen.")),
        ("005", ("¿Qué hace set.seed?", "What does set.seed do?", "Hvad gør set.seed?"), (("sequence", ("Fija secuencia pseudoaleatoria", "Fixes pseudo-random sequence", "Fastlægger pseudo-tilfældig sekvens")), ("truth", ("Valida el modelo", "Validates the model", "Validerer modellen")), ("normal", ("Hace normales los datos", "Makes data normal", "Gør data normale")), ("independent", ("Crea independencia", "Creates independence", "Skaber uafhængighed"))), "sequence", ("La semilla permite repetir la secuencia.", "The seed permits repeating the sequence.", "Seedet gør sekvensen gentagelig.")),
        ("006", ("¿Qué define el n efectivo?", "What defines effective n?", "Hvad definerer effektivt n?"), (("independent", ("Unidades independientes", "Independent units", "Uafhængige enheder")), ("rows", ("Número de filas", "Number of rows", "Antal rækker")), ("columns", ("Número de columnas", "Number of columns", "Antal kolonner")), ("files", ("Número de archivos", "Number of files", "Antal filer"))), "independent", ("Las réplicas correlacionadas no añaden una unidad completa.", "Correlated replicates do not add a full unit.", "Korrelerede replikater tilføjer ikke en fuld enhed.")),
        ("007", ("¿Qué distribución es continua y simétrica?", "Which distribution is continuous and symmetric?", "Hvilken fordeling er kontinuert og symmetrisk?"), (("normal", ("Normal", "Normal", "Normal")), ("binomial", ("Binomial", "Binomial", "Binomial")), ("bernoulli", ("Bernoulli", "Bernoulli", "Bernoulli")), ("categorical", ("Categórica", "Categorical", "Kategorisk"))), "normal", ("La normal está definida por media y desviación estándar.", "The normal is defined by mean and standard deviation.", "Normalfordelingen defineres ved gennemsnit og standardafvigelse.")),
        ("008", ("¿Qué indica sobredispersión binomial?", "What does binomial overdispersion indicate?", "Hvad indikerer binomial overdispersion?"), (("insufficient", ("Modelo insuficiente", "Insufficient model", "Utilstrækkelig model")), ("perfect", ("Ajuste perfecto", "Perfect fit", "Perfekt fit")), ("normal", ("Normalidad", "Normality", "Normalitet")), ("missing", ("Solo NA", "Only NA", "Kun NA"))), "insufficient", ("Puede reflejar heterogeneidad o dependencia.", "It may reflect heterogeneity or dependence.", "Det kan afspejle heterogenitet eller afhængighed.")),
    ),
    true_false=(
        ("009", ("P(A|B) y P(B|A) son intercambiables.", "P(A|B) and P(B|A) are interchangeable.", "P(A|B) og P(B|A) kan byttes."), False, ("Tienen denominadores distintos.", "They have different denominators.", "De har forskellige nævnere.")),
        ("010", ("La binomial supone un p común bajo el modelo.", "The binomial assumes a common p under the model.", "Binomialfordelingen antager et fælles p under modellen."), True, ("Es parte del mecanismo binomial.", "It is part of the binomial mechanism.", "Det er en del af binomialmekanismen.")),
        ("011", ("Toda variable continua es normal.", "Every continuous variable is normal.", "Enhver kontinuert variabel er normal."), False, ("Continuidad no implica normalidad.", "Continuity does not imply normality.", "Kontinuitet indebærer ikke normalitet.")),
        ("012", ("El error estándar suele disminuir al aumentar n independiente.", "Standard error usually decreases as independent n increases.", "Standardfejl falder normalt når uafhængigt n stiger."), True, ("Frecuentemente escala con 1/sqrt(n).", "It often scales with 1/sqrt(n).", "Det skalerer ofte med 1/sqrt(n).")),
        ("013", ("Tres réplicas del mismo paciente son tres pacientes independientes.", "Three replicates from one patient are three independent patients.", "Tre replikater fra én patient er tre uafhængige patienter."), False, ("Comparten unidad biológica.", "They share a biological unit.", "De deler biologisk enhed.")),
        ("014", ("Una simulación válida debe representar el mecanismo relevante.", "A valid simulation must represent the relevant mechanism.", "En gyldig simulation skal repræsentere den relevante mekanisme."), True, ("Repetir código incorrecto no valida supuestos.", "Repeating incorrect code does not validate assumptions.", "Gentagelse af forkert kode validerer ikke antagelser.")),
        ("015", ("set.seed demuestra que el modelo es correcto.", "set.seed proves the model is correct.", "set.seed beviser at modellen er korrekt."), False, ("Solo controla reproducibilidad pseudoaleatoria.", "It only controls pseudo-random reproducibility.", "Det kontrollerer kun pseudo-tilfældig reproducerbarhed.")),
        ("016", ("La desviación estándar y el error estándar responden a preguntas distintas.", "Standard deviation and standard error answer different questions.", "Standardafvigelse og standardfejl besvarer forskellige spørgsmål."), True, ("Una describe observaciones y la otra un estimador.", "One describes observations and the other an estimator.", "Den ene beskriver observationer og den anden en estimator.")),
    ),
    tutor=(
        (
            "La probabilidad biomédica requiere definir eventos y condicionamiento, elegir una distribución coherente con el mecanismo, reconocer unidades independientes y distinguir variación individual de incertidumbre del estimador.",
            "Biomedical probability requires defining events and conditioning, choosing a distribution consistent with the mechanism, recognising independent units, and distinguishing individual variation from estimator uncertainty.",
            "Biomedicinsk sandsynlighed kræver definition af hændelser og betingning, valg af en fordeling der passer til mekanismen, genkendelse af uafhængige enheder og skelnen mellem individuel variation og estimatorusikkerhed.",
        ),
        (
            ("El orden del condicionamiento importa.", "Conditioning order matters.", "Betingningsrækkefølgen betyder noget."),
            ("La binomial modela conteos bajo supuestos.", "The binomial models counts under assumptions.", "Binomialfordelingen modellerer antal under antagelser."),
            ("El error estándar pertenece a un estimador.", "Standard error belongs to an estimator.", "Standardfejl tilhører en estimator."),
            ("La simulación debe imitar el mecanismo.", "Simulation must imitate the mechanism.", "Simulation skal efterligne mekanismen."),
        ),
        (
            ("Invertir sensibilidad y valor predictivo.", "Reversing sensitivity and predictive value.", "At vende sensitivitet og prædiktiv værdi."),
            ("Contar réplicas como unidades independientes.", "Counting replicates as independent units.", "At tælle replikater som uafhængige enheder."),
            ("Confundir SD y SE.", "Confusing SD and SE.", "At forveksle SD og SE."),
        ),
        (
            ("¿Cuál es el espacio condicionado?", "What is the conditioned space?", "Hvad er det betingede rum?"),
            ("¿Qué mecanismo genera el dato?", "What mechanism generates the data?", "Hvilken mekanisme genererer data?"),
            ("¿Cuál es la unidad independiente?", "What is the independent unit?", "Hvad er den uafhængige enhed?"),
        ),
        (
            ("Define eventos y denominadores.", "Defines events and denominators.", "Definerer hændelser og nævnere."),
            ("Justifica la distribución.", "Justifies the distribution.", "Begrunder fordelingen."),
            ("Interpreta incertidumbre correctamente.", "Interprets uncertainty correctly.", "Fortolker usikkerhed korrekt."),
        ),
        (
            ("No inventar prevalencias ni independencia.", "Do not invent prevalence or independence.", "Opfind ikke prævalens eller uafhængighed."),
            ("No presentar aproximaciones como exactas.", "Do not present approximations as exact.", "Præsenter ikke approximationer som eksakte."),
            ("Responder en el idioma activo.", "Respond in the active language.", "Svar på det aktive sprog."),
        ),
        (
            "SDU ODIN BMB830 active course description approved 2025-03-06",
            "R base documentation: probability distributions",
            "Foundational probability and sampling theory",
        ),
    ),
)

LOCALIZED_MODULE_03_PROBABILITY = build_module(_SPEC)
LOCALIZED_OBJECTIVE_QUESTION_BANK_03 = build_question_bank(_SPEC)
MODULE_03_PROBABILITY: LearningModule = LOCALIZED_MODULE_03_PROBABILITY.materialize(
    AppLocale.SPANISH_SPAIN
)
OBJECTIVE_QUESTION_BANK_03: tuple[AssessmentItem, ...] = materialize_bank(
    LOCALIZED_OBJECTIVE_QUESTION_BANK_03
)


def materialize_module_03_question_bank(
    locale: AppLocale | str = AppLocale.SPANISH_SPAIN,
) -> tuple[AssessmentItem, ...]:
    """Return the module-3 objective bank in one locale."""

    return materialize_bank(LOCALIZED_OBJECTIVE_QUESTION_BANK_03, locale)


__all__ = [
    "LOCALIZED_MODULE_03_PROBABILITY",
    "LOCALIZED_OBJECTIVE_QUESTION_BANK_03",
    "MODULE_03_PROBABILITY",
    "OBJECTIVE_QUESTION_BANK_03",
    "materialize_module_03_question_bank",
]
