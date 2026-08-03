# Adding and Removing Courses

This guide describes the current developer workflow for adding or removing a course from Computational Biomedicine Study Hub. It documents the existing Python architecture. It does not introduce a plugin system, external course format, or end-user course editor.

## Integration levels

A course can be integrated at three levels:

1. **Catalog only** — the course appears in the home page and sidebar and provides its own `QWidget` page.
2. **Standard modular course** — the course uses authored modules, the shared reader, guided practice, and objective assessment.
3. **Fully tracked modular course** — assessment activities are linked to learning objectives and attempts contribute to mastery, review, and the error notebook.

A new academic course should normally target level 2. Use level 3 only after its activity-to-objective mapping is complete and validated.

## Choose the nearest existing template

Start from the course whose behavior is closest to the new subject:

- `src/computational_biomedicine_study_hub/courses/dm847.py` — general multi-module course with objective assessment and optional persistent objective evidence.
- `src/computational_biomedicine_study_hub/courses/dm857.py` — programming course with executable Python and course-specific project workflows.
- `src/computational_biomedicine_study_hub/courses/bmb830.py` — multi-module course with editable R laboratories.
- `src/computational_biomedicine_study_hub/courses/bmb831.py` — advanced biostatistics and omics course with R laboratories and persistent writing workflows.

Do not copy a specialized workflow unless the new course needs it.

# Adding a Course

## 1. Choose stable identifiers

Define the identifiers before writing content.

```text
Course code: GEN101
Course package: gen101
Course route: course/gen101
Module IDs: gen101.m01, gen101.m02, ...
Objective IDs: m01.o1, m01.o2, ...
Practice IDs: m01.p01, m01.p02, ...
Objective-bank IDs: gen101.m01.bank.001, gen101.m01.bank.002, ...
```

Rules:

- Course codes and generated routes must be unique.
- Module, objective, activity, and option IDs must be stable.
- Do not reuse retired IDs for unrelated material.
- Visible wording may change without changing an ID when the underlying meaning remains the same.
- Change an ID when an activity is replaced by a substantially different activity.

Old learner progress may still reference removed identifiers, so identifier reuse can attach historical evidence to unrelated content.

## 2. Create the academic content package

Create a package such as:

```text
src/computational_biomedicine_study_hub/content/gen101/
├── __init__.py
├── module_01_genome_organization.py
├── module_02_dna_replication.py
├── source_catalog.py          # recommended
└── source_audit.py            # recommended
```

Use the authoring models in:

```text
src/computational_biomedicine_study_hub/content/localized_models.py
```

A completed module requires:

- course code, module ID, title, and summary;
- learning objectives;
- concept blocks;
- worked examples;
- guided practice exercises;
- authored assessment items;
- tutor support material.

The runtime models reject missing required collections and duplicate IDs.

### Localization helper

Completed content must exist in Spanish, English, and Danish.

```python
from computational_biomedicine_study_hub.content.localized_models import LocalizedText


def text(es: str, en: str, da: str) -> LocalizedText:
    return LocalizedText(spanish=es, english=en, danish=da)
```

`LocalizedText` rejects empty values. Use a meaningful description such as "Not applicable" rather than an empty string when a field is structurally required but not computationally relevant.

### Module shape

The following is a structural outline, not a complete course module:

```text
LocalizedLearningModule(
    course_code="GEN101",
    module_id="gen101.m01",
    title=LocalizedText(...),
    summary=LocalizedText(...),
    objectives=(LocalizedLearningObjective(...), ...),
    concepts=(LocalizedConceptBlock(...), ...),
    worked_examples=(LocalizedWorkedExample(...), ...),
    practice_exercises=(LocalizedPracticeExercise(...), ...),
    assessment_items=(LocalizedAssessmentItem(...), ...),
    tutor_support=LocalizedTutorSupportPacket(...),
)
```

## 3. Author the objective question bank

The interactive objective evaluator currently supports:

- `ActivityType.MULTIPLE_CHOICE`;
- `ActivityType.TRUE_FALSE`.

The default session contains six questions. Each module bank therefore needs at least six valid questions. A larger bank is preferred so repeated sessions vary meaningfully.

Use stable option IDs so answer identity remains independent of language:

```python
from computational_biomedicine_study_hub.content.localized_models import (
    LocalizedAssessmentItem,
    LocalizedAssessmentOption,
)
from computational_biomedicine_study_hub.learning import ActivityType

LOCALIZED_OBJECTIVE_QUESTION_BANK_01 = (
    LocalizedAssessmentItem(
        item_id="gen101.m01.bank.001",
        activity_type=ActivityType.MULTIPLE_CHOICE,
        prompt=text("Pregunta", "Question", "Spørgsmål"),
        options=(
            LocalizedAssessmentOption(
                option_id="option_a",
                text=text("Opción A", "Option A", "Mulighed A"),
            ),
            LocalizedAssessmentOption(
                option_id="option_b",
                text=text("Opción B", "Option B", "Mulighed B"),
            ),
        ),
        correct_option_ids=("option_a",),
        accepted_answers=(),
        explanation=text("Explicación", "Explanation", "Forklaring"),
    ),
)
```

Every bank item ID must begin with the complete module ID followed by a period.

## 4. Create validated bundles

In `content/gen101/__init__.py`, pair each localized module with its objective bank and content version.

```python
from computational_biomedicine_study_hub.content.bundles import (
    LocalizedModuleBundle,
    validate_bundle_catalog,
)
from computational_biomedicine_study_hub.i18n import AppLocale

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

BUNDLES = tuple(bundle.materialize(AppLocale.SPANISH_SPAIN) for bundle in LOCALIZED_BUNDLES)
```

Bundle validation checks:

- non-empty content versions;
- non-empty question banks;
- unique and correctly scoped item IDs;
- supported objective-question types;
- unique module IDs;
- one consistent course code per bundle catalog.

## 5. Link activities to objectives for persistent evidence

Questions can be displayed without persistence. To contribute to mastery, spaced review, and the error notebook, activities must be mapped to learning objectives.

Add an `ObjectiveLinkCatalog` in:

```text
src/computational_biomedicine_study_hub/content/objective_links.py
```

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

Register the catalog while preserving existing entries:

```python
_CATALOGS = {
    DM847_M01_OBJECTIVE_LINKS.module_id: DM847_M01_OBJECTIVE_LINKS,
    GEN101_M01_OBJECTIVE_LINKS.module_id: GEN101_M01_OBJECTIVE_LINKS,
}
```

`ObjectiveLinkCatalog.validate_against(...)` requires exact coverage of:

- guided practice exercises;
- authored assessment items;
- objective-bank questions.

It also rejects references to objectives that do not exist. Do not enable persistent recording until this mapping validates.

## 6. Create the course page

Create:

```text
src/computational_biomedicine_study_hub/courses/gen101.py
```

For a normal multi-module course, copy the structure of `courses/dm847.py` or `courses/bmb830.py` and update:

- content imports;
- page and reader class names;
- Qt object names;
- the course-code label;
- course metadata;
- specialized laboratory widgets, when needed.

The page must expose a locale-aware factory:

```python
def create_page(locale: AppLocale = DEFAULT_LOCALE) -> QWidget:
    return GEN101Page(locale)
```

Declare the course registration:

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
        AppLocale.SPANISH_SPAIN: "Resumen en español.",
        AppLocale.ENGLISH: "English summary.",
        AppLocale.DANISH_DENMARK: "Dansk resumé.",
    },
)
```

## 7. Register the course in the central catalog

Edit:

```text
src/computational_biomedicine_study_hub/courses/catalog.py
```

Add the import:

```python
from .gen101 import COURSE as GEN101
```

Add the registration to `COURSES`:

```python
COURSES: tuple[CourseRegistration, ...] = (
    DM857,
    DM847,
    BMB830,
    BMB831,
    GEN101,
)
```

The catalog automatically supplies the course to:

- the home page;
- the navigation sidebar;
- route registration;
- localized page headers.

`validate_catalog()` rejects duplicate course codes and routes.

Update `tests/test_course_catalog.py` so expected codes, routes, and ECTS totals match the new catalog.

## 8. Add optional full-progress integration

The current architecture uses explicit course-specific hooks for some tracked modular courses.

### Configure the progress recorder

When the new course page exposes `configure_progress_recorder(...)`, update:

```text
src/computational_biomedicine_study_hub/application.py
```

Follow the existing DM847 or DM857 pattern:

```python
from .courses.gen101 import configure_progress_recorder as configure_gen101_progress_recorder

# Inside main(...)
configure_gen101_progress_recorder(progress_service)
```

### Preserve module and tab location

`MainWindow` currently recognizes modular page classes explicitly. To preserve the selected module and tab across language changes and to open a module from review, update:

```text
src/computational_biomedicine_study_hub/ui/main_window.py
```

Add the new page class to:

- the imports;
- `ModularCoursePage`;
- `_modular_course_page(...)`.

This is not required for basic course navigation. It is required for the same location-restoration behavior provided to recognized modular pages.

## 9. Add tests

At minimum, test:

- course registration and route stability;
- required module sections;
- non-empty and unique IDs;
- complete ES, EN, and DA materialization;
- at least six valid objective questions per module;
- stable answer identities across locales;
- active evaluation rendering for every module;
- exact objective-link coverage when persistence is enabled;
- persistence under the expected course, module, item, and objective IDs;
- source catalogs and source audits when academic coverage claims are made;
- specialized executable examples or laboratories, when present.

Suggested files:

```text
tests/test_gen101_course.py
tests/test_gen101_content.py
tests/test_gen101_localization.py
tests/test_gen101_assessment.py
tests/test_gen101_objective_links.py
```

## 10. Validate before merging

Run the same checks as GitHub Actions:

```bash
ruff check .
ruff format --check .
mypy
pytest
```

Focused first pass:

```bash
pytest tests/test_course_catalog.py tests/test_gen101_*.py
```

Do not merge while content validation, localization, assessment integrity, or objective-link tests are failing.

# Removing a Course

## 11. Unregister it first

Edit:

```text
src/computational_biomedicine_study_hub/courses/catalog.py
```

Remove the course import and remove it from `COURSES`.

This removes the course from:

- the home-page course list;
- the navigation sidebar;
- route registration;
- normal application access.

Keeping the implementation files temporarily is useful when removal may be reversed or historical material must remain inspectable.

## 12. Remove course-specific integrations

When applicable, remove:

- progress-recorder imports and configuration from `application.py`;
- page imports from `ui/main_window.py`;
- the page class from `ModularCoursePage`;
- the page class from `_modular_course_page(...)`;
- course-specific persistent workflows;
- course-specific CLI entry points;
- course-specific datasets or registries no longer used.

Do not remove shared infrastructure used by other courses.

## 13. Update tests and documentation

Update:

- `tests/test_course_catalog.py`;
- tests that enumerate all courses;
- README course lists and totals;
- source-audit summaries;
- navigation and route expectations;
- documentation that names the removed course.

Search the complete repository before deleting files:

```bash
rg -n "GEN101|gen101" .
```

Review every match rather than deleting mechanically.

## 14. Decide whether to delete the implementation

For a permanent removal, delete the course-specific files after all references have been removed:

```text
src/computational_biomedicine_study_hub/courses/gen101.py
src/computational_biomedicine_study_hub/content/gen101/
tests/test_gen101_*.py
```

Retain source-license or provenance records when their preservation is legally or scientifically necessary.

## 15. Existing learner data

Unregistering or deleting course code does **not** automatically delete rows from the local SQLite progress database.

Consequences:

- historical attempts may remain stored but become unreachable through normal navigation;
- review items for an unregistered route may no longer open the original module;
- reusing retired IDs can attach old evidence to unrelated new content.

Therefore:

- never reuse retired identifiers for a different meaning;
- treat database cleanup as a separate migration;
- do not silently delete learner data during course removal;
- document any intentional migration or purge.

## Removal checklist

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

# New-course pull request checklist

```text
[ ] Stable course, route, module, objective, item, and option IDs
[ ] Complete ES, EN, and DA content
[ ] Required module collections are non-empty
[ ] At least six objective questions per module
[ ] Deterministic answer keys use stable option IDs
[ ] Content version assigned to every bundle
[ ] Objective links complete before persistence is enabled
[ ] Course registered in the central catalog
[ ] Location restoration added when required
[ ] Source basis and licensing reviewed
[ ] Course-specific and full test suites pass
```
