# Artifact-based technical reasoning

## Purpose

The application does not attempt to simulate an oral examination. Public course descriptions do not establish a fixed conversational script, and a real examination may combine conceptual questions, code reading, algorithm tracing, debugging, output interpretation, and short technical explanations.

The technical-station system therefore trains the underlying capabilities directly through concrete artifacts.

## Station forms

The shared domain supports:

- code reading;
- execution tracing;
- debugging;
- output interpretation;
- method selection;
- complexity analysis;
- scientific interpretation;
- project reasoning.

The first authored set contains sixteen DM847 stations: four for short-read mapping, four for pairwise alignment, four for suffix-array/FM-index work, and four for hidden Markov models.

## Evidence model

A station contains:

- a stable station, course, and laboratory identity;
- a concrete code, trace, output, or scenario artifact;
- a bounded technical prompt;
- explicit self-review criteria;
- an authored source basis;
- a minimum substantive-response requirement.

Learner evidence contains:

- the technical explanation;
- explicitly checked review criteria;
- the progressive support level requested;
- timestamps;
- whether the response was recorded as attempted and self-reviewed.

Changing the explanation invalidates previous self-review evidence. A station can be recorded as reviewed only after the response reaches the authored minimum and every criterion has been checked.

## Interpretation boundary

A reviewed station means only:

1. the learner produced a substantive response;
2. the learner explicitly compared it with the authored review dimensions.

It does not mean:

- an official grade;
- an examination prediction;
- an oral-examination simulation;
- deterministic mastery;
- institutional assessment completion.

Technical-station progress is stored separately from laboratory checkpoints and the deterministic objective-mastery model.

## Socratic mentor boundary

Ollama receives the concrete artifact, task, learner explanation, support level, and private review dimensions. The prompt requires the mentor to:

- diagnose reasoning from the artifact;
- ask one central question before explaining;
- avoid examiner role-play;
- avoid official grades or examination predictions;
- avoid revealing private review criteria verbatim;
- distinguish implementation behaviour, algorithmic reasoning, and biological interpretation.

Model feedback remains formative and cannot mark a station as reviewed or mutate objective mastery.

## Current DM847 coverage

### Laboratory 1 — short-read mapping

- read an approximate-search contract;
- trace overlapping matches;
- debug an off-by-one boundary;
- interpret multimapping uncertainty.

### Laboratory 2 — pairwise alignment

- explain the dynamic-programming recurrence;
- calculate one matrix cell;
- debug Smith–Waterman traceback termination;
- choose global or local alignment and defend interpretation limits.

### Laboratory 3 — sequence indexes

- explain `Occ(c, k)` semantics;
- trace backward search;
- debug count-versus-locate confusion;
- defend preprocessing, query-time, memory, and locate trade-offs.

### Laboratory 4 — hidden Markov models

- explain log-sum-exp;
- separate Forward and Viterbi calculations;
- debug Backward initialization;
- distinguish a global Viterbi path from marginal posterior probabilities.

## Expansion path

The same architecture can later support:

- DM857 project-code understanding and contribution evidence;
- BMB830 R code, model-output, diagnostic-plot, and method-selection stations;
- BMB831 analysis-to-report traceability stations;
- later DM847 motif, network, and OMICS laboratories.

New stations should remain artifact-centred, source-grounded, and independent of assumptions about unpublished examination mechanics.
