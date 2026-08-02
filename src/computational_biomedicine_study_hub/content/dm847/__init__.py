"""Complete trilingual authored content and validated runtime bundles for DM847."""

from __future__ import annotations

from dataclasses import replace

from ...i18n import AppLocale
from ..bundles import LocalizedModuleBundle, validate_bundle_catalog
from ..localized_models import LocalizedText
from .book_grounded_audit import (
    DM847_BOOK_SOURCES,
    DM847_MODULE_SOURCE_AUDIT as _BASE_DM847_MODULE_SOURCE_AUDIT,
    apply_book_grounded_extensions,
)
from .book_grounded_hmm_bwt import apply_hmm_bwt_extensions, update_hmm_bwt_audit
from .module_01_molecular_information import (
    LOCALIZED_MODULE_01_MOLECULAR_INFORMATION,
    LOCALIZED_OBJECTIVE_QUESTION_BANK_01,
    materialize_module_01_question_bank,
)
from .module_02_ontologies_databases import (
    LOCALIZED_MODULE_02_ONTOLOGIES_DATABASES,
    LOCALIZED_OBJECTIVE_QUESTION_BANK_02,
    materialize_module_02_question_bank,
)
from .module_03_sequence_scoring_matching import (
    LOCALIZED_MODULE_03_SEQUENCE_SCORING_MATCHING,
    LOCALIZED_OBJECTIVE_QUESTION_BANK_03,
    materialize_module_03_question_bank,
)
from .module_04_pairwise_alignment import (
    LOCALIZED_MODULE_04_PAIRWISE_ALIGNMENT,
    LOCALIZED_OBJECTIVE_QUESTION_BANK_04,
    materialize_module_04_question_bank,
)
from .module_05_hidden_markov_models import (
    LOCALIZED_MODULE_05_HIDDEN_MARKOV_MODELS,
    LOCALIZED_OBJECTIVE_QUESTION_BANK_05,
    materialize_module_05_question_bank,
)
from .module_06_suffix_arrays_bwt_mapping import (
    LOCALIZED_MODULE_06_SUFFIX_ARRAYS_BWT_MAPPING as _RAW_LOCALIZED_MODULE_06,
)
from .module_06_suffix_arrays_bwt_mapping import (
    LOCALIZED_OBJECTIVE_QUESTION_BANK_06,
    materialize_module_06_question_bank,
)
from .module_07_operons_bacterial_genetics import (
    LOCALIZED_MODULE_07_OPERONS_BACTERIAL_GENETICS,
    LOCALIZED_OBJECTIVE_QUESTION_BANK_07,
    materialize_module_07_question_bank,
)
from .module_08_motif_discovery_em import (
    LOCALIZED_MODULE_08_MOTIF_DISCOVERY_EM as _RAW_LOCALIZED_MODULE_08,
)
from .module_08_motif_discovery_em import (
    LOCALIZED_OBJECTIVE_QUESTION_BANK_08,
    materialize_module_08_question_bank,
)
from .module_09_biological_networks_enrichment import (
    LOCALIZED_MODULE_09_BIOLOGICAL_NETWORKS_ENRICHMENT,
    LOCALIZED_OBJECTIVE_QUESTION_BANK_09,
    materialize_module_09_question_bank,
)
from .module_10_omics_learning_project import (
    LOCALIZED_MODULE_10_OMICS_LEARNING_PROJECT,
    LOCALIZED_OBJECTIVE_QUESTION_BANK_10,
    materialize_module_10_question_bank,
)

DM847_MODULE_SOURCE_AUDIT = update_hmm_bwt_audit(_BASE_DM847_MODULE_SOURCE_AUDIT)


def _replace_spanish(
    texts: tuple[LocalizedText, ...],
    spanish_values: tuple[str, ...],
) -> tuple[LocalizedText, ...]:
    """Replace only the Spanish member while preserving English and Danish identity."""
    if len(texts) != len(spanish_values):
        raise ValueError("Localized tutor correction must preserve item count.")
    return tuple(
        replace(text, spanish=spanish) for text, spanish in zip(texts, spanish_values, strict=True)
    )


_module_06_tutor = _RAW_LOCALIZED_MODULE_06.tutor_support
LOCALIZED_MODULE_06_SUFFIX_ARRAYS_BWT_MAPPING = replace(
    _RAW_LOCALIZED_MODULE_06,
    tutor_support=replace(
        _module_06_tutor,
        knowledge_fragments=_replace_spanish(
            _module_06_tutor.knowledge_fragments,
            (
                "El suffix array almacena posiciones.",
                "LCP mide prefijos compartidos.",
                "BWT requiere un centinela único.",
                "LF conserva el rango de ocurrencia.",
                "FM-index separa count y locate.",
                "El mapeo de lecturas requiere verificar candidatos.",
            ),
        ),
        common_misconceptions=_replace_spanish(
            _module_06_tutor.common_misconceptions,
            (
                "Almacenar sufijos completos.",
                "Usar varios centinelas.",
                "Confundir F y L.",
                "Tratar count como locate.",
                "Elegir arbitrariamente una posición con multimapping.",
                "Interpretar MAPQ como universal.",
            ),
        ),
        socratic_questions=_replace_spanish(
            _module_06_tutor.socratic_questions,
            (
                "¿Qué se almacena en el índice?",
                "¿El centinela es único?",
                "¿Qué significan los límites del intervalo?",
                "¿Se necesita count o locate?",
                "¿Cómo se manejan los mismatches?",
                "¿Cómo se reporta el multimapping?",
            ),
        ),
        grading_criteria=_replace_spanish(
            _module_06_tutor.grading_criteria,
            (
                "Construye suffix arrays y BWT correctos.",
                "Explica LF y backward search.",
                "Analiza los compromisos de memoria.",
                "Distingue count y locate.",
                "Diseña correctamente seed-and-extend.",
                "Conserva la incertidumbre del mapeo.",
            ),
        ),
        response_constraints=_replace_spanish(
            _module_06_tutor.response_constraints,
            (
                "No inventar coordenadas de mapeo.",
                "No ocultar multimapping.",
                "No asumir que MAPQ está calibrado universalmente.",
                "No recomendar construcciones ingenuas para genomas.",
                "Responder en el idioma activo.",
            ),
        ),
    ),
)

_module_08_tutor = _RAW_LOCALIZED_MODULE_08.tutor_support
LOCALIZED_MODULE_08_MOTIF_DISCOVERY_EM = replace(
    _RAW_LOCALIZED_MODULE_08,
    tutor_support=replace(
        _module_08_tutor,
        knowledge_fragments=_replace_spanish(
            _module_08_tutor.knowledge_fragments,
            (
                "Las PWM requieren pseudoconteos.",
                "La entropía mide incertidumbre.",
                "El score depende del modelo de fondo.",
                "El modelo de ocurrencia es un supuesto.",
                "EM encuentra óptimos locales.",
                "La validación requiere datos retenidos y evidencia externa.",
            ),
        ),
        common_misconceptions=_replace_spanish(
            _module_08_tutor.common_misconceptions,
            (
                "Omitir pseudoconteos.",
                "Asumir un fondo uniforme.",
                "Forzar OOPS cuando pueden faltar sitios.",
                "Usar una sola inicialización de EM.",
                "Seleccionar la anchura con los datos de prueba.",
                "Interpretar un logo como prueba funcional.",
            ),
        ),
        socratic_questions=_replace_spanish(
            _module_08_tutor.socratic_questions,
            (
                "¿Qué modelo de fondo se utiliza?",
                "¿Qué modelo de ocurrencia es apropiado?",
                "¿Cómo se selecciona la anchura?",
                "¿Cuántos reinicios se ejecutan?",
                "¿El motivo es estable?",
                "¿Qué evidencia externa existe?",
            ),
        ),
        grading_criteria=_replace_spanish(
            _module_08_tutor.grading_criteria,
            (
                "Construye y normaliza la PWM.",
                "Interpreta entropía e información.",
                "Formula log-odds frente al fondo correcto.",
                "Explica los pasos E y M.",
                "Gestiona los óptimos locales.",
                "Diseña una validación independiente.",
            ),
        ),
        response_constraints=_replace_spanish(
            _module_08_tutor.response_constraints,
            (
                "No inventar sitios de unión.",
                "No atribuir función basándose solo en una PWM.",
                "No ocultar el fondo ni los pseudoconteos.",
                "No usar motivos didácticos con fines clínicos.",
                "Responder en el idioma activo.",
            ),
        ),
    ),
)

(
    LOCALIZED_MODULE_01_MOLECULAR_INFORMATION,
    LOCALIZED_MODULE_02_ONTOLOGIES_DATABASES,
    LOCALIZED_MODULE_03_SEQUENCE_SCORING_MATCHING,
    LOCALIZED_MODULE_04_PAIRWISE_ALIGNMENT,
    LOCALIZED_MODULE_05_HIDDEN_MARKOV_MODELS,
    LOCALIZED_MODULE_06_SUFFIX_ARRAYS_BWT_MAPPING,
    LOCALIZED_MODULE_07_OPERONS_BACTERIAL_GENETICS,
    LOCALIZED_MODULE_08_MOTIF_DISCOVERY_EM,
    LOCALIZED_MODULE_09_BIOLOGICAL_NETWORKS_ENRICHMENT,
    LOCALIZED_MODULE_10_OMICS_LEARNING_PROJECT,
) = apply_hmm_bwt_extensions(
    apply_book_grounded_extensions(
        (
            LOCALIZED_MODULE_01_MOLECULAR_INFORMATION,
            LOCALIZED_MODULE_02_ONTOLOGIES_DATABASES,
            LOCALIZED_MODULE_03_SEQUENCE_SCORING_MATCHING,
            LOCALIZED_MODULE_04_PAIRWISE_ALIGNMENT,
            LOCALIZED_MODULE_05_HIDDEN_MARKOV_MODELS,
            LOCALIZED_MODULE_06_SUFFIX_ARRAYS_BWT_MAPPING,
            LOCALIZED_MODULE_07_OPERONS_BACTERIAL_GENETICS,
            LOCALIZED_MODULE_08_MOTIF_DISCOVERY_EM,
            LOCALIZED_MODULE_09_BIOLOGICAL_NETWORKS_ENRICHMENT,
            LOCALIZED_MODULE_10_OMICS_LEARNING_PROJECT,
        )
    )
)

_LOCALIZED_MODULES = (
    LOCALIZED_MODULE_01_MOLECULAR_INFORMATION,
    LOCALIZED_MODULE_02_ONTOLOGIES_DATABASES,
    LOCALIZED_MODULE_03_SEQUENCE_SCORING_MATCHING,
    LOCALIZED_MODULE_04_PAIRWISE_ALIGNMENT,
    LOCALIZED_MODULE_05_HIDDEN_MARKOV_MODELS,
    LOCALIZED_MODULE_06_SUFFIX_ARRAYS_BWT_MAPPING,
    LOCALIZED_MODULE_07_OPERONS_BACTERIAL_GENETICS,
    LOCALIZED_MODULE_08_MOTIF_DISCOVERY_EM,
    LOCALIZED_MODULE_09_BIOLOGICAL_NETWORKS_ENRICHMENT,
    LOCALIZED_MODULE_10_OMICS_LEARNING_PROJECT,
)

_LOCALIZED_OBJECTIVE_BANKS = (
    LOCALIZED_OBJECTIVE_QUESTION_BANK_01,
    LOCALIZED_OBJECTIVE_QUESTION_BANK_02,
    LOCALIZED_OBJECTIVE_QUESTION_BANK_03,
    LOCALIZED_OBJECTIVE_QUESTION_BANK_04,
    LOCALIZED_OBJECTIVE_QUESTION_BANK_05,
    LOCALIZED_OBJECTIVE_QUESTION_BANK_06,
    LOCALIZED_OBJECTIVE_QUESTION_BANK_07,
    LOCALIZED_OBJECTIVE_QUESTION_BANK_08,
    LOCALIZED_OBJECTIVE_QUESTION_BANK_09,
    LOCALIZED_OBJECTIVE_QUESTION_BANK_10,
)

_CONTENT_VERSIONS = (
    "1.0.0",
    "1.0.0",
    "1.1.0",
    "1.1.0",
    "1.1.0",
    "1.1.0",
    "1.0.0",
    "1.0.0",
    "1.0.0",
    "1.0.0",
)

LOCALIZED_BUNDLES = tuple(
    LocalizedModuleBundle(
        localized_module=module,
        localized_objective_question_bank=bank,
        content_version=version,
    )
    for module, bank, version in zip(
        _LOCALIZED_MODULES,
        _LOCALIZED_OBJECTIVE_BANKS,
        _CONTENT_VERSIONS,
        strict=True,
    )
)
validate_bundle_catalog(LOCALIZED_BUNDLES)

BUNDLES = tuple(bundle.materialize(AppLocale.SPANISH_SPAIN) for bundle in LOCALIZED_BUNDLES)
LOCALIZED_MODULES = tuple(bundle.localized_module for bundle in LOCALIZED_BUNDLES)
MODULES = tuple(bundle.module for bundle in BUNDLES)
OBJECTIVE_QUESTION_BANKS = {
    bundle.module.module_id: bundle.objective_question_bank for bundle in BUNDLES
}

MODULE_01_MOLECULAR_INFORMATION = BUNDLES[0].module
MODULE_02_ONTOLOGIES_DATABASES = BUNDLES[1].module
MODULE_03_SEQUENCE_SCORING_MATCHING = BUNDLES[2].module
MODULE_04_PAIRWISE_ALIGNMENT = BUNDLES[3].module
MODULE_05_HIDDEN_MARKOV_MODELS = BUNDLES[4].module
MODULE_06_SUFFIX_ARRAYS_BWT_MAPPING = BUNDLES[5].module
MODULE_07_OPERONS_BACTERIAL_GENETICS = BUNDLES[6].module
MODULE_08_MOTIF_DISCOVERY_EM = BUNDLES[7].module
MODULE_09_BIOLOGICAL_NETWORKS_ENRICHMENT = BUNDLES[8].module
MODULE_10_OMICS_LEARNING_PROJECT = BUNDLES[9].module

OBJECTIVE_QUESTION_BANK_01 = BUNDLES[0].objective_question_bank
OBJECTIVE_QUESTION_BANK_02 = BUNDLES[1].objective_question_bank
OBJECTIVE_QUESTION_BANK_03 = BUNDLES[2].objective_question_bank
OBJECTIVE_QUESTION_BANK_04 = BUNDLES[3].objective_question_bank
OBJECTIVE_QUESTION_BANK_05 = BUNDLES[4].objective_question_bank
OBJECTIVE_QUESTION_BANK_06 = BUNDLES[5].objective_question_bank
OBJECTIVE_QUESTION_BANK_07 = BUNDLES[6].objective_question_bank
OBJECTIVE_QUESTION_BANK_08 = BUNDLES[7].objective_question_bank
OBJECTIVE_QUESTION_BANK_09 = BUNDLES[8].objective_question_bank
OBJECTIVE_QUESTION_BANK_10 = BUNDLES[9].objective_question_bank

__all__ = [
    "BUNDLES",
    "DM847_BOOK_SOURCES",
    "DM847_MODULE_SOURCE_AUDIT",
    "LOCALIZED_BUNDLES",
    "LOCALIZED_MODULES",
    "LOCALIZED_MODULE_01_MOLECULAR_INFORMATION",
    "LOCALIZED_MODULE_02_ONTOLOGIES_DATABASES",
    "LOCALIZED_MODULE_03_SEQUENCE_SCORING_MATCHING",
    "LOCALIZED_MODULE_04_PAIRWISE_ALIGNMENT",
    "LOCALIZED_MODULE_05_HIDDEN_MARKOV_MODELS",
    "LOCALIZED_MODULE_06_SUFFIX_ARRAYS_BWT_MAPPING",
    "LOCALIZED_MODULE_07_OPERONS_BACTERIAL_GENETICS",
    "LOCALIZED_MODULE_08_MOTIF_DISCOVERY_EM",
    "LOCALIZED_MODULE_09_BIOLOGICAL_NETWORKS_ENRICHMENT",
    "LOCALIZED_MODULE_10_OMICS_LEARNING_PROJECT",
    "LOCALIZED_OBJECTIVE_QUESTION_BANK_01",
    "LOCALIZED_OBJECTIVE_QUESTION_BANK_02",
    "LOCALIZED_OBJECTIVE_QUESTION_BANK_03",
    "LOCALIZED_OBJECTIVE_QUESTION_BANK_04",
    "LOCALIZED_OBJECTIVE_QUESTION_BANK_05",
    "LOCALIZED_OBJECTIVE_QUESTION_BANK_06",
    "LOCALIZED_OBJECTIVE_QUESTION_BANK_07",
    "LOCALIZED_OBJECTIVE_QUESTION_BANK_08",
    "LOCALIZED_OBJECTIVE_QUESTION_BANK_09",
    "LOCALIZED_OBJECTIVE_QUESTION_BANK_10",
    "MODULES",
    "MODULE_01_MOLECULAR_INFORMATION",
    "MODULE_02_ONTOLOGIES_DATABASES",
    "MODULE_03_SEQUENCE_SCORING_MATCHING",
    "MODULE_04_PAIRWISE_ALIGNMENT",
    "MODULE_05_HIDDEN_MARKOV_MODELS",
    "MODULE_06_SUFFIX_ARRAYS_BWT_MAPPING",
    "MODULE_07_OPERONS_BACTERIAL_GENETICS",
    "MODULE_08_MOTIF_DISCOVERY_EM",
    "MODULE_09_BIOLOGICAL_NETWORKS_ENRICHMENT",
    "MODULE_10_OMICS_LEARNING_PROJECT",
    "OBJECTIVE_QUESTION_BANKS",
    "OBJECTIVE_QUESTION_BANK_01",
    "OBJECTIVE_QUESTION_BANK_02",
    "OBJECTIVE_QUESTION_BANK_03",
    "OBJECTIVE_QUESTION_BANK_04",
    "OBJECTIVE_QUESTION_BANK_05",
    "OBJECTIVE_QUESTION_BANK_06",
    "OBJECTIVE_QUESTION_BANK_07",
    "OBJECTIVE_QUESTION_BANK_08",
    "OBJECTIVE_QUESTION_BANK_09",
    "OBJECTIVE_QUESTION_BANK_10",
    "apply_book_grounded_extensions",
    "apply_hmm_bwt_extensions",
    "materialize_module_01_question_bank",
    "materialize_module_02_question_bank",
    "materialize_module_03_question_bank",
    "materialize_module_04_question_bank",
    "materialize_module_05_question_bank",
    "materialize_module_06_question_bank",
    "materialize_module_07_question_bank",
    "materialize_module_08_question_bank",
    "materialize_module_09_question_bank",
    "materialize_module_10_question_bank",
]
