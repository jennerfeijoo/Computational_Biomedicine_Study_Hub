"""Regression tests for the DM847 hidden Markov model laboratory."""

from __future__ import annotations

from computational_biomedicine_study_hub.content.labs import DM847_LAB_04
from computational_biomedicine_study_hub.content.labs.dm847_workspace_04 import (
    DM847_LAB_04_WORKSPACE,
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

_REFERENCE = """import math


def logsumexp(values):
    values = list(values)
    if not values:
        raise ValueError("logsumexp requires at least one value")
    maximum = max(values)
    if maximum == -math.inf:
        return -math.inf
    return maximum + math.log(sum(math.exp(value - maximum) for value in values))


def _distribution(mapping, labels, name):
    if set(mapping) != set(labels):
        raise ValueError(f"{name} labels do not match")
    values = []
    for label in labels:
        value = mapping[label]
        if isinstance(value, bool) or not isinstance(value, (int, float)) or value <= 0:
            raise ValueError(f"{name} probabilities must be positive")
        values.append(float(value))
    if not math.isclose(sum(values), 1.0, rel_tol=1e-9, abs_tol=1e-9):
        raise ValueError(f"{name} must sum to one")


def validate_model(model):
    if not isinstance(model, dict):
        raise TypeError("model must be a dictionary")
    states = tuple(model["states"])
    if not states or len(set(states)) != len(states):
        raise ValueError("states must be unique and non-empty")
    initial = model["initial"]
    transition = model["transition"]
    emission = model["emission"]
    _distribution(initial, states, "initial")
    alphabet = None
    for state in states:
        _distribution(transition[state], states, f"transition {state}")
        symbols = tuple(emission[state])
        if alphabet is None:
            alphabet = symbols
        elif set(symbols) != set(alphabet):
            raise ValueError("emission alphabets must match")
        _distribution(emission[state], symbols, f"emission {state}")
    return states


def _normalize(observations, model):
    if not isinstance(observations, str):
        raise TypeError("observations must be a string")
    states = validate_model(model)
    normalized = "".join(observations.split()).upper()
    alphabet = set(model["emission"][states[0]])
    if any(symbol not in alphabet for symbol in normalized):
        raise ValueError("unknown observation")
    return normalized, states


def forward_log_likelihood(observations, model):
    observations, states = _normalize(observations, model)
    if not observations:
        return 0.0
    initial = model["initial"]
    transition = model["transition"]
    emission = model["emission"]
    previous = {
        state: math.log(initial[state]) + math.log(emission[state][observations[0]])
        for state in states
    }
    for symbol in observations[1:]:
        current = {}
        for state in states:
            current[state] = math.log(emission[state][symbol]) + logsumexp(
                previous[source] + math.log(transition[source][state])
                for source in states
            )
        previous = current
    return logsumexp(previous.values())


def viterbi_decode(observations, model):
    observations, states = _normalize(observations, model)
    if not observations:
        return 0.0, ()
    initial = model["initial"]
    transition = model["transition"]
    emission = model["emission"]
    scores = {
        state: math.log(initial[state]) + math.log(emission[state][observations[0]])
        for state in states
    }
    backpointers = []
    for symbol in observations[1:]:
        current = {}
        back = {}
        for state in states:
            candidates = [
                (scores[source] + math.log(transition[source][state]), source)
                for source in states
            ]
            best_score = max(candidate[0] for candidate in candidates)
            source = next(
                candidate_state
                for candidate_score, candidate_state in candidates
                if math.isclose(candidate_score, best_score, rel_tol=0.0, abs_tol=1e-15)
            )
            current[state] = best_score + math.log(emission[state][symbol])
            back[state] = source
        scores = current
        backpointers.append(back)
    best_score = max(scores.values())
    last = next(
        state
        for state in states
        if math.isclose(scores[state], best_score, rel_tol=0.0, abs_tol=1e-15)
    )
    path = [last]
    for back in reversed(backpointers):
        path.append(back[path[-1]])
    return best_score, tuple(reversed(path))


def forward_backward(observations, model):
    observations, states = _normalize(observations, model)
    if not observations:
        return []
    initial = model["initial"]
    transition = model["transition"]
    emission = model["emission"]
    alpha = [
        {
            state: math.log(initial[state]) + math.log(emission[state][observations[0]])
            for state in states
        }
    ]
    for symbol in observations[1:]:
        alpha.append(
            {
                state: math.log(emission[state][symbol])
                + logsumexp(
                    alpha[-1][source] + math.log(transition[source][state])
                    for source in states
                )
                for state in states
            }
        )
    likelihood = logsumexp(alpha[-1].values())
    beta = [{state: 0.0 for state in states} for _ in observations]
    for position in range(len(observations) - 2, -1, -1):
        symbol = observations[position + 1]
        beta[position] = {
            state: logsumexp(
                math.log(transition[state][target])
                + math.log(emission[target][symbol])
                + beta[position + 1][target]
                for target in states
            )
            for state in states
        }
    return [
        {
            state: math.exp(alpha[position][state] + beta[position][state] - likelihood)
            for state in states
        }
        for position in range(len(observations))
    ]
"""


def test_hmm_lab_covers_the_complete_cycle_and_locales() -> None:
    assert tuple(task.stage for task in DM847_LAB_04.tasks) == tuple(LabStage)
    assert DM847_LAB_04.estimated_minutes == 185
    assert sum(task.kind is LabTaskKind.PYTHON for task in DM847_LAB_04.tasks) == 2
    assert len({task.task_id for task in DM847_LAB_04.tasks}) == len(DM847_LAB_04.tasks)
    for locale in AppLocale:
        assert DM847_LAB_04.title.text(locale)
        assert DM847_LAB_04.research_question.text(locale)
        assert "SDU" in DM847_LAB_04.disclaimer.text(locale)
        for task in DM847_LAB_04.tasks:
            assert task.title.text(locale)
            assert task.instructions.text(locale)
            assert task.mentor_notes.text(locale)


def test_reference_implementation_passes_both_python_checkpoints() -> None:
    runner = PythonSubprocessRunner()
    python_tasks = tuple(task for task in DM847_LAB_04.tasks if task.kind is LabTaskKind.PYTHON)

    for task in python_tasks:
        result = runner.run(
            PythonExecutionRequest(
                source=f"{_REFERENCE}\n{task.verification_source}",
                expected_output=task.expected_output,
                timeout_seconds=4.0,
            )
        )
        assert result.status is ExecutionStatus.PASSED, result.stderr


def test_workspace_contains_reproducible_hmm_resources_without_real_data() -> None:
    paths = {item.relative_path for item in DM847_LAB_04_WORKSPACE.files}
    assert DM847_LAB_04_WORKSPACE.lab_id == DM847_LAB_04.lab_id
    assert DM847_LAB_04_WORKSPACE.entrypoint == "student/hmm_inference.py"
    assert DM847_LAB_04_WORKSPACE.test_entrypoint == "tests/test_hmm_inference.py"
    assert {
        "README.md",
        "data/model.json",
        "data/observations.csv",
        "metadata/data_dictionary.csv",
        "student/hmm_inference.py",
        "tests/test_hmm_inference.py",
        "report.md",
        "output/.gitkeep",
    } == paths

    readme = DM847_LAB_04_WORKSPACE.file("README.md").content
    report = DM847_LAB_04_WORKSPACE.file("report.md").content
    tests = DM847_LAB_04_WORKSPACE.file("tests/test_hmm_inference.py").content
    assert "synthetic" in readme.casefold()
    assert "clinical probabilities" in readme
    assert "Path and posterior comparison" in report
    assert "all hidden-Markov-model checks passed" in tests
    assert DM847_LAB_04_WORKSPACE.file("student/hmm_inference.py").editable
    assert DM847_LAB_04_WORKSPACE.file("report.md").editable
    assert not DM847_LAB_04_WORKSPACE.file("tests/test_hmm_inference.py").editable
