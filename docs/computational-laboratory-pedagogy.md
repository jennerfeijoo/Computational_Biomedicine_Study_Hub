# Computational laboratory pedagogy

This document is the internal specification for laboratory experiences authored for the Study Hub. Laboratories are preparatory learning activities aligned with course outcomes; they do not reproduce unpublished SDU laboratory sheets.

## Laboratory identity

A computational biomedicine laboratory is a bounded investigation that connects a biological or clinical question with data, a computational representation, implementation, validation, interpretation, and reproducible evidence.

The visible learning cycle is:

1. Prepare
2. Investigate
3. Implement
4. Check
5. Interpret
6. Defend
7. Consolidate

## Required evidence

Every published laboratory must contain:

- one explicit biomedical or biological question;
- observable learning objectives;
- prerequisites and a diagnostic preparation task;
- a worked or scaffolded example;
- guided implementation with decreasing support;
- at least one conceptual checkpoint;
- a transfer task that is not a superficial parameter substitution;
- validation through tests, controls, diagnostics, or manual verification;
- a biological interpretation and a limitation statement;
- a short written or oral defence;
- a reflection on the most important error and its prevention;
- persistent learner-owned work and an exportable record.

## Mentor policy

Ollama acts as a Socratic laboratory mentor. It receives only the current task, relevant code or response, latest execution result, failed checkpoint, prior hint level, and authored evaluation notes. It must:

- ask for the learner's reasoning before giving a solution;
- provide one directed question or hint at a time;
- increase support progressively;
- distinguish code correctness from conceptual reasoning;
- require an explanation after a corrected solution;
- require transfer before treating performance as stable;
- never convert model feedback into objective mastery automatically.

## Pilot scope

The first vertical pilot is DM857 Laboratory 1: validating and summarising physiological measurements. It intentionally uses the restricted single-file Python runner. A multi-file workspace, third-party scientific libraries, datasets, and project-level execution are later increments, after the pedagogical workflow has been validated.

## Editorial gate

A laboratory is publishable only when:

- all stable identities are unique;
- every task maps to one or more objectives;
- starter code executes or fails in the intended way;
- the reference implementation passes every authored checkpoint;
- incomplete or common erroneous implementations fail relevant checkpoints;
- translations exist in Spanish, English, and Danish;
- time estimates are coherent;
- the activity clearly states that it is internal preparation;
- solutions are not exposed in the learner interface;
- the final record can be restored and exported.
