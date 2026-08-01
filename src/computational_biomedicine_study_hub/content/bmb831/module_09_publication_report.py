"""BMB831 module 9: publication appraisal and the individual English report."""

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
    module_id="bmb831.m09",
    title=_t(
        "Evaluación de publicaciones e informe individual en inglés",
        "Publication appraisal and the individual English report",
        "Publikationsvurdering og den individuelle engelske rapport",
    ),
    summary=_t(
        "Reconstruye pregunta, diseño, datos, métodos, resultados y afirmaciones de una publicación; verifica trazabilidad y límites; y redacta un informe individual en inglés con evidencia cuantitativa y reproducibilidad explícitas.",
        "Reconstruct a publication's question, design, data, methods, results, and claims; verify traceability and limits; and write an individual English report with explicit quantitative evidence and reproducibility.",
        "Rekonstruér en publikations spørgsmål, design, data, metoder, resultater og påstande; verificér sporbarhed og grænser; og skriv en individuel engelsk rapport med eksplicit kvantitativ evidens og reproducerbarhed.",
    ),
    objectives=(
        (
            "m09.o1",
            _t(
                "Reconstruir estimando, población, diseño, comparaciones y unidad independiente desde una publicación.",
                "Reconstruct the estimand, population, design, comparisons, and independent unit from a publication.",
                "Rekonstruere estimand, population, design, sammenligninger og uafhængig enhed fra en publikation.",
            ),
        ),
        (
            "m09.o2",
            _t(
                "Auditar la cadena fuente–procesamiento–modelo–tabla–figura–afirmación y detectar evidencia faltante.",
                "Audit the source–processing–model–table–figure–claim chain and detect missing evidence.",
                "Auditere kæden kilde–behandling–model–tabel–figur–påstand og opdage manglende evidens.",
            ),
        ),
        (
            "m09.o3",
            _t(
                "Evaluar validez, multiplicidad, sensibilidad, relevancia biológica, replicación y generalización.",
                "Evaluate validity, multiplicity, sensitivity, biological relevance, replication, and generalization.",
                "Vurdere validitet, multiplicitet, følsomhed, biologisk relevans, replikation og generalisering.",
            ),
        ),
        (
            "m09.o4",
            _t(
                "Redactar en inglés un informe coherente, cuantitativo, atribuible y reproducible sin inventar resultados.",
                "Write a coherent, quantitative, attributable, and reproducible report in English without inventing results.",
                "Skrive en sammenhængende, kvantitativ, attribuerbar og reproducerbar rapport på engelsk uden at opfinde resultater.",
            ),
        ),
    ),
    concepts=(
        (
            "appraisal-question",
            _t("Reconstrucción de la pregunta", "Question reconstruction", "Rekonstruktion af spørgsmålet"),
            _t(
                "El título o abstract no siempre declara el estimando. Deben identificarse población, unidad, exposición o grupos, outcome o matriz, tiempo, contraste y objetivo exploratorio o confirmatorio. La unidad independiente se obtiene del diseño, no del número de filas de una tabla. Cuando la pregunta no puede reconstruirse, la interpretación de coeficientes y figuras queda indeterminada.",
                "A title or abstract does not always state the estimand. Identify population, unit, exposure or groups, outcome or matrix, time, contrast, and exploratory or confirmatory purpose. The independent unit comes from design, not table row count. When the question cannot be reconstructed, coefficients and figures remain indeterminate.",
                "Titel eller abstract angiver ikke altid estimand. Identificér population, enhed, eksponering eller grupper, outcome eller matrix, tid, kontrast og eksplorativt eller konfirmatorisk formål. Den uafhængige enhed kommer fra designet, ikke antal tabelrækker. Når spørgsmålet ikke kan rekonstrueres, forbliver koefficienter og figurer ubestemte.",
            ),
            (
                _t("Escribe el estimando antes de resumir resultados.", "Write the estimand before summarizing results.", "Skriv estimand før resultater opsummeres."),
                _t("Distingue muestras, features y observaciones repetidas.", "Distinguish samples, features, and repeated observations.", "Skeln mellem prøver, features og gentagne observationer."),
            ),
        ),
        (
            "claim-traceability",
            _t("Trazabilidad de afirmaciones", "Claim traceability", "Påstandssporbarhed"),
            _t(
                "Cada afirmación cuantitativa debe vincularse con una tabla, figura o artefacto; cada artefacto con un modelo y datos derivados; y cada dato derivado con una fuente y decisiones. Una figura seleccionada no puede sostener una afirmación sobre toda la familia de hipótesis sin la tabla completa. La disponibilidad de código no compensa metadata incompleta ni resultados no reportados.",
                "Every quantitative claim should link to a table, figure, or artifact; every artifact to a model and derived data; and every derived dataset to source and decisions. A selected figure cannot support a claim about the full hypothesis family without the complete table. Code availability does not compensate for incomplete metadata or unreported results.",
                "Enhver kvantitativ påstand bør forbindes med en tabel, figur eller artefakt; hvert artefakt med en model og afledte data; og hvert afledt datasæt med kilde og beslutninger. En udvalgt figur kan ikke understøtte en påstand om hele hypotese-familien uden den komplette tabel. Tilgængelig kode kompenserer ikke for ufuldstændige metadata eller urapporterede resultater.",
            ),
            (
                _t("Construye una tabla claim–evidence–limit.", "Build a claim–evidence–limit table.", "Byg en tabel med påstand–evidens–grænse."),
                _t("Marca lo no reportado en lugar de asumirlo.", "Mark unreported information rather than assuming it.", "Markér ikke-rapporteret information frem for at antage den."),
            ),
        ),
        (
            "validity-appraisal",
            _t("Validez y relevancia", "Validity and relevance", "Validitet og relevans"),
            _t(
                "La evaluación separa validez interna, generalización y relevancia biológica. Revisa confusión, lote, missingness, selección, multiplicidad, sensibilidad y replicación. Un valor p pequeño no sustituye tamaño de efecto ni validación. Una interpretación de pathway o estructura añade contexto, pero no demuestra mecanismo. La conclusión debe ser proporcional al diseño y a la evidencia independiente.",
                "Appraisal separates internal validity, generalization, and biological relevance. Review confounding, batch, missingness, selection, multiplicity, sensitivity, and replication. A small p-value does not replace effect size or validation. Pathway or structural interpretation adds context but does not demonstrate mechanism. The conclusion should be proportional to design and independent evidence.",
                "Vurdering adskiller intern validitet, generalisering og biologisk relevans. Gennemgå confounding, batch, missingness, selektion, multiplicitet, følsomhed og replikation. En lille p-værdi erstatter ikke effektstørrelse eller validering. Pathway- eller strukturfortolkning tilføjer kontekst, men demonstrerer ikke mekanisme. Konklusionen bør være proportional med design og uafhængig evidens.",
            ),
            (
                _t("Busca análisis alternativos y resultados completos.", "Look for alternative analyses and complete results.", "Søg alternative analyser og komplette resultater."),
                _t("Distingue limitación reconocida de limitación omitida.", "Distinguish acknowledged from omitted limitations.", "Skeln mellem anerkendte og udeladte begrænsninger."),
            ),
        ),
        (
            "english-report",
            _t("Informe individual en inglés", "Individual English report", "Individuel engelsk rapport"),
            _t(
                "El informe mantiene una línea lógica: pregunta y estimando, datos y procedencia, métodos, QC, resultados cuantitativos, figuras, interpretación, limitaciones y reproducibilidad. Métodos se redacta para regenerar el análisis; resultados informa efecto, incertidumbre y denominadores; discusión no introduce resultados nuevos. Abstract resume valores consistentes con el cuerpo. Las fuentes se atribuyen y cualquier información ausente se declara.",
                "The report maintains a logical line: question and estimand, data and provenance, methods, QC, quantitative results, figures, interpretation, limitations, and reproducibility. Methods are written to regenerate the analysis; results report effect, uncertainty, and denominators; discussion introduces no new results. The abstract summarizes values consistent with the body. Sources are attributed, and missing information is declared.",
                "Rapporten bevarer en logisk linje: spørgsmål og estimand, data og proveniens, metoder, QC, kvantitative resultater, figurer, fortolkning, begrænsninger og reproducerbarhed. Metoder skrives så analysen kan regenereres; resultater rapporterer effekt, usikkerhed og denominatorer; diskussion introducerer ingen nye resultater. Abstract opsummerer værdier konsistente med hovedteksten. Kilder attribueres, og manglende information deklareres.",
            ),
            (
                _t("Redacta métodos y resultados antes del abstract.", "Draft methods and results before the abstract.", "Skriv metoder og resultater før abstract."),
                _t("La herramienta prepara, pero no reproduce una rúbrica privada.", "The tool prepares but does not reproduce a private rubric.", "Værktøjet forbereder, men gengiver ikke en privat rubrik."),
            ),
        ),
    ),
    examples=(
        (
            "m09.e01",
            _t("Generar una frase cuantitativa coherente", "Generate a coherent quantitative sentence", "Generér en sammenhængende kvantitativ sætning"),
            _t("Construye una frase desde campos explícitos sin alterar valores.", "Construct a sentence from explicit fields without changing values.", "Konstruér en sætning fra eksplicitte felter uden at ændre værdier."),
            (
                _t("Se informa contraste y escala.", "Contrast and scale are reported.", "Kontrast og skala rapporteres."),
                _t("Se informa intervalo y FDR.", "Interval and FDR are reported.", "Interval og FDR rapporteres."),
                _t("No se añade causalidad.", "No causality is added.", "Ingen kausalitet tilføjes."),
            ),
            """result <- list(
  feature = "G1",
  contrast = "treated versus control",
  log2fc = 1.20,
  lower = 0.70,
  upper = 1.70,
  padj = 0.010
)
sentence <- sprintf(
  "%s showed a log2 fold change of %.2f for %s (95%% CI %.2f to %.2f; adjusted p = %.3f).",
  result$feature,
  result$log2fc,
  result$contrast,
  result$lower,
  result$upper,
  result$padj
)
cat(sentence)
""",
            "G1 showed a log2 fold change of 1.20 for treated versus control (95% CI 0.70 to 1.70; adjusted p = 0.010).",
            _t("La frase conserva magnitud, contraste, precisión y evidencia ajustada sin afirmar mecanismo.", "The sentence preserves magnitude, contrast, precision, and adjusted evidence without claiming mechanism.", "Sætningen bevarer størrelse, kontrast, præcision og justeret evidens uden at påstå mekanisme."),
        ),
        (
            "m09.e02",
            _t("Auditar campos de reproducibilidad", "Audit reproducibility fields", "Auditér reproducerbarhedsfelter"),
            _t("Identifica elementos ausentes de un paquete de análisis mínimo.", "Identify missing elements from a minimum analysis package.", "Identificér manglende elementer i en minimal analysepakke."),
            (
                _t("Los campos esperados se declaran antes.", "Expected fields are declared first.", "Forventede felter deklareres først."),
                _t("Ausencia se reporta explícitamente.", "Absence is reported explicitly.", "Fravær rapporteres eksplicit."),
                _t("El control es determinista.", "The check is deterministic.", "Kontrollen er deterministisk."),
            ),
            """expected <- c("source", "checksums", "script", "parameters", "session_info", "complete_results")
provided <- c("source", "script", "parameters", "complete_results")
missing <- setdiff(expected, provided)
cat("missing=", paste(missing, collapse = ","), "\n", sep = "")
cat("complete=", length(missing) == 0, sep = "")
""",
            """missing=checksums,session_info
complete=FALSE""",
            _t("El paquete carece de identidad verificable de archivos y reconstrucción del entorno.", "The package lacks verifiable file identity and environment reconstruction.", "Pakken mangler verificerbar filidentitet og rekonstruktion af miljøet."),
        ),
    ),
    practices=(
        (
            "m09.p01",
            "PIPELINE_DESIGN",
            _t("Diseña una matriz claim–evidence–limit para una publicación ómica.", "Design a claim–evidence–limit matrix for an omics publication.", "Design en claim–evidence–limit-matrix for en omikpublikation."),
            (_t("Incluye localización exacta de evidencia.", "Include exact evidence location.", "Medtag præcis evidensplacering."), _t("Distingue datos de interpretación.", "Distinguish data from interpretation.", "Skeln mellem data og fortolkning.")),
            _t("Cada fila contiene claim, tipo, estimando, tabla/figura, método, datos y muestra, resultado cuantitativo, fuente externa, supuestos, limitación y evaluación supported/partial/unsupported. Los campos no reportados permanecen marcados como ausentes.", "Each row contains claim, type, estimand, table or figure, method, data and sample, quantitative result, external source, assumptions, limitation, and supported/partial/unsupported assessment. Unreported fields remain marked as missing.", "Hver række indeholder claim, type, estimand, tabel eller figur, metode, data og prøve, kvantitativt resultat, ekstern kilde, antagelser, begrænsning og supported/partial/unsupported-vurdering. Ikke-rapporterede felter markeres som manglende."),
            _t("La matriz obliga a separar lo observado de lo inferido.", "The matrix forces separation of observation from inference.", "Matricen tvinger adskillelse af observation fra inferens."),
            "",
        ),
        (
            "m09.p02",
            "DATA_INTERPRETATION",
            _t("El abstract afirma biomarcador clínico; el estudio usa ocho muestras celulares y no valida predicción. Evalúa la afirmación.", "The abstract claims a clinical biomarker; the study uses eight cell-line samples and does not validate prediction. Appraise the claim.", "Abstractet hævder en klinisk biomarkør; studiet bruger otte cellelinjeprøver og validerer ikke prædiktion. Vurdér påstanden."),
            (_t("Compara población y uso previsto.", "Compare population and intended use.", "Sammenlign population og tiltænkt brug."), _t("Busca validación y rendimiento.", "Look for validation and performance.", "Søg validering og performance.")),
            _t("Los datos pueden sostener una asociación experimental en células, no desempeño clínico. Faltan pacientes, uso previsto, definición de outcome, partición, calibración, umbral, comparación y validación externa. Biomarcador clínico excede población, diseño y evidencia.", "The data may support an experimental association in cells, not clinical performance. Patients, intended use, outcome definition, splitting, calibration, threshold, comparison, and external validation are missing. The clinical-biomarker claim exceeds population, design, and evidence.", "Data kan understøtte en eksperimentel association i celler, ikke klinisk performance. Patienter, tiltænkt brug, outcome-definition, split, kalibrering, tærskel, sammenligning og ekstern validering mangler. Påstanden om klinisk biomarkør overstiger population, design og evidens."),
            _t("La fuerza de la afirmación debe corresponder al contexto estudiado.", "Claim strength must match the studied context.", "Påstandens styrke skal matche den studerede kontekst."),
            "",
        ),
        (
            "m09.p03",
            "DEBUGGING",
            _t("Una figura informa 20 genes, pero métodos no explica selección y la tabla completa no está disponible. Reconstruye el problema.", "A figure reports 20 genes, but methods do not explain selection and the full table is unavailable. Reconstruct the problem.", "En figur rapporterer 20 gener, men metoder forklarer ikke selektionen, og hele tabellen er ikke tilgængelig. Rekonstruér problemet."),
            (_t("No puede auditarse la familia ni el criterio.", "The family and criterion cannot be audited.", "Familien og kriteriet kan ikke auditeres."), _t("Puede existir selección post hoc.", "Post-hoc selection may exist.", "Post-hoc-selektion kan eksistere.")),
            _t("No se conoce si los genes fueron seleccionados por FDR, efecto, interés previo o apariencia, ni cuántas hipótesis se probaron. La figura no permite evaluar multiplicidad, resultados discordantes o magnitudes no mostradas. Deben publicarse método, regla y tabla completa.", "It is unknown whether genes were selected by FDR, effect, prior interest, or appearance, or how many hypotheses were tested. The figure cannot assess multiplicity, discordant results, or hidden magnitudes. Method, rule, and complete table should be provided.", "Det er ukendt om gener blev valgt efter FDR, effekt, prior interesse eller udseende, eller hvor mange hypoteser der blev testet. Figuren kan ikke vurdere multiplicitet, uoverensstemmende resultater eller skjulte størrelser. Metode, regel og komplet tabel bør leveres."),
            _t("La selección visible no sustituye el conjunto completo de resultados.", "Visible selection does not replace the complete result set.", "Synlig selektion erstatter ikke det komplette resultatsæt."),
            "",
        ),
        (
            "m09.p04",
            "SHORT_ANSWER",
            _t("Distingue Methods, Results y Discussion en el informe.", "Distinguish Methods, Results, and Discussion in the report.", "Skeln mellem Methods, Results og Discussion i rapporten."),
            (_t("Methods permite regenerar.", "Methods enables regeneration.", "Methods muliggør regenerering."), _t("Discussion limita e interpreta.", "Discussion interprets and limits.", "Discussion fortolker og begrænser.")),
            _t("Methods describe data, preprocessing, model, parameters, software and checks. Results report prespecified quantitative findings, uncertainty, denominators, tables and figures. Discussion interprets those results against prior evidence, alternatives, limitations and generalisation without introducing new analyses as established findings.", "Methods describe data, preprocessing, model, parameters, software and checks. Results report prespecified quantitative findings, uncertainty, denominators, tables and figures. Discussion interprets those results against prior evidence, alternatives, limitations and generalisation without introducing new analyses as established findings.", "Methods beskriver data, præprocessering, model, parametre, software og kontroller. Results rapporterer foruddefinerede kvantitative fund, usikkerhed, denominatorer, tabeller og figurer. Discussion fortolker resultaterne mod prior evidens, alternativer, begrænsninger og generalisering uden at introducere nye analyser som etablerede fund."),
            _t("La separación evita ocultar decisiones o inflar interpretación.", "The separation prevents hidden decisions and inflated interpretation.", "Adskillelsen forhindrer skjulte beslutninger og oppustet fortolkning."),
            "",
        ),
        (
            "m09.p05",
            "CODE_COMPLETION",
            _t("Completa una función que devuelva campos faltantes de reproducibilidad.", "Complete a function returning missing reproducibility fields.", "Færdiggør en funktion, der returnerer manglende reproducerbarhedsfelter."),
            (_t("Usa setdiff.", "Use setdiff.", "Brug setdiff."), _t("Preserva el orden esperado.", "Preserve expected order.", "Bevar forventet rækkefølge.")),
            _t("missing_fields <- function(expected, provided) { setdiff(expected, provided) }", "missing_fields <- function(expected, provided) { setdiff(expected, provided) }", "missing_fields <- function(expected, provided) { setdiff(expected, provided) }"),
            _t("La función hace explícito lo que falta en lugar de asumir completitud.", "The function makes missing evidence explicit rather than assuming completeness.", "Funktionen gør manglende evidens eksplicit frem for at antage fuldstændighed."),
            "missing_fields <- function(expected, provided) {\n  # return missing names\n}",
        ),
        (
            "m09.p06",
            "ORAL_EXPLANATION",
            _t("Prepara una explicación de 90 segundos: ¿cómo decides si una conclusión de una publicación está justificada?", "Prepare a 90-second explanation: how do you decide whether a publication conclusion is justified?", "Forbered en 90-sekunders forklaring: hvordan afgør du om en publikations konklusion er begrundet?"),
            (_t("Traza claim a evidencia.", "Trace the claim to evidence.", "Spor claim til evidens."), _t("Incluye alternativas y generalización.", "Include alternatives and generalization.", "Medtag alternativer og generalisering.")),
            _t("Primero formulo exactamente la conclusión y reconstruyo población, estimando y diseño. La vinculo con resultados cuantitativos completos, modelo, incertidumbre y multiplicidad; reviso QC, confusión, selección, sensibilidad y replicación. Comparo explicaciones alternativas y evidencia externa. La conclusión es justificada sólo hasta el alcance sostenido por diseño y datos; mecanismo, causalidad o uso clínico requieren evidencia adicional.", "First I state the conclusion precisely and reconstruct population, estimand, and design. I link it to complete quantitative results, model, uncertainty, and multiplicity; review QC, confounding, selection, sensitivity, and replication; and compare alternatives and external evidence. The conclusion is justified only to the extent supported by design and data; mechanism, causality, or clinical use require additional evidence.", "Først formulerer jeg konklusionen præcist og rekonstruerer population, estimand og design. Jeg forbinder den med komplette kvantitative resultater, model, usikkerhed og multiplicitet; gennemgår QC, confounding, selektion, følsomhed og replikation; og sammenligner alternativer og ekstern evidens. Konklusionen er kun begrundet i det omfang design og data understøtter den; mekanisme, kausalitet eller klinisk brug kræver yderligere evidens."),
            _t("La respuesta evalúa proporcionalidad entre afirmación y evidencia.", "The answer evaluates proportionality between claim and evidence.", "Svaret vurderer proportionalitet mellem påstand og evidens."),
            "",
        ),
    ),
    mcqs=(
        _mcq("q01", _t("¿Qué debe reconstruirse primero?", "What should be reconstructed first?", "Hvad bør rekonstrueres først?"), (_option("a", _t("Pregunta, población y estimando", "Question, population, and estimand", "Spørgsmål, population og estimand")), _option("b", _t("Paleta", "Palette", "Palette")), _option("c", _t("Factor de impacto", "Impact factor", "Impact factor")), _option("d", _t("Longitud del PDF", "PDF length", "PDF-længde"))), "a", _t("Sin pregunta no puede interpretarse el análisis.", "Without a question, the analysis cannot be interpreted.", "Uden et spørgsmål kan analysen ikke fortolkes.")),
        _mcq("q02", _t("¿Qué define la unidad independiente?", "What defines the independent unit?", "Hvad definerer den uafhængige enhed?"), (_option("a", _t("Diseño de muestreo", "Sampling design", "Samplingdesign")), _option("b", _t("Número de genes", "Gene count", "Antal gener")), _option("c", _t("Número de figuras", "Figure count", "Antal figurer")), _option("d", _t("Número de filas", "Row count", "Antal rækker"))), "a", _t("La independencia surge de cómo se obtuvieron observaciones.", "Independence arises from how observations were obtained.", "Uafhængighed kommer fra hvordan observationer blev opnået.")),
        _mcq("q03", _t("¿Qué conecta una matriz claim–evidence?", "What does a claim–evidence matrix connect?", "Hvad forbinder en claim–evidence-matrix?"), (_option("a", _t("Afirmación, resultado, método y límite", "Claim, result, method, and limit", "Påstand, resultat, metode og grænse")), _option("b", _t("Sólo autores", "Only authors", "Kun forfattere")), _option("c", _t("Sólo referencias", "Only references", "Kun referencer")), _option("d", _t("Sólo colores", "Only colors", "Kun farver"))), "a", _t("Permite auditar si la afirmación está sostenida.", "It enables auditing whether the claim is supported.", "Det muliggør audit af om påstanden er understøttet.")),
        _mcq("q04", _t("¿Qué no compensa código disponible?", "What does available code not compensate for?", "Hvad kompenserer tilgængelig kode ikke for?"), (_option("a", _t("Metadata o resultados incompletos", "Incomplete metadata or results", "Ufuldstændige metadata eller resultater")), _option("b", _t("Comentarios", "Comments", "Kommentarer")), _option("c", _t("Versiones", "Versions", "Versioner")), _option("d", _t("Checksums", "Checksums", "Checksums"))), "a", _t("Reproducir código no recupera información omitida.", "Running code does not recover omitted information.", "Kørsel af kode genskaber ikke udeladt information.")),
        _mcq("q05", _t("¿Qué debe acompañar un valor p?", "What should accompany a p-value?", "Hvad bør ledsage en p-værdi?"), (_option("a", _t("Efecto, incertidumbre y multiplicidad", "Effect, uncertainty, and multiplicity", "Effekt, usikkerhed og multiplicitet")), _option("b", _t("Sólo signo", "Only sign", "Kun fortegn")), _option("c", _t("Sólo pathway", "Only pathway", "Kun pathway")), _option("d", _t("Sólo cita", "Only citation", "Kun citation"))), "a", _t("La evidencia aislada no expresa magnitud ni precisión.", "Evidence alone does not express magnitude or precision.", "Evidens alene udtrykker ikke størrelse eller præcision.")),
        _mcq("q06", _t("¿Dónde se introducen resultados cuantitativos nuevos?", "Where are new quantitative results introduced?", "Hvor introduceres nye kvantitative resultater?"), (_option("a", _t("Results", "Results", "Results")), _option("b", _t("Discussion solamente", "Discussion only", "Kun Discussion")), _option("c", _t("Referencias", "References", "Referencer")), _option("d", _t("Título", "Title", "Titel"))), "a", _t("Discussion interpreta resultados ya reportados.", "Discussion interprets already reported results.", "Discussion fortolker allerede rapporterede resultater.")),
        _mcq("q07", _t("¿Cuándo debe redactarse el abstract?", "When should the abstract be drafted?", "Hvornår bør abstract skrives?"), (_option("a", _t("Después de métodos y resultados", "After methods and results", "Efter metoder og resultater")), _option("b", _t("Antes de analizar", "Before analysis", "Før analyse")), _option("c", _t("Sin valores", "Without values", "Uden værdier")), _option("d", _t("Sólo desde título", "Only from title", "Kun fra titel"))), "a", _t("Debe resumir resultados consistentes con el cuerpo.", "It should summarize results consistent with the body.", "Det bør opsummere resultater konsistente med hovedteksten.")),
        _mcq("q08", _t("¿Qué puede certificar el estudio de informe?", "What can the report studio certify?", "Hvad kan rapportstudiet certificere?"), (_option("a", _t("Organización y persistencia del borrador", "Draft organization and persistence", "Organisering og persistens af udkast")), _option("b", _t("Calificación oficial", "Official grade", "Officiel karakter")), _option("c", _t("Asistencia", "Attendance", "Deltagelse")), _option("d", _t("Equivalencia con rúbrica privada", "Equivalence to a private rubric", "Ækvivalens med privat rubrik"))), "a", _t("La herramienta prepara sin reproducir evaluación privada.", "The tool prepares without reproducing private assessment.", "Værktøjet forbereder uden at gengive privat evaluering.")),
    ),
    true_false=(
        _tf("tf01", _t("El abstract siempre declara el estimando completo.", "The abstract always states the complete estimand.", "Abstract angiver altid det komplette estimand."), False, _t("Debe reconstruirse desde métodos y diseño.", "It may require reconstruction from methods and design.", "Det kan kræve rekonstruktion fra metoder og design.")),
        _tf("tf02", _t("La unidad independiente se deduce del diseño.", "The independent unit follows from design.", "Den uafhængige enhed følger af designet."), True, _t("No equivale al número de features.", "It is not the number of features.", "Det er ikke antallet af features.")),
        _tf("tf03", _t("Una figura seleccionada sustituye la tabla completa.", "A selected figure replaces the complete table.", "En udvalgt figur erstatter den komplette tabel."), False, _t("La familia y resultados no mostrados siguen siendo necesarios.", "The family and unshown results remain necessary.", "Familien og ikke-viste resultater er stadig nødvendige.")),
        _tf("tf04", _t("Código disponible garantiza validez científica.", "Available code guarantees scientific validity.", "Tilgængelig kode garanterer videnskabelig validitet."), False, _t("Diseño y datos pueden seguir siendo inadecuados.", "Design and data may remain inadequate.", "Design og data kan stadig være utilstrækkelige.")),
        _tf("tf05", _t("La evaluación debe considerar sensibilidad y replicación.", "Appraisal should consider sensitivity and replication.", "Vurdering bør overveje følsomhed og replikation."), True, _t("Evalúan robustez y generalización.", "They assess robustness and generalization.", "De vurderer robusthed og generalisering.")),
        _tf("tf06", _t("Discussion puede introducir análisis no reportados como hallazgos confirmados.", "Discussion may introduce unreported analyses as confirmed findings.", "Discussion kan introducere ikke-rapporterede analyser som bekræftede fund."), False, _t("Los resultados deben aparecer con método y evidencia.", "Results require method and evidence.", "Resultater kræver metode og evidens.")),
        _tf("tf07", _t("El informe publicado por SDU debe escribirse en inglés.", "The published SDU report requirement is in English.", "Det offentliggjorte SDU-rapportkrav er på engelsk."), True, _t("La interfaz puede ser trilingüe, pero el borrador se prepara en inglés.", "The interface may be trilingual, but the draft is prepared in English.", "Interfacet kan være tresproget, men udkastet forberedes på engelsk.")),
        _tf("tf08", _t("El estudio de informe asigna calificación oficial.", "The report studio assigns an official grade.", "Rapportstudiet giver en officiel karakter."), False, _t("Organiza preparación y persistencia únicamente.", "It only structures preparation and persistence.", "Det strukturerer kun forberedelse og persistens.")),
    ),
    tutor=(
        _t("El tutor debe vincular cada afirmación con evidencia y limitarse a materiales disponibles. Puede revisar estructura y claridad, pero no inventar resultados ni reproducir una rúbrica privada.", "The tutor must link every claim to evidence and remain within available material. It may review structure and clarity but may not invent results or reproduce a private rubric.", "Tutoren skal forbinde hver påstand med evidens og holde sig til tilgængeligt materiale. Den kan gennemgå struktur og klarhed, men må ikke opfinde resultater eller gengive en privat rubrik."),
        (
            _t("Pregunta y estimando preceden a interpretación.", "Question and estimand precede interpretation.", "Spørgsmål og estimand går forud for fortolkning."),
            _t("Claims requieren artefactos cuantitativos.", "Claims require quantitative artifacts.", "Claims kræver kvantitative artefakter."),
            _t("Validez, relevancia y generalización son distintas.", "Validity, relevance, and generalization are distinct.", "Validitet, relevans og generalisering er forskellige."),
            _t("El informe debe ser regenerable y atribuible.", "The report should be regenerable and attributable.", "Rapporten bør være regenererbar og attribuerbar."),
        ),
        (
            _t("Resumir sólo abstract.", "Summarize only the abstract.", "Opsummér kun abstract."),
            _t("Aceptar figura sin tabla completa.", "Accept a figure without a complete table.", "Acceptér en figur uden komplet tabel."),
            _t("Confundir significación con utilidad.", "Confuse significance with utility.", "Forveksl signifikans med nytte."),
            _t("Inventar datos faltantes.", "Invent missing data.", "Opfind manglende data."),
        ),
        (
            _t("¿Cuál es el estimando exacto?", "What is the exact estimand?", "Hvad er det præcise estimand?"),
            _t("¿Dónde está la evidencia de esta frase?", "Where is the evidence for this sentence?", "Hvor er evidensen for denne sætning?"),
            _t("¿Qué análisis de sensibilidad se informó?", "Which sensitivity analysis was reported?", "Hvilken følsomhedsanalyse blev rapporteret?"),
            _t("¿Qué limita la generalización?", "What limits generalization?", "Hvad begrænser generalisering?"),
        ),
        (
            _t("Reconstruye diseño y pregunta.", "Reconstructs design and question.", "Rekonstruerer design og spørgsmål."),
            _t("Traza claims a resultados.", "Traces claims to results.", "Sporer claims til resultater."),
            _t("Evalúa validez y límites.", "Evaluates validity and limits.", "Vurderer validitet og grænser."),
            _t("Redacta informe cuantitativo en inglés.", "Writes a quantitative English report.", "Skriver en kvantitativ engelsk rapport."),
        ),
        (
            _t("No asignar una nota oficial.", "Do not assign an official grade.", "Giv ikke en officiel karakter."),
            _t("No inventar valores, fuentes o métodos.", "Do not invent values, sources, or methods.", "Opfind ikke værdier, kilder eller metoder."),
            _t("No ocultar incertidumbre o resultados faltantes.", "Do not hide uncertainty or missing results.", "Skjul ikke usikkerhed eller manglende resultater."),
            _t("Responder en el idioma activo, preservando el borrador en inglés.", "Respond in the active language while preserving the English draft.", "Svar på det aktive sprog, mens det engelske udkast bevares."),
        ),
        (
            "https://odin.sdu.dk/sitecore/index.php?a=searchfagbesk&internkode=BMB831&lang=en",
            "https://www.equator-network.org/",
            "https://www.nature.com/sdata/policies/repositories",
        ),
    ),
)

LOCALIZED_MODULE_09_PUBLICATION_REPORT = build_module(_SPEC)
LOCALIZED_OBJECTIVE_QUESTION_BANK_09 = build_question_bank(_SPEC)


def materialize_module_09_question_bank(
    locale: AppLocale | str = AppLocale.SPANISH_SPAIN,
) -> tuple[AssessmentItem, ...]:
    """Materialize the stable module 9 objective bank."""

    return materialize_bank(LOCALIZED_OBJECTIVE_QUESTION_BANK_09, locale)


MODULE_09_PUBLICATION_REPORT: LearningModule = LOCALIZED_MODULE_09_PUBLICATION_REPORT.materialize(
    AppLocale.SPANISH_SPAIN
)
OBJECTIVE_QUESTION_BANK_09 = materialize_module_09_question_bank()

__all__ = [
    "LOCALIZED_MODULE_09_PUBLICATION_REPORT",
    "LOCALIZED_OBJECTIVE_QUESTION_BANK_09",
    "MODULE_09_PUBLICATION_REPORT",
    "OBJECTIVE_QUESTION_BANK_09",
    "materialize_module_09_question_bank",
]
