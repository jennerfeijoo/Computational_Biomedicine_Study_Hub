# BMB831 official coverage audit

> **Status note — 2026-08-09:** This file is a historical coverage record. Several gaps listed below have since been implemented in the runtime curriculum. The current readiness gate is `docs/semester-readiness-audit.md`; the executable source of truth remains `content/bmb831/official_coverage.py`.

## Source boundary

The public SDU description exposes seven learning outcomes and six content topics, but not the detailed weekly syllabus, official exercise set, report prompt, grading rubric, or Itslearning materials. The Study Hub therefore does not claim equivalence with unpublished material.

## Current runtime status

BMB831 now contains nine authored modules covering:

1. Synthea workflows;
2. omics matrices and QC;
3. differential modelling;
4. multivariate omics;
5. advanced visualisation;
6. public omics workflows;
7. protein characterisation;
8. biological interpretation;
9. publication/report preparation.

The book-grounded audit records all nine modules as source-reviewed. The runtime also contains a persistent individual-report workflow and deterministic R laboratories.

## Historical items that are no longer current gaps

The earlier audit marked the following as gaps because the course was still being built:

- advanced PCA/clustering and multivariate analysis;
- advanced visualisation;
- enrichment/pathway interpretation;
- protein characterisation;
- public omics workflows;
- individual report workflow.

Those capabilities are now represented by the M04–M09 runtime modules and associated assessment/report infrastructure.

## Remaining boundaries

The following are deliberately not claimed as equivalent to SDU institutional components:

- tutorial/attendance requirements;
- unpublished Itslearning exercises;
- official report prompt and grading rubric;
- teacher feedback and supervision;
- official examination administration.

Synthea remains a synthetic clinical-data teaching resource. It must not be presented as real-patient evidence, and it cannot substitute for transcriptomic/proteomic datasets.

## Data strategy

The public-omics registry now provides version-aware contracts for:

- Bioconductor `airway`;
- NCBI GEO `GSE305298`;
- UCSC Xena TCGA/TARGET/GTEx;
- ProteomeXchange `PXD000001`.

These are source contracts, not silently downloaded mutable datasets. A reproducible learner workflow must retain the exact local snapshot, metadata, parameters, software versions and SHA-256 manifest.

## Conclusion

The historical gap table should no longer be used to judge the current BMB831 implementation. Use the current runtime coverage, the book-grounded audit and `docs/semester-readiness-audit.md` together when evaluating readiness for self-study.
