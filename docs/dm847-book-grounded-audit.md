# DM847 book-grounded content audit

## Scope

This audit compares the ten authored DM847 modules with the active SDU course description and the relevant chapters of Compeau and Pevzner, *Bioinformatics Algorithms: An Active Learning Approach*, volumes I and II.

A source mapping is not treated as a completed review. A module becomes `consistent` only after its existing content has been inspected, any genuine gap has been addressed, and regression tests protect the result.

The textbook is used selectively. Chapters on genome assembly, peptide sequencing, phylogeny, and rearrangements are not inserted merely because they appear in the books; the active DM847 course scope remains the curricular boundary.

## Current source map

| Module | Main mapped source scope | State |
|---|---|---|
| M01 Molecular information | Volume I chapter 1 plus active course scope | Consistent |
| M02 Ontologies and databases | Active course scope; specialized source still required | Pending |
| M03 Sequence scoring and matching | Volume I chapters 1 and 5 | Consistent |
| M04 Pairwise alignment | Volume I chapter 5 | Consistent |
| M05 Hidden Markov models | Volume II chapter 10 | Consistent |
| M06 Suffix arrays, BWT, mapping | Volume II chapter 9 | Consistent |
| M07 Operons and bacterial genetics | Active course scope; specialized source still required | Pending |
| M08 Motif discovery and EM | Volume I chapter 2; Volume II chapter 8 | Consistent |
| M09 Biological networks | Active DM847 scope; Ideker et al. (2002); Alcaraz et al. (2012) | Consistent |
| M10 OMICS learning | Volume II chapter 8 plus active course scope | Consistent |

## Completed focused review: M03

The existing module already covered k-mer composition, substitution matrices, log-odds scores, exact search, empirical null models, search-space effects, and multiplicity.

The missing transition was from exact matching to approximate matching. The extension now covers:

- Hamming distance for equal-length strings;
- matching with at most `d` substitutions;
- the pattern-neighborhood concept;
- the identity `d = 0` as exact matching;
- the distinction between mismatches and gaps;
- explicit strand and reverse-complement policy;
- input validation preventing `zip` truncation from accepting partial windows.

Stable IDs:

- `m03.bg.o1`
- `approximate-pattern-matching-and-neighborhoods`
- `m03.bg.e01`
- `m03.bg.p01`
- `dm847.m03.book.001`

Content version: `1.1.0`.

## Completed focused review: M04

The existing module already covered alignment objectives, global, local and semiglobal alignment, dynamic-programming recurrences, initialization, traceback, ties, affine gaps, complexity, and validation.

The missing boundary was between score-only computation and alignment reconstruction. The extension now covers:

- rolling-row dynamic programming;
- `O(nm)` time with `O(min(n,m))` memory for score-only computation;
- why the final row does not retain direct traceback information;
- matrix or pointer storage for direct reconstruction;
- divide-and-conquer reconstruction through middle nodes or edges;
- explicit output contracts: score, one alignment, or multiple optima.

Stable IDs:

- `m04.bg.o1`
- `linear-space-scoring-and-traceback-boundary`
- `m04.bg.e01`
- `m04.bg.p01`
- `dm847.m04.book.001`

Content version: `1.1.0`.

## Completed focused review: M05

The existing module already covered HMM components, path and sequence probabilities, Forward, Viterbi, numerical stability, supervised parameter estimation, Baum-Welch, and profile HMMs.

The missing component was explicit soft decoding. The extension now covers:

- Forward values as prefix-and-state joint probabilities;
- Backward values as suffix probabilities conditional on current state;
- posterior state probability proportional to `alpha_t(k) * beta_t(k)`;
- normalization to one independently at every sequence position;
- filtered prefix probabilities versus posteriors smoothed with the complete sequence;
- local posterior uncertainty versus one globally optimal Viterbi path;
- the possibility that independent posterior maxima violate structural transition constraints.

The deterministic example calculates posterior state probabilities for the observation sequence `GA`:

```text
[{'H': 0.651, 'L': 0.349}, {'H': 0.316, 'L': 0.684}]
```

Stable IDs:

- `m05.bg.o1`
- `soft-decoding-forward-backward`
- `m05.bg.e01`
- `m05.bg.p01`
- `dm847.m05.book.001`

Content version: `1.1.0`.

## Completed focused review: M06

The existing module already covered suffix arrays, LCP, BWT construction and inversion assumptions, LF-mapping, backward search, FM-index count and locate operations, suffix-array sampling, multimapping, and seed-and-extend workflows.

The missing component was the explicit reduction of mismatch-bounded matching to exact seed searches. The extension now covers:

- partitioning a pattern into `d + 1` disjoint nonempty seeds;
- the pigeonhole proof that at least one seed is exact when the full window has at most `d` substitutions;
- converting each seed hit to a candidate start by subtracting its offset;
- rejecting out-of-bounds starts and deduplicating candidates;
- verifying every complete candidate with Hamming distance;
- why an exact seed does not itself prove a valid full match;
- the boundary that this guarantee does not cover insertions or deletions.

The deterministic example produces candidate and verified positions separately:

```text
([0, 5, 10], [0, 5])
```

Position 10 shares an exact seed but is rejected because the full window contains two mismatches.

Stable IDs:

- `m06.bg.o1`
- `pigeonhole-seeding-and-verification`
- `m06.bg.e01`
- `m06.bg.p01`
- `dm847.m06.book.001`

Content version: `1.1.0`.

## Completed focused review: M08

The existing module already covered PWM construction, pseudocounts, entropy, log-odds scoring, OOPS/ZOOPS/TCM occurrence models, latent positions, EM responsibilities, local optima, background choice, and independent validation.

The missing implementation boundary was the complete soft M-step and an auditable stopping rule. The extension now covers:

- responsibilities normalized within the occurrence model;
- fractional expected base counts rather than hard argmax assignments;
- pseudocount addition and column normalization;
- monotonic observed-data likelihood up to numerical tolerance;
- absolute or relative convergence tolerance;
- a maximum iteration limit as a separate safeguard;
- comparable objective functions across random restarts.

The deterministic example produces a two-column PWM from fractional responsibilities:

```text
[{'A': 0.4, 'C': 0.167, 'G': 0.267, 'T': 0.167}, {'A': 0.167, 'C': 0.367, 'G': 0.167, 'T': 0.3}]
```

Stable IDs:

- `m08.bg.o1`
- `fractional-counts-and-em-convergence`
- `m08.bg.e01`
- `m08.bg.p01`
- `dm847.m08.book.001`

Content version: `1.1.0`.

## Completed focused review: M09

The existing module already covered network semantics, topology, centrality, hypergeometric over-representation analysis, multiplicity, random-walk propagation, computational modules, and structure-aware null models.

The source audit also found and corrected an inaccurate mapping: chapter 11 of Compeau and Pevzner volume II concerns peptide sequencing and peptide-spectrum analysis, not biological network enrichment. M09 is now grounded in the active DM847 description and the primary jActiveModules and KeyPathwayMiner publications.

The missing methodological boundary was between testing predefined gene sets and selecting connected active subnetworks from the observed data. The extension now covers:

- ORA as a test of terms fixed before observing the selected list;
- connected active-module extraction from topology and node evidence;
- jActiveModules-style size-normalized aggregate scores;
- KeyPathwayMiner-style connected extraction with explicit exceptions;
- heuristic search and the absence of a guaranteed global optimum;
- module scores versus calibrated p-values;
- selection-aware null models that reproduce search and constraints;
- stability under network and score perturbation.

The deterministic example compares two connected candidates:

```text
{'AB': 3.536, 'ABC': 2.309}
```

Stable IDs:

- `m09.bg.o1`
- `predefined-enrichment-vs-active-subnetworks`
- `m09.bg.e01`
- `m09.bg.p01`
- `dm847.m09.book.001`

Content version: `1.1.0`.

## Completed focused review: M01

The existing module already covered molecular information flow, sequence alphabets, ambiguity, strand orientation, coordinate systems, regulation, bacterial genetics, phages, provenance, and biological question framing.

The missing boundary was an explicit computational problem contract. The extension now covers:

- inputs, outputs, alphabets, orientation, and coordinate conventions;
- overlap and reverse-complement policies;
- invalid symbols, empty patterns, and short-input edge cases;
- known-answer examples and invariants before algorithm selection;
- separation of computational correctness from biological interpretation.

The deterministic example searches canonical DNA on the supplied strand with zero-based positions and overlapping matches:

```text
[0, 2]
```

Stable IDs:

- `m01.bg.o1`
- `computational-problem-contracts`
- `m01.bg.e01`
- `m01.bg.p01`
- `dm847.m01.book.001`

Content version: `1.1.0`.

## Completed focused review: M10

The existing module already covered OMICS matrix design, preprocessing, leakage, PCA, clustering, supervised learning, nested validation, metrics, interpretation, and reproducibility.

The missing algorithmic boundary was the relation between clustering objective, initialization, assignment type, and scientific stability. The extension now covers:

- hard k-means assignments and distortion;
- Lloyd updates and local optima;
- multiple restarts and comparable objectives;
- soft responsibilities that sum to one;
- hierarchical distance and linkage choices;
- dependence on transformation, scaling, feature selection, and batch;
- resampling stability and external replication.

The deterministic example compares two Lloyd restarts:

```text
{'left_start': ((1.0, 12.5), 11.286), 'right_start': ((5.5, 20.0), 17.929)}
```

Stable IDs:

- `m10.bg.o1`
- `clustering-objectives-initialization-and-stability`
- `m10.bg.e01`
- `m10.bg.p01`
- `dm847.m10.book.001`

Content version: `1.1.0`.

## Source boundary

All visible explanations, code, examples, exercises, values, and solutions are original paraphrases and adaptations. No textbook exercise, figure, table, or extended passage is reproduced verbatim.

No experimental dataset acquisition is implemented in this increment.
