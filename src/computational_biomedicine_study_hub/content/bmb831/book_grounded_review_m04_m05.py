"""Focused source-grounded review extensions for BMB831 modules 4 and 5."""

from __future__ import annotations

from dataclasses import replace

from ...learning.activity_types import ActivityType
from ..localized_models import LocalizedLearningModule
from .authoring import concept, example, objective, objective_mcq, practice
from .book_grounded_audit import ModuleSourceAudit


def review_module_source_audit(
    audits: tuple[ModuleSourceAudit, ...],
) -> tuple[ModuleSourceAudit, ...]:
    """Mark the completed M04-M05 reviews while preserving the stable registry."""

    updated: list[ModuleSourceAudit] = []
    for audit in audits:
        if audit.module_id == "bmb831.m04":
            updated.append(
                replace(
                    audit,
                    state="consistent",
                    finding=(
                        "Existing PCA, distance, clustering, batch, stability, and leakage coverage "
                        "is consistent. The focused review identified one missing finite-sample "
                        "boundary: after centering, at most min(p, n - 1) principal components can "
                        "carry non-zero sample variation, and near-tied components should be "
                        "interpreted as a potentially unstable subspace rather than fixed axes."
                    ),
                    implemented_change=(
                        "Added a trilingual finite-rank and subspace-stability explanation, a "
                        "deterministic rank-ceiling example, a high-dimensional interpretation "
                        "exercise, and a stable objective assessment item."
                    ),
                )
            )
        elif audit.module_id == "bmb831.m05":
            updated.append(
                replace(
                    audit,
                    state="consistent",
                    finding=(
                        "Existing figure contracts, MA and volcano plots, heatmaps, accessibility, "
                        "and reproducible export are consistent. The focused review identified one "
                        "missing distinction between observed spread, standard error, confidence "
                        "intervals, and prediction uncertainty."
                    ),
                    implemented_change=(
                        "Added a trilingual uncertainty-target explanation, a deterministic "
                        "mean/SD/SE/CI example, an error-bar interpretation exercise, and a stable "
                        "objective assessment item."
                    ),
                )
            )
        else:
            updated.append(audit)
    return tuple(updated)


def _extend_multivariate_rank(
    module: LocalizedLearningModule,
) -> LocalizedLearningModule:
    return replace(
        module,
        objectives=module.objectives
        + (
            objective(
                "m04.bg.o1",
                (
                    "Reconocer el límite de rango impuesto por el número de muestras y evaluar estabilidad de subespacios cuando las componentes son cercanas.",
                    "Recognize the rank limit imposed by sample count and assess subspace stability when components are close.",
                    "Genkende ranggrænsen bestemt af antallet af prøver og vurdere underrumsstabilitet, når komponenter ligger tæt.",
                ),
            ),
        ),
        concepts=module.concepts
        + (
            concept(
                "finite-sample-rank-and-subspace-stability",
                (
                    "Rango finito y estabilidad del subespacio",
                    "Finite-sample rank and subspace stability",
                    "Endelig rang og underrumsstabilitet",
                ),
                (
                    "En matriz centrada con n muestras y p características tiene rango máximo min(p, n - 1). Por tanto, medir miles de genes o proteínas no crea miles de direcciones independientes si sólo existen pocas muestras: como máximo n - 1 componentes pueden contener variación muestral no nula. Este límite no impide usar PCA, pero restringe la complejidad identificable y exige separar cantidad de características de información independiente. Además, cuando dos valores propios son iguales o muy próximos, pequeñas perturbaciones pueden rotar sus ejes y cambiar loadings individuales aunque el subespacio conjunto sea prácticamente el mismo. En ese caso deben compararse varianza capturada, proyecciones o ángulos del subespacio, estabilidad bajo remuestreo y coherencia biológica, no una lista rígida de loadings de una sola ejecución.",
                    "A centered matrix with n samples and p features has maximum rank min(p, n - 1). Therefore, measuring thousands of genes or proteins does not create thousands of independent directions when only a few samples exist: at most n - 1 components can contain non-zero sample variation. This limit does not prevent PCA, but it constrains identifiable complexity and requires separating feature count from independent information. In addition, when two eigenvalues are equal or very close, small perturbations may rotate their axes and change individual loadings even though the joint subspace is nearly unchanged. In that setting, compare captured variance, projections or subspace angles, resampling stability, and biological coherence rather than a rigid loading list from one run.",
                    "En centreret matrix med n prøver og p features har maksimal rang min(p, n - 1). Måling af tusindvis af gener eller proteiner skaber derfor ikke tusindvis af uafhængige retninger, når der kun findes få prøver: højst n - 1 komponenter kan indeholde ikke-nul prøvevariation. Grænsen forhindrer ikke PCA, men begrænser den identificerbare kompleksitet og kræver, at featureantal adskilles fra uafhængig information. Når to egenværdier er ens eller meget tætte, kan små perturbationer desuden rotere akserne og ændre individuelle loadings, selv om det fælles underrum næsten er uændret. I denne situation bør man sammenligne forklaret variation, projektioner eller underrumsvinkler, stabilitet under resampling og biologisk sammenhæng frem for en rigid loadingliste fra én kørsel.",
                ),
                (
                    (
                        "Tras centrar, el número de componentes no nulas no supera min(p, n - 1).",
                        "After centering, the number of non-zero components cannot exceed min(p, n - 1).",
                        "Efter centrering kan antallet af ikke-nul komponenter ikke overstige min(p, n - 1).",
                    ),
                    (
                        "Más características no equivalen a más muestras independientes.",
                        "More features do not equal more independent samples.",
                        "Flere features er ikke det samme som flere uafhængige prøver.",
                    ),
                    (
                        "Componentes casi degeneradas pueden rotar sin que cambie el subespacio relevante.",
                        "Nearly degenerate components may rotate without changing the relevant subspace.",
                        "Næsten degenererede komponenter kan rotere uden at ændre det relevante underrum.",
                    ),
                    (
                        "La estabilidad debe evaluarse sobre la estructura conjunta y bajo perturbaciones plausibles.",
                        "Stability should be assessed on the joint structure under plausible perturbations.",
                        "Stabilitet bør vurderes på den fælles struktur under plausible perturbationer.",
                    ),
                ),
            ),
        ),
        worked_examples=module.worked_examples
        + (
            example(
                "m04.bg.e01",
                (
                    "Verificar el techo de rango de una matriz p mayor que n",
                    "Verify the rank ceiling of a p-greater-than-n matrix",
                    "Kontrollér rangloftet for en matrix med p større end n",
                ),
                (
                    "Centra una matriz con cuatro muestras y seis características y comprueba cuántas componentes pueden contener variación no nula.",
                    "Center a matrix with four samples and six features and verify how many components can contain non-zero variation.",
                    "Centrér en matrix med fire prøver og seks features og kontrollér, hvor mange komponenter der kan indeholde ikke-nul variation.",
                ),
                (
                    (
                        "Las muestras son filas y las características columnas.",
                        "Samples are rows and features are columns.",
                        "Prøver er rækker og features er kolonner.",
                    ),
                    (
                        "El centrado elimina una dimensión asociada con la media.",
                        "Centering removes one dimension associated with the mean.",
                        "Centrering fjerner én dimension forbundet med middelværdien.",
                    ),
                    (
                        "El umbral numérico se expresa en relación con la mayor desviación estándar.",
                        "The numerical threshold is expressed relative to the largest standard deviation.",
                        "Den numeriske tærskel udtrykkes relativt til den største standardafvigelse.",
                    ),
                ),
                """x <- matrix(
  c(1, 2, 3, 4, 5, 6,
    2, 1, 4, 3, 6, 5,
    3, 5, 1, 6, 2, 4,
    5, 3, 6, 1, 4, 2),
  nrow = 4,
  byrow = TRUE
)
centered <- scale(x, center = TRUE, scale = FALSE)
rank_ceiling <- min(nrow(x) - 1, ncol(x))
observed_rank <- qr(centered)$rank
fit <- prcomp(x, center = TRUE, scale. = FALSE)
threshold <- sqrt(.Machine$double.eps) * max(fit$sdev)
nonzero_pcs <- sum(fit$sdev > threshold)
cat("samples=", nrow(x), "\n", sep = "")
cat("features=", ncol(x), "\n", sep = "")
cat("rank_ceiling=", rank_ceiling, "\n", sep = "")
cat("observed_rank=", observed_rank, "\n", sep = "")
cat("nonzero_pcs=", nonzero_pcs, sep = "")
""",
                """samples=4
features=6
rank_ceiling=3
observed_rank=3
nonzero_pcs=3""",
                (
                    "Aunque hay seis características, cuatro muestras centradas sólo permiten tres direcciones no nulas. El resultado limita la dimensionalidad identificable; no demuestra que tres componentes sean biológicamente suficientes.",
                    "Although there are six features, four centered samples allow only three non-zero directions. The result limits identifiable dimensionality; it does not prove that three components are biologically sufficient.",
                    "Selv om der er seks features, tillader fire centrerede prøver kun tre ikke-nul retninger. Resultatet begrænser den identificerbare dimensionalitet; det beviser ikke, at tre komponenter er biologisk tilstrækkelige.",
                ),
            ),
        ),
        practice_exercises=module.practice_exercises
        + (
            practice(
                "m04.bg.p01",
                ActivityType.DATA_INTERPRETATION,
                (
                    "Un estudio tiene 12 muestras y 20 000 genes. Explica el límite de dimensionalidad identificable y diseña una comprobación de estabilidad para los dos primeros componentes.",
                    "A study has 12 samples and 20,000 genes. Explain the identifiable dimensionality limit and design a stability check for the first two components.",
                    "Et studie har 12 prøver og 20.000 gener. Forklar grænsen for identificerbar dimensionalitet og design en stabilitetskontrol for de to første komponenter.",
                ),
                (
                    (
                        "Separa número de genes de rango muestral.",
                        "Separate gene count from sample rank.",
                        "Adskil genantal fra prøverang.",
                    ),
                    (
                        "Considera remuestreo, perturbación de features y comparación del subespacio.",
                        "Consider resampling, feature perturbation, and subspace comparison.",
                        "Overvej resampling, featureperturbation og sammenligning af underrummet.",
                    ),
                ),
                (
                    "Tras centrar, como máximo 11 componentes pueden tener variación no nula, aunque existan 20 000 genes. Repetiría PCA bajo bootstrap o eliminación razonable de muestras y subconjuntos de genes, manteniendo el preprocesamiento definido, y compararía el subespacio PC1-PC2 mediante proyecciones, correlaciones absolutas o ángulos, además de revisar varianza explicada y metadata. Si los ejes rotan pero el plano se conserva, reportaría estabilidad del subespacio y no de loadings individuales.",
                    "After centering, at most 11 components can have non-zero variation despite 20,000 genes. Repeat PCA under bootstrap or reasonable sample removal and feature subsets while preserving the defined preprocessing, and compare the PC1-PC2 subspace through projections, absolute correlations or angles, together with explained variance and metadata. If axes rotate but the plane is preserved, report subspace stability rather than individual-loading stability.",
                    "Efter centrering kan højst 11 komponenter have ikke-nul variation trods 20.000 gener. Gentag PCA under bootstrap eller rimelig fjernelse af prøver og featuresubsets med det definerede præprocesseringstrin bevaret, og sammenlign PC1-PC2-underrummet via projektioner, absolutte korrelationer eller vinkler samt forklaret varians og metadata. Hvis akserne roterer, men planet bevares, rapporteres underrumsstabilitet frem for stabilitet af individuelle loadings.",
                ),
                (
                    "Una respuesta completa declara el techo n - 1, no trata genes como réplicas y evalúa estructura conjunta bajo perturbación.",
                    "A complete answer states the n - 1 ceiling, does not treat genes as replicates, and evaluates joint structure under perturbation.",
                    "Et fuldstændigt svar angiver n - 1-loftet, behandler ikke gener som replikater og vurderer fælles struktur under perturbation.",
                ),
                "",
            ),
        ),
        assessment_items=module.assessment_items
        + (
            objective_mcq(
                "bmb831.m04.book.001",
                (
                    "Después de centrar una matriz con n muestras y p características, ¿cuál es el máximo número de componentes principales con variación no nula?",
                    "After centering a matrix with n samples and p features, what is the maximum number of principal components with non-zero variation?",
                    "Efter centrering af en matrix med n prøver og p features, hvad er det maksimale antal hovedkomponenter med ikke-nul variation?",
                ),
                (
                    (
                        "rank_ceiling",
                        (
                            "min(p, n - 1)",
                            "min(p, n - 1)",
                            "min(p, n - 1)",
                        ),
                    ),
                    (
                        "feature_count",
                        (
                            "Siempre p",
                            "Always p",
                            "Altid p",
                        ),
                    ),
                    (
                        "sample_count",
                        (
                            "Siempre n",
                            "Always n",
                            "Altid n",
                        ),
                    ),
                ),
                "rank_ceiling",
                (
                    "El centrado introduce una dependencia lineal entre las filas, por lo que el rango no puede superar n - 1 ni p.",
                    "Centering introduces a linear dependence among rows, so rank cannot exceed either n - 1 or p.",
                    "Centrering indfører en lineær afhængighed mellem rækkerne, så rangen kan hverken overstige n - 1 eller p.",
                ),
            ),
        ),
    )


def _extend_visual_uncertainty(
    module: LocalizedLearningModule,
) -> LocalizedLearningModule:
    return replace(
        module,
        objectives=module.objectives
        + (
            objective(
                "m05.bg.o1",
                (
                    "Distinguir dispersión de observaciones, error estándar, intervalo de confianza e incertidumbre predictiva antes de elegir barras de error.",
                    "Distinguish observation spread, standard error, confidence interval, and predictive uncertainty before choosing error bars.",
                    "Skelne mellem observationsspredning, standardfejl, konfidensinterval og prædiktiv usikkerhed før valg af fejlbjælker.",
                ),
            ),
        ),
        concepts=module.concepts
        + (
            concept(
                "spread-versus-estimator-uncertainty",
                (
                    "Dispersión frente a incertidumbre del estimador",
                    "Spread versus estimator uncertainty",
                    "Spredning versus estimatorusikkerhed",
                ),
                (
                    "Las barras de error no tienen un significado universal. La desviación estándar describe dispersión entre observaciones bajo una escala definida; el error estándar cuantifica variabilidad estimada del promedio; un intervalo de confianza expresa incertidumbre del parámetro bajo un procedimiento y sus supuestos; y un intervalo predictivo busca cubrir una observación futura e incorpora variabilidad residual. Ninguno significa automáticamente que un porcentaje fijo de datos esté dentro de la barra. Dos grupos pueden tener la misma media y dispersión muy distinta, y una figura que muestra sólo medias puede ocultarlo. La leyenda debe nombrar exactamente el estimando, el tipo y nivel del intervalo, n, la unidad analítica y el método. Con muestras pequeñas suelen ser necesarios puntos individuales o distribuciones junto con el resumen para evitar precisión visual ficticia.",
                    "Error bars do not have a universal meaning. Standard deviation describes spread among observations on a defined scale; standard error quantifies estimated variability of the mean; a confidence interval expresses parameter uncertainty under a procedure and its assumptions; and a prediction interval aims to cover a future observation and includes residual variability. None automatically means that a fixed percentage of data lies inside the bar. Two groups may have the same mean and very different spread, and a mean-only figure can hide that difference. The caption should name the estimand, interval type and level, n, analytical unit, and method. With small samples, individual points or distributions are often needed alongside the summary to avoid false visual precision.",
                    "Fejlbjælker har ikke én universel betydning. Standardafvigelsen beskriver spredning mellem observationer på en defineret skala; standardfejlen kvantificerer den estimerede variation af middelværdien; et konfidensinterval udtrykker parameterusikkerhed under en procedure og dens antagelser; og et prædiktionsinterval søger at dække en fremtidig observation og inkluderer residual variation. Ingen af dem betyder automatisk, at en fast andel af data ligger inden for bjælken. To grupper kan have samme middelværdi og meget forskellig spredning, og en figur med kun middelværdier kan skjule forskellen. Figurteksten bør navngive estimand, intervaltype og niveau, n, analytisk enhed og metode. Ved små stikprøver er individuelle punkter eller fordelinger ofte nødvendige sammen med resumeet for at undgå falsk visuel præcision.",
                ),
                (
                    (
                        "SD describe observaciones; SE e intervalos describen objetivos inferenciales distintos.",
                        "SD describes observations; SE and intervals describe different inferential targets.",
                        "SD beskriver observationer; SE og intervaller beskriver forskellige inferentielle mål.",
                    ),
                    (
                        "El tipo de barra, nivel, n y método deben declararse.",
                        "Bar type, level, n, and method must be declared.",
                        "Bjælketype, niveau, n og metode skal deklareres.",
                    ),
                    (
                        "Una media aislada puede ocultar asimetría, outliers y heterogeneidad.",
                        "A mean alone can hide skew, outliers, and heterogeneity.",
                        "En middelværdi alene kan skjule skævhed, outliers og heterogenitet.",
                    ),
                    (
                        "La visualización debe corresponder al estimando y a la unidad analítica.",
                        "The visualization must match the estimand and analytical unit.",
                        "Visualiseringen skal svare til estimand og analytisk enhed.",
                    ),
                ),
            ),
        ),
        worked_examples=module.worked_examples
        + (
            example(
                "m05.bg.e01",
                (
                    "Comparar SD, SE e intervalo de confianza con la misma media",
                    "Compare SD, SE, and confidence interval with the same mean",
                    "Sammenlign SD, SE og konfidensinterval ved samme middelværdi",
                ),
                (
                    "Resume dos grupos con igual media y distinta dispersión para mostrar que las barras deben nombrar el objetivo de incertidumbre.",
                    "Summarize two groups with the same mean and different spread to show that error bars must name their uncertainty target.",
                    "Opsummér to grupper med samme middelværdi og forskellig spredning for at vise, at fejlbjælker skal navngive deres usikkerhedsmål.",
                ),
                (
                    (
                        "Cada grupo contiene cuatro observaciones independientes en este ejemplo didáctico.",
                        "Each group contains four independent observations in this didactic example.",
                        "Hver gruppe indeholder fire uafhængige observationer i dette didaktiske eksempel.",
                    ),
                    (
                        "El intervalo usa la distribución t con tres grados de libertad.",
                        "The interval uses the t distribution with three degrees of freedom.",
                        "Intervallet bruger t-fordelingen med tre frihedsgrader.",
                    ),
                    (
                        "El ejemplo no sustituye un modelo para datos pareados, longitudinales o jerárquicos.",
                        "The example does not replace a model for paired, longitudinal, or hierarchical data.",
                        "Eksemplet erstatter ikke en model for parrede, longitudinelle eller hierarkiske data.",
                    ),
                ),
                """values <- list(
  A = c(8, 10, 10, 12),
  B = c(4, 10, 10, 16)
)
summarise_group <- function(x) {
  standard_error <- sd(x) / sqrt(length(x))
  c(
    mean = mean(x),
    sd = sd(x),
    se = standard_error,
    ci_half = qt(0.975, df = length(x) - 1) * standard_error
  )
}
summaries <- lapply(values, summarise_group)
for (index in seq_along(summaries)) {
  group <- names(summaries)[index]
  values_text <- paste(
    names(summaries[[group]]),
    sprintf("%.3f", summaries[[group]]),
    sep = ":",
    collapse = ","
  )
  ending <- if (index < length(summaries)) "\n" else ""
  cat("group_", group, "=", values_text, ending, sep = "")
}
""",
                """group_A=mean:10.000,sd:1.633,se:0.816,ci_half:2.598
group_B=mean:10.000,sd:4.899,se:2.449,ci_half:7.795""",
                (
                    "Ambos grupos tienen media diez, pero B presenta tres veces la desviación estándar y un intervalo mucho más amplio. Una figura de medias sin puntos ni definición de barras ocultaría esa diferencia. El intervalo describe incertidumbre de la media bajo los supuestos del ejemplo, no el rango esperado de observaciones.",
                    "Both groups have mean ten, but B has three times the standard deviation and a much wider interval. A mean-only figure without points or an error-bar definition would hide that difference. The interval describes uncertainty of the mean under the example assumptions, not the expected range of observations.",
                    "Begge grupper har middelværdi ti, men B har tre gange så stor standardafvigelse og et langt bredere interval. En figur med kun middelværdier uden punkter eller definition af fejlbjælker ville skjule forskellen. Intervallet beskriver usikkerhed om middelværdien under eksemplets antagelser, ikke det forventede observationsinterval.",
                ),
            ),
        ),
        practice_exercises=module.practice_exercises
        + (
            practice(
                "m05.bg.p01",
                ActivityType.DATA_INTERPRETATION,
                (
                    "Una figura muestra media ± SEM para cuatro réplicas y la leyenda dice 'variabilidad biológica'. Corrige la figura y la leyenda según la pregunta científica.",
                    "A figure shows mean ± SEM for four replicates and the caption says 'biological variability'. Correct the figure and caption according to the scientific question.",
                    "En figur viser middelværdi ± SEM for fire replikater, og figurteksten siger 'biologisk variation'. Korrigér figur og tekst efter det videnskabelige spørgsmål.",
                ),
                (
                    (
                        "Decide si el objetivo es describir observaciones o estimar una media.",
                        "Decide whether the target is describing observations or estimating a mean.",
                        "Afgør om målet er at beskrive observationer eller estimere en middelværdi.",
                    ),
                    (
                        "Declara tipo de intervalo, nivel, n y unidad experimental.",
                        "State interval type, level, n, and experimental unit.",
                        "Angiv intervaltype, niveau, n og eksperimentel enhed.",
                    ),
                ),
                (
                    "Si el objetivo es mostrar variabilidad biológica, presentaría puntos individuales y una medida de dispersión apropiada, como SD o un resumen robusto, preservando la unidad experimental. Si el objetivo es estimar la media, mostraría un intervalo de confianza con nivel y método explícitos, idealmente junto con los puntos. La leyenda no llamaría variabilidad al SEM; indicaría n = 4, qué constituye una réplica independiente y si existe pareamiento o jerarquía que requiera otro modelo.",
                    "If the goal is biological variability, show individual points and an appropriate spread measure such as SD or a robust summary while preserving the experimental unit. If the goal is mean estimation, show a confidence interval with explicit level and method, preferably alongside the points. The caption should not call SEM variability; it should state n = 4, what constitutes an independent replicate, and whether pairing or hierarchy requires another model.",
                    "Hvis målet er biologisk variation, vises individuelle punkter og et passende spredningsmål som SD eller et robust resume med den eksperimentelle enhed bevaret. Hvis målet er estimering af middelværdien, vises et konfidensinterval med eksplicit niveau og metode, helst sammen med punkterne. Figurteksten bør ikke kalde SEM for variation; den skal angive n = 4, hvad der udgør en uafhængig replikat, og om parring eller hierarki kræver en anden model.",
                ),
                (
                    "Una respuesta completa alinea el gráfico con el estimando, corrige la semántica del SEM y declara independencia y método.",
                    "A complete answer aligns the plot with the estimand, corrects SEM semantics, and states independence and method.",
                    "Et fuldstændigt svar tilpasser figuren til estimand, korrigerer SEM-semantikken og angiver uafhængighed og metode.",
                ),
                "",
            ),
        ),
        assessment_items=module.assessment_items
        + (
            objective_mcq(
                "bmb831.m05.book.001",
                (
                    "¿Qué representa un intervalo de confianza del 95% para una media?",
                    "What does a 95% confidence interval for a mean represent?",
                    "Hvad repræsenterer et 95 % konfidensinterval for en middelværdi?",
                ),
                (
                    (
                        "procedure",
                        (
                            "La incertidumbre del estimador bajo un procedimiento que cubriría el parámetro en el 95% de repeticiones compatibles con sus supuestos.",
                            "Estimator uncertainty under a procedure that would cover the parameter in 95% of compatible repetitions under its assumptions.",
                            "Estimatorusikkerhed under en procedure, der ville dække parameteren i 95 % af kompatible gentagelser under dens antagelser.",
                        ),
                    ),
                    (
                        "observations",
                        (
                            "El rango que contiene necesariamente al 95% de las observaciones.",
                            "The range that necessarily contains 95% of observations.",
                            "Det interval, der nødvendigvis indeholder 95 % af observationerne.",
                        ),
                    ),
                    (
                        "posterior",
                        (
                            "Una probabilidad posterior automática de 0,95 para cada valor dentro del intervalo.",
                            "An automatic posterior probability of 0.95 for every value inside the interval.",
                            "En automatisk posterior sandsynlighed på 0,95 for hver værdi i intervallet.",
                        ),
                    ),
                ),
                "procedure",
                (
                    "El intervalo se refiere al comportamiento del procedimiento de estimación bajo sus supuestos; no es un intervalo de observaciones ni una probabilidad posterior automática.",
                    "The interval concerns the behavior of the estimation procedure under its assumptions; it is neither an observation interval nor an automatic posterior probability.",
                    "Intervallet vedrører estimationsprocedurens adfærd under dens antagelser; det er hverken et observationsinterval eller en automatisk posterior sandsynlighed.",
                ),
            ),
        ),
    )


def apply_multivariate_visualization_extensions(
    modules: tuple[LocalizedLearningModule, ...],
) -> tuple[LocalizedLearningModule, ...]:
    """Apply the completed M04 and M05 focused-review extensions."""

    updated: list[LocalizedLearningModule] = []
    for module in modules:
        if module.module_id == "bmb831.m04":
            updated.append(_extend_multivariate_rank(module))
        elif module.module_id == "bmb831.m05":
            updated.append(_extend_visual_uncertainty(module))
        else:
            updated.append(module)
    return tuple(updated)


__all__ = [
    "apply_multivariate_visualization_extensions",
    "review_module_source_audit",
]
