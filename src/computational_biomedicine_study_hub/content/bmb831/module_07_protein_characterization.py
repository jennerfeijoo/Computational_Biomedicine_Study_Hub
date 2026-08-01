"""BMB831 module 7: computational protein characterization."""

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
    module_id="bmb831.m07",
    title=_t(
        "Caracterización computacional de proteínas",
        "Computational protein characterization",
        "Computational proteinkarakterisering",
    ),
    summary=_t(
        "Caracteriza una proteína desde una secuencia versionada hasta propiedades, dominios, localización y estructura, distinguiendo evidencia experimental, curación, predicción y límites de cobertura.",
        "Characterize a protein from a versioned sequence through properties, domains, localization, and structure while distinguishing experimental evidence, curation, prediction, and coverage limits.",
        "Karakterisér et protein fra en versioneret sekvens gennem egenskaber, domæner, lokalisering og struktur, mens eksperimentel evidens, kuratering, prædiktion og dækningsgrænser adskilles.",
    ),
    objectives=(
        (
            "m07.o1",
            _t(
                "Validar identidad, especie, isoforma, longitud, alfabeto y versión de una secuencia proteica.",
                "Validate identity, species, isoform, length, alphabet, and version of a protein sequence.",
                "Validere identitet, art, isoform, længde, alfabet og version af en proteinsekvens.",
            ),
        ),
        (
            "m07.o2",
            _t(
                "Calcular e interpretar propiedades derivadas de secuencia sin tratarlas como mediciones experimentales.",
                "Calculate and interpret sequence-derived properties without treating them as experimental measurements.",
                "Beregne og fortolke sekvensafledte egenskaber uden at behandle dem som eksperimentelle målinger.",
            ),
        ),
        (
            "m07.o3",
            _t(
                "Integrar dominios, familias, sitios, señales, regiones transmembrana y anotación funcional con procedencia.",
                "Integrate domains, families, sites, signals, transmembrane regions, and functional annotation with provenance.",
                "Integrere domæner, familier, sites, signaler, transmembranregioner og funktionel annotering med proveniens.",
            ),
        ),
        (
            "m07.o4",
            _t(
                "Evaluar evidencia estructural experimental y predicha considerando cobertura, resolución o confianza y contexto biológico.",
                "Evaluate experimental and predicted structural evidence considering coverage, resolution or confidence, and biological context.",
                "Vurdere eksperimentel og prædikteret strukturel evidens med hensyn til dækning, opløsning eller confidence og biologisk kontekst.",
            ),
        ),
    ),
    concepts=(
        (
            "sequence-identity",
            _t(
                "Identidad de secuencia y versiones",
                "Sequence identity and versions",
                "Sekvensidentitet og versioner",
            ),
            _t(
                "Un nombre de proteína puede referirse a especies, isoformas o revisiones distintas. El contrato mínimo incluye accession, versión, organismo, isoforma, longitud y secuencia exacta. Deben comprobarse caracteres no estándar, residuos ambiguos y discrepancias entre FASTA y metadata. Comparar resultados obtenidos con versiones diferentes sin declararlo puede atribuir cambios de anotación a biología.",
                "A protein name may refer to different species, isoforms, or revisions. The minimum contract includes accession, version, organism, isoform, length, and exact sequence. Nonstandard characters, ambiguous residues, and discrepancies between FASTA and metadata must be checked. Comparing results obtained from different versions without declaring this may attribute annotation changes to biology.",
                "Et proteinnavn kan referere til forskellige arter, isoformer eller revisioner. Minimumskontrakten omfatter accession, version, organisme, isoform, længde og præcis sekvens. Ikke-standardtegn, tvetydige rester og forskelle mellem FASTA og metadata skal kontrolleres. Sammenligning af resultater fra forskellige versioner uden deklaration kan tilskrive annoteringsændringer til biologi.",
            ),
            (
                _t(
                    "Conserva el FASTA exacto y su checksum.",
                    "Retain the exact FASTA and its checksum.",
                    "Bevar den præcise FASTA og dens checksum.",
                ),
                _t(
                    "La isoforma forma parte de la identidad analítica.",
                    "The isoform is part of analytical identity.",
                    "Isoformen er del af den analytiske identitet.",
                ),
            ),
        ),
        (
            "sequence-properties",
            _t(
                "Propiedades derivadas de secuencia",
                "Sequence-derived properties",
                "Sekvensafledte egenskaber",
            ),
            _t(
                "Composición, masa aproximada, carga, pI e hidropatía se calculan bajo escalas y supuestos definidos. Son descriptores útiles para formular hipótesis sobre solubilidad, separación o segmentos de membrana, pero no sustituyen mediciones de estado oligomérico, modificaciones postraduccionales o comportamiento en una condición experimental. Las ventanas hidropáticas dependen de escala y longitud de ventana.",
                "Composition, approximate mass, charge, pI, and hydropathy are calculated under defined scales and assumptions. They are useful descriptors for hypotheses about solubility, separation, or membrane segments but do not replace measurements of oligomeric state, post-translational modifications, or behavior under an experimental condition. Hydropathy windows depend on scale and window length.",
                "Sammensætning, omtrentlig masse, ladning, pI og hydrofobicitet beregnes under definerede skalaer og antagelser. De er nyttige deskriptorer til hypoteser om opløselighed, separation eller membransegmenter, men erstatter ikke målinger af oligomerisk tilstand, posttranslationelle modifikationer eller adfærd under en eksperimentel betingelse. Hydropativinduer afhænger af skala og vindueslængde.",
            ),
            (
                _t(
                    "Registra la escala usada para cada descriptor.",
                    "Record the scale used for every descriptor.",
                    "Registrér skalaen for hver deskriptor.",
                ),
                _t(
                    "Interpreta predicciones como hipótesis, no confirmaciones.",
                    "Interpret predictions as hypotheses, not confirmations.",
                    "Fortolk prædiktioner som hypoteser, ikke bekræftelser.",
                ),
            ),
        ),
        (
            "domains-annotation",
            _t(
                "Dominios, familias y anotación",
                "Domains, families, and annotation",
                "Domæner, familier og annotering",
            ),
            _t(
                "InterPro integra firmas de familias, dominios, repeticiones y sitios. Un match tiene coordenadas, modelo, base integrante y puntuación o umbral; la arquitectura completa importa más que una etiqueta aislada. UniProt puede incluir evidencia revisada, literatura, similitud o predicción. La procedencia y el código de evidencia deben acompañar cualquier afirmación funcional, especialmente en proteínas no revisadas.",
                "InterPro integrates family, domain, repeat, and site signatures. A match has coordinates, model, member database, and score or threshold; complete architecture matters more than an isolated label. UniProt may include reviewed evidence, literature, similarity, or prediction. Provenance and evidence code should accompany every functional claim, especially for unreviewed proteins.",
                "InterPro integrerer signaturer for familier, domæner, repeats og sites. Et match har koordinater, model, medlemsdatabase og score eller tærskel; den komplette arkitektur er vigtigere end en isoleret label. UniProt kan indeholde reviewed evidens, litteratur, lighed eller prædiktion. Proveniens og evidenskode bør ledsage enhver funktionel påstand, især for ikke-reviewed proteiner.",
            ),
            (
                _t(
                    "Comprueba cobertura y solapamiento de dominios.",
                    "Check domain coverage and overlap.",
                    "Kontrollér domænedækning og overlap.",
                ),
                _t(
                    "Distingue anotación transferida de evidencia directa.",
                    "Distinguish transferred annotation from direct evidence.",
                    "Skeln mellem overført annotering og direkte evidens.",
                ),
            ),
        ),
        (
            "structure-evidence",
            _t(
                "Estructura experimental y predicha",
                "Experimental and predicted structure",
                "Eksperimentel og prædikteret struktur",
            ),
            _t(
                "Una estructura PDB debe evaluarse por método, resolución o calidad, constructo, ligandos, mutaciones y cobertura de residuos. Una predicción como AlphaFold aporta un modelo con confianza local y relaciones geométricas, pero regiones de baja confianza pueden ser desordenadas o depender de contexto. Un modelo monomérico no demuestra ensamblaje, interacción, dinámica ni estado funcional. La estructura se integra con secuencia y evidencia experimental.",
                "A PDB structure should be evaluated by method, resolution or quality, construct, ligands, mutations, and residue coverage. A prediction such as AlphaFold provides a model with local confidence and geometric relations, but low-confidence regions may be disordered or context dependent. A monomeric model does not demonstrate assembly, interaction, dynamics, or functional state. Structure is integrated with sequence and experimental evidence.",
                "En PDB-struktur bør vurderes efter metode, opløsning eller kvalitet, construct, ligander, mutationer og restdækning. En prædiktion som AlphaFold giver en model med lokal confidence og geometriske relationer, men lav-confidence-regioner kan være uordnede eller kontekstafhængige. En monomerisk model demonstrerer ikke assembly, interaktion, dynamik eller funktionel tilstand. Struktur integreres med sekvens og eksperimentel evidens.",
            ),
            (
                _t(
                    "Alinea numeración de estructura e isoforma.",
                    "Align structure numbering with the isoform.",
                    "Afstem strukturnummerering med isoformen.",
                ),
                _t(
                    "Reporta residuos no modelados y baja confianza.",
                    "Report unmodeled and low-confidence residues.",
                    "Rapportér ikke-modellerede rester og lav confidence.",
                ),
            ),
        ),
    ),
    examples=(
        (
            "m07.e01",
            _t(
                "Validar alfabeto y composición",
                "Validate alphabet and composition",
                "Validér alfabet og sammensætning",
            ),
            _t(
                "Comprueba una secuencia y resume residuos hidrofóbicos.",
                "Check a sequence and summarize hydrophobic residues.",
                "Kontrollér en sekvens og opsummér hydrofobe rester.",
            ),
            (
                _t(
                    "Se usa el alfabeto estándar de veinte residuos.",
                    "The standard twenty-residue alphabet is used.",
                    "Standardalfabetet med tyve rester bruges.",
                ),
                _t(
                    "La fracción es un descriptor, no una localización confirmada.",
                    "The fraction is a descriptor, not confirmed localization.",
                    "Fraktionen er en deskriptor, ikke bekræftet lokalisering.",
                ),
                _t(
                    "La secuencia exacta permanece visible.",
                    "The exact sequence remains visible.",
                    "Den præcise sekvens forbliver synlig.",
                ),
            ),
            """sequence <- "MKWVTFISLL"
residues <- strsplit(sequence, "", fixed = TRUE)[[1]]
standard <- strsplit("ACDEFGHIKLMNPQRSTVWY", "", fixed = TRUE)[[1]]
hydrophobic <- strsplit("AILMFWVY", "", fixed = TRUE)[[1]]
cat("valid=", all(residues %in% standard), "\n", sep = "")
cat("length=", length(residues), "\n", sep = "")
cat(sprintf("hydrophobic_fraction=%.2f", mean(residues %in% hydrophobic)))
""",
            """valid=TRUE
length=10
hydrophobic_fraction=0.70""",
            _t(
                "La secuencia usa residuos estándar y siete de diez pertenecen al conjunto hidrofóbico declarado.",
                "The sequence uses standard residues, and seven of ten belong to the declared hydrophobic set.",
                "Sekvensen bruger standardrester, og syv af ti tilhører det deklarerede hydrofobe sæt.",
            ),
        ),
        (
            "m07.e02",
            _t(
                "Calcular una ventana hidropática",
                "Calculate a hydropathy window",
                "Beregn et hydropativindue",
            ),
            _t(
                "Aplica una escala pequeña declarada para identificar la ventana más hidrofóbica.",
                "Apply a small declared scale to identify the most hydrophobic window.",
                "Anvend en lille deklareret skala til at identificere det mest hydrofobe vindue.",
            ),
            (
                _t(
                    "La escala es ilustrativa y explícita.",
                    "The scale is illustrative and explicit.",
                    "Skalaen er illustrativ og eksplicit.",
                ),
                _t(
                    "La ventana tiene longitud cuatro.",
                    "The window length is four.",
                    "Vindueslængden er fire.",
                ),
                _t(
                    "El máximo genera una hipótesis de segmento.",
                    "The maximum generates a segment hypothesis.",
                    "Maksimum genererer en segmenthypotese.",
                ),
            ),
            """residues <- strsplit("DDDAILMVKK", "", fixed = TRUE)[[1]]
scale <- c(A = 1.8, I = 4.5, L = 3.8, M = 1.9, V = 4.2, D = -3.5, K = -3.9)
window <- 4
scores <- vapply(seq_len(length(residues) - window + 1), function(start) {
  mean(scale[residues[start:(start + window - 1)]])
}, numeric(1))
best <- which.max(scores)
cat("best_start=", best, "\n", sep = "")
cat(sprintf("best_score=%.2f", scores[best]))
""",
            """best_start=4
best_score=3.00""",
            _t(
                "La ventana AILM inicia en la posición cuatro y maximiza la escala ilustrativa; no confirma por sí sola una hélice transmembrana.",
                "The AILM window starts at position four and maximizes the illustrative scale; it does not by itself confirm a transmembrane helix.",
                "AILM-vinduet starter ved position fire og maksimerer den illustrative skala; det bekræfter ikke i sig selv en transmembranhelix.",
            ),
        ),
    ),
    practices=(
        (
            "m07.p01",
            "PIPELINE_DESIGN",
            _t(
                "Diseña una ficha de identidad para caracterizar una proteína humana.",
                "Design an identity record for characterizing a human protein.",
                "Design en identitetsregistrering til karakterisering af et humant protein.",
            ),
            (
                _t(
                    "Incluye accession, isoforma y versión.",
                    "Include accession, isoform, and version.",
                    "Medtag accession, isoform og version.",
                ),
                _t(
                    "Incluye checksum del FASTA.",
                    "Include a FASTA checksum.",
                    "Medtag FASTA-checksum.",
                ),
            ),
            _t(
                "La ficha contiene accession y versión, nombre, especie y taxón, isoforma, longitud, secuencia exacta, checksum, fecha y fuente. Registra cualquier conversión de identificadores y conserva el FASTA como entrada inmutable.",
                "The record contains accession and version, name, species and taxon, isoform, length, exact sequence, checksum, date, and source. It records identifier conversion and retains FASTA as immutable input.",
                "Registreringen indeholder accession og version, navn, art og taxon, isoform, længde, præcis sekvens, checksum, dato og kilde. Den registrerer identifikatorkonvertering og bevarer FASTA som uforanderligt input.",
            ),
            _t(
                "Sin identidad exacta, los resultados de herramientas no son comparables.",
                "Without exact identity, tool results are not comparable.",
                "Uden præcis identitet er værktøjsresultater ikke sammenlignelige.",
            ),
            "",
        ),
        (
            "m07.p02",
            "DATA_INTERPRETATION",
            _t(
                "InterPro devuelve dos dominios solapados de bases integrantes diferentes. ¿Cómo lo interpretas?",
                "InterPro returns two overlapping domains from different member databases. How do you interpret them?",
                "InterPro returnerer to overlappende domæner fra forskellige medlemsdatabaser. Hvordan fortolkes de?",
            ),
            (
                _t(
                    "Revisa modelos, coordenadas y jerarquía.",
                    "Review models, coordinates, and hierarchy.",
                    "Gennemgå modeller, koordinater og hierarki.",
                ),
                _t(
                    "No cuentes automáticamente dos dominios físicos.",
                    "Do not automatically count two physical domains.",
                    "Tæl ikke automatisk to fysiske domæner.",
                ),
            ),
            _t(
                "Los matches pueden representar firmas alternativas o niveles jerárquicos de la misma región. Se revisan modelo, miembro, score, integración InterPro, coordenadas y arquitectura completa. El solapamiento no demuestra dos unidades estructurales independientes.",
                "Matches may represent alternative signatures or hierarchical levels for the same region. Review model, member, score, InterPro integration, coordinates, and complete architecture. Overlap does not prove two independent structural units.",
                "Matches kan repræsentere alternative signaturer eller hierarkiske niveauer for samme region. Gennemgå model, medlem, score, InterPro-integration, koordinater og komplet arkitektur. Overlap beviser ikke to uafhængige strukturelle enheder.",
            ),
            _t(
                "La arquitectura integrada prevalece sobre contar etiquetas.",
                "Integrated architecture is more informative than counting labels.",
                "Integreret arkitektur er mere informativ end at tælle labels.",
            ),
            "",
        ),
        (
            "m07.p03",
            "DEBUGGING",
            _t(
                "Un analista usa una estructura de otra isoforma y mapea una mutación por número. Reconstruye el error.",
                "An analyst uses a structure from another isoform and maps a mutation by residue number. Reconstruct the error.",
                "En analytiker bruger en struktur fra en anden isoform og mapper en mutation efter restnummer. Rekonstruér fejlen.",
            ),
            (
                _t(
                    "La numeración puede desplazarse.",
                    "Numbering may shift.",
                    "Nummerering kan forskydes.",
                ),
                _t(
                    "Alinea secuencias y cobertura.",
                    "Align sequences and coverage.",
                    "Afstem sekvenser og dækning.",
                ),
            ),
            _t(
                "El mismo número no garantiza el mismo residuo entre isoformas o constructs. Debe alinearse la secuencia de referencia con la cadena estructural, verificar identidad, inserciones, deleciones, constructo y residuos no modelados, y reportar la numeración en ambos sistemas.",
                "The same number does not guarantee the same residue across isoforms or constructs. Align the reference sequence to the structural chain, verify identity, insertions, deletions, construct, and unmodeled residues, and report numbering in both systems.",
                "Samme nummer garanterer ikke samme rest på tværs af isoformer eller constructs. Afstem referencesekvensen med strukturkæden, verificér identitet, insertioner, deletioner, construct og ikke-modellerede rester, og rapportér nummerering i begge systemer.",
            ),
            _t(
                "La posición estructural es una relación de alineamiento, no una coincidencia numérica.",
                "Structural position is an alignment relationship, not numeric coincidence.",
                "Strukturel position er en alignmentrelation, ikke numerisk tilfældighed.",
            ),
            "",
        ),
        (
            "m07.p04",
            "SHORT_ANSWER",
            _t(
                "Distingue evidencia reviewed, transferencia por similitud y predicción.",
                "Distinguish reviewed evidence, similarity transfer, and prediction.",
                "Skeln mellem reviewed evidens, lighedsoverførsel og prædiktion.",
            ),
            (
                _t(
                    "Describe procedencia y fuerza.",
                    "Describe provenance and strength.",
                    "Beskriv proveniens og styrke.",
                ),
                _t(
                    "No conviertas reviewed en experimental para cada detalle.",
                    "Do not turn reviewed into experimental evidence for every detail.",
                    "Gør ikke reviewed til eksperimentel evidens for hver detalje.",
                ),
            ),
            _t(
                "Reviewed indica curación experta de la entrada, pero cada afirmación conserva su evidencia. Transferencia por similitud infiere función desde homólogos y depende de ortología, cobertura y conservación. Predicción deriva de un modelo computacional y requiere validación. Las tres categorías deben citar fuente y código de evidencia.",
                "Reviewed indicates expert curation of the entry, but each statement retains its own evidence. Similarity transfer infers function from homologues and depends on orthology, coverage, and conservation. Prediction derives from a computational model and requires validation. All three categories require source and evidence code.",
                "Reviewed angiver ekspertkuratering af indgangen, men hver påstand bevarer sin egen evidens. Lighedsoverførsel udleder funktion fra homologer og afhænger af ortologi, dækning og konservering. Prædiktion kommer fra en computational model og kræver validering. Alle tre kategorier kræver kilde og evidenskode.",
            ),
            _t(
                "Curación y evidencia directa son dimensiones relacionadas pero distintas.",
                "Curation and direct evidence are related but distinct dimensions.",
                "Kuratering og direkte evidens er relaterede men forskellige dimensioner.",
            ),
            "",
        ),
        (
            "m07.p05",
            "CODE_COMPLETION",
            _t(
                "Completa una función que valide un alfabeto proteico estándar.",
                "Complete a function validating the standard protein alphabet.",
                "Færdiggør en funktion, der validerer standardproteinalfabetet.",
            ),
            (
                _t(
                    "Divide la cadena en residuos.",
                    "Split the string into residues.",
                    "Opdel strengen i rester.",
                ),
                _t(
                    "Devuelve un único lógico.",
                    "Return one logical value.",
                    "Returnér én logisk værdi.",
                ),
            ),
            _t(
                "valid_protein <- function(sequence) { residues <- strsplit(sequence, '', fixed = TRUE)[[1]]; all(residues %in% strsplit('ACDEFGHIKLMNPQRSTVWY', '', fixed = TRUE)[[1]]) }",
                "valid_protein <- function(sequence) { residues <- strsplit(sequence, '', fixed = TRUE)[[1]]; all(residues %in% strsplit('ACDEFGHIKLMNPQRSTVWY', '', fixed = TRUE)[[1]]) }",
                "valid_protein <- function(sequence) { residues <- strsplit(sequence, '', fixed = TRUE)[[1]]; all(residues %in% strsplit('ACDEFGHIKLMNPQRSTVWY', '', fixed = TRUE)[[1]]) }",
            ),
            _t(
                "La función valida el alfabeto, pero la identidad y versión requieren metadata adicional.",
                "The function validates the alphabet, but identity and version require additional metadata.",
                "Funktionen validerer alfabetet, men identitet og version kræver yderligere metadata.",
            ),
            "valid_protein <- function(sequence) {\n  # return TRUE only for standard residues\n}",
        ),
        (
            "m07.p06",
            "ORAL_EXPLANATION",
            _t(
                "Prepara una explicación de 90 segundos: ¿qué puede y qué no puede demostrar AlphaFold?",
                "Prepare a 90-second explanation: what can and cannot AlphaFold demonstrate?",
                "Forbered en 90-sekunders forklaring: hvad kan og kan AlphaFold ikke demonstrere?",
            ),
            (
                _t(
                    "Incluye confianza local y contexto.",
                    "Include local confidence and context.",
                    "Medtag lokal confidence og kontekst.",
                ),
                _t(
                    "Distingue estructura de función.",
                    "Distinguish structure from function.",
                    "Skeln mellem struktur og funktion.",
                ),
            ),
            _t(
                "AlphaFold predice una conformación plausible y confianza local a partir de secuencia y aprendizaje previo. Puede apoyar hipótesis sobre pliegue, dominios o residuos estructurados. No demuestra ensamblaje fisiológico, ligandos, dinámica, estado activo, interacción ni mecanismo; regiones de baja confianza requieren cautela y toda afirmación funcional necesita evidencia independiente.",
                "AlphaFold predicts a plausible conformation and local confidence from sequence and prior learning. It can support hypotheses about fold, domains, or structured residues. It does not demonstrate physiological assembly, ligands, dynamics, active state, interaction, or mechanism; low-confidence regions require caution, and every functional claim needs independent evidence.",
                "AlphaFold prædikterer en plausibel konformation og lokal confidence fra sekvens og tidligere læring. Det kan understøtte hypoteser om fold, domæner eller strukturerede rester. Det demonstrerer ikke fysiologisk assembly, ligander, dynamik, aktiv tilstand, interaktion eller mekanisme; lav-confidence-regioner kræver forsigtighed, og enhver funktionel påstand kræver uafhængig evidens.",
            ),
            _t(
                "La respuesta separa modelo, confianza, hipótesis y validación.",
                "The answer separates model, confidence, hypothesis, and validation.",
                "Svaret adskiller model, confidence, hypotese og validering.",
            ),
            "",
        ),
    ),
    mcqs=(
        _mcq(
            "q01",
            _t(
                "¿Qué forma parte de la identidad analítica de una proteína?",
                "What is part of protein analytical identity?",
                "Hvad er del af et proteins analytiske identitet?",
            ),
            (
                _option(
                    "a",
                    _t(
                        "Accession, versión, especie e isoforma",
                        "Accession, version, species, and isoform",
                        "Accession, version, art og isoform",
                    ),
                ),
                _option("b", _t("Sólo nombre común", "Only common name", "Kun almindeligt navn")),
                _option("c", _t("Sólo longitud", "Only length", "Kun længde")),
                _option("d", _t("Color estructural", "Structure color", "Strukturfarve")),
            ),
            "a",
            _t(
                "La misma etiqueta puede representar secuencias distintas.",
                "The same label may represent different sequences.",
                "Samme label kan repræsentere forskellige sekvenser.",
            ),
        ),
        _mcq(
            "q02",
            _t(
                "¿Qué es una fracción hidrofóbica calculada?",
                "What is a calculated hydrophobic fraction?",
                "Hvad er en beregnet hydrofob fraktion?",
            ),
            (
                _option(
                    "a",
                    _t(
                        "Descriptor bajo una definición declarada",
                        "A descriptor under a declared definition",
                        "En deskriptor under en deklareret definition",
                    ),
                ),
                _option(
                    "b",
                    _t(
                        "Prueba de membrana",
                        "Proof of membrane localization",
                        "Bevis for membranlokalisering",
                    ),
                ),
                _option("c", _t("Resolución PDB", "PDB resolution", "PDB-opløsning")),
                _option("d", _t("Código de evidencia", "Evidence code", "Evidenskode")),
            ),
            "a",
            _t(
                "La propiedad genera hipótesis, no confirmación experimental.",
                "The property generates hypotheses, not experimental confirmation.",
                "Egenskaben genererer hypoteser, ikke eksperimentel bekræftelse.",
            ),
        ),
        _mcq(
            "q03",
            _t(
                "¿Qué integra InterPro?",
                "What does InterPro integrate?",
                "Hvad integrerer InterPro?",
            ),
            (
                _option(
                    "a",
                    _t(
                        "Firmas de familias, dominios, repeticiones y sitios",
                        "Family, domain, repeat, and site signatures",
                        "Signaturer for familier, domæner, repeats og sites",
                    ),
                ),
                _option("b", _t("Sólo estructuras", "Only structures", "Kun strukturer")),
                _option("c", _t("Sólo publicaciones", "Only publications", "Kun publikationer")),
                _option("d", _t("Sólo expresión", "Only expression", "Kun ekspression")),
            ),
            "a",
            _t(
                "Integra múltiples bases miembro y modelos de firma.",
                "It integrates multiple member databases and signature models.",
                "Det integrerer flere medlemsdatabaser og signaturmodeller.",
            ),
        ),
        _mcq(
            "q04",
            _t(
                "¿Qué debe acompañar una anotación funcional?",
                "What should accompany a functional annotation?",
                "Hvad bør ledsage en funktionel annotering?",
            ),
            (
                _option(
                    "a",
                    _t(
                        "Procedencia y evidencia",
                        "Provenance and evidence",
                        "Proveniens og evidens",
                    ),
                ),
                _option("b", _t("Sólo nombre", "Only name", "Kun navn")),
                _option("c", _t("Sólo color", "Only color", "Kun farve")),
                _option("d", _t("Sólo longitud", "Only length", "Kun længde")),
            ),
            "a",
            _t(
                "La fuerza de la afirmación depende de cómo se obtuvo.",
                "Claim strength depends on how it was obtained.",
                "Påstandens styrke afhænger af hvordan den blev opnået.",
            ),
        ),
        _mcq(
            "q05",
            _t(
                "¿Qué debe revisarse en una estructura PDB?",
                "What should be reviewed in a PDB structure?",
                "Hvad bør gennemgås i en PDB-struktur?",
            ),
            (
                _option(
                    "a",
                    _t(
                        "Método, calidad, constructo, ligandos y cobertura",
                        "Method, quality, construct, ligands, and coverage",
                        "Metode, kvalitet, construct, ligander og dækning",
                    ),
                ),
                _option("b", _t("Sólo imagen", "Only image", "Kun billede")),
                _option("c", _t("Sólo título", "Only title", "Kun titel")),
                _option("d", _t("Sólo cadena A", "Only chain A", "Kun kæde A")),
            ),
            "a",
            _t(
                "La estructura puede representar sólo parte o una condición artificial.",
                "A structure may represent only a portion or artificial condition.",
                "En struktur kan repræsentere kun en del eller en kunstig betingelse.",
            ),
        ),
        _mcq(
            "q06",
            _t(
                "¿Qué indica baja confianza estructural predicha?",
                "What does low predicted structural confidence indicate?",
                "Hvad angiver lav prædikteret strukturel confidence?",
            ),
            (
                _option(
                    "a",
                    _t(
                        "La geometría local es incierta o contextual",
                        "Local geometry is uncertain or contextual",
                        "Lokal geometri er usikker eller kontekstuel",
                    ),
                ),
                _option("b", _t("Función falsa", "False function", "Falsk funktion")),
                _option(
                    "c",
                    _t(
                        "Secuencia inválida siempre",
                        "Always invalid sequence",
                        "Altid ugyldig sekvens",
                    ),
                ),
                _option("d", _t("Ausencia de proteína", "Protein absence", "Fravær af protein")),
            ),
            "a",
            _t(
                "Puede reflejar desorden o dependencia de interacción.",
                "It may reflect disorder or interaction dependence.",
                "Det kan afspejle uorden eller interaktionsafhængighed.",
            ),
        ),
        _mcq(
            "q07",
            _t(
                "¿Qué prueba un modelo monomérico?",
                "What does a monomeric model prove?",
                "Hvad beviser en monomerisk model?",
            ),
            (
                _option(
                    "a",
                    _t(
                        "No prueba el ensamblaje fisiológico",
                        "It does not prove physiological assembly",
                        "Det beviser ikke fysiologisk assembly",
                    ),
                ),
                _option(
                    "b",
                    _t("Interacción obligatoria", "Obligate interaction", "Obligat interaktion"),
                ),
                _option("c", _t("Estado activo", "Active state", "Aktiv tilstand")),
                _option("d", _t("Afinidad", "Affinity", "Affinitet")),
            ),
            "a",
            _t(
                "El ensamblaje requiere evidencia adicional.",
                "Assembly requires additional evidence.",
                "Assembly kræver yderligere evidens.",
            ),
        ),
        _mcq(
            "q08",
            _t(
                "¿Qué evita errores al mapear una mutación?",
                "What prevents mutation-mapping errors?",
                "Hvad forhindrer fejl ved mutationsmapping?",
            ),
            (
                _option(
                    "a",
                    _t(
                        "Alinear secuencia de referencia y cadena estructural",
                        "Align reference sequence and structural chain",
                        "Afstem referencesekvens og strukturkæde",
                    ),
                ),
                _option("b", _t("Usar mismo número", "Use the same number", "Brug samme nummer")),
                _option("c", _t("Ignorar isoformas", "Ignore isoforms", "Ignorér isoformer")),
                _option("d", _t("Cambiar color", "Change color", "Skift farve")),
            ),
            "a",
            _t(
                "La numeración depende de isoforma, constructo y residuos modelados.",
                "Numbering depends on isoform, construct, and modeled residues.",
                "Nummerering afhænger af isoform, construct og modellerede rester.",
            ),
        ),
    ),
    true_false=(
        _tf(
            "tf01",
            _t(
                "El nombre de proteína identifica siempre una secuencia única.",
                "A protein name always identifies one unique sequence.",
                "Et proteinnavn identificerer altid én unik sekvens.",
            ),
            False,
            _t(
                "Puede haber especies, isoformas y versiones.",
                "Species, isoforms, and versions may differ.",
                "Arter, isoformer og versioner kan variere.",
            ),
        ),
        _tf(
            "tf02",
            _t(
                "El FASTA exacto debe conservarse.",
                "The exact FASTA should be retained.",
                "Den præcise FASTA bør bevares.",
            ),
            True,
            _t(
                "Es la entrada reproducible del análisis.",
                "It is the reproducible analysis input.",
                "Det er analysens reproducerbare input.",
            ),
        ),
        _tf(
            "tf03",
            _t(
                "La hidropatía confirma localización transmembrana.",
                "Hydropathy confirms transmembrane localization.",
                "Hydropati bekræfter transmembranlokalisering.",
            ),
            False,
            _t(
                "Es una predicción dependiente de escala y ventana.",
                "It is a scale- and window-dependent prediction.",
                "Det er en skala- og vinduesafhængig prædiktion.",
            ),
        ),
        _tf(
            "tf04",
            _t(
                "Dominios solapados pueden ser firmas alternativas de la misma región.",
                "Overlapping domains may be alternative signatures of the same region.",
                "Overlappende domæner kan være alternative signaturer for samme region.",
            ),
            True,
            _t(
                "Debe revisarse la integración y arquitectura.",
                "Integration and architecture should be reviewed.",
                "Integration og arkitektur bør gennemgås.",
            ),
        ),
        _tf(
            "tf05",
            _t(
                "Reviewed significa que cada afirmación tiene evidencia experimental directa.",
                "Reviewed means every statement has direct experimental evidence.",
                "Reviewed betyder at hver påstand har direkte eksperimentel evidens.",
            ),
            False,
            _t(
                "La entrada está curada, pero las afirmaciones conservan evidencias distintas.",
                "The entry is curated, but statements retain different evidence.",
                "Indgangen er kurateret, men påstande bevarer forskellig evidens.",
            ),
        ),
        _tf(
            "tf06",
            _t(
                "Una estructura puede cubrir sólo parte de la proteína.",
                "A structure may cover only part of a protein.",
                "En struktur kan dække kun en del af et protein.",
            ),
            True,
            _t(
                "Constructs y residuos no modelados limitan cobertura.",
                "Constructs and unmodeled residues limit coverage.",
                "Constructs og ikke-modellerede rester begrænser dækning.",
            ),
        ),
        _tf(
            "tf07",
            _t(
                "AlphaFold demuestra mecanismo funcional.",
                "AlphaFold demonstrates functional mechanism.",
                "AlphaFold demonstrerer funktionel mekanisme.",
            ),
            False,
            _t(
                "Predice estructura; mecanismo requiere evidencia adicional.",
                "It predicts structure; mechanism requires additional evidence.",
                "Det prædikterer struktur; mekanisme kræver yderligere evidens.",
            ),
        ),
        _tf(
            "tf08",
            _t(
                "La numeración debe verificarse entre isoforma y estructura.",
                "Numbering should be verified between isoform and structure.",
                "Nummerering bør verificeres mellem isoform og struktur.",
            ),
            True,
            _t(
                "Inserciones, deleciones y constructs pueden desplazar posiciones.",
                "Insertions, deletions, and constructs may shift positions.",
                "Insertioner, deletioner og constructs kan forskyde positioner.",
            ),
        ),
    ),
    tutor=(
        _t(
            "El tutor debe comenzar por identidad exacta y procedencia, y separar descriptores, anotación, estructura predicha y evidencia experimental.",
            "The tutor should begin with exact identity and provenance and separate descriptors, annotation, predicted structure, and experimental evidence.",
            "Tutoren bør begynde med præcis identitet og proveniens og adskille deskriptorer, annotering, prædikteret struktur og eksperimentel evidens.",
        ),
        (
            _t(
                "Accession, versión, especie e isoforma son obligatorios.",
                "Accession, version, species, and isoform are required.",
                "Accession, version, art og isoform er påkrævede.",
            ),
            _t(
                "Propiedades calculadas generan hipótesis.",
                "Calculated properties generate hypotheses.",
                "Beregnede egenskaber genererer hypoteser.",
            ),
            _t(
                "Anotaciones requieren códigos de evidencia.",
                "Annotations require evidence codes.",
                "Annoteringer kræver evidenskoder.",
            ),
            _t(
                "Estructuras requieren cobertura y confianza.",
                "Structures require coverage and confidence.",
                "Strukturer kræver dækning og confidence.",
            ),
        ),
        (
            _t(
                "Confundir nombre con secuencia única.",
                "Confuse a name with a unique sequence.",
                "Forveksl et navn med en unik sekvens.",
            ),
            _t(
                "Tratar predicción como medición.",
                "Treat prediction as measurement.",
                "Behandl prædiktion som måling.",
            ),
            _t(
                "Contar matches solapados como dominios independientes.",
                "Count overlapping matches as independent domains.",
                "Tæl overlappende matches som uafhængige domæner.",
            ),
            _t(
                "Inferir función desde una imagen estructural.",
                "Infer function from a structure image.",
                "Udled funktion fra et strukturbillede.",
            ),
        ),
        (
            _t(
                "¿Cuál es la secuencia exacta?",
                "What is the exact sequence?",
                "Hvad er den præcise sekvens?",
            ),
            _t(
                "¿Qué escala y supuestos usa el descriptor?",
                "Which scale and assumptions does the descriptor use?",
                "Hvilken skala og hvilke antagelser bruger deskriptoren?",
            ),
            _t(
                "¿Qué evidencia sostiene la anotación?",
                "Which evidence supports the annotation?",
                "Hvilken evidens understøtter annoteringen?",
            ),
            _t(
                "¿Qué residuos cubre la estructura?",
                "Which residues does the structure cover?",
                "Hvilke rester dækker strukturen?",
            ),
        ),
        (
            _t(
                "Valida identidad y secuencia.",
                "Validates identity and sequence.",
                "Validerer identitet og sekvens.",
            ),
            _t(
                "Interpreta propiedades con límites.",
                "Interprets properties with limits.",
                "Fortolker egenskaber med grænser.",
            ),
            _t(
                "Integra dominios y evidencia.",
                "Integrates domains and evidence.",
                "Integrerer domæner og evidens.",
            ),
            _t(
                "Evalúa estructura y cobertura.",
                "Evaluates structure and coverage.",
                "Vurderer struktur og dækning.",
            ),
        ),
        (
            _t(
                "No inventar resultados de InterPro, UniProt, PDB o AlphaFold.",
                "Do not invent InterPro, UniProt, PDB, or AlphaFold results.",
                "Opfind ikke InterPro-, UniProt-, PDB- eller AlphaFold-resultater.",
            ),
            _t(
                "No atribuir causalidad desde predicciones.",
                "Do not assign causality from predictions.",
                "Tildel ikke kausalitet fra prædiktioner.",
            ),
            _t(
                "No ocultar isoformas o cobertura parcial.",
                "Do not hide isoforms or partial coverage.",
                "Skjul ikke isoformer eller delvis dækning.",
            ),
            _t(
                "Responder en el idioma activo y conservar identificadores.",
                "Respond in the active language and preserve identifiers.",
                "Svar på det aktive sprog og bevar identifikatorer.",
            ),
        ),
        (
            "https://www.ebi.ac.uk/interpro/",
            "https://www.uniprot.org/help/uniprotkb",
            "https://www.rcsb.org/",
            "https://alphafold.ebi.ac.uk/",
        ),
    ),
)

LOCALIZED_MODULE_07_PROTEIN_CHARACTERIZATION = build_module(_SPEC)
LOCALIZED_OBJECTIVE_QUESTION_BANK_07 = build_question_bank(_SPEC)


def materialize_module_07_question_bank(
    locale: AppLocale | str = AppLocale.SPANISH_SPAIN,
) -> tuple[AssessmentItem, ...]:
    """Materialize the stable module 7 objective bank."""

    return materialize_bank(LOCALIZED_OBJECTIVE_QUESTION_BANK_07, locale)


MODULE_07_PROTEIN_CHARACTERIZATION: LearningModule = (
    LOCALIZED_MODULE_07_PROTEIN_CHARACTERIZATION.materialize(AppLocale.SPANISH_SPAIN)
)
OBJECTIVE_QUESTION_BANK_07 = materialize_module_07_question_bank()

__all__ = [
    "LOCALIZED_MODULE_07_PROTEIN_CHARACTERIZATION",
    "LOCALIZED_OBJECTIVE_QUESTION_BANK_07",
    "MODULE_07_PROTEIN_CHARACTERIZATION",
    "OBJECTIVE_QUESTION_BANK_07",
    "materialize_module_07_question_bank",
]
