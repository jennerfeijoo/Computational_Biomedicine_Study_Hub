"""Source-grounded BMB830 audit and focused foundational extensions.

The active public SDU course description defines the curricular boundary. The
statistical references are used to verify depth and terminology, not to invent
institutional assessment mechanics. Visible teaching material is original
trilingual paraphrase and adaptation.
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
    """One stable source used by the BMB830 audit."""

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


BMB830_BOOK_SOURCES: tuple[AcademicReference, ...] = (
    AcademicReference(
        "sdu-bmb830-active-2025",
        "SDU, BMB830: Biostatistics in R I, approved active course description (2025).",
        (
            "R scripting, probability, statistical modelling, visualisation, interpretation, "
            "multivariate analysis, biological data analysis, and individual oral reasoning"
        ),
    ),
    AcademicReference(
        "ims-2024-data-eda",
        (
            "Mine Çetinkaya-Rundel and Johanna Hardin, Introduction to Modern Statistics, "
            "2nd ed. (2024), parts 1 and 2."
        ),
        (
            "data structure, study design, descriptive statistics, robust summaries, "
            "visualisation, and multivariable exploratory analysis"
        ),
    ),
    AcademicReference(
        "ims-2024-probability-inference",
        (
            "Mine Çetinkaya-Rundel and Johanna Hardin, Introduction to Modern Statistics, "
            "2nd ed. (2024), parts 4 and 5."
        ),
        (
            "conditional probability, simulation, sampling distributions, bootstrap intervals, "
            "confidence intervals, hypothesis testing, and repeated-sampling interpretation"
        ),
    ),
    AcademicReference(
        "ims-2024-regression-models",
        (
            "Mine Çetinkaya-Rundel and Johanna Hardin, Introduction to Modern Statistics, "
            "2nd ed. (2024), parts 3 and 6."
        ),
        (
            "linear and logistic regression, multiple predictors, model interpretation, "
            "inference, diagnostics, and prediction"
        ),
    ),
    AcademicReference(
        "islr-2021-ch02-05",
        (
            "Gareth James, Daniela Witten, Trevor Hastie, and Robert Tibshirani, "
            "An Introduction to Statistical Learning with Applications in R, 2nd ed. "
            "(2021), chapters 2 through 5."
        ),
        (
            "statistical learning, regression, classification, resampling, model assessment, "
            "test error, and bootstrap reasoning"
        ),
    ),
    AcademicReference(
        "yachay-probability-statistics",
        "Yachay Tech, Clases probabilidad y estadística, course notes.",
        (
            "descriptive statistics, events, conditional probability, Bayes theorem, random "
            "variables, sampling distributions, estimation, and hypothesis testing"
        ),
    ),
    AcademicReference(
        "yachay-biostatistics-linear-models",
        "Yachay Tech, Completo bioestadística, biostatistics and linear-model course notes.",
        (
            "confidence intervals, one-sample tests, ANOVA, simple and multiple regression, "
            "assumptions, leverage, influence, and model diagnostics"
        ),
    ),
)


BMB830_MODULE_SOURCE_AUDIT: tuple[ModuleSourceAudit, ...] = (
    ModuleSourceAudit(
        "bmb830.m01",
        ("sdu-bmb830-active-2025", "ims-2024-data-eda"),
        (
            "R data structures and analytical roles",
            "keys, missingness, validation, and reproducible scripts",
            "clean-session execution and traceable output",
        ),
        "consistent",
        (
            "Existing coverage of R objects, factors, indexing, keys, missingness, assertions, "
            "and clean-session reproducibility is consistent with the mapped scope."
        ),
        "Added explicit source-basis traceability without expanding the already adequate module.",
    ),
    ModuleSourceAudit(
        "bmb830.m02",
        ("sdu-bmb830-active-2025", "ims-2024-data-eda", "yachay-probability-statistics"),
        (
            "centre, dispersion, shape, and robust summaries",
            "quality auditing and provenance-preserving exclusions",
            "statistical graphics and descriptive interpretation boundaries",
        ),
        "consistent",
        (
            "Existing coverage of robust summaries, outlier investigation, quality rules, "
            "visual encodings, denominators, uncertainty, and causal boundaries is consistent."
        ),
        "Added explicit source-basis traceability without duplicating current content.",
    ),
    ModuleSourceAudit(
        "bmb830.m03",
        (
            "sdu-bmb830-active-2025",
            "ims-2024-probability-inference",
            "yachay-probability-statistics",
        ),
        (
            "events, conditional probability, and independence",
            "Bernoulli, binomial, normal, and sampling distributions",
            "Bayes updating for diagnostic interpretation",
        ),
        "consistent",
        (
            "Existing probability and sampling-distribution coverage is consistent. The module "
            "distinguished reversed conditional probabilities but needed an explicit numerical "
            "Bayes update showing the effect of prevalence on a positive result."
        ),
        (
            "Added an original trilingual Bayes explanation, deterministic diagnostic example, "
            "interpretation exercise, and stable objective item."
        ),
    ),
    ModuleSourceAudit(
        "bmb830.m04",
        (
            "sdu-bmb830-active-2025",
            "ims-2024-probability-inference",
            "islr-2021-ch02-05",
            "yachay-biostatistics-linear-models",
        ),
        (
            "estimands, estimators, uncertainty, and repeated-sampling coverage",
            "model-based confidence intervals for means and proportions",
            "bootstrap resampling and design-preserving uncertainty",
        ),
        "consistent",
        (
            "Existing treatment of estimands, standard errors, t intervals, Wilson intervals, "
            "coverage, effective sample size, and precision is consistent. Bootstrap intervals "
            "and the requirement to resample independent units needed one explicit treatment."
        ),
        (
            "Added an original bootstrap explanation, exhaustive deterministic example, design "
            "exercise, and stable objective item."
        ),
    ),
    ModuleSourceAudit(
        "bmb830.m05",
        (
            "sdu-bmb830-active-2025",
            "ims-2024-probability-inference",
            "yachay-biostatistics-linear-models",
        ),
        ("null and alternative hypotheses", "errors and power", "p-values and multiplicity"),
        "pending",
        "Source scope is mapped; focused comparison remains pending.",
    ),
    ModuleSourceAudit(
        "bmb830.m06",
        ("sdu-bmb830-active-2025", "ims-2024-probability-inference"),
        ("paired and independent comparisons", "Welch procedures", "ANOVA and contrasts"),
        "pending",
        "Source scope is mapped; focused comparison remains pending.",
    ),
    ModuleSourceAudit(
        "bmb830.m07",
        (
            "sdu-bmb830-active-2025",
            "ims-2024-regression-models",
            "yachay-biostatistics-linear-models",
        ),
        ("correlation", "simple linear regression", "prediction and causal boundaries"),
        "pending",
        "Source scope is mapped; focused comparison remains pending.",
    ),
    ModuleSourceAudit(
        "bmb830.m08",
        (
            "sdu-bmb830-active-2025",
            "ims-2024-regression-models",
            "islr-2021-ch02-05",
            "yachay-biostatistics-linear-models",
        ),
        ("multiple regression", "design matrices and contrasts", "confounding and collinearity"),
        "pending",
        "Source scope is mapped; focused comparison remains pending.",
    ),
    ModuleSourceAudit(
        "bmb830.m09",
        ("sdu-bmb830-active-2025", "ims-2024-regression-models", "islr-2021-ch02-05"),
        ("interactions", "effect modification", "nonlinearity and extrapolation"),
        "pending",
        "Source scope is mapped; focused comparison remains pending.",
    ),
    ModuleSourceAudit(
        "bmb830.m10",
        (
            "sdu-bmb830-active-2025",
            "ims-2024-regression-models",
            "islr-2021-ch02-05",
            "yachay-biostatistics-linear-models",
        ),
        ("residual diagnostics", "leverage and influence", "validation and leakage"),
        "pending",
        "Source scope is mapped; focused comparison remains pending.",
    ),
    ModuleSourceAudit(
        "bmb830.m11",
        ("sdu-bmb830-active-2025", "islr-2021-ch02-05"),
        ("matrix preprocessing", "PCA", "hierarchical clustering and stability"),
        "pending",
        "Source scope is mapped; focused comparison remains pending.",
    ),
    ModuleSourceAudit(
        "bmb830.m12",
        ("sdu-bmb830-active-2025", "islr-2021-ch02-05"),
        (
            "high-dimensional biological matrices",
            "training-only feature selection",
            "batch effects, leakage, and external validation",
        ),
        "pending",
        "Source scope is mapped; focused comparison remains pending.",
    ),
)


def _source_ids(module_id: str) -> tuple[str, ...]:
    return next(item.source_ids for item in BMB830_MODULE_SOURCE_AUDIT if item.module_id == module_id)


def _with_source_basis(module: LocalizedLearningModule) -> LocalizedLearningModule:
    tutor = module.tutor_support
    merged = tuple(dict.fromkeys((*tutor.source_basis, *_source_ids(module.module_id))))
    updated_tutor: LocalizedTutorSupportPacket = replace(tutor, source_basis=merged)
    return replace(module, tutor_support=updated_tutor)


def _extend_probability(module: LocalizedLearningModule) -> LocalizedLearningModule:
    extended = replace(
        module,
        objectives=module.objectives
        + (
            objective(
                "m03.bg.o1",
                (
                    "Actualizar una probabilidad diagnóstica con el teorema de Bayes y una prevalencia explícita.",
                    "Update a diagnostic probability with Bayes' theorem and explicit prevalence.",
                    "Opdatere en diagnostisk sandsynlighed med Bayes' sætning og eksplicit prævalens.",
                ),
            ),
        ),
        concepts=module.concepts
        + (
            concept(
                "bayes-updating-and-base-rates",
                (
                    "Actualización bayesiana y tasas basales",
                    "Bayesian updating and base rates",
                    "Bayesiansk opdatering og basisrater",
                ),
                (
                    "La sensibilidad es P(+|D) y la especificidad es P(-|no D); ninguna de las dos es P(D|+). Para interpretar un resultado positivo se combina la sensibilidad con la prevalencia P(D) y la tasa de falsos positivos 1-especificidad. El denominador suma todas las rutas que producen un positivo. Por ello, la misma prueba puede tener valores predictivos positivos distintos en poblaciones con prevalencias diferentes. La actualización sólo es válida para la población, definición de enfermedad y condiciones operativas que justifican esos parámetros.",
                    "Sensitivity is P(+|D) and specificity is P(-|not D); neither equals P(D|+). Interpreting a positive result combines sensitivity with prevalence P(D) and the false-positive rate 1-specificity. The denominator sums every route that produces a positive result. The same test can therefore have different positive predictive values in populations with different prevalence. The update is valid only for the population, disease definition, and operating conditions that justify those parameters.",
                    "Sensitivitet er P(+|D), og specificitet er P(-|ikke D); ingen af dem er P(D|+). Fortolkning af et positivt resultat kombinerer sensitivitet med prævalens P(D) og falsk-positiv-raten 1-specificitet. Nævneren summerer alle veje til et positivt resultat. Den samme test kan derfor have forskellige positive prædiktive værdier i populationer med forskellig prævalens. Opdateringen gælder kun for den population, sygdomsdefinition og driftsbetingelser, der begrunder parametrene.",
                ),
                (
                    (
                        "Sensibilidad y valor predictivo positivo condicionan en direcciones distintas.",
                        "Sensitivity and positive predictive value condition in different directions.",
                        "Sensitivitet og positiv prædiktiv værdi betinger i forskellige retninger.",
                    ),
                    (
                        "La prevalencia es parte del cálculo posterior, no un detalle opcional.",
                        "Prevalence is part of the posterior calculation, not an optional detail.",
                        "Prævalens er en del af posteriorberegningen, ikke en valgfri detalje.",
                    ),
                    (
                        "El denominador incluye verdaderos y falsos positivos.",
                        "The denominator includes true and false positives.",
                        "Nævneren omfatter sande og falske positive.",
                    ),
                    (
                        "Transportar sensibilidad, especificidad o prevalencia exige justificación.",
                        "Transporting sensitivity, specificity, or prevalence requires justification.",
                        "Overførsel af sensitivitet, specificitet eller prævalens kræver begrundelse.",
                    ),
                ),
            ),
        ),
        worked_examples=module.worked_examples
        + (
            example(
                "m03.bg.e01",
                (
                    "Probabilidad de enfermedad tras un positivo",
                    "Disease probability after a positive result",
                    "Sygdomssandsynlighed efter et positivt resultat",
                ),
                (
                    "Combina prevalencia 0,02, sensibilidad 0,90 y especificidad 0,95.",
                    "Combine prevalence 0.02, sensitivity 0.90, and specificity 0.95.",
                    "Kombinér prævalens 0,02, sensitivitet 0,90 og specificitet 0,95.",
                ),
                (
                    (
                        "Calcula primero la probabilidad total de un positivo.",
                        "First calculate the total probability of a positive result.",
                        "Beregn først den samlede sandsynlighed for et positivt resultat.",
                    ),
                    (
                        "Divide la ruta verdadero-positivo entre todas las rutas positivas.",
                        "Divide the true-positive route by all positive routes.",
                        "Divider den sandt-positive vej med alle positive veje.",
                    ),
                ),
                """prevalence <- 0.02
sensitivity <- 0.90
specificity <- 0.95
positive_probability <- sensitivity * prevalence +
  (1 - specificity) * (1 - prevalence)
posterior <- sensitivity * prevalence / positive_probability
cat(sprintf("P(D|+)=%.3f\n", posterior))
""",
                "P(D|+)=0.269",
                (
                    "Aunque la sensibilidad es 0,90, la baja prevalencia hace que los falsos positivos contribuyan de forma importante al conjunto de resultados positivos.",
                    "Although sensitivity is 0.90, low prevalence makes false positives contribute substantially to the set of positive results.",
                    "Selv om sensitiviteten er 0,90, betyder den lave prævalens, at falske positive bidrager væsentligt til de positive resultater.",
                ),
            ),
        ),
        practice_exercises=module.practice_exercises
        + (
            practice(
                "m03.bg.p01",
                ActivityType.DATA_INTERPRETATION,
                (
                    "La misma prueba tiene sensibilidad 0,90 y especificidad 0,95. Compara P(D|+) cuando la prevalencia es 0,02 y cuando es 0,20, y explica la diferencia.",
                    "The same test has sensitivity 0.90 and specificity 0.95. Compare P(D|+) when prevalence is 0.02 and when it is 0.20, and explain the difference.",
                    "Den samme test har sensitivitet 0,90 og specificitet 0,95. Sammenlign P(D|+) ved prævalens 0,02 og 0,20, og forklar forskellen.",
                ),
                (
                    (
                        "Usa sensibilidad × prevalencia en el numerador.",
                        "Use sensitivity × prevalence in the numerator.",
                        "Brug sensitivitet × prævalens i tælleren.",
                    ),
                    (
                        "Incluye la ruta de falsos positivos en el denominador.",
                        "Include the false-positive route in the denominator.",
                        "Medtag den falsk-positive vej i nævneren.",
                    ),
                ),
                (
                    "Los valores son aproximadamente 0,269 y 0,818. La prueba no cambió; cambió la proporción previa de personas enfermas entre quienes pueden producir un resultado positivo.",
                    "The values are approximately 0.269 and 0.818. The test did not change; the prior proportion with disease among those who can produce a positive result changed.",
                    "Værdierne er omtrent 0,269 og 0,818. Testen ændrede sig ikke; den forudgående andel med sygdom blandt dem, der kan give et positivt resultat, ændrede sig.",
                ),
                (
                    "Una respuesta completa calcula ambas probabilidades y distingue sensibilidad de valor predictivo positivo.",
                    "A complete answer calculates both probabilities and distinguishes sensitivity from positive predictive value.",
                    "Et fuldstændigt svar beregner begge sandsynligheder og skelner sensitivitet fra positiv prædiktiv værdi.",
                ),
                "",
            ),
        ),
        assessment_items=module.assessment_items
        + (
            objective_mcq(
                "bmb830.m03.book.001",
                (
                    "¿Qué información adicional se necesita para convertir sensibilidad y especificidad en P(D|+)?",
                    "What additional information is needed to convert sensitivity and specificity into P(D|+)?",
                    "Hvilken yderligere information kræves for at omdanne sensitivitet og specificitet til P(D|+)?",
                ),
                (
                    (
                        "sample_mean",
                        ("La media de una variable continua.", "The mean of a continuous variable.", "Gennemsnittet af en kontinuert variabel."),
                    ),
                    (
                        "prevalence",
                        ("La prevalencia en la población objetivo.", "Prevalence in the target population.", "Prævalensen i målpopulationen."),
                    ),
                    (
                        "plot_colour",
                        ("El color usado en el gráfico.", "The colour used in the plot.", "Farven anvendt i figuren."),
                    ),
                ),
                "prevalence",
                (
                    "Bayes combina las probabilidades condicionadas de la prueba con la tasa basal de enfermedad.",
                    "Bayes combines the test's conditional probabilities with the disease base rate.",
                    "Bayes kombinerer testens betingede sandsynligheder med sygdommens basisrate.",
                ),
            ),
        ),
    )
    return _with_source_basis(extended)


def _extend_estimation(module: LocalizedLearningModule) -> LocalizedLearningModule:
    extended = replace(
        module,
        objectives=module.objectives
        + (
            objective(
                "m04.bg.o1",
                (
                    "Construir un intervalo bootstrap respetando la unidad independiente y declarar sus límites.",
                    "Construct a bootstrap interval while respecting the independent unit and state its limitations.",
                    "Konstruere et bootstrap-interval med respekt for den uafhængige enhed og angive dets begrænsninger.",
                ),
            ),
        ),
        concepts=module.concepts
        + (
            concept(
                "bootstrap-resampling-and-design-units",
                (
                    "Bootstrap, remuestreo y unidad de diseño",
                    "Bootstrap resampling and design units",
                    "Bootstrap-resampling og designenheder",
                ),
                (
                    "El bootstrap no paramétrico aproxima la distribución muestral remuestreando con reemplazo unidades observadas del mismo tamaño que la muestra y recalculando el estimador. Los percentiles de las réplicas pueden formar un intervalo, pero el procedimiento hereda sesgo, dependencia, falta de representatividad y errores de medición de los datos originales. La unidad de remuestreo debe coincidir con la unidad independiente: pacientes completos en datos longitudinales, pares completos en diseños pareados y, cuando existe agrupación, conglomerados o bloques completos en lugar de filas aisladas. Una semilla hace reproducible una aproximación Monte Carlo; no vuelve válido un diseño incorrecto.",
                    "The nonparametric bootstrap approximates a sampling distribution by resampling observed units with replacement at the original sample size and recalculating the estimator. Percentiles of the replicates can form an interval, but the procedure inherits bias, dependence, lack of representativeness, and measurement error from the original data. The resampling unit must match the independent unit: complete patients for longitudinal data, complete pairs for paired designs, and whole clusters or blocks rather than isolated rows when grouping is present. A seed makes a Monte Carlo approximation reproducible; it does not make an invalid design valid.",
                    "Det ikke-parametriske bootstrap approksimerer en stikprøvefordeling ved at resample observerede enheder med tilbagelægning i samme stikprøvestørrelse og genberegne estimatoren. Percentiler af replikaterne kan danne et interval, men proceduren arver bias, afhængighed, manglende repræsentativitet og målefejl fra de oprindelige data. Resamplingsenheden skal svare til den uafhængige enhed: hele patienter i longitudinelle data, hele par i parrede design og hele klynger eller blokke frem for enkelte rækker ved gruppering. Et seed gør en Monte Carlo-approksimation reproducerbar; det gør ikke et ugyldigt design gyldigt.",
                ),
                (
                    (
                        "Cada réplica conserva el tamaño muestral y usa reemplazo.",
                        "Each replicate preserves sample size and samples with replacement.",
                        "Hvert replikat bevarer stikprøvestørrelsen og anvender tilbagelægning.",
                    ),
                    (
                        "Se recalcula el estimador completo en cada réplica.",
                        "The complete estimator is recalculated in every replicate.",
                        "Hele estimatoren genberegnes i hvert replikat.",
                    ),
                    (
                        "La unidad de remuestreo debe preservar la dependencia del diseño.",
                        "The resampling unit must preserve design dependence.",
                        "Resamplingsenheden skal bevare designets afhængighed.",
                    ),
                    (
                        "Bootstrap no corrige automáticamente sesgo ni mala representatividad.",
                        "Bootstrap does not automatically correct bias or poor representativeness.",
                        "Bootstrap korrigerer ikke automatisk bias eller dårlig repræsentativitet.",
                    ),
                ),
            ),
        ),
        worked_examples=module.worked_examples
        + (
            example(
                "m04.bg.e01",
                (
                    "Bootstrap exhaustivo de una media pequeña",
                    "Exhaustive bootstrap for a small mean",
                    "Udtømmende bootstrap for et lille gennemsnit",
                ),
                (
                    "Enumera las 4^4 muestras bootstrap posibles de cuatro unidades y obtiene un intervalo percentil determinista.",
                    "Enumerate all 4^4 bootstrap samples from four units and obtain a deterministic percentile interval.",
                    "Enumerér alle 4^4 bootstrap-stikprøver fra fire enheder og opnå et deterministisk percentilinterval.",
                ),
                (
                    (
                        "Cada fila de índices representa una muestra con reemplazo de tamaño cuatro.",
                        "Each index row represents a size-four sample with replacement.",
                        "Hver indeksrække repræsenterer en stikprøve med tilbagelægning af størrelse fire.",
                    ),
                    (
                        "El estimador de cada réplica es la media.",
                        "The estimator in every replicate is the mean.",
                        "Estimatoren i hvert replikat er gennemsnittet.",
                    ),
                ),
                """x <- c(2, 4, 5, 9)
indices <- expand.grid(rep(list(seq_along(x)), length(x)))
bootstrap_means <- apply(indices, 1, function(i) mean(x[as.integer(i)]))
ci <- quantile(bootstrap_means, c(0.025, 0.975), names = FALSE, type = 1)
cat(sprintf("observed=%.2f\n", mean(x)))
cat(sprintf("resamples=%d\n", length(bootstrap_means)))
cat(sprintf("ci=[%.2f, %.2f]\n", ci[1], ci[2]))
""",
                """observed=5.00
resamples=256
ci=[2.75, 7.75]""",
                (
                    "La enumeración elimina error Monte Carlo en este ejemplo pequeño, pero el intervalo sigue dependiendo de que las cuatro observaciones sean unidades independientes y representativas del mecanismo objetivo.",
                    "Enumeration removes Monte Carlo error in this small example, but the interval still depends on the four observations being independent units representative of the target mechanism.",
                    "Enumerationen fjerner Monte Carlo-fejl i dette lille eksempel, men intervallet afhænger stadig af, at de fire observationer er uafhængige enheder, der repræsenterer målmekanismen.",
                ),
            ),
        ),
        practice_exercises=module.practice_exercises
        + (
            practice(
                "m04.bg.p01",
                ActivityType.PIPELINE_DESIGN,
                (
                    "Un estudio contiene cinco mediciones por paciente. Diseña un bootstrap para la media entre pacientes y explica por qué remuestrear las filas individuales es incorrecto.",
                    "A study contains five measurements per patient. Design a bootstrap for the patient-level mean and explain why resampling individual rows is incorrect.",
                    "Et studie indeholder fem målinger pr. patient. Design et bootstrap for gennemsnittet mellem patienter og forklar, hvorfor resampling af enkelte rækker er forkert.",
                ),
                (
                    (
                        "Identifica primero la unidad independiente.",
                        "Identify the independent unit first.",
                        "Identificér først den uafhængige enhed.",
                    ),
                    (
                        "Conserva juntas todas las mediciones de un paciente.",
                        "Keep all measurements from one patient together.",
                        "Hold alle målinger fra én patient samlet.",
                    ),
                ),
                (
                    "Remuestrear pacientes completos con reemplazo, mantener sus cinco mediciones juntas y recalcular todo el estimador en cada réplica. Remuestrear filas trataría mediciones correlacionadas como unidades independientes y produciría incertidumbre demasiado optimista.",
                    "Resample complete patients with replacement, keep their five measurements together, and recalculate the full estimator in every replicate. Resampling rows would treat correlated measurements as independent units and produce overly optimistic uncertainty.",
                    "Resample hele patienter med tilbagelægning, hold deres fem målinger samlet, og genberegn hele estimatoren i hvert replikat. Resampling af rækker ville behandle korrelerede målinger som uafhængige enheder og give for optimistisk usikkerhed.",
                ),
                (
                    "Una respuesta completa conserva la estructura longitudinal y distingue número de filas de tamaño muestral efectivo.",
                    "A complete answer preserves longitudinal structure and distinguishes row count from effective sample size.",
                    "Et fuldstændigt svar bevarer den longitudinelle struktur og skelner antal rækker fra effektiv stikprøvestørrelse.",
                ),
                "",
            ),
        ),
        assessment_items=module.assessment_items
        + (
            objective_mcq(
                "bmb830.m04.book.001",
                (
                    "¿Qué se debe remuestrear en un bootstrap de datos longitudinales agrupados por paciente?",
                    "What should be resampled in a bootstrap of longitudinal data grouped by patient?",
                    "Hvad skal resamples i et bootstrap af longitudinelle data grupperet efter patient?",
                ),
                (
                    (
                        "isolated_rows",
                        ("Filas aisladas ignorando paciente.", "Isolated rows while ignoring patient.", "Enkelte rækker uden hensyn til patient."),
                    ),
                    (
                        "complete_patients",
                        ("Pacientes completos con sus mediciones.", "Complete patients with their measurements.", "Hele patienter med deres målinger."),
                    ),
                    (
                        "only_outliers",
                        ("Sólo las observaciones extremas.", "Only the extreme observations.", "Kun de ekstreme observationer."),
                    ),
                ),
                "complete_patients",
                (
                    "La unidad de remuestreo debe preservar la dependencia que define el diseño.",
                    "The resampling unit must preserve the dependence defined by the design.",
                    "Resamplingsenheden skal bevare den afhængighed, som designet definerer.",
                ),
            ),
        ),
    )
    return _with_source_basis(extended)


def apply_foundation_review(module: LocalizedLearningModule) -> LocalizedLearningModule:
    """Attach source traceability and focused additions to reviewed modules M01-M04."""

    if module.module_id == "bmb830.m03":
        return _extend_probability(module)
    if module.module_id == "bmb830.m04":
        return _extend_estimation(module)
    if module.module_id in {"bmb830.m01", "bmb830.m02"}:
        return _with_source_basis(module)
    return module


__all__ = [
    "AcademicReference",
    "BMB830_BOOK_SOURCES",
    "BMB830_MODULE_SOURCE_AUDIT",
    "ModuleSourceAudit",
    "VerificationState",
    "apply_foundation_review",
]
