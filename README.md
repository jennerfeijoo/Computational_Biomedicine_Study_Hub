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
  - 8 complete modules
  - R objects and reproducible workflows
  - data quality, descriptive statistics, and scientific visualization
  - probability, sampling, and reference distributions
  - estimation, standard errors, and confidence intervals
  - hypothesis tests, type I and II errors, power, and effect sizes
  - independent, paired, and multi-group comparisons with assumptions and multiplicity control
  - correlation, association versus causation, and simple linear regression
  - confidence intervals for conditional means and individual prediction intervals
  - multiple regression, design matrices, adjusted coefficients, factors, reference levels, confounding, and collinearity
  - 128 stable objective-bank questions
  - optional editable R laboratories executed through a locally installed `Rscript`

The remaining BMB830 blocks on interactions, model diagnostics, model comparison, and introductory multivariate analysis are under development.

### Registered first-semester courses

- **DM857** — Introduction to Programming
- **DM847** — Introduction to Bioinformatics
- **BMB830** — Biostatistics in R I
- **BMB831** — Biostatistics in R II

BMB831 is registered in the application shell, but its complete academic modules are not yet implemented.

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

BMB830 worked examples can be edited and executed when `Rscript` is available on the local `PATH`. The runner uses `Rscript --vanilla`, a temporary working directory, a hard timeout, bounded output, and a conservative policy that rejects file, network, external-process, package-installation, dynamic-evaluation, and native-code capabilities.

R is optional. Without `Rscript`, all BMB830 theory, worked code, expected output, practice, and objective assessment remain available; attempting to run a laboratory produces an explicit local-runtime message.

## Requirements

- Python 3.11 or 3.12
- A desktop environment capable of running Qt 6
- R with `Rscript` on `PATH` only when executable BMB830 laboratories are required
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
- **Lazy UI construction:** heavy readers are created only when selected.
- **Testable:** content and interface behavior are protected by automated regression tests.
- **Incremental:** new courses and features are added through reviewable pull requests.

## Development status

Active development. DM857 and DM847 provide complete academic course implementations. BMB830 contains eight complete modules covering foundations through multiple regression and design matrices; interactions, diagnostics, model comparison, and introductory multivariate analysis remain under development. Shared flashcard, glossary, search, notes, export, backup, and distribution workflows remain under development. Group-presentation rehearsal is intentionally outside the application scope.
