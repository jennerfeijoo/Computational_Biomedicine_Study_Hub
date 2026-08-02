"""Focused source-grounded extensions for BMB830 hypothesis tests and group comparisons."""

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


def update_inference_audit(
    audit: tuple[ModuleSourceAudit, ...],
) -> tuple[ModuleSourceAudit, ...]:
    """Mark M05-M06 reviewed only after their focused extensions are present."""

    findings = {
        "bmb830.m05": (
            "Existing coverage of hypotheses, p-values, one- and two-sided decisions, type I "
            "and type II errors, power, minimum relevant effects, and effect-size reporting is "
            "consistent. Construction of a null distribution by design-respecting "
            "randomization required one explicit treatment."
        ),
        "bmb830.m06": (
            "Existing coverage of independent and paired designs, Welch procedures, ANOVA, "
            "rank-based alternatives, assumptions, and multiplicity boundaries is consistent. "
            "The ANOVA F ratio and the distinction between an omnibus test and planned "
            "contrasts required one executable treatment."
        ),
    }
    changes = {
        "bmb830.m05": (
            "Added an original trilingual randomization-test explanation, exhaustive null "
            "example, design-diagnostic exercise, and stable objective item."
        ),
        "bmb830.m06": (
            "Added an original trilingual ANOVA decomposition explanation, deterministic global "
            "test example, interpretation exercise, and stable objective item."
        ),
    }

    updated: list[ModuleSourceAudit] = []
    for item in audit:
        if item.module_id == "bmb830.m05":
            updated.append(
                replace(
                    item,
                    state="consistent",
                    finding=findings[item.module_id],
                    implemented_change=changes[item.module_id],
                )
            )
        elif item.module_id == "bmb830.m06":
            updated.append(
                replace(
                    item,
                    source_ids=tuple(
                        dict.fromkeys((*item.source_ids, "yachay-biostatistics-linear-models"))
                    ),
                    source_scope=item.source_scope
                    + (
                        "between-group and within-group variation",
                        "omnibus hypotheses and planned contrasts",
                    ),
                    state="consistent",
                    finding=findings[item.module_id],
                    implemented_change=changes[item.module_id],
                )
            )
        else:
            updated.append(item)
    return tuple(updated)


def _extend_hypothesis_testing(module: LocalizedLearningModule) -> LocalizedLearningModule:
    extended = replace(
        module,
        objectives=module.objectives
        + (
            objective(
                "m05.bg.o1",
                (
                    "Construir una distribución nula por aleatorización respetando la unidad y las restricciones del diseño.",
                    "Construct a randomization null distribution while preserving the design unit and its restrictions.",
                    "Konstruere en randomiseringsnulfordeling, der bevarer designenheden og dens begrænsninger.",
                ),
            ),
        ),
        concepts=module.concepts
        + (
            concept(
                "randomization-tests-and-exchangeability",
                (
                    "Pruebas de aleatorización e intercambiabilidad",
                    "Randomization tests and exchangeability",
                    "Randomiseringstest og udskiftelighed",
                ),
                (
                    "Una prueba de aleatorización genera resultados compatibles con la hipótesis nula reasignando etiquetas únicamente de formas permitidas por el diseño. En grupos independientes se conservan los tamaños de grupo y se permutan las etiquetas entre unidades intercambiables. En datos pareados se intercambian las condiciones dentro de cada par, y en diseños por conglomerados se reasignan conglomerados completos. Para cada reasignación se recalcula el mismo estadístico; el valor p bilateral es la proporción de estadísticas nulas al menos tan extremas en valor absoluto como la observada. Una mezcla arbitraria de filas puede destruir dependencia, bloqueo o pareamiento y producir una distribución nula inválida. En una enumeración exhaustiva se incluyen todas las asignaciones permitidas; con simulación Monte Carlo conviene incluir la asignación observada y usar una corrección coherente como (extremos+1)/(B+1).",
                    "A randomization test generates outcomes compatible with the null hypothesis by reassigning labels only in ways allowed by the design. For independent groups, group sizes are retained and labels are permuted across exchangeable units. For paired data, conditions are swapped within each pair, and cluster designs reassign whole clusters. The same statistic is recalculated for every reassignment; a two-sided p-value is the proportion of null statistics at least as extreme in absolute value as the observed statistic. Arbitrarily shuffling rows can destroy dependence, blocking, or pairing and produce an invalid null distribution. Exhaustive enumeration includes every permitted assignment; Monte Carlo sampling should include the observed assignment and use a coherent correction such as (extreme+1)/(B+1).",
                    "En randomiseringstest genererer resultater, der er forenelige med nulhypotesen, ved kun at omfordele etiketter på måder, som designet tillader. For uafhængige grupper bevares gruppestørrelserne, og etiketter permuteres mellem udskiftelige enheder. For parrede data byttes betingelser inden for hvert par, og i klyngedesign omfordeles hele klynger. Den samme statistik genberegnes for hver omfordeling; en tosidet p-værdi er andelen af nulstatistikker, der i absolut værdi er mindst lige så ekstreme som den observerede. Vilkårlig blanding af rækker kan ødelægge afhængighed, blokering eller parring og give en ugyldig nulfordeling. Fuld enumeration omfatter alle tilladte tildelinger; Monte Carlo-sampling bør medtage den observerede tildeling og anvende en konsistent korrektion som (ekstreme+1)/(B+1).",
                ),
                (
                    (
                        "La intercambiabilidad depende de la hipótesis nula y del diseño.",
                        "Exchangeability depends on the null hypothesis and the design.",
                        "Udskiftelighed afhænger af nulhypotesen og designet.",
                    ),
                    (
                        "El tamaño de cada grupo se conserva al permutar etiquetas independientes.",
                        "Each group size is preserved when independent labels are permuted.",
                        "Hver gruppestørrelse bevares, når uafhængige etiketter permuteres.",
                    ),
                    (
                        "El pareamiento exige reasignaciones dentro de cada par.",
                        "Pairing requires reassignment within each pair.",
                        "Parring kræver omfordeling inden for hvert par.",
                    ),
                    (
                        "El estadístico observado y los estadísticos nulos deben calcularse de la misma forma.",
                        "The observed and null statistics must be calculated in the same way.",
                        "Den observerede statistik og nulstatistikkerne skal beregnes på samme måde.",
                    ),
                ),
            ),
        ),
        worked_examples=module.worked_examples
        + (
            example(
                "m05.bg.e01",
                (
                    "Enumerar una distribución nula de dos grupos",
                    "Enumerate a two-group null distribution",
                    "Enumerér en nulfordeling for to grupper",
                ),
                (
                    "Enumera las veinte asignaciones posibles de seis unidades a dos grupos de tres y calcula un valor p bilateral para la diferencia de medias.",
                    "Enumerate all twenty assignments of six units to two groups of three and calculate a two-sided p-value for the mean difference.",
                    "Enumerér alle tyve tildelinger af seks enheder til to grupper på tre og beregn en tosidet p-værdi for middelforskellen.",
                ),
                (
                    (
                        "La asignación observada usa las tres primeras unidades como grupo A.",
                        "The observed assignment uses the first three units as group A.",
                        "Den observerede tildeling bruger de første tre enheder som gruppe A.",
                    ),
                    (
                        "Cada columna de combn conserva exactamente tres unidades en A.",
                        "Each combn column retains exactly three units in A.",
                        "Hver combn-kolonne bevarer præcis tre enheder i A.",
                    ),
                    (
                        "La comparación bilateral usa el valor absoluto de la diferencia.",
                        "The two-sided comparison uses the absolute difference.",
                        "Den tosidede sammenligning bruger den absolutte forskel.",
                    ),
                ),
                """values <- c(2, 3, 4, 6, 7, 9)
observed_a <- 1:3
observed <- mean(values[-observed_a]) - mean(values[observed_a])
assignments <- combn(seq_along(values), 3)
null_statistics <- apply(assignments, 2, function(index_a) {
  mean(values[-index_a]) - mean(values[index_a])
})
p_value <- mean(abs(null_statistics) >= abs(observed))
cat(sprintf("observed=%.2f\n", observed))
cat(sprintf("assignments=%d\n", ncol(assignments)))
cat(sprintf("p=%.3f", p_value))
""",
                """observed=4.33
assignments=20
p=0.100""",
                (
                    "Sólo dos de las veinte asignaciones producen una diferencia absoluta al menos tan grande como la observada. La conclusión sigue condicionada a que las seis unidades sean intercambiables bajo la nulidad.",
                    "Only two of the twenty assignments produce an absolute difference at least as large as observed. The conclusion remains conditional on the six units being exchangeable under the null.",
                    "Kun to af de tyve tildelinger giver en absolut forskel, der er mindst lige så stor som den observerede. Konklusionen er fortsat betinget af, at de seks enheder er udskiftelige under nulhypotesen.",
                ),
            ),
        ),
        practice_exercises=module.practice_exercises
        + (
            practice(
                "m05.bg.p01",
                ActivityType.DEBUGGING,
                (
                    "Un estudio mide antes y después a cada paciente, pero el análisis permuta libremente las doce filas como si fueran independientes. Diagnostica el error y especifica una reasignación válida.",
                    "A study measures each patient before and after, but the analysis freely permutes all twelve rows as if they were independent. Diagnose the error and specify a valid reassignment.",
                    "Et studie måler hver patient før og efter, men analysen permuterer frit alle tolv rækker, som om de var uafhængige. Diagnosticér fejlen og angiv en gyldig omfordeling.",
                ),
                (
                    (
                        "La unidad independiente es el paciente, no la fila.",
                        "The independent unit is the patient, not the row.",
                        "Den uafhængige enhed er patienten, ikke rækken.",
                    ),
                    (
                        "Conserva las dos observaciones de cada paciente juntas.",
                        "Keep both observations from each patient together.",
                        "Hold begge observationer fra hver patient sammen.",
                    ),
                ),
                (
                    "La permutación libre rompe el pareamiento y crea asignaciones imposibles. Bajo una nulidad de ausencia de efecto dentro de paciente, se intercambian las etiquetas antes/después dentro de cada paciente o, de forma equivalente para una diferencia simétrica, se cambia aleatoriamente el signo de cada diferencia completa.",
                    "Free permutation breaks pairing and creates impossible assignments. Under a null of no within-patient effect, swap before/after labels within each patient or, equivalently for a symmetric difference statistic, randomly flip the sign of each complete difference.",
                    "Fri permutation bryder parringen og skaber umulige tildelinger. Under en nulhypotese om ingen effekt inden for patienten byttes før/efter-etiketter inden for hver patient, eller fortegnet på hver komplet forskel vendes tilfældigt for en symmetrisk differensstatistik.",
                ),
                (
                    "Una corrección válida preserva la estructura de dependencia que produjo los datos.",
                    "A valid correction preserves the dependence structure that generated the data.",
                    "En gyldig korrektion bevarer den afhængighedsstruktur, der genererede dataene.",
                ),
                "",
            ),
        ),
        assessment_items=module.assessment_items
        + (
            objective_mcq(
                "bmb830.m05.book.001",
                (
                    "¿Qué reasignación construye una distribución nula válida para un diseño antes-después?",
                    "Which reassignment constructs a valid null distribution for a before-after design?",
                    "Hvilken omfordeling konstruerer en gyldig nulfordeling for et før-efter-design?",
                ),
                (
                    (
                        "shuffle_all_rows",
                        (
                            "Mezclar todas las filas sin conservar pacientes.",
                            "Shuffle every row without preserving patients.",
                            "Bland alle rækker uden at bevare patienter.",
                        ),
                    ),
                    (
                        "swap_within_patient",
                        (
                            "Intercambiar las etiquetas dentro de cada paciente.",
                            "Swap labels within each patient.",
                            "Byt etiketter inden for hver patient.",
                        ),
                    ),
                    (
                        "resample_measurements",
                        (
                            "Remuestrear mediciones individuales como si fueran independientes.",
                            "Resample individual measurements as if independent.",
                            "Genudtag individuelle målinger, som om de var uafhængige.",
                        ),
                    ),
                ),
                "swap_within_patient",
                (
                    "La reasignación debe conservar la unidad independiente y el pareamiento del diseño.",
                    "Reassignment must preserve the independent unit and the design pairing.",
                    "Omfordelingen skal bevare den uafhængige enhed og designets parring.",
                ),
            ),
        ),
    )
    return _with_source_basis(
        extended,
        (
            "sdu-bmb830-active-2025",
            "ims-2024-probability-inference",
            "yachay-biostatistics-linear-models",
        ),
    )


def _extend_group_comparison(module: LocalizedLearningModule) -> LocalizedLearningModule:
    extended = replace(
        module,
        objectives=module.objectives
        + (
            objective(
                "m06.bg.o1",
                (
                    "Descomponer la variación de un ANOVA y separar la hipótesis global de los contrastes específicos.",
                    "Decompose ANOVA variation and separate the global hypothesis from specific contrasts.",
                    "Opdele variationen i en ANOVA og adskille den globale hypotese fra specifikke kontraster.",
                ),
            ),
        ),
        concepts=module.concepts
        + (
            concept(
                "anova-global-test-and-planned-contrasts",
                (
                    "Prueba global ANOVA y contrastes planificados",
                    "ANOVA global test and planned contrasts",
                    "Global ANOVA-test og planlagte kontraster",
                ),
                (
                    "En ANOVA de un factor compara la variación entre medias de grupo con la variación residual dentro de los grupos. El estadístico F es el cociente entre el cuadrado medio entre grupos y el cuadrado medio residual. La hipótesis nula global afirma que todas las medias poblacionales son iguales; rechazarla sólo establece que al menos una difiere y no identifica cuál. Un contraste planificado traduce una comparación científica preespecificada a una combinación de medias, mientras que una búsqueda exploratoria de muchas parejas forma una familia de pruebas y requiere control de multiplicidad. La independencia es esencial; la normalidad aproximada y la homogeneidad de varianzas condicionan el ANOVA clásico. Con tamaños desiguales y heterocedasticidad importante debe considerarse ANOVA de Welch u otro modelo compatible con el diseño.",
                    "A one-way ANOVA compares variation among group means with residual variation within groups. The F-statistic is the ratio of the between-group mean square to the residual mean square. The global null states that all population means are equal; rejecting it establishes only that at least one differs and does not identify which one. A planned contrast translates a prespecified scientific comparison into a combination of means, whereas an exploratory search over many pairs creates a family of tests and requires multiplicity control. Independence is essential; approximate normality and homogeneous variances condition classical ANOVA. With unequal sample sizes and important heteroscedasticity, Welch's ANOVA or another design-compatible model should be considered.",
                    "En en-faktor-ANOVA sammenligner variationen mellem gruppemiddelværdier med residualvariationen inden for grupper. F-statistikken er forholdet mellem middelkvadratet mellem grupper og det residuale middelkvadrat. Den globale nulhypotese siger, at alle populationsmiddelværdier er ens; forkastelse viser kun, at mindst én afviger, og identificerer ikke hvilken. En planlagt kontrast omsætter en foruddefineret videnskabelig sammenligning til en kombination af middelværdier, mens en eksplorativ søgning blandt mange par danner en familie af test og kræver kontrol for multiplicitet. Uafhængighed er afgørende; tilnærmet normalitet og homogene varianser er betingelser for klassisk ANOVA. Ved ulige stikprøvestørrelser og vigtig heteroskedasticitet bør Welchs ANOVA eller en anden designkompatibel model overvejes.",
                ),
                (
                    (
                        "F compara señal entre grupos con variación residual dentro de grupos.",
                        "F compares between-group signal with within-group residual variation.",
                        "F sammenligner signal mellem grupper med residualvariation inden for grupper.",
                    ),
                    (
                        "Una prueba global significativa no implica que todas las parejas difieran.",
                        "A significant global test does not imply that every pair differs.",
                        "En signifikant global test betyder ikke, at alle par er forskellige.",
                    ),
                    (
                        "Los contrastes planificados deben derivarse de la pregunta científica.",
                        "Planned contrasts should follow from the scientific question.",
                        "Planlagte kontraster bør følge af det videnskabelige spørgsmål.",
                    ),
                    (
                        "Las comparaciones exploratorias múltiples requieren un control explícito del error.",
                        "Multiple exploratory comparisons require explicit error control.",
                        "Flere eksplorative sammenligninger kræver eksplicit fejlkontrol.",
                    ),
                ),
            ),
        ),
        worked_examples=module.worked_examples
        + (
            example(
                "m06.bg.e01",
                (
                    "Descomponer un ANOVA de tres grupos",
                    "Decompose a three-group ANOVA",
                    "Opdel en ANOVA med tre grupper",
                ),
                (
                    "Calcula manualmente la razón F para tres grupos equilibrados y reporta además el contraste planificado C menos A.",
                    "Manually calculate the F ratio for three balanced groups and also report the planned C-minus-A contrast.",
                    "Beregn F-forholdet manuelt for tre balancerede grupper og rapportér også den planlagte kontrast C minus A.",
                ),
                (
                    (
                        "Las medias de grupo son 5, 6 y 9.",
                        "The group means are 5, 6, and 9.",
                        "Gruppemiddelværdierne er 5, 6 og 9.",
                    ),
                    (
                        "La suma entre grupos usa la distancia de cada media a la media global.",
                        "The between-group sum uses each mean's distance from the grand mean.",
                        "Summen mellem grupper bruger hver middelværdis afstand fra totalmiddelværdien.",
                    ),
                    (
                        "El contraste C-A responde una pregunta distinta de la prueba global.",
                        "The C-minus-A contrast answers a different question from the global test.",
                        "Kontrasten C minus A besvarer et andet spørgsmål end den globale test.",
                    ),
                ),
                """response <- c(4, 5, 6, 5, 6, 7, 8, 9, 10)
group <- factor(rep(c("A", "B", "C"), each = 3))
group_means <- tapply(response, group, mean)
grand_mean <- mean(response)
n_by_group <- table(group)
ss_between <- sum(n_by_group * (group_means - grand_mean)^2)
ss_within <- sum((response - group_means[as.character(group)])^2)
df_between <- nlevels(group) - 1
df_within <- length(response) - nlevels(group)
f_statistic <- (ss_between / df_between) / (ss_within / df_within)
p_value <- pf(f_statistic, df_between, df_within, lower.tail = FALSE)
contrast <- unname(group_means["C"] - group_means["A"])
cat(sprintf("F=%.2f\n", f_statistic))
cat(sprintf("p=%.4f\n", p_value))
cat(sprintf("C_minus_A=%.2f", contrast))
""",
                """F=13.00
p=0.0066
C_minus_A=4.00""",
                (
                    "La razón F grande indica que la separación entre medias supera la variación residual esperada bajo la nulidad. El contraste de cuatro unidades cuantifica C-A, pero su inferencia debe respetar si fue planificado o seleccionado tras explorar los datos.",
                    "The large F ratio indicates that separation among means exceeds residual variation expected under the null. The four-unit contrast quantifies C minus A, but its inference must reflect whether it was planned or selected after inspecting the data.",
                    "Det store F-forhold viser, at adskillelsen mellem middelværdier overstiger den residualvariation, der forventes under nulhypotesen. Kontrasten på fire enheder kvantificerer C minus A, men inferensen skal afspejle, om den var planlagt eller valgt efter inspektion af data.",
                ),
            ),
        ),
        practice_exercises=module.practice_exercises
        + (
            practice(
                "m06.bg.p01",
                ActivityType.DATA_INTERPRETATION,
                (
                    "Un ANOVA de cuatro tratamientos produce p=0,01. Evalúa la afirmación: «todos los tratamientos difieren entre sí» y especifica el siguiente análisis válido.",
                    "A four-treatment ANOVA gives p=0.01. Evaluate the statement 'all treatments differ from each other' and specify a valid next analysis.",
                    "En ANOVA med fire behandlinger giver p=0,01. Vurdér udsagnet 'alle behandlinger adskiller sig fra hinanden', og angiv en gyldig næste analyse.",
                ),
                (
                    (
                        "La alternativa global sólo exige una diferencia.",
                        "The global alternative requires only one difference.",
                        "Det globale alternativ kræver kun én forskel.",
                    ),
                    (
                        "Distingue contrastes planificados de búsqueda post hoc.",
                        "Distinguish planned contrasts from post-hoc searching.",
                        "Skeln mellem planlagte kontraster og post hoc-søgning.",
                    ),
                ),
                (
                    "La afirmación es inválida: el resultado global indica que al menos una media difiere. El siguiente paso es estimar los contrastes científicos preespecificados con intervalos; si se inspeccionan todas las parejas después del ANOVA, debe aplicarse un procedimiento que controle la familia de comparaciones y reportar estimaciones ajustadas, no sólo decisiones binarias.",
                    "The statement is invalid: the global result indicates that at least one mean differs. Next estimate prespecified scientific contrasts with intervals; if every pair is inspected after ANOVA, apply a procedure that controls the comparison family and report adjusted estimates rather than binary decisions alone.",
                    "Udsagnet er ugyldigt: det globale resultat viser, at mindst én middelværdi afviger. Estimér derefter foruddefinerede videnskabelige kontraster med intervaller; hvis alle par undersøges efter ANOVA, skal en procedure kontrollere sammenligningsfamilien, og justerede estimater bør rapporteres frem for kun binære beslutninger.",
                ),
                (
                    "Una interpretación completa separa la conclusión global, la magnitud de cada contraste y el control de multiplicidad.",
                    "A complete interpretation separates the global conclusion, each contrast magnitude, and multiplicity control.",
                    "En fuldstændig fortolkning adskiller den globale konklusion, størrelsen af hver kontrast og kontrol for multiplicitet.",
                ),
                "",
            ),
        ),
        assessment_items=module.assessment_items
        + (
            objective_mcq(
                "bmb830.m06.book.001",
                (
                    "¿Qué concluye directamente una prueba F global significativa en un ANOVA de un factor?",
                    "What does a significant global F-test directly establish in a one-way ANOVA?",
                    "Hvad fastslår en signifikant global F-test direkte i en en-faktor-ANOVA?",
                ),
                (
                    (
                        "all_pairs_differ",
                        (
                            "Todas las parejas de medias difieren.",
                            "Every pair of means differs.",
                            "Alle par af middelværdier er forskellige.",
                        ),
                    ),
                    (
                        "at_least_one_differs",
                        (
                            "Al menos una media poblacional difiere de otra.",
                            "At least one population mean differs from another.",
                            "Mindst én populationsmiddelværdi afviger fra en anden.",
                        ),
                    ),
                    (
                        "largest_group_causes_result",
                        (
                            "El grupo con mayor media causa necesariamente el resultado.",
                            "The group with the largest mean necessarily causes the result.",
                            "Gruppen med den største middelværdi forårsager nødvendigvis resultatet.",
                        ),
                    ),
                ),
                "at_least_one_differs",
                (
                    "La hipótesis alternativa global no identifica pares concretos ni afirma que todos difieran.",
                    "The global alternative identifies no specific pair and does not state that all pairs differ.",
                    "Det globale alternativ identificerer intet bestemt par og siger ikke, at alle par er forskellige.",
                ),
            ),
        ),
    )
    return _with_source_basis(
        extended,
        (
            "sdu-bmb830-active-2025",
            "ims-2024-probability-inference",
            "yachay-biostatistics-linear-models",
        ),
    )


def apply_inference_review(module: LocalizedLearningModule) -> LocalizedLearningModule:
    """Apply the focused M05-M06 review extension to one localized module."""

    if module.module_id == "bmb830.m05":
        return _extend_hypothesis_testing(module)
    if module.module_id == "bmb830.m06":
        return _extend_group_comparison(module)
    raise ValueError(f"Unsupported inference-review module: {module.module_id}")


__all__ = ["apply_inference_review", "update_inference_audit"]
