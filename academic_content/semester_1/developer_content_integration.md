# Content integration guidance

## Scope

This branch contains canonical academic material. Implementation work must consume it without changing its scientific meaning, stable identifiers, language alignment, answer keys, rubrics, source mappings, or documented limitations.

The content source is intentionally independent of the graphical interface. Runtime classes, database tables, widgets, and serializers may differ from the authoring format, but the transformation must be deterministic and testable.

## General integration rules

1. Preserve every stable ID exactly.
2. Use IDs, not translated text, for persistence, grading, linking, and progress.
3. Validate all three locales before making a package available.
4. Keep canonical academic files read-only at runtime.
5. Store learner state separately from content.
6. Never infer a correct answer from display order.
7. Do not silently discard unsupported fields or activity types.
8. Report schema incompatibilities explicitly.
9. Keep hidden support material outside the standard module reader.
10. Do not expose answer keys or grading criteria during an active graded session.

## Memory-card implementation

### Required card fields

Each runtime card must preserve:

- `id`;
- `module_id`;
- `mode`;
- `card_type`;
- `difficulty`;
- localized `front`;
- localized `back`;
- `linked_objectives`;
- `linked_concepts`;
- `tags`;
- optional code, formula, data snippet, hint, follow-up, and accepted answer elements.

### Card presentation

The card page should provide:

- course and module filters;
- card-type and difficulty filters;
- conceptual, practical, and mixed sessions;
- shuffled order without changing card identity;
- front reveal followed by the structured back;
- selectable text;
- monospaced formatting for code;
- readable mathematical notation;
- preserved line breaks and lists;
- support for long answers through scrolling rather than truncation;
- keyboard navigation;
- clear focus state;
- language switching without losing the active card or review state.

### Review controls

After revealing the answer, provide four learner ratings:

- Again;
- Hard;
- Good;
- Easy.

Store scheduling data outside the canonical content:

- last review time;
- next review time;
- interval;
- stability or ease value;
- review count;
- lapse count;
- last rating.

The scheduling algorithm must be isolated from the card widget and covered by unit tests.

### Practical cards

Practical cards may include code, formulas, compact tables, or workflow fragments.

- Do not reduce them to plain definition cards.
- Preserve code indentation and exact symbols.
- For output-prediction cards, reveal both the result and the reasoning trace.
- For calculation cards, show setup, intermediate reasoning, units, and interpretation.
- For method-selection cards, show the selected method, decisive evidence, assumptions, and rejected alternative.
- For debugging cards, show root cause, correction, validation, and prevention.
- For interpretation cards, separate direct reading, uncertainty, prohibited overclaim, and next validation step.

### Open retrieval

Some cards ask for an explanation rather than a fixed phrase.

- Do not use exact-string grading.
- Use `accepted_answer_elements` as a self-check rubric.
- Allow the learner to reveal the answer and rate recall quality.
- Preserve multiple scientifically valid formulations.

### Reverse cards

Only cards with `reverse_allowed: true` may be presented in reverse.

Do not automatically reverse:

- misconception cards;
- output-interpretation cards;
- debugging cards;
- workflow-order cards;
- scenario-based method-selection cards;
- oral-defense cards.

### Session construction

A balanced standard-module session should sample:

- at least one definition or mechanism card;
- at least one assumption or interpretation card;
- at least one practical card;
- at least one misconception card;
- no duplicate concept unless the learner is in targeted review mode.

A cumulative session should:

- respect prerequisite order;
- mix retrieval from several modules;
- increase representation of overdue and weak concepts;
- avoid selecting multiple superficial variants of the same fact.

### Progress views

Expose, at minimum:

- due cards;
- new cards;
- reviewed cards;
- lapse count;
- module coverage;
- objective coverage;
- conceptual versus practical performance;
- recent review history.

Do not equate number of reviews with mastery. Mastery estimates should incorporate accuracy, spacing, difficulty, and repeated successful retrieval.

## Content validation

Add automated validation for:

- unique IDs;
- valid module references;
- valid objective and concept references;
- complete ES, EN, and DA fields;
- required card counts;
- required category distribution;
- valid card modes and types;
- no empty front or back;
- no duplicate normalized prompts within a module;
- reverse-card eligibility;
- code-block preservation;
- formulas stored without translation damage;
- stable identity across locales.

Add a coverage report showing, for every module:

- number of cards;
- number by mode;
- number by type;
- number by difficulty;
- objectives without sufficient cards;
- concepts without conceptual cards;
- concepts without practical cards;
- untranslated fields;
- duplicate or near-duplicate prompts.

## Content ingestion

Recommended flow:

1. Parse canonical YAML.
2. Validate schema and references.
3. Materialize the selected locale.
4. Map canonical activity and card types to registered runtime renderers.
5. Keep unsupported packages unavailable rather than partially rendering them.
6. Emit a deterministic validation report.
7. Run regression tests against all previously released content versions.

## Hidden guided-support material

Each module includes material that must not appear as ordinary lesson text:

- canonical explanations;
- misconception catalogue;
- Socratic prompts;
- grading criteria;
- response constraints;
- escalation rules;
- source anchors.

Store and index this material separately from standard reader content. Retrieval must remain scoped to the active course, module, locale, and task. During graded work, exclude answer keys and protected grading material.

## Versioning

- Content versions use semantic versioning.
- Patch: wording, translation, or non-semantic correction.
- Minor: new cards, examples, or activities without changing existing answer identity.
- Major: changed learning meaning, removed IDs, changed answer keys, or incompatible schema.
- Retired IDs must not be reused.
- Learner history should remain readable after content updates.

## Acceptance criteria

Integration is acceptable only when:

- every canonical package validates;
- all three locales materialize;
- IDs remain stable;
- memory-card counts and distributions match the coverage plan;
- learner progress survives language changes and restarts;
- practical card formatting is preserved;
- unsupported content is reported rather than silently omitted;
- hidden support and answer keys remain protected;
- automated tests cover parsing, validation, presentation, persistence, and review scheduling.
