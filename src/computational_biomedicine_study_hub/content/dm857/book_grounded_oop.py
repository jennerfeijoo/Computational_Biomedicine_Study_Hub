"""Book-grounded extension for DM857 object-oriented substitution contracts."""

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


def update_oop_audit(
    audit: tuple[ModuleSourceAudit, ...],
) -> tuple[ModuleSourceAudit, ...]:
    """Mark M12 reviewed after its focused substitution extension is present."""
    updated: list[ModuleSourceAudit] = []
    for item in audit:
        if item.module_id == "dm857.m12":
            updated.append(
                replace(
                    item,
                    state="consistent",
                    finding=(
                        "Existing coverage of classes, construction, identity, equality, "
                        "encapsulation, dataclasses, protocols, composition, limited inheritance, "
                        "polymorphism, shared-state errors, and object testing is consistent. "
                        "Override compatibility and substitutability needed one explicit treatment."
                    ),
                    implemented_change=(
                        "Added an original substitution-contract explanation, valid and invalid "
                        "override example, shared-client practice, and stable objective item."
                    ),
                )
            )
        else:
            updated.append(item)
    return tuple(updated)


def _extend_oop(module: LocalizedLearningModule) -> LocalizedLearningModule:
    """Add safe overriding and substitutability boundaries to M12."""
    extended = replace(
        module,
        objectives=module.objectives
        + (
            objective(
                "m12.bg.o1",
                (
                    "Evaluar si una sobrescritura preserva el contrato y permite sustituir la "
                    "clase base por la subclase.",
                    "Evaluate whether an override preserves the contract and permits substituting "
                    "a subclass for its base class.",
                    "Vurdere om en overskrivning bevarer kontrakten og tillader, at en underklasse "
                    "erstatter sin basisklasse.",
                ),
            ),
        ),
        concepts=module.concepts
        + (
            concept(
                "substitution-safe-overrides",
                (
                    "Sobrescritura segura y sustitución",
                    "Safe overriding and substitution",
                    "Sikker overskrivning og substitution",
                ),
                (
                    "La herencia sólo es útil cuando un objeto de la subclase puede ocupar los "
                    "lugares previstos para la clase base sin romper el código cliente. Al "
                    "sobrescribir un método, la subclase no debe exigir argumentos adicionales, "
                    "rechazar entradas que el contrato base aceptaba, devolver un resultado más "
                    "débil ni introducir efectos o errores incompatibles. Puede ofrecer una "
                    "garantía más fuerte, añadir comportamiento y reutilizar trabajo común con "
                    "super(), siempre que conserve el comportamiento observable prometido. "
                    "super() controla la delegación y la resolución de métodos; no demuestra por "
                    "sí solo que el contrato sea correcto. Una suite escrita contra la interfaz "
                    "base debe ejecutarse sobre cada subclase. Si una relación conceptual no "
                    "sostiene esta sustitución, la composición suele modelarla mejor.",
                    "Inheritance is useful only when a subclass object can occupy every place "
                    "intended for the base class without breaking client code. When overriding a "
                    "method, the subclass should not require extra arguments, reject inputs the "
                    "base contract accepted, return a weaker result, or introduce incompatible "
                    "effects or errors. It may provide a stronger guarantee, add behavior, and "
                    "reuse common work with super(), provided it preserves the promised observable "
                    "behavior. super() controls delegation and method resolution; it does not by "
                    "itself prove contract correctness. A suite written against the base interface "
                    "should run against every subclass. If a conceptual relation cannot support "
                    "that substitution, composition usually models it better.",
                    "Arv er kun nyttig, når et objekt fra underklassen kan bruges alle steder, hvor "
                    "basisklassen forventes, uden at klientkode brydes. Ved overskrivning bør "
                    "underklassen ikke kræve ekstra argumenter, afvise input som basiskontrakten "
                    "accepterede, returnere et svagere resultat eller indføre inkompatible effekter "
                    "eller fejl. Den må give en stærkere garanti, tilføje adfærd og genbruge fælles "
                    "arbejde med super(), hvis den lovede observerbare adfærd bevares. super() "
                    "styrer delegation og metodeopslag; det beviser ikke i sig selv kontraktens "
                    "korrekthed. En suite skrevet mod basisinterfacet bør kunne køres på hver "
                    "underklasse. Hvis relationen ikke understøtter substitution, er komposition "
                    "ofte en bedre model.",
                ),
                (
                    (
                        "Una subclase no debe fortalecer las precondiciones del método base.",
                        "A subclass should not strengthen the base method's preconditions.",
                        "En underklasse bør ikke skærpe basismetodens forudsætninger.",
                    ),
                    (
                        "La subclase debe conservar o reforzar las garantías observables.",
                        "The subclass should preserve or strengthen observable guarantees.",
                        "Underklassen bør bevare eller styrke observerbare garantier.",
                    ),
                    (
                        "super() reutiliza implementación; no valida sustituibilidad.",
                        "super() reuses implementation; it does not validate substitutability.",
                        "super() genbruger implementering; det validerer ikke substitution.",
                    ),
                    (
                        "Una suite de cliente compartida prueba el contrato de toda la jerarquía.",
                        "A shared client suite tests the contract across the hierarchy.",
                        "En fælles klientsuite tester kontrakten i hele hierarkiet.",
                    ),
                ),
            ),
        ),
        worked_examples=module.worked_examples
        + (
            example(
                "m12.bg.e01",
                (
                    "Detectar una sobrescritura incompatible",
                    "Detect an incompatible override",
                    "Opdag en inkompatibel overskrivning",
                ),
                (
                    "Ejecuta el mismo cliente sobre una clase base, una subclase compatible que "
                    "usa super() y una subclase que exige un argumento nuevo.",
                    "Run the same client against a base class, a compatible subclass that uses "
                    "super(), and a subclass that requires a new argument.",
                    "Kør den samme klient på en basisklasse, en kompatibel underklasse der bruger "
                    "super(), og en underklasse der kræver et nyt argument.",
                ),
                (
                    (
                        "El cliente llama report() sin conocer el tipo concreto.",
                        "The client calls report() without knowing the concrete type.",
                        "Klienten kalder report() uden at kende den konkrete type.",
                    ),
                    (
                        "TaggedReading conserva la firma y el resultado string.",
                        "TaggedReading preserves the signature and string result.",
                        "TaggedReading bevarer signaturen og string-resultatet.",
                    ),
                    (
                        "BrokenReading fortalece la precondición al exigir unit.",
                        "BrokenReading strengthens the precondition by requiring unit.",
                        "BrokenReading skærper forudsætningen ved at kræve unit.",
                    ),
                ),
                "class Reading:\n"
                "    def __init__(self, value):\n"
                "        if value < 0:\n"
                "            raise ValueError('value must be non-negative')\n"
                "        self._value = float(value)\n\n"
                "    def report(self):\n"
                "        return f'{self._value:.1f}'\n\n"
                "class TaggedReading(Reading):\n"
                "    def __init__(self, value, tag):\n"
                "        super().__init__(value)\n"
                "        self._tag = str(tag)\n\n"
                "    def report(self):\n"
                "        return f'{self._tag}:{super().report()}'\n\n"
                "class BrokenReading(Reading):\n"
                "    def report(self, unit):\n"
                "        return f'{self._value:.1f} {unit}'\n\n"
                "def render(reading):\n"
                "    result = reading.report()\n"
                "    if not isinstance(result, str) or not result:\n"
                "        raise TypeError('report contract violated')\n"
                "    return result\n\n"
                "print(render(Reading(2)))\n"
                "print(render(TaggedReading(2, 'A')))\n"
                "try:\n"
                "    print(render(BrokenReading(2)))\n"
                "except TypeError:\n"
                "    print('contract violation')",
                "2.0\nA:2.0\ncontract violation",
                (
                    "La subclase compatible puede sustituir Reading porque acepta la misma llamada "
                    "y mantiene un resultado string no vacío. BrokenReading obliga al cliente a "
                    "conocer un detalle del subtipo y por eso rompe el contrato.",
                    "The compatible subclass can replace Reading because it accepts the same call "
                    "and preserves a non-empty string result. BrokenReading forces the client to "
                    "know a subtype detail and therefore breaks the contract.",
                    "Den kompatible underklasse kan erstatte Reading, fordi den accepterer samme "
                    "kald og bevarer et ikke-tomt string-resultat. BrokenReading tvinger klienten "
                    "til at kende en undertypedetalje og bryder derfor kontrakten.",
                ),
            ),
        ),
        practice_exercises=module.practice_exercises
        + (
            practice(
                "m12.bg.p01",
                ActivityType.DEBUGGING,
                (
                    "Una clase base Parser acepta cualquier string y devuelve una lista. Una "
                    "subclase sobrescribe parse(text) para aceptar sólo strings que empiecen por "
                    "'BIO:' y devuelve None cuando no cumplen la condición. Diagnostica dos "
                    "violaciones del contrato y propón una alternativa.",
                    "A base Parser accepts any string and returns a list. A subclass overrides "
                    "parse(text) to accept only strings beginning with 'BIO:' and returns None when "
                    "the condition is not met. Diagnose two contract violations and propose an "
                    "alternative.",
                    "En basis-Parser accepterer enhver string og returnerer en liste. En "
                    "underklasse overskriver parse(text), så den kun accepterer strings der "
                    "begynder med 'BIO:', og returnerer None ellers. Diagnosticér to "
                    "kontraktbrud og foreslå et alternativ.",
                ),
                (
                    (
                        "Compara las entradas aceptadas por la base y por la subclase.",
                        "Compare inputs accepted by the base and subclass.",
                        "Sammenlign input accepteret af basis og underklasse.",
                    ),
                    (
                        "Compara el tipo de resultado prometido.",
                        "Compare the promised result type.",
                        "Sammenlign den lovede resultattype.",
                    ),
                ),
                (
                    "La subclase fortalece la precondición porque rechaza strings que la base "
                    "aceptaba y debilita la postcondición porque puede devolver None en vez de una "
                    "lista. Debe conservar la entrada y salida del contrato base, o el filtrado "
                    "BIO debe modelarse como un colaborador compuesto o como un método distinto "
                    "con un contrato explícito.",
                    "The subclass strengthens the precondition because it rejects strings accepted "
                    "by the base and weakens the postcondition because it may return None instead "
                    "of a list. It should preserve the base input and output contract, or BIO "
                    "filtering should be modeled as a composed collaborator or a separate method "
                    "with an explicit contract.",
                    "Underklassen skærper forudsætningen, fordi den afviser strings som basis "
                    "accepterede, og svækker efterbetingelsen, fordi den kan returnere None i "
                    "stedet for en liste. Den bør bevare basiskontraktens input og output, eller "
                    "BIO-filtrering bør modelleres som en sammensat samarbejdspartner eller en "
                    "separat metode med eksplicit kontrakt.",
                ),
                (
                    "La respuesta debe razonar desde el cliente de Parser, no desde la intención "
                    "interna de la subclase.",
                    "The answer must reason from the Parser client's perspective, not the "
                    "subclass's internal intent.",
                    "Svaret skal tage udgangspunkt i Parser-klienten, ikke underklassens interne "
                    "hensigt.",
                ),
            ),
        ),
        assessment_items=module.assessment_items
        + (
            objective_mcq(
                "dm857.m12.book.001",
                (
                    "¿Qué cambio conserva mejor la sustituibilidad de una subclase?",
                    "Which change best preserves subclass substitutability?",
                    "Hvilken ændring bevarer bedst underklassens substitution?",
                ),
                (
                    (
                        "extra_required_argument",
                        (
                            "Hacer obligatorio un argumento adicional en un método sobrescrito.",
                            "Require an additional argument in an overridden method.",
                            "Kræv et ekstra argument i en overskrevet metode.",
                        ),
                    ),
                    (
                        "compatible_extension",
                        (
                            "Mantener la firma y las garantías del método base, reutilizar trabajo "
                            "con super() y añadir información compatible al resultado.",
                            "Preserve the base method's signature and guarantees, reuse work with "
                            "super(), and add compatible information to the result.",
                            "Bevar basismetodens signatur og garantier, genbrug arbejde med "
                            "super(), og tilføj kompatibel information til resultatet.",
                        ),
                    ),
                    (
                        "weaker_result",
                        (
                            "Devolver None en casos donde el método base prometía una colección.",
                            "Return None where the base method promised a collection.",
                            "Returnér None hvor basismetoden lovede en samling.",
                        ),
                    ),
                ),
                "compatible_extension",
                (
                    "La sustitución exige que el cliente pueda realizar las mismas llamadas y "
                    "confiar en garantías compatibles. super() puede reutilizar la implementación "
                    "base, pero la compatibilidad depende del contrato completo.",
                    "Substitution requires clients to make the same calls and rely on compatible "
                    "guarantees. super() may reuse the base implementation, but compatibility "
                    "depends on the complete contract.",
                    "Substitution kræver, at klienter kan foretage de samme kald og stole på "
                    "kompatible garantier. super() kan genbruge basisimplementeringen, men "
                    "kompatibilitet afhænger af hele kontrakten.",
                ),
            ),
        ),
    )
    return _with_source_basis(
        extended,
        ("guttag-2021-ch10-12", "downey-2024-files-oop"),
    )


def apply_oop_book_extension(
    modules: tuple[LocalizedLearningModule, ...],
) -> tuple[LocalizedLearningModule, ...]:
    """Apply the focused M12 extension without changing other modules."""
    return tuple(
        _extend_oop(module) if module.module_id == "dm857.m12" else module for module in modules
    )
