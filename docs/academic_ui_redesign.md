# Academic UI redesign

Branch: `feat/academic-ui-redesign`

Base: `feat/semester-1-learning-engine`

## Product direction

The interface is evolving toward a restrained **digital academic laboratory** rather than a
collection of administrative forms. The design must remain readable for long scientific text,
code, statistical output and trilingual content while making the next learning action obvious.

## Design principles

1. Academic content remains the source of truth; presentation does not alter scientific meaning.
2. Progress is evidence-based and never inferred from decorative interaction alone.
3. Primary actions are visually dominant; metadata and technical identifiers remain secondary.
4. Course identity is communicated through a controlled accent, not a separate visual system.
5. Motion is brief, purposeful and compatible with keyboard navigation.
6. Components preserve stable object names where existing tests or integrations depend on them.
7. New interface layers do not import SQL or mutate the canonical YAML content.

## Phase 1 implemented

### Central design system

`ui/design_system.py` defines:

- canvas, surface, border and text colors;
- semantic primary, success, warning and danger colors;
- spacing and radius tokens;
- restrained card elevation;
- course accents for DM857, DM847, BMB830 and BMB831;
- a stylesheet extension loaded after the existing application QSS.

No external UI dependency is required for this phase.

### Responsive navigation

The sidebar now supports:

- expanded and compact icon-only states;
- a 180 ms width transition;
- persistent compact state through `QSettings`;
- native Qt icons, tooltips and accessible names;
- immediate retranslation without losing the active route;
- the same route IDs and signals used before the redesign.

### Learner-centred dashboard

The previous static four-card page is replaced by a refreshable dashboard containing:

- continue-study action based on the most recent attempt;
- direct access to due review;
- due activity count;
- modules started across the semester;
- most recent activity;
- course cards with evidence-based progress, pending reviews and success ratio;
- localized Spanish, English and Danish copy;
- automatic refresh whenever the user returns to Home.

The dashboard reads through `AcademicCatalog` and `ProgressRepository`; it does not access
SQLite directly.

## Compatibility measures

- Existing `courseCard`, `courseOpenButton`, `courseCardCode`, `courseCardTitle`,
  `courseCardMetadata` and `courseCardSummary` object names are preserved.
- Existing course routes and navigation signals are unchanged.
- The original application stylesheet remains active; the design-system stylesheet is an
  additive override.
- The dashboard works without a catalog or repository so lightweight widget tests and isolated
  previews remain possible.

## Validation added

`tests/test_academic_ui_design.py` verifies:

- navigation labels disappear only visually in compact mode;
- tooltips and accessible names remain available;
- expanding restores labels;
- four course cards and four open buttons remain discoverable through their previous object
  names;
- dashboard refresh reconstructs its visible course cards.

## Next phases

### Phase 2 — shared academic components

- standard section headers and status badges;
- empty-state component;
- semantic callouts for assumptions, misconceptions, interpretation and limitations;
- unified code/output blocks;
- compact course-module toolbar across all four courses.

### Phase 3 — focused study experience

- concentration mode that hides navigation and secondary controls;
- controlled content width and larger reading typography;
- keyboard-first movement between module sections;
- progress-aware module map.

### Phase 4 — learning analytics

- weekly activity heatmap;
- due-review trend;
- mastery distribution by course and module;
- recurring-error overview;
- accessible charts using a Qt-native or PyQtGraph adapter.

### Phase 5 — selective richer interaction

- QML only for components where it produces measurable value, such as flashcard transitions or
  a module map;
- reduced-motion setting;
- light, dark and system appearance modes;
- onboarding and contextual keyboard-shortcut help.

## Dependency policy

The current phase deliberately uses PySide6 only. Future candidates must be evaluated before
adoption:

- `qtawesome` for a consistent vector icon registry;
- `pyqtgraph` for learning analytics and scientific plots;
- `QScintilla` only if editable code workflows justify its packaging and licensing cost;
- Qt Quick/QML only as isolated visual components, not as a full rewrite.

No general-purpose theme library should be combined with the custom design system without a
prototype and regression review.
