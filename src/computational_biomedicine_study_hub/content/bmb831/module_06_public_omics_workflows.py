"""BMB831 module 6: versioned public transcriptomics and proteomics workflows."""

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
    module_id="bmb831.m06",
    title=_t(
        "Pipelines públicos de transcriptómica y proteómica",
        "Public transcriptomics and proteomics pipelines",
        "Offentlige transcriptomik- og proteomikpipelines",
    ),
    summary=_t(
        "Construye un análisis de extremo a extremo desde una fuente pública identificable hasta resultados auditables, separando adquisición, cuantificación, QC, modelado, visualización e interpretación y conservando versiones, metadatos y checksums.",
        "Build an end-to-end analysis from an identifiable public source to auditable results, separating acquisition, quantification, QC, modeling, visualization, and interpretation while retaining versions, metadata, and checksums.",
        "Byg en end-to-end-analyse fra en identificerbar offentlig kilde til auditérbare resultater, hvor acquisition, kvantificering, QC, modellering, visualisering og fortolkning adskilles, og versioner, metadata og checksums bevares.",
    ),
    objectives=(
        (
            "m06.o1",
            _t(
                "Crear una tarjeta de dataset y un manifiesto local para una fuente pública de RNA-seq o proteómica.",
                "Create a dataset card and local manifest for a public RNA-seq or proteomics source.",
                "Oprette et datasetkort og lokalt manifest for en offentlig RNA-seq- eller proteomikkilde.",
            ),
        ),
        (
            "m06.o2",
            _t(
                "Distinguir unidades y etapas de RNA-seq y MS-proteómica desde archivos fuente hasta matrices analíticas.",
                "Distinguish RNA-seq and MS-proteomics units and stages from source files to analytical matrices.",
                "Skelne mellem enheder og trin i RNA-seq og MS-proteomik fra kildefiler til analytiske matricer.",
            ),
        ),
        (
            "m06.o3",
            _t(
                "Diseñar QC, normalización, missingness, modelado y multiplicidad compatibles con cada modalidad.",
                "Design QC, normalization, missingness handling, modeling, and multiplicity compatible with each modality.",
                "Designe QC, normalisering, håndtering af missingness, modellering og multiplicitet kompatibelt med hver modalitet.",
            ),
        ),
        (
            "m06.o4",
            _t(
                "Producir un paquete reproducible con artefactos intermedios, decisiones, resultados y límites de generalización.",
                "Produce a reproducible package with intermediate artifacts, decisions, results, and generalization limits.",
                "Producere en reproducerbar pakke med mellemprodukter, beslutninger, resultater og generaliseringsgrænser.",
            ),
        ),
    ),
    concepts=(
        (
            "source-contract",
            _t("Fuente pública y snapshot local", "Public source and local snapshot", "Offentlig kilde og lokalt snapshot"),
            _t(
                "Un accession o nombre de paquete identifica una fuente, pero no define los archivos realmente analizados. El snapshot local debe registrar versión o fecha de acceso, nombres, tamaños, checksums, licencia o condiciones de uso, metadata y cualquier selección realizada. El dataset card declara diseño, unidad independiente, modalidades, factores técnicos, exclusiones y límites. Los archivos fuente permanecen inmutables.",
                "An accession or package name identifies a source but not the files actually analyzed. The local snapshot records version or access date, names, sizes, checksums, license or use conditions, metadata, and every selection made. The dataset card declares design, independent unit, modalities, technical factors, exclusions, and limits. Source files remain immutable.",
                "En accession eller et pakkenavn identificerer en kilde, men ikke de filer der faktisk analyseres. Det lokale snapshot registrerer version eller adgangsdato, navne, størrelser, checksums, licens eller brugsvilkår, metadata og alle foretagne valg. Datasetkortet deklarerer design, uafhængig enhed, modaliteter, tekniske faktorer, eksklusioner og grænser. Kildefiler forbliver uforanderlige.",
            ),
            (
                _t("La aplicación registra fuentes, pero el usuario conserva el snapshot exacto.", "The application registers sources, while the learner retains the exact snapshot.", "Applikationen registrerer kilder, mens den studerende bevarer det præcise snapshot."),
                _t("No se analiza una URL mutable como si fuera una versión.", "A mutable URL is not analyzed as though it were a version.", "En mutabel URL analyseres ikke som om den var en version."),
            ),
        ),
        (
            "rnaseq-workflow",
            _t("Contrato RNA-seq", "RNA-seq contract", "RNA-seq-kontrakt"),
            _t(
                "Un pipeline bulk RNA-seq conecta bibliotecas y muestras con cuantificaciones por transcrito o gen. Debe documentar referencia, anotación, cuantificador, versión y reglas de importación. Para modelos de conteo, la matriz analítica conserva conteos compatibles con el método; transformaciones de estabilización se reservan para exploración y visualización. El diseño experimental, no la cantidad de genes, determina replicación e inferencia.",
                "A bulk RNA-seq pipeline connects libraries and samples to transcript- or gene-level quantifications. It documents reference, annotation, quantifier, version, and import rules. For count models, the analytical matrix retains counts compatible with the method; variance-stabilizing transformations are reserved for exploration and visualization. Experimental design, not gene count, determines replication and inference.",
                "En bulk RNA-seq-pipeline forbinder biblioteker og prøver med transkript- eller genniveaukvantificeringer. Den dokumenterer reference, annotering, kvantificeringsværktøj, version og importregler. Til count-modeller bevarer den analytiske matrix counts kompatible med metoden; variansstabiliserende transformationer bruges til udforskning og visualisering. Forsøgsdesign, ikke antal gener, bestemmer replikation og inferens.",
            ),
            (
                _t("Airway sirve como fuente pública docente, no como evidencia universal.", "Airway is a public teaching source, not universal evidence.", "Airway er en offentlig undervisningskilde, ikke universel evidens."),
                _t("Cell line y treatment pertenecen al diseño y deben modelarse.", "Cell line and treatment belong to the design and must be modeled.", "Cellelinje og behandling tilhører designet og skal modelleres."),
            ),
        ),
        (
            "proteomics-workflow",
            _t("Contrato MS-proteómico", "MS-proteomics contract", "MS-proteomikkontrakt"),
            _t(
                "La proteómica puede comenzar en espectros, identificaciones, precursores, péptidos o intensidades de proteínas. Cada nivel tiene claves y fuentes de incertidumbre distintas. Deben documentarse software de búsqueda o cuantificación, filtros de calidad, protein grouping, normalización y tratamiento de valores no detectados. Missingness dependiente de intensidad no debe reemplazarse automáticamente por un número pequeño sin evaluar el mecanismo y la sensibilidad.",
                "Proteomics may begin with spectra, identifications, precursors, peptides, or protein intensities. Each level has distinct keys and uncertainty sources. Search or quantification software, quality filters, protein grouping, normalization, and treatment of nondetections must be documented. Intensity-dependent missingness should not be automatically replaced by a small number without assessing mechanism and sensitivity.",
                "Proteomik kan begynde med spektre, identifikationer, precursors, peptider eller proteinintensiteter. Hvert niveau har forskellige nøgler og usikkerhedskilder. Søge- eller kvantificeringssoftware, kvalitetsfiltre, protein grouping, normalisering og håndtering af ikke-detekterede værdier skal dokumenteres. Intensitetsafhængig missingness bør ikke automatisk erstattes af et lille tal uden vurdering af mekanisme og følsomhed.",
            ),
            (
                _t("El accession de ProteomeXchange no define por sí solo la tabla final.", "A ProteomeXchange accession does not by itself define the final table.", "En ProteomeXchange-accession definerer ikke i sig selv den endelige tabel."),
                _t("Conserva el mapeo precursor–péptido–proteína.", "Retain precursor–peptide–protein mappings.", "Bevar precursor–peptid–protein-mappinger."),
            ),
        ),
        (
            "analysis-package",
            _t("Paquete reproducible y controles de transición", "Reproducible package and transition checks", "Reproducerbar pakke og overgangskontroller"),
            _t(
                "Cada transición del pipeline registra dimensiones, IDs, tipos, missingness y checksums: fuente a matriz, matriz a objeto filtrado, objeto a modelo y modelo a tablas/figuras. El paquete final contiene manifest, dataset card, scripts, parámetros, session information, tablas completas y un registro de decisiones. Un resultado aislado sin trazabilidad no demuestra que el pipeline sea reproducible.",
                "Every pipeline transition records dimensions, IDs, types, missingness, and checksums: source to matrix, matrix to filtered object, object to model, and model to tables or figures. The final package contains a manifest, dataset card, scripts, parameters, session information, complete tables, and a decision log. An isolated result without traceability does not demonstrate reproducibility.",
                "Hver pipelineovergang registrerer dimensioner, ID'er, typer, missingness og checksums: kilde til matrix, matrix til filtreret objekt, objekt til model og model til tabeller eller figurer. Den endelige pakke indeholder manifest, datasetkort, scripts, parametre, session information, komplette tabeller og beslutningslog. Et isoleret resultat uden sporbarhed demonstrerer ikke reproducerbarhed.",
            ),
            (
                _t("Las comprobaciones fallan temprano ante IDs o dimensiones inesperadas.", "Checks fail early on unexpected IDs or dimensions.", "Kontroller fejler tidligt ved uventede ID'er eller dimensioner."),
                _t("Las conclusiones se limitan al diseño representado.", "Conclusions are limited to the represented design.", "Konklusioner begrænses til det repræsenterede design."),
            ),
        ),
    ),
    examples=(
        (
            "m06.e01",
            _t("Auditar una transición de matriz", "Audit a matrix transition", "Auditér en matrixovergang"),
            _t("Filtra características con una regla declarada y registra dimensiones y missingness antes y después.", "Filter features with a declared rule and record dimensions and missingness before and after.", "Filtrér features med en deklareret regel og registrér dimensioner og missingness før og efter."),
            (
                _t("La matriz fuente se conserva.", "The source matrix is retained.", "Kildematricen bevares."),
                _t("La regla no usa etiquetas de outcome.", "The rule does not use outcome labels.", "Reglen bruger ikke outcome-labels."),
                _t("La auditoría cuantifica la transición.", "The audit quantifies the transition.", "Auditten kvantificerer overgangen."),
            ),
            """x <- matrix(
  c(10, 20, 30, 40,
    0, 0, 1, 0,
    8, NA, 9, 10,
    100, 120, 130, 140),
  nrow = 4,
  byrow = TRUE,
  dimnames = list(paste0("F", 1:4), paste0("S", 1:4))
)
keep <- rowSums(x >= 5, na.rm = TRUE) >= 3
filtered <- x[keep, , drop = FALSE]
cat("source_dim=", paste(dim(x), collapse = "x"), "\n", sep = "")
cat("filtered_dim=", paste(dim(filtered), collapse = "x"), "\n", sep = "")
cat(sprintf("filtered_missing=%.3f", mean(is.na(filtered))))
""",
            """source_dim=4x4
filtered_dim=3x4
filtered_missing=0.083""",
            _t("La auditoría conserva tres características y registra un valor faltante entre doce celdas.", "The audit retains three features and records one missing value among twelve cells.", "Auditten bevarer tre features og registrerer én manglende værdi blandt tolv celler."),
        ),
        (
            "m06.e02",
            _t("Comparar missingness entre grupos sin imputar", "Compare missingness across groups without imputation", "Sammenlign missingness mellem grupper uden imputation"),
            _t("Resume detección por condición antes de decidir un método proteómico.", "Summarize detection by condition before choosing a proteomics method.", "Opsummér detektion efter betingelse før valg af proteomikmetode."),
            (
                _t("Las columnas son muestras.", "Columns are samples.", "Kolonner er prøver."),
                _t("NA representa no detección en el fixture.", "NA represents nondetection in the fixture.", "NA repræsenterer ikke-detektion i fixturet."),
                _t("La comparación informa el mecanismo potencial.", "The comparison informs the potential mechanism.", "Sammenligningen informerer den potentielle mekanisme."),
            ),
            """intensity <- matrix(
  c(10, 11, NA, 13,
    NA, NA, 8, 9,
    6, 7, 6, 7),
  nrow = 3,
  byrow = TRUE,
  dimnames = list(paste0("P", 1:3), paste0("S", 1:4))
)
group <- c("A", "A", "B", "B")
detection <- sapply(split(seq_along(group), group), function(index) {
  mean(!is.na(intensity[, index, drop = FALSE]))
})
cat("detection_A=", format(round(detection["A"], 3), nsmall = 3), "\n", sep = "")
cat("detection_B=", format(round(detection["B"], 3), nsmall = 3), sep = "")
""",
            """detection_A=0.667
detection_B=0.833""",
            _t("La detección difiere entre grupos; esto debe investigarse antes de una imputación o análisis diferencial.", "Detection differs across groups; this must be investigated before imputation or differential analysis.", "Detektion varierer mellem grupper; dette skal undersøges før imputation eller differential analyse."),
        ),
    ),
    practices=(
        (
            "m06.p01",
            "PIPELINE_DESIGN",
            _t("Diseña la estructura de carpetas y manifiestos para un snapshot local de airway.", "Design the folder and manifest structure for a local airway snapshot.", "Design mappe- og manifeststrukturen for et lokalt airway-snapshot."),
            (_t("Separa raw, derived y results.", "Separate raw, derived, and results.", "Adskil raw, derived og results."), _t("Incluye versión y checksums.", "Include version and checksums.", "Medtag version og checksums.")),
            _t("raw contiene el objeto o export original y metadata inmutable; manifest registra versión, fecha, archivos y SHA-256; derived contiene matrices filtradas y transformadas; results conserva tablas y figuras; dataset_card declara diseño, unidad, variables y límites; scripts y sessionInfo permiten regeneración.", "raw contains the original object or export and immutable metadata; the manifest records version, date, files, and SHA-256; derived contains filtered and transformed matrices; results retains tables and figures; the dataset card declares design, unit, variables, and limits; scripts and sessionInfo enable regeneration.", "raw indeholder det originale objekt eller eksport og uforanderlige metadata; manifestet registrerer version, dato, filer og SHA-256; derived indeholder filtrerede og transformerede matricer; results bevarer tabeller og figurer; datasetkortet deklarerer design, enhed, variable og grænser; scripts og sessionInfo muliggør regenerering."),
            _t("La estructura separa procedencia, transformación y comunicación.", "The structure separates provenance, transformation, and communication.", "Strukturen adskiller proveniens, transformation og kommunikation."),
            "",
        ),
        (
            "m06.p02",
            "SHORT_ANSWER",
            _t("Compara la unidad analítica en RNA-seq y proteómica LFQ.", "Compare the analytical unit in RNA-seq and LFQ proteomics.", "Sammenlign den analytiske enhed i RNA-seq og LFQ-proteomik."),
            (_t("Distingue muestra de feature.", "Distinguish sample from feature.", "Skeln mellem prøve og feature."), _t("Incluye niveles proteómicos.", "Include proteomics levels.", "Medtag proteomikniveauer.")),
            _t("La unidad independiente suele ser la muestra biológica en ambas modalidades. Las features RNA-seq son genes o transcritos derivados de bibliotecas; en proteómica pueden ser precursors, péptidos, protein groups o proteínas. Cambiar de nivel requiere un mapeo explícito y cambia incertidumbre e interpretación.", "The independent unit is usually the biological sample in both modalities. RNA-seq features are genes or transcripts derived from libraries; proteomics features may be precursors, peptides, protein groups, or proteins. Changing level requires explicit mapping and changes uncertainty and interpretation.", "Den uafhængige enhed er normalt den biologiske prøve i begge modaliteter. RNA-seq-features er gener eller transkripter afledt af biblioteker; proteomik-features kan være precursors, peptider, protein groups eller proteiner. Niveauændring kræver eksplicit mapping og ændrer usikkerhed og fortolkning."),
            _t("Miles de features no sustituyen réplicas biológicas.", "Thousands of features do not replace biological replicates.", "Tusindvis af features erstatter ikke biologiske replikater."),
            "",
        ),
        (
            "m06.p03",
            "DEBUGGING",
            _t("Un analista descarga nuevamente una URL latest y no puede reproducir el resultado anterior. Reconstruye el fallo.", "An analyst redownloads a latest URL and cannot reproduce the earlier result. Reconstruct the failure.", "En analytiker downloader en latest-URL igen og kan ikke reproducere det tidligere resultat. Rekonstruér fejlen."),
            (_t("Latest no es una versión.", "Latest is not a version.", "Latest er ikke en version."), _t("Faltan archivos y hashes locales.", "Local files and hashes are missing.", "Lokale filer og hashes mangler.")),
            _t("El pipeline dependía de contenido mutable no archivado. Debía conservar los archivos exactos, checksums, versión o accession, fecha, metadata y script de importación. El nuevo contenido debe tratarse como otro snapshot y compararse, no asumirse idéntico.", "The pipeline depended on mutable content that was not archived. Exact files, checksums, version or accession, date, metadata, and import script should have been retained. New content is a different snapshot and must be compared rather than assumed identical.", "Pipelinen afhang af mutabelt indhold, der ikke blev arkiveret. Præcise filer, checksums, version eller accession, dato, metadata og importscript skulle være bevaret. Nyt indhold er et andet snapshot og skal sammenlignes frem for at antages identisk."),
            _t("La reproducibilidad requiere fijar entradas, no sólo código.", "Reproducibility requires fixed inputs, not code alone.", "Reproducerbarhed kræver fastlåste input, ikke kun kode."),
            "",
        ),
        (
            "m06.p04",
            "DATA_INTERPRETATION",
            _t("La missingness proteómica es mayor en el grupo control y en intensidades bajas. ¿Qué implica?", "Proteomics missingness is higher in controls and at low intensities. What does this imply?", "Proteomisk missingness er højere i kontrolgruppen og ved lave intensiteter. Hvad indebærer det?"),
            (_t("No es MCAR evidente.", "It is not evidently MCAR.", "Det er ikke tydeligt MCAR."), _t("Considera sensibilidad y modelo.", "Consider sensitivity and model choice.", "Overvej følsomhed og modelvalg.")),
            _t("El patrón depende de intensidad y grupo, por lo que una imputación uniforme puede introducir diferencias artificiales o atenuarlas. Deben auditarse detección, calidad y diseño; utilizar un método que modele la no detección o cuantifique incertidumbre; y comparar conclusiones bajo estrategias plausibles.", "The pattern depends on intensity and group, so uniform imputation may create or attenuate artificial differences. Detection, quality, and design should be audited; a method modeling nondetection or quantification uncertainty should be used; and conclusions compared across plausible strategies.", "Mønstret afhænger af intensitet og gruppe, så ensartet imputation kan skabe eller dæmpe kunstige forskelle. Detektion, kvalitet og design bør auditeres; en metode der modellerer ikke-detektion eller kvantificeringsusikkerhed bør bruges; og konklusioner sammenlignes på tværs af plausible strategier."),
            _t("Missingness es parte del proceso de medida, no sólo un hueco numérico.", "Missingness is part of the measurement process, not merely a numeric gap.", "Missingness er del af måleprocessen, ikke blot et numerisk hul."),
            "",
        ),
        (
            "m06.p05",
            "CODE_COMPLETION",
            _t("Completa una función que devuelva dimensiones, número de NA y unicidad de IDs.", "Complete a function returning dimensions, NA count, and ID uniqueness.", "Færdiggør en funktion, der returnerer dimensioner, antal NA og ID-unikhed."),
            (_t("Usa dim, sum(is.na()) y anyDuplicated.", "Use dim, sum(is.na()), and anyDuplicated.", "Brug dim, sum(is.na()) og anyDuplicated."), _t("Devuelve una lista nombrada.", "Return a named list.", "Returnér en navngivet liste.")),
            _t("audit_matrix <- function(x) { list(rows = nrow(x), columns = ncol(x), missing = sum(is.na(x)), unique_rows = !anyDuplicated(rownames(x)), unique_columns = !anyDuplicated(colnames(x))) }", "audit_matrix <- function(x) { list(rows = nrow(x), columns = ncol(x), missing = sum(is.na(x)), unique_rows = !anyDuplicated(rownames(x)), unique_columns = !anyDuplicated(colnames(x))) }", "audit_matrix <- function(x) { list(rows = nrow(x), columns = ncol(x), missing = sum(is.na(x)), unique_rows = !anyDuplicated(rownames(x)), unique_columns = !anyDuplicated(colnames(x))) }"),
            _t("La función crea un control de transición mínimo y determinista.", "The function creates a minimum deterministic transition check.", "Funktionen skaber en minimal deterministisk overgangskontrol."),
            "audit_matrix <- function(x) {\n  # return a named audit list\n}",
        ),
        (
            "m06.p06",
            "ORAL_EXPLANATION",
            _t("Prepara una explicación de 90 segundos: ¿por qué una fuente pública no garantiza un análisis reproducible?", "Prepare a 90-second explanation: why does a public source not guarantee reproducible analysis?", "Forbered en 90-sekunders forklaring: hvorfor garanterer en offentlig kilde ikke en reproducerbar analyse?"),
            (_t("Incluye versión, selección y pipeline.", "Include version, selection, and pipeline.", "Medtag version, selektion og pipeline."), _t("Incluye límites de generalización.", "Include generalization limits.", "Medtag generaliseringsgrænser.")),
            _t("La fuente sólo proporciona acceso. La reproducibilidad requiere fijar archivos, versiones, checksums, metadata, unidades, filtros, parámetros, software, decisiones y artefactos. Dos personas pueden seleccionar archivos o niveles distintos del mismo accession. Además, un resultado reproducible puede seguir siendo inválido o no generalizable si el diseño no sostiene la afirmación.", "The source only provides access. Reproducibility requires fixing files, versions, checksums, metadata, units, filters, parameters, software, decisions, and artifacts. Two people may select different files or levels from the same accession. A reproducible result may still be invalid or nongeneralizable when the design does not support the claim.", "Kilden giver kun adgang. Reproducerbarhed kræver fastlåsning af filer, versioner, checksums, metadata, enheder, filtre, parametre, software, beslutninger og artefakter. To personer kan vælge forskellige filer eller niveauer fra samme accession. Et reproducerbart resultat kan stadig være ugyldigt eller ikke generaliserbart, hvis designet ikke understøtter påstanden."),
            _t("La respuesta separa acceso, reproducibilidad, validez y generalización.", "The answer separates access, reproducibility, validity, and generalization.", "Svaret adskiller adgang, reproducerbarhed, validitet og generalisering."),
            "",
        ),
    ),
    mcqs=(
        _mcq("q01", _t("¿Qué fija el snapshot analizado?", "What fixes the analyzed snapshot?", "Hvad fastlægger det analyserede snapshot?"), (_option("a", _t("Archivos exactos, versión y checksums", "Exact files, version, and checksums", "Præcise filer, version og checksums")), _option("b", _t("Sólo la URL", "Only the URL", "Kun URL'en")), _option("c", _t("El nombre del gráfico", "The plot name", "Plotnavnet")), _option("d", _t("La fecha del informe", "The report date", "Rapportdatoen"))), "a", _t("La identidad del análisis depende de entradas concretas y verificables.", "Analysis identity depends on concrete verifiable inputs.", "Analysens identitet afhænger af konkrete verificerbare input.")),
        _mcq("q02", _t("¿Qué determina replicación biológica?", "What determines biological replication?", "Hvad bestemmer biologisk replikation?"), (_option("a", _t("Número de muestras independientes", "Number of independent samples", "Antal uafhængige prøver")), _option("b", _t("Número de genes", "Number of genes", "Antal gener")), _option("c", _t("Número de colores", "Number of colors", "Antal farver")), _option("d", _t("Tamaño del archivo", "File size", "Filstørrelse"))), "a", _t("Features repetidas dentro de una muestra no son réplicas independientes.", "Repeated features within a sample are not independent replicates.", "Gentagne features i en prøve er ikke uafhængige replikater.")),
        _mcq("q03", _t("¿Qué entrada requiere un modelo de conteo RNA-seq estándar?", "What input does a standard RNA-seq count model require?", "Hvilket input kræver en standard RNA-seq-count-model?"), (_option("a", _t("Conteos compatibles y metadata alineada", "Compatible counts and aligned metadata", "Kompatible counts og afstemt metadata")), _option("b", _t("Z-scores como conteos", "Z-scores as counts", "Z-scores som counts")), _option("c", _t("Sólo fold changes", "Only fold changes", "Kun fold changes")), _option("d", _t("Capturas de pantalla", "Screenshots", "Screenshots"))), "a", _t("El contrato del modelo incluye escala de entrada y diseño.", "The model contract includes input scale and design.", "Modelkontrakten omfatter inputskala og design.")),
        _mcq("q04", _t("¿Qué nivel puede ser una feature proteómica?", "Which level may be a proteomics feature?", "Hvilket niveau kan være en proteomik-feature?"), (_option("a", _t("Precursor, péptido o proteína", "Precursor, peptide, or protein", "Precursor, peptid eller protein")), _option("b", _t("Sólo gen", "Only gene", "Kun gen")), _option("c", _t("Sólo paciente", "Only patient", "Kun patient")), _option("d", _t("Sólo pathway", "Only pathway", "Kun pathway"))), "a", _t("El nivel debe declararse y conservar su mapeo.", "The level must be declared and its mapping retained.", "Niveauet skal deklareres og dets mapping bevares.")),
        _mcq("q05", _t("¿Por qué no imputar siempre un valor pequeño?", "Why not always impute a small value?", "Hvorfor ikke altid imputere en lille værdi?"), (_option("a", _t("Puede introducir sesgo cuando missingness depende de intensidad o grupo", "It may introduce bias when missingness depends on intensity or group", "Det kan introducere bias, når missingness afhænger af intensitet eller gruppe")), _option("b", _t("Porque R no acepta números", "Because R rejects numbers", "Fordi R afviser tal")), _option("c", _t("Porque elimina metadata", "Because it removes metadata", "Fordi det fjerner metadata")), _option("d", _t("Porque aumenta filas", "Because it adds rows", "Fordi det tilføjer rækker"))), "a", _t("El mecanismo de no detección afecta la inferencia.", "The nondetection mechanism affects inference.", "Ikke-detekteringsmekanismen påvirker inferens.")),
        _mcq("q06", _t("¿Qué debe registrar cada transición?", "What should each transition record?", "Hvad bør hver overgang registrere?"), (_option("a", _t("Dimensiones, IDs, tipos y missingness", "Dimensions, IDs, types, and missingness", "Dimensioner, ID'er, typer og missingness")), _option("b", _t("Sólo tiempo", "Only time", "Kun tid")), _option("c", _t("Sólo valor p", "Only p-value", "Kun p-værdi")), _option("d", _t("Sólo memoria", "Only memory", "Kun hukommelse"))), "a", _t("Los controles detectan transformaciones o pérdidas inesperadas.", "Checks detect unexpected transformations or losses.", "Kontroller opdager uventede transformationer eller tab.")),
        _mcq("q07", _t("¿Qué contiene un dataset card?", "What does a dataset card contain?", "Hvad indeholder et datasetkort?"), (_option("a", _t("Diseño, unidades, procedencia, variables y límites", "Design, units, provenance, variables, and limits", "Design, enheder, proveniens, variable og grænser")), _option("b", _t("Sólo autor", "Only author", "Kun forfatter")), _option("c", _t("Sólo licencia", "Only license", "Kun licens")), _option("d", _t("Sólo tabla final", "Only final table", "Kun den endelige tabel"))), "a", _t("La tarjeta contextualiza qué puede sostener el dataset.", "The card contextualizes what the dataset can support.", "Kortet kontekstualiserer hvad datasættet kan understøtte.")),
        _mcq("q08", _t("¿Qué limita la conclusión final?", "What limits the final conclusion?", "Hvad begrænser den endelige konklusion?"), (_option("a", _t("Diseño y población representada", "Design and represented population", "Design og repræsenteret population")), _option("b", _t("Resolución de pantalla", "Screen resolution", "Skærmopløsning")), _option("c", _t("Nombre del paquete", "Package name", "Pakkenavn")), _option("d", _t("Cantidad de código", "Amount of code", "Mængde kode"))), "a", _t("Reproducibilidad técnica no amplía el alcance del diseño.", "Technical reproducibility does not expand design scope.", "Teknisk reproducerbarhed udvider ikke designets rækkevidde.")),
    ),
    true_false=(
        _tf("tf01", _t("Un accession identifica automáticamente los archivos exactos analizados.", "An accession automatically identifies the exact analyzed files.", "En accession identificerer automatisk de præcise analyserede filer."), False, _t("Debe registrarse la selección y snapshot local.", "Selection and local snapshot must be recorded.", "Selektion og lokalt snapshot skal registreres.")),
        _tf("tf02", _t("Los archivos fuente deben permanecer inmutables.", "Source files should remain immutable.", "Kildefiler bør forblive uforanderlige."), True, _t("Los cambios producen nuevos artefactos derivados.", "Changes produce new derived artifacts.", "Ændringer producerer nye afledte artefakter.")),
        _tf("tf03", _t("Miles de genes equivalen a miles de réplicas.", "Thousands of genes equal thousands of replicates.", "Tusindvis af gener svarer til tusindvis af replikater."), False, _t("La muestra biológica es la unidad independiente.", "The biological sample is the independent unit.", "Den biologiske prøve er den uafhængige enhed.")),
        _tf("tf04", _t("La transformación exploratoria siempre es entrada válida para un modelo de conteo.", "An exploratory transformation is always valid input for a count model.", "En eksplorativ transformation er altid gyldigt input til en count-model."), False, _t("Cada método define una escala de entrada.", "Every method defines an input scale.", "Hver metode definerer en inputskala.")),
        _tf("tf05", _t("Proteomics missingness puede depender de intensidad.", "Proteomics missingness may depend on intensity.", "Proteomisk missingness kan afhænge af intensitet."), True, _t("La no detección forma parte del proceso de medida.", "Nondetection is part of measurement.", "Ikke-detektion er del af målingen.")),
        _tf("tf06", _t("El mapeo péptido–proteína debe conservarse.", "Peptide–protein mapping should be retained.", "Peptid–protein-mapping bør bevares."), True, _t("La agregación cambia la unidad y la incertidumbre.", "Aggregation changes unit and uncertainty.", "Aggregering ændrer enhed og usikkerhed.")),
        _tf("tf07", _t("Un pipeline reproducible puede seguir siendo científicamente inválido.", "A reproducible pipeline may still be scientifically invalid.", "En reproducerbar pipeline kan stadig være videnskabeligt ugyldig."), True, _t("Reproducibilidad no corrige un diseño inadecuado.", "Reproducibility does not repair an inadequate design.", "Reproducerbarhed reparerer ikke et utilstrækkeligt design.")),
        _tf("tf08", _t("Session information ayuda a reconstruir el entorno.", "Session information helps reconstruct the environment.", "Session information hjælper med at rekonstruere miljøet."), True, _t("Registra versiones de R y paquetes.", "It records R and package versions.", "Det registrerer R- og pakkeversioner.")),
    ),
    tutor=(
        _t("El tutor debe mantener separados fuente pública, snapshot local, matriz analítica, modelo y afirmación. Debe exigir unidades, versiones, checksums, metadata, controles de transición y límites.", "The tutor must keep public source, local snapshot, analytical matrix, model, and claim separate. It should require units, versions, checksums, metadata, transition checks, and limits.", "Tutoren skal holde offentlig kilde, lokalt snapshot, analytisk matrix, model og påstand adskilt. Den bør kræve enheder, versioner, checksums, metadata, overgangskontroller og grænser."),
        (
            _t("Airway y PXD000001 son fuentes registradas, no datos embebidos.", "Airway and PXD000001 are registered sources, not embedded data.", "Airway og PXD000001 er registrerede kilder, ikke indlejrede data."),
            _t("RNA-seq y proteómica requieren contratos de entrada diferentes.", "RNA-seq and proteomics require different input contracts.", "RNA-seq og proteomik kræver forskellige inputkontrakter."),
            _t("Missingness proteómica requiere análisis del mecanismo.", "Proteomics missingness requires mechanism analysis.", "Proteomisk missingness kræver analyse af mekanismen."),
            _t("Cada transición produce evidencia auditable.", "Every transition produces auditable evidence.", "Hver overgang producerer auditérbar evidens."),
        ),
        (
            _t("Tratar latest como versión fija.", "Treat latest as a fixed version.", "Behandl latest som en fast version."),
            _t("Confundir features con réplicas.", "Confuse features with replicates.", "Forveksl features med replikater."),
            _t("Imputar sin estudiar missingness.", "Impute without studying missingness.", "Imputér uden at undersøge missingness."),
            _t("Omitir archivos intermedios y decisiones.", "Omit intermediate files and decisions.", "Udelad mellemprodukter og beslutninger."),
        ),
        (
            _t("¿Qué archivos exactos forman el snapshot?", "Which exact files form the snapshot?", "Hvilke præcise filer udgør snapshottet?"),
            _t("¿Cuál es la unidad en cada tabla?", "What is the unit in each table?", "Hvad er enheden i hver tabel?"),
            _t("¿Qué mecanismo de missingness es plausible?", "Which missingness mechanism is plausible?", "Hvilken missingness-mekanisme er plausibel?"),
            _t("¿Qué controles prueban cada transición?", "Which checks verify every transition?", "Hvilke kontroller verificerer hver overgang?"),
        ),
        (
            _t("Fija fuente y snapshot.", "Fixes source and snapshot.", "Fastlægger kilde og snapshot."),
            _t("Declara unidades y diseño.", "Declares units and design.", "Deklarerer enheder og design."),
            _t("Adapta QC y modelo a modalidad.", "Adapts QC and model to modality.", "Tilpasser QC og model til modalitet."),
            _t("Conserva artefactos y límites.", "Retains artifacts and limits.", "Bevarer artefakter og grænser."),
        ),
        (
            _t("No afirmar que los datos públicos están incluidos en la aplicación.", "Do not claim public data are bundled in the application.", "Påstå ikke at offentlige data er inkluderet i applikationen."),
            _t("No inventar archivos, muestras o resultados de una fuente.", "Do not invent files, samples, or results from a source.", "Opfind ikke filer, prøver eller resultater fra en kilde."),
            _t("No equiparar reproducibilidad con validez.", "Do not equate reproducibility with validity.", "Sidestil ikke reproducerbarhed med validitet."),
            _t("Responder en el idioma activo y conservar identificadores.", "Respond in the active language and preserve identifiers.", "Svar på det aktive sprog og bevar identifikatorer."),
        ),
        (
            "https://bioconductor.org/packages/release/data/experiment/html/airway.html",
            "https://bioconductor.org/packages/release/bioc/html/rpx.html",
            "https://bioconductor.org/packages/release/bioc/html/limpa.html",
        ),
    ),
)

LOCALIZED_MODULE_06_PUBLIC_OMICS_WORKFLOWS = build_module(_SPEC)
LOCALIZED_OBJECTIVE_QUESTION_BANK_06 = build_question_bank(_SPEC)


def materialize_module_06_question_bank(
    locale: AppLocale | str = AppLocale.SPANISH_SPAIN,
) -> tuple[AssessmentItem, ...]:
    """Materialize the stable module 6 objective bank."""

    return materialize_bank(LOCALIZED_OBJECTIVE_QUESTION_BANK_06, locale)


MODULE_06_PUBLIC_OMICS_WORKFLOWS: LearningModule = (
    LOCALIZED_MODULE_06_PUBLIC_OMICS_WORKFLOWS.materialize(AppLocale.SPANISH_SPAIN)
)
OBJECTIVE_QUESTION_BANK_06 = materialize_module_06_question_bank()

__all__ = [
    "LOCALIZED_MODULE_06_PUBLIC_OMICS_WORKFLOWS",
    "LOCALIZED_OBJECTIVE_QUESTION_BANK_06",
    "MODULE_06_PUBLIC_OMICS_WORKFLOWS",
    "OBJECTIVE_QUESTION_BANK_06",
    "materialize_module_06_question_bank",
]
