"""DM857 module 11: abstract data types, contracts, and core containers."""

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

LOCALIZED_MODULE_11_ADTS = LocalizedLearningModule(
    course_code="DM857",
    module_id="dm857.m11",
    title=t(
        "Tipos abstractos de datos, contratos e invariantes",
        "Abstract data types, contracts, and invariants",
        "Abstrakte datatyper, kontrakter og invarianter",
    ),
    summary=t(
        "Este módulo separa el comportamiento observable de una estructura de su representación interna. Desarrolla interfaces, contratos, invariantes, encapsulación, pilas, colas, colas de prioridad, mapas y conjuntos como abstracciones, composición, análisis de complejidad y pruebas de comportamiento.",
        "This module separates a structure's observable behavior from its internal representation. It develops interfaces, contracts, invariants, encapsulation, stacks, queues, priority queues, maps and sets as abstractions, composition, complexity analysis, and behavioral testing.",
        "Dette modul adskiller en strukturs observerbare adfærd fra dens interne repræsentation. Det udvikler interfaces, kontrakter, invarianter, indkapsling, stakke, køer, prioritetskøer, maps og mængder som abstraktioner, komposition, kompleksitetsanalyse og adfærdstest.",
    ),
    objectives=(
        objective(
            "m11.o1",
            (
                "Distinguir interfaz, contrato y representación.",
                "Distinguish interface, contract, and representation.",
                "Skelne mellem interface, kontrakt og repræsentation.",
            ),
        ),
        objective(
            "m11.o2",
            (
                "Definir invariantes de representación verificables.",
                "Define verifiable representation invariants.",
                "Definere verificerbare repræsentationsinvarianter.",
            ),
        ),
        objective(
            "m11.o3",
            (
                "Implementar y usar una pila LIFO.",
                "Implement and use a LIFO stack.",
                "Implementere og bruge en LIFO-stak.",
            ),
        ),
        objective(
            "m11.o4",
            (
                "Implementar y usar una cola FIFO.",
                "Implement and use a FIFO queue.",
                "Implementere og bruge en FIFO-kø.",
            ),
        ),
        objective(
            "m11.o5",
            (
                "Modelar prioridades con heapq y desempate estable.",
                "Model priorities with heapq and stable tie-breaking.",
                "Modellere prioriteter med heapq og stabil afgørelse af ligheder.",
            ),
        ),
        objective(
            "m11.o6",
            (
                "Seleccionar entre secuencia, mapa, conjunto, pila y cola.",
                "Choose among sequence, map, set, stack, and queue.",
                "Vælge mellem sekvens, map, mængde, stak og kø.",
            ),
        ),
        objective(
            "m11.o7",
            (
                "Componer abstracciones sin exponer detalles internos.",
                "Compose abstractions without exposing internal details.",
                "Sammensætte abstraktioner uden at afsløre interne detaljer.",
            ),
        ),
        objective(
            "m11.o8",
            (
                "Diseñar pruebas de contrato, propiedades y complejidad.",
                "Design contract, property, and complexity tests.",
                "Designe kontrakt-, egenskabs- og kompleksitetstest.",
            ),
        ),
    ),
    concepts=(
        concept(
            "adt-interface-contract",
            (
                "Abstracción, interfaz y contrato",
                "Abstraction, interface, and contract",
                "Abstraktion, interface og kontrakt",
            ),
            (
                "Un tipo abstracto de datos se define por valores válidos y operaciones observables, no por una estructura concreta. La interfaz enumera las operaciones; el contrato especifica precondiciones, resultados, errores y efectos; la implementación decide cómo almacenar el estado. Dos implementaciones son intercambiables cuando cumplen el mismo comportamiento observable. Esta separación permite cambiar rendimiento o representación sin obligar a modificar el código cliente.",
                "An abstract data type is defined by valid values and observable operations, not by one concrete structure. The interface lists operations; the contract specifies preconditions, results, errors, and effects; the implementation decides how state is stored. Two implementations are interchangeable when they satisfy the same observable behavior. This separation permits changing performance or representation without changing client code.",
                "En abstrakt datatype defineres af gyldige værdier og observerbare operationer, ikke af én konkret struktur. Interfacet oplister operationer; kontrakten angiver forudsætninger, resultater, fejl og effekter; implementeringen bestemmer lagring af tilstand. To implementeringer kan udskiftes, når de opfylder samme observerbare adfærd.",
            ),
            (
                (
                    "El cliente depende del contrato, no de la lista interna.",
                    "Clients depend on the contract, not the internal list.",
                    "Klienten afhænger af kontrakten, ikke den interne liste.",
                ),
                (
                    "La complejidad puede formar parte del contrato.",
                    "Complexity may be part of the contract.",
                    "Kompleksitet kan være en del af kontrakten.",
                ),
                (
                    "Los errores esperados deben documentarse.",
                    "Expected errors should be documented.",
                    "Forventede fejl bør dokumenteres.",
                ),
            ),
        ),
        concept(
            "representation-invariants",
            (
                "Invariantes de representación",
                "Representation invariants",
                "Repræsentationsinvarianter",
            ),
            (
                "Una invariante de representación describe condiciones que el estado interno debe cumplir después de construir el objeto y después de cada operación pública. En una cola circular puede exigir índices dentro de rango y tamaño coherente; en una pila acotada, 0 <= tamaño <= capacidad. Las operaciones pueden modificar temporalmente el estado, pero deben restablecer la invariante antes de devolver control. Las aserciones internas ayudan durante desarrollo, aunque no sustituyen la validación de entradas externas.",
                "A representation invariant states conditions that internal state must satisfy after construction and after every public operation. A circular queue may require indices within bounds and a consistent size; a bounded stack may require 0 <= size <= capacity. Operations may temporarily modify state, but must restore the invariant before returning control. Internal assertions help during development but do not replace validation of external inputs.",
                "En repræsentationsinvariant beskriver betingelser, som den interne tilstand skal opfylde efter konstruktion og efter hver offentlig operation. En cirkulær kø kan kræve indeks inden for grænser og konsistent størrelse; en begrænset stak kan kræve 0 <= størrelse <= kapacitet. Operationer må midlertidigt ændre tilstanden, men skal gendanne invarianten før retur.",
            ),
            (
                (
                    "La invariante debe poder comprobarse.",
                    "The invariant should be checkable.",
                    "Invarianten bør kunne kontrolleres.",
                ),
                (
                    "Cada mutación pública debe preservarla.",
                    "Every public mutation must preserve it.",
                    "Hver offentlig mutation skal bevare den.",
                ),
                (
                    "Una aserción interna no es un mensaje de usuario.",
                    "An internal assertion is not a user-facing error.",
                    "En intern assertion er ikke en brugerfejl.",
                ),
            ),
        ),
        concept(
            "stack-adt",
            ("Pila LIFO", "LIFO stack", "LIFO-stak"),
            (
                "Una pila expone push, pop, peek, is_empty y, a menudo, len. La última entrada es la primera en salir. Una lista de Python implementa eficientemente el extremo final mediante append y pop. La abstracción debe definir qué ocurre al extraer de una pila vacía: lanzar una excepción específica suele ser más claro que devolver un valor ambiguo. Las pilas modelan deshacer, evaluación de expresiones, validación de delimitadores y DFS iterativo.",
                "A stack exposes push, pop, peek, is_empty, and often len. The last inserted item is the first removed. A Python list efficiently implements the end through append and pop. The abstraction must define empty-pop behavior: raising a specific exception is often clearer than returning an ambiguous value. Stacks model undo, expression evaluation, delimiter validation, and iterative DFS.",
                "En stak eksponerer push, pop, peek, is_empty og ofte len. Det sidst indsatte element fjernes først. En Python-liste implementerer enden effektivt med append og pop. Abstraktionen skal definere pop på tom stak; en specifik exception er ofte tydeligere end en tvetydig værdi. Stakke modellerer undo, udtryksevaluering og iterativ DFS.",
            ),
            (
                (
                    "push y pop operan sobre el mismo extremo.",
                    "push and pop operate on the same end.",
                    "push og pop arbejder på samme ende.",
                ),
                (
                    "peek no elimina el elemento.",
                    "peek does not remove the item.",
                    "peek fjerner ikke elementet.",
                ),
                (
                    "El caso vacío pertenece al contrato.",
                    "The empty case belongs to the contract.",
                    "Det tomme tilfælde hører til kontrakten.",
                ),
            ),
        ),
        concept(
            "queue-adt",
            ("Cola FIFO", "FIFO queue", "FIFO-kø"),
            (
                "Una cola expone enqueue, dequeue, front, is_empty y len. El primer elemento insertado es el primero en salir. collections.deque ofrece append y popleft con coste amortizado constante, mientras list.pop(0) desplaza los elementos restantes. Una cola puede ser ilimitada o acotada; en el segundo caso el contrato debe definir qué sucede al alcanzar capacidad. Las colas modelan planificación, buffers y recorridos en anchura.",
                "A queue exposes enqueue, dequeue, front, is_empty, and len. The first inserted item is the first removed. collections.deque provides append and popleft with amortized constant cost, while list.pop(0) shifts remaining items. A queue may be unbounded or bounded; in the latter case the contract must define behavior at capacity. Queues model scheduling, buffers, and breadth-first traversal.",
                "En kø eksponerer enqueue, dequeue, front, is_empty og len. Det først indsatte element fjernes først. collections.deque giver append og popleft med amortiseret konstant omkostning, mens list.pop(0) flytter resten. En kø kan være ubegrænset eller begrænset; i sidste tilfælde skal kontrakten definere adfærd ved kapacitet.",
            ),
            (
                (
                    "enqueue añade al final y dequeue retira del frente.",
                    "enqueue appends at the rear and dequeue removes from the front.",
                    "enqueue tilføjer bagest og dequeue fjerner forrest.",
                ),
                (
                    "FIFO conserva orden temporal.",
                    "FIFO preserves temporal order.",
                    "FIFO bevarer tidsrækkefølgen.",
                ),
                (
                    "deque evita desplazamientos lineales.",
                    "deque avoids linear shifts.",
                    "deque undgår lineære flytninger.",
                ),
            ),
        ),
        concept(
            "priority-queue",
            ("Cola de prioridad y montículo", "Priority queue and heap", "Prioritetskø og heap"),
            (
                "Una cola de prioridad devuelve el elemento con prioridad extrema, no necesariamente el más antiguo. heapq implementa un min-heap sobre una lista. Insertar y extraer cuesta O(log n), y consultar el mínimo O(1). Si dos prioridades coinciden, comparar directamente objetos no ordenables puede fallar; una tupla (prioridad, contador, elemento) introduce un desempate estable. Actualizar prioridad suele requerir entradas nuevas y marcado de las antiguas, o una abstracción especializada.",
                "A priority queue returns the item with extreme priority, not necessarily the oldest. heapq implements a min-heap over a list. Insertion and removal cost O(log n), and reading the minimum costs O(1). If priorities tie, direct comparison of non-orderable objects may fail; a tuple (priority, counter, item) provides stable tie-breaking. Priority updates often require new entries and marking old ones, or a specialized abstraction.",
                "En prioritetskø returnerer elementet med ekstrem prioritet, ikke nødvendigvis det ældste. heapq implementerer en min-heap over en liste. Indsættelse og fjernelse koster O(log n), og aflæsning af minimum O(1). Ved ens prioriteter kan sammenligning af ikke-ordnede objekter fejle; tuplen (prioritet, tæller, element) giver stabil afgørelse.",
            ),
            (
                ("heapq es un min-heap.", "heapq is a min-heap.", "heapq er en min-heap."),
                (
                    "El contador evita comparar elementos empatados.",
                    "The counter avoids comparing tied items.",
                    "Tælleren undgår sammenligning af elementer med samme prioritet.",
                ),
                (
                    "El orden de heap no es una lista totalmente ordenada.",
                    "Heap order is not a fully sorted list.",
                    "Heap-rækkefølge er ikke en fuldt sorteret liste.",
                ),
            ),
        ),
        concept(
            "maps-sets-as-adts",
            (
                "Mapas y conjuntos como abstracciones",
                "Maps and sets as abstractions",
                "Maps og mængder som abstraktioner",
            ),
            (
                "Un mapa asocia claves únicas con valores y un conjunto representa pertenencia sin duplicados. Aunque dict y set son implementaciones concretas de Python, el código cliente debería razonar sobre operaciones abstractas: insertar, buscar, eliminar, iterar y comprobar pertenencia. La semántica de igualdad y hashabilidad forma parte del contrato. Elegir un mapa para contar o un conjunto para deduplicar expresa mejor la intención que una lista con búsquedas repetidas.",
                "A map associates unique keys with values, and a set represents membership without duplicates. Although dict and set are concrete Python implementations, client code should reason about abstract operations: insert, lookup, remove, iterate, and test membership. Equality and hashability semantics belong to the contract. Choosing a map for counting or a set for deduplication expresses intent better than a list with repeated searches.",
                "Et map forbinder unikke nøgler med værdier, og en mængde repræsenterer medlemskab uden dubletter. Selvom dict og set er konkrete Python-implementeringer, bør klientkode tænke i abstrakte operationer: indsæt, opslag, fjern, iterér og medlemskab. Lighed og hashbarhed hører til kontrakten.",
            ),
            (
                (
                    "La clave identifica una asociación.",
                    "The key identifies an association.",
                    "Nøglen identificerer en association.",
                ),
                (
                    "El conjunto no conserva duplicados.",
                    "A set does not retain duplicates.",
                    "En mængde bevarer ikke dubletter.",
                ),
                (
                    "La intención de acceso guía la estructura.",
                    "Access intent guides the structure.",
                    "Adgangsintentionen styrer strukturen.",
                ),
            ),
        ),
        concept(
            "composition-and-encapsulation",
            (
                "Composición y encapsulación",
                "Composition and encapsulation",
                "Komposition og indkapsling",
            ),
            (
                "Una abstracción puede construirse componiendo otras: un historial de deshacer usa dos pilas; un planificador combina una cola de prioridad y un mapa de tareas; un buffer acotado envuelve una deque. La representación interna debe mantenerse privada por convención o mediante atributos protegidos, y no debe devolverse una referencia mutable que permita violar invariantes. Exponer una copia, una vista inmutable o un iterador controlado conserva el encapsulamiento.",
                "An abstraction may be built by composing others: undo history uses two stacks; a scheduler combines a priority queue and a task map; a bounded buffer wraps a deque. Internal representation should remain private by convention or protected attributes, and mutable references that permit invariant violations should not be returned. A copy, immutable view, or controlled iterator preserves encapsulation.",
                "En abstraktion kan bygges ved at sammensætte andre: undo-historik bruger to stakke; en planlægger kombinerer prioritetskø og opgavemap; en begrænset buffer indpakker en deque. Den interne repræsentation bør forblive privat, og muterbare referencer, der kan bryde invarianter, bør ikke returneres. En kopi eller kontrolleret iterator bevarer indkapsling.",
            ),
            (
                (
                    "Composición reutiliza contratos existentes.",
                    "Composition reuses existing contracts.",
                    "Komposition genbruger eksisterende kontrakter.",
                ),
                (
                    "No expongas el contenedor interno mutable.",
                    "Do not expose the mutable internal container.",
                    "Eksponér ikke den muterbare interne container.",
                ),
                (
                    "Las operaciones públicas deben ser la única vía de mutación.",
                    "Public operations should be the only mutation path.",
                    "Offentlige operationer bør være den eneste mutationsvej.",
                ),
            ),
        ),
        concept(
            "behavioral-testing-complexity",
            (
                "Pruebas de comportamiento y complejidad",
                "Behavioral and complexity testing",
                "Adfærds- og kompleksitetstest",
            ),
            (
                "Las pruebas de un ADT se formulan contra su contrato, no contra atributos privados. Deben cubrir construcción, secuencias normales, estados vacíos y llenos, errores, preservación de orden, idempotencia cuando corresponda y aislamiento entre instancias. Las pruebas de propiedades verifican relaciones como push(x) seguido de pop() devuelve x. La complejidad esperada puede comprobarse indirectamente con tamaños crecientes o revisando que la implementación use la estructura adecuada.",
                "ADT tests are written against the contract, not private attributes. They should cover construction, normal sequences, empty and full states, errors, order preservation, idempotence where applicable, and isolation between instances. Property tests verify relations such as push(x) followed by pop() returns x. Expected complexity can be checked indirectly with increasing sizes or by verifying that the appropriate structure is used.",
                "ADT-test skrives mod kontrakten, ikke private attributter. De bør dække konstruktion, normale sekvenser, tomme og fulde tilstande, fejl, rækkefølge, idempotens hvor relevant og isolation mellem instanser. Egenskabstest kontrollerer relationer som at push(x) efterfulgt af pop() returnerer x. Forventet kompleksitet kan kontrolleres indirekte med voksende størrelser eller passende struktur.",
            ),
            (
                (
                    "Prueba resultados observables.",
                    "Test observable results.",
                    "Test observerbare resultater.",
                ),
                (
                    "Incluye secuencias de operaciones, no sólo llamadas aisladas.",
                    "Include operation sequences, not only isolated calls.",
                    "Inkludér operationssekvenser, ikke kun isolerede kald.",
                ),
                (
                    "La implementación puede cambiar sin romper las pruebas.",
                    "Implementation may change without breaking tests.",
                    "Implementeringen kan ændres uden at bryde testene.",
                ),
            ),
        ),
    ),
    worked_examples=(
        example(
            "stack-class",
            (
                "Pila con contrato explícito",
                "Stack with an explicit contract",
                "Stak med eksplicit kontrakt",
            ),
            (
                "Implementa push, pop, peek y len sin exponer la lista interna.",
                "Implement push, pop, peek, and len without exposing the internal list.",
                "Implementér push, pop, peek og len uden at eksponere den interne liste.",
            ),
            (
                (
                    "Guardar elementos en una lista privada.",
                    "Store items in a private list.",
                    "Gem elementer i en privat liste.",
                ),
                (
                    "Lanzar IndexError al consultar el vacío.",
                    "Raise IndexError on empty access.",
                    "Kast IndexError ved adgang til tom stak.",
                ),
            ),
            "class Stack:\n    def __init__(self):\n        self._items = []\n\n    def push(self, item):\n        self._items.append(item)\n\n    def pop(self):\n        if not self._items:\n            raise IndexError('pop from empty stack')\n        return self._items.pop()\n\n    def peek(self):\n        if not self._items:\n            raise IndexError('peek from empty stack')\n        return self._items[-1]\n\n    def __len__(self):\n        return len(self._items)\n\ns = Stack(); s.push('A'); s.push('B'); print(s.pop(), s.peek())",
            "B A",
            (
                "El cliente observa LIFO sin depender de la lista.",
                "The client observes LIFO without depending on the list.",
                "Klienten observerer LIFO uden at afhænge af listen.",
            ),
        ),
        example(
            "balanced-delimiters",
            (
                "Validación de delimitadores con pila",
                "Delimiter validation with a stack",
                "Validering af afgrænsere med en stak",
            ),
            (
                "Comprueba que paréntesis, corchetes y llaves estén correctamente anidados.",
                "Check that parentheses, brackets, and braces are correctly nested.",
                "Kontrollér at parenteser, klammer og tuborgklammer er korrekt indlejret.",
            ),
            (
                ("Apilar aperturas.", "Push opening symbols.", "Læg åbningssymboler på stakken."),
                (
                    "Cada cierre debe coincidir con la cima.",
                    "Each closing symbol must match the top.",
                    "Hvert lukningssymbol skal matche toppen.",
                ),
            ),
            "def balanced(text):\n    pairs = {')': '(', ']': '[', '}': '{'}\n    stack = []\n    for char in text:\n        if char in pairs.values():\n            stack.append(char)\n        elif char in pairs:\n            if not stack or stack.pop() != pairs[char]:\n                return False\n    return not stack\n\nprint(balanced('a[(b+c)]'))",
            "True",
            (
                "La cima representa la apertura pendiente más reciente.",
                "The top represents the most recent pending opening symbol.",
                "Toppen repræsenterer det seneste ventende åbningssymbol.",
            ),
        ),
        example(
            "queue-deque",
            ("Cola con deque", "Queue with deque", "Kø med deque"),
            (
                "Conserva el orden de llegada de tres elementos.",
                "Preserve arrival order for three items.",
                "Bevar ankomstrækkefølgen for tre elementer.",
            ),
            (
                ("Añadir con append.", "Append with append.", "Tilføj med append."),
                ("Retirar con popleft.", "Remove with popleft.", "Fjern med popleft."),
            ),
            "from collections import deque\n\nqueue = deque()\nfor item in ['A', 'B', 'C']:\n    queue.append(item)\nprint(queue.popleft(), queue.popleft())",
            "A B",
            (
                "La operación es FIFO y evita desplazar la lista.",
                "The operation is FIFO and avoids shifting a list.",
                "Operationen er FIFO og undgår at flytte en liste.",
            ),
        ),
        example(
            "stable-priority-queue",
            (
                "Prioridad con desempate estable",
                "Priority with stable tie-breaking",
                "Prioritet med stabil afgørelse",
            ),
            (
                "Procesa primero menor prioridad numérica y conserva llegada entre empates.",
                "Process lower numeric priority first and preserve arrival order for ties.",
                "Behandl lavere numerisk prioritet først og bevar ankomstorden ved lighed.",
            ),
            (
                (
                    "Usar un contador creciente.",
                    "Use an increasing counter.",
                    "Brug en stigende tæller.",
                ),
                (
                    "Insertar tuplas prioridad-contador-elemento.",
                    "Insert priority-counter-item tuples.",
                    "Indsæt tupler med prioritet-tæller-element.",
                ),
            ),
            "import heapq\nfrom itertools import count\n\ncounter = count()\nheap = []\nfor priority, item in [(2, 'A'), (1, 'B'), (1, 'C')]:\n    heapq.heappush(heap, (priority, next(counter), item))\nprint([heapq.heappop(heap)[2] for _ in range(3)])",
            "['B', 'C', 'A']",
            (
                "El contador resuelve empates sin comparar strings u objetos de dominio.",
                "The counter resolves ties without comparing domain objects.",
                "Tælleren løser ligheder uden at sammenligne domæneobjekter.",
            ),
        ),
        example(
            "bounded-buffer",
            ("Buffer acotado compuesto", "Composed bounded buffer", "Sammensat begrænset buffer"),
            (
                "Envuelve una deque y rechaza inserciones cuando está lleno.",
                "Wrap a deque and reject insertion when full.",
                "Indpak en deque og afvis indsættelse, når den er fuld.",
            ),
            (
                (
                    "Guardar capacidad positiva.",
                    "Store a positive capacity.",
                    "Gem en positiv kapacitet.",
                ),
                (
                    "Comprobar len antes de append.",
                    "Check len before append.",
                    "Kontrollér len før append.",
                ),
            ),
            "from collections import deque\n\nclass BoundedBuffer:\n    def __init__(self, capacity):\n        if capacity <= 0:\n            raise ValueError('capacity must be positive')\n        self._capacity = capacity\n        self._items = deque()\n\n    def put(self, item):\n        if len(self._items) == self._capacity:\n            raise OverflowError('buffer full')\n        self._items.append(item)\n\n    def get(self):\n        if not self._items:\n            raise IndexError('buffer empty')\n        return self._items.popleft()",
            "put conserva 0 <= len <= capacity / put preserves 0 <= len <= capacity / put bevarer 0 <= len <= capacity",
            (
                "La clase compone deque y protege la invariante de capacidad.",
                "The class composes deque and protects the capacity invariant.",
                "Klassen sammensætter deque og beskytter kapacitetsinvarianten.",
            ),
        ),
    ),
    practice_exercises=(
        practice(
            "m11.p01",
            ActivityType.CODE_TRACING,
            (
                "Traza push(1), push(2), pop(), push(3), peek().",
                "Trace push(1), push(2), pop(), push(3), peek().",
                "Gennemgå push(1), push(2), pop(), push(3), peek().",
            ),
            (("La pila es LIFO.", "The stack is LIFO.", "Stakken er LIFO."),),
            (
                "pop devuelve 2; peek devuelve 3; el estado final es [1, 3].",
                "pop returns 2; peek returns 3; final state is [1, 3].",
                "pop returnerer 2; peek returnerer 3; sluttilstanden er [1, 3].",
            ),
            (
                "peek observa sin eliminar.",
                "peek observes without removing.",
                "peek observerer uden at fjerne.",
            ),
        ),
        practice(
            "m11.p02",
            ActivityType.FILL_IN_THE_BLANK,
            (
                "Completa una cola deque: item = queue.____().",
                "Complete a deque queue: item = queue.____().",
                "Udfyld en deque-kø: item = queue.____().",
            ),
            (
                (
                    "Retira el elemento más antiguo.",
                    "Remove the oldest item.",
                    "Fjern det ældste element.",
                ),
            ),
            ("popleft", "popleft", "popleft"),
            (
                "popleft implementa dequeue FIFO.",
                "popleft implements FIFO dequeue.",
                "popleft implementerer FIFO-dequeue.",
            ),
        ),
        practice(
            "m11.p03",
            ActivityType.DEBUGGING,
            (
                "Corrige una cola implementada con append y pop().",
                "Fix a queue implemented with append and pop().",
                "Ret en kø implementeret med append og pop().",
            ),
            (
                (
                    "pop() retira el elemento más reciente.",
                    "pop() removes the newest item.",
                    "pop() fjerner det nyeste element.",
                ),
            ),
            (
                "Usar deque.append y deque.popleft, o definir claramente otra política.",
                "Use deque.append and deque.popleft, or clearly define another policy.",
                "Brug deque.append og deque.popleft, eller definér tydeligt en anden politik.",
            ),
            (
                "append/pop produce LIFO, no FIFO.",
                "append/pop produce LIFO, not FIFO.",
                "append/pop giver LIFO, ikke FIFO.",
            ),
        ),
        practice(
            "m11.p04",
            ActivityType.CODE_COMPLETION,
            (
                "Añade is_empty y __len__ a una Stack.",
                "Add is_empty and __len__ to a Stack.",
                "Tilføj is_empty og __len__ til en Stack.",
            ),
            (
                (
                    "Ambas consultan la colección interna.",
                    "Both inspect the internal collection.",
                    "Begge læser den interne samling.",
                ),
            ),
            (
                "def is_empty(self):\n    return not self._items\n\ndef __len__(self):\n    return len(self._items)",
                "def is_empty(self):\n    return not self._items\n\ndef __len__(self):\n    return len(self._items)",
                "def is_empty(self):\n    return not self._items\n\ndef __len__(self):\n    return len(self._items)",
            ),
            (
                "No es necesario exponer self._items.",
                "There is no need to expose self._items.",
                "Det er ikke nødvendigt at eksponere self._items.",
            ),
            "class Stack:\n    def is_empty(self):\n        pass\n\n    def __len__(self):\n        pass",
        ),
        practice(
            "m11.p05",
            ActivityType.MATCHING,
            (
                "Relaciona ADT y política de acceso.",
                "Match ADT and access policy.",
                "Match ADT og adgangspolitik.",
            ),
            (
                (
                    "LIFO, FIFO y prioridad son políticas distintas.",
                    "LIFO, FIFO, and priority are distinct policies.",
                    "LIFO, FIFO og prioritet er forskellige politikker.",
                ),
            ),
            (
                "Pila-LIFO; cola-FIFO; cola de prioridad-prioridad extrema.",
                "Stack-LIFO; queue-FIFO; priority queue-extreme priority.",
                "Stak-LIFO; kø-FIFO; prioritetskø-ekstrem prioritet.",
            ),
            (
                "La política observable define la abstracción.",
                "Observable policy defines the abstraction.",
                "Den observerbare politik definerer abstraktionen.",
            ),
        ),
        practice(
            "m11.p06",
            ActivityType.ORDERING,
            (
                "Ordena una operación mutadora segura.",
                "Order a safe mutating operation.",
                "Sæt en sikker muterende operation i rækkefølge.",
            ),
            (
                (
                    "Valida antes de confirmar el nuevo estado.",
                    "Validate before committing new state.",
                    "Validér før den nye tilstand bekræftes.",
                ),
            ),
            (
                "Comprobar precondición → calcular cambio → actualizar estado → verificar invariante → retornar.",
                "Check precondition → compute change → update state → verify invariant → return.",
                "Kontrollér forudsætning → beregn ændring → opdatér tilstand → verificér invariant → returnér.",
            ),
            (
                "La invariante debe cumplirse al salir.",
                "The invariant must hold on exit.",
                "Invarianten skal gælde ved retur.",
            ),
        ),
        practice(
            "m11.p07",
            ActivityType.SHORT_ANSWER,
            (
                "Distingue interfaz y representación de una pila.",
                "Distinguish a stack interface and representation.",
                "Skeln mellem en staks interface og repræsentation.",
            ),
            (
                (
                    "La interfaz son operaciones; la representación almacena estado.",
                    "The interface is operations; representation stores state.",
                    "Interfacet er operationer; repræsentationen lagrer tilstand.",
                ),
            ),
            (
                "La interfaz incluye push, pop y peek; la representación puede ser una lista, deque u otra estructura sin cambiar el contrato.",
                "The interface includes push, pop, and peek; representation may be a list, deque, or another structure without changing the contract.",
                "Interfacet omfatter push, pop og peek; repræsentationen kan være liste, deque eller anden struktur uden at ændre kontrakten.",
            ),
            (
                "El cliente no debe depender del atributo interno.",
                "Clients should not depend on the internal attribute.",
                "Klienten bør ikke afhænge af den interne attribut.",
            ),
        ),
        practice(
            "m11.p08",
            ActivityType.DATA_INTERPRETATION,
            (
                "Una cola basada en list tarda cada vez más al usar pop(0). Interpreta el patrón.",
                "A list-based queue becomes slower with pop(0). Interpret the pattern.",
                "En listebaseret kø bliver langsommere med pop(0). Fortolk mønsteret.",
            ),
            (
                (
                    "Los elementos restantes se desplazan.",
                    "Remaining elements are shifted.",
                    "De resterende elementer flyttes.",
                ),
            ),
            (
                "dequeue es O(n) con pop(0); una deque ofrece popleft amortizado O(1).",
                "dequeue is O(n) with pop(0); a deque provides amortized O(1) popleft.",
                "dequeue er O(n) med pop(0); en deque giver amortiseret O(1) popleft.",
            ),
            (
                "La representación afecta al rendimiento aunque el contrato sea el mismo.",
                "Representation affects performance even when the contract is the same.",
                "Repræsentationen påvirker ydelsen, selv om kontrakten er den samme.",
            ),
        ),
        practice(
            "m11.p09",
            ActivityType.DEBUGGING,
            (
                "Corrige una PriorityQueue que inserta (priority, item) cuando item no es ordenable.",
                "Fix a PriorityQueue that inserts (priority, item) when item is not orderable.",
                "Ret en PriorityQueue, der indsætter (priority, item), når item ikke kan ordnes.",
            ),
            (
                (
                    "Los empates obligan a comparar item.",
                    "Ties force item comparison.",
                    "Ligheder tvinger sammenligning af item.",
                ),
            ),
            (
                "Insertar (priority, counter, item) con un contador único creciente.",
                "Insert (priority, counter, item) with a unique increasing counter.",
                "Indsæt (priority, counter, item) med en unik stigende tæller.",
            ),
            (
                "El contador garantiza un segundo campo comparable y estable.",
                "The counter provides a comparable stable second field.",
                "Tælleren giver et sammenligneligt stabilt andet felt.",
            ),
        ),
        practice(
            "m11.p10",
            ActivityType.ORAL_EXPLANATION,
            (
                "Explica por qué devolver self._items rompe encapsulación.",
                "Explain why returning self._items breaks encapsulation.",
                "Forklar hvorfor returnering af self._items bryder indkapsling.",
            ),
            (
                (
                    "El cliente obtiene una referencia mutable.",
                    "The client gets a mutable reference.",
                    "Klienten får en muterbar reference.",
                ),
            ),
            (
                "El cliente puede modificar el contenedor sin pasar por operaciones públicas y violar invariantes. Debe devolverse una copia o una vista controlada.",
                "The client may mutate the container without public operations and violate invariants. Return a copy or controlled view instead.",
                "Klienten kan ændre containeren uden offentlige operationer og bryde invarianter. Returnér i stedet en kopi eller kontrolleret visning.",
            ),
            (
                "La privacidad por convención necesita apoyo del diseño.",
                "Privacy by convention needs design support.",
                "Privatliv efter konvention kræver designstøtte.",
            ),
        ),
        practice(
            "m11.p11",
            ActivityType.PIPELINE_DESIGN,
            (
                "Diseña una cola de trabajos cancelables.",
                "Design a cancellable job queue.",
                "Design en kø med annullerbare opgaver.",
            ),
            (
                (
                    "Combina prioridad con identidad estable.",
                    "Combine priority with stable identity.",
                    "Kombinér prioritet med stabil identitet.",
                ),
            ),
            (
                "Mantener heap de entradas y mapa job_id→estado; cancelar marca la entrada, pop descarta entradas canceladas hasta hallar una activa.",
                "Maintain a heap of entries and a job_id→state map; cancellation marks an entry, and pop skips cancelled entries until an active one is found.",
                "Bevar en heap af poster og et job_id→tilstand-map; annullering markerer posten, og pop springer annullerede poster over til en aktiv findes.",
            ),
            (
                "Actualizar in situ un heap arbitrario no es una operación directa de heapq.",
                "Arbitrary in-place heap update is not a direct heapq operation.",
                "Vilkårlig in-place-opdatering er ikke en direkte heapq-operation.",
            ),
        ),
        practice(
            "m11.p12",
            ActivityType.CODE_TRACING,
            (
                "Traza prioridades (2,A), (1,B), (1,C) con contador de llegada.",
                "Trace priorities (2,A), (1,B), (1,C) with an arrival counter.",
                "Gennemgå prioriteter (2,A), (1,B), (1,C) med ankomsttæller.",
            ),
            (
                (
                    "Menor prioridad numérica sale primero; el contador desempata.",
                    "Lower numeric priority leaves first; counter breaks ties.",
                    "Lavere numerisk prioritet kommer først; tælleren afgør lighed.",
                ),
            ),
            ("B, C, A", "B, C, A", "B, C, A"),
            (
                "B y C mantienen su orden de llegada.",
                "B and C preserve arrival order.",
                "B og C bevarer ankomstrækkefølgen.",
            ),
        ),
    ),
    assessment_items=(
        objective_mcq(
            "dm857.m11.assessment.001",
            (
                "¿Qué define principalmente un ADT?",
                "What primarily defines an ADT?",
                "Hvad definerer primært en ADT?",
            ),
            (
                (
                    "behavior",
                    ("Comportamiento observable", "Observable behavior", "Observerbar adfærd"),
                ),
                ("list", ("Una lista interna", "An internal list", "En intern liste")),
                (
                    "syntax",
                    (
                        "Un nombre de clase concreto",
                        "A concrete class name",
                        "Et konkret klassenavn",
                    ),
                ),
            ),
            "behavior",
            (
                "La abstracción se define por valores y operaciones.",
                "The abstraction is defined by values and operations.",
                "Abstraktionen defineres af værdier og operationer.",
            ),
        ),
        authored_item(
            "dm857.m11.assessment.002",
            ActivityType.MULTIPLE_SELECT,
            (
                "Selecciona componentes de un contrato.",
                "Select contract components.",
                "Vælg kontraktkomponenter.",
            ),
            (),
            (
                "Precondiciones, resultados, errores y efectos observables.",
                "Preconditions, results, errors, and observable effects.",
                "Forudsætninger, resultater, fejl og observerbare effekter.",
            ),
            options=(
                ("pre", ("Precondiciones", "Preconditions", "Forudsætninger")),
                ("result", ("Resultados", "Results", "Resultater")),
                ("errors", ("Errores", "Errors", "Fejl")),
                ("effects", ("Efectos", "Effects", "Effekter")),
                (
                    "private",
                    (
                        "Nombre del atributo privado",
                        "Private attribute name",
                        "Navn på privat attribut",
                    ),
                ),
            ),
            correct_option_ids=("pre", "result", "errors", "effects"),
        ),
        authored_item(
            "dm857.m11.assessment.003",
            ActivityType.CODE_TRACING,
            (
                "Traza una pila tras push A, push B, pop, push C.",
                "Trace a stack after push A, push B, pop, push C.",
                "Gennemgå en stak efter push A, push B, pop, push C.",
            ),
            (
                (
                    "Estado final [A,C]; pop devolvió B.",
                    "Final state [A,C]; pop returned B.",
                    "Sluttilstand [A,C]; pop returnerede B.",
                ),
            ),
            ("La pila aplica LIFO.", "The stack applies LIFO.", "Stakken anvender LIFO."),
        ),
        authored_item(
            "dm857.m11.assessment.004",
            ActivityType.FILL_IN_THE_BLANK,
            (
                "En deque, dequeue FIFO usa ____.",
                "In a deque, FIFO dequeue uses ____.",
                "I en deque bruger FIFO-dequeue ____.",
            ),
            (("popleft", "popleft", "popleft"),),
            (
                "El frente está a la izquierda.",
                "The front is on the left.",
                "Fronten er til venstre.",
            ),
        ),
        authored_item(
            "dm857.m11.assessment.005",
            ActivityType.MATCHING,
            (
                "Relaciona abstracción y operación.",
                "Match abstraction and operation.",
                "Match abstraktion og operation.",
            ),
            (),
            (
                "Pila-pop; cola-dequeue; mapa-lookup; conjunto-membership.",
                "Stack-pop; queue-dequeue; map-lookup; set-membership.",
                "Stak-pop; kø-dequeue; map-lookup; mængde-membership.",
            ),
            options=(
                ("stack", ("Pila → pop", "Stack → pop", "Stak → pop")),
                ("queue", ("Cola → dequeue", "Queue → dequeue", "Kø → dequeue")),
                ("map", ("Mapa → lookup", "Map → lookup", "Map → lookup")),
                ("set", ("Conjunto → membership", "Set → membership", "Mængde → membership")),
            ),
            correct_option_ids=("stack", "queue", "map", "set"),
        ),
        authored_item(
            "dm857.m11.assessment.006",
            ActivityType.ORDERING,
            (
                "Ordena la creación de un ADT fiable.",
                "Order reliable ADT construction.",
                "Sæt opbygningen af en pålidelig ADT i rækkefølge.",
            ),
            (),
            (
                "Definir contrato → elegir representación → formular invariante → implementar operaciones → probar comportamiento.",
                "Define contract → choose representation → state invariant → implement operations → test behavior.",
                "Definér kontrakt → vælg repræsentation → formulér invariant → implementér operationer → test adfærd.",
            ),
            options=(
                ("contract", ("Definir contrato", "Define contract", "Definér kontrakt")),
                (
                    "representation",
                    ("Elegir representación", "Choose representation", "Vælg repræsentation"),
                ),
                ("invariant", ("Formular invariante", "State invariant", "Formulér invariant")),
                ("implement", ("Implementar", "Implement", "Implementér")),
                ("test", ("Probar", "Test", "Test")),
            ),
            correct_option_ids=("contract", "representation", "invariant", "implement", "test"),
        ),
        authored_item(
            "dm857.m11.assessment.007",
            ActivityType.CODE_COMPLETION,
            (
                "Implementa peek para una pila que lanza IndexError al vacío.",
                "Implement peek for a stack that raises IndexError when empty.",
                "Implementér peek for en stak, der kaster IndexError, når den er tom.",
            ),
            (
                (
                    "def peek(self):\n    if not self._items:\n        raise IndexError('peek from empty stack')\n    return self._items[-1]",
                    "def peek(self):\n    if not self._items:\n        raise IndexError('peek from empty stack')\n    return self._items[-1]",
                    "def peek(self):\n    if not self._items:\n        raise IndexError('peek from empty stack')\n    return self._items[-1]",
                ),
            ),
            (
                "peek no elimina el elemento.",
                "peek does not remove the item.",
                "peek fjerner ikke elementet.",
            ),
            rubric=(("Conserva el estado.", "Preserves state.", "Bevarer tilstanden."),),
        ),
        authored_item(
            "dm857.m11.assessment.008",
            ActivityType.DEBUGGING,
            (
                "Una propiedad items devuelve la lista interna. Corrígela.",
                "An items property returns the internal list. Fix it.",
                "En items-egenskab returnerer den interne liste. Ret den.",
            ),
            (
                (
                    "Retornar tuple(self._items), una copia o un iterador que no permita mutación externa.",
                    "Return tuple(self._items), a copy, or an iterator that prevents external mutation.",
                    "Returnér tuple(self._items), en kopi eller en iterator, der forhindrer ekstern mutation.",
                ),
            ),
            (
                "La referencia mutable permite violar invariantes.",
                "The mutable reference permits invariant violations.",
                "Den muterbare reference gør det muligt at bryde invarianter.",
            ),
        ),
        authored_item(
            "dm857.m11.assessment.009",
            ActivityType.SHORT_ANSWER,
            (
                "Explica la propiedad push(x); pop() == x.",
                "Explain the property push(x); pop() == x.",
                "Forklar egenskaben push(x); pop() == x.",
            ),
            (
                (
                    "Si no intervienen otras operaciones, el último elemento insertado debe ser el siguiente extraído por LIFO.",
                    "If no other operations intervene, the last inserted item must be the next removed under LIFO.",
                    "Hvis ingen andre operationer griber ind, skal det sidst indsatte element være det næste, der fjernes under LIFO.",
                ),
            ),
            (
                "Es una prueba de contrato independiente de la representación.",
                "It is a representation-independent contract test.",
                "Det er en repræsentationsuafhængig kontrakttest.",
            ),
        ),
        authored_item(
            "dm857.m11.assessment.010",
            ActivityType.DATA_INTERPRETATION,
            (
                "Un dequeue tarda proporcionalmente al tamaño de la cola. Diagnostica la representación probable.",
                "A dequeue takes time proportional to queue size. Diagnose the likely representation.",
                "En dequeue tager tid proportionalt med køens størrelse. Diagnosticér den sandsynlige repræsentation.",
            ),
            (
                (
                    "Probablemente una lista con pop(0), que desplaza los elementos; usar deque.",
                    "Likely a list with pop(0), which shifts items; use deque.",
                    "Sandsynligvis en liste med pop(0), som flytter elementer; brug deque.",
                ),
            ),
            (
                "El contrato FIFO puede mantenerse con una representación ineficiente.",
                "The FIFO contract can be met by an inefficient representation.",
                "FIFO-kontrakten kan opfyldes af en ineffektiv repræsentation.",
            ),
        ),
        authored_item(
            "dm857.m11.assessment.011",
            ActivityType.PIPELINE_DESIGN,
            (
                "Diseña un planificador con prioridad y cancelación.",
                "Design a scheduler with priority and cancellation.",
                "Design en planlægger med prioritet og annullering.",
            ),
            (
                (
                    "Heap de entradas (prioridad, contador, id), mapa de estado por id y descarte perezoso de entradas canceladas.",
                    "Heap of (priority, counter, id) entries, a state map by id, and lazy skipping of cancelled entries.",
                    "Heap af poster (prioritet, tæller, id), et tilstandsmap efter id og doven springning over annullerede poster.",
                ),
            ),
            (
                "La composición preserva una interfaz simple.",
                "Composition preserves a simple interface.",
                "Komposition bevarer et enkelt interface.",
            ),
            rubric=(
                ("Usa identidad estable.", "Uses stable identity.", "Bruger stabil identitet."),
            ),
        ),
        authored_item(
            "dm857.m11.assessment.012",
            ActivityType.ORAL_EXPLANATION,
            (
                "Explica invariante frente a precondición.",
                "Explain invariant versus precondition.",
                "Forklar invariant versus forudsætning.",
            ),
            (
                (
                    "La precondición debe cumplirse antes de una operación concreta; la invariante describe el estado válido del objeto entre operaciones públicas.",
                    "A precondition must hold before one operation; an invariant describes valid object state between public operations.",
                    "En forudsætning skal gælde før en operation; en invariant beskriver gyldig objekttilstand mellem offentlige operationer.",
                ),
            ),
            (
                "Una operación puede validar ambas responsabilidades.",
                "An operation may validate both responsibilities.",
                "En operation kan validere begge ansvar.",
            ),
        ),
        authored_item(
            "dm857.m11.assessment.013",
            ActivityType.DEBUGGING,
            (
                "heapq falla al empatar prioridades de objetos no comparables. Corrige el diseño.",
                "heapq fails when priorities tie for non-comparable objects. Fix the design.",
                "heapq fejler ved ens prioriteter for ikke-sammenlignelige objekter. Ret designet.",
            ),
            (
                (
                    "Añadir un contador único entre prioridad y objeto.",
                    "Add a unique counter between priority and object.",
                    "Tilføj en unik tæller mellem prioritet og objekt.",
                ),
            ),
            (
                "La comparación termina antes de alcanzar el objeto.",
                "Comparison ends before reaching the object.",
                "Sammenligningen slutter før objektet nås.",
            ),
        ),
        authored_item(
            "dm857.m11.assessment.014",
            ActivityType.SHORT_ANSWER,
            (
                "Propón pruebas mínimas para un buffer acotado.",
                "Propose minimum tests for a bounded buffer.",
                "Foreslå minimale test for en begrænset buffer.",
            ),
            (
                (
                    "Capacidad inválida, vacío, una inserción, orden FIFO, exactamente lleno, inserción al lleno, extracción hasta vacío y aislamiento entre instancias.",
                    "Invalid capacity, empty, one insertion, FIFO order, exactly full, insertion when full, removal until empty, and instance isolation.",
                    "Ugyldig kapacitet, tom, én indsættelse, FIFO-rækkefølge, præcis fuld, indsættelse ved fuld, fjernelse til tom og isolation mellem instanser.",
                ),
            ),
            (
                "Los casos cubren contrato e invariante.",
                "The cases cover contract and invariant.",
                "Tilfældene dækker kontrakt og invariant.",
            ),
        ),
    ),
    tutor_support=tutor_support(
        (
            "Un tipo abstracto de datos se define por sus valores y operaciones observables. La interfaz nombra operaciones; el contrato define precondiciones, resultados, errores, efectos y, cuando importa, complejidad; la representación almacena el estado. Una invariante describe el estado interno válido y debe cumplirse después de la construcción y de cada operación pública. Una pila aplica LIFO con push, pop y peek; una cola aplica FIFO con enqueue y dequeue; una cola de prioridad entrega el elemento de prioridad extrema y suele implementarse con heapq. Los mapas asocian claves con valores y los conjuntos expresan pertenencia única. La composición permite construir abstracciones mayores, pero el contenedor interno mutable no debe exponerse. Las pruebas deben formularse contra el comportamiento, cubrir secuencias y errores, y permanecer válidas aunque cambie la representación. Los escenarios biomédicos son ejemplos de programación y no protocolos. La corrección de un ADT se evalúa mediante secuencias observables: construcción, consultas, mutaciones, errores y conservación del orden. Cada operación pública debe comprobar sus precondiciones, modificar el estado de forma controlada y restablecer la invariante antes de devolver el control. La elección de representación debe justificarse por las operaciones dominantes y por la complejidad prometida. Las pruebas no deben fijar atributos privados, sino demostrar propiedades como LIFO, FIFO, prioridad estable, aislamiento entre instancias y comportamiento definido en estados vacíos o llenos. Así una implementación puede cambiar sin alterar al cliente.",
            "An abstract data type is defined by its values and observable operations. The interface names operations; the contract defines preconditions, results, errors, effects, and when relevant complexity; the representation stores state. An invariant describes valid internal state and must hold after construction and every public operation. A stack applies LIFO with push, pop, and peek; a queue applies FIFO with enqueue and dequeue; a priority queue returns the extreme-priority item and is often implemented with heapq. Maps associate keys with values, and sets express unique membership. Composition builds larger abstractions, but mutable internal containers must not be exposed. Tests should target behavior, cover sequences and errors, and remain valid when representation changes. Biomedical scenarios are programming examples, not protocols. ADT correctness is evaluated through observable sequences: construction, queries, mutations, errors, and order preservation. Every public operation should check its preconditions, change state in a controlled way, and restore the invariant before returning control. The representation choice should be justified by dominant operations and promised complexity. Tests should not freeze private attributes; they should demonstrate properties such as LIFO, FIFO, stable priority, instance isolation, and defined behavior in empty or full states. This permits an implementation to change without altering client code.",
            "En abstrakt datatype defineres af værdier og observerbare operationer. Interfacet navngiver operationer; kontrakten definerer forudsætninger, resultater, fejl, effekter og eventuelt kompleksitet; repræsentationen lagrer tilstand. En invariant beskriver gyldig intern tilstand og skal gælde efter konstruktion og hver offentlig operation. En stak anvender LIFO med push, pop og peek; en kø anvender FIFO med enqueue og dequeue; en prioritetskø returnerer elementet med ekstrem prioritet og implementeres ofte med heapq. Maps forbinder nøgler med værdier, og mængder udtrykker unikt medlemskab. Komposition bygger større abstraktioner, men den muterbare interne container må ikke eksponeres. Test skal målrette adfærd, sekvenser og fejl og forblive gyldige ved ændret repræsentation. Biomedicinske scenarier er programmeringseksempler og ikke protokoller. Korrektheden af en ADT vurderes gennem observerbare sekvenser: konstruktion, forespørgsler, mutationer, fejl og bevarelse af rækkefølge. Hver offentlig operation bør kontrollere sine forudsætninger, ændre tilstanden kontrolleret og gendanne invarianten før retur. Valget af repræsentation bør begrundes med de dominerende operationer og den lovede kompleksitet. Test bør ikke fastlåse private attributter, men demonstrere egenskaber som LIFO, FIFO, stabil prioritet, isolation mellem instanser og defineret adfærd i tomme eller fulde tilstande. Dermed kan implementeringen ændres uden at ændre klientkoden.",
        ),
        (
            (
                "La interfaz y la representación son responsabilidades distintas.",
                "Interface and representation are distinct responsibilities.",
                "Interface og repræsentation er forskellige ansvar.",
            ),
            (
                "El contrato incluye errores esperados.",
                "The contract includes expected errors.",
                "Kontrakten inkluderer forventede fejl.",
            ),
            (
                "La invariante debe cumplirse entre operaciones públicas.",
                "The invariant must hold between public operations.",
                "Invarianten skal gælde mellem offentlige operationer.",
            ),
            ("Una pila es LIFO.", "A stack is LIFO.", "En stak er LIFO."),
            ("Una cola es FIFO.", "A queue is FIFO.", "En kø er FIFO."),
            (
                "deque implementa eficientemente ambos extremos.",
                "deque efficiently implements both ends.",
                "deque implementerer begge ender effektivt.",
            ),
            (
                "heapq mantiene un min-heap, no una lista ordenada.",
                "heapq maintains a min-heap, not a sorted list.",
                "heapq vedligeholder en min-heap, ikke en sorteret liste.",
            ),
            (
                "Un contador estable resuelve empates de prioridad.",
                "A stable counter resolves priority ties.",
                "En stabil tæller løser prioritetsligheder.",
            ),
            (
                "Mapas y conjuntos expresan intenciones de acceso distintas.",
                "Maps and sets express distinct access intentions.",
                "Maps og mængder udtrykker forskellige adgangsintentioner.",
            ),
            (
                "La composición reutiliza abstracciones existentes.",
                "Composition reuses existing abstractions.",
                "Komposition genbruger eksisterende abstraktioner.",
            ),
            (
                "Exponer una lista interna rompe encapsulación.",
                "Exposing an internal list breaks encapsulation.",
                "Eksponering af en intern liste bryder indkapsling.",
            ),
            (
                "Las pruebas deben observar el contrato.",
                "Tests should observe the contract.",
                "Test bør observere kontrakten.",
            ),
            (
                "Las secuencias de operaciones revelan errores de estado.",
                "Operation sequences reveal state errors.",
                "Operationssekvenser afslører tilstandsfejl.",
            ),
            (
                "La complejidad depende de la representación elegida.",
                "Complexity depends on the chosen representation.",
                "Kompleksitet afhænger af den valgte repræsentation.",
            ),
        ),
        (
            (
                "Definir un ADT por el nombre del atributo interno.",
                "Defining an ADT by its internal attribute name.",
                "At definere en ADT efter navnet på den interne attribut.",
            ),
            (
                "Considerar privada una lista que se devuelve directamente.",
                "Considering a directly returned list private.",
                "At betragte en direkte returneret liste som privat.",
            ),
            (
                "Usar pop(0) sin analizar coste.",
                "Using pop(0) without analyzing cost.",
                "At bruge pop(0) uden at analysere omkostning.",
            ),
            ("Confundir peek con pop.", "Confusing peek with pop.", "At forveksle peek med pop."),
            (
                "Devolver None al vacío sin documentarlo.",
                "Returning None on empty without documenting it.",
                "At returnere None ved tom uden dokumentation.",
            ),
            (
                "Suponer que heapq mantiene todo ordenado.",
                "Assuming heapq keeps everything sorted.",
                "At antage at heapq holder alt sorteret.",
            ),
            (
                "Ignorar empates de prioridad.",
                "Ignoring priority ties.",
                "At ignorere prioritetsligheder.",
            ),
            (
                "Probar atributos privados en lugar de comportamiento.",
                "Testing private attributes instead of behavior.",
                "At teste private attributter i stedet for adfærd.",
            ),
            (
                "No comprobar aislamiento entre instancias.",
                "Failing to test instance isolation.",
                "Ikke at teste isolation mellem instanser.",
            ),
            (
                "Usar assertions como validación de usuario.",
                "Using assertions as user validation.",
                "At bruge assertions som brugervalidering.",
            ),
            (
                "Mezclar contrato y detalle de implementación.",
                "Mixing contract and implementation detail.",
                "At blande kontrakt og implementeringsdetalje.",
            ),
            (
                "Elegir una lista para toda política de acceso.",
                "Choosing a list for every access policy.",
                "At vælge en liste til enhver adgangspolitik.",
            ),
        ),
        (
            (
                "¿Qué puede observar el cliente?",
                "What can the client observe?",
                "Hvad kan klienten observere?",
            ),
            (
                "¿Qué debe garantizar el contrato al vacío?",
                "What must the contract guarantee when empty?",
                "Hvad skal kontrakten garantere ved tom tilstand?",
            ),
            (
                "¿Cuál es la invariante de representación?",
                "What is the representation invariant?",
                "Hvad er repræsentationsinvarianten?",
            ),
            (
                "¿La política requerida es LIFO, FIFO o prioridad?",
                "Is the required policy LIFO, FIFO, or priority?",
                "Er den krævede politik LIFO, FIFO eller prioritet?",
            ),
            (
                "¿La operación consulta o modifica?",
                "Does the operation inspect or mutate?",
                "Læser eller muterer operationen?",
            ),
            (
                "¿Qué ocurre con prioridades iguales?",
                "What happens with equal priorities?",
                "Hvad sker der ved ens prioriteter?",
            ),
            (
                "¿Se expone una referencia mutable?",
                "Is a mutable reference exposed?",
                "Eksponeres en muterbar reference?",
            ),
            (
                "¿Podría cambiar la implementación sin cambiar al cliente?",
                "Could implementation change without changing the client?",
                "Kan implementeringen ændres uden at ændre klienten?",
            ),
            (
                "¿Qué secuencia mínima demuestra la propiedad?",
                "Which minimum sequence demonstrates the property?",
                "Hvilken minimal sekvens demonstrerer egenskaben?",
            ),
            (
                "¿La complejidad forma parte del requisito?",
                "Is complexity part of the requirement?",
                "Er kompleksitet en del af kravet?",
            ),
            (
                "¿Qué error específico comunica mejor la violación?",
                "Which specific error best communicates the violation?",
                "Hvilken specifik fejl kommunikerer overtrædelsen bedst?",
            ),
            (
                "¿Qué abstracciones pueden componerse?",
                "Which abstractions can be composed?",
                "Hvilke abstraktioner kan sammensættes?",
            ),
        ),
        (
            (
                "Distingue interfaz, contrato y representación.",
                "Distinguishes interface, contract, and representation.",
                "Skelner mellem interface, kontrakt og repræsentation.",
            ),
            (
                "Formula una invariante comprobable.",
                "States a checkable invariant.",
                "Formulerer en kontrollerbar invariant.",
            ),
            (
                "Respeta LIFO o FIFO según el contrato.",
                "Respects LIFO or FIFO according to the contract.",
                "Respekterer LIFO eller FIFO efter kontrakten.",
            ),
            (
                "Maneja estados vacíos y llenos.",
                "Handles empty and full states.",
                "Håndterer tomme og fulde tilstande.",
            ),
            (
                "Usa heapq con desempate seguro.",
                "Uses heapq with safe tie-breaking.",
                "Bruger heapq med sikker tie-breaking.",
            ),
            ("Preserva encapsulación.", "Preserves encapsulation.", "Bevarer indkapsling."),
            (
                "Selecciona la estructura adecuada.",
                "Selects the appropriate structure.",
                "Vælger den passende struktur.",
            ),
            (
                "Analiza la complejidad observable.",
                "Analyzes observable complexity.",
                "Analyserer observerbar kompleksitet.",
            ),
            (
                "Prueba secuencias y propiedades.",
                "Tests sequences and properties.",
                "Tester sekvenser og egenskaber.",
            ),
            (
                "Evita depender de atributos privados.",
                "Avoids dependence on private attributes.",
                "Undgår afhængighed af private attributter.",
            ),
        ),
        (
            (
                "No convertir ejemplos de planificación en decisiones clínicas.",
                "Do not turn scheduling examples into clinical decisions.",
                "Gør ikke planlægningseksempler til kliniske beslutninger.",
            ),
            (
                "Evaluar el comportamiento, no exigir una representación concreta salvo requisito explícito.",
                "Evaluate behavior, not a specific representation unless explicitly required.",
                "Vurdér adfærd, ikke en bestemt repræsentation medmindre krævet.",
            ),
            (
                "Definir la política de error antes de calificar.",
                "Define error policy before grading.",
                "Definér fejlpolitik før vurdering.",
            ),
            (
                "Diferenciar peek de pop.",
                "Differentiate peek from pop.",
                "Skeln mellem peek og pop.",
            ),
            (
                "No afirmar O(1) para list.pop(0).",
                "Do not claim O(1) for list.pop(0).",
                "Påstå ikke O(1) for list.pop(0).",
            ),
            ("Explicar los empates de heapq.", "Explain heapq ties.", "Forklar heapq-ligheder."),
            (
                "No recomendar exponer estado mutable.",
                "Do not recommend exposing mutable state.",
                "Anbefal ikke eksponering af muterbar tilstand.",
            ),
            (
                "Dar pistas antes de soluciones completas.",
                "Give hints before complete solutions.",
                "Giv ledetråde før komplette løsninger.",
            ),
            (
                "Mantenerse dentro del alcance de ADT y estructuras básicas.",
                "Stay within ADTs and basic structures.",
                "Hold dig inden for ADT'er og grundlæggende strukturer.",
            ),
        ),
        (
            "Guttag, Introduction to Computation and Programming Using Python, 3rd ed.",
            "Python documentation: collections.deque and heapq.",
            "Compeau and Pevzner, Bioinformatics Algorithms, 2nd ed., data-structure foundations.",
        ),
    ),
)

_OBJECTIVE_MCQS = (
    (
        "001",
        ("¿Qué define un ADT?", "What defines an ADT?", "Hvad definerer en ADT?"),
        (
            (
                "behavior",
                (
                    "Valores y operaciones observables",
                    "Values and observable operations",
                    "Værdier og observerbare operationer",
                ),
            ),
            (
                "attribute",
                (
                    "Un atributo privado concreto",
                    "One concrete private attribute",
                    "Én konkret privat attribut",
                ),
            ),
            (
                "library",
                ("Una biblioteca específica", "A specific library", "Et bestemt bibliotek"),
            ),
        ),
        "behavior",
        (
            "La abstracción se define por comportamiento.",
            "The abstraction is defined by behavior.",
            "Abstraktionen defineres af adfærd.",
        ),
    ),
    (
        "002",
        (
            "¿Qué política usa una pila?",
            "Which policy does a stack use?",
            "Hvilken politik bruger en stak?",
        ),
        (
            ("lifo", ("LIFO", "LIFO", "LIFO")),
            ("fifo", ("FIFO", "FIFO", "FIFO")),
            ("priority", ("Prioridad", "Priority", "Prioritet")),
        ),
        "lifo",
        (
            "El último elemento entra y sale primero.",
            "The last item enters and leaves first.",
            "Det sidste element ind og først ud.",
        ),
    ),
    (
        "003",
        (
            "¿Qué política usa una cola?",
            "Which policy does a queue use?",
            "Hvilken politik bruger en kø?",
        ),
        (
            ("fifo", ("FIFO", "FIFO", "FIFO")),
            ("lifo", ("LIFO", "LIFO", "LIFO")),
            ("random", ("Aleatoria", "Random", "Tilfældig")),
        ),
        "fifo",
        (
            "El primer elemento entra y sale primero.",
            "The first item enters and leaves first.",
            "Det første element ind og først ud.",
        ),
    ),
    (
        "004",
        (
            "¿Qué operación observa la cima sin eliminarla?",
            "Which operation inspects the top without removing it?",
            "Hvilken operation ser toppen uden at fjerne den?",
        ),
        (
            ("peek", ("peek", "peek", "peek")),
            ("pop", ("pop", "pop", "pop")),
            ("push", ("push", "push", "push")),
        ),
        "peek",
        ("peek conserva el estado.", "peek preserves state.", "peek bevarer tilstanden."),
    ),
    (
        "005",
        (
            "¿Qué implementación es adecuada para una cola Python?",
            "Which implementation suits a Python queue?",
            "Hvilken implementering passer til en Python-kø?",
        ),
        (
            ("deque", ("collections.deque", "collections.deque", "collections.deque")),
            ("list0", ("list con pop(0)", "list with pop(0)", "list med pop(0)")),
            ("set", ("set", "set", "set")),
        ),
        "deque",
        (
            "deque ofrece popleft amortizado constante.",
            "deque provides amortized constant popleft.",
            "deque giver amortiseret konstant popleft.",
        ),
    ),
    (
        "006",
        (
            "¿Qué estructura mantiene heapq?",
            "What structure does heapq maintain?",
            "Hvilken struktur vedligeholder heapq?",
        ),
        (
            ("minheap", ("Min-heap", "Min-heap", "Min-heap")),
            ("sorted", ("Lista totalmente ordenada", "Fully sorted list", "Fuldt sorteret liste")),
            ("maxheap", ("Siempre max-heap", "Always max-heap", "Altid max-heap")),
        ),
        "minheap",
        (
            "La raíz contiene el mínimo.",
            "The root contains the minimum.",
            "Roden indeholder minimum.",
        ),
    ),
    (
        "007",
        (
            "¿Qué campo evita comparar objetos empatados en heapq?",
            "Which field avoids comparing tied heapq objects?",
            "Hvilket felt undgår sammenligning af objekter med samme heapq-prioritet?",
        ),
        (
            ("counter", ("Contador único", "Unique counter", "Unik tæller")),
            ("none", ("None", "None", "None")),
            ("length", ("Longitud del objeto", "Object length", "Objektlængde")),
        ),
        "counter",
        (
            "El contador rompe el empate antes del objeto.",
            "The counter breaks the tie before the object.",
            "Tælleren afgør ligheden før objektet.",
        ),
    ),
    (
        "008",
        (
            "¿Qué describe una invariante?",
            "What does an invariant describe?",
            "Hvad beskriver en invariant?",
        ),
        (
            (
                "valid_state",
                ("Estado interno válido", "Valid internal state", "Gyldig intern tilstand"),
            ),
            (
                "one_call",
                ("Sólo una entrada de método", "Only one method input", "Kun ét metodeinput"),
            ),
            ("ui", ("El color de la interfaz", "The interface color", "Brugerfladens farve")),
        ),
        "valid_state",
        (
            "Debe cumplirse entre operaciones públicas.",
            "It must hold between public operations.",
            "Den skal gælde mellem offentlige operationer.",
        ),
    ),
    (
        "009",
        (
            "¿Qué debe ocurrir tras una operación mutadora?",
            "What must hold after a mutating operation?",
            "Hvad skal gælde efter en muterende operation?",
        ),
        (
            (
                "restore",
                ("Restablecer la invariante", "Restore the invariant", "Gendan invarianten"),
            ),
            ("expose", ("Exponer la lista", "Expose the list", "Eksponér listen")),
            ("sort", ("Ordenar siempre", "Always sort", "Sortér altid")),
        ),
        "restore",
        (
            "El objeto debe volver a un estado válido.",
            "The object must return to a valid state.",
            "Objektet skal vende tilbage til en gyldig tilstand.",
        ),
    ),
    (
        "010",
        (
            "¿Qué ADT expresa pertenencia sin duplicados?",
            "Which ADT expresses membership without duplicates?",
            "Hvilken ADT udtrykker medlemskab uden dubletter?",
        ),
        (
            ("set", ("Conjunto", "Set", "Mængde")),
            ("queue", ("Cola", "Queue", "Kø")),
            ("stack", ("Pila", "Stack", "Stak")),
        ),
        "set",
        (
            "El conjunto conserva elementos únicos.",
            "A set keeps unique elements.",
            "En mængde bevarer unikke elementer.",
        ),
    ),
    (
        "011",
        (
            "¿Qué ADT asocia claves con valores?",
            "Which ADT associates keys with values?",
            "Hvilken ADT forbinder nøgler med værdier?",
        ),
        (
            ("map", ("Mapa", "Map", "Map")),
            ("stack", ("Pila", "Stack", "Stak")),
            ("queue", ("Cola", "Queue", "Kø")),
        ),
        "map",
        (
            "Un mapa modela asociaciones clave-valor.",
            "A map models key-value associations.",
            "Et map modellerer nøgle-værdi-associationer.",
        ),
    ),
    (
        "012",
        ("¿Qué rompe encapsulación?", "What breaks encapsulation?", "Hvad bryder indkapsling?"),
        (
            (
                "mutable_ref",
                (
                    "Devolver la colección interna mutable",
                    "Returning the mutable internal collection",
                    "At returnere den muterbare interne samling",
                ),
            ),
            ("copy", ("Devolver una copia", "Returning a copy", "At returnere en kopi")),
            (
                "method",
                ("Usar un método público", "Using a public method", "At bruge en offentlig metode"),
            ),
        ),
        "mutable_ref",
        (
            "El cliente puede mutar sin control.",
            "The client can mutate without control.",
            "Klienten kan mutere uden kontrol.",
        ),
    ),
    (
        "013",
        (
            "¿Qué prueba es independiente de representación?",
            "Which test is representation-independent?",
            "Hvilken test er repræsentationsuafhængig?",
        ),
        (
            (
                "behavior",
                (
                    "push(x) seguido de pop devuelve x",
                    "push(x) followed by pop returns x",
                    "push(x) efterfulgt af pop returnerer x",
                ),
            ),
            ("attribute", ("self._items es list", "self._items is list", "self._items er list")),
            ("memory", ("La dirección de memoria", "The memory address", "Hukommelsesadressen")),
        ),
        "behavior",
        ("Prueba el contrato LIFO.", "It tests the LIFO contract.", "Det tester LIFO-kontrakten."),
    ),
    (
        "014",
        ("¿Qué coste tiene heappush?", "What is heappush cost?", "Hvad koster heappush?"),
        (
            ("log", ("O(log n)", "O(log n)", "O(log n)")),
            ("constant", ("O(1) siempre", "Always O(1)", "Altid O(1)")),
            ("quadratic", ("O(n²)", "O(n²)", "O(n²)")),
        ),
        "log",
        (
            "El elemento asciende por la altura del heap.",
            "The item rises along heap height.",
            "Elementet bevæger sig op gennem heapens højde.",
        ),
    ),
    (
        "015",
        (
            "¿Qué coste tiene consultar heap[0]?",
            "What is the cost of reading heap[0]?",
            "Hvad koster det at læse heap[0]?",
        ),
        (
            ("constant", ("O(1)", "O(1)", "O(1)")),
            ("log", ("O(log n)", "O(log n)", "O(log n)")),
            ("linear", ("O(n)", "O(n)", "O(n)")),
        ),
        "constant",
        ("El mínimo está en la raíz.", "The minimum is at the root.", "Minimum er ved roden."),
    ),
    (
        "016",
        (
            "¿Qué concepto permite cambiar lista por deque sin cambiar clientes?",
            "Which concept permits replacing a list with deque without changing clients?",
            "Hvilket koncept tillader at erstatte en liste med deque uden at ændre klienter?",
        ),
        (
            (
                "abstraction",
                ("Abstracción por contrato", "Contract abstraction", "Kontraktabstraktion"),
            ),
            ("inherit", ("Herencia obligatoria", "Mandatory inheritance", "Obligatorisk arv")),
            ("global", ("Estado global", "Global state", "Global tilstand")),
        ),
        "abstraction",
        (
            "El cliente depende de la interfaz.",
            "The client depends on the interface.",
            "Klienten afhænger af interfacet.",
        ),
    ),
    (
        "017",
        (
            "¿Qué estado debe probar una cola acotada?",
            "Which state must a bounded queue test?",
            "Hvilken tilstand skal en begrænset kø teste?",
        ),
        (
            ("full", ("Llena", "Full", "Fuld")),
            ("only_one", ("Sólo un elemento", "Only one item", "Kun ét element")),
            (
                "sorted",
                ("Ordenada alfabéticamente", "Alphabetically sorted", "Alfabetisk sorteret"),
            ),
        ),
        "full",
        (
            "La capacidad forma parte del contrato.",
            "Capacity belongs to the contract.",
            "Kapacitet hører til kontrakten.",
        ),
    ),
    (
        "018",
        (
            "¿Qué operación de pila elimina?",
            "Which stack operation removes?",
            "Hvilken stakoperation fjerner?",
        ),
        (
            ("pop", ("pop", "pop", "pop")),
            ("peek", ("peek", "peek", "peek")),
            ("len", ("len", "len", "len")),
        ),
        "pop",
        (
            "pop devuelve y elimina la cima.",
            "pop returns and removes the top.",
            "pop returnerer og fjerner toppen.",
        ),
    ),
    (
        "019",
        (
            "¿Qué composición sirve para historial undo/redo?",
            "Which composition supports undo/redo history?",
            "Hvilken komposition understøtter undo/redo-historik?",
        ),
        (
            ("two_stacks", ("Dos pilas", "Two stacks", "To stakke")),
            ("one_set", ("Un conjunto", "One set", "Én mængde")),
            ("one_heap", ("Un heap", "One heap", "Én heap")),
        ),
        "two_stacks",
        (
            "Una pila conserva undo y otra redo.",
            "One stack stores undo and another redo.",
            "Én stak gemmer undo og en anden redo.",
        ),
    ),
    (
        "020",
        (
            "¿Qué debe comprobar un método público al recibir entrada inválida?",
            "What should a public method do with invalid input?",
            "Hvad bør en offentlig metode gøre ved ugyldigt input?",
        ),
        (
            (
                "validate",
                (
                    "Validar y aplicar el contrato de error",
                    "Validate and apply the error contract",
                    "Validér og anvend fejlkontrakten",
                ),
            ),
            (
                "assert_only",
                ("Confiar sólo en assert", "Rely only on assert", "Stol kun på assert"),
            ),
            ("ignore", ("Ignorarla", "Ignore it", "Ignorér den")),
        ),
        "validate",
        (
            "La validación externa no debe depender de assert.",
            "External validation should not depend on assert.",
            "Ekstern validering bør ikke afhænge af assert.",
        ),
    ),
)

_OBJECTIVE_TFS = (
    (
        "021",
        (
            "Dos implementaciones pueden cumplir el mismo ADT.",
            "Two implementations can satisfy the same ADT.",
            "To implementeringer kan opfylde samme ADT.",
        ),
        True,
        (
            "La equivalencia depende del comportamiento observable.",
            "Equivalence depends on observable behavior.",
            "Ækvivalens afhænger af observerbar adfærd.",
        ),
    ),
    (
        "022",
        ("peek debe eliminar la cima.", "peek must remove the top.", "peek skal fjerne toppen."),
        False,
        ("peek sólo consulta.", "peek only inspects.", "peek læser kun."),
    ),
    (
        "023",
        (
            "Una cola FIFO puede implementarse eficientemente con deque.",
            "A FIFO queue can be efficiently implemented with deque.",
            "En FIFO-kø kan implementeres effektivt med deque.",
        ),
        True,
        (
            "append y popleft son apropiados.",
            "append and popleft are appropriate.",
            "append og popleft er passende.",
        ),
    ),
    (
        "024",
        (
            "list.pop(0) es amortizado O(1).",
            "list.pop(0) is amortized O(1).",
            "list.pop(0) er amortiseret O(1).",
        ),
        False,
        (
            "Desplaza los elementos restantes.",
            "It shifts remaining elements.",
            "Den flytter de resterende elementer.",
        ),
    ),
    (
        "025",
        (
            "heapq conserva una lista completamente ordenada.",
            "heapq keeps a fully sorted list.",
            "heapq holder en fuldt sorteret liste.",
        ),
        False,
        (
            "Sólo conserva la propiedad de heap.",
            "It only preserves the heap property.",
            "Den bevarer kun heap-egenskaben.",
        ),
    ),
    (
        "026",
        (
            "Una invariante puede comprobarse después de cada mutación pública.",
            "An invariant can be checked after each public mutation.",
            "En invariant kan kontrolleres efter hver offentlig mutation.",
        ),
        True,
        (
            "Debe cumplirse al devolver control.",
            "It must hold when control returns.",
            "Den skal gælde ved retur.",
        ),
    ),
    (
        "027",
        (
            "Devolver una copia puede proteger encapsulación.",
            "Returning a copy can protect encapsulation.",
            "At returnere en kopi kan beskytte indkapsling.",
        ),
        True,
        (
            "El cliente no obtiene la referencia original.",
            "The client does not obtain the original reference.",
            "Klienten får ikke den oprindelige reference.",
        ),
    ),
    (
        "028",
        (
            "Las pruebas de ADT deben exigir siempre una lista interna.",
            "ADT tests must always require an internal list.",
            "ADT-test skal altid kræve en intern liste.",
        ),
        False,
        (
            "Deben probar comportamiento salvo requisito explícito.",
            "They should test behavior unless explicitly required.",
            "De bør teste adfærd medmindre andet kræves.",
        ),
    ),
    (
        "029",
        (
            "Un conjunto expresa pertenencia sin duplicados.",
            "A set expresses membership without duplicates.",
            "En mængde udtrykker medlemskab uden dubletter.",
        ),
        True,
        ("Es su semántica principal.", "That is its main semantics.", "Det er dens hovedsemantik."),
    ),
    (
        "030",
        (
            "Las prioridades empatadas pueden requerir un contador estable.",
            "Tied priorities may require a stable counter.",
            "Ens prioriteter kan kræve en stabil tæller.",
        ),
        True,
        (
            "Evita comparar objetos no ordenables.",
            "It avoids comparing non-orderable objects.",
            "Det undgår sammenligning af ikke-ordnede objekter.",
        ),
    ),
)

LOCALIZED_OBJECTIVE_QUESTION_BANK_11 = tuple(
    objective_mcq(f"dm857.m11.bank.{suffix}", prompt, options, correct_option_id, explanation)
    for suffix, prompt, options, correct_option_id, explanation in _OBJECTIVE_MCQS
) + tuple(
    objective_tf(
        f"dm857.m11.bank.{suffix}",
        prompt,
        correct=correct,
        explanation=explanation,
    )
    for suffix, prompt, correct, explanation in _OBJECTIVE_TFS
)


def materialize_module_11_question_bank(
    locale: AppLocale | str = AppLocale.SPANISH_SPAIN,
) -> tuple[AssessmentItem, ...]:
    """Materialize the stable objective bank in one supported locale."""
    resolved = locale if isinstance(locale, AppLocale) else AppLocale.resolve(locale)
    return tuple(item.materialize(resolved) for item in LOCALIZED_OBJECTIVE_QUESTION_BANK_11)


MODULE_11_ADTS: LearningModule = LOCALIZED_MODULE_11_ADTS.materialize(AppLocale.SPANISH_SPAIN)
OBJECTIVE_QUESTION_BANK_11 = materialize_module_11_question_bank()

__all__ = [
    "LOCALIZED_MODULE_11_ADTS",
    "LOCALIZED_OBJECTIVE_QUESTION_BANK_11",
    "MODULE_11_ADTS",
    "OBJECTIVE_QUESTION_BANK_11",
    "materialize_module_11_question_bank",
]
