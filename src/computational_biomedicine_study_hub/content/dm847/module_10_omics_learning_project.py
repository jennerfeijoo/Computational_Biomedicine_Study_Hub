"""DM847 module 10: OMICS learning, validation, and integrative project."""

from __future__ import annotations

from ...i18n import AppLocale
from ..localized_models import LocalizedLearningModule
from ..models import AssessmentItem, LearningModule
from .standard import StandardModuleSpec, build_module, build_question_bank, materialize_bank

_SPEC = StandardModuleSpec(
    module_id="dm847.m10",
    title=(
        "Aprendizaje sobre OMICS y proyecto integrador",
        "Learning from OMICS data and integrative project",
        "Læring fra OMICS-data og integrerende projekt",
    ),
    summary=(
        "Estructura matrices ómicas, preprocesamiento y modelos supervisados/no supervisados con validación anidada, control de fuga, interpretación y comunicación reproducible de un proyecto bioinformático completo.",
        "Structure OMICS matrices, preprocessing, and supervised or unsupervised models with nested validation, leakage control, interpretation, and reproducible communication of a complete bioinformatics project.",
        "Strukturér OMICS-matricer, preprocessing og superviserede eller usuperviserede modeller med nested validering, leakage-kontrol, fortolkning og reproducerbar kommunikation af et komplet bioinformatikprojekt.",
    ),
    objectives=(
        (
            "m10.o1",
            (
                "Definir muestras, características, outcomes, grupos y unidades experimentales.",
                "Define samples, features, outcomes, groups, and experimental units.",
                "Definere prøver, features, outcomes, grupper og eksperimentelle enheder.",
            ),
        ),
        (
            "m10.o2",
            (
                "Aplicar filtrado, transformación, imputación y escalado dentro de validación.",
                "Apply filtering, transformation, imputation, and scaling within validation.",
                "Anvende filtrering, transformation, imputering og skalering inden for validering.",
            ),
        ),
        (
            "m10.o3",
            (
                "Interpretar PCA, clustering y embeddings como descripciones dependientes del preprocesamiento.",
                "Interpret PCA, clustering, and embeddings as preprocessing-dependent descriptions.",
                "Fortolke PCA, clustering og embeddings som beskrivelser afhængige af preprocessing.",
            ),
        ),
        (
            "m10.o4",
            (
                "Entrenar modelos supervisados con validación agrupada y anidada.",
                "Train supervised models with grouped and nested validation.",
                "Træne superviserede modeller med grouped og nested validering.",
            ),
        ),
        (
            "m10.o5",
            (
                "Evaluar desbalance, calibración, selección de características e interpretación estable.",
                "Evaluate imbalance, calibration, feature selection, and stable interpretation.",
                "Evaluere ubalance, kalibrering, feature-selektion og stabil fortolkning.",
            ),
        ),
        (
            "m10.o6",
            (
                "Diseñar, documentar y defender un proyecto bioinformático reproducible.",
                "Design, document, and defend a reproducible bioinformatics project.",
                "Designe, dokumentere og forsvare et reproducerbart bioinformatikprojekt.",
            ),
        ),
    ),
    concepts=(
        (
            "data-matrix",
            ("Matriz de datos y unidad experimental", "Data matrix and experimental unit", "Datamatrix og eksperimentel enhed"),
            (
                "En matriz ómica suele organizar muestras en filas y características en columnas, pero la convención debe declararse. La unidad independiente puede ser paciente, animal, línea celular, lote o sujeto longitudinal, no cada aliquot o medición. Outcome, covariables, batch, tiempo y grupos de parentesco deben separarse de las features para evitar fuga y pseudorreplicación.",
                "An OMICS matrix often places samples in rows and features in columns, but the convention must be declared. The independent unit may be a patient, animal, cell line, batch, or longitudinal subject, not every aliquot or measurement. Outcome, covariates, batch, time, and relatedness groups should be separated from features to avoid leakage and pseudoreplication.",
                "En OMICS-matrix placerer ofte prøver i rækker og features i kolonner, men konventionen skal erklæres. Den uafhængige enhed kan være patient, dyr, cellelinje, batch eller longitudinelt subjekt, ikke hver aliquot eller måling. Outcome, kovariater, batch, tid og slægtskabsgrupper bør adskilles fra features for at undgå leakage og pseudoreplikation.",
            ),
            (
                (
                    "La unidad de split debe coincidir con la unidad independiente.",
                    "The splitting unit should match the independent unit.",
                    "Split-enheden bør svare til den uafhængige enhed.",
                ),
                (
                    "IDs y metadatos no deben entrar accidentalmente como predictores.",
                    "IDs and metadata should not accidentally enter as predictors.",
                    "ID'er og metadata bør ikke utilsigtet indgå som prædiktorer.",
                ),
            ),
        ),
        (
            "preprocessing",
            ("Preprocesamiento dentro del pipeline", "Preprocessing inside the pipeline", "Preprocessing i pipelinen"),
            (
                "Filtrado por baja abundancia, transformación logarítmica o estabilizadora, normalización, imputación, escalado y selección de variables pueden aprender información de los datos. Cada parámetro debe estimarse sólo en entrenamiento y aplicarse sin reajuste a validación y test. Batch correction que utiliza outcomes o mezcla folds también produce fuga.",
                "Low-abundance filtering, log or variance-stabilizing transformation, normalization, imputation, scaling, and feature selection can learn information from data. Every parameter should be estimated on training data only and applied without refitting to validation and test. Batch correction using outcomes or mixing folds also creates leakage.",
                "Filtrering af lav abundans, log- eller variansstabiliserende transformation, normalisering, imputering, skalering og feature-selektion kan lære information fra data. Hver parameter bør estimeres kun på træningsdata og anvendes uden genfit på validering og test. Batch-korrektion, der bruger outcomes eller blander folds, skaber også leakage.",
            ),
            (
                (
                    "El preprocesamiento aprendido forma parte del modelo.",
                    "Learned preprocessing is part of the model.",
                    "Lært preprocessing er en del af modellen.",
                ),
                (
                    "El test no debe influir en filtros ni hiperparámetros.",
                    "Test data should not influence filters or hyperparameters.",
                    "Testdata bør ikke påvirke filtre eller hyperparametre.",
                ),
            ),
        ),
        (
            "unsupervised",
            ("Aprendizaje no supervisado", "Unsupervised learning", "Usuperviseret læring"),
            (
                "PCA encuentra direcciones lineales de varianza; clustering agrupa según una distancia, transformación y algoritmo; t-SNE o UMAP priorizan vecindarios bajo parámetros concretos. Estas técnicas revelan estructura descriptiva, outliers y batch, pero no validan categorías clínicas por sí solas. La estabilidad se evalúa con remuestreo y perturbaciones.",
                "PCA finds linear directions of variance; clustering groups according to a distance, transformation, and algorithm; t-SNE or UMAP prioritize neighborhoods under specific parameters. These methods reveal descriptive structure, outliers, and batch but do not validate clinical categories by themselves. Stability is assessed through resampling and perturbations.",
                "PCA finder lineære variansretninger; clustering grupperer efter afstand, transformation og algoritme; t-SNE eller UMAP prioriterer nabolag under bestemte parametre. Metoderne afslører deskriptiv struktur, outliers og batch, men validerer ikke kliniske kategorier alene. Stabilitet vurderes gennem resampling og perturbationer.",
            ),
            (
                (
                    "PCA depende de escala y centrado.",
                    "PCA depends on scaling and centering.",
                    "PCA afhænger af skalering og centrering.",
                ),
                (
                    "Clusters visuales pueden ser inestables o impulsados por batch.",
                    "Visual clusters may be unstable or batch-driven.",
                    "Visuelle clusters kan være ustabile eller batch-drevne.",
                ),
            ),
        ),
        (
            "supervised-validation",
            ("Modelado supervisado y validación", "Supervised modeling and validation", "Superviseret modellering og validering"),
            (
                "En tarea supervisada define outcome, horizonte, población y métrica antes de ajustar. Cross-validation agrupada mantiene sujetos o familias juntos. Nested CV separa selección de hiperparámetros en folds internos y estimación de rendimiento en folds externos. Un test final se consulta una vez después de congelar el pipeline.",
                "A supervised task defines outcome, horizon, population, and metric before fitting. Grouped cross-validation keeps subjects or families together. Nested CV separates hyperparameter selection in inner folds from performance estimation in outer folds. A final test set is evaluated once after freezing the pipeline.",
                "En superviseret opgave definerer outcome, horisont, population og metrik før fit. Grouped cross-validation holder subjekter eller familier samlet. Nested CV adskiller hyperparameterselektion i indre folds fra præstationsestimering i ydre folds. Et endeligt testsæt evalueres én gang efter fastlåsning af pipelinen.",
            ),
            (
                (
                    "El fold externo no participa en selección.",
                    "The outer fold does not participate in selection.",
                    "Det ydre fold deltager ikke i selektion.",
                ),
                (
                    "Repetir decisiones tras ver test convierte test en entrenamiento.",
                    "Repeating decisions after seeing test turns test into training.",
                    "Gentagne beslutninger efter testvisning gør test til træning.",
                ),
            ),
        ),
        (
            "metrics-interpretation",
            ("Métricas e interpretación", "Metrics and interpretation", "Metrikker og fortolkning"),
            (
                "Accuracy puede ocultar clases raras. Sensibilidad, especificidad, precision, recall, AUROC, AUPRC, calibración y utilidad responden preguntas diferentes. La importancia de características puede ser inestable bajo correlación y no implica causalidad. Deben reportarse intervalos, distribución entre folds, baselines y análisis de errores.",
                "Accuracy can hide rare classes. Sensitivity, specificity, precision, recall, AUROC, AUPRC, calibration, and utility answer different questions. Feature importance may be unstable under correlation and does not imply causality. Report intervals, fold distributions, baselines, and error analysis.",
                "Accuracy kan skjule sjældne klasser. Sensitivitet, specificitet, precision, recall, AUROC, AUPRC, kalibrering og nytte besvarer forskellige spørgsmål. Feature-importance kan være ustabil ved korrelation og indebærer ikke kausalitet. Rapportér intervaller, foldfordelinger, baselines og fejlanalyse.",
            ),
            (
                (
                    "La métrica debe corresponder a prevalencia y decisión.",
                    "The metric should match prevalence and decision.",
                    "Metrikken bør passe til prævalens og beslutning.",
                ),
                (
                    "Interpretabilidad local y estabilidad global no son equivalentes.",
                    "Local interpretability and global stability are not equivalent.",
                    "Lokal fortolkbarhed og global stabilitet er ikke det samme.",
                ),
            ),
        ),
        (
            "project-reproducibility",
            ("Proyecto y defensa reproducible", "Reproducible project and defense", "Reproducerbart projekt og forsvar"),
            (
                "Un proyecto sólido delimita pregunta, datos, permisos, diccionario, versiones, hipótesis, baselines, pipeline, validación, resultados, limitaciones y artefactos ejecutables. La defensa oral debe explicar decisiones, no sólo mostrar métricas. Un análisis negativo o inconcluso puede ser valioso si el diseño, la auditoría y la interpretación son rigurosos.",
                "A strong project defines question, data, permissions, dictionary, versions, hypotheses, baselines, pipeline, validation, results, limitations, and executable artifacts. The oral defense should explain decisions, not merely show metrics. A negative or inconclusive analysis can be valuable when design, audit, and interpretation are rigorous.",
                "Et stærkt projekt afgrænser spørgsmål, data, tilladelser, ordbog, versioner, hypoteser, baselines, pipeline, validering, resultater, begrænsninger og eksekverbare artefakter. Det mundtlige forsvar bør forklare beslutninger, ikke kun vise metrikker. En negativ eller inkonklusiv analyse kan være værdifuld, når design, audit og fortolkning er strenge.",
            ),
            (
                (
                    "Código, entorno y datos derivados deben ser trazables.",
                    "Code, environment, and derived data should be traceable.",
                    "Kode, miljø og afledte data bør være sporbare.",
                ),
                (
                    "La defensa debe anticipar alternativas y amenazas a validez.",
                    "The defense should anticipate alternatives and validity threats.",
                    "Forsvaret bør forudse alternativer og trusler mod validitet.",
                ),
            ),
        ),
    ),
    examples=(
        (
            "m10.e01",
            ("Estandarización sin fuga", "Leakage-free standardization", "Leakage-fri standardisering"),
            (
                "Ajusta media y desviación en entrenamiento y transforma test con los mismos parámetros.",
                "Fit mean and standard deviation on training data and transform test with the same parameters.",
                "Tilpas middelværdi og standardafvigelse på træningsdata og transformér test med de samme parametre.",
            ),
            (
                (
                    "Cada columna se ajusta independientemente.",
                    "Each column is fitted independently.",
                    "Hver kolonne tilpasses uafhængigt.",
                ),
                (
                    "El test nunca recalcula parámetros.",
                    "Test data never recomputes parameters.",
                    "Testdata genberegner aldrig parametre.",
                ),
            ),
            """def fit_standardizer(rows: list[list[float]]) -> tuple[list[float], list[float]]:
    columns = list(zip(*rows, strict=True))
    means = [sum(column) / len(column) for column in columns]
    scales = [
        (sum((value - mean) ** 2 for value in column) / len(column)) ** 0.5 or 1.0
        for column, mean in zip(columns, means, strict=True)
    ]
    return means, scales


def transform(rows, means, scales):
    return [
        [(value - mean) / scale for value, mean, scale in zip(row, means, scales, strict=True)]
        for row in rows
    ]


train = [[1.0, 10.0], [3.0, 14.0]]
test = [[5.0, 18.0]]
means, scales = fit_standardizer(train)
print(transform(test, means, scales))
""",
            "[[3.0, 3.0]]",
            (
                "El ejemplo hace explícito que los parámetros proceden sólo de entrenamiento.",
                "The example makes explicit that parameters come only from training.",
                "Eksemplet gør det eksplicit, at parametrene kun kommer fra træning.",
            ),
        ),
        (
            "m10.e02",
            ("PCA mediante covarianza", "PCA through covariance", "PCA gennem kovarians"),
            (
                "Calcula una dirección principal simple con NumPy y reporta varianza explicada.",
                "Compute a simple principal direction with NumPy and report explained variance.",
                "Beregn en simpel hovedretning med NumPy og rapportér forklaret varians.",
            ),
            (
                (
                    "Los datos se centran antes de descomponer.",
                    "Data are centered before decomposition.",
                    "Data centreres før dekomposition.",
                ),
                (
                    "Los autovalores se ordenan de mayor a menor.",
                    "Eigenvalues are ordered from largest to smallest.",
                    "Egenværdier ordnes fra størst til mindst.",
                ),
            ),
            """import numpy as np


def first_pc(matrix: np.ndarray) -> tuple[np.ndarray, float]:
    centered = matrix - matrix.mean(axis=0)
    covariance = np.cov(centered, rowvar=False)
    values, vectors = np.linalg.eigh(covariance)
    order = np.argsort(values)[::-1]
    explained = float(values[order[0]] / values.sum())
    return vectors[:, order[0]], explained


vector, explained = first_pc(np.array([[1.0, 1.0], [2.0, 2.0], [3.0, 3.0]]))
print(round(abs(float(vector[0])), 3), round(explained, 3))
""",
            "0.707 1.0",
            (
                "La dirección captura toda la varianza de puntos colineales; no demuestra una clase biológica.",
                "The direction captures all variance of collinear points; it does not prove a biological class.",
                "Retningen fanger al varians i kollineære punkter; den beviser ikke en biologisk klasse.",
            ),
        ),
        (
            "m10.e03",
            ("Partición agrupada", "Grouped splitting", "Grupperet split"),
            (
                "Crea folds sin distribuir muestras del mismo sujeto entre entrenamiento y validación.",
                "Create folds without distributing samples from the same subject across training and validation.",
                "Opret folds uden at fordele prøver fra samme subjekt mellem træning og validering.",
            ),
            (
                (
                    "Se asignan grupos, no filas individuales.",
                    "Groups, not individual rows, are assigned.",
                    "Grupper, ikke individuelle rækker, tildeles.",
                ),
                (
                    "Todas las mediciones de un sujeto permanecen juntas.",
                    "All measurements from one subject remain together.",
                    "Alle målinger fra ét subjekt forbliver sammen.",
                ),
            ),
            """def grouped_folds(groups: list[str], fold_count: int) -> list[list[int]]:
    unique_groups = sorted(set(groups))
    assignment = {group: index % fold_count for index, group in enumerate(unique_groups)}
    folds = [[] for _ in range(fold_count)]
    for row_index, group in enumerate(groups):
        folds[assignment[group]].append(row_index)
    return folds


print(grouped_folds(["P1", "P1", "P2", "P3", "P3"], 2))
""",
            "[[0, 1, 3, 4], [2]]",
            (
                "La partición evita que réplicas del mismo sujeto aparezcan a ambos lados.",
                "The split prevents replicates from the same subject appearing on both sides.",
                "Splittet forhindrer replikater fra samme subjekt i at optræde på begge sider.",
            ),
        ),
    ),
    practices=(
        (
            "m10.p01",
            "SHORT_ANSWER",
            (
                "Distingue muestra, réplica técnica y unidad experimental.",
                "Distinguish sample, technical replicate, and experimental unit.",
                "Skeln mellem prøve, teknisk replikat og eksperimentel enhed.",
            ),
            (("Piensa en independencia.", "Think independence.", "Tænk på uafhængighed."),),
            (
                "Una muestra es el material medido; una réplica técnica repite medición del mismo material; la unidad experimental es la entidad independientemente asignada o inferida, como paciente o animal.",
                "A sample is measured material; a technical replicate repeats measurement of the same material; the experimental unit is the independently assigned or inferred entity, such as a patient or animal.",
                "En prøve er det målte materiale; et teknisk replikat gentager målingen af samme materiale; den eksperimentelle enhed er den uafhængigt tildelte eller infererede entitet, såsom patient eller dyr.",
            ),
            (
                "Tratar réplicas como sujetos infla el tamaño efectivo.",
                "Treating replicates as subjects inflates effective sample size.",
                "Behandling af replikater som subjekter oppuster effektiv stikprøvestørrelse.",
            ),
            "",
        ),
        (
            "m10.p02",
            "ORDERING",
            (
                "Ordena: definir split, ajustar imputador, ajustar escalador, seleccionar features, entrenar, evaluar fold.",
                "Order: define split, fit imputer, fit scaler, select features, train, evaluate fold.",
                "Ordén: definér split, tilpas imputering, tilpas skalering, vælg features, træn, evaluér fold.",
            ),
            (("Todo ajuste ocurre después del split.", "All fitting occurs after splitting.", "Alt fit sker efter split."),),
            (
                "Definir split → ajustar imputador en train → ajustar escalador en train → seleccionar features en train → entrenar → transformar y evaluar validación.",
                "Define split → fit imputer on train → fit scaler on train → select features on train → train → transform and evaluate validation.",
                "Definér split → tilpas imputering på train → tilpas skalering på train → vælg features på train → træn → transformér og evaluér validering.",
            ),
            (
                "La selección previa al split produce fuga.",
                "Selection before splitting creates leakage.",
                "Selektion før split skaber leakage.",
            ),
            "",
        ),
        (
            "m10.p03",
            "DATA_INTERPRETATION",
            (
                "PCA separa casos y controles, pero también coincide con batch. Interpreta.",
                "PCA separates cases and controls but also matches batch. Interpret it.",
                "PCA adskiller cases og kontroller, men matcher også batch. Fortolk.",
            ),
            (("Outcome y batch están confundidos.", "Outcome and batch are confounded.", "Outcome og batch er confounded."),),
            (
                "La separación no puede atribuirse al estado biológico porque batch y outcome explican la misma dirección. Se requiere rediseño, balance, covariables o datos donde ambos factores puedan separarse.",
                "The separation cannot be attributed to biological state because batch and outcome explain the same direction. Redesign, balancing, covariates, or data where the factors can be separated are needed.",
                "Adskillelsen kan ikke tilskrives biologisk tilstand, fordi batch og outcome forklarer samme retning. Redesign, balancering, kovariater eller data, hvor faktorerne kan adskilles, er nødvendige.",
            ),
            (
                "Una corrección matemática no recupera información ausente por confusión perfecta.",
                "A mathematical correction cannot recover information lost to perfect confounding.",
                "En matematisk korrektion kan ikke genskabe information tabt ved perfekt confounding.",
            ),
            "",
        ),
        (
            "m10.p04",
            "FILL_IN_THE_BLANK",
            (
                "La validación con selección interna de hiperparámetros y evaluación externa se llama ________ CV.",
                "Validation with inner hyperparameter selection and outer evaluation is called ________ CV.",
                "Validering med intern hyperparameterselektion og ekstern evaluering kaldes ________ CV.",
            ),
            (("Usa dos niveles.", "It uses two levels.", "Den bruger to niveauer."),),
            ("nested", "nested", "nested"),
            (
                "El fold externo estima generalización sin participar en selección.",
                "The outer fold estimates generalization without participating in selection.",
                "Det ydre fold estimerer generalisering uden at deltage i selektion.",
            ),
            "",
        ),
        (
            "m10.p05",
            "PIPELINE_DESIGN",
            (
                "Diseña evaluación para un clasificador con 10 % de casos positivos.",
                "Design evaluation for a classifier with 10% positive cases.",
                "Design evaluering af en klassifikator med 10 % positive cases.",
            ),
            (("Accuracy es insuficiente.", "Accuracy is insufficient.", "Accuracy er utilstrækkelig."),),
            (
                "Usar splits estratificados y agrupados; comparar baseline de prevalencia; reportar AUPRC, sensibilidad, especificidad, precision, calibración y matriz de confusión; elegir umbral según coste; incluir intervalos y análisis por subgrupos.",
                "Use stratified grouped splits; compare a prevalence baseline; report AUPRC, sensitivity, specificity, precision, calibration, and confusion matrix; choose threshold by cost; include intervals and subgroup analysis.",
                "Brug stratificerede grouped splits; sammenlign en prævalensbaseline; rapportér AUPRC, sensitivitet, specificitet, precision, kalibrering og confusion matrix; vælg tærskel efter omkostning; medtag intervaller og subgruppeanalyse.",
            ),
            (
                "AUROC sola puede ocultar rendimiento positivo pobre.",
                "AUROC alone may hide poor positive-class performance.",
                "AUROC alene kan skjule dårlig præstation for den positive klasse.",
            ),
            "",
        ),
        (
            "m10.p06",
            "DEBUGGING",
            (
                "Un modelo logra 98 % en CV y 55 % en test externo. Diagnostica.",
                "A model achieves 98% in CV and 55% on external test. Diagnose it.",
                "En model opnår 98 % i CV og 55 % på ekstern test. Diagnosticér.",
            ),
            (("Busca fuga y shift.", "Look for leakage and shift.", "Søg efter leakage og shift."),),
            (
                "Auditar duplicados/sujetos compartidos, preprocesamiento antes de CV, selección de features, tuning repetido, batch y población; comparar distribuciones, baselines y rendimiento por sitio; reconstruir pipeline anidado y agrupado.",
                "Audit duplicates/shared subjects, preprocessing before CV, feature selection, repeated tuning, batch, and population; compare distributions, baselines, and site-level performance; rebuild a nested grouped pipeline.",
                "Auditér dubletter/delte subjekter, preprocessing før CV, feature-selektion, gentaget tuning, batch og population; sammenlign fordelinger, baselines og site-specifik præstation; genopbyg en nested grouped pipeline.",
            ),
            (
                "La discrepancia puede combinar optimismo interno y distribution shift.",
                "The discrepancy may combine internal optimism and distribution shift.",
                "Uoverensstemmelsen kan kombinere intern optimisme og distribution shift.",
            ),
            "",
        ),
        (
            "m10.p07",
            "ORAL_EXPLANATION",
            (
                "Explica por qué importancia de features no implica causalidad.",
                "Explain why feature importance does not imply causality.",
                "Forklar hvorfor feature-importance ikke indebærer kausalitet.",
            ),
            (("Considera correlación y sustitución.", "Consider correlation and substitution.", "Overvej korrelation og substitution."),),
            (
                "La importancia resume contribución predictiva bajo un modelo y distribución. Features correlacionadas pueden sustituirse, el modelo puede explotar confusores y la dirección causal no se identifica sin diseño e intervención.",
                "Importance summarizes predictive contribution under a model and distribution. Correlated features may substitute for each other, the model may exploit confounders, and causal direction is not identified without design and intervention.",
                "Importance opsummerer prædiktivt bidrag under en model og fordeling. Korrelerede features kan erstatte hinanden, modellen kan udnytte confoundere, og kausal retning identificeres ikke uden design og intervention.",
            ),
            (
                "Debe evaluarse estabilidad entre folds y métodos.",
                "Stability should be evaluated across folds and methods.",
                "Stabilitet bør evalueres mellem folds og metoder.",
            ),
            "",
        ),
        (
            "m10.p08",
            "PIPELINE_DESIGN",
            (
                "Diseña la estructura de un proyecto final reproducible.",
                "Design the structure of a reproducible final project.",
                "Design strukturen for et reproducerbart afsluttende projekt.",
            ),
            (("Incluye decisión, datos, validación y defensa.", "Include decision, data, validation, and defense.", "Medtag beslutning, data, validering og forsvar."),),
            (
                "Pregunta y alcance; fuentes/permisos/versiones; diccionario y auditoría; hipótesis y baseline; pipeline reproducible; plan de validación; resultados con incertidumbre; análisis de errores; limitaciones; README, entorno, tests y figuras; guion oral con decisiones y alternativas.",
                "Question and scope; sources/permissions/versions; dictionary and audit; hypothesis and baseline; reproducible pipeline; validation plan; results with uncertainty; error analysis; limitations; README, environment, tests, and figures; oral script explaining decisions and alternatives.",
                "Spørgsmål og scope; kilder/tilladelser/versioner; ordbog og audit; hypotese og baseline; reproducerbar pipeline; valideringsplan; resultater med usikkerhed; fejlanalyse; begrænsninger; README, miljø, tests og figurer; mundtligt manuskript med beslutninger og alternativer.",
            ),
            (
                "La calidad se evalúa por trazabilidad y razonamiento, no sólo por una métrica alta.",
                "Quality is evaluated through traceability and reasoning, not only a high metric.",
                "Kvalitet evalueres gennem sporbarhed og ræsonnement, ikke kun en høj metrik.",
            ),
            "",
        ),
    ),
    mcqs=(
        (
            "001",
            ("¿Cuál debe ser la unidad de split?", "What should be the splitting unit?", "Hvad bør split-enheden være?"),
            (
                ("independent", ("Unidad experimental independiente", "Independent experimental unit", "Uafhængig eksperimentel enhed")),
                ("row", ("Cada fila siempre", "Every row always", "Altid hver række")),
                ("feature", ("Cada feature", "Each feature", "Hver feature")),
            ),
            "independent",
            ("Réplicas del mismo sujeto deben permanecer juntas.", "Replicates from one subject should remain together.", "Replikater fra samme subjekt bør forblive sammen."),
        ),
        (
            "002",
            ("¿Dónde se ajusta un escalador?", "Where is a scaler fitted?", "Hvor tilpasses en scaler?"),
            (
                ("train", ("Sólo entrenamiento", "Training only", "Kun træning")),
                ("all", ("Todo el dataset", "Entire dataset", "Hele datasættet")),
                ("test", ("Sólo test", "Test only", "Kun test")),
            ),
            "train",
            ("Usar validación o test filtra información.", "Using validation or test leaks information.", "Brug af validering eller test lækker information."),
        ),
        (
            "003",
            ("¿Qué maximiza PCA?", "What does PCA maximize?", "Hvad maksimerer PCA?"),
            (
                ("variance", ("Varianza proyectada", "Projected variance", "Projiceret varians")),
                ("labels", ("Separación de labels", "Label separation", "Label-adskillelse")),
                ("accuracy", ("Accuracy", "Accuracy", "Accuracy")),
            ),
            "variance",
            ("PCA no utiliza outcomes.", "PCA does not use outcomes.", "PCA bruger ikke outcomes."),
        ),
        (
            "004",
            ("¿Qué riesgo tiene un cluster visual?", "What risk does a visual cluster have?", "Hvilken risiko har et visuelt cluster?"),
            (
                ("batch", ("Puede reflejar batch o parámetros", "It may reflect batch or parameters", "Det kan afspejle batch eller parametre")),
                ("proof", ("Prueba clase verdadera", "It proves a true class", "Det beviser en sand klasse")),
                ("causal", ("Demuestra causalidad", "It proves causality", "Det beviser kausalitet")),
            ),
            "batch",
            ("La estructura no supervisada requiere estabilidad y contexto.", "Unsupervised structure requires stability and context.", "Usuperviseret struktur kræver stabilitet og kontekst."),
        ),
        (
            "005",
            ("¿Qué hace nested CV?", "What does nested CV do?", "Hvad gør nested CV?"),
            (
                ("separate", ("Separa selección y estimación", "Separates selection and estimation", "Adskiller selektion og estimering")),
                ("duplicate", ("Duplica test", "Duplicates test", "Duplikerer test")),
                ("remove", ("Elimina hiperparámetros", "Removes hyperparameters", "Fjerner hyperparametre")),
            ),
            "separate",
            ("Los folds internos seleccionan y los externos evalúan.", "Inner folds select and outer folds evaluate.", "Indre folds selekterer, og ydre folds evaluerer."),
        ),
        (
            "006",
            ("¿Qué métrica es informativa con positivos raros?", "Which metric is informative with rare positives?", "Hvilken metrik er informativ ved sjældne positive?"),
            (
                ("auprc", ("AUPRC", "AUPRC", "AUPRC")),
                ("accuracy", ("Sólo accuracy", "Accuracy only", "Kun accuracy")),
                ("mse", ("MSE de labels", "Label MSE", "Label-MSE")),
            ),
            "auprc",
            ("Relaciona precision y recall para la clase positiva.", "It relates precision and recall for the positive class.", "Den relaterer precision og recall for den positive klasse."),
        ),
        (
            "007",
            ("¿Qué evalúa calibración?", "What does calibration evaluate?", "Hvad evaluerer kalibrering?"),
            (
                ("probabilities", ("Correspondencia entre probabilidades y frecuencias", "Agreement between probabilities and frequencies", "Overensstemmelse mellem sandsynligheder og frekvenser")),
                ("ranking", ("Sólo ranking", "Ranking only", "Kun ranking")),
                ("speed", ("Velocidad", "Speed", "Hastighed")),
            ),
            "probabilities",
            ("Predicciones de 0.8 deberían ocurrir cerca del 80 % bajo calibración.", "Predictions of 0.8 should occur about 80% under calibration.", "Prædiktioner på 0,8 bør forekomme omkring 80 % ved kalibrering."),
        ),
        (
            "008",
            ("¿Qué causa selección de features antes de CV?", "What does feature selection before CV cause?", "Hvad forårsager feature-selektion før CV?"),
            (
                ("leakage", ("Fuga de información", "Information leakage", "Informationsleakage")),
                ("fairness", ("Equidad automática", "Automatic fairness", "Automatisk fairness")),
                ("compression", ("Compresión sin sesgo", "Unbiased compression", "Uskæv komprimering")),
            ),
            "leakage",
            ("La selección usa outcomes de folds futuros.", "Selection uses outcomes from future folds.", "Selektionen bruger outcomes fra fremtidige folds."),
        ),
        (
            "009",
            ("¿Qué significa una feature importante?", "What does an important feature mean?", "Hvad betyder en vigtig feature?"),
            (
                ("predictive", ("Contribución predictiva bajo el modelo", "Predictive contribution under the model", "Prædiktivt bidrag under modellen")),
                ("causal", ("Causa demostrada", "Proven cause", "Bevist årsag")),
                ("stable", ("Siempre estable", "Always stable", "Altid stabil")),
            ),
            "predictive",
            ("No identifica dirección causal.", "It does not identify causal direction.", "Den identificerer ikke kausal retning."),
        ),
        (
            "010",
            ("¿Cuándo se usa el test final?", "When is the final test used?", "Hvornår bruges det endelige test?"),
            (
                ("once", ("Una vez con pipeline congelado", "Once with a frozen pipeline", "Én gang med fastlåst pipeline")),
                ("tuning", ("Durante cada decisión", "During every decision", "Under hver beslutning")),
                ("preprocess", ("Para ajustar escalado", "To fit scaling", "Til at tilpasse skalering")),
            ),
            "once",
            ("Reutilizar test produce optimismo adaptativo.", "Reusing test produces adaptive optimism.", "Genbrug af test giver adaptiv optimisme."),
        ),
    ),
    true_false=(
        ("011", ("Cada aliquot de un paciente es una unidad independiente.", "Every aliquot from a patient is an independent unit.", "Hver aliquot fra en patient er en uafhængig enhed."), False, ("Comparten el mismo sujeto y fuentes de variación.", "They share the same subject and variation sources.", "De deler samme subjekt og variationskilder.")),
        ("012", ("El preprocesamiento aprendido forma parte del modelo.", "Learned preprocessing is part of the model.", "Lært preprocessing er en del af modellen."), True, ("Sus parámetros deben ajustarse dentro de train.", "Its parameters should be fitted inside training.", "Dets parametre bør tilpasses i træning.")),
        ("013", ("PCA usa labels para maximizar separación.", "PCA uses labels to maximize separation.", "PCA bruger labels til at maksimere adskillelse."), False, ("Maximiza varianza sin supervisión.", "It maximizes variance without supervision.", "Den maksimerer varians uden supervision.")),
        ("014", ("Clusters pueden depender de escala y distancia.", "Clusters may depend on scale and distance.", "Clusters kan afhænge af skala og afstand."), True, ("Son decisiones del análisis.", "They are analysis decisions.", "Det er analysebeslutninger.")),
        ("015", ("El fold externo puede usarse para elegir hiperparámetros.", "The outer fold may be used to choose hyperparameters.", "Det ydre fold kan bruges til at vælge hyperparametre."), False, ("Debe reservarse para estimación.", "It should be reserved for estimation.", "Det bør reserveres til estimering.")),
        ("016", ("Accuracy alta puede coexistir con recall positivo cero.", "High accuracy can coexist with zero positive recall.", "Høj accuracy kan sameksistere med nul positiv recall."), True, ("Ocurre en clases muy desbalanceadas.", "This occurs with highly imbalanced classes.", "Det forekommer ved stærkt ubalancerede klasser.")),
        ("017", ("AUROC y calibración miden lo mismo.", "AUROC and calibration measure the same thing.", "AUROC og kalibrering måler det samme."), False, ("Una evalúa ranking y la otra probabilidades.", "One evaluates ranking and the other probabilities.", "Den ene evaluerer ranking og den anden sandsynligheder.")),
        ("018", ("Feature importance demuestra causalidad.", "Feature importance proves causality.", "Feature-importance beviser kausalitet."), False, ("Es asociación predictiva dependiente del modelo.", "It is model-dependent predictive association.", "Det er modelafhængig prædiktiv association.")),
        ("019", ("Un resultado negativo puede formar un proyecto riguroso.", "A negative result can form a rigorous project.", "Et negativt resultat kan danne et stringent projekt."), True, ("Diseño, auditoría y límites también son resultados científicos.", "Design, audit, and limitations are scientific outputs too.", "Design, audit og begrænsninger er også videnskabelige outputs.")),
        ("020", ("Un modelo didáctico validado por CV es automáticamente clínico.", "A teaching model validated by CV is automatically clinical.", "En undervisningsmodel valideret med CV er automatisk klinisk."), False, ("La implementación clínica exige validación, gobernanza y contexto adicionales.", "Clinical implementation requires additional validation, governance, and context.", "Klinisk implementering kræver yderligere validering, governance og kontekst.")),
    ),
    tutor=(
        (
            "El aprendizaje con datos ómicos comienza identificando la unidad experimental, la orientación de la matriz, outcomes, grupos, batches y dependencias. Todo preprocesamiento que aprende parámetros —filtrado, imputación, escalado, corrección o selección— debe ajustarse dentro de entrenamiento. PCA, clustering y embeddings describen estructura sensible a escala y batch, no clases verdaderas automáticas. El modelado supervisado requiere métricas definidas, splits agrupados y nested CV para separar selección de estimación. Desbalance, calibración, baselines, intervalos y análisis de errores complementan una métrica puntual. Importancia de features es predictiva, puede ser inestable y no demuestra causalidad. Un proyecto final sólido conserva datos, versiones, código, entorno, decisiones, validación y limitaciones, y su defensa explica alternativas y amenazas a validez.",
            "Learning from OMICS data begins by identifying the experimental unit, matrix orientation, outcomes, groups, batches, and dependencies. Any preprocessing that learns parameters—filtering, imputation, scaling, correction, or selection—must be fitted within training data. PCA, clustering, and embeddings describe structure sensitive to scale and batch, not automatic true classes. Supervised modeling requires predefined metrics, grouped splits, and nested CV to separate selection from estimation. Imbalance, calibration, baselines, intervals, and error analysis complement a point metric. Feature importance is predictive, may be unstable, and does not prove causality. A strong final project preserves data, versions, code, environment, decisions, validation, and limitations, and its defense explains alternatives and threats to validity.",
            "Læring fra OMICS-data begynder med at identificere den eksperimentelle enhed, matrixorientering, outcomes, grupper, batches og afhængigheder. Al preprocessing, der lærer parametre—filtrering, imputering, skalering, korrektion eller selektion—skal tilpasses inden for træningsdata. PCA, clustering og embeddings beskriver struktur, der er følsom over for skala og batch, ikke automatisk sande klasser. Superviseret modellering kræver prædefinerede metrikker, grouped splits og nested CV for at adskille selektion fra estimering. Ubalance, kalibrering, baselines, intervaller og fejlanalyse supplerer en punktmetrik. Feature-importance er prædiktiv, kan være ustabil og beviser ikke kausalitet. Et stærkt afsluttende projekt bevarer data, versioner, kode, miljø, beslutninger, validering og begrænsninger, og forsvaret forklarer alternativer og trusler mod validitet.",
        ),
        (
            ("La unidad experimental define independencia.", "The experimental unit defines independence.", "Den eksperimentelle enhed definerer uafhængighed."),
            ("Preprocesamiento aprendido pertenece al pipeline.", "Learned preprocessing belongs to the pipeline.", "Lært preprocessing tilhører pipelinen."),
            ("PCA y clustering son descriptivos.", "PCA and clustering are descriptive.", "PCA og clustering er deskriptive."),
            ("Nested CV separa selección y estimación.", "Nested CV separates selection and estimation.", "Nested CV adskiller selektion og estimering."),
            ("Métricas dependen de prevalencia y decisión.", "Metrics depend on prevalence and decision.", "Metrikker afhænger af prævalens og beslutning."),
            ("Reproducibilidad incluye decisiones y entorno.", "Reproducibility includes decisions and environment.", "Reproducerbarhed omfatter beslutninger og miljø."),
        ),
        (
            ("Dividir filas en vez de sujetos.", "Splitting rows instead of subjects.", "At opdele rækker i stedet for subjekter."),
            ("Escalar antes de CV.", "Scaling before CV.", "At skalere før CV."),
            ("Interpretar PCA como prueba de clase.", "Interpreting PCA as proof of class.", "At fortolke PCA som bevis for klasse."),
            ("Ajustar hiperparámetros en folds externos.", "Tuning hyperparameters on outer folds.", "At tune hyperparametre på ydre folds."),
            ("Reportar sólo accuracy o AUROC.", "Reporting only accuracy or AUROC.", "At rapportere kun accuracy eller AUROC."),
            ("Interpretar importancia como causalidad.", "Interpreting importance as causality.", "At fortolke importance som kausalitet."),
        ),
        (
            ("¿Cuál es la unidad independiente?", "What is the independent unit?", "Hvad er den uafhængige enhed?"),
            ("¿Qué pasos aprenden parámetros?", "Which steps learn parameters?", "Hvilke trin lærer parametre?"),
            ("¿Outcome y batch están confundidos?", "Are outcome and batch confounded?", "Er outcome og batch confounded?"),
            ("¿Quién selecciona hiperparámetros?", "Which data select hyperparameters?", "Hvilke data vælger hyperparametre?"),
            ("¿Qué métrica corresponde a la decisión?", "Which metric matches the decision?", "Hvilken metrik passer til beslutningen?"),
            ("¿Puede otra persona ejecutar el proyecto?", "Can another person execute the project?", "Kan en anden person køre projektet?"),
        ),
        (
            ("Define datos y unidades correctamente.", "Defines data and units correctly.", "Definerer data og enheder korrekt."),
            ("Evita fuga en preprocessing.", "Avoids preprocessing leakage.", "Undgår leakage i preprocessing."),
            ("Interpreta análisis no supervisado con cautela.", "Interprets unsupervised analysis cautiously.", "Fortolker usuperviseret analyse forsigtigt."),
            ("Diseña validación agrupada y anidada.", "Designs grouped and nested validation.", "Designer grouped og nested validering."),
            ("Reporta métricas, incertidumbre y errores.", "Reports metrics, uncertainty, and errors.", "Rapporterer metrikker, usikkerhed og fejl."),
            ("Entrega y defiende un proyecto reproducible.", "Delivers and defends a reproducible project.", "Leverer og forsvarer et reproducerbart projekt."),
        ),
        (
            ("No inventar rendimiento o biomarcadores.", "Do not invent performance or biomarkers.", "Opfind ikke præstation eller biomarkører."),
            ("No usar test para decisiones repetidas.", "Do not use test data for repeated decisions.", "Brug ikke testdata til gentagne beslutninger."),
            ("No presentar asociaciones predictivas como mecanismos.", "Do not present predictive associations as mechanisms.", "Præsenter ikke prædiktive associationer som mekanismer."),
            ("No convertir ejercicios en modelos clínicos.", "Do not turn exercises into clinical models.", "Omsæt ikke øvelser til kliniske modeller."),
            ("Responder en el idioma activo.", "Answer in the active language.", "Svar på det aktive sprog."),
        ),
        (
            "High-dimensional OMICS data-analysis principles.",
            "PCA, clustering, and dimensionality-reduction foundations.",
            "Grouped and nested cross-validation methodology.",
            "Calibration, class imbalance, and precision-recall evaluation.",
            "Feature-selection leakage and model-interpretation literature.",
            "Active SDU DM847 supervised and unsupervised OMICS learning outcomes.",
        ),
    ),
)

LOCALIZED_MODULE_10_OMICS_LEARNING_PROJECT: LocalizedLearningModule = build_module(_SPEC)
LOCALIZED_OBJECTIVE_QUESTION_BANK_10 = build_question_bank(_SPEC)


def materialize_module_10_question_bank(
    locale: AppLocale | str = AppLocale.SPANISH_SPAIN,
) -> tuple[AssessmentItem, ...]:
    return materialize_bank(LOCALIZED_OBJECTIVE_QUESTION_BANK_10, locale)


MODULE_10_OMICS_LEARNING_PROJECT: LearningModule = LOCALIZED_MODULE_10_OMICS_LEARNING_PROJECT.materialize(
    AppLocale.SPANISH_SPAIN
)
OBJECTIVE_QUESTION_BANK_10 = materialize_module_10_question_bank()

__all__ = [
    "LOCALIZED_MODULE_10_OMICS_LEARNING_PROJECT",
    "LOCALIZED_OBJECTIVE_QUESTION_BANK_10",
    "MODULE_10_OMICS_LEARNING_PROJECT",
    "OBJECTIVE_QUESTION_BANK_10",
    "materialize_module_10_question_bank",
]
