"""BMB831 module 8: biological interpretation, enrichment, and evidence."""

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
    module_id="bmb831.m08",
    title=_t(
        "Interpretación biológica, enriquecimiento y evidencia",
        "Biological interpretation, enrichment, and evidence",
        "Biologisk fortolkning, enrichment og evidens",
    ),
    summary=_t(
        "Convierte resultados estadísticos en hipótesis biológicas mediante mapeo de identificadores, universos explícitos, enriquecimiento y redes, controlando multiplicidad, redundancia, circularidad y fuerza de la evidencia.",
        "Turn statistical results into biological hypotheses through identifier mapping, explicit universes, enrichment, and networks while controlling multiplicity, redundancy, circularity, and evidence strength.",
        "Omsæt statistiske resultater til biologiske hypoteser gennem identifikatormapping, eksplicitte universer, enrichment og netværk med kontrol af multiplicitet, redundans, cirkularitet og evidensstyrke.",
    ),
    objectives=(
        (
            "m08.o1",
            _t(
                "Auditar mapeo de identificadores, especie, versión, pérdidas y relaciones uno-a-muchos.",
                "Audit identifier mapping, species, version, losses, and one-to-many relations.",
                "Auditere identifikatormapping, art, version, tab og en-til-mange-relationer.",
            ),
        ),
        (
            "m08.o2",
            _t(
                "Elegir y justificar universo, análisis de sobrerrepresentación o método basado en ranking.",
                "Choose and justify a universe, over-representation analysis, or rank-based method.",
                "Vælge og begrunde univers, over-representation-analyse eller rankingbaseret metode.",
            ),
        ),
        (
            "m08.o3",
            _t(
                "Interpretar pathways, ontologías y redes considerando multiplicidad, redundancia, dirección y genes conductores.",
                "Interpret pathways, ontologies, and networks considering multiplicity, redundancy, direction, and driver genes.",
                "Fortolke pathways, ontologier og netværk med hensyn til multiplicitet, redundans, retning og drivende gener.",
            ),
        ),
        (
            "m08.o4",
            _t(
                "Limitar afirmaciones biológicas mediante jerarquía de evidencia, validación y detección de circularidad.",
                "Limit biological claims through evidence hierarchy, validation, and detection of circularity.",
                "Begrænse biologiske påstande gennem evidenshierarki, validering og detektion af cirkularitet.",
            ),
        ),
    ),
    concepts=(
        (
            "identifier-universe",
            _t(
                "Identificadores y universo",
                "Identifiers and universe",
                "Identifikatorer og univers",
            ),
            _t(
                "El mapeo entre Ensembl, Entrez, UniProt y símbolos depende de especie, versión y tipo de feature. Deben contarse IDs sin mapear, duplicados y relaciones uno-a-muchos antes de enrichment. El universo no es todo el genoma por defecto: representa las features que podían observarse y probarse después de filtros técnicos independientes del resultado. Cambiar el universo cambia la hipótesis nula.",
                "Mapping among Ensembl, Entrez, UniProt, and symbols depends on species, version, and feature type. Unmapped IDs, duplicates, and one-to-many relations must be counted before enrichment. The universe is not the entire genome by default: it represents features that could be observed and tested after outcome-independent technical filtering. Changing the universe changes the null hypothesis.",
                "Mapping mellem Ensembl, Entrez, UniProt og symboler afhænger af art, version og featuretype. Ikke-mappede ID'er, dubletter og en-til-mange-relationer skal tælles før enrichment. Universet er ikke hele genomet som standard: det repræsenterer features, der kunne observeres og testes efter outcome-uafhængig teknisk filtrering. Et andet univers ændrer nulhypotesen.",
            ),
            (
                _t(
                    "Conserva una tabla de mapeo con estado y procedencia.",
                    "Retain a mapping table with status and provenance.",
                    "Bevar en mappingtabel med status og proveniens.",
                ),
                _t(
                    "Declara la unidad: gen, transcrito, proteína o protein group.",
                    "Declare the unit: gene, transcript, protein, or protein group.",
                    "Deklarér enheden: gen, transkript, protein eller protein group.",
                ),
            ),
        ),
        (
            "ora-ranked",
            _t(
                "Sobrerrepresentación y ranking",
                "Over-representation and ranking",
                "Over-representation og ranking",
            ),
            _t(
                "ORA compara una lista seleccionada con un universo mediante una tabla de contingencia o distribución hipergeométrica. Depende de un umbral de selección y pierde información de ranking. Los métodos rank-based utilizan una estadística ordenada de todas las features y preguntan si un conjunto se concentra en extremos. Requieren una métrica con dirección consistente y una estrategia válida para empates, correlación y permutaciones.",
                "ORA compares a selected list with a universe using a contingency table or hypergeometric distribution. It depends on a selection threshold and discards ranking information. Rank-based methods use an ordered statistic for all features and ask whether a set concentrates at the extremes. They require a consistently directed metric and a valid strategy for ties, correlation, and permutations.",
                "ORA sammenligner en udvalgt liste med et univers ved hjælp af en kontingenstabel eller hypergeometrisk fordeling. Den afhænger af en selektionstærskel og kasserer rankinginformation. Rankingbaserede metoder bruger en ordnet statistik for alle features og spørger om et sæt koncentreres i yderpunkterne. De kræver en konsistent retningsbestemt metrisk og en gyldig strategi for ties, korrelation og permutationer.",
            ),
            (
                _t(
                    "El método debe coincidir con la forma del resultado disponible.",
                    "The method must match the form of the available result.",
                    "Metoden skal matche formen af det tilgængelige resultat.",
                ),
                _t(
                    "No uses sólo genes significativos cuando la pregunta es sobre señal distribuida.",
                    "Do not use only significant genes when the question concerns distributed signal.",
                    "Brug ikke kun signifikante gener, når spørgsmålet handler om distribueret signal.",
                ),
            ),
        ),
        (
            "redundancy-direction",
            _t(
                "Redundancia, dirección y genes conductores",
                "Redundancy, direction, and driver genes",
                "Redundans, retning og drivende gener",
            ),
            _t(
                "Pathways y términos comparten genes y jerarquías, por lo que múltiples resultados pueden representar la misma señal. El ajuste de multiplicidad no elimina redundancia semántica. Deben examinarse tamaños de conjunto, solapamiento, dirección, leading edge y genes que contribuyen. Resumir términos puede mejorar comunicación, pero la regla debe ser reproducible y no ocultar resultados discordantes.",
                "Pathways and terms share genes and hierarchies, so multiple results may represent the same signal. Multiplicity adjustment does not remove semantic redundancy. Set sizes, overlap, direction, leading edge, and contributing genes should be examined. Summarizing terms may improve communication, but the rule must be reproducible and must not hide discordant results.",
                "Pathways og termer deler gener og hierarkier, så flere resultater kan repræsentere samme signal. Multiplicitetsjustering fjerner ikke semantisk redundans. Sætstørrelser, overlap, retning, leading edge og bidragende gener bør undersøges. Opsummering af termer kan forbedre kommunikationen, men reglen skal være reproducerbar og må ikke skjule uoverensstemmende resultater.",
            ),
            (
                _t(
                    "Relaciona cada término con sus features conductoras.",
                    "Relate every term to its driver features.",
                    "Relatér hver term til dens drivende features.",
                ),
                _t(
                    "Separa actividad inferida de expresión individual.",
                    "Separate inferred activity from individual expression.",
                    "Adskil infereret aktivitet fra individuel ekspression.",
                ),
            ),
        ),
        (
            "evidence-circularity",
            _t(
                "Evidencia, redes y circularidad",
                "Evidence, networks, and circularity",
                "Evidens, netværk og cirkularitet",
            ),
            _t(
                "Una asociación de pathway no demuestra activación, mecanismo ni causalidad. Las bases pueden derivar de experimentos, curación, predicción o literatura y contener sesgos de estudio. Las redes añaden conocimiento previo y pueden resaltar módulos, pero seleccionar genes por una base y validar con la misma base es circular. La interpretación madura integra dirección estadística, evidencia molecular independiente, replicación y límites del modelo.",
                "A pathway association does not demonstrate activation, mechanism, or causality. Databases may derive from experiments, curation, prediction, or literature and contain study bias. Networks add prior knowledge and may highlight modules, but selecting genes from one database and validating with the same database is circular. Mature interpretation integrates statistical direction, independent molecular evidence, replication, and model limits.",
                "En pathway-association demonstrerer ikke aktivering, mekanisme eller kausalitet. Databaser kan stamme fra eksperimenter, kuratering, prædiktion eller litteratur og indeholde studiebias. Netværk tilføjer prior viden og kan fremhæve moduler, men valg af gener fra én database og validering med samme database er cirkulært. Moden fortolkning integrerer statistisk retning, uafhængig molekylær evidens, replikation og modelgrænser.",
            ),
            (
                _t(
                    "Declara la procedencia de cada recurso biológico.",
                    "Declare provenance for every biological resource.",
                    "Deklarér proveniens for hver biologisk ressource.",
                ),
                _t(
                    "Busca validación que no reutilice la misma información previa.",
                    "Seek validation that does not reuse the same prior information.",
                    "Søg validering, der ikke genbruger samme prior-information.",
                ),
            ),
        ),
    ),
    examples=(
        (
            "m08.e01",
            _t(
                "Calcular sobrerrepresentación hipergeométrica",
                "Calculate hypergeometric over-representation",
                "Beregn hypergeometrisk over-representation",
            ),
            _t(
                "Evalúa tres o más genes seleccionados de un pathway de cinco dentro de un universo de veinte.",
                "Evaluate three or more selected genes from a five-gene pathway within a universe of twenty.",
                "Vurdér tre eller flere udvalgte gener fra et pathway med fem gener i et univers på tyve.",
            ),
            (
                _t(
                    "El universo contiene veinte genes medibles.",
                    "The universe contains twenty measurable genes.",
                    "Universet indeholder tyve målbare gener.",
                ),
                _t(
                    "La lista seleccionada contiene cuatro genes.",
                    "The selected list contains four genes.",
                    "Den udvalgte liste indeholder fire gener.",
                ),
                _t(
                    "Tres genes seleccionados pertenecen al pathway.",
                    "Three selected genes belong to the pathway.",
                    "Tre udvalgte gener tilhører pathwayet.",
                ),
            ),
            """universe_size <- 20
pathway_size <- 5
selected_size <- 4
overlap <- 3
p_value <- phyper(
  overlap - 1,
  pathway_size,
  universe_size - pathway_size,
  selected_size,
  lower.tail = FALSE
)
cat(sprintf("ora_p=%.4f", p_value))
""",
            "ora_p=0.0320",
            _t(
                "Bajo este universo y selección, observar al menos tres genes del pathway tiene probabilidad aproximada 0.032 bajo la hipótesis nula; todavía requiere multiplicidad y contexto.",
                "Under this universe and selection, observing at least three pathway genes has probability about 0.032 under the null; multiplicity and context are still required.",
                "Under dette univers og denne selektion har observation af mindst tre pathway-gener sandsynlighed cirka 0,032 under nulhypotesen; multiplicitet og kontekst kræves stadig.",
            ),
        ),
        (
            "m08.e02",
            _t(
                "Resumir señal en un ranking",
                "Summarize signal in a ranking",
                "Opsummér signal i en ranking",
            ),
            _t(
                "Compara la media de una métrica dirigida dentro y fuera de un conjunto.",
                "Compare the mean of a directed metric inside and outside a set.",
                "Sammenlign middelværdien af en retningsbestemt metrisk inden for og uden for et sæt.",
            ),
            (
                _t(
                    "La métrica positiva representa una dirección declarada.",
                    "Positive metric values represent a declared direction.",
                    "Positive metrikværdier repræsenterer en deklareret retning.",
                ),
                _t(
                    "El ejemplo no sustituye un test de enriquecimiento validado.",
                    "The example does not replace a validated enrichment test.",
                    "Eksemplet erstatter ikke en valideret enrichment-test.",
                ),
                _t(
                    "La tabla completa permanece disponible.",
                    "The full table remains available.",
                    "Hele tabellen forbliver tilgængelig.",
                ),
            ),
            """statistic <- c(G1 = 3, G2 = 2, G3 = -1, G4 = -2)
gene_set <- c("G1", "G2")
inside <- mean(statistic[names(statistic) %in% gene_set])
outside <- mean(statistic[!names(statistic) %in% gene_set])
cat(sprintf("inside_mean=%.1f\n", inside))
cat(sprintf("outside_mean=%.1f\n", outside))
cat(sprintf("contrast=%.1f", inside - outside))
""",
            """inside_mean=2.5
outside_mean=-1.5
contrast=4.0""",
            _t(
                "El conjunto se concentra en valores positivos en este fixture; una inferencia formal debe considerar ranking completo, tamaño, correlación y permutación.",
                "The set concentrates at positive values in this fixture; formal inference must consider the full ranking, size, correlation, and permutation.",
                "Sættet koncentreres ved positive værdier i dette fixture; formel inferens skal overveje fuld ranking, størrelse, korrelation og permutation.",
            ),
        ),
    ),
    practices=(
        (
            "m08.p01",
            "PIPELINE_DESIGN",
            _t(
                "Diseña una tabla de auditoría para mapear Ensembl a Entrez.",
                "Design an audit table for mapping Ensembl to Entrez.",
                "Design en audittabel til mapping fra Ensembl til Entrez.",
            ),
            (
                _t(
                    "Incluye versión, estado y multiplicidad.",
                    "Include version, status, and multiplicity.",
                    "Medtag version, status og multiplicitet.",
                ),
                _t("Conserva IDs originales.", "Retain original IDs.", "Bevar originale ID'er."),
            ),
            _t(
                "La tabla contiene ID original, versión, especie, ID destino, base y versión de mapeo, estado mapped/unmapped/ambiguous, número de destinos y regla de resolución. Se reportan pérdidas y duplicados sin sobrescribir el ID fuente.",
                "The table contains original ID, version, species, target ID, mapping database and version, mapped/unmapped/ambiguous status, number of targets, and resolution rule. Losses and duplicates are reported without overwriting the source ID.",
                "Tabellen indeholder originalt ID, version, art, mål-ID, mappingdatabase og version, mapped/unmapped/ambiguous-status, antal mål og løsningsregel. Tab og dubletter rapporteres uden at overskrive kilde-ID'et.",
            ),
            _t(
                "El mapeo es una transformación auditable, no una sustitución silenciosa.",
                "Mapping is an auditable transformation, not silent replacement.",
                "Mapping er en auditérbar transformation, ikke skjult erstatning.",
            ),
            "",
        ),
        (
            "m08.p02",
            "SHORT_ANSWER",
            _t(
                "Explica cómo elegir el universo para ORA.",
                "Explain how to choose the ORA universe.",
                "Forklar hvordan ORA-universet vælges.",
            ),
            (
                _t(
                    "Piensa en detectabilidad y filtros.",
                    "Think detectability and filters.",
                    "Tænk detekterbarhed og filtre.",
                ),
                _t(
                    "No uses automáticamente todo el genoma.",
                    "Do not automatically use the whole genome.",
                    "Brug ikke automatisk hele genomet.",
                ),
            ),
            _t(
                "El universo incluye features que podían medirse, mapearse y entrar al test bajo el pipeline, después de filtros técnicos independientes del resultado. Debe coincidir en especie, tipo de ID y unidad con la lista seleccionada. Excluir genes no observables evita una hipótesis nula incorrecta.",
                "The universe includes features that could be measured, mapped, and tested under the pipeline after outcome-independent technical filters. It must match the selected list in species, ID type, and unit. Excluding unobservable genes prevents an incorrect null hypothesis.",
                "Universet omfatter features, der kunne måles, mappes og testes under pipelinen efter outcome-uafhængige tekniske filtre. Det skal matche den udvalgte liste i art, ID-type og enhed. Udelukkelse af ikke-observerbare gener forhindrer en forkert nulhypotese.",
            ),
            _t(
                "El universo define qué solapamiento se considera esperado.",
                "The universe defines which overlap is considered expected.",
                "Universet definerer hvilket overlap der betragtes som forventet.",
            ),
            "",
        ),
        (
            "m08.p03",
            "DATA_INTERPRETATION",
            _t(
                "Diez términos GO significativos comparten casi los mismos genes. ¿Cómo los comunicas?",
                "Ten significant GO terms share almost the same genes. How do you communicate them?",
                "Ti signifikante GO-termer deler næsten de samme gener. Hvordan kommunikeres de?",
            ),
            (
                _t(
                    "Examina solapamiento y jerarquía.",
                    "Inspect overlap and hierarchy.",
                    "Undersøg overlap og hierarki.",
                ),
                _t(
                    "Conserva tabla completa.", "Retain the complete table.", "Bevar hele tabellen."
                ),
            ),
            _t(
                "Se cuantifica solapamiento, relación jerárquica, dirección y genes conductores. Puede resumirse un grupo redundante con una regla declarada y un término representativo, manteniendo la tabla completa y señalando que múltiples términos no equivalen a señales independientes.",
                "Quantify overlap, hierarchy, direction, and driver genes. A redundant group may be summarized using a declared rule and representative term while retaining the full table and noting that multiple terms do not equal independent signals.",
                "Kvantificér overlap, hierarki, retning og drivende gener. En redundant gruppe kan opsummeres med en deklareret regel og repræsentativ term, mens hele tabellen bevares og det bemærkes at flere termer ikke svarer til uafhængige signaler.",
            ),
            _t(
                "El ajuste estadístico no resuelve por sí solo redundancia biológica.",
                "Statistical adjustment alone does not resolve biological redundancy.",
                "Statistisk justering løser ikke alene biologisk redundans.",
            ),
            "",
        ),
        (
            "m08.p04",
            "DEBUGGING",
            _t(
                "Genes se seleccionan desde una red curada y luego se 'validan' porque forman un módulo en la misma red. Reconstruye la circularidad.",
                "Genes are selected from a curated network and then 'validated' because they form a module in the same network. Reconstruct the circularity.",
                "Gener vælges fra et kurateret netværk og 'valideres' derefter, fordi de danner et modul i samme netværk. Rekonstruér cirkulariteten.",
            ),
            (
                _t(
                    "La misma información se usa dos veces.",
                    "The same information is used twice.",
                    "Samme information bruges to gange.",
                ),
                _t(
                    "Busca evidencia independiente.",
                    "Seek independent evidence.",
                    "Søg uafhængig evidens.",
                ),
            ),
            _t(
                "La conectividad estaba incorporada al criterio de selección, por lo que reaparece necesariamente en la evaluación. No es validación independiente. Debe separarse descubrimiento y evaluación y utilizar datos externos, una base no usada, perturbación experimental o cohorte independiente.",
                "Connectivity was embedded in selection and therefore necessarily reappears during evaluation. This is not independent validation. Discovery and evaluation should be separated using external data, an unused resource, experimental perturbation, or an independent cohort.",
                "Connectivity var indbygget i selektionen og genoptræder derfor nødvendigvis i evalueringen. Det er ikke uafhængig validering. Discovery og evaluering bør adskilles med eksterne data, en ubrugt ressource, eksperimentel perturbation eller en uafhængig kohorte.",
            ),
            _t(
                "La validación debe aportar información no contenida en la selección.",
                "Validation must add information not contained in selection.",
                "Validering skal tilføre information, der ikke var indeholdt i selektionen.",
            ),
            "",
        ),
        (
            "m08.p05",
            "CODE_COMPLETION",
            _t(
                "Completa una función para calcular el valor p de ORA.",
                "Complete a function calculating an ORA p-value.",
                "Færdiggør en funktion, der beregner en ORA-p-værdi.",
            ),
            (
                _t(
                    "Usa phyper con overlap - 1.",
                    "Use phyper with overlap minus one.",
                    "Brug phyper med overlap minus én.",
                ),
                _t(
                    "Usa lower.tail = FALSE.", "Use lower.tail = FALSE.", "Brug lower.tail = FALSE."
                ),
            ),
            _t(
                "ora_p <- function(overlap, pathway_size, universe_size, selected_size) { phyper(overlap - 1, pathway_size, universe_size - pathway_size, selected_size, lower.tail = FALSE) }",
                "ora_p <- function(overlap, pathway_size, universe_size, selected_size) { phyper(overlap - 1, pathway_size, universe_size - pathway_size, selected_size, lower.tail = FALSE) }",
                "ora_p <- function(overlap, pathway_size, universe_size, selected_size) { phyper(overlap - 1, pathway_size, universe_size - pathway_size, selected_size, lower.tail = FALSE) }",
            ),
            _t(
                "La función calcula P(X ≥ overlap) bajo el modelo hipergeométrico.",
                "The function calculates P(X at least overlap) under the hypergeometric model.",
                "Funktionen beregner P(X mindst overlap) under den hypergeometriske model.",
            ),
            "ora_p <- function(overlap, pathway_size, universe_size, selected_size) {\n  # return the upper-tail probability\n}",
        ),
        (
            "m08.p06",
            "ORAL_EXPLANATION",
            _t(
                "Prepara una explicación de 90 segundos: ¿qué significa que un pathway esté enriquecido?",
                "Prepare a 90-second explanation: what does it mean for a pathway to be enriched?",
                "Forbered en 90-sekunders forklaring: hvad betyder det at et pathway er enriched?",
            ),
            (
                _t(
                    "Define lista/ranking y universo.",
                    "Define list/ranking and universe.",
                    "Definér liste/ranking og univers.",
                ),
                _t(
                    "Limita mecanismo y causalidad.",
                    "Limit mechanism and causality.",
                    "Begræns mekanisme og kausalitet.",
                ),
            ),
            _t(
                "Significa que genes de un conjunto aparecen más de lo esperado en una lista o se concentran en un extremo de un ranking bajo un universo y método declarados. La interpretación depende de mapeo, tamaño, solapamiento, dirección, multiplicidad y genes conductores. No demuestra que el pathway esté activado, sea causal o explique el fenotipo; genera una hipótesis contextualizada.",
                "It means genes from a set occur more than expected in a list or concentrate at one end of a ranking under a declared universe and method. Interpretation depends on mapping, size, overlap, direction, multiplicity, and driver genes. It does not demonstrate that the pathway is activated, causal, or explains the phenotype; it generates a contextualized hypothesis.",
                "Det betyder at gener fra et sæt forekommer mere end forventet i en liste eller koncentreres i en ende af en ranking under et deklareret univers og metode. Fortolkningen afhænger af mapping, størrelse, overlap, retning, multiplicitet og drivende gener. Det demonstrerer ikke at pathwayet er aktiveret, kausalt eller forklarer fænotypen; det genererer en kontekstualiseret hypotese.",
            ),
            _t(
                "La respuesta separa resultado matemático de afirmación mecanística.",
                "The answer separates the mathematical result from a mechanistic claim.",
                "Svaret adskiller det matematiske resultat fra en mekanistisk påstand.",
            ),
            "",
        ),
    ),
    mcqs=(
        _mcq(
            "q01",
            _t(
                "¿Qué debe auditarse antes de enrichment?",
                "What should be audited before enrichment?",
                "Hvad bør auditeres før enrichment?",
            ),
            (
                _option(
                    "a",
                    _t(
                        "Mapeo, pérdidas y duplicados",
                        "Mapping, losses, and duplicates",
                        "Mapping, tab og dubletter",
                    ),
                ),
                _option("b", _t("Sólo colores", "Only colors", "Kun farver")),
                _option("c", _t("Sólo título", "Only title", "Kun titel")),
                _option("d", _t("Sólo memoria", "Only memory", "Kun hukommelse")),
            ),
            "a",
            _t(
                "Los IDs determinan qué features entran a los conjuntos.",
                "IDs determine which features enter sets.",
                "ID'er bestemmer hvilke features der indgår i sættene.",
            ),
        ),
        _mcq(
            "q02",
            _t(
                "¿Qué universo es apropiado?",
                "Which universe is appropriate?",
                "Hvilket univers er passende?",
            ),
            (
                _option(
                    "a",
                    _t(
                        "Features medibles y elegibles para el test",
                        "Features measurable and eligible for testing",
                        "Features der kunne måles og testes",
                    ),
                ),
                _option(
                    "b",
                    _t("Siempre todo el genoma", "Always the entire genome", "Altid hele genomet"),
                ),
                _option(
                    "c",
                    _t(
                        "Sólo significativos",
                        "Only significant features",
                        "Kun signifikante features",
                    ),
                ),
                _option("d", _t("Sólo genes conocidos", "Only familiar genes", "Kun kendte gener")),
            ),
            "a",
            _t(
                "El universo representa oportunidades reales de selección.",
                "The universe represents real selection opportunities.",
                "Universet repræsenterer reelle selektionsmuligheder.",
            ),
        ),
        _mcq(
            "q03",
            _t("¿Qué pierde ORA?", "What does ORA discard?", "Hvad kasserer ORA?"),
            (
                _option(
                    "a",
                    _t(
                        "Información de ranking fuera del umbral",
                        "Ranking information outside the threshold",
                        "Rankinginformation uden for tærsklen",
                    ),
                ),
                _option("b", _t("Todos los IDs", "All IDs", "Alle ID'er")),
                _option("c", _t("El universo", "The universe", "Universet")),
                _option("d", _t("El overlap", "The overlap", "Overlappet")),
            ),
            "a",
            _t(
                "Convierte un resultado continuo en lista seleccionada/no seleccionada.",
                "It converts a continuous result into selected/not-selected status.",
                "Det konverterer et kontinuert resultat til valgt/ikke-valgt status.",
            ),
        ),
        _mcq(
            "q04",
            _t(
                "¿Qué requiere un método rank-based?",
                "What does a rank-based method require?",
                "Hvad kræver en rankingbaseret metode?",
            ),
            (
                _option(
                    "a",
                    _t(
                        "Métrica dirigida consistente para todas las features",
                        "A consistently directed metric for all features",
                        "En konsistent retningsbestemt metrisk for alle features",
                    ),
                ),
                _option("b", _t("Sólo p < 0.05", "Only p below 0.05", "Kun p under 0,05")),
                _option("c", _t("Sólo diez genes", "Only ten genes", "Kun ti gener")),
                _option("d", _t("Sin empates nunca", "No ties ever", "Ingen ties nogensinde")),
            ),
            "a",
            _t(
                "El orden debe tener una interpretación uniforme.",
                "The ordering must have a uniform interpretation.",
                "Rækkefølgen skal have en ensartet fortolkning.",
            ),
        ),
        _mcq(
            "q05",
            _t(
                "¿Qué no elimina el ajuste FDR?",
                "What does FDR adjustment not remove?",
                "Hvad fjerner FDR-justering ikke?",
            ),
            (
                _option(
                    "a",
                    _t(
                        "Redundancia entre términos",
                        "Redundancy among terms",
                        "Redundans mellem termer",
                    ),
                ),
                _option("b", _t("Valores p", "P-values", "P-værdier")),
                _option("c", _t("IDs", "IDs", "ID'er")),
                _option("d", _t("Tamaño de conjuntos", "Set size", "Sætstørrelse")),
            ),
            "a",
            _t(
                "Términos correlacionados pueden seguir representando la misma señal.",
                "Correlated terms may still represent the same signal.",
                "Korrelerede termer kan stadig repræsentere samme signal.",
            ),
        ),
        _mcq(
            "q06",
            _t(
                "¿Qué son genes conductores?",
                "What are driver genes in enrichment interpretation?",
                "Hvad er drivende gener i enrichment-fortolkning?",
            ),
            (
                _option(
                    "a",
                    _t(
                        "Features que contribuyen directamente a la señal del conjunto",
                        "Features directly contributing to the set signal",
                        "Features der bidrager direkte til sætsignalet",
                    ),
                ),
                _option(
                    "b",
                    _t(
                        "Todos los genes del genoma",
                        "All genes in the genome",
                        "Alle gener i genomet",
                    ),
                ),
                _option(
                    "c",
                    _t("Sólo housekeeping", "Only housekeeping genes", "Kun housekeeping-gener"),
                ),
                _option("d", _t("Nombres de pathways", "Pathway names", "Pathwaynavne")),
            ),
            "a",
            _t(
                "Conectan el término agregado con resultados feature-level.",
                "They connect the aggregate term to feature-level results.",
                "De forbinder den aggregerede term med feature-level-resultater.",
            ),
        ),
        _mcq(
            "q07",
            _t(
                "¿Qué es validación circular?",
                "What is circular validation?",
                "Hvad er cirkulær validering?",
            ),
            (
                _option(
                    "a",
                    _t(
                        "Reutilizar la misma información previa para seleccionar y validar",
                        "Reuse the same prior information for selection and validation",
                        "Genbrug samme prior-information til selektion og validering",
                    ),
                ),
                _option(
                    "b", _t("Usar otra cohorte", "Use another cohort", "Brug en anden kohorte")
                ),
                _option(
                    "c",
                    _t(
                        "Replicar experimentalmente",
                        "Replicate experimentally",
                        "Replikér eksperimentelt",
                    ),
                ),
                _option("d", _t("Cambiar base", "Change database", "Skift database")),
            ),
            "a",
            _t(
                "La evaluación no añade evidencia independiente.",
                "Evaluation adds no independent evidence.",
                "Evalueringen tilføjer ingen uafhængig evidens.",
            ),
        ),
        _mcq(
            "q08",
            _t(
                "¿Qué demuestra enrichment?",
                "What does enrichment demonstrate?",
                "Hvad demonstrerer enrichment?",
            ),
            (
                _option(
                    "a",
                    _t(
                        "Asociación de un conjunto bajo método y universo",
                        "Set association under a method and universe",
                        "Sætassociation under en metode og et univers",
                    ),
                ),
                _option("b", _t("Mecanismo causal", "Causal mechanism", "Kausal mekanisme")),
                _option("c", _t("Activación directa", "Direct activation", "Direkte aktivering")),
                _option("d", _t("Utilidad clínica", "Clinical utility", "Klinisk nytte")),
            ),
            "a",
            _t(
                "La afirmación mecanística requiere evidencia adicional.",
                "A mechanistic claim requires additional evidence.",
                "En mekanistisk påstand kræver yderligere evidens.",
            ),
        ),
    ),
    true_false=(
        _tf(
            "tf01",
            _t(
                "El mapeo de IDs es independiente de especie y versión.",
                "ID mapping is independent of species and version.",
                "ID-mapping er uafhængig af art og version.",
            ),
            False,
            _t(
                "Ambas determinan correspondencias válidas.",
                "Both determine valid correspondences.",
                "Begge bestemmer gyldige korrespondancer.",
            ),
        ),
        _tf(
            "tf02",
            _t(
                "El universo cambia la hipótesis nula de ORA.",
                "The universe changes the ORA null hypothesis.",
                "Universet ændrer ORA-nulhypotesen.",
            ),
            True,
            _t(
                "Define oportunidades esperadas de overlap.",
                "It defines expected overlap opportunities.",
                "Det definerer forventede overlapmuligheder.",
            ),
        ),
        _tf(
            "tf03",
            _t(
                "ORA utiliza información completa de ranking.",
                "ORA uses complete ranking information.",
                "ORA bruger komplet rankinginformation.",
            ),
            False,
            _t(
                "Usa una lista seleccionada por umbral.",
                "It uses a threshold-selected list.",
                "Det bruger en tærskelvalgt liste.",
            ),
        ),
        _tf(
            "tf04",
            _t(
                "Métodos rank-based pueden detectar señal distribuida.",
                "Rank-based methods can detect distributed signal.",
                "Rankingbaserede metoder kan detektere distribueret signal.",
            ),
            True,
            _t(
                "Utilizan todas las features ordenadas.",
                "They use all ordered features.",
                "De bruger alle ordnede features.",
            ),
        ),
        _tf(
            "tf05",
            _t(
                "FDR elimina redundancia semántica.",
                "FDR removes semantic redundancy.",
                "FDR fjerner semantisk redundans.",
            ),
            False,
            _t(
                "Controla multiplicidad, no solapamiento conceptual.",
                "It controls multiplicity, not conceptual overlap.",
                "Det kontrollerer multiplicitet, ikke konceptuelt overlap.",
            ),
        ),
        _tf(
            "tf06",
            _t(
                "Leading edge conecta términos con features contribuyentes.",
                "Leading edge connects terms to contributing features.",
                "Leading edge forbinder termer med bidragende features.",
            ),
            True,
            _t(
                "Permite inspeccionar qué impulsa la señal.",
                "It identifies what drives the signal.",
                "Det identificerer hvad der driver signalet.",
            ),
        ),
        _tf(
            "tf07",
            _t(
                "Enrichment demuestra causalidad.",
                "Enrichment demonstrates causality.",
                "Enrichment demonstrerer kausalitet.",
            ),
            False,
            _t(
                "Es una asociación agregada bajo conocimiento previo.",
                "It is an aggregate association under prior knowledge.",
                "Det er en aggregeret association under prior viden.",
            ),
        ),
        _tf(
            "tf08",
            _t(
                "La validación independiente debe aportar nueva información.",
                "Independent validation should add new information.",
                "Uafhængig validering bør tilføre ny information.",
            ),
            True,
            _t(
                "Reutilizar el mismo recurso es circular.",
                "Reusing the same resource is circular.",
                "Genbrug af samme ressource er cirkulært.",
            ),
        ),
    ),
    tutor=(
        _t(
            "El tutor debe exigir IDs, universo, método, multiplicidad, dirección, genes conductores y procedencia antes de formular una interpretación biológica.",
            "The tutor should require IDs, universe, method, multiplicity, direction, driver genes, and provenance before making a biological interpretation.",
            "Tutoren bør kræve ID'er, univers, metode, multiplicitet, retning, drivende gener og proveniens før biologisk fortolkning.",
        ),
        (
            _t(
                "Mapeo y universo definen la prueba.",
                "Mapping and universe define the test.",
                "Mapping og univers definerer testen.",
            ),
            _t(
                "ORA y ranking responden preguntas distintas.",
                "ORA and ranking answer different questions.",
                "ORA og ranking besvarer forskellige spørgsmål.",
            ),
            _t(
                "Redundancia requiere análisis explícito.",
                "Redundancy requires explicit analysis.",
                "Redundans kræver eksplicit analyse.",
            ),
            _t(
                "Pathways generan hipótesis, no mecanismos confirmados.",
                "Pathways generate hypotheses, not confirmed mechanisms.",
                "Pathways genererer hypoteser, ikke bekræftede mekanismer.",
            ),
        ),
        (
            _t(
                "Usar todo el genoma sin justificar.",
                "Use the whole genome without justification.",
                "Brug hele genomet uden begrundelse.",
            ),
            _t("Ignorar IDs no mapeados.", "Ignore unmapped IDs.", "Ignorér ikke-mappede ID'er."),
            _t(
                "Contar términos redundantes como señales independientes.",
                "Count redundant terms as independent signals.",
                "Tæl redundante termer som uafhængige signaler.",
            ),
            _t(
                "Validar con la misma base usada para seleccionar.",
                "Validate using the same database used for selection.",
                "Validér med samme database som blev brugt til selektion.",
            ),
        ),
        (
            _t(
                "¿Qué features podían entrar al universo?",
                "Which features could enter the universe?",
                "Hvilke features kunne indgå i universet?",
            ),
            _t(
                "¿Qué se perdió durante mapping?",
                "What was lost during mapping?",
                "Hvad gik tabt under mapping?",
            ),
            _t(
                "¿Qué genes impulsan el término?",
                "Which genes drive the term?",
                "Hvilke gener driver termen?",
            ),
            _t(
                "¿Qué evidencia independiente existe?",
                "Which independent evidence exists?",
                "Hvilken uafhængig evidens findes?",
            ),
        ),
        (
            _t("Audita IDs y universo.", "Audits IDs and universe.", "Auditerer ID'er og univers."),
            _t(
                "Elige método compatible.",
                "Chooses a compatible method.",
                "Vælger kompatibel metode.",
            ),
            _t(
                "Interpreta dirección y redundancia.",
                "Interprets direction and redundancy.",
                "Fortolker retning og redundans.",
            ),
            _t(
                "Limita mecanismo y causalidad.",
                "Limits mechanism and causality.",
                "Begrænser mekanisme og kausalitet.",
            ),
        ),
        (
            _t(
                "No inventar pathways o genes conductores.",
                "Do not invent pathways or driver genes.",
                "Opfind ikke pathways eller drivende gener.",
            ),
            _t(
                "No afirmar activación sin evidencia.",
                "Do not claim activation without evidence.",
                "Påstå ikke aktivering uden evidens.",
            ),
            _t(
                "No ocultar resultados discordantes.",
                "Do not hide discordant results.",
                "Skjul ikke uoverensstemmende resultater.",
            ),
            _t(
                "Responder en el idioma activo con fuentes explícitas.",
                "Respond in the active language with explicit sources.",
                "Svar på det aktive sprog med eksplicitte kilder.",
            ),
        ),
        (
            "https://reactome.org/userguide/analysis",
            "https://geneontology.org/docs/go-enrichment-analysis/",
            "https://bioconductor.org/packages/release/bioc/html/clusterProfiler.html",
        ),
    ),
)

LOCALIZED_MODULE_08_BIOLOGICAL_INTERPRETATION = build_module(_SPEC)
LOCALIZED_OBJECTIVE_QUESTION_BANK_08 = build_question_bank(_SPEC)


def materialize_module_08_question_bank(
    locale: AppLocale | str = AppLocale.SPANISH_SPAIN,
) -> tuple[AssessmentItem, ...]:
    """Materialize the stable module 8 objective bank."""

    return materialize_bank(LOCALIZED_OBJECTIVE_QUESTION_BANK_08, locale)


MODULE_08_BIOLOGICAL_INTERPRETATION: LearningModule = (
    LOCALIZED_MODULE_08_BIOLOGICAL_INTERPRETATION.materialize(AppLocale.SPANISH_SPAIN)
)
OBJECTIVE_QUESTION_BANK_08 = materialize_module_08_question_bank()

__all__ = [
    "LOCALIZED_MODULE_08_BIOLOGICAL_INTERPRETATION",
    "LOCALIZED_OBJECTIVE_QUESTION_BANK_08",
    "MODULE_08_BIOLOGICAL_INTERPRETATION",
    "OBJECTIVE_QUESTION_BANK_08",
    "materialize_module_08_question_bank",
]
