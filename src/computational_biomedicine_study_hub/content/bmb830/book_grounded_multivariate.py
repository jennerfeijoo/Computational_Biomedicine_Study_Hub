"""Focused source-grounded extensions for BMB830 multivariate analysis."""

from __future__ import annotations

from dataclasses import replace

from ...learning.activity_types import ActivityType
from ..localized_models import LocalizedLearningModule, LocalizedTutorSupportPacket
from .authoring import concept, example, objective, objective_mcq, practice
from .book_grounded_audit import AcademicReference, ModuleSourceAudit

BMB830_MULTIVARIATE_SOURCES: tuple[AcademicReference, ...] = (
    AcademicReference(
        "murphy-2023-ch20",
        ("Kevin P. Murphy, Probabilistic Machine Learning: An Introduction (2023), chapter 20."),
        (
            "principal component analysis, covariance eigendecomposition, centring, "
            "linear dimensionality reduction, reconstruction, and effective dimension"
        ),
    ),
    AcademicReference(
        "islr-2021-ch06",
        (
            "Gareth James, Daniela Witten, Trevor Hastie, and Robert Tibshirani, "
            "An Introduction to Statistical Learning with Applications in R, 2nd ed. "
            "(2021), chapter 6."
        ),
        (
            "high-dimensional data, p greater than n, non-unique least squares, "
            "regularisation, dimension reduction, overfitting, and cross-validation"
        ),
    ),
    AcademicReference(
        "yachay-biostatistics-multivariate",
        (
            "Yachay Tech, Biostatistics syllabus and course material, introduction to "
            "multivariate analysis."
        ),
        (
            "biological hyperspaces, clustering, ordination, PCA from covariance and "
            "correlation matrices, multidimensional scaling, and partial least squares"
        ),
    ),
)


def _with_source_basis(
    module: LocalizedLearningModule,
    source_ids: tuple[str, ...],
) -> LocalizedLearningModule:
    tutor = module.tutor_support
    merged = tuple(dict.fromkeys((*tutor.source_basis, *source_ids)))
    updated_tutor: LocalizedTutorSupportPacket = replace(tutor, source_basis=merged)
    return replace(module, tutor_support=updated_tutor)


def update_multivariate_audit(
    audit: tuple[ModuleSourceAudit, ...],
) -> tuple[ModuleSourceAudit, ...]:
    """Mark M11-M12 reviewed after focused multivariate extensions."""

    updated: list[ModuleSourceAudit] = []
    for item in audit:
        if item.module_id == "bmb830.m11":
            updated.append(
                replace(
                    item,
                    source_ids=tuple(
                        dict.fromkeys(
                            (
                                *item.source_ids,
                                "murphy-2023-ch20",
                                "yachay-biostatistics-multivariate",
                            )
                        )
                    ),
                    source_scope=item.source_scope
                    + (
                        "covariance-matrix versus correlation-matrix PCA",
                        "scale-dependent loading and explained-variance interpretation",
                    ),
                    state="consistent",
                    finding=(
                        "Existing coverage of matrix orientation, preprocessing, PCA scores, "
                        "loadings, explained variance, sign indeterminacy, hierarchical "
                        "clustering, and sensitivity analysis is consistent. The explicit "
                        "relationship between unscaled covariance PCA and standardised "
                        "correlation PCA needed one operational treatment."
                    ),
                    implemented_change=(
                        "Added an original trilingual covariance-versus-correlation PCA "
                        "explanation, deterministic scale-sensitivity example, interpretation "
                        "exercise, and stable objective item."
                    ),
                )
            )
        elif item.module_id == "bmb830.m12":
            updated.append(
                replace(
                    item,
                    source_ids=tuple(
                        dict.fromkeys(
                            (
                                *item.source_ids,
                                "islr-2021-ch06",
                                "murphy-2023-ch20",
                            )
                        )
                    ),
                    source_scope=item.source_scope
                    + (
                        "rank ceilings in centred p-greater-than-n matrices",
                        "singular covariance and non-identifiable unregularised models",
                    ),
                    state="consistent",
                    finding=(
                        "Existing coverage of provenance, missingness, filtering, imputation, "
                        "log transformation, scaling, batch effects, training-only feature "
                        "selection, multiplicity, leakage, and external validation is strong. "
                        "The geometric rank ceiling that explains why many features do not "
                        "create additional independent sample directions needed one explicit "
                        "treatment."
                    ),
                    implemented_change=(
                        "Added an original trilingual rank-ceiling explanation, deterministic "
                        "p-greater-than-n PCA example, validation-boundary exercise, and stable "
                        "objective item."
                    ),
                )
            )
        else:
            updated.append(item)
    return tuple(updated)


def _extend_intro_multivariate(module: LocalizedLearningModule) -> LocalizedLearningModule:
    extended = replace(
        module,
        objectives=module.objectives
        + (
            objective(
                "m11.bg.o1",
                (
                    "Distinguir PCA basada en covarianza de PCA basada en correlación y justificar la elección desde las unidades y la pregunta biológica.",
                    "Distinguish covariance-based PCA from correlation-based PCA and justify the choice from measurement units and the biological question.",
                    "Skelne mellem kovariansbaseret og korrelationsbaseret PCA og begrunde valget ud fra måleenheder og det biologiske spørgsmål.",
                ),
            ),
        ),
        concepts=module.concepts
        + (
            concept(
                "covariance-vs-correlation-pca",
                (
                    "PCA de covarianza frente a PCA de correlación",
                    "Covariance PCA versus correlation PCA",
                    "Kovarians-PCA versus korrelations-PCA",
                ),
                (
                    "PCA sobre la matriz de covarianza centra las variables pero conserva sus escalas originales. Por ello, una variable con una varianza numérica mucho mayor puede dominar los primeros componentes. PCA sobre la matriz de correlación equivale a centrar y dividir cada variable por su desviación estándar antes del ajuste; cada variable no constante entra entonces con varianza uno. Ninguna opción es universalmente superior: la covarianza puede ser adecuada cuando las variables comparten unidades y la magnitud absoluta es científicamente relevante, mientras que la correlación puede ser preferible cuando las unidades o dispersiones no son comparables. Estandarizar cambia la geometría, los loadings y la varianza explicada; no es una corrección cosmética. Las variables con varianza cero deben retirarse o tratarse antes de estandarizar.",
                    "PCA on the covariance matrix centres variables but preserves their original scales. A variable with much larger numerical variance can therefore dominate the leading components. PCA on the correlation matrix is equivalent to centring and dividing each variable by its standard deviation before fitting, so every non-constant variable enters with variance one. Neither choice is universally superior: covariance PCA may be appropriate when variables share units and absolute magnitude is scientifically meaningful, whereas correlation PCA may be preferable when units or dispersions are not comparable. Standardisation changes the geometry, loadings, and explained variance; it is not a cosmetic correction. Zero-variance variables must be removed or otherwise handled before standardisation.",
                    "PCA på kovariansmatricen centrerer variablene, men bevarer deres oprindelige skalaer. En variabel med langt større numerisk varians kan derfor dominere de første komponenter. PCA på korrelationsmatricen svarer til at centrere og dividere hver variabel med dens standardafvigelse før tilpasning, så hver ikke-konstant variabel indgår med varians én. Ingen af mulighederne er universelt bedst: kovarians-PCA kan være passende, når variablene har samme enhed og absolut størrelse er videnskabeligt relevant, mens korrelations-PCA kan foretrækkes, når enheder eller spredninger ikke kan sammenlignes. Standardisering ændrer geometrien, loadings og forklaret varians; det er ikke en kosmetisk korrektion. Variable med nulvarians skal fjernes eller håndteres før standardisering.",
                ),
                (
                    (
                        "Covariance PCA corresponds to centre=TRUE and scale.=FALSE in prcomp.",
                        "Covariance PCA corresponds to centre=TRUE and scale.=FALSE in prcomp.",
                        "Kovarians-PCA svarer til centre=TRUE og scale.=FALSE i prcomp.",
                    ),
                    (
                        "Correlation PCA corresponds to centre=TRUE and scale.=TRUE for non-constant variables.",
                        "Correlation PCA corresponds to centre=TRUE and scale.=TRUE for non-constant variables.",
                        "Korrelations-PCA svarer til centre=TRUE og scale.=TRUE for ikke-konstante variable.",
                    ),
                    (
                        "Scaling changes the scientific weighting assigned to each variable.",
                        "Scaling changes the scientific weighting assigned to each variable.",
                        "Skalering ændrer den videnskabelige vægtning af hver variabel.",
                    ),
                    (
                        "Loadings from differently scaled analyses answer different questions.",
                        "Loadings from differently scaled analyses answer different questions.",
                        "Loadings fra forskelligt skalerede analyser besvarer forskellige spørgsmål.",
                    ),
                ),
            ),
        ),
        worked_examples=module.worked_examples
        + (
            example(
                "m11.bg.e01",
                (
                    "La escala modifica los loadings de PCA",
                    "Scale changes PCA loadings",
                    "Skala ændrer PCA-loadings",
                ),
                (
                    "Compara dos marcadores perfectamente correlacionados que difieren cien veces en escala.",
                    "Compare two perfectly correlated markers that differ one hundredfold in scale.",
                    "Sammenlign to perfekt korrelerede markører, der adskiller sig hundrede gange i skala.",
                ),
                (
                    (
                        "Los valores absolutos evitan depender del signo arbitrario del componente.",
                        "Absolute values avoid dependence on the arbitrary component sign.",
                        "Absolutte værdier undgår afhængighed af komponentens vilkårlige fortegn.",
                    ),
                    (
                        "El ajuste no escalado usa la covarianza; el escalado usa la correlación.",
                        "The unscaled fit uses covariance; the scaled fit uses correlation.",
                        "Den uskalerede tilpasning bruger kovarians; den skalerede bruger korrelation.",
                    ),
                ),
                """x <- data.frame(
  marker_small = c(-1, -1, 1, 1),
  marker_large = c(-100, -100, 100, 100)
)
covariance_fit <- prcomp(x, center = TRUE, scale. = FALSE)
correlation_fit <- prcomp(x, center = TRUE, scale. = TRUE)
cat(
  "covariance_abs_loadings=",
  paste(sprintf("%.3f", abs(covariance_fit$rotation[, 1])), collapse = ","),
  "\n",
  sep = ""
)
cat(
  "correlation_abs_loadings=",
  paste(sprintf("%.3f", abs(correlation_fit$rotation[, 1])), collapse = ","),
  sep = ""
)
""",
                """covariance_abs_loadings=0.010,1.000
correlation_abs_loadings=0.707,0.707""",
                (
                    "Sin escalar, el marcador de mayor varianza domina PC1. Tras estandarizar, ambos marcadores reciben la misma magnitud de loading porque contienen el mismo perfil relativo. Los dos resultados son algebraicamente válidos, pero responden a ponderaciones científicas distintas.",
                    "Without scaling, the higher-variance marker dominates PC1. After standardisation, both markers receive the same loading magnitude because they contain the same relative profile. Both results are algebraically valid, but they answer scientifically different weightings.",
                    "Uden skalering dominerer markøren med størst varians PC1. Efter standardisering får begge markører samme loading-størrelse, fordi de indeholder den samme relative profil. Begge resultater er algebraisk gyldige, men svarer til videnskabeligt forskellige vægtninger.",
                ),
            ),
        ),
        practice_exercises=module.practice_exercises
        + (
            practice(
                "m11.bg.p01",
                ActivityType.DATA_INTERPRETATION,
                (
                    "Un análisis combina concentraciones en ng/mL, porcentajes y una puntuación clínica. Decide entre PCA de covarianza y de correlación y especifica qué información debes revisar antes.",
                    "An analysis combines concentrations in ng/mL, percentages, and a clinical score. Choose covariance or correlation PCA and state what information must be reviewed first.",
                    "En analyse kombinerer koncentrationer i ng/mL, procentdele og en klinisk score. Vælg kovarians- eller korrelations-PCA og angiv, hvilke oplysninger der først skal gennemgås.",
                ),
                (
                    (
                        "Compara unidades, dispersión, calidad y significado de magnitud absoluta.",
                        "Compare units, spread, quality, and the meaning of absolute magnitude.",
                        "Sammenlign enheder, spredning, kvalitet og betydningen af absolut størrelse.",
                    ),
                    (
                        "No selecciones el método por la figura que separa mejor los grupos.",
                        "Do not choose the method from the plot that separates groups best.",
                        "Vælg ikke metoden ud fra det plot, der adskiller grupper bedst.",
                    ),
                ),
                (
                    "Las unidades no son comparables, por lo que PCA de correlación es un punto de partida defendible si cada variable debe recibir peso inicial comparable. Antes deben revisarse unidades, transformaciones, varianza cero, errores de medición, distribución y relevancia de la magnitud absoluta. Si la magnitud en unidades originales es parte de la pregunta, también debe ejecutarse un análisis de sensibilidad con PCA de covarianza.",
                    "The units are not comparable, so correlation PCA is a defensible starting point if each variable should receive comparable initial weight. First review units, transformations, zero variance, measurement error, distributions, and whether absolute magnitude is scientifically meaningful. If original-scale magnitude is part of the question, a covariance-PCA sensitivity analysis is also required.",
                    "Enhederne kan ikke sammenlignes, så korrelations-PCA er et forsvarligt udgangspunkt, hvis hver variabel skal have sammenlignelig startvægt. Gennemgå først enheder, transformationer, nulvarians, målefejl, fordelinger og om absolut størrelse er videnskabeligt meningsfuld. Hvis størrelse på original skala indgår i spørgsmålet, kræves også en følsomhedsanalyse med kovarians-PCA.",
                ),
                (
                    "La elección de escala define la geometría analítica.",
                    "The scale choice defines the analytical geometry.",
                    "Valget af skala definerer den analytiske geometri.",
                ),
            ),
        ),
        assessment_items=module.assessment_items
        + (
            objective_mcq(
                "bmb830.m11.book.001",
                (
                    "¿Qué operación convierte PCA de covarianza en PCA de correlación para variables no constantes?",
                    "What operation converts covariance PCA into correlation PCA for non-constant variables?",
                    "Hvilken operation omdanner kovarians-PCA til korrelations-PCA for ikke-konstante variable?",
                ),
                (
                    (
                        "centre_only",
                        ("Solo centrar", "Centre only", "Kun centrere"),
                    ),
                    (
                        "standardise",
                        (
                            "Centrar y dividir por la desviación estándar",
                            "Centre and divide by the standard deviation",
                            "Centrere og dividere med standardafvigelsen",
                        ),
                    ),
                    (
                        "rank_transform",
                        ("Transformar a rangos", "Replace by ranks", "Erstatte med rangordener"),
                    ),
                ),
                "standardise",
                (
                    "Estandarizar produce variables con varianza uno y equivale a usar su matriz de correlación.",
                    "Standardisation gives variables unit variance and is equivalent to using their correlation matrix.",
                    "Standardisering giver variablene varians én og svarer til at bruge deres korrelationsmatrix.",
                ),
            ),
        ),
    )
    return _with_source_basis(
        extended,
        (
            "sdu-bmb830-active-2025",
            "murphy-2023-ch20",
            "yachay-biostatistics-multivariate",
        ),
    )


def _extend_high_dimensional_case(module: LocalizedLearningModule) -> LocalizedLearningModule:
    extended = replace(
        module,
        objectives=module.objectives
        + (
            objective(
                "m12.bg.o1",
                (
                    "Explicar el límite de rango de una matriz centrada con p mayor que n y sus consecuencias para PCA y modelos no regularizados.",
                    "Explain the rank ceiling of a centred matrix with p greater than n and its consequences for PCA and unregularised models.",
                    "Forklare rangloftet for en centreret matrix med p større end n og konsekvenserne for PCA og uregulariserede modeller.",
                ),
            ),
        ),
        concepts=module.concepts
        + (
            concept(
                "rank-ceiling-and-p-greater-than-n",
                (
                    "Límite de rango cuando p es mayor que n",
                    "Rank ceiling when p exceeds n",
                    "Rangloft når p overstiger n",
                ),
                (
                    "Para una matriz X con n muestras y p características, centrar las columnas impone que sus filas sumen cero. Por ello, rango(X centrada) no puede exceder min(n-1,p). Si p es mayor que n, PCA puede producir como máximo n-1 componentes con varianza no nula y la matriz de covarianza de características es singular. Añadir miles de características no añade miles de unidades independientes. En regresión sin regularización, p igual o mayor que n permite soluciones no únicas y puede producir ajuste perfecto del entrenamiento sin capacidad de generalización. PCA, ridge, lasso u otras restricciones seleccionan una solución mediante supuestos adicionales; no crean información muestral y deben elegirse y evaluarse dentro del remuestreo, con una capa externa cuando se estima rendimiento.",
                    "For a matrix X with n samples and p features, column centring forces its rows to sum to zero. Therefore rank(centred X) cannot exceed min(n-1,p). When p exceeds n, PCA can have at most n-1 components with non-zero variance and the feature covariance matrix is singular. Adding thousands of features does not add thousands of independent units. In unregularised regression, p greater than or equal to n permits non-unique solutions and may produce perfect training fit without generalisation. PCA, ridge, lasso, and other constraints choose a solution through additional assumptions; they do not create sample information and must be selected and evaluated inside resampling, with an outer layer when performance is estimated.",
                    "For en matrix X med n prøver og p features medfører kolonnecentrering, at rækkerne summerer til nul. Derfor kan rang(centreret X) ikke overstige min(n-1,p). Når p overstiger n, kan PCA højst have n-1 komponenter med ikke-nul varians, og feature-kovariansmatricen er singulær. Tusindvis af ekstra features giver ikke tusindvis af uafhængige enheder. Ved uregulariseret regression tillader p større end eller lig n ikke-entydige løsninger og kan give perfekt træningstilpasning uden generalisering. PCA, ridge, lasso og andre begrænsninger vælger en løsning gennem yderligere antagelser; de skaber ikke stikprøveinformation og skal vælges og evalueres inde i resampling med et ydre lag, når præstation estimeres.",
                ),
                (
                    (
                        "After centring, the maximum number of non-zero PCs is min(n-1,p).",
                        "After centring, the maximum number of non-zero PCs is min(n-1,p).",
                        "Efter centrering er det maksimale antal ikke-nul PC'er min(n-1,p).",
                    ),
                    (
                        "A singular covariance matrix is expected rather than a software defect when p exceeds n.",
                        "A singular covariance matrix is expected rather than a software defect when p exceeds n.",
                        "En singulær kovariansmatrix er forventelig og ikke en softwarefejl, når p overstiger n.",
                    ),
                    (
                        "More features increase model-search opportunities, not independent sample size.",
                        "More features increase model-search opportunities, not independent sample size.",
                        "Flere features øger mulighederne for modelsøgning, ikke den uafhængige stikprøvestørrelse.",
                    ),
                    (
                        "Regularisation and dimension reduction add assumptions that require nested validation.",
                        "Regularisation and dimension reduction add assumptions that require nested validation.",
                        "Regularisering og dimensionsreduktion tilføjer antagelser, der kræver indlejret validering.",
                    ),
                ),
            ),
        ),
        worked_examples=module.worked_examples
        + (
            example(
                "m12.bg.e01",
                (
                    "Contar direcciones no nulas en una matriz p mayor que n",
                    "Count non-zero directions in a p-greater-than-n matrix",
                    "Tæl ikke-nul retninger i en matrix med p større end n",
                ),
                (
                    "Centra cuatro muestras con seis características dependientes y cuenta los componentes con varianza no nula.",
                    "Centre four samples with six dependent features and count components with non-zero variance.",
                    "Centrér fire prøver med seks afhængige features og tæl komponenter med ikke-nul varians.",
                ),
                (
                    (
                        "Con cuatro muestras, el límite tras centrar es tres.",
                        "With four samples, the post-centring ceiling is three.",
                        "Med fire prøver er loftet efter centrering tre.",
                    ),
                    (
                        "Las columnas adicionales son combinaciones de las tres primeras.",
                        "The additional columns are combinations of the first three.",
                        "De ekstra kolonner er kombinationer af de første tre.",
                    ),
                ),
                """x <- rbind(
  sample_1 = c(1, 0, 0, 1, 1, 0),
  sample_2 = c(0, 1, 0, 1, 0, 1),
  sample_3 = c(0, 0, 1, 0, 1, 1),
  sample_4 = c(1, 1, 1, 2, 2, 2)
)
fit <- prcomp(x, center = TRUE, scale. = FALSE)
nonzero <- sum(fit$sdev > 1e-10)
cat(sprintf("samples=%d\n", nrow(x)))
cat(sprintf("features=%d\n", ncol(x)))
cat(sprintf("rank_ceiling=%d\n", min(nrow(x) - 1, ncol(x))))
cat(sprintf("nonzero_pcs=%d", nonzero))
""",
                """samples=4
features=6
rank_ceiling=3
nonzero_pcs=3""",
                (
                    "Aunque existen seis columnas, cuatro muestras centradas sólo sostienen tres direcciones independientes. La coincidencia entre el límite teórico y los tres componentes no nulos muestra que la dimensionalidad algebraica está limitada por las muestras, no por el número bruto de proteínas.",
                    "Although there are six columns, four centred samples support only three independent directions. Agreement between the theoretical ceiling and the three non-zero components shows that algebraic dimension is limited by samples, not by the raw number of proteins.",
                    "Selv om der er seks kolonner, understøtter fire centrerede prøver kun tre uafhængige retninger. Overensstemmelsen mellem det teoretiske loft og de tre ikke-nul komponenter viser, at den algebraiske dimension begrænses af prøverne, ikke af det rå antal proteiner.",
                ),
            ),
        ),
        practice_exercises=module.practice_exercises
        + (
            practice(
                "m12.bg.p01",
                ActivityType.DATA_INTERPRETATION,
                (
                    "Un estudio tiene 40 pacientes y 10 000 proteínas. Indica el máximo de componentes principales no nulos tras centrar y explica por qué un ajuste perfecto del entrenamiento no demuestra capacidad predictiva.",
                    "A study has 40 patients and 10,000 proteins. State the maximum number of non-zero principal components after centring and explain why perfect training fit does not demonstrate predictive ability.",
                    "Et studie har 40 patienter og 10.000 proteiner. Angiv det maksimale antal ikke-nul hovedkomponenter efter centrering, og forklar hvorfor perfekt træningstilpasning ikke viser prædiktionsevne.",
                ),
                (
                    (
                        "Aplica min(n-1,p).",
                        "Apply min(n-1,p).",
                        "Anvend min(n-1,p).",
                    ),
                    (
                        "Separa ajuste, identificación de parámetros y error fuera de muestra.",
                        "Separate fit, parameter identification, and out-of-sample error.",
                        "Adskil tilpasning, parameteridentifikation og fejl uden for stikprøven.",
                    ),
                ),
                (
                    "El máximo es 39 componentes no nulos. Con muchas más características que pacientes, múltiples modelos pueden interpolar o ajustar casi perfectamente los datos observados. Ese ajuste no identifica una solución única ni estima el error en pacientes nuevos. Toda selección, regularización o reducción de dimensión debe aprenderse dentro de los folds de entrenamiento y evaluarse en datos reservados o externos.",
                    "The maximum is 39 non-zero components. With far more features than patients, multiple models can interpolate or nearly perfectly fit the observed data. That fit neither identifies a unique solution nor estimates error in new patients. Feature selection, regularisation, and dimension reduction must be learned inside training folds and evaluated on held-out or external data.",
                    "Maksimum er 39 ikke-nul komponenter. Med langt flere features end patienter kan flere modeller interpolere eller næsten perfekt tilpasse de observerede data. Denne tilpasning identificerer hverken en entydig løsning eller estimerer fejl hos nye patienter. Featureudvælgelse, regularisering og dimensionsreduktion skal læres i træningsfold og evalueres på reserverede eller eksterne data.",
                ),
                (
                    "La dimensionalidad observada no sustituye replicación biológica.",
                    "Observed dimensionality does not replace biological replication.",
                    "Observeret dimensionalitet erstatter ikke biologisk replikation.",
                ),
            ),
        ),
        assessment_items=module.assessment_items
        + (
            objective_mcq(
                "bmb830.m12.book.001",
                (
                    "Con n muestras y p>n características, ¿cuál es el máximo de componentes con varianza no nula después de centrar?",
                    "With n samples and p>n features, what is the maximum number of components with non-zero variance after centring?",
                    "Hvad er det maksimale antal komponenter med ikke-nul varians efter centrering ved n prøver og p>n features?",
                ),
                (
                    (
                        "p",
                        ("p", "p", "p"),
                    ),
                    (
                        "n",
                        ("n", "n", "n"),
                    ),
                    (
                        "n_minus_one",
                        ("n-1", "n-1", "n-1"),
                    ),
                ),
                "n_minus_one",
                (
                    "El centrado elimina una dirección y el rango no puede superar n-1.",
                    "Centring removes one direction and rank cannot exceed n-1.",
                    "Centrering fjerner én retning, og rangen kan ikke overstige n-1.",
                ),
            ),
        ),
    )
    return _with_source_basis(
        extended,
        (
            "sdu-bmb830-active-2025",
            "islr-2021-ch06",
            "murphy-2023-ch20",
        ),
    )


def apply_multivariate_review(module: LocalizedLearningModule) -> LocalizedLearningModule:
    """Apply the focused M11-M12 review to the matching module."""

    if module.module_id == "bmb830.m11":
        return _extend_intro_multivariate(module)
    if module.module_id == "bmb830.m12":
        return _extend_high_dimensional_case(module)
    return module
