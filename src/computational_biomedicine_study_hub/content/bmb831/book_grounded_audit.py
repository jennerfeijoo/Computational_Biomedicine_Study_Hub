"""Source-grounded BMB831 audit and focused M01-M03 review.

The active public SDU course description defines the curricular boundary. Public
methodological references are used to verify analytical depth and terminology;
they do not reconstruct private Itslearning material, attendance, or grading.
Visible teaching material is original trilingual paraphrase and adaptation.
"""

from __future__ import annotations

from dataclasses import dataclass, replace
from typing import Literal

from ...learning.activity_types import ActivityType
from ..localized_models import LocalizedLearningModule, LocalizedTutorSupportPacket
from .authoring import concept, example, objective, objective_mcq, practice

VerificationState = Literal["pending", "consistent", "improve", "correct", "outside_scope"]


@dataclass(frozen=True, slots=True)
class AcademicReference:
    """One stable public source used by the BMB831 audit."""

    source_id: str
    citation: str
    relevant_scope: str


@dataclass(frozen=True, slots=True)
class ModuleSourceAudit:
    """Source mapping and focused verification state for one module."""

    module_id: str
    source_ids: tuple[str, ...]
    source_scope: tuple[str, ...]
    state: VerificationState
    finding: str
    implemented_change: str = ""


BMB831_BOOK_SOURCES: tuple[AcademicReference, ...] = (
    AcademicReference(
        "sdu-bmb831-active-2025",
        "SDU, BMB831: Biostatistics in R II, approved active course description (2025).",
        (
            "advanced R scripting, large biological data, multivariate analysis, advanced "
            "visualisation, biological interpretation, protein characterisation, standard omics "
            "workflows, publication appraisal, and an individual English report"
        ),
    ),
    AcademicReference(
        "synthea-official-csv-export",
        "Synthea official documentation, CSV exporter and synthetic patient-data boundary.",
        (
            "relational synthetic patient tables, patient foreign keys, reproducible generation, "
            "and the boundary between simulated records and observed clinical evidence"
        ),
    ),
    AcademicReference(
        "bioconductor-summarizedexperiment",
        (
            "Bioconductor, SummarizedExperiment: coordinating matrix-like assays, samples, "
            "features, and experiment metadata. DOI 10.18129/B9.bioc.SummarizedExperiment."
        ),
        (
            "feature-by-sample assays, colData, rowData or rowRanges, coordinated subsetting, "
            "object validity, and scalable matrix-like backends"
        ),
    ),
    AcademicReference(
        "bioconductor-edger-normalization",
        "Bioconductor edgeR User's Guide and methodological documentation.",
        (
            "count filtering, library composition, TMM-style normalisation factors, effective "
            "library sizes, negative-binomial dispersion, and differential-expression workflows"
        ),
    ),
    AcademicReference(
        "bioconductor-deseq2",
        (
            "Love, Huber, and Anders, Moderated estimation of fold change and dispersion for "
            "RNA-seq data with DESeq2, Genome Biology 15, 550 (2014), and package vignette."
        ),
        (
            "median-ratio size factors, dispersion estimation and shrinkage, negative-binomial "
            "models, contrasts, independent filtering, and fold-change shrinkage boundaries"
        ),
    ),
    AcademicReference(
        "limma-empirical-bayes",
        (
            "Ritchie et al., limma powers differential expression analyses for RNA-sequencing "
            "and microarray studies, Nucleic Acids Research 43:e47 (2015)."
        ),
        (
            "design matrices, contrasts, precision weights, empirical-Bayes variance moderation, "
            "moderated statistics, and complex experimental designs"
        ),
    ),
    AcademicReference(
        "islr-2021-unsupervised-multiple-testing",
        (
            "James, Witten, Hastie, and Tibshirani, An Introduction to Statistical Learning with "
            "Applications in R, 2nd ed. (2021), chapters 12 and 13."
        ),
        (
            "principal components, clustering, preprocessing sensitivity, multiple testing, "
            "family-wise error, false discovery rate, and resampling-based assessment"
        ),
    ),
    AcademicReference(
        "ims-2024-visualisation-reporting",
        (
            "Çetinkaya-Rundel and Hardin, Introduction to Modern Statistics, 2nd ed. (2024), "
            "exploratory communication, modelling, inference, and reproducible R labs."
        ),
        (
            "clear statistical graphics, uncertainty, accessibility, reproducible reporting, "
            "model interpretation, and critical communication of limitations"
        ),
    ),
    AcademicReference(
        "bioconductor-public-omics-workflows",
        (
            "Bioconductor workflow and package documentation for public transcriptomics and "
            "proteomics analyses, including airway, limma, and experiment containers."
        ),
        (
            "versioned public datasets, immutable snapshots, assay-specific preprocessing, "
            "workflow provenance, checksums, and reproducible computational environments"
        ),
    ),
    AcademicReference(
        "protein-public-resources",
        (
            "UniProt, InterPro, Protein Data Bank, and AlphaFold Protein Structure Database "
            "public documentation and provenance records."
        ),
        (
            "sequence records, domains, experimental structures, model coverage, confidence, "
            "versioning, and evidence boundaries for computational protein characterisation"
        ),
    ),
    AcademicReference(
        "functional-interpretation-resources",
        (
            "Gene Ontology and Reactome public documentation for enrichment, annotation, "
            "pathways, evidence, and versioned biological interpretation."
        ),
        (
            "identifier mapping, tested universe, over-representation, pathway databases, "
            "network interpretation, redundancy, circularity, and evidence provenance"
        ),
    ),
)


BMB831_MODULE_SOURCE_AUDIT: tuple[ModuleSourceAudit, ...] = (
    ModuleSourceAudit(
        "bmb831.m01",
        ("sdu-bmb831-active-2025", "synthea-official-csv-export"),
        (
            "advanced reproducible R workflows and large relational data",
            "primary and foreign keys, grain, cardinality, and patient-level independence",
            "synthetic-data provenance and separation from real clinical or omics evidence",
        ),
        "consistent",
        (
            "The module already treats Synthea as a bounded workflow example, preserves patient-"
            "level dependence, validates relational contracts, and explicitly rejects treating "
            "synthetic records as clinical or omics evidence."
        ),
        "Added stable source-basis traceability without expanding Synthea's curricular role.",
    ),
    ModuleSourceAudit(
        "bmb831.m02",
        (
            "sdu-bmb831-active-2025",
            "bioconductor-summarizedexperiment",
            "bioconductor-edger-normalization",
            "bioconductor-deseq2",
        ),
        (
            "assay, feature, and sample-metadata coordination",
            "quality control, filtering, transformation, and normalisation",
            "library composition and robust between-sample size factors",
        ),
        "consistent",
        (
            "Existing matrix, metadata, quality-control, filtering, transformation, scaling, and "
            "provenance coverage is consistent. It needed one explicit demonstration that total-"
            "count scaling can create apparent changes under strong composition imbalance."
        ),
        (
            "Added a trilingual composition-bias explanation, deterministic median-ratio example, "
            "pipeline-design exercise, and stable objective assessment item."
        ),
    ),
    ModuleSourceAudit(
        "bmb831.m03",
        (
            "sdu-bmb831-active-2025",
            "bioconductor-edger-normalization",
            "bioconductor-deseq2",
            "limma-empirical-bayes",
            "islr-2021-unsupervised-multiple-testing",
        ),
        (
            "design matrices, contrasts, count and Gaussian models",
            "feature-wise nuisance-parameter estimation and empirical-Bayes moderation",
            "effect sizes, uncertainty, multiplicity, and false-discovery interpretation",
        ),
        "consistent",
        (
            "Existing design, model-scale, effect, uncertainty, and FDR coverage is consistent. "
            "The module needed an explicit separation of variance or dispersion moderation, effect-"
            "size shrinkage, and multiple-testing adjustment."
        ),
        (
            "Added a trilingual information-sharing explanation, deterministic moderated-variance "
            "example, interpretation exercise, and stable objective assessment item."
        ),
    ),
    ModuleSourceAudit(
        "bmb831.m04",
        (
            "sdu-bmb831-active-2025",
            "islr-2021-unsupervised-multiple-testing",
            "bioconductor-summarizedexperiment",
        ),
        (
            "PCA scores, loadings, explained variance, and preprocessing",
            "distance, hierarchical and partitioning clustering, and stability",
            "batch structure, leakage, and biological validation",
        ),
        "pending",
        "Source scope is mapped; focused comparison remains pending.",
    ),
    ModuleSourceAudit(
        "bmb831.m05",
        ("sdu-bmb831-active-2025", "ims-2024-visualisation-reporting"),
        (
            "question-driven graphics and analytical units",
            "MA, volcano, heatmap, uncertainty, and multiplicity-aware display",
            "accessibility, reproducible export, and visual integrity",
        ),
        "pending",
        "Source scope is mapped; focused comparison remains pending.",
    ),
    ModuleSourceAudit(
        "bmb831.m06",
        (
            "sdu-bmb831-active-2025",
            "bioconductor-public-omics-workflows",
            "bioconductor-summarizedexperiment",
            "bioconductor-deseq2",
            "limma-empirical-bayes",
        ),
        (
            "standard transcriptomics and proteomics workflows",
            "versioned public data, checksums, immutable snapshots, and dataset cards",
            "assay-specific preprocessing, modelling, and reproducible execution",
        ),
        "pending",
        "Source scope is mapped; focused comparison remains pending.",
    ),
    ModuleSourceAudit(
        "bmb831.m07",
        ("sdu-bmb831-active-2025", "protein-public-resources"),
        (
            "sequence-derived protein properties and domain evidence",
            "UniProt and InterPro provenance",
            "PDB experimental coverage and AlphaFold confidence boundaries",
        ),
        "pending",
        "Source scope is mapped; focused comparison remains pending.",
    ),
    ModuleSourceAudit(
        "bmb831.m08",
        (
            "sdu-bmb831-active-2025",
            "functional-interpretation-resources",
            "islr-2021-unsupervised-multiple-testing",
        ),
        (
            "identifier mapping and tested-universe definition",
            "enrichment, pathway, and network interpretation",
            "redundancy, circularity, multiplicity, and annotation provenance",
        ),
        "pending",
        "Source scope is mapped; focused comparison remains pending.",
    ),
    ModuleSourceAudit(
        "bmb831.m09",
        ("sdu-bmb831-active-2025", "ims-2024-visualisation-reporting"),
        (
            "objective appraisal of published data-analysis methods",
            "estimand, design, validity, reproducibility, and evidence boundaries",
            "individual English scientific reporting without private-rubric reconstruction",
        ),
        "pending",
        "Source scope is mapped; focused comparison remains pending.",
    ),
)


def _source_ids(module_id: str) -> tuple[str, ...]:
    return next(
        item.source_ids for item in BMB831_MODULE_SOURCE_AUDIT if item.module_id == module_id
    )


def _with_source_basis(module: LocalizedLearningModule) -> LocalizedLearningModule:
    tutor = module.tutor_support
    merged = tuple(dict.fromkeys((*tutor.source_basis, *_source_ids(module.module_id))))
    updated_tutor: LocalizedTutorSupportPacket = replace(tutor, source_basis=merged)
    return replace(module, tutor_support=updated_tutor)


def _extend_omics_normalisation(module: LocalizedLearningModule) -> LocalizedLearningModule:
    extended = replace(
        module,
        objectives=module.objectives
        + (
            objective(
                "m02.bg.o1",
                (
                    "Diagnosticar sesgo composicional y distinguir tamaño de biblioteca de un factor de normalización robusto.",
                    "Diagnose composition bias and distinguish library size from a robust normalisation factor.",
                    "Diagnosticere kompositionsbias og skelne biblioteksstørrelse fra en robust normaliseringsfaktor.",
                ),
            ),
        ),
        concepts=module.concepts
        + (
            concept(
                "composition-bias-and-size-factors",
                (
                    "Sesgo composicional y factores de tamaño",
                    "Composition bias and size factors",
                    "Kompositionsbias og størrelsesfaktorer",
                ),
                (
                    "El total de conteos de una muestra no siempre representa sólo profundidad técnica. Si unas pocas características aumentan de forma extrema, ocupan una fracción mayor de la biblioteca y hacen que características estables parezcan disminuir al dividir por el total. Los métodos robustos estiman factores relativos usando muchas características y una referencia implícita, con supuestos como que la mayoría no cambia fuertemente o que los cambios están aproximadamente equilibrados. Un factor de normalización no crea abundancias absolutas ni corrige un diseño confundido. Deben inspeccionarse los factores, las distribuciones y la plausibilidad de sus supuestos; ante cambios globales reales pueden requerirse controles externos, spike-ins o una estrategia específica del experimento.",
                    "A sample's total count does not always represent technical depth alone. If a few features increase extremely, they occupy a larger library fraction and make stable features appear to decrease after total-count scaling. Robust methods estimate relative factors from many features and an implicit reference, relying on assumptions such as most features not changing strongly or changes being approximately balanced. A normalisation factor does not create absolute abundance or repair a confounded design. Inspect factors, distributions, and assumption plausibility; genuine global shifts may require external controls, spike-ins, or an experiment-specific strategy.",
                    "En prøves totale count repræsenterer ikke altid kun teknisk dybde. Hvis få features stiger ekstremt, optager de en større del af biblioteket og får stabile features til at se reducerede ud efter skalering med totalen. Robuste metoder estimerer relative faktorer fra mange features og en implicit reference under antagelser som, at de fleste features ikke ændres kraftigt, eller at ændringerne omtrent er balancerede. En normaliseringsfaktor skaber ikke absolut abundans og reparerer ikke et confounded design. Faktorer, fordelinger og antagelser skal inspiceres; reelle globale skift kan kræve eksterne kontroller, spike-ins eller en experimentspecifik strategi.",
                ),
                (
                    (
                        "Biblioteksstørrelse y factor de normalización no son sinónimos.",
                        "Library size and normalisation factor are not synonyms.",
                        "Biblioteksstørrelse og normaliseringsfaktor er ikke synonymer.",
                    ),
                    (
                        "Una característica dominante puede inducir cambios aparentes en las demás.",
                        "A dominant feature can induce apparent changes in the others.",
                        "En dominerende feature kan fremkalde tilsyneladende ændringer i de øvrige.",
                    ),
                    (
                        "Los factores robustos dependen de supuestos sobre la mayoría de características.",
                        "Robust factors depend on assumptions about the majority of features.",
                        "Robuste faktorer afhænger af antagelser om flertallet af features.",
                    ),
                    (
                        "Cambios globales reales requieren controles o una estrategia justificada.",
                        "Genuine global shifts require controls or a justified strategy.",
                        "Reelle globale skift kræver kontroller eller en begrundet strategi.",
                    ),
                ),
            ),
        ),
        worked_examples=module.worked_examples
        + (
            example(
                "m02.bg.e01",
                (
                    "Contrastar total de biblioteca y razón mediana",
                    "Contrast total-library and median-ratio scaling",
                    "Sammenlign totalbibliotek- og median-ratio-skalering",
                ),
                (
                    "Muestra cómo una única característica dominante distorsiona la normalización por total mientras una razón mediana conserva las características estables bajo sus supuestos.",
                    "Show how one dominant feature distorts total-count scaling while a median ratio preserves stable features under its assumptions.",
                    "Vis hvordan én dominerende feature forvrænger total-count-skalering, mens en median-ratio bevarer stabile features under sine antagelser.",
                ),
                (
                    (
                        "Dos características permanecen estables entre condiciones.",
                        "Two features remain stable across conditions.",
                        "To features forbliver stabile mellem betingelser.",
                    ),
                    (
                        "La tercera aumenta diez veces en las muestras tratadas.",
                        "The third increases ten-fold in treated samples.",
                        "Den tredje stiger ti gange i de behandlede prøver.",
                    ),
                    (
                        "Los factores se centran geométricamente para poder compararlos.",
                        "Factors are geometrically centred for comparison.",
                        "Faktorerne geometrisk centreres for sammenligning.",
                    ),
                ),
                """counts <- matrix(
  c(100, 120, 100, 120,
    100, 120, 100, 120,
    100, 120, 1000, 1200),
  nrow = 3,
  byrow = TRUE,
  dimnames = list(paste0("G", 1:3), paste0("S", 1:4))
)
library_sizes <- colSums(counts)
library_factors <- library_sizes / exp(mean(log(library_sizes)))
geometric_means <- exp(rowMeans(log(counts)))
ratios <- sweep(counts, 1, geometric_means, "/")
median_factors <- apply(ratios, 2, median)
median_factors <- median_factors / exp(mean(log(median_factors)))
normalized_total <- counts["G1", ] / library_factors
normalized_median <- counts["G1", ] / median_factors
cat("library_factors=", paste(sprintf("%.3f", library_factors), collapse = ","), "\n", sep = "")
cat("median_factors=", paste(sprintf("%.3f", median_factors), collapse = ","), "\n", sep = "")
cat("G1_total=", paste(sprintf("%.3f", normalized_total), collapse = ","), "\n", sep = "")
cat("G1_median=", paste(sprintf("%.3f", normalized_median), collapse = ","), sep = "")
""",
                """library_factors=0.456,0.548,1.826,2.191
median_factors=0.913,1.095,0.913,1.095
G1_total=219.089,219.089,54.772,54.772
G1_median=109.545,109.545,109.545,109.545""",
                (
                    "La normalización por total hace que G1 parezca cuatro veces menor en tratamiento porque G3 domina la biblioteca. La razón mediana conserva G1 bajo el supuesto de que la mayoría de características es estable; el ejemplo no demuestra que ese supuesto sea válido en todo experimento.",
                    "Total-count scaling makes G1 appear four-fold lower in treatment because G3 dominates the library. The median ratio preserves G1 under the assumption that most features are stable; the example does not prove that assumption for every experiment.",
                    "Total-count-skalering får G1 til at se fire gange lavere ud i behandling, fordi G3 dominerer biblioteket. Median-ratioen bevarer G1 under antagelsen om, at de fleste features er stabile; eksemplet beviser ikke denne antagelse for alle eksperimenter.",
                ),
            ),
        ),
        practice_exercises=module.practice_exercises
        + (
            practice(
                "m02.bg.p01",
                ActivityType.PIPELINE_DESIGN,
                (
                    "Un experimento induce una respuesta global esperada en casi todos los transcritos. Diseña una estrategia de normalización y explica por qué un factor estimado sólo desde la mayoría de genes puede borrar parte de la señal.",
                    "An experiment is expected to induce a global response in almost all transcripts. Design a normalisation strategy and explain why a factor estimated only from the majority of genes could remove part of the signal.",
                    "Et eksperiment forventes at fremkalde et globalt respons i næsten alle transkripter. Design en normaliseringsstrategi og forklar, hvorfor en faktor estimeret kun fra flertallet af gener kan fjerne en del af signalet.",
                ),
                (
                    (
                        "Distingue cambio técnico de cambio global biológico.",
                        "Distinguish technical change from a global biological shift.",
                        "Skeln teknisk ændring fra et globalt biologisk skift.",
                    ),
                    (
                        "Considera controles externos o spike-ins definidos antes del análisis.",
                        "Consider external controls or spike-ins defined before analysis.",
                        "Overvej eksterne kontroller eller spike-ins defineret før analysen.",
                    ),
                ),
                (
                    "Usaría controles externos o spike-ins técnicamente comparables, evaluaría sus supuestos y realizaría análisis de sensibilidad frente a estrategias alternativas. Una normalización que fuerza estable a la mayoría puede interpretar el desplazamiento biológico global como profundidad y eliminarlo.",
                    "Use technically comparable external controls or spike-ins, assess their assumptions, and perform sensitivity analyses across alternative strategies. A normalisation that forces the majority to be stable may interpret the global biological shift as depth and remove it.",
                    "Brug teknisk sammenlignelige eksterne kontroller eller spike-ins, vurder deres antagelser, og udfør følsomhedsanalyser med alternative strategier. En normalisering, der tvinger flertallet til at være stabilt, kan fortolke det globale biologiske skift som dybde og fjerne det.",
                ),
                (
                    "Una respuesta completa declara la referencia de escala, los controles, los supuestos y una comprobación de sensibilidad.",
                    "A complete answer states the scale reference, controls, assumptions, and a sensitivity check.",
                    "Et fuldstændigt svar angiver skalareference, kontroller, antagelser og en følsomhedskontrol.",
                ),
                "",
            ),
        ),
        assessment_items=module.assessment_items
        + (
            objective_mcq(
                "bmb831.m02.book.001",
                (
                    "¿Por qué el total de conteos puede ser un factor de escala engañoso?",
                    "Why can total count be a misleading scale factor?",
                    "Hvorfor kan det totale count være en misvisende skalafaktor?",
                ),
                (
                    (
                        "dominant_features",
                        (
                            "Porque pocas características dominantes pueden alterar la composición de la biblioteca.",
                            "Because a few dominant features can alter library composition.",
                            "Fordi få dominerende features kan ændre bibliotekets sammensætning.",
                        ),
                    ),
                    (
                        "sample_names",
                        (
                            "Porque los nombres de muestra siempre cambian la profundidad.",
                            "Because sample names always change sequencing depth.",
                            "Fordi prøvenavne altid ændrer sekventeringsdybden.",
                        ),
                    ),
                    (
                        "pca_rotation",
                        (
                            "Porque PCA rota automáticamente todos los conteos.",
                            "Because PCA automatically rotates all counts.",
                            "Fordi PCA automatisk roterer alle counts.",
                        ),
                    ),
                ),
                "dominant_features",
                (
                    "El total mezcla profundidad con composición; una señal muy abundante puede cambiar la fracción relativa de todas las demás.",
                    "The total mixes depth with composition; a highly abundant signal can change every other feature's relative fraction.",
                    "Totalen blander dybde med sammensætning; et meget abundant signal kan ændre den relative andel af alle øvrige features.",
                ),
            ),
        ),
    )
    return _with_source_basis(extended)


def _extend_differential_moderation(module: LocalizedLearningModule) -> LocalizedLearningModule:
    extended = replace(
        module,
        objectives=module.objectives
        + (
            objective(
                "m03.bg.o1",
                (
                    "Distinguir moderación de varianza o dispersión, shrinkage del efecto y control de FDR en análisis de alta dimensión.",
                    "Distinguish variance or dispersion moderation, effect shrinkage, and FDR control in high-dimensional analysis.",
                    "Skelne mellem moderering af varians eller dispersion, effekt-shrinkage og FDR-kontrol i højdimensionel analyse.",
                ),
            ),
        ),
        concepts=module.concepts
        + (
            concept(
                "information-sharing-across-features",
                (
                    "Préstamo de información entre características",
                    "Information sharing across features",
                    "Informationsdeling på tværs af features",
                ),
                (
                    "En experimentos ómicos suele ajustarse un modelo por gen o proteína con pocas muestras. Las estimaciones individuales de varianza o dispersión pueden ser muy inestables, aunque existan miles de características que informan sobre su distribución global. Los procedimientos empírico-bayesianos combinan la estimación específica de cada característica con una tendencia o distribución estimada del conjunto para moderar parámetros de ruido y estabilizar estadísticos. Esto no supone que los efectos biológicos sean idénticos ni convierte las características en réplicas independientes. La moderación de varianza o dispersión es distinta del shrinkage del log-fold change y ambas son distintas del ajuste por multiplicidad: la primera estabiliza ruido, la segunda regulariza magnitud y la tercera controla una familia de decisiones. El diseño, el contraste y los diagnósticos siguen siendo necesarios.",
                    "Omics experiments commonly fit one model per gene or protein with few samples. Feature-specific variance or dispersion estimates can be unstable even though thousands of features inform their global distribution. Empirical-Bayes procedures combine each feature's estimate with a trend or distribution estimated across features to moderate noise parameters and stabilise statistics. This does not assume identical biological effects or turn features into independent replicates. Variance or dispersion moderation differs from log-fold-change shrinkage, and both differ from multiplicity adjustment: the first stabilises noise, the second regularises magnitude, and the third controls a family of decisions. Design, contrast, and diagnostics remain necessary.",
                    "I omikeksperimenter tilpasses ofte én model pr. gen eller protein med få prøver. Feature-specifikke estimater af varians eller dispersion kan være ustabile, selv om tusindvis af features informerer deres globale fordeling. Empirisk-bayesianske procedurer kombinerer hver features estimat med en trend eller fordeling estimeret på tværs af features for at moderere støjparametre og stabilisere statistikker. Det antager ikke identiske biologiske effekter og gør ikke features til uafhængige replikater. Moderering af varians eller dispersion adskiller sig fra shrinkage af log-fold change, og begge adskiller sig fra multiplicitetstilpasning: den første stabiliserer støj, den anden regulariserer størrelse, og den tredje kontrollerer en familie af beslutninger. Design, kontrast og diagnostik er fortsat nødvendige.",
                ),
                (
                    (
                        "La información compartida estabiliza parámetros de ruido, no el diseño experimental.",
                        "Shared information stabilises noise parameters, not experimental design.",
                        "Delt information stabiliserer støjparametre, ikke forsøgsdesign.",
                    ),
                    (
                        "Moderación, shrinkage del efecto y FDR resuelven problemas diferentes.",
                        "Moderation, effect shrinkage, and FDR solve different problems.",
                        "Moderering, effekt-shrinkage og FDR løser forskellige problemer.",
                    ),
                    (
                        "Un prior estimado no corrige confusión ni pseudorreplicación.",
                        "An estimated prior does not repair confounding or pseudoreplication.",
                        "En estimeret prior reparerer ikke confounding eller pseudoreplikation.",
                    ),
                    (
                        "Deben revisarse tendencias, outliers y sensibilidad del procedimiento.",
                        "Trends, outliers, and procedural sensitivity must be reviewed.",
                        "Trends, outliers og procedurens følsomhed skal gennemgås.",
                    ),
                ),
            ),
        ),
        worked_examples=module.worked_examples
        + (
            example(
                "m03.bg.e01",
                (
                    "Moderar varianzas con un prior común",
                    "Moderate variances with a common prior",
                    "Moderér varianser med en fælles prior",
                ),
                (
                    "Aplica una actualización empírico-bayesiana didáctica para mostrar cómo las varianzas extremas se acercan a una referencia sin cambiar los efectos estimados.",
                    "Apply a didactic empirical-Bayes update to show how extreme variances move toward a reference without changing estimated effects.",
                    "Anvend en didaktisk empirisk-bayesiansk opdatering for at vise, hvordan ekstreme varianser bevæger sig mod en reference uden at ændre estimerede effekter.",
                ),
                (
                    (
                        "Cada característica tiene cuatro grados de libertad residuales.",
                        "Each feature has four residual degrees of freedom.",
                        "Hver feature har fire residuale frihedsgrader.",
                    ),
                    (
                        "El prior tiene varianza uno y seis grados de libertad.",
                        "The prior has variance one and six degrees of freedom.",
                        "Prioren har varians én og seks frihedsgrader.",
                    ),
                    (
                        "Los efectos permanecen iguales; sólo cambia el denominador del estadístico.",
                        "Effects remain unchanged; only the statistic's denominator changes.",
                        "Effekterne forbliver uændrede; kun statistikkens nævner ændres.",
                    ),
                ),
                """effects <- c(1, 1, 1)
raw_variance <- c(0.25, 1.00, 4.00)
residual_df <- 4
prior_variance <- 1
prior_df <- 6
contrast_variance <- 0.5
moderated_variance <- (prior_df * prior_variance + residual_df * raw_variance) /
  (prior_df + residual_df)
raw_t <- effects / sqrt(raw_variance * contrast_variance)
moderated_t <- effects / sqrt(moderated_variance * contrast_variance)
cat("raw_variance=", paste(sprintf("%.2f", raw_variance), collapse = ","), "\n", sep = "")
cat("moderated_variance=", paste(sprintf("%.2f", moderated_variance), collapse = ","), "\n", sep = "")
cat("raw_t=", paste(sprintf("%.2f", raw_t), collapse = ","), "\n", sep = "")
cat("moderated_t=", paste(sprintf("%.2f", moderated_t), collapse = ","), sep = "")
""",
                """raw_variance=0.25,1.00,4.00
moderated_variance=0.70,1.00,2.20
raw_t=2.83,1.41,0.71
moderated_t=1.69,1.41,0.95""",
                (
                    "La varianza muy pequeña aumenta y la muy grande disminuye hacia la referencia; el efecto sigue siendo uno en las tres características. Es una ilustración algebraica, no una reproducción completa de limma, edgeR o DESeq2.",
                    "The very small variance increases and the very large variance decreases toward the reference; the effect remains one for all three features. This is an algebraic illustration, not a complete reproduction of limma, edgeR, or DESeq2.",
                    "Den meget lille varians stiger, og den meget store varians falder mod referencen; effekten forbliver én for alle tre features. Dette er en algebraisk illustration, ikke en fuld reproduktion af limma, edgeR eller DESeq2.",
                ),
            ),
        ),
        practice_exercises=module.practice_exercises
        + (
            practice(
                "m03.bg.p01",
                ActivityType.DATA_INTERPRETATION,
                (
                    "Un pipeline devuelve log2 fold changes crudos, log2 fold changes con shrinkage, estadísticos moderados y valores p ajustados. Explica qué pregunta responde cada columna y cuál usarías para ranking, magnitud e inferencia.",
                    "A pipeline returns raw log2 fold changes, shrunken log2 fold changes, moderated statistics, and adjusted p-values. Explain the question answered by each column and which you would use for ranking, magnitude, and inference.",
                    "En pipeline returnerer rå log2 fold changes, shrinkede log2 fold changes, modererede statistikker og justerede p-værdier. Forklar hvilket spørgsmål hver kolonne besvarer, og hvad du ville bruge til ranking, størrelse og inferens.",
                ),
                (
                    (
                        "Separa estimación del efecto, estabilización del ruido y multiplicidad.",
                        "Separate effect estimation, noise stabilisation, and multiplicity.",
                        "Adskil effektestimering, støjstabilisering og multiplicitet.",
                    ),
                    (
                        "Declara que el uso exacto depende del método y del objetivo.",
                        "State that exact use depends on method and purpose.",
                        "Angiv at den præcise anvendelse afhænger af metode og formål.",
                    ),
                ),
                (
                    "El efecto crudo representa la estimación sin regularización; el efecto con shrinkage estabiliza magnitudes, especialmente con poca información; el estadístico moderado combina efecto y ruido estabilizado para ordenar evidencia bajo el modelo; el valor p ajustado se usa para decisiones dentro de la familia de hipótesis. Ninguna columna sustituye el diseño, los intervalos, la abundancia basal o la validación.",
                    "The raw effect is the unregularised estimate; the shrunken effect stabilises magnitudes, especially with little information; the moderated statistic combines effect and stabilised noise to rank evidence under the model; the adjusted p-value supports decisions within the hypothesis family. No column replaces design, intervals, baseline abundance, or validation.",
                    "Den rå effekt er det uregulariserede estimat; den shrinkede effekt stabiliserer størrelser, især ved begrænset information; den modererede statistik kombinerer effekt og stabiliseret støj til ranking af evidens under modellen; den justerede p-værdi understøtter beslutninger inden for hypotese-familien. Ingen kolonne erstatter design, intervaller, basisabundans eller validering.",
                ),
                (
                    "Una respuesta completa distingue claramente los tres procedimientos y evita interpretar FDR como probabilidad posterior por gen.",
                    "A complete answer clearly distinguishes the three procedures and avoids interpreting FDR as a per-gene posterior probability.",
                    "Et fuldstændigt svar skelner tydeligt mellem de tre procedurer og undgår at fortolke FDR som en posterior sandsynlighed pr. gen.",
                ),
                "",
            ),
        ),
        assessment_items=module.assessment_items
        + (
            objective_mcq(
                "bmb831.m03.book.001",
                (
                    "¿Qué describe mejor la moderación empírico-bayesiana de varianzas?",
                    "What best describes empirical-Bayes variance moderation?",
                    "Hvad beskriver bedst empirisk-bayesiansk moderering af varianser?",
                ),
                (
                    (
                        "noise_parameters",
                        (
                            "Combina información específica y global para estabilizar parámetros de ruido.",
                            "It combines feature-specific and global information to stabilise noise parameters.",
                            "Den kombinerer feature-specifik og global information for at stabilisere støjparametre.",
                        ),
                    ),
                    (
                        "identical_effects",
                        (
                            "Obliga a que todos los efectos biológicos sean idénticos.",
                            "It forces all biological effects to be identical.",
                            "Den tvinger alle biologiske effekter til at være identiske.",
                        ),
                    ),
                    (
                        "remove_fdr",
                        (
                            "Elimina la necesidad de ajustar por multiplicidad.",
                            "It removes the need for multiplicity adjustment.",
                            "Den fjerner behovet for multiplicitetstilpasning.",
                        ),
                    ),
                ),
                "noise_parameters",
                (
                    "La moderación estabiliza estimaciones de variación; no iguala efectos ni reemplaza el control de FDR.",
                    "Moderation stabilises variation estimates; it neither equalises effects nor replaces FDR control.",
                    "Moderering stabiliserer variationsestimater; den udligner hverken effekter eller erstatter FDR-kontrol.",
                ),
            ),
        ),
    )
    return _with_source_basis(extended)


def apply_book_grounded_extensions(
    modules: tuple[LocalizedLearningModule, ...],
) -> tuple[LocalizedLearningModule, ...]:
    """Attach source traceability and apply completed M02-M03 extensions."""

    updated: list[LocalizedLearningModule] = []
    for module in modules:
        if module.module_id == "bmb831.m02":
            updated.append(_extend_omics_normalisation(module))
        elif module.module_id == "bmb831.m03":
            updated.append(_extend_differential_moderation(module))
        else:
            updated.append(_with_source_basis(module))
    return tuple(updated)


__all__ = [
    "AcademicReference",
    "BMB831_BOOK_SOURCES",
    "BMB831_MODULE_SOURCE_AUDIT",
    "ModuleSourceAudit",
    "VerificationState",
    "apply_book_grounded_extensions",
]
