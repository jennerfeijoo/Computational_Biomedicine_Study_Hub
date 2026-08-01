"""BMB831 module 5: advanced statistical and omics visualization."""

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
    module_id="bmb831.m05",
    title=_t(
        "Visualización avanzada, incertidumbre y comunicación reproducible",
        "Advanced visualization, uncertainty, and reproducible communication",
        "Avanceret visualisering, usikkerhed og reproducerbar kommunikation",
    ),
    summary=_t(
        "Diseña figuras que respondan una pregunta explícita, representen escala e incertidumbre correctamente y mantengan trazabilidad entre datos, transformación, selección, anotación y exportación.",
        "Design figures that answer an explicit question, represent scale and uncertainty correctly, and preserve traceability among data, transformation, selection, annotation, and export.",
        "Design figurer, der besvarer et eksplicit spørgsmål, repræsenterer skala og usikkerhed korrekt og bevarer sporbarhed mellem data, transformation, selektion, annotering og eksport.",
    ),
    objectives=(
        (
            "m05.o1",
            _t(
                "Definir el contrato de una figura: pregunta, unidad, variables, transformación, comparación y audiencia.",
                "Define a figure contract: question, unit, variables, transformation, comparison, and audience.",
                "Definere en figurkontrakt: spørgsmål, enhed, variable, transformation, sammenligning og publikum.",
            ),
        ),
        (
            "m05.o2",
            _t(
                "Construir visualizaciones de QC, resultados diferenciales y estructura multivariante sin distorsionar magnitud o incertidumbre.",
                "Construct QC, differential-result, and multivariate visualizations without distorting magnitude or uncertainty.",
                "Konstruere QC-, differential- og multivariate visualiseringer uden at forvrænge størrelse eller usikkerhed.",
            ),
        ),
        (
            "m05.o3",
            _t(
                "Diseñar heatmaps y anotaciones con orden, distancia, escala y selección declarados.",
                "Design heatmaps and annotations with declared ordering, distance, scale, and selection.",
                "Designe heatmaps og annoteringer med deklareret rækkefølge, afstand, skala og selektion.",
            ),
        ),
        (
            "m05.o4",
            _t(
                "Exportar figuras reproducibles, accesibles y auditables con datos y parámetros asociados.",
                "Export reproducible, accessible, and auditable figures with associated data and parameters.",
                "Eksportere reproducerbare, tilgængelige og auditérbare figurer med tilknyttede data og parametre.",
            ),
        ),
    ),
    concepts=(
        (
            "figure-contract",
            _t(
                "Contrato de figura y evidencia",
                "Figure and evidence contract",
                "Figur- og evidenskontrakt",
            ),
            _t(
                "Una figura científica comienza con una pregunta y una unidad analítica, no con un tipo de gráfico. Debe declarar qué representa cada punto, qué resumen se muestra, qué transformación se aplicó y qué comparación pretende sostener. Una figura exploratoria ayuda a generar preguntas; una inferencial comunica un estimando y su incertidumbre. Mezclar ambos propósitos favorece sobreinterpretación.",
                "A scientific figure begins with a question and analytical unit, not a chart type. It should declare what each mark represents, which summary is shown, what transformation was applied, and which comparison it supports. An exploratory figure helps generate questions; an inferential figure communicates an estimand and uncertainty. Mixing these purposes encourages overinterpretation.",
                "En videnskabelig figur begynder med et spørgsmål og en analytisk enhed, ikke en diagramtype. Den bør deklarere hvad hvert mærke repræsenterer, hvilket resume der vises, hvilken transformation der er anvendt, og hvilken sammenligning den understøtter. En eksplorativ figur hjælper med at generere spørgsmål; en inferentiel figur kommunikerer et estimand og usikkerhed. Sammenblanding fremmer overfortolkning.",
            ),
            (
                _t(
                    "Incluye unidad, denominador y escala en el pie de figura.",
                    "Include unit, denominator, and scale in the caption.",
                    "Medtag enhed, denominator og skala i figurteksten.",
                ),
                _t(
                    "Conserva el dataset usado para dibujar cada marca.",
                    "Retain the plotting dataset used for every mark.",
                    "Bevar plotting-datasættet, der bruges til hvert mærke.",
                ),
            ),
        ),
        (
            "differential-figures",
            _t("MA, volcano y magnitud", "MA, volcano, and magnitude", "MA, volcano og størrelse"),
            _t(
                "Un MA plot relaciona efecto con abundancia media y permite detectar dependencia de precisión o sesgo con la intensidad. Un volcano combina magnitud y evidencia, pero no sustituye intervalos, abundancia ni tabla completa. Los puntos destacados deben seguir reglas predefinidas que integren control de multiplicidad y magnitud mínima; etiquetar sólo resultados favorables puede convertir una figura en selección post hoc.",
                "An MA plot relates effect to mean abundance and helps detect precision dependence or intensity-related bias. A volcano plot combines magnitude and evidence but does not replace intervals, abundance, or the complete table. Highlighted points should follow predefined rules integrating multiplicity control and minimum magnitude; labeling only favorable results can turn a figure into post-hoc selection.",
                "Et MA-plot relaterer effekt til middelabundans og hjælper med at opdage præcisionsafhængighed eller intensitetsrelateret bias. Et volcano-plot kombinerer størrelse og evidens, men erstatter ikke intervaller, abundans eller hele tabellen. Fremhævede punkter bør følge foruddefinerede regler, der integrerer multiplicitetskontrol og minimumsstørrelse; labels kun på fordelagtige resultater kan gøre figuren til post-hoc-selektion.",
            ),
            (
                _t(
                    "Representa no significativos y faltantes explícitamente.",
                    "Represent nonsignificant and missing results explicitly.",
                    "Repræsentér ikke-signifikante og manglende resultater eksplicit.",
                ),
                _t(
                    "Evita interpretar -log10(p) como tamaño del efecto.",
                    "Do not interpret -log10(p) as effect size.",
                    "Fortolk ikke -log10(p) som effektstørrelse.",
                ),
            ),
        ),
        (
            "heatmaps",
            _t(
                "Heatmaps, orden y anotación",
                "Heatmaps, ordering, and annotation",
                "Heatmaps, rækkefølge og annotering",
            ),
            _t(
                "Un heatmap depende de la matriz seleccionada, transformación, escalado por fila o columna, distancia y algoritmo de ordenamiento. El color muestra valores relativos bajo esa escala; no convierte filas en significativas. Las anotaciones de grupo, lote y calidad deben estar alineadas con columnas y utilizar codificaciones accesibles. Seleccionar genes por el mismo outcome que colorea columnas debe describirse como visualización supervisada.",
                "A heatmap depends on the selected matrix, transformation, row or column scaling, distance, and ordering algorithm. Color shows relative values under that scale; it does not make rows significant. Group, batch, and quality annotations must align with columns and use accessible encodings. Selecting genes by the same outcome used to color columns should be described as supervised visualization.",
                "Et heatmap afhænger af den valgte matrix, transformation, række- eller kolonneskalering, afstand og sorteringsalgoritme. Farve viser relative værdier under denne skala; den gør ikke rækker signifikante. Gruppe-, batch- og kvalitetsannoteringer skal følge kolonnerne og bruge tilgængelige kodninger. Valg af gener efter samme outcome, som farver kolonnerne, bør beskrives som superviseret visualisering.",
            ),
            (
                _t(
                    "Registra qué filas fueron seleccionadas y por qué.",
                    "Record which rows were selected and why.",
                    "Registrér hvilke rækker der blev valgt og hvorfor.",
                ),
                _t(
                    "No ocultes anotaciones técnicas que explican la estructura.",
                    "Do not hide technical annotations that explain structure.",
                    "Skjul ikke tekniske annoteringer, der forklarer struktur.",
                ),
            ),
        ),
        (
            "uncertainty-export",
            _t(
                "Incertidumbre, accesibilidad y exportación",
                "Uncertainty, accessibility, and export",
                "Usikkerhed, tilgængelighed og eksport",
            ),
            _t(
                "La incertidumbre puede mostrarse con intervalos, distribuciones, puntos individuales o bandas, según el estimando. El color no debe ser el único canal para distinguir categorías; formas, etiquetas o facetas mejoran accesibilidad. La exportación reproducible fija dimensiones, unidades, dispositivo, tipografía y versión del script. El artefacto final debe poder regenerarse desde datos derivados versionados, no mediante edición manual invisible.",
                "Uncertainty may be shown through intervals, distributions, individual points, or bands depending on the estimand. Color should not be the only channel distinguishing categories; shapes, labels, or facets improve accessibility. Reproducible export fixes dimensions, units, device, typography, and script version. The final artifact should be regenerable from versioned derived data rather than invisible manual editing.",
                "Usikkerhed kan vises med intervaller, fordelinger, individuelle punkter eller bånd afhængigt af estimand. Farve bør ikke være den eneste kanal til at skelne kategorier; former, labels eller facetter forbedrer tilgængelighed. Reproducerbar eksport fastlægger dimensioner, enheder, device, typografi og scriptversion. Det endelige artefakt bør kunne regenereres fra versionerede afledte data frem for usynlig manuel redigering.",
            ),
            (
                _t(
                    "Usa formatos vectoriales para figuras que deban escalarse.",
                    "Use vector formats for figures that must scale.",
                    "Brug vektorformater til figurer, der skal skaleres.",
                ),
                _t(
                    "Versiona también los datos resumidos usados por la figura.",
                    "Version the summarized plotting data as well.",
                    "Versionér også de opsummerede plotting-data.",
                ),
            ),
        ),
    ),
    examples=(
        (
            "m05.e01",
            _t(
                "Preparar una selección reproducible para volcano",
                "Prepare a reproducible volcano selection",
                "Forbered en reproducerbar volcano-selektion",
            ),
            _t(
                "Calcula coordenadas y reglas de resaltado sin ocultar la tabla completa.",
                "Calculate coordinates and highlighting rules without hiding the complete table.",
                "Beregn koordinater og fremhævningsregler uden at skjule hele tabellen.",
            ),
            (
                _t(
                    "El eje x usa log2 fold change.",
                    "The x-axis uses log2 fold change.",
                    "X-aksen bruger log2 fold change.",
                ),
                _t(
                    "El eje y usa -log10 del valor ajustado.",
                    "The y-axis uses -log10 of the adjusted value.",
                    "Y-aksen bruger -log10 af den justerede værdi.",
                ),
                _t(
                    "La selección combina FDR y magnitud.",
                    "Selection combines FDR and magnitude.",
                    "Selektionen kombinerer FDR og størrelse.",
                ),
            ),
            """result <- data.frame(
  gene = paste0("G", 1:5),
  log2fc = c(2.0, -1.4, 0.7, 1.5, 0.1),
  padj = c(0.001, 0.020, 0.030, 0.200, 0.900)
)
result$minus_log10_padj <- -log10(result$padj)
result$highlight <- result$padj < 0.05 & abs(result$log2fc) >= 1
plot(result$log2fc, result$minus_log10_padj, pch = ifelse(result$highlight, 19, 1))
cat("highlighted=", paste(result$gene[result$highlight], collapse = ","), sep = "")
""",
            "highlighted=G1,G2",
            _t(
                "La regla identifica G1 y G2. Todos los puntos permanecen visibles y el criterio puede reconstruirse desde la tabla.",
                "The rule identifies G1 and G2. All points remain visible, and the criterion can be reconstructed from the table.",
                "Reglen identificerer G1 og G2. Alle punkter forbliver synlige, og kriteriet kan rekonstrueres fra tabellen.",
            ),
        ),
        (
            "m05.e02",
            _t(
                "Alinear anotaciones de un heatmap",
                "Align heatmap annotations",
                "Afstem heatmap-annoteringer",
            ),
            _t(
                "Ordena una matriz por clustering y comprueba que la metadata siga exactamente el nuevo orden.",
                "Order a matrix by clustering and verify that metadata follows the new order exactly.",
                "Sortér en matrix efter clustering og kontrollér at metadata følger den nye rækkefølge præcist.",
            ),
            (
                _t("Las muestras son columnas.", "Samples are columns.", "Prøver er kolonner."),
                _t(
                    "El clustering devuelve un orden de columnas.",
                    "Clustering returns a column order.",
                    "Clustering returnerer en kolonnerækkefølge.",
                ),
                _t(
                    "Metadata se reordena por match y se verifica.",
                    "Metadata is reordered by match and verified.",
                    "Metadata omordnes med match og verificeres.",
                ),
            ),
            """x <- matrix(
  c(0, 0.2, 5, 5.1,
    1, 1.1, 6, 6.2,
    2, 2.1, 7, 7.1),
  nrow = 3,
  byrow = TRUE,
  dimnames = list(paste0("F", 1:3), paste0("S", 1:4))
)
metadata <- data.frame(sample_id = c("S3", "S1", "S4", "S2"), group = c("B", "A", "B", "A"))
order_index <- hclust(dist(t(x)))$order
ordered_ids <- colnames(x)[order_index]
metadata_ordered <- metadata[match(ordered_ids, metadata$sample_id), ]
stopifnot(identical(ordered_ids, metadata_ordered$sample_id))
cat("aligned=TRUE\n")
cat("first_pair_same_group=", metadata_ordered$group[1] == metadata_ordered$group[2], sep = "")
""",
            """aligned=TRUE
first_pair_same_group=TRUE""",
            _t(
                "La comprobación impide asociar colores de anotación a muestras equivocadas después del clustering.",
                "The check prevents annotation colors from being assigned to the wrong samples after clustering.",
                "Kontrollen forhindrer at annoteringsfarver tildeles forkerte prøver efter clustering.",
            ),
        ),
    ),
    practices=(
        (
            "m05.p01",
            "PIPELINE_DESIGN",
            _t(
                "Diseña el contrato de una figura para comparar expresión diferencial entre tratamiento y control.",
                "Design the contract for a figure comparing differential expression between treatment and control.",
                "Design kontrakten for en figur, der sammenligner differential ekspression mellem behandling og kontrol.",
            ),
            (
                _t(
                    "Incluye unidad, estimando, escala y selección.",
                    "Include unit, estimand, scale, and selection.",
                    "Medtag enhed, estimand, skala og selektion.",
                ),
                _t(
                    "Distingue exploración e inferencia.",
                    "Separate exploration and inference.",
                    "Adskil udforskning og inferens.",
                ),
            ),
            _t(
                "Unidad: gen dentro de muestras elegibles. Estimando: log2 fold change tratamiento-control ajustado por lote. Ejes: efecto y evidencia ajustada o abundancia media. Selección: FDR y magnitud declarados. La tabla completa y los intervalos acompañan la figura; el pie declara transformación, modelo y población.",
                "Unit: gene within eligible samples. Estimand: batch-adjusted treatment-control log2 fold change. Axes: effect and adjusted evidence or mean abundance. Selection: declared FDR and magnitude. The complete table and intervals accompany the figure; the caption states transformation, model, and population.",
                "Enhed: gen i kvalificerede prøver. Estimand: batchjusteret treatment-control log2 fold change. Akser: effekt og justeret evidens eller middelabundans. Selektion: deklareret FDR og størrelse. Hele tabellen og intervaller ledsager figuren; figurteksten angiver transformation, model og population.",
            ),
            _t(
                "El contrato conecta cada elemento visual con una afirmación verificable.",
                "The contract connects every visual element to a verifiable claim.",
                "Kontrakten forbinder hvert visuelt element med en verificerbar påstand.",
            ),
            "",
        ),
        (
            "m05.p02",
            "DATA_INTERPRETATION",
            _t(
                "Un volcano muestra muchos puntos con -log10(padj) alto pero efectos cercanos a cero. Interprétalo.",
                "A volcano plot shows many points with high -log10(padj) but effects near zero. Interpret it.",
                "Et volcano-plot viser mange punkter med høj -log10(padj), men effekter tæt på nul. Fortolk det.",
            ),
            (
                _t(
                    "No confundas evidencia con magnitud.",
                    "Do not confuse evidence with magnitude.",
                    "Forveksl ikke evidens med størrelse.",
                ),
                _t(
                    "Considera tamaño muestral y precisión.",
                    "Consider sample size and precision.",
                    "Overvej stikprøvestørrelse og præcision.",
                ),
            ),
            _t(
                "Existe evidencia estadística precisa para diferencias pequeñas, posiblemente favorecida por tamaño muestral o baja variabilidad. La relevancia requiere umbral de efecto, intervalos, abundancia basal y contexto. El eje vertical no demuestra importancia biológica.",
                "There is precise statistical evidence for small differences, possibly favored by sample size or low variability. Relevance requires an effect threshold, intervals, baseline abundance, and context. The vertical axis does not demonstrate biological importance.",
                "Der er præcis statistisk evidens for små forskelle, muligvis hjulpet af stikprøvestørrelse eller lav variation. Relevans kræver effekttærskel, intervaller, basisabundans og kontekst. Den lodrette akse demonstrerer ikke biologisk betydning.",
            ),
            _t(
                "La figura debe leerse junto con magnitud, precisión y pregunta aplicada.",
                "The figure must be read together with magnitude, precision, and applied question.",
                "Figuren skal læses sammen med størrelse, præcision og det anvendte spørgsmål.",
            ),
            "",
        ),
        (
            "m05.p03",
            "DEBUGGING",
            _t(
                "Un heatmap cambia el orden de columnas, pero la barra de lote conserva el orden original. Reconstruye el error.",
                "A heatmap changes column order, but the batch bar retains the original order. Reconstruct the error.",
                "Et heatmap ændrer kolonnerækkefølgen, men batchbjælken bevarer den oprindelige rækkefølge. Rekonstruér fejlen.",
            ),
            (
                _t(
                    "La anotación debe indexarse por ID.",
                    "Annotation must be indexed by ID.",
                    "Annoteringen skal indekseres efter ID.",
                ),
                _t(
                    "Comprueba identidad después de reordenar.",
                    "Check identity after reordering.",
                    "Kontrollér identitet efter omordning.",
                ),
            ),
            _t(
                "Los colores de lote quedaron asociados por posición y ya no corresponden a las muestras. Debe obtenerse ordered_ids del heatmap, reordenar metadata mediante match o nombres y verificar identical(ordered_ids, metadata_ordered$sample_id) antes de dibujar.",
                "Batch colors remained positionally associated and no longer correspond to samples. Obtain ordered_ids from the heatmap, reorder metadata by match or names, and verify identical(ordered_ids, metadata_ordered$sample_id) before plotting.",
                "Batchfarver forblev positionelt forbundet og svarer ikke længere til prøverne. Hent ordered_ids fra heatmappet, omordn metadata med match eller navne, og verificér identical(ordered_ids, metadata_ordered$sample_id) før plotting.",
            ),
            _t(
                "La alineación visual es una relación de claves, no una suposición posicional.",
                "Visual alignment is a key relationship, not a positional assumption.",
                "Visuel afstemning er en nøglerelation, ikke en positionsantagelse.",
            ),
            "",
        ),
        (
            "m05.p04",
            "SHORT_ANSWER",
            _t(
                "Explica por qué un heatmap de genes seleccionados por el outcome es supervisado aunque use clustering no supervisado.",
                "Explain why a heatmap of genes selected by outcome is supervised even when it uses unsupervised clustering.",
                "Forklar hvorfor et heatmap af gener valgt efter outcome er superviseret, selv når det bruger usuperviseret clustering.",
            ),
            (
                _t(
                    "La selección define el espacio mostrado.",
                    "Selection defines the displayed space.",
                    "Selektionen definerer det viste rum.",
                ),
                _t(
                    "Considera fuga y validación.",
                    "Consider leakage and validation.",
                    "Overvej leakage og validering.",
                ),
            ),
            _t(
                "Las etiquetas influyeron en qué filas entraron al heatmap, por lo que la estructura ya está condicionada al outcome. El clustering posterior no elimina esa supervisión. Para inferencia o predicción, la selección debe realizarse dentro de training; para descripción, debe declararse explícitamente.",
                "Labels influenced which rows entered the heatmap, so the structure is already conditioned on outcome. Later clustering does not remove that supervision. For inference or prediction, selection must occur within training; for description, it must be declared explicitly.",
                "Labels påvirkede hvilke rækker der kom i heatmappet, så strukturen er allerede betinget af outcome. Efterfølgende clustering fjerner ikke denne supervision. Til inferens eller prædiktion skal selektionen ske inden for training; til beskrivelse skal den deklareres eksplicit.",
            ),
            _t(
                "No supervisado describe el algoritmo de ordenamiento, no todo el pipeline.",
                "Unsupervised describes the ordering algorithm, not the entire pipeline.",
                "Usuperviseret beskriver sorteringsalgoritmen, ikke hele pipelinen.",
            ),
            "",
        ),
        (
            "m05.p05",
            "CODE_COMPLETION",
            _t(
                "Completa una función que añada coordenada y y una regla de resaltado a una tabla diferencial.",
                "Complete a function that adds a y-coordinate and highlighting rule to a differential table.",
                "Færdiggør en funktion, der tilføjer y-koordinat og fremhævningsregel til en differential tabel.",
            ),
            (
                _t("Usa -log10(padj).", "Use -log10(padj).", "Brug -log10(padj)."),
                _t(
                    "Combina alpha y min_effect.",
                    "Combine alpha and min_effect.",
                    "Kombinér alpha og min_effect.",
                ),
            ),
            _t(
                "prepare_volcano <- function(tab, alpha = 0.05, min_effect = 1) { tab$y <- -log10(tab$padj); tab$highlight <- tab$padj < alpha & abs(tab$log2fc) >= min_effect; tab }",
                "prepare_volcano <- function(tab, alpha = 0.05, min_effect = 1) { tab$y <- -log10(tab$padj); tab$highlight <- tab$padj < alpha & abs(tab$log2fc) >= min_effect; tab }",
                "prepare_volcano <- function(tab, alpha = 0.05, min_effect = 1) { tab$y <- -log10(tab$padj); tab$highlight <- tab$padj < alpha & abs(tab$log2fc) >= min_effect; tab }",
            ),
            _t(
                "La función conserva la tabla completa y hace explícita la regla visual.",
                "The function retains the complete table and makes the visual rule explicit.",
                "Funktionen bevarer hele tabellen og gør den visuelle regel eksplicit.",
            ),
            "prepare_volcano <- function(tab, alpha = 0.05, min_effect = 1) {\n  # add y and highlight columns\n}",
        ),
        (
            "m05.p06",
            "ORAL_EXPLANATION",
            _t(
                "Prepara una explicación de 90 segundos: ¿qué hace que una figura sea reproducible y no sólo bonita?",
                "Prepare a 90-second explanation: what makes a figure reproducible rather than merely attractive?",
                "Forbered en 90-sekunders forklaring: hvad gør en figur reproducerbar frem for blot attraktiv?",
            ),
            (
                _t(
                    "Incluye datos, parámetros y exportación.",
                    "Include data, parameters, and export.",
                    "Medtag data, parametre og eksport.",
                ),
                _t(
                    "Incluye trazabilidad de selección.",
                    "Include selection traceability.",
                    "Medtag sporbarhed af selektion.",
                ),
            ),
            _t(
                "Una figura reproducible se genera por código desde datos fuente o derivados versionados, con reglas de filtrado, transformación, orden, escalas, etiquetas y dimensiones declaradas. Conserva la tabla de plotting, versiones y entorno; puede regenerarse sin edición manual oculta y produce el mismo mensaje científico bajo el mismo contrato.",
                "A reproducible figure is generated by code from versioned source or derived data, with declared filtering, transformation, ordering, scales, labels, and dimensions. It retains the plotting table, versions, and environment; it can be regenerated without hidden manual editing and produces the same scientific message under the same contract.",
                "En reproducerbar figur genereres med kode fra versionerede kilde- eller afledte data med deklareret filtrering, transformation, rækkefølge, skalaer, labels og dimensioner. Den bevarer plotting-tabellen, versioner og miljø; den kan regenereres uden skjult manuel redigering og giver samme videnskabelige budskab under samme kontrakt.",
            ),
            _t(
                "La estética está subordinada a evidencia, claridad y trazabilidad.",
                "Aesthetics is subordinate to evidence, clarity, and traceability.",
                "Æstetik er underordnet evidens, klarhed og sporbarhed.",
            ),
            "",
        ),
    ),
    mcqs=(
        _mcq(
            "q01",
            _t(
                "¿Cuál es el primer elemento de un contrato de figura?",
                "What is the first element of a figure contract?",
                "Hvad er det første element i en figurkontrakt?",
            ),
            (
                _option(
                    "a",
                    _t(
                        "Pregunta y unidad analítica",
                        "Question and analytical unit",
                        "Spørgsmål og analytisk enhed",
                    ),
                ),
                _option("b", _t("Paleta", "Palette", "Palette")),
                _option("c", _t("Fuente tipográfica", "Font", "Skrifttype")),
                _option("d", _t("Número de paneles", "Number of panels", "Antal paneler")),
            ),
            "a",
            _t(
                "La figura debe responder una pregunta sobre una unidad definida.",
                "A figure should answer a question about a defined unit.",
                "En figur bør besvare et spørgsmål om en defineret enhed.",
            ),
        ),
        _mcq(
            "q02",
            _t(
                "¿Qué muestra el eje y habitual de un volcano?",
                "What does the usual volcano y-axis show?",
                "Hvad viser den sædvanlige y-akse i et volcano-plot?",
            ),
            (
                _option(
                    "a",
                    _t(
                        "-log10 de una medida de evidencia",
                        "-log10 of an evidence measure",
                        "-log10 af et evidensmål",
                    ),
                ),
                _option("b", _t("Tamaño del efecto", "Effect size", "Effektstørrelse")),
                _option("c", _t("Abundancia cruda", "Raw abundance", "Rå abundans")),
                _option("d", _t("Número de muestras", "Sample count", "Antal prøver")),
            ),
            "a",
            _t(
                "La magnitud suele mostrarse en x; y representa evidencia transformada.",
                "Magnitude is usually shown on x; y represents transformed evidence.",
                "Størrelse vises normalt på x; y repræsenterer transformeret evidens.",
            ),
        ),
        _mcq(
            "q03",
            _t(
                "¿Qué añade un MA plot frente a un volcano?",
                "What does an MA plot add relative to a volcano?",
                "Hvad tilføjer et MA-plot i forhold til et volcano-plot?",
            ),
            (
                _option(
                    "a",
                    _t(
                        "Relación entre efecto y abundancia media",
                        "Relation between effect and mean abundance",
                        "Relation mellem effekt og middelabundans",
                    ),
                ),
                _option("b", _t("Causalidad", "Causality", "Kausalitet")),
                _option("c", _t("Identidad de pacientes", "Patient identity", "Patientidentitet")),
                _option("d", _t("Validación externa", "External validation", "Ekstern validering")),
            ),
            "a",
            _t(
                "Permite observar dependencia del efecto o precisión con intensidad.",
                "It reveals dependence of effect or precision on intensity.",
                "Det viser afhængighed af effekt eller præcision med intensitet.",
            ),
        ),
        _mcq(
            "q04",
            _t(
                "¿Qué debe determinar el resaltado de genes?",
                "What should determine gene highlighting?",
                "Hvad bør bestemme fremhævelse af gener?",
            ),
            (
                _option(
                    "a",
                    _t(
                        "Regla predefinida de FDR y magnitud",
                        "A predefined FDR and magnitude rule",
                        "En foruddefineret FDR- og størrelsesregel",
                    ),
                ),
                _option("b", _t("Preferencia visual", "Visual preference", "Visuel præference")),
                _option(
                    "c", _t("Sólo nombres conocidos", "Only familiar names", "Kun kendte navne")
                ),
                _option("d", _t("El color disponible", "Available color", "Tilgængelig farve")),
            ),
            "a",
            _t(
                "La selección debe ser reconstruible y no post hoc.",
                "Selection should be reconstructable and not post hoc.",
                "Selektionen bør kunne rekonstrueres og ikke være post hoc.",
            ),
        ),
        _mcq(
            "q05",
            _t(
                "¿Qué cambia un z-score por fila en un heatmap?",
                "What does row-wise z-scoring change in a heatmap?",
                "Hvad ændrer rækkevis z-score i et heatmap?",
            ),
            (
                _option(
                    "a",
                    _t(
                        "Muestra patrones relativos y elimina magnitud absoluta por fila",
                        "It shows relative patterns and removes absolute row magnitude",
                        "Det viser relative mønstre og fjerner absolut rækkestørrelse",
                    ),
                ),
                _option(
                    "b",
                    _t("Prueba significación", "It proves significance", "Det beviser signifikans"),
                ),
                _option("c", _t("Corrige lote", "It corrects batch", "Det korrigerer batch")),
                _option("d", _t("Aumenta muestras", "It increases samples", "Det øger prøver")),
            ),
            "a",
            _t(
                "Centrar y escalar cada fila cambia la interpretación a desviaciones relativas.",
                "Centering and scaling each row changes interpretation to relative deviations.",
                "Centrering og skalering af hver række ændrer fortolkningen til relative afvigelser.",
            ),
        ),
        _mcq(
            "q06",
            _t(
                "¿Cómo debe alinearse metadata con columnas ordenadas?",
                "How should metadata align with ordered columns?",
                "Hvordan bør metadata afstemmes med sorterede kolonner?",
            ),
            (
                _option(
                    "a",
                    _t(
                        "Por identificadores verificados",
                        "By verified identifiers",
                        "Med verificerede identifikatorer",
                    ),
                ),
                _option(
                    "b",
                    _t(
                        "Por posición original", "By original position", "Efter oprindelig position"
                    ),
                ),
                _option("c", _t("Al azar", "Randomly", "Tilfældigt")),
                _option("d", _t("Por color", "By color", "Efter farve")),
            ),
            "a",
            _t(
                "El orden visual debe propagarse mediante claves de muestra.",
                "Visual order should propagate through sample keys.",
                "Den visuelle rækkefølge bør propagere via prøvenøgler.",
            ),
        ),
        _mcq(
            "q07",
            _t(
                "¿Qué mejora accesibilidad además del color?",
                "What improves accessibility in addition to color?",
                "Hvad forbedrer tilgængelighed ud over farve?",
            ),
            (
                _option(
                    "a",
                    _t(
                        "Formas, etiquetas o facetas",
                        "Shapes, labels, or facets",
                        "Former, labels eller facetter",
                    ),
                ),
                _option("b", _t("Más saturación", "More saturation", "Mere mætning")),
                _option("c", _t("Menos contexto", "Less context", "Mindre kontekst")),
                _option("d", _t("Ejes dobles", "Dual axes", "Dobbelte akser")),
            ),
            "a",
            _t(
                "Canales redundantes permiten distinguir categorías sin depender sólo del color.",
                "Redundant channels distinguish categories without relying only on color.",
                "Redundante kanaler skelner kategorier uden kun at afhænge af farve.",
            ),
        ),
        _mcq(
            "q08",
            _t(
                "¿Qué artefacto debe versionarse junto con una figura?",
                "Which artifact should be versioned with a figure?",
                "Hvilket artefakt bør versioneres sammen med en figur?",
            ),
            (
                _option(
                    "a",
                    _t(
                        "La tabla de datos usada para dibujar",
                        "The plotting data table",
                        "Plotting-datatabellen",
                    ),
                ),
                _option("b", _t("Sólo una captura", "Only a screenshot", "Kun et screenshot")),
                _option("c", _t("Una edición manual", "A manual edit", "En manuel redigering")),
                _option("d", _t("Sólo el título", "Only the title", "Kun titlen")),
            ),
            "a",
            _t(
                "La tabla de plotting conecta el gráfico con datos y reglas.",
                "The plotting table connects the graph to data and rules.",
                "Plotting-tabellen forbinder grafen med data og regler.",
            ),
        ),
    ),
    true_false=(
        _tf(
            "tf01",
            _t(
                "Un gráfico bonito es reproducible si se guarda como imagen.",
                "An attractive plot is reproducible if saved as an image.",
                "Et attraktivt plot er reproducerbart, hvis det gemmes som billede.",
            ),
            False,
            _t(
                "Se necesitan datos, código, parámetros y entorno regenerable.",
                "Data, code, parameters, and a regenerable environment are needed.",
                "Data, kode, parametre og et regenererbart miljø er nødvendige.",
            ),
        ),
        _tf(
            "tf02",
            _t(
                "-log10(p) es una medida de tamaño del efecto.",
                "-log10(p) is an effect-size measure.",
                "-log10(p) er et mål for effektstørrelse.",
            ),
            False,
            _t(
                "Representa evidencia transformada, no magnitud.",
                "It represents transformed evidence, not magnitude.",
                "Det repræsenterer transformeret evidens, ikke størrelse.",
            ),
        ),
        _tf(
            "tf03",
            _t(
                "Un MA plot puede revelar dependencia con abundancia media.",
                "An MA plot can reveal dependence on mean abundance.",
                "Et MA-plot kan vise afhængighed af middelabundans.",
            ),
            True,
            _t(
                "Relaciona efecto y nivel medio.",
                "It relates effect and mean level.",
                "Det relaterer effekt og middelniveau.",
            ),
        ),
        _tf(
            "tf04",
            _t(
                "Escalar filas de un heatmap conserva magnitudes absolutas entre genes.",
                "Row scaling in a heatmap preserves absolute magnitudes among genes.",
                "Rækkeskalering i et heatmap bevarer absolutte størrelser mellem gener.",
            ),
            False,
            _t(
                "Convierte cada fila a desviaciones relativas.",
                "It converts each row to relative deviations.",
                "Det konverterer hver række til relative afvigelser.",
            ),
        ),
        _tf(
            "tf05",
            _t(
                "Seleccionar genes por outcome hace supervisado el espacio visual.",
                "Selecting genes by outcome makes the displayed space supervised.",
                "Valg af gener efter outcome gør det viste rum superviseret.",
            ),
            True,
            _t(
                "Las etiquetas determinaron qué variables se muestran.",
                "Labels determined which variables are shown.",
                "Labels bestemte hvilke variable der vises.",
            ),
        ),
        _tf(
            "tf06",
            _t(
                "Metadata puede conservar su orden original después de reordenar columnas.",
                "Metadata may keep its original order after columns are reordered.",
                "Metadata kan beholde sin oprindelige rækkefølge efter kolonner omordnes.",
            ),
            False,
            _t(
                "Debe seguir exactamente el orden de muestras mostrado.",
                "It must exactly follow the displayed sample order.",
                "Det skal præcist følge den viste prøverækkefølge.",
            ),
        ),
        _tf(
            "tf07",
            _t(
                "El color debe complementarse con otros canales cuando sea posible.",
                "Color should be complemented with other channels when possible.",
                "Farve bør suppleres med andre kanaler, når det er muligt.",
            ),
            True,
            _t(
                "Mejora accesibilidad y robustez de lectura.",
                "This improves accessibility and reading robustness.",
                "Det forbedrer tilgængelighed og robust læsning.",
            ),
        ),
        _tf(
            "tf08",
            _t(
                "Una figura inferencial debe comunicar incertidumbre.",
                "An inferential figure should communicate uncertainty.",
                "En inferentiel figur bør kommunikere usikkerhed.",
            ),
            True,
            _t(
                "El estimando sin precisión favorece conclusiones excesivas.",
                "An estimand without precision encourages excessive conclusions.",
                "Et estimand uden præcision fremmer overdrevne konklusioner.",
            ),
        ),
    ),
    tutor=(
        _t(
            "El tutor debe exigir un contrato de figura antes de recomendar un gráfico. Debe separar magnitud, evidencia e incertidumbre; verificar alineación; y rechazar selecciones o ediciones invisibles.",
            "The tutor should require a figure contract before recommending a plot. It must separate magnitude, evidence, and uncertainty; verify alignment; and reject invisible selection or editing.",
            "Tutoren bør kræve en figurkontrakt før et plot anbefales. Den skal adskille størrelse, evidens og usikkerhed; verificere afstemning; og afvise usynlig selektion eller redigering.",
        ),
        (
            _t(
                "La pregunta y unidad determinan la figura.",
                "Question and unit determine the figure.",
                "Spørgsmål og enhed bestemmer figuren.",
            ),
            _t(
                "Volcano y MA responden preguntas complementarias.",
                "Volcano and MA answer complementary questions.",
                "Volcano og MA besvarer komplementære spørgsmål.",
            ),
            _t(
                "Heatmaps dependen de selección, escala y orden.",
                "Heatmaps depend on selection, scale, and order.",
                "Heatmaps afhænger af selektion, skala og rækkefølge.",
            ),
            _t(
                "Datos, código y parámetros hacen reproducible la exportación.",
                "Data, code, and parameters make export reproducible.",
                "Data, kode og parametre gør eksport reproducerbar.",
            ),
        ),
        (
            _t(
                "Confundir evidencia con efecto.",
                "Confuse evidence with effect.",
                "Forveksl evidens med effekt.",
            ),
            _t(
                "Etiquetar resultados favorables post hoc.",
                "Label favorable results post hoc.",
                "Sæt labels på fordelagtige resultater post hoc.",
            ),
            _t(
                "Desalinear anotaciones después de ordenar.",
                "Misalign annotations after ordering.",
                "Fejlafstem annoteringer efter sortering.",
            ),
            _t(
                "Depender sólo del color o edición manual.",
                "Rely only on color or manual editing.",
                "Afhæng kun af farve eller manuel redigering.",
            ),
        ),
        (
            _t(
                "¿Qué afirmación debe sostener la figura?",
                "Which claim should the figure support?",
                "Hvilken påstand skal figuren understøtte?",
            ),
            _t(
                "¿Qué unidad y transformación representa cada marca?",
                "Which unit and transformation does each mark represent?",
                "Hvilken enhed og transformation repræsenterer hvert mærke?",
            ),
            _t(
                "¿Cómo se definieron selección y orden?",
                "How were selection and order defined?",
                "Hvordan blev selektion og rækkefølge defineret?",
            ),
            _t(
                "¿Puede regenerarse desde datos versionados?",
                "Can it be regenerated from versioned data?",
                "Kan den regenereres fra versionerede data?",
            ),
        ),
        (
            _t(
                "Define contrato y audiencia.",
                "Defines contract and audience.",
                "Definerer kontrakt og publikum.",
            ),
            _t(
                "Representa escala e incertidumbre correctamente.",
                "Represents scale and uncertainty correctly.",
                "Repræsenterer skala og usikkerhed korrekt.",
            ),
            _t(
                "Alinea datos y anotaciones.",
                "Aligns data and annotations.",
                "Afstemmer data og annoteringer.",
            ),
            _t(
                "Conserva trazabilidad y accesibilidad.",
                "Preserves traceability and accessibility.",
                "Bevarer sporbarhed og tilgængelighed.",
            ),
        ),
        (
            _t(
                "No inventar resultados ausentes de la tabla.",
                "Do not invent results absent from the table.",
                "Opfind ikke resultater, der mangler fra tabellen.",
            ),
            _t(
                "No ocultar puntos no significativos o faltantes.",
                "Do not hide nonsignificant or missing points.",
                "Skjul ikke ikke-signifikante eller manglende punkter.",
            ),
            _t(
                "No tratar una figura exploratoria como confirmatoria.",
                "Do not treat an exploratory figure as confirmatory.",
                "Behandl ikke en eksplorativ figur som konfirmatorisk.",
            ),
            _t(
                "Responder en el idioma activo con terminología precisa.",
                "Respond in the active language with precise terminology.",
                "Svar på det aktive sprog med præcis terminologi.",
            ),
        ),
        (
            "https://odin.sdu.dk/sitecore/index.php?a=searchfagbesk&internkode=BMB831&lang=en",
            "https://bioconductor.org/help/course-materials/",
        ),
    ),
)

LOCALIZED_MODULE_05_ADVANCED_VISUALIZATION = build_module(_SPEC)
LOCALIZED_OBJECTIVE_QUESTION_BANK_05 = build_question_bank(_SPEC)


def materialize_module_05_question_bank(
    locale: AppLocale | str = AppLocale.SPANISH_SPAIN,
) -> tuple[AssessmentItem, ...]:
    """Materialize the stable module 5 objective bank."""

    return materialize_bank(LOCALIZED_OBJECTIVE_QUESTION_BANK_05, locale)


MODULE_05_ADVANCED_VISUALIZATION: LearningModule = (
    LOCALIZED_MODULE_05_ADVANCED_VISUALIZATION.materialize(AppLocale.SPANISH_SPAIN)
)
OBJECTIVE_QUESTION_BANK_05 = materialize_module_05_question_bank()

__all__ = [
    "LOCALIZED_MODULE_05_ADVANCED_VISUALIZATION",
    "LOCALIZED_OBJECTIVE_QUESTION_BANK_05",
    "MODULE_05_ADVANCED_VISUALIZATION",
    "OBJECTIVE_QUESTION_BANK_05",
    "materialize_module_05_question_bank",
]
