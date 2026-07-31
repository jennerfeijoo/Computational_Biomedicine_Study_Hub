"""BMB830 module 2: data quality, descriptive statistics, and visualization."""

from __future__ import annotations

from ...i18n import AppLocale
from ..localized_models import LocalizedLearningModule
from ..models import AssessmentItem, LearningModule
from .standard import StandardModuleSpec, build_module, build_question_bank, materialize_bank

_SPEC = StandardModuleSpec(
    module_id="bmb830.m02",
    title=(
        "Calidad, resumen y visualización de datos",
        "Data quality, summary, and visualization",
        "Datakvalitet, opsummering og visualisering",
    ),
    summary=(
        "Audita datos biológicos, elige resúmenes compatibles con su distribución y construye gráficos que preserven escala, grupos, tamaños muestrales e incertidumbre.",
        "Audit biological data, choose summaries compatible with their distribution, and build plots that preserve scale, groups, sample sizes, and uncertainty.",
        "Gennemgå biologiske data, vælg opsummeringer der passer til fordelingen, og byg figurer som bevarer skala, grupper, stikprøvestørrelser og usikkerhed.",
    ),
    objectives=(
        (
            "m02.o1",
            (
                "Distinguir tendencia central, dispersión, forma y valores extremos.",
                "Distinguish central tendency, dispersion, shape, and extreme values.",
                "Skelne mellem central tendens, spredning, form og ekstreme værdier.",
            ),
        ),
        (
            "m02.o2",
            (
                "Evaluar calidad mediante rangos, ausencia, duplicados y coherencia entre variables.",
                "Assess quality through ranges, missingness, duplicates, and cross-variable consistency.",
                "Vurdere kvalitet gennem intervaller, manglende data, dubletter og konsistens mellem variable.",
            ),
        ),
        (
            "m02.o3",
            (
                "Seleccionar gráficos coherentes con el tipo de variable y la pregunta.",
                "Select plots consistent with variable type and the question.",
                "Vælge figurer i overensstemmelse med variabeltype og spørgsmål.",
            ),
        ),
        (
            "m02.o4",
            (
                "Interpretar visualizaciones sin confundir patrón descriptivo, inferencia y causalidad.",
                "Interpret visualizations without confusing descriptive pattern, inference, and causality.",
                "Fortolke visualiseringer uden at forveksle deskriptivt mønster, inferens og kausalitet.",
            ),
        ),
    ),
    concepts=(
        (
            "distribution",
            (
                "Centro, dispersión y forma",
                "Centre, dispersion, and shape",
                "Centrum, spredning og form",
            ),
            (
                "La media resume el balance numérico y es sensible a extremos; la mediana es más robusta. La desviación estándar describe dispersión alrededor de la media y el IQR resume el 50 % central. Ningún número único describe asimetría, multimodalidad o colas.",
                "The mean summarises numerical balance and is sensitive to extremes; the median is more robust. Standard deviation describes spread around the mean and IQR summarises the central 50%. No single number captures skewness, multimodality, or tails.",
                "Gennemsnittet opsummerer numerisk balance og er følsomt over for ekstremer; medianen er mere robust. Standardafvigelsen beskriver spredning omkring gennemsnittet, og IQR opsummerer de centrale 50 %. Intet enkelt tal beskriver skævhed, multimodalitet eller haler.",
            ),
            (
                (
                    "Combina centro, dispersión y una inspección de la forma.",
                    "Combine centre, dispersion, and inspection of shape.",
                    "Kombinér centrum, spredning og undersøgelse af formen.",
                ),
                (
                    "Un extremo se investiga; no se elimina automáticamente.",
                    "An extreme value is investigated, not removed automatically.",
                    "En ekstrem værdi undersøges og fjernes ikke automatisk.",
                ),
            ),
        ),
        (
            "quality-audit",
            (
                "Auditoría de calidad",
                "Quality audit",
                "Kvalitetskontrol",
            ),
            (
                "Una auditoría examina dimensiones, tipos, claves, rangos plausibles, ausencia y relaciones lógicas. Las reglas deben definirse antes de observar el resultado principal y cada exclusión debe conservar su motivo y procedencia.",
                "An audit examines dimensions, types, keys, plausible ranges, missingness, and logical relations. Rules should be defined before inspecting the primary result, and each exclusion should retain its reason and provenance.",
                "En kontrol undersøger dimensioner, typer, nøgler, plausible intervaller, manglende data og logiske relationer. Regler bør defineres før det primære resultat undersøges, og hver udelukkelse bør bevare begrundelse og proveniens.",
            ),
            (
                (
                    "Distingue errores imposibles de observaciones inusuales plausibles.",
                    "Distinguish impossible errors from plausible unusual observations.",
                    "Skeln mellem umulige fejl og plausible usædvanlige observationer.",
                ),
                (
                    "Reporta cuántas filas cambian en cada filtro.",
                    "Report how many rows change at each filter.",
                    "Rapportér hvor mange rækker der ændres ved hvert filter.",
                ),
            ),
        ),
        (
            "visual-encoding",
            (
                "Codificación visual",
                "Visual encoding",
                "Visuel kodning",
            ),
            (
                "Histogramas muestran distribuciones; boxplots resumen cuantiles; puntos muestran relaciones entre variables continuas; barras representan conteos o proporciones. Posición y longitud suelen comunicar cantidades con mayor precisión que área o color.",
                "Histograms show distributions; boxplots summarise quantiles; points show relations between continuous variables; bars represent counts or proportions. Position and length usually communicate quantities more precisely than area or colour.",
                "Histogrammer viser fordelinger; boxplots opsummerer kvantiler; punkter viser relationer mellem kontinuerte variable; søjler repræsenterer antal eller proportioner. Position og længde kommunikerer normalt mængder mere præcist end areal eller farve.",
            ),
            (
                (
                    "Muestra observaciones individuales cuando sea viable.",
                    "Show individual observations when feasible.",
                    "Vis individuelle observationer når det er muligt.",
                ),
                (
                    "Etiqueta unidades, transformaciones y denominadores.",
                    "Label units, transformations, and denominators.",
                    "Angiv enheder, transformationer og nævnere.",
                ),
            ),
        ),
        (
            "responsible-interpretation",
            (
                "Interpretación responsable",
                "Responsible interpretation",
                "Ansvarlig fortolkning",
            ),
            (
                "Un gráfico es una transformación de datos. Ejes truncados, escalas logarítmicas no declaradas, agregación excesiva y tamaños de grupo desiguales pueden alterar la impresión. Un patrón visual genera hipótesis, pero no demuestra significación ni causalidad.",
                "A plot is a transformation of data. Truncated axes, undeclared log scales, excessive aggregation, and unequal group sizes can alter impressions. A visual pattern generates hypotheses but proves neither significance nor causality.",
                "En figur er en transformation af data. Afkortede akser, ikke-erklærede logskalaer, overdreven aggregering og ulige gruppestørrelser kan ændre indtrykket. Et visuelt mønster skaber hypoteser, men beviser hverken signifikans eller kausalitet.",
            ),
            (
                (
                    "Separa descripción, inferencia y explicación causal.",
                    "Separate description, inference, and causal explanation.",
                    "Adskil beskrivelse, inferens og kausal forklaring.",
                ),
                (
                    "Incluye tamaño muestral e incertidumbre relevante.",
                    "Include sample size and relevant uncertainty.",
                    "Medtag stikprøvestørrelse og relevant usikkerhed.",
                ),
            ),
        ),
    ),
    examples=(
        (
            "m02.e01",
            (
                "Media, mediana e IQR ante un extremo",
                "Mean, median, and IQR with an extreme value",
                "Gennemsnit, median og IQR med en ekstrem værdi",
            ),
            (
                "Compara resúmenes de una medición que contiene un valor extremo.",
                "Compare summaries of a measurement containing an extreme value.",
                "Sammenlign opsummeringer af en måling med en ekstrem værdi.",
            ),
            (
                (
                    "La media incorpora la magnitud del extremo.",
                    "The mean incorporates the magnitude of the extreme value.",
                    "Gennemsnittet indarbejder den ekstreme værdis størrelse.",
                ),
                (
                    "La mediana y el IQR dependen del orden y son más robustos.",
                    "The median and IQR depend on order and are more robust.",
                    "Medianen og IQR afhænger af rækkefølge og er mere robuste.",
                ),
            ),
            """x <- c(4, 5, 5, 6, 30)
cat(sprintf("mean=%.1f\n", mean(x)))
cat(sprintf("median=%.1f\n", median(x)))
cat(sprintf("IQR=%.1f\n", IQR(x)))
""",
            """mean=10.0
median=5.0
IQR=1.0""",
            (
                "La discrepancia alerta sobre asimetría o extremos, pero no justifica por sí sola una exclusión.",
                "The discrepancy flags skewness or extremes but does not by itself justify exclusion.",
                "Forskellen peger på skævhed eller ekstremer, men begrunder ikke i sig selv udelukkelse.",
            ),
        ),
        (
            "m02.e02",
            (
                "Proporciones por grupo",
                "Group-wise proportions",
                "Proportioner efter gruppe",
            ),
            (
                "Calcula la proporción de respuesta dentro de cada grupo usando el denominador correcto.",
                "Calculate response proportion within each group using the correct denominator.",
                "Beregn responsandelen inden for hver gruppe med den korrekte nævner.",
            ),
            (
                (
                    "La tabla conserva los conteos originales.",
                    "The table preserves the original counts.",
                    "Tabellen bevarer de oprindelige antal.",
                ),
                (
                    "margin = 1 normaliza dentro de cada grupo.",
                    "margin = 1 normalises within each group.",
                    "margin = 1 normaliserer inden for hver gruppe.",
                ),
            ),
            """counts <- matrix(c(28, 72, 52, 48), nrow = 2, byrow = TRUE)
rownames(counts) <- c("control", "treated")
colnames(counts) <- c("no", "yes")
proportions <- prop.table(counts, margin = 1)
cat(sprintf("control_yes=%.2f\n", proportions["control", "yes"]))
cat(sprintf("treated_yes=%.2f\n", proportions["treated", "yes"]))
""",
            """control_yes=0.72
treated_yes=0.48""",
            (
                "Las proporciones son comparables porque cada fila utiliza su propio total como denominador.",
                "The proportions are comparable because each row uses its own total as denominator.",
                "Proportionerne kan sammenlignes, fordi hver række bruger sin egen total som nævner.",
            ),
        ),
    ),
    practices=(
        (
            "m02.p01",
            "DATA_INTERPRETATION",
            (
                "Explica qué sugieren media 10 y mediana 5 en una muestra pequeña.",
                "Explain what mean 10 and median 5 suggest in a small sample.",
                "Forklar hvad gennemsnit 10 og median 5 antyder i en lille stikprøve.",
            ),
            (("Inspecciona forma y extremos.", "Inspect shape and extremes.", "Undersøg form og ekstremer."),),
            (
                "Sugieren asimetría o un extremo influyente, que debe inspeccionarse.",
                "They suggest skewness or an influential extreme that should be inspected.",
                "De antyder skævhed eller en indflydelsesrig ekstrem værdi, som bør undersøges.",
            ),
            (
                "La diferencia no prueba que exista un error.",
                "The difference does not prove an error.",
                "Forskellen beviser ikke en fejl.",
            ),
            "",
        ),
        (
            "m02.p02",
            "PIPELINE_DESIGN",
            (
                "Diseña una auditoría antes de comparar grupos.",
                "Design an audit before comparing groups.",
                "Design en kontrol før grupper sammenlignes.",
            ),
            (("Incluye claves, tipos, rangos y NA.", "Include keys, types, ranges, and NA.", "Medtag nøgler, typer, intervaller og NA."),),
            (
                "Verificar dimensiones, claves, tipos, rangos, ausencia, coherencia y exclusiones.",
                "Check dimensions, keys, types, ranges, missingness, consistency, and exclusions.",
                "Kontrollér dimensioner, nøgler, typer, intervaller, manglende data, konsistens og udelukkelser.",
            ),
            (
                "Las reglas se establecen antes de inspeccionar el efecto principal.",
                "Rules are established before inspecting the primary effect.",
                "Regler fastlægges før den primære effekt undersøges.",
            ),
            "",
        ),
        (
            "m02.p03",
            "MULTIPLE_CHOICE",
            (
                "Elige un gráfico para una variable continua por dos grupos.",
                "Choose a plot for a continuous variable in two groups.",
                "Vælg en figur for en kontinuert variabel i to grupper.",
            ),
            (("Conserva observaciones individuales.", "Preserve individual observations.", "Bevar individuelle observationer."),),
            (
                "Puntos por grupo con boxplot o resumen superpuesto.",
                "Group-wise points with a boxplot or summary overlay.",
                "Punkter efter gruppe med boxplot eller overlagt opsummering.",
            ),
            (
                "Una barra de medias oculta distribución y tamaño muestral.",
                "A mean bar hides distribution and sample size.",
                "En gennemsnitssøjle skjuler fordeling og stikprøvestørrelse.",
            ),
            "",
        ),
        (
            "m02.p04",
            "CODE_COMPLETION",
            (
                "Completa el cálculo del IQR de x.",
                "Complete the calculation of the IQR of x.",
                "Fuldfør beregningen af IQR for x.",
            ),
            (("Usa la función base IQR.", "Use the base IQR function.", "Brug basisfunktionen IQR."),),
            ("IQR(x)", "IQR(x)", "IQR(x)"),
            (
                "IQR resume la mitad central de la distribución.",
                "IQR summarises the central half of the distribution.",
                "IQR opsummerer den centrale halvdel af fordelingen.",
            ),
            "result <- ______",
        ),
        (
            "m02.p05",
            "DEBUGGING",
            (
                "Corrige una proporción calculada con el total global cuando la pregunta es dentro de grupo.",
                "Correct a proportion calculated with the global total when the question is within group.",
                "Korrigér en proportion beregnet med den globale total, når spørgsmålet gælder inden for gruppe.",
            ),
            (("Normaliza filas.", "Normalise rows.", "Normalisér rækker."),),
            (
                "Usar prop.table(counts, margin = 1).",
                "Use prop.table(counts, margin = 1).",
                "Brug prop.table(counts, margin = 1).",
            ),
            (
                "El denominador debe corresponder a la población descrita.",
                "The denominator must match the population described.",
                "Nævneren skal svare til den beskrevne population.",
            ),
            "prop.table(counts)",
        ),
        (
            "m02.p06",
            "ORAL_EXPLANATION",
            (
                "Explica por qué un patrón visual no demuestra causalidad.",
                "Explain why a visual pattern does not demonstrate causality.",
                "Forklar hvorfor et visuelt mønster ikke demonstrerer kausalitet.",
            ),
            (("Considera confusión y diseño.", "Consider confounding and design.", "Overvej confounding og design."),),
            (
                "El gráfico describe asociación observada; diseño, temporalidad y control de confusión sustentan afirmaciones causales.",
                "The plot describes observed association; design, temporality, and confounding control support causal claims.",
                "Figuren beskriver observeret association; design, temporalitet og kontrol af confounding understøtter kausale påstande.",
            ),
            (
                "La claridad visual no añade identificación causal.",
                "Visual clarity does not add causal identification.",
                "Visuel klarhed tilføjer ikke kausal identifikation.",
            ),
            "",
        ),
    ),
    mcqs=(
        ("001", ("¿Qué resumen es más robusto ante un extremo?", "Which summary is more robust to an extreme value?", "Hvilket mål er mere robust over for en ekstrem værdi?"), (("mean", ("Media", "Mean", "Gennemsnit")), ("median", ("Mediana", "Median", "Median")), ("range", ("Rango", "Range", "Interval")), ("sum", ("Suma", "Sum", "Sum"))), "median", ("La mediana depende del orden.", "The median depends on order.", "Medianen afhænger af rækkefølge.")),
        ("002", ("¿Qué resume el 50 % central?", "What summarises the central 50%?", "Hvad opsummerer de centrale 50 %?"), (("iqr", ("IQR", "IQR", "IQR")), ("mean", ("Media", "Mean", "Gennemsnit")), ("max", ("Máximo", "Maximum", "Maksimum")), ("n", ("Tamaño", "Sample size", "Stikprøvestørrelse"))), "iqr", ("IQR es Q3 menos Q1.", "IQR is Q3 minus Q1.", "IQR er Q3 minus Q1.")),
        ("003", ("¿Qué gráfico muestra una distribución continua?", "Which plot shows a continuous distribution?", "Hvilken figur viser en kontinuert fordeling?"), (("hist", ("Histograma", "Histogram", "Histogram")), ("pie", ("Circular", "Pie chart", "Cirkeldiagram")), ("table", ("Tabla", "Table", "Tabel")), ("label", ("Etiqueta", "Label", "Etiket"))), "hist", ("El histograma agrupa valores por intervalos.", "A histogram bins values into intervals.", "Et histogram grupperer værdier i intervaller.")),
        ("004", ("¿Qué debe registrarse al excluir una fila?", "What should be recorded when excluding a row?", "Hvad bør registreres når en række udelukkes?"), (("reason", ("Motivo y regla", "Reason and rule", "Begrundelse og regel")), ("colour", ("Color", "Colour", "Farve")), ("screen", ("Captura", "Screenshot", "Skærmbillede")), ("nothing", ("Nada", "Nothing", "Intet"))), "reason", ("La exclusión debe ser trazable.", "Exclusion must be traceable.", "Udelukkelse skal kunne spores.")),
        ("005", ("¿Qué normaliza proporciones dentro de filas?", "What normalises proportions within rows?", "Hvad normaliserer proportioner inden for rækker?"), (("row", ("prop.table(x, 1)", "prop.table(x, 1)", "prop.table(x, 1)")), ("all", ("prop.table(x)", "prop.table(x)", "prop.table(x)")), ("mean", ("mean(x)", "mean(x)", "mean(x)")), ("sort", ("sort(x)", "sort(x)", "sort(x)"))), "row", ("margin = 1 utiliza cada fila como denominador.", "margin = 1 uses each row as denominator.", "margin = 1 bruger hver række som nævner.")),
        ("006", ("¿Qué puede distorsionar la impresión visual?", "What can distort visual impression?", "Hvad kan forvrænge det visuelle indtryk?"), (("truncated", ("Eje truncado", "Truncated axis", "Afkortet akse")), ("units", ("Unidades claras", "Clear units", "Klare enheder")), ("n", ("Mostrar n", "Showing n", "At vise n")), ("points", ("Mostrar puntos", "Showing points", "At vise punkter"))), "truncated", ("Un eje truncado amplifica diferencias visuales.", "A truncated axis amplifies visual differences.", "En afkortet akse forstærker visuelle forskelle.")),
        ("007", ("¿Qué diferencia debe investigarse, no borrarse?", "What difference should be investigated, not erased?", "Hvilken forskel bør undersøges og ikke slettes?"), (("outlier", ("Valor extremo", "Extreme value", "Ekstrem værdi")), ("label", ("Etiqueta", "Label", "Etiket")), ("title", ("Título", "Title", "Titel")), ("unit", ("Unidad", "Unit", "Enhed"))), "outlier", ("Puede ser error o biología real.", "It may be error or real biology.", "Det kan være en fejl eller reel biologi.")),
        ("008", ("¿Qué acompaña una comparación gráfica?", "What should accompany a graphical comparison?", "Hvad bør ledsage en grafisk sammenligning?"), (("sample", ("Tamaños de grupo", "Group sizes", "Gruppestørrelser")), ("logo", ("Logotipo", "Logo", "Logo")), ("animation", ("Animación", "Animation", "Animation")), ("random", ("Color aleatorio", "Random colour", "Tilfældig farve"))), "sample", ("El tamaño muestra cuánta evidencia sustenta el patrón.", "Size shows how much evidence supports the pattern.", "Størrelsen viser hvor meget evidens der understøtter mønstret.")),
    ),
    true_false=(
        ("009", ("La media siempre representa mejor el centro.", "The mean always represents centre best.", "Gennemsnittet repræsenterer altid centrum bedst."), False, ("Depende de forma y extremos.", "It depends on shape and extremes.", "Det afhænger af form og ekstremer.")),
        ("010", ("Un valor extremo es automáticamente un error.", "An extreme value is automatically an error.", "En ekstrem værdi er automatisk en fejl."), False, ("Requiere investigación y procedencia.", "It requires investigation and provenance.", "Det kræver undersøgelse og proveniens.")),
        ("011", ("IQR es robusto ante valores extremos.", "IQR is robust to extreme values.", "IQR er robust over for ekstreme værdier."), True, ("Depende de cuantiles centrales.", "It depends on central quantiles.", "Det afhænger af centrale kvantiler.")),
        ("012", ("Un boxplot muestra todas las observaciones.", "A boxplot shows every observation.", "Et boxplot viser alle observationer."), False, ("Resume cuantiles y posibles extremos.", "It summarises quantiles and possible extremes.", "Det opsummerer kvantiler og mulige ekstremer.")),
        ("013", ("Los porcentajes requieren un denominador declarado.", "Percentages require a declared denominator.", "Procenter kræver en erklæret nævner."), True, ("El mismo numerador puede producir porcentajes distintos.", "The same numerator can yield different percentages.", "Samme tæller kan give forskellige procenter.")),
        ("014", ("Una escala logarítmica debe indicarse.", "A logarithmic scale should be stated.", "En logaritmisk skala bør angives."), True, ("La transformación cambia distancias visuales.", "The transformation changes visual distances.", "Transformationen ændrer visuelle afstande.")),
        ("015", ("Un gráfico por sí solo establece significación estadística.", "A plot alone establishes statistical significance.", "En figur alene fastslår statistisk signifikans."), False, ("La inferencia exige un modelo y supuestos.", "Inference requires a model and assumptions.", "Inferens kræver en model og antagelser.")),
        ("016", ("Mostrar puntos puede revelar heterogeneidad oculta por una media.", "Showing points can reveal heterogeneity hidden by a mean.", "At vise punkter kan afsløre heterogenitet skjult af et gennemsnit."), True, ("La agregación puede ocultar estructura.", "Aggregation may hide structure.", "Aggregering kan skjule struktur.")),
    ),
    tutor=(
        (
            "El análisis descriptivo válido combina auditoría, resúmenes compatibles con la distribución, visualización transparente y separación explícita entre observación, inferencia y causalidad.",
            "Valid descriptive analysis combines auditing, distribution-compatible summaries, transparent visualization, and explicit separation of observation, inference, and causality.",
            "Gyldig deskriptiv analyse kombinerer kontrol, fordelingspassende opsummeringer, transparent visualisering og tydelig adskillelse af observation, inferens og kausalitet.",
        ),
        (
            ("Media y mediana responden distinto a extremos.", "Mean and median respond differently to extremes.", "Gennemsnit og median reagerer forskelligt på ekstremer."),
            ("IQR resume el 50 % central.", "IQR summarises the central 50%.", "IQR opsummerer de centrale 50 %."),
            ("Cada porcentaje requiere denominador.", "Every percentage requires a denominator.", "Hver procent kræver en nævner."),
            ("Un gráfico no identifica causalidad.", "A plot does not identify causality.", "En figur identificerer ikke kausalitet."),
        ),
        (
            ("Eliminar extremos por regla automática.", "Automatically deleting extremes.", "Automatisk at slette ekstremer."),
            ("Usar barras para ocultar datos continuos.", "Using bars to hide continuous data.", "At bruge søjler til at skjule kontinuerte data."),
            ("Interpretar asociación como causa.", "Interpreting association as cause.", "At fortolke association som årsag."),
        ),
        (
            ("¿Qué distribución hay detrás del resumen?", "What distribution lies behind the summary?", "Hvilken fordeling ligger bag opsummeringen?"),
            ("¿Cuál es el denominador?", "What is the denominator?", "Hvad er nævneren?"),
            ("¿Qué puede ocultar esta visualización?", "What might this visualization hide?", "Hvad kan denne visualisering skjule?"),
        ),
        (
            ("Audita antes de resumir.", "Audits before summarising.", "Kontrollerer før opsummering."),
            ("Justifica centro y dispersión.", "Justifies centre and dispersion.", "Begrunder centrum og spredning."),
            ("Separa descripción e inferencia.", "Separates description and inference.", "Adskiller beskrivelse og inferens."),
        ),
        (
            ("No inventar valores ni tamaños muestrales.", "Do not invent values or sample sizes.", "Opfind ikke værdier eller stikprøvestørrelser."),
            ("No recomendar exclusiones sin procedencia.", "Do not recommend exclusions without provenance.", "Anbefal ikke udelukkelser uden proveniens."),
            ("Responder en el idioma activo.", "Respond in the active language.", "Svar på det aktive sprog."),
        ),
        (
            "SDU ODIN BMB830 active course description approved 2025-03-06",
            "R base documentation: summary statistics and graphics",
            "Graphical principles for transparent scientific reporting",
        ),
    ),
)

LOCALIZED_MODULE_02_DATA_SUMMARY = build_module(_SPEC)
LOCALIZED_OBJECTIVE_QUESTION_BANK_02 = build_question_bank(_SPEC)
MODULE_02_DATA_SUMMARY: LearningModule = LOCALIZED_MODULE_02_DATA_SUMMARY.materialize(
    AppLocale.SPANISH_SPAIN
)
OBJECTIVE_QUESTION_BANK_02: tuple[AssessmentItem, ...] = materialize_bank(
    LOCALIZED_OBJECTIVE_QUESTION_BANK_02
)


def materialize_module_02_question_bank(
    locale: AppLocale | str = AppLocale.SPANISH_SPAIN,
) -> tuple[AssessmentItem, ...]:
    """Return the module-2 objective bank in one locale."""

    return materialize_bank(LOCALIZED_OBJECTIVE_QUESTION_BANK_02, locale)


__all__ = [
    "LOCALIZED_MODULE_02_DATA_SUMMARY",
    "LOCALIZED_OBJECTIVE_QUESTION_BANK_02",
    "MODULE_02_DATA_SUMMARY",
    "OBJECTIVE_QUESTION_BANK_02",
    "materialize_module_02_question_bank",
]
