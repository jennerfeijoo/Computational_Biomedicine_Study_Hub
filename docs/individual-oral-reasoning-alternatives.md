# Individual oral-reasoning preparation without in-app audio grading

## Decision

The Study Hub will not attempt to simulate an official oral examination through automatic speech recognition, pronunciation scoring, or model-generated grades. Those mechanisms are difficult to validate and can distract from the scientific reasoning that SDU actually expects.

Instead, oral preparation is decomposed into inspectable individual activities that can be completed inside the application and then verbalised independently.

## Recommended activity types

### 1. Timed answer outline

The learner receives a question and prepares, for example, a 60- or 90-second outline containing:

1. direct answer or thesis;
2. two supporting reasons;
3. one assumption or limitation;
4. one concrete consequence for analysis.

The application stores text rather than audio. The learner can later speak from the outline without reading it word for word.

### 2. Figure and table interpretation

A prompt presents a plot, model summary, confusion matrix, PCA output, dendrogram, residual pattern, or dataset dimensions. The learner must state:

- what is directly observed;
- what is inferred;
- what cannot be concluded;
- what diagnostic or additional result is needed next.

This closely targets oral scientific reasoning while remaining deterministic and reviewable.

### 3. Code-tracing defense

The learner explains:

- what the code is intended to do;
- the unit represented by each object;
- possible failure modes;
- expected output;
- one modification required under a changed assumption.

For programming courses, deterministic tests remain the authority for correctness. The written defense evaluates explanation only.

### 4. Follow-up question chain

After an initial answer, the Study Hub presents one bounded follow-up such as:

- What changes if observations are paired?
- What changes if classes are imbalanced?
- What changes if the split is by encounter instead of patient?
- What changes if residual variance increases with the fitted value?
- What changes if a suffix-tree construction exceeds memory?

The objective is transfer, not memorisation of a single response.

### 5. Error reconstruction

The learner receives a plausible but incorrect conclusion and must identify:

- the first invalid step;
- the violated assumption;
- the corrected reasoning;
- the evidence required to verify the correction.

Existing error-notebook records can later provide personalised prompts.

### 6. External self-recording packet

The application can eventually export a small packet containing:

- prompt;
- preparation time;
- maximum speaking time;
- required concepts;
- follow-up questions;
- internal self-evaluation checklist.

The learner may record audio with any local device outside the Study Hub. No recording needs to be uploaded, stored, transcribed, or graded by the application.

## Internal self-evaluation criteria

A useful non-official checklist should assess whether the answer:

- answers the exact question early;
- uses correct technical terminology;
- distinguishes data, method, result, and interpretation;
- states assumptions;
- quantifies uncertainty where relevant;
- avoids causal or clinical overclaiming;
- explains a concrete next step;
- remains within the allocated time.

The checklist is a preparation aid and must never be described as SDU's official rubric.

## Course-specific applications

### DM857

- explain program decomposition;
- defend data-structure choice;
- trace recursion or tree traversal;
- explain a failed test and correction;
- compare two implementations by complexity and readability.

### DM847

- trace dynamic programming, Viterbi, backward search, or EM;
- explain biological assumptions behind an algorithm;
- interpret sequence, network, motif, or omics output;
- discuss complexity, uncertainty, and validation.

### BMB830

- select a method from a study design;
- interpret coefficients, intervals, diagnostics, and PCA;
- identify confounding, interaction, leakage, or pseudoreplication;
- explain what a publication's result does and does not establish.

### BMB831

The public examination is an individual report rather than an oral examination. Oral-reasoning drills are still useful for defending report decisions informally, but the main application workflow should prioritise:

- report structure;
- data and method traceability;
- figure interpretation;
- critical appraisal;
- reproducibility;
- English scientific writing.

## Initial implementation

BMB831 module 1 includes a no-audio oral-explanation practice: the learner writes a 90-second outline explaining why repeated encounters from one patient are not independent patients. The reference answer uses a thesis, two reasons, and one analytical consequence.

## Recommended next implementation

Create a reusable **Individual Reasoning Studio** with:

1. stable prompt identity;
2. optional preparation and response timers;
3. structured outline fields;
4. one authored follow-up question;
5. reference concepts revealed after submission;
6. self-evaluation checklist;
7. local persistence;
8. no automatic official grade;
9. export to a printable or plain-text self-recording packet.
