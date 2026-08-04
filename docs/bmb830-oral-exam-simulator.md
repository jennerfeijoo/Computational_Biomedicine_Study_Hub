# BMB830 oral-exam simulator

## Purpose

Add an individual, timed, source-grounded oral-examination workflow for **BMB830 — Biostatistics in R I**.

The simulator is a preparation aid. It must not claim to reproduce unpublished SDU questions, certify readiness, or assign an official Danish grade. Its purpose is to train the reasoning chain expected in an individual oral examination:

1. identify the scientific question and analytical unit;
2. define the estimand;
3. inspect design, data quality, and dependence;
4. choose and justify a model;
5. state assumptions;
6. interpret output and uncertainty;
7. diagnose threats to validity;
8. propose sensitivity analyses;
9. communicate conclusions and limitations in English.

## Why this is the first priority

The authored BMB830 modules cover the public academic scope, but the existing audit still identifies the oral examination as partial. The current application contains oral-explanation activities but no complete timed session spanning the syllabus, no adaptive follow-up questioning, no figure or R-output station, and no persistent examination transcript.

## Design principles

- **Source-grounded:** questions, reference points, and feedback are generated only from validated BMB830 module content and its authorised tutor material.
- **Individual:** no group-project or presentation workflow is introduced for BMB830.
- **Exam-like but non-official:** the interface states clearly that timing, rubrics, prompts, and feedback are internal preparation tools.
- **Evidence-bearing:** every session stores the selected modules, prompts, responses, follow-ups, self-assessment, feedback, and timestamps.
- **No false precision:** the system reports criterion-level evidence and readiness signals, not an official grade prediction.
- **Hardware-capable:** the architecture may use local speech recognition and a local language model because the target machine has sufficient CPU, RAM, and GPU capacity. These services remain optional so the academic workflow still works offline without them.
- **Deterministic core:** session construction, syllabus coverage, timing, persistence, and rubric calculations remain deterministic. Model-generated feedback cannot mutate mastery records automatically.

## Examination modes

### 1. Focused drill

- one selected module;
- one primary question;
- two follow-up questions;
- configurable preparation and answer time;
- immediate criterion-level review.

Use case: deliberate practice on a weak topic.

### 2. Mixed oral session

- randomised coverage across the complete BMB830 sequence;
- three stations;
- approximately 20–30 minutes in total;
- no immediate feedback between stations;
- final structured review.

Suggested station types:

1. **Concept and design** — explain an estimand, study design, model choice, or inferential principle;
2. **R output or figure interpretation** — interpret a table, diagnostic plot, confidence interval, PCA result, or validation result;
3. **Methodological challenge** — respond to a changed assumption, confounder, dependence structure, multiplicity problem, or sensitivity-analysis request.

### 3. Full mock examination

- timed preparation phase;
- one main case sampled from multiple modules;
- adaptive questioning across assumptions, diagnostics, uncertainty, and biological interpretation;
- no hints during the attempt;
- complete transcript and post-session review;
- session coverage balanced over repeated attempts.

## Question taxonomy

Every prompt must declare a stable `question_kind`:

- `study_design`
- `estimand`
- `data_quality`
- `model_selection`
- `assumption_check`
- `r_output_interpretation`
- `figure_interpretation`
- `effect_and_uncertainty`
- `diagnostics`
- `causal_boundary`
- `multiplicity`
- `validation`
- `multivariate_interpretation`
- `publication_appraisal`
- `sensitivity_analysis`

Each prompt also records:

- source module IDs;
- linked learning objectives;
- expected reasoning points;
- common failure modes;
- permitted follow-up transformations;
- difficulty;
- whether a figure, table, or code/output artifact is required.

## Rubric

The internal rubric uses six criteria, each scored from 0 to 4:

1. **Problem framing** — identifies the question, analytical unit, design, and estimand.
2. **Methodological justification** — chooses and defends an appropriate model or procedure.
3. **Assumptions and diagnostics** — states assumptions and proposes checks or alternatives.
4. **Statistical interpretation** — interprets estimates, effect sizes, uncertainty, and multiplicity correctly.
5. **Biological and causal boundaries** — distinguishes association, prediction, explanation, and causal claims.
6. **Communication under questioning** — gives a structured answer and adapts coherently to follow-ups.

The simulator may calculate an internal readiness profile, but the UI must display:

> Internal preparation rubric — not an official SDU grade or grading scale.

## Session-generation rules

A mixed or full session must:

- sample across distinct modules where possible;
- avoid repeating the same objective until the configured review interval has elapsed;
- include at least one interpretation task;
- include at least one follow-up that changes an assumption or data condition;
- include at least one limitation or validity question;
- preserve a deterministic seed for reproducibility;
- record why each question was selected;
- prefer weak or overdue objectives when learner evidence exists;
- retain balanced syllabus coverage when no learner history exists.

## Follow-up engine

Follow-ups are not generic requests to “explain more.” They must apply a defined transformation to the case, for example:

- change independent observations to paired or longitudinal measurements;
- introduce heteroscedasticity;
- add a confounder;
- change a continuous outcome to binary;
- increase the number of tested features;
- reveal a batch effect;
- remove an influential observation;
- show disagreement between training and validation performance;
- change covariance-PCA to correlation-PCA;
- introduce `p > n`;
- replace a statistically significant result with a clinically negligible effect;
- reveal that the plotted error bars are SD rather than confidence intervals.

The learner must explain what changes in the model, interpretation, or conclusion.

## Optional local speech workflow

The target machine can support a local speech pipeline. Audio remains optional and does not block the first implementation.

Recommended architecture:

1. record microphone input locally;
2. transcribe with a local Whisper-compatible engine;
3. retain both audio metadata and editable transcript;
4. require learner confirmation before feedback generation;
5. evaluate scientific reasoning from the confirmed transcript;
6. never treat transcription confidence as subject-matter mastery.

The speech layer must be isolated behind a protocol so the application can support:

- typed responses only;
- external self-recording;
- local transcription;
- future pronunciation or fluency tools without mixing those scores with statistical reasoning.

No audio is uploaded by the Study Hub.

## Optional local model workflow

Ollama may support:

- grounded follow-up selection;
- omission detection;
- contradiction detection;
- comparison against the authored reasoning points;
- restructuring an answer into a concise oral response;
- producing a post-session improvement plan.

The model must receive:

- only the selected BMB830 tutor documents;
- the exact prompt and deterministic rubric;
- the learner-confirmed transcript;
- explicit instructions not to invent SDU requirements or assign an official grade.

The model response must be parsed into a bounded schema. Invalid or unsupported output is rejected rather than silently accepted.

## Persistence model

### `OralExamSession`

- `session_id`
- `course_code`
- `mode`
- `locale`
- `seed`
- `created_at`
- `started_at`
- `completed_at`
- `status`
- `planned_duration_seconds`
- `actual_duration_seconds`
- `source_content_versions`

### `OralExamStation`

- `station_id`
- `session_id`
- `order_index`
- `question_id`
- `question_kind`
- `module_ids`
- `objective_ids`
- `prompt_text`
- `artifact_reference`
- `preparation_seconds`
- `answer_seconds`
- `selection_reason`

### `OralExamTurn`

- `turn_id`
- `station_id`
- `turn_index`
- `speaker`
- `prompt_text`
- `response_text`
- `response_started_at`
- `response_completed_at`
- `transcription_source`
- `learner_confirmed`

### `OralExamReview`

- criterion scores and evidence notes;
- missing reasoning points;
- unsupported claims;
- strong reasoning points;
- recommended remediation modules;
- learner self-assessment;
- model and source identifiers when model assistance was used.

## User interface

Add a **BMB830 Oral** tab to the existing Assessments page.

The page contains:

1. mode selection;
2. module or syllabus-scope selection;
3. timing controls;
4. deterministic session seed;
5. exam integrity notice;
6. active prompt and timer;
7. typed response editor;
8. optional audio controls when a speech backend is available;
9. follow-up panel;
10. final transcript;
11. criterion-level review;
12. session history and coverage map.

The active attempt should minimise distractions. Tutor chat must not reveal reference answers during a no-hints mock session.

## Implementation increments

### Increment 1 — deterministic typed simulator

- domain models;
- stable authored question bank;
- deterministic mixed-session generator;
- timers;
- typed responses;
- structured self-assessment;
- persistent session history;
- integration into Assessments;
- tests for coverage, timing state, persistence, localisation, and reproducibility.

### Increment 2 — grounded review

- deterministic reference-point comparison;
- optional Ollama review using bounded JSON output;
- adaptive follow-up selection;
- criterion-level evidence notes;
- remediation links back to BMB830 modules.

### Increment 3 — interpretation artifacts

- authored R-output fixtures;
- statistical tables;
- diagnostic plots;
- PCA and clustering artifacts;
- publication-method extracts within copyright limits;
- artifact-specific follow-up questions.

### Increment 4 — local speech

- microphone capture;
- optional local transcription backend;
- transcript confirmation;
- audio-session metadata;
- latency and failure handling;
- no automatic fluency grading.

### Increment 5 — full readiness analytics

- syllabus coverage matrix;
- repeated-error analysis;
- response-time trends;
- criterion stability across sessions;
- weak-objective prioritisation;
- exportable revision plan.

## Acceptance criteria for Increment 1

- A learner can create, complete, pause, resume, and review a BMB830 oral session.
- A mixed session samples at least three distinct reasoning categories and at least two modules.
- The same seed and content versions reproduce the same session.
- Every question resolves to existing BMB830 modules and objectives.
- No official grade, official rubric, or examination-equivalence claim appears.
- Session data survives application restart and language changes.
- Spanish, English, and Danish interfaces are complete with no fallback.
- The full test suite passes on Python 3.11 and 3.12.

## Initial delivery order

1. implement Increment 1;
2. add BMB830-specific grounded review;
3. add interpretation artifacts;
4. add local speech support;
5. then move to DM857 presentation and project defence;
6. then implement the DM847 oral simulator and integrated project.
