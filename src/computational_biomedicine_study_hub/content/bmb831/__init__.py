"""Trilingual authored content and runtime bundles for BMB831."""

from __future__ import annotations

from dataclasses import replace

from ...i18n import AppLocale
from ..bundles import LocalizedModuleBundle, validate_bundle_catalog
from ..localized_models import LocalizedLearningModule, LocalizedText
from .module_01_synthea_workflows import (
    LOCALIZED_MODULE_01_SYNTHEA_WORKFLOWS,
    LOCALIZED_OBJECTIVE_QUESTION_BANK_01,
    materialize_module_01_question_bank,
)
from .module_02_omics_matrices_qc import (
    LOCALIZED_MODULE_02_OMICS_MATRICES_QC,
    LOCALIZED_OBJECTIVE_QUESTION_BANK_02,
    materialize_module_02_question_bank,
)
from .module_03_differential_modeling import (
    LOCALIZED_MODULE_03_DIFFERENTIAL_MODELING,
    LOCALIZED_OBJECTIVE_QUESTION_BANK_03,
    materialize_module_03_question_bank,
)
from .module_04_multivariate_omics import (
    LOCALIZED_MODULE_04_MULTIVARIATE_OMICS,
    LOCALIZED_OBJECTIVE_QUESTION_BANK_04,
    materialize_module_04_question_bank,
)
from .module_05_advanced_visualization import (
    LOCALIZED_MODULE_05_ADVANCED_VISUALIZATION,
    LOCALIZED_OBJECTIVE_QUESTION_BANK_05,
    materialize_module_05_question_bank,
)
from .module_06_public_omics_workflows import (
    LOCALIZED_MODULE_06_PUBLIC_OMICS_WORKFLOWS,
    LOCALIZED_OBJECTIVE_QUESTION_BANK_06,
    materialize_module_06_question_bank,
)
from .module_07_protein_characterization import (
    LOCALIZED_MODULE_07_PROTEIN_CHARACTERIZATION,
    LOCALIZED_OBJECTIVE_QUESTION_BANK_07,
    materialize_module_07_question_bank,
)
from .module_08_biological_interpretation import (
    LOCALIZED_MODULE_08_BIOLOGICAL_INTERPRETATION,
    LOCALIZED_OBJECTIVE_QUESTION_BANK_08,
    materialize_module_08_question_bank,
)
from .module_09_publication_report import (
    LOCALIZED_MODULE_09_PUBLICATION_REPORT,
    LOCALIZED_OBJECTIVE_QUESTION_BANK_09,
    materialize_module_09_question_bank,
)


def _correct_public_omics_sources(
    module: LocalizedLearningModule,
) -> LocalizedLearningModule:
    """Repair the canonical limma source URL before bundle materialization."""

    corrected_sources = tuple(
        source.replace("/limpa.html", "/limma.html")
        for source in module.tutor_support.source_basis
    )
    return replace(
        module,
        tutor_support=replace(module.tutor_support, source_basis=corrected_sources),
    )


def _correct_protein_hydropathy_example(
    module: LocalizedLearningModule,
) -> LocalizedLearningModule:
    """Align M07.e02 prose and expected output with its executable R code."""

    corrected_examples = []
    found = False
    for example in module.worked_examples:
        if example.example_id != "m07.e02":
            corrected_examples.append(example)
            continue
        found = True
        corrected_examples.append(
            replace(
                example,
                expected_output=LocalizedText(
                    spanish="best_start=5\nbest_score=3.60",
                    english="best_start=5\nbest_score=3.60",
                    danish="best_start=5\nbest_score=3.60",
                ),
                explanation=LocalizedText(
                    spanish=(
                        "La ventana ILMV inicia en la posición cinco y maximiza la escala "
                        "ilustrativa; no confirma por sí sola una hélice transmembrana."
                    ),
                    english=(
                        "The ILMV window starts at position five and maximizes the illustrative "
                        "scale; it does not by itself confirm a transmembrane helix."
                    ),
                    danish=(
                        "ILMV-vinduet starter ved position fem og maksimerer den illustrative "
                        "skala; det bekræfter ikke i sig selv en transmembranhelix."
                    ),
                ),
            )
        )
    if not found:
        raise ValueError("BMB831 module 7 requires worked example m07.e02.")
    return replace(module, worked_examples=tuple(corrected_examples))


LOCALIZED_MODULE_06_PUBLIC_OMICS_WORKFLOWS = _correct_public_omics_sources(
    LOCALIZED_MODULE_06_PUBLIC_OMICS_WORKFLOWS
)
LOCALIZED_MODULE_07_PROTEIN_CHARACTERIZATION = _correct_protein_hydropathy_example(
    LOCALIZED_MODULE_07_PROTEIN_CHARACTERIZATION
)

LOCALIZED_BUNDLES = (
    LocalizedModuleBundle(
        LOCALIZED_MODULE_01_SYNTHEA_WORKFLOWS,
        LOCALIZED_OBJECTIVE_QUESTION_BANK_01,
        "1.0.0",
    ),
    LocalizedModuleBundle(
        LOCALIZED_MODULE_02_OMICS_MATRICES_QC,
        LOCALIZED_OBJECTIVE_QUESTION_BANK_02,
        "1.0.0",
    ),
    LocalizedModuleBundle(
        LOCALIZED_MODULE_03_DIFFERENTIAL_MODELING,
        LOCALIZED_OBJECTIVE_QUESTION_BANK_03,
        "1.0.0",
    ),
    LocalizedModuleBundle(
        LOCALIZED_MODULE_04_MULTIVARIATE_OMICS,
        LOCALIZED_OBJECTIVE_QUESTION_BANK_04,
        "1.0.0",
    ),
    LocalizedModuleBundle(
        LOCALIZED_MODULE_05_ADVANCED_VISUALIZATION,
        LOCALIZED_OBJECTIVE_QUESTION_BANK_05,
        "1.0.0",
    ),
    LocalizedModuleBundle(
        LOCALIZED_MODULE_06_PUBLIC_OMICS_WORKFLOWS,
        LOCALIZED_OBJECTIVE_QUESTION_BANK_06,
        "1.0.0",
    ),
    LocalizedModuleBundle(
        LOCALIZED_MODULE_07_PROTEIN_CHARACTERIZATION,
        LOCALIZED_OBJECTIVE_QUESTION_BANK_07,
        "1.0.0",
    ),
    LocalizedModuleBundle(
        LOCALIZED_MODULE_08_BIOLOGICAL_INTERPRETATION,
        LOCALIZED_OBJECTIVE_QUESTION_BANK_08,
        "1.0.0",
    ),
    LocalizedModuleBundle(
        LOCALIZED_MODULE_09_PUBLICATION_REPORT,
        LOCALIZED_OBJECTIVE_QUESTION_BANK_09,
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

MODULE_01_SYNTHEA_WORKFLOWS = BUNDLES[0].module
MODULE_02_OMICS_MATRICES_QC = BUNDLES[1].module
MODULE_03_DIFFERENTIAL_MODELING = BUNDLES[2].module
MODULE_04_MULTIVARIATE_OMICS = BUNDLES[3].module
MODULE_05_ADVANCED_VISUALIZATION = BUNDLES[4].module
MODULE_06_PUBLIC_OMICS_WORKFLOWS = BUNDLES[5].module
MODULE_07_PROTEIN_CHARACTERIZATION = BUNDLES[6].module
MODULE_08_BIOLOGICAL_INTERPRETATION = BUNDLES[7].module
MODULE_09_PUBLICATION_REPORT = BUNDLES[8].module

OBJECTIVE_QUESTION_BANK_01 = BUNDLES[0].objective_question_bank
OBJECTIVE_QUESTION_BANK_02 = BUNDLES[1].objective_question_bank
OBJECTIVE_QUESTION_BANK_03 = BUNDLES[2].objective_question_bank
OBJECTIVE_QUESTION_BANK_04 = BUNDLES[3].objective_question_bank
OBJECTIVE_QUESTION_BANK_05 = BUNDLES[4].objective_question_bank
OBJECTIVE_QUESTION_BANK_06 = BUNDLES[5].objective_question_bank
OBJECTIVE_QUESTION_BANK_07 = BUNDLES[6].objective_question_bank
OBJECTIVE_QUESTION_BANK_08 = BUNDLES[7].objective_question_bank
OBJECTIVE_QUESTION_BANK_09 = BUNDLES[8].objective_question_bank

__all__ = [
    "BUNDLES",
    "LOCALIZED_BUNDLES",
    "LOCALIZED_MODULES",
    "LOCALIZED_MODULE_01_SYNTHEA_WORKFLOWS",
    "LOCALIZED_MODULE_02_OMICS_MATRICES_QC",
    "LOCALIZED_MODULE_03_DIFFERENTIAL_MODELING",
    "LOCALIZED_MODULE_04_MULTIVARIATE_OMICS",
    "LOCALIZED_MODULE_05_ADVANCED_VISUALIZATION",
    "LOCALIZED_MODULE_06_PUBLIC_OMICS_WORKFLOWS",
    "LOCALIZED_MODULE_07_PROTEIN_CHARACTERIZATION",
    "LOCALIZED_MODULE_08_BIOLOGICAL_INTERPRETATION",
    "LOCALIZED_MODULE_09_PUBLICATION_REPORT",
    "LOCALIZED_OBJECTIVE_QUESTION_BANK_01",
    "LOCALIZED_OBJECTIVE_QUESTION_BANK_02",
    "LOCALIZED_OBJECTIVE_QUESTION_BANK_03",
    "LOCALIZED_OBJECTIVE_QUESTION_BANK_04",
    "LOCALIZED_OBJECTIVE_QUESTION_BANK_05",
    "LOCALIZED_OBJECTIVE_QUESTION_BANK_06",
    "LOCALIZED_OBJECTIVE_QUESTION_BANK_07",
    "LOCALIZED_OBJECTIVE_QUESTION_BANK_08",
    "LOCALIZED_OBJECTIVE_QUESTION_BANK_09",
    "MODULES",
    "MODULE_01_SYNTHEA_WORKFLOWS",
    "MODULE_02_OMICS_MATRICES_QC",
    "MODULE_03_DIFFERENTIAL_MODELING",
    "MODULE_04_MULTIVARIATE_OMICS",
    "MODULE_05_ADVANCED_VISUALIZATION",
    "MODULE_06_PUBLIC_OMICS_WORKFLOWS",
    "MODULE_07_PROTEIN_CHARACTERIZATION",
    "MODULE_08_BIOLOGICAL_INTERPRETATION",
    "MODULE_09_PUBLICATION_REPORT",
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
    "materialize_module_01_question_bank",
    "materialize_module_02_question_bank",
    "materialize_module_03_question_bank",
    "materialize_module_04_question_bank",
    "materialize_module_05_question_bank",
    "materialize_module_06_question_bank",
    "materialize_module_07_question_bank",
    "materialize_module_08_question_bank",
    "materialize_module_09_question_bank",
]
