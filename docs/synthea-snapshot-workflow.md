# Reproducible Synthea CSV snapshot workflow

## Scientific boundary

Synthea generates synthetic, realistic-looking health records. These records are useful for software, data-engineering, statistical, visualisation, and validation practice without exposing real patients. They are not observations from real patients, do not establish clinical utility, and do not replace transcriptomics, proteomics, or other omics data.

Every Study Hub artifact derived from Synthea must retain `synthetic_data: true` and the following boundary:

> Synthetic Synthea records support technical and methodological practice; they are not real-patient or omics evidence.

## Why the repository does not commit the mutable `latest` archive

The official sample-data site exposes a `latest` CSV archive. That path can change when the maintainers regenerate sample data. Committing a large mutable archive would:

- obscure which generation was analysed;
- increase repository size;
- make updates difficult to review;
- encourage accidental treatment of one sample as an authoritative population.

The Study Hub therefore inspects a learner-owned local copy and records checksums, row counts, columns, and validation findings in a deterministic manifest.

## Obtain and extract a snapshot

Use the official Synthea sample-data page or generate your own population from the official Synthea project. For the public CSV sample, extract the archive into a dedicated directory such as:

```text
D:\datasets\synthea\csv-latest-2026-08-01\
├── patients.csv
├── encounters.csv
├── conditions.csv
├── observations.csv
└── ... additional Synthea tables
```

Do not edit files inside this source directory. Derived tables and reports belong in a separate analysis directory.

## Inspect the snapshot

After installing the Study Hub in editable mode, run:

```powershell
cb-synthea-inspect "D:\datasets\synthea\csv-latest-2026-08-01" `
  --source-label "official-latest-downloaded-2026-08-01" `
  --manifest "artifacts\synthea-manifest.json"
```

Linux or macOS:

```bash
cb-synthea-inspect data/synthea/csv-latest-2026-08-01 \
  --source-label official-latest-downloaded-2026-08-01 \
  --manifest artifacts/synthea-manifest.json
```

Exit status:

- `0`: all required contracts passed; warnings may still be present;
- `2`: at least one error was detected.

## Current minimum table contract

The inspector deliberately validates a stable subset of columns rather than requiring every optional or version-specific field.

### `patients.csv`

Required:

- `Id`
- `BIRTHDATE`
- `GENDER`

Validation:

- `Id` must be non-empty and unique.

### `encounters.csv`

Required:

- `Id`
- `START`
- `STOP`
- `PATIENT`
- `ENCOUNTERCLASS`
- `CODE`
- `DESCRIPTION`

Validation:

- `Id` must be non-empty and unique;
- every non-empty `PATIENT` must exist in `patients.Id`.

### `conditions.csv`

Required:

- `START`
- `PATIENT`
- `ENCOUNTER`
- `CODE`
- `DESCRIPTION`

Validation:

- every non-empty `PATIENT` must exist in `patients.Id`;
- every non-empty `ENCOUNTER` must exist in `encounters.Id`;
- blank encounter references are retained as warnings rather than silently removed.

### `observations.csv`

Required:

- `DATE`
- `PATIENT`
- `ENCOUNTER`
- `CODE`
- `DESCRIPTION`
- `VALUE`
- `UNITS`
- `TYPE`

Validation follows the same patient and encounter foreign-key rules.

## Manifest contents

The generated JSON manifest contains:

- source label;
- local root name, but not the full private path;
- explicit synthetic-data flag;
- file size;
- SHA-256 checksum;
- complete observed column order;
- row count;
- duplicate and blank primary-key counts;
- blank and orphan foreign-key counts;
- validation issues with severity;
- path-independent snapshot fingerprint;
- scientific-use boundary.

The fingerprint is calculated from file profiles and validation findings. Identical extracted data produce the same fingerprint even when stored in different directories or assigned different human-readable labels.

## What the inspector does not prove

A valid manifest means the local files satisfy the declared structural contract. It does not prove:

- epidemiological representativeness;
- statistical similarity to a real hospital population;
- correctness of every clinical code;
- absence of generator bias;
- clinical model validity;
- suitability for an omics pipeline;
- equivalence with an SDU assignment or official dataset.

These limitations must appear in reports and model cards that use Synthea.

## Priority-zero next use

The next BMB831 increment should consume a validated local snapshot to build one patient-level analytical table. It should:

1. define a cohort and index time;
2. retain only information available before index time;
3. aggregate repeated events at patient level;
4. keep patient IDs grouped during validation;
5. record intermediate dimensions;
6. produce a data dictionary and derived-table checksum;
7. state which conclusions remain synthetic-only.

## Sources

- SDU ODIN public BMB831 course description: `https://odin.sdu.dk/sitecore/index.php?a=searchfagbesk&internkode=BMB831&lang=en`
- Official Synthea repository: `https://github.com/synthetichealth/synthea`
- Official Synthea sample data: `https://synthetichealth.github.io/synthea-sample-data/`
- Official CSV data dictionary: `https://github.com/synthetichealth/synthea/wiki/CSV-File-Data-Dictionary`
