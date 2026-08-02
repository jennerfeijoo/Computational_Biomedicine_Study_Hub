# BMB831 source-grounded curricular and bibliographic audit

## Boundary

The active public SDU description of **BMB831 — Biostatistics in R II** defines the curricular boundary. It requires advanced R analysis of demanding and large biological datasets, multivariate methods, advanced visualisation, biological interpretation, computational protein characterisation, standard omics workflows, objective appraisal of published analyses, and an individual English report.

Public books, methodological papers, Bioconductor documentation, and biological databases are used to verify terminology, assumptions, analytical depth, and interpretation boundaries. Private Itslearning exercises, official attendance certification, the unpublished report prompt, grading criteria, and official examination equivalence are not reconstructed.

Synthea remains one bounded synthetic relational example. It does not define the course, does not replace transcriptomics or proteomics, and is not presented as real-patient evidence.

## Stable source registry

The repository exposes `BMB831_BOOK_SOURCES` and `BMB831_MODULE_SOURCE_AUDIT`.

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
| M04 — multivariate omics | `consistent` | Existing PCA, distance, clustering, batch, stability, and leakage coverage was adequate. Finite-sample rank and near-degenerate subspace stability required explicit treatment. |
| M05 — advanced visualisation | `consistent` | Existing figure contracts, omics plots, heatmaps, accessibility, and reproducible export were adequate. Error-bar targets and the distinction among spread, SE, confidence intervals, and prediction uncertainty required explicit treatment. |
| M06 — public omics workflows | `consistent` | Existing public-source snapshots, assay-specific contracts, missingness, transition checks, and reproducibility boundaries were adequate. Shared peptides and protein-group inference required explicit treatment. |
| M07 — protein characterisation | `consistent` | Existing sequence identity, annotation provenance, PDB coverage, and AlphaFold limits were adequate. The distinction between local pLDDT and relative-domain PAE required explicit treatment. |
| M08 — biological interpretation | `consistent` | Existing identifier mapping, universes, enrichment, networks, redundancy, circularity, and evidence boundaries were adequate. Ontology propagation and dependence among parent and child terms required explicit treatment. |
| M09 — publication appraisal and report | `consistent` | Existing estimand reconstruction, claim traceability, validity appraisal, reproducibility, and report structure were adequate. Specification sensitivity and selective reporting required explicit treatment. |

Progress: **9/9 modules source-reviewed**.

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

## M04 extension — finite-sample rank and subspace stability

Stable additions:

- objective `m04.bg.o1`;
- concept `finite-sample-rank-and-subspace-stability`;
- example `m04.bg.e01`;
- practice `m04.bg.p01`;
- assessment item `bmb831.m04.book.001`.

The unit makes the finite-sample boundary explicit. After centering an `n × p` sample-by-feature matrix, no more than `min(p, n - 1)` principal components can contain non-zero sample variation. Thousands of measured genes therefore do not substitute for independent samples or create thousands of identifiable dimensions.

It also distinguishes stability of individual component axes from stability of their joint subspace. When eigenvalues are tied or close, small perturbations can rotate scores and loadings while preserving the scientifically relevant plane. Stability checks should therefore include resampling, feature perturbation, explained variance, metadata, and subspace comparisons rather than rigid loading lists from one run.

Deterministic example:

```text
samples=4
features=6
rank_ceiling=3
observed_rank=3
nonzero_pcs=3
```

The example establishes a mathematical ceiling. It does not claim that the retained components are biologically sufficient or externally validated.

M04 content version is `1.1.0`.

## M05 extension — spread and uncertainty targets

Stable additions:

- objective `m05.bg.o1`;
- concept `spread-versus-estimator-uncertainty`;
- example `m05.bg.e01`;
- practice `m05.bg.p01`;
- assessment item `bmb831.m05.book.001`.

The unit distinguishes:

- standard deviation as observed spread;
- standard error as estimated variability of a mean;
- confidence intervals as uncertainty from a defined inferential procedure;
- prediction intervals as uncertainty for future observations, including residual variation.

Error bars must state their type, level, method, sample size, and analytical unit. A mean-only figure can hide skew, outliers, dependence, and heterogeneity, so individual observations or distributions should accompany summaries when appropriate.

Deterministic example:

```text
group_A=mean:10.000,sd:1.633,se:0.816,ci_half:2.598
group_B=mean:10.000,sd:4.899,se:2.449,ci_half:7.795
```

The groups have the same mean but different spread and estimator uncertainty. The example assumes four independent observations per group and does not replace paired, longitudinal, or hierarchical models.

M05 content version is `1.1.0`.

## M06 extension — shared peptides and protein inference

Stable additions:

- objective `m06.bg.o1`;
- concept `shared-peptides-and-protein-inference`;
- example `m06.bg.e01`;
- practice `m06.bg.p01`;
- assessment item `bmb831.m06.book.001`.

The unit distinguishes peptide-level quantification from protein-level identification. A proteotypic peptide can support an individual protein, whereas a shared peptide remains compatible with multiple proteins, isoforms, or family members. Parsimony, razor-peptide, and protein-grouping rules produce a usable table but do not manufacture evidence that separates indistinguishable entities.

The analytical package must therefore retain precursor–peptide–protein mappings, declare grouping rules, and limit the estimand and biological claim to the level actually identified. A differential signal assigned to a protein group does not identify which member changed.

Deterministic example:

```text
peptides=4
unique_peptides=2
shared_peptides=2
proteins_with_unique=2
proteins_shared_only=2
```

The fixture contains individual evidence for P1 and P2, but only group-compatible evidence for P3 and P4.

M06 content version is `1.1.0`.

## M07 extension — pLDDT and relative-domain PAE

Stable additions:

- objective `m07.bg.o1`;
- concept `local-confidence-versus-domain-placement`;
- example `m07.bg.e01`;
- practice `m07.bg.p01`;
- assessment item `bmb831.m07.book.001`.

The unit separates local structural confidence from confidence in long-range placement. pLDDT is interpreted per residue or region as local confidence. PAE is used to assess how confidently one region is positioned relative to another and is therefore necessary when interpreting domain packing or global topology.

Two domains may each have high pLDDT and low internal PAE while retaining high PAE between domains. In that case the internal folds may be plausible, but their mutual orientation remains uncertain. Neither metric proves biological interaction, dynamics, active state, function, or mechanism.

Deterministic example:

```text
domain_A_plddt=90.0
domain_B_plddt=89.0
within_A_pae=2.0
within_B_pae=2.0
between_pae=18.0
```

The example demonstrates confidence separation; it is not an experimental structure or a validation of a biological assembly.

M07 content version is `1.1.0`.

## M08 extension — ontology propagation and dependent terms

Stable additions:

- objective `m08.bg.o1`;
- concept `ontology-propagation-and-term-dependence`;
- example `m08.bg.e01`;
- practice `m08.bg.p01`;
- assessment item `bmb831.m08.book.001`.

The unit makes ontology inheritance explicit. A direct annotation to a specific term can propagate to compatible ancestors, so parent and child terms share genes by construction. Significant parent and child results are therefore dependent and may summarize one annotation signal rather than independent biological confirmations.

Multiplicity adjustment does not remove ontology dependence or semantic redundancy. Interpretation must retain ontology release, relations, evidence codes, direct and propagated annotations, and driver genes. Term reduction or clustering requires a declared reproducible rule and must not hide the complete result table.

Deterministic example:

```text
direct_annotations=3
propagated_annotations=6
parent_genes=3
child_terms=2
```

The propagated parent annotations arise from the same three direct observations; they are not additional biological replicates.

M08 content version is `1.1.0`.

## M09 extension — specification sensitivity and selective reporting

Stable additions:

- objective `m09.bg.o1`;
- concept `specification-sensitivity-and-selective-reporting`;
- example `m09.bg.e01`;
- practice `m09.bg.p01`;
- assessment item `bmb831.m09.book.001`.

The unit treats analytical decisions as part of the evidence chain. Inclusion criteria, filters, transformations, covariates, contrasts, missing-data handling, multiplicity, and model choice may all alter magnitude, direction, or uncertainty. One favourable specification does not establish robustness when other scientifically defensible analyses are absent or discordant.

The appraisal should define the expected specification set, separate primary and sensitivity analyses, preserve complete results, record deviations, and mark missing evidence rather than reconstructing it by assumption. A report may describe the observed model while classifying robustness as not assessable when declared alternatives are unavailable.

Deterministic example:

```text
specifications=4
positive=3
negative=1
range=-0.20,0.80
sign_stable=FALSE
```

The example contains a sign reversal, so it does not support a robust directional claim without explaining the analytical decisions.

M09 content version is `1.1.0`.

## Audit completion and next boundary

The source-grounded review is complete for all nine BMB831 modules. Completion means that each module has a mapped public source scope, focused comparison, implemented correction or extension where needed, deterministic regression coverage, and stable trilingual identities.

It does **not** establish official equivalence with private teaching, attendance, examination, or grading material. The next distinct repository phase may evaluate controlled acquisition of public experimental datasets and executable end-to-end workflows. Any such phase should preserve licenses, immutable snapshots, checksums, dataset cards, assay-specific processing, computational resource limits, and a strict separation between reproducibility and scientific validity.
