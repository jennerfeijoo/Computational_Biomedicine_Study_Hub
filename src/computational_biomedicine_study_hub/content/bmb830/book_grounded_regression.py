"""Focused source-grounded extensions and corrections for BMB830 regression models."""

from __future__ import annotations

from dataclasses import replace

from ...learning.activity_types import ActivityType
from ..localized_models import LocalizedLearningModule, LocalizedTutorSupportPacket
from .authoring import concept, example, objective, objective_mcq, practice
from .book_grounded_audit import ModuleSourceAudit


def _with_source_basis(
    module: LocalizedLearningModule,
    source_ids: tuple[str, ...],
) -> LocalizedLearningModule:
    tutor = module.tutor_support
    merged = tuple(dict.fromkeys((*tutor.source_basis, *source_ids)))
    updated_tutor: LocalizedTutorSupportPacket = replace(tutor, source_basis=merged)
    return replace(module, tutor_support=updated_tutor)


def update_regression_audit(
    audit: tuple[ModuleSourceAudit, ...],
) -> tuple[ModuleSourceAudit, ...]:
    """Mark M07-M08 reviewed after their extensions and output corrections are present."""

    findings = {
        "bmb830.m07": (
            "Existing coverage of association versus causation, Pearson and Spearman correlation, "
            "simple linear models, confidence and prediction intervals, R-squared, and "
            "extrapolation boundaries is conceptually strong. The exact scale-dependent bridge "
            "between correlation, slope, and R-squared required one explicit treatment, and one "
            "worked prediction example contained incorrect rounded interval output."
        ),
        "bmb830.m08": (
            "Existing coverage of conditional means, design matrices, categorical predictors, "
            "reference levels, confounding, collinearity, and overfitting is conceptually strong. "
            "The operational meaning of an adjusted coefficient through partial regression "
            "required one explicit treatment, and both existing worked examples contained "
            "incorrect numerical output."
        ),
    }
    changes = {
        "bmb830.m07": (
            "Added an original trilingual correlation-slope identity explanation, deterministic "
            "standardisation example, interpretation exercise, stable objective item, and "
            "corrected the confidence and prediction interval output."
        ),
        "bmb830.m08": (
            "Added an original trilingual partial-regression explanation, deterministic "
            "residualisation example, interpretation exercise, stable objective item, and "
            "corrected the numerical output of both existing worked examples."
        ),
    }

    updated: list[ModuleSourceAudit] = []
    for item in audit:
        if item.module_id == "bmb830.m07":
            updated.append(
                replace(
                    item,
                    source_ids=tuple(dict.fromkeys((*item.source_ids, "islr-2021-ch02-05"))),
                    source_scope=item.source_scope
                    + (
                        "correlation-slope scale identity",
                        "standardisation and simple-regression R-squared",
                    ),
                    state="correct",
                    finding=findings[item.module_id],
                    implemented_change=changes[item.module_id],
                )
            )
        elif item.module_id == "bmb830.m08":
            updated.append(
                replace(
                    item,
                    source_scope=item.source_scope
                    + (
                        "partial regression and residualisation",
                        "adjusted coefficients as conditional linear associations",
                    ),
                    state="correct",
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
        replace(item, expected_output=expected_output) if item.example_id == example_id else item
        for item in module.worked_examples
    )
    return replace(module, worked_examples=corrected)


def _extend_simple_regression(module: LocalizedLearningModule) -> LocalizedLearningModule:
    corrected = _correct_example_output(
        module,
        "m07.e02",
        "mean=5.55\nmean_ci=[5.31, 5.79]\nprediction=[4.99, 6.12]",
    )
    extended = replace(
        corrected,
        objectives=corrected.objectives
        + (
            objective(
                "m07.bg.o1",
                (
                    "Relacionar correlación, pendiente, escala y R² en una regresión lineal simple con intercepto.",
                    "Relate correlation, slope, scale, and R-squared in simple linear regression with an intercept.",
                    "Knytte korrelation, hældning, skala og R-kvadreret sammen i simpel lineær regression med skæring.",
                ),
            ),
        ),
        concepts=corrected.concepts
        + (
            concept(
                "correlation-slope-and-standardisation",
                (
                    "Correlación, pendiente y estandarización",
                    "Correlation, slope, and standardisation",
                    "Korrelation, hældning og standardisering",
                ),
                (
                    "En una regresión lineal simple por mínimos cuadrados con intercepto, la pendiente estimada satisface β̂1 = r·sY/sX y R² = r². La correlación r es simétrica, adimensional e invariante ante cambios positivos de unidades; la pendiente no es simétrica y conserva unidades de Y por unidad de X. Por ello, r=0,80 no significa que Y aumente 0,80 unidades cuando X aumenta una unidad. Si X e Y se estandarizan con sus desviaciones estándar muestrales, la pendiente de la regresión estandarizada coincide con r. Centrar X cambia el intercepto, pero no la pendiente ni los valores ajustados. Estas identidades requieren un único predictor y un intercepto y no se trasladan sin cambios a la regresión múltiple.",
                    "In ordinary least-squares simple linear regression with an intercept, the estimated slope satisfies beta-hat-one = r times sY divided by sX, and R-squared equals r squared. Correlation is symmetric, dimensionless, and invariant to positive unit changes; the slope is asymmetric and retains units of Y per unit of X. Therefore, r=0.80 does not mean that Y increases by 0.80 units when X increases by one unit. If X and Y are standardised using their sample standard deviations, the standardised regression slope equals r. Centring X changes the intercept but not the slope or fitted values. These identities require one predictor and an intercept and do not transfer unchanged to multiple regression.",
                    "I simpel mindste-kvadraters regression med en skæring opfylder den estimerede hældning beta-hat-et = r gange sY divideret med sX, og R-kvadreret er lig r i anden. Korrelation er symmetrisk, dimensionsløs og invariant over for positive enhedsskift; hældningen er asymmetrisk og har enheden Y pr. enhed X. Derfor betyder r=0,80 ikke, at Y stiger 0,80 enheder, når X stiger én enhed. Hvis X og Y standardiseres med deres stikprøvestandardafvigelser, er den standardiserede regressionshældning lig r. Centrering af X ændrer skæringen, men ikke hældningen eller de tilpassede værdier. Identiteterne kræver én prædiktor og en skæring og overføres ikke uændret til multipel regression.",
                ),
                (
                    (
                        "La pendiente recupera las unidades mediante sY/sX.",
                        "The slope recovers measurement units through sY/sX.",
                        "Hældningen genvinder måleenheder gennem sY/sX.",
                    ),
                    (
                        "En regresión simple con intercepto, R² y r² son idénticos.",
                        "In simple regression with an intercept, R-squared and r squared are identical.",
                        "I simpel regression med skæring er R-kvadreret og r i anden identiske.",
                    ),
                    (
                        "La correlación estandarizada no es una pendiente en unidades originales.",
                        "Standardised correlation is not a slope in original units.",
                        "Standardiseret korrelation er ikke en hældning i oprindelige enheder.",
                    ),
                    (
                        "Cambiar qué variable es respuesta cambia la regresión, aunque no cambie r.",
                        "Changing which variable is the response changes the regression even though r is unchanged.",
                        "Et skift af responsvariabel ændrer regressionen, selv om r er uændret.",
                    ),
                ),
            ),
        ),
        worked_examples=corrected.worked_examples
        + (
            example(
                "m07.bg.e01",
                (
                    "Comprobar la identidad entre correlación y pendiente",
                    "Verify the correlation-slope identity",
                    "Kontrollér identiteten mellem korrelation og hældning",
                ),
                (
                    "Comprueba en datos sintéticos que la pendiente original es r·sY/sX, que la pendiente estandarizada es r y que R²=r².",
                    "Verify on synthetic data that the original slope is r times sY divided by sX, the standardised slope is r, and R-squared equals r squared.",
                    "Kontrollér på syntetiske data, at den oprindelige hældning er r gange sY divideret med sX, at den standardiserede hældning er r, og at R-kvadreret er lig r i anden.",
                ),
                (
                    (
                        "Se ajusta una regresión con un único predictor e intercepto.",
                        "Fit a regression with one predictor and an intercept.",
                        "Tilpas en regression med én prædiktor og en skæring.",
                    ),
                    (
                        "Las variables estandarizadas conservan la asociación, pero eliminan las unidades.",
                        "The standardised variables retain association while removing units.",
                        "De standardiserede variable bevarer associationen, men fjerner enhederne.",
                    ),
                    (
                        "Las dos identidades se comprueban numéricamente, no se infieren del redondeo.",
                        "Both identities are checked numerically rather than inferred from rounding.",
                        "Begge identiteter kontrolleres numerisk og udledes ikke af afrunding.",
                    ),
                ),
                """x <- c(1, 2, 4, 5, 7)
y <- c(2, 3, 6, 7, 10)
fit <- lm(y ~ x)
r <- cor(x, y)
expected_slope <- r * sd(y) / sd(x)
zx <- (x - mean(x)) / sd(x)
zy <- (y - mean(y)) / sd(y)
standardised_fit <- lm(zy ~ zx)
cat(sprintf("r=%.3f\n", r))
cat(sprintf("slope=%.3f\n", coef(fit)[["x"]]))
cat(sprintf("r_sy_sx=%.3f\n", expected_slope))
cat(sprintf("standardised_slope=%.3f\n", coef(standardised_fit)[["zx"]]))
cat(sprintf("r2=%.3f\n", summary(fit)$r.squared))
cat(sprintf("r_squared=%.3f", r^2))
""",
                """r=0.998
slope=1.342
r_sy_sx=1.342
standardised_slope=0.998
r2=0.997
r_squared=0.997""",
                (
                    "La correlación y la pendiente estandarizada coinciden, mientras que la pendiente original incorpora la razón de escalas. R² coincide con r² únicamente bajo este contrato de regresión simple con intercepto.",
                    "Correlation and the standardised slope coincide, whereas the original slope incorporates the scale ratio. R-squared equals r squared only under this simple-regression-with-intercept contract.",
                    "Korrelationen og den standardiserede hældning er ens, mens den oprindelige hældning indarbejder skalaforholdet. R-kvadreret er kun lig r i anden under denne kontrakt med simpel regression og skæring.",
                ),
            ),
        ),
        practice_exercises=corrected.practice_exercises
        + (
            practice(
                "m07.bg.p01",
                ActivityType.DATA_INTERPRETATION,
                (
                    "Un informe afirma: «r=0,80; por tanto, Y aumenta 0,80 mg/L por cada año adicional de X». Diagnostica la interpretación y especifica qué información falta.",
                    "A report states: 'r=0.80; therefore Y increases by 0.80 mg/L for every additional year of X.' Diagnose the interpretation and specify what information is missing.",
                    "En rapport angiver: 'r=0,80; derfor stiger Y med 0,80 mg/L for hvert ekstra år af X.' Diagnosticér fortolkningen og angiv, hvilke oplysninger der mangler.",
                ),
                (
                    (
                        "Distingue una medida adimensional de una pendiente con unidades.",
                        "Distinguish a dimensionless measure from a slope with units.",
                        "Skeln mellem et dimensionsløst mål og en hældning med enheder.",
                    ),
                    (
                        "Usa la relación entre r, sY, sX y la pendiente.",
                        "Use the relationship among r, sY, sX, and the slope.",
                        "Brug relationen mellem r, sY, sX og hældningen.",
                    ),
                ),
                (
                    "La afirmación es inválida porque r no tiene unidades y es simétrico. La pendiente en mg/L por año sería β̂1=r·sY/sX, por lo que faltan las desviaciones estándar o el ajuste de la regresión en las unidades originales. El valor r=0,80 sólo describe la fuerza y dirección de la asociación lineal muestral; tampoco establece causalidad.",
                    "The statement is invalid because r is unitless and symmetric. The slope in mg/L per year would be beta-hat-one = r times sY divided by sX, so the standard deviations or the fitted regression in original units are missing. The value r=0.80 describes only the strength and direction of the sample linear association and does not establish causation.",
                    "Påstanden er ugyldig, fordi r er uden enhed og symmetrisk. Hældningen i mg/L pr. år ville være beta-hat-et = r gange sY divideret med sX, så standardafvigelserne eller den tilpassede regression i oprindelige enheder mangler. Værdien r=0,80 beskriver kun styrken og retningen af den lineære association i stikprøven og fastslår ikke kausalitet.",
                ),
                (
                    "Una correlación sólo se convierte en pendiente después de restaurar la razón de escalas.",
                    "A correlation becomes a slope only after restoring the scale ratio.",
                    "En korrelation bliver først en hældning, når skalaforholdet genindføres.",
                ),
                "",
            ),
        ),
        assessment_items=corrected.assessment_items
        + (
            objective_mcq(
                "bmb830.m07.book.001",
                (
                    "¿Qué identidad es exacta para una regresión lineal simple por mínimos cuadrados con intercepto?",
                    "Which identity is exact for ordinary least-squares simple linear regression with an intercept?",
                    "Hvilken identitet er eksakt for simpel mindste-kvadraters regression med en skæring?",
                ),
                (
                    (
                        "slope_equals_r",
                        (
                            "La pendiente siempre es igual a r en las unidades originales.",
                            "The slope always equals r in the original units.",
                            "Hældningen er altid lig r i de oprindelige enheder.",
                        ),
                    ),
                    (
                        "slope_scale_identity",
                        (
                            "La pendiente es r·sY/sX y R²=r².",
                            "The slope is r times sY divided by sX, and R-squared equals r squared.",
                            "Hældningen er r gange sY divideret med sX, og R-kvadreret er lig r i anden.",
                        ),
                    ),
                    (
                        "correlation_has_units",
                        (
                            "La correlación tiene las mismas unidades que Y/X.",
                            "Correlation has the same units as Y/X.",
                            "Korrelation har samme enhed som Y/X.",
                        ),
                    ),
                ),
                "slope_scale_identity",
                (
                    "La razón sY/sX restaura las unidades de la pendiente, mientras que R²=r² bajo el contrato simple con intercepto.",
                    "The ratio sY/sX restores slope units, while R-squared equals r squared under the simple model with an intercept.",
                    "Forholdet sY/sX genindfører hældningens enheder, mens R-kvadreret er lig r i anden i den simple model med skæring.",
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


def _extend_multiple_regression(module: LocalizedLearningModule) -> LocalizedLearningModule:
    corrected = _correct_example_output(
        module,
        "m08.e01",
        "crude_exposure=1.191\nadjusted_exposure=0.382\nadjusted_age=0.123",
    )
    corrected = _correct_example_output(
        corrected,
        "m08.e02",
        "(Intercept),groupA,groupB,age\ngroupA=0.95\ngroupB=1.89",
    )
    extended = replace(
        corrected,
        objectives=corrected.objectives
        + (
            objective(
                "m08.bg.o1",
                (
                    "Recuperar un coeficiente ajustado mediante regresión parcial y explicar su límite causal.",
                    "Recover an adjusted coefficient through partial regression and explain its causal boundary.",
                    "Genskabe en justeret koefficient gennem partiel regression og forklare dens kausale grænse.",
                ),
            ),
        ),
        concepts=corrected.concepts
        + (
            concept(
                "partial-regression-and-adjusted-coefficients",
                (
                    "Regresión parcial y coeficientes ajustados",
                    "Partial regression and adjusted coefficients",
                    "Partiel regression og justerede koefficienter",
                ),
                (
                    "En el modelo Y~X+Z con intercepto, el coeficiente ajustado de X puede recuperarse en tres pasos: ajustar X~Z y conservar sus residuos, ajustar Y~Z y conservar sus residuos, y regresar los residuos de Y sobre los residuos de X. La pendiente resultante es idéntica al coeficiente de X en el modelo múltiple. Esta identidad convierte «mantener Z constante» en una operación algebraica: compara la parte de X no explicada linealmente por Z con la parte de Y no explicada linealmente por Z. Con varias covariables, ambas residualizaciones deben usar exactamente la misma matriz de covariables. Si Z explica casi toda la variación de X, queda poca señal residual y la pendiente puede ser inestable, lo que conecta la regresión parcial con la colinealidad. La identidad describe el modelo especificado; no demuestra que Z sea un conjunto suficiente de confusores ni convierte la asociación ajustada en causal.",
                    "In the model Y~X+Z with an intercept, the adjusted coefficient of X can be recovered in three steps: fit X~Z and retain its residuals, fit Y~Z and retain its residuals, then regress the Y residuals on the X residuals. The resulting slope is identical to the X coefficient in the multiple model. This identity turns 'holding Z fixed' into an algebraic operation: it compares the part of X not linearly explained by Z with the part of Y not linearly explained by Z. With several covariates, both residualisations must use exactly the same covariate design matrix. If Z explains almost all variation in X, little residual signal remains and the slope can be unstable, connecting partial regression with collinearity. The identity describes the specified model; it does not prove that Z is a sufficient confounder set or make the adjusted association causal.",
                    "I modellen Y~X+Z med en skæring kan den justerede koefficient for X genskabes i tre trin: tilpas X~Z og behold residualerne, tilpas Y~Z og behold residualerne, og regressér derefter Y-residualerne på X-residualerne. Den resulterende hældning er identisk med X-koefficienten i den multiple model. Identiteten gør 'hold Z fast' til en algebraisk operation: den sammenligner den del af X, som ikke forklares lineært af Z, med den del af Y, som ikke forklares lineært af Z. Med flere kovariater skal begge residualiseringer bruge præcis den samme kovariatdesignmatrix. Hvis Z forklarer næsten al variation i X, er der kun lidt residualt signal tilbage, og hældningen kan være ustabil, hvilket forbinder partiel regression med kollinearitet. Identiteten beskriver den specificerede model; den beviser ikke, at Z er et tilstrækkeligt confoundersæt, og gør ikke den justerede association kausal.",
                ),
                (
                    (
                        "Residualiza X e Y frente a las mismas covariables.",
                        "Residualise X and Y against the same covariates.",
                        "Residualisér X og Y mod de samme kovariater.",
                    ),
                    (
                        "La pendiente parcial coincide con el coeficiente ajustado.",
                        "The partial slope equals the adjusted coefficient.",
                        "Den partielle hældning er lig den justerede koefficient.",
                    ),
                    (
                        "Poca variación residual de X implica poca información independiente sobre su pendiente.",
                        "Little residual variation in X means little independent information about its slope.",
                        "Lille residual variation i X betyder lidt uafhængig information om hældningen.",
                    ),
                    (
                        "La equivalencia algebraica no garantiza control causal de confusión.",
                        "Algebraic equivalence does not guarantee causal confounding control.",
                        "Algebraisk ækvivalens garanterer ikke kausal kontrol af confounding.",
                    ),
                ),
            ),
        ),
        worked_examples=corrected.worked_examples
        + (
            example(
                "m08.bg.e01",
                (
                    "Recuperar una pendiente ajustada por residualización",
                    "Recover an adjusted slope by residualisation",
                    "Genskab en justeret hældning ved residualisering",
                ),
                (
                    "Comprueba que la pendiente de los residuos coincide con el coeficiente de exposición ajustado por edad.",
                    "Verify that the residual-on-residual slope equals the exposure coefficient adjusted for age.",
                    "Kontrollér, at residual-på-residual-hældningen er lig eksponeringskoefficienten justeret for alder.",
                ),
                (
                    (
                        "La exposición y la respuesta se residualizan por separado respecto de edad.",
                        "Exposure and response are residualised separately with respect to age.",
                        "Eksponering og respons residualiseres separat i forhold til alder.",
                    ),
                    (
                        "La regresión parcial usa exactamente las dos series residuales.",
                        "The partial regression uses exactly the two residual series.",
                        "Den partielle regression bruger præcis de to residualserier.",
                    ),
                    (
                        "La igualdad numérica verifica una identidad del modelo, no causalidad.",
                        "The numerical equality verifies a model identity, not causality.",
                        "Den numeriske lighed verificerer en modelidentitet, ikke kausalitet.",
                    ),
                ),
                """exposure <- c(1, 2, 2, 3, 4, 4, 5, 6)
age <- c(30, 34, 39, 42, 48, 53, 57, 62)
response <- c(5.2, 6.1, 6.8, 7.4, 8.8, 9.2, 10.1, 11.0)
adjusted <- lm(response ~ exposure + age)
exposure_residual <- residuals(lm(exposure ~ age))
response_residual <- residuals(lm(response ~ age))
partial <- lm(response_residual ~ exposure_residual)
cat(sprintf("adjusted=%.3f\n", coef(adjusted)[["exposure"]]))
cat(sprintf("partial=%.3f\n", coef(partial)[["exposure_residual"]]))
cat(sprintf("max_abs_exposure_residual=%.3f", max(abs(exposure_residual))))
""",
                """adjusted=0.382
partial=0.382
max_abs_exposure_residual=0.457""",
                (
                    "La pendiente parcial reproduce exactamente el coeficiente ajustado. La pequeña amplitud residual de exposición muestra que edad explica gran parte de su variación, por lo que la estimación usa una fracción limitada de información independiente.",
                    "The partial slope exactly reproduces the adjusted coefficient. The small residual exposure range shows that age explains much of its variation, so the estimate uses a limited amount of independent information.",
                    "Den partielle hældning genskaber præcis den justerede koefficient. Det lille residuale eksponeringsområde viser, at alder forklarer en stor del af variationen, så estimatet bruger en begrænset mængde uafhængig information.",
                ),
            ),
        ),
        practice_exercises=corrected.practice_exercises
        + (
            practice(
                "m08.bg.p01",
                ActivityType.DEBUGGING,
                (
                    "Para interpretar el coeficiente de X en Y~X+edad+sexo, un análisis residualiza X sólo por edad y residualiza Y por edad y sexo. Diagnostica el error y corrige el procedimiento.",
                    "To interpret the X coefficient in Y~X+age+sex, an analysis residualises X only on age but residualises Y on age and sex. Diagnose the error and correct the procedure.",
                    "For at fortolke X-koefficienten i Y~X+alder+køn residualiserer en analyse kun X mod alder, men Y mod alder og køn. Diagnosticér fejlen og ret proceduren.",
                ),
                (
                    (
                        "Compara las matrices de covariables usadas en ambos pasos.",
                        "Compare the covariate design matrices used in both steps.",
                        "Sammenlign kovariatdesignmatricerne i begge trin.",
                    ),
                    (
                        "La identidad parcial requiere el mismo conjunto de términos.",
                        "The partial-regression identity requires the same set of terms.",
                        "Identiteten for partiel regression kræver det samme sæt led.",
                    ),
                ),
                (
                    "El procedimiento no recupera el coeficiente del modelo objetivo porque las residualizaciones usan espacios de ajuste distintos. Debe ajustar X~edad+sexo y Y~edad+sexo con la misma codificación, conservar ambos residuos y ajustar residuo_Y~residuo_X. La pendiente resultante coincide con el coeficiente de X en Y~X+edad+sexo, siempre que los modelos incluyan el mismo intercepto y términos.",
                    "The procedure does not recover the target-model coefficient because the residualisations use different adjustment spaces. Fit X~age+sex and Y~age+sex with identical coding, retain both residuals, and fit residual_Y~residual_X. The resulting slope equals the X coefficient in Y~X+age+sex provided the models use the same intercept and terms.",
                    "Proceduren genskaber ikke koefficienten fra målmodellen, fordi residualiseringerne bruger forskellige justeringsrum. Tilpas X~alder+køn og Y~alder+køn med identisk kodning, behold begge residualer, og tilpas residual_Y~residual_X. Den resulterende hældning er lig X-koefficienten i Y~X+alder+køn, forudsat at modellerne bruger samme skæring og led.",
                ),
                (
                    "Regresión parcial exige residualizar ambas variables contra la misma matriz de covariables.",
                    "Partial regression requires residualising both variables against the same covariate matrix.",
                    "Partiel regression kræver residualisering af begge variable mod den samme kovariatmatrix.",
                ),
                "",
            ),
        ),
        assessment_items=corrected.assessment_items
        + (
            objective_mcq(
                "bmb830.m08.book.001",
                (
                    "¿Qué procedimiento recupera el coeficiente de X en Y~X+Z?",
                    "Which procedure recovers the X coefficient in Y~X+Z?",
                    "Hvilken procedure genskaber X-koefficienten i Y~X+Z?",
                ),
                (
                    (
                        "residualise_x_only",
                        (
                            "Residualizar sólo X respecto de Z y regresionar Y sobre ese residuo.",
                            "Residualise only X on Z and regress Y on that residual.",
                            "Residualisér kun X mod Z og regressér Y på denne residual.",
                        ),
                    ),
                    (
                        "residualise_both_same_z",
                        (
                            "Residualizar X e Y respecto del mismo Z y regresar un residuo sobre el otro.",
                            "Residualise X and Y on the same Z and regress one residual on the other.",
                            "Residualisér X og Y mod det samme Z og regressér den ene residual på den anden.",
                        ),
                    ),
                    (
                        "separate_simple_models",
                        (
                            "Ajustar por separado Y~X y Y~Z y promediar las pendientes.",
                            "Fit Y~X and Y~Z separately and average the slopes.",
                            "Tilpas Y~X og Y~Z separat og beregn gennemsnittet af hældningerne.",
                        ),
                    ),
                ),
                "residualise_both_same_z",
                (
                    "La identidad de regresión parcial usa los residuos de X y de Y frente al mismo conjunto de covariables.",
                    "The partial-regression identity uses residuals of both X and Y against the same covariate set.",
                    "Identiteten for partiel regression bruger residualerne af både X og Y mod det samme kovariatsæt.",
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


def apply_regression_review(module: LocalizedLearningModule) -> LocalizedLearningModule:
    """Apply the focused M07-M08 review to the matching module."""

    if module.module_id == "bmb830.m07":
        return _extend_simple_regression(module)
    if module.module_id == "bmb830.m08":
        return _extend_multiple_regression(module)
    return module
