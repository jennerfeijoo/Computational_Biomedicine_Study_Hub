# Internationalization contract

The application supports exactly three locales:

- `es-ES` — Spanish used in Spain
- `en` — English
- `da-DK` — Danish used in Denmark

## Non-negotiable rules

1. Every user-facing translation key must exist in every catalog.
2. Missing strings are programming errors; the application must not display raw keys.
3. Catalogs must use the same formatting placeholders.
4. Academic content must be authored and reviewed in all three languages before a language is exposed for that content.
5. Code, library names, commands and official identifiers remain technically accurate rather than being translated mechanically.
6. The selected locale will ultimately control the shell, academic content, activities, feedback, diagnostics and Ollama tutor prompts.
7. Release validation must fail when any visible string or academic field lacks one of the three locales.

## Academic authoring contract

`LocalizedText` requires non-empty Spanish, English and Danish values at construction time. Academic structures use stable language-independent identifiers and localized visible text.

Assessment options have stable IDs. Correct answers reference those IDs instead of translated option labels, so grading remains deterministic when the displayed language changes.

A `LocalizedLearningModule` can be materialized into the existing runtime `LearningModule` for one selected locale. The reader, practice engine, assessment engine and tutor therefore consume one coherent language without duplicating their business logic.

The following fields are localized when they can be visible or supplied to Ollama:

- module titles, summaries and objectives;
- concept titles, explanations and key points;
- worked-example problems, reasoning, code, output and explanation;
- practice prompts, hints, starter code, solutions and feedback;
- assessment prompts, options, accepted answers, explanations and rubrics;
- canonical tutor explanations, misconceptions, Socratic questions, grading criteria and response constraints.

Stable identifiers, activity types and bibliographic source references are language-independent.

## Incremental integration order

1. strict locale and catalog domain layer;
2. localized learning-module data models;
3. complete DM857 module 1 translations;
4. persisted language preference;
5. shell and navigation retranslation;
6. settings selector and immediate page rebuild;
7. localized course metadata;
8. tutor retrieval over the selected language;
9. translation coverage checks for every future module;
10. packaging tests in all three languages.

The language selector must not expose partially translated academic material. A locale becomes visible in the final interface only when the currently reachable content is complete in that locale.
