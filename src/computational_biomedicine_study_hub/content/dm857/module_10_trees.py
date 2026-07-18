"""DM857 module 10: hierarchical structures, trees, traversals, and testing."""

from __future__ import annotations

from ...i18n import AppLocale
from ...learning.activity_types import ActivityType
from ..localized_models import LocalizedLearningModule
from ..models import AssessmentItem, LearningModule
from .authoring import (
    authored_item,
    concept,
    example,
    objective,
    objective_mcq,
    objective_tf,
    practice,
    t,
    tutor_support,
)

LOCALIZED_MODULE_10_TREES = LocalizedLearningModule(
    course_code="DM857",
    module_id="dm857.m10",
    title=t(
        "Estructuras jerárquicas, árboles y recorridos",
        "Hierarchical structures, trees, and traversals",
        "Hierarkiske strukturer, træer og gennemløb",
    ),
    summary=t(
        "Este módulo formaliza las estructuras jerárquicas mediante árboles. Presenta vocabulario estructural, representaciones anidadas y orientadas a objetos, árboles binarios, recorridos en profundidad y anchura, métricas, búsqueda, complejidad, invariantes y pruebas. Los ejemplos biomédicos son escenarios didácticos y no protocolos clínicos.",
        "This module formalizes hierarchical structures through trees. It introduces structural vocabulary, nested and object-oriented representations, binary trees, depth-first and breadth-first traversals, metrics, search, complexity, invariants, and testing. Biomedical examples are teaching scenarios rather than clinical protocols.",
        "Dette modul formaliserer hierarkiske strukturer med træer. Det introducerer strukturelt ordforråd, indlejrede og objektorienterede repræsentationer, binære træer, dybde- og breddegennemløb, mål, søgning, kompleksitet, invarianter og test. Biomedicinske eksempler er undervisningsscenarier og ikke kliniske protokoller.",
    ),
    objectives=(
        objective("m10.o1", ("Describir árboles con terminología estructural precisa.", "Describe trees with precise structural terminology.", "Beskrive træer med præcis strukturel terminologi.")),
        objective("m10.o2", ("Representar jerarquías mediante estructuras anidadas y objetos.", "Represent hierarchies with nested structures and objects.", "Repræsentere hierarkier med indlejrede strukturer og objekter.")),
        objective("m10.o3", ("Implementar recorridos preorden, inorden y postorden.", "Implement preorder, inorder, and postorder traversals.", "Implementere preorder-, inorder- og postorder-gennemløb.")),
        objective("m10.o4", ("Implementar búsqueda en profundidad y en anchura.", "Implement depth-first and breadth-first search.", "Implementere dybde- og breddeførst søgning.")),
        objective("m10.o5", ("Calcular tamaño, altura, profundidad y número de hojas.", "Compute size, height, depth, and leaf count.", "Beregne størrelse, højde, dybde og antal blade.")),
        objective("m10.o6", ("Distinguir árboles generales, binarios y de búsqueda.", "Distinguish general, binary, and search trees.", "Skelne mellem generelle træer, binære træer og søgetræer.")),
        objective("m10.o7", ("Analizar coste temporal y espacial de recorridos.", "Analyze traversal time and space cost.", "Analysere tids- og pladsomkostning ved gennemløb.")),
        objective("m10.o8", ("Diseñar invariantes y pruebas para árboles vacíos y no vacíos.", "Design invariants and tests for empty and non-empty trees.", "Designe invarianter og test for tomme og ikke-tomme træer.")),
    ),
    concepts=(
        concept(
            "tree-vocabulary",
            ("Vocabulario e invariantes estructurales", "Vocabulary and structural invariants", "Ordforråd og strukturelle invarianter"),
            (
                "Un árbol organiza nodos mediante relaciones padre-hijo. La raíz no tiene padre; una hoja no tiene hijos; un nodo interno tiene al menos uno. La profundidad mide aristas desde la raíz y la altura mide la mayor distancia hasta una hoja. Un árbol conectado con n nodos tiene n-1 aristas y cada nodo no raíz posee exactamente un padre. Estas propiedades son invariantes que deben mantenerse al insertar, eliminar o reconstruir nodos.",
                "A tree organizes nodes through parent-child relations. The root has no parent; a leaf has no children; an internal node has at least one. Depth counts edges from the root, and height measures the greatest distance to a leaf. A connected tree with n nodes has n-1 edges, and every non-root node has exactly one parent. These properties are invariants that insertion, deletion, and reconstruction must preserve.",
                "Et træ organiserer noder gennem forælder-barn-relationer. Roden har ingen forælder; et blad har ingen børn; en intern node har mindst ét barn. Dybde tæller kanter fra roden, og højde måler den største afstand til et blad. Et sammenhængende træ med n noder har n-1 kanter, og hver ikke-rod-node har præcis én forælder. Disse egenskaber er invarianter, som ændringer skal bevare.",
            ),
            (
                ("La raíz tiene profundidad cero.", "The root has depth zero.", "Roden har dybde nul."),
                ("Una hoja puede ser también la raíz.", "A leaf may also be the root.", "Et blad kan også være roden."),
                ("Cada nodo no raíz tiene un único padre.", "Every non-root node has one parent.", "Hver ikke-rod-node har én forælder."),
            ),
        ),
        concept(
            "tree-representations",
            ("Representaciones de árboles", "Tree representations", "Trærepræsentationer"),
            (
                "Una jerarquía puede representarse con diccionarios anidados, listas de hijos, tablas padre-hijo o instancias de una clase Node. La elección determina facilidad de validación, mutabilidad y coste de navegación. Las estructuras anidadas son compactas, pero una clase puede expresar mejor identidad, métodos e invariantes. Las tablas padre-hijo son adecuadas para almacenamiento, aunque suelen requerir un índice para navegar eficientemente.",
                "A hierarchy may be represented with nested dictionaries, child lists, parent-child tables, or instances of a Node class. The choice determines validation, mutability, and navigation cost. Nested structures are compact, while a class can express identity, methods, and invariants more clearly. Parent-child tables suit storage but usually need an index for efficient navigation.",
                "Et hierarki kan repræsenteres med indlejrede ordbøger, lister over børn, forælder-barn-tabeller eller instanser af en Node-klasse. Valget påvirker validering, muterbarhed og navigationsomkostning. Indlejrede strukturer er kompakte, mens en klasse tydeligere kan udtrykke identitet, metoder og invarianter. Tabeller kræver normalt et indeks for effektiv navigation.",
            ),
            (
                ("La representación debe corresponder a las operaciones frecuentes.", "Representation should match frequent operations.", "Repræsentationen bør passe til hyppige operationer."),
                ("La identidad del nodo no es igual a su etiqueta.", "Node identity is not the same as its label.", "Nodeidentitet er ikke det samme som dens etiket."),
                ("Los ciclos deben rechazarse en una estructura que pretende ser árbol.", "Cycles must be rejected in a structure intended as a tree.", "Cykler skal afvises i en struktur, der skal være et træ."),
            ),
        ),
        concept(
            "binary-trees",
            ("Árboles binarios", "Binary trees", "Binære træer"),
            (
                "En árbol binario cada nodo tiene como máximo un hijo izquierdo y uno derecho. La posición importa: intercambiar hijos puede cambiar el significado y el resultado de un recorrido. Un árbol binario no necesita estar completo, equilibrado ni ordenado. Esas son propiedades adicionales que deben comprobarse por separado. La representación suele utilizar referencias left y right cuyo valor puede ser None.",
                "In a binary tree each node has at most one left child and one right child. Position matters: swapping children may change meaning and traversal output. A binary tree need not be complete, balanced, or ordered. Those are additional properties that must be checked separately. Representation commonly uses left and right references that may be None.",
                "I et binært træ har hver node højst ét venstre og ét højre barn. Placeringen betyder noget: byttes børnene, kan betydningen og gennemløbsresultatet ændres. Et binært træ behøver ikke være komplet, balanceret eller ordnet. Disse er ekstra egenskaber, som skal kontrolleres separat. Repræsentationen bruger ofte left- og right-referencer, som kan være None.",
            ),
            (
                ("Binario significa como máximo dos hijos.", "Binary means at most two children.", "Binær betyder højst to børn."),
                ("Izquierda y derecha son posiciones distintas.", "Left and right are distinct positions.", "Venstre og højre er forskellige positioner."),
                ("None representa un subárbol vacío.", "None represents an empty subtree.", "None repræsenterer et tomt deltræ."),
            ),
        ),
        concept(
            "depth-first-traversals",
            ("Recorridos en profundidad", "Depth-first traversals", "Dybdeførst gennemløb"),
            (
                "La búsqueda en profundidad explora un subárbol antes de pasar al siguiente. En un árbol binario, preorden visita nodo-izquierda-derecha; inorden visita izquierda-nodo-derecha; postorden visita izquierda-derecha-nodo. La diferencia es el momento en que se procesa el nodo actual. Puede implementarse recursivamente usando la pila de llamadas o iterativamente con una pila explícita. Cada variante sirve a objetivos diferentes.",
                "Depth-first search explores one subtree before moving to the next. In a binary tree, preorder visits node-left-right; inorder visits left-node-right; postorder visits left-right-node. The difference is when the current node is processed. It can be implemented recursively with the call stack or iteratively with an explicit stack. Each variant serves different goals.",
                "Dybdeførst søgning udforsker ét deltræ før det næste. I et binært træ besøger preorder node-venstre-højre; inorder venstre-node-højre; postorder venstre-højre-node. Forskellen er tidspunktet, hvor den aktuelle node behandles. Det kan implementeres rekursivt med kaldstakken eller iterativt med en eksplicit stak.",
            ),
            (
                ("Preorden procesa el nodo antes que sus hijos.", "Preorder processes the node before its children.", "Preorder behandler noden før dens børn."),
                ("Postorden procesa el nodo después de sus hijos.", "Postorder processes the node after its children.", "Postorder behandler noden efter dens børn."),
                ("Inorden sólo tiene una definición natural para árboles binarios.", "Inorder has a natural definition only for binary trees.", "Inorder har kun en naturlig definition for binære træer."),
            ),
        ),
        concept(
            "breadth-first-search",
            ("Recorrido en anchura", "Breadth-first traversal", "Breddeførst gennemløb"),
            (
                "La búsqueda en anchura procesa los nodos por niveles. Utiliza una cola: se extrae el nodo más antiguo y se añaden sus hijos al final. Es apropiada para calcular distancias mínimas en árboles no ponderados, producir niveles o encontrar la primera coincidencia más cercana a la raíz. Usar una lista con pop(0) desplaza elementos y puede degradar el rendimiento; collections.deque permite popleft en tiempo amortizado constante.",
                "Breadth-first search processes nodes level by level. It uses a queue: remove the oldest node and append its children. It suits shortest distances in unweighted trees, level generation, and finding the closest matching node to the root. Using a list with pop(0) shifts elements and may degrade performance; collections.deque provides amortized constant-time popleft.",
                "Breddeførst søgning behandler noder niveau for niveau. Den bruger en kø: fjern den ældste node og tilføj dens børn til slutningen. Den er velegnet til korteste afstande i uvægtede træer, niveaudannelse og nærmeste match til roden. En liste med pop(0) flytter elementer; collections.deque giver amortiseret konstant popleft.",
            ),
            (
                ("BFS requiere una cola FIFO.", "BFS requires a FIFO queue.", "BFS kræver en FIFO-kø."),
                ("El orden de inserción de hijos afecta al orden visible.", "Child insertion order affects visible order.", "Børnenes indsættelsesrækkefølge påvirker den synlige rækkefølge."),
                ("La memoria depende del ancho máximo.", "Memory depends on maximum width.", "Hukommelsen afhænger af maksimal bredde."),
            ),
        ),
        concept(
            "tree-metrics",
            ("Tamaño, altura, profundidad y hojas", "Size, height, depth, and leaves", "Størrelse, højde, dybde og blade"),
            (
                "El tamaño es el número de nodos. La altura de un árbol vacío debe definirse explícitamente, por ejemplo -1 si una hoja tiene altura 0, o 0 si se cuentan niveles. La profundidad pertenece a un nodo respecto a la raíz, mientras que la altura pertenece a un nodo respecto a sus descendientes. Confundir estas convenciones produce errores de uno en uno. Toda API debe documentar qué cuenta: nodos, aristas o niveles.",
                "Size is the number of nodes. The height of an empty tree must be defined explicitly, for example -1 when a leaf has height 0, or 0 when counting levels. Depth belongs to a node relative to the root, while height belongs to a node relative to descendants. Mixing conventions creates off-by-one errors. Every API should document whether it counts nodes, edges, or levels.",
                "Størrelse er antal noder. Højden af et tomt træ skal defineres eksplicit, f.eks. -1 når et blad har højde 0, eller 0 når niveauer tælles. Dybde gælder en node relativt til roden, mens højde gælder relativt til efterkommere. Blandede konventioner giver off-by-one-fejl. API'et skal dokumentere, om det tæller noder, kanter eller niveauer.",
            ),
            (
                ("Las convenciones deben permanecer constantes.", "Conventions must remain consistent.", "Konventioner skal være konsistente."),
                ("La altura suele calcularse de abajo hacia arriba.", "Height is usually computed bottom-up.", "Højde beregnes normalt nedefra og op."),
                ("La profundidad suele propagarse de arriba hacia abajo.", "Depth is usually propagated top-down.", "Dybde udbredes normalt oppefra og ned."),
            ),
        ),
        concept(
            "tree-search-and-order",
            ("Búsqueda y árboles binarios de búsqueda", "Search and binary search trees", "Søgning og binære søgetræer"),
            (
                "Un árbol binario de búsqueda añade una invariante de orden: las claves del subárbol izquierdo son menores y las del derecho mayores, según una política definida para duplicados. Esta invariante permite descartar un subárbol en cada comparación. El coste depende de la altura: un árbol equilibrado ofrece búsqueda logarítmica, mientras que uno degenerado puede comportarse como una lista y requerir tiempo lineal. Ser binario no implica ser un árbol de búsqueda.",
                "A binary search tree adds an ordering invariant: left-subtree keys are smaller and right-subtree keys larger, under a defined duplicate policy. This invariant allows discarding one subtree at each comparison. Cost depends on height: a balanced tree offers logarithmic search, while a degenerate tree may behave like a list and require linear time. Being binary does not imply being a search tree.",
                "Et binært søgetræ tilføjer en ordensinvariant: nøgler i venstre deltræ er mindre og i højre større under en defineret dubletpolitik. Invarianten gør det muligt at udelukke ét deltræ ved hver sammenligning. Omkostningen afhænger af højden: et balanceret træ giver logaritmisk søgning, mens et degenereret træ kan kræve lineær tid. Binær betyder ikke automatisk søgetræ.",
            ),
            (
                ("La invariante debe cumplirse en todos los descendientes.", "The invariant must hold for all descendants.", "Invarianten skal gælde for alle efterkommere."),
                ("El coste es O(h), donde h es la altura.", "Cost is O(h), where h is height.", "Omkostningen er O(h), hvor h er højden."),
                ("Los duplicados necesitan una política explícita.", "Duplicates need an explicit policy.", "Dubletter kræver en eksplicit politik."),
            ),
        ),
        concept(
            "complexity-and-testing",
            ("Complejidad, robustez y pruebas", "Complexity, robustness, and testing", "Kompleksitet, robusthed og test"),
            (
                "Un recorrido completo visita cada nodo una vez y suele costar O(n). El espacio auxiliar depende de la estrategia: DFS usa O(h) marcos o elementos de pila; BFS puede usar O(w), donde w es el ancho máximo. Las pruebas deben incluir árbol vacío, un solo nodo, ramas sesgadas, árbol equilibrado, etiquetas repetidas, orden de hijos, gran profundidad y estructuras inválidas con ciclos o padres múltiples. Las propiedades estructurales complementan ejemplos concretos.",
                "A complete traversal visits every node once and usually costs O(n). Auxiliary space depends on strategy: DFS uses O(h) frames or stack entries; BFS may use O(w), where w is maximum width. Tests should include an empty tree, one node, skewed branches, a balanced tree, repeated labels, child order, great depth, and invalid structures with cycles or multiple parents. Structural properties complement concrete examples.",
                "Et fuldt gennemløb besøger hver node én gang og koster normalt O(n). Ekstra plads afhænger af strategien: DFS bruger O(h) frames eller stakposter; BFS kan bruge O(w), hvor w er maksimal bredde. Test bør omfatte tomt træ, én node, skæve grene, balanceret træ, gentagne etiketter, børnerækkefølge, stor dybde og ugyldige strukturer med cykler eller flere forældre.",
            ),
            (
                ("Tiempo lineal no implica espacio lineal.", "Linear time does not imply linear space.", "Lineær tid betyder ikke lineær plads."),
                ("La forma del árbol afecta a la memoria.", "Tree shape affects memory.", "Træets form påvirker hukommelsen."),
                ("Las pruebas de propiedades detectan clases de errores.", "Property tests detect classes of errors.", "Egenskabstest opdager fejlklasser."),
            ),
        ),
    ),
    worked_examples=(
        example(
            "nested-size",
            ("Tamaño de una jerarquía anidada", "Size of a nested hierarchy", "Størrelse af et indlejret hierarki"),
            ("Cuenta todos los nodos de un diccionario con una lista children.", "Count every node in a dictionary with a children list.", "Tæl alle noder i en ordbog med en children-liste."),
            (("Contar el nodo actual.", "Count the current node.", "Tæl den aktuelle node."), ("Sumar recursivamente los hijos.", "Recursively sum children.", "Summér børnene rekursivt.")),
            "def tree_size(node):\n    return 1 + sum(tree_size(child) for child in node.get('children', []))\n\ntree = {'name': 'root', 'children': [{'name': 'A'}, {'name': 'B', 'children': [{'name': 'C'}]}]}\nprint(tree_size(tree))",
            "4",
            ("Cada llamada aporta uno y delega cada subárbol.", "Each call contributes one and delegates each subtree.", "Hvert kald bidrager med én og delegerer hvert deltræ."),
        ),
        example(
            "binary-preorder",
            ("Preorden con una clase Node", "Preorder with a Node class", "Preorder med en Node-klasse"),
            ("Produce el orden nodo-izquierda-derecha.", "Produce node-left-right order.", "Producer rækkefølgen node-venstre-højre."),
            (("Tratar None como subárbol vacío.", "Treat None as an empty subtree.", "Behandl None som tomt deltræ."), ("Visitar antes de descender.", "Visit before descending.", "Besøg før nedstigning.")),
            "from dataclasses import dataclass\n\n@dataclass\nclass Node:\n    value: str\n    left: 'Node | None' = None\n    right: 'Node | None' = None\n\ndef preorder(node):\n    if node is None:\n        return []\n    return [node.value] + preorder(node.left) + preorder(node.right)\n\nroot = Node('A', Node('B'), Node('C'))\nprint(preorder(root))",
            "['A', 'B', 'C']",
            ("El nodo actual se añade antes de recorrer ambos subárboles.", "The current node is added before both subtrees are traversed.", "Den aktuelle node tilføjes før begge deltræer gennemløbes."),
        ),
        example(
            "breadth-first-levels",
            ("Recorrido por niveles con deque", "Level-order traversal with deque", "Niveaugennemløb med deque"),
            ("Recorre un árbol general en anchura.", "Traverse a general tree breadth-first.", "Gennemløb et generelt træ i bredden."),
            (("Inicializar la cola con la raíz.", "Initialize the queue with the root.", "Initialisér køen med roden."), ("Extraer por la izquierda y añadir hijos.", "Remove from the left and append children.", "Fjern fra venstre og tilføj børn.")),
            "from collections import deque\n\ndef breadth_first(root):\n    queue = deque([root])\n    order = []\n    while queue:\n        node = queue.popleft()\n        order.append(node['name'])\n        queue.extend(node.get('children', []))\n    return order\n\nroot = {'name': 'A', 'children': [{'name': 'B'}, {'name': 'C'}]}\nprint(breadth_first(root))",
            "['A', 'B', 'C']",
            ("La cola mantiene el orden FIFO entre niveles.", "The queue maintains FIFO order across levels.", "Køen bevarer FIFO-rækkefølgen mellem niveauer."),
        ),
        example(
            "tree-height",
            ("Altura con convención de aristas", "Height using an edge convention", "Højde med kantkonvention"),
            ("Define altura(None)=-1 para que una hoja tenga altura 0.", "Define height(None)=-1 so a leaf has height 0.", "Definér height(None)=-1, så et blad har højde 0."),
            (("Retornar -1 para el vacío.", "Return -1 for empty.", "Returnér -1 for tomt."), ("Tomar uno más que la mayor altura hija.", "Take one plus the greater child height.", "Tag én plus den største børnehøjde.")),
            "def height(node):\n    if node is None:\n        return -1\n    return 1 + max(height(node.left), height(node.right))",
            "Una hoja produce 0 / A leaf produces 0 / Et blad giver 0",
            ("La convención evita una corrección especial para las hojas.", "The convention avoids a special correction for leaves.", "Konventionen undgår en særregel for blade."),
        ),
        example(
            "bst-search",
            ("Búsqueda guiada por la invariante", "Search guided by the invariant", "Søgning styret af invarianten"),
            ("Busca una clave sin recorrer ambos subárboles.", "Search for a key without traversing both subtrees.", "Søg efter en nøgle uden at gennemløbe begge deltræer."),
            (("Comparar con la clave actual.", "Compare with the current key.", "Sammenlign med den aktuelle nøgle."), ("Elegir exactamente un subárbol.", "Choose exactly one subtree.", "Vælg præcis ét deltræ.")),
            "def contains_bst(node, target):\n    while node is not None:\n        if target == node.value:\n            return True\n        node = node.left if target < node.value else node.right\n    return False",
            "True o False / True or False / True eller False",
            ("El coste es proporcional a la altura si se conserva el orden.", "Cost is proportional to height when ordering is preserved.", "Omkostningen er proportional med højden, når ordenen bevares."),
        ),
    ),
    practice_exercises=(
        practice("m10.p01", ActivityType.CODE_TRACING, ("Traza el preorden del árbol A(B(D,E),C).", "Trace preorder for A(B(D,E),C).", "Gennemgå preorder for A(B(D,E),C)."), (("Visita el nodo antes que sus hijos.", "Visit the node before its children.", "Besøg noden før dens børn."),), ("A, B, D, E, C", "A, B, D, E, C", "A, B, D, E, C"), ("Preorden procesa raíz y luego subárboles de izquierda a derecha.", "Preorder processes root and then subtrees left to right.", "Preorder behandler rod og derefter deltræer fra venstre mod højre.")),
        practice("m10.p02", ActivityType.FILL_IN_THE_BLANK, ("Completa BFS: node = queue.____().", "Complete BFS: node = queue.____().", "Udfyld BFS: node = queue.____()."), (("La cola es FIFO.", "The queue is FIFO.", "Køen er FIFO."),), ("popleft", "popleft", "popleft"), ("deque.popleft extrae el elemento más antiguo.", "deque.popleft removes the oldest element.", "deque.popleft fjerner det ældste element.")),
        practice("m10.p03", ActivityType.DEBUGGING, ("Corrige una función height que retorna 0 para None y también 0 para una hoja sin documentarlo.", "Fix a height function that returns 0 for None and also 0 for a leaf without documenting it.", "Ret en height-funktion, der returnerer 0 for None og også 0 for et blad uden dokumentation."), (("Elige aristas o niveles y sé consistente.", "Choose edges or levels and stay consistent.", "Vælg kanter eller niveauer og vær konsistent."),), ("Por aristas: height(None)=-1 y height(leaf)=0. Por niveles: height(None)=0 y height(leaf)=1.", "By edges: height(None)=-1 and height(leaf)=0. By levels: height(None)=0 and height(leaf)=1.", "Med kanter: height(None)=-1 og height(leaf)=0. Med niveauer: height(None)=0 og height(leaf)=1."), ("El problema es mezclar convenciones, no elegir una concreta.", "The problem is mixing conventions, not choosing a particular one.", "Problemet er at blande konventioner, ikke at vælge en bestemt.")),
        practice("m10.p04", ActivityType.CODE_COMPLETION, ("Implementa count_leaves(node) para un árbol general.", "Implement count_leaves(node) for a general tree.", "Implementér count_leaves(node) for et generelt træ."), (("Una hoja no tiene hijos.", "A leaf has no children.", "Et blad har ingen børn."),), ("def count_leaves(node):\n    children = node.get('children', [])\n    if not children:\n        return 1\n    return sum(count_leaves(child) for child in children)", "def count_leaves(node):\n    children = node.get('children', [])\n    if not children:\n        return 1\n    return sum(count_leaves(child) for child in children)", "def count_leaves(node):\n    children = node.get('children', [])\n    if not children:\n        return 1\n    return sum(count_leaves(child) for child in children)"), ("Las hojas aportan uno y los nodos internos agregan sus subárboles.", "Leaves contribute one and internal nodes aggregate subtrees.", "Blade bidrager med én, og interne noder aggregerer deltræer."), "def count_leaves(node):\n    pass"),
        practice("m10.p05", ActivityType.MATCHING, ("Relaciona recorrido y momento de procesar la raíz.", "Match traversal and root-processing time.", "Match gennemløb og tidspunkt for behandling af roden."), (("Compara antes, entre o después de los hijos.", "Compare before, between, or after children.", "Sammenlign før, mellem eller efter børn."),), ("Preorden-antes; inorden-entre; postorden-después.", "Preorder-before; inorder-between; postorder-after.", "Preorder-før; inorder-mellem; postorder-efter."), ("La posición del procesamiento define el recorrido.", "Processing position defines the traversal.", "Behandlingspositionen definerer gennemløbet.")),
        practice("m10.p06", ActivityType.ORDERING, ("Ordena los pasos de BFS.", "Order the BFS steps.", "Sæt BFS-trinene i rækkefølge."), (("Empieza con la raíz en una cola.", "Start with the root in a queue.", "Start med roden i en kø."),), ("Encolar raíz → extraer izquierda → procesar → encolar hijos → repetir.", "Enqueue root → remove left → process → enqueue children → repeat.", "Sæt rod i kø → fjern venstre → behandl → sæt børn i kø → gentag."), ("La cola preserva el orden por niveles.", "The queue preserves level order.", "Køen bevarer niveaurækkefølgen.")),
        practice("m10.p07", ActivityType.SHORT_ANSWER, ("Explica por qué un árbol binario no es necesariamente un árbol binario de búsqueda.", "Explain why a binary tree is not necessarily a binary search tree.", "Forklar hvorfor et binært træ ikke nødvendigvis er et binært søgetræ."), (("Binario limita hijos; búsqueda añade orden.", "Binary limits children; search adds order.", "Binær begrænser børn; søgning tilføjer orden."),), ("Un árbol binario sólo limita a dos hijos; un BST exige además una invariante global de claves.", "A binary tree only limits nodes to two children; a BST additionally requires a global key-order invariant.", "Et binært træ begrænser kun til to børn; et BST kræver også en global nøgleordensinvariant."), ("Las propiedades son independientes.", "The properties are independent.", "Egenskaberne er uafhængige.")),
        practice("m10.p08", ActivityType.DATA_INTERPRETATION, ("Un BFS alcanza 1200 nodos en la cola mientras DFS usa 18 marcos. Interpreta la diferencia.", "A BFS queue reaches 1200 nodes while DFS uses 18 frames. Interpret the difference.", "En BFS-kø når 1200 noder, mens DFS bruger 18 frames. Fortolk forskellen."), (("Compara ancho máximo y altura.", "Compare maximum width and height.", "Sammenlign maksimal bredde og højde."),), ("El árbol es ancho y relativamente poco profundo; BFS retiene un nivel grande, mientras DFS retiene principalmente una ruta.", "The tree is wide and relatively shallow; BFS retains a large level while DFS mainly retains one path.", "Træet er bredt og relativt lavt; BFS holder et stort niveau, mens DFS primært holder én sti."), ("Tiempo y memoria deben analizarse por separado.", "Time and memory must be analyzed separately.", "Tid og hukommelse skal analyseres separat.")),
        practice("m10.p09", ActivityType.DEBUGGING, ("Detecta el riesgo de recorrer una supuesta jerarquía que contiene un ciclo.", "Detect the risk of traversing a supposed hierarchy that contains a cycle.", "Find risikoen ved at gennemløbe et påstået hierarki med en cykel."), (("Un árbol no debe volver a un ancestro.", "A tree must not return to an ancestor.", "Et træ må ikke vende tilbage til en forfader."),), ("El recorrido puede no terminar. Valida la estructura o mantén un conjunto visited y rechaza una segunda visita.", "Traversal may not terminate. Validate the structure or keep a visited set and reject a second visit.", "Gennemløbet kan være uendeligt. Validér strukturen eller brug et visited-sæt og afvis andet besøg."), ("La detección de ciclos protege la invariante de árbol.", "Cycle detection protects the tree invariant.", "Cyklusdetektion beskytter træinvarianten.")),
        practice("m10.p10", ActivityType.ORAL_EXPLANATION, ("Explica la diferencia entre profundidad y altura de un nodo.", "Explain the difference between node depth and height.", "Forklar forskellen mellem en nodes dybde og højde."), (("Una mira hacia la raíz y otra hacia las hojas.", "One looks toward the root and the other toward leaves.", "Den ene ser mod roden og den anden mod bladene."),), ("La profundidad cuenta la distancia desde la raíz hasta el nodo; la altura cuenta la mayor distancia desde el nodo hasta una hoja.", "Depth counts distance from the root to the node; height counts the greatest distance from the node to a leaf.", "Dybde tæller afstand fra roden til noden; højde tæller den største afstand fra noden til et blad."), ("Ambas dependen de una convención de aristas o niveles.", "Both depend on an edge or level convention.", "Begge afhænger af en kant- eller niveaukonvention.")),
        practice("m10.p11", ActivityType.PIPELINE_DESIGN, ("Diseña una validación de una tabla parent-child antes de construir el árbol.", "Design validation for a parent-child table before building the tree.", "Design validering af en forælder-barn-tabel før træet bygges."), (("Comprueba raíz, padres, ciclos y conectividad.", "Check root, parents, cycles, and connectivity.", "Kontrollér rod, forældre, cykler og sammenhæng."),), ("Validar IDs únicos → una sola raíz → cada no-raíz con un padre → referencias existentes → ausencia de ciclos → todos los nodos alcanzables.", "Validate unique IDs → one root → one parent per non-root → existing references → no cycles → all nodes reachable.", "Validér unikke ID'er → én rod → én forælder pr. ikke-rod → eksisterende referencer → ingen cykler → alle noder kan nås."), ("La construcción debe ocurrir después de validar las invariantes.", "Construction should occur after invariants are validated.", "Konstruktion bør ske efter validering af invarianterne.")),
        practice("m10.p12", ActivityType.CODE_TRACING, ("Traza una búsqueda BST de 7 en el árbol 8(3,10), donde 3 tiene hijo derecho 6 y 6 hijo derecho 7.", "Trace BST search for 7 in 8(3,10), where 3 has right child 6 and 6 has right child 7.", "Gennemgå BST-søgning efter 7 i 8(3,10), hvor 3 har højre barn 6 og 6 højre barn 7."), (("Cada comparación elige un subárbol.", "Each comparison chooses one subtree.", "Hver sammenligning vælger ét deltræ."),), ("8 → 3 → 6 → 7", "8 → 3 → 6 → 7", "8 → 3 → 6 → 7"), ("La invariante descarta los subárboles incompatibles.", "The invariant discards incompatible subtrees.", "Invarianten udelukker inkompatible deltræer.")),
    ),
    assessment_items=(
        objective_mcq("dm857.m10.assessment.001", ("¿Qué define una hoja?", "What defines a leaf?", "Hvad definerer et blad?"), (("no_children", ("No tiene hijos", "It has no children", "Den har ingen børn")), ("no_parent", ("No tiene padre", "It has no parent", "Den har ingen forælder")), ("two_children", ("Tiene dos hijos", "It has two children", "Den har to børn")), ("depth_zero", ("Tiene profundidad cero", "It has depth zero", "Den har dybde nul"))), "no_children", ("Una hoja es un nodo sin hijos.", "A leaf is a node without children.", "Et blad er en node uden børn.")),
        authored_item("dm857.m10.assessment.002", ActivityType.MULTIPLE_SELECT, ("Selecciona invariantes de un árbol válido.", "Select invariants of a valid tree.", "Vælg invarianter for et gyldigt træ."), (), ("Una raíz, un padre por nodo no raíz y ausencia de ciclos.", "One root, one parent per non-root node, and no cycles.", "Én rod, én forælder pr. ikke-rod-node og ingen cykler."), options=(("root", ("Una raíz", "One root", "Én rod")), ("parent", ("Un padre por nodo no raíz", "One parent per non-root node", "Én forælder pr. ikke-rod-node")), ("acyclic", ("Sin ciclos", "No cycles", "Ingen cykler")), ("sorted", ("Todas las etiquetas ordenadas", "All labels sorted", "Alle etiketter sorterede"))), correct_option_ids=("root", "parent", "acyclic")),
        authored_item("dm857.m10.assessment.003", ActivityType.CODE_TRACING, ("Da el postorden de A(B(D,E),C).", "Give postorder for A(B(D,E),C).", "Angiv postorder for A(B(D,E),C)."), (("D, E, B, C, A", "D, E, B, C, A", "D, E, B, C, A"),), ("Postorden procesa hijos antes que la raíz.", "Postorder processes children before the root.", "Postorder behandler børn før roden.")),
        authored_item("dm857.m10.assessment.004", ActivityType.FILL_IN_THE_BLANK, ("Con altura por aristas, height(None)=____.", "With edge-based height, height(None)=____.", "Med kantbaseret højde er height(None)=____."), (("-1", "-1", "-1"),), ("Así una hoja tiene altura cero.", "This makes a leaf height zero.", "Så har et blad højde nul.")),
        authored_item("dm857.m10.assessment.005", ActivityType.MATCHING, ("Relaciona estrategia y estructura auxiliar.", "Match strategy and auxiliary structure.", "Match strategi og hjælpestruktur."), (), ("DFS-pila; BFS-cola.", "DFS-stack; BFS-queue.", "DFS-stak; BFS-kø."), options=(("dfs", ("DFS → pila", "DFS → stack", "DFS → stak")), ("bfs", ("BFS → cola", "BFS → queue", "BFS → kø"))), correct_option_ids=("dfs", "bfs")),
        authored_item("dm857.m10.assessment.006", ActivityType.ORDERING, ("Ordena un preorden recursivo.", "Order a recursive preorder traversal.", "Sæt et rekursivt preorder-gennemløb i rækkefølge."), (), ("Comprobar vacío → procesar nodo → recorrer izquierda → recorrer derecha.", "Check empty → process node → traverse left → traverse right.", "Kontrollér tomt → behandl node → gennemløb venstre → gennemløb højre."), options=(("empty", ("Comprobar vacío", "Check empty", "Kontrollér tomt")), ("node", ("Procesar nodo", "Process node", "Behandl node")), ("left", ("Recorrer izquierda", "Traverse left", "Gennemløb venstre")), ("right", ("Recorrer derecha", "Traverse right", "Gennemløb højre"))), correct_option_ids=("empty", "node", "left", "right")),
        authored_item("dm857.m10.assessment.007", ActivityType.CODE_COMPLETION, ("Escribe size(node) para un árbol binario.", "Write size(node) for a binary tree.", "Skriv size(node) for et binært træ."), (("def size(node):\n    if node is None:\n        return 0\n    return 1 + size(node.left) + size(node.right)", "def size(node):\n    if node is None:\n        return 0\n    return 1 + size(node.left) + size(node.right)", "def size(node):\n    if node is None:\n        return 0\n    return 1 + size(node.left) + size(node.right)"),), ("Cada nodo aporta uno.", "Each node contributes one.", "Hver node bidrager med én."), rubric=(("Incluye caso vacío.", "Includes the empty case.", "Inkluderer det tomme tilfælde."),)),
        authored_item("dm857.m10.assessment.008", ActivityType.DEBUGGING, ("Corrige BFS implementado con una pila.", "Fix BFS implemented with a stack.", "Ret BFS implementeret med en stak."), (("Sustituir la pila LIFO por una cola FIFO, preferiblemente deque.", "Replace the LIFO stack with a FIFO queue, preferably deque.", "Erstat LIFO-stakken med en FIFO-kø, helst deque."),), ("Una pila produce un recorrido en profundidad.", "A stack produces depth-first behavior.", "En stak giver dybdeførst adfærd.")),
        authored_item("dm857.m10.assessment.009", ActivityType.SHORT_ANSWER, ("Explica por qué el coste de búsqueda BST es O(h).", "Explain why BST search cost is O(h).", "Forklar hvorfor BST-søgning koster O(h)."), (("Cada comparación desciende como máximo un nivel y el número máximo de descensos es la altura h.", "Each comparison descends at most one level, and the maximum number of descents is height h.", "Hver sammenligning går højst ét niveau ned, og det maksimale antal nedstigninger er højden h."),), ("El equilibrio determina si h es logarítmica o lineal.", "Balance determines whether h is logarithmic or linear.", "Balancen afgør, om h er logaritmisk eller lineær.")),
        authored_item("dm857.m10.assessment.010", ActivityType.DATA_INTERPRETATION, ("Un recorrido visita 500 nodos una vez y mantiene como máximo 12 marcos. Indica tiempo y espacio.", "A traversal visits 500 nodes once and keeps at most 12 frames. State time and space.", "Et gennemløb besøger 500 noder én gang og holder højst 12 frames. Angiv tid og plads."), (("Tiempo O(n) y espacio auxiliar O(h), aquí h≈12.", "Time O(n) and auxiliary space O(h), here h≈12.", "Tid O(n) og ekstra plads O(h), her h≈12."),), ("La cantidad total de nodos y la profundidad máxima son medidas distintas.", "Total nodes and maximum depth are distinct measures.", "Samlet antal noder og maksimal dybde er forskellige mål.")),
        authored_item("dm857.m10.assessment.011", ActivityType.PIPELINE_DESIGN, ("Diseña un proceso para importar una jerarquía desde CSV.", "Design a process to import a hierarchy from CSV.", "Design en proces til at importere et hierarki fra CSV."), (("Leer y validar filas → indexar IDs → validar una raíz y referencias → detectar ciclos → construir hijos → comprobar alcanzabilidad.", "Read and validate rows → index IDs → validate one root and references → detect cycles → build children → check reachability.", "Læs og validér rækker → indeksér ID'er → validér én rod og referencer → find cykler → byg børn → kontrollér nåbarhed."),), ("La validación precede a la exposición del árbol.", "Validation precedes exposing the tree.", "Validering går forud for eksponering af træet."), rubric=(("Incluye detección de ciclos.", "Includes cycle detection.", "Inkluderer cyklusdetektion."),)),
        authored_item("dm857.m10.assessment.012", ActivityType.ORAL_EXPLANATION, ("Compara DFS recursivo y DFS iterativo.", "Compare recursive and iterative DFS.", "Sammenlign rekursiv og iterativ DFS."), (("Ambos siguen profundidad; el recursivo usa la pila de llamadas y es claro para árboles moderados, mientras el iterativo usa una pila explícita y controla mejor grandes profundidades.", "Both follow depth; recursive DFS uses the call stack and is clear for moderate trees, while iterative DFS uses an explicit stack and better controls great depth.", "Begge følger dybden; rekursiv DFS bruger kaldstakken og er tydelig for moderate træer, mens iterativ DFS bruger en eksplicit stak og styrer stor dybde bedre."),), ("El orden depende de cómo se apilan los hijos.", "Order depends on how children are pushed.", "Rækkefølgen afhænger af, hvordan børn lægges på stakken.")),
        authored_item("dm857.m10.assessment.013", ActivityType.DEBUGGING, ("Una función usa label como clave única y pierde nodos con etiquetas repetidas. Corrígela.", "A function uses label as a unique key and loses nodes with repeated labels. Fix it.", "En funktion bruger label som unik nøgle og mister noder med gentagne etiketter. Ret den."), (("Separar identidad estable del texto visible, por ejemplo con node_id único.", "Separate stable identity from visible text, for example with a unique node_id.", "Adskil stabil identitet fra synlig tekst, f.eks. med et unikt node_id."),), ("Las etiquetas no garantizan identidad.", "Labels do not guarantee identity.", "Etiketter garanterer ikke identitet.")),
        authored_item("dm857.m10.assessment.014", ActivityType.SHORT_ANSWER, ("Propón casos mínimos de prueba para height.", "Propose minimum test cases for height.", "Foreslå minimale testtilfælde for height."), (("Árbol vacío, una hoja, cadena sesgada, raíz con dos alturas distintas y árbol equilibrado.", "Empty tree, one leaf, a skewed chain, a root with unequal child heights, and a balanced tree.", "Tomt træ, ét blad, en skæv kæde, en rod med forskellige børnehøjder og et balanceret træ."),), ("Los casos cubren convención, base, máximo y forma.", "The cases cover convention, base, maximum, and shape.", "Tilfældene dækker konvention, base, maksimum og form.")),
    ),
    tutor_support=tutor_support(
        (
            "Un árbol es una estructura jerárquica conectada y acíclica. Tiene una raíz, cada nodo no raíz posee un único padre y los hijos forman subárboles. Las representaciones más comunes son estructuras anidadas, tablas padre-hijo y objetos Node. Los recorridos en profundidad procesan completamente un subárbol antes del siguiente; preorden, inorden y postorden se distinguen por el momento de procesar el nodo. El recorrido en anchura usa una cola FIFO y procesa niveles. Tamaño, altura, profundidad y hojas requieren convenciones explícitas. Un árbol binario limita a dos hijos; un árbol binario de búsqueda añade una invariante global de orden. Un recorrido completo suele costar O(n), mientras el espacio depende de altura o anchura. Las pruebas deben cubrir vacío, hoja, formas sesgadas y equilibradas, orden de hijos, ciclos y referencias inválidas. Los ejemplos biomédicos son ejercicios de programación y no representan protocolos.",
            "A tree is a connected acyclic hierarchical structure. It has one root, every non-root node has one parent, and children form subtrees. Common representations include nested structures, parent-child tables, and Node objects. Depth-first traversals complete one subtree before the next; preorder, inorder, and postorder differ in when the node is processed. Breadth-first traversal uses a FIFO queue and processes levels. Size, height, depth, and leaves require explicit conventions. A binary tree limits nodes to two children; a binary search tree adds a global ordering invariant. A complete traversal usually costs O(n), while space depends on height or width. Tests should cover empty, leaf, skewed and balanced shapes, child order, cycles, and invalid references. Biomedical examples are programming exercises, not protocols.",
            "Et træ er en sammenhængende, acyklisk hierarkisk struktur. Det har én rod, hver ikke-rod-node har én forælder, og børn danner deltræer. Almindelige repræsentationer er indlejrede strukturer, forælder-barn-tabeller og Node-objekter. Dybdeførst gennemløb afslutter ét deltræ før det næste; preorder, inorder og postorder adskiller sig ved tidspunktet for nodebehandling. Breddeførst gennemløb bruger en FIFO-kø og behandler niveauer. Størrelse, højde, dybde og blade kræver eksplicitte konventioner. Et binært træ begrænser til to børn; et binært søgetræ tilføjer en global ordensinvariant. Et fuldt gennemløb koster normalt O(n), mens plads afhænger af højde eller bredde. Test skal dække tomt træ, blad, skæve og balancerede former, børnerækkefølge, cykler og ugyldige referencer. Biomedicinske eksempler er programmeringsøvelser og ikke protokoller.",
        ),
        (
            ("Una jerarquía válida tiene una raíz y no contiene ciclos.", "A valid hierarchy has one root and no cycles.", "Et gyldigt hierarki har én rod og ingen cykler."),
            ("Profundidad y altura miden direcciones opuestas.", "Depth and height measure opposite directions.", "Dybde og højde måler modsatte retninger."),
            ("Preorden procesa antes; postorden después.", "Preorder processes before; postorder after.", "Preorder behandler før; postorder efter."),
            ("BFS usa cola FIFO y DFS usa pila explícita o implícita.", "BFS uses a FIFO queue and DFS an explicit or implicit stack.", "BFS bruger FIFO-kø og DFS en eksplicit eller implicit stak."),
            ("Un árbol binario no implica orden de búsqueda.", "A binary tree does not imply search ordering.", "Et binært træ indebærer ikke søgeorden."),
            ("La búsqueda BST cuesta O(h).", "BST search costs O(h).", "BST-søgning koster O(h)."),
            ("Un recorrido completo suele visitar n nodos una vez.", "A complete traversal usually visits n nodes once.", "Et fuldt gennemløb besøger normalt n noder én gang."),
            ("El espacio DFS depende de altura y BFS de anchura.", "DFS space depends on height and BFS on width.", "DFS-plads afhænger af højde og BFS af bredde."),
            ("La representación debe preservar identidad y relaciones.", "Representation must preserve identity and relations.", "Repræsentationen skal bevare identitet og relationer."),
            ("Las convenciones de altura deben documentarse.", "Height conventions must be documented.", "Højdekonventioner skal dokumenteres."),
            ("Los ciclos convierten un supuesto árbol en un grafo inválido para este contrato.", "Cycles turn a supposed tree into a graph invalid for this contract.", "Cykler gør et påstået træ til en graf, der er ugyldig for kontrakten."),
            ("Las etiquetas repetidas requieren IDs independientes.", "Repeated labels require independent IDs.", "Gentagne etiketter kræver uafhængige ID'er."),
            ("La cola deque evita el coste de desplazar listas.", "A deque avoids list-shifting cost.", "En deque undgår omkostningen ved at flytte lister."),
            ("Las pruebas estructurales complementan casos concretos.", "Structural tests complement concrete cases.", "Strukturelle test supplerer konkrete tilfælde."),
        ),
        (
            ("Creer que toda jerarquía anidada es automáticamente acíclica.", "Assuming every nested hierarchy is automatically acyclic.", "At antage at hvert indlejret hierarki automatisk er acyklisk."),
            ("Confundir hoja con nodo sin padre.", "Confusing a leaf with a node without a parent.", "At forveksle et blad med en node uden forælder."),
            ("Usar altura y profundidad como sinónimos.", "Using height and depth as synonyms.", "At bruge højde og dybde som synonymer."),
            ("Suponer que binario significa equilibrado.", "Assuming binary means balanced.", "At antage at binær betyder balanceret."),
            ("Suponer que binario significa árbol de búsqueda.", "Assuming binary means search tree.", "At antage at binær betyder søgetræ."),
            ("Implementar BFS con una pila.", "Implementing BFS with a stack.", "At implementere BFS med en stak."),
            ("Usar pop(0) sin considerar su coste.", "Using pop(0) without considering its cost.", "At bruge pop(0) uden at overveje omkostningen."),
            ("Ignorar el caso vacío.", "Ignoring the empty case.", "At ignorere det tomme tilfælde."),
            ("Tratar etiquetas visibles como identidad única.", "Treating visible labels as unique identity.", "At behandle synlige etiketter som unik identitet."),
            ("Afirmar que todo recorrido usa espacio O(n).", "Claiming every traversal uses O(n) space.", "At hævde at hvert gennemløb bruger O(n) plads."),
            ("No documentar la convención de altura.", "Failing to document the height convention.", "Ikke at dokumentere højdekonventionen."),
            ("Validar sólo ejemplos equilibrados.", "Testing only balanced examples.", "Kun at teste balancerede eksempler."),
        ),
        (
            ("¿Qué propiedad distingue una raíz de una hoja?", "What property distinguishes a root from a leaf?", "Hvilken egenskab adskiller en rod fra et blad?"),
            ("¿Qué representación facilita las operaciones requeridas?", "Which representation supports the required operations?", "Hvilken repræsentation understøtter de krævede operationer?"),
            ("¿Cuándo se procesa el nodo en este recorrido?", "When is the node processed in this traversal?", "Hvornår behandles noden i dette gennemløb?"),
            ("¿Necesitas una pila o una cola?", "Do you need a stack or a queue?", "Har du brug for en stak eller en kø?"),
            ("¿Qué convención de altura estás usando?", "Which height convention are you using?", "Hvilken højdekonvention bruger du?"),
            ("¿Qué invariante permite descartar un subárbol?", "Which invariant allows discarding a subtree?", "Hvilken invariant gør det muligt at udelukke et deltræ?"),
            ("¿Cuál es la forma extrema que debe soportar la función?", "What extreme shape must the function support?", "Hvilken ekstrem form skal funktionen understøtte?"),
            ("¿Cómo detectarías un ciclo?", "How would you detect a cycle?", "Hvordan ville du opdage en cykel?"),
            ("¿El orden de los hijos forma parte del resultado?", "Is child order part of the result?", "Er børnenes rækkefølge en del af resultatet?"),
            ("¿Qué mide n, h o w en tu análisis?", "What do n, h, or w measure in your analysis?", "Hvad måler n, h eller w i din analyse?"),
            ("¿Qué ocurre con un árbol vacío?", "What happens with an empty tree?", "Hvad sker der med et tomt træ?"),
            ("¿La etiqueta visible identifica de forma estable al nodo?", "Does the visible label stably identify the node?", "Identificerer den synlige etiket noden stabilt?"),
        ),
        (
            ("Usa terminología correcta de raíz, hoja, profundidad y altura.", "Uses correct root, leaf, depth, and height terminology.", "Bruger korrekt terminologi for rod, blad, dybde og højde."),
            ("Mantiene invariantes estructurales.", "Maintains structural invariants.", "Bevarer strukturelle invarianter."),
            ("Elige la estructura auxiliar correcta.", "Chooses the correct auxiliary structure.", "Vælger den korrekte hjælpestruktur."),
            ("Produce el orden de recorrido solicitado.", "Produces the requested traversal order.", "Producerer den ønskede gennemløbsrækkefølge."),
            ("Documenta convenciones de métricas.", "Documents metric conventions.", "Dokumenterer målkonventioner."),
            ("Analiza tiempo y espacio por separado.", "Analyzes time and space separately.", "Analyserer tid og plads separat."),
            ("Incluye casos vacíos y extremos.", "Includes empty and extreme cases.", "Inkluderer tomme og ekstreme tilfælde."),
            ("Distingue árbol binario y BST.", "Distinguishes binary tree and BST.", "Skelner mellem binært træ og BST."),
            ("Evita depender de etiquetas como identidad.", "Avoids relying on labels as identity.", "Undgår at bruge etiketter som identitet."),
            ("Explica la corrección del algoritmo.", "Explains algorithm correctness.", "Forklarer algoritmens korrekthed."),
        ),
        (
            ("No inventar protocolos clínicos a partir de ejemplos biomédicos.", "Do not invent clinical protocols from biomedical examples.", "Opfind ikke kliniske protokoller ud fra biomedicinske eksempler."),
            ("Mantenerse dentro de árboles y jerarquías.", "Stay within trees and hierarchies.", "Hold dig til træer og hierarkier."),
            ("Definir la convención de altura antes de evaluar respuestas.", "Define the height convention before grading answers.", "Definér højdekonventionen før vurdering."),
            ("No afirmar coste logarítmico sin justificar equilibrio.", "Do not claim logarithmic cost without justified balance.", "Påstå ikke logaritmisk omkostning uden begrundet balance."),
            ("Separar identidad estable de texto visible.", "Separate stable identity from visible text.", "Adskil stabil identitet fra synlig tekst."),
            ("Dar pistas progresivas antes de mostrar soluciones.", "Give progressive hints before solutions.", "Giv gradvise ledetråde før løsninger."),
            ("Explicar el orden de visita paso a paso.", "Explain visit order step by step.", "Forklar besøgsrækkefølgen trin for trin."),
            ("Considerar árbol vacío y None explícitamente.", "Consider the empty tree and None explicitly.", "Overvej tomt træ og None eksplicit."),
            ("Diferenciar tiempo de memoria auxiliar.", "Differentiate time from auxiliary memory.", "Skeln mellem tid og ekstra hukommelse."),
        ),
        (
            "Guttag, Introduction to Computation and Programming Using Python, 3rd ed.",
            "Python documentation: collections.deque and dataclasses.",
            "Compeau and Pevzner, Bioinformatics Algorithms, 2nd ed., graph and traversal foundations.",
        ),
    ),
)

_OBJECTIVE_MCQS = (
    ("001", ("¿Qué nodo no tiene padre?", "Which node has no parent?", "Hvilken node har ingen forælder?"), (("root", ("Raíz", "Root", "Rod")), ("leaf", ("Hoja", "Leaf", "Blad")), ("internal", ("Interno", "Internal", "Intern"))), "root", ("La raíz no tiene padre.", "The root has no parent.", "Roden har ingen forælder.")),
    ("002", ("¿Qué estructura usa BFS?", "Which structure does BFS use?", "Hvilken struktur bruger BFS?"), (("queue", ("Cola", "Queue", "Kø")), ("stack", ("Pila", "Stack", "Stak")), ("set", ("Conjunto", "Set", "Mængde"))), "queue", ("BFS requiere FIFO.", "BFS requires FIFO.", "BFS kræver FIFO.")),
    ("003", ("¿Qué orden es nodo-izquierda-derecha?", "Which order is node-left-right?", "Hvilken rækkefølge er node-venstre-højre?"), (("pre", ("Preorden", "Preorder", "Preorder")), ("in", ("Inorden", "Inorder", "Inorder")), ("post", ("Postorden", "Postorder", "Postorder"))), "pre", ("Preorden procesa el nodo primero.", "Preorder processes the node first.", "Preorder behandler noden først.")),
    ("004", ("¿Qué orden es izquierda-derecha-nodo?", "Which order is left-right-node?", "Hvilken rækkefølge er venstre-højre-node?"), (("post", ("Postorden", "Postorder", "Postorder")), ("pre", ("Preorden", "Preorder", "Preorder")), ("bfs", ("Anchura", "Breadth-first", "Breddeførst"))), "post", ("Postorden procesa el nodo al final.", "Postorder processes the node last.", "Postorder behandler noden sidst.")),
    ("005", ("¿Qué mide la profundidad?", "What does depth measure?", "Hvad måler dybde?"), (("root_distance", ("Distancia desde la raíz", "Distance from the root", "Afstand fra roden")), ("leaf_distance", ("Máxima distancia a una hoja", "Maximum distance to a leaf", "Maksimal afstand til et blad")), ("node_count", ("Número total de nodos", "Total node count", "Samlet antal noder"))), "root_distance", ("La profundidad mira hacia la raíz.", "Depth looks toward the root.", "Dybde ser mod roden.")),
    ("006", ("¿Qué mide la altura?", "What does height measure?", "Hvad måler højde?"), (("leaf_distance", ("Máxima distancia a una hoja", "Maximum distance to a leaf", "Maksimal afstand til et blad")), ("root_distance", ("Distancia desde la raíz", "Distance from the root", "Afstand fra roden")), ("siblings", ("Número de hermanos", "Number of siblings", "Antal søskende"))), "leaf_distance", ("La altura mira hacia los descendientes.", "Height looks toward descendants.", "Højde ser mod efterkommere.")),
    ("007", ("¿Cuál es el coste de un recorrido completo?", "What is the cost of a complete traversal?", "Hvad er omkostningen ved et fuldt gennemløb?"), (("linear", ("O(n)", "O(n)", "O(n)")), ("log", ("O(log n)", "O(log n)", "O(log n)")), ("constant", ("O(1)", "O(1)", "O(1)"))), "linear", ("Cada nodo se visita una vez.", "Each node is visited once.", "Hver node besøges én gang.")),
    ("008", ("¿De qué depende el espacio recursivo DFS?", "What determines recursive DFS space?", "Hvad bestemmer pladsen for rekursiv DFS?"), (("height", ("Altura", "Height", "Højde")), ("width", ("Anchura máxima", "Maximum width", "Maksimal bredde")), ("labels", ("Longitud de etiquetas", "Label length", "Etiketlængde"))), "height", ("La pila mantiene una ruta activa.", "The stack keeps one active path.", "Stakken holder én aktiv sti.")),
    ("009", ("¿De qué depende principalmente la memoria BFS?", "What mainly determines BFS memory?", "Hvad bestemmer primært BFS-hukommelse?"), (("width", ("Anchura máxima", "Maximum width", "Maksimal bredde")), ("height", ("Sólo altura", "Height only", "Kun højde")), ("root", ("Valor de la raíz", "Root value", "Rodværdi"))), "width", ("La cola puede retener un nivel completo.", "The queue may retain a full level.", "Køen kan holde et helt niveau.")),
    ("010", ("¿Qué añade un BST a un árbol binario?", "What does a BST add to a binary tree?", "Hvad tilføjer et BST til et binært træ?"), (("order", ("Invariante de orden", "Ordering invariant", "Ordensinvariant")), ("three", ("Tres hijos", "Three children", "Tre børn")), ("cycle", ("Un ciclo", "A cycle", "En cykel"))), "order", ("El BST ordena claves globalmente.", "A BST globally orders keys.", "Et BST ordner nøgler globalt.")),
    ("011", ("¿Qué método de deque extrae el elemento más antiguo?", "Which deque method removes the oldest element?", "Hvilken deque-metode fjerner det ældste element?"), (("popleft", ("popleft", "popleft", "popleft")), ("pop", ("pop", "pop", "pop")), ("appendleft", ("appendleft", "appendleft", "appendleft"))), "popleft", ("popleft implementa extracción FIFO.", "popleft implements FIFO removal.", "popleft implementerer FIFO-fjernelse.")),
    ("012", ("Con altura por aristas, ¿qué altura tiene una hoja?", "With edge-based height, what height has a leaf?", "Med kantbaseret højde, hvilken højde har et blad?"), (("zero", ("0", "0", "0")), ("one", ("1", "1", "1")), ("minus", ("-1", "-1", "-1"))), "zero", ("None vale -1 y la hoja suma uno.", "None is -1 and the leaf adds one.", "None er -1 og bladet lægger én til.")),
    ("013", ("¿Qué propiedad viola un nodo con dos padres?", "What property is violated by a node with two parents?", "Hvilken egenskab brydes af en node med to forældre?"), (("unique_parent", ("Padre único", "Unique parent", "Unik forælder")), ("binary", ("Máximo dos hijos", "At most two children", "Højst to børn")), ("height", ("Altura definida", "Defined height", "Defineret højde"))), "unique_parent", ("Cada nodo no raíz debe tener un padre.", "Each non-root node must have one parent.", "Hver ikke-rod-node skal have én forælder.")),
    ("014", ("¿Qué recorrido es natural para calcular altura?", "Which traversal is natural for computing height?", "Hvilket gennemløb er naturligt til at beregne højde?"), (("post", ("Postorden", "Postorder", "Postorder")), ("pre", ("Preorden", "Preorder", "Preorder")), ("bfs_only", ("Sólo BFS", "BFS only", "Kun BFS"))), "post", ("La altura del padre depende de alturas hijas.", "Parent height depends on child heights.", "Forælderens højde afhænger af børnenes højder.")),
    ("015", ("¿Qué recorrido encuentra primero una coincidencia más cercana a la raíz?", "Which traversal first finds a match closest to the root?", "Hvilket gennemløb finder først et match nærmest roden?"), (("bfs", ("BFS", "BFS", "BFS")), ("post", ("Postorden", "Postorder", "Postorder")), ("in", ("Inorden", "Inorder", "Inorder"))), "bfs", ("BFS procesa distancias crecientes.", "BFS processes increasing distances.", "BFS behandler stigende afstande.")),
    ("016", ("¿Qué representa None en un árbol binario?", "What does None represent in a binary tree?", "Hvad repræsenterer None i et binært træ?"), (("empty", ("Subárbol vacío", "Empty subtree", "Tomt deltræ")), ("leaf", ("Siempre una hoja", "Always a leaf", "Altid et blad")), ("root", ("La raíz", "The root", "Roden"))), "empty", ("None marca ausencia de nodo.", "None marks absence of a node.", "None markerer fravær af en node.")),
    ("017", ("¿Qué forma puede degradar un BST a búsqueda lineal?", "Which shape can degrade a BST to linear search?", "Hvilken form kan degradere et BST til lineær søgning?"), (("skewed", ("Cadena sesgada", "Skewed chain", "Skæv kæde")), ("balanced", ("Equilibrado", "Balanced", "Balanceret")), ("empty", ("Vacío", "Empty", "Tomt"))), "skewed", ("Una cadena tiene altura proporcional a n.", "A chain has height proportional to n.", "En kæde har højde proportional med n.")),
    ("018", ("¿Qué debe separarse de una etiqueta visible?", "What should be separated from a visible label?", "Hvad bør adskilles fra en synlig etiket?"), (("identity", ("Identidad estable", "Stable identity", "Stabil identitet")), ("height", ("Altura", "Height", "Højde")), ("queue", ("Cola", "Queue", "Kø"))), "identity", ("Las etiquetas pueden repetirse o cambiar.", "Labels may repeat or change.", "Etiketter kan gentages eller ændres.")),
    ("019", ("¿Qué comprobación detecta una estructura que no es árbol?", "Which check detects a structure that is not a tree?", "Hvilken kontrol opdager en struktur, der ikke er et træ?"), (("cycle", ("Detección de ciclos", "Cycle detection", "Cyklusdetektion")), ("lower", ("Convertir etiquetas a minúsculas", "Lowercase labels", "Små bogstaver i etiketter")), ("sort", ("Ordenar hermanos", "Sort siblings", "Sortér søskende"))), "cycle", ("Un árbol es acíclico.", "A tree is acyclic.", "Et træ er acyklisk.")),
    ("020", ("¿Qué traversal binario visita la raíz entre subárboles?", "Which binary traversal visits the root between subtrees?", "Hvilket binært gennemløb besøger roden mellem deltræer?"), (("in", ("Inorden", "Inorder", "Inorder")), ("pre", ("Preorden", "Preorder", "Preorder")), ("post", ("Postorden", "Postorder", "Postorder"))), "in", ("Inorden es izquierda-nodo-derecha.", "Inorder is left-node-right.", "Inorder er venstre-node-højre.")),
)

_OBJECTIVE_TFS = (
    ("021", ("La raíz siempre es una hoja.", "The root is always a leaf.", "Roden er altid et blad."), False, ("Sólo es hoja si no tiene hijos.", "It is a leaf only if it has no children.", "Den er kun et blad, hvis den ikke har børn.")),
    ("022", ("Un árbol conectado con n nodos tiene n-1 aristas.", "A connected tree with n nodes has n-1 edges.", "Et sammenhængende træ med n noder har n-1 kanter."), True, ("Es una propiedad estructural de los árboles.", "This is a structural tree property.", "Det er en strukturel træegenskab.")),
    ("023", ("BFS utiliza semántica LIFO.", "BFS uses LIFO semantics.", "BFS bruger LIFO-semantik."), False, ("BFS utiliza FIFO.", "BFS uses FIFO.", "BFS bruger FIFO.")),
    ("024", ("Inorden tiene una definición natural para árboles binarios.", "Inorder has a natural definition for binary trees.", "Inorder har en naturlig definition for binære træer."), True, ("Requiere posiciones izquierda y derecha.", "It relies on left and right positions.", "Det bygger på venstre og højre positioner.")),
    ("025", ("Todo árbol binario está equilibrado.", "Every binary tree is balanced.", "Hvert binært træ er balanceret."), False, ("Equilibrio es una propiedad adicional.", "Balance is an additional property.", "Balance er en ekstra egenskab.")),
    ("026", ("Un recorrido completo puede costar O(n).", "A complete traversal can cost O(n).", "Et fuldt gennemløb kan koste O(n)."), True, ("Visita cada nodo una vez.", "It visits each node once.", "Det besøger hver node én gang.")),
    ("027", ("La memoria BFS puede depender del ancho máximo.", "BFS memory may depend on maximum width.", "BFS-hukommelse kan afhænge af maksimal bredde."), True, ("La cola puede contener un nivel amplio.", "The queue may hold a wide level.", "Køen kan indeholde et bredt niveau.")),
    ("028", ("Ser binario implica cumplir la invariante BST.", "Being binary implies the BST invariant.", "At være binær indebærer BST-invarianten."), False, ("La invariante de orden es independiente.", "The ordering invariant is independent.", "Ordensinvarianten er uafhængig.")),
    ("029", ("Una etiqueta repetida puede pertenecer a nodos distintos.", "A repeated label may belong to distinct nodes.", "En gentaget etiket kan tilhøre forskellige noder."), True, ("Identidad y etiqueta deben separarse.", "Identity and label should be separate.", "Identitet og etiket bør adskilles.")),
    ("030", ("Un ciclo es compatible con la definición estricta de árbol.", "A cycle is compatible with the strict tree definition.", "En cykel er kompatibel med den strenge trædefinition."), False, ("Los árboles son acíclicos.", "Trees are acyclic.", "Træer er acykliske.")),
)

LOCALIZED_OBJECTIVE_QUESTION_BANK_10 = tuple(
    objective_mcq(
        f"dm857.m10.bank.{suffix}", prompt, options, correct_option_id, explanation
    )
    for suffix, prompt, options, correct_option_id, explanation in _OBJECTIVE_MCQS
) + tuple(
    objective_tf(
        f"dm857.m10.bank.{suffix}",
        prompt,
        correct=correct,
        explanation=explanation,
    )
    for suffix, prompt, correct, explanation in _OBJECTIVE_TFS
)


def materialize_module_10_question_bank(
    locale: AppLocale | str = AppLocale.SPANISH_SPAIN,
) -> tuple[AssessmentItem, ...]:
    """Materialize the stable objective bank in one supported locale."""
    resolved = locale if isinstance(locale, AppLocale) else AppLocale.resolve(locale)
    return tuple(item.materialize(resolved) for item in LOCALIZED_OBJECTIVE_QUESTION_BANK_10)


MODULE_10_TREES: LearningModule = LOCALIZED_MODULE_10_TREES.materialize(
    AppLocale.SPANISH_SPAIN
)
OBJECTIVE_QUESTION_BANK_10 = materialize_module_10_question_bank()

__all__ = [
    "LOCALIZED_MODULE_10_TREES",
    "LOCALIZED_OBJECTIVE_QUESTION_BANK_10",
    "MODULE_10_TREES",
    "OBJECTIVE_QUESTION_BANK_10",
    "materialize_module_10_question_bank",
]
