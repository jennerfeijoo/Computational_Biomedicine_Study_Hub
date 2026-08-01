# BMB831 completion roadmap

## Source boundary

This roadmap is grounded in the active public SDU description for **BMB831 — Biostatistics in R II**, approved 2025-03-06. The public specification defines seven learning outcomes, six main content topics, an exercise prerequisite with at least 80% participation, and an individual report in English.

The detailed lecture order, official exercises, package choices, report prompt, and grading rubric remain on itslearning and are not public. The Study Hub therefore provides a conservative preparation sequence rather than claiming to reproduce the official internal syllabus.

## Course-level design decision

BMB831 is an omics and advanced-data-analysis course. Synthea remains one bounded synthetic clinical-data case for relational and longitudinal engineering, but it does not define the curriculum and cannot replace transcriptomics, proteomics, protein characterisation, or a real-data final project.

## Authored sequence

| Module | Scope | Current state |
|---|---|---|
| M01 | Reproducible relational and longitudinal workflows using Synthea as a synthetic case | Complete |
| M02 | Omics matrix contracts, metadata alignment, quality control, filtering, normalization, transformation, and scaling | Complete |
| M03 | Differential modeling, design matrices, count-model reasoning, effect sizes, uncertainty, and false-discovery control | Complete |
| M04 | Multivariate analysis: PCA, distances, clustering, stability, supervised reduction, and leakage control | Complete |
| M05 | Advanced visualization: figure contracts, MA and volcano reasoning, heatmaps, uncertainty, annotation, accessibility, and reproducible export | Complete |
| M06 | End-to-end transcriptomics and proteomics workflows on versioned public data | Pending |
| M07 | Protein characterisation: sequence, domains, physicochemical properties, structure, annotation, and provenance | Pending |
| M08 | Biological interpretation: enrichment, pathways, networks, evidence hierarchy, and claim boundaries | Pending |
| M09 | Publication appraisal and individual English report studio with a cumulative real-data project | Pending |

## Required evidence per completed module

Every completed module must include:

- at least four explicit learning objectives;
- at least four conceptual sections;
- at least two deterministic executable R examples where local policy permits;
- at least six individually completable practices;
- eight integrated assessment items;
- a stable sixteen-item objective question bank;
- strict Spanish, English, and Danish materialization;
- bounded tutor guidance with sources and inferential constraints;
- regression tests for identity, localization, content integrity, and lazy UI construction.

## Real-data requirement

The final course sequence must contain at least one versioned public transcriptomics or proteomics dataset with:

- immutable source files or documented retrieval identifiers;
- checksums and a dataset card;
- sample and feature metadata;
- a declared biological question and estimand;
- reproducible preprocessing;
- quality-control decisions and sensitivity analyses;
- statistical modeling and multiplicity control;
- multivariate and advanced visual outputs;
- biological interpretation with source-bounded claims;
- a complete English report artifact.

Synthetic teaching matrices remain useful for deterministic exercises but cannot satisfy the final real-data project by themselves.

## Completion criterion

BMB831 will be described as **authored-course complete** only when modules M01–M09 are implemented and the public coverage audit has no academic-content gaps. Examination equivalence will remain unclaimed until the official itslearning exercises, report prompt, and rubric are available.
