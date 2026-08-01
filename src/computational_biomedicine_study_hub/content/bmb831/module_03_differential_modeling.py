"""BMB831 module 3: differential modeling, multiplicity, and interpretation."""

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
    module_id="bmb831.m03",
    title=_t(
        "Modelado diferencial, multiplicidad e interpretación",
        "Differential modeling, multiplicity, and interpretation",
        "Differential modellering, multiplicitet og fortolkning",
    ),
    summary=_t(
        "Formula contrastes biológicos mediante matrices de diseño, relaciona escala de datos y modelo, interpreta tamaños de efecto e incertidumbre y controla descubrimientos falsos sin convertir significación estadística en relevancia biológica automática.",
        "Formulate biological contrasts through design matrices, connect data scale to the model, interpret effect sizes and uncertainty, and control false discoveries without turning statistical significance into automatic biological relevance.",
        "Formulér biologiske kontraster gennem designmatricer, forbind dataskala med modellen, fortolk effektstørrelser og usikkerhed, og kontrollér falske fund uden at gøre statistisk signifikans til automatisk biologisk relevans.",
    ),
    objectives=(
        (
            "m03.o1",
            _t(
                "Traducir una pregunta biológica y un diseño experimental a un modelo y contraste explícitos.",
                "Translate a biological question and experimental design into an explicit model and contrast.",
                "Oversætte et biologisk spørgsmål og forsøgsdesign til en eksplicit model og kontrast.",
            ),
        ),
        (
            "m03.o2",
            _t(
                "Distinguir modelos gaussianos y de conteo, y reconocer el papel de la dispersión, offsets y covariables.",
                "Distinguish Gaussian and count models and recognize the roles of dispersion, offsets, and covariates.",
                "Skelne mellem gaussiske modeller og count-modeller samt forstå rollerne for dispersion, offsets og kovariater.",
            ),
        ),
        (
            "m03.o3",
            _t(
                "Interpretar coeficientes, contrastes, intervalos, valores p ajustados y relevancia práctica de forma conjunta.",
                "Interpret coefficients, contrasts, intervals, adjusted p-values, and practical relevance jointly.",
                "Fortolke koefficienter, kontraster, intervaller, justerede p-værdier og praktisk relevans samlet.",
            ),
        ),
        (
            "m03.o4",
            _t(
                "Evaluar multiplicidad, confusión, dependencia y validación antes de formular una conclusión biológica.",
                "Evaluate multiplicity, confounding, dependence, and validation before making a biological conclusion.",
                "Vurdere multiplicitet, confounding, afhængighed og validering før en biologisk konklusion formuleres.",
            ),
        ),
    ),
    concepts=(
        (
            "estimand-design",
            _t(
                "Estimando, diseño y contraste",
                "Estimand, design, and contrast",
                "Estimand, design og kontrast",
            ),
            _t(
                "El análisis diferencial comienza definiendo qué comparación se desea estimar y en qué población o conjunto de muestras. La matriz de diseño representa grupos, lotes y covariables; el contraste especifica una combinación de coeficientes. Un coeficiente sólo tiene significado condicionado a la codificación, nivel de referencia y demás términos del modelo. Si grupo y lote están completamente confundidos, no existe información para separar sus efectos.",
                "Differential analysis begins by defining the comparison to estimate and the population or sample set to which it applies. The design matrix represents groups, batches, and covariates; the contrast specifies a combination of coefficients. A coefficient is meaningful only conditional on coding, reference level, and other model terms. If group and batch are completely confounded, there is no information to separate their effects.",
                "Differential analyse begynder med at definere den sammenligning, der skal estimeres, og den population eller det prøvesæt, den gælder for. Designmatricen repræsenterer grupper, batches og kovariater; kontrasten angiver en kombination af koefficienter. En koefficient giver kun mening betinget af kodning, referenceniveau og øvrige modelled. Hvis gruppe og batch er fuldstændigt confounded, findes der ingen information til at adskille effekterne.",
            ),
            (
                _t(
                    "Declara la comparación antes de observar resultados.",
                    "Declare the comparison before inspecting results.",
                    "Deklarér sammenligningen før resultaterne inspiceres.",
                ),
                _t(
                    "Comprueba rango y confusión de la matriz de diseño.",
                    "Check design-matrix rank and confounding.",
                    "Kontrollér designmatricens rang og confounding.",
                ),
            ),
        ),
        (
            "model-scale",
            _t(
                "Escala, distribución y modelo",
                "Scale, distribution, and model",
                "Skala, fordeling og model",
            ),
            _t(
                "Los conteos de RNA-seq presentan discreción, diferencias de profundidad y sobredispersión, por lo que los pipelines estándar suelen utilizar modelos de conteo con factores de tamaño y dispersión. Las intensidades transformadas o abundancias aproximadamente continuas pueden analizarse con modelos gaussianos cuando los residuos y la varianza son compatibles. La elección no depende de una etiqueta genérica de omics, sino del proceso de medida, la escala y el estimando.",
                "RNA-seq counts are discrete, vary in depth, and are overdispersed, so standard pipelines commonly use count models with size factors and dispersion. Transformed intensities or approximately continuous abundances may be analyzed with Gaussian models when residual and variance behavior is compatible. Choice does not depend on a generic omics label but on measurement process, scale, and estimand.",
                "RNA-seq-counts er diskrete, varierer i dybde og er overdispergerede, så standardpipelines bruger ofte count-modeller med størrelsesfaktorer og dispersion. Transformerede intensiteter eller omtrent kontinuerte abundanser kan analyseres med gaussiske modeller, når residual- og variansadfærd er kompatibel. Valget afhænger ikke af en generisk omiketiket, men af måleproces, skala og estimand.",
            ),
            (
                _t(
                    "No introduzcas valores log-transformados en un modelo que espera conteos crudos.",
                    "Do not feed log-transformed values into a model that expects raw counts.",
                    "Indsæt ikke log-transformerede værdier i en model, der forventer rå counts.",
                ),
                _t(
                    "La dispersión representa variación adicional respecto a una Poisson simple.",
                    "Dispersion represents extra variation beyond a simple Poisson model.",
                    "Dispersion repræsenterer ekstra variation ud over en simpel Poisson-model.",
                ),
            ),
        ),
        (
            "effect-uncertainty",
            _t(
                "Efecto, incertidumbre y dirección",
                "Effect, uncertainty, and direction",
                "Effekt, usikkerhed og retning",
            ),
            _t(
                "Un resultado diferencial debe comunicar dirección, magnitud, incertidumbre y escala. Un log2 fold change de 1 corresponde a una razón de dos bajo la definición habitual, pero su relevancia depende de la precisión, la abundancia basal, el contexto y el objetivo. El valor p evalúa compatibilidad con una hipótesis nula bajo el modelo; no mide tamaño del efecto, probabilidad de replicación ni importancia biológica.",
                "A differential result should communicate direction, magnitude, uncertainty, and scale. A log2 fold change of 1 corresponds to a ratio of two under the usual definition, but relevance depends on precision, baseline abundance, context, and purpose. A p-value assesses compatibility with a null hypothesis under the model; it does not measure effect size, replication probability, or biological importance.",
                "Et differentialt resultat bør kommunikere retning, størrelse, usikkerhed og skala. En log2 fold change på 1 svarer under den sædvanlige definition til et forhold på to, men relevansen afhænger af præcision, basisabundans, kontekst og formål. En p-værdi vurderer kompatibilitet med en nulhypotese under modellen; den måler ikke effektstørrelse, replikationssandsynlighed eller biologisk betydning.",
            ),
            (
                _t(
                    "Interpreta intervalos y tamaños de efecto junto al valor p.",
                    "Interpret intervals and effect sizes together with the p-value.",
                    "Fortolk intervaller og effektstørrelser sammen med p-værdien.",
                ),
                _t(
                    "Distingue significación estadística de utilidad biológica.",
                    "Distinguish statistical significance from biological utility.",
                    "Skeln mellem statistisk signifikans og biologisk nytte.",
                ),
            ),
        ),
        (
            "multiple-testing",
            _t(
                "Multiplicidad y descubrimientos falsos",
                "Multiplicity and false discoveries",
                "Multiplicitet og falske fund",
            ),
            _t(
                "Probar miles de características genera falsos positivos aun cuando cada prueba tenga un nivel nominal pequeño. El control de false discovery rate limita la proporción esperada de falsos descubrimientos entre los resultados declarados bajo sus supuestos. El ajuste Benjamini-Hochberg depende del conjunto de hipótesis probado. Filtrar después de ver los valores p o reportar sólo genes favorables altera ese conjunto y rompe la interpretación planificada.",
                "Testing thousands of features produces false positives even when every test has a small nominal level. False-discovery-rate control limits the expected proportion of false discoveries among declared results under its assumptions. Benjamini-Hochberg adjustment depends on the tested hypothesis family. Filtering after observing p-values or reporting only favorable genes changes that family and breaks the planned interpretation.",
                "Test af tusindvis af features producerer falske positive, selv når hver test har et lille nominelt niveau. Kontrol af false discovery rate begrænser den forventede andel af falske fund blandt deklarerede resultater under metodens antagelser. Benjamini-Hochberg-justering afhænger af den testede hypotese-familie. Filtrering efter at p-værdier er set eller rapportering af kun fordelagtige gener ændrer familien og bryder den planlagte fortolkning.",
            ),
            (
                _t(
                    "Define la familia de hipótesis antes del ajuste.",
                    "Define the hypothesis family before adjustment.",
                    "Definér hypotese-familien før justering.",
                ),
                _t(
                    "Un FDR de 5% no significa que cada gen tenga 95% de probabilidad de ser verdadero.",
                    "An FDR of 5% does not mean every gene has a 95% probability of being true.",
                    "En FDR på 5% betyder ikke, at hvert gen har 95% sandsynlighed for at være sandt.",
                ),
            ),
        ),
    ),
    examples=(
        (
            "m03.e01",
            _t(
                "Ajustar grupo y lote en un modelo lineal",
                "Adjust for group and batch in a linear model",
                "Justér for gruppe og batch i en lineær model",
            ),
            _t(
                "Usa una matriz pequeña transformada para mostrar que el coeficiente de grupo es condicional al lote.",
                "Use a small transformed matrix to show that the group coefficient is conditional on batch.",
                "Brug en lille transformeret matrix til at vise, at gruppekoefficienten er betinget af batch.",
            ),
            (
                _t(
                    "El nivel control es la referencia.",
                    "Control is the reference level.",
                    "Control er referenceniveauet.",
                ),
                _t(
                    "El lote B se representa con un indicador.",
                    "Batch B is represented by an indicator.",
                    "Batch B repræsenteres med en indikator.",
                ),
                _t(
                    "El coeficiente de grupo compara treated con control a lote constante.",
                    "The group coefficient compares treated with control at constant batch.",
                    "Gruppekoefficienten sammenligner treated med control ved konstant batch.",
                ),
            ),
            """metadata <- data.frame(
  group = factor(c("control", "control", "treated", "treated")),
  batch = factor(c("A", "B", "A", "B"))
)
log_abundance <- c(2, 3, 5, 6)
fit <- lm(log_abundance ~ group + batch, data = metadata)
coefs <- coef(fit)
cat(sprintf("group_effect=%.1f batch_effect=%.1f", coefs["grouptreated"], coefs["batchB"]))
""",
            "group_effect=3.0 batch_effect=1.0",
            _t(
                "Bajo este diseño balanceado, treated se asocia con tres unidades adicionales y el lote B con una unidad, manteniendo constante el otro término.",
                "Under this balanced design, treated is associated with three additional units and batch B with one unit while holding the other term constant.",
                "I dette balancerede design er treated associeret med tre ekstra enheder og batch B med én enhed, mens det andet led holdes konstant.",
            ),
        ),
        (
            "m03.e02",
            _t(
                "Aplicar Benjamini-Hochberg y un umbral de efecto",
                "Apply Benjamini-Hochberg and an effect threshold",
                "Anvend Benjamini-Hochberg og en effekttærskel",
            ),
            _t(
                "Separa el ajuste por multiplicidad de la decisión de relevancia mínima.",
                "Separate multiplicity adjustment from a minimum-relevance decision.",
                "Adskil multiplicitetstilpasning fra en beslutning om minimumsrelevans.",
            ),
            (
                _t(
                    "Se ajustan todos los valores p de la familia.",
                    "All p-values in the family are adjusted.",
                    "Alle p-værdier i familien justeres.",
                ),
                _t(
                    "El umbral de efecto se declara por separado.",
                    "The effect threshold is declared separately.",
                    "Effekttærsklen deklareres separat.",
                ),
                _t(
                    "La tabla completa se conserva aunque sólo algunos genes se destaquen.",
                    "The complete table is retained even when only some genes are highlighted.",
                    "Hele tabellen bevares, selv når kun nogle gener fremhæves.",
                ),
            ),
            """result <- data.frame(
  gene = paste0("G", 1:5),
  log2fc = c(2.0, 1.2, 0.8, -1.5, 0.1),
  pvalue = c(0.001, 0.010, 0.040, 0.200, 0.800)
)
result$padj <- p.adjust(result$pvalue, method = "BH")
selected <- result$gene[result$padj < 0.05 & abs(result$log2fc) >= 1]
cat("selected=", paste(selected, collapse = ","), "\n", sep = "")
cat("adjusted=", paste(format(round(result$padj, 3), nsmall = 3), collapse = ","), sep = "")
""",
            """selected=G1,G2
adjusted=0.005,0.025,0.067,0.250,0.800""",
            _t(
                "G1 y G2 cumplen simultáneamente el criterio de FDR y el umbral de magnitud. G4 tiene efecto grande en este ejemplo, pero evidencia estadística insuficiente.",
                "G1 and G2 satisfy both the FDR criterion and the magnitude threshold. G4 has a large effect in this example but insufficient statistical evidence.",
                "G1 og G2 opfylder både FDR-kriteriet og størrelsestærsklen. G4 har en stor effekt i eksemplet, men utilstrækkelig statistisk evidens.",
            ),
        ),
    ),
    practices=(
        (
            "m03.p01",
            "SHORT_ANSWER",
            _t(
                "Formula un estimando y un contraste para comparar tratamiento frente a control ajustando por lote.",
                "Formulate an estimand and contrast for treatment versus control adjusted for batch.",
                "Formulér et estimand og en kontrast for behandling versus kontrol justeret for batch.",
            ),
            (
                _t(
                    "Indica población, escala y covariables.",
                    "State population, scale, and covariates.",
                    "Angiv population, skala og kovariater.",
                ),
                _t(
                    "No describas sólo una función de R.",
                    "Do not describe only an R function.",
                    "Beskriv ikke kun en R-funktion.",
                ),
            ),
            _t(
                "Estimando: diferencia media o log-fold-change entre tratamiento y control en las muestras elegibles, condicionada al lote. Diseño: ~ batch + group. Contraste: coeficiente treatment versus control con control como referencia, siempre que grupo y lote sean identificables.",
                "Estimand: mean difference or log fold change between treatment and control in eligible samples, conditional on batch. Design: ~ batch + group. Contrast: treatment versus control coefficient with control as reference, provided group and batch are identifiable.",
                "Estimand: middelforskel eller log fold change mellem behandling og kontrol i kvalificerede prøver, betinget af batch. Design: ~ batch + group. Kontrast: treatment versus control-koefficient med control som reference, forudsat at gruppe og batch kan identificeres.",
            ),
            _t(
                "El contraste adquiere significado por el diseño, la codificación y la población.",
                "The contrast gains meaning from design, coding, and population.",
                "Kontrasten får mening fra design, kodning og population.",
            ),
            "",
        ),
        (
            "m03.p02",
            "CODE_TRACING",
            _t(
                "Explica por qué design <- model.matrix(~ batch + group, metadata) puede ser singular cuando cada grupo aparece en un único lote.",
                "Explain why design <- model.matrix(~ batch + group, metadata) can be singular when every group occurs in only one batch.",
                "Forklar hvorfor design <- model.matrix(~ batch + group, metadata) kan være singulær, når hver gruppe kun forekommer i ét batch.",
            ),
            (
                _t(
                    "Piensa en columnas linealmente dependientes.",
                    "Think about linearly dependent columns.",
                    "Tænk på lineært afhængige kolonner.",
                ),
                _t(
                    "La función no crea información ausente.",
                    "The function does not create missing information.",
                    "Funktionen skaber ikke manglende information.",
                ),
            ),
            _t(
                "Si todos los controles están en A y todos los tratados en B, los indicadores de grupo y lote contienen la misma separación. La matriz no tiene rango completo y ningún método puede atribuir de forma única la diferencia a tratamiento o lote.",
                "If all controls are in A and all treated samples are in B, group and batch indicators contain the same separation. The matrix lacks full rank, and no method can uniquely attribute the difference to treatment or batch.",
                "Hvis alle kontroller er i A og alle behandlede prøver i B, indeholder gruppe- og batchindikatorer den samme adskillelse. Matricen har ikke fuld rang, og ingen metode kan entydigt tilskrive forskellen behandling eller batch.",
            ),
            _t(
                "El confounding perfecto es un problema de diseño, no de sintaxis.",
                "Perfect confounding is a design problem, not a syntax problem.",
                "Perfekt confounding er et designproblem, ikke et syntaksproblem.",
            ),
            "",
        ),
        (
            "m03.p03",
            "SHORT_ANSWER",
            _t(
                "Compara qué información aporta un log2 fold change, su intervalo de confianza, el valor p y el valor p ajustado.",
                "Compare the information provided by a log2 fold change, its confidence interval, the p-value, and the adjusted p-value.",
                "Sammenlign informationen fra en log2 fold change, dens konfidensinterval, p-værdien og den justerede p-værdi.",
            ),
            (
                _t(
                    "Distingue magnitud, precisión y multiplicidad.",
                    "Separate magnitude, precision, and multiplicity.",
                    "Adskil størrelse, præcision og multiplicitet.",
                ),
                _t(
                    "No interpretes el valor p como probabilidad de verdad.",
                    "Do not interpret a p-value as probability of truth.",
                    "Fortolk ikke en p-værdi som sandsynlighed for sandhed.",
                ),
            ),
            _t(
                "El log2 fold change describe dirección y magnitud; el intervalo muestra precisión y valores compatibles; el valor p evalúa compatibilidad con la hipótesis nula bajo el modelo; el valor ajustado sitúa esa evidencia dentro de la familia de pruebas para controlar multiplicidad.",
                "The log2 fold change describes direction and magnitude; the interval shows precision and compatible values; the p-value assesses compatibility with the null under the model; the adjusted value places that evidence within the tested family to control multiplicity.",
                "Log2 fold change beskriver retning og størrelse; intervallet viser præcision og kompatible værdier; p-værdien vurderer kompatibilitet med nulhypotesen under modellen; den justerede værdi placerer evidensen i testfamilien for at kontrollere multiplicitet.",
            ),
            _t(
                "Ningún número aislado establece relevancia biológica.",
                "No single number establishes biological relevance.",
                "Intet enkelt tal etablerer biologisk relevans.",
            ),
            "",
        ),
        (
            "m03.p04",
            "DEBUGGING",
            _t(
                "Un informe selecciona genes con p < 0.05 entre 20 000 pruebas y no informa ajuste. Reconstruye el problema y corrige la estrategia.",
                "A report selects genes with p < 0.05 among 20,000 tests and reports no adjustment. Reconstruct the problem and correct the strategy.",
                "En rapport udvælger gener med p < 0,05 blandt 20.000 tests og rapporterer ingen justering. Rekonstruér problemet og korrigér strategien.",
            ),
            (
                _t(
                    "Calcula el orden esperado de falsos positivos bajo nulos.",
                    "Consider the expected order of false positives under nulls.",
                    "Overvej det forventede antal falske positive under nuller.",
                ),
                _t(
                    "Define la familia y el objetivo de error.",
                    "Define the family and error target.",
                    "Definér familien og fejlmålet.",
                ),
            ),
            _t(
                "Con miles de hipótesis, el umbral nominal produce numerosos falsos positivos. Debe definirse la familia, aplicar un procedimiento como BH para FDR, conservar la tabla completa, declarar umbrales de efecto y realizar validación independiente cuando la afirmación lo requiera.",
                "With thousands of hypotheses, a nominal threshold produces many false positives. The family should be defined, a procedure such as BH applied for FDR, the complete table retained, effect thresholds declared, and independent validation performed when the claim requires it.",
                "Med tusindvis af hypoteser producerer en nominel tærskel mange falske positive. Familien bør defineres, en procedure som BH anvendes til FDR, hele tabellen bevares, effekttærskler deklareres, og uafhængig validering udføres når påstanden kræver det.",
            ),
            _t(
                "El ajuste debe formar parte del plan, no añadirse después de elegir genes.",
                "Adjustment should be part of the plan, not added after choosing genes.",
                "Justering bør være del af planen, ikke tilføjes efter at gener er valgt.",
            ),
            "",
        ),
        (
            "m03.p05",
            "CODE_COMPLETION",
            _t(
                "Completa una función que añada valores BH y marque resultados con padj < alpha y |log2fc| >= min_effect.",
                "Complete a function that adds BH values and marks results with padj < alpha and |log2fc| >= min_effect.",
                "Færdiggør en funktion, der tilføjer BH-værdier og markerer resultater med padj < alpha og |log2fc| >= min_effect.",
            ),
            (
                _t(
                    "Usa p.adjust con method = 'BH'.",
                    "Use p.adjust with method = 'BH'.",
                    "Brug p.adjust med method = 'BH'.",
                ),
                _t(
                    "Devuelve la tabla completa.",
                    "Return the complete table.",
                    "Returnér hele tabellen.",
                ),
            ),
            _t(
                "mark_results <- function(tab, alpha = 0.05, min_effect = 1) { tab$padj <- p.adjust(tab$pvalue, method = 'BH'); tab$selected <- tab$padj < alpha & abs(tab$log2fc) >= min_effect; tab }",
                "mark_results <- function(tab, alpha = 0.05, min_effect = 1) { tab$padj <- p.adjust(tab$pvalue, method = 'BH'); tab$selected <- tab$padj < alpha & abs(tab$log2fc) >= min_effect; tab }",
                "mark_results <- function(tab, alpha = 0.05, min_effect = 1) { tab$padj <- p.adjust(tab$pvalue, method = 'BH'); tab$selected <- tab$padj < alpha & abs(tab$log2fc) >= min_effect; tab }",
            ),
            _t(
                "La función conserva todas las hipótesis y separa control de error de relevancia mínima.",
                "The function retains all hypotheses and separates error control from minimum relevance.",
                "Funktionen bevarer alle hypoteser og adskiller fejlkontrol fra minimumsrelevans.",
            ),
            "mark_results <- function(tab, alpha = 0.05, min_effect = 1) {\n  # add padj and selected columns\n}",
        ),
        (
            "m03.p06",
            "ORAL_EXPLANATION",
            _t(
                "Prepara una explicación de 90 segundos: un gen tiene padj = 0.01 y log2FC = 0.08. ¿Qué puedes y qué no puedes concluir?",
                "Prepare a 90-second explanation: a gene has padj = 0.01 and log2FC = 0.08. What can and cannot be concluded?",
                "Forbered en 90-sekunders forklaring: et gen har padj = 0,01 og log2FC = 0,08. Hvad kan og kan ikke konkluderes?",
            ),
            (
                _t(
                    "Separa evidencia estadística y magnitud.",
                    "Separate statistical evidence and magnitude.",
                    "Adskil statistisk evidens og størrelse.",
                ),
                _t(
                    "Menciona precisión, contexto y validación.",
                    "Mention precision, context, and validation.",
                    "Nævn præcision, kontekst og validering.",
                ),
            ),
            _t(
                "El resultado aporta evidencia contra el nulo dentro del procedimiento de FDR, pero la magnitud estimada es pequeña. Deben examinarse intervalo, abundancia, escala, calidad y relevancia biológica. No prueba causalidad, mecanismo, utilidad clínica ni replicación. Puede ser preciso pero de efecto trivial para la pregunta aplicada.",
                "The result provides evidence against the null within the FDR procedure, but the estimated magnitude is small. The interval, abundance, scale, quality, and biological relevance should be examined. It does not prove causality, mechanism, clinical utility, or replication. It may be precise yet practically trivial for the applied question.",
                "Resultatet giver evidens mod nulhypotesen inden for FDR-proceduren, men den estimerede størrelse er lille. Interval, abundans, skala, kvalitet og biologisk relevans bør undersøges. Det beviser ikke kausalitet, mekanisme, klinisk nytte eller replikation. Det kan være præcist, men praktisk trivielt for det anvendte spørgsmål.",
            ),
            _t(
                "Una respuesta madura limita la afirmación al estimando y al diseño.",
                "A mature answer limits the claim to the estimand and design.",
                "Et modent svar begrænser påstanden til estimand og design.",
            ),
            "",
        ),
    ),
    mcqs=(
        _mcq(
            "q01",
            _t(
                "¿Qué define directamente la comparación científica de interés?",
                "What directly defines the scientific comparison of interest?",
                "Hvad definerer direkte den videnskabelige sammenligning af interesse?",
            ),
            (
                _option("a", _t("El contraste", "The contrast", "Kontrasten")),
                _option("b", _t("El número de genes", "The number of genes", "Antallet af gener")),
                _option("c", _t("La paleta de color", "The color palette", "Farvepaletten")),
                _option("d", _t("El orden de filas", "The row order", "Rækkerækkefølgen")),
            ),
            "a",
            _t(
                "El contraste especifica la combinación de coeficientes que responde a la pregunta.",
                "The contrast specifies the coefficient combination answering the question.",
                "Kontrasten angiver den koefficientkombination, der besvarer spørgsmålet.",
            ),
        ),
        _mcq(
            "q02",
            _t(
                "¿Cuándo no puede separarse grupo de lote?",
                "When can group not be separated from batch?",
                "Hvornår kan gruppe ikke adskilles fra batch?",
            ),
            (
                _option(
                    "a",
                    _t(
                        "Cuando están completamente confundidos",
                        "When they are completely confounded",
                        "Når de er fuldstændigt confounded",
                    ),
                ),
                _option(
                    "b",
                    _t(
                        "Cuando hay muchos genes",
                        "When there are many genes",
                        "Når der er mange gener",
                    ),
                ),
                _option("c", _t("Cuando se usa R", "When R is used", "Når R bruges")),
                _option(
                    "d",
                    _t(
                        "Cuando el outcome es continuo",
                        "When the outcome is continuous",
                        "Når outcome er kontinuert",
                    ),
                ),
            ),
            "a",
            _t(
                "Sin combinación cruzada de grupo y lote, sus efectos no son identificables.",
                "Without cross-combination of group and batch, their effects are not identifiable.",
                "Uden krydskombination af gruppe og batch kan effekterne ikke identificeres.",
            ),
        ),
        _mcq(
            "q03",
            _t(
                "¿Qué modelo es conceptualmente compatible con conteos sobredispersos de RNA-seq?",
                "Which model is conceptually compatible with overdispersed RNA-seq counts?",
                "Hvilken model er konceptuelt kompatibel med overdispergerede RNA-seq-counts?",
            ),
            (
                _option(
                    "a",
                    _t(
                        "Un modelo de conteo con dispersión",
                        "A count model with dispersion",
                        "En count-model med dispersion",
                    ),
                ),
                _option(
                    "b",
                    _t(
                        "Una regresión sobre colores",
                        "A regression on colors",
                        "En regression på farver",
                    ),
                ),
                _option(
                    "c", _t("Una media sin error", "A mean without error", "Et middel uden fejl")
                ),
                _option(
                    "d",
                    _t(
                        "Un modelo que ignora profundidad",
                        "A model ignoring depth",
                        "En model der ignorerer dybde",
                    ),
                ),
            ),
            "a",
            _t(
                "La sobredispersión requiere variación adicional a una Poisson simple y ajuste por exposición.",
                "Overdispersion requires variation beyond a simple Poisson and exposure adjustment.",
                "Overdispersion kræver variation ud over en simpel Poisson og justering for eksponering.",
            ),
        ),
        _mcq(
            "q04",
            _t(
                "¿Qué comunica principalmente log2FC?",
                "What does log2FC primarily communicate?",
                "Hvad kommunikerer log2FC primært?",
            ),
            (
                _option(
                    "a",
                    _t(
                        "Dirección y magnitud relativa",
                        "Direction and relative magnitude",
                        "Retning og relativ størrelse",
                    ),
                ),
                _option(
                    "b",
                    _t(
                        "Probabilidad de que el gen sea verdadero",
                        "Probability that the gene is true",
                        "Sandsynlighed for at genet er sandt",
                    ),
                ),
                _option("c", _t("Número de pruebas", "Number of tests", "Antal tests")),
                _option(
                    "d", _t("Calidad de anotación", "Annotation quality", "Annoteringskvalitet")
                ),
            ),
            "a",
            _t(
                "El log2 fold change describe una razón en escala logarítmica.",
                "The log2 fold change describes a ratio on a logarithmic scale.",
                "Log2 fold change beskriver et forhold på logaritmisk skala.",
            ),
        ),
        _mcq(
            "q05",
            _t(
                "¿Qué controla Benjamini-Hochberg bajo sus supuestos?",
                "What does Benjamini-Hochberg control under its assumptions?",
                "Hvad kontrollerer Benjamini-Hochberg under sine antagelser?",
            ),
            (
                _option(
                    "a",
                    _t(
                        "La proporción esperada de falsos descubrimientos entre los declarados",
                        "The expected proportion of false discoveries among declared discoveries",
                        "Den forventede andel af falske fund blandt deklarerede fund",
                    ),
                ),
                _option(
                    "b",
                    _t(
                        "La probabilidad de que cada gen sea verdadero",
                        "The probability every gene is true",
                        "Sandsynligheden for at hvert gen er sandt",
                    ),
                ),
                _option("c", _t("El tamaño del efecto", "The effect size", "Effektstørrelsen")),
                _option("d", _t("El efecto de lote", "The batch effect", "Batcheffekten")),
            ),
            "a",
            _t(
                "FDR es una propiedad del conjunto de descubrimientos, no una probabilidad posterior por gen.",
                "FDR is a property of the discovery set, not a posterior probability per gene.",
                "FDR er en egenskab ved fundmængden, ikke en posterior sandsynlighed pr. gen.",
            ),
        ),
        _mcq(
            "q06",
            _t(
                "¿Qué práctica invalida la interpretación planificada de multiplicidad?",
                "Which practice invalidates the planned multiplicity interpretation?",
                "Hvilken praksis ugyldiggør den planlagte fortolkning af multiplicitet?",
            ),
            (
                _option(
                    "a",
                    _t(
                        "Elegir genes después de ver p-values y ajustar sólo esos",
                        "Choose genes after seeing p-values and adjust only those",
                        "Vælg gener efter at have set p-værdier og justér kun dem",
                    ),
                ),
                _option(
                    "b",
                    _t(
                        "Conservar la tabla completa",
                        "Retain the complete table",
                        "Bevar hele tabellen",
                    ),
                ),
                _option("c", _t("Declarar la familia", "Declare the family", "Deklarér familien")),
                _option(
                    "d",
                    _t(
                        "Informar tamaños de efecto",
                        "Report effect sizes",
                        "Rapportér effektstørrelser",
                    ),
                ),
            ),
            "a",
            _t(
                "La familia no debe redefinirse usando los mismos resultados que se ajustan.",
                "The family should not be redefined using the results being adjusted.",
                "Familien bør ikke omdefineres ved hjælp af de resultater, der justeres.",
            ),
        ),
        _mcq(
            "q07",
            _t(
                "¿Qué conclusión es compatible con padj pequeño y efecto muy pequeño?",
                "Which conclusion is compatible with a small adjusted p-value and a very small effect?",
                "Hvilken konklusion er kompatibel med en lille justeret p-værdi og en meget lille effekt?",
            ),
            (
                _option(
                    "a",
                    _t(
                        "Evidencia estadística con posible relevancia práctica limitada",
                        "Statistical evidence with possibly limited practical relevance",
                        "Statistisk evidens med muligvis begrænset praktisk relevans",
                    ),
                ),
                _option(
                    "b",
                    _t(
                        "Mecanismo causal probado",
                        "A proven causal mechanism",
                        "En bevist kausal mekanisme",
                    ),
                ),
                _option(
                    "c",
                    _t(
                        "Utilidad clínica garantizada",
                        "Guaranteed clinical utility",
                        "Garanteret klinisk nytte",
                    ),
                ),
                _option("d", _t("Error de software", "A software error", "En softwarefejl")),
            ),
            "a",
            _t(
                "Precisión estadística no convierte una magnitud pequeña en importancia aplicada.",
                "Statistical precision does not turn a small magnitude into applied importance.",
                "Statistisk præcision gør ikke en lille størrelse anvendt vigtig.",
            ),
        ),
        _mcq(
            "q08",
            _t(
                "¿Qué debe verificarse antes de interpretar un coeficiente?",
                "What should be checked before interpreting a coefficient?",
                "Hvad bør kontrolleres før en koefficient fortolkes?",
            ),
            (
                _option(
                    "a",
                    _t(
                        "Codificación, referencia y demás términos del modelo",
                        "Coding, reference, and other model terms",
                        "Kodning, reference og øvrige modelled",
                    ),
                ),
                _option("b", _t("Sólo su signo", "Only its sign", "Kun dets fortegn")),
                _option("c", _t("Sólo el valor p", "Only the p-value", "Kun p-værdien")),
                _option("d", _t("El color del gráfico", "The plot color", "Plottets farve")),
            ),
            "a",
            _t(
                "Los coeficientes son condicionales a la parametrización y al diseño.",
                "Coefficients are conditional on parameterization and design.",
                "Koefficienter er betinget af parametrisering og design.",
            ),
        ),
    ),
    true_false=(
        _tf(
            "tf01",
            _t(
                "Una matriz de diseño puede recuperar información ausente por confusión perfecta.",
                "A design matrix can recover information absent because of perfect confounding.",
                "En designmatrix kan genskabe information, der mangler på grund af perfekt confounding.",
            ),
            False,
            _t(
                "Ningún método estadístico separa efectos no identificables por el diseño.",
                "No statistical method separates effects that the design does not identify.",
                "Ingen statistisk metode adskiller effekter, som designet ikke identificerer.",
            ),
        ),
        _tf(
            "tf02",
            _t(
                "El coeficiente de grupo depende del nivel de referencia y de las covariables incluidas.",
                "The group coefficient depends on reference level and included covariates.",
                "Gruppekoefficienten afhænger af referenceniveau og inkluderede kovariater.",
            ),
            True,
            _t(
                "La interpretación es condicional a la parametrización.",
                "Interpretation is conditional on parameterization.",
                "Fortolkningen er betinget af parametrisering.",
            ),
        ),
        _tf(
            "tf03",
            _t(
                "Los valores log-transformados siempre deben introducirse en DESeq2 como si fueran conteos.",
                "Log-transformed values should always be entered into DESeq2 as counts.",
                "Log-transformerede værdier bør altid indtastes i DESeq2 som counts.",
            ),
            False,
            _t(
                "Los modelos de conteo requieren la escala de entrada especificada por el método.",
                "Count models require the input scale specified by the method.",
                "Count-modeller kræver den inputskala, som metoden specificerer.",
            ),
        ),
        _tf(
            "tf04",
            _t(
                "Un valor p pequeño mide directamente el tamaño del efecto.",
                "A small p-value directly measures effect size.",
                "En lille p-værdi måler direkte effektstørrelse.",
            ),
            False,
            _t(
                "El valor p depende del efecto, variabilidad, tamaño muestral y modelo.",
                "The p-value depends on effect, variability, sample size, and model.",
                "P-værdien afhænger af effekt, variation, stikprøvestørrelse og model.",
            ),
        ),
        _tf(
            "tf05",
            _t(
                "Un log2FC de 1 suele corresponder a una razón de dos.",
                "A log2FC of 1 commonly corresponds to a ratio of two.",
                "En log2FC på 1 svarer ofte til et forhold på to.",
            ),
            True,
            _t(
                "Dos elevado a uno es dos bajo la definición habitual.",
                "Two to the power of one is two under the usual definition.",
                "To opløftet i første er to under den sædvanlige definition.",
            ),
        ),
        _tf(
            "tf06",
            _t(
                "BH convierte cada valor ajustado en la probabilidad de que el gen sea un falso positivo.",
                "BH turns each adjusted value into the probability that the gene is a false positive.",
                "BH gør hver justeret værdi til sandsynligheden for, at genet er falsk positivt.",
            ),
            False,
            _t(
                "La interpretación de FDR es sobre el procedimiento y el conjunto de descubrimientos.",
                "FDR interpretation concerns the procedure and discovery set.",
                "FDR-fortolkning vedrører proceduren og fundmængden.",
            ),
        ),
        _tf(
            "tf07",
            _t(
                "Los umbrales de efecto y error responden a preguntas distintas.",
                "Effect and error thresholds answer different questions.",
                "Effekt- og fejltærskler besvarer forskellige spørgsmål.",
            ),
            True,
            _t(
                "Uno expresa magnitud mínima; el otro controla evidencia y multiplicidad.",
                "One expresses minimum magnitude; the other controls evidence and multiplicity.",
                "Den ene udtrykker minimumsstørrelse; den anden kontrollerer evidens og multiplicitet.",
            ),
        ),
        _tf(
            "tf08",
            _t(
                "Un hallazgo diferencial demuestra causalidad biológica.",
                "A differential finding proves biological causality.",
                "Et differentialt fund beviser biologisk kausalitet.",
            ),
            False,
            _t(
                "La asociación estimada está limitada por diseño, modelo y posibles factores de confusión.",
                "The estimated association is limited by design, model, and possible confounding.",
                "Den estimerede association er begrænset af design, model og mulig confounding.",
            ),
        ),
    ),
    tutor=(
        _t(
            "El tutor debe comenzar por estimando, diseño y escala antes de discutir paquetes o valores p. Debe exigir tamaños de efecto, incertidumbre, multiplicidad y límites de inferencia.",
            "The tutor should begin with estimand, design, and scale before discussing packages or p-values. It should require effect sizes, uncertainty, multiplicity, and inference limits.",
            "Tutoren bør begynde med estimand, design og skala før pakker eller p-værdier diskuteres. Den bør kræve effektstørrelser, usikkerhed, multiplicitet og inferensgrænser.",
        ),
        (
            _t(
                "El contraste define la comparación y el diseño define su contexto.",
                "The contrast defines the comparison and the design defines its context.",
                "Kontrasten definerer sammenligningen, og designet definerer dens kontekst.",
            ),
            _t(
                "La escala y el proceso de medida determinan la familia de modelos adecuada.",
                "Scale and measurement process determine the suitable model family.",
                "Skala og måleproces bestemmer den passende modelfamilie.",
            ),
            _t(
                "Efecto, intervalo y valor ajustado deben interpretarse juntos.",
                "Effect, interval, and adjusted value should be interpreted together.",
                "Effekt, interval og justeret værdi bør fortolkes sammen.",
            ),
            _t(
                "La multiplicidad pertenece a una familia de hipótesis declarada.",
                "Multiplicity belongs to a declared hypothesis family.",
                "Multiplicitet tilhører en deklareret hypotese-familie.",
            ),
        ),
        (
            _t(
                "Interpretar p como probabilidad de que el nulo sea verdadero.",
                "Interpreting p as the probability the null is true.",
                "At fortolke p som sandsynligheden for at nulhypotesen er sand.",
            ),
            _t(
                "Ignorar confusión entre grupo y lote.",
                "Ignoring confounding between group and batch.",
                "At ignorere confounding mellem gruppe og batch.",
            ),
            _t(
                "Introducir valores transformados en modelos de conteo sin comprobar el contrato.",
                "Entering transformed values into count models without checking the contract.",
                "At indtaste transformerede værdier i count-modeller uden at kontrollere kontrakten.",
            ),
            _t(
                "Seleccionar genes por valores p nominales entre miles de pruebas.",
                "Selecting genes by nominal p-values among thousands of tests.",
                "At vælge gener efter nominelle p-værdier blandt tusindvis af tests.",
            ),
        ),
        (
            _t(
                "¿Cuál es exactamente el estimando y el contraste?",
                "What exactly are the estimand and contrast?",
                "Hvad er præcis estimand og kontrast?",
            ),
            _t(
                "¿La escala de entrada coincide con el modelo?",
                "Does the input scale match the model?",
                "Matcher inputskalaen modellen?",
            ),
            _t(
                "¿Qué magnitud e intervalo acompañan al valor ajustado?",
                "What magnitude and interval accompany the adjusted value?",
                "Hvilken størrelse og hvilket interval ledsager den justerede værdi?",
            ),
            _t(
                "¿Cómo se definió la familia de hipótesis?",
                "How was the hypothesis family defined?",
                "Hvordan blev hypotese-familien defineret?",
            ),
        ),
        (
            _t(
                "Formula diseño y contraste identificables.",
                "Formulates an identifiable design and contrast.",
                "Formulerer et identificerbart design og en kontrast.",
            ),
            _t(
                "Elige un modelo compatible con escala y variación.",
                "Chooses a model compatible with scale and variation.",
                "Vælger en model kompatibel med skala og variation.",
            ),
            _t(
                "Interpreta efecto, incertidumbre y multiplicidad.",
                "Interprets effect, uncertainty, and multiplicity.",
                "Fortolker effekt, usikkerhed og multiplicitet.",
            ),
            _t(
                "Limita conclusiones a diseño, datos y validación.",
                "Limits conclusions to design, data, and validation.",
                "Begrænser konklusioner til design, data og validering.",
            ),
        ),
        (
            _t(
                "No asignar causalidad ni utilidad clínica a partir de asociación diferencial.",
                "Do not assign causality or clinical utility from differential association.",
                "Tildel ikke kausalitet eller klinisk nytte ud fra differential association.",
            ),
            _t(
                "No inventar el diseño, la escala o la familia de pruebas.",
                "Do not invent design, scale, or hypothesis family.",
                "Opfind ikke design, skala eller hypotese-familie.",
            ),
            _t(
                "No recomendar un paquete sin explicar su contrato de entrada y modelo.",
                "Do not recommend a package without explaining its input contract and model.",
                "Anbefal ikke en pakke uden at forklare dens inputkontrakt og model.",
            ),
            _t(
                "Responder en el idioma activo y mantener términos estadísticos precisos.",
                "Respond in the active language and keep statistical terms precise.",
                "Svar på det aktive sprog og bevar præcise statistiske termer.",
            ),
        ),
        (
            "https://odin.sdu.dk/sitecore/index.php?a=searchfagbesk&internkode=BMB831&lang=en",
            "https://bioconductor.org/packages/release/bioc/html/DESeq2.html",
            "https://bioconductor.org/packages/release/bioc/html/edgeR.html",
            "https://bioconductor.org/packages/release/bioc/html/limma.html",
        ),
    ),
)

LOCALIZED_MODULE_03_DIFFERENTIAL_MODELING = build_module(_SPEC)
LOCALIZED_OBJECTIVE_QUESTION_BANK_03 = build_question_bank(_SPEC)


def materialize_module_03_question_bank(
    locale: AppLocale | str = AppLocale.SPANISH_SPAIN,
) -> tuple[AssessmentItem, ...]:
    """Materialize the stable module 3 objective bank."""

    return materialize_bank(LOCALIZED_OBJECTIVE_QUESTION_BANK_03, locale)


MODULE_03_DIFFERENTIAL_MODELING: LearningModule = (
    LOCALIZED_MODULE_03_DIFFERENTIAL_MODELING.materialize(AppLocale.SPANISH_SPAIN)
)
OBJECTIVE_QUESTION_BANK_03 = materialize_module_03_question_bank()

__all__ = [
    "LOCALIZED_MODULE_03_DIFFERENTIAL_MODELING",
    "LOCALIZED_OBJECTIVE_QUESTION_BANK_03",
    "MODULE_03_DIFFERENTIAL_MODELING",
    "OBJECTIVE_QUESTION_BANK_03",
    "materialize_module_03_question_bank",
]
