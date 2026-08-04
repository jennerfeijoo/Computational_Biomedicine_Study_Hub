"""Regression tests for the DM847 short-read mapping laboratory."""

from __future__ import annotations

from pathlib import Path

from computational_biomedicine_study_hub.content.labs import (
    DM847_LAB_01,
    WORKSPACE_TEMPLATES,
)
from computational_biomedicine_study_hub.content.labs.dm847_workspace_01 import (
    DM847_LAB_01_WORKSPACE,
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

_REFERENCE_IMPLEMENTATION = """def normalize_dna(sequence):
    if not isinstance(sequence, str):
        raise TypeError("sequence must be text")
    normalized = "".join(sequence.split()).upper()
    if not normalized:
        raise ValueError("sequence cannot be empty")
    if any(base not in "ACGT" for base in normalized):
        raise ValueError("sequence must contain only A, C, G, and T")
    return normalized


def hamming_distance(left, right):
    normalized_left = normalize_dna(left)
    normalized_right = normalize_dna(right)
    if len(normalized_left) != len(normalized_right):
        raise ValueError("Hamming distance requires equal lengths")
    return sum(a != b for a, b in zip(normalized_left, normalized_right, strict=True))


def find_matches(reference, read, max_mismatches=0):
    if isinstance(max_mismatches, bool) or not isinstance(max_mismatches, int):
        raise TypeError("max_mismatches must be an integer")
    if max_mismatches < 0:
        raise ValueError("max_mismatches cannot be negative")
    normalized_reference = normalize_dna(reference)
    normalized_read = normalize_dna(read)
    if len(normalized_read) > len(normalized_reference):
        raise ValueError("read cannot be longer than reference")
    matches = []
    final_start = len(normalized_reference) - len(normalized_read)
    for position in range(final_start + 1):
        window = normalized_reference[position : position + len(normalized_read)]
        mismatches = hamming_distance(window, normalized_read)
        if mismatches <= max_mismatches:
            matches.append((position, mismatches))
    return matches


def classify_mapping(matches):
    candidates = list(matches)
    if not candidates:
        return "unmapped"
    if len(candidates) == 1:
        return "unique"
    return "multimapping"
"""

_WORKSPACE_IMPLEMENTATION = '''"""Reference implementation used only by automated tests."""

from __future__ import annotations

from pathlib import Path
from typing import Iterable


def normalize_dna(sequence: str) -> str:
    if not isinstance(sequence, str):
        raise TypeError("sequence must be text")
    normalized = "".join(sequence.split()).upper()
    if not normalized:
        raise ValueError("sequence cannot be empty")
    if any(base not in "ACGT" for base in normalized):
        raise ValueError("sequence must contain only A, C, G, and T")
    return normalized


def hamming_distance(left: str, right: str) -> int:
    left_normalized = normalize_dna(left)
    right_normalized = normalize_dna(right)
    if len(left_normalized) != len(right_normalized):
        raise ValueError("Hamming distance requires equal lengths")
    return sum(
        left_base != right_base
        for left_base, right_base in zip(
            left_normalized,
            right_normalized,
            strict=True,
        )
    )


def find_matches(
    reference: str,
    read: str,
    max_mismatches: int = 0,
) -> list[tuple[int, int]]:
    if isinstance(max_mismatches, bool) or not isinstance(max_mismatches, int):
        raise TypeError("max_mismatches must be an integer")
    if max_mismatches < 0:
        raise ValueError("max_mismatches cannot be negative")
    normalized_reference = normalize_dna(reference)
    normalized_read = normalize_dna(read)
    if len(normalized_read) > len(normalized_reference):
        raise ValueError("read cannot be longer than reference")
    matches: list[tuple[int, int]] = []
    for position in range(len(normalized_reference) - len(normalized_read) + 1):
        window = normalized_reference[position : position + len(normalized_read)]
        mismatches = hamming_distance(window, normalized_read)
        if mismatches <= max_mismatches:
            matches.append((position, mismatches))
    return matches


def classify_mapping(matches: Iterable[tuple[int, int]]) -> str:
    candidates = list(matches)
    if not candidates:
        return "unmapped"
    if len(candidates) == 1:
        return "unique"
    return "multimapping"


def load_reference(path: str | Path) -> str:
    lines = [line.strip() for line in Path(path).read_text(encoding="utf-8").splitlines()]
    sequence_lines = [line for line in lines if line and not line.startswith(">")]
    if not sequence_lines:
        raise ValueError("The FASTA file does not contain a sequence.")
    return normalize_dna("".join(sequence_lines))


def load_reads(path: str | Path) -> list[tuple[str, str, str]]:
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


def test_dm847_python_checkpoints_accept_the_reference_algorithm() -> None:
    runner = PythonSubprocessRunner()
    tasks = tuple(task for task in DM847_LAB_01.tasks if task.kind is LabTaskKind.PYTHON)

    assert len(tasks) == 2
    for task in tasks:
        result = runner.run(
            PythonExecutionRequest(
                source=f"{_REFERENCE_IMPLEMENTATION}\n{task.verification_source}",
                expected_output=task.expected_output,
                timeout_seconds=4.0,
            )
        )
        assert result.status is ExecutionStatus.PASSED, result.stderr


def test_dm847_workspace_is_registered_with_reproducible_resources() -> None:
    assert WORKSPACE_TEMPLATES[DM847_LAB_01.lab_id] is DM847_LAB_01_WORKSPACE
    assert DM847_LAB_01_WORKSPACE.entrypoint == "student/mapper.py"
    assert DM847_LAB_01_WORKSPACE.test_entrypoint == "tests/test_mapper.py"
    assert {item.relative_path for item in DM847_LAB_01_WORKSPACE.files} >= {
        "README.md",
        "data/reference.fasta",
        "data/reads.fastq",
        "metadata/data_dictionary.csv",
        "student/mapper.py",
        "tests/test_mapper.py",
        "report.md",
    }
    assert {item.relative_path for item in DM847_LAB_01_WORKSPACE.editable_files} == {
        "student/mapper.py",
        "report.md",
    }


def test_dm847_workspace_reference_implementation_passes_script_and_tests(
    tmp_path: Path,
) -> None:
    manager = ScientificWorkspaceManager(tmp_path)
    workspace = manager.materialize(DM847_LAB_01_WORKSPACE)
    manager.write_text(
        DM847_LAB_01_WORKSPACE,
        "student/mapper.py",
        _WORKSPACE_IMPLEMENTATION,
    )
    runner = ScientificWorkspaceRunner()

    run_result = runner.run(
        DM847_LAB_01_WORKSPACE,
        workspace,
        WorkspaceExecutionMode.RUN,
    )
    test_result = runner.run(
        DM847_LAB_01_WORKSPACE,
        workspace,
        WorkspaceExecutionMode.TEST,
    )

    assert run_result.status is WorkspaceExecutionStatus.PASSED, run_result.stderr
    assert "read_unique\tmultimapping" in run_result.stdout
    assert "read_one_substitution\tunique\t[(0, 1)]" in run_result.stdout
    assert "read_unmapped\tunmapped\t[]" in run_result.stdout
    assert test_result.status is WorkspaceExecutionStatus.PASSED, test_result.stderr
    assert "all workspace checks passed" in test_result.stdout
