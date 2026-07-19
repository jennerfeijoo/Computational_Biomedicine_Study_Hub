# Semester 1 academic content workspace

This directory contains the implementation-independent academic source for the first semester of the MSc in Computational Biomedicine:

- **DM857 — Introduction to Programming**
- **DM847 — Introduction to Bioinformatics**
- **BMB830 — Biostatistics in R I**
- **BMB831 — Biostatistics in R II**

The material is authored before UI integration. Codex or another implementation agent must consume these packages without rewriting their scientific meaning, answer keys, rubrics, identifiers, or language alignment.

## Authoring principles

1. **Official-outcome alignment.** Every module maps to one or more approved SDU learning outcomes.
2. **Problem-first teaching.** Biological, medical, statistical, or computational questions precede formal methods whenever appropriate.
3. **Observable objectives.** Each objective specifies what the learner must explain, calculate, implement, diagnose, compare, or defend.
4. **Constructive alignment.** Concepts, examples, practice, assessment, flashcards, glossary terms, and tutor support map to module objectives.
5. **Trilingual parity.** Spanish, English, and Danish carry the same scientific meaning and preserve stable IDs.
6. **Original synthesis.** Sources guide factual accuracy and sequencing; no package reproduces substantial copyrighted passages.
7. **Biomedical restraint.** Synthetic examples are explicitly identified and must not be represented as validated clinical protocols.
8. **Reproducibility.** Computational examples state assumptions, inputs, expected outputs, validation checks, and limitations.
9. **Interpretation over button-pushing.** Learners must connect outputs to assumptions, uncertainty, biological meaning, and possible failure modes.
10. **Tutor grounding.** Each module contains hidden support for Qwen/Ollama: canonical explanations, misconceptions, Socratic prompts, grading criteria, response constraints, and source anchors.

## Planned package structure

```text
academic_content/semester_1/
├── README.md
├── content_contract.yaml
├── curriculum_blueprint.yaml
├── source_policy.md
├── dm857/
│   ├── course.yaml
│   ├── modules/
│   ├── cumulative_assessment.yaml
│   └── qwen_tutor/
├── dm847/
│   ├── course.yaml
│   ├── modules/
│   ├── portfolio_assessment.yaml
│   └── qwen_tutor/
├── bmb830/
│   ├── course.yaml
│   ├── modules/
│   ├── oral_exam_bank.yaml
│   └── qwen_tutor/
└── bmb831/
    ├── course.yaml
    ├── modules/
    ├── report_project.yaml
    └── qwen_tutor/
```

## Completion definition

A course is academically complete only when it has:

- an official learning-outcome map;
- a coherent module sequence;
- complete ES/EN/DA module content;
- worked examples with verified outputs;
- guided practice with hints and reference solutions;
- objective and open-response assessment;
- cumulative or exam-specific preparation;
- flashcards and glossary entries;
- Qwen/Ollama grounding material;
- source mapping and scientific limitations;
- cross-module prerequisites and review links;
- an academic quality checklist.

A course is **not** complete merely because module titles, placeholders, enums, or UI routes exist.
