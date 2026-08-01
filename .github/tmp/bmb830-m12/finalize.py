from __future__ import annotations

import shutil
from pathlib import Path

ROOT = Path.cwd()


def replace_once(path: Path, old: str, new: str) -> None:
    text = path.read_text(encoding="utf-8")
    count = text.count(old)
    if count != 1:
        raise SystemExit(f"Expected one match in {path}; found {count}: {old[:100]!r}")
    path.write_text(text.replace(old, new), encoding="utf-8")


def replace_n(path: Path, old: str, new: str, expected: int) -> None:
    text = path.read_text(encoding="utf-8")
    count = text.count(old)
    if count != expected:
        raise SystemExit(f"Expected {expected} matches in {path}; found {count}: {old[:100]!r}")
    path.write_text(text.replace(old, new), encoding="utf-8")


init = ROOT / "src/computational_biomedicine_study_hub/content/bmb830/__init__.py"
replace_once(
    init,
    '''from .module_11_intro_multivariate import (
    LOCALIZED_MODULE_11_INTRO_MULTIVARIATE,
    LOCALIZED_OBJECTIVE_QUESTION_BANK_11,
    materialize_module_11_question_bank,
)
''',
    '''from .module_11_intro_multivariate import (
    LOCALIZED_MODULE_11_INTRO_MULTIVARIATE,
    LOCALIZED_OBJECTIVE_QUESTION_BANK_11,
    materialize_module_11_question_bank,
)
from .module_12_high_dimensional_case import (
    LOCALIZED_MODULE_12_HIGH_DIMENSIONAL_CASE,
    LOCALIZED_OBJECTIVE_QUESTION_BANK_12,
    materialize_module_12_question_bank,
)
''',
)
replace_once(
    init,
    '''    LocalizedModuleBundle(
        LOCALIZED_MODULE_11_INTRO_MULTIVARIATE,
        LOCALIZED_OBJECTIVE_QUESTION_BANK_11,
        "1.0.0",
    ),
)''',
    '''    LocalizedModuleBundle(
        LOCALIZED_MODULE_11_INTRO_MULTIVARIATE,
        LOCALIZED_OBJECTIVE_QUESTION_BANK_11,
        "1.0.0",
    ),
    LocalizedModuleBundle(
        LOCALIZED_MODULE_12_HIGH_DIMENSIONAL_CASE,
        LOCALIZED_OBJECTIVE_QUESTION_BANK_12,
        "1.0.0",
    ),
)''',
)
replace_once(
    init,
    "MODULE_11_INTRO_MULTIVARIATE = BUNDLES[10].module\n",
    "MODULE_11_INTRO_MULTIVARIATE = BUNDLES[10].module\nMODULE_12_HIGH_DIMENSIONAL_CASE = BUNDLES[11].module\n",
)
replace_once(
    init,
    "OBJECTIVE_QUESTION_BANK_11 = BUNDLES[10].objective_question_bank\n",
    "OBJECTIVE_QUESTION_BANK_11 = BUNDLES[10].objective_question_bank\nOBJECTIVE_QUESTION_BANK_12 = BUNDLES[11].objective_question_bank\n",
)
for old, new in (
    ('    "LOCALIZED_MODULE_11_INTRO_MULTIVARIATE",\n', '    "LOCALIZED_MODULE_11_INTRO_MULTIVARIATE",\n    "LOCALIZED_MODULE_12_HIGH_DIMENSIONAL_CASE",\n'),
    ('    "LOCALIZED_OBJECTIVE_QUESTION_BANK_11",\n', '    "LOCALIZED_OBJECTIVE_QUESTION_BANK_11",\n    "LOCALIZED_OBJECTIVE_QUESTION_BANK_12",\n'),
    ('    "MODULE_11_INTRO_MULTIVARIATE",\n', '    "MODULE_11_INTRO_MULTIVARIATE",\n    "MODULE_12_HIGH_DIMENSIONAL_CASE",\n'),
    ('    "OBJECTIVE_QUESTION_BANK_11",\n', '    "OBJECTIVE_QUESTION_BANK_11",\n    "OBJECTIVE_QUESTION_BANK_12",\n'),
    ('    "materialize_module_11_question_bank",\n', '    "materialize_module_11_question_bank",\n    "materialize_module_12_question_bank",\n'),
):
    replace_once(init, old, new)

core = ROOT / "tests/test_bmb830_core_modules.py"
replace_once(
    core,
    "def test_bmb830_registers_eleven_complete_modules_in_order() -> None:\n",
    "def test_bmb830_registers_twelve_complete_modules_in_order() -> None:\n",
)
replace_once(core, '        "bmb830.m11",\n    )', '        "bmb830.m11",\n        "bmb830.m12",\n    )')
replace_once(
    core,
    "    assert len(BUNDLES) == len(LOCALIZED_BUNDLES) == 11\n",
    "    assert len(BUNDLES) == len(LOCALIZED_BUNDLES) == 12\n",
)
replace_once(core, '        "bmb830.m11",\n    }', '        "bmb830.m11",\n        "bmb830.m12",\n    }')
replace_once(
    core,
    "    assert sum(len(bundle.objective_question_bank) for bundle in BUNDLES) == 176\n",
    "    assert sum(len(bundle.objective_question_bank) for bundle in BUNDLES) == 192\n",
)

lazy = ROOT / "tests/test_bmb830_lazy_loading.py"
replace_once(lazy, "    MODULE_11_INTRO_MULTIVARIATE,\n", "    MODULE_12_HIGH_DIMENSIONAL_CASE,\n")
replace_once(lazy, "page.module_count == 11", "page.module_count == 12")
replace_once(lazy, "not page.has_constructed_reader(10)", "not page.has_constructed_reader(11)")
replace_n(lazy, 'page.select_module_by_id("bmb830.m11")', 'page.select_module_by_id("bmb830.m12")', 2)
replace_once(
    lazy,
    "final_reader.module is MODULE_11_INTRO_MULTIVARIATE",
    "final_reader.module is MODULE_12_HIGH_DIMENSIONAL_CASE",
)
replace_once(lazy, "not page.select_module(11)", "not page.select_module(12)")
replace_once(
    lazy,
    'assert page.reader.module.title.startswith("Introduktion")',
    'assert page.reader.module.title.startswith("Individuel")',
)

audit = ROOT / "src/computational_biomedicine_study_hub/content/bmb830/official_coverage.py"
replace_once(
    audit,
    '    "bmb830.m11",\n)\n\nOFFICIAL_BMB830_REQUIREMENTS',
    '    "bmb830.m11",\n    "bmb830.m12",\n)\n\nOFFICIAL_BMB830_REQUIREMENTS',
)
replace_once(
    audit,
    '''        "The course provides an individual workflow from R foundations through model validation, "
        "but most worked data remain compact teaching examples rather than one integrated biological data set.",
        "Add an individually completed biological-data case with provenance, quality control, "
        "visualisation, modelling, diagnostics, interpretation, and reproducible reporting.",''',
    '''        "An integrated individual synthetic proteomics case now joins provenance, quality control, "
        "multivariate exploration, feature screening, and reporting, but it is deliberately not presented "
        "as an externally sourced biological data set.",
        "Add a source-bounded real biological data case when suitable public data and provenance are selected.",''',
)
replace_once(
    audit,
    '("bmb830.m01", "bmb830.m02", "bmb830.m06", "bmb830.m08", "bmb830.m10", "bmb830.m11"),',
    '("bmb830.m01", "bmb830.m02", "bmb830.m06", "bmb830.m08", "bmb830.m10", "bmb830.m11", "bmb830.m12"),',
)
replace_once(
    audit,
    '''        "Standard analysis and leakage-safe reasoning are covered, but no laboratory yet exercises "
        "memory-aware processing or feature screening on a realistically large matrix.",
        "Add an individual high-dimensional biological matrix laboratory with dimensions, missingness, "
        "filtering, feature summaries, and leakage-safe validation.",''',
    '''        "The bounded p-greater-than-n proteomics case exercises dimensions, missingness, filtering, "
        "feature summaries, PCA, and training-only screening, but 48 by 240 remains a teaching matrix "
        "rather than a realistically large data amount.",
        "Add memory-aware processing of a substantially larger public biological matrix.",''',
)
replace_once(
    audit,
    '''            "bmb830.m11",
        ),
        CoverageStatus.PARTIAL,
        "The course teaches the concepts required for critique and includes oral explanations, but "''',
    '''            "bmb830.m11",
            "bmb830.m12",
        ),
        CoverageStatus.PARTIAL,
        "The course teaches the concepts required for critique and includes oral explanations, but "''',
)
replace_n(
    audit,
    '("bmb830.m04", "bmb830.m05", *_REGRESSION_MODULES, "bmb830.m11"),\n        CoverageStatus.PARTIAL,',
    '("bmb830.m04", "bmb830.m05", *_REGRESSION_MODULES, "bmb830.m11", "bmb830.m12"),\n        CoverageStatus.PARTIAL,',
    2,
)
replace_once(
    audit,
    '''        ("bmb830.m02", "bmb830.m06", "bmb830.m08", "bmb830.m10", "bmb830.m11"),
        CoverageStatus.PARTIAL,
        "Biological framing is strong, but most examples remain compact teaching data rather than a "
        "realistic end-to-end molecular or clinical data set.",
        "Add a provenance-preserving individual biological case without fabricating an SDU assignment.",''',
    '''        ("bmb830.m02", "bmb830.m06", "bmb830.m08", "bmb830.m10", "bmb830.m11", "bmb830.m12"),
        CoverageStatus.PARTIAL,
        "The synthetic proteomics case provides realistic metadata, missingness, batch structure, and "
        "end-to-end decisions, but synthetic provenance cannot replace analysis of an external biological data set.",
        "Add a provenance-preserving public biological case without fabricating an SDU assignment.",''',
)
replace_once(
    audit,
    '''        ("bmb830.m01", "bmb830.m02", "bmb830.m08", "bmb830.m10", "bmb830.m11"),
        CoverageStatus.PARTIAL,
        "The conceptual safeguards exist, but computational scale and high-dimensional feature "
        "workflows are not yet exercised.",
        "Add a bounded large-matrix laboratory and explicit patient-versus-feature dimension checks.",''',
    '''        ("bmb830.m01", "bmb830.m02", "bmb830.m08", "bmb830.m10", "bmb830.m11", "bmb830.m12"),
        CoverageStatus.COVERED,
        "The individual proteomics case explicitly exercises a p-greater-than-n matrix, dimension and "
        "memory checks, feature-level missingness, filtering, PCA, and training-only feature screening.",''',
)
replace_once(
    audit,
    '''        ("bmb830.m11",),
        CoverageStatus.COVERED,
        "The module connects matrix orientation and preprocessing to PCA, hierarchical "''',
    '''        ("bmb830.m11", "bmb830.m12"),
        CoverageStatus.COVERED,
        "The modules connect matrix orientation and preprocessing to PCA, hierarchical "''',
)

coverage_test = ROOT / "tests/test_bmb830_official_coverage.py"
replace_once(
    coverage_test,
    "assert rows[MasterCriterionKind.SCALE].criterion.status is CoverageStatus.PARTIAL",
    "assert rows[MasterCriterionKind.SCALE].criterion.status is CoverageStatus.COVERED",
)
replace_once(coverage_test, "assert summary.covered == 3", "assert summary.covered == 4")
replace_once(coverage_test, "assert summary.partial == 4", "assert summary.partial == 3")

readme = ROOT / "README.md"
replace_once(readme, "  - 10 complete modules\n", "  - 12 complete modules\n")
replace_once(
    readme,
    "  - multivariate matrices, centring, scaling, distances, PCA, scores, loadings, explained variance, hierarchical clustering, and stability analysis\n",
    "  - multivariate matrices, centring, scaling, distances, PCA, scores, loadings, explained variance, hierarchical clustering, and stability analysis\n"
    "  - individual synthetic proteomics case with provenance, p-greater-than-n quality control, missingness, filtering, imputation, batch assessment, leakage-safe feature screening, and reproducible reporting\n",
)
replace_once(readme, "  - 176 stable objective-bank questions\n", "  - 192 stable objective-bank questions\n")
replace_once(
    readme,
    "The public multivariate requirement is now covered by an individual introductory module. Realistic large biological data, detailed figure-building practice, structured publication appraisal, and a complete individual oral-exam rehearsal remain partial until their official or source materials are available.",
    "The public multivariate requirement is covered, and an individual bounded high-dimensional proteomics case now exercises the complete exploratory workflow. A substantially larger externally sourced biological data set, detailed figure-building practice, structured publication appraisal, and a complete individual oral-exam rehearsal remain partial until suitable source materials are selected or become available.",
)
replace_once(
    readme,
    "Active development. DM857 and DM847 provide complete academic course implementations. BMB830 contains eleven complete modules covering foundations through introductory multivariate analysis. The official multivariate gap is closed, while realistic large biological data, detailed visualisation practice, publication appraisal, and full individual oral-exam rehearsal remain partial. Shared flashcard, glossary, search, notes, export, backup, and distribution workflows remain under development. Group-presentation rehearsal is intentionally outside the application scope.",
    "Active development. DM857 and DM847 provide complete academic course implementations. BMB830 contains twelve complete modules covering foundations through an individual high-dimensional proteomics case. High-dimensional p-greater-than-n workflow readiness is now covered, while a substantially larger externally sourced biological data set, detailed visualisation practice, publication appraisal, and full individual oral-exam rehearsal remain partial. Shared flashcard, glossary, search, notes, export, backup, and distribution workflows remain under development. Group-presentation rehearsal is intentionally outside the application scope.",
)

shutil.rmtree(ROOT / ".github/tmp/bmb830-m12")
for workflow in (
    ROOT / ".github/workflows/bmb830-m12-sync.yml",
    ROOT / ".github/workflows/bmb830-m12-pr-sync.yml",
):
    if workflow.exists():
        workflow.unlink()
