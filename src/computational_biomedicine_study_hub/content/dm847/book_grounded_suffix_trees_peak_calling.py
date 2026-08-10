"""Focused source-grounded extensions for DM847 suffix trees and peak calling."""

from __future__ import annotations

from dataclasses import replace

from ..localized_models import LocalizedLearningModule
from .authoring import concept, example, objective_mcq
from .book_grounded_audit import ModuleSourceAudit


def update_suffix_tree_peak_calling_audit(
    audit: tuple[ModuleSourceAudit, ...],
) -> tuple[ModuleSourceAudit, ...]:
    findings = {
        "dm847.m06": "Suffix-array/BWT coverage is extended with suffix trees and their indexing trade-offs.",
        "dm847.m10": "OMICS coverage is extended with bimodal peak calling, strand-aware signal, controls, QC and reproducibility.",
    }
    changes = {
        "dm847.m06": "Added an original trilingual suffix-tree concept, example and objective item.",
        "dm847.m10": "Added an original trilingual bimodal peak-calling concept, example and objective item.",
    }
    return tuple(
        replace(item, state="consistent", finding=findings[item.module_id], implemented_change=changes[item.module_id])
        if item.module_id in findings else item
        for item in audit
    )


def _extend_m06(module: LocalizedLearningModule) -> LocalizedLearningModule:
    return replace(
        module,
        concepts=module.concepts + (
            concept(
                "suffix-trees",
                ("Suffix trees", "Suffix trees", "Suffixtræer"),
                (
                    "Un suffix tree representa todos los sufijos mediante un trie comprimido. Las hojas conservan posiciones de inicio y los caminos compartidos compactan prefijos comunes. Frente a un suffix array, ofrece otra estructura para búsquedas de patrones, con mayor complejidad y coste de memoria.",
                    "A suffix tree represents all suffixes using a compressed trie. Leaves retain starting positions and shared paths compact common prefixes. Compared with a suffix array, it provides another structure for pattern queries, with greater implementation and memory complexity.",
                    "Et suffixtræ repræsenterer alle suffikser med et komprimeret trie. Blade bevarer startpositioner, og fælles stier komprimerer fælles præfikser. Sammenlignet med et suffix-array giver det en anden struktur til mønstersøgning med større implementerings- og hukommelseskompleksitet.",
                ),
                (
                    ("Las hojas representan posiciones de inicio.", "Leaves represent starting positions.", "Blade repræsenterer startpositioner."),
                    ("Los prefijos compartidos pueden compactarse.", "Shared prefixes can be compacted.", "Fælles præfikser kan komprimeres."),
                    ("La memoria es una consideración práctica.", "Memory is a practical consideration.", "Hukommelse er en praktisk overvejelse."),
                ),
            ),
        ),
        worked_examples=module.worked_examples + (
            example(
                "m06.bg.suffix-tree",
                ("Relacionar sufijos con un suffix tree", "Relate suffixes to a suffix tree", "Relatér suffikser til et suffixtræ"),
                ("Identifica un prefijo común entre sufijos y explica cómo se compacta.", "Identify a shared prefix between suffixes and explain how it is compacted.", "Identificér et fælles præfiks mellem suffikser og forklar, hvordan det komprimeres."),
                (("Agrupa sufijos por prefijo inicial.", "Group suffixes by initial prefix.", "Gruppér suffikser efter begyndelsespræfiks."),),
                "sequence = 'banana$'\nsuffixes = [sequence[i:] for i in range(len(sequence))]\nprint(suffixes)",
                "['banana$', 'anana$', 'nana$', 'ana$', 'na$', 'a$', '$']",
                ("El árbol comparte tramos comunes antes de ramificarse.", "The tree shares common stretches before branching.", "Træet deler fælles stykker før forgrening."),
            ),
        ),
        assessment_items=module.assessment_items + (
            objective_mcq(
                "dm847.m06.audit.001",
                ("¿Qué representa un suffix tree comprimido?", "What does a compressed suffix tree represent?", "Hvad repræsenterer et komprimeret suffixtræ?"),
                (
                    ("a", ("Todos los sufijos mediante un trie comprimido.", "All suffixes using a compressed trie.", "Alle suffikser med et komprimeret trie.")),
                    ("b", ("Sólo el GC%.", "Only GC%.", "Kun GC%.")),
                    ("c", ("Sólo las lecturas únicas.", "Only unique reads.", "Kun unikke reads.")),
                ),
                "a",
                ("La estructura representa los sufijos y sus posiciones.", "The structure represents suffixes and their positions.", "Strukturen repræsenterer suffikser og deres positioner."),
            ),
        ),
    )


def _extend_m10(module: LocalizedLearningModule) -> LocalizedLearningModule:
    return replace(
        module,
        concepts=module.concepts + (
            concept(
                "bimodal-peak-calling",
                ("Bimodal peak calling", "Bimodal peak calling", "Bimodal peak calling"),
                (
                    "Un perfil bimodal puede aparecer cuando la señal genómica presenta dos lóbulos alrededor de un punto biológico común. El peak calling debe evaluarse con control, fondo, orientación de hebras, calidad y reproducibilidad. Dos lóbulos no constituyen por sí solos evidencia de función biológica.",
                    "A bimodal profile can occur when genomic signal forms two lobes around a shared biological point. Peak calling should be evaluated with controls, background, strand orientation, quality and reproducibility. Two lobes alone are not evidence of biological function.",
                    "En bimodal profil kan opstå, når genomisk signal danner to toppe omkring et fælles biologisk punkt. Peak calling bør vurderes med kontroller, baggrund, strengorientering, kvalitet og reproducerbarhed. To toppe alene er ikke evidens for biologisk funktion.",
                ),
                (
                    ("La forma bimodal describe señal, no función.", "Bimodal shape describes signal, not function.", "Bimodal form beskriver signal, ikke funktion."),
                    ("El control ayuda a separar señal y fondo.", "Controls help separate signal from background.", "Kontroller hjælper med at skelne signal fra baggrund."),
                    ("Las réplicas aportan evidencia de reproducibilidad.", "Replicates provide reproducibility evidence.", "Replikater giver evidens for reproducerbarhed."),
                ),
            ),
        ),
        worked_examples=module.worked_examples + (
            example(
                "m10.bg.bimodal-peak-calling",
                ("Interpretar una señal bimodal", "Interpret a bimodal signal", "Fortolk et bimodalt signal"),
                ("Define las comprobaciones mínimas antes de llamar un pico.", "Define minimum checks before calling a peak.", "Definér minimumskontroller før et peak kaldes."),
                (("Comprueba control, fondo, orientación y réplicas.", "Check control, background, orientation and replicates.", "Kontrollér kontrol, baggrund, orientering og replikater."),),
                "checks = ['control', 'background', 'strand_orientation', 'replicates']\nprint(checks)",
                "['control', 'background', 'strand_orientation', 'replicates']",
                ("La interpretación biológica requiere señal controlada y reproducible.", "Biological interpretation requires controlled, reproducible signal.", "Biologisk fortolkning kræver kontrolleret, reproducerbart signal."),
            ),
        ),
        assessment_items=module.assessment_items + (
            objective_mcq(
                "dm847.m10.audit.001",
                ("¿Qué debe comprobarse antes de interpretar un peak call bimodal?", "What should be checked before interpreting a bimodal peak call?", "Hvad bør kontrolleres før fortolkning af et bimodalt peak call?"),
                (
                    ("a", ("Control, fondo, orientación y reproducibilidad.", "Control, background, orientation and reproducibility.", "Kontrol, baggrund, orientering og reproducerbarhed.")),
                    ("b", ("Sólo el color de la figura.", "Only figure colour.", "Kun figurens farve.")),
                    ("c", ("Sólo el número de lecturas.", "Only read count.", "Kun read count.")),
                ),
                "a",
                ("La forma bimodal requiere controles técnicos y evidencia reproducible.", "Bimodal shape requires technical controls and reproducible evidence.", "Bimodal form kræver tekniske kontroller og reproducerbar evidens."),
            ),
        ),
    )


def apply_suffix_tree_peak_calling_extensions(
    modules: tuple[LocalizedLearningModule, ...],
) -> tuple[LocalizedLearningModule, ...]:
    if len(modules) != 10:
        raise ValueError("DM847 requires exactly ten authored modules.")
    updated = list(modules)
    updated[5] = _extend_m06(updated[5])
    updated[9] = _extend_m10(updated[9])
    return tuple(updated)


__all__ = ["apply_suffix_tree_peak_calling_extensions", "update_suffix_tree_peak_calling_audit"]
