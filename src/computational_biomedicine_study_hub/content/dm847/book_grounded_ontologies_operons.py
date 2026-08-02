"""Focused source-grounded extensions for DM847 ontologies and operons."""

from __future__ import annotations

from dataclasses import replace

from ...learning.activity_types import ActivityType
from ..localized_models import LocalizedLearningModule, LocalizedTutorSupportPacket
from .authoring import concept, example, objective, objective_mcq, practice
from .book_grounded_audit import AcademicReference, ModuleSourceAudit

DM847_ONTOLOGY_OPERON_SOURCES: tuple[AcademicReference, ...] = (
    AcademicReference(
        source_id="coveney-2014-ch03-ch08",
        citation=(
            "Peter V. Coveney, Vanessa Díaz-Zuccarini, Peter Hunter, and Marco Viceconti "
            "(eds.), Computational Biomedicine: Modelling the Human Body, Oxford "
            "University Press (2014), chapters 3 and 8."
        ),
        relevant_scope=(
            "ontology-based semantic interoperability, composite biomedical annotations, "
            "meaningful semantic queries, persistent identity, and workflow provenance"
        ),
    ),
    AcademicReference(
        source_id="yachay-molecular-biology-ch19-ch26",
        citation=(
            "Yachay Tech Molecular Biology lecture notes, chapters 19 and 26: "
            "prokaryotic transcription and the operon."
        ),
        relevant_scope=(
            "strand-relative upstream and downstream direction, promoters, transcriptional "
            "termination, polycistronic RNA, and operon boundaries"
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


def update_ontology_operon_source_catalog(
    sources: tuple[AcademicReference, ...],
) -> tuple[AcademicReference, ...]:
    """Append the specialized references needed for M02 and M07."""

    existing_ids = {source.source_id for source in sources}
    additions = tuple(
        source for source in DM847_ONTOLOGY_OPERON_SOURCES if source.source_id not in existing_ids
    )
    return (*sources, *additions)


def update_ontology_operon_audit(
    audit: tuple[ModuleSourceAudit, ...],
) -> tuple[ModuleSourceAudit, ...]:
    """Mark M02 and M07 reviewed after their focused extensions exist."""

    updated: list[ModuleSourceAudit] = []
    for item in audit:
        if item.module_id == "dm847.m02":
            updated.append(
                replace(
                    item,
                    source_ids=(
                        "sdu-dm847-active-2025",
                        "coveney-2014-ch03-ch08",
                    ),
                    source_scope=(
                        "biomedical ontologies and semantic interoperability",
                        "asserted versus inferred annotations",
                        "relation-specific query expansion",
                        "versioned provenance and reproducible semantic queries",
                    ),
                    state="consistent",
                    finding=(
                        "Existing coverage of identifiers, versions, vocabularies, ontologies, "
                        "relation semantics, relational design, FAIR principles, provenance, "
                        "joins, and integrity checks is consistent. The boundary between directly "
                        "asserted annotations and ontology-derived annotations required one "
                        "explicit treatment, including proof paths and versioned query contracts."
                    ),
                    implemented_change=(
                        "Added an original trilingual semantic-closure explanation, deterministic "
                        "asserted-versus-inferred example, query-design exercise, and stable "
                        "objective item."
                    ),
                )
            )
        elif item.module_id == "dm847.m07":
            updated.append(
                replace(
                    item,
                    source_ids=(
                        "sdu-dm847-active-2025",
                        "yachay-molecular-biology-ch19-ch26",
                    ),
                    source_scope=(
                        "prokaryotic transcription and polycistronic operons",
                        "genomic adjacency and strand-relative transcriptional order",
                        "promoter and terminator orientation",
                        "species-aware operon prediction and validation",
                    ),
                    state="consistent",
                    finding=(
                        "Existing coverage of operon biology, genomic adjacency, intergenic "
                        "distance, predictive features, classification, calibration, cross-species "
                        "validation, horizontal transfer, and independent biological evidence is "
                        "consistent. The distinction between genomic coordinate order and "
                        "transcriptional order on the negative strand required one explicit "
                        "algorithmic treatment."
                    ),
                    implemented_change=(
                        "Added an original trilingual strand-aware adjacency explanation, "
                        "deterministic positive- and negative-strand example, pipeline exercise, "
                        "and stable objective item."
                    ),
                )
            )
        else:
            updated.append(item)
    return tuple(updated)


def _extend_ontologies(module: LocalizedLearningModule) -> LocalizedLearningModule:
    """Add asserted-versus-inferred semantic query contracts to M02."""

    extended = replace(
        module,
        objectives=module.objectives
        + (
            objective(
                "m02.bg.o1",
                (
                    "Distinguir anotaciones afirmadas e inferidas, aplicar cierre sólo sobre "
                    "relaciones autorizadas y conservar la ruta y versión que justifican cada "
                    "resultado.",
                    "Distinguish asserted and inferred annotations, apply closure only over "
                    "authorized relations, and preserve the path and version supporting each "
                    "result.",
                    "Skelne mellem påståede og infererede annotationer, anvende lukning kun over "
                    "tilladte relationer og bevare den sti og version, der begrunder hvert "
                    "resultat.",
                ),
            ),
        ),
        concepts=module.concepts
        + (
            concept(
                "semantic-closure-and-assertion-provenance",
                (
                    "Cierre semántico y procedencia de inferencias",
                    "Semantic closure and inference provenance",
                    "Semantisk lukning og inferensproveniens",
                ),
                (
                    "Una anotación directa afirma una relación presente en la fuente; una "
                    "anotación inferida aparece al aplicar reglas de la ontología. Por ejemplo, "
                    "si un gen está anotado a T-cell y T-cell is_a lymphocyte, una consulta "
                    "expandida puede recuperar lymphocyte, pero debe etiquetarlo como inferido. "
                    "El cierre no se aplica indiscriminadamente: is_a suele permitir propagación "
                    "hacia ancestros, mientras regulates o located_in requieren reglas distintas "
                    "y no deben tratarse como transitivas por defecto. Un resultado reproducible "
                    "conserva la anotación inicial, la ruta de relaciones, el conjunto de reglas, "
                    "la dirección, la versión de la ontología y la fuente. Las consultas exactas "
                    "y expandidas responden preguntas diferentes y sus conteos no deben mezclarse "
                    "sin declararlo.",
                    "A direct annotation asserts a relation present in the source; an inferred "
                    "annotation appears after applying ontology rules. For example, if a gene is "
                    "annotated to T-cell and T-cell is_a lymphocyte, an expanded query may return "
                    "lymphocyte, but it should label it as inferred. Closure is not applied "
                    "indiscriminately: is_a commonly supports propagation to ancestors, whereas "
                    "regulates or located_in require different rules and should not be treated as "
                    "transitive by default. A reproducible result preserves the initial annotation, "
                    "relation path, rule set, direction, ontology release, and source. Exact and "
                    "expanded queries answer different questions, and their counts should not be "
                    "mixed without an explicit declaration.",
                    "En direkte annotation påstår en relation, der findes i kilden; en infereret "
                    "annotation opstår efter anvendelse af ontologiregler. Hvis et gen eksempelvis "
                    "er annoteret til T-cell, og T-cell is_a lymphocyte, kan en udvidet forespørgsel "
                    "returnere lymphocyte, men resultatet skal mærkes som infereret. Lukning må ikke "
                    "anvendes ukritisk: is_a understøtter ofte propagation til forfædre, mens "
                    "regulates og located_in kræver andre regler og ikke bør antages transitive. Et "
                    "reproducerbart resultat bevarer startannotationen, relationsstien, regelsættet, "
                    "retningen, ontologiversionen og kilden. Eksakte og udvidede forespørgsler "
                    "besvarer forskellige spørgsmål, og deres antal må ikke blandes uden en "
                    "eksplicit erklæring.",
                ),
                (
                    (
                        "Afirmado e inferido son estados epistemológicos distintos.",
                        "Asserted and inferred are distinct epistemic states.",
                        "Påstået og infereret er forskellige epistemiske tilstande.",
                    ),
                    (
                        "El cierre depende del tipo y dirección de la relación.",
                        "Closure depends on relation type and direction.",
                        "Lukning afhænger af relationstype og retning.",
                    ),
                    (
                        "Cada inferencia debe conservar una ruta o justificación auditable.",
                        "Every inference should preserve an auditable path or justification.",
                        "Hver inferens bør bevare en revisionsbar sti eller begrundelse.",
                    ),
                    (
                        "La versión de la ontología forma parte del contrato de consulta.",
                        "The ontology release is part of the query contract.",
                        "Ontologiversionen er en del af forespørgselskontrakten.",
                    ),
                ),
            ),
        ),
        worked_examples=module.worked_examples
        + (
            example(
                "m02.bg.e01",
                (
                    "Separar anotaciones directas e inferidas",
                    "Separate direct and inferred annotations",
                    "Adskil direkte og infererede annotationer",
                ),
                (
                    "Expande una anotación sólo por relaciones is_a y conserva la ruta que "
                    "justifica cada ancestro.",
                    "Expand an annotation only through is_a relations and preserve the path "
                    "supporting every ancestor.",
                    "Udvid kun en annotation gennem is_a-relationer og bevar den sti, der "
                    "understøtter hver forfader.",
                ),
                (
                    (
                        "La anotación inicial se registra como asserted.",
                        "The starting annotation is recorded as asserted.",
                        "Startannotationen registreres som asserted.",
                    ),
                    (
                        "La cola recorre ancestros sin repetir nodos.",
                        "The queue traverses ancestors without repeating nodes.",
                        "Køen gennemløber forfædre uden at gentage noder.",
                    ),
                    (
                        "Cada ancestro conserva una ruta desde el término original.",
                        "Every ancestor preserves a path from the original term.",
                        "Hver forfader bevarer en sti fra den oprindelige term.",
                    ),
                ),
                "def closure_with_paths(\n"
                "    term: str, parents: dict[str, tuple[str, ...]]\n"
                ") -> list[tuple[str, tuple[str, ...], str]]:\n"
                "    results = [(term, (term,), 'asserted')]\n"
                "    queue = [(term, (term,))]\n"
                "    visited = {term}\n"
                "    while queue:\n"
                "        current, path = queue.pop(0)\n"
                "        for parent in sorted(parents.get(current, ())):\n"
                "            if parent in visited:\n"
                "                continue\n"
                "            visited.add(parent)\n"
                "            parent_path = (*path, parent)\n"
                "            results.append((parent, parent_path, 'inferred'))\n"
                "            queue.append((parent, parent_path))\n"
                "    return results\n"
                "\n"
                "\n"
                "parents = {'T-cell': ('lymphocyte',), 'lymphocyte': ('cell',)}\n"
                "print(closure_with_paths('T-cell', parents))",
                "[('T-cell', ('T-cell',), 'asserted'), ('lymphocyte', "
                "('T-cell', 'lymphocyte'), 'inferred'), ('cell', "
                "('T-cell', 'lymphocyte', 'cell'), 'inferred')]",
                (
                    "La salida permite mostrar resultados expandidos sin presentarlos como "
                    "afirmaciones directas. En un sistema real también se registra la versión de "
                    "la ontología y la fuente de la anotación inicial.",
                    "The output exposes expanded results without presenting them as direct "
                    "assertions. A real system would also record the ontology release and the "
                    "source of the starting annotation.",
                    "Outputtet viser udvidede resultater uden at fremstille dem som direkte "
                    "påstande. Et reelt system ville også registrere ontologiversionen og kilden "
                    "til startannotationen.",
                ),
            ),
        ),
        practice_exercises=module.practice_exercises
        + (
            practice(
                "m02.bg.p01",
                ActivityType.DATA_INTERPRETATION,
                (
                    "Una consulta exacta devuelve 18 genes y una consulta expandida por is_a "
                    "devuelve 47. Explica qué debe registrarse antes de comparar o publicar esos "
                    "conteos.",
                    "An exact query returns 18 genes and an is_a-expanded query returns 47. "
                    "Explain what must be recorded before comparing or publishing those counts.",
                    "En eksakt forespørgsel returnerer 18 gener, og en is_a-udvidet forespørgsel "
                    "returnerer 47. Forklar hvad der skal registreres, før antallene sammenlignes "
                    "eller publiceres.",
                ),
                (
                    (
                        "Separa coincidencias directas de coincidencias heredadas.",
                        "Separate direct matches from inherited matches.",
                        "Adskil direkte matches fra nedarvede matches.",
                    ),
                    (
                        "Incluye versión, relaciones y dirección de expansión.",
                        "Include release, relations, and expansion direction.",
                        "Medtag version, relationer og udvidelsesretning.",
                    ),
                ),
                (
                    "Registrar la versión o fecha de la ontología, el conjunto de anotaciones y "
                    "su release, si la consulta es exacta o expandida, las relaciones autorizadas "
                    "y su dirección, el tratamiento de términos obsoletos, la deduplicación por "
                    "gen, la ruta de inferencia y los conteos separados de resultados asserted e "
                    "inferred. El aumento de 18 a 47 refleja la semántica de expansión y no una "
                    "nueva medición biológica.",
                    "Record the ontology version or date, annotation set and release, whether the "
                    "query is exact or expanded, authorized relations and direction, handling of "
                    "obsolete terms, gene-level deduplication, inference paths, and separate counts "
                    "for asserted and inferred results. The increase from 18 to 47 reflects query "
                    "expansion semantics rather than a new biological measurement.",
                    "Registrér ontologiversion eller dato, annotationssæt og release, om "
                    "forespørgslen er eksakt eller udvidet, tilladte relationer og retning, "
                    "håndtering af forældede termer, deduplikering pr. gen, inferensstier og "
                    "separate antal for asserted og inferred resultater. Stigningen fra 18 til 47 "
                    "afspejler udvidelsens semantik og ikke en ny biologisk måling.",
                ),
                (
                    "Una consulta semántica reproducible declara tanto la evidencia original como "
                    "las reglas que generan resultados derivados.",
                    "A reproducible semantic query declares both original evidence and the rules "
                    "that generate derived results.",
                    "En reproducerbar semantisk forespørgsel erklærer både oprindelig evidens og "
                    "de regler, der genererer afledte resultater.",
                ),
            ),
        ),
        assessment_items=module.assessment_items
        + (
            objective_mcq(
                "dm847.m02.book.001",
                (
                    "¿Qué hace reproducible una anotación inferida por una ontología?",
                    "What makes an ontology-inferred annotation reproducible?",
                    "Hvad gør en ontologi-infereret annotation reproducerbar?",
                ),
                (
                    (
                        "provenance",
                        (
                            "Separar asserted e inferred y conservar ruta, reglas y versión.",
                            "Separate asserted and inferred results and preserve path, rules, and release.",
                            "Adskil asserted og inferred resultater og bevar sti, regler og version.",
                        ),
                    ),
                    (
                        "all_transitive",
                        (
                            "Tratar todas las relaciones como transitivas.",
                            "Treat every relation as transitive.",
                            "Behandle alle relationer som transitive.",
                        ),
                    ),
                    (
                        "labels_only",
                        (
                            "Guardar únicamente las etiquetas visibles.",
                            "Store only display labels.",
                            "Gem kun de viste labels.",
                        ),
                    ),
                ),
                "provenance",
                (
                    "La inferencia depende de relaciones autorizadas, dirección, ruta, fuente y "
                    "versión; no debe presentarse como una afirmación directa.",
                    "Inference depends on authorized relations, direction, path, source, and "
                    "release; it should not be presented as a direct assertion.",
                    "Inferens afhænger af tilladte relationer, retning, sti, kilde og version og "
                    "må ikke fremstilles som en direkte påstand.",
                ),
            ),
        ),
    )
    return _with_source_basis(
        extended,
        ("sdu-dm847-active-2025", "coveney-2014-ch03-ch08"),
    )


def _extend_operons(module: LocalizedLearningModule) -> LocalizedLearningModule:
    """Add strand-aware genomic and transcriptional ordering to M07."""

    extended = replace(
        module,
        objectives=module.objectives
        + (
            objective(
                "m07.bg.o1",
                (
                    "Construir adyacencias genómicas sin saltar genes intermedios y convertirlas "
                    "a orden transcripcional según la hebra.",
                    "Construct genomic adjacencies without skipping intervening genes and convert "
                    "them to strand-aware transcriptional order.",
                    "Konstruere genomiske naboskaber uden at springe mellemliggende gener over og "
                    "omsætte dem til strengbevidst transkriptionsrækkefølge.",
                ),
            ),
        ),
        concepts=module.concepts
        + (
            concept(
                "genomic-order-vs-transcriptional-order",
                (
                    "Orden genómico frente a orden transcripcional",
                    "Genomic order versus transcriptional order",
                    "Genomisk rækkefølge versus transkriptionsrækkefølge",
                ),
                (
                    "La adyacencia se determina primero por coordenadas dentro del mismo replicón, "
                    "considerando todos los genes. Agrupar por hebra antes de formar pares puede "
                    "saltar un gen de la hebra opuesta y crear una adyacencia falsa. Después de "
                    "formar pares genómicamente consecutivos se conservan los que comparten hebra. "
                    "En la hebra positiva, el gen de menor coordenada aparece primero en orden "
                    "transcripcional; en la negativa ocurre lo contrario. La distancia física entre "
                    "dos CDS puede calcularse en coordenadas genómicas, pero upstream, downstream, "
                    "promotores, terminadores y ventanas de motivos deben interpretarse respecto "
                    "a la dirección 5'→3' de transcripción. Para comparar secuencias reguladoras "
                    "entre hebras, las ventanas de la hebra negativa suelen orientarse mediante "
                    "complemento inverso. El orden correcto no demuestra co-transcripción, pero "
                    "evita construir características biológicamente invertidas.",
                    "Adjacency is determined first from coordinates within the same replicon while "
                    "considering every gene. Grouping by strand before pairing can skip an "
                    "opposite-strand gene and create a false adjacency. After forming genomically "
                    "consecutive pairs, retain pairs sharing a strand. On the positive strand, the "
                    "lower-coordinate gene comes first in transcriptional order; on the negative "
                    "strand the order is reversed. Physical CDS distance can be computed in genomic "
                    "coordinates, but upstream, downstream, promoters, terminators, and motif "
                    "windows must be interpreted relative to the 5'→3' transcription direction. "
                    "For cross-strand regulatory-sequence comparison, negative-strand windows are "
                    "usually reverse-complemented into transcriptional orientation. Correct order "
                    "does not prove co-transcription, but it prevents biologically inverted features.",
                    "Naboskab bestemmes først ud fra koordinater inden for samme replikon, mens alle "
                    "gener medtages. Gruppering efter streng før pardannelse kan springe et gen på "
                    "den modsatte streng over og skabe et falsk naboskab. Efter dannelse af genomisk "
                    "konsekutive par beholdes par på samme streng. På plusstrengen kommer genet med "
                    "lavest koordinat først i transkriptionsrækkefølgen; på minusstrengen er "
                    "rækkefølgen omvendt. Den fysiske CDS-afstand kan beregnes i genomiske "
                    "koordinater, men upstream, downstream, promotere, terminatorer og motivvinduer "
                    "skal fortolkes relativt til transkriptionens 5'→3'-retning. Ved sammenligning "
                    "af regulatoriske sekvenser orienteres minusstrengsvinduer normalt med omvendt "
                    "komplement. Korrekt rækkefølge beviser ikke co-transkription, men forhindrer "
                    "biologisk inverterede features.",
                ),
                (
                    (
                        "La adyacencia se construye antes de filtrar por hebra.",
                        "Adjacency is constructed before filtering by strand.",
                        "Naboskab konstrueres før filtrering efter streng.",
                    ),
                    (
                        "La hebra negativa invierte el orden transcripcional del par.",
                        "The negative strand reverses the pair's transcriptional order.",
                        "Minusstrengen vender parrets transkriptionsrækkefølge.",
                    ),
                    (
                        "Upstream y downstream son relativos a la dirección de transcripción.",
                        "Upstream and downstream are relative to transcription direction.",
                        "Upstream og downstream er relative til transkriptionsretningen.",
                    ),
                    (
                        "Orientación correcta es necesaria, pero no suficiente, para inferir operones.",
                        "Correct orientation is necessary but insufficient for operon inference.",
                        "Korrekt orientering er nødvendig, men utilstrækkelig til operoninferens.",
                    ),
                ),
            ),
        ),
        worked_examples=module.worked_examples
        + (
            example(
                "m07.bg.e01",
                (
                    "Convertir adyacencia genómica a orden transcripcional",
                    "Convert genomic adjacency to transcriptional order",
                    "Omsæt genomisk naboskab til transkriptionsrækkefølge",
                ),
                (
                    "Forma pares consecutivos dentro del replicón, conserva sólo pares de la "
                    "misma hebra y devuelve cada par en dirección transcripcional.",
                    "Form consecutive pairs within a replicon, retain only same-strand pairs, and "
                    "return each pair in transcriptional direction.",
                    "Dan konsekutive par inden for et replikon, behold kun par på samme streng, og "
                    "returnér hvert par i transkriptionsretningen.",
                ),
                (
                    (
                        "Todos los genes se ordenan juntos por coordenada.",
                        "All genes are sorted together by coordinate.",
                        "Alle gener sorteres samlet efter koordinat.",
                    ),
                    (
                        "La distancia física se calcula entre los límites genómicos.",
                        "Physical distance is calculated between genomic boundaries.",
                        "Den fysiske afstand beregnes mellem genomiske grænser.",
                    ),
                    (
                        "Los pares negativos se invierten al devolver el orden transcripcional.",
                        "Negative-strand pairs are reversed when transcriptional order is returned.",
                        "Minusstrengspar vendes, når transkriptionsrækkefølgen returneres.",
                    ),
                ),
                "def transcriptional_pairs(\n"
                "    genes: list[dict[str, object]]\n"
                ") -> list[tuple[str, str, int]]:\n"
                "    pairs: list[tuple[str, str, int]] = []\n"
                "    replicons = sorted({str(gene['replicon']) for gene in genes})\n"
                "    for replicon in replicons:\n"
                "        ordered = sorted(\n"
                "            (gene for gene in genes if gene['replicon'] == replicon),\n"
                "            key=lambda gene: int(gene['start']),\n"
                "        )\n"
                "        for left, right in zip(ordered, ordered[1:], strict=False):\n"
                "            if left['strand'] != right['strand']:\n"
                "                continue\n"
                "            gap = int(right['start']) - int(left['end']) - 1\n"
                "            if left['strand'] == '+':\n"
                "                upstream, downstream = left, right\n"
                "            else:\n"
                "                upstream, downstream = right, left\n"
                "            pairs.append((str(upstream['id']), str(downstream['id']), gap))\n"
                "    return pairs\n"
                "\n"
                "\n"
                "genes = [\n"
                "    {'id': 'g1', 'replicon': 'chr', 'start': 1, 'end': 100, 'strand': '+'},\n"
                "    {'id': 'g2', 'replicon': 'chr', 'start': 121, 'end': 200, 'strand': '+'},\n"
                "    {'id': 'g3', 'replicon': 'chr', 'start': 301, 'end': 380, 'strand': '-'},\n"
                "    {'id': 'g4', 'replicon': 'chr', 'start': 401, 'end': 500, 'strand': '-'},\n"
                "]\n"
                "print(transcriptional_pairs(genes))",
                "[('g1', 'g2', 20), ('g4', 'g3', 20)]",
                (
                    "Los dos pares tienen el mismo gap físico. El par negativo se devuelve como "
                    "g4→g3 porque la transcripción avanza hacia coordenadas decrecientes.",
                    "Both pairs have the same physical gap. The negative pair is returned as "
                    "g4→g3 because transcription proceeds toward decreasing coordinates.",
                    "Begge par har samme fysiske gap. Minusstrengeparret returneres som g4→g3, "
                    "fordi transkriptionen bevæger sig mod faldende koordinater.",
                ),
            ),
        ),
        practice_exercises=module.practice_exercises
        + (
            practice(
                "m07.bg.p01",
                ActivityType.PIPELINE_DESIGN,
                (
                    "Tres genes aparecen en orden genómico A(-), B(+) y C(-). Un pipeline agrupa "
                    "por hebra antes de crear pares y propone A–C como adyacentes. Corrige el "
                    "procedimiento y explica cómo orientar las ventanas regulatorias.",
                    "Three genes occur in genomic order A(-), B(+), and C(-). A pipeline groups "
                    "by strand before pairing and proposes A–C as adjacent. Correct the procedure "
                    "and explain how regulatory windows should be oriented.",
                    "Tre gener forekommer i genomisk rækkefølge A(-), B(+) og C(-). En pipeline "
                    "grupperer efter streng før pardannelse og foreslår A–C som naboer. Ret "
                    "proceduren og forklar hvordan regulatoriske vinduer skal orienteres.",
                ),
                (
                    (
                        "La adyacencia depende de todos los genes del replicón.",
                        "Adjacency depends on every gene in the replicon.",
                        "Naboskab afhænger af alle gener i replikonet.",
                    ),
                    (
                        "Upstream cambia de dirección en la hebra negativa.",
                        "Upstream changes direction on the negative strand.",
                        "Upstream skifter retning på minusstrengen.",
                    ),
                ),
                (
                    "Agrupar por replicón, ordenar todos los genes por coordenada, formar sólo "
                    "pares consecutivos y después filtrar los pares de la misma hebra. A y C no "
                    "son adyacentes porque B está entre ellos. Para un par negativo válido, "
                    "invertir el orden de genes al expresarlo en dirección transcripcional; extraer "
                    "la región upstream hacia coordenadas mayores y aplicar complemento inverso "
                    "para comparar motivos en orientación 5'→3'. Registrar ensamblaje, convención "
                    "de coordenadas y tratamiento de solapamientos.",
                    "Group by replicon, sort every gene by coordinate, form only consecutive pairs, "
                    "and then filter same-strand pairs. A and C are not adjacent because B lies "
                    "between them. For a valid negative-strand pair, reverse gene order when "
                    "expressing transcriptional direction; extract the upstream region toward "
                    "higher coordinates and reverse-complement it for 5'→3' motif comparison. "
                    "Record assembly, coordinate convention, and overlap handling.",
                    "Gruppér efter replikon, sortér alle gener efter koordinat, dan kun konsekutive "
                    "par, og filtrér derefter par på samme streng. A og C er ikke naboer, fordi B "
                    "ligger imellem dem. For et gyldigt minusstrengspar vendes genrækkefølgen i "
                    "transkriptionsretningen; upstream-regionen udtrækkes mod højere koordinater og "
                    "omvendt-komplementeres til 5'→3'-motivsammenligning. Registrér assembly, "
                    "koordinatkonvention og overlaphåndtering.",
                ),
                (
                    "El procedimiento evita tanto adyacencias falsas como ventanas reguladoras "
                    "invertidas.",
                    "The procedure prevents both false adjacencies and inverted regulatory windows.",
                    "Proceduren forhindrer både falske naboskaber og inverterede regulatoriske vinduer.",
                ),
            ),
        ),
        assessment_items=module.assessment_items
        + (
            objective_mcq(
                "dm847.m07.book.001",
                (
                    "¿Cuál es el orden correcto para construir pares candidatos a operón?",
                    "What is the correct order for constructing candidate operon pairs?",
                    "Hvad er den korrekte rækkefølge til konstruktion af operonkandidatpar?",
                ),
                (
                    (
                        "genomic_first",
                        (
                            "Ordenar todos los genes por replicón, formar adyacencias, filtrar "
                            "por hebra y orientar transcripcionalmente.",
                            "Sort all genes by replicon, form adjacencies, filter by strand, and "
                            "orient transcriptionally.",
                            "Sortér alle gener efter replikon, dan naboskaber, filtrér efter streng, "
                            "og orientér transkriptionelt.",
                        ),
                    ),
                    (
                        "strand_first",
                        (
                            "Agrupar primero por hebra y unir cualquier gen consecutivo del grupo.",
                            "Group by strand first and join any consecutive genes in that group.",
                            "Gruppér først efter streng og forbind alle konsekutive gener i gruppen.",
                        ),
                    ),
                    (
                        "ignore_orientation",
                        (
                            "Ignorar hebra porque la distancia física es suficiente.",
                            "Ignore strand because physical distance is sufficient.",
                            "Ignorér streng, fordi fysisk afstand er tilstrækkelig.",
                        ),
                    ),
                ),
                "genomic_first",
                (
                    "La adyacencia se define con todos los genes; la hebra determina después la "
                    "elegibilidad y el orden transcripcional.",
                    "Adjacency is defined using every gene; strand then determines eligibility and "
                    "transcriptional order.",
                    "Naboskab defineres med alle gener; strengen bestemmer derefter egnethed og "
                    "transkriptionsrækkefølge.",
                ),
            ),
        ),
    )
    return _with_source_basis(
        extended,
        ("sdu-dm847-active-2025", "yachay-molecular-biology-ch19-ch26"),
    )


def apply_ontology_operon_extensions(
    modules: tuple[LocalizedLearningModule, ...],
) -> tuple[LocalizedLearningModule, ...]:
    """Apply the focused M02 and M07 extensions without changing module order."""

    updated: list[LocalizedLearningModule] = []
    for module in modules:
        if module.module_id == "dm847.m02":
            updated.append(_extend_ontologies(module))
        elif module.module_id == "dm847.m07":
            updated.append(_extend_operons(module))
        else:
            updated.append(module)
    return tuple(updated)


__all__ = [
    "DM847_ONTOLOGY_OPERON_SOURCES",
    "apply_ontology_operon_extensions",
    "update_ontology_operon_audit",
    "update_ontology_operon_source_catalog",
]
