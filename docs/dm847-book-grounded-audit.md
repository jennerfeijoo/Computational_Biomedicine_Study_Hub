# DM847 book-grounded content audit

## Scope

This audit compares the ten authored DM847 modules with the active SDU course description and the relevant chapters of Compeau and Pevzner, *Bioinformatics Algorithms: An Active Learning Approach*, volumes I and II.

A source mapping is not treated as a completed review. A module becomes `consistent` only after its existing content has been inspected, any genuine gap has been addressed, and regression tests protect the result.

The textbook is used selectively. Chapters on genome assembly, peptide sequencing, phylogeny, and rearrangements are not inserted merely because they appear in the books; the active DM847 course scope remains the curricular boundary.

## Current source map

| Module | Main mapped source scope | State |
|---|---|---|
| M01 Molecular information | Active course scope; biological-question framing and sequence orientation | Pending |
| M02 Ontologies and databases | Active course scope; specialized source still required | Pending |
| M03 Sequence scoring and matching | Volume I chapters 1 and 5 | Consistent |
| M04 Pairwise alignment | Volume I chapter 5 | Consistent |
| M05 Hidden Markov models | Volume II chapter 10 | Consistent |
| M06 Suffix arrays, BWT, mapping | Volume II chapter 9 | Consistent |
| M07 Operons and bacterial genetics | Active course scope; specialized source still required | Pending |
| M08 Motif discovery and EM | Volume I chapter 2; Volume II chapter 8 | Pending |
| M09 Biological networks | Volume II chapter 11 | Pending |
| M10 OMICS learning | Volume II chapter 8 plus active course scope | Pending |

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

## Source boundary

All visible explanations, code, examples, exercises, values, and solutions are original paraphrases and adaptations. No textbook exercise, figure, table, or extended passage is reproduced verbatim.

No experimental dataset acquisition is implemented in this increment.
