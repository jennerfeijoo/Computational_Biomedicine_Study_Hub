"""DM847 module 1: molecular information, regulation, and biological context."""

from __future__ import annotations

from ...i18n import AppLocale
from ..localized_models import LocalizedLearningModule
from ..models import AssessmentItem, LearningModule
from .standard import StandardModuleSpec, build_module, build_question_bank, materialize_bank

_SPEC = StandardModuleSpec(
    module_id="dm847.m01",
    title=(
        "Información molecular, regulación y contexto biológico",
        "Molecular information, regulation, and biological context",
        "Molekylær information, regulering og biologisk kontekst",
    ),
    summary=(
        "Convierte ADN, ARN, proteínas, regulación y genética bacteriana en representaciones computables con orientación, coordenadas, procedencia e incertidumbre explícitas.",
        "Turn DNA, RNA, proteins, regulation, and bacterial genetics into computable representations with explicit orientation, coordinates, provenance, and uncertainty.",
        "Omsæt DNA, RNA, proteiner, regulering og bakteriel genetik til beregnelige repræsentationer med eksplicit orientering, koordinater, proveniens og usikkerhed.",
    ),
    objectives=(
        ("m01.o1", ("Explicar el dogma central como flujo de información condicionado por contexto.", "Explain the central dogma as context-dependent information flow.", "Forklare det centrale dogme som kontekstafhængigt informationsflow.")),
        ("m01.o2", ("Representar secuencias con alfabetos, orientación y símbolos ambiguos explícitos.", "Represent sequences with explicit alphabets, orientation, and ambiguity symbols.", "Repræsentere sekvenser med eksplicitte alfabeter, orientering og tvetydighedssymboler.")),
        ("m01.o3", ("Convertir coordenadas biológicas a intervalos computacionales sin errores de borde.", "Convert biological coordinates into computational intervals without boundary errors.", "Konvertere biologiske koordinater til beregningsintervaller uden grænsefejl.")),
        ("m01.o4", ("Distinguir secuencia, anotación, señal experimental y estado regulatorio.", "Distinguish sequence, annotation, experimental signal, and regulatory state.", "Skelne mellem sekvens, annotation, eksperimentelt signal og regulatorisk tilstand.")),
        ("m01.o5", ("Explicar operones, transferencia horizontal y particularidades de fagos.", "Explain operons, horizontal transfer, and phage-specific features.", "Forklare operoner, horisontal overførsel og fagspecifikke egenskaber.")),
        ("m01.o6", ("Transformar una pregunta biomédica en entidad, operación, evidencia y validación.", "Transform a biomedical question into entity, operation, evidence, and validation.", "Omsætte et biomedicinsk spørgsmål til entitet, operation, evidens og validering.")),
    ),
    concepts=(
        (
            "information-flow",
            ("Dogma central como modelo", "Central dogma as a model", "Det centrale dogme som model"),
            (
                "ADN, ARN y proteína describen capas relacionadas, pero la transformación concreta depende de región, hebra, marco, código genético, procesamiento del ARN y contexto celular. El modelo computacional debe conservar estos supuestos en vez de tratar una cadena como una entidad biológica completa.",
                "DNA, RNA, and protein describe related layers, but each transformation depends on region, strand, frame, genetic code, RNA processing, and cellular context. A computational model must preserve these assumptions rather than treating a string as a complete biological entity.",
                "DNA, RNA og protein beskriver relaterede lag, men hver transformation afhænger af region, streng, læseramme, genetisk kode, RNA-processering og cellulær kontekst. En beregningsmodel skal bevare disse antagelser frem for at behandle en streng som en komplet biologisk entitet.",
            ),
            (
                ("Una secuencia no identifica por sí sola un gen o transcrito.", "A sequence alone does not identify a gene or transcript.", "En sekvens alene identificerer ikke et gen eller transkript."),
                ("Marco, hebra y procedencia forman parte del dato.", "Frame, strand, and provenance are part of the data.", "Læseramme, streng og proveniens er en del af data."),
            ),
        ),
        (
            "alphabets-ambiguity",
            ("Alfabetos y ambigüedad", "Alphabets and ambiguity", "Alfabeter og tvetydighed"),
            (
                "El ADN canónico usa A, C, G y T; el ARN sustituye T por U; las proteínas usan códigos de aminoácidos. Los símbolos IUPAC representan incertidumbre o mezclas. Aceptar N, R o Y puede ser apropiado para almacenamiento, pero algunas operaciones requieren resolver o rechazar la ambigüedad.",
                "Canonical DNA uses A, C, G, and T; RNA replaces T with U; proteins use amino-acid codes. IUPAC symbols represent uncertainty or mixtures. Accepting N, R, or Y may be appropriate for storage, while some operations must resolve or reject ambiguity.",
                "Kanonisk DNA bruger A, C, G og T; RNA erstatter T med U; proteiner bruger aminosyrekoder. IUPAC-symboler repræsenterer usikkerhed eller blandinger. N, R eller Y kan accepteres ved lagring, mens visse operationer skal opløse eller afvise tvetydighed.",
            ),
            (
                ("La política de ambigüedad depende de la operación.", "Ambiguity policy depends on the operation.", "Tvetydighedspolitikken afhænger af operationen."),
                ("No mezclar T y U sin conversión declarada.", "Do not mix T and U without a declared conversion.", "Bland ikke T og U uden en erklæret konvertering."),
            ),
        ),
        (
            "strand-coordinates",
            ("Hebra, orientación y coordenadas", "Strand, orientation, and coordinates", "Streng, orientering og koordinater"),
            (
                "Las hebras de ADN son antiparalelas y el complemento inverso expresa la hebra opuesta en dirección 5'→3'. Los formatos biológicos alternan entre coordenadas 0-based o 1-based y extremos inclusivos o exclusivos. Cada intervalo debe conservar sistema de referencia, ensamblaje, hebra y convención.",
                "DNA strands are antiparallel, and the reverse complement expresses the opposite strand in the 5'→3' direction. Biological formats vary between zero- or one-based coordinates and inclusive or exclusive ends. Every interval should retain reference system, assembly, strand, and convention.",
                "DNA-strenge er antiparallelle, og det omvendte komplement udtrykker den modsatte streng i 5'→3'-retning. Biologiske formater varierer mellem nul- og én-baserede koordinater samt inklusive og eksklusive ender. Hvert interval bør bevare referencesystem, assembly, streng og konvention.",
            ),
            (
                ("Complementar e invertir son operaciones distintas.", "Complementing and reversing are distinct operations.", "Komplementering og vending er forskellige operationer."),
                ("La longitud esperada detecta errores de coordenadas.", "Expected length detects coordinate errors.", "Forventet længde opdager koordinatfejl."),
            ),
        ),
        (
            "regulation-epigenetics",
            ("Regulación y epigenética", "Regulation and epigenetics", "Regulering og epigenetik"),
            (
                "La expresión depende de promotores, potenciadores, represores, factores de transcripción, accesibilidad de cromatina y modificaciones químicas. Una marca epigenética es una medición asociada a posición, muestra, ensayo y estado celular; no equivale necesariamente a cambiar la secuencia de bases.",
                "Expression depends on promoters, enhancers, repressors, transcription factors, chromatin accessibility, and chemical modifications. An epigenetic mark is a measurement tied to position, sample, assay, and cell state; it does not necessarily change the base sequence.",
                "Ekspression afhænger af promotorer, enhancere, repressorer, transkriptionsfaktorer, kromatintilgængelighed og kemiske modifikationer. Et epigenetisk mærke er en måling knyttet til position, prøve, assay og celletilstand; det ændrer ikke nødvendigvis basesekvensen.",
            ),
            (
                ("Secuencia y señal experimental son capas diferentes.", "Sequence and experimental signal are different layers.", "Sekvens og eksperimentelt signal er forskellige lag."),
                ("Asociación regulatoria no implica causalidad.", "Regulatory association does not imply causality.", "Regulatorisk association indebærer ikke kausalitet."),
            ),
        ),
        (
            "bacterial-genetics",
            ("Genética bacteriana y operones", "Bacterial genetics and operons", "Bakteriel genetik og operoner"),
            (
                "En operón agrupa genes transcritos conjuntamente bajo control regulatorio compartido. Distancia intergénica, orientación, conservación y coexpresión aportan evidencia, pero ninguna señal aislada demuestra un operón. Plásmidos y transferencia horizontal alteran la relación entre historia génica e historia del organismo.",
                "An operon groups genes transcribed together under shared regulatory control. Intergenic distance, orientation, conservation, and co-expression provide evidence, but no single signal proves an operon. Plasmids and horizontal transfer alter the relationship between gene history and organism history.",
                "Et operon grupperer gener, der transskriberes sammen under fælles regulatorisk kontrol. Intergen afstand, orientering, konservering og co-ekspression giver evidens, men intet enkelt signal beviser et operon. Plasmider og horisontal overførsel ændrer forholdet mellem genhistorie og organismens historie.",
            ),
            (
                ("Predicción de operones integra varias evidencias.", "Operon prediction integrates multiple evidence sources.", "Operonprædiktion integrerer flere evidenskilder."),
                ("La transferencia horizontal rompe supuestos filogenéticos simples.", "Horizontal transfer breaks simple phylogenetic assumptions.", "Horisontal overførsel bryder simple fylogenetiske antagelser."),
            ),
        ),
        (
            "phage-context",
            ("Fagos y contexto evolutivo", "Phages and evolutionary context", "Fager og evolutionær kontekst"),
            (
                "Los fagos pueden seguir ciclos líticos o lisogénicos, integrarse como profagos y transportar genes. Sus genomas compactos, solapamientos y alta diversidad dificultan la anotación por homología. El contexto genómico y la arquitectura de módulos funcionales son tan importantes como una coincidencia local.",
                "Phages may follow lytic or lysogenic cycles, integrate as prophages, and transport genes. Their compact genomes, overlaps, and high diversity complicate homology-based annotation. Genomic context and functional module architecture can be as important as a local match.",
                "Fager kan følge lytiske eller lysogene cyklusser, integreres som profager og transportere gener. Deres kompakte genomer, overlap og høje diversitet vanskeliggør homologibaseret annotation. Genomisk kontekst og funktionel modularkitektur kan være lige så vigtige som et lokalt match.",
            ),
            (
                ("Una coincidencia débil no basta para anotar función.", "A weak match is insufficient for functional annotation.", "Et svagt match er utilstrækkeligt til funktionel annotation."),
                ("El contexto distingue profagos de regiones bacterianas ordinarias.", "Context helps distinguish prophages from ordinary bacterial regions.", "Kontekst hjælper med at skelne profager fra almindelige bakterielle regioner."),
            ),
        ),
    ),
    examples=(
        (
            "m01.e01",
            ("Complemento inverso validado", "Validated reverse complement", "Valideret omvendt komplement"),
            ("Normaliza una secuencia de ADN y calcula su complemento inverso rechazando símbolos fuera del alfabeto permitido.", "Normalize a DNA sequence and compute its reverse complement while rejecting symbols outside the allowed alphabet.", "Normalisér en DNA-sekvens og beregn dens omvendte komplement, mens symboler uden for det tilladte alfabet afvises."),
            (("Normalizar evita diferencias por espacios o minúsculas.", "Normalization removes whitespace and case differences.", "Normalisering fjerner forskelle i mellemrum og store/små bogstaver."), ("La tabla de traducción conserva símbolos IUPAC seleccionados.", "The translation table preserves selected IUPAC symbols.", "Oversættelsestabellen bevarer udvalgte IUPAC-symboler.")),
            """def reverse_complement(raw: str) -> str:\n    sequence = \"\".join(raw.split()).upper()\n    allowed = set(\"ACGTRYN\")\n    invalid = set(sequence) - allowed\n    if invalid:\n        raise ValueError(f\"invalid symbols: {sorted(invalid)}\")\n    table = str.maketrans(\"ACGTRYN\", \"TGCAYRN\")\n    return sequence.translate(table)[::-1]\n\n\nprint(reverse_complement(\"ACG TRY\"))\n""",
            "RYACGT",
            ("El resultado mantiene orientación 5'→3' y una política de ambigüedad explícita.", "The result retains 5'→3' orientation and an explicit ambiguity policy.", "Resultatet bevarer 5'→3'-orientering og en eksplicit tvetydighedspolitik."),
        ),
        (
            "m01.e02",
            ("Conversión de coordenadas", "Coordinate conversion", "Koordinatkonvertering"),
            ("Extrae un intervalo 1-based inclusivo mediante un slice 0-based con final exclusivo.", "Extract a one-based inclusive interval using a zero-based half-open slice.", "Udtræk et én-baseret inklusivt interval med et nul-baseret halvåbent slice."),
            (("El inicio se desplaza una posición.", "The start is shifted by one position.", "Starten forskydes én position."), ("El extremo inclusivo coincide con el final exclusivo de Python.", "The inclusive end matches Python's exclusive stop.", "Den inklusive slutposition svarer til Pythons eksklusive stop.")),
            """def extract_1_based(sequence: str, start: int, end: int) -> str:\n    if start < 1 or end < start or end > len(sequence):\n        raise ValueError(\"invalid interval\")\n    fragment = sequence[start - 1 : end]\n    assert len(fragment) == end - start + 1\n    return fragment\n\n\nprint(extract_1_based(\"AACCGGTT\", 3, 6))\n""",
            "CCGG",
            ("La aserción de longitud hace visible el contrato de coordenadas.", "The length assertion makes the coordinate contract explicit.", "Længdeassertionen gør koordinatkontrakten eksplicit."),
        ),
        (
            "m01.e03",
            ("Puntuación de evidencia de operón", "Operon evidence score", "Evidensscore for operon"),
            ("Combina orientación, distancia y coexpresión en una puntuación didáctica interpretable.", "Combine orientation, distance, and co-expression in an interpretable teaching score.", "Kombinér orientering, afstand og co-ekspression i en fortolkelig undervisningsscore."),
            (("Cada evidencia recibe un peso visible.", "Each evidence source receives a visible weight.", "Hver evidenskilde får en synlig vægt."), ("El umbral no constituye una regla biológica universal.", "The threshold is not a universal biological rule.", "Tærsklen er ikke en universel biologisk regel.")),
            """def operon_score(same_strand: bool, distance_bp: int, correlation: float) -> float:\n    score = 0.0\n    score += 1.0 if same_strand else -1.0\n    score += max(0.0, 1.0 - distance_bp / 500.0)\n    score += max(-1.0, min(1.0, correlation))\n    return round(score, 3)\n\n\nprint(operon_score(True, 80, 0.86))\n""",
            "2.7",
            ("El ejemplo enseña integración de evidencia; un modelo real requiere datos, calibración y validación independientes.", "The example teaches evidence integration; a real model requires data, calibration, and independent validation.", "Eksemplet lærer evidensintegration; en reel model kræver data, kalibrering og uafhængig validering."),
        ),
    ),
    practices=(
        ("m01.p01", "SHORT_ANSWER", ("Distingue gen, transcrito y CDS.", "Distinguish gene, transcript, and CDS.", "Skeln mellem gen, transkript og CDS."), (("Incluye entidad y coordenadas.", "Include entity and coordinates.", "Medtag entitet og koordinater."),), ("Un gen es una entidad genómica regulada; un transcrito es un producto de ARN concreto; una CDS es la región traducida dentro de un transcrito o anotación.", "A gene is a regulated genomic entity; a transcript is a specific RNA product; a CDS is the translated region within a transcript or annotation.", "Et gen er en reguleret genomisk entitet; et transkript er et specifikt RNA-produkt; en CDS er den translaterede region i et transkript eller en annotation."), ("No deben usarse como sinónimos.", "They should not be used as synonyms.", "De bør ikke bruges som synonymer."), ""),
        ("m01.p02", "CODE_TRACING", ("Traza el complemento inverso de ACGN.", "Trace the reverse complement of ACGN.", "Gennemgå det omvendte komplement af ACGN."), (("Complementa y después invierte.", "Complement, then reverse.", "Komplementér og vend derefter."),), ("NCGT", "NCGT", "NCGT"), ("N permanece ambiguo y la salida se expresa 5'→3'.", "N remains ambiguous and the output is expressed 5'→3'.", "N forbliver tvetydig, og output udtrykkes 5'→3'."), ""),
        ("m01.p03", "FILL_IN_THE_BLANK", ("El intervalo biológico [start, end] 1-based inclusivo se extrae como sequence[____:____].", "The one-based inclusive biological interval [start, end] is extracted as sequence[____:____].", "Det én-baserede inklusive biologiske interval [start, end] udtrækkes som sequence[____:____]."), (("Convierte sólo el inicio.", "Convert only the start.", "Konvertér kun starten."),), ("start - 1, end", "start - 1, end", "start - 1, end"), ("Python usa inicio 0-based y final exclusivo.", "Python uses a zero-based start and exclusive stop.", "Python bruger nul-baseret start og eksklusiv slut."), ""),
        ("m01.p04", "DATA_INTERPRETATION", ("Una región tiene alta metilación y baja expresión. ¿Qué puede concluirse?", "A region has high methylation and low expression. What can be concluded?", "En region har høj methylering og lav ekspression. Hvad kan konkluderes?"), (("Separa asociación y causalidad.", "Separate association from causality.", "Adskil association fra kausalitet."),), ("Existe una asociación en esa muestra y ensayo; no se demuestra que la metilación cause la reducción ni que el efecto sea general.", "There is an association in that sample and assay; it does not prove methylation caused the reduction or that the effect generalizes.", "Der er en association i den prøve og det assay; det beviser ikke, at methylering forårsagede reduktionen, eller at effekten generaliserer."), ("Se requieren diseño experimental, covariables y replicación.", "Experimental design, covariates, and replication are required.", "Eksperimentelt design, kovariater og replikation er nødvendige."), ""),
        ("m01.p05", "PIPELINE_DESIGN", ("Diseña los metadatos mínimos para almacenar una variante genómica.", "Design minimum metadata for storing a genomic variant.", "Design minimale metadata til lagring af en genomisk variant."), (("Incluye referencia y coordenadas.", "Include reference and coordinates.", "Medtag reference og koordinater."),), ("Ensamblaje, cromosoma/contig, posición y convención, alelo de referencia, alelo alternativo, hebra cuando proceda, muestra, método, calidad y procedencia.", "Assembly, chromosome/contig, position and convention, reference allele, alternate allele, strand when relevant, sample, method, quality, and provenance.", "Assembly, kromosom/contig, position og konvention, referenceallel, alternativ allel, streng når relevant, prøve, metode, kvalitet og proveniens."), ("Sin ensamblaje y alelos una posición es ambigua.", "Without assembly and alleles a position is ambiguous.", "Uden assembly og alleler er en position tvetydig."), ""),
        ("m01.p06", "MATCHING", ("Relaciona promotor, enhancer, CDS y marca epigenética con su capa.", "Match promoter, enhancer, CDS, and epigenetic mark to their layer.", "Match promotor, enhancer, CDS og epigenetisk mærke med deres lag."), (("Distingue anotación y medición.", "Distinguish annotation and measurement.", "Skeln mellem annotation og måling."),), ("Promotor/enhancer/CDS son anotaciones funcionales o estructurales; la marca epigenética es una observación dependiente de muestra y ensayo.", "Promoter/enhancer/CDS are functional or structural annotations; an epigenetic mark is a sample- and assay-dependent observation.", "Promotor/enhancer/CDS er funktionelle eller strukturelle annotationer; et epigenetisk mærke er en prøve- og assayafhængig observation."), ("Una misma coordenada puede tener varias capas de información.", "The same coordinate may have several information layers.", "Den samme koordinat kan have flere informationslag."), ""),
        ("m01.p07", "ORAL_EXPLANATION", ("Explica por qué un árbol de genes puede diferir del árbol de especies.", "Explain why a gene tree may differ from a species tree.", "Forklar hvorfor et gentræ kan afvige fra et artstræ."), (("Incluye transferencia horizontal y duplicación.", "Include horizontal transfer and duplication.", "Medtag horisontal overførsel og duplikation."),), ("Transferencia horizontal, duplicación, pérdida, recombinación y señal limitada pueden producir historias génicas distintas de la historia de especies.", "Horizontal transfer, duplication, loss, recombination, and limited signal can produce gene histories different from species history.", "Horisontal overførsel, duplikation, tab, rekombination og begrænset signal kan give genhistorier, der afviger fra artshistorien."), ("La discordancia no implica automáticamente un error.", "Discordance does not automatically imply an error.", "Uoverensstemmelse indebærer ikke automatisk en fejl."), ""),
        ("m01.p08", "DEBUGGING", ("Una extracción devuelve una base menos de lo esperado. Diagnostica.", "An extraction returns one fewer base than expected. Diagnose it.", "Et udtræk returnerer én base mindre end forventet. Diagnosticér."), (("Compara convención y longitud.", "Compare convention and length.", "Sammenlign konvention og længde."),), ("Revisar si el origen es 1-based inclusivo y el slice se escribió con end - 1; comprobar longitud end - start + 1 y documentar la conversión.", "Check whether the source is one-based inclusive and the slice incorrectly used end - 1; verify length end - start + 1 and document the conversion.", "Kontrollér om kilden er én-baseret inklusiv, og om slicet fejlagtigt brugte end - 1; verificér længden end - start + 1 og dokumentér konverteringen."), ("Es un error off-by-one clásico.", "This is a classic off-by-one error.", "Det er en klassisk off-by-one-fejl."), ""),
    ),
    mcqs=(
        ("001", ("¿Qué metadato es imprescindible para interpretar una posición genómica?", "Which metadata is essential for interpreting a genomic position?", "Hvilke metadata er nødvendige for at fortolke en genomisk position?"), (("assembly", ("Ensamblaje de referencia", "Reference assembly", "Reference-assembly")), ("color", ("Color de visualización", "Display color", "Visningsfarve")), ("author", ("Inicial del analista", "Analyst initial", "Analytikerens initial"))), "assembly", ("La misma coordenada puede apuntar a bases distintas en ensamblajes diferentes.", "The same coordinate may point to different bases in different assemblies.", "Den samme koordinat kan pege på forskellige baser i forskellige assemblies.")),
        ("002", ("¿Qué operación produce la hebra opuesta en orientación 5'→3'?", "Which operation produces the opposite strand in 5'→3' orientation?", "Hvilken operation producerer den modsatte streng i 5'→3'-orientering?"), (("rc", ("Complemento inverso", "Reverse complement", "Omvendt komplement")), ("reverse", ("Sólo invertir", "Reverse only", "Kun vending")), ("upper", ("Convertir a mayúsculas", "Uppercase", "Store bogstaver"))), "rc", ("La antiparalelidad exige complementar e invertir.", "Antiparallelism requires complementing and reversing.", "Antiparallelitet kræver komplementering og vending.")),
        ("003", ("¿Qué símbolo IUPAC representa una base no determinada?", "Which IUPAC symbol represents an undetermined base?", "Hvilket IUPAC-symbol repræsenterer en ubestemt base?"), (("n", ("N", "N", "N")), ("u", ("U", "U", "U")), ("x", ("X", "X", "X"))), "n", ("N puede representar cualquiera de las bases canónicas.", "N may represent any canonical base.", "N kan repræsentere enhver kanonisk base.")),
        ("004", ("¿Qué longitud tiene un intervalo 1-based inclusivo [4, 9]?", "What is the length of the one-based inclusive interval [4, 9]?", "Hvad er længden af det én-baserede inklusive interval [4, 9]?"), (("six", ("6", "6", "6")), ("five", ("5", "5", "5")), ("nine", ("9", "9", "9"))), "six", ("La longitud es end - start + 1.", "Length is end - start + 1.", "Længden er end - start + 1.")),
        ("005", ("¿Qué capa depende directamente de muestra y ensayo?", "Which layer directly depends on sample and assay?", "Hvilket lag afhænger direkte af prøve og assay?"), (("signal", ("Señal epigenética medida", "Measured epigenetic signal", "Målt epigenetisk signal")), ("alphabet", ("Alfabeto de ADN", "DNA alphabet", "DNA-alfabet")), ("codon", ("Definición de codón", "Codon definition", "Definition af kodon"))), "signal", ("Las señales experimentales requieren contexto de muestra y protocolo.", "Experimental signals require sample and protocol context.", "Eksperimentelle signaler kræver prøve- og protokolkontekst.")),
        ("006", ("¿Qué evidencia aislada demuestra un operón?", "Which single evidence source proves an operon?", "Hvilken enkelt evidenskilde beviser et operon?"), (("none", ("Ninguna por sí sola", "None by itself", "Ingen alene")), ("distance", ("Sólo distancia corta", "Short distance alone", "Kort afstand alene")), ("strand", ("Sólo misma hebra", "Same strand alone", "Samme streng alene"))), "none", ("La predicción integra varias señales y necesita validación.", "Prediction integrates several signals and requires validation.", "Prædiktion integrerer flere signaler og kræver validering.")),
        ("007", ("¿Qué proceso puede separar historia génica e historia de especies?", "Which process can separate gene history from species history?", "Hvilken proces kan adskille genhistorie fra artshistorie?"), (("hgt", ("Transferencia horizontal", "Horizontal transfer", "Horisontal overførsel")), ("uppercase", ("Mayúsculas", "Uppercasing", "Store bogstaver")), ("sorting", ("Ordenación lexicográfica", "Lexicographic sorting", "Leksikografisk sortering"))), "hgt", ("Un gen transferido puede tener afinidad con un linaje distante.", "A transferred gene may be related to a distant lineage.", "Et overført gen kan være beslægtet med en fjern linje.")),
        ("008", ("¿Qué describe mejor un profago?", "What best describes a prophage?", "Hvad beskriver bedst en profag?"), (("integrated", ("Genoma fágico integrado", "Integrated phage genome", "Integreret faggenom")), ("protein", ("Proteína ribosomal", "Ribosomal protein", "Ribosomalt protein")), ("intron", ("Intrón eucariota", "Eukaryotic intron", "Eukaryot intron"))), "integrated", ("Un profago es material fágico integrado o mantenido en el hospedador.", "A prophage is phage material integrated or maintained in the host.", "En profag er fagmateriale integreret eller vedligeholdt i værten.")),
        ("009", ("¿Qué debe definirse antes de calcular contenido GC con N presentes?", "What must be defined before computing GC content with Ns present?", "Hvad skal defineres før beregning af GC-indhold med N'er?"), (("policy", ("Política para bases ambiguas", "Ambiguity policy", "Politik for tvetydige baser")), ("font", ("Tipografía", "Font", "Skrifttype")), ("plot", ("Color del gráfico", "Plot color", "Plotfarve"))), "policy", ("Excluir, imputar o incluir ambiguos cambia el denominador.", "Excluding, imputing, or including ambiguity changes the denominator.", "Eksklusion, imputering eller inklusion af tvetydighed ændrer nævneren.")),
        ("010", ("¿Cuál es la primera unidad de una formulación computacional?", "What is the first unit in a computational formulation?", "Hvad er den første enhed i en beregningsformulering?"), (("question", ("Pregunta y unidad de análisis", "Question and unit of analysis", "Spørgsmål og analyseenhed")), ("answer", ("Respuesta deseada", "Desired answer", "Ønsket svar")), ("plot", ("Tipo de gráfico", "Plot type", "Graftype"))), "question", ("La representación y el algoritmo dependen de una pregunta delimitada.", "Representation and algorithm depend on a bounded question.", "Repræsentation og algoritme afhænger af et afgrænset spørgsmål.")),
    ),
    true_false=(
        ("011", ("Una cadena de ADN identifica por sí sola un gen concreto.", "A DNA string by itself identifies a specific gene.", "En DNA-streng identificerer alene et bestemt gen."), False, ("Faltan referencia, coordenadas, hebra y anotación.", "Reference, coordinates, strand, and annotation are missing.", "Reference, koordinater, streng og annotation mangler.")),
        ("012", ("El complemento sin inversión equivale al complemento inverso.", "Complement without reversal equals reverse complement.", "Komplement uden vending svarer til omvendt komplement."), False, ("Son operaciones distintas.", "They are distinct operations.", "Det er forskellige operationer.")),
        ("013", ("Python usa normalmente slices con extremo final exclusivo.", "Python normally uses slices with an exclusive stop.", "Python bruger normalt slices med eksklusiv slut."), True, ("sequence[a:b] incluye a y excluye b.", "sequence[a:b] includes a and excludes b.", "sequence[a:b] inkluderer a og ekskluderer b.")),
        ("014", ("Una marca epigenética siempre cambia la secuencia de bases.", "An epigenetic mark always changes the base sequence.", "Et epigenetisk mærke ændrer altid basesekvensen."), False, ("Generalmente es una modificación o señal asociada, no una sustitución de base.", "It is generally an associated modification or signal, not a base substitution.", "Det er generelt en associeret modifikation eller et signal, ikke en basesubstitution.")),
        ("015", ("La baja expresión junto a alta metilación demuestra causalidad.", "Low expression with high methylation proves causality.", "Lav ekspression sammen med høj methylering beviser kausalitet."), False, ("La observación es asociativa sin diseño causal.", "The observation is associative without causal design.", "Observationen er associativ uden kausalt design.")),
        ("016", ("Los genes de un operón suelen compartir regulación transcripcional.", "Genes in an operon commonly share transcriptional regulation.", "Gener i et operon deler ofte transkriptionsregulering."), True, ("Esa es una característica definitoria del concepto.", "That is a defining feature of the concept.", "Det er et definerende træk ved begrebet.")),
        ("017", ("La transferencia horizontal puede introducir genes de linajes distantes.", "Horizontal transfer can introduce genes from distant lineages.", "Horisontal overførsel kan introducere gener fra fjerne linjer."), True, ("Por ello un árbol génico puede discordar del árbol de especies.", "Therefore a gene tree may disagree with the species tree.", "Derfor kan et gentræ afvige fra artstræet.")),
        ("018", ("Los genomas de fagos siempre son fáciles de anotar por homología.", "Phage genomes are always easy to annotate by homology.", "Faggenomer er altid lette at annotere ved homologi."), False, ("Su diversidad y compactación dificultan la anotación.", "Their diversity and compactness complicate annotation.", "Deres diversitet og kompakthed vanskeliggør annotation.")),
        ("019", ("La política para símbolos ambiguos debe documentarse.", "The policy for ambiguous symbols should be documented.", "Politikken for tvetydige symboler bør dokumenteres."), True, ("Afecta resultados y reproducibilidad.", "It affects results and reproducibility.", "Den påvirker resultater og reproducerbarhed.")),
        ("020", ("Los ejemplos de este módulo constituyen protocolos clínicos validados.", "The examples in this module are validated clinical protocols.", "Eksemplerne i dette modul er validerede kliniske protokoller."), False, ("Son ejercicios computacionales didácticos.", "They are computational teaching exercises.", "De er beregningsmæssige undervisningsøvelser.")),
    ),
    tutor=(
        (
            "La bioinformática comienza representando entidades biológicas sin borrar su contexto. ADN, ARN y proteína se conectan mediante transformaciones condicionadas por hebra, marco, región, procesamiento y código genético. Las secuencias requieren alfabetos y políticas explícitas para ambigüedad. Las coordenadas deben conservar ensamblaje, convención y orientación. Regulación y epigenética añaden señales dependientes de muestra y ensayo que no deben confundirse con la secuencia. En bacterias, operones, plásmidos y transferencia horizontal exigen integrar contexto y múltiples evidencias. Los fagos presentan genomas compactos, ciclos diversos y regiones integradas. Toda pregunta debe convertirse en unidad de análisis, representación, operación, criterio de éxito y validación, manteniendo procedencia e incertidumbre.",
            "Bioinformatics begins by representing biological entities without erasing context. DNA, RNA, and protein are connected by transformations conditioned on strand, frame, region, processing, and genetic code. Sequences require explicit alphabets and ambiguity policies. Coordinates must retain assembly, convention, and orientation. Regulation and epigenetics add sample- and assay-dependent signals that should not be confused with sequence. In bacteria, operons, plasmids, and horizontal transfer require integration of context and multiple evidence sources. Phages have compact genomes, diverse cycles, and integrated regions. Every question should become a unit of analysis, representation, operation, success criterion, and validation while retaining provenance and uncertainty.",
            "Bioinformatik begynder med at repræsentere biologiske entiteter uden at fjerne konteksten. DNA, RNA og protein forbindes gennem transformationer, der afhænger af streng, læseramme, region, processering og genetisk kode. Sekvenser kræver eksplicitte alfabeter og tvetydighedspolitikker. Koordinater skal bevare assembly, konvention og orientering. Regulering og epigenetik tilføjer prøve- og assayafhængige signaler, som ikke må forveksles med sekvens. I bakterier kræver operoner, plasmider og horisontal overførsel integration af kontekst og flere evidenskilder. Fager har kompakte genomer, forskellige cyklusser og integrerede regioner. Hvert spørgsmål bør omsættes til analyseenhed, repræsentation, operation, succeskriterium og validering med bevaret proveniens og usikkerhed.",
        ),
        (
            ("Entidad biológica y cadena computacional no son sinónimos.", "Biological entity and computational string are not synonyms.", "Biologisk entitet og beregningsstreng er ikke synonymer."),
            ("La orientación debe acompañar toda operación dependiente de hebra.", "Orientation must accompany every strand-dependent operation.", "Orientering skal følge enhver strengafhængig operation."),
            ("La longitud valida conversiones de coordenadas.", "Length validates coordinate conversions.", "Længde validerer koordinatkonverteringer."),
            ("Las señales reguladoras dependen de contexto celular y experimental.", "Regulatory signals depend on cellular and experimental context.", "Regulatoriske signaler afhænger af cellulær og eksperimentel kontekst."),
            ("Predicciones de operones combinan evidencia.", "Operon predictions combine evidence.", "Operonprædiktioner kombinerer evidens."),
            ("La transferencia horizontal altera historias génicas.", "Horizontal transfer alters gene histories.", "Horisontal overførsel ændrer genhistorier."),
        ),
        (
            ("Confundir gen, transcrito y CDS.", "Confusing gene, transcript, and CDS.", "At forveksle gen, transkript og CDS."),
            ("Olvidar invertir al calcular el complemento inverso.", "Forgetting reversal when computing reverse complement.", "At glemme vending ved beregning af omvendt komplement."),
            ("Mezclar sistemas de coordenadas.", "Mixing coordinate systems.", "At blande koordinatsystemer."),
            ("Interpretar correlación epigenética como causalidad.", "Interpreting epigenetic correlation as causality.", "At fortolke epigenetisk korrelation som kausalitet."),
            ("Tratar una señal de operón como prueba definitiva.", "Treating one operon signal as definitive proof.", "At behandle ét operonsignal som endeligt bevis."),
            ("Suponer que todo gen sigue la filogenia de especies.", "Assuming every gene follows species phylogeny.", "At antage at hvert gen følger artsfylogenien."),
        ),
        (
            ("¿Qué entidad exacta representa esta cadena?", "Which exact entity does this string represent?", "Hvilken præcis entitet repræsenterer denne streng?"),
            ("¿Cuál es la orientación y la convención de coordenadas?", "What are the orientation and coordinate convention?", "Hvad er orienteringen og koordinatkonventionen?"),
            ("¿Qué política se aplica a bases ambiguas?", "Which policy applies to ambiguous bases?", "Hvilken politik gælder for tvetydige baser?"),
            ("¿La evidencia es secuencia, anotación o señal experimental?", "Is the evidence sequence, annotation, or experimental signal?", "Er evidensen sekvens, annotation eller eksperimentelt signal?"),
            ("¿Qué evidencia alternativa apoyaría el operón?", "What alternative evidence would support the operon?", "Hvilken alternativ evidens ville støtte operonet?"),
            ("¿Cómo se validará fuera de los datos usados para formular el modelo?", "How will it be validated outside the data used to formulate the model?", "Hvordan valideres det uden for de data, der blev brugt til at formulere modellen?"),
        ),
        (
            ("Define correctamente las entidades moleculares.", "Correctly defines molecular entities.", "Definerer molekylære entiteter korrekt."),
            ("Conserva orientación, ensamblaje y coordenadas.", "Preserves orientation, assembly, and coordinates.", "Bevarer orientering, assembly og koordinater."),
            ("Distingue secuencia de medición experimental.", "Distinguishes sequence from experimental measurement.", "Skelner sekvens fra eksperimentel måling."),
            ("Integra evidencia bacteriana sin sobreafirmar.", "Integrates bacterial evidence without overclaiming.", "Integrerer bakteriel evidens uden overfortolkning."),
            ("Expone incertidumbre y limitaciones.", "States uncertainty and limitations.", "Angiver usikkerhed og begrænsninger."),
            ("Propone validaciones reproducibles.", "Proposes reproducible validation.", "Foreslår reproducerbar validering."),
        ),
        (
            ("No presentar asociaciones como mecanismos causales.", "Do not present associations as causal mechanisms.", "Præsenter ikke associationer som kausale mekanismer."),
            ("No inventar anotaciones o coordenadas de referencia.", "Do not invent annotations or reference coordinates.", "Opfind ikke annotationer eller referencekoordinater."),
            ("No convertir ejemplos didácticos en recomendaciones clínicas.", "Do not turn teaching examples into clinical recommendations.", "Omsæt ikke undervisningseksempler til kliniske anbefalinger."),
            ("No omitir políticas de ambigüedad.", "Do not omit ambiguity policies.", "Udelad ikke tvetydighedspolitikker."),
            ("Responder en el idioma activo con términos técnicos precisos.", "Answer in the active language with precise technical terms.", "Svar på det aktive sprog med præcise tekniske termer."),
        ),
        (
            "Alberts et al., Molecular Biology of the Cell, central dogma and gene regulation.",
            "NCBI sequence conventions and IUPAC nucleotide codes.",
            "SAM/BED/GFF coordinate and strand conventions.",
            "Reviews on bacterial operon prediction and horizontal gene transfer.",
            "Phage genomics and prophage annotation literature.",
            "Active SDU DM847 course description and learning outcomes.",
        ),
    ),
)

LOCALIZED_MODULE_01_MOLECULAR_INFORMATION: LocalizedLearningModule = build_module(_SPEC)
LOCALIZED_OBJECTIVE_QUESTION_BANK_01 = build_question_bank(_SPEC)


def materialize_module_01_question_bank(
    locale: AppLocale | str = AppLocale.SPANISH_SPAIN,
) -> tuple[AssessmentItem, ...]:
    return materialize_bank(LOCALIZED_OBJECTIVE_QUESTION_BANK_01, locale)


MODULE_01_MOLECULAR_INFORMATION: LearningModule = LOCALIZED_MODULE_01_MOLECULAR_INFORMATION.materialize(
    AppLocale.SPANISH_SPAIN
)
OBJECTIVE_QUESTION_BANK_01 = materialize_module_01_question_bank()

__all__ = [
    "LOCALIZED_MODULE_01_MOLECULAR_INFORMATION",
    "LOCALIZED_OBJECTIVE_QUESTION_BANK_01",
    "MODULE_01_MOLECULAR_INFORMATION",
    "OBJECTIVE_QUESTION_BANK_01",
    "materialize_module_01_question_bank",
]
