# Architecture and learning-path roadmap

## Decision

The application has reached the point where adding each new assessment directly to the main window or the assessment tab container would increase coupling and duplicate persistence logic. The next development phase therefore introduces shared infrastructure while preserving the rule that each course keeps independent authored content and course-specific workflows.

## Problems addressed

1. The main window recognises only DM847 and DM857 as modular course pages even though BMB830 and BMB831 expose the same navigation contract. This prevents generic location restoration and review routing for the biostatistics courses.
2. The assessment workspace hard-codes course pages and therefore requires central edits for every new assessment workflow.
3. Course-specific JSON sidecar stores duplicate atomic-write, in-memory-test, malformed-document, and cleanup logic.
4. Objective mastery, review scheduling, written work, oral work, projects, and reports are not yet orchestrated by one explicit learning-path model.
5. Local AI and speech services need to remain optional adapters around a deterministic academic core.

## Target architecture

### Independent course content

Each course retains its own Python package, modules, source audit, assessment identities, trilingual content, and course-specific workflows. Shared infrastructure must not flatten course semantics or force every course into the same examination format.

### Structural course-page protocol

The shell depends on a small runtime-checkable protocol rather than concrete course-page classes. Any page that exposes module selection and a reader can participate in:

- language-change location restoration;
- objective-review routing;
- contextual tutor grounding;
- future learning-path navigation.

### Assessment registry

Course assessment pages are registered through stable metadata and factories. The workspace constructs tabs from the registry and stores pages by course code. Adding BMB830 oral practice, DM847 oral defence, or DM857 presentation rehearsal becomes a registration change rather than another hard-coded branch.

### Shared atomic JSON persistence

A generic local sidecar store owns:

- atomic temporary-file replacement;
- isolated in-memory documents for tests;
- defensive deletion of malformed documents;
- stable suffix namespaces;
- typed serialization and deserialization callbacks.

Course stores remain thin typed wrappers so their public APIs stay explicit.

### Evidence-driven learning path

The learning path is not a fixed chapter checklist. It is a deterministic sequence of evidence states:

1. **Orient** — understand the module question, outcomes, vocabulary, and prerequisites.
2. **Learn** — study concepts and worked examples.
3. **Practice** — complete executable or guided activities without relying on recognition alone.
4. **Retrieve** — answer objective questions from memory with confidence recorded before feedback.
5. **Transfer** — solve a novel open response, coding case, figure interpretation, or analysis task.
6. **Assess** — rehearse the course's real examination mode: oral, project, report, or mixed portfolio.
7. **Consolidate** — revisit due objectives, unresolved errors, and weak rubric dimensions.

The path engine should recommend the next evidence-producing action from local progress. It must not mark mastery from model feedback alone.

## Delivery order

1. Add the generic course-page protocol and repair shell routing for all four courses.
2. Replace hard-coded assessment tabs with a registration catalog.
3. Introduce the shared atomic JSON sidecar store and migrate existing wrappers.
4. Add the deterministic learning-path domain model and recommendation engine.
5. Expose a trilingual learning-path page with direct navigation to the recommended activity.
6. Continue assessment additions: BMB830 oral, DM857 presentation and defence, DM847 oral and integrated project.
7. Add optional local speech transcription and local-model critique behind asynchronous service adapters.

## Quality boundaries

- No unpublished SDU material is reconstructed.
- Internal readiness indicators are not official grades.
- Every generated recommendation must resolve to authored content or a registered assessment workflow.
- Course content remains usable without Ollama, speech recognition, internet access, or a GPU.
- Compute-intensive local services run outside the UI thread and may use the available CPU, RAM, and GPU without weakening deterministic validation.
- Every architectural increment requires tests for identity stability, localization, persistence, and regression boundaries.
