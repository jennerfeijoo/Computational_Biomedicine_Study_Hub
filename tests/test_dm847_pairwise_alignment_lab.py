"""Regression tests for the DM847 pairwise-alignment laboratory."""

from __future__ import annotations

from pathlib import Path

from computational_biomedicine_study_hub.content.labs import (
    DM847_LAB_02,
    WORKSPACE_TEMPLATES,
)
from computational_biomedicine_study_hub.content.labs.dm847_workspace_02 import (
    DM847_LAB_02_WORKSPACE,
)
from computational_biomedicine_study_hub.learning.computational_labs import LabTaskKind
from computational_biomedicine_study_hub.learning.python_execution import (
    ExecutionStatus,
    PythonExecutionRequest,
    PythonSubprocessRunner,
)
from computational_biomedicine_study_hub.learning.scientific_workspace import (
    WorkspaceExecutionMode,
    WorkspaceExecutionStatus,
)
from computational_biomedicine_study_hub.learning.scientific_workspace_execution import (
    ScientificWorkspaceRunner,
)
from computational_biomedicine_study_hub.storage.scientific_workspace_manager import (
    ScientificWorkspaceManager,
)

_CHECKPOINT_IMPLEMENTATION = """def normalize_sequence(sequence):
    if not isinstance(sequence, str):
        raise TypeError("sequence must be text")
    normalized = "".join(sequence.split()).upper()
    if not normalized:
        raise ValueError("sequence cannot be empty")
    if any(base not in "ACGT" for base in normalized):
        raise ValueError("sequence must contain only A, C, G, and T")
    return normalized


def needleman_wunsch_score(sequence_a, sequence_b, match=2, mismatch=-1, gap=-2):
    sequence_a = "".join(sequence_a.split()).upper()
    sequence_b = "".join(sequence_b.split()).upper()
    matrix = [[0] * (len(sequence_b) + 1) for _ in range(len(sequence_a) + 1)]
    for i in range(1, len(sequence_a) + 1):
        matrix[i][0] = i * gap
    for j in range(1, len(sequence_b) + 1):
        matrix[0][j] = j * gap
    for i, left in enumerate(sequence_a, start=1):
        for j, right in enumerate(sequence_b, start=1):
            substitution = match if left == right else mismatch
            matrix[i][j] = max(
                matrix[i - 1][j - 1] + substitution,
                matrix[i - 1][j] + gap,
                matrix[i][j - 1] + gap,
            )
    return matrix[-1][-1]


def needleman_wunsch(sequence_a, sequence_b, match=2, mismatch=-1, gap=-2):
    sequence_a = normalize_sequence(sequence_a) if sequence_a else ""
    sequence_b = normalize_sequence(sequence_b) if sequence_b else ""
    rows = len(sequence_a) + 1
    columns = len(sequence_b) + 1
    scores = [[0] * columns for _ in range(rows)]
    pointers = [[""] * columns for _ in range(rows)]
    for i in range(1, rows):
        scores[i][0] = i * gap
        pointers[i][0] = "U"
    for j in range(1, columns):
        scores[0][j] = j * gap
        pointers[0][j] = "L"
    for i in range(1, rows):
        for j in range(1, columns):
            diagonal = scores[i - 1][j - 1] + (
                match if sequence_a[i - 1] == sequence_b[j - 1] else mismatch
            )
            up = scores[i - 1][j] + gap
            left = scores[i][j - 1] + gap
            best = max(diagonal, up, left)
            scores[i][j] = best
            pointers[i][j] = "D" if diagonal == best else ("U" if up == best else "L")
    aligned_a = []
    aligned_b = []
    i = len(sequence_a)
    j = len(sequence_b)
    while i or j:
        pointer = pointers[i][j]
        if pointer == "D":
            aligned_a.append(sequence_a[i - 1])
            aligned_b.append(sequence_b[j - 1])
            i -= 1
            j -= 1
        elif pointer == "U":
            aligned_a.append(sequence_a[i - 1])
            aligned_b.append("-")
            i -= 1
        else:
            aligned_a.append("-")
            aligned_b.append(sequence_b[j - 1])
            j -= 1
    return scores[-1][-1], "".join(reversed(aligned_a)), "".join(reversed(aligned_b))


def smith_waterman(sequence_a, sequence_b, match=2, mismatch=-1, gap=-2):
    sequence_a = normalize_sequence(sequence_a)
    sequence_b = normalize_sequence(sequence_b)
    rows = len(sequence_a) + 1
    columns = len(sequence_b) + 1
    scores = [[0] * columns for _ in range(rows)]
    pointers = [["0"] * columns for _ in range(rows)]
    best_score = 0
    best_position = (0, 0)
    for i in range(1, rows):
        for j in range(1, columns):
            diagonal = scores[i - 1][j - 1] + (
                match if sequence_a[i - 1] == sequence_b[j - 1] else mismatch
            )
            up = scores[i - 1][j] + gap
            left = scores[i][j - 1] + gap
            best = max(0, diagonal, up, left)
            scores[i][j] = best
            if best == 0:
                pointers[i][j] = "0"
            elif diagonal == best:
                pointers[i][j] = "D"
            elif up == best:
                pointers[i][j] = "U"
            else:
                pointers[i][j] = "L"
            if best > best_score:
                best_score = best
                best_position = (i, j)
    i, j = best_position
    end_a, end_b = i, j
    aligned_a = []
    aligned_b = []
    while i > 0 and j > 0 and scores[i][j] > 0:
        pointer = pointers[i][j]
        if pointer == "D":
            aligned_a.append(sequence_a[i - 1])
            aligned_b.append(sequence_b[j - 1])
            i -= 1
            j -= 1
        elif pointer == "U":
            aligned_a.append(sequence_a[i - 1])
            aligned_b.append("-")
            i -= 1
        elif pointer == "L":
            aligned_a.append("-")
            aligned_b.append(sequence_b[j - 1])
            j -= 1
        else:
            break
    return (
        best_score,
        "".join(reversed(aligned_a)),
        "".join(reversed(aligned_b)),
        (i, end_a),
        (j, end_b),
    )
"""

_WORKSPACE_IMPLEMENTATION = '''"""Reference implementation used only by automated tests."""

from __future__ import annotations

import csv
from pathlib import Path
from typing import Iterable


def normalize_sequence(sequence: str) -> str:
    if not isinstance(sequence, str):
        raise TypeError("sequence must be text")
    normalized = "".join(sequence.split()).upper()
    if not normalized:
        raise ValueError("sequence cannot be empty")
    if any(base not in "ACGT" for base in normalized):
        raise ValueError("sequence must contain only A, C, G, and T")
    return normalized


def needleman_wunsch(
    sequence_a: str,
    sequence_b: str,
    match: int = 2,
    mismatch: int = -1,
    gap: int = -2,
) -> tuple[int, str, str]:
    sequence_a = normalize_sequence(sequence_a) if sequence_a else ""
    sequence_b = normalize_sequence(sequence_b) if sequence_b else ""
    rows = len(sequence_a) + 1
    columns = len(sequence_b) + 1
    scores = [[0] * columns for _ in range(rows)]
    pointers = [[""] * columns for _ in range(rows)]
    for i in range(1, rows):
        scores[i][0] = i * gap
        pointers[i][0] = "U"
    for j in range(1, columns):
        scores[0][j] = j * gap
        pointers[0][j] = "L"
    for i in range(1, rows):
        for j in range(1, columns):
            diagonal = scores[i - 1][j - 1] + (
                match if sequence_a[i - 1] == sequence_b[j - 1] else mismatch
            )
            up = scores[i - 1][j] + gap
            left = scores[i][j - 1] + gap
            best = max(diagonal, up, left)
            scores[i][j] = best
            pointers[i][j] = "D" if diagonal == best else ("U" if up == best else "L")
    aligned_a: list[str] = []
    aligned_b: list[str] = []
    i = len(sequence_a)
    j = len(sequence_b)
    while i or j:
        pointer = pointers[i][j]
        if pointer == "D":
            aligned_a.append(sequence_a[i - 1])
            aligned_b.append(sequence_b[j - 1])
            i -= 1
            j -= 1
        elif pointer == "U":
            aligned_a.append(sequence_a[i - 1])
            aligned_b.append("-")
            i -= 1
        else:
            aligned_a.append("-")
            aligned_b.append(sequence_b[j - 1])
            j -= 1
    return scores[-1][-1], "".join(reversed(aligned_a)), "".join(reversed(aligned_b))


def smith_waterman(
    sequence_a: str,
    sequence_b: str,
    match: int = 2,
    mismatch: int = -1,
    gap: int = -2,
) -> tuple[int, str, str, tuple[int, int], tuple[int, int]]:
    sequence_a = normalize_sequence(sequence_a)
    sequence_b = normalize_sequence(sequence_b)
    rows = len(sequence_a) + 1
    columns = len(sequence_b) + 1
    scores = [[0] * columns for _ in range(rows)]
    pointers = [["0"] * columns for _ in range(rows)]
    best_score = 0
    best_position = (0, 0)
    for i in range(1, rows):
        for j in range(1, columns):
            diagonal = scores[i - 1][j - 1] + (
                match if sequence_a[i - 1] == sequence_b[j - 1] else mismatch
            )
            up = scores[i - 1][j] + gap
            left = scores[i][j - 1] + gap
            best = max(0, diagonal, up, left)
            scores[i][j] = best
            if best == 0:
                pointers[i][j] = "0"
            elif diagonal == best:
                pointers[i][j] = "D"
            elif up == best:
                pointers[i][j] = "U"
            else:
                pointers[i][j] = "L"
            if best > best_score:
                best_score = best
                best_position = (i, j)
    i, j = best_position
    end_a, end_b = i, j
    aligned_a: list[str] = []
    aligned_b: list[str] = []
    while i > 0 and j > 0 and scores[i][j] > 0:
        pointer = pointers[i][j]
        if pointer == "D":
            aligned_a.append(sequence_a[i - 1])
            aligned_b.append(sequence_b[j - 1])
            i -= 1
            j -= 1
        elif pointer == "U":
            aligned_a.append(sequence_a[i - 1])
            aligned_b.append("-")
            i -= 1
        elif pointer == "L":
            aligned_a.append("-")
            aligned_b.append(sequence_b[j - 1])
            j -= 1
        else:
            break
    return (
        best_score,
        "".join(reversed(aligned_a)),
        "".join(reversed(aligned_b)),
        (i, end_a),
        (j, end_b),
    )


def score_alignment(
    aligned_a: str,
    aligned_b: str,
    match: int = 2,
    mismatch: int = -1,
    gap: int = -2,
) -> int:
    if len(aligned_a) != len(aligned_b):
        raise ValueError("aligned sequences must have equal length")
    score = 0
    for left, right in zip(aligned_a, aligned_b, strict=True):
        if left == "-" and right == "-":
            raise ValueError("double-gap columns are invalid")
        if left == "-" or right == "-":
            score += gap
        elif left == right:
            score += match
        else:
            score += mismatch
    return score


def load_pairs(path: str | Path) -> list[dict[str, str]]:
    with Path(path).open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def summarize_results(rows: Iterable[dict[str, str]]) -> None:
    print("pair_id\\tobjective\\tscore\\talignment")
    for row in rows:
        if row["objective"] == "local":
            score, aligned_a, aligned_b, coordinates_a, coordinates_b = smith_waterman(
                row["sequence_a"], row["sequence_b"]
            )
            alignment = f"{aligned_a}/{aligned_b} {coordinates_a} {coordinates_b}"
        else:
            score, aligned_a, aligned_b = needleman_wunsch(
                row["sequence_a"], row["sequence_b"]
            )
            alignment = f"{aligned_a}/{aligned_b}"
        print(f"{row['pair_id']}\\t{row['objective']}\\t{score}\\t{alignment}")


def main() -> None:
    summarize_results(load_pairs("data/sequence_pairs.csv"))


if __name__ == "__main__":
    main()
'''


def test_dm847_alignment_checkpoints_accept_reference_algorithms() -> None:
    runner = PythonSubprocessRunner()
    tasks = tuple(task for task in DM847_LAB_02.tasks if task.kind is LabTaskKind.PYTHON)

    assert len(tasks) == 2
    for task in tasks:
        result = runner.run(
            PythonExecutionRequest(
                source=f"{_CHECKPOINT_IMPLEMENTATION}\n{task.verification_source}",
                expected_output=task.expected_output,
                timeout_seconds=4.0,
            )
        )
        assert result.status is ExecutionStatus.PASSED, result.stderr


def test_dm847_alignment_workspace_is_registered_and_reproducible() -> None:
    assert WORKSPACE_TEMPLATES[DM847_LAB_02.lab_id] is DM847_LAB_02_WORKSPACE
    assert DM847_LAB_02_WORKSPACE.entrypoint == "student/alignment.py"
    assert DM847_LAB_02_WORKSPACE.test_entrypoint == "tests/test_alignment.py"
    assert {item.relative_path for item in DM847_LAB_02_WORKSPACE.files} >= {
        "README.md",
        "data/sequence_pairs.csv",
        "metadata/data_dictionary.csv",
        "student/alignment.py",
        "tests/test_alignment.py",
        "report.md",
    }
    assert {item.relative_path for item in DM847_LAB_02_WORKSPACE.editable_files} == {
        "student/alignment.py",
        "report.md",
    }


def test_dm847_alignment_workspace_reference_implementation_passes(
    tmp_path: Path,
) -> None:
    manager = ScientificWorkspaceManager(tmp_path)
    workspace = manager.materialize(DM847_LAB_02_WORKSPACE)
    manager.write_text(
        DM847_LAB_02_WORKSPACE,
        "student/alignment.py",
        _WORKSPACE_IMPLEMENTATION,
    )
    runner = ScientificWorkspaceRunner()

    run_result = runner.run(
        DM847_LAB_02_WORKSPACE,
        workspace,
        WorkspaceExecutionMode.RUN,
    )
    test_result = runner.run(
        DM847_LAB_02_WORKSPACE,
        workspace,
        WorkspaceExecutionMode.TEST,
    )

    assert run_result.status is WorkspaceExecutionStatus.PASSED, run_result.stderr
    assert "pair_global_small\tglobal\t2\tACG/A-G" in run_result.stdout
    assert "pair_local_core\tlocal\t6\tACG/ACG (2, 5) (0, 3)" in run_result.stdout
    assert test_result.status is WorkspaceExecutionStatus.PASSED, test_result.stderr
    assert "all workspace checks passed" in test_result.stdout
