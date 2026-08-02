"""Focused source-grounded extensions for BMB830 nonlinear modelling and validation."""

from __future__ import annotations

from dataclasses import replace

from ...learning.activity_types import ActivityType
from ..localized_models import LocalizedLearningModule, LocalizedTutorSupportPacket
from .authoring import concept, example, objective, objective_mcq, practice, same
from .book_grounded_audit import ModuleSourceAudit


def _with_source_basis(
    module: LocalizedLearningModule,
    source_ids: tuple[str, ...],
) -> LocalizedLearningModule:
    tutor = module.tutor_support
    merged = tuple(dict.fromkeys((*tutor.source_basis, *source_ids)))
    updated_tutor: LocalizedTutorSupportPacket = replace(tutor, source_basis=merged)
    return replace(module, tutor_support=updated_tutor)


def update_model_diagnostics_audit(
    audit: tuple[ModuleSourceAudit, ...],
) -> tuple[ModuleSourceAudit, ...]:
    """Mark M09-M10 reviewed after focused nonlinear and validation extensions."""

    findings = {
        "bmb830.m09": (
            "Existing coverage of effect modification, product terms, hierarchy, centring, "
            "conditional slopes, quadratic curvature, nested comparisons, and extrapolation is "
            "conceptually strong. The nonlinear block stopped at a global polynomial and needed "
            "one explicit local basis treatment. The existing quadratic worked example also "
            "contained incorrect coefficient, p-value, and prediction output."
        ),
        "bmb830.m10": (
            "Existing coverage of residual patterns, heteroscedasticity, leverage, studentised "
            "residuals, Cook's distance, sensitivity analysis, held-out validation, leakage, and "
            "dependence-aware splitting is consistent with the mapped scope. The exact bridge "
            "between leverage diagnostics and ordinary-least-squares leave-one-out error needed "
            "one explicit treatment."
        ),
    }
    changes = {
        "bmb830.m09": (
            "Added an original trilingual piecewise-linear hinge-basis explanation, deterministic "
            "local-slope example, interpretation exercise, stable objective item, and corrected "
            "the numerical output of the existing quadratic example."
        ),
        "bmb830.m10": (
            "Added an original trilingual PRESS and leave-one-out identity explanation, "
            "deterministic validation example, leakage-boundary exercise, and stable objective "
            "item."
        ),
    }

    updated: list[ModuleSourceAudit] = []
    for item in audit:
        if item.module_id == "bmb830.m09":
            updated.append(
                replace(
                    item,
                    source_ids=tuple(dict.fromkeys((*item.source_ids, "islr-2021-ch07"))),
                    source_scope=item.source_scope
                    + (
                        "piecewise-linear basis functions and local slope changes",
                        "global polynomial versus local basis flexibility",
                    ),
                    state="correct",
                    finding=findings[item.module_id],
                    implemented_change=changes[item.module_id],
                )
            )
        elif item.module_id == "bmb830.m10":
            updated.append(
                replace(
                    item,
                    source_scope=item.source_scope
                    + (
                        "PRESS residuals and the OLS leave-one-out identity",
                        "training error versus cross-validated prediction error",
                    ),
                    state="consistent",
                    finding=findings[item.module_id],
                    implemented_change=changes[item.module_id],
                )
            )
        else:
            updated.append(item)
    return tuple(updated)


def _correct_example_output(
    module: LocalizedLearningModule,
    example_id: str,
    expected_output: str,
) -> LocalizedLearningModule:
    corrected = tuple(
        replace(item, expected_output=same(expected_output))
        if item.example_id == example_id
        else item
        for item in module.worked_examples
    )
    return replace(module, worked_examples=corrected)


def _extend_interactions_nonlinearity(
    module: LocalizedLearningModule,
) -> LocalizedLearningModule:
    corrected = _correct_example_output(
        module,
        "m09.e02",
        "quadratic=0.344\ncomparison_p=0.0000\n2.34, 1.04, 2.49",
    )
    extended = replace(
        corrected,
        objectives=corrected.objectives
        + (
            objective(
                "m09.bg.o1",
                (
                    "Representar un cambio local de pendiente mediante una base lineal por tramos y distinguirla de un polinomio global.",
                    "Represent a local slope change with a piecewise-linear basis and distinguish it from a global polynomial.",
                    "Repræsentere en lokal ændring i hældning med en stykkevis lineær basis og skelne den fra et globalt polynomium.",
                ),
            ),
        ),
        concepts=corrected.concepts
        + (
            concept(
                "piecewise-linear-basis-and-local-slopes",
                (
                    "Base lineal por tramos y pendientes locales",
                    "Piecewise-linear basis and local slopes",
                    "Stykkevis lineær basis og lokale hældninger",
                ),
                (
                    "Una función bisagra se define como (x-k)+ = max(0, x-k), donde k es un nudo. En el modelo E(Y|X)=β0+β1X+β2(X-k)+, la curva es continua en k: antes del nudo la pendiente es β1 y después es β1+β2. El coeficiente β2 es un cambio de pendiente, no la pendiente posterior completa. Esta base modifica la forma localmente después del nudo, mientras que un término polinomial global altera la curva en todo el rango. Los nudos deben justificarse científicamente o seleccionarse dentro del procedimiento de validación; buscarlos repetidamente en todos los datos y después informar inferencia ordinaria produce optimismo. La representación flexible tampoco elimina el riesgo de extrapolación.",
                    "A hinge function is defined as (x-k)+ = max(0, x-k), where k is a knot. In E(Y|X)=beta0+beta1 X+beta2 (X-k)+, the curve is continuous at k: the slope before the knot is beta1 and the slope after it is beta1+beta2. Beta2 is a change in slope, not the complete post-knot slope. This basis changes the shape locally after the knot, whereas a global polynomial term changes the curve across the full range. Knots should be scientifically justified or selected inside the validation procedure; repeatedly searching all data and then reporting ordinary inference creates optimism. Flexible representation also does not remove extrapolation risk.",
                    "En hængselfunktion defineres som (x-k)+ = max(0, x-k), hvor k er et knudepunkt. I E(Y|X)=beta0+beta1 X+beta2 (X-k)+ er kurven kontinuert ved k: hældningen før knuden er beta1, og hældningen efter er beta1+beta2. Beta2 er en ændring i hældning, ikke hele hældningen efter knuden. Denne basis ændrer formen lokalt efter knuden, mens et globalt polynomium ændrer kurven over hele området. Knuder bør begrundes videnskabeligt eller vælges inde i valideringsproceduren; gentagen søgning i alle data efterfulgt af almindelig inferens skaber optimisme. Fleksibel repræsentation fjerner heller ikke risikoen ved ekstrapolation.",
                ),
                (
                    (
                        "La bisagra vale cero antes del nudo y crece linealmente después.",
                        "The hinge is zero before the knot and increases linearly afterwards.",
                        "Hængslet er nul før knuden og vokser lineært derefter.",
                    ),
                    (
                        "La pendiente posterior es β1+β2, no β2.",
                        "The post-knot slope is beta1+beta2, not beta2.",
                        "Hældningen efter knuden er beta1+beta2, ikke beta2.",
                    ),
                    (
                        "Una base local puede ser más estable en los extremos que un polinomio global de alto grado.",
                        "A local basis can be more stable near the boundaries than a high-degree global polynomial.",
                        "En lokal basis kan være mere stabil nær grænserne end et globalt polynomium af høj grad.",
                    ),
                    (
                        "La selección del nudo forma parte del proceso de modelado y validación.",
                        "Knot selection is part of the modelling and validation process.",
                        "Valg af knude er en del af modellerings- og valideringsprocessen.",
                    ),
                ),
            ),
        ),
        worked_examples=corrected.worked_examples
        + (
            example(
                "m09.bg.e01",
                (
                    "Recuperar pendientes antes y después de un nudo",
                    "Recover slopes before and after a knot",
                    "Genskab hældninger før og efter en knude",
                ),
                (
                    "Ajusta una base bisagra a datos sintéticos continuos y recupera ambas pendientes locales.",
                    "Fit a hinge basis to continuous synthetic data and recover both local slopes.",
                    "Tilpas en hængselbasis til kontinuerte syntetiske data og genskab begge lokale hældninger.",
                ),
                (
                    (
                        "El nudo se fija en x=3 antes del ajuste.",
                        "The knot is fixed at x=3 before fitting.",
                        "Knuden fastlægges ved x=3 før tilpasningen.",
                    ),
                    (
                        "La columna hinge es pmax(0, x-knot).",
                        "The hinge column is pmax(0, x-knot).",
                        "Hængselkolonnen er pmax(0, x-knot).",
                    ),
                    (
                        "La segunda pendiente suma el coeficiente lineal y el cambio de pendiente.",
                        "The second slope adds the linear coefficient and the slope change.",
                        "Den anden hældning summerer den lineære koefficient og ændringen i hældning.",
                    ),
                ),
                """x <- 0:6
knot <- 3
hinge <- pmax(0, x - knot)
response <- 1 + 0.5 * x + 1.5 * hinge
fit <- lm(response ~ x + hinge)
b <- coef(fit)
new_x <- c(2, 5)
new_data <- data.frame(x = new_x, hinge = pmax(0, new_x - knot))
predicted <- predict(fit, newdata = new_data)
cat(sprintf("slope_before=%.2f\n", b[["x"]]))
cat(sprintf("slope_after=%.2f\n", b[["x"]] + b[["hinge"]]))
cat(sprintf("predictions=%s", paste(sprintf("%.2f", predicted), collapse = ", ")))
""",
                """slope_before=0.50
slope_after=2.00
predictions=2.00, 6.50""",
                (
                    "El coeficiente de hinge es 1,50, pero la pendiente posterior completa es 0,50+1,50=2,00. La continuidad surge porque la bisagra vale cero exactamente en el nudo.",
                    "The hinge coefficient is 1.50, but the complete post-knot slope is 0.50+1.50=2.00. Continuity follows because the hinge equals zero exactly at the knot.",
                    "Hængselkoefficienten er 1,50, men hele hældningen efter knuden er 0,50+1,50=2,00. Kontinuiteten følger af, at hængslet er nul præcis ved knuden.",
                ),
            ),
        ),
        practice_exercises=corrected.practice_exercises
        + (
            practice(
                "m09.bg.p01",
                ActivityType.DATA_INTERPRETATION,
                (
                    "En modelo Y~x+pmax(0,x-4), βx=0,7 y βhinge=−0,3. Interpreta ambas pendientes y explica qué representa βhinge.",
                    "In Y~x+pmax(0,x-4), beta_x=0.7 and beta_hinge=-0.3. Interpret both slopes and explain beta_hinge.",
                    "I Y~x+pmax(0,x-4) er beta_x=0,7 og beta_hinge=-0,3. Fortolk begge hældninger og forklar beta_hinge.",
                ),
                (
                    (
                        "Antes del nudo la bisagra es cero.",
                        "Before the knot the hinge is zero.",
                        "Før knuden er hængslet nul.",
                    ),
                    (
                        "Después del nudo deriva ambos términos respecto de x.",
                        "After the knot, differentiate both terms with respect to x.",
                        "Efter knuden differentieres begge led med hensyn til x.",
                    ),
                ),
                (
                    "Antes de x=4, la pendiente es 0,7. Después de x=4, la pendiente es 0,7−0,3=0,4. βhinge=−0,3 representa el cambio de pendiente al cruzar el nudo, no una pendiente independiente ni la pendiente posterior completa.",
                    "Before x=4, the slope is 0.7. After x=4, the slope is 0.7-0.3=0.4. Beta_hinge=-0.3 is the change in slope at the knot, not an independent slope or the complete post-knot slope.",
                    "Før x=4 er hældningen 0,7. Efter x=4 er hældningen 0,7-0,3=0,4. Beta_hinge=-0,3 er ændringen i hældning ved knuden, ikke en selvstændig hældning eller hele hældningen efter knuden.",
                ),
                (
                    "La parametrización mantiene una curva continua con una pendiente distinta a cada lado del nudo.",
                    "The parameterisation keeps the curve continuous with a different slope on each side of the knot.",
                    "Parametriseringen holder kurven kontinuert med forskellig hældning på hver side af knuden.",
                ),
            ),
        ),
        assessment_items=corrected.assessment_items
        + (
            objective_mcq(
                "bmb830.m09.book.001",
                (
                    "En E(Y|X)=β0+β1X+β2(X-k)+, ¿cuál es la pendiente cuando X>k?",
                    "In E(Y|X)=beta0+beta1 X+beta2 (X-k)+, what is the slope when X>k?",
                    "Hvad er hældningen for X>k i E(Y|X)=beta0+beta1 X+beta2 (X-k)+?",
                ),
                (
                    (
                        "beta1",
                        ("β1", "beta1", "beta1"),
                    ),
                    (
                        "beta2",
                        ("β2", "beta2", "beta2"),
                    ),
                    (
                        "beta1_plus_beta2",
                        ("β1+β2", "beta1+beta2", "beta1+beta2"),
                    ),
                ),
                "beta1_plus_beta2",
                (
                    "Después del nudo, tanto X como la bisagra aumentan una unidad por cada unidad adicional de X.",
                    "After the knot, both X and the hinge increase by one for each additional unit of X.",
                    "Efter knuden stiger både X og hængslet med én for hver ekstra enhed X.",
                ),
            ),
        ),
    )
    return _with_source_basis(
        extended,
        (
            "sdu-bmb830-active-2025",
            "ims-2024-regression-models",
            "islr-2021-ch02-05",
            "islr-2021-ch07",
        ),
    )


def _extend_diagnostics_validation(
    module: LocalizedLearningModule,
) -> LocalizedLearningModule:
    extended = replace(
        module,
        objectives=module.objectives
        + (
            objective(
                "m10.bg.o1",
                (
                    "Relacionar residuos ordinarios, leverage, residuos PRESS y error leave-one-out en una regresión lineal de diseño fijo.",
                    "Relate ordinary residuals, leverage, PRESS residuals, and leave-one-out error in fixed-design linear regression.",
                    "Knytte ordinære residualer, leverage, PRESS-residualer og leave-one-out-fejl sammen i lineær regression med fast design.",
                ),
            ),
        ),
        concepts=module.concepts
        + (
            concept(
                "press-residuals-and-loocv",
                (
                    "Residuos PRESS y validación leave-one-out",
                    "PRESS residuals and leave-one-out validation",
                    "PRESS-residualer og leave-one-out-validering",
                ),
                (
                    "En mínimos cuadrados ordinarios con una matriz de diseño fija, el residuo de la observación i cuando el modelo se reajusta sin esa observación es e(i)=ei/(1-hii), donde ei es el residuo ordinario y hii su leverage. PRESS suma los cuadrados de estos residuos eliminados y sqrt(PRESS/n) es el RMSE leave-one-out. El denominador muestra por qué el mismo residuo ordinario produce una penalización mayor cuando hii es alto. Esta identidad conecta diagnóstico e información fuera de muestra sin requerir n reajustes explícitos, pero sólo para el mismo modelo lineal y las mismas columnas de diseño. Imputación, escalado aprendido, selección de variables, elección de nudos o ajuste de hiperparámetros deben repetirse dentro de cada fold; aplicar la identidad después de preparar los datos con toda la muestra no valida la canalización completa.",
                    "For ordinary least squares with a fixed design matrix, the residual for observation i after refitting without that observation is e_(i)=e_i/(1-h_ii), where e_i is the ordinary residual and h_ii is its leverage. PRESS sums the squared deleted residuals, and sqrt(PRESS/n) is the leave-one-out RMSE. The denominator shows why the same ordinary residual receives a larger penalty when h_ii is high. This identity connects diagnostics with out-of-sample information without n explicit refits, but only for the same linear model and the same design columns. Learned imputation, scaling, variable selection, knot choice, or hyperparameter tuning must be repeated inside every fold; applying the identity after preparing data with the full sample does not validate the complete pipeline.",
                    "For ordinære mindste kvadrater med en fast designmatrix er residualen for observation i efter gentilpasning uden observationen e_(i)=e_i/(1-h_ii), hvor e_i er den ordinære residual, og h_ii er dens leverage. PRESS summerer de kvadrerede slettede residualer, og sqrt(PRESS/n) er leave-one-out-RMSE. Nævneren viser, hvorfor den samme ordinære residual straffes mere, når h_ii er høj. Identiteten forbinder diagnostik med information uden for stikprøven uden n eksplicitte gentilpasninger, men kun for samme lineære model og samme designkolonner. Lært imputering, skalering, variabelvalg, valg af knuder eller hyperparametertuning skal gentages inde i hvert fold; identiteten validerer ikke hele pipelinen, hvis data først er forberedt med hele stikprøven.",
                ),
                (
                    (
                        "PRESS usa residuos eliminados, no residuos ordinarios.",
                        "PRESS uses deleted residuals, not ordinary residuals.",
                        "PRESS bruger slettede residualer, ikke ordinære residualer.",
                    ),
                    (
                        "Cuando hii se aproxima a uno, 1-hii amplifica fuertemente el error leave-one-out.",
                        "As h_ii approaches one, 1-h_ii strongly amplifies leave-one-out error.",
                        "Når h_ii nærmer sig én, forstærker 1-h_ii leave-one-out-fejlen kraftigt.",
                    ),
                    (
                        "El RMSE de entrenamiento suele ser optimista respecto del RMSE leave-one-out.",
                        "Training RMSE is usually optimistic relative to leave-one-out RMSE.",
                        "Trænings-RMSE er normalt optimistisk i forhold til leave-one-out-RMSE.",
                    ),
                    (
                        "La identidad no sustituye validación externa ni resampling de una canalización adaptativa.",
                        "The identity does not replace external validation or resampling an adaptive pipeline.",
                        "Identiteten erstatter ikke ekstern validering eller resampling af en adaptiv pipeline.",
                    ),
                ),
            ),
        ),
        worked_examples=module.worked_examples
        + (
            example(
                "m10.bg.e01",
                (
                    "Calcular PRESS sin reajustar seis modelos",
                    "Compute PRESS without refitting six models",
                    "Beregn PRESS uden at gentilpasse seks modeller",
                ),
                (
                    "Compara el RMSE de entrenamiento con el RMSE leave-one-out obtenido mediante leverage.",
                    "Compare training RMSE with leave-one-out RMSE obtained through leverage.",
                    "Sammenlign trænings-RMSE med leave-one-out-RMSE beregnet via leverage.",
                ),
                (
                    (
                        "Ajusta una única regresión lineal con intercepto.",
                        "Fit one linear regression with an intercept.",
                        "Tilpas én lineær regression med skæring.",
                    ),
                    (
                        "Divide cada residuo por uno menos su leverage.",
                        "Divide every residual by one minus its leverage.",
                        "Divider hver residual med én minus dens leverage.",
                    ),
                    (
                        "Resume los residuos eliminados con PRESS y RMSE.",
                        "Summarise the deleted residuals with PRESS and RMSE.",
                        "Opsummér de slettede residualer med PRESS og RMSE.",
                    ),
                ),
                """x <- 1:6
response <- c(1, 2, 3, 4, 5, 8)
fit <- lm(response ~ x)
ordinary_residual <- residuals(fit)
leverage <- hatvalues(fit)
loo_residual <- ordinary_residual / (1 - leverage)
press <- sum(loo_residual^2)
train_rmse <- sqrt(mean(ordinary_residual^2))
loocv_rmse <- sqrt(mean(loo_residual^2))
cat(sprintf("train_rmse=%.3f\n", train_rmse))
cat(sprintf("loocv_rmse=%.3f\n", loocv_rmse))
cat(sprintf("press=%.3f\n", press))
cat(sprintf("largest_loo_residual=%.3f", max(abs(loo_residual))))
""",
                """train_rmse=0.563
loocv_rmse=1.018
press=6.219
largest_loo_residual=2.000""",
                (
                    "El error leave-one-out es mayor que el error aparente de entrenamiento. La observación extrema combina discrepancia y leverage, por lo que su residuo eliminado alcanza 2,00.",
                    "Leave-one-out error is larger than apparent training error. The extreme observation combines discrepancy and leverage, so its deleted residual reaches 2.00.",
                    "Leave-one-out-fejlen er større end den tilsyneladende træningsfejl. Den ekstreme observation kombinerer afvigelse og leverage, så dens slettede residual når 2,00.",
                ),
            ),
        ),
        practice_exercises=module.practice_exercises
        + (
            practice(
                "m10.bg.p01",
                ActivityType.DEBUGGING,
                (
                    "Un analista imputa faltantes, estandariza variables y selecciona predictores usando toda la muestra; luego calcula ei/(1-hii) y lo presenta como validación leave-one-out de la canalización. Diagnostica el error.",
                    "An analyst imputes missing values, standardises variables, and selects predictors using the full sample; then computes e_i/(1-h_ii) and presents it as leave-one-out validation of the pipeline. Diagnose the error.",
                    "En analytiker imputerer manglende værdier, standardiserer variable og vælger prædiktorer med hele stikprøven; derefter beregnes e_i/(1-h_ii) og præsenteres som leave-one-out-validering af pipelinen. Diagnosticér fejlen.",
                ),
                (
                    (
                        "Pregunta qué información utilizó cada transformación.",
                        "Ask which observations informed each transformation.",
                        "Spørg hvilke observationer der informerede hver transformation.",
                    ),
                    (
                        "La identidad PRESS supone columnas de diseño fijas.",
                        "The PRESS identity assumes fixed design columns.",
                        "PRESS-identiteten antager faste designkolonner.",
                    ),
                ),
                (
                    "Existe fuga de información porque imputación, escalado y selección usaron también la observación que debía quedar fuera. La identidad PRESS valida el ajuste OLS de una matriz de diseño fija, no una canalización adaptativa preparada con toda la muestra. Cada transformación y selección debe aprenderse exclusivamente con el fold de entrenamiento y aplicarse al fold reservado. Si además se elige complejidad, la estimación no sesgada del rendimiento requiere una capa externa de validación o datos externos.",
                    "There is information leakage because imputation, scaling, and selection also used the observation that should have been held out. PRESS validates the OLS fit for a fixed design matrix, not an adaptive pipeline prepared on the full sample. Every transformation and selection step must be learned only from the training fold and then applied to the held-out fold. If complexity is also selected, an unbiased performance estimate requires an outer validation layer or external data.",
                    "Der er informationslækage, fordi imputering, skalering og udvælgelse også brugte den observation, der skulle holdes ude. PRESS validerer OLS-tilpasningen for en fast designmatrix, ikke en adaptiv pipeline forberedt på hele stikprøven. Hvert transformations- og udvælgelsestrin skal læres udelukkende i træningsfoldet og derefter anvendes på det reserverede fold. Hvis kompleksitet også vælges, kræver et upartisk præstationsestimat et ydre valideringslag eller eksterne data.",
                ),
                (
                    "Resampling skal omfatte hele den datadrevne modelleringsprocedure.",
                    "Resampling must enclose the full data-driven modelling procedure.",
                    "Resampling skal omslutte hele den datadrevne modelleringsprocedure.",
                ),
            ),
        ),
        assessment_items=module.assessment_items
        + (
            objective_mcq(
                "bmb830.m10.book.001",
                (
                    "Para OLS con diseño fijo, ¿cuál es el residuo leave-one-out de la observación i?",
                    "For fixed-design OLS, what is the leave-one-out residual for observation i?",
                    "Hvad er leave-one-out-residualen for observation i ved OLS med fast design?",
                ),
                (
                    (
                        "ordinary",
                        ("ei", "e_i", "e_i"),
                    ),
                    (
                        "divide_one_minus_h",
                        ("ei/(1-hii)", "e_i/(1-h_ii)", "e_i/(1-h_ii)"),
                    ),
                    (
                        "multiply_one_minus_h",
                        ("ei(1-hii)", "e_i(1-h_ii)", "e_i(1-h_ii)"),
                    ),
                ),
                "divide_one_minus_h",
                (
                    "Eliminar una observación amplifica su residuo ordinario por el factor 1/(1-hii).",
                    "Deleting an observation amplifies its ordinary residual by 1/(1-h_ii).",
                    "Sletning af en observation forstærker dens ordinære residual med 1/(1-h_ii).",
                ),
            ),
        ),
    )
    return _with_source_basis(
        extended,
        (
            "sdu-bmb830-active-2025",
            "ims-2024-regression-models",
            "islr-2021-ch02-05",
            "yachay-biostatistics-linear-models",
        ),
    )


def apply_model_diagnostics_review(
    module: LocalizedLearningModule,
) -> LocalizedLearningModule:
    """Apply the focused M09-M10 review to the matching module."""

    if module.module_id == "bmb830.m09":
        return _extend_interactions_nonlinearity(module)
    if module.module_id == "bmb830.m10":
        return _extend_diagnostics_validation(module)
    return module
