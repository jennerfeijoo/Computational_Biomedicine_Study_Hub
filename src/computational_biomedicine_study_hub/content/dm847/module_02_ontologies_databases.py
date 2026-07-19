"""DM847 module 2: biomedical ontologies and systems biology databases."""

from __future__ import annotations

from ...i18n import AppLocale
from ..localized_models import LocalizedLearningModule
from ..models import AssessmentItem, LearningModule
from .standard import StandardModuleSpec, build_module, build_question_bank, materialize_bank

_SPEC = StandardModuleSpec(
    module_id="dm847.m02",
    title=(
        "Ontologías biomédicas y diseño de bases de datos",
        "Biomedical ontologies and database design",
        "Biomedicinske ontologier og databasedesign",
    ),
    summary=(
        "Modela identidad, relaciones, procedencia e integridad en datos biomédicos mediante vocabularios controlados, ontologías, esquemas relacionales y grafos de conocimiento.",
        "Model identity, relationships, provenance, and integrity in biomedical data through controlled vocabularies, ontologies, relational schemas, and knowledge graphs.",
        "Modellér identitet, relationer, proveniens og integritet i biomedicinske data gennem kontrollerede vokabularer, ontologier, relationelle skemaer og vidensgrafer.",
    ),
    objectives=(
        (
            "m02.o1",
            (
                "Distinguir identificadores, nombres, sinónimos y versiones.",
                "Distinguish identifiers, names, synonyms, and versions.",
                "Skelne mellem identifikatorer, navne, synonymer og versioner.",
            ),
        ),
        (
            "m02.o2",
            (
                "Explicar la diferencia entre vocabulario controlado, taxonomía y ontología.",
                "Explain the difference between a controlled vocabulary, taxonomy, and ontology.",
                "Forklare forskellen mellem kontrolleret vokabular, taksonomi og ontologi.",
            ),
        ),
        (
            "m02.o3",
            (
                "Modelar relaciones biomédicas con semántica y dirección explícitas.",
                "Model biomedical relationships with explicit semantics and direction.",
                "Modellere biomedicinske relationer med eksplicit semantik og retning.",
            ),
        ),
        (
            "m02.o4",
            (
                "Diseñar esquemas relacionales normalizados y claves verificables.",
                "Design normalized relational schemas and verifiable keys.",
                "Designe normaliserede relationelle skemaer og verificerbare nøgler.",
            ),
        ),
        (
            "m02.o5",
            (
                "Conservar procedencia, versiones y evidencia en cada afirmación.",
                "Preserve provenance, versions, and evidence for every assertion.",
                "Bevare proveniens, versioner og evidens for hver påstand.",
            ),
        ),
        (
            "m02.o6",
            (
                "Validar consultas, cardinalidades y dependencias antes de interpretar resultados.",
                "Validate queries, cardinalities, and dependencies before interpreting results.",
                "Validere forespørgsler, kardinaliteter og afhængigheder før resultater fortolkes.",
            ),
        ),
    ),
    concepts=(
        (
            "identity-versioning",
            ("Identidad y versionado", "Identity and versioning", "Identitet og versionsstyring"),
            (
                "Un identificador estable debe distinguirse del nombre visible. Los nombres cambian, los sinónimos se solapan y las bases externas actualizan versiones. Una referencia reproducible conserva espacio de nombres, identificador, versión o fecha y, cuando sea posible, checksum o release.",
                "A stable identifier must be distinguished from its display name. Names change, synonyms overlap, and external databases update releases. A reproducible reference retains namespace, identifier, version or date, and when possible a checksum or release.",
                "En stabil identifikator skal adskilles fra det viste navn. Navne ændres, synonymer overlapper, og eksterne databaser opdaterer releases. En reproducerbar reference bevarer namespace, identifikator, version eller dato og om muligt checksum eller release.",
            ),
            (
                (
                    "Los nombres no son claves primarias fiables.",
                    "Names are not reliable primary keys.",
                    "Navne er ikke pålidelige primærnøgler.",
                ),
                (
                    "Una versión forma parte de la identidad analítica.",
                    "A version is part of analytical identity.",
                    "En version er en del af den analytiske identitet.",
                ),
            ),
        ),
        (
            "vocabulary-ontology",
            (
                "Vocabularios, taxonomías y ontologías",
                "Vocabularies, taxonomies, and ontologies",
                "Vokabularer, taksonomier og ontologier",
            ),
            (
                "Un vocabulario controla términos; una taxonomía organiza categorías jerárquicas; una ontología define clases, relaciones, restricciones y, a veces, axiomas que permiten inferencia. La semántica de is_a, part_of, regulates o located_in no es intercambiable.",
                "A vocabulary controls terms; a taxonomy organizes hierarchical categories; an ontology defines classes, relationships, constraints, and sometimes axioms enabling inference. The semantics of is_a, part_of, regulates, or located_in are not interchangeable.",
                "Et vokabular kontrollerer termer; en taksonomi organiserer hierarkiske kategorier; en ontologi definerer klasser, relationer, begrænsninger og undertiden aksiomer, der muliggør inferens. Semantikken i is_a, part_of, regulates og located_in er ikke udskiftelig.",
            ),
            (
                (
                    "Cada relación debe tener significado formal.",
                    "Each relationship should have formal meaning.",
                    "Hver relation bør have formel betydning.",
                ),
                (
                    "La jerarquía no representa todas las dependencias.",
                    "Hierarchy does not represent every dependency.",
                    "Hierarki repræsenterer ikke alle afhængigheder.",
                ),
            ),
        ),
        (
            "graph-semantics",
            ("Semántica de grafos", "Graph semantics", "Grafsemantik"),
            (
                "En afirmación puede representarse como sujeto–predicado–objeto, pero la dirección y el tipo de nodo importan. La transitividad debe declararse: is_a suele permitir herencia, mientras regulates no puede propagarse sin una regla justificada. Los ciclos pueden ser válidos en redes, pero problemáticos en jerarquías.",
                "An assertion can be represented as subject–predicate–object, but direction and node type matter. Transitivity must be declared: is_a often supports inheritance, whereas regulates cannot be propagated without a justified rule. Cycles may be valid in networks but problematic in hierarchies.",
                "En påstand kan repræsenteres som subjekt–prædikat–objekt, men retning og nodetype er vigtige. Transitivitet skal erklæres: is_a understøtter ofte arv, mens regulates ikke kan propageres uden en begrundet regel. Cykler kan være gyldige i netværk, men problematiske i hierarkier.",
            ),
            (
                (
                    "No asumir transitividad universal.",
                    "Do not assume universal transitivity.",
                    "Antag ikke universel transitivitet.",
                ),
                (
                    "Tipo y dirección determinan la interpretación.",
                    "Type and direction determine interpretation.",
                    "Type og retning bestemmer fortolkningen.",
                ),
            ),
        ),
        (
            "relational-design",
            ("Diseño relacional", "Relational design", "Relationelt design"),
            (
                "La normalización separa entidades y relaciones para evitar duplicación, anomalías de actualización y valores multivaluados opacos. Las claves primarias identifican filas; las foráneas expresan integridad referencial; las tablas puente modelan relaciones muchos-a-muchos y pueden almacenar evidencia específica.",
                "Normalization separates entities and relationships to avoid duplication, update anomalies, and opaque multivalued fields. Primary keys identify rows; foreign keys express referential integrity; junction tables model many-to-many relations and may store relation-specific evidence.",
                "Normalisering adskiller entiteter og relationer for at undgå duplikation, opdateringsanomalier og uigennemsigtige multiværdifelter. Primærnøgler identificerer rækker; fremmednøgler udtrykker referentiel integritet; koblingstabeller modellerer mange-til-mange-relationer og kan lagre relationsspecifik evidens.",
            ),
            (
                (
                    "Una celda no debe ocultar listas sin estructura.",
                    "A cell should not hide unstructured lists.",
                    "En celle bør ikke skjule ustrukturerede lister.",
                ),
                (
                    "La cardinalidad pertenece al contrato del esquema.",
                    "Cardinality belongs to the schema contract.",
                    "Kardinalitet tilhører skemakontrakten.",
                ),
            ),
        ),
        (
            "provenance-evidence",
            ("Procedencia y evidencia", "Provenance and evidence", "Proveniens og evidens"),
            (
                "Una afirmación biomédica debe enlazar fuente, método, versión, fecha, muestra o cohorte, nivel de evidencia y transformación. Mezclar predicciones, anotaciones manuales y observaciones experimentales sin etiquetarlas produce una base aparentemente completa pero epistemológicamente incoherente.",
                "A biomedical assertion should link source, method, version, date, sample or cohort, evidence level, and transformation. Mixing predictions, manual annotations, and experimental observations without labels creates an apparently complete but epistemically incoherent database.",
                "En biomedicinsk påstand bør knytte kilde, metode, version, dato, prøve eller kohorte, evidensniveau og transformation. Blanding af prædiktioner, manuelle annotationer og eksperimentelle observationer uden mærkning skaber en tilsyneladende komplet, men epistemisk inkohærent database.",
            ),
            (
                (
                    "Predicción y observación deben distinguirse.",
                    "Prediction and observation must be distinguished.",
                    "Prædiktion og observation skal skelnes.",
                ),
                (
                    "La procedencia debe viajar con el dato derivado.",
                    "Provenance should travel with derived data.",
                    "Proveniens bør følge afledte data.",
                ),
            ),
        ),
        (
            "query-validation",
            ("Consultas y validación", "Queries and validation", "Forespørgsler og validering"),
            (
                "Un join puede multiplicar filas si la cardinalidad real no coincide con la esperada. Antes de interpretar conteos o asociaciones se validan unicidad, cobertura de claves, nulos, duplicados, dirección de relaciones y número de filas antes y después. Una consulta correcta sintácticamente puede ser incorrecta semánticamente.",
                "A join can multiply rows when actual cardinality differs from expectation. Before interpreting counts or associations, validate uniqueness, key coverage, nulls, duplicates, relation direction, and row counts before and after. A syntactically correct query may still be semantically wrong.",
                "Et join kan multiplicere rækker, når den faktiske kardinalitet afviger fra forventningen. Før antal eller associationer fortolkes, valideres unikhed, nøgledækning, null-værdier, dubletter, relationsretning og rækkeantal før og efter. En syntaktisk korrekt forespørgsel kan stadig være semantisk forkert.",
            ),
            (
                (
                    "Validar cardinalidad antes del join.",
                    "Validate cardinality before a join.",
                    "Validér kardinalitet før et join.",
                ),
                (
                    "Los conteos son pruebas de integridad útiles.",
                    "Counts are useful integrity checks.",
                    "Antal er nyttige integritetskontroller.",
                ),
            ),
        ),
    ),
    examples=(
        (
            "m02.e01",
            ("Normalizar un CURIE", "Normalize a CURIE", "Normalisér en CURIE"),
            (
                "Valida identificadores compactos como GO:0008150 sin confundir prefijo y acceso.",
                "Validate compact identifiers such as GO:0008150 without confusing prefix and accession.",
                "Validér kompakte identifikatorer som GO:0008150 uden at forveksle præfiks og accession.",
            ),
            (
                (
                    "El namespace se normaliza por separado.",
                    "The namespace is normalized separately.",
                    "Namespace normaliseres separat.",
                ),
                (
                    "El acceso no se interpreta como número si puede contener ceros significativos.",
                    "The accession is not parsed as an integer when leading zeros matter.",
                    "Accession fortolkes ikke som heltal, når indledende nuller er betydningsfulde.",
                ),
            ),
            """def normalize_curie(raw: str) -> tuple[str, str]:\n    prefix, separator, accession = raw.strip().partition(\":\")\n    if not separator or not prefix or not accession:\n        raise ValueError(\"expected PREFIX:ACCESSION\")\n    return prefix.upper(), accession\n\n\nprint(normalize_curie(\" go:0008150 \"))\n""",
            "('GO', '0008150')",
            (
                "El resultado conserva una identidad descompuesta y verificable.",
                "The result preserves a decomposed, verifiable identity.",
                "Resultatet bevarer en opdelt og verificerbar identitet.",
            ),
        ),
        (
            "m02.e02",
            ("Ancestros transitivos", "Transitive ancestors", "Transitive forfædre"),
            (
                "Recorre relaciones is_a y evita ciclos accidentales.",
                "Traverse is_a relations while avoiding accidental cycles.",
                "Gennemløb is_a-relationer og undgå utilsigtede cykler.",
            ),
            (
                (
                    "La pila contiene términos pendientes.",
                    "The stack contains pending terms.",
                    "Stakken indeholder ventende termer.",
                ),
                (
                    "El conjunto visited evita repetir nodos.",
                    "The visited set prevents repeated nodes.",
                    "Mængden visited forhindrer gentagelse af noder.",
                ),
            ),
            """def ancestors(term: str, parents: dict[str, set[str]]) -> set[str]:\n    visited: set[str] = set()\n    stack = list(parents.get(term, set()))\n    while stack:\n        current = stack.pop()\n        if current in visited:\n            continue\n        visited.add(current)\n        stack.extend(parents.get(current, set()))\n    return visited\n\n\ngraph = {\"T-cell\": {\"lymphocyte\"}, \"lymphocyte\": {\"cell\"}}\nprint(sorted(ancestors(\"T-cell\", graph)))\n""",
            "['cell', 'lymphocyte']",
            (
                "La transitividad sólo es válida porque la relación modelada es is_a.",
                "Transitivity is valid only because the modeled relation is is_a.",
                "Transitivitet er kun gyldig, fordi den modellerede relation er is_a.",
            ),
        ),
        (
            "m02.e03",
            (
                "Comprobar integridad referencial",
                "Check referential integrity",
                "Kontrollér referentiel integritet",
            ),
            (
                "Detecta asociaciones gen–término que apuntan a entidades inexistentes.",
                "Detect gene–term associations pointing to missing entities.",
                "Find gen–term-associationer, der peger på manglende entiteter.",
            ),
            (
                (
                    "Se construyen conjuntos de claves válidas.",
                    "Sets of valid keys are constructed.",
                    "Mængder af gyldige nøgler oprettes.",
                ),
                (
                    "Cada relación se verifica en ambos extremos.",
                    "Each relation is checked at both ends.",
                    "Hver relation kontrolleres i begge ender.",
                ),
            ),
            """def invalid_links(\n    genes: set[str], terms: set[str], links: list[tuple[str, str]]\n) -> list[tuple[str, str]]:\n    return [(gene, term) for gene, term in links if gene not in genes or term not in terms]\n\n\nprint(invalid_links({\"G1\"}, {\"GO:1\"}, [(\"G1\", \"GO:1\"), (\"G2\", \"GO:1\")]))\n""",
            "[('G2', 'GO:1')]",
            (
                "La integridad evita interpretar relaciones huérfanas como evidencia biológica.",
                "Integrity prevents orphaned relations from being interpreted as biological evidence.",
                "Integritet forhindrer, at forældreløse relationer fortolkes som biologisk evidens.",
            ),
        ),
    ),
    practices=(
        (
            "m02.p01",
            "SHORT_ANSWER",
            (
                "Distingue identificador, etiqueta y sinónimo.",
                "Distinguish identifier, label, and synonym.",
                "Skeln mellem identifikator, label og synonym.",
            ),
            (("Piensa en estabilidad.", "Think about stability.", "Tænk på stabilitet."),),
            (
                "El identificador pretende ser estable y único; la etiqueta es el nombre preferido visible; los sinónimos son formas alternativas que no deben actuar como claves.",
                "The identifier is intended to be stable and unique; the label is the preferred display name; synonyms are alternatives that should not act as keys.",
                "Identifikatoren er tiltænkt som stabil og unik; labelen er det foretrukne viste navn; synonymer er alternativer, der ikke bør fungere som nøgler.",
            ),
            (
                "La separación permite renombrar sin romper enlaces.",
                "Separation allows renaming without breaking links.",
                "Adskillelsen muliggør omdøbning uden at bryde links.",
            ),
            "",
        ),
        (
            "m02.p02",
            "MATCHING",
            (
                "Relaciona is_a, part_of, regulates y located_in con su semántica.",
                "Match is_a, part_of, regulates, and located_in to their semantics.",
                "Match is_a, part_of, regulates og located_in med deres semantik.",
            ),
            (
                (
                    "No todas son jerárquicas.",
                    "Not all are hierarchical.",
                    "Ikke alle er hierarkiske.",
                ),
            ),
            (
                "is_a expresa subtipo; part_of composición; regulates influencia regulatoria; located_in localización.",
                "is_a expresses subtype; part_of composition; regulates regulatory influence; located_in location.",
                "is_a udtrykker subtype; part_of komposition; regulates regulatorisk påvirkning; located_in lokalisering.",
            ),
            (
                "La dirección debe conservarse.",
                "Direction must be preserved.",
                "Retningen skal bevares.",
            ),
            "",
        ),
        (
            "m02.p03",
            "DATA_INTERPRETATION",
            (
                "Un join duplica cada gen tres veces. Interpreta.",
                "A join duplicates every gene three times. Interpret it.",
                "Et join duplikerer hvert gen tre gange. Fortolk det.",
            ),
            (("Revisa cardinalidad.", "Inspect cardinality.", "Undersøg kardinalitet."),),
            (
                "La tabla enlazada tiene tres filas por gen o una clave no única. Debe decidirse si la multiplicidad es válida, agregarse previamente o modelarse explícitamente.",
                "The joined table has three rows per gene or a non-unique key. Decide whether multiplicity is valid, aggregate first, or model it explicitly.",
                "Den joinede tabel har tre rækker pr. gen eller en ikke-unik nøgle. Det skal afgøres, om multipliciteten er gyldig, aggregeres først eller modelleres eksplicit.",
            ),
            (
                "No deben interpretarse conteos antes de resolverlo.",
                "Counts should not be interpreted before resolving it.",
                "Antal bør ikke fortolkes før problemet er løst.",
            ),
            "",
        ),
        (
            "m02.p04",
            "PIPELINE_DESIGN",
            (
                "Diseña un esquema para genes, términos y asociaciones con evidencia.",
                "Design a schema for genes, terms, and evidence-bearing associations.",
                "Design et skema for gener, termer og associationer med evidens.",
            ),
            (("Usa una tabla puente.", "Use a junction table.", "Brug en koblingstabel."),),
            (
                "Gene(gene_id,...), Term(term_id,label,ontology_version), GeneTerm(gene_id,term_id,evidence_code,source,release,date), con claves foráneas y unicidad definida.",
                "Gene(gene_id,...), Term(term_id,label,ontology_version), GeneTerm(gene_id,term_id,evidence_code,source,release,date), with foreign keys and defined uniqueness.",
                "Gene(gene_id,...), Term(term_id,label,ontology_version), GeneTerm(gene_id,term_id,evidence_code,source,release,date), med fremmednøgler og defineret unikhed.",
            ),
            (
                "La evidencia pertenece a la asociación, no al gen aislado.",
                "Evidence belongs to the association, not to the gene alone.",
                "Evidensen tilhører associationen, ikke genet alene.",
            ),
            "",
        ),
        (
            "m02.p05",
            "DEBUGGING",
            (
                "Una consulta de descendientes entra en bucle. Diagnostica.",
                "A descendant query loops forever. Diagnose it.",
                "En forespørgsel efter efterkommere kører i ring. Diagnosticér.",
            ),
            (
                (
                    "Busca ciclos o falta de visited.",
                    "Look for cycles or missing visited state.",
                    "Søg efter cykler eller manglende visited-tilstand.",
                ),
            ),
            (
                "Añadir seguimiento de nodos visitados, verificar si la relación debería ser acíclica y reportar el ciclo en vez de ocultarlo.",
                "Track visited nodes, verify whether the relation should be acyclic, and report the cycle instead of hiding it.",
                "Spor besøgte noder, verificér om relationen bør være acyklisk, og rapportér cyklen i stedet for at skjule den.",
            ),
            (
                "Un ciclo puede ser error de datos o una propiedad válida de otra relación.",
                "A cycle may be a data error or a valid property of another relation.",
                "En cykel kan være en datafejl eller en gyldig egenskab ved en anden relation.",
            ),
            "",
        ),
        (
            "m02.p06",
            "ORAL_EXPLANATION",
            (
                "Explica por qué FAIR no equivale a datos abiertos sin restricciones.",
                "Explain why FAIR does not mean unrestricted open data.",
                "Forklar hvorfor FAIR ikke betyder ubegrænset åbne data.",
            ),
            (
                (
                    "Considera privacidad y reutilización.",
                    "Consider privacy and reuse.",
                    "Overvej privatliv og genbrug.",
                ),
            ),
            (
                "FAIR busca datos encontrables, accesibles bajo condiciones claras, interoperables y reutilizables. Datos sensibles pueden requerir acceso controlado y seguir siendo FAIR mediante metadatos, gobernanza y procedimientos.",
                "FAIR seeks data that are findable, accessible under clear conditions, interoperable, and reusable. Sensitive data may require controlled access and still be FAIR through metadata, governance, and procedures.",
                "FAIR søger data, der er findbare, tilgængelige under klare betingelser, interoperable og genanvendelige. Følsomme data kan kræve kontrolleret adgang og stadig være FAIR gennem metadata, governance og procedurer.",
            ),
            (
                "Accesible no significa anónimo ni público.",
                "Accessible does not mean anonymous or public.",
                "Tilgængelig betyder ikke anonym eller offentlig.",
            ),
            "",
        ),
        (
            "m02.p07",
            "ORDERING",
            (
                "Ordena una integración: identificar releases, mapear IDs, validar claves, unir, comprobar conteos, interpretar.",
                "Order an integration: identify releases, map IDs, validate keys, join, check counts, interpret.",
                "Ordén en integration: identificér releases, kortlæg ID'er, validér nøgler, join, kontrollér antal, fortolk.",
            ),
            (
                (
                    "La interpretación ocurre al final.",
                    "Interpretation comes last.",
                    "Fortolkning kommer til sidst.",
                ),
            ),
            (
                "Identificar releases → mapear IDs → validar claves → unir → comprobar conteos → interpretar.",
                "Identify releases → map IDs → validate keys → join → check counts → interpret.",
                "Identificér releases → kortlæg ID'er → validér nøgler → join → kontrollér antal → fortolk.",
            ),
            (
                "Cada paso conserva trazabilidad.",
                "Each step preserves traceability.",
                "Hvert trin bevarer sporbarhed.",
            ),
            "",
        ),
        (
            "m02.p08",
            "FILL_IN_THE_BLANK",
            (
                "Una relación muchos-a-muchos se modela normalmente mediante una tabla ________.",
                "A many-to-many relationship is normally modeled through a ________ table.",
                "En mange-til-mange-relation modelleres normalt gennem en ________ tabel.",
            ),
            (
                (
                    "También se llama junction.",
                    "It is also called a junction table.",
                    "Den kaldes også en junction table.",
                ),
            ),
            ("puente", "junction", "koblings"),
            (
                "La tabla almacena las claves de ambos extremos y atributos de la relación.",
                "The table stores keys from both ends and relationship attributes.",
                "Tabellen lagrer nøgler fra begge ender og relationsattributter.",
            ),
            "",
        ),
    ),
    mcqs=(
        (
            "001",
            (
                "¿Qué debe usarse como clave estable?",
                "What should be used as a stable key?",
                "Hvad bør bruges som stabil nøgle?",
            ),
            (
                (
                    "id",
                    (
                        "Identificador persistente",
                        "Persistent identifier",
                        "Persistent identifikator",
                    ),
                ),
                ("label", ("Etiqueta visible", "Display label", "Visningslabel")),
                ("synonym", ("Primer sinónimo", "First synonym", "Første synonym")),
            ),
            "id",
            (
                "Las etiquetas y sinónimos pueden cambiar o repetirse.",
                "Labels and synonyms may change or repeat.",
                "Labels og synonymer kan ændres eller gentages.",
            ),
        ),
        (
            "002",
            (
                "¿Qué añade una ontología sobre un vocabulario?",
                "What does an ontology add beyond a vocabulary?",
                "Hvad tilføjer en ontologi ud over et vokabular?",
            ),
            (
                (
                    "relations",
                    (
                        "Relaciones y restricciones formales",
                        "Formal relations and constraints",
                        "Formelle relationer og begrænsninger",
                    ),
                ),
                ("colors", ("Colores", "Colors", "Farver")),
                ("compression", ("Compresión", "Compression", "Komprimering")),
            ),
            "relations",
            (
                "La ontología modela semántica y puede permitir inferencia.",
                "An ontology models semantics and may enable inference.",
                "En ontologi modellerer semantik og kan muliggøre inferens.",
            ),
        ),
        (
            "003",
            (
                "¿Cuál relación suele ser transitiva?",
                "Which relation is commonly transitive?",
                "Hvilken relation er ofte transitiv?",
            ),
            (
                ("isa", ("is_a", "is_a", "is_a")),
                ("regulates", ("regulates", "regulates", "regulates")),
                ("binds", ("binds", "binds", "binds")),
            ),
            "isa",
            (
                "La herencia de clases suele seguir is_a.",
                "Class inheritance commonly follows is_a.",
                "Klassearv følger ofte is_a.",
            ),
        ),
        (
            "004",
            (
                "¿Dónde debe almacenarse el código de evidencia de una anotación gen–término?",
                "Where should the evidence code for a gene–term annotation be stored?",
                "Hvor bør evidenskoden for en gen–term-annotation lagres?",
            ),
            (
                ("association", ("En la asociación", "On the association", "På associationen")),
                ("gene", ("Sólo en el gen", "Only on the gene", "Kun på genet")),
                ("term", ("Sólo en el término", "Only on the term", "Kun på termen")),
            ),
            "association",
            (
                "La evidencia respalda esa relación concreta.",
                "Evidence supports that specific relation.",
                "Evidensen understøtter den konkrete relation.",
            ),
        ),
        (
            "005",
            (
                "¿Qué expresa una clave foránea?",
                "What does a foreign key express?",
                "Hvad udtrykker en fremmednøgle?",
            ),
            (
                (
                    "reference",
                    ("Integridad referencial", "Referential integrity", "Referentiel integritet"),
                ),
                ("style", ("Estilo", "Style", "Stil")),
                ("order", ("Orden visual", "Visual order", "Visuel rækkefølge")),
            ),
            "reference",
            (
                "La clave exige que la entidad referenciada exista.",
                "The key requires the referenced entity to exist.",
                "Nøglen kræver, at den refererede entitet findes.",
            ),
        ),
        (
            "006",
            (
                "¿Qué riesgo indica un join que multiplica filas?",
                "What risk is indicated by a join multiplying rows?",
                "Hvilken risiko indikerer et join, der multiplicerer rækker?",
            ),
            (
                (
                    "cardinality",
                    ("Cardinalidad inesperada", "Unexpected cardinality", "Uventet kardinalitet"),
                ),
                ("encoding", ("Codificación de texto", "Text encoding", "Tekstkodning")),
                ("color", ("Color de tabla", "Table color", "Tabelfarve")),
            ),
            "cardinality",
            (
                "Una clave no única puede inflar conteos.",
                "A non-unique key may inflate counts.",
                "En ikke-unik nøgle kan oppuste antal.",
            ),
        ),
        (
            "007",
            (
                "¿Qué referencia es más reproducible?",
                "Which reference is more reproducible?",
                "Hvilken reference er mest reproducerbar?",
            ),
            (
                (
                    "versioned",
                    (
                        "ID + namespace + release",
                        "ID + namespace + release",
                        "ID + namespace + release",
                    ),
                ),
                ("name", ("Sólo nombre", "Name only", "Kun navn")),
                ("memory", ("Recordar la página", "Remember the page", "Huske siden")),
            ),
            "versioned",
            (
                "La versión fija el estado de la fuente.",
                "The release fixes the state of the source.",
                "Releasen fastlægger kildens tilstand.",
            ),
        ),
        (
            "008",
            (
                "¿Qué modelo representa mejor una relación muchos-a-muchos?",
                "Which model best represents a many-to-many relation?",
                "Hvilken model repræsenterer bedst en mange-til-mange-relation?",
            ),
            (
                ("junction", ("Tabla puente", "Junction table", "Koblingstabel")),
                ("cell", ("Lista en una celda", "List in one cell", "Liste i én celle")),
                ("duplicate", ("Duplicar columnas", "Duplicate columns", "Duplikere kolonner")),
            ),
            "junction",
            (
                "La tabla puente mantiene estructura e integridad.",
                "A junction table preserves structure and integrity.",
                "En koblingstabel bevarer struktur og integritet.",
            ),
        ),
        (
            "009",
            (
                "¿Qué debe distinguir una base de conocimiento?",
                "What should a knowledge base distinguish?",
                "Hvad bør en vidensbase skelne mellem?",
            ),
            (
                (
                    "evidence",
                    (
                        "Predicción, observación y curación",
                        "Prediction, observation, and curation",
                        "Prædiktion, observation og kuratering",
                    ),
                ),
                ("font", ("Fuentes tipográficas", "Fonts", "Skrifttyper")),
                ("screen", ("Tamaño de pantalla", "Screen size", "Skærmstørrelse")),
            ),
            "evidence",
            (
                "Los niveles de evidencia no son equivalentes.",
                "Evidence levels are not equivalent.",
                "Evidensniveauer er ikke ækvivalente.",
            ),
        ),
        (
            "010",
            (
                "¿Qué se valida antes de interpretar una consulta?",
                "What is validated before interpreting a query?",
                "Hvad valideres før en forespørgsel fortolkes?",
            ),
            (
                (
                    "integrity",
                    (
                        "Claves, nulos, duplicados y conteos",
                        "Keys, nulls, duplicates, and counts",
                        "Nøgler, null-værdier, dubletter og antal",
                    ),
                ),
                ("title", ("Título del gráfico", "Plot title", "Graftitel")),
                ("theme", ("Tema visual", "Visual theme", "Visuelt tema")),
            ),
            "integrity",
            (
                "Una consulta puede ser sintácticamente válida y semánticamente errónea.",
                "A query can be syntactically valid and semantically wrong.",
                "En forespørgsel kan være syntaktisk gyldig og semantisk forkert.",
            ),
        ),
    ),
    true_false=(
        (
            "011",
            (
                "Una etiqueta visible es siempre un identificador único.",
                "A display label is always a unique identifier.",
                "En visningslabel er altid en unik identifikator.",
            ),
            False,
            (
                "Las etiquetas pueden cambiar y repetirse.",
                "Labels may change and repeat.",
                "Labels kan ændres og gentages.",
            ),
        ),
        (
            "012",
            (
                "is_a y regulates tienen la misma semántica.",
                "is_a and regulates have the same semantics.",
                "is_a og regulates har samme semantik.",
            ),
            False,
            (
                "Una expresa subtipo y la otra influencia regulatoria.",
                "One expresses subtype and the other regulatory influence.",
                "Den ene udtrykker subtype og den anden regulatorisk påvirkning.",
            ),
        ),
        (
            "013",
            (
                "Una ontología puede contener axiomas para inferencia.",
                "An ontology may contain axioms for inference.",
                "En ontologi kan indeholde aksiomer til inferens.",
            ),
            True,
            (
                "Esa capacidad la distingue de un simple listado.",
                "That capability distinguishes it from a simple list.",
                "Denne evne adskiller den fra en simpel liste.",
            ),
        ),
        (
            "014",
            (
                "Todas las relaciones de un grafo biomédico son transitivas.",
                "All relationships in a biomedical graph are transitive.",
                "Alle relationer i en biomedicinsk graf er transitive.",
            ),
            False,
            (
                "La transitividad depende del predicado.",
                "Transitivity depends on the predicate.",
                "Transitivitet afhænger af prædikatet.",
            ),
        ),
        (
            "015",
            (
                "Una tabla puente puede almacenar atributos de la relación.",
                "A junction table may store relationship attributes.",
                "En koblingstabel kan lagre relationsattributter.",
            ),
            True,
            (
                "Por ejemplo evidencia, fuente o fecha.",
                "For example evidence, source, or date.",
                "For eksempel evidens, kilde eller dato.",
            ),
        ),
        (
            "016",
            (
                "La procedencia puede descartarse después de integrar datos.",
                "Provenance can be discarded after data integration.",
                "Proveniens kan kasseres efter dataintegration.",
            ),
            False,
            (
                "Debe conservarse para auditoría y reproducibilidad.",
                "It must be retained for audit and reproducibility.",
                "Den skal bevares til audit og reproducerbarhed.",
            ),
        ),
        (
            "017",
            (
                "Un join muchos-a-muchos puede aumentar el número de filas.",
                "A many-to-many join can increase row count.",
                "Et mange-til-mange-join kan øge rækkeantallet.",
            ),
            True,
            (
                "Cada combinación compatible genera una fila.",
                "Each compatible combination produces a row.",
                "Hver kompatibel kombination producerer en række.",
            ),
        ),
        (
            "018",
            (
                "FAIR exige que todo dato biomédico sensible sea público.",
                "FAIR requires all sensitive biomedical data to be public.",
                "FAIR kræver, at alle følsomme biomedicinske data er offentlige.",
            ),
            False,
            (
                "El acceso puede estar controlado bajo condiciones claras.",
                "Access may be controlled under clear conditions.",
                "Adgang kan være kontrolleret under klare betingelser.",
            ),
        ),
        (
            "019",
            (
                "Una consulta sintácticamente correcta puede ser semánticamente errónea.",
                "A syntactically correct query may be semantically wrong.",
                "En syntaktisk korrekt forespørgsel kan være semantisk forkert.",
            ),
            True,
            (
                "La selección o cardinalidad pueden no corresponder a la pregunta.",
                "Selection or cardinality may not match the question.",
                "Udvælgelse eller kardinalitet kan afvige fra spørgsmålet.",
            ),
        ),
        (
            "020",
            (
                "Los nombres de genes son universales y nunca ambiguos.",
                "Gene names are universal and never ambiguous.",
                "Gennavne er universelle og aldrig tvetydige.",
            ),
            False,
            (
                "Existen alias, especies y convenciones diferentes.",
                "Aliases, species, and differing conventions exist.",
                "Der findes aliaser, arter og forskellige konventioner.",
            ),
        ),
    ),
    tutor=(
        (
            "Las bases biomédicas confiables separan identidad de presentación. Los identificadores deben conservar namespace y versión; las etiquetas y sinónimos facilitan lectura y búsqueda, pero no sustituyen claves. Los vocabularios controlan términos, las taxonomías organizan jerarquías y las ontologías formalizan clases, relaciones y restricciones. En grafos, tipo, dirección y transitividad deben declararse. En bases relacionales, normalización, claves y tablas puente preservan integridad y cardinalidad. Cada afirmación necesita procedencia y nivel de evidencia. Antes de interpretar una integración se validan releases, mapeos, unicidad, nulos, duplicados y conteos. La interoperabilidad no elimina privacidad ni gobernanza.",
            "Trustworthy biomedical databases separate identity from presentation. Identifiers retain namespace and version; labels and synonyms support reading and search but do not replace keys. Vocabularies control terms, taxonomies organize hierarchies, and ontologies formalize classes, relationships, and constraints. In graphs, type, direction, and transitivity must be declared. In relational databases, normalization, keys, and junction tables preserve integrity and cardinality. Every assertion requires provenance and evidence level. Before interpreting an integration, validate releases, mappings, uniqueness, nulls, duplicates, and counts. Interoperability does not remove privacy or governance.",
            "Pålidelige biomedicinske databaser adskiller identitet fra præsentation. Identifikatorer bevarer namespace og version; labels og synonymer understøtter læsning og søgning, men erstatter ikke nøgler. Vokabularer kontrollerer termer, taksonomier organiserer hierarkier, og ontologier formaliserer klasser, relationer og begrænsninger. I grafer skal type, retning og transitivitet erklæres. I relationelle databaser bevarer normalisering, nøgler og koblingstabeller integritet og kardinalitet. Hver påstand kræver proveniens og evidensniveau. Før en integration fortolkes, valideres releases, mappings, unikhed, null-værdier, dubletter og antal. Interoperabilitet fjerner ikke privatliv eller governance.",
        ),
        (
            (
                "Los identificadores estables no son etiquetas.",
                "Stable identifiers are not labels.",
                "Stabile identifikatorer er ikke labels.",
            ),
            (
                "Las relaciones tienen semántica y dirección.",
                "Relationships have semantics and direction.",
                "Relationer har semantik og retning.",
            ),
            (
                "La normalización reduce anomalías.",
                "Normalization reduces anomalies.",
                "Normalisering reducerer anomalier.",
            ),
            (
                "La evidencia pertenece a la afirmación.",
                "Evidence belongs to the assertion.",
                "Evidens tilhører påstanden.",
            ),
            (
                "Versiones y releases afectan reproducibilidad.",
                "Versions and releases affect reproducibility.",
                "Versioner og releases påvirker reproducerbarhed.",
            ),
            (
                "Los joins requieren validación de cardinalidad.",
                "Joins require cardinality validation.",
                "Joins kræver kardinalitetsvalidering.",
            ),
        ),
        (
            ("Usar nombres como claves.", "Using names as keys.", "At bruge navne som nøgler."),
            (
                "Asumir que toda relación es transitiva.",
                "Assuming every relation is transitive.",
                "At antage at alle relationer er transitive.",
            ),
            (
                "Guardar listas opacas en una celda.",
                "Storing opaque lists in one cell.",
                "At lagre uigennemsigtige lister i én celle.",
            ),
            (
                "Eliminar procedencia tras integrar.",
                "Dropping provenance after integration.",
                "At fjerne proveniens efter integration.",
            ),
            (
                "Interpretar conteos inflados por joins.",
                "Interpreting counts inflated by joins.",
                "At fortolke antal oppustet af joins.",
            ),
            (
                "Confundir acceso FAIR con acceso público.",
                "Confusing FAIR access with public access.",
                "At forveksle FAIR-adgang med offentlig adgang.",
            ),
        ),
        (
            (
                "¿Cuál es la identidad estable de esta entidad?",
                "What is the stable identity of this entity?",
                "Hvad er denne entitets stabile identitet?",
            ),
            (
                "¿Qué versión de la fuente se utilizó?",
                "Which source version was used?",
                "Hvilken kildeversion blev brugt?",
            ),
            (
                "¿Qué significa exactamente la relación?",
                "What exactly does the relationship mean?",
                "Hvad betyder relationen præcist?",
            ),
            (
                "¿Cuál es la cardinalidad esperada?",
                "What is the expected cardinality?",
                "Hvad er den forventede kardinalitet?",
            ),
            (
                "¿Qué evidencia respalda la afirmación?",
                "What evidence supports the assertion?",
                "Hvilken evidens understøtter påstanden?",
            ),
            (
                "¿Cómo cambiaron los conteos tras el join?",
                "How did counts change after the join?",
                "Hvordan ændrede antallene sig efter joinet?",
            ),
        ),
        (
            (
                "Distingue identidad, etiqueta y sinónimo.",
                "Distinguishes identity, label, and synonym.",
                "Skelner identitet, label og synonym.",
            ),
            (
                "Usa relaciones con semántica correcta.",
                "Uses relationships with correct semantics.",
                "Bruger relationer med korrekt semantik.",
            ),
            (
                "Diseña claves y cardinalidades explícitas.",
                "Designs explicit keys and cardinalities.",
                "Designer eksplicitte nøgler og kardinaliteter.",
            ),
            (
                "Conserva procedencia y versiones.",
                "Preserves provenance and versions.",
                "Bevarer proveniens og versioner.",
            ),
            (
                "Valida integridad antes de interpretar.",
                "Validates integrity before interpretation.",
                "Validerer integritet før fortolkning.",
            ),
            (
                "Reconoce límites de privacidad y acceso.",
                "Recognizes privacy and access constraints.",
                "Anerkender begrænsninger for privatliv og adgang.",
            ),
        ),
        (
            (
                "No inventar identificadores o mapeos.",
                "Do not invent identifiers or mappings.",
                "Opfind ikke identifikatorer eller mappings.",
            ),
            (
                "No inferir transitividad sin axioma.",
                "Do not infer transitivity without an axiom.",
                "Inferér ikke transitivitet uden aksiom.",
            ),
            (
                "No ocultar predicciones como observaciones.",
                "Do not hide predictions as observations.",
                "Skjul ikke prædiktioner som observationer.",
            ),
            (
                "No recomendar exposición de datos sensibles.",
                "Do not recommend exposing sensitive data.",
                "Anbefal ikke eksponering af følsomme data.",
            ),
            (
                "Responder en el idioma activo.",
                "Answer in the active language.",
                "Svar på det aktive sprog.",
            ),
        ),
        (
            "Gene Ontology documentation and relation semantics.",
            "OBO Foundry principles and identifier conventions.",
            "FAIR Guiding Principles for scientific data management.",
            "Relational database normalization and integrity constraints.",
            "RDF/OWL knowledge representation concepts.",
            "Active SDU DM847 course description and database learning outcomes.",
        ),
    ),
)

LOCALIZED_MODULE_02_ONTOLOGIES_DATABASES: LocalizedLearningModule = build_module(_SPEC)
LOCALIZED_OBJECTIVE_QUESTION_BANK_02 = build_question_bank(_SPEC)


def materialize_module_02_question_bank(
    locale: AppLocale | str = AppLocale.SPANISH_SPAIN,
) -> tuple[AssessmentItem, ...]:
    return materialize_bank(LOCALIZED_OBJECTIVE_QUESTION_BANK_02, locale)


MODULE_02_ONTOLOGIES_DATABASES: LearningModule = (
    LOCALIZED_MODULE_02_ONTOLOGIES_DATABASES.materialize(AppLocale.SPANISH_SPAIN)
)
OBJECTIVE_QUESTION_BANK_02 = materialize_module_02_question_bank()

__all__ = [
    "LOCALIZED_MODULE_02_ONTOLOGIES_DATABASES",
    "LOCALIZED_OBJECTIVE_QUESTION_BANK_02",
    "MODULE_02_ONTOLOGIES_DATABASES",
    "OBJECTIVE_QUESTION_BANK_02",
    "materialize_module_02_question_bank",
]
