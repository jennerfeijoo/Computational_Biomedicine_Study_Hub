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

## Incremental integration order

1. strict locale and catalog domain layer;
2. persisted language preference;
3. shell and navigation retranslation;
4. settings selector and immediate page rebuild;
5. localized course metadata;
6. localized learning-module data models;
7. complete DM857 module 1 translations;
8. tutor retrieval over the selected language;
9. translation coverage checks for every future module;
10. packaging tests in all three languages.

The language selector must not expose partially translated academic material. A locale becomes visible in the final interface only when the currently reachable content is complete in that locale.
