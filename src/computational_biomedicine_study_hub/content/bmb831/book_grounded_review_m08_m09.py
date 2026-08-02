"""Focused source-grounded review extensions for BMB831 modules 8 and 9."""

from __future__ import annotations

from dataclasses import replace

from ...learning.activity_types import ActivityType
from ..localized_models import LocalizedLearningModule
from .authoring import concept, example, objective, objective_mcq, practice
from .book_grounded_audit import ModuleSourceAudit


def review_interpretation_report_audit(
    audits: tuple[ModuleSourceAudit, ...],
) -> tuple[ModuleSourceAudit, ...]:
    """Mark the completed M08-M09 reviews while preserving the source registry."""

    updated: list[ModuleSourceAudit] = []
    for audit in audits:
        if audit.module_id == "bmb831.m08":
            updated.append(
                replace(
                    audit,
                    state="consistent",
                    finding=(
                        "Existing identifier mapping, tested universes, ORA and ranked methods, "
                        "redundancy, networks, circularity, and evidence boundaries are consistent. "
                        "The focused review identified one missing ontology boundary: annotation "
                        "propagation through parent-child relations makes related terms dependent "
                        "and prevents parent and child hits from being counted as independent "
                        "biological confirmations."
                    ),
                    implemented_change=(
                        "Added a trilingual ontology-propagation explanation, a deterministic "
                        "ancestor-propagation example, an interpretation exercise, and a stable "
                        "objective assessment item."
                    ),
                )
            )
        elif audit.module_id == "bmb831.m09":
            updated.append(
                replace(
                    audit,
                    state="consistent",
                    finding=(
                        "Existing estimand reconstruction, claim traceability, validity appraisal, "
                        "reproducibility, and English-report structure are consistent. The focused "
                        "review identified one missing reporting boundary: conclusions should be "
                        "evaluated across defensible analysis specifications, and selective "
                        "reporting of one favourable model must not be presented as robustness."
                    ),
                    implemented_change=(
                        "Added a trilingual specification-sensitivity explanation, a deterministic "
                        "multi-specification example, a publication-appraisal exercise, and a "
                        "stable objective assessment item."
                    ),
                )
            )
        else:
            updated.append(audit)
    return tuple(updated)


def _extend_ontology_propagation(
    module: LocalizedLearningModule,
) -> LocalizedLearningModule:
    return replace(
        module,
        objectives=module.objectives
        + (
            objective(
                "m08.bg.o1",
                (
                    "Interpretar propagación de anotaciones en ontologías y evitar contar términos relacionados como confirmaciones independientes.",
                    "Interpret annotation propagation in ontologies and avoid counting related terms as independent confirmations.",
                    "Fortolke annotationspropagering i ontologier og undgå at tælle relaterede termer som uafhængige bekræftelser.",
                ),
            ),
        ),
        concepts=module.concepts
        + (
            concept(
                "ontology-propagation-and-term-dependence",
                (
                    "Propagación ontológica y dependencia entre términos",
                    "Ontology propagation and dependence among terms",
                    "Ontologipropagering og afhængighed mellem termer",
                ),
                (
                    "En ontología jerárquica, una anotación a un término específico suele implicar anotación a sus ancestros mediante relaciones compatibles. Esta propagación mejora cobertura semántica, pero hace que términos padre e hijo compartan genes por construcción. Sus pruebas de enriquecimiento no son independientes y varios términos significativos pueden representar una sola señal anotativa. El ajuste de multiplicidad controla una familia de decisiones bajo un procedimiento definido, pero no elimina dependencia, herencia ni redundancia semántica. Deben conservarse versión de ontología, relaciones utilizadas, códigos de evidencia, anotaciones directas y propagadas, y genes conductores. Resumir términos requiere una regla reproducible y no convierte términos relacionados en replicaciones biológicas.",
                    "In a hierarchical ontology, an annotation to a specific term commonly implies annotation to compatible ancestors. This propagation improves semantic coverage but makes parent and child terms share genes by construction. Their enrichment tests are not independent, and several significant terms may represent one annotation signal. Multiplicity adjustment controls a family of decisions under a defined procedure but does not remove dependence, inheritance, or semantic redundancy. Retain ontology version, relations used, evidence codes, direct and propagated annotations, and driver genes. Term summarization requires a reproducible rule and does not turn related terms into biological replications.",
                    "I en hierarkisk ontologi indebærer en annotation til en specifik term normalt annotation til kompatible forfædre. Denne propagering forbedrer semantisk dækning, men gør, at forældre- og barnetermer deler gener ved konstruktion. Deres enrichment-tests er ikke uafhængige, og flere signifikante termer kan repræsentere ét annotationssignal. Multiplicitetsjustering kontrollerer en familie af beslutninger under en defineret procedure, men fjerner ikke afhængighed, arv eller semantisk redundans. Bevar ontologiversion, anvendte relationer, evidenskoder, direkte og propagerede annotationer samt drivende gener. Termsammenfatning kræver en reproducerbar regel og gør ikke relaterede termer til biologiske replikationer.",
                ),
                (
                    (
                        "Las anotaciones específicas pueden heredarse hacia términos ancestros.",
                        "Specific annotations may propagate to ancestor terms.",
                        "Specifikke annotationer kan propageres til forfædretermer.",
                    ),
                    (
                        "Padres e hijos comparten genes por estructura ontológica, no por validación independiente.",
                        "Parents and children share genes through ontology structure, not independent validation.",
                        "Forældre og børn deler gener gennem ontologistruktur, ikke uafhængig validering.",
                    ),
                    (
                        "FDR no elimina dependencia ni redundancia semántica.",
                        "FDR does not remove dependence or semantic redundancy.",
                        "FDR fjerner ikke afhængighed eller semantisk redundans.",
                    ),
                    (
                        "Versión, relaciones, evidencia y genes conductores deben permanecer trazables.",
                        "Version, relations, evidence, and driver genes must remain traceable.",
                        "Version, relationer, evidens og drivende gener skal forblive sporbare.",
                    ),
                ),
            ),
        ),
        worked_examples=module.worked_examples
        + (
            example(
                "m08.bg.e01",
                (
                    "Propagar anotaciones hacia un término padre",
                    "Propagate annotations to a parent term",
                    "Propagér annotationer til en forældreterm",
                ),
                (
                    "Construye anotaciones directas y propagadas para dos términos hijos que comparten un ancestro.",
                    "Construct direct and propagated annotations for two child terms sharing one ancestor.",
                    "Konstruér direkte og propagerede annotationer for to barnetermer med en fælles forfader.",
                ),
                (
                    (
                        "Cada gen tiene una anotación directa a un término hijo.",
                        "Each gene has one direct annotation to a child term.",
                        "Hvert gen har én direkte annotation til en barneterm.",
                    ),
                    (
                        "Cada anotación hija se propaga al término padre.",
                        "Each child annotation propagates to the parent term.",
                        "Hver barneannotation propageres til forældretermen.",
                    ),
                    (
                        "El recuento propagado no representa observaciones biológicas adicionales.",
                        "The propagated count does not represent additional biological observations.",
                        "Det propagerede antal repræsenterer ikke yderligere biologiske observationer.",
                    ),
                ),
                """direct <- data.frame(
  gene = c("G1", "G2", "G3"),
  term = c("child_A", "child_A", "child_B"),
  stringsAsFactors = FALSE
)
parent_map <- c(child_A = "parent", child_B = "parent")
propagated <- rbind(
  direct,
  data.frame(
    gene = direct$gene,
    term = unname(parent_map[direct$term]),
    stringsAsFactors = FALSE
  )
)
cat("direct_annotations=", nrow(direct), "\n", sep = "")
cat("propagated_annotations=", nrow(propagated), "\n", sep = "")
cat("parent_genes=", length(unique(propagated$gene[propagated$term == "parent"])), "\n", sep = "")
cat("child_terms=", length(unique(direct$term)), sep = "")
""",
                """direct_annotations=3
propagated_annotations=6
parent_genes=3
child_terms=2""",
                (
                    "Tres anotaciones directas producen seis filas después de incluir ancestros. Los tres genes del padre provienen de las mismas anotaciones hijas y no constituyen una réplica independiente.",
                    "Three direct annotations produce six rows after ancestors are included. The three parent genes arise from the same child annotations and are not an independent replication.",
                    "Tre direkte annotationer giver seks rækker efter inkludering af forfædre. De tre gener i forældretermen kommer fra de samme barneannotationer og er ikke en uafhængig replikation.",
                ),
            ),
        ),
        practice_exercises=module.practice_exercises
        + (
            practice(
                "m08.bg.p01",
                ActivityType.DATA_INTERPRETATION,
                (
                    "Un análisis devuelve un término GO padre y cuatro hijos significativos con casi los mismos genes. Explica qué evidencia existe y cómo resumirla sin inflarla.",
                    "An analysis returns one significant GO parent and four significant children with nearly the same genes. Explain the evidence and how to summarize it without inflation.",
                    "En analyse returnerer én signifikant GO-forældreterm og fire signifikante børn med næsten de samme gener. Forklar evidensen og hvordan den sammenfattes uden inflation.",
                ),
                (
                    (
                        "Examina propagación, solapamiento y genes conductores.",
                        "Examine propagation, overlap, and driver genes.",
                        "Undersøg propagering, overlap og drivende gener.",
                    ),
                    (
                        "No cuentes cinco términos como cinco validaciones.",
                        "Do not count five terms as five validations.",
                        "Tæl ikke fem termer som fem valideringer.",
                    ),
                ),
                (
                    "Los resultados apoyan una señal funcional asociada con el conjunto compartido de genes bajo la versión y evidencia anotativa utilizadas. El padre y los hijos son pruebas dependientes por jerarquía y solapamiento. Deben mostrarse genes conductores, tamaños, dirección, anotaciones directas y propagadas y versión de GO; luego agrupar términos con una regla declarada o elegir un representante sin ocultar los resultados completos. La validación requiere datos o recursos independientes.",
                    "The results support a functional signal associated with the shared gene set under the annotation version and evidence used. Parent and child tests are dependent through hierarchy and overlap. Report driver genes, sizes, direction, direct and propagated annotations, and GO version; then group terms with a declared rule or choose a representative without hiding complete results. Validation requires independent data or resources.",
                    "Resultaterne understøtter et funktionelt signal associeret med det delte gensæt under den anvendte annotationsversion og evidens. Forældre- og barnetests er afhængige gennem hierarki og overlap. Rapportér drivende gener, størrelser, retning, direkte og propagerede annotationer samt GO-version; gruppér derefter termer med en deklareret regel eller vælg en repræsentant uden at skjule komplette resultater. Validering kræver uafhængige data eller ressourcer.",
                ),
                (
                    "Una respuesta completa separa señal funcional, dependencia ontológica y validación independiente.",
                    "A complete answer separates functional signal, ontology dependence, and independent validation.",
                    "Et fuldstændigt svar adskiller funktionelt signal, ontologiafhængighed og uafhængig validering.",
                ),
                "",
            ),
        ),
        assessment_items=module.assessment_items
        + (
            objective_mcq(
                "bmb831.m08.book.001",
                (
                    "Un término padre y varios hijos comparten casi todos sus genes y son significativos. ¿Qué interpretación es válida?",
                    "A parent term and several children share nearly all genes and are significant. Which interpretation is valid?",
                    "En forældreterm og flere børn deler næsten alle gener og er signifikante. Hvilken fortolkning er gyldig?",
                ),
                (
                    (
                        "dependent_signal",
                        (
                            "Representan resultados dependientes que pueden resumir una misma señal anotativa",
                            "They are dependent results that may summarize the same annotation signal",
                            "De er afhængige resultater, der kan sammenfatte det samme annotationssignal",
                        ),
                    ),
                    (
                        "independent_replications",
                        (
                            "Cada término constituye una replicación biológica independiente",
                            "Each term is an independent biological replication",
                            "Hver term er en uafhængig biologisk replikation",
                        ),
                    ),
                    (
                        "causal_mechanisms",
                        (
                            "Cada término demuestra un mecanismo causal distinto",
                            "Each term demonstrates a distinct causal mechanism",
                            "Hver term demonstrerer en særskilt kausal mekanisme",
                        ),
                    ),
                ),
                "dependent_signal",
                (
                    "La jerarquía y propagación generan solapamiento y dependencia; los términos no son validaciones independientes.",
                    "Hierarchy and propagation generate overlap and dependence; the terms are not independent validations.",
                    "Hierarki og propagering skaber overlap og afhængighed; termerne er ikke uafhængige valideringer.",
                ),
            ),
        ),
    )


def _extend_specification_sensitivity(
    module: LocalizedLearningModule,
) -> LocalizedLearningModule:
    return replace(
        module,
        objectives=module.objectives
        + (
            objective(
                "m09.bg.o1",
                (
                    "Evaluar sensibilidad a especificaciones analíticas y detectar reporte selectivo de modelos favorables.",
                    "Evaluate sensitivity to analytical specifications and detect selective reporting of favourable models.",
                    "Vurdere følsomhed over for analytiske specifikationer og opdage selektiv rapportering af fordelagtige modeller.",
                ),
            ),
        ),
        concepts=module.concepts
        + (
            concept(
                "specification-sensitivity-and-selective-reporting",
                (
                    "Sensibilidad de especificación y reporte selectivo",
                    "Specification sensitivity and selective reporting",
                    "Specifikationsfølsomhed og selektiv rapportering",
                ),
                (
                    "Un resultado depende de decisiones sobre inclusión, filtros, transformaciones, covariables, contraste, missingness, multiplicidad y modelo. Cuando varias elecciones son científicamente defendibles, una sola especificación favorable no demuestra robustez. Debe definirse un conjunto justificable de análisis principales y de sensibilidad, conservar resultados completos y explicar qué decisiones cambian magnitud, dirección o incertidumbre. La preespecificación reduce flexibilidad retrospectiva, pero no reemplaza controles de calidad ni análisis de sensibilidad. En una evaluación de publicación, discrepancias entre métodos declarados, resultados mostrados y análisis omitidos deben marcarse como evidencia incompleta, no resolverse mediante suposiciones. Un informe sólido distingue análisis principal, alternativas, desviaciones y conclusiones que permanecen estables.",
                    "A result depends on decisions about inclusion, filtering, transformations, covariates, contrast, missingness, multiplicity, and model. When several choices are scientifically defensible, one favourable specification does not demonstrate robustness. Define a justified set of primary and sensitivity analyses, retain complete results, and explain which decisions change magnitude, direction, or uncertainty. Preregistration reduces retrospective flexibility but does not replace quality control or sensitivity analysis. In publication appraisal, discrepancies among declared methods, displayed results, and omitted analyses should be marked as incomplete evidence rather than resolved by assumptions. A strong report distinguishes the primary analysis, alternatives, deviations, and conclusions that remain stable.",
                    "Et resultat afhænger af beslutninger om inklusion, filtrering, transformationer, kovariater, kontrast, missingness, multiplicitet og model. Når flere valg er videnskabeligt forsvarlige, demonstrerer én fordelagtig specifikation ikke robusthed. Definér et begrundet sæt primære analyser og følsomhedsanalyser, bevar komplette resultater, og forklar hvilke beslutninger der ændrer størrelse, retning eller usikkerhed. Præregistrering reducerer retrospektiv fleksibilitet, men erstatter ikke kvalitetskontrol eller følsomhedsanalyse. Ved publikationsvurdering skal uoverensstemmelser mellem deklarerede metoder, viste resultater og udeladte analyser markeres som ufuldstændig evidens frem for at blive løst med antagelser. En stærk rapport adskiller primæranalyse, alternativer, afvigelser og konklusioner, der forbliver stabile.",
                ),
                (
                    (
                        "Una especificación favorable no equivale a robustez.",
                        "One favourable specification does not equal robustness.",
                        "Én fordelagtig specifikation er ikke det samme som robusthed.",
                    ),
                    (
                        "Las alternativas defendibles deben definirse y reportarse de forma completa.",
                        "Defensible alternatives should be defined and reported completely.",
                        "Forsvarlige alternativer bør defineres og rapporteres fuldstændigt.",
                    ),
                    (
                        "Cambios de signo, magnitud o precisión limitan la conclusión.",
                        "Changes in sign, magnitude, or precision limit the conclusion.",
                        "Ændringer i fortegn, størrelse eller præcision begrænser konklusionen.",
                    ),
                    (
                        "Lo no reportado se marca como ausente; no se reconstruye por conjetura.",
                        "Unreported information is marked missing rather than reconstructed by guesswork.",
                        "Ikke-rapporteret information markeres som manglende frem for at blive rekonstrueret ved gæt.",
                    ),
                ),
            ),
        ),
        worked_examples=module.worked_examples
        + (
            example(
                "m09.bg.e01",
                (
                    "Auditar estabilidad entre especificaciones",
                    "Audit stability across specifications",
                    "Auditér stabilitet på tværs af specifikationer",
                ),
                (
                    "Resume cuatro estimaciones obtenidas bajo decisiones analíticas defendibles y comprueba estabilidad de signo.",
                    "Summarize four estimates obtained under defensible analytical decisions and check sign stability.",
                    "Opsummér fire estimater opnået under forsvarlige analytiske beslutninger og kontrollér fortegnsstabilitet.",
                ),
                (
                    (
                        "Cada estimación corresponde a una especificación declarada.",
                        "Each estimate corresponds to one declared specification.",
                        "Hvert estimat svarer til én deklareret specifikation.",
                    ),
                    (
                        "El rango resume sensibilidad de magnitud.",
                        "The range summarizes magnitude sensitivity.",
                        "Intervallet opsummerer følsomhed i størrelse.",
                    ),
                    (
                        "Un cambio de signo impide declarar estabilidad direccional.",
                        "A sign change prevents a claim of directional stability.",
                        "Et fortegnsskift forhindrer en påstand om retningsstabilitet.",
                    ),
                ),
                """estimate <- c(primary = 0.80, adjusted = 0.60, filtered = 0.10, imputed = -0.20)
positive <- sum(estimate > 0)
negative <- sum(estimate < 0)
sign_stable <- positive == length(estimate) || negative == length(estimate)
cat("specifications=", length(estimate), "\n", sep = "")
cat("positive=", positive, "\n", sep = "")
cat("negative=", negative, "\n", sep = "")
cat(sprintf("range=%.2f,%.2f\n", min(estimate), max(estimate)))
cat("sign_stable=", sign_stable, sep = "")
""",
                """specifications=4
positive=3
negative=1
range=-0.20,0.80
sign_stable=FALSE""",
                (
                    "La estimación cambia de 0.80 a -0.20 y una especificación invierte el signo. El resultado no sostiene una conclusión direccional robusta sin explicar las decisiones y su plausibilidad.",
                    "The estimate changes from 0.80 to -0.20, and one specification reverses sign. The result does not support a robust directional conclusion without explaining the decisions and their plausibility.",
                    "Estimatet ændres fra 0,80 til -0,20, og én specifikation vender fortegnet. Resultatet understøtter ikke en robust retningsbestemt konklusion uden forklaring af beslutningerne og deres plausibilitet.",
                ),
            ),
        ),
        practice_exercises=module.practice_exercises
        + (
            practice(
                "m09.bg.p01",
                ActivityType.DATA_INTERPRETATION,
                (
                    "Una publicación muestra sólo el modelo con mayor efecto; tres análisis alternativos mencionados en métodos no aparecen. Diseña la evaluación y la redacción apropiada para el informe.",
                    "A publication shows only the model with the largest effect; three alternative analyses mentioned in methods are absent. Design the appraisal and appropriate report wording.",
                    "En publikation viser kun modellen med størst effekt; tre alternative analyser nævnt i metoderne mangler. Design vurderingen og passende rapportformulering.",
                ),
                (
                    (
                        "Reconstruye el conjunto de especificaciones esperado.",
                        "Reconstruct the expected specification set.",
                        "Rekonstruér det forventede specifikationssæt.",
                    ),
                    (
                        "Distingue ausencia de evidencia de evidencia de ausencia.",
                        "Distinguish absence of evidence from evidence of absence.",
                        "Skeln mellem fravær af evidens og evidens for fravær.",
                    ),
                ),
                (
                    "Debe construirse una tabla con cada especificación declarada, covariables, filtros, población, estimando y resultado disponible. El modelo mostrado se describe cuantitativamente, pero la robustez se clasifica como no evaluable porque faltan tres resultados. El informe indica reporte incompleto y posible selección, solicita tablas completas o suplementos y evita afirmar que las alternativas confirmaron o refutaron el hallazgo. Si se obtienen, se comparan dirección, magnitud, incertidumbre y decisiones que explican divergencias.",
                    "Build a table for every declared specification, covariates, filters, population, estimand, and available result. Describe the displayed model quantitatively, but classify robustness as not assessable because three results are missing. The report states incomplete reporting and possible selection, requests complete tables or supplements, and avoids claiming that alternatives confirmed or refuted the finding. If obtained, compare direction, magnitude, uncertainty, and decisions explaining divergence.",
                    "Byg en tabel for hver deklareret specifikation, kovariater, filtre, population, estimand og tilgængeligt resultat. Beskriv den viste model kvantitativt, men klassificér robusthed som ikke vurderbar, fordi tre resultater mangler. Rapporten angiver ufuldstændig rapportering og mulig selektion, efterspørger komplette tabeller eller supplementer og undgår at påstå, at alternativer bekræftede eller afkræftede fundet. Hvis de opnås, sammenlignes retning, størrelse, usikkerhed og beslutninger, der forklarer forskelle.",
                ),
                (
                    "Una respuesta completa no inventa resultados ausentes y separa hallazgo observado de robustez no evaluable.",
                    "A complete answer does not invent missing results and separates the observed finding from unassessable robustness.",
                    "Et fuldstændigt svar opfinder ikke manglende resultater og adskiller det observerede fund fra ikke-vurderbar robusthed.",
                ),
                "",
            ),
        ),
        assessment_items=module.assessment_items
        + (
            objective_mcq(
                "bmb831.m09.book.001",
                (
                    "Una publicación informa sólo la especificación con mayor efecto y omite alternativas declaradas. ¿Cuál es la conclusión adecuada?",
                    "A publication reports only the specification with the largest effect and omits declared alternatives. What is the appropriate conclusion?",
                    "En publikation rapporterer kun specifikationen med størst effekt og udelader deklarerede alternativer. Hvad er den passende konklusion?",
                ),
                (
                    (
                        "robustness_unknown",
                        (
                            "El efecto mostrado puede describirse, pero la robustez no es evaluable con resultados incompletos",
                            "The displayed effect can be described, but robustness is not assessable with incomplete results",
                            "Den viste effekt kan beskrives, men robusthed kan ikke vurderes med ufuldstændige resultater",
                        ),
                    ),
                    (
                        "robust_confirmed",
                        (
                            "El mayor efecto confirma que el resultado es robusto",
                            "The largest effect confirms that the result is robust",
                            "Den største effekt bekræfter, at resultatet er robust",
                        ),
                    ),
                    (
                        "alternatives_negative",
                        (
                            "Las alternativas omitidas necesariamente fueron negativas",
                            "The omitted alternatives were necessarily negative",
                            "De udeladte alternativer var nødvendigvis negative",
                        ),
                    ),
                ),
                "robustness_unknown",
                (
                    "La evidencia faltante impide evaluar sensibilidad; no autoriza confirmar robustez ni inventar el contenido omitido.",
                    "Missing evidence prevents sensitivity assessment; it does not justify confirming robustness or inventing omitted content.",
                    "Manglende evidens forhindrer følsomhedsvurdering; den retfærdiggør ikke bekræftelse af robusthed eller opfindelse af udeladt indhold.",
                ),
            ),
        ),
    )


def apply_interpretation_report_extensions(
    modules: tuple[LocalizedLearningModule, ...],
) -> tuple[LocalizedLearningModule, ...]:
    """Apply the completed M08-M09 extensions to the localized module catalog."""

    updated: list[LocalizedLearningModule] = []
    for module in modules:
        if module.module_id == "bmb831.m08":
            updated.append(_extend_ontology_propagation(module))
        elif module.module_id == "bmb831.m09":
            updated.append(_extend_specification_sensitivity(module))
        else:
            updated.append(module)
    return tuple(updated)


__all__ = [
    "apply_interpretation_report_extensions",
    "review_interpretation_report_audit",
]
