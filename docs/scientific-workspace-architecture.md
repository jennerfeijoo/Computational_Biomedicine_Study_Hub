# Scientific laboratory workspace architecture

## Purpose

The computational-laboratory route now supports two complementary execution levels:

1. the existing restricted single-response checkpoint for short, deterministic tasks;
2. a persistent multi-file scientific workspace for datasets, source code, tests, reports, and generated outputs.

The workspace is intended to make laboratory preparation resemble a small reproducible computational investigation rather than a sequence of disconnected code snippets.

## Directory contract

The DM857 pilot materializes the following structure beside the local progress database:

```text
<progress database>.workspaces/
└── dm857_lab01_workspace/
    ├── README.md
    ├── data/
    │   └── measurements.csv
    ├── metadata/
    │   └── data_dictionary.csv
    ├── student/
    │   └── analysis.py
    ├── tests/
    │   └── test_analysis.py
    ├── report.md
    ├── output/
    │   ├── last_run.txt
    │   └── last_tests.txt
    └── .workspace-manifest.json
```

Learner-owned files are preserved when the workspace is materialized again. Authored read-only files are refreshed from the application so that datasets, tests, documentation, and metadata remain consistent with the registered workspace version.

## Execution boundary

The application executes only the exact authored script or test entrypoint. It does not expose a shell, package installation, arbitrary commands, or user-selected executable paths.

Before execution, learner-owned Python files are parsed and checked against the laboratory import allowlist. Network, process-management, dynamic-import, and similar capabilities are rejected. The subprocess also blocks network sockets and writes outside the workspace root. Environment variables are reduced and proxy variables are cleared.

This is a controlled educational execution boundary, not a claim of hostile-code operating-system isolation. Workspaces are application-owned and intended for the enrolled learner's own code.

## Pedagogical use

The workspace preserves a separation between:

- implementation correctness demonstrated by authored tests;
- biomedical interpretation written by the learner;
- model-generated feedback from Ollama;
- objective mastery recorded by deterministic learning activities.

Passing workspace tests does not establish clinical validity. Ollama receives only the active file, the authored file list, and the latest execution record. It is instructed to ask one diagnostic question before suggesting code and never receives the authored test source as content.

## Expansion path

The same domain can support later laboratories with explicitly declared dependencies and entrypoints:

- DM847 sequence algorithms, indexes, and small omics classifiers;
- BMB830 R analysis projects with figures and model diagnostics;
- BMB831 larger omics pipelines, reproducible reports, and interpretation artifacts.

Scientific dependencies should be added per laboratory rather than globally. Dataset provenance, licenses, checksums, and versioned environment descriptions remain mandatory before public release of each laboratory.
