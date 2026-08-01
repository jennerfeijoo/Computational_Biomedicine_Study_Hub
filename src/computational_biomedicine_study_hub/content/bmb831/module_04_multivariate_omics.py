"""BMB831 module 4: multivariate omics analysis and stability."""

from __future__ import annotations

from ...i18n import AppLocale
from ..models import AssessmentItem, LearningModule
from .authoring import Triple
from .standard import (
    McqSpec,
    OptionSpec,
    StandardModuleSpec,
    TfSpec,
    build_module,
    build_question_bank,
    materialize_bank,
)


def _t(spanish: str, english: str, danish: str) -> Triple:
    return spanish, english, danish


def _option(option_id: str, text: Triple) -> OptionSpec:
    return option_id, text


def _mcq(
    item_id: str,
    prompt: Triple,
    options: tuple[OptionSpec, ...],
    correct_option_id: str,
    explanation: Triple,
) -> McqSpec:
    return item_id, prompt, options, correct_option_id, explanation


def _tf(item_id: str, prompt: Triple, correct: bool, explanation: Triple) -> TfSpec:
    return item_id, prompt, correct, explanation


_SPEC = StandardModuleSpec(
    module_id="bmb831.m04",
    title=_t(
        "Análisis multivariante ómico, estabilidad y validación",
        "Multivariate omics analysis, stability, and validation",
        "Multivariat omikanalyse, stabilitet og validering",
    ),
    summary=_t(
        "Analiza estructura conjunta en matrices de alta dimensionalidad mediante PCA, distancias y clustering; distingue exploración de predicción; evalúa estabilidad frente a preprocesamiento y perturbaciones; y evita fuga al usar información supervisada.",
        "Analyze joint structure in high-dimensional matrices through PCA, distances, and clustering; distinguish exploration from prediction; assess stability across preprocessing and perturbations; and prevent leakage when supervised information is used.",
        "Analysér fælles struktur i højdimensionelle matricer med PCA, afstande og clustering; skeln mellem udforskning og prædiktion; vurder stabilitet på tværs af præprocessering og perturbationer; og undgå leakage ved brug af superviseret information.",
    ),
    objectives=(
        (
            "m04.o1",
            _t(
                "Elegir orientación, transformación, centrado, escalado y distancia de acuerdo con la pregunta y la escala de medida.",
                "Choose orientation, transformation, centering, scaling, and distance according to the question and measurement scale.",
                "Vælge orientering, transformation, centrering, skalering og afstand efter spørgsmål og måleskala.",
            ),
        ),
        (
            "m04.o2",
            _t(
                "Interpretar scores, loadings, varianza explicada, distancias y dendrogramas sin convertir patrones exploratorios en subtipos confirmados.",
                "Interpret scores, loadings, explained variance, distances, and dendrograms without turning exploratory patterns into confirmed subtypes.",
                "Fortolke scores, loadings, forklaret varians, afstande og dendrogrammer uden at gøre eksplorative mønstre til bekræftede subtyper.",
            ),
        ),
        (
            "m04.o3",
            _t(
                "Evaluar estabilidad frente a muestras, características, parámetros, lotes y perturbaciones razonables.",
                "Assess stability across samples, features, parameters, batches, and reasonable perturbations.",
                "Vurdere stabilitet på tværs af prøver, features, parametre, batches og rimelige perturbationer.",
            ),
        ),
        (
            "m04.o4",
            _t(
                "Separar análisis exploratorio no supervisado de selección o reducción supervisada y aplicar validación sólo con entrenamiento.",
                "Separate unsupervised exploration from supervised selection or reduction and perform fitting only within training data.",
                "Adskille usuperviseret udforskning fra superviseret selektion eller reduktion og kun fitte inden for træningsdata.",
            ),
        ),
    ),
    concepts=(
        (
            "geometry-contract",
            _t(
                "Geometría inducida por el preprocesamiento",
                "Geometry induced by preprocessing",
                "Geometri induceret af præprocessering",
            ),
            _t(
                "La orientación correcta coloca muestras como observaciones y características como variables. Centrar elimina niveles medios, escalar iguala varianzas y una transformación puede reducir asimetría o dependencia media-varianza. Estas decisiones cambian la geometría: dos muestras pueden parecer próximas o lejanas según la escala y la distancia. Euclídea enfatiza magnitud; una distancia basada en correlación enfatiza forma de perfil. Ninguna elección es neutral.",
                "The correct orientation places samples as observations and features as variables. Centering removes mean levels, scaling equalizes variances, and transformation may reduce skew or mean-variance dependence. These decisions change geometry: two samples may appear close or distant depending on scale and distance. Euclidean distance emphasizes magnitude; correlation-based distance emphasizes profile shape. No choice is neutral.",
                "Den korrekte orientering placerer prøver som observationer og features som variable. Centrering fjerner middelniveauer, skalering udligner varianser, og transformation kan reducere skævhed eller middelværdi-varians-afhængighed. Valgene ændrer geometrien: to prøver kan fremstå nære eller fjerne afhængigt af skala og afstand. Euklidisk afstand fremhæver størrelse; korrelationsbaseret afstand fremhæver profilform. Intet valg er neutralt.",
            ),
            (
                _t(
                    "Declara qué aspecto biológico debe representar la proximidad.",
                    "Declare which biological aspect proximity should represent.",
                    "Deklarér hvilket biologisk aspekt nærhed skal repræsentere.",
                ),
                _t(
                    "Realiza análisis de sensibilidad a transformaciones y escalado.",
                    "Perform sensitivity analysis across transformations and scaling.",
                    "Udfør følsomhedsanalyse på tværs af transformationer og skalering.",
                ),
            ),
        ),
        (
            "pca-interpretation",
            _t(
                "PCA: scores, loadings y varianza",
                "PCA: scores, loadings, and variance",
                "PCA: scores, loadings og varians",
            ),
            _t(
                "PCA construye combinaciones lineales ortogonales que maximizan varianza sucesiva. Los scores ubican muestras; los loadings describen la contribución de características; la varianza explicada cuantifica variación capturada, no importancia biológica. El signo de una componente es arbitrario y puede invertirse sin cambiar la solución. Separación por grupo puede reflejar señal biológica, lote, composición celular, calidad o confusión.",
                "PCA constructs orthogonal linear combinations that maximize successive variance. Scores locate samples; loadings describe feature contributions; explained variance quantifies captured variation, not biological importance. Component sign is arbitrary and may reverse without changing the solution. Group separation may reflect biological signal, batch, cell composition, quality, or confounding.",
                "PCA konstruerer ortogonale lineære kombinationer, der maksimerer successiv varians. Scores placerer prøver; loadings beskriver featurebidrag; forklaret varians kvantificerer indfanget variation, ikke biologisk betydning. Komponentens fortegn er vilkårligt og kan vendes uden at ændre løsningen. Gruppeadskillelse kan afspejle biologisk signal, batch, cellesammensætning, kvalitet eller confounding.",
            ),
            (
                _t(
                    "Interpreta scores y loadings conjuntamente.",
                    "Interpret scores and loadings jointly.",
                    "Fortolk scores og loadings samlet.",
                ),
                _t(
                    "Superpone metadata sin usarla para construir un PCA no supervisado.",
                    "Overlay metadata without using it to construct an unsupervised PCA.",
                    "Overlej metadata uden at bruge dem til at konstruere en usuperviseret PCA.",
                ),
            ),
        ),
        (
            "clustering-stability",
            _t("Clustering y estabilidad", "Clustering and stability", "Clustering og stabilitet"),
            _t(
                "El clustering jerárquico depende de distancia, linkage, variables y preprocesamiento. Un dendrograma representa una secuencia de fusiones, no una prueba de que exista un número verdadero de grupos. La estabilidad se evalúa repitiendo el análisis bajo remuestreo, eliminación de características, cambios razonables de parámetros y corrección o estratificación por lote. Un patrón frágil debe describirse como exploratorio.",
                "Hierarchical clustering depends on distance, linkage, variables, and preprocessing. A dendrogram represents a sequence of merges, not proof that a true number of groups exists. Stability is assessed by repeating analysis under resampling, feature removal, reasonable parameter changes, and batch adjustment or stratification. A fragile pattern should be described as exploratory.",
                "Hierarkisk clustering afhænger af afstand, linkage, variable og præprocessering. Et dendrogram repræsenterer en sekvens af fusioner, ikke bevis for at et sandt antal grupper findes. Stabilitet vurderes ved at gentage analysen under resampling, featurefjernelse, rimelige parameterændringer og batchjustering eller stratificering. Et skrøbeligt mønster bør beskrives som eksplorativt.",
            ),
            (
                _t(
                    "Compara particiones, no etiquetas numéricas arbitrarias.",
                    "Compare partitions, not arbitrary numeric labels.",
                    "Sammenlign partitioner, ikke vilkårlige numeriske labels.",
                ),
                _t(
                    "Reporta parámetros y resultados alternativos relevantes.",
                    "Report relevant parameters and alternative results.",
                    "Rapportér relevante parametre og alternative resultater.",
                ),
            ),
        ),
        (
            "supervised-leakage",
            _t(
                "Reducción supervisada y fuga",
                "Supervised reduction and leakage",
                "Superviseret reduktion og leakage",
            ),
            _t(
                "Seleccionar características por asociación con el outcome, ajustar una proyección supervisada o elegir el número de componentes utiliza etiquetas. Todas esas decisiones deben ocurrir dentro de cada partición de entrenamiento. Aplicarlas antes de la validación permite que la información de test influya en el espacio de representación y produce rendimiento optimista. Un gráfico exploratorio con etiquetas no es una estimación validada de capacidad predictiva.",
                "Selecting features by outcome association, fitting a supervised projection, or choosing component count uses labels. All such decisions must occur within each training partition. Applying them before validation allows test information to influence the representation and produces optimistic performance. An exploratory labeled plot is not a validated estimate of predictive ability.",
                "Valg af features efter outcome-association, fit af en superviseret projektion eller valg af komponentantal bruger labels. Alle sådanne beslutninger skal ske inden for hver træningspartition. Anvendelse før validering lader testinformation påvirke repræsentationen og giver optimistisk performance. Et eksplorativt plot med labels er ikke et valideret estimat af prædiktionsevne.",
            ),
            (
                _t(
                    "Encapsula selección, transformación y modelo dentro del resampling.",
                    "Nest selection, transformation, and model fitting within resampling.",
                    "Indlejr selektion, transformation og modeltilpasning i resampling.",
                ),
                _t(
                    "Separa descubrimiento, descripción y predicción.",
                    "Separate discovery, description, and prediction.",
                    "Adskil discovery, beskrivelse og prædiktion.",
                ),
            ),
        ),
    ),
    examples=(
        (
            "m04.e01",
            _t(
                "PCA de una matriz con una única dirección dominante",
                "PCA of a matrix with one dominant direction",
                "PCA af en matrix med én dominerende retning",
            ),
            _t(
                "Comprueba varianza explicada e invariancia del signo mediante correlación absoluta.",
                "Check explained variance and sign invariance through absolute correlation.",
                "Kontrollér forklaret varians og fortegnsinvarians med absolut korrelation.",
            ),
            (
                _t(
                    "Las muestras son filas y las características columnas.",
                    "Samples are rows and features are columns.",
                    "Prøver er rækker og features er kolonner.",
                ),
                _t(
                    "Las tres características son proporcionales.",
                    "The three features are proportional.",
                    "De tre features er proportionale.",
                ),
                _t(
                    "La correlación se interpreta en valor absoluto porque el signo de PC1 es arbitrario.",
                    "Correlation is interpreted in absolute value because PC1 sign is arbitrary.",
                    "Korrelation fortolkes absolut, fordi PC1-fortegnet er vilkårligt.",
                ),
            ),
            """x <- matrix(
  c(-1, -2, -3,
     1,  2,  3,
    -2, -4, -6,
     2,  4,  6),
  nrow = 4,
  byrow = TRUE,
  dimnames = list(paste0("S", 1:4), paste0("F", 1:3))
)
fit <- prcomp(x, center = TRUE, scale. = TRUE)
variance <- summary(fit)$importance["Proportion of Variance", 1]
alignment <- abs(cor(fit$x[, 1], x[, 1]))
cat(sprintf("pc1_variance=%.3f\n", variance))
cat(sprintf("abs_cor_pc1_f1=%.3f", alignment))
""",
            """pc1_variance=1.000
abs_cor_pc1_f1=1.000""",
            _t(
                "PC1 captura toda la variación porque las variables aportan la misma dirección. El signo puede cambiar, pero la geometría no.",
                "PC1 captures all variation because the variables contribute the same direction. The sign may change, but the geometry does not.",
                "PC1 indfanger al variation, fordi variablerne bidrager med samme retning. Fortegnet kan ændres, men geometrien gør ikke.",
            ),
        ),
        (
            "m04.e02",
            _t(
                "Verificar una partición jerárquica sin depender de etiquetas",
                "Verify a hierarchical partition without relying on labels",
                "Kontrollér en hierarkisk partition uden at afhænge af labels",
            ),
            _t(
                "Comprueba relaciones dentro y entre grupos en lugar de comparar números de cluster arbitrarios.",
                "Check within- and between-group relations instead of comparing arbitrary cluster numbers.",
                "Kontrollér relationer inden for og mellem grupper i stedet for vilkårlige clusternumre.",
            ),
            (
                _t(
                    "Se construyen dos pares claramente separados.",
                    "Two clearly separated pairs are constructed.",
                    "To tydeligt adskilte par konstrueres.",
                ),
                _t(
                    "Complete linkage produce dos grupos para k = 2.",
                    "Complete linkage produces two groups for k = 2.",
                    "Complete linkage producerer to grupper for k = 2.",
                ),
                _t(
                    "La evaluación usa igualdad de pertenencia.",
                    "Evaluation uses equality of membership.",
                    "Evalueringen bruger lighed i medlemskab.",
                ),
            ),
            """x <- matrix(
  c(0.0, 0.0,
    0.1, 0.2,
    5.0, 5.0,
    5.2, 4.9),
  ncol = 2,
  byrow = TRUE,
  dimnames = list(paste0("S", 1:4), c("F1", "F2"))
)
cluster <- cutree(hclust(dist(x), method = "complete"), k = 2)
cat("within_first=", cluster[1] == cluster[2], "\n", sep = "")
cat("within_second=", cluster[3] == cluster[4], "\n", sep = "")
cat("between_separated=", cluster[1] != cluster[3], sep = "")
""",
            """within_first=TRUE
within_second=TRUE
between_separated=TRUE""",
            _t(
                "Las etiquetas 1 y 2 podrían intercambiarse. Lo reproducible es qué muestras comparten grupo.",
                "Labels 1 and 2 could be exchanged. What is reproducible is which samples share a group.",
                "Labels 1 og 2 kan byttes. Det reproducerbare er hvilke prøver, der deler gruppe.",
            ),
        ),
    ),
    practices=(
        (
            "m04.p01",
            "SHORT_ANSWER",
            _t(
                "Compara distancia euclídea y distancia 1 - correlación para perfiles ómicos.",
                "Compare Euclidean distance and 1 minus correlation distance for omics profiles.",
                "Sammenlign euklidisk afstand og 1 minus korrelationsafstand for omikprofiler.",
            ),
            (
                _t(
                    "Piensa en magnitud frente a forma.",
                    "Think magnitude versus shape.",
                    "Tænk størrelse versus form.",
                ),
                _t(
                    "Indica cuándo el escalado cambia la respuesta.",
                    "State when scaling changes the answer.",
                    "Angiv hvornår skalering ændrer svaret.",
                ),
            ),
            _t(
                "Euclídea mide diferencias absolutas y es sensible a escala; 1 - correlación compara forma relativa y puede considerar similares perfiles con distinta amplitud. La elección depende de si la magnitud o el patrón relativo representa la pregunta biológica.",
                "Euclidean distance measures absolute differences and is scale-sensitive; 1 minus correlation compares relative shape and may treat profiles with different amplitudes as similar. Choice depends on whether magnitude or relative pattern represents the biological question.",
                "Euklidisk afstand måler absolutte forskelle og er skala-følsom; 1 minus korrelation sammenligner relativ form og kan betragte profiler med forskellig amplitude som ens. Valget afhænger af om størrelse eller relativt mønster repræsenterer det biologiske spørgsmål.",
            ),
            _t(
                "La distancia define la noción de similitud y debe justificarse.",
                "Distance defines similarity and must be justified.",
                "Afstand definerer lighed og skal begrundes.",
            ),
            "",
        ),
        (
            "m04.p02",
            "CODE_TRACING",
            _t(
                "Explica qué cambia al ejecutar prcomp(x, scale. = TRUE) frente a scale. = FALSE.",
                "Explain what changes when running prcomp(x, scale. = TRUE) versus scale. = FALSE.",
                "Forklar hvad der ændres ved prcomp(x, scale. = TRUE) versus scale. = FALSE.",
            ),
            (
                _t(
                    "Relaciona varianza con peso geométrico.",
                    "Relate variance to geometric weight.",
                    "Knyt varians til geometrisk vægt.",
                ),
                _t("Menciona unidades.", "Mention units.", "Nævn enheder."),
            ),
            _t(
                "Con scale. = FALSE, variables con mayor varianza o unidades grandes dominan la covarianza. Con TRUE, cada variable se divide por su desviación estándar y PCA opera sobre una geometría equivalente a correlaciones, dando peso comparable a variables con escalas distintas.",
                "With scale. = FALSE, variables with larger variance or units dominate covariance. With TRUE, each variable is divided by its standard deviation and PCA operates on correlation-like geometry, giving comparable weight across scales.",
                "Med scale. = FALSE dominerer variable med større varians eller enheder kovariansen. Med TRUE divideres hver variabel med sin standardafvigelse, og PCA arbejder på en korrelationslignende geometri med sammenlignelig vægt på tværs af skalaer.",
            ),
            _t(
                "Escalar modifica la pregunta, no sólo la apariencia del gráfico.",
                "Scaling changes the question, not only the plot appearance.",
                "Skalering ændrer spørgsmålet, ikke kun plottets udseende.",
            ),
            "",
        ),
        (
            "m04.p03",
            "DATA_INTERPRETATION",
            _t(
                "PC1 explica 38% y separa simultáneamente grupos y lotes. ¿Qué análisis adicionales necesitas?",
                "PC1 explains 38% and separates both groups and batches. What additional analyses are needed?",
                "PC1 forklarer 38% og adskiller både grupper og batches. Hvilke yderligere analyser kræves?",
            ),
            (
                _t(
                    "Revisa el diseño cruzado.",
                    "Inspect cross-classification in the design.",
                    "Undersøg krydsklassifikation i designet.",
                ),
                _t(
                    "Usa loadings y sensibilidad.",
                    "Use loadings and sensitivity analysis.",
                    "Brug loadings og følsomhedsanalyse.",
                ),
            ),
            _t(
                "Debe comprobarse si grupo y lote están confundidos, inspeccionar loadings y métricas QC, colorear por otras covariables, repetir tras ajustes justificados y evaluar si la separación persiste. PCA no identifica por sí sola la causa de PC1.",
                "Check whether group and batch are confounded, inspect loadings and QC metrics, color by other covariates, repeat after justified adjustments, and assess persistence. PCA alone does not identify the cause of PC1.",
                "Kontrollér om gruppe og batch er confounded, inspicér loadings og QC-mål, farv efter andre kovariater, gentag efter begrundede justeringer og vurder om adskillelsen består. PCA identificerer ikke alene årsagen til PC1.",
            ),
            _t(
                "Una componente resume covariación; la atribución causal requiere diseño y evidencia adicional.",
                "A component summarizes covariation; causal attribution requires design and additional evidence.",
                "En komponent opsummerer kovariation; kausal tilskrivning kræver design og yderligere evidens.",
            ),
            "",
        ),
        (
            "m04.p04",
            "DEBUGGING",
            _t(
                "Un modelo selecciona 100 genes usando todo el dataset y luego realiza validación cruzada. Reconstruye la fuga.",
                "A model selects 100 genes using the full dataset and then performs cross-validation. Reconstruct the leakage.",
                "En model vælger 100 gener med hele datasættet og udfører derefter krydsvalidering. Rekonstruér leakage.",
            ),
            (
                _t(
                    "La selección usó etiquetas de todas las muestras.",
                    "Selection used labels from all samples.",
                    "Selektionen brugte labels fra alle prøver.",
                ),
                _t(
                    "Anida el paso dentro de cada fold.",
                    "Nest the step within each fold.",
                    "Indlejr trinnet i hvert fold.",
                ),
            ),
            _t(
                "Las muestras de validación influyeron en qué genes se conservaron, por lo que el modelo ya recibió información de sus outcomes. En cada fold deben estimarse filtro supervisado, transformación, componentes, hiperparámetros y modelo sólo con training, aplicándose después a validación.",
                "Validation samples influenced which genes were retained, so the model already received information about their outcomes. Within each fold, supervised filtering, transformation, components, hyperparameters, and model must be fitted only on training and then applied to validation.",
                "Valideringsprøver påvirkede hvilke gener der blev bevaret, så modellen modtog allerede information om deres outcomes. I hvert fold skal superviseret filtrering, transformation, komponenter, hyperparametre og model kun fittes på training og derefter anvendes på validering.",
            ),
            _t(
                "La validación debe envolver todo paso aprendido de los datos.",
                "Validation must wrap every data-learned step.",
                "Validering skal omslutte hvert trin, der læres fra data.",
            ),
            "",
        ),
        (
            "m04.p05",
            "CODE_COMPLETION",
            _t(
                "Completa una función que compare si dos vectores de cluster representan la misma partición para un conjunto de pares.",
                "Complete a function that compares whether two cluster vectors represent the same partition for a set of pairs.",
                "Færdiggør en funktion, der sammenligner om to clustervektorer repræsenterer samme partition for et sæt par.",
            ),
            (
                _t(
                    "Compara igualdad dentro de cada vector.",
                    "Compare equality within each vector.",
                    "Sammenlign lighed inden for hver vektor.",
                ),
                _t(
                    "No compares los números directamente.",
                    "Do not compare numbers directly.",
                    "Sammenlign ikke tallene direkte.",
                ),
            ),
            _t(
                "same_partition <- function(a, b) { outer(a, a, '==') |> identical(outer(b, b, '==')) }",
                "same_partition <- function(a, b) { outer(a, a, '==') |> identical(outer(b, b, '==')) }",
                "same_partition <- function(a, b) { outer(a, a, '==') |> identical(outer(b, b, '==')) }",
            ),
            _t(
                "Las matrices de co-pertenencia son invariantes a permutar etiquetas.",
                "Co-membership matrices are invariant to label permutation.",
                "Co-memberskabsmatricer er invariante over for labelpermutation.",
            ),
            "same_partition <- function(a, b) {\n  # return TRUE when pairwise memberships agree\n}",
        ),
        (
            "m04.p06",
            "ORAL_EXPLANATION",
            _t(
                "Prepara una explicación de 90 segundos: ¿por qué un cluster visible no demuestra un nuevo subtipo biológico?",
                "Prepare a 90-second explanation: why does a visible cluster not prove a new biological subtype?",
                "Forbered en 90-sekunders forklaring: hvorfor beviser en synlig cluster ikke en ny biologisk subtype?",
            ),
            (
                _t(
                    "Incluye dependencia del método.",
                    "Include method dependence.",
                    "Medtag metodeafhængighed.",
                ),
                _t(
                    "Incluye validación externa.",
                    "Include external validation.",
                    "Medtag ekstern validering.",
                ),
            ),
            _t(
                "El cluster depende de selección de muestras y variables, transformación, distancia, linkage y número de grupos. Puede reflejar lote, calidad o covariables. Debe ser estable bajo perturbaciones, asociarse con evidencia biológica independiente y replicarse en otra cohorte antes de sostener un subtipo.",
                "The cluster depends on sample and feature selection, transformation, distance, linkage, and group count. It may reflect batch, quality, or covariates. It should be stable under perturbations, supported by independent biological evidence, and replicated in another cohort before claiming a subtype.",
                "Clusteren afhænger af valg af prøver og features, transformation, afstand, linkage og gruppeantal. Den kan afspejle batch, kvalitet eller kovariater. Den bør være stabil under perturbationer, understøttet af uafhængig biologisk evidens og replikeret i en anden kohorte før en subtype hævdes.",
            ),
            _t(
                "La respuesta distingue patrón exploratorio, estabilidad, interpretación y replicación.",
                "The answer separates exploratory pattern, stability, interpretation, and replication.",
                "Svaret adskiller eksplorativt mønster, stabilitet, fortolkning og replikation.",
            ),
            "",
        ),
    ),
    mcqs=(
        _mcq(
            "q01",
            _t(
                "¿Qué representa un score de PCA?",
                "What does a PCA score represent?",
                "Hvad repræsenterer en PCA-score?",
            ),
            (
                _option(
                    "a",
                    _t(
                        "La posición de una muestra en una componente",
                        "A sample position on a component",
                        "En prøves position på en komponent",
                    ),
                ),
                _option("b", _t("Un valor p", "A p-value", "En p-værdi")),
                _option("c", _t("La anotación de un gen", "A gene annotation", "En genannotering")),
                _option(
                    "d", _t("Un cluster confirmado", "A confirmed cluster", "En bekræftet cluster")
                ),
            ),
            "a",
            _t(
                "Los scores son coordenadas de muestras en el espacio de componentes.",
                "Scores are sample coordinates in component space.",
                "Scores er prøvekoordinater i komponentrummet.",
            ),
        ),
        _mcq(
            "q02",
            _t(
                "¿Qué representa un loading?",
                "What does a loading represent?",
                "Hvad repræsenterer en loading?",
            ),
            (
                _option(
                    "a",
                    _t(
                        "Contribución de una variable a una componente",
                        "A variable contribution to a component",
                        "En variabels bidrag til en komponent",
                    ),
                ),
                _option("b", _t("Tamaño de muestra", "Sample size", "Stikprøvestørrelse")),
                _option("c", _t("Etiqueta de lote", "Batch label", "Batchlabel")),
                _option("d", _t("FDR", "FDR", "FDR")),
            ),
            "a",
            _t(
                "Los loadings definen la combinación lineal.",
                "Loadings define the linear combination.",
                "Loadings definerer den lineære kombination.",
            ),
        ),
        _mcq(
            "q03",
            _t(
                "¿Por qué se usa valor absoluto al comparar una componente entre ejecuciones?",
                "Why use absolute value when comparing a component across runs?",
                "Hvorfor bruges absolut værdi ved sammenligning af en komponent mellem kørsler?",
            ),
            (
                _option(
                    "a",
                    _t(
                        "El signo de PCA es arbitrario",
                        "PCA sign is arbitrary",
                        "PCA-fortegnet er vilkårligt",
                    ),
                ),
                _option(
                    "b",
                    _t(
                        "La varianza siempre es negativa",
                        "Variance is always negative",
                        "Varians er altid negativ",
                    ),
                ),
                _option(
                    "c",
                    _t(
                        "Los genes no tienen signo", "Genes have no sign", "Gener har intet fortegn"
                    ),
                ),
                _option("d", _t("Para aumentar R²", "To increase R-squared", "For at øge R²")),
            ),
            "a",
            _t(
                "Invertir scores y loadings deja la solución geométrica intacta.",
                "Reversing scores and loadings leaves the geometric solution unchanged.",
                "Vending af scores og loadings efterlader den geometriske løsning uændret.",
            ),
        ),
        _mcq(
            "q04",
            _t(
                "¿Qué distancia enfatiza forma de perfil más que magnitud?",
                "Which distance emphasizes profile shape more than magnitude?",
                "Hvilken afstand fremhæver profilform mere end størrelse?",
            ),
            (
                _option("a", _t("1 - correlación", "1 minus correlation", "1 minus korrelation")),
                _option(
                    "b", _t("Euclídea sin escalar", "Unscaled Euclidean", "Uskaleret euklidisk")
                ),
                _option("c", _t("Número de filas", "Row count", "Antal rækker")),
                _option("d", _t("Valor p", "P-value", "P-værdi")),
            ),
            "a",
            _t(
                "La correlación compara patrones relativos.",
                "Correlation compares relative patterns.",
                "Korrelation sammenligner relative mønstre.",
            ),
        ),
        _mcq(
            "q05",
            _t(
                "¿Qué prueba mejor la estabilidad de un cluster?",
                "What best tests cluster stability?",
                "Hvad tester bedst clusterstabilitet?",
            ),
            (
                _option(
                    "a",
                    _t(
                        "Repetir bajo remuestreo y parámetros razonables",
                        "Repeat under resampling and reasonable parameters",
                        "Gentag under resampling og rimelige parametre",
                    ),
                ),
                _option("b", _t("Cambiar colores", "Change colors", "Skift farver")),
                _option(
                    "c",
                    _t(
                        "Elegir el dendrograma más bonito",
                        "Choose the nicest dendrogram",
                        "Vælg det pæneste dendrogram",
                    ),
                ),
                _option("d", _t("Usar una sola distancia", "Use one distance", "Brug én afstand")),
            ),
            "a",
            _t(
                "La estabilidad exige que relaciones relevantes persistan ante perturbaciones plausibles.",
                "Stability requires relevant relations to persist under plausible perturbations.",
                "Stabilitet kræver at relevante relationer består under plausible perturbationer.",
            ),
        ),
        _mcq(
            "q06",
            _t(
                "¿Qué paso produce fuga si se realiza antes de cross-validation?",
                "Which step causes leakage when done before cross-validation?",
                "Hvilket trin skaber leakage, hvis det udføres før krydsvalidering?",
            ),
            (
                _option(
                    "a",
                    _t(
                        "Seleccionar genes usando todas las etiquetas",
                        "Select genes using all labels",
                        "Vælg gener med alle labels",
                    ),
                ),
                _option("b", _t("Definir IDs", "Define IDs", "Definér ID'er")),
                _option("c", _t("Conservar datos fuente", "Retain source data", "Bevar kildedata")),
                _option(
                    "d", _t("Documentar versiones", "Document versions", "Dokumentér versioner")
                ),
            ),
            "a",
            _t(
                "La selección supervisada debe ajustarse dentro de training.",
                "Supervised selection must be fitted within training.",
                "Superviseret selektion skal fittes inden for training.",
            ),
        ),
        _mcq(
            "q07",
            _t(
                "¿Qué demuestra por sí solo un dendrograma?",
                "What does a dendrogram prove by itself?",
                "Hvad beviser et dendrogram i sig selv?",
            ),
            (
                _option(
                    "a",
                    _t(
                        "Sólo la secuencia de fusiones bajo decisiones específicas",
                        "Only the merge sequence under specific decisions",
                        "Kun fusionssekvensen under specifikke valg",
                    ),
                ),
                _option("b", _t("Subtipos reales", "True subtypes", "Sande subtyper")),
                _option("c", _t("Causalidad", "Causality", "Kausalitet")),
                _option("d", _t("Replicación", "Replication", "Replikation")),
            ),
            "a",
            _t(
                "La estructura depende de datos, distancia, linkage y preprocesamiento.",
                "Structure depends on data, distance, linkage, and preprocessing.",
                "Strukturen afhænger af data, afstand, linkage og præprocessering.",
            ),
        ),
        _mcq(
            "q08",
            _t(
                "¿Qué comparación de clusters es invariante a intercambiar etiquetas?",
                "Which cluster comparison is invariant to label swapping?",
                "Hvilken clustersammenligning er invariant over for labelbytning?",
            ),
            (
                _option(
                    "a",
                    _t(
                        "Co-pertenencia por pares",
                        "Pairwise co-membership",
                        "Parvist co-medlemskab",
                    ),
                ),
                _option(
                    "b",
                    _t(
                        "Igualdad numérica directa",
                        "Direct numeric equality",
                        "Direkte numerisk lighed",
                    ),
                ),
                _option("c", _t("Media de etiquetas", "Mean label", "Middel label")),
                _option("d", _t("Orden alfabético", "Alphabetic order", "Alfabetisk rækkefølge")),
            ),
            "a",
            _t(
                "Las relaciones de pertenencia no dependen del nombre del cluster.",
                "Membership relations do not depend on cluster names.",
                "Medlemskabsrelationer afhænger ikke af clusternavne.",
            ),
        ),
    ),
    true_false=(
        _tf(
            "tf01",
            _t(
                "La varianza explicada mide directamente importancia biológica.",
                "Explained variance directly measures biological importance.",
                "Forklaret varians måler direkte biologisk betydning.",
            ),
            False,
            _t(
                "Mide variación capturada, que puede ser técnica o biológica.",
                "It measures captured variation, which may be technical or biological.",
                "Den måler indfanget variation, som kan være teknisk eller biologisk.",
            ),
        ),
        _tf(
            "tf02",
            _t(
                "El signo de una componente principal puede invertirse sin cambiar PCA.",
                "A principal component sign may reverse without changing PCA.",
                "Fortegnet på en hovedkomponent kan vendes uden at ændre PCA.",
            ),
            True,
            _t(
                "Scores y loadings pueden multiplicarse por -1 conjuntamente.",
                "Scores and loadings may both be multiplied by -1.",
                "Scores og loadings kan begge multipliceres med -1.",
            ),
        ),
        _tf(
            "tf03",
            _t(
                "Escalar variables puede cambiar qué estructura domina PCA.",
                "Scaling variables can change which structure dominates PCA.",
                "Skalering af variable kan ændre hvilken struktur der dominerer PCA.",
            ),
            True,
            _t(
                "El escalado modifica el peso relativo de las variables.",
                "Scaling changes relative variable weight.",
                "Skalering ændrer variablernes relative vægt.",
            ),
        ),
        _tf(
            "tf04",
            _t(
                "Las etiquetas numéricas de cluster tienen significado intrínseco.",
                "Numeric cluster labels have intrinsic meaning.",
                "Numeriske clusterlabels har iboende betydning.",
            ),
            False,
            _t(
                "Las etiquetas son arbitrarias; importa la partición.",
                "Labels are arbitrary; the partition matters.",
                "Labels er vilkårlige; partitionen er vigtig.",
            ),
        ),
        _tf(
            "tf05",
            _t(
                "Un patrón inestable debe comunicarse como exploratorio.",
                "An unstable pattern should be communicated as exploratory.",
                "Et ustabilt mønster bør kommunikeres som eksplorativt.",
            ),
            True,
            _t(
                "La fragilidad limita generalización e interpretación.",
                "Fragility limits generalization and interpretation.",
                "Skrøbelighed begrænser generalisering og fortolkning.",
            ),
        ),
        _tf(
            "tf06",
            _t(
                "Seleccionar features con todo el dataset antes de validar es aceptable si PCA es no supervisado.",
                "Selecting features on the full dataset before validation is acceptable when PCA is unsupervised.",
                "Featurevalg på hele datasættet før validering er acceptabelt, når PCA er usuperviseret.",
            ),
            False,
            _t(
                "Si la selección usa outcomes o decisiones optimizadas, produce fuga independientemente del paso posterior.",
                "If selection uses outcomes or optimized decisions, it causes leakage regardless of the later step.",
                "Hvis selektionen bruger outcomes eller optimerede beslutninger, skaber den leakage uanset det senere trin.",
            ),
        ),
        _tf(
            "tf07",
            _t(
                "La separación por grupo en PCA puede reflejar lote confundido.",
                "Group separation in PCA may reflect a confounded batch.",
                "Gruppeadskillelse i PCA kan afspejle et confounded batch.",
            ),
            True,
            _t(
                "PCA resume variación y no asigna su causa.",
                "PCA summarizes variation and does not assign its cause.",
                "PCA opsummerer variation og tildeler ikke årsagen.",
            ),
        ),
        _tf(
            "tf08",
            _t(
                "Un cluster replicado externamente ofrece evidencia más fuerte que uno visto una sola vez.",
                "An externally replicated cluster provides stronger evidence than one seen once.",
                "En eksternt replikeret cluster giver stærkere evidens end en, der ses én gang.",
            ),
            True,
            _t(
                "La replicación evalúa generalización fuera del dataset de descubrimiento.",
                "Replication assesses generalization beyond the discovery dataset.",
                "Replikation vurderer generalisering ud over discovery-datasættet.",
            ),
        ),
    ),
    tutor=(
        _t(
            "El tutor debe tratar PCA y clustering como herramientas dependientes de geometría y preprocesamiento. Debe exigir estabilidad, metadata, sensibilidad y separación estricta entre exploración y predicción.",
            "The tutor must treat PCA and clustering as tools dependent on geometry and preprocessing. It should require stability, metadata, sensitivity, and strict separation between exploration and prediction.",
            "Tutoren skal behandle PCA og clustering som værktøjer, der afhænger af geometri og præprocessering. Den bør kræve stabilitet, metadata, følsomhed og streng adskillelse mellem udforskning og prædiktion.",
        ),
        (
            _t(
                "Preprocesamiento y distancia definen la geometría.",
                "Preprocessing and distance define geometry.",
                "Præprocessering og afstand definerer geometrien.",
            ),
            _t(
                "Scores, loadings y metadata se interpretan conjuntamente.",
                "Scores, loadings, and metadata are interpreted jointly.",
                "Scores, loadings og metadata fortolkes samlet.",
            ),
            _t(
                "Clusters requieren estabilidad y validación externa.",
                "Clusters require stability and external validation.",
                "Clusters kræver stabilitet og ekstern validering.",
            ),
            _t(
                "Todo paso supervisado se ajusta dentro de resampling.",
                "Every supervised step is fitted within resampling.",
                "Hvert superviseret trin fittes inden for resampling.",
            ),
        ),
        (
            _t(
                "Declarar subtipos por una sola figura.",
                "Declare subtypes from one figure.",
                "Deklarér subtyper fra én figur.",
            ),
            _t(
                "Interpretar varianza explicada como importancia biológica.",
                "Interpret explained variance as biological importance.",
                "Fortolk forklaret varians som biologisk betydning.",
            ),
            _t(
                "Comparar etiquetas de cluster directamente.",
                "Compare cluster labels directly.",
                "Sammenlign clusterlabels direkte.",
            ),
            _t(
                "Seleccionar variables antes de validación supervisada.",
                "Select variables before supervised validation.",
                "Vælg variable før superviseret validering.",
            ),
        ),
        (
            _t(
                "¿Qué geometría crea el preprocesamiento?",
                "What geometry does preprocessing create?",
                "Hvilken geometri skaber præprocesseringen?",
            ),
            _t(
                "¿Qué metadata se alinea con scores o clusters?",
                "Which metadata aligns with scores or clusters?",
                "Hvilke metadata følger scores eller clusters?",
            ),
            _t(
                "¿El patrón es estable a perturbaciones plausibles?",
                "Is the pattern stable to plausible perturbations?",
                "Er mønsteret stabilt over for plausible perturbationer?",
            ),
            _t(
                "¿Algún paso aprendió información fuera de training?",
                "Did any step learn information outside training?",
                "Lærte noget trin information uden for training?",
            ),
        ),
        (
            _t(
                "Justifica transformación, escalado y distancia.",
                "Justifies transformation, scaling, and distance.",
                "Begrunder transformation, skalering og afstand.",
            ),
            _t(
                "Interpreta componentes sin sobreafirmar.",
                "Interprets components without overclaiming.",
                "Fortolker komponenter uden overdrivelse.",
            ),
            _t(
                "Evalúa estabilidad y alternativas.",
                "Assesses stability and alternatives.",
                "Vurderer stabilitet og alternativer.",
            ),
            _t(
                "Previene fuga en análisis supervisado.",
                "Prevents leakage in supervised analysis.",
                "Forhindrer leakage i superviseret analyse.",
            ),
        ),
        (
            _t(
                "No inferir causalidad desde una proyección.",
                "Do not infer causality from a projection.",
                "Inferér ikke kausalitet fra en projektion.",
            ),
            _t(
                "No inventar un número verdadero de clusters.",
                "Do not invent a true cluster count.",
                "Opfind ikke et sandt antal clusters.",
            ),
            _t(
                "No ocultar sensibilidad a parámetros.",
                "Do not hide parameter sensitivity.",
                "Skjul ikke parameterfølsomhed.",
            ),
            _t(
                "Responder en el idioma activo y preservar términos técnicos.",
                "Respond in the active language and preserve technical terms.",
                "Svar på det aktive sprog og bevar tekniske termer.",
            ),
        ),
        (
            "https://odin.sdu.dk/sitecore/index.php?a=searchfagbesk&internkode=BMB831&lang=en",
            "https://bioconductor.org/help/course-materials/",
        ),
    ),
)

LOCALIZED_MODULE_04_MULTIVARIATE_OMICS = build_module(_SPEC)
LOCALIZED_OBJECTIVE_QUESTION_BANK_04 = build_question_bank(_SPEC)


def materialize_module_04_question_bank(
    locale: AppLocale | str = AppLocale.SPANISH_SPAIN,
) -> tuple[AssessmentItem, ...]:
    """Materialize the stable module 4 objective bank."""

    return materialize_bank(LOCALIZED_OBJECTIVE_QUESTION_BANK_04, locale)


MODULE_04_MULTIVARIATE_OMICS: LearningModule = LOCALIZED_MODULE_04_MULTIVARIATE_OMICS.materialize(
    AppLocale.SPANISH_SPAIN
)
OBJECTIVE_QUESTION_BANK_04 = materialize_module_04_question_bank()

__all__ = [
    "LOCALIZED_MODULE_04_MULTIVARIATE_OMICS",
    "LOCALIZED_OBJECTIVE_QUESTION_BANK_04",
    "MODULE_04_MULTIVARIATE_OMICS",
    "OBJECTIVE_QUESTION_BANK_04",
    "materialize_module_04_question_bank",
]
