"""BMB831 module 2: omics matrices, quality control, and normalization."""

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
    module_id="bmb831.m02",
    title=_t(
        "Matrices ómicas, control de calidad y normalización",
        "Omics matrices, quality control, and normalization",
        "Omikmatricer, kvalitetskontrol og normalisering",
    ),
    summary=_t(
        "Estructura matrices de abundancia con metadatos alineados, identifica problemas de calidad, filtra características informativamente y elige transformaciones compatibles con la escala y la pregunta biológica.",
        "Structure abundance matrices with aligned metadata, identify quality problems, filter features informatively, and choose transformations compatible with the measurement scale and biological question.",
        "Strukturér abundansmatricer med afstemte metadata, identificér kvalitetsproblemer, filtrér features informativt, og vælg transformationer, der passer til måleskalaen og det biologiske spørgsmål.",
    ),
    objectives=(
        (
            "m02.o1",
            _t(
                "Declarar el contrato de una matriz ómica y comprobar la alineación entre muestras, características y metadatos.",
                "Declare an omics-matrix contract and verify alignment among samples, features, and metadata.",
                "Deklarere en kontrakt for en omikmatrix og kontrollere afstemning mellem prøver, features og metadata.",
            ),
        ),
        (
            "m02.o2",
            _t(
                "Auditar profundidad, missingness, distribución y posibles muestras atípicas sin eliminar observaciones automáticamente.",
                "Audit depth, missingness, distributions, and possible outlier samples without automatically deleting observations.",
                "Auditere dybde, missingness, fordelinger og mulige outlier-prøver uden automatisk at slette observationer.",
            ),
        ),
        (
            "m02.o3",
            _t(
                "Distinguir filtrado, normalización, transformación y escalado, y justificar el orden del pipeline.",
                "Distinguish filtering, normalization, transformation, and scaling, and justify pipeline order.",
                "Skelne mellem filtrering, normalisering, transformation og skalering samt begrunde rækkefølgen i pipelinen.",
            ),
        ),
        (
            "m02.o4",
            _t(
                "Construir un flujo reproducible para datos de alto rendimiento con artefactos, parámetros y controles explícitos.",
                "Build a reproducible high-throughput-data workflow with explicit artifacts, parameters, and checks.",
                "Bygge et reproducerbart workflow til high-throughput-data med eksplicitte artefakter, parametre og kontroller.",
            ),
        ),
    ),
    concepts=(
        (
            "assay-contract",
            _t(
                "Contrato de matriz y metadatos",
                "Assay-matrix and metadata contract",
                "Kontrakt for assay-matrix og metadata",
            ),
            _t(
                "Una matriz ómica suele representar características en filas y muestras en columnas. Los identificadores de columnas deben coincidir de forma exacta y única con los identificadores de las filas del metadata. Las anotaciones de características se mantienen en una tabla separada y alineada con las filas. Cambiar silenciosamente el orden de muestras puede asociar abundancias con grupos incorrectos y producir un análisis numéricamente válido pero científicamente falso.",
                "An omics matrix commonly represents features in rows and samples in columns. Column identifiers must match the metadata row identifiers exactly and uniquely. Feature annotations remain in a separate table aligned to matrix rows. Silently changing sample order can associate abundances with the wrong groups and produce a numerically valid but scientifically false analysis.",
                "En omikmatrix repræsenterer ofte features i rækker og prøver i kolonner. Kolonneidentifikatorer skal matche metadata-rækkeidentifikatorer præcist og entydigt. Feature-annoteringer opbevares i en separat tabel afstemt med matrixrækkerne. En skjult ændring af prøveordenen kan forbinde abundanser med forkerte grupper og give en numerisk gyldig, men videnskabeligt falsk analyse.",
            ),
            (
                _t(
                    "Comprueba unicidad, conjunto y orden de los identificadores.",
                    "Check identifier uniqueness, set equality, and order.",
                    "Kontrollér identifikatorers unikhed, mængdelighed og rækkefølge.",
                ),
                _t(
                    "La unidad independiente suele ser la muestra biológica, no cada característica.",
                    "The independent unit is usually the biological sample, not each feature.",
                    "Den uafhængige enhed er normalt den biologiske prøve, ikke hver feature.",
                ),
            ),
        ),
        (
            "quality-audit",
            _t(
                "Control de calidad multicapas",
                "Multilayer quality control",
                "Kvalitetskontrol i flere lag",
            ),
            _t(
                "El control de calidad combina métricas técnicas y visuales: profundidad total, porcentaje de ceros o valores faltantes, distribución por muestra, similitud entre perfiles, relación con lotes y coherencia con variables biológicas conocidas. Una muestra extrema es una señal para investigar metadatos, procesamiento y trazabilidad; no es una autorización automática para excluirla.",
                "Quality control combines technical and visual metrics: total depth, proportion of zeros or missing values, sample distributions, profile similarity, association with batches, and consistency with known biological variables. An extreme sample is a signal to investigate metadata, processing, and provenance; it is not automatic authorization to exclude it.",
                "Kvalitetskontrol kombinerer tekniske og visuelle mål: total dybde, andel af nuller eller manglende værdier, prøvefordelinger, profilligelighed, relation til batches og konsistens med kendte biologiske variable. En ekstrem prøve er et signal om at undersøge metadata, behandling og proveniens; den er ikke en automatisk tilladelse til at ekskludere prøven.",
            ),
            (
                _t(
                    "Documenta el motivo y la sensibilidad de cualquier exclusión.",
                    "Document the reason and sensitivity of every exclusion.",
                    "Dokumentér årsag og følsomhed for enhver eksklusion.",
                ),
                _t(
                    "Revisa si el patrón atípico coincide con un lote o error de anotación.",
                    "Check whether an outlying pattern aligns with a batch or annotation error.",
                    "Kontrollér om et afvigende mønster følger et batch eller en annoteringsfejl.",
                ),
            ),
        ),
        (
            "pipeline-operations",
            _t(
                "Filtrado, normalización, transformación y escalado",
                "Filtering, normalization, transformation, and scaling",
                "Filtrering, normalisering, transformation og skalering",
            ),
            _t(
                "El filtrado elimina características sin información suficiente según una regla declarada. La normalización corrige factores técnicos comparables entre muestras. La transformación modifica la relación entre media y varianza o aproxima una escala útil para visualización. El escalado centra o estandariza variables para métodos sensibles a magnitud. Estas operaciones no son intercambiables y deben ajustarse al modelo posterior.",
                "Filtering removes features with insufficient information according to a declared rule. Normalization adjusts comparable technical factors among samples. Transformation changes the mean-variance relation or approaches a scale useful for visualization. Scaling centers or standardizes variables for magnitude-sensitive methods. These operations are not interchangeable and must fit the downstream model.",
                "Filtrering fjerner features med utilstrækkelig information efter en deklareret regel. Normalisering justerer sammenlignelige tekniske faktorer mellem prøver. Transformation ændrer middelværdi-varians-relationen eller skaber en skala, der er nyttig til visualisering. Skalering centrerer eller standardiserer variable til metoder, der er følsomme over for størrelse. Operationerne er ikke udskiftelige og skal passe til den efterfølgende model.",
            ),
            (
                _t(
                    "No uses datos futuros o etiquetas de outcome para decidir filtros no supervisados.",
                    "Do not use future data or outcome labels to decide unsupervised filters.",
                    "Brug ikke fremtidige data eller outcome-labels til at vælge usuperviserede filtre.",
                ),
                _t(
                    "Los conteos crudos se conservan para modelos que los requieren.",
                    "Raw counts are retained for models that require them.",
                    "Rå counts bevares til modeller, der kræver dem.",
                ),
            ),
        ),
        (
            "large-data-workflow",
            _t(
                "Flujo reproducible para grandes matrices",
                "Reproducible workflow for large matrices",
                "Reproducerbart workflow til store matricer",
            ),
            _t(
                "Un pipeline escalable separa datos fuente, objetos intermedios y resultados. Registra dimensiones, tipos, checksums, parámetros de filtrado y versiones de software. Lee sólo columnas o assays necesarios, reduce temprano cuando la regla es científicamente predefinida y evita copias completas innecesarias. El rendimiento se mide antes de optimizar y nunca reemplaza la validación científica.",
                "A scalable pipeline separates source data, intermediate objects, and results. It records dimensions, types, checksums, filtering parameters, and software versions. It reads only required columns or assays, reduces early when the rule is scientifically predefined, and avoids unnecessary full copies. Performance is measured before optimization and never replaces scientific validation.",
                "En skalerbar pipeline adskiller kildedata, mellemobjekter og resultater. Den registrerer dimensioner, typer, checksums, filtreringsparametre og softwareversioner. Den læser kun nødvendige kolonner eller assays, reducerer tidligt når reglen er videnskabeligt foruddefineret, og undgår unødvendige fulde kopier. Ydeevne måles før optimering og erstatter aldrig videnskabelig validering.",
            ),
            (
                _t(
                    "Cada artefacto derivado debe poder relacionarse con entradas y parámetros.",
                    "Every derived artifact should be traceable to inputs and parameters.",
                    "Hvert afledt artefakt bør kunne spores til input og parametre.",
                ),
                _t(
                    "Una matriz pequeña de prueba valida la lógica antes de escalar.",
                    "A small test matrix validates logic before scaling.",
                    "En lille testmatrix validerer logikken før skalering.",
                ),
            ),
        ),
    ),
    examples=(
        (
            "m02.e01",
            _t(
                "Validar y filtrar una matriz de conteos",
                "Validate and filter a count matrix",
                "Validér og filtrér en count-matrix",
            ),
            _t(
                "Comprueba identificadores y aplica una regla de abundancia mínima antes de crear artefactos derivados.",
                "Check identifiers and apply a minimum-abundance rule before creating derived artifacts.",
                "Kontrollér identifikatorer og anvend en minimumsabundansregel før afledte artefakter oprettes.",
            ),
            (
                _t(
                    "Las columnas de counts deben coincidir con metadata$sample_id.",
                    "The count columns must match metadata$sample_id.",
                    "Count-kolonnerne skal matche metadata$sample_id.",
                ),
                _t(
                    "La regla conserva genes con al menos diez conteos en dos muestras.",
                    "The rule retains genes with at least ten counts in two samples.",
                    "Reglen bevarer gener med mindst ti counts i to prøver.",
                ),
                _t(
                    "Se registran profundidad y características retenidas.",
                    "Depth and retained features are recorded.",
                    "Dybde og bevarede features registreres.",
                ),
            ),
            """counts <- matrix(
  c(10, 20, 40, 80,
    0, 0, 1, 2,
    50, 50, 100, 100,
    5, 10, 5, 10),
  nrow = 4,
  byrow = TRUE,
  dimnames = list(paste0("G", 1:4), paste0("S", 1:4))
)
metadata <- data.frame(
  sample_id = paste0("S", 1:4),
  group = c("control", "control", "treated", "treated")
)
stopifnot(identical(colnames(counts), metadata$sample_id))
keep <- rowSums(counts >= 10) >= 2
cat("kept=", paste(rownames(counts)[keep], collapse = ","), "\n", sep = "")
cat("library_sizes=", paste(colSums(counts), collapse = ","), sep = "")
""",
            """kept=G1,G3,G4
library_sizes=65,80,146,192""",
            _t(
                "La característica G2 queda fuera por baja información. La regla se declara antes de modelar y los conteos crudos permanecen intactos.",
                "Feature G2 is removed for low information. The rule is declared before modeling, and raw counts remain intact.",
                "Feature G2 fjernes på grund af lav information. Reglen deklareres før modellering, og rå counts forbliver intakte.",
            ),
        ),
        (
            "m02.e02",
            _t(
                "Investigar una muestra con perfil extremo",
                "Investigate a sample with an extreme profile",
                "Undersøg en prøve med en ekstrem profil",
            ),
            _t(
                "Resume la desviación de cada muestra respecto al perfil mediano sin convertir el resultado en una exclusión automática.",
                "Summarize each sample's deviation from the median profile without turning the result into an automatic exclusion.",
                "Opsummér hver prøves afvigelse fra medianprofilen uden at gøre resultatet til en automatisk eksklusion.",
            ),
            (
                _t(
                    "Se calcula un perfil mediano por característica.",
                    "A median profile is calculated per feature.",
                    "En medianprofil beregnes pr. feature.",
                ),
                _t(
                    "La desviación media absoluta sirve como señal diagnóstica.",
                    "Mean absolute deviation serves as a diagnostic signal.",
                    "Middel absolut afvigelse fungerer som et diagnostisk signal.",
                ),
                _t(
                    "La decisión final requiere revisar metadata y procesamiento.",
                    "The final decision requires metadata and processing review.",
                    "Den endelige beslutning kræver gennemgang af metadata og behandling.",
                ),
            ),
            """log_abundance <- matrix(
  c(1.0, 1.2, 0.8, 5.0,
    2.0, 2.1, 1.9, 6.0,
    3.0, 3.1, 2.9, 7.0),
  nrow = 3,
  byrow = TRUE,
  dimnames = list(paste0("F", 1:3), paste0("S", 1:4))
)
feature_medians <- apply(log_abundance, 1, median)
deviation <- colMeans(abs(log_abundance - feature_medians))
cat("largest_profile_deviation=", names(which.max(deviation)), sep = "")
""",
            "largest_profile_deviation=S4",
            _t(
                "S4 merece investigación porque su perfil se aparta del centro. El resultado por sí solo no prueba contaminación ni justifica eliminar la muestra.",
                "S4 warrants investigation because its profile departs from the center. The result alone does not prove contamination or justify removing the sample.",
                "S4 bør undersøges, fordi profilen afviger fra centrum. Resultatet alene beviser ikke kontaminering og retfærdiggør ikke at fjerne prøven.",
            ),
        ),
    ),
    practices=(
        (
            "m02.p01",
            "OPEN_RESPONSE",
            _t(
                "Escribe un contrato mínimo para una matriz de RNA-seq: unidad de filas, unidad de columnas, claves, metadata y artefactos fuente.",
                "Write a minimum contract for an RNA-seq matrix: row unit, column unit, keys, metadata, and source artifacts.",
                "Skriv en minimumskontrakt for en RNA-seq-matrix: rækkeenhed, kolonneenhed, nøgler, metadata og kildeartefakter.",
            ),
            (
                _t(
                    "Empieza por qué representa una celda.",
                    "Start with what one cell represents.",
                    "Start med hvad én celle repræsenterer.",
                ),
                _t(
                    "Incluye el vínculo exacto con metadata.",
                    "Include the exact metadata link.",
                    "Medtag den præcise forbindelse til metadata.",
                ),
            ),
            _t(
                "Una celda representa el conteo o abundancia de una característica en una muestra; filas y columnas tienen IDs únicos; colnames(counts) coincide exactamente con metadata$sample_id; la anotación de características está alineada con rownames(counts); los archivos fuente son inmutables y versionados.",
                "A cell represents the count or abundance of one feature in one sample; rows and columns have unique IDs; colnames(counts) exactly matches metadata$sample_id; feature annotation aligns with rownames(counts); source files are immutable and versioned.",
                "En celle repræsenterer count eller abundans af én feature i én prøve; rækker og kolonner har unikke ID'er; colnames(counts) matcher præcist metadata$sample_id; feature-annotering følger rownames(counts); kildefiler er uforanderlige og versionerede.",
            ),
            _t(
                "El contrato evita desalineación y hace explícita la unidad analítica.",
                "The contract prevents misalignment and makes the analytical unit explicit.",
                "Kontrakten forhindrer fejlafstemning og gør den analytiske enhed eksplicit.",
            ),
            "",
        ),
        (
            "m02.p02",
            "CODE_READING",
            _t(
                "Explica por qué metadata <- metadata[match(colnames(counts), metadata$sample_id), ] requiere comprobar también valores NA y duplicados.",
                "Explain why metadata <- metadata[match(colnames(counts), metadata$sample_id), ] also requires checking NA values and duplicates.",
                "Forklar hvorfor metadata <- metadata[match(colnames(counts), metadata$sample_id), ] også kræver kontrol af NA-værdier og dubletter.",
            ),
            (
                _t("match puede devolver NA.", "match can return NA.", "match kan returnere NA."),
                _t(
                    "Un ID duplicado no define una fila única.",
                    "A duplicated ID does not define a unique row.",
                    "Et duplikeret ID definerer ikke en entydig række.",
                ),
            ),
            _t(
                "La reordenación sólo es segura cuando todos los IDs de columnas aparecen exactamente una vez en metadata. Deben verificarse unicidad, ausencia de NA y equivalencia de conjuntos antes de aceptar el orden.",
                "Reordering is safe only when every column ID appears exactly once in metadata. Uniqueness, absence of NA, and set equality must be verified before accepting the order.",
                "Omordning er kun sikker, når hvert kolonne-ID findes præcis én gang i metadata. Unikhed, fravær af NA og lighed mellem mængder skal kontrolleres før rækkefølgen accepteres.",
            ),
            _t(
                "Reordenar no repara metadatos incompletos ni ambiguos.",
                "Reordering does not repair incomplete or ambiguous metadata.",
                "Omordning reparerer ikke ufuldstændige eller tvetydige metadata.",
            ),
            "",
        ),
        (
            "m02.p03",
            "OPEN_RESPONSE",
            _t(
                "Distingue qué pregunta responde cada operación: filtrado por baja abundancia, normalización por tamaño de biblioteca, log-transformación y z-score por característica.",
                "Distinguish the question answered by each operation: low-abundance filtering, library-size normalization, log transformation, and feature-wise z-scoring.",
                "Skeln mellem spørgsmålet for hver operation: filtrering af lav abundans, normalisering efter biblioteksstørrelse, log-transformation og featurevis z-score.",
            ),
            (
                _t("No son sinónimos.", "They are not synonyms.", "De er ikke synonymer."),
                _t(
                    "Relaciona cada paso con el método posterior.",
                    "Relate each step to the downstream method.",
                    "Knyt hvert trin til den efterfølgende metode.",
                ),
            ),
            _t(
                "El filtrado retira características poco informativas; la normalización ajusta exposición técnica entre muestras; el log reduce asimetría y dependencia media-varianza para exploración; el z-score iguala escala entre características para métodos de distancia, pero elimina magnitudes absolutas.",
                "Filtering removes poorly informative features; normalization adjusts technical exposure among samples; log transformation reduces skew and mean-variance dependence for exploration; z-scoring equalizes feature scale for distance methods but removes absolute magnitudes.",
                "Filtrering fjerner features med lav information; normalisering justerer teknisk eksponering mellem prøver; log-transformation reducerer skævhed og middelværdi-varians-afhængighed til udforskning; z-score udligner feature-skala til afstandsmetoder, men fjerner absolutte størrelser.",
            ),
            _t(
                "La operación correcta depende de la escala y del estimando.",
                "The correct operation depends on the scale and estimand.",
                "Den korrekte operation afhænger af skala og estimand.",
            ),
            "",
        ),
        (
            "m02.p04",
            "ERROR_RECONSTRUCTION",
            _t(
                "Un analista elimina S7 porque aparece separada en PCA y luego informa grupos más claros. Reconstruye el error y propone un análisis de sensibilidad.",
                "An analyst removes S7 because it separates in PCA and then reports clearer groups. Reconstruct the error and propose a sensitivity analysis.",
                "En analytiker fjerner S7, fordi den ligger separat i PCA, og rapporterer derefter tydeligere grupper. Rekonstruér fejlen og foreslå en følsomhedsanalyse.",
            ),
            (
                _t(
                    "PCA no diagnostica por sí sola la causa.",
                    "PCA alone does not diagnose the cause.",
                    "PCA diagnosticerer ikke alene årsagen.",
                ),
                _t(
                    "Compara resultados con y sin S7.",
                    "Compare results with and without S7.",
                    "Sammenlign resultater med og uden S7.",
                ),
            ),
            _t(
                "La exclusión se decidió para mejorar el patrón, lo que introduce selección post hoc. Deben revisarse métricas técnicas, metadata, lote, identidad y procesamiento; justificar cualquier exclusión con criterios independientes; y presentar resultados con y sin S7.",
                "The exclusion was chosen to improve the pattern, creating post-hoc selection. Technical metrics, metadata, batch, identity, and processing should be reviewed; any exclusion requires independent criteria; and results with and without S7 should be reported.",
                "Eksklusionen blev valgt for at forbedre mønsteret og skaber post-hoc-selektion. Tekniske mål, metadata, batch, identitet og behandling bør gennemgås; enhver eksklusion kræver uafhængige kriterier; og resultater med og uden S7 bør rapporteres.",
            ),
            _t(
                "Una visualización es evidencia diagnóstica, no una regla automática de limpieza.",
                "A visualization is diagnostic evidence, not an automatic cleaning rule.",
                "En visualisering er diagnostisk evidens, ikke en automatisk oprydningsregel.",
            ),
            "",
        ),
        (
            "m02.p05",
            "STARTER_CODE",
            _t(
                "Completa una función base R que compruebe que los IDs de muestras de una matriz y metadata son únicos y coinciden en orden.",
                "Complete a base-R function that checks whether matrix and metadata sample IDs are unique and match in order.",
                "Færdiggør en base-R-funktion, der kontrollerer om prøve-ID'er i matrix og metadata er unikke og matcher i rækkefølge.",
            ),
            (
                _t(
                    "Usa anyDuplicated e identical.",
                    "Use anyDuplicated and identical.",
                    "Brug anyDuplicated og identical.",
                ),
                _t(
                    "Devuelve un único valor lógico.",
                    "Return one logical value.",
                    "Returnér én logisk værdi.",
                ),
            ),
            _t(
                "aligned_samples <- function(x, metadata) { !anyDuplicated(colnames(x)) && !anyDuplicated(metadata$sample_id) && identical(colnames(x), metadata$sample_id) }",
                "aligned_samples <- function(x, metadata) { !anyDuplicated(colnames(x)) && !anyDuplicated(metadata$sample_id) && identical(colnames(x), metadata$sample_id) }",
                "aligned_samples <- function(x, metadata) { !anyDuplicated(colnames(x)) && !anyDuplicated(metadata$sample_id) && identical(colnames(x), metadata$sample_id) }",
            ),
            _t(
                "La función exige unicidad y correspondencia posicional exacta.",
                "The function requires uniqueness and exact positional correspondence.",
                "Funktionen kræver unikhed og præcis positionsmæssig overensstemmelse.",
            ),
            "aligned_samples <- function(x, metadata) {\n  # return TRUE only for a safe exact alignment\n}",
        ),
        (
            "m02.p06",
            "ORAL_EXPLANATION",
            _t(
                "Prepara una explicación de 90 segundos: ¿por qué normalizar no corrige automáticamente un efecto de lote?",
                "Prepare a 90-second explanation: why does normalization not automatically correct a batch effect?",
                "Forbered en 90-sekunders forklaring: hvorfor korrigerer normalisering ikke automatisk en batcheffekt?",
            ),
            (
                _t(
                    "Define primero normalización y lote.",
                    "Define normalization and batch first.",
                    "Definér først normalisering og batch.",
                ),
                _t(
                    "Incluye una estrategia de diagnóstico y modelado.",
                    "Include a diagnostic and modeling strategy.",
                    "Medtag en diagnostisk og modelleringsstrategi.",
                ),
            ),
            _t(
                "La normalización ajusta factores técnicos específicos como profundidad o escala global. Un lote puede alterar subconjuntos de características o interactuar con la biología, por lo que debe diagnosticarse con metadata y visualización, incluirse en el diseño cuando sea identificable y evaluarse mediante sensibilidad. Si lote y grupo están confundidos, el efecto no puede separarse de forma fiable.",
                "Normalization adjusts specific technical factors such as depth or global scale. A batch can alter subsets of features or interact with biology, so it should be diagnosed using metadata and visualization, included in the design when identifiable, and assessed through sensitivity analysis. If batch and group are confounded, their effects cannot be reliably separated.",
                "Normalisering justerer specifikke tekniske faktorer som dybde eller global skala. Et batch kan påvirke undergrupper af features eller interagere med biologien og bør derfor diagnosticeres med metadata og visualisering, inkluderes i designet når det kan identificeres, og vurderes med følsomhedsanalyse. Hvis batch og gruppe er confounded, kan effekterne ikke adskilles pålideligt.",
            ),
            _t(
                "Una respuesta sólida separa objetivo técnico, diagnóstico, diseño y límite de identificabilidad.",
                "A strong answer separates technical target, diagnosis, design, and identifiability limit.",
                "Et stærkt svar adskiller teknisk mål, diagnose, design og grænsen for identificerbarhed.",
            ),
            "",
        ),
    ),
    mcqs=(
        _mcq(
            "q01",
            _t(
                "¿Qué comprobación protege directamente contra asignar una muestra al grupo equivocado?",
                "Which check directly protects against assigning a sample to the wrong group?",
                "Hvilken kontrol beskytter direkte mod at tildele en prøve til den forkerte gruppe?",
            ),
            (
                _option(
                    "a",
                    _t(
                        "Comparar media y mediana",
                        "Compare mean and median",
                        "Sammenlign middelværdi og median",
                    ),
                ),
                _option(
                    "b",
                    _t(
                        "Comprobar coincidencia exacta y única entre colnames y sample_id",
                        "Check exact unique agreement between colnames and sample_id",
                        "Kontrollér præcis unik overensstemmelse mellem colnames og sample_id",
                    ),
                ),
                _option("c", _t("Aplicar log2", "Apply log2", "Anvend log2")),
                _option(
                    "d",
                    _t(
                        "Eliminar genes constantes",
                        "Remove constant genes",
                        "Fjern konstante gener",
                    ),
                ),
            ),
            "b",
            _t(
                "La correspondencia exacta de identificadores vincula cada columna con su metadata correcta.",
                "Exact identifier correspondence links every column to the correct metadata row.",
                "Præcis identifikatoroverensstemmelse forbinder hver kolonne med den korrekte metadata-række.",
            ),
        ),
        _mcq(
            "q02",
            _t(
                "¿Qué afirmación describe mejor una muestra extrema en PCA?",
                "Which statement best describes an extreme sample in PCA?",
                "Hvilket udsagn beskriver bedst en ekstrem prøve i PCA?",
            ),
            (
                _option(
                    "a",
                    _t(
                        "Debe eliminarse siempre",
                        "It must always be removed",
                        "Den skal altid fjernes",
                    ),
                ),
                _option(
                    "b",
                    _t(
                        "Prueba contaminación",
                        "It proves contamination",
                        "Den beviser kontaminering",
                    ),
                ),
                _option(
                    "c",
                    _t(
                        "Es una señal que requiere investigación independiente",
                        "It is a signal requiring independent investigation",
                        "Det er et signal, der kræver uafhængig undersøgelse",
                    ),
                ),
                _option(
                    "d",
                    _t(
                        "Demuestra efecto biológico",
                        "It proves a biological effect",
                        "Den beviser en biologisk effekt",
                    ),
                ),
            ),
            "c",
            _t(
                "La separación puede reflejar biología, lote, error o variación legítima y necesita evidencia adicional.",
                "Separation may reflect biology, batch, error, or legitimate variation and needs additional evidence.",
                "Adskillelsen kan afspejle biologi, batch, fejl eller legitim variation og kræver yderligere evidens.",
            ),
        ),
        _mcq(
            "q03",
            _t(
                "¿Qué operación elimina características poco informativas?",
                "Which operation removes poorly informative features?",
                "Hvilken operation fjerner features med lav information?",
            ),
            (
                _option("a", _t("Filtrado", "Filtering", "Filtrering")),
                _option("b", _t("Normalización", "Normalization", "Normalisering")),
                _option("c", _t("Escalado", "Scaling", "Skalering")),
                _option("d", _t("Ajuste por lote", "Batch adjustment", "Batchjustering")),
            ),
            "a",
            _t(
                "El filtrado aplica una regla explícita de información o abundancia.",
                "Filtering applies an explicit information or abundance rule.",
                "Filtrering anvender en eksplicit informations- eller abundansregel.",
            ),
        ),
        _mcq(
            "q04",
            _t(
                "¿Qué operación ajusta principalmente diferencias de exposición técnica entre muestras?",
                "Which operation primarily adjusts differences in technical exposure among samples?",
                "Hvilken operation justerer primært forskelle i teknisk eksponering mellem prøver?",
            ),
            (
                _option("a", _t("Anotación", "Annotation", "Annotering")),
                _option("b", _t("Normalización", "Normalization", "Normalisering")),
                _option("c", _t("Clustering", "Clustering", "Clustering")),
                _option("d", _t("Imputación de grupo", "Group imputation", "Gruppeimputation")),
            ),
            "b",
            _t(
                "La normalización busca hacer comparables factores técnicos definidos.",
                "Normalization aims to make defined technical factors comparable.",
                "Normalisering sigter mod at gøre definerede tekniske faktorer sammenlignelige.",
            ),
        ),
        _mcq(
            "q05",
            _t(
                "¿Por qué debe conservarse la matriz de conteos crudos?",
                "Why should the raw count matrix be retained?",
                "Hvorfor bør den rå count-matrix bevares?",
            ),
            (
                _option(
                    "a",
                    _t("Para modificarla después", "To modify it later", "For at ændre den senere"),
                ),
                _option(
                    "b",
                    _t(
                        "Porque algunos modelos requieren conteos y para mantener trazabilidad",
                        "Because some models require counts and to preserve provenance",
                        "Fordi nogle modeller kræver counts, og for at bevare sporbarhed",
                    ),
                ),
                _option(
                    "c",
                    _t(
                        "Porque siempre es adecuada para PCA",
                        "Because it is always suitable for PCA",
                        "Fordi den altid er egnet til PCA",
                    ),
                ),
                _option(
                    "d",
                    _t(
                        "Para reemplazar metadata",
                        "To replace metadata",
                        "For at erstatte metadata",
                    ),
                ),
            ),
            "b",
            _t(
                "Los datos fuente inmutables permiten reproducir transformaciones y usar modelos compatibles con conteos.",
                "Immutable source data support reproducible transformations and count-compatible models.",
                "Uforanderlige kildedata understøtter reproducerbare transformationer og count-kompatible modeller.",
            ),
        ),
        _mcq(
            "q06",
            _t(
                "¿Qué riesgo tiene aplicar z-score por característica?",
                "What is a consequence of feature-wise z-scoring?",
                "Hvad er en konsekvens af featurevis z-score?",
            ),
            (
                _option(
                    "a",
                    _t(
                        "Conserva magnitudes absolutas",
                        "It preserves absolute magnitudes",
                        "Det bevarer absolutte størrelser",
                    ),
                ),
                _option(
                    "b",
                    _t(
                        "Elimina toda variación",
                        "It removes all variation",
                        "Det fjerner al variation",
                    ),
                ),
                _option(
                    "c",
                    _t(
                        "Iguala escala pero pierde magnitud absoluta",
                        "It equalizes scale but loses absolute magnitude",
                        "Det udligner skala men mister absolut størrelse",
                    ),
                ),
                _option(
                    "d",
                    _t(
                        "Corrige cualquier lote",
                        "It corrects every batch",
                        "Det korrigerer ethvert batch",
                    ),
                ),
            ),
            "c",
            _t(
                "Centrar y dividir por desviación estándar cambia la interpretación de magnitud.",
                "Centering and dividing by standard deviation changes magnitude interpretation.",
                "Centrering og division med standardafvigelsen ændrer fortolkningen af størrelse.",
            ),
        ),
        _mcq(
            "q07",
            _t(
                "¿Qué debe acompañar una exclusión de muestra?",
                "What should accompany a sample exclusion?",
                "Hvad bør ledsage en prøveeksklusion?",
            ),
            (
                _option("a", _t("Sólo una figura PCA", "Only a PCA plot", "Kun et PCA-plot")),
                _option(
                    "b",
                    _t(
                        "Criterio independiente, trazabilidad y análisis de sensibilidad",
                        "An independent criterion, provenance, and sensitivity analysis",
                        "Et uafhængigt kriterium, sporbarhed og følsomhedsanalyse",
                    ),
                ),
                _option(
                    "c",
                    _t(
                        "Mejor separación de grupos",
                        "Better group separation",
                        "Bedre gruppeadskillelse",
                    ),
                ),
                _option("d", _t("Menor valor p", "A smaller p-value", "En mindre p-værdi")),
            ),
            "b",
            _t(
                "La exclusión no debe elegirse para mejorar el resultado observado.",
                "Exclusion should not be chosen to improve the observed result.",
                "Eksklusion bør ikke vælges for at forbedre det observerede resultat.",
            ),
        ),
        _mcq(
            "q08",
            _t(
                "¿Qué práctica favorece escalabilidad y auditabilidad?",
                "Which practice supports scalability and auditability?",
                "Hvilken praksis understøtter skalerbarhed og auditérbarhed?",
            ),
            (
                _option(
                    "a",
                    _t(
                        "Crear copias completas en cada paso",
                        "Create full copies at every step",
                        "Opret fulde kopier ved hvert trin",
                    ),
                ),
                _option(
                    "b",
                    _t("Modificar los archivos fuente", "Modify source files", "Ændr kildefilerne"),
                ),
                _option(
                    "c",
                    _t(
                        "Registrar dimensiones, parámetros y artefactos",
                        "Record dimensions, parameters, and artifacts",
                        "Registrér dimensioner, parametre og artefakter",
                    ),
                ),
                _option(
                    "d",
                    _t(
                        "Omitir matrices pequeñas de prueba",
                        "Skip small test matrices",
                        "Spring små testmatricer over",
                    ),
                ),
            ),
            "c",
            _t(
                "Los registros intermedios permiten detectar cambios inesperados y reproducir el flujo.",
                "Intermediate records allow unexpected changes to be detected and the workflow reproduced.",
                "Mellemregistreringer gør det muligt at opdage uventede ændringer og reproducere workflowet.",
            ),
        ),
    ),
    true_false=(
        _tf(
            "tf01",
            _t(
                "El orden de las muestras puede ignorarse si los nombres aparecen en ambos objetos.",
                "Sample order can be ignored when names occur in both objects.",
                "Prøverækkefølgen kan ignoreres, når navnene findes i begge objekter.",
            ),
            False,
            _t(
                "El orden debe coincidir o reordenarse de forma validada.",
                "Order must match or be reordered with validation.",
                "Rækkefølgen skal matche eller omordnes med validering.",
            ),
        ),
        _tf(
            "tf02",
            _t(
                "Una muestra separada en PCA debe investigarse antes de decidir su exclusión.",
                "A sample separated in PCA should be investigated before deciding on exclusion.",
                "En prøve adskilt i PCA bør undersøges før beslutning om eksklusion.",
            ),
            True,
            _t(
                "PCA es una señal diagnóstica, no una decisión causal.",
                "PCA is a diagnostic signal, not a causal decision.",
                "PCA er et diagnostisk signal, ikke en kausal beslutning.",
            ),
        ),
        _tf(
            "tf03",
            _t(
                "Filtrado y normalización responden a la misma pregunta.",
                "Filtering and normalization answer the same question.",
                "Filtrering og normalisering besvarer det samme spørgsmål.",
            ),
            False,
            _t(
                "Filtrado decide qué características conservar; normalización ajusta comparabilidad técnica.",
                "Filtering decides which features to retain; normalization adjusts technical comparability.",
                "Filtrering afgør hvilke features der bevares; normalisering justerer teknisk sammenlignelighed.",
            ),
        ),
        _tf(
            "tf04",
            _t(
                "Los conteos crudos pueden ser necesarios para modelos de RNA-seq.",
                "Raw counts may be required by RNA-seq models.",
                "Rå counts kan være nødvendige for RNA-seq-modeller.",
            ),
            True,
            _t(
                "Los modelos de conteo suelen estimar media y dispersión desde conteos no transformados.",
                "Count models commonly estimate mean and dispersion from untransformed counts.",
                "Count-modeller estimerer ofte middelværdi og dispersion fra utransformerede counts.",
            ),
        ),
        _tf(
            "tf05",
            _t(
                "Normalizar por profundidad elimina cualquier efecto de lote.",
                "Depth normalization removes every batch effect.",
                "Normalisering efter dybde fjerner enhver batcheffekt.",
            ),
            False,
            _t(
                "Un lote puede afectar características selectivamente y debe modelarse o investigarse por separado.",
                "A batch may affect features selectively and must be modeled or investigated separately.",
                "Et batch kan påvirke features selektivt og skal modelleres eller undersøges separat.",
            ),
        ),
        _tf(
            "tf06",
            _t(
                "Una regla de filtrado supervisada debe aprenderse sólo con datos de entrenamiento.",
                "A supervised filtering rule should be learned only from training data.",
                "En superviseret filtreringsregel bør kun læres fra træningsdata.",
            ),
            True,
            _t(
                "Usar etiquetas de validación o prueba para seleccionar features produce fuga.",
                "Using validation or test labels for feature selection causes leakage.",
                "Brug af validerings- eller testlabels til featurevalg skaber leakage.",
            ),
        ),
        _tf(
            "tf07",
            _t(
                "Los archivos fuente deberían permanecer inmutables.",
                "Source files should remain immutable.",
                "Kildefiler bør forblive uforanderlige.",
            ),
            True,
            _t(
                "Las transformaciones deben producir artefactos derivados trazables.",
                "Transformations should produce traceable derived artifacts.",
                "Transformationer bør producere sporbare afledte artefakter.",
            ),
        ),
        _tf(
            "tf08",
            _t(
                "Un pipeline rápido puede considerarse válido aunque las muestras estén desalineadas.",
                "A fast pipeline can be considered valid even when samples are misaligned.",
                "En hurtig pipeline kan betragtes som gyldig, selv når prøver er fejlafstemt.",
            ),
            False,
            _t(
                "El rendimiento no compensa una asociación incorrecta entre datos y metadata.",
                "Performance does not compensate for an incorrect data-metadata association.",
                "Ydeevne kompenserer ikke for en forkert forbindelse mellem data og metadata.",
            ),
        ),
    ),
    tutor=(
        _t(
            "El análisis ómico comienza con un contrato explícito de matriz, metadata y procedencia. El tutor debe separar calidad, normalización, transformación y escalado, y nunca recomendar exclusiones sólo para mejorar patrones.",
            "Omics analysis begins with an explicit matrix, metadata, and provenance contract. The tutor must separate quality, normalization, transformation, and scaling and never recommend exclusions merely to improve patterns.",
            "Omikanalyse begynder med en eksplicit kontrakt for matrix, metadata og proveniens. Tutoren skal adskille kvalitet, normalisering, transformation og skalering og må aldrig anbefale eksklusioner alene for at forbedre mønstre.",
        ),
        (
            _t(
                "Las muestras y metadata deben estar alineadas de forma única.",
                "Samples and metadata must be uniquely aligned.",
                "Prøver og metadata skal være entydigt afstemt.",
            ),
            _t(
                "El control de calidad produce preguntas para investigar, no exclusiones automáticas.",
                "Quality control produces questions to investigate, not automatic exclusions.",
                "Kvalitetskontrol skaber spørgsmål til undersøgelse, ikke automatiske eksklusioner.",
            ),
            _t(
                "Filtrado, normalización, transformación y escalado tienen objetivos diferentes.",
                "Filtering, normalization, transformation, and scaling have different purposes.",
                "Filtrering, normalisering, transformation og skalering har forskellige formål.",
            ),
            _t(
                "Los datos fuente y parámetros deben conservarse para reproducibilidad.",
                "Source data and parameters must be retained for reproducibility.",
                "Kildedata og parametre skal bevares for reproducerbarhed.",
            ),
        ),
        (
            _t(
                "Eliminar toda muestra separada en PCA.",
                "Removing every sample separated in PCA.",
                "At fjerne enhver prøve adskilt i PCA.",
            ),
            _t(
                "Usar normalización como sinónimo de corrección de lote.",
                "Using normalization as a synonym for batch correction.",
                "At bruge normalisering som synonym for batchkorrektion.",
            ),
            _t(
                "Reordenar metadata sin comprobar NA o duplicados.",
                "Reordering metadata without checking NA or duplicates.",
                "At omordne metadata uden at kontrollere NA eller dubletter.",
            ),
            _t(
                "Sobrescribir la matriz fuente con valores transformados.",
                "Overwriting the source matrix with transformed values.",
                "At overskrive kildematricen med transformerede værdier.",
            ),
        ),
        (
            _t(
                "¿Qué representa una celda y cuál es la unidad independiente?",
                "What does one cell represent, and what is the independent unit?",
                "Hvad repræsenterer én celle, og hvad er den uafhængige enhed?",
            ),
            _t(
                "¿Qué factor técnico intenta ajustar la normalización?",
                "Which technical factor is normalization intended to adjust?",
                "Hvilken teknisk faktor skal normaliseringen justere?",
            ),
            _t(
                "¿Qué evidencia independiente justificaría excluir una muestra?",
                "What independent evidence would justify excluding a sample?",
                "Hvilken uafhængig evidens ville retfærdiggøre at ekskludere en prøve?",
            ),
            _t(
                "¿El método posterior requiere conteos, valores transformados o variables escaladas?",
                "Does the downstream method require counts, transformed values, or scaled variables?",
                "Kræver den efterfølgende metode counts, transformerede værdier eller skalerede variable?",
            ),
        ),
        (
            _t(
                "Declara matriz, metadata, IDs y procedencia.",
                "Declares matrix, metadata, IDs, and provenance.",
                "Deklarerer matrix, metadata, ID'er og proveniens.",
            ),
            _t(
                "Interpreta métricas de calidad sin automatizar exclusiones.",
                "Interprets quality metrics without automating exclusions.",
                "Fortolker kvalitetsmål uden at automatisere eksklusioner.",
            ),
            _t(
                "Justifica cada operación de preprocesamiento.",
                "Justifies each preprocessing operation.",
                "Begrunder hver præprocesseringsoperation.",
            ),
            _t(
                "Conserva artefactos y parámetros reproducibles.",
                "Retains reproducible artifacts and parameters.",
                "Bevarer reproducerbare artefakter og parametre.",
            ),
        ),
        (
            _t(
                "No inventar propiedades del dataset que no estén declaradas.",
                "Do not invent dataset properties that are not declared.",
                "Opfind ikke egenskaber ved datasættet, der ikke er deklareret.",
            ),
            _t(
                "No confundir una transformación exploratoria con la entrada requerida por un modelo.",
                "Do not confuse an exploratory transformation with the input required by a model.",
                "Forveksl ikke en eksplorativ transformation med det input, en model kræver.",
            ),
            _t(
                "No convertir una señal de QC en una causa confirmada.",
                "Do not turn a QC signal into a confirmed cause.",
                "Gør ikke et QC-signal til en bekræftet årsag.",
            ),
            _t(
                "Responder en el idioma activo y preservar nombres técnicos de R.",
                "Respond in the active language and preserve technical R names.",
                "Svar på det aktive sprog og bevar tekniske R-navne.",
            ),
        ),
        (
            "https://odin.sdu.dk/sitecore/index.php?a=searchfagbesk&internkode=BMB831&lang=en",
            "https://bioconductor.org/packages/release/bioc/html/SummarizedExperiment.html",
            "https://bioconductor.org/help/course-materials/",
        ),
    ),
)

LOCALIZED_MODULE_02_OMICS_MATRICES_QC = build_module(_SPEC)
LOCALIZED_OBJECTIVE_QUESTION_BANK_02 = build_question_bank(_SPEC)


def materialize_module_02_question_bank(
    locale: AppLocale | str = AppLocale.SPANISH_SPAIN,
) -> tuple[AssessmentItem, ...]:
    """Materialize the stable module 2 objective bank."""

    return materialize_bank(LOCALIZED_OBJECTIVE_QUESTION_BANK_02, locale)


MODULE_02_OMICS_MATRICES_QC: LearningModule = LOCALIZED_MODULE_02_OMICS_MATRICES_QC.materialize(
    AppLocale.SPANISH_SPAIN
)
OBJECTIVE_QUESTION_BANK_02 = materialize_module_02_question_bank()

__all__ = [
    "LOCALIZED_MODULE_02_OMICS_MATRICES_QC",
    "LOCALIZED_OBJECTIVE_QUESTION_BANK_02",
    "MODULE_02_OMICS_MATRICES_QC",
    "OBJECTIVE_QUESTION_BANK_02",
    "materialize_module_02_question_bank",
]
