"""Complete trilingual authored content and validated runtime bundles for DM847."""

from __future__ import annotations

from ...i18n import AppLocale
from ..bundles import LocalizedModuleBundle, validate_bundle_catalog
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
    LOCALIZED_MODULE_06_SUFFIX_ARRAYS_BWT_MAPPING,
    LOCALIZED_OBJECTIVE_QUESTION_BANK_06,
    materialize_module_06_question_bank,
)
from .module_07_operons_bacterial_genetics import (
    LOCALIZED_MODULE_07_OPERONS_BACTERIAL_GENETICS,
    LOCALIZED_OBJECTIVE_QUESTION_BANK_07,
    materialize_module_07_question_bank,
)
from .module_08_motif_discovery_em import (
    LOCALIZED_MODULE_08_MOTIF_DISCOVERY_EM,
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

LOCALIZED_BUNDLES = (
    LocalizedModuleBundle(
        LOCALIZED_MODULE_01_MOLECULAR_INFORMATION,
        LOCALIZED_OBJECTIVE_QUESTION_BANK_01,
        "1.0.0",
    ),
    LocalizedModuleBundle(
        LOCALIZED_MODULE_02_ONTOLOGIES_DATABASES,
        LOCALIZED_OBJECTIVE_QUESTION_BANK_02,
        "1.0.0",
    ),
    LocalizedModuleBundle(
        LOCALIZED_MODULE_03_SEQUENCE_SCORING_MATCHING,
        LOCALIZED_OBJECTIVE_QUESTION_BANK_03,
        "1.0.0",
    ),
    LocalizedModuleBundle(
        LOCALIZED_MODULE_04_PAIRWISE_ALIGNMENT,
        LOCALIZED_OBJECTIVE_QUESTION_BANK_04,
        "1.0.0",
    ),
    LocalizedModuleBundle(
        LOCALIZED_MODULE_05_HIDDEN_MARKOV_MODELS,
        LOCALIZED_OBJECTIVE_QUESTION_BANK_05,
        "1.0.0",
    ),
    LocalizedModuleBundle(
        LOCALIZED_MODULE_06_SUFFIX_ARRAYS_BWT_MAPPING,
        LOCALIZED_OBJECTIVE_QUESTION_BANK_06,
        "1.0.0",
    ),
    LocalizedModuleBundle(
        LOCALIZED_MODULE_07_OPERONS_BACTERIAL_GENETICS,
        LOCALIZED_OBJECTIVE_QUESTION_BANK_07,
        "1.0.0",
    ),
    LocalizedModuleBundle(
        LOCALIZED_MODULE_08_MOTIF_DISCOVERY_EM,
        LOCALIZED_OBJECTIVE_QUESTION_BANK_08,
        "1.0.0",
    ),
    LocalizedModuleBundle(
        LOCALIZED_MODULE_09_BIOLOGICAL_NETWORKS_ENRICHMENT,
        LOCALIZED_OBJECTIVE_QUESTION_BANK_09,
        "1.0.0",
    ),
    LocalizedModuleBundle(
        LOCALIZED_MODULE_10_OMICS_LEARNING_PROJECT,
        LOCALIZED_OBJECTIVE_QUESTION_BANK_10,
        "1.0.0",
    ),
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
