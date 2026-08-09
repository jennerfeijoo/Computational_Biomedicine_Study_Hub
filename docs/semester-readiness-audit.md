# First-semester autonomous-study readiness audit

## Scope

This document is the current engineering and curriculum gate for using the Study Hub as the principal self-study system for the SDU first semester, together with JupyterLab and RStudio.

The target is not to reproduce SDU's private Itslearning materials, attendance requirements, group dynamics, or official grading. Those remain institutional components. The target is to make the **academic learning pathway** self-sufficient: theory, deliberate practice, executable work, assessment, datasets, transfer, and reproducibility.

## Architecture decision

Keep the responsibilities separate:

- **Study Hub:** curriculum, explanations, retrieval practice, formative assessment, progress, tutor context, source/provenance contracts and integrated assignments.
- **JupyterLab:** Python and algorithmic laboratory for DM857/DM847.
- **RStudio:** R, statistics, Bioconductor and omics laboratory for BMB830/BMB831.

The Study Hub should not become a replacement IDE.

## Changes implemented in this release

### DM847 coverage gaps

1. **Suffix trees** were added explicitly to M06 alongside suffix arrays, LCP, BWT and FM-index concepts.
2. **Bimodal peak calling** was added explicitly to M10, including strand-aware signal interpretation, control/QC boundaries and a reproducible mini-pipeline design task.
3. Each addition has a trilingual concept, worked example, independent practice, objective-level assessment item and tutor source basis.

### Assessment integration

The top-level **Evaluación / Assessment / Evaluering** workspace now exposes:

- DM847 written assessment plus a timed assessment simulation in the same DM847 workspace;
- DM857 capstone;
- BMB830 assessment;
- BMB831 report;
- an integrated first-semester capstone evidence tracker.

The DM847 simulation uses the existing 30-minute plan, eight reasoning domains, follow-ups and transparent evidence extraction. It explicitly flags that mentor/human review remains necessary.

### Real-data pathway

The public-omics registry now includes:

- Bioconductor `airway` for compact RNA-seq practice;
- NCBI GEO `GSE305298` for human bulk RNA-seq design and differential analysis;
- UCSC Xena's TCGA/TARGET/GTEx cohort for integration-scale feature selection and multivariate work;
- the existing ProteomeXchange teaching contract.

The registry remains snapshot-first: accession metadata is not treated as a reproducible dataset until the learner records the exact local files/version, metadata and SHA-256 manifest.

### Executable capstone evidence

The integrated capstone evidence tracker now has an explicit artifact contract in `learning/semester_capstone_artifacts.py`.

Each artifact records:

```text
artifact ID
semester stage
execution environment
artifact kind
portable relative path
description
```

The contract validates:

- unique artifact IDs;
- relative, workspace-safe paths;
- file-extension compatibility with the declared artifact kind;
- JupyterLab-compatible Python/notebook evidence;
- RStudio-compatible R/RMarkdown evidence.

The Study Hub still does **not** execute arbitrary learner notebooks or scripts. It records and validates the evidence reference; execution remains in JupyterLab/RStudio.

### Reproducibility boundary

Every real-data laboratory should retain:

```text
source accession
version/release
sample metadata
feature annotation
analysis-ready input
parameters
software versions
SHA-256 manifest
dataset card
analysis script/notebook
```

## Cross-course integration target

The semester is treated as one competency chain:

```text
DM857  ->  DM847  ->  BMB830  ->  BMB831
Python    algorithms  statistics   omics
   \\          |           |          /
    \\---------+-----------+---------/
              integrated biomedical problem
```

The integrated capstone now records observable evidence for: biological question, computational formulation, algorithmic solution, statistical analysis, omics workflow, biological interpretation and reproducible report. Evidence can additionally reference portable JupyterLab/RStudio artifacts.

## DM857 source-grounded verification boundary

The source-review record is being kept separate from the readiness gate. The uploaded Guttag 3rd edition contains dedicated chapters on functions, structured types and mutability, recursion, modules/files, testing/debugging, exceptions/assertions, classes/OOP, algorithmic complexity and data structures. fileciteturn202file0L1-L1

The uploaded Think Python 3rd edition explicitly emphasizes programming practice, exercises, recursion, core data structures, files, OOP, testing/debugging and Jupyter-based executable learning. fileciteturn202file8L1-L1

The repository already contains book-grounded DM857 extension modules for foundations, strings/mappings, trees, ADTs, OOP and scientific libraries. The historical `pending` table in `docs/dm857-book-grounded-audit.md` therefore remains a record of what was documented in that older audit, not a claim that those runtime modules are missing. fileciteturn195file0L2-L2

A module is not marked `consistent` merely because a matching chapter exists. The final source-grounded state requires an explicit chapter-level comparison and regression evidence.

## Remaining gates before declaring "semester-ready"

| Gate | Requirement | Status |
|---|---|---|
| G1 | Four SDU courses have explicit learning-outcome mappings | Implemented in course coverage modules |
| G2 | DM847 suffix trees and bimodal peak calling are explicit | **Closed in this release** |
| G3 | DM857 source-grounded audit has no misleading `pending` claims | **Documentation cleanup completed; detailed chapter-level verification remains** |
| G4 | DM857 has sufficient independent coding transfer tasks | Partial |
| G5 | DM847 has an oral reasoning simulator exposed in the UI | **Closed in this release** |
| G6 | BMB830 has at least one real public biomedical dataset path | **Closed at registry level; lab integration remains** |
| G7 | BMB831 has real public omics workflows and protein data contracts | Partial-to-strong |
| G8 | Cross-course cumulative project is executable and assessed | **Partial-plus — evidence workspace and JupyterLab/RStudio artifact contracts implemented; end-to-end execution remains** |
| G9 | CI is green for lint, formatting, typing and tests | **Currently failing at lint; must be repaired and re-run** |
| G10 | Private SDU/Itslearning material is explicitly separated from public coverage claims | Implemented |

## Acceptance criteria for the final autonomous-study release

The repository may claim **academic self-study ready** only when all of the following are true:

1. Every public SDU learning outcome maps to at least one concept, one independent practice and one assessment.
2. Every algorithmic learning outcome has at least one problem requiring the learner to produce or modify code in JupyterLab.
3. Every major statistical outcome has at least one RStudio analysis using data that are not hand-designed solely for the exercise.
4. At least one cumulative problem crosses course boundaries.
5. Real datasets are versioned locally before analysis and are accompanied by provenance metadata.
6. Oral reasoning is practised for DM847 and BMB830 through timed prompts and rubric-based self-evaluation.
7. Documentation and executable coverage reports agree with the current codebase.
8. CI passes on both supported Python versions.

## Non-goals

This release does **not** claim that the Study Hub replaces:

- SDU teaching staff;
- official attendance/tutorial requirements;
- group collaboration;
- unpublished Itslearning materials;
- the official grading process.

Those are intentionally outside the autonomous-study claim.
