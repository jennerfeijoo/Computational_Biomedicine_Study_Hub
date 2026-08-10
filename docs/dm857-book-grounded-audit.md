# DM857 book-grounded audit

> **Status note — 2026-08-09:** This document is retained as the historical source-review record. It is **not** the final semester-readiness gate. The current autonomous-study acceptance criteria are defined in `docs/semester-readiness-audit.md`.

## Source boundary

This audit compares the authored DM857 sequence with:

- John V. Guttag, *Introduction to Computation and Programming Using Python*, 3rd edition;
- Allen B. Downey, *Think Python*, 3rd edition.

It evaluates academic content only. SDU grading, attendance, group projects, and presentation format are not coverage requirements.

## Current interpretation

The runtime DM857 curriculum contains fourteen modules covering foundations, conditionals, iteration, functions, strings, sequences, mappings/sets, files/exceptions, recursion, trees, ADTs, OOP, scientific libraries, and testing/debugging/quality. The repository also contains focused book-grounded extensions and regression tests for several of those modules.

The old table below used `pending` to mean that a detailed source comparison had not yet been recorded in this particular audit file. It should **not** be interpreted as meaning that the corresponding runtime module is empty or unavailable.

## Historical review status

| Module | Historical state in this audit |
|---|---|
| M01 Foundations | pending |
| M02 Conditionals | pending |
| M03 Iteration | pending |
| M04 Functions | consistent |
| M05 Strings | pending |
| M06 Sequences | consistent |
| M07 Mappings and sets | pending |
| M08 Files and exceptions | consistent |
| M09 Recursion | consistent |
| M10 Trees | pending |
| M11 ADTs | pending |
| M12 OOP | pending |
| M13 Scientific libraries | pending |
| M14 Testing and quality | consistent |

This historical status is intentionally preserved rather than rewritten as if a source review had occurred when it was not recorded here.

## Runtime evidence already present

- fourteen authored modules;
- executable Python challenges and computational laboratories;
- capstone and supervision workflows;
- stable objective-level assessment;
- tutor source-basis metadata;
- regression tests for content registration and several focused source-grounded extensions.

## Next verification pass

The remaining work is a **source-grounded verification pass**, not creation of placeholder content. Each pending module should be checked against the relevant book chapters, with explicit findings, implemented corrections, and tests before its audit state is changed to `consistent`.

For the overall first-semester decision, use `docs/semester-readiness-audit.md` and the executable course coverage modules as the authoritative engineering gate.
