# Computational Biomedicine Study Hub

Offline-first desktop study companion for the MSc in Computational Biomedicine at the University of Southern Denmark.

The application combines concise theory, worked examples, executable code, guided practice, objective assessment, persistent revision, written-response preparation, and retrieval-ready tutor material. Academic content is authored in Spanish, English, and Danish while preserving language-independent assessment identities.

## Current implementation

### Completed course content

- **DM857 — Introduction to Programming**
  - 14 complete modules
  - Python foundations, control flow, functions, data structures, recursion, trees, abstract data types, object-oriented programming, scientific libraries, testing, debugging, and software quality
  - persistent five-milestone project-and-report preparation workflow
- **DM847 — Introduction to Bioinformatics**
  - 10 complete modules
  - molecular information, ontologies and databases, sequence scoring, pairwise alignment, hidden Markov models, suffix arrays and BWT, bacterial genetics, motif discovery, biological networks, and omics learning
  - persistent open-response and essay studio with one authored task per module

### BMB830 implementation in progress

- **BMB830 — Biostatistics in R I**
  - 12 complete modules
  - R objects and reproducible workflows
  - data quality, descriptive statistics, and scientific visualization
  - probability, sampling, and reference distributions
  - estimation, standard errors, and confidence intervals
  - hypothesis tests, type I and II errors, power, and effect sizes
  - independent, paired, and multi-group comparisons with assumptions and multiplicity control
  - correlation, association versus causation, and simple linear regression
  - confidence intervals for conditional means and individual prediction intervals
  - multiple regression, design matrices, adjusted coefficients, factors, reference levels, confounding, and collinearity
  - interactions, effect modification, group-specific slopes, centring, polynomial terms, and nested-model comparison
  - residual diagnostics, heteroscedasticity, leverage, Cook's distance, sensitivity analysis, information leakage, and out-of-sample validation
  - multivariate matrices, centring, scaling, distances, PCA, scores, loadings, explained variance, hierarchical clustering, and stability analysis
  - individual synthetic proteomics case with provenance, p-greater-than-n quality control, missingness, filtering, imputation, batch assessment, leakage-safe feature screening, and reproducible reporting
  - 192 stable objective-bank questions
  - optional editable R laboratories executed through a locally installed `Rscript`
  - conservative audit against the active public SDU specification and a separate master-level readiness matrix

The public multivariate requirement is covered, and an individual bounded high-dimensional proteomics case now exercises the complete exploratory workflow. A substantially larger externally sourced biological data set, detailed figure-building practice, structured publication appraisal, and complete individual oral-reasoning preparation remain partial until suitable source materials are selected or become available.

BMB830 does not include a group project, role allocation, collaborative submission, or group presentation. The public course description recommends discussion during exercise sessions but publishes an individual oral examination rather than a group-project assessment. All Study Hub activities for this course are individually completable.

### BMB831 implementation in progress

- **BMB831 — Biostatistics in R II**
  - 1 complete module
  - Synthea provenance and scientific-use boundary
  - relational grain, primary and foreign keys, and cardinality validation
  - patient-level aggregation of repeated clinical events
  - temporal leakage and patient-level validation splits
  - scalable and auditable R workflow design
  - 16 stable objective-bank questions
  - two editable base-R laboratories using deterministic Synthea-structured fixtures
  - conservative audit against all seven public learning outcomes, six public content topics, tutorial prerequisite, and individual-report examination

Synthea is used as a temporary synthetic clinical-data source for relational, longitudinal, large-table, modelling, visualisation, and critical-reasoning practice. It is never described as real-patient evidence. It also does not replace transcriptomics, proteomics, protein-characterisation, or other omics data required by BMB831; those remain explicit gaps for subsequent modules.

### Registered first-semester courses

- **DM857** — Introduction to Programming
- **DM847** — Introduction to Bioinformatics
- **BMB830** — Biostatistics in R I
- **BMB831** — Biostatistics in R II

## Main capabilities

- Immediate language switching between **ES**, **EN**, and **DK**
- Stable question and answer identities across translations
- Lazy construction of course modules and reader sections
- Guided practice, executable Python challenges, executable R examples, and objective assessments
- Persistent objective evidence, confidence, spaced review, and error notebook
- Resumable adaptive-review sessions across courses
- Persistent DM857 project-and-report preparation with repository evidence
- Persistent DM847 open responses and essay drafts
- Optional local Ollama support for:
  - scientific-content review of open answers
  - writing revision that preserves the learner's valid ideas
  - thesis, structure, and draft development for essays
- Automated validation of content, localization, executable examples, UI behavior, persistence, and assessment integrity

## Individual oral-reasoning preparation

The application does not depend on speech recognition or attempt to grade pronunciation, fluency, or audio automatically. Oral preparation is instead decomposed into individually useful, inspectable activities:

- timed answer outlines;
- thesis–evidence–limitation structures;
- code, table, and figure interpretation;
- follow-up questions that change assumptions or data conditions;
- concise explanations of model choice, diagnostics, uncertainty, and validity threats;
- optional self-recording outside the application using prompts exported from the Study Hub.

The first BMB831 module includes a no-audio oral-explanation exercise: the learner writes a 90-second reasoning outline, receives a reference structure, and can later verbalize the same argument independently. This approach trains scientific reasoning without pretending that typed text is an official oral examination.

## Local tutor model

The preferred and default Ollama model is:

```text
qwen3.5:9b-q8_0
```

Install Ollama separately and pull the model:

```bash
ollama pull qwen3.5:9b-q8_0
```

The application connects to the local Ollama API at:

```text
http://localhost:11434/api
```

Connection settings are validated in the application. Preferences are stored only after the user selects **Save**.

DM847 written feedback is generated from the authorised tutor documents of the selected module. Source identifiers are preserved with the response. Ollama may identify omissions or suggest revisions, but it does not assign an official grade, declare mastery, or modify deterministic learning progress. Learner drafts and the latest feedback remain in local sidecar storage.

## Local R laboratories

BMB830 and BMB831 worked examples can be edited and executed when `Rscript` is available on the local `PATH`. The runner uses `Rscript --vanilla`, a temporary working directory, a hard timeout, bounded output, and a conservative policy that rejects file, network, external-process, package-installation, dynamic-evaluation, and native-code capabilities.

R is optional. Without `Rscript`, all theory, worked code, expected output, practice, and objective assessment remain available; attempting to run a laboratory produces an explicit local-runtime message.

## Requirements

- Python 3.11 or 3.12
- A desktop environment capable of running Qt 6
- R with `Rscript` on `PATH` only when executable BMB830 or BMB831 laboratories are required
- Ollama only when local tutor or written-feedback support is required

## Installation

Clone the repository and create a virtual environment:

```bash
git clone https://github.com/jennerfeijoo/Computational_Biomedicine_Study_Hub.git
cd Computational_Biomedicine_Study_Hub
python -m venv .venv
```

Activate the environment.

### Windows PowerShell

```powershell
.\.venv\Scripts\Activate.ps1
```

### Linux or macOS

```bash
source .venv/bin/activate
```

Install the application and development dependencies:

```bash
python -m pip install --upgrade pip
python -m pip install -e ".[dev]"
```

## Run the application

```bash
cb-study-hub
```

Alternative:

```bash
python -m computational_biomedicine_study_hub.application
```

## Quality checks

Run the same checks used by GitHub Actions:

```bash
ruff check .
ruff format --check .
mypy
pytest
```

GitHub Actions validates the project independently with Python 3.11 and Python 3.12.

For headless Linux execution, including CI:

```bash
QT_QPA_PLATFORM=offscreen pytest
```

## Project structure

```text
src/computational_biomedicine_study_hub/
├── content/        # Academic models and course modules
├── courses/        # Course registration and course-page construction
├── i18n/           # Locale resolution, UI copy, and language control
├── integrations/   # Optional local services such as Ollama
├── learning/       # Practice, assessment, review, execution, and learner-state models
├── storage/        # SQLite and atomic local sidecar persistence
├── tutoring/       # Authored retrieval, diagnostics, and bounded model prompts
└── ui/             # PySide6 application shell, pages, and widgets

tests/              # Unit, content-integrity, localization, persistence, and UI tests
```

## Design principles

- **Offline-first:** essential academic material remains available without internet access.
- **Strictly trilingual:** completed content must exist in Spanish, English, and Danish without silent fallback.
- **Course-aware:** courses share the application shell but may use different academic structures.
- **Stable assessment identity:** deterministic grading uses internal IDs rather than translated visible text.
- **Model-bounded:** Ollama provides grounded assistance but cannot replace deterministic assessment or mutate mastery automatically.
- **Learner-owned writing:** edits invalidate feedback attached to older text, and drafts remain stored locally.
- **Conservative local execution:** editable Python and R laboratories run with explicit time, output, and capability boundaries.
- **Synthetic-data honesty:** Synthea is useful for reproducible technical practice but is not real-patient or omics evidence.
- **Individual assessment focus:** group presentation workflows are intentionally excluded; oral reasoning is prepared through structured individual drills rather than fabricated audio grading.
- **Lazy UI construction:** heavy readers are created only when selected.
- **Testable:** content and interface behavior are protected by automated regression tests.
- **Incremental:** new courses and features are added through reviewable pull requests.

## Development status

Active development. DM857 and DM847 provide complete authored course sequences, although additional executable practice remains desirable. BMB830 contains twelve complete modules covering foundations through an individual high-dimensional proteomics case. BMB831 now contains its first complete module on Synthea-based relational and longitudinal workflows, while advanced modelling, detailed visualisation, multivariate methods, publication appraisal, protein characterisation, omics pipelines, a downloaded versioned dataset snapshot, and the individual English report workflow remain to be implemented. Shared flashcard, glossary, search, notes, export, backup, and distribution workflows remain under development.
