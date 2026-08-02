# BMB831 source-grounded curricular and bibliographic audit

## Boundary

The active public SDU description of **BMB831 — Biostatistics in R II** defines the curricular boundary. It requires advanced R analysis of demanding and large biological datasets, multivariate methods, advanced visualisation, biological interpretation, computational protein characterisation, standard omics workflows, objective appraisal of published analyses, and an individual English report.

Public books, methodological papers, Bioconductor documentation, and biological databases are used to verify terminology, assumptions, analytical depth, and interpretation boundaries. Private Itslearning exercises, official attendance certification, the unpublished report prompt, grading criteria, and official examination equivalence are not reconstructed.

Synthea remains one bounded synthetic relational example. It does not define the course, does not replace transcriptomics or proteomics, and is not presented as real-patient evidence.

## Stable source registry

The repository now exposes `BMB831_BOOK_SOURCES` and `BMB831_MODULE_SOURCE_AUDIT`.

Core mapped sources include:

- active SDU BMB831 course description;
- official Synthea CSV-export documentation;
- Bioconductor `SummarizedExperiment` documentation;
- edgeR normalisation and count-modelling documentation;
- DESeq2 dispersion, size-factor, and shrinkage methodology;
- limma empirical-Bayes differential-modelling methodology;
- ISLR chapters on unsupervised learning and multiple testing;
- *Introduction to Modern Statistics* for visual communication and reporting;
- public transcriptomics and proteomics workflow documentation;
- UniProt, InterPro, PDB, AlphaFold DB, Gene Ontology, and Reactome provenance resources.

Mapping a module to sources is not treated as completed verification. A module remains `pending` until its focused comparison, required corrections or extensions, and regression tests exist.

## Current audit state

| Module | State | Finding |
|---|---|---|
| M01 — reproducible Synthea workflows | `consistent` | Existing boundaries, relational contracts, patient-level independence, temporal leakage controls, and reproducibility are adequate. Source traceability was added without expanding Synthea's curricular role. |
| M02 — omics matrices, QC, and normalisation | `consistent` | Existing matrix and QC content was adequate, but composition bias and the distinction between library size and robust size factors required explicit treatment. |
| M03 — differential modelling | `consistent` | Existing design, contrast, model-scale, effect, uncertainty, and FDR content was adequate, but information sharing across features and the separation of moderation, effect shrinkage, and multiplicity required explicit treatment. |
| M04 — multivariate omics | `pending` | Source scope mapped; focused comparison pending. |
| M05 — advanced visualisation | `pending` | Source scope mapped; focused comparison pending. |
| M06 — public omics workflows | `pending` | Source scope mapped; focused comparison pending. |
| M07 — protein characterisation | `pending` | Source scope mapped; focused comparison pending. |
| M08 — biological interpretation | `pending` | Source scope mapped; focused comparison pending. |
| M09 — publication appraisal and report | `pending` | Source scope mapped; focused comparison pending. |

Progress: **3/9 modules source-reviewed**.

## M01 review

M01 is retained as a transferable workflow-engineering foundation rather than an omics evidence module. It already establishes:

- synthetic-data provenance and generation metadata;
- primary keys, foreign keys, grain, and cardinality;
- patient-level dependence and longitudinal aggregation;
- patient-level train/test splitting and temporal leakage prevention;
- immutable source files, manifests, validation, and derived artifacts;
- the explicit boundary that Synthea is neither observed clinical evidence nor a substitute for omics data.

No duplicate teaching unit was added. Its content version remains `1.0.0`.

## M02 extension — composition bias and size factors

Stable additions:

- objective `m02.bg.o1`;
- concept `composition-bias-and-size-factors`;
- example `m02.bg.e01`;
- practice `m02.bg.p01`;
- assessment item `bmb831.m02.book.001`.

The unit distinguishes total library size from a robust relative normalisation factor. It explains how one highly abundant feature can alter library composition and make unchanged features appear lower after total-count scaling. It also states the assumptions behind median-ratio or TMM-style strategies and the need for external controls or spike-ins when a genuine global biological shift is expected.

Deterministic example:

```text
library_factors=0.456,0.548,1.826,2.191
median_factors=0.913,1.095,0.913,1.095
G1_total=219.089,219.089,54.772,54.772
G1_median=109.545,109.545,109.545,109.545
```

The example is algebraic and bounded. It does not claim that median-ratio assumptions hold for every experiment.

M02 content version is `1.1.0`.

## M03 extension — information sharing across features

Stable additions:

- objective `m03.bg.o1`;
- concept `information-sharing-across-features`;
- example `m03.bg.e01`;
- practice `m03.bg.p01`;
- assessment item `bmb831.m03.book.001`.

The unit separates three distinct procedures:

1. variance or dispersion moderation stabilises nuisance-parameter estimates;
2. effect-size shrinkage regularises estimated magnitude;
3. multiple-testing adjustment controls decisions over a hypothesis family.

It also states that empirical-Bayes information sharing does not make genes biological replicates, equalise their effects, repair confounding, or remove the need for FDR control.

Deterministic example:

```text
raw_variance=0.25,1.00,4.00
moderated_variance=0.70,1.00,2.20
raw_t=2.83,1.41,0.71
moderated_t=1.69,1.41,0.95
```

This is an explanatory algebraic model, not a reimplementation of limma, edgeR, or DESeq2.

M03 content version is `1.1.0`.

## Deferred work

The next focused block is:

- M04 — PCA, distances, clustering, stability, batch effects, and leakage;
- M05 — advanced statistical visualisation, uncertainty, visual integrity, and reproducible export.

Experimental-data acquisition remains deferred until all nine source reviews are complete.
