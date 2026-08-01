# BMB831 official coverage audit

## Source boundary

This audit is based on the active public SDU ODIN description for **BMB831 — Biostatistics in R II**:

- approval date: 2025-03-06;
- status: Approved - active;
- teaching language: English;
- public examination: individual report;
- prerequisite examination: tutorials and exercises, including at least 80 percent participation.

ODIN publishes seven learning outcomes and six content topics. It does not expose the detailed weekly syllabus, official exercise set, report prompt, grading rubric, or itslearning materials. The Study Hub therefore does not claim equivalence with unpublished material.

## Synthea boundary

Synthea is used temporarily for reproducible practice with:

- relational clinical tables;
- longitudinal events;
- patient-level aggregation;
- large-table preparation;
- modelling and visualisation in later modules;
- leakage prevention and validation;
- critical discussion of synthetic-data limitations.

Synthea is **not** described as real-patient evidence. It also does not provide transcriptomic or proteomic abundance matrices, so it cannot satisfy the public omics-pipeline or protein-characterisation requirements by itself.

## Current authored evidence

The first complete BMB831 module provides:

- 4 learning objectives;
- 4 concept blocks;
- 2 executable base-R laboratories;
- 6 individual practices;
- 8 integrated assessment items;
- 16 stable objective-bank items;
- strict Spanish, English, and Danish materialisation;
- one no-audio oral-reasoning outline exercise;
- conservative tutor constraints around provenance and clinical claims.

The laboratories use deterministic fixtures whose fields and relations are structurally aligned with Synthea CSV tables. They do not pretend to be downloaded patient records. A versioned Synthea snapshot with checksums and a dataset manifest is the next data increment.

## Learning outcomes

| ID | Public requirement | Current status | Next required increment |
|---|---|---|---|
| `bmb831.sdu.lo01` | Independently analyse conceptually demanding data sets. | Partial | Add cumulative modelling, visualisation, interpretation, and report modules. |
| `bmb831.sdu.lo02` | Work with large data amounts and identify relevant features. | Partial | Add a versioned Synthea snapshot and memory-aware end-to-end feature pipeline. |
| `bmb831.sdu.lo03` | Use standard algorithms for multivariate analysis. | Gap | Add advanced PCA, clustering, stability, and validated supervised reduction. |
| `bmb831.sdu.lo04` | Design scripts for detailed visualisation. | Gap | Add layered figures, uncertainty, annotation, longitudinal views, and reproducible export. |
| `bmb831.sdu.lo05` | Know and apply tools for data interpretation. | Partial | Extend to enrichment, pathway, and protein interpretation tools. |
| `bmb831.sdu.lo06` | Know and apply standard omics-processing pipelines. | Gap | Add separate transcriptomics and proteomics teaching matrices and workflows. |
| `bmb831.sdu.lo07` | Objectively discuss applied methods in publications. | Partial | Add a source-bounded publication-appraisal studio linked to the final report. |

## Content topics

| ID | Public topic | Current status |
|---|---|---|
| `bmb831.sdu.ct01` | Statistics for large data sets. | Partial |
| `bmb831.sdu.ct02` | Different types of data modelling. | Gap |
| `bmb831.sdu.ct03` | Advanced data visualisation. | Gap |
| `bmb831.sdu.ct04` | Advanced data interpretation. | Partial |
| `bmb831.sdu.ct05` | Computational tools for protein characterisation. | Gap |
| `bmb831.sdu.ct06` | Standard workflows for omics experiments. | Gap |

## Examination alignment

| ID | Public requirement | Current status | Boundary |
|---|---|---|---|
| `bmb831.sdu.exam01` | Tutorials and exercises prerequisite. | Partial | Individual practices exist, but attendance and equivalence with itslearning cannot be certified. |
| `bmb831.sdu.exam02` | Individual report in English. | Gap | No persistent BMB831 report workflow or internal preparation rubric exists yet. |

## Current conclusion

The initial BMB831 module closes the empty-course placeholder and establishes the data-contract foundation. It does not make the course complete. The next priority-zero increments are:

1. import a versioned Synthea CSV snapshot with a dataset card and checksums;
2. add large-table feature engineering and modelling;
3. add advanced visualisation;
4. add multivariate analysis;
5. add the individual English report studio;
6. add separate omics and protein-characterisation data sources rather than misusing Synthea for those requirements.

The executable source of truth is `content/bmb831/official_coverage.py`.
