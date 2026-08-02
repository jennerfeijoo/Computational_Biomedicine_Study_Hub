"""Focused source-grounded review extensions for BMB831 modules 6 and 7."""

from __future__ import annotations

from dataclasses import replace

from ...learning.activity_types import ActivityType
from ..localized_models import LocalizedLearningModule
from .authoring import concept, example, objective, objective_mcq, practice
from .book_grounded_audit import ModuleSourceAudit


def review_public_omics_protein_audit(
    audits: tuple[ModuleSourceAudit, ...],
) -> tuple[ModuleSourceAudit, ...]:
    """Mark the completed M06-M07 reviews while preserving the source registry."""

    updated: list[ModuleSourceAudit] = []
    for audit in audits:
        if audit.module_id == "bmb831.m06":
            updated.append(
                replace(
                    audit,
                    state="consistent",
                    finding=(
                        "Existing public-source snapshots, assay-specific RNA-seq and proteomics "
                        "contracts, missingness, transition checks, and reproducibility boundaries "
                        "are consistent. The focused review identified one missing proteomics "
                        "boundary: shared peptides and protein-group inference can prevent "
                        "protein-specific attribution even when peptide quantification is precise."
                    ),
                    implemented_change=(
                        "Added a trilingual shared-peptide and protein-inference explanation, a "
                        "deterministic peptide-to-protein evidence example, an interpretation "
                        "exercise, and a stable objective assessment item."
                    ),
                )
            )
        elif audit.module_id == "bmb831.m07":
            updated.append(
                replace(
                    audit,
                    state="consistent",
                    finding=(
                        "Existing sequence identity, derived properties, UniProt and InterPro "
                        "provenance, PDB coverage, and AlphaFold boundaries are consistent. The "
                        "focused review identified one missing structural-confidence distinction: "
                        "high local pLDDT does not guarantee confident relative domain placement, "
                        "which requires inspection of predicted aligned error."
                    ),
                    implemented_change=(
                        "Added a trilingual pLDDT-versus-PAE explanation, a deterministic two-domain "
                        "confidence example, an interpretation exercise, and a stable objective "
                        "assessment item."
                    ),
                )
            )
        else:
            updated.append(audit)
    return tuple(updated)


def _extend_protein_inference(
    module: LocalizedLearningModule,
) -> LocalizedLearningModule:
    return replace(
        module,
        objectives=module.objectives
        + (
            objective(
                "m06.bg.o1",
                (
                    "Distinguir evidencia peptídica única, compartida y de grupo antes de atribuir cuantificación a proteínas individuales.",
                    "Distinguish unique, shared, and group-level peptide evidence before attributing quantification to individual proteins.",
                    "Skelne mellem unik, delt og gruppeniveau-peptidevidens før kvantificering tilskrives individuelle proteiner.",
                ),
            ),
        ),
        concepts=module.concepts
        + (
            concept(
                "shared-peptides-and-protein-inference",
                (
                    "Péptidos compartidos e inferencia de proteínas",
                    "Shared peptides and protein inference",
                    "Delte peptider og proteininferens",
                ),
                (
                    "En señal de espectrometría de masas se asigna primero a precursores y péptidos, no directamente a una proteína única. Un péptido proteotípico puede apoyar una proteína concreta, mientras que un péptido compartido es compatible con varias proteínas, isoformas o miembros de una familia. Las reglas de parsimonia, razor peptides o protein grouping resuelven la tabla computacional, pero no crean evidencia que distinga entidades biológicamente indistinguibles. Por ello deben conservarse los mapeos precursor–péptido–proteína, declararse las reglas de agrupación y limitar el estimando al nivel realmente identificado. Una diferencia en un protein group no demuestra cuál de sus miembros cambió.",
                    "A mass-spectrometry signal is assigned first to precursors and peptides, not directly to one unique protein. A proteotypic peptide may support a particular protein, whereas a shared peptide is compatible with several proteins, isoforms, or family members. Parsimony, razor-peptide, or protein-grouping rules resolve the computational table but do not create evidence that distinguishes biologically indistinguishable entities. Therefore precursor-peptide-protein mappings must be retained, grouping rules declared, and the estimand limited to the level actually identified. A difference in a protein group does not demonstrate which member changed.",
                    "Et massespektrometrisignal tildeles først precursors og peptider, ikke direkte til ét unikt protein. Et proteotypisk peptid kan understøtte et bestemt protein, mens et delt peptid er kompatibelt med flere proteiner, isoformer eller familiemedlemmer. Parsimoni-, razor-peptide- eller protein-grouping-regler løser den beregningsmæssige tabel, men skaber ikke evidens, der adskiller biologisk uadskillelige enheder. Derfor skal precursor-peptid-protein-mappinger bevares, grouping-regler deklareres, og estimanden begrænses til det faktisk identificerede niveau. En forskel i en proteingruppe demonstrerer ikke, hvilket medlem der ændrede sig.",
                ),
                (
                    (
                        "La cuantificación peptídica y la identificación proteica son niveles relacionados pero distintos.",
                        "Peptide quantification and protein identification are related but distinct levels.",
                        "Peptidkvantificering og proteinidentifikation er relaterede, men forskellige niveauer.",
                    ),
                    (
                        "Un péptido compartido no identifica por sí solo una proteína individual.",
                        "A shared peptide does not by itself identify an individual protein.",
                        "Et delt peptid identificerer ikke i sig selv et individuelt protein.",
                    ),
                    (
                        "Las reglas de agrupación cambian la unidad analítica y deben registrarse.",
                        "Grouping rules change the analytical unit and must be recorded.",
                        "Grouping-regler ændrer den analytiske enhed og skal registreres.",
                    ),
                    (
                        "La afirmación final no puede ser más específica que la evidencia identificable.",
                        "The final claim cannot be more specific than the identifiable evidence.",
                        "Den endelige påstand kan ikke være mere specifik end den identificerbare evidens.",
                    ),
                ),
            ),
        ),
        worked_examples=module.worked_examples
        + (
            example(
                "m06.bg.e01",
                (
                    "Auditar evidencia peptídica única y compartida",
                    "Audit unique and shared peptide evidence",
                    "Auditér unik og delt peptidevidens",
                ),
                (
                    "Resume un mapeo péptido–proteína y detecta proteínas respaldadas sólo por péptidos compartidos.",
                    "Summarize a peptide-protein mapping and detect proteins supported only by shared peptides.",
                    "Opsummér en peptid-protein-mapping og identificér proteiner, der kun understøttes af delte peptider.",
                ),
                (
                    (
                        "Cada fila representa una relación de compatibilidad entre un péptido y una proteína.",
                        "Each row represents one compatibility relation between a peptide and a protein.",
                        "Hver række repræsenterer én kompatibilitetsrelation mellem et peptid og et protein.",
                    ),
                    (
                        "La multiplicidad del péptido determina si su evidencia es única o compartida.",
                        "Peptide multiplicity determines whether its evidence is unique or shared.",
                        "Peptidets multiplicitet bestemmer, om evidensen er unik eller delt.",
                    ),
                    (
                        "Una proteína sin péptidos únicos permanece identificada sólo al nivel de grupo.",
                        "A protein without unique peptides remains identified only at group level.",
                        "Et protein uden unikke peptider forbliver kun identificeret på gruppeniveau.",
                    ),
                ),
                """mapping <- data.frame(
  peptide = c("pep1", "pep2", "pep2", "pep3", "pep4", "pep4"),
  protein = c("P1", "P1", "P2", "P2", "P3", "P4"),
  stringsAsFactors = FALSE
)
peptide_multiplicity <- table(mapping$peptide)
unique_peptides <- names(peptide_multiplicity[peptide_multiplicity == 1])
shared_peptides <- names(peptide_multiplicity[peptide_multiplicity > 1])
proteins_with_unique <- unique(mapping$protein[mapping$peptide %in% unique_peptides])
all_proteins <- unique(mapping$protein)
shared_only <- setdiff(all_proteins, proteins_with_unique)
cat("peptides=", length(peptide_multiplicity), "\n", sep = "")
cat("unique_peptides=", length(unique_peptides), "\n", sep = "")
cat("shared_peptides=", length(shared_peptides), "\n", sep = "")
cat("proteins_with_unique=", length(proteins_with_unique), "\n", sep = "")
cat("proteins_shared_only=", length(shared_only), sep = "")
""",
                """peptides=4
unique_peptides=2
shared_peptides=2
proteins_with_unique=2
proteins_shared_only=2""",
                (
                    "P1 y P2 tienen al menos un péptido único, mientras que P3 y P4 sólo comparten pep4. El fixture permite una afirmación de grupo para P3/P4, no una atribución individual.",
                    "P1 and P2 have at least one unique peptide, whereas P3 and P4 share only pep4. The fixture supports a group-level claim for P3/P4, not individual attribution.",
                    "P1 og P2 har mindst ét unikt peptid, mens P3 og P4 kun deler pep4. Fixturet understøtter en påstand på gruppeniveau for P3/P4, ikke individuel tilskrivning.",
                ),
            ),
        ),
        practice_exercises=module.practice_exercises
        + (
            practice(
                "m06.bg.p01",
                ActivityType.DATA_INTERPRETATION,
                (
                    "Un protein group contiene tres isoformas y todos los péptidos cuantificados son compartidos. El grupo cambia entre condiciones. Formula la conclusión válida y los controles necesarios.",
                    "A protein group contains three isoforms and all quantified peptides are shared. The group changes between conditions. State the valid conclusion and required checks.",
                    "En proteingruppe indeholder tre isoformer, og alle kvantificerede peptider er delte. Gruppen ændrer sig mellem betingelser. Formulér den gyldige konklusion og de nødvendige kontroller.",
                ),
                (
                    (
                        "Limita la afirmación al nivel de grupo.",
                        "Limit the claim to group level.",
                        "Begræns påstanden til gruppeniveau.",
                    ),
                    (
                        "Revisa mapeo, reglas de agrupación y péptidos específicos ausentes.",
                        "Review mappings, grouping rules, and absent specific peptides.",
                        "Gennemgå mappinger, grouping-regler og fraværende specifikke peptider.",
                    ),
                ),
                (
                    "La evidencia sostiene un cambio en la señal asignada al protein group, pero no identifica cuál isoforma cambió. Deben conservarse los péptidos y precursores originales, verificar secuencias e isoformas de referencia, documentar la regla de protein grouping, inspeccionar péptidos únicos o discriminantes y realizar análisis de sensibilidad ante reglas alternativas. Una conclusión isoforma-específica requeriría evidencia adicional.",
                    "The evidence supports a change in signal assigned to the protein group but does not identify which isoform changed. Retain original peptides and precursors, verify reference sequences and isoforms, document the protein-grouping rule, inspect unique or discriminating peptides, and perform sensitivity analysis under alternative rules. An isoform-specific conclusion requires additional evidence.",
                    "Evidensen understøtter en ændring i signalet tildelt proteingruppen, men identificerer ikke, hvilken isoform der ændrede sig. Bevar originale peptider og precursors, verificér referencesekvenser og isoformer, dokumentér protein-grouping-reglen, inspicér unikke eller diskriminerende peptider, og udfør følsomhedsanalyse under alternative regler. En isoformspecifik konklusion kræver yderligere evidens.",
                ),
                (
                    "Una respuesta completa separa cuantificación, inferencia de proteínas y especificidad de la afirmación.",
                    "A complete answer separates quantification, protein inference, and claim specificity.",
                    "Et fuldstændigt svar adskiller kvantificering, proteininferens og påstandens specificitet.",
                ),
                "",
            ),
        ),
        assessment_items=module.assessment_items
        + (
            objective_mcq(
                "bmb831.m06.book.001",
                (
                    "Todos los péptidos cuantificados de un grupo son compartidos por dos isoformas. ¿Qué conclusión está respaldada?",
                    "All quantified peptides in a group are shared by two isoforms. Which conclusion is supported?",
                    "Alle kvantificerede peptider i en gruppe deles af to isoformer. Hvilken konklusion understøttes?",
                ),
                (
                    (
                        "group_level",
                        (
                            "La señal del grupo difiere, sin atribuir el cambio a una isoforma concreta",
                            "The group signal differs without attributing the change to one specific isoform",
                            "Gruppens signal er forskelligt uden at tilskrive ændringen til én bestemt isoform",
                        ),
                    ),
                    (
                        "first_isoform",
                        (
                            "La primera isoforma necesariamente cambió",
                            "The first isoform necessarily changed",
                            "Den første isoform ændrede sig nødvendigvis",
                        ),
                    ),
                    (
                        "both_individual",
                        (
                            "Ambas isoformas fueron cuantificadas individualmente",
                            "Both isoforms were individually quantified",
                            "Begge isoformer blev kvantificeret individuelt",
                        ),
                    ),
                ),
                "group_level",
                (
                    "Los péptidos compartidos sostienen evidencia compatible con el grupo, pero no resuelven la contribución de cada isoforma.",
                    "Shared peptides support evidence compatible with the group but do not resolve each isoform's contribution.",
                    "Delte peptider understøtter evidens kompatibel med gruppen, men opløser ikke hver isoforms bidrag.",
                ),
            ),
        ),
    )


def _extend_alphafold_confidence(
    module: LocalizedLearningModule,
) -> LocalizedLearningModule:
    return replace(
        module,
        objectives=module.objectives
        + (
            objective(
                "m07.bg.o1",
                (
                    "Distinguir confianza estructural local de confianza en la orientación relativa de dominios usando pLDDT y PAE.",
                    "Distinguish local structural confidence from confidence in relative domain orientation using pLDDT and PAE.",
                    "Skelne lokal strukturel confidence fra confidence i domæners relative orientering ved hjælp af pLDDT og PAE.",
                ),
            ),
        ),
        concepts=module.concepts
        + (
            concept(
                "local-confidence-versus-domain-placement",
                (
                    "Confianza local y colocación relativa de dominios",
                    "Local confidence and relative domain placement",
                    "Lokal confidence og relativ domæneplacering",
                ),
                (
                    "pLDDT estima confianza local por residuo y ayuda a identificar regiones cuyo entorno atómico predicho es más o menos fiable. No evalúa por sí solo si dos dominios están orientados correctamente entre sí. PAE estima el error esperado en la posición de una región cuando la predicción se alinea sobre otra y, por tanto, informa sobre relaciones de largo alcance, empaquetamiento de dominios y topología global. Dos dominios pueden tener pLDDT alto y geometría interna plausible, pero PAE alto entre ellos, indicando que su orientación relativa es incierta. La interpretación debe revisar ambas métricas por región y no convertir una media global en certeza biológica, interacción, dinámica o mecanismo.",
                    "pLDDT estimates local confidence per residue and helps identify regions whose predicted atomic environment is more or less reliable. By itself it does not assess whether two domains are correctly oriented relative to one another. PAE estimates the expected positional error of one region when the prediction is aligned on another and therefore informs long-range relationships, domain packing, and global topology. Two domains may have high pLDDT and plausible internal geometry but high PAE between them, indicating uncertain relative orientation. Interpretation should inspect both metrics by region and should not turn a global average into biological certainty, interaction, dynamics, or mechanism.",
                    "pLDDT estimerer lokal confidence pr. rest og hjælper med at identificere regioner, hvis forudsagte atomare miljø er mere eller mindre pålideligt. Det vurderer ikke i sig selv, om to domæner er korrekt orienteret i forhold til hinanden. PAE estimerer den forventede positionsfejl for én region, når prædiktionen alignes på en anden, og informerer derfor om langtrækkende relationer, domænepakning og global topologi. To domæner kan have høj pLDDT og plausibel intern geometri, men høj PAE mellem dem, hvilket angiver usikker relativ orientering. Fortolkningen bør inspicere begge mål efter region og må ikke omdanne et globalt gennemsnit til biologisk sikkerhed, interaktion, dynamik eller mekanisme.",
                ),
                (
                    (
                        "pLDDT es una medida local por residuo.",
                        "pLDDT is a local per-residue measure.",
                        "pLDDT er et lokalt mål pr. rest.",
                    ),
                    (
                        "PAE informa sobre la confianza en posiciones relativas entre regiones.",
                        "PAE informs confidence in relative positions between regions.",
                        "PAE informerer om confidence i relative positioner mellem regioner.",
                    ),
                    (
                        "Dominios localmente confiables pueden tener orientación mutua incierta.",
                        "Locally confident domains may have uncertain mutual orientation.",
                        "Lokalt pålidelige domæner kan have usikker indbyrdes orientering.",
                    ),
                    (
                        "Ninguna métrica estructural demuestra por sí sola función o mecanismo.",
                        "No structural confidence metric alone demonstrates function or mechanism.",
                        "Intet strukturelt confidence-mål demonstrerer alene funktion eller mekanisme.",
                    ),
                ),
            ),
        ),
        worked_examples=module.worked_examples
        + (
            example(
                "m07.bg.e01",
                (
                    "Separar confianza intradominio e interdominio",
                    "Separate within-domain and between-domain confidence",
                    "Adskil confidence inden for og mellem domæner",
                ),
                (
                    "Resume pLDDT y una matriz PAE para dos dominios de tres residuos cada uno.",
                    "Summarize pLDDT and a PAE matrix for two three-residue domains.",
                    "Opsummér pLDDT og en PAE-matrix for to domæner med tre rester hver.",
                ),
                (
                    (
                        "pLDDT se resume por dominio como confianza local.",
                        "pLDDT is summarized by domain as local confidence.",
                        "pLDDT opsummeres pr. domæne som lokal confidence.",
                    ),
                    (
                        "PAE intradominio excluye la diagonal trivial.",
                        "Within-domain PAE excludes the trivial diagonal.",
                        "PAE inden for domænet udelukker den trivielle diagonal.",
                    ),
                    (
                        "PAE interdominio resume la incertidumbre de colocación relativa.",
                        "Between-domain PAE summarizes uncertainty in relative placement.",
                        "PAE mellem domæner opsummerer usikkerheden i relativ placering.",
                    ),
                ),
                """plddt <- c(92, 90, 88, 91, 89, 87)
pae <- matrix(
  c(0, 2, 2, 18, 18, 18,
    2, 0, 2, 18, 18, 18,
    2, 2, 0, 18, 18, 18,
    18, 18, 18, 0, 2, 2,
    18, 18, 18, 2, 0, 2,
    18, 18, 18, 2, 2, 0),
  nrow = 6,
  byrow = TRUE
)
domain_a <- 1:3
domain_b <- 4:6
within_mean <- function(index) {
  block <- pae[index, index, drop = FALSE]
  mean(block[upper.tri(block)])
}
between_mean <- mean(pae[domain_a, domain_b, drop = FALSE])
cat(sprintf("domain_A_plddt=%.1f\n", mean(plddt[domain_a])))
cat(sprintf("domain_B_plddt=%.1f\n", mean(plddt[domain_b])))
cat(sprintf("within_A_pae=%.1f\n", within_mean(domain_a)))
cat(sprintf("within_B_pae=%.1f\n", within_mean(domain_b)))
cat(sprintf("between_pae=%.1f", between_mean))
""",
                """domain_A_plddt=90.0
domain_B_plddt=89.0
within_A_pae=2.0
within_B_pae=2.0
between_pae=18.0""",
                (
                    "Ambos dominios tienen alta confianza local y bajo PAE interno, pero el PAE de 18 entre dominios indica que su orientación relativa es mucho menos segura.",
                    "Both domains have high local confidence and low internal PAE, but the between-domain PAE of 18 indicates that their relative orientation is much less certain.",
                    "Begge domæner har høj lokal confidence og lav intern PAE, men PAE på 18 mellem domænerne viser, at deres relative orientering er langt mindre sikker.",
                ),
            ),
        ),
        practice_exercises=module.practice_exercises
        + (
            practice(
                "m07.bg.p01",
                ActivityType.DATA_INTERPRETATION,
                (
                    "Un modelo tiene dos dominios con pLDDT medio superior a 90, pero PAE alto entre dominios. ¿Qué puede afirmarse y qué debe evitarse?",
                    "A model has two domains with mean pLDDT above 90 but high PAE between domains. What can be stated, and what should be avoided?",
                    "En model har to domæner med gennemsnitlig pLDDT over 90, men høj PAE mellem domænerne. Hvad kan angives, og hvad bør undgås?",
                ),
                (
                    (
                        "Separa geometría local de orientación relativa.",
                        "Separate local geometry from relative orientation.",
                        "Adskil lokal geometri fra relativ orientering.",
                    ),
                    (
                        "No infieras interacción o mecanismo desde confianza estructural.",
                        "Do not infer interaction or mechanism from structural confidence.",
                        "Udled ikke interaktion eller mekanisme fra strukturel confidence.",
                    ),
                ),
                (
                    "Puede afirmarse que cada dominio tiene una predicción localmente confiable bajo pLDDT, mientras que su empaquetamiento u orientación mutua es incierto según PAE. Deben mostrarse métricas por región, revisar posibles linkers flexibles y comparar con evidencia experimental, homólogos o estructuras de complejos. Debe evitarse tratar la disposición global como definida o usarla como prueba de interacción, dinámica, estado activo o mecanismo.",
                    "Each domain can be described as locally confident under pLDDT, while their mutual packing or orientation is uncertain according to PAE. Report regional metrics, examine possible flexible linkers, and compare with experimental evidence, homologues, or complex structures. Avoid treating the global arrangement as fixed or using it as proof of interaction, dynamics, active state, or mechanism.",
                    "Hvert domæne kan beskrives som lokalt pålideligt under pLDDT, mens deres indbyrdes pakning eller orientering er usikker ifølge PAE. Rapportér regionale mål, undersøg mulige fleksible linkers, og sammenlign med eksperimentel evidens, homologer eller kompleksstrukturer. Undgå at behandle det globale arrangement som fastlagt eller bruge det som bevis for interaktion, dynamik, aktiv tilstand eller mekanisme.",
                ),
                (
                    "Una respuesta completa interpreta pLDDT y PAE como métricas complementarias con límites biológicos explícitos.",
                    "A complete answer interprets pLDDT and PAE as complementary metrics with explicit biological limits.",
                    "Et fuldstændigt svar fortolker pLDDT og PAE som komplementære mål med eksplicitte biologiske grænser.",
                ),
                "",
            ),
        ),
        assessment_items=module.assessment_items
        + (
            objective_mcq(
                "bmb831.m07.book.001",
                (
                    "Dos dominios tienen pLDDT alto, pero PAE alto entre ellos. ¿Cuál es la interpretación correcta?",
                    "Two domains have high pLDDT but high PAE between them. What is the correct interpretation?",
                    "To domæner har høj pLDDT, men høj PAE mellem dem. Hvad er den korrekte fortolkning?",
                ),
                (
                    (
                        "local_not_relative",
                        (
                            "La geometría local puede ser confiable, pero la orientación relativa es incierta",
                            "Local geometry may be reliable, but relative orientation is uncertain",
                            "Lokal geometri kan være pålidelig, men den relative orientering er usikker",
                        ),
                    ),
                    (
                        "global_certain",
                        (
                            "La estructura global completa está confirmada",
                            "The complete global structure is confirmed",
                            "Den komplette globale struktur er bekræftet",
                        ),
                    ),
                    (
                        "function_proven",
                        (
                            "La función y el mecanismo están demostrados",
                            "Function and mechanism are demonstrated",
                            "Funktion og mekanisme er demonstreret",
                        ),
                    ),
                ),
                "local_not_relative",
                (
                    "pLDDT informa confianza local, mientras que PAE alto entre dominios advierte sobre su colocación relativa.",
                    "pLDDT reports local confidence, whereas high between-domain PAE warns about relative placement.",
                    "pLDDT rapporterer lokal confidence, mens høj PAE mellem domæner advarer om relativ placering.",
                ),
            ),
        ),
    )


def apply_public_omics_protein_extensions(
    modules: tuple[LocalizedLearningModule, ...],
) -> tuple[LocalizedLearningModule, ...]:
    """Apply the completed M06-M07 extensions to the localized module catalog."""

    updated: list[LocalizedLearningModule] = []
    for module in modules:
        if module.module_id == "bmb831.m06":
            updated.append(_extend_protein_inference(module))
        elif module.module_id == "bmb831.m07":
            updated.append(_extend_alphafold_confidence(module))
        else:
            updated.append(module)
    return tuple(updated)


__all__ = [
    "apply_public_omics_protein_extensions",
    "review_public_omics_protein_audit",
]
