# Adding and Removing Courses

This guide documents the current developer workflow for adding or removing a course from Computational Biomedicine Study Hub. It describes the existing Python-based architecture. It does not introduce a plugin system, external course format, or end-user course editor.

## 1. Scope and integration levels

A course can be integrated at three levels:

1. **Catalog only** — the course appears in the home page and sidebar and provides its own `QWidget` page.
2. **Standard modular course** — the course uses authored `LearningModule` content, a module selector, the shared `ModuleReaderPage`, guided practice, and objective assessment.
3. **Fully tracked modular course** — objective questions are linked to learning objectives and attempts are persisted for review, mastery, and the error notebook.

A new course should normally target level 2. Use level 3 when its activity-to-objective mapping has been authored and validated.

## 2. Choose the nearest existing template

Start from the course whose behavior is closest to the new subject:

- `courses/dm847.py` — general multi-module course with objective assessment and optional persistent objective evidence.
- `courses/dm857.py` — programming course with executable Python work and course-specific project workflows.
- `courses/bmb830.py` — multi-module course with editable R laboratories.
- `courses/bmb831.py` — advanced biostatistics and omics course with R laboratories and additional persistent writing workflows.

Do not copy a specialized workflow unless the new course actually needs it.

## 3. Stable naming rules

Choose identifiers before authoring content.

Example course:

```text
Course code: GEN101
Course package: gen101
Course route: course/gen101
Module IDs: gen101.m01, gen101.m02, ...
Objective IDs: m01.o1, m01.o2, ...
Practice IDs: m01.p01, m01.p02, ...
Objective bank IDs: gen101.m01.bank.001, gen101.m01.bank.002, ...
```

Rules:

- Course codes and routes must be unique.
- Module IDs must be stable and unique within the repository.
- Activity IDs must not be reused for unrelated content.
- Do not reuse a removed course code or module ID for a different subject. Existing local progress may still refer to those identifiers.
- Changing visible wording does not require changing an ID. Changing the meaning of an activity usually does.

## 4. Create the content package

Create:

```text
src/computational_biomedicine_study_hub/content/gen101/
├── __init__.py
├── module_01_genome_organization.py
├── module_02_dna_replication.py
├── source_catalog.py          # recommended
└── source_audit.py            # recommended
```

Each completed module should be authored using the localized content models in:

```text
src/computational_biomedicine_study_hub/content/localized_models.py
```

The runtime models require a complete module with:

- title and summary;
- learning objectives;
- concept blocks;
- worked examples;
- guided practice exercises;
- authored assessment items;
- tutor support material.

A module that omits a required collection is rejected during import or testing.

### Minimal module structure

The exact content will be longer, but the shape is:

```python
from computational_biomedicine_study_hub.content.localized_models import (
    LocalizedAssessmentItem,
    LocalizedAssessmentOption,
    LocalizedConceptBlock,
    LocalizedLearningModule,
    LocalizedLearningObjective,
    LocalizedPracticeExercise,
    LocalizedText,
    LocalizedTutorSupportPacket,
    LocalizedWorkedExample,
)
from computational_biomedicine_study_hub.learning import ActivityType


def text(es: str, en: str, da: str) -> LocalizedText:
    return LocalizedText(spanish=es, english=en, danish=da)


LOCALIZED_MODULE_01 = LocalizedLearningModule(
    course_code="GEN101",
    module_id="gen101.m01",
    title=text(
        "Organización del genoma",
        "Genome organization",
        "Genomets organisering",
    ),
    summary=text("...", "...", "..."),
    objectives=(
        LocalizedLearningObjective(
            objective_id="m01.o1",
            statement=text("...", "...", "..."),
        ),
    ),
    concepts=(
        LocalizedConceptBlock(
            concept_id="m01.c01",
            title=text("...", "...", "..."),
            body=text("...", "...", "..."),
            key_points=(text("...", "...", "..."),),
        ),
    ),
    worked_examples=(
        LocalizedWorkedExample(
            example_id="m01.e01",
            title=text("...", "...", "..."),
            problem=text("...", "...", "..."),
            reasoning=(text("...", "...", "..."),),
            code=text("", "", ""),
            expected_output=text("", "", ""),
            explanation=text("...", "...", "..."),
        ),
    ),
    practice_exercises=(
        LocalizedPracticeExercise(
            exercise_id="m01.p01",
            activity_type=ActivityType.SHORT_ANSWER,
            prompt=text("...", "...", "..."),
            hints=(text("...", "...", "..."),),
            solution=text("...", "...", "..."),
            explanation=text("...", "...", "..."),
        ),
    ),
    assessment_items=(
        # Add at least one authored assessment item.
    ),
    tutor_support=LocalizedTutorSupportPacket(
        canonical_explanation=text("...", "...", "..."),
        knowledge_fragments=(text("...", "...", "..."),),
        common_misconceptions=(text("...", "...", "..."),),
        socratic_questions=(text("...", "...", "..."),),
        grading_criteria=(text("...", "...", "..."),),
        response_constraints=(text("...", "...", "..."),),
        source_basis=("Source identifier or bibliographic reference",),
    ),
)
```

The example above is structural. Replace every placeholder and ensure all required collections are non-empty. For text-free worked examples, use a meaningful non-empty description rather than empty localized strings because `LocalizedText` rejects empty values.

## 5. Author the objective question bank

The interactive objective evaluator currently supports:

- `ActivityType.MULTIPLE_CHOICE`;
- `ActivityType.TRUE_FALSE`.

The default session contains six questions, so each module bank must contain at least six valid items. A larger bank is strongly preferred so sessions vary meaningfully.

Use stable option IDs so grading remains independent of translation:

```python
LOCALIZED_OBJECTIVE_QUESTION_BANK_01 = (
    LocalizedAssessmentItem(
        item_id="gen101.m01.bank.001",
        activity_type=ActivityType.MULTIPLE_CHOICE,
        prompt=text("...", "...", "..."),
        options=(
            LocalizedAssessmentOption(
                option_id="option_a",
                text=text("...", "...", "..."),
            ),
            LocalizedAssessmentOption(
                option_id="option_b",
                text=text("...", "...", "..."),
            ),
        ),
        correct_option_ids=("option_a",),
        accepted_answers=(),
        explanation=text("...", "...", "..."),
    ),
)
```

Every bank item ID must begin with the complete module ID followed by a period.

## 6. Create validated module bundles

In `content/gen101/__init__.py`, combine modules, question banks, and content versions:

```python
from computational_biomedicine_study_hub.i18n import AppLocale
from computational_biomedicine_study_hub.content.bundles import (
    LocalizedModuleBundle,
    validate_bundle_catalog,
)

from .module_01_genome_organization import (
    LOCALIZED_MODULE_01,
    LOCALIZED_OBJECTIVE_QUESTION_BANK_01,
)

LOCALIZED_BUNDLES = (
    LocalizedModuleBundle(
        localized_module=LOCALIZED_MODULE_01,
        localized_objective_question_bank=LOCALIZED_OBJECTIVE_QUESTION_BANK_01,
        content_version="1.0.0",
    ),
)

validate_bundle_catalog(LOCALIZED_BUNDLES)

BUNDLES = tuple(
    bundle.materialize(AppLocale.SPANISH_SPAIN)
    for bundle in LOCALIZED_BUNDLES
)
```

Bundle validation checks non-empty versions, non-empty question banks, identifier scope, supported objective item types, module uniqueness, and course consistency.

## 7. Link activities to objectives for persistent learning evidence

The evaluator can display questions without persistence. To contribute to mastery, spaced review, and the error notebook, every assessable activity must be linked to one or more learning objectives.

Add an `ObjectiveLinkCatalog` in:

```text
src/computational_biomedicine_study_hub/content/objective_links.py
```

Example:

```python
GEN101_M01_OBJECTIVE_LINKS = ObjectiveLinkCatalog(
    module_id="gen101.m01",
    links=(
        ObjectiveLink(
            activity_id="m01.p01",
            objective_ids=("m01.o1",),
        ),
        ObjectiveLink(
            activity_id="gen101.m01.bank.001",
            objective_ids=("m01.o1",),
        ),
    ),
)
```

Register it in `_CATALOGS`:

```python
_CATALOGS = {
    DM847_M01_OBJECTIVE_LINKS.module_id: DM847_M01_OBJECTIVE_LINKS,
    GEN101_M01_OBJECTIVE_LINKS.module_id: GEN101_M01_OBJECTIVE_LINKS,
}
```

`ObjectiveLinkCatalog.validate_against(...)` requires exact coverage of the module's guided practice, authored assessments, and objective question bank. It also rejects references to objectives that do not exist.

Do not enable persistent objective recording until this mapping validates.

## 8. Create the course page

Create:

```text
src/computational_biomedicine_study_hub/courses/gen101.py
```

For a normal multi-module course, copy the structure of `courses/dm847.py` or `courses/bmb830.py` and change:

- imports;
- page and reader class names;
- object names;
- course-code label;
- `COURSE` metadata;
- any specialized laboratory widget.

The page must expose a locale-aware factory:

```python
def create_page(locale: AppLocale = DEFAULT_LOCALE) -> QWidget:
    return GEN101Page(locale)
```

Register the visible course metadata:

```python
COURSE = CourseRegistration(
    code="GEN101",
    title="Genética molecular",
    ects=5,
    semester=1,
    summary="Organización, replicación, expresión y regulación del genoma.",
    page_factory=create_page,
    localized_titles={
        AppLocale.SPANISH_SPAIN: "Genética molecular",
        AppLocale.ENGLISH: "Molecular Genetics",
        AppLocale.DANISH_DENMARK: "Molekylær genetik",
    },
    localized_summaries={
        AppLocale.SPANISH_SPAIN: "...",
        AppLocale.ENGLISH: "...",
        AppLocale.DANISH_DENMARK: "...",
    },
)
```

## 9. Register the course in the central catalog

Edit:

```text
src/computational_biomedicine_study_hub/courses/catalog.py
```

Add the import:

```python
from .gen101 import COURSE as GEN101
```

Add the course to `COURSES`:

```python
COURSES: tuple[CourseRegistration, ...] = (
    DM857,
    DM847,
    BMB830,
    BMB831,
    GEN101,
)
```

The home page, sidebar, route, header, title, and summary are derived from this catalog. `validate_catalog()` rejects duplicate codes and routes.

Update `tests/test_course_catalog.py` so the expected codes, routes, and ECTS totals match the new catalog.

## 10. Optional full-progress integration

The current architecture uses explicit course-specific hooks for some fully tracked modular courses.

### Application-level recorder

When the course page accepts a shared progress recorder, add its configuration in:

```text
src/computational_biomedicine_study_hub/application.py
```

Follow the existing DM847 or DM857 pattern:

```python
from .courses.gen101 import configure_progress_recorder as configure_gen101_progress_recorder

# Inside main(...)
configure_gen101_progress_recorder(progress_service)
```

### Restoring module and section position

`MainWindow` currently recognizes selected modular page classes explicitly. To preserve the current module and tab across language changes and to open the course from review, update:

```text
src/computational_biomedicine_study_hub/ui/main_window.py
```

Add the page class to:

- the imports;
- `ModularCoursePage`;
- `_modular_course_page(...)`.

This step is not required for basic navigation, but it is required for the same location-restoration behavior currently provided to recognized modular pages.

## 11. Add tests

At minimum, add tests for:

- course registration and stable route;
- all required module sections;
- non-empty and unique IDs;
- complete ES, EN, and DA materialization;
- at least six valid objective questions per module;
- stable answer identities across locales;
- active evaluation rendering for every module;
- exact objective-link coverage when persistence is enabled;
- progress persistence under the expected course, module, item, and objective IDs;
- source catalog and source audit when the course makes academic coverage claims;
- specialized executable examples or laboratories, when present.

Recommended file names:

```text
tests/test_gen101_course.py
tests/test_gen101_content.py
tests/test_gen101_localization.py
tests/test_gen101_assessment.py
tests/test_gen101_objective_links.py
```

## 12. Validate before merging

Run the same checks as GitHub Actions:

```bash
ruff check .
ruff format --check .
mypy
pytest
```

For a focused first pass:

```bash
pytest tests/test_course_catalog.py tests/test_gen101_*.py
```

Do not merge a course while content validation, localization, assessment integrity, or objective-link tests are failing.

---

# Removing a Course

Removing a course from the visible application is simpler than deleting all of its content.

## 13. Recommended safe removal: unregister first

Edit:

```text
src/computational_biomedicine_study_hub/courses/catalog.py
```

Remove the course import and remove it from `COURSES`.

This immediately removes it from:

- the home-page course list;
- the navigation sidebar;
- route registration;
- normal application access.

Keeping the content and course files temporarily is useful when the removal may be reversed or when historical data must remain inspectable.

## 14. Remove course-specific integrations

When applicable, remove:

- the course progress-recorder import and configuration from `application.py`;
- the page import from `ui/main_window.py`;
- the page class from `ModularCoursePage`;
- the page class from `_modular_course_page(...)`;
- course-specific persistent pages or workflows;
- course-specific CLI entry points;
- course-specific datasets or source registries that are no longer used.

Do not remove shared infrastructure used by other courses.

## 15. Update tests and documented catalog claims

Update:

- `tests/test_course_catalog.py`;
- tests that enumerate all courses;
- README course lists and totals;
- source-audit summaries;
- documentation that names the removed course;
- any expected navigation labels or routes.

Run a repository search for the course code before deleting files:

```bash
rg -n "GEN101|gen101" .
```

Review every match rather than deleting mechanically.

## 16. Decide whether to delete the implementation

After the course is unregistered and all references are removed, the following may be deleted if the course is permanently retired:

```text
src/computational_biomedicine_study_hub/courses/gen101.py
src/computational_biomedicine_study_hub/content/gen101/
tests/test_gen101_*.py
```

Keep source-license records or provenance documents when their retention is legally or scientifically necessary.

## 17. Existing learner data

Unregistering or deleting course code does **not** automatically delete rows from the user's local SQLite progress database.

Consequences:

- historical attempts may remain stored but become unreachable from the current navigation;
- review items for an unregistered route may no longer open the original module;
- reusing the same course, module, objective, or item IDs for unrelated material can attach old evidence to new content.

Therefore:

- never reuse retired IDs for a different meaning;
- treat database cleanup as a separate, explicit migration;
- do not silently delete learner data during course removal;
- document any intentional migration or purge.

## 18. Final removal checklist

```text
[ ] Removed from courses/catalog.py
[ ] Removed course-specific progress configuration
[ ] Removed course-specific MainWindow type checks
[ ] Updated catalog and navigation tests
[ ] Updated README and documentation
[ ] Searched the repository for remaining references
[ ] Decided whether implementation files should be retained or deleted
[ ] Preserved or migrated learner data deliberately
[ ] Ran ruff, mypy, and pytest successfully
```

# Pull request checklist for a new course

```text
[ ] Stable course code, route, module IDs, objective IDs, and item IDs
[ ] Complete ES, EN, and DA content
[ ] Required module collections are non-empty
[ ] At least six objective questions per module
[ ] Deterministic answer keys use stable option IDs
[ ] Content version assigned to every module bundle
[ ] Objective links complete before persistence is enabled
[ ] Course registered in the central catalog
[ ] Course location restoration added when required
[ ] Source basis and licensing reviewed
[ ] Course-specific and full test suites pass
```
