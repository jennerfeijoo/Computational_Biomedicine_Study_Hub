"""Regression tests for the DM847 sequence-index laboratory."""

from __future__ import annotations

from computational_biomedicine_study_hub.content.labs import DM847_LAB_03
from computational_biomedicine_study_hub.content.labs.dm847_workspace_03 import (
    DM847_LAB_03_WORKSPACE,
)
from computational_biomedicine_study_hub.i18n.locales import AppLocale
from computational_biomedicine_study_hub.learning.computational_labs import (
    LabStage,
    LabTaskKind,
)
from computational_biomedicine_study_hub.learning.python_execution import (
    ExecutionStatus,
    PythonExecutionRequest,
    PythonSubprocessRunner,
)

_SUFFIX_REFERENCE = """def validate_terminated_text(text):
    if not isinstance(text, str):
        raise TypeError("text must be a string")
    normalized = "".join(text.split()).upper()
    if normalized.count("$") != 1 or not normalized.endswith("$"):
        raise ValueError("text requires one terminal sentinel")
    if any(symbol not in "ACGTN" for symbol in normalized[:-1]):
        raise ValueError("invalid biological symbol")
    return normalized


def suffix_array(text):
    text = validate_terminated_text(text)
    return sorted(range(len(text)), key=lambda position: text[position:])


def bwt_from_suffix_array(text, suffixes):
    text = validate_terminated_text(text)
    if sorted(suffixes) != list(range(len(text))):
        raise ValueError("suffix array must be a permutation")
    return "".join(text[position - 1] if position else text[-1] for position in suffixes)
"""

_FM_REFERENCE = """def validate_terminated_text(text):
    if not isinstance(text, str):
        raise TypeError("text must be a string")
    normalized = "".join(text.split()).upper()
    if normalized.count("$") != 1 or not normalized.endswith("$"):
        raise ValueError("text requires one terminal sentinel")
    if any(symbol not in "ACGTN" for symbol in normalized[:-1]):
        raise ValueError("invalid biological symbol")
    return normalized


def suffix_array(text):
    text = validate_terminated_text(text)
    return sorted(range(len(text)), key=lambda position: text[position:])


def bwt_from_suffix_array(text, suffixes):
    text = validate_terminated_text(text)
    if sorted(suffixes) != list(range(len(text))):
        raise ValueError("suffix array must be a permutation")
    return "".join(text[position - 1] if position else text[-1] for position in suffixes)


def build_occurrence_table(bwt):
    alphabet = sorted(set(bwt))
    table = {symbol: [0] for symbol in alphabet}
    for current in bwt:
        for symbol in alphabet:
            table[symbol].append(table[symbol][-1] + int(current == symbol))
    return {symbol: tuple(counts) for symbol, counts in table.items()}


def build_fm_index(text):
    text = validate_terminated_text(text)
    suffixes = suffix_array(text)
    bwt = bwt_from_suffix_array(text, suffixes)
    first = {}
    offset = 0
    for symbol in sorted(set(bwt)):
        first[symbol] = offset
        offset += bwt.count(symbol)
    return {
        "text": text,
        "suffix_array": suffixes,
        "bwt": bwt,
        "first": first,
        "occ": build_occurrence_table(bwt),
    }


def _normalize_pattern(pattern, index):
    if not isinstance(pattern, str):
        raise TypeError("pattern must be a string")
    normalized = "".join(pattern.split()).upper()
    if not normalized or "$" in normalized:
        raise ValueError("pattern must be non-empty and sentinel-free")
    alphabet = set(index["first"]) - {"$"}
    if any(symbol not in alphabet for symbol in normalized):
        raise ValueError("pattern contains a symbol outside the index alphabet")
    return normalized


def backward_search(pattern, index):
    pattern = _normalize_pattern(pattern, index)
    top = 0
    bottom = len(index["bwt"])
    for symbol in reversed(pattern):
        top = index["first"][symbol] + index["occ"][symbol][top]
        bottom = index["first"][symbol] + index["occ"][symbol][bottom]
        if top >= bottom:
            return top, top
    return top, bottom


def locate(pattern, index):
    top, bottom = backward_search(pattern, index)
    return sorted(index["suffix_array"][top:bottom])
"""


def test_sequence_index_lab_covers_the_complete_cycle_and_locales() -> None:
    assert tuple(task.stage for task in DM847_LAB_03.tasks) == tuple(LabStage)
    assert DM847_LAB_03.estimated_minutes == 170
    assert sum(task.kind is LabTaskKind.PYTHON for task in DM847_LAB_03.tasks) == 2
    assert len({task.task_id for task in DM847_LAB_03.tasks}) == len(DM847_LAB_03.tasks)
    for locale in AppLocale:
        assert DM847_LAB_03.title.text(locale)
        assert DM847_LAB_03.research_question.text(locale)
        assert "SDU" in DM847_LAB_03.disclaimer.text(locale)
        for task in DM847_LAB_03.tasks:
            assert task.title.text(locale)
            assert task.instructions.text(locale)
            assert task.mentor_notes.text(locale)


def test_reference_implementations_pass_both_python_checkpoints() -> None:
    runner = PythonSubprocessRunner()
    python_tasks = tuple(task for task in DM847_LAB_03.tasks if task.kind is LabTaskKind.PYTHON)
    references = (_SUFFIX_REFERENCE, _FM_REFERENCE)

    for task, reference in zip(python_tasks, references, strict=True):
        result = runner.run(
            PythonExecutionRequest(
                source=f"{reference}\n{task.verification_source}",
                expected_output=task.expected_output,
                timeout_seconds=4.0,
            )
        )
        assert result.status is ExecutionStatus.PASSED, result.stderr


def test_workspace_contains_reproducible_index_resources_without_real_data() -> None:
    paths = {item.relative_path for item in DM847_LAB_03_WORKSPACE.files}
    assert DM847_LAB_03_WORKSPACE.lab_id == DM847_LAB_03.lab_id
    assert DM847_LAB_03_WORKSPACE.entrypoint == "student/sequence_index.py"
    assert DM847_LAB_03_WORKSPACE.test_entrypoint == "tests/test_sequence_index.py"
    assert {
        "README.md",
        "data/reference.fasta",
        "data/patterns.csv",
        "metadata/data_dictionary.csv",
        "student/sequence_index.py",
        "tests/test_sequence_index.py",
        "report.md",
        "output/.gitkeep",
    } == paths

    readme = DM847_LAB_03_WORKSPACE.file("README.md").content
    report = DM847_LAB_03_WORKSPACE.file("report.md").content
    tests = DM847_LAB_03_WORKSPACE.file("tests/test_sequence_index.py").content
    assert "synthetic" in readme.casefold()
    assert "biological origin" in readme
    assert "Complexity defence" in report
    assert "all sequence-index checks passed" in tests
    assert DM847_LAB_03_WORKSPACE.file("student/sequence_index.py").editable
    assert DM847_LAB_03_WORKSPACE.file("report.md").editable
    assert not DM847_LAB_03_WORKSPACE.file("tests/test_sequence_index.py").editable
