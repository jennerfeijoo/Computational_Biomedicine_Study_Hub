"""Reference mapping and targeted book-grounded extensions for DM857.

The reference catalog records where each authored module should be checked.  A
module is marked ``consistent`` only after a focused comparison with the named
source scope.  The extensions in this file are original teaching material; they
paraphrase and synthesize concepts without reproducing textbook prose or
proprietary exercises.
"""

from __future__ import annotations

from dataclasses import dataclass, replace
from typing import Literal

from ...learning.activity_types import ActivityType
from ..localized_models import LocalizedLearningModule, LocalizedTutorSupportPacket
from .authoring import concept, example, objective, objective_mcq, practice

VerificationState = Literal["pending", "consistent", "improve", "correct", "outside_scope"]


@dataclass(frozen=True, slots=True)
class BookReference:
    """One stable bibliographic source used by the internal content audit."""

    source_id: str
    citation: str
    relevant_scope: str


@dataclass(frozen=True, slots=True)
class ModuleSourceAudit:
    """Source mapping and current verification state for one DM857 module."""

    module_id: str
    source_ids: tuple[str, ...]
    source_scope: tuple[str, ...]
    state: VerificationState
    finding: str
    implemented_change: str = ""


DM857_BOOK_SOURCES: tuple[BookReference, ...] = (
    BookReference(
        source_id="guttag-2021-ch01-03",
        citation=(
            "John V. Guttag, Introduction to Computation and Programming Using Python, "
            "3rd ed. (2021), chapters 1-3."
        ),
        relevant_scope=(
            "computational problem solving, Python expressions, control flow, and simple "
            "numerical programs"
        ),
    ),
    BookReference(
        source_id="guttag-2021-ch04",
        citation=(
            "John V. Guttag, Introduction to Computation and Programming Using Python, "
            "3rd ed. (2021), chapter 4."
        ),
        relevant_scope="functions, specifications, scope, stack frames, and abstraction",
    ),
    BookReference(
        source_id="guttag-2021-ch05",
        citation=(
            "John V. Guttag, Introduction to Computation and Programming Using Python, "
            "3rd ed. (2021), chapter 5."
        ),
        relevant_scope="structured types, mutability, identity, aliasing, cloning, and mappings",
    ),
    BookReference(
        source_id="guttag-2021-ch06",
        citation=(
            "John V. Guttag, Introduction to Computation and Programming Using Python, "
            "3rd ed. (2021), chapter 6."
        ),
        relevant_scope="recursion, recursive calls, stack behavior, and global state",
    ),
    BookReference(
        source_id="guttag-2021-ch07-09",
        citation=(
            "John V. Guttag, Introduction to Computation and Programming Using Python, "
            "3rd ed. (2021), chapters 7-9."
        ),
        relevant_scope="modules, files, testing, debugging, exceptions, and assertions",
    ),
    BookReference(
        source_id="guttag-2021-ch10-12",
        citation=(
            "John V. Guttag, Introduction to Computation and Programming Using Python, "
            "3rd ed. (2021), chapters 10-12."
        ),
        relevant_scope=(
            "classes, object-oriented programming, algorithmic complexity, algorithms, "
            "and data structures"
        ),
    ),
    BookReference(
        source_id="guttag-2021-ch13-15-23",
        citation=(
            "John V. Guttag, Introduction to Computation and Programming Using Python, "
            "3rd ed. (2021), chapters 13-15 and 23."
        ),
        relevant_scope=(
            "plotting, graph foundations, dynamic programming, and data exploration with "
            "scientific libraries"
        ),
    ),
    BookReference(
        source_id="downey-2024-foundations",
        citation="Allen B. Downey, Think Python, 3rd ed. (2024), foundational sequence.",
        relevant_scope=(
            "incremental programming, precise vocabulary, expressions, conditionals, loops, "
            "functions, and recursion"
        ),
    ),
    BookReference(
        source_id="downey-2024-strings-collections",
        citation="Allen B. Downey, Think Python, 3rd ed. (2024), strings and core data structures.",
        relevant_scope="strings, lists, dictionaries, tuples, mutation, and collection algorithms",
    ),
    BookReference(
        source_id="downey-2024-files-oop",
        citation="Allen B. Downey, Think Python, 3rd ed. (2024), files, databases, and OOP sequence.",
        relevant_scope="persistent storage, files, classes, objects, interfaces, and inheritance",
    ),
    BookReference(
        source_id="downey-2024-testing",
        citation="Allen B. Downey, Think Python, 3rd ed. (2024), testing and debugging material.",
        relevant_scope=(
            "input validation, doctest, unittest, automated testing, debugging strategy, and "
            "correct-program development"
        ),
    ),
)


DM857_MODULE_SOURCE_AUDIT: tuple[ModuleSourceAudit, ...] = (
    ModuleSourceAudit(
        "dm857.m01",
        ("guttag-2021-ch01-03", "downey-2024-foundations"),
        ("problem formulation", "expressions and bindings", "hand tracing"),
        "pending",
        "Source scope mapped; line-by-line module review remains pending.",
    ),
    ModuleSourceAudit(
        "dm857.m02",
        ("guttag-2021-ch01-03", "downey-2024-foundations"),
        ("Boolean expressions", "branching", "boundary conditions"),
        "pending",
        "Source scope mapped; line-by-line module review remains pending.",
    ),
    ModuleSourceAudit(
        "dm857.m03",
        ("guttag-2021-ch01-03", "downey-2024-foundations"),
        ("iteration", "loop invariants", "termination and tracing"),
        "pending",
        "Source scope mapped; line-by-line module review remains pending.",
    ),
    ModuleSourceAudit(
        "dm857.m04",
        ("guttag-2021-ch04", "downey-2024-foundations", "downey-2024-testing"),
        ("function specifications", "scope and frames", "defaults", "unit tests"),
        "consistent",
        (
            "Existing coverage of interfaces, contracts, scope, return values, purity, and unit "
            "testing is consistent. Mutable default state needed one explicit diagnostic."
        ),
        "Added an original mutable-default explanation, safe example, debugging task, and question.",
    ),
    ModuleSourceAudit(
        "dm857.m05",
        ("guttag-2021-ch05", "downey-2024-strings-collections"),
        ("string immutability", "slicing", "search and transformation"),
        "pending",
        "Source scope mapped; line-by-line module review remains pending.",
    ),
    ModuleSourceAudit(
        "dm857.m06",
        ("guttag-2021-ch05", "downey-2024-strings-collections"),
        ("lists and tuples", "mutation versus rebinding", "aliasing and shallow copies"),
        "consistent",
        (
            "The module already distinguishes identity, aliasing, reassignment, shallow copying, "
            "nested-row aliasing, and mutation during traversal."
        ),
    ),
    ModuleSourceAudit(
        "dm857.m07",
        ("guttag-2021-ch05", "guttag-2021-ch10-12", "downey-2024-strings-collections"),
        ("dictionaries", "sets", "hash-based lookup", "collection contracts"),
        "pending",
        "Source scope mapped; line-by-line module review remains pending.",
    ),
    ModuleSourceAudit(
        "dm857.m08",
        ("guttag-2021-ch07-09", "downey-2024-files-oop", "downey-2024-testing"),
        ("files and resource lifetime", "exceptions", "input validation", "assertions"),
        "consistent",
        (
            "File boundaries, context managers, specific exceptions, propagation, and failure "
            "testing are consistent. The role of assert versus public input validation needed "
            "one explicit distinction."
        ),
        "Added an original exceptions-versus-assertions explanation, example, practice, and question.",
    ),
    ModuleSourceAudit(
        "dm857.m09",
        ("guttag-2021-ch06", "downey-2024-foundations"),
        ("base cases", "well-founded progress", "call frames", "unwinding", "cost"),
        "consistent",
        (
            "The module already covers reachable base cases, a decreasing progress measure, "
            "independent frames, LIFO unwinding, recursive cost, and memoization boundaries."
        ),
    ),
    ModuleSourceAudit(
        "dm857.m10",
        ("guttag-2021-ch10-12", "guttag-2021-ch13-15-23"),
        ("tree representation", "recursive traversal", "search", "complexity"),
        "pending",
        "Source scope mapped; line-by-line module review remains pending.",
    ),
    ModuleSourceAudit(
        "dm857.m11",
        ("guttag-2021-ch10-12", "downey-2024-files-oop"),
        ("abstract data types", "representation invariants", "interface and implementation"),
        "pending",
        "Source scope mapped; line-by-line module review remains pending.",
    ),
    ModuleSourceAudit(
        "dm857.m12",
        ("guttag-2021-ch10-12", "downey-2024-files-oop"),
        ("classes and instances", "encapsulation", "inheritance", "method contracts"),
        "pending",
        "Source scope mapped; line-by-line module review remains pending.",
    ),
    ModuleSourceAudit(
        "dm857.m13",
        ("guttag-2021-ch13-15-23",),
        ("scientific arrays", "plotting", "tabular data", "library interfaces"),
        "pending",
        "Source scope mapped; line-by-line module review remains pending.",
    ),
    ModuleSourceAudit(
        "dm857.m14",
        ("guttag-2021-ch07-09", "downey-2024-testing"),
        ("black-box tests", "boundaries", "regression tests", "debugging workflow"),
        "consistent",
        (
            "The module already treats tests as executable contracts, covers boundaries and "
            "expected failures, isolates fixtures, and ends debugging with a regression test."
        ),
    ),
)


def _with_source_basis(
    module: LocalizedLearningModule, source_ids: tuple[str, ...]
) -> LocalizedLearningModule:
    tutor = module.tutor_support
    merged = tuple(dict.fromkeys((*tutor.source_basis, *source_ids)))
    updated_tutor: LocalizedTutorSupportPacket = replace(tutor, source_basis=merged)
    return replace(module, tutor_support=updated_tutor)


def _extend_functions(module: LocalizedLearningModule) -> LocalizedLearningModule:
    """Add the mutable-default distinction missing from the original M04."""

    extended = replace(
        module,
        objectives=module.objectives
        + (
            objective(
                "m04.bg.o1",
                (
                    "Predecir y evitar estado compartido creado por parámetros predeterminados mutables.",
                    "Predict and prevent shared state created by mutable default parameters.",
                    "Forudsige og undgå delt tilstand skabt af muterbare standardparametre.",
                ),
            ),
        ),
        concepts=module.concepts
        + (
            concept(
                "mutable-default-arguments",
                (
                    "Parámetros predeterminados mutables",
                    "Mutable default parameters",
                    "Muterbare standardparametre",
                ),
                (
                    "Las expresiones predeterminadas se evalúan cuando Python ejecuta la definición de la función, no en cada llamada. Si el valor es una lista, diccionario o conjunto y la función lo modifica, las llamadas que omiten ese argumento reutilizan el mismo objeto. Esto crea estado compartido oculto. Para una colección nueva por llamada, usa un valor centinela inmutable como None y construye la colección dentro de la función. Un default mutable sólo es apropiado cuando el estado compartido es intencional, explícito y documentado.",
                    "Default expressions are evaluated when Python executes the function definition, not on every call. If the value is a list, dictionary, or set and the function mutates it, calls that omit the argument reuse the same object. This creates hidden shared state. For a fresh collection per call, use an immutable sentinel such as None and construct the collection inside the function. A mutable default is appropriate only when shared state is intentional, explicit, and documented.",
                    "Standardudtryk evalueres når Python udfører funktionsdefinitionen, ikke ved hvert kald. Hvis værdien er en liste, dictionary eller set, og funktionen muterer den, genbruger kald uden argumentet det samme objekt. Det skaber skjult delt tilstand. Brug en uforanderlig sentinel som None og opret samlingen inde i funktionen, når hvert kald skal have en ny samling. En muterbar standardværdi er kun passende, når delt tilstand er tilsigtet, eksplicit og dokumenteret.",
                ),
                (
                    (
                        "La evaluación ocurre una vez al definir la función.",
                        "Evaluation happens once when the function is defined.",
                        "Evalueringen sker én gang, når funktionen defineres.",
                    ),
                    (
                        "Mutar el default hace visible estado de llamadas anteriores.",
                        "Mutating the default exposes state from earlier calls.",
                        "Mutation af standardværdien gør tidligere kalds tilstand synlig.",
                    ),
                    (
                        "None permite crear una colección independiente por llamada.",
                        "None allows a separate collection to be created per call.",
                        "None gør det muligt at oprette en separat samling pr. kald.",
                    ),
                ),
            ),
        ),
        worked_examples=module.worked_examples
        + (
            example(
                "m04.bg.e01",
                (
                    "Una lista nueva en cada llamada",
                    "A fresh list on every call",
                    "En ny liste ved hvert kald",
                ),
                (
                    "Diseña una función que añada una etiqueta sin compartir accidentalmente la lista entre llamadas.",
                    "Design a function that adds a label without accidentally sharing the list across calls.",
                    "Design en funktion der tilføjer en etiket uden utilsigtet at dele listen mellem kald.",
                ),
                (
                    (
                        "None es un centinela inmutable que indica que la llamada no entregó una colección.",
                        "None is an immutable sentinel indicating that the caller supplied no collection.",
                        "None er en uforanderlig sentinel, der viser at kaldet ikke leverede en samling.",
                    ),
                    (
                        "La lista se crea dentro del cuerpo y pertenece sólo a esa llamada.",
                        "The list is created inside the body and belongs only to that call.",
                        "Listen oprettes inde i kroppen og tilhører kun det kald.",
                    ),
                ),
                "def add_label(label: str, labels: list[str] | None = None) -> list[str]:\n    if labels is None:\n        labels = []\n    labels.append(label)\n    return labels\n\nprint(add_label(\"rna\"))\nprint(add_label(\"protein\"))",
                "['rna']\n['protein']",
                (
                    "Cada llamada que omite labels crea su propia lista; una colección entregada explícitamente todavía puede modificarse según el contrato.",
                    "Each call that omits labels creates its own list; an explicitly supplied collection may still be mutated according to the contract.",
                    "Hvert kald der udelader labels opretter sin egen liste; en eksplicit leveret samling kan stadig muteres i henhold til kontrakten.",
                ),
            ),
        ),
        practice_exercises=module.practice_exercises
        + (
            practice(
                "m04.bg.p01",
                ActivityType.DEBUGGING,
                (
                    "La función collect(value, values=[]) devuelve [1] en la primera llamada y [1, 2] en la segunda. Reconstruye la causa y corrígela para que la segunda llamada devuelva [2].",
                    "The function collect(value, values=[]) returns [1] on the first call and [1, 2] on the second. Reconstruct the cause and fix it so the second call returns [2].",
                    "Funktionen collect(value, values=[]) returnerer [1] ved første kald og [1, 2] ved det andet. Rekonstruér årsagen og ret den, så andet kald returnerer [2].",
                ),
                (
                    (
                        "Pregunta cuándo se crea la lista predeterminada.",
                        "Ask when the default list is created.",
                        "Spørg hvornår standardlisten oprettes.",
                    ),
                    (
                        "Sustituye el default por None y crea la lista dentro.",
                        "Replace the default with None and create the list inside.",
                        "Erstat standardværdien med None og opret listen inde i funktionen.",
                    ),
                ),
                (
                    "El objeto lista fue creado una vez al definir la función y se reutilizó. Usa def collect(value, values=None): seguido de if values is None: values = [].",
                    "The list object was created once when the function was defined and reused. Use def collect(value, values=None): followed by if values is None: values = [].",
                    "Listeobjektet blev oprettet én gang ved funktionsdefinitionen og genbrugt. Brug def collect(value, values=None): efterfulgt af if values is None: values = [].",
                ),
                (
                    "La corrección cambia el momento de creación de la colección y elimina el estado compartido implícito.",
                    "The fix changes when the collection is created and removes implicit shared state.",
                    "Rettelsen ændrer tidspunktet for oprettelse af samlingen og fjerner implicit delt tilstand.",
                ),
                "def collect(value, values=[]):\n    values.append(value)\n    return values",
            ),
        ),
        assessment_items=module.assessment_items
        + (
            objective_mcq(
                "dm857.m04.book.001",
                (
                    "¿Qué diseño produce una lista independiente cuando el argumento se omite?",
                    "Which design produces an independent list when the argument is omitted?",
                    "Hvilket design producerer en uafhængig liste, når argumentet udelades?",
                ),
                (
                    (
                        "mutable_default",
                        (
                            "def f(items=[]): items.append(1); return items",
                            "def f(items=[]): items.append(1); return items",
                            "def f(items=[]): items.append(1); return items",
                        ),
                    ),
                    (
                        "none_sentinel",
                        (
                            "def f(items=None): items = [] if items is None else items; items.append(1); return items",
                            "def f(items=None): items = [] if items is None else items; items.append(1); return items",
                            "def f(items=None): items = [] if items is None else items; items.append(1); return items",
                        ),
                    ),
                    (
                        "global_list",
                        (
                            "Usar siempre una lista global",
                            "Always use a global list",
                            "Brug altid en global liste",
                        ),
                    ),
                ),
                "none_sentinel",
                (
                    "El centinela None permite crear la lista dentro de cada llamada que no recibe una colección explícita.",
                    "The None sentinel allows the list to be created inside every call that receives no explicit collection.",
                    "None-sentinellen gør det muligt at oprette listen inde i hvert kald uden en eksplicit samling.",
                ),
            ),
        ),
    )
    return _with_source_basis(
        extended,
        ("guttag-2021-ch04", "guttag-2021-ch05", "downey-2024-foundations"),
    )


def _extend_files_and_exceptions(module: LocalizedLearningModule) -> LocalizedLearningModule:
    """Clarify public validation errors versus internal assertions in M08."""

    extended = replace(
        module,
        objectives=module.objectives
        + (
            objective(
                "m08.bg.o1",
                (
                    "Elegir entre una excepción de contrato y una assertion de invariante interno.",
                    "Choose between a contract exception and an internal-invariant assertion.",
                    "Vælge mellem en kontrakt-exception og en assertion for en intern invariant.",
                ),
            ),
        ),
        concepts=module.concepts
        + (
            concept(
                "exceptions-versus-assertions",
                (
                    "Excepciones de contrato y assertions internas",
                    "Contract exceptions and internal assertions",
                    "Kontrakt-exceptions og interne assertions",
                ),
                (
                    "Una entrada externa inválida es una posibilidad prevista por la interfaz y debe producir una excepción explícita, por ejemplo ValueError o TypeError, con contexto útil. assert expresa una invariante interna que el programador considera verdadera si el código es correcto. Un AssertionError suele señalar un defecto de programación, no un error que el usuario deba corregir. Como las assertions pueden omitirse al ejecutar Python con optimización, no deben proteger validación pública, permisos, límites de seguridad ni integridad de datos externos.",
                    "Invalid external input is an anticipated interface condition and should produce an explicit exception such as ValueError or TypeError with useful context. assert expresses an internal invariant that the programmer expects to hold when the code is correct. An AssertionError usually signals a programming defect, not an error the caller should fix. Because assertions may be omitted when Python runs with optimization, they must not enforce public validation, permissions, safety limits, or external-data integrity.",
                    "Ugyldigt eksternt input er en forventet grænsetilstand i grænsefladen og bør give en eksplicit exception som ValueError eller TypeError med nyttig kontekst. assert udtrykker en intern invariant, som programmøren forventer er sand, når koden er korrekt. En AssertionError peger normalt på en programmeringsfejl, ikke en fejl som brugeren skal rette. Assertions kan udelades ved optimeret Python-kørsel og må derfor ikke håndhæve offentlig validering, rettigheder, sikkerhedsgrænser eller eksterne datas integritet.",
                ),
                (
                    (
                        "Entrada inválida prevista → excepción explícita.",
                        "Anticipated invalid input → explicit exception.",
                        "Forventet ugyldigt input → eksplicit exception.",
                    ),
                    (
                        "Estado interno imposible → assert para detectar un defecto.",
                        "Impossible internal state → assert to detect a defect.",
                        "Umulig intern tilstand → assert for at opdage en fejl.",
                    ),
                    (
                        "La corrección del programa no debe depender de que assert esté activo.",
                        "Program correctness must not depend on assert being active.",
                        "Programmets korrekthed må ikke afhænge af at assert er aktiv.",
                    ),
                ),
            ),
        ),
        worked_examples=module.worked_examples
        + (
            example(
                "m08.bg.e01",
                (
                    "Validar la frontera y comprobar la invariante",
                    "Validate the boundary and check the invariant",
                    "Validér grænsen og kontrollér invarianten",
                ),
                (
                    "Convierte un porcentaje textual en una fracción y distingue una entrada inválida de un estado interno imposible.",
                    "Convert a textual percentage into a fraction and distinguish invalid input from an impossible internal state.",
                    "Konvertér en tekstlig procent til en brøk og skeln ugyldigt input fra en umulig intern tilstand.",
                ),
                (
                    (
                        "float puede fallar con ValueError y el rango forma parte del contrato público.",
                        "float may fail with ValueError, and the range belongs to the public contract.",
                        "float kan fejle med ValueError, og intervallet tilhører den offentlige kontrakt.",
                    ),
                    (
                        "Después de validar, la fracción debería cumplir una invariante interna.",
                        "After validation, the fraction should satisfy an internal invariant.",
                        "Efter validering bør brøken opfylde en intern invariant.",
                    ),
                ),
                "def parse_percentage(text: str) -> float:\n    value = float(text)\n    if not 0.0 <= value <= 100.0:\n        raise ValueError(\"percentage must be between 0 and 100\")\n    fraction = value / 100.0\n    assert 0.0 <= fraction <= 1.0\n    return fraction\n\nprint(parse_percentage(\"12.5\"))",
                "0.125",
                (
                    "ValueError comunica una condición inválida prevista al llamador; assert documenta y comprueba una consecuencia interna de la validación.",
                    "ValueError communicates an anticipated invalid condition to the caller; assert documents and checks an internal consequence of validation.",
                    "ValueError kommunikerer en forventet ugyldig tilstand til kalderen; assert dokumenterer og kontrollerer en intern konsekvens af valideringen.",
                ),
            ),
        ),
        practice_exercises=module.practice_exercises
        + (
            practice(
                "m08.bg.p01",
                ActivityType.DATA_INTERPRETATION,
                (
                    "Clasifica cada comprobación: edad textual no convertible; edad fuera de 0-130; contador interno negativo después de una función que promete incrementos no negativos.",
                    "Classify each check: non-convertible textual age; age outside 0-130; negative internal counter after a function that promises non-negative increments.",
                    "Klassificér hver kontrol: tekstalder der ikke kan konverteres; alder uden for 0-130; negativ intern tæller efter en funktion der lover ikke-negative stigninger.",
                ),
                (
                    (
                        "Las dos primeras condiciones pertenecen a la frontera de entrada.",
                        "The first two conditions belong to the input boundary.",
                        "De to første tilstande tilhører inputgrænsen.",
                    ),
                    (
                        "La tercera contradice una invariante interna.",
                        "The third contradicts an internal invariant.",
                        "Den tredje modsiger en intern invariant.",
                    ),
                ),
                (
                    "Conversión inválida: ValueError original o traducido con contexto; rango inválido: ValueError explícito; contador interno negativo: assert o error interno equivalente durante desarrollo y pruebas.",
                    "Invalid conversion: the original ValueError or one translated with context; invalid range: explicit ValueError; negative internal counter: assert or an equivalent internal error during development and tests.",
                    "Ugyldig konvertering: den oprindelige ValueError eller en oversat med kontekst; ugyldigt interval: eksplicit ValueError; negativ intern tæller: assert eller tilsvarende intern fejl under udvikling og test.",
                ),
                (
                    "La decisión depende de quién puede causar la condición y quién debe corregirla.",
                    "The decision depends on who can cause the condition and who should fix it.",
                    "Beslutningen afhænger af hvem der kan forårsage tilstanden, og hvem der skal rette den.",
                ),
            ),
        ),
        assessment_items=module.assessment_items
        + (
            objective_mcq(
                "dm857.m08.book.001",
                (
                    "¿Qué comprobación debe usar una excepción explícita y no sólo assert?",
                    "Which check should use an explicit exception rather than only assert?",
                    "Hvilken kontrol bør bruge en eksplicit exception frem for kun assert?",
                ),
                (
                    (
                        "public_range",
                        (
                            "Rechazar una edad externa fuera del rango permitido",
                            "Reject an external age outside the allowed range",
                            "Afvis en ekstern alder uden for det tilladte interval",
                        ),
                    ),
                    (
                        "internal_sorted",
                        (
                            "Comprobar durante desarrollo que una función interna devolvió una lista ordenada",
                            "Check during development that an internal function returned a sorted list",
                            "Kontrollér under udvikling at en intern funktion returnerede en sorteret liste",
                        ),
                    ),
                    (
                        "unreachable_branch",
                        (
                            "Detectar una rama que el diseño considera inalcanzable",
                            "Detect a branch that the design considers unreachable",
                            "Opdag en gren som designet anser for utilgængelig",
                        ),
                    ),
                ),
                "public_range",
                (
                    "El rango de una entrada pública debe seguir validándose aunque Python se ejecute con assertions desactivadas.",
                    "A public-input range must remain validated even when Python runs with assertions disabled.",
                    "Intervallet for et offentligt input skal fortsat valideres, selv når Python kører med deaktiverede assertions.",
                ),
            ),
        ),
    )
    return _with_source_basis(
        extended,
        ("guttag-2021-ch07-09", "downey-2024-files-oop", "downey-2024-testing"),
    )


def apply_book_grounded_extensions(
    modules: tuple[LocalizedLearningModule, ...],
) -> tuple[LocalizedLearningModule, ...]:
    """Apply reviewed extensions without changing module order or stable IDs."""

    extended: list[LocalizedLearningModule] = []
    for module in modules:
        if module.module_id == "dm857.m04":
            extended.append(_extend_functions(module))
        elif module.module_id == "dm857.m08":
            extended.append(_extend_files_and_exceptions(module))
        elif module.module_id == "dm857.m06":
            extended.append(
                _with_source_basis(
                    module,
                    ("guttag-2021-ch05", "downey-2024-strings-collections"),
                )
            )
        elif module.module_id == "dm857.m09":
            extended.append(
                _with_source_basis(
                    module,
                    ("guttag-2021-ch06", "downey-2024-foundations"),
                )
            )
        elif module.module_id == "dm857.m14":
            extended.append(
                _with_source_basis(
                    module,
                    ("guttag-2021-ch07-09", "downey-2024-testing"),
                )
            )
        else:
            extended.append(module)
    return tuple(extended)


__all__ = [
    "BookReference",
    "DM857_BOOK_SOURCES",
    "DM857_MODULE_SOURCE_AUDIT",
    "ModuleSourceAudit",
    "VerificationState",
    "apply_book_grounded_extensions",
]
