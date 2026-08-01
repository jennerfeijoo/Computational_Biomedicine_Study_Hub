# DM857 book-grounded audit

This audit compares the authored DM857 sequence with:

- John V. Guttag, *Introduction to Computation and Programming Using Python*, 3rd edition;
- Allen B. Downey, *Think Python*, 3rd edition.

It evaluates academic content only. SDU grading, attendance, group projects, and presentation format are not coverage requirements.

## Current status

| Module | Reference scope | State | Result |
|---|---|---|---|
| M01 Foundations | Guttag 1–3; Downey foundations | `pending` | Source mapping complete; detailed review pending. |
| M02 Conditionals | Guttag 1–3; Downey foundations | `pending` | Source mapping complete; detailed review pending. |
| M03 Iteration | Guttag 1–3; Downey foundations | `pending` | Source mapping complete; detailed review pending. |
| M04 Functions | Guttag 4–5; Downey functions/testing | `consistent` | Contracts, scope, return, purity, decomposition, and unit testing were already strong. Added mutable-default-state coverage. |
| M05 Strings | Guttag 5; Downey strings | `pending` | Source mapping complete; detailed review pending. |
| M06 Sequences | Guttag 5; Downey collections | `consistent` | Already covers mutation versus rebinding, aliasing, shallow copies, nested-row aliasing, and mutation during traversal. |
| M07 Mappings and sets | Guttag 5 and 12; Downey collections | `pending` | Source mapping complete; detailed review pending. |
| M08 Files and exceptions | Guttag 7–9; Downey files/testing | `consistent` | File boundaries, context managers, specific exceptions, propagation, and failure testing were already strong. Added exceptions-versus-assertions coverage. |
| M09 Recursion | Guttag 6; Downey recursion | `consistent` | Already covers reachable base cases, decreasing progress measures, independent frames, unwinding, cost, and memoization limits. |
| M10 Trees | Guttag 10–12 and 14 | `pending` | Source mapping complete; detailed review pending. |
| M11 ADTs | Guttag 10–12; Downey OOP | `pending` | Source mapping complete; detailed review pending. |
| M12 OOP | Guttag 10; Downey OOP | `pending` | Source mapping complete; detailed review pending. |
| M13 Scientific libraries | Guttag 13 and 23 | `pending` | Source mapping complete; detailed review pending. |
| M14 Testing and quality | Guttag 8–9; Downey testing | `consistent` | Already treats tests as executable contracts and covers boundaries, expected failures, fixture isolation, debugging hypotheses, and regression tests. |

Five modules have completed a focused source comparison. Nine remain explicitly pending; the repository does not represent source mapping as completed verification.

## Implemented improvements

### M04: mutable default parameters

The existing module stated that default values are evaluated when a function is defined, but it did not make the resulting shared-state failure sufficiently explicit. The extension adds:

- a trilingual concept explaining why mutable defaults persist across calls;
- an original safe `None`-sentinel example;
- a debugging exercise that reconstructs the hidden shared state;
- a stable objective item distinguishing safe and unsafe designs.

### M08: exceptions versus assertions

The existing module covered input validation and specific exceptions but did not clearly separate a public contract violation from an internal invariant failure. The extension adds:

- a trilingual concept distinguishing explicit exceptions from assertions;
- an original percentage-parsing example;
- an interpretation exercise classifying boundary errors and internal defects;
- a stable objective item verifying that public validation cannot depend on `assert`.

## Integrity controls

- The additions are original paraphrases and examples, not copied textbook prose or exercises.
- Reviewed source IDs are attached to the tutor source basis of M04, M06, M08, M09, and M14.
- New examples execute deterministically in regression tests.
- Stable IDs are preserved across Spanish, English, and Danish.
- The experimental-data layer remains deferred.

## Next pass

1. M01–M03: models, binding, Boolean reasoning, iteration, loop invariants, and incremental development.
2. M05 and M07: string and collection algorithms, identity/value semantics, hashing, and complexity.
3. M10–M12: trees, ADT representation invariants, classes, inheritance, and interface discipline.
4. M13: scientific-library interfaces, arrays, tabular data, and plotting contracts.
5. Expand executable challenges only after each corresponding source review.
