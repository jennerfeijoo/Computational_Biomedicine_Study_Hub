# Book-grounded content audit

This audit separates three questions that must not be conflated:

1. Does a module cover the public SDU knowledge requirement?
2. Is the explanation technically consistent with an appropriate reference source?
3. Can the learner transfer the knowledge through executable or interpretive practice?

Official assessment format, attendance, grading, group work, and institutional administration are outside this academic-content audit.

## Source policy

- Reference books are used to verify terminology, conceptual sequencing, assumptions, examples, and exercise design.
- The Study Hub paraphrases and synthesizes; it does not reproduce textbook prose, figures, tables, or proprietary exercise statements.
- Time-sensitive software behavior must later be checked against official documentation and primary methodological sources.
- A source match does not by itself prove mastery. Each important concept should also have worked reasoning, practice, feedback, and transfer evidence.

## Verification states

| State | Meaning |
|---|---|
| `pending` | Not yet checked against a named source. |
| `consistent` | Current content agrees with the cited source at the stated scope. |
| `improve` | Broadly correct but missing a distinction, assumption, counterexample, or practice step. |
| `correct` | A technical error or materially misleading statement must be fixed. |
| `outside_scope` | Valid source content that is not required for the present course trajectory. |

## First-semester source map

### DM857 — Introduction to Programming

Primary books:

- John V. Guttag, *Introduction to Computation and Programming Using Python*, 3rd ed.
- Allen B. Downey, *Think Python*, 3rd ed.

Audit priorities:

- programs as models and structured problem solving;
- expressions, branching, iteration, and functions;
- specifications, abstraction, scope, and decomposition;
- mutation, aliasing, identity, and value semantics;
- recursion, base cases, recursive data structures, and call reasoning;
- modules, files, exceptions, assertions, testing, and debugging;
- classes, data abstraction, invariants, and abstract data types;
- algorithmic complexity, searching, sorting, trees, and graph foundations;
- incremental development, boundary tests, and failure reconstruction.

Book-derived improvement targets for the existing course:

1. Make function specifications and pre/postconditions explicit in executable challenges.
2. Add mutation-versus-rebinding and aliasing diagnostics rather than only syntax questions.
3. Require boundary-condition tests, invalid-input tests, and exception contracts.
4. Contrast iterative and recursive solutions using correctness and cost, not style alone.
5. Add complexity comparisons tied to concrete implementations.
6. Strengthen design-first and incremental-development exercises.
7. Expand hidden-test challenges across all modules.

### DM847 — Introduction to Bioinformatics

Primary books:

- Phillip Compeau and Pavel Pevzner, *Bioinformatics Algorithms: An Active Learning Approach*, Volumes I and II.

Supporting sources:

- molecular biology and genetics references for biological interpretation;
- official NCBI/EMBL-EBI documentation and primary algorithm/tool papers for current database and software behavior.

Audit priorities:

- computational problem statements before implementation;
- k-mer counting, mismatches, neighborhoods, and replication-origin reasoning;
- motif scoring, entropy, randomized search, Gibbs sampling, and EM;
- graph representations, genome assembly, De Bruijn graphs, Eulerian paths;
- dynamic programming for sequence alignment;
- suffix structures, BWT, read mapping, and indexing;
- HMM formulation and interpretation;
- phylogenetic distance and character methods;
- clustering, dimensionality reduction, and biological networks;
- code challenges followed by interpretation and transfer tasks.

### BMB830 — Biostatistics in R I

Primary books:

- Mine Çetinkaya-Rundel and Johanna Hardin, *Introduction to Modern Statistics*, 2nd ed.
- Gareth James, Daniela Witten, Trevor Hastie, and Robert Tibshirani, *An Introduction to Statistical Learning with Applications in R*, 2nd ed.
- Yachay Tech biostatistics and probability/statistics notes as supplementary historical course material.

Audit priorities:

- data and study design before calculation;
- exploratory analysis and robust summaries;
- sampling, randomization, bootstrap, and mathematical inference;
- effect sizes, uncertainty, assumptions, and multiplicity;
- regression design matrices, interactions, diagnostics, and validation;
- prediction versus explanation and association versus causation;
- reproducible R workflows and interpretation of output.

### BMB831 — Biostatistics in R II

Primary conceptual books:

- *An Introduction to Statistical Learning with Applications in R*.
- Kevin P. Murphy, *Probabilistic Machine Learning: An Introduction*.
- *Introduction to Modern Statistics* for study design and inferential foundations.

Required methodological sources in later passes:

- Bioconductor vignettes and package documentation;
- primary papers for differential-expression, enrichment, protein-annotation, and omics methods;
- official repository documentation for public datasets.

Audit priorities:

- high-dimensional data and leakage-safe workflows;
- normalization, transformation, missingness, and batch structure;
- differential models, contrasts, uncertainty, and multiplicity;
- multivariate geometry, stability, and interpretation;
- biological identifier mapping, enrichment, pathways, and networks;
- computational protein characterization and evidence boundaries;
- complete reproducible workflow reasoning.

## Deferred experimental-data layer

Experimental downloads are intentionally deferred until the authored content has passed the book-grounded audit.

The later data layer should provide explicit, user-triggered commands rather than silent network activity. It should include:

- R/Bioconductor installation and retrieval commands;
- Python clients or command-line tools where appropriate;
- accession, version, access date, file list, sizes, and SHA-256 manifest;
- resumable downloads and clear failure messages;
- immutable `raw/`, derived `derived/`, and generated `results/` boundaries;
- dataset cards and scientific-use limitations;
- no bundled credentials, no controlled-access bypass, and no claim that a mutable URL is a reproducible snapshot.

Candidate interfaces to evaluate later include `BiocManager`, `ExperimentHub`, `recount3`, `GEOquery`, `BiocFileCache`, ENA/SRA retrieval tools, PRIDE Archive interfaces, and repository-specific APIs. Exact commands and versions must be verified against current official documentation before implementation.

## Implementation order

1. Audit and improve DM857 using Guttag and Downey.
2. Audit and improve DM847 using Compeau and Pevzner.
3. Audit and improve BMB830 using modern statistics and statistical-learning references.
4. Audit and improve BMB831 using statistical references plus method-specific primary sources.
5. Add the explicit experimental-data download layer.
6. Run independent question, solution, executable-example, and transfer audits.
