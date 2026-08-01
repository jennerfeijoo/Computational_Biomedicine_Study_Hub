"""Book-grounded extension for DM857 ADT representation independence."""

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


def update_adts_audit(
    audit: tuple[ModuleSourceAudit, ...],
) -> tuple[ModuleSourceAudit, ...]:
    """Mark M11 reviewed only after representation-independence coverage exists."""
    updated: list[ModuleSourceAudit] = []
    for item in audit:
        if item.module_id == "dm857.m11":
            updated.append(
                replace(
                    item,
                    state="consistent",
                    finding=(
                        "Existing coverage of ADT interfaces, contracts, representation "
                        "invariants, encapsulation, stacks, queues, priority queues, maps, sets, "
                        "composition, complexity, and behavioral testing is consistent. Explicit "
                        "demonstration of representation independence through two interchangeable "
                        "implementations and one shared contract suite was still needed."
                    ),
                    implemented_change=(
                        "Added an original representation-independence explanation, two concrete "
                        "set implementations exercised by the same deterministic contract suite, "
                        "a client-coupling diagnosis, and a stable objective item."
                    ),
                )
            )
        else:
            updated.append(item)
    return tuple(updated)


def _extend_adts(module: LocalizedLearningModule) -> LocalizedLearningModule:
    """Add representation independence and shared contract testing to M11."""
    extended = replace(
        module,
        objectives=module.objectives
        + (
            objective(
                "m11.bg.o1",
                (
                    "Demostrar independencia de representación comparando dos implementaciones "
                    "mediante el mismo contrato observable.",
                    "Demonstrate representation independence by comparing two implementations "
                    "through the same observable contract.",
                    "Demonstrere repræsentationsuafhængighed ved at sammenligne to "
                    "implementeringer gennem samme observerbare kontrakt.",
                ),
            ),
        ),
        concepts=module.concepts
        + (
            concept(
                "representation-independence-and-contract-suites",
                (
                    "Independencia de representación y suites de contrato",
                    "Representation independence and contract suites",
                    "Repræsentationsuafhængighed og kontraktsuiter",
                ),
                (
                    "Una barrera de abstracción separa el valor abstracto que observa el cliente "
                    "de las estructuras concretas que lo codifican. Dos implementaciones pueden "
                    "usar estados internos distintos —por ejemplo, una lista sin duplicados o las "
                    "claves de un diccionario— y seguir representando el mismo ADT si producen los "
                    "mismos resultados, errores y efectos públicos. La invariante determina qué "
                    "estados internos son válidos; el contrato determina lo que el cliente puede "
                    "observar. Una misma suite de pruebas debe ejecutarse contra ambas "
                    "implementaciones. Si las pruebas inspeccionan atributos privados, orden "
                    "accidental o tipos internos, cruzan la barrera de abstracción y convierten un "
                    "cambio legítimo de representación en una falsa regresión.",
                    "An abstraction barrier separates the abstract value observed by clients from "
                    "the concrete structures that encode it. Two implementations may use different "
                    "internal states—for example, a duplicate-free list or dictionary keys—and "
                    "still represent the same ADT when they produce the same public results, "
                    "errors, and effects. The invariant determines which internal states are valid; "
                    "the contract determines what clients may observe. The same contract suite "
                    "should run against both implementations. Tests that inspect private "
                    "attributes, accidental order, or internal types cross the abstraction barrier "
                    "and turn a legitimate representation change into a false regression.",
                    "En abstraktionsbarriere adskiller den abstrakte værdi, som klienten ser, fra "
                    "de konkrete strukturer, der koder den. To implementeringer kan bruge forskellig "
                    "intern tilstand—f.eks. en liste uden dubletter eller nøglerne i en ordbog—og "
                    "stadig repræsentere samme ADT, når de giver samme offentlige resultater, fejl "
                    "og effekter. Invarianten afgør, hvilke interne tilstande der er gyldige; "
                    "kontrakten afgør, hvad klienten må observere. Den samme kontraktsuite bør køres "
                    "mod begge implementeringer. Test, der undersøger private attributter, tilfældig "
                    "rækkefølge eller interne typer, krydser abstraktionsbarrieren og gør en legitim "
                    "repræsentationsændring til en falsk regression.",
                ),
                (
                    (
                        "Equivalencia observable no significa igualdad de atributos internos.",
                        "Observable equivalence does not mean identical internal attributes.",
                        "Observerbar ækvivalens betyder ikke identiske interne attributter.",
                    ),
                    (
                        "La invariante valida la representación; el contrato gobierna al cliente.",
                        "The invariant validates representation; the contract governs clients.",
                        "Invarianten validerer repræsentationen; kontrakten styrer klienten.",
                    ),
                    (
                        "Una suite compartida debe probar operaciones, errores y secuencias.",
                        "A shared suite should test operations, errors, and sequences.",
                        "En delt suite bør teste operationer, fejl og sekvenser.",
                    ),
                    (
                        "Inspeccionar estado privado acopla la prueba a una implementación.",
                        "Inspecting private state couples a test to one implementation.",
                        "Inspektion af privat tilstand kobler testen til én implementering.",
                    ),
                ),
            ),
        ),
        worked_examples=module.worked_examples
        + (
            example(
                "m11.bg.e01",
                (
                    "Una suite de contrato para dos representaciones",
                    "One contract suite for two representations",
                    "Én kontraktsuite for to repræsentationer",
                ),
                (
                    "Ejecuta la misma secuencia pública sobre un conjunto respaldado por lista y "
                    "otro respaldado por diccionario, sin inspeccionar su estado interno.",
                    "Run the same public sequence on a list-backed set and a dictionary-backed set "
                    "without inspecting their internal state.",
                    "Kør den samme offentlige sekvens på en listebaseret mængde og en "
                    "ordbogsbaseret mængde uden at undersøge deres interne tilstand.",
                ),
                (
                    (
                        "Ambas clases ofrecen insert, remove, member y len.",
                        "Both classes provide insert, remove, member, and len.",
                        "Begge klasser tilbyder insert, remove, member og len.",
                    ),
                    (
                        "La lista evita duplicados explícitamente; el diccionario los evita por "
                        "unicidad de claves.",
                        "The list prevents duplicates explicitly; the dictionary prevents them "
                        "through key uniqueness.",
                        "Listen forhindrer dubletter eksplicit; ordbogen forhindrer dem gennem "
                        "unikke nøgler.",
                    ),
                    (
                        "La función contract_trace usa sólo operaciones públicas.",
                        "The contract_trace function uses only public operations.",
                        "Funktionen contract_trace bruger kun offentlige operationer.",
                    ),
                ),
                "class ListSet:\n"
                "    def __init__(self):\n"
                "        self._values = []\n\n"
                "    def insert(self, value):\n"
                "        if value not in self._values:\n"
                "            self._values.append(value)\n\n"
                "    def remove(self, value):\n"
                "        if value not in self._values:\n"
                "            raise KeyError(value)\n"
                "        self._values.remove(value)\n\n"
                "    def member(self, value):\n"
                "        return value in self._values\n\n"
                "    def __len__(self):\n"
                "        return len(self._values)\n\n"
                "class DictSet:\n"
                "    def __init__(self):\n"
                "        self._values = {}\n\n"
                "    def insert(self, value):\n"
                "        self._values[value] = None\n\n"
                "    def remove(self, value):\n"
                "        if value not in self._values:\n"
                "            raise KeyError(value)\n"
                "        del self._values[value]\n\n"
                "    def member(self, value):\n"
                "        return value in self._values\n\n"
                "    def __len__(self):\n"
                "        return len(self._values)\n\n"
                "def contract_trace(factory):\n"
                "    collection = factory()\n"
                "    collection.insert('A')\n"
                "    collection.insert('B')\n"
                "    collection.insert('A')\n"
                "    collection.remove('B')\n"
                "    return collection.member('A'), collection.member('B'), len(collection)\n\n"
                "print(contract_trace(ListSet))\n"
                "print(contract_trace(DictSet))",
                "(True, False, 1)\n(True, False, 1)",
                (
                    "Las representaciones y sus costes internos no son idénticos, pero la traza "
                    "observable coincide. La prueba permanecería válida si una implementación "
                    "cambia de estructura mientras conserva el contrato.",
                    "The representations and their internal costs are not identical, but the "
                    "observable trace matches. The test remains valid if an implementation changes "
                    "structure while preserving the contract.",
                    "Repræsentationerne og deres interne omkostninger er ikke identiske, men det "
                    "observerbare spor er det samme. Testen forbliver gyldig, hvis en "
                    "implementering ændrer struktur og bevarer kontrakten.",
                ),
            ),
        ),
        practice_exercises=module.practice_exercises
        + (
            practice(
                "m11.bg.p01",
                ActivityType.DEBUGGING,
                (
                    "Una prueba exige que collection._values sea una lista y compara directamente "
                    "su orden después de varias inserciones. Diagnostica el defecto y reformula la "
                    "prueba para que acepte cualquier implementación correcta del ADT conjunto.",
                    "A test requires collection._values to be a list and directly compares its "
                    "order after several insertions. Diagnose the defect and reformulate the test "
                    "so it accepts any correct implementation of the set ADT.",
                    "En test kræver, at collection._values er en liste, og sammenligner direkte "
                    "dens rækkefølge efter flere indsættelser. Diagnosticér fejlen og omformulér "
                    "testen, så den accepterer enhver korrekt implementering af mængde-ADT'et.",
                ),
                (
                    (
                        "El contrato del conjunto trata pertenencia y unicidad, no el tipo privado.",
                        "The set contract concerns membership and uniqueness, not the private type.",
                        "Mængdekontrakten handler om medlemskab og entydighed, ikke den private type.",
                    ),
                    (
                        "Comprueba resultados públicos y errores documentados.",
                        "Check public results and documented errors.",
                        "Kontrollér offentlige resultater og dokumenterede fejl.",
                    ),
                ),
                (
                    "La prueba cruza la barrera de abstracción al depender de _values y de un orden "
                    "que el contrato no promete. Debe construir la colección mediante insert, "
                    "comprobar member y len, verificar que duplicar una inserción no aumenta el "
                    "tamaño y comprobar el KeyError documentado al eliminar un ausente. La misma "
                    "función de prueba debe ejecutarse contra todas las implementaciones.",
                    "The test crosses the abstraction barrier by depending on _values and on an "
                    "order the contract does not promise. It should construct the collection with "
                    "insert, check member and len, verify that duplicate insertion does not increase "
                    "size, and check the documented KeyError when removing an absent value. The "
                    "same test function should run against every implementation.",
                    "Testen krydser abstraktionsbarrieren ved at afhænge af _values og en "
                    "rækkefølge, som kontrakten ikke lover. Den bør opbygge samlingen med insert, "
                    "kontrollere member og len, verificere at gentagen indsættelse ikke øger "
                    "størrelsen og kontrollere den dokumenterede KeyError ved fjernelse af en "
                    "manglende værdi. Den samme testfunktion bør køres mod alle implementeringer.",
                ),
                (
                    "Una prueba de contrato protege el comportamiento prometido, no una fotografía "
                    "accidental de la implementación.",
                    "A contract test protects promised behavior, not an accidental snapshot of the "
                    "implementation.",
                    "En kontrakttest beskytter lovet adfærd, ikke et tilfældigt øjebliksbillede af "
                    "implementeringen.",
                ),
            ),
        ),
        assessment_items=module.assessment_items
        + (
            objective_mcq(
                "dm857.m11.book.001",
                (
                    "¿Qué prueba respeta mejor la independencia de representación de un ADT conjunto?",
                    "Which test best respects representation independence for a set ADT?",
                    "Hvilken test respekterer bedst repræsentationsuafhængighed for et mængde-ADT?",
                ),
                (
                    (
                        "private_list",
                        (
                            "Comprobar que _values es exactamente una lista y que conserva el orden "
                            "de inserción.",
                            "Check that _values is exactly a list and preserves insertion order.",
                            "Kontrollér at _values præcis er en liste og bevarer indsættelsesrækkefølge.",
                        ),
                    ),
                    (
                        "shared_contract",
                        (
                            "Ejecutar la misma secuencia de insert, member, remove y len contra cada "
                            "implementación y comparar resultados y errores públicos.",
                            "Run the same insert, member, remove, and len sequence against every "
                            "implementation and compare public results and errors.",
                            "Kør den samme sekvens af insert, member, remove og len mod hver "
                            "implementering og sammenlign offentlige resultater og fejl.",
                        ),
                    ),
                    (
                        "memory_layout",
                        (
                            "Comparar el tamaño en bytes de todos los atributos internos y exigir "
                            "que sea idéntico.",
                            "Compare the byte size of every internal attribute and require it to be "
                            "identical.",
                            "Sammenlign byte-størrelsen af alle interne attributter og kræv, at den "
                            "er identisk.",
                        ),
                    ),
                ),
                "shared_contract",
                (
                    "La independencia de representación exige probar el contrato observable. El "
                    "tipo, orden y diseño del estado privado pueden cambiar legítimamente.",
                    "Representation independence requires testing the observable contract. The "
                    "type, order, and design of private state may legitimately change.",
                    "Repræsentationsuafhængighed kræver test af den observerbare kontrakt. Type, "
                    "rækkefølge og design af privat tilstand kan lovligt ændres.",
                ),
            ),
        ),
    )
    return _with_source_basis(
        extended,
        ("guttag-2021-ch10-12", "downey-2024-files-oop"),
    )


def apply_adts_book_extension(
    modules: tuple[LocalizedLearningModule, ...],
) -> tuple[LocalizedLearningModule, ...]:
    """Apply the M11 extension without changing any other module."""
    return tuple(
        _extend_adts(module) if module.module_id == "dm857.m11" else module for module in modules
    )
