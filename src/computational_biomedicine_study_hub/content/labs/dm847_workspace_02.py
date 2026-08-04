"""Persistent workspace for DM847 laboratory 2."""

from __future__ import annotations

from ...learning.scientific_workspace import (
    ScientificWorkspaceTemplate,
    WorkspaceFileRole,
    WorkspaceFileTemplate,
)

_DM847_ALIGNMENT_README = """# DM847 Laboratory 2 workspace

This workspace is internal preparation aligned with DM847 pairwise-alignment learning
outcomes. It is not an official SDU laboratory sheet.

## Research question

How does the optimal correspondence between two sequences change when the alignment
objective and scoring function change?

## Structure

- `data/sequence_pairs.csv`: synthetic DNA pairs for global and local alignment.
- `metadata/data_dictionary.csv`: provenance and interpretation limits.
- `student/alignment.py`: learner-owned dynamic-programming implementation.
- `tests/test_alignment.py`: authored deterministic implementation checks.
- `report.md`: learner-owned parameter analysis and algorithm defence.
- `output/`: generated execution records.

The reference tasks use linear gaps, deterministic tie-breaking, and small synthetic
sequences. Passing tests demonstrates implementation behaviour under that model. It
does not establish homology, shared function, evolutionary history, or clinical value.
"""

_DM847_ALIGNMENT_DATA = """pair_id,sequence_a,sequence_b,objective,note
pair_global_small,ACG,AG,global,one internal gap is expected
pair_local_core,TTACG,ACGAA,local,shared ACG region is embedded in flanks
pair_parameter_sensitive,ACGTT,ACTT,compare,inspect gap versus mismatch trade-off
pair_no_local,AAAA,TTTT,local,zero local optimum under default scores
pair_tie,AG,GA,compare,multiple optimal solutions may exist
"""

_DM847_ALIGNMENT_DICTIONARY = """variable,description,type,allowed_interpretation
pair_id,Synthetic pair identifier,string,local educational use only
sequence_a,First synthetic DNA sequence,string,not a patient or clinical sequence
sequence_b,Second synthetic DNA sequence,string,not a patient or clinical sequence
objective,Authored comparison objective,string,global local or parameter comparison
note,Pedagogical design note,string,not biological annotation
"""

_DM847_ALIGNMENT_SOURCE = '''"""Learner-owned pairwise alignment analysis for DM847 Laboratory 2."""

from __future__ import annotations

import csv
from pathlib import Path
from typing import Iterable


def normalize_sequence(sequence: str) -> str:
    """Return uppercase DNA without whitespace and reject invalid symbols."""

    # TODO: define and implement the sequence contract.
    raise NotImplementedError


def needleman_wunsch(
    sequence_a: str,
    sequence_b: str,
    match: int = 2,
    mismatch: int = -1,
    gap: int = -2,
) -> tuple[int, str, str]:
    """Return score and one deterministic optimal global alignment."""

    # TODO: initialize score and traceback matrices, fill them, and trace back.
    raise NotImplementedError


def smith_waterman(
    sequence_a: str,
    sequence_b: str,
    match: int = 2,
    mismatch: int = -1,
    gap: int = -2,
) -> tuple[int, str, str, tuple[int, int], tuple[int, int]]:
    """Return one deterministic optimal local alignment and half-open coordinates."""

    # TODO: add the zero reset, track the first maximum, and stop traceback at zero.
    raise NotImplementedError


def score_alignment(
    aligned_a: str,
    aligned_b: str,
    match: int = 2,
    mismatch: int = -1,
    gap: int = -2,
) -> int:
    """Recalculate the linear-gap score of an already aligned pair."""

    # TODO: reject unequal lengths and double-gap columns.
    raise NotImplementedError


def load_pairs(path: str | Path) -> list[dict[str, str]]:
    """Load the authored synthetic sequence-pair table."""

    with Path(path).open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def summarize_results(rows: Iterable[dict[str, str]]) -> None:
    """Run the authored objective for each synthetic pair and print compact evidence."""

    print("pair_id\\tobjective\\tscore\\talignment")
    for row in rows:
        if row["objective"] == "local":
            score, aligned_a, aligned_b, coordinates_a, coordinates_b = smith_waterman(
                row["sequence_a"],
                row["sequence_b"],
            )
            alignment = f"{aligned_a}/{aligned_b} {coordinates_a} {coordinates_b}"
        else:
            score, aligned_a, aligned_b = needleman_wunsch(
                row["sequence_a"],
                row["sequence_b"],
            )
            alignment = f"{aligned_a}/{aligned_b}"
        print(f"{row['pair_id']}\\t{row['objective']}\\t{score}\\t{alignment}")


def main() -> None:
    summarize_results(load_pairs("data/sequence_pairs.csv"))


if __name__ == "__main__":
    main()
'''

_DM847_ALIGNMENT_TESTS = '''"""Deterministic checks for the learner-owned alignment implementation."""

from __future__ import annotations

import importlib.util
from pathlib import Path


WORKSPACE = Path(__file__).resolve().parents[1]
SOURCE = WORKSPACE / "student" / "alignment.py"
SPEC = importlib.util.spec_from_file_location("student_alignment", SOURCE)
if SPEC is None or SPEC.loader is None:
    raise RuntimeError("Unable to load student/alignment.py")
MODULE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(MODULE)
normalize_sequence = MODULE.normalize_sequence
needleman_wunsch = MODULE.needleman_wunsch
smith_waterman = MODULE.smith_waterman
score_alignment = MODULE.score_alignment
load_pairs = MODULE.load_pairs


def check(actual: object, expected: object, label: str) -> None:
    if actual != expected:
        raise AssertionError(f"{label}: expected {expected!r}, received {actual!r}")


check(normalize_sequence(" ac g "), "ACG", "normalization")
for invalid in ("", "ACN", 123):
    try:
        normalize_sequence(invalid)
    except (TypeError, ValueError):
        pass
    else:
        raise AssertionError(f"invalid sequence {invalid!r} must be rejected")

check(needleman_wunsch("", ""), (0, "", ""), "empty global alignment")
check(needleman_wunsch("A", ""), (-2, "A", "-"), "global deletion")
check(needleman_wunsch("", "A"), (-2, "-", "A"), "global insertion")
check(needleman_wunsch("ACG", "AG"), (2, "ACG", "A-G"), "global traceback")

local = smith_waterman("TTACG", "ACGAA")
check(local, (6, "ACG", "ACG", (2, 5), (0, 3)), "local traceback")
check(smith_waterman("AAAA", "TTTT")[0], 0, "zero local optimum")

for result, original_a, original_b in (
    (needleman_wunsch("ACG", "AG"), "ACG", "AG"),
    (smith_waterman("TTACG", "ACGAA"), "ACG", "ACG"),
):
    score = result[0]
    aligned_a = result[1]
    aligned_b = result[2]
    check(len(aligned_a), len(aligned_b), "equal aligned lengths")
    check(aligned_a.replace("-", ""), original_a, "recover first sequence")
    check(aligned_b.replace("-", ""), original_b, "recover second sequence")
    check(score_alignment(aligned_a, aligned_b), score, "recomputed score")

try:
    score_alignment("A-", "A")
except ValueError:
    pass
else:
    raise AssertionError("unequal aligned lengths must be rejected")

try:
    score_alignment("-", "-")
except ValueError:
    pass
else:
    raise AssertionError("double-gap columns must be rejected")

rows = load_pairs(WORKSPACE / "data" / "sequence_pairs.csv")
check(len(rows), 5, "authored pair count")
check(rows[1]["pair_id"], "pair_local_core", "table ordering")
print("all workspace checks passed")
'''

_DM847_ALIGNMENT_REPORT = """# Pairwise-alignment interpretation and defence

## Scoring contract

State the meaning of the dynamic-programming state, initialization, recurrence, tie
policy, coordinate convention, and validation invariants.

## Global versus local objective

For each authored pair, justify whether global, local, or semiglobal alignment answers
the intended question. Identify one scenario where another objective would be misleading.

## Parameter sensitivity

Compare at least two scoring configurations. Record the score and alignment, then
separate observed changes from biological interpretation. Discuss ties and stability.

## Traceback validation

Show that aligned strings have equal length, removing gaps recovers the intended input
region, and recalculating the score reproduces the matrix optimum.

## Complexity and model limits

Explain O(nm) time and memory, score-only memory reduction, the information required for
traceback, and why affine gaps require additional states. State the limitations of
synthetic sequences, linear gaps, deterministic tie-breaking, and absence of a null model.

## Biological interpretation

Explain why an optimal score is conditional on the scoring model and does not alone
establish homology, function, evolutionary history, pathogenicity, or clinical value.

## Error reflection

Document the most important error, the evidence that exposed it, the correction, and a
deterministic test that prevents recurrence.
"""


DM847_LAB_02_WORKSPACE = ScientificWorkspaceTemplate(
    workspace_id="dm847.lab02.workspace",
    lab_id="dm847.lab02.pairwise-alignment",
    version="1.0.0",
    files=(
        WorkspaceFileTemplate(
            "README.md",
            _DM847_ALIGNMENT_README,
            WorkspaceFileRole.README,
        ),
        WorkspaceFileTemplate(
            "data/sequence_pairs.csv",
            _DM847_ALIGNMENT_DATA,
            WorkspaceFileRole.DATA,
        ),
        WorkspaceFileTemplate(
            "metadata/data_dictionary.csv",
            _DM847_ALIGNMENT_DICTIONARY,
            WorkspaceFileRole.METADATA,
        ),
        WorkspaceFileTemplate(
            "student/alignment.py",
            _DM847_ALIGNMENT_SOURCE,
            WorkspaceFileRole.SOURCE,
            editable=True,
        ),
        WorkspaceFileTemplate(
            "tests/test_alignment.py",
            _DM847_ALIGNMENT_TESTS,
            WorkspaceFileRole.TEST,
        ),
        WorkspaceFileTemplate(
            "report.md",
            _DM847_ALIGNMENT_REPORT,
            WorkspaceFileRole.REPORT,
            editable=True,
        ),
        WorkspaceFileTemplate(
            "output/.gitkeep",
            "",
            WorkspaceFileRole.OUTPUT,
        ),
    ),
    entrypoint="student/alignment.py",
    test_entrypoint="tests/test_alignment.py",
    allowed_import_roots=frozenset({"csv", "pathlib", "typing"}),
    timeout_seconds=12.0,
    output_limit=32_000,
)


__all__ = ["DM847_LAB_02_WORKSPACE"]
