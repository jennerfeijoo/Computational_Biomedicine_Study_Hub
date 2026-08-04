"""Persistent scientific workspace for DM847 laboratory 4."""

from __future__ import annotations

from ...learning.scientific_workspace import (
    ScientificWorkspaceTemplate,
    WorkspaceFileRole,
    WorkspaceFileTemplate,
)

_README = """# DM847 Laboratory 4 workspace

This internal preparation workspace develops hidden Markov model inference from first
principles. It is not an official SDU laboratory sheet.

## Research question

How do total observation probability, the globally most probable hidden path, and
position-wise posterior state probabilities answer different questions about the same
synthetic sequence?

## Model

The synthetic model has two latent states:

- `H`: GC-rich emission profile;
- `L`: AT-rich emission profile.

These labels are teaching abstractions. They are not genomic annotations, disease
states, patient labels, or calibrated clinical probabilities.

## Required distinctions

- observation likelihood `P(x)` versus joint path probability `P(path, x)`;
- Viterbi path versus posterior probability at one position;
- summing alternative paths versus retaining only a maximum;
- numerical implementation in log space versus the underlying probability model;
- algorithmic output versus biological or clinical validity.

## Files

- `data/model.json`: authored synthetic HMM parameters.
- `data/observations.csv`: authored synthetic observation sequences.
- `metadata/data_dictionary.csv`: provenance and interpretation limits.
- `student/hmm_inference.py`: learner-owned implementation.
- `tests/test_hmm_inference.py`: authored deterministic checks.
- `report.md`: learner-owned interpretation and model defence.
- `output/`: generated execution records.

Passing tests establishes behaviour for the declared synthetic model and contracts. It
does not establish that the latent states correspond to real biological regions, that
the parameters were learned appropriately, or that outputs are clinically valid.
"""

_MODEL = """{
  "states": ["H", "L"],
  "initial": {"H": 0.5, "L": 0.5},
  "transition": {
    "H": {"H": 0.8, "L": 0.2},
    "L": {"H": 0.2, "L": 0.8}
  },
  "emission": {
    "H": {"A": 0.1, "C": 0.4, "G": 0.4, "T": 0.1},
    "L": {"A": 0.4, "C": 0.1, "G": 0.1, "T": 0.4}
  }
}
"""

_OBSERVATIONS = """observation_id,sequence,teaching_role
obs_gc,GCGC,GC-rich evidence
obs_at,ATAT,AT-rich evidence
obs_switch,GGGCAATT,one synthetic state transition
obs_ambiguous,ACGT,position-wise uncertainty
obs_long,GGGCCCAAATTT,longer transition and underflow preparation
"""

_DICTIONARY = """field,meaning,provenance,interpretation_limit
state_H,Synthetic GC-rich latent state,authored for DM847 laboratory 4,not a genomic annotation or clinical class
state_L,Synthetic AT-rich latent state,authored for DM847 laboratory 4,not a genomic annotation or clinical class
initial,Probability of the first latent state,authored normalized distribution,not an estimated population prevalence
transition,Conditional probability of the next state,authored first-order Markov model,does not encode realistic segment durations
emission,Conditional probability of a nucleotide given state,authored synthetic profile,does not model sequencing quality or context
sequence,Synthetic observed DNA symbols,authored deterministic cases,not patient or experimental data
posterior,Probability of one state at one position given the full sequence,derived from the synthetic model,not calibrated biological confidence
viterbi_path,Globally highest joint-probability path,derived from the synthetic model,does not preserve full path uncertainty
"""

_SOURCE = '''"""Learner-owned hidden Markov model inference implementation."""

from __future__ import annotations

import csv
import json
import math
from pathlib import Path


_TOLERANCE = 1e-9


def logsumexp(values: list[float]) -> float:
    """Return log(sum(exp(values))) without avoidable underflow."""

    raise NotImplementedError


def validate_model(model: dict[str, object]) -> tuple[str, ...]:
    """Validate the HMM and return the declared state order."""

    raise NotImplementedError


def normalize_observations(observations: str, model: dict[str, object]) -> str:
    """Return uppercase observations without whitespace and reject unknown symbols."""

    raise NotImplementedError


def forward_log_likelihood(observations: str, model: dict[str, object]) -> float:
    """Return log P(observations | model) using the Forward algorithm."""

    raise NotImplementedError


def viterbi_decode(
    observations: str,
    model: dict[str, object],
) -> tuple[float, tuple[str, ...]]:
    """Return best-path log joint probability and the complete state path."""

    raise NotImplementedError


def forward_backward(
    observations: str,
    model: dict[str, object],
) -> list[dict[str, float]]:
    """Return posterior state probabilities at each observation position."""

    raise NotImplementedError


def path_log_probability(
    observations: str,
    path: tuple[str, ...],
    model: dict[str, object],
) -> float:
    """Recompute log P(path, observations) for one complete state path."""

    raise NotImplementedError


def load_model(path: str | Path) -> dict[str, object]:
    """Load an authored JSON model and validate it."""

    with Path(path).open(encoding="utf-8") as handle:
        model = json.load(handle)
    validate_model(model)
    return model


def load_observations(path: str | Path) -> list[tuple[str, str]]:
    """Load observation identifiers and sequences from the authored CSV."""

    with Path(path).open(newline="", encoding="utf-8") as handle:
        return [(row["observation_id"], row["sequence"]) for row in csv.DictReader(handle)]


def main() -> None:
    model = load_model("data/model.json")
    for observation_id, sequence in load_observations("data/observations.csv"):
        log_likelihood = forward_log_likelihood(sequence, model)
        path_score, path = viterbi_decode(sequence, model)
        posterior = forward_backward(sequence, model)
        print(
            observation_id,
            round(log_likelihood, 6),
            "".join(path),
            round(path_score, 6),
            [round(row["H"], 3) for row in posterior],
        )


if __name__ == "__main__":
    main()
'''

_TESTS = '''"""Deterministic checks for learner-owned HMM inference."""

from __future__ import annotations

import importlib.util
import math
from pathlib import Path


WORKSPACE = Path(__file__).resolve().parents[1]
SOURCE = WORKSPACE / "student" / "hmm_inference.py"
SPEC = importlib.util.spec_from_file_location("student_hmm_inference", SOURCE)
if SPEC is None or SPEC.loader is None:
    raise RuntimeError("Unable to load student/hmm_inference.py")
MODULE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(MODULE)


def check(actual: object, expected: object, label: str) -> None:
    if actual != expected:
        raise AssertionError(f"{label}: expected {expected!r}, received {actual!r}")


def close(actual: float, expected: float, label: str, tolerance: float = 1e-6) -> None:
    if not math.isclose(actual, expected, rel_tol=tolerance, abs_tol=tolerance):
        raise AssertionError(f"{label}: expected {expected!r}, received {actual!r}")


model = MODULE.load_model(WORKSPACE / "data" / "model.json")
check(MODULE.validate_model(model), ("H", "L"), "state order")
check(MODULE.normalize_observations(" acg\\nT ", model), "ACGT", "normalization")

for invalid_sequence in ("ACX", "$", "123"):
    try:
        MODULE.normalize_observations(invalid_sequence, model)
    except (TypeError, ValueError):
        pass
    else:
        raise AssertionError(f"invalid observations must be rejected: {invalid_sequence!r}")

invalid_model = {
    "states": ["H", "L"],
    "initial": {"H": 0.7, "L": 0.7},
    "transition": model["transition"],
    "emission": model["emission"],
}
try:
    MODULE.validate_model(invalid_model)
except (TypeError, ValueError):
    pass
else:
    raise AssertionError("an unnormalized initial distribution must be rejected")

close(MODULE.forward_log_likelihood("", model), 0.0, "empty Forward")
close(MODULE.forward_log_likelihood("ACGT", model), -5.977166526873296, "ACGT Forward")
close(
    MODULE.forward_log_likelihood("GGGCAATT", model),
    -10.23519025624718,
    "switch Forward",
)

empty_score, empty_path = MODULE.viterbi_decode("", model)
close(empty_score, 0.0, "empty Viterbi score")
check(empty_path, (), "empty Viterbi path")

score, path = MODULE.viterbi_decode("GGGCAATT", model)
close(score, -10.971771996456278, "switch Viterbi score")
check(path, tuple("HHHHLLLL"), "switch Viterbi path")
close(
    MODULE.path_log_probability("GGGCAATT", path, model),
    score,
    "recomputed Viterbi path",
)
check(MODULE.viterbi_decode("GCGC", model)[1], tuple("HHHH"), "GC-rich path")
check(MODULE.viterbi_decode("ATAT", model)[1], tuple("LLLL"), "AT-rich path")

posteriors = MODULE.forward_backward("ACGT", model)
check(len(posteriors), 4, "posterior length")
expected_h = (0.38235294117647073, 0.7316176470588236, 0.7316176470588236, 0.38235294117647073)
for index, (row, expected) in enumerate(zip(posteriors, expected_h, strict=True)):
    check(tuple(row), ("H", "L"), f"posterior state order at {index}")
    close(sum(row.values()), 1.0, f"posterior normalization at {index}")
    close(row["H"], expected, f"H posterior at {index}")

check(MODULE.forward_backward("", model), [], "empty posterior")
observations = MODULE.load_observations(WORKSPACE / "data" / "observations.csv")
check(observations[0], ("obs_gc", "GCGC"), "observation loading")
check(observations[-1][0], "obs_long", "observation order")

print("all hidden-Markov-model checks passed")
'''

_REPORT = """# Hidden Markov model interpretation and defence

## Model contract

Define the observed alphabet, latent states, initial distribution, transition and
emission matrices, empty-sequence policy, state order, and normalization tolerance.
State what H and L do and do not represent.

## Manual inference

For a short sequence, show the first two columns of Forward and Viterbi. Label every
factor and state whether alternatives are summed or maximized. Explain the backpointer
needed for Viterbi traceback.

## Numerical stability

Explain why direct products underflow for long sequences. Derive the role of log-sum-exp
and identify which HMM operations become addition, maximum, or log-sum-exp in log space.

## Path and posterior comparison

For `ACGT` and `GGGCAATT`, report:

- Forward log likelihood;
- Viterbi path and log joint probability;
- posterior state probabilities at each position;
- positions with material uncertainty.

Distinguish `P(x)`, `P(path, x)`, `P(path | x)`, and `P(state_t | x)`. Explain why a
sequence of marginally most probable states need not equal the globally most probable
path.

## Complexity and architecture defence

Use `T` observations and `K` states. Separate time and memory for Forward, Viterbi,
traceback, Backward, and posterior calculation. Explain when rolling arrays are possible
and when complete tables or backpointers are required.

## Scientific limitations

Discuss first-order Markov dependence, conditionally independent emissions, known fixed
parameters, state-label interpretation, missing biological covariates, sequencing error,
external validation, parameter learning, and calibration. Passing tests does not validate
real genomic segmentation or clinical use.

## Error reflection and extension

Document the most important error, its symptom, root cause, correction, and regression
test. Select one extension—scaling, Baum–Welch, duration modelling, additional states,
or validation against labels—and justify its scientific priority.
"""


DM847_LAB_04_WORKSPACE = ScientificWorkspaceTemplate(
    workspace_id="dm847.lab04.workspace",
    lab_id="dm847.lab04.hidden-markov-models",
    version="1.0.0",
    files=(
        WorkspaceFileTemplate("README.md", _README, WorkspaceFileRole.README),
        WorkspaceFileTemplate(
            "data/model.json",
            _MODEL,
            WorkspaceFileRole.DATA,
        ),
        WorkspaceFileTemplate(
            "data/observations.csv",
            _OBSERVATIONS,
            WorkspaceFileRole.DATA,
        ),
        WorkspaceFileTemplate(
            "metadata/data_dictionary.csv",
            _DICTIONARY,
            WorkspaceFileRole.METADATA,
        ),
        WorkspaceFileTemplate(
            "student/hmm_inference.py",
            _SOURCE,
            WorkspaceFileRole.SOURCE,
            editable=True,
        ),
        WorkspaceFileTemplate(
            "tests/test_hmm_inference.py",
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
    entrypoint="student/hmm_inference.py",
    test_entrypoint="tests/test_hmm_inference.py",
    allowed_import_roots=frozenset({"csv", "json", "math", "pathlib"}),
    timeout_seconds=15.0,
    output_limit=32_000,
)


__all__ = ["DM847_LAB_04_WORKSPACE"]
