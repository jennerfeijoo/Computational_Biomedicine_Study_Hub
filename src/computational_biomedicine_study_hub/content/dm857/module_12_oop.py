"""DM857 module 12: classes, objects, composition, and object testing."""

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

LOCALIZED_MODULE_12_OOP = LocalizedLearningModule(
    course_code="DM857",
    module_id="dm857.m12",
    title=t(
        "Clases, objetos y diseño orientado a objetos",
        "Classes, objects, and object-oriented design",
        "Klasser, objekter og objektorienteret design",
    ),
    summary=t(
        "Este módulo introduce clases e instancias como una forma de combinar estado y comportamiento. Cubre construcción, atributos, métodos, identidad, igualdad, encapsulación, propiedades, dataclasses, métodos especiales, composición, herencia limitada, polimorfismo, errores de estado compartido y pruebas de objetos.",
        "This module introduces classes and instances as a way to combine state and behavior. It covers construction, attributes, methods, identity, equality, encapsulation, properties, dataclasses, special methods, composition, limited inheritance, polymorphism, shared-state errors, and object testing.",
        "Dette modul introducerer klasser og instanser som en måde at kombinere tilstand og adfærd. Det dækker konstruktion, attributter, metoder, identitet, lighed, indkapsling, properties, dataclasses, særlige metoder, komposition, begrænset arv, polymorfi, fejl med delt tilstand og objekttest.",
    ),
    objectives=(
        objective("m12.o1", ("Distinguir clase, instancia, atributo y método.", "Distinguish class, instance, attribute, and method.", "Skelne mellem klasse, instans, attribut og metode.")),
        objective("m12.o2", ("Construir objetos válidos mediante __init__.", "Construct valid objects through __init__.", "Konstruere gyldige objekter gennem __init__.")),
        objective("m12.o3", ("Diferenciar identidad, igualdad y representación.", "Differentiate identity, equality, and representation.", "Skelne mellem identitet, lighed og repræsentation.")),
        objective("m12.o4", ("Proteger invariantes con encapsulación y propiedades.", "Protect invariants with encapsulation and properties.", "Beskytte invarianter med indkapsling og properties.")),
        objective("m12.o5", ("Usar dataclasses para modelos de datos apropiados.", "Use dataclasses for appropriate data models.", "Bruge dataclasses til passende datamodeller.")),
        objective("m12.o6", ("Implementar métodos especiales con contratos coherentes.", "Implement special methods with coherent contracts.", "Implementere særlige metoder med konsistente kontrakter.")),
        objective("m12.o7", ("Preferir composición y justificar la herencia cuando corresponda.", "Prefer composition and justify inheritance when appropriate.", "Foretrække komposition og begrunde arv, når det er passende.")),
        objective("m12.o8", ("Diseñar pruebas de estado, comportamiento e independencia entre objetos.", "Design state, behavior, and object-independence tests.", "Designe test af tilstand, adfærd og uafhængighed mellem objekter.")),
    ),
    concepts=(
        concept(
            "classes-and-instances",
            ("Clases, instancias y espacio de nombres", "Classes, instances, and namespaces", "Klasser, instanser og namespaces"),
            (
                "Una clase define una familia de objetos y el comportamiento compartido; una instancia contiene identidad y estado propios. Acceder a obj.method produce un método enlazado que pasa obj como self. Los atributos de instancia suelen almacenarse en obj.__dict__, mientras los atributos de clase pertenecen a la clase y pueden compartirse. La resolución busca primero en la instancia y después en la clase, por lo que asignar un atributo homónimo en la instancia puede ocultar el de clase.",
                "A class defines a family of objects and shared behavior; an instance has its own identity and state. Accessing obj.method creates a bound method that passes obj as self. Instance attributes are commonly stored in obj.__dict__, while class attributes belong to the class and may be shared. Lookup searches the instance before the class, so assigning the same name on an instance may shadow the class attribute.",
                "En klasse definerer en familie af objekter og delt adfærd; en instans har egen identitet og tilstand. Adgang til obj.method opretter en bundet metode, der sender obj som self. Instansattributter lagres ofte i obj.__dict__, mens klasseattributter tilhører klassen og kan deles. Opslag søger først i instansen og derefter i klassen.",
            ),
            (
                ("self referencia la instancia receptora.", "self references the receiving instance.", "self refererer til den modtagende instans."),
                ("Cada instancia puede tener estado independiente.", "Each instance may have independent state.", "Hver instans kan have uafhængig tilstand."),
                ("Los atributos de clase pueden compartirse accidentalmente.", "Class attributes may be shared accidentally.", "Klasseattributter kan deles ved en fejl."),
            ),
        ),
        concept(
            "construction-and-invariants",
            ("Construcción e invariantes", "Construction and invariants", "Konstruktion og invarianter"),
            (
                "__init__ inicializa una instancia ya creada y debe dejarla en un estado válido. Conviene validar entradas antes de asignar parcialmente el estado, normalizar valores cuando el contrato lo requiera y evitar que el objeto exista públicamente con invariantes rotas. Los parámetros predeterminados mutables, como [], se crean una sola vez y pueden compartir estado entre instancias; se utiliza None y se crea una nueva colección dentro de __init__.",
                "__init__ initializes an already created instance and should leave it in a valid state. Validate inputs before partially assigning state, normalize values when required by the contract, and avoid exposing objects with broken invariants. Mutable default parameters such as [] are created once and may share state between instances; use None and create a fresh collection inside __init__.",
                "__init__ initialiserer en allerede oprettet instans og bør efterlade den i en gyldig tilstand. Validér input før delvis tildeling, normalisér værdier efter kontrakten, og undgå objekter med brudte invarianter. Muterbare standardparametre som [] oprettes én gang og kan dele tilstand; brug None og opret en ny samling i __init__.",
            ),
            (
                ("__init__ no debe retornar un valor distinto de None.", "__init__ must not return a value other than None.", "__init__ må ikke returnere en værdi forskellig fra None."),
                ("La validación debe preceder a la exposición del objeto.", "Validation should precede object exposure.", "Validering bør gå forud for eksponering af objektet."),
                ("Cada instancia necesita sus propias colecciones mutables.", "Each instance needs its own mutable collections.", "Hver instans har brug for egne muterbare samlinger."),
            ),
        ),
        concept(
            "identity-equality-representation",
            ("Identidad, igualdad y representación", "Identity, equality, and representation", "Identitet, lighed og repræsentation"),
            (
                "El operador is compara identidad: si dos referencias apuntan al mismo objeto. == invoca una noción de igualdad, normalmente __eq__. Dos objetos distintos pueden ser iguales por valor. __repr__ debería producir una representación inequívoca y útil para depuración; __str__ puede ofrecer una forma más legible para usuarios. Definir igualdad exige decidir qué atributos forman la identidad lógica y cómo tratar tipos diferentes. Si un objeto mutable define igualdad, hacerlo hashable puede ser inseguro.",
                "The is operator compares identity: whether references point to the same object. == invokes a notion of equality, usually __eq__. Distinct objects may be value-equal. __repr__ should provide an unambiguous debugging representation; __str__ may provide a user-friendly form. Defining equality requires deciding which attributes form logical identity and how different types are handled. Making a mutable value-equal object hashable may be unsafe.",
                "Operatoren is sammenligner identitet: om referencer peger på samme objekt. == bruger en lighedsdefinition, normalt __eq__. Forskellige objekter kan være værdimæssigt ens. __repr__ bør give en entydig repræsentation til fejlfinding; __str__ kan være mere brugervenlig. Lighed kræver valg af logisk identitet og håndtering af forskellige typer. Muterbare værdilighedsobjekter bør ikke uden videre være hashbare.",
            ),
            (
                ("is no sustituye a == para comparar valores.", "is does not replace == for value comparison.", "is erstatter ikke == ved værdisammenligning."),
                ("__repr__ debe ayudar a identificar estado relevante.", "__repr__ should expose relevant state for debugging.", "__repr__ bør vise relevant tilstand til fejlfinding."),
                ("Igualdad y hash deben ser coherentes.", "Equality and hashing must be coherent.", "Lighed og hash skal være konsistente."),
            ),
        ),
        concept(
            "encapsulation-properties",
            ("Encapsulación y propiedades", "Encapsulation and properties", "Indkapsling og properties"),
            (
                "Python utiliza convenciones más que privacidad absoluta. Un atributo _value comunica uso interno; una property permite conservar una sintaxis de atributo mientras ejecuta validación o cálculo. Un setter debe preservar invariantes y evitar efectos inesperados. No toda variable necesita una property: añadir acceso indirecto sin una regla concreta aumenta complejidad. Una propiedad calculada no debería parecer barata si realiza trabajo costoso o E/S.",
                "Python relies more on conventions than absolute privacy. An _value attribute communicates internal use; a property preserves attribute syntax while executing validation or computation. A setter must preserve invariants and avoid surprising effects. Not every variable needs a property: indirect access without a concrete rule adds complexity. A computed property should not appear cheap if it performs expensive work or I/O.",
                "Python bruger mere konventioner end absolut privatliv. En _value-attribut signalerer intern brug; en property bevarer attributsyntaks, mens den udfører validering eller beregning. En setter skal bevare invarianter og undgå overraskende effekter. Ikke alle variable behøver en property; indirekte adgang uden en konkret regel øger kompleksiteten.",
            ),
            (
                ("Una property protege una regla, no sólo oculta un nombre.", "A property protects a rule, not merely a name.", "En property beskytter en regel, ikke blot et navn."),
                ("Los setters deben validar antes de modificar.", "Setters should validate before mutating.", "Settere bør validere før mutation."),
                ("Las operaciones costosas suelen merecer métodos explícitos.", "Expensive operations often deserve explicit methods.", "Dyre operationer fortjener ofte eksplicitte metoder."),
            ),
        ),
        concept(
            "dataclasses",
            ("Dataclasses y modelos de datos", "Dataclasses and data models", "Dataclasses og datamodeller"),
            (
                "@dataclass genera __init__, __repr__ y __eq__ a partir de campos declarados. Es apropiado para objetos cuyo propósito principal es almacenar datos con invariantes moderadas. field(default_factory=list) crea una colección nueva por instancia. frozen=True limita la reasignación y favorece modelos de valor, aunque no vuelve inmutables los objetos anidados. __post_init__ permite validar después del inicializador generado. Una dataclass no sustituye un diseño de dominio cuando existen procesos complejos o control fino de estado.",
                "@dataclass generates __init__, __repr__, and __eq__ from declared fields. It suits objects primarily storing data with moderate invariants. field(default_factory=list) creates a fresh collection per instance. frozen=True limits reassignment and supports value models, though nested objects remain potentially mutable. __post_init__ permits validation after the generated initializer. A dataclass does not replace domain design when complex processes or fine state control are required.",
                "@dataclass genererer __init__, __repr__ og __eq__ fra deklarerede felter. Den passer til objekter, der primært lagrer data med moderate invarianter. field(default_factory=list) opretter en ny samling pr. instans. frozen=True begrænser omtildeling og støtter værdimodeller, men indlejrede objekter kan stadig være muterbare. __post_init__ muliggør validering efter den genererede initialisering.",
            ),
            (
                ("default_factory evita estado compartido.", "default_factory avoids shared state.", "default_factory undgår delt tilstand."),
                ("frozen no congela recursivamente.", "frozen does not recursively freeze.", "frozen fryser ikke rekursivt."),
                ("__post_init__ puede validar campos relacionados.", "__post_init__ can validate related fields.", "__post_init__ kan validere relaterede felter."),
            ),
        ),
        concept(
            "special-methods",
            ("Métodos especiales y protocolos", "Special methods and protocols", "Særlige metoder og protokoller"),
            (
                "Los métodos especiales integran objetos con protocolos de Python. __len__ debe retornar un entero no negativo; __iter__ devuelve un iterador; __contains__ implementa in; __eq__ define igualdad; __repr__ apoya depuración. Implementarlos implica respetar expectativas generales, no sólo hacer que una prueba pase. Un contenedor con __iter__ puede participar en for y comprensiones sin exponer su lista interna. Sobrecargar operadores debe conservar significado claro y predecible.",
                "Special methods integrate objects with Python protocols. __len__ must return a non-negative integer; __iter__ returns an iterator; __contains__ implements in; __eq__ defines equality; __repr__ supports debugging. Implementing them means respecting general expectations, not merely passing one test. A container with __iter__ can participate in for loops and comprehensions without exposing its internal list. Operator overloading should remain clear and predictable.",
                "Særlige metoder integrerer objekter med Python-protokoller. __len__ skal returnere et ikke-negativt heltal; __iter__ returnerer en iterator; __contains__ implementerer in; __eq__ definerer lighed; __repr__ støtter fejlfinding. Implementeringen skal respektere generelle forventninger. En container med __iter__ kan bruges i for-løkker uden at eksponere sin interne liste.",
            ),
            (
                ("Los protocolos permiten polimorfismo por comportamiento.", "Protocols enable behavior-based polymorphism.", "Protokoller muliggør adfærdsbaseret polymorfi."),
                ("__len__ no debe tener efectos secundarios.", "__len__ should not have side effects.", "__len__ bør ikke have sideeffekter."),
                ("__iter__ puede proteger la representación interna.", "__iter__ can protect internal representation.", "__iter__ kan beskytte den interne repræsentation."),
            ),
        ),
        concept(
            "composition-inheritance-polymorphism",
            ("Composición, herencia y polimorfismo", "Composition, inheritance, and polymorphism", "Komposition, arv og polymorfi"),
            (
                "La composición modela una relación tiene-un: un StudyPlan tiene módulos. La herencia modela es-un y debe mantener el contrato de la clase base. Se prefiere composición cuando sólo se reutiliza una parte del comportamiento o cuando las variantes necesitan componentes intercambiables. El polimorfismo permite usar objetos distintos que ofrecen el mismo protocolo, sin exigir siempre una jerarquía de herencia. Herencias profundas aumentan acoplamiento y dificultan razonar sobre estado.",
                "Composition models a has-a relation: a StudyPlan has modules. Inheritance models is-a and must preserve the base-class contract. Prefer composition when only part of behavior is reused or variants need interchangeable components. Polymorphism permits using different objects that provide the same protocol without always requiring an inheritance hierarchy. Deep inheritance increases coupling and makes state harder to reason about.",
                "Komposition modellerer en har-en-relation: en StudyPlan har moduler. Arv modellerer er-en og skal bevare basisklassens kontrakt. Foretræk komposition, når kun en del af adfærden genbruges, eller varianter kræver udskiftelige komponenter. Polymorfi tillader forskellige objekter med samme protokol uden nødvendigvis arv. Dyb arv øger kobling.",
            ),
            (
                ("Composición suele reducir acoplamiento.", "Composition often reduces coupling.", "Komposition reducerer ofte kobling."),
                ("Una subclase debe poder sustituir a la base.", "A subclass should substitute for the base.", "En underklasse bør kunne erstatte basisklassen."),
                ("Compartir protocolo no exige herencia.", "Sharing a protocol does not require inheritance.", "En fælles protokol kræver ikke arv."),
            ),
        ),
        concept(
            "object-testing-design",
            ("Diseño y pruebas de objetos", "Object design and testing", "Objektdesign og test"),
            (
                "Las pruebas deben cubrir construcción válida e inválida, transiciones de estado, métodos que consultan, invariantes después de mutaciones, igualdad, representación y aislamiento entre instancias. No deben depender de atributos privados salvo que el contrato los exponga. Las pruebas de aliasing detectan colecciones compartidas accidentalmente. Diseñar una clase también exige decidir responsabilidades: una clase pequeña con una razón clara para cambiar suele ser más mantenible que un objeto que carga datos, E/S, análisis y presentación simultáneamente.",
                "Tests should cover valid and invalid construction, state transitions, query methods, invariants after mutations, equality, representation, and isolation between instances. They should not depend on private attributes unless the contract exposes them. Aliasing tests detect accidentally shared collections. Class design also requires choosing responsibilities: a small class with one clear reason to change is often more maintainable than an object that combines data, I/O, analysis, and presentation.",
                "Test bør dække gyldig og ugyldig konstruktion, tilstandsovergange, forespørgselsmetoder, invarianter efter mutation, lighed, repræsentation og isolation mellem instanser. De bør ikke afhænge af private attributter, medmindre kontrakten eksponerer dem. Aliasing-test opdager utilsigtet delte samlinger. En lille klasse med ét tydeligt ansvar er ofte mere vedligeholdelig end et objekt, der kombinerer data, I/O, analyse og præsentation.",
            ),
            (
                ("Prueba objetos independientes.", "Test independent objects.", "Test uafhængige objekter."),
                ("Prueba secuencias de estado.", "Test state sequences.", "Test tilstandssekvenser."),
                ("Mantén responsabilidades cohesionadas.", "Keep responsibilities cohesive.", "Hold ansvar sammenhængende."),
            ),
        ),
    ),
    worked_examples=(
        example(
            "validated-counter",
            ("Contador con estado encapsulado", "Counter with encapsulated state", "Tæller med indkapslet tilstand"),
            ("Mantén un entero no negativo y evita decrementos inválidos.", "Maintain a non-negative integer and prevent invalid decrements.", "Bevar et ikke-negativt heltal og forhindr ugyldige decrementer."),
            (("Validar el valor inicial.", "Validate the initial value.", "Validér startværdien."), ("Proteger la invariante antes de decrementar.", "Protect the invariant before decrementing.", "Beskyt invarianten før decrement.")),
            "class Counter:\n    def __init__(self, initial=0):\n        if initial < 0:\n            raise ValueError('initial must be non-negative')\n        self._value = initial\n\n    @property\n    def value(self):\n        return self._value\n\n    def increment(self):\n        self._value += 1\n\n    def decrement(self):\n        if self._value == 0:\n            raise ValueError('counter cannot become negative')\n        self._value -= 1\n\nc = Counter(1); c.decrement(); print(c.value)",
            "0",
            ("Todas las operaciones públicas preservan value >= 0.", "All public operations preserve value >= 0.", "Alle offentlige operationer bevarer value >= 0."),
        ),
        example(
            "sample-dataclass",
            ("Modelo de muestra con dataclass", "Sample model with a dataclass", "Prøvemodel med dataclass"),
            ("Representa un identificador y valores numéricos con validación básica.", "Represent an identifier and numeric values with basic validation.", "Repræsentér et ID og numeriske værdier med grundlæggende validering."),
            (("Usar default_factory para la lista.", "Use default_factory for the list.", "Brug default_factory til listen."), ("Validar ID y valores en __post_init__.", "Validate ID and values in __post_init__.", "Validér ID og værdier i __post_init__.")),
            "from dataclasses import dataclass, field\n\n@dataclass\nclass Sample:\n    sample_id: str\n    values: list[float] = field(default_factory=list)\n\n    def __post_init__(self):\n        if not self.sample_id.strip():\n            raise ValueError('sample_id cannot be blank')\n        if any(value < 0 for value in self.values):\n            raise ValueError('values must be non-negative')\n\na = Sample('S1'); b = Sample('S2'); a.values.append(2.0); print(a.values, b.values)",
            "[2.0] []",
            ("Cada instancia recibe una lista independiente.", "Each instance receives an independent list.", "Hver instans får en uafhængig liste."),
        ),
        example(
            "temperature-property",
            ("Propiedad con validación", "Property with validation", "Property med validering"),
            ("Protege una temperatura absoluta no negativa.", "Protect a non-negative absolute temperature.", "Beskyt en ikke-negativ absolut temperatur."),
            (("Guardar el valor en _kelvin.", "Store the value in _kelvin.", "Gem værdien i _kelvin."), ("Validar tanto en construcción como en setter.", "Validate in construction and setter.", "Validér både i konstruktion og setter.")),
            "class Temperature:\n    def __init__(self, kelvin):\n        self.kelvin = kelvin\n\n    @property\n    def kelvin(self):\n        return self._kelvin\n\n    @kelvin.setter\n    def kelvin(self, value):\n        if value < 0:\n            raise ValueError('kelvin must be non-negative')\n        self._kelvin = float(value)\n\nt = Temperature(273.15); print(t.kelvin)",
            "273.15",
            ("Todas las asignaciones pasan por la misma regla.", "All assignments pass through the same rule.", "Alle tildelinger går gennem samme regel."),
        ),
        example(
            "iterable-collection",
            ("Colección iterable sin exponer la lista", "Iterable collection without exposing the list", "Iterérbar samling uden at eksponere listen"),
            ("Permite len, in y for sobre una colección interna.", "Permit len, in, and for over an internal collection.", "Tillad len, in og for over en intern samling."),
            (("Implementar protocolos de consulta.", "Implement query protocols.", "Implementér forespørgselsprotokoller."), ("Devolver iterador, no la lista para mutación.", "Return an iterator, not the list for mutation.", "Returnér iterator, ikke listen til mutation.")),
            "class CourseCodes:\n    def __init__(self, codes=()):\n        self._codes = list(codes)\n\n    def __len__(self):\n        return len(self._codes)\n\n    def __contains__(self, code):\n        return code in self._codes\n\n    def __iter__(self):\n        return iter(tuple(self._codes))\n\ncodes = CourseCodes(['DM857', 'DM847']); print(len(codes), 'DM857' in codes, list(codes))",
            "2 True ['DM857', 'DM847']",
            ("El objeto participa en protocolos sin entregar su lista interna.", "The object participates in protocols without giving away its internal list.", "Objektet deltager i protokoller uden at udlevere sin interne liste."),
        ),
        example(
            "composition",
            ("Composición de un plan de estudio", "Composition of a study plan", "Komposition af en studieplan"),
            ("Un plan contiene módulos y delega su progreso.", "A plan contains modules and delegates progress.", "En plan indeholder moduler og delegerer fremskridt."),
            (("Modelar ModuleProgress como objeto independiente.", "Model ModuleProgress as an independent object.", "Modellér ModuleProgress som et uafhængigt objekt."), ("Componer una lista de objetos.", "Compose a list of objects.", "Sammensæt en liste af objekter.")),
            "from dataclasses import dataclass\n\n@dataclass\nclass ModuleProgress:\n    module_id: str\n    completed: bool = False\n\nclass StudyPlan:\n    def __init__(self, modules):\n        self._modules = list(modules)\n\n    def completed_count(self):\n        return sum(module.completed for module in self._modules)\n\nplan = StudyPlan([ModuleProgress('m1', True), ModuleProgress('m2')])\nprint(plan.completed_count())",
            "1",
            ("StudyPlan tiene objetos ModuleProgress; no es un tipo de módulo.", "StudyPlan has ModuleProgress objects; it is not a kind of module.", "StudyPlan har ModuleProgress-objekter; den er ikke en type modul."),
        ),
    ),
    practice_exercises=(
        practice("m12.p01", ActivityType.CODE_TRACING, ("Traza dos instancias Counter y demuestra que sus valores son independientes.", "Trace two Counter instances and show that their values are independent.", "Gennemgå to Counter-instanser og vis at deres værdier er uafhængige."), (("Cada __init__ asigna self._value en un objeto distinto.", "Each __init__ assigns self._value on a different object.", "Hver __init__ tildeler self._value på et forskelligt objekt."),), ("Incrementar a no modifica b; cada instancia conserva su propio estado.", "Incrementing a does not change b; each instance keeps its own state.", "Incrementering af a ændrer ikke b; hver instans bevarer egen tilstand."), ("La independencia debe probarse explícitamente.", "Independence should be tested explicitly.", "Uafhængighed bør testes eksplicit.")),
        practice("m12.p02", ActivityType.FILL_IN_THE_BLANK, ("Completa una lista segura en dataclass: values: list = field(____=list).", "Complete a safe dataclass list: values: list = field(____=list).", "Udfyld en sikker dataclass-liste: values: list = field(____=list)."), (("Necesitas una fábrica por instancia.", "You need a factory per instance.", "Du behøver en fabrik pr. instans."),), ("default_factory", "default_factory", "default_factory"), ("La fábrica crea una lista nueva para cada objeto.", "The factory creates a fresh list for each object.", "Fabrikken opretter en ny liste for hvert objekt.")),
        practice("m12.p03", ActivityType.DEBUGGING, ("Corrige __init__(self, items=[]).", "Fix __init__(self, items=[]).", "Ret __init__(self, items=[])."), (("El objeto predeterminado se crea una sola vez.", "The default object is created once.", "Standardobjektet oprettes én gang."),), ("Usar items=None y dentro self._items = [] if items is None else list(items).", "Use items=None and inside set self._items = [] if items is None else list(items).", "Brug items=None og sæt inde i metoden self._items = [] if items is None else list(items)."), ("Esto evita compartir y también copia una entrada externa.", "This avoids sharing and also copies an external input.", "Det undgår deling og kopierer også eksternt input.")),
        practice("m12.p04", ActivityType.CODE_COMPLETION, ("Implementa __repr__ para Point(x,y).", "Implement __repr__ for Point(x,y).", "Implementér __repr__ for Point(x,y)."), (("Incluye nombre de clase y campos.", "Include class name and fields.", "Inkludér klassenavn og felter."),), ("def __repr__(self):\n    return f'Point(x={self.x!r}, y={self.y!r})'", "def __repr__(self):\n    return f'Point(x={self.x!r}, y={self.y!r})'", "def __repr__(self):\n    return f'Point(x={self.x!r}, y={self.y!r})'"), ("!r usa representaciones inequívocas de los valores.", "!r uses unambiguous value representations.", "!r bruger entydige værdirepræsentationer."), "class Point:\n    def __repr__(self):\n        pass"),
        practice("m12.p05", ActivityType.MATCHING, ("Relaciona método especial y protocolo.", "Match special method and protocol.", "Match særlig metode og protokol."), (("Piensa en len, in, for e igualdad.", "Think of len, in, for, and equality.", "Tænk på len, in, for og lighed."),), ("__len__-len; __contains__-in; __iter__-for; __eq__-==.", "__len__-len; __contains__-in; __iter__-for; __eq__-==.", "__len__-len; __contains__-in; __iter__-for; __eq__-==."), ("Los protocolos integran el objeto con sintaxis estándar.", "Protocols integrate the object with standard syntax.", "Protokoller integrerer objektet med standardsyntaks.")),
        practice("m12.p06", ActivityType.ORDERING, ("Ordena la construcción segura de un objeto.", "Order safe object construction.", "Sæt sikker objektkonstruktion i rækkefølge."), (("Valida antes de publicar estado parcial.", "Validate before publishing partial state.", "Validér før delvis tilstand offentliggøres."),), ("Recibir argumentos → normalizar → validar → asignar atributos → verificar invariante.", "Receive arguments → normalize → validate → assign attributes → verify invariant.", "Modtag argumenter → normalisér → validér → tildel attributter → verificér invariant."), ("El objeto debe quedar válido al terminar __init__.", "The object must be valid when __init__ ends.", "Objektet skal være gyldigt, når __init__ slutter.")),
        practice("m12.p07", ActivityType.SHORT_ANSWER, ("Distingue is y ==.", "Distinguish is and ==.", "Skeln mellem is og ==."), (("Uno compara identidad; el otro igualdad.", "One compares identity; the other equality.", "Den ene sammenligner identitet; den anden lighed."),), ("is comprueba si dos referencias son el mismo objeto; == comprueba igualdad según el tipo y puede ser verdadera para objetos distintos.", "is checks whether two references are the same object; == checks type-defined equality and may be true for distinct objects.", "is kontrollerer om to referencer er samme objekt; == kontrollerer typedefineret lighed og kan være sand for forskellige objekter."), ("No se debe usar is para comparar números o strings por valor.", "Do not use is for numeric or string value comparison.", "Brug ikke is til værdisammenligning af tal eller strings.")),
        practice("m12.p08", ActivityType.DATA_INTERPRETATION, ("Dos instancias recién creadas comparten la misma lista. Diagnostica el error.", "Two newly created instances share the same list. Diagnose the error.", "To nyoprettede instanser deler samme liste. Diagnosticér fejlen."), (("Busca un atributo de clase o parámetro predeterminado mutable.", "Look for a class attribute or mutable default parameter.", "Se efter en klasseattribut eller muterbar standardparameter."),), ("La colección fue creada una sola vez, como atributo de clase o valor predeterminado. Debe crearse por instancia.", "The collection was created once, as a class attribute or default value. It must be created per instance.", "Samlingen blev oprettet én gang som klasseattribut eller standardværdi. Den skal oprettes pr. instans."), ("Una prueba de independencia revela el aliasing.", "An independence test reveals the aliasing.", "En uafhængighedstest afslører aliasing.")),
        practice("m12.p09", ActivityType.DEBUGGING, ("Corrige una property setter que asigna antes de validar.", "Fix a property setter that assigns before validating.", "Ret en property-setter, der tildeler før validering."), (("Una excepción no debe dejar estado inválido.", "An exception must not leave invalid state.", "En exception må ikke efterlade ugyldig tilstand."),), ("Validar value primero y sólo después asignar self._value.", "Validate value first and only then assign self._value.", "Validér value først og tildel først derefter self._value."), ("La operación debe ser atómica respecto a la invariante.", "The operation should be atomic with respect to the invariant.", "Operationen bør være atomisk i forhold til invarianten.")),
        practice("m12.p10", ActivityType.ORAL_EXPLANATION, ("Explica cuándo preferir composición a herencia.", "Explain when to prefer composition over inheritance.", "Forklar hvornår komposition bør foretrækkes frem for arv."), (("Pregunta si la relación es tiene-un o es-un.", "Ask whether the relation is has-a or is-a.", "Spørg om relationen er har-en eller er-en."),), ("Se prefiere composición cuando un objeto contiene o delega componentes, cuando sólo se reutiliza parte del comportamiento o cuando se desean componentes intercambiables sin acoplar jerarquías.", "Prefer composition when an object contains or delegates to components, only part of behavior is reused, or interchangeable components are needed without coupling hierarchies.", "Foretræk komposition, når et objekt indeholder eller delegerer til komponenter, kun en del af adfærden genbruges, eller udskiftelige komponenter ønskes uden koblede hierarkier."), ("La herencia requiere sustituibilidad real.", "Inheritance requires genuine substitutability.", "Arv kræver reel substituerbarhed.")),
        practice("m12.p11", ActivityType.PIPELINE_DESIGN, ("Diseña un modelo de progreso con responsabilidades separadas.", "Design a progress model with separated responsibilities.", "Design en fremskridtsmodel med adskilte ansvar."), (("Separa datos, persistencia y presentación.", "Separate data, persistence, and presentation.", "Adskil data, persistens og præsentation."),), ("ModuleProgress mantiene estado y reglas; ProgressRepository guarda/carga; una vista presenta resultados. Se conectan por interfaces, no en una clase monolítica.", "ModuleProgress maintains state and rules; ProgressRepository saves/loads; a view presents results. They connect through interfaces rather than one monolithic class.", "ModuleProgress vedligeholder tilstand og regler; ProgressRepository gemmer/indlæser; en visning præsenterer resultater. De forbindes gennem interfaces, ikke én monolitisk klasse."), ("La separación mejora pruebas y cambio independiente.", "Separation improves testing and independent change.", "Adskillelse forbedrer test og uafhængige ændringer.")),
        practice("m12.p12", ActivityType.CODE_TRACING, ("Predice a is b y a == b para dos dataclass Point(1,2) distintas.", "Predict a is b and a == b for two distinct dataclass Point(1,2) objects.", "Forudsig a is b og a == b for to forskellige dataclass Point(1,2)-objekter."), (("dataclass genera igualdad por campos.", "dataclass generates field equality.", "dataclass genererer feltlighed."),), ("a is b es False; a == b es True.", "a is b is False; a == b is True.", "a is b er False; a == b er True."), ("Identidad física y valor lógico son distintos.", "Object identity and logical value are distinct.", "Objektidentitet og logisk værdi er forskellige.")),
    ),
    assessment_items=(
        objective_mcq("dm857.m12.assessment.001", ("¿Qué representa self en un método de instancia?", "What does self represent in an instance method?", "Hvad repræsenterer self i en instansmetode?"), (("instance", ("La instancia receptora", "The receiving instance", "Den modtagende instans")), ("class", ("Siempre la clase", "Always the class", "Altid klassen")), ("module", ("El módulo Python", "The Python module", "Python-modulet"))), "instance", ("El método enlazado pasa la instancia como self.", "A bound method passes the instance as self.", "En bundet metode sender instansen som self.")),
        authored_item("dm857.m12.assessment.002", ActivityType.MULTIPLE_SELECT, ("Selecciona riesgos de estado compartido accidental.", "Select risks of accidental shared state.", "Vælg risici for utilsigtet delt tilstand."), (), ("Lista como atributo de clase y parámetro predeterminado mutable.", "A list as a class attribute and a mutable default parameter.", "En liste som klasseattribut og en muterbar standardparameter."), options=(("class_list", ("Lista de clase mutable", "Mutable class list", "Muterbar klasseliste")), ("default_list", ("Parámetro items=[]", "Parameter items=[]", "Parameter items=[]")), ("factory", ("default_factory=list", "default_factory=list", "default_factory=list")), ("none", ("items=None con lista interna", "items=None with internal list", "items=None med intern liste"))), correct_option_ids=("class_list", "default_list")),
        authored_item("dm857.m12.assessment.003", ActivityType.CODE_TRACING, ("Dos objetos iguales por dataclass se crean por separado. Evalúa is y ==.", "Two value-equal dataclass objects are created separately. Evaluate is and ==.", "To værdilige dataclass-objekter oprettes separat. Vurdér is og ==."), (("is es False y == es True.", "is is False and == is True.", "is er False og == er True."),), ("La identidad difiere aunque los campos sean iguales.", "Identity differs even when fields are equal.", "Identiteten er forskellig, selv om felterne er ens.")),
        authored_item("dm857.m12.assessment.004", ActivityType.FILL_IN_THE_BLANK, ("Para una lista nueva por instancia usa field(____=list).", "For a fresh list per instance use field(____=list).", "For en ny liste pr. instans brug field(____=list)."), (("default_factory", "default_factory", "default_factory"),), ("La fábrica se invoca para cada objeto.", "The factory is called for each object.", "Fabrikken kaldes for hvert objekt.")),
        authored_item("dm857.m12.assessment.005", ActivityType.MATCHING, ("Relaciona método especial y operación.", "Match special method and operation.", "Match særlig metode og operation."), (), ("__repr__-repr; __len__-len; __iter__-for; __eq__-==.", "__repr__-repr; __len__-len; __iter__-for; __eq__-==.", "__repr__-repr; __len__-len; __iter__-for; __eq__-==."), options=(("repr", ("__repr__ → repr", "__repr__ → repr", "__repr__ → repr")), ("len", ("__len__ → len", "__len__ → len", "__len__ → len")), ("iter", ("__iter__ → for", "__iter__ → for", "__iter__ → for")), ("eq", ("__eq__ → ==", "__eq__ → ==", "__eq__ → =="))), correct_option_ids=("repr", "len", "iter", "eq")),
        authored_item("dm857.m12.assessment.006", ActivityType.ORDERING, ("Ordena un setter que preserva invariantes.", "Order a setter that preserves invariants.", "Sæt en setter, der bevarer invarianter, i rækkefølge."), (), ("Recibir valor → normalizar → validar → asignar → retornar.", "Receive value → normalize → validate → assign → return.", "Modtag værdi → normalisér → validér → tildel → returnér."), options=(("receive", ("Recibir", "Receive", "Modtag")), ("normalize", ("Normalizar", "Normalize", "Normalisér")), ("validate", ("Validar", "Validate", "Validér")), ("assign", ("Asignar", "Assign", "Tildel")), ("return", ("Retornar", "Return", "Returnér"))), correct_option_ids=("receive", "normalize", "validate", "assign", "return")),
        authored_item("dm857.m12.assessment.007", ActivityType.CODE_COMPLETION, ("Implementa __len__ para una colección interna _items.", "Implement __len__ for an internal _items collection.", "Implementér __len__ for en intern _items-samling."), (("def __len__(self):\n    return len(self._items)", "def __len__(self):\n    return len(self._items)", "def __len__(self):\n    return len(self._items)"),), ("Debe retornar un entero no negativo sin modificar estado.", "It must return a non-negative integer without changing state.", "Den skal returnere et ikke-negativt heltal uden at ændre tilstand."), rubric=(("Sin efectos secundarios.", "No side effects.", "Ingen sideeffekter."),)),
        authored_item("dm857.m12.assessment.008", ActivityType.DEBUGGING, ("Un setter asigna self._age=value y luego valida value<0. Corrígelo.", "A setter assigns self._age=value and then validates value<0. Fix it.", "En setter tildeler self._age=value og validerer derefter value<0. Ret den."), (("Validar primero y asignar sólo cuando value sea válido.", "Validate first and assign only when value is valid.", "Validér først og tildel kun, når value er gyldig."),), ("Una excepción no debe dejar estado inválido.", "An exception must not leave invalid state.", "En exception må ikke efterlade ugyldig tilstand.")),
        authored_item("dm857.m12.assessment.009", ActivityType.SHORT_ANSWER, ("Distingue atributo de clase y de instancia.", "Distinguish class and instance attributes.", "Skeln mellem klasse- og instansattributter."), (("El atributo de clase pertenece a la clase y puede compartirse; el de instancia se asigna al objeto y puede variar entre instancias.", "A class attribute belongs to the class and may be shared; an instance attribute belongs to one object and may differ among instances.", "En klasseattribut tilhører klassen og kan deles; en instansattribut tilhører ét objekt og kan variere mellem instanser."),), ("Una colección mutable de clase puede causar aliasing global.", "A mutable class collection may cause global aliasing.", "En muterbar klassesamling kan give global aliasing.")),
        authored_item("dm857.m12.assessment.010", ActivityType.DATA_INTERPRETATION, ("Modificar a.tags también cambia b.tags. Diagnostica y corrige.", "Changing a.tags also changes b.tags. Diagnose and fix.", "Ændring af a.tags ændrer også b.tags. Diagnosticér og ret."), (("Las instancias comparten una lista creada como atributo de clase o predeterminado mutable; crear una lista por instancia o usar default_factory.", "Instances share a list created as a class attribute or mutable default; create one list per instance or use default_factory.", "Instanser deler en liste oprettet som klasseattribut eller muterbar standard; opret én liste pr. instans eller brug default_factory."),), ("La prueba demuestra aliasing no intencionado.", "The test demonstrates unintended aliasing.", "Testen demonstrerer utilsigtet aliasing.")),
        authored_item("dm857.m12.assessment.011", ActivityType.PIPELINE_DESIGN, ("Diseña clases para importar, validar y presentar datos sin una clase monolítica.", "Design classes for importing, validating, and presenting data without one monolithic class.", "Design klasser til import, validering og præsentation uden én monolitisk klasse."), (("DataRecord modela datos; Validator aplica reglas; Repository gestiona E/S; Presenter transforma para la interfaz.", "DataRecord models data; Validator applies rules; Repository manages I/O; Presenter transforms for the UI.", "DataRecord modellerer data; Validator anvender regler; Repository håndterer I/O; Presenter transformerer til brugerfladen."),), ("Las responsabilidades separadas mejoran pruebas y mantenimiento.", "Separated responsibilities improve testing and maintenance.", "Adskilte ansvar forbedrer test og vedligeholdelse."), rubric=(("Evita mezclar E/S con el modelo.", "Avoids mixing I/O with the model.", "Undgår at blande I/O med modellen."),)),
        authored_item("dm857.m12.assessment.012", ActivityType.ORAL_EXPLANATION, ("Explica por qué frozen=True no garantiza inmutabilidad profunda.", "Explain why frozen=True does not guarantee deep immutability.", "Forklar hvorfor frozen=True ikke garanterer dyb immutabilitet."), (("Impide reasignar campos de la dataclass, pero un campo que contiene una lista u otro objeto mutable aún puede modificarse internamente.", "It prevents reassigning dataclass fields, but a field containing a list or another mutable object may still be mutated internally.", "Det forhindrer omtildeling af dataclass-felter, men et felt med en liste eller andet muterbart objekt kan stadig ændres internt."),), ("La inmutabilidad debe considerarse recursivamente.", "Immutability must be considered recursively.", "Immutabilitet skal vurderes rekursivt.")),
        authored_item("dm857.m12.assessment.013", ActivityType.DEBUGGING, ("Una subclase cambia un método para devolver None donde la base promete un resultado. Analiza el problema.", "A subclass changes a method to return None where the base promises a result. Analyze the problem.", "En underklasse ændrer en metode til at returnere None, hvor basen lover et resultat. Analysér problemet."), (("La subclase viola el contrato y no puede sustituir a la base; debe conservar la poscondición o no heredar.", "The subclass violates the contract and cannot substitute for the base; preserve the postcondition or avoid inheritance.", "Underklassen bryder kontrakten og kan ikke erstatte basen; bevar efterbetingelsen eller undgå arv."),), ("Herencia exige sustituibilidad.", "Inheritance requires substitutability.", "Arv kræver substituerbarhed.")),
        authored_item("dm857.m12.assessment.014", ActivityType.SHORT_ANSWER, ("Propón pruebas mínimas para una clase Temperature con property kelvin.", "Propose minimum tests for a Temperature class with a kelvin property.", "Foreslå minimale test for en Temperature-klasse med property kelvin."), (("Construcción válida, cero, negativo en construcción, actualización válida, actualización negativa que conserva el valor anterior, conversión de tipo y dos instancias independientes.", "Valid construction, zero, negative construction, valid update, negative update preserving the previous value, type conversion, and two independent instances.", "Gyldig konstruktion, nul, negativ konstruktion, gyldig opdatering, negativ opdatering der bevarer tidligere værdi, typekonvertering og to uafhængige instanser."),), ("Las pruebas cubren invariante y atomicidad.", "The tests cover invariant and atomicity.", "Testene dækker invariant og atomicitet.")),
    ),
    tutor_support=tutor_support(
        (
            "Una clase define comportamiento compartido y una instancia mantiene identidad y estado propios. self referencia la instancia receptora. __init__ debe dejar el objeto en un estado válido y evitar parámetros predeterminados mutables compartidos. is compara identidad y == igualdad lógica; __repr__ ayuda a depurar. La encapsulación limita mutaciones a operaciones que preservan invariantes, y una property permite validar asignaciones cuando existe una regla concreta. @dataclass reduce código repetitivo y default_factory crea colecciones independientes. Los métodos especiales integran objetos con protocolos como len, in, for y ==. La composición modela tiene-un y suele reducir acoplamiento; la herencia modela es-un y debe preservar el contrato de la base. Las pruebas cubren construcción, transiciones, igualdad, representación, errores, aliasing e independencia entre instancias. Los ejemplos biomédicos son modelos didácticos y no decisiones clínicas.",
            "A class defines shared behavior, and an instance maintains its own identity and state. self references the receiving instance. __init__ should leave the object valid and avoid shared mutable default parameters. is compares identity and == logical equality; __repr__ supports debugging. Encapsulation limits mutation to operations that preserve invariants, and a property validates assignments when there is a concrete rule. @dataclass reduces boilerplate, and default_factory creates independent collections. Special methods integrate objects with protocols such as len, in, for, and ==. Composition models has-a and often reduces coupling; inheritance models is-a and must preserve the base contract. Tests cover construction, transitions, equality, representation, errors, aliasing, and instance independence. Biomedical examples are teaching models, not clinical decisions.",
            "En klasse definerer delt adfærd, og en instans bevarer egen identitet og tilstand. self refererer til den modtagende instans. __init__ bør efterlade objektet gyldigt og undgå delte muterbare standardparametre. is sammenligner identitet og == logisk lighed; __repr__ støtter fejlfinding. Indkapsling begrænser mutation til operationer, der bevarer invarianter, og en property validerer tildelinger ved en konkret regel. @dataclass reducerer gentagelser, og default_factory opretter uafhængige samlinger. Særlige metoder integrerer objekter med protokoller som len, in, for og ==. Komposition modellerer har-en og reducerer ofte kobling; arv modellerer er-en og skal bevare basiskontrakten. Test dækker konstruktion, overgange, lighed, repræsentation, fejl, aliasing og instansuafhængighed. Biomedicinske eksempler er undervisningsmodeller og ikke kliniske beslutninger.",
        ),
        (
            ("Una clase define comportamiento y una instancia estado concreto.", "A class defines behavior and an instance concrete state.", "En klasse definerer adfærd og en instans konkret tilstand."),
            ("self es la instancia receptora.", "self is the receiving instance.", "self er den modtagende instans."),
            ("__init__ debe establecer invariantes.", "__init__ should establish invariants.", "__init__ bør etablere invarianter."),
            ("Los predeterminados mutables comparten objetos.", "Mutable defaults share objects.", "Muterbare standarder deler objekter."),
            ("is compara identidad y == igualdad.", "is compares identity and == equality.", "is sammenligner identitet og == lighed."),
            ("Una property debe proteger una regla concreta.", "A property should protect a concrete rule.", "En property bør beskytte en konkret regel."),
            ("default_factory crea valores por instancia.", "default_factory creates per-instance values.", "default_factory opretter værdier pr. instans."),
            ("frozen no implica inmutabilidad profunda.", "frozen does not imply deep immutability.", "frozen indebærer ikke dyb immutabilitet."),
            ("Los métodos especiales implementan protocolos.", "Special methods implement protocols.", "Særlige metoder implementerer protokoller."),
            ("Composición modela tiene-un.", "Composition models has-a.", "Komposition modellerer har-en."),
            ("Herencia modela es-un y exige sustituibilidad.", "Inheritance models is-a and requires substitutability.", "Arv modellerer er-en og kræver substituerbarhed."),
            ("El polimorfismo puede basarse en comportamiento.", "Polymorphism may be behavior-based.", "Polymorfi kan være adfærdsbaseret."),
            ("Las pruebas de independencia detectan aliasing.", "Independence tests detect aliasing.", "Uafhængighedstest opdager aliasing."),
            ("Una clase cohesionada tiene responsabilidades claras.", "A cohesive class has clear responsibilities.", "En sammenhængende klasse har tydelige ansvar."),
        ),
        (
            ("Creer que self es una palabra reservada mágica.", "Believing self is a magical reserved word.", "At tro at self er et magisk reserveret ord."),
            ("Usar una lista mutable como valor predeterminado.", "Using a mutable list as a default value.", "At bruge en muterbar liste som standardværdi."),
            ("Guardar datos de instancia en atributos de clase.", "Storing instance data in class attributes.", "At gemme instansdata i klasseattributter."),
            ("Usar is para comparar valores.", "Using is to compare values.", "At bruge is til værdisammenligning."),
            ("Asignar antes de validar en un setter.", "Assigning before validating in a setter.", "At tildele før validering i en setter."),
            ("Crear properties para todos los atributos sin necesidad.", "Creating properties for every attribute without need.", "At oprette properties for alle attributter uden behov."),
            ("Suponer que frozen congela objetos anidados.", "Assuming frozen freezes nested objects.", "At antage at frozen fryser indlejrede objekter."),
            ("Definir __eq__ y hash incoherentes.", "Defining inconsistent __eq__ and hash.", "At definere inkonsistent __eq__ og hash."),
            ("Usar herencia sólo para reutilizar código.", "Using inheritance only to reuse code.", "At bruge arv kun for at genbruge kode."),
            ("Construir una clase monolítica con E/S, análisis y vista.", "Building one monolithic I/O, analysis, and view class.", "At bygge én monolitisk klasse med I/O, analyse og visning."),
            ("Probar sólo una instancia.", "Testing only one instance.", "Kun at teste én instans."),
            ("Depender de atributos privados en las pruebas.", "Depending on private attributes in tests.", "At afhænge af private attributter i test."),
        ),
        (
            ("¿Qué estado pertenece a cada instancia?", "Which state belongs to each instance?", "Hvilken tilstand tilhører hver instans?"),
            ("¿Qué invariante debe cumplir el objeto al construirse?", "Which invariant must the object satisfy after construction?", "Hvilken invariant skal objektet opfylde efter konstruktion?"),
            ("¿La colección se crea una vez o por instancia?", "Is the collection created once or per instance?", "Oprettes samlingen én gang eller pr. instans?"),
            ("¿Necesitas comparar identidad o valor?", "Do you need identity or value comparison?", "Har du brug for identitets- eller værdisammenligning?"),
            ("¿Qué regla justifica esta property?", "Which rule justifies this property?", "Hvilken regel begrunder denne property?"),
            ("¿Qué campos forman la igualdad lógica?", "Which fields form logical equality?", "Hvilke felter danner logisk lighed?"),
            ("¿Qué protocolo intenta implementar el método especial?", "Which protocol is the special method implementing?", "Hvilken protokol implementerer den særlige metode?"),
            ("¿La relación es tiene-un o es-un?", "Is the relation has-a or is-a?", "Er relationen har-en eller er-en?"),
            ("¿Puede la subclase sustituir a la base?", "Can the subclass substitute for the base?", "Kan underklassen erstatte basen?"),
            ("¿Cómo probarías independencia entre objetos?", "How would you test independence between objects?", "Hvordan ville du teste uafhængighed mellem objekter?"),
            ("¿La clase tiene más de una razón para cambiar?", "Does the class have more than one reason to change?", "Har klassen mere end én grund til at ændre sig?"),
            ("¿Una excepción deja el objeto en estado válido?", "Does an exception leave the object valid?", "Efterlader en exception objektet gyldigt?"),
        ),
        (
            ("Distingue clase e instancia.", "Distinguishes class and instance.", "Skelner mellem klasse og instans."),
            ("Inicializa estado válido.", "Initializes valid state.", "Initialiserer gyldig tilstand."),
            ("Evita estado mutable compartido.", "Avoids shared mutable state.", "Undgår delt muterbar tilstand."),
            ("Diferencia identidad e igualdad.", "Differentiates identity and equality.", "Skelner mellem identitet og lighed."),
            ("Preserva invariantes en setters.", "Preserves invariants in setters.", "Bevarer invarianter i settere."),
            ("Usa dataclasses apropiadamente.", "Uses dataclasses appropriately.", "Bruger dataclasses passende."),
            ("Respeta contratos de métodos especiales.", "Respects special-method contracts.", "Respekterer kontrakter for særlige metoder."),
            ("Justifica composición o herencia.", "Justifies composition or inheritance.", "Begrunder komposition eller arv."),
            ("Separa responsabilidades.", "Separates responsibilities.", "Adskiller ansvar."),
            ("Prueba transiciones e independencia.", "Tests transitions and independence.", "Tester overgange og uafhængighed."),
        ),
        (
            ("No convertir modelos didácticos en recomendaciones clínicas.", "Do not turn teaching models into clinical recommendations.", "Gør ikke undervisningsmodeller til kliniske anbefalinger."),
            ("No usar is para igualdad de valores.", "Do not use is for value equality.", "Brug ikke is til værdilighed."),
            ("Advertir sobre predeterminados mutables.", "Warn about mutable defaults.", "Advar om muterbare standarder."),
            ("Validar antes de mutar estado.", "Validate before mutating state.", "Validér før mutation af tilstand."),
            ("No afirmar privacidad absoluta en Python.", "Do not claim absolute privacy in Python.", "Påstå ikke absolut privatliv i Python."),
            ("No recomendar herencia sin relación es-un.", "Do not recommend inheritance without an is-a relation.", "Anbefal ikke arv uden en er-en-relation."),
            ("Explicar límites de frozen=True.", "Explain frozen=True limitations.", "Forklar begrænsninger ved frozen=True."),
            ("Dar pistas antes de soluciones completas.", "Give hints before full solutions.", "Giv ledetråde før fulde løsninger."),
            ("Mantenerse dentro de diseño orientado a objetos introductorio.", "Stay within introductory object-oriented design.", "Hold dig til introducerende objektorienteret design."),
        ),
        (
            "Guttag, Introduction to Computation and Programming Using Python, 3rd ed.",
            "Python documentation: classes, data model, dataclasses, and property.",
            "Think Python, 3rd ed., classes and object-oriented programming chapters.",
        ),
    ),
)

_OBJECTIVE_MCQS = (
    ("001", ("¿Qué referencia self?", "What does self reference?", "Hvad refererer self til?"), (("instance", ("La instancia receptora", "The receiving instance", "Den modtagende instans")), ("class", ("Siempre la clase", "Always the class", "Altid klassen")), ("file", ("El archivo", "The file", "Filen"))), "instance", ("Un método enlazado pasa la instancia.", "A bound method passes the instance.", "En bundet metode sender instansen.")),
    ("002", ("¿Dónde debe quedar válida una instancia?", "When must an instance be valid?", "Hvornår skal en instans være gyldig?"), (("after_init", ("Al terminar __init__", "When __init__ ends", "Når __init__ slutter")), ("after_print", ("Después de print", "After print", "Efter print")), ("never", ("No es necesario", "It is unnecessary", "Det er unødvendigt"))), "after_init", ("La construcción debe establecer invariantes.", "Construction must establish invariants.", "Konstruktion skal etablere invarianter.")),
    ("003", ("¿Qué compara is?", "What does is compare?", "Hvad sammenligner is?"), (("identity", ("Identidad", "Identity", "Identitet")), ("value", ("Valor lógico", "Logical value", "Logisk værdi")), ("repr", ("Representación textual", "Text representation", "Tekstrepræsentation"))), "identity", ("is comprueba si es el mismo objeto.", "is checks whether it is the same object.", "is kontrollerer om det er samme objekt.")),
    ("004", ("¿Qué compara normalmente ==?", "What does == normally compare?", "Hvad sammenligner == normalt?"), (("equality", ("Igualdad lógica", "Logical equality", "Logisk lighed")), ("identity", ("Sólo identidad", "Identity only", "Kun identitet")), ("address", ("Dirección hexadecimal", "Hex address", "Hex-adresse"))), "equality", ("== delega en la igualdad del tipo.", "== delegates to type equality.", "== delegerer til typens lighed.")),
    ("005", ("¿Qué evita listas compartidas en dataclass?", "What avoids shared dataclass lists?", "Hvad undgår delte dataclass-lister?"), (("factory", ("field(default_factory=list)", "field(default_factory=list)", "field(default_factory=list)")), ("default", ("values=[]", "values=[]", "values=[]")), ("class_attr", ("Lista de clase", "Class list", "Klasseliste"))), "factory", ("La fábrica se ejecuta por instancia.", "The factory runs per instance.", "Fabrikken kører pr. instans.")),
    ("006", ("¿Qué método genera una representación para depuración?", "Which method provides a debugging representation?", "Hvilken metode giver en repræsentation til fejlfinding?"), (("repr", ("__repr__", "__repr__", "__repr__")), ("len", ("__len__", "__len__", "__len__")), ("iter", ("__iter__", "__iter__", "__iter__"))), "repr", ("__repr__ debe ser inequívoco y útil.", "__repr__ should be unambiguous and useful.", "__repr__ bør være entydig og nyttig.")),
    ("007", ("¿Qué método integra con len()?", "Which method integrates with len()?", "Hvilken metode integrerer med len()?"), (("len", ("__len__", "__len__", "__len__")), ("eq", ("__eq__", "__eq__", "__eq__")), ("str", ("__str__", "__str__", "__str__"))), "len", ("len(obj) llama __len__.", "len(obj) calls __len__.", "len(obj) kalder __len__.")),
    ("008", ("¿Qué método integra con for?", "Which method integrates with for?", "Hvilken metode integrerer med for?"), (("iter", ("__iter__", "__iter__", "__iter__")), ("contains", ("__contains__", "__contains__", "__contains__")), ("repr", ("__repr__", "__repr__", "__repr__"))), "iter", ("for solicita un iterador.", "for requests an iterator.", "for anmoder om en iterator.")),
    ("009", ("¿Qué relación modela composición?", "Which relation does composition model?", "Hvilken relation modellerer komposition?"), (("has", ("Tiene-un", "Has-a", "Har-en")), ("is", ("Es-un", "Is-a", "Er-en")), ("equals", ("Es igual a", "Equals", "Er lig med"))), "has", ("Un objeto contiene o delega a componentes.", "An object contains or delegates to components.", "Et objekt indeholder eller delegerer til komponenter.")),
    ("010", ("¿Qué relación pretende modelar herencia?", "Which relation should inheritance model?", "Hvilken relation bør arv modellere?"), (("is", ("Es-un", "Is-a", "Er-en")), ("has", ("Tiene-un", "Has-a", "Har-en")), ("uses", ("Usa temporalmente", "Temporarily uses", "Bruger midlertidigt"))), "is", ("La subclase debe ser sustituible por la base.", "The subclass should substitute for the base.", "Underklassen bør kunne erstatte basen.")),
    ("011", ("¿Dónde validar campos relacionados de dataclass?", "Where can related dataclass fields be validated?", "Hvor kan relaterede dataclass-felter valideres?"), (("post", ("__post_init__", "__post_init__", "__post_init__")), ("repr", ("__repr__", "__repr__", "__repr__")), ("del", ("__del__", "__del__", "__del__"))), "post", ("Se ejecuta después del inicializador generado.", "It runs after the generated initializer.", "Den kører efter den genererede initialisering.")),
    ("012", ("¿Qué debe hacer un setter antes de asignar?", "What should a setter do before assignment?", "Hvad bør en setter gøre før tildeling?"), (("validate", ("Validar", "Validate", "Validér")), ("assign", ("Asignar y luego comprobar", "Assign then check", "Tildel og kontrollér derefter")), ("print", ("Imprimir", "Print", "Udskriv"))), "validate", ("Evita dejar estado inválido tras una excepción.", "It avoids invalid state after an exception.", "Det undgår ugyldig tilstand efter en exception.")),
    ("013", ("¿Qué atributo suele comunicar uso interno?", "Which attribute usually communicates internal use?", "Hvilken attribut signalerer normalt intern brug?"), (("underscore", ("Nombre con _ inicial", "Leading-underscore name", "Navn med indledende _")), ("uppercase", ("Nombre en mayúsculas", "Uppercase name", "Navn med store bogstaver")), ("number", ("Nombre numérico", "Numeric name", "Numerisk navn"))), "underscore", ("Es una convención de Python.", "It is a Python convention.", "Det er en Python-konvention.")),
    ("014", ("¿Qué puede permanecer mutable en una dataclass frozen?", "What may remain mutable in a frozen dataclass?", "Hvad kan forblive muterbart i en frozen dataclass?"), (("nested", ("Un objeto anidado mutable", "A nested mutable object", "Et indlejret muterbart objekt")), ("field_assignment", ("La reasignación directa de campos", "Direct field reassignment", "Direkte omtildeling af felter")), ("class", ("La palabra class", "The class keyword", "Nøgleordet class"))), "nested", ("frozen no congela recursivamente.", "frozen does not recursively freeze.", "frozen fryser ikke rekursivt.")),
    ("015", ("¿Qué prueba detecta aliasing entre instancias?", "Which test detects aliasing between instances?", "Hvilken test opdager aliasing mellem instanser?"), (("independent", ("Modificar una y comprobar la otra", "Modify one and inspect the other", "Ændr den ene og kontrollér den anden")), ("same", ("Probar una sola instancia", "Test one instance only", "Test kun én instans")), ("repr", ("Imprimir la clase", "Print the class", "Udskriv klassen"))), "independent", ("La segunda no debe cambiar.", "The second should not change.", "Den anden bør ikke ændre sig.")),
    ("016", ("¿Qué protocolo implementa __contains__?", "Which protocol does __contains__ implement?", "Hvilken protokol implementerer __contains__?"), (("in", ("in", "in", "in")), ("len", ("len", "len", "len")), ("repr", ("repr", "repr", "repr"))), "in", ("x in obj consulta __contains__.", "x in obj consults __contains__.", "x in obj bruger __contains__.")),
    ("017", ("¿Qué suele ser mejor para componentes intercambiables?", "What is often better for interchangeable components?", "Hvad er ofte bedre for udskiftelige komponenter?"), (("composition", ("Composición", "Composition", "Komposition")), ("deep", ("Herencia profunda", "Deep inheritance", "Dyb arv")), ("global", ("Variables globales", "Global variables", "Globale variable"))), "composition", ("Reduce acoplamiento a una jerarquía.", "It reduces coupling to a hierarchy.", "Det reducerer kobling til et hierarki.")),
    ("018", ("¿Qué responsabilidad tiene __repr__?", "What responsibility does __repr__ have?", "Hvilket ansvar har __repr__?"), (("debug", ("Representación útil para depuración", "Useful debugging representation", "Nyttig repræsentation til fejlfinding")), ("save", ("Guardar automáticamente en disco", "Automatically save to disk", "Gem automatisk på disk")), ("validate", ("Validar todos los setters", "Validate all setters", "Validér alle settere"))), "debug", ("Debe mostrar estado relevante de forma clara.", "It should clearly show relevant state.", "Den bør tydeligt vise relevant tilstand.")),
    ("019", ("¿Qué diseño tiene una sola razón clara para cambiar?", "Which design has one clear reason to change?", "Hvilket design har én tydelig grund til at ændre sig?"), (("cohesive", ("Clase cohesionada", "Cohesive class", "Sammenhængende klasse")), ("monolith", ("Clase monolítica", "Monolithic class", "Monolitisk klasse")), ("global", ("Estado global", "Global state", "Global tilstand"))), "cohesive", ("Responsabilidades claras mejoran mantenimiento.", "Clear responsibilities improve maintenance.", "Tydelige ansvar forbedrer vedligeholdelse.")),
    ("020", ("¿Qué debe preservar una subclase?", "What must a subclass preserve?", "Hvad skal en underklasse bevare?"), (("contract", ("Contrato de la base", "Base contract", "Basiskontrakten")), ("private_name", ("Todos los nombres privados", "All private names", "Alle private navne")), ("memory", ("La misma dirección", "The same address", "Samme adresse"))), "contract", ("La sustituibilidad depende del comportamiento.", "Substitutability depends on behavior.", "Substituerbarhed afhænger af adfærd.")),
)

_OBJECTIVE_TFS = (
    ("021", ("Cada instancia puede mantener estado independiente.", "Each instance may maintain independent state.", "Hver instans kan bevare uafhængig tilstand."), True, ("Los atributos de instancia pertenecen al objeto.", "Instance attributes belong to the object.", "Instansattributter tilhører objektet.")),
    ("022", ("__init__ debe retornar la instancia.", "__init__ must return the instance.", "__init__ skal returnere instansen."), False, ("Debe retornar None implícitamente.", "It must return None implicitly.", "Den skal implicit returnere None.")),
    ("023", ("Usar items=[] puede compartir estado entre instancias.", "Using items=[] may share state between instances.", "Brug af items=[] kan dele tilstand mellem instanser."), True, ("El valor predeterminado se crea una vez.", "The default value is created once.", "Standardværdien oprettes én gang.")),
    ("024", ("is y == siempre producen el mismo resultado.", "is and == always produce the same result.", "is og == giver altid samme resultat."), False, ("Identidad y igualdad son conceptos distintos.", "Identity and equality are distinct concepts.", "Identitet og lighed er forskellige begreber.")),
    ("025", ("Una property puede validar asignaciones.", "A property can validate assignments.", "En property kan validere tildelinger."), True, ("El setter puede preservar invariantes.", "The setter can preserve invariants.", "Setteren kan bevare invarianter.")),
    ("026", ("frozen=True garantiza inmutabilidad profunda.", "frozen=True guarantees deep immutability.", "frozen=True garanterer dyb immutabilitet."), False, ("Los objetos anidados pueden seguir siendo mutables.", "Nested objects may remain mutable.", "Indlejrede objekter kan forblive muterbare.")),
    ("027", ("__iter__ permite usar un objeto en for.", "__iter__ permits using an object in for.", "__iter__ gør det muligt at bruge et objekt i for."), True, ("Forma parte del protocolo de iteración.", "It belongs to the iteration protocol.", "Den hører til iterationsprotokollen.")),
    ("028", ("Composición siempre requiere herencia.", "Composition always requires inheritance.", "Komposition kræver altid arv."), False, ("Composición contiene o delega objetos.", "Composition contains or delegates to objects.", "Komposition indeholder eller delegerer til objekter.")),
    ("029", ("Una subclase debe preservar las poscondiciones de la base.", "A subclass should preserve base postconditions.", "En underklasse bør bevare basens efterbetingelser."), True, ("Es necesaria para sustituibilidad.", "This is required for substitutability.", "Det er nødvendigt for substituerbarhed.")),
    ("030", ("Probar dos instancias ayuda a detectar estado compartido.", "Testing two instances helps detect shared state.", "Test af to instanser hjælper med at opdage delt tilstand."), True, ("Modificar una no debe alterar la otra.", "Changing one should not alter the other.", "Ændring af den ene bør ikke ændre den anden.")),
)

LOCALIZED_OBJECTIVE_QUESTION_BANK_12 = tuple(
    objective_mcq(
        f"dm857.m12.bank.{suffix}", prompt, options, correct_option_id, explanation
    )
    for suffix, prompt, options, correct_option_id, explanation in _OBJECTIVE_MCQS
) + tuple(
    objective_tf(
        f"dm857.m12.bank.{suffix}",
        prompt,
        correct=correct,
        explanation=explanation,
    )
    for suffix, prompt, correct, explanation in _OBJECTIVE_TFS
)


def materialize_module_12_question_bank(
    locale: AppLocale | str = AppLocale.SPANISH_SPAIN,
) -> tuple[AssessmentItem, ...]:
    """Materialize the stable objective bank in one supported locale."""
    resolved = locale if isinstance(locale, AppLocale) else AppLocale.resolve(locale)
    return tuple(item.materialize(resolved) for item in LOCALIZED_OBJECTIVE_QUESTION_BANK_12)


MODULE_12_OOP: LearningModule = LOCALIZED_MODULE_12_OOP.materialize(AppLocale.SPANISH_SPAIN)
OBJECTIVE_QUESTION_BANK_12 = materialize_module_12_question_bank()

__all__ = [
    "LOCALIZED_MODULE_12_OOP",
    "LOCALIZED_OBJECTIVE_QUESTION_BANK_12",
    "MODULE_12_OOP",
    "OBJECTIVE_QUESTION_BANK_12",
    "materialize_module_12_question_bank",
]
