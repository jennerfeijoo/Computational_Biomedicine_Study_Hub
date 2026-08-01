"""BMB830 module 11: introductory multivariate analysis."""

from __future__ import annotations

from ...i18n import AppLocale
from ..models import AssessmentItem, LearningModule
from .standard import StandardModuleSpec, build_module, build_question_bank, materialize_bank

_SPEC = StandardModuleSpec(
    module_id="bmb830.m11",
    title=(
        "Análisis multivariante introductorio",
        "Introductory multivariate analysis",
        "Introduktion til multivariat analyse",
    ),
    summary=(
        "Organiza matrices biológicas, estandariza variables, aplica PCA y clustering jerárquico, y evalúa sensibilidad sin confundir patrones exploratorios con subtipos biológicos confirmados.",
        "Organise biological matrices, standardise variables, apply PCA and hierarchical clustering, and assess sensitivity without confusing exploratory patterns with confirmed biological subtypes.",
        "Organisér biologiske matricer, standardisér variable, anvend PCA og hierarkisk klyngedannelse, og vurder følsomhed uden at forveksle eksplorative mønstre med bekræftede biologiske undertyper.",
    ),
    objectives=(
        (
            "m11.o1",
            (
                "Distinguir muestras, variables, unidades independientes y metadatos antes de aplicar un método multivariante.",
                "Distinguish samples, variables, independent units, and metadata before applying a multivariate method.",
                "Skelne mellem prøver, variable, uafhængige enheder og metadata før anvendelse af en multivariat metode.",
            ),
        ),
        (
            "m11.o2",
            (
                "Justificar centrado, escalado, transformación y medida de distancia según la pregunta y las unidades.",
                "Justify centring, scaling, transformation, and distance according to the question and measurement units.",
                "Begrunde centrering, skalering, transformation og afstandsmål ud fra spørgsmålet og måleenhederne.",
            ),
        ),
        (
            "m11.o3",
            (
                "Ejecutar e interpretar PCA mediante varianza explicada, scores y loadings, reconociendo sus límites.",
                "Run and interpret PCA using explained variance, scores, and loadings while recognising its limits.",
                "Udføre og fortolke PCA med forklaret varians, scores og loadings og samtidig erkende metodens begrænsninger.",
            ),
        ),
        (
            "m11.o4",
            (
                "Aplicar clustering jerárquico y evaluar la sensibilidad de los grupos a distancia, linkage, variables y perturbaciones.",
                "Apply hierarchical clustering and assess cluster sensitivity to distance, linkage, variables, and perturbations.",
                "Anvende hierarkisk klyngedannelse og vurdere klyngernes følsomhed over for afstand, linkage, variable og perturbationer.",
            ),
        ),
    ),
    concepts=(
        (
            "matrix-orientation",
            (
                "Matriz multivariante y unidad de análisis",
                "Multivariate matrix and unit of analysis",
                "Multivariat matrix og analyseenhed",
            ),
            (
                "Una matriz multivariante suele organizar n muestras en filas y p variables en columnas. Antes del análisis deben verificarse identidad de muestras, unidades independientes, tipos de variable, valores ausentes, varianza cero y correspondencia con metadatos. Muchas variables no convierten mediciones repetidas del mismo paciente en muestras independientes.",
                "A multivariate matrix commonly places n samples in rows and p variables in columns. Before analysis, verify sample identity, independent units, variable types, missing values, zero variance, and metadata correspondence. Many variables do not turn repeated measurements from one patient into independent samples.",
                "En multivariat matrix placerer normalt n prøver i rækker og p variable i kolonner. Før analysen skal prøveidentitet, uafhængige enheder, variabletyper, manglende værdier, nulvarians og sammenhæng med metadata kontrolleres. Mange variable gør ikke gentagne målinger fra samme patient til uafhængige prøver.",
            ),
            (
                (
                    "La orientación equivocada intercambia preguntas sobre muestras y variables.",
                    "Incorrect orientation swaps questions about samples and variables.",
                    "Forkert orientering bytter spørgsmål om prøver og variable.",
                ),
                (
                    "Las columnas no numéricas deben mantenerse como metadatos o codificarse con una justificación explícita.",
                    "Non-numeric columns should remain metadata or be encoded with explicit justification.",
                    "Ikke-numeriske kolonner bør forblive metadata eller kodes med en eksplicit begrundelse.",
                ),
            ),
        ),
        (
            "preprocessing-distance",
            (
                "Preprocesamiento, escala y distancia",
                "Preprocessing, scale, and distance",
                "Forbehandling, skala og afstand",
            ),
            (
                "Centrar resta la media de cada variable; escalar por su desviación estándar evita que variables con unidades o dispersión grandes dominen automáticamente. Transformaciones como log pueden estabilizar distribuciones sesgadas, pero deben responder al proceso de medición. La distancia euclídea resume magnitud conjunta y depende de la escala; la distancia basada en correlación prioriza similitud de perfil.",
                "Centring subtracts each variable mean; scaling by its standard deviation prevents variables with large units or spread from automatically dominating. Transformations such as logs may stabilise skewed measurements but should reflect the measurement process. Euclidean distance summarises joint magnitude and depends on scale; correlation-based distance prioritises profile similarity.",
                "Centrering fratrækker hver variabels middelværdi; skalering med standardafvigelsen forhindrer variable med store enheder eller stor spredning i automatisk at dominere. Transformationer som log kan stabilisere skæve målinger, men bør afspejle måleprocessen. Euklidisk afstand opsummerer samlet størrelse og afhænger af skala; korrelationsbaseret afstand prioriterer profillig lighed.",
            ),
            (
                (
                    "Escalar no es una corrección universal: cambia la pregunta implícita sobre qué diferencias importan.",
                    "Scaling is not a universal correction: it changes the implicit question about which differences matter.",
                    "Skalering er ikke en universel korrektion: den ændrer det implicitte spørgsmål om, hvilke forskelle der betyder noget.",
                ),
                (
                    "El preprocesamiento utilizado en una tarea predictiva debe estimarse dentro de cada partición de entrenamiento.",
                    "Preprocessing used in prediction must be estimated within each training split.",
                    "Forbehandling i en prædiktiv opgave skal estimeres inden for hver træningsopdeling.",
                ),
            ),
        ),
        (
            "pca",
            (
                "PCA: scores, loadings y varianza explicada",
                "PCA: scores, loadings, and explained variance",
                "PCA: scores, loadings og forklaret varians",
            ),
            (
                "El análisis de componentes principales construye combinaciones lineales ortogonales que ordenan la variación de una matriz centrada y, con frecuencia, escalada. Los scores sitúan las muestras en el nuevo sistema; los loadings describen la contribución y dirección de las variables; la varianza explicada resume cuánta variación captura cada componente. El signo de un componente es arbitrario y puede invertirse sin cambiar la solución.",
                "Principal component analysis constructs orthogonal linear combinations that order variation in a centred and often scaled matrix. Scores place samples in the new coordinate system; loadings describe variable contribution and direction; explained variance summarises how much variation each component captures. Component signs are arbitrary and may flip without changing the solution.",
                "Principal komponentanalyse konstruerer ortogonale lineære kombinationer, der ordner variationen i en centreret og ofte skaleret matrix. Scores placerer prøverne i det nye koordinatsystem; loadings beskriver variablernes bidrag og retning; forklaret varians opsummerer, hvor meget variation hver komponent indfanger. Fortegnet på en komponent er vilkårligt og kan vendes uden at ændre løsningen.",
            ),
            (
                (
                    "PCA es no supervisado: una separación visual por grupos no prueba causalidad ni capacidad predictiva.",
                    "PCA is unsupervised: visual group separation does not prove causality or predictive ability.",
                    "PCA er ikke-superviseret: visuel gruppeadskillelse beviser ikke kausalitet eller prædiktionsevne.",
                ),
                (
                    "Una componente puede reflejar biología, lote, centro, calidad de muestra o una combinación.",
                    "A component may reflect biology, batch, centre, sample quality, or a combination.",
                    "En komponent kan afspejle biologi, batch, center, prøvekvalitet eller en kombination.",
                ),
            ),
        ),
        (
            "clustering-stability",
            (
                "Clustering jerárquico y estabilidad",
                "Hierarchical clustering and stability",
                "Hierarkisk klyngedannelse og stabilitet",
            ),
            (
                "El clustering jerárquico agrupa muestras según una matriz de distancias y una regla de linkage. El dendrograma representa el orden de fusiones, no una prueba de que exista un número verdadero de subtipos. La partición debe examinarse frente a cambios razonables en escalado, distancia, linkage, variables, muestras y perturbaciones; grupos frágiles deben describirse como exploratorios.",
                "Hierarchical clustering groups samples from a distance matrix and a linkage rule. The dendrogram represents the order of merges, not proof that a true number of subtypes exists. The partition should be examined under reasonable changes in scaling, distance, linkage, variables, samples, and perturbations; fragile groups should be described as exploratory.",
                "Hierarkisk klyngedannelse grupperer prøver ud fra en afstandsmatrix og en linkage-regel. Dendrogrammet viser rækkefølgen af sammenlægninger, ikke et bevis for et sandt antal undertyper. Opdelingen bør undersøges under rimelige ændringer i skalering, afstand, linkage, variable, prøver og perturbationer; skrøbelige grupper bør beskrives som eksplorative.",
            ),
            (
                (
                    "Cortar un dendrograma en k grupos es una decisión analítica que necesita justificación.",
                    "Cutting a dendrogram into k groups is an analytical decision requiring justification.",
                    "At skære et dendrogram i k grupper er en analytisk beslutning, der kræver begrundelse.",
                ),
                (
                    "La concordancia con una etiqueta clínica debe evaluarse después de documentar cómo se obtuvo la partición.",
                    "Agreement with a clinical label should be assessed after documenting how the partition was obtained.",
                    "Overensstemmelse med en klinisk etiket bør vurderes efter dokumentation af, hvordan opdelingen blev opnået.",
                ),
            ),
        ),
    ),
    examples=(
        (
            "m11.e01",
            (
                "PCA de perfiles coordinados",
                "PCA of coordinated profiles",
                "PCA af koordinerede profiler",
            ),
            (
                "Aplica PCA a cuatro muestras y tres marcadores perfectamente coordinados, usando valores absolutos para evitar depender del signo arbitrario del componente.",
                "Apply PCA to four samples and three perfectly coordinated markers, using absolute values so the result does not depend on the arbitrary component sign.",
                "Anvend PCA på fire prøver og tre perfekt koordinerede markører, og brug absolutte værdier, så resultatet ikke afhænger af komponentens vilkårlige fortegn.",
            ),
            (
                (
                    "Las filas son muestras y las columnas son marcadores.",
                    "Rows are samples and columns are markers.",
                    "Rækker er prøver, og kolonner er markører.",
                ),
                (
                    "Los tres marcadores contienen una sola dirección de variación.",
                    "The three markers contain one direction of variation.",
                    "De tre markører indeholder én variationsretning.",
                ),
            ),
            """x <- data.frame(
  marker_a = c(-1, -1, 1, 1),
  marker_b = c(-1, -1, 1, 1),
  marker_c = c(1, 1, -1, -1),
  row.names = paste0("sample_", 1:4)
)
fit <- prcomp(x, center = TRUE, scale. = TRUE)
variance <- 100 * fit$sdev^2 / sum(fit$sdev^2)
cat(sprintf("pc1_variance=%.1f\n", variance[[1]]))
cat("absolute_loadings=", paste(sprintf("%.3f", abs(fit$rotation[, 1])), collapse = ","), "\n", sep = "")
cat("absolute_scores=", paste(sprintf("%.3f", abs(fit$x[, 1])), collapse = ","), sep = "")
""",
            """pc1_variance=100.0
absolute_loadings=0.577,0.577,0.577
absolute_scores=1.500,1.500,1.500,1.500""",
            (
                "PC1 contiene toda la variación de este ejemplo construido. Las magnitudes iguales de los loadings reflejan contribución simétrica; el signo podría invertirse sin alterar distancias ni varianza explicada.",
                "PC1 contains all variation in this constructed example. Equal loading magnitudes reflect symmetric contribution; signs could flip without changing distances or explained variance.",
                "PC1 indeholder al variation i dette konstruerede eksempel. Ens loading-størrelser afspejler symmetrisk bidrag; fortegn kan vendes uden at ændre afstande eller forklaret varians.",
            ),
        ),
        (
            "m11.e02",
            (
                "Clustering y análisis de sensibilidad",
                "Clustering and sensitivity analysis",
                "Klyngedannelse og følsomhedsanalyse",
            ),
            (
                "Compara clustering jerárquico completo con distancias euclídea y Manhattan en cuatro perfiles claramente separados.",
                "Compare complete-linkage hierarchical clustering under Euclidean and Manhattan distances for four clearly separated profiles.",
                "Sammenlign hierarkisk complete-linkage-klyngedannelse med euklidisk og Manhattan-afstand for fire tydeligt adskilte profiler.",
            ),
            (
                (
                    "Las dos primeras muestras son similares entre sí y las dos últimas forman otro par.",
                    "The first two samples resemble each other and the last two form another pair.",
                    "De første to prøver ligner hinanden, og de sidste to danner et andet par.",
                ),
                (
                    "La estabilidad aquí se evalúa comparando dos decisiones razonables de distancia.",
                    "Stability here is assessed by comparing two reasonable distance choices.",
                    "Stabilitet vurderes her ved at sammenligne to rimelige valg af afstand.",
                ),
            ),
            """x <- rbind(
  A = c(0, 0, 0),
  B = c(0, 1, 0),
  C = c(10, 10, 10),
  D = c(10, 11, 10)
)
scaled <- scale(x)
euclidean <- cutree(hclust(dist(scaled), method = "complete"), k = 2)
manhattan <- cutree(hclust(dist(scaled, method = "manhattan"), method = "complete"), k = 2)
same_partition <- function(a, b) {
  identical(outer(a, a, "=="), outer(b, b, "=="))
}
format_clusters <- function(groups) {
  paste(paste(names(groups), groups, sep = "="), collapse = ",")
}
cat("clusters_euclidean=", format_clusters(euclidean), "\n", sep = "")
cat("clusters_manhattan=", format_clusters(manhattan), "\n", sep = "")
cat("same_partition=", same_partition(euclidean, manhattan), sep = "")
""",
            """clusters_euclidean=A=1,B=1,C=2,D=2
clusters_manhattan=A=1,B=1,C=2,D=2
same_partition=TRUE""",
            (
                "La partición es estable frente a estas dos distancias en el ejemplo. Eso no demuestra subtipos verdaderos; en datos reales deben evaluarse más decisiones, perturbaciones y metadatos.",
                "The partition is stable under these two distances in this example. This does not prove true subtypes; real data require more decisions, perturbations, and metadata checks.",
                "Opdelingen er stabil under disse to afstande i eksemplet. Det beviser ikke sande undertyper; virkelige data kræver flere beslutninger, perturbationer og metadata-kontroller.",
            ),
        ),
    ),
    practices=(
        (
            "m11.p01",
            "DATA_INTERPRETATION",
            (
                "Una matriz tiene 30 pacientes en filas, 2 visitas por paciente y 500 proteínas en columnas. ¿Cuál es la unidad independiente y qué error produciría tratar 60 visitas como pacientes independientes?",
                "A matrix has 30 patients, two visits per patient, and 500 proteins. What is the independent unit and what error follows from treating 60 visits as independent patients?",
                "En matrix har 30 patienter, to besøg pr. patient og 500 proteiner. Hvad er den uafhængige enhed, og hvilken fejl opstår ved at behandle 60 besøg som uafhængige patienter?",
            ),
            (
                (
                    "Distingue filas físicas de unidades estadísticas.",
                    "Distinguish physical rows from statistical units.",
                    "Skeln mellem fysiske rækker og statistiske enheder.",
                ),
            ),
            (
                "El paciente es la unidad independiente; las visitas están correlacionadas. Ignorarlo infla el tamaño muestral efectivo y puede crear patrones o precisión aparentes.",
                "The patient is the independent unit; visits are correlated. Ignoring this inflates effective sample size and may create apparent patterns or precision.",
                "Patienten er den uafhængige enhed; besøg er korrelerede. Hvis dette ignoreres, oppustes den effektive stikprøvestørrelse, og der kan opstå tilsyneladende mønstre eller præcision.",
            ),
            (
                "PCA descriptivo aún puede usar visitas, pero la dependencia debe conservarse en interpretación y validación.",
                "Descriptive PCA may still include visits, but dependence must be preserved in interpretation and validation.",
                "Deskriptiv PCA kan stadig inkludere besøg, men afhængighed skal bevares i fortolkning og validering.",
            ),
            "",
        ),
        (
            "m11.p02",
            "METHOD_SELECTION",
            (
                "Dos biomarcadores están en ng/mL y uno en miles de células/µL. Decide si escalar antes de PCA y explica la consecuencia.",
                "Two biomarkers are in ng/mL and one is in thousands of cells/µL. Decide whether to scale before PCA and explain the consequence.",
                "To biomarkører er i ng/mL og én i tusinder af celler/µL. Beslut om der skal skaleres før PCA, og forklar konsekvensen.",
            ),
            (
                (
                    "Compara la pregunta sobre variación absoluta con la pregunta sobre variación estandarizada.",
                    "Compare the question about absolute variation with the question about standardised variation.",
                    "Sammenlign spørgsmålet om absolut variation med spørgsmålet om standardiseret variation.",
                ),
            ),
            (
                "Escalar es normalmente defendible cuando las unidades no son comparables y se desea que cada variable contribuya según su variación relativa. Sin escalado, la variable con mayor dispersión numérica puede dominar.",
                "Scaling is usually defensible when units are incomparable and each variable should contribute by relative variation. Without scaling, the numerically most dispersed variable may dominate.",
                "Skalering er normalt forsvarlig, når enheder ikke er sammenlignelige, og hver variabel skal bidrage efter relativ variation. Uden skalering kan variablen med størst numerisk spredning dominere.",
            ),
            (
                "La decisión debe registrarse y someterse a sensibilidad.",
                "The decision should be recorded and subjected to sensitivity analysis.",
                "Beslutningen bør registreres og indgå i en følsomhedsanalyse.",
            ),
            "",
        ),
        (
            "m11.p03",
            "DATA_INTERPRETATION",
            (
                "PC1 explica 48% y PC2 21%. Dos grupos se separan visualmente en PC1-PC2. Formula una conclusión válida y una inválida.",
                "PC1 explains 48% and PC2 21%. Two groups visually separate in PC1-PC2. State one valid and one invalid conclusion.",
                "PC1 forklarer 48 %, og PC2 21 %. To grupper adskilles visuelt i PC1-PC2. Formulér én gyldig og én ugyldig konklusion.",
            ),
            (
                (
                    "PCA resume variación y no usa necesariamente las etiquetas.",
                    "PCA summarises variation and does not necessarily use labels.",
                    "PCA opsummerer variation og bruger ikke nødvendigvis etiketter.",
                ),
            ),
            (
                "Válida: en los datos analizados, las dos primeras componentes capturan 69% de la variación y muestran una separación descriptiva que debe contrastarse con lote y otros metadatos. Inválida: PCA demuestra dos enfermedades causalmente distintas.",
                "Valid: in these data, the first two components capture 69% of variation and show descriptive separation that should be checked against batch and other metadata. Invalid: PCA proves two causally distinct diseases.",
                "Gyldig: i disse data indfanger de første to komponenter 69 % af variationen og viser en deskriptiv adskillelse, som bør kontrolleres mod batch og andre metadata. Ugyldig: PCA beviser to kausalt forskellige sygdomme.",
            ),
            (
                "La separación puede cambiar con preprocesamiento, selección de muestras y variables.",
                "Separation may change with preprocessing and sample or variable selection.",
                "Adskillelsen kan ændres med forbehandling og valg af prøver eller variable.",
            ),
            "",
        ),
        (
            "m11.p04",
            "ORAL_EXPLANATION",
            (
                "Explica por qué los loadings de PC1 pueden aparecer con signos opuestos en dos programas y seguir representando la misma solución.",
                "Explain why PC1 loadings may have opposite signs in two programs yet represent the same solution.",
                "Forklar hvorfor PC1-loadings kan have modsatte fortegn i to programmer og stadig repræsentere samme løsning.",
            ),
            (
                (
                    "Una dirección geométrica puede describirse con un vector o su negativo.",
                    "A geometric direction can be represented by a vector or its negative.",
                    "En geometrisk retning kan repræsenteres af en vektor eller dens negative.",
                ),
            ),
            (
                "Multiplicar simultáneamente loadings y scores por −1 conserva reconstrucción, distancias, varianza explicada y relaciones entre muestras. Deben interpretarse contribuciones relativas, no el signo aislado entre ejecuciones.",
                "Multiplying both loadings and scores by −1 preserves reconstruction, distances, explained variance, and sample relationships. Interpret relative contributions rather than isolated signs across runs.",
                "Når både loadings og scores multipliceres med −1, bevares rekonstruktion, afstande, forklaret varians og relationer mellem prøver. Fortolk relative bidrag frem for isolerede fortegn på tværs af kørsler.",
            ),
            (
                "El signo dentro de una misma solución sí permite comparar direcciones relativas entre variables.",
                "Within one solution, signs still describe relative directions among variables.",
                "Inden for én løsning beskriver fortegn stadig relative retninger mellem variable.",
            ),
            "",
        ),
        (
            "m11.p05",
            "METHOD_SELECTION",
            (
                "Un dendrograma cambia de tres grupos a dos al sustituir distancia euclídea por correlación. ¿Cómo debes reportarlo?",
                "A dendrogram changes from three groups to two when Euclidean distance is replaced by correlation distance. How should this be reported?",
                "Et dendrogram ændres fra tre grupper til to, når euklidisk afstand erstattes af korrelationsafstand. Hvordan bør det rapporteres?",
            ),
            (
                (
                    "La distancia define qué significa similitud.",
                    "Distance defines what similarity means.",
                    "Afstanden definerer, hvad lighed betyder.",
                ),
            ),
            (
                "La estructura es sensible a una decisión analítica fundamental. Deben mostrarse ambas definiciones, justificar cuál responde a la pregunta y evitar presentar los grupos como subtipos robustos hasta evaluar más estabilidad y validación.",
                "The structure is sensitive to a fundamental analytical choice. Show both definitions, justify which matches the question, and avoid presenting clusters as robust subtypes until further stability and validation are assessed.",
                "Strukturen er følsom over for et grundlæggende analytisk valg. Vis begge definitioner, begrund hvilken der passer til spørgsmålet, og undgå at præsentere klyngerne som robuste undertyper før yderligere stabilitet og validering er vurderet.",
            ),
            (
                "No debe elegirse la distancia solo porque produce la figura más clara.",
                "Distance should not be chosen merely because it produces the clearest figure.",
                "Afstand bør ikke vælges alene, fordi den giver den tydeligste figur.",
            ),
            "",
        ),
        (
            "m11.p06",
            "DATA_INTERPRETATION",
            (
                "En pipeline predictivo calcula media, desviación y PCA con todos los pacientes antes de validación cruzada. Identifica el problema y corrige el orden.",
                "A predictive pipeline computes means, standard deviations, and PCA on all patients before cross-validation. Identify the problem and correct the order.",
                "En prædiktiv pipeline beregner middelværdier, standardafvigelser og PCA på alle patienter før krydsvalidering. Identificér problemet og ret rækkefølgen.",
            ),
            (
                (
                    "Los componentes aprendieron información de los pacientes de validación.",
                    "The components learned information from validation patients.",
                    "Komponenterne lærte information fra valideringspatienterne.",
                ),
            ),
            (
                "Existe fuga de información. En cada fold: separar pacientes, estimar transformación, centrado, escalado y PCA solo en entrenamiento; proyectar validación con esos parámetros; ajustar y evaluar el modelo sin reutilizar la validación.",
                "There is information leakage. Within each fold: split patients, estimate transformation, centring, scaling, and PCA on training only; project validation using those parameters; fit and evaluate without reusing validation.",
                "Der er informationslækage. I hvert fold: opdel patienter, estimér transformation, centrering, skalering og PCA kun på træning; projicér validering med disse parametre; tilpas og evaluér uden at genbruge valideringen.",
            ),
            (
                "En PCA puramente descriptiva del conjunto completo es otra tarea y debe etiquetarse como exploratoria.",
                "A purely descriptive PCA of the full data is a different task and should be labelled exploratory.",
                "En rent deskriptiv PCA af hele datasættet er en anden opgave og bør betegnes som eksplorativ.",
            ),
            "",
        ),
    ),
    mcqs=(
        (
            "001",
            (
                "¿Qué orientación es habitual para PCA de muestras biológicas?",
                "Which orientation is usual for PCA of biological samples?",
                "Hvilken orientering er almindelig for PCA af biologiske prøver?",
            ),
            (
                ("a", ("Muestras en filas y variables en columnas", "Samples in rows and variables in columns", "Prøver i rækker og variable i kolonner")),
                ("b", ("Variables en filas y ninguna columna", "Variables in rows and no columns", "Variable i rækker og ingen kolonner")),
                ("c", ("Solo metadatos numéricos", "Numeric metadata only", "Kun numeriske metadata")),
                ("d", ("Una fila por proteína sin muestras", "One row per protein without samples", "Én række pr. protein uden prøver")),
            ),
            "a",
            (
                "Esta orientación permite interpretar scores por muestra y loadings por variable.",
                "This orientation supports sample scores and variable loadings.",
                "Denne orientering understøtter scores for prøver og loadings for variable.",
            ),
        ),
        (
            "002",
            (
                "¿Cuándo es especialmente importante considerar escalado?",
                "When is scaling especially important?",
                "Hvornår er skalering særligt vigtig?",
            ),
            (
                ("a", ("Cuando las variables tienen unidades o dispersiones muy distintas", "When variables have very different units or spreads", "Når variable har meget forskellige enheder eller spredninger")),
                ("b", ("Solo cuando n=1", "Only when n=1", "Kun når n=1")),
                ("c", ("Para demostrar causalidad", "To prove causality", "For at bevise kausalitet")),
                ("d", ("Para eliminar toda variabilidad", "To remove all variability", "For at fjerne al variation")),
            ),
            "a",
            (
                "Sin escalado, la magnitud numérica puede dominar la geometría.",
                "Without scaling, numerical magnitude may dominate the geometry.",
                "Uden skalering kan numerisk størrelse dominere geometrien.",
            ),
        ),
        (
            "003",
            (
                "¿Qué representan los scores de PCA?",
                "What do PCA scores represent?",
                "Hvad repræsenterer PCA-scores?",
            ),
            (
                ("a", ("Coordenadas de las muestras en los componentes", "Sample coordinates on the components", "Prøvernes koordinater på komponenterne")),
                ("b", ("Valores p de cada variable", "P-values for each variable", "P-værdier for hver variabel")),
                ("c", ("Errores de medición confirmados", "Confirmed measurement errors", "Bekræftede målefejl")),
                ("d", ("Etiquetas clínicas predichas", "Predicted clinical labels", "Forudsagte kliniske etiketter")),
            ),
            "a",
            (
                "Los loadings corresponden a las variables; los scores, a las muestras.",
                "Loadings correspond to variables; scores correspond to samples.",
                "Loadings svarer til variable; scores svarer til prøver.",
            ),
        ),
        (
            "004",
            (
                "¿Qué representan los loadings?",
                "What do loadings represent?",
                "Hvad repræsenterer loadings?",
            ),
            (
                ("a", ("Contribución y dirección de las variables", "Variable contribution and direction", "Variablernes bidrag og retning")),
                ("b", ("Número de pacientes", "Number of patients", "Antal patienter")),
                ("c", ("Probabilidad de causalidad", "Probability of causality", "Sandsynlighed for kausalitet")),
                ("d", ("Altura del dendrograma únicamente", "Dendrogram height only", "Kun dendrogramhøjde")),
            ),
            "a",
            (
                "Los loadings definen las combinaciones lineales de las variables.",
                "Loadings define the linear combinations of variables.",
                "Loadings definerer lineære kombinationer af variable.",
            ),
        ),
        (
            "005",
            (
                "¿Qué implica que PC1 explique 40%?",
                "What does it mean that PC1 explains 40%?",
                "Hvad betyder det, at PC1 forklarer 40 %?",
            ),
            (
                ("a", ("Captura 40% de la variación total bajo el preprocesamiento usado", "It captures 40% of total variation under the chosen preprocessing", "Den indfanger 40 % af den samlede variation under den valgte forbehandling")),
                ("b", ("Predice correctamente 40% de pacientes", "It correctly predicts 40% of patients", "Den forudsiger 40 % af patienterne korrekt")),
                ("c", ("Demuestra 40% de causalidad", "It proves 40% causality", "Den beviser 40 % kausalitet")),
                ("d", ("Elimina 40% de errores", "It removes 40% of errors", "Den fjerner 40 % af fejlene")),
            ),
            "a",
            (
                "La varianza explicada es geométrica y depende de la matriz analizada.",
                "Explained variance is geometric and depends on the analysed matrix.",
                "Forklaret varians er geometrisk og afhænger af den analyserede matrix.",
            ),
        ),
        (
            "006",
            (
                "¿Qué determina un clustering jerárquico?",
                "What determines hierarchical clustering?",
                "Hvad bestemmer hierarkisk klyngedannelse?",
            ),
            (
                ("a", ("Preprocesamiento, distancia y linkage", "Preprocessing, distance, and linkage", "Forbehandling, afstand og linkage")),
                ("b", ("Solo el nombre de las muestras", "Sample names only", "Kun prøvernes navne")),
                ("c", ("Un valor p único", "A single p-value", "En enkelt p-værdi")),
                ("d", ("La causalidad conocida", "Known causality", "Kendt kausalitet")),
            ),
            "a",
            (
                "Cada decisión define la geometría o la regla de fusión.",
                "Each decision defines the geometry or merge rule.",
                "Hver beslutning definerer geometrien eller sammenlægningsreglen.",
            ),
        ),
        (
            "007",
            (
                "¿Qué demuestra cortar un dendrograma en tres grupos?",
                "What does cutting a dendrogram into three groups prove?",
                "Hvad beviser det at skære et dendrogram i tre grupper?",
            ),
            (
                ("a", ("Solo produce una partición bajo esa decisión", "It only produces a partition under that decision", "Det producerer kun en opdeling under denne beslutning")),
                ("b", ("Demuestra tres subtipos verdaderos", "It proves three true subtypes", "Det beviser tre sande undertyper")),
                ("c", ("Garantiza validación externa", "It guarantees external validation", "Det garanterer ekstern validering")),
                ("d", ("Elimina efectos de lote", "It removes batch effects", "Det fjerner batcheffekter")),
            ),
            "a",
            (
                "La robustez requiere sensibilidad y validación adicional.",
                "Robustness requires further sensitivity and validation.",
                "Robusthed kræver yderligere følsomhed og validering.",
            ),
        ),
        (
            "008",
            (
                "¿Qué orden evita fuga al usar PCA en predicción?",
                "Which order avoids leakage when PCA is used for prediction?",
                "Hvilken rækkefølge undgår lækage, når PCA bruges til prædiktion?",
            ),
            (
                ("a", ("Ajustar preprocesamiento y PCA en entrenamiento y proyectar validación", "Fit preprocessing and PCA on training and project validation", "Tilpas forbehandling og PCA på træning og projicér validering")),
                ("b", ("Ajustar PCA con todos los pacientes antes de dividir", "Fit PCA on all patients before splitting", "Tilpas PCA på alle patienter før opdeling")),
                ("c", ("Elegir componentes según el conjunto de prueba", "Choose components using the test set", "Vælg komponenter med testsættet")),
                ("d", ("Repetir hasta obtener separación visual", "Repeat until visual separation appears", "Gentag indtil visuel adskillelse opstår")),
            ),
            "a",
            (
                "La validación no debe influir en ningún parámetro aprendido.",
                "Validation must not influence any learned parameter.",
                "Validering må ikke påvirke nogen lærte parametre.",
            ),
        ),
    ),
    true_false=(
        (
            "009",
            (
                "Más variables implican automáticamente más muestras independientes.",
                "More variables automatically imply more independent samples.",
                "Flere variable indebærer automatisk flere uafhængige prøver.",
            ),
            False,
            (
                "La independencia pertenece a las unidades observacionales y al diseño.",
                "Independence belongs to observational units and design.",
                "Uafhængighed vedrører observationsenheder og design.",
            ),
        ),
        (
            "010",
            (
                "Escalar puede cambiar la estructura observada por PCA y clustering.",
                "Scaling can change the structure seen by PCA and clustering.",
                "Skalering kan ændre den struktur, der ses af PCA og klyngedannelse.",
            ),
            True,
            (
                "Cambia el peso relativo de las variables.",
                "It changes the relative weight of variables.",
                "Det ændrer variablernes relative vægt.",
            ),
        ),
        (
            "011",
            (
                "El signo de una componente principal es único y científicamente fijo.",
                "The sign of a principal component is unique and scientifically fixed.",
                "Fortegnet på en principal komponent er entydigt og videnskabeligt fast.",
            ),
            False,
            (
                "El vector y su negativo describen la misma dirección.",
                "A vector and its negative describe the same direction.",
                "En vektor og dens negative beskriver samme retning.",
            ),
        ),
        (
            "012",
            (
                "Una separación en PCA puede reflejar un efecto de lote.",
                "PCA separation may reflect a batch effect.",
                "Adskillelse i PCA kan afspejle en batcheffekt.",
            ),
            True,
            (
                "Las componentes ordenan variación sin conocer su causa.",
                "Components order variation without knowing its cause.",
                "Komponenter ordner variation uden at kende dens årsag.",
            ),
        ),
        (
            "013",
            (
                "PCA demuestra capacidad predictiva cuando dos colores se separan visualmente.",
                "PCA proves predictive ability when two colours visually separate.",
                "PCA beviser prædiktionsevne, når to farver adskilles visuelt.",
            ),
            False,
            (
                "La predicción requiere una evaluación supervisada fuera de muestra.",
                "Prediction requires supervised out-of-sample evaluation.",
                "Prædiktion kræver superviseret evaluering uden for stikprøven.",
            ),
        ),
        (
            "014",
            (
                "La distancia euclídea depende de la escala de las variables.",
                "Euclidean distance depends on variable scale.",
                "Euklidisk afstand afhænger af variablernes skala.",
            ),
            True,
            (
                "Variables con gran dispersión pueden dominarla.",
                "Variables with large spread may dominate it.",
                "Variable med stor spredning kan dominere den.",
            ),
        ),
        (
            "015",
            (
                "Un dendrograma prueba por sí solo el número verdadero de subtipos.",
                "A dendrogram alone proves the true number of subtypes.",
                "Et dendrogram alene beviser det sande antal undertyper.",
            ),
            False,
            (
                "El corte y la estabilidad requieren decisiones y evidencia adicionales.",
                "Cutting and stability require additional decisions and evidence.",
                "Skæring og stabilitet kræver yderligere beslutninger og evidens.",
            ),
        ),
        (
            "016",
            (
                "La estabilidad debe evaluarse frente a decisiones analíticas razonables.",
                "Stability should be assessed under reasonable analytical choices.",
                "Stabilitet bør vurderes under rimelige analytiske valg.",
            ),
            True,
            (
                "Resultados frágiles deben comunicarse como exploratorios.",
                "Fragile results should be communicated as exploratory.",
                "Skrøbelige resultater bør kommunikeres som eksplorative.",
            ),
        ),
    ),
    tutor=(
        (
            "El análisis multivariante introductorio comienza por la matriz y la unidad independiente; después justifica preprocesamiento, PCA o clustering y termina con sensibilidad e interpretación biológica prudente.",
            "Introductory multivariate analysis begins with the matrix and independent unit, then justifies preprocessing, PCA or clustering, and ends with sensitivity and cautious biological interpretation.",
            "Introducerende multivariat analyse begynder med matricen og den uafhængige enhed, begrunder derefter forbehandling, PCA eller klyngedannelse og afslutter med følsomhed og forsigtig biologisk fortolkning.",
        ),
        (
            (
                "Las filas representan muestras y las columnas variables; los metadatos describen las muestras sin convertirse automáticamente en características numéricas.",
                "Rows represent samples and columns variables; metadata describe samples without automatically becoming numeric features.",
                "Rækker repræsenterer prøver og kolonner variable; metadata beskriver prøver uden automatisk at blive numeriske features.",
            ),
            (
                "Centrado, escalado, transformación y distancia cambian la geometría del análisis.",
                "Centring, scaling, transformation, and distance change analysis geometry.",
                "Centrering, skalering, transformation og afstand ændrer analysens geometri.",
            ),
            (
                "PCA separa scores de muestras, loadings de variables y varianza explicada por componente.",
                "PCA separates sample scores, variable loadings, and variance explained by component.",
                "PCA adskiller prøvescores, variable-loadings og forklaret varians pr. komponent.",
            ),
            (
                "Clustering depende de distancia y linkage; los grupos necesitan análisis de estabilidad.",
                "Clustering depends on distance and linkage; groups require stability analysis.",
                "Klyngedannelse afhænger af afstand og linkage; grupper kræver stabilitetsanalyse.",
            ),
        ),
        (
            (
                "PCA supervisa las etiquetas de grupo.",
                "PCA is supervised by group labels.",
                "PCA superviseres af gruppeetiketter.",
            ),
            (
                "Escalar siempre mejora cualquier análisis.",
                "Scaling always improves every analysis.",
                "Skalering forbedrer altid enhver analyse.",
            ),
            (
                "Un dendrograma descubre automáticamente subtipos verdaderos.",
                "A dendrogram automatically discovers true subtypes.",
                "Et dendrogram opdager automatisk sande undertyper.",
            ),
            (
                "El signo de los loadings es fijo entre programas.",
                "Loading signs are fixed across programs.",
                "Fortegn på loadings er faste på tværs af programmer.",
            ),
        ),
        (
            (
                "¿Cuáles son las muestras, variables y unidades independientes?",
                "What are the samples, variables, and independent units?",
                "Hvad er prøverne, variablerne og de uafhængige enheder?",
            ),
            (
                "¿Qué cambia al centrar, escalar o transformar?",
                "What changes when centring, scaling, or transforming?",
                "Hvad ændres ved centrering, skalering eller transformation?",
            ),
            (
                "¿Qué muestran scores, loadings y varianza explicada?",
                "What do scores, loadings, and explained variance show?",
                "Hvad viser scores, loadings og forklaret varians?",
            ),
            (
                "¿La partición es estable frente a decisiones razonables?",
                "Is the partition stable under reasonable choices?",
                "Er opdelingen stabil under rimelige valg?",
            ),
        ),
        (
            (
                "Define correctamente matriz, unidad independiente y metadatos.",
                "Correctly defines matrix, independent unit, and metadata.",
                "Definerer matrix, uafhængig enhed og metadata korrekt.",
            ),
            (
                "Justifica el preprocesamiento y la distancia según la pregunta.",
                "Justifies preprocessing and distance according to the question.",
                "Begrunder forbehandling og afstand ud fra spørgsmålet.",
            ),
            (
                "Interpreta PCA sin atribuir causalidad o predicción no evaluada.",
                "Interprets PCA without attributing causality or unevaluated prediction.",
                "Fortolker PCA uden at tillægge kausalitet eller ikke-evalueret prædiktion.",
            ),
            (
                "Evalúa sensibilidad y comunica incertidumbre exploratoria.",
                "Assesses sensitivity and communicates exploratory uncertainty.",
                "Vurderer følsomhed og kommunikerer eksplorativ usikkerhed.",
            ),
        ),
        (
            (
                "No presentar clusters como diagnósticos clínicos ni subtipos confirmados.",
                "Do not present clusters as clinical diagnoses or confirmed subtypes.",
                "Præsentér ikke klynger som kliniske diagnoser eller bekræftede undertyper.",
            ),
            (
                "No usar etiquetas de validación para ajustar preprocesamiento o PCA.",
                "Do not use validation data to fit preprocessing or PCA.",
                "Brug ikke valideringsdata til at tilpasse forbehandling eller PCA.",
            ),
            (
                "No convertir discusión recomendada en proyecto o evaluación grupal.",
                "Do not convert recommended discussion into a group project or group assessment.",
                "Konvertér ikke anbefalet diskussion til et gruppeprojekt eller en gruppebedømmelse.",
            ),
        ),
        (
            "bmb830.m11.concepts",
            "bmb830.m11.examples",
            "bmb830.m11.practice",
            "bmb830.m11.assessment",
        ),
    ),
)

LOCALIZED_MODULE_11_INTRO_MULTIVARIATE = build_module(_SPEC)
LOCALIZED_OBJECTIVE_QUESTION_BANK_11 = build_question_bank(_SPEC)


def materialize_module_11_question_bank(
    locale: AppLocale | str = AppLocale.SPANISH_SPAIN,
) -> tuple[AssessmentItem, ...]:
    """Materialize the stable objective bank for module 11."""

    return materialize_bank(LOCALIZED_OBJECTIVE_QUESTION_BANK_11, locale)


MODULE_11_INTRO_MULTIVARIATE: LearningModule = LOCALIZED_MODULE_11_INTRO_MULTIVARIATE.materialize(
    AppLocale.SPANISH_SPAIN
)
OBJECTIVE_QUESTION_BANK_11 = materialize_module_11_question_bank()

__all__ = [
    "LOCALIZED_MODULE_11_INTRO_MULTIVARIATE",
    "LOCALIZED_OBJECTIVE_QUESTION_BANK_11",
    "MODULE_11_INTRO_MULTIVARIATE",
    "OBJECTIVE_QUESTION_BANK_11",
    "materialize_module_11_question_bank",
]
