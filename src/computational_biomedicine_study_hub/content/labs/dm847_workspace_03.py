"""Persistent scientific workspace for DM847 laboratory 3."""

from __future__ import annotations

from ...learning.scientific_workspace import (
    ScientificWorkspaceTemplate,
    WorkspaceFileRole,
    WorkspaceFileTemplate,
)

_README = """# DM847 Laboratory 3 workspace

This internal preparation workspace develops exact sequence indexes from first principles.
It is not an official SDU laboratory sheet.

## Research question

How can one index a reference once, then reuse that index to count and locate many exact
patterns without scanning the complete reference for every query?

## Required distinctions

- suffix-array row versus reference coordinate;
- BWT row interval versus located positions;
- `count` versus `locate`;
- exact index match versus biological origin;
- transparent educational construction versus a compressed production FM-index.

## Files

- `data/reference.fasta`: one synthetic terminated reference without the sentinel.
- `data/patterns.csv`: synthetic exact-query cases.
- `metadata/data_dictionary.csv`: provenance and interpretation limits.
- `student/sequence_index.py`: learner-owned implementation.
- `tests/test_sequence_index.py`: authored deterministic checks.
- `report.md`: learner-owned interpretation and complexity defence.
- `output/`: generated execution records.

Passing tests establishes implementation behaviour for the declared contracts. It does
not establish read origin, homology, pathogenicity, clinical relevance, or correctness
for approximate mapping.
"""

_REFERENCE = """>synthetic_reference_dm847_lab03
ACGTCGACG
"""

_PATTERNS = """pattern,expected_count,expected_positions,teaching_role
ACG,2,0;6,repeated exact pattern
CG,3,1;4;7,multimapping interval
GTC,1,2,unique exact pattern
TTA,0,,absent pattern
"""

_DICTIONARY = """field,meaning,provenance,interpretation_limit
reference,Synthetic DNA text,authored for DM847 laboratory 3,not a genome or clinical reference
pattern,Synthetic exact query,authored for deterministic tests,does not model sequencing error
expected_count,Number of exact forward-strand matches,derived from synthetic reference,not mapping confidence
expected_positions,Zero-based exact start coordinates,derived from synthetic reference,not true biological origin
sentinel,Unique terminal symbol $,added by the learner implementation,not part of the biological alphabet
"""

_SOURCE = '''"""Learner-owned suffix-array, BWT, and FM-index implementation."""

from __future__ import annotations

import csv
from pathlib import Path


def normalize_reference(sequence: str) -> str:
    """Return uppercase A/C/G/T/N sequence without whitespace."""

    raise NotImplementedError


def terminate_reference(sequence: str) -> str:
    """Return a normalized reference followed by one unique '$'."""

    raise NotImplementedError


def suffix_array(text: str) -> list[int]:
    """Return suffix starting positions in lexicographic order."""

    raise NotImplementedError


def lcp_array(text: str, suffixes: list[int]) -> list[int]:
    """Return LCP with the preceding suffix; the first value is zero."""

    raise NotImplementedError


def bwt_from_suffix_array(text: str, suffixes: list[int]) -> str:
    """Return the Burrows-Wheeler transform for a terminated text."""

    raise NotImplementedError


def build_occurrence_table(bwt: str) -> dict[str, tuple[int, ...]]:
    """Return Occ(c, k): counts of c in bwt[:k] for k=0..len(bwt)."""

    raise NotImplementedError


def build_fm_index(sequence: str) -> dict[str, object]:
    """Build text, suffix array, LCP, BWT, first occurrence, and Occ."""

    raise NotImplementedError


def backward_search(pattern: str, index: dict[str, object]) -> tuple[int, int]:
    """Return the half-open suffix-array row interval matching pattern."""

    raise NotImplementedError


def count(pattern: str, index: dict[str, object]) -> int:
    """Return the number of exact forward-strand matches."""

    raise NotImplementedError


def locate(pattern: str, index: dict[str, object]) -> list[int]:
    """Return sorted zero-based exact start positions."""

    raise NotImplementedError


def load_reference(path: str | Path) -> str:
    """Load one FASTA record and return its sequence."""

    raise NotImplementedError


def load_patterns(path: str | Path) -> list[str]:
    """Load the pattern column from the authored CSV."""

    with Path(path).open(newline="", encoding="utf-8") as handle:
        return [row["pattern"] for row in csv.DictReader(handle)]


def main() -> None:
    reference = load_reference("data/reference.fasta")
    index = build_fm_index(reference)
    for pattern in load_patterns("data/patterns.csv"):
        print(pattern, count(pattern, index), locate(pattern, index))


if __name__ == "__main__":
    main()
'''

_TESTS = '''"""Deterministic checks for the learner-owned sequence index."""

from __future__ import annotations

import importlib.util
from pathlib import Path


WORKSPACE = Path(__file__).resolve().parents[1]
SOURCE = WORKSPACE / "student" / "sequence_index.py"
SPEC = importlib.util.spec_from_file_location("student_sequence_index", SOURCE)
if SPEC is None or SPEC.loader is None:
    raise RuntimeError("Unable to load student/sequence_index.py")
MODULE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(MODULE)


def check(actual: object, expected: object, label: str) -> None:
    if actual != expected:
        raise AssertionError(f"{label}: expected {expected!r}, received {actual!r}")


check(MODULE.normalize_reference(" acg\\nTN "), "ACGTN", "normalization")
for invalid in ("ACX", "AC$G", ""):
    try:
        MODULE.normalize_reference(invalid)
    except (TypeError, ValueError):
        pass
    else:
        raise AssertionError(f"invalid reference must be rejected: {invalid!r}")

text = MODULE.terminate_reference("GATTACA")
check(text, "GATTACA$", "termination")
sa = MODULE.suffix_array(text)
check(sa, [7, 6, 4, 1, 5, 0, 3, 2], "suffix array")
check(sorted(sa), list(range(len(text))), "suffix-array permutation")
check(
    [text[position:] for position in sa],
    sorted(text[position:] for position in sa),
    "suffix-array order",
)
check(MODULE.lcp_array(text, sa), [0, 0, 1, 1, 0, 0, 0, 1], "LCP array")
check(MODULE.bwt_from_suffix_array(text, sa), "ACTGA$TA", "BWT")

reference = MODULE.load_reference(WORKSPACE / "data" / "reference.fasta")
check(reference, "ACGTCGACG", "FASTA loading")
index = MODULE.build_fm_index(reference)
check(index["text"], "ACGTCGACG$", "indexed text")
check(index["suffix_array"], [9, 6, 0, 7, 4, 1, 8, 5, 2, 3], "indexed SA")
check(index["bwt"], "GG$ATACCCG", "indexed BWT")
check(index["first"], {"$": 0, "A": 1, "C": 3, "G": 6, "T": 9}, "C table")

occ = index["occ"]
for symbol in "$ACGT":
    check(len(occ[symbol]), len(index["bwt"]) + 1, f"Occ length for {symbol}")
    check(occ[symbol][0], 0, f"Occ starts at zero for {symbol}")
    check(occ[symbol][-1], index["bwt"].count(symbol), f"Occ total for {symbol}")

check(MODULE.backward_search("ACG", index), (1, 3), "ACG interval")
check(MODULE.count("ACG", index), 2, "ACG count")
check(MODULE.locate("ACG", index), [0, 6], "ACG locate")
check(MODULE.count("CG", index), 3, "CG count")
check(MODULE.locate("CG", index), [1, 4, 7], "CG locate")
check(MODULE.locate("GTC", index), [2], "GTC locate")
check(MODULE.locate("TTA", index), [], "absent locate")

for invalid_pattern in ("", "A$", "AX"):
    try:
        MODULE.backward_search(invalid_pattern, index)
    except (TypeError, ValueError):
        pass
    else:
        raise AssertionError(f"invalid pattern must be rejected: {invalid_pattern!r}")

print("all sequence-index checks passed")
'''

_REPORT = """# Sequence-index interpretation and defence

## Index contract

State the alphabet, sentinel rule, coordinate convention, empty-pattern policy, and
forward-strand limitation.

## Manual construction

Show the sorted suffixes, suffix array, adjacent LCP values, and BWT for `GATTACA$`.
Explain one invariant used to verify each structure.

## Query interpretation

For `ACG`, `CG`, `GTC`, and `TTA`, report the backward-search interval, count, and
located positions. Separate the index result from any claim about biological origin.

## Complexity defence

Use variables `n` for reference length, `m` for pattern length, and `q` for number of
queries. Compare exhaustive search, suffix-array binary search, and this educational
FM-index in preprocessing, memory, count, and locate. Explain why a full suffix array is
retained here and how sampling would change locate.

## Limitations and extension

Discuss reverse complements, mismatches, indels, incomplete references, repetitive
regions, base quality, and the distinction between exact search and alignment. Select
one extension and justify its priority.

## Error reflection

Document the most important error, its symptom, root cause, correction, and regression
test.
"""


DM847_LAB_03_WORKSPACE = ScientificWorkspaceTemplate(
    workspace_id="dm847.lab03.workspace",
    lab_id="dm847.lab03.sequence-indexes",
    version="1.0.0",
    files=(
        WorkspaceFileTemplate("README.md", _README, WorkspaceFileRole.README),
        WorkspaceFileTemplate(
            "data/reference.fasta",
            _REFERENCE,
            WorkspaceFileRole.DATA,
        ),
        WorkspaceFileTemplate(
            "data/patterns.csv",
            _PATTERNS,
            WorkspaceFileRole.DATA,
        ),
        WorkspaceFileTemplate(
            "metadata/data_dictionary.csv",
            _DICTIONARY,
            WorkspaceFileRole.METADATA,
        ),
        WorkspaceFileTemplate(
            "student/sequence_index.py",
            _SOURCE,
            WorkspaceFileRole.SOURCE,
            editable=True,
        ),
        WorkspaceFileTemplate(
            "tests/test_sequence_index.py",
            _TESTS,
            WorkspaceFileRole.TEST,
        ),
        WorkspaceFileTemplate(
            "report.md",
            _REPORT,
            WorkspaceFileRole.REPORT,
            editable=True,
        ),
        WorkspaceFileTemplate(
            "output/.gitkeep",
            "",
            WorkspaceFileRole.OUTPUT,
        ),
    ),
    entrypoint="student/sequence_index.py",
    test_entrypoint="tests/test_sequence_index.py",
    allowed_import_roots=frozenset({"csv", "pathlib"}),
    timeout_seconds=15.0,
    output_limit=32_000,
)


__all__ = ["DM847_LAB_03_WORKSPACE"]
