"""Book-grounded extensions for DM857 strings, dictionaries, and sets."""

from __future__ import annotations

from dataclasses import replace

from ...learning.activity_types import ActivityType
from ..localized_models import LocalizedLearningModule, LocalizedTutorSupportPacket
from .authoring import concept, example, objective, objective_mcq, practice
from .book_grounded_extensions import ModuleSourceAudit


def _with_source_basis(
    module: LocalizedLearningModule,
    source_ids: tuple[str, ...],
) -> LocalizedLearningModule:
    tutor = module.tutor_support
    merged = tuple(dict.fromkeys((*tutor.source_basis, *source_ids)))
    updated_tutor: LocalizedTutorSupportPacket = replace(
        tutor,
        source_basis=merged,
    )
    return replace(module, tutor_support=updated_tutor)


def update_strings_mappings_audit(
    audit: tuple[ModuleSourceAudit, ...],
) -> tuple[ModuleSourceAudit, ...]:
    """Mark M05 and M07 reviewed only after their extensions are present."""
    findings = {
        "dm857.m05": (
            "Existing coverage of sequence semantics, immutability, slicing, traversal, search, "
            "normalization, parsing, validation, formatting, Unicode-aware comparison, and text "
            "pipelines is consistent. Regular expressions required one explicit introductory "
            "treatment because Think Python's third edition includes them in its string sequence."
        ),
        "dm857.m07": (
            "Existing coverage of mappings, hashable keys, safe access, mutation, frequency "
            "tables, grouping, nested schemas, set algebra, and structure selection is "
            "consistent. The hash-table mechanism, collision handling, and average-versus-worst "
            "case lookup cost required one explicit model."
        ),
    }
    changes = {
        "dm857.m05": (
            "Added an original regular-expression boundary explanation, deterministic fullmatch "
            "example, debugging exercise, and stable objective item."
        ),
        "dm857.m07": (
            "Added an original hash-table and collision explanation, deterministic bucket-model "
            "example, interpretation exercise, and stable objective item."
        ),
    }

    updated: list[ModuleSourceAudit] = []
    for item in audit:
        if item.module_id in findings:
            updated.append(
                replace(
                    item,
                    state="consistent",
                    finding=findings[item.module_id],
                    implemented_change=changes[item.module_id],
                )
            )
        else:
            updated.append(item)
    return tuple(updated)


def _extend_strings(module: LocalizedLearningModule) -> LocalizedLearningModule:
    """Add bounded regular-expression use to M05."""
    extended = replace(
        module,
        objectives=module.objectives
        + (
            objective(
                "m05.bg.o1",
                (
                    "Elegir entre operaciones de cadenas y expresiones regulares, y validar el "
                    "alcance completo de un patrón.",
                    "Choose between string operations and regular expressions, and validate the "
                    "full scope of a pattern.",
                    "Vælge mellem strengoperationer og regulære udtryk samt validere hele "
                    "mønsterets omfang.",
                ),
            ),
        ),
        concepts=module.concepts
        + (
            concept(
                "regex-validation-boundaries",
                (
                    "Expresiones regulares y límites de validación",
                    "Regular expressions and validation boundaries",
                    "Regulære udtryk og valideringsgrænser",
                ),
                (
                    "Una expresión regular describe una familia de cadenas mediante literales, "
                    "clases de caracteres, cuantificadores y alternativas. Es útil cuando la "
                    "estructura textual no se expresa con claridad mediante una sola llamada a "
                    "split, startswith o isdigit. En Python conviene escribir patrones como "
                    "cadenas raw para que las barras invertidas permanezcan legibles. search "
                    "acepta una coincidencia en cualquier parte del texto; fullmatch exige que "
                    "todo el texto cumpla el patrón. Una expresión regular valida forma léxica, "
                    "pero no demuestra que el identificador exista, que una fecha sea posible o "
                    "que el dato tenga significado biológico.",
                    "A regular expression describes a family of strings through literals, "
                    "character classes, quantifiers, and alternatives. It is useful when textual "
                    "structure is not expressed clearly by one call to split, startswith, or "
                    "isdigit. In Python, raw strings keep backslashes in patterns readable. "
                    "search accepts a match anywhere in the text, whereas fullmatch requires the "
                    "entire text to satisfy the pattern. A regular expression validates lexical "
                    "form, but it does not prove that an identifier exists, a date is possible, "
                    "or a value has biological meaning.",
                    "Et regulært udtryk beskriver en familie af strenge med litteraler, "
                    "tegnklasser, kvantifikatorer og alternativer. Det er nyttigt, når "
                    "tekststrukturen ikke udtrykkes klart med ét kald til split, startswith eller "
                    "isdigit. I Python holder raw-strenge omvendte skråstreger læsbare. search "
                    "accepterer et match hvor som helst i teksten, mens fullmatch kræver, at hele "
                    "teksten opfylder mønsteret. Et regulært udtryk validerer leksikalsk form, men "
                    "beviser ikke, at et id findes, at en dato er mulig, eller at en værdi har "
                    "biologisk betydning.",
                ),
                (
                    (
                        "Usa operaciones simples de cadenas cuando expresan mejor el contrato.",
                        "Use simple string operations when they express the contract more clearly.",
                        "Brug simple strengoperationer, når de udtrykker kontrakten tydeligere.",
                    ),
                    (
                        "Las cadenas raw reducen la doble interpretación de barras invertidas.",
                        "Raw strings reduce the double interpretation of backslashes.",
                        "Raw-strenge reducerer dobbeltfortolkning af omvendte skråstreger.",
                    ),
                    (
                        "fullmatch valida toda la entrada; search sólo necesita una coincidencia "
                        "parcial.",
                        "fullmatch validates the entire input; search needs only a partial match.",
                        "fullmatch validerer hele inputtet; search kræver kun et delvist match.",
                    ),
                    (
                        "La forma sintáctica y la validez semántica son contratos diferentes.",
                        "Syntactic form and semantic validity are different contracts.",
                        "Syntaktisk form og semantisk gyldighed er forskellige kontrakter.",
                    ),
                ),
            ),
        ),
        worked_examples=module.worked_examples
        + (
            example(
                "m05.bg.e01",
                (
                    "Validar el identificador completo",
                    "Validate the complete identifier",
                    "Validér hele identifikatoren",
                ),
                (
                    "Comprueba un prefijo didáctico seguido exactamente por tres dígitos sin "
                    "aceptar texto adicional antes o después.",
                    "Check a teaching prefix followed by exactly three digits without accepting "
                    "additional text before or after it.",
                    "Kontrollér et undervisningspræfiks efterfulgt af præcis tre cifre uden at "
                    "acceptere ekstra tekst før eller efter.",
                ),
                (
                    (
                        "Compila un patrón raw con una clase de dígitos y un cuantificador.",
                        "Compile a raw pattern with a digit class and a quantifier.",
                        "Kompilér et raw-mønster med en cifferklasse og en kvantifikator.",
                    ),
                    (
                        "Aplica fullmatch porque el contrato se refiere al identificador entero.",
                        "Apply fullmatch because the contract concerns the whole identifier.",
                        "Anvend fullmatch, fordi kontrakten gælder hele identifikatoren.",
                    ),
                ),
                'import re\n\npattern = re.compile(r"SMP-\\d{3}")\n'
                'for code in ("SMP-104", "xSMP-104", "SMP-10A"):\n'
                "    print(bool(pattern.fullmatch(code)))",
                "True\nFalse\nFalse",
                (
                    "Sólo la primera cadena satisface por completo el prefijo y los tres dígitos. "
                    "Los valores son didácticos y no representan un sistema clínico oficial.",
                    "Only the first string fully satisfies the prefix and three digits. The "
                    "values are instructional and do not represent an official clinical system.",
                    "Kun den første streng opfylder hele præfikset og de tre cifre. Værdierne er "
                    "til undervisning og repræsenterer ikke et officielt klinisk system.",
                ),
            ),
        ),
        practice_exercises=module.practice_exercises
        + (
            practice(
                "m05.bg.p01",
                ActivityType.DEBUGGING,
                (
                    "El validador usa re.search(r'SMP-\\d{3}', text) y acepta "
                    "'prefix-SMP-104-extra'. Corrige el contrato para validar toda la entrada y "
                    "explica por qué el resultado anterior era un falso positivo.",
                    "The validator uses re.search(r'SMP-\\d{3}', text) and accepts "
                    "'prefix-SMP-104-extra'. Fix the contract so it validates the whole input and "
                    "explain why the previous result was a false positive.",
                    "Validatoren bruger re.search(r'SMP-\\d{3}', text) og accepterer "
                    "'prefix-SMP-104-extra'. Ret kontrakten, så hele inputtet valideres, og forklar "
                    "hvorfor det tidligere resultat var falsk positivt.",
                ),
                (
                    (
                        "La función elegida permite coincidencias parciales.",
                        "The selected function permits partial matches.",
                        "Den valgte funktion tillader delvise match.",
                    ),
                    (
                        "El contrato exige que el patrón consuma toda la cadena.",
                        "The contract requires the pattern to consume the entire string.",
                        "Kontrakten kræver, at mønsteret dækker hele strengen.",
                    ),
                ),
                (
                    "Usa bool(re.fullmatch(r'SMP-\\d{3}', text)) o un patrón compilado con "
                    "fullmatch. search encontró una subcadena válida dentro de una entrada que no "
                    "cumplía el formato completo.",
                    "Use bool(re.fullmatch(r'SMP-\\d{3}', text)) or a compiled pattern with "
                    "fullmatch. search found a valid substring inside an input that did not "
                    "satisfy the complete format.",
                    "Brug bool(re.fullmatch(r'SMP-\\d{3}', text)) eller et kompileret mønster med "
                    "fullmatch. search fandt en gyldig delstreng i et input, som ikke opfyldte hele "
                    "formatet.",
                ),
                (
                    "La corrección debe cambiar el alcance de la coincidencia y distinguir forma "
                    "léxica de validez semántica.",
                    "The correction must change match scope and distinguish lexical form from "
                    "semantic validity.",
                    "Rettelsen skal ændre matchomfanget og skelne leksikalsk form fra semantisk "
                    "gyldighed.",
                ),
                "import re\n\ndef is_code(text: str) -> bool:\n"
                '    return bool(re.search(r"SMP-\\d{3}", text))',
            ),
        ),
        assessment_items=module.assessment_items
        + (
            objective_mcq(
                "dm857.m05.book.001",
                (
                    "¿Qué afirmación distingue correctamente search y fullmatch?",
                    "Which statement correctly distinguishes search and fullmatch?",
                    "Hvilket udsagn skelner korrekt mellem search og fullmatch?",
                ),
                (
                    (
                        "same_scope",
                        (
                            "Ambas funciones exigen que toda la cadena coincida.",
                            "Both functions require the entire string to match.",
                            "Begge funktioner kræver, at hele strengen matcher.",
                        ),
                    ),
                    (
                        "partial_vs_complete",
                        (
                            "search puede encontrar una subcadena; fullmatch exige toda la entrada.",
                            "search can find a substring; fullmatch requires the entire input.",
                            "search kan finde en delstreng; fullmatch kræver hele inputtet.",
                        ),
                    ),
                    (
                        "semantic_guarantee",
                        (
                            "fullmatch demuestra que el identificador existe en una base real.",
                            "fullmatch proves that the identifier exists in a real database.",
                            "fullmatch beviser, at identifikatoren findes i en virkelig database.",
                        ),
                    ),
                ),
                "partial_vs_complete",
                (
                    "El alcance de la coincidencia forma parte del contrato. Ninguna de las dos "
                    "funciones establece por sí sola validez semántica.",
                    "Match scope is part of the contract. Neither function establishes semantic "
                    "validity by itself.",
                    "Matchomfanget er en del af kontrakten. Ingen af funktionerne fastslår alene "
                    "semantisk gyldighed.",
                ),
            ),
        ),
    )
    return _with_source_basis(
        extended,
        ("guttag-2021-ch05", "downey-2024-strings-collections"),
    )


def _extend_mappings(module: LocalizedLearningModule) -> LocalizedLearningModule:
    """Add hash-table mechanism and cost boundaries to M07."""
    extended = replace(
        module,
        objectives=module.objectives
        + (
            objective(
                "m07.bg.o1",
                (
                    "Explicar cómo hashing, colisiones e igualdad sostienen el acceso a "
                    "diccionarios y conjuntos.",
                    "Explain how hashing, collisions, and equality support dictionary and set "
                    "access.",
                    "Forklare hvordan hashing, kollisioner og lighed understøtter adgang til "
                    "ordbøger og mængder.",
                ),
            ),
        ),
        concepts=module.concepts
        + (
            concept(
                "hash-tables-collisions-and-cost",
                (
                    "Tablas hash, colisiones y coste",
                    "Hash tables, collisions, and cost",
                    "Hash-tabeller, kollisioner og omkostning",
                ),
                (
                    "Los diccionarios y conjuntos usan una función hash para dirigir una clave "
                    "hashable hacia una región de una tabla. Dos claves diferentes pueden llegar "
                    "a la misma región; eso es una colisión y no significa que sean iguales. La "
                    "estructura resuelve la colisión comparando claves candidatas mediante "
                    "igualdad. Por contrato, dos objetos iguales deben producir hashes "
                    "compatibles, y una clave no debe cambiar de manera que altere su hash mientras "
                    "está almacenada. Con una distribución y carga normales, búsqueda, inserción y "
                    "pertenencia tienen coste promedio cercano a constante; el peor caso puede "
                    "degradarse y no debe presentarse como una garantía universal de O(1).",
                    "Dictionaries and sets use a hash function to direct a hashable key toward a "
                    "region of a table. Different keys can reach the same region; this is a "
                    "collision and does not mean the keys are equal. The structure resolves the "
                    "collision by comparing candidate keys for equality. By contract, equal "
                    "objects must produce compatible hashes, and a stored key must not change in "
                    "a way that alters its hash. Under normal distribution and load, lookup, "
                    "insertion, and membership have near-constant average cost; the worst case can "
                    "degrade and must not be presented as a universal O(1) guarantee.",
                    "Ordbøger og mængder bruger en hashfunktion til at lede en hashbar nøgle mod "
                    "et område i en tabel. Forskellige nøgler kan nå samme område; det er en "
                    "kollision og betyder ikke, at nøglerne er ens. Strukturen løser kollisionen "
                    "ved at sammenligne kandidatnøgler med lighed. Ifølge kontrakten skal ens "
                    "objekter give kompatible hashes, og en lagret nøgle må ikke ændres, så dens "
                    "hash ændres. Ved normal fordeling og belastning har opslag, indsættelse og "
                    "medlemskab næsten konstant gennemsnitsomkostning; værste fald kan forringes og "
                    "er ikke en universel O(1)-garanti.",
                ),
                (
                    (
                        "El hash selecciona candidatos; la igualdad confirma la clave.",
                        "The hash selects candidates; equality confirms the key.",
                        "Hashen vælger kandidater; lighed bekræfter nøglen.",
                    ),
                    (
                        "Una colisión entre claves diferentes es válida y debe resolverse.",
                        "A collision between different keys is valid and must be resolved.",
                        "En kollision mellem forskellige nøgler er gyldig og skal løses.",
                    ),
                    (
                        "Las claves almacenadas necesitan hash y semántica de igualdad estables.",
                        "Stored keys need stable hash and equality semantics.",
                        "Lagrede nøgler kræver stabil hash- og lighedssemantik.",
                    ),
                    (
                        "O(1) describe el caso promedio esperado, no todos los casos posibles.",
                        "O(1) describes expected average behavior, not every possible case.",
                        "O(1) beskriver forventet gennemsnitsadfærd, ikke alle mulige tilfælde.",
                    ),
                ),
            ),
        ),
        worked_examples=module.worked_examples
        + (
            example(
                "m07.bg.e01",
                (
                    "Modelar colisiones en cubetas",
                    "Model bucket collisions",
                    "Modellér kollisioner i buckets",
                ),
                (
                    "Usa una tabla didáctica de cinco cubetas para mostrar que claves diferentes "
                    "pueden compartir una posición inicial.",
                    "Use a teaching table with five buckets to show that different keys can share "
                    "an initial position.",
                    "Brug en undervisningstabel med fem buckets til at vise, at forskellige "
                    "nøgler kan dele en startposition.",
                ),
                (
                    (
                        "Calcula una cubeta didáctica mediante key % bucket_count.",
                        "Compute a teaching bucket with key % bucket_count.",
                        "Beregn en undervisningsbucket med key % bucket_count.",
                    ),
                    (
                        "Conserva todas las claves que colisionan en la misma cubeta.",
                        "Retain all keys that collide in the same bucket.",
                        "Bevar alle nøgler, der kolliderer i samme bucket.",
                    ),
                ),
                "bucket_count = 5\nkeys = (11, 16, 21)\nbuckets = {}\n"
                "for key in keys:\n    bucket = key % bucket_count\n"
                "    buckets.setdefault(bucket, []).append(key)\nprint(buckets)",
                "{1: [11, 16, 21]}",
                (
                    "Las tres claves producen la misma cubeta en este modelo, pero siguen siendo "
                    "claves distintas. Una implementación real de dict gestiona las colisiones "
                    "internamente; el módulo no afirma que Python use exactamente esta tabla.",
                    "All three keys produce the same bucket in this model but remain distinct "
                    "keys. A real dict implementation manages collisions internally; the module "
                    "does not claim that Python uses exactly this table.",
                    "Alle tre nøgler giver samme bucket i modellen, men er stadig forskellige "
                    "nøgler. En virkelig dict-implementering håndterer kollisioner internt; modulet "
                    "påstår ikke, at Python bruger præcis denne tabel.",
                ),
            ),
        ),
        practice_exercises=module.practice_exercises
        + (
            practice(
                "m07.bg.p01",
                ActivityType.DATA_INTERPRETATION,
                (
                    "En tabla didáctica con diez cubetas, las claves 7, 17 y 27 producen la misma "
                    "cubeta con key % 10. Explica por qué esto no las convierte en la misma clave, "
                    "cómo se distingue la clave correcta y qué significa afirmar que el acceso a "
                    "dict es O(1) en promedio.",
                    "In a teaching table with ten buckets, keys 7, 17, and 27 produce the same "
                    "bucket with key % 10. Explain why this does not make them the same key, how "
                    "the correct key is distinguished, and what it means to say dict access is "
                    "O(1) on average.",
                    "I en undervisningstabel med ti buckets giver nøglerne 7, 17 og 27 samme "
                    "bucket med key % 10. Forklar hvorfor det ikke gør dem til samme nøgle, hvordan "
                    "den korrekte nøgle skelnes, og hvad det betyder, at dict-adgang er O(1) i "
                    "gennemsnit.",
                ),
                (
                    (
                        "Una posición inicial no reemplaza la comparación de igualdad.",
                        "An initial position does not replace equality comparison.",
                        "En startposition erstatter ikke lighedssammenligning.",
                    ),
                    (
                        "Distingue comportamiento promedio de garantía de peor caso.",
                        "Distinguish average behavior from a worst-case guarantee.",
                        "Skeln mellem gennemsnitsadfærd og en garanti for værste fald.",
                    ),
                ),
                (
                    "Las claves son diferentes aunque colisionen. La tabla conserva candidatos y "
                    "usa igualdad para identificar la clave buscada. O(1) describe el coste "
                    "promedio esperado con una distribución y carga normales; no excluye casos "
                    "degradados.",
                    "The keys remain different despite colliding. The table retains candidates "
                    "and uses equality to identify the requested key. O(1) describes expected "
                    "average cost under normal distribution and load; it does not exclude "
                    "degraded cases.",
                    "Nøglerne er forskellige trods kollisionen. Tabellen bevarer kandidater og "
                    "bruger lighed til at identificere den ønskede nøgle. O(1) beskriver forventet "
                    "gennemsnitsomkostning ved normal fordeling og belastning; det udelukker ikke "
                    "forringede tilfælde.",
                ),
                (
                    "Una respuesta completa debe explicar colisión, igualdad y límite del modelo "
                    "de complejidad.",
                    "A complete answer must explain collision, equality, and the boundary of the "
                    "complexity model.",
                    "Et fuldstændigt svar skal forklare kollision, lighed og grænsen for "
                    "kompleksitetsmodellen.",
                ),
                "bucket_count = 10\nkeys = (7, 17, 27)\n"
                "print([key % bucket_count for key in keys])",
            ),
        ),
        assessment_items=module.assessment_items
        + (
            objective_mcq(
                "dm857.m07.book.001",
                (
                    "¿Qué afirmación describe correctamente una tabla hash?",
                    "Which statement correctly describes a hash table?",
                    "Hvilket udsagn beskriver en hash-tabel korrekt?",
                ),
                (
                    (
                        "collision_means_equal",
                        (
                            "Dos claves que colisionan deben ser iguales.",
                            "Two colliding keys must be equal.",
                            "To kolliderende nøgler skal være ens.",
                        ),
                    ),
                    (
                        "hash_then_equality",
                        (
                            "El hash dirige la búsqueda y la igualdad distingue claves candidatas.",
                            "The hash directs lookup and equality distinguishes candidate keys.",
                            "Hashen styrer opslaget, og lighed skelner kandidatnøgler.",
                        ),
                    ),
                    (
                        "constant_worst_case",
                        (
                            "Toda operación de dict está garantizada como O(1) en el peor caso.",
                            "Every dict operation is guaranteed O(1) in the worst case.",
                            "Alle dict-operationer er garanteret O(1) i værste fald.",
                        ),
                    ),
                ),
                "hash_then_equality",
                (
                    "Las colisiones son posibles; el hash reduce candidatos y la igualdad "
                    "confirma la clave. La complejidad constante es una expectativa promedio.",
                    "Collisions are possible; the hash narrows candidates and equality confirms "
                    "the key. Constant complexity is an average-case expectation.",
                    "Kollisioner er mulige; hashen indsnævrer kandidater, og lighed bekræfter "
                    "nøglen. Konstant kompleksitet er en forventning i gennemsnit.",
                ),
            ),
        ),
    )
    return _with_source_basis(
        extended,
        (
            "guttag-2021-ch05",
            "guttag-2021-ch10-12",
            "downey-2024-strings-collections",
        ),
    )


def apply_strings_mappings_book_extensions(
    modules: tuple[LocalizedLearningModule, ...],
) -> tuple[LocalizedLearningModule, ...]:
    """Apply M05 and M07 extensions without changing module order."""
    extended: list[LocalizedLearningModule] = []
    for module in modules:
        if module.module_id == "dm857.m05":
            extended.append(_extend_strings(module))
        elif module.module_id == "dm857.m07":
            extended.append(_extend_mappings(module))
        else:
            extended.append(module)
    return tuple(extended)


__all__ = [
    "apply_strings_mappings_book_extensions",
    "update_strings_mappings_audit",
]
