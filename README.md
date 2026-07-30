# Computational Biomedicine Study Hub

Offline-first desktop study companion for the MSc in Computational Biomedicine at the University of Southern Denmark.

The application combines concise theory, worked examples, executable code, guided practice, objective assessment, common misconceptions, and retrieval-ready tutor material. Academic content is authored in Spanish, English, and Danish while preserving language-independent assessment identities.

## Current implementation

### Completed course content

- **DM857 — Introduction to Programming**
  - 14 complete modules
  - Python foundations, control flow, functions, data structures, recursion, trees, abstract data types, object-oriented programming, scientific libraries, testing, debugging, and software quality
- **DM847 — Introduction to Bioinformatics**
  - 10 complete modules
  - molecular information, ontologies and databases, sequence scoring, pairwise alignment, hidden Markov models, suffix arrays and BWT, bacterial genetics, motif discovery, biological networks, and omics learning

### Registered first-semester courses

- **DM857** — Introduction to Programming
- **DM847** — Introduction to Bioinformatics
- **BMB830** — Biostatistics in R I
- **BMB831** — Biostatistics in R II

BMB830 and BMB831 are registered in the application shell but their complete academic modules are not yet implemented.

## Main capabilities

- Immediate language switching between **ES**, **EN**, and **DK**
- Stable question and answer identities across translations
- Lazy construction of course modules and reader sections
- Guided practice and self-correcting objective assessments
- Retrieval-ready tutor documents generated from validated course content
- Optional local Ollama integration
- Persistent navigation, window geometry, language, and Ollama preferences
- Automated validation of content, localization, executable examples, UI behavior, and assessment integrity

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

## Requirements

- Python 3.11 or 3.12
- A desktop environment capable of running Qt 6
- Ollama only when the local tutor integration is required

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
├── learning/       # Practice, assessment, retrieval, and tutor logic
└── ui/             # PySide6 application shell, pages, and widgets

tests/              # Unit, content-integrity, localization, and UI tests
```

## Design principles

- **Offline-first:** essential academic material remains available without internet access.
- **Strictly trilingual:** completed content must exist in Spanish, English, and Danish without silent fallback.
- **Course-aware:** courses share the application shell but may use different academic structures.
- **Stable assessment identity:** grading uses internal IDs rather than translated visible text.
- **Lazy UI construction:** heavy readers are created only when selected.
- **Testable:** content and interface behavior are protected by automated regression tests.
- **Incremental:** new courses and features are added through reviewable pull requests.

## Development status

Active development. DM857 and DM847 provide the first complete academic course implementations. Shared revision, flashcard, glossary, and cross-course assessment pages remain under development.
