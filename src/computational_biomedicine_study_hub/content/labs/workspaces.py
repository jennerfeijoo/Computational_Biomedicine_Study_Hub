"""Authored multi-file workspace templates for computational laboratories."""

from __future__ import annotations

from ...learning.scientific_workspace import (
    ScientificWorkspaceTemplate,
    WorkspaceFileRole,
    WorkspaceFileTemplate,
)

_DM857_README = """# DM857 Laboratory 1 workspace

This workspace is internal preparation aligned with DM857 learning outcomes. It is not
an official SDU laboratory sheet.

## Research question

How can potentially dirty physiological measurements be transformed into a reliable,
defensible summary without turning a data-quality rule into a clinical conclusion?

## Structure

- `data/measurements.csv`: synthetic measurements used for local development.
- `metadata/data_dictionary.csv`: variable definitions and provenance.
- `student/analysis.py`: learner-owned implementation.
- `tests/test_analysis.py`: authored deterministic checks.
- `report.md`: learner-owned interpretation and design defence.
- `output/`: generated execution records.

Run the script to inspect its current behaviour. Run the tests to validate normal,
boundary, and invalid inputs. Passing tests are evidence of implementation behaviour,
not evidence of clinical validity.
"""

_DM857_DATA = """measurement_id,value,unit,source_note
m01,72,bpm,synthetic resting value
m02,80,bpm,synthetic resting value
m03,250,bpm,synthetic out-of-range value
m04,,bpm,synthetic missing value
m05,60,bpm,synthetic resting value
"""

_DM857_DICTIONARY = """variable,description,type,allowed_use
measurement_id,Synthetic row identifier,string,local educational analysis only
value,Generic physiological measurement,float or missing,not for clinical use
unit,Illustrative unit,string,interpret only with provenance
source_note,Synthetic provenance note,string,educational context
"""

_DM857_SOURCE = '''"""Learner-owned analysis for DM857 Laboratory 1."""

from __future__ import annotations

import csv
from pathlib import Path
from typing import Iterable


def summarize_measurements(
    values: Iterable[object],
    lower: float,
    upper: float,
) -> tuple[int, int, float | None]:
    """Return valid count, invalid count, and rounded mean for inclusive bounds."""

    # TODO: implement the input contract from the laboratory.
    raise NotImplementedError


def load_measurements(path: str | Path) -> list[float | None]:
    """Load the synthetic CSV while preserving missing measurements as None."""

    measurements: list[float | None] = []
    with Path(path).open(newline="", encoding="utf-8") as handle:
        for row in csv.DictReader(handle):
            raw = row["value"].strip()
            measurements.append(float(raw) if raw else None)
    return measurements


def main() -> None:
    values = load_measurements("data/measurements.csv")
    print(summarize_measurements(values, 40, 220))


if __name__ == "__main__":
    main()
'''

_DM857_TESTS = '''"""Deterministic checks for the learner-owned DM857 analysis."""

from __future__ import annotations

import importlib.util
from pathlib import Path


WORKSPACE = Path(__file__).resolve().parents[1]
SOURCE = WORKSPACE / "student" / "analysis.py"
SPEC = importlib.util.spec_from_file_location("student_analysis", SOURCE)
if SPEC is None or SPEC.loader is None:
    raise RuntimeError("Unable to load student/analysis.py")
MODULE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(MODULE)
summarize_measurements = MODULE.summarize_measurements
load_measurements = MODULE.load_measurements


def check(actual: object, expected: object, label: str) -> None:
    if actual != expected:
        raise AssertionError(f"{label}: expected {expected!r}, received {actual!r}")


check(
    summarize_measurements([72, 80, 250, None, 60], 40, 220),
    (3, 2, 70.67),
    "mixed synthetic values",
)
check(summarize_measurements([], 40, 220), (0, 0, None), "empty input")
check(
    summarize_measurements([True, False, 50], 40, 220),
    (1, 2, 50.0),
    "Boolean exclusion",
)
check(
    summarize_measurements([39.9, 40, 220, 220.1], 40, 220),
    (2, 2, 130.0),
    "inclusive boundaries",
)
try:
    summarize_measurements([70], 220, 40)
except ValueError:
    pass
else:
    raise AssertionError("lower > upper must raise ValueError")

check(
    load_measurements(WORKSPACE / "data" / "measurements.csv"),
    [72.0, 80.0, 250.0, None, 60.0],
    "CSV loading",
)
print("all workspace checks passed")
'''

_DM857_REPORT = """# Laboratory interpretation and design defence

## Computational result

Describe what the program establishes from the synthetic values.

## Biomedical limits

Explain what the result does not establish clinically. Identify the units, device,
population, sampling conditions, and temporal context that would be required before
research use.

## Design defence

Defend one error-handling decision and one return-value decision. Compare each with an
alternative and state one consequence.

## Error reflection

Document the most important error, how it was detected, the correction, and the test
that prevents recurrence.
"""


DM857_LAB_01_WORKSPACE = ScientificWorkspaceTemplate(
    workspace_id="dm857.lab01.workspace",
    lab_id="dm857.lab01.measurement-contracts",
    version="1.0.0",
    files=(
        WorkspaceFileTemplate(
            "README.md",
            _DM857_README,
            WorkspaceFileRole.README,
        ),
        WorkspaceFileTemplate(
            "data/measurements.csv",
            _DM857_DATA,
            WorkspaceFileRole.DATA,
        ),
        WorkspaceFileTemplate(
            "metadata/data_dictionary.csv",
            _DM857_DICTIONARY,
            WorkspaceFileRole.METADATA,
        ),
        WorkspaceFileTemplate(
            "student/analysis.py",
            _DM857_SOURCE,
            WorkspaceFileRole.SOURCE,
            editable=True,
        ),
        WorkspaceFileTemplate(
            "tests/test_analysis.py",
            _DM857_TESTS,
            WorkspaceFileRole.TEST,
        ),
        WorkspaceFileTemplate(
            "report.md",
            _DM857_REPORT,
            WorkspaceFileRole.REPORT,
            editable=True,
        ),
        WorkspaceFileTemplate(
            "output/.gitkeep",
            "",
            WorkspaceFileRole.OUTPUT,
        ),
    ),
    entrypoint="student/analysis.py",
    test_entrypoint="tests/test_analysis.py",
    allowed_import_roots=frozenset({"csv", "pathlib", "typing"}),
    timeout_seconds=12.0,
    output_limit=32_000,
)

WORKSPACE_TEMPLATES = {
    DM857_LAB_01_WORKSPACE.lab_id: DM857_LAB_01_WORKSPACE,
}

__all__ = ["DM857_LAB_01_WORKSPACE", "WORKSPACE_TEMPLATES"]
