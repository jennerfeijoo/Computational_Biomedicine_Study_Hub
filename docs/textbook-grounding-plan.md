# Textbook-grounded content plan

The Study Hub treats public course descriptions as scope signals, not as the sole
academic authority. Textbooks and primary documentation are used to verify concepts,
algorithmic relationships, terminology, limitations, and exercise progression.

## Rules

1. Learning text, examples, and exercises are independently authored paraphrases.
2. Copyrighted textbook passages are not embedded in the application.
3. Every evidence record uses a stable source ID and a chapter, section, or page locator.
4. `verified` means that the stated scope was checked directly against the registered
   source. `partial` means that only part of the content was checked. `pending` means
   that the source is relevant but has not yet been reviewed.
5. A textbook can support foundational concepts, but software behavior and current
   bioinformatics workflows must later be checked against official documentation and
   primary methodological literature.

## Registered textbook set

| Course | Initial sources |
|---|---|
| DM857 | Guttag, *Introduction to Computation and Programming Using Python*; Downey, *Think Python* |
| DM847 | Compeau and Pevzner, *Bioinformatics Algorithms*, Volumes 1 and 2 |
| BMB830 | Çetinkaya-Rundel and Hardin, *Introduction to Modern Statistics*; James et al., *An Introduction to Statistical Learning* |
| BMB831 | James et al.; Murphy, *Probabilistic Machine Learning*; later supplemented by official Bioconductor documentation and methodological papers |

## First completed increment

DM847 module 6 now adds:

- compacted suffix trees and the distinction from suffix tries;
- the relationship among suffix trees, suffix arrays, LCP, BWT, and FM-indexes;
- an executable longest-repeated-substring example using suffix-array order and LCP;
- two trilingual practices on representation trade-offs and LCP interpretation;
- exact textbook provenance for Chapter 9 of Compeau and Pevzner, Volume 2;
- regression tests for evidence integrity, trilingual materialization, executable output,
  and content-versioning.

## Ordered review sequence

1. **DM847 algorithm audit**
   - pairwise alignment and affine gaps;
   - HMM probability, decoding, Viterbi, and parameter estimation;
   - motif finding, entropy, pseudocounts, and local optima;
   - genome assembly and graph algorithms where useful to the course;
   - read mapping and the boundary between indexing and downstream peak calling.
2. **DM857 programming audit**
   - input contracts and validation;
   - function decomposition, mutation, aliasing, and copying;
   - recursion, termination, and stack reasoning;
   - classes, abstract data types, testing, debugging, and complexity;
   - textbook-grounded executable challenges rather than additional passive prose.
3. **BMB830 statistical audit**
   - study design and the unit of inference;
   - exploratory analysis and multivariable relationships;
   - estimation, randomization, bootstrap, and mathematical inference;
   - regression diagnostics, model interpretation, and uncertainty;
   - cross-validation and leakage boundaries where appropriate.
4. **BMB831 advanced audit**
   - dimensionality reduction and clustering assumptions;
   - model assessment and validation;
   - distinction between general statistical learning and omics-specific methods;
   - explicit flags wherever textbooks do not support an omics-specific claim.

## Deferred dataset acquisition phase

No experimental data are downloaded in the textbook-audit phase. After content review,
the application can add an optional acquisition layer that:

- displays the source, accession, expected size, license or access conditions, and target
  directory before download;
- installs no package automatically without explicit learner action;
- provides copyable commands for R/Bioconductor and repository APIs;
- verifies files with checksums and writes a local manifest and dataset card;
- keeps raw files immutable and separates `raw`, `derived`, and `results` artifacts;
- supports cancellation, retry, and resumable downloads where the upstream service
  permits them;
- never presents synthetic data as experimental evidence.

The acquisition layer should be implemented only after the relevant analytical
pipeline and source contract have been reviewed.
