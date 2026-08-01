"""Book-grounded extension for DM857 tree traversal and path contracts."""

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


def update_trees_audit(
    audit: tuple[ModuleSourceAudit, ...],
) -> tuple[ModuleSourceAudit, ...]:
    """Mark M10 reviewed only after its focused path extension is present."""
    updated: list[ModuleSourceAudit] = []
    for item in audit:
        if item.module_id == "dm857.m10":
            updated.append(
                replace(
                    item,
                    state="consistent",
                    finding=(
                        "Existing coverage of tree vocabulary, representations, recursive and "
                        "iterative traversals, breadth-first search, metrics, binary search "
                        "trees, complexity, invariants, and invalid structures is consistent. "
                        "Path reconstruction and the boundary between minimum-edge and "
                        "minimum-weight search needed one explicit treatment."
                    ),
                    implemented_change=(
                        "Added an original predecessor-map explanation, deterministic breadth-"
                        "first path example, weighted-path interpretation exercise, and stable "
                        "objective item."
                    ),
                )
            )
        else:
            updated.append(item)
    return tuple(updated)


def _extend_trees(module: LocalizedLearningModule) -> LocalizedLearningModule:
    """Add path reconstruction and shortest-path scope boundaries to M10."""
    extended = replace(
        module,
        objectives=module.objectives
        + (
            objective(
                "m10.bg.o1",
                (
                    "Distinguir recorrido, alcanzabilidad, reconstrucción de ruta, mínimo número "
                    "de aristas y mínimo peso total.",
                    "Distinguish traversal, reachability, path reconstruction, minimum edge "
                    "count, and minimum total weight.",
                    "Skelne mellem gennemløb, nåbarhed, rekonstruktion af sti, færrest kanter og "
                    "laveste samlede vægt.",
                ),
            ),
        ),
        concepts=module.concepts
        + (
            concept(
                "path-reconstruction-and-search-contracts",
                (
                    "Reconstrucción de rutas y contratos de búsqueda",
                    "Path reconstruction and search contracts",
                    "Rekonstruktion af stier og søgekontrakter",
                ),
                (
                    "Recorrer nodos, decidir alcanzabilidad y devolver una ruta son contratos "
                    "diferentes. Una búsqueda puede registrar para cada nodo descubierto su "
                    "predecesor; al alcanzar el objetivo, esos enlaces se siguen hacia atrás y "
                    "luego se invierten. En un árbol enraizado válido existe una única ruta simple "
                    "desde la raíz hasta cada nodo. En un grafo no ponderado con rutas alternativas, "
                    "BFS descubre por capas y la primera llegada minimiza el número de aristas. "
                    "Una DFS genérica no garantiza que la primera ruta encontrada sea la más corta. "
                    "Si las aristas tienen pesos, minimizar aristas y minimizar peso total son "
                    "problemas distintos; BFS simple no resuelve por sí sola el segundo.",
                    "Traversing nodes, deciding reachability, and returning a path are different "
                    "contracts. A search can record the predecessor of every discovered node; once "
                    "the goal is reached, those links are followed backward and then reversed. A "
                    "valid rooted tree has one unique simple path from the root to every node. In "
                    "an unweighted graph with alternative routes, BFS discovers nodes by layers, "
                    "so first discovery minimizes edge count. A generic DFS does not guarantee that "
                    "its first successful route is shortest. With weighted edges, minimizing edge "
                    "count and minimizing total weight are different problems; plain BFS does not "
                    "solve the latter by itself.",
                    "Gennemløb af noder, afgørelse af nåbarhed og returnering af en sti er "
                    "forskellige kontrakter. En søgning kan registrere forgængeren for hver "
                    "opdaget node; når målet nås, følges disse forbindelser baglæns og vendes. I et "
                    "gyldigt rodfæstet træ findes én entydig simpel sti fra roden til hver node. I "
                    "en uvægtet graf med alternative ruter opdager BFS noder lagvist, så den første "
                    "opdagelse minimerer antal kanter. En generel DFS garanterer ikke, at den første "
                    "fundne rute er kortest. Ved vægtede kanter er færrest kanter og laveste samlede "
                    "vægt forskellige problemer; almindelig BFS løser ikke automatisk det sidste.",
                ),
                (
                    (
                        "Un mapa de predecesores permite reconstruir sin copiar rutas completas en "
                        "cada paso.",
                        "A predecessor map reconstructs a path without copying complete paths at "
                        "every step.",
                        "Et forgængerkort rekonstruerer en sti uden at kopiere hele stier ved hvert "
                        "trin.",
                    ),
                    (
                        "En un árbol válido la ruta simple entre raíz y nodo es única.",
                        "In a valid tree, the simple root-to-node path is unique.",
                        "I et gyldigt træ er den simple sti fra rod til node entydig.",
                    ),
                    (
                        "BFS minimiza aristas en estructuras no ponderadas, no peso total.",
                        "BFS minimizes edges in unweighted structures, not total weight.",
                        "BFS minimerer kanter i uvægtede strukturer, ikke samlet vægt.",
                    ),
                    (
                        "La primera ruta encontrada por DFS no es una garantía de optimalidad.",
                        "The first route found by DFS is not an optimality guarantee.",
                        "Den første rute fundet af DFS er ikke en garanti for optimalitet.",
                    ),
                ),
            ),
        ),
        worked_examples=module.worked_examples
        + (
            example(
                "m10.bg.e01",
                (
                    "Reconstruir una ruta con predecesores",
                    "Reconstruct a path with predecessors",
                    "Rekonstruér en sti med forgængere",
                ),
                (
                    "Usa BFS para encontrar una ruta desde la raíz de una jerarquía didáctica y "
                    "reconstrúyela sin almacenar una copia completa por cada nodo en espera.",
                    "Use BFS to find a path from the root of a teaching hierarchy and reconstruct "
                    "it without storing a complete path copy for every queued node.",
                    "Brug BFS til at finde en sti fra roden i et undervisningshierarki og "
                    "rekonstruér den uden at gemme en fuld stikopi for hver node i køen.",
                ),
                (
                    (
                        "El diccionario parent sirve también como conjunto de descubiertos.",
                        "The parent dictionary also acts as the discovered set.",
                        "Ordbogen parent fungerer også som mængde af opdagede noder.",
                    ),
                    (
                        "La reconstrucción comienza en el objetivo y sigue predecesores.",
                        "Reconstruction starts at the goal and follows predecessors.",
                        "Rekonstruktionen starter ved målet og følger forgængere.",
                    ),
                    (
                        "Invertir al final produce el orden raíz-objetivo.",
                        "Reversing at the end produces root-to-goal order.",
                        "Vending til sidst giver rækkefølgen fra rod til mål.",
                    ),
                ),
                "from collections import deque\n\n"
                "children = {\n"
                "    'root': ('cellular', 'systems'),\n"
                "    'cellular': ('nucleus',),\n"
                "    'systems': ('immune', 'neural'),\n"
                "    'nucleus': (),\n"
                "    'immune': (),\n"
                "    'neural': (),\n"
                "}\n\n"
                "def path_by_edges(graph, start, goal):\n"
                "    queue = deque([start])\n"
                "    parent = {start: None}\n"
                "    while queue:\n"
                "        node = queue.popleft()\n"
                "        if node == goal:\n"
                "            break\n"
                "        for child in graph.get(node, ()):\n"
                "            if child not in parent:\n"
                "                parent[child] = node\n"
                "                queue.append(child)\n"
                "    if goal not in parent:\n"
                "        return None\n"
                "    path = []\n"
                "    current = goal\n"
                "    while current is not None:\n"
                "        path.append(current)\n"
                "        current = parent[current]\n"
                "    return list(reversed(path))\n\n"
                "print(path_by_edges(children, 'root', 'immune'))",
                "['root', 'systems', 'immune']",
                (
                    "La cola determina el orden por capas; parent conserva una sola referencia "
                    "por nodo descubierto y permite reconstruir la ruta al final. Los nombres son "
                    "etiquetas didácticas, no una ontología biomédica.",
                    "The queue determines layer order; parent stores one reference per discovered "
                    "node and reconstructs the route at the end. The names are teaching labels, "
                    "not a biomedical ontology.",
                    "Køen bestemmer lagrækkefølgen; parent gemmer én reference pr. opdaget node "
                    "og rekonstruerer ruten til sidst. Navnene er undervisningsetiketter, ikke en "
                    "biomedicinsk ontologi.",
                ),
            ),
        ),
        practice_exercises=module.practice_exercises
        + (
            practice(
                "m10.bg.p01",
                ActivityType.DATA_INTERPRETATION,
                (
                    "Una estructura ponderada ofrece una ruta directa A→B con peso 9 y otra "
                    "A→C→D→B con pesos 1, 1 y 1. ¿Qué optimiza BFS sin adaptación y qué ruta tiene "
                    "menor peso total?",
                    "A weighted structure offers a direct route A→B with weight 9 and another "
                    "A→C→D→B with weights 1, 1, and 1. What does unmodified BFS optimize, and "
                    "which route has lower total weight?",
                    "En vægtet struktur har en direkte rute A→B med vægt 9 og en anden "
                    "A→C→D→B med vægtene 1, 1 og 1. Hvad optimerer uændret BFS, og hvilken rute "
                    "har lavest samlet vægt?",
                ),
                (
                    (
                        "Cuenta aristas por separado de la suma de pesos.",
                        "Count edges separately from the sum of weights.",
                        "Tæl kanter separat fra summen af vægte.",
                    ),
                    (
                        "La primera ruta por capas no tiene por qué ser la más barata.",
                        "The first layer-order route need not be the cheapest.",
                        "Den første lagvise rute behøver ikke være den billigste.",
                    ),
                ),
                (
                    "BFS sin adaptación minimiza el número de aristas y por eso alcanza A→B "
                    "primero. La ruta A→C→D→B tiene peso total 3 y es más barata que la ruta "
                    "directa de peso 9. Se necesita un algoritmo de ruta mínima ponderada para "
                    "optimizar la suma de pesos.",
                    "Unmodified BFS minimizes edge count and therefore reaches A→B first. The "
                    "route A→C→D→B has total weight 3 and is cheaper than the direct route of "
                    "weight 9. A weighted shortest-path algorithm is required to optimize the "
                    "weight sum.",
                    "Uændret BFS minimerer antal kanter og når derfor A→B først. Ruten "
                    "A→C→D→B har samlet vægt 3 og er billigere end den direkte rute med vægt 9. "
                    "Der kræves en vægtet korteste-sti-algoritme for at optimere vægtsummen.",
                ),
                (
                    "La respuesta debe separar la métrica estructural —número de aristas— de la "
                    "función objetivo —suma de pesos—.",
                    "The answer must separate the structural metric—edge count—from the objective "
                    "function—the sum of weights.",
                    "Svaret skal adskille det strukturelle mål—antal kanter—fra målfunktionen—"
                    "summen af vægte.",
                ),
            ),
        ),
        assessment_items=module.assessment_items
        + (
            objective_mcq(
                "dm857.m10.book.001",
                (
                    "¿Qué afirmación describe correctamente la reconstrucción y optimalidad de "
                    "rutas?",
                    "Which statement correctly describes path reconstruction and optimality?",
                    "Hvilket udsagn beskriver korrekt rekonstruktion og optimalitet af stier?",
                ),
                (
                    (
                        "dfs_first_is_shortest",
                        (
                            "La primera ruta encontrada por cualquier DFS siempre tiene el menor "
                            "número de aristas.",
                            "The first route found by any DFS always has the fewest edges.",
                            "Den første rute fundet af enhver DFS har altid færrest kanter.",
                        ),
                    ),
                    (
                        "parent_and_scope",
                        (
                            "Un mapa de predecesores permite reconstruir la ruta; BFS garantiza "
                            "mínimo número de aristas en estructuras no ponderadas, no mínimo peso "
                            "total.",
                            "A predecessor map reconstructs the route; BFS guarantees minimum edge "
                            "count in unweighted structures, not minimum total weight.",
                            "Et forgængerkort rekonstruerer ruten; BFS garanterer færrest kanter i "
                            "uvægtede strukturer, ikke laveste samlede vægt.",
                        ),
                    ),
                    (
                        "labels_define_path",
                        (
                            "Las etiquetas repetidas bastan para identificar de forma única cada "
                            "nodo de la ruta.",
                            "Repeated labels are sufficient to identify every path node uniquely.",
                            "Gentagne etiketter er nok til entydigt at identificere hver node på "
                            "stien.",
                        ),
                    ),
                ),
                "parent_and_scope",
                (
                    "La reconstrucción depende de identidad y predecesores. La garantía de BFS se "
                    "refiere al número de aristas cuando todas se tratan con el mismo coste.",
                    "Reconstruction depends on identity and predecessors. The BFS guarantee refers "
                    "to edge count when every edge is treated as having the same cost.",
                    "Rekonstruktion afhænger af identitet og forgængere. BFS-garantien gælder "
                    "antal kanter, når alle kanter behandles som om de har samme omkostning.",
                ),
            ),
        ),
    )
    return _with_source_basis(
        extended,
        ("guttag-2021-ch10-12", "guttag-2021-ch13-15-23"),
    )


def apply_trees_book_extension(
    modules: tuple[LocalizedLearningModule, ...],
) -> tuple[LocalizedLearningModule, ...]:
    """Apply the M10 extension without changing module order or stable IDs."""
    return tuple(
        _extend_trees(module) if module.module_id == "dm857.m10" else module for module in modules
    )


__all__ = [
    "apply_trees_book_extension",
    "update_trees_audit",
]
