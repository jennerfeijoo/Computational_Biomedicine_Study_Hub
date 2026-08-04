"""Authored multi-file workspace for DM847 Laboratory 1."""

from __future__ import annotations

from ...learning.scientific_workspace import (
    ScientificWorkspaceTemplate,
    WorkspaceFileRole,
    WorkspaceFileTemplate,
)

_README = """# DM847 Laboratory 1 workspace

This internal preparation workspace develops exact and substitution-tolerant short-read
mapping from first principles. It is aligned with DM847 themes in sequence
representation, matching, indexing, and interpretation, but it is not an official SDU
laboratory sheet.

## Research question

How do candidate positions and mapping uncertainty change when a short read is allowed
to differ from a reference by a bounded number of substitutions?

## Structure

- `data/reference.fasta`: one synthetic reference sequence.
- `data/reads.fastq`: synthetic reads with deterministic high quality symbols.
- `metadata/data_dictionary.csv`: provenance and interpretation constraints.
- `student/mapper.py`: learner-owned implementation and command-line analysis.
- `tests/test_mapper.py`: authored deterministic checks.
- `report.md`: learner-owned interpretation and algorithm defence.
- `output/`: generated execution records.

The implementation deliberately uses exhaustive window scanning. This makes every
candidate and mismatch count inspectable. It is a correctness reference for small
synthetic data, not a scalable replacement for production read mappers.

Passing the authored tests establishes behaviour under the declared contract. It does
not establish biological origin, variant status, expression, or clinical validity.
"""

_REFERENCE = """>synthetic_reference_dm847_lab01
ACGTTGCATGTCGCATGATGCATGAGAGCT
"""

_READS = """@read_unique
GATGC
+
IIIII
@read_multimapping
GCATG
+
IIIII
@read_one_substitution
ACGTA
+
IIIII
@read_unmapped
TTTTT
+
IIIII
"""

_DICTIONARY = """resource,field,description,interpretation_constraint
reference.fasta,sequence,Synthetic 32-base DNA reference,Educational use only; not a genome or clinical reference
reads.fastq,read_unique,Exact match at one zero-based position,Uniqueness is conditional on this synthetic reference and search model
reads.fastq,read_multimapping,Exact match at several positions,Do not select one position without an explicit policy
reads.fastq,read_one_substitution,One candidate when one substitution is allowed,A mismatch is not automatically a biological variant
reads.fastq,read_unmapped,No candidate with at most one substitution,Absence of a candidate does not prove absence from a biological sample
reads.fastq,quality,Deterministic ASCII I symbols,Quality scores are illustrative and are not used by this mapper
"""

_SOURCE = '''"""Learner-owned mapper for DM847 Laboratory 1."""

from __future__ import annotations

from pathlib import Path
from typing import Iterable


def normalize_dna(sequence: str) -> str:
    """Return uppercase DNA without whitespace under an A/C/G/T-only contract."""

    # TODO: normalize and validate one non-empty sequence.
    raise NotImplementedError


def hamming_distance(left: str, right: str) -> int:
    """Return substitutions between equal-length normalized DNA sequences."""

    # TODO: reject unequal lengths and count differing positions.
    raise NotImplementedError


def find_matches(
    reference: str,
    read: str,
    max_mismatches: int = 0,
) -> list[tuple[int, int]]:
    """Return zero-based (position, mismatch_count) candidates in position order."""

    # TODO: validate the mismatch limit and scan every complete reference window.
    raise NotImplementedError


def classify_mapping(matches: Iterable[tuple[int, int]]) -> str:
    """Classify candidates as unmapped, unique, or multimapping."""

    # TODO: classification depends only on the number of candidate positions.
    raise NotImplementedError


def load_reference(path: str | Path) -> str:
    """Load exactly one FASTA record from the synthetic workspace."""

    lines = [line.strip() for line in Path(path).read_text(encoding="utf-8").splitlines()]
    sequence_lines = [line for line in lines if line and not line.startswith(">")]
    if not sequence_lines:
        raise ValueError("The FASTA file does not contain a sequence.")
    return normalize_dna("".join(sequence_lines))


def load_reads(path: str | Path) -> list[tuple[str, str, str]]:
    """Load strict four-line FASTQ records as (identifier, sequence, quality)."""

    lines = Path(path).read_text(encoding="utf-8").splitlines()
    if len(lines) % 4 != 0:
        raise ValueError("FASTQ content must contain complete four-line records.")
    reads: list[tuple[str, str, str]] = []
    for index in range(0, len(lines), 4):
        identifier, sequence, separator, quality = lines[index : index + 4]
        if not identifier.startswith("@") or separator != "+":
            raise ValueError("FASTQ record markers are malformed.")
        normalized = normalize_dna(sequence)
        if len(normalized) != len(quality):
            raise ValueError("FASTQ sequence and quality lengths differ.")
        reads.append((identifier[1:], normalized, quality))
    return reads


def main() -> None:
    reference = load_reference("data/reference.fasta")
    reads = load_reads("data/reads.fastq")
    print("read_id\\tclassification\\tcandidates")
    for read_id, sequence, _quality in reads:
        matches = find_matches(reference, sequence, max_mismatches=1)
        print(f"{read_id}\\t{classify_mapping(matches)}\\t{matches}")


if __name__ == "__main__":
    main()
'''

_TESTS = '''"""Deterministic checks for the learner-owned DM847 mapper."""

from __future__ import annotations

import importlib.util
from pathlib import Path


WORKSPACE = Path(__file__).resolve().parents[1]
SOURCE = WORKSPACE / "student" / "mapper.py"
SPEC = importlib.util.spec_from_file_location("student_mapper", SOURCE)
if SPEC is None or SPEC.loader is None:
    raise RuntimeError("Unable to load student/mapper.py")
MODULE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(MODULE)

normalize_dna = MODULE.normalize_dna
hamming_distance = MODULE.hamming_distance
find_matches = MODULE.find_matches
classify_mapping = MODULE.classify_mapping
load_reference = MODULE.load_reference
load_reads = MODULE.load_reads


def check(actual: object, expected: object, label: str) -> None:
    if actual != expected:
        raise AssertionError(f"{label}: expected {expected!r}, received {actual!r}")


check(normalize_dna(" ac gt\\n"), "ACGT", "normalization")
for invalid in ("", "ACGN", "ACG-", "123"):
    try:
        normalize_dna(invalid)
    except ValueError:
        pass
    else:
        raise AssertionError(f"normalize_dna must reject {invalid!r}")

check(hamming_distance("ACGTT", "ACGTA"), 1, "single substitution")
check(hamming_distance("AAAA", "TTTT"), 4, "all positions differ")
try:
    hamming_distance("ACG", "ACGT")
except ValueError:
    pass
else:
    raise AssertionError("Unequal lengths must raise ValueError")

reference = load_reference(WORKSPACE / "data" / "reference.fasta")
check(reference, "ACGTTGCATGTCGCATGATGCATGAGAGCT", "FASTA loading")
reads = load_reads(WORKSPACE / "data" / "reads.fastq")
check([read_id for read_id, _sequence, _quality in reads], [
    "read_unique",
    "read_multimapping",
    "read_one_substitution",
    "read_unmapped",
], "FASTQ identifiers")

check(find_matches(reference, "GATGC", 0), [(16, 0)], "unique exact match")
check(
    find_matches(reference, "GCATG", 0),
    [(5, 0), (12, 0), (19, 0)],
    "exact multimapping",
)
check(find_matches(reference, "ACGTA", 0), [], "exact mismatch rejection")
check(find_matches(reference, "ACGTA", 1), [(0, 1)], "one-substitution match")
check(find_matches(reference, "TTTTT", 1), [], "unmapped read")
check(find_matches("AAAAA", "AAA", 0), [(0, 0), (1, 0), (2, 0)], "overlap")

for invalid_limit in (-1, 1.5, True):
    try:
        find_matches("ACGT", "ACG", invalid_limit)
    except (TypeError, ValueError):
        pass
    else:
        raise AssertionError(f"Mismatch limit {invalid_limit!r} must be rejected")
try:
    find_matches("ACGT", "ACGTA", 1)
except ValueError:
    pass
else:
    raise AssertionError("A read longer than the reference must raise ValueError")

check(classify_mapping([]), "unmapped", "unmapped classification")
check(classify_mapping([(16, 0)]), "unique", "unique classification")
check(
    classify_mapping([(5, 0), (12, 0), (19, 0)]),
    "multimapping",
    "multimapping classification",
)
print("all workspace checks passed")
'''

_REPORT = """# DM847 Laboratory 1 report

## Input and algorithm contract

State the accepted alphabet, normalization rules, mismatch-limit rules, coordinates, and
error behaviour. Explain why Hamming distance excludes insertions and deletions.

## Candidate evidence

For each synthetic read, report exact and one-substitution candidates as
`(zero-based position, mismatch count)`. Distinguish no mapping, unique mapping, and
multimapping.

## Biological interpretation limits

Explain why a unique candidate is not automatically the true biological origin. Address
at least reference completeness, repeats, reverse-complement mapping, base quality,
insertions/deletions, and the policy for multimapping reads.

## Algorithmic defence

Give time complexity in terms of reference length, read length, and number of reads.
Compare exhaustive scanning with a suffix array or FM-index, including construction,
memory, candidate verification, and approximate matching.

## Error reflection

Document one consequential implementation error, the input that exposed it, the
correction, and the regression test that prevents recurrence.
"""


DM847_LAB_01_WORKSPACE = ScientificWorkspaceTemplate(
    workspace_id="dm847.lab01.workspace",
    lab_id="dm847.lab01.short-read-mapping",
    version="1.0.0",
    files=(
        WorkspaceFileTemplate("README.md", _README, WorkspaceFileRole.README),
        WorkspaceFileTemplate(
            "data/reference.fasta",
            _REFERENCE,
            WorkspaceFileRole.DATA,
        ),
        WorkspaceFileTemplate(
            "data/reads.fastq",
            _READS,
            WorkspaceFileRole.DATA,
        ),
        WorkspaceFileTemplate(
            "metadata/data_dictionary.csv",
            _DICTIONARY,
            WorkspaceFileRole.METADATA,
        ),
        WorkspaceFileTemplate(
            "student/mapper.py",
            _SOURCE,
            WorkspaceFileRole.SOURCE,
            editable=True,
        ),
        WorkspaceFileTemplate(
            "tests/test_mapper.py",
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
    entrypoint="student/mapper.py",
    test_entrypoint="tests/test_mapper.py",
    allowed_import_roots=frozenset({"pathlib", "typing"}),
    timeout_seconds=15.0,
    output_limit=32_000,
)

__all__ = ["DM847_LAB_01_WORKSPACE"]
