# First-semester autonomous-study readiness audit

## Scope

This document is the current engineering and curriculum gate for using the Study Hub as the principal self-study system for the SDU first semester, together with JupyterLab and RStudio.

The target is not to reproduce SDU's private Itslearning materials, attendance requirements, group dynamics, or official grading. Those remain institutional components. The target is to make the **academic learning pathway** self-sufficient: theory, deliberate practice, executable work, assessment, datasets, transfer, and reproducibility.

## Architecture decision

Keep the responsibilities separate:

The target is not to reproduce SDU's private Itslearning materials, attendance requirements, group dynamics, or official grading. Those remain institutional components. The target is to make the academic learning pathway self-sufficient: theory, deliberate practice, executable work, assessment, datasets, transfer, and reproducibility.

## Architecture decision

- **Study Hub:** curriculum, explanations, retrieval practice, formative assessment, progress, tutor context, source/provenance contracts and integrated assignments.
- **JupyterLab:** Python and algorithmic laboratory for DM857/DM847.
- **RStudio:** R, statistics, Bioconductor and omics laboratory for BMB830/BMB831.

The Study Hub should not become a replacement IDE.

## Changes implemented in this release

### DM847 coverage gaps

1. **Suffix trees** were added explicitly to M06 alongside suffix arrays, LCP, BWT and FM-index concepts.
2. **Bimodal peak calling** was added explicitly to M10, including strand-aware signal interpretation, control/QC boundaries and a reproducible mini-pipeline design task.
3. Each addition has a trilingual concept, worked example, independent practice, objective-level assessment item and tutor source basis.

### Real-data pathway

The public-omics registry now includes:

- Bioconductor `airway` for compact RNA-seq practice;
- NCBI GEO `GSE305298` for human bulk RNA-seq design and differential analysis;
- UCSC Xena's TCGA/TARGET/GTEx cohort for integration-scale feature selection and multivariate work;
- the existing ProteomeXchange teaching contract.

The registry remains snapshot-first: accession metadata is not treated as a reproducible dataset until the learner records the exact local files/version, metadata and SHA-256 manifest.

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

### Cross-course integration target

The semester is treated as one competency chain:

```text
DM857  ->  DM847  ->  BMB830  ->  BMB831
Python    algorithms  statistics   omics
   \          |           |          /
    \---------+-----------+---------/
              integrated biomedical problem
```

A learner should repeatedly move from a biological question to a computational representation, statistical model, executable analysis, validation and biological interpretation.

## Remaining gates before declaring "semester-ready"
## Changes implemented

### DM847

1. Suffix trees are explicit in M06 alongside suffix arrays, LCP, BWT and FM-index concepts.
2. Bimodal peak calling is explicit in M10, including strand-aware signal interpretation, controls, QC and reproducibility.
3. Each addition has trilingual content, a worked example and objective-level assessment evidence.

### Real-data pathway

The public-omics registry includes Bioconductor `airway`, NCBI GEO `GSE305298`, UCSC Xena TCGA/TARGET/GTEx and a ProteomeXchange teaching contract.

The registry is snapshot-first: accession metadata is not treated as a reproducible dataset until the learner records the exact local files/version, metadata and SHA-256 manifest.

## Cross-course integration

```text
DM857 -> DM847 -> BMB830 -> BMB831
Python   algorithms   statistics   omics
   \        |            |          /
    \-------+------------+---------/
             biomedical problem
```

The learner should repeatedly move from a biological question to computational representation, executable analysis, validation and biological interpretation.

## Readiness gates

| Gate | Requirement | Status |
|---|---|---|
| G1 | Four SDU courses have explicit learning-outcome mappings | Implemented in course coverage modules |
| G2 | DM847 suffix trees and bimodal peak calling are explicit | **Closed in this release** |
| G3 | DM857 source-grounded audit has no misleading `pending` claims | **Documentation cleanup required** |
| G4 | DM857 has sufficient independent coding transfer tasks | Partial |
| G5 | DM847 has an oral reasoning simulator | Partial |
| G6 | BMB830 has at least one real public biomedical dataset path | **Closed at registry level; lab integration remains** |
| G7 | BMB831 has real public omics workflows and protein data contracts | Partial-to-strong |
| G8 | Cross-course cumulative project is executable and assessed | Partial |
| G9 | CI is green for lint, formatting, typing and tests | Must be verified after this branch |
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
| G2 | DM847 suffix trees and bimodal peak calling are explicit | Closed in this release |
| G3 | DM857 audit preserves historical review status without misleading claims | Closed as documentation boundary |
| G4 | DM857 has sufficient independent coding transfer tasks | Partial; requires final depth audit |
| G5 | DM847 has a general assessment simulator | Implemented; final UI/coverage audit pending |
| G6 | BMB830 has a real public biomedical dataset path | Closed at registry level; lab integration remains |
| G7 | BMB831 has public omics workflows and protein data contracts | Strong; executable lab integration remains |
| G8 | Cross-course cumulative project is executable and assessed | Partial |
| G9 | CI is green for lint, formatting, typing and tests | Must be verified on the final branch |
| G10 | Private SDU/Itslearning material is separated from public coverage claims | Implemented |

## Acceptance criteria

The repository may claim **academic self-study ready** only when:

1. Every public SDU learning outcome maps to at least one concept, one independent practice and one assessment.
2. Every algorithmic learning outcome has at least one problem requiring the learner to produce or modify code in JupyterLab.
3. Every major statistical outcome has at least one RStudio analysis using data not hand-designed solely for the exercise.
4. At least one cumulative problem crosses course boundaries.
5. Real datasets are versioned locally before analysis and accompanied by provenance metadata.
6. The general assessment simulator provides timed prompts and rubric-based self-evaluation where appropriate; it is not represented as an official SDU exam format.
7. Documentation and executable coverage reports agree with the current codebase.
8. CI passes on both supported Python versions.

## Mentor chat

`Limpiar chat` / `Clear chat` / `Ryd chat` clears mentor conversation state only. It must not delete mastery, course progress, assessment results or other learner evidence.

## Non-goals

This release does not claim that the Study Hub replaces SDU teaching staff, official attendance/tutorial requirements, group collaboration, unpublished Itslearning materials or the official grading process.
