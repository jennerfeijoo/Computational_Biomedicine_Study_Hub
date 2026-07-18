# Academic content authoring standard

Each module is authored as a complete learning unit rather than a long note dump. The
same domain model supports the application UI, deterministic assessment and grounded
Ollama assistance.

## Required module components

Every module must contain:

1. observable learning objectives;
2. connected concept explanations;
3. worked examples that show reasoning, code and expected output;
4. formative practice with hints and authored solutions;
5. assessment items with deterministic answers and feedback;
6. a tutor-support packet with canonical explanations, misconceptions, Socratic prompts,
   grading criteria and response constraints;
7. source-basis notes identifying the material used to author the module.

The user-facing module header does not include level, prerequisites, estimated time or
subjective difficulty labels.

## Learning sequence

Content should move through the following sequence where appropriate:

- concept formation;
- worked example;
- guided practice;
- active retrieval;
- feedback;
- transfer to a new context;
- spaced review.

A module should use multiple activity formats rather than repeating only multiple-choice
questions. Suitable formats include code tracing, debugging, fill-in-the-blank, matching,
ordering, short explanation, oral explanation and data interpretation.

## Assessment policy

Objective questions are graded deterministically from authored answers. Ollama must not
replace those answers. Local-model evaluation is reserved for responses that require
explanation, reasoning or code review. Even then, the model receives an authored rubric
and reference material.

Solutions must explain why an answer is correct and, when useful, why common alternatives
are incorrect. A program that executes without an exception is not automatically treated as
correct.

## Ollama support material

The authored module is converted into small retrieval documents with stable identifiers and
tags. Retrieval documents include:

- module overview and canonical explanation;
- one document per concept;
- one document per worked example;
- one document per practice solution;
- one document per assessment explanation;
- tutor guidance covering misconceptions, questioning strategy and grading criteria.

The model should receive only documents relevant to the current question. Full-module
context should not be inserted by default. Solutions are kept separate from the learner's
initial prompt so the tutor can provide hints before revealing a complete answer.

## Quality controls

Each module must pass automated checks for:

- non-empty required components;
- unique stable identifiers;
- valid assessment answers;
- deterministic retrieval-document generation;
- substantive tutor-support material;
- a deliberate mixture of learning activities.

Academic content is authored one module at a time and reviewed before the next module is
started.
